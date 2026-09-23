# Project Satoshi Gate — Brutal Rating Log

Judge stance: a finance-professor and M&A-practitioner panel scoring against the case's own asks (Mission, 5.1–5.6, Expected Output 1–8) and the Modeling Clarification. Scores are deliberately harsh; a slide that asserts without a number scores as if the number were missing.

## Rubric (100)

| # | Criterion | Pts | What earns full marks |
|---|---|---|---|
| 1 | Strategic verdict & rationale (5.1) | 12 | One clear path; why not the other three; partnership-vs-ownership answered; opportunity sized against the risk of leaving the core |
| 2 | Customer churn defence (5.2) | 12 | Return profile under 30–45% churn; a stated churn tolerance; specific governance safeguards; retention economics |
| 3 | Capital, financing & valuation (5.3) | 20 | Cash/debt/equity mix vs EPS from ₹7.50; implied multiple and supportability; breakeven with the ₹750 Cr drag; MDR offset quantified; deferred/earn-out/CVR structures |
| 4 | Regulatory path (5.4) | 10 | Sequence before/at/after; capital-requirement question; operating controls |
| 5 | Competitive risk (5.5) | 8 | Outbid response; multiple-compression answer; implications of consortium ownership |
| 6 | Contingency planning (5.6) | 10 | >45% remediation/unwind; minority-then-option; milestones; standalone indefinitely; walk-away after signing |
| 7 | Model rigour & assumption discipline | 14 | Dedicated assumptions slide with values; facts ≠ calcs ≠ assumptions; PAT and FCF breakeven both shown; sensitivities; reproducible model |
| 8 | Board-readiness | 14 | Answer first; action titles; internally consistent numbers; 10–15 slides; roadmap with triggers; no filler |

---

## Round 1 — v1, the blueprint as supplied (`versions/v1_blueprint_as_given.md`)

| # | Criterion | Score | Findings |
|---|---|---|---|
| 1 | Strategic verdict | 8/12 | Clear recommendation and good "access before control" framing. "25% as a midpoint" is arbitrary. Partnership-only is dismissed in one line without the security-of-supply argument. No view on why Liminal's shareholders would accept. |
| 2 | Churn defence | 7/12 | Churn table is correct and useful. No P&L impact of churn (a 37.5% revenue loss on a breakeven cost base is a loss, not zero). The explicit case question "what level of churn makes the deal unattractive" is not answered. Governance list is generic; founder/management retention absent. "Reversibility: High" for a private minority is overstated. |
| 3 | Capital / financing / valuation | 8/20 | The EPS bridge stops at "1.6% mechanical dilution before financing costs" when the case says EPS impact comes *primarily* from new shares and financing costs: the dominant effect is omitted. No cash/debt/equity mix comparison, though 5.3 asks for it. No breakeven year on either PAT or FCF, though 5.3 asks "how long". MDR offset not quantified. Control-tranche financing "not pre-committed" reads as a dodge. No leverage or liquidity metrics. |
| 4 | Regulatory | 6/10 | Reasonable checklist. Not mapped to Phase 1 vs control. Capital question correctly flagged as decisive but not connected to any number. |
| 5 | Competitive | 5/8 | Sound principle ("don't match"), no reservation value, no observation that the consortium inherits the same wallet conflict, stock-compression handled qualitatively. |
| 6 | Contingency | 6/10 | Playbook exists. Milestones unquantified. ">45% remediation/unwind" is one line. "Standalone indefinitely" not answered. |
| 7 | Model rigour | 5/14 | The assumptions slide lists assumption *names* without values, which does not satisfy the Modeling Clarification ("listing all material assumptions used in their financial model"). PAT and FCF breakeven are formulas, not results. No model. |
| 8 | Board-readiness | 9/14 | Good action titles and flow. Slides 7, A2, A3 repeat each other; "not specified — validate" appears four times in the options table; decision gates have no thresholds; text-heavy. |
| | **Total** | **54/100** | Structurally right, numerically hollow. A judge would say: "You told me what to model. Where is the model?" |

### Fixes commissioned for Round 2
1. Build a transparent model (`model/satoshi_gate_model.py`) and put values on every assumption.
2. Full EPS bridge including foregone interest, debt cost and post-churn loss; five financing mixes; leverage and liquidity per mix.
3. PAT and FCF breakeven years for full acquisition, Phase 1 and control; 10-year table.
4. Quantify the MDR offset (gross and after conversion); keep it outside the deal.
5. "What you need to believe" DCF and a stated churn tolerance.
6. Replace 25% with 26% and give the statutory reason; add ROFR/ROFO and the seller's perspective.
7. Convert the earn-out into a schedule tied to the case's churn range.
8. Quantify decision gates; add a downside matrix (churn × capital treatment).
9. Add founder/management retention and client-auditable governance mechanics.

---

## Round 2 — v2 (`versions/v2.md`)

