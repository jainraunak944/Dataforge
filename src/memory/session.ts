/**
 * Pure derivation of everything the UI shows from a small set of concept
 * variables. The UI renders THIS state — there are no painted output values.
 * Because it is pure and deterministic, unit tests exercise exactly what the
 * interface displays, and every preset/reset is reproducible.
 */

import {
  outerProduct,
  readMemory,
  writeAssociation,
  zeroMatrix,
  type Matrix,
  type Vec,
} from './additiveMemory';
import { coreStateSlots, historySlots } from './accounting';
import { argmaxOrTie, matchScores, recallReport, type RecallReport, type TieOutcome } from './evaluate';
import { guidedFixture, type GuidedFixture } from './fixtures';
import { HISTORY_CAP, maxAbsDifference, referenceRead, type Pair } from './reference';

export interface SessionParams {
  rho: number;
  lambda: number;
  /** Times each of A and B is written, interleaved A,B,A,B… ≥1. */
  repeats: number;
}

export interface QueryView {
  label: 'A' | 'B';
  cue: Vec;
  report: RecallReport; // desired, retrieved (recurrent), l2 error
  referenceRetrieved: Vec; // independent explicit-history path
  recurrentVsReferenceMaxDiff: number;
  cueMatchScores: number[]; // dot(k_i, cue) — raw scores, not probabilities
  tie: TieOutcome;
}

export interface SessionState {
  params: SessionParams;
  fixture: GuidedFixture;
  writes: { label: 'A' | 'B'; k: Vec; v: Vec; contribution: Matrix }[];
  /** Matrix after each write, starting with M_0 = 0 (for stepping). */
  matrixTimeline: Matrix[];
  matrix: Matrix;
  queries: [QueryView, QueryView];
  accounting: {
    coreSlots: number;
    historySlotsUsed: number;
    historyCap: number;
    dtype: 'float64';
  };
}

export const MAX_REPEATS = Math.floor(HISTORY_CAP / 2);

export function clampRepeats(r: number): number {
  if (!Number.isFinite(r)) return 1;
  return Math.min(MAX_REPEATS, Math.max(1, Math.round(r)));
}

export function deriveSession(paramsRaw: SessionParams): SessionState {
  const repeats = clampRepeats(paramsRaw.repeats);
  const fixture = guidedFixture(paramsRaw.rho);
  const lambda = paramsRaw.lambda;
  const params: SessionParams = { rho: fixture.rho, lambda, repeats };

  const writeSeq: { label: 'A' | 'B'; k: Vec; v: Vec }[] = [];
  for (let r = 0; r < repeats; r++) {
    writeSeq.push({ label: 'A', k: fixture.kA, v: fixture.vA });
    writeSeq.push({ label: 'B', k: fixture.kB, v: fixture.vB });
  }

  const matrixTimeline: Matrix[] = [zeroMatrix(2, 2)];
  const writes: SessionState['writes'] = [];
  const history: Pair[] = [];
  for (const w of writeSeq) {
    const prev = matrixTimeline[matrixTimeline.length - 1];
    matrixTimeline.push(writeAssociation(prev, w.k, w.v, lambda));
    writes.push({ ...w, contribution: outerProduct(w.v, w.k) });
    history.push({ k: w.k, v: w.v });
  }
  const matrix = matrixTimeline[matrixTimeline.length - 1];

  const storedKeys = [fixture.kA, fixture.kB];
  const makeQuery = (label: 'A' | 'B'): QueryView => {
    const cue = label === 'A' ? fixture.kA : fixture.kB;
    const desired = label === 'A' ? fixture.vA : fixture.vB;
    const retrieved = readMemory(matrix, cue);
    const ref = referenceRead(history, cue, lambda, 2);
    const scores = matchScores(cue, storedKeys);
    return {
      label,
      cue,
      report: recallReport(desired, retrieved),
      referenceRetrieved: ref,
      recurrentVsReferenceMaxDiff: maxAbsDifference(retrieved, ref),
      cueMatchScores: scores,
      tie: argmaxOrTie(scores),
    };
  };

  return {
    params,
    fixture,
    writes,
    matrixTimeline,
    matrix,
    queries: [makeQuery('A'), makeQuery('B')],
    accounting: {
      coreSlots: coreStateSlots(2, 2),
      historySlotsUsed: historySlots(history.length, 2, 2),
      historyCap: HISTORY_CAP,
      dtype: 'float64',
    },
  };
}
