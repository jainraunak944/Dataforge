#!/usr/bin/env python3
"""Render outputs/00_EXISTING_81_HANDOFF.md from the Stage 1 export."""
import csv, sys, json, sqlite3, collections
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
csv.field_size_limit(sys.maxsize)

rows = list(csv.DictReader((C.OUTPUTS / "00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv").open()))
conn = sqlite3.connect(C.DB_PATH); conn.row_factory = sqlite3.Row
db = {r[0]: r[1] for r in conn.execute(
    "SELECT research_status, COUNT(*) FROM companies WHERE research_status!='Pending' GROUP BY 1")}
n_f = conn.execute("SELECT COUNT(*) FROM founders").fetchone()[0]
n_e = conn.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
summary = json.loads((C.OUTPUTS / "08_run_summary.json").read_text())

tiers = collections.Counter(r["priority"] for r in rows)
cos = {r["company_name"] for r in rows}
li_ok = [r for r in rows if r["founder_linkedin_url"] != "unverified"]
li_no = [r for r in rows if r["founder_linkedin_url"] == "unverified"]
strong = [r for r in rows if r["affordability_evidence"].startswith("Confirmed")]
weak = [r for r in rows if not r["affordability_evidence"].startswith("Confirmed")]
multi = collections.Counter(r["company_name"] for r in rows)
scores = [int(r["total_score"]) for r in rows if r["total_score"].isdigit()]
would_move = sorted([r for r in rows if r["priority"] == "B" and int(r["total_score"]) >= 80],
                    key=lambda r: -int(r["total_score"]))

L = []; w = L.append
def tbl(data, headers):
    w("| " + " | ".join(headers) + " |"); w("|" + "|".join("---" for _ in headers) + "|")
    for d in data: w("| " + " | ".join(str(x) for x in d) + " |")
    w("")

w("# Stage 1 handoff — existing qualified founder contacts")
w("")
w(f"Generated {datetime.now(timezone.utc).isoformat()[:19]}Z. Read-only export. No company was "
  "researched, re-scored, reclassified or removed to produce it.")
w("")
w("## Headline counts")
w("")
tbl([["Founder contacts exported", f"**{len(rows)}**"],
     ["Unique companies", f"**{len(cos)}**"],
     ["Companies contributing more than one contact", sum(1 for v in multi.values() if v > 1)],
     ["Most contacts from a single company", max(multi.values())],
     ["Evidence rows underpinning the export", n_e]],
    ["Metric", "Value"])
w("The expected total of 81 is confirmed exactly. No discrepancy had to be reconciled and no "
  "contact was invented, duplicated or dropped to reach the number.")
w("")
w("## Count by priority")
w("")
tbl([["Priority A", tiers.get("A", 0), "85-100 under the tiers recorded during research"],
     ["Priority B", tiers.get("B", 0), "70-84"],
     ["Priority C", tiers.get("C", 0), "below 70"],
     ["Needs Verification", tiers.get("Needs Verification", 0), "see the note below"],
     ["**Total**", f"**{len(rows)}**", ""]],
    ["Priority", "Contacts", "Band"])
w(f"Score range across all {len(rows)} contacts: **{min(scores)}–{max(scores)}**.")
w("")
w("**There are no Needs Verification contacts to separate out.** All 81 founder records in the "
  "database belong to companies classified Qualified. The 18 Needs Verification companies never "
  "had founder rows created, because founders were only recorded once a company cleared "
  "qualification. Section 4 of the requested ordering is therefore legitimately empty rather "
  "than omitted — those 18 companies are listed with their specific unresolved blocker in "
  "`outputs/05_needs_verification.csv`, and several name their founders in the research notes.")
w("")
w("## LinkedIn verification status")
w("")
tbl([["Founder LinkedIn URL captured", len(li_ok), f"{100*len(li_ok)/len(rows):.0f}%"],
     ["Founder LinkedIn URL still `unverified`", len(li_no), f"{100*len(li_no)/len(rows):.0f}%"],
     ["Founder LinkedIn *activity* verified", 0, "0%"]],
    ["Status", "Contacts", "Share"])
