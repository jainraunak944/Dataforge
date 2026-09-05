# Research ledger — claims, sources, evidence categories

All primary sources were fetched and read live on 2026-09-05 during the build. Full verbatim quotes, per-source fetch logs (including which mirrors failed from the build environment) and additional context are in `docs/research-notes/{bdh,bdh-cq,delta-rule}.md`. This file is the ledger mapping every substantive scientific claim made in the artifact and submission documents to its source.

**Evidence categories used everywhere:**
- **FORMAL** — a mathematical statement provable from definitions (or proven in the source).
- **AUTHOR-REPORTED** — an empirical result reported by the system's own developers.
- **SEMI-INDEPENDENT** — checked by parties with a stake (e.g. co-authors auditing black-box).
- **INDEPENDENT** — externally reproduced by unaffiliated parties. *(None of the frontier results we cite has this status, and we say so.)*
- **TOY** — our own 2×2 original computation, reproducible from this repo.

## Primary papers (verified metadata)

| Ref | Citation | Version read | Role |
|---|---|---|---|
| [1] | S. Yang, B. Wang, Y. Zhang, Y. Shen, Y. Kim, *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, NeurIPS 2024, arXiv:2406.06484 | v6, 15 Jan 2025 | recent primary (2024) |
| [2] | S. Yang, J. Kautz, A. Hatamizadeh, *Gated Delta Networks: Improving Mamba2 with Delta Rule*, ICLR 2025, arXiv:2412.06464 | v3, 6 Mar 2025 | recent primary (2024) |
| [3] | I. Schlag, K. Irie, J. Schmidhuber, *Linear Transformers Are Secretly Fast Weight Programmers*, ICML 2021, arXiv:2102.11174 | v3, 9 Jun 2021 | background only — outside the 2022–2026 window, per the build rules |
| [4] | A. Kosowski, P. Uznański, J. Chorowski, Z. Stamirowska, M. Bartoszkiewicz, *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain*, arXiv:2509.26507 | v1 (HTML), 30 Sep 2025 | recent primary (2025) |
| [5] | B. Engdahl, A. Kosowski, J. Chorowski, Z. Stamirowska, P. Uznański, J. Jiang, R. Phadke, R. Kinas, R. Zhong, *BDH-CQ: In-Context Learning with Recurrent Latent Reasoning*, arXiv:2608.09888 | v1, 10 Aug 2026 | recent primary (2026) |

The ≥3-recent-papers requirement (brief p.10) is met by [1], [2], [4], [5].

**Access note:** direct fetches of arxiv.org, pathway.com and aws.amazon.com were blocked by this build environment's egress proxy. Full texts of [1]–[5] were retrieved through the Firecrawl research index, whose passages embed the arXiv version banners quoted above; that provenance caveat is recorded in each notes file. One resource could not be retrieved at all: Pathway's "From attention to synapses" derivation chapter (body unreachable on every route tried). **Nothing in this submission relies on it**; it is listed as further reading only. This follows the rule: log inaccessible sources, never fabricate their contents.

## Claim-to-source ledger

### The toy mechanism (claims in lesson steps 1–4, 6–7)

| Claim | Source & locator | Category | Assumptions / limits |
|---|---|---|---|
| Additive fast-weight memory: `M_t = λM_{t−1} + v_t k_tᵀ`, read `M q`; equals `Σ λ^(t−i) v_i (k_i·q)` by linearity | standard linear algebra; same form as [1] §2.1 (λ=1) and [3] Eq. 17 | FORMAL | linear read/write only; not softmax attention |
| Guided fixture recalls `[1, ρ]` / `[ρ, 1]`; L2 error = ρ; exact at ρ=0; both reads `[1,1]` at ρ=1 | hand derivation in `docs/CLAIM.md`; verified by `tests/memory.test.ts` against literals and independent reference | FORMAL + TOY | claim conditions in CLAIM.md |
| Storing more associations than the key dimension supports "will result in a retrieval error" | [3] §4.1 (Smolensky tensor-product capacity argument) | FORMAL (in source) | applies to the linear-attention memory family |
| Purely additive fast weights break down at scale: WikiText-103 unlimited-context ppl >260 vs 29.4 test ppl for the delta-rule variant, both ≈90M params | [3] Table 4, §6.3, App. D.3 | AUTHOR-REPORTED | their setting: fast-weight memory carried across segments; normalization removed for delta variant |

### Delta-rule comparison (Comparison section)

