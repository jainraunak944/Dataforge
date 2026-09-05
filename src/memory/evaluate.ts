/**
 * Evaluator-side helpers. The evaluator knows the task's ground truth
 * (desired values) so it can display error; the memory engine in
 * additiveMemory.ts never does. This file is that boundary.
 */

import { dot, l2Distance, type Vec } from './additiveMemory';

export interface RecallReport {
  desired: Vec;
  retrieved: Vec;
  l2Error: number;
}

export function recallReport(desired: Vec, retrieved: Vec): RecallReport {
  return { desired, retrieved, l2Error: l2Distance(desired, retrieved) };
}

/**
 * Cue-match scores against the stored keys: dot(k_i, q). Raw scores —
 * never probabilities, and the UI labels them as scores.
 */
export function matchScores(q: Vec, keys: readonly Vec[]): number[] {
  return keys.map((k) => dot(k, q));
}

export type TieOutcome =
  | { kind: 'winner'; index: number }
  | { kind: 'tie'; indices: number[] };

/**
 * Deterministic tie reporting. Scores within `epsilon` of the maximum tie;
 * a tie is reported as a tie (indices in ascending order), never resolved
 * by an arbitrary argmax. At ρ = 1 the two cues are identical, so both
 * associations tie and the cue carries no distinguishing information.
 */
export function argmaxOrTie(scores: readonly number[], epsilon = 1e-12): TieOutcome {
  if (scores.length === 0) throw new RangeError('argmaxOrTie: empty scores');
  let max = -Infinity;
  for (const s of scores) {
    if (!Number.isFinite(s)) throw new RangeError('argmaxOrTie: non-finite score');
    if (s > max) max = s;
  }
  const indices = scores.flatMap((s, i) => (max - s <= epsilon ? [i] : []));
  return indices.length === 1
    ? { kind: 'winner', index: indices[0] }
    : { kind: 'tie', indices };
}
