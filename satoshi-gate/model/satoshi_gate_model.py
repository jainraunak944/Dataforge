"""
Project Satoshi Gate - simple accretion/dilution + transaction model.
All CASE FACTS are taken verbatim from the case document. Everything under
TEAM ASSUMPTIONS is a disclosed team assumption (per the Modeling Clarification).
Run:  python3 satoshi_gate_model.py   -> prints every table used in the deck.
"""
from math import log

# ----------------------------- CASE FACTS ---------------------------------
PAT0, SH0, EPS0 = 480.0, 64.0, 7.50           # Rs Cr, Cr shares, Rs/share
CASH0, DEBT0, EBITDA0, REV0 = 8900.0, 350.0, 640.0, 8450.0
MCAP = 118750.0
DEAL, DEAL_CASH, DEAL_EQ = 4000.0, 2100.0, 1900.0
ARR0, LIM_PAT0 = 220.0, 0.0
CHURN_LO, CHURN_HI = 0.30, 0.45               # full-acquisition ARR loss within 12m
DRAG = 750.0                                  # recurring annual FCF drag at full ownership
MDR = 115.0                                   # incremental net revenue, Paytm standalone
TOP4 = 0.60                                   # share of ARR from HDFC, Axis, CoinDCX, ZebPay

# --------------------------- TEAM ASSUMPTIONS -----------------------------
STAKE = 0.26                                  # negative-control stake (one share > 25%)
P1_PRICE = STAKE * DEAL                       # pro-rata to headline = 1,040 (ceiling)
YIELD = 0.06                                  # pre-tax yield on Paytm surplus cash
KD = 0.085                                    # pre-tax cost of new debt (CRISIL AA- issuer)
TAX = 0.25
G_BEAR, G_BASE, G_BULL = 0.10, 0.20, 0.30     # Liminal ARR growth
MARGIN_STEP, MARGIN_CAP = 0.05, 0.25          # EBITDA margin ramps 5pp/yr to 25%
PAT_CONV = 0.75                               # PAT = 75% of EBITDA (tax; D&A ~ capex)
FCF_EQ_PAT = True                             # asset-light: FCF ~ PAT
CHURN_BASE = 0.375                            # midpoint of case range, applied at control
STICKY = 0.50                                 # 50% of lost revenue's cost base sticky for 1 yr
MDR_FLOW = 0.80                               # EBITDA flow-through of MDR net revenue
MDR_PAT = MDR * MDR_FLOW * (1 - TAX)          # = 69
INTEG_CONTROL, P1_FEES = 100.0, 15.0          # one-time
WACC, TG = 0.12, 0.05
PRICE = MCAP / SH0                            # implied share price
MAX_GROSS_LEV, MIN_CASH = 1.5, 5000.0         # rating / liquidity guardrails
# Control tranche (74%) = 2,960 headline-equivalent, split upfront + retention earn-out
CTRL_TOTAL = DEAL - P1_PRICE                  # 2,960
CTRL_UPFRONT = 1650.0                         # ~74% x worst-case value (45% churn)
CTRL_EARNOUT = CTRL_TOTAL - CTRL_UPFRONT      # 1,310, linear between 55% and 100% retention
EO_FLOOR, EO_FULL = 0.55, 1.00
CTRL_CASH, CTRL_DEBT = 1150.0, 500.0          # funding of the upfront control tranche
CTRL_YEAR = 1                                 # exercise at end of Y1

def post_tax_cash_cost(x): return x * YIELD * (1 - TAX)
def post_tax_debt_cost(x): return x * KD * (1 - TAX)

def liminal_path(g, churn=0.0, churn_year=None, years=10):
    """Returns list of dicts per year 1..years: rev, ebitda, pat (Rs Cr)."""
    out = []
    for t in range(1, years + 1):
        rev_nc = ARR0 * (1 + g) ** t
        m = min(MARGIN_STEP * t, MARGIN_CAP)
        if churn_year is not None and t >= churn_year:
            rev = rev_nc * (1 - churn)
            ebitda = rev * m
            if t == churn_year:
                ebitda -= STICKY * (rev_nc - rev)     # one-year sticky cost penalty
        else:
            rev, ebitda = rev_nc, rev_nc * m
        pat = ebitda * PAT_CONV if ebitda > 0 else ebitda   # no group relief on losses
        out.append(dict(t=t, rev=rev, ebitda=ebitda, pat=pat, fcf=pat))
    return out

