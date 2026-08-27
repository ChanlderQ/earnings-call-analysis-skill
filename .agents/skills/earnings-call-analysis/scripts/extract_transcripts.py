#!/usr/bin/env python3
"""Extract text and page metadata from an earnings-call PDF directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--glob", default="*.pdf", help="PDF filename pattern")
    return parser.parse_args()


def safe_stem(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("_")
    return stem or "transcript"


def main() -> None:
    args = parse_args()
    try:
        import pdfplumber
    except ImportError as exc:
        raise SystemExit("pdfplumber is required: python3 -m pip install pdfplumber") from exc

    files = sorted(args.input_dir.glob(args.glob))
    if not files:
        raise SystemExit(f"No PDFs matched {args.glob!r} in {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source in files:
        with pdfplumber.open(source) as pdf:
            page_text = [page.extract_text(x_tolerance=2, y_tolerance=3) or "" for page in pdf.pages]
        text = "\n\n".join(
            f"=== Page {number} ===\n{content}"
            for number, content in enumerate(page_text, start=1)
        )
        destination = args.output_dir / f"{safe_stem(source.name)}.txt"
        destination.write_text(text, encoding="utf-8")
        entry = {
            "source": str(source.resolve()),
            "output": str(destination.resolve()),
            "pages": len(page_text),
            "characters": len(text),
            "contains_qa_marker": bool(re.search(r"\bQ\s*&\s*A\b|question", text, re.I)),
        }
        manifest.append(entry)
        print(json.dumps(entry, ensure_ascii=False))

    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
