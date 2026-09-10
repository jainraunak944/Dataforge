// CaseConsilium_Wookies deck generator
const pptxgen = require("pptxgenjs");
const { C, PAGE, FONT, header, footer, soWhat, secLabel } = require("./theme");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Team Wookies";
pres.title = "Case Consilium 2026 - EP Biocomposites Limited";

const T = (t, o = {}) => ({ text: t, options: o });

// Table cell helpers
function cell(text, opts = {}) {
  return {
    text,
    options: Object.assign({
      fontFace: FONT, fontSize: 8.5, color: C.ink, valign: "top", align: "left",
      border: [{ type: "solid", color: C.line, pt: 0.5 }, { type: "solid", color: C.line, pt: 0.5 },
               { type: "solid", color: C.line, pt: 0.5 }, { type: "solid", color: C.line, pt: 0.5 }],
      margin: [0.035, 0.05, 0.035, 0.05],
    }, opts),
  };
}
function hcell(text, opts = {}) {
  return cell(text, Object.assign({ bold: true, color: "FFFFFF", fill: { color: C.navy }, valign: "middle", fontSize: 8.5 }, opts));
}
function lcell(text, opts = {}) { // label cell (left column)
  return cell(text, Object.assign({ bold: true, color: C.navy, fill: { color: C.panel } }, opts));
}

/* ================= SLIDE 1: COVER ================= */
(function cover() {
  const s = pres.addSlide();
  s.background = { color: C.navy };
  // subtle concentric circle motif, right side
  [2.6, 2.0, 1.4].forEach((r, i) => {
    s.addShape("ellipse", {
      x: 10.6 - r, y: 3.75 - r, w: 2 * r, h: 2 * r,
      fill: { type: "none" }, line: { color: C.teal, width: 1.1, transparency: 55 + i * 10 },
    });
  });
  s.addShape("ellipse", { x: 10.6 - 0.06, y: 3.75 - 0.06, w: 0.12, h: 0.12, fill: { color: C.amber }, line: { type: "none" } });

  s.addText("CASE CONSILIUM 2026  |  ROUND 2  |  BGCC, BITS PILANI K K BIRLA GOA CAMPUS", {
    x: 0.75, y: 0.62, w: 11, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: "9FC4C3", charSpacing: 2, bold: true,
  });
  s.addText("EP Biocomposites Limited", {
    x: 0.75, y: 2.05, w: 9.4, h: 0.95, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 44, color: "FFFFFF", bold: true,
  });
  s.addText("Concentrate to conquer: three private buyers, one west-coast corridor,\nservice-led growth from ₹11.7 crore to ₹25 crore by FY29", {
    x: 0.75, y: 3.12, w: 8.9, h: 1.0, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 17, color: "CFE3E2", lineSpacingMultiple: 1.12,
  });
  s.addShape("line", { x: 0.78, y: 4.62, w: 2.2, h: 0, line: { color: C.amber, width: 2 } });
  s.addText("TEAM WOOKIES", {
    x: 0.75, y: 4.85, w: 6, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 15, color: C.amber, bold: true, charSpacing: 2.5,
  });
  s.addText("Raunak Jain      Dhruv Mundra      Khushi Jha      Sambhav Khandelwal", {
    x: 0.75, y: 5.26, w: 10, h: 0.35, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13.5, color: "E8EFF2",
  });
  s.addText("Bio-digester toilets  |  decentralised STP / ETP  |  wastewater reuse   -   private-pay Tier 2/3 markets of Goa, Maharashtra and Karnataka", {
    x: 0.75, y: 6.78, w: 11.8, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 10, color: "7E98A8",
  });
})();

/* ================= SLIDE 2: EXECUTIVE SUMMARY ================= */
(function exec() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Executive summary", "Win three compliance-driven buyers in a serviceable corridor, then let service quality, not geography, set the pace", { titleSize: 20, titleH: 0.62 });

  const rows = [
    ["Priority personas", "Coastal and leisure hoteliers (20-150 keys), Tier-2 residential developers (100-400 units), and private hospitals (30-150 beds). They score 4.50, 3.80 and 3.75 on our 10-factor weighted framework; all three buy under a compliance trigger, not discretionary demand."],
    ["Market opportunity", "Private-pay decentralised demand in the three states is ~₹270 cr/yr (bottom-up); ₹165 cr/yr is serviceable from EPBL's corridor and capability. Realistic 3-year capture: ₹15-28 cr of new revenue (base ₹21 cr), on top of the existing ₹11.7 cr base."],
    ["Where to start", "Phase 1 is Goa plus the 250 km corridor: Sindhudurg-Ratnagiri, Kolhapur, Belagavi, where EPBL is the only in-state OEM with references. Karnataka's Tier-2 anchors (Hubballi-Dharwad, Mangaluru, Mysuru) follow in Year 2, Tier-3 depth via partners in Year 3."],
    ["Commercial model", "Audit-led direct sales plus MEP-consultant and CREDAI/hotel-association channels; standardised 10/25/50/100 KLD FRP packages; 30-40-25-5 milestone billing; AMC attached to ≥60% of new installs."],
    ["End of Year 3", "₹25.4 cr revenue (2.2x FY26), ~66 new treatment projects and 400+ bio-digesters delivered, ₹2.4 cr/yr recurring service revenue, receivable days ≤75, all funded from internal accruals and IPO working capital (~₹6 cr investment over 3 years)."],
    ["Adjacent offerings", "1) STP Rescue: retrofit and O&M takeover of failing third-party plants (launch now, zero capex). 2) SmartSTP: IoT compliance monitoring on the AMC fleet (month 6). 3) AquaLoop: water-reuse polishing module built on the IISc MoU (months 9-12)."],
    ["Biggest risk", "Developer receivables stretching working capital. Control: milestone billing with advances, credit checks and PDCs, developer exposure capped at 25% of the order book, and KPI gates that stop expansion when DSO exceeds 75 days."],
  ];
  let y = y0 + 0.04;
  const rh = [0.72, 0.72, 0.72, 0.60, 0.72, 0.72, 0.62];
  rows.forEach((r, i) => {
    s.addText(r[0].toUpperCase(), {
      x: PAGE.mL, y, w: 1.72, h: rh[i], isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.5, bold: true, color: C.teal, valign: "top", lineSpacingMultiple: 1.0,
    });
    s.addText(r[1], {
      x: 2.42, y, w: 6.28, h: rh[i], isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.8, color: C.ink, valign: "top", lineSpacingMultiple: 1.04,
    });
    if (i < rows.length - 1) s.addShape("line", { x: PAGE.mL, y: y + rh[i] + 0.035, w: 8.15, h: 0, line: { color: C.line, width: 0.75 } });
    y += rh[i] + 0.10;
  });

  // Right stat panel
  const px = 9.0, pw = 3.78;
  s.addShape("roundRect", { x: px, y: y0 + 0.04, w: pw, h: 5.42, rectRadius: 0.07, fill: { color: C.navy }, line: { type: "none" } });
  s.addText("EPBL BY FY29 (BASE CASE)", {
    x: px + 0.22, y: y0 + 0.22, w: pw - 0.44, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 10.5, bold: true, color: C.amber, charSpacing: 1.5,
  });
  const stats = [
    ["₹25.4 cr", "revenue, 2.2x the FY26 base of ₹11.7 cr"],
    ["₹21 cr", "cumulative new private-market revenue FY27-29 (range ₹15-28 cr)"],
    ["7.2%", "share of serviceable annual demand by FY29, from ~0% today"],
    ["₹2.4 cr/yr", "recurring AMC, O&M and monitoring revenue (~10% of sales)"],
    ["14 clusters", "across 3 states, via 2 service hubs and 25 certified partners"],
  ];
  let sy = y0 + 0.62;
  stats.forEach((st, i) => {
    s.addText(st[0], { x: px + 0.22, y: sy, w: pw - 0.44, h: 0.42, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 21, bold: true, color: "FFFFFF" });
    s.addText(st[1], { x: px + 0.22, y: sy + 0.40, w: pw - 0.44, h: 0.42, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 8.8, color: "BFD3DE", lineSpacingMultiple: 1.02 });
    if (i < stats.length - 1) s.addShape("line", { x: px + 0.22, y: sy + 0.85, w: pw - 0.44, h: 0, line: { color: "2B4E6E", width: 0.75 } });
    sy += 0.97;
  });
  footer(s, "Figures from the market model on p.4 and roadmap on p.5; FY26 base per BGCC problem statement. All FY27-29 figures are estimates.", 2);
})();

