# Stage 1 handoff — existing qualified founder contacts

Generated 2026-09-14T10:56:02Z. Read-only export. No company was researched, re-scored, reclassified or removed to produce it.

## Headline counts

| Metric | Value |
|---|---|
| Founder contacts exported | **81** |
| Unique companies | **51** |
| Companies contributing more than one contact | 26 |
| Most contacts from a single company | 3 |
| Evidence rows underpinning the export | 289 |

The expected total of 81 is confirmed exactly. No discrepancy had to be reconciled and no contact was invented, duplicated or dropped to reach the number.

## Count by priority

| Priority | Contacts | Band |
|---|---|---|
| Priority A | 13 | 85-100 under the tiers recorded during research |
| Priority B | 58 | 70-84 |
| Priority C | 10 | below 70 |
| Needs Verification | 0 | see the note below |
| **Total** | **81** |  |

Score range across all 81 contacts: **66–91**.

**There are no Needs Verification contacts to separate out.** All 81 founder records in the database belong to companies classified Qualified. The 18 Needs Verification companies never had founder rows created, because founders were only recorded once a company cleared qualification. Section 4 of the requested ordering is therefore legitimately empty rather than omitted — those 18 companies are listed with their specific unresolved blocker in `outputs/05_needs_verification.csv`, and several name their founders in the research notes.

## LinkedIn verification status

| Status | Contacts | Share |
|---|---|---|
| Founder LinkedIn URL captured | 8 | 10% |
| Founder LinkedIn URL still `unverified` | 73 | 90% |
| Founder LinkedIn *activity* verified | 0 | 0% |

This is the single biggest gap in the file and it is an environment limitation, not an oversight. **LinkedIn is not reachable from the research environment**, so no profile could be opened to count posts, read a feed or confirm a headline. Where a profile URL appears it was recovered from a search result, so the URL is evidenced but its contents are not.

Every `founder_content_activity`, `content_gap` and `status_quo_need` value is therefore **inference from off-LinkedIn evidence** — podcast appearances, bylined articles, Forbes council profiles, conference listings — not observation of posting behaviour. The contacts with a captured URL are the cheapest to verify manually first:

| Founder | Company | Priority | Score | Profile URL |
|---|---|---|---|---|
| Grant Drzyzga | Revela | A | 86 | https://www.linkedin.com/in/grant-drzyzga-5a017047/ |
| Richy Glassberg | SafeGuard Privacy | A | 86 | https://www.linkedin.com/in/richy-glassberg-49a915/ |
| Jen Grogono | uStudio | B | 84 | https://www.linkedin.com/in/jengrogono/ |
| Sheila Talton | Gray Matter Analytics | B | 81 | https://www.linkedin.com/in/sheila-talton-8b295/ |
| Guilherme Cerqueira | Worthix | B | 80 | https://www.linkedin.com/in/guicerqueira (slug evidenced via post URL; profile not inspectable) |
| Kevin Fu | Repool | B | 76 | https://www.linkedin.com/in/kevinfu93/ |
| Ryan Arnett | Videate | B | 75 | https://www.linkedin.com/in/ryan-arnett-37b9196/ |
| Jared Broad | QuantConnect | B | 72 | https://www.linkedin.com/in/jaredbroad/ |

## Affordability evidence strength

| Affordability evidence | Contacts | Share |
|---|---|---|
| Strong — ability to pay Confirmed | 63 | 78% |
| Weaker — Probable, resting on funding or scale rather than revenue | 18 | 22% |

A Confirmed rating required at least one of: estimated or reported revenue of $1M+, funding of $1M+ alongside an active product, a credible enterprise customer base, or clear high-ticket pricing. Probable means the company looks able to pay on operating signals but no single hard figure was established. Nothing in this file rests on the vendor `Annual Revenue Hubspot` field, which is zero for all 173,119 source rows and carries no information.

Contacts whose affordability is Probable rather than Confirmed:

