# Earnings Call Analysis Skill

A portable Codex skill for analyzing a multi-quarter series of earnings-call transcripts and verifying management commitments against later financial statements.

The skill is stored at:

```text
.agents/skills/earnings-call-analysis/
```

## What it does

- audits transcript-quarter continuity and fiscal/calendar-year alignment;
- limits financial data to four quarters before and up to four available quarters after the covered calls;
- builds a pre-call financial baseline;
- codes complete analyst Q&A turns with non-exclusive topics;
- evaluates management response directness and inferred investor satisfaction;
- classifies management statements as result commitments, driver plans, or strategic narratives;
- maps targets to accounting or external evidence;
- tracks maintained, raised, lowered, delayed, redefined, and discontinued targets;
- calculates strict financial and management-reported completion rates separately.

## Use in Codex

Clone the repository and open it as a Codex project. Codex discovers repository-level skills under `.agents/skills`.

Invoke it explicitly with:

```text
$earnings-call-analysis analyze the earnings-call PDFs in this directory.
```

Or use a more specific request:

```text
$earnings-call-analysis check transcript continuity, download the bounded FMP financial window, analyze recurring investor concerns, and verify management targets.
```

## Requirements

- Python 3.10 or later
- `pdfplumber` for PDF transcript extraction
- An FMP API key when downloading financial statements

Install the PDF dependency:

```bash
python3 -m pip install pdfplumber
```

Set the FMP key without committing it:

```bash
export FMP_API_KEY="your-key"
```

PowerShell:

```powershell
$env:FMP_API_KEY = "your-key"
```

## Reusable scripts

Extract transcript text and page metadata:

```bash
python3 .agents/skills/earnings-call-analysis/scripts/extract_transcripts.py \
  --input-dir /path/to/transcripts \
  --output-dir tmp/transcripts
```

Download quarterly FMP statements and audit continuity:

```bash
python3 .agents/skills/earnings-call-analysis/scripts/fetch_fmp_financials.py \
  --symbol NVDA \
  --coverage-first 2026-Q3 \
  --coverage-last 2027-Q2 \
  --output-dir data/fmp/nvda
```

The FMP script writes bounded income-statement, balance-sheet, and cash-flow CSVs, plus a continuity audit and manifest. It does not store the API key in generated files and does not fabricate future quarters.

## Skill contents

```text
earnings-call-analysis/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── methodology.md
│   ├── report-template.md
│   └── tracker-schema.md
└── scripts/
    ├── extract_transcripts.py
    └── fetch_fmp_financials.py
```

## Verification principles

- A quantified target without a deadline does not enter the completion-rate denominator.
- `On track` is not the same as `delivered`.
- Non-GAAP targets require the corresponding reconciliation.
- A changed definition is not completion of the original target.
- Strategic narratives require customer, product, industry, benchmark, or third-party evidence.
- Management-reported operating targets remain separate from independently verified financial targets.

Source transcripts, financial data, API credentials, company analysis, and temporary outputs are intentionally not included in this repository.

