# BDH (Dragon Hatchling) — verified research notes

Compiled 2026-09-05 by live retrieval of primary sources. Every claim below carries a locator
(section / equation / figure / table number, or a verbatim quote) and an evidence category:

- **[F]** formal/theoretical (definition, claim, or proof in the paper)
- **[AE]** author-reported empirical (experiment run and reported by the Pathway authors)
- **[IE]** independently evaluated (third party); note: none of the claims below reach this bar
  except where explicitly discussed (ARC-AGI replication, which is itself only *reported by Pathway*)
- **[PA]** partnership/marketing announcement (not validation of any technical claim)

**Access constraints for this session (see Fetch log):** the network egress proxy blocked
`arxiv.org` (abs, pdf, html, ar5iv, export), `pathway.com`, `aws.amazon.com`, `finance.yahoo.com`,
`web.archive.org`, `huggingface.co`, `alphaxiv.org`, and `api.semanticscholar.org` — for curl AND
for the WebFetch tool. Paper full text was therefore read live through the Firecrawl research
index, which serves the body of the **arXiv HTML v1** rendering (`arxiv.org/html/2509.26507v1` —
all internal anchors in the retrieved text point at `...v1`). The GitHub repo was cloned directly
(git worked through the proxy) and read from disk. Pathway web pages were retrieved as extended
verbatim excerpts from the Firecrawl web index, except one page that is not indexed (flagged below).

---

## 1. Citation metadata

- **Title:** *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain*
  (title banner of v1 HTML: `arXiv:2509.26507v1 [cs.NE] 30 Sep 2025`).
- **Authors (in order):** Adrian Kosowski (corresponding), Przemysław Uznański, Jan Chorowski,
  Zuzanna Stamirowska, Michał Bartoszkiewicz. Affiliation line: "Pathway, Palo Alto, USA",
  contact `research@pathway.com`. (Front matter of v1; equal-contribution footnote on authors 2–5.)
- **Year:** 2025. **arXiv ID:** 2509.26507. **Categories:** cs.NE, cs.AI, cs.LG, stat.ML
  (Firecrawl canonical metadata; created "Tue, 30 Sep 2025 16:49:01 GMT", index updated 2025-10-01).
- **Version read:** **v1 (30 Sep 2025)**, via the arXiv HTML v1 mirror in the Firecrawl index.
  Existence of any later revision (v2, v3, …): **UNVERIFIED** — arxiv.org unreachable from this
  environment; every citation found elsewhere (repo README, Pathway pages, third-party posts)
  references v1 or the unversioned ID.
- License shown on the paper: "arXiv.org perpetual non-exclusive license" (v1 front matter).
- Repo README citation block: "*A. Kosowski, P. Uznański, J. Chorowski, Z. Stamirowska,
  M. Bartoszkiewicz.* The Dragon Hatchling …, arXiv (2025)" (README.md, pathwaycom/bdh).

---

## 2. The core equations (state update / attention-as-synaptic-memory)

### 2.1 Notation and dimensions (paper §3.1 "Notation for BDH-GPU")

| Symbol | Space / shape | Meaning (locator) |
|---|---|---|
| `n` | scalar | number of neurons/particles; the single scaling dimension (§3.1; Claim 2) |
| `d` | scalar | low-rank dimension, "log n < d ≪ n (d=256 in practice)" (Claim 2); vectors in R^d are "(fuzzy) addresses of a virtual memory space of size n" (§3.1) |
| `L` | scalar | number of layers; "e.g. L=8 in most of this paper" (§2.2) |
| `x_{t,l}` | (R⁺)^n, column | neuron activations; serves as **query** (at time t) and **key** (at times τ<t) (§6.1) |
| `y_{t,l}` | (R⁺)^n, column, sparse | second activation vector; its low-rank image is the **value** source; "typically sparse in the sense of ‖y‖₀" (Fig. 3 caption) |
| `v*_{t,l} = LN(E y_{t,l})` | R^d | "attention 'value' inputs" (§3.2, State-space representation) |
| `a*_{t,l}` | R^d | "the result of a linear attention mechanism for time t in layer l" (§3.2) |
| `σ_{t,l}` | R^{n×n} | synaptic state matrix, "interpretation as synapse weights that connect neurons" (§6.2) |
| `ρ_{t,l} = E σ_{t,l}` | see note below | compressed state (Fig. 3; §3.1: "a compressed form with reduced dimensionality, ρ = Eσ") |
| `E` | R^{d×n} | learned encoder, "reduce dimensionality of activation vectors (e.g., a* = Ez)" (§3.1) |
| `D_x, D_y` | R^{n×d} | learned decoders, "lift them back into R^n" (§3.1) |
| `U` | R^{n×n} | "a diagonal or block-diagonal matrix representing local rotation or damping of state (such as ALiBi or RoPE)" (Def. 4) |
| `G_x^e, G_x^i, G_y^e, G_y^i, G_s` | R⁺^{n×n} | neuron–neuron interaction graphs of graph-BDH (§2.2, Table 1) |
| `(z)^+` | — | ReLU, "(z)^+ := max{0, z_i}" coordinatewise (§3.1, "Nonlinearities: ReLU and LayerNorm") |
| `LN(·)` | R^d → R^d | non-parametric LayerNorm, `LN(z*) = (z* − 1·E_d z*)/σ_d z*` (§3.1) |

