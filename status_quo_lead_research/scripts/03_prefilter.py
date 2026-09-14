#!/usr/bin/env python3
"""Stage 4: broad local prefilter + preliminary prioritization.

Five gates (US, employees, B2B SaaS, company type, ability to pay). Each returns
retain / conditional / reject with an explicit reason. A company is rejected
locally only when a gate clearly fails; anything uncertain is carried into the
research queue, because the brief's cost asymmetry is explicit -- losing a good
company to stale data is worse than researching a borderline one.

Outputs: outputs/02_prefiltered_research_queue.csv
         outputs/02_locally_rejected.csv
         data/interim/prefilter_report.json
"""
from __future__ import annotations
import sys, json, re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
import pandas as pd

IN_CSV = C.OUTPUTS / "01_deduplicated_companies.csv"
OUT_QUEUE = C.OUTPUTS / "02_prefiltered_research_queue.csv"
OUT_REJECT = C.OUTPUTS / "02_locally_rejected.csv"
REPORT = C.DATA / "interim" / "prefilter_report.json"

RETAIN, COND, REJECT = "retain", "conditional", "reject"

# ------------------------------------------------------------------ gate 1 --
def gate_us(r):
    st, loc_us = r["us_status"], bool(r["locality_looks_us"])
    if st == "us":
        return RETAIN, "Country resolves to United States"
    if st == "us_territory":
        return COND, f"US territory ({r['country_normalized']}) - verify HQ treatment"
    if st == "unknown":
        if loc_us:
            return COND, "Country blank but Locality names a US state - verify"
        return COND, "Country blank and Locality inconclusive - verify"
    if loc_us:
        return COND, (f"Country says {r['country_normalized']} but Locality "
                      f"'{r['locality']}' names a US state - material conflict, verify")
    return REJECT, f"Country clearly foreign ({r['country_normalized']}) with no US location evidence"

# ------------------------------------------------------------------ gate 2 --
def gate_employees(r):
    hc = r["employee_headcount_numeric"]
    hc = None if pd.isna(hc) else int(hc)
    lo, hi = r["employee_range_low"], r["employee_range_high"]
    lo = None if pd.isna(lo) else int(lo)
    hi = None if pd.isna(hi) else int(hi)
    band = r["employee_range_normalized"]

    hc_known = hc is not None and hc > 0
    hc_in = hc_known and 11 <= hc <= 50
    hc_near = hc_known and (8 <= hc <= 10 or 51 <= hc <= 65)
    rg_known = lo is not None
    rg_in = rg_known and not (hi < 11 or lo > 50)

    if hc_in and rg_in:
        return RETAIN, f"headcount {hc} and band '{band}' both inside 11-50"
    if hc_in and not rg_known:
        return COND, f"headcount {hc} inside 11-50, no size band - verify"
    if hc_in and not rg_in:
        return COND, f"CONFLICT: headcount {hc} inside 11-50 but band '{band}' is outside - verify"
    if rg_in and not hc_known:
        return COND, f"band '{band}' overlaps 11-50, headcount missing or zero - verify"
    if rg_in and not hc_in:
        return COND, f"CONFLICT: band '{band}' overlaps 11-50 but headcount {hc} is outside - verify"
    if hc_near and rg_known:
        return COND, f"headcount {hc} sits just outside 11-50 (band '{band}') - verify current size"
    if hc_near:
        return COND, f"headcount {hc} sits just outside 11-50, no band - verify"
    if hc_known and hc < 11 and rg_known and hi < 11:
        return REJECT, f"headcount {hc} and band '{band}' both clearly below 11"
    if hc_known and hc > 50 and rg_known and lo > 50:
        return REJECT, f"headcount {hc} and band '{band}' both clearly above 50"
    if hc_known and hc < 11 and not rg_known:
        return REJECT, f"headcount {hc} clearly below 11, no contradicting band"
    if hc_known and hc > 50 and not rg_known:
        return REJECT, f"headcount {hc} clearly above 50, no contradicting band"
    if rg_known and hi < 11 and not hc_known:
        return REJECT, f"band '{band}' clearly below 11, no headcount"
    if rg_known and lo > 50 and not hc_known:
        return REJECT, f"band '{band}' clearly above 50, no headcount"
    return COND, "employee size indeterminate - verify"

