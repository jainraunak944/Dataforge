# Status Quo lead-research dataset — receipt log

Source dataset for the "Status Quo Complete US SaaS Lead Research System" task
(US software / SaaS company database, delivered as a 10-part CSV upload).

**Status: parts 01–05 received and verified. Parts 06–10 pending upload. No
processing has started yet — per instruction, processing begins only after all
10 parts arrive.**

## Files received 2026-09-14

| File | MD5 | CSV records |
|---|---|---|
| us-software-saas-companies-part-01.csv | 588863052e5cc0b5f955667c4517fa2a | 16,365 |
| us-software-saas-companies-part-02.csv | 77a349627636c455c02c646aa229397b | 17,990 |
| us-software-saas-companies-part-03.csv | 0be53fc0c85f8bbf46b6ea5a3fa14866 | 18,169 |
| us-software-saas-companies-part-04.csv | bce9de278525312000a13af757324093 | 18,690 |
| us-software-saas-companies-part-05.csv | 06d73ab286db13c545ff12e98016cdda | 26,452 |

Total records so far: 97,666 (expected ~173,119 across all 10 parts).

## Verification performed at receipt (not processing)

- MD5 checksums of workspace copies match the uploaded originals bit-for-bit.
- All five parts share an identical 27-column header:
  `Domain, Company Name, LinkedIn Company URL, Industry, JSON Industry,
  Country, JSON Country, Employee Headcount, JSON Employee Headcount,
  Employee Size Range, JSON Employee Size Range, Description, Company Type,
  Business Type, Pattern Tags, Founded, Locality, Specialties,
  Annual Revenue Clay, Annual Revenue Hubspot, Total Funding Range,
  Scale Scope, SubIndustry, Derived Description, Derived Industry,
  Follower Count, Slug`
- Every record parses to exactly 27 fields (0 malformed rows).
- Note: quoted Description fields contain embedded newlines, so physical line
  counts (`wc -l`) overstate record counts; always use a real CSV parser.
- Filenames here are the original part names; the upload system's random hash
  prefixes (e.g. `43a1f1e6-`) were stripped when copying into the workspace.

## Next steps (blocked until parts 06–10 arrive)

1. Receive and verify parts 06–10 the same way.
2. Concatenate all 10 parts (header once) into
   `us-software-saas-companies-cleaned.csv` — the input file named by the task.
3. Begin the research pipeline (audit → normalize → dedupe → prefilter →
   web research → outputs) in `status_quo_lead_research/`, per the task spec.

The part files in this directory are source data: never modify, overwrite,
rename, or delete them.
