"""Builds the formula-driven H2-SHIFT Round 2 workbook (openpyxl). Recalculate with LibreOffice headless."""
import json, os, sys, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
sys.path.insert(0, os.path.dirname(__file__))
from model_inputs import INPUTS

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-Dataforge/8c3116aa-5914-54b9-9102-e947be44cbb4/scratchpad/out/H2SHIFT_model.xlsx"
SRC_JSON = os.path.join(os.path.dirname(__file__), "sources.json")

wb = Workbook()
BLUE = Font(color="1F4E9E")            # inputs
BOLD = Font(bold=True)
HDR = Font(bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="002444")
SFILL = PatternFill("solid", fgColor="DDF1E3")
IFILL = PatternFill("solid", fgColor="FFF7D6")
OFILL = PatternFill("solid", fgColor="E8F0FA")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

def hdr(ws, row, values, widths=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = Font(bold=True, size=14, color="002444")
    if sub:
        ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="555555")

def put(ws, ref, value, fmt=None, bold=False, fill=None, font=None):
    c = ws[ref]; c.value = value
    if fmt: c.number_format = fmt
    if bold: c.font = BOLD
    if font: c.font = font
    if fill: c.fill = fill
    return c

# ------------------------------------------------------------------ ReadMe
ws = wb.active; ws.title = "ReadMe"
title(ws, "H2-SHIFT Round 2 model: hydrogen retrofit of factory-CNG passenger cars versus continuing on CNG and versus a BEV",
      "Team Wookies, NIT Warangal. SRDI Igniters Innovation Challenge 2026, Engineering Track, Option 2. Research cut-off 14 September 2026.")
lines = [
 "Purpose: one consistent set of inputs feeding the presentation, annexure and pitch. All outputs are formulas; change inputs only on the Inputs sheet.",
 "Scenario selector: Inputs!C3 (1 = Base, 2 = Downside for the retrofit case, 3 = Upside for the retrofit case). 'Downside' means the retrofit looks worse (for example cheaper CNG, dearer hydrogen).",
 "Colour code: blue text on yellow = input; black = formula; green header = key output.",
 "Evidence classes on the Inputs sheet: A = verified external evidence; B = our calculated estimate; C = explicit assumption or sensitivity range; D = proposed target requiring validation.",
 "Options compared for an owner deciding in the decision year: A = continue operating the CNG donor; B = retrofit the donor to hydrogen (H2-ICE, petrol retained as backup); C = sell the donor and buy a compact fleet BEV.",
 "Fairness rules: the donor's resale value is a cash inflow only in option C (sold at t0); options A and B receive the donor's residual value at the end of the horizon instead. No depreciation is charged in addition to capital cost. Battery replacement is not assumed within the horizon (warranty evidence on Inputs). Charging during idle hours carries no time cost; in-shift charging or refuelling carries a time cost in all three options.",
 "Levelised cost per km = NPV of costs divided by discounted kilometres. Break-even hydrogen price = the year-1 delivered price at which option B has the same NPV as the comparator, holding the same price trajectory shape.",
 "Hydrogen price is the delivered price at the dispenser and is built up on the H2_Supply sheet (production, transport, compression electricity, station capital recovery at a stated utilisation, O&M, losses, margin and taxes). Station capital is recovered through the fuel price only, never allocated twice.",
 "Sheets: Inputs; Donor_Tech (donor and technology comparison); BOM (conversion cost, pilot versus commercial volume); Energy_Range (energy balance, storage, range, mass, power); TCO (cash flows, NPVs, break-even); H2_Supply (fleet demand, station sizing, delivered price, utilisation); Market (bottom-up sizing); Pilot_Budget (phases, budget, rollout); Emissions (per-km and fleet-scale); Sensitivities (grids and one-at-a-time); Sources (register).",
 "Recalculated with LibreOffice Calc (headless) on the build date; open in Excel and press F9 if values do not appear.",
 "Limitations: many external documents were inaccessible through the build environment's network policy; such inputs are flagged in Sources with 'excerpt' or 'summary' status and should be re-verified against originals before publication.",
]
for i, l in enumerate(lines, start=4):
    ws.cell(row=i, column=1, value=l).alignment = WRAP
ws.column_dimensions["A"].width = 160

# ------------------------------------------------------------------ Inputs
wi = wb.create_sheet("Inputs")
title(wi, "Inputs (single source of truth)", "Change values in the Base / Downside / Upside columns only. Active column follows the scenario selector.")
put(wi, "B3", "Scenario selector (1 Base, 2 Downside, 3 Upside):", bold=True)
put(wi, "C3", 1, fill=IFILL, font=BLUE)
hdr(wi, 5, ["Key", "Parameter", "Base", "Downside", "Upside", "Active", "Unit", "Class", "Source IDs", "Notes"],
    [22, 70, 14, 14, 14, 14, 16, 8, 18, 60])
A = {}      # key -> absolute address of Active value
ROW = {}    # key -> row
r = 6
for item in INPUTS:
    if item[0] == "SECTION":
        c = wi.cell(row=r, column=1, value=item[1]); c.font = Font(bold=True, color="016F49"); c.fill = SFILL
        for col in range(2, 11):
            wi.cell(row=r, column=col).fill = SFILL
        r += 1; continue
    key, name, base, down, up, unit, cls, src, note = item
    wi.cell(row=r, column=1, value=key)
    wi.cell(row=r, column=2, value=name).alignment = WRAP
    for col, v in zip((3, 4, 5), (base, down, up)):
        c = wi.cell(row=r, column=col, value=v); c.font = BLUE; c.fill = IFILL
        if isinstance(v, float) and abs(v) < 1: c.number_format = "0.00%" if unit.startswith("fraction") else "0.000"
        elif isinstance(v, (int, float)): c.number_format = "#,##0.##"
    wi.cell(row=r, column=6, value=f"=CHOOSE($C$3,C{r},D{r},E{r})").number_format = "#,##0.###"
    wi.cell(row=r, column=7, value=unit); wi.cell(row=r, column=8, value=cls)
    wi.cell(row=r, column=9, value=src); wi.cell(row=r, column=10, value=note).alignment = WRAP
    A[key] = f"Inputs!$F${r}"; ROW[key] = r
    r += 1
wi.freeze_panes = "C6"
I = lambda k: A[k]

# ------------------------------------------------------------------ BOM
wb_ = wb.create_sheet("BOM")
title(wb_, "Retrofit bill of materials and conversion cost", "Pilot batch (about 30 kits) versus commercial volume (about 10,000 kits per year with localised cylinders). Unit costs are estimates unless a source is given.")
hdr(wb_, 4, ["#", "Component / activity", "Qty", "Unit cost pilot (Rs)", "Unit cost volume (Rs)", "Pilot total (Rs)", "Volume total (Rs)", "Class", "Basis / source"],
    [5, 62, 6, 20, 20, 18, 18, 8, 70])
bom = [
 ("Storage and mounting", None),
 ("Composite hydrogen cylinder, 60 L water volume, 350 bar (Type III or IV), 15-year life", 1, 250000, 95000, "B", "Scaled from DOE/Strategic Analysis Type IV system cost records (S-CYLCOST): about $33/kWh at low volume and $21/kWh at 10k/yr for a 5.6 kg 700 bar system, applied to a 1.45 kg (48 kWh) cylinder with a small-size penalty; example product Luxfer G-Stor Pro V060H35 (S-CYL)"),
 ("On-tank valve with solenoid, excess-flow, manual shut-off and TPRD (UN R134 class)", 1, 55000, 18000, "C", "Production parts exist (S-OTV); no public price; estimate"),
 ("Mounting frame, straps, boot bulkhead shield, TPRD vent duct, boot ventilation", 1, 30000, 11000, "C", "Fabricated steel frame per UN R110-type 20 g / 8 g loads; estimate"),
 ("Fuel delivery", None),
 ("H35 receptacle, check valve, high-pressure filter", 1, 25000, 8000, "C", "ISO 17268 H35 receptacle; estimate"),
 ("Stainless (316L) high-pressure lines and fittings", 1, 18000, 7000, "C", "Estimate"),
 ("Two-stage pressure regulator 350 bar to injection pressure, with pressure and temperature sensors", 1, 55000, 15000, "C", "Production FCEV regulators exist (S-REG); estimate for ICE outlet pressure"),
 ("Hydrogen port-fuel injectors (4) and rail", 1, 40000, 12000, "C", "Bosch / PHINIA H2 PFI injectors announced 2024-25 (S-INJ); estimate"),
 ("Low-pressure hose, fuel shut-off, pressure relief", 1, 8000, 3500, "C", "Estimate"),
 ("Controls and safety", None),
 ("Hydrogen ECU (dual-map, CAN, automatic petrol fallback, diagnostics) with harness", 1, 45000, 15000, "C", "Analogous to sequential CNG ECU at volume; pilot uses low-volume controller"),
 ("Hydrogen leak sensors (boot and engine bay), controller, cabin warning, vent fan", 1, 22000, 7000, "C", "Automotive H2 sensors exist (S-SENS); estimate"),
 ("Engine and emissions", None),
 ("Cold-grade spark plugs, PCV/oil-separator upgrade, coolant and knock sensor check", 1, 8000, 4000, "C", "Backfire and pre-ignition mitigation items (S-H2ICE)"),
 ("Lean-NOx aftertreatment provision (lean NOx trap) and lambda sensor", 1, 35000, 15000, "C", "Needed if lean calibration alone does not meet BS-VI NOx over the cycle (S-NOX); estimate"),
 ("Installation and validation", None),
 ("Removal of CNG kit and cylinder, installation labour (hours)", 40, 600, 600, "C", "Pilot 40 h; volume 14 h at Rs 600/h (see qty note)"),
 ("Per-vehicle leak test, commissioning, road test and documentation", 1, 10000, 2500, "C", "Estimate"),
 ("Certification and engineering amortisation per kit", 1, 0, 8000, "B", "Volume: one-time development and type-approval cost (Pilot_Budget) spread over 50,000 kits; pilot carries it in the programme budget"),
]
r = 5; n = 0; sub_rows = []
for item in bom:
    if item[1] is None:
        c = wb_.cell(row=r, column=2, value=item[0]); c.font = Font(bold=True, color="016F49"); r += 1; continue
    n += 1
    name, qty, up_, uv, cls, basis = item
    wb_.cell(row=r, column=1, value=n)
    wb_.cell(row=r, column=2, value=name).alignment = WRAP
    c = wb_.cell(row=r, column=3, value=qty); c.font = BLUE; c.fill = IFILL
    c = wb_.cell(row=r, column=4, value=up_); c.font = BLUE; c.fill = IFILL; c.number_format = "#,##0"
    c = wb_.cell(row=r, column=5, value=uv); c.font = BLUE; c.fill = IFILL; c.number_format = "#,##0"
    if name.startswith("Removal of CNG kit"):
        wb_.cell(row=r, column=6, value=f"=C{r}*D{r}").number_format = "#,##0"
        wb_.cell(row=r, column=7, value=f"=14*E{r}").number_format = "#,##0"
    else:
        wb_.cell(row=r, column=6, value=f"=C{r}*D{r}").number_format = "#,##0"
        wb_.cell(row=r, column=7, value=f"=C{r}*E{r}").number_format = "#,##0"
    wb_.cell(row=r, column=8, value=cls); wb_.cell(row=r, column=9, value=basis).alignment = WRAP
    sub_rows.append(r); r += 1
