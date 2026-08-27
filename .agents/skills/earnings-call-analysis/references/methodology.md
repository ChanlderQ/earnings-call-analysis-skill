# Methodology

## 1. Coverage and continuity

Create a coverage table with file, fiscal quarter, call date, period end, pages, prepared remarks, Q&A, and status. Order by the company's fiscal calendar, not filenames alone.

Classify continuity findings as `complete`, `missing`, `future_not_reported`, or `label_mismatch`. Resolve fiscal/calendar-year offsets before downloading financial data.

## 2. Financial baseline

Use the four reported quarters immediately before the earliest covered earnings release. Exclude the earliest covered quarter itself from the baseline.

At minimum calculate revenue and growth; GAAP gross and operating margins; net income, operating cash flow, capital expenditure, and free cash flow; cash and short-term investments; inventory, receivables, deferred revenue, and debt; and company-specific drivers such as purchase commitments or customer concentration when disclosed.

Flag one-time charges, acquisitions, accounting changes, and product-transition effects. Use non-GAAP figures only with a cited reconciliation.

## 3. Q&A coding

One coding unit is an analyst's complete question plus the corresponding management response. Multi-part questions can receive multiple labels.

Common topic labels include growth and guidance; demand and customer ROI; customer concentration; supply, power, inventory, purchase commitments, and deferred revenue; margins and pricing; competition and market share; product roadmap and TAM; capital allocation; and disclosure or accounting treatment.

Report both question count and percentage of complete question turns. State that labels are non-exclusive.

## 4. Response quality

Evaluate directness, quantification, deadline, modelability, consistency, and evidence. Use high/medium/low labels with a short reason.

Do not infer investor satisfaction from politeness. Use same-call repetition, later-quarter recurrence, explicit analyst challenge, and later disclosure added to close the gap. Call the result an inferred satisfaction proxy.

## 5. Statement classification

### Result commitment

A target for an eventual business outcome, such as revenue, margin, EPS, customer count, segment revenue, or market share. Prefer financial statements, filings, and non-GAAP reconciliations.

### Driver plan

An action intended to produce an outcome, such as procurement, inventory building, pricing, hiring, capacity reservation, capital expenditure, or repurchases. Accounting evidence usually verifies execution, not causality or success.

### Strategic narrative

A claim about platform advantage, technology leadership, TAM, design wins, ecosystem strength, or customer behavior. Require product, customer, industry, benchmark, or third-party evidence.

## 6. Verification states

- `delivered`: deadline passed and comparable evidence shows completion;
- `on_track`: deadline has not passed and current evidence supports progress;
- `deviated`: result or timeline has moved away from the original plan;
- `not_verifiable`: evidence or decision criteria are insufficient;
- `definition_changed`: scope, metric, customer set, product grouping, or stated number changed incompatibly.

Record update types separately: `new`, `maintained`, `raised`, `lowered`, `delayed`, `definition_changed`, or `discontinued`.

## 7. Accounting mapping

| Statement | Evidence |
|---|---|
| Revenue target | Income statement revenue |
| GAAP margin | Revenue, cost, and profit fields |
| Non-GAAP margin | Earnings release reconciliation |
| Inventory or supply build | Inventory, prepayments, cash flow, purchase-obligation notes |
| Acceptance delay | Deferred revenue and revenue-recognition notes |
| Extended payment terms | Receivables, DSO, allowance, and operating cash flow |
| Pricing | Revenue and margins plus ASP/mix disclosure |
| Repurchases/dividends | Financing cash flow and equity statement |
| Customer concentration | 10-Q/10-K concentration notes |
| Product or market share | Company product disclosure plus external evidence |

## 8. Completion-rate rules

A target enters the denominator only when it has a numeric target or objective pass/fail criterion, a clear deadline, a passed deadline, a comparable definition, and available evidence.

Report:

- `strict_rate = independently verified delivered targets / eligible independently verifiable targets`;
- `management_reported_rate = delivered targets including company-only operating disclosures / corresponding eligible targets`.

Show numerator, denominator, exclusions, and pending targets. Never treat a 100% short-term guidance rate as proof that long-term strategic claims are reliable.
