import type { SessionState } from '../memory/session';
import { Badge, Eq } from './primitives';

/**
 * Lesson step 4: distinguish the four kinds of "state". This toy has no
 * training step — the table says so instead of inventing an animated badge.
 */
export default function WhatChanged({ session }: { session: SessionState }) {
  return (
    <div className="panel">
      <p className="panel-title">
        Four things that could be called “memory” — only two changed <Badge kind="live" />
      </p>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">Quantity</th>
              <th scope="col">In this toy</th>
              <th scope="col">Changes when…</th>
              <th scope="col">Changed just now?</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <strong>Current memory</strong> (recurrent state)
              </td>
              <td>
                the 2×2 matrix <Eq tex="M" /> — {session.accounting.coreSlots} numbers
              </td>
              <td>every write: λM + vkᵀ</td>
              <td>Yes — it is {`{`}{session.matrix.map((r) => r.map((x) => x.toFixed(2)).join(', ')).join(' ; ')}{`}`}</td>
            </tr>
            <tr>
              <td>
                <strong>Current activation</strong>
              </td>
              <td>
                the readout <Eq tex="Mq" /> and cue-match scores
              </td>
              <td>every query — recomputed, never stored</td>
              <td>Yes — recomputed on your last slider move</td>
            </tr>
            <tr>
              <td>
                <strong>Encoding convention</strong>
              </td>
              <td>which vectors stand for A and B (the fixture)</td>
              <td>never during the lesson — fixed by design</td>
              <td>No</td>
            </tr>
            <tr>
              <td>
                <strong>Trained weights</strong>
              </td>
              <td>
                <em>none exist</em> — this toy has no training step
              </td>
              <td>would change only under gradient training</td>
              <td>No — there is nothing to change</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p>
        This split is the vocabulary the BDH section needs: in a trained network the analogue of{' '}
        <Eq tex="M" /> is <em>fast</em> state written at inference time, while the parameters that
        decide <em>how</em> to write and read are <em>slow</em> weights learned by training. The
        toy deliberately has only the fast part.
      </p>
    </div>
  );
}