first, last = sub_rows[0], sub_rows[-1]
r += 1
put(wb_, f"B{r}", "Subtotal parts, labour and validation", bold=True)
put(wb_, f"F{r}", f"=SUM(F{first}:F{last})", "#,##0", bold=True); put(wb_, f"G{r}", f"=SUM(G{first}:G{last})", "#,##0", bold=True); sub = r; r += 1
put(wb_, f"B{r}", "Warranty provision (share of subtotal)"); put(wb_, f"D{r}", 0.05, "0%", font=BLUE, fill=IFILL); put(wb_, f"E{r}", 0.04, "0%", font=BLUE, fill=IFILL)
put(wb_, f"F{r}", f"=F{sub}*D{r}", "#,##0"); put(wb_, f"G{r}", f"=G{sub}*E{r}", "#,##0"); war = r; r += 1
put(wb_, f"B{r}", "Installer and kit-maker margin (share of subtotal)"); put(wb_, f"D{r}", 0.0, "0%", font=BLUE, fill=IFILL); put(wb_, f"E{r}", 0.15, "0%", font=BLUE, fill=IFILL)
put(wb_, f"F{r}", f"=F{sub}*D{r}", "#,##0"); put(wb_, f"G{r}", f"=G{sub}*E{r}", "#,##0"); mar = r; r += 1
put(wb_, f"B{r}", "GST on kit and installation (rate assumed; CNG kits attract 28 percent, hydrogen kit classification to be confirmed)"); put(wb_, f"D{r}", 0.18, "0%", font=BLUE, fill=IFILL); put(wb_, f"E{r}", 0.18, "0%", font=BLUE, fill=IFILL)
put(wb_, f"F{r}", f"=(F{sub}+F{war}+F{mar})*D{r}", "#,##0"); put(wb_, f"G{r}", f"=(G{sub}+G{war}+G{mar})*E{r}", "#,##0"); gst = r; r += 1
# fixed rows for totals so Inputs can reference: force row 40
while r < 40: r += 1
put(wb_, "B40", "Installed conversion cost per vehicle (incl. taxes)", bold=True, fill=SFILL)
put(wb_, "F40", f"=F{sub}+F{war}+F{mar}+F{gst}", "#,##0", bold=True, fill=SFILL)
put(wb_, "G40", f"=F40", "#,##0", bold=True, fill=SFILL)
put(wb_, "H40", f"=G{sub}+G{war}+G{mar}+G{gst}", "#,##0", bold=True, fill=SFILL)
put(wb_, "E40", "Pilot (G) / Volume (H):", bold=True)
put(wb_, "B41", "Share of cylinder and valve in volume kit cost")
put(wb_, "F41", f"=(G{first}+G{first+1})/G{sub}", "0%")
put(wb_, "B42", "Volume kit cost in Rs lakh"); put(wb_, "F42", "=H40/100000", "0.00")
put(wb_, "B43", "Pilot kit cost in Rs lakh"); put(wb_, "F43", "=G40/100000", "0.00")
put(wb_, "B44", "Reference: Round 1 assumed Rs 1.8 to 2.2 lakh installed. Reference: sequential CNG retrofit kit incl. cylinder and fitting in India about Rs 0.6 to 0.9 lakh (S-CNGKIT).")

# ------------------------------------------------------------------ Energy_Range
we = wb.create_sheet("Energy_Range")
title(we, "Energy balance, storage, range, mass and power", "Column vectors of formulas referencing Inputs. Hydrogen consumption is an input cross-checked against the CNG energy balance.")
hdr(we, 4, ["Quantity", "Value", "Unit", "Formula / note"], [64, 16, 14, 90])
rows = [
 ("Energy use per km on CNG (fleet real-world)", f"={I('cng_lhv')}/{I('cng_kmkg')}", "MJ/km", "LHV / km per kg"),
 ("Energy use per km on petrol (fleet real-world)", f"={I('petrol_lhv')}/{I('petrol_kml')}", "MJ/km", ""),
 ("Hydrogen consumption assumed (input)", f"={I('h2_cons')}", "kg/100 km", "Input h2_cons"),
 ("Energy use per km on hydrogen", f"=B7/100*{I('h2_lhv')}", "MJ/km", ""),
 ("Implied H2-ICE efficiency relative to CNG operation (>1 = better)", "=B5/B8", "ratio", "Cross-check: lean PFI hydrogen at part load can match or exceed CNG efficiency; retrofit calibration usually loses some of that"),
 ("Hydrogen economy", "=100/B7", "km/kg", ""),
 ("Cylinder internal volume", f"={I('cyl_vol')}", "L", ""),
 ("Nominal hydrogen at 350 bar, 15 C", f"=B11/1000*{I('h2_density_350')}", "kg", "Density 24.0 kg/m3 (S-DENS)"),
 ("Nominal hydrogen if 700 bar cylinder of same volume", f"=B11/1000*{I('h2_density_700')}", "kg", "Design option; needs 700 bar dispensing"),
 ("Hydrogen after a non-cooled 350 bar fill", f"=B12*{I('fill_soc')}", "kg", "Fill SOC input; hot ambient, no pre-cooling"),
 ("Residual hydrogen at minimum usable pressure", f"=B11/1000*{I('resid_density')}", "kg", "About 20 bar residual"),
 ("Usable hydrogen per fill", "=B14-B15", "kg", "Key output"),
 ("Range on hydrogen per fill", "=B16/(B7/100)", "km", "Key output"),
 ("Range on hydrogen per fill, 700 bar option", f"=(B13*{I('fill_soc')}-B15)/(B7/100)", "km", ""),
 ("Petrol backup range", f"={I('petrol_tank')}*{I('petrol_kml')}", "km", "Existing tank retained"),
 ("Daily hydrogen need at full hydrogen operation", f"={I('km_day')}*B7/100", "kg/day", ""),
 ("Fills per day needed for 100 percent hydrogen operation", "=B20/B16", "fills/day", ""),
 ("Maximum share of km on hydrogen with the available depot fills", f"=MIN(1,{I('fills_day')}*B16/B20)", "fraction", "Compare with input h2_share"),
 ("Share of km on hydrogen used in the model (input)", f"={I('h2_share')}", "fraction", ""),
 ("Hydrogen used per operating day in the model", f"={I('km_day')}*B7/100*B23", "kg/day", ""),
 ("Mass added: cylinder + valve/frame/regulator/lines/ECU", f"={I('cyl_mass')}+{I('kit_other_mass')}", "kg", ""),
 ("Mass removed: CNG cylinder + CNG kit", f"={I('cng_cyl_mass')}+{I('cng_kit_mass')}", "kg", ""),
 ("Net kerb mass change", "=B25-B26", "kg", "Negative = lighter than CNG configuration"),
 ("Peak power on petrol", f"={I('petrol_ps')}", "PS", "Donor spec"),
 ("Peak power on CNG (factory)", f"={I('cng_ps')}", "PS", "Third-party figure; official CNG rating not captured"),
 ("Estimated peak power on hydrogen (lean PFI)", f"={I('petrol_ps')}*{I('h2_power_factor')}", "PS", "About 30 percent air displacement plus lean operation (S-H2PWR)"),
 ("Power loss versus petrol", f"=1-{I('h2_power_factor')}", "fraction", ""),
 ("Power loss versus CNG", "=1-B30/B29", "fraction", ""),
 ("Power-to-mass, hydrogen mode, 4 occupants (kerb 1045 kg + 300 kg)", "=B30/((1045+B27+300)/1000)", "PS per tonne", "Urban duty reference: a loaded 800 cc hatchback is about 40 PS per tonne"),
 ("HCNG 18 vol% blend: hydrogen share of energy", "=(18*10.8)/(18*10.8+82*35.8)", "fraction", "Volumetric LHVs 10.8 and 35.8 MJ/Nm3 (S-HCNG); no vehicle modification"),
]
for i, (q, f, u, note) in enumerate(rows, start=5):
    we.cell(row=i, column=1, value=q).alignment = WRAP
    c = we.cell(row=i, column=2, value=f); c.number_format = "#,##0.00"
    we.cell(row=i, column=3, value=u); we.cell(row=i, column=4, value=note).alignment = WRAP
for rr in (16, 17, 22, 30):
    we.cell(row=rr, column=1).fill = SFILL; we.cell(row=rr, column=2).fill = SFILL; we.cell(row=rr, column=2).font = BOLD
