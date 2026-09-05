# Evidence file: arXiv:2608.09888 — BDH-CQ

Verified: 2026-09-05. Verifier: Claude (research-verifier task, DataForge).
Source of full text: arXiv HTML v1 ("arXiv:2608.09888v1 [cs.NE] 10 Aug 2026"), retrieved via the
Firecrawl research index (arxiv.org itself is blocked by this environment's egress proxy; see Fetch log).
All quotes are verbatim from that v1 full text. Locators are section/equation/table numbers from the
paper's own numbering (the HTML source carries no PDF page numbers). Nothing below is from model memory.

---

## 1. Citation metadata

- **Title (exact):** BDH-CQ: In-Context Learning with Recurrent Latent Reasoning
- **arXiv ID:** 2608.09888 (v1 banner in retrieved HTML: `arXiv:2608.09888v1 [cs.NE] 10 Aug 2026`)
- **Authors (in order, with affiliations as printed):**
  1. Björn Engdahl — Pathway (pathway.com/research)
  2. Adrian Kosowski — Pathway
  3. Jan Chorowski — Pathway
  4. Zuzanna Stamirowska — Pathway
  5. Przemysław Uznański — Pathway
  6. Junlin Jiang — Pathway
  7. Rohan Phadke — Pathway
  8. Remigiusz Kinas — Bielik AI (bielik.ai)
  9. Richard Zhong — New York University
- **Dates:** created 2026-08-10; updated 2026-08-11 (Firecrawl canonical-metadata record). The retrieved
  full text is v1, dated 10 Aug 2026. Whether the 2026-08-11 update is a v2 revision could not be
  confirmed directly because arxiv.org is unreachable from this environment (see Fetch log).
- **Categories:** cs.NE, cs.AI, cs.LG, stat.ML (Firecrawl canonical-metadata record; primary cs.NE per v1 banner)
- **License:** "arXiv.org perpetual non-exclusive license" (v1 HTML header)
- **Model size:** "A 150M-parameter configuration" (Abstract); "we train a 150M-parameter model" (§4.2)
- **Companion pages:** Author affiliation links point to https://pathway.com/research. Web search surfaced
  a companion page URL `pathway.com/research/introducing-bdh-cq/arc-agi-1` and a companion repo
  `github.com/pathwaycom/arc-task-gen` ("Generates original ARC-AGI-1-style tasks distribution-matched to
  the public eval set"). Neither page could be opened from this environment (egress blocked), so their
  content is NOT verified — existence is attested only by search-result listings.
- **Evidence category:** formal (bibliographic record, cross-checked between Firecrawl metadata and the v1 HTML header).

---

## 2. Contextual memory from demonstrations (the memory/state update)

**Locator: §3.2 "In-context learning through recurrent memory", Equation (1).**

Setup (verbatim, §3.2): "Rather than compressing the demonstrations into a single task vector, BDH-CQ
processes their elements sequentially."

A task provides demonstrations D = {(x_t, y_t)}_{t=1}^{K} and a query input x*. The memory update is:

    S_t = U_θ(S_{t−1}, D_t)                                   (Eq. 1, §3.2)

Verbatim continuation (§3.2, after Eq. 1): "where D_t denotes the content of the t-th demonstration and
θ remains fixed."

Relation to attention / fast weights / linear attention (the passage the DataForge brief refers to),
**locator: §3.2, final paragraph**:

> "This recurrent contextual state plays a role analogous to the context-dependent associations
> constructed by attention, while avoiding a growing explicit key–value cache."

> "The interpretation is generally related to attention, fast-weight memory, and linear-attention views
> of contextual association" (cites Vaswani et al. 2017; Ba et al. 2016; Katharopoulos et al. 2020;
> Geva et al. 2021)

> "with linear attention being the conceptually simplest standalone realization of linear correction
> rules on S, capturing the special case S_t = S_{t−1} + U_θ(D_t)."

So the additive-per-demonstration accumulation S_t = S_{t−1} + U_θ(D_t) is presented as the **special
case** (the linear-attention realization) of the general update Eq. (1). The DataForge brief's wording is
**confirmed**.

**Symbol table (as defined by the paper):**

| Symbol | Meaning (paper's definition) | Dimensions |
|---|---|---|
| D = {(x_t, y_t)}_{t=1}^{K} | task demonstrations (input/output pairs) | ARC grids; sizes task-dependent |
| K | number of demonstrations in the task | scalar |
| D_t | "the content of the t-th demonstration" (§3.2) | not stated |
| S_t | recurrent memory / "recurrent contextual state" after ingesting demonstration t (§3.2) | **not disclosed** |
| U_θ | parameterized memory-update operator (Eq. 1) | **not disclosed** |
| θ | model parameters; "θ remains fixed" during ingestion (§3.2) | 150M total (§4.2) |
| x* | query input (§3.2) | ARC grid |

**IMPORTANT caveat, verbatim (§3.3, end):** "Dimensions, exact update rules, and implementation details
remain proprietary." — The paper deliberately does NOT give dimensions for S, H, or the concrete form of
U_θ, E_θ, F_θ, G_θ. Any dimension attached to these symbols elsewhere would be fabricated.

**Evidence category:** formal (equations as stated in the paper), but *interface-level only*: the concrete
update rule is explicitly withheld as proprietary, so Eq. (1) is a formal abstraction of an undisclosed
mechanism, not a reproducible specification.

---

## 3. "Recurrent latent reasoning" — operational meaning

**Locator: §3.3 "Recurrent latent reasoning", Equations (2)–(4).**

Verbatim (§3.3): "After the demonstrations and query have been ingested, BDH-CQ performs iterative
computation in a structured latent workspace H_r." — "This happens after the ingestion of the K
demonstrations into memory."

    H_0     = E_θ(x*, S_K)                                    (Eq. 2)
    H_{r+1} = F_θ(H_r, S_K),   r = 0, …, R−1                  (Eq. 3)
    ŷ       = G_θ(H_R)                                        (Eq. 4)

What is iterated: the latent workspace H_r, updated R times by F_θ, conditioned on the frozen post-ingestion
memory S_K; only the final H_R is decoded to the answer ŷ. Role separation, verbatim (§3.3): "S_t changes
as evidence is encountered and supports in-context learning. H_r carries the ongoing computation used to
answer the current query."

No verbalized intermediate steps, verbatim (Abstract): "the model then solves a query through iterative
computation in a high-dimensional latent space, without verbalizing its intermediate reasoning."

**No parameter updates at inference — explicit statement, verbatim (§1, Introduction):**

> "Neither task identifiers nor evaluation-task demonstration pairs participate in training, and no
> parameters are updated at inference time."

Reinforced formally by "θ remains fixed" (§3.2, after Eq. 1). The paper contrasts this with HRM/TRM ARC
pipelines (§8): "task information is written into recurrent memory through context, and latent computation
applies it without puzzle-specific optimization."

**Evidence category:** the iteration scheme (Eqs. 2–4) is formal-but-interface-level (details proprietary);
"no parameter updates at inference" is an author-reported design property (not independently verifiable
from the paper, since weights/implementation are closed; the black-box audit in §5 had "no access to model
weights" and thus cannot verify this either).

---

## 4. Training setup vs. evaluation tasks

**Brief's claim: "no evaluation-task demonstrations in training." — Verified as an explicit author claim
for ARC-AGI-1; with a ConceptARC caveat (below).**

- Explicit statement, verbatim (§1): "Neither task identifiers nor evaluation-task demonstration pairs
  participate in training, and no parameters are updated at inference time."
- Training data (§4.2, verbatim): "The dataset combines privately curated examples with publicly available
  data from the ARC-AGI-1 **training** set, RE-ARC, ConceptARC, ARC-Heavy, and ARC-GEN100K." Plus:
  "We apply additional augmentations to increase the variety of the training data."
- Objective (§4.1, verbatim): "During training, the model predicts outputs after preceding examples have
  been incorporated into recurrent context." And: "We report the task interface and data provenance; the
  complete internal training recipe remains proprietary."
- Task formalization: Eq. (5), §4.1: T_i = ({(x_{i,j}, y_{i,j})}_{j=1}^{K_i}, {(x^test_{i,q}, y^test_{i,q})}_{q=1}^{Q_i}), Q_i ≥ 1.
- Controlled behavioral tasks were built "after freezing the model" (§6.2: "We generated fresh ARC-like
  tasks after freezing the model."), i.e., post-freeze generators cannot have leaked into training.

**Verifier caveat (unresolved in the paper):** §4.2 lists **ConceptARC** in the training mixture, yet §6.1
evaluates on ConceptARC (Table 1/2). The paper itself flags this, verbatim (§6.5): the replication
"does not make ConceptARC a fresh benchmark, rule out exposure through training or checkpoint selection,
or isolate the two interventions factorially." So "no evaluation-task demonstrations in training" is
clean as stated for the ARC-AGI-1 public evaluation split, but ConceptARC results should not be read as
contamination-free; the paper does not state that evaluated ConceptARC tasks were excluded from training.

**Evidence category:** author-reported; not externally auditable because "the complete internal training
recipe remains proprietary" (§4.1).

---

## 5. ARC-AGI(-1) results — exact numbers

Model: 150M parameters (Abstract, §4.2). Benchmark: 400-task public ARC-AGI-1 evaluation split, two-attempt
leaderboard convention pass@2 (§5).

**Headline (Abstract; §5; §9):** 29.5% pass@2 at a computed $0.0007 per task (Abstract wording:
"$0.0007 per task—less than one-tenth of a cent"; §5 and §9 wording: "$0.00070 per task").
Cost derivation, verbatim (§5): "the 150M-parameter system reaches 29.5% pass@2 in approximately
0.85 H200 GPU-seconds per task. At $3 per H200-hour this gives a computed cost of $0.00070 per task,
less than one-tenth of a cent."

**Table 1 (§6, "Headline results on the public ARC-AGI-1 evaluation and on ConceptARC") — copied exactly:**

| Set / condition | Unit | N | pass@1 | pass@2 [95% Wilson] |
|---|---|---|---|---|
| ARC-AGI-1 public | tasks | 400 | 97 (24.25%) | 118 (29.50%) [25.24, 34.15] |
|  | test pairs | 419 | 108 (25.78%) | 130 (31.03%) |
| ConceptARC, semantic IDs | tasks | 160 | 73 (45.63%) | 95 (59.38%) [51.63, 66.68] |
|  | test pairs | 480 | 332 (69.17%) | 374 (77.92%) |
| ConceptARC, opaque IDs | tasks | 160 | 72 (45.00%) | 96 (60.00%) [52.26, 67.27] |
|  | test pairs | 480 | 334 (69.58%) | 374 (77.92%) |

**Effort settings — LOW / MEDIUM / HIGH (§7, Table 5 "Comparing pass@2 and cost across reasoning efforts
LOW, MEDIUM, HIGH"; Figure 7) — copied exactly:**

| Effort | Pass@2 | Cost reduction |
|---|---|---|
| HIGH | 29.5% | 0% |
| MEDIUM | 27% | 11% |
| LOW | 21% | 22% |

Mechanism (§7, verbatim): "we train the model changing the levels of latent reasoning during training…
For inference, we can choose the level of reasoning to apply." (The paper does not disclose what iteration
counts R the levels correspond to.)

**Separate MIN vs STANDARD effort comparison (§6.6) — copied exactly:** "the MIN effort setting cost
one third of standard ($0.00088399 versus $0.00265246 per task) and scored 111/400 rather than 118/400
pass@2, a difference of −1.75 percentage points." Paired split: 105 both, 13 standard-only, 6 min-only,
276 neither; "two-sided exact McNemar p=0.167"; the paper calls this comparison "statistically unresolved."
Determinism (§6.6): repeated identical requests were byte-identical at both effort tiers (all 419 test inputs).

**Verifier note (internal tension, recorded not resolved):** §5 computes $0.00070/task at the default
29.5% operating point, while §6.6 quotes standard effort at $0.00265246/task for the same 118/400 score.
The paper does not reconcile these two cost figures.

**Baseline comparisons made by the paper itself:**
- §5, verbatim: "Using ARC Prize's reported costs as of July 2026, BDH-CQ is approximately 57x cheaper
  than GPT 5.6 Luna (Low) which scores 34.2% at $0.040." After OpenAI's "80% public API price reduction
  of GPT 5.6 Luna on July 30, 2026," it "is approximately 11x cheaper than GPT 5.6 Luna (Low)."
- §5/Figure 2: leaderboard points collected from the official ARC Prize leaderboard on August 4, 2026;
  "no plotted system attains at least this accuracy at equal or lower reported cost" (Pareto claim).
- §8, verbatim: "ARC Prize reports costs of $1.48 per task for HRM and $1.76 per task for TRM."
- Appendix Table 6 (STANDARD effort): Public ARC-AGI-1 400 tasks, 118 solved, 29.5%; calibrated generated
  400 tasks, 149, 37.2%; mechanic-stratified generated 1,131 tasks, 337, 29.8%.

**Independent evaluation (§5 "Independent evaluation" paragraph), verbatim:** "An independent black-box
audit conducted by co-authors from Bielik and New York University reproduced the deployed system's 29.5%
pass@2 score" — "under a documented protocol without access to model weights" (reports: Kinas 2026,
protocol BDH-ARC-BBX-001; Zhong 2026).

**Evidence categories:** all numbers are author-reported empirical. The 29.5% pass@2 figure has a
black-box reproduction, but the auditors (Kinas, Zhong) are listed co-authors of this same paper, so it is
best classed as semi-independent (author-affiliated audit), not fully independently evaluated. The Pareto
/ "57x–11x cheaper" comparisons rest on third-party (ARC Prize) cost reporting combined with the authors'
own computed cost.

---

## 6. Relationship to BDH (base architecture)

**Locator: §3.1 "BDH provenance".**

- BDH = "the Dragon Hatchling", "a post-Transformer sequence-model architecture built around
  high-dimensional positive activations, low-rank communication, and a recurrent associative state"
  (§3.1; Kosowski et al. 2025, arXiv:2509.26507). GPU formulation: "BDH layers combining ReLU-low-rank
  transformations with linear attention in a large neuron or feature space" (§3.1).
- What BDH-CQ adds, verbatim (§3.1): "BDH-CQ extends this line into a new reasoning system that combines
  a structured latent workspace and recurrent computation over model depth with an interface for learning
  visual transformations from demonstrations."
- Naming convention, verbatim (§3.1): "We use 'BDH' for the architectural family and 'BDH-CQ' for the
  system introduced here."
- System scope, verbatim (§3.1): "The complete evaluated system includes input transformations, candidate
  construction, ranking, and the inference pipeline." (i.e., BDH-CQ is evaluated as a full pipeline, not a
  bare model.)
- Antecedent: Pathway's BDH-based Sudoku constraint-satisfaction system (§3.1; Pathway Research 2025,
  pathway.com/research/beyond-transformers-sudoku-bench).
- Scaling note (§9.2, verbatim): "Early experiments confirm Transformer-like scaling laws apply during
  pretraining at scales from 1B to 600B parameters," with tensor sharding "inherited from the BDH
  architecture."

**Evidence category:** author-reported (architecture provenance formal at interface level; the §9.2
1B–600B scaling claim is author-reported with no numbers, tables, or details given).

---

## 7. Limitations stated in the paper itself

1. **Proprietary core** (§3.3): "Dimensions, exact update rules, and implementation details remain
   proprietary." (§4.1): "the complete internal training recipe remains proprietary."
2. **Within-task inconsistency** (§6.4): 52/160 ConceptARC tasks had one or two of three test pairs correct
   but failed as tasks; "the observed transformation is not applied consistently across inputs." The
   18.5-point gap: pair pass@2 77.92% vs strict task 59.38%.
3. **ConceptARC replication scope** (§6.5): the opaque-ID replication "does not make ConceptARC a fresh
   benchmark, rule out exposure through training or checkpoint selection, or isolate the two interventions
   factorially."
4. **pass@2 interpretation** (§6.6): all 75 single-candidate records were correct at rank one, so "nominal
   pass@2 should not be interpreted as the result of two independently sampled attempts for every input."
5. **Capability boundaries** (§6.2–6.3, Tables 3–4, Figure 5): ordering collapses at length 8 (1/24 pass@2;
   only 3/24 outputs have correct dimensions); nesting drops at depth 5 (29/36); reflection composed with
   relocation 47/72; color swap composed with relocation 0/72; color swap atomically only 26/72 pooled.
6. **Small samples** (§6.1): ten tasks per ConceptARC family — "these counts are a profile rather than a
   reliable ranking" (Wilson intervals for 9/10 and 2/10 overlap broadly).
7. **Generated-set confounds** (Appendix A.2–A.4): generator authored by GPT-5.6 ("each rate also reflects
   how that generator instantiates the requested operation"); at least one generated task with
   contradictory test output; LLM mechanic labels agree 82.9%; each ladder condition only 40 tasks from one
   family — results "do not yet establish that these differences generalize across visual operations."
8. **Opacity of failures** (A.4): "a correct rule applied incompletely is observationally indistinguishable
   from a narrower rule applied completely" (the evaluator returns grids, not traces).
9. **Structural weak spots quantified** (Table 8): conditional rule selection 100.0% → 56.7% (−43.3);
   parameter absent from demonstrations 30.0% → 0.0%; panel union two→three panels 65.0% → 2.5%; support
   chain shortest→eight objects 80.0% → 27.5%. Unseen parameter values: 0/120 when the value is absent
   from demonstrations (A.3).

**Evidence category:** author-reported (self-identified limitations).

---

## 8. Evidence-category summary per claim

| Claim | Category |
|---|---|
| Citation metadata (title/authors/dates/categories) | formal (bibliographic; cross-checked two sources) |
| Memory update Eq. (1) + additive special case S_t = S_{t−1} + U_θ(D_t) | formal at interface level; internals proprietary |
| Attention / fast-weight / linear-attention relation (§3.2) | formal-interpretive, author-asserted analogy |
| Latent reasoning loop Eqs. (2)–(4); iterate H_r, R steps on frozen S_K | formal at interface level; internals proprietary |
| "No parameters updated at inference"; "θ remains fixed" | author-reported (closed weights; not externally verifiable) |
| Training mixture; no evaluation-task demos in training | author-reported; proprietary recipe; ConceptARC caveat (§4.2 vs §6.1, §6.5) |
| ARC-AGI-1 29.50% pass@2 (118/400), 24.25% pass@1 (97/400) | author-reported empirical; black-box reproduction by co-author auditors (semi-independent) |
| $0.00070/task cost; Pareto/state-of-the-art cost efficiency | author-reported computed metric (0.85 H200 GPU-s × $3/hr) + third-party leaderboard costs |
| Effort scaling LOW 21% / MEDIUM 27% / HIGH 29.5% | author-reported empirical |
| MIN vs STANDARD: 111/400 vs 118/400; $0.00088399 vs $0.00265246 | author-reported empirical; paper itself calls it statistically unresolved |
| BDH provenance and what BDH-CQ adds | author-reported |
| 1B–600B pretraining scaling-law claim (§9.2) | author-reported, no supporting data shown |

---

## 9. Fetch log (every URL/tool attempted, in order, 2026-09-05)

| # | Target | Method | Outcome |
|---|---|---|---|
| 1 | https://arxiv.org/abs/2608.09888 | curl (via agent proxy) | FAILED — CONNECT tunnel 403, egress proxy denied arxiv.org:443 (curl exit 56) |
| 2 | https://arxiv.org/pdf/2608.09888 | curl (via agent proxy) | FAILED — CONNECT tunnel 403, same denial; PDF never obtained, so no pdftotext pass |
| 3 | https://arxiv.org/abs/2608.09888 | WebFetch | FAILED — EGRESS_BLOCKED (arxiv.org) |
| 4 | arXiv:2608.09888 | Firecrawl research_inspect_paper | SUCCESS — canonical metadata (title, 9 authors, categories cs.NE/cs.AI/cs.LG/stat.ML, created 2026-08-10, updated 2026-08-11, abstract) |
| 5 | query "BDH-CQ in-context learning recurrent latent reasoning Pathway" | Firecrawl research_search_papers | SUCCESS — confirmed arxiv:2608.09888 and arXiv cs.NE listing pages |
| 6 | https://export.arxiv.org/abs/2608.09888 | WebFetch | FAILED — EGRESS_BLOCKED (export.arxiv.org) |
| 7 | arxiv:2608.09888 (memory-update question, k=15) | Firecrawl research_read_paper | SUCCESS — full-text passages of arXiv HTML v1 incl. §§1–5, 3.2 Eq. 1, 3.3 Eqs. 2–4, §4, §6–§10, Appendix A, references |
| 8 | arxiv:2608.09888 (ARC results/limitations question, k=12) | Firecrawl research_read_paper | SUCCESS — §5 cost details, Table 1, §6.4–6.6, §7 Table 5, Appendix Tables 6–9 |
| 9 | https://pathway.com/research | WebFetch | FAILED — EGRESS_BLOCKED (pathway.com) |
| 10 | arxiv:2608.09888 (effort levels/state description question, k=8) | Firecrawl research_read_paper | SUCCESS — confirmed §3.1–3.3 and §7 passages; no additional S_t detail exists in the paper (proprietary) |
| 11 | Web search "Pathway BDH-CQ research page …" | WebSearch | SUCCESS — surfaced pathway.com/research/introducing-bdh-cq/arc-agi-1, github.com/pathwaycom/arc-task-gen, arxiv.org/abs/2608.09888 + /html/2608.09888v1, alphaxiv.org/abs/2608.09888, huggingface.co/papers/2608.09888 (listings only; pages not opened) |
| 12 | https://huggingface.co/papers/2608.09888 | WebFetch | FAILED — EGRESS_BLOCKED (huggingface.co) |
| 13 | https://www.alphaxiv.org/abs/2608.09888 | WebFetch | FAILED — EGRESS_BLOCKED (alphaxiv.org) |

Net result: full v1 text obtained through the Firecrawl paper index (items 4, 7, 8, 10); direct arXiv,
Pathway, and mirror access all blocked at the network layer. v1/v2 suffix retries were moot: the block is
domain-level, not ID-level, and the v1 full text was recovered through the index.
