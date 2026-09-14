# H2-SHIFT Round 2 submission package (Team Wookies, NIT Warangal)

SRDI Igniters Innovation Challenge 2026, Engineering Track, Option 2: Hydrogen Retrofit Solution.
Research cut-off: 14 September 2026. Built from the official brief (Case Study E-track PDF, 3 pages) and the shortlisted Round 1 deck (4 slides, 16:9).

## Files to submit (deliverables/)

| File | Purpose | Size |
|---|---|---|
| Raunak_TeamWookies_NITWarangal.pptx | Main 10-slide presentation (slide 1 = unchanged Round 1 title slide as the native image; slides 2-10 editable) | 1.2 MB |
| Raunak_TeamWookies_NITWarangal.pdf | Matching PDF export of the main presentation (fonts identical on every machine) | 1.5 MB |
| Raunak_TeamWookies_NITWarangal_Annexure.pdf (+ .docx) | Annexure A1-A10: claim audit, assumptions and 309-entry source register, cost model, packaging and performance, regulatory matrix and hazard analysis, market sizing, benchmarks, pilot design and first 90 days, budget, judge Q&A, validation and change logs | 2.1 MB |
| Raunak_TeamWookies_NITWarangal_Model.xlsx | Formula-driven workbook, 11 sheets, recalculated (scenario selector on Inputs!C3) | 0.1 MB |
| Raunak_TeamWookies_NITWarangal_Model.pdf | PDF export of the workbook for portals that accept only PDF | 0.5 MB |
| Raunak_TeamWookies_NITWarangal_Pitch_Script.pdf (+ .docx) | Three-minute pitch script (379 words, 176 s), timing table, recording layout and export settings | 0.1 MB |
| Raunak_TeamWookies_NITWarangal_QA_Validation_ChangeLog.pdf (+ .docx) | 20 judge questions with answers, validation log, Round 1 to Round 2 change log | 0.1 MB |

Main presentation: 10 slides, PPTX and PDF each below 2 MB (limit 5 MB). Only the team leader may submit.

## Items the team must confirm before uploading

1. Filename stem: the convention is LeaderFirstName_TeamName_InstituteName. The Round 1 deck lists Raunak Jain first but names no leader; the files assume Raunak Jain is the leader. Rename if not.
2. Round 2 deadline and portal fields: the official challenge page (gradpartners.in) was not reachable from the build environment, so the deadline, the annexure field and whether Excel is accepted could not be verified. If only PPT or PDF formats are accepted, upload the Annexure PDF and the Model PDF instead of the workbook.
3. Video: no presenter footage was supplied, so no MP4 exists. Record using the pitch script and layout (split screen or picture-in-picture bottom-right), export H.264 MP4 at 1920 x 1080, verify duration 170-180 s and size below 50 MB.
4. Re-verify entries marked "excerpt" or "summary" in the source register against the original documents where the team has access (ARAI, MoRTH, PESO, PIB, DOE sites were blocked in the build environment).

## Central recommendation (one paragraph)

Hydrogen retrofits of factory-CNG cars can be engineered safely, but no approval route exists and, at any credible delivered hydrogen price to 2032, the conversion costs the owner more than staying on CNG (fuel parity needs about Rs 190/kg; the cheapest 2030 forecast found is about Rs 360/kg). The Round 2 strategy is therefore an option, not a launch: an HCNG step that needs no vehicle change, a 30-car H2-ICE retrofit validation pilot in a captive Faridabad fleet (Rs 37.6 crore over four gated phases), and a 2030 scale decision against explicit price and approval gates. Expected 2030 impact is bounded at about 1,400 cars and 3,600 t CO2e per year, conditional on those gates.


## Redesigned deck (deliverables_v2/): dense, exhibit-led version

Built on 14 Sep 2026 from the same model outputs and source register; numbers are unchanged from v1. Use this version for submission if the exhibit-led style is preferred; v1 (deliverables/) remains available.

| File | Purpose | Size |
|---|---|---|
| deliverables_v2/Raunak_TeamWookies_NITWarangal.pptx | Redesigned 10-slide deck: exact Round 1 title slide; slides 2-10 editable exhibits (log-scale funnel, comparison matrix with status ladder, annotated sedan schematic, hazard and approval matrices, stacked ownership-cost and conversion-cost charts, supply flow and utilisation curves, five-lane Gantt with gates, scorecard and scenario table) | 1.2 MB |
| deliverables_v2/Raunak_TeamWookies_NITWarangal.pdf | Matching PDF export (Liberation Sans embedded; DejaVu Sans for the rupee and subscript glyphs) | 1.5 MB |
| deliverables_v2/Raunak_TeamWookies_NITWarangal_Pitch_Script.pdf (+ .docx) | Pitch script with the storyboard's visual-emphasis column updated to the new exhibits (slide order unchanged) | 0.1 MB |

Redesign map: working/build/redesign_map.md. Generator: working/build/build_deck_v2.py with deck_lib.py (v2 helpers appended). Renders: working/renders_v2/. The annexure, workbook and Q&A files in deliverables/ apply to both versions.

Checks performed on v2: every slide rendered and inspected at presentation size and as a contact sheet; title slide compared pixel-wise with the original render (differences are sub-pixel resampling only); PDF fonts inspected (no substitution beyond the metric-compatible Liberation Sans used on the build machine); slide count 10; both files below 2 MB.

## Working files (working/)

- research/: the four research workstream reports (engineering; safety and regulation; market, infrastructure and benchmarks; economics and emissions) with source registers.
- build/: generators for the workbook (build_workbook.py, model_inputs.py), deck (build_deck.py, deck_lib.py), annexure and pitch (build_annexure.py, build_pitch_qa.py, content.py, docx_lib.py), the parsed source register (sources.json), model outputs (model_outputs_base.json) and the style specification derived from the Round 1 deck.
- inputs/: the official brief, the Round 1 deck, the extracted native title-slide image and the organiser's presenter-layout reference.
- renders/: PNG renders of the ten final slides.

Rebuild: `python3 build_workbook.py && soffice --headless --convert-to xlsx --outdir recalc H2SHIFT_model.xlsx` (recalculate), then `python3 build_deck.py`, `python3 build_annexure.py`, `python3 build_pitch_qa.py`; convert with LibreOffice as in the scripts. Paths inside the scripts point at the build environment's scratchpad and need adjusting.
