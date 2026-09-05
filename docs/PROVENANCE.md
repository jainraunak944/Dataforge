# Provenance — code, data, graphics, fonts, components

## Original work in this repository

| Item | Origin | License |
|---|---|---|
| All application code (`src/`, `tests/`, `scripts/`), all prose in the app and docs, the SVG favicon and unit-circle diagram, all fixtures and test values | written for this submission (with AI assistance — see `docs/AI_DISCLOSURE.md`) | MIT (`LICENSE`) |

## Third-party components (npm, pinned in `package-lock.json`)

| Package | Version | License | Use | Modifications |
|---|---|---|---|---|
| react, react-dom | 18.3.1 | MIT | UI rendering | none |
| katex | 0.16.11 | MIT | equation rendering; its bundled fonts (KaTeX fonts, SIL OFL 1.1) ship in the build | none |
| vite, @vitejs/plugin-react | 5.4.11 / 4.3.4 | MIT | build tooling (dev dependency; not shipped) | none |
| typescript | 5.6.3 | Apache-2.0 | typechecking (dev) | none |
| vitest | 2.1.8 | MIT | tests (dev) | none |
| playwright-core | 1.49.1 | Apache-2.0 | browser smoke test (dev) | none |
| @types/* | pinned | MIT | types (dev) | none |

Transitive dependencies are recorded exactly in `package-lock.json` (committed).

## Fonts

- UI text: system font stacks only (Charter/Georgia serif, system sans, system mono) — nothing bundled or downloaded.
- Equations: KaTeX fonts, bundled from the `katex` npm package, SIL Open Font License 1.1.

## Data and weights

- **No datasets, no model weights, no checkpoints** are used or shipped. All numbers rendered by the app are computed live from the 2×2 toy; all benchmark numbers quoted in text are citations to the papers listed in `docs/RESEARCH.md`.
- The official BDH repository (github.com/pathwaycom/bdh, MIT, © 2025 Pathway Technology, Inc.) was **read** during research to cross-check conventions; **no code from it is used, copied, or adapted** in this project.

## Third-party content quoted

- Short verbatim quotes (≤ 25 words) from arXiv:2509.26507, arXiv:2608.09888, arXiv:2406.06484, arXiv:2412.06464, arXiv:2102.11174 appear in the app, docs and submission PDFs with citation — fair use for scholarship/teaching. Equations are transcribed with equation-number attribution.
- The screenshots in `submission/blog.pdf` and `artifacts/screenshots/` are of this project's own UI.

## Private inputs (not redistributed)

- The DataForge/Pathway organizer brief (`Pathway PS.pdf`) is a private input; it is **not** committed to the repository or included in any public archive.
- Downloaded paper texts used during research are not redistributed; the repo stores our own notes with locators instead.

## Trademarks / names

"BDH", "Dragon Hatchling", "BDH-CQ" and "Pathway" refer to Pathway's published research; this project is an independent educational artifact, not affiliated with or endorsed by Pathway.
