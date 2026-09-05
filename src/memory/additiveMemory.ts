/**
 * Unnormalized additive associative memory (the recurrent path).
 *
 * Convention: column vectors throughout.
 *   k_t, q ∈ R^{dKey}   v_t ∈ R^{dValue}   M_t ∈ R^{dValue × dKey}
 *   M_0 = 0
 *   M_t = λ · M_{t-1} + v_t · k_tᵀ
 *   retrieved(q) = M_t · q
 *
 * Matrices are stored row-major: M[row][col], row indexes the value
 * dimension, col indexes the key dimension.
 *
 * This module is the memory engine. It never receives item identities or
 * ground-truth answers — only vectors. The evaluator (UI / tests) holds the
 * desired values and computes errors; that boundary is documented in
 * docs/ARCHITECTURE.md.
 *
 * This is NOT softmax attention and NOT a BDH model; see docs/CLAIM.md.
 */

export type Vec = readonly number[];
export type Matrix = readonly (readonly number[])[];

/** Hard bounds; stated in the UI. Exceeding them throws (never silently clamps). */
export const BOUNDS = {
  maxDim: 8,
  maxAbsComponent: 4,
  lambdaMin: 0,
  lambdaMax: 1,
} as const;

export function assertFiniteVec(x: Vec, name: string): void {
  if (x.length === 0 || x.length > BOUNDS.maxDim) {
    throw new RangeError(`${name}: dimension ${x.length} outside 1..${BOUNDS.maxDim}`);
  }
  for (let i = 0; i < x.length; i++) {
    const c = x[i];
    if (!Number.isFinite(c)) throw new RangeError(`${name}[${i}] is not finite`);
    if (Math.abs(c) > BOUNDS.maxAbsComponent) {
      throw new RangeError(`${name}[${i}]=${c} exceeds |${BOUNDS.maxAbsComponent}|`);
    }
  }
}

export function assertLambda(lambda: number): void {
  if (!Number.isFinite(lambda) || lambda < BOUNDS.lambdaMin || lambda > BOUNDS.lambdaMax) {
    throw new RangeError(`lambda=${lambda} outside [${BOUNDS.lambdaMin}, ${BOUNDS.lambdaMax}]`);
  }
}

export function zeroMatrix(dValue: number, dKey: number): Matrix {
  return Array.from({ length: dValue }, () => Array.from({ length: dKey }, () => 0));
}

/** v · kᵀ — the write's rank-1 contribution, also displayed by the UI. */
export function outerProduct(v: Vec, k: Vec): Matrix {
  assertFiniteVec(v, 'v');
  assertFiniteVec(k, 'k');
  return v.map((vi) => k.map((kj) => vi * kj));
}

/** One write: M_t = λ · M_{t-1} + v · kᵀ. Pure — returns a new matrix. */
export function writeAssociation(M: Matrix, k: Vec, v: Vec, lambda: number): Matrix {
  assertFiniteVec(k, 'k');
  assertFiniteVec(v, 'v');
  assertLambda(lambda);
  if (M.length !== v.length || (M[0]?.length ?? 0) !== k.length) {
    throw new RangeError(
      `shape mismatch: M is ${M.length}×${M[0]?.length ?? 0}, write is ${v.length}×${k.length}`,
    );
  }
  return M.map((row, i) => row.map((mij, j) => lambda * mij + v[i] * k[j]));
}

/** Read: retrieved(q) = M · q. Raw scores — not probabilities. */
export function readMemory(M: Matrix, q: Vec): number[] {
  assertFiniteVec(q, 'q');
  if ((M[0]?.length ?? 0) !== q.length) {
    throw new RangeError(`shape mismatch: M has ${M[0]?.length ?? 0} cols, q has ${q.length}`);
  }
  return M.map((row) => row.reduce((acc, mij, j) => acc + mij * q[j], 0));
}

export function dot(a: Vec, b: Vec): number {
  if (a.length !== b.length) throw new RangeError('dot: length mismatch');
  return a.reduce((acc, ai, i) => acc + ai * b[i], 0);
}

export function l2Norm(x: Vec): number {
  return Math.sqrt(dot(x, x));
}

/** L2 error between desired and retrieved — computed by the evaluator, not the memory. */
export function l2Distance(a: Vec, b: Vec): number {
  if (a.length !== b.length) throw new RangeError('l2Distance: length mismatch');
  return Math.sqrt(a.reduce((acc, ai, i) => acc + (ai - b[i]) ** 2, 0));
}

export function matrixShape(M: Matrix): { rows: number; cols: number } {
  return { rows: M.length, cols: M[0]?.length ?? 0 };
}
