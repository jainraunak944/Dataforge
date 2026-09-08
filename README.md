# Memory Under Pressure — How a Matrix Remembers and Interferes

An interactive explainer for the **DataForge 2026 Pathway track**. Topic: **Associative Memory and Fast Weights**, connected to **BDH (the Dragon Hatchling)** and **BDH-CQ**.

## The central claim

> For the additive memory in this explainer, storing two associations with orthogonal unit keys permits exact recall; increasing their key overlap introduces calculable interference while the recurrent matrix keeps the same shape and no trained parameters change.

Conditions, refutation paths and non-claims: [`docs/CLAIM.md`](docs/CLAIM.md). The artifact lets a learner reproduce, test and try to break this sentence in under a minute.

## Audience and prerequisites

Undergraduate ML learners and working data scientists who know **vectors, dot products, matrix multiplication and basic neural networks**. Visual refreshers (outer product, linear read) appear in the lesson where needed. No GPU, training, paid API, account or server is required to use the artifact.

## Learning objectives

After the lesson a learner can:

1. Trace an outer-product write and a matrix–vector read.
2. Predict the retrieved value as two keys become more similar (leak = ρ · other value).
3. Distinguish temporary recurrent state from trained parameters.
4. Explain how fixed state size differs from unlimited recall capacity.
5. Identify the corresponding write/read in BDH-GPU (Eq. 8, arXiv:2509.26507), list the machinery the toy omits, and state BDH-CQ's distinct role (per-demonstration state accumulation + recurrent latent reasoning, arXiv:2608.09888).

## Run it

Requires Node ≥ 20.

```bash
npm ci          # install pinned dependencies (package-lock.json committed)
npm run dev     # local dev server (URL printed; opens the full lesson)
```

Production build and checks:

```bash
npm run typecheck   # tsc --noEmit
npm test            # 31 Vitest math/unit tests (hand-calculated fixtures + independent reference)
npm run build       # static production build → dist/
npm run smoke       # 21 browser checks incl. "no painted values" (needs Chromium; CHROMIUM_PATH env overrides)
npm run pdfs        # regenerate submission PDFs from submission/src/
```

**URLs:** public source repository: <https://github.com/jainraunak944/Dataforge> (public; branch `claude/memory-under-pressure-p6vp89`). Public no-sign-in artifact: <https://jainraunak944.github.io/Dataforge/> — deployed 2026-09-08 by the GitHub Pages workflow (`.github/workflows/deploy.yml`, run #6); GitHub's Pages deployment status reported success for commit `a67aa13`. See `submission/SUBMISSION_CHECKLIST.md` for the verification record.

## Architecture (short version — full: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md))

Concept variables (ρ, λ, repeats) → pure `deriveSession()` → React renders that state. The memory engine (`src/memory/additiveMemory.ts`, `M_t = λM_{t−1} + v_t k_tᵀ`, read `M q`, column vectors) never sees item identities or ground truth; the evaluator (`fixtures.ts` + `evaluate.ts`) holds truth and computes errors. A deliberately separate explicit-history reference (`reference.ts`, `Σ λ^(t−i) v_i (k_i·q)`) provides the non-circular correctness check (stated tolerance 1e−9).

| Component | Role |
|---|---|
| `src/memory/` | engine, independent reference, evaluator, fixtures, accounting, pure session derivation |
| `src/components/StoreTwoThings` | step 1 — writes as outer products, matrix timeline, Play/Pause/Step |
| `src/components/CollideCues` | step 2 — ρ slider, truth beside estimate, reference column, ρ=1 ambiguity |
| `src/components/CrossTerm` | step 3 — clickable cell decomposition; point at the interference |
| `src/components/WhatChanged` | step 4 — state vs activation vs convention vs (absent) trained weights |
| `src/components/BdhModule` | step 5 — BDH-GPU Eq. (8) walkthrough, variable-role table, omissions, learner question; BDH-CQ |
| `src/components/BreakTheClaim` | step 6 — presets, decay λ, repeated writes, honest memory accounting |
| `src/components/Comparison` | why-now table (delta-rule papers, BDH, BDH-CQ) |
| `src/components/ExplainItBack` | step 7 — predict → live reveal on held-out ρ, deterministic feedback |
| `tests/`, `scripts/smoke.mjs` | math tests against hand-calculated literals; browser checks |

