# Project Satoshi Gate — Paytm × Liminal Custody Solutions

## Board / Investment Committee analysis, financial model and slide content

Prepared 23 September 2026 by the deal team. Source of truth: the case document *Project Satoshi Gate — Problem Statement: Round 1 Case Deck Submission* (5 pp.) and *Addendum 1: Modeling Inputs and Clarifications* (1 p.). Companion workbook: `Paytm_Liminal_Deal_Model.xlsx` (21 sheets, 21,662 formula cells, 166 named inputs; every output traces to a labelled input).

**Evidence classes used throughout**

| Tag | Meaning |
|---|---|
| **CASE FACT** | Stated in the case document or Addendum. Never replaced by outside figures. |
| **CALCULATION** | Arithmetic on case facts only. |
| **ANALYST ASSUMPTION** | A parameter the case does not give (Addendum 1 requires these to be disclosed). All are on the `Inputs` sheet and are flexed. |
| **EXTERNAL FACT** | Sourced, dated public information, used only for context, comparables, regulatory sequencing and diligence. Sources on the `Sources` sheet. |
| **INFERENCE** | Our reasoning from the above. |
| **UNKNOWN** | Not knowable from the case or the public record; a diligence item. |

Case note honoured: the case states that Paytm's market capitalisation and the UPI MDR framework are real facts as of September 2026, and that the deal terms, Liminal's financials, the churn range, the ₹750 Cr drag and the PhonePe–Mastercard consortium are constructed for the case. We model the constructed facts exactly as given. External research on the real Liminal Custody, Paytm, PhonePe and Mastercard appears only as labelled context and as diligence questions.

All ₹ figures in crore unless stated. Model base settings unless stated: Liminal ARR growth 20% p.a., discount rate 13%, churn 37.5% (midpoint of the case range), ₹750 Cr fixed cash drag, case headline financing mix (₹2,100 Cr cash from the balance sheet + ₹1,900 Cr in Paytm shares).

---

# A. EXECUTIVE CONCLUSION

**Do not acquire 100% of Liminal for ₹4,000 Cr. Secure the capability by contract, buy a 26% negative-control stake at a valuation of no more than ₹2,500 Cr for 100% (₹650 Cr), attach a growth-linked call option, and hold. Exercise control only if six gates clear. The base expectation is Hold.**

