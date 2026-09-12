"""Build the NAADI pilot economics workbook with live formulas.

India Chem 2026 — Team NIT Warangal. DRAFT for team review; every input is an
assumption the team must challenge and ratify. Blue+yellow cells = inputs,
black = formulas. Units: INR lakh unless stated.
"""

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

BLUE = Font(name="Arial", color="0000FF", size=10)
BLACK = Font(name="Arial", color="000000", size=10)
BOLD = Font(name="Arial", bold=True, size=10)
H1 = Font(name="Arial", bold=True, size=13, color="12212F")
H2 = Font(name="Arial", bold=True, size=11, color="087E8B")
GREY = Font(name="Arial", size=9, color="555555", italic=True)
YELLOW = PatternFill("solid", fgColor="FFFF00")
LIGHT = PatternFill("solid", fgColor="F4F7F8")
THIN = Border(bottom=Side(style="thin", color="D9E2E7"))

L = '#,##0.0" L"'      # INR lakh
LPH = '#,##0.00" L/h"'
HRS = '#,##0" h"'
PCT = "0.0%"
MON = '#,##0.0" mo"'
NUM = "#,##0"

wb = Workbook()


def put(ws, cell, value, font=BLACK, fmt=None, fill=None, comment=None, wrap=False):
    c = ws[cell]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if wrap:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if comment:
        c.comment = Comment(comment, "Team NITW draft")
    return c


# ---------------------------------------------------------------- Assumptions
ws = wb.active
ws.title = "Assumptions"
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 14
ws.column_dimensions["C"].width = 12
ws.column_dimensions["D"].width = 78

put(ws, "A1", "NAADI pilot — assumptions register (units: INR lakh unless stated)", H1)
put(ws, "A2", "Blue+yellow cells are inputs for the team to edit and ratify. Every value "
    "is labelled Fact / Sourced range / Estimate. Nothing here is primary research.",
    GREY, wrap=True)

A = {}   # key -> "Assumptions!B<row>"
row = [3]  # mutable row counter


def header(label):
    put(ws, f"A{row[0]}", label, H2)
    row[0] += 1


def assume(key, label, value, fmt, note):
    r = row[0]
    put(ws, f"A{r}", label, BLACK, wrap=True)
    is_formula = isinstance(value, str) and value.startswith("=")
    put(ws, f"B{r}", value, BLACK if is_formula else BLUE, fmt,
        fill=None if is_formula else YELLOW)
    kind = ("Formula" if is_formula else
            "Sourced range" if "SOURCED" in note else "Estimate")
    put(ws, f"C{r}", kind, GREY)
    put(ws, f"D{r}", note, GREY, wrap=True)
    ws[f"A{r}"].border = THIN
    A[key] = f"Assumptions!B{r}"
    row[0] += 1


header("PLANT ARCHETYPE (representative use case — TEAM ESTIMATES)")
assume("revenue", "Plant annual revenue (INR lakh)", 50000, NUM,
       "Estimate: mid-size speciality chemicals plant, ~INR 500 Cr/yr revenue. Team to ratify.")
assume("margin", "Contribution margin (% of revenue)", 0.30, PCT,
       "Estimate: typical speciality-chem contribution margin used for lost-production "
       "valuation. Team to ratify.")
assume("hours", "Operating hours per year", 8000, NUM,
       "Estimate: continuous plant, ~91% utilisation.")
assume("pumps_total", "Total pumps in plant (count)", 200, NUM,
       "Estimate: typical mid-size plant pump population; context only.")
assume("pumps", "Critical 'bad-actor' pumps in pilot (count)", 25, NUM,
       "Pilot scope: selected by criticality ranking per ISO 14224 taxonomy.")
assume("points", "Measurement points (2 bearing housings per pump)",
       "={p}*2".format(p="B" + A["pumps"].split("B")[1]), NUM,
       "Drive-end + non-drive-end bearing housing per pump. (Formula)")

header("BASELINE LOSSES ON THE 25 PUMPS (TEAM ESTIMATES)")
assume("dt_hours", "Unplanned downtime caused by these pumps (h/yr)", 60, HRS,
       "Estimate: 3-4 pump-caused trips/yr with multi-hour restarts in a continuous "
       "process. Replace with the pilot plant's real 24-month history in Phase 0.")
