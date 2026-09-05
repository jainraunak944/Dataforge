import { useState } from 'react';
import { deriveSession } from '../memory/session';
import { fmt, AssocMark, Badge, Eq, VectorView } from './primitives';

/**
 * Lesson step 7: predict before reveal, on a held-out setting (ρ = 0.8,
 * which the guided lesson never lands on by default). Feedback is
 * deterministic — the reveal is a live computation, and the multiple-choice
 * grading is a lookup, not an LLM.
 */

const HELD_OUT_RHO = 0.8;

interface Choice {
  id: string;
  label: string;
  correct: boolean;
  explain: string;
}

const PREDICT_CHOICES: Choice[] = [
  {
    id: 'exact',
    label: '[1.00, 0.00] — recall stays exact',
    correct: false,
    explain:
      'Exact recall needs orthogonal keys (ρ = 0). At ρ = 0.8 the cross term v_B(k_B·k_A) = 0.8·v_B is not zero.',
  },
  {
    id: 'interfered',
    label: '[1.00, 0.80] — the other value leaks in, scaled by ρ',
    correct: true,
    explain: 'Yes: M·k_A = v_A(k_A·k_A) + v_B(k_B·k_A) = v_A + ρ·v_B = [1, 0.8].',
  },
  {
    id: 'avg',
    label: '[0.50, 0.50] — the memory averages the two values',
    correct: false,
    explain:
      'The additive memory does not normalize or average; it sums outer products, and the cue weights each stored value by its key similarity.',
  },
  {
    id: 'blowup',
    label: '[1.80, 1.80] — everything adds up equally',
    correct: false,
    explain:
      'Only at ρ = 1 do both associations contribute fully to both components. At ρ = 0.8 the A-read keeps v_A at weight 1 and lets v_B in at weight 0.8.',
  },
];

const STATE_CHOICES: Choice[] = [
  {
    id: 'matrix',
    label: 'The 2×2 recurrent matrix M (and the readouts computed from it)',
    correct: true,
    explain:
      'Right. Writes changed M; queries recomputed activations. Nothing else changed.',
  },
  {
    id: 'weights',
    label: 'Trained weights were updated by the slider',
    correct: false,
    explain:
      'No trained weights exist in this toy, and nothing here performs gradient training. The slider changes the fixture and M — inference-time state, not parameters.',
  },
  {
    id: 'encoding',
    label: 'The encoding convention (which vector means A)',
    correct: false,
    explain: 'The fixture’s meaning is fixed by design; only ρ rotates k_B.',
  },
];

const LIMIT_CHOICES: Choice[] = [
  {
    id: 'interference',
    label:
      'Overlapping keys contaminate recall — a fixed-size additive state buys constant memory at the price of interference',
    correct: true,
    explain:
      'That is the central limitation this explainer demonstrates, and the motivation for delta-rule and gated variants.',
  },
  {
    id: 'slots',
    label: 'The matrix runs out of empty slots after two writes',
    correct: false,
    explain:
      'There are no slots. Writes superimpose; the failure mode is interference, not slot exhaustion.',
  },
  {
    id: 'nocompute',
    label: 'Reading the memory requires re-running all past writes',
    correct: false,
    explain:
      'Reading is one matrix–vector product on the current state — that is precisely the appeal of the recurrent form.',
  },
];

function QuizQuestion({
  title,
  choices,
  revealed,
  onAnswer,
  answered,
}: {
  title: React.ReactNode;
  choices: Choice[];
  revealed?: React.ReactNode;
  onAnswer?: () => void;
  answered?: string | null;
}) {
  const [picked, setPicked] = useState<string | null>(answered ?? null);
  const pickedChoice = choices.find((c) => c.id === picked);
  return (
    <div style={{ margin: '1.2rem 0' }}>
      <h3>{title}</h3>
      {choices.map((c) => (
        <button
          key={c.id}
          type="button"
          className="quiz-option"
          aria-pressed={picked === c.id}
          onClick={() => {
            setPicked(c.id);
            onAnswer?.();
          }}
        >
          {c.label}
        </button>
      ))}
      {pickedChoice && (
        <div
          className={`quiz-feedback ${pickedChoice.correct ? 'correct' : 'incorrect'}`}
          role="status"
        >
          <strong>{pickedChoice.correct ? 'Correct.' : 'Not quite.'}</strong> {pickedChoice.explain}
        </div>
      )}
      {pickedChoice && revealed}
    </div>
  );
}

export default function ExplainItBack() {
  const [revealed, setRevealed] = useState(false);
  const heldOut = deriveSession({ rho: HELD_OUT_RHO, lambda: 1, repeats: 1 });
  const qa = heldOut.queries[0];

  return (
    <div className="panel">
      <p className="panel-title">
        Predict, then see the computed answer <Badge kind="live" />
      </p>
      <p>
        A setting you have not seen yet: ρ = {fmt(HELD_OUT_RHO, 2)}, λ = 1, one write each. Before
        the app computes anything — what will the memory return for cue <AssocMark which="A" />?
      </p>

      <QuizQuestion
        title={
          <>
            1 · Predict <Eq tex="M\,k_A" /> at ρ = 0.8
          </>
        }
        choices={PREDICT_CHOICES}
        onAnswer={() => setRevealed(true)}
        revealed={
          revealed && (
            <div className="viz-row" style={{ marginTop: '0.8rem' }}>
              <VectorView v={qa.report.retrieved} caption="computed now — retrieved M·k_A" />
              <VectorView v={qa.report.desired} caption="desired" accent="a" />
              <p style={{ alignSelf: 'center' }}>
                L2 error {fmt(qa.report.l2Error)} = ρ. The reveal is a fresh live computation of the
                same memory module, not a stored answer.
              </p>
            </div>
          )
        }
      />

      <QuizQuestion
        title={<>2 · Which state changed while you used this page?</>}
        choices={STATE_CHOICES}
      />

      <QuizQuestion
        title={<>3 · What remains a limitation even when you use decay or more writes?</>}
        choices={LIMIT_CHOICES}
      />
    </div>
  );
}
