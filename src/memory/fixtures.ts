/**
 * The guided two-association fixture and sandbox presets.
 *
 *   k_A = [1, 0]ᵀ         v_A = [1, 0]ᵀ
 *   k_B = [ρ, √(1−ρ²)]ᵀ   v_B = [0, 1]ᵀ      ρ ∈ [0, 1]
 *
 * Both keys are unit length for every ρ, and k_A · k_B = ρ, so the slider
 * value IS the key overlap (cosine similarity).
 *
 * Ground truth (desired values) lives here with the fixture — i.e. with the
 * EVALUATOR. The memory engine never sees it.
 */

export interface GuidedFixture {
  rho: number;
  kA: readonly number[];
  kB: readonly number[];
  vA: readonly number[];
  vB: readonly number[];
}

export function clampRho(rho: number): number {
  if (!Number.isFinite(rho)) return 0;
  return Math.min(1, Math.max(0, rho));
}

export function guidedFixture(rhoRaw: number): GuidedFixture {
  const rho = clampRho(rhoRaw);
  return {
    rho,
    kA: [1, 0],
    kB: [rho, Math.sqrt(Math.max(0, 1 - rho * rho))],
    vA: [1, 0],
    vB: [0, 1],
  };
}

export interface Preset {
  id: string;
  label: string;
  description: string;
  rho: number;
  lambda: number;
  /** How many times each of A and B is written (in A,B,A,B… order). */
  repeats: number;
}

/** "Try to break the claim" presets. Each is a full deterministic reset. */
export const PRESETS: readonly Preset[] = [
  {
    id: 'orthogonal',
    label: 'Orthogonal cues',
    description: 'ρ = 0 — the claim predicts exact recall of both associations.',
    rho: 0,
    lambda: 1,
    repeats: 1,
  },
  {
    id: 'partial',
    label: 'Partial overlap',
    description: 'ρ = 0.6 — the claim predicts interference of exactly 0.6 in the off component.',
    rho: 0.6,
    lambda: 1,
    repeats: 1,
  },
  {
    id: 'identical',
    label: 'Identical cues',
    description: 'ρ = 1 — both reads return [1, 1]; the cue cannot distinguish A from B.',
    rho: 1,
    lambda: 1,
    repeats: 1,
  },
  {
    id: 'repeated',
    label: 'Repeated writes',
    description: 'Write A and B three times each (λ = 1): magnitudes triple, shape does not change.',
    rho: 0.3,
    lambda: 1,
    repeats: 3,
  },
  {
    id: 'decay',
    label: 'Decay',
    description: 'λ = 0.5 — earlier writes fade; the newest write keeps full weight.',
    rho: 0.3,
    lambda: 0.5,
    repeats: 1,
  },
] as const;
