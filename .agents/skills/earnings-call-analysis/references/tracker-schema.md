# Commitment Tracker Schema

Create one row per material forward-looking statement. Preserve the original target rather than overwriting it with later guidance.

## Required fields

| Field | Meaning |
|---|---|
| `statement_id` | Stable unique identifier |
| `classification` | `result_commitment`, `driver_plan`, or `strategic_narrative` |
| `topic` | Short normalized subject |
| `first_raised_period` | Fiscal quarter of first mention |
| `original_statement` | Concise faithful wording |
| `numeric_target` | Number, range, milestone, or blank |
| `has_numeric_target` | Boolean |
| `deadline` | Fiscal quarter, year, date, or blank |
| `has_clear_deadline` | Boolean |
| `accounting_mapping` | Statement, line item, note, or external evidence class |
| `update_trajectory` | Chronological summary of subsequent statements |
| `latest_update_period` | Most recent reviewed quarter |
| `update_type` | Normalized update type |
| `verification_state` | Normalized verification state |
| `evidence_grade` | `A`, `B`, or `C` |
| `commitment_quality` | `high`, `medium`, or `low` |
| `verification_conclusion` | Evidence-based explanation |
| `source_ids` | Transcript/filing/data references |
| `strict_denominator` | Boolean |
| `strict_delivered` | 1, 0, or blank |
| `management_denominator` | Boolean |
| `management_delivered` | 1, 0, or blank |

## Evidence grades

- `A`: directly verifiable from GAAP statements or filed notes.
- `B`: verifiable from an official reconciliation, supplemental table, or clearly mapped indirect financial evidence.
- `C`: relies mainly on management narrative, product claims, customer statements, benchmarks, or third-party evidence.

## Quality guide

- `high`: quantified, dated, stable definition, and grade A/B evidence.
- `medium`: missing one important element or dependent on indirect evidence.
- `low`: no measurable result, no deadline, unstable definition, or only grade C narrative evidence.

Do not merge a strategic narrative into a result commitment merely because management attached a large TAM number to it.
