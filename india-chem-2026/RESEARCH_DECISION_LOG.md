# India Chem 2026 Youth Innovation Challenge — Research & Decision Log

Team: Raunak Jain + Shreya, NIT Warangal
Status: **Stage 1 — problem-statement selection. Awaiting team confirmation before any deck design.**
This log is the working record required by the team's process. It is NOT part of the 8-slide submission.

Last updated: 12 September 2026 (session date)

---

## 1. Non-negotiable competition constraints (from the official brief, read in full)

Source: "Youth Innovation Challenge" brief, Department of Chemicals & Petrochemicals (GoI) + FICCI, India Chem 2026.

| # | Constraint | Detail |
|---|---|---|
| 1 | **Deadline** | Concept deck + participant details due **14 September 2026**, submitted **by the institution** (not the team) from the institute's official email ID. Late submissions not evaluated. |
| 2 | Routing | To **indiachem@gov.in** and **indiachemconference@ficci.com**. Subject line: *"India Chem 2026 Submission – Youth Innovation Challenge – [Name of the Institute/University]"*. Institutions nominate **one team**. |
| 3 | Deck size | Concept deck, **maximum 8 slides**, in the prescribed submission format. |
| 4 | Prescribed content | Problem Statement · Existing Scenario and Global Best Practices · Proposed Solution · Methodology for Execution · Technical Feasibility · Economic Feasibility · Supporting Evidence · Way Forward. |
| 5 | Team | Max 2 students, B.Tech./M.Tech., age 18–26, **one problem statement per team**, one entry per student. |
| 6 | One PS only | Team selects exactly one problem statement from the Annexure (13 listed). |
| 7 | Final round | Top 5 teams present offline at Bombay Exhibition Centre, Mumbai, **24 Oct 2026**: **10 min presentation + 5 min jury Q&A**. Jury: senior government officials, industry executives, academicians. Travel + stay (23–24 Oct) covered. |
| 8 | Evaluation criteria | Relevance to sector · Innovation & novelty · Technical/analytical depth · Feasibility & scalability · Presentation quality. |
| 9 | **AI rule** | AI permitted for research, data collection, information gathering. "Presentations generated wholly or substantially by AI **will be disqualified**. All submissions must demonstrate original analysis and critical thinking." → Team must contribute the decisive analysis, assumptions and decisions; this log records that trail. |
| 10 | Prizes | ₹50,000 / ₹30,000 / ₹20,000; participation certificates for finalists. |

⚠️ **Schedule risk flagged to team (12 Sep 2026): the institutional submission deadline is 14 Sep 2026 — two days away — and the submission must be routed through NIT Warangal's nodal officer / official institutional email. Confirming the problem statement and the institutional routing today is the critical path.**

## 2. Annexure problem statements (verbatim short forms)

PS-1 Distillation column energy reduction · PS-2 Solvent recovery & reuse from waste streams · PS-3 Green hydrogen production infrastructure · PS-4 Sustainable utilisation of a selected industrial waste · PS-5 ZLD strategy for a speciality chemical plant (max water recovery, min OpEx) · PS-6 Carbon capture technology evaluation for a medium-scale facility · PS-7 AI-driven predictive maintenance / digital reliability framework · PS-8 Plastic waste → chemicals/petrochemical feedstocks · PS-9 Water reuse & recycling framework · PS-10 Biodegradable/recyclable chemical packaging materials · PS-11 Bio-based specialty chemicals (e.g., plasticizers) · PS-12 Spent HCl (15–33%) recovery & purification (Cl₂, VOC, heavy-metal contaminated) · PS-13 Manufacturing technologies not available with Indian manufacturers.

## 3. Problem-selection decision matrix

**Method (team to ratify):** 9 criteria fixed by the team's brief; weights are a working proposal by the AI assistant, deliberately over-weighting *team fit* and *time-to-strong-submission* because of the 2-day deadline. Scores 1–5 are judgment calls based on the assistant's domain knowledge, **not sourced facts** — they are selection aids, not deck content.

Weights: Team fit 15 · Original analysis 12 · Public data 10 · Technical feasibility 10 · Economic demonstrability 10 · Pilot/prototype 8 · India relevance 10 · Differentiation 10 · Time-to-complete 15 (= 100).

