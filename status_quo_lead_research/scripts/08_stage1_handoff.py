#!/usr/bin/env python3
"""Stage 1: export every existing qualified founder contact for immediate outreach.

Read-only over the research state. Nothing is re-scored, re-researched, reclassified
or removed. Existing priority tiers are preserved exactly as recorded; the Stage 2
scoring bands are deliberately NOT applied here, and the difference is reported in
the handoff instead.

Outputs: outputs/00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv
         outputs/00_PRIORITY_A_CONTACTS.csv
         outputs/00_PRIORITY_B_CONTACTS.csv
         outputs/00_EXISTING_81_HANDOFF.md
"""
from __future__ import annotations
import sys, csv, sqlite3, re, collections
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
csv.field_size_limit(sys.maxsize)

UNV = "unverified"
COLUMNS = [
    "outreach_rank", "priority", "total_score", "company_name", "company_domain",
    "company_website", "company_linkedin_url", "founder_name", "founder_first_name",
    "founder_last_name", "founder_current_title", "founder_linkedin_url",
    "founder_location", "company_hq", "us_based_status", "employee_count",
    "employee_range", "estimated_revenue", "total_funding", "company_status",
    "business_model", "b2b_saas_evidence", "affordability_evidence",
    "founder_market_authority", "founder_content_activity", "content_gap",
    "status_quo_need", "buying_trigger", "personalized_outreach_angle",
    "qualification_reason", "disqualification_risks", "verification_status",
    "last_verified_date", "primary_evidence_url", "additional_evidence_urls",
    "research_notes",
]
GENERIC = ["you are doing great work", "i liked your profile", "loved your journey",
           "i help founders", "looks interesting", "you should post more",
           "noticed you are a saas founder", "great work"]

def clean(v):
    """Never emit a blank or a placeholder-looking value; say unverified instead."""
    if v is None:
        return UNV
    s = str(v).strip()
    if not s or s.lower() in {"none", "nan", "n/a", "na", "not established", ""}:
        return UNV
    return s

def split_name(full):
    parts = [p for p in str(full or "").split() if p]
    if not parts:
        return UNV, UNV
    if len(parts) == 1:
        return parts[0], UNV
    return parts[0], parts[-1]

def tier_of(score, recorded):
    """Preserve the recorded tier. Only derive when one was never written."""
    if recorded:
        return recorded
    if score is None:
        return "C"
    return "A" if score >= 85 else "B" if score >= 70 else "C"


