#!/usr/bin/env python3
"""Stage 4b: strict second-stage local qualification over the 57,673-company queue.

The first prefilter was deliberately broad. This pass is deliberately narrow: it
uses only existing dataset fields to isolate companies with a high prior of
qualifying, so that scarce web-research capacity is spent where it pays.

Every company in the old queue lands in exactly one bucket:

  already_researched      - the 72 completed records, never re-evaluated
  strict                  - passes every strict rule cleanly
  headcount_conflict      - numeric headcount contradicts the size band
  affordability_exception - retained on funding/scale rather than a retain-band revenue
  newly_rejected          - fails a strict rule

Precedence: already_researched > newly_rejected > headcount_conflict >
affordability_exception > strict. A hard failure (country, company type, business
model, dead domain, corrupted layer) outranks a soft flag, so nothing that fails a
mandatory rule can be smuggled into a verification queue.

Outputs: outputs/02b_strict_high_probability_queue.csv
         outputs/02b_headcount_conflicts.csv
         outputs/02b_affordability_exceptions.csv
         outputs/02b_newly_rejected.csv
         outputs/02b_filter_summary.md
"""
from __future__ import annotations
import sys, csv, json, re, sqlite3
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
import pandas as pd

QUEUE = C.OUTPUTS / "02_prefiltered_research_queue.csv"
DEDUP = C.OUTPUTS / "01_deduplicated_companies.csv"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

RETAIN_REV = {"1M-5M", "5M-10M", "10M-25M", "25M-75M"}
EXCEPTION_REV = {"500K-1M", ""}
LOW_REV = {"0-500K"}
TOO_BIG_REV = {"75M-200M", "200M-500M", "500M-1B", "1B-10B", "10B-100B", "100B-1T"}

EXCLUDE_TYPES = {"public company", "government agency", "non profit", "nonprofit",
                 "educational", "self employed"}

# ------------------------------------------------------------------ signals --
SAAS_RE = re.compile(
    r"\b(saas|software[- ]as[- ]a[- ]service|cloud[- ]?based software|cloud software|"
    r"enterprise software|subscription software|software platform|our platform|"
    r"our software|the platform|web[- ]based platform|software solution|"
    r"cloud platform|platform that|platform for|api platform|data platform)\b", re.I)
PLATFORM_RE = re.compile(r"\bplatform\b", re.I)
RECURRING_RE = re.compile(r"\b(subscription|recurring revenue|per user per month|"
                          r"monthly plan|annual plan|seats?|licen[cs]e)\b", re.I)
B2B_TEXT_RE = re.compile(
    r"\b(businesses|companies|enterprises?|organi[sz]ations|teams|b2b|"
    r"our clients|our customers|firms|operators|manufacturers|retailers|"
    r"providers|practices|agencies|departments|institutions)\b", re.I)

# Disqualifying business models. Matched against industry + description text, and
# only allowed to fire when no strong SaaS product signal is present.
AGENCY_RE = re.compile(
    r"\b(marketing agency|digital agency|creative agency|advertising agency|"
    r"branding agency|seo agency|web design|website design|design agency|"
    r"pr agency|public relations agency|media agency|content agency)\b", re.I)
SERVICES_RE = re.compile(
    r"\b(staffing|recruitment agency|recruiting agency|staff augmentation|"
    r"outsourcing|offshore development|it services|managed services provider|msp|"
    r"custom software development|bespoke software|software development services|"
    r"development agency|consultancy|consulting firm|systems integrator|"
    r"body shop|talent solutions|payroll services)\b", re.I)
HARDWARE_RE = re.compile(
    r"\b(manufactur\w+ of|hardware manufacturer|we manufacture|our devices|"
    r"equipment manufacturer|machinery|fabrication|assembly line|sensors? hardware|"
    r"industrial equipment)\b", re.I)
B2C_RE = re.compile(
    r"\b(consumers?|shoppers?|for individuals|personal finance app|dating|"
    r"mobile game|gaming app|fitness app|recipe|travel booking|social network for)\b", re.I)

