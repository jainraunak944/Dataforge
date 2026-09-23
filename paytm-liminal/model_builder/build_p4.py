"""Part 4: Structures, Scenarios, Thresholds, Synergies."""
from common import *
from engine import *
from build_p2 import WID

def minority_block(ws, r, b, title, churn_expr="lv_min_churn", price_expr="lv_min_price", drag_mode_expr="lv_min_drag_mode"):
    """Minority-stake economics block (equity-accounted associate). Returns (r, rows)."""
    r, L = lim_block(ws, r, dict(g="lv_g", churn=churn_expr, churn_year="a_churn_year"), title + " — Liminal operating block (minority churn applied)")
    rows = dict(L); yr = L['yr']
    r = subheader(ws, r, title + " — Paytm economics (equity method)", ncols=14)
    def row(key, lab, f0, ft, fmt=F_INR1, bold=False):
        nonlocal r
        rows[key] = r; label(ws, r, lab, bold=bold)
        if f0 is not None: calc(ws, r, yc(0), f0, fmt, bold=bold)
        for t in range(1, NY + 1): calc(ws, r, yc(t), ft(t), fmt, bold=bold)
        r += 1
    rows['price'] = r; label(ws, r, "Price paid for the stake (₹ Cr)"); calc(ws, r, yc(0), f"={price_expr}", F_INR); r += 1
    rows['cof'] = r; label(ws, r, "Foregone after-tax yield on the cash used (₹ Cr/yr)"); calc(ws, r, yc(0), f"=({price_expr}+a_integ_min)*a_yield*(1-a_tax)", F_INR1); r += 1
    row('assoc', "Paytm's share of Liminal PAT (equity method) (₹ Cr)", "=0", lambda t: f"=lv_stake*{yl(t)}{L['pat']}")
    row('drag', "Capital drag borne by Paytm at minority (₹ Cr/yr): 0 none / pro-rata / full", "=0", lambda t: f"=CHOOSE({drag_mode_expr}+1,0,lv_stake*lv_drag,lv_drag)")
    row('inc_pat', "Incremental PAT = associate share − foregone yield", f"=-{yl(0)}{rows['cof']}", lambda t: f"={yl(t)}{rows['assoc']}-{yl(0)}{rows['cof']}", bold=True)
    row('eps', "Pro-forma EPS ex-MDR (₹) — no new shares", f"=(cf_pat+{yl(0)}{rows['inc_pat']})/cf_shares", lambda t: f"=(cf_pat*(1+a_pat_growth)^{yl(t)}{yr}+{yl(t)}{rows['inc_pat']})/cf_shares", F_EPS, bold=True)
    row('acc', "Accretion / (dilution) vs ₹7.50", f"={yl(0)}{rows['eps']}/cf_eps-1", lambda t: f"={yl(t)}{rows['eps']}/cf_eps-1", F_PCT)
    row('fcf', "Incremental FCF to Paytm (cash view): −foregone yield − drag (no cash yield until dividends/exit)", f"=-{price_expr}-a_integ_min", lambda t: f"=-{yl(0)}{rows['cof']}-{yl(t)}{rows['drag']}")
    row('econ', "Economic share of Liminal FCF accruing to the stake (₹ Cr) = stake × Liminal FCF", "=0", lambda t: f"=lv_stake*{yl(t)}{L['fcf']}")
    row('df', "Discount factor", "=1", lambda t: f"=1/(1+lv_wacc)^{yl(t)}{yr}", '0.000')
    def scalar(key, lab, f, fmt=F_INR, bold=False, fill=None):
        nonlocal r
        rows[key] = r; label(ws, r, lab, bold=bold); calc(ws, r, yc(0), f, fmt, bold=bold, fill=fill, border=bool(fill)); r += 1
    rng = lambda key: f"{yl(1)}{rows[key]}:{yl(NY)}{rows[key]}"
    scalar('ev100', "DCF value of 100% of Liminal on this block (₹ Cr)", f"=SUMPRODUCT({yl(1)}{L['fcf']}:{yl(NY)}{L['fcf']},{rng('df')})+{yl(NY)}{L['fcf']}*(1+a_tg)/(lv_wacc-a_tg)*{yl(NY)}{rows['df']}")
    scalar('stake_val', "Value of the stake (pro-rata) (₹ Cr)", f"=lv_stake*{yl(0)}{rows['ev100']}")
    scalar('pv_drag', "PV of drag borne at minority (₹ Cr)", f"=SUMPRODUCT({rng('drag')},{rng('df')})")
    scalar('npv', "NPV to Paytm = stake value − price − one-time − PV drag (₹ Cr)", f"={yl(0)}{rows['stake_val']}-{price_expr}-a_integ_min-{yl(0)}{rows['pv_drag']}", F_INR, bold=True, fill=FILL_OUT)
    scalar('eps_y1', "Year-1 EPS (₹)", f"={yl(1)}{rows['eps']}", F_EPS, bold=True, fill=FILL_OUT)
    scalar('eps_y3', "Year-3 EPS (₹)", f"={yl(3)}{rows['eps']}", F_EPS)
    scalar('cover', "Year in which the associate share covers the foregone yield (99 = never in horizon)", f"=MIN(IF({yl(1)}{rows['assoc']}>={yl(0)}{rows['cof']},1,99),IF({yl(2)}{rows['assoc']}>={yl(0)}{rows['cof']},2,99),IF({yl(3)}{rows['assoc']}>={yl(0)}{rows['cof']},3,99),IF({yl(4)}{rows['assoc']}>={yl(0)}{rows['cof']},4,99),IF({yl(5)}{rows['assoc']}>={yl(0)}{rows['cof']},5,99),IF({yl(6)}{rows['assoc']}>={yl(0)}{rows['cof']},6,99),IF({yl(7)}{rows['assoc']}>={yl(0)}{rows['cof']},7,99),IF({yl(8)}{rows['assoc']}>={yl(0)}{rows['cof']},8,99),IF({yl(9)}{rows['assoc']}>={yl(0)}{rows['cof']},9,99),IF({yl(10)}{rows['assoc']}>={yl(0)}{rows['cof']},10,99))", F_YR)
    scalar('cash_after', "Paytm cash after the investment (₹ Cr)", f"=cf_cash-{price_expr}-a_integ_min", F_INR)
    scalar('pct_mcap', "Cheque as % of Paytm market cap", f"={price_expr}/cf_mcap", '0.00%')
    rows['end'] = r
    return r + 1, rows