# ------------------------------------------------------------------ gate 3 --
SAAS_WORDS = re.compile(
    r"\b(saas|software[- ]as[- ]a[- ]service|subscription software|cloud[- ]based software|"
    r"platform|software platform|our software|our platform)\b", re.I)
WEAK_WORDS = re.compile(
    r"\b(cloud|api|apis|dashboard|integrations?|workflow|automation|analytics|"
    r"web[- ]based|login|sign ?up|free trial|book a demo|request a demo|pricing|"
    r"enterprise software|software solution)\b", re.I)
B2B_WORDS = re.compile(
    r"\b(businesses|companies|teams|enterprises?|organi[sz]ations|clients|b2b|"
    r"customers|firms|agencies|providers|operators|manufacturers|retailers)\b", re.I)
SOFTWARE_SUBIND = re.compile(
    r"(Enterprise Software|Developer Tools|AI and ML Platforms|Data and Analytics Software|"
    r"Healthcare Software|Financial Services Software|Security and Identity Software|"
    r"Logistics Technology|Manufacturing Software|Retail Technology|PropTech|"
    r"E-Learning Platforms|Marketing Technology|Sales Technology|HR Tech|"
    r"Software|Platforms|SaaS)", re.I)
# Clear disqualifiers, only when no SaaS product signal is present.
AGENCY_INDUSTRY = {
    "advertising services", "marketing services", "design services",
    "public relations and communications services", "staffing and recruiting",
    "human resources services", "outsourcing and offshoring consulting",
    "translation and localization", "graphic design", "photography",
    "writing and editing", "market research",
}
NONPROFIT_TYPES = {"non profit", "nonprofit", "government agency", "educational"}

def gate_saas(r):
    txt = " ".join(str(r.get(k) or "") for k in
                   ["description", "derived_description", "specialties", "pattern_tags",
                    "subindustry", "derived_industry", "industry", "company_name_original"])
    tags = {t.strip().lower() for t in str(r.get("pattern_tags") or "").split(",") if t.strip()}
    btype = str(r.get("business_type") or "").upper()
    industry = str(r.get("industry") or "").strip().lower()
    subind = str(r.get("subindustry") or "")

    strong, weak = [], []
    if "B2B" in btype:
        strong.append("Business Type contains B2B")
    if "b2b" in tags and ("saas" in tags or "software" in " ".join(tags)):
        strong.append("Pattern Tags contain B2B + SaaS/software")
    if re.search(r"\bsaas\b|software[- ]as[- ]a[- ]service|subscription software", txt, re.I):
        strong.append("description states SaaS / subscription software")
    if SOFTWARE_SUBIND.search(subind):
        strong.append(f"SubIndustry is software/platform ({subind[:60]})")
    if "saas" in tags:
        strong.append("Pattern Tags contain SaaS")

    if industry in {"software development", "computer software", "information technology and services",
                    "computer and network security", "it system custom software development",
                    "technology, information and internet", "data infrastructure and analytics"}:
        weak.append(f"Industry = {r.get('industry')}")
    if SAAS_WORDS.search(txt):
        weak.append("platform/software product language")
    if WEAK_WORDS.search(txt):
        weak.append("cloud/API/dashboard/demo/pricing language")
    if B2B_WORDS.search(txt):
        weak.append("sells to businesses/teams/organisations")
    if "software" in str(r.get("specialties") or "").lower():
        weak.append("Specialties mention software")

    ctype = str(r.get("company_type") or "").strip().lower()
    if ctype in NONPROFIT_TYPES:
        return REJECT, f"Company Type is {r.get('company_type')}", strong, weak
    if btype == "B2C" and not strong:
        return REJECT, "Business Type is B2C only with no B2B software signal", strong, weak
    if btype == "NONPROFIT":
        return REJECT, "Business Type is Nonprofit", strong, weak
    if industry in AGENCY_INDUSTRY and not strong:
        return REJECT, f"Industry '{r.get('industry')}' is an agency/services category with no SaaS product signal", strong, weak

    if strong:
        return RETAIN, f"{len(strong)} strong signal(s): {'; '.join(strong[:3])}", strong, weak
    if len(weak) >= 2:
        return RETAIN, f"{len(weak)} weak signals: {'; '.join(weak[:3])}", strong, weak
    if len(weak) == 1:
        return COND, f"single weak signal: {weak[0]} - verify website", strong, weak
    return REJECT, "no B2B SaaS or software-product signal in any field", strong, weak