ER = {"usable": "Energy_Range!$B$16", "range": "Energy_Range!$B$17", "range700": "Energy_Range!$B$18", "maxshare": "Energy_Range!$B$22",
      "kgday": "Energy_Range!$B$24", "netmass": "Energy_Range!$B$27", "h2ps": "Energy_Range!$B$30", "kmkg": "Energy_Range!$B$10",
      "effratio": "Energy_Range!$B$9", "hcng": "Energy_Range!$B$34", "petrolrange": "Energy_Range!$B$19", "dailyneed": "Energy_Range!$B$20", "fills": "Energy_Range!$B$21"}

# ------------------------------------------------------------------ TCO
wt = wb.create_sheet("TCO")
title(wt, "Ownership cost comparison for one vehicle: A continue on CNG, B hydrogen retrofit, C sell and buy BEV", "Nominal cash costs (Rs). Negative values are inflows (residual values). Years in columns; t0 = decision date.")
cols = ["C", "D", "E", "F", "G", "H"]   # t0..t5
put(wt, "A3", "Year index", bold=True)
for j, c in enumerate(cols):
    put(wt, f"{c}3", j, bold=True)
put(wt, "A4", "Calendar year")
for j, c in enumerate(cols):
    put(wt, f"{c}4", f"={I('decision_year')}+{c}3")
put(wt, "A5", "Discount factor")
for c in cols:
    put(wt, f"{c}5", f"=1/(1+{I('disc')})^{c}3", "0.000")
put(wt, "A6", "Annual km")
put(wt, "C6", 0)
for c in cols[1:]:
    put(wt, f"{c}6", f"={I('days')}*{I('km_day')}", "#,##0")
put(wt, "A7", "Petrol price (Rs/L)");  put(wt, "A8", "CNG price (Rs/kg)"); put(wt, "A9", "Delivered hydrogen price (Rs/kg)")
put(wt, "A10", "Hydrogen price trajectory multiplier (relative to year 1)"); put(wt, "A11", "Depot tariff (Rs/kWh)"); put(wt, "A12", "Public fast-charge price (Rs/kWh)")
put(wt, "A13", "Hydrogen consumed (kg)")
for c in cols[1:]:
    put(wt, f"{c}7", f"={I('petrol_price')}*(1+{I('fuel_esc')})^({c}3-1)", "0.0")
    put(wt, f"{c}8", f"={I('cng_price')}*(1+{I('fuel_esc')})^({c}3-1)", "0.0")
    put(wt, f"{c}9", f"={I('h2_price_y1')}*(1+{I('h2_change')})^({c}3-1)", "0")
    put(wt, f"{c}10", f"=(1+{I('h2_change')})^({c}3-1)", "0.000")
    put(wt, f"{c}11", f"={I('depot_tariff')}*(1+{I('elec_esc')})^({c}3-1)", "0.00")
    put(wt, f"{c}12", f"={I('pub_tariff')}*(1+{I('elec_esc')})^({c}3-1)", "0.00")
    put(wt, f"{c}13", f"={c}6*{I('h2_share')}*{I('h2_cons')}/100", "#,##0")

def block(start, label, lines, capital, residual):
    """lines: list of (label, formula_template using {c}) for annual rows (t1..t5). Returns dict of row numbers."""
    put(wt, f"A{start}", label, bold=True, fill=SFILL)
    for c in ["B"] + cols: wt[f"{c}{start}"].fill = SFILL
    r0 = start + 1
    put(wt, f"A{r0}", "Capital / transaction at t0"); put(wt, f"C{r0}", capital, "#,##0")
    for c in cols[1:]: put(wt, f"{c}{r0}", 0)
    rowmap = {"cap": r0}
    rr = r0 + 1
    for lab, tmpl in lines:
        put(wt, f"A{rr}", lab); put(wt, f"C{rr}", 0)
        for c in cols[1:]:
            put(wt, f"{c}{rr}", tmpl.format(c=c), "#,##0")
        rowmap[lab] = rr; rr += 1
    put(wt, f"A{rr}", "Residual value at end of horizon (inflow)"); 
    for c in cols[:-1]: put(wt, f"{c}{rr}", 0)
    put(wt, f"H{rr}", residual, "#,##0"); rowmap["resid"] = rr; rr += 1
    put(wt, f"A{rr}", "Total cash cost", bold=True)
    for c in cols: put(wt, f"{c}{rr}", f"=SUM({c}{r0}:{c}{rr-1})", "#,##0", bold=True)
    rowmap["total"] = rr; rr += 1
    put(wt, f"A{rr}", "Present value")
    for c in cols: put(wt, f"{c}{rr}", f"={c}{rr-1}*{c}$5", "#,##0")
    rowmap["pv"] = rr; rr += 1
    put(wt, f"A{rr}", "NPV of costs (Rs)", bold=True, fill=OFILL); put(wt, f"C{rr}", f"=SUM(C{rr-1}:H{rr-1})", "#,##0", bold=True, fill=OFILL)
    rowmap["npv"] = rr
    return rowmap

RA = block(16, "Option A: continue operating the CNG donor", [
    ("CNG fuel", "={c}6*(1-%s)/%s*{c}8" % (I('petrol_share_cng'), I('cng_kmkg'))),
    ("Petrol fuel (share of km)", "={c}6*%s/%s*{c}7" % (I('petrol_share_cng'), I('petrol_kml'))),
    ("Maintenance and tyres", "={c}6*%s" % I('maint_cng')),
    ("Insurance", "=%s" % I('ins_cng')),
    ("Cylinder periodic test (annualised)", "=%s/3" % I('cng_retest')),
    ("In-shift refuelling time cost", "=%s*%s*%s" % (I('time_cng_h'), I('days'), I('vot'))),
], "=0", f"=-{I('donor_value_end')}")
RB = block(RA["npv"] + 3, "Option B: retrofit the donor to hydrogen (H2-ICE, petrol backup retained)", [
    ("Hydrogen fuel", "={c}13*{c}9"),
    ("Petrol fuel (backup share of km)", "={c}6*(1-%s)/%s*{c}7" % (I('h2_share'), I('petrol_kml'))),
    ("Maintenance and tyres", "={c}6*%s" % I('maint_h2')),
    ("Insurance", "=%s" % I('ins_h2')),
    ("Hydrogen system inspection and cylinder requalification", "=%s" % I('h2_inspect_yr')),
    ("In-shift refuelling time and detour cost", "=%s*%s*%s" % (I('time_h2_h'), I('days'), I('vot'))),
], f"={I('kit_cost')}-{I('salvage_cng')}+{I('downtime_days')}*{I('lost_margin_day')}", f"=-({I('donor_value_end')}*{I('mod_resid_factor')}+{I('kit_resid')})")
r_exh2 = RB["npv"] + 1
put(wt, f"A{r_exh2}", "NPV of option B excluding hydrogen fuel (Rs)"); put(wt, f"C{r_exh2}", f"=C{RB['npv']}-SUMPRODUCT(D{RB['Hydrogen fuel']}:H{RB['Hydrogen fuel']},D5:H5)", "#,##0")
RC = block(r_exh2 + 3, "Option C: sell the donor and buy a compact fleet BEV", [
    ("Electricity (depot and public mix)", "={c}6*%s/100*(%s*{c}12+(1-%s)*{c}11)" % (I('bev_kwh100'), I('pub_share'), I('pub_share'))),
    ("Maintenance and tyres", "={c}6*%s" % I('maint_bev')),
    ("Insurance", "=%s" % I('ins_bev')),
    ("In-shift charging time cost", "=%s*%s*%s" % (I('time_bev_h'), I('days'), I('vot'))),
], f"={I('bev_price')}+{I('bev_onroad')}-{I('donor_value_now')}", f"=-{I('bev_resid')}")

# Summary
s = RC["npv"] + 3
put(wt, f"A{s}", "SUMMARY (active scenario)", bold=True, fill=HFILL, font=HDR)
for c in ["B"] + cols: wt[f"{c}{s}"].fill = HFILL
S = {}
def srow(label, formula, fmt="#,##0", key=None, note=None):
    global s
    s += 1
    put(wt, f"A{s}", label); put(wt, f"C{s}", formula, fmt)
    if note: put(wt, f"D{s}", note)
    if key: S[key] = f"TCO!$C${s}"
    return s
