"""Part 1: README, Dashboard (levers), Inputs (case facts + team assumptions)."""
from common import *

YEARS = list(range(0, 11))   # Y0..Y10
YC0 = 3                      # column index of Y0 (C); Y1 = D ... Y10 = M
def yc(t): return YC0 + t     # column index for year t

def build_readme(b):
    ws = b.sheet("README", tab_color="1F3864", widths={"A": 4, "B": 34, "C": 110})
    r = header(ws, 1, "PROJECT SATOSHI GATE — Paytm × Liminal Custody Solutions: transaction & accretion/dilution model", ncols=3, size=13)
    r = note(ws, r, "Prepared for the Board / Investment Committee discussion. All ₹ figures in Cr unless stated. Model date: 23 Sep 2026.", col=2)
    r += 1
    rows = [
        ("Purpose", "One workbook that traces every decision-relevant number from a labelled input to an output: valuation → FCF → leverage → EPS → transaction economics → decision thresholds."),
        ("Source of truth", "The case document 'Project Satoshi Gate' (5 pp.) and 'Addendum 1: Modeling Inputs and Clarifications' (1 p.). Case inputs are never replaced by outside figures. External facts are used only for context, comparables and regulatory sequencing, and are labelled as such."),
        ("Colour code", "Blue text on light-blue fill = CASE FACT (from the case document, cell comment gives the section). Blue text on yellow fill = TEAM / ANALYST ASSUMPTION (changeable). Blue text on orange fill = EXTERNAL FACT (sourced, dated). Black = formula. Green = link to another sheet. Green fill = key output."),
        ("How to use", "Change the levers on 'Dashboard' (growth case, churn, capital drag level and interpretation, financing mix, minority stake terms, WACC). Every downstream sheet recalculates. Do not type over black formula cells."),
        ("Sheet map", "Dashboard (levers + headline outputs) · Inputs (case facts, calculations on case facts, team assumptions) · Liminal_Ops (10-yr operating forecast, standalone and post-churn) · DCF (standalone value, what-you-need-to-believe, WACC×growth and churn×growth grids) · Financing (cash/debt/equity mixes, leverage, liquidity, cost of funds) · Sources_Uses · Accretion (EPS Y0–Y3 from the ₹7.50 baseline; accounting vs economic view) · Capital_Drag (three readings of the ₹750 Cr drag, ₹500–1,250 Cr grid, break-even drag, MDR offset) · Churn (0–60% grid, effective multiple, breakevens, maximum acceptable churn) · Structures (full / minority / JV / walk-away / hybrid side by side) · Earnout (retention-linked consideration, call-option strike, escrow) · Scenarios (base, upside, moderate, severe, break; dominant-variable test) · Thresholds (decision triggers, computed) · Synergies (tree with incrementality tests) · Comps · Precedents · Regulatory (external, sourced) · Audit_Trail."),
        ("Conventions", "Y0 = trailing twelve months at signing (mid-Sep 2026). Y1 = first 12 months after close. Liminal revenue is modelled as ARR run-rate. Percentages stored as fractions. Negative = outflow. Breakeven year = first year in which the incremental line is ≥ 0 (PAT: accounting; FCF: cash, after capital drag and cost of funds)."),
        ("Evidence classes", "CASE FACT · CALCULATION (arithmetic on case facts) · ANALYST ASSUMPTION · EXTERNAL FACT (sourced) · INFERENCE · UNKNOWN. Every important number on the Audit_Trail sheet carries one of these tags."),
        ("Not modelled", "Purchase-price-allocation amortisation is shown as a switchable line (default on for reported EPS, off for cash EPS). Liminal's tax-loss carry-forwards are ignored (conservative). Paytm standalone earnings are held flat at ₹480 Cr unless the growth lever is changed, so that the deal effect is isolated. Currency: ₹ only; the ~$470M is the case's own conversion."),
    ]
    for k, v in rows:
        text(ws, r, 2, k, bold=True)
        text(ws, r, 3, v, wrap=True)
        ws.row_dimensions[r].height = 15 * max(1, (len(v) // 105) + 1)
        r += 1
    return ws

def build_inputs(b):
    ws = b.sheet("Inputs", tab_color="2F75B5", widths={"A": 46, "B": 16, "C": 14, "D": 60})
    r = header(ws, 1, "INPUTS — case facts, calculations on case facts, and team assumptions", ncols=4)
    r = note(ws, r, "Blue on light-blue = CASE FACT (comment = case section). Blue on yellow = TEAM ASSUMPTION (per Addendum 1, disclosed and flexed). Black = calculation.")
    r += 1
    # ---------------- CASE FACTS ----------------
    r = subheader(ws, r, "A. CASE FACTS — Paytm baseline (case §1, 'Baseline financials (assume for modeling)')", ncols=4)
    cf = [
        ("cf_mcap", "Market capitalisation (₹ Cr)", 118750, F_INR, "Case §1 and §2 table: ₹1,18,750 Cr (~$14B), mid-Sep 2026. Case note: real, verified fact."),
        ("cf_shares", "Diluted shares outstanding (Cr)", 64, F_INR1, "Case §1: 64 Cr diluted shares."),
        ("cf_cash", "Cash (₹ Cr)", 8900, F_INR, "Case §1: ₹8,900 Cr cash."),
        ("cf_debt", "Gross debt (₹ Cr)", 350, F_INR, "Case §1: ₹350 Cr gross debt."),
        ("cf_rev", "Trailing revenue (₹ Cr)", 8450, F_INR, "Case §1: trailing revenue ₹8,450 Cr."),
        ("cf_ebitda", "EBITDA (₹ Cr)", 640, F_INR, "Case §1: EBITDA ₹640 Cr."),
        ("cf_pat", "PAT (₹ Cr)", 480, F_INR, "Case §1: PAT ₹480 Cr. Starting point for all dilution calculations (case §5.3)."),
        ("cf_eps", "Diluted EPS (₹)", 7.50, F_EPS, "Case §1: diluted EPS ₹7.50. Baseline for §5.3."),
    ]
    for nm, lab, val, fmt, cm in cf:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="case", comment=cm); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    label(ws, r, "Credit rating"); c = inp(ws, r, 2, "CRISIL AA- (Stable)", F_GEN, kind="case", comment="Case §1."); r += 1
    r += 1
    r = subheader(ws, r, "B. CASE FACTS — Liminal and the proposed transaction (case §2, §3)", ncols=4)
    cf2 = [
        ("cf_deal", "Headline deal value (₹ Cr)", 4000, F_INR, "Case §2: ₹4,000 Cr (~$470M)."),
        ("cf_deal_cash", "  of which cash consideration (₹ Cr)", 2100, F_INR, "Case §2: ₹2,100 Cr cash; may be funded from balance-sheet cash, new debt, or a mix."),
        ("cf_deal_eq", "  of which equity consideration (₹ Cr)", 1900, F_INR, "Case §2: ₹1,900 Cr equity (Paytm shares issued to Liminal shareholders)."),
        ("cf_arr", "Liminal ARR (₹ Cr)", 220, F_INR, "Case §2 table: Target ARR ₹220 Cr (~$26M)."),
        ("cf_lim_pat", "Liminal net income today (₹ Cr)", 0, F_INR, "Case §2: 'approximately breakeven at the net income level today'."),
        ("cf_top4", "Top-4 clients' share of ARR (HDFC Bank, Axis Bank, CoinDCX, ZebPay)", 0.60, F_PCT, "Case §2: together 60% of Liminal's ARR."),
        ("cf_churn_lo", "ARR lost within 12 months of a FULL acquisition — low end", 0.30, F_PCT, "Case §3.1: assume 30% to 45% of ARR lost within 12 months of a full acquisition."),
        ("cf_churn_hi", "ARR lost within 12 months of a FULL acquisition — high end", 0.45, F_PCT, "Case §3.1."),
        ("cf_drag", "Recurring annual FCF drag from bank-like capital reserves if Paytm owns the custody infrastructure (₹ Cr/yr)", 750, F_INR, "Case §3.2: RBI requires bank-like capital reserves against custodied assets because Paytm holds a PA licence, not a banking licence → recurring annual FCF drag ₹750 Cr (~$88M)."),
        ("cf_mdr", "Incremental net revenue to Paytm from the new UPI MDR (₹ Cr/yr)", 115, F_INR, "Case §3.4: 0.4% MDR on P2M UPI > ₹2,000, capped ₹300/txn, effective 15 Oct 2026; assume ₹115 Cr/yr incremental net revenue for Paytm. Case note: the MDR framework is a real fact; the ₹115 Cr is the case's modelling input."),
    ]
    for nm, lab, val, fmt, cm in cf2:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="case", comment=cm); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    label(ws, r, "Competing bidder"); inp(ws, r, 2, "PhonePe–Mastercard exploratory consortium", F_GEN, kind="case", comment="Case §2: formed to acquire Liminal should Paytm walk away. No price or terms given."); r += 1
    label(ws, r, "Case's stated implied multiple"); inp(ws, r, 2, "18x Deal Value / ARR", F_GEN, kind="case", comment="Case §2 table."); r += 1
    r += 1
    # ---------------- CALCULATIONS ON CASE FACTS ----------------
    r = subheader(ws, r, "C. CALCULATIONS on case facts (no assumptions involved)", ncols=4)
    calcs = [
        ("c_price", "Implied Paytm share price (₹) = market cap ÷ diluted shares", "=cf_mcap/cf_shares", F_INR),
        ("c_pe", "Paytm trailing P/E = market cap ÷ PAT", "=cf_mcap/cf_pat", F_X),
        ("c_earn_yield", "Paytm earnings yield = PAT ÷ market cap", "=cf_pat/cf_mcap", '0.00%'),
        ("c_mult", "Headline multiple = deal value ÷ ARR", "=cf_deal/cf_arr", F_X2),
        ("c_new_shares_case", "New Paytm shares for the ₹1,900 Cr equity leg (Cr) = equity ÷ share price", "=cf_deal_eq/c_price", F_INR2),
        ("c_pct_co_case", "…as % of existing share count", "=c_new_shares_case/cf_shares", F_PCT),
        ("c_top4_arr", "Top-4 clients' ARR (₹ Cr)", "=cf_arr*cf_top4", F_INR),
        ("c_churn_lo_arr", "ARR at risk — low (₹ Cr)", "=cf_arr*cf_churn_lo", F_INR1),
        ("c_churn_hi_arr", "ARR at risk — high (₹ Cr)", "=cf_arr*cf_churn_hi", F_INR1),
        ("c_churn_of_top4_lo", "Case churn as % of top-4 book — low", "=cf_churn_lo/cf_top4", F_PCT),
        ("c_churn_of_top4_hi", "Case churn as % of top-4 book — high", "=cf_churn_hi/cf_top4", F_PCT),
        ("c_drag_v_ebitda", "Capital drag ÷ Paytm EBITDA", "=cf_drag/cf_ebitda", F_PCT),
        ("c_drag_v_pat", "Capital drag ÷ Paytm PAT", "=cf_drag/cf_pat", F_PCT),
        ("c_drag_v_arr", "Capital drag ÷ Liminal ARR", "=cf_drag/cf_arr", F_X),
        ("c_mdr_v_drag", "MDR net revenue ÷ capital drag (gross, revenue line)", "=cf_mdr/cf_drag", F_PCT),
        ("c_deal_v_mcap", "Deal value ÷ Paytm market cap", "=cf_deal/cf_mcap", F_PCT),
        ("c_deal_v_cash", "Cash consideration ÷ Paytm cash", "=cf_deal_cash/cf_cash", F_PCT),
        ("c_netcash0", "Paytm net cash today (₹ Cr)", "=cf_cash-cf_debt", F_INR),
        ("c_lev0", "Gross debt ÷ EBITDA today", "=cf_debt/cf_ebitda", F_X2),
    ]
    for nm, lab, f, fmt in calcs:
        label(ws, r, lab); calc(ws, r, 2, f, fmt); b.name(nm, ws, f"B{r}"); r += 1
    r += 1
    # ---------------- TEAM ASSUMPTIONS ----------------
    r = subheader(ws, r, "D. TEAM ASSUMPTIONS — Liminal operating model (Addendum 1: unstated parameters are team assumptions)", ncols=4)
    ta = [
        ("a_g_bear", "Liminal ARR growth — bear case (p.a.)", 0.10, F_PCT, "Bear: growth slows to a mature-SaaS rate. Range tested 0–40% on DCF sheet."),
        ("a_g_base", "Liminal ARR growth — base case (p.a.)", 0.20, F_PCT, "Base: an infrastructure SaaS provider at ₹220 Cr ARR growing 20%. Deliberately below the growth that justifies 18x (see DCF 'what you need to believe')."),
        ("a_g_bull", "Liminal ARR growth — bull case (p.a.)", 0.30, F_PCT, "Bull: sustained 30% for a decade; consistent with institutional digital-asset adoption scaling in India/UAE/Singapore."),
        ("a_m0", "EBITDA margin today", 0.0, F_PCT, "Case: ~breakeven at net income. We set EBITDA ≈ 0 today (D&A ≈ capex, no tax)."),
        ("a_mstep", "EBITDA margin improvement per year (pp)", 0.05, F_PCT, "Operating leverage of an infrastructure SaaS: +5pp per year."),
        ("a_mcap", "EBITDA margin cap (mature)", 0.25, F_PCT, "Mature margin of a regulated custody/infra business with compliance and security cost load; below pure software (30–40%)."),
        ("a_tax", "Tax rate", 0.25, F_PCT, "Indian corporate rate ~25.2% (s.115BAA). Losses not group-relieved (no group relief in India); Liminal's own carry-forwards ignored (conservative)."),
        ("a_da", "D&A as % of revenue", 0.03, F_PCT, "Asset-light: mostly software, HSMs, security infrastructure."),
        ("a_capex", "Capex as % of revenue", 0.03, F_PCT, "≈ D&A in steady state."),
        ("a_wc", "Working capital as % of incremental revenue", 0.05, F_PCT, "Custody fees billed monthly/quarterly; modest receivables."),
        ("a_sticky", "Share of lost revenue's cost base that stays for one year after churn", 0.50, F_PCT, "Costs do not fall as fast as revenue: half of the cost base tied to lost clients persists for 12 months (a 37.5% revenue loss on a breakeven cost base is a loss, not zero)."),
        ("a_churn_year", "Year in which full-acquisition churn hits (case: within 12 months)", 1, F_YR, "Case §3.1: within 12 months of a full acquisition → year 1."),
        ("a_horizon", "Explicit forecast horizon (years)", 10, F_YR, "10 years; terminal value thereafter."),
    ]
    for nm, lab, val, fmt, cm in ta:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    r += 1
    r = subheader(ws, r, "E. TEAM ASSUMPTIONS — financing, cost of capital, accounting", ncols=4)
    ta2 = [
        ("a_yield", "Pre-tax yield on Paytm surplus cash (opportunity cost of cash used)", 0.06, F_PCT, "Treasury yield on liquid Indian debt funds/deposits; tested 5–7%."),
        ("a_kd", "Pre-tax cost of new debt for a CRISIL AA- issuer", 0.085, F_PCT, "AA- corporate bond/term-loan pricing; tested 8–10%. Interest is tax-deductible."),
        ("a_issue_disc", "Discount to market on Paytm shares issued as consideration", 0.0, F_PCT, "0% base: SEBI ICDR preferential-issue floor pricing (90-day / 10-day VWAP) usually allows issuance near market; flex for a compressed stock."),
        ("a_fees_pct", "Transaction costs as % of consideration", 0.015, F_PCT, "Advisory, legal, diligence, stamp duty: ~1.5% of consideration (one-time, expensed, not in run-rate EPS)."),
        ("a_integ_full", "One-time integration/separation cost at full acquisition (₹ Cr)", 100, F_INR, "Ring-fence build-out, information barriers, independent compliance, retention pool (cash, year 1)."),
        ("a_integ_min", "One-time costs for a minority investment (₹ Cr)", 15, F_INR, "Diligence, documentation, shareholder agreement."),
        ("a_min_cash", "Liquidity guardrail — minimum cash to hold (₹ Cr)", 5000, F_INR, "Team guardrail to protect the AA- rating and PA-licence net-worth/escrow needs: keep ≥ ₹5,000 Cr (~7 months of revenue)."),
        ("a_max_lev", "Leverage guardrail — maximum gross debt ÷ EBITDA", 1.5, F_X2, "Team guardrail for an AA- issuer with volatile earnings: ≤ 1.5x gross debt/EBITDA."),
        ("a_ppa_on", "Charge purchase-price-allocation amortisation in the headline EPS? (1 = yes, 0 = no)", 0, F_YR, "0 = case basis (case §2: EPS impact from new shares and financing costs). 1 = Ind AS reported basis (amortisation of acquired intangibles). The reported-basis EPS is always shown as a separate line."),
        ("a_ppa_share", "Share of purchase price allocated to amortisable intangibles (technology, customer contracts)", 0.25, F_PCT, "Typical for software/infra targets: 20–35% to identifiable intangibles; the rest is goodwill (not amortised, tested for impairment)."),
        ("a_ppa_life", "Amortisation life of acquired intangibles (years)", 8, F_YR, "Technology 5–7 yrs, customer relationships 8–10 yrs → blended 8."),
        ("a_mdr_flow", "EBITDA flow-through of the ₹115 Cr MDR net revenue", 0.80, F_PCT, "Net revenue is after interchange/processing; some incremental collection, dispute and compliance cost → 80% reaches EBITDA. Tested 60–100%."),
        ("a_pat_growth", "Paytm standalone PAT growth p.a. (excluding MDR)", 0.0, F_PCT, "Held at 0% so that the deal's effect on EPS is isolated; the case gives no forecast. Flex to test."),
        ("a_wacc_base", "WACC / discount rate for Liminal cash flows (base)", 0.13, F_PCT, "Build-up: India 10-yr G-sec ~6.5% + β 1.0 × ERP 6.5% ≈ 13% for an all-equity infra business. Risk is placed in the cash flows (churn, drag, growth scenarios), not inflated in the rate. Tested 11–15%."),
        ("a_tg", "Terminal growth (p.a., nominal)", 0.05, F_PCT, "Below India nominal GDP growth; tested 3–6%."),
        ("a_recovery", "Share of cumulative trapped reserve capital recovered at the end of the horizon (drag reading B)", 0.0, F_PCT, "0% = the case's literal reading (a permanent FCF drag). 100% = reserves are released on exit/deregulation. Only relevant under reading B (see Capital_Drag)."),
        ("a_be_gate", "Breakeven gate: PAT and FCF must break even within N years of taking control", 5, F_YR, "Board gate used in the decision framework."),
    ]
    for nm, lab, val, fmt, cm in ta2:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    r += 1
    r = subheader(ws, r, "F. TEAM ASSUMPTIONS — alternative structures (minority, call option, JV, walk-away)", ncols=4)
    ta3 = [
        ("a_stake", "Minority stake (case range 20–30%)", 0.26, F_PCT, "26% = one share above the 25% special-resolution blocking threshold under the Companies Act 2013 (s.114): negative control without operational control."),
        ("a_min_val100", "Implied valuation of 100% at which the minority stake is bought (₹ Cr)", 2500, F_INR, "Entry valuation for the minority: ₹2,500 Cr = 11.4x ARR, i.e. Paytm's own EV/sales, the middle of the listed custody/infra comps range (5–11x) and the bull-case DCF pro-rata. Ceiling = ₹4,000 Cr headline (pro-rata ₹1,040 Cr); floor = base DCF (₹1,219 Cr)."),
        ("a_primary_share", "Share of the minority cheque that is primary (new shares into Liminal) vs secondary", 0.50, F_PCT, "Primary capital funds Liminal's growth and stays in the group; secondary gives sellers liquidity. 50/50 base."),
        ("a_min_churn", "ARR churn triggered by a ring-fenced minority stake (year 1)", 0.0, F_PCT, "Base 0% because no change of control occurs and contracts are unaffected; this is a GATE to be validated by client consents, not a belief. Flex 0–20%."),
        ("a_min_drag_mode", "Capital drag applied to Paytm at minority (0 = none, 1 = pro-rata to stake, 2 = full ₹ drag)", 0, F_YR, "Case ties the reserve to Paytm 'owning' the custody infrastructure. At a non-consolidated 26% we assume none, tested pro-rata and full. Written RBI comfort is a signing condition."),
        ("a_opt_year", "Year at end of which the call option is exercised (if gates pass)", 1, F_YR, "Validation period 12 months; option window months 12–24."),
        ("a_ctrl_churn", "ARR churn on exercising control (post-consent)", 0.20, F_PCT, "Control is only exercised if clients representing ≥ 80% of ARR have consented in writing; residual 20% churn assumed."),
        ("a_ctrl_mult", "Call-option strike multiple (× ARR at exercise) applied to the remaining stake, before the retention earn-out", 10, F_X, "10x = the listed custody leader's subscription multiple (BitGo 9–11x) and a premium to FI-infrastructure software (4–6x); below the 18.2x headline. Strike = remaining stake × multiple × ARR at exercise, capped at the headline-equivalent; paid as 55% upfront (worst-case retained ARR) + retention earn-out. Tested 8–14x."),
        ("a_ctrl_debt", "Control tranche: amount funded from new debt (₹ Cr); the rest of the upfront comes from cash", 500, F_INR, "≤ 1.5x gross debt/EBITDA."),
        ("a_eo_floor", "Retained-ARR level at which the earn-out is zero", 0.55, F_PCT, "The case's worst case (45% churn) → sellers receive nothing extra below 55% retention."),
        ("a_eo_full", "Retained-ARR level at which the earn-out is fully paid", 1.00, F_PCT, "100% retention → full headline."),
        ("a_eo_collar", "Collar on Paytm shares used to settle the earn-out (± band)", 0.15, F_PCT, "Protects both sides against stock moves between exercise and settlement."),
        ("a_ctrl_drag", "Capital drag on taking control (₹ Cr/yr) — gate value", 0, F_INR, "0 by construction of the gate: control is not exercised unless RBI treatment is written and the recurring cost is nil/structured away. Flex to test."),
        ("a_jv_paytm_share", "JV: Paytm economic share of the settlement JV", 0.60, F_PCT, "Paytm-majority 'SettleCo' for e₹/tokenised-treasury/cross-border settlement products."),
        ("a_jv_capital", "JV: Paytm capital contribution (₹ Cr)", 300, F_INR, "Working capital, licences, build."),
        ("a_jv_rev_y3", "JV: revenue in year 3 (₹ Cr)", 60, F_INR, "Illustrative: Paytm merchant/B2B settlement volumes on Liminal-licensed MPC; ramps from year 1."),
        ("a_jv_margin", "JV: mature EBITDA margin", 0.20, F_PCT, "Licence royalty to Liminal reduces margin vs owning the tech."),
        ("a_build_cost", "Walk-away: cost to build/partner an equivalent custody capability (₹ Cr, total)", 250, F_INR, "Team estimate: engineering, certifications (ISO 27001, SOC 2), licences, 24–36 months. Excludes the institutional franchise, which cannot be built."),
        ("a_build_years", "Walk-away: time to build/partner (years)", 3, F_YR, "24–36 months."),
    ]
    for nm, lab, val, fmt, cm in ta3:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    r += 1
    r = subheader(ws, r, "G. TEAM ASSUMPTIONS — synergies (base case = zero; upside quantified on 'Synergies')", ncols=4)
    ta4 = [
        ("a_syn_on", "Include synergies in the base case? (1 = yes, 0 = no)", 0, F_YR, "Base excludes synergies: none is proven, most are not ownership-dependent, and the MDR is a standalone Paytm item."),
        ("a_syn_partner_rev_y3", "Partnership revenue to Liminal from Paytm use cases by year 3 (₹ Cr)", 30, F_INR, "Custody/MPC fees on Paytm's tokenised-treasury, e₹ and cross-border pilots. Achievable under a commercial agreement WITHOUT ownership (not ownership-dependent)."),
        ("a_syn_xsell_y3", "Cross-sell revenue to Liminal from Paytm's merchant/institutional base by year 3 (₹ Cr)", 20, F_INR, "Ownership-dependent share only partly; requires the ring-fence not to be breached."),
        ("a_syn_cost", "Cost synergies (₹ Cr/yr) from year 2", 0, F_INR, "Deliberately zero: any shared-services integration breaches the information barrier that protects the franchise."),
        ("a_syn_ramp1", "Synergy ramp — share achieved in year 1", 0.25, F_PCT, ""),
        ("a_syn_ramp2", "Synergy ramp — share achieved in year 2", 0.60, F_PCT, ""),
    ]
    for nm, lab, val, fmt, cm in ta4:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm or None); text(ws, r, 4, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    return ws

def build_dashboard(b):
    ws = b.sheet("Dashboard", tab_color="C00000", widths={"A": 50, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 40})
    r = header(ws, 1, "DASHBOARD — key levers (yellow) and headline outputs (green). Change a lever; every sheet recalculates.", ncols=7)
    r = note(ws, r, "Levers are TEAM ASSUMPTIONS / scenario choices. Case facts live on 'Inputs' and are not levers.")
    r += 1
    r = subheader(ws, r, "1. SCENARIO LEVERS", ncols=7)
    lv = [
        ("lv_gcase", "Liminal growth case (1 = bear, 2 = base, 3 = bull)", 2, F_YR, "Selects a_g_bear / a_g_base / a_g_bull."),
        ("lv_churn", "ARR churn within 12 months of a FULL acquisition (case range 30–45%)", 0.375, F_PCT, "Case §3.1 range 30–45%; base = midpoint 37.5%. Set 0% to see the no-churn case."),
        ("lv_drag", "Recurring capital drag at full ownership (₹ Cr/yr) — case value 750; grid 500 / 750 / 1,000 / 1,250", 750, F_INR, "Case §3.2. Flex to test."),
        ("lv_drag_mode", "Capital drag reading (1 = fixed cash drag as the case states; 2 = scales with retained/growing custodied assets; 3 = P&L operating cost)", 1, F_YR, "See Capital_Drag for the three readings. Reading 1 is the case's literal wording."),
        ("lv_wacc", "Discount rate for Liminal cash flows", "=a_wacc_base", F_PCT, "Defaults to the Inputs base; overwrite to flex."),
        ("lv_mdr_in_deal", "Credit the ₹115 Cr MDR to the DEAL's breakeven? (0 = no: standalone Paytm item; 1 = yes: case-style offset)", 0, F_YR, "The MDR accrues to Paytm with or without Liminal. Both views are always shown; this lever picks which one the verdict lines use."),
    ]
    for nm, lab, val, fmt, cm in lv:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 7, cm, italic=True, color=GREY, wrap=True); b.name(nm, ws, f"B{r}"); r += 1
    label(ws, r, "→ Selected Liminal growth rate"); calc(ws, r, 2, "=CHOOSE(lv_gcase,a_g_bear,a_g_base,a_g_bull)", F_PCT, bold=True); b.name("lv_g", ws, f"B{r}"); r += 1
    r += 1
    r = subheader(ws, r, "2. FINANCING LEVERS — full acquisition (₹4,000 Cr headline; case: ₹2,100 Cr cash portion from cash, new debt or mix; ₹1,900 Cr in Paytm shares)", ncols=7)
    lv2 = [
        ("lv_mix_cash", "Cash consideration funded from balance-sheet cash (₹ Cr)", 2100, F_INR, "Case headline: ₹2,100 Cr from existing cash."),
        ("lv_mix_debt", "Cash consideration funded from new debt (₹ Cr)", 0, F_INR, "Case headline: none."),
        ("lv_mix_eq", "Consideration paid in new Paytm shares (₹ Cr)", 1900, F_INR, "Case headline: ₹1,900 Cr."),
    ]
    for nm, lab, val, fmt, cm in lv2:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 7, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    label(ws, r, "→ Total consideration from the mix (must equal the price paid)"); calc(ws, r, 2, "=lv_mix_cash+lv_mix_debt+lv_mix_eq", F_INR, bold=True); b.name("lv_mix_total", ws, f"B{r}"); r += 1
    label(ws, r, "Price paid for 100% (₹ Cr) — case headline 4,000; lower to test a renegotiated price"); inp(ws, r, 2, "=cf_deal", F_INR, kind="assump", comment="Defaults to the case headline; overwrite to test a lower negotiated price. The mix above must sum to this."); b.name("lv_price", ws, f"B{r}"); r += 1
    label(ws, r, "→ Check: mix = price (should read 0)"); calc(ws, r, 2, "=lv_mix_total-lv_price", F_INR, bold=True, fill=FILL_WARN); r += 1
    r += 1
    r = subheader(ws, r, "3. MINORITY / HYBRID LEVERS", ncols=7)
    lv3 = [
        ("lv_stake", "Minority stake", "=a_stake", F_PCT, "Defaults to Inputs (26%)."),
        ("lv_min_val100", "Implied 100% valuation for the minority entry (₹ Cr) — ceiling 4,000 (headline), floor = base DCF", "=a_min_val100", F_INR, "Defaults to Inputs (₹2,500 Cr = 11.4x ARR)."),
        ("lv_min_churn", "Churn triggered at minority", "=a_min_churn", F_PCT, "Defaults to Inputs (0%; a gate)."),
        ("lv_min_drag_mode", "Drag applied at minority (0 none / 1 pro-rata / 2 full)", "=a_min_drag_mode", F_YR, "Defaults to Inputs (0)."),
    ]
    for nm, lab, val, fmt, cm in lv3:
        label(ws, r, lab); inp(ws, r, 2, val, fmt, kind="assump", comment=cm); text(ws, r, 7, cm, italic=True, color=GREY); b.name(nm, ws, f"B{r}"); r += 1
    label(ws, r, "→ Minority price (₹ Cr) = stake × implied 100% valuation"); calc(ws, r, 2, "=lv_stake*lv_min_val100", F_INR, bold=True); b.name("lv_min_price", ws, f"B{r}"); r += 1
    label(ws, r, "→ Implied entry multiple (× ARR) / discount to the headline pro-rata"); calc(ws, r, 2, "=lv_min_val100/cf_arr", F_X); calc(ws, r, 3, "=1-lv_min_val100/lv_price", F_PCT); r += 1
    r += 1
    b.dash_outputs_row = r   # outputs are appended by part 6 once all sheets exist
    return ws
