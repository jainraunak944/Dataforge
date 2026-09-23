import json, os, sys
from common import *
from engine import *
import build_p1, build_p2, build_p3, build_p4, build_p5

OUT = sys.argv[1] if len(sys.argv) > 1 else "Paytm_Liminal_Deal_Model.xlsx"
DATA = "research_data.json"
data = json.load(open(DATA)) if os.path.exists(DATA) else {}

b = Book()
build_p1.build_readme(b)
build_p1.build_dashboard(b)
build_p1.build_inputs(b)
build_p2.build_liminal_ops(b)
build_p2.build_dcf(b)
build_p2.build_deal_cf(b)
build_p2.build_financing(b)
build_p3.build_earnout(b)          # defines eo_max before Sources_Uses uses it
build_p2.build_sources_uses(b)
build_p2.build_accretion(b)
build_p3.build_capital_drag(b)
build_p3.build_churn(b)
build_p4.build_structures(b)
build_p4.build_scenarios(b)
build_p4.build_thresholds(b)
build_p4.build_synergies(b)
build_p5.build_external(b, data)
build_p5.build_audit(b)
build_p5.build_dashboard_outputs(b)

order = ["README", "Dashboard", "Inputs", "Liminal_Ops", "DCF", "Financing", "Sources_Uses", "Accretion", "Deal_CF", "Capital_Drag", "Churn", "Structures", "Earnout", "Scenarios", "Thresholds", "Synergies", "Comps", "Precedents", "Regulatory", "Sources", "Audit_Trail"]
b.wb._sheets = [b.wb[n] for n in order]
b.wb.active = 1
# freeze panes on year sheets
for n in ["Liminal_Ops", "DCF", "Deal_CF", "Capital_Drag", "Churn", "Structures", "Scenarios", "Accretion"]:
    b.wb[n].freeze_panes = "C4"
b.wb.save(OUT)
print("saved", OUT, "sheets:", len(order), "names:", len(b.names))