# ------------------------------------------------------------------ gate 4 --
def gate_company_type(r):
    ct = str(r.get("company_type") or "").strip()
    low = ct.lower()
    if low == "privately held":
        return RETAIN, "Privately Held"
    if low == "public company":
        return REJECT, "Public Company"
    if low in {"government agency", "non profit", "educational"}:
        return REJECT, ct
    if low == "self employed":
        return REJECT, "Self Employed"
    if low == "self owned":
        band = str(r.get("employee_range_normalized") or "").lower()
        hc = r["employee_headcount_numeric"]
        hc = None if pd.isna(hc) else int(hc)
        if band in {"self-employed", "0-1 employees", "2-10 employees"} or (hc is not None and 0 < hc <= 2):
            return REJECT, "Self Owned at individual scale"
        return COND, "Self Owned but operating scale - verify it is a real company"
    if low == "partnership":
        return COND, "Partnership - verify private operating company"
    if not ct:
        return COND, "Company Type missing - verify ownership"
    return COND, f"Company Type '{ct}' - verify"

# ------------------------------------------------------------------ gate 5 --
AUTO_REV = {"1M-5M", "5M-10M", "10M-25M", "25M-75M"}
COND_REV = {"500K-1M", ""}

def gate_pay(r):
    band = str(r.get("revenue_band_original") or "").strip()
    fl = r["funding_low_usd"]
    fl = None if pd.isna(fl) else float(fl)
    hc = r["employee_headcount_numeric"]
    hc = None if pd.isna(hc) else int(hc)
    rlo = r["employee_range_low"]
    rlo = None if pd.isna(rlo) else int(rlo)

    strong_alt = []
    if fl is not None and fl >= 1_000_000:
        strong_alt.append(f"funding band {r.get('funding_band_original')}")
    if hc is not None and 20 <= hc <= 50:
        strong_alt.append(f"headcount {hc} (20-50)")
    if rlo == 11 and hc is not None and hc >= 20:
        strong_alt.append("operating scale in 11-50 band")

    if band in AUTO_REV:
        return RETAIN, f"estimated revenue band {band}", strong_alt
    if band in {"75M-200M", "200M-500M", "500M-1B", "1B-10B", "10B-100B", "100B-1T"}:
        return COND, (f"estimated revenue {band} is far above the target band and contradicts an "
                      f"11-50 headcount - verify company identity and size"), strong_alt
    if band == "500K-1M":
        return COND, "estimated revenue 500K-1M - verify ability to pay", strong_alt
    if band == "":
        return COND, "revenue estimate missing - assess ability to pay from funding/scale", strong_alt
    if band == "0-500K":
        if strong_alt:
            return COND, ("estimated revenue 0-500K but contradicted by " + "; ".join(strong_alt) +
                          " - estimate may be stale, verify"), strong_alt
        return REJECT, "estimated revenue 0-500K with no funding, scale or growth signal to contradict it", strong_alt
    return COND, f"revenue band '{band}' unrecognised - verify", strong_alt

# ------------------------------------------------------- preliminary score --
ATTRACTIVE = re.compile(
    r"(artificial intelligence|\bai\b|machine learning|developer tool|cyber ?security|"
    r"data infrastructure|analytics|sales tech|marketing tech|hr tech|human resources|"
    r"fintech|financial|compliance|legal tech|legaltech|healthcare|health ?tech|supply chain|"
    r"logistics|vertical saas|workflow|automation|productivity|collaboration|"
    r"customer success|revenue operations|revops|fin ?ops|procurement|insurtech|proptech)", re.I)
SALES_LED = re.compile(r"(book a demo|request a demo|schedule a demo|contact sales|talk to sales|"
                       r"enterprise plan|custom pricing|get a quote)", re.I)
PROOF = re.compile(r"(case stud|customer stor|trusted by|our customers include|success stor|testimonial)", re.I)