## What is live, precomputed, synthetic, animated

- **Live:** every displayed number (matrix cells, readouts, errors, scores, accounting, quiz reveal) is computed in the browser from the toy at interaction time. The smoke test drives the slider and fails if displayed values diverge from the closed form.
- **Precomputed:** nothing. There are no shipped result files.
- **Synthetic:** the fixture vectors themselves (chosen, not learned) — stated in the lesson.
- **Animated:** only the write-stepping, which replays real computed matrix states; honors `prefers-reduced-motion`.
- **Source-derived (not ours):** BDH/BDH-CQ equations, transcribed with equation numbers. **Author-reported (not ours, labeled):** every benchmark number quoted. The toy is an original computation and **is not an official BDH model**.

## Limitations (the honest list)

- The toy teaches the mechanism, not trained behavior: nothing here demonstrates BDH's reported sparsity, monosemantic synapses, or performance — those are author-reported results of trained models, labeled as such.
- The recurrent≡explicit-history equivalence shown holds for this linear operation, not softmax attention.
- Memory accounting is analytical (float64 slot counts), not measured GPU RAM; the teaching UI keeps extra bounded state beyond the 4-number model state.
- ρ=1 leaves cue-based recall undecidable; the app reports the tie rather than resolving it.
- Sandbox caps (history ≤ 64 pairs, |components| ≤ 4, λ ∈ [0,1]) are stated in-app.
- The 60-second learner protocol is **proposed**; no user study has been run yet ([`docs/LEARNER_TEST.md`](docs/LEARNER_TEST.md)).
- The interaction-latency measurement (27 ms slider→render in our environment) is machine-specific, not a device-independent guarantee.

## Reproduce the results

1. `git clone https://github.com/jainraunak944/dataforge && cd dataforge && git checkout claude/memory-under-pressure-p6vp89`
2. `npm ci && npm run typecheck && npm test` — 31 tests must pass; expected values are hand-calculated in the test files.
3. `npm run build && npm run smoke` — 21 browser checks; artifacts land in `artifacts/` (screenshots + JSON log).
4. Verify any scientific claim via [`docs/RESEARCH.md`](docs/RESEARCH.md): each has an exact section/equation locator into its primary source.
5. `npm run pdfs` regenerates both submission PDFs from their committed HTML sources.

## Documentation map

[`docs/CLAIM.md`](docs/CLAIM.md) · [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) (brief→implementation matrix) · [`docs/RESEARCH.md`](docs/RESEARCH.md) (claim-to-source ledger) · [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · [`docs/LEARNER_TEST.md`](docs/LEARNER_TEST.md) · [`docs/DEFENSE_GUIDE.md`](docs/DEFENSE_GUIDE.md) · [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) · [`docs/PROVENANCE.md`](docs/PROVENANCE.md) · [`submission/`](submission/) (concept summary PDF, blog PDF, checklist, manifest)

## AI assistance disclosure (mirrored from [`docs/AI_DISCLOSURE.md`](docs/AI_DISCLOSURE.md))

This project was built with **Claude Code** (Anthropic) as an implementation assistant directed by the team's written brief: it produced the application/test code, documentation and submission prose under that brief, and ran the live research-verification workflow that grounds every scientific claim in `docs/research-notes/` + `docs/RESEARCH.md`. No external application code was reused or forked; the official BDH repo was read for convention-checking only. No mentors or additional contributors are declared. The team owns and must be able to defend every component — that is what [`docs/DEFENSE_GUIDE.md`](docs/DEFENSE_GUIDE.md) is for.

## Credits and licenses

Original code and prose: MIT ([`LICENSE`](LICENSE)). Dependencies: React, KaTeX (fonts under SIL OFL 1.1), Vite, Vitest, Playwright — full origin/version/license table in [`docs/PROVENANCE.md`](docs/PROVENANCE.md). BDH, BDH-CQ and all cited results belong to their authors (see References in-app and the ledger). This project is independent and not affiliated with Pathway or DataForge organizers.