assume("lakh_per_h", "Value of lost production (INR lakh per hour)",
       "={rev}*{m}/{h}".format(rev="B" + A["revenue"].split("B")[1],
                               m="B" + A["margin"].split("B")[1],
                               h="B" + A["hours"].split("B")[1]), LPH,
       "Revenue x contribution margin / operating hours. (Formula)")
assume("repairs", "Pump repair events per year (count)", 12, NUM,
       "Estimate: MTBR ~25 months across 25 bad actors.")
assume("repair_cost", "Average direct repair cost per event", 2.5, L,
       "Estimate: mechanical seal/bearing cartridge replacement incl. labour.")
assume("cat_events", "Catastrophic secondary-damage events avoided per year", 2, NUM,
       "Estimate: bearing run-to-seizure destroying shaft/impeller, downgraded to "
       "planned repair.")
assume("cat_extra", "Extra cost of a catastrophic vs planned repair", 2.5, L,
       "Estimate: secondary damage + emergency logistics premium.")

header("EFFECTIVENESS (SOURCED RANGES, APPLIED AT LOW END)")
assume("dt_red", "Downtime reduction from PdM (fraction)", 0.35, PCT,
       "SOURCED range: US DOE FEMP O&M Best Practices Guide R3.0 (2010) reports 35-45% "
       "downtime reduction for functioning PdM programmes; low end used. "
       "https://www.energy.gov/sites/prod/files/2020/04/f74/omguide_complete_w-eo-disclaimer.pdf")
assume("rep_red", "Repair-spend reduction vs preventive-only (fraction)", 0.10, PCT,
       "SOURCED range: DOE FEMP reports 8-12% savings of PdM over preventive maintenance "
       "alone; mid value used.")

header("PILOT COSTS (TEAM ESTIMATES — VENDOR QUOTES NEEDED)")
assume("sensor_cost", "Wireless tri-axial vibration+temp sensor, Ex-rated, installed "
       "(per point)", 0.35, L,
       "Estimate: market range for industrial wireless sensors incl. mounting and "
       "commissioning. No vendor quote yet — TEAM INPUT REQUIRED before final.")
assume("gateways", "Edge gateways (count)", 5, NUM,
       "Estimate: 1 gateway per ~10 pumps/plant area.")
assume("gateway_cost", "Cost per edge gateway", 1.5, L, "Estimate.")
assume("integration", "Historian/CMMS integration + software + commissioning", 10, L,
       "Estimate: OPC-UA connector, dashboard, alert-to-work-order workflow.")
assume("training", "Operator & reliability-engineer training", 2, L, "Estimate.")
assume("opex", "Annual OpEx (connectivity, compute, batteries, model upkeep)", 6, L,
       "Estimate: ~10%/yr sensor battery/replacement + compute + model retraining effort.")

header("FINANCE")
assume("disc", "Discount rate for NPV", 0.12, PCT,
       "Estimate: typical Indian industrial hurdle rate.")
assume("horizon", "Evaluation horizon (years)", 5, NUM,
       "Per competition economic-feasibility convention.")

# ---------------------------------------------------------------- Model
m = wb.create_sheet("Model")
m.column_dimensions["A"].width = 52
for col in "BCDEFG":
    m.column_dimensions[col].width = 13

put(m, "A1", "NAADI pilot — unit economics (all formulas; INR lakh)", H1)

put(m, "A3", "ANNUAL BENEFIT", H2)
put(m, "A4", "Avoided downtime (h/yr)")
put(m, "B4", f"={A['dt_hours']}*{A['dt_red']}", BLACK, HRS)
put(m, "A5", "Value of avoided downtime")
put(m, "B5", f"=B4*{A['lakh_per_h']}", BLACK, L)
put(m, "A6", "Repair-spend saving")
put(m, "B6", f"={A['repairs']}*{A['repair_cost']}*{A['rep_red']}", BLACK, L)
put(m, "A7", "Avoided catastrophic secondary damage")
put(m, "B7", f"={A['cat_events']}*{A['cat_extra']}", BLACK, L)
put(m, "A8", "Total annual benefit", BOLD)
put(m, "B8", "=SUM(B5:B7)", BOLD, L, fill=LIGHT)

put(m, "A10", "CAPEX", H2)
put(m, "A11", "Sensors installed")
put(m, "B11", f"={A['points']}*{A['sensor_cost']}", BLACK, L)
put(m, "A12", "Edge gateways")
put(m, "B12", f"={A['gateways']}*{A['gateway_cost']}", BLACK, L)
put(m, "A13", "Integration, software, commissioning")
put(m, "B13", f"={A['integration']}", BLACK, L)
put(m, "A14", "Training")
put(m, "B14", f"={A['training']}", BLACK, L)
put(m, "A15", "Total CapEx", BOLD)
put(m, "B15", "=SUM(B11:B14)", BOLD, L, fill=LIGHT)