srow("Discounted km over horizon", "=SUMPRODUCT(D6:H6,D5:H5)", key="pvkm")
srow("NPV A: continue CNG (Rs)", f"=C{RA['npv']}", key="npvA")
srow("NPV B: hydrogen retrofit (Rs)", f"=C{RB['npv']}", key="npvB")
srow("NPV C: sell and buy BEV (Rs)", f"=C{RC['npv']}", key="npvC")
srow("Levelised cost per km, A (Rs/km)", f"={S['npvA']}/{S['pvkm']}", "0.00", key="lcA")
srow("Levelised cost per km, B (Rs/km)", f"={S['npvB']}/{S['pvkm']}", "0.00", key="lcB")
srow("Levelised cost per km, C (Rs/km)", f"={S['npvC']}/{S['pvkm']}", "0.00", key="lcC")
srow("Extra cost of B versus A over horizon (Rs)", f"={S['npvB']}-{S['npvA']}", key="dBA")
srow("Extra cost of B versus C over horizon (Rs)", f"={S['npvB']}-{S['npvC']}", key="dBC")
srow("Extra cost of C versus A over horizon (Rs)", f"={S['npvC']}-{S['npvA']}", key="dCA")
srow("Year-1 fuel cost per km, CNG mode (Rs/km)", f"=D8/{I('cng_kmkg')}", "0.00", key="fkm_cng")
srow("Year-1 fuel cost per km, hydrogen mode (Rs/km)", f"={I('h2_cons')}/100*D9", "0.00", key="fkm_h2")
srow("Year-1 fuel cost per km, petrol mode (Rs/km)", f"=D7/{I('petrol_kml')}", "0.00", key="fkm_petrol")
srow("Year-1 energy cost per km, BEV (Rs/km)", f"={I('bev_kwh100')}/100*({I('pub_share')}*D12+(1-{I('pub_share')})*D11)", "0.00", key="fkm_bev")
srow("Year-1 blended fuel cost per km, option B (Rs/km)", f"={I('h2_share')}*{S['fkm_h2']}+(1-{I('h2_share')})*{S['fkm_petrol']}", "0.00", key="fkm_B")
srow("Year-1 blended fuel cost per km, option A (Rs/km)", f"=(1-{I('petrol_share_cng')})*{S['fkm_cng']}+{I('petrol_share_cng')}*{S['fkm_petrol']}", "0.00", key="fkm_A")
srow("Year-1 non-fuel operating cost per km, A (Rs/km)", f"=(D{RA['Maintenance and tyres']}+D{RA['Insurance']}+D{RA['Cylinder periodic test (annualised)']}+D{RA['In-shift refuelling time cost']})/D6", "0.00", key="okm_A")
srow("Year-1 non-fuel operating cost per km, B (Rs/km)", f"=(D{RB['Maintenance and tyres']}+D{RB['Insurance']}+D{RB['Hydrogen system inspection and cylinder requalification']}+D{RB['In-shift refuelling time and detour cost']})/D6", "0.00", key="okm_B")
srow("Year-1 non-fuel operating cost per km, C (Rs/km)", f"=(D{RC['Maintenance and tyres']}+D{RC['Insurance']}+D{RC['In-shift charging time cost']})/D6", "0.00", key="okm_C")
srow("Discounted hydrogen kg, trajectory-weighted", f"=SUMPRODUCT(D13:H13,D10:H10,D5:H5)", key="pvkg_shaped")
srow("Discounted hydrogen kg, flat", f"=SUMPRODUCT(D13:H13,D5:H5)", key="pvkg_flat")
srow("Break-even year-1 hydrogen price versus A, same trajectory (Rs/kg)", f"=({S['npvA']}-C{r_exh2})/{S['pvkg_shaped']}", "0", key="be_A")
srow("Break-even flat hydrogen price versus A (Rs/kg)", f"=({S['npvA']}-C{r_exh2})/{S['pvkg_flat']}", "0", key="be_A_flat")
srow("Break-even year-1 hydrogen price versus C (BEV), same trajectory (Rs/kg)", f"=({S['npvC']}-C{r_exh2})/{S['pvkg_shaped']}", "0", key="be_C")
srow("Fuel-parity hydrogen price versus CNG (fuel cost per km equal) (Rs/kg)", f"={S['fkm_cng']}/({I('h2_cons')}/100)", "0", key="parity_cng")
srow("Fuel-parity hydrogen price versus petrol (Rs/kg)", f"={S['fkm_petrol']}/({I('h2_cons')}/100)", "0", key="parity_petrol")
srow("Maximum conversion cost for parity with A at the active hydrogen price (Rs)", f"=MAX(0,{I('kit_cost')}+({S['npvA']}-{S['npvB']}))", key="maxkit_A")
srow("Maximum conversion cost for parity with C at the active hydrogen price (Rs)", f"=MAX(0,{I('kit_cost')}+({S['npvC']}-{S['npvB']}))", key="maxkit_C")
srow("Year-1 operating saving of B versus A (Rs/yr; negative = B costs more)", f"=D{RA['total']}-D{RB['total']}", key="save1")
srow("Simple payback of conversion versus A (years)", f"=IF({S['save1']}>0,C{RB['cap']}/{S['save1']},\"none\")", "0.0", key="payback")
srow("Annuity factor (sum of discount factors, years 1-5)", "=SUM(D5:H5)", "0.000", key="af")
srow("Minimum annual km for payback within horizon (year-1 prices)", f"=IF(({S['fkm_A']}+{S['okm_A']}-{S['fkm_B']}-{S['okm_B']})>0,(C{RB['cap']}/{S['af']})/({S['fkm_A']}+{S['okm_A']}-{S['fkm_B']}-{S['okm_B']}),\"n/a\")", "#,##0", key="minkm")
# sensitivity coefficients
srow("Coefficient a (B-A): fixed and capital terms (Rs)", f"=C{RB['cap']}-C{RA['cap']}+SUMPRODUCT(D{RB['Insurance']}:H{RB['Insurance']},D5:H5)+SUMPRODUCT(D{RB['Hydrogen system inspection and cylinder requalification']}:H{RB['Hydrogen system inspection and cylinder requalification']},D5:H5)+SUMPRODUCT(D{RB['In-shift refuelling time and detour cost']}:H{RB['In-shift refuelling time and detour cost']},D5:H5)-SUMPRODUCT(D{RA['Insurance']}:H{RA['Insurance']},D5:H5)-SUMPRODUCT(D{RA['Cylinder periodic test (annualised)']}:H{RA['Cylinder periodic test (annualised)']},D5:H5)-SUMPRODUCT(D{RA['In-shift refuelling time cost']}:H{RA['In-shift refuelling time cost']},D5:H5)+(H{RB['resid']}-H{RA['resid']})*H5", key="aBA")
srow("Coefficient b (B-A): per-km non-hydrogen terms (Rs per km)", f"=SUMPRODUCT(D7:H7,D5:H5)*(1-{I('h2_share')})/{I('petrol_kml')}+{I('maint_h2')}*SUM(D5:H5)-SUMPRODUCT(D8:H8,D5:H5)*(1-{I('petrol_share_cng')})/{I('cng_kmkg')}-SUMPRODUCT(D7:H7,D5:H5)*{I('petrol_share_cng')}/{I('petrol_kml')}-{I('maint_cng')}*SUM(D5:H5)", "0.000", key="bBA")
srow("Coefficient c: hydrogen term (Rs per km per Rs/kg of year-1 price)", f"={I('h2_share')}*{I('h2_cons')}/100*SUMPRODUCT(D10:H10,D5:H5)", "0.00000", key="cH2")
srow("Check: a + b*km + c*km*P reproduces B-A (should be ~0)", f"={S['aBA']}+{S['bBA']}*D6+{S['cH2']}*D6*{I('h2_price_y1')}-{S['dBA']}", "0.00", key="chk")
srow("Coefficient a (B-C): fixed and capital terms (Rs)", f"=C{RB['cap']}-C{RC['cap']}+SUMPRODUCT(D{RB['Insurance']}:H{RB['Insurance']},D5:H5)+SUMPRODUCT(D{RB['Hydrogen system inspection and cylinder requalification']}:H{RB['Hydrogen system inspection and cylinder requalification']},D5:H5)+SUMPRODUCT(D{RB['In-shift refuelling time and detour cost']}:H{RB['In-shift refuelling time and detour cost']},D5:H5)-SUMPRODUCT(D{RC['Insurance']}:H{RC['Insurance']},D5:H5)-SUMPRODUCT(D{RC['In-shift charging time cost']}:H{RC['In-shift charging time cost']},D5:H5)+(H{RB['resid']}-H{RC['resid']})*H5", key="aBC")
srow("Coefficient b (B-C): per-km non-hydrogen terms (Rs per km)", f"=SUMPRODUCT(D7:H7,D5:H5)*(1-{I('h2_share')})/{I('petrol_kml')}+{I('maint_h2')}*SUM(D5:H5)-{I('bev_kwh100')}/100*({I('pub_share')}*SUMPRODUCT(D12:H12,D5:H5)+(1-{I('pub_share')})*SUMPRODUCT(D11:H11,D5:H5))-{I('maint_bev')}*SUM(D5:H5)", "0.000", key="bBC")
srow("Check: a + b*km + c*km*P reproduces B-C (should be ~0)", f"={S['aBC']}+{S['bBC']}*D6+{S['cH2']}*D6*{I('h2_price_y1')}-{S['dBC']}", "0.00", key="chk2")
wt.column_dimensions["A"].width = 70
for c in ["B"] + cols: wt.column_dimensions[c].width = 15
wt.column_dimensions["D"].width = 15

# ------------------------------------------------------------------ H2_Supply
wh = wb.create_sheet("H2_Supply")
title(wh, "Hydrogen supply: fleet demand, station sizing and delivered price build-up", "Delivered price = (production + transport + compression electricity + station capital recovery + O&M) x (1 + losses) x (1 + margin and taxes). Capital is recovered only here.")
hdr(wh, 4, ["Quantity", "Pilot (2028)", "Hub (2030)", "Unit", "Note"], [66, 16, 16, 14, 80])
H = {}
def hrow(rr, q, fp, fh, u, note="", key=None, fmt="#,##0.00"):
    wh.cell(row=rr, column=1, value=q).alignment = WRAP
    c = wh.cell(row=rr, column=2, value=fp); c.number_format = fmt
    c = wh.cell(row=rr, column=3, value=fh); c.number_format = fmt
    wh.cell(row=rr, column=4, value=u); wh.cell(row=rr, column=5, value=note).alignment = WRAP
    if key: H[key] = (f"H2_Supply!$B${rr}", f"H2_Supply!$C${rr}")
