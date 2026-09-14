# Data audit — US software / SaaS company database

Generated 2026-09-14T09:02:29Z · research date 2026-09-14

## Input

| Property | Value |
|---|---|
| File | `us-software-saas-companies-cleaned.csv` |
| Path | `/home/user/Dataforge/status_quo_lead_research/data/us-software-saas-companies-cleaned.csv` |
| Size | 263,947,553 bytes |
| SHA-256 | `c47bd9c3e2b884860954bc57b5f391ee7a4edf1083b68e2cfefa3516b03063ef` |
| Encoding | utf-8 |
| Rows | 173,119 |
| Source columns | 27 |
| Assembled from | 10 uploaded parts |

The source arrived as ten byte-chunked parts, each repeating the 27-column header. They were reassembled in part order with a CSV parser (free-text columns embed newlines, so line-based concatenation would corrupt records). The reassembled row count is **173,119**, an exact match for the count stated in the brief, with zero width-malformed rows. Two provenance columns (`source_part`, `source_row_id`) were appended; the originals are unmodified and held read-only.

## Completeness

| Column | Missing | Missing % |
|---|---|---|
| `Specialties` | 64,527 | 37.27% |
| `Business Type` | 48,195 | 27.84% |
| `SubIndustry` | 46,720 | 26.99% |
| `Derived Industry` | 46,664 | 26.95% |
| `Pattern Tags` | 46,661 | 26.95% |
| `Scale Scope` | 46,661 | 26.95% |
| `Derived Description` | 46,659 | 26.95% |
| `Founded` | 38,946 | 22.50% |
| `Annual Revenue Clay` | 19,226 | 11.11% |
| `Company Type` | 11,478 | 6.63% |
| `JSON Industry` | 8,171 | 4.72% |
| `JSON Employee Size Range` | 5,966 | 3.45% |
| `Total Funding Range` | 3,931 | 2.27% |
| `JSON Country` | 3,596 | 2.08% |
| `Industry` | 2,002 | 1.16% |
| `Locality` | 1,340 | 0.77% |
| `Employee Size Range` | 940 | 0.54% |
| `Slug` | 761 | 0.44% |
| `Country` | 567 | 0.33% |
| `Domain` | 0 | 0.00% |
| `Company Name` | 0 | 0.00% |
| `LinkedIn Company URL` | 0 | 0.00% |
| `Employee Headcount` | 0 | 0.00% |
| `JSON Employee Headcount` | 0 | 0.00% |
| `Description` | 0 | 0.00% |
| `Annual Revenue Hubspot` | 0 | 0.00% |
| `Follower Count` | 0 | 0.00% |

## Identifiers and duplicates

| Key | Unique values | Values appearing >1× | Excess rows |
|---|---|---|---|
| Domain (normalized) | 173,118 | 1 | 1 |
| LinkedIn company slug | 160,322 | 3,479 | 12,797 |
| Company name (normalized) | 157,637 | 5,311 | 15,481 |

Every row carries a domain and a LinkedIn URL, and all 173,119 LinkedIn URLs parse to a slug. Domains are effectively unique: after excluding shared site-builder hosts (Yola, Leadpages and similar, where the registrable domain names the platform rather than the business), just 1 domain value repeats. 

**The real duplication axis is the LinkedIn company page.** 3,479 slugs appear on more than one row, covering 16,276 rows — 12,797 of them redundant. These are typically one company reached through several domains. Name-based collisions are looser still and include genuinely distinct companies that share a name, so name matching is only ever used together with locality.

### Suspected duplicate clusters

| Cluster type | Count |
|---|---|
| Domain clusters | 1 |
| LinkedIn slug clusters | 3,479 |
| Name + locality clusters | 3,550 |
| Rows in name+locality clusters | 16,424 |

## Country — the headline data-quality failure

| `Country` resolves to | Rows | Share |
|---|---|---|
| us | 162,276 | 93.74% |
| foreign | 10,266 | 5.93% |
| unknown | 567 | 0.33% |
| us_territory | 10 | 0.01% |

**`JSON Country` is unusable as location evidence.** It reports a US value for 169,488 rows (97.9%). That includes **every one of the 10,266 rows whose `Country` column names a foreign country** — the column labels essentially the entire file United States regardless of the underlying record. It is excluded from all filtering.

`Country` itself mixes full names with ISO-3166 alpha-2 codes in mixed case (`PK`, `TW`, `am`, `cl`), which normalization resolves. The largest foreign group is Singapore (5,623 rows), conspicuous in a file labelled as US companies.

Top countries after normalization:

| Country | Rows |
|---|---|
| United States | 162,276 |
| Singapore | 5,623 |
| Israel | 962 |
| Canada | 594 |
| (blank) | 567 |
| United Kingdom | 551 |
| India | 439 |
| Germany | 289 |
| Australia | 142 |
| France | 141 |
| China | 123 |
| Netherlands | 87 |

## Employees

| Numeric headcount | Rows |
|---|---|
| 1-10 | 110,776 |
| 11-50 | 32,332 |
| 51-200 | 11,458 |
| 201-1000 | 5,363 |
| 1001+ | 9,692 |

| `Employee Size Range` | Rows |
|---|---|
| 2-10 employees | 78,470 |
| 11-50 employees | 49,262 |
| 51-200 employees | 16,587 |
| Self-employed | 10,480 |
| 5,001-10,000 employees | 6,090 |
| 201-500 employees | 4,966 |
| 1,001-5,000 employees | 3,243 |
| 501-1,000 employees | 2,100 |
| 10,001+ employees | 975 |
| (blank) | 940 |
| 0-1 employees | 6 |

