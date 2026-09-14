#!/usr/bin/env python3
"""Build research_state.sqlite and load the prefiltered queue into it.

All research state lives here so the workflow survives interruption: every
company carries its own status, attempt count and timestamps, and re-running
this script is idempotent (existing rows keep their research state).
"""
from __future__ import annotations
import sys, sqlite3, csv, json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

QUEUE = C.OUTPUTS / "02_prefiltered_research_queue.csv"
BATCH_SIZE = 40

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS companies (
  canonical_company_id   TEXT PRIMARY KEY,
  source_row_ids         TEXT,
  domain                 TEXT,
  company_name           TEXT,
  website_url            TEXT,
  linkedin_company_url   TEXT,
  queue_rank             INTEGER,
  research_priority      TEXT,
  preliminary_score      INTEGER,
  assigned_batch         INTEGER,

  company_status         TEXT DEFAULT 'unknown',
  research_status        TEXT DEFAULT 'Pending',
  attempt_count          INTEGER DEFAULT 0,
  last_attempted_utc     TEXT,
  last_completed_utc     TEXT,
  error                  TEXT,
  retry_status           TEXT,
  evidence_count         INTEGER DEFAULT 0,
  founder_count          INTEGER DEFAULT 0,

  business_model         TEXT,
  b2b_saas_confidence    TEXT,
  hq_city                TEXT,
  hq_state               TEXT,
  hq_country             TEXT,
  hq_confidence          TEXT,
  employee_estimate      TEXT,
  employee_range_verified TEXT,
  employee_confidence    TEXT,
  revenue_estimate       TEXT,
  revenue_confidence     TEXT,
  funding_total          TEXT,
  latest_round           TEXT,
  latest_round_date      TEXT,
  ability_to_pay         TEXT,
  ability_to_pay_reason  TEXT,
  tam_status             TEXT,
  saas_category          TEXT,
  target_customer        TEXT,
  sales_motion           TEXT,
  pricing_motion         TEXT,
  customer_examples      TEXT,
  product_summary        TEXT,
  internal_content_team  TEXT,
  recent_trigger         TEXT,
  trigger_date           TEXT,
  trigger_evidence_url   TEXT,

  company_fit_score      INTEGER,
  ability_to_pay_score   INTEGER,
  timing_score           INTEGER,
  penalties              TEXT,
  hard_disqualifier      TEXT,
  final_classification   TEXT,
  final_score            INTEGER,
  research_confidence    TEXT,
  research_notes         TEXT,
  research_date          TEXT
);

CREATE TABLE IF NOT EXISTS founders (
  founder_id             INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_company_id   TEXT NOT NULL,
  full_name              TEXT,
  exact_title            TEXT,
  founder_status         TEXT,
  contact_rank           INTEGER,
  linkedin_url           TEXT,
  location               TEXT,
  role_in_business       TEXT,
  still_operational      TEXT,
  follower_count         TEXT,
  most_recent_post_date  TEXT,
  posts_30d              TEXT,
  posts_90d              TEXT,
  posts_180d             TEXT,
  activity_class         TEXT,
  content_topics         TEXT,
  expertise              TEXT,
  founder_story          TEXT,
  content_style          TEXT,
  content_consistency    TEXT,
  positioning_quality    TEXT,
  content_gap            TEXT,
  content_opportunity    TEXT,
  raw_material           TEXT,
  ghostwriter_likelihood TEXT,
  recent_founder_trigger TEXT,
  outreach_angle         TEXT,
  public_email           TEXT,
  email_verification     TEXT,
  email_source_url       TEXT,
  alt_contact_route      TEXT,
  content_need_score     INTEGER,
  founder_suitability_score INTEGER,
  final_score            INTEGER,
  qualification_status   TEXT,
  research_notes         TEXT,
  UNIQUE(canonical_company_id, full_name)
);

CREATE TABLE IF NOT EXISTS evidence (
  evidence_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_company_id   TEXT NOT NULL,
  founder_name           TEXT,
  source_url             TEXT,
  source_type            TEXT,
  page_title             TEXT,
  access_date            TEXT,
  evidence_category      TEXT,
  evidence_summary       TEXT,
  confidence             TEXT,
  fact_or_inference      TEXT,
  content_hash           TEXT
);

CREATE TABLE IF NOT EXISTS fetch_cache (
  url                    TEXT PRIMARY KEY,
  access_date            TEXT,
  http_status            TEXT,
  content_hash           TEXT,
  blocked_reason         TEXT,
  payload_path           TEXT
);

CREATE TABLE IF NOT EXISTS runs (
  run_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  started_utc            TEXT,
  finished_utc           TEXT,
  companies_attempted    INTEGER,
  companies_completed    INTEGER,
  notes                  TEXT
);

CREATE INDEX IF NOT EXISTS idx_status   ON companies(research_status);
CREATE INDEX IF NOT EXISTS idx_batch    ON companies(assigned_batch);
CREATE INDEX IF NOT EXISTS idx_priority ON companies(research_priority, queue_rank);
CREATE INDEX IF NOT EXISTS idx_ev_co    ON evidence(canonical_company_id);
CREATE INDEX IF NOT EXISTS idx_fo_co    ON founders(canonical_company_id);
"""


def main():
    csv.field_size_limit(sys.maxsize)
    conn = sqlite3.connect(C.DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()

    if not QUEUE.exists():
        sys.exit(f"Queue not found: {QUEUE}")

    inserted = existing = 0
    with QUEUE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    cur = conn.cursor()
    cur.execute("BEGIN")
    for i, r in enumerate(rows):
        batch = i // BATCH_SIZE + 1
        cur.execute("SELECT 1 FROM companies WHERE canonical_company_id=?",
                    (r["canonical_company_id"],))
        if cur.fetchone():
            existing += 1
            continue
        cur.execute("""INSERT INTO companies
            (canonical_company_id, source_row_ids, domain, company_name, website_url,
             linkedin_company_url, queue_rank, research_priority, preliminary_score,
             assigned_batch, research_status)
            VALUES (?,?,?,?,?,?,?,?,?,?,'Pending')""",
            (r["canonical_company_id"], r["source_row_ids"], r["domain"], r["company_name"],
             r["website_url"], r["linkedin_company_url"], int(r["queue_rank"]),
             r["research_priority"], int(float(r["preliminary_score"] or 0)), batch))
        inserted += 1
    conn.commit()

    tot = cur.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    pend = cur.execute("SELECT COUNT(*) FROM companies WHERE research_status='Pending'").fetchone()[0]
    nb = cur.execute("SELECT MAX(assigned_batch) FROM companies").fetchone()[0]
    print(f"queue rows read : {len(rows):,}")
    print(f"inserted        : {inserted:,}")
    print(f"already present : {existing:,}")
    print(f"total in db     : {tot:,}")
    print(f"pending         : {pend:,}")
    print(f"batches         : {nb:,} of {BATCH_SIZE}")
    conn.close()


if __name__ == "__main__":
    main()