hrow(5, "Cars served", f"={I('pilot_cars')}", "=B27", "cars", "Hub: cars per station at design utilisation (row 27)", "cars")
hrow(6, "Hydrogen per car per operating day", f"={ER['kgday']}", f"={ER['kgday']}", "kg/car/day", "From Energy_Range", "kgcar")
hrow(7, "Fleet hydrogen demand per operating day", "=B5*B6", "=C5*C6", "kg/day", "", "demand")
hrow(8, "Station design capacity", f"={I('station_cap_pilot')}", f"={I('station_cap_2030')}", "kg/day", "", "cap")
hrow(9, "Station utilisation assumed for pricing", f"={I('station_util_pilot')}", f"={I('station_util_2030')}", "fraction", "Pilot station shared with bus/truck pilot users", "util", "0%")
hrow(10, "Hydrogen dispensed per year at that utilisation", "=B8*365*B9", "=C8*365*C9", "kg/yr", "", "kgyr", "#,##0")
hrow(11, "Fills per day (cars x fills)", f"=B5*{I('fills_day')}", f"=C5*{I('fills_day')}", "fills/day", "", "fillsday", "#,##0")
hrow(12, "Peak window length", 3, 3, "hours", "Start-of-shift window", "peakh")
for cc in ("B12", "C12"): wh[cc].font = BLUE; wh[cc].fill = IFILL
hrow(13, "Share of fills in the peak window", 0.5, 0.4, "fraction", "Assumption", "peakshare", "0%")
for cc in ("B13", "C13"): wh[cc].font = BLUE; wh[cc].fill = IFILL
hrow(14, "Fills per hour in the peak window", "=B11*B13/B12", "=C11*C13/C12", "fills/h", "", "fillsh", "0.0")
hrow(15, "Dispenser positions needed (6 fills per hour each, 1.2 kg fills at 350 bar)", "=ROUNDUP(B14/6,0)", "=ROUNDUP(C14/6,0)", "dispensers", "Assumption 6 fills/h per H35 dispenser incl. connection", "disp", "0")
hrow(16, "Compressor throughput needed (16 operating hours)", "=B8/16", "=C8/16", "kg/h", "Sized on design capacity", "comp")
hrow(17, "On-site storage buffer (1.5 days of demand)", "=1.5*B7", "=1.5*C7", "kg", "Cascade at 450 bar", "buffer")
hrow(18, "Tube-trailer deliveries per week", f"=B7*7/{I('trailer_kg')}", f"=C7*7/{I('trailer_kg')}", "deliveries/week", "", "deliv", "0.0")
hrow(19, "Production cost at plant gate", f"={I('h2_prod_cost')}", f"={I('h2_prod_cost_2030')}", "Rs/kg", "", "prod", "0")
hrow(20, "Transport (tube trailer)", f"={I('transport_cost')}", f"={I('transport_cost')}", "Rs/kg", "", "trans", "0")
hrow(21, "Compression and dispensing electricity", f"={I('comp_kwh')}*{I('ind_tariff')}", f"={I('comp_kwh')}*{I('ind_tariff')}", "Rs/kg", "", "elec", "0")
hrow(22, "Station capex", f"={I('station_capex_pilot')}", f"={I('station_capex_2030')}", "Rs", "", "capex", "#,##0")
hrow(23, "Capital recovery factor", f"={I('disc')}*(1+{I('disc')})^{I('station_life')}/((1+{I('disc')})^{I('station_life')}-1)", f"={I('disc')}*(1+{I('disc')})^{I('station_life')}/((1+{I('disc')})^{I('station_life')}-1)", "fraction", "", "crf", "0.000")
hrow(24, "Station capital recovery per kg", "=B22*B23/B10", "=C22*C23/C10", "Rs/kg", "At the assumed utilisation", "caprec", "0")
hrow(25, "Station fixed O&M per kg", f"=B22*{I('station_om')}/B10", f"=C22*{I('station_om')}/C10", "Rs/kg", "", "om", "0")
hrow(26, "Delivered price at dispenser", f"=(B19+B20+B21+B24+B25)*(1+{I('h2_loss')})*(1+{I('h2_margin_tax')})", f"=(C19+C20+C21+C24+C25)*(1+{I('h2_loss')})*(1+{I('h2_margin_tax')})", "Rs/kg", "Key output; compare with Inputs h2_price_y1", "delivered", "0")
hrow(27, "Cars a station can serve at design utilisation", "=B8*B9/B6", "=C8*C9/C6", "cars", "", "carsper", "0")
hrow(28, "Utilisation implied by the car fleet alone", "=B7/B8", "=C7/C8", "fraction", "", "utilimpl", "0%")
wh["A26"].fill = SFILL; wh["B26"].fill = SFILL; wh["C26"].fill = SFILL; wh["B26"].font = BOLD; wh["C26"].font = BOLD
# utilisation table
put(wh, "A31", "Delivered price versus station utilisation (Rs/kg)", bold=True)
hdr(wh, 32, ["Utilisation", "Pilot station (2028)", "Hub station (2030)"])
for k, u in enumerate([0.2, 0.35, 0.5, 0.65, 0.8, 0.95]):
    rr = 33 + k
    put(wh, f"A{rr}", u, "0%")
    put(wh, f"B{rr}", f"=($B$19+$B$20+$B$21+($B$22*$B$23+$B$22*{I('station_om')})/($B$8*365*A{rr}))*(1+{I('h2_loss')})*(1+{I('h2_margin_tax')})", "0")
    put(wh, f"C{rr}", f"=($C$19+$C$20+$C$21+($C$22*$C$23+$C$22*{I('station_om')})/($C$8*365*A{rr}))*(1+{I('h2_loss')})*(1+{I('h2_margin_tax')})", "0")
put(wh, "A40", "Utilisation needed to reach a target delivered price", bold=True)
hdr(wh, 41, ["Target", "Target price (Rs/kg)", "Pilot station utilisation needed", "Hub station utilisation needed"])
targets = [("CNG fuel-parity price (from TCO)", f"={S['parity_cng']}"), ("Full-TCO break-even versus continuing on CNG (from TCO)", f"={S['be_A']}"), ("Petrol fuel-parity price (from TCO)", f"={S['parity_petrol']}"), ("Full-TCO break-even versus BEV (from TCO)", f"={S['be_C']}")]
for k, (lab, f) in enumerate(targets):
    rr = 42 + k
    put(wh, f"A{rr}", lab); put(wh, f"B{rr}", f, "0")
    for colL, col in (("C", "B"), ("D", "C")):
        put(wh, f"{colL}{rr}", f"=IF(B{rr}/((1+{I('h2_loss')})*(1+{I('h2_margin_tax')}))-(${col}$19+${col}$20+${col}$21)<=0,\"not reachable at any utilisation\",MIN(9.99,(${col}$22*${col}$23+${col}$22*{I('station_om')})/(${col}$8*365)/(B{rr}/((1+{I('h2_loss')})*(1+{I('h2_margin_tax')}))-(${col}$19+${col}$20+${col}$21))))", "0%")
put(wh, "A47", "Note: values above 100 percent mean the target cannot be met even at full utilisation; 'not reachable' means production plus transport plus electricity alone exceed the target.")
H2S = {"delivered_pilot": "H2_Supply!$B$26", "delivered_hub": "H2_Supply!$C$26", "carsper_hub": "H2_Supply!$C$27", "demand_pilot": "H2_Supply!$B$7", "disp_pilot": "H2_Supply!$B$15", "deliv_pilot": "H2_Supply!$B$18", "buffer_pilot": "H2_Supply!$B$17"}

# ------------------------------------------------------------------ Market
wm = wb.create_sheet("Market")
title(wm, "Bottom-up addressable market and supply-constrained deployment", "Funnel from national CNG stock to what stations can actually serve by 2030.")
hdr(wm, 4, ["Step", "Vehicles", "Share applied", "Note"], [70, 16, 14, 80])
mrows = [
 ("CNG vehicles in India, all categories", f"={I('cng_stock')}", "", "Input, class A"),
 ("Passenger cars among them", f"=B5*{I('cng_pv_share')}", f"={I('cng_pv_share')}", "Share input"),
 ("Technically eligible: factory-fitted, boot-cylinder layout, under 6 years old at 2028", f"=B6*{I('eligible_share')}", f"={I('eligible_share')}", "Excludes older vehicles and layouts without a compatible cylinder bay"),
 ("In commercial fleets (taxi, aggregator, corporate, institutional)", f"=B7*{I('fleet_share')}", f"={I('fleet_share')}", "Private owners excluded from the first segment"),
 ("In cities with a hydrogen hub station by 2030", f"=B8*{I('hub_share')}", f"={I('hub_share')}", "Delhi-NCR, Gujarat corridor, Pune-Mumbai, Kochi and similar"),
 ("Plausible early adopters (return-to-base fleets willing to convert)", f"=B9*{I('adopter_share')}", f"={I('adopter_share')}", "Hypothesis to be validated with fleet interviews"),
 ("Supply-constrained capacity: stations x cars per station", f"={I('hub_stations_2030')}*{H2S['carsper_hub']}", "", "From H2_Supply"),
 ("Realistic 2030 converted fleet (minimum of demand and supply)", "=MIN(B10,B11)", "", "Key output"),
 ("Round 1 claim for 2030", 100000, "", "For comparison"),
]
for i, (a, b, c, d) in enumerate(mrows, start=5):
    wm.cell(row=i, column=1, value=a).alignment = WRAP
    wm.cell(row=i, column=2, value=b).number_format = "#,##0"
    if c: wm.cell(row=i, column=3, value=c).number_format = "0%"
    wm.cell(row=i, column=4, value=d).alignment = WRAP
wm["A12"].fill = SFILL; wm["B12"].fill = SFILL; wm["B12"].font = BOLD
MK = {"eligible": "Market!$B$7", "fleet": "Market!$B$8", "hub": "Market!$B$9", "adopters": "Market!$B$10", "supply": "Market!$B$11", "fleet2030": "Market!$B$12", "pv": "Market!$B$6"}

