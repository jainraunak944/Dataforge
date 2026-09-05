import { useMemo, useState } from 'react';
import { readHashSettings, useHashSync } from './hooks';
import { deriveSession, type SessionParams } from './memory/session';
import BdhModule from './components/BdhModule';
import BreakTheClaim from './components/BreakTheClaim';
import CollideCues from './components/CollideCues';
import Comparison from './components/Comparison';
import CrossTerm from './components/CrossTerm';
import ExplainItBack from './components/ExplainItBack';
import References from './components/References';
import StoreTwoThings from './components/StoreTwoThings';
import WhatChanged from './components/WhatChanged';
import { Badge, Eq } from './components/primitives';

/**
 * The lesson spine. Guided steps 1–4 run at λ = 1 with one write per pair —
 * the conditions of the claim. The sandbox (step 6) opens λ and repeats.
 * Settings are shareable via the URL hash.
 */

const DEFAULTS: SessionParams = { rho: 0.6, lambda: 1, repeats: 1 };

function Step({ n, title, children }: { n: number; title: string; children?: React.ReactNode }) {
  const id = `step-${n}`;
  return (
    <>
      <p className="stepkicker" aria-hidden="true">
        Step {n} of 7
      </p>
      <h2 id={id}>{title}</h2>
      {children}
    </>
  );
}