/* ================= SLIDE 3: CORE 1 - SEGMENTATION ================= */
(function core1() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Deliverable 1 | Customer segmentation and targeting", "Three of eight private buyer segments justify focused pursuit: hoteliers, Tier-2 developers and private hospitals", { titleSize: 20, titleH: 0.62 });

  /* ---- Left: bubble matrix ---- */
  const mx = PAGE.mL, my = y0 + 0.30, mw = 4.55, mh = 3.55;
  secLabel(s, "Segment attractiveness, 10-factor weighted score", mx, y0 + 0.02, mw + 0.4, { size: 11 });
  // plot frame
  s.addShape("rect", { x: mx, y: my, w: mw, h: mh, fill: { color: "FBFCFD" }, line: { color: C.line, width: 1 } });
  // quadrant lines (x range 2.2-5.1, y range 2.5-5.0)
  const X = v => mx + ((v - 2.2) / 2.9) * mw;
  const Y = v => my + mh - ((v - 2.5) / 2.5) * mh;
  s.addShape("line", { x: X(3.65), y: my, w: 0, h: mh, line: { color: C.line, width: 0.75, dashType: "dash" } });
  s.addShape("line", { x: mx, y: Y(3.75), w: mw, h: 0, line: { color: C.line, width: 0.75, dashType: "dash" } });
  // bubbles: [name, ease(x), value(y), ticketL, priority?]
  const B = [
    ["Societies (retrofit)", 3.00, 3.33, 14, 0],
    ["MSME industrial", 2.75, 3.50, 40, 0],
    ["Commercial dev.", 2.88, 3.17, 35, 0],
    ["Schools & CSR", 3.25, 2.92, 14, 0],
    ["Homeowners", 4.38, 2.83, 0.6, 0],
    ["Hoteliers", 4.38, 4.58, 24, 1],
    ["Developers", 2.88, 4.42, 48, 1],
    ["Hospitals", 3.88, 3.67, 16, 1],
  ];
  B.forEach(([name, ex, vy, tick, pri]) => {
    const r = 0.11 + Math.sqrt(tick) * 0.038;
    s.addShape("ellipse", {
      x: X(ex) - r, y: Y(vy) - r, w: 2 * r, h: 2 * r,
      fill: { color: pri ? C.amber : C.aqua, transparency: pri ? 8 : 42 },
      line: { color: pri ? "B37417" : C.teal, width: pri ? 1.5 : 0.8 },
    });
  });
  // labels placed to avoid overlap
  const L = [
    ["Hoteliers", 4.38, 4.58, 0.0, -0.40, 1], ["Developers", 2.88, 4.42, 0.05, -0.50, 1],
    ["Hospitals", 3.88, 3.67, 0.62, -0.28, 1], ["Homeowners", 4.38, 2.83, 0.0, 0.26, 0],
    ["Societies (retrofit)", 3.00, 3.33, -0.20, -0.48, 0], ["MSME industrial", 2.75, 3.50, 0.30, -0.60, 0],
    ["Schools & CSR", 3.25, 2.92, 0.68, 0.0, 0], ["Commercial dev.", 2.88, 3.17, 0.0, 0.44, 0],
  ];
  L.forEach(([name, ex, vy, dx, dy, pri]) => {
    s.addText(name, {
      x: X(ex) - 0.75 + dx, y: Y(vy) + dy - 0.10, w: 1.5, h: 0.22, isTextBox: true, margin: 0, align: "center",
      fontFace: FONT, fontSize: 8, bold: !!pri, color: pri ? C.navy : C.mut,
    });
  });
  // axes titles
  s.addText("Ease of capture →  (access to decision maker, cycle, payment reliability, serviceability, rivalry)", {
    x: mx, y: my + mh + 0.05, w: mw, h: 0.32, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.5, color: C.mut, align: "center",
  });
  s.addText("Value at stake →", {
    x: mx - 1.62, y: my + mh / 2 - 0.10, w: 3.2, h: 0.2, isTextBox: true, margin: 0, rotate: 270,
    fontFace: FONT, fontSize: 7.5, color: C.mut, align: "center",
  });
  s.addText("Bubble area = average ticket size (₹0.6 L to ₹48 L). Amber = priority personas.", {
    x: mx, y: my + mh + 0.34, w: mw, h: 0.22, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.5, color: C.mut, align: "center",
  });
  s.addText([
    T("Weights: ", { bold: true, color: C.navy, fontSize: 7.8 }),
    T("demand 15 · compliance urgency 15 · product fit 10 · ticket 10 · decision-maker access 10 · payment reliability 10 · repeat & AMC 10 · serviceability 10 · rivalry 5 · cycle 5. Scores 1-5, evidence in backup (p.9).", { color: C.mut, fontSize: 7.8 }),
  ], { x: mx, y: my + mh + 0.60, w: mw, h: 0.55, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.05 });

  /* ---- Right: persona table ---- */
  const tx = 5.42, tw = 7.36;
  secLabel(s, "Priority persona playbook", tx, y0 + 0.02, tw, { size: 11 });
  const P = (t, o = {}) => cell(t, Object.assign({ fontSize: 8.0 }, o));
  const PH = (t) => cell(t, { bold: true, color: "FFFFFF", fill: { color: C.teal }, fontSize: 8.6, valign: "middle" });
  const PL = (t) => cell(t, { bold: true, color: C.navy, fill: { color: C.panel }, fontSize: 8.0 });
  const tableRows = [
    [PL(""), PH("1 | Coastal & leisure hotelier"), PH("2 | Tier-2 residential developer"), PH("3 | Private hospital / clinic")],
    [PL("Who & trigger"), P("20-150 key hotels, resorts, hostels in Goa, Konkan, hill towns. Trigger: GSPCB/MPCB consent renewal or notice, expansion, tanker-water cost."), P("100-400 unit projects in Kolhapur, Belagavi, Hubballi, Mysuru. Trigger: EC condition (≥20,000 sqm) and occupancy certificate need a working STP."), P("30-150 bed private hospitals. Trigger: BMW Rules 2016 mandate effluent treatment for >10-bed facilities; NABH audits; SPCB consent.")],
    [PL("Decision maker"), P("Owner-promoter decides; GM, chief engineer and PCB consultant influence."), P("Promoter/director decides; MEP consultant, PMC and liaison architect specify."), P("Owner-doctor or trustee decides; hospital administrator and biomedical engineer influence.")],
    [PL("How they shortlist"), P("Peer referrals, MEP consultants, TTAG/GCCI association contacts, visible local installs."), P("Consultant empanelment, CREDAI chapter events, past-project references."), P("Hospital consultants, IMA/AHPI chapters, PCB-liaison advisors.")],
    [PL("Price they bear"), P("₹18-45 L turnkey (10-50 KLD) + AMC ₹0.6-1.5 L/yr."), P("₹35 L-1.2 cr design-build (25-150 KLD), milestone billed."), P("₹12-35 L compact ETP/STP skid (5-30 KLD) + AMC ₹0.8-2 L/yr.")],
    [PL("Cycle & proof"), P("2-4 months. Needs reference visits, effluent lab reports, uptime SLA, DRDO-certified pedigree."), P("6-9 months, tracks construction. Needs 200+ housing installs, ONGC 100-KLD MBR reference, bank guarantee."), P("3-6 months. Needs compliance document pack, disinfection performance, live-site install method.")],
    [PL("Entry offer → onboarding"), P("₹25k water & compliance audit credited to order → design in 7 days → fixed-price modular install ≤4 weeks → AMC with quarterly lab reports."), P("Free STP sizing + compliance plan at EC stage → spec-in via consultant → staged install → society handover kit with 3-yr O&M."), P("BMW-compliance liquid-waste audit → PCB liaison support → phased install in live hospital → compliance dashboard reporting.")],
    [PL("Repeat & referral"), P("Sister properties, reuse-module upsell, consumables; dense hotel clusters refer."), P("Next projects, retrofit of older stock, society O&M annuity after handover."), P("Sister facilities, disinfection upgrades, long AMC tenure; doctor networks refer.")],
  ];
  s.addTable(tableRows, {
    x: tx, y: y0 + 0.30, w: tw,
    colW: [0.86, 2.17, 2.17, 2.16],
    border: { type: "solid", color: C.line, pt: 0.5 },
    autoPage: false,
  });

  soWhat(s, "Decision", "Put 80% of new-business effort on these three personas. Homeowners stay a dealer-led run-rate business; industrial ETPs are taken opportunistically, not pursued.", 6.44);
  footer(s, "Sources: GSPCB consent framework (susbio.in guide); Bio-medical Waste Mgmt Rules 2016 (>10-bed ETP mandate); EIA Notification 2006 item 8(a); KSPCB apartment STP rules (Deccan Herald, 2024); EPBL references (epbiocomposites.com; EquityBulls, Dec 2023). Scores: team analysis.", 3);
})();

