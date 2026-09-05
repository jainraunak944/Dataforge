# Defense guide — own every component

Purpose: any team member should be able to trace the system live, predict the result of changes, and distinguish real behavior from precomputation. Read this beside the code.

## 1. Plain-English code walkthrough

**`src/memory/additiveMemory.ts` (the engine).** One matrix `M`, stored row-major, `d_v` rows × `d_k` columns. `writeAssociation(M, k, v, λ)` returns `λ·M + v·kᵀ` — for each cell (i,j): `λ·M[i][j] + v[i]·k[j]`. `readMemory(M, q)` returns `M·q` — row i is `Σ_j M[i][j]·q[j]`. Everything validates: finite numbers, |component| ≤ 4, dims ≤ 8, λ ∈ [0,1]; violations throw, never silently clamp. The engine never receives labels or ground truth — only vectors.

**`src/memory/reference.ts` (the independent check).** Keeps every (k, v) pair in a list and computes `Σ_i λ^(t−i)·v_i·(k_i·q)` with plain index loops. Deliberately shares no helpers with the engine, so when both agree (tolerance 1e−9, stated) it's evidence, not circularity. λ=0 convention: newest write keeps weight λ⁰=1 (JS: `Math.pow(0,0)===1`).

**`src/memory/fixtures.ts` (the evaluator's data).** `guidedFixture(ρ)` builds `k_A=[1,0]`, `k_B=[ρ,√(1−ρ²)]` (both unit length ⇒ `k_A·k_B = ρ` exactly), `v_A=[1,0]`, `v_B=[0,1]`, plus the five presets. Ground truth lives here — with the evaluator, never the engine.

**`src/memory/evaluate.ts`.** L2 error between desired and retrieved; cue-match scores `dot(k_i, q)` (displayed as *scores*, never probabilities); `argmaxOrTie` reports ties within 1e−12 as ties — at ρ=1 the answer is "tie [A,B]", deterministically, never an arbitrary winner.

**`src/memory/session.ts`.** Pure function (ρ, λ, repeats) → everything the UI shows: write sequence (A,B interleaved), matrix timeline (M₀=0 onward), both queries with engine + reference results, accounting. Determinism is unit-tested (same params ⇒ deep-equal state). The UI renders this object directly — there is no other source of displayed numbers.

**Components** map 1:1 to lesson steps (see `docs/ARCHITECTURE.md` table). The only "animation" is stepping through the computed matrix timeline; reduced-motion makes Play instant.

## 2. Worked example by hand (do this on a whiteboard)

ρ = 0.6, λ = 1, write A then B:

1. `M₁ = 0 + v_A k_Aᵀ = [[1,0],[0,0]]` (v_A=[1,0] down the rows, times k_A=[1,0] across).
2. `v_B k_Bᵀ = [0,1]ᵀ·[0.6,0.8] = [[0,0],[0.6,0.8]]`.
3. `M₂ = [[1,0],[0.6,0.8]]`.
4. Read A: `M₂·[1,0]ᵀ = [1, 0.6]` — desired `[1,0]`, L2 error `0.6` = ρ. The leak is `v_B·(k_B·k_A) = 0.6·v_B`.
5. Read B: `M₂·[0.6,0.8]ᵀ = [0.6, 0.36+0.64] = [0.6, 1]` — desired `[0,1]`, error 0.6.
6. Reference check: `v_A(k_A·q) + v_B(k_B·q)` with q=k_A → `[1,0]·1 + [0,1]·0.6 = [1,0.6]` ✓.

## 3. Predict-the-change drills (judges love these)

- *Set λ=0.5, ρ=0.6, read A?* `M = 0.5·v_Ak_Aᵀ + v_Bk_Bᵀ`, so `[0.5, 0.6]`.
- *Write everything twice, λ=1?* All readouts double; matrix still 2×2.
- *Swap v_A to [0,1] too?* Both reads at ρ=0 return [0,1]; values may collide freely — only key overlap causes cross-talk.
- *Query with 2·k_A?* Retrieved doubles: reading is linear in the cue. Error becomes |[2,1.2]−[1,0]| — the fixture's "desired" assumes unit cues; the sandbox doesn't allow this, which is why bounds are stated.
- *Add a third orthogonal key in 2-D?* Impossible — only 2 orthogonal directions exist in R². That IS the capacity story: more associations than dimensions forces overlap (Schlag §4.1).

## 4. Real vs precomputed vs animated — the honest map

- **Live:** every number in every panel (matrix, readouts, errors, scores, accounting, quiz reveal). Verified by the smoke test driving the slider and checking values match the closed form.
- **Source-derived illustration:** BDH/BDH-CQ equations (transcribed from the papers with equation numbers), variable-role table.
- **Author-reported:** every benchmark number in the comparison and BDH-CQ sections (labeled inline).
- **Animation:** only the write-stepping, which replays computed matrix states. No scripted/painted values anywhere; `scripts/smoke.mjs` fails if displayed numbers diverge from the math.

## 5. Design trade-offs (be ready to defend)

2×2 for total visibility; two independent code paths for non-circular verification; λ excluded from the guided lesson to keep the claim's conditions clean; deterministic quiz over LLM grading; no external services so the artifact runs offline; pinned lockfile for reproducibility; separate evaluator so truth-beside-estimate can't leak into the engine.

## 6. Likely judge questions, with answers

1. **"Why is the claim falsifiable?"** It predicts exact numbers ([1,ρ], error ρ, exactness at ρ=0, [1,1] tie at ρ=1) under stated conditions. Any deviation the learner can produce in the sandbox refutes it. The independent reference path removes the "your code checks itself" objection.
2. **"Isn't this just linear attention?"** It's the memory update that linear attention maintains (unnormalized, per Schlag Eq. 17 / DeltaNet §2.1). We say "unnormalized additive associative memory": no φ feature map, no normalization, no learned projections — those omissions are listed in-app.
3. **"Where exactly is this in BDH?"** BDH-GPU Eq. (8), arXiv:2509.26507 §3.2: state `ρ` accumulates `LN(E y)·xᵀ` per token (our `v·kᵀ`), read as `ρ·x` (our `M·q`), decayed by `U` (our λ). Keys=queries=the sparse activation x — one real difference from the toy, stated in the variable table.
4. **"Is BDH an SSM like Mamba?"** No — and the brief itself warns against this. The paper positions BDH-GPU as linear attention in one very high-dimensional, non-negative, sparsely active neuronal space; graph BDH is a neuron-synapse local-rule system. We show both forms (Eq. 8 vs Eq. 6).
5. **"What does BDH-CQ add?"** Per its report (§3.1–3.3): contextual memory built per demonstration `S_t = U_θ(S_{t−1}, D_t)` with additive accumulation as its linear-attention special case, plus recurrent latent reasoning `H_{r+1} = F_θ(H_r, S_K)` — with no parameter updates at inference (§1, quoted in-app). We also surface its own caveats: internals proprietary, ConceptARC in the training mixture.
6. **"Are the ARC numbers independent?"** No — author-reported (Table 1: 118/400 = 29.50% pass@2), audited black-box by co-authors, which we label semi-independent. We never call any of this independently validated.
7. **"Why does the error equal ρ exactly?"** `M k_A = v_A(k_A·k_A) + v_B(k_B·k_A) = v_A + ρ v_B`; since `v_B` is a unit vector orthogonal to `v_A`, the L2 distance from `v_A` is exactly ρ. If values weren't orthonormal the error would be `ρ·‖v_B‖` in the `v_B` direction.
8. **"What happens with 100 writes — does the matrix overflow?"** With λ=1 magnitudes grow linearly with writes (unnormalized!); shape stays 2×2. The app caps at 64 pairs and states the cap; the accumulator growth is exactly why real systems add normalization, decay or delta corrections (Schlag §6.3 had to remove normalization carefully; Gated DeltaNet folds decay into the transition).
9. **"Does constant state mean constant memory use?"** Model state, yes: d_k·d_v scalars. The teaching page keeps extra bounded history for stepping, and total browser memory is not constant — stated in-app. Slot counts are analytical under float64, not measured GPU RAM.
10. **"Why not show softmax attention beside it?"** Scope: one claim. The recurrent≡explicit-history identity we demonstrate is specific to the linear form; softmax breaks it (no fixed-size sufficient state). We say this rather than gesturing at equivalence.
11. **"How do delta rules 'fix' interference?"** DeltaNet's write subtracts the currently-retrieved value before inserting: `S_t = S_{t−1} − β(S_{t−1}k − v)kᵀ` — one SGD step on recall error, overwriting rather than superimposing under a reused key. Cost: sequential structure (their contribution is parallelizing it) and, without decay, poor length generalization — hence gated variants.
12. **"Could the engine be reading the answer?"** No path exists: the engine module imports nothing from fixtures/evaluator; it receives vectors. Tests + the smoke test's slider-vs-closed-form check would catch painted output.
13. **"What breaks if I query before any write?"** `M₀ = 0` ⇒ retrieved `[0,0]`, reference (empty history) `[0,0]` — tested ("zero state and zero writes").
14. **"Why λ⁰=1 at λ=0 and not 'everything zero'?"** The recurrence `M_t = 0·M_{t−1} + v_t k_tᵀ` keeps the newest write by construction; the reference must match, so its weight is λ^(t−i) with exponent 0 for the newest. Conventions must match or the two paths disagree at λ=0 — that's exactly what the decay-endpoint test pins.
15. **"What's the single most important limitation of your artifact?"** It teaches the mechanism, not the trained behavior: nothing here shows how learned encoders shape keys/values, so it cannot demonstrate BDH's reported sparsity, monosemanticity, or performance — all labeled author-reported. Second: the learner protocol is proposed, not yet run on people (LEARNER_TEST.md is explicit).
16. **"Who computed the maturity scores?"** We did — labeled "our assessment" with a defined scale, in the comparison section; not an official rating.
