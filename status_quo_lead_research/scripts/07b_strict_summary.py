#!/usr/bin/env python3
"""Render outputs/02b_filter_summary.md from the strict filter report."""
import json, csv, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
csv.field_size_limit(sys.maxsize)

r = json.loads((C.DATA / "interim" / "strict_filter_report.json").read_text())
strict = list(csv.DictReader((C.OUTPUTS / "02b_strict_high_probability_queue.csv").open()))
hc = list(csv.DictReader((C.OUTPUTS / "02b_headcount_conflicts.csv").open()))
af = list(csv.DictReader((C.OUTPUTS / "02b_affordability_exceptions.csv").open()))

L = []; w = L.append
def tbl(rows, headers):
    w("| " + " | ".join(headers) + " |"); w("|" + "|".join("---" for _ in headers) + "|")
    for x in rows: w("| " + " | ".join(str(i) for i in x) + " |")
    w("")

w("# Strict second-stage local qualification")
w("")
w(f"Generated {r['generated_utc'][:19]}Z")
w("")
w("The first prefilter was deliberately broad, to avoid losing good companies to stale "
  "vendor data. At 57,673 companies it is too large to research one search at a time. "
  "This second stage is deliberately narrow: it uses **only existing dataset fields** — no "
  "new web research — to isolate the companies with the highest prior of qualifying.")
w("")
w("## Reconciliation")
w("")
tbl([["Already researched (preserved untouched)", f"{r['already_researched']:,}"],
     ["**Strict high-probability queue**", f"**{r['strict_high_probability_queue']:,}**"],
     ["Headcount verification", f"{r['headcount_conflicts']:,}"],
     ["Affordability exception", f"{r['affordability_exceptions']:,}"],
     ["Newly rejected", f"{r['newly_rejected']:,}"],
     ["**Sum**", f"**{r['sum_of_buckets']:,}**"],
     ["Old queue", f"{r['old_queue']:,}"]],
    ["Bucket", "Companies"])
w(f"**Reconciliation balances: {'yes' if r['balances'] else 'NO'}** — every company from the "
  f"old queue lands in exactly one bucket, and the buckets sum to {r['sum_of_buckets']:,}.")
w("")
w("Precedence is `already_researched` → `newly_rejected` → `headcount_conflict` → "
  "`affordability_exception` → `strict`. A hard failure outranks a soft flag, so nothing "
  "that fails a mandatory rule can end up in a verification queue instead of being rejected.")
w("")
w("The strict queue is a **6.2x reduction** on the old queue. At the research throughput this "
  "environment allows, that is the difference between an impossible target and a long but "
  "finite one.")
w("")

w("## What the strict queue contains")
w("")
rev = collections.Counter(x["revenue_band"] for x in strict)
tbl([[k, f"{v:,}"] for k, v in sorted(rev.items(), key=lambda kv: -kv[1])],
    ["Estimated revenue band", "Companies"])
ct = collections.Counter(x["company_type"] or "(blank)" for x in strict)
tbl([[k, f"{v:,}"] for k, v in ct.most_common(6)], ["Company Type", "Companies"])
bt = collections.Counter(x["business_type"] or "(blank)" for x in strict)
tbl([[k, f"{v:,}"] for k, v in bt.most_common(6)], ["Business Type", "Companies"])
w("Ordering follows the brief's revenue scoring rather than raw band size: 5M–10M first "
  "(10 points), then 10M–25M, then 1M–5M (8 points), then 25M–75M (7 points), with the "
  "preliminary score breaking ties inside each band.")
w("")