# ------------------------------------------------------------------ Pilot_Budget
wp = wb.create_sheet("Pilot_Budget")
title(wp, "Programme budget by phase and rollout quantities", "Rs. Phases run October 2026 to September 2030. Contingency applied to all phases.")
hdr(wp, 4, ["Phase", "Line item", "Quantity", "Unit cost (Rs)", "Total (Rs)", "Class", "Basis"], [30, 66, 10, 16, 18, 8, 70])
budget = [
 ("Phase 0: Feasibility and validation (Oct 2026 - Mar 2027)", [
   ("Regulator and test-agency consultations, route definition (AISC, MoRTH, ARAI/ICAT, PESO)", 1, 2500000, "C", "Engineering time, travel, legal review"),
   ("Fleet and fuel-partner validation: 30 operator interviews, duty-cycle telematics on 20 cars", 1, 2500000, "C", "Customer demand is a hypothesis; this buys the evidence"),
   ("Donor inspection, packaging study, CAD and mule vehicle (boot mock-up)", 1, 4000000, "C", ""),
 ]),
 ("Phase 1: Engineering and controlled validation (Apr 2027 - Mar 2028)", [
   ("Hydrogen engine test-cell time and instrumentation (calibration, NOx, abnormal combustion, 500 h)", 1, 30000000, "C", "Hydrogen test cells exist at ARAI, iCAT and IOCL R&D (S-TEST)"),
   ("Prototype conversions (3 vehicles) at pilot kit cost", 3, "=BOM!$G$40", "B", "BOM pilot cost"),
   ("Prototype donor vehicles (used Tour S CNG)", 3, 500000, "C", ""),
   ("Storage system qualification samples and tests (burst, cycling, bonfire, drop, permeation)", 1, 15000000, "C", "UN GTR 13 / R134 type tests via supplier and PESO"),
   ("Vehicle-level safety tests (leak, sled/crash structure, ventilation) at test agency", 1, 12000000, "C", ""),
   ("Engineering team (8 FTE x 12 months)", 96, 250000, "C", "Rs 2.5 lakh per FTE-month fully loaded"),
 ]),
 ("Phase 2: Certification and pilot build (Apr 2028 - Mar 2029)", [
   ("Kit type approval and emissions testing at ARAI/ICAT (analogous to CNG kit approval)", 1, 10000000, "C", "Industry reports Rs 40-50 lakh for CNG kit approval (S-TAFEE); hydrogen scope larger"),
   ("Durability demonstration (2 vehicles x 80,000 km accelerated)", 1, 8000000, "C", ""),
   ("Pilot conversions (30 vehicles) at pilot kit cost", "=Inputs!$F$%d" % ROW['pilot_cars'], "=BOM!$G$40", "B", "BOM pilot cost"),
   ("Instrumentation and telematics (30 cars + 20 comparison cars)", 50, 60000, "C", "CAN logger, GPS, hydrogen sensor logging"),
   ("Hydrogen dispensing point at partner site (compressor, cascade, one dispenser, safety, PESO)", 1, "=Inputs!$F$%d" % ROW['station_capex_pilot'], "B", "Input station_capex_pilot; delivered hydrogen, no on-site electrolyser"),
   ("Workshop upgrade (ventilation, detection, training) at 2 service points", 2, 4000000, "C", "NFPA 2 type ventilation and detection"),
 ]),
 ("Phase 3: Pilot operation and evaluation (Apr 2029 - Sep 2030)", [
   ("Hydrogen fuel for 30 cars, 18 months (kg at delivered pilot price)", f"={I('pilot_cars')}*{ER['kgday']}*{I('days')}*1.5", f"={H2S['delivered_pilot']}", "B", "Quantity from Energy_Range and H2_Supply"),
   ("Operations, safety officer, data analysis and independent evaluation (18 months)", 18, 1500000, "C", "Per month"),
   ("Quarterly emissions and consumption tests at test agency", 6, 800000, "C", ""),
   ("Insurance, incident reserve and driver training", 1, 6000000, "C", ""),
 ]),
]
r = 5; phase_total_rows = []
for phase, items in budget:
    c = wp.cell(row=r, column=1, value=phase); c.font = Font(bold=True, color="016F49"); c.fill = SFILL
    for col in range(2, 8): wp.cell(row=r, column=col).fill = SFILL
    r += 1; startr = r
    for name, qty, uc, cls, basis in items:
        wp.cell(row=r, column=2, value=name).alignment = WRAP
        cq = wp.cell(row=r, column=3, value=qty); cq.number_format = "#,##0.0"
        cu = wp.cell(row=r, column=4, value=uc); cu.number_format = "#,##0"
        if not (isinstance(qty, str) and qty.startswith("=")): cq.font = BLUE; cq.fill = IFILL
        if not (isinstance(uc, str) and uc.startswith("=")): cu.font = BLUE; cu.fill = IFILL
        wp.cell(row=r, column=5, value=f"=C{r}*D{r}").number_format = "#,##0"
        wp.cell(row=r, column=6, value=cls); wp.cell(row=r, column=7, value=basis).alignment = WRAP
        r += 1
    wp.cell(row=r, column=2, value="Phase subtotal").font = BOLD
    wp.cell(row=r, column=5, value=f"=SUM(E{startr}:E{r-1})").number_format = "#,##0"; wp.cell(row=r, column=5).font = BOLD
    phase_total_rows.append(r); r += 2
put(wp, f"B{r}", "Subtotal all phases", bold=True); put(wp, f"E{r}", "=" + "+".join(f"E{x}" for x in phase_total_rows), "#,##0", bold=True); subt = r; r += 1
put(wp, f"B{r}", "Contingency (share of subtotal)"); put(wp, f"C{r}", 0.15, "0%", font=BLUE, fill=IFILL); put(wp, f"E{r}", f"=E{subt}*C{r}", "#,##0"); cont = r; r += 1
put(wp, f"B{r}", "Total programme budget to September 2030 (Rs)", bold=True, fill=SFILL); put(wp, f"E{r}", f"=E{subt}+E{cont}", "#,##0", bold=True, fill=SFILL); tot = r; r += 1
put(wp, f"B{r}", "Total in Rs crore"); put(wp, f"E{r}", f"=E{tot}/10000000", "0.0"); totcr = r; r += 2
put(wp, f"B{r}", "Proposed funding split (shares are proposals, not commitments)", bold=True); r += 1
for lab, sh in [("Suzuki R&D Center India / Maruti Suzuki (engineering, prototypes, test cells)", 0.40), ("Public support sought (MNRE NGHM R&D or pilot scheme, state hydrogen policy)", 0.35), ("Fuel and station partner (OMC or gas utility): dispensing point", 0.15), ("Fleet partner (vehicles, drivers, operations)", 0.10)]:
    put(wp, f"B{r}", lab); put(wp, f"C{r}", sh, "0%", font=BLUE, fill=IFILL); put(wp, f"E{r}", f"=C{r}*E{tot}", "#,##0"); r += 1
r += 1
put(wp, f"B{r}", "Rollout quantities (conditional expansion after gates)", bold=True); r += 1
hdr(wp, r, ["", "Item", "2028", "2029", "2030", "", "Note"]); r += 1
put(wp, f"B{r}", "Converted cars in operation (cumulative)"); put(wp, f"C{r}", 3); put(wp, f"D{r}", f"={I('pilot_cars')}"); put(wp, f"E{r}", f"={MK['fleet2030']}", "#,##0"); put(wp, f"G{r}", "2030 value from Market sheet (supply-constrained scenario, conditional on gates)"); roll_cars = r; r += 1
put(wp, f"B{r}", "Fleet-hub stations serving cars"); put(wp, f"C{r}", 1); put(wp, f"D{r}", 1); put(wp, f"E{r}", f"={I('hub_stations_2030')}"); r += 1
put(wp, f"B{r}", "Hydrogen demand from cars (t/yr)"); put(wp, f"C{r}", f"=C{roll_cars}*{ER['kgday']}*{I('days')}/1000", "0.0"); put(wp, f"D{r}", f"=D{roll_cars}*{ER['kgday']}*{I('days')}/1000", "0.0"); put(wp, f"E{r}", f"=E{roll_cars}*{ER['kgday']}*{I('days')}/1000", "0.0"); r += 1
PB = {"total": f"Pilot_Budget!$E${tot}", "totalcr": f"Pilot_Budget!$E${totcr}", "phases": [f"Pilot_Budget!$E${x}" for x in phase_total_rows]}
for k, x in enumerate(phase_total_rows):
    PB[f"phase{k}"] = f"Pilot_Budget!$E${x}"

