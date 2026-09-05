import { useState } from 'react';
import { Badge, Eq } from './primitives';

/**
 * Lesson step 5: the BDH module. Source of truth: "The Dragon Hatchling"
 * (arXiv:2509.26507v1) with exact equation references; BDH-CQ from its
 * technical report (arXiv:2608.09888v1). All equations here are
 * source-derived illustrations rendered from the papers' formulas — this
 * page runs the 2×2 toy, never a BDH model.
 */

const STATE_QUESTION = [
  {
    id: 'sigma',
    label: 'The synaptic state ρ (equivalently σ) — and the activations x, y',
    correct: true,
    explain:
      'Right. During inference the fast state ρ accumulates a rank-1 write per token while the trained matrices E, Dx, Dy stay frozen. That is the same split as the toy: M changed, no trained weights exist to change.',
  },
  {
    id: 'encoder',
    label: 'The trained matrices E, Dx, Dy',
    correct: false,
    explain:
      'No — those are slow weights, fixed after training. Only the state ρ and the activations change as the model reads. (In the toy there were no trained weights at all.)',
  },
  {
    id: 'both',
    label: 'Both the state and the trained matrices',
    correct: false,
    explain:
      'Only the state. If trained parameters changed during inference, that would be online learning of weights — a different mechanism the BDH paper explicitly separates from its fast synaptic memory.',
  },
] as const;