/* ================= SLIDE 4: CORE 2 - MARKET & COMPETITION ================= */
(function core2() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Deliverable 2a | Market opportunity and competitive positioning", "A ~₹270 cr/yr private market; EPBL can credibly win ₹15-28 cr of new revenue over three years", { titleSize: 20, titleH: 0.62 });

  /* ---- Left: TAM/SAM/SOM funnel ---- */
  const fx = PAGE.mL, fy = y0 + 0.28;
  secLabel(s, "Bottom-up opportunity (annual)", fx, y0 + 0.02, 4.3, { size: 11 });
  const funnel = [
    ["TAM  ₹270 cr/yr", "All private-pay decentralised demand, Tier 2/3 of Goa + MH + KA (₹239 cr STP/ETP + ₹32 cr bio-digester)", 4.30, C.navy],
    ["SAM  ₹165 cr/yr", "Within EPBL's 3-phase corridor & capability; ₹5 L-2.5 cr projects; excludes complex industrial chemistry", 3.55, C.teal],
    ["SOM  ₹21 cr", "3-yr cumulative NEW revenue FY27-29 (range ₹15-28 cr); FY29 run-rate = 7.2% of SAM", 2.80, C.amber],
  ];
  let fyy = fy;
  funnel.forEach(([big, sub, w, col]) => {
    s.addShape("roundRect", { x: fx, y: fyy, w, h: 0.68, rectRadius: 0.05, fill: { color: col }, line: { type: "none" } });
    s.addText(big, { x: fx + 0.12, y: fyy + 0.03, w: w - 0.2, h: 0.24, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: "FFFFFF" });
    s.addText(sub, { x: fx + 0.12, y: fyy + 0.26, w: w - 0.2, h: 0.40, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 6.9, color: "FFFFFF", lineSpacingMultiple: 0.98 });
    fyy += 0.76;
  });
  // state split + formula
  s.addText([
    T("By state (TAM): ", { bold: true, color: C.navy, fontSize: 8 }),
    T("MH 59% · KA 28% · Goa 13%; Goa is smallest but highest win-rate (home market). ", { color: C.ink, fontSize: 8 }),
    T("Formula: ", { bold: true, color: C.navy, fontSize: 8 }),
    T("units x %lacking x fit x conversion x ticket, per segment per state (p.9).", { color: C.ink, fontSize: 8 }),
  ], { x: fx, y: fyy + 0.04, w: 4.35, h: 0.42, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.02 });

  /* ---- Middle: SAM by segment (native bar) ---- */
  const cx = 5.15, cw = 3.55;
  secLabel(s, "SAM by segment, ₹cr/yr", cx, y0 + 0.02, cw, { size: 11 });
  s.addChart("bar", [{
    name: "SAM",
    labels: ["Residential developers", "Hospitality", "Bio-digesters (retail)", "Hospitals", "Societies retrofit", "Education & CSR", "Commercial"],
    values: [96.8, 27.5, 20.9, 8.6, 5.9, 3.4, 2.4],
  }], {
    x: cx, y: fy - 0.02, w: cw, h: 2.30, barDir: "bar",
    chartColors: [C.teal], showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: C.navy, dataLabelFontSize: 8, dataLabelFontFace: FONT, dataLabelFormatCode: "0.#",
    catAxisLabelColor: C.ink, catAxisLabelFontSize: 8, catAxisLabelFontFace: FONT,
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    valAxisMaxVal: 110, barGapWidthPct: 45,
  });
  s.addText([
    T("Developers dominate value but pay slowly: ", { color: C.ink, fontSize: 8 }),
    T("SOM tilts to hotels & hospitals first; ", { bold: true, color: C.navy, fontSize: 8 }),
    T("developer exposure capped at 25% of order book.", { color: C.ink, fontSize: 8 }),
  ], { x: cx, y: fy + 2.34, w: cw, h: 0.62, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.04 });

  /* ---- Right: sensitivities ---- */
  const rx = 9.05, rw = 3.73;
  secLabel(s, "Scenarios & key sensitivities", rx, y0 + 0.02, rw, { size: 11 });
  const scT = [
    [hcell("FY29, ₹cr", { fontSize: 7.8 }), hcell("Cons.", { fontSize: 7.8, align: "center" }), hcell("Base", { fontSize: 7.8, align: "center" }), hcell("Upside", { fontSize: 7.8, align: "center" })],
    [cell("Total revenue", { fontSize: 7.8 }), cell("22.1", { align: "center", fontSize: 7.8 }), cell("25.4", { align: "center", fontSize: 7.8, bold: true, fill: { color: C.amberLt } }), cell("29.3", { align: "center", fontSize: 7.8 })],
    [cell("Cum. new rev. FY27-29", { fontSize: 7.8 }), cell("15.0", { align: "center", fontSize: 7.8 }), cell("20.7", { align: "center", fontSize: 7.8, bold: true, fill: { color: C.amberLt } }), cell("27.6", { align: "center", fontSize: 7.8 })],
    [cell("Cum. total rev. FY27-29", { fontSize: 7.8 }), cell("53.7", { align: "center", fontSize: 7.8 }), cell("59.4", { align: "center", fontSize: 7.8, bold: true, fill: { color: C.amberLt } }), cell("66.3", { align: "center", fontSize: 7.8 })],
  ];
  s.addTable(scT, { x: rx, y: fy - 0.02, w: rw, colW: [1.63, 0.70, 0.70, 0.70], autoPage: false });
  s.addText([
    T("Swing factors: ", { bold: true, color: C.navy, fontSize: 8 }),
    T("hotel conversion 6→10%/yr (±₹9 cr TAM); developer STP-trigger share 15→25% (±₹35 cr); win-rate 15→25%. Checks: FY29 needs 34 installs/yr (5 crews, feasible); receivables at 75 DSO = ₹5.2 cr vs net worth >₹12 cr.", { color: C.ink, fontSize: 8 }),
  ], { x: rx, y: fy + 1.24, w: rw, h: 1.55, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.05 });

  /* ---- Bottom: competitor table ---- */
  const ty = 4.50;
  secLabel(s, "Competitor & technology landscape (researched)", PAGE.mL, ty - 0.26, 9, { size: 11 });
  const K = (t, o = {}) => cell(t, Object.assign({ fontSize: 7.2 }, o));
  const KH = (t) => cell(t, { bold: true, color: "FFFFFF", fill: { color: C.navy }, fontSize: 7.6, valign: "middle" });
  const comp = [
    [KH("Player"), KH("Technology"), KH("Focus & scale"), KH("Presence"), KH("Whitespace EPBL exploits")],
    [K("Daiki Axis India", { bold: true }), K("Johkasou FRP capsule, 1-50 KLD"), K("Villas, hotels, institutions"), K("Pan-India dealers; ₹200 cr Tumakuru (KA) plant announced"), K("Dealer-led premium import; thin local turnkey-civil + AMC depth")],
    [K("Ion Exchange", { bold: true }), K("INDION packaged, SBR, MBR"), K("SME to municipal, all scales"), K("Pan-India partner network"), K("Small jobs routed to partners, little direct engineering attention")],
    [K("Thermax", { bold: true }), K("FabX MBBR, BioCask packaged, custom ETP"), K("Industrial & large commercial; >1 MLD sweet spot"), K("Pan-India"), K("10-50 KLD packaged sold via 3rd-party distributors, not a focus")],
    [K("Banka BioLoo", { bold: true }), K("DRDO-inoculum bio-toilets, STP, FSM"), K("Railways, institutions (₹56.5 cr rev.)"), K("Pan-India, Hyderabad base"), K("Rail-centric; weak west-coast hospitality presence")],
    [K("SUSBIO (Pune)", { bold: true }), K("ECOTREAT anaerobic + MBBR FRP, 1-500 KLD"), K("Hotels, resorts; from ₹35k/KLD, 3-5 day install"), K("Maharashtra & west"), K("Sharpest rival: match its speed; beat it on Goa/KA service + certification")],
    [K("Netsol / Kelvin (NCR)", { bold: true }), K("MBBR / MBR / SBR fabrication"), K("Commercial & industrial"), K("Pan-India claims; no verified GA/MH/KA installs"), K("Remote AMC response; local 24-48h service wins")],
    [K("CDD Society / Boson", { bold: true }), K("DEWATS nature-based; STP-water polishing + IoT (WaaS)"), K("Communities; Bengaluru apartments"), K("Karnataka base"), K("Adjacent models to learn from (reuse, WaaS), not plant rivals in Tier 2/3")],
  ];
  s.addTable(comp, {
    x: PAGE.mL, y: ty, w: 12.23,
    colW: [1.55, 2.45, 2.55, 2.30, 3.38],
    autoPage: false,
  });

  soWhat(s, "Positioning", "EPBL, the west-coast compliance partner: in-state FRP manufacturing, DRDO-certified ToT, MBBR/SBR/MBR + ozone range, 24-48h corridor service; sold on audited compliance and lifecycle cost, not lowest capex.", 6.56, 0.46, 11);
  footer(s, "Sources: CPCB STP Inventory 2021; Goa Tourism 2024; HVS-ANAROCK 2024; MahaRERA (Construction World, 2025); 99acres RERA counts; BMW Rules 2016; company sites: daikiaxis.in, ionexchangeglobal.com, thermaxglobal.com, susbio.in, netsolwater.com, cddindia.org; Screener (Banka). Full URLs p.8; model assumptions p.9.", 4);
})();

