import { useId } from 'react';
import { PRESETS } from '../memory/fixtures';
import { HISTORY_CAP } from '../memory/reference';
import { MAX_REPEATS, type SessionParams, type SessionState } from '../memory/session';
import { slotsToBytes } from '../memory/accounting';
import { fmt, AssocMark, Badge, Eq, ErrorChip, MatrixView, VectorView } from './primitives';

/**
 * Lesson step 6 + sandbox: compact presets that try to break the claim, plus
 * the decay and repeated-write controls. Every preset is a full
 * deterministic reset (same params → identical state, unit-tested).
 */
export default function BreakTheClaim({
  session,
  params,
  onParams,
}: {
  session: SessionState;
  params: SessionParams;
  onParams: (p: SessionParams) => void;
}) {
  const lambdaId = useId();
  const repeatsId = useId();
  const rhoId = useId();
  const [qa, qb] = session.queries;
  const acct = session.accounting;

  return (
    <div className="panel">
      <p className="panel-title">
        Sandbox — try to break the claim <Badge kind="live" />
      </p>

      <div className="control-row" role="group" aria-label="presets">
        {PRESETS.map((p) => {
          const active =
            Math.abs(params.rho - p.rho) < 1e-9 &&
            Math.abs(params.lambda - p.lambda) < 1e-9 &&
            params.repeats === p.repeats;
          return (
            <button
              key={p.id}
              type="button"
              className={active ? 'primary' : ''}
              aria-pressed={active}
              title={p.description}
              onClick={() => onParams({ rho: p.rho, lambda: p.lambda, repeats: p.repeats })}
            >
              {p.label}
            </button>
          );
        })}
      </div>
      <p style={{ fontFamily: 'var(--sans)', fontSize: '0.88rem', color: 'var(--ink-soft)' }}>
        {PRESETS.map((p) => (
          <span key={p.id} style={{ display: 'block' }}>
            <strong>{p.label}:</strong> {p.description}
          </span>
        ))}
      </p>

      <div className="slider-block">
        <label htmlFor={rhoId}>Key overlap ρ</label>
        <div className="slider-row">
          <input
            id={rhoId}
            data-testid="sandbox-rho"
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={params.rho}
            onChange={(e) => onParams({ ...params, rho: Number(e.target.value) })}
            aria-valuetext={`overlap ${fmt(params.rho, 2)}`}
          />
          <span className="slider-value" data-testid="sandbox-rho-value">{fmt(params.rho, 2)}</span>
        </div>
      </div>

      <div className="slider-block">
        <label htmlFor={lambdaId}>
          Decay λ — the guided lesson fixed λ = 1; here it is yours
        </label>
        <div className="slider-row">
          <input
            id={lambdaId}
            data-testid="sandbox-lambda"
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={params.lambda}
            onChange={(e) => onParams({ ...params, lambda: Number(e.target.value) })}
            aria-valuetext={`decay ${fmt(params.lambda, 2)}`}
          />
          <span className="slider-value" data-testid="sandbox-lambda-value">{fmt(params.lambda, 2)}</span>
        </div>
      </div>

      <div className="slider-block">
        <label htmlFor={repeatsId}>
          Writes of each pair (A,B,A,B…) — capped at {MAX_REPEATS} each so the retained-pairs
          comparison below stays bounded at {HISTORY_CAP} pairs
        </label>
        <div className="slider-row">
          <input
            id={repeatsId}
            data-testid="sandbox-repeats"
            type="range"
            min={1}
            max={MAX_REPEATS}
            step={1}
            value={params.repeats}
            onChange={(e) => onParams({ ...params, repeats: Number(e.target.value) })}
            aria-valuetext={`${params.repeats} writes of each pair`}
          />
          <span className="slider-value" data-testid="sandbox-repeats-value">{params.repeats}×</span>
        </div>
      </div>

      <div className="viz-row">
        <MatrixView
          M={session.matrix}
          caption={
            <>
              M after {session.writes.length} writes — still{' '}
              {`${session.matrix.length}×${session.matrix[0].length}`}
            </>
          }
        />
        {([qa, qb] as const).map((q) => (
          <div key={q.label}>
            <h3 style={{ marginTop: 0 }}>
              Read <AssocMark which={q.label} />
            </h3>
            <div className="viz-row" style={{ gap: '0.5rem' }}>
              <VectorView v={q.report.desired} caption="desired" accent={q.label === 'A' ? 'a' : 'b'} />
              <VectorView v={q.report.retrieved} caption="retrieved" testId={`sandbox-retrieved-${q.label}`} />
            </div>
            <p style={{ margin: '0.4rem 0 0' }}>
              <ErrorChip value={q.report.l2Error} />
            </p>
            {q.tie.kind === 'tie' && (
              <p className="note warn" style={{ margin: '0.4rem 0 0' }}>
                Cue-match scores tie ({q.cueMatchScores.map((s) => fmt(s, 2)).join(' vs ')}) — the
                cue cannot distinguish the associations. Reported as a tie, not a winner.
              </p>
            )}
          </div>
        ))}
      </div>

      <h3>Honest memory accounting</h3>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">Storage strategy</th>
              <th scope="col">Scalar slots (float64)</th>
              <th scope="col">Bytes</th>
              <th scope="col">Grows with writes?</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                Recurrent matrix <Eq tex="M" /> (d_k·d_v)
              </td>
              <td className="num">{acct.coreSlots}</td>
              <td className="num">{slotsToBytes(acct.coreSlots, 'float64')}</td>
              <td>No — constant shape (that is the point)</td>
            </tr>
            <tr>
              <td>Retained pairs (N·(d_k+d_v)), the reference path</td>
              <td className="num">{acct.historySlotsUsed}</td>
              <td className="num">{slotsToBytes(acct.historySlotsUsed, 'float64')}</td>
              <td>Yes — linear in N (capped at {acct.historyCap} pairs here)</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p className="note">
        These counts are analytical, for the model state alone under float64. The teaching page
        additionally holds a bounded write history for the step animation, the fixture and the
        ground truth. A constant-size <em>model state</em> does not mean constant total browser
        memory, fixed total compute, unbounded lossless storage — or zero interference; the error
        column above is the price. Not measured GPU RAM; not a Transformer benchmark.
      </p>

      <p>
        What repeated writes show: with λ = 1 the readout magnitudes scale with the write count
        (write everything twice, read twice as much) while the matrix stays{' '}
        {`${session.matrix.length}×${session.matrix[0].length}`}. What decay shows: with λ &lt; 1
        older writes fade geometrically — at λ = 0 only the newest write survives (the newest keeps
        weight λ⁰ = 1 by convention). Neither escape hatch removes interference; delta-rule
        memories (see the comparison below) attack it differently.
      </p>
    </div>
  );
}
