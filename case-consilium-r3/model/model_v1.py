"""Single-source cohort, pricing and channel model for the BGCC Round 3 FanCode deck.
Run: python3 model.py  -> writes outputs/*.csv and outputs/model_outputs.json (consumed by deck/build_deck.js).
Every visible financial number in the deck must trace to this file."""
import json, csv, math, os, copy
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "assumptions.json")))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
t = A["tax"]["gst_rate"]; VC = A["variable_costs"]; SK = A["skus"]

def contrib(price, hours, cost_mult=1.0):
    """Contribution before marketing: net of GST, payment gateway, support/refunds, CDN."""
    return price/(1+t) - cost_mult*(VC["payment_gateway_share_of_gross"]+VC["support_refund_share_of_gross"])*price - cost_mult*VC["cdn_cost_per_hour_inr"]*hours

def c(sku, cm=1.0): return contrib(SK[sku]["price"], SK[sku]["hours"], cm)

def pathways(sc):
    """Expected contribution by pathway and horizon (d90, m12, m24) for each entry SKU under scenario sc."""
    cm = sc["cost_mult"]; C = A["cohorts"]
    c_s = c("session_model", cm); c_t89 = c("tournament_masters", cm); c_t79 = c("tournament_250_500", cm)
    c_tmix = (c_t89 + c_t79)/2
    c_fts = c("finish_season", cm)
    c_step_t_fts = contrib(SK["finish_season"]["price"]-SK["tournament_masters"]["price"], SK["finish_season"]["hours"]-SK["tournament_masters"]["hours"], cm)
    c_step_s_t = contrib(SK["tournament_masters"]["price"]-SK["session_model"]["price"], SK["tournament_masters"]["hours"]-SK["session_model"]["hours"], cm)
    c_399 = c("season_2027", cm); c_349 = c("season_2027_loyalty", cm); c_mon = c("monthly_pass", cm); c_f1 = c("f1_weekend", cm)
    m = C["cross_sport_monthly_take_rate"]; w = C["cross_sport_would_have_bought_f1_share"]
    xsport = m*(c_mon - w*c_f1)               # season-end bridge value per FTS-level holder (net of displaced F1 weekend pass)
    rep = {h: C["repeat_passes_beyond_entry"][h]*sc["repeat_mult"] for h in ("d90","m12","m24")}
    reps = {h: C["repeat_sessions_beyond_entry"][h]*sc["repeat_mult"] for h in ("d90","m12","m24")}
    r_u, r_f, r2 = sc["renewal_upg"], sc["renewal_fts"], C["renewal_2028_of_2027_renewers"]
    np27, np28 = C["non_renewer_passes_2027"], C["non_renewer_passes_2028_partial"]
    P = {}
    # tournament entrant pathways
    P["entry_only"] = {h: c_t89 for h in ("d90","m12","m24")}
    P["repeat_no_upgrade"] = {h: c_t89 + rep[h]*c_tmix for h in ("d90","m12","m24")}
    up90 = c_t89 + c_step_t_fts + xsport
    P["upgrade_via_credit"] = {"d90": up90,
        "m12": up90 + r_u*c_349 + (1-r_u)*np27*c_tmix,
        "m24": up90 + r_u*c_349 + (1-r_u)*np27*c_tmix + r_u*r2*c_399 + r_u*(1-r2)*np27*c_tmix + (1-r_u)*np28*c_tmix}
    fd90 = c_fts + xsport
    P["fts_direct"] = {"d90": fd90,
        "m12": fd90 + r_f*c_349 + (1-r_f)*np27*c_tmix,
        "m24": fd90 + r_f*c_349 + (1-r_f)*np27*c_tmix + r_f*r2*c_399 + r_f*(1-r2)*np27*c_tmix + (1-r_f)*np28*c_tmix}
    te = sc["tournament_entrant"]
    E_t = {h: te["p_entry_only"]*P["entry_only"][h] + te["p_repeat"]*P["repeat_no_upgrade"][h] + te["p_upgrade"]*P["upgrade_via_credit"][h] for h in ("d90","m12","m24")}
    se = C["session_entrant"]
    E_s = {h: se["p_never"]*c_s + se["p_repeat_sessions"]*(c_s + reps[h]*c_s) + se["p_upgrade_to_tournament"]*(c_s + c_step_s_t + (E_t[h]-c_t89)) for h in ("d90","m12","m24")}
    # cross-sell purchase by an existing payer (no cross-sport bridge value; same ladder otherwise)
    E_x = {"session": {h: E_s[h] for h in E_s}, "tournament": {h: E_t[h] for h in E_t}, "fts": {h: P["fts_direct"][h]-xsport for h in E_t}}
    units = dict(c_session=c_s, c_t79=c_t79, c_t89=c_t89, c_t99=c("tournament_finals",cm), c_tmix=c_tmix, c_fts=c_fts, c_step_t_fts=c_step_t_fts,
                 c_step_s_t=c_step_s_t, c_season399=c_399, c_season349=c_349, c_monthly=c_mon, c_f1_weekend=c_f1, xsport_value=xsport)
    return P, E_t, E_s, E_x, units

