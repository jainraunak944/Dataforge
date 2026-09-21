# BGCC Case Consilium 2026, Round 3 (FanCode): "Earn the Second Occasion"

Submission build for the Round 3 case on converting irregular ATP Tour interest into incremental, retained and profitable
subscription growth for FanCode in India. Everything here is reproducible from the model and the generator.

## Deliverables

| File | Purpose |
|---|---|
| `deck/out/TEAMNAME_BGCCR3.pdf` | **Provisional submission file** (12 pages: cover, executive summary, 8 solution slides, 2 reference pages). Rename after the team name is filled in: `<REGISTERED_TEAM_NAME>_BGCCR3.pdf`. |
| `deck/out/TEAMNAME_BGCCR3.pptx` | Matching editable working deck (native text, tables and charts; nothing is flattened). |
| `model/` | Central assumptions (`assumptions.json`), the cohort/pricing/channel model (`model.py`) and its outputs (`outputs/*.csv`, `outputs/model_outputs.json`). Every financial number on the slides is read from `model_outputs.json`. |
| `research/` | Case-facts register, requirement-to-slide checklist, source ledger (CSV), IST calendar, private decision memo and slide argument. |
| `deck/` | Generator (`build_deck.js`, `theme.js`), fonts (Poppins and Inter, SIL OFL) and `package.json`. |
| `inputs/` | Copy of the master prompt. The three design-reference PDFs stay in the upload folder (git-ignored here). |

## Regenerate with the team's details

```bash
cd deck && npm install                      # once
cd ../model && python3 model.py             # rebuilds outputs/*.csv and model_outputs.json
cd ../deck && TEAM_NAME="Exact Registered Name" TEAM_MEMBERS="A, B, C" INSTITUTION="BITS Goa" node build_deck.js
python3 <pptx-skill>/scripts/office/soffice.py --headless --convert-to pdf "out/Exact Registered Name_BGCCR3.pptx"
```

The cover shows orange placeholders until the environment variables are set. The PDF was exported with LibreOffice
24.2 (Impress) with Inter and Poppins installed and embedded; PowerPoint users should install the two fonts from
`deck/fonts/` before editing the PPTX, otherwise a substitute font may reflow a few dense tables.

## What the team must resolve before uploading

1. **Team identity**: registered team name, member names and institution (cover), then rename the PDF.
2. **Case PDF verification**: the case brief was not available in the build session. All case inputs (CF1-CF19) and the
   submission rules were taken from the master prompt's register; check every CF and page reference against the PDF.
3. **Deadline**: the case lists 19 September 2026, 11:59 PM IST; this build ran on 21 September 2026 and no organizer
   extension was found or supplied. Confirm with the organizers before relying on the upload.
4. **Unverified items disclosed in the deck**: Tennis TV's live availability in India under FanCode's exclusivity;
   session start times (typical of recent editions, to be confirmed against the 2026 orders of play); CRM planning pools.

## Evidence and method notes

- Evidence cut-off: sources published on or before 19 September 2026, accessed 21 September 2026 through search-index
  copies (the build environment could not open the sites directly). See `research/source_ledger.csv`.
- Contribution = price / 1.18 (18% GST assumed included) - 4% of gross (gateway, support) - Rs 2 per streaming hour.
  The fixed ATP rights fee is excluded: contribution is not profit.
- CAC is reported attributed and incremental; new payers (first FanCode payment) are separated from existing-payer ATP
  purchases; retention metrics are defined on matured cohorts only.