/* ================= SLIDE 5: CORE 3 - ROADMAP ================= */
(function core3() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Deliverable 2b | Three-year go-to-market roadmap", "Corridor by corridor, gated by service quality and cash: ₹11.7 cr → ₹25.4 cr by FY29", { titleSize: 20, titleH: 0.62 });

  /* ---- Phase cards ---- */
  const py = y0 + 0.02, ph = 3.06, pw = 3.78, gap = 0.44;
  const phases = [
    {
      name: "PHASE 1 · FY27", title: "Fortress Goa + Konkan", col: C.teal,
      rows: [
        ["Where", "Goa (all), Sindhudurg-Ratnagiri, Kolhapur, Belagavi (≤250 km of Bicholim)"],
        ["Who", "Hoteliers first, hospitals, selective developers"],
        ["Sell", "10/25/50 KLD FRP packages; ₹25k compliance audit entry offer; bio-digester retail; STP Rescue retrofits"],
        ["Route", "Founder-led ABM + 2 account managers; 15 MEP consultants; TTAG, GCCI, CREDAI Kolhapur; 10 plumber-dealers"],
        ["Invest", "₹1.4 cr: hires, demo skids, service van, CRM, NABL lab tie-up"],
        ["Target", "₹3.0-3.5 cr new orders · 10 installs · AMC attach ≥50%"],
      ],
    },
    {
      name: "PHASE 2 · FY28", title: "Karnataka corridor", col: C.navy2,
      rows: [
        ["Where", "+ Hubballi-Dharwad, Mangaluru, Mysuru, Sangli probe; Belagavi service hub + Mangaluru spoke"],
        ["Who", "Developers scaled up, hospitals, education & CSR campuses"],
        ["Sell", "+ 100 KLD series, hospital ETP skid, SmartSTP monitoring, 3-yr O&M handover contracts"],
        ["Route", "25 consultants; 6 EPC install franchisees; AHPI/IMA chapters; CSR implementation partners"],
        ["Invest", "₹2.2 cr: 2 hubs, 4 hires, inventory, monitoring stock"],
        ["Target", "₹6.4 cr new revenue · channel ≥40% of pipeline · uptime ≥95%"],
      ],
    },
    {
      name: "PHASE 3 · FY29", title: "Tier-3 via partners", col: C.green,
      rows: [
        ["Where", "Davanagere, Shivamogga, Udupi, Hassan, Solapur; Nashik & Sambhajinagar partner-led"],
        ["Who", "All three personas + societies retrofit at scale"],
        ["Sell", "Full catalogue + AquaLoop reuse module + O&M takeovers; WaaS pilot"],
        ["Route", "25 certified dealer-installers; association bulk programmes; account-based direct for ₹50 L+ deals"],
        ["Invest", "₹2.6 cr: dealer academy, monitoring fleet, working capital"],
        ["Target", "₹11.9 cr new revenue · recurring ~10% of sales · 34 installs/yr"],
      ],
    },
  ];
  phases.forEach((p, i) => {
    const x = PAGE.mL + i * (pw + gap);
    s.addShape("roundRect", { x, y: py, w: pw, h: ph, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.line, width: 0.75 } });
    s.addShape("roundRect", { x, y: py, w: pw, h: 0.42, rectRadius: 0.06, fill: { color: p.col }, line: { type: "none" } });
    s.addText([
      T(p.name + "   ", { bold: true, fontSize: 8.5, color: "D9E6EC" }),
      T(p.title, { bold: true, fontSize: 10.5, color: "FFFFFF" }),
    ], { x: x + 0.14, y: py, w: pw - 0.28, h: 0.42, isTextBox: true, margin: 0, fontFace: FONT, valign: "middle" });
    let ry = py + 0.50;
    const rh = [0.42, 0.28, 0.50, 0.50, 0.28, 0.40];
    p.rows.forEach((r, j) => {
      s.addText(r[0].toUpperCase(), { x: x + 0.14, y: ry, w: 0.62, h: rh[j], isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7, bold: true, color: p.col, valign: "top" });
      s.addText(r[1], { x: x + 0.80, y: ry, w: pw - 0.96, h: rh[j], isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.4, color: C.ink, valign: "top", lineSpacingMultiple: 0.98 });
      ry += rh[j] + 0.028;
    });
    if (i < 2) {
      s.addShape("chevron", { x: x + pw + 0.045, y: py + 1.22, w: 0.36, h: 0.55, fill: { color: C.amber }, line: { type: "none" } });
    }
  });
  // gate criteria strip
  const gy = py + ph + 0.08;
  const gates = [
    ["GATE 1 → 2", "≥10 lab-verified reference installs · AMC attach ≥50% · DSO ≤75 days · pipeline ≥3x next-year target"],
    ["GATE 2 → 3", "Channel-sourced ≥40% of qualified pipeline · install cycle ≤45 days · fleet uptime ≥95% · repeat/referral ≥20% of orders · gross margin ≥30%"],
  ];
  gates.forEach((g, i) => {
    const x = PAGE.mL + 1.9 + i * (pw + gap);
    s.addShape("roundRect", { x, y: gy, w: pw + 0.2, h: 0.48, rectRadius: 0.05, fill: { color: C.amberLt }, line: { color: C.amber, width: 1 } });
    s.addText([T(g[0] + "  ", { bold: true, color: "9A6A0F", fontSize: 7.8 }), T(g[1], { color: C.ink, fontSize: 7.3 })], {
      x: x + 0.10, y: gy, w: pw, h: 0.48, isTextBox: true, margin: 0, fontFace: FONT, valign: "middle", lineSpacingMultiple: 0.98,
    });
  });

  /* ---- Bottom left: funnel ---- */
  const fy2 = gy + 0.62;
  secLabel(s, "Acquisition funnel & capacity (FY27 → FY29)", PAGE.mL, fy2, 6.6, { size: 10.5 });
  const st = [["Audits / leads", "320 → 900"], ["Qualified", "130 → 380\n(₹32 → 95 cr)"], ["Proposals", "55 → 160"], ["Wins", "10 → 34"], ["New revenue", "₹2.4 → 11.9 cr"]];
  st.forEach(([a, b], i) => {
    const x = PAGE.mL + i * 1.40;
    if (i === 4) {
      s.addShape("roundRect", { x, y: fy2 + 0.26, w: 1.62, h: 0.74, rectRadius: 0.08, fill: { color: C.navy }, line: { type: "none" } });
      s.addText([T(a + "\n", { bold: true, fontSize: 7.3, color: "FFFFFF" }), T(b, { fontSize: 7.1, color: "FFD9A0" })], {
        x: x + 0.08, y: fy2 + 0.26, w: 1.46, h: 0.74, isTextBox: true, margin: 0, fontFace: FONT, valign: "middle", align: "center", lineSpacingMultiple: 0.96,
      });
    } else {
      s.addShape("chevron", { x, y: fy2 + 0.26, w: 1.34, h: 0.74, fill: { color: C.tealLt }, line: { color: C.teal, width: 0.75 } });
      s.addText([T(a + "\n", { bold: true, fontSize: 7.3, color: C.navy }), T(b, { fontSize: 7.1, color: C.ink })], {
        x: x + 0.14, y: fy2 + 0.26, w: 1.10, h: 0.74, isTextBox: true, margin: 0, fontFace: FONT, valign: "middle", align: "center", lineSpacingMultiple: 0.96,
      });
    }
  });
  s.addText("Cycle: hotels 2-4 mo · hospitals 3-6 mo · developers 6-9 mo. Capacity: 2 own crews FY27 → 3 own + 2 partner crews FY29 (~8 installs/crew/yr). KPIs: pipeline cover, proposal→win %, DSO, install cycle, AMC attach, uptime, repeat share.", {
    x: PAGE.mL, y: fy2 + 1.06, w: 7.15, h: 0.42, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.3, color: C.mut, lineSpacingMultiple: 1.0,
  });

  /* ---- Bottom right: revenue chart ---- */
  const chx = 8.0, chw = 4.78;
  secLabel(s, "Revenue build, ₹cr (base case)", chx, fy2, chw, { size: 10.5 });
  s.addChart("bar", [
    { name: "Existing base (5%/yr)", labels: ["FY26", "FY27", "FY28", "FY29"], values: [11.7, 12.3, 12.9, 13.5] },
    { name: "New private-market", labels: ["FY26", "FY27", "FY28", "FY29"], values: [0, 2.4, 6.4, 11.9] },
  ], {
    x: chx, y: fy2 + 0.22, w: chw, h: 1.26, barDir: "col", barGrouping: "stacked",
    chartColors: [C.navy, C.amber], showLegend: true, legendPos: "r", legendFontSize: 7.5, legendColor: C.ink, legendFontFace: FONT,
    showTitle: false, showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 7, dataLabelFontFace: FONT, dataLabelFormatCode: "0.#;;",
    catAxisLabelColor: C.ink, catAxisLabelFontSize: 8, catAxisLabelFontFace: FONT,
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMaxVal: 30,
    barGapWidthPct: 60,
  });

  soWhat(s, "Rule", "A new cluster opens only when the previous one passes its gate: service quality and cash discipline scale before geography.", 6.62, 0.40);
  footer(s, "Targets are team estimates from the p.4 model; cluster distances from Bicholim, Goa. Investment funded by internal accruals + IPO working capital (problem statement).", 5);
})();