| Founder | Company | Priority | Score | Evidence |
|---|---|---|---|---|
| Steve S. Kim | Valer | B | 82 | Probable: Bootstrapped and operating since 2012 with health-system customers on recurring contracts; sustained |
| Sheila Talton | Gray Matter Analytics | B | 81 | Probable: Operating since 2013 with payer and provider clients on recurring analytics contracts, and a newly a |
| Matthew Player | Zoneomics | B | 81 | Probable: 25 employees with blue-chip clients (Cushman & Wakefield, Stanford University, Crexi, Sidewalk Labs) |
| Chelsea Lamego | FundMiner | B | 80 | Probable: $4.22M raised across 7 investors with 29 employees; universities and community foundations are slow  |
| Kevin Fu | Repool | B | 76 | Probable: YC S21 with a $3.7M seed from Canaan, Matrix and Global Founders Capital; fund administration carrie |
| Ryan Arnett | Videate | B | 75 | Probable: Multiple institutional investors including S3 Ventures; enterprise SaaS customers using video automa |
| Archer Chiang | Giftpack | B | 74 | Probable: $4.3M raised with enterprise customers including Google, J.P. Morgan Chase, Meta and Zappos; corpora |
| Matthew Smith | Truss | B | 73 | Probable: Institutional backing from General Catalyst, American Express Ventures and Balderton; construction p |
| Wias Issa | Ubiq Security | B | 73 | Probable: $6.4M seed with an exceptional early customer list - US Army, Department of Homeland Security, Veriz |
| Dan Ciprari | Pointivo | B | 72 | Probable: $8.38M raised with institutional backing; enterprise buyers in insurance, telecom, solar and energy  |
| Jared Broad | QuantConnect | B | 72 | Probable: Operating since 2011 with a large paying user base and institutional tier; capital-efficient at only |
| Mike Preuss | Visible.vc | B | 72 | Probable: 2,000+ paying businesses, documented 80% growth in one year without burning capital, established pro |
| Marty Staszak | Valer | B | 71 | Probable: Bootstrapped and operating since 2012 with health-system customers on recurring contracts; sustained |
| Justin Carrao | Repool | B | 70 | Probable: YC S21 with a $3.7M seed from Canaan, Matrix and Global Founders Capital; fund administration carrie |
| Dave Gullo | Videate | B | 70 | Probable: Multiple institutional investors including S3 Ventures; enterprise SaaS customers using video automa |
| Habib Fathi | Pointivo | C | 68 | Probable: $8.38M raised with institutional backing; enterprise buyers in insurance, telecom, solar and energy  |
| Alejandro Stevenson-Duran | FundMiner | C | 67 | Probable: $4.22M raised across 7 investors with 29 employees; universities and community foundations are slow  |
| Nick Addison | Truss | C | 67 | Probable: Institutional backing from General Catalyst, American Express Ventures and Balderton; construction p |

## Discrepancies

### 1. Database, CSV outputs and run summary agree

| Metric | Database | Run summary | This export | Result |
|---|---|---|---|---|
| Qualified companies | 51 | 51 | 51 | match |
| Founder contacts | 81 | 81 | 81 | match |
| Needs Verification | 18 | 18 | n/a | match |
| Rejected after research | 14 | 14 | n/a | match |

No reconciliation was needed.

### 2. Scoring bands differ between this file and the Stage 2 specification

This is the one material discrepancy and it needs a decision from you.

These 81 contacts were scored and tiered during research using **A ≥ 85, B 70–84, C < 70**. The Stage 2 brief specifies **A 80–100, B 65–79, C 50–64**. I have preserved the recorded tiers exactly, because Stage 1 instructs that existing research must not be re-scored.

If the Stage 2 bands were applied to these same unmodified scores, **17 contacts currently marked Priority B would become Priority A** (13 → 30), and the 10 Priority C contacts would all become Priority B, leaving no Priority C at all.

The contacts that would move from B to A:

| Score | Founder | Company |
|---|---|---|
| 84 | Ashish Srimal | Ratio |
| 84 | Sindre Haaland | SalesScreen |
| 84 | Ankit Saxena | Thena |
| 84 | Jen Grogono | uStudio |
| 83 | Marlon Misra | Assembly |
| 83 | Nick Bonfiglio | Syncari |
| 83 | Dirck T. Schou Jr. | Taqtile |
| 82 | Rich Cannon | Rali |
| 82 | Steve S. Kim | Valer |
| 82 | Tal Sholklapper | Voltaiq |
| 81 | Sheila Talton | Gray Matter Analytics |
| 81 | Brian Hassan | Kickfin |
| 81 | Andrew Sweeney | ReadyWorks |
| 81 | Matthew Player | Zoneomics |
| 80 | Chelsea Lamego | FundMiner |
| 80 | Mike Durham | Peachjar |
| 80 | Guilherme Cerqueira | Worthix |

