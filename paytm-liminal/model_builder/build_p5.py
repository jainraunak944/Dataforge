"""Part 5: External sheets (Comps, Precedents, Regulatory) placeholders filled from research JSON, Audit_Trail, Dashboard outputs, main assembly."""
import json, os
from common import *
from engine import *

def build_external(b, data):
    """data: dict with 'comps', 'precedents', 'regulatory', 'sources' lists (from research)."""
    # ---- Comps ----
    ws = b.sheet("Comps", tab_color="FFC000", widths={"A": 26, "B": 14, "C": 14, "D": 14, "E": 12, "F": 12, "G": 10, "H": 10, "I": 10, "J": 34, "K": 34, "L": 40, "M": 14})
    r = header(ws, 1, "COMPARABLE COMPANIES — EXTERNAL FACTS (sourced, dated). Used for context on what 18x ARR means; NEVER to replace case inputs.", ncols=13)
    r = note(ws, r, "Orange cells = EXTERNAL FACT with source and date. Multiples are as reported/derived at the stated date. 'n/d' = not disclosed. Comparability notes explain why each peer is or is not a benchmark for Liminal.")
    r += 1
    heads = ["Company (ticker)", "Market cap (US$ bn)", "EV (US$ bn)", "LTM revenue (US$ bn)", "Revenue growth", "EBITDA margin", "EV/Revenue", "EV/EBITDA", "P/E", "Why comparable", "Why not / adjustment", "Source (URL, date)", "Certainty"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 40; r += 1
    first = r
    for row in data.get("comps", []):
        for j, key in enumerate(["name", "mcap", "ev", "rev", "growth", "margin", "ev_rev", "ev_ebitda", "pe", "why", "why_not", "source", "certainty"]):
            v = row.get(key, "n/d")
            if isinstance(v, (int, float)):
                fmt = F_PCT if key in ("growth", "margin") else (F_X if key in ("ev_rev", "ev_ebitda", "pe") else F_INR1)
                inp(ws, r, 1 + j, v, fmt, kind="ext")
            else:
                text(ws, r, 1 + j, v, wrap=True, fill=FILL_EXT if j in (1,2,3,4,5,6,7,8) else None)
        ws.row_dimensions[r].height = 60; r += 1
    last = r - 1
    r += 1
    if last >= first:
        label(ws, r, "Median EV/Revenue of peers with data", bold=True); calc(ws, r, 2, f"=IFERROR(MEDIAN(G{first}:G{last}),\"n/d\")", F_X); r += 1
        label(ws, r, "Liminal headline multiple (case) for comparison", bold=True); link(ws, r, 2, "=c_mult", F_X); r += 1
        label(ws, r, "Implied value of Liminal at the peer median EV/Revenue (₹ Cr) — context only", bold=True); calc(ws, r, 2, f"=IFERROR(B{r-2}*cf_arr,\"n/d\")", F_INR); r += 1
    for n_ in data.get("comps_notes", []): r = note(ws, r, n_, italic=False)
    # ---- Precedents ----
    ws = b.sheet("Precedents", tab_color="FFC000", widths={"A": 34, "B": 12, "C": 14, "D": 14, "E": 12, "F": 30, "G": 22, "H": 30, "I": 40, "J": 12})
    r = header(ws, 1, "PRECEDENT TRANSACTIONS — EXTERNAL FACTS (sourced, dated). Context for the 18x ARR price; not case inputs.", ncols=10)
    r += 1
    heads = ["Transaction (acquirer – target)", "Date", "Value (US$ m)", "Target revenue/ARR (US$ m)", "Implied multiple", "Rationale / target profile", "Buyer type / regulatory notes", "Comparability to Liminal", "Source (URL, date)", "Certainty"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 40; r += 1
    for row in data.get("precedents", []):
        for j, key in enumerate(["deal", "date", "value", "target_rev", "multiple", "rationale", "buyer", "comparability", "source", "certainty"]):
            v = row.get(key, "n/d")
            if isinstance(v, (int, float)):
                inp(ws, r, 1 + j, v, F_X if key == "multiple" else F_INR, kind="ext")
            else:
                text(ws, r, 1 + j, v, wrap=True, fill=FILL_EXT if j in (1,2,3,4) else None)
        ws.row_dimensions[r].height = 60; r += 1
    r += 1
    for n_ in data.get("precedents_notes", []): r = note(ws, r, n_, italic=False)
    # ---- Regulatory ----
    ws = b.sheet("Regulatory", tab_color="FFC000", widths={"A": 30, "B": 50, "C": 40, "D": 40, "E": 18, "F": 12})
    r = header(ws, 1, "REGULATORY & LEGAL CONTEXT — EXTERNAL FACTS (sourced, dated) mapped to approval type. The case's constructed assumptions (e.g., the ₹750 Cr reserve) are NOT overridden by these facts.", ncols=6)
    r += 1
    heads = ["Item", "What it says", "Source (URL, date)", "Relevance to this deal", "Approval type (CP / CS / sequencing / diligence)", "Certainty"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 36; r += 1
    for row in data.get("regulatory", []):
        for j, key in enumerate(["item", "says", "source", "relevance", "type", "certainty"]):
            text(ws, r, 1 + j, row.get(key, ""), wrap=True, fill=FILL_EXT if j == 1 else None)
        ws.row_dimensions[r].height = 75; r += 1
    # ---- Sources ----
    ws = b.sheet("Sources", tab_color="FFC000", widths={"A": 6, "B": 60, "C": 80, "D": 16})
    r = header(ws, 1, "SOURCES — every external fact used in this workbook and the accompanying analysis", ncols=4)
    r += 1
    for j, h in enumerate(["#", "Source", "URL", "Date"]):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, border=True)
    r += 1
    for i, srow in enumerate(data.get("sources", []), 1):
        text(ws, r, 1, i); text(ws, r, 2, srow.get("name", ""), wrap=True); text(ws, r, 3, srow.get("url", ""), wrap=True); text(ws, r, 4, srow.get("date", ""))
        r += 1
    return ws

def build_audit(b):
    ws = b.sheet("Audit_Trail", tab_color="7F7F7F", widths={"A": 46, "B": 18, "C": 22, "D": 60, "E": 60})
    r = header(ws, 1, "AUDIT TRAIL — Source → Input → Formula → Output → Interpretation, for every decision-relevant number", ncols=5)
    r += 1
    for j, h in enumerate(["Output", "Value (live)", "Evidence class", "Trace: inputs and formula", "Interpretation"]):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, border=True, wrap=True)
    r += 1
    rows = [
        ("Headline multiple (Deal value ÷ ARR)", "=c_mult", F_X2, "CALCULATION", "cf_deal (case §2) ÷ cf_arr (case §2)", "The case rounds to 18x; exact 18.2x."),
        ("Implied Paytm share price", "=c_price", F_INR, "CALCULATION", "cf_mcap ÷ cf_shares (both case §1)", "Used to convert the ₹1,900 Cr equity leg into shares."),
        ("New shares for the equity leg (Cr)", "=c_new_shares_case", F_INR2, "CALCULATION", "cf_deal_eq ÷ c_price", "≈1.6% of the share count: the 'mechanical' dilution."),
        ("Standalone DCF value of Liminal", "=dcf_ev", F_INR, "ANALYST ASSUMPTION-driven CALCULATION", "Liminal_Ops Block 1 FCF (growth, margin ramp, tax, capex, WC assumptions) discounted at lv_wacc with Gordon TV at a_tg", "Financial value before churn/drag; compare with the ₹4,000 Cr price."),
        ("Breakeven growth for price = DCF", "=dcf_be_growth", F_PCT, "CALCULATION on assumptions", "DCF sheet §3: interpolation on the growth grid at lv_wacc", "What you must believe for 18x to be a financial (not strategic) price."),
        ("Year-1 EPS, full acquisition, Dashboard mix", "=e_eps_y1", F_EPS, "CALCULATION on case facts + assumptions", "Deal_CF: (cf_pat + Liminal post-churn PAT − cost of funds − PPA − drag P&L effects) ÷ (cf_shares + new shares)", "Compare with ₹7.50 (case) and with the standalone-with-MDR baseline."),
        ("Year-1 EPS dilution vs ₹7.50", "=e_eps_y1/cf_eps-1", F_PCT, "CALCULATION", "e_eps_y1 ÷ cf_eps − 1", "Case §3.3 shareholder-pressure lens."),
        ("Year-1 incremental FCF after drag and cost of funds", "=e_fcf_y1", F_INR, "CALCULATION", "Deal_CF fcf_post: Liminal FCF − drag − one-time − cost of funds", "Negative = the deal consumes cash every year."),
        ("FCF breakeven year (full acquisition)", "=e_fcf_be", F_YR, "CALCULATION", "Deal_CF: first year fcf_post ≥ 0 (99 = never within 10 years)", "Answers case §5.3 'how long to breakeven after the ₹750 Cr drag'."),
        ("PAT breakeven year (full acquisition)", "=e_pat_be", F_YR, "CALCULATION", "Deal_CF: first year incremental PAT ≥ 0", "Accounting breakeven (Addendum 1)."),
        ("NPV of the full acquisition to Paytm", "=e_npv", F_INR, "CALCULATION", "Value of Liminal (post-churn DCF) + synergies − PV drag − one-time − price", "Economic verdict at the Dashboard levers."),
        ("PV of the capital drag", "=e_pv_drag", F_INR, "CALCULATION", "Deal_CF: Σ drag_t × DF_t − recovery × trapped capital × DF_10", "Under reading 1 at 13%: ≈ the price itself."),
        ("Break-even capital drag", "=cd_max_drag", F_INR, "CALCULATION", "(NPV + PV drag) ÷ annuity factor", "Negative → no capacity for any reserve at this price."),
        ("Maximum acceptable churn at the headline price", "=ch_max_churn", F_PCT, "CALCULATION", "Churn sheet: interpolated churn at which NPV = 0", "Answers case §5.2 'what level of churn makes the deal unattractive'."),
        ("Maximum acceptable churn, drag = 0", "=ch_max_churn_nodrag", F_PCT, "CALCULATION", "Churn sheet, drag isolated", "Churn tolerance of a buyer without the reserve."),
        ("MDR reaching PAT/FCF", "=cf_mdr*a_mdr_flow*(1-a_tax)", F_INR1, "CASE FACT × ASSUMPTION", "cf_mdr (case §3.4) × a_mdr_flow × (1 − a_tax)", "Standalone Paytm item; offsets ~9% of the drag on a cash basis; not a synergy."),
        ("Minority price (Dashboard)", "=lv_min_price", F_INR, "ANALYST ASSUMPTION", "lv_stake × lv_price × (1 − lv_min_disc)", "Ceiling = pro-rata of headline; target below."),
        ("Minority-stake NPV", "=th_min_npv", F_INR, "CALCULATION", "Structures Block A: stake × DCF − price − one-time − PV drag at minority", "Premium paid for access and blocking rights."),
        ("Hybrid NPV", "=th_hy_npv", F_INR, "CALCULATION", "Structures Block B", "Value of minority + option path if exercised at the Inputs gate settings."),
        ("Hybrid maximum total consideration", "=hy_max_total", F_INR, "CALCULATION", "Sources_Uses C: minority + upfront + max earn-out", "Never exceeds the headline by construction."),
        ("Reservation value for 100% (max price)", "=th_max_price_full", F_INR, "CALCULATION", "lv_price + e_npv", "Walk-away line vs the consortium."),
    ]
    for lab, f, fmt, cls, trace, interp in rows:
        label(ws, r, lab); link(ws, r, 2, f, fmt); text(ws, r, 3, cls); text(ws, r, 4, trace, wrap=True); text(ws, r, 5, interp, wrap=True)
        ws.row_dimensions[r].height = 30; r += 1
    return ws

def build_dashboard_outputs(b):
    ws = b.wb["Dashboard"]; r = b.dash_outputs_row
    r = subheader(ws, r, "4. HEADLINE OUTPUTS — valuation → FCF → leverage → EPS → transaction economics → decision thresholds (green = key outputs)", ncols=7)
    heads = ["Output", "Full acquisition (levers)", "Minority stake", "Hybrid (minority + option)", "JV", "Walk away", "Read-across"]
    for j, h in enumerate(heads):
        c = ws.cell(row=r, column=1 + j, value=h); style(c, bold=True, fill=FILL_SUB, wrap=True, align="center", border=True)
    ws.row_dimensions[r].height = 30; r += 1
    H, M, J, W = b.H, b.M, b.J, b.W
    lines = [
        ("VALUATION — standalone DCF of 100% (₹ Cr)", "=dcf_ev", "=dcf_ev", "=dcf_ev", "n/a", "n/a", F_INR, "Financial value before churn and drag; compare with ₹4,000 Cr."),
        ("Headline multiple / effective multiple on retained ARR", "=e_eff_mult", "=lv_min_val100/cf_arr", f"=(lv_min_price+eo_total)/(cf_arr*(1+lv_g)^a_opt_year*(1-a_ctrl_churn))", "n/a", "n/a", F_X, "Full: price ÷ year-1 retained ARR. Minority: entry valuation ÷ ARR. Hybrid: total consideration ÷ retained ARR at exercise."),
        ("Breakeven 10-yr growth for DCF = price", "=dcf_be_growth", "", "", "", "", F_PCT, "What you need to believe."),
        ("FCF — year-1 incremental FCF after drag and cost of funds (₹ Cr)", "=e_fcf_y1", f"=Structures!{yl(1)}{M['fcf']}", f"=Structures!{yl(1)}{H['fcf']}", f"=Structures!{yl(1)}{J['fcf']}", f"=Structures!{yl(1)}{W['build']}", F_INR, "Cash consumed in year 1."),
        ("FCF breakeven year (99 = never within 10 yrs)", "=e_fcf_be", "n/a", f"=Structures!{yl(0)}{H['fcf_be']}", "n/a", "n/a", F_YR, "Case §5.3."),
        ("PAT breakeven year (99 = never within 10 yrs)", "=e_pat_be", f"=Structures!{yl(0)}{M['cover']}", f"=Structures!{yl(0)}{H['pat_be']}", "n/a", "n/a", F_YR, "Addendum 1: accounting breakeven."),
        ("LEVERAGE — gross debt ÷ EBITDA after close", "=e_lev_after", "=c_lev0", f"=Structures!{yl(0)}{H['lev_after_ctrl']}", "=c_lev0", "=c_lev0", F_X2, "Guardrail ≤ a_max_lev."),
        ("Cash after close (₹ Cr)", "=e_cash_after", f"=Structures!{yl(0)}{M['cash_after']}", f"=Structures!{yl(0)}{H['cash_after_ctrl']}", "=cf_cash-a_jv_capital", "=cf_cash", F_INR, "Guardrail ≥ a_min_cash."),
        ("EPS — year-1 pro-forma ex-MDR (₹)", "=e_eps_y1", f"=Structures!{yl(0)}{M['eps_y1']}", f"=Structures!{yl(0)}{H['eps_y1']}", f"=Structures!{yl(0)}{J['eps_y1']}", f"=Structures!{yl(0)}{W['eps_y1']}", F_EPS, "From the ₹7.50 baseline."),
        ("EPS — year-1 accretion / (dilution) vs ₹7.50", "=e_eps_y1/cf_eps-1", f"=Structures!{yl(0)}{M['eps_y1']}/cf_eps-1", f"=Structures!{yl(0)}{H['eps_y1']}/cf_eps-1", f"=Structures!{yl(0)}{J['eps_y1']}/cf_eps-1", f"=Structures!{yl(0)}{W['eps_y1']}/cf_eps-1", F_PCT, "Case §3.3 lens."),
        ("EPS — year-3 pro-forma ex-MDR (₹)", "=e_eps_y3", f"=Structures!{yl(0)}{M['eps_y3']}", f"=Structures!{yl(0)}{H['eps_y3']}", f"=Structures!{yl(0)}{J['eps_y3']}", "=cf_eps", F_EPS, ""),
        ("TRANSACTION ECONOMICS — NPV to Paytm (₹ Cr)", "=e_npv", f"=Structures!{yl(0)}{M['npv']}", f"=Structures!{yl(0)}{H['npv']}", f"=Structures!{yl(0)}{J['npv']}", f"=Structures!{yl(0)}{W['npv']}", F_INR, "Economic verdict."),
        ("Maximum total commitment (₹ Cr)", "=lv_price+lv_price*a_fees_pct+a_integ_full", "=lv_min_price+a_integ_min", "=hy_max_total", "=a_jv_capital", "=a_build_cost", F_INR, ""),
        ("Maximum unconditional commitment (₹ Cr)", "=lv_price+lv_price*a_fees_pct+a_integ_full", "=lv_min_price+a_integ_min", "=lv_min_price+a_integ_min", "=a_jv_capital", "=0", F_INR, "Cash at risk before any gate."),
        ("DECISION THRESHOLDS — max churn at headline price (NPV ≥ 0)", "=ch_max_churn", "", "", "", "", F_PCT, "Above this: renegotiate or walk."),
        ("Break-even capital drag (₹ Cr/yr)", "=cd_max_drag", "", "", "", "", F_INR, "Negative: no capacity for any reserve."),
        ("Reservation value for 100% at these levers (₹ Cr)", "=th_max_price_full", "", "", "", "", F_INR, "Walk-away line vs the consortium."),
        ("Strategic premium embedded in the headline (₹ Cr)", "=th_strat_prem", "", "", "", "", F_INR, "Must be justified by option value."),
        ("Hybrid passes the breakeven gate after exercise? (1 = yes)", "", "", "=th_hy_gate", "", "", F_YR, "0 → hold the minority."),
    ]
    for lab, *vals, fmt, ra in lines:
        label(ws, r, lab, bold=lab.isupper() or "—" in lab[:25])
        for j, v in enumerate(vals):
            if isinstance(v, str) and v.startswith("="):
                calc(ws, r, 2 + j, v, fmt, bold=True, fill=FILL_OUT, border=True)
            elif v:
                text(ws, r, 2 + j, v, italic=True, color=GREY)
        text(ws, r, 7, ra, italic=True, color=GREY, wrap=True)
        r += 1
    r += 1
    r = subheader(ws, r, "5. VERDICT LINES (formulas)", ncols=7)
    label(ws, r, "Full acquisition at these levers"); calc(ws, r, 2, "=IF(e_npv>=0,\"Value-creating\",\"Value-destroying: NPV \"&TEXT(e_npv,\"#,##0\")&\" Cr; FCF breakeven \"&IF(e_fcf_be=99,\"never in 10 yrs\",\"year \"&e_fcf_be))", F_GEN, bold=True); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7); r += 1
    label(ws, r, "Minority stake at these levers"); calc(ws, r, 2, "=IF(th_min_npv>=0,\"Financially self-supporting\",\"Costs \"&TEXT(-th_min_npv,\"#,##0\")&\" Cr of NPV = the price of access + blocking rights; justify as an option, not as an investment\")", F_GEN, bold=True); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7); r += 1
    label(ws, r, "Hybrid: exercise the option at these gate settings?"); calc(ws, r, 2, "=IF(AND(th_hy_gate=1,th_hy_npv>=0),\"Eligible to exercise (subject to consents, RBI treatment, compliance)\",\"HOLD the minority: \"&IF(th_hy_gate=0,\"breakeven gate fails; \",\"\")&IF(th_hy_npv<0,\"NPV negative at these terms\",\"\"))", F_GEN, bold=True); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7); r += 1
    return ws
