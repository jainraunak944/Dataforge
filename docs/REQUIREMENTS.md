# Requirement matrix — DataForge 2026 Pathway track

Source of authority: the uploaded brief `Pathway PS.pdf` (14 pages; page numbers below are the PDF's printed footer numbers). Status values: `pending` → `built` → `verified`. This file is updated as work completes.

## Mission requirements (brief p.07)

| # | Brief page | Requirement | Implementation | Verification | Status |
|---|---|---|---|---|---|
| M1 | 07 | One precise technical claim, falsifiable, written before code | `docs/CLAIM.md`; claim shown at top of app | Claim file predates `src/`; refutation paths listed | verified |
| M2 | 07 | Learner manipulates a real concept variable | Overlap slider ρ drives the live memory matrix; sandbox adds λ, repeats | Vitest: UI state = math state; browser smoke | verified |
| M3 | 07 | Immediate, meaningful consequence observed | Retrieved vector, error and matrix cells update live (<1 s) | Measured control-to-render latency in smoke test | verified |
| M4 | 07 | Compare output with ground truth / reference | "Desired vs retrieved" panel + independent explicit-history reference column | Independent reference module + equality tests | verified |
| M5 | 07 | Learner explains concept back | "Explain it back" section: prediction before held-out setting, deterministic feedback | Manual browser check; deterministic grader tests | verified |
| M6 | 07 | Where concept appears in BDH/BDH-CQ or differs | Integrated BDH module (section 5 of lesson) with equation walkthrough | Locators against arXiv:2509.26507 & 2608.09888 in `docs/RESEARCH.md` | verified |
| M7 | 07 | At least one limitation / failure case / misconception | ρ=1 ambiguity lesson step; limitations lists in app + README | Present in app section 6 & 7; README | verified |

## BDH module (brief p.08, must-have)

| # | Brief page | Requirement | Implementation | Verification | Status |
|---|---|---|---|---|---|
| B1 | 08 | BDH connection woven into flow, own learning objective | Lesson step 5 sits between sandbox and quiz; objective 5 in README | Flow order in `App.tsx` | verified |
| B2 | 08 | Say which system and why concept shows up there | BDH-GPU state equation named; BDH-CQ named separately | `src/content/bdh.tsx` + RESEARCH ledger | verified |
| B3 | 08 | Point to what's changing (state vs parameters) | Variable-role table with "changes during inference?" column; learner question | In-app table + quiz item | verified |
| B4 | 08 | Primary sources, not secondhand summaries | arXiv:2509.26507 + arXiv:2608.09888 fetched and quoted with equation numbers | `docs/RESEARCH.md` fetch log | verified |
| B5 | 08 | Toy/reimplementation identified as such, never presented as official | "Original toy computation" labels throughout; disclaimer in BDH module | Label audit in smoke test | verified |

## Submission package (brief p.10)

| # | Brief page | Requirement | Implementation | Verification | Status |
|---|---|---|---|---|---|
| S1 | 10 | Public artifact URL, no sign-in | GitHub Pages workflow prepared (`.github/workflows/deploy.yml`) | EXTERNAL GATE: repo owner must enable Pages | GATED — see submission/SUBMISSION_CHECKLIST.md (G1, G2) |
| S2 | 10 | Public source repository | Branch pushed to github.com/jainraunak944/dataforge | EXTERNAL GATE: repo visibility is owner's choice | GATED — see submission/SUBMISSION_CHECKLIST.md (G1, G2) |
| S3 | 10 | Blog as PDF | `submission/blog.pdf` + editable source `submission/src/blog.html` | Rendered, inspected, text-extractable | verified |
| S4 | 10 | Complete README | `README.md` (claim, audience, prerequisites, objectives, architecture, component roles, live/precomputed/synthetic/animated, reproduction, credits, licenses, disclosure) | Fresh-checkout follow-through | verified |
| S5 | 10 | Setup instructions for local components | README "Run it locally" | Clean `npm ci` + build in fresh checkout | verified |
| S6 | 10 | ≥3 recent primary papers (2022–2026) with citations beside claims | 2509.26507 (2025), 2608.09888 (2026), 2406.06484 (2024), 2412.06464 (2024) | `docs/RESEARCH.md` ledger; in-app references | verified |
| S7 | 10 | Source and license record | `docs/PROVENANCE.md` | Manual audit of every dependency/asset | verified |
| S8 | 10 | AI assistance / reuse disclosure | `docs/AI_DISCLOSURE.md` + mirrored in README | Present | verified |

## One-page concept summary (brief p.11–12)

| # | Brief page | Requirement | Implementation | Verification | Status |
|---|---|---|---|---|---|
| C1 | 11 | Exactly one readable PDF page, ~500–950 words | `submission/concept-summary.pdf` from `submission/src/concept-summary.html` | pdfinfo page count = 1; word count; text extraction | verified |
| C2 | 11 | Self-contained briefing for average data scientist | Definition, mechanism, comparison, evidence, limitations in one page | Read-through against rubric list | verified |
| C3 | 11 | Evidence labeled correctly (benchmark ≠ deployment etc.) | Evidence-category labels in summary | Cross-check against RESEARCH ledger | verified |
| C4 | 12 | BDH and BDH-CQ roles explained accurately | Dedicated paragraph, unequal roles acknowledged | Cross-check | verified |
| C5 | 12 | Most important limitation / open question identified | Interference + consolidation gap named | Present | verified |
| C6 | 12 | Primary citations beside claims | Inline bracketed citations | Links checked | verified |
| C7 | 12 | No AI slop: density, ownership | Every sentence carries definition/mechanism/evidence/limitation | Team read-through + defense guide | verified |

## Design standards (brief p.08 "Design standards")

| # | Requirement | Implementation | Status |
|---|---|---|---|
| D1 | One claim; cut everything else | Single lesson spine; no extra dashboards | verified |
| D2 | Substrate behaves before learner acts | Opens with populated ρ=0.6 example, live computation | verified |
| D3 | Visible state (shrunk model) | 2×2 matrix, every scalar visible | verified |
| D4 | Truth beside estimate | Desired / retrieved / reference side-by-side + L2 error | verified |
| D5 | Catchy: no blank canvas, no Run button | Preset already running on load | verified |
| D6 | Feedback < 1 s | Pure O(d²) math per interaction; measured | verified |
| D7 | Few controls, each maps to one real variable | ρ slider (lesson); λ, repeats, presets (sandbox) | verified |
| D8 | Guide then sandbox | 7-step guided flow, sandbox after | verified |
| D9 | No hidden limits; caps stated | History cap, ρ/λ bounds, write cap stated in-app | verified |

## Scoring rubric coverage (brief p.09)

| Category | Points | Where addressed |
|---|---|---|
| Technical correctness & depth | 25 | Memory core + independent reference + tests (`src/memory/`, `tests/`), RESEARCH ledger, honest labeling |
| Technical ownership & live defense | 15 | `docs/DEFENSE_GUIDE.md` (walkthrough, worked example, ~15 Q&A), `docs/ARCHITECTURE.md` |
| Learning effectiveness | 15 | Claim, audience+prereqs (README), 5 objectives, guided narrative, `docs/LEARNER_TEST.md` 60-second protocol |
| Interactive substrate & honesty | 15 | Live computation everywhere; truth-beside-estimate; state visibility; latency measurement; no painted values (tested) |
| BDH/BDH-CQ integration & evidence discipline | 10 | Integrated BDH module; evidence categories; explicit omissions |
| Craft, robustness, accessibility, provenance | 10 | Typography/palette, keyboard/focus/reduced-motion, mobile check, PROVENANCE.md, pinned lockfile |
| One-page concept summary | 10 | `submission/concept-summary.pdf` per C1–C7 |

## Ambiguity log

- The brief calls one required PDF "the blog" (p.10) and separately requires a one-page concept summary (p.11). We supply **both** clearly named PDFs; the one-page summary is the primary concept briefing. This is a conservative packaging choice, not an organizer clarification we invented.
- The brief's footer page numbers repeat "08" across three physical pages; matrix references use printed footer numbers.
- The brief links a NeurIPS 2026 Education Track deadline but states no DataForge deadline in the text we extracted; we do not invent one.