**I have not applied this.** Say the word and I will re-band the existing contacts to the Stage 2 scale so the whole list is consistent when new batches arrive. Left as is, contacts researched before and after Stage 2 will not be directly comparable on priority.

### 3. Company-level tiers are not the same thing as contact-level tiers

Earlier run summaries quoted company-level tier counts. This file is contact-level, and one company can contribute several contacts — 26 of the 51 companies do, up to 3 contacts each. Contact counts by tier will therefore never match company counts by tier.

## Files created

| File | Contents |
|---|---|
| `outputs/00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv` | 81 contacts, all priorities, outreach order |
| `outputs/00_PRIORITY_A_CONTACTS.csv` | 13 contacts, highest score first |
| `outputs/00_PRIORITY_B_CONTACTS.csv` | 58 contacts, highest score first |
| `outputs/00_EXISTING_81_HANDOFF.md` | this document |

Generated by `scripts/08_stage1_handoff.py` and `scripts/08b_handoff_doc.py`. Both are read-only over the research state and can be re-run at any time without side effects.

## Validation

| Check | Failures |
|---|---|
| Duplicate founder LinkedIn URLs | 0 |
| Duplicate founder + company pairs | 0 |
| Blank company names | 0 |
| Qualified companies with no founder | 0 |
| Priority A contacts without a qualification reason | 0 |
| Generic or missing outreach angles | 0 |
| Contacts with no evidence URL | 0 |
| Empty cells (all use `unverified` instead) | 0 |
| Contacts silently removed | 0 |

Every factual claim in the file either carries an evidence URL or reads `unverified`. Revenue figures are labelled as vendor or third-party estimates throughout and are never presented as confirmed.

## Who to approach first

My recommendation is not simply the top 10 by score. Two of the highest scorers are harder first conversations than slightly lower scorers with a live hook, and the ordering below weights **a specific, checkable reason to make contact this month** alongside the score.

Approach in this order:

| # | Founder | Title | Company | Score | Trigger |
|---|---|---|---|---|---|
| 1 | Tanya Bakalov | Founder & CEO | HelloTeam | 91 | Inc 2025 Female Founders 500 listing and the $10M Grand Oaks rou |
| 2 | Ryan Keane | Founder & Chief Executive Officer | KORIO | 89 | Series A funding round |
| 3 | Sara Well | Founder & CEO | Dropstat | 88 | Podcast appearance - 'Nurse Builds Healthcare SaaS and Saves Mor |
| 4 | Steve Helmbrecht | Co-Founder, President & CEO | Treasury4 | 88 | $20M Series A |
| 5 | Ben Turner | Founder & CEO | VERITUITY | 88 | Confidence-based verification product launch, March 2026 |
| 6 | Max Rudman | Chairman & CEO, Co-Founder | Prodly | 87 | Appointment as Chairman and CEO of Prodly |
| 7 | Grant Drzyzga | Founder & CEO | Revela | 86 | Series A round |
| 8 | Richy Glassberg | Founder & CEO | SafeGuard Privacy | 86 | $3.6M round and Adweek coverage |
| 9 | Brandon Newman | Co-Founder & CEO | Xevant | 86 | Series A funding round and a major platform enhancement launch ( |
| 10 | Shin Kim | Founder | Eraser | 85 | AI diagramming adoption |

Before contacting any of them, do the one manual check this environment could not: open the founder's LinkedIn profile and confirm the posting pattern the `content_gap` column infers. That check takes a minute per contact and is the difference between a personalised opening and an embarrassing one — the angle for several of these contacts asserts that they are *not* publishing consistently, which is exactly the claim that would be wrong if they started last month.

---

Stage 2 has not been started. No queue has been imported, no new company researched and no Clay credits consumed. Awaiting `START NEXT BATCH`.