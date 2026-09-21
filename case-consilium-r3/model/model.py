"""v2 cohort, pricing and channel model for the BGCC Round 3 FanCode deck (redesign audit corrections).
Run: python3 model.py -> outputs/*.csv and outputs/model_outputs.json. Every number on the slides comes from here."""
import json, csv, math, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)); A = json.load(open(os.path.join(HERE, "assumptions.json")))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
t = A["tax"]["gst_rate"]; VC = A["variable_costs"]; SK = A["skus"]; H = ("d90","m12","m24")
def contrib(price, hours, cm=1.0):
    return price/(1+t) - cm*(VC["payment_gateway_share_of_gross"]+VC["support_refund_share_of_gross"])*price - cm*VC["cdn_cost_per_hour_inr"]*hours
def c(sku, cm=1.0): return contrib(SK[sku]["price"], SK[sku]["hours"], cm)
def pathways(sc):
    cm = sc["cost_mult"]; C = A["cohorts"]
    c_s = c("session_model", cm); c_t89 = c("tournament_masters", cm); c_t79 = c("tournament_250_500", cm); c_tmix = (c_t89+c_t79)/2
    c_fts = c("finish_season", cm)
    c_step_t_fts = contrib(SK["finish_season"]["price"]-SK["tournament_masters"]["price"], SK["finish_season"]["hours"]-SK["tournament_masters"]["hours"], cm)
    c_step_s_t = contrib(SK["tournament_masters"]["price"]-SK["session_model"]["price"], SK["tournament_masters"]["hours"]-SK["session_model"]["hours"], cm)
    c_399 = c("season_2027", cm); c_349 = c("season_2027_loyalty", cm); c_mon = c("monthly_pass", cm); c_f1 = c("f1_weekend", cm)
    xsport = C["cross_sport_monthly_take_rate"]*(c_mon - C["cross_sport_would_have_bought_f1_share"]*c_f1)
    rep = {h: C["repeat_passes_beyond_entry"][h]*sc["repeat_mult"] for h in H}; reps = {h: C["repeat_sessions_beyond_entry"][h]*sc["repeat_mult"] for h in H}
    r_u, r_f, r2 = sc["renewal_upg"], sc["renewal_fts"], C["renewal_2028_of_2027_renewers"]; np27, np28 = C["non_renewer_passes_2027"], C["non_renewer_passes_2028_partial"]
    P = {}
    P["entry_only"] = {h: c_t89 for h in H}
    P["repeat_no_upgrade"] = {h: c_t89 + rep[h]*c_tmix for h in H}
    up90 = c_t89 + c_step_t_fts + xsport
    P["upgrade_via_credit"] = {"d90": up90, "m12": up90 + r_u*c_349 + (1-r_u)*np27*c_tmix,
        "m24": up90 + r_u*c_349 + (1-r_u)*np27*c_tmix + r_u*r2*c_399 + r_u*(1-r2)*np27*c_tmix + (1-r_u)*np28*c_tmix}
    fd90 = c_fts + xsport
    P["fts_direct"] = {"d90": fd90, "m12": fd90 + r_f*c_349 + (1-r_f)*np27*c_tmix,
        "m24": fd90 + r_f*c_349 + (1-r_f)*np27*c_tmix + r_f*r2*c_399 + r_f*(1-r2)*np27*c_tmix + (1-r_f)*np28*c_tmix}
    te = sc["tournament_entrant"]
    E_t = {h: te["p_entry_only"]*P["entry_only"][h] + te["p_repeat"]*P["repeat_no_upgrade"][h] + te["p_upgrade"]*P["upgrade_via_credit"][h] for h in H}
    se = C["session_entrant"]
    E_s = {h: se["p_never"]*c_s + se["p_repeat_sessions"]*(c_s + reps[h]*c_s) + se["p_upgrade_to_tournament"]*(c_s + c_step_s_t + (E_t[h]-c_t89)) for h in H}
    E_x = {"session": E_s, "tournament": E_t, "fts": {h: P["fts_direct"][h]-xsport for h in H}}   # existing payers: no cross-sport bridge value
    U = dict(c_session=c_s, c_t79=c_t79, c_t89=c_t89, c_t99=c("tournament_finals",cm), c_tmix=c_tmix, c_fts=c_fts, c_step_t_fts=c_step_t_fts, c_step_s_t=c_step_s_t,
             c_season399=c_399, c_season349=c_349, c_monthly=c_mon, c_f1_weekend=c_f1, xsport_value=xsport)
    return P, E_t, E_s, E_x, U