Parameter count: "The model has 3nd + 2Ωd = (3+o(1))nd parameters" with trainable set
`M = (E, D_x, D_y, f_e, f_d)`; f_e: Ω→R^d token encoder, f_d: R^d→Ω token decoder
(§3.2, "BDH-GPU as a language model"). Vector convention: **column vectors**;
"a one-dimensional vector is denoted by a lower-case letter, e.g., z, with z ∈ R^{n×1}";
d-dimensional vectors carry an asterisk (§3.1).

**Shape wobble worth flagging for teaching:** Fig. 3's caption and §6.1 state
"ρ_{t,l} ∈ R^{n×d}" / "The matrix ρ ∈ R^{n×d}", but the displayed recurrences compose as
`ρ = Eσ` with `E ∈ R^{d×n}`, `σ ∈ R^{n×n}`, i.e. **d×n**; likewise Eq. (5)/(8) build ρ from
`(d×1)(1×n)` outer products. The paper uses the two orientations interchangeably (transpose);
the §8.2-area comparison table also calls the per-layer attention state an "n×d tensor".

### 2.2 BDH-GPU inference dynamics — Definition 4, Eq. (4) (§3.2)

Verbatim (de-mangled from the v1 HTML; symbols as in the paper):

```
x_{t,l}  := x_{t,l-1} + ( D_x v*_{t,l-1} )^+
a*_{t,l} := Σ_{τ<t} v*_{τ,l-1} x_{τ,l}^T U^{t-τ} x_{t,l}
y_{t,l}  := ( D_y LN(a*_{t,l}) )^+ ⊙ x_{t,l}
v*_{t,l} := LN( E y_{t,l} )                                   (4)
```

"where inputs to the system are provided through the boundary condition v*_{τ,0} in layer 0"
(Def. 4). A BDH-GPU(n,d) system is "given by three parameter matrices: E ∈ R^{d×n} and
D_x, D_y ∈ R^{n×d}" (Def. 4). **[F]**

### 2.3 The synaptic state (Hebbian write) and readout — Eqs. (5), (8), (16)

Attention state definition (§3.2, Eq. (5)):

```
ρ_{t-1,l} = Σ_{τ<t} v*_{τ,l-1} x_{τ,l}^T U^{t-τ}              (5)
```

State-space form of **BDH-GPU** (Fig. 3, Eq. (8)) — this is "the primary point of reference for
all model training and all empirical results presented in this study" (Fig. 3 caption):

```
ρ_{t,l} := ( ρ_{t-1,l} + LN(E y_{t,l-1}) x_{t,l}^T ) U        — Hebbian write (rank-1 outer product)
x_{t,l} := x_{t,l-1} + ( D_x LN(E y_{t,l-1}) )^+              — residual feed-forward
y_{t,l} := ( D_y LN( ρ_{t-1,l} x_{t,l} ) )^+ ⊙ x_{t,l}        — readout (query = x_{t,l})   (8)
```

Recovery of the full synaptic matrix (§6.2, Eq. (16)):

```
σ_{t-1,l} = Σ_{τ<t} y_{τ,l-1} x_{τ,l}^T U^{t-τ}               (16)
```

Key structural facts, all **[F]**:

- **Write:** additive rank-1 outer product `y x^T` (or its low-rank image `LN(Ey) x^T`) added to
  the running state each token — the readout uses `ρ_{t-1,l}` / `σ_{t-1,l}`, i.e. the state
  **before** the current token's write (strict causality, `Σ_{τ<t}`).
- **Decay:** yes, via right-multiplication by `U` each step (equivalently `U^{t-τ}` inside the
  sums): "local rotation or damping of state (such as ALiBi or RoPE)" (Def. 4). In the graph
  formulation the same thing appears as the per-edge decay rule `σ_l(i,j) ↓_{1−u(i,j)}` with
  "damping hyperparameters on state, u>0 … defined separately as u(i,j) for each edge" (§2.2 +
  Table 1). Empirically: "damping of historical signals over long sequences is necessary in
  BDH-GPU to avoid overwhelming the model with noise from stale context" — RoPE+ALiBi suffice
  (§6.1, "Natural support for long context"). Note the decay acts on the **x (key) index** side.