| # | Criterion | Score | Findings |
|---|---|---|---|
| 1 | Strategic verdict | 11/12 | Strong. Missing: an honest statement of the strategic premium in the ₹1,040 Cr ceiling versus fundamental value, and a "base expectation is Hold" admission that pre-empts the "isn't this just a minority stake?" challenge. |
| 2 | Churn defence | 10/12 | Tolerance answered (earn-out floor; >45% never exercise). Governance concrete. Retention-economics sentence mixes what sellers receive (₹291 Cr per 10 pts) with headline value (₹400 Cr) without saying they differ. No remediation/unwind ladder for >45%. |
| 3 | Capital / financing / valuation | 18/20 | Mix table, breakevens, MDR offset and DCF all present and consistent. Missing a sources-and-uses table, the like-for-like MDR baseline (₹8.58) beside the ₹7.89, and the accounting treatment (associate vs consolidation). "3.4% of the company" should be 3.3%. |
| 4 | Regulatory | 8/10 | Good sequencing by phase. No indicative timelines. "Does owning custody create additional requirements" not answered as a sentence. "Arm's-length indefinitely" only implicit. |
| 5 | Competitive | 7/8 | Consortium's shared conflict and Mastercard's edge both noted. Fallback thin; shareholder justification under compression could cite the 0.9%-of-market-cap cheque. |
| 6 | Contingency | 8/10 | Matrix is the right tool. >45% path is one cell; needs a dated ladder. |
| 7 | Model rigour | 13/14 | 20 valued assumptions, both breakevens, sensitivities, script. Slide 11 claims "even ₹100 Cr/yr breaks the gate" before the model prints that check. |
| 8 | Board-readiness | 11/14 | Dense; "put-free" and similar slips; Board ask lacks the authorisations being requested; JV column says "not modelled" twice with no design sketch. |
| | **Total** | **86/100** | Now a real board deck. Remaining gaps are honesty statements, one missing plan (>45% ladder), one missing table (sources & uses), and polish. |

### Fixes applied in Round 3
1. Slide 1: "Base expectation: Hold" paragraph; four Board authorisations; cheque as 0.9% of market cap.
2. Slide 2: sized answer to "large enough to leave the core?"; cost of walking away.
3. Slide 4: JV design sketch and its role as fallback; reversibility wording fixed.
4. Slide 5: fundamental value of 26% (₹456–951 Cr) and the premium; negotiating target; veto-vs-ROFR clarity; earn-out measurement rules (audited, Paytm revenue excluded); "cap 16% below bull DCF"; fallback if the option is refused; accounting treatment.
5. Slide 7: supportability answered in one paragraph; drag NPV folded into the WYNTB conclusion.
6. Slide 8: sources & uses; ₹8.58 like-for-like; consolidation note; 3.3%.
7. Slide 9: "how much recurring capital cost can control bear" with the model's ₹50/₹100 Cr checks.
8. Slide 10: retention-economics sentence corrected; "how significant is the risk" answered directly.
9. Slide 11: indicative timelines (TA); direct answer on additional requirements.
10. Slide 12: remediation and unwind ladder (day 30/90/180); shareholder justification line.
11. Slide 13: Gate 2 quantified with the model's thresholds; "indefinitely" answered for associate and subsidiary; walk-away after signing.
12. Model: sections O (Phase-1 value), P (capital-cost gate check), Q (sources & uses) added so every deck claim prints from the script.

---

## Round 3 — v3, final (`SATOSHI_GATE_BOARD_DECK.md`)

| # | Criterion | Score | Residual findings |
|---|---|---|---|
| 1 | Strategic verdict | 12/12 | Path, alternatives, partnership question, size-of-prize, walk-away cost and base expectation all stated with numbers. |
| 2 | Churn defence | 12/12 | Return profile at 30/37.5/45%; tolerance defined; auditable governance; retention economics; remediation ladder. |
| 3 | Capital / financing / valuation | 19/20 | Complete. Residual: PPA amortisation and goodwill are flagged, not quantified; a judge could ask for the number. |
| 4 | Regulatory | 9/10 | Sequenced with timelines and the decisive capital question. Residual: approval names are hedged ("as applicable") because the case supplies no regulatory detail; a team with counsel input could firm these up. |
| 5 | Competitive | 8/8 | Reservation value, "let them win" logic, consortium's own conflict, compression answer, fallback. |
| 6 | Contingency | 10/10 | Matrix, ladder, milestones, indefinite hold, post-signing walk-away. |
| 7 | Model rigour | 14/14 | 21 valued assumptions with ranges; PAT and FCF breakeven for every path; every claim printed by the script. |
| 8 | Board-readiness | 12/14 | Answer-first, consistent, 13 + 9 slides, quantified gates. Residual: content density is high for a 13-slide deck; the team must cut text to visuals in layout, and Slides 5 and 8 each carry two tables that may need splitting into a main slide plus appendix. |
| | **Total** | **96/100** | Target of 95+ met. Remaining points are layout and two optional numbers, not substance. |

### What would take it to 98–100 (optional)
- Quantify PPA amortisation under a stated intangible allocation (e.g., 25% of price over 8 years) and show reported EPS with it.
- Bring counsel-verified names and timings for the RBI, competition and securities steps.
- Convert Slides 5 and 8 into one visual each (earn-out curve; financing-mix bar chart) and push the tables to A3/A4.