def dcf(g, years=10, wacc=WACC, tg=TG):
    p = liminal_path(g, years=years)
    pv = sum(y['fcf'] / (1 + wacc) ** y['t'] for y in p)
    tv = p[-1]['fcf'] * (1 + tg) / (wacc - tg)
    return pv + tv / (1 + wacc) ** years

def solve_growth(target):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if dcf(mid) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def fmt(x, d=1): return f"{x:,.{d}f}"

print("=" * 78)
print("A. CHURN SENSITIVITY (case facts + arithmetic)")
print("=" * 78)
hm = DEAL / ARR0
print(f"Headline multiple: {DEAL:,.0f} / {ARR0:,.0f} = {hm:.2f}x (case rounds to 18x)")
print(f"{'churn':>7} {'ARR lost':>9} {'retained':>9} {'eff. mult':>10} {'value@18.2x':>12} {'gap':>8} {'recovery growth':>16}")
for c in (0.0, 0.30, 0.375, 0.45):
    lost = ARR0 * c; ret = ARR0 - lost
    print(f"{c*100:>6.1f}% {lost:>9.1f} {ret:>9.1f} {DEAL/ret:>9.1f}x {hm*ret:>12,.0f} {DEAL-hm*ret:>8,.0f} {(ARR0/ret-1)*100:>15.1f}%")
print(f"Top-4 ARR = {ARR0*TOP4:.0f}; case churn {ARR0*CHURN_LO:.0f}-{ARR0*CHURN_HI:.0f} = {CHURN_LO/TOP4*100:.0f}-{CHURN_HI/TOP4*100:.0f}% of top-4 ARR")
print(f"Value destroyed per 10pts of churn at 18.2x: {hm*ARR0*0.10:,.0f} Cr")

print("\n" + "=" * 78)
print("B. THE CAPITAL DRAG IN CONTEXT")
print("=" * 78)
print(f"Drag {DRAG:.0f} vs Paytm EBITDA {EBITDA0:.0f} = {DRAG/EBITDA0*100:.0f}% ; vs PAT {PAT0:.0f} = {DRAG/PAT0*100:.0f}%")
print(f"Drag vs Liminal ARR {ARR0:.0f} = {DRAG/ARR0*100:.0f}% of Liminal's entire revenue")
ann10 = DRAG * (1 - (1 + WACC) ** -10) / WACC
print(f"NPV of drag @ {WACC*100:.0f}%: 10-yr annuity = {ann10:,.0f} Cr ; perpetuity = {DRAG/WACC:,.0f} Cr  (deal value {DEAL:,.0f})")
fcf_margin = MARGIN_CAP * PAT_CONV
need = DRAG / fcf_margin
print(f"Liminal FCF needed to cover drag alone = {DRAG:.0f}; at {fcf_margin*100:.2f}% FCF margin -> ARR {need:,.0f} Cr = {need/ARR0:.1f}x today's ARR")
for g in (G_BASE, G_BULL, 0.40):
    yrs = log(need / ARR0) / log(1 + g)
    print(f"  years to reach {need:,.0f} ARR at {g*100:.0f}% growth from 220 (zero churn): {yrs:.1f}")
print(f"MDR offset: {MDR:.0f}/{DRAG:.0f} = {MDR/DRAG*100:.1f}% gross ; at PAT/FCF conversion {MDR_FLOW*(1-TAX)*100:.0f}% -> {MDR_PAT:.0f} Cr = {MDR_PAT/DRAG*100:.1f}% of drag")
print(f"Net cash cost of full ownership after MDR: {DRAG-MDR_PAT:.0f} Cr/yr")

print("\n" + "=" * 78)
print("C. LIMINAL STANDALONE PROJECTIONS (team assumptions; no churn)")
print("=" * 78)
for g in (G_BEAR, G_BASE, G_BULL):
    p = liminal_path(g)
    print(f"growth {g*100:.0f}%: " + " | ".join(f"Y{y['t']} rev {y['rev']:.0f} PAT {y['pat']:.0f}" for y in p[:6]) + f" | Y10 rev {p[-1]['rev']:.0f} PAT {p[-1]['pat']:.0f}")

