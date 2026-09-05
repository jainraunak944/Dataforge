# Evidence file: Additive associative memory (fast weights) and the delta rule

Verified: 2026-09-05. All quotes and numbers below were taken from live-fetched primary text
(arXiv full text served through the Firecrawl research index; see Fetch log at the bottom for
what was and was not reachable). Nothing here is from memory alone.

Evidence categories used per claim:

- **[PRIMARY-QUOTED]** — verbatim text (≤25 words) copied from the fetched full text of the paper.
- **[PRIMARY-PARAPHRASE]** — restated from the fetched full text (equation transcribed from the fetched rendering).
- **[AUTHOR-REPORTED RESULT]** — a number copied exactly from the paper's own tables. Author-reported; not independently reproduced.
- **[METADATA]** — bibliographic data from the arXiv record (via the Firecrawl paper index and the arXiv version banner embedded in the fetched full text).
- **[INFERENCE]** — attribution I made that is consistent with, but not stated in one sentence of, the retrieved text. Flagged explicitly.

---

## 1. Yang et al. 2024 — DeltaNet parallelization (arXiv:2406.06484)

### Metadata [METADATA]

- **Exact title:** "Parallelizing Linear Transformers with the Delta Rule over Sequence Length"
- **Authors:** Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen, Yoon Kim (MIT / Soochow University / MIT-IBM Watson AI Lab)
- **Submitted (v1):** Mon, 10 Jun 2024 17:24:42 GMT
- **Latest version fetched:** v6 — the fetched full text carries the banner `arXiv:2406.06484v6 [cs.LG] 15 Jan 2025` (index "updated" field: 2025-01-16)
- **Categories:** cs.LG, cs.CL. Published at NeurIPS 2024 (not verified live — OpenReview unreachable; treat venue as unverified here).
- Full version history (v1–v5 dates) could not be verified: arXiv abs page unreachable (see Fetch log).

### Additive linear-attention memory update, as this paper writes it [PRIMARY-PARAPHRASE, orientation exact]

§2.1 ("Linear Transformer: Transformers with Linear Attention"), with kernel feature map φ:

> S_t = Σ_{i=1}^t v_i φ(k_i)^T ∈ R^{d×n},  z_t = Σ_{i=1}^t φ(k_i) ∈ R^n

and, after dropping the normalizer and taking φ = identity (§2.1, "Efficient training" paragraph):

> **S_t = S_{t−1} + v_t k_t^T,  o_t = S_t q_t**

**ORIENTATION:** value-times-key-transpose, i.e. **v_t k_t^T** with q_t, k_t, v_t, o_t ∈ R^d as **column vectors**; the state S is a matrix whose rows index the value dimension and columns index the key dimension (S_t ∈ R^{d×n} in the kernel form). Retrieval right-multiplies by the query: o_t = S_t q_t. The same equation reappears in the model-comparison Table 2 (§5.1) as the "Linear Attention" row, and §5.1 gives the general class "S_t = S_{t−1} • M_t + v_t k_t^T (recurrence), o_t = S_t q_t (memory read-out)".

### Delta-rule update in DeltaNet [PRIMARY-PARAPHRASE, equation transcribed exactly]

§2.2 ("DeltaNet: Linear Transformers with the Delta Update Rule"), inline (unnumbered) equation:

> **S_t = S_{t−1} − β_t (S_{t−1} k_t − v_t) k_t^⊤**

where β_t is the (data-dependent) learning rate, S_{t−1}k_t is the current prediction, v_t the target value. §2.2 also derives it as one SGD step on the online loss **L_t(S) = ½‖S k_t − v_t‖²** ("S_t = S_{t−1} − β_t ∇_{S_{t−1}} L_t(S_{t−1})"), and §3.1 gives the purely additive reparameterization **S_t = Σ_{i=1}^t u_i k_i^T with u_i = β_i (v_i − v_i^old)** (used to build the WY/chunkwise algorithm; UT transform in Eqs. 10–11, state update Eq. 8, output Eq. 9, recurrent form Eq. 7).

### Motivation — what problem with purely additive writes does it fix [PRIMARY-QUOTED]

§2.2, immediately after restating S_t = S_{t−1} + v_t k_t^T:

