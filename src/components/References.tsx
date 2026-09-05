/**
 * Primary sources. Bracket numbers match inline citations throughout the
 * lesson. Full claim-to-source ledger with exact locators: docs/RESEARCH.md.
 */
export default function References() {
  return (
    <section aria-labelledby="refs-h">
      <h2 id="refs-h">References</h2>
      <p style={{ fontSize: '0.95rem' }}>
        Primary papers (2022–2026 requirement met by [1], [2], [4], [5]); [3] is foundational
        background. Every technical claim on this page carries a bracket citation; exact
        section/equation locators and evidence categories are in{' '}
        <code>docs/RESEARCH.md</code> in the repository.
      </p>
      <ol className="refs">
        <li>
          [1] S. Yang, B. Wang, Y. Zhang, Y. Shen, Y. Kim.{' '}
          <em>Parallelizing Linear Transformers with the Delta Rule over Sequence Length.</em>{' '}
          NeurIPS 2024. <a href="https://arxiv.org/abs/2406.06484">arXiv:2406.06484</a>
        </li>
        <li>
          [2] S. Yang, J. Kautz, A. Hatamizadeh.{' '}
          <em>Gated Delta Networks: Improving Mamba2 with Delta Rule.</em> ICLR 2025.{' '}
          <a href="https://arxiv.org/abs/2412.06464">arXiv:2412.06464</a>
        </li>
        <li>
          [3] I. Schlag, K. Irie, J. Schmidhuber.{' '}
          <em>Linear Transformers Are Secretly Fast Weight Programmers.</em> ICML 2021.{' '}
          <a href="https://arxiv.org/abs/2102.11174">arXiv:2102.11174</a> (background — predates
          the 2022–2026 window)
        </li>
        <li>
          [4] A. Kosowski, P. Uznański, J. Chorowski, Z. Stamirowska, M. Bartoszkiewicz.{' '}
          <em>The Dragon Hatchling: The Missing Link between the Transformer and Models of the
          Brain.</em> 2025. <a href="https://arxiv.org/abs/2509.26507">arXiv:2509.26507</a>
        </li>
        <li>
          [5] B. Engdahl, A. Kosowski, J. Chorowski, et&nbsp;al.{' '}
          <em>BDH-CQ: In-Context Learning with Recurrent Latent Reasoning.</em> 2026.{' '}
          <a href="https://arxiv.org/abs/2608.09888">arXiv:2608.09888</a>
        </li>
      </ol>
      <h3>Official BDH resources</h3>
      <ul className="refs">
        <li>
          Official (toy) BDH implementation, MIT license:{' '}
          <a href="https://github.com/pathwaycom/bdh">github.com/pathwaycom/bdh</a> — not used by
          this page's simulation; read to cross-check conventions.
        </li>
        <li>
          Pathway,{' '}
          <a href="https://pathway.com/research/the-equations-of-reasoning">
            The Equations of Reasoning
          </a>{' '}
          and{' '}
          <a href="https://pathway.com/research/bdh-explainer/brain-inspired-ai-architecture">
            Why BDH uses a brain-inspired architecture
          </a>
          .
        </li>
        <li>
          Pathway,{' '}
          <a href="https://pathway.com/research/bdh-explainer/bdh-architecture-derivation">
            From attention to synapses: deriving BDH
          </a>{' '}
          — listed for further reading; we could not retrieve its body from our build environment,
          so nothing on this page relies on it (logged in docs/RESEARCH.md).
        </li>
      </ul>
    </section>
  );
}
