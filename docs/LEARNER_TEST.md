# Sixty-second learner test

**Status: PROPOSED PROTOCOL.** As of 2026-09-05, no people have yet been run through this protocol. Nothing below reports actual user feedback; when a session is run, append its results verbatim to the log section at the bottom. (Automated checks — math tests and browser smoke — have run and passed; those are machine verification, not a user study.)

## Protocol (repeatable, one learner, ~60 seconds of interaction)

Setup: open the artifact at its default state (ρ = 0.6 loads pre-populated). Do not coach beyond the script. Timer starts at first interaction.

1. **(0–10 s) Orient.** Say: "This page stores two associations in the small matrix you see. Slide the overlap slider to 0."
2. **(10–25 s) Observe exactness.** Ask Q1: *"Read the two L2 errors. What are they?"* (Expected: both 0.)
3. **(25–45 s) Predict interference.** Say: "Now slide to 0.5 — but first tell me what the retrieved vector for cue A will be." Ask Q2: *prediction.* (Expected: [1, 0.5] or "the other value leaks in by 0.5".) Then let them move the slider and check themselves.
4. **(45–60 s) Name the state.** Ask Q3: *"While you did that, did any trained weights change?"* (Expected: no — there are none; only the matrix state and readouts changed.)

Post-task (untimed, optional): Q4: *"Where does this same write/read appear in BDH?"* (Expected: the synaptic state ρ accumulating LN(Ey)xᵀ per token / "the fast state, not the trained matrices".)

## Scoring key

| Score | Criterion |
|---|---|
| 3 — clicks | Q1 correct, Q2 predicted the leak direction *and* magnitude ρ (any phrasing), Q3 correct |
| 2 — mechanism grasped | Q1 correct, Q2 predicted leak but not magnitude, Q3 correct |
| 1 — partial | Q1 correct, Q2 or Q3 wrong |
| 0 — did not land | Q1 wrong or no engagement |

Q4 is scored separately (BDH module effectiveness): 1 point for naming state-vs-weights correctly in any wording.

Success threshold for the artifact (proposed): median ≥ 2 over ≥ 5 learners from the stated audience, with at least one scoring 3.

## Why these questions

Q1 tests the claim's exact-recall arm; Q2 tests the falsifiable interference arm (the learner can refute the claim here if the app misbehaved); Q3 tests the state/parameter distinction; Q4 tests transfer to BDH — together they cover learning objectives 2, 3 and 5.

## Session log (actual results only — never invented)

*(empty — no sessions run yet)*
