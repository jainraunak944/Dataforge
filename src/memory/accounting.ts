/**
 * Honest memory accounting for the two storage strategies.
 *
 * These are analytical scalar-slot counts for the toy under a stated dtype.
 * They are NOT measured GPU RAM and NOT a benchmark of production
 * Transformers. The teaching interface additionally holds bounded visual
 * history, fixture data and ground truth; a constant-size MODEL state does
 * not mean constant total browser memory, fixed total compute, unbounded
 * lossless storage, or zero interference.
 */

export type Dtype = 'float64' | 'float32';

export const BYTES_PER_SCALAR: Record<Dtype, number> = {
  float64: 8,
  float32: 4,
};

/** Recurrent matrix: dKey·dValue scalars regardless of how many writes occurred. */
export function coreStateSlots(dKey: number, dValue: number): number {
  return dKey * dValue;
}

/** Retained pairs: N·(dKey+dValue) scalars for N writes. */
export function historySlots(nWrites: number, dKey: number, dValue: number): number {
  return nWrites * (dKey + dValue);
}

export function slotsToBytes(slots: number, dtype: Dtype): number {
  return slots * BYTES_PER_SCALAR[dtype];
}