put(m, "A17", "RETURNS", H2)
put(m, "A18", "Annual OpEx")
put(m, "B18", f"={A['opex']}", BLACK, L)
put(m, "A19", "Net annual benefit", BOLD)
put(m, "B19", "=B8-B18", BOLD, L, fill=LIGHT)
put(m, "A20", "Simple payback (months)", BOLD)
put(m, "B20", "=B15/B19*12", BOLD, MON, fill=LIGHT)
put(m, "A21", "5-year NPV @ discount rate", BOLD)
put(m, "B21", f"=-B15+NPV({A['disc']},B24:F24)", BOLD, L, fill=LIGHT)
put(m, "A22", "Cost per avoided downtime-hour (CapEx amortised over horizon)")
put(m, "B22", f"=(B15/{A['horizon']}+B18)/B4", BLACK, LPH)

put(m, "A23", "Year", GREY)
for i, col in enumerate("BCDEF", start=1):
    put(m, f"{col}23", i, GREY, NUM)
    put(m, f"{col}24", "=$B$19", BLACK, L)
put(m, "A24", "Net cash flow per year (uniform, no ramp; a conservative ramp "
    "pushes payback ~2-3 months later)", GREY, wrap=True)

# ---------------------------------------------------------------- Sensitivity
s = wb.create_sheet("Sensitivity")
s.column_dimensions["A"].width = 56
for col in "BCD":
    s.column_dimensions[col].width = 16

put(s, "A1", "Sensitivity — simple payback (months) under single-variable swings", H1)
put(s, "A2", "Each row recomputes the full model with one input changed; all else at base.",
    GREY)

put(s, "A4", "Scenario", BOLD)
put(s, "B4", "Payback (mo)", BOLD)

BEN = ("({dt}*{dtred}*{lph}+{rep}*{repc}*{repred}+{cat}*{catx})".format(
    dt=A['dt_hours'], dtred="{dtred}", lph=A['lakh_per_h'], rep=A['repairs'],
    repc=A['repair_cost'], repred=A['rep_red'], cat=A['cat_events'],
    catx=A['cat_extra']))


def pb(dtred="{}".format(A['dt_red']), capex_mult=1.0, lph_mult=1.0):
    ben = ("({dt}*{dtred}*{lph}*{lm}+{rep}*{repc}*{repred}+{cat}*{catx})".format(
        dt=A['dt_hours'], dtred=dtred, lph=A['lakh_per_h'], lm=lph_mult,
        rep=A['repairs'], repc=A['repair_cost'], repred=A['rep_red'],
        cat=A['cat_events'], catx=A['cat_extra']))
    return f"=Model!B15*{capex_mult}/({ben}-{A['opex']})*12"


scenarios = [
    ("Base case (35% downtime cut, base margin, base CapEx)", pb()),
    ("Downtime reduction only 20% (programme underperforms DOE band)", pb(dtred="0.2")),
    ("Downtime reduction 45% (top of DOE band)", pb(dtred="0.45")),
    ("Lost-production value 1/3 lower", pb(lph_mult=(2 / 3))),
    ("CapEx overrun +30%", pb(capex_mult=1.3)),
    ("Downside stack: 20% cut AND CapEx +30%", pb(dtred="0.2", capex_mult=1.3)),
]
r = 5
for name, formula in scenarios:
    put(s, f"A{r}", name, BLACK, wrap=True)
    put(s, f"B{r}", formula, BLACK, MON)
    r += 1

put(s, f"A{r + 1}", "Reading: payback stays under ~20 months even if the programme "
    "delivers only 20% downtime reduction (below the DOE-reported band) or CapEx "
    "overruns 30%. The model breaks only if BOTH the plant's downtime history and "
    "the DOE effectiveness band are far off — which Phase 0 baselining will test.",
    GREY, wrap=True)
put(s, f"A{r + 3}", "LEGEND: yellow+blue = team-editable inputs; black = formulas; "
    "currency in INR lakh. Sources for DOE ranges on the Assumptions sheet.",
    GREY, wrap=True)

wb.save("/home/user/Dataforge/india-chem-2026/economics/NAADI_pilot_economics.xlsx")
print("saved; assumption cells:", A)
