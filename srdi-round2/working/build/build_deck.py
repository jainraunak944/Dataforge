"""Builds the 10-slide Round 2 deck. Slide 1 = exact Round 1 title asset; slides 2-10 editable, numbers from model_outputs_base.json."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from deck_lib import *
SP = "/tmp/claude-0/-home-user-Dataforge/8c3116aa-5914-54b9-9102-e947be44cbb4/scratchpad"
O = json.load(open(f"{SP}/out/model_outputs_base.json"))
S, E, H, M, EM, B, PB, IN = O["S"], O["ER"], O["H2S"], O["MK"], O["EM"], O["BOM"], O["PB"], O["INPUTS"]
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SP}/out/Raunak_TeamWookies_NITWarangal.pptx"

def L(x, d=1):  # rupees to lakh string
    return f"{x/1e5:.{d}f}"
def cr(x, d=1):
    return f"{x/1e7:.{d}f}"
def n0(x): return f"{x:,.0f}"

prs = new_presentation()
# ---------------------------------------------------------------- Slide 1 (exact)
add_title_slide(prs, f"{SP}/assets/r1page-000.png")

# ---------------------------------------------------------------- Slide 2
s = blank_slide(prs)
y0 = header(s, "Recommendation: validate before selling. A 30-car hydrogen retrofit pilot in a captive Faridabad fleet, scaled only if delivered hydrogen falls below about ₹190 per kg",
            "Answer to the brief: a CNG-to-hydrogen retrofit can be made safe by 2030, but at unsubsidised hydrogen prices it is not affordable; its 2030 role is a policy-supported niche of about 1,400 cars, not a mass product.")
colw = Inches(6.1); gap = Inches(0.25); x1 = MARGIN; x2 = x1 + colw + gap; x3 = x2 + colw + gap
ph = Inches(6.3)
bx, by, bw, bh = panel(s, x1, y0, colw, ph, "1. THE ANSWER TO THE BRIEF'S QUESTION")
textbox(s, bx, by, bw, bh, [
    ("**Safe:** yes, with known engineering (composite cylinder, thermally activated relief, twin leak sensors, lean burn with NOx control). But no approval route exists today for a hydrogen retrofit of a car; creating one is gate 1.", {'bullet': True}),
    (f"**Affordable:** not by 2030. At ₹{IN['h2_price_y1']['active']:.0f}/kg delivered (2028) the converted car costs ₹{S['lcB']:.1f}/km all-in versus ₹{S['lcA']:.1f}/km on CNG. Fuel parity with CNG needs ₹{S['parity_cng']:.0f}/kg; the cheapest 2030 forecast found is about ₹360/kg delivered.", {'bullet': True}),
    (f"**Viable complement:** only as a captive-fleet niche next to hydrogen hubs. A compact BEV bought in 2028 comes to ₹{S['lcC']:.1f}/km including purchase, so BEVs stay the economic default for high-utilisation fleets.", {'bullet': True}),
    ("**So the strategy is an option, not a launch:** an HCNG step that needs no vehicle change, a bounded H2-ICE retrofit pilot that creates the approval route and the data, and a scale decision in 2030 against explicit price gates.", {'bullet': True}),
], size=16, line_spacing=1.05, space_after=6)
bx, by, bw, bh = panel(s, x2, y0, colw, ph, "2. FIRST CUSTOMER AND USE CASE", fill=GREEN)
textbox(s, bx, by, bw, bh, [
    ("**Donor:** Maruti Suzuki Dzire Tour S CNG, 3 to 5 years old, factory bi-fuel; petrol stays as the automatic backup fuel.", {'bullet': True}),
    ("**Fleet:** captive, return-to-base institutional and contract fleets (PSU and corporate staff transport, airport contracts) in Faridabad, Delhi-NCR, running 150 to 210 km per day with two depot fills.", {'bullet': True}),
    ("**Why here:** IOCL R&D Faridabad hosts India's only car-capable hydrogen dispensing point, and the MNRE Sahibabad-Faridabad-Delhi hydrogen corridor (sanctioned March 2025) brings buses and trucks that a shared station needs.", {'bullet': True}),
    ("**Why not Delhi app-cabs first:** the 2023 aggregator scheme counts only electric cars toward onboarding ratios, and CAQM allows only CNG or EV new aggregator vehicles in NCR from January 2026. A hydrogen conversion earns no credit there.", {'bullet': True}),
    ("**Second hub:** Ahmedabad-Vadodara-Surat corridor (Gujarat funds 30 percent of the first 20 hydrogen stations).", {'bullet': True}),
], size=15.5, line_spacing=1.05, space_after=6)
bx, by, bw, bh = panel(s, x3, y0, colw, ph, "3. HOW BIG, HONESTLY (bottom-up, 2030)")
fun = M["funnel"]
rows = [["Step", "Vehicles"]]
labels = ["CNG vehicles on road, Mar 2025 (all types)", "Passenger cars among them (estimate)", "Factory-fitted, boot cylinder, under 6 yr in 2028", "In commercial or institutional fleets", "In cities with a hydrogen hub by 2030", "Plausible early adopters (hypothesis)", "Station-limited capacity: 8 hubs x 174 cars", "Realistic converted fleet by 2030"]
for lab, (a, b) in zip(labels, fun[:8]):
    rows.append([lab, n0(b)])
table(s, bx, by, bw, Inches(4.25), rows, col_widths=[3.2, 1.1], font_size=13.5, header_size=13.5, row_fills={8: MINT2}, bold_rows=(8,))
textbox(s, bx, by + Inches(4.35), bw, Inches(1.2), [
    "Round 1 said 1,00,000 cars by 2030. Stations, not demand, set the ceiling: one 500 kg/day hub at 70 percent utilisation serves about 174 cars.",
    "Customer demand is a hypothesis: no fleet interviews exist yet; Phase 0 buys 30 of them."], size=13.5, color=DARKGREY, line_spacing=1.05, space_after=3)
shp = rect(s, MARGIN, Inches(8.8), SLIDE_W - 2 * MARGIN, Inches(0.95), DARKGREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
shape_text(shp, "Same idea as Round 1: convert the installed CNG base, fleets first, aggregate hydrogen demand at hubs. What changed: pump price instead of production cost, petrol backup instead of a second cylinder, a station-limited rollout, and explicit stop rules.", size=16, color=WHITE, bold=True, align=PP_ALIGN.LEFT, margins=(0.3, 0.05, 0.3, 0.05))
textbox(s, MARGIN, Inches(9.85), Inches(19), Inches(0.6), "Evidence labels used throughout: verified = external source in the register; model = workbook output; assumption = stated input range; target = proposed value requiring validation.", size=12.5, color=MIDGREY, space_after=0)
footer(s, "Sources: PNGRB/Vahan 81.95 lakh CNG vehicles, Aug 2025 [W3-S2]; Delhi aggregator scheme 2023 [W3-S17]; CAQM NCR direction [W3-S19]; IOCL Faridabad dispensing [W3-S46]; MNRE pilot routes, PIB 3 Mar 2025 [W3-S36]; Gujarat Green Hydrogen Policy [W4-S76]; CEEW 2025 delivered cost [W4-S22]; model workbook (TCO, Market).", 2)

# ---------------------------------------------------------------- Slide 3
s = blank_slide(prs)
y0 = header(s, "H2-ICE is the only conversion at conversion cost, but it carries the weakest fuel economics; a fuel-cell conversion costs as much as a new BEV",
            "Matched criteria for the same donor and duty (Dzire Tour S CNG, 55,000 km per year, owner decision in 2028). Values are model outputs unless a source is named.")
tw = Inches(12.6)
rows = [["Criterion", "H2-ICE retrofit (selected)", "Fuel-cell conversion", "New compact BEV (donor sold)", "Continue on CNG"],
 ["What changes", "Cylinder, lines, injectors, ECU, sensors; engine and petrol system retained", "Whole powertrain: stack, battery, motor, inverter, cooling, tank, controls", "New vehicle; donor sold for about ₹3.5 lakh", "Nothing"],
 ["Cost to the owner", f"₹{L(B['volume'])} lakh installed at 10,000/yr; ₹{L(B['pilot'])} lakh in the pilot", "₹15 to 25 lakh pilot; ₹8 to 12 lakh at volume (estimate)", f"₹{L(IN['bev_price']['active'])} lakh purchase (Tiago EV to Punch EV class)", "0"],
 ["Energy cost per km, 2028", f"₹{S['fkm_B']:.1f} blended (hydrogen km ₹{S['fkm_h2']:.1f} at ₹{IN['h2_price_y1']['active']:.0f}/kg)", "About half of H2-ICE per hydrogen km", f"₹{S['fkm_bev']:.1f} (depot and public mix)", f"₹{S['fkm_A']:.1f}"],
 ["Range per fill or charge", f"{E['range']:.0f} km on hydrogen plus {E['petrolrange']:.0f} km on petrol", "About 2x H2-ICE on the same tank", "187 to 260 km in real-world tests", "About 250 km at 25 km/kg"],
 ["Refuel or recharge time", "3 to 5 min (350 bar, non-cooled fill)", "3 to 5 min", "About 1 h DC (10 to 80 percent); 6 to 8 h AC", "3 to 5 min plus queue"],
 ["Peak power versus petrol", f"About {IN['h2_power_factor']['active']*100:.0f} percent (lean burn); city duty", "Restored by electric drive", "Higher", "About 85 percent"],
 ["Tailpipe", "Zero CO2 on hydrogen km; NOx must be controlled", "Water vapour only", "Zero", "About 105 g CO2/km"],
 ["Approval route today", "None for retrofits; AIS-195 covers new H2-ICE vehicles", "None; AIS-157 scope excludes retrofitted or converted FCEVs", "Established", "Established"],
 ["Supplier readiness", "Injectors, valves, regulators production-intent; car-size cylinders scarce", "Imported stacks; no light-duty supply chain in India", "Mature", "Mature"],
]
table(s, MARGIN, y0, tw, Inches(6.4), rows, col_widths=[1.5, 2.3, 2.1, 2.0, 1.5], font_size=12, header_size=13, highlight_col=1, align_center_from=99)
px = MARGIN + tw + Inches(0.25); pw = SLIDE_W - MARGIN - px
bx, by, bw, bh = panel(s, px, y0, pw, Inches(6.9), "WHAT GLOBAL EXPERIENCE TEACHES", fill=GREEN)
textbox(s, bx, by, bw, bh, [
    ("**Captive fleets with depot fuelling survive:** KEYOU truck conversions (Germany, 2024 to 2027 with Daimler), ULEMCo van conversions (UK), Toyota's hydrogen HiAce at its Altona depot (2024), NTPC Leh buses (80 kg/day, 350 bar).", {'bullet': True}),
    ("**Retail light-duty networks retreat:** Shell closed its 7 California car stations (Feb 2024); H2 Mobility closed 36 German car stations (2025); Stellantis cancelled its hydrogen vans (Jul 2025); Toyota sold 210 Mirai in the US in 2025.", {'bullet': True}),
    ("**H2-ICE momentum is heavy-duty:** JCB EU type approval (May 2025); Cummins B6.7H built in Jamshedpur for Tata trucks (Mar 2025); 70 MNRE pilot vehicles are buses and trucks, zero cars.", {'bullet': True}),
    ("**Small-car hydrogen combustion is live but pre-commercial:** Suzuki and AVL hydrogen Swift prototype (1.4 L direct injection, 100 kW, Vienna, May 2026); Suzuki hydrogen Burgman (2023, 2025). No company sells a passenger-car hydrogen conversion anywhere.", {'bullet': True}),
    ("**Transfer to India:** design for a depot, not a network; treat fuel price as the gating variable; borrow heavy-duty supplier parts; do not cite prototypes as proof of cost.", {'bullet': True}),
], size=14.5, line_spacing=1.06, space_after=6)
callout(s, MARGIN, Inches(9.35), Inches(19), Inches(0.8), "Selected route: H2-ICE with port injection, lean burn and automatic petrol fallback. It is the only architecture that is a retrofit in cost and scope; its case rests entirely on the delivered hydrogen price, so the pilot is designed to measure exactly that.", fill=MINT, size=15, bold=True, color=DARKGREEN)
footer(s, "Sources: KEYOU, ULEMCo, Toyota Australia, NTPC [W3-S61, S63, S55, S44]; Shell, H2 Mobility, Stellantis, Toyota sales [W3-S65, S66, S64, S51]; JCB, Cummins, MNRE pilots [W3-S60, S59, S37]; Suzuki-AVL Swift (Fuel Cells Works, 7 May 2026), Burgman [W3-S58]; AIS-157 scope [W2-S11 and Scribd copy]; BEV data [W3-S27, S30]; fuel-cell conversion costs are estimates.", 3)

# ---------------------------------------------------------------- Slide 4
s = blank_slide(prs)
y0 = header(s, "What the retrofit changes: storage, fuel delivery, controls and safety are new; the engine, petrol system and body are retained (concept, to be verified by mock-up)",
            "Donor: Maruti Suzuki Dzire Tour S CNG, 1.2 L K-series, 60 kW on petrol, 55 L steel CNG cylinder in the boot, 37 L petrol tank, 163 mm ground clearance (no under-floor cylinder option).")
# diagram
dx = MARGIN; dy = y0; dw = Inches(9.2); dh = Inches(4.65)
rect(s, dx, dy, dw, dh, RGBColor(0xF6, 0xF7, 0xF8), line=GREY2, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
textbox(s, dx + Inches(0.15), dy + Inches(0.05), dw, Inches(0.4), "System architecture (schematic, not to scale). Green = new, blue = retained, grey = removed.", size=13, color=DARKGREY, bold=True, space_after=0)
def box(x, y, w, h, text, fill, color=WHITE, size=12.5):
    shp = rect(s, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    shape_text(shp, text, size=size, color=color, bold=True, margins=(0.06, 0.03, 0.06, 0.03))
    return shp
bw_ = Inches(1.75); bh_ = Inches(0.95); r1y = dy + Inches(0.5); r2y = dy + Inches(1.85); r3y = dy + Inches(3.3)
xs = [dx + Inches(0.2) + i * (bw_ + Inches(0.42)) for i in range(4)]
box(xs[0], r1y, bw_, bh_, "H35 receptacle, check valve, filter (new)", GREEN)
box(xs[1], r1y, bw_, bh_, "60 L composite cylinder, 350 bar, OTV with TPRD, boot frame (new)", GREEN, size=11.5)
box(xs[2], r1y, bw_, bh_, "316L high-pressure line, two-stage regulator (new)", GREEN)
box(xs[3], r1y, bw_, bh_, "Hydrogen rail and 4 port injectors (new)", GREEN)
for i in range(3):
    arrow(s, xs[i] + bw_, r1y + bh_ // 2, xs[i + 1], r1y + bh_ // 2, color=DARKGREEN, width=2.5)
box(xs[3], r2y, bw_, bh_, "1.2 L K-series engine, gearbox, three-way catalyst (retained)", TAGBLUE, size=11.5)
arrow(s, xs[3] + bw_ // 2, r1y + bh_, xs[3] + bw_ // 2, r2y, color=DARKGREEN, width=2.5)
box(xs[2], r2y, bw_, bh_, "Petrol tank 37 L and petrol injection (retained, automatic backup)", TAGBLUE, size=11.5)
arrow(s, xs[2] + bw_, r2y + bh_ // 2, xs[3], r2y + bh_ // 2, color=TAGBLUE, width=2.5)
box(xs[1], r2y, bw_, bh_, "Hydrogen ECU: dual map, lambda 1.6 to 2.2, fallback logic, diagnostics (new)", GREEN, size=11.5)
arrow(s, xs[1] + bw_, r2y + bh_ // 2, xs[2], r2y + bh_ // 2, color=DARKGREEN, width=2.5)
box(xs[0], r2y, bw_, bh_, "Twin hydrogen sensors, boot vent fan, cabin warning, manual shut-off (new)", GREEN, size=11.5)
arrow(s, xs[0] + bw_, r2y + bh_ // 2, xs[1], r2y + bh_ // 2, color=DARKGREEN, width=2.5)
box(xs[0], r3y, bw_, bh_, "TPRD vent line to outside, sealed boot bulkhead (new)", GREEN, size=12)
box(xs[1], r3y, bw_, bh_, "Lean NOx trap provision and lambda sensor (new, if cycle test needs it)", GREEN, size=11.5)
box(xs[2], r3y, bw_, bh_, "55 L steel CNG cylinder, CNG regulator, rail, lines (removed, not reusable)", MIDGREY, size=11.5)
box(xs[3], r3y, bw_, bh_, "Cold plugs, PCV route, calibration (modified)", NAVY2, size=12)
# right side: stat tiles and table
rx = dx + dw + Inches(0.25); rw = SLIDE_W - MARGIN - rx
tiles = [
 (f"{E['usable']:.2f} kg", f"usable hydrogen per fill (1.44 kg nominal at 350 bar, 85 percent fill, 20 bar residual)"),
 (f"{E['range']:.0f} km", f"range per fill at {IN['h2_cons']['active']:.2f} kg/100 km; {E['range700']:.0f} km with a 700 bar cylinder of the same size"),
 (f"~{E['usable']*2/ (IN['h2_cons']['active']/100):.0f} km/day", f"on hydrogen with two depot fills ({E['maxshare']*100:.0f} percent of a 167 km day); petrol covers the rest"),
 (f"{E['h2ps']:.0f} PS", f"peak power in hydrogen mode, {100*(1-IN['h2_power_factor']['active']):.0f} percent below petrol; city duty, automatic petrol switch at high load"),
 (f"{E['netmass']:+.0f} kg", "net kerb mass change; cylinder is 84 mm larger in diameter, so the boot loses a further 40 to 60 L (estimate)"),
 ("3 days", "conversion downtime per car in the pilot; 14 labour hours at volume"),
]
tx = rx; tyy = y0; tw_ = (rw - Inches(0.2)) / 2; th_ = Inches(1.42)
for i, (v, lab) in enumerate(tiles):
    cx = tx + (i % 2) * (tw_ + Inches(0.2)); cy = tyy + (i // 2) * (th_ + Inches(0.18))
    stat_tile(s, cx, cy, tw_, th_, v, lab, value_size=26, label_size=12.5)
# lower table
ty2 = y0 + dh + Inches(0.2)
rows = [["Retained", "Modified", "Removed (cannot be reused with hydrogen)", "Added"],
        ["Engine, gearbox, body, brakes, suspension, petrol tank and injection, three-way catalyst, CNG-hardened valve seats",
         "Calibration (lean lambda 1.6 to 2.2, retarded spark, injection timed after intake valve closing to stop backfire), cold-grade plugs, crankcase ventilation, boot bulkhead sealing and ventilation",
         "55 L steel CNG cylinder (ISO 11439 steel is limited to 2 percent hydrogen), CNG regulator, rail, injectors, hoses and lines",
         "Composite cylinder (60 L, OD 400 x 767 mm, 36 kg), on-tank valve with TPRD, H35 receptacle, 316L lines, two-stage regulator, hydrogen injectors and rail, hydrogen ECU, two sensors, vent fan, lean NOx trap provision"]]
table(s, MARGIN, ty2, SLIDE_W - 2 * MARGIN, Inches(2.0), rows, col_widths=[1, 1.2, 1.1, 1.4], font_size=12, header_size=13, align_center_from=99, first_col_bold=False, row_heights=[Inches(0.38), Inches(1.6)])
callout(s, MARGIN, Inches(9.45), Inches(19), Inches(0.72), "Injection strategy: port injection with late timing and lean mixtures avoids backfire and pre-ignition but costs power; direct injection (as in the Suzuki-AVL Swift prototype) recovers it but is not a retrofit. Durability items to prove: valve seats and guides, lubricant ash, sensor drift. Consumption cross-check: 1.85 kg/100 km equals 0.87 of the CNG car's energy efficiency at 25 km/kg.", fill=YELLOW, size=13)
footer(s, "Sources: Maruti Suzuki Tour S and Dzire specifications [W1-S3a to S3c]; Luxfer G-Stor Pro V060H35 [W1-S2]; hydrogen densities 24.0 and 40.2 g/L at 15 C [W1-S13a]; PFI power loss and lambda-NOx behaviour [W1-S9a, S9b, S9h]; ISO 11439 hydrogen limit [W1-S11a]; UN R110 20 g / 8 g mounting loads [W1-S14d]; model workbook (Energy_Range, BOM).", 4)

# ---------------------------------------------------------------- Slide 5
s = blank_slide(prs)
y0 = header(s, "Safety: the hazards are known and controllable; approval is the real gap, because no route exists yet for a hydrogen retrofit of a car",
            "Hydrogen ignites between 4 and 75 percent in air at 0.017 mJ, diffuses 3.8 times faster than natural gas and burns almost invisibly: different risks, not automatically higher, if designed for.")
rows = [["Hazard", "Prevention (design)", "Detection and response", "Validation evidence"],
 ["Leak into boot, cabin, garage or basement", "Sealed boot bulkhead, vented boot, no ignition sources in the bay, valve closed when engine off", "Two hydrogen sensors (alarm at 1 and 2 percent), tank valve closes within 1 s, ECU switches to petrol, driver warning", "Concentration below 4 percent in cabin and below 8 percent at vents (GTR 13 / AIS-195 type tests); enclosed-space test"],
 ["Embrittlement, permeation, material ageing", "Hydrogen-rated 316L lines, elastomers and composite liner; no reuse of CNG steel parts", "3-yearly cylinder requalification (Gas Cylinder Rules 2025), 15-year life, leak check at service", "Supplier qualification to ISO 19881 / UN R134; cycling and permeation tests"],
 ["Crash damage", "Cylinder behind rear seat inside the crush-free zone; frame designed to 20 g / 8 g loads", "Inertia switch closes the tank valve; post-crash leak limit", "Sled test of the mounting, full-vehicle rear crash under AIS-195 procedures"],
 ["Overpressure and fire", "TPRD vents away from occupants, wheel wells and electrics; burst ratio 2.25 x working pressure", "TPRD opens on heat; controlled release rather than rupture", "Bonfire, burst, drop and cycling tests (GTR 13); vent-line routing review"],
 ["Detection or control failure", "Redundant sensors, ECU watchdog, manual shut-off valve, limp-home on petrol", "Fault codes, forced petrol mode, service lock-out", "Hardware-in-the-loop and fault-injection tests; 500 h engine durability"],
 ["Workshop and refuelling incidents", "NFPA 2 type ventilation (1 cfm per sq ft), hydrogen detection, permit-to-work, PESO-trained staff", "Gas detection interlocks on the dispenser and in the bay; nitrogen purge for venting", "PESO Form-H licence for the dispensing point; SAE J2601 fill protocol; lessons from Kjørbo 2019 (assembly error) and Santa Clara 2019 (procedures)"],
]
table(s, MARGIN, y0, Inches(12.3), Inches(6.3), rows, col_widths=[1.15, 1.75, 1.75, 1.85], font_size=11.5, header_size=12.5, align_center_from=99)
px = MARGIN + Inches(12.3) + Inches(0.25); pw = SLIDE_W - MARGIN - px
bx, by, bw, bh = panel(s, px, y0, pw, Inches(6.3), "APPROVAL PATH AND OPEN QUESTIONS", fill=NAVY2)
textbox(s, bx, by, bw, bh, [
    ("**Exists:** AIS-195:2023 (Amd 1, May 2025) for new M and N hydrogen ICE vehicles via CMVR Rule 125M (GSR 746(E), 16 Oct 2023).", {'bullet': True}),
    ("**Exists in principle:** MV Act s.52 and CMVR Rule 126 proviso (retrofitted vehicles tested and type-approved by test agencies) plus the Rule 115 CNG-kit machinery: kit type approval, authorised workshops, RC endorsement (Form 22D).", {'bullet': True}),
    ("**Gap:** no hydrogen retrofit kit standard or emission procedure; AIS-157 explicitly excludes retrofitted or converted fuel-cell vehicles; the AIS-195 position on retrofits could not be verified (document inaccessible in this study).", {'bullet': True}),
    ("**Cylinders and stations:** Gas Cylinder Rules 2025 now cover on-board hydrogen cylinders; PESO Form-H licences for dispensing online since May 2025; no car-size PESO-approved cylinder yet.", {'bullet': True}),
    ("**Trial route:** trade certificate plus test-agency evaluation, as used for the ICAT Mirai pilot (2022) and the Tata truck trials (2025); the MNRE transport pilot scheme names 4-wheelers.", {'bullet': True}),
    ("**Insurance and warranty:** IMT-25 covers only CNG and LPG kits; OEM warranty is void after conversion. Both need new instruments.", {'bullet': True}),
], size=13, line_spacing=1.04, space_after=5)
callout(s, MARGIN, Inches(8.85), Inches(12.3), Inches(1.3), "NOx: hydrogen combustion still forms thermal NOx (US DOE). Lean burn above lambda 2 keeps engine-out NOx near zero at steady state, but accelerations leave that regime, so the design carries a lean NOx trap provision and must meet BS-VI 60 mg/km on the certification cycle. This is a target to demonstrate, not a result.", fill=YELLOW, size=13.5)
callout(s, px, Inches(8.85), pw, Inches(1.3), "We do not claim 'approved' or 'fully safe'. Gate 1 (March 2027): a written regulator and test-agency view on the retrofit route, or the programme stops.", fill=MINT, size=14, bold=True, color=DARKGREEN)
footer(s, "Sources: H2Tools hydrogen properties [W2-S43]; DOE 'Similar but Different' [W2-S44]; NFPA 2 [W2-S45]; GTR 13 limits [W2-S42]; Gas Cylinder Rules 2025, GSR 225(E) [W2-S24]; PESO Form-H [W2-S27]; GSR 746(E) Rule 125M [W2-S13]; Rule 126 and Rule 115 [W2-S9, S3]; AIS-157 scope [W2-S11, Scribd copy]; IMT-25 [W2-S53]; incidents [W2-S48, S49]; DOE NOx page [W2-S52].", 5)

# ---------------------------------------------------------------- Slide 6
s = blank_slide(prs)
y0 = header(s, "Economics: at every credible hydrogen price to 2032 the retrofit costs the owner more than staying on CNG; the sign never turns",
            "Fair comparison for an owner deciding in 2028 with a 3-year-old Dzire Tour S CNG: keep it, convert it, or sell it and buy a compact BEV. Five years, 55,000 km per year, 12 percent discount rate, unsubsidised, same time costs for queues and charging.")
ch = bar_chart(s, MARGIN, y0, Inches(7.4), Inches(4.6), ["Continue on CNG", "Hydrogen retrofit", "Sell, buy compact BEV"],
               [("Fuel or energy, ₹/km (2028)", (round(S['fkm_A'], 2), round(S['fkm_B'], 2), round(S['fkm_bev'], 2))), ("All-in levelised cost, ₹/km", (round(S['lcA'], 2), round(S['lcB'], 2), round(S['lcC'], 2)))],
               [CHARTBLUE, GREEN], number_format='0.0', font_size=12, value_axis_title="₹ per km", label_size=12, title="Cost per km, base case (model)")
textbox(s, MARGIN, y0 + Inches(4.65), Inches(7.4), Inches(1.1), [
    f"Five-year NPV of costs: continue ₹{L(S['npvA'])} lakh; retrofit ₹{L(S['npvB'])} lakh; BEV ₹{L(S['npvC'])} lakh (donor sale of ₹{L(IN['donor_value_now']['active'])} lakh and BEV resale credited).",
    f"Hydrogen at ₹{IN['h2_price_y1']['active']:.0f}/kg in 2028 falling 10 percent a year; CNG ₹{IN['cng_price']['active']:.0f}/kg; petrol ₹{IN['petrol_price']['active']:.0f}/L; depot power ₹{IN['depot_tariff']['active']:.0f}/kWh, public DC ₹{IN['pub_tariff']['active']:.0f}/kWh."], size=13, color=DARKGREY, line_spacing=1.05, space_after=3)
# conditions table
cx = MARGIN + Inches(7.65); cw = Inches(5.9)
rows = [["Condition for competitiveness", "Value (model)"],
 ["Fuel-cost parity with CNG (₹/kg delivered)", f"₹{S['parity_cng']:.0f}"],
 ["Fuel-cost parity with petrol (₹/kg)", f"₹{S['parity_petrol']:.0f}"],
 ["Full-TCO break-even versus continuing on CNG", "None within 5 years at any hydrogen price: kit cost and petrol backup km outweigh the fuel saving"],
 ["Full-TCO break-even versus the BEV", "None at base; needs hydrogen below about ₹150/kg with a ₹2 lakh kit and 85 percent hydrogen km"],
 ["Conversion cost", f"₹{L(B['pilot'])} lakh pilot; ₹{L(B['volume'])} lakh installed at 10,000/yr (₹2.3 lakh ex-works). Round 1 said ₹1.8 to 2.2 lakh"],
 ["Extra cost of converting versus continuing (5 yr)", f"₹{L(S['dBA'])} lakh at base; ₹5.8 lakh even at ₹250/kg hydrogen"],
 ["Abatement cost versus continuing", f"₹{EM['abate']/1000:.0f},000 per t CO2e at base; about ₹45,000/t at ₹250/kg (India voluntary credits trade at ₹1,350 to 2,800/t)"],
]
table(s, cx, y0, cw, Inches(5.8), rows, col_widths=[1.5, 1.9], font_size=12.5, header_size=13, align_center_from=99)
# heat grid
gx = cx + cw + Inches(0.25); gw = SLIDE_W - MARGIN - gx
textbox(s, gx, y0, gw, Inches(0.5), "Extra cost of the retrofit versus continuing on CNG over 5 years, ₹ lakh (model)", size=13, bold=True, color=DEEPNAVY, space_after=0)
g1 = O["SENS"]["grid1"]
hdrrow = g1[0]; kmcols = [1, 3, 5]  # 30k, 50k, 70k
rows = [["₹/kg \\ km/yr"] + [n0(hdrrow[c]) for c in kmcols]]
sel = [r for r in g1[1:] if r[0] in (150, 250, 400, 600, 800)]
for r in sel:
    rows.append([f"₹{r[0]:.0f}"] + [f"+{r[c]:.1f}" for c in kmcols])
tb = table(s, gx, y0 + Inches(0.5), gw, Inches(3.3), rows, col_widths=[1.2, 1, 1, 1], font_size=13, header_size=12.5)
# colour cells
def heat(vv):
    vv = max(0, min(22, vv))
    t = vv / 22
    r_ = int(0xC3 + (0xE0 - 0xC3) * t); g_ = int(0xED - (0xED - 0x7A) * t); b_ = int(0xD9 - (0xD9 - 0x66) * t)
    return RGBColor(r_, g_, b_)
for i, r in enumerate(sel, start=1):
    for j, c in enumerate(kmcols, start=1):
        cell = tb.cell(i, j); cell.fill.solid(); cell.fill.fore_color.rgb = heat(r[c])
textbox(s, gx, y0 + Inches(3.9), gw, Inches(1.9), ["Every cell is positive: the conversion never saves money against CNG in this horizon. Higher mileage makes it worse while hydrogen is dearer than ₹188/kg.",
        "Against a petrol-only donor, fuel parity sits at ₹368/kg, inside the 2030 forecast range, but a ₹60,000 CNG conversion beats it wherever CNG exists. LNG passenger cars do not exist in India."], size=12.5, color=DARKGREY, line_spacing=1.05, space_after=3)
callout(s, MARGIN, Inches(9.05), Inches(19), Inches(0.8), "Reading: the retrofit is a decarbonisation cost, not a saving. It needs a paying counterparty (policy or a corporate abatement budget) or a far cheaper hydrogen molecule than any 2030 forecast found (CEEW ₹360/kg delivered; record refinery-gate tender ₹279/kg before compression and dispensing).", fill=MINT, size=14, bold=True, color=DARKGREEN)
footer(s, "Sources: CNG and petrol prices Sep 2026 [W4-S16, S19]; DERC EV tariff and public charging [W4-S20, S21]; BEV prices and tests [W3-S27, S30]; battery warranties and degradation [W4-S26, S27]; NITI Aayog taxi mileage [W4-S30]; CEEW 2025 delivered hydrogen [W4-S22]; Numaligarh tender ₹279/kg [W3-S39]; carbon credit prices [W4-S73]; model workbook (TCO, Sensitivities, BOM).", 6)

# ---------------------------------------------------------------- Slide 7
s = blank_slide(prs)
bd = H["build"]
y0 = header(s, f"Fuel supply: a 30-car pilot needs about {bd['demand'][0]:.0f} kg a day; delivered hydrogen costs about ₹{bd['delivered'][0]:,.0f}/kg at a pilot point and about ₹{bd['delivered'][1]:,.0f}/kg at a 2030 hub at 70 percent utilisation",
            "Pilot setting: Faridabad, Delhi-NCR. IOCL R&D dispensed hydrogen for the 2022 Mirai pilot and its fuel-cell buses; the MNRE Sahibabad-Faridabad-Delhi corridor was sanctioned in March 2025 (18 to 24 months to commission). No station is public or confirmed available: access is a proposed partnership.")
cats = ["Pilot point 2028 (150 kg/day, 50 percent used)", "Hub station 2030 (500 kg/day, 70 percent used)"]
lossmarg = [bd['delivered'][i] - (bd['prod'][i] + bd['trans'][i] + bd['elec'][i] + bd['caprec'][i] + bd['om'][i]) for i in range(2)]
series = [("Production (green, plant gate)", (bd['prod'][0], bd['prod'][1])), ("Tube-trailer transport", (bd['trans'][0], bd['trans'][1])), ("Compression electricity", (bd['elec'][0], bd['elec'][1])),
          ("Station capital recovery", (bd['caprec'][0], bd['caprec'][1])), ("Station O&M", (bd['om'][0], bd['om'][1])), ("Losses, margin, taxes", (lossmarg[0], lossmarg[1]))]
bar_chart(s, MARGIN, y0, Inches(6.9), Inches(5.0), cats, series, [GREEN, TAGBLUE, CHARTBLUE, NAVY2, MIDGREY, AMBER], number_format='0', font_size=11.5, stacked=True, value_axis_title="₹ per kg delivered", label_size=11, data_labels=False, title=f"Delivered price build-up, unsubsidised (model): ₹{bd['delivered'][0]:,.0f} pilot, ₹{bd['delivered'][1]:,.0f} hub")
textbox(s, MARGIN, y0 + Inches(5.05), Inches(6.9), Inches(1.0), [f"Production ₹{bd['prod'][0]:.0f}/kg (2026-28) and ₹{bd['prod'][1]:.0f}/kg (2030) from CEEW, IEA and SIGHT auction evidence; capex ₹{IN['station_capex_pilot']['active']/1e7:.0f} crore (pilot) and ₹{IN['station_capex_2030']['active']/1e7:.0f} crore (hub) recovered over 10 years at 12 percent. CEEW's central 2030 case is ₹360/kg at a 1,000 kg/day station; ours is deliberately conservative."], size=12, color=DARKGREY, space_after=0)
# sizing table
tx = MARGIN + Inches(7.15); tw_ = Inches(5.6)
rows = [["Station sizing from the fleet (pilot)", "Value"],
 ["Cars x km/day x kg/km", f"30 x 167 x {IN['h2_cons']['active']/100:.4f} x {IN['h2_share']['active']:.2f} share = {bd['demand'][0]:.0f} kg/day"],
 ["Fills per day; peak-window rate", f"{bd['fills'][0]:.0f} fills; {bd['fills'][0]*0.5/3:.0f} per hour in a 3 h start-of-shift window"],
 ["Dispenser positions (6 fills/h each)", f"{bd['disp'][0]:.0f}"],
 ["Compressor throughput (16 h/day, 150 kg/day design)", f"{bd['comp'][0]:.1f} kg/h"],
 ["Cascade storage buffer (1.5 days)", f"{bd['buffer'][0]:.0f} kg at 450 bar"],
 ["Tube-trailer deliveries (300 kg payload)", f"{bd['deliv'][0]:.1f} per week"],
 ["Utilisation from cars alone; assumed with bus and truck users", f"{bd['demand'][0]/bd['cap'][0]*100:.0f} percent; 50 percent"],
 ["Planned downtime, supply interruption cover", "Buffer covers 1.5 days; petrol backup covers the rest"],
 ["Cars one 2030 hub can serve", f"{bd['carsper'][1]:.0f} at 70 percent utilisation"],
]
table(s, tx, y0, tw_, Inches(5.2), rows, col_widths=[1.6, 1.5], font_size=12.5, header_size=13, align_center_from=99)
# responsibilities
rx = tx + tw_ + Inches(0.25); rw = SLIDE_W - MARGIN - rx
bx, by, bw, bh = panel(s, rx, y0, rw, Inches(5.2), "WHO DOES WHAT (proposed, not committed)", fill=GREEN)
textbox(s, bx, by, bw, bh, [
    ("**Vehicles:** fleet partner owns and operates; programme buy-back guarantee on residual value.", {'bullet': True}),
    ("**Kits:** SRDI-led consortium owns during the pilot; kit integrator warrants parts and workmanship.", {'bullet': True}),
    ("**Station:** oil marketing company partner (proposed IOCL, Faridabad) owns and operates under a PESO Form-H licence; take-or-pay from the fleet covers utilisation risk.", {'bullet': True}),
    ("**Fuel:** certified green hydrogen (2 kg CO2e/kg standard) by tube trailer from a SIGHT-awarded producer; delivered price is a programme cost during the pilot.", {'bullet': True}),
    ("**Service:** two hydrogen-ready workshops with trained staff; 3-yearly cylinder tests at a PESO-approved station.", {'bullet': True}),
    ("**Risk carriers:** development (programme); utilisation (station partner with take-or-pay); residual value (fleet, backed by buy-back).", {'bullet': True}),
], size=12.5, line_spacing=1.04, space_after=4)
ut = H["util_table"]
callout(s, MARGIN, Inches(8.6), Inches(19), Inches(1.0), f"Utilisation alone cannot close the gap: at 95 percent utilisation the hub price is still about ₹{ut[-1][2]:,.0f}/kg, and CNG parity (₹{S['parity_cng']:.0f}/kg) is out of reach because production, transport and compression alone exceed it. Delivered versus on-site electrolysis: delivered hydrogen keeps the pilot's capital to a dispensing point; an electrolyser is justified only at hub scale.", fill=YELLOW, size=13.5)
footer(s, "Sources: MNRE pilot corridors, PIB 3 Mar 2025 [W3-S36]; IOCL Faridabad dispensing [W3-S46, W4-S81]; CEEW 2025 station model [W4-S22]; ICCT station cost by utilisation [W4-S46]; Indian station capex indication [W4-S56]; green hydrogen cost evidence [W4-S33, S38, S57]; Gas Cylinder Rules and Form-H [W2-S24, S27]; model workbook (H2_Supply).", 7)

# ---------------------------------------------------------------- Slide 8
s = blank_slide(prs)
ph_ = [x / 1e7 for x in PB["phases"]]; tot = PB["total"] / 1e7
y0 = header(s, f"Roadmap to 2030: four gated phases, ₹{tot:.1f} crore including contingency, with a proceed, redesign or stop decision at each gate",
            "Calendar phases from October 2026; each phase ends with evidence, not a date. Suzuki R&D Center India is proposed as engineering lead; public support is sought under the MNRE transport pilot scheme, which names 4-wheelers.")
phases = [
 ("PHASE 0  Oct 2026 to Mar 2027", f"₹{ph_[0]:.1f} cr", "Feasibility and validation", NAVY2),
 ("PHASE 1  Apr 2027 to Mar 2028", f"₹{ph_[1]:.1f} cr", "Engineering and controlled validation", TAGBLUE),
 ("PHASE 2  Apr 2028 to Mar 2029", f"₹{ph_[2]:.1f} cr", "Certification and pilot build", GREEN),
 ("PHASE 3  Apr 2029 to Sep 2030", f"₹{ph_[3]:.1f} cr", "Pilot operation and evaluation", DEEPGREEN),
 ("PHASE 4  from Oct 2030", "conditional", "Expansion only if gate 4 passes", DARKGREEN),
]
cw_ = Inches(3.85); x = MARGIN
for i, (t, bud, sub, col) in enumerate(phases):
    chevron(s, x, y0, cw_, Inches(0.8), t, col, first=(i == 0), size=13)
    textbox(s, x + Inches(0.1), y0 + Inches(0.85), cw_ - Inches(0.35), Inches(0.5), f"**{sub}**  |  {bud}", size=13, color=DEEPNAVY, space_after=0)
    x += cw_ - Inches(0.12)
rows = [["", "Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4 (conditional)"],
 ["Deliverable", "Written regulator and test-agency view on the retrofit route; 30 fleet interviews and telematics on 20 cars; boot mock-up and CAD packaging; station partner letter", "500 h hydrogen engine test-cell programme; 3 converted prototypes; storage qualification (burst, cycling, bonfire, drop); vehicle leak, ventilation and crash-structure tests", "Kit type approval under the agreed route; 80,000 km durability on 2 cars; 30 conversions; dispensing point commissioned; 2 workshops upgraded", "18 months of operation with 10 CNG and 10 BEV comparison cars; quarterly emission tests; independent evaluation report", "1,000 to 1,500 cars at up to 8 hub stations; localised cylinders and kit production"],
 ["Accountable", "SRDI engineering lead; ARAI or ICAT; PESO liaison", "SRDI with a test-cell partner (HORIBA Chakan or ARAI); cylinder supplier", "Kit integrator; ARAI or ICAT; OMC station partner; fleet partner", "Fleet partner operations; independent evaluator (IIT or CEEW); SRDI data team", "Consortium and public programme"],
 ["Dependencies", "Regulator engagement; fleet access", "Car-size cylinder samples (Luxfer, Quantum, NPROXX, Time Technoplast); hydrogen injectors", "MNRE pilot sanction; PESO approvals; corridor station timing", "Fuel supply contract; insurer endorsement", "Delivered hydrogen price; policy support"],
 ["Gate and decision", "Gate 1: route defined, partner secured, demand evidence from 3 fleets. Otherwise stop.", "Gate 2: consumption at or below 2.2 kg/100 km, NOx at or below 60 mg/km on cycle, no abnormal combustion in 500 h, safety tests passed. Otherwise redesign once, then stop.", "Gate 3: approval granted and station commissioned within 6 months of plan. Otherwise pause.", "Gate 4 (Sep 2030): availability 95 percent or better, zero reportable hydrogen incidents, measured ₹/km published, delivered hydrogen at or below ₹250/kg with a credible path to ₹190/kg. Otherwise stop and publish.", "Proceed only with fuel price and approval in place"],
]
table(s, MARGIN, y0 + Inches(1.4), SLIDE_W - 2 * MARGIN, Inches(4.4), rows, col_widths=[0.85, 1.55, 1.7, 1.55, 1.75, 1.2], font_size=11.5, header_size=12.5, align_center_from=99, row_heights=[Inches(0.38), Inches(1.1), Inches(0.72), Inches(0.72), Inches(1.45)])
fund = [("Suzuki R&D Center India and Maruti Suzuki: engineering, prototypes, test cells", 0.40), ("Public support sought: MNRE transport pilot scheme (4-wheelers named) or R&D scheme, state hydrogen policy", 0.35), ("Oil marketing company partner: dispensing point", 0.15), ("Fleet partner: vehicles, drivers, operations", 0.10)]
rows = [["Proposed funding split (not committed)", "Share", "₹ crore"]] + [[a, f"{b*100:.0f} percent", f"{b*tot:.1f}"] for a, b in fund] + [["Total to September 2030 (incl. 15 percent contingency)", "100 percent", f"{tot:.1f}"]]
table(s, MARGIN, Inches(8.45), Inches(12.6), Inches(1.5), rows, col_widths=[3.4, 0.8, 0.8], font_size=11, header_size=11.5, bold_rows=(5,), row_heights=[Inches(0.28)]*6)
callout(s, MARGIN + Inches(12.85), Inches(8.45), Inches(6.6), Inches(1.5), "Why Suzuki's role is plausible: CNG engine and calibration know-how, a 70 percent share of India's CNG cars, and its own hydrogen combustion work (Swift prototype with AVL, 2026; Burgman). This is a proposal; no endorsement is implied.", fill=MINT, size=12.5, color=DARKGREEN)
footer(s, "Sources: MNRE scheme guidelines, PIB 14 Feb 2024 (buses, trucks and 4-wheelers) [PIB PRID 2006052]; ARAI Phase-II call for proposals (Sep to Dec 2025); HORIBA and ARAI hydrogen test facilities [W4-S14, S15]; CNG kit approval precedent [W2-S3, S8]; PESO rules [W2-S24]; model workbook (Pilot_Budget).", 8)

# ---------------------------------------------------------------- Slide 9
s = blank_slide(prs)
y0 = header(s, "Expected impact is real but small by 2030; the decision requested is ₹0.9 crore for Phase 0, which buys the facts that decide whether ₹37.6 crore is worth spending",
            "Bounded outcomes at matched service (same car, same duty), with the assumptions under which each conclusion reverses.")
bar_chart(s, MARGIN, y0, Inches(6.6), Inches(4.3), ["Continue on CNG", "Retrofit, green H2", "Retrofit, grey H2", "BEV, 2025 grid", "BEV, 2030 grid"],
          [("g CO2e per km, well-to-wheel incl. amortised manufacturing", (round(EM['A']), round(EM['Bgreen']), round(EM['Bgrey']), round(EM['C25']), round(EM['C30'])))],
          [GREEN], number_format='0', font_size=11.5, value_axis_title="g CO2e per km", legend=False, label_size=12, title="Emissions per km, same car and duty (model)")
textbox(s, MARGIN, y0 + Inches(4.35), Inches(6.6), Inches(1.6), [
    f"Green-hydrogen retrofit: {EM['redB']*100:.0f} percent below CNG (petrol backup km included). Grid-electrolysis hydrogen would be {EM['Bgrid']:.0f} g/km, four times worse than CNG. Reversal thresholds: hydrogen above {EM['cithr']:.1f} kg CO2e/kg makes the retrofit worse than CNG; grid below {EM['gridthr']:.2f} kg/kWh at the meter makes the BEV cleaner than the green-hydrogen retrofit (CEA path reaches about 0.5 by 2032).",
    "NOx is the other tailpipe issue: zero CO2 on hydrogen km does not mean zero pollutants."], size=12.5, color=DARKGREY, line_spacing=1.05, space_after=3)
# middle: bounded outcomes + uncertainties
mx = MARGIN + Inches(6.85); mw = Inches(6.3)
rows = [["Bounded outcome", "Pilot (30 cars)", "2030 conditional (about 1,400 cars)"],
 ["CO2e avoided per year (green hydrogen)", f"{EM['pilot_t']:.0f} t", f"{EM['fleet_t']:,.0f} t"],
 ["Hydrogen demand per year", f"{30*E['kgday']*330/1000:.0f} t", f"{EM['fleet_h2']:,.0f} t (about one hub station)"],
 ["Conversion kits sold", "30 (₹7.7 lakh each)", f"about 1,400 (₹3.2 lakh each, ₹{1400*B['volume']/1e7:.0f} crore)"],
 ["Round 1 claim for 2030", "", "1,00,000 cars; 0.9 Mt CO2; 15,000 t/yr hydrogen"],
]
table(s, mx, y0, mw, Inches(2.5), rows, col_widths=[1.5, 1.0, 1.5], font_size=12, header_size=12.5, align_center_from=99)
bx, by, bw, bh = panel(s, mx, y0 + Inches(2.7), mw, Inches(3.3), "TOP REMAINING UNCERTAINTIES (ranked)", fill=NAVY2)
textbox(s, bx, by, bw, bh, [
    ("**1. Delivered hydrogen price:** ₹360 to ₹1,430/kg across sources and our build-up; the single variable that decides everything.", {'bullet': True}),
    ("**2. Approval route:** none exists; timing depends on AISC, MoRTH and PESO.", {'bullet': True}),
    ("**3. NOx on transients:** lean burn is clean at steady state only; aftertreatment and cycle results pending.", {'bullet': True}),
    ("**4. Car-size cylinder supply and PESO approval:** only 150 to 250 L truck cylinders approved in India so far.", {'bullet': True}),
    ("**5. Customer demand:** a hypothesis until Phase 0 interviews; power loss and boot loss may be refused.", {'bullet': True}),
], size=12.5, line_spacing=1.04, space_after=4)
rx = mx + mw + Inches(0.25); rw = SLIDE_W - MARGIN - rx
bx, by, bw, bh = panel(s, rx, y0, rw, Inches(6.0), "DECISION REQUESTED", fill=GREEN)
textbox(s, bx, by, bw, bh, [
    (f"**Approve Phase 0 (₹{ph_[0]:.1f} crore, six months)** and the four-gate framework; no commitment beyond gate 1.", {'bullet': True}),
    ("**Endorse an application** under the MNRE transport pilot scheme (4-wheeler category) with ARAI as implementing agency, and a Gujarat hydrogen-station subsidy request for the second hub.", {'bullet': True}),
    ("**Nominate** an SRDI engineering lead and a fleet and fuel partner shortlist (proposed: IOCL Faridabad, PSU and airport-contract fleets).", {'bullet': True}),
    ("**Start the HCNG step in parallel** where a CGD company can blend to IS 17314: legal since 2020, no vehicle change, about 6 percent of energy from hydrogen, an air-quality measure rather than a decarbonisation step.", {'bullet': True}),
    ("**What would make us stop:** no regulator route by March 2027; NOx or backfire not controlled in 500 h; delivered hydrogen still above ₹250/kg with no path to ₹190/kg in 2030; fleets unwilling to accept a 48 percent power loss and a smaller boot.", {'bullet': True}),
], size=12.5, line_spacing=1.04, space_after=4)
shp = rect(s, MARGIN, Inches(9.2), SLIDE_W - 2 * MARGIN, Inches(0.7), DARKGREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
shape_text(shp, "H2-SHIFT keeps India's hydrogen retrofit option open at low cost, tells the truth about price, and hands the 2030 scale decision to evidence instead of ambition.", size=15, color=WHITE, bold=True, margins=(0.3, 0.05, 0.3, 0.05))
footer(s, "Sources: CEA CO2 baseline v21 and National Electricity Plan [W4-S59, S60]; IPCC fuel factors [W4-S62]; ICCT 2025 lifecycle factors and battery footprint [W4-S63]; hydrogen carbon intensities [W4-S64, S65]; DOE NOx page [W2-S52]; MNRE scheme scope, PIB 14 Feb 2024; Gujarat policy [W4-S76]; H-CNG notification GSR 585(E) [W2-S1]; model workbook (Emissions, Market, Pilot_Budget).", 9)

# ---------------------------------------------------------------- Slide 10
s = blank_slide(prs)
y0 = header(s, "Key sources and annexure index", "Research cut-off 14 September 2026. Full register of 300 plus entries with URLs, dates, sections and limitations is in the annexure and the workbook (Sources sheet).", wordmark=True)
srcs = [
 "1. PIB, MNRE, 'Pilot Projects on Hydrogen Fuelled Buses and Trucks Launched under the NGHM', 3 Mar 2025 (PRID 2107795): 5 projects, 37 vehicles, 9 stations, 10 routes incl. Sahibabad-Faridabad-Delhi, ₹208 crore.",
 "2. PIB, MNRE, 'Scheme Guidelines for Pilot Projects on use of Green Hydrogen in the Transport Sector', 14 Feb 2024 (PRID 2006052): buses, trucks and 4-wheelers; ₹496 crore; PIB 29 Jul 2026: 12 projects, 70 vehicles, 16 stations, ₹410.77 crore.",
 "3. MoRTH, GSR 746(E), 16 Oct 2023: CMVR Rule 125M, AIS 195:2023 for hydrogen ICE vehicles of categories M and N; ARAI AIS-195 with Amendment 1 (May 2025); AIS 157:2020 (GSR 579(E), 23 Sep 2020), scope excludes retrofitted or converted fuel-cell vehicles.",
 "4. DPIIT/PESO, Gas Cylinders (Amendment) Rules 2025, GSR 225(E), 11 Apr 2025: on-board hydrogen cylinders, 3-yearly testing, 15-year life; PESO Form-H online licensing for hydrogen dispensing, May 2025.",
 "5. MoRTH, GSR 585(E), 25 Sep 2020: H-CNG per IS 17314:2019 added to CMVR Rule 115; IOCL and DTC 50-bus HCNG trial, Oct 2020.",
 "6. PNGRB citing Vahan (Aug 2025): 81.95 lakh CNG vehicles (Mar 2025); MoPNG: 8,150 plus CNG stations, 17,700 to 18,000 targeted by 2030; IGL, MGL, MNGL price notices Sep 2026.",
 "7. Maruti Suzuki specifications and releases (Tour S, Dzire, WagonR, Ertiga, Eeco); Maruti CNG sales FY25 6.12 to 6.2 lakh, FY26 above 7 lakh; Suzuki Growth Strategy FY2030.",
 "8. Luxfer G-Stor Pro H2 specification table (V060H35: 60 L, 350 bar, 36 kg, 1.45 kg); Hexagon Purus Type 4 table (Rev 08/22); US DOE Records 19008 and 24006 on Type IV storage cost.",
 "9. US DOE and H2Tools: hydrogen properties; 'Does the use of hydrogen produce NOx'; NFPA 2 (2023); UN GTR 13 Amendment 1 (2023) and UN R134; SAE J2601 (2020); ISO 19881:2025; ISO 14687.",
 "10. CEEW (2025) India hydrogen and EV TCO model: delivered green hydrogen USD 4.2/kg in 2030; ICCT (2022, 2025): station cost by utilisation, lifecycle factors; IEA Global Hydrogen Review 2025; NITI Aayog (Feb 2026) taxi mileage 70,000 km/yr.",
 "11. CEA CO2 Baseline Database v21 (FY2024-25, 0.710 t/MWh) and National Electricity Plan 2022-32; IPCC 2006 fuel factors; MNRE Green Hydrogen Standard (2 kg CO2e/kg).",
 "12. Global programmes: Toyota (Mirai, HiAce, GR Corolla), Hyundai Nexo, KEYOU, ULEMCo, JCB, Cummins B6.7H India, Stellantis (Jul 2025), Shell California (Feb 2024), H2 Mobility Germany (2025); Suzuki-AVL hydrogen Swift, Vienna Motor Symposium, May 2026 (Fuel Cells Works, RushLane).",
 "13. Delhi Motor Vehicle Aggregator and Delivery Service Provider Scheme 2023; Delhi EV Policy 2026; CAQM NCR direction (Jan 2026); Gujarat Green Hydrogen Policy 2025; Maharashtra Green Hydrogen Policy 2023.",
]
textbox(s, MARGIN, y0, Inches(12.4), Inches(8.2), [(t, {'space_after': 5}) for t in srcs], size=13, color=DARKGREY, line_spacing=1.04)
bx, by, bw, bh = panel(s, MARGIN + Inches(12.65), y0, Inches(6.25), Inches(5.6), "ANNEXURE INDEX (separate PDF and workbook)")
textbox(s, bx, by, bw, bh, [
    "A1  Claim audit: Round 1 versus evidence, with corrections",
    "A2  Assumptions, evidence classes and full source register",
    "A3  Cost model: BOM, TCO, break-even, sensitivities",
    "A4  Packaging, energy balance and performance calculations",
    "A5  Regulatory compliance matrix and hazard analysis",
    "A6  Market sizing method and bottom-up funnel",
    "A7  Global benchmark evidence (progress and setbacks)",
    "A8  Pilot design, instrumentation and first 90 days",
    "A9  Phase budgets, responsibilities and funding",
    "A10 Judge Q&A, validation log and change log",
    "Workbook: H2SHIFT_model.xlsx (11 sheets, formula-driven, recalculated)",
], size=14.5, color=DARKGREY, line_spacing=1.1, space_after=4)
callout(s, MARGIN + Inches(12.65), y0 + Inches(5.8), Inches(6.25), Inches(2.3), "Evidence discipline: every headline number traces to a source ID (verified), a workbook cell (model) or a stated assumption. Many original documents were inaccessible through the build environment's network policy; such entries are marked 'excerpt' or 'summary' in the register and should be re-verified before external use. No customer interviews, letters of interest, test results or partnerships are claimed.", fill=YELLOW, size=12.5)
footer(s, "Team Wookies, NIT Warangal. SRDI Igniters Innovation Challenge 2026, Engineering Track, Option 2: Hydrogen Retrofit Solution. Round 2 submission.", 10)

prs.save(OUT)
print("saved", OUT, "slides", len(prs.slides))
