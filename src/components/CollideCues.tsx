import { useId } from 'react';
import type { SessionState } from '../memory/session';
import { fmt, AssocMark, Badge, Eq, ErrorChip, KeyCircle, VectorView } from './primitives';

/**
 * Lesson step 2: the overlap slider. Desired value, retrieved value,
 * independent reference and L2 error side by side for both cues.
 * Truth (desired) is held by the evaluator; the memory only ever sees vectors.
 */
export default function CollideCues({
  session,
  rho,
  onRho,
}: {
  session: SessionState;
  rho: number;
  onRho: (r: number) => void;
}) {
  const sliderId = useId();
  const [qa, qb] = session.queries;

  return (
    <div className="panel">
      <p className="panel-title">
        One slider: key overlap ρ = k<sub>A</sub>·k<sub>B</sub> <Badge kind="live" />
      </p>

      <div className="slider-block">
        <label htmlFor={sliderId}>
          Key overlap ρ (0 = orthogonal cues, 1 = identical cues)
        </label>
        <div className="slider-row">
          <input
            id={sliderId}
            data-testid="guided-rho"
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={rho}
            onChange={(e) => onRho(Number(e.target.value))}
            aria-valuetext={`overlap ${fmt(rho, 2)}`}
          />
          <output htmlFor={sliderId} className="slider-value" data-testid="guided-rho-value">
            {fmt(rho, 2)}
          </output>
        </div>
      </div>

      <div className="viz-row">
        <div style={{ flex: '0 1 210px' }}>
          <KeyCircle kA={session.fixture.kA} kB={session.fixture.kB} />
          <p style={{ fontFamily: 'var(--sans)', fontSize: '0.85rem', color: 'var(--ink-soft)' }}>
            Both keys stay unit length; the slider only rotates{' '}
            <span className="assoc b">▲&thinsp;k_B</span> toward{' '}
            <span className="assoc a">●&thinsp;k_A</span>.
          </p>
        </div>

        {([qa, qb] as const).map((q) => (
          <div key={q.label}>
            <h3>
              Query with cue <AssocMark which={q.label} />
            </h3>
            <div className="viz-row" style={{ gap: '0.5rem' }}>
              <VectorView
                v={q.report.desired}
                caption={<>desired (ground truth)</>}
                accent={q.label === 'A' ? 'a' : 'b'}
              />
              <VectorView v={q.report.retrieved} caption={<>retrieved = M·cue</>} />
              <VectorView v={q.referenceRetrieved} caption={<>reference Σ vᵢ(kᵢ·q)</>} />
            </div>
            <p style={{ margin: '0.5rem 0 0' }}>
              <ErrorChip value={q.report.l2Error} />{' '}
              <span
                style={{ fontFamily: 'var(--sans)', fontSize: '0.83rem', color: 'var(--ink-soft)' }}
              >
                recurrent vs reference agree to {q.recurrentVsReferenceMaxDiff.toExponential(1)}
              </span>
            </p>
          </div>
        ))}
      </div>

      <p>
        The closed forms are visible in the numbers: reading with <Eq tex="k_A" /> returns{' '}
        <Eq tex="[1,\ \rho]^{\top}" />, reading with <Eq tex="k_B" /> returns{' '}
        <Eq tex="[\rho,\ 1]^{\top}" />. At ρ = 0 recall is exact. As overlap grows, each cue drags
        in <em>ρ of the other value</em> — and the L2 error is exactly ρ. Drag the slider and watch
        the prediction hold.
      </p>

      {session.fixture.rho >= 1 && (
        <div className="note warn" role="status">
          <strong>ρ = 1: full ambiguity.</strong> Both cues are now the same vector, and both reads
          return [1, 1]. The cue contains no information that can distinguish A from B — reporting a
          “winner” here would be a lie, so the app reports a tie instead.
        </div>
      )}

      <p className="note">
        The <strong>reference</strong> column is an independent computation that keeps every (key,
        value) pair in a list and evaluates <Eq tex="\textstyle\sum_i v_i (k_i \cdot q)" /> directly
        — the same algebra with a different storage strategy. Agreement between the two columns is a
        property of this <em>linear</em> operation, not of softmax attention. The stated tolerance
        is 10⁻⁹.
      </p>
    </div>
  );
}
