import { useState } from 'react';
import type { SessionState } from '../memory/session';
import { fmt, AssocMark, Badge, Eq, MatrixView } from './primitives';

/**
 * Lesson step 3: where did the extra signal come from? The learner clicks a
 * matrix cell and sees its decomposition into A's and B's contributions,
 * with the interference-producing cells highlighted.
 *
 * Reading with k_A = [1,0] multiplies COLUMN 1 of M by 1 and column 2 by 0,
 * so the interference in component 2 of the readout comes entirely from
 * cell M[2][1] — which is ρ, contributed by B's write.
 */
export default function CrossTerm({ session }: { session: SessionState }) {
  const [sel, setSel] = useState<{ row: number; col: number } | null>({ row: 1, col: 0 });
  const rho = session.fixture.rho;

  // Contribution of each write to each cell (guided mode: one A write, one B write, λ=1).
  const contribA = session.writes.find((w) => w.label === 'A')!.contribution;
  const contribB = session.writes.find((w) => w.label === 'B')!.contribution;

  const cellStory = (row: number, col: number) => {
    const a = contribA[row][col];
    const b = contribB[row][col];
    return { a, b, total: session.matrix[row][col] };
  };

  const story = sel ? cellStory(sel.row, sel.col) : null;

  return (
    <div className="panel">
      <p className="panel-title">
        Point at the interference <Badge kind="live" />
      </p>
      <p>
        Query <AssocMark which="A" /> should return <Eq tex="[1, 0]^{\top}" /> but returns{' '}
        <Eq tex={`[1,\\ ${fmt(rho, 2)}]^{\\top}`} />. Algebraically the read expands to
      </p>
      <Eq
        block
        tex="M k_A \;=\; v_A\,(k_A\!\cdot\!k_A) \;+\; v_B\,\underbrace{(k_B\!\cdot\!k_A)}_{\rho}\;=\; v_A + \rho\, v_B"
        label="M times k A equals v A times k A dot k A plus v B times k B dot k A, which equals v A plus rho times v B"
      />
      <p>
        The extra signal is the <strong>cross term</strong> <Eq tex="\rho\,v_B" /> — association B
        leaking through, scaled by exactly the key overlap. Click the matrix cells to see which
        write put what where. Because the cue is <Eq tex="[1,0]^{\top}" />, the read touches only
        column 1; the highlighted cell is the one that leaks.
      </p>

      <div className="viz-row">
        <MatrixView
          M={session.matrix}
          caption={
            <>
              M — click a cell <span aria-hidden="true">☝</span>
            </>
          }
          highlight={(r, c) => r === 1 && c === 0}
          selected={sel}
          onCellClick={(row, col) => setSel({ row, col })}
        />
        {story && sel && (
          <div>
            <h3>
              Cell M[{sel.row + 1}][{sel.col + 1}] = {fmt(story.total)}
            </h3>
            <table>
              <thead>
                <tr>
                  <th scope="col">write</th>
                  <th scope="col">contribution</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <AssocMark which="A" /> <Eq tex="v_A k_A^{\top}" />
                  </td>
                  <td className="num">{fmt(story.a)}</td>
                </tr>
                <tr>
                  <td>
                    <AssocMark which="B" /> <Eq tex="v_B k_B^{\top}" />
                  </td>
                  <td className="num">{fmt(story.b)}</td>
                </tr>
                <tr>
                  <td>
                    <strong>sum (what M stores)</strong>
                  </td>
                  <td className="num">
                    <strong>{fmt(story.total)}</strong>
                  </td>
                </tr>
              </tbody>
            </table>
            {sel.row === 1 && sel.col === 0 ? (
              <p className="note good" style={{ margin: 0 }}>
                This is it: B wrote ρ = {fmt(rho, 2)} here, and the cue k_A reads this cell at full
                strength. This single number is the interference you saw above.
              </p>
            ) : (
              <p className="note" style={{ margin: 0 }}>
                {sel.col === 1
                  ? 'Cue k_A = [1,0] multiplies this column by 0 — whatever is stored here cannot affect the A-read.'
                  : 'This cell feeds component 1 of the readout — the part that recalls correctly.'}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