> "a purely additive update rule makes it difficult to deallocate past key-value associations, eventually leading to key 'collisions' when L > d" (citing Schlag et al.)

followed (same paragraph) by: "A model should ideally learn to remove less important key-value associations to make room for new ones" [PRIMARY-QUOTED, 18 words]. §2.2 adds that the additive/Hebbian-style rule "has limited memory capacity" (fast weight programming perspective), and that the delta rule "has been shown better memory capacity" (citing Gardner 1988; Prados & Kak 1989; and Schlag et al. 2021).

### Headline results usable for a comparison table [AUTHOR-REPORTED RESULT]

Setting for all rows: trained on a subset of SlimPajama, Mistral tokenizer, evaluated with lm-evaluation-harness. 340M models / 15B tokens; 1.3B models / 100B tokens (Table 1 caption and §A.1).

1. **Table 1, 1.3B / 100B tokens:** DeltaNet (w. conv): Wikitext ppl **16.87**, LAMBADA ppl **12.21**, zero-shot avg acc **51.6** — vs. Mamba (w. conv) 17.06 / 13.89 / 50.0, GLA (w/o conv) 17.22 / 14.47 / 51.0, Transformer++ 16.85 / 13.44 / 50.9. (§4.2 text: "DeltaNet outperforms the strong Mamba/GLA baselines in terms of both perplexity and downstream task performance.")
2. **Table 1, 340M / 15B tokens, recall-intensive tasks:** DeltaNet (w. conv) SWDE **26.4** / SQuAD **28.9** / FDA **12.8** vs. GLA (w. conv, same 128x state expansion) 24.0 / 24.7 / 7.3. §4.2: "under the same state size at the 340M scale, DeltaNet outperforms GLA, confirming the effectiveness of the delta rule."
3. **MQAR synthetic recall (Figure 4; seq. len 512, 64 key-value pairs):** §4.1: "DeltaNet performs perfectly (even without convolution) in the hardest setting and outperforms Mamba (which uses convolutions) in the low-dimension setting." (Curve figure — exact per-point numbers not tabulated in text.)

Caveat also author-stated (§4.2): at 1.3B on recall-intensive tasks DeltaNet **underperforms GLA** "due to its poorer state size scability", and at 3B scale DeltaNet-3B avg 59.8 slightly underperforms transformer PowerLM-3B 62.3 (Figure 5 table).

### Stated limitations relevant to memory capacity / interference [PRIMARY-QUOTED / PRIMARY-PARAPHRASE]

§5.3 "Limitations and Future Work":

1. Training speed "still lags behind that of GLA" (overhead of modeling state-to-state dependencies). [PRIMARY-QUOTED, 8 words]
2. Head-dimension / state-size scalability: "This limitation would potentially limit DeltaNet's memory size, consequently lowering the recall-intensive task performance" [PRIMARY-QUOTED, 14 words] (as observed in §4.2 at 1.3B).
3. "the length generalization of DeltaNet was limited" — "We speculate that this is because DeltaNet lacks explicit decay factors" [PRIMARY-QUOTED], fixable "through incorporating a gating term in the recurrence" (pointing to the Gated DeltaNet work).
4. §6 Related Work: vanilla linear transformers "use a Hebbian-like update rule, which has been shown to have limited memory capacity"; and "Irie et al. revealed theoretical limitations of the delta update rule in terms of expressiveness." [PRIMARY-QUOTED]

---

## 2. Yang, Kautz, Hatamizadeh 2024 — Gated Delta Networks (arXiv:2412.06464)

### Metadata [METADATA]

- **Exact title:** "Gated Delta Networks: Improving Mamba2 with Delta Rule"
- **Authors:** Songlin Yang (MIT CSAIL), Jan Kautz (NVIDIA), Ali Hatamizadeh (NVIDIA)
- **Submitted (v1):** Mon, 9 Dec 2024 13:09:04 GMT
- **Latest version fetched:** v3 — fetched full text carries the banner `arXiv:2412.06464v3 [cs.CL] 6 Mar 2025` (index "updated": 2025-03-07)
- **Categories:** cs.CL, cs.LG. Header of fetched text: "Published as a conference paper at ICLR 2025." [PRIMARY-QUOTED]
- Full version history (v2 date) not verifiable (abs page unreachable).