EXCLUDE_INDUSTRY = {
    "advertising services", "marketing services", "design services",
    "public relations and communications services", "staffing and recruiting",
    "human resources services", "outsourcing and offshoring consulting",
    "translation and localization", "graphic design", "photography",
    "writing and editing", "market research", "business consulting and services",
    "it services and it consulting", "information technology and services",
    "it system custom software development", "management consulting",
    "venture capital and private equity principals", "investment management",
    "real estate", "staffing & recruiting", "professional training and coaching",
}
# Industries that are software-native and never trip the services exclusion.
SOFTWARE_INDUSTRY = {
    "software development", "computer software", "computer and network security",
    "data infrastructure and analytics", "technology, information and internet",
}
SOFTWARE_SUBIND_RE = re.compile(
    r"(Enterprise Software|Developer Tools|AI and ML Platforms|Data and Analytics Software|"
    r"Healthcare Software|Financial Services Software|Security and Identity Software|"
    r"Logistics Technology|Manufacturing Software|Retail Technology|PropTech|"
    r"E-Learning Platforms|Marketing Technology|Sales Technology|HR Tech|SaaS|"
    r"Software|Platforms)", re.I)
# Names that announce the company is already owned by someone else. The comma form
# ("Syxsense, An Absolute Security Company") and the parenthetical form
# ("Wonder Dynamics (an Autodesk Company)") are both common, as are dash and pipe
# separators, so all four are matched.
ACQUIRED_NAME_RE = re.compile(
    r"([,\-|(\[]\s*(an?|part of)\s+[\w\s&.\-']{2,40}?\s*(company|group|brand|business)\b"
    r"|\bacquired by\b|\(acquired\)|\ban?\s+[\w\s&.\-']{2,40}?\s+company\s*[)\]]?\s*$)", re.I)

def txt(r, *keys):
    return " ".join(str(r.get(k) or "") for k in keys)