| PS | Fit | Orig. | Data | Tech | Econ | Pilot | India | Diff. | Time | **Weighted /5** |
|---|---|---|---|---|---|---|---|---|---|---|
| **PS-7 Predictive maintenance** | 5 | 5 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | **4.70** |
| **PS-1 Distillation energy** | 5 | 4 | 4 | 5 | 5 | 3 | 5 | 3 | 4 | **4.27** |
| **PS-5 ZLD (speciality chem)** | 4 | 4 | 4 | 4 | 4 | 3 | 5 | 3 | 4 | **3.92** |
| PS-3 Green hydrogen | 4 | 4 | 5 | 4 | 4 | 3 | 5 | 2 | 4 | 3.92 |
| PS-9 Water reuse framework | 4 | 3 | 4 | 4 | 4 | 3 | 5 | 2 | 4 | 3.70 |
| PS-4 Industrial waste utilisation | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 4 | 3 | 3.32 |
| PS-2 Solvent recovery | 3 | 3 | 3 | 4 | 4 | 3 | 4 | 3 | 3 | 3.30 |
| PS-8 Plastic waste conversion | 3 | 3 | 4 | 3 | 3 | 2 | 4 | 3 | 3 | 3.12 |
| PS-12 Spent HCl recovery | 3 | 4 | 2 | 3 | 3 | 2 | 4 | 5 | 2 | 3.09 |
| PS-6 Carbon capture evaluation | 3 | 3 | 4 | 3 | 2 | 2 | 3 | 3 | 4 | 3.07 |
| PS-13 Technology localisation | 3 | 3 | 2 | 3 | 3 | 1 | 5 | 4 | 2 | 2.89 |
| PS-10 Chemical packaging | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2.85 |
| PS-11 Bio-based plasticizers | 2 | 3 | 3 | 2 | 3 | 1 | 4 | 4 | 2 | 2.64 |

### Key scoring rationale (assistant judgment, for team challenge)

- **PS-7 (4.70):** Only PS where the team can produce a *working, team-built artefact before the deadline*: train/validate a failure-prediction model in Python on public run-to-failure datasets (e.g., NASA C-MAPSS turbofan, NASA IMS / Case Western bearing data) and report real precision/recall — original analysis in the exact sense the AI rule demands. Mech fit (rotating equipment, vibration, failure modes) + Raunak's Python/data skills. Risks: "AI" attracts many shallow entries → must be narrowed to one asset class in one plant context with an economics layer; chem-sector jury will probe process specificity.
- **PS-1 (4.27):** Highest sector relevance (distillation dominates process-separation energy; figure to be sourced from IEA/DOE before use) and clean mech-eng fit (thermo, heat integration, MVR heat pumps). Original analysis = column energy balance + retrofit techno-economics in Python for one named column service. Risks: crowded topic; "pilot" is simulation + industrial pilot proposal, no physical prototype.
- **PS-5 (3.92):** Strong regulatory hook (CPCB ZLD framework) and water-stressed speciality-chem clusters; mech fit via evaporators/MVR compressors; original analysis = staged water-balance + cost-per-m³ optimisation. Risks: well-documented technology train → needs a sharp optimisation angle to avoid a textbook deck.
- **PS-3 (near-tie 3.92, not shortlisted):** Best public data (MNRE mission documents, IEA/IRENA), but likely the most-picked topic in the pool and "design the infrastructure" is broad → weakest differentiation (2/5). Kept as alternate if the team has a specific angle.
- **PS-12 (3.09) noted as the contrarian high-differentiation pick (5/5)** — few teams will attempt it — but public data on contaminant matrices is thin and doing it credibly in 2 days is unrealistic for a non-chemical team.

**Assistant recommendation (needs team decision): PS-7, with PS-1 as strong runner-up and PS-5 third.**

## 4. Design notes from reference decks (visual language only — no content/branding reuse)

- Zerodha-style deck: two-tone titles (dark + one accent keyword), thin title underline, 4-stat KPI strip, timeline rail, competitor table with generous row spacing, letter-medallion SWOT. Avoid: clip-art people, density.
- Swiggy Instamart deck: single accent colour, numbered section cards, comparison matrix, 2×2 positioning map, numbered source links. Avoid: long-scroll format, icon clutter.
- LinkedIn deck: icon-medallion card grid, star-rating comparison matrix, funnel visual (top-down vs bottom-up), per-claim inline citations. Avoid: heavy borders, mascots.
- To adopt (per team's visual direction): keyword-accent titles as full takeaway sentences, KPI strips, weighted decision matrix, editable vector PFD, direct labelling, numbered compact source footers, more whitespace than all three references.

## 5. Open items — [TEAM INPUT REQUIRED]

1. **Confirm one problem statement** (assistant recommends PS-7; team decides).
2. Shreya's surname and programme/branch (needed for the title slide — will not be invented).
3. Confirmation that NIT Warangal's nodal officer / official email routing is arranged before 14 Sep.
4. After PS confirmation: the team's own use-case choice, assumptions, preferred technology, rejected alternatives and final recommendation must be reviewed and approved by the team before the deck is finalised (AI-rule compliance).

## 6. Source register (running)

| # | Claim | Source | Year | Type |
|---|---|---|---|---|
| S1 | All rules/constraints in §1–§2 | Youth Innovation Challenge brief (DCPC, GoI + FICCI), provided by team | 2026 | Fact (primary document) |
| — | All matrix scores in §3 | Assistant judgment | 2026 | Estimate (to be ratified by team) |

No external research has been performed yet; all technical claims for the deck will be sourced once the PS is confirmed.
