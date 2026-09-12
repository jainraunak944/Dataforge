# NAADI — Research log (claim → source register)

India Chem 2026 Youth Innovation Challenge · Team NIT Warangal (Raunak Jain,
Anushriya Bhattacharya). Working record — NOT part of the 8-slide submission.
Types: **F** = sourced fact · **C** = computed by team code (reproducible) ·
**E** = team estimate/judgment (labelled on slides) · **S** = standard (cited by number).

| # | Claim | Source | Link | Year | Excerpt / data point | Used on | Type |
|---|---|---|---|---|---|---|---|
| 1 | Competition rules: 8 slides max, submission format, 14 Sep deadline, AI-usage rule, evaluation criteria | Youth Innovation Challenge brief, DCPC (GoI) + FICCI | provided by team (PDF) | 2026 | "concept deck (maximum 8 slides)"; "presentations generated wholly or substantially by AI will be disqualified" | structure of all slides | F |
| 2 | Indian chemicals & petrochemicals demand expected to ~triple to USD 1 trillion by 2040 | PIB press release (Min. of PNG / DCPC context) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=1925546 | 2023 | "Chemicals & Petrochemicals demand in India expected to nearly triple and reach USD 1 Trillion by 2040" | Slide 8 footer | F |
| 3 | PdM effectiveness: 35–45% downtime reduction; 8–12% savings over preventive-only; 70–75% breakdown elimination; ~30–40% possible vs reactive | US DOE FEMP, O&M Best Practices Guide, Release 3.0, §5.4 (Predictive Maintenance) | https://www.energy.gov/sites/prod/files/2020/04/f74/omguide_complete_w-eo-disclaimer.pdf | 2010 | "Reduction in downtime: 35% to 45%; ... savings of 8% to 12% over ... preventive maintenance alone" (industry-average estimates attributed therein) | Slides 1, 3, 7, 8; economics model | F (foundational; no newer official range found) |
| 4 | ~89% of failure modes show no age-related wear-out pattern (aviation study; basis of RCM) | Nowlan, F.S. & Heap, H.F., *Reliability-Centered Maintenance*, US DoD report AD-A066579 | https://reliabilityweb.com (mirrors); DTIC AD-A066579 | 1978 | Six failure patterns; only ~11% age-related (4+2+5%), ~89% random-dominant | Slides 2, 8 | F (foundational) |
| 5 | Bearing and mechanical-seal degradation dominate centrifugal pump failure modes | McKee, K. et al., "A review of major centrifugal pump failure modes with application to the water supply and sewerage industries", ICOMS Asset Management Conference | https://espace.curtin.edu.au/handle/20.500.11937/28560 | 2011 | review identifies bearing and seal failures as principal recurring modes | Slides 2, 7 | F (peer-reviewed review) |
| 6 | CWRU seeded-fault bearing dataset (12 kHz drive-end + normal baseline); prototype metrics: 97.9% 4-class accuracy on unseen 3 hp load; 100/100% fault-vs-healthy precision/recall; 0/237 healthy windows misflagged; 98.9% grouped 5-fold CV; logistic baseline 97.2% | CWRU Bearing Data Center (dataset); metrics computed by `model/train_fault_model.py` (this repo) | https://engineering.case.edu/bearingdatacenter (mirror used: github.com/s-whynot/cwru-dataset) | data ~2000s; run 2026 | see `model/results/metrics.json`, `confusion_matrix.csv` | Slides 4, 5, 8 | C — **pending team re-run & ratification** |
| 7 | Vibration severity zones & condition-monitoring practice | ISO 20816-3:2022; ISO 13374-1:2003; ISO 17359:2018; ISO 14224:2016 | iso.org (paywalled; titles verified) | 2003–2022 | 20816-3: industrial machinery >15 kW in-situ vibration evaluation zones | Slides 3–6 | S |
| 8 | National AI/CPS policy anchors: NITI Aayog National Strategy for AI (#AIforAll); DST NM-ICPS approved 2018, ₹3,660 Cr, 25 Technology Innovation Hubs | NITI Aayog (2018); DST | https://www.niti.gov.in (NSAI PDF); https://dst.gov.in/national-mission-interdisciplinary-cyber-physical-systems-nm-icps | 2018 | NM-ICPS "total outlay of Rs.3660 Crores"; 25 TIHs | Slide 8 footer | F |
| 9 | SAMARTH Udyog Bharat 4.0 — MHI Industry 4.0 demo centres, MSME digital-maturity focus | Ministry of Heavy Industries / PIB | https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2084143 ; https://samarthudyog-i40.in/ | 2024 | four SAMARTH centres + 10 additional I4.0 centres (Phase II) | Slide 8 roadmap | F |
| 10 | Pumping systems ≈ 20% of the world's electric-motor energy demand | Hydraulic Institute, Europump & US DOE OIT, *Pump Life Cycle Costs: A Guide to LCC Analysis for Pumping Systems* | https://www.energy.gov/eere/amo (archived guide) | 2001 | "Pumping systems account for nearly 20% of the world's electrical energy demand" | Slide 7 | F (foundational) |
| 11 | Plant archetype: ₹500 Cr revenue, 30% contribution margin, 8,000 h/yr, 200 pumps, 25 bad actors, 60 h/yr downtime, 12 repairs/yr, ₹2.5 L/repair, 2 catastrophic events | Team assumption register | `economics/NAADI_pilot_economics.xlsx` (Assumptions sheet) | 2026 | every cell labelled; replaced by plant history in pilot P0 | Slides 2, 7 | E |
| 12 | Cost inputs: ₹35k/sensor point installed; ₹1.5 L/gateway; ₹10 L integration; ₹2 L training; ₹6 L/yr OpEx; ~₹1.5 L/pump all-in | Team estimates — **no vendor quotes yet** | same workbook | 2026 | flagged TEAM INPUT REQUIRED | Slides 4, 7 | E |
| 13 | Economics outputs: benefit ₹47.4 L/yr, net ₹41.4 L/yr, payback ~11 mo, 5-yr NPV @12% ≈ ₹1.1 Cr, payback ≤24 mo in stacked downside | Computed from #3 + #11 + #12 | `economics/CALCULATIONS.md` + workbook | 2026 | live formulas; sensitivity sheet | Slides 1, 7, 8 | C (on E inputs) |
| 14 | Slide-3 comparison matrix scores (2.3 / 3.0 / 2.9 / 2.9 / 4.3) and weights (30/20/10/10/10/20) | Team judgment from documented characteristics of each approach class | scoring note below | 2026 | — | Slide 3 | E |
| 15 | PESO approval required for equipment in Indian hazardous (explosive) areas; IECEx/ATEX-class intrinsically safe sensors specified | PESO (Petroleum & Explosives Safety Organisation), DPIIT | https://peso.gov.in | current | statutory approvals for Ex equipment | Slides 4, 7 | F (regulatory context) |
| 16 | IMS run-to-failure bearing dataset for future prognostics work | Qiu, H., Lee, J., Lin, J., Yu, G., *J. Sound & Vibration* 289 (2006); NASA Prognostics Data Repository | https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/ | 2006 | run-to-failure test data | roadmap (not on slides) | F |

## Verification notes / honesty flags

- **#3 (DOE ranges)**: 2010 guide is the newest official DOE source for these
  ranges; widely cited since. Used as a *range*, applied at the low end.
- **#6 (prototype)**: computed in this session by AI-assisted code. Per the
  competition's AI rule and our own process, the TEAM must re-run
  `python3 model/train_fault_model.py`, review the code, and only then present
  the numbers as team analysis. Until then they are draft numbers.
- **#5**: qualitative claim only (which modes dominate); no percentage is
  quoted on slides because per-mode percentages vary by study.
- **No primary research is claimed anywhere**: no interviews, surveys, plant
  visits, lab tests or vendor quotes exist. Slide 6/8 present the pilot as a
  proposal.
- **Live-link check pending**: engineering.case.edu was unreachable from this
  build environment (proxy policy); the GitHub mirror was used for data.
  TEAM: click-verify all URLs above from a normal connection before submission.

## Slide-3 matrix scoring note (Type E)

Criteria & weights (sum 100): detection lead time 30 · TCO 20 · skill
dependence 10 · data ownership 10 · retrofit ease 10 · MSME scalability 20.
Scores 1–5 per approach were set by team-AI judgment from: DOE FEMP programme
descriptions (#3), ISO 17359 practice (#7), and product-class characteristics
of portable-route analysis vs online OEM systems (public vendor documentation
classes, no specific vendor cited). The proposed stack's TCO/scalability
scores presume estimate #12 — they inherit its uncertainty.

## Team decision record

| Date | Decision | By |
|---|---|---|
| 12 Sep 2026 | Problem statement confirmed: AI-driven predictive maintenance (PS-7) | Team (chat message) |
| 12 Sep 2026 | Team member 2 details supplied: Anushriya Bhattacharya, B.Tech Chemical Engineering, 2nd year | Team |
| pending | Ratify assumption register (#11, #12), matrix scores (#14), prototype re-run (#6), final deck wording | **TEAM INPUT REQUIRED** |
