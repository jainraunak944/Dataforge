#!/usr/bin/env python3
"""Record researched companies, founders and evidence into research_state.sqlite.

Usage:  python3 scripts/05_record.py payload.json

Payload is a list of company objects. Each write is one transaction, so an
interrupted run leaves the database consistent and the company simply stays
Pending. Checkpoint CSV every 20 completions, DB backup every 100, progress line
every 50, full summary every 500 -- as the brief requires.
"""
from __future__ import annotations
import sys, json, sqlite3, shutil, csv
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

CKPT = C.ROOT / "checkpoints"
BACKUP = C.ROOT / "checkpoints" / "db_backups"
LOGS = C.ROOT / "logs"
for d in (CKPT, BACKUP, LOGS):
    d.mkdir(parents=True, exist_ok=True)

COMPANY_FIELDS = [
    "company_status", "research_status", "business_model", "b2b_saas_confidence",
    "hq_city", "hq_state", "hq_country", "hq_confidence", "employee_estimate",
    "employee_range_verified", "employee_confidence", "revenue_estimate",
    "revenue_confidence", "funding_total", "latest_round", "latest_round_date",
    "ability_to_pay", "ability_to_pay_reason", "tam_status", "saas_category",
    "target_customer", "sales_motion", "pricing_motion", "customer_examples",
    "product_summary", "internal_content_team", "recent_trigger", "trigger_date",
    "trigger_evidence_url", "company_fit_score", "ability_to_pay_score",
    "timing_score", "penalties", "hard_disqualifier", "final_classification",
    "final_score", "research_confidence", "research_notes", "error", "retry_status",
]
FOUNDER_FIELDS = [
    "full_name", "exact_title", "founder_status", "contact_rank", "linkedin_url",
    "location", "role_in_business", "still_operational", "follower_count",
    "most_recent_post_date", "posts_30d", "posts_90d", "posts_180d", "activity_class",
    "content_topics", "expertise", "founder_story", "content_style",
    "content_consistency", "positioning_quality", "content_gap", "content_opportunity",
    "raw_material", "ghostwriter_likelihood", "recent_founder_trigger", "outreach_angle",
    "public_email", "email_verification", "email_source_url", "alt_contact_route",
    "content_need_score", "founder_suitability_score", "final_score",
    "qualification_status", "research_notes",
]
EVIDENCE_FIELDS = [
    "founder_name", "source_url", "source_type", "page_title", "access_date",
    "evidence_category", "evidence_summary", "confidence", "fact_or_inference",
    "content_hash",
]
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW = datetime.now(timezone.utc).isoformat()


def completed_count(conn):
    return conn.execute(
        "SELECT COUNT(*) FROM companies WHERE research_status IN "
        "('Qualified','Needs Verification','Rejected','Blocked')").fetchone()[0]


def export_checkpoint(conn, n):
    path = CKPT / f"checkpoint_{n:06d}.csv"
    cur = conn.execute(
        "SELECT canonical_company_id, company_name, domain, research_status, "
        "final_classification, final_score, tam_status, ability_to_pay, hq_confidence, "
        "employee_confidence, research_confidence, last_completed_utc "
        "FROM companies WHERE research_status NOT IN ('Pending') ORDER BY queue_rank")
    rows = cur.fetchall()
    with path.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([d[0] for d in cur.description])
        wr.writerows(rows)
    latest = CKPT / "checkpoint_latest.csv"
    shutil.copyfile(path, latest)
    return path


def backup_db(conn, n):
    dest = BACKUP / f"research_state_{n:06d}.sqlite"
    bck = sqlite3.connect(dest)
    with bck:
        conn.backup(bck)
    bck.close()
    return dest


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: 05_record.py payload.json")
    payload = json.loads(Path(sys.argv[1]).read_text())
    if isinstance(payload, dict):
        payload = [payload]

    conn = sqlite3.connect(C.DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    before = completed_count(conn)
    written = ev_written = fo_written = 0

    for co in payload:
        cid = co["canonical_company_id"]
        cur = conn.cursor()
        try:
            cur.execute("BEGIN")
            sets, vals = [], []
            for f in COMPANY_FIELDS:
                if f in co:
                    sets.append(f"{f}=?"); vals.append(co[f])
            sets += ["last_attempted_utc=?", "last_completed_utc=?", "research_date=?",
                     "attempt_count=attempt_count+1"]
            vals += [NOW, NOW, TODAY]
            vals.append(cid)
            cur.execute(f"UPDATE companies SET {', '.join(sets)} WHERE canonical_company_id=?", vals)
            if cur.rowcount == 0:
                raise KeyError(f"unknown canonical_company_id {cid}")

            for fo in co.get("founders", []):
                cols = [f for f in FOUNDER_FIELDS if f in fo]
                cur.execute(
                    f"INSERT OR REPLACE INTO founders (canonical_company_id, {', '.join(cols)}) "
                    f"VALUES ({', '.join(['?'] * (len(cols) + 1))})",
                    [cid] + [fo[c] for c in cols])
                fo_written += 1

            for ev in co.get("evidence", []):
                ev.setdefault("access_date", TODAY)
                cols = [f for f in EVIDENCE_FIELDS if f in ev]
                cur.execute(
                    f"INSERT INTO evidence (canonical_company_id, {', '.join(cols)}) "
                    f"VALUES ({', '.join(['?'] * (len(cols) + 1))})",
                    [cid] + [ev[c] for c in cols])
                ev_written += 1

            cur.execute(
                "UPDATE companies SET evidence_count="
                "(SELECT COUNT(*) FROM evidence WHERE canonical_company_id=?), founder_count="
                "(SELECT COUNT(*) FROM founders WHERE canonical_company_id=?) "
                "WHERE canonical_company_id=?", (cid, cid, cid))
            conn.commit()
            written += 1
        except Exception as e:
            conn.rollback()
            print(f"  !! {cid}: {type(e).__name__}: {e}", file=sys.stderr)

    after = completed_count(conn)
    msgs = []
    if after // 20 > before // 20:
        msgs.append(f"checkpoint -> {export_checkpoint(conn, after).name}")
    if after // 100 > before // 100:
        msgs.append(f"db backup -> {backup_db(conn, after).name}")

    total = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    if after // 50 > before // 50:
        msgs.append(f"PROGRESS {after:,}/{total:,} ({100.0*after/total:.2f}%) - "
                    f"{total-after:,} remaining")
    if after // 500 > before // 500:
        dist = dict(conn.execute(
            "SELECT final_classification, COUNT(*) FROM companies "
            "WHERE final_classification IS NOT NULL GROUP BY 1").fetchall())
        msgs.append(f"SUMMARY at {after:,}: {dist}")

    print(f"recorded companies={written} founders={fo_written} evidence={ev_written} "
          f"| completed {after:,}/{total:,} | remaining {total-after:,}")
    for m in msgs:
        print(f"  {m}")
    with (LOGS / "research_progress.log").open("a") as f:
        f.write(f"{NOW}\tcompleted={after}\tremaining={total-after}\t"
                f"batch_written={written}\n")
    conn.close()


if __name__ == "__main__":
    main()