def mixval(mix, E_s, E_t, P, h, shift=0.0):
    m = dict(mix); m["session"] = m.get("session",0)+shift; m["tournament"] = m.get("tournament",0)-shift
    return m["session"]*E_s[h] + m["tournament"]*E_t[h] + m.get("fts",0)*P["fts_direct"][h]
def breakeven(P, te, cac, h):
    w_e, w_r = te["p_entry_only"], te["p_repeat"]; c_non = (w_e*P["entry_only"][h] + w_r*P["repeat_no_upgrade"][h])/(w_e+w_r); c_up = P["upgrade_via_credit"][h]
    return None if c_up-c_non <= 0 else (cac-c_non)/(c_up-c_non)
def run(scname, stage):
    """stage: 'stage1' (released now), 'full' (Stage 1 + Stage 2 = ₹10 lakh)."""
    sc = A["scenarios"][scname]; P, E_t, E_s, E_x, U = pathways(sc); C = A["cohorts"]; cann = C["cannibalisation"]; shift = sc["session_shift"]
    rows = []
    for ch in A["channels"]:
        spend = ch["stage1"] if stage=="stage1" else ch["spend"]
        r = dict(id=ch["id"], name=ch["name"], group=ch["group"], spend=spend, spend_full=ch["spend"], stage1=ch["stage1"], stage2=ch["stage2"], method=ch["method"], persona=ch["persona"], execution=ch["execution"], evidence=ch["evidence"], rule=ch["rule"])
        f = min(1.0, ch.get("incremental_share",0)*sc["f_mult"]); r["incremental_share"]=f
        if spend == 0 and ch["method"] in ("cpm","cpc"):
            r.update(purchases=0, new=0, react=0, exist=0, incr_new=0, incr_react=0, incr_exist=0, cac_new_attr=None, cac_new_incr=None,
                     value_new={h:0 for h in H}, value_react={h:0 for h in H}, value_exist={h:0 for h in H}, mix=ch["mix"]); rows.append(r); continue
        if ch["method"] == "cpm":
            imp = spend/ch["cpm"]*1000; clicks = imp*ch["ctr"]; purch = clicks*ch["cvr"]*sc["cvr_mult"]; r.update(impressions=imp, clicks=clicks, cpc=spend/clicks)
        elif ch["method"] == "cpc":
            clicks = spend/ch["cpc"]; purch = clicks*ch["cvr"]*sc["cvr_mult"]; r.update(clicks=clicks, cpc=ch["cpc"])
        if ch["method"] in ("cpm","cpc"):
            m = ch["customer_mix"]; new, react, exist = purch*m["new"], purch*m["react"], purch*m["exist"]
            r.update(purchases=purch, new=new, react=react, exist=exist, incr_new=new*f, incr_react=react*f, incr_exist=exist*f,
                     cac_new_attr=(spend/new if new else None), cac_new_incr=(spend/(new*f) if new else None), cost_per_react=(spend/react if react and m["react"]>=0.5 else None),
                     value_new={h: mixval(ch["mix"], E_s, E_t, P, h, shift) for h in H}, value_react={h: mixval(C["reactivated_mix"], E_s, E_t, P, h, shift) for h in H},
                     value_exist={h: sum(ch["mix"][k]*E_x[k][h] for k in ch["mix"]) for h in H}, mix=ch["mix"])
        elif ch["method"] == "owned":
            scale = spend/ch["spend"]   # stage 1 runs the same pools with fewer sends: outcomes scale with the funded share of contacts
            treated = {k: v*(1-ch["holdout"]) for k, v in ch["pools"].items()}
            conv = {k: treated[k]*ch["delivery"]*ch["click"][k]*ch["purchase"][k]*sc["cvr_mult"]*scale for k in treated}
            new = sum(v for k, v in conv.items() if ch["pool_class"][k]=="new"); exist = sum(v for k, v in conv.items() if ch["pool_class"][k]=="exist")
            share_new = sum(treated[k] for k in treated if ch["pool_class"][k]=="new")/sum(treated.values()); cost_new = spend*share_new
            r.update(purchases=new+exist, new=new, react=0, exist=exist, incr_new=new*f, incr_react=0, incr_exist=exist*f, conversions_by_pool=conv,
                     cost_allocated_new=cost_new, cost_allocated_exist=spend-cost_new, cac_new_attr=cost_new/new, cac_new_incr=cost_new/(new*f), cost_per_exist=(spend-cost_new)/exist,
                     value_new={h: mixval(ch["mix_new"], E_s, E_t, P, h, shift) for h in H}, value_react={h: 0 for h in H},
                     value_exist={h: sum(ch["mix_existing"][k]*E_x[k][h] for k in ch["mix_existing"]) for h in H}, mix=ch["mix_new"], treated_total=sum(treated.values()))
        else:
            r.update(purchases=None, new=None, react=None, exist=None, incr_new=None, cac_new_attr=None, cac_new_incr=None)
        rows.append(r)
    byid = {r["id"]: r for r in rows}; d = A["dedup"]["overlap_share_removed"]
    conv_rows = [r for r in rows if r.get("new") is not None]
    dedup_new = d*(byid["C3"]["new"] + byid["C4"]["new"]); dedup_incr = d*(byid["C3"]["incr_new"] + byid["C4"]["incr_new"])
    spend = sum(r["spend"] for r in rows); impl = A["meta"]["implementation_budget_inr"] if stage=="full" else 0
    new = sum(r["new"] for r in conv_rows) - dedup_new; incr_new = sum(r["incr_new"] for r in conv_rows) - dedup_incr
    react = sum(r["react"] for r in conv_rows); incr_react = sum(r["incr_react"] for r in conv_rows)
    exist = sum(r["exist"] for r in conv_rows); incr_exist = sum(r["incr_exist"] for r in conv_rows)
    def val(kind, h):
        v = sum(r[kind][h]*r[{"value_new":"new","value_react":"react","value_exist":"exist"}[kind]] for r in conv_rows if r.get(kind))
        return v
    attr = {h: val("value_new",h) - dedup_new*byid["C2"]["value_new"][h] + val("value_react",h) + val("value_exist",h) for h in H}
    incr = {h: sum(r["value_new"][h]*r["incr_new"] + r["value_react"][h]*r["incr_react"] + r["value_exist"][h]*r["incr_exist"] for r in conv_rows) - dedup_incr*byid["C2"]["value_new"][h] for h in H}
    # cannibalisation (scenario-scaled), applied to attributed and incremental alike (conservative)
    n_fts = sum(r["new"]*r["mix"].get("fts",0) + r["react"]*C["reactivated_mix"]["fts"] for r in conv_rows)
    n_t = sum(r["new"]*r["mix"].get("tournament",0) + r["react"]*C["reactivated_mix"]["tournament"] for r in conv_rows) + byid["C3"]["exist"]*A["channels"][2]["mix_existing"]["tournament"]
    n_up = n_t*sc["tournament_entrant"]["p_upgrade"]; n_ren = n_up*sc["renewal_upg"] + n_fts*sc["renewal_fts"]
    la = cann["fts_intender_leakage_share"]*n_fts*(U["c_fts"]-U["c_t89"]); lb = cann["multi_event_buyer_share_of_upgraders"]*n_up*max(0, 3*U["c_tmix"]-(U["c_t89"]+U["c_step_t_fts"])); lc = cann["loyalty_discount_would_renew_anyway_share"]*n_ren*(U["c_season399"]-U["c_season349"])
    cannib = {"d90": sc["cannib_mult"]*(la+lb), "m12": sc["cannib_mult"]*(la+lb+lc), "m24": sc["cannib_mult"]*(la+lb+lc)}
    net_attr = {h: attr[h]-cannib[h]-spend for h in H}; net_incr = {h: incr[h]-cannib[h]-spend for h in H}; net_incr_impl = {h: incr[h]-cannib[h]-spend-impl for h in H}
    paid_ids = [i for i in ("C1","C2","C4") if byid[i]["spend"]>0]; paid_spend = sum(byid[i]["spend"] for i in paid_ids)
    paid_new = sum(byid[i]["new"] for i in paid_ids) - d*byid["C4"]["new"]; paid_incr = sum(byid[i]["incr_new"] for i in paid_ids) - d*byid["C4"]["incr_new"]
    c2 = byid["C2"]; te = sc["tournament_entrant"]
    be = {}
    for label, cac in (("attr", c2["cac_new_attr"]), ("incr", c2["cac_new_incr"]), ("150",150), ("200",200)):
        for h in ("m12","m24"): be[f"{label}_{h}"] = breakeven(P, te, cac, h)
    return dict(scenario=scname, stage=stage, rows=rows, units=U, pathways=P, E_t=E_t, E_s=E_s, totals=dict(
        spend=spend, implementation=impl, new_attr=new, new_incr=incr_new, react_attr=react, react_incr=incr_react, exist_attr=exist, exist_incr=incr_exist,
        cost_per_new_attr=spend/new, cost_per_new_incr=spend/incr_new, cost_per_new_incr_incl_impl=(spend+impl)/incr_new, cost_per_new_or_react_attr=spend/(new+react),
        paid_spend=paid_spend, paid_cac_attr=(paid_spend/paid_new if paid_new else None), paid_cac_incr=(paid_spend/paid_incr if paid_incr else None),
        c2_cac_attr=c2["cac_new_attr"], c2_cac_incr=c2["cac_new_incr"], c2_value=c2["value_new"], value_attr=attr, value_incr=incr, cannibalisation=cannib,
        net_attr=net_attr, net_incr=net_incr, net_incr_incl_impl=net_incr_impl, breakeven=be, dedup_new=dedup_new,
        performance_share=sum(byid[i]["spend"] for i in ("C1","C2","C4"))/spend))