def build():
    conn = sqlite3.connect(C.DB_PATH)
    conn.row_factory = sqlite3.Row

    companies = {r["canonical_company_id"]: dict(r) for r in
                 conn.execute("SELECT * FROM companies WHERE research_status='Qualified'")}
    founders = [dict(r) for r in conn.execute(
        "SELECT * FROM founders WHERE canonical_company_id IN "
        "(SELECT canonical_company_id FROM companies WHERE research_status='Qualified')")]

    # Founder rows attached to a company that is NOT qualified, i.e. any Needs
    # Verification contacts that already exist in the founder list.
    nv_founders = [dict(r) for r in conn.execute(
        "SELECT f.* FROM founders f JOIN companies c USING(canonical_company_id) "
        "WHERE c.research_status='Needs Verification'")]

    ev_by_co = collections.defaultdict(list)
    ev_by_founder = collections.defaultdict(list)
    for e in conn.execute("SELECT * FROM evidence"):
        ev_by_co[e["canonical_company_id"]].append(dict(e))
        if e["founder_name"]:
            ev_by_founder[(e["canonical_company_id"], e["founder_name"])].append(dict(e))

    # tier from the existing exported founder file, so nothing is re-derived
    recorded_tier = {}
    p = C.OUTPUTS / "04_all_qualified_status_quo_founder_leads.csv"
    if p.exists():
        for r in csv.DictReader(p.open()):
            recorded_tier[(r["co_company_name"], r["full_name"])] = r["priority_tier"]

    def row_for(f, co, bucket_label=None):
        cid = f["canonical_company_id"]
        score = f["final_score"] if f["final_score"] is not None else co["final_score"]
        tier = bucket_label or tier_of(score, recorded_tier.get((co["company_name"], f["full_name"])))
        first, last = split_name(f["full_name"])

        urls, seen = [], set()
        for e in ev_by_founder.get((cid, f["full_name"]), []) + ev_by_co.get(cid, []):
            u = (e.get("source_url") or "").strip()
            if u and u not in seen:
                seen.add(u); urls.append(u)

        hq = ", ".join(x for x in [clean(co["hq_city"]), clean(co["hq_state"]),
                                   clean(co["hq_country"])] if x != UNV) or UNV
        us_status = (f"US-based ({clean(co['hq_confidence'])} confidence)"
                     if (co["hq_country"] or "").startswith("United States")
                     else f"{clean(co['hq_country'])} ({clean(co['hq_confidence'])} confidence)")

        b2b = f"{clean(co['b2b_saas_confidence'])} confidence: {clean(co['business_model'])}. " \
              f"{clean(co['product_summary'])}"
        afford = f"{clean(co['ability_to_pay'])}: {clean(co['ability_to_pay_reason'])}"
        trigger = clean(f.get("recent_founder_trigger"))
        if trigger == UNV:
            t, d = clean(co["recent_trigger"]), clean(co["trigger_date"])
            trigger = f"{t} ({d})" if t != UNV and d != UNV else t

        qual = (f"TAM: {clean(co['tam_status'])}; {clean(co['saas_category'])} sold to "
                f"{clean(co['target_customer'])}. Size: {clean(co['employee_range_verified'])} "
                f"(confidence {clean(co['employee_confidence'])}). HQ: {hq} "
                f"({clean(co['hq_confidence'])}). Ability to pay: {clean(co['ability_to_pay'])}. "
                f"Buyer: {clean(f['exact_title'])}, {clean(f['founder_status'])}.")

        risks = []
        if clean(co["penalties"]) not in (UNV, "none"):
            risks.append(f"penalties applied: {co['penalties']}")
        if clean(co["hard_disqualifier"]) not in (UNV, "none"):
            risks.append(f"hard disqualifier flag: {co['hard_disqualifier']}")
        if clean(co["employee_confidence"]) in ("Low",):
            risks.append("employee count not independently verified")
        if clean(co["hq_confidence"]) in ("Low", "Conflicting"):
            risks.append("headquarters not firmly established")
        if clean(f.get("still_operational")).lower().startswith("requires"):
            risks.append("founder's current operational role not confirmed")
        if clean(f.get("linkedin_url")) in (UNV,):
            risks.append("founder LinkedIn URL not captured")
        risks.append("LinkedIn posting activity could not be inspected from the research "
                     "environment, so content-gap fields are inference not observation")

        vstat = (f"research confidence {clean(co['research_confidence'])}; "
                 f"LinkedIn activity {UNV}; "
                 f"founder profile URL "
                 f"{'captured' if clean(f.get('linkedin_url')) != UNV else UNV}")

        notes = " || ".join(x for x in [clean(f.get("research_notes")),
                                        clean(co.get("research_notes"))] if x != UNV) or UNV

        return {
            "outreach_rank": 0,
            "priority": tier,
            "total_score": score if score is not None else UNV,
            "company_name": clean(co["company_name"]),
            "company_domain": clean(co["domain"]),
            "company_website": clean(co["website_url"]),
            "company_linkedin_url": clean(co["linkedin_company_url"]),
            "founder_name": clean(f["full_name"]),
            "founder_first_name": first,
            "founder_last_name": last,
            "founder_current_title": clean(f["exact_title"]),
            "founder_linkedin_url": clean(f.get("linkedin_url")),
            "founder_location": clean(f.get("location")),
            "company_hq": hq,
            "us_based_status": us_status,
            "employee_count": clean(co["employee_estimate"]),
            "employee_range": clean(co["employee_range_verified"]),
            "estimated_revenue": clean(co["revenue_estimate"]),
            "total_funding": clean(co["funding_total"]),
            "company_status": clean(co["company_status"]),
            "business_model": clean(co["business_model"]),
            "b2b_saas_evidence": b2b,
            "affordability_evidence": afford,
            "founder_market_authority": clean(f.get("expertise")),
            "founder_content_activity": clean(f.get("activity_class")),
            "content_gap": clean(f.get("content_gap")),
            "status_quo_need": clean(f.get("content_opportunity")),
            "buying_trigger": trigger,
            "personalized_outreach_angle": clean(f.get("outreach_angle")),
            "qualification_reason": qual,
            "disqualification_risks": "; ".join(risks),
            "verification_status": vstat,
            "last_verified_date": clean(co["research_date"]),
            "primary_evidence_url": urls[0] if urls else UNV,
            "additional_evidence_urls": " | ".join(urls[1:]) if len(urls) > 1 else UNV,
            "research_notes": notes,
        }

    rows = [row_for(f, companies[f["canonical_company_id"]]) for f in founders]
    nv_rows = []
    if nv_founders:
        nv_cos = {r["canonical_company_id"]: dict(r) for r in
                  conn.execute("SELECT * FROM companies WHERE research_status='Needs Verification'")}
        nv_rows = [row_for(f, nv_cos[f["canonical_company_id"]], "Needs Verification")
                   for f in nv_founders]

    order = {"A": 0, "B": 1, "C": 2, "Needs Verification": 3}
    allrows = rows + nv_rows
    allrows.sort(key=lambda r: (order.get(r["priority"], 9),
                                -(r["total_score"] if isinstance(r["total_score"], int) else 0),
                                r["company_name"]))
    for i, r in enumerate(allrows, 1):
        r["outreach_rank"] = i

    def write(path, data):
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
            w.writeheader(); w.writerows(data)
        return len(data)

    n_all = write(C.OUTPUTS / "00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv", allrows)
    a_rows = [r for r in allrows if r["priority"] == "A"]
    b_rows = [r for r in allrows if r["priority"] == "B"]
    for i, r in enumerate(a_rows, 1): r["outreach_rank"] = i
    n_a = write(C.OUTPUTS / "00_PRIORITY_A_CONTACTS.csv", a_rows)
    for i, r in enumerate(b_rows, 1): r["outreach_rank"] = i
    n_b = write(C.OUTPUTS / "00_PRIORITY_B_CONTACTS.csv", b_rows)
    # restore global ranks after the per-file renumbering
    for i, r in enumerate(allrows, 1): r["outreach_rank"] = i
    write(C.OUTPUTS / "00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv", allrows)

    conn.close()
    return allrows, nv_rows, n_all, n_a, n_b, companies, founders


