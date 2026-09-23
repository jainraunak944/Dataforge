"""Reusable 10-year blocks: Liminal operating block and the full-acquisition deal engine."""
from common import *

YC0 = 3                     # column of Y0
def yc(t): return YC0 + t   # column index for year t (Y0..Y10)
def yl(t): return col(yc(t))
NY = 10

def year_row(ws, r, title="Year"):
    label(ws, r, title, bold=True)
    for t in range(0, NY + 1):
        c = ws.cell(row=r, column=yc(t), value=t)
        style(c, bold=True, fmt='"Y"0', align="center", fill=FILL_SUB)
    return r

def lim_block(ws, r, p, title, show_all=True):
    """Liminal operating block. p: dict with formula strings: g, churn, churn_year.
    Returns dict of row numbers: yr, rev_nc, ret, rev, margin, sticky, ebitda, da, ebit, tax, pat, capex, dwc, fcf."""
    rows = {}
    r = subheader(ws, r, title, ncols=14)
    rows['yr'] = r; year_row(ws, r); r += 1
    Y = lambda t: f"{yl(t)}{{row}}"
    # revenue no churn
    rows['rev_nc'] = r; label(ws, r, "Revenue (ARR run-rate) before churn", indent=0)
    calc(ws, r, yc(0), "=cf_arr", F_INR1, color=GREEN)
    for t in range(1, NY + 1):
        calc(ws, r, yc(t), f"={yl(t-1)}{r}*(1+{p['g']})", F_INR1)
    r += 1
    rows['ret'] = r; label(ws, r, "Retention factor (1 − churn from churn year)")
    calc(ws, r, yc(0), "=1", F_PCT)
    for t in range(1, NY + 1):
        calc(ws, r, yc(t), f"=IF({yl(t)}{rows['yr']}>={p['churn_year']},1-{p['churn']},1)", F_PCT)
    r += 1
    rows['rev'] = r; label(ws, r, "Revenue after churn", bold=True)
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['rev_nc']}*{yl(t)}{rows['ret']}", F_INR1, bold=True)
    r += 1
    rows['margin'] = r; label(ws, r, "EBITDA margin (ramp)")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"=MIN(a_m0+a_mstep*{yl(t)}{rows['yr']},a_mcap)", F_PCT)
    r += 1
    rows['sticky'] = r; label(ws, r, "Sticky cost of lost revenue (churn year only)")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"=IF({yl(t)}{rows['yr']}={p['churn_year']},a_sticky*({yl(t)}{rows['rev_nc']}-{yl(t)}{rows['rev']})*(1-{yl(t)}{rows['margin']}),0)", F_INR1)
    r += 1
    rows['ebitda'] = r; label(ws, r, "EBITDA", bold=True)
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['rev']}*{yl(t)}{rows['margin']}-{yl(t)}{rows['sticky']}", F_INR1, bold=True)
    r += 1
    rows['da'] = r; label(ws, r, "Depreciation & amortisation")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['rev']}*a_da", F_INR1)
    r += 1
    rows['ebit'] = r; label(ws, r, "EBIT")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['ebitda']}-{yl(t)}{rows['da']}", F_INR1)
    r += 1
    rows['tax'] = r; label(ws, r, "Tax (only on positive EBIT; no group relief)")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"=MAX(0,{yl(t)}{rows['ebit']})*a_tax", F_INR1)
    r += 1
    rows['pat'] = r; label(ws, r, "PAT (net income)", bold=True)
    calc(ws, r, yc(0), "=cf_lim_pat", F_INR1, bold=True, color=GREEN)
    for t in range(1, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['ebit']}-{yl(t)}{rows['tax']}", F_INR1, bold=True)
    r += 1
    rows['capex'] = r; label(ws, r, "Capex")
    for t in range(0, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['rev']}*a_capex", F_INR1)
    r += 1
    rows['dwc'] = r; label(ws, r, "Increase in working capital")
    calc(ws, r, yc(0), "=0", F_INR1)
    for t in range(1, NY + 1):
        calc(ws, r, yc(t), f"=a_wc*({yl(t)}{rows['rev']}-{yl(t-1)}{rows['rev']})", F_INR1)
    r += 1
    rows['fcf'] = r; label(ws, r, "Unlevered free cash flow = PAT + D&A − capex − ΔWC", bold=True)
    calc(ws, r, yc(0), "=0", F_INR1)
    for t in range(1, NY + 1):
        calc(ws, r, yc(t), f"={yl(t)}{rows['pat']}+{yl(t)}{rows['da']}-{yl(t)}{rows['capex']}-{yl(t)}{rows['dwc']}", F_INR1, bold=True)
    r += 1
    rows['end'] = r
    return r + 1, rows