def sample_sizes():
    za, zb = 1.959964, 0.841621; k = A["sample_size"]["allocation_treatment_share"]/(1-A["sample_size"]["allocation_treatment_share"]); out=[]
    for p0 in A["sample_size"]["baselines"]:
        for lift in A["sample_size"]["relative_lifts"]:
            p1 = p0*(1+lift); pbar = (k*p1+p0)/(k+1)
            n_c = (za*math.sqrt((1+1/k)*pbar*(1-pbar)) + zb*math.sqrt(p1*(1-p1)/k + p0*(1-p0)))**2/(p1-p0)**2
            out.append(dict(baseline=p0, relative_lift=lift, treated_conv=p1, n_control=math.ceil(n_c), n_treatment=math.ceil(n_c*k), n_total=math.ceil(n_c*(k+1))))
    return out
if __name__ == "__main__":
    res = {(s,st): run(s,st) for s in ("downside","base","upside") for st in ("stage1","full")}
    B = res[("base","full")]; B1 = res[("base","stage1")]
    def T(s,st,k): return res[(s,st)]["totals"][k]
    with open(os.path.join(OUT,"channel_plan_base.csv"),"w",newline="") as f:
        cols=["id","name","group","spend_full","stage1","stage2","method","clicks","cpc","purchases","new","react","exist","incremental_share","incr_new","cac_new_attr","cac_new_incr","cost_per_react","cost_per_exist","evidence","rule"]
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader()
        for r in B["rows"]: w.writerow({k:(round(v,2) if isinstance(v,float) else v) for k,v in r.items() if k in cols})
    with open(os.path.join(OUT,"cohort_pathways_base.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["pathway","d90","m12","m24"])
        for k,v in B["pathways"].items(): w.writerow([k]+[round(v[h],1) for h in H])
        w.writerow(["EXPECTED tournament entrant"]+[round(B["E_t"][h],1) for h in H]); w.writerow(["EXPECTED session entrant"]+[round(B["E_s"][h],1) for h in H])
    with open(os.path.join(OUT,"scenarios.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["metric","stage","downside","base","upside"])
        for st in ("stage1","full"):
            for k,lab in (("new_attr","attributed new payers (dedup)"),("new_incr","incremental new payers"),("react_attr","reactivated payers"),("exist_attr","existing-payer ATP purchases"),("c2_cac_attr","C2 attributed CAC (new payers)"),("c2_cac_incr","C2 incremental CAC"),("cost_per_new_attr","programme cost per attributed new payer"),("cost_per_new_incr","programme cost per incremental new payer"),("cost_per_new_incr_incl_impl","incl. implementation, per incremental new payer")):
                w.writerow([lab, st]+[round(T(s,st,k)) if T(s,st,k) is not None else "" for s in ("downside","base","upside")])
            for h in ("m12","m24"):
                w.writerow([f"{h} net, attributed contribution minus spend (₹)", st]+[round(res[(s,st)]["totals"]["net_attr"][h]) for s in ("downside","base","upside")])
                w.writerow([f"{h} net, incremental contribution minus spend (₹)", st]+[round(res[(s,st)]["totals"]["net_incr"][h]) for s in ("downside","base","upside")])
                w.writerow([f"{h} net, incremental minus spend and implementation (₹)", st]+[round(res[(s,st)]["totals"]["net_incr_incl_impl"][h]) for s in ("downside","base","upside")])
    with open(os.path.join(OUT,"sample_sizes_90_10.csv"),"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["baseline","relative_lift","treated_conv","n_control","n_treatment","n_total"]); w.writeheader(); w.writerows(sample_sizes())
    sens=[]
    for u in (0.10,0.20,0.30,0.40):
        for rm in (0.6,1.0,1.4):
            sc=copy.deepcopy(A["scenarios"]["base"]); sc["tournament_entrant"]={"p_entry_only":round(0.4-(u-0.2),2),"p_repeat":0.40,"p_upgrade":u}; sc["repeat_mult"]=rm
            P,E_t,E_s,E_x,U=pathways(sc); sens.append(dict(upgrade_share=u,repeat_passes_24m=round(A["cohorts"]["repeat_passes_beyond_entry"]["m24"]*rm,2),value_m12=round(E_t["m12"],1),value_m24=round(E_t["m24"],1)))
    with open(os.path.join(OUT,"sensitivity_tournament_entrant.csv"),"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(sens[0].keys())); w.writeheader(); w.writerows(sens)
    with open(os.path.join(OUT,"rate_card.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["sku","price_inr","status","label","contribution_before_marketing_inr"])
        for k,v in SK.items(): w.writerow([k,v["price"],v["status"],v["label"],round(contrib(v["price"],v["hours"]),1)])
    ceilings = {"all_new_payers": {"150": 150*0.078, "200": 200*0.078}, "n045": {"150": 150*0.078*0.45, "200": 200*0.078*0.45}, "n045_f05": {"150": 150*0.078*0.45*0.5, "200": 200*0.078*0.45*0.5}}
    summary = dict(meta=A["meta"], units=B["units"], pathways=B["pathways"], E_t=B["E_t"], E_s=B["E_s"], base_full=B["totals"], base_stage1=B1["totals"], rows_base_full=B["rows"], rows_base_stage1=B1["rows"],
                   scenarios={f"{s}_{st}": res[(s,st)]["totals"] for (s,st) in res}, sensitivity=sens, sample_sizes_90_10=sample_sizes(), contest_cpc_ceilings=ceilings,
                   competitors=A["competitors"], skus=SK, credit_ladder=A["credit_ladder"], cohorts=A["cohorts"], channels=A["channels"], dedup=A["dedup"], current_allocation=A["current_allocation"], tax=A["tax"], variable_costs=VC)
    json.dump(summary, open(os.path.join(OUT,"model_outputs.json"),"w"), indent=1, default=lambda o: None, ensure_ascii=False)
    # digest
    print("UNITS", {k: round(v,1) for k,v in B["units"].items()})
    for k,v in B["pathways"].items(): print(f"  {k:20s}", [round(v[h]) for h in H])
    print("  E_t", [round(B["E_t"][h]) for h in H], " E_s", [round(B["E_s"][h]) for h in H])
    for st in ("stage1","full"):
        print(f"--- {st} ---")
        for r in res[("base",st)]["rows"]:
            if r.get("new") is not None: print(f"{r['id']:3s} spend {r['spend']:>7} purch {r['purchases']:7.0f} new {r['new']:6.0f} react {r['react']:5.0f} exist {r['exist']:5.0f} CACnew {r['cac_new_attr'] or 0:6.0f}/{r['cac_new_incr'] or 0:6.0f} v12new {r['value_new']['m12'] if r.get('value_new') else 0:5.0f} v24new {r['value_new']['m24'] if r.get('value_new') else 0:5.0f}")
        for s in ("downside","base","upside"):
            Tt=res[(s,st)]["totals"]; print(f"{s:9s} new {Tt['new_attr']:6.0f}/{Tt['new_incr']:6.0f} react {Tt['react_attr']:5.0f} exist {Tt['exist_attr']:5.0f} | C2 {Tt['c2_cac_attr']:4.0f}/{Tt['c2_cac_incr']:4.0f} | cost/new attr {Tt['cost_per_new_attr']:5.0f} incr {Tt['cost_per_new_incr']:5.0f} +impl {Tt['cost_per_new_incr_incl_impl']:5.0f} | val12 attr {Tt['value_attr']['m12']/1e5:5.2f}L incr {Tt['value_incr']['m12']/1e5:5.2f}L | net12 incr {Tt['net_incr']['m12']/1e5:6.2f}L net24 incr {Tt['net_incr']['m24']/1e5:6.2f}L net24 incr+impl {Tt['net_incr_incl_impl']['m24']/1e5:6.2f}L | net24 attr {Tt['net_attr']['m24']/1e5:6.2f}L | perf {Tt['performance_share']:.2f}")
        print("  breakeven", {k:(round(v,2) if v is not None else None) for k,v in res[("base",st)]["totals"]["breakeven"].items()}, "C2 value m24", round(res[("base",st)]["totals"]["c2_value"]["m24"]))
    print("sample 90/10:", [(x["baseline"], x["relative_lift"], x["n_control"], x["n_total"]) for x in sample_sizes()])