| Claim | Source & locator | Category | Assumptions / limits |
|---|---|---|---|
| Additive rule "makes it difficult to deallocate past key-value associations, eventually leading to key 'collisions' when L > d" | [1] §2.2 (motivating DeltaNet) | FORMAL argument, quoted | |
| DeltaNet update `S_t = S_{t−1} − β_t(S_{t−1}k_t − v_t)k_tᵀ` = one SGD step on recall loss | [1] §2.2 | FORMAL | |
| DeltaNet 1.3B/100B SlimPajama: avg zero-shot 51.6 vs Mamba 50.0, GLA 51.0 (Wikitext ppl 16.87) | [1] Table 1 | AUTHOR-REPORTED | their training setup; not a controlled comparison with other rows of our table |
| Gated update `S_t = S_{t−1}(α_t(I − β_t k_t k_tᵀ)) + β_t v_t k_tᵀ`; "gating enables rapid memory erasure while the delta rule facilitates targeted updates" | [2] §3.1 Eq. 10; abstract | FORMAL + quoted | |
| Gated DeltaNet S-NIAH-2 @4K: 92.2 vs DeltaNet 18.6, Mamba2 56.2 (1.3B); S-NIAH-1 @8K: 91.8 vs DeltaNet 98.8, Mamba2 30.4 | [2] Table 2 | AUTHOR-REPORTED | synthetic needle-in-haystack; decay-vs-retention trade-off reading is the paper's own (§3.2) |
| "their fixed state size makes it hard for retrieval tasks" (root constraint stays) | [2] §3.4 | quoted author statement | |

### BDH module (lesson step 5)

| Claim | Source & locator | Category | Assumptions / limits |
|---|---|---|---|
| BDH-GPU layer state update `ρ_{t,ℓ} := (ρ_{t−1,ℓ} + LN(E y_{t,ℓ−1}) x_{t,ℓ}ᵀ) U`; readout `y_{t,ℓ} := (D_y LN(ρ_{t−1,ℓ} x_{t,ℓ}))⁺ ⊙ x_{t,ℓ}` | [4] Eq. (8), Fig. 3, §3.2 | source equations (FORMAL within the paper) | we transcribe, not run; toy≠BDH |
| Keys and queries are the same non-negative activation x; value is LN(Ey) ∈ R^d | [4] §6.1, §3.2 | source description | |
| U is "local rotation or damping … such as ALiBi or RoPE" (decay generalizing toy λ) | [4] Definition 4 | source description, quoted | |
| Graph-BDH form `σ_{t,ℓ} := (σ_{t−1,ℓ} + (y xᵀ ⊙ G_s)) U`, distinct from BDH-GPU | [4] Eq. (6), Table 1; unrolled Eq. (5)/(16) | source equations | graph BDH ≠ BDH-GPU; BDH ≠ Mamba-style SSM (paper positions BDH-GPU as linear attention in high-dimensional neuronal space, §3, Claim 7) |
| Dimensions: x,y ∈ (R⁺)ⁿ; E ∈ R^{d×n}; D_x,D_y ∈ R^{n×d}; ≈3nd params; d=256, n up to ~10⁶ in experiments | [4] §3.2, §6.1, experimental sections | source description | |
| **Recorded discrepancy:** Fig. 3 caption says ρ ∈ R^{n×d} while Eq. (8) composes ρ as d×n; we follow the composition that type-checks and say so in-app | [4] Fig. 3 caption vs Eq. (8); noted also for the repo (row-vector convention, V = residual x, no decay beyond RoPE — `bdh.py` lines 72–74) | our observation of the sources | equations are not mixed silently, per the build rules |
| ~5% of neurons active; activity varies with predictability | [4] Empirical Finding 1, §4.1; Fig. 14 (range 4.0–7.5%) | AUTHOR-REPORTED | |
| Monosemantic synapses (e.g. currency/country synapse, U=2368, p<10⁻¹⁴) | [4] §6.3 | AUTHOR-REPORTED | trained models; our toy demonstrates nothing about this |
| Heavy-tailed / scale-free connectivity of trained σ graph | [4] Fig. 11 | AUTHOR-REPORTED | after thresholding |
| GPT-2-class language performance, 10M–1B scale, Europarl | [4] Fig. 7, Tables 4–5 | AUTHOR-REPORTED | their tokenization/data; not independently reproduced |
| Sudoku-Extreme result | **NOT in [4]**; appears in Pathway blog/README for an internal implementation the open repo "does not reproduce out of the box" | company-reported | therefore NOT used in our artifact |
| Official repo is a toy implementation, MIT license, Pathway Technology 2025 | github.com/pathwaycom/bdh (cloned; LICENSE.md; `bdh.py`, `train.py` tiny-Shakespeare demo) | direct inspection | we read it to cross-check conventions; none of its code is used here |