# ------------------------------------------------------------------ Emissions
wem = wb.create_sheet("Emissions")
title(wem, "Emissions per km and at fleet scale, same service boundary for all options", "Tailpipe, well-to-tank and amortised manufacturing. Hydrogen combustion emits NOx (not CO2); see NOx rows.")
hdr(wem, 4, ["Quantity", "Value", "Unit", "Note"], [70, 16, 16, 80])
erows = [
 ("A: CNG tailpipe CO2 per km (CNG share of km)", f"=(1-{I('petrol_share_cng')})/{I('cng_kmkg')}*{I('ef_cng')}*1000", "g/km", ""),
 ("A: petrol tailpipe CO2 per km (petrol share)", f"={I('petrol_share_cng')}/{I('petrol_kml')}*{I('ef_petrol')}*1000", "g/km", ""),
 ("A: well-to-tank CO2e per km", f"=B5*{I('wtt_cng')}+B6*{I('wtt_petrol')}", "g/km", "Uplift factors on tailpipe"),
 ("A: total well-to-wheel CO2e per km", "=B5+B6+B7", "g/km", "Key"),
 ("B: hydrogen share of km", f"={I('h2_share')}", "fraction", ""),
 ("B: hydrogen consumption", f"={I('h2_cons')}", "kg/100 km", ""),
 ("B: well-to-wheel CO2e per km, green hydrogen", f"=B9*B10/100*{I('ci_h2_green')}*1000+(1-B9)/{I('petrol_kml')}*{I('ef_petrol')}*(1+{I('wtt_petrol')})*1000", "g/km", "Tailpipe CO2 on hydrogen km is zero; petrol backup km counted"),
 ("B: well-to-wheel CO2e per km, grid-electrolysis hydrogen", f"=B9*B10/100*{I('ci_h2_grid')}*1000+(1-B9)/{I('petrol_kml')}*{I('ef_petrol')}*(1+{I('wtt_petrol')})*1000", "g/km", "Reversal case"),
 ("B: well-to-wheel CO2e per km, grey (SMR) hydrogen", f"=B9*B10/100*{I('ci_h2_grey')}*1000+(1-B9)/{I('petrol_kml')}*{I('ef_petrol')}*(1+{I('wtt_petrol')})*1000", "g/km", "Reversal case"),
 ("B: retrofit kit manufacturing amortised over horizon km", f"={I('kit_mfg')}*1000000/({I('days')}*{I('km_day')}*{I('horizon')})", "g/km", ""),
 ("B: total per km incl. kit manufacturing, green hydrogen", "=B11+B14", "g/km", "Key"),
 ("C: BEV electricity per km at 2025 grid factor", f"={I('bev_kwh100')}/100*{I('grid_now')}*1000", "g/km", "Metered kWh already include charging losses"),
 ("C: BEV electricity per km at 2030 grid factor", f"={I('bev_kwh100')}/100*{I('grid_2030')}*1000", "g/km", ""),
 ("C: BEV manufacturing amortised per km", f"={I('bev_mfg')}*1000000/{I('bev_life_km')}", "g/km", "New vehicle and battery; counterfactual is keeping the donor"),
 ("C: total per km incl. manufacturing, 2025 grid", "=B16+B18", "g/km", "Key"),
 ("C: total per km incl. manufacturing, 2030 grid", "=B17+B18", "g/km", "Key"),
 ("Reduction of B (green) versus A", "=1-B15/B8", "fraction", ""),
 ("Reduction of C (2030 grid) versus A", "=1-B20/B8", "fraction", "Negative = BEV replacement emits more than continuing on CNG within the horizon"),
 ("Grid factor at which BEV equals green-hydrogen retrofit per km", f"=(B15-B18)/({I('bev_kwh100')}/100)/1000", "kg CO2/kWh", "Reversal threshold"),
 ("Hydrogen carbon intensity at which retrofit equals continuing on CNG", f"=(B8-(1-B9)/{I('petrol_kml')}*{I('ef_petrol')}*(1+{I('wtt_petrol')})*1000-B14)/(B9*B10/100*1000)", "kg CO2e/kg H2", "Retrofit is worse than CNG above this hydrogen carbon intensity"),
 ("Per-car CO2e avoided over the horizon, B (green) versus A", f"=(B8-B15)*{I('days')}*{I('km_day')}*{I('horizon')}/1000000", "t CO2e", ""),
 ("Abatement cost of the retrofit versus continuing on CNG (active scenario)", f"=IF(B25>0,{S['dBA']}/B25,\"n/a\")", "Rs per t CO2e", "Extra ownership cost divided by CO2e avoided"),
 ("Pilot fleet (30 cars) CO2e avoided per year, green hydrogen", f"={I('pilot_cars')}*(B8-B15)*{I('days')}*{I('km_day')}/1000000", "t CO2e/yr", ""),
 ("2030 converted fleet CO2e avoided per year, green hydrogen", f"={MK['fleet2030']}*(B8-B15)*{I('days')}*{I('km_day')}/1000000", "t CO2e/yr", "Supply-constrained fleet from Market"),
 ("2030 converted fleet hydrogen demand", f"={MK['fleet2030']}*{ER['kgday']}*{I('days')}/1000", "t/yr", ""),
 ("NOx: BS-VI limit for M1 petrol", f"={I('nox_bs6')}", "mg/km", "Applies to the converted vehicle by analogy; test procedure for H2-ICE retrofits does not exist yet"),
 ("NOx: lean hydrogen combustion engine-out (lambda above 2) reported range", "5 to 20", "mg/km class", "Literature indicates near-zero NOx above lambda about 2 (S-NOX); transients and high load exceed it, hence aftertreatment provision"),
]
for i, (q, f, u, n) in enumerate(erows, start=5):
    wem.cell(row=i, column=1, value=q).alignment = WRAP
    c = wem.cell(row=i, column=2, value=f); c.number_format = "#,##0.0"
    wem.cell(row=i, column=3, value=u); wem.cell(row=i, column=4, value=n).alignment = WRAP
for rr in (8, 15, 19, 20):
    wem.cell(row=rr, column=1).fill = SFILL; wem.cell(row=rr, column=2).fill = SFILL; wem.cell(row=rr, column=2).font = BOLD
EM = {"A": "Emissions!$B$8", "Bgreen": "Emissions!$B$15", "Bgrid": "Emissions!$B$12", "Bgrey": "Emissions!$B$13", "C25": "Emissions!$B$19", "C30": "Emissions!$B$20",
      "redB": "Emissions!$B$21", "redC": "Emissions!$B$22", "gridthr": "Emissions!$B$23", "cithr": "Emissions!$B$24", "avoidcar": "Emissions!$B$25", "abate": "Emissions!$B$26", "pilot_t": "Emissions!$B$27", "fleet_t": "Emissions!$B$28", "fleet_h2": "Emissions!$B$29"}

# ------------------------------------------------------------------ Sensitivities
wsn = wb.create_sheet("Sensitivities")
title(wsn, "When does the recommendation change? Grids use the closed-form decomposition from the TCO sheet (same trajectory shape, active scenario for all other inputs).", "Values in Rs lakh over the horizon; negative = the hydrogen retrofit is cheaper than the comparator.")
put(wsn, "A4", "Grid 1: retrofit minus continue-on-CNG (Rs lakh) by year-1 delivered hydrogen price (rows) and annual km (columns)", bold=True)
kms = [30000, 40000, 50000, 60000, 70000]
prices = [100, 150, 200, 250, 300, 400, 500, 600, 800]
put(wsn, "A5", "Rs/kg \\ km/yr", bold=True)
for j, km in enumerate(kms):
    put(wsn, f"{get_column_letter(2+j)}5", km, "#,##0", bold=True)
for i, p in enumerate(prices):
    rr = 6 + i
    put(wsn, f"A{rr}", p, "0", bold=True)
    for j, km in enumerate(kms):
        col = get_column_letter(2 + j)
        put(wsn, f"{col}{rr}", f"=({S['aBA']}+{S['bBA']}*{col}$5+{S['cH2']}*{col}$5*$A{rr})/100000", "0.0")
g2 = 6 + len(prices) + 2
put(wsn, f"A{g2}", "Grid 2: retrofit minus sell-and-buy-BEV (Rs lakh) by year-1 hydrogen price (rows) and BEV price in Rs lakh (columns)", bold=True)
bevs = [9, 10, 11, 12, 13, 14]
put(wsn, f"A{g2+1}", "Rs/kg \\ BEV price", bold=True)
for j, b in enumerate(bevs):
    put(wsn, f"{get_column_letter(2+j)}{g2+1}", b, "0", bold=True)
for i, p in enumerate(prices):
    rr = g2 + 2 + i
    put(wsn, f"A{rr}", p, "0", bold=True)
    for j, b in enumerate(bevs):
        col = get_column_letter(2 + j)
        put(wsn, f"{col}{rr}", f"=({S['aBC']}-({col}${g2+1}*100000-{I('bev_price')})+{S['bBC']}*TCO!$D$6+{S['cH2']}*TCO!$D$6*$A{rr})/100000", "0.0")
