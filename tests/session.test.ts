/**
 * Tests for the pure session derivation the UI renders. Because the UI maps
 * this state directly to the DOM, these tests are the "no painted output
 * values" guarantee at the logic level (the browser smoke test covers the
 * DOM level).
 */
import { describe, expect, it } from 'vitest';
import { PRESETS } from '../src/memory/fixtures';
import {
  clampLambda,
  clampRepeats,
  deriveSession,
  MAX_REPEATS,
  normalizeSessionParams,
} from '../src/memory/session';
import { FLOAT_TOLERANCE, maxAbsDifference } from '../src/memory/reference';

describe('deriveSession', () => {
  it('is deterministic: same params, identical state', () => {
    const a = deriveSession({ rho: 0.42, lambda: 0.7, repeats: 2 });
    const b = deriveSession({ rho: 0.42, lambda: 0.7, repeats: 2 });
    expect(a).toEqual(b);
  });

  it('guided default (ρ=0.6, λ=1, 1 repeat) matches hand calculation', () => {
    const s = deriveSession({ rho: 0.6, lambda: 1, repeats: 1 });
    expect(s.matrix[0][0]).toBeCloseTo(1, 12);
    expect(s.matrix[1][0]).toBeCloseTo(0.6, 12);
    expect(s.matrix[1][1]).toBeCloseTo(0.8, 12);
    const [qa, qb] = s.queries;
    expect(qa.report.retrieved[0]).toBeCloseTo(1, 12);
    expect(qa.report.retrieved[1]).toBeCloseTo(0.6, 12);
    expect(qa.report.l2Error).toBeCloseTo(0.6, 12);
    expect(qb.report.retrieved[0]).toBeCloseTo(0.6, 12);
    expect(qb.report.retrieved[1]).toBeCloseTo(1, 12);
  });

  it('recurrent and reference paths agree for every preset', () => {
    for (const p of PRESETS) {
      const s = deriveSession({ rho: p.rho, lambda: p.lambda, repeats: p.repeats });
      for (const q of s.queries) {
        expect(q.recurrentVsReferenceMaxDiff).toBeLessThan(FLOAT_TOLERANCE);
      }
    }
  });

  it('ρ=1 preset reports a tie on both cues', () => {
    const s = deriveSession({ rho: 1, lambda: 1, repeats: 1 });
    expect(s.queries[0].tie.kind).toBe('tie');
    expect(s.queries[1].tie.kind).toBe('tie');
  });

  it('core state slots stay 4 while history slots grow with writes', () => {
    const one = deriveSession({ rho: 0.3, lambda: 1, repeats: 1 });
    const many = deriveSession({ rho: 0.3, lambda: 1, repeats: 10 });
    expect(one.accounting.coreSlots).toBe(4);
    expect(many.accounting.coreSlots).toBe(4);
    expect(one.accounting.historySlotsUsed).toBe(2 * (2 + 2)); // 2 writes × (dK+dV)
    expect(many.accounting.historySlotsUsed).toBe(20 * (2 + 2)); // 20 writes
    expect(many.matrix.length).toBe(2);
    expect(many.matrix[0].length).toBe(2);
  });

  it('matrix timeline starts at M_0 = 0 and has one entry per write (stepping support)', () => {
    const s = deriveSession({ rho: 0.5, lambda: 1, repeats: 2 });
    expect(s.matrixTimeline.length).toBe(5); // M_0 + 4 writes
    expect(s.matrixTimeline[0]).toEqual([
      [0, 0],
      [0, 0],
    ]);
  });

  it('clamps out-of-range params instead of crashing (stated bounds)', () => {
    // repeats: integer in [1, MAX_REPEATS], existing Math.round behavior
    expect(clampRepeats(9999)).toBe(MAX_REPEATS);
    expect(clampRepeats(-5)).toBe(1);
    expect(clampRepeats(0)).toBe(1);
    expect(clampRepeats(2.4)).toBe(2);
    expect(clampRepeats(2.5)).toBe(3);
    expect(clampRepeats(NaN)).toBe(1);

    // λ: engine bounds [0, 1]; non-finite falls back to 1 (no decay)
    expect(clampLambda(2)).toBe(1);
    expect(clampLambda(-0.5)).toBe(0);
    expect(clampLambda(0.35)).toBe(0.35);
    expect(clampLambda(NaN)).toBe(1);

    // one normalization boundary for all three params
    expect(normalizeSessionParams({ rho: 7, lambda: 2, repeats: 9999 })).toEqual({
      rho: 1,
      lambda: 1,
      repeats: MAX_REPEATS,
    });
    expect(normalizeSessionParams({ rho: -3, lambda: -0.5, repeats: 0 })).toEqual({
      rho: 0,
      lambda: 0,
      repeats: 1,
    });

    // deriveSession must be safe when called directly with invalid params
    // (would previously throw RangeError from the engine for λ ∉ [0, 1])
    expect(() => deriveSession({ rho: 7, lambda: 2, repeats: 9999 })).not.toThrow();
    const s = deriveSession({ rho: 7, lambda: 2, repeats: 9999 });
    expect(s.params).toEqual({ rho: 1, lambda: 1, repeats: MAX_REPEATS });
    expect(s.writes.length).toBe(2 * MAX_REPEATS); // the effective repeats drove the math

    expect(() => deriveSession({ rho: 0.5, lambda: -0.5, repeats: 0 })).not.toThrow();
    const t = deriveSession({ rho: 0.5, lambda: -0.5, repeats: 0 });
    expect(t.params).toEqual({ rho: 0.5, lambda: 0, repeats: 1 });
    // Hand check that the normalized λ = 0 drove the computation: only the
    // newest write (B) survives, so M·kB = vB·(kB·kB) = [0, 1] exactly.
    expect(maxAbsDifference(t.queries[1].report.retrieved, [0, 1])).toBeLessThan(1e-12);

    // recurrent and independent reference paths still agree after normalization
    for (const session of [s, t]) {
      for (const q of session.queries) {
        expect(q.recurrentVsReferenceMaxDiff).toBeLessThan(FLOAT_TOLERANCE);
      }
    }
  });

  it('repeated-writes preset triples magnitude (λ=1, 3 repeats)', () => {
    const p = PRESETS.find((x) => x.id === 'repeated')!;
    const s = deriveSession({ rho: p.rho, lambda: p.lambda, repeats: p.repeats });
    // 3·(M for single pair): read with kA gives 3·[1, ρ] = [3, 0.9] at ρ=0.3
    expect(s.queries[0].report.retrieved[0]).toBeCloseTo(3, 12);
    expect(s.queries[0].report.retrieved[1]).toBeCloseTo(0.9, 12);
  });
});
