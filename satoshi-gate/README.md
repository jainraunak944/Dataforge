# Project Satoshi Gate — Board deck content

Paytm × Liminal Custody Solutions case (case document + Modeling Clarification, September 2026).

| File | What it is |
|---|---|
| `SATOSHI_GATE_BOARD_DECK.md` | **Final content (v3, rated 96/100)**: title + 13 main slides + appendix A1–A9. Each block is a slide element. |
| `RATING_LOG.md` | Rubric, three brutal rating rounds (54 → 86 → 96), and the fixes applied between rounds. |
| `model/satoshi_gate_model.py` | Transparent accretion/dilution and transaction model. `python3 satoshi_gate_model.py` reprints every number in the deck. |
| `model/model_output.txt` | Current printout of the model (sections A–Q). |
| `versions/v1_blueprint_as_given.md` | The team blueprint as supplied (Round 1 baseline). |
| `versions/v2.md` | Intermediate version (Round 2). |

Tags used throughout: **CF** case fact · **CALC** arithmetic on case facts · **TA** team assumption (all listed with values on Slide 6).

Deliberate changes from the blueprint, with reasons in the deck:
- 25% → **26%** stake (one share above the 25% special-resolution threshold gives negative control), so ₹1,000 Cr → **₹1,040 Cr** at the pro-rata ceiling.
- The "1.6% mechanical dilution" figure is kept only as a footnote; the deck leads with the full year-1 EPS bridge (₹5.29, −29%).
- The earn-out is a schedule (₹1,650 Cr upfront + up to ₹1,310 Cr, linear 55–100% retention) rather than a principle.
- Decision gates carry thresholds; a downside matrix (churn × capital treatment) shows how the recommendation changes.