print("\n" + "=" * 78)
print("D. WHAT YOU NEED TO BELIEVE - standalone DCF vs 4,000 headline (WACC 12%, TG 5%)")
print("=" * 78)
for g in (0.10, 0.20, 0.30, 0.40, 0.50):
    v = dcf(g)
    print(f"  growth {g*100:>3.0f}% for 10 yrs, margin -> 25%: DCF = {v:>7,.0f} Cr  ({v/ARR0:.1f}x ARR)  vs 4,000 -> {'supported' if v>=DEAL else 'NOT supported'}")
g_req = solve_growth(DEAL)
print(f"  Growth required for DCF = 4,000: {g_req*100:.1f}% p.a. for 10 years, zero churn, no capital drag")
for w in (0.11, 0.12, 0.14):
    print(f"  WACC {w*100:.0f}%: base DCF = {dcf(G_BASE, wacc=w):,.0f}; bull DCF = {dcf(G_BULL, wacc=w):,.0f}")

print("\n" + "=" * 78)
print("E. FULL-ACQUISITION YEAR-1 EPS UNDER FINANCING MIXES (churn 37.5% base)")
print("=" * 78)
lim_y1 = liminal_path(G_BASE, churn=CHURN_BASE, churn_year=1)[0]
print(f"Liminal Y1 after {CHURN_BASE*100:.1f}% churn: rev {lim_y1['rev']:.1f}, EBITDA {lim_y1['ebitda']:.1f}, PAT {lim_y1['pat']:.1f} (sticky costs)")
mixes = [
    ("Case headline: 2,100 cash (B/S) + 1,900 equity", 2100, 0, 1900),
    ("2,100 new debt + 1,900 equity",                    0, 2100, 1900),
    ("Mix: 1,400 cash + 700 debt + 1,900 equity",     1400, 700, 1900),
    ("All cash 4,000",                                 4000, 0, 0),
    ("All equity 4,000",                                  0, 0, 4000),
]
print(f"{'structure':<48}{'shares':>8}{'PAT':>8}{'EPS':>7}{'vs 7.50':>9}{'EPS+MDR':>9}{'cash':>8}{'gross debt':>11}{'GD/EBITDA':>10}{'mech-only EPS':>14}")
for name, cash, debt, eq in mixes:
    sh = SH0 + eq / PRICE
    pat = PAT0 - post_tax_cash_cost(cash) - post_tax_debt_cost(debt) + lim_y1['pat']
    eps = pat / sh
    mech = PAT0 / sh
    print(f"{name:<48}{sh:>8.2f}{pat:>8.0f}{eps:>7.2f}{(eps/EPS0-1)*100:>8.1f}%{(pat+MDR_PAT)/sh:>9.2f}{CASH0-cash:>8,.0f}{DEBT0+debt:>11,.0f}{(DEBT0+debt)/EBITDA0:>9.1f}x{mech:>14.2f}")
print(f"Implied share price {PRICE:,.0f}; 1,900 Cr equity = {DEAL_EQ/PRICE:.3f} Cr shares; trailing P/E = {MCAP/PAT0:.0f}x (earnings yield {PAT0/MCAP*100:.2f}%)")
print(f"At 25% lower share price ({PRICE*0.75:,.0f}): 1,900 Cr equity = {DEAL_EQ/(PRICE*0.75):.2f} Cr shares")
# churn sensitivity of headline-mix EPS
print("Headline-mix Y1 EPS by churn: " + ", ".join(f"{c*100:.0f}%: {(PAT0 - post_tax_cash_cost(2100) + liminal_path(G_BASE, churn=c, churn_year=1)[0]['pat'])/(SH0+DEAL_EQ/PRICE):.2f}" for c in (0, 0.30, 0.375, 0.45)))

print("\n" + "=" * 78)
print("F. FULL ACQUISITION (headline mix) 10-YEAR PAT & FCF BREAKEVEN, churn 37.5%, growth 20%")
print("=" * 78)
sh_full = SH0 + DEAL_EQ / PRICE
cof_full = post_tax_cash_cost(DEAL_CASH)
print(f"Cost of funds (foregone interest on 2,100): {cof_full:.1f}/yr ; shares {sh_full:.2f}")
print(f"{'Yr':>3}{'Lim rev':>9}{'Lim PAT':>9}{'incr PAT':>10}{'EPS':>7}{'EPS+MDR':>9}{'incr FCF':>10}{'incrFCF+MDR':>12}{'cum FCF':>10}")
cum = -DEAL_CASH
be_pat = be_fcf = be_pat_mdr = be_fcf_mdr = None
for y in liminal_path(G_BASE, churn=CHURN_BASE, churn_year=1):
    ipat = y['pat'] - cof_full
    ifcf = y['fcf'] - cof_full - DRAG - (INTEG_CONTROL if y['t'] == 1 else 0)
    cum += ifcf
    if be_pat is None and ipat >= 0: be_pat = y['t']
    if be_fcf is None and ifcf >= 0: be_fcf = y['t']
    if be_pat_mdr is None and ipat + MDR_PAT >= 0: be_pat_mdr = y['t']
    if be_fcf_mdr is None and ifcf + MDR_PAT >= 0: be_fcf_mdr = y['t']
    print(f"{y['t']:>3}{y['rev']:>9.0f}{y['pat']:>9.0f}{ipat:>10.0f}{(PAT0+ipat)/sh_full:>7.2f}{(PAT0+ipat+MDR_PAT)/sh_full:>9.2f}{ifcf:>10.0f}{ifcf+MDR_PAT:>12.0f}{cum:>10.0f}")
print(f"PAT breakeven year: {be_pat or '>10'} (with MDR credited: {be_pat_mdr or '>10'}) ; FCF breakeven year: {be_fcf or '>10'} (with MDR: {be_fcf_mdr or '>10'})")
# zero churn, bull growth, still with drag
be = None
for y in liminal_path(G_BULL):
    if y['fcf'] - cof_full - DRAG + MDR_PAT >= 0: be = y['t']; break
print(f"Even at 0% churn, 30% growth, MDR credited: FCF breakeven year = {be or '>10'}")

print("\n" + "=" * 78)
print("G. PHASE 1: 26% MINORITY FOR 1,040 CASH (no churn, no drag - validation gates)")
print("=" * 78)
cof_p1 = post_tax_cash_cost(P1_PRICE)
print(f"Foregone post-tax treasury income: {cof_p1:.1f}/yr ; Phase-1 fees {P1_FEES:.0f} one-time ; cash after {CASH0-P1_PRICE:,.0f}")
print(f"Standalone EPS with MDR: {(PAT0+MDR_PAT)/SH0:.2f}")
for g in (G_BEAR, G_BASE, G_BULL):
    p = liminal_path(g)
    row = []
    be = None
    for y in p:
        assoc = STAKE * y['pat']
        eps = (PAT0 + assoc - cof_p1) / SH0
        if be is None and assoc >= cof_p1: be = y['t']
        row.append(f"Y{y['t']} {eps:.2f}")
    print(f"growth {g*100:.0f}%: EPS " + " ".join(row[:5]) + f" ... associate income covers foregone interest in year {be or '>10'}")
y1 = liminal_path(G_BASE)[0]
eps_p1 = (PAT0 + STAKE * y1['pat'] - cof_p1) / SH0
print(f"Base Y1 EPS {eps_p1:.2f} ({(eps_p1/EPS0-1)*100:.1f}% vs 7.50); with MDR {(PAT0+MDR_PAT+STAKE*y1['pat']-cof_p1)/SH0:.2f} ({((PAT0+MDR_PAT+STAKE*y1['pat']-cof_p1)/(PAT0+MDR_PAT)-1)*100:.1f}% vs 8.58 like-for-like)")
for yld in (0.05, 0.06, 0.07):
    print(f"  yield sensitivity {yld*100:.0f}%: Y1 EPS {(PAT0 + STAKE*y1['pat'] - P1_PRICE*yld*(1-TAX))/SH0:.2f}")
print(f"If RBI applied the drag pro-rata at 26%: {STAKE*DRAG:.0f} Cr/yr FCF -> Phase-1 cash cost {cof_p1+STAKE*DRAG:.0f}/yr ; full drag {DRAG:.0f} -> structure fails")
print(f"Share-funded alternative: {P1_PRICE/PRICE:.2f} Cr new shares -> EPS {(PAT0+STAKE*y1['pat'])/(SH0+P1_PRICE/PRICE):.2f}")
# Phase-1 IRR grid
print("Phase-1 stake IRR (exit end-Y5 at multiple x ARR5, 26% stake, no dividends):")
print(f"{'growth / exit':>12}" + "".join(f"{m:>8.0f}x" for m in (6, 10, 14, 18.2)))
for g in (G_BEAR, G_BASE, G_BULL):
    arr5 = ARR0 * (1 + g) ** 5
    print(f"{g*100:>11.0f}%" + "".join(f"{((STAKE*m*arr5/P1_PRICE)**(1/5)-1)*100:>8.1f}%" for m in (6, 10, 14, 18.2)))