def preliminary_score(r):
    s, why = 0, []
    band = str(r.get("revenue_band_original") or "")
    if band in {"5M-10M", "10M-25M"}:
        s += 25; why.append("revenue 5M-25M")
    elif band == "1M-5M":
        s += 20; why.append("revenue 1M-5M")
    elif band == "25M-75M":
        s += 12; why.append("revenue 25M-75M")
    elif band == "500K-1M":
        s += 8; why.append("revenue 500K-1M")

    fl = r["funding_low_usd"]; fh = r["funding_high_usd"]
    fl = None if pd.isna(fl) else float(fl)
    fh = None if pd.isna(fh) else float(fh)
    if fl is not None and fl >= 1_000_000 and (fh is None or fh <= 25_000_000):
        s += 15; why.append(f"funding {r.get('funding_band_original')}")
    elif fl is not None and fl >= 1_000_000:
        s += 8; why.append("funding above 25M")

    hc = r["employee_headcount_numeric"]
    hc = None if pd.isna(hc) else int(hc)
    if hc is not None and 20 <= hc <= 50:
        s += 15; why.append(f"headcount {hc}")
    elif hc is not None and 11 <= hc <= 19:
        s += 10; why.append(f"headcount {hc}")

    if str(r.get("company_type") or "").strip().lower() == "privately held":
        s += 5; why.append("privately held")

    txt = " ".join(str(r.get(k) or "") for k in
                   ["description", "derived_description", "specialties", "pattern_tags", "subindustry"])
    if re.search(r"\bsaas\b|software[- ]as[- ]a[- ]service", txt, re.I):
        s += 8; why.append("explicit SaaS")
    if ATTRACTIVE.search(txt):
        s += 7; why.append("attractive SaaS category")
    if SALES_LED.search(txt):
        s += 5; why.append("demo/sales-led language")
    if PROOF.search(txt):
        s += 5; why.append("customer proof in description")

    fol = r["follower_count"]
    fol = None if pd.isna(fol) else int(fol)
    if fol is not None and 200 <= fol <= 20000:
        s += 5; why.append(f"{fol} followers")
    elif fol is not None and fol > 20000:
        s += 1

    yr = r["founded_year"]
    yr = None if pd.isna(yr) else int(yr)
    if yr is not None and 2010 <= yr <= 2023:
        s += 5; why.append(f"founded {yr}")
    elif yr is not None and yr >= 2024:
        s += 2; why.append(f"founded {yr}")

    if r.get("linkedin_slug"):
        s += 3
    return min(s, 100), "; ".join(why)


