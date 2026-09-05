/**
 * Correctness tests for the memory core.
 *
 * Expected values are HAND-CALCULATED literals (worked in the comments) or
 * come from the independently written explicit-history reference — never
 * from a second call to the implementation under test.
 */
import { describe, expect, it } from 'vitest';
import {
  BOUNDS,
  l2Distance,
  matrixShape,
  outerProduct,
  readMemory,
  writeAssociation,
  zeroMatrix,
} from '../src/memory/additiveMemory';
import { argmaxOrTie, matchScores } from '../src/memory/evaluate';
import { guidedFixture } from '../src/memory/fixtures';
import { FLOAT_TOLERANCE, maxAbsDifference, referenceRead } from '../src/memory/reference';

const TOL = 1e-12; // for exact hand-calculated 2×2 cases

describe('zero state and zero writes', () => {
  it('M_0 = 0 and reading it returns the zero vector', () => {
    const M = zeroMatrix(2, 2);
    expect(M).toEqual([
      [0, 0],
      [0, 0],
    ]);
    expect(readMemory(M, [1, 0])).toEqual([0, 0]);
    expect(readMemory(M, [0.6, 0.8])).toEqual([0, 0]);
  });

  it('reference with empty history returns the zero vector too', () => {
    expect(referenceRead([], [1, 0], 1, 2)).toEqual([0, 0]);
  });
});

describe('hand-calculated orthogonal fixture (ρ = 0)', () => {
  // kA=[1,0] kB=[0,1] vA=[1,0] vB=[0,1], λ=1
  // M = vA·kAᵀ + vB·kBᵀ = [[1,0],[0,0]] + [[0,0],[0,1]] = [[1,0],[0,1]]
  const f = guidedFixture(0);
  const M = writeAssociation(writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 1), f.kB, f.vB, 1);

  it('memory matrix is the identity', () => {
    expect(M[0][0]).toBeCloseTo(1, 12);
    expect(M[0][1]).toBeCloseTo(0, 12);
    expect(M[1][0]).toBeCloseTo(0, 12);
    expect(M[1][1]).toBeCloseTo(1, 12);
  });

  it('recall is exact: M·kA = [1,0], M·kB = [0,1], L2 error 0', () => {
    const a = readMemory(M, f.kA);
    const b = readMemory(M, f.kB);
    expect(maxAbsDifference(a, [1, 0])).toBeLessThan(TOL);
    expect(maxAbsDifference(b, [0, 1])).toBeLessThan(TOL);
    expect(l2Distance(a, [1, 0])).toBeLessThan(TOL);
    expect(l2Distance(b, [0, 1])).toBeLessThan(TOL);
  });
});

describe('hand-calculated partial overlap (ρ = 0.6)', () => {
  // kB = [0.6, 0.8] since √(1−0.36) = 0.8
  // M = [[1,0],[0,0]] + [0,1]ᵀ·[0.6,0.8] = [[1,0],[0.6,0.8]]
  // M·kA = [1·1+0·0, 0.6·1+0.8·0] = [1, 0.6]           (= [1, ρ])
  // M·kB = [1·0.6+0·0.8, 0.6·0.6+0.8·0.8] = [0.6, 1]   (= [ρ, 1])
  const f = guidedFixture(0.6);
  const M = writeAssociation(writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 1), f.kB, f.vB, 1);

  it('matrix matches the hand calculation', () => {
    expect(M[0][0]).toBeCloseTo(1, 12);
    expect(M[0][1]).toBeCloseTo(0, 12);
    expect(M[1][0]).toBeCloseTo(0.6, 12);
    expect(M[1][1]).toBeCloseTo(0.8, 12);
  });

  it('interference appears exactly as the closed form predicts', () => {
    expect(maxAbsDifference(readMemory(M, f.kA), [1, 0.6])).toBeLessThan(TOL);
    expect(maxAbsDifference(readMemory(M, f.kB), [0.6, 1])).toBeLessThan(TOL);
  });

  it('L2 error against desired equals ρ for both cues', () => {
    // |[1,0.6] − [1,0]| = 0.6 ; |[0.6,1] − [0,1]| = 0.6
    expect(l2Distance(readMemory(M, f.kA), [1, 0])).toBeCloseTo(0.6, 12);
    expect(l2Distance(readMemory(M, f.kB), [0, 1])).toBeCloseTo(0.6, 12);
  });
});