/* ================= SLIDE 6: CORE 4 - RISKS ================= */
(function core4() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Deliverable 3 | Risk assessment and mitigation", "The binding constraints are cash and credibility, not demand: two red-zone risks get standing controls", { titleSize: 20, titleH: 0.62 });

  /* ---- Left: heatmap ---- */
  const hx = PAGE.mL + 0.22, hy = y0 + 0.30, cwd = 0.76, chd = 0.70;
  secLabel(s, "Likelihood x impact heatmap", PAGE.mL, y0 + 0.02, 4.2, { size: 11 });
  // cells
  for (let li = 1; li <= 5; li++) {
    for (let im = 1; im <= 5; im++) {
      const sev = li + im;
      const col = sev >= 8 ? C.redLt : sev >= 6 ? C.yellowLt : C.greenLt;
      s.addShape("rect", { x: hx + (li - 1) * cwd, y: hy + (5 - im) * chd, w: cwd, h: chd, fill: { color: col }, line: { color: "FFFFFF", width: 1.5 } });
    }
  }
  // scale ticks
  for (let i = 1; i <= 5; i++) {
    s.addText(String(i), { x: hx + (i - 1) * cwd, y: hy + 5 * chd + 0.02, w: cwd, h: 0.18, isTextBox: true, margin: 0, align: "center", fontFace: FONT, fontSize: 7, color: C.faint });
    s.addText(String(i), { x: hx - 0.20, y: hy + (5 - i) * chd + chd / 2 - 0.09, w: 0.16, h: 0.18, isTextBox: true, margin: 0, align: "center", fontFace: FONT, fontSize: 7, color: C.faint });
  }
  // risk dots: [code, likelihood, impact, dxOffset]
  const R = [
    ["R1", 4, 5, 0], ["R2", 4, 3, 0], ["R3", 3, 4, -0.19], ["R4", 3, 3, 0],
    ["R5", 3, 4, 0.19], ["R6", 2, 4, 0], ["R7", 3, 2, 0], ["R8", 2, 5, 0],
  ];
  R.forEach(([code, li, im, dxo]) => {
    const px = hx + (li - 1) * cwd + cwd / 2 - 0.16 + dxo;
    const pyy = hy + (5 - im) * chd + chd / 2 - 0.16;
    const hot = li + im >= 8;
    s.addShape("ellipse", { x: px, y: pyy, w: 0.32, h: 0.32, fill: { color: hot ? C.red : C.navy }, line: { color: "FFFFFF", width: 1 } });
    s.addText(code, { x: px - 0.05, y: pyy + 0.025, w: 0.42, h: 0.26, isTextBox: true, margin: 0, align: "center", fontFace: FONT, fontSize: 7.5, bold: true, color: "FFFFFF" });
  });
  s.addText("Likelihood →", { x: hx, y: hy + 5 * chd + 0.22, w: 5 * cwd, h: 0.2, isTextBox: true, margin: 0, align: "center", fontFace: FONT, fontSize: 7.5, color: C.mut });
  s.addText("Impact →", { x: hx - 1.52, y: hy + 2.5 * chd - 0.1, w: 2.4, h: 0.2, isTextBox: true, margin: 0, rotate: 270, align: "center", fontFace: FONT, fontSize: 7.5, color: C.mut });
  s.addText([
    T("R1 ", { bold: true }), T("Developer receivables (Fin) · "), T("R2 ", { bold: true }), T("Price war (Comp) · "),
    T("R3 ", { bold: true }), T("Commissioning & inoculum variability (Ops) · "), T("R4 ", { bold: true }), T("Partner conflict (Distr.) · "),
    T("R5 ", { bold: true }), T("Expansion outruns service (Ops) · "), T("R6 ", { bold: true }), T("Norm tightening (Reg.) · "),
    T("R7 ", { bold: true }), T("Long cycles stall cash (Fin) · "), T("R8 ", { bold: true }), T("Marquee-site failure (Reputation). "),
    T("Red dots = red-zone (likelihood + impact ≥ 8).", { color: C.mut }),
  ], { x: PAGE.mL, y: hy + 5 * chd + 0.50, w: 4.0, h: 1.05, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.8, color: C.ink, lineSpacingMultiple: 1.14 });

  /* ---- Right: mitigation table ---- */
  const tx = 4.85, tw2 = 7.93;
  secLabel(s, "Mitigation plan for the six material risks", tx, y0 + 0.02, tw2, { size: 11 });
  const M = (t, o = {}) => cell(t, Object.assign({ fontSize: 7.8 }, o));
  const MH2 = (t) => cell(t, { bold: true, color: "FFFFFF", fill: { color: C.navy }, fontSize: 8.1, valign: "middle" });
  const mit = [
    [MH2("Risk (cat.)"), MH2("Root cause & impact"), MH2("Early warning"), MH2("Preventive control"), MH2("Contingency"), MH2("Owner")],
    [M("R1 Developer receivables (Financial)", { bold: true, color: C.red }), M("Milestone slippage, RERA escrow timing; ₹2-3 cr locked, growth stalls"), M("DSO >75; billing-collection gap >2 mo"), M("30-40-25-5 milestone billing with advance; credit check + PDCs; developer cap 25% of book"), M("Stop-work clause; invoice discounting"), M("CFO")],
    [M("R2 Price-led rivalry (Competitive)", { bold: true }), M("SUSBIO from ₹35k/KLD; Daiki KA plant; NCR online bidders; margin erosion"), M("Win rate <25%; avg discount >8%"), M("Lifecycle-cost selling; compliance + AMC bundle; walk-away floor at 28% GM"), M("Value-engineered Lite SKU for price deals"), M("Sales head")],
    [M("R3 Commissioning & inoculum variation (Operational)", { bold: true }), M("Site variability; biology stabilises over 4-8 weeks; norm breach at handover"), M(">2 sites off-norm at day-30 test"), M("Factory acceptance test; inoculum batch QC; 30/60/90-day third-party NABL tests"), M("Rapid-response protocol; ozone-assist retrofit"), M("Technical head")],
    [M("R4 Partner conflict / underperformance (Distribution)", { bold: true }), M("Overlapping territories, poaching; channel stalls"), M("Partner pipeline <30% of plan; duplicate lead claims"), M("≤2 partners per territory; registered-lead lock; installer academy; tiered margins"), M("Territory reassignment; direct coverage"), M("Channel manager")],
    [M("R5 Expansion outruns service (Operational)", { bold: true, color: C.red }), M("Install base grows faster than technicians; SLA breach, churn"), M("Response >48h; uptime <95%"), M("KPI gates before new clusters; hub per ~150 km; 1 technician : 25 AMC sites"), M("Freeze new clusters; contract service partners"), M("COO")],
    [M("R6 Discharge norms tighten (Regulatory, added category)", { bold: true }), M("NGT / CPCB revisions strand installed designs"), M("Draft notifications; consent-renewal queries"), M("Design margin to stricter norms; IISc tertiary pipeline"), M("Paid retrofit-upgrade programme (upside)"), M("MD + Tech")],
  ];
  s.addTable(mit, {
    x: tx, y: y0 + 0.30, w: tw2,
    colW: [1.32, 1.72, 1.10, 1.90, 1.14, 0.75],
    autoPage: false,
  });

  soWhat(s, "Control", "Milestone billing, exposure caps and gated expansion keep the plan self-funding; R7 and R8 stay on watch metrics.", 6.56, 0.44);
  footer(s, "Likelihood/impact: team scoring from competitor research (susbio.in; biltraxmedia.com on Daiki), CPCB 2021 utilisation gap, and SME receivable norms. Impact scale: 5 = >₹2 cr or franchise damage.", 6);
})();