export default function BdhModule() {
  const [picked, setPicked] = useState<string | null>(null);
  const pickedChoice = STATE_QUESTION.find((c) => c.id === picked);

  return (
    <div className="panel">
      <p className="panel-title">
        The same write and read inside BDH-GPU <Badge kind="source" />
      </p>

      <p>
        <strong>Which system, precisely:</strong> the Dragon Hatchling paper gives two coupled
        formulations. <em>Graph BDH</em> describes neurons and synapses with local rules —
        attention becomes Hebbian synaptic memory on a graph (its state update is Eq.&nbsp;6 of the
        paper). <em>BDH-GPU</em> is the tensor-friendly formulation actually trained on hardware
        (§3.2). It is <em>not</em> a Mamba-style state-space model: the paper positions it as
        linear attention operating in one very high-dimensional, non-negative, sparsely active
        neuronal space. The concept from our toy shows up in BDH-GPU's layer state update,
        Eq.&nbsp;(8) of arXiv:2509.26507:
      </p>

      <Eq
        block
        tex="\rho_{t,\ell} \;:=\; \big(\rho_{t-1,\ell} \;+\; \mathrm{LN}(E\, y_{t,\ell-1})\, x_{t,\ell}^{\top}\big)\, U"
        label="rho at t equals open paren rho at t minus one plus layer norm of E y, times x transpose, close paren, times U"
      />
      <p style={{ textAlign: 'center', fontFamily: 'var(--sans)', fontSize: '0.9rem', color: 'var(--ink-soft)' }}>
        the write — compare the toy's <Eq tex="M_t = \lambda M_{t-1} + v_t k_t^{\top}" />
      </p>
      <Eq
        block
        tex="y_{t,\ell} \;:=\; \big(D_y\, \mathrm{LN}(\rho_{t-1,\ell}\, x_{t,\ell})\big)^{+} \odot\, x_{t,\ell}"
        label="y at t equals ReLU of D y layer norm of rho times x, elementwise times x"
      />
      <p style={{ textAlign: 'center', fontFamily: 'var(--sans)', fontSize: '0.9rem', color: 'var(--ink-soft)' }}>
        the read — inside it sits the toy's <Eq tex="M q" /> (here <Eq tex="\rho\,x" />), wrapped
        in machinery the toy omits
      </p>

      <h3>Every symbol, and whether it changes at inference</h3>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">Symbol</th>
              <th scope="col">Space (paper §3.2, §6.1)</th>
              <th scope="col">Role — in the toy's vocabulary</th>
              <th scope="col">Changes during inference?</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <Eq tex="x_{t,\ell}" />
              </td>
              <td>
                <Eq tex="(\mathbb{R}^{+})^{n}" />, n up to ~10⁶, ~5% active
              </td>
              <td>
                the <strong>key and the query at once</strong> — BDH uses the same sparse
                activation vector for both, where the toy had separate k and q
              </td>
              <td>yes — activation</td>
            </tr>
            <tr>
              <td>
                <Eq tex="y_{t,\ell}" />
              </td>
              <td>
                <Eq tex="(\mathbb{R}^{+})^{n}" />
              </td>
              <td>output activation; its low-rank projection makes the next value</td>
              <td>yes — activation</td>
            </tr>
            <tr>
              <td>
                <Eq tex="\mathrm{LN}(E\,y_{t,\ell-1})" />
              </td>
              <td>
                <Eq tex="\mathbb{R}^{d}" />, d = 256 in the paper's runs
              </td>
              <td>
                the <strong>value</strong> <Eq tex="v_t" /> — computed from activity, not looked up
              </td>
              <td>yes — derived from activations</td>
            </tr>
            <tr>
              <td>
                <Eq tex="\rho_{t,\ell}" />
              </td>
              <td>
                d×n as composed in Eq. (8) — see note below
              </td>
              <td>
                the <strong>memory matrix</strong> <Eq tex="M" /> — fast “synaptic” state, zeroed
                at sequence start, written once per token per layer
              </td>
              <td>
                <strong>yes — this is the fast weight state</strong>
              </td>
            </tr>
            <tr>
              <td>
                <Eq tex="U" />
              </td>
              <td>linear map on the time axis</td>
              <td>
                the <strong>decay/rotation</strong> — the toy's λ generalized (“local rotation or
                damping… such as ALiBi or RoPE”, Def. 4)
              </td>
              <td>no — fixed convention</td>
            </tr>
            <tr>
              <td>
                <Eq tex="E,\ D_x,\ D_y" />
              </td>
              <td>
                <Eq tex="E \in \mathbb{R}^{d\times n}" />, <Eq tex="D_x, D_y \in \mathbb{R}^{n\times d}" /> (≈3nd params total)
              </td>
              <td>
                <strong>trained weights</strong> — encoder/decoders deciding how to write and read;
                the toy has no counterpart at all
              </td>
              <td>
                <strong>no — frozen after training</strong>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p className="note">
        <strong>Dimension check</strong> (do it yourself): the write{' '}
        <Eq tex="\mathrm{LN}(E y)\,x^{\top}" /> is (d×1)(1×n) = d×n, a rank-1 outer product exactly
        like the toy's <Eq tex="v k^{\top}" />; the read <Eq tex="\rho\, x" /> is (d×n)(n×1) = d,
        a matrix–vector product exactly like <Eq tex="Mq" />. Indexing is causal: the read at
        token t uses <Eq tex="\rho_{t-1}" /> — the state <em>before</em> this token's write, so no
        token reads its own write. One honesty note from our source check: the paper's Fig.&nbsp;3
        caption declares <Eq tex="\rho \in \mathbb{R}^{n \times d}" /> while its equations compose
        ρ as d×n; we follow the composition that makes Eq.&nbsp;(8)'s algebra type-check, and
        record the discrepancy in docs/RESEARCH.md rather than silently mixing conventions.
      </p>

      <h3>What the toy leaves out — deliberately</h3>
      <ul>
        <li>
          <strong>Non-negativity and sparsity:</strong> BDH activations live in{' '}
          <Eq tex="(\mathbb{R}^{+})^{n}" /> with ReLU thresholding; ~5% of neurons are active
          (Empirical Finding 1, §4.1 — author-reported). The toy's vectors go negative and dense.
        </li>
        <li>
          <strong>Trained encoder/decoders</strong> E, D<sub>x</sub>, D<sub>y</sub> that learn{' '}
          <em>what</em> to write; the toy hand-picks its vectors.
        </li>
        <li>
          <strong>Layer structure and gating:</strong> the read is thresholded and gated{' '}
          (<Eq tex="\odot\, x" />), and layers stack with a shared state pattern; the toy is one
          bare matrix.
        </li>
        <li>
          <strong>The graph view:</strong> per-synapse local rules, excitatory/inhibitory circuits
          (Eq. 6, Table 1) — with reported (author-evaluated) consequences: monosemantic synapses
          (§6.3) and heavy-tailed connectivity (Fig. 11).
        </li>
        <li>
          <strong>Scale:</strong> BDH-GPU runs at n up to ~10⁶ with GPT-2-class language
          performance at 10M–1B parameters (Fig. 7, Tables 4–5 — author-reported, Europarl).
          The toy is 2×2 on purpose: every scalar visible.
        </li>
      </ul>
      <p className="note warn">
        This page's simulation is an <strong>original toy computation</strong> of the shared
        mechanism. It is not an official BDH model, does not use BDH code or checkpoints, and
        demonstrates nothing about trained monosemantic synapses. Adding linear attention to a
        Transformer does not recreate BDH — the paper derives the architecture from local
        neuron–synapse dynamics, of which the fast-weight write is one ingredient.
      </p>

      <h3>Check yourself: during BDH inference, which quantity changes?</h3>
      <div role="group" aria-label="BDH state question">
        {STATE_QUESTION.map((c) => (
          <button
            key={c.id}
            type="button"
            className="quiz-option"
            aria-pressed={picked === c.id}
            onClick={() => setPicked(c.id)}
          >
            {c.label}
          </button>
        ))}
        {pickedChoice && (
          <div
            className={`quiz-feedback ${pickedChoice.correct ? 'correct' : 'incorrect'}`}
            role="status"
          >
            <strong>{pickedChoice.correct ? 'Correct.' : 'Not quite.'}</strong>{' '}
            {pickedChoice.explain}
          </div>
        )}
      </div>

      <h3>
        And BDH-CQ — the same split, one level up <Badge kind="source" />
      </h3>
      <p>
        BDH-CQ (arXiv:2608.09888, 2026) applies this vocabulary to learning{' '}
        <em>from demonstrations</em>. Reading demonstrations D₁…D_K builds a contextual memory by a
        recurrent update (its Eq. 1, §3.2):
      </p>
      <Eq
        block
        tex="S_t = U_\theta(S_{t-1}, D_t)"
        label="S at t equals U sub theta of S at t minus 1 and D at t"
      />
      <p>
        with θ — the trained parameters — held fixed. The report explicitly relates this to
        “attention, fast-weight memory, and linear-attention views of contextual association,”
        with linear attention as the special case where the state accumulates additively per
        demonstration, <Eq tex="S_t = S_{t-1} + U_\theta(D_t)" /> — precisely our toy's write,
        one demonstration per stamp. Answering then iterates a latent workspace against the frozen
        memory (Eqs. 2–4): <Eq tex="H_{r+1} = F_\theta(H_r, S_K)" /> — recurrent latent reasoning,
        distinct from the memory write. The report states plainly: “Neither task identifiers nor
        evaluation-task demonstration pairs participate in training, and no parameters are updated
        at inference time” (§1). Adaptation lives entirely in state — the toy's lesson, load-bearing.
      </p>
      <p className="note warn">
        Evidence discipline: BDH-CQ reports 118/400 = 29.50% pass@2 on ARC-AGI-1 at ≈0.85 H200
        GPU-seconds (≈$0.0007) per task, with accuracy scaling across LOW/MEDIUM/HIGH latent-effort
        settings (21% / 27% / 29.5%; Tables 1 and 5) — <strong>author-reported</strong>, audited
        black-box by co-authors, and the report itself notes its update rules and dimensions are
        proprietary. Our toy demonstrates the memory <em>mechanism family</em>; it reproduces
        nothing about ARC or the full reasoning system.
      </p>
    </div>
  );
}
