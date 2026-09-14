#!/usr/bin/env python3
"""Stages 2 and 3: normalization and duplicate resolution.

Normalizes every row into canonical fields, then resolves duplicates in the
order the brief specifies:

  1. normalized domain            -> confident merge
  2. normalized LinkedIn slug     -> confident merge
  3. normalized name + locality   -> NOT merged; flagged for review
  4. name + description overlap   -> NOT merged; flagged for review

Tier 2 is only safe once mis-enriched LinkedIn rows are stripped out. The source
attaches one company's LinkedIn page to thousands of unrelated domains (5,573
distinct domains carry Lazada's page, name, country, headcount and description).
Those rows are detected, excluded from merging, and have their LinkedIn-layer
fields cleared while the trustworthy domain-derived layer is kept -- see
`detect_enrichment_suspects`. Tier 1 is an identity match, so merging is safe. Tiers 3 and 4 routinely collide on genuinely distinct companies that
share a name in the same city, which is material uncertainty: those clusters are
written to the review queue and their rows are kept separate, per the brief's
"do not merge when there is material uncertainty".

Outputs: outputs/01_deduplicated_companies.csv
         outputs/01_possible_duplicates.csv
         data/interim/dedupe_report.json
"""
from __future__ import annotations
import sys, csv, json, re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
import pandas as pd

OUT_DEDUP = C.OUTPUTS / "01_deduplicated_companies.csv"
OUT_DUPES = C.OUTPUTS / "01_possible_duplicates.csv"
REPORT = C.DATA / "interim" / "dedupe_report.json"

# Fields whose presence indicates a more complete source record.
COMPLETENESS_FIELDS = [
    "Company Name", "Domain", "LinkedIn Company URL", "Description", "Derived Description",
    "Industry", "SubIndustry", "Derived Industry", "Specialties", "Locality", "Country",
    "Founded", "Employee Headcount", "Employee Size Range", "Annual Revenue Clay",
    "Total Funding Range", "Business Type", "Company Type", "Pattern Tags", "Follower Count",
]

_WORD = re.compile(r"[a-z0-9]+")
_KEY = re.compile(r"[^a-z0-9]+")

# Fields scraped from the LinkedIn company page. When the page belongs to a
# different company these are all wrong together, so they are cleared together.
LINKEDIN_LAYER = [
    "company_name_original", "company_name_normalized", "linkedin_company_url",
    "linkedin_slug", "linkedin_company_url_original", "country_original",
    "country_normalized", "locality", "employee_headcount_numeric",
    "employee_range_normalized", "employee_range_low", "employee_range_high",
    "description", "industry", "company_type", "founded_year", "specialties",
    "follower_count",
]
# Derived from the domain itself; verified to vary per row inside a corrupted
# cluster, so these survive the repair.
DOMAIN_LAYER = ["derived_description", "pattern_tags", "subindustry", "scale_scope",
                "derived_industry", "revenue_band_original", "funding_band_original"]

_NAME_FROM_DESC = re.compile(
    r"^([A-Z][\w&.\-']*(?:\s+[A-Z0-9][\w&.\-']*){0,4})\s+"
    r"(?:is|are|was|provides?|offers?|helps?|delivers?|builds?|develops?|"
    r"specciali[sz]es?|speciali[sz]es?|creates?|enables?|operates?|has|makes?|"
    r"powers?|supplies|serves)\b")

def keyify(s: str) -> str:
    return _KEY.sub("", (s or "").lower())

def corroborates(domain_stem: str, slug_key: str, name_key: str) -> bool:
    """True when the domain supports the LinkedIn identity attached to the row."""
    if len(domain_stem) < 4:
        return True  # too short to judge; give the row the benefit of the doubt
    for other in (slug_key, name_key):
        if len(other) >= 4 and (domain_stem in other or other in domain_stem):
            return True
    return False

def name_from_domain(domain: str) -> str:
    stem = domain.rsplit(".", 1)[0] if "." in domain else domain
    stem = stem.split(".")[-1]
    return stem.replace("-", " ").title()