print("\n" + "=" * 78)
print("H. CONTROL TRANCHE: RETENTION-LINKED EARN-OUT")
print("=" * 78)
print(f"Total control consideration cap {CTRL_TOTAL:,.0f} = {CTRL_UPFRONT:,.0f} upfront + up to {CTRL_EARNOUT:,.0f} earn-out (linear {EO_FLOOR*100:.0f}%-{EO_FULL*100:.0f}% retention)")
print(f"{'churn':>6}{'retention':>10}{'earn-out':>10}{'control total':>14}{'grand total':>12}{'74% of 18.2x value':>20}")
for c in (0.0, 0.10, 0.20, 0.30, 0.375, 0.45, 0.55):
    r = 1 - c
    eo = CTRL_EARNOUT * min(max((r - EO_FLOOR) / (EO_FULL - EO_FLOOR), 0), 1)
    print(f"{c*100:>5.1f}%{r*100:>9.0f}%{eo:>10,.0f}{CTRL_UPFRONT+eo:>14,.0f}{P1_PRICE+CTRL_UPFRONT+eo:>12,.0f}{(1-STAKE)*hm*ARR0*r:>20,.0f}")
print(f"Earn-out in Paytm shares at current price: up to {CTRL_EARNOUT/PRICE:.2f} Cr shares ({CTRL_EARNOUT/PRICE/SH0*100:.1f}% of share count)")

print("\n" + "=" * 78)
print("I. PHASE 3 CONTROL EXERCISE AT END-Y1 (gates pass): consolidated EPS/FCF, growth 20%")
print("=" * 78)
cof_ctrl = cof_p1 + post_tax_cash_cost(CTRL_CASH) + post_tax_debt_cost(CTRL_DEBT)
print(f"Cost of funds after control: P1 {cof_p1:.1f} + cash {post_tax_cash_cost(CTRL_CASH):.1f} + debt {post_tax_debt_cost(CTRL_DEBT):.1f} = {cof_ctrl:.1f}/yr")
print(f"Balance sheet post-control: cash {CASH0-P1_PRICE-CTRL_CASH:,.0f} ; gross debt {DEBT0+CTRL_DEBT:,.0f} ({(DEBT0+CTRL_DEBT)/EBITDA0:.2f}x EBITDA) ; guardrails: cash >= {MIN_CASH:,.0f}, GD/EBITDA <= {MAX_GROSS_LEV}x")
for c, drag in ((0.0, 0.0), (0.20, 0.0), (0.20, 100.0), (0.30, 0.0), (0.20, DRAG)):
    r = 1 - c
    eo = CTRL_EARNOUT * min(max((r - EO_FLOOR) / (EO_FULL - EO_FLOOR), 0), 1)
    sh = SH0 + eo / PRICE
    be_p = be_f = None
    eps_rows = []
    for y in liminal_path(G_BASE, churn=c, churn_year=CTRL_YEAR + 1):
        if y['t'] <= CTRL_YEAR:
            ipat = STAKE * y['pat'] - cof_p1
            ifcf = -cof_p1
            s = SH0
        else:
            ipat = y['pat'] - cof_ctrl
            ifcf = y['fcf'] - cof_ctrl - drag - (INTEG_CONTROL if y['t'] == CTRL_YEAR + 1 else 0)
            s = sh
        if be_p is None and ipat >= 0: be_p = y['t']
        if be_f is None and ifcf >= 0: be_f = y['t']
        eps_rows.append(f"Y{y['t']} {(PAT0+ipat)/s:.2f}")
    print(f"churn {c*100:>4.0f}%, drag {drag:>3.0f}: earn-out {eo:,.0f}, shares {sh:.2f} | EPS " + " ".join(eps_rows[:6]) + f" | PAT b/e Y{be_p or '>10'} ; FCF b/e Y{be_f or '>10'}")