def classify(r, researched_ids):
    """Return (bucket, reason, detail_dict)."""
    cid = r["canonical_company_id"]
    if cid in researched_ids:
        return "already_researched", "completed in a previous run - preserved", {}

    hard = []   # hard rejections
    soft = {}   # soft flags

    # ---------------------------------------------------------- rule 6: hygiene
    if str(r.get("linkedin_enrichment_suspect")).lower() in ("true", "1"):
        hard.append("corrupted LinkedIn/company layer - name, HQ, size and description "
                    "were cleared by the enrichment repair, so no strict local judgement "
                    "is possible from dataset fields alone")
    dom = str(r.get("domain") or "").strip().lower()
    if not dom or "." not in dom:
        hard.append(f"dead or invalid domain ('{dom}')")
    elif dom in C.PLATFORM_DOMAINS or any(dom.endswith("." + p) for p in C.PLATFORM_DOMAINS):
        hard.append(f"domain is a shared site-builder host, not a company domain ('{dom}')")
    name = str(r.get("company_name") or "")
    if ACQUIRED_NAME_RE.search(name):
        hard.append(f"company name indicates it is already part of another company ('{name}')")

    # ------------------------------------------------------------ rule 1: country
    country = str(r.get("country") or "").strip()
    if country != "United States":
        hard.append(f"Country is '{country or '(blank)'}', not United States")

    # ------------------------------------------------------- rule 3: company type
    ctype = str(r.get("company_type") or "").strip()
    low = ctype.lower()
    hc_raw = r.get("employee_headcount_numeric")
    hc = None
    try:
        hc = None if hc_raw in (None, "", "nan") or pd.isna(hc_raw) else int(float(hc_raw))
    except (TypeError, ValueError):
        hc = None
    band = str(r.get("employee_range") or "").strip()
    if low in EXCLUDE_TYPES:
        hard.append(f"Company Type is {ctype}")
    elif low == "self owned":
        if band.lower() in {"self-employed", "0-1 employees", "2-10 employees"} or (hc is not None and 0 < hc <= 2):
            hard.append("Self Owned at individual scale")
        else:
            soft["company_type"] = "Self Owned at operating scale - kept only on other evidence"

    # --------------------------------------------------------- rule 2: employees
    band_is_target = band.lower() == "11-50 employees"
    hc_known = hc is not None and hc > 0
    hc_in = hc_known and 11 <= hc <= 50
    headcount_conflict = False
    if hc_in and band and not band_is_target:
        headcount_conflict = True
        soft["headcount"] = f"headcount {hc} is inside 11-50 but the band says '{band}'"
    elif hc_known and not hc_in and band_is_target:
        headcount_conflict = True
        soft["headcount"] = f"band is '11-50 employees' but headcount is {hc}"
    elif hc_in:
        pass                                    # clean pass
    elif not hc_known and band_is_target:
        pass                                    # explicitly allowed by the rules
    else:
        hard.append(f"employee size fails the strict rule (headcount "
                    f"{hc if hc_known else 'missing/zero'}, band '{band or '(blank)'}')")

    # ---------------------------------------------------- rule 4: business model
    blob = txt(r, "description", "derived_description", "specialties", "pattern_tags",
               "subindustry", "derived_industry", "industry", "company_name")
    tags = {t.strip().lower() for t in str(r.get("pattern_tags") or "").split(",") if t.strip()}
    btype = str(r.get("business_type") or "").upper()
    industry = str(r.get("industry") or "").strip().lower()
    subind = str(r.get("subindustry") or "")

    b2b = []
    if "B2B" in btype:
        b2b.append("Business Type contains B2B")
    if "b2b" in tags:
        b2b.append("Pattern Tags contain B2B")
    if not b2b and B2B_TEXT_RE.search(blob):
        b2b.append("description addresses businesses/teams/organisations")

    saas = []
    if "saas" in tags:
        saas.append("Pattern Tags contain SaaS")
    if SAAS_RE.search(blob):
        saas.append("explicit SaaS / cloud / enterprise-software / platform language")
    if SOFTWARE_SUBIND_RE.search(subind):
        saas.append(f"SubIndustry is software/platform ({subind[:50]})")
    if RECURRING_RE.search(blob):
        saas.append("recurring/subscription/licence language")
    if not saas and PLATFORM_RE.search(blob) and industry in SOFTWARE_INDUSTRY:
        saas.append("platform language in a software-native industry")

    strong_saas = bool(saas)
    if btype == "B2C" and "B2B" not in btype:
        hard.append("Business Type is B2C only")
    if btype == "NONPROFIT":
        hard.append("Business Type is Nonprofit")
    if not b2b:
        hard.append("no B2B evidence in Business Type, Pattern Tags or description")
    if not strong_saas:
        hard.append("no SaaS / cloud / enterprise-software / platform / subscription evidence")

    # Disqualifying models, only when no strong SaaS product signal offsets them.
    if not strong_saas or industry in EXCLUDE_INDUSTRY:
        if industry in EXCLUDE_INDUSTRY and not (SOFTWARE_SUBIND_RE.search(subind) and "saas" in tags):
            hard.append(f"Industry '{r.get('industry')}' is an excluded services/agency category")
    if AGENCY_RE.search(blob) and not ("saas" in tags or SOFTWARE_SUBIND_RE.search(subind)):
        hard.append("description reads as an agency")
    if SERVICES_RE.search(blob) and not ("saas" in tags or SOFTWARE_SUBIND_RE.search(subind)):
        hard.append("description reads as consulting / custom development / outsourcing / staffing")
    if HARDWARE_RE.search(blob) and not ("saas" in tags):
        hard.append("description reads as hardware-first")
    if B2C_RE.search(blob) and "B2B" not in btype:
        hard.append("description reads as a consumer product")

    # ------------------------------------------------------ rule 5: ability to pay
    rev = str(r.get("revenue_band") or "").strip()
    fund = str(r.get("funding_band") or "").strip()
    fund_lo, _ = None, None
    _b, fund_lo, _hi = C.parse_funding(fund)
    fund_1m = fund_lo is not None and fund_lo >= 1_000_000
    established = (hc is not None and 20 <= hc <= 50) and strong_saas and bool(b2b)

    affordability_exception = False
    if rev in RETAIN_REV:
        pass
    elif rev in TOO_BIG_REV:
        hard.append(f"estimated revenue {rev} is far above the target band and implausible "
                    f"for an 11-50 headcount")
    elif rev in EXCEPTION_REV:
        if fund_1m:
            affordability_exception = True
            soft["affordability"] = f"revenue {rev or '(missing)'} retained on funding {fund}"
        elif established:
            affordability_exception = True
            soft["affordability"] = (f"revenue {rev or '(missing)'} retained on operating scale "
                                     f"(headcount {hc}, strong B2B SaaS signals)")
        else:
            hard.append(f"revenue {rev or '(missing)'} with no funding of $1M+ and no "
                        f"strong operating-scale evidence")
    elif rev in LOW_REV:
        if fund_1m:
            affordability_exception = True
            soft["affordability"] = f"revenue 0-500K contradicted by funding {fund}"
        else:
            hard.append("revenue 0-500K with no meaningful funding to contradict it")
    else:
        hard.append(f"revenue band '{rev}' unrecognised")

    if soft.get("company_type") and not (strong_saas and (rev in RETAIN_REV or fund_1m)):
        hard.append("Self Owned without strong operating-company evidence")

    detail = {"b2b_signals": "; ".join(b2b), "saas_signals": "; ".join(saas),
              "soft_flags": "; ".join(f"{k}: {v}" for k, v in soft.items())}

    if hard:
        return "newly_rejected", " | ".join(hard), detail
    if headcount_conflict:
        return "headcount_conflict", soft["headcount"], detail
    if affordability_exception:
        return "affordability_exception", soft["affordability"], detail
    return "strict", "passes every strict rule", detail


