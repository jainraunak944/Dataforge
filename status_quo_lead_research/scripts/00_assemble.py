#!/usr/bin/env python3
"""Stage 0b: assemble the ten uploaded parts into the canonical source CSV.

The brief names a single input file, `us-software-saas-companies-cleaned.csv`.
It was delivered as ten byte-chunked parts, each repeating the 27-column header.
This reassembles them, in part order, into one canonical file and records a
per-part record count so the audit can reconcile against the source.

Reads and writes with a real CSV parser throughout: the free-text columns embed
newlines inside quoted fields, so line-based concatenation would corrupt records.

Output: data/us-software-saas-companies-cleaned.csv
        data/interim/assembly_report.json
"""
import csv, json, hashlib, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw_parts"
OUT = ROOT / "data" / "us-software-saas-companies-cleaned.csv"
REPORT = ROOT / "data" / "interim" / "assembly_report.json"

csv.field_size_limit(sys.maxsize)

parts = sorted(RAW.glob("us-software-saas-companies-part-*.csv"))
if len(parts) != 10:
    sys.exit(f"Expected 10 parts, found {len(parts)}")

header = None
per_part = []
total = 0

REPORT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as fout:
    writer = None
    for p in parts:
        with p.open("r", newline="", encoding="utf-8") as fin:
            reader = csv.reader(fin)
            try:
                h = next(reader)
            except StopIteration:
                sys.exit(f"{p.name} is empty")
            if header is None:
                header = h
                writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header + ["source_part", "source_row_id"])
            elif h != header:
                sys.exit(f"{p.name} header differs from part 01")

            n = 0
            badwidth = 0
            for row in reader:
                if len(row) != len(header):
                    badwidth += 1
                    # pad / truncate defensively so the canonical file stays rectangular;
                    # the audit counts these as malformed records.
                    row = (row + [""] * len(header))[: len(header)]
                total += 1
                n += 1
                writer.writerow(row + [p.name.split("part-")[1].split(".")[0], total])
            per_part.append({"part": p.name, "records": n, "malformed_width": badwidth})
            print(f"  {p.name}: {n:,} records" + (f"  ({badwidth} malformed width)" if badwidth else ""))

sha = hashlib.sha256()
with OUT.open("rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        sha.update(chunk)

report = {
    "assembled_utc": datetime.now(timezone.utc).isoformat(),
    "canonical_file": str(OUT),
    "canonical_bytes": OUT.stat().st_size,
    "canonical_sha256": sha.hexdigest(),
    "source_columns": header,
    "added_columns": ["source_part", "source_row_id"],
    "total_records": total,
    "per_part": per_part,
}
REPORT.write_text(json.dumps(report, indent=2))
print(f"\nTotal records: {total:,}")
print(f"Canonical file: {OUT}  ({OUT.stat().st_size:,} bytes)")
print(f"Report: {REPORT}")