print("\n" + "=" * 78)
print("J. LIQUIDITY & RATING GUARDRAILS BY STRUCTURE")
print("=" * 78)
for name, cash, debt in (("Phase 1 only", P1_PRICE, 0), ("Phase 1 + control upfront", P1_PRICE + CTRL_CASH, CTRL_DEBT), ("Full acquisition headline (cash from B/S)", DEAL_CASH, 0), ("Full acquisition, cash portion all debt", 0, DEAL_CASH)):
    c_after = CASH0 - cash; gd = DEBT0 + debt
    print(f"{name:<44} cash {c_after:>6,.0f} | gross debt {gd:>5,.0f} | GD/EBITDA {gd/EBITDA0:>4.1f}x | net cash {c_after-gd:>6,.0f} | yrs of drag funding above {MIN_CASH:,.0f} floor: {(c_after-MIN_CASH)/DRAG:>4.1f}")

print("\n" + "=" * 78)
print("K. CONTROL GATE CHECK: base (20%) vs bull (30%) growth, exercise end-Y1, no drag")
print("=" * 78)
print(f"Signal at month 12: ARR >= {ARR0*(1+G_BULL):.0f} Cr (30% growth) = bull ; ARR ~{ARR0*(1+G_BASE):.0f} Cr (20%) = base")
for label, g in (("base 20%", G_BASE), ("bull 30%", G_BULL)):
    for c in (0.0, 0.20):
        r = 1 - c
        eo = CTRL_EARNOUT * min(max((r - EO_FLOOR) / (EO_FULL - EO_FLOOR), 0), 1)
        sh = SH0 + eo / PRICE
        be_p = be_f = None
        rows = []
        for y in liminal_path(g, churn=c, churn_year=CTRL_YEAR + 1):
            if y['t'] <= CTRL_YEAR:
                ipat, ifcf, s = STAKE * y['pat'] - cof_p1, -cof_p1, SH0
            else:
                ipat = y['pat'] - cof_ctrl
                ifcf = y['fcf'] - cof_ctrl - (INTEG_CONTROL if y['t'] == CTRL_YEAR + 1 else 0)
                s = sh
            if be_p is None and ipat >= 0: be_p = y['t']
            if be_f is None and ifcf >= 0: be_f = y['t']
            rows.append(f"Y{y['t']} {(PAT0+ipat)/s:.2f}")
        yrs_after = (be_p - CTRL_YEAR) if be_p else None
        verdict = "EXERCISE (b/e <= 5 yrs after exercise)" if yrs_after and yrs_after <= 5 else "HOLD (b/e > 5 yrs after exercise)"
        print(f"{label}, churn {c*100:>3.0f}%: EPS " + " ".join(rows[:7]) + f" | PAT b/e Y{be_p or '>10'} FCF b/e Y{be_f or '>10'} -> {verdict}")

print("\n" + "=" * 78)
print("L. LIMINAL BASE-CASE P&L (team assumptions; appendix table)")
print("=" * 78)
print(f"{'Yr':>3}{'ARR/rev':>9}{'EBITDA m':>10}{'EBITDA':>8}{'PAT':>7}{'26% share':>11}{'foregone int':>14}{'net EPS effect':>15}")
print(f"{0:>3}{ARR0:>9.0f}{0:>9.0f}%{0:>8.0f}{0:>7.0f}{0:>11.1f}{0:>14.1f}{0:>15.2f}")
for y in liminal_path(G_BASE)[:6]:
    m = min(MARGIN_STEP * y['t'], MARGIN_CAP)
    print(f"{y['t']:>3}{y['rev']:>9.0f}{m*100:>9.0f}%{y['ebitda']:>8.0f}{y['pat']:>7.0f}{STAKE*y['pat']:>11.1f}{cof_p1:>14.1f}{(STAKE*y['pat']-cof_p1)/SH0:>15.2f}")

print("\n" + "=" * 78)
print("M. FULL-ACQUISITION Y1 EPS, ALL MIXES, AT 0% CHURN (best case for full deal)")
print("=" * 78)
lim0 = liminal_path(G_BASE)[0]
for name, cash, debt, eq in mixes:
    sh = SH0 + eq / PRICE
    pat = PAT0 - post_tax_cash_cost(cash) - post_tax_debt_cost(debt) + lim0['pat']
    print(f"{name:<48} EPS {pat/sh:.2f} ({(pat/sh/EPS0-1)*100:+.1f}%)")

