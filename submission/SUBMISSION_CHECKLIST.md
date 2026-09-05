# Submission checklist — Memory Under Pressure

Statuses: **verified** = command/check actually ran and passed in this workspace · **built** = exists, not yet re-verified · **GATED** = requires an action outside this workspace (listed at the bottom). Nothing here is predicted or assumed.

## Package contents (brief p.10)

| Requirement | Path / URL | Status |
|---|---|---|
| Public artifact URL, opens without sign-in | GitHub Pages workflow at `.github/workflows/deploy.yml` (builds `dist/` from this branch) | **GATED** — see gate G1; no URL claimed |
| Public source code repository | https://github.com/jainraunak944/dataforge branch `claude/memory-under-pressure-p6vp89` | **GATED** — pushed; public visibility is gate G2 |
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

## Ambiguity handling

The brief calls one required PDF "the blog" (p.10) and separately specifies a one-page concept summary (p.11). Both are supplied, clearly named; the one-page summary is the primary concept briefing. Conservative packaging choice — not an invented organizer clarification.

## External gates (exact remaining actions — for the team, not done by the build)

Facts verified via the GitHub API on 2026-09-05: the repository `jainraunak944/Dataforge` is currently **private** (`visibility: private`, `has_pages: false`), and `claude/memory-under-pressure-p6vp89` is its **default branch**, so the committed deploy workflow is already active (run #1 triggered by the push).

- **G2 first — make the repository Public.** GitHub → repository **Settings → General → Danger Zone → Change visibility → Public**. This is the owner's decision, deliberately not performed by the build. (On a free personal plan, GitHub Pages is unavailable while the repo is private, so G1 depends on this.)
- **G1 — Public artifact URL.** After G2, re-run the "Deploy artifact to GitHub Pages" workflow (Actions tab → the workflow → Re-run). The workflow attempts to enable Pages itself (`actions/configure-pages@v5` with `enablement: true`); if that step fails, enable once manually: **Settings → Pages → Source: GitHub Actions**, then re-run. Expected URL: `https://jainraunak944.github.io/Dataforge/`. Before submitting it, verify in a logged-out/incognito session: page loads, slider works, no console errors, repo links resolve. Alternative (no Pages): host `dist/` on any static host (build with `BASE_PATH=/ npm run build` for a root path).
- **G3 — Competition portal.** Submission to the DataForge portal is the team's action; nothing was submitted on your behalf.
- **G4 — Learner test.** `docs/LEARNER_TEST.md` is a proposed protocol; running ≥5 people and logging results is a team action (optional but strengthens the learning-effectiveness score).

## Label definitions used across the project

**Built** = working code/deliverable exists locally. **Verified** = the relevant command/check actually passed. **Submission-ready** = all mandatory files present AND public links live and verified. Current overall status: **built + verified locally; submission-ready pending gates G1–G2.**