def breakeven_upgrade(E_paths, te, cac, h):
    """Two-path break-even upgrade share: non-upgrade path = mix of entry-only and repeat (weights from te)."""
    w_e, w_r = te["p_entry_only"], te["p_repeat"]
    c_non = (w_e*E_paths["entry_only"][h] + w_r*E_paths["repeat_no_upgrade"][h])/(w_e+w_r)
    c_up = E_paths["upgrade_via_credit"][h]
    if c_up - c_non <= 0: return None
    return (cac - c_non)/(c_up - c_non)

def run(scname):
    sc = A["scenarios"][scname]
    P, E_t, E_s, E_x, U = pathways(sc)
    C = A["cohorts"]; cann = C["cannibalisation"]; cm = sc["cost_mult"]
    def entrant_value(mix, h):
        mix = dict(mix); s = sc["session_shift"]
        # price/mix shift: move share from tournament to session (downside) or the reverse (upside)
        mix["session"] = mix.get("session",0)+s; mix["tournament"] = mix.get("tournament",0)-s
        return mix["session"]*E_s[h] + mix["tournament"]*E_t[h] + mix.get("fts",0)*P["fts_direct"][h], mix
    rows = []; tot = dict(spend=0, purchases=0, new_payers=0, incr_new=0, xsell=0, incr_xsell=0)
    for ch in A["channels"]:
        r = dict(id=ch["id"], name=ch["name"], group=ch["group"], spend=ch["spend"], share=ch["share"], persona=ch["persona"], execution=ch["execution"], evidence=ch["evidence"], rule=ch["rule"], method=ch["method"])
        f = min(1.0, ch.get("incremental_share",0)*sc["f_mult"])
        if ch["method"] == "cpm":
            imp = ch["spend"]/ch["cpm"]*1000; clicks = imp*ch["ctr"]; cpc = ch["spend"]/clicks
            purch = clicks*ch["cvr"]*sc["cvr_mult"]; newp = purch*ch["new_payer_share"]; incr = newp*f
            r.update(impressions=imp, clicks=clicks, cpc=cpc, cvr=ch["cvr"]*sc["cvr_mult"], purchases=purch, new_payers=newp, incr_new_payers=incr,
                     cac_attributed=ch["spend"]/newp, cac_incremental=ch["spend"]/incr, new_payer_share=ch["new_payer_share"], incremental_share=f)
            v12, mix = entrant_value(ch["mix"], "m12"); v24, _ = entrant_value(ch["mix"], "m24"); v90, _ = entrant_value(ch["mix"], "d90")
            r.update(value_d90=v90, value_m12=v12, value_m24=v24, mix=mix)
        elif ch["method"] == "cpc":
            clicks = ch["spend"]/ch["cpc"]; purch = clicks*ch["cvr"]*sc["cvr_mult"]; newp = purch*ch["new_payer_share"]; incr = newp*f
            r.update(clicks=clicks, cpc=ch["cpc"], cvr=ch["cvr"]*sc["cvr_mult"], purchases=purch, new_payers=newp, incr_new_payers=incr,
                     cac_attributed=ch["spend"]/newp, cac_incremental=ch["spend"]/incr, new_payer_share=ch["new_payer_share"], incremental_share=f)
            v12, mix = entrant_value(ch["mix"], "m12"); v24, _ = entrant_value(ch["mix"], "m24"); v90, _ = entrant_value(ch["mix"], "d90")
            r.update(value_d90=v90, value_m12=v12, value_m24=v24, mix=mix)
        elif ch["method"] == "owned":
            treated = {k: v*(1-ch["holdout"]) for k, v in ch["pools"].items()}
            conv = {k: treated[k]*ch["delivery"]*ch["click"][k]*ch["purchase"][k]*sc["cvr_mult"] for k in treated}
            newp = sum(conv[k] for k in ch["new_payer_pools"]); xs = sum(conv[k] for k in conv if k not in ch["new_payer_pools"])
            share_new = sum(treated[k] for k in ch["new_payer_pools"])/sum(treated.values())
            cost_new = ch["spend"]*share_new; cost_x = ch["spend"]-cost_new
            incr = newp*f; incr_x = xs*f
            r.update(treated_total=sum(treated.values()), treated_new_pool=sum(treated[k] for k in ch["new_payer_pools"]), conversions_by_pool=conv,
                     purchases=newp+xs, new_payers=newp, incr_new_payers=incr, xsell_purchases=xs, incr_xsell=incr_x,
                     cost_allocated_new=cost_new, cost_allocated_xsell=cost_x, cac_attributed=cost_new/newp, cac_incremental=cost_new/incr,
                     cost_per_xsell=cost_x/xs, cost_per_incr_xsell=cost_x/incr_x, incremental_share=f, new_payer_share=1.0)
            v12, mix = entrant_value(ch["mix_new"], "m12"); v24, _ = entrant_value(ch["mix_new"], "m24"); v90, _ = entrant_value(ch["mix_new"], "d90")
            r.update(value_d90=v90, value_m12=v12, value_m24=v24, mix=mix)
            mx = ch["mix_existing"]
            r.update(xsell_value_m12=sum(mx[k]*E_x[k]["m12"] for k in mx), xsell_value_m24=sum(mx[k]*E_x[k]["m24"] for k in mx), xsell_value_d90=sum(mx[k]*E_x[k]["d90"] for k in mx))
            tot["xsell"] += xs; tot["incr_xsell"] += incr_x
        else:
            r.update(purchases=None, new_payers=None, incr_new_payers=None, cac_attributed=None, cac_incremental=None)
        tot["spend"] += ch["spend"]
        if r.get("new_payers"): tot["purchases"] += r["purchases"]; tot["new_payers"] += r["new_payers"]; tot["incr_new"] += r["incr_new_payers"]
        rows.append(r)
    byid = {r["id"]: r for r in rows}
    d = A["dedup"]["overlap_share_removed"]
    dedup_removed = d*(byid["C3"]["new_payers"] + byid["C4"]["new_payers"]); dedup_removed_incr = d*(byid["C3"]["incr_new_payers"] + byid["C4"]["incr_new_payers"])
    paid_ids = ["C1","C2","C4"]
    paid_spend = sum(byid[i]["spend"] for i in paid_ids)
    paid_new = sum(byid[i]["new_payers"] for i in paid_ids) - d*byid["C4"]["new_payers"]
    paid_incr = sum(byid[i]["incr_new_payers"] for i in paid_ids) - d*byid["C4"]["incr_new_payers"]
    paid_ex_test_spend = paid_spend - byid["C1"]["spend"]; paid_ex_test_new = paid_new - byid["C1"]["new_payers"]; paid_ex_test_incr = paid_incr - byid["C1"]["incr_new_payers"]
    all_new = tot["new_payers"] - dedup_removed; all_incr = tot["incr_new"] - dedup_removed_incr
    # harmonic check on compatible paid rows (same denominator: attributed new payers)
    w = {i: byid[i]["spend"]/paid_spend for i in paid_ids}
    harmonic = 1/sum(w[i]/byid[i]["cac_attributed"] for i in paid_ids)
    # contribution totals
    def total_value(h):
        v = 0
        for i in ["C1","C2","C3","C4"]:
            v += byid[i]["new_payers"]*byid[i][f"value_{h}"]
        v -= dedup_removed*byid["C2"][f"value_{h}"]
        v += byid["C3"]["xsell_purchases"]*byid["C3"][f"xsell_value_{h}"]
        return v
    # cannibalisation (absolute, scenario-scaled)
    n_fts_direct = sum(byid[i]["new_payers"]*byid[i]["mix"].get("fts",0) for i in ["C1","C2","C3","C4"])
    n_t_entrants = sum(byid[i]["new_payers"]*byid[i]["mix"].get("tournament",0) for i in ["C1","C2","C3","C4"]) + byid["C3"]["xsell_purchases"]*A["channels"][2]["mix_existing"]["tournament"]
    n_upgraders = n_t_entrants*sc["tournament_entrant"]["p_upgrade"]
    n_renewers = n_upgraders*sc["renewal_upg"] + n_fts_direct*sc["renewal_fts"]
    loss_a = cann["fts_intender_leakage_share"]*n_fts_direct*(U["c_fts"]-U["c_t89"])
    loss_b = cann["multi_event_buyer_share_of_upgraders"]*n_upgraders*max(0, 3*U["c_tmix"]-(U["c_t89"]+U["c_step_t_fts"]))
    loss_c = cann["loyalty_discount_would_renew_anyway_share"]*n_renewers*(U["c_season399"]-U["c_season349"])
    cann_d90 = sc["cannib_mult"]*(loss_a+loss_b); cann_m12 = sc["cannib_mult"]*(loss_a+loss_b+loss_c); cann_m24 = cann_m12
    val = {h: total_value(h) for h in ("d90","m12","m24")}
    xsell_val = {h: byid["C3"]["xsell_purchases"]*byid["C3"][f"xsell_value_{h}"] for h in ("d90","m12","m24")}
    newp_val = {h: val[h]-xsell_val[h] for h in val}
    net = {"d90": val["d90"]-cann_d90-tot["spend"], "m12": val["m12"]-cann_m12-tot["spend"], "m24": val["m24"]-cann_m24-tot["spend"]}
    # acquisition-only view (paid rows C2+C4, the rows that would be scaled) and per-lakh steady state for C2
    acq_val = {h: byid["C2"]["new_payers"]*byid["C2"][f"value_{h}"] + (1-d)*byid["C4"]["new_payers"]*byid["C4"][f"value_{h}"] for h in ("d90","m12","m24")}
    acq_net = {h: acq_val[h] - (byid["C2"]["spend"]+byid["C4"]["spend"]) for h in acq_val}
    c2 = byid["C2"]; per_lakh = dict(new_payers=100000/c2["cac_attributed"], value_m12=100000/c2["cac_attributed"]*c2["value_m12"], value_m24=100000/c2["cac_attributed"]*c2["value_m24"])
    te = sc["tournament_entrant"]
    be = {f"be_upgrade_{h}_cac{cac}": breakeven_upgrade(P, te, cac, h) for h in ("m12","m24") for cac in (150, 175, 200, round(c2["cac_attributed"]))}
    return dict(scenario=scname, sc=sc, rows=rows, units=U, pathways=P, E_t=E_t, E_s=E_s, totals=dict(spend=tot["spend"], purchases=tot["purchases"], new_payers_attributed_dedup=all_new,
        incremental_new_payers=all_incr, xsell_purchases=tot["xsell"], incr_xsell=tot["incr_xsell"], dedup_removed=dedup_removed,
        paid_spend=paid_spend, paid_new_payers=paid_new, paid_blended_cac_attributed=paid_spend/paid_new, paid_blended_cac_incremental=paid_spend/paid_incr,
        paid_ex_test_cac_attributed=paid_ex_test_spend/paid_ex_test_new, paid_ex_test_cac_incremental=paid_ex_test_spend/paid_ex_test_incr,
        harmonic_check_paid=harmonic, programme_cost_per_new_payer=tot["spend"]/all_new, programme_cost_per_incremental_new_payer=tot["spend"]/all_incr,
        value=val, cannibalisation=dict(d90=cann_d90, m12=cann_m12, m24=cann_m24, loss_fts_leakage=loss_a, loss_multi_event=loss_b, loss_loyalty=loss_c, n_fts_direct=n_fts_direct, n_upgraders=n_upgraders, n_renewers=n_renewers),
        net=net, acq_value=acq_val, acq_net=acq_net, per_lakh_c2=per_lakh, xsell_value=xsell_val, new_payer_value=newp_val,
        value_per_new_payer_m12=(newp_val["m12"]-cann_m12)/all_new, value_per_new_payer_m24=(newp_val["m24"]-cann_m24)/all_new,
        value_per_new_payer_d90=(newp_val["d90"]-cann_d90)/all_new, breakeven=be))

