"""Bottom-up market model: private-pay decentralised sanitation, Goa+MH+KA Tier 2/3.
All money in Rs crore unless noted. Formula per segment:
  eligible units x %lacking compliant treatment x solution-fit% x annual conversion% x avg ticket
Sources for anchors in research/*.md. Every derived number labelled estimate.
"""

def seg(name, units, lack, fit, conv, ticket_l, new_annual=0, new_fit=0.0, new_ticket_l=0.0, note=""):
    """units: stock count; lack/fit/conv: fractions; ticket_l: Rs lakh.
    new_annual: annual NEW construction units (flow), converted at new_fit."""
    stock_proj = units * lack * fit * conv
    flow_proj = new_annual * new_fit
    projects = stock_proj + flow_proj
    val_cr = (stock_proj * ticket_l + flow_proj * (new_ticket_l or ticket_l)) / 100.0
    return dict(name=name, projects=projects, val=val_cr, note=note)

# ---------------- STP/ETP opportunity (annual) ----------------
stp = []

# A. Hospitality. Stock: properties >=20 keys needing onsite treatment.
#   Goa ~9,000 registered accommodation units (DoT 2024) -> est 16% are >=20 keys ~ 1,450
#   MH Tier2/3 leisure clusters (Konkan, Kolhapur, Nashik, Mahabaleshwar, Sambhajinagar) est 1,150
#   KA Tier2/3 (Mysuru, Mangaluru, Coorg, Chikkamagaluru, Hampi, Hubballi) est 1,400
#   Lack compliant onsite STP: 55% (proxy: Goa 62.5% treatment gap, CPCB 2021; consent enforcement partial)
#   Fit (space/scale/willingness for 10-50 KLD FRP modular): 60%
#   Conversion 8%/yr (consent renewals + renovation cycle ~ stock converts over ~12 yrs)
#   New hotels: Tier2/3 = 74% of 2024 room signings (HVS); est 110 new mid-size properties/yr across 3 geos, 55% fit
stp.append(seg("Hospitality", 4000, 0.55, 0.60, 0.08, 28, new_annual=110, new_fit=0.55, new_ticket_l=32,
               note="avg 25 KLD @ ~Rs1.1L/KLD installed"))

# B. Residential developers (new build). Annual RERA-registered launches in Tier2/3:
#   MH ~4,500/yr statewide recent run-rate, Tier2/3 ~40% -> 1,800; above STP trigger (>=20k sqm EC / unsewered) 20% -> 360
#   KA (ex-Bengaluru) ~800/yr, Tier2/3 ~35% -> 280; above trigger (KSPCB unsewered rule) 40% -> 112
#   Goa ~150/yr; above trigger 30% -> 45
#   Decentralised fit (unsewered site, developer-procured): 60%
stp.append(seg("Residential developers", 0, 0, 0, 0, 0, new_annual=(360+112+45), new_fit=0.60, new_ticket_l=55,
               note="25-150 KLD design-build, avg 60 KLD"))

# C. Existing housing societies (retrofit/replacement of failed STP or septic)
#   Tier2 cities societies w/ STP >8yrs old or failing: est 900 across geos; 60% fit; 12% annual conversion
stp.append(seg("Housing societies (retrofit)", 900, 1.0, 0.60, 0.12, 18, note="rehab + upgrade jobs"))

# D. Private healthcare >10 beds (BMW Rules 2016: ETP mandatory)
#   Est 5,500 private HCFs >10 beds in MH+KA+Goa Tier2/3 (MH & KA private-bed heavy states)
#   Non-compliant onsite: 50%; fit 50%; conversion 6%/yr (enforcement + NABH)
stp.append(seg("Hospitals & healthcare", 5500, 0.50, 0.50, 0.06, 16, note="5-30 KLD ETP/STP skids"))

# E. Education & CSR-funded campuses (residential schools, colleges, ashrams, trusts)
#   Est 3,000 residential campuses; 55% lacking; 45% fit; 5%/yr conversion; avg Rs14L (bio-digester bank or small STP)
stp.append(seg("Education & CSR institutions", 3000, 0.55, 0.45, 0.05, 14, note="bio-digester banks + 5-20 KLD"))

# F. MSME industrial (compact ETP <= Rs1 cr; food/pharma/textile clusters)
#   Est 2,600 consented MSMEs in target clusters needing new/upgraded compact ETP; 45% lack; 40% fit; 7%/yr
stp.append(seg("MSME industrial (compact ETP)", 2600, 0.45, 0.40, 0.07, 40, note="excl. complex chemistry"))

# G. Commercial & mixed-use (offices, malls, wedding venues, highway hotels)
stp.append(seg("Commercial & mixed-use", 1200, 0.50, 0.50, 0.07, 35, note="20-75 KLD"))

# ---------------- Bio-digester toilets (annual) ----------------
bio = []
# H. Individual homes: new unsewered homes Tier2/3 3 states est 220k/yr; engineered onsite adoption 2.5%; ticket Rs0.55L
bio.append(seg("Individual homes (bio-digester)", 0, 0, 0, 0, 0, new_annual=220000, new_fit=0.025, new_ticket_l=0.55,
               note="vs mason septic; premium adopters"))