### BDH-CQ (lesson step 5 + comparison + summary)

| Claim | Source & locator | Category | Assumptions / limits |
|---|---|---|---|
| Contextual memory `S_t = U_θ(S_{t−1}, D_t)`, θ fixed | [5] Eq. 1, §3.2 | source equation | interface-level: "Dimensions, exact update rules, and implementation details remain proprietary" (§3.3) |
| Relation to "attention, fast-weight memory, and linear-attention views of contextual association", additive special case `S_t = S_{t−1} + U_θ(D_t)` | [5] §3.2 | source description, quoted | this is the exact bridge to our toy |
| Latent reasoning: `H_0 = E_θ(x*, S_K)`, `H_{r+1} = F_θ(H_r, S_K)`, `ŷ = G_θ(H_R)` | [5] §3.3, Eqs. 2–4 | source equations | |
| "Neither task identifiers nor evaluation-task demonstration pairs participate in training, and no parameters are updated at inference time" | [5] §1 | quoted author design claim | §6.5 concedes ConceptARC appears in the training mixture and exposure "through training or checkpoint selection" cannot be fully ruled out |
| ARC-AGI-1: pass@1 97/400 (24.25%); pass@2 118/400 (29.50%), Wilson CI [25.24, 34.15] | [5] Table 1, §6 | AUTHOR-REPORTED | 400 evaluation tasks |
| ≈0.85 H200 GPU-seconds ≈ $0.00070 per task at $3/hr | [5] §5 | AUTHOR-REPORTED | §6.6 lists a different per-task cost ($0.00265) for the standard setting; the paper does not reconcile the two — we cite the §5 figure with the "≈" it deserves |
| Effort scaling: LOW 21% (−22% cost), MEDIUM 27% (−11%), HIGH 29.5% | [5] Table 5, §7 | AUTHOR-REPORTED | |
| Paper's own comparisons: GPT 5.6 Luna (Low) 34.2% at $0.040/task; HRM $1.48, TRM $1.76 per task | [5] §5, §8 | AUTHOR-REPORTED (comparisons drawn by [5]'s authors) | unlike hardware/settings; not controlled |
| 29.5% reproduced by black-box audit | [5] §6 | SEMI-INDEPENDENT — auditors (Bielik AI, NYU) are co-authors | not an independent evaluation, and we label it so |
| BDH-CQ adds "a structured latent workspace and recurrent computation over model depth" to the BDH family | [5] §3.1 | source description | evaluated system is a full pipeline (input transforms, candidate construction, ranking) |

### Claims about deployment/partnership (used only in docs, labeled)

| Claim | Source & locator | Category |
|---|---|---|
| AWS SageMaker HyperPod integration; "Early experiments confirm Transformer-like scaling laws … 1B to 600B parameters" | Pathway press release (Aug 2026) announcing BDH-CQ; AWS executive quote therein | COMPANY-REPORTED partnership announcement — **not** an independent evaluation, not in any paper we verified; the 600B figure is an early-experiments claim by the company |

## Notation reconciliation (per build rule §3)

Our toy, [1], [2], [3] and [4]'s Eq. (8) all write the state as **value · keyᵀ acting on a column query from the right** (or the row-vector transpose of the same thing); differences are decay placement ([2] folds gating into a transition matrix; [4] applies U on the right) and [3]'s feature map φ. The one true discrepancy found — [4]'s ρ shape in its Fig. 3 caption vs its own equations — is stated in the app rather than silently normalized. The Pathway "Equations of Reasoning" page matches [4] Table 1 notation but names the write "outer product of X and Y" (order reversed relative to the equation's v·kᵀ composition); we teach from the paper's equations.

## Contemporary relevance (why now)

- 2024–2025: delta-rule linear attention moved from theory to competitive 1B+ LMs with open code [1][2] — the additive rule's interference is their stated motivation ([1] §2.2).
- 2025: BDH reformulates attention as Hebbian synaptic memory, making fast weights the core of a brain-inspired post-Transformer architecture [4].
- 2026: BDH-CQ makes per-demonstration state accumulation (our toy's write, one level up) the mechanism of in-context skill acquisition on ARC-AGI-1, with latent recurrent reasoning and no inference-time parameter updates [5].

## What would falsify / weaken our teaching claims

- A reader reproducing the fixture and getting different numbers (tests + independent reference guard this).
- A future [4] revision changing Eq. (8): the module cites v1 explicitly.
- Independent replications failing to confirm [1][2][4][5] author-reported results would not falsify the toy's math but would change the maturity assessment; we labeled every such number author-reported for exactly this reason.
