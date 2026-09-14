import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import *
from content import *
SP = "/tmp/claude-0/-home-user-Dataforge/8c3116aa-5914-54b9-9102-e947be44cbb4/scratchpad"
# ---- Pitch script and storyboard
d = new_doc(landscape=False, base_size=10.5)
para(d, "H2-SHIFT Round 2: three-minute video pitch script and recording storyboard", size=16, bold=True, color=NAVY, space_after=2)
para(d, f"{TEAM['team']} | {TEAM['members']} | {TEAM['institute']}", size=10, color=GREY)
words = sum(len(t.split()) for _, _, t, _, _ in PITCH); secs = sum(x for _, x, _, _, _ in PITCH)
para(d, f"Length: {words} spoken words; planned duration {secs} seconds ({secs//60} min {secs%60} s) including pauses, about {round(words/secs*60)} words per minute. Read aloud once with a stopwatch; if it runs over 178 seconds, drop the second sentence of segment 3 (about 20 words).", size=10)
d.add_heading("Script", 2)
for sl, sec_, t, act, vis in PITCH:
    p = d.add_paragraph(); r = p.add_run(f"Slide {sl} ({sec_} s): "); r.bold = True; r.font.color.rgb = GREEN
    p.add_run(t); p.paragraph_format.space_after = Pt(6)
d.add_heading("Timing table", 2)
rows = [["Time window", "Slide", "Spoken words", "Presenter action", "Visual emphasis"]]
t0 = 0
for sl, sec_, t, act, vis in PITCH:
    rows.append([f"{t0//60}:{t0%60:02d} to {(t0+sec_)//60}:{(t0+sec_)%60:02d}", str(sl), str(len(t.split())), act, vis]); t0 += sec_
rows.append(["Total", "", str(words), f"{secs} s", ""])
table(d, rows, widths=[2.6, 1.2, 1.8, 5.6, 6.2], size=9)
d.add_heading("Recording layout and export settings", 2)
bullets(d, [
 "Layout: split screen. The slide occupies the left 76 percent of the frame; the presenter occupies the right column (about 24 percent) with a plain background, so no chart label or table cell is covered. If the organiser's picture-in-picture layout is preferred (presenter bottom-right, about 24 percent wide and 38 percent tall as in the reference image), the deck was built so that footnotes sit bottom-left and only source lines fall under that zone.",
 "Both presenter and solution must be visible throughout; keep the presenter on screen during the title slide and the closing banner.",
 "Slides: use the PDF export (identical fonts on every machine); advance exactly at the timing-table boundaries.",
 "Video: 1920 x 1080, 25 or 30 fps, H.264 (MP4, High profile), 2-pass at 1.8 to 2.2 Mbit/s video; audio AAC 128 kbit/s stereo, 48 kHz; expected file size 40 to 48 MB for 176 s; verify below 50 MB before upload and reduce the video bitrate to 1.6 Mbit/s if needed.",
 "Audio: lapel or USB microphone 30 cm from the mouth, quiet room, record a 5-second silence for noise removal; peak level minus 6 dB.",
 "Check after export: actual duration between 170 and 180 s, file size below 50 MB, slide text legible at 100 percent, audio in sync at the slide changes on slides 4 and 6.",
 "Presenter recording is the remaining input: no video file has been produced; the script, storyboard, layout and export settings are complete.",
], size=10)
d.add_heading("Do-not-say list (keeps the video consistent with the deck)", 2)
bullets(d, ["No 'approved', 'fully safe', 'zero emission' (hydrogen combustion emits NOx), 'partnership' or 'letter of intent'.", "No numbers that are not on the slides; the pitch uses only slide figures rounded for speech.", "Say 'proposed partner' for IOCL, ARAI, fleets and Suzuki R&D Center India."], size=10)
d.save(f"{SP}/v2/Raunak_TeamWookies_NITWarangal_Pitch_Script.docx")
# ---- Q&A and change log
d = new_doc(landscape=False, base_size=10)
para(d, "H2-SHIFT Round 2: judge Q&A, validation log and change log", size=16, bold=True, color=NAVY, space_after=2)
para(d, f"{TEAM['team']} | {TEAM['members']} | {TEAM['institute']} | Research cut-off 14 September 2026", size=10, color=GREY)
d.add_heading("1. Judge Q&A (20 strongest questions)", 2)
for i, (q, a) in enumerate(QA, start=1):
    p = d.add_paragraph(); r = p.add_run(f"{i}. {q}"); r.bold = True; r.font.color.rgb = NAVY; p.paragraph_format.space_after = Pt(1)
    p = d.add_paragraph(a); p.paragraph_format.space_after = Pt(6)
d.add_heading("2. Validation log", 2)
table(d, [["Item", "What was done"]] + [list(r) for r in VALIDATION_LOG], widths=[3.5, 14], size=9, bold_first_col=True)
d.add_heading("3. Change log: Round 1 to Round 2", 2)
table(d, [["Element", "Round 1", "Round 2"]] + [list(r) for r in CHANGE_LOG], widths=[3.2, 7, 7.3], size=9, bold_first_col=True)
d.add_heading("4. Internal review framework (our own, not the organiser's scoring)", 2)
para(d, "We reviewed the deck as an automotive R&D engineer (physics, packaging, power, NOx), a fleet operator (downtime, boot, refuelling, cost per km), a type-approval specialist (route, standards, evidence), a finance reviewer (fair TCO, no double counting, discounting) and a competition judge (answers the brief, builds on Round 1, honest). Corrections made during review: fallback fuel changed to petrol; kit cost raised; pump-price basis; payback claim withdrawn; roadmap and impact rebased; AIS-157 versus AIS-195 corrected; HiAce versus Hilux corrected; job claim removed. Official scoring weights were not published to us and are not assumed.", size=10)
para(d, TEAM["leader_note"], size=9.5, italic=True, color=GREY)
d.save(f"{SP}/v2/Raunak_TeamWookies_NITWarangal_QA_Validation_ChangeLog.docx")
print("saved pitch and QA docs")