### The additive update and Mamba2's gated update, as this paper writes them [PRIMARY-PARAPHRASE, orientation exact]

§2.1 ("Mamba2: Linear Attention with Decay"), first display (inline, unnumbered):

> **S_t = S_{t−1} + v_t k_t^⊺ ∈ R^{d_v×d_k},  o_t = S_t q_t ∈ R^{d_v}**   (linear transformer)

Intro, inline: Mamba2's gated rule **S_t = α_t S_{t−1} + v_t k_t^⊺**, "which uniformly decays all key-value associations at each time step by a dynamic ratio, α_t ∈ (0, 1)." [PRIMARY-QUOTED, from Intro]

**ORIENTATION:** value-times-key-transpose **v_t k_t^⊺**; state explicitly typed **S ∈ R^{d_v × d_k}** (rows = value dim, columns = key dim); column vectors; read-out o_t = S_t q_t. Same orientation as the DeltaNet paper.

DeltaNet as re-stated here (§2.2):

> S_t = S_{t−1} − (S_{t−1}k_t)k_t^⊺ + (β_t v_t + (1−β_t) S_{t−1}k_t)k_t^⊺ = **S_{t−1}(I − β_t k_t k_t^⊺) + β_t v_t k_t^⊺**

i.e. "a first-order linear recurrence with generalized Householder transition matrices (I − β_t k_t k_t^⊺)" [PRIMARY-QUOTED, 13 words] — note the transition matrix multiplies S_{t−1} on the **right** in this orientation.

### The gated delta rule [PRIMARY-PARAPHRASE, equation transcribed exactly]

§3.1 "Formulation: Gated Delta Rule", **Eq. 10** (§3.3 and §3.4 both refer back to "the recurrence in Eq. 10" / "the gated delta rule (Eq. 10)"):

> **S_t = S_{t−1} (α_t (I − β_t k_t k_t^T)) + β_t v_t k_t^T**,  α_t ∈ (0, 1) a data-dependent gating/decay term.

Table 1 (§3, online-learning framework of Liu et al. 2024) gives the aligned family exactly as:

| Method | Online update |
|---|---|
| LA (linear attention) | S_t = S_{t−1} + v_t k_t^T |
| Mamba2 | S_t = α_t S_{t−1} + v_t k_t^T |
| DeltaNet | S_t = S_{t−1}(I − β_t k_t k_t^T) + β_t v_t k_t^T |
| **Gated DeltaNet** | **S_t = S_{t−1}(α_t(I − β_t k_t k_t^T)) + β_t v_t k_t^T** |

§3 also interprets it as SGD on L(S_t) = ½‖S_t k_t − v_t‖² with an added "adaptive weight decay term α_t" [PRIMARY-PARAPHRASE].

### What gating adds beyond the delta rule [PRIMARY-QUOTED]

- Abstract: "gating enables rapid memory erasure while the delta rule facilitates targeted updates" (12 words).
- Intro, on pure DeltaNet: "the model lacks the ability to rapidly clear outdated or irrelevant information, especially during context switches" (16 words).
- Intro, on the combined rule: "it can promptly clear memory by setting α_t → 0, while selectively updating specific content without affecting other information by setting α_t → 1" (23 words) — α_t → 1 "effectively switching to the pure delta rule".
- §3.2 case study (S-NIAH): "Gating facilitates filtering" (memory collision at long lengths without clearance); "Decay hurts memory retention" (Mamba2 "decays historical information too quickly" on S-NIAH-1); "Delta rule helps memorization" (S-NIAH-3 UUID values).

### Headline results [AUTHOR-REPORTED RESULT]

Training data: FineWeb-Edu subset, Llama2 tokenizer (32K vocab), 4K training length. The 400M-parameter ablations are explicitly "trained for 15B tokens" (Table S.1 caption). Table 2 is captioned "for 1.3B models"; Figure 3 is captioned "1.3B models on a single H100".

1. **Table 2, S-NIAH suite, 1.3B models (zero-shot accuracy):**
   - S-NIAH-2 (number in haystack) @4K: **Gated DeltaNet 92.2 vs. Mamba2 56.2 vs. DeltaNet 18.6** (@2K: 99.8 / 98.8 / 45.6).
   - S-NIAH-1 (pass-key) @8K: **DeltaNet 98.8 vs. Gated DeltaNet 91.8 vs. Mamba2 30.4** — the paper's own evidence that pure decay (Mamba2) hurts retention while the delta rule retains, and gating costs a little retention.
   - S-NIAH-3 (UUID) @2K: Gated DeltaNet 84.2 vs. Mamba2 47.6 vs. DeltaNet 47.0.
