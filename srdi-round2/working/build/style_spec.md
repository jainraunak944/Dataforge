# Working style specification (derived from inspection of the Round 1 PDF, 14 Sep 2026)

Source: "Untitled design (1).pdf" (Canva export, 4 pages, each page a single raster image; no live text, no embedded fonts).

## Dimensions
- Page size 1440 x 810 pt = 20.0 x 11.25 in, aspect 16:9 (Canva 1920x1080 px canvas). Round 2 deck keeps 20 x 11.25 in.
- Native image resolution of page 1: 1376 x 768 px (69 ppi at page size). Title slide is preserved as that native image, unscaled in pixel terms, filling the full slide.

## Sampled colours
Title slide (page 1):
- Background light blue gradient: #93C6EE .. #9ECBF2 (dominant), mid-tone #8BB9DE, darker fringe #315271 (circuit lines).
- Suzuki mark / SUZUKI wordmark blue: #15448C.  Headline navy: #002444 .. #002745.  Team name navy: #00264D.  Member names: #000000.
Content slides (pages 2-4), white background (#FFFFFF):
- Headline black: #000000 / #121212.  Section-header navy: #2C4662; deep navy: #001D57 / #00194C (numbered circles, table headers).
- Dark green (primary accent): #2A765D; deep green: #016F49; darkest green banner: #002D0F / #0B3D2E; donut green #01935E.
- Mint / light green fills: #C3EDD9, #C2ECD8, #DDF1E3, #D2ECD6, #C6EED4, #E5F2EC.
- Greys: panel #E9E9E9 / #E1E6ED, step box #C2C4C3, mid grey #787974, dark grey #3D3D3B.
- Blues: light-blue band #DEE9F5, chart light blue #8CC5FC, tag blue #256B98 / #2877BD.
- Yellow callouts: pale yellow #FFF3B0 (approx; sampled callouts are pale yellow with dark text).

## Typography (observed) and Round 2 mapping
- Observed: condensed bold sans headlines (Bebas/Oswald-like on page 1; Roboto Condensed-like on pages 2-4), humanist sans body (Roboto/Arial-like), serif small caps for TEAM WOOKIES (Times-like). Exact fonts are not recoverable (rasterised export).
- Round 2 new slides use Arial (Bold for headlines) so that PowerPoint, Keynote, LibreOffice and PDF render identically without font substitution; Liberation Sans is the metric-compatible font used for the PDF export on the build machine.
- Hierarchy on 20 x 11.25 in canvas: headline 34-38 pt bold navy (#002444); sub-headline / one-line takeaway 20-22 pt; section header 18-20 pt bold white on navy/green bars; body 18-20 pt (minimum 18 pt for essential labels, 16 pt table cells where dense); captions/footnotes 13-14 pt grey (#3D3D3B). No em dashes.

## Layout grammar (observed)
- Full-width headline at top (finding-based, upper case in R1), one-line sub-headline, then 2-3 column panels with rounded rectangles and a dark header bar per panel.
- Roadmap = chevron band across bottom; impact strip of big numbers; green banner conclusion line.
- Tables: navy header row, white/mint alternating rows, highlighted column for the proposed option (mint).
- Motifs: green check marks, numbered circles (navy), mint call-outs, yellow caution/quote boxes, H2-SHIFT wordmark in green/blue.

## Round 2 grid
- Margins 0.55 in left/right, 0.45 in top/bottom; title band 0.45-1.55 in from top; content zone 1.75-10.35 in; footnote/source line at 10.45-10.95 in (bottom-left, max width 14 in).
- Presenter-safe zone for the video PiP: bottom-right 4.8 in x 4.3 in (24% x 38% of slide, matching the organiser's presenter-layout reference). No essential labels placed there; the pitch storyboard alternatively uses a split layout (deck 76% width left, presenter right column).
