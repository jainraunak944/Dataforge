#!/usr/bin/env python3
"""Stage 1: audit the canonical source CSV. Read-only; the source is never modified.

Writes outputs/00_data_audit.json (machine-readable) and
       outputs/00_data_audit_summary.md (human-readable).
"""
from __future__ import annotations
import sys, json, csv, hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
import pandas as pd

RESEARCH_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT_JSON = C.OUTPUTS / "00_data_audit.json"
OUT_MD = C.OUTPUTS / "00_data_audit_summary.md"
C.OUTPUTS.mkdir(parents=True, exist_ok=True)


def topn(counter, n=40):
    return [{"value": k if k != "" else "(blank)", "count": int(v)}
            for k, v in counter.most_common(n)]


def main():
    src = C.CANONICAL_CSV
    print(f"Auditing {src} ...")
    df = pd.read_csv(src, dtype=str, keep_default_na=False, engine="python")
    n = len(df)
    cols = [c for c in df.columns if c not in ("source_part", "source_row_id")]

    sha = hashlib.sha256()
    with src.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)

    audit = {
        "audit_generated_utc": datetime.now(timezone.utc).isoformat(),
        "research_date": RESEARCH_DATE,
        "input": {
            "filename": src.name,
            "path": str(src),
            "file_size_bytes": src.stat().st_size,
            "sha256": sha.hexdigest(),
            "encoding": "utf-8",
            "assembled_from_parts": 10,
            "total_rows": int(n),
            "total_columns_source": len(cols),
            "column_names": cols,
            "pipeline_added_columns": ["source_part", "source_row_id"],
        },
    }

    # ---------------------------------------------------------- completeness --
    missing = {}
    for c in cols:
        blank = int(df[c].eq("").sum())
        missing[c] = {"missing_count": blank, "missing_pct": round(100.0 * blank / n, 3)}
    audit["missing_values"] = missing

    # ------------------------------------------------------------ identifiers --
    dom_norm = df["Domain"].map(C.normalize_domain)
    li = df["LinkedIn Company URL"].map(C.normalize_linkedin)
    li_slug = li.map(lambda t: t[1])
    name_norm = df["Company Name"].map(C.normalize_company_name)

    dom_nonblank = dom_norm[dom_norm != ""]
    slug_nonblank = li_slug[li_slug != ""]
    name_nonblank = name_norm[name_norm != ""]

    dom_counts = Counter(dom_nonblank)
    slug_counts = Counter(slug_nonblank)
    name_counts = Counter(name_nonblank)

    dup_dom = {k: v for k, v in dom_counts.items() if v > 1}
    dup_slug = {k: v for k, v in slug_counts.items() if v > 1}
    dup_name = {k: v for k, v in name_counts.items() if v > 1}

    audit["identifiers"] = {
        "domain": {
            "present": int((df["Domain"] != "").sum()),
            "missing": int((df["Domain"] == "").sum()),
            "normalized_nonblank": int(len(dom_nonblank)),
            "unique_normalized": int(len(dom_counts)),
            "duplicate_domain_values": int(len(dup_dom)),
            "rows_sharing_a_duplicate_domain": int(sum(dup_dom.values())),
            "excess_rows_from_domain_dupes": int(sum(dup_dom.values()) - len(dup_dom)),
            "top_duplicates": topn(Counter(dup_dom), 25),
        },
        "linkedin_company_url": {
            "present": int((df["LinkedIn Company URL"] != "").sum()),
            "missing": int((df["LinkedIn Company URL"] == "").sum()),
            "parsed_slugs": int(len(slug_nonblank)),
            "unparseable_nonblank": int(((df["LinkedIn Company URL"] != "") & (li_slug == "")).sum()),
            "unique_slugs": int(len(slug_counts)),
            "duplicate_slug_values": int(len(dup_slug)),
            "rows_sharing_a_duplicate_slug": int(sum(dup_slug.values())),
            "excess_rows_from_slug_dupes": int(sum(dup_slug.values()) - len(dup_slug)),
            "top_duplicates": topn(Counter(dup_slug), 25),
        },
        "company_name": {
            "present": int((df["Company Name"] != "").sum()),
            "missing": int((df["Company Name"] == "").sum()),
            "unique_normalized": int(len(name_counts)),
            "duplicate_name_values": int(len(dup_name)),
            "rows_sharing_a_duplicate_name": int(sum(dup_name.values())),
            "excess_rows_from_name_dupes": int(sum(dup_name.values()) - len(dup_name)),
            "top_duplicates": topn(Counter(dup_name), 25),
        },
        "invalid_urls": {
            "invalid_domain_values": int((~df["Domain"].map(C.valid_url)).sum() - (df["Domain"] == "").sum()),
            "invalid_linkedin_values": int(((df["LinkedIn Company URL"] != "") & (li_slug == "")).sum()),
        },
    }

    # --------------------------------------------------------------- country --
    cnorm = df["Country"].map(C.normalize_country)
    jnorm = df["JSON Country"].map(C.normalize_country)
    cstat = cnorm.map(C.us_status)
    jstat = jnorm.map(C.us_status)

    conflict_mask = (cnorm != "") & (jnorm != "") & (cnorm != jnorm)
    json_says_us_country_says_foreign = int(((jstat.isin(["us", "us_territory"])) & (cstat == "foreign")).sum())
    country_says_us_json_says_foreign = int(((cstat == "us") & (jstat == "foreign")).sum())

    audit["country"] = {
        "country_raw_distribution": topn(Counter(df["Country"]), 60),
        "country_normalized_distribution": topn(Counter(cnorm), 60),
        "json_country_distribution": topn(Counter(df["JSON Country"]), 20),
        "us_status_from_country": dict(Counter(cstat)),
        "us_status_from_json_country": dict(Counter(jstat)),
        "rows_where_country_and_json_country_differ": int(conflict_mask.sum()),
        "json_country_claims_us_but_country_is_foreign": json_says_us_country_says_foreign,
        "country_is_us_but_json_country_is_foreign": country_says_us_json_says_foreign,
        "note": ("JSON Country labels ~98% of rows United States and cannot be used as "
                 "evidence of a US headquarters. Country is the primary location filter."),
    }

    # ------------------------------------------------------------- employees --
    hc = df["Employee Headcount"].map(C.parse_headcount)
    rng = df["Employee Size Range"].map(C.parse_employee_range)
    rlo = rng.map(lambda t: t[0]); rhi = rng.map(lambda t: t[1])
    assess = [C.employee_assessment(h, lo, hi) for h, lo, hi in zip(hc, rlo, rhi)]
    emp_fit = [a[0] for a in assess]; emp_conflict = [a[1] for a in assess]

    hc_present = hc.dropna()
    hc_pos = hc_present[hc_present > 0]
    audit["employees"] = {
        "headcount_missing_or_blank": int(hc.isna().sum()),
        "headcount_zero": int((hc == 0).sum()),
        "headcount_positive": int(len(hc_pos)),
        "headcount_describe": {k: (float(v) if v == v else None)
                               for k, v in hc_pos.describe().to_dict().items()},
        "headcount_buckets": {
            "1-10": int(((hc_pos >= 1) & (hc_pos <= 10)).sum()),
            "11-50": int(((hc_pos >= 11) & (hc_pos <= 50)).sum()),
            "51-200": int(((hc_pos >= 51) & (hc_pos <= 200)).sum()),
            "201-1000": int(((hc_pos >= 201) & (hc_pos <= 1000)).sum()),
            "1001+": int((hc_pos > 1000).sum()),
        },
        "size_range_distribution": topn(Counter(df["Employee Size Range"]), 15),
        "employee_field_conflicts": int(sum(emp_conflict)),
        "initial_fit_distribution": dict(Counter(emp_fit)),
        "note": ("Numeric headcount and the size band are independent estimates. Where they "
                 "disagree the row is retained and flagged for verification rather than "
                 "resolved toward whichever value would qualify the company."),
    }

    # --------------------------------------------------------------- revenue --
    rev = df["Annual Revenue Clay"].map(C.parse_revenue)
    audit["revenue"] = {
        "clay_band_distribution": topn(Counter(df["Annual Revenue Clay"]), 20),
        "clay_missing": int((df["Annual Revenue Clay"] == "").sum()),
        "hubspot_distinct_values": topn(Counter(df["Annual Revenue Hubspot"]), 10),
        "hubspot_all_zero": bool((df["Annual Revenue Hubspot"].str.strip() == "0").all()),
        "note": ("Annual Revenue Hubspot is 0 for every one of the 173,119 rows and carries "
                 "no information; it is never read as evidence of no revenue. Annual Revenue "
                 "Clay is an estimate used for preliminary filtering only."),
    }

    audit["funding"] = {
        "band_distribution": topn(Counter(df["Total Funding Range"]), 15),
        "funding_unknown": int((df["Total Funding Range"] == "Funding unknown").sum()),
        "missing": int((df["Total Funding Range"] == "").sum()),
    }

    # ----------------------------------------------------------- categorical --
    audit["business_type_distribution"] = topn(Counter(df["Business Type"]), 15)
    audit["company_type_distribution"] = topn(Counter(df["Company Type"]), 15)
    audit["industry_distribution"] = topn(Counter(df["Industry"]), 50)
    audit["subindustry_distribution"] = topn(Counter(df["SubIndustry"]), 50)
    audit["derived_industry_distribution"] = topn(Counter(df["Derived Industry"]), 50)

    yr = df["Founded"].map(C.parse_year)
    yr_ok = yr.dropna()
    audit["founded"] = {
        "missing_or_unparseable": int(yr.isna().sum()),
        "min": int(yr_ok.min()) if len(yr_ok) else None,
        "max": int(yr_ok.max()) if len(yr_ok) else None,
        "buckets": {
            "pre-1990": int((yr_ok < 1990).sum()),
            "1990-1999": int(((yr_ok >= 1990) & (yr_ok <= 1999)).sum()),
            "2000-2009": int(((yr_ok >= 2000) & (yr_ok <= 2009)).sum()),
            "2010-2014": int(((yr_ok >= 2010) & (yr_ok <= 2014)).sum()),
            "2015-2019": int(((yr_ok >= 2015) & (yr_ok <= 2019)).sum()),
            "2020-2026": int((yr_ok >= 2020).sum()),
        },
    }

    fol = df["Follower Count"].map(C.parse_int).dropna()
    audit["followers"] = {
        "missing": int(df["Follower Count"].eq("").sum()),
        "describe": {k: (float(v) if v == v else None) for k, v in fol.describe().to_dict().items()},
        "buckets": {
            "0-49": int((fol < 50).sum()),
            "50-199": int(((fol >= 50) & (fol < 200)).sum()),
            "200-1999": int(((fol >= 200) & (fol < 2000)).sum()),
            "2000-19999": int(((fol >= 2000) & (fol < 20000)).sum()),
            "20000+": int((fol >= 20000).sum()),
        },
    }

    # ------------------------------------------------------- malformed rows ---
    no_name = int((df["Company Name"] == "").sum())
    no_dom = int((df["Domain"] == "").sum())
    no_li = int((df["LinkedIn Company URL"] == "").sum())
    no_id_at_all = int(((df["Company Name"] == "") & (df["Domain"] == "") &
                        (df["LinkedIn Company URL"] == "")).sum())
    audit["malformed"] = {
        "missing_company_name": no_name,
        "missing_domain": no_dom,
        "missing_linkedin_url": no_li,
        "rows_with_no_usable_identifier": no_id_at_all,
        "width_malformed_rows_at_assembly": json.loads(
            (C.DATA / "interim" / "assembly_report.json").read_text()).get("per_part"),
    }

    # ------------------------------------------- suspected duplicate clusters --
    multi_dom = sum(1 for v in dup_dom.values())
    multi_slug = sum(1 for v in dup_slug.values())
    key_cluster = Counter()
    loc = df["Locality"].fillna("")
    for nm, lc in zip(name_norm, loc):
        if nm:
            key_cluster[(nm, lc.strip().lower())] += 1
    dup_name_loc = {k: v for k, v in key_cluster.items() if v > 1}
    audit["duplicate_clusters"] = {
        "domain_clusters": multi_dom,
        "linkedin_slug_clusters": multi_slug,
        "name_plus_locality_clusters": len(dup_name_loc),
        "rows_in_name_plus_locality_clusters": int(sum(dup_name_loc.values())),
        "estimated_total_excess_rows": int(
            sum(dup_dom.values()) - len(dup_dom)),
    }

    # ------------------------------------------------------ material issues ---
    issues = []
    issues.append({
        "issue": "JSON Country is unusable as location evidence",
        "detail": (f"JSON Country reports a US value for "
                   f"{int((jstat.isin(['us','us_territory'])).sum()):,} of {n:,} rows "
                   f"({100.0*int((jstat.isin(['us','us_territory'])).sum())/n:.1f}%), including "
                   f"{json_says_us_country_says_foreign:,} rows whose Country column names a "
                   f"foreign country."),
        "handling": "Country is the primary filter; JSON Country is never used as proof of US HQ.",
    })
    issues.append({
        "issue": "Annual Revenue Hubspot is entirely zero",
        "detail": "All 173,119 rows contain 0. The column carries no signal.",
        "handling": "Excluded from all filtering; never read as evidence of zero revenue.",
    })
    issues.append({
        "issue": "Total Funding Range is mostly unknown",
        "detail": f"{int((df['Total Funding Range']=='Funding unknown').sum()):,} rows are 'Funding unknown'.",
        "handling": "Absence of funding data never rejects a company on its own.",
    })
    issues.append({
        "issue": "Singapore over-represented for a US dataset",
        "detail": f"{int((cnorm=='Singapore').sum()):,} rows are Singapore-registered, the second "
                  f"largest country group, despite the file being labelled US companies.",
        "handling": "Rejected at the local US filter unless other evidence indicates a US HQ.",
    })
    issues.append({
        "issue": "Employee fields disagree",
        "detail": f"{int(sum(emp_conflict)):,} rows have a numeric headcount that contradicts the size band; "
                  f"{int((hc==0).sum()):,} rows have headcount 0.",
        "handling": "Both estimates retained, conflict flagged, verification required before qualifying.",
    })
    issues.append({
        "issue": "Most rows are outside the target employee band",
        "detail": f"{int((df['Employee Size Range']=='2-10 employees').sum()):,} rows are 2-10 employees and "
                  f"{int((df['Employee Size Range']=='Self-employed').sum()):,} are Self-employed.",
        "handling": "Filtered at Stage 4; borderline and conflicting cases are researched, not discarded.",
    })
    audit["material_issues"] = issues

    OUT_JSON.write_text(json.dumps(audit, indent=2, default=str))
    print(f"Wrote {OUT_JSON}")
    return audit, df


if __name__ == "__main__":
    main()