2. **Table 3, language modeling + zero-shot commonsense (covers 400M and 1.3B scales):** in the larger-scale block: **Gated DeltaNet Wikitext ppl 16.42, LAMBADA ppl 12.17, avg acc 55.32** vs. Mamba2 16.56 / 12.56 / 54.89, DeltaNet 17.71 / 16.88 / 52.14, Transformer++ 18.53 / 18.32 / 52.25; hybrids Gated DeltaNet-H1 16.07/12.12/56.40, H2 15.91/12.55/56.18. Paper text: "Gated DeltaNet consistently outperforms other linear models... at both scales." **[INFERENCE for the scale label:** the retrieved fragment did not include the block header row; the attribution of these rows to the 1.3B block is inferred from the 400M ablations averaging ~27–31 ppl (Table S.1) versus 16–19 ppl here, and from the surrounding 1.3B-captioned tables. Token count for the 1.3B run (100B, per the authors' code release) was not directly retrieved from the paper text — treat as unverified.**]**
3. **Table 4 (real-world retrieval: SWDE, SQuAD, FDA, TriviaQA, NQ, Drop), avg acc:** Gated DeltaNet **30.6** vs. Mamba2 29.8, DeltaNet 26.2; Transformer++ 37.0 still ahead. **Table 5 (LongBench, 14 tasks), avg:** Gated DeltaNet **16.6** vs. Mamba2 13.5, DeltaNet 13.6, Transformer++ 11.0.

### Stated limitations relevant to capacity / interference [PRIMARY-PARAPHRASE unless quoted]

No dedicated "Limitations" section was found in the retrieved full text. Relevant author-stated caveats:

1. Retrieval gap to attention remains: pure recurrent models show a "gap compared to Transformers" on real-world retrieval (Table 4 discussion; Transformer++ avg 37.0 vs Gated DeltaNet 30.6), and hybrids are the fix the paper itself reaches for.
2. Gating trades away some retention: S-NIAH-1 @2K–8K Gated DeltaNet (88.4–91.8) is below pure DeltaNet (96.8–98.8) — "Gated DeltaNet's degradation is less severe thanks to the use of delta rule" (§3.2) still concedes degradation vs. no-decay DeltaNet.
3. Throughput: Gated DeltaNet ≈ DeltaNet, "slightly slower than Mamba2 (2-3K tokens/sec) due to their more expressive transition matrices" [PRIMARY-QUOTED, §4 Throughput Comparison].
4. Fixed state size remains the root constraint: "their fixed state size makes it hard for retrieval tasks" [PRIMARY-QUOTED, §3.4 Hybrid models].

---

## 3. Schlag, Irie, Schmidhuber 2021 — Fast Weight Programmers (arXiv:2102.11174) — background

### Metadata [METADATA]

- **Exact title:** "Linear Transformers Are Secretly Fast Weight Programmers"
- **Authors:** Imanol Schlag*, Kazuki Irie*, Jürgen Schmidhuber (The Swiss AI Lab IDSIA, USI & SUPSI; * equal contribution)
- **Submitted (v1):** Mon, 22 Feb 2021 16:51:38 GMT
- **Latest version fetched:** v3 — fetched full text carries the banner `arXiv:2102.11174v3 [cs.LG] 09 Jun 2021` (index "updated": 2021-06-10)
- **Category:** cs.LG. Keywords block in the fetched text: "Machine Learning, ICML" (ICML 2021; venue page itself unreachable, see Fetch log).

### The fast-weight-programmer equivalence claim [PRIMARY-QUOTED]

Intro (§1): the paper emphasizes

> "the formal equivalence of this family of linear Transformers and the Fast Weight Controllers or Fast Weight Programmers (FWPs) from the '90s" (23 words)

"(apart from normalisation)" — and §3.2, after deriving Eqs. 15–19: "the core of linear Transformer variants are outer product-based Fast Weight Programmers." (12 words)

### Additive outer-product update, as this paper writes it [PRIMARY-PARAPHRASE, orientation exact, equation numbers exact]

§3.1 (softmax removed, no feature map), **Eqs. 10–11**:

> **W^(i) = W^(i−1) + v^(i) ⊗ k^(i)  (Eq. 10),  y^(i) = W^(i) q^(i)  (Eq. 11)**

§3.2 (linearised softmax with feature map φ and normalizer), **Eqs. 17–19**:

> **W^(i) = W^(i−1) + v^(i) ⊗ φ(k^(i))  (Eq. 17)**,  z^(i) = z^(i−1) + φ(k^(i))  (Eq. 18),  y^(i) = W^(i) φ(q^(i)) / (z^(i)·φ(q^(i)))  (Eq. 19)

**ORIENTATION:** outer product written **v ⊗ φ(k)** — value first, key second — equal to v φ(k)^T with column vectors; W ∈ R^{d_value × d_key} (Appendix A.2 states W ∈ R^{d_value×d_key} explicitly); read-out right-multiplies by φ(query). Same value-row/key-column orientation as both 2024 papers.

### Capacity argument — more associations than dimensions [PRIMARY-QUOTED / PRIMARY-PARAPHRASE]

§4.1 "Capacity Limitation":

- "Endlessly adding new associations to a memory of finite size, as in Eq. 17, inevitably will reach a limit." (19 words)
- Keys must be orthogonal to avoid interference at retrieval; with keys in a d_dot-dimensional space, "storing more than d_dot associations will result in a retrieval error." (11 words)
- "when the length of the sequence is longer than d_dot, the model might be in such an overcapacity regime" (19 words)
- Formal grounding via tensor product representations: "Theorem 3.3 and 3.1 of Smolensky 1990 discuss more formally the crosstalk and retrieval error" (§4.1, "Tensor Product Representation Theory" paragraph).

### Improved (delta-rule-like) update rule [PRIMARY-PARAPHRASE, equation numbers exact]

§4.2 "Improving the FWP's Programming Instruction", Eqs. 20–25:

> v̄^(i) = W^(i−1) φ(k^(i))  (Eq. 20) — retrieve value currently paired with the key
> β^(i) = σ(W_β x^(i))  (Eq. 21) — self-invented, dynamically changing learning rate ("write-strength")
> v_new^(i) = β^(i) v^(i) + (1−β^(i)) v̄^(i)  (Eq. 22)
> **W^(i) = W^(i−1) + v_new^(i) ⊗ φ(k^(i)) [write] − v̄^(i) ⊗ φ(k^(i)) [remove]  (Eq. 23)**
> **      = W^(i−1) + β^(i) (v^(i) − v̄^(i)) ⊗ φ(k^(i))  (Eq. 24)**,  y^(i) = W^(i) φ(q^(i))  (Eq. 25)

§4.2: "our programming instruction or update rule is effectively a delta rule with a dynamic learning rate β^(i)" (17 words) [PRIMARY-QUOTED]. Appendix B contrasts it with Peng et al. 2021's gated rule W^(i) = (1−β^(i))W^(i−1) + β^(i) v^(i)⊗φ(k^(i)) (Eq. 52): the delta rule "keeps the value associated with k_1 unmodified" when overwriting k_2's value, whereas uniform gating decays unrelated associations too — the paper's precise statement of *targeted* vs. *uniform* forgetting.

### Headline result (background paper; for context only) [AUTHOR-REPORTED RESULT]

WikiText-103 language modeling **without truncating context** (Table 4; fast weight memory carried across training segments): **Delta Network (their update rule): valid/test perplexity 27.8 / 29.4**, vs. **Linear Transformer (purely additive sum update): >260 / >260** — "the baseline Linear Transformer model with the naive sum update rule ... breaks" (§6.3 / Appendix D.3). Both models ≈90M params (89.9M vs 89.8M in the table). Synthetic setting 1 (§6.1.1) experimentally demonstrates the §4.1 capacity limit for linear attention.

### Stated limitation relevant to capacity/interference [PRIMARY-PARAPHRASE]

The §4.1 capacity bound applies to their own model too (finite d_dot); improving φ (DPFP, §5.4) raises d_dot but does not remove the bound. Practical caveat from the unlimited-context experiment: attention normalisation had to be removed for the Delta Network "since the accumulator blows up" (§6.3/App. D; the sum-normalisation interaction of the delta rule, discussed in §4.2).

---

## Cross-paper orientation summary (for the education material)

All three papers write the associative write as **value ⊗ key** (value-times-key-transpose) with column vectors, state = matrix mapping key-space → value-space, retrieval by right-multiplication with the (feature-mapped) query:

| Paper | Additive form | Delta / gated form | State shape |
|---|---|---|---|
| Schlag et al. 2021 | W^(i) = W^(i−1) + v^(i) ⊗ φ(k^(i)) (Eq. 17) | W^(i) = W^(i−1) + β^(i)(v^(i) − v̄^(i)) ⊗ φ(k^(i)) (Eq. 24) | W ∈ R^{d_value×d_key} |
| Yang et al. 2024 (DeltaNet) | S_t = S_{t−1} + v_t k_t^T (§2.1) | S_t = S_{t−1} − β_t(S_{t−1}k_t − v_t)k_t^⊤ (§2.2) | S ∈ R^{d×n} (value-dim × key-feature-dim) |
| Yang et al. 2024 (Gated DeltaNet) | S_t = S_{t−1} + v_t k_t^⊺ (§2.1) | S_t = S_{t−1}(α_t(I − β_t k_t k_t^T)) + β_t v_t k_t^T (Eq. 10) | S ∈ R^{d_v×d_k} |

Note for readers of other papers: some of the linear-attention literature uses the transposed convention (S_t = S_{t−1} + k_t v_t^T with read-out S_t^T q or q^T S). None of these three papers do; verify the convention before mixing equations across sources.

---

## Fetch log (2026-09-05)

| Target | Method | Result |
|---|---|---|
| https://arxiv.org/abs/{2406.06484, 2412.06464, 2102.11174} | curl (agent proxy) | **FETCH FAILED** — CONNECT tunnel 403, `connect_rejected` (egress proxy policy) |
| https://arxiv.org/pdf/{all three} | curl (agent proxy) | **FETCH FAILED** — CONNECT tunnel 403 (same policy block) |
| https://arxiv.org/abs/{all three} | WebFetch | **FETCH FAILED** — `EGRESS_BLOCKED: Access to arxiv.org is blocked by the network egress proxy` |
| https://ar5iv.labs.arxiv.org/html/2406.06484 (mirror) | curl | **FETCH FAILED** — CONNECT tunnel 403 (`ar5iv.labs.arxiv.org` connect_rejected); a second curl attempt was denied by the sandbox permission classifier |
| https://export.arxiv.org/abs/2406.06484 (mirror) | curl | **FETCH FAILED** — CONNECT tunnel 403 |
| openreview.net, proceedings.mlr.press, aclanthology.org, semanticscholar.org | curl reachability probe | **FETCH FAILED** — all blocked by egress proxy (so conference-page venue confirmation was not possible) |
| arXiv metadata, all three papers | Firecrawl MCP `research_inspect_paper` | **OK** — titles, authors, abstracts, created/updated dates |
| Full text, arXiv:2406.06484 | Firecrawl MCP `research_read_paper` (3 queries) | **OK** — passages from the arXiv HTML rendering; embedded banner confirms **v6, 15 Jan 2025** |
| Full text, arXiv:2412.06464 | Firecrawl MCP `research_read_paper` (4 queries) | **OK** — passages from the paper text; embedded banner confirms **v3, 6 Mar 2025**; "Published as a conference paper at ICLR 2025" header present |
| Full text, arXiv:2102.11174 | Firecrawl MCP `research_read_paper` (2 queries) | **OK** — passages from the arXiv HTML rendering; embedded banner confirms **v3, 09 Jun 2021** |

Provenance caveat: because arxiv.org itself was unreachable from this environment, full text came through Firecrawl's index of the arXiv HTML renderings (the fetched passages include the literal arXiv version banners quoted above). Equations were transcribed from those renderings; math in arXiv HTML conversions can occasionally mis-render, so anyone reusing an equation load-bearingly should spot-check it against the PDF from an unrestricted network. Complete per-version submission histories (dates of v2…v5) were not retrievable. All benchmark numbers are author-reported.
