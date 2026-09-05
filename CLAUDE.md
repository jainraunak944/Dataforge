# Memory Under Pressure — working notes for Claude

Project: DataForge 2026 Pathway track submission. Topic: **Associative Memory and Fast Weights**.

## Core claim (do not weaken or broaden)

Storing two associations with orthogonal unit keys in the additive memory permits exact recall; increasing key overlap introduces calculable interference while the recurrent matrix keeps the same shape and no trained parameters change. Full statement + conditions: `docs/CLAIM.md`.

## Scientific guardrails

- Column vectors everywhere in the toy: `M_t = λ·M_{t-1} + v_t k_tᵀ`, `retrieved(q) = M_t q`. Call it **unnormalized additive associative memory**. It is not softmax attention and not BDH.
- Correctness tests use hand-computed values or the separate explicit-history reference (`src/memory/reference.ts`), never the implementation under test.
- Raw readouts are **scores**, never probabilities. ρ=1 is reported as ambiguity, never an argmax winner.
- The memory engine never sees item IDs or ground truth; only the evaluator does (documented boundary).
- BDH ≠ Mamba-style SSM. Graph BDH ≠ BDH-GPU. Toy ≠ official model. BDH-CQ inference changes state, not parameters.
- Never invent numbers, citations, test results, URLs or user actions. Evidence categories: formal / author-reported / independently evaluated / original toy result.
- Memory accounting: core state `d_k·d_v` scalars vs explicit history `N·(d_k+d_v)`, stated dtype; teaching UI holds extra bounded history — say so.

## Commands

- `npm install` (Node 20+), `npm run dev` — local dev server
- `npm test` — Vitest math/unit tests
- `npm run typecheck` — tsc --noEmit
- `npm run build` — production build to `dist/`
- `npm run smoke` — Playwright browser smoke test (uses /opt/pw-browsers/chromium in this container)
- `npm run pdfs` — regenerate submission PDFs from `submission/src/`

## Key docs

`docs/CLAIM.md` · `docs/REQUIREMENTS.md` (requirement matrix) · `docs/RESEARCH.md` (claim-to-source ledger) · `docs/ARCHITECTURE.md` · `docs/DEFENSE_GUIDE.md` · `TASKS.md` + `BUILD_STATUS.md` (session continuity — read these first on continuation and proceed; do not restart the project).

## Branch

All work on `claude/memory-under-pressure-p6vp89`; push with `git push -u origin claude/memory-under-pressure-p6vp89`.
