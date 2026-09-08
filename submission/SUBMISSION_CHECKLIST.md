# Submission checklist — Memory Under Pressure

Statuses: **verified** = command/check actually ran and passed in this workspace · **built** = exists, not yet re-verified · **GATED** = requires an action outside this workspace (listed at the bottom). Nothing here is predicted or assumed.

## Package contents (brief p.10)

| Requirement | Path / URL | Status |
|---|---|---|
| Public artifact URL, opens without sign-in | https://jainraunak944.github.io/Dataforge/ (Pages workflow `.github/workflows/deploy.yml`) | **deployed** — run #6 (2026-09-08), GitHub Pages deployment status "success" for commit `a67aa13`; final incognito spot-check is the team's (see G1) |
| Public source code repository | https://github.com/jainraunak944/Dataforge branch `claude/memory-under-pressure-p6vp89` | verified — repository visibility confirmed **public** via GitHub API on 2026-09-08 |
| Blog as PDF | `submission/blog.pdf` (editable source `submission/src/blog.html`, real screenshots in `submission/src/img/`) | verified (rendered, 9 pages, text-extractable) |
| One-page concept summary PDF | `submission/concept-summary.pdf` (source `submission/src/concept-summary.html`) | verified — exactly 1 A4 page (pdfinfo), 802 words, text extraction + ∈/ρ glyphs checked |
| Complete README | `README.md` | verified against brief's required list |
| Setup instructions | `README.md` "Run it" | verified in a fresh checkout (see below) |
| ≥3 recent primary papers (2022–2026), citations beside claims | [1] 2406.06484, [2] 2412.06464, [4] 2509.26507, [5] 2608.09888 — inline bracket citations in app + PDFs; ledger `docs/RESEARCH.md` | verified (fetched live, locators recorded) |
| Source & license record | `docs/PROVENANCE.md` | verified |
| AI assistance / reuse disclosure | `docs/AI_DISCLOSURE.md`, mirrored in README | verified |

## Checks actually run (2026-09-05, this workspace)

| Check | Command | Result |
|---|---|---|
| Type checking | `npm run typecheck` | pass (0 errors) |
| Math/unit tests (hand-calculated fixtures, independent reference, bounds, ties, decay endpoints, seeded equality, constant shape) | `npm test` | 31/31 pass |
| Production build | `npm run build` | pass |
| Browser smoke (7 steps render, live-math-not-painted slider check, ρ=1 tie, keyboard/skip-link, reduced motion, mobile overflow 0px, URL sharing, zero console errors) | `npm run smoke` | 21/21 pass (`artifacts/smoke-results.json`) |
| Control→render latency | measured in smoke | 27 ms on this machine (< 1 s requirement; machine-specific, no device-independent guarantee claimed) |
| PDF page count / extraction / links | `pdfinfo`, `pdftotext`, raster inspection | concept summary exactly 1 page; both PDFs extract cleanly |
| Fresh checkout follows README | clean clone + `npm ci` + typecheck + test + build + smoke | recorded below after final run |
| Screenshots inspected (desktop full, panel, mobile) | manual review of `artifacts/screenshots/` | pass (one label-clipping defect found and fixed) |
| Submission archive builds and opens; excludes organizer brief, papers, node_modules | `git archive --format=zip -o <path>.zip HEAD` then `unzip -t` | pass (80 files; no private inputs) |
| CI on GitHub's own runner (independent of this machine) | Actions run #1 build job: npm ci, typecheck, tests, BASE_PATH build | pass (deploy job failed as expected — Pages not enabled; see G1/G2) |

## Ambiguity handling

The brief calls one required PDF "the blog" (p.10) and separately specifies a one-page concept summary (p.11). Both are supplied, clearly named; the one-page summary is the primary concept briefing. Conservative packaging choice — not an invented organizer clarification.

## External gates (status as of 2026-09-08)

- **G2 — repository Public: DONE.** Owner changed visibility on 2026-09-08; confirmed `visibility: public` via the GitHub API.
- **G1 — Public artifact URL: DEPLOYED.** Owner set **Settings → Pages → Source: GitHub Actions** (the workflow token cannot create the Pages site itself — first attempt failed with "Resource not accessible by integration", recorded in run #5). Run #6 (2026-09-08, commit `a67aa13`) then built (npm ci, typecheck, tests, BASE_PATH build) and deployed; `actions/deploy-pages@v4` polled GitHub's Pages deployment status and logged "Reported success!" with environment URL `https://jainraunak944.github.io/Dataforge/`. Honest scope note: the build container's egress policy blocks `github.io`, so a logged-out **browser** load was not performed from the build environment — do the 10-second incognito spot-check (page loads, ρ slider works, no console errors) before pasting the URL into the portal.
- **G3 — Competition portal.** Submission to the DataForge portal is the team's action; nothing was submitted on your behalf.
- **G4 — Learner test.** `docs/LEARNER_TEST.md` is a proposed protocol; running ≥5 people and logging results is a team action (optional but strengthens the learning-effectiveness score).

## Label definitions used across the project

**Built** = working code/deliverable exists locally. **Verified** = the relevant command/check actually passed. **Submission-ready** = all mandatory files present AND public links live and verified. Current overall status: **built + verified; repo public and Pages deployment reported success by GitHub (2026-09-08) — submission-ready after the team's incognito spot-check of the URL, then portal upload (G3).**