export default function App() {
  const initial = useMemo(() => readHashSettings(DEFAULTS), []);
  const [rho, setRho] = useState(initial.rho);
  const [sandbox, setSandbox] = useState<SessionParams>({
    rho: initial.rho,
    lambda: initial.lambda,
    repeats: initial.repeats,
  });

  // Guided lesson: the claim's exact conditions (λ = 1, one write each).
  const guided = useMemo(() => deriveSession({ rho, lambda: 1, repeats: 1 }), [rho]);
  const sandboxSession = useMemo(() => deriveSession(sandbox), [sandbox]);
  useHashSync({ rho, lambda: sandbox.lambda, repeats: sandbox.repeats });

  return (
    <div className="page">
      <a href="#step-1" className="skip-link">
        Skip to the interactive lesson
      </a>
      <header>
        <h1>Memory Under Pressure</h1>
        <p className="subtitle">How a matrix remembers — and interferes</p>
        <div className="claim">
          <strong>The one-sentence claim, which this page lets you test</strong>
          For the additive memory below, storing two associations with orthogonal unit keys permits
          exact recall; increasing their key overlap introduces calculable interference — while the
          recurrent matrix keeps the same shape and no trained parameters change.
        </div>
        <p>
          <strong>Who this is for:</strong> undergraduate ML learners and working data scientists
          comfortable with vectors, dot products, matrix multiplication and basic neural networks.
          Refreshers appear where needed. <strong>Conditions of the claim:</strong> zero initial
          state, one write per association, no decay in the guided lesson (λ = 1), the unit
          keys/values shown in step 1, queries after both writes.
        </p>
        <p style={{ fontFamily: 'var(--sans)', fontSize: '0.85rem' }}>
          Labels used on this page: <Badge kind="live" /> numbers computed in your browser right
          now · <Badge kind="source" /> equations/figures transcribed from a cited paper ·{' '}
          <Badge kind="reported" /> results a paper's own authors report ·{' '}
          <Badge kind="toy" /> our 2×2 model, which is not BDH.
        </p>
        <nav className="toc" aria-label="lesson steps">
          <strong style={{ fontSize: '0.85rem' }}>The journey</strong>
          <ol>
            <li><a href="#step-1">Store two things</a></li>
            <li><a href="#step-2">Make the cues collide</a></li>
            <li><a href="#step-3">Where did the extra signal come from?</a></li>
            <li><a href="#step-4">What changed?</a></li>
            <li><a href="#step-5">The same mechanism in BDH and BDH-CQ</a></li>
            <li><a href="#step-6">Try to break the claim</a></li>
            <li><a href="#step-7">Explain it back</a></li>
          </ol>
        </nav>
      </header>

      <main>
        <Step n={1} title="Store two things">
          <p>
            A <em>fast weight</em> memory stores relationships by changing connections, not by
            appending to a list. Here is the whole mechanism — an{' '}
            <strong>unnormalized additive associative memory</strong> with state{' '}
            <Eq tex="M \in \mathbb{R}^{2\times 2}" />, writes{' '}
            <Eq tex="M_t = \lambda M_{t-1} + v_t k_t^{\top}" /> (λ = 1 for now) and reads{' '}
            <Eq tex="\mathrm{retrieved}(q) = M_t\, q" />. Column vectors throughout. Two
            associations get written: cue <Eq tex="k_A" /> should recall value <Eq tex="v_A" />,
            cue <Eq tex="k_B" /> should recall <Eq tex="v_B" />.
          </p>
          <StoreTwoThings session={guided} />
          <p className="note">
            Refresher — <strong>outer product:</strong> <Eq tex="v k^{\top}" /> is the matrix whose
            (i,&thinsp;j) entry is <Eq tex="v_i k_j" />: a rank-1 “stamp” of the whole pair.{' '}
            <strong>Reading</strong> is a matrix–vector product; by linearity it returns each
            stored value weighted by how much its key matches the cue:{' '}
            <Eq tex="Mq = \textstyle\sum_i v_i\,(k_i \cdot q)" />.
          </p>
        </Step>

        <Step n={2} title="Make the cues collide">
          <p>
            Everything interesting is controlled by one number: the overlap{' '}
            <Eq tex="\rho = k_A \cdot k_B" />. The claim says recall at ρ = 0 is exact and the
            error at ρ &gt; 0 is exactly calculable. Test it.
          </p>
          <CollideCues session={guided} rho={rho} onRho={setRho} />
        </Step>

        <Step n={3} title="Where did the extra signal come from?">
          <CrossTerm session={guided} />
        </Step>

        <Step n={4} title="What changed?">
          <WhatChanged session={guided} />
        </Step>

        <Step n={5} title="The same mechanism in BDH and BDH-CQ">
          <p>
            You now own the vocabulary: rank-1 <strong>write</strong>, matrix–vector{' '}
            <strong>read</strong>, fast <strong>state</strong> vs trained <strong>weights</strong>,
            and <strong>interference</strong>. Here is where each piece lives in a published
            frontier architecture.
          </p>
          <BdhModule />
        </Step>

        <Step n={6} title="Try to break the claim">
          <p>
            The guided lesson kept the claim's exact conditions. The sandbox lets you leave them —
            repeat writes, add decay — and watch what survives. The claim's edge cases are presets.
          </p>
          <BreakTheClaim
            session={sandboxSession}
            params={sandbox}
            onParams={(p) => {
              setSandbox(p);
            }}
          />
          <h3 style={{ marginTop: '2rem' }}>Why this matters in 2026</h3>
          <Comparison />
        </Step>

        <Step n={7} title="Explain it back">
          <ExplainItBack />
        </Step>

        <References />
      </main>

      <footer>
        <p>
          <strong>Memory Under Pressure</strong> — a DataForge 2026 Pathway-track explainer.
          Everything interactive on this page is computed live in your browser from the 2×2 toy
          memory (original toy computation, MIT-licensed source). Equations from cited papers are
          source-derived illustrations; benchmark numbers are author-reported by their papers.
          No BDH model runs here. Caps: history ≤ 64 pairs, |components| ≤ 4, λ ∈ [0,1] — stated,
          not hidden.
        </p>
        <p>
          Source, tests, research ledger, and AI-assistance disclosure:{' '}
          <a href="https://github.com/jainraunak944/dataforge">repository</a> ·{' '}
          <a
            href="https://github.com/jainraunak944/dataforge/blob/claude/memory-under-pressure-p6vp89/docs/RESEARCH.md"
          >
            docs/RESEARCH.md
          </a>
        </p>
      </footer>
    </div>
  );
}