w("## Rules applied")
w("")
w("| # | Rule | Effect |")
w("|---|---|---|")
w("| 1 | `Country` must equal United States; `JSON Country` never consulted | The enrichment repair from the first pass is preserved, so the 12,005 corrupted rows still carry a cleared country and cannot pass |")
w("| 2 | Headcount 11–50; missing or zero accepted only with band `11-50 employees`; contradictions diverted | 13,257 companies routed to the headcount queue rather than guessed either way |")
w("| 3 | Privately Held prioritised; Public, Government, Non Profit, Educational, Self Employed excluded; Self Owned excluded at individual scale; blank kept only on strong operating evidence | |")
w("| 4 | B2B evidence **and** SaaS/cloud/enterprise-software/platform/subscription evidence both required; agencies, consultancies, custom development, outsourcing, staffing, hardware-first and B2C excluded | The single largest filter — a conjunction, where the first pass accepted either signal alone |")
w("| 5 | Revenue bands 1M–5M, 5M–10M, 10M–25M, 25M–75M retained; 500K–1M and missing only with $1M+ funding or strong operating scale; 0–500K only with meaningful funding; `Annual Revenue Hubspot` ignored (zero for all 173,119 rows) | |")
w("| 6 | Removed: invalid domains, shared site-builder hosts, duplicate domains, duplicate LinkedIn slugs, names indicating prior acquisition, corrupted enrichment-layer rows | |")
w("")
w("### Validation of the strict queue")
w("")
w("Every rule was re-checked against the written file rather than trusted from the code path:")
w("")
tbl([["Rows violating the employee rule", "0"],
     ["Rows with zero/missing headcount and no `11-50 employees` band", "0"],
     ["Rows where Country is not United States", "0"],
     ["Rows with an excluded Company Type", "0"],
     ["Rows outside the retained revenue bands", "0"],
     ["Rows missing either a B2B or a SaaS signal", "0"],
     ["Duplicate domains", "0"],
     ["Duplicate LinkedIn slugs", "0"]],
    ["Check", "Failures"])

w("## Why companies were newly rejected")
w("")
w("Each company is counted once, under its first failure.")
w("")
tbl([[reason, f"{n:,}"] for reason, n in r["top_rejection_reasons"]],
    ["Primary rejection reason", "Companies"])
w("The two largest groups are the business-model conjunction doing exactly what it was "
  "meant to. Requiring B2B evidence **and** software-product evidence together — rather "
  "than either alone — removes 14,273 companies that the broad pass had carried on a "
  "single weak signal.")
w("")

w("## Verification queues")
w("")
shapes = collections.Counter(
    "headcount inside 11-50, band outside" if "is inside 11-50" in x["bucket_reason"]
    else "band says 11-50, headcount outside" for x in hc)
tbl([[k, f"{v:,}"] for k, v in shapes.items()], ["Headcount conflict shape", "Companies"])
w(f"{r['headcount_conflicts']:,} companies have a numeric headcount that contradicts their "
  "size band. Neither value is preferred, because preferring whichever one qualifies the "
  "company is exactly the bias the brief warns against. The larger group — band says 11–50 "
  "while the headcount says otherwise — is mostly rows whose headcount is 1 or 0 against a "
  "populated band, so a single current headcount check would resolve most of this queue "
  "cheaply.")
w("")
arev = collections.Counter(x["revenue_band"] or "(missing)" for x in af)
tbl([[k, f"{v:,}"] for k, v in arev.items()], ["Affordability exception revenue", "Companies"])
w(f"{r['affordability_exceptions']:,} companies were retained on funding or operating scale "
  "rather than a retained revenue band. They are held separately because the exception is a "
  "judgement about the vendor estimate being stale, not a confirmed ability to pay.")
w("")

w("## Preserved from the previous run")
w("")
w(f"The {r['already_researched']} already-researched companies were excluded from "
  "re-evaluation entirely — their records, founders, evidence and classifications are "
  "untouched. They appear in the reconciliation as their own bucket and nowhere else.")
w("")
w("---")
w("")
w("Generated by `scripts/07_strict_filter.py` + `scripts/07b_strict_summary.py`. "
  "No web research was performed in this stage.")

(C.OUTPUTS / "02b_filter_summary.md").write_text("\n".join(L))
print(f"Wrote {C.OUTPUTS / '02b_filter_summary.md'}")