Why, in six numbers (all from the model at the case's own inputs):

1. **The price is not a financial value.** A standalone DCF of Liminal at 20% growth for ten years, margins rising to 25% and a 13% discount rate is ₹1,219 Cr (5.5× ARR); the bull case (30% growth) is ₹2,480 Cr (11.3×). For ₹4,000 Cr to be a financial price, Liminal must compound ARR at 36.8% p.a. for a decade with zero churn and no capital drag. The listed custody leader trades at 5–11× recurring revenue; the only disclosed custody/exchange precedent with revenue public closed at 2.1×. (CALCULATION; EXTERNAL FACT)

2. **The ₹750 Cr drag is worth more than the company.** Its present value over ten years is ₹4,070 Cr against a standalone value of ₹1,219 Cr. The break-even drag at the headline price is negative (−₹630 Cr/yr): there is no capacity for any recurring capital cost at ₹4,000 Cr. The full acquisition never reaches FCF breakeven in ten years under any scenario we ran; cumulative cash consumption is ₹12,052 Cr by year 10. (CALCULATION)

3. **The drag, not the churn, kills the deal first.** Removing the drag improves NPV by ₹4,070 Cr; removing all churn improves it by ₹494 Cr. At the headline price NPV is −₹7,487 Cr in the base case and still −₹2,923 Cr with zero churn and zero drag. The maximum economically acceptable churn at ₹4,000 Cr is therefore "none", at any drag. (CALCULATION)

4. **EPS is dilutive at every financing mix.** From the ₹7.50 baseline, year-1 EPS is ₹5.26 (−30%) at the case mix, ₹6.59 (−12%) all-equity, ₹4.65 (−38%) if the cash leg is debt-funded (gross debt/EBITDA 3.8×), ₹4.00 (−47%) all-cash. The "mechanical" share-count-only figure of ₹7.38 (−1.6%) hides 95% of the dilution. Reported EPS including purchase-price amortisation is ₹3.81. (CALCULATION; ANALYST ASSUMPTION on cost of funds)

5. **The MDR is real but not incremental.** The ₹115 Cr/yr accrues to Paytm with or without Liminal; after flow-through and tax it is ₹69 Cr/yr, 9% of the drag, and it lifts the like-for-like standalone EPS baseline to ₹8.58. Netting it against the deal is a category error. (CASE FACT; CALCULATION)

6. **The strategic need is real and mostly contractable.** Custody/MPC technology can be bought as a service; what cannot be bought is the institutional franchise, and ownership is exactly what destroys 30–45% of it. A ₹650 Cr minority stake with negative control, ROFR/ROFO and a call option secures supply and blocks the consortium for 0.55% of market cap; its expected NPV cost is ₹348 Cr in the base case and about zero in the bull case. That cost is the price of an option, and the Board should approve it as one, not as an investment. (CALCULATION; INFERENCE)

**The decision framework.** (i) Sign a commercial custody/MPC agreement and an exclusivity/ROFR now (cost ≤ ₹25 Cr). (ii) Within three months, if diligence clears six conditions, invest ₹520–650 Cr for 26% (half primary), with a call option on the remaining 74% at 10× audited ARR at exercise, capped at ₹2,960 Cr and paid 55% upfront plus a retention earn-out. (iii) Months 12–24: exercise only if clients representing ≥80% of ARR consent in writing, RBI confirms in writing that no bank-like reserve applies, the then-current DCF exceeds the strike, PAT and FCF break even within five years of exercise, and compliance is clean. Otherwise hold the stake indefinitely, or exit through the ROFO/tag mechanism. Walk away from any structure that carries the ₹750 Cr reserve, from any unconditional price above ₹1,300 Cr for 100%, and from a bidding war with the consortium.

---

# B. FULL ANALYTICAL WORK

## B1. Case deconstruction

### B1.1 Given facts (CASE FACT unless marked)

| Item | Value | Case reference | Certainty | Why it matters | Sensitivity |
|---|---|---|---|---|---|
| Paytm market cap | ₹1,18,750 Cr (~$14B), mid-Sep 2026 | §1, §2 table; case says real | High | Denominator for dilution; share price for the equity leg | Share price ×0.75 → 1.37 Cr shares for ₹1,900 Cr |
| Diluted shares | 64 Cr | §1 | High | EPS denominator; implied price ₹1,855 (CALC) | — |
| Cash / gross debt | ₹8,900 Cr / ₹350 Cr | §1 | High | Liquidity headroom; leverage | Cash floor guardrail ₹5,000 Cr (assumption) |
| Revenue / EBITDA / PAT / EPS | ₹8,450 / ₹640 / ₹480 Cr / ₹7.50 | §1; §5.3 says start all dilution maths from ₹7.50 | High | Baseline; the drag equals 117% of EBITDA (CALC) | PAT held flat (assumption) |
| Credit rating | CRISIL AA− (Stable) | §1 | High (case) | Debt capacity, guardrails | — |
| Deal value | ₹4,000 Cr = ₹2,100 Cr cash + ₹1,900 Cr Paytm shares | §2 | High | Price; consideration mix | Cash leg may be cash, debt or mix (§2) |
| Liminal ARR | ₹220 Cr (~$26M) | §2 table | High | Only financial fact on the target | Growth is the dominant value driver |
| Implied multiple | "18x" (18.18× exact, CALC) | §2 table | High | Anchor for the valuation debate | — |
| Liminal profitability | ~breakeven at net income | §2 | High | No acquired earnings; EPS effect = shares + financing (§2) | Margin ramp is an assumption |
| Top-4 clients | HDFC Bank, Axis Bank, CoinDCX, ZebPay = 60% of ARR | §2 | High | Concentration; the churn mechanism | 30–45% churn = 50–75% of the top-4 book (CALC) |
| Churn on FULL acquisition | 30–45% of ARR within 12 months | §3.1 | High | Applies to full acquisition; minority/JV churn unspecified | Each 10 pts = ₹400 Cr at 18.2×; ~₹132 Cr in DCF terms (CALC) |
| Capital drag | RBI requires bank-like reserves against custodied assets because Paytm holds a PA licence → recurring annual FCF drag ₹750 Cr | §3.2 | High (case) | Owner-specific; PV ₹4,070 Cr at 13% (CALC) | Reading 1/2/3 on `Capital_Drag` |
| Valuation risk | Rich multiple + immediate EPS hit → shareholder pressure for buybacks over M&A | §3.3 | High | EPS is a constraint, not the objective | — |
| UPI MDR | 0.4% on P2M UPI > ₹2,000, capped ₹300, from 15 Oct 2026; assume ₹115 Cr/yr incremental net revenue to Paytm | §3.4; case says framework is real | High (framework), case input (₹115 Cr) | Standalone Paytm item; not a synergy | Flow-through 60–100% |
| Counter-bidder | PhonePe–Mastercard exploratory consortium, if Paytm walks | §2 | High (case); constructed | Competitive urgency; walk-away discipline | No price or terms given |
| Deliverable | 10–15 slides + simple accretion/dilution and transaction model; assumptions slide; PAT and FCF breakeven | §5; Addendum 1 | High | Shapes the outputs | — |

### B1.2 External facts that may legitimately be researched
The case permits treating its figures as given and forbids substituting outside figures. Outside research is used for: (a) comparables and precedents to interpret 18×; (b) the real regulatory sequence (RBI, CCI, FEMA/ODI, SEBI, foreign regulators); (c) Paytm's and the counter-bidders' public record for strategic fit and capacity; (d) the real Liminal's public record as a diligence lens. None of it changes a case input. Full sourcing on the `Sources` sheet (54 entries) and in `Comps`, `Precedents`, `Regulatory`.

### B1.3 Case-constructed assumptions
The case explicitly constructs: the transaction, Liminal's ARR and profitability, the client list and concentration, the churn range, the ₹750 Cr reserve, and the consortium. These are treated as facts of the simulation. The most consequential construction is §3.2: the reserve is triggered by *Paytm owning* the custody infrastructure, i.e. it is owner-specific, not asset-specific.

### B1.4 Unknowns that could change the deal (UNKNOWN)
Liminal's cost base, margin path, AUC, client contracts (change-of-control clauses, term, pricing), churn under a minority (the case only specifies full-acquisition churn), whether the reserve applies at minority or JV level, the reserve's mechanics (fixed cash, AUC-linked or P&L), the consortium's price and structure, Paytm's share of MDR economics, Liminal's licences and litigation. Section B20 turns these into a diligence list.

### B1.5 The decision variables (the ten that decide value creation)

| # | Variable | Base | Range tested | Effect on full-acquisition NPV (₹ Cr) | Effect on the recommendation |
|---|---|---|---|---|---|
| 1 | Capital drag (₹ Cr/yr) and its reading | 750, fixed cash | 0–1,250; fixed / scales with assets / P&L | 0 → +4,070; 1,250 → −2,713; "scales" → −2,552 | Dominant. Any reserve at control level defeats control; written treatment is a condition precedent |
| 2 | Price for 100% | 4,000 | 1,000–4,000 | Linear: each ₹1,000 Cr ≈ +₹1,013 Cr | Sets the walk-away line: ₹1,000–1,300 Cr with no drag; zero with the drag |
| 3 | Liminal ARR growth | 20% | 10–50% | bear −395; bull +1,942 (before drag) | Bull path is the only one where control can pass the gates |
| 4 | Churn on change of control | 37.5% | 0–60% | 0% → +494; 45% → −99 | Franchise damage; governs consent gate and earn-out |
| 5 | Discount rate | 13% | 11–15% | 11% → −11 (drag PV rises too); 15% → +111 | Robust: no rate in range supports the price |
| 6 | Financing mix | 2,100 cash + 1,900 shares | all-cash … all-equity | No NPV effect; EPS −12% to −54%; leverage 0.5–3.8× | Constrains structure and rating, not value |
| 7 | Minority entry valuation | ₹2,500 Cr for 100% | 1,219–4,000 | minority NPV −348 (base) / −20 (bull); at 4,000: −738 / −410 | Negotiating range ₹520–650 Cr for 26% |
| 8 | Churn under minority | 0% | 0–20% | minority NPV −348 → −417 | A gate tested by client consents, not a belief |
| 9 | Drag applied at minority | none | none / pro-rata / full | −348 → −1,406 / −4,418 | If RBI applies any reserve at 26%, do not close |
| 10 | Option strike multiple | 10× ARR at exercise | 8–14× | hybrid NPV in bull: −298 (10×) / −903 (14×) | Above ~10–11× the option is never worth exercising |

## B2. Deal-room facts (the numbers a banker keeps on one page)

| Calculation on case facts | Value |
|---|---|
| Implied Paytm share price | ₹1,855 |
| Trailing P/E; earnings yield | 247×; 0.40% |
| New shares for ₹1,900 Cr equity leg | 1.02 Cr (1.6% of count) |
| Deal ÷ market cap; cash leg ÷ cash | 3.4%; 23.6% |
| Headline multiple | 18.18× ARR |
| Top-4 ARR; case churn in ₹ | ₹132 Cr; ₹66–99 Cr |
| Drag ÷ EBITDA; ÷ PAT; ÷ Liminal ARR | 117%; 156%; 3.4× |
| MDR ÷ drag (revenue line) | 15.3% |
| Net cash today; gross debt/EBITDA | ₹8,550 Cr; 0.55× |

External context (EXTERNAL FACT, for the judges' reality check only): the real One97 reported cash of ₹13,529 Cr at 30 Jun 2026, FY26 PAT ₹552 Cr and diluted EPS ₹8.55, a market cap of ~₹1.14–1.16 lakh Cr in mid/late September 2026 (Paytm Q1 FY27 release, 20 Jul 2026; Screener 23 Sep 2026). Management's stated posture: "dry powder for selective inorganic action, only at the right price and only where strategically additive… we will not deploy capital simply because we have it" (Q4 FY26 release, 6 May 2026) and, on the call, "any new investment, only in AI" (7 May 2026). Paytm's largest transaction ever was a sale (Insider to Zomato, ₹2,048 Cr, Aug 2024); its largest acquisitions were ~₹260 Cr (TicketNew, 2018). A ₹4,000 Cr purchase would be roughly fifteen times anything Paytm has ever bought.

## B3. Root problem

**What Paytm is trying to solve (INFERENCE from §1):** core UPI and checkout growth has slowed, PhonePe and Google Pay dominate volume, the company still operates under regulatory scrutiny after the 2024 Payments Bank action, and management wants a B2B settlement growth vector aligned with RBI's e₹ pilot (tokenised treasury, cross-border settlement). The gap is a regulated-grade trust layer for institutional digital-asset settlement: custody and key-management technology, certifications, and, above all, institutional counterparties that trust Paytm with their settlement flows.

Six layers:

- **Strategic.** The capability gap is credibility with institutions, not code. MPC and custody software are available from Fireblocks, BitGo, Zodia, Coinbase and others, all of which now serve India (CoinSwitch's DigiVault runs on Fireblocks, Mar 2026; WazirX moved to BitGo/Zodia in 2025; Coinbase launched INR rails on 31 May 2026: EXTERNAL FACT). Liminal's differentiators in the case are Indian domicile, FIU-registration, certifications and the bank relationships.
- **Economic.** Value in this deal can only come from (a) Liminal's own cash flows (₹1,219 Cr base, ₹2,480 Cr bull), (b) contracted use of its rails by Paytm (achievable without ownership), and (c) option value on tokenisation/CBDC infrastructure. Ownership adds two large negatives, churn and the reserve, and no positive that a contract cannot deliver.
- **Capability.** What Liminal has that Paytm cannot efficiently build: the certifications and operating history (24–36 months to build: ANALYST ASSUMPTION), and the institutional book. What Paytm can build or rent: the technology.
- **Ownership.** Ownership is needed only to (i) stop a competitor owning the supplier and (ii) capture upside. Both can be had at 26% with ROFR/ROFO, a veto and a call option. Control is needed for neither, and control is what triggers §3.1 and §3.2.
- **Risk transfer.** On ownership Paytm inherits: the reserve; the client revolt; a change-of-control cascade in client contracts; cyber and AML liability for custodied assets; RBI supervisory attention on a group whose payments-bank licence was cancelled in April 2026 and whose PA licence is less than a year old (EXTERNAL FACT); goodwill impairment risk; and the reputational tail of custody incidents (the real Liminal was the multisig co-signer in the July 2024 WazirX hack: EXTERNAL FACT, root cause publicly unresolved).
- **Competitive.** If PhonePe/Mastercard own Liminal, PhonePe faces the same wallet conflict with banks and exchanges (INFERENCE from §3.1); Mastercard as a foreign, non-RBI-regulated owner would not trigger Paytm's PA-specific reserve (INFERENCE from §3.2) and has $11.3B of cash (EXTERNAL FACT, 30 Jun 2026). Paytm cannot win an auction on economics, and should not try.

**Transaction-level problem statement.** Paytm needs assured access to a regulated-grade custody/MPC rail and institutional counterparties for its settlement ambitions within about two years, and wants to deny that rail to its main competitor, at a time when (a) the rail's technology is a commodity available from several global vendors, (b) the target's most valuable asset, its institutional franchise, loses 30–45% of its revenue if Paytm controls it, and (c) control triggers a recurring ₹750 Cr capital cost that exceeds Paytm's entire EBITDA. The question is not "buy or not" but "how much control is worth paying for, at what price, and how to make the sellers bear the risks that ownership creates".

## B4. Strategic hypothesis

**H1 — Access beats ownership.** A multi-year custody/MPC services agreement, a segregated desk and information barriers deliver the capability and most of the strategic value. Test: can Liminal contractually commit capacity, SLAs and exclusivity for Paytm's use cases? (Diligence item.)

**H2 — Negative control is enough to block.** 26% (one share above the 25% special-resolution threshold, Companies Act s.114 / Singapore Companies Act s.184: EXTERNAL FACT) plus ROFR/ROFO on all transfers and a veto on new issuance and schemes closes the consortium's routes. Test: shareholder agreement drafting; the veto does not stop a secondary sale by other holders without a ROFR.

**H3 — Control should be earned, not bought.** A call option at a growth-linked strike converts the ₹4,000 Cr headline from an unconditional price into a cap reached only if Liminal grows into it and its clients consent. Test: seller acceptance of a cap; the option is worth exercising only on the bull path (B15).

**H4 — The reserve is a structure question, not a cost to absorb.** The case ties the reserve to Paytm owning the infrastructure. Non-consolidated ownership, a custodian-level structure, or a regulated (IFSC/foreign) holding may avoid it; nothing in any custodian regime surveyed (MiCA, MAS, ADGM, VARA) levies capital at that scale (EXTERNAL FACT). Test: written RBI treatment before signing anything that could trigger it.

**What would make the hypothesis wrong.** If RBI applies the reserve at any ownership level, if the banks' relationships are already fragile because RBI wants regulated entities insulated from private crypto (RBI testimony, 2 Jul 2026: EXTERNAL FACT), or if Liminal's technology and licences are weaker than the case assumes, then the right answer moves from "minority + option" to "commercial agreement only" or "walk away". The model and the gates are built so that each of these findings changes the recommendation rather than the rationalisation.

## B5. Non-linear issue tree (second- and third-order effects)

**Chain A — Full acquisition.** Announcement → HDFC/Axis/CoinDCX/ZebPay invoke change-of-control or non-renewal (§3.1) → ARR −30–45% within 12 months → cost base sticky, Liminal loses ₹44 Cr in year 1 (ANALYST ASSUMPTION: half the lost revenue's cost persists for a year) → effective entry multiple 24–33× → RBI reserve ₹750 Cr/yr on top → incremental FCF −₹1,045 Cr in year 1 → Paytm's cash falls from ₹8,900 Cr to ₹6,640 Cr at close and ₹5,374 Cr by end of year 3 → the ₹5,000 Cr liquidity floor is breached in year 5 → funding the reserve requires debt, which breaches the leverage guardrail (max new debt ₹610 Cr at 1.5× EBITDA) → rating pressure on a AA− issuer → trapped reserve capital grows to ₹7,500 Cr by year 10 and its foregone yield (over ₹300 Cr/yr after tax by year 10) erodes standalone PAT → EPS −30% in year 1 on the case basis, −49% reported, and falling as trapped capital grows → the stock's turnaround narrative and 247× multiple are exposed exactly when Paytm needs paper to fund anything else (§3.3) → buyback-vs-M&A pressure → forced sale of Liminal at a distressed price into a market where Copper is drawing offers at ~10% of its 2022 valuation (EXTERNAL FACT).

**Feedback loop inside Chain A.** Churn reduces custodied assets; if the reserve scales with assets (reading 2), churn shrinks the reserve, but growth enlarges it: at 20% growth the year-5 reserve is 2.5× the year-1 reserve and the ten-year NPV worsens by ₹2,552 Cr. Under that reading growth cannot rescue the deal; only a change of regulatory treatment can.

**Chain B — Walk away.** Consortium acquires Liminal → PhonePe faces the same bank/exchange revolt (INFERENCE) and, being loss-making with a paused IPO (EXTERNAL FACT), may not fund a ₹4,000 Cr cheque; Mastercard could, and would run Liminal as global stablecoin/tokenisation infrastructure without Paytm's reserve → Paytm loses an Indian-domiciled partner but not the capability: Fireblocks, BitGo, Zodia and Coinbase serve India → Paytm's cost is 24–36 months and ~₹250 Cr to build/partner (ANALYST ASSUMPTION) and the loss of a potential bank-relationship bridge → the strategic loss is real but bounded, and far smaller than the ₹7,487 Cr of value the full acquisition destroys.

**Chain C — Minority + option.** No change of control → contracts unaffected → churn not triggered (a gate, not a belief) → Paytm gets information rights and board presence → RBI reads the exchange filing: supervisory questions about a PA-licensed group holding a crypto custodian → mitigated by holding at OCL/SPV (never inside PPSL), no PA services to crypto flows, and positioning as tokenisation/CBDC key-management → sellers get liquidity and an anchor client → Liminal's growth path reveals itself within 12 months (ARR ≥ ₹286 Cr signals the bull path) → control is exercised only if it is then cheap relative to value.

**Asymmetries and irreversibilities.** The reserve is asymmetric (it can only hurt); the churn is largely irreversible (banks do not come back); the consortium threat is informational (the case gives no price, and the public record shows no such consortium: EXTERNAL FACT); the option is reversible (it lapses); the full acquisition is not (goodwill, integration, reputation). Small operationally, large financially: purchase-price amortisation (−₹1.44 per share of reported EPS at a 25% intangible allocation over 8 years: ANALYST ASSUMPTION); the foregone yield on trapped capital; and the ODI three-year-profit rule, which may make the automatic route unavailable for an overseas financial-services target because One97 reported losses in FY24 and FY25 (EXTERNAL FACT, B18).

## B6. Financial model

`Paytm_Liminal_Deal_Model.xlsx` is built so that a lever change on `Dashboard` propagates through valuation → FCF → leverage → EPS → transaction economics → decision thresholds. Structure:

| Sheet | Purpose | Key outputs |
|---|---|---|
| Dashboard | Scenario, financing and minority levers; headline outputs for all five structures; verdict lines | NPV, EPS, FCF, breakevens, thresholds |
| Inputs | Case facts (light blue, with the case section in a cell comment), calculations on case facts, 50+ team assumptions (yellow) with rationale | — |
| Liminal_Ops | 10-year operating forecast: standalone and post-churn | Revenue, EBITDA, PAT, unlevered FCF |
| DCF | Standalone value; WACC × growth grid; breakeven growth; churn × growth grid | ₹1,219 Cr base; 36.8% breakeven growth |
| Financing | Seven cash/debt/equity mixes: shares, leverage, liquidity, cost of funds, year-1 EPS, guardrail flags | — |
| Sources_Uses | Full acquisition, minority, hybrid control tranche; sources = uses checks | — |
| Accretion | EPS Y0–Y10 from ₹7.50; year-1 bridge; accounting vs economic view | ₹5.26 (−30%) |
| Deal_CF | Master engine: deal cash flows, drag readings, PAT/FCF breakeven, NPV, break-even drag | NPV −₹7,487 Cr |
| Capital_Drag | Three readings; ₹0/500/750/1,000/1,250 grid; MDR offset; break-even drag | −₹630 Cr/yr |
| Churn | 0–60% grid; maximum acceptable churn; price × churn NPV grids | "none" at ₹4,000 Cr |
| Structures | Full / minority / hybrid / JV / walk-away side by side; minority IRR grid; hybrid engine | — |
| Earnout | Retention earn-out schedule; call-option strike formula; escrow; re-cut of a 100% deal | — |
| Scenarios | Base / upside / moderate / severe / break; one-variable-at-a-time test | Drag dominates |
| Thresholds | Computed decision triggers | — |
| Synergies | Tree with incrementality tests; synergy required to justify the price | ₹599 Cr/yr |
| Comps, Precedents, Regulatory, Sources | External facts, sourced and dated | — |
| Audit_Trail | Source → input → formula → output → interpretation for 21 decision-relevant numbers | — |

Every engine (Deal_CF, the churn and drag grids, the five scenarios, the tornado) is the same 10-year block with different parameter cells, so the sheets cannot drift apart. Core outputs were re-computed independently in Python and match to the rupee. Recalculation in LibreOffice reports zero formula errors.

**Material team assumptions (Addendum 1 disclosure; all on `Inputs`):**

| Assumption | Base | Range | Rationale |
|---|---|---|---|
| Liminal ARR growth | 20% (bear 10%, bull 30%) | 10–50% | Infrastructure SaaS at ₹220 Cr ARR; deliberately below the 36.8% that justifies 18× |
| EBITDA margin | 0% today, +5 pp/yr to 25% cap | 20–30% cap | Case: breakeven; mature regulated-infra margin below pure software |
| Tax | 25%, only on positive EBIT; no group relief | — | Indian rate; losses not relievable across entities |
| D&A / capex / working capital | 3% / 3% of revenue; 5% of incremental revenue | — | Asset-light |
| Sticky cost after churn | 50% of lost revenue's cost base for one year | — | Costs fall slower than revenue |
| Cost of cash / cost of debt | 6.0% / 8.5% pre-tax | 5–7% / 8–10% | Treasury yield; AA− pricing |
| Discount rate / terminal growth | 13% / 5% | 11–15% | Rf ~6.5% + β 1.0 × ERP 6.5%; risk placed in the cash flows, not the rate |
| Transaction costs / integration | 1.5% of price / ₹100 Cr (full), ₹15 Cr (minority) | — | Advisory, legal, ring-fence build |
| PPA amortisation | 25% of price over 8 years; off in headline EPS, shown separately | — | Case says EPS effect comes from shares and financing; Ind AS view shown |
| MDR flow-through | 80% to EBITDA, 25% tax → ₹69 Cr | 60–100% | Net revenue already after interchange |
| Liquidity / leverage guardrails | Cash ≥ ₹5,000 Cr; gross debt/EBITDA ≤ 1.5× | — | AA− protection |
| Minority entry valuation | ₹2,500 Cr for 100% (26% = ₹650 Cr); half primary | ₹1,219–4,000 Cr | 11.4× ARR: Paytm's own EV/sales, middle of custody comps, bull DCF pro-rata |
| Churn at minority / at control | 0% (gate) / 20% (after ≥80% consents) | 0–20% / 0–55% | Not beliefs; gates |
| Drag at minority / at control | none (signing condition) / none (gate) | none / pro-rata / full | Written RBI treatment required |
| Option strike | 10× audited ARR at exercise, cap ₹2,960 Cr, 55% upfront + retention earn-out (zero below 55% retention) | 8–14× | BitGo subscription multiple; premium to FI software |
| Control tranche funding | ≤ ₹500 Cr new debt, balance cash; earn-out in collared shares | — | Inside guardrails |
| Build/partner alternative | ₹250 Cr over 3 years | — | Team estimate |

## B7. DCF and valuation: what must be true for 18× to be rational

**Standalone DCF (no churn, no drag), 100% of Liminal, at 13%:**

| 10-year growth | DCF (₹ Cr) | × ARR | Versus ₹4,000 Cr |
|---|---|---|---|
| 10% | 581 | 2.6× | Not supported |
| 20% (base) | 1,219 | 5.5× | Not supported |
| 30% (bull) | 2,480 | 11.3× | Not supported |
| 36.8% | 4,000 | 18.2× | Breakeven: a decade of ~37% growth, zero churn, no reserve, 25% margins |
| 40% | 4,872 | 22.1× | Supported |

At 11% the breakeven growth is 31%; at 15% it is 42%. Terminal value is 68% of the base DCF, which is the honest shape of a young infrastructure business and the reason the multiple is so sensitive to the growth belief.

**Value of the retained business (churn in year 1) × growth, ₹ Cr:**

| Churn ↓ / growth → | 10% | 20% | 30% | 40% |
|---|---|---|---|---|
| 0% | 581 | 1,219 | 2,480 | 4,872 |
| 30% | 380 | 824 | 1,703 | 3,375 |
| 37.5% | 329 | 725 | 1,509 | 3,001 |
| 45% | 279 | 625 | 1,315 | 2,626 |

**Reverse-engineering the ask.** At ₹4,000 Cr the effective multiple is 24.2× retained ARR at 37.5% churn (33.1× at 45%) and 48.9× once the PV of the drag is added to the price. For the ask to be a financial price, all of the following must hold: growth ≥ 37% p.a. for ten years; churn 0%; no reserve; margins reaching 25%. None of the four is the case's own base case.

**Standalone financial value vs strategic/option value.** Financial value: ₹725 Cr after case-midpoint churn (₹1,219 Cr before churn; ₹2,480 Cr bull before churn). Strategic premium embedded in the headline: ₹7,487 Cr with the reserve (the drag is worth −₹4,070 Cr), ₹2,923 Cr without it. In other words, even a buyer who faces no reserve and suffers no churn would be paying about ₹2,800 Cr of premium over base financial value, or ₹1,500 Cr over bull value. Synergies required in perpetuity to close the base-case gap: ₹599 Cr/yr after tax, 2.7× Liminal's entire current ARR (`Synergies`). This argument does not survive scrutiny in any form: the price is a bet on optionality that the case's own constraints then destroy.

**Minority stake value.** Pro-rata DCF of 26%: ₹151 Cr (bear), ₹317 Cr (base), ₹645 Cr (bull). Our entry ceiling of ₹650 Cr equals the bull pro-rata; our target of ₹520 Cr (₹2,000 Cr implied) sits between base and bull. IRR on a year-5 exit at 10× ARR: 7% bear, 16% base, 26% bull; at 6× exit: −4%, 5%, 14% (`Structures` A2). Against a 13% hurdle the stake earns its cost of capital only if Liminal grows ≥ 20% and exits at ≥ 8–10× ARR.

## B8. Comparable companies (EXTERNAL FACT; data 22–23 Sep 2026; `Comps` sheet)

| Peer | Why comparable | Why not / adjustment | Multiple |
|---|---|---|---|
| BitGo (NYSE: BTGO) | Only listed pure-play institutional custodian; 5,833 clients, $65B on platform; Subscriptions & Services line is the closest analogue to ARR | 40× Liminal's scale; OCC trust-bank charter; gross revenue dominated by digital-asset sales; adj. EBITDA negative; ~55% below its Jan 2026 IPO price | 5–7× revenue net of direct costs; 9–11× S&S (derived from Q2 2026 8-K) |
| Coinbase | Largest institutional custodian; now live in India with INR rails | Retail exchange, USDC float; 200× scale | 8.4× EV/revenue |
| Circle | Regulated infra, enterprise distribution | Stablecoin issuer; interest income | 7.7× |
| Gemini | NY-chartered custody | Loss-making retail exchange; custodial fees fell on "institutional custody net outflows" | 5.2× |
| Bullish | Institutional exchange with subscription revenue | EV inflated by treasury assets; the one crypto comp near 18×, for the wrong reason | 17–21× |
| Temenos | ARR-based software sold to banks; 41% EBIT margin | Scale; core banking | 5.8× EV/sales |
| SS&C / Broadridge | Fund-admin and post-trade infrastructure with recurring revenue | 100× scale; slow growth | 4.0× / 2.9× |
| Adyen | Regulated payments infra, 20% growth, 49% margins | Payments, not custody | 6.4× |
| Marqeta | API infrastructure with a documented single-customer concentration history | Card issuing | 1.4× despite 17% growth and 21% adj. EBITDA margin: how markets price concentration |
| Paytm | The acquirer's own currency | Consumer platform | 11.4× EV/sales; ~180× P/E (aggregator) |
| Zaggle / MobiKwik / AvenuesAI | Indian B2B fintech infrastructure | Gross-revenue accounting; consumer | 0.5–1.0× |

**Resulting range.** Applying 5–11× (regulated custody, BitGo) to ₹220 Cr gives ₹1,100–2,460 Cr; FI-infrastructure software (4–6×) gives ₹880–1,320 Cr; the acquirer's own multiple (11.4×) gives ₹2,500 Cr. This corroborates the DCF: ₹1,200–2,500 Cr is the defensible band for 100% before any concentration discount; 18× is a 2021–22 private-market vintage (Fireblocks raised at $8B on >$100M ARR in January 2022, ~80×: EXTERNAL FACT) that the 2026 market no longer pays.

## B9. Precedent transactions (EXTERNAL FACT; `Precedents` sheet)

| Deal | Date | Value | Revenue | Multiple | Read-across |
|---|---|---|---|---|---|
| Robinhood – Bitstamp (50+ licences, institutional-heavy, ~EBITDA-neutral) | closed 2 Jun 2025 | ~$200M | ~$95M LTM net | ~2.1× | The only regulated, institutional, breakeven precedent with both numbers public |
| Ripple – Metaco (bank-grade custody tech; BNP, SocGen, Citi, DBS as clients) | 17 May 2023 | $250M | n/d | n/d | Closest business analogue; a bank-client roster changed hands for $250M |
| Ripple – Palisade (MPC wallet/custody tech) | 3 Nov 2025 | undisclosed | n/d | n/d | Closest technology analogue; small enough not to disclose |
| Standard Chartered – Zodia Custody | offer accepted May 2026 | undisclosed | n/d | n/d | Bank-owned custodian model; price not disclosed |
| Copper (sale process) | May–Aug 2026 | offers ~$200M vs ~$500M ask | n/d | n/d | A scaled custodian drawing ~10% of its 2022 round valuation |
| Mastercard – BVNK | completed 3 Aug 2026 | up to $1.8B incl. $300M contingent | n/d | n/d | Mastercard's appetite; ~17% contingent consideration |
| Mastercard – Zerohash | talks ended Jan/May 2026 | $1.5–2B reported, never signed | n/d | n/d | Mastercard walked away twice |
| Zomato – Blinkit | Jun 2022 | ₹4,447 Cr all stock | ₹236 Cr FY22 | ~18.8× | The only Indian ~18× revenue deal: all-stock, consumer, hyper-growth |
| Zomato – Paytm Insider | Aug 2024 | ₹2,048 Cr cash | n/r | n/d | Paytm's largest ever transaction was a sale |
| PhonePe – ZestMoney (aborted) | Mar 2023 | — | — | — | Counter-bidder walked away after diligence |

**Comparability limits.** No 2025–26 custody-technology deal with a disclosed price above $250M was found. Large tickets cluster in stablecoin rails and volume platforms with undisclosed revenue, so no multiple can be asserted for them. Contingent consideration is standard where value is uncertain. None of the targets carried an owner-specific capital charge like the case's reserve. Conclusion: precedents support a price band of low single-digit to ~10× ARR for a regulated, concentrated, breakeven custodian, and they support structuring (earn-outs, equity-heavy consideration) for concentration risk.

## B10. Financing and Sources & Uses

**Sources & Uses, full acquisition at the case mix (₹ Cr):** Uses: cash consideration 2,100; Paytm shares to sellers 1,900; transaction costs 60; integration/ring-fence 100; total 4,160. Sources: balance-sheet cash 2,260; new debt 0; new Paytm equity (seller paper) 1,900; contingent 0; total 4,160. Check: 0.

**Financing mixes, year-1, 37.5% churn (`Financing`):**

| Mix | New shares (Cr) | Cash after (₹ Cr) | Gross debt/EBITDA | Cost of funds after tax (₹ Cr/yr) | Year-1 EPS | vs ₹7.50 | Guardrail |
|---|---|---|---|---|---|---|---|
| Case: 2,100 cash + 1,900 shares | 1.02 | 6,640 | 0.55× | 94.5 | ₹5.26 | −30% | OK |
| 2,100 debt + 1,900 shares | 1.02 | 8,740 | 3.83× | 133.9 | ₹4.65 | −38% | Leverage breach |
| 1,400 cash + 700 debt + 1,900 shares | 1.02 | 7,340 | 1.64× | 107.6 | ₹5.05 | −33% | Leverage breach |
| All cash 4,000 | 0 | 4,740 | 0.55× | 180.0 | ₹4.00 | −47% | Cash-floor breach |
| All equity 4,000 | 2.16 | 8,740 | 0.55× | 0 | ₹6.59 | −12% | OK |
| 2,100 cash + 1,900 debt (no dilution) | 0 | 6,640 | 3.52× | 215.6 | ₹3.45 | −54% | Leverage breach |

**Readings.** (1) At 247× trailing earnings, Paytm's shares are its cheapest currency in EPS terms (earnings yield 0.4% versus 4.5% after-tax cash yield), so every rupee moved from cash to equity reduces dilution. But an all-equity deal issues 3.4% of the company for a breakeven asset and works only while the multiple holds (§3.3). (2) Debt-funding the cash leg takes gross debt/EBITDA from 0.55× to 3.8×, outside any reasonable AA− headroom; the maximum new debt inside a 1.5× guardrail is ₹610 Cr. (3) No mix changes the deal's NPV: financing moves the cost between shareholders (dilution), the P&L (interest, foregone yield) and the balance sheet (liquidity, leverage). (4) Sensitivity of the case-mix EPS to the cash-yield assumption: ₹5.36 at 5%, ₹5.16 at 7%.

**Balance-sheet resilience after the case mix.** Cash ₹6,640 Cr at close; year-1 deal FCF −₹1,045 Cr; with Paytm's own ₹480 Cr of PAT retained the cash balance is ₹5,374 Cr by end of year 3 and crosses the ₹5,000 Cr floor in year 5. The reserve alone consumes 2.2 years of cash headroom above the floor. That is the mechanism by which an "FCF drag" becomes a rating and a capital-raising problem.

**Financing the recommended structure.** Phase 1: ₹665 Cr from cash (₹650 Cr stake incl. ₹325 Cr primary into Liminal, plus ₹15 Cr costs); no debt, no shares; cash after ₹8,235 Cr; leverage unchanged. Control tranche, if ever exercised (base case at 10×): upfront ₹1,074 Cr funded ₹574 Cr cash + ₹500 Cr debt (gross debt/EBITDA 1.33×, inside the guardrail), earn-out ≤ ₹879 Cr in collared Paytm shares (≤ 0.47 Cr shares, 0.7% of count). Maximum ever payable ₹2,604 Cr; maximum unconditional ₹665 Cr.

## B11. Accretion / dilution (from the ₹7.50 baseline; `Accretion`, `Deal_CF`)

**Full acquisition, case mix, base scenario:**

| | Y0 (day one, annualised) | Y1 | Y2 | Y3 |
|---|---|---|---|---|
| Paytm standalone PAT (₹ Cr) | 480 | 480 | 480 | 480 |
| Liminal PAT after churn (₹ Cr) | 0 | −43.7 | 10.4 | 21.4 |
| Cost of funds after tax (₹ Cr) | −94.5 | −94.5 | −94.5 | −94.5 |
| Foregone yield on trapped reserve capital (₹ Cr) | 0 | 0 | −33.8 | −67.5 |
| Incremental PAT (₹ Cr) | −94.5 | −138.2 | −117.9 | −140.6 |
| Pro-forma shares (Cr) | 65.02 | 65.02 | 65.02 | 65.02 |
| Pro-forma EPS ex-MDR (₹) | 5.93 | 5.26 | 5.57 | 5.22 |
| vs ₹7.50 | −21% | −30% | −26% | −30% |
| Pro-forma EPS incl. MDR (₹) | 5.93 | 6.32 | 6.63 | 6.28 |
| vs like-for-like standalone with MDR (₹8.58) | — | −26% | −23% | −27% |
| Reported EPS incl. PPA amortisation (₹) | 4.49 | 3.81 | 4.13 | 3.78 |
| "Mechanical" share-count-only EPS (₹) | 7.38 | 7.38 | 7.38 | 7.38 |

**Year-1 bridge (₹ per share):** 7.50 baseline → −0.12 new shares → −1.45 cost of funds (foregone treasury yield on ₹2,100 Cr) → −0.67 Liminal's post-churn loss → **5.26**; PPA amortisation would take a further −1.44; the MDR adds +1.06 but is Paytm's own.

**Accounting accretion versus economic value.** PAT breakeven on the deal never arrives within ten years at base settings (year 9 in the bull case with zero churn; year 8 in the upside scenario); if the MDR is (wrongly) credited to the deal it arrives in year 3, which is exactly why the MDR must be kept outside. The economic verdict is the NPV: −₹7,487 Cr. An EPS-accretive structure (all-equity gets closest, −12%) would still destroy the same ₹7,487 Cr; the Board should treat EPS as the shareholder-pressure constraint the case describes (§3.3), not as the objective.

**Minority and hybrid.** Minority: year-1 EPS ₹7.05 (−6%), all of it the foregone yield on ₹665 Cr less a ₹1 Cr associate share; no new shares; associate income covers the foregone yield in year 7 (base) or year 5 (bull). Hybrid with control at end of year 1 (bull path, 20% control churn, no reserve): trough EPS ₹5.84 in year 2 (consolidation of a breakeven business plus cost of funds), PAT and FCF breakeven in year 5, i.e. four years after exercise. Base path: breakeven in year 7, six years after exercise, which fails the five-year gate.

## B12. Churn economics (`Churn`)

**Who leaves and why (INFERENCE from §3.1 and the public record).** The case's range removes ₹66–99 Cr of ARR, which is 50–75% of the top-4 book. The two banks are the natural leavers: they are RBI-regulated, RBI told Parliament in July 2026 that regulated entities should be insulated from private crypto (EXTERNAL FACT), and a bank cannot let a competing wallet operator sit inside its digital-asset key management. The exchanges leave for commercial and data reasons: Paytm could become a competitor in retail digital assets, and Paytm Payments Bank cut off crypto exchanges in May 2021 (EXTERNAL FACT). ZebPay was co-founded by Liminal's founder (CASE FACT), so its ARR is a founder relationship, a key-person risk. The "long tail" (40% of ARR: exchanges, hedge funds, OTC desks) is assumed to stay. Change-of-control clauses, consent rights and termination-for-convenience terms are UNKNOWN and are the first diligence request.

**Grid, full acquisition at ₹4,000 Cr (base growth, ₹750 Cr drag):**

| Churn | Retained ARR | Effective multiple | Value at 18.2× | Y1 Liminal PAT | Y1 EPS | vs ₹7.50 | Y1 FCF after cost of funds | NPV | NPV with drag = 0 |
|---|---|---|---|---|---|---|---|---|---|
| 0% | 220 | 18.2× | 4,000 | +4 | 5.99 | −20% | −1,003 | −6,992 | −2,923 |
| 10% | 198 | 20.2× | 3,600 | −8 | 5.81 | −23% | −1,013 | −7,123 | −3,054 |
| 20% | 176 | 22.7× | 3,200 | −21 | 5.61 | −25% | −1,025 | −7,256 | −3,186 |
| 30% | 154 | 26.0× | 2,800 | −34 | 5.41 | −28% | −1,037 | −7,388 | −3,318 |
| 35% | 143 | 28.0× | 2,600 | −40 | 5.31 | −29% | −1,043 | −7,454 | −3,384 |
| 40% | 132 | 30.3× | 2,400 | −47 | 5.21 | −31% | −1,048 | −7,520 | −3,450 |
| 45% | 121 | 33.1× | 2,200 | −54 | 5.11 | −32% | −1,054 | −7,586 | −3,516 |
| 50% | 110 | 36.4× | 2,000 | −60 | 5.00 | −33% | −1,060 | −7,652 | −3,582 |
| 60% | 88 | 45.5× | 1,600 | −73 | 4.80 | −36% | −1,072 | −7,784 | −3,714 |

PAT, FCF and payback all read "never within ten years" at every churn level.

**Maximum economically acceptable churn.** At ₹4,000 Cr: none. NPV is negative at 0% churn with or without the reserve, so the price, not the churn, is the binding constraint. Churn tolerance is a function of price: without the reserve, 100% of Liminal is value-neutral at about ₹1,080 Cr with 0% churn and about ₹650 Cr at 37.5% churn (base growth). Each 10 points of churn costs ~₹130 Cr of DCF value, versus ₹400 Cr at the headline multiple, because the market-implied multiple overstates what the lost revenue was worth. The shareholder-pressure threshold is different: year-1 dilution exceeds 30% at 38% churn.

**Price × churn (NPV, ₹ Cr, no reserve):**

| Churn ↓ / price → | 1,000 | 1,500 | 2,000 | 2,500 | 3,000 | 4,000 |
|---|---|---|---|---|---|---|
| 0% | +117 | −390 | −896 | −1,403 | −1,910 | −2,923 |
| 20% | −146 | −653 | −1,159 | −1,666 | −2,173 | −3,186 |
| 37.5% | −344 | −851 | −1,358 | −1,864 | −2,371 | −3,384 |
| 45% | −476 | −983 | −1,490 | −1,996 | −2,503 | −3,516 |

With the reserve, no cell is positive at any price above zero. **Why 30–45% is not just a sensitivity:** the leavers are the clients whose relationships constitute the strategic rationale (banks for e₹/tokenised settlement). Losing them does not merely cut revenue; it removes the reason to own the asset. That is why the earn-out floor sits at 55% retention and the consent gate at 80%.

## B13. Capital-drag economics (`Capital_Drag`)

**What the case says and what it can mean.** §3.2 makes the reserve (a) owner-specific: it is triggered by Paytm, a PA-licence holder, owning the custody infrastructure; (b) "bank-like capital reserves against custodied assets"; (c) a recurring annual FCF drag of ₹750 Cr. Three readings are modelled:

| Reading | Mechanics | Year-1 FCF | 10-yr NPV of the deal | Year-1 EPS | Comment |
|---|---|---|---|---|---|
| 1. Literal (base): fixed cash set aside each year | Cash leaves FCF; PAT untouched except the foregone yield on the growing trapped pile (₹34 Cr in Y2 rising to ₹338 Cr in Y10) | −1,045 | −7,487 | 5.26 | Trapped capital reaches ₹7,500 Cr by year 10; recovery only on exit/deregulation (0% assumed; lever `a_recovery`) |
| 2. Proportional to custodied assets (revenue as proxy) | Falls with churn, rises with growth: year-5 reserve 2.5× year-1 | −858 | −10,039 | 5.40 | Growth deepens the trap; the only exit is a change of treatment |
| 3. P&L operating cost | ₹750 Cr expense, ₹562 Cr after tax | −858 | −6,469 | −2.39 | EPS turns negative; the case says "FCF drag", so not the base reading |

**Context (CALCULATION).** ₹750 Cr is 117% of Paytm's EBITDA, 156% of PAT and 3.4× Liminal's revenue. Its PV is ₹4,070 Cr over ten years and ₹5,769 Cr in perpetuity at 13%. For Liminal to fund it from its own cash flow at a 25% margin it would need ₹4,000 Cr of ARR (18× today), 16 years away at 20% growth and 11 at 30%. Post-deal cash covers 2.2 years of it above the liquidity floor.

**Is the ₹115 Cr MDR incremental?** No. It is a policy change Paytm captures whether or not it buys Liminal (§3.4 states it as a Paytm standalone fact). Gross offset 15.3%; after 80% flow-through and 25% tax, ₹69 Cr, i.e. 9.2% of the reserve, leaving a net cash cost of ₹681 Cr/yr in the case-style view. It is therefore an independent Paytm benefit: it belongs in the standalone baseline (EPS ₹8.58 like-for-like), it adds FCF capacity to absorb a drag (liquidity), and it adds nothing to the deal's value. External check: the MDR framework is real (NPCI circular of 15 Sep 2026, effective 15 Oct 2026; an enabling amendment was passed in August 2026; a Supreme Court PIL was filed on 16 Sep 2026), and Paytm has not quantified its share; the ₹115 Cr is the case's modelling input and is used unchanged (EXTERNAL FACT; CASE FACT).

**Grid (base growth, 37.5% churn, headline mix):**

| Drag (₹ Cr/yr) | Y1 FCF after cost of funds | Cumulative cash, 10 yrs | PV of drag | NPV | FCF breakeven | Payback | Effective multiple incl. PV drag | Cash at end of Y3 |
|---|---|---|---|---|---|---|---|---|
| 0 | −295 | −4,552 | 0 | −3,417 | year 9 | never | 24.2× | 7,624 |
| 500 | −795 | −9,552 | 2,713 | −6,130 | never | never | 40.7× | 6,124 |
| 750 | −1,045 | −12,052 | 4,070 | −7,487 | never | never | 48.9× | 5,374 |
| 1,000 | −1,295 | −14,552 | 5,426 | −8,843 | never | never | 57.1× | 4,624 |
| 1,250 | −1,545 | −17,052 | 6,783 | −10,200 | never | never | 65.3× | 3,874 |

**Break-even capital-drag threshold.** The fixed drag at which the full acquisition's NPV is zero is −₹630 Cr/yr at ₹4,000 Cr (i.e. no capacity; the price already exceeds the value of the retained cash flows). At a price of ₹1,200 Cr it is −₹107 Cr/yr; at the bull-growth, zero-churn case it is −₹306 Cr/yr at ₹4,000 Cr. The maximum drag consistent with FCF breakeven by year 5 is also negative (−₹41 Cr/yr). The hybrid's control gate therefore requires a written treatment of nil, or a reserve structured at the custodian level and funded by client economics, not by Paytm. If the reserve applied pro-rata at 26% (₹195 Cr/yr) the minority's NPV falls from −₹348 Cr to −₹1,406 Cr and the structure fails; at the full ₹750 Cr it is −₹4,418 Cr.

**External interpretation (EXTERNAL FACT, used only to interpret, not to override).** No non-bank custodian regime surveyed levies capital at this scale: MiCA Class 2 custodians need €125,000 or one quarter of fixed overheads; VARA AED 600,000 or 25% of overheads; MAS S$250,000; ADGM Category 3C six months' expenditure. Basel SCO60 (in force 1 Jan 2026) applies a 1,250% risk weight to a bank's own Group 2 crypto exposures, not to client assets in custody. A ₹750 Cr recurring charge is consistent only with a bank-balance-sheet treatment or self-insurance of client losses. That is precisely why the case ties it to Paytm's PA licence, and why the structural answer is to keep the custody licence, the client assets and any reserve inside Liminal, unconsolidated, until RBI's treatment is written.
## B14. Synergies (`Synergies`)

Base case credits zero synergies. Each line was tested for reality, incrementality, measurability, timing, ownership-dependence, evidence, obstacles and double counting.

| Line | Year-3 value (₹ Cr, if credited) | Real? | Incremental to the deal? | Needs ownership? | Verdict |
|---|---|---|---|---|---|
| Paytm as anchor client: custody/MPC fees on tokenised-treasury, e₹ and cross-border pilots | 30 | Yes | Yes (new revenue to Liminal) | **No**: a commercial agreement delivers it | Real, contractable; the core of the "access" case |
| Cross-sell to Paytm's merchant/institutional base | 20 | Plausible | Partly | Partly (distribution) | Weak: the ring-fence forbids sharing client data; product not built |
| Bank relationships (HDFC, Axis) opening distribution to Paytm | 0 | No | Negative | — | The case says these clients leave on ownership |
| CBDC/e₹ infrastructure role | 0 | Option | Unclear | No | RBI builds the rails itself (UMI, Demat 2.0, Drunix: EXTERNAL FACT); banks are the pilot participants |
| Cross-border settlement / stablecoin rails | 0 | Option | Unclear | No | RBI's stance on private stablecoins is hostile (EXTERNAL FACT); Nexus/CBDC are the sanctioned lanes |
| Cost synergies (shared services) | 0 | Small | Yes | Yes | Deliberately zero: integration breaches the information barrier that protects the franchise |
| Capital synergies | 0 | Negative | Negative | Yes | The reserve is the opposite of a capital synergy |
| Strategic option value (owning the trust layer) | not quantified | Real but unpriced | Yes | Partly (26% + call captures most) | Belongs in the option, not the DCF |

Double counting flagged: the anchor-client line and cross-sell overlap; the option value must not be added to a DCF that already assumes 20–30% growth. **What must be true:** to justify ₹4,000 Cr the deal needs ₹599 Cr/yr of after-tax synergies in perpetuity, 64× the after-tax value of the synergy revenue the tree can evidence. The capitalised value of the credited upside is ~₹117 Cr. Most of the tree is achievable by contract; ownership adds the churn and the reserve, not the synergies.

## B15. Alternative structures (`Structures`)

| | Full acquisition (case mix) | 26% minority (₹650 Cr) | Hybrid: minority + call option | JV ("SettleCo") | Walk away |
|---|---|---|---|---|---|
| Upfront cash out (₹ Cr) | 2,260 | 665 | 665 | 300 | 0 |
| New shares (Cr) / new debt (₹ Cr) | 1.02 / 0 | 0 / 0 | 0.26 (earn-out, later) / 500 (later) | 0 / 0 | 0 / 0 |
| Cash after close; leverage | 6,640; 0.55× | 8,235; 0.55× | 7,561 after control; 1.33× | 8,600; 0.55× | 8,900; 0.55× |
| Maximum total / unconditional commitment (₹ Cr) | 4,160 / 4,160 | 665 / 665 | 2,604 / 665 | 300 / 300 | 250 / 0 |
| Churn exposure | 37.5% (case) | 0% (gate) | 20% after ≥80% consents | 0% | 0% |
| Capital drag exposure | ₹750 Cr/yr | none (signing condition) | none (gate) | none | none |
| Year-1 EPS (vs ₹7.50) | ₹5.26 (−30%) | ₹7.05 (−6%) | ₹7.05 (−6%); trough ₹5.94 after control | ₹7.30 (−3%) | ₹6.52 (−13%, build cost expensed) |
| Year-3 EPS | ₹5.22 | ₹7.17 | ₹6.53 | ₹7.35 | ₹7.50 |
| PAT / FCF breakeven | never / never | year 7 / no cash yield until exit | year 7 / 7 (base: fails gate); year 5 / 5 (bull: passes) | small | n/a |
| NPV to Paytm, base (₹ Cr) | −7,487 | −348 | −1,187 (Hold outcome) | −284 | −197 |
| NPV to Paytm, bull (₹ Cr) | −6,702 | −20 | −298 (exercise; positive on then-current information) | — | −197 |
| Cash at risk if the thesis fails (₹ Cr) | 8,230 (price + PV drag) | 665 | 665 | 300 | 250 |
| Control | Full, day one | Negative control; board seat; information rights | Negative now; full optional | Shared | None |
| Blocks the consortium? | Yes | Partly (ROFR/ROFO + veto on issuance/schemes) | Yes while the option lives | No | No |
| Reversibility | Low | Medium (tag/ROFO; illiquid) | Medium → low after exercise | Medium | High |
| Time to capability | Immediate if clients stay | Immediate (commercial agreement) | Immediate | 12–24 months | 24–36 months build/partner |
| Regulatory exposure | Highest: reserve, CCI (deal value > ₹2,000 Cr), SEBI preferential issue, RBI supervisory | Lower: no consolidation; CCI likely exempt; ODI/FEMA structuring | As minority; full set at exercise | Moderate | None |

**Strongest case for and against each.**

*Full acquisition.* For: certainty of control and of blocking; immediate capability; upside fully captured if the bull path and zero churn both materialise. Against: value-destroying in every scenario run (best case −₹1,662 Cr at bull growth, zero churn and zero drag); the reserve alone exceeds the company's value; the churn removes the asset's rationale; EPS −12% to −54% depending on mix; liquidity floor breached by year 5; Paytm's supervisory position (PA licence under a year old, payments bank licence cancelled April 2026: EXTERNAL FACT) is the worst platform from which to consolidate a crypto custodian. This argument does not survive scrutiny because none of its benefits requires 100% today and all of its costs do.

*Minority.* For: 0.55% of market cap; secures supply and information; blocks the easiest consortium routes; no reserve if unconsolidated (to be confirmed in writing); no churn trigger; expected NPV cost ₹348 Cr base, about zero bull. Against: a minority in a private company is illiquid and pays no cash yield; at any price above pro-rata base DCF (₹317 Cr) it is a premium for an option, not an investment; if RBI applies the reserve even pro-rata the structure fails; a 26% stake with veto rights is "control" for CCI purposes (EXTERNAL FACT) and must be filed if thresholds are met; ODI into a foreign financial-services entity may require RBI approval because One97 did not post profits in FY24–FY25 (EXTERNAL FACT). This argument survives scrutiny only if the entry price is ≤ ₹650 Cr and the reserve is confirmed not to apply.

*Hybrid.* For: everything the minority gives plus a defined, capped path to control at a growth-linked price; sellers bear churn through the earn-out; control is exercised only when observable facts justify it; maximum ever payable ₹2,604 Cr at 10× (never above ₹4,000 Cr). Against: sellers may refuse a cap or demand an option premium (~₹59 Cr at 3%); the option lapses if gates fail, leaving a minority; on the base path the option is never worth exercising (NPV −₹1,187 Cr; breakeven six years after exercise), so the Board must accept that "Hold" is the modal outcome. Survives scrutiny as an option, provided the Board does not treat exercise as a plan.

*JV.* For: no ownership of the custody book, hence no revolt and no reserve; Paytm-majority in the settlement products; capital-light (₹300 Cr). Against: does not block the consortium (Liminal itself stays for sale); two-parent governance; JV economics are unproven (illustrative NPV −₹284 Cr on our assumptions); the JV's value is the capability, the same value a commercial agreement gives at lower cost. Survives only as a fallback if RBI applies a reserve at minority level.

*Walk away.* For: zero cash at risk; the capability is available from global vendors now serving India; consortium ownership imposes the same wallet conflict on PhonePe. Against: loses an Indian-domiciled, FIU-registered partner and the option on bank relationships; 24–36 months and ~₹250 Cr to replicate; a competitor-owned supplier. Survives scrutiny if diligence finds the franchise weaker than the case assumes, or if sellers insist on unconditional pricing.

**Hybrid mechanics (base and bull):**

| | Base (20%) | Bull (30%) |
|---|---|---|
| ARR at exercise (end Y1) | 264 | 286 |
| Strike (74% × 10× ARR), capped at 2,960 | 1,954 | 2,116 |
| Upfront at exercise (55% retained) | 1,074 | 1,164 |
| Earn-out at 20% control churn | 488 | 529 |
| Control consideration; total incl. minority | 1,563; 2,213 | 1,693; 2,343 |
| Implied multiple on retained ARR at exercise | 10.5× | 10.2× |
| PAT / FCF breakeven after exercise | 6 yrs (fail) | 4 yrs (pass) |
| Then-current DCF of 100% at exercise (approx.) | 1,463 | 3,224 |
| Verdict at month 12–24 | Hold | Eligible to exercise, subject to consents, RBI treatment, compliance |

## B16. Negotiation architecture (`Earnout`)

Principle: pay upfront for what is known (₹220 Cr of ARR, certifications, an operating platform); make the sellers bear what is uncertain (retention on change of control, growth, regulatory treatment, litigation).

**Phase 1 — minority.** Price: target ₹520 Cr (₹2,000 Cr implied, 9.1× ARR), ceiling ₹650 Cr (₹2,500 Cr, 11.4×), walk above ₹780 Cr (₹3,000 Cr). Half primary (growth capital into Liminal, which keeps cash in the group and does not pay founders to leave), half secondary. Rights: one of five board seats plus an observer; information and audit rights; ROFR/ROFO on all transfers; tag-along; anti-dilution; reserved matters (new investor, sale of business, change of custody model, related-party dealings with Paytm); founder and key-engineer retention pool vesting over 24 months; a client-protection charter binding Liminal. Conditions precedent: written RBI comfort that no bank-like reserve applies at 26% and that the group firewall is acceptable; FEMA/ODI route confirmed; competition analysis documented; top-4 soundings under NDA completed; AML/cyber audit clean; no undisclosed litigation.

**Call option on the remaining 74%.** Window months 12–24; a right, not an obligation. Strike = 74% × M × audited ARR at exercise, M = 10× (tested 8–14×), capped at ₹2,960 Cr. Paid 55% at exercise (the worst-case retained ARR in the case's range) and up to 45% as a retention earn-out measured at month 18 after control on the pre-control client base, audited, excluding Paytm-related revenue so that Paytm's own business cannot inflate it, linear between 55% and 100% retention. Earn-out settled in Paytm shares inside a ±15% collar, or cash at Paytm's election if the stock has compressed. Escrow: 10% of the upfront for indemnities; specific indemnity for pre-closing security incidents and regulatory penalties; reps and warranties on licences, client contracts, key material, data localisation; MAC clause covering regulatory action against Liminal or any top-4 client leaving before exercise. If the sellers refuse the option: fall back to 26% + ROFR/ROFO without the call; if they demand a premium, cap it at 3% of the strike (~₹59 Cr) and offset it against the earn-out.

**If the Board insists on 100% now (not recommended).** Re-cut the ₹4,000 Cr as ₹2,200 Cr upfront (55% retention at the headline multiple) plus up to ₹1,800 Cr of retention earn-out; 10% escrow; a condition precedent of written RBI capital treatment with a price adjustment equal to the PV of any reserve (₹4,070 Cr at the case value, i.e. the deal would not close). Even re-cut, this fixes the price risk, not the ownership risk: the churn and the reserve are consequences of control, and no earn-out cures them.

**Contingent value rights.** If the sellers argue for the upside of a tokenisation/CBDC regime, offer a CVR paying a share of Liminal's revenue from RBI-sanctioned tokenisation use cases above a threshold, rather than a higher fixed price. It transfers the regulatory upside risk to the party claiming it.

## B17. Governance design: does each element solve the risk or decorate it?

| Element | Solves the underlying risk? | Comment |
|---|---|---|
| Standalone subsidiary / brand / legal entity | Partly | Necessary but cosmetic on its own; clients judge who controls the keys and sees the data |
| Independent directors, independent chair; Paytm one of five seats (two of seven on control) | Partly | Signals intent; binding only if paired with reserved matters that keep custody operations outside Paytm's reach |
| Ring-fenced operations, separate data architecture, no Paytm access to client identities, positions or flows; MPC key shares never on Paytm infrastructure | Yes | This is the substance: the conflict is data and key control, not branding |
| Restricted employee access; no shared services | Yes | Cost synergies deliberately forgone to keep it credible |
| Independent compliance committee; CCO and CISO reporting to Liminal's board risk committee; annual independent attestation of the barriers shared with clients | Yes | Makes independence auditable by clients rather than described to them |
| Client consent rights and data portability on any change of control | Yes | Converts the case's churn assumption into a measured consent rate before control is taken |
| Institutional client advisory board | Partly | Useful for early warning; not a substitute for consents |
| Arm's-length agreements; Paytm served by a segregated desk on standard terms; published client charter (no preferential pricing, routing or SLAs) | Yes | Removes the commercial-favouritism objection |
| Founder retention and nomination rights while the ring-fence stands | Yes | ZebPay is a founder relationship; key-person risk is concentration risk |
| Reserved matters and conflict protocols | Yes | Defines what Paytm cannot do even at 100% |
| Regulatory reporting architecture: FIU-IND, CERT-In (6-hour incident reporting), DPDP (full obligations May 2027), RBI data localisation if Liminal ever touches PPSL's stack | Yes | Compliance stack that RBI will read (EXTERNAL FACT) |
| Group structure: hold at One97 or an SPV, never inside the PA (PPSL); no PA/escrow services to crypto flows | Yes | The single most important item for the RBI relationship (EXTERNAL FACT: PA Directions 2025 net-worth and fit-and-proper tests; RBI's July 2026 stance) |

**Honest limit.** Governance can convert a 30–45% churn into a measured consent rate; it cannot make a bank comfortable if RBI tells banks to stay away from private crypto. That is why the consent gate is 80% of ARR in writing, not a governance promise.

## B18. Regulatory analysis (EXTERNAL FACT unless marked; `Regulatory` sheet)

**Sequence for the recommended structure.**

| Step | Item | Type | Source (date) |
|---|---|---|---|
| Before term sheet | FEMA/ODI classification: is Liminal (Singapore parent) a "financial services" foreign entity? If yes, the automatic route needs three years of net profits; One97 reported losses in FY24 and FY25 and its first profit in FY26, so an RBI approval route, a profitable investing entity, or investment into the Indian entity is required | Condition precedent (structural) | FEM (OI) Rules 2022, Sch. I para 2; RBI Master Direction on OI (24 Jul 2024); Paytm FY26 results |
| Before term sheet | Investing entity: One97 or an SPV, never PPSL; check Companies Act s.186 headroom (special resolution if exceeded) | Sequencing | Companies Act 2013 |
| Pre-signing | RBI engagement (DPSS) on the group firewall: no PPSL funds or escrow touching Liminal; no PA services to crypto; positioning as tokenisation/CBDC key-management. No licence consent is required for One97 buying a minority (the PA regime's prior-approval rule covers changes of control of the PA itself), but the supervisory relationship is the real gate | Sequencing (supervisory) | RBI PA Directions 2025 (15 Sep 2025); RBI circular 4 Jul 2022; RBI testimony 2 Jul 2026 |
| Pre-signing | Written RBI view on capital treatment at 26% and at control (the case's §3.2) | Condition precedent | Case §3.2 (CASE FACT) |
| Diligence | Liminal's licences and consents: ADGM FSRA controller approval if the ADGM entity is live (the register shows Liminal's FSP withdrawn in March 2025); VARA (in-principle approval, May 2026); MAS status (the Singapore entity appears on MAS's "no longer exempt" list) | CP where licensed; red flag where not | ADGM register (23 Sep 2026); LARA on the Block (17 May 2026); MAS list |
| Diligence | Press Note 3 screen of Liminal's cap table; FDI regularisation check for Liminal India | CP if triggered | DPIIT PN3 (2020) |
| Signing → closing | CCI: 26% with veto rights is "control"; notifiable if thresholds are met and the de minimis target exemption (India assets ≤ ₹450 Cr or turnover ≤ ₹1,250 Cr) is unavailable; Phase I 30 days, outer limit 150 days; the full ₹4,000 Cr deal exceeds the ₹2,000 Cr deal-value threshold | CP if notifiable | Competition (Amendment) Act 2023; 2024 Regulations |
| At signing | SEBI LODR Reg 30 disclosure within 30 minutes/12–24 hours including SHA terms; if Paytm shares are used as consideration, ICDR preferential-issue floor pricing and a special resolution (4–6 weeks) | Condition subsequent / sequencing | SEBI LODR; SEBI ICDR |
| Closing conditions | FIU-IND registration covering every entity serving Indian clients; CERT-In record-keeping and 6-hour reporting; DPDP readiness (full obligations 14 May 2027); AML audit; no undisclosed litigation (WazirX) | Condition subsequent / covenants | PMLA notification 7 Mar 2023; CERT-In Directions 28 Apr 2022; DPDP Rules Nov 2025 |
| At option exercise | RBI written treatment at control; CCI filing (control acquisition); FSRA/VARA/MAS controller approvals; client consents ≥ 80%; refreshed audits; shareholder resolution for any share-settled earn-out | CPs | as above |
| Post-close | Ind AS 28 equity accounting; contingent-liability disclosure; monitoring of the Parliamentary VDA report (new committee from Oct 2026), any SRO/licensing regime, and MDR notification changes | Ongoing | Lok Sabha Finance Committee 36th Report (23 Jul 2026) |

**Does owning custody create additional requirements?** Per the case: yes, bank-like reserves at ownership (₹750 Cr/yr). Per the public record: VDA custody in India is a PMLA-registered but otherwise unregulated activity (MoF to Parliament, July 2026); no custodian licence or capital rule exists; RBI has asked lawmakers to keep regulated entities insulated from private crypto and formally backed a ban (Reuters, 8 Jul 2026). We never say "RBI will approve". The relevant items are: a supervisory conversation before announcement; a written capital treatment as a condition precedent; and a structure that keeps the licence, the client assets and any reserve inside Liminal.

**Between signing and closing:** no material adverse regulatory change on either side; no top-4 client termination; FIU-IND standing; clean cyber audit. **After closing:** standalone compliance; AML monitoring; segregated data and keys; continuous cyber monitoring; independent reporting to both boards' risk committees. **Regime-change scenario:** a future Indian licensing regime with capital and ring-fencing from banks is a scenario the model carries as the reserve; it is the reason control is never exercised without a written treatment.

## B19. Competitive dynamics

**Why the consortium would value Liminal (INFERENCE).** PhonePe wants what Paytm wants: an institutional settlement rail and a defence against being disintermediated in tokenised payments. Mastercard's public strategy is stablecoin settlement and tokenisation infrastructure (BVNK acquired for up to $1.8B in 2026; stablecoin settlement launched June 2026; a 100-partner crypto programme: EXTERNAL FACT), and an Indian-domiciled, FIU-registered custodian with bank relationships would be a natural node.

**Could their economics differ?** Yes, in Paytm's disfavour. Mastercard is not an RBI-regulated PA; the case's reserve is triggered by Paytm's licence status, so a foreign owner may not carry it (INFERENCE from §3.2). Mastercard has $11.3B of cash and $7.8B of buyback headroom (30 Jun 2026): the price is immaterial to it. PhonePe, by contrast, reported a FY26 net loss of ₹2,792 Cr, paused its IPO in March 2026, has made no acquisition since 2022 and has said publicly why it stayed away from crypto (EXTERNAL FACT). The plausible consortium is Mastercard's cheque with PhonePe's distribution.

**If they win.** PhonePe inherits the same bank/exchange revolt (the case's mechanism is "a competing payments company that also runs a consumer wallet"), so Liminal's institutional book is impaired for them too; Mastercard gains an India node for tokenisation. Paytm loses an Indian partner, not the capability: Fireblocks, BitGo, Zodia and Coinbase all serve Indian institutions today. The strategic loss is bounded: 24–36 months and ~₹250 Cr to build or partner, and the loss of a potential bridge to bank relationships that, under RBI's current stance, may not be available to any wallet operator anyway.

**If Paytm overpays out of fear.** The model says what fear costs: at ₹4,000 Cr with the reserve, −₹7,487 Cr; without the reserve, −₹2,923 Cr at zero churn. Winning at 18× a business that loses 30–45% of its revenue on change of control is the winner's curse the case describes in §3.3.

**Is competitive ownership itself a sufficient justification?** No. It justifies a blocking position (26% + ROFR/ROFO + veto + call), which costs ₹350 Cr of expected value in the base case; it does not justify a control premium.

**Walk-away threshold (economics, not emotion).** For 100%: with the reserve, zero; without the reserve, ₹1,000–1,300 Cr at base growth and 0–20% churn, up to ~₹2,500 Cr only on the bull path with contingent structure. For 26%: ₹650 Cr. If the consortium offers more on unconditional terms, let them. Public-record check: no PhonePe–Mastercard consortium or custody interest exists outside the case (EXTERNAL FACT, searched to 23 Sep 2026); the only link is a device-tokenisation partnership (7 Oct 2025).

**If Paytm's multiple compresses.** Phase 1 is cash and independent of the stock. A 25% fall in the share price would lift the case's ₹1,900 Cr equity leg from 1.02 to 1.37 Cr shares; the real exposure is narrative: a −30% EPS print on a stock at ~247× earnings. The recommended structure prints −6% and can be justified to shareholders as a 0.55%-of-market-cap option with a defined cap.

## B20. Information asymmetry and diligence

**The ten unknowns that could change the decision:**

| Unknown | Why it matters | How to test | Decision consequence |
|---|---|---|---|
| Change-of-control, consent and termination clauses in the top-4 contracts | They convert the case's 30–45% into a contractual fact | Contract review; top-4 soundings under NDA | Consents < 80% → no control; < 55% → no option value; contracts silent → price the risk in the earn-out |
| RBI's capital treatment at 26% and at 100% | The reserve is worth more than the company | Pre-signing consultation; written response | Any reserve at 26% → do not close; any reserve at control → never exercise |
| ARR definition and quality: contracted vs run-rate, pricing per client, Paytm-independent | The only target financial the case gives | Revenue recognition review; client-level ARR schedule; renewal history | ARR < ₹200 Cr contracted → re-price pro-rata |
| Cost base and margin path | Our ramp to 25% is an assumption | Management accounts; headcount; cloud/HSM costs | Mature margin ≤ 15% → base DCF ≈ ₹700 Cr; minority ceiling falls to ~₹400 Cr |
| Licences and regulatory perimeter (Singapore, ADGM, Dubai, Hong Kong, India) | Determines consents needed and whether the "regulated custodian" premise holds | Regulator registers; legal opinions | Unlicensed servicing of Indian/overseas clients → red flag; re-price or walk |
| Security incidents, litigation and indemnity exposure (the real Liminal's WazirX history) | Reputational and financial tail; the mechanism of client sensitivity | Forensic reports; police correspondence; insurance; claims register | Unresolved liability → specific indemnity + escrow; unquantifiable → walk |
| Key-person and founder dependence (ZebPay relationship) | Concentration disguised as a client | Retention terms; succession | No retention pool → discount ARR at risk |
| Technology concentration and IP ownership (MPC libraries, HSM vendors, third-party components) | Supply risk; licensability of the tech to Paytm | Code and licence audit | Third-party dependence → licence terms in the commercial agreement |
| Custodied-asset base and its link to any reserve | Determines whether the reserve is fixed or asset-linked (reading 1 vs 2) | AUC by client and asset type | Asset-linked reserve → growth deepens the trap; restructure |
| The consortium's real interest, price and structure | Sets urgency and the reservation price | Market intelligence; sellers' process letters | Evidence of a foreign-owner bid without the reserve → do not match; keep ROFR |

Full request list covers: customer concentration and profitability, ARR definition, renewal and churn history, contracts and consents, regulatory dependencies, technology concentration, key persons, cybersecurity, litigation, IP, employee retention, founder dependence, geography of clients and entities, counterparty exposure and revenue quality.
## B21. Scenario tree (`Scenarios`; full acquisition at ₹4,000 Cr, case mix)

| | Base | Upside | Moderate downside | Severe downside | Break case |
|---|---|---|---|---|---|
| Growth / churn / drag / reading / WACC | 20% / 37.5% / 750 fixed / 13% | 30% / 10% / 500 fixed / 12% | 20% / 30% / 750 fixed / 13% | 10% / 45% / 1,000 fixed / 14% | 10% / 55% / 1,250 scaling / 15% |
| Retained year-1 ARR (₹ Cr) | 165 | 257 | 185 | 133 | 109 |
| Effective multiple | 24.2× | 15.5× | 21.6× | 30.1× | 36.7× |
| Year-1 EPS (vs ₹7.50) | 5.26 (−30%) | 5.80 (−23%) | 5.41 (−28%) | 5.17 (−31%) | 4.99 (−33%) |
| Year-1 FCF after cost of funds (₹ Cr) | −1,045 | −765 | −1,037 | −1,299 | −929 |
| Cumulative cash, 10 years (₹ Cr) | −12,052 | −8,563 | −11,971 | −14,866 | −14,790 |
| PAT / FCF breakeven | never / never | year 8 / never | never / never | never / never | never / never |
| Value of Liminal before drag (₹ Cr) | 725 | 2,667 | 824 | 236 | 149 |
| PV of drag (₹ Cr) | 4,070 | 2,825 | 4,070 | 5,216 | 4,441 |
| NPV (₹ Cr) | −7,487 | −4,301 | −7,388 | −9,120 | −8,431 |
| Cash at end of year 3 (₹ Cr) | 5,374 | 6,174 | 5,386 | 4,613 | 5,550 |

Even the upside scenario (ring-fence works, 30% growth, reserve cut to ₹500 Cr, 12% WACC) destroys ₹4,301 Cr. **Which variable kills the deal first?** One-at-a-time from base: drag → 0: +₹4,070 Cr; drag → ₹1,250 Cr: −₹2,713 Cr; drag scaling with assets: −₹2,552 Cr; churn → 0%: +₹494 Cr; churn → 45%: −₹99 Cr; growth → bear: −₹395 Cr; WACC +2pp: +₹111 Cr (the drag's PV falls faster than Liminal's value). Order of lethality at the headline price: (1) the reserve, (2) the price itself (NPV −₹2,923 Cr with neither churn nor reserve), (3) growth, (4) churn. Churn is strategically first (it removes the rationale) but financially fourth (because the DCF, unlike the headline multiple, values the lost revenue at ~₹130 Cr per 10 points).

**How the recommendation changes under downside (case §4).** The recommended structure's exposure is capped at ₹665 Cr in every scenario until gates clear. Under the base case the outcome is Hold; under the upside it is Exercise (control at ~₹1,700 Cr, breakeven within four years); under moderate downside, Hold; under severe downside, exit via ROFO/tag (stake NPV −₹514 Cr at bear growth); under the break case, exit, and the consortium is welcome to the reserve.

## B22. Deal killer

| Step | Content |
|---|---|
| 1. Single most dangerous assumption | That the ₹750 Cr reserve is a manageable cost rather than a structural bar. It is triggered by Paytm's own licence status, it recurs, and under an asset-linked reading it grows with the very growth that is supposed to justify the price. |
| 2. Second-order consequence if wrong | If any reserve applies at minority level, the minority's NPV falls from −₹348 Cr to −₹1,406 Cr (pro-rata) or −₹4,418 Cr (full); the option is worthless; Paytm holds an illiquid stake in a business it cannot consolidate. If a reserve applies at control after exercise, cash breaches the floor within five years and the rating is at risk. |
| 3. Financial impact | PV ₹4,070 Cr over ten years (₹5,769 Cr in perpetuity) at the case value; ₹195 Cr/yr pro-rata at 26%; trapped capital of ₹7,500 Cr by year 10; foregone yield over ₹300 Cr/yr by year 10. |
| 4. Strategic impact | A regulated payments group that cannot consolidate the asset it bought; supervisory attention on a PA licence under a year old; the buyback-vs-M&A narrative the case warns of. |
| 5. Mitigation | Never consolidate before the treatment is written; keep the licence, client assets and any reserve inside Liminal; hold at One97/SPV, not PPSL; position as tokenisation/CBDC key management; JV/licence fallback if RBI applies a reserve at minority level. |
| 6. Contractual protection | Written RBI treatment as a condition precedent for Phase 1 and a gate for exercise; MAC clause covering adverse regulatory treatment; price adjustment equal to the PV of any reserve in any 100% structure; termination right after signing if the treatment changes. |
| 7. Walk-away trigger | Any recurring reserve at minority level → do not close. Any recurring reserve at control → never exercise. A change of treatment after signing → terminate under the CP/MAC before closing. |

Second deal killer, for completeness: top-4 consents below 55% of ARR at the validation point → no option value, remediation ladder (day 30 review, day 90 governance reset, day 180 exit process); below 80% → hold.

## B23. Hidden value (searched deliberately after the downside)

| Area | What it is | Ownership needed? | Classification | Evidence |
|---|---|---|---|---|
| Key-management for bank tokenised deposits and RBI's Unified Markets Interface | Banks in the e₹ and tokenisation pilots (HDFC Bank and Axis Bank among the 19 e₹ pilot banks) need institutional-grade key management; RBI's UMI settles tokenised CDs and, since 10 Sep 2026, corporate bonds ("Demat 2.0") in wholesale CBDC | No (vendor role) | Probable, not yet material | EXTERNAL FACT: RBI Annual Report FY26; Indian Express 11 Sep 2026 |
| Tokenised securities custody in GIFT City | IFSCA consultation (Feb 2025) contemplates third-party custodians for tokenised real-world assets; no final framework | No | Possible | EXTERNAL FACT: IFSCA consultation paper |
| Cross-border settlement with stablecoins | Liminal's real business is dominated by USDT/USDC flows for cross-border payment firms; RBI prefers CBDC/Nexus and is hostile to private stablecoins | No | Possible offshore; improbable onshore | EXTERNAL FACT: Liminal PR 5 Mar 2026; RBI FSR Dec 2025 |
| Institutional treasury and B2B settlement for Paytm merchants | Custody rails for merchant treasury products (tokenised deposits, programmable payouts) | No (commercial agreement) | Possible | Case §1 ambition |
| Collateral management and OTC settlement (Liminal Prime, Sep 2026) | Off-exchange settlement for institutions; OTC products are unavailable in India, UAE, Singapore and Taiwan | No | Possible, offshore only | EXTERNAL FACT: GlobeNewswire 2 Sep 2026 |
| Regulator-led substitutes | NPCI's Drunix ledger (Jun 2026) and RBI's own rails reduce the room for a private custodian in domestic CBDC infrastructure | — | Negative for the thesis | EXTERNAL FACT: Business Standard 17 Jun 2026 |
| Primary capital into Liminal (our ₹325 Cr) | Funds licences, HSM vaults and the bank-facing product without diluting Paytm's balance sheet | Minority suffices | Probable | Structure choice |

Economically material today: none. The hidden value is real but it is option value that a 26% stake and a commercial agreement capture as well as 100% does, and most of it does not depend on ownership at all.

## B24. Non-obvious insights

1. **Fact:** the case makes the reserve owner-specific (Paytm's PA licence). **Interpretation:** the reserve is not a property of the asset; a bank-licensed or foreign owner may not carry it. **Why it matters:** Paytm is structurally the highest-cost owner of Liminal in the field. **Consequence:** Paytm cannot win an auction on economics and should compete on structure (block, access, option), not price.

2. **Fact:** DCF value of 100% is ₹1,219 Cr; PV of the reserve is ₹4,070 Cr. **Interpretation:** the drag is worth 3.3× the company. **Why it matters:** the debate about churn (₹400 Cr per 10 points at the headline multiple) is a rounding error against the reserve. **Consequence:** the first negotiation is with RBI's treatment, not with the sellers.

3. **Fact:** if the reserve is "against custodied assets", it scales with assets. **Interpretation:** growth deepens the trap (year-5 reserve 2.5× year-1 at 20% growth). **Why it matters:** the usual defence of a high multiple ("growth will fix it") inverts. **Consequence:** the exercise gate must include the written form of the reserve, not just its current level.

4. **Fact:** the MDR is effective 15 Oct 2026 regardless of the deal and equals ₹69 Cr/yr after tax. **Interpretation:** the case invites teams to net it against the drag. **Why it matters:** doing so moves PAT breakeven from "never" to year 3 and flatters every structure. **Consequence:** the correct EPS baseline is ₹8.58, and the deal is measured against it.

5. **Fact:** Paytm trades at ~247× trailing earnings; its after-tax cash yield is 4.5%. **Interpretation:** in EPS terms, paper is Paytm's cheapest currency and cash its most expensive, so all-equity "looks" best (−12%). **Why it matters:** issuing 3.4% of the company for a breakeven asset is cheap only while the multiple holds, and §3.3 says the multiple is the fragile thing. **Consequence:** no unconditional equity; earn-out shares inside a collar; cash for Phase 1.

6. **Fact:** the top-4 include ZebPay, co-founded by Liminal's founder. **Interpretation:** part of the concentrated ARR is a founder relationship. **Why it matters:** it is key-person risk disguised as customer concentration. **Consequence:** founder retention and nomination rights are retention economics, not HR.

7. **Fact:** purchase-price amortisation is not in the case's EPS framing. **Interpretation:** reported Ind AS EPS would be ₹3.81 (−49%), not ₹5.26 (−30%). **Why it matters:** the number shareholders and the press see is the reported one. **Consequence:** any control structure needs a communicated cash-EPS bridge before signing.

8. **Fact:** the FEMA/ODI rules require three years of net profits for automatic-route investment into a foreign financial-services entity, and One97 posted losses in FY24 and FY25 (EXTERNAL FACT). **Interpretation:** the binding legal gate may be FEMA, not the PA regime. **Why it matters:** it decides which entity invests and whether RBI approval is needed before the sellers are even engaged. **Consequence:** structure the investing entity first; a term sheet that ignores this is unsignable.

9. **Fact:** the custody technology is available in India from Fireblocks, BitGo, Zodia and Coinbase (EXTERNAL FACT). **Interpretation:** "security of supply" is weaker than the case's consortium framing implies. **Why it matters:** the value of blocking is bounded by the cost of switching supplier, not by Liminal's value. **Consequence:** the minority premium should be small (₹150–350 Cr over pro-rata value), and it is.

10. **Fact:** the real Liminal's regulatory perimeter narrowed after the 2024 WazirX incident (ADGM permission withdrawn, MAS "no longer exempt" listing, UAE rebrand with only an in-principle approval: EXTERNAL FACT). **Interpretation:** the case's "ISO 27001 / SOC 2, bank clients" construct should be verified, not assumed. **Why it matters:** the premise that Paytm is buying a licensed, bank-grade custodian is the premise on which every rupee of premium rests. **Consequence:** licences, incidents and litigation are conditions precedent, and the commercial agreement comes first because it is the cheapest way to learn.

## B25. Decision triggers (`Thresholds`; computed, not asserted)

| Trigger | Threshold (base levers) | Action |
|---|---|---|
| Any recurring reserve at 26% | > ₹0 | Do not close Phase 1; move to commercial agreement + JV/licence path |
| Any recurring reserve at control | > ₹0 (break-even drag is negative at any price) | Never exercise; hold or exit |
| Minority entry valuation | > ₹2,500 Cr implied (₹650 Cr for 26%) | Do not invest; commercial agreement + ROFR only |
| Written client consents to Paytm control | < 80% of ARR | Hold; < 55% → no option value, remediation ladder, then exit via ROFO/tag |
| ARR at month 12 | ≥ ₹286 Cr signals the bull path; ~₹264 Cr base | Only the bull path passes the five-year breakeven gate |
| Then-current DCF at exercise vs strike | DCF of 74% < strike | Do not exercise |
| PAT and FCF breakeven after exercise | > 5 years | Do not exercise |
| Strike multiple demanded by sellers | > ~11× ARR at exercise | Option not worth holding; fall back to 26% + ROFR |
| Full-acquisition price (no reserve, base growth) | > ₹1,300 Cr at 0–20% churn; > ₹650 Cr at 37.5% churn | Walk away |
| Full-acquisition price (bull path, contingent structure) | > ~₹2,500 Cr total incl. earn-out | Walk away |
| New debt | > ₹610 Cr (1.5× gross debt/EBITDA) | Use cash or equity; or do not proceed |
| Cash after any step | < ₹5,000 Cr | Do not proceed |
| Year-1 EPS dilution at control (case basis) | worse than −10% | Re-cut consideration mix or defer |
| Licences / incidents / litigation in diligence | Any unremediated red flag (MAS perimeter, unresolved incident liability) | Do not close Phase 1 |
| Consortium offers unconditional terms above reservation value | any | Let them |
| Regulatory deterioration after signing | Reserve applied, RBI objection, top-4 termination | Terminate under CP/MAC before closing; suspend exercise after closing |

## B26. Recommendation

**Recommended path: commercial access now, 26% negative-control stake at ≤ ₹650 Cr, growth-linked call option, control only if earned. Base expectation: Hold.**

*What must be true for each structure to work.* Full acquisition at ₹4,000 Cr: ≥37% growth for ten years, zero churn, no reserve; none is the case's base and the reserve is the case's fact. Minority: entry ≤ ₹650 Cr, no reserve at 26%, contracts unaffected by a minority, licences verified. Hybrid: the bull path (ARR ≥ ₹286 Cr at month 12), ≥80% consents, written nil treatment, strike ≤ ~11×. JV: RBI applies a reserve at minority level and the sellers accept licensing. Walk away: diligence finds the franchise or licences weaker than the case assumes, or the sellers insist on unconditional pricing.

*What destroys value.* The reserve (₹4,070 Cr PV), the price (₹2,800 Cr above base value even with no churn and no reserve), asset-linked scaling of the reserve, churn of the bank relationships, and paying for control before it is observable.

*Controllable risks.* Structure (no consolidation before treatment), price (cap and earn-out), governance (ring-fence auditable by clients), sequencing (RBI engagement before disclosure), financing (cash for Phase 1, ≤ ₹500 Cr debt at control, collared shares).

*Uncontrollable risks.* RBI's treatment and stance on crypto; bank clients' willingness to consent; the consortium's price; Liminal's growth; the MDR's durability (a PIL is pending).

*Structure that protects Paytm if the assumptions are wrong.* Maximum unconditional exposure ₹665 Cr (0.56% of market cap); every further rupee is conditional on facts observed after 12 months; total can never exceed ₹4,000 Cr and at a 10× strike would be about ₹2,600–2,800 Cr depending on ARR at exercise; exit rights (ROFO/tag) if the thesis fails.

*Acceptable price and terms.* Phase 1: ₹520–650 Cr for 26%, half primary; ROFR/ROFO, veto, board seat, information rights, retention pool, client charter. Option: 74% × 10× audited ARR at exercise, capped at ₹2,960 Cr, 55% upfront + 45% retention earn-out (zero below 55% retention), collared shares, 10% escrow, specific indemnities. Reservation value for 100%: zero with the reserve; ₹1,000–1,300 Cr without it at base growth; ~₹2,500 Cr total only on the bull path with contingent structure.

*Conditions before closing Phase 1.* Written RBI treatment (no reserve at 26%; firewall acceptable); FEMA/ODI route confirmed; competition analysis documented; top-4 soundings completed; licences verified in each jurisdiction; AML/cyber audit clean; incidents and litigation disclosed and indemnified; SHA with reserved matters executed; commercial agreement executed.

*Renegotiate or walk.* Renegotiate if contracted ARR is below ₹200 Cr, if the mature margin is below 15%, or if the sellers demand a strike above ~11×. Walk if any reserve applies at 26%, if consents are unobtainable, if licences or incidents are unremediated, or if the consortium bids unconditionally above the reservation value.

---
# C. SLIDE CONTENT (text only; 13 main slides + 2 appendix pages)

**Slide 1 — Board recommendation: secure the rail, do not buy the reserve**
- Core message: Do not acquire 100% of Liminal for ₹4,000 Cr. Sign a custody/MPC agreement, buy 26% at ≤ ₹650 Cr (≤ ₹2,500 Cr implied), hold a growth-linked call option, and exercise control only if six gates clear. Base expectation: Hold.
- Bullets: (1) Standalone DCF ₹1,219 Cr base / ₹2,480 Cr bull vs ₹4,000 Cr ask; 18× needs 37% growth for ten years with zero churn and no reserve. (2) The ₹750 Cr reserve has a PV of ₹4,070 Cr, more than the company; break-even drag at the headline price is negative. (3) Full acquisition: NPV −₹7,487 Cr, year-1 EPS ₹5.26 (−30%), FCF never breaks even, cash floor breached in year 5. (4) Recommended path: ₹665 Cr unconditional (0.56% of market cap), EPS −6%, cap ₹2,604 Cr at a 10× strike, never above ₹4,000 Cr. (5) Board ask: approve the commercial agreement, the ₹665 Cr investment subject to six conditions precedent, and the option framework; delegate gate reviews to the M&A/Risk committee.
- Exhibit: one bar chart of NPV by structure (full −7,487; hybrid −1,187 base / −298 bull; minority −348 / −20; JV −284; walk-away −197) with the unconditional cheque overlaid.
- Sources: model `Dashboard`, `Structures`.
- Why it matters: answer first; every number on the slide reproduces from the workbook.

**Slide 2 — What Paytm is actually trying to solve**
- Core message: Paytm needs a trusted institutional settlement rail and counterparties; the technology is buyable by contract, the franchise is destroyed by control.
- Bullets: (1) Case §1: UPI/checkout growth slowing, PhonePe and Google Pay dominate, RBI scrutiny, ambition in tokenised treasury and e₹ settlement. (2) Liminal offers custody/MPC, ISO 27001 and SOC 2, and HDFC, Axis, CoinDCX, ZebPay = 60% of ARR. (3) The paradox: the clients Paytm wants are the clients who leave if Paytm controls their custodian (30–45% of ARR). (4) Substitutes exist: Fireblocks, BitGo, Zodia and Coinbase serve India today (external). (5) Therefore the deal question is how much control to pay for, not whether to have access.
- Exhibit: two-column "what ownership adds vs what a contract delivers".
- Sources: case §1–§3; `Regulatory`, `Sources`.
- Why it matters: reframes the case away from buy/no-buy before any number is shown.

**Slide 3 — Assumptions: case facts vs calculations vs team assumptions (Addendum 1)**
- Core message: every number is a case fact, arithmetic on one, or a disclosed, flexed assumption.
- Bullets: Case facts table (Paytm baseline; deal; ARR; churn; drag; MDR). Calculations (share price ₹1,855; 18.2×; 1.02 Cr shares; drag 117% of EBITDA). Team assumptions with base/range: growth 20% (10–50%), margin ramp to 25%, tax 25%, WACC 13% (11–15%), cash yield 6%, debt 8.5%, guardrails (cash ≥ ₹5,000 Cr, debt/EBITDA ≤ 1.5×), minority entry ₹2,500 Cr implied, option strike 10× (8–14×), churn at control 20% after ≥80% consents, drag at minority/control nil (gates).
- Exhibit: three-column table.
- Sources: `Inputs`.
- Why it matters: the Addendum requires it; it pre-empts "where does that come from".

**Slide 4 — Valuation: what you need to believe for 18×**
- Core message: ₹4,000 Cr is a strategic premium, not a financial value.
- Bullets: (1) DCF by growth at 13%: 10% → ₹581 Cr; 20% → ₹1,219 Cr; 30% → ₹2,480 Cr; breakeven 36.8%. (2) Public custody leader at 5–11× recurring revenue; regulated-institutional precedent (Bitstamp) at 2.1×; Indian ~18× exists only for an all-stock hyper-growth consumer deal (Blinkit). (3) Effective multiple on retained ARR: 24.2× at 37.5% churn, 48.9× including the reserve's PV. (4) Value band for 100%: ₹1,200–2,500 Cr before concentration discount; pro-rata for 26%: ₹317 Cr base, ₹645 Cr bull. (5) Synergies needed to justify the ask: ₹599 Cr/yr after tax in perpetuity, 2.7× Liminal's ARR.
- Exhibit: WACC × growth grid with the ₹4,000 Cr contour; comps bar (multiple × ₹220 Cr).
- Sources: `DCF`, `Comps`, `Precedents`.
- Why it matters: replaces "18× is expensive" with the exact belief the price requires.

**Slide 5 — The reserve is worth more than the company**
- Core message: at any price above zero, a ₹750 Cr recurring reserve makes ownership uneconomic; the treatment must be written before any consolidation.
- Bullets: (1) ₹750 Cr = 117% of EBITDA, 156% of PAT, 3.4× Liminal's revenue; PV ₹4,070 Cr (ten years), ₹5,769 Cr (perpetuity). (2) Three readings: fixed cash (NPV −₹7,487 Cr), scales with assets (−₹10,039 Cr; growth deepens the trap), P&L cost (EPS −₹2.39). (3) Grid ₹0/500/750/1,000/1,250 Cr: FCF never breaks even at any positive level; cash at end of year 3 falls to ₹5,374 Cr at ₹750 Cr. (4) Break-even drag −₹630 Cr/yr: no capacity. (5) MDR covers 15% gross, 9% net (₹69 Cr) and accrues without the deal; it belongs in the ₹8.58 baseline.
- Exhibit: waterfall of value (DCF 1,219 → after churn 725 → minus PV drag −4,070 → minus one-time −142 → minus price −4,000 = −7,487).
- Sources: `Capital_Drag`, `Deal_CF`.
- Why it matters: it is the deal killer, quantified and structured around.

**Slide 6 — Churn: who leaves, what it costs, and the maximum acceptable churn**
- Core message: churn removes the rationale before it removes the value; at ₹4,000 Cr no churn level is acceptable, so the answer is price and structure, not a tolerance.
- Bullets: (1) 30–45% of ARR = 50–75% of the top-4 book; banks are the natural leavers (RBI wants regulated entities insulated from private crypto); ZebPay is a founder relationship. (2) Grid 0–60%: effective multiple 18.2× → 45.5×; EPS ₹5.99 → ₹4.80; NPV −₹6,992 → −₹7,784 Cr; never breaks even. (3) Each 10 points costs ₹400 Cr at the headline multiple but ~₹130 Cr of DCF value. (4) Value-neutral price without the reserve: ~₹1,080 Cr at 0% churn, ~₹650 Cr at 37.5%. (5) Structural answer: consent gate 80%, earn-out floor 55%, sellers paid only for revenue that survives control.
- Exhibit: price × churn NPV heat-map (no reserve).
- Sources: `Churn`, `Earnout`.
- Why it matters: answers §5.2 directly, including the "what level of churn" question honestly.

**Slide 7 — Financing and EPS from ₹7.50: every mix is dilutive; no mix changes value**
- Core message: financing moves the pain between shareholders, the P&L and the balance sheet; it does not create value.
- Bullets: (1) Case mix: 1.02 Cr shares, cash ₹6,640 Cr, year-1 EPS ₹5.26 (−30%); reported incl. PPA ₹3.81; mechanical share-count-only ₹7.38 (−1.6%) hides 95% of the dilution. (2) All-equity ₹6.59 (−12%) but 3.4% of the company for a breakeven asset; all-debt cash leg ₹4.65 (−38%) at 3.8× EBITDA; all-cash ₹4.00 (−47%) with cash at ₹4,740 Cr. (3) Guardrails: max new debt ₹610 Cr; max cash deployable ₹3,740 Cr. (4) Like-for-like baseline with MDR is ₹8.58; the deal is −26% against it. (5) Recommended path: cash only, EPS ₹7.05 (−6%) in year 1, no shares, no debt; control tranche ≤ ₹500 Cr debt, earn-out in collared shares.
- Exhibit: EPS bar by mix with leverage/cash flags; year-1 bridge (7.50 → −0.12 → −1.45 → −0.67 → 5.26).
- Sources: `Financing`, `Accretion`, `Sources_Uses`.
- Why it matters: §5.3 asks for exactly this; the bridge shows why "1.6% dilution" is wrong.

**Slide 8 — PAT and FCF breakeven (Addendum 1)**
- Core message: full acquisition never breaks even; the recommended path breaks even only on the bull path, four years after exercise.
- Bullets: (1) Full acquisition: incremental PAT −₹138 Cr (Y1), −₹141 Cr (Y3); FCF −₹1,045 Cr (Y1); cumulative −₹12,052 Cr by Y10; PAT breakeven never (year 3 only if the MDR is wrongly credited). (2) Minority: associate income covers the foregone yield in year 7 (base), year 5 (bull); no cash yield until dividends or exit. (3) Hybrid, bull: control at ~₹1,700 Cr at end-Y1, trough EPS ₹5.84 in Y2, PAT and FCF breakeven in Y5; base: Y7, fails the five-year gate → Hold. (4) Even ₹50 Cr/yr of recurring reserve at control fails the gate in the base path.
- Exhibit: 10-year lines of incremental PAT and FCF for the three paths.
- Sources: `Deal_CF`, `Structures`.
- Why it matters: it is the Addendum's explicit requirement and the basis of Gate 4/5.

**Slide 9 — Alternatives compared: the trade-offs, not a scorecard**
- Core message: only the minority-plus-option keeps both unresolved risks (client response, reserve) off Paytm's balance sheet while securing access and blocking.
- Bullets: table of upfront cash, max commitment, churn and reserve exposure, EPS, NPV base/bull, cash at risk, control, blocking, reversibility, time to capability (from B15). Strongest case for and against each in one line.
- Exhibit: the comparison table.
- Sources: `Structures`.
- Why it matters: §5.1 asks for the choice and the reasons; judges look for honest cons.

**Slide 10 — Transaction architecture and negotiation**
- Core message: pay upfront for what is known; make sellers bear what is uncertain.
- Bullets: (1) Phase 1: 26% at ₹520–650 Cr, half primary; board seat, information rights, ROFR/ROFO, veto, retention pool, client charter. (2) Option: 74% × 10× audited ARR at exercise, cap ₹2,960 Cr, 55% upfront + 45% retention earn-out (zero below 55% retention), collared shares, 10% escrow, specific indemnities. (3) Schedule: at 0/20/30/45% churn the control total is ₹1,954/1,563/1,368/1,074 Cr (base ARR); grand total never above ₹4,000 Cr. (4) Why sellers say yes: liquidity now, anchor client, defined path, same wallet conflict with any other payments buyer; if they refuse the cap, 26% + ROFR only. (5) If the Board insists on 100%: ₹2,200 Cr upfront + ₹1,800 Cr earn-out + CP on written treatment; still not recommended because earn-outs fix price risk, not ownership risk.
- Exhibit: earn-out curve (retention → consideration).
- Sources: `Earnout`, `Sources_Uses`.
- Why it matters: converts the ₹4,000 Cr from a price into a cap.

**Slide 11 — Governance that clients can audit; regulatory sequence that RBI can accept**
- Core message: independence must be verifiable, and the group structure must keep the custodian outside the PA.
- Bullets: (1) Substance: information barriers, keys never on Paytm infrastructure, independent CCO/CISO reporting to Liminal's risk committee, annual attestation shared with clients, segregated desk on standard terms, client consent and portability rights. (2) Hold at One97/SPV, never in PPSL; no PA/escrow services to crypto flows; position as tokenisation/CBDC key management. (3) Sequence: FEMA/ODI route (three-year-profit test) → investing entity → RBI engagement before disclosure → written reserve treatment (CP) → licences/consents abroad (FSRA, VARA, MAS) → CCI analysis (26% + veto = control) → LODR disclosure at signing → FIU-IND/CERT-In/DPDP covenants. (4) At exercise: RBI treatment, CCI filing, controller approvals, ≥80% consents, refreshed audits. (5) Honest limit: governance converts churn into a measured consent rate; it cannot override RBI's stance on banks and crypto.
- Exhibit: timeline before signing / signing-to-closing / at exercise / post-close.
- Sources: `Regulatory`.
- Why it matters: §5.4; shows the team knows the real gates, not "RBI will approve".

**Slide 12 — Competitive dynamics: set the walk-away line now**
- Core message: Paytm is the highest-cost owner of Liminal; compete on structure, not price.
- Bullets: (1) The reserve is Paytm-specific; a foreign, non-RBI-regulated owner may not carry it; Mastercard has $11.3B of cash. (2) PhonePe inherits the same wallet conflict; it is loss-making with a paused IPO and no crypto appetite (external). (3) If they win: Paytm loses a partner, not the capability; 24–36 months and ~₹250 Cr to replace. (4) Reservation values: 100% with reserve = 0; without reserve ₹1,000–1,300 Cr (base), ~₹2,500 Cr (bull, contingent); 26% = ₹650 Cr. (5) If outbid on unconditional terms, let them; if the multiple compresses, Phase 1 is cash and −6% EPS is defensible as a 0.56%-of-market-cap option.
- Exhibit: buyer economics comparison (Paytm vs foreign owner: reserve yes/no; churn yes/yes; cost of capital).
- Sources: `Thresholds`, `Sources`.
- Why it matters: §5.5; it makes discipline explicit before the auction starts.

**Slide 13 — Decision framework, roadmap and triggers**
- Core message: Invest → Validate → Exercise / Hold / Exit, with quantified gates the Board can audit.
- Bullets: (1) Months 0–3: commercial agreement + exclusivity/ROFR; diligence; six CPs; close 26%. (2) Months 3–12: consents, RBI treatment, ARR (≥ ₹286 Cr = bull), margins, licences, incidents. (3) Months 12–24: exercise only if consents ≥ 80%, written nil reserve, then-DCF ≥ strike, breakeven ≤ 5 years, compliance clean; else hold indefinitely or exit via ROFO/tag. (4) Walk-away after signing: any reserve applied, RBI objection, top-4 termination, licence red flag. (5) Remediation ladder if churn > 45%: day-30 review and CEO outreach; day-90 governance reset funded from the sellers' earn-out at risk; day-180 exit process. Sunk cost never justifies escalation.
- Exhibit: decision tree with thresholds.
- Sources: `Thresholds`, `Scenarios`.
- Why it matters: §5.6 and Expected Output 8; the recommendation is conditional logic.

**Appendix A1 — Scenario tree and dominant-variable test** (base/upside/moderate/severe/break NPVs; tornado: drag → 0 +₹4,070 Cr, churn → 0 +₹494 Cr, drag → ₹1,250 Cr −₹2,713 Cr; conclusion: the reserve kills first, the price second, churn fourth). Source: `Scenarios`.

**Appendix A2 — Diligence request list and risk register** (ten decision-changing unknowns with tests and consequences; risk → financial impact → strategic impact → mitigant → contract → trigger for the reserve, churn, licences/incidents, ODI/FEMA, CCI, MDR durability, stock compression, founder dependence). Source: B20, B22.

---

# D. JUDGE Q&A

Format: Honest answer → Evidence → Weakness/limitation → Defensible trade-off.

**Valuation**

*Q1. Isn't 18× ARR normal for crypto infrastructure?*
Honest answer: it was, in 2021–22; it is not in 2026. Evidence: Fireblocks raised at ~80× ARR in January 2022; BitGo, the listed custody leader, trades at 5–11× recurring revenue and 55% below its January 2026 IPO price; Copper draws offers at ~10% of its 2022 valuation; Bitstamp closed at 2.1× net revenue. Weakness: private, strategic prices for scarce licensed rails (Bridge, BVNK) are undisclosed and may be high. Trade-off: we accept that a strategic buyer might pay more; we do not accept that Paytm, the highest-cost owner, should.

*Q2. Your DCF is 68% terminal value. Why trust it?*
Honest answer: don't trust the point estimate; trust the shape. Evidence: the grid shows no growth rate below 37% and no discount rate between 11% and 15% that reaches ₹4,000 Cr; the conclusion is the same at 11% (breakeven 31%) and 15% (42%). Weakness: a ten-year 40%+ compounder is possible in this sector. Trade-off: the option structure pays for that outcome if it appears, without paying for it now.

*Q3. Why 13%?*
Honest answer: a build-up (risk-free ~6.5% + β 1.0 × ERP 6.5%) for an all-equity infrastructure business, with the sector's risk placed in the cash-flow scenarios rather than inflated in the rate. Evidence: `Inputs`; sensitivity 11–15%. Weakness: a crypto-infra beta above 1 would raise the rate and lower value further. Trade-off: 13% is, if anything, generous to the sellers.

**Financing**

*Q4. All-equity is only −12% dilutive. Why not do that?*
Honest answer: because dilution is not value; the NPV is −₹7,487 Cr whatever the mix. Evidence: `Financing`, `Deal_CF`. Weakness: EPS is what shareholders react to (§3.3). Trade-off: we minimise EPS damage in the recommended path (−6%, cash-funded) because we minimise the cheque, not because we optimise the mix.

*Q5. Why not debt? You have ₹8,900 Cr of cash and almost no debt.*
Honest answer: debt-funding the cash leg takes gross debt/EBITDA to 3.8×, outside AA− territory, and the reserve then consumes the remaining cash within four years. Evidence: `Financing`, `Thresholds` (max new debt ₹610 Cr at 1.5×). Weakness: net cash would still be positive at close. Trade-off: we allow ≤ ₹500 Cr of debt only at control, when the business is consolidated and its cash flows are observable.

**Churn**

*Q6. What level of churn makes the deal unattractive?*
Honest answer: at ₹4,000 Cr, any level, including zero; churn is the fourth-ranked value driver behind the reserve, the price and growth. Evidence: NPV −₹2,923 Cr at 0% churn with no reserve; −₹6,992 Cr with it. Weakness: the answer sounds evasive. Trade-off: we give the churn tolerance as a function of price: ~₹1,080 Cr at 0%, ~₹650 Cr at 37.5% (no reserve), and we set the consent gate at 80% and the earn-out floor at 55%.

*Q7. Why would a minority not trigger the same churn?*
Honest answer: because no change of control occurs, so contracts are unaffected; but we do not assume it, we test it. Evidence: the case ties the churn to a full acquisition; consents are measured before any control. Weakness: a 26% holder with a board seat may still worry a bank. Trade-off: information barriers, no data or key access, and a minority-churn lever (0–20%) in the model; at 20% the minority NPV is −₹417 Cr, still bounded.

**Capital drag**

*Q8. Isn't ₹750 Cr a one-off capital lock-up rather than an annual drag?*
Honest answer: the case says "recurring annual FCF drag"; we model it as stated and show the alternatives. Evidence: three readings on `Capital_Drag`; even a one-off ₹750 Cr with a 4.5% after-tax carrying cost would cost ~₹34 Cr/yr, but that is not what the case says. Weakness: the mechanics are a case construct with no real-world analogue. Trade-off: the written treatment is a condition precedent precisely because the reading matters more than any other input.

*Q9. Doesn't the MDR offset it?*
Honest answer: it offsets 9% of it in cash and none of it in value, because Paytm earns the MDR anyway. Evidence: ₹115 Cr × 80% × 75% = ₹69 Cr; standalone EPS with MDR ₹8.58. Weakness: the MDR does add liquidity capacity. Trade-off: we show both views and use the like-for-like baseline.

**Strategic rationale**

*Q10. If custody is strategic, why not just buy it?*
Honest answer: because the strategic asset is the franchise, and control destroys 30–45% of it; the technology is buyable by contract. Evidence: case §3.1; global vendors serving India. Weakness: a contract gives no upside. Trade-off: the 26% stake and the option give upside; the premium paid for them is ₹150–350 Cr, disclosed.

*Q11. Is the opportunity large enough to justify leaving the core?*
Honest answer: large enough for a ₹665 Cr option, not for a ₹4,000 Cr control cheque. Evidence: RBI builds the tokenisation rails itself (UMI, Demat 2.0) and has asked lawmakers to insulate regulated entities from private crypto; the addressable role is key-management vendor to banks, not owner of the rails. Weakness: policy could turn friendlier (the Economic Survey signalled openness to a stablecoin framework). Trade-off: the option captures a friendlier regime without pre-paying for it.

**Governance**

*Q12. Isn't the ring-fence cosmetic?*
Honest answer: brand and directors are; data, key control, independent compliance reporting and client consent rights are not. Evidence: B17 table. Weakness: no governance overrides RBI's stance on banks and crypto. Trade-off: we make the consent rate the gate, not the governance promise.

**Regulation**

*Q13. What approvals do you actually need?*
Honest answer: for the minority, none from RBI as a licence matter, but a FEMA/ODI route (three-year-profit test), possibly a CCI filing (26% + veto = control), foreign controller approvals where Liminal is licensed, and a supervisory conversation with RBI that we would not skip. Evidence: `Regulatory` with sources and dates. Weakness: we have no counsel opinion; the ODI classification of crypto custody is open. Trade-off: we sequence the structural questions before the term sheet.

*Q14. The real Liminal's licences look thinner than the case says. Which do you use?*
Honest answer: the case's construct for modelling; the public record for diligence. Evidence: the case instructs it; the register findings are conditions precedent. Weakness: if the real facts prevailed, the minority premium would fall further. Trade-off: the commercial agreement comes first because it is the cheapest way to learn.

**Competitive dynamics**

*Q15. If PhonePe–Mastercard buys Liminal, haven't you lost?*
Honest answer: we lose a partner, not the capability, and they inherit the revolt and, for PhonePe, the same conflict. Evidence: B19. Weakness: a Mastercard-owned Liminal could become the tokenisation node for Indian banks. Trade-off: 26% + ROFR/ROFO + veto + call blocks the easy routes at 0.56% of market cap; beyond that, the auction is theirs.

*Q16. Would you match a higher bid?*
Honest answer: no on unconditional terms. Evidence: reservation values in `Thresholds`. Weakness: strategic regret is real. Trade-off: regret is cheaper than −₹7,487 Cr.

**Alternatives**

*Q17. Why not the JV?*
Honest answer: it avoids the reserve and the revolt but does not block the consortium, and its value is the capability a contract already gives. Evidence: illustrative JV NPV −₹284 Cr. Weakness: JV economics are assumption-heavy. Trade-off: it is the fallback if RBI applies a reserve at minority level.

*Q18. Why not walk away entirely?*
Honest answer: because the option is cheap relative to the cost of replacing an Indian-domiciled, FIU-registered partner and to the value of blocking, if diligence confirms the franchise. Evidence: minority NPV −₹348 Cr base vs walk-away −₹197 Cr build cost. Weakness: the ₹150 Cr difference is a judgement about option value. Trade-off: the Board is asked to approve an option premium, explicitly.

**Negotiation**

*Q19. Why would sellers accept a capped, growth-linked option?*
Honest answer: liquidity now, an anchor client, a defined path to the headline, and the same conflict with any other payments buyer; if they refuse, we hold 26% + ROFR. Evidence: `Earnout`. Weakness: they may demand a premium or a higher multiple. Trade-off: premium capped at ~3% of strike; multiple above ~11× and we let the option go.

*Q20. Why 10×?*
Honest answer: the listed custody leader's subscription multiple and a premium to FI software; below the ask, above the precedents. Evidence: `Comps`. Weakness: a number, not a law. Trade-off: tested 8–14×; at 14× the bull-path exercise is NPV −₹903 Cr, so the strike is a hard limit.

**Recommendation**

*Q21. You call it a recommendation but the base outcome is "Hold". Is that a decision?*
Honest answer: yes: it is a decision to pay ₹665 Cr for access, blocking and information, and to pay for control only on facts observed later. Evidence: B25 triggers. Weakness: the Board may want a definitive buy/no-buy. Trade-off: the definitive answer on 100% at ₹4,000 Cr is no; the conditional answer on control is the honest one.

*Q22. What would change your mind?*
Honest answer: a written RBI treatment of nil at control plus contracted consents ≥ 80% plus ARR ≥ ₹286 Cr at month 12 would make us exercise; a reserve at 26% or consents below 55% would make us exit; a seller demanding unconditional pricing above ₹1,300 Cr for 100% would make us walk. Evidence: `Thresholds`. Weakness: none; that is the framework. Trade-off: none.

---

*End of document. Companion workbook: `Paytm_Liminal_Deal_Model.xlsx`.*
