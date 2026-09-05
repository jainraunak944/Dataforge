import { Badge, Eq } from './primitives';

/**
 * Lesson step: why this matters now. One compact comparison of update rules
 * across architecture families, every number author-reported from the cited
 * primary paper (locators in docs/RESEARCH.md and the references below).
 * No second live simulator — the toy stays the only substrate.
 */
export default function Comparison() {
  return (
    <div className="panel">
      <p className="panel-title">
        The same design pressure, four responses <Badge kind="reported" />
      </p>
      <p>
        The interference you just produced is not a toy artifact — it is the reason a family of
        2024–2026 architectures exists. When Schlag et&nbsp;al. trained a purely additive
        linear-attention model on WikiText-103 with <em>unlimited</em> context (fast-weight memory
        carried across segments), perplexity broke down to worse than 260, while the same model
        with an interference-correcting <em>delta rule</em> reached 29.4 — both ≈90M parameters
        [3, Table&nbsp;4]. Storing more associations than the key dimension supports{' '}
        <em>“will result in a retrieval error”</em> [3, §4.1]. That is our ρ&nbsp;&gt;&nbsp;0 lesson
        at scale.
      </p>

      <div className="table-scroll">
        <table>
          <caption className="sr-only">
            Comparison of memory update rules across architecture families
          </caption>
          <thead>
            <tr>
              <th scope="col">System / family</th>
              <th scope="col">Update per token or demo</th>
              <th scope="col">State growth</th>
              <th scope="col">Strength</th>
              <th scope="col">Limitation</th>
              <th scope="col">Evidence maturity</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <strong>Additive fast weights</strong> (this toy; linear attention)
              </td>
              <td>
                <Eq tex="S_t = S_{t-1} + v_t k_t^{\top}" />
              </td>
              <td>constant (d_v×d_k)</td>
              <td>O(1) state; write and read are cheap; exactly analyzable</td>
              <td>interference grows with key overlap and write count [3, §4.1]</td>
              <td>formal analysis + our live toy; long-studied</td>
            </tr>
            <tr>
              <td>
                <strong>DeltaNet</strong> (2024) [1]
              </td>
              <td>
                <Eq tex="S_t = S_{t-1} - \beta_t (S_{t-1} k_t - v_t) k_t^{\top}" />
              </td>
              <td>constant</td>
              <td>
                overwrites the old value under a reused key (one gradient step on recall error);
                1.3B/100B-token run beats Mamba and GLA on avg zero-shot (51.6 vs 50.0 / 51.0)
                [1, Table&nbsp;1]
              </td>
              <td>no decay → weaker length generalization; retrieval gap to attention remains</td>
              <td>author-reported benchmarks, open code</td>
            </tr>
            <tr>
              <td>
                <strong>Gated DeltaNet</strong> (2024) [2]
              </td>
              <td>
                <Eq tex="S_t = S_{t-1}\big(\alpha_t (I - \beta_t k_t k_t^{\top})\big) + \beta_t v_t k_t^{\top}" />
              </td>
              <td>constant</td>
              <td>
                adds fast erasure: on S-NIAH-2 @4K it scores 92.2 vs DeltaNet 18.6, Mamba2 56.2
                [2, Table&nbsp;2, 1.3B]
              </td>
              <td>
                decay costs retention (S-NIAH-1 @8K: 91.8 vs pure DeltaNet 98.8); “fixed state size
                makes it hard for retrieval tasks” [2, §3.4]
              </td>
              <td>author-reported benchmarks, open code</td>
            </tr>
            <tr>
              <td>
                <strong>BDH / BDH-GPU</strong> (2025) [4]
              </td>
              <td>
                Hebbian synaptic write into per-synapse state; linear-attention form in a very
                high-dimensional, sparsely active neuronal space (details in the BDH section above)
              </td>
              <td>constant per synapse set</td>
              <td>
                memory and reasoning share one substrate; interpretable sparse activations;
                GPT-2-class language performance at 10M–1B scale [4]
              </td>
              <td>
                young architecture; results are the developer’s own; large-scale evidence still
                accumulating
              </td>
              <td>author-reported; open toy code</td>
            </tr>
            <tr>
              <td>
                <strong>BDH-CQ</strong> (2026) [5]
              </td>
              <td>
                per-demonstration state update <Eq tex="S_t = U_\theta(S_{t-1}, D_t)" /> (additive
                accumulation as its linear-attention special case), θ frozen at inference
              </td>
              <td>constant</td>
              <td>
                ARC-AGI-1: 118/400 (29.50%) pass@2 at ≈$0.0007 of H200 time per task
                [5, Table&nbsp;1, §5]
              </td>
              <td>
                below the strongest LLMs on raw accuracy (paper cites GPT&nbsp;5.6 Luna Low at
                34.2%); update-rule internals proprietary
              </td>
              <td>author-reported; audit by co-authors, not fully independent</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p className="note warn">
        Every number above is <strong>author-reported</strong> from the cited paper's own
        evaluation setting (model sizes, data and hardware differ across rows — this table is not a
        controlled head-to-head). None of these results has, to our knowledge, a fully independent
        external reproduction; BDH-CQ's ARC score was audited black-box by two of its co-authors,
        which is not independent evaluation. Exact locators for every cell: docs/RESEARCH.md.
      </p>

      <h3>Our maturity assessment</h3>
      <p>
        On a 0–10 scale where 10 = boring, standardized infrastructure (softmax-attention
        Transformers) and 5 = adopted in production LLMs by multiple organizations, we place{' '}
        <strong>delta-rule linear attention at ≈6</strong> (variants ship in prominent
        architectures; trade-offs mapped by several groups) and{' '}
        <strong>BDH/BDH-CQ at ≈3</strong> (public paper, public toy code, striking
        developer-reported results, but no independent reproduction and key internals
        undisclosed). This scale is our assessment for this submission, not an official rating.
        The biggest open gaps: independent replications, and — for the field — how inference-time
        fast state should consolidate into durable weights.
      </p>
    </div>
  );
}