def build_structures(b):
    ws = b.sheet("Structures", tab_color="BF8F00", widths=WID)
    r = header(ws, 1, "ALTERNATIVE STRUCTURES — full acquisition · minority stake · hybrid (minority + call option + retention earn-out) · JV · walk away", ncols=14)
    r = note(ws, r, "Side-by-side on the same levers. Numbers where the structure can be modelled; text where the case gives no basis for a number. No arbitrary scores.")
    r += 1
    r = subheader(ws, r, "1. SUMMARY (filled from the blocks below)", ncols=14)
    sum_row = r
    heads = ["Metric", "Full acquisition (Dashboard mix)", "Minority stake", "Hybrid: minority + option", "Joint venture", "Walk away"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 32; r += 1
    metrics = ["Upfront cash out (₹ Cr)", "New Paytm shares issued (Cr)", "New debt (₹ Cr)", "Cash after close (₹ Cr)", "Gross debt ÷ EBITDA after close", "Maximum total commitment (₹ Cr)", "Maximum unconditional commitment (₹ Cr)",
               "Churn exposure (ARR lost)", "Capital drag exposure (₹ Cr/yr)", "Year-1 EPS ex-MDR (₹)", "vs ₹7.50", "Year-3 EPS ex-MDR (₹)", "PAT breakeven year", "FCF breakeven year", "NPV to Paytm (₹ Cr)", "Cash at risk if the thesis fails (₹ Cr)",
               "Control", "Blocks the PhonePe–Mastercard consortium?", "Reversibility", "Time to capability", "Regulatory exposure", "Governance complexity"]
    mrows = {}
    for m in metrics:
        label(ws, r, m); mrows[m] = r; r += 1
    r += 2
    # ---------- blocks ----------
    r, M = minority_block(ws, r, b, "BLOCK A — MINORITY STAKE (Dashboard stake, price, churn, drag mode)")
    b.M = M
    r = subheader(ws, r, "BLOCK A2 — MINORITY STAKE AS AN INVESTMENT: IRR on exit at end of year 5 (stake × exit multiple × ARR5 ÷ price; no dividends)", ncols=14)
    label(ws, r, "Growth ↓ / exit multiple (× ARR at year 5) →", bold=True)
    mults = [4, 6, 10, 14, 18.2]
    for i, m in enumerate(mults): inp(ws, r, yc(1 + i), m, F_X, kind="assump")
    hm = r; r += 1
    for lab, g in (("Bear", "a_g_bear"), ("Base", "a_g_base"), ("Bull", "a_g_bull")):
        label(ws, r, f"{lab} growth — IRR"); calc(ws, r, 2, f"={g}", F_PCT0)
        for i in range(len(mults)):
            calc(ws, r, yc(1 + i), f"=(lv_stake*{col(yc(1+i))}${hm}*cf_arr*(1+$B{r})^5*(1-lv_min_churn)/(lv_min_price+a_integ_min))^(1/5)-1", F_PCT)
        r += 1
    r = note(ws, r, "Against a hurdle equal to the Dashboard WACC, the stake earns its cost of capital only in the cells at or above that rate. The strategic value (blocking, access, option) is what the Board pays for in the other cells.")
    r += 1
    # hybrid: minority year(s), then control
    r = subheader(ws, r, "BLOCK B — HYBRID: minority now, call option exercised at end of the option year if gates pass; consolidated thereafter", ncols=14)
    r, H = lim_block(ws, r, dict(g="lv_g", churn="a_ctrl_churn", churn_year="a_opt_year+1"), "Hybrid — Liminal operating block (control churn applied in the year after exercise)")
    yr = H['yr']; H['fcf_lim'] = H['fcf']; H['pat_lim'] = H['pat']
    def row(key, lab, f0, ft, fmt=F_INR1, bold=False):
        nonlocal r
        H[key] = r; label(ws, r, lab, bold=bold)
        if f0 is not None: calc(ws, r, yc(0), f0, fmt, bold=bold)
        for t in range(1, NY + 1): calc(ws, r, yc(t), ft(t), fmt, bold=bold)
        r += 1
    r = subheader(ws, r, "Hybrid — Paytm economics", ncols=14)
    H['eo'] = r; label(ws, r, "Earn-out paid at retention = 1 − control churn (₹ Cr)"); calc(ws, r, yc(0), "=eo_max*MIN(1,MAX(0,((1-a_ctrl_churn)-a_eo_floor)/(a_eo_full-a_eo_floor)))", F_INR); r += 1
    H['ctrl_total'] = r; label(ws, r, "Control consideration = upfront + earn-out (₹ Cr)"); calc(ws, r, yc(0), f"=eo_upfront+{yl(0)}{H['eo']}", F_INR); r += 1
    H['total'] = r; label(ws, r, "Total consideration incl. minority (₹ Cr)", bold=True); calc(ws, r, yc(0), f"=lv_min_price+{yl(0)}{H['ctrl_total']}", F_INR, bold=True); r += 1
    H['sh_eo'] = r; label(ws, r, "Shares issued for the earn-out (Cr)"); calc(ws, r, yc(0), f"={yl(0)}{H['eo']}/c_price", F_INR2); r += 1
    H['cof_min'] = r; label(ws, r, "Cost of funds after tax — minority period (₹ Cr/yr)"); calc(ws, r, yc(0), "=(lv_min_price+a_integ_min)*a_yield*(1-a_tax)", F_INR1); r += 1
    H['cof_ctrl'] = r; label(ws, r, "Cost of funds after tax — after control (₹ Cr/yr)"); calc(ws, r, yc(0), f"={yl(0)}{H['cof_min']}+eo_cash*a_yield*(1-a_tax)+a_ctrl_debt*a_kd*(1-a_tax)", F_INR1); r += 1
    H['ppa'] = r; label(ws, r, "PPA amortisation after tax on the control tranche (₹ Cr/yr)"); calc(ws, r, yc(0), f"=a_ppa_on*{yl(0)}{H['ctrl_total']}*a_ppa_share/a_ppa_life*(1-a_tax)", F_INR1); r += 1
    row('ctrl', "Control flag (1 after exercise)", "=0", lambda t: f"=IF({yl(t)}{yr}>a_opt_year,1,0)", F_YR)
    row('shares', "Diluted shares (Cr)", "=cf_shares", lambda t: f"=cf_shares+{yl(t)}{H['ctrl']}*{yl(0)}{H['sh_eo']}", F_INR2)
    row('inc_pat', "Incremental PAT: minority (associate share − cof) then control (100% PAT − cof − PPA)", f"=-{yl(0)}{H['cof_min']}",
        lambda t: f"=IF({yl(t)}{H['ctrl']}=1,{yl(t)}{H['pat']}-{yl(0)}{H['cof_ctrl']}-{yl(0)}{H['ppa']},lv_stake*{yl(t)}{H['pat']}-{yl(0)}{H['cof_min']})", bold=True)
    row('eps', "Pro-forma EPS ex-MDR (₹)", f"=(cf_pat+{yl(0)}{H['inc_pat']})/cf_shares", lambda t: f"=(cf_pat*(1+a_pat_growth)^{yl(t)}{yr}+{yl(t)}{H['inc_pat']})/{yl(t)}{H['shares']}", F_EPS, bold=True)
    row('acc', "Accretion / (dilution) vs ₹7.50", f"={yl(0)}{H['eps']}/cf_eps-1", lambda t: f"={yl(t)}{H['eps']}/cf_eps-1", F_PCT)
    row('drag', "Capital drag after control (₹ Cr/yr) — gate value (Inputs a_ctrl_drag)", "=0", lambda t: f"={yl(t)}{H['ctrl']}*a_ctrl_drag")
    row('fcf', "Incremental FCF after cost of funds: minority (−cof) then control (100% FCF − cof − drag − one-time in exercise+1)", f"=-lv_min_price-a_integ_min",
        lambda t: f"=IF({yl(t)}{H['ctrl']}=1,{yl(t)}{H['fcf_lim']}-{yl(0)}{H['cof_ctrl']}-{yl(t)}{H['drag']}-IF({yl(t)}{yr}=a_opt_year+1,a_integ_full+{yl(0)}{H['ctrl_total']}*a_fees_pct,0),-{yl(0)}{H['cof_min']})", bold=True)
    row('consid', "Consideration paid (₹ Cr): control tranche in the exercise year", "=0", lambda t: f"=IF({yl(t)}{yr}=a_opt_year,{yl(0)}{H['ctrl_total']},0)")
    row('cum', "Cumulative cash incl. all consideration (₹ Cr)", f"=-lv_min_price-a_integ_min", lambda t: f"={yl(t-1)}{H['cum']}+{yl(t)}{H['fcf']}-{yl(t)}{H['consid']}")
    row('df', "Discount factor", "=1", lambda t: f"=1/(1+lv_wacc)^{yl(t)}{yr}", '0.000')
    row('f_pat', "helper: year if incremental PAT ≥ 0 after control else 99", "=99", lambda t: f"=IF(AND({yl(t)}{H['ctrl']}=1,{yl(t)}{H['inc_pat']}>=0),{yl(t)}{yr},99)", F_YR)
    row('f_fcf', "helper: year if FCF after cost of funds ≥ 0 after control else 99", "=99", lambda t: f"=IF(AND({yl(t)}{H['ctrl']}=1,{yl(t)}{H['fcf']}>=0),{yl(t)}{yr},99)", F_YR)
    row('econ', "Economic FCF attributable to Paytm: stake × Liminal FCF before control, 100% after", "=0", lambda t: f"=IF({yl(t)}{H['ctrl']}=1,1,lv_stake)*{yl(t)}{H['fcf_lim']}")
    def scalar(key, lab, f, fmt=F_INR, bold=False, fill=None):
        nonlocal r
        H[key] = r; label(ws, r, lab, bold=bold); calc(ws, r, yc(0), f, fmt, bold=bold, fill=fill, border=bool(fill)); r += 1
    rng = lambda key: f"{yl(1)}{H[key]}:{yl(NY)}{H[key]}"
    scalar('pat_be', "PAT breakeven year after control (99 = never in horizon)", f"=MIN({rng('f_pat')})", F_YR, bold=True, fill=FILL_OUT)
    scalar('fcf_be', "FCF breakeven year after control (99 = never in horizon)", f"=MIN({rng('f_fcf')})", F_YR, bold=True, fill=FILL_OUT)
    scalar('gate', "Passes the ≤ N-year breakeven gate after exercise? (1 = yes)", f"=IF(AND({yl(0)}{H['pat_be']}-a_opt_year<=a_be_gate,{yl(0)}{H['fcf_be']}-a_opt_year<=a_be_gate),1,0)", F_YR, bold=True)
    scalar('npv', "NPV to Paytm = PV(economic FCF) + PV(TV) − PV(consideration) − minority price − one-time − PV(drag) (₹ Cr)",
           f"=SUMPRODUCT({rng('econ')},{rng('df')})+{yl(NY)}{H['fcf_lim']}*(1+a_tg)/(lv_wacc-a_tg)*{yl(NY)}{H['df']}-SUMPRODUCT({rng('consid')},{rng('df')})-lv_min_price-a_integ_min-SUMPRODUCT({rng('drag')},{rng('df')})-(a_integ_full+{yl(0)}{H['ctrl_total']}*a_fees_pct)*INDEX({rng('df')},a_opt_year+1)", F_INR, bold=True, fill=FILL_OUT)
    scalar('eps_y1', "Year-1 EPS (₹)", f"={yl(1)}{H['eps']}", F_EPS, bold=True, fill=FILL_OUT)
    scalar('eps_y3', "Year-3 EPS (₹)", f"={yl(3)}{H['eps']}", F_EPS)
    scalar('eps_trough', "Trough EPS in years 1–10 (₹)", f"=MIN({rng('eps')})", F_EPS)
    scalar('cash_after_ctrl', "Paytm cash after the control tranche (₹ Cr)", f"=cf_cash-lv_min_price-a_integ_min-eo_cash-a_integ_full", F_INR)
    scalar('lev_after_ctrl', "Gross debt ÷ EBITDA after control", f"=(cf_debt+a_ctrl_debt)/cf_ebitda", F_X2)
    b.H = H
    r += 1
    # JV block
    r = subheader(ws, r, "BLOCK C — JOINT VENTURE ('SettleCo'): Paytm-majority settlement JV licensing Liminal's MPC; Liminal's custody book stays outside", ncols=14)
    year_row(ws, r); yrj = r; r += 1
    J = {}
    def jrow(key, lab, f0, ft, fmt=F_INR1, bold=False):
        nonlocal r
        J[key] = r; label(ws, r, lab, bold=bold)
        if f0 is not None: calc(ws, r, yc(0), f0, fmt, bold=bold)
        for t in range(1, NY + 1): calc(ws, r, yc(t), ft(t), fmt, bold=bold)
        r += 1
    jrow('rev', "JV revenue (₹ Cr): ramps to the year-3 level, then grows at the Liminal growth rate", "=0", lambda t: f"=IF({yl(t)}{yrj}<=3,a_jv_rev_y3*{yl(t)}{yrj}/3,{yl(t-1)}{J['rev']}*(1+lv_g))")
    jrow('margin', "EBITDA margin (ramps 5pp/yr to the JV cap)", "=0", lambda t: f"=MIN(a_mstep*{yl(t)}{yrj},a_jv_margin)", F_PCT)
    jrow('pat', "JV PAT (₹ Cr) = revenue × margin × (1 − tax) − D&A ignored (asset-light)", "=0", lambda t: f"={yl(t)}{J['rev']}*{yl(t)}{J['margin']}*(1-a_tax)")
    jrow('share', "Paytm share of JV PAT (₹ Cr)", "=0", lambda t: f"=a_jv_paytm_share*{yl(t)}{J['pat']}")
    J['cof'] = r; label(ws, r, "Foregone after-tax yield on the JV capital (₹ Cr/yr)"); calc(ws, r, yc(0), "=a_jv_capital*a_yield*(1-a_tax)", F_INR1); r += 1
    jrow('inc_pat', "Incremental PAT to Paytm (₹ Cr)", f"=-{yl(0)}{J['cof']}", lambda t: f"={yl(t)}{J['share']}-{yl(0)}{J['cof']}")
    jrow('eps', "Pro-forma EPS ex-MDR (₹)", f"=(cf_pat+{yl(0)}{J['inc_pat']})/cf_shares", lambda t: f"=(cf_pat*(1+a_pat_growth)^{yl(t)}{yrj}+{yl(t)}{J['inc_pat']})/cf_shares", F_EPS, bold=True)
    jrow('fcf', "Incremental FCF to Paytm: capital at Y0, then share of JV cash (≈ PAT less capex)", "=-a_jv_capital", lambda t: f"=a_jv_paytm_share*({yl(t)}{J['pat']}-{yl(t)}{J['rev']}*a_capex)-{yl(0)}{J['cof']}")
    jrow('df', "Discount factor", "=1", lambda t: f"=1/(1+lv_wacc)^{yl(t)}{yrj}", '0.000')
    J['npv'] = r; label(ws, r, "NPV to Paytm (₹ Cr) incl. terminal value of its JV share", bold=True)
    calc(ws, r, yc(0), f"=SUMPRODUCT({yl(1)}{J['fcf']}:{yl(NY)}{J['fcf']},{yl(1)}{J['df']}:{yl(NY)}{J['df']})-a_jv_capital+a_jv_paytm_share*({yl(NY)}{J['pat']}-{yl(NY)}{J['rev']}*a_capex)*(1+a_tg)/(lv_wacc-a_tg)*{yl(NY)}{J['df']}", F_INR, bold=True, fill=FILL_OUT, border=True); r += 1
    J['eps_y1'] = r; label(ws, r, "Year-1 EPS (₹)"); calc(ws, r, yc(0), f"={yl(1)}{J['eps']}", F_EPS); r += 1
    J['eps_y3'] = r; label(ws, r, "Year-3 EPS (₹)"); calc(ws, r, yc(0), f"={yl(3)}{J['eps']}", F_EPS); r += 1
    b.J = J
    r += 1
    # walk-away block
    r = subheader(ws, r, "BLOCK D — WALK AWAY: build or partner for an equivalent capability (team assumptions a_build_cost, a_build_years)", ncols=14)
    year_row(ws, r); yrw = r; r += 1
    W = {}
    W['build'] = r; label(ws, r, "Build/partner spend (₹ Cr), spread evenly over the build years"); calc(ws, r, yc(0), "=0", F_INR1)
    for t in range(1, NY + 1): calc(ws, r, yc(t), f"=IF({yl(t)}{yrw}<=a_build_years,-a_build_cost/a_build_years,0)", F_INR1)
    r += 1
    W['df'] = r; label(ws, r, "Discount factor"); calc(ws, r, yc(0), "=1", '0.000')
    for t in range(1, NY + 1): calc(ws, r, yc(t), f"=1/(1+lv_wacc)^{yl(t)}{yrw}", '0.000')
    r += 1
    W['npv'] = r; label(ws, r, "NPV of the build path (₹ Cr) — cost only; the capability's revenue is not credited (same treatment as synergies)", bold=True)
    calc(ws, r, yc(0), f"=SUMPRODUCT({yl(1)}{W['build']}:{yl(NY)}{W['build']},{yl(1)}{W['df']}:{yl(NY)}{W['df']})", F_INR, bold=True, fill=FILL_OUT, border=True); r += 1
    W['eps_y1'] = r; label(ws, r, "Year-1 EPS (₹) — build spend expensed"); calc(ws, r, yc(0), f"=(cf_pat+{yl(1)}{W['build']}*(1-a_tax))/cf_shares", F_EPS); r += 1
    b.W = W
    # ---------- fill summary ----------
    E = b.E; M = b.M
    S = {
        "Upfront cash out (₹ Cr)": (f"=lv_mix_cash+lv_price*a_fees_pct+a_integ_full", "=lv_min_price+a_integ_min", "=lv_min_price+a_integ_min", "=a_jv_capital", "=0"),
        "New Paytm shares issued (Cr)": (f"=Deal_CF!{yl(0)}{E['shares_new']}", "=0", f"={yl(0)}{H['sh_eo']}", "=0", "=0"),
        "New debt (₹ Cr)": ("=lv_mix_debt", "=0", "=a_ctrl_debt", "=0", "=0"),
        "Cash after close (₹ Cr)": ("=e_cash_after", f"={yl(0)}{M['cash_after']}", f"={yl(0)}{H['cash_after_ctrl']}", "=cf_cash-a_jv_capital", "=cf_cash"),
        "Gross debt ÷ EBITDA after close": ("=e_lev_after", "=c_lev0", f"={yl(0)}{H['lev_after_ctrl']}", "=c_lev0", "=c_lev0"),
        "Maximum total commitment (₹ Cr)": ("=lv_price+lv_price*a_fees_pct+a_integ_full", "=lv_min_price+a_integ_min", "=hy_max_total", "=a_jv_capital", "=a_build_cost"),
        "Maximum unconditional commitment (₹ Cr)": ("=lv_price+lv_price*a_fees_pct+a_integ_full", "=lv_min_price+a_integ_min", "=lv_min_price+a_integ_min", "=a_jv_capital", "=0"),
        "Churn exposure (ARR lost)": ("=lv_churn", "=lv_min_churn", "=a_ctrl_churn", "=0", "=0"),
        "Capital drag exposure (₹ Cr/yr)": (f"=Deal_CF!{yl(1)}{E['drag']}", f"={yl(1)}{M['drag']}", "=a_ctrl_drag", "=0", "=0"),
        "Year-1 EPS ex-MDR (₹)": ("=e_eps_y1", f"={yl(0)}{M['eps_y1']}", f"={yl(0)}{H['eps_y1']}", f"={yl(0)}{J['eps_y1']}", f"={yl(0)}{W['eps_y1']}"),
        "vs ₹7.50": ("=e_eps_y1/cf_eps-1", f"={yl(0)}{M['eps_y1']}/cf_eps-1", f"={yl(0)}{H['eps_y1']}/cf_eps-1", f"={yl(0)}{J['eps_y1']}/cf_eps-1", f"={yl(0)}{W['eps_y1']}/cf_eps-1"),
        "Year-3 EPS ex-MDR (₹)": ("=e_eps_y3", f"={yl(0)}{M['eps_y3']}", f"={yl(0)}{H['eps_y3']}", f"={yl(0)}{J['eps_y3']}", "=cf_eps"),
        "PAT breakeven year": ("=e_pat_be", f"={yl(0)}{M['cover']}", f"={yl(0)}{H['pat_be']}", "n/a (small)", "n/a"),
        "FCF breakeven year": ("=e_fcf_be", "n/a (no cash yield until exit)", f"={yl(0)}{H['fcf_be']}", "n/a (small)", "n/a"),
        "NPV to Paytm (₹ Cr)": ("=e_npv", f"={yl(0)}{M['npv']}", f"={yl(0)}{H['npv']}", f"={yl(0)}{J['npv']}", f"={yl(0)}{W['npv']}"),
        "Cash at risk if the thesis fails (₹ Cr)": ("=lv_price+lv_price*a_fees_pct+a_integ_full+e_pv_drag", "=lv_min_price+a_integ_min", "=lv_min_price+a_integ_min", "=a_jv_capital", "=a_build_cost"),
        "Control": ("Full, day one", "Negative control (≥ 25% blocks special resolutions); board seat; information rights", "Negative control now; full control optional after gates", "Shared; Paytm-majority in the JV only", "None"),
        "Blocks the PhonePe–Mastercard consortium?": ("Yes", "Partly: ROFR/ROFO on transfers + veto on new issuance/schemes; cannot stop a secondary sale of others' shares without ROFR", "Yes while the option lives (call + ROFR/ROFO + veto)", "No: Liminal itself remains for sale", "No"),
        "Reversibility": ("Low (integration, goodwill, reputational)", "Medium: tag/ROFO exit process; private stake is illiquid", "Medium before exercise; low after", "Medium: JV unwind clauses", "High"),
        "Time to capability": ("Immediate (if clients stay)", "Immediate via the commercial agreement", "Immediate via the commercial agreement", "12–24 months to build the JV products", "24–36 months build/partner (a_build_years)"),
        "Regulatory exposure": ("Highest: bank-like reserves (case §3.2), RBI change-in-control, CCI, SEBI preferential issue", "Lower: no consolidation; RBI comfort on minority treatment to be obtained; CCI depends on control rights", "As minority now; full set at exercise", "Moderate: JV licensing/PA scope", "None"),
        "Governance complexity": ("High: must run a ring-fence inside a wholly-owned subsidiary", "Moderate: shareholder agreement, reserved matters, information barriers", "Moderate → high after exercise", "High: two-parent JV", "None"),
    }
    for m, vals in S.items():
        rr = mrows[m]
        for j, v in enumerate(vals):
            if isinstance(v, str) and v.startswith("="):
                fmt = F_PCT if ("vs ₹7.50" in m or "exposure (ARR" in m) else (F_EPS if "EPS" in m else (F_X2 if "EBITDA after" in m else (F_YR if "breakeven" in m else (F_INR2 if "shares" in m else F_INR))))
                calc(ws, rr, 2 + j, v, fmt, bold=("NPV" in m), fill=FILL_OUT if "NPV" in m else None, border=True)
            else:
                text(ws, rr, 2 + j, v, wrap=True); ws.cell(row=rr, column=2 + j).border = BOX
        if any(isinstance(v, str) and not v.startswith("=") for v in vals): ws.row_dimensions[rr].height = 44
    for cidx in range(2, 7): ws.column_dimensions[col(cidx)].width = 26
    return ws

def build_scenarios(b):
    ws = b.sheet("Scenarios", tab_color="BF8F00", widths=WID)
    r = header(ws, 1, "SCENARIO TREE — base · upside · moderate downside · severe downside · break case (full acquisition), plus a one-variable-at-a-time test of which variable kills the deal first", ncols=14)
    r = note(ws, r, "Each scenario is a complete deal engine with its own parameter column (blue). The dominant-variable test flexes one input at a time from the base.")
    r += 1
    r = subheader(ws, r, "1. SCENARIO PARAMETERS (team assumptions)", ncols=14)
    names = ["Base", "Upside", "Moderate downside", "Severe downside", "Break case"]
    label(ws, r, "Parameter", bold=True)
    for j, n in enumerate(names):
        c = ws.cell(row=r, column=2 + j, value=n); style(c, bold=True, fill=FILL_SUB, align="center", border=True)
    hdr = r; r += 1
    params = [
        ("growth", "Liminal ARR growth", ["=a_g_base", "=a_g_bull", "=a_g_base", "=a_g_bear", "=a_g_bear"], F_PCT),
        ("churn", "ARR churn in year 1", [0.375, 0.10, 0.30, 0.45, 0.55], F_PCT),
        ("drag", "Capital drag (₹ Cr/yr)", [750, 500, 750, 1000, 1250], F_INR),
        ("mode", "Drag reading (1 fixed / 2 scales / 3 P&L)", [1, 1, 1, 1, 2], F_YR),
        ("cash", "Cash used (₹ Cr)", ["=lv_mix_cash"] * 5, F_INR),
        ("debt", "New debt (₹ Cr)", ["=lv_mix_debt"] * 5, F_INR),
        ("eq", "Equity issued (₹ Cr)", ["=lv_mix_eq"] * 5, F_INR),
        ("wacc", "WACC", ["=lv_wacc", "=lv_wacc-0.01", "=lv_wacc", "=lv_wacc+0.01", "=lv_wacc+0.02"], F_PCT),
        ("price", "Price paid (₹ Cr)", ["=lv_price"] * 5, F_INR),
        ("mdr", "Credit MDR to the deal? (0/1)", ["=lv_mdr_in_deal"] * 5, F_YR),
    ]
    prow = {}
    for key, lab, vals, fmt in params:
        label(ws, r, lab); prow[key] = r
        for j, v in enumerate(vals):
            if isinstance(v, str): link(ws, r, 2 + j, v, fmt)
            else: inp(ws, r, 2 + j, v, fmt, kind="assump")
        r += 1
    desc = ["Case midpoint churn, case drag, base growth, Dashboard mix.", "Low churn (ring-fence works), stronger growth, reserve partly structured away, lower WACC.", "~30% churn with the full ₹750 Cr drag.", "45% churn, ₹1,000 Cr drag, bear growth, higher WACC.", "55% churn (top-4 gone), ₹1,250 Cr drag scaling with assets, bear growth, valuation pressure (+2pp WACC)."]
    label(ws, r, "Narrative");
    for j, d in enumerate(desc): text(ws, r, 2 + j, d, wrap=True)
    ws.row_dimensions[r].height = 60; r += 2
    r = subheader(ws, r, "2. RESULTS", ncols=14)
    res_hdr = r
    label(ws, r, "Output", bold=True)
    for j, n in enumerate(names):
        c = ws.cell(row=r, column=2 + j, value=n); style(c, bold=True, fill=FILL_SUB, align="center", border=True)
    r += 1
    outs = [("Retained year-1 ARR (₹ Cr)", 'rev1', F_INR1), ("Effective multiple on retained ARR", 'eff_mult', F_X), ("Year-1 EPS ex-MDR (₹)", 'eps_y1', F_EPS), ("vs ₹7.50", 'acc1', F_PCT), ("Year-3 EPS ex-MDR (₹)", 'eps_y3', F_EPS),
            ("Year-1 FCF after cost of funds (₹ Cr)", 'fcf_y1', F_INR), ("Cumulative cash after 10 years (₹ Cr)", 'cum10', F_INR), ("PAT breakeven year", 'pat_be', F_YR), ("FCF breakeven year", 'fcf_be', F_YR), ("Payback year", 'payback', F_YR),
            ("Value of Liminal before drag (₹ Cr)", 'ev_lim', F_INR), ("PV of drag (₹ Cr)", 'pv_drag', F_INR), ("NPV to Paytm (₹ Cr)", 'npv', F_INR), ("Cash at end of year 3 (₹ Cr)", 'cash_y3', F_INR), ("Verdict at this price", 'verdict', F_GEN)]
    orow = {}
    for lab, key, fmt in outs:
        label(ws, r, lab, bold=(key in ('npv', 'verdict'))); orow[key] = r; r += 1
    r += 2
    r = subheader(ws, r, "3. WHICH VARIABLE KILLS THE DEAL FIRST? — one-at-a-time flex from the Base scenario (NPV, ₹ Cr)", ncols=14)
    tor_hdr = r
    tnames = ["Base", "Churn → 45%", "Drag → ₹1,250 Cr", "Growth → bear", "WACC +2pp", "Drag scales with assets (reading 2)", "Churn → 0% (best case)", "Drag → 0 (best case)"]
    label(ws, r, "Flex", bold=True)
    for j, n in enumerate(tnames):
        c = ws.cell(row=r, column=2 + j, value=n); style(c, bold=True, fill=FILL_SUB, align="center", border=True, wrap=True)
    ws.row_dimensions[r].height = 40; r += 1
    tparams = [
        ("growth", ["=a_g_base", "=a_g_base", "=a_g_base", "=a_g_bear", "=a_g_base", "=a_g_base", "=a_g_base", "=a_g_base"], F_PCT),
        ("churn", [0.375, 0.45, 0.375, 0.375, 0.375, 0.375, 0.0, 0.375], F_PCT),
        ("drag", [750, 750, 1250, 750, 750, 750, 750, 0], F_INR),
        ("mode", [1, 1, 1, 1, 1, 2, 1, 1], F_YR),
        ("wacc", ["=lv_wacc", "=lv_wacc", "=lv_wacc", "=lv_wacc", "=lv_wacc+0.02", "=lv_wacc", "=lv_wacc", "=lv_wacc"], F_PCT),
    ]
    tprow = {}
    for key, vals, fmt in tparams:
        label(ws, r, key); tprow[key] = r
        for j, v in enumerate(vals):
            if isinstance(v, str): link(ws, r, 2 + j, v, fmt)
            else: inp(ws, r, 2 + j, v, fmt, kind="assump")
        r += 1
    label(ws, r, "NPV to Paytm (₹ Cr)", bold=True); tnpv = r; r += 1
    label(ws, r, "Change vs Base (₹ Cr)", bold=True); tdelta = r; r += 1
    label(ws, r, "FCF breakeven year"); tfcf = r; r += 1
    label(ws, r, "Year-1 EPS (₹)"); teps = r; r += 1
    r = note(ws, r, "Reading: the largest negative change identifies the dominant risk driver at the base settings. Compare the 'best case' columns: if NPV stays negative with churn at 0% but turns positive with drag at 0, the DRAG kills the deal first; if the reverse, CHURN does.")
    r += 1
    # engines
    engines = []
    for j in range(5):
        c = col(2 + j)
        p = dict(g=f"'{ws.title}'!${c}${prow['growth']}", churn=f"'{ws.title}'!${c}${prow['churn']}", churn_year="a_churn_year", drag=f"'{ws.title}'!${c}${prow['drag']}", mode=f"'{ws.title}'!${c}${prow['mode']}",
                 cash=f"'{ws.title}'!${c}${prow['cash']}", debt=f"'{ws.title}'!${c}${prow['debt']}", eq=f"'{ws.title}'!${c}${prow['eq']}", wacc=f"'{ws.title}'!${c}${prow['wacc']}", price=f"'{ws.title}'!${c}${prow['price']}",
                 mdr_flag=f"'{ws.title}'!${c}${prow['mdr']}", integ="a_integ_full", fees_pct="a_fees_pct", syn_on="a_syn_on")
        r, E = engine(ws, r, p, f"ENGINE — scenario: {names[j]}")
        engines.append(E)
    for j, E in enumerate(engines):
        c = 2 + j
        calc(ws, orow['rev1'], c, f"={yl(1)}{E['rev']}", F_INR1)
        calc(ws, orow['eff_mult'], c, f"={yl(0)}{E['eff_mult']}", F_X)
        calc(ws, orow['eps_y1'], c, f"={yl(0)}{E['eps_y1']}", F_EPS)
        calc(ws, orow['acc1'], c, f"={yl(0)}{E['eps_y1']}/cf_eps-1", F_PCT)
        calc(ws, orow['eps_y3'], c, f"={yl(0)}{E['eps_y3']}", F_EPS)
        calc(ws, orow['fcf_y1'], c, f"={yl(0)}{E['fcf_y1']}", F_INR)
        calc(ws, orow['cum10'], c, f"={yl(0)}{E['cum10']}", F_INR)
        calc(ws, orow['pat_be'], c, f"={yl(0)}{E['pat_be']}", F_YR)
        calc(ws, orow['fcf_be'], c, f"={yl(0)}{E['fcf_be']}", F_YR)
        calc(ws, orow['payback'], c, f"={yl(0)}{E['payback']}", F_YR)
        calc(ws, orow['ev_lim'], c, f"={yl(0)}{E['ev_lim']}", F_INR)
        calc(ws, orow['pv_drag'], c, f"={yl(0)}{E['pv_drag']}", F_INR)
        calc(ws, orow['npv'], c, f"={yl(0)}{E['npv']}", F_INR, bold=True, fill=FILL_OUT, border=True)
        calc(ws, orow['cash_y3'], c, f"={yl(0)}{E['cash_y3']}", F_INR)
        calc(ws, orow['verdict'], c, f"=IF({yl(0)}{E['npv']}>=0,\"Value-creating at this price\",IF({yl(0)}{E['npv']}>=-lv_price*0.25,\"Destroys value: renegotiate price/structure\",\"Destroys value: do not acquire at this price\"))", F_GEN, bold=True)
    tengines = []
    for j in range(len(tnames)):
        c = col(2 + j)
        p = lever_params()
        p.update(g=f"'{ws.title}'!${c}${tprow['growth']}", churn=f"'{ws.title}'!${c}${tprow['churn']}", drag=f"'{ws.title}'!${c}${tprow['drag']}", mode=f"'{ws.title}'!${c}${tprow['mode']}", wacc=f"'{ws.title}'!${c}${tprow['wacc']}")
        r, E = engine(ws, r, p, f"ENGINE — flex: {tnames[j]}")
        tengines.append(E)
    for j, E in enumerate(tengines):
        c = 2 + j
        calc(ws, tnpv, c, f"={yl(0)}{E['npv']}", F_INR, bold=True, fill=FILL_OUT, border=True)
        calc(ws, tdelta, c, f"={col(c)}{tnpv}-$B${tnpv}", F_INR, bold=True)
        calc(ws, tfcf, c, f"={yl(0)}{E['fcf_be']}", F_YR)
        calc(ws, teps, c, f"={yl(0)}{E['eps_y1']}", F_EPS)
    b.scen = dict(names=names, orow=orow, engines=engines, tnpv=tnpv, tdelta=tdelta, tnames=tnames)
    for cidx in range(2, 10): ws.column_dimensions[col(cidx)].width = 16
    return ws

def build_thresholds(b):
    ws = b.sheet("Thresholds", tab_color="C00000", widths={"A": 70, "B": 18, "C": 70})
    r = header(ws, 1, "DECISION THRESHOLDS — computed triggers that turn the recommendation into conditional logic", ncols=3)
    r = note(ws, r, "Every threshold is a formula on the current Dashboard levers. Text in column C states the action.")
    r += 1
    T = {}
    def th(key, lab, f, fmt, action, bold=True):
        nonlocal r
        label(ws, r, lab, bold=bold); out(ws, r, 2, f, fmt); text(ws, r, 3, action, wrap=True); ws.row_dimensions[r].height = 30; T[key] = r; b.name(f"th_{key}", ws, f"B{r}"); r += 1
    r = subheader(ws, r, "A. PRICE AND VALUE", ncols=3)
    th('dcf', "Standalone DCF value of 100% of Liminal at Dashboard growth/WACC (₹ Cr)", "=dcf_ev", F_INR, "The most Paytm should pay for 100% on financial value alone, before churn, drag and any strategic premium.")
    th('be_growth', "10-year ARR growth needed for the standalone DCF to equal the price (zero churn, no drag)", "=dcf_be_growth", F_PCT, "If diligence cannot support this growth, the headline price is a strategic premium, not a financial value.")
    th('max_price_full', "Maximum price for 100% at Dashboard churn and drag = price + NPV (₹ Cr)", "=lv_price+e_npv", F_INR, "Reservation value for a full acquisition. Walk away above it whatever the consortium does.")
    th('max_price_nodrag', "Maximum price for 100% at Dashboard churn with NO capital drag (₹ Cr)", "=lv_price+e_npv+e_pv_drag", F_INR, "What the asset is worth to an owner who does not trigger the reserve, e.g. a bank-licensed or foreign buyer. The gap to the row above is the value of the capital-treatment question.")
    th('strat_prem', "Strategic premium embedded in the headline price (₹ Cr) = price − value after churn and drag", "=lv_price-(lv_price+e_npv)", F_INR, "Amount that must be justified by option/strategic value that the DCF cannot capture. Compare with Synergies 'what must be true'.")
    th('min_val', "Pro-rata DCF value of the minority stake at Dashboard growth (₹ Cr)", "=lv_stake*dcf_ev", F_INR, "Negotiating target for the minority price before any strategic premium; the Dashboard minority price minus this = premium paid for access/blocking.")
    gcols = {0.10: b.dcf_growths.index(0.10), 0.20: b.dcf_growths.index(0.20), 0.30: b.dcf_growths.index(0.30)}
    th('min_val_bear', "Pro-rata value of the stake at BEAR growth (10%) (₹ Cr)", f"=lv_stake*DCF!{col(yc(1+gcols[0.10]))}{b.dcf_sel_row}", F_INR, "Floor of the negotiating range.")
    th('min_val_base', "Pro-rata value of the stake at BASE growth (20%) (₹ Cr)", f"=lv_stake*DCF!{col(yc(1+gcols[0.20]))}{b.dcf_sel_row}", F_INR, "Base of the negotiating range.")
    th('min_val_bull', "Pro-rata value of the stake at BULL growth (30%) (₹ Cr)", f"=lv_stake*DCF!{col(yc(1+gcols[0.30]))}{b.dcf_sel_row}", F_INR, "Ceiling on financial value; anything above is paid for blocking/option value.")
    th('min_prem', "Premium in the Dashboard minority price over the base pro-rata value (₹ Cr)", "=lv_min_price-th_min_val_base", F_INR, "The explicit price of access + blocking rights + option: must be justified as such, not as an investment.")
    r = subheader(ws, r, "B. CHURN", ncols=3)
    th('max_churn', "Maximum churn at which the full acquisition still has NPV ≥ 0 at Dashboard price and drag", "=ch_max_churn", F_PCT, "Churn above this → renegotiate price/structure or do not proceed. 'none' means the deal is value-negative even with zero churn.")
    th('max_churn_nodrag', "Maximum churn with the drag set to zero", "=ch_max_churn_nodrag", F_PCT, "Isolates the churn question: this is the churn tolerance an owner without the reserve would have.")
    th('consent', "Minimum written client consents (% of ARR) before control is exercised (hybrid)", "=1-a_ctrl_churn", F_PCT, "Gate 1 for the call option. Consents below this → hold the minority; do not exercise.")
    th('top4_floor', "Retention floor below which the earn-out pays zero (retained ARR)", "=a_eo_floor", F_PCT, "Sellers receive nothing above the upfront below this retention: aligns them with retention.")
    r = subheader(ws, r, "C. CAPITAL DRAG", ncols=3)
    th('max_drag', "Break-even recurring capital drag at Dashboard price/churn (₹ Cr/yr)", "=cd_max_drag", F_INR, "A written RBI treatment above this → restructure (no consolidation) or walk away. Negative = no capacity for any drag at this price.")
    th('max_drag_gate', "Maximum drag consistent with FCF breakeven by the gate year (₹ Cr/yr)", "=cd_max_drag_gate", F_INR, "Gate 2 for exercising control.")
    th('drag_years', "Years of the case drag fundable from post-deal cash above the cash floor", "=(e_cash_after-a_min_cash)/lv_drag", F_INR1, "Liquidity runway if the drag applies and nothing else changes.")
    r = subheader(ws, r, "D. FINANCING AND RATING", ncols=3)
    th('max_debt', "Maximum new debt inside the leverage guardrail (₹ Cr) = cap × EBITDA − existing debt", "=a_max_lev*cf_ebitda-cf_debt", F_INR, "Debt above this breaches the AA- guardrail; use equity or cash instead.")
    th('max_cash', "Maximum cash deployable above the cash floor after one-time costs (₹ Cr)", "=cf_cash-a_min_cash-lv_price*a_fees_pct-a_integ_full", F_INR, "Cash above this breaches the liquidity guardrail.")
    th('dil_case', "Year-1 EPS dilution at the Dashboard mix vs ₹7.50", "=e_eps_y1/cf_eps-1", F_PCT, "Case §3.3: a large immediate EPS hit invites buyback-vs-M&A pressure. Board tolerance is a judgement; the Churn sheet shows the churn at which dilution exceeds 30%.")
    th('dil_like', "Year-1 EPS dilution vs the like-for-like standalone-with-MDR baseline", f"=Deal_CF!{yl(1)}{b.E['acc_mdr']}", F_PCT, "The honest comparison: the MDR lifts the standalone baseline; the deal must be measured against that.")
    r = subheader(ws, r, "E. HYBRID GATES (computed)", ncols=3)
    th('hy_gate', "Hybrid passes the ≤ N-year PAT and FCF breakeven gate after exercise? (1 = yes)", f"=Structures!{yl(0)}{b.H['gate']}", F_YR, "0 → HOLD the minority; 1 → eligible to exercise if consents, capital treatment, valuation cap and compliance gates also clear.")
    th('hy_npv', "Hybrid NPV at Dashboard levers (₹ Cr)", f"=Structures!{yl(0)}{b.H['npv']}", F_INR, "Negative → the option should not be exercised at these parameters; the minority is held or exited.")
    th('min_npv', "Minority-stake NPV at Dashboard levers (₹ Cr)", f"=Structures!{yl(0)}{b.M['npv']}", F_INR, "The financial cost of the blocking/access position: the premium paid over pro-rata value.")
    b.T = T
    return ws

def build_synergies(b):
    ws = b.sheet("Synergies", tab_color="548235", widths={"A": 44, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12, "G": 12, "H": 30, "I": 30, "J": 14})
    r = header(ws, 1, "SYNERGY TREE — every line tested for reality, incrementality, measurability, timing, ownership-dependence and double counting", ncols=10)
    r = note(ws, r, "Base case credits ZERO synergies (Inputs a_syn_on = 0). The upside quantification below uses the Inputs §G assumptions. The MDR is NOT a synergy and appears nowhere in this tree.")
    r += 1
    heads = ["Synergy line", "Year-3 value (₹ Cr)", "Real?", "Incremental to the deal?", "Needs ownership?", "Measurable?", "Timing", "Evidence / what must be true", "What prevents it", "Double-count risk"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 40; r += 1
    lines = [
        ("REVENUE — Paytm as anchor client: custody/MPC fees on tokenised-treasury, e₹ and cross-border settlement pilots", "=a_syn_partner_rev_y3", "Yes", "Yes (new revenue to Liminal)", "NO — a commercial agreement delivers it", "Yes (contracted fees)", "Y1–Y3", "Paytm's own settlement volumes; RBI e₹ pilot scope", "Pilot scale stays small; RBI scope; Liminal capacity", "Do not also count in 'strategic value'"),
        ("REVENUE — cross-sell to Paytm's merchant/institutional base (treasury, tokenised deposits)", "=a_syn_xsell_y3", "Plausible", "Partly", "Partly (distribution)", "Weak", "Y2–Y4", "Institutional demand for tokenised settlement in India; product not yet built", "Ring-fence forbids sharing client data; regulation of tokenised assets", "Overlaps with the anchor-client line"),
        ("REVENUE — institutional relationships (HDFC, Axis) opening bank distribution to Paytm", "=0", "No", "Negative", "n/a", "No", "—", "The case says these clients LEAVE on ownership", "Case §3.1", "—"),
        ("REVENUE — CBDC/e₹ infrastructure role", "=0", "Option", "Unclear", "No", "No", "Y3+", "RBI e₹ pilots; no revenue model yet", "RBI designs the rails itself; banks are the pilot participants", "Counted as strategic option value only"),
        ("REVENUE — cross-border settlement / stablecoin rails", "=0", "Option", "Unclear", "No", "No", "Y3+", "Depends on regulation of stablecoins/VDAs in India", "RBI stance on private stablecoins", "Option value only"),
        ("COST — shared services (finance, HR, cloud)", "=a_syn_cost", "Small", "Yes", "Yes", "Yes", "Y2+", "Set to zero deliberately", "Integration breaches the information barrier that protects the franchise", "—"),
        ("CAPITAL — treasury/cash pooling", "=0", "Negative", "Negative", "Yes", "Yes", "Y1", "The reserve requirement is the opposite of a capital synergy", "Case §3.2", "—"),
        ("STRATEGIC OPTION VALUE — owning the 'trust layer' for institutional digital-asset settlement", "n/q", "Real but unpriced", "Yes", "Partly (a minority + call option captures most of it)", "No", "Y3–Y10", "Institutional adoption in India; regulatory clarity", "Regulation; competition (global custodians); franchise damage from ownership", "Do not add to DCF"),
    ]
    for line in lines:
        for j, v in enumerate(line):
            if j == 1 and isinstance(v, str) and v.startswith("="): link(ws, r, 2, v, F_INR)
            else: text(ws, r, 1 + j, v, wrap=True)
        ws.row_dimensions[r].height = 48; r += 1
    r += 1
    r = subheader(ws, r, "UPSIDE QUANTIFICATION — what the credited synergies would be worth, and what the price REQUIRES", ncols=10)
    label(ws, r, "Year-3 synergy revenue credited if switched on (₹ Cr)"); calc(ws, r, 2, "=a_syn_partner_rev_y3+a_syn_xsell_y3", F_INR); r1 = r; r += 1
    label(ws, r, "…at the mature margin and after tax = annual synergy PAT/FCF at run-rate (₹ Cr)"); calc(ws, r, 2, f"=B{r1}*a_mcap*(1-a_tax)+a_syn_cost*(1-a_tax)", F_INR1); r2 = r; r += 1
    label(ws, r, "PV of synergies in the Dashboard engine when switched on (₹ Cr) — set Inputs a_syn_on = 1 to see it flow"); link(ws, r, 2, "=e_pv_syn", F_INR); r += 1
    label(ws, r, "Approximate capitalised value of the run-rate synergy at WACC − g (₹ Cr)"); calc(ws, r, 2, f"=B{r2}/(lv_wacc-a_tg)", F_INR); r += 1
    label(ws, r, "NPV of the full acquisition at Dashboard levers WITHOUT synergies (₹ Cr)"); link(ws, r, 2, "=e_npv", F_INR); rn = r; r += 1
    label(ws, r, "Annual after-tax synergy needed IN PERPETUITY to bring NPV to zero (₹ Cr/yr)", bold=True); out(ws, r, 2, f"=MAX(0,-B{rn})*(lv_wacc-a_tg)", F_INR); r += 1
    label(ws, r, "…as % of Liminal's current ARR", bold=True); out(ws, r, 2, f"=B{r-1}/cf_arr", F_PCT); r += 1
    label(ws, r, "…as a multiple of the year-3 synergy revenue credited above"); calc(ws, r, 2, f"=IF(B{r1}>0,B{r-2}/(B{r1}*a_mcap*(1-a_tax)),\"n/a\")", F_X); r += 1
    r = note(ws, r, "Reading: if the required perpetual synergy is a large multiple of anything the tree can evidence, the price is not a synergy story. Most of the tree is achievable by contract; ownership adds the churn and the reserve, not the synergies.", italic=False)
    return ws
