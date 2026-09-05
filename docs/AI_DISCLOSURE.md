# AI assistance disclosure

This disclosure is mirrored in the README, as the brief requires.

## What was AI-assisted

This project was built with **Claude Code** (Anthropic), operating as an implementation assistant in a cloud session on 2026-09-05, directed by the team's build brief. Concretely, AI assistance produced, under the team's instructions and review:

- All application and test code in this repository (`src/`, `tests/`, `scripts/`).
- All documentation and submission prose (docs/, README, submission PDFs), from the team-approved outline: the central claim, fixture, lesson sequence, honesty rules and packaging choices were specified in the team's written brief that the assistant executed.
- The research verification workflow: AI agents fetched the primary papers live and produced `docs/research-notes/` with exact locators; every scientific claim in the artifact traces to those verified notes (`docs/RESEARCH.md`), not to model memory.

## What was NOT AI-generated

- The competition brief and its requirements (organizer's document).
- The primary sources (papers by their respective authors, cited throughout).
- Third-party components listed in `docs/PROVENANCE.md`.

## Reused / forked work

None. This repository is not a fork; no external application code was copied or adapted. The official BDH repo was read for convention-checking only (see PROVENANCE).

## Mentors and contributors

No mentors or additional contributors are declared for this work at the time of writing. (Per our rules, none are invented; if mentorship occurs before submission, it must be added here and in the README.)

## Ownership commitment

The registered team is responsible for understanding and defending every component. `docs/DEFENSE_GUIDE.md` exists precisely to make that real: a plain-English walkthrough of every file, worked examples by hand, and the likely judge questions. Per the brief, teams must be able to explain every claim, sentence and citation — the claim-to-source ledger in `docs/RESEARCH.md` maps each one to its exact locator so any team member can re-verify it from the primary source.