describe('second hand-calculated overlap (ρ = 0.28, exact decimals)', () => {
  // √(1−0.28²) = √0.9216 = 0.96 exactly in decimal
  // M = [[1,0],[0.28,0.96]] ; M·kA = [1,0.28] ; M·kB = [0.28, 0.28²+0.96² = 1]
  const f = guidedFixture(0.28);
  const M = writeAssociation(writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 1), f.kB, f.vB, 1);
  it('reads match the hand calculation', () => {
    expect(maxAbsDifference(readMemory(M, f.kA), [1, 0.28])).toBeLessThan(TOL);
    expect(maxAbsDifference(readMemory(M, f.kB), [0.28, 1])).toBeLessThan(TOL);
  });
});

describe('ρ = 1 ambiguity and deterministic tie reporting', () => {
  const f = guidedFixture(1);
  const M = writeAssociation(writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 1), f.kB, f.vB, 1);

  it('both cues are the same vector and both reads return [1, 1]', () => {
    expect(f.kB[0]).toBeCloseTo(1, 12);
    expect(f.kB[1]).toBeCloseTo(0, 12);
    expect(maxAbsDifference(readMemory(M, f.kA), [1, 1])).toBeLessThan(TOL);
    expect(maxAbsDifference(readMemory(M, f.kB), [1, 1])).toBeLessThan(TOL);
  });

  it('cue-match scores tie and are reported as a tie, never a winner', () => {
    const scores = matchScores(f.kA, [f.kA, f.kB]); // [1, 1]
    const outcome = argmaxOrTie(scores);
    expect(outcome).toEqual({ kind: 'tie', indices: [0, 1] });
  });

  it('below ρ = 1 there is a deterministic winner', () => {
    const g = guidedFixture(0.6);
    expect(argmaxOrTie(matchScores(g.kA, [g.kA, g.kB]))).toEqual({ kind: 'winner', index: 0 });
    expect(argmaxOrTie(matchScores(g.kB, [g.kA, g.kB]))).toEqual({ kind: 'winner', index: 1 });
  });
});

describe('repeated writes scale magnitude, not shape', () => {
  it('writing A,B twice with λ=1 doubles every readout', () => {
    // M after A,B,A,B = 2·(vA kAᵀ + vB kBᵀ) → M·kA = [2, 1.2] at ρ=0.6
    const f = guidedFixture(0.6);
    let M = zeroMatrix(2, 2);
    for (let i = 0; i < 2; i++) {
      M = writeAssociation(M, f.kA, f.vA, 1);
      M = writeAssociation(M, f.kB, f.vB, 1);
    }
    expect(maxAbsDifference(readMemory(M, f.kA), [2, 1.2])).toBeLessThan(TOL);
    expect(matrixShape(M)).toEqual({ rows: 2, cols: 2 });
  });
});

describe('decay endpoints', () => {
  const f = guidedFixture(0.6);

  it('λ = 0: only the newest write survives (newest has weight λ^0 = 1)', () => {
    // After A then B with λ=0: M = vB·kBᵀ = [[0,0],[0.6,0.8]]
    const M = writeAssociation(writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 0), f.kB, f.vB, 0);
    expect(M[0][0]).toBeCloseTo(0, 12);
    expect(M[1][0]).toBeCloseTo(0.6, 12);
    expect(M[1][1]).toBeCloseTo(0.8, 12);
    // M·kB = [0, 0.36+0.64] = [0, 1] — B recalls exactly, A is gone
    expect(maxAbsDifference(readMemory(M, f.kB), [0, 1])).toBeLessThan(TOL);
    expect(maxAbsDifference(readMemory(M, f.kA), [0, 0.6])).toBeLessThan(TOL);
    // Reference must use the same convention (Math.pow(0,0)===1 for newest)
    const ref = referenceRead([{ k: f.kA, v: f.vA }, { k: f.kB, v: f.vB }], f.kB, 0);
    expect(maxAbsDifference(ref, [0, 1])).toBeLessThan(TOL);
  });

  it('λ = 1 equals the plain sum; λ = 0.5 halves the older write', () => {
    // λ=0.5: M = 0.5·vA kAᵀ + vB kBᵀ = [[0.5,0],[0.6,0.8]] → M·kA = [0.5, 0.6]
    const M = writeAssociation(
      writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, 0.5),
      f.kB,
      f.vB,
      0.5,
    );
    expect(maxAbsDifference(readMemory(M, f.kA), [0.5, 0.6])).toBeLessThan(TOL);
  });
});

