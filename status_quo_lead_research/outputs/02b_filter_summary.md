# Strict second-stage local qualification

Generated 2026-09-14T10:34:00Z

The first prefilter was deliberately broad, to avoid losing good companies to stale vendor data. At 57,673 companies it is too large to research one search at a time. This second stage is deliberately narrow: it uses **only existing dataset fields** — no new web research — to isolate the companies with the highest prior of qualifying.

## Reconciliation

| Bucket | Companies |
|---|---|
| Already researched (preserved untouched) | 80 |
| **Strict high-probability queue** | **9,255** |
| Headcount verification | 13,245 |
| Affordability exception | 357 |
| Newly rejected | 34,736 |
| **Sum** | **57,673** |
| Old queue | 57,673 |

**Reconciliation balances: yes** — every company from the old queue lands in exactly one bucket, and the buckets sum to 57,673.

Precedence is `already_researched` → `newly_rejected` → `headcount_conflict` → `affordability_exception` → `strict`. A hard failure outranks a soft flag, so nothing that fails a mandatory rule can end up in a verification queue instead of being rejected.

The strict queue is a **6.2x reduction** on the old queue. At the research throughput this environment allows, that is the difference between an impossible target and a long but finite one.

## What the strict queue contains

| Estimated revenue band | Companies |
|---|---|
| 1M-5M | 8,867 |
| 5M-10M | 255 |
| 10M-25M | 125 |
| 25M-75M | 8 |

| Company Type | Companies |
|---|---|
| Privately Held | 8,720 |
| Partnership | 302 |
| (blank) | 137 |
| Self Owned | 96 |

| Business Type | Companies |
|---|---|
| B2B | 8,200 |
| B2B,B2C | 608 |
| (blank) | 430 |
| B2B, B2C | 16 |
| Unknown | 1 |

Ordering follows the brief's revenue scoring rather than raw band size: 5M–10M first (10 points), then 10M–25M, then 1M–5M (8 points), then 25M–75M (7 points), with the preliminary score breaking ties inside each band.

## Rules applied

| # | Rule | Effect |
|---|---|---|
| 1 | `Country` must equal United States; `JSON Country` never consulted | The enrichment repair from the first pass is preserved, so the 12,005 corrupted rows still carry a cleared country and cannot pass |
| 2 | Headcount 11–50; missing or zero accepted only with band `11-50 employees`; contradictions diverted | 13,257 companies routed to the headcount queue rather than guessed either way |
| 3 | Privately Held prioritised; Public, Government, Non Profit, Educational, Self Employed excluded; Self Owned excluded at individual scale; blank kept only on strong operating evidence | |
| 4 | B2B evidence **and** SaaS/cloud/enterprise-software/platform/subscription evidence both required; agencies, consultancies, custom development, outsourcing, staffing, hardware-first and B2C excluded | The single largest filter — a conjunction, where the first pass accepted either signal alone |
| 5 | Revenue bands 1M–5M, 5M–10M, 10M–25M, 25M–75M retained; 500K–1M and missing only with $1M+ funding or strong operating scale; 0–500K only with meaningful funding; `Annual Revenue Hubspot` ignored (zero for all 173,119 rows) | |
| 6 | Removed: invalid domains, shared site-builder hosts, duplicate domains, duplicate LinkedIn slugs, names indicating prior acquisition, corrupted enrichment-layer rows | |

### Validation of the strict queue

Every rule was re-checked against the written file rather than trusted from the code path:

| Check | Failures |
|---|---|
| Rows violating the employee rule | 0 |
| Rows with zero/missing headcount and no `11-50 employees` band | 0 |
| Rows where Country is not United States | 0 |
| Rows with an excluded Company Type | 0 |
| Rows outside the retained revenue bands | 0 |
| Rows missing either a B2B or a SaaS signal | 0 |
| Duplicate domains | 0 |
| Duplicate LinkedIn slugs | 0 |

## Why companies were newly rejected

Each company is counted once, under its first failure.

| Primary rejection reason | Companies |
|---|---|
| no SaaS / cloud / enterprise-software / platform / subscription evidence | 9,833 |
| no B2B evidence in Business Type, Pattern Tags or description | 4,429 |
| corrupted LinkedIn/company layer - name, HQ, size and description were cleared by the enri | 2,883 |
| Industry 'IT Services and IT Consulting' is an excluded services/agency category | 2,617 |
| Business Type is B2C only | 1,874 |
| Industry 'Advertising Services' is an excluded services/agency category | 1,073 |
| revenue (missing) with no funding of $1M+ and no strong operating-scale evidence | 867 |
| Industry 'Information Technology and Services' is an excluded services/agency category | 809 |
| description reads as hardware-first | 656 |
| description reads as consulting / custom development / outsourcing / staffing | 643 |
| employee size fails the strict rule (headcount 1, band '51-200 employees') | 512 |
| Industry 'Business Consulting and Services' is an excluded services/agency category | 446 |
| Industry 'Marketing Services' is an excluded services/agency category | 385 |
| employee size fails the strict rule (headcount 2, band '51-200 employees') | 370 |
| employee size fails the strict rule (headcount 8, band '2-10 employees') | 363 |
| employee size fails the strict rule (headcount 10, band '2-10 employees') | 360 |
| employee size fails the strict rule (headcount 9, band '2-10 employees') | 355 |
| employee size fails the strict rule (headcount 3, band '51-200 employees') | 313 |
| Industry 'Venture Capital and Private Equity Principals' is an excluded services/agency ca | 291 |
| employee size fails the strict rule (headcount 4, band '51-200 employees') | 257 |

The two largest groups are the business-model conjunction doing exactly what it was meant to. Requiring B2B evidence **and** software-product evidence together — rather than either alone — removes 14,273 companies that the broad pass had carried on a single weak signal.

## Verification queues

| Headcount conflict shape | Companies |
|---|---|
| headcount inside 11-50, band outside | 3,601 |
| band says 11-50, headcount outside | 9,644 |

13,245 companies have a numeric headcount that contradicts their size band. Neither value is preferred, because preferring whichever one qualifies the company is exactly the bias the brief warns against. The larger group — band says 11–50 while the headcount says otherwise — is mostly rows whose headcount is 1 or 0 against a populated band, so a single current headcount check would resolve most of this queue cheaply.

| Affordability exception revenue | Companies |
|---|---|
| 0-500K | 63 |
| 500K-1M | 40 |
| (missing) | 254 |

357 companies were retained on funding or operating scale rather than a retained revenue band. They are held separately because the exception is a judgement about the vendor estimate being stale, not a confirmed ability to pay.

## Preserved from the previous run

The 80 already-researched companies were excluded from re-evaluation entirely — their records, founders, evidence and classifications are untouched. They appear in the reconciliation as their own bucket and nowhere else.

---

Generated by `scripts/07_strict_filter.py` + `scripts/07b_strict_summary.py`. No web research was performed in this stage.