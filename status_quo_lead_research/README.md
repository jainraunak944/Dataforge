# Status Quo — US B2B SaaS founder lead research

Evidence-backed lead list of US B2B SaaS founders for Status Quo's LinkedIn
ghostwriting and founder-personal-branding service.

**Status: incomplete and resumable.** The deterministic stages (audit, normalization,
deduplication, prefilter) are finished over the full dataset. Web research covers part
of a 57,673-company queue. `outputs/08_run_summary.md` always carries the true
remaining count — see [Resuming](#resuming).

---

## Purpose

Turn a 173,119-row US software/SaaS company database into an outreach-ready list of
founders who (1) sit in Status Quo's target market, (2) can afford the service, (3) have
a founder or co-founder who can buy it, and (4) present a real founder-branding
opportunity. Score orders the list; it never caps it.

## Input

`data/us-software-saas-companies-cleaned.csv` — 173,119 rows, 27 source columns, UTF-8.

Delivered as ten byte-chunked parts, each repeating the header. `scripts/00_assemble.py`
reassembles them with a CSV parser into the canonical file and appends `source_part` and
`source_row_id` for provenance. The originals live in `data/raw_parts/` at mode 444 and
are never modified. `INTAKE.md` is the receipt with per-part checksums.

The free-text columns contain newlines inside quoted fields, so **every reader must use a
real CSV parser** — splitting on newlines corrupts records.

## Folder structure

```
status_quo_lead_research/
  scripts/          pipeline, numbered in run order
  logs/             run logs and research progress log
  cache/            reserved for HTTP cache (unused — see Known limitations)
  evidence/         reserved for stored evidence payloads
  checkpoints/      CSV checkpoint every 20 companies, DB backup every 100
  outputs/          all deliverable files
  data/             canonical CSV, raw parts, interim reports
  research_state.sqlite
  INTAKE.md         source-part receipt with checksums
  README.md
```

## Installation

Python 3.11+. `pip install pandas beautifulsoup4 lxml tldextract httpx`
(only `pandas` and `tldextract` are required for the deterministic stages).

## Run commands

```bash
cd status_quo_lead_research

python3 scripts/00_assemble.py          # parts -> canonical CSV
python3 scripts/01_audit.py             # -> outputs/00_data_audit.json
python3 scripts/01b_audit_summary.py    # -> outputs/00_data_audit_summary.md
python3 scripts/02_normalize_dedupe.py  # -> outputs/01_*.csv        (~3 min)
python3 scripts/03_prefilter.py         # -> outputs/02_*.csv        (~2 min)
python3 scripts/04_init_state.py        # load queue into SQLite (idempotent)
python3 scripts/06_export.py            # -> outputs/03..08
```

## Resuming

Research state lives in `research_state.sqlite`. Every company carries its own
`research_status`, `attempt_count` and timestamps, and each company is written in its own
transaction, so an interrupted run never corrupts state and never loses completed work.

```bash
# What is left, in priority order:
sqlite3 research_state.sqlite \
  "SELECT queue_rank, canonical_company_id, company_name, domain, research_priority
   FROM companies WHERE research_status='Pending'
   ORDER BY research_priority, queue_rank LIMIT 50;"

# Re-init is safe — existing rows keep their research state:
python3 scripts/04_init_state.py

# Record a researched batch (payload format in scripts/05_record.py docstring):
python3 scripts/05_record.py payload.json

# Re-export all deliverables at any point:
python3 scripts/06_export.py
```

`scripts/05_record.py` checkpoints a CSV every 20 completions, backs up the database
every 100, prints progress every 50 and a classification summary every 500.

## Filtering logic

### TAM definition (all mandatory)

US-headquartered · ~11–50 employees · active · for-profit · privately owned · genuine
B2B SaaS or software product · live product · sells to businesses · identifiable
founder/co-founder · credible web presence.

### Local prefilter gates

Five gates, each returning **retain / conditional / reject**. A company is rejected
locally only when a gate *clearly* fails. Anything uncertain goes into the research
queue, because losing a good company to stale vendor data costs more than researching a
borderline one.

| Gate | Retain | Conditional | Reject |
|---|---|---|---|
| US | `Country` resolves to United States | US territory; country blank; country foreign but locality names a US state | Country clearly foreign with no US location evidence |
| Employees | headcount **and** band both inside 11–50 | either inside; the two conflict; headcount 8–10 or 51–65; indeterminate | both clearly below 11 or both clearly above 50 |
| B2B SaaS | ≥1 strong signal or ≥2 weak signals | 1 weak signal | B2C-only, nonprofit, or agency/staffing industry with no SaaS signal |
| Company type | Privately Held | Partnership; missing; Self Owned at operating scale | Public, Government, Non Profit, Educational, Self Employed, Self Owned at individual scale |
| Ability to pay | revenue band 1M–5M, 5M–10M, 10M–25M, 25M–75M | 500K–1M; missing; implausibly large for the headcount | 0–500K with no funding, scale or growth signal to contradict it |

Keyword rejection is deliberately avoided: "consulting", "services" and "solutions" never
reject on their own, because SaaS companies routinely sell implementation alongside a real
product.

### Ability to pay

Never rests on the vendor revenue estimate alone. Funding, headcount, enterprise
customers, pricing motion, hiring and product maturity all count. Classified as
**Confirmed / Probable / Uncertain / Insufficient**; the qualified list takes Confirmed and
Probable only.

## Scoring

100 points: company and TAM fit 25 · ability to pay 20 · need for Status Quo 25 · founder
suitability 20 · timing 10. Penalties (existing ghostwriter, mature internal content team,
founder inactive 180d+, unresolved location or employee conflict, services-led, weak
personalisation) are applied after the base score and recorded individually. Scores are
clamped to 0–100.

**Hard disqualifiers override any score**: not US-headquartered, clearly <11 or >50
employees, not B2B SaaS, public company or subsidiary of one, closed/acquired/inactive, no
working product, no relevant founder, insufficient ability to pay, B2C-only, agency or
consultancy without a SaaS product, government/nonprofit/educational/self-employed.

### Priority tiers

A = 85–100 · B = 70–84 · C = below 70. **All three tiers ship.** Tier orders outreach; it
does not gate inclusion. There is no Top-N cap anywhere in the pipeline.

## Data-quality handling

The vendor data is not trustworthy field-by-field, and three defects drive real decisions:

1. **`JSON Country` is unusable.** It reports a US value for 98% of rows, including every
   one of the 10,266 rows whose `Country` column names a foreign country. Excluded from
   all filtering. `Country` is the primary location filter and is verified downstream.
2. **`Annual Revenue Hubspot` is `0` for all 173,119 rows.** No signal. Never read as
   evidence of no revenue.
3. **Mis-enriched LinkedIn pages — 12,005 rows, 6.9% of the dataset.** The vendor attached
   one company's LinkedIn page to thousands of unrelated domains: 5,573 distinct domains
   carry Lazada's page, name, country, headcount, founding year and description verbatim
   (this is also the source of the file's odd Singapore skew). Detected by checking whether
   a row's domain corroborates the LinkedIn identity attached to it.

   The repair matters in both directions. Left alone, 5,578 genuine candidates would have
   been rejected as Singaporean and 4,928 would have been accepted carrying Lazada's
   5,001–10,000 headcount. The dataset has two layers and only the LinkedIn-scraped one is
   corrupted: `Derived Description`, `Pattern Tags`, `SubIndustry` and the Clay revenue
   estimate stay per-domain and correct. So the pipeline clears the LinkedIn layer, keeps
   the domain layer, recovers a company name from the derived description (3,613) or the
   domain (8,392), and resets country and size to *unknown* — sending those companies to
   verification rather than judging them on another company's facts.

Employee fields conflict on 43,109 rows (25%). Both values are kept as independent
estimates, the conflict is recorded, and neither is silently preferred because it would
make a company qualify.

## Duplicate handling

Resolved in the brief's order, but only the identity-grade keys merge:

1. **Normalized domain** → merged. After excluding shared site-builder hosts (Yola,
   Leadpages and similar, where the registrable domain names the platform rather than the
   business), domains are effectively unique — one value repeats.
2. **Normalized LinkedIn slug** → merged, *after* mis-enriched rows are removed. This is
   the real duplication axis: 1,098 genuine clusters. Before the repair it looked like
   3,479 clusters with a largest cluster of 5,573; afterwards the largest is 11.
3. **Name + locality** and 4. **name + description overlap** → **not merged**. These
   collide on genuinely distinct companies sharing a name in one city, which is material
   uncertainty. They go to `outputs/01_possible_duplicates.csv` graded
   `likely_same_company` / `possible_same_company` / `probable_name_collision`, and their
   rows stay separate.

The surviving record in a merge is the most complete one; all source row IDs, merged
domains, merged names and field-level disagreements are recorded on the row.

## Research source hierarchy

Official company website → official announcement → public company LinkedIn → public
founder LinkedIn → official podcast/webinar/conference page → reputable business database
→ reputable news → search snippet only when nothing else is reachable.

## Evidence rules

Every material claim carries a source URL, source type, page title, access date, a short
summary, a confidence level and a **fact-or-inference** label, stored in the `evidence`
table and exported to `outputs/07_research_sources.csv`. One source never supports an
unrelated claim. Nothing is invented: unavailable facts are recorded as
`not established`, never guessed. Research confidence is High/Medium/Low, and only High
and Medium can qualify.

## LinkedIn limitations

**LinkedIn is not reachable from this environment**, so no founder profile could be opened
to count posts or inspect activity. Per the brief, this does not by itself fail a company.
Founder identity, title and role are established from official leadership pages,
announcements and interviews; LinkedIn-specific fields are marked `unverified` or
`Unknown - LinkedIn not inspectable`, and founder public-activity scores are held
conservatively rather than guessed.

Anyone resuming with LinkedIn access should re-run the founder-activity fields first: they
carry the largest block of unverified values and drive the content-gap classification and
25 of the 100 scoring points.

## Checkpoint and cache behaviour

Checkpoint CSV every 20 completions (`checkpoints/checkpoint_latest.csv` always points at
the newest), SQLite backup every 100 (`checkpoints/db_backups/`). Completed companies are
never re-researched. `fetch_cache` stores URL, access date, HTTP status and content hash;
it is currently unused because the environment blocks direct fetching.

## Output files

| File | Contents |
|---|---|
| `00_data_audit.json` / `.md` | Full audit: completeness, duplicates, country/employee/revenue conflicts, material issues |
| `01_deduplicated_companies.csv` | Every canonical company with normalized fields and merge provenance |
| `01_possible_duplicates.csv` | Graded duplicate clusters held for review, not merged |
| `02_prefiltered_research_queue.csv` | Every company selected for research, with gates, conflicts, preliminary score and priority |
| `02_locally_rejected.csv` | Every locally rejected company with gate and reason |
| `03_all_qualified_status_quo_companies.csv` | One row per qualified company — no row limit |
| `04_all_qualified_status_quo_founder_leads.csv` | One row per qualified founder — the outreach list, no row limit |
| `05_needs_verification.csv` | Promising companies with a named unresolved fact |
| `06_rejected_after_research.csv` | Rejected after research, with reason and evidence |
| `07_research_sources.csv` | One row per evidence source |
| `08_run_summary.json` / `.md` | Counts, three-way reconciliation, validation results |

The three largest intermediate tables (560 MB combined) are gitignored; they regenerate
from the source CSV and carry the third-party database content.

## Known limitations

- **Outbound web access is restricted.** Direct HTTP from Python is refused by the egress
  proxy, and `WebFetch` fails on company domains. Research runs through search tools only,
  which means no page-by-page website inspection (pricing, careers, team, case-study
  pages) and roughly two orders of magnitude less throughput than a fetch-based harness.
  Allowlisting outbound HTTP would let `scripts/` fetch and parse sites directly.
- **LinkedIn is unreachable**, so all founder-activity fields are unverified. This is the
  single biggest gap in the founder-level output.
- Employee counts from aggregators disagree routinely; several companies sit at 51–61
  against a 50 ceiling and are held in Needs Verification rather than force-decided.
- Revenue bands are vendor estimates throughout and are never reported as confirmed.
- The queue is far larger than one session can research; the remaining count is reported
  honestly rather than presented as a finished list.

## Changing the definitions

| To change | Edit |
|---|---|
| Source CSV | Replace `data/raw_parts/`, re-run `00_assemble.py` onward |
| Employee range | `TARGET_EMP_LOW` / `TARGET_EMP_HIGH` in `scripts/common.py`, and `gate_employees` in `scripts/03_prefilter.py` |
| Geography | `US_NAMES`, `US_TERRITORIES`, `US_STATE_ABBR`, `US_STATE_NAMES` in `scripts/common.py`, and `gate_us` in `scripts/03_prefilter.py` |
| Revenue preferences | `AUTO_REV` / `COND_REV` and `gate_pay` in `scripts/03_prefilter.py`; band boundaries in `_REV_MAP` in `scripts/common.py` |
| Scoring weights | `preliminary_score` in `scripts/03_prefilter.py` (local priority) and the recorded component scores |
| Priority tier cutoffs | `tier()` in `scripts/06_export.py` |

### Refreshing only stale leads

```bash
sqlite3 research_state.sqlite \
  "UPDATE companies SET research_status='Pending'
   WHERE last_completed_utc < '2026-03-01';"
python3 scripts/06_export.py
```

Then re-run research over the reopened rows. Rerunning research later works the same way:
reset the rows you want revisited to `Pending` and continue.

## Compliance

Public, professional, business-relevant information only. No authentication bypassed, no
CAPTCHAs solved, no access controls evaded, no paid data purchased, no personal email
addresses guessed, and no contact made with any lead. This is research and list building
only.
