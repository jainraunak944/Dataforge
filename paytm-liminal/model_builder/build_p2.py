"""Part 2: Liminal_Ops, DCF, Deal_CF (engine at lever settings), Financing, Sources_Uses, Accretion."""
from common import *
from engine import *

WID = {"A": 62, "B": 12}
for t in range(0, 11): WID[yl(t)] = 11

def build_liminal_ops(b):
    ws = b.sheet("Liminal_Ops", tab_color="548235", widths=WID)
    r = header(ws, 1, "LIMINAL OPERATING FORECAST — 10 years, from case ARR ₹220 Cr and team assumptions (Inputs §D)", ncols=14)
    r = note(ws, r, "Block 1: standalone, no churn, at the Dashboard growth case. Block 2: after a full acquisition, with the Dashboard churn applied in the churn year. Revenue = ARR run-rate.")
    r += 1
    r, sa = lim_block(ws, r, dict(g="lv_g", churn="0", churn_year="a_churn_year"), "BLOCK 1 — Standalone Liminal (no churn) at the selected growth case")
    r, fa = lim_block(ws, r, dict(g="lv_g", churn="lv_churn", churn_year="a_churn_year"), "BLOCK 2 — Liminal after a FULL acquisition (case churn applied in year 1)")
    b.lim_sa = sa; b.lim_fa = fa
    # three-growth summary (for the DCF what-you-need-to-believe and the deck)
    r = subheader(ws, r, "BLOCK 3 — Standalone revenue and PAT by growth case (no churn), for reference", ncols=14)
    year_row(ws, r); yr = r; r += 1
    for lab, g in (("Bear", "a_g_bear"), ("Base", "a_g_base"), ("Bull", "a_g_bull")):
        label(ws, r, f"{lab} — revenue"); calc(ws, r, yc(0), "=cf_arr", F_INR1, color=GREEN)
        for t in range(1, NY + 1): calc(ws, r, yc(t), f"={yl(t-1)}{r}*(1+{g})", F_INR1)
        rr = r; r += 1
        label(ws, r, f"{lab} — PAT (margin ramp, tax on positive EBIT)"); calc(ws, r, yc(0), "=cf_lim_pat", F_INR1, color=GREEN)
        for t in range(1, NY + 1):
            calc(ws, r, yc(t), f"=({yl(t)}{rr}*(MIN(a_m0+a_mstep*{yl(t)}{yr},a_mcap)-a_da))*(1-a_tax*({yl(t)}{rr}*(MIN(a_m0+a_mstep*{yl(t)}{yr},a_mcap)-a_da)>0))", F_INR1)
        r += 1
    return ws

def fcf_row_closed(ws, r, g_expr, churn_expr, yr, lab):
    """One-row closed-form unlevered FCF for the DCF sensitivity helper (exact replica of lim_block logic; churn hits in a_churn_year)."""
    label(ws, r, lab)
    calc(ws, r, yc(0), "=0", F_INR1)
    for t in range(1, NY + 1):
        Y = f"{yl(t)}{yr}"; Yp = f"{yl(t-1)}{yr}"
        rev_nc = f"(cf_arr*(1+{g_expr})^{Y})"
        rev = f"({rev_nc}*IF({Y}>=a_churn_year,1-{churn_expr},1))"
        rev_prev = f"(cf_arr*(1+{g_expr})^{Yp}*IF({Yp}>=a_churn_year,1-{churn_expr},1))"
        m = f"MIN(a_m0+a_mstep*{Y},a_mcap)"
        sticky = f"IF({Y}=a_churn_year,a_sticky*({rev_nc}-{rev})*(1-{m}),0)"
        ebit = f"({rev}*({m}-a_da)-{sticky})"
        f = f"={ebit}-MAX(0,{ebit})*a_tax+{rev}*a_da-{rev}*a_capex-a_wc*({rev}-{rev_prev})"
        calc(ws, r, yc(t), f, F_INR1)
    return r

def build_dcf(b):
    ws = b.sheet("DCF", tab_color="548235", widths=WID)
    r = header(ws, 1, "DCF — standalone value of Liminal, what you need to believe for ₹4,000 Cr, and sensitivity grids", ncols=14)
    r = note(ws, r, "Unlevered FCF from Liminal_Ops Block 1 (standalone, no churn). End-year discounting. Terminal value = Gordon growth. This is the STANDALONE FINANCIAL value; strategic/option value is assessed separately (Structures, Synergies).")
    r += 1
    sa = b.lim_sa
    r = subheader(ws, r, "1. Standalone DCF at Dashboard settings (growth case, WACC)", ncols=14)
    year_row(ws, r); yr = r; r += 1
    label(ws, r, "Unlevered FCF (from Liminal_Ops Block 1)"); rf = r
    for t in range(0, NY + 1): link(ws, r, yc(t), f"=Liminal_Ops!{yl(t)}{sa['fcf']}", F_INR1)
    r += 1
    label(ws, r, "Discount factor"); rd = r
    calc(ws, r, yc(0), "=1", '0.000')
    for t in range(1, NY + 1): calc(ws, r, yc(t), f"=1/(1+lv_wacc)^{yl(t)}{yr}", '0.000')
    r += 1
    label(ws, r, "PV of FCF"); rpv = r
    for t in range(0, NY + 1): calc(ws, r, yc(t), f"={yl(t)}{rf}*{yl(t)}{rd}", F_INR1)
    r += 1
    rows = {}
    def sc(key, lab, f, fmt=F_INR, bold=False, fill=None):
        nonlocal r
        rows[key] = r; label(ws, r, lab, bold=bold); calc(ws, r, 2, f, fmt, bold=bold, fill=fill, border=bool(fill)); r += 1
    sc('pv', "Sum of PV of FCF, years 1–10 (₹ Cr)", f"=SUM({yl(1)}{rpv}:{yl(NY)}{rpv})")
    sc('tv', "Terminal value at Y10 (₹ Cr) = FCF10 × (1 + g) ÷ (WACC − g)", f"={yl(NY)}{rf}*(1+a_tg)/(lv_wacc-a_tg)")
    sc('pvtv', "PV of terminal value (₹ Cr)", f"=B{rows['tv']}*{yl(NY)}{rd}")
    sc('ev', "Standalone DCF value of 100% of Liminal (₹ Cr)", f"=B{rows['pv']}+B{rows['pvtv']}", bold=True, fill=FILL_OUT)
    b.name("dcf_ev", ws, f"B{rows['ev']}")
    sc('tv_share', "Share of value from terminal value", f"=B{rows['pvtv']}/B{rows['ev']}", F_PCT)
    sc('ev_arr', "Implied EV ÷ current ARR", f"=B{rows['ev']}/cf_arr", F_X)
    sc('vs_price', "DCF value − headline price (₹ Cr): negative = price exceeds standalone value", f"=B{rows['ev']}-lv_price", bold=True)
    sc('prem', "Price ÷ DCF value − 1 = premium over standalone value", f"=lv_price/B{rows['ev']}-1", F_PCT, bold=True)
    sc('stake_val', "DCF value of the minority stake (pro-rata, before minority discount) (₹ Cr)", f"=lv_stake*B{rows['ev']}")
    sc('stake_prem', "Minority price ÷ pro-rata DCF value − 1", f"=lv_min_price/B{rows['stake_val']}-1", F_PCT)
    r += 1
    # what you need to believe: growth grid
    r = subheader(ws, r, "2. WHAT YOU NEED TO BELIEVE — standalone DCF by 10-year growth rate (no churn, no drag), at the Dashboard WACC", ncols=14)
    r = note(ws, r, "Helper rows compute unlevered FCF for each growth rate with the same formulas as Liminal_Ops (closed form). The grid then discounts each row at several WACCs.")
    year_row(ws, r); yr2 = r; r += 1
    growths = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    g_rows = []
    for g in growths:
        label(ws, r, f"Growth {int(g*100)}% p.a. — FCF"); inp(ws, r, 2, g, F_PCT0, kind="assump")
        fcf_row_closed(ws, r, f"$B{r}", "0", yr2, f"Growth {int(g*100)}% p.a. — unlevered FCF")
        g_rows.append(r); r += 1
    r += 1
    label(ws, r, "WACC →", bold=True); waccs = [0.11, 0.12, 0.13, 0.14, 0.15]
    wcols = []
    for i, w in enumerate(waccs):
        c = yc(1 + i); inp(ws, r, c, w, F_PCT, kind="assump"); wcols.append(c)
    hdr = r; r += 1
    label(ws, r, "Growth ↓  /  DCF value of 100% (₹ Cr)", bold=True); r += 1
    grid_first = r
    for gi, g in enumerate(growths):
        label(ws, r, f"Growth {int(g*100)}%"); calc(ws, r, 2, f"=B{g_rows[gi]}", F_PCT0)
        for i, w in enumerate(waccs):
            wc = f"{col(wcols[i])}${hdr}"
            fr = f"{yl(1)}{g_rows[gi]}:{yl(NY)}{g_rows[gi]}"
            f = (f"=SUMPRODUCT({fr},1/(1+{wc})^{yl(1)}${yr2}:{yl(NY)}${yr2})"
                 f"+{yl(NY)}{g_rows[gi]}*(1+a_tg)/({wc}-a_tg)/(1+{wc})^{yl(NY)}${yr2}")
            calc(ws, r, wcols[i], f, F_INR)
        r += 1
    grid_last = r - 1
    # implied multiple grid
    r += 1
    label(ws, r, "Same grid as EV ÷ current ARR", bold=True); r += 1
    for gi, g in enumerate(growths):
        label(ws, r, f"Growth {int(g*100)}%")
        for i in range(len(waccs)):
            calc(ws, r, wcols[i], f"={col(wcols[i])}{grid_first+gi}/cf_arr", F_X)
        r += 1
    r += 1
    # breakeven growth at selected WACC (interpolated on the 13% column? use the selected lv_wacc via a dedicated column)
    r = subheader(ws, r, "3. BREAKEVEN GROWTH — growth rate at which the standalone DCF equals the price paid (at Dashboard WACC)", ncols=14)
    label(ws, r, "DCF at the Dashboard WACC by growth (helper)"); rsel = r
    for gi in range(len(growths)):
        fr = f"{yl(1)}{g_rows[gi]}:{yl(NY)}{g_rows[gi]}"
        f = (f"=SUMPRODUCT({fr},1/(1+lv_wacc)^{yl(1)}${yr2}:{yl(NY)}${yr2})"
             f"+{yl(NY)}{g_rows[gi]}*(1+a_tg)/(lv_wacc-a_tg)/(1+lv_wacc)^{yl(NY)}${yr2}")
        calc(ws, r, yc(1 + gi), f, F_INR)
    r += 1
    b.dcf_sel_row = rsel; b.dcf_growths = growths
    label(ws, r, "Growth grid (helper)"); rg = r
    for gi, g in enumerate(growths): calc(ws, r, yc(1 + gi), f"=B{g_rows[gi]}", F_PCT0)
    r += 1
    n = len(growths)
    rngv = f"{yl(1)}{rsel}:{yl(n)}{rsel}"; rngg = f"{yl(1)}{rg}:{yl(n)}{rg}"
    label(ws, r, "Number of grid points with DCF below the price (helper)"); calc(ws, r, 2, f"=COUNTIF({rngv},\"<\"&lv_price)", F_YR); rk = r; r += 1
    label(ws, r, "Breakeven 10-year growth rate for DCF = price (linear interpolation; 'n/a' if outside 10–50%)", bold=True)
    f = (f"=IF(OR(B{rk}=0,B{rk}={n}),\"outside grid\",INDEX({rngg},B{rk})+(INDEX({rngg},B{rk}+1)-INDEX({rngg},B{rk}))*"
         f"(lv_price-INDEX({rngv},B{rk}))/(INDEX({rngv},B{rk}+1)-INDEX({rngv},B{rk})))")
    out(ws, r, 2, f, F_PCT); b.name("dcf_be_growth", ws, f"B{r}"); r += 1
    r = note(ws, r, "Reading: the price is rational as a STANDALONE investment only if Liminal compounds ARR at ≥ this rate for ten years with zero churn and no capital drag, and still reaches a 25% EBITDA margin.")
    r += 1
    # churn x growth grid (exact blocks for 4 churn levels)
    r = subheader(ws, r, "4. VALUE OF THE RETAINED BUSINESS — churn (year 1) × growth, at Dashboard WACC; value of 100% (₹ Cr)", ncols=14)
    r = note(ws, r, "Exact closed-form rows: churn removes revenue permanently from year 1 and leaves half of its cost base for one year (Inputs a_sticky).")
    year_row(ws, r); yr3 = r; r += 1
    churns = [0.0, 0.30, 0.375, 0.45]
    cg = [0.10, 0.20, 0.30, 0.40]
    label(ws, r, "Churn ↓ / growth →", bold=True)
    for i, g in enumerate(cg): inp(ws, r, yc(1 + i), g, F_PCT0, kind="assump")
    hdr2 = r; r += 1
    res_start = r
    helper_rows = {}
    # write result rows first (reserve), then helpers below
    for ci, c in enumerate(churns):
        label(ws, r, f"Churn {c*100:.1f}%"); inp(ws, r, 2, c, F_PCT, kind="assump")
        r += 1
    r += 1
    label(ws, r, "Helper FCF rows (churn, growth):", bold=True); r += 1
    for ci, c in enumerate(churns):
        for gi, g in enumerate(cg):
            fcf_row_closed(ws, r, f"{col(yc(1+gi))}${hdr2}", f"$B${res_start+ci}", yr3, f"FCF: churn {c*100:.1f}%, growth {int(g*100)}%")
            helper_rows[(ci, gi)] = r; r += 1
    for ci, c in enumerate(churns):
        for gi, g in enumerate(cg):
            hr = helper_rows[(ci, gi)]
            fr = f"{yl(1)}{hr}:{yl(NY)}{hr}"
            f = (f"=SUMPRODUCT({fr},1/(1+lv_wacc)^{yl(1)}${yr3}:{yl(NY)}${yr3})"
                 f"+{yl(NY)}{hr}*(1+a_tg)/(lv_wacc-a_tg)/(1+lv_wacc)^{yl(NY)}${yr3}")
            calc(ws, res_start + ci, yc(1 + gi), f, F_INR)
    b.dcf_rows = rows
    return ws

def build_deal_cf(b):
    ws = b.sheet("Deal_CF", tab_color="C55A11", widths=WID)
    r = header(ws, 1, "DEAL CASH FLOWS & VALUE — full acquisition at the Dashboard levers (growth, churn, drag, mix, WACC, price)", ncols=14)
    r = note(ws, r, "This is the master engine. The same engine is replicated on Churn, Capital_Drag and Scenarios with different parameter sets. Read the scalar outputs at the bottom.")
    r += 1
    r, E = engine(ws, r, lever_params(), "FULL ACQUISITION — Dashboard levers")
    b.E = E
    for k in ('pat_be', 'fcf_be', 'fcf_be_mdr', 'pat_be_mdr', 'payback', 'npv', 'npv_mdr', 'ev_lim', 'pv_drag', 'eff_mult', 'eff_mult_drag', 'max_drag', 'eps_y1', 'eps_y3', 'fcf_y1', 'cum10', 'cash_after', 'debt_after', 'lev_after', 'pv_syn', 'pv_onetime', 'cash_y3'):
        b.name(f"e_{k}", ws, f"{yl(0)}{E[k]}")
    return ws

def build_financing(b):
    ws = b.sheet("Financing", tab_color="C55A11", widths={"A": 52, "B": 13, "C": 13, "D": 13, "E": 13, "F": 13, "G": 13, "H": 13, "I": 13, "J": 13, "K": 13, "L": 13, "M": 13, "N": 13, "O": 13, "P": 13})
    r = header(ws, 1, "FINANCING — cash / debt / equity mixes for the ₹4,000 Cr payout: liquidity, leverage, cost of funds, shares, year-1 EPS", ncols=16)
    r = note(ws, r, "Row 1 is the Dashboard mix. Rows 2–6 are preset mixes (blue inputs, editable). Case: the ₹2,100 Cr cash portion may come from existing cash, new debt or a mix; ₹1,900 Cr is paid in Paytm shares.")
    r += 1
    heads = ["Structure", "Cash used (₹ Cr)", "New debt (₹ Cr)", "New equity (₹ Cr)", "Total (₹ Cr)", "Check vs price", "New shares (Cr)", "Shares after (Cr)", "% of count issued", "Cash after close (₹ Cr)", "Gross debt after (₹ Cr)", "Gross debt ÷ EBITDA", "Net cash after (₹ Cr)", "Cost of funds after tax (₹ Cr/yr)", "Year-1 EPS ex-MDR (₹)", "Guardrails"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 42
    hdr = r; r += 1
    mixes = [
        ("Dashboard mix (selected)", "=lv_mix_cash", "=lv_mix_debt", "=lv_mix_eq", True),
        ("Case headline: ₹2,100 Cr from cash + ₹1,900 Cr shares", 2100, 0, 1900, False),
        ("₹2,100 Cr new debt + ₹1,900 Cr shares", 0, 2100, 1900, False),
        ("₹1,400 Cr cash + ₹700 Cr debt + ₹1,900 Cr shares", 1400, 700, 1900, False),
        ("All cash ₹4,000 Cr", 4000, 0, 0, False),
        ("All equity ₹4,000 Cr", 0, 0, 4000, False),
        ("₹2,100 Cr cash + ₹1,900 Cr debt (no dilution)", 2100, 1900, 0, False),
    ]
    E = b.E
    lim_pat1 = f"Liminal_Ops!{yl(1)}{b.lim_fa['pat']}"
    first = r
    for name, cash, debt, eq, sel in mixes:
        text(ws, r, 1, name, bold=sel)
        if sel:
            link(ws, r, 2, cash); link(ws, r, 3, debt); link(ws, r, 4, eq)
        else:
            inp(ws, r, 2, cash, F_INR, kind="assump"); inp(ws, r, 3, debt, F_INR, kind="assump"); inp(ws, r, 4, eq, F_INR, kind="assump")
        calc(ws, r, 5, f"=B{r}+C{r}+D{r}", F_INR)
        calc(ws, r, 6, f"=E{r}-lv_price", F_INR)
        calc(ws, r, 7, f"=D{r}/(c_price*(1-a_issue_disc))", F_INR2)
        calc(ws, r, 8, f"=cf_shares+G{r}", F_INR2)
        calc(ws, r, 9, f"=G{r}/cf_shares", F_PCT)
        calc(ws, r, 10, f"=cf_cash-B{r}-lv_price*a_fees_pct-a_integ_full", F_INR)
        calc(ws, r, 11, f"=cf_debt+C{r}", F_INR)
        calc(ws, r, 12, f"=K{r}/cf_ebitda", F_X2)
        calc(ws, r, 13, f"=J{r}-K{r}", F_INR)
        calc(ws, r, 14, f"=B{r}*a_yield*(1-a_tax)+C{r}*a_kd*(1-a_tax)", F_INR1)
        calc(ws, r, 15, f"=(cf_pat+{lim_pat1}-N{r}-a_ppa_on*lv_price*a_ppa_share/a_ppa_life*(1-a_tax))/H{r}", F_EPS, bold=True)
        calc(ws, r, 16, f"=IF(AND(J{r}>=a_min_cash,L{r}<=a_max_lev),\"OK\",\"BREACH: \"&IF(J{r}<a_min_cash,\"cash floor \",\"\")&IF(L{r}>a_max_lev,\"leverage cap\",\"\"))", F_GEN)
        r += 1
    last = r - 1
    b.fin_rows = (first, last)
    r += 1
    r = subheader(ws, r, "Reading the table", ncols=16)
    notes = [
        "Year-1 EPS here uses the Liminal post-churn PAT from Liminal_Ops Block 2 at the Dashboard churn, the after-tax cost of funds of each mix, and PPA amortisation if switched on; MDR excluded (it is a standalone Paytm item).",
        "At ~247x trailing earnings, Paytm shares are its cheapest currency in EPS terms (earnings yield 0.4% vs 4.5% after-tax cash yield), so more equity = less EPS dilution — but issuing 3.3% of the company for a breakeven asset is only 'cheap' while the stock holds its multiple.",
        "Debt-funding the ₹2,100 Cr cash leg takes gross debt/EBITDA from 0.5x to 3.8x — outside any reasonable AA- headroom. The guardrail column flags cash-floor and leverage-cap breaches.",
        "None of the mixes changes the economics of the deal (NPV); they only move the cost between shareholders (dilution), the P&L (interest, foregone yield) and the balance sheet (liquidity, leverage).",
    ]
    for n_ in notes: r = note(ws, r, n_, italic=False)
    r += 1
    r = subheader(ws, r, "Sensitivity of year-1 EPS (case headline mix) to the cost-of-funds assumptions", ncols=16)
    label(ws, r, "Cash yield ↓ / cost of debt →", bold=True)
    kds = [0.075, 0.085, 0.095, 0.10]
    for i, k in enumerate(kds): inp(ws, r, 2 + i, k, F_PCT, kind="assump")
    h2 = r; r += 1
    for y in (0.05, 0.06, 0.07):
        inp(ws, r, 1, y, F_PCT, kind="assump")
        for i in range(len(kds)):
            kc = f"{col(2+i)}${h2}"
            f = f"=(cf_pat+{lim_pat1}-lv_mix_cash*$A{r}*(1-a_tax)-lv_mix_debt*{kc}*(1-a_tax)-a_ppa_on*lv_price*a_ppa_share/a_ppa_life*(1-a_tax))/(cf_shares+lv_mix_eq/(c_price*(1-a_issue_disc)))"
            calc(ws, r, 2 + i, f, F_EPS)
        r += 1
    r = note(ws, r, "Uses the Dashboard mix. With the case headline mix (no new debt) only the cash-yield row matters.")
    return ws

def build_sources_uses(b):
    ws = b.sheet("Sources_Uses", tab_color="C55A11", widths={"A": 58, "B": 14, "C": 4, "D": 58, "E": 14})
    r = header(ws, 1, "SOURCES & USES — full acquisition (Dashboard mix), minority stake, and the hybrid control tranche", ncols=5)
    r += 1
    def su(r, title, uses, sources):
        r = subheader(ws, r, title, ncols=5)
        text(ws, r, 1, "USES", bold=True); text(ws, r, 4, "SOURCES", bold=True); r += 1
        n = max(len(uses), len(sources)); u0 = r
        for i in range(n):
            if i < len(uses):
                label(ws, r, uses[i][0]); calc(ws, r, 2, uses[i][1], F_INR)
            if i < len(sources):
                label(ws, r, sources[i][0], col=4); calc(ws, r, 5, sources[i][1], F_INR)
            r += 1
        label(ws, r, "Total uses", bold=True); calc(ws, r, 2, f"=SUM(B{u0}:B{r-1})", F_INR, bold=True, fill=FILL_OUT, border=True)
        label(ws, r, "Total sources", col=4, bold=True); calc(ws, r, 5, f"=SUM(E{u0}:E{r-1})", F_INR, bold=True, fill=FILL_OUT, border=True)
        tr = r; r += 1
        label(ws, r, "Check: sources − uses (must be 0)", bold=True); calc(ws, r, 2, f"=E{tr}-B{tr}", F_INR, bold=True, fill=FILL_WARN, border=True)
        return r + 2
    r = su(r, "A. FULL ACQUISITION — headline ₹4,000 Cr at the Dashboard mix",
           [("Purchase consideration — cash portion", "=lv_mix_cash+lv_mix_debt"),
            ("Purchase consideration — Paytm shares issued to Liminal shareholders", "=lv_mix_eq"),
            ("Transaction costs (fees % × price)", "=lv_price*a_fees_pct"),
            ("Integration / ring-fence build-out (one-time)", "=a_integ_full")],
           [("Existing balance-sheet cash", "=lv_mix_cash+lv_price*a_fees_pct+a_integ_full"),
            ("New debt", "=lv_mix_debt"),
            ("New Paytm equity issued to sellers (seller paper)", "=lv_mix_eq"),
            ("Deferred / contingent consideration", "=0")])
    r = note(ws, r, "Note: the case headline pays 100% upfront; deferred/contingent consideration is zero. The Earnout sheet shows how the same ₹4,000 Cr cap can be re-cut so that up to ~₹1,300–2,000 Cr becomes contingent.")
    r += 1
    r = su(r, "B. MINORITY STAKE — Dashboard stake and price",
           [("Secondary purchase from existing shareholders", "=lv_min_price*(1-a_primary_share)"),
            ("Primary subscription (new Liminal shares; cash stays in Liminal)", "=lv_min_price*a_primary_share"),
            ("Transaction costs", "=a_integ_min")],
           [("Existing balance-sheet cash", "=lv_min_price+a_integ_min"),
            ("New debt", "=0"), ("New Paytm equity", "=0")])
    r = su(r, "C. HYBRID — control tranche on exercising the call option (remaining stake), if all gates pass",
           [("Upfront control consideration at exercise", "=eo_upfront"),
            ("Retention earn-out (maximum; paid only for retained ARR)", "=eo_max"),
            ("Integration / ring-fence (one-time)", "=a_integ_full")],
           [("Existing balance-sheet cash", "=eo_cash+a_integ_full"),
            ("New debt", "=a_ctrl_debt"),
            ("Paytm shares (earn-out settled in shares, collared)", "=eo_max")])
    label(ws, r, "Check: upfront control cash + debt = upfront consideration (must be 0)", bold=True); calc(ws, r, 2, "=eo_cash+a_ctrl_debt-eo_upfront", F_INR, bold=True, fill=FILL_WARN, border=True); r += 1
    label(ws, r, "Maximum total ever payable under the hybrid (minority + upfront + max earn-out) (₹ Cr)", bold=True); out(ws, r, 2, "=lv_min_price+eo_upfront+eo_max", F_INR); b.name("hy_max_total", ws, f"B{r}"); r += 1
    label(ws, r, "Maximum unconditional commitment under the hybrid (₹ Cr)", bold=True); out(ws, r, 2, "=lv_min_price+a_integ_min", F_INR); r += 1
    b.su_ws = ws
    return ws

def build_accretion(b):
    ws = b.sheet("Accretion", tab_color="C55A11", widths=WID)
    r = header(ws, 1, "ACCRETION / DILUTION — full acquisition from the ₹7.50 baseline: Y0 (day-one annualised), Y1, Y2, Y3 (and to Y10)", ncols=14)
    r = note(ws, r, "Accounting view (EPS) and economic view (NPV) are deliberately separated: Liminal is breakeven, so EPS accretion is driven by shares and financing costs (case §2), not by value creation.")
    r += 1
    E = b.E
    r = subheader(ws, r, "1. EPS bridge at the Dashboard levers (links to Deal_CF)", ncols=14)
    year_row(ws, r); yr = r; r += 1
    lines = [
        ("Paytm standalone PAT ex-MDR (₹ Cr)", 'pat_sa', F_INR1),
        ("MDR PAT — standalone Paytm item (₹ Cr)", 'mdr_pat', F_INR1),
        ("Liminal PAT after churn (₹ Cr)", None, F_INR1),
        ("(−) Cost of funds after tax (₹ Cr)", 'cof', F_INR1),
        ("(−) PPA amortisation after tax (₹ Cr)", 'ppa', F_INR1),
        ("(−) Drag hitting PAT (reading 3 only) (₹ Cr)", 'drag_pl', F_INR1),
        ("(−) Foregone yield on trapped reserve capital (₹ Cr)", 'trap_int', F_INR1),
        ("→ Incremental PAT from the deal (₹ Cr)", 'inc_pat', F_INR1),
        ("Pro-forma PAT ex-MDR (₹ Cr)", 'pf_pat', F_INR1),
        ("New shares issued (Cr)", 'shares_new', F_INR2),
        ("Pro-forma diluted shares (Cr)", 'shares_pf', F_INR2),
        ("Standalone EPS ex-MDR (₹)", 'eps_sa', F_EPS),
        ("Pro-forma EPS ex-MDR (₹)", 'eps_pf', F_EPS),
        ("Accretion / (dilution) vs ₹7.50", 'acc', F_PCT),
        ("Standalone EPS incl. MDR — like-for-like baseline (₹)", 'eps_sa_mdr', F_EPS),
        ("Pro-forma EPS incl. MDR (₹)", 'eps_pf_mdr', F_EPS),
        ("Accretion / (dilution) vs like-for-like baseline", 'acc_mdr', F_PCT),
        ("Cash EPS ex-MDR, ex-PPA (₹)", 'eps_cash', F_EPS),
        ("Reported EPS ex-MDR incl. PPA amortisation (₹) — Ind AS view, whatever the toggle", 'eps_reported', F_EPS),
        ("'Mechanical' share-count-only EPS (₹) — the number that hides the dilution", 'eps_mech', F_EPS),
    ]
    for lab, key, fmt in lines:
        bold = key in ('inc_pat', 'eps_pf', 'acc')
        label(ws, r, lab, bold=bold)
        for t in range(0, NY + 1):
            if key is None:
                link(ws, r, yc(t), f"=Liminal_Ops!{yl(t)}{b.lim_fa['pat']}", fmt)
            elif key in ('cof', 'ppa', 'shares_new', 'shares_pf'):
                if t == 0: link(ws, r, yc(t), f"=Deal_CF!{yl(0)}{E[key]}", fmt)
                elif key in ('cof', 'ppa'): link(ws, r, yc(t), f"=Deal_CF!{yl(0)}{E[key]}", fmt)
                else: link(ws, r, yc(t), f"=Deal_CF!{yl(0)}{E[key]}", fmt)
            else:
                link(ws, r, yc(t), f"=Deal_CF!{yl(t)}{E[key]}", fmt, bold=bold)
        r += 1
    r += 1
    r = subheader(ws, r, "2. Year-1 EPS bridge in ₹ per share (case headline mix as on Dashboard)", ncols=14)
    label(ws, r, "Baseline EPS (case)"); link(ws, r, 2, "=cf_eps", F_EPS); r0 = r; r += 1
    label(ws, r, "Effect of new shares alone (mechanical)"); calc(ws, r, 2, f"=Deal_CF!{yl(1)}{E['eps_mech']}-cf_eps", F_EPS); r += 1
    label(ws, r, "Effect of cost of funds (foregone yield + interest)"); calc(ws, r, 2, f"=-Deal_CF!{yl(0)}{E['cof']}/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "Effect of Liminal's post-churn result"); calc(ws, r, 2, f"=Liminal_Ops!{yl(1)}{b.lim_fa['pat']}/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "Effect of PPA amortisation"); calc(ws, r, 2, f"=-Deal_CF!{yl(0)}{E['ppa']}/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "Effect of drag on PAT / trapped-capital yield (readings 3 / 1–2)"); calc(ws, r, 2, f"=-(Deal_CF!{yl(1)}{E['drag_pl']}+Deal_CF!{yl(1)}{E['trap_int']})/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "Effect of synergies (if switched on)"); calc(ws, r, 2, f"=Deal_CF!{yl(1)}{E['syn']}*(1-a_tax)/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "→ Year-1 pro-forma EPS ex-MDR (₹)", bold=True); out(ws, r, 2, f"=SUM(B{r0}:B{r-1})", F_EPS); r1 = r; r += 1
    label(ws, r, "Check vs Deal_CF (must be 0)"); calc(ws, r, 2, f"=B{r1}-Deal_CF!{yl(1)}{E['eps_pf']}", F_EPS, fill=FILL_WARN); r += 1
    label(ws, r, "Add: MDR (standalone Paytm item) per share"); calc(ws, r, 2, f"=Deal_CF!{yl(1)}{E['mdr_pat']}/Deal_CF!{yl(0)}{E['shares_pf']}", F_EPS); r += 1
    label(ws, r, "→ Year-1 pro-forma EPS incl. MDR (₹)"); calc(ws, r, 2, f"=B{r1}+B{r-1}", F_EPS, bold=True); r += 1
    r += 1
    r = subheader(ws, r, "3. Accounting accretion vs economic value — the two are not the same thing", ncols=14)
    label(ws, r, "Year-3 EPS accretion / (dilution) vs ₹7.50"); link(ws, r, 2, f"=Deal_CF!{yl(3)}{E['acc']}", F_PCT); r += 1
    label(ws, r, "PAT breakeven year (accounting)"); link(ws, r, 2, "=e_pat_be", F_YR); r += 1
    label(ws, r, "NPV to Paytm at the Dashboard levers (economic) (₹ Cr)"); link(ws, r, 2, "=e_npv", F_INR); r += 1
    label(ws, r, "Value of Liminal to Paytm before drag (₹ Cr)"); link(ws, r, 2, "=e_ev_lim", F_INR); r += 1
    label(ws, r, "PV of the capital drag (₹ Cr)"); link(ws, r, 2, "=e_pv_drag", F_INR); r += 1
    r = note(ws, r, "An EPS-accretive deal can destroy value (issue cheap paper for a low-return asset) and a dilutive deal can create it. Paytm at ~247x earnings makes almost any equity-funded purchase look 'cheap' on EPS. The Board should decide on NPV, retained-ARR economics and the capital drag, and treat EPS as a constraint (shareholder pressure, case §3.3), not as the objective.")
    return ws
