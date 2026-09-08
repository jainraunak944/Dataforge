# Build status

Last update: 2026-09-08 (deployment completed)

## Deployment (2026-09-08)

- Repo made **public** by the owner; confirmed `visibility: public` via GitHub API.
- Owner enabled Pages (Settings → Pages → Source: GitHub Actions) — required because the workflow token cannot create the Pages site (run #5 recorded "Resource not accessible by integration").
- Workflow run #6 (commit `a67aa13`): build green on GitHub's runner; `actions/deploy-pages@v4` logged "Reported success!"; environment URL `https://jainraunak944.github.io/Dataforge/`.
- Not verified from the build container: a logged-out browser load of the URL (egress policy blocks github.io here). Team spot-check in incognito before portal upload.

## Completed and verified (commands actually ran in this workspace)

- Full 14-page brief read; requirement matrix `docs/REQUIREMENTS.md` — all rows verified except the two GATED public-URL rows.
- Primary sources fetched live with exact locators: `docs/research-notes/{bdh,bdh-cq,delta-rule}.md`; consolidated ledger `docs/RESEARCH.md`. Notation discrepancies recorded (BDH ρ shape; Pathway page wording; repo conventions). One source unreachable (Pathway derivation chapter) — logged; nothing relies on it.
- App: 7-step guided lesson + sandbox + BDH/BDH-CQ module. `npm run typecheck` clean; `npm test` 31/31; `npm run build` ok; `npm run smoke` 21/21 (includes live-math-not-painted check; 27 ms slider→render on this machine).
- Fresh-checkout reproduction (clean clone + `npm ci`): typecheck, tests, build, smoke, `npm run pdfs` (concept summary re-renders at exactly 1 page), `BASE_PATH=/dataforge/ npm run build` (asset paths correct for Pages).
- Submission: `concept-summary.pdf` (1 A4 page, 802 words), `blog.pdf` (9 pages, real screenshots), editable sources, `SUBMISSION_CHECKLIST.md`, `manifest.json` (checksums; regenerate with `node scripts/make-manifest.mjs`).
- Screenshots inspected (desktop/mobile/panels); one clipping defect found and fixed.

## Decisions (stable — do not relitigate on resume)

- Stack: React 18.3.1 + TS 5.6.3 + Vite 5.4.11, KaTeX 0.16.11, Vitest 2.1.8, playwright-core 1.49.1 with container Chromium (`/opt/pw-browsers/chromium`, override via CHROMIUM_PATH). Lockfile committed.
- Column vectors; unnormalized additive associative memory; guided lesson pins λ=1; decay/repeats live in sandbox; ρ=1 reported as tie; scores never called probabilities; engine never sees ground truth.
- Two clearly named PDFs supplied (ambiguity documented in REQUIREMENTS.md).
- License MIT; organizer brief and paper texts NOT committed (private inputs).

## Blockers / external gates (remaining work — user actions)

- G1: DONE except final spot-check — Pages deployed (run #6, success); open https://jainraunak944.github.io/Dataforge/ in incognito once before submitting.
- G2: DONE — repository is Public (confirmed via API 2026-09-08).
- G3: submit to the DataForge portal (team action).
- G4 (optional): run the proposed 60-second learner protocol with ≥5 people, log results in docs/LEARNER_TEST.md.

## Test results (latest)

typecheck 0 errors · unit 31/31 · smoke 21/21 · concept-summary.pdf Pages: 1 · fresh checkout: all of the above reproduced.

## Next command

None. README URLs, SUBMISSION_CHECKLIST G1/G2, and REQUIREMENTS S1/S2 updated with the deployed URL; manifest regenerated. Remaining: team incognito spot-check of the URL, then portal upload (G3), optional learner study (G4).
