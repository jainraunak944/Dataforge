# NAADI — Calculation sheet (formulas, units, assumptions)

Companion to `NAADI_pilot_economics.xlsx` (live formulas) and
`../model/train_fault_model.py` (prototype metrics). DRAFT — every estimate
below requires team ratification before submission. Currency: INR lakh (L).

## 1. Prototype model metrics (computed, reproducible)

Run: `python3 ../model/train_fault_model.py` (CWRU 12 kHz drive-end + normal
baseline; 64 recordings → 4,367 windows of 2,048 samples; 16 interpretable
features/window).

| Metric | Value | Evaluation protocol |
|---|---|---|
| 4-class accuracy | 97.9% | Train 0/1/2 hp recordings, test **unseen 3 hp** load |
| Macro precision / recall | 97.7% / 97.6% | same |
| Fault-vs-normal precision / recall | 100% / 100% | same (benchmark conditions) |
| Normal windows misflagged | 0 of 237 | same |
| 4-class accuracy (grouped 5-fold CV by recording) | 98.9% | no recording crosses train/test |
| Logistic-regression baseline | 97.2% | unseen 3 hp load |

Errors are only between fault types (21 inner-race windows → ball), never
fault→normal. Caveat stated on the slide: clean test rig, seeded faults;
plant performance will be lower — the pilot exists to measure it.

## 2. Value of lost production

```
lakh_per_hour = revenue × contribution_margin / operating_hours
             = 50,000 L × 0.30 / 8,000 h = 1.875 L/h   (≈ ₹1.9 lakh/h)
```
All three inputs are TEAM ESTIMATES for a representative mid-size speciality
chemicals plant (₹500 Cr revenue, 30% contribution, 8,000 h/yr).

## 3. Annual benefit

```
avoided_downtime  = 60 h/yr × 35%            = 21 h/yr
downtime_value    = 21 h × 1.875 L/h         = 39.4 L
repair_saving     = 12 events × 2.5 L × 10%  =  3.0 L
catastrophic_avoid= 2 events × 2.5 L         =  5.0 L
total_benefit                                = 47.4 L/yr
```
- 60 h/yr baseline downtime on 25 bad-actor pumps: ESTIMATE (3–4 trips/yr,
  multi-hour restarts). Replaced by plant's real 24-month history in Phase 0.
- 35% and 10% effectiveness: SOURCED, low/mid of US DOE FEMP ranges
  (35–45% downtime reduction; 8–12% saving of PdM over preventive alone),
  O&M Best Practices Guide R3.0, 2010.

## 4. Costs

```
CapEx: 50 points × 0.35 L  = 17.5 L   (sensors, Ex-rated, installed — estimate)
       5 gateways × 1.5 L  =  7.5 L
       integration          = 10.0 L
       training             =  2.0 L
       total                = 37.0 L
OpEx = 6 L/yr (connectivity, compute, batteries ~10%/yr, model upkeep)
```

## 5. Returns

```
net_annual   = 47.4 − 6      = 41.4 L/yr
payback      = 37 / 41.4 ×12 = 10.7 months  (deck: "~11 months")
NPV(5y, 12%) = −37 + 41.4 × 3.6048 = 112 L ≈ ₹1.1 Cr
cost per avoided downtime-hour = (37/5 + 6)/21 = 0.64 L/h  vs value 1.875 L/h
```

## 6. Sensitivity (single-variable, payback in months)

| Scenario | Payback |
|---|---|
| Base | 10.7 |
| Downtime reduction only 20% (below DOE band) | 18.1 |
| Downtime reduction 45% (top of DOE band) | 8.4 |
| Lost-production value 1/3 lower | 15.7 |
| CapEx +30% | 14.0 |
| Downside stack (20% AND CapEx +30%) | 23.6 |

Deck statement: "payback ~11 months at base; stays under 24 months even in
the stacked downside" — no false precision, ranges quoted.

## 7. Unit checks

- L × (L/h)⁻¹ h: revenue[L/yr] × margin[–] / hours[h/yr] → L/h ✓
- h/yr × L/h → L/yr ✓ ; counts × L/event → L/yr ✓
- payback = L / (L/yr) × 12 → months ✓ ; NPV in L ✓