**43,109 rows (24.9%) have a numeric headcount that contradicts the size band**, and 3,498 rows report headcount 0. Both fields are treated as independent estimates: where they disagree the row is retained, the conflict is recorded, and verification is required before the company can qualify. Neither value is silently preferred because it would make a company fit.

| Preliminary 11-50 fit (either estimate) | Rows |
|---|---|
| below | 88,087 |
| in_range | 60,677 |
| above | 24,355 |

## Revenue and funding

| `Annual Revenue Clay` (estimate) | Rows |
|---|---|
| 0-500K | 68,435 |
| 1M-5M | 52,315 |
| (blank) | 19,226 |
| 10M-25M | 16,399 |
| 500K-1M | 7,625 |
| 25M-75M | 3,965 |
| 5M-10M | 2,761 |
| 75M-200M | 1,295 |
| 200M-500M | 426 |
| 1B-10B | 354 |
| 500M-1B | 291 |
| 10B-100B | 25 |
| 100B-1T | 2 |

**`Annual Revenue Hubspot` is `0` for all 173,119 rows.** It carries no information and is never read as evidence that a company has no revenue. `Annual Revenue Clay` is an estimate used for preliminary filtering and priority only; it is never reported as confirmed revenue.

| `Total Funding Range` | Rows |
|---|---|
| Funding unknown | 154,494 |
| Under $1M | 4,372 |
| (blank) | 3,931 |
| $1M - $5M | 3,927 |
| $10M - $25M | 2,124 |
| $5M - $10M | 1,835 |
| $25M - $50M | 1,073 |
| $50M - $100M | 682 |
| $100M - $250M | 475 |
| $250M+ | 206 |

154,494 rows are `Funding unknown`, so absence of funding data never rejects a company on its own.

## Classification fields

| `Business Type` | Rows |
|---|---|
| B2B | 97,935 |
| (blank) | 48,195 |
| B2C | 14,830 |
| B2B,B2C | 8,911 |
| Nonprofit | 2,541 |
| Unknown | 517 |
| B2B, B2C | 188 |
| B2G | 2 |

| `Company Type` | Rows |
|---|---|
| Privately Held | 122,589 |
| (blank) | 11,478 |
| Self Owned | 10,486 |
| Partnership | 10,221 |
| Public Company | 9,424 |
| Self Employed | 4,603 |
| Non Profit | 3,252 |
| Educational | 942 |
| Government Agency | 124 |

Top industries:

| `Industry` | Rows |
|---|---|
| Software Development | 64,808 |
| Technology, Information and Internet | 14,035 |
| IT Services and IT Consulting | 10,656 |
| Advertising Services | 6,968 |
| Information Technology and Services | 5,068 |
| Financial Services | 4,050 |
| Hospitals and Health Care | 3,654 |
| Marketing Services | 3,259 |
| Business Consulting and Services | 2,979 |
| Telecommunications | 2,871 |
| Computer and Network Security | 2,222 |
| (blank) | 2,002 |
| Appliances, Electrical, and Electronics Manufacturing | 1,739 |
| Technology, Information and Media | 1,577 |
| Design Services | 1,525 |
| Venture Capital and Private Equity Principals | 1,437 |
| Information Services | 1,431 |
| Wellness and Fitness Services | 1,414 |
| E-Learning Providers | 1,219 |
| Transportation, Logistics, Supply Chain and Storage | 1,030 |

## Founded year and followers

| Founded | Rows |
|---|---|
| pre-1990 | 6,213 |
| 1990-1999 | 8,640 |
| 2000-2009 | 20,428 |
| 2010-2014 | 25,400 |
| 2015-2019 | 32,845 |
| 2020-2026 | 40,573 |

39,020 rows have no parseable founding year (range 1819–2026).

| LinkedIn followers | Rows |
|---|---|
| 0-49 | 64,773 |
| 50-199 | 30,846 |
| 200-1999 | 42,415 |
| 2000-19999 | 21,375 |
| 20000+ | 13,710 |

## Malformed and unusable records

| Problem | Rows |
|---|---|
| Missing company name | 0 |
| Missing domain | 0 |
| Missing LinkedIn URL | 0 |
| No usable identifier at all | 0 |
| Width-malformed rows at assembly | 0 |

## Material issues carried into the pipeline

**1. JSON Country is unusable as location evidence**  
JSON Country reports a US value for 169,488 of 173,119 rows (97.9%), including 10,266 rows whose Country column names a foreign country.  
*Handling:* Country is the primary filter; JSON Country is never used as proof of US HQ.

**2. Annual Revenue Hubspot is entirely zero**  
All 173,119 rows contain 0. The column carries no signal.  
*Handling:* Excluded from all filtering; never read as evidence of zero revenue.

**3. Total Funding Range is mostly unknown**  
154,494 rows are 'Funding unknown'.  
*Handling:* Absence of funding data never rejects a company on its own.

**4. Singapore over-represented for a US dataset**  
5,623 rows are Singapore-registered, the second largest country group, despite the file being labelled US companies.  
*Handling:* Rejected at the local US filter unless other evidence indicates a US HQ.

**5. Employee fields disagree**  
43,109 rows have a numeric headcount that contradicts the size band; 3,498 rows have headcount 0.  
*Handling:* Both estimates retained, conflict flagged, verification required before qualifying.

**6. Most rows are outside the target employee band**  
78,470 rows are 2-10 employees and 10,480 are Self-employed.  
*Handling:* Filtered at Stage 4; borderline and conflicting cases are researched, not discarded.

---

Source file unmodified throughout. Generated by `scripts/01_audit.py` + `scripts/01b_audit_summary.py`.