# India Chem 2026 — NAADI submission workspace

Team: Raunak Jain (Mech) · Anushriya Bhattacharya (Chem) — NIT Warangal.
Problem statement: AI-driven predictive maintenance (confirmed by team, 12 Sep 2026).

**STATUS: complete draft — awaiting team ratification (see checklist below).
Submission deadline: 14 Sep 2026 via NIT Warangal's official institutional email.**

## Contents

| Path | What it is |
|---|---|
| `deck/India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx` | **CURRENT deck (v2)**: purple redesign, infographic-led, references slide, speaker notes embedded |
| `deck/India_Chem_2026_NITW_Raunak_Anushriya_v2.pdf` | Visually identical PDF of v2 (rendered from the PPTX) |
| `deck/build_deck_v2.cjs` + `deck/strip_dashes.py` | Editable source that generates v2 (see rebuild steps below) |
| `deck/India_Chem_2026_NITW_Raunak_Anushriya.pptx` | Superseded v1 deck (navy/teal), kept for reference |
| `deck/India_Chem_2026_NITW_Raunak_Anushriya.pdf` | Superseded v1 PDF |
| `deck/build_deck.cjs` | v1 generator source |
| `model/train_fault_model.py` | Prototype fault-detection model (CWRU public data); rerun to reproduce metrics |
| `model/results/` | metrics.json, confusion_matrix.csv, feature_importances.csv from the last run |
| `economics/NAADI_pilot_economics.xlsx` | Live-formula economics workbook (blue+yellow cells = your inputs) |
| `economics/CALCULATIONS.md` | Human-readable calculation sheet: formulas, units, checks |
| `RESEARCH_LOG.md` | Claim → source register (fact/computed/estimate labels), scoring notes, decision record |
| `RESEARCH_DECISION_LOG.md` | Stage-1 record: constraints summary + problem-selection matrix |
| `SPEAKER_NOTES.md` | 10-minute presentation script (also embedded in PPTX notes) |
| `JURY_PREP.md` | 18 hard questions with answer directions |

Reproducing the model needs the public CWRU data:
`git clone --depth 1 https://github.com/s-whynot/cwru-dataset` and point
`DATA_ROOT` in `train_fault_model.py` at it (dataset ≈ 900 MB, not committed).

## TEAM RATIFICATION CHECKLIST — required before submission (AI-usage rule)

The competition disqualifies decks "generated wholly or substantially by AI".
This draft was co-created with AI assistance; it becomes yours by doing the
following, and should not be submitted before:

1. [ ] **Re-run the model yourselves** (`python3 model/train_fault_model.py`),
       read the code, and confirm you can explain windowing, the 16 features,
       GroupKFold and the unseen-load split (JURY_PREP.md rehearsal item).
2. [ ] **Ratify or change every yellow cell** in the economics workbook —
       especially plant archetype, 60 h/yr downtime, and sensor costs (no
       vendor quotes exist yet). Rebuild the deck if numbers change.
3. [ ] **Ratify the slide-3 matrix scores and weights** (RESEARCH_LOG.md
       scoring note) — they are judgment calls, and the jury may probe them.
4. [ ] **Rewrite at least the title-slide thesis and slide-8 takeaway in your
       own words**, and edit any sentence that does not sound like you.
5. [ ] **Click-verify every URL** in RESEARCH_LOG.md from a normal connection.
6. [ ] **Confirm name spellings**: "Anushriya Bhattacharya" (differs from
       "Shreya" in the original planning note) and "Raunak Jain", exactly as
       they should appear on certificates.
7. [ ] Approve use case (25 critical pumps, speciality-chem plant), preferred
       technology (wireless vibration + edge + RF classifier), and rejected
       alternatives (OEM cloud, offline routes, MCSA-first) — or direct changes.
8. [ ] Arrange the institutional submission: nodal officer, official email to
       indiachem@gov.in and indiachemconference@ficci.com, subject line
       "India Chem 2026 Submission – Youth Innovation Challenge – National
       Institute of Technology Warangal", by 14 Sep 2026.

## Rebuilding after edits (v2)

```bash
cd deck && npm i pptxgenjs             # once
node build_deck_v2.cjs                 # regenerate PPTX
python3 strip_dashes.py India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx  # zero em/en dashes rule
soffice --headless --convert-to pdf India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx
```

v2 conventions: white background on every slide; purple #5B2A86 as the only
primary accent (green = validated/positive, amber = risk/uncertainty);
per-claim citation numbers [1] to [11] resolved on slide 8; estimate and
calculation labels beside the numbers; no em or en dashes anywhere in the
file (the strip_dashes step also cleans the pptxgenjs slide-master bullets).