def validate(rows, companies, founders):
    fails = []
    li = [r["founder_linkedin_url"] for r in rows if r["founder_linkedin_url"] != UNV]
    dup_li = [u for u, n in collections.Counter(li).items() if n > 1]
    if dup_li: fails.append(f"duplicate founder LinkedIn URLs: {dup_li}")
    pair = collections.Counter((r["founder_name"], r["company_name"]) for r in rows)
    dup_pair = [k for k, n in pair.items() if n > 1]
    if dup_pair: fails.append(f"duplicate founder+company pairs: {dup_pair}")
    blank = [r["outreach_rank"] for r in rows if r["company_name"] == UNV]
    if blank: fails.append(f"blank company names at ranks {blank}")
    with_f = {f["canonical_company_id"] for f in founders}
    missing = [c["company_name"] for cid, c in companies.items() if cid not in with_f]
    if missing: fails.append(f"qualified companies with no founder: {missing}")
    a_no_reason = [r["founder_name"] for r in rows
                   if r["priority"] == "A" and (r["qualification_reason"] == UNV
                                                or len(r["qualification_reason"]) < 40)]
    if a_no_reason: fails.append(f"Priority A without qualification reason: {a_no_reason}")
    gen = [r["founder_name"] for r in rows
           if any(g in r["personalized_outreach_angle"].lower() for g in GENERIC)
           or r["personalized_outreach_angle"] == UNV]
    if gen: fails.append(f"generic or missing outreach angle: {gen}")
    noev = [r["founder_name"] for r in rows if r["primary_evidence_url"] == UNV]
    if noev: fails.append(f"contacts with no evidence URL: {noev}")
    blanks = [(r["outreach_rank"], k) for r in rows for k, v in r.items()
              if v is None or str(v).strip() == ""]
    if blanks: fails.append(f"empty cells (should be 'unverified'): {blanks[:5]}")
    if len(rows) < len(founders):
        fails.append(f"contacts lost: {len(founders)} founders in DB, {len(rows)} exported")
    return fails


if __name__ == "__main__":
    rows, nv_rows, n_all, n_a, n_b, companies, founders = build()
    fails = validate(rows, companies, founders)
    print(f"exported : {n_all} contacts  (Priority A {n_a}, Priority B {n_b}, "
          f"C {sum(1 for r in rows if r['priority']=='C')}, "
          f"Needs Verification {len(nv_rows)})")
    print(f"companies: {len(companies)} qualified, {len(founders)} founder rows in DB")
    print(f"VALIDATION: {'ALL CHECKS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
    for f in fails:
        print("  !", f)
