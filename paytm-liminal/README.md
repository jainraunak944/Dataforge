# Project Satoshi Gate — Paytm × Liminal Custody Solutions

Deal-team deliverables for the M&A case competition (case document + Addendum 1, September 2026).

| File | What it is |
|---|---|
| `Paytm_Liminal_Board_Analysis.md` | The full written work: A. executive conclusion · B. 26 analytical sections (case deconstruction through recommendation) · C. text-only content for 13 slides + 2 appendix pages · D. judge Q&A (22 questions). |
| `Paytm_Liminal_Deal_Model.xlsx` | The single Excel financial model: 21 sheets, 21,662 formula cells, 166 named cells, zero formula errors after recalculation. Change the yellow levers on `Dashboard`; every sheet recalculates (valuation → FCF → leverage → EPS → transaction economics → decision thresholds). |
| `model_builder/` | Python scripts that generate the workbook (openpyxl) and a LibreOffice recalculation helper, kept for auditability. `python3 main.py out.xlsx` rebuilds it; `python3 uno_recalc.py out.xlsx` recalculates and scans for errors. |

## Conventions
- **Blue on light-blue** = CASE FACT (cell comment gives the case section). **Blue on yellow** = TEAM / ANALYST ASSUMPTION. **Blue on orange** = EXTERNAL FACT (sourced, dated). **Black** = formula. **Green** = link to another sheet. **Green fill** = key output.
- Case inputs are never replaced by outside figures. External research (comparables, precedents, regulatory sequence, public record of the parties) is labelled and used only for context and diligence.
- Base levers: Liminal ARR growth 20%, discount rate 13%, churn 37.5%, ₹750 Cr fixed cash drag, case financing mix.

## Headline results (base levers)
- Standalone DCF of Liminal ₹1,219 Cr (bull ₹2,480 Cr); ₹4,000 Cr needs 36.8% growth for ten years with zero churn and no reserve.
- Full acquisition: NPV −₹7,487 Cr; year-1 EPS ₹5.26 (−30%) from ₹7.50; FCF never breaks even; PV of the ₹750 Cr reserve ₹4,070 Cr; break-even drag negative.
- Recommended: commercial agreement + 26% at ≤ ₹650 Cr + growth-linked call option; maximum unconditional ₹665 Cr; base expectation Hold; exercise only if six gates clear.

## Provenance
Prepared with AI assistance (Claude Code) in a single session; all case facts were read from the uploaded PDFs; external facts carry URLs and dates on the `Sources` sheet.
