import { useEffect, useState } from 'react';
import { useReducedMotion } from '../hooks';
import type { SessionState } from '../memory/session';
import { AssocMark, Badge, Eq, MatrixView, VectorView, fmt } from './primitives';

/**
 * Lesson step 1: the two cue/value pairs, each write's outer product, and
 * the changing 2×2 matrix. Stepping walks the REAL matrix timeline computed
 * by the memory module — every transition shown is a computed state.
 */
export default function StoreTwoThings({ session }: { session: SessionState }) {
  const reduced = useReducedMotion();
  const maxStep = session.matrixTimeline.length - 1; // 2 writes in guided mode
  const [step, setStep] = useState(maxStep);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (!playing) return;
    if (step >= maxStep) {
      setPlaying(false);
      return;
    }
    const id = window.setTimeout(() => setStep((s) => Math.min(maxStep, s + 1)), reduced ? 0 : 900);
    return () => window.clearTimeout(id);
  }, [playing, step, maxStep, reduced]);

  useEffect(() => {
    // If the fixture changes (ρ moved), snap to the final state.
    setStep(maxStep);
    setPlaying(false);
  }, [session, maxStep]);

  const M = session.matrixTimeline[step];
  const lastWrite = step > 0 ? session.writes[step - 1] : null;

  return (
    <div className="panel">
      <p className="panel-title">
        Two writes into one 2×2 matrix <Badge kind="live" />
      </p>

      <div className="viz-row">
        <div>
          <h3>
            The pairs to store <span aria-hidden="true">—</span> cue → value
          </h3>
          <div className="viz-row" style={{ gap: '0.8rem' }}>
            <div>
              <AssocMark which="A" />
              <div className="viz-row" style={{ gap: '0.5rem', marginTop: '0.4rem' }}>
                <VectorView v={session.fixture.kA} caption={<Eq tex="k_A" />} accent="a" />
                <VectorView v={session.fixture.vA} caption={<Eq tex="v_A" />} accent="a" />
              </div>
            </div>
            <div>
              <AssocMark which="B" />
              <div className="viz-row" style={{ gap: '0.5rem', marginTop: '0.4rem' }}>
                <VectorView v={session.fixture.kB} caption={<Eq tex="k_B" />} accent="b" />
                <VectorView v={session.fixture.vB} caption={<Eq tex="v_B" />} accent="b" />
              </div>
            </div>
          </div>
        </div>

        <div>
          <h3>Each write adds an outer product</h3>
          <Eq
            block
            tex="M_t \;=\; \lambda\, M_{t-1} \;+\; v_t\, k_t^{\top}"
            label="M sub t equals lambda times M sub t minus 1, plus v sub t times k sub t transpose"
          />
          {lastWrite ? (
            <MatrixView
              M={lastWrite.contribution}
              caption={
                <>
                  write {step}: <AssocMark which={lastWrite.label} />{' '}
                  <Eq tex={`v_${lastWrite.label} k_${lastWrite.label}^{\\top}`} />
                </>
              }
            />
          ) : (
            <p style={{ fontFamily: 'var(--sans)', fontSize: '0.9rem', color: 'var(--ink-soft)' }}>
              Nothing written yet — the memory starts at <Eq tex="M_0 = 0" />.
            </p>
          )}
        </div>

        <div>
          <h3>Memory after step {step}</h3>
          <MatrixView M={M} caption={<Eq tex={`M_{${step}}`} />} />
          <div className="control-row" role="group" aria-label="write stepping controls">
            <button type="button" onClick={() => setStep((s) => Math.max(0, s - 1))} disabled={step === 0}>
              ◀ Back
            </button>
            <button
              type="button"
              onClick={() => setStep((s) => Math.min(maxStep, s + 1))}
              disabled={step === maxStep}
            >
              Step ▶
            </button>
            <button
              type="button"
              onClick={() => {
                if (playing) {
                  setPlaying(false);
                } else {
                  if (step >= maxStep) setStep(0);
                  setPlaying(true);
                }
              }}
            >
              {playing ? 'Pause' : reduced ? 'Play (instant — reduced motion)' : 'Play'}
            </button>
          </div>
        </div>
      </div>

      <p style={{ fontSize: '0.95rem' }}>
        Writing is <strong>addition</strong>: each pair drops a rank-1 stamp{' '}
        <Eq tex="v\,k^{\top}" /> onto the same four numbers. Nothing is stored “in a slot”; both
        associations share every cell. With the current overlap (ρ = {fmt(session.fixture.rho, 2)}),
        the matrix ends at{' '}
        <Eq
          tex={`M_2 = \\begin{bmatrix} ${fmt(session.matrix[0][0], 2)} & ${fmt(session.matrix[0][1], 2)} \\\\ ${fmt(session.matrix[1][0], 2)} & ${fmt(session.matrix[1][1], 2)} \\end{bmatrix}`}
          label="the current two by two memory matrix"
        />
        .
      </p>
    </div>
  );
}