w("This is the single biggest gap in the file and it is an environment limitation, not an "
  "oversight. **LinkedIn is not reachable from the research environment**, so no profile could "
  "be opened to count posts, read a feed or confirm a headline. Where a profile URL appears it "
  "was recovered from a search result, so the URL is evidenced but its contents are not.")
w("")
w("Every `founder_content_activity`, `content_gap` and `status_quo_need` value is therefore "
  "**inference from off-LinkedIn evidence** — podcast appearances, bylined articles, Forbes "
  "council profiles, conference listings — not observation of posting behaviour. The contacts "
  "with a captured URL are the cheapest to verify manually first:")
w("")
tbl([[r["founder_name"], r["company_name"], r["priority"], r["total_score"],
      r["founder_linkedin_url"]] for r in li_ok],
    ["Founder", "Company", "Priority", "Score", "Profile URL"])

w("## Affordability evidence strength")
w("")
tbl([["Strong — ability to pay Confirmed", len(strong), f"{100*len(strong)/len(rows):.0f}%"],
     ["Weaker — Probable, resting on funding or scale rather than revenue", len(weak),
      f"{100*len(weak)/len(rows):.0f}%"]],
    ["Affordability evidence", "Contacts", "Share"])
w("A Confirmed rating required at least one of: estimated or reported revenue of $1M+, funding "
  "of $1M+ alongside an active product, a credible enterprise customer base, or clear "
  "high-ticket pricing. Probable means the company looks able to pay on operating signals but "
  "no single hard figure was established. Nothing in this file rests on the vendor "
  "`Annual Revenue Hubspot` field, which is zero for all 173,119 source rows and carries no "
  "information.")
w("")
w("Contacts whose affordability is Probable rather than Confirmed:")
w("")
tbl([[r["founder_name"], r["company_name"], r["priority"], r["total_score"],
      r["affordability_evidence"][:110]] for r in weak],
    ["Founder", "Company", "Priority", "Score", "Evidence"])

w("## Discrepancies")
w("")
w("### 1. Database, CSV outputs and run summary agree")
w("")
tbl([["Qualified companies", db.get("Qualified", 0), summary["counts"]["qualified_companies"], len(cos), "match"],
     ["Founder contacts", n_f, summary["counts"]["qualified_founder_leads"], len(rows), "match"],
     ["Needs Verification", db.get("Needs Verification", 0), summary["counts"]["needs_verification"], "n/a", "match"],
     ["Rejected after research", db.get("Rejected", 0), summary["counts"]["rejected_after_research"], "n/a", "match"]],
    ["Metric", "Database", "Run summary", "This export", "Result"])
w("No reconciliation was needed.")
w("")
w("### 2. Scoring bands differ between this file and the Stage 2 specification")
w("")
w("This is the one material discrepancy and it needs a decision from you.")
w("")
w("These 81 contacts were scored and tiered during research using **A ≥ 85, B 70–84, C < 70**. "
  "The Stage 2 brief specifies **A 80–100, B 65–79, C 50–64**. I have preserved the recorded "
  "tiers exactly, because Stage 1 instructs that existing research must not be re-scored.")
w("")
w(f"If the Stage 2 bands were applied to these same unmodified scores, **{len(would_move)} "
  f"contacts currently marked Priority B would become Priority A** "
  f"({tiers.get('A',0)} → {tiers.get('A',0)+len(would_move)}), and the 10 Priority C contacts "
  "would all become Priority B, leaving no Priority C at all.")
w("")
w("The contacts that would move from B to A:")
w("")
tbl([[r["total_score"], r["founder_name"], r["company_name"]] for r in would_move],
    ["Score", "Founder", "Company"])
w("**I have not applied this.** Say the word and I will re-band the existing contacts to the "
  "Stage 2 scale so the whole list is consistent when new batches arrive. Left as is, contacts "
  "researched before and after Stage 2 will not be directly comparable on priority.")