def engine(ws, r, p, title):
    """Full-acquisition deal engine. p: formula strings for g, churn, churn_year, drag, mode, cash, debt, eq, wacc, price, mdr_flag, integ, fees_pct, syn_on.
    Returns (next_row, rows) with output rows: eps rows, breakevens, npv etc."""
    r, L = lim_block(ws, r, p, title + " — Liminal operating block (post-churn)")
    rows = dict(L)
    yr = L['yr']
    r = subheader(ws, r, title + " — deal cash flows, earnings and value to Paytm", ncols=14)
    def row(key, lab, f0, ft, fmt=F_INR1, bold=False):
        nonlocal r
        rows[key] = r; label(ws, r, lab, bold=bold)
        if f0 is not None: calc(ws, r, yc(0), f0, fmt, bold=bold)
        for t in range(1, NY + 1):
            calc(ws, r, yc(t), ft(t), fmt, bold=bold)
        r += 1
    # financing quantities (scalar, placed in Y0 column)
    rows['shares_new'] = r; label(ws, r, "New Paytm shares issued (Cr) = equity consideration ÷ issue price")
    calc(ws, r, yc(0), f"={p['eq']}/(c_price*(1-a_issue_disc))", F_INR2); r += 1
    rows['shares_pf'] = r; label(ws, r, "Pro-forma diluted shares (Cr)")
    calc(ws, r, yc(0), f"=cf_shares+{yl(0)}{rows['shares_new']}", F_INR2); r += 1
    rows['cof'] = r; label(ws, r, "Cost of funds after tax (₹ Cr/yr) = foregone yield on cash used + interest on new debt")
    calc(ws, r, yc(0), f"={p['cash']}*a_yield*(1-a_tax)+{p['debt']}*a_kd*(1-a_tax)", F_INR1); r += 1
    rows['ppa_full'] = r; label(ws, r, "PPA amortisation after tax (₹ Cr/yr) — always computed (price × intangible share ÷ life × (1 − tax))")
    calc(ws, r, yc(0), f"={p['price']}*a_ppa_share/a_ppa_life*(1-a_tax)", F_INR1); r += 1
    rows['ppa'] = r; label(ws, r, "PPA amortisation charged in the headline EPS (₹ Cr/yr) = above × toggle a_ppa_on")
    calc(ws, r, yc(0), f"=a_ppa_on*{yl(0)}{rows['ppa_full']}", F_INR1); r += 1
    rows['onetime'] = r; label(ws, r, "One-time costs (₹ Cr): fees + integration, year 1")
    calc(ws, r, yc(0), f"={p['price']}*{p['fees_pct']}+{p['integ']}", F_INR1); r += 1
    # synergies (optional)
    row('syn', "Synergy EBITDA credited (₹ Cr) — zero unless switched on", "=0",
        lambda t: f"={p['syn_on']}*(a_syn_partner_rev_y3+a_syn_xsell_y3)*a_mcap*IF({yl(t)}{yr}=1,a_syn_ramp1,IF({yl(t)}{yr}=2,a_syn_ramp2,1))+{p['syn_on']}*IF({yl(t)}{yr}>=2,a_syn_cost,0)")
    # drag by mode
    row('drag', "Capital drag applied (₹ Cr/yr) — reading 1 fixed; 2 scales with revenue; 3 P&L cost (after-tax cash)", "=0",
        lambda t: f"=CHOOSE({p['mode']},{p['drag']},{p['drag']}*{yl(t)}{L['rev']}/cf_arr,{p['drag']}*(1-a_tax))")
    row('drag_pl', "Capital drag hitting PAT (₹ Cr/yr) — only under reading 3", "=0",
        lambda t: f"=IF({p['mode']}=3,{p['drag']}*(1-a_tax),0)")
    row('trapped', "Cumulative trapped reserve capital (₹ Cr) — readings 1 and 2", "=0",
        lambda t: f"=IF({p['mode']}=3,0,{yl(t-1)}{rows['trapped']}+{yl(t)}{rows['drag']})")
    row('trap_int', "Foregone after-tax yield on trapped capital (₹ Cr/yr) — hits PAT", "=0",
        lambda t: f"={yl(t-1)}{rows['trapped']}*a_yield*(1-a_tax)")
    # earnings
    row('pat_sa', "Paytm standalone PAT excluding MDR", "=cf_pat", lambda t: f"=cf_pat*(1+a_pat_growth)^{yl(t)}{yr}")
    row('mdr_pat', "MDR contribution to PAT (standalone Paytm item) = 115 × flow-through × (1 − tax)", "=0", lambda t: "=cf_mdr*a_mdr_flow*(1-a_tax)")
    row('eps_sa', "Standalone EPS excluding MDR (₹)", "=cf_eps", lambda t: f"={yl(t)}{rows['pat_sa']}/cf_shares", F_EPS)
    row('eps_sa_mdr', "Standalone EPS including MDR (₹) — like-for-like baseline", "=cf_eps", lambda t: f"=({yl(t)}{rows['pat_sa']}+{yl(t)}{rows['mdr_pat']})/cf_shares", F_EPS)
    row('inc_pat', "Incremental PAT from the deal = Liminal PAT + synergies×(1−t) − cost of funds − PPA − drag(P&L) − foregone yield on trapped capital",
        f"=-{yl(0)}{rows['cof']}-{yl(0)}{rows['ppa']}",
        lambda t: f"={yl(t)}{L['pat']}+{yl(t)}{rows['syn']}*(1-a_tax)-{yl(0)}{rows['cof']}-{yl(0)}{rows['ppa']}-{yl(t)}{rows['drag_pl']}-{yl(t)}{rows['trap_int']}", bold=True)
    row('pf_pat', "Pro-forma PAT excluding MDR", f"={yl(0)}{rows['pat_sa']}+{yl(0)}{rows['inc_pat']}", lambda t: f"={yl(t)}{rows['pat_sa']}+{yl(t)}{rows['inc_pat']}")
    row('eps_pf', "Pro-forma EPS excluding MDR (₹)", f"={yl(0)}{rows['pf_pat']}/{yl(0)}{rows['shares_pf']}", lambda t: f"={yl(t)}{rows['pf_pat']}/{yl(0)}{rows['shares_pf']}", F_EPS, bold=True)
    row('acc', "Accretion / (dilution) vs ₹7.50 case baseline", f"={yl(0)}{rows['eps_pf']}/cf_eps-1", lambda t: f"={yl(t)}{rows['eps_pf']}/cf_eps-1", F_PCT, bold=True)
    row('eps_pf_mdr', "Pro-forma EPS including MDR (₹)", f"={yl(0)}{rows['eps_pf']}", lambda t: f"=({yl(t)}{rows['pf_pat']}+{yl(t)}{rows['mdr_pat']})/{yl(0)}{rows['shares_pf']}", F_EPS)
    row('acc_mdr', "Accretion / (dilution) vs like-for-like standalone-with-MDR EPS", f"={yl(0)}{rows['acc']}", lambda t: f"={yl(t)}{rows['eps_pf_mdr']}/{yl(t)}{rows['eps_sa_mdr']}-1", F_PCT)
    row('eps_cash', "Cash EPS excluding MDR (adds back PPA amortisation) (₹)", f"=({yl(0)}{rows['pf_pat']}+{yl(0)}{rows['ppa']})/{yl(0)}{rows['shares_pf']}", lambda t: f"=({yl(t)}{rows['pf_pat']}+{yl(0)}{rows['ppa']})/{yl(0)}{rows['shares_pf']}", F_EPS)
    row('eps_reported', "Reported EPS ex-MDR including PPA amortisation whatever the toggle (₹) — Ind AS view", f"=({yl(0)}{rows['pf_pat']}-{yl(0)}{rows['ppa_full']}+{yl(0)}{rows['ppa']})/{yl(0)}{rows['shares_pf']}", lambda t: f"=({yl(t)}{rows['pf_pat']}-{yl(0)}{rows['ppa_full']}+{yl(0)}{rows['ppa']})/{yl(0)}{rows['shares_pf']}", F_EPS)
    row('eps_mech', "'Mechanical' EPS: share count only, no financing cost or Liminal result (₹) — for reference", f"={yl(0)}{rows['pat_sa']}/{yl(0)}{rows['shares_pf']}", lambda t: f"={yl(t)}{rows['pat_sa']}/{yl(0)}{rows['shares_pf']}", F_EPS)
    # cash flows
    row('fcf_pre', "Incremental FCF before financing = Liminal FCF + synergies×(1−t) − drag − one-time", None,
        lambda t: f"={yl(t)}{L['fcf']}+{yl(t)}{rows['syn']}*(1-a_tax)-{yl(t)}{rows['drag']}-IF({yl(t)}{yr}=1,{yl(0)}{rows['onetime']},0)")
    row('fcf_post', "Incremental FCF after cost of funds (cash view)", None,
        lambda t: f"={yl(t)}{rows['fcf_pre']}-{yl(0)}{rows['cof']}", bold=True)
    row('mdr_cash', "MDR after-tax cash (standalone Paytm item, shown beside the deal)", "=0", lambda t: f"={yl(t)}{rows['mdr_pat']}")
    row('fcf_post_mdr', "Incremental FCF after cost of funds, WITH the MDR credited (case-style view)", None,
        lambda t: f"={yl(t)}{rows['fcf_post']}+{yl(t)}{rows['mdr_cash']}")
    row('fcf_used', "FCF line used for the verdict (per Dashboard lever lv_mdr_in_deal)", None,
        lambda t: f"=IF({p['mdr_flag']}=1,{yl(t)}{rows['fcf_post_mdr']},{yl(t)}{rows['fcf_post']})")
    row('cum', "Cumulative cash: −total consideration at Y0, then FCF after cost of funds (payback view)", f"=-{p['price']}",
        lambda t: f"={yl(t-1)}{rows['cum']}+{yl(t)}{rows['fcf_used']}")
    row('df', "Discount factor at the selected WACC (end-year)", "=1", lambda t: f"=1/(1+{p['wacc']})^{yl(t)}{yr}", '0.000')
    # scalars: breakevens and value
    def scalar(key, lab, f, fmt=F_INR1, bold=False, fill=None):
        nonlocal r
        rows[key] = r; label(ws, r, lab, bold=bold); calc(ws, r, yc(0), f, fmt, bold=bold, fill=fill, border=bool(fill)); r += 1
    rng = lambda key: f"{yl(1)}{rows[key]}:{yl(NY)}{rows[key]}"
    # helper flag rows (LibreOffice-safe way to find the first year a line turns non-negative)
    row('f_pat', "helper: year if incremental PAT ≥ 0 else 99", "=99", lambda t: f"=IF({yl(t)}{rows['inc_pat']}>=0,{yl(t)}{yr},99)", F_YR)
    row('f_pat_mdr', "helper: year if incremental PAT + MDR ≥ 0 else 99", "=99", lambda t: f"=IF({yl(t)}{rows['inc_pat']}+{yl(t)}{rows['mdr_pat']}>=0,{yl(t)}{yr},99)", F_YR)
    row('f_fcf', "helper: year if FCF after cost of funds ≥ 0 else 99", "=99", lambda t: f"=IF({yl(t)}{rows['fcf_post']}>=0,{yl(t)}{yr},99)", F_YR)
    row('f_fcf_mdr', "helper: year if FCF after cost of funds + MDR ≥ 0 else 99", "=99", lambda t: f"=IF({yl(t)}{rows['fcf_post_mdr']}>=0,{yl(t)}{yr},99)", F_YR)
    row('f_cum', "helper: year if cumulative cash ≥ 0 else 99", "=99", lambda t: f"=IF({yl(t)}{rows['cum']}>=0,{yl(t)}{yr},99)", F_YR)
    scalar('pat_be', "PAT breakeven year (first year incremental PAT ≥ 0; 99 = beyond horizon)", f"=MIN({rng('f_pat')})", F_YR, bold=True, fill=FILL_OUT)
    scalar('pat_be_mdr', "PAT breakeven year if the MDR is credited to the deal", f"=MIN({rng('f_pat_mdr')})", F_YR)
    scalar('fcf_be', "FCF breakeven year, after drag and cost of funds (99 = beyond horizon)", f"=MIN({rng('f_fcf')})", F_YR, bold=True, fill=FILL_OUT)
    scalar('fcf_be_mdr', "FCF breakeven year if the MDR is credited to the deal", f"=MIN({rng('f_fcf_mdr')})", F_YR)
    scalar('payback', "Payback year (cumulative cash ≥ 0; 99 = beyond horizon)", f"=MIN({rng('f_cum')})", F_YR)
    scalar('cum10', "Cumulative cash after 10 years (₹ Cr)", f"={yl(NY)}{rows['cum']}", F_INR, bold=True)
    scalar('pv_fcf', "PV of Liminal unlevered FCF, years 1–10 (₹ Cr)", f"=SUMPRODUCT({rng('fcf')},{rng('df')})")
    scalar('tv', "Terminal value at Y10 = FCF10 × (1+g_t) ÷ (WACC − g_t) (₹ Cr)", f"={yl(NY)}{L['fcf']}*(1+a_tg)/({p['wacc']}-a_tg)")
    scalar('pv_tv', "PV of terminal value (₹ Cr)", f"={yl(0)}{rows['tv']}*{yl(NY)}{rows['df']}")
    scalar('ev_lim', "Value of Liminal to Paytm on these cash flows, before drag (₹ Cr)", f"={yl(0)}{rows['pv_fcf']}+{yl(0)}{rows['pv_tv']}", F_INR, bold=True)
    scalar('pv_drag', "PV of the capital drag over 10 years, net of any recovery of trapped capital (₹ Cr)", f"=SUMPRODUCT({rng('drag')},{rng('df')})-a_recovery*{yl(NY)}{rows['trapped']}*{yl(NY)}{rows['df']}", F_INR)
    scalar('pv_syn', "PV of synergies after tax (₹ Cr)", f"=SUMPRODUCT({rng('syn')},{rng('df')})*(1-a_tax)")
    scalar('pv_onetime', "PV of one-time costs (₹ Cr)", f"={yl(0)}{rows['onetime']}*{yl(1)}{rows['df']}")
    scalar('npv', "NPV to Paytm = value of Liminal + synergies − drag − one-time − price paid (₹ Cr)", f"={yl(0)}{rows['ev_lim']}+{yl(0)}{rows['pv_syn']}-{yl(0)}{rows['pv_drag']}-{yl(0)}{rows['pv_onetime']}-{p['price']}", F_INR, bold=True, fill=FILL_OUT)
    scalar('npv_mdr', "NPV if the MDR were (wrongly) credited to the deal (₹ Cr) — for the case-style view", f"={yl(0)}{rows['npv']}+SUMPRODUCT({rng('mdr_cash')},{rng('df')})", F_INR)
    scalar('eff_mult', "Effective multiple = price ÷ retained year-1 ARR", f"={p['price']}/{yl(1)}{L['rev']}", F_X, bold=True)
    scalar('eff_mult_drag', "Effective multiple including PV of drag = (price + PV drag) ÷ retained ARR", f"=({p['price']}+{yl(0)}{rows['pv_drag']})/{yl(1)}{L['rev']}", F_X)
    scalar('max_drag', "Break-even capital drag (₹ Cr/yr, reading 1): drag at which NPV = 0", f"=({yl(0)}{rows['npv']}+{yl(0)}{rows['pv_drag']})/SUMPRODUCT({rng('df')})", F_INR, bold=True)
    scalar('eps_y1', "Year-1 pro-forma EPS excluding MDR (₹)", f"={yl(1)}{rows['eps_pf']}", F_EPS, bold=True, fill=FILL_OUT)
    scalar('eps_y3', "Year-3 pro-forma EPS excluding MDR (₹)", f"={yl(3)}{rows['eps_pf']}", F_EPS)
    scalar('fcf_y1', "Year-1 incremental FCF after cost of funds (₹ Cr)", f"={yl(1)}{rows['fcf_post']}", F_INR, bold=True, fill=FILL_OUT)
    scalar('cash_after', "Paytm cash after close (₹ Cr) = cash − cash used − one-time", f"=cf_cash-{p['cash']}-{yl(0)}{rows['onetime']}", F_INR)
    scalar('debt_after', "Gross debt after close (₹ Cr)", f"=cf_debt+{p['debt']}", F_INR)
    scalar('lev_after', "Gross debt ÷ EBITDA after close", f"={yl(0)}{rows['debt_after']}/cf_ebitda", F_X2)
    scalar('cash_y3', "Paytm cash at end of year 3 if the deal's cash flows are absorbed (₹ Cr)", f"={yl(0)}{rows['cash_after']}+SUM({yl(1)}{rows['fcf_used']}:{yl(3)}{rows['fcf_used']})+3*cf_pat", F_INR)
    rows['end'] = r
    return r + 1, rows

def lever_params():
    return dict(g="lv_g", churn="lv_churn", churn_year="a_churn_year", drag="lv_drag", mode="lv_drag_mode",
                cash="lv_mix_cash", debt="lv_mix_debt", eq="lv_mix_eq", wacc="lv_wacc", price="lv_price",
                mdr_flag="lv_mdr_in_deal", integ="a_integ_full", fees_pct="a_fees_pct", syn_on="a_syn_on")
