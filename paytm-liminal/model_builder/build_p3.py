"""Part 3: Capital_Drag, Churn, Earnout, Structures, Scenarios, Thresholds, Synergies."""
from common import *
from engine import *
from build_p2 import WID

def build_capital_drag(b):
    ws = b.sheet("Capital_Drag", tab_color="7030A0", widths=WID)
    r = header(ws, 1, "CAPITAL DRAG — what the ₹750 Cr/yr means, three readings, the ₹500–1,250 Cr grid, the break-even drag, and the MDR offset", ncols=14)
    r = note(ws, r, "Case §3.2: owning Liminal's custody infrastructure forces RBI to require bank-like capital reserves against custodied assets → a recurring annual FCF drag of ₹750 Cr. The case frames it as CASH (FCF), RECURRING, and OWNER-SPECIFIC (Paytm holds a PA licence, not a banking licence).")
    r += 1
    r = subheader(ws, r, "1. THREE READINGS OF THE SAME SENTENCE (select on Dashboard: lv_drag_mode)", ncols=14)
    readings = [
        ("Reading 1 — literal (case wording): a fixed ₹750 Cr leaves free cash flow every year",
         "Cash that must be set aside as reserve capital each year; not an expense, so PAT is untouched except for the yield foregone on the growing pile of trapped capital. Never recovered unless a_recovery > 0. This is the base reading."),
        ("Reading 2 — proportional: the reserve scales with custodied assets, proxied by Liminal's revenue",
         "If reserves are 'against custodied assets', they fall when clients leave (churn) and RISE as Liminal grows. Growth makes the trap deeper: at 20% growth the year-5 drag is ~2.5× the year-1 drag. Under this reading growth cannot rescue the deal."),
        ("Reading 3 — operating cost: ₹750 Cr/yr is a P&L expense (e.g., insurance, collateral fees, capital charge)",
         "Worst case for reported earnings: after tax it removes ~₹560 Cr of PAT, i.e. more than Paytm's entire ₹480 Cr PAT — EPS turns negative. Shown for completeness; the case says 'FCF drag', so this is not the base reading."),
    ]
    for t_, d in readings:
        text(ws, r, 1, t_, bold=True); r += 1
        text(ws, r, 1, d, wrap=True); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=14); ws.row_dimensions[r].height = 30; r += 1
    r += 1
    r = subheader(ws, r, "2. THE DRAG IN CONTEXT (calculations on case facts)", ncols=14)
    ctx = [
        ("Drag ÷ Paytm EBITDA", "=c_drag_v_ebitda", F_PCT),
        ("Drag ÷ Paytm PAT", "=c_drag_v_pat", F_PCT),
        ("Drag ÷ Liminal ARR", "=c_drag_v_arr", F_X),
        ("PV of a fixed ₹750 Cr/yr for 10 years at the Dashboard WACC (₹ Cr)", "=cf_drag*(1-(1+lv_wacc)^-a_horizon)/lv_wacc", F_INR),
        ("PV of the same drag in perpetuity (₹ Cr)", "=cf_drag/lv_wacc", F_INR),
        ("Liminal ARR needed to fund the drag from its own FCF at the mature margin (₹ Cr) = drag ÷ (margin cap × (1 − tax))", "=cf_drag/(a_mcap*(1-a_tax))", F_INR),
        ("…as a multiple of today's ARR", f"=B{r+5}/cf_arr", F_X),
        ("Years to reach that ARR at the base growth rate (zero churn)", f"=LN(B{r+5}/cf_arr)/LN(1+a_g_base)", F_INR1),
        ("Years to reach that ARR at the bull growth rate", f"=LN(B{r+5}/cf_arr)/LN(1+a_g_bull)", F_INR1),
        ("Years of drag fundable from cash after the headline deal, above the cash floor", "=(cf_cash-cf_deal_cash-a_min_cash)/cf_drag", F_INR1),
    ]
    for lab, f, fmt in ctx:
        label(ws, r, lab); calc(ws, r, 2, f, fmt); r += 1
    r += 1
    r = subheader(ws, r, "3. MDR OFFSET — is the ₹115 Cr incremental, and how much of the drag does it cover?", ncols=14)
    mdr = [
        ("MDR net revenue (case) (₹ Cr/yr)", "=cf_mdr", F_INR),
        ("MDR ÷ drag at the revenue line (gross offset)", "=cf_mdr/cf_drag", F_PCT),
        ("MDR reaching PAT / FCF after flow-through and tax (₹ Cr/yr)", "=cf_mdr*a_mdr_flow*(1-a_tax)", F_INR1),
        ("MDR ÷ drag on a cash basis (net offset)", f"=B{r+2}/cf_drag", F_PCT),
        ("Net annual cash cost of full ownership after the MDR (₹ Cr/yr) — case-style view", f"=cf_drag-B{r+2}", F_INR),
        ("MDR per Paytm share, standalone (₹) — accrues WITHOUT the deal", f"=B{r+2}/cf_shares", F_EPS),
        ("Standalone Paytm EPS incl. MDR (₹) — the correct like-for-like baseline", f"=cf_eps+B{r+5}", F_EPS),
    ]
    for lab, f, fmt in mdr:
        label(ws, r, lab); calc(ws, r, 2, f, fmt); r += 1
    r = note(ws, r, "Verdict: the MDR is REAL (case §3.4) but NOT INCREMENTAL to the acquisition — Paytm earns it whether or not it buys Liminal. It is Paytm's own tailwind and belongs in the standalone baseline. Netting it against the drag flatters the deal by ~₹69 Cr/yr; the deal must stand on its own. It does, however, add ~₹69 Cr/yr of FCF capacity to absorb a drag, which matters for liquidity, not for value.", italic=False)
    r += 1
    r = subheader(ws, r, "4. DRAG GRID — ₹0 / 500 / 750 / 1,000 / 1,250 Cr/yr and the Dashboard value, all other levers as on Dashboard", ncols=14)
    r = note(ws, r, "Each row is a full deal engine (below) with only the drag changed. Reading (1/2/3) follows the Dashboard lever.")
    heads = ["Drag (₹ Cr/yr)", "Year-1 FCF after cost of funds (₹ Cr)", "Cumulative cash after 10 yrs (₹ Cr)", "PV of drag (₹ Cr)", "NPV to Paytm (₹ Cr)", "FCF breakeven year", "FCF breakeven with MDR credited", "Payback year", "Effective multiple incl. PV of drag", "Year-1 EPS (₹)", "Cash at end of year 3 (₹ Cr)"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 42; r += 1
    levels = [("=0", "0"), ("=500", "500"), ("=lv_drag", "Dashboard"), ("=750", "750"), ("=1000", "1000"), ("=1250", "1250")]
    grid_rows = []
    for f, lab in levels:
        grid_rows.append(r); r += 1
    r += 1
    label(ws, r, "Break-even capital drag (₹ Cr/yr): the fixed drag at which NPV = 0 at the Dashboard levers", bold=True); out(ws, r, 2, "=e_max_drag", F_INR); b.name("cd_max_drag", ws, f"B{r}"); r += 1
    label(ws, r, "Maximum drag that still allows FCF breakeven by the gate year (₹ Cr/yr) = Liminal FCF in gate year − cost of funds", bold=True)
    calc(ws, r, 2, f"=INDEX(Liminal_Ops!{yl(1)}{b.lim_fa['fcf']}:{yl(NY)}{b.lim_fa['fcf']},a_be_gate)-Deal_CF!{yl(0)}{b.E['cof']}", F_INR, bold=True, fill=FILL_OUT, border=True); b.name("cd_max_drag_gate", ws, f"B{r}"); r += 1
    r = note(ws, r, "If the break-even drag is negative, the deal has no capacity to absorb ANY recurring capital cost at that price: the price alone already exceeds the value of the retained cash flows.")
    r += 1
    # engines for grid: one full engine per drag level; grid row col B = drag level, metrics from col C
    engines = []
    for (f, lab), gr in zip(levels, grid_rows):
        text(ws, gr, 1, f"Drag {lab}", bold=True)
        if f == "=lv_drag": link(ws, gr, 2, "=lv_drag", F_INR)
        else: inp(ws, gr, 2, float(f[1:]), F_INR, kind="assump")
        p = lever_params(); p['drag'] = f"'{ws.title}'!$B${gr}"
        r, E = engine(ws, r, p, f"ENGINE — drag {lab}")
        engines.append(E)
    for (f, lab), gr, E in zip(levels, grid_rows, engines):
        vals = [f"={yl(1)}{E['fcf_post']}", f"={yl(0)}{E['cum10']}", f"={yl(0)}{E['pv_drag']}", f"={yl(0)}{E['npv']}", f"={yl(0)}{E['fcf_be']}", f"={yl(0)}{E['fcf_be_mdr']}", f"={yl(0)}{E['payback']}", f"={yl(0)}{E['eff_mult_drag']}", f"={yl(0)}{E['eps_y1']}", f"={yl(0)}{E['cash_y3']}"]
        fmts = [F_INR, F_INR, F_INR, F_INR, F_YR, F_YR, F_YR, F_X, F_EPS, F_INR]
        for j, (v, fm) in enumerate(zip(vals, fmts)):
            calc(ws, gr, 3 + j, v, fm, bold=(j == 3), fill=FILL_OUT if j == 3 else None)
    b.cd_grid = (grid_rows, engines)
    return ws

def build_churn(b):
    ws = b.sheet("Churn", tab_color="7030A0", widths=WID)
    r = header(ws, 1, "CHURN — 0% to 60% ARR loss after a full acquisition: retained ARR, effective multiple, earnings, cash, breakevens, and the maximum acceptable churn", ncols=14)
    r = note(ws, r, "Case §3.1: 30–45% of ARR lost within 12 months of a full acquisition; top-4 clients (HDFC Bank, Axis Bank, CoinDCX, ZebPay) = 60% of ARR. Each grid row below is a full deal engine at the Dashboard levers with only churn changed.")
    r += 1
    r = subheader(ws, r, "1. WHO LEAVES — the case's churn range expressed against the top-4 book (calculations)", ncols=14)
    label(ws, r, "Top-4 ARR (₹ Cr)"); calc(ws, r, 2, "=c_top4_arr", F_INR); r += 1
    label(ws, r, "ARR at risk, case low / high (₹ Cr)"); calc(ws, r, 2, "=c_churn_lo_arr", F_INR1); calc(ws, r, 3, "=c_churn_hi_arr", F_INR1); r += 1
    label(ws, r, "…as % of the top-4 book: low / high"); calc(ws, r, 2, "=c_churn_of_top4_lo", F_PCT); calc(ws, r, 3, "=c_churn_of_top4_hi", F_PCT); r += 1
    label(ws, r, "Value destroyed per 10 points of churn at the headline multiple (₹ Cr)"); calc(ws, r, 2, "=c_mult*cf_arr*0.1", F_INR); r += 1
    r = note(ws, r, "The case range therefore implies that between half and three-quarters of the top-4 book leaves; the two banks alone could be most of it. The 'long tail' (40% of ARR: exchanges, hedge funds, OTC desks) is assumed to stay.")
    r += 1
    r = subheader(ws, r, "2. CHURN GRID (full acquisition, Dashboard mix / growth / drag / WACC)", ncols=14)
    heads = ["Churn", "Retained ARR (₹ Cr)", "ARR lost (₹ Cr)", "Effective multiple (price ÷ retained ARR)", "Value at headline multiple (₹ Cr)", "Gap vs price (₹ Cr)", "Year-1 Liminal PAT (₹ Cr)", "Year-1 EPS ex-MDR (₹)", "vs ₹7.50", "Year-1 FCF after cost of funds (₹ Cr)", "NPV to Paytm (₹ Cr)", "PAT breakeven yr", "FCF breakeven yr", "Payback yr"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 54; r += 1
    churns = [0.0, 0.10, 0.20, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60]
    grid_rows = []
    for c_ in churns:
        inp(ws, r, 1, c_, F_PCT, kind="assump"); grid_rows.append(r); r += 1
    g_first, g_last = grid_rows[0], grid_rows[-1]
    r += 1
    r = subheader(ws, r, "3. MAXIMUM ECONOMICALLY ACCEPTABLE CHURN", ncols=14)
    label(ws, r, "Churn at which NPV = 0 at the Dashboard price and drag (linear interpolation on the grid; 'none' if NPV < 0 even at 0% churn)", bold=True)
    npv_rng = f"K{g_first}:K{g_last}"; ch_rng = f"A{g_first}:A{g_last}"
    k = f"COUNTIF({npv_rng},\">=0\")"
    f = (f"=IF({k}=0,\"none: NPV<0 even at 0% churn\",IF({k}={len(churns)},\"all grid points positive\","
         f"INDEX({ch_rng},{k})+(INDEX({ch_rng},{k}+1)-INDEX({ch_rng},{k}))*INDEX({npv_rng},{k})/(INDEX({npv_rng},{k})-INDEX({npv_rng},{k}+1))))")
    out(ws, r, 2, f, F_PCT); b.name("ch_max_churn", ws, f"B{r}"); r += 1
    label(ws, r, "Same test with the capital drag set to zero (isolates churn from the drag)", bold=True)
    npv0_rng = f"O{g_first}:O{g_last}"
    k0 = f"COUNTIF({npv0_rng},\">=0\")"
    f0 = (f"=IF({k0}=0,\"none: NPV<0 even at 0% churn\",IF({k0}={len(churns)},\"all grid points positive\","
          f"INDEX({ch_rng},{k0})+(INDEX({ch_rng},{k0}+1)-INDEX({ch_rng},{k0}))*INDEX({npv0_rng},{k0})/(INDEX({npv0_rng},{k0})-INDEX({npv0_rng},{k0}+1))))")
    out(ws, r, 2, f0, F_PCT); b.name("ch_max_churn_nodrag", ws, f"B{r}"); r += 1
    label(ws, r, "Churn at which year-1 EPS dilution vs ₹7.50 exceeds 30% (interpolated; shareholder-pressure threshold, case §3.3)")
    dil_rng = f"I{g_first}:I{g_last}"
    kd = f"COUNTIF({dil_rng},\">=-0.3\")"
    fd = (f"=IF({kd}=0,\"exceeds 30% at all churn levels\",IF({kd}={len(churns)},\"never exceeds 30%\","
          f"INDEX({ch_rng},{kd})+(INDEX({ch_rng},{kd}+1)-INDEX({ch_rng},{kd}))*(INDEX({dil_rng},{kd})+0.3)/(INDEX({dil_rng},{kd})-INDEX({dil_rng},{kd}+1))))")
    calc(ws, r, 2, fd, F_PCT, bold=True); r += 1
    label(ws, r, "Price at which each churn level would be value-neutral (₹ Cr) = price + NPV (drag as on Dashboard) — see column P of the grid"); r += 1
    r = note(ws, r, "How to read: at the headline price the maximum acceptable churn is the point where the retained business, after the drag, is worth exactly what is paid. Column P shows the price that WOULD be acceptable at each churn level — the basis for retention-linked consideration (Earnout).")
    r += 1
    r = subheader(ws, r, "4. PRICE × CHURN — NPV to Paytm (₹ Cr) for alternative prices, WITHOUT the capital drag (the negotiation exhibit)", ncols=14)
    r = note(ws, r, "NPV at price P = NPV at the Dashboard price + (Dashboard price − P) × (1 + fees% × DF1): the price enters the NPV linearly (fees scale with price). Green = value-creating.")
    prices = [1000, 1500, 2000, 2500, 3000, 4000]
    label(ws, r, "Churn ↓ / price for 100% (₹ Cr) →", bold=True)
    for i, pp in enumerate(prices): inp(ws, r, 2 + i, pp, F_INR, kind="assump")
    hp = r; r += 1
    for gr in grid_rows:
        calc(ws, r, 1, f"=A{gr}", F_PCT)
        for i in range(len(prices)):
            calc(ws, r, 2 + i, f"=O{gr}+(lv_price-{col(2+i)}${hp})*(1+a_fees_pct/(1+lv_wacc))", F_INR)
        r += 1
    r += 1
    r = subheader(ws, r, "5. PRICE × CHURN — NPV to Paytm (₹ Cr) WITH the Dashboard capital drag", ncols=14)
    label(ws, r, "Churn ↓ / price for 100% (₹ Cr) →", bold=True)
    for i, pp in enumerate(prices): inp(ws, r, 2 + i, pp, F_INR, kind="assump")
    hp2 = r; r += 1
    for gr in grid_rows:
        calc(ws, r, 1, f"=A{gr}", F_PCT)
        for i in range(len(prices)):
            calc(ws, r, 2 + i, f"=K{gr}+(lv_price-{col(2+i)}${hp2})*(1+a_fees_pct/(1+lv_wacc))", F_INR)
        r += 1
    r = note(ws, r, "Reading: with the case's ₹750 Cr drag no price above zero is value-creating at the base growth rate; the drag, not the churn, sets the walk-away line. Without the drag, the value-creating price band is a function of churn and growth (see DCF §4).")
    r += 1
    # engines
    engines = []
    for c_, gr in zip(churns, grid_rows):
        p = lever_params(); p['churn'] = f"'{ws.title}'!$A${gr}"
        r, E = engine(ws, r, p, f"ENGINE — churn {c_*100:.0f}%")
        p0 = lever_params(); p0['churn'] = f"'{ws.title}'!$A${gr}"; p0['drag'] = "0"
        r, E0 = engine(ws, r, p0, f"ENGINE — churn {c_*100:.0f}%, drag = 0 (isolation)")
        engines.append((E, E0))
    for c_, gr, (E, E0) in zip(churns, grid_rows, engines):
        vals = [(f"=cf_arr*(1-A{gr})", F_INR1), (f"=cf_arr*A{gr}", F_INR1), (f"=lv_price/(cf_arr*(1-A{gr}))", F_X), (f"=c_mult*cf_arr*(1-A{gr})", F_INR), (f"=lv_price-c_mult*cf_arr*(1-A{gr})", F_INR),
                (f"={yl(1)}{E['pat']}", F_INR1), (f"={yl(0)}{E['eps_y1']}", F_EPS), (f"={yl(0)}{E['eps_y1']}/cf_eps-1", F_PCT), (f"={yl(0)}{E['fcf_y1']}", F_INR), (f"={yl(0)}{E['npv']}", F_INR),
                (f"={yl(0)}{E['pat_be']}", F_YR), (f"={yl(0)}{E['fcf_be']}", F_YR), (f"={yl(0)}{E['payback']}", F_YR), (f"={yl(0)}{E0['npv']}", F_INR), (f"=lv_price+{yl(0)}{E['npv']}", F_INR)]
        for j, (v, fm) in enumerate(vals):
            calc(ws, gr, 2 + j, v, fm, bold=(j in (2, 9)), fill=FILL_OUT if j == 9 else None)
    # extra headers for cols O, P
    c = ws.cell(row=grid_rows[0] - 1, column=15, value="NPV with drag = 0 (₹ Cr)"); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    c = ws.cell(row=grid_rows[0] - 1, column=16, value="Value-neutral price at this churn (₹ Cr)"); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.column_dimensions['O'].width = 12; ws.column_dimensions['P'].width = 12
    b.ch_grid = (grid_rows, engines)
    return ws

def build_earnout(b):
    ws = b.sheet("Earnout", tab_color="BF8F00", widths={"A": 58, "B": 14, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 14})
    r = header(ws, 1, "NEGOTIATION ARCHITECTURE — retention-linked consideration, call-option strike, escrow: pay upfront for what is known, make sellers bear what is uncertain", ncols=8)
    r += 1
    r = subheader(ws, r, "1. RETENTION EARN-OUT FOR THE CONTROL TRANCHE (hybrid structure) — team assumptions from Inputs §F", ncols=8)
    label(ws, r, "Remaining stake acquired at exercise"); calc(ws, r, 2, "=1-lv_stake", F_PCT); r_rem = r; r += 1
    label(ws, r, "Headline-equivalent value of the remaining stake (₹ Cr) = remaining stake × headline price — the CAP"); calc(ws, r, 2, f"=B{r_rem}*lv_price", F_INR); r_ctrl = r; r += 1
    label(ws, r, "ARR at the end of the option year at the Dashboard growth (₹ Cr)"); calc(ws, r, 2, "=cf_arr*(1+lv_g)^a_opt_year", F_INR1); r_arr = r; r += 1
    label(ws, r, "Strike multiple (× ARR at exercise) — Inputs a_ctrl_mult"); link(ws, r, 2, "=a_ctrl_mult", F_X); r_m = r; r += 1
    label(ws, r, "Control consideration at 100% retention (₹ Cr) = MIN(cap, remaining stake × multiple × ARR at exercise)", bold=True); out(ws, r, 2, f"=MIN(B{r_ctrl},B{r_rem}*B{r_m}*B{r_arr})", F_INR); r_tot = r; b.name("eo_total", ws, f"B{r}"); r += 1
    label(ws, r, "Upfront at exercise (₹ Cr) = control consideration × retention floor (pays for the worst-case retained ARR)", bold=True); out(ws, r, 2, f"=B{r_tot}*a_eo_floor", F_INR); r_up = r; b.name("eo_upfront", ws, f"B{r}"); r += 1
    label(ws, r, "Maximum earn-out (₹ Cr) = control consideration − upfront; linear from the floor to full retention", bold=True); out(ws, r, 2, f"=B{r_tot}-B{r_up}", F_INR); r_eomax = r
    b.name("eo_max", ws, f"B{r}"); r += 1
    label(ws, r, "Upfront funded from cash (₹ Cr) = upfront − new debt (Inputs a_ctrl_debt)"); calc(ws, r, 2, f"=B{r_up}-a_ctrl_debt", F_INR); b.name("eo_cash", ws, f"B{r}"); r += 1
    label(ws, r, "Implied multiple of the control consideration on CURRENT ARR (remaining stake basis)"); calc(ws, r, 2, f"=B{r_tot}/(B{r_rem}*cf_arr)", F_X); r += 1
    label(ws, r, "Earn-out per 10 points of retained ARR (₹ Cr)"); calc(ws, r, 2, f"=B{r_eomax}/((a_eo_full-a_eo_floor)*10)", F_INR); r += 1
    label(ws, r, "Value of 10 points of ARR at the headline multiple (₹ Cr) — what those clients are 'worth' at the ask"); calc(ws, r, 2, "=c_mult*cf_arr*0.1", F_INR); r += 1
    label(ws, r, "Maximum shares to settle the earn-out (Cr) / % of count"); calc(ws, r, 2, f"=B{r_eomax}/c_price", F_INR2); calc(ws, r, 3, f"=B{r}/cf_shares", F_PCT); r += 1
    r += 1
    heads = ["Post-control churn", "Retained ARR", "Retention factor for payout (0–1)", "Earn-out paid (₹ Cr)", "Control total = upfront + earn-out (₹ Cr)", "Grand total incl. minority (₹ Cr)", "Remaining stake × strike multiple × retained ARR at exercise (₹ Cr)", "Structure over/(under)-pays vs retained value"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 54; r += 1
    for c_ in (0.0, 0.10, 0.20, 0.30, 0.375, 0.45, 0.55):
        inp(ws, r, 1, c_, F_PCT, kind="assump")
        calc(ws, r, 2, f"=1-A{r}", F_PCT)
        calc(ws, r, 3, f"=MIN(1,MAX(0,(B{r}-a_eo_floor)/(a_eo_full-a_eo_floor)))", '0.00')
        calc(ws, r, 4, f"=B${r_eomax}*C{r}", F_INR)
        calc(ws, r, 5, f"=B${r_up}+D{r}", F_INR, bold=True)
        calc(ws, r, 6, f"=lv_min_price+E{r}", F_INR)
        calc(ws, r, 7, f"=B${r_rem}*B${r_m}*B${r_arr}*B{r}", F_INR)
        calc(ws, r, 8, f"=E{r}/G{r}-1", F_PCT)
        r += 1
    r = note(ws, r, "The schedule reproduces 'strike multiple × retained ARR' for the remaining stake across the case's churn range: the upfront covers the worst case; the earn-out pays only for revenue that survives control. Grand total never exceeds the ₹4,000 Cr headline.")
    r += 1
    r = subheader(ws, r, "2. CALL-OPTION TERMS — why the strike is a formula, not a number (team assumption; the case gives no option terms)", ncols=8)
    label(ws, r, "Strike = remaining stake × strike multiple × audited ARR at exercise, capped at the headline-equivalent (₹ Cr) and paid 55% upfront + 45% retention earn-out. A growth-linked strike gives sellers the upside they would otherwise demand as an option premium; the cap protects Paytm; the earn-out makes sellers bear the churn."); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 42; r += 1
    label(ws, r, "Strike sensitivity: control consideration at 100% retention for strike multiples 8x / 10x / 12x / 14x (₹ Cr)")
    for i, m in enumerate((8, 10, 12, 14)):
        calc(ws, r, 2 + i, f"=MIN(B{r_ctrl},B{r_rem}*{m}*B{r_arr})", F_INR)
    r += 1
    label(ws, r, "Indicative option premium if sellers still demand one (% of control consideration, team assumption) → ₹ Cr"); inp(ws, r, 2, 0.03, F_PCT, kind="assump"); calc(ws, r, 3, f"=B{r}*B{r_tot}", F_INR); r += 1
    label(ws, r, "Why sellers can accept: liquidity now (primary + secondary), Paytm as anchor client, a defined path to control at a growth-linked price, founder/key-engineer retention pool, and the same wallet-conflict facing any other payments-company buyer. Why they may not: the cap; expect to trade cap for option premium or a higher multiple."); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 42; r += 1
    r += 1
    r = subheader(ws, r, "3. FULL-ACQUISITION ALTERNATIVE: RE-CUT THE ₹4,000 Cr INTO UPFRONT + CONTINGENT (if the Board insists on 100% today)", ncols=8)
    label(ws, r, "Upfront for 100% (₹ Cr) = headline × 55% retained × (1 − further discount for the capital-treatment risk)"); inp(ws, r, 2, 2200, F_INR, kind="assump", comment="Team assumption: 4,000 × 55% = 2,200, i.e. the case's worst-case retained ARR at the headline multiple."); r_up100 = r; r += 1
    label(ws, r, "Contingent (₹ Cr): retention earn-out to the headline cap"); calc(ws, r, 2, f"=lv_price-B{r_up100}", F_INR); r += 1
    label(ws, r, "Escrow held back from the upfront for indemnities / capital-treatment CP (₹ Cr, team assumption 10%)"); inp(ws, r, 2, 0.10, F_PCT, kind="assump"); calc(ws, r, 3, f"=B{r}*B{r_up100}", F_INR); r += 1
    label(ws, r, "Condition precedent: written RBI capital treatment. If a reserve applies, price adjusts by PV of the drag (₹ Cr) →"); link(ws, r, 2, "=e_pv_drag", F_INR); r += 1
    r = note(ws, r, "Even re-cut, a 100% acquisition today still triggers the churn (the sellers bear the price, Paytm bears the franchise damage) and the capital drag (which no earn-out cures). The re-cut fixes the PRICE risk, not the OWNERSHIP risk.")
    return ws
