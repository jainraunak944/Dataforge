# Demo script — 3-minute live walkthrough

**Setup:** open the artifact (default loads populated at ρ = 0.6; nothing to click to start).

## 1 · First insight (≈40 s)

"This 2×2 matrix is an entire memory system. Two associations were just written into it — watch." Press **Play** in step 1: the two outer-product stamps land in the same four numbers. "No slots. Both memories share every cell. The question is what that sharing costs."

Scroll to step 2. "Truth on the left, what the memory actually returns beside it. At overlap 0.6, cue A asks for [1, 0] and gets [1, 0.6] — the other memory leaks in by exactly the overlap. L2 error: 0.6. Not roughly — exactly."

## 2 · Change the input (≈30 s)

Drag ρ to **0**: "Orthogonal cues — both errors collapse to zero. Exact recall, four numbers total." Drag toward **1** slowly: "Interference grows linearly; the readout is always value-plus-ρ-times-the-other-value. The claim on top of the page predicts every number you're seeing; the third column recomputes everything from a separate retained-pairs implementation as a check."

## 3 · Failure case (≈30 s)

Set ρ = **1** (or click the *Identical cues* preset in step 6): "Both cues are now the same vector. Both reads return [1,1]. The cue carries zero distinguishing information — and the app reports a **tie**, because declaring a winner here would be fabrication. This is the toy's honest failure mode, and it's the same pressure — key collisions — that the 2024 delta-rule papers cite as their motivation."

## 4 · BDH connection (≈45 s)

Scroll to step 5. "Same vocabulary, real architecture. BDH-GPU's state update — equation 8 of the Dragon Hatchling paper — is our write with machinery around it: the value is a learned projection LN(Ey), the key and query are the *same* sparse activation x, our λ becomes the operator U. The variable table says, for every symbol, whether it changes during inference — the state ρ does; the trained matrices E, D don't. And BDH-CQ lifts the same split one level: memory accumulates per demonstration — its report names additive accumulation as its linear-attention special case — while parameters stay frozen at inference."

Point at the labels: "Equations are transcribed from the papers with equation numbers — this page never runs BDH, and says so."

## 5 · Evidence (≈20 s)

Scroll to the comparison. "Every number here is author-reported, from the cited table of the cited paper — Schlag's additive model breaking past perplexity 260 while the delta variant sits at 29; BDH-CQ's 29.5% on ARC-AGI-1 at a fraction of a cent of GPU time per task, audited by co-authors — labeled semi-independent, because that's what it is. Full claim-to-source ledger with equation-level locators is in the repo."

**Closer:** "One matrix, one slider, one falsifiable sentence — and the learner leaves able to point at the exact term where interference is born."

## Fallbacks

- If the browser fails: `npm run dev` locally, or open the screenshots in `artifacts/screenshots/` while restarting.
- If asked to prove numbers aren't painted: open devtools console — or run `npm test` and `npm run smoke` live (31 unit tests + 21 browser checks, includes slider-vs-closed-form).
- If asked for the hand calculation: whiteboard §2 of `docs/DEFENSE_GUIDE.md`.