describe('outer product (write contribution shown in the UI)', () => {
  it('v·kᵀ for v=[0,1], k=[0.6,0.8] is [[0,0],[0.6,0.8]]', () => {
    expect(outerProduct([0, 1], [0.6, 0.8])).toEqual([
      [0, 0],
      [0.6, 0.8],
    ]);
  });
});

describe('input bounds, invalid values, finite outputs', () => {
  it('rejects NaN and Infinity components', () => {
    expect(() => readMemory(zeroMatrix(2, 2), [NaN, 0])).toThrow(RangeError);
    expect(() => writeAssociation(zeroMatrix(2, 2), [1, 0], [Infinity, 0], 1)).toThrow(RangeError);
  });
  it('rejects out-of-bounds λ and oversized components', () => {
    expect(() => writeAssociation(zeroMatrix(2, 2), [1, 0], [1, 0], 1.5)).toThrow(RangeError);
    expect(() => writeAssociation(zeroMatrix(2, 2), [1, 0], [1, 0], -0.1)).toThrow(RangeError);
    expect(() =>
      writeAssociation(zeroMatrix(2, 2), [BOUNDS.maxAbsComponent + 1, 0], [1, 0], 1),
    ).toThrow(RangeError);
  });
  it('rejects dimension mismatches', () => {
    expect(() => readMemory(zeroMatrix(2, 2), [1, 0, 0])).toThrow(RangeError);
    expect(() => writeAssociation(zeroMatrix(2, 2), [1, 0, 0], [1, 0], 1)).toThrow(RangeError);
  });
  it('all outputs finite across the ρ, λ grid', () => {
    for (let rho = 0; rho <= 1.0001; rho += 0.05) {
      for (const lambda of [0, 0.25, 0.5, 0.75, 1]) {
        const f = guidedFixture(Math.min(1, rho));
        const M = writeAssociation(
          writeAssociation(zeroMatrix(2, 2), f.kA, f.vA, lambda),
          f.kB,
          f.vB,
          lambda,
        );
        for (const out of [readMemory(M, f.kA), readMemory(M, f.kB)]) {
          for (const c of out) expect(Number.isFinite(c)).toBe(true);
        }
      }
    }
  });
});

describe('independent explicit-history equality (seeded fixtures)', () => {
  // Deterministic LCG — seeds stated, reproducible.
  function lcg(seed: number): () => number {
    let s = seed >>> 0;
    return () => {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 2 ** 32;
    };
  }

  it.each([[1], [42], [20260905]])('seed %i: recurrent equals reference within tolerance', (seed) => {
    const rand = lcg(seed);
    const dK = 2 + Math.floor(rand() * 3); // 2..4
    const dV = 2 + Math.floor(rand() * 3);
    for (const lambda of [0, 0.35, 1]) {
      let M = zeroMatrix(dV, dK);
      const history: { k: number[]; v: number[] }[] = [];
      const n = 1 + Math.floor(rand() * 63); // 1..64 writes, within HISTORY_CAP
      for (let i = 0; i < n; i++) {
        const k = Array.from({ length: dK }, () => rand() * 2 - 1);
        const v = Array.from({ length: dV }, () => rand() * 2 - 1);
        M = writeAssociation(M, k, v, lambda);
        history.push({ k, v });
      }
      const q = Array.from({ length: dK }, () => rand() * 2 - 1);
      const recurrent = readMemory(M, q);
      const ref = referenceRead(history, q, lambda);
      expect(maxAbsDifference(recurrent, ref)).toBeLessThan(FLOAT_TOLERANCE);
    }
  });
});

describe('constant core-state shape across sequence lengths', () => {
  it('shape stays 2×2 after 1, 8 and 64 writes', () => {
    const f = guidedFixture(0.3);
    for (const n of [1, 8, 64]) {
      let M = zeroMatrix(2, 2);
      for (let i = 0; i < n; i++) {
        M = writeAssociation(M, i % 2 === 0 ? f.kA : f.kB, i % 2 === 0 ? f.vA : f.vB, 1);
      }
      expect(matrixShape(M)).toEqual({ rows: 2, cols: 2 });
    }
  });
});