- **Key/query/value roles (§6.1, "Basic properties of BDH-GPU attention"):** "The key-query space
  for BDH-GPU is R^n"; keys and queries "are expressed by the same vector x_{t,l} (noting that at
  time t, x_{t,l} is used as a query, and only x_{τ,l}, for τ≤t−1, are used as keys)";
  "'Value' vectors of BDH-GPU remain in the small dimension, R^d".
- **ReLU / non-negativity:** activations pass through `(·)^+` everywhere (Eqs. 4/6/7/8);
  "Activation vectors x,y of BDH-GPU are positive (after passing through ReLU gates)" (§4.2 list);
  "BDH-GPU uses the positive orthant (R⁺)^n as its latent space … Attention keys and queries are
  prepared entirely in this positive orthant" (§6.1). The multiplicative gate `⊙ x_{t,l}` in the
  y-update is interpreted as replicator-dynamics competition (§2.5 discussion of Round 4l+2).
- **Linear-attention connection — explicit in the paper:** §3 intro step 2: "Never materialize the
  σ state matrix, preferring instead to access it using a linear attention operation over low-rank
  representation of values"; §3.2: a*_{t,l} is "the result of a linear attention mechanism";
  Section 6 is titled "Analysis: linear attention, sparse positive activation, and
  monosemanticity"; §4.2 list: "Attention of BDH-GPU is linear, but happens in the model's large
  neuronal dimension." General attention is formalized as `a_t = Σ_{τ=1}^{t−1} φ(k_t,k_τ) v_τ`
  (Eq. (14), §6.1), with the softmax/linear-attention relation attributed to FAVOR+
  (Choromanski et al., 2021). Claim 7 [F]: linear attention in R^n expresses affinities for up to
  ~Õ(n) key-value pairs (formal statement in Appendix C.2).
- The state is explicitly called **fast weights**: BDH dynamics use "fast-weight-like state
  variables σ(i,j), defined on a subset of edges of the system" (§2.2, "Inference dynamics of
  BDH"); the Hebbian reading is stated at Fig. 13: "The synapse is updated using a Hebbian
  learning rule when activity in y activations at a preceding layer … leads to firing of neuron x
  in the next layer."

### 2.4 Graph-BDH and BDH-Normfree — Eqs. (6), (7), (9) (Fig. 3)

**BDH (graph form), Eq. (6):**

```
σ_{t,l} := ( σ_{t-1,l} + ((y_{t,l-1} x_{t,l}^T) ⊙ G_s) ) U
x_{t,l} := x_{t,l-1} + ( (G_x^e − G_x^i) y_{t,l-1} )^+
y_{t,l} := ( (G_y^e − G_y^i) σ_{t-1,l} x_{t,l} )^+ ⊙ x_{t,l}      (6)
```

**BDH-Normfree (intermediate, no LayerNorm), Eq. (7):**

```
σ_{t,l} := ( σ_{t-1,l} + y_{t,l-1} x_{t,l}^T ) U      }  alternative
ρ_{t,l} := ( ρ_{t-1,l} + (E y_{t,l-1}) x_{t,l}^T ) U  }  representations
x_{t,l} := x_{t,l-1} + ( D_x E y_{t,l-1} )^+
y_{t,l} := ( D_y  E σ_{t-1,l}  x_{t,l} )^+ ⊙ x_{t,l}     [Eσ_{t-1,l} braced as ρ_{t-1,l}]   (7)
```

**Equivalence of parameters (Observation 4, Eq. (9)):**

```
G_x^e − G_x^i = D_x E,   G_y^e − G_y^i = D_y E,   G_s = 1^{n×n}    (9)
```

"where 1^{n×n} is the all-ones matrix" — i.e. BDH-Normfree/BDH-GPU is the special case of graph-
BDH whose synapse graph is complete and whose interaction graphs are ReLU-low-rank products. **[F]**

---

## 3. Graph/neuron-synapse BDH vs. BDH-GPU (locators)

- Graph-BDH is defined in **§2** ("BDH: a language model architecture given by local distributed
  graph dynamics"): §2.1 interaction/edge-reweighting kernel formalism (Definitions 1–2);
  §2.2 Definition 3 + **Table 1 "the equations of reasoning"** — local rules on n neurons,
  scheduler executing 4 rule-columns per layer, "ingesting new tokens every 4L rounds"; state
  variables X(i), Y(i), A(i) at neurons and σ(i,j) at synapse edges of G_s. **[F]**
- Table 1 rules (Communication row, verbatim): `X(i), σ_l(i,j) → A(j)` (Round 4l);
  `Y(i), X(j) →[G_s(i,j)] σ_l(i,j)` (Round 4l+1 — the Hebbian write);
  `A(i) →[G_y^e(i,j)] Y^e(j)`, `A(i) →[G_y^i(i,j)] Y^i(j)` (4l+2);
  `Y(i) →[G_x^e(i,j)] X^e(j)`, `Y(i) →[G_x^i(i,j)] X^i(j)` (4l+3). Computation row includes decay
  `σ_l(i,j) ↓_{1−u(i,j)}` and thresholdings `(Y^e(i) − Y^i(i))^+, X(i) → Y(i)` and
  `(X^e(i) − X^i(i))^+ → X(i)`.
- The restriction from BDH to BDH-GPU (§3 preamble / Claim 1-2 area): "This restriction is
  obtained by treating the communication of the n particles as proceeding through a mean-field
  ('radio network'), rather than a graph ('communication by wire')". Three steps (§3 intro):
  (1) "Express graphs G_x and G_y [as] low-rank factorizations of their transition matrices,
  followed by ReLU nonlinearities"; (2) never materialize σ, use linear attention;
  (3) "Normalize all state variables using LayerNorm."
- Equivalence & expressiveness: Observation 1 (Table 1 ruleset ≡ Eq. (6)) with proof in App. C.1;
  Observation 4 + Eq. (9); §3.4 "In general, BDH is not less expressive than its tensor-based
  counterpart"; §3.4.1 encodes D·E products as squared sparse graphs G ∈ 𝒢²(n,m) (Claim 3/4,
  App. C.4). **[F]**
