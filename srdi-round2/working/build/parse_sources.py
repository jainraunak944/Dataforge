"""Extract source-register rows from the four research reports into sources.json (prefixing IDs by workstream)."""
import re, json, os
SP="/tmp/claude-0/-home-user-Dataforge/8c3116aa-5914-54b9-9102-e947be44cbb4/scratchpad"
files={"W1":"ws1_engineering.md","W2":"ws2_safety_regulatory.md","W3":"ws3_market_infra_benchmarks.md","W4":"ws4_economics_emissions.md"}
out=[]
for tag,fn in files.items():
    path=f"{SP}/research/{fn}"
    if not os.path.exists(path): print("missing",fn); continue
    txt=open(path,encoding="utf-8").read()
    # find the source register section
    m=re.search(r"#+\s*\d*\.?\s*Source register.*?\n(.*?)(?=\n#+\s|\Z)", txt, re.S|re.I)
    if not m: print("no register in",fn); continue
    block=m.group(1)
    rows=[l for l in block.split("\n") if l.startswith("|")]
    header=[h.strip().lower() for h in rows[0].strip("|").split("|")] if rows else []
    for l in rows[2:]:
        cells=[c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells)<6: continue
        rec={"id":f"{tag}-{cells[0]}"}
        # map by header names
        for h,c in zip(header,cells):
            if h.startswith("id"): continue
            key={"claim supported":"claim","publisher":"publisher","title":"title","document title":"title","url":"url","pub date / data year":"date","pub date":"date","page/table/section":"section","section/clause/page":"section","geography":"geo","unit":"unit","status":"status","status (observed/modelled/target/announced)":"status","limitations":"limits"}.get(h,h)
            rec[key]=c
        out.append(rec)
    print(tag, len(rows)-2, "rows")
json.dump(out, open(f"{SP}/build/sources.json","w"), indent=1, ensure_ascii=False)
print("total sources", len(out))
