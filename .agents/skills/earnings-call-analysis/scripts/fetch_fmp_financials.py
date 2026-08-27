#!/usr/bin/env python3
"""Fetch bounded FMP quarterly statements and audit their continuity."""

from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path


ENDPOINTS = {
    "income_statement": "income-statement",
    "balance_sheet": "balance-sheet-statement",
    "cash_flow": "cash-flow-statement",
}


def parse_period(value: str) -> int:
    try:
        year_text, quarter_text = value.upper().split("-Q")
        year, quarter = int(year_text), int(quarter_text)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("period must look like 2026-Q3") from exc
    if quarter not in range(1, 5):
        raise argparse.ArgumentTypeError("quarter must be Q1 through Q4")
    return year * 4 + quarter - 1


def format_period(key: int) -> str:
    return f"{key // 4}-Q{key % 4 + 1}"


def row_key(row: dict) -> int:
    return parse_period(f"{row['fiscalYear']}-{row['period']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", required=True, type=str.upper)
    parser.add_argument("--coverage-first", required=True, type=parse_period)
    parser.add_argument("--coverage-last", required=True, type=parse_period)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--extra-quarters", default=4, type=int)
    parser.add_argument("--limit", default=40, type=int)
    parser.add_argument("--api-key-env", default="FMP_API_KEY")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        help="Use cached <dataset>.json files instead of network requests",
    )
    return parser.parse_args()


def download(endpoint: str, symbol: str, limit: int, api_key: str) -> tuple[list[dict], str]:
    public_query = urllib.parse.urlencode({"symbol": symbol, "period": "quarter", "limit": limit})
    source_url = f"https://financialmodelingprep.com/stable/{endpoint}?{public_query}"
    request_url = f"{source_url}&apikey={urllib.parse.quote(api_key)}"
    with urllib.request.urlopen(request_url, timeout=60) as response:
        payload = json.load(response)
    return payload, source_url


def write_csv(path: Path, rows: list[dict], source_url: str) -> None:
    headers = [*rows[0].keys(), "source_url"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "source_url": source_url})


def main() -> None:
    args = parse_args()
    if args.coverage_first > args.coverage_last:
        raise SystemExit("coverage-first must not be after coverage-last")
    if args.extra_quarters < 0:
        raise SystemExit("extra-quarters must be non-negative")

    requested_first = args.coverage_first - args.extra_quarters
    requested_last = args.coverage_last + args.extra_quarters
    args.output_dir.mkdir(parents=True, exist_ok=True)
    api_key = os.environ.get(args.api_key_env, "")
    if not args.raw_dir and not api_key:
        raise SystemExit(f"Environment variable {args.api_key_env} is not set")

    loaded: dict[str, list[dict]] = {}
    sources: dict[str, str] = {}
    for dataset, endpoint in ENDPOINTS.items():
        if args.raw_dir:
            raw_path = args.raw_dir / f"{dataset}.json"
            rows = json.loads(raw_path.read_text(encoding="utf-8"))
            source_url = f"cached:{raw_path.resolve()}"
        else:
            rows, source_url = download(endpoint, args.symbol, args.limit, api_key)

        if not isinstance(rows, list) or not rows:
            raise SystemExit(f"{dataset} returned no rows")
        if any(row.get("symbol") != args.symbol for row in rows):
            raise SystemExit(f"{dataset} contains a symbol other than {args.symbol}")
        bounded = [row for row in rows if requested_first <= row_key(row) <= requested_last]
        bounded.sort(key=row_key)
        if not bounded:
            raise SystemExit(f"{dataset} has no rows in the requested window")

        loaded[dataset] = bounded
        sources[dataset] = source_url
        write_csv(args.output_dir / f"{args.symbol}_quarterly_{dataset}.csv", bounded, source_url)

    effective_first = max(requested_first, min(row_key(row) for rows in loaded.values() for row in rows))
    effective_last = min(requested_last, max(row_key(row) for rows in loaded.values() for row in rows))
    audit_path = args.output_dir / f"{args.symbol}_quarterly_data_continuity.csv"
    incomplete = []
    with audit_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["period", *[f"{name}_date" for name in ENDPOINTS], "status"])
        for key in range(effective_first, effective_last + 1):
            dates = []
            complete = True
            for dataset in ENDPOINTS:
                found = next((row for row in loaded[dataset] if row_key(row) == key), None)
                dates.append(found.get("date") if found else "MISSING")
                complete = complete and found is not None
            status = "COMPLETE" if complete else "INCOMPLETE"
            writer.writerow([format_period(key), *dates, status])
            if not complete:
                incomplete.append(format_period(key))

    manifest = {
        "symbol": args.symbol,
        "period": "quarter",
        "coverage": {
            "first": format_period(args.coverage_first),
            "last": format_period(args.coverage_last),
        },
        "requestedWindow": {
            "first": format_period(requested_first),
            "last": format_period(requested_last),
        },
        "effectiveAvailableWindow": {
            "first": format_period(effective_first),
            "last": format_period(effective_last),
        },
        "futurePeriodsFabricated": False,
        "continuityExceptions": incomplete,
        "datasets": {
            name: {
                "rows": len(rows),
                "sourceUrl": sources[name],
                "csv": f"{args.symbol}_quarterly_{name}.csv",
            }
            for name, rows in loaded.items()
        },
        "continuityAudit": audit_path.name,
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    if incomplete:
        raise SystemExit(f"Continuity exceptions: {', '.join(incomplete)}")


if __name__ == "__main__":
    main()