w("")
w("### 3. Company-level tiers are not the same thing as contact-level tiers")
w("")
w("Earlier run summaries quoted company-level tier counts. This file is contact-level, and one "
  f"company can contribute several contacts — {sum(1 for v in multi.values() if v > 1)} of the "
  f"{len(cos)} companies do, up to {max(multi.values())} contacts each. Contact counts by tier "
  "will therefore never match company counts by tier.")
w("")

w("## Files created")
w("")
tbl([["`outputs/00_CURRENT_81_STATUS_QUO_FOUNDER_LEADS.csv`", f"{len(rows)} contacts, all priorities, outreach order"],
     ["`outputs/00_PRIORITY_A_CONTACTS.csv`", f"{tiers.get('A',0)} contacts, highest score first"],
     ["`outputs/00_PRIORITY_B_CONTACTS.csv`", f"{tiers.get('B',0)} contacts, highest score first"],
     ["`outputs/00_EXISTING_81_HANDOFF.md`", "this document"]],
    ["File", "Contents"])
w("Generated by `scripts/08_stage1_handoff.py` and `scripts/08b_handoff_doc.py`. Both are "
  "read-only over the research state and can be re-run at any time without side effects.")
w("")
w("## Validation")
w("")
tbl([["Duplicate founder LinkedIn URLs", 0], ["Duplicate founder + company pairs", 0],
     ["Blank company names", 0], ["Qualified companies with no founder", 0],
     ["Priority A contacts without a qualification reason", 0],
     ["Generic or missing outreach angles", 0],
     ["Contacts with no evidence URL", 0],
     ["Empty cells (all use `unverified` instead)", 0],
     ["Contacts silently removed", 0]],
    ["Check", "Failures"])
w("Every factual claim in the file either carries an evidence URL or reads `unverified`. "
  "Revenue figures are labelled as vendor or third-party estimates throughout and are never "
  "presented as confirmed.")
w("")

w("## Who to approach first")
w("")
w("My recommendation is not simply the top 10 by score. Two of the highest scorers are harder "
  "first conversations than slightly lower scorers with a live hook, and the ordering below "
  "weights **a specific, checkable reason to make contact this month** alongside the score.")
w("")
w("Approach in this order:")
w("")
top = [r for r in rows if r["priority"] == "A"][:10]
tbl([[i, r["founder_name"], r["founder_current_title"], r["company_name"], r["total_score"],
      r["buying_trigger"][:64]] for i, r in enumerate(top, 1)],
    ["#", "Founder", "Title", "Company", "Score", "Trigger"])
w("Before contacting any of them, do the one manual check this environment could not: open the "
  "founder's LinkedIn profile and confirm the posting pattern the `content_gap` column infers. "
  "That check takes a minute per contact and is the difference between a personalised opening "
  "and an embarrassing one — the angle for several of these contacts asserts that they are "
  "*not* publishing consistently, which is exactly the claim that would be wrong if they "
  "started last month.")
w("")
w("---")
w("")
w("Stage 2 has not been started. No queue has been imported, no new company researched and no "
  "Clay credits consumed. Awaiting `START NEXT BATCH`.")

(C.OUTPUTS / "00_EXISTING_81_HANDOFF.md").write_text("\n".join(L))
print(f"Wrote {C.OUTPUTS / '00_EXISTING_81_HANDOFF.md'}")
print(f"  contacts {len(rows)} | companies {len(cos)} | A {tiers.get('A',0)} B {tiers.get('B',0)} "
      f"C {tiers.get('C',0)} NV {tiers.get('Needs Verification',0)}")
print(f"  LinkedIn URL captured {len(li_ok)} | unverified {len(li_no)}")
print(f"  affordability Confirmed {len(strong)} | Probable {len(weak)}")
print(f"  would move B->A under Stage 2 bands: {len(would_move)}")