/* ================= SLIDE 7: CORE 5 - PORTFOLIO ================= */
(function core5() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Deliverable 4 | Portfolio expansion: adjacent products and technologies", "Extend the installed base: rescue and run plants first, monitor them second, recycle their water third", { titleSize: 20, titleH: 0.62 });

  /* ---- Left: weighted scores bar chart ---- */
  const bx = PAGE.mL, bw = 5.0;
  secLabel(s, "Weighted adjacency scores (7 criteria, 100 pts)", bx, y0 + 0.02, bw, { size: 11 });
  const adjLabels = ["Biogas & nutrient recovery", "Sludge / faecal-sludge svcs", "Water-as-a-service (BOOT)", "Constructed wetlands / DEWATS", "MBR premium line", "Advanced disinfection", "Greywater recycling", "Water-reuse module (tertiary)", "IoT monitoring & dashboards", "STP retrofit + O&M takeover"];
  s.addChart("bar", [
    { name: "Evaluated", labels: adjLabels, values: [2.30, 3.00, 3.05, 3.20, 3.20, 3.55, 3.55, null, null, null] },
    { name: "Selected", labels: adjLabels, values: [null, null, null, null, null, null, null, 4.30, 4.55, 4.65] },
  ], {
    x: bx, y: y0 + 0.30, w: bw, h: 3.55, barDir: "bar", barGrouping: "stacked",
    chartColors: [C.aqua, C.amber], showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 7.5, dataLabelFontFace: FONT, dataLabelFormatCode: "0.00;;",
    catAxisLabelColor: C.ink, catAxisLabelFontSize: 7.6, catAxisLabelFontFace: FONT,
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMaxVal: 5.4,
    barGapWidthPct: 38,
  });
  s.addText([
    T("Criteria (weights): ", { bold: true, color: C.navy, fontSize: 7.8 }),
    T("market demand 20 · synergy & technical feasibility 20 · capital required 15 (inverse) · margin 15 · operational complexity 10 (inverse) · time-to-market 10 · recurring potential 10. Scores 1-5; matrix in backup (p.9).", { color: C.mut, fontSize: 7.8 }),
  ], { x: bx, y: y0 + 3.92, w: bw, h: 0.68, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.05 });

  /* ---- Right: three selected cards ---- */
  const cx = 5.95, cw2 = 6.83;
  secLabel(s, "The chosen three: sequenced, not simultaneous", cx, y0 + 0.02, cw2, { size: 11 });
  const cards = [
    {
      chip: "NOW (M0-3) · BUILD IN-HOUSE", name: "STP Rescue: retrofit + O&M takeover", col: C.teal,
      body: "Why: CPCB 2021 shows a third of installed capacity idle or off-norm, so demand is certain and capex is zero. Target: hotels & societies with failing third-party STPs. Price: ₹3-15 L retrofit + ₹0.5-3 L/yr O&M. Pilot: 10 audits at Goa hotels. Metric: 25 retrofits + 40 O&M contracts by FY29 at ~35% GM; seeds the AMC fleet.",
    },
    {
      chip: "M6 · WHITE-LABEL + OWN DASHBOARD", name: "SmartSTP: IoT monitoring & compliance reports", col: C.navy2,
      body: "Why: consent renewals increasingly demand data; differentiates every EPBL AMC. Mode: distribute white-label sensors, own the dashboard. Invest ₹50-70 L. Price: ₹10-15k install + ₹3-5k/month per site. Pilot: 20 AMC sites in Goa. Metric: 150 connected sites by FY29, churn <10%.",
    },
    {
      chip: "M9-12 · DEVELOP WITH IISc", name: "AquaLoop: treated-water reuse module", col: C.green,
      body: "Why: hotels pay tanker rates for water CGWA already tells them to recycle; builds directly on the ozone oxy-STP line and Feb-2026 IISc MoU (non-biological treatment). Mode: develop + assemble at Bicholim; ₹1-1.5 cr. Price: ₹6-18 L add-on skid (UF + carbon + UV/O3). Pilot: 2 Goa resorts + 1 Kolhapur society. Metric: attached to 25% of new STP orders by FY29.",
    },
  ];
  let cy = y0 + 0.30;
  const chs = [1.24, 1.06, 1.30];
  cards.forEach((c2, i) => {
    s.addShape("roundRect", { x: cx, y: cy, w: cw2, h: chs[i], rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.line, width: 0.75 } });
    s.addText([
      T(c2.name + "   ", { bold: true, fontSize: 10, color: c2.col }),
      T(c2.chip, { bold: true, fontSize: 7, color: "9A6A0F" }),
    ], { x: cx + 0.14, y: cy + 0.05, w: cw2 - 0.28, h: 0.24, isTextBox: true, margin: 0, fontFace: FONT });
    s.addText(c2.body, { x: cx + 0.14, y: cy + 0.30, w: cw2 - 0.28, h: chs[i] - 0.36, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 7.9, color: C.ink, lineSpacingMultiple: 1.0, valign: "top" });
    cy += chs[i] + 0.14;
  });
  s.addText([
    T("Deferred: ", { bold: true, color: C.navy, fontSize: 8 }),
    T("WaaS/BOOT piloted only in FY29 via partner financing (capital-heavy); MBR premium line, FSTP and biogas dropped for now: capex, municipal dependence, or sub-scale economics. Combined contribution of the three: ~₹2.4 cr/yr recurring by FY29 at 35-40% GM, cross-sold to the installed base.", { color: C.ink, fontSize: 8 }),
  ], { x: cx, y: cy + 0.06, w: cw2, h: 0.80, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.06 });

  soWhat(s, "Sequence", "Each adjacency deepens the same installed base and lifts recurring revenue to ~10% of sales by FY29; none needs new manufacturing beyond Bicholim.", 6.50);
  footer(s, "Sources: CPCB 2021 (operational 26,869 vs installed 31,841 MLD; 20,235 MLD utilised); CGWA 2020 recycled-water mandate; IISc MoU (ANI, Feb 2026); Boson Whitewater WaaS benchmark (Zerodha Rainmatter). Scores: team analysis, matrix p.9.", 7);
})();

