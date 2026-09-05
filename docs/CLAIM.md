# Central claim

> **For the additive memory in this explainer, storing two associations with orthogonal unit keys permits exact recall; increasing their key overlap introduces calculable interference while the recurrent matrix keeps the same shape and no trained parameters change.**

This sentence is the single thing the explainer teaches. Every control, chart and paragraph in the artifact serves it.

## Explicit conditions

The claim holds under these exact conditions, all of which the artifact makes visible:

1. **Zero initial state**: `M_0 = 0` (the 2×2 matrix starts empty).
2. **One write per association**: association A is written once, then association B is written once.
3. **No decay for this experiment**: `λ = 1` in the guided lesson. Decay is a sandbox extension, clearly separated.
4. **The specified unit keys and values** (column vectors):
   - `k_A = [1, 0]ᵀ`, `k_B = [ρ, √(1−ρ²)]ᵀ` with `ρ ∈ [0, 1]` (both unit length)
   - `v_A = [1, 0]ᵀ`, `v_B = [0, 1]ᵀ`
5. **Querying after both writes**, with the stored keys as cues.

## What makes it falsifiable

With `λ = 1` and the fixture above, the memory `M = v_A k_Aᵀ + v_B k_Bᵀ` must return:

- `M k_A = [1, ρ]ᵀ` — exact recall `[1, 0]ᵀ` iff `ρ = 0`; interference term `ρ · v_B` otherwise.
- `M k_B = [ρ, 1]ᵀ` — exact recall `[0, 1]ᵀ` iff `ρ = 0`.
- At `ρ = 1` both cues are identical and both reads return `[1, 1]ᵀ`: the cue carries no information that can distinguish A from B. The artifact reports this ambiguity explicitly instead of picking an argmax winner.

A learner can refute the claim inside the artifact: if any recall at `ρ = 0` were inexact, if the interference did not match the predicted closed form `ρ`, if the matrix changed shape with more writes, or if any trained parameter changed, the claim would be false. The independent explicit-history reference (`Σᵢ vᵢ (kᵢ·q)`) is computed by a separate code path so the check is not circular.

## What the claim is NOT

- It is **not** a claim that this toy reproduces BDH or BDH-CQ performance.
- It is **not** a claim that all fixed-size memories behave identically (delta-rule and gated variants behave differently by design; see the comparison section).
- It is **not** a claim about softmax attention: the recurrent/explicit-history equivalence shown holds for this linear operation only.
- It is **not** a claim about production-scale memory usage; the slot counts shown are analytical accounting for the toy under a stated dtype, not measured GPU RAM.

## Scope note

Approved central topic: **Associative Memory and Fast Weights** (DataForge 2026 Pathway track). Linear attention appears only as the mathematical connection between the toy and BDH-GPU/BDH-CQ formulations, not as a second survey.
