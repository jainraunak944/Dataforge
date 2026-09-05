# Architecture

## Data flow

```
                    concept variables (ρ, λ, repeats)
                                 │  (slider / presets / URL hash)
                                 ▼
                    src/memory/session.ts  deriveSession()   ← pure, deterministic
                                 │
        ┌────────────────────────┼──────────────────────────┐
        ▼                        ▼                          ▼
  fixtures.ts             additiveMemory.ts           reference.ts
  guidedFixture(ρ)        M_t = λM_{t-1} + v k^T      Σ λ^(t-i) v_i (k_i·q)
  + ground truth          retrieved = M q             (independent path,
  (evaluator side)        (memory engine)              retained-pairs list)
        │                        │                          │
        └────────────┬───────────┴──────────────────────────┘
                     ▼
              evaluate.ts  — L2 error, cue-match scores, tie reporting
                     │
                     ▼
              SessionState (matrix timeline, queries, accounting)
                     │
                     ▼
              React components render THIS state — no painted values
```

## Equations and dimensions

Column vectors throughout:

- `k_t, q ∈ R^{d_k}` (d_k = 2 in the lesson), `v_t ∈ R^{d_v}` (d_v = 2), `M_t ∈ R^{d_v × d_k}`.
- `M_0 = 0`; write `M_t = λ·M_{t−1} + v_t k_tᵀ` (λ = 1 in the guided lesson); read `retrieved(q) = M_t q`.
- Independent reference: `reference(q) = Σ_{i=1..t} λ^(t−i) · v_i · (k_i·q)`. Convention at λ = 0: the newest write keeps weight λ⁰ = 1 (`Math.pow(0,0) === 1`).
- Fixture: `k_A = [1,0]ᵀ`, `k_B = [ρ, √(1−ρ²)]ᵀ`, `v_A = [1,0]ᵀ`, `v_B = [0,1]ᵀ`, ρ ∈ [0,1]. Closed forms at λ=1, one write each: `M k_A = [1, ρ]ᵀ`, `M k_B = [ρ, 1]ᵀ`.
- Recurrent-vs-reference agreement is asserted within stated tolerance 1e−9 (float64; the 2×2 lesson agrees to ~1e−15). This equivalence is a property of the chosen linear operation — not a claim about softmax attention.

## State ownership (the honesty boundary)

| Holder | Knows | Never knows |
|---|---|---|
| Memory engine (`additiveMemory.ts`) | vectors it is given | item identities, ground truth, the fixture's meaning |
| Reference path (`reference.ts`) | the retained (k, v) list | ground truth |
| Evaluator (`fixtures.ts` + `evaluate.ts` + UI) | ground truth (desired values), labels A/B | — (it displays error precisely because it holds truth) |

The engine cannot cheat: it receives only vectors and returns only vectors. The evaluator computes errors and tie reports. This boundary is what makes "truth beside estimate" honest.

## Storage accounting

- Core recurrent state: `d_k·d_v` scalars (4 in the lesson), independent of write count. float64 → 32 bytes.
- Retained pairs (reference path): `N·(d_k+d_v)` scalars, linear in N. Capped at `HISTORY_CAP = 64` pairs — the cap is stated in the UI and exists so the teaching interface itself stays bounded; the explicit-history reference is only ever computed over this visible bounded fixture or documented test runs.
- The teaching UI additionally holds the bounded matrix timeline (for stepping), fixture data and ground truth. Constant-size *model state* ≠ constant total browser memory, fixed total compute, unbounded lossless storage, or zero interference. These counts are analytical for the toy under the stated dtype — not measured GPU RAM, not a Transformer benchmark.

## Determinism

No RNG anywhere in the app. All state is a pure function of (ρ, λ, repeats); presets are parameter tuples; the URL hash serializes the same three numbers. Test seeds (LCG) exist only in the test suite and are stated literals.

## Component roles

| Path | Role | Nature |
|---|---|---|
| `src/memory/additiveMemory.ts` | memory engine: write/read/outer product, bounds, validation | live computation |
| `src/memory/reference.ts` | independent explicit-history reference + tolerance | live computation |
| `src/memory/fixtures.ts` | guided fixture, presets, ground truth (evaluator side) | fixed data |
| `src/memory/evaluate.ts` | L2 error, cue-match scores (labeled scores, never probabilities), deterministic tie reporting | live computation |
| `src/memory/session.ts` | pure derivation of everything rendered | live computation |
| `src/memory/accounting.ts` | slot/byte counts for both storage strategies | analytical |
| `src/components/StoreTwoThings.tsx` | step 1: pairs, outer products, matrix timeline with Play/Pause/Step (animates only computed transitions; honors reduced motion) | live |
| `src/components/CollideCues.tsx` | step 2: ρ slider, truth-beside-estimate, reference column, ρ=1 ambiguity notice | live |
| `src/components/CrossTerm.tsx` | step 3: clickable per-cell decomposition into A/B contributions | live |
| `src/components/WhatChanged.tsx` | step 4: state taxonomy (no invented training step) | live + fixed prose |
| `src/components/BdhModule.tsx` | step 5: BDH-GPU Eq. (8) walkthrough, variable-role table, omissions, learner question; BDH-CQ section | source-derived illustration + author-reported numbers, labeled |
| `src/components/BreakTheClaim.tsx` | step 6: presets, λ, repeats, accounting table | live |
| `src/components/Comparison.tsx` | contemporary relevance table | author-reported numbers, labeled |
| `src/components/ExplainItBack.tsx` | step 7: predict→reveal (held-out ρ=0.8 computed live), state question, limitation question; deterministic grading | live + fixed feedback text |
| `src/components/References.tsx` | primary sources | fixed |
| `scripts/smoke.mjs` | browser verification incl. "no painted values" check | test |

## Design trade-offs

- **2×2 on purpose**: every scalar visible beats realism; capacity/interference already fully expressible.
- **Two code paths for one algebra**: costs duplication, buys non-circular verification.
- **Pure derivation over incremental state**: recomputing the whole session per interaction is O(repeats·d²) ≈ microseconds, and makes UI = f(params) trivially testable and shareable via URL.
- **Guided λ=1**: decay is a second concept; it lives in the sandbox so the central claim stays falsifiable under fixed conditions.
- **No LLM grading**: the quiz targets exact predictable outcomes; deterministic feedback is both honest and offline.
- **KaTeX + system fonts, no CDN**: everything bundles locally; the artifact needs no network, GPU, account or server.