/* ================= SLIDE 8: REFERENCES & METHODOLOGY ================= */
(function refs() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Supporting material", "References and methodology", { titleSize: 20, titleH: 0.5 });

  const G = (t) => T(t + "\n", { bold: true, color: C.teal, fontSize: 8.8 });
  const I = (t) => T(t + "\n", { color: C.ink, fontSize: 7.3 });
  const colL = [
    G("CASE"),
    I("BGCC Case Consilium 2026 Round 2, EP Biocomposites Ltd problem statement, BITS Pilani Goa (all slides). Company FY26 financials, price ranges, IISc MoU and Unkal Nullah reference are cited from this document."),
    G("EPBL & GROUP"),
    I("EPBL website, product pages: epbiocomposites.com/bio-digester-toilet-manufacturer-in-goa/; /sewage-and-effluent-treatment-plant-manufacturer-in-goa/ (acc. Sep 2026), slides 3-5"),
    I("EPBL IPO details & pre-IPO financials: chittorgarh.com/ipo/ep-biocomposites-ipo/1286/ (2022), slides 2,5"),
    I("ONGC 100-KLD MBR STP order ₹72.27 L: equitybulls.com/category.php?id=340437 (Dec 2023), slides 3,4"),
    I("IISc Bengaluru MoU: aninews.in/news/business/ep-biocomposites-strengthens-technology-capabilities... (Feb 2026), slides 2,7"),
    I("EPBL incorporation, Bicholim: zaubacorp.com/EP-BIOCOMPOSITES-LIMITED-U28900GA2020PLC014240, slide 5"),
    G("GOVERNMENT & REGULATORY"),
    I("CPCB, National Inventory of Sewage Treatment Plants, Mar 2021: cpcb.gov.in (report id 1228); state gap for Goa via navhindtimes.in (Oct 2021), slides 2,4,6,7"),
    I("Bio-medical Waste Management Rules 2016 (amended 2018), >10-bed ETP mandate: cpcb.gov.in / MoEFCC gazette, slides 3,4"),
    I("Karnataka apartment STP rules & 2024 revision: deccanherald.com/india/karnataka/karnataka-government-relaxes-rules-stp-not-must-for-apartments-with-less-than-120-units-2933606 (2024), slides 3,4"),
    I("EIA Notification 2006 item 8(a) ≥20,000 sqm: lexology.com/library/detail.aspx?g=8b0e2b16 (2025 review), slides 3,4"),
    I("NGT OA 593/2017 order 28.08.2019 (100% treatment): greentribunal.gov.in, slide 4"),
    I("CGWA groundwater guidelines, 24 Sep 2020 (recycled-water mandate): cgwa-noc.gov.in via thesustainabilitycloud.com/blog/cgwa-guidelines/, slides 4,7"),
    I("CSR: ₹34,908.75 cr FY24 total; health & sanitation ~₹8,739 cr: csr.gov.in via indiacsr.in (2024) and proteantech.in, slide 4"),
    I("Census of India 2011: urban households on septic tanks 38.2%: censusindia.gov.in (HL-08 analysis), slide 4"),
  ];
  const colR = [
    G("MARKET & DEMAND"),
    I("Goa tourist arrivals 2024 (10.41 mn): goa-tourism.com/news/goa-records-robust-21-percent-growth-in-tourism..., slides 3,4"),
    I("Goa registered accommodation ~9,000 units (2024): Goa DoT via traveltrendstoday.in, slides 4,9"),
    I("HVS ANAROCK India Hospitality Overview 2024 (Tier-2 28% + Tier-3/4 46% of new room signings): hvs.com/article/10158, slides 4,9"),
    I("MahaRERA 50,162 registered projects: constructionworld.in (2025), slides 4,9"),
    I("K-RERA ~5,672 & Goa RERA ~1,250 projects (portal counts, secondary): 99acres.com/rera-registered-projects-in-karnataka-ffid; ...-in-goa-ffid, slides 4,9"),
    I("India wastewater treatment market USD 10.4 bn 2025: imarcgroup.com/india-wastewater-treatment-market; plants market USD 1.33 bn 2024: techsciresearch.com (report 4514), slide 4"),
    G("COMPETITORS & PRICING"),
    I("Daiki Axis India (Johkasou; Tumakuru plant ₹200 cr): daikiaxis.in; biltraxmedia.com/daiki-axis-to-invest-200-inr-crore..., slides 4,6"),
    I("Ion Exchange INDION packaged STPs: ionexchangeglobal.com; Thermax FabX/BioCask: thermaxglobal.com, slide 4"),
    I("Banka BioLoo financials: screener.in/company/BANKA/consolidated/, slide 4"),
    I("SUSBIO ECOTREAT, from ₹35k/KLD: susbio.in; susbio.in/stp-plant-cost-per-kld-in-india-2026/, slides 4,6"),
    I("Netsol Water / Kelvin (NCR): netsolwater.com/service-locations.php; kelvinindia.in, slide 4"),
    I("CDD Society DEWATS: cddindia.org; Boson Whitewater WaaS: zerodha.com/z-connect/rainmatter/introducing-boson-whitewater, slides 4,7"),
    I("Packaged-STP & AMC price benchmarks: studiomatrx.org/guides/stp-cost-per-kld-india; teamonebiotech.com (O&M costs 2026), slides 3,4,9"),
    I("DRDO bio-digester ToT licensees (49 firms, 2012): indiatvnews.com/news/india/drdo-licensing-eco-toilets-private-companies-16612.html, slide 4"),
    I("All URLs accessed 10 Sep 2026. Secondary sources are marked; where a figure exists only in the problem statement, the deck cites the problem statement."),
  ];
  s.addText(colL, { x: PAGE.mL, y: y0, w: 5.95, h: 5.9, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.12, valign: "top" });
  s.addText(colR, { x: 6.7, y: y0, w: 4.35, h: 5.9, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.12, valign: "top" });

  // Methodology panel
  const mx2 = 11.2, mw2 = 1.58;
  s.addShape("roundRect", { x: mx2, y: y0, w: mw2, h: 5.9, rectRadius: 0.06, fill: { color: C.tealLt }, line: { type: "none" } });
  s.addText([
    T("METHODOLOGY\n", { bold: true, color: C.teal, fontSize: 8.5 }),
    T("\nSizing: bottom-up per segment per state: units x %lacking x fit x conversion x ticket. No top-down market-report allocation.\n", { color: C.ink, fontSize: 7 }),
    T("\nScenarios: conversion, trigger-share and win-rate flexed; conservative = lowest defensible, upside = still capacity-bound.\n", { color: C.ink, fontSize: 7 }),
    T("\nScoring: segmentation 10 factors / portfolio 7 criteria, weights shown on slides 3 and 7; scores 1-5, evidence-based.\n", { color: C.ink, fontSize: 7 }),
    T("\nRounding: ₹cr to 1 decimal; estimates labelled; no false precision.", { color: C.ink, fontSize: 7 }),
  ], { x: mx2 + 0.1, y: y0 + 0.08, w: mw2 - 0.2, h: 5.7, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.05, valign: "top" });

  footer(s, "", 8);
})();