def sample_sizes():
    from math import sqrt
    # normal approximation, two-sided alpha, per-arm n
    za = 1.959964; zb = 0.841621
    out = []
    for p0 in A["sample_size"]["baselines"]:
        for lift in A["sample_size"]["relative_lifts"]:
            p1 = p0*(1+lift); n = (za*sqrt(2*((p0+p1)/2)*(1-(p0+p1)/2)) + zb*sqrt(p0*(1-p0)+p1*(1-p1)))**2/(p1-p0)**2
            out.append(dict(baseline=p0, relative_lift=lift, treated_conv=p1, n_per_arm=math.ceil(n), eligible_with_10pct_holdout=math.ceil(n/0.10)))
    return out

if __name__ == "__main__":
    res = {s: run(s) for s in ("downside","base","upside")}
    B = res["base"]
    # ---- CSV outputs
    with open(os.path.join(OUT,"channel_plan_base.csv"),"w",newline="") as f:
        cols=["id","name","group","share","spend","persona","execution","method","clicks","cpc","cvr","purchases","new_payer_share","new_payers","incremental_share","incr_new_payers","cac_attributed","cac_incremental","value_m12","value_m24","xsell_purchases","cost_per_xsell","evidence","rule"]
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader()
        for r in B["rows"]: w.writerow({k:(round(v,2) if isinstance(v,float) else v) for k,v in r.items() if k in cols})
    with open(os.path.join(OUT,"cohort_pathways_base.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["pathway","d90","m12","m24"])
        for k,v in B["pathways"].items(): w.writerow([k]+[round(v[h],1) for h in ("d90","m12","m24")])
        w.writerow(["EXPECTED tournament entrant"]+[round(B["E_t"][h],1) for h in ("d90","m12","m24")])
        w.writerow(["EXPECTED session entrant"]+[round(B["E_s"][h],1) for h in ("d90","m12","m24")])
    with open(os.path.join(OUT,"scenarios.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["metric","downside","base","upside"])
        T=lambda s,k: res[s]["totals"][k]
        w.writerow(["new payers attributed (dedup)"]+[round(T(s,"new_payers_attributed_dedup")) for s in res])
        w.writerow(["incremental new payers"]+[round(T(s,"incremental_new_payers")) for s in res])
        w.writerow(["paid blended CAC attributed (C1+C2+C4)"]+[round(T(s,"paid_blended_cac_attributed")) for s in res])
        w.writerow(["paid blended CAC attributed excl. prospecting test"]+[round(T(s,"paid_ex_test_cac_attributed")) for s in res])
        w.writerow(["paid blended CAC incremental"]+[round(T(s,"paid_blended_cac_incremental")) for s in res])
        w.writerow(["programme cost per new payer (all ₹10 lakh)"]+[round(T(s,"programme_cost_per_new_payer")) for s in res])
        w.writerow(["12-month contribution per new payer (net of cannibalisation)"]+[round(T(s,"value_per_new_payer_m12")) for s in res])
        w.writerow(["24-month contribution per new payer"]+[round(T(s,"value_per_new_payer_m24")) for s in res])
        w.writerow(["90-day contribution per new payer"]+[round(T(s,"value_per_new_payer_d90")) for s in res])
        w.writerow(["cross-sell ATP purchases by existing payers"]+[round(T(s,"xsell_purchases")) for s in res])
        w.writerow(["90-day programme net (₹)"]+[round(res[s]["totals"]["net"]["d90"]) for s in res])
        w.writerow(["12-month programme net (₹)"]+[round(res[s]["totals"]["net"]["m12"]) for s in res])
        w.writerow(["24-month programme net (₹)"]+[round(res[s]["totals"]["net"]["m24"]) for s in res])
        w.writerow(["24-month acquisition-rows net C2+C4 (₹)"]+[round(res[s]["totals"]["acq_net"]["m24"]) for s in res])
        w.writerow(["break-even upgrade share 24m at C2 CAC"]+[res[s]["totals"]["breakeven"][f"be_upgrade_m24_cac{round(res[s]['rows'][1]['cac_attributed'])}"] for s in res])
    with open(os.path.join(OUT,"sample_sizes.csv"),"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["baseline","relative_lift","treated_conv","n_per_arm","eligible_with_10pct_holdout"]); w.writeheader(); w.writerows(sample_sizes())
    # sensitivity: tournament entrant 24m and 12m value by upgrade share x repeat passes multiplier
    sens=[]
    for u in (0.10,0.20,0.30,0.40):
        for rm in (0.6,1.0,1.4):
            sc=copy.deepcopy(A["scenarios"]["base"]); sc["tournament_entrant"]={"p_entry_only":0.6-u*1.0 if False else round(0.4-(u-0.2),2),"p_repeat":0.40,"p_upgrade":u}; sc["repeat_mult"]=rm
            P,E_t,E_s,E_x,U=pathways(sc); sens.append(dict(upgrade_share=u,repeat_passes_12m=round(A["cohorts"]["repeat_passes_beyond_entry"]["m12"]*rm,2),repeat_passes_24m=round(A["cohorts"]["repeat_passes_beyond_entry"]["m24"]*rm,2),value_m12=round(E_t["m12"],1),value_m24=round(E_t["m24"],1)))
    with open(os.path.join(OUT,"sensitivity_tournament_entrant.csv"),"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(sens[0].keys())); w.writeheader(); w.writerows(sens)
    # rate card
    with open(os.path.join(OUT,"rate_card.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["sku","price_inr","status","label","contribution_before_marketing_inr"])
        for k,v in SK.items(): w.writerow([k,v["price"],v["status"],v["label"],round(contrib(v["price"],v["hours"]),1)])
    # contest CPC ceilings (case CVR 7.8%)
    ceilings = {"all_new_payers": {"150": 150*0.078, "200": 200*0.078}, "n055": {"150": 150*0.078*0.55, "200": 200*0.078*0.55}, "n055_f05": {"150": 150*0.078*0.55*0.5, "200": 200*0.078*0.55*0.5}}
    per10k = dict(eligible=10000, treated=9000, delivered=8100, clicks=8100*0.05, purchases=8100*0.05*0.08, incremental=8100*0.05*0.08*0.5)
    summary = dict(meta=A["meta"], units=B["units"], pathways=B["pathways"], E_t=B["E_t"], E_s=B["E_s"], base_totals=B["totals"], rows_base=B["rows"],
                   scenarios={s: dict(totals=res[s]["totals"], E_t=res[s]["E_t"], E_s=res[s]["E_s"], pathways=res[s]["pathways"], rows={r["id"]: {k: r.get(k) for k in ("new_payers","incr_new_payers","cac_attributed","cac_incremental","value_m12","value_m24","xsell_purchases")} for r in res[s]["rows"]}) for s in res},
                   sensitivity=sens, sample_sizes=sample_sizes(), contest_cpc_ceilings=ceilings, crm_per_10k=per10k, competitors=A["competitors"], skus=SK, credit_ladder=A["credit_ladder"], cohorts=A["cohorts"], channels=A["channels"], dedup=A["dedup"], current_allocation=A["current_allocation"], tax=A["tax"], variable_costs=VC)
    json.dump(summary, open(os.path.join(OUT,"model_outputs.json"),"w"), indent=1, default=lambda o: None)
    # ---- console digest
    print("UNIT CONTRIBUTIONS:", {k: round(v,1) for k,v in B["units"].items()})
    print("PATHWAYS (d90/m12/m24):"); [print(f"  {k:22s}", [round(v[h],1) for h in ("d90","m12","m24")]) for k,v in B["pathways"].items()]
    print("  E[tournament entrant]", [round(B["E_t"][h],1) for h in ("d90","m12","m24")]); print("  E[session entrant]   ", [round(B["E_s"][h],1) for h in ("d90","m12","m24")])
    for r in B["rows"]:
        if r.get("new_payers"): print(f"{r['id']} spend {r['spend']:>7} purch {r['purchases']:7.0f} newp {r['new_payers']:7.0f} incr {r['incr_new_payers']:6.0f} CACattr {r['cac_attributed']:6.0f} CACincr {r['cac_incremental']:6.0f} v12 {r['value_m12']:5.0f} v24 {r['value_m24']:5.0f}" + (f" xsell {r['xsell_purchases']:.0f} cost/xsell {r['cost_per_xsell']:.0f}" if r.get('xsell_purchases') else ""))
    T=B["totals"]; print({k:(round(v) if isinstance(v,(int,float)) else v) for k,v in T.items() if k not in ("value","net","acq_value","acq_net","per_lakh_c2","breakeven","cannibalisation")})
    print("value",{k:round(v) for k,v in T["value"].items()}, "cannib",{k:round(v) for k,v in T["cannibalisation"].items()}); print("net",{k:round(v) for k,v in T["net"].items()}, "acq_net",{k:round(v) for k,v in T["acq_net"].items()}, "per lakh C2", {k:round(v) for k,v in T["per_lakh_c2"].items()})
    print("breakeven", {k:(round(v,3) if v is not None else None) for k,v in T["breakeven"].items()})
    for s in res: print(s, "newp", round(res[s]["totals"]["new_payers_attributed_dedup"]), "incr", round(res[s]["totals"]["incremental_new_payers"]), "paidCAC", round(res[s]["totals"]["paid_blended_cac_attributed"]), "exTest", round(res[s]["totals"]["paid_ex_test_cac_attributed"]), "incrCAC", round(res[s]["totals"]["paid_blended_cac_incremental"]), "v12/np", round(res[s]["totals"]["value_per_new_payer_m12"]), "v24/np", round(res[s]["totals"]["value_per_new_payer_m24"]), "net12", round(res[s]["totals"]["net"]["m12"]), "net24", round(res[s]["totals"]["net"]["m24"]), "acqnet24", round(res[s]["totals"]["acq_net"]["m24"]))
    print("sample sizes:", [(x["baseline"], x["relative_lift"], x["n_per_arm"]) for x in sample_sizes()])
    print("sensitivity 24m:", [(x["upgrade_share"], x["repeat_passes_24m"], x["value_m24"]) for x in sens])
