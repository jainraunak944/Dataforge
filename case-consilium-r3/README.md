# BGCC Case Consilium 2026, Round 3 (FanCode): Wookies submission build (v2 visual redesign)

Submission build for the Round 3 case on converting irregular ATP Tour interest into incremental, retained and profitable
subscription growth for FanCode in India. Everything here is reproducible from the model and the generator.

## Deliverables

| File | Purpose |
|---|---|
| `deck/out/Wookies_BGCCR3.pdf` | **Submission file** (12 pages: cover, executive summary, 8 solution slides, 2 reference pages), team Wookies. |
| `deck/out/Wookies_BGCCR3.pptx` | Matching editable working deck (native text, tables, charts and diagrams; nothing is flattened). |
| `qa/v2/Wookies_BGCCR3_contact_sheet.png` | Contact-sheet preview of the 12 pages. |
| `deck/out/v1/` | The first (text-heavy) build, kept for reference only. |
| `model/` | Central assumptions (`assumptions.json`, v2) and the cohort/pricing/channel model (`model.py`, v2) with outputs in `outputs/` (`model_outputs.json` feeds the generator). v1 files are kept as `assumptions_v1.json` / `model_v1.py`. |
| `research/` | Case-facts register, requirement checklist, source ledger (CSV), IST calendar, decision memo, v2 slide specification and the private audit change log (`change_log_v2.md`). |
| `deck/` | v2 generator (`build_v2.js`, `theme2.js`; v1 kept as `build_deck.js`, `theme.js`), fonts (Poppins and Inter, SIL OFL) and `package.json`. |
| `inputs/` | Copy of the master prompt. The three design-reference PDFs stay in the upload folder (git-ignored here). |

## Regenerate

```bash
cd deck && npm install                      # once
cd ../model && python3 model.py             # rebuilds outputs/*.csv and model_outputs.json
cd ../deck && node build_v2.js              # writes out/Wookies_BGCCR3.pptx and prints per-page word counts
python3 <pptx-skill>/scripts/office/soffice.py --headless --convert-to pdf out/Wookies_BGCCR3.pptx
```

The PDF was exported with LibreOffice 24.2 (Impress) with Inter and Poppins installed and embedded; PowerPoint users
should install the two fonts from `deck/fonts/` before editing the PPTX.

## What the team must resolve before uploading

1. **Case PDF verification**: the case brief was not available in the build session. All case inputs (CF1-CF19) and the
   submission rules were taken from the master prompt's register; check every CF and page reference against the PDF.
2. **Deadline**: the case lists 19 September 2026, 11:59 PM IST; this build ran on 21 September 2026 and no organizer
   extension was found or supplied. Confirm with the organizers before relying on the upload.
3. **Unverified items disclosed in the deck**: Tennis TV's live availability in India under FanCode's exclusivity;
   session start times (typical of recent editions, to be confirmed against the 2026 orders of play); CRM planning pools; the 2027 season tariff (assumed ₹399); Monthly Pass tour inclusions.

## Evidence and method notes

- Evidence cut-off: sources published on or before 19 September 2026, accessed 21 September 2026 through search-index
  copies (the build environment could not open the sites directly). See `research/source_ledger.csv`.
- Contribution = price / 1.18 (18% GST assumed included) - 4% of gross (gateway, support) - Rs 2 per streaming hour.
  The fixed ATP rights fee is excluded: contribution is not profit.
- CAC is reported attributed and incremental; new payers (first FanCode payment) are separated from existing-payer ATP
  purchases; retention metrics are defined on matured cohorts only.
