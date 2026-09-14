#!/usr/bin/env python3
"""Stage 6: export every final output file from research_state.sqlite.

Produces outputs 03-08 and runs the reconciliation and validation checks.
Safe to run at any point: unresearched companies simply stay in the
unprocessed count, which the run summary reports honestly.
"""
from __future__ import annotations
import sys, csv, json, sqlite3
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW = datetime.now(timezone.utc).isoformat()

def tier(score):
    if score is None:
        return ""
    if score >= 85: return "A"
    if score >= 70: return "B"
    return "C"

def q(conn, sql, args=()):
    cur = conn.execute(sql, args)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]

def write(path, rows, cols):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def main():
    conn = sqlite3.connect(C.DB_PATH)
    C.OUTPUTS.mkdir(parents=True, exist_ok=True)

    total = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    qualified = q(conn, "SELECT * FROM companies WHERE research_status='Qualified' "
                        "ORDER BY final_score DESC, queue_rank")
    needs_ver = q(conn, "SELECT * FROM companies WHERE research_status='Needs Verification' "
                        "ORDER BY preliminary_score DESC")
    rejected  = q(conn, "SELECT * FROM companies WHERE research_status='Rejected' "
                        "ORDER BY queue_rank")
    blocked   = q(conn, "SELECT * FROM companies WHERE research_status='Blocked'")
    pending   = conn.execute("SELECT COUNT(*) FROM companies WHERE research_status='Pending'").fetchone()[0]

    ev_by_co = {}
    for e in q(conn, "SELECT canonical_company_id, source_url FROM evidence"):
        ev_by_co.setdefault(e["canonical_company_id"], []).append(e["source_url"])

    # ------------------------------------------- 03 company-level output ----
    for i, c in enumerate(qualified, 1):
        c["company_rank"] = i
        c["priority_tier"] = tier(c["final_score"])
        c["evidence_urls"] = " | ".join(ev_by_co.get(c["canonical_company_id"], []))
    COMPANY_COLS = [
        "company_rank","priority_tier","final_score","company_name","canonical_company_id",
        "domain","website_url","linkedin_company_url","source_row_ids","hq_city","hq_state",
        "hq_country","hq_confidence","employee_estimate","employee_range_verified",
        "employee_confidence","company_status","business_model","b2b_saas_confidence",
        "product_summary","target_customer","saas_category","sales_motion","pricing_motion",
        "customer_examples","revenue_estimate","revenue_confidence","funding_total",
        "latest_round","latest_round_date","recent_trigger","trigger_date",
        "trigger_evidence_url","internal_content_team","ability_to_pay",
        "ability_to_pay_reason","tam_status","company_fit_score","ability_to_pay_score",
        "timing_score","penalties","hard_disqualifier","final_classification",
        "research_confidence","evidence_count","founder_count","evidence_urls",
        "research_date","research_notes"]
    n03 = write(C.OUTPUTS / "03_all_qualified_status_quo_companies.csv", qualified, COMPANY_COLS)

    # ------------------------------------------- 04 founder-level output ----
    rank_of = {c["canonical_company_id"]: c["company_rank"] for c in qualified}
    co_by_id = {c["canonical_company_id"]: c for c in qualified}
    founders = q(conn, "SELECT * FROM founders WHERE canonical_company_id IN "
                       "(SELECT canonical_company_id FROM companies WHERE research_status='Qualified')")
    for f in founders:
        c = co_by_id[f["canonical_company_id"]]
        f["company_rank"] = c["company_rank"]
        f["priority_tier"] = tier(f["final_score"] if f["final_score"] is not None else c["final_score"])
        f["total_score"] = f["final_score"] if f["final_score"] is not None else c["final_score"]
        for k in ["company_name","domain","website_url","linkedin_company_url","hq_city",
                  "hq_state","hq_country","employee_range_verified","revenue_estimate",
                  "funding_total","ability_to_pay","business_model","saas_category",
                  "target_customer","sales_motion","internal_content_team","recent_trigger",
                  "ability_to_pay_reason","tam_status","research_confidence","research_date",
                  "company_fit_score","ability_to_pay_score","timing_score","penalties"]:
            f[f"co_{k}"] = c[k]
        f["verified_company_hq"] = f"{c['hq_city']}, {c['hq_state']}, {c['hq_country']}"
        f["evidence_urls"] = " | ".join(ev_by_co.get(f["canonical_company_id"], []))
        f["why_in_tam"] = (f"{c['business_model']} in {c['saas_category']}; "
                           f"{c['employee_range_verified']} employees; HQ {f['verified_company_hq']} "
                           f"({c['hq_confidence']} confidence)")
        f["why_can_pay"] = c["ability_to_pay_reason"]
    founders.sort(key=lambda f: (f["priority_tier"], -(f["total_score"] or 0),
                                 f["co_research_confidence"] or "", f["contact_rank"] or 9))
    for i, f in enumerate(founders, 1):
        f["overall_lead_rank"] = i
    FOUNDER_COLS = [
        "overall_lead_rank","company_rank","priority_tier","total_score","co_company_name",
        "co_domain","co_website_url","co_linkedin_company_url","verified_company_hq",
        "co_employee_range_verified","co_revenue_estimate","co_funding_total",
        "co_ability_to_pay","co_business_model","co_saas_category","co_target_customer",
        "co_sales_motion","full_name","exact_title","founder_status","contact_rank",
        "linkedin_url","location","role_in_business","still_operational","follower_count",
        "most_recent_post_date","posts_30d","posts_90d","posts_180d","activity_class",
        "content_topics","expertise","founder_story","content_style","content_consistency",
        "positioning_quality","content_gap","content_opportunity","raw_material",
        "ghostwriter_likelihood","co_internal_content_team","recent_founder_trigger",
        "co_recent_trigger","why_in_tam","why_can_pay","content_opportunity",
        "outreach_angle","public_email","email_verification","email_source_url",
        "alt_contact_route","co_company_fit_score","co_ability_to_pay_score",
        "content_need_score","founder_suitability_score","co_timing_score","co_penalties",
        "total_score","co_tam_status","qualification_status","co_research_confidence",
        "evidence_urls","co_research_date","research_notes"]
    seen, FCOLS = set(), []
    for c in FOUNDER_COLS:
        if c not in seen:
            seen.add(c); FCOLS.append(c)
    n04 = write(C.OUTPUTS / "04_all_qualified_status_quo_founder_leads.csv", founders, FCOLS)

    # ----------------------------------------------- 05 needs verification --
    for c in needs_ver:
        c["evidence_urls"] = " | ".join(ev_by_co.get(c["canonical_company_id"], []))
        unresolved = []
        if (c["hq_confidence"] or "") in ("Low", "Conflicting"): unresolved.append("headquarters")
        if (c["employee_confidence"] or "") in ("Low",) or "ABOVE" in (c["employee_range_verified"] or "") \
           or "above" in (c["employee_range_verified"] or ""): unresolved.append("employee count")
        if (c["ability_to_pay"] or "") == "Uncertain": unresolved.append("ability to pay")
        if (c["b2b_saas_confidence"] or "") in ("Low", "Medium"): unresolved.append("business model")
        # A Needs Verification company has no founder rows by construction, so an empty
        # founder_count proves nothing. Flag founder identity only where the research
        # actually recorded it as the open question.
        notes = (c["research_notes"] or "").lower()
        if any(k in notes for k in ("founder identity", "no founder is identified",
                                    "founder operational status", "founder status",
                                    "no operational founder", "founder control",
                                    "still operational", "founders no longer")):
            unresolved.append("founder identity / operational status")
        if not unresolved:
            unresolved.append("see research notes")
        c["unresolved_facts"] = "; ".join(unresolved)
        # Environment limitation, recorded separately so it never reads as a company-specific blocker.
        c["linkedin_activity_status"] = "not inspectable in this environment - unverified for every lead"
    NV_COLS = ["canonical_company_id","company_name","domain","website_url",
               "linkedin_company_url","unresolved_facts","linkedin_activity_status","hq_city","hq_state","hq_country",
               "hq_confidence","employee_estimate","employee_range_verified",
               "employee_confidence","business_model","b2b_saas_confidence","revenue_estimate",
               "funding_total","ability_to_pay","ability_to_pay_reason","tam_status",
               "hard_disqualifier","research_confidence","evidence_urls","research_date",
               "research_notes"]
    n05 = write(C.OUTPUTS / "05_needs_verification.csv", needs_ver, NV_COLS)

    # ------------------------------------------- 06 rejected after research --
    for c in rejected:
        c["rejection_stage"] = "web_research"
        c["primary_rejection_reason"] = c["hard_disqualifier"] or c["research_notes"] or ""
        c["secondary_rejection_reasons"] = c["research_notes"] or ""
        c["evidence_url"] = " | ".join(ev_by_co.get(c["canonical_company_id"], []))
    RJ_COLS = ["company_name","domain","canonical_company_id","source_row_ids",
               "rejection_stage","primary_rejection_reason","secondary_rejection_reasons",
               "hard_disqualifier","evidence_url","research_date"]
    n06 = write(C.OUTPUTS / "06_rejected_after_research.csv", rejected, RJ_COLS)

    # ------------------------------------------------- 07 research sources --
    sources = q(conn, """SELECT e.canonical_company_id, c.company_name AS company,
                                e.founder_name, e.source_url, e.source_type, e.page_title,
                                e.access_date, e.evidence_category, e.evidence_summary,
                                e.confidence, e.fact_or_inference
                         FROM evidence e JOIN companies c
                           ON c.canonical_company_id = e.canonical_company_id
                         ORDER BY c.company_name, e.evidence_id""")
    n07 = write(C.OUTPUTS / "07_research_sources.csv", sources,
                ["company","canonical_company_id","founder_name","source_url","source_type",
                 "page_title","access_date","evidence_category","evidence_summary",
                 "confidence","fact_or_inference"])

    # ------------------------------------------------------ 08 run summary --
    strict_report = {}
    sp = C.DATA / "interim" / "strict_filter_report.json"
    if sp.exists():
        strict_report = json.loads(sp.read_text())
    strict_pending = conn.execute(
        "SELECT COUNT(*) FROM strict_bucket s JOIN companies c USING(canonical_company_id) "
        "WHERE s.bucket='strict' AND c.research_status='Pending'").fetchone()[0] \
        if strict_report else 0
    audit = json.loads((C.OUTPUTS / "00_data_audit.json").read_text())
    ded = json.loads((C.DATA / "interim" / "dedupe_report.json").read_text())
    pre = json.loads((C.DATA / "interim" / "prefilter_report.json").read_text())
    researched = len(qualified) + len(needs_ver) + len(rejected) + len(blocked)
    tiers = Counter(tier(c["final_score"]) for c in qualified)

    summary = {
        "generated_utc": NOW, "research_date": TODAY,
        "counts": {
            "original_rows": audit["input"]["total_rows"],
            "deduplicated_companies": ded["canonical_companies"],
            "rows_absorbed_by_merging": ded["rows_absorbed_by_merging"],
            "locally_rejected": pre["locally_rejected"],
            "prefiltered_research_queue": pre["queued_for_research"],
            "fully_researched": researched,
            "qualified_companies": len(qualified),
            "qualified_founder_leads": n04,
            "priority_a": tiers.get("A", 0),
            "priority_b": tiers.get("B", 0),
            "priority_c": tiers.get("C", 0),
            "needs_verification": len(needs_ver),
            "rejected_after_research": len(rejected),
            "blocked_sources": len(blocked),
            "remaining_unprocessed_old_queue": pending,
            "strict_high_probability_queue": strict_report.get("strict_high_probability_queue"),
            "strict_queue_remaining": strict_pending,
            "headcount_verification_queue": strict_report.get("headcount_conflicts"),
            "affordability_exception_queue": strict_report.get("affordability_exceptions"),
            "deprioritised_by_strict_filter": strict_report.get("newly_rejected"),
            "duplicate_clusters_reviewed": ded["review_queue_clusters"],
            "enrichment_suspect_rows_repaired": ded["enrichment_repair"]["rows_flagged_suspect"],
        },
        "reconciliation": {
            "rows_to_companies": {
                "original_rows": audit["input"]["total_rows"],
                "canonical_companies_plus_absorbed":
                    ded["canonical_companies"] + ded["rows_absorbed_by_merging"],
                "balances": ded["canonical_companies"] + ded["rows_absorbed_by_merging"]
                            == audit["input"]["total_rows"]},
            "companies_to_queue": {
                "deduplicated_companies": ded["canonical_companies"],
                "locally_rejected_plus_queued": pre["locally_rejected"] + pre["queued_for_research"],
                "balances": pre["locally_rejected"] + pre["queued_for_research"]
                            == ded["canonical_companies"]},
            "queue_to_classification": {
                "queue": pre["queued_for_research"],
                "qualified_plus_needs_ver_plus_rejected_plus_blocked_plus_pending":
                    researched + pending,
                "balances": researched + pending == pre["queued_for_research"],
                "unprocessed_count": pending,
                "run_complete": pending == 0},
            "founder_rows_exceed_company_rows": n04 >= len(qualified),
            "founder_row_explanation":
                "A qualified company may yield more than one credible buyer, so the "
                "founder-level file can carry more rows than the company-level file.",
        },
        "validation": {},
    }

    # -------------------------------------------------------- validation ----
    v = summary["validation"]
    v["duplicate_domains_in_company_output"] = len(
        [d for d, k in Counter(c["domain"] for c in qualified).items() if k > 1])
    li = [f["linkedin_url"] for f in founders
          if f["linkedin_url"] and f["linkedin_url"] != "unverified"]
    v["duplicate_founder_linkedin_urls"] = len([u for u, k in Counter(li).items() if k > 1])
    v["qualified_without_evidence"] = len([c for c in qualified if not c["evidence_count"]])
    v["qualified_without_founder"] = len([c for c in qualified if not c["founder_count"]])
    v["qualified_with_low_confidence"] = len(
        [c for c in qualified if (c["research_confidence"] or "") not in ("High", "Medium")])
    v["qualified_non_us"] = len(
        [c for c in qualified if (c["hq_country"] or "") != "United States"])
    v["qualified_with_hard_disqualifier"] = len(
        [c for c in qualified if (c["hard_disqualifier"] or "none").lower() not in ("none", "")])
    v["scores_out_of_range"] = len(
        [c for c in qualified if c["final_score"] is None or not 0 <= c["final_score"] <= 100])
    v["tier_mismatches"] = len(
        [c for c in qualified if c["priority_tier"] != tier(c["final_score"])])
    v["all_checks_pass"] = all(x == 0 for k, x in v.items() if isinstance(x, int))

    (C.OUTPUTS / "08_run_summary.json").write_text(json.dumps(summary, indent=2))

    c_ = summary["counts"]; r_ = summary["reconciliation"]
    md = [
        "# Run summary — Status Quo US B2B SaaS founder lead research", "",
        f"Generated {NOW[:19]}Z · research date {TODAY}", "",
        "## Counts", "",
        "| Stage | Count |", "|---|---:|",
        f"| Original rows | {c_['original_rows']:,} |",
        f"| Deduplicated companies | {c_['deduplicated_companies']:,} |",
        f"| Rows absorbed by merging | {c_['rows_absorbed_by_merging']:,} |",
        f"| Locally rejected | {c_['locally_rejected']:,} |",
        f"| Prefiltered research queue | {c_['prefiltered_research_queue']:,} |",
        f"| Fully researched | {c_['fully_researched']:,} |",
        f"| Qualified companies | {c_['qualified_companies']:,} |",
        f"| Qualified founder leads | {c_['qualified_founder_leads']:,} |",
        f"| Priority A | {c_['priority_a']:,} |",
        f"| Priority B | {c_['priority_b']:,} |",
        f"| Priority C | {c_['priority_c']:,} |",
        f"| Needs Verification | {c_['needs_verification']:,} |",
        f"| Rejected after research | {c_['rejected_after_research']:,} |",
        f"| Blocked sources | {c_['blocked_sources']:,} |",
        f"| **Remaining unprocessed (old queue)** | **{c_['remaining_unprocessed_old_queue']:,}** |",
        "", "## Strict second-stage queue", "",
        "| Bucket | Count |", "|---|---:|",
        f"| **Strict high-probability queue** | **{(c_.get('strict_high_probability_queue') or 0):,}** |",
        f"| — of which still to research | {(c_.get('strict_queue_remaining') or 0):,} |",
        f"| Headcount verification | {(c_.get('headcount_verification_queue') or 0):,} |",
        f"| Affordability exception | {(c_.get('affordability_exception_queue') or 0):,} |",
        f"| Deprioritised by the strict filter | {(c_.get('deprioritised_by_strict_filter') or 0):,} |",
        "", "## Reconciliation", "",
        f"- Rows to companies: {c_['original_rows']:,} = "
        f"{c_['deduplicated_companies']:,} companies + {c_['rows_absorbed_by_merging']:,} absorbed "
        f"— **{'balances' if r_['rows_to_companies']['balances'] else 'DOES NOT BALANCE'}**",
        f"- Companies to queue: {c_['deduplicated_companies']:,} = "
        f"{c_['locally_rejected']:,} locally rejected + {c_['prefiltered_research_queue']:,} queued "
        f"— **{'balances' if r_['companies_to_queue']['balances'] else 'DOES NOT BALANCE'}**",
        f"- Queue to classification: {c_['prefiltered_research_queue']:,} = "
        f"{c_['fully_researched']:,} classified + {c_['remaining_unprocessed_old_queue']:,} pending "
        f"— **{'balances' if r_['queue_to_classification']['balances'] else 'DOES NOT BALANCE'}**",
        "",
        f"Run complete: **{'yes' if r_['queue_to_classification']['run_complete'] else 'NO — ' + format(c_.get('strict_queue_remaining') or 0, ',') + ' strict-queue companies remain unresearched (' + format(c_['remaining_unprocessed_old_queue'], ',') + ' across the full old queue)'}**",
        "",
        "Founder rows may exceed company rows because one qualified company can yield more "
        "than one credible buyer; each additional founder is an intentional separate contact row.",
        "", "## Validation", "",
        "| Check | Failures |", "|---|---:|",
    ]
    for k, val in v.items():
        if k == "all_checks_pass":
            continue
        md.append(f"| {k.replace('_', ' ')} | {val} |")
    md += ["", f"All checks pass: **{'yes' if v['all_checks_pass'] else 'no'}**", ""]
    (C.OUTPUTS / "08_run_summary.md").write_text("\n".join(md))

    print(f"03 qualified companies      : {n03:,}")
    print(f"04 qualified founder leads  : {n04:,}")
    print(f"05 needs verification       : {n05:,}")
    print(f"06 rejected after research  : {n06:,}")
    print(f"07 research sources         : {n07:,}")
    print(f"08 run summary              : written")
    print(f"   remaining unprocessed    : {pending:,}")
    print(f"   all validation checks pass: {v['all_checks_pass']}")
    conn.close()


if __name__ == "__main__":
    main()