g3 = g2 + 2 + len(prices) + 2
put(wsn, f"A{g3}", "Grid 3: retrofit minus continue-on-CNG (Rs lakh) by year-1 hydrogen price (rows) and installed kit cost in Rs lakh (columns)", bold=True)
kits = [1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
put(wsn, f"A{g3+1}", "Rs/kg \\ kit cost", bold=True)
for j, k in enumerate(kits):
    put(wsn, f"{get_column_letter(2+j)}{g3+1}", k, "0.0", bold=True)
for i, p in enumerate(prices):
    rr = g3 + 2 + i
    put(wsn, f"A{rr}", p, "0", bold=True)
    for j, k in enumerate(kits):
        col = get_column_letter(2 + j)
        put(wsn, f"{col}{rr}", f"=({S['aBA']}+({col}${g3+1}*100000-{I('kit_cost')})+{S['bBA']}*TCO!$D$6+{S['cH2']}*TCO!$D$6*$A{rr})/100000", "0.0")
g4 = g3 + 2 + len(prices) + 2
put(wsn, f"A{g4}", "One-at-a-time sensitivities: extra cost of retrofit versus continuing on CNG (Rs lakh), other inputs at active values", bold=True)
hdr(wsn, g4 + 1, ["Driver", "Low value", "High value", "Extra cost at low", "Extra cost at high", "Note"])
oat = [
 ("Year-1 delivered hydrogen price (Rs/kg)", f"=Inputs!$E${ROW['h2_price_y1']}", f"=Inputs!$D${ROW['h2_price_y1']}", f"=({S['aBA']}+{S['bBA']}*TCO!$D$6+{S['cH2']}*TCO!$D$6*B{{r}})/100000", f"=({S['aBA']}+{S['bBA']}*TCO!$D$6+{S['cH2']}*TCO!$D$6*C{{r}})/100000", "Upside and downside inputs"),
 ("Installed kit cost (Rs)", f"=Inputs!$E${ROW['kit_cost']}", f"=Inputs!$D${ROW['kit_cost']}", f"=({S['dBA']}+(B{{r}}-{I('kit_cost')}))/100000", f"=({S['dBA']}+(C{{r}}-{I('kit_cost')}))/100000", ""),
 ("Annual km", "=30000", "=70000", f"=({S['aBA']}+{S['bBA']}*B{{r}}+{S['cH2']}*B{{r}}*{I('h2_price_y1')})/100000", f"=({S['aBA']}+{S['bBA']}*C{{r}}+{S['cH2']}*C{{r}}*{I('h2_price_y1')})/100000", "More km increases the fuel-cost penalty at current hydrogen prices"),
 ("Hydrogen consumption (kg/100 km)", f"=Inputs!$E${ROW['h2_cons']}", f"=Inputs!$D${ROW['h2_cons']}", f"=({S['dBA']}+{S['cH2']}*(B{{r}}/{I('h2_cons')}-1)*TCO!$D$6*{I('h2_price_y1')})/100000", f"=({S['dBA']}+{S['cH2']}*(C{{r}}/{I('h2_cons')}-1)*TCO!$D$6*{I('h2_price_y1')})/100000", "Scales the hydrogen term"),
 ("CNG price (Rs/kg)", f"=Inputs!$E${ROW['cng_price']}", f"=Inputs!$D${ROW['cng_price']}", f"=({S['dBA']}-(B{{r}}/{I('cng_price')}-1)*SUMPRODUCT(TCO!$D$8:$H$8,TCO!$D$5:$H$5)*TCO!$D$6*(1-{I('petrol_share_cng')})/{I('cng_kmkg')})/100000", f"=({S['dBA']}-(C{{r}}/{I('cng_price')}-1)*SUMPRODUCT(TCO!$D$8:$H$8,TCO!$D$5:$H$5)*TCO!$D$6*(1-{I('petrol_share_cng')})/{I('cng_kmkg')})/100000", "Dearer CNG helps the retrofit"),
 ("Share of km on hydrogen", f"=Inputs!$E${ROW['h2_share']}", f"=Inputs!$D${ROW['h2_share']}", f"=({S['dBA']}+(B{{r}}-{I('h2_share')})*TCO!$D$6*({I('h2_cons')}/100*SUMPRODUCT(TCO!$D$9:$H$9,TCO!$D$5:$H$5)-SUMPRODUCT(TCO!$D$7:$H$7,TCO!$D$5:$H$5)/{I('petrol_kml')}))/100000", f"=({S['dBA']}+(C{{r}}-{I('h2_share')})*TCO!$D$6*({I('h2_cons')}/100*SUMPRODUCT(TCO!$D$9:$H$9,TCO!$D$5:$H$5)-SUMPRODUCT(TCO!$D$7:$H$7,TCO!$D$5:$H$5)/{I('petrol_kml')}))/100000", "At current prices, more hydrogen km cost more than petrol km"),
]
for i, (lab, lo, hi, flo, fhi, note) in enumerate(oat):
    rr = g4 + 2 + i
    put(wsn, f"A{rr}", lab); put(wsn, f"B{rr}", lo, "#,##0.##"); put(wsn, f"C{rr}", hi, "#,##0.##")
    put(wsn, f"D{rr}", flo.format(r=rr), "0.0"); put(wsn, f"E{rr}", fhi.format(r=rr), "0.0"); put(wsn, f"F{rr}", note)
wsn.column_dimensions["A"].width = 46
for col in "BCDEFG": wsn.column_dimensions[col].width = 16
SN = {"grid1_top": 6, "g2": g2, "g3": g3, "g4": g4}

# ------------------------------------------------------------------ Donor_Tech
wd = wb.create_sheet("Donor_Tech")
title(wd, "Donor platform and technology-route comparison", "Donor figures are manufacturer-declared unless marked third-party; hydrogen figures are model outputs.")
hdr(wd, 4, ["Criterion", "Dzire Tour S CNG (primary)", "WagonR S-CNG / Tour H3", "Ertiga S-CNG / Tour M", "Eeco CNG", "Source / note"], [44, 24, 24, 24, 20, 60])
drows = [
 ("Engine", "1197 cc, 4-cyl K12N", "998 cc, 3-cyl K10C", "1462 cc, 4-cyl K15C", "1197 cc, 4-cyl K12N", "S-DONOR"),
 ("Power petrol / CNG (PS)", "81.6 / ~70 (CNG third-party)", "~66 / ~57 (CNG third-party)", "103 / 87.8", "82 / n.a.", "S-DONOR; official CNG ratings for 1.0 and 1.2 L cars not captured"),
 ("Kerb mass CNG (kg)", "~1045 (third-party)", "~850-930", "1250-1255", "1085", "S-DONOR"),
 ("Gross vehicle weight (kg)", "1375 (Dzire S-CNG)", "1340", "1820", "n.a.", "S-DONOR"),
 ("CNG cylinder water volume (L) and location", "55, boot, transverse", "60, boot", "60, boot", "65, under rear floor area", "S-DONOR"),
 ("Boot volume without cylinder (L)", "382", "335", "209 (3rd row up)", "van", "S-DONOR"),
 ("Declared CNG economy (km/kg)", "32.1", "34.4", "26.5", "27.0", "S-DONOR (MIDC declared); fleet real-world 24-30"),
 ("Ground clearance (mm)", "163", "165", "185", "160", "Under-floor hydrogen cylinders not credible; boot bay only"),
 ("Fleet presence (taxi / aggregator)", "Very high (app cabs, airport)", "High (Delhi taxis, private)", "Medium (outstation, 7 seats)", "Medium (tier-2 taxi, school van)", "Qualitative"),
 ("Hydrogen cylinder that fits the bay (350 bar)", "60 L composite, OD 400 x 767 mm", "60 L composite", "60-74 L composite", "60-74 L composite", "Luxfer G-Stor Pro V060H35 example: 36 kg, 1.45 kg H2 (S-CYL)"),
 ("Power margin after 45 percent hydrogen derate", "adequate for urban duty", "marginal (3-cyl, 41 PS)", "best (48 PS)", "adequate", "Model estimate"),
 ("Verdict as first donor", "PRIMARY: fleet workhorse, 4-cyl, sedan boot", "Alternative: private/taxi hatch, weakest power", "Alternative for larger storage (2 cylinders, 5-seat mode)", "Alternative for tier-2 fleets", ""),
]
for i, row in enumerate(drows, start=5):
    for j, v in enumerate(row, start=1):
        wd.cell(row=i, column=j, value=v).alignment = WRAP
r = 5 + len(drows) + 2
put(wd, f"A{r}", "Technology route comparison for the same donor and duty (matched criteria)", bold=True); r += 1
hdr(wd, r, ["Criterion", "H2-ICE retrofit (selected)", "Fuel-cell conversion", "New BEV (sell donor)", "Continue on CNG", "Basis"]); r += 1
trows = [
 ("What changes", "Fuel storage and delivery, injectors, ECU, sensors; engine retained", "Entire powertrain: stack, battery, motor, inverter, cooling, tank, controls", "New vehicle", "Nothing", "Engineering scope"),
 ("Conversion or purchase cost (Rs lakh, model)", "=BOM!$F$42", "15 to 25 (pilot), 8 to 12 (volume)", f"={I('bev_price')}/100000", "0", "BOM; fuel-cell figures are estimates from stack and battery cost literature (S-FCCOST)"),
 ("Energy cost per km, year 1 (Rs/km)", f"={S['fkm_B']}", "about half of H2-ICE per km on hydrogen", f"={S['fkm_bev']}", f"={S['fkm_A']}", "TCO sheet"),
 ("Range per fill or charge (km)", f"={ER['range']}", "about 2x H2-ICE for same tank", "187 to 260 (Tiago EV, Punch EV tests)", "about 250 on CNG at 25 km/kg", "Energy_Range; Autocar India real-world tests (W3-S30)"),
 ("Refuel or recharge time", "3 to 5 min (350 bar, non-cooled fill)", "3 to 5 min", "about 58 min 10-80 percent DC (Tiago EV 24 kWh); 6-8 h AC", "3 to 5 min", "SAE J2601; Tata specifications (W3-S27)"),
 ("Peak power versus petrol", f"={I('h2_power_factor')}", "restored (electric drive)", "typically higher", "about 0.85", "Model / spec"),
 ("Tailpipe CO2 on hydrogen km", "zero (NOx present)", "zero (water only)", "zero", "about 105 g/km", "Emissions sheet"),
 ("Approval route today", "None for retrofit; new-vehicle standard AIS-195 exists", "None for retrofit; AIS-157 covers new FCEVs", "Established", "Established", "WS2 findings"),
 ("Supplier readiness", "Injectors, valves, regulators production-intent; small cylinders scarce", "Stacks imported; no Indian light-duty supply chain", "Mature", "Mature", "WS1/WS3"),
 ("Verdict", "Selected: only route that is a retrofit at an affordable scope; economics hinge on hydrogen price", "Not a retrofit in cost terms; equals a new vehicle", "Benchmark to beat; lowest running cost", "Baseline", ""),
]
for row in trows:
    for j, v in enumerate(row, start=1):
        c = wd.cell(row=r, column=j, value=v); c.alignment = WRAP
        if isinstance(v, str) and v.startswith("="): c.number_format = "0.00"
    r += 1

# ------------------------------------------------------------------ Sources
wsrc = wb.create_sheet("Sources")
title(wsrc, "Source register", "Access date 14 September 2026 unless noted. Status: observed / modelled / target / announced / spec / regulation. 'excerpt' or 'summary' in Limitations means the original could not be opened in the build environment.")
hdr(wsrc, 4, ["ID", "Claim / input supported", "Publisher", "Document title", "URL", "Publication / data date", "Page / table / section", "Geography", "Unit", "Status", "Limitations"],
    [12, 44, 24, 44, 50, 16, 20, 12, 12, 14, 40])
if os.path.exists(SRC_JSON):
    srcs = json.load(open(SRC_JSON))
    for i, s_ in enumerate(srcs, start=5):
        for j, k in enumerate(["id", "claim", "publisher", "title", "url", "date", "section", "geo", "unit", "status", "limits"], start=1):
            wsrc.cell(row=i, column=j, value=s_.get(k, "")).alignment = WRAP
else:
    wsrc["A5"] = "sources.json not found at build time"

# key outputs map for downstream use
for ws_ in wb.worksheets:
    ws_.page_setup.orientation = "landscape"
    ws_.page_setup.paperSize = ws_.PAPERSIZE_A4
    ws_.page_setup.fitToWidth = 1
    ws_.page_setup.fitToHeight = 0
    ws_.sheet_properties.pageSetUpPr.fitToPage = True
    ws_.page_margins.left = ws_.page_margins.right = 0.4
    ws_.page_margins.top = ws_.page_margins.bottom = 0.5
    ws_.print_options.gridLines = False
KEYS = {"S": S, "ER": ER, "H2S": H2S, "MK": MK, "PB": PB, "EM": EM, "ROW": ROW, "SN": SN, "RA": RA, "RB": RB, "RC": RC}
json.dump(KEYS, open(os.path.join(os.path.dirname(OUT), "model_keys.json"), "w"), indent=1)
wb.save(OUT)
print("saved", OUT)