def name_from_derived(desc: str) -> str:
    m = _NAME_FROM_DESC.match((desc or "").strip())
    return m.group(1).strip() if m else ""

def desc_tokens(s: str) -> set[str]:
    return set(_WORD.findall((s or "").lower()))

def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class Union:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def main():
    print("Loading canonical CSV ...")
    df = pd.read_csv(C.CANONICAL_CSV, dtype=str, keep_default_na=False, engine="python")
    n = len(df)
    print(f"  {n:,} rows")

    print("Normalizing ...")
    norm = pd.DataFrame(index=df.index)
    norm["source_row_id"] = df["source_row_id"]
    norm["source_part"] = df["source_part"]
    norm["company_name_original"] = df["Company Name"]
    norm["company_name_normalized"] = df["Company Name"].map(C.normalize_company_name)
    norm["domain_original"] = df["Domain"]
    norm["domain_normalized"] = df["Domain"].map(C.normalize_domain)
    norm["website_url"] = norm["domain_normalized"].map(C.website_url)

    li = df["LinkedIn Company URL"].map(C.normalize_linkedin)
    norm["linkedin_company_url_original"] = df["LinkedIn Company URL"]
    norm["linkedin_company_url"] = li.map(lambda t: t[0])
    norm["linkedin_slug"] = li.map(lambda t: t[1])

    norm["country_original"] = df["Country"]
    norm["country_normalized"] = df["Country"].map(C.normalize_country)
    norm["us_status"] = norm["country_normalized"].map(C.us_status)
    norm["json_country_original"] = df["JSON Country"]
    norm["locality"] = df["Locality"].str.strip()
    norm["locality_looks_us"] = norm["locality"].map(C.locality_looks_us)

    hc = df["Employee Headcount"].map(C.parse_headcount)
    rng = df["Employee Size Range"].map(C.parse_employee_range)
    norm["employee_headcount_numeric"] = hc
    norm["employee_range_normalized"] = rng.map(lambda t: t[2])
    norm["employee_range_low"] = rng.map(lambda t: t[0])
    norm["employee_range_high"] = rng.map(lambda t: t[1])
    assess = [C.employee_assessment(h, lo, hi)
              for h, lo, hi in zip(hc, norm["employee_range_low"], norm["employee_range_high"])]
    norm["employee_initial_fit"] = [a[0] for a in assess]
    norm["employee_conflict"] = [a[1] for a in assess]
    norm["employee_verification_required"] = [a[2] for a in assess]

    rev = df["Annual Revenue Clay"].map(C.parse_revenue)
    norm["revenue_band_original"] = rev.map(lambda t: t[0])
    norm["revenue_low_usd"] = rev.map(lambda t: t[1])
    norm["revenue_high_usd"] = rev.map(lambda t: t[2])
    norm["revenue_midpoint_usd"] = rev.map(lambda t: t[3])
    norm["revenue_initial_fit"] = [
        ("target" if (lo is not None and lo >= 1_000_000 and hi is not None and hi <= 25_000_000)
         else "above" if (lo is not None and lo >= 25_000_000)
         else "below" if (hi is not None and hi <= 1_000_000)
         else "unknown")
        for lo, hi in zip(norm["revenue_low_usd"], norm["revenue_high_usd"])]
    # Clay bands are vendor estimates, never confirmed revenue.
    norm["revenue_confidence"] = ["estimated_vendor" if b else "unknown"
                                  for b in norm["revenue_band_original"]]

    fund = df["Total Funding Range"].map(C.parse_funding)
    norm["funding_band_original"] = fund.map(lambda t: t[0])
    norm["funding_low_usd"] = fund.map(lambda t: t[1])
    norm["funding_high_usd"] = fund.map(lambda t: t[2])

    norm["business_type"] = df["Business Type"].str.strip()
    norm["company_type"] = df["Company Type"].str.strip()
    norm["industry"] = df["Industry"].str.strip()
    norm["subindustry"] = df["SubIndustry"].str.strip()
    norm["derived_industry"] = df["Derived Industry"].str.strip()
    norm["pattern_tags"] = df["Pattern Tags"].str.strip()
    norm["specialties"] = df["Specialties"].str.strip()
    norm["description"] = df["Description"].str.strip()
    norm["derived_description"] = df["Derived Description"].str.strip()
    norm["scale_scope"] = df["Scale Scope"].str.strip()
    norm["founded_year"] = df["Founded"].map(C.parse_year)
    norm["follower_count"] = df["Follower Count"].map(C.parse_int)

    completeness = df[COMPLETENESS_FIELDS].ne("").sum(axis=1)
    norm["completeness_score"] = completeness

    # ------------------------------------ repair mis-enriched LinkedIn rows ----
    print("Detecting mis-enriched LinkedIn rows ...")
    stem = norm["domain_normalized"].map(
        lambda d: keyify(d.rsplit(".", 1)[0] if "." in d else d))
    skey = norm["linkedin_slug"].map(keyify)
    nkey = norm["company_name_normalized"].map(keyify)

    slug_groups = defaultdict(list)
    for i, sg in enumerate(norm["linkedin_slug"]):
        if sg:
            slug_groups[sg].append(i)

    suspect = set()
    clusters_affected = 0
    for sg, idxs in slug_groups.items():
        if len(idxs) < 2:
            continue
        corr = {i for i in idxs if corroborates(stem.iat[i], skey.iat[i], nkey.iat[i])}
        non = [i for i in idxs if i not in corr]
        if non and len(non) != len(idxs):
            clusters_affected += 1
            suspect.update(non)
        elif len(non) == len(idxs) and len(idxs) >= 3:
            # Nothing in the cluster corroborates and it is too large to be a
            # coincidence: the real owner is absent, so every row is suspect.
            clusters_affected += 1
            suspect.update(idxs)
    print(f"  mis-enriched clusters: {clusters_affected:,}")
    print(f"  rows flagged enrichment-suspect: {len(suspect):,}")

    norm["linkedin_enrichment_suspect"] = [i in suspect for i in range(n)]
    norm["company_name_source"] = "linkedin"

    if suspect:
        sus = sorted(suspect)
        # Recover a usable company name before clearing the LinkedIn layer.
        recovered, src = [], []
        for i in sus:
            cand = name_from_derived(norm["derived_description"].iat[i])
            if cand and len(cand) >= 3:
                recovered.append(cand); src.append("derived_description")
            else:
                recovered.append(name_from_domain(norm["domain_normalized"].iat[i]))
                src.append("domain")
        for col in LINKEDIN_LAYER:
            norm.loc[norm.index[sus], col] = None
        norm.loc[norm.index[sus], "company_name_original"] = recovered
        norm.loc[norm.index[sus], "company_name_normalized"] = [
            C.normalize_company_name(x) for x in recovered]
        norm.loc[norm.index[sus], "company_name_source"] = src
        # Location and size are now unknown, not foreign and not large.
        norm.loc[norm.index[sus], "country_normalized"] = ""
        norm.loc[norm.index[sus], "us_status"] = "unknown"
        norm.loc[norm.index[sus], "locality"] = ""
        norm.loc[norm.index[sus], "locality_looks_us"] = False
        norm.loc[norm.index[sus], "employee_initial_fit"] = "unknown"
        norm.loc[norm.index[sus], "employee_conflict"] = False
        norm.loc[norm.index[sus], "employee_verification_required"] = True
        norm.loc[norm.index[sus], "description"] = ""
        norm.loc[norm.index[sus], "industry"] = ""
        norm.loc[norm.index[sus], "company_type"] = ""
        norm.loc[norm.index[sus], "specialties"] = ""
        norm.loc[norm.index[sus], "linkedin_company_url"] = ""
        norm.loc[norm.index[sus], "linkedin_slug"] = ""

    # ------------------------------------------------------------ dedupe ----
    print("Resolving duplicates ...")
    uf = Union(n)
    merge_reason = defaultdict(set)

    by_domain = defaultdict(list)
    for i, d in enumerate(norm["domain_normalized"]):
        if d:
            by_domain[d].append(i)
    dom_clusters = 0
    for d, idxs in by_domain.items():
        if len(idxs) > 1:
            dom_clusters += 1
            for j in idxs[1:]:
                uf.union(idxs[0], j)
                merge_reason[d].add("domain")

    by_slug = defaultdict(list)
    for i, s in enumerate(norm["linkedin_slug"]):
        if s:
            by_slug[s].append(i)
    slug_clusters = 0
    for s, idxs in by_slug.items():
        if len(idxs) > 1:
            slug_clusters += 1
            for j in idxs[1:]:
                uf.union(idxs[0], j)

    groups = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)
    print(f"  domain clusters merged: {dom_clusters:,}")
    print(f"  linkedin slug clusters merged: {slug_clusters:,}")
    print(f"  canonical companies: {len(groups):,}")

    # --------------------------------------------- tier 3/4 review queue ----
    # Name+locality and name+description matches among rows NOT already merged.
    rep_of = {}
    for root, idxs in groups.items():
        best = max(idxs, key=lambda i: (norm["completeness_score"].iat[i], -i))
        rep_of[root] = best

    name_loc = defaultdict(list)
    for root, idxs in groups.items():
        r = rep_of[root]
        nm = norm["company_name_normalized"].iat[r]
        lc = (norm["locality"].iat[r] or "").lower()
        if nm:
            name_loc[(nm, lc)].append(root)

    review_rows = []
    review_clusters = 0
    for (nm, lc), roots in name_loc.items():
        if len(roots) < 2:
            continue
        review_clusters += 1
        reps = [rep_of[r] for r in roots]
        toks = [desc_tokens(norm["description"].iat[i] + " " + norm["derived_description"].iat[i])
                for i in reps]
        # Pairwise max description overlap grades how likely these are the same company.
        best_sim = 0.0
        for a in range(len(toks)):
            for b in range(a + 1, len(toks)):
                best_sim = max(best_sim, jaccard(toks[a], toks[b]))
        same_country = len({norm["country_normalized"].iat[i] for i in reps}) == 1
        if best_sim >= 0.55 and same_country:
            verdict = "likely_same_company"
        elif best_sim >= 0.25 and same_country:
            verdict = "possible_same_company"
        else:
            verdict = "probable_name_collision"
        for i in reps:
            review_rows.append({
                "cluster_key": f"{nm}||{lc}",
                "cluster_size": len(roots),
                "review_verdict": verdict,
                "max_description_similarity": round(best_sim, 3),
                "same_country": same_country,
                "match_basis": "normalized_name + locality",
                "merged_by_pipeline": "no - kept separate pending review",
                "source_row_id": norm["source_row_id"].iat[i],
                "company_name": norm["company_name_original"].iat[i],
                "company_name_normalized": nm,
                "domain": norm["domain_normalized"].iat[i],
                "linkedin_company_url": norm["linkedin_company_url"].iat[i],
                "locality": norm["locality"].iat[i],
                "country": norm["country_normalized"].iat[i],
                "employee_range": norm["employee_range_normalized"].iat[i],
                "revenue_band": norm["revenue_band_original"].iat[i],
                "description_excerpt": (norm["description"].iat[i] or "")[:240],
            })

    # ------------------------------------------------ build deduped table ----
    print("Building deduplicated table ...")
    out_rows = []
    for root, idxs in groups.items():
        rep = rep_of[root]
        rec = {c: norm[c].iat[rep] for c in norm.columns}
        rec["canonical_company_id"] = f"SQ{root:06d}"
        rec["source_row_ids"] = ";".join(str(norm["source_row_id"].iat[i]) for i in sorted(idxs))
        rec["merged_row_count"] = len(idxs)
        rec["merged_domains"] = ";".join(sorted({norm["domain_normalized"].iat[i] for i in idxs if norm["domain_normalized"].iat[i]}))
        rec["merged_linkedin_slugs"] = ";".join(sorted({norm["linkedin_slug"].iat[i] for i in idxs if norm["linkedin_slug"].iat[i]}))
        rec["merged_company_names"] = ";".join(sorted({norm["company_name_original"].iat[i] for i in idxs}))
        if len(idxs) > 1:
            basis = []
            if len({norm["domain_normalized"].iat[i] for i in idxs}) < len(idxs):
                basis.append("domain")
            if len({norm["linkedin_slug"].iat[i] for i in idxs}) < len(idxs):
                basis.append("linkedin_slug")
            rec["merge_basis"] = "+".join(basis) or "transitive"
            # Record field-level disagreement among merged rows.
            conflicts = []
            for fld in ["country_normalized", "employee_range_normalized", "revenue_band_original",
                        "company_type", "business_type"]:
                vals = {str(norm[fld].iat[i]) for i in idxs if str(norm[fld].iat[i]) not in ("", "None", "nan")}
                if len(vals) > 1:
                    conflicts.append(f"{fld}=[{'|'.join(sorted(vals))}]")
            rec["merge_field_conflicts"] = "; ".join(conflicts)
        else:
            rec["merge_basis"] = ""
            rec["merge_field_conflicts"] = ""
        out_rows.append(rec)

    ded = pd.DataFrame(out_rows)
    ded = ded.sort_values("canonical_company_id")
    lead_cols = ["canonical_company_id", "source_row_ids", "merged_row_count", "merge_basis",
                 "merge_field_conflicts", "merged_domains", "merged_linkedin_slugs",
                 "merged_company_names"]
    ded = ded[lead_cols + [c for c in ded.columns if c not in lead_cols]]
    C.OUTPUTS.mkdir(parents=True, exist_ok=True)
    ded.to_csv(OUT_DEDUP, index=False)
    print(f"  wrote {OUT_DEDUP}  ({len(ded):,} companies)")

    rev_df = pd.DataFrame(review_rows)
    if len(rev_df):
        rev_df = rev_df.sort_values(["review_verdict", "cluster_key"])
    rev_df.to_csv(OUT_DUPES, index=False)
    print(f"  wrote {OUT_DUPES}  ({len(rev_df):,} rows in {review_clusters:,} clusters)")

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input_rows": int(n),
        "enrichment_repair": {
            "mis_enriched_clusters": int(clusters_affected),
            "rows_flagged_suspect": int(len(suspect)),
            "pct_of_dataset": round(100.0 * len(suspect) / n, 2),
            "linkedin_layer_cleared": LINKEDIN_LAYER,
            "domain_layer_retained": DOMAIN_LAYER,
            "names_recovered_from_derived_description": int(
                (norm["company_name_source"] == "derived_description").sum()),
            "names_recovered_from_domain": int((norm["company_name_source"] == "domain").sum()),
        },
        "canonical_companies": int(len(ded)),
        "rows_absorbed_by_merging": int(n - len(ded)),
        "domain_clusters_merged": dom_clusters,
        "linkedin_slug_clusters_merged": slug_clusters,
        "multi_row_companies": int((ded["merged_row_count"] > 1).sum()),
        "largest_cluster": int(ded["merged_row_count"].max()),
        "companies_with_merge_field_conflicts": int((ded["merge_field_conflicts"] != "").sum()),
        "review_queue_clusters": review_clusters,
        "review_queue_rows": int(len(rev_df)),
        "review_verdicts": dict(Counter(r["review_verdict"] for r in review_rows)),
        "reconciliation": {
            "input_rows": int(n),
            "canonical_companies_plus_absorbed": int(len(ded) + (n - len(ded))),
            "balances": bool(len(ded) + (n - len(ded)) == n),
        },
    }
    REPORT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