def main():
    print("Loading queue and full field set ...")
    q = pd.read_csv(QUEUE, dtype=str, keep_default_na=False, low_memory=False)
    queue_ids = set(q["canonical_company_id"])
    print(f"  old queue: {len(q):,}")

    ded = pd.read_csv(DEDUP, dtype=str, keep_default_na=False, low_memory=False)
    ded = ded[ded["canonical_company_id"].isin(queue_ids)].copy()
    print(f"  joined full fields: {len(ded):,}")

    rank = dict(zip(q["canonical_company_id"], q["queue_rank"]))
    prelim = dict(zip(q["canonical_company_id"], q["preliminary_score"]))

    conn = sqlite3.connect(C.DB_PATH)
    researched = {r[0] for r in conn.execute(
        "SELECT canonical_company_id FROM companies WHERE research_status != 'Pending'")}
    print(f"  already researched (preserved): {len(researched):,}")

    ded = ded.rename(columns={
        "company_name_original": "company_name", "domain_normalized": "domain",
        "country_normalized": "country", "employee_range_normalized": "employee_range",
        "revenue_band_original": "revenue_band", "funding_band_original": "funding_band"})

    buckets = defaultdict(list)
    reject_reasons = Counter()
    for r in ded.to_dict("records"):
        cid = r["canonical_company_id"]
        bucket, reason, detail = classify(r, researched)
        row = {
            "canonical_company_id": cid,
            "old_queue_rank": rank.get(cid, ""),
            "preliminary_score": prelim.get(cid, ""),
            "company_name": r.get("company_name", ""),
            "domain": r.get("domain", ""),
            "website_url": r.get("website_url", ""),
            "linkedin_company_url": r.get("linkedin_company_url", ""),
            "linkedin_slug": r.get("linkedin_slug", ""),
            "country": r.get("country", ""),
            "locality": r.get("locality", ""),
            "employee_headcount_numeric": r.get("employee_headcount_numeric", ""),
            "employee_range": r.get("employee_range", ""),
            "company_type": r.get("company_type", ""),
            "business_type": r.get("business_type", ""),
            "revenue_band": r.get("revenue_band", ""),
            "funding_band": r.get("funding_band", ""),
            "industry": r.get("industry", ""),
            "subindustry": r.get("subindustry", ""),
            "pattern_tags": r.get("pattern_tags", ""),
            "founded_year": r.get("founded_year", ""),
            "follower_count": r.get("follower_count", ""),
            "b2b_signals": detail.get("b2b_signals", ""),
            "saas_signals": detail.get("saas_signals", ""),
            "bucket": bucket,
            "bucket_reason": reason,
            "description": (r.get("description") or "")[:600],
            "derived_description": (r.get("derived_description") or "")[:600],
            "filter_date": TODAY,
        }
        buckets[bucket].append(row)
        if bucket == "newly_rejected":
            reject_reasons[reason.split(" | ")[0][:90]] += 1

    # ------------------------------------------------- strict ranking + output --
    def rev_rank(b):
        return {"5M-10M": 0, "10M-25M": 1, "1M-5M": 2, "25M-75M": 3}.get(b, 4)

    strict = buckets["strict"]
    strict.sort(key=lambda x: (rev_rank(x["revenue_band"]),
                               -float(x["preliminary_score"] or 0)))
    for i, row in enumerate(strict, 1):
        row["strict_rank"] = i
    cols = ["strict_rank"] + [c for c in (strict[0].keys() if strict else []) if c != "strict_rank"]

    def write(path, rows, first=None):
        if not rows:
            path.write_text("")
            return 0
        keys = first if first else list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        return len(rows)

    n_strict = write(C.OUTPUTS / "02b_strict_high_probability_queue.csv", strict, cols)
    for b in ("headcount_conflict", "affordability_exception"):
        buckets[b].sort(key=lambda x: -float(x["preliminary_score"] or 0))
    n_hc = write(C.OUTPUTS / "02b_headcount_conflicts.csv", buckets["headcount_conflict"])
    n_af = write(C.OUTPUTS / "02b_affordability_exceptions.csv", buckets["affordability_exception"])
    n_rj = write(C.OUTPUTS / "02b_newly_rejected.csv", buckets["newly_rejected"])
    n_ar = len(buckets["already_researched"])

    total = n_strict + n_hc + n_af + n_rj + n_ar
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "old_queue": int(len(q)),
        "already_researched": n_ar,
        "strict_high_probability_queue": n_strict,
        "headcount_conflicts": n_hc,
        "affordability_exceptions": n_af,
        "newly_rejected": n_rj,
        "sum_of_buckets": total,
        "balances": total == len(q),
        "top_rejection_reasons": reject_reasons.most_common(20),
        "strict_revenue_mix": dict(Counter(x["revenue_band"] for x in strict)),
        "strict_company_type_mix": dict(Counter(x["company_type"] for x in strict)),
    }
    (C.DATA / "interim" / "strict_filter_report.json").write_text(json.dumps(report, indent=2))

    # --------------------------------------------- write bucket back to sqlite --
    conn.execute("CREATE TABLE IF NOT EXISTS strict_bucket ("
                 "canonical_company_id TEXT PRIMARY KEY, bucket TEXT, strict_rank INTEGER, "
                 "bucket_reason TEXT)")
    conn.execute("DELETE FROM strict_bucket")
    rows = [(r["canonical_company_id"], b, r.get("strict_rank"), r["bucket_reason"])
            for b in buckets for r in buckets[b]]
    conn.executemany("INSERT INTO strict_bucket VALUES (?,?,?,?)", rows)
    conn.commit()
    conn.close()

    print(f"\nalready researched (untouched) : {n_ar:,}")
    print(f"strict high-probability queue  : {n_strict:,}")
    print(f"headcount conflicts            : {n_hc:,}")
    print(f"affordability exceptions       : {n_af:,}")
    print(f"newly rejected                 : {n_rj:,}")
    print(f"sum                            : {total:,} / {len(q):,}  balances={report['balances']}")
    print("\ntop rejection reasons:")
    for reason, n in reject_reasons.most_common(12):
        print(f"  {n:>7,}  {reason}")


if __name__ == "__main__":
    main()