- Table (Conclusions area, §8.2 vicinity) contrasts columns "Transformer (GPT2) | BDH-GPU(n,d) |
  BDH(n,Δ) | Brain models": e.g. attention state "n×d tensor for each layer (localized at
  neurons)" vs "Memory on synapse edge weights".
- Biological reading: Observation 2 (§2.5): the ruleset reduces to "neuron activation with
  positive state variables, Hebbian learning, and communication through excitatory and inhibitory
  circuits with thresholding". Abstract: "The working memory of BDH during inference entirely
  relies on synaptic plasticity with Hebbian learning using spiking neurons." **[F]/[AE]**

---

## 4. Reported empirical results relevant to teaching

All results below are **author-reported empirical [AE]** from the paper (v1) unless stated.

- **Sparsity ≈ 5%:** Empirical Finding 1: "The positive activations of BDH-GPU exhibit sparsity
  (at about 5% level) in the y vectors of its state space dynamics". §4.1: "in a typical training
  run, only ρ≈5% of the n entries of vector x_t are non-zero". Fig. 14 (synthetic memorization
  task, n=65536, d=256, L=4, letter tokens): layer-2 activations "4.0%−7.5% non-zero entries
  during memorization and approximately 2.5% … during repetition" (§6.4).
- **Monosemantic synapses:** §6.3 + Figs. 12–13: identified σ entries acting as a "currency
  synapse" and "country synapse" on a Europarl-trained model (App. B.3: d=256, n=49152, 4 heads,
  8 layers, ~1.9B tokens En-Es/Pt/Fr); same synapse fires for "livre sterling" vs "British
  Pound". Selectivity test: 50 currency vs 50 contrast sentences (generated with ChatGPT),
  one-sided Mann–Whitney "U=2368 with U_opt=2500, p<10⁻¹⁴"; rank-biserial correlation 0.86.
- **Scale-free connectivity:** Fig. 11 caption: "BDH's state σ encodes neuron connections as a
  scale-free graph showing clear heavy-tailed (power-law-like) degree distribution" (σ computed
  for head 0, layer 5 of an 8-layer Europarl model; negative RoPE-induced entries filtered and a
  small positive threshold applied — §6.2). Emergent structure also in *parameters* (§5.5,
  Fig. 10, thresholded G_x := D_x E). Modularity claims are theoretical (§5.4, Claim 6,
  Observation 6) **[F]**.
- **GPT-2-comparable language performance:** Empirical Finding 1: "follow[s] scaling laws
  (parameters vs. loss) of optimized Transformers in the GPT architecture, at parameter scales
  between 10M to 1B". Fig. 7 (translation task): "We observe that BDH-GPU' matches the GPT
  Transformer at all model sizes we have evaluated." Setup (App. B.1–B.2): Europarl En-PL +
  En-Cs, 380MB, raw UTF-8 bytes, 1.2B tokens ≈ 3 epochs, TBPTT with carried state; baseline
  "GPTXL" = GPT2-like NanoGPT + TransformerXL-style carried KV-cache + ALiBi. Concrete size grid
  in Tables 4–5: 25M/50M/100M/200M/400M/800M; all BDH runs use d=256, 8 layers, 4 heads, n from
  32768 to 1048576. (Abstract also claims 10M-1B on "language and translation tasks".)
- **Model merging (§7.1, Table 2/6, Fig. 15):** two 19M models (n=24576) fine-tuned from a common
  En-Es base on En-Fr / En-Pt were merged by **concatenating** all n-dimension tensors (D_y, D_x,
  E, RoPE buffers) and averaging the rest → 38M model (n=49152) that translates all pairs without
  further training (qualitative; language mixing observed in samples).
- **Training without backpropagation through time (§7.2):** detaching K,V raises English loss
  from ≈0.65 to ≈0.75–1.05; model "lost the ability to match concepts between different
  languages during translation". Preliminary.