/* ================= SLIDE 9: GLOSSARY & MODEL BACKUP ================= */
(function backup() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  const y0 = header(s, "Supporting material", "Glossary, assumptions and calculation backup", { titleSize: 20, titleH: 0.5 });

  // Glossary
  secLabel(s, "Glossary", PAGE.mL, y0, 3.4, { size: 11 });
  const gl = [
    ["STP / ETP", "Sewage / Effluent Treatment Plant"],
    ["KLD / MLD", "Kilo / Million Litres per Day"],
    ["MBBR", "Moving Bed Biofilm Reactor"],
    ["SBR", "Sequencing Batch Reactor"],
    ["MBR", "Membrane Bioreactor"],
    ["DEWATS", "Decentralised Wastewater Treatment Systems (nature-based)"],
    ["FRP", "Fibre-Reinforced Plastic"],
    ["O&M / AMC", "Operation & Maintenance / Annual Maintenance Contract"],
    ["TAM/SAM/SOM", "Total / Serviceable Addressable / Obtainable Market"],
    ["DSO", "Days Sales Outstanding (receivable days)"],
    ["ToT", "Transfer of Technology (DRDO licence)"],
    ["EC / OC", "Environmental Clearance / Occupancy Certificate"],
    ["CTE / CTO", "Consent to Establish / Operate (pollution boards)"],
    ["BMW Rules", "Bio-medical Waste Management Rules, 2016"],
    ["CGWA", "Central Ground Water Authority"],
    ["WaaS / BOOT", "Water-as-a-Service / Build-Own-Operate-Transfer"],
  ];
  const glRows = gl.map(([a, b]) => [
    cell(a, { bold: true, color: C.navy, fontSize: 7.2, fill: { color: C.panel } }),
    cell(b, { fontSize: 7.2 }),
  ]);
  s.addTable(glRows, { x: PAGE.mL, y: y0 + 0.26, w: 3.55, colW: [1.05, 2.50], autoPage: false });

  // TAM assumptions table
  const ax = 4.35, aw = 8.43;
  secLabel(s, "TAM build (annual, ₹cr): eligible units x %lacking x fit x conversion x avg ticket", ax, y0, aw, { size: 11 });
  const A = (t, o = {}) => cell(t, Object.assign({ fontSize: 6.9, align: "center", valign: "middle" }, o));
  const AH = (t) => cell(t, { bold: true, color: "FFFFFF", fill: { color: C.navy }, fontSize: 7.1, align: "center", valign: "middle" });
  const tam = [
    [AH("Segment"), AH("Eligible units (basis)"), AH("% lack"), AH("Fit"), AH("Conv./yr"), AH("Ticket ₹L"), AH("Proj./yr"), AH("₹cr/yr")],
    [A("Hospitality (≥20 keys)", { align: "left" }), A("4,000 stock (Goa DoT ~9,000 units; HVS Tier-2/3) + 110 new/yr", { align: "left" }), A("55%"), A("60%"), A("8% + new"), A("24-28"), A("166"), A("42.3")],
    [A("Residential developers", { align: "left" }), A("517 STP-trigger launches/yr (RERA run-rates x Tier-2/3 x trigger share)", { align: "left" }), A("n/a"), A("60%"), A("flow"), A("48"), A("310"), A("148.9")],
    [A("Housing societies (retrofit)", { align: "left" }), A("900 with failing/aged STPs", { align: "left" }), A("100%"), A("60%"), A("12%"), A("14"), A("65"), A("9.1")],
    [A("Hospitals >10 beds", { align: "left" }), A("5,500 private HCFs (BMW Rules base)", { align: "left" }), A("50%"), A("50%"), A("6%"), A("16"), A("82"), A("13.2")],
    [A("Education & CSR campuses", { align: "left" }), A("3,000 residential campuses", { align: "left" }), A("55%"), A("45%"), A("5%"), A("14"), A("37"), A("5.2")],
    [A("MSME industrial (compact ETP)", { align: "left" }), A("2,600 consented units, simple effluents", { align: "left" }), A("45%"), A("40%"), A("7%"), A("40"), A("33"), A("13.1")],
    [A("Commercial & mixed-use", { align: "left" }), A("1,200 properties", { align: "left" }), A("50%"), A("50%"), A("7%"), A("35"), A("21"), A("7.4")],
    [A("Homes (bio-digester)", { align: "left" }), A("220,000 new unsewered Tier-2/3 homes/yr", { align: "left" }), A("n/a"), A("2.5% adopt"), A("flow"), A("0.55"), A("5,500"), A("30.3")],
    [A("Homestays & small hospitality", { align: "left" }), A("3,500 stock", { align: "left" }), A("60%"), A("50%"), A("8%"), A("2.2"), A("84"), A("1.8")],
    [A("TOTAL TAM", { bold: true, align: "left", fill: { color: C.amberLt } }), A("", { fill: { color: C.amberLt } }), A("", { fill: { color: C.amberLt } }), A("", { fill: { color: C.amberLt } }), A("", { fill: { color: C.amberLt } }), A("", { fill: { color: C.amberLt } }), A("~6,300", { bold: true, fill: { color: C.amberLt } }), A("271.2", { bold: true, fill: { color: C.amberLt } })],
  ];
  s.addTable(tam, {
    x: ax, y: y0 + 0.26, w: aw,
    colW: [1.55, 2.80, 0.62, 0.62, 0.72, 0.72, 0.65, 0.75],
    autoPage: false,
  });

  // SOM bridge + scoring backup
  const by2 = y0 + 3.30;
  secLabel(s, "SOM bridge, base case (₹cr)", ax, by2, 4.0, { size: 10.5 });
  const som = [
    [AH("₹cr"), AH("FY27"), AH("FY28"), AH("FY29")],
    [A("Existing base (+5%/yr)", { align: "left" }), A("12.3"), A("12.9"), A("13.5")],
    [A("New private-market", { align: "left" }), A("2.4"), A("6.4"), A("11.9")],
    [A("Total revenue", { align: "left", bold: true }), A("14.7", { bold: true }), A("19.3", { bold: true }), A("25.4", { bold: true })],
  ];
  s.addTable(som, { x: ax, y: by2 + 0.24, w: 3.6, colW: [1.65, 0.65, 0.65, 0.65], autoPage: false });

  s.addText([
    T("FY29 new-business mix: ", { bold: true, color: C.navy, fontSize: 7.5 }),
    T("26 STP/ETP projects (avg ₹32 L) ₹8.3 cr + 8 retrofits ₹1.0 cr + ~230 bio-digesters ₹1.8 cr + AMC/monitoring/O&M ₹0.8 cr = ₹11.9 cr. ", { color: C.ink, fontSize: 7.5 }),
    T("Working capital: ", { bold: true, color: C.navy, fontSize: 7.5 }),
    T("receivables at 75 DSO = ₹5.2 cr against net worth >₹12 cr plus IPO working capital; ₹6.2 cr phase investment from internal accruals. ", { color: C.ink, fontSize: 7.5 }),
    T("Segment scores (wtd): ", { bold: true, color: C.navy, fontSize: 7.5 }),
    T("hoteliers 4.50, developers 3.80, hospitals 3.75, homeowners 3.45, societies 3.20, MSME 3.20, schools & CSR 3.05, commercial 3.05.", { color: C.ink, fontSize: 7.5 }),
  ], { x: 8.15, y: by2 + 0.24, w: 4.63, h: 1.05, isTextBox: true, margin: 0, fontFace: FONT, lineSpacingMultiple: 1.06, valign: "top" });

  // Adjacency scoring detail (top 5 of 10)
  const my3 = by2 + 1.16;
  secLabel(s, "Adjacency scoring, top 5 of 10 options (capital & complexity scored inverse: 5 = low)", ax, my3, 8.4, { size: 10.5 });
  const J = (t, o = {}) => cell(t, Object.assign({ fontSize: 6.7, align: "center", valign: "middle" }, o));
  const JH = (t) => cell(t, { bold: true, color: "FFFFFF", fill: { color: C.navy }, fontSize: 6.8, align: "center", valign: "middle" });
  const adj = [
    [JH("Option"), JH("Dem 20"), JH("Syn 20"), JH("Cap 15"), JH("Mar 15"), JH("Op 10"), JH("TTM 10"), JH("Rec 10"), JH("Wtd")],
    [J("STP retrofit + O&M takeover", { align: "left" }), J("5"), J("5"), J("5"), J("4"), J("3"), J("5"), J("5"), J("4.65", { bold: true, fill: { color: C.amberLt } })],
    [J("IoT monitoring & dashboards", { align: "left" }), J("4"), J("5"), J("5"), J("4"), J("4"), J("5"), J("5"), J("4.55", { bold: true, fill: { color: C.amberLt } })],
    [J("Water-reuse module (tertiary)", { align: "left" }), J("5"), J("5"), J("4"), J("4"), J("3"), J("4"), J("4"), J("4.30", { bold: true, fill: { color: C.amberLt } })],
    [J("Greywater recycling", { align: "left" }), J("3"), J("4"), J("4"), J("3"), J("4"), J("4"), J("3"), J("3.55")],
    [J("Advanced disinfection", { align: "left" }), J("3"), J("4"), J("4"), J("3"), J("4"), J("4"), J("3"), J("3.55")],
  ];
  s.addTable(adj, { x: ax, y: my3 + 0.26, w: 6.7, colW: [1.90, 0.60, 0.60, 0.60, 0.60, 0.55, 0.55, 0.55, 0.75], autoPage: false });

  footer(s, "All FY27-29 figures are team estimates; stock counts marked 'est.' are transparent proxies built from the sources on p.8 (RERA portals, Goa DoT, HVS-ANAROCK, BMW Rules registers).", 9);
})();

pres.writeFile({ fileName: "CaseConsilium_Wookies.pptx" }).then(() => console.log("deck written"));