# I. Homestays/farm-stays/small resorts + event venues: 3,500 stock; 60% lack; 50% fit; 8%/yr; Rs2.2L
bio.append(seg("Homestays & small hospitality", 3500, 0.60, 0.50, 0.08, 2.2, note="700-15,000 L systems"))

TAM_stp = sum(s["val"] for s in stp)
TAM_bio = sum(s["val"] for s in bio)
TAM = TAM_stp + TAM_bio

print("=== ANNUAL TAM (3 states, private-pay, Tier2/3) ===")
for s in stp + bio:
    print(f"  {s['name']:34s} {s['projects']:7.0f} proj/yr  Rs {s['val']:6.1f} cr  ({s['note']})")
print(f"  STP/ETP subtotal Rs {TAM_stp:.1f} cr | Bio-digester subtotal Rs {TAM_bio:.1f} cr")
print(f"  TAM = Rs {TAM:.1f} cr/yr")

# ---------------- SAM ----------------
# Serviceable: priority personas (A,B,D) + retrofit (C) + institutions (E) + bio (H,I subset),
# within Phase1-3 corridor coverage (~65% of 3-state Tier2/3 demand by value), project size 5L-2.5cr (all),
# minus complex MSME chemistry (drop 100% of F) and half of commercial G.
corridor = 0.65
sam_parts = {
    "Hospitality": stp[0]["val"] * corridor,
    "Residential developers": stp[1]["val"] * corridor,
    "Housing societies (retrofit)": stp[2]["val"] * corridor,
    "Hospitals & healthcare": stp[3]["val"] * corridor,
    "Education & CSR institutions": stp[4]["val"] * corridor,
    "Commercial & mixed-use": stp[6]["val"] * corridor * 0.5,
    "Bio-digesters (homes+small hosp.)": (bio[0]["val"] + bio[1]["val"]) * corridor,
}
SAM = sum(sam_parts.values())
print("\n=== SAM (serviceable, annual) ===")
for k, v in sam_parts.items():
    print(f"  {k:34s} Rs {v:6.1f} cr")
print(f"  SAM = Rs {SAM:.1f} cr/yr  ({SAM/TAM*100:.0f}% of TAM)")

# ---------------- SOM: EPBL 3-year capture ----------------
# Base business (existing govt/institutional/retail) grows 5%/yr off FY26 Rs11.7 cr.
base = [11.7 * 1.05, 11.7 * 1.05**2, 11.7 * 1.05**3]
# New private-market revenue (base case), built from capacity+funnel:
# FY27: 12 STP proj x avg 30L = 3.6? -> keep conservative: 9 proj Goa corridor (2.7) + bio 0.5 + AMC 0.1 = 2.9? set 2.4
new = {
    "cons": [1.8, 4.6, 8.6],
    "base": [2.4, 6.4, 11.9],
    "up":   [3.2, 8.6, 15.8],
}
print("\n=== SOM scenarios (Rs cr) ===")
for k, v in new.items():
    tot = [b + n for b, n in zip(base, v)]
    print(f"  {k:5s} new: FY27 {v[0]:4.1f} FY28 {v[1]:4.1f} FY29 {v[2]:4.1f} | cum new {sum(v):5.1f} | "
          f"total rev: {tot[0]:4.1f} / {tot[1]:4.1f} / {tot[2]:4.1f} | cum total {sum(tot):5.1f}")
print(f"  base-case FY29 total = Rs {base[2]+new['base'][2]:.1f} cr = {(base[2]+new['base'][2])/11.7:.1f}x FY26; "
      f"FY29 new-biz share of SAM = {new['base'][2]/SAM*100:.1f}%")

# Capacity check (base case FY29): new Rs11.9 cr =
#  ~26 STP/ETP projects avg 32L = 8.3 + retrofits 8 x 12L = 1.0 + bio-digesters ~230 units avg 0.8L = 1.8 + AMC/monitoring 0.8
chk = 26*32/100 + 8*12/100 + 230*0.8/100 + 0.8
print(f"\n  FY29 new-biz capacity check: 26 STP + 8 retrofit + 230 bio units + AMC = Rs {chk:.1f} cr")
# Crews: STP install 3-4 wks/crew -> 26+8=34 jobs needs ~3.5 crew-years -> 3 own + 2 partner crews OK.
# WC check: FY29 total rev 25.4, DSO 75 -> receivables 25.4*75/365 = 5.2 cr vs net worth >12 + milestone billing OK.
print(f"  WC check: FY29 receivables @75 DSO = Rs {(base[2]+new['base'][2])*75/365:.1f} cr vs net worth > Rs 12 cr")

# Funnel FY27 (base): audits 320 -> qualified 130 (Rs 32 cr pipeline) -> proposals 55 -> wins 22 (40% of proposals)
# wins value: 12 STP x 28L=3.4? Let's detail: new Rs2.4 = 8 STP x 22L avg (1.76) + 60 bio x 0.7 (0.42) + retrofits 2 x 10L (0.2)
print("\n  FY27 new-biz mix: 8 STP x Rs22L + 2 retrofit x Rs10L + ~60 bio-digesters + AMC = Rs",
      f"{8*22/100 + 2*10/100 + 60*0.7/100 + 0.06:.2f} cr")