print("\n" + "=" * 78)
print("N. DOWNSIDE MATRIX -> RECOMMENDATION (churn consents x capital treatment)")
print("=" * 78)
cap_levels = [("none / structured away", 0.0), ("pro-rata at 26% (195)", STAKE * DRAG), ("full 750 at any ownership", DRAG)]
churn_levels = [("<=20%", 0.20), ("20-45%", 0.375), (">45%", 0.55)]
for cl, c in churn_levels:
    for kl, d in cap_levels:
        if d >= DRAG: rec = "Do not exercise; hold 26% only if minority is drag-free, else restructure to JV/licence or exit"
        elif d > 0: rec = "Do not exercise; hold minority only if Phase-1 cash cost acceptable; pursue JV/licence"
        elif c <= 0.20: rec = "Eligible to exercise if bull trajectory (b/e <= 4 yrs) and valuation cap hold"
        elif c <= 0.45: rec = "Hold minority; earn-out floor protects; re-test at month 24"
        else: rec = "No control; activate remediation; consider exit via ROFO/tag"
        print(f"churn {cl:<7} | capital {kl:<28} -> {rec}")

print("\n" + "=" * 78)
print("O. WHAT PAYTM PAYS FOR IN PHASE 1: fundamental value of 26% vs 1,040 ceiling")
print("=" * 78)
for label, g in (("base 20%", G_BASE), ("bull 30%", G_BULL)):
    v = dcf(g)
    print(f"{label}: standalone DCF {v:,.0f} -> 26% = {STAKE*v:,.0f} Cr ; premium in 1,040 ceiling = {P1_PRICE-STAKE*v:,.0f} Cr")
v_ex = dcf(G_BULL) * (1 + G_BULL)   # DCF scales with ARR; one year of bull growth
print(f"DCF at end-Y1 if bull delivered (ARR {ARR0*(1+G_BULL):.0f}): {v_ex:,.0f} Cr -> 4,000 total cap is {(1-DEAL/v_ex)*100:.0f}% below it")
print(f"Phase-1 cheque as % of market cap: {P1_PRICE/MCAP*100:.2f}% ; of cash: {P1_PRICE/CASH0*100:.0f}%")

print("\n" + "=" * 78)
print("P. RECURRING CAPITAL COST AT CONTROL: does a 100 Cr/yr cost pass the 5-year gate?")
print("=" * 78)
for label, g in (("base 20%", G_BASE), ("bull 30%", G_BULL)):
    for c in (0.0, 0.20):
        for d in (0.0, 50.0, 100.0):
            be_f = None
            for y in liminal_path(g, churn=c, churn_year=CTRL_YEAR + 1):
                if y['t'] <= CTRL_YEAR: continue
                ifcf = y['fcf'] - cof_ctrl - d - (INTEG_CONTROL if y['t'] == CTRL_YEAR + 1 else 0)
                if ifcf >= 0: be_f = y['t']; break
            ok = be_f is not None and be_f - CTRL_YEAR <= 5
            print(f"{label}, churn {c*100:>3.0f}%, recurring cost {d:>3.0f}: FCF b/e Y{be_f or '>10'} -> {'PASS' if ok else 'FAIL'} 5-yr gate")

print("\n" + "=" * 78)
print("Q. SOURCES & USES")
print("=" * 78)
print(f"Phase 1  | Uses: 26% secondary {P1_PRICE:,.0f} + fees {P1_FEES:.0f} = {P1_PRICE+P1_FEES:,.0f} | Sources: balance-sheet cash {P1_PRICE+P1_FEES:,.0f} (debt 0, equity 0)")
print(f"Control  | Uses: upfront {CTRL_UPFRONT:,.0f} + integration {INTEG_CONTROL:.0f} + earn-out <= {CTRL_EARNOUT:,.0f} | Sources: cash {CTRL_CASH+INTEG_CONTROL:,.0f} + new debt {CTRL_DEBT:,.0f} + Paytm shares <= {CTRL_EARNOUT:,.0f} ({CTRL_EARNOUT/PRICE:.2f} Cr shares)")
print(f"Maximum total consideration {P1_PRICE+CTRL_TOTAL:,.0f} = headline; maximum unconditional {P1_PRICE:,.0f}")