- **Sudoku:** **NOT FOUND IN PAPER.** The only related phrase is §4.2: BDH-GPU "learns faster per
  data token … and on synthetic puzzles" (no benchmark named). The 97.4% Sudoku-Extreme claim is
  from Pathway's site/README only (see §7 below).
- **Long context:** in-paper support is architectural/theoretical: "There is no notion of context
  length in BDH-GPU, and consequently no hard bound on it" (§4.2 list); Claim 7 (≈Õ(n) facts)
  **[F]**; plus the §6.1 damping caveat. Specific long-context benchmark numbers (e.g. BABILong):
  **NOT FOUND IN PAPER** (Pathway's homepage reports BDH 134M: 95% at 32K / 82% at 128K on
  BABILong QA1-QA5, "pending final contamination checks, independent validation, and leaderboard
  review" — company-reported [AE], retrieved via search index).

---

## 5. What BDH has that a 2×2 additive outer-product toy memory omits

A toy `S ← S + v k^T`, `out = S q` memory captures only the write of Eq. (7) line 1 and the bare
readout. The paper's full machinery on top of that (locators in parentheses):

1. **ReLU thresholding / non-negativity** on both activation pathways: `(·)^+` in every x/y update
   (Eqs. 4, 6–8); excitatory-minus-inhibitory thresholding `(Y^e−Y^i)^+`, `(X^e−X^i)^+`
   (Table 1(b); Observation 2, §2.5).
2. **Multiplicative gating of the readout by the query**: `y := (…)^+ ⊙ x_{t,l}` — replicator-
   dynamics "competition effect between neurons" (Eqs. 6–8; §2.5).
3. **State decay / positional damping**: right-factor `U` (RoPE/ALiBi) in every state update;
   per-edge `σ ↓_{1−u(i,j)}` (Def. 4; Table 1; §6.1 damping discussion).
4. **Learned encoder/decoder matrices** `E ∈ R^{d×n}`, `D_x, D_y ∈ R^{n×d}` giving the ReLU-
   low-rank feed-forward and the compressed d-dim value channel (Def. 4; §3 intro step 1).
5. **LayerNorm on all state variables** (§3 intro step 3; LN in Eqs. 4 and 8).
6. **Layer structure with a residual stream**: L layers, `x_{t,l} := x_{t,l-1} + …`, separate
   state per layer, y fed forward across layers (Def. 4; Fig. 6 per §4.2).
7. **Strictly causal read-before-write**: readout uses σ_{t−1}/ρ_{t−1}, sums over τ<t
   (Eqs. 5, 8, 16).
8. **High-dimensional sparse positive key/query space (R⁺)^n with values in small R^d** — the
   n vs d asymmetry is the whole geometry (§6.1); sparsity ≈5% (§4.1).
9. **Token encoder/decoder** f_e: Ω→R^d, f_d: R^d→Ω (§3.2, "BDH-GPU as a language model").
10. **Graph dynamics generalization**: selective synapse graph G_s, excitatory/inhibitory circuit
    graphs, per-edge damping — the full BDH of Table 1/Eq. (6), of which BDH-GPU is the mean-field
    special case with G_s = all-ones (Eq. (9)).
11. **Multi-head + RoPE neuron pairing** in practice (heads: §4.1; Fig. 4: d=256, k=2 pairing,
    h heads; Tables 4–5: 4 heads).

---

## 6. Pathway explainer/derivation pages

### 6.1 https://pathway.com/research/bdh-explainer/bdh-architecture-derivation (Chapter 2)

**FETCH FAILED** for the page body: direct curl → proxy `CONNECT tunnel failed, response 403`;
WebFetch → `EGRESS_BLOCKED: pathway.com`; Wayback Machine also blocked; the page's body is not in
the Firecrawl web index (only the series landing page is). What the landing page
(`pathway.com/research/bdh-explainer`, retrieved via index) says about it, verbatim:

> "Chapter 2 derives BDH from the attention equations, reframing retrieval as synaptic memory in
> a high-dimensional sparse neuron space and showing how Hebbian updates and low-rank
> factorization lead to the practical BDH-GPU architecture. It then highlights the key
> differences between BDH and the Transformer."

Consequently a notation/orientation comparison of *this specific page* against the paper is
**UNVERIFIED — page body not retrievable from this environment**. Do not cite chapter-2-specific
equations without re-fetching from an unrestricted network.

### 6.2 https://pathway.com/research/bdh-explainer/brain-inspired-ai-architecture (Chapter 1)

Direct fetch blocked (same as above); extended verbatim excerpts retrieved via Firecrawl index.
Section headings seen: "1.4 The brain as nature's scale-free network", "1.5 The design
requirements for a brain-inspired model", "1.6 Why synaptic memory is the right memory
architecture". The four design requirements, verbatim (§1.5): "Neurons as identifiable
computational units", "Synapses as identifiable connections", "Network-centric memory",
"State tracking on synapses". Notable line: "Memory should live in the network, not as a
separate, ever-growing list of token-indexed traces." Non-technical framing; no equations in the
retrieved excerpts. **[AE/PA]** (company explainer of its own paper).

### 6.3 https://pathway.com/research/the-equations-of-reasoning

Direct fetch blocked; **substantial verbatim excerpts retrieved via Firecrawl index**, including
its full re-rendering of the paper's Table 1 (sourced: "**Source**: BDH paper, Table 1").

How it presents attention→synapses (verbatim):

> "They rewrite attention as a local physical process on a graph of neurons as follows. First,
> each token activates a set of neurons. Then, their activity reads and updates the memory stored
> in the synapses, while the learned graph determines where activity flows next."

> "Step 2 (round 4l+1): the system reweights the synaptic state with the outer (or Hebbian)
> product of X and Y to update synaptic connections. This is similar to a standard state-space
> model (SSM) memory write."

> "**attention ⪯ BDH-GPU ⪯ local neuron-synapse dynamics**" (§5.1, "a rigorous bridge from fast
> weights and attention to local synaptic dynamics"; page cites paper Appendices C.1, C.3, C.4).

**Notation comparison with the paper (observed differences/agreements):**

- Symbols match the paper exactly: σ_l(i,j), G_x^e/G_x^i/G_y^e/G_y^i/G_s, decay written
  `σ_l(i,j) ↓_{1−u(i,j)}`, tokens every 4L rounds, L=8 example. No re-indexing, no row/column
  flip is visible in the retrieved fragments (the page reproduces the paper's Table 1 rather than
  the tensor Eqs. (4)/(8), so the x^T-vs-x orientation question does not arise there).
- **Ordering discrepancy (minor, cosmetic):** the page describes the write as "the outer (or
  Hebbian) product of X and Y"; the paper's tensor equations write the outer product as
  `y_{t,l-1} x_{t,l}^T` (y indexes rows/post-side, x indexes columns/key-side) and its Table 1
  rule as `Y(i), X(j) → σ_l(i,j)`. Same object; the page's prose reverses the naming order only.
- The page's simplified Table 1(a) rendering shows Round 4l+2 as `A(i), X(j) →[G_y^e(i,j)] Y(j)`
  (query-gating folded into the rule); the general version (b) matches the paper's
  `A(i) → Y^e(j)` / `A(i) → Y^i(j)` + threshold form.
- Round labels on the page: "Inference from state / Reweighting of synapse state / Neuron
  replicator dynamics + inference from parameters / Inference from parameters" — these labels
  also appear in the paper's v1 Table 1 header (seen in the arXiv HTML snippet), so they are not
  a Pathway addition.
- The decay factor is present on the page (same `↓_{1−u(i,j)}` symbol); no discrepancy.

---

## 7. Official repo — github.com/pathwaycom/bdh

Cloned 2026-09-05 (depth-1); HEAD = `2b0d7a45b058d4309c84a10e0768d541fe18bdc2`,
"Update README.md", Fri May 15 2026. Local copy at
`/tmp/claude-0/-home-user-Dataforge/e9443645-223b-5476-ac0b-a77cdb163112/scratchpad/bdh-repo`.

- **License:** MIT (LICENSE.md; verbatim first lines: "Copyright 2025 Pathway Technology, Inc."
  + standard MIT permission/warranty text).
- **Contents:** `bdh.py` (172 lines — model), `train.py` (~120 lines — training script on tiny
  Shakespeare, byte-level, BLOCK_SIZE 512, BATCH_SIZE 32, MAX_ITERS 3000, LR 1e-3, weight decay
  0.1, AdamW implied via torch), `README.md`, `requirements.txt` (`torch, numpy, requests`),
  `figs/`, `.gitignore`. No notebooks (a `notebooks/` mention is commented out in README). README:
  "This repository contains the official implementation from the paper".
- **What the code implements:** the BDH-GPU formulation in **token-parallel (training) form** —
  it materializes the T×T linear-attention score matrix instead of carrying an explicit recurrent
  ρ/σ state (the paper's Appendix E "didactic code listing" counterpart). State/attention
  implementation, `bdh.py` lines 72–74:

  ```python
  # Current attention
  scores = (QR @ KR.mT).tril(diagonal=-1)
  return scores @ V
  ```

  No softmax; `tril(diagonal=-1)` = strictly-causal Σ_{τ<t}, matching Eqs. (4)/(5). Q and K are
  the *same* sparse n-dim vector (`assert K is Q`, line 58) — matching "keys and queries … are
  expressed by the same vector x_{t,l}" (§6.1) — with RoPE applied (lines 61–70) playing the role
  of U^{t−τ}. The layer loop, lines 122–144:

  ```python
  for level in range(C.n_layer):
      x_latent = x @ self.encoder
      x_sparse = F.relu(x_latent)          # B, nh, T, N
      yKV = self.attn(Q=x_sparse, K=x_sparse, V=x)
      yKV = self.ln(yKV)
      y_latent = yKV @ self.encoder_v
      y_sparse = F.relu(y_latent)
      xy_sparse = x_sparse * y_sparse      # gate ⊙
      ...
      yMLP = (xy_sparse.transpose(1, 2).reshape(B, 1, T, N * nh) @ self.decoder)
      y = self.ln(yMLP)
      x = self.ln(x + y)                   # residual
  ```

- **Code vs paper notation (differences to record):**
  - Row-vector convention (`x @ self.encoder`) vs the paper's column vectors (`E y`); the code's
    `encoder` (shape `(nh, D, N)`) plays E-transposed per head; `decoder` `(nh*N, D)` plays a
    D_x/D_y-like role; there is an extra `encoder_v` `(nh, D, N)` not named in Eq. (8).
  - Dim names: code `D` = paper d (default `n_embd=256`); code `N = mlp_internal_dim_multiplier
    * D // nh` = per-head neuron dimension (128·256/4 = 8192 by default); `n_layer=6` default
    (paper experiments use 8).
  - Attention **values** in code are the d-dim residual stream `x` itself (`V=x`), whereas
    Eq. (4) uses `v* = LN(E y)` from the previous layer; same low-dim-value design, different
    plumbing. The x-update `(D_x v*)^+` branch of Eq. (4) is not a separate branch in code — the
    residual+MLP path covers it.
  - **No explicit decay factor in code** beyond RoPE rotation of Q/K (`get_freqs`, theta=2^16,
    frequency-quantized in pairs — the paper's k=2 neuron pairing); no ALiBi in the repo.
- **README claims** (author-reported): "BDH matches **GPT-2-scale Transformers** across language
  and translation tasks at equivalent parameter scales (10M-1B)"; Sudoku table (97.4% vs ~0% for
  "Leading LLMs (O3-mini, DeepSeek R1, Claude 3.7 8K)", "~250,000 difficult puzzles", LLM scores
  sourced to arXiv:2506.21734). Crucially the README itself flags: "The Sudoku Extreme result
  refers to Pathway's internal BDH implementation, not to the current open-source repository …
  does not reproduce the 97.4% benchmark result out of the box." **[AE]**, and the Sudoku result
  is **not reproducible from the released code** by the authors' own statement.

---

## 8. Amazon SageMaker HyperPod / AWS integration claim

- Primary sources located but **direct fetch blocked** (aws.amazon.com, finance.yahoo.com,
  pathway.com all EGRESS_BLOCKED; content below retrieved as verbatim excerpts via the Firecrawl
  web index — treat as near-primary, re-fetch for archival citation):
  1. AWS Startups article: `https://aws.amazon.com/aws-startups/learn/pathways-bdh-a-new-post-transformer-approach-to-enterprise-ai-on-aws/`
     (listed on Pathway's blog as "AWS Startups … May 3, 2026"). Search snippet: "Pathway, an AWS
     frontier model partner, is pioneering this next generation of AI with Dragon Hatchling
     (BDH). Developed on Amazon SageMaker and optimized for …". **[PA]**
  2. Pathway press release, `https://pathway.com/blog/pathway-150m-model-breaks-arc-agi-1-cost-efficiency-frontier`
     (dated Aug 11, 2026 in Pathway's blog listing), quoting Nicolas Tarducci, "Head of Solution
     Architecture for Startups EMEA at Amazon Web Services": "Pathway's work training BDH-CQ on
     Amazon SageMaker HyperPod points to a promising path toward deploying high-performing
     systems more cost-effectively at scale." **[PA/AE]**
  3. Business Wire, Dec 1, 2025: "Pathway to Deliver New Class of Adaptive and Continuously
     Learning AI Systems with AWS and NVIDIA Technologies" (URL seen in Pathway blog listing;
     body not retrieved). **[PA]**
- **Evidence category: partnership announcement — NOT independent validation** of any BDH
  performance or scaling claim. The same press release reports ARC-AGI-1 replication by Łukasz
  Kaiser ("replicated their ARC-AGI-1 results myself") and Richard Zhong (NYU) — but this
  replication claim itself appears only inside Pathway's own release, so classify as
  **author-reported claim of independent evaluation**, not [IE], until the replication report
  (linked from `pathway.com/research/introducing-bdh-cq/arc-agi-1`) is independently retrieved.

---

## 9. The "1B to 600B parameters" scaling claim (DataForge brief)

- **NOT FOUND IN PAPER.** arXiv:2509.26507 v1 reports scaling experiments at **10M-1B**
  (Empirical Finding 1; §4.2; Tables 4-5 list 25M-800M configurations). Nothing in the retrieved
  paper text mentions 600B or any run above ~1B.
- What the primary (company) source actually says — Pathway press release (Aug 11, 2026),
  verbatim: "Early experiments confirm Transformer-like scaling laws apply during pretraining at
  scales from 1B to 600B parameters, while preserving the latent reasoning capabilities specific
  to BDH-CQ." Context: this is about **BDH-CQ** (a 150M-parameter ARC-AGI reasoning model line),
  in a press release; no paper, loss curves, or artifacts for the 1B-600B runs were located.
  Category: **company-reported [AE], unreviewed; no independent or peer-reviewed support found.**
  If the DataForge brief attributes "1B to 600B" to the arXiv paper, that attribution is wrong.

---

## 10. Related Pathway claims encountered (for completeness, all company-reported)

- Sudoku Extreme 97.4% top-1, ~250k puzzles, no chain-of-thought
  (`pathway.com/research/beyond-transformers-sudoku-bench`, Mar 17, 2026; repo README). Internal
  implementation only; not in the paper; open repo "does not reproduce" it.
- BDH-CQ: 29.5% pass@2 on ARC-AGI-1 at $0.0007/task (`pathway.com/research/introducing-bdh-cq`).
- BABILong: 95% @ 32K, 82% @ 128K with a 134M BDH, "pending final contamination checks,
  independent validation, and leaderboard review" (pathway.com homepage).

---

## Fetch log (2026-09-05)

| URL / source | Method | Outcome |
|---|---|---|
| https://arxiv.org/pdf/2509.26507 | curl | FAILED — proxy CONNECT 403 (egress policy) |
| https://arxiv.org/abs/2509.26507 | curl | FAILED — proxy CONNECT 403 |
| https://arxiv.org/abs/2509.26507 | WebFetch | FAILED — EGRESS_BLOCKED arxiv.org |
| https://arxiv.org/html/2509.26507v1 | curl | FAILED — 000/CONNECT 403 |
| https://ar5iv.labs.arxiv.org/html/2509.26507 | curl | FAILED — 000 |
| https://export.arxiv.org/abs/2509.26507 | curl | FAILED — 000 |
| https://www.alphaxiv.org/abs/2509.26507 | curl | FAILED — 000 |
| https://huggingface.co/papers/2509.26507 | curl | FAILED — 000 |
| arXiv:2509.26507 metadata | Firecrawl research_inspect_paper | OK — title, authors, categories, dates, abstract |
| arXiv:2509.26507 full text (v1 HTML) | Firecrawl research_read_paper ×7 queries | OK — §§1-8, App. B/C/E excerpts incl. Eqs. 4-9, 12, 14, 16, Tables 1, 4-6, Figs. 3, 7, 11-16 |
| https://pathway.com/research/bdh-explainer/bdh-architecture-derivation | curl, WebFetch, Wayback | FAILED — all blocked; body absent from Firecrawl index → UNVERIFIED |
| https://pathway.com/research/bdh-explainer (series index) | Firecrawl search (index excerpt) | OK — chapter summaries, verbatim |
| https://pathway.com/research/bdh-explainer/brain-inspired-ai-architecture | Firecrawl search (index excerpt) | PARTIAL OK — §§1.4-1.6 excerpts; direct fetch blocked |
| https://pathway.com/research/the-equations-of-reasoning | Firecrawl search (index excerpt) | OK (extensive) — §§4, 5, 5.1, 5.2, Table 1 rendering, Conclusion; direct fetch blocked |
| https://github.com/pathwaycom/bdh | git clone (proxy) | OK — full working tree @ 2b0d7a4 (2026-05-15) |
| https://raw.githubusercontent.com/pathwaycom/bdh/main/README.md | curl | OK |
| https://api.github.com/repos/pathwaycom/bdh | curl + GitHub MCP | FAILED — repo not enabled for this session's GitHub credentials (clone used instead) |
| https://aws.amazon.com/aws-startups/learn/pathways-bdh-a-new-post-transformer-approach-to-enterprise-ai-on-aws/ | WebFetch | FAILED — EGRESS_BLOCKED aws.amazon.com; search snippet only |
| https://pathway.com/blog/pathway-150m-model-breaks-arc-agi-1-cost-efficiency-frontier | Firecrawl search (index excerpt) | OK (near-full press release text) — 600B sentence, HyperPod quote |
| https://finance.yahoo.com/technology/ai/articles/pathways-150m-parameter-model-breaks-113000925.html | WebFetch | FAILED — EGRESS_BLOCKED finance.yahoo.com |
| https://api.semanticscholar.org/graph/v1/paper/arXiv:2509.26507 | curl | FAILED — 000 (blocked) |
| https://web.archive.org (mirror attempt) | curl | FAILED — CONNECT 403 |
| Search for arXiv v2/v3 of 2509.26507 | Firecrawl search | No later version found; all citations reference v1 → later versions UNVERIFIED |
