#!/usr/bin/env python3
"""Render outputs/00_data_audit_summary.md from outputs/00_data_audit.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

a = json.loads((C.OUTPUTS / "00_data_audit.json").read_text())
inp, ids, ctry, emp, rev = a["input"], a["identifiers"], a["country"], a["employees"], a["revenue"]
n = inp["total_rows"]
L = []
w = L.append

def tbl(rows, headers):
    w("| " + " | ".join(headers) + " |")
    w("|" + "|".join("---" for _ in headers) + "|")
    for r in rows:
        w("| " + " | ".join(str(x) for x in r) + " |")
    w("")

w("# Data audit — US software / SaaS company database")
w("")
w(f"Generated {a['audit_generated_utc'][:19]}Z · research date {a['research_date']}")
w("")
w("## Input")
w("")
tbl([
    ["File", f"`{inp['filename']}`"],
    ["Path", f"`{inp['path']}`"],
    ["Size", f"{inp['file_size_bytes']:,} bytes"],
    ["SHA-256", f"`{inp['sha256']}`"],
    ["Encoding", inp["encoding"]],
    ["Rows", f"{n:,}"],
    ["Source columns", inp["total_columns_source"]],
    ["Assembled from", f"{inp['assembled_from_parts']} uploaded parts"],
], ["Property", "Value"])
w("The source arrived as ten byte-chunked parts, each repeating the 27-column header. "
  "They were reassembled in part order with a CSV parser (free-text columns embed newlines, "
  "so line-based concatenation would corrupt records). The reassembled row count is "
  f"**{n:,}**, an exact match for the count stated in the brief, with zero width-malformed rows. "
  "Two provenance columns (`source_part`, `source_row_id`) were appended; the originals are "
  "unmodified and held read-only.")
w("")

w("## Completeness")
w("")
miss = sorted(a["missing_values"].items(), key=lambda kv: -kv[1]["missing_pct"])
tbl([[f"`{k}`", f"{v['missing_count']:,}", f"{v['missing_pct']:.2f}%"] for k, v in miss],
    ["Column", "Missing", "Missing %"])

w("## Identifiers and duplicates")
w("")
d, li, nm = ids["domain"], ids["linkedin_company_url"], ids["company_name"]
tbl([
    ["Domain (normalized)", f"{d['unique_normalized']:,}", f"{d['duplicate_domain_values']:,}",
     f"{d['excess_rows_from_domain_dupes']:,}"],
    ["LinkedIn company slug", f"{li['unique_slugs']:,}", f"{li['duplicate_slug_values']:,}",
     f"{li['excess_rows_from_slug_dupes']:,}"],
    ["Company name (normalized)", f"{nm['unique_normalized']:,}", f"{nm['duplicate_name_values']:,}",
     f"{nm['excess_rows_from_name_dupes']:,}"],
], ["Key", "Unique values", "Values appearing >1×", "Excess rows"])
w(f"Every row carries a domain and a LinkedIn URL, and all {n:,} LinkedIn URLs parse to a slug. "
  "Domains are effectively unique: after excluding shared site-builder hosts (Yola, Leadpages "
  "and similar, where the registrable domain names the platform rather than the business), "
  f"just {d['duplicate_domain_values']} domain value repeats. ")
w("")
w(f"**The real duplication axis is the LinkedIn company page.** {li['duplicate_slug_values']:,} "
  f"slugs appear on more than one row, covering {li['rows_sharing_a_duplicate_slug']:,} rows — "
  f"{li['excess_rows_from_slug_dupes']:,} of them redundant. These are typically one company "
  "reached through several domains. Name-based collisions are looser still and include genuinely "
  "distinct companies that share a name, so name matching is only ever used together with locality.")
w("")
w("### Suspected duplicate clusters")
w("")
dc = a["duplicate_clusters"]
tbl([["Domain clusters", f"{dc['domain_clusters']:,}"],
     ["LinkedIn slug clusters", f"{dc['linkedin_slug_clusters']:,}"],
     ["Name + locality clusters", f"{dc['name_plus_locality_clusters']:,}"],
     ["Rows in name+locality clusters", f"{dc['rows_in_name_plus_locality_clusters']:,}"]],
    ["Cluster type", "Count"])

w("## Country — the headline data-quality failure")
w("")
us = ctry["us_status_from_country"]
tbl([[k, f"{v:,}", f"{100.0*v/n:.2f}%"] for k, v in sorted(us.items(), key=lambda kv: -kv[1])],
    ["`Country` resolves to", "Rows", "Share"])
w(f"**`JSON Country` is unusable as location evidence.** It reports a US value for "
  f"{sum(ctry['us_status_from_json_country'].get(k,0) for k in ('us','us_territory')):,} rows "
  f"({100.0*sum(ctry['us_status_from_json_country'].get(k,0) for k in ('us','us_territory'))/n:.1f}%). "
  f"That includes **every one of the {ctry['json_country_claims_us_but_country_is_foreign']:,} rows "
  "whose `Country` column names a foreign country** — the column labels essentially the entire file "
  "United States regardless of the underlying record. It is excluded from all filtering.")
w("")
w("`Country` itself mixes full names with ISO-3166 alpha-2 codes in mixed case (`PK`, `TW`, `am`, "
  "`cl`), which normalization resolves. The largest foreign group is Singapore "
  f"({next((x['count'] for x in ctry['country_normalized_distribution'] if x['value']=='Singapore'), 0):,} rows), "
  "conspicuous in a file labelled as US companies.")
w("")
w("Top countries after normalization:")
w("")
tbl([[x["value"], f"{x['count']:,}"] for x in ctry["country_normalized_distribution"][:12]],
    ["Country", "Rows"])

w("## Employees")
w("")
b = emp["headcount_buckets"]
tbl([[k, f"{v:,}"] for k, v in b.items()], ["Numeric headcount", "Rows"])
tbl([[x["value"], f"{x['count']:,}"] for x in emp["size_range_distribution"]],
    ["`Employee Size Range`", "Rows"])
w(f"**{emp['employee_field_conflicts']:,} rows ({100.0*emp['employee_field_conflicts']/n:.1f}%) have a "
  "numeric headcount that contradicts the size band**, and "
  f"{emp['headcount_zero']:,} rows report headcount 0. Both fields are treated as independent "
  "estimates: where they disagree the row is retained, the conflict is recorded, and verification "
  "is required before the company can qualify. Neither value is silently preferred because it "
  "would make a company fit.")
w("")
tbl([[k, f"{v:,}"] for k, v in sorted(emp["initial_fit_distribution"].items(), key=lambda kv: -kv[1])],
    ["Preliminary 11-50 fit (either estimate)", "Rows"])

w("## Revenue and funding")
w("")
tbl([[x["value"], f"{x['count']:,}"] for x in rev["clay_band_distribution"]],
    ["`Annual Revenue Clay` (estimate)", "Rows"])
w(f"**`Annual Revenue Hubspot` is `0` for all {n:,} rows.** It carries no information and is never "
  "read as evidence that a company has no revenue. `Annual Revenue Clay` is an estimate used for "
  "preliminary filtering and priority only; it is never reported as confirmed revenue.")
w("")
tbl([[x["value"], f"{x['count']:,}"] for x in a["funding"]["band_distribution"]],
    ["`Total Funding Range`", "Rows"])
w(f"{a['funding']['funding_unknown']:,} rows are `Funding unknown`, so absence of funding data "
  "never rejects a company on its own.")
w("")

w("## Classification fields")
w("")
tbl([[x["value"], f"{x['count']:,}"] for x in a["business_type_distribution"]], ["`Business Type`", "Rows"])
tbl([[x["value"], f"{x['count']:,}"] for x in a["company_type_distribution"]], ["`Company Type`", "Rows"])
w("Top industries:")
w("")
tbl([[x["value"], f"{x['count']:,}"] for x in a["industry_distribution"][:20]], ["`Industry`", "Rows"])

w("## Founded year and followers")
w("")
f_ = a["founded"]
tbl([[k, f"{v:,}"] for k, v in f_["buckets"].items()], ["Founded", "Rows"])
w(f"{f_['missing_or_unparseable']:,} rows have no parseable founding year "
  f"(range {f_['min']}–{f_['max']}).")
w("")
tbl([[k, f"{v:,}"] for k, v in a["followers"]["buckets"].items()], ["LinkedIn followers", "Rows"])

w("## Malformed and unusable records")
w("")
m = a["malformed"]
tbl([["Missing company name", f"{m['missing_company_name']:,}"],
     ["Missing domain", f"{m['missing_domain']:,}"],
     ["Missing LinkedIn URL", f"{m['missing_linkedin_url']:,}"],
     ["No usable identifier at all", f"{m['rows_with_no_usable_identifier']:,}"],
     ["Width-malformed rows at assembly", "0"]],
    ["Problem", "Rows"])

w("## Material issues carried into the pipeline")
w("")
for i, it in enumerate(a["material_issues"], 1):
    w(f"**{i}. {it['issue']}**  ")
    w(f"{it['detail']}  ")
    w(f"*Handling:* {it['handling']}")
    w("")

w("---")
w("")
w("Source file unmodified throughout. Generated by `scripts/01_audit.py` + "
  "`scripts/01b_audit_summary.py`.")

(C.OUTPUTS / "00_data_audit_summary.md").write_text("\n".join(L))
print(f"Wrote {C.OUTPUTS / '00_data_audit_summary.md'}")