def main():
    print(f"Loading {IN_CSV} ...")
    df = pd.read_csv(IN_CSV, dtype={"source_row_ids": str}, keep_default_na=False,
                     low_memory=False)
    for col in ["employee_headcount_numeric", "employee_range_low", "employee_range_high",
                "revenue_low_usd", "revenue_high_usd", "funding_low_usd", "funding_high_usd",
                "founded_year", "follower_count", "completeness_score", "merged_row_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["locality_looks_us"] = df["locality_looks_us"].astype(str).str.lower().isin(["true", "1"])
    n = len(df)
    print(f"  {n:,} canonical companies")

    queue, rejected = [], []
    gate_counter = Counter()

    for rec in df.to_dict("records"):
        g1, r1 = gate_us(rec)
        g2, r2 = gate_employees(rec)
        g3, r3, strong, weak = gate_saas(rec)
        g4, r4 = gate_company_type(rec)
        g5, r5, alt = gate_pay(rec)

        gates = {"us": (g1, r1), "employees": (g2, r2), "b2b_saas": (g3, r3),
                 "company_type": (g4, r4), "ability_to_pay": (g5, r5)}
        failed = [k for k, (g, _) in gates.items() if g == REJECT]
        conds = [k for k, (g, _) in gates.items() if g == COND]

        base = {
            "canonical_company_id": rec["canonical_company_id"],
            "source_row_ids": rec["source_row_ids"],
            "company_name": rec["company_name_original"],
            "company_name_normalized": rec["company_name_normalized"],
            "domain": rec["domain_normalized"],
            "website_url": rec["website_url"],
            "linkedin_company_url": rec["linkedin_company_url"],
            "linkedin_slug": rec["linkedin_slug"],
            "country": rec["country_normalized"],
            "locality": rec["locality"],
            "employee_headcount_numeric": rec["employee_headcount_numeric"],
            "employee_range": rec["employee_range_normalized"],
            "employee_conflict": rec["employee_conflict"],
            "revenue_band": rec["revenue_band_original"],
            "funding_band": rec["funding_band_original"],
            "company_type": rec["company_type"],
            "business_type": rec["business_type"],
            "industry": rec["industry"],
            "subindustry": rec["subindustry"],
            "founded_year": rec["founded_year"],
            "follower_count": rec["follower_count"],
            "description": (rec["description"] or "")[:900],
            "derived_description": (rec.get("derived_description") or "")[:900],
            "linkedin_enrichment_suspect": rec.get("linkedin_enrichment_suspect"),
            "company_name_source": rec.get("company_name_source"),
            "merge_field_conflicts": rec.get("merge_field_conflicts"),
        }
        for k, (g, why) in gates.items():
            base[f"gate_{k}"] = g
            base[f"gate_{k}_reason"] = why

        if failed:
            gate_counter[f"reject:{failed[0]}"] += 1
            rejected.append({**base,
                             "rejection_stage": "local_prefilter",
                             "primary_rejection_reason": gates[failed[0]][1],
                             "primary_rejection_gate": failed[0],
                             "secondary_rejection_reasons": "; ".join(
                                 f"{k}: {gates[k][1]}" for k in failed[1:]),
                             "hard_disqualifier": failed[0] in {"us", "employees", "company_type"},
                             "research_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")})
            continue

        score, why = preliminary_score(rec)
        if str(rec.get("linkedin_enrichment_suspect")).lower() in ("true","1"):
            conds = list(dict.fromkeys(conds + ["enrichment"]))
            gates["enrichment"] = (COND,
                "source attached another company's LinkedIn page to this domain; name, HQ, "
                "size, description and industry were cleared - research from the domain up")
        tam = "probable" if not conds else "possible"
        afford = ("probable" if gates["ability_to_pay"][0] == RETAIN else "uncertain")
        prio = ("P1" if score >= 55 else "P2" if score >= 40 else "P3" if score >= 25 else "P4")
        gate_counter["queued"] += 1
        queue.append({**base,
                      "preliminary_tam_status": tam,
                      "preliminary_affordability_status": afford,
                      "preliminary_score": score,
                      "inclusion_reason": why or "passed all gates",
                      "conflicts_requiring_verification": "; ".join(
                          f"{k}: {gates[k][1]}" for k in conds),
                      "conditional_gate_count": len(conds),
                      "research_status": "Pending",
                      "research_priority": prio})

    C.OUTPUTS.mkdir(parents=True, exist_ok=True)
    qdf = pd.DataFrame(queue).sort_values(
        ["research_priority", "preliminary_score"], ascending=[True, False])
    qdf.insert(0, "queue_rank", range(1, len(qdf) + 1))
    qdf.to_csv(OUT_QUEUE, index=False)
    rdf = pd.DataFrame(rejected)
    rdf.to_csv(OUT_REJECT, index=False)

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input_companies": int(n),
        "queued_for_research": int(len(qdf)),
        "locally_rejected": int(len(rdf)),
        "reconciliation_balances": bool(len(qdf) + len(rdf) == n),
        "rejection_by_gate": dict(Counter(rdf["primary_rejection_gate"])) if len(rdf) else {},
        "queue_by_priority": dict(Counter(qdf["research_priority"])) if len(qdf) else {},
        "queue_conditional_gate_counts": dict(Counter(qdf["conditional_gate_count"])) if len(qdf) else {},
        "queue_score_describe": {k: float(v) for k, v in qdf["preliminary_score"].describe().items()} if len(qdf) else {},
    }
    REPORT.write_text(json.dumps(report, indent=2))
    print(f"\nQueued:   {len(qdf):,}")
    print(f"Rejected: {len(rdf):,}")
    print(json.dumps(report["rejection_by_gate"], indent=2))
    print(json.dumps(report["queue_by_priority"], indent=2))


if __name__ == "__main__":
    main()
