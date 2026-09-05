/**
 * Explicit-history reference — the INDEPENDENT check on the recurrent memory.
 *
 * Deliberately written in a different style from additiveMemory.ts (index
 * loops over a retained list of pairs, no shared helpers) so that agreement
 * between the two paths is evidence, not circularity. Tests compare both
 * against hand-calculated fixtures as well.
 *
 *   reference(q) = Σ_{i=1..t} λ^(t−i) · v_i · (k_i · q)
 *
 * Convention at λ = 0: the newest write (i = t) has weight λ^0 = 1, all
 * earlier writes have weight 0. (JavaScript: Math.pow(0, 0) === 1.)
 *
 * This equivalence is a property of the chosen LINEAR operation. It is not
 * an assertion of equality with conventional softmax attention.
 *
 * Memory accounting: this path retains every pair — N·(dKey+dValue) scalars
 * for N writes — where the recurrent path holds dKey·dValue regardless of N.
 * In the app the history is capped (see HISTORY_CAP); the cap is stated in
 * the UI and exists so the teaching interface itself stays bounded.
 */

export interface Pair {
  readonly k: readonly number[];
  readonly v: readonly number[];
}

/** Cap on retained pairs in the teaching interface (stated in the UI). */
export const HISTORY_CAP = 64;

export function referenceRead(
  history: readonly Pair[],
  q: readonly number[],
  lambda: number,
  dValueIfEmpty = 0,
): number[] {
  if (history.length > HISTORY_CAP) {
    throw new RangeError(`history length ${history.length} exceeds cap ${HISTORY_CAP}`);
  }
  const t = history.length;
  const dValue = t > 0 ? history[0].v.length : dValueIfEmpty;
  const out: number[] = new Array(dValue).fill(0);
  for (let i = 0; i < t; i++) {
    const { k, v } = history[i];
    // weight for the (i+1)-th write of t total: λ^(t − (i+1))
    const w = Math.pow(lambda, t - (i + 1));
    let kDotQ = 0;
    for (let j = 0; j < k.length; j++) {
      kDotQ += k[j] * q[j];
    }
    for (let r = 0; r < dValue; r++) {
      out[r] += w * v[r] * kDotQ;
    }
  }
  return out;
}

/**
 * Tolerance for recurrent-vs-reference agreement (stated where compared).
 * Sized for the app's bounds: components ≤ 4, dims ≤ 8, ≤ 64 writes in
 * float64 — worst-case accumulated rounding stays orders of magnitude below
 * this; the 2×2 lesson agrees to ~1e-15.
 */
export const FLOAT_TOLERANCE = 1e-9;

export function maxAbsDifference(a: readonly number[], b: readonly number[]): number {
  if (a.length !== b.length) return Number.POSITIVE_INFINITY;
  let m = 0;
  for (let i = 0; i < a.length; i++) {
    const d = Math.abs(a[i] - b[i]);
    if (d > m) m = d;
  }
  return m;
}
