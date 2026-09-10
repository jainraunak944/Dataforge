// CaseConsilium_Wookies v2 — reference-matched infographic style
const pptxgen = require("pptxgenjs");
const { buildIcons } = require("./icons");
const { C, PAGE, F, card, chip, header2, sec2, statCard, ribbon, footer2, shadow, shadowSm } = require("./theme2");

const T = (t, o = {}) => ({ text: t, options: o });
const HB = "#"; // hex helper for icon colors only (icons take #-hex; pptx colors never do)

const ICON_SPECS = {};
function I(name, hex6) { const k = name + "_" + hex6; ICON_SPECS[k] = [name, "#" + hex6]; return k; }
// pre-register variants
const b = h => h; // no-op clarity
const BR = "1568DC", WH = "FFFFFF", GN = "129454", AM = "ED9B12", RD = "D64226", GY = "55616D", DK = "0C3E86";
const IC = {};
[
  ["target", BR], ["target", WH], ["hotel", BR], ["building", BR], ["hospital", BR], ["home", BR], ["school", BR],
  ["industry", BR], ["users", BR], ["rupee", BR], ["rupee", DK], ["chart", BR], ["chartline", BR], ["chartline", WH],
  ["funnel", BR], ["shield", BR], ["shield", WH], ["alert", RD], ["alert", BR], ["gear", BR], ["handshake", BR],
  ["pin", BR], ["pin", GN], ["wrench", BR], ["wifi", BR], ["recycle", BR], ["recycle", WH], ["recycle", GN],
  ["flask", BR], ["calendar", BR], ["certificate", BR], ["briefcase", BR], ["drop", BR], ["drop", WH], ["leaf", GN],
  ["search", BR], ["bolt", BR], ["bolt", AM], ["doc", BR], ["check", GN], ["check", WH], ["clock", BR], ["eye", BR],
  ["route", BR], ["bulb", BR], ["bulb", WH], ["flag", BR], ["flag", WH], ["flag", AM], ["tag", BR], ["network", BR],
  ["sensors", BR], ["trend", BR], ["trend", GN], ["verified", BR], ["water", BR], ["apartment", BR], ["factory", BR],
  ["gavel", RD], ["star", AM], ["monitor", BR], ["users", GY], ["gear", GY], ["clock", GY],
].forEach(([n, h]) => { IC[n + "_" + h] = 1; ICON_SPECS[n + "_" + h] = [n, "#" + h]; });

// ---- table cell helpers (v2 style) ----
function cell(text, opts = {}) {
  return {
    text,
    options: Object.assign({
      fontFace: F, fontSize: 7.4, color: C.ink, valign: "top", align: "left",
      border: [{ type: "solid", color: C.line, pt: 0.5 }, { type: "solid", color: C.line, pt: 0.5 },
               { type: "solid", color: C.line, pt: 0.5 }, { type: "solid", color: C.line, pt: 0.5 }],
      margin: [0.035, 0.05, 0.035, 0.05],
    }, opts),
  };
}
const hcell = (t, o = {}) => cell(t, Object.assign({ bold: true, color: "FFFFFF", fill: { color: C.brand }, valign: "middle" }, o));

async function main() {
  const ICONS = await buildIcons(ICON_SPECS);
  const K = (n, h) => ICONS[n + "_" + h]; // direct data access
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.author = "Team Wookies";
  pres.title = "Case Consilium 2026 - EP Biocomposites Limited";

  /* ============ S1 COVER ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    // diagonal collage right
    s.addShape("rect", { x: 9.4, y: -1.6, w: 7.2, h: 5.4, rotate: 24, fill: { color: C.tint }, line: { type: "none" } });
    s.addShape("rect", { x: 10.6, y: 2.6, w: 6.4, h: 4.6, rotate: 24, fill: { color: C.brand }, line: { type: "none" } });
    s.addShape("rect", { x: 8.55, y: 5.6, w: 3.4, h: 2.6, rotate: 24, fill: { color: C.greenT }, line: { type: "none" } });
    s.addShape("ellipse", { x: 8.9, y: 0.62, w: 0.16, h: 0.16, fill: { color: C.amber }, line: { type: "none" } });
    s.addImage({ data: K("drop", WH), x: 11.55, y: 4.35, w: 0.85, h: 0.85, transparency: 18 });
    // floating KPI mini-cards on the diagonal
    const mini = [
      [9.0, 1.05, "chart_" + BR, "₹270 cr/yr", "of private demand across 3 states"],
      [9.95, 2.45, "target_" + BR, "3 buyers", "hotels, developers, hospitals"],
      [8.6, 3.85, "trend_" + GN, "₹25.4 cr", "revenue we target by FY29"],
    ];
    mini.forEach(([x, y, ic, big, sub]) => {
      card(s, x, y, 2.5, 0.92, {});
      s.addImage({ data: ICONS[ic], x: x + 0.16, y: y + 0.26, w: 0.4, h: 0.4 });
      s.addText(big, { x: x + 0.68, y: y + 0.12, w: 1.75, h: 0.36, isTextBox: true, margin: 0, fontFace: F, fontSize: 16.5, bold: true, color: C.brandDk });
      s.addText(sub, { x: x + 0.68, y: y + 0.48, w: 1.78, h: 0.36, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.8, color: C.gray, lineSpacingMultiple: 1.0 });
    });
    // brand block
    chip(s, ICONS, "drop_" + BR, 0.55, 0.5, 0.5);
    s.addText("EP BIOCOMPOSITES LTD", { x: 1.18, y: 0.5, w: 5.5, h: 0.32, isTextBox: true, margin: 0, fontFace: F, fontSize: 16, bold: true, color: C.ink });
    s.addText("EP Kamat Group  ·  BSE SME listed  ·  Bicholim, Goa", { x: 1.18, y: 0.82, w: 5.5, h: 0.22, isTextBox: true, margin: 0, fontFace: F, fontSize: 9, color: C.gray });
    s.addShape("roundRect", { x: 0.55, y: 1.32, w: 3.1, h: 0.34, rectRadius: 0.17, fill: { color: C.tint }, line: { type: "none" } });
    s.addText("CASE CONSILIUM 2026  ·  ROUND 2", { x: 0.55, y: 1.32, w: 3.1, h: 0.34, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 8.5, bold: true, color: C.brand, charSpacing: 1.2 });
    // title
    s.addText([
      T("How EPBL wins the\n", { color: C.ink }),
      T("private wastewater market", { color: C.brand }),
    ], { x: 0.55, y: 2.30, w: 8.3, h: 1.6, isTextBox: true, margin: 0, fontFace: F, fontSize: 34, bold: true, lineSpacingMultiple: 1.04 });
    s.addShape("roundRect", { x: 0.58, y: 3.98, w: 1.1, h: 0.07, rectRadius: 0.03, fill: { color: C.brand }, line: { type: "none" } });
    s.addText("Sell to the three buyers who are forced to treat their wastewater, start close to home, and let service income compound. That takes EPBL from ₹11.7 crore today to about ₹25 crore by FY29.", {
      x: 0.55, y: 4.22, w: 7.6, h: 0.85, isTextBox: true, margin: 0, fontFace: F, fontSize: 13, bold: true, color: C.ink, lineSpacingMultiple: 1.12,
    });
    // team
    s.addText("TEAM WOOKIES", { x: 0.55, y: 5.45, w: 4, h: 0.3, isTextBox: true, margin: 0, fontFace: F, fontSize: 13, bold: true, color: C.brand, charSpacing: 2.5 });
    const members = ["Raunak Jain", "Dhruv Mundra", "Khushi Jha", "Sambhav Khandelwal"];
    members.forEach((m, i) => {
      const x = 0.55 + i * 1.98;
      s.addShape("roundRect", { x, y: 5.85, w: 1.86, h: 0.4, rectRadius: 0.2, fill: { color: C.tint2 }, line: { color: C.line, width: 0.75 } });
      s.addImage({ data: K("users", BR), x: x + 0.12, y: y0m(5.85, 0.4, 0.2), w: 0.2, h: 0.2 });
      s.addText(m, { x: x + 0.38, y: 5.85, w: 1.45, h: 0.4, isTextBox: true, margin: 0, fontFace: F, fontSize: 9.5, bold: true, color: C.ink, valign: "middle" });
    });
    s.addText("Bio-digester toilets  ·  decentralised STP / ETP  ·  wastewater reuse   |   private-pay Tier 2/3 markets of Goa, Maharashtra & Karnataka", {
      x: 0.55, y: 6.85, w: 9.6, h: 0.3, isTextBox: true, margin: 0, fontFace: F, fontSize: 8.5, color: C.faint,
    });
    function y0m(y, h, ih) { return y + (h - ih) / 2; }
  })();

  /* ============ S2 EXECUTIVE SUMMARY ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "", "One-page recommendation", "Executive ", "Summary", 2);
    // KPI row
    const kw = 2.985, kg = 0.13, ky = 1.40, kh = 1.06;
    statCard(s, ICONS, 0.5, ky, kw, kh, "rupee_" + BR, "₹25.4 cr", "FY29 revenue in our base case (low ₹22.1, high ₹29.3)", "2.2x the FY26 base of ₹11.7 cr");
    statCard(s, ICONS, 0.5 + (kw + kg), ky, kw, kh, "chartline_" + BR, "₹21 cr", "of new private-market revenue added over FY27-29", "₹15-28 cr depending on scenario");
    statCard(s, ICONS, 0.5 + 2 * (kw + kg), ky, kw, kh, "target_" + BR, "7.2%", "of the ₹165 cr/yr serviceable market held by FY29", "starting from roughly zero today");
    statCard(s, ICONS, 0.5 + 3 * (kw + kg), ky, kw, kh, "recycle_" + BR, "₹2.4 cr/yr", "comes back yearly from AMC, O&M and monitoring", "about 10% of FY29 sales");

    // three columns
    const cy = 2.66, ch = 3.30, cw = 3.97, cg = 0.21;
    // Col 1: the play
    card(s, 0.5, cy, cw, ch);
    sec2(s, ICONS, "bulb_" + BR, "Our plan in five steps", 0.66, cy + 0.14, { w: 3.4 });
    const moves = [
      "Sell to the buyers who have no choice: hotels, Tier-2 developers and private hospitals",
      "Start in Goa and towns within a day's drive; enter new cities only after old ones hit their targets",
      "Open doors with a ₹25k site audit, then sell standard 10/25/50/100 KLD packages billed by milestone",
      "Put AMC on at least 60% of installs, with IoT monitoring so clients clear consent renewals",
      "Grow from the installed base: fix broken STPs, monitor them, then recycle their water (with IISc)",
    ];
    let my = cy + 0.56;
    moves.forEach((m, i) => {
      s.addShape("roundRect", { x: 0.66, y: my, w: 0.26, h: 0.26, rectRadius: 0.05, fill: { color: C.brand }, line: { type: "none" } });
      s.addText(String(i + 1), { x: 0.66, y: my, w: 0.26, h: 0.26, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 10, bold: true, color: "FFFFFF" });
      s.addText(m, { x: 1.02, y: my - 0.02, w: 3.32, h: 0.52, isTextBox: true, margin: 0, fontFace: F, fontSize: 8.3, color: C.ink, lineSpacingMultiple: 1.0 });
      my += 0.535;
    });
    // Col 2: personas
    const c2x = 0.5 + cw + cg;
    card(s, c2x, cy, cw, ch);
    sec2(s, ICONS, "users_" + BR, "Who we go after first (weighted score)", c2x + 0.16, cy + 0.14, { w: 3.6, size: 12 });
    const pers = [
      ["hotel_" + BR, "Coastal & leisure hoteliers", "4.50", "20-150 keys · ₹18-45 L + AMC", "Buys when PCB consent or water bills bite"],
      ["building_" + BR, "Tier-2 residential developers", "3.80", "100-400 units · ₹35 L-1.2 cr", "Needs a working STP to get the occupancy certificate"],
      ["hospital_" + BR, "Private hospitals & clinics", "3.75", "30-150 beds · ₹12-35 L + AMC", "BMW Rules make treatment compulsory above 10 beds"],
    ];
    let py = cy + 0.60;
    pers.forEach(([ic, nm, sc, pr, tg]) => {
      chip(s, ICONS, ic, c2x + 0.16, py, 0.4);
      s.addText(nm, { x: c2x + 0.66, y: py - 0.03, w: 2.55, h: 0.24, isTextBox: true, margin: 0, fontFace: F, fontSize: 9.5, bold: true, color: C.ink });
      s.addShape("roundRect", { x: c2x + cw - 0.62, y: py - 0.02, w: 0.5, h: 0.24, rectRadius: 0.12, fill: { color: C.brand }, line: { type: "none" } });
      s.addText(sc, { x: c2x + cw - 0.62, y: py - 0.02, w: 0.5, h: 0.24, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 8.5, bold: true, color: "FFFFFF" });
      s.addText(pr, { x: c2x + 0.66, y: py + 0.21, w: 3.1, h: 0.2, isTextBox: true, margin: 0, fontFace: F, fontSize: 8, bold: true, color: C.brandDk });
      s.addText(tg, { x: c2x + 0.66, y: py + 0.40, w: 3.15, h: 0.34, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.6, color: C.gray, lineSpacingMultiple: 1.0 });
      py += 0.89;
    });
    // Col 3: corridor + risk
    const c3x = 0.5 + 2 * (cw + cg);
    card(s, c3x, cy, cw, 1.92);
    sec2(s, ICONS, "pin_" + BR, "Where, and in what order", c3x + 0.16, cy + 0.14, { w: 3.4, size: 12 });
    const phases = [
      ["P1 · FY27", "Goa plus Konkan, Kolhapur, Belagavi (within 250 km)"],
      ["P2 · FY28", "Hubballi-Dharwad, Mangaluru, Mysuru, with 2 hubs"],
      ["P3 · FY29", "Deeper Tier-3 towns through 25 trained partners"],
    ];
    let phy = cy + 0.58;
    phases.forEach(([tag, txt]) => {
      s.addShape("roundRect", { x: c3x + 0.16, y: phy, w: 0.78, h: 0.3, rectRadius: 0.06, fill: { color: C.tint }, line: { type: "none" } });
      s.addText(tag, { x: c3x + 0.16, y: phy, w: 0.78, h: 0.3, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 8, bold: true, color: C.brand });
      s.addText(txt, { x: c3x + 1.04, y: phy + 0.01, w: 2.82, h: 0.36, isTextBox: true, margin: 0, fontFace: F, fontSize: 8, color: C.ink, lineSpacingMultiple: 0.98 });
      phy += 0.42;
    });
    card(s, c3x, cy + 2.06, cw, 1.24, { fill: C.redT, lineColor: "F0C7BE" });
    sec2(s, ICONS, "alert_" + RD, "The risk that worries us most", c3x + 0.16, cy + 2.18, { w: 3.4, size: 12, color: C.red, bg: "F7D9D2" });
    s.addText([
      T("Developers paying late and locking up working capital. ", { bold: true, color: C.ink, fontSize: 8.2 }),
      T("Our guardrails: 30-40-25-5 milestone billing with an advance, credit checks with PDCs, developers capped at 25% of the order book, and no new city if DSO crosses 75 days.", { color: C.ink, fontSize: 8.2 }),
    ], { x: c3x + 0.16, y: cy + 2.56, w: 3.65, h: 0.68, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.04 });

    ribbon(s, ICONS, "flag_" + WH, "By FY29", "66 treatment projects and 400-plus bio-digesters, 14 clusters via 2 hubs and 25 partners, about ₹6 cr of self-funded spend", 6.55, 0.44, 11);
    footer2(s, "Figures from the p.4 market model and p.5 roadmap; FY26 base per BGCC problem statement. All FY27-29 figures are estimates.", 2);
  })();

  /* ============ S3 SEGMENTATION ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "1", "Deliverable 1 · Customer segmentation & targeting", "Eight buyer groups scored: ", "three worth chasing", 3);

    // ---- left: bubble matrix ----
    const mx = 0.5, mw = 4.55, my2 = 1.86, mh = 3.42;
    sec2(s, ICONS, "search_" + BR, "How we scored them (10 factors)", mx, 1.44, { w: 4.5, size: 12.5 });
    card(s, mx, my2, mw, mh, { noShadow: false, r: 0.06 });
    const X = v => mx + ((v - 2.2) / 2.9) * mw;
    const Y = v => my2 + mh - ((v - 2.5) / 2.5) * mh;
    s.addShape("line", { x: X(3.65), y: my2 + 0.06, w: 0, h: mh - 0.12, line: { color: C.line, width: 0.75, dashType: "dash" } });
    s.addShape("line", { x: mx + 0.06, y: Y(3.75), w: mw - 0.12, h: 0, line: { color: C.line, width: 0.75, dashType: "dash" } });
    const B = [
      ["Societies (retrofit)", 3.00, 3.33, 14, 0], ["MSME industrial", 2.75, 3.50, 40, 0],
      ["Commercial dev.", 2.88, 3.17, 35, 0], ["Schools & CSR", 3.25, 2.92, 14, 0],
      ["Homeowners", 4.38, 2.83, 0.6, 0], ["Hoteliers", 4.38, 4.58, 24, 1],
      ["Developers", 2.88, 4.42, 48, 1], ["Hospitals", 3.88, 3.67, 16, 1],
    ];
    B.forEach(([nm, ex, vy, tick, pri]) => {
      const r = 0.11 + Math.sqrt(tick) * 0.038;
      s.addShape("ellipse", {
        x: X(ex) - r, y: Y(vy) - r, w: 2 * r, h: 2 * r,
        fill: { color: pri ? C.brand : C.tint, transparency: pri ? 0 : 18 },
        line: { color: pri ? C.brandDk : "9FC2EE", width: pri ? 1.5 : 1 },
      });
    });
    const L = [
      ["Hoteliers", 4.38, 4.58, 0.0, -0.40, 1], ["Developers", 2.88, 4.42, 0.05, -0.50, 1],
      ["Hospitals", 3.88, 3.67, 0.62, -0.28, 1], ["Homeowners", 4.38, 2.83, 0.0, 0.26, 0],
      ["Societies (retrofit)", 3.00, 3.33, -0.20, -0.48, 0], ["MSME industrial", 2.75, 3.50, 0.30, -0.60, 0],
      ["Schools & CSR", 3.25, 2.92, 0.68, 0.0, 0], ["Commercial dev.", 2.88, 3.17, 0.0, 0.44, 0],
    ];
    L.forEach(([nm, ex, vy, dx, dy, pri]) => {
      s.addText(nm, {
        x: X(ex) - 0.75 + dx, y: Y(vy) + dy - 0.10, w: 1.5, h: 0.22, isTextBox: true, margin: 0, align: "center",
        fontFace: F, fontSize: 8, bold: !!pri, color: pri ? C.brandDk : C.gray,
      });
    });
    s.addText("Ease of capture →   (decision-maker access · cycle · payment · serviceability · rivalry)", {
      x: mx, y: my2 + mh + 0.06, w: mw, h: 0.2, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.2, color: C.gray, align: "center",
    });
    s.addText("Value at stake →", { x: mx - 1.6, y: my2 + mh / 2 - 0.1, w: 3.2, h: 0.2, isTextBox: true, margin: 0, rotate: 270, align: "center", fontFace: F, fontSize: 7.2, color: C.gray });
    s.addText("Bubble area = avg ticket (₹0.6 L - ₹48 L)  ·  blue solid = priority", {
      x: mx, y: my2 + mh + 0.28, w: mw, h: 0.2, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.2, color: C.gray, align: "center",
    });
    card(s, mx, my2 + mh + 0.52, mw, 0.52, { fill: C.tint2, noShadow: true });
    s.addText([
      T("WEIGHTS  ", { bold: true, color: C.brand, fontSize: 7 }),
      T("demand 15 · urgency 15 · fit 10 · ticket 10 · access to decision maker 10 · payment 10 · repeat/AMC 10 · service reach 10 · rivalry 5 · cycle 5  (scored 1 to 5, detail on p.9)", { color: C.gray, fontSize: 7 }),
    ], { x: mx + 0.1, y: my2 + mh + 0.55, w: mw - 0.2, h: 0.46, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.05, valign: "middle" });

    // ---- right: 3 persona cards ----
    const px0 = 5.32, pcw = 2.42, pcg = 0.18, pcy = 1.86, pch = 4.55;
    sec2(s, ICONS, "users_" + BR, "The three buyers, up close", px0, 1.44, { w: 6, size: 12.5 });
    const cards3 = [
      {
        ic: "hotel_" + BR, nm: "Coastal & leisure\nhotelier", sc: "4.50",
        rows: [
          ["bolt_" + BR, "Why now", "Consent renewal due, property expanding, or tanker bills hurting"],
          ["users_" + GY, "Who signs", "The owner; GM and MEP consultant weigh in"],
          ["rupee_" + BR, "Budget", "₹18-45 L turnkey plus AMC of ₹0.6-1.5 L a year"],
          ["clock_" + GY, "Timeline", "2 to 4 months"],
          ["certificate_" + BR, "Proof", "A hotel they can visit, NABL lab reports, DRDO pedigree"],
          ["flag_" + BR, "Way in", "₹25k audit, adjusted against the order; install inside 4 weeks"],
          ["recycle_" + GN, "Repeat", "Sister properties, reuse add-on, consumables"],
        ],
      },
      {
        ic: "building_" + BR, nm: "Tier-2 residential\ndeveloper", sc: "3.80",
        rows: [
          ["bolt_" + BR, "Why now", "EC terms and the occupancy certificate demand a live STP"],
          ["users_" + GY, "Who signs", "Promoter; MEP consultant and PMC write the spec"],
          ["rupee_" + BR, "Budget", "₹35 L to 1.2 cr design-build, billed by milestone"],
          ["clock_" + GY, "Timeline", "6 to 9 months, moving with construction"],
          ["certificate_" + BR, "Proof", "200-plus housing installs, the ONGC 100 KLD job, bank guarantee"],
          ["flag_" + BR, "Way in", "Free STP sizing at EC stage so we get written into the spec"],
          ["recycle_" + GN, "Repeat", "Their next project, plus society O&M after handover"],
        ],
      },
      {
        ic: "hospital_" + BR, nm: "Private hospital\n& clinic", sc: "3.75",
        rows: [
          ["bolt_" + BR, "Why now", "BMW Rules apply above 10 beds; NABH and consent add pressure"],
          ["users_" + GY, "Who signs", "Owner-doctor or trustee; the administrator runs the process"],
          ["rupee_" + BR, "Budget", "₹12-35 L compact skid plus AMC of ₹0.8-2 L a year"],
          ["clock_" + GY, "Timeline", "3 to 6 months"],
          ["certificate_" + BR, "Proof", "Compliance file, and proof we can install without shutting wards"],
          ["flag_" + BR, "Way in", "Liquid-waste audit plus help dealing with the PCB"],
          ["recycle_" + GN, "Repeat", "Sister facilities, disinfection upgrades, long AMC stays"],
        ],
      },
    ];
    cards3.forEach((cd, i) => {
      const x = px0 + i * (pcw + pcg);
      card(s, x, pcy, pcw, pch);
      chip(s, ICONS, cd.ic, x + 0.13, pcy + 0.13, 0.42);
      s.addText(cd.nm, { x: x + 0.64, y: pcy + 0.10, w: pcw - 1.2, h: 0.5, isTextBox: true, margin: 0, fontFace: F, fontSize: 9.5, bold: true, color: C.ink, lineSpacingMultiple: 0.95 });
      s.addShape("roundRect", { x: x + pcw - 0.60, y: pcy + 0.14, w: 0.48, h: 0.26, rectRadius: 0.13, fill: { color: C.brand }, line: { type: "none" } });
      s.addText(cd.sc, { x: x + pcw - 0.60, y: pcy + 0.14, w: 0.48, h: 0.26, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 8.5, bold: true, color: "FFFFFF" });
      s.addShape("line", { x: x + 0.13, y: pcy + 0.66, w: pcw - 0.26, h: 0, line: { color: C.line, width: 0.75 } });
      let ry = pcy + 0.76;
      cd.rows.forEach(([ic2, lb, tx]) => {
        s.addImage({ data: ICONS[ic2], x: x + 0.13, y: ry + 0.01, w: 0.15, h: 0.15 });
        s.addText([
          T(lb.toUpperCase() + "  ", { bold: true, color: C.brand, fontSize: 6.6 }),
          T(tx, { color: C.ink, fontSize: 7.3 }),
        ], { x: x + 0.34, y: ry - 0.02, w: pcw - 0.45, h: 0.5, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 0.98 });
        ry += 0.535;
      });
    });

    ribbon(s, ICONS, "target_" + WH, "Our call", "Put 80% of new-business time on these three. Homeowners keep buying through dealers; industrial ETPs only when they come to us.", 6.58, 0.42, 11);
    footer2(s, "Sources: GSPCB consent framework (susbio.in guide); BMW Rules 2016; EIA 2006 item 8(a); KSPCB rules (Deccan Herald 2024); EPBL refs (epbiocomposites.com; EquityBulls Dec 2023). Scores: team analysis.", 3);
  })();

  /* ============ S4 MARKET & COMPETITION ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "2", "Deliverable 2a · Market opportunity & competitive positioning", "A ₹270 cr a year market: ", "we can take ₹21 cr of it", 4);

    // ---- left: concentric TAM/SAM/SOM ----
    sec2(s, ICONS, "chart_" + BR, "Sized bottom-up, not from reports", 0.5, 1.44, { w: 3.7, size: 12.5 });
    const cxc = 2.15, byc = 4.02; // bottom of circles
    const circ = [
      [1.11, C.tint, "9FC2EE"], [0.81, "BBD7F5", "7FB0E8"], [0.50, C.brand, C.brandDk],
    ];
    circ.forEach(([r, fill, ln]) => {
      s.addShape("ellipse", { x: cxc - r, y: byc - 2 * r, w: 2 * r, h: 2 * r, fill: { color: fill }, line: { color: ln, width: 1 } });
    });
    s.addText([T("TAM  ", { bold: true, fontSize: 9.5, color: C.brandDk }), T("₹270 cr/yr", { bold: true, fontSize: 9.5, color: C.ink })],
      { x: cxc - 1.1, y: byc - 2.22 + 0.13, w: 2.2, h: 0.22, isTextBox: true, margin: 0, align: "center", fontFace: F });
    s.addText([T("SAM  ", { bold: true, fontSize: 9, color: C.brandDk }), T("₹165 cr/yr", { bold: true, fontSize: 9, color: C.ink })],
      { x: cxc - 1.0, y: byc - 1.62 + 0.11, w: 2.0, h: 0.2, isTextBox: true, margin: 0, align: "center", fontFace: F });
    s.addText([T("SOM\n", { bold: true, fontSize: 8.5, color: "FFFFFF" }), T("₹21 cr", { bold: true, fontSize: 11, color: "FFFFFF" })],
      { x: cxc - 0.5, y: byc - 0.86, w: 1.0, h: 0.56, isTextBox: true, margin: 0, align: "center", fontFace: F, lineSpacingMultiple: 0.95 });
    s.addText([
      T("● ", { color: "9FC2EE", fontSize: 6.8 }), T("TAM ", { bold: true, color: C.brandDk, fontSize: 6.8 }),
      T("all private-pay Tier 2/3 demand in the 3 states (₹239 cr STP/ETP, ₹32 cr bio)   ", { color: C.gray, fontSize: 6.8 }),
      T("● ", { color: "7FB0E8", fontSize: 6.8 }), T("SAM ", { bold: true, color: C.brandDk, fontSize: 6.8 }),
      T("what our corridor and skills can serve, ₹5 L-2.5 cr jobs   ", { color: C.gray, fontSize: 6.8 }),
      T("● ", { color: C.brand, fontSize: 6.8 }), T("SOM ", { bold: true, color: C.brandDk, fontSize: 6.8 }),
      T("new revenue we add over FY27-29 (₹15-28 cr), 7.2% of SAM by FY29", { color: C.gray, fontSize: 6.8 }),
    ], { x: 0.5, y: 4.12, w: 3.8, h: 0.42, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.05 });
    // state pills
    const states = [["MH", "59%"], ["KA", "28%"], ["Goa", "13%"]];
    states.forEach(([st, pc], i) => {
      const x = 0.52 + i * 1.28;
      s.addShape("roundRect", { x, y: 4.60, w: 1.16, h: 0.32, rectRadius: 0.16, fill: { color: C.tint2 }, line: { color: C.line, width: 0.75 } });
      s.addImage({ data: K("pin", BR), x: x + 0.09, y: 4.67, w: 0.18, h: 0.18 });
      s.addText([T(st + " ", { bold: true, color: C.ink, fontSize: 8.5 }), T(pc, { bold: true, color: C.brand, fontSize: 8.5 })],
        { x: x + 0.30, y: 4.60, w: 0.85, h: 0.32, isTextBox: true, margin: 0, fontFace: F, valign: "middle" });
    });

    // ---- middle: SAM by segment ----
    sec2(s, ICONS, "chartline_" + BR, "Serviceable demand by segment, ₹cr/yr", 4.42, 1.44, { w: 4.3, size: 12.5 });
    s.addChart("bar", [{
      name: "SAM",
      labels: ["Residential developers", "Hospitality", "Bio-digesters (retail)", "Hospitals", "Societies retrofit", "Education & CSR", "Commercial"],
      values: [96.8, 27.5, 20.9, 8.6, 5.9, 3.4, 2.4],
    }], {
      x: 4.42, y: 1.78, w: 4.15, h: 2.55, barDir: "bar",
      chartColors: [C.brand], showLegend: false, showTitle: false,
      showValue: true, dataLabelPosition: "outEnd", dataLabelColor: C.brandDk, dataLabelFontSize: 8, dataLabelFontFace: F, dataLabelFormatCode: "0.#",
      catAxisLabelColor: C.ink, catAxisLabelFontSize: 8, catAxisLabelFontFace: F,
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMaxVal: 110, barGapWidthPct: 42,
    });
    card(s, 4.42, 4.44, 4.15, 0.62, { fill: C.tint2, noShadow: true });
    s.addText([
      T("Developers are the biggest pool but pay slowly, so ", { color: C.ink, fontSize: 7.6 }),
      T("we lean on hotels and hospitals and cap developers at 25% of the book. ", { bold: true, color: C.brandDk, fontSize: 7.6 }),
      T("Formula: units x share lacking treatment x fit x conversion x ticket (p.9).", { color: C.gray, fontSize: 7.6 }),
    ], { x: 4.52, y: 4.50, w: 3.95, h: 0.52, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.02 });

    // ---- right: scenarios + checks ----
    const rx = 8.83, rw = 4.0;
    sec2(s, ICONS, "gear_" + BR, "Scenarios & feasibility checks", rx, 1.44, { w: 4.0, size: 12.5 });
    const scT = [
      [hcell("FY29, ₹cr", { fontSize: 7.6 }), hcell("Cons.", { fontSize: 7.6, align: "center" }), hcell("Base", { fontSize: 7.6, align: "center" }), hcell("Upside", { fontSize: 7.6, align: "center" })],
      [cell("Total revenue", { fontSize: 7.6 }), cell("22.1", { align: "center", fontSize: 7.6 }), cell("25.4", { align: "center", fontSize: 7.6, bold: true, fill: { color: C.amberT } }), cell("29.3", { align: "center", fontSize: 7.6 })],
      [cell("Cum. new revenue FY27-29", { fontSize: 7.6 }), cell("15.0", { align: "center", fontSize: 7.6 }), cell("20.7", { align: "center", fontSize: 7.6, bold: true, fill: { color: C.amberT } }), cell("27.6", { align: "center", fontSize: 7.6 })],
      [cell("Cum. total revenue FY27-29", { fontSize: 7.6 }), cell("53.7", { align: "center", fontSize: 7.6 }), cell("59.4", { align: "center", fontSize: 7.6, bold: true, fill: { color: C.amberT } }), cell("66.3", { align: "center", fontSize: 7.6 })],
    ];
    s.addTable(scT, { x: rx, y: 1.78, w: rw, colW: [1.90, 0.70, 0.70, 0.70], autoPage: false });
    card(s, rx, 2.98, rw, 1.02, { fill: C.tint2, noShadow: true });
    s.addImage({ data: K("bolt", AM), x: rx + 0.10, y: 3.06, w: 0.2, h: 0.2 });
    s.addText([
      T("WHAT MOVES THE NUMBER  ", { bold: true, color: C.brand, fontSize: 7 }),
      T("hotel conversion between 6 and 10% a year (₹9 cr swing); developer STP-trigger share between 15 and 25% (₹35 cr); proposal win rate between 15 and 25%.", { color: C.ink, fontSize: 7.4 }),
    ], { x: rx + 0.36, y: 3.04, w: rw - 0.5, h: 0.9, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.04 });
    const checks = [
      "FY29 needs 34 installs a year; 5 crews (3 ours, 2 partner) can do it",
      "At 75 receivable days, ₹5.2 cr is locked up, vs net worth above ₹12 cr",
      "The ₹6.2 cr of investment over 3 years comes from internal accruals",
    ];
    let cyk = 4.06;
    checks.forEach(t => {
      s.addImage({ data: K("check", GN), x: rx + 0.02, y: cyk + 0.01, w: 0.17, h: 0.17 });
      s.addText(t, { x: rx + 0.27, y: cyk - 0.02, w: rw - 0.3, h: 0.30, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.6, color: C.ink, lineSpacingMultiple: 0.98 });
      cyk += 0.31;
    });

    // ---- positioning ribbon, then evidence matrix ----
    ribbon(s, ICONS, "shield_" + WH, "Our pitch", "The compliance partner next door: certified technology, FRP made in Goa, service within a day or two. We sell on lifetime cost, not the cheapest quote.", 5.10, 0.36, 10);
    const colDef = [
      ["COMPETITOR MATRIX", C.ink], ["EPBL", C.brand], ["Daiki Axis", C.daiki], ["Ion Exchange", C.ionx],
      ["Thermax", C.thermax], ["SUSBIO", C.susbio], ["Banka BioLoo", C.banka], ["NCR online", C.ncr],
    ];
    const matRows = [
      ["Technology", "DRDO bio-digester + MBBR/SBR/MBR + ozone FRP", "Johkasou FRP capsule, 1-50 KLD", "INDION packaged, SBR, MBR", "FabX MBBR, BioCask, custom ETP", "ECOTREAT anaerobic + MBBR FRP", "DRDO-inoculum bio-toilets, STP, FSM", "MBBR / MBR / SBR fabrication"],
      ["Sweet spot", "5-100 KLD private compliance buyers", "Villas, hotels, institutions", "SME up to municipal, all scales", "Industrial; above 1 MLD EPC", "Hotels; ₹35k/KLD, 3-5 day install", "Railways, institutions (₹56.5 cr)", "Commercial & industrial"],
      ["Presence & local O&M", "Goa OEM, 200+ installs, 24-48h corridor crews", "Dealers; ₹200 cr Tumakuru plant; dealer O&M", "Partner network; small jobs routed out", "Pan-India; distributor-sold small KLD", "MH & west; service base growing", "Hyderabad; rail O&M annuity focus", "SEO claims; remote response only"],
      ["Gap EPBL can use", "Ours to defend, with certification and service", "Premium import; thin turnkey civil work", "Small jobs get no direct engineering", "10-50 KLD is not their focus", "Toughest rival; beat them on Goa/KA service", "Weak hospitality presence", "Local 24-48h service wins"],
    ];
    const colW = [1.30, 1.62, 1.60, 1.55, 1.55, 1.58, 1.60, 1.53];
    const tbl = [colDef.map(([t, col], i) => cell(t, { bold: true, color: "FFFFFF", fill: { color: col }, fontSize: i ? 7.2 : 6.6, align: i ? "center" : "left", valign: "middle" }))];
    matRows.forEach((r, ri) => {
      tbl.push(r.map((t, i) => cell(t, {
        fontSize: 6.5, align: "left",
        bold: i === 0, color: i === 0 ? C.brandDk : (i === 1 ? C.brandDk : C.ink),
        fill: i === 1 ? { color: C.tint } : (ri % 2 ? { color: C.tint2 } : undefined),
      })));
    });
    s.addTable(tbl, { x: 0.5, y: 5.56, w: 12.33, colW, autoPage: false });
    footer2(s, "CPCB 2021; Goa Tourism 2024; HVS-ANAROCK 2024; MahaRERA 2025; 99acres RERA; BMW Rules 2016; daikiaxis.in; ionexchangeglobal.com; thermaxglobal.com; susbio.in; screener.in (BANKA); netsolwater.com. Adjacent models: CDD DEWATS & Boson WaaS (learn, not fight). URLs p.8.", 4);
  })();

  /* ============ S5 ROADMAP ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "2", "Deliverable 2b · Three-year go-to-market roadmap", "A 36-month rollout ", "that earns each next step", 5);

    const pw = 3.85, gap = 0.39, py = 1.42, ph = 3.02;
    const phases = [
      {
        n: "1", fy: "FY27", ttl: "Goa and the Konkan belt", col: C.brand,
        rows: [
          ["pin_" + BR, "Where", "Goa (all), Sindhudurg-Ratnagiri, Kolhapur, Belagavi (≤250 km of Bicholim)"],
          ["users_" + BR, "Who", "Hoteliers first; hospitals; selective developers"],
          ["tag_" + BR, "Sell", "10/25/50 KLD FRP packages; ₹25k audit entry; bio-digester retail; STP Rescue"],
          ["route_" + BR, "Route", "Founder-led key accounts plus 2 salespeople; 15 MEP consultants; TTAG, GCCI, CREDAI Kolhapur; 10 dealers"],
          ["rupee_" + BR, "Invest", "₹1.4 cr: hires, demo skids, service van, CRM, NABL tie-up"],
          ["target_" + BR, "Target", "₹3.0-3.5 cr new orders · 10 installs · AMC ≥50%"],
        ],
      },
      {
        n: "2", fy: "FY28", ttl: "Into Karnataka", col: C.brandDk,
        rows: [
          ["pin_" + BR, "Where", "+ Hubballi-Dharwad, Mangaluru, Mysuru, Sangli probe; Belagavi hub + Mangaluru spoke"],
          ["users_" + BR, "Who", "Developers scaled up; hospitals; education & CSR"],
          ["tag_" + BR, "Sell", "+100 KLD series, hospital ETP skid, SmartSTP monitoring, 3-yr O&M handover"],
          ["route_" + BR, "Route", "25 consultants; 6 EPC franchisees; AHPI/IMA chapters; CSR implementation partners"],
          ["rupee_" + BR, "Invest", "₹2.2 cr: 2 hubs, 4 hires, inventory, monitoring stock"],
          ["target_" + BR, "Target", "₹6.4 cr new revenue · channel ≥40% · uptime ≥95%"],
        ],
      },
      {
        n: "3", fy: "FY29", ttl: "Tier-3 through partners", col: C.green,
        rows: [
          ["pin_" + BR, "Where", "Davanagere, Shivamogga, Udupi, Hassan, Solapur; Nashik & Sambhajinagar partner-led"],
          ["users_" + BR, "Who", "All three personas + societies retrofit at scale"],
          ["tag_" + BR, "Sell", "Full catalogue + AquaLoop reuse + O&M takeovers; WaaS pilot"],
          ["route_" + BR, "Route", "25 certified dealer-installers; association programmes; direct for ₹50 L+ deals"],
          ["rupee_" + BR, "Invest", "₹2.6 cr: dealer academy, monitoring fleet, working capital"],
          ["target_" + BR, "Target", "₹11.9 cr new revenue · recurring ~10% · 34 installs/yr"],
        ],
      },
    ];
    phases.forEach((p, i) => {
      const x = 0.5 + i * (pw + gap);
      card(s, x, py, pw, ph);
      s.addShape("roundRect", { x, y: py, w: pw, h: 0.44, rectRadius: 0.08, fill: { color: p.col }, line: { type: "none" } });
      s.addShape("ellipse", { x: x + 0.10, y: py + 0.08, w: 0.28, h: 0.28, fill: { color: "FFFFFF" }, line: { type: "none" } });
      s.addText(p.n, { x: x + 0.10, y: py + 0.08, w: 0.28, h: 0.28, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 12, bold: true, color: p.col });
      s.addText([T(p.ttl + "  ", { bold: true, fontSize: 11, color: "FFFFFF" }), T(p.fy, { bold: true, fontSize: 8.5, color: "D8E6FA" })],
        { x: x + 0.46, y: py, w: pw - 0.56, h: 0.44, isTextBox: true, margin: 0, fontFace: F, valign: "middle" });
      let ry = py + 0.54;
      const rh = [0.46, 0.28, 0.44, 0.46, 0.28, 0.30];
      p.rows.forEach(([ic, lb, tx], j) => {
        s.addImage({ data: ICONS[ic], x: x + 0.12, y: ry + 0.01, w: 0.15, h: 0.15 });
        s.addText([
          T(lb.toUpperCase() + "  ", { bold: true, color: p.col, fontSize: 6.6 }),
          T(tx, { color: C.ink, fontSize: 7.3 }),
        ], { x: x + 0.34, y: ry - 0.02, w: pw - 0.46, h: rh[j], isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 0.97 });
        ry += rh[j] + 0.032;
      });
      if (i < 2) s.addShape("chevron", { x: x + pw + 0.05, y: py + 1.25, w: 0.30, h: 0.5, fill: { color: C.amber }, line: { type: "none" } });
    });
    // gates
    const gates = [
      ["GATE 1 → 2", "≥10 lab-verified references · AMC ≥50% · DSO ≤75 · pipeline ≥3× next-year target"],
      ["GATE 2 → 3", "Channel ≥40% of pipeline · install ≤45 days · uptime ≥95% · repeat ≥20% · GM ≥30%"],
    ];
    gates.forEach((g, i) => {
      const x = 2.4 + i * (pw + gap);
      s.addShape("roundRect", { x, y: 4.56, w: pw + 0.2, h: 0.42, rectRadius: 0.09, fill: { color: C.amberT }, line: { color: C.amber, width: 1 } });
      s.addImage({ data: K("flag", AM), x: x + 0.10, y: 4.66, w: 0.2, h: 0.2 });
      s.addText([T(g[0] + "  ", { bold: true, color: "9A6A0F", fontSize: 7.6 }), T(g[1], { color: C.ink, fontSize: 7.1 })],
        { x: x + 0.36, y: 4.56, w: pw - 0.2, h: 0.42, isTextBox: true, margin: 0, fontFace: F, valign: "middle", lineSpacingMultiple: 0.96 });
    });
    // funnel
    sec2(s, ICONS, "funnel_" + BR, "Acquisition funnel & capacity  (FY27 → FY29)", 0.5, 5.12, { w: 6.5, size: 12 });
    const st = [["Audits / leads", "320 → 900"], ["Qualified", "130 → 380 (₹32→95 cr)"], ["Proposals", "55 → 160"], ["Wins", "10 → 34"], ["New revenue", "₹2.4 → 11.9 cr"]];
    st.forEach(([a, bb], i) => {
      const x = 0.5 + i * 1.40;
      if (i === 4) {
        s.addShape("roundRect", { x, y: 5.44, w: 1.62, h: 0.70, rectRadius: 0.09, fill: { color: C.brand }, line: { type: "none" }, shadow: shadowSm() });
        s.addText([T(a + "\n", { bold: true, fontSize: 7.3, color: "FFFFFF" }), T(bb, { fontSize: 7.1, color: "FFD98A", bold: true })],
          { x: x + 0.06, y: 5.44, w: 1.5, h: 0.70, isTextBox: true, margin: 0, fontFace: F, valign: "middle", align: "center", lineSpacingMultiple: 0.96 });
      } else {
        s.addShape("chevron", { x, y: 5.44, w: 1.34, h: 0.70, fill: { color: C.tint }, line: { color: "9FC2EE", width: 0.75 } });
        s.addText([T(a + "\n", { bold: true, fontSize: 7.3, color: C.brandDk }), T(bb, { fontSize: 7.0, color: C.ink })],
          { x: x + 0.15, y: 5.44, w: 1.08, h: 0.70, isTextBox: true, margin: 0, fontFace: F, valign: "middle", align: "center", lineSpacingMultiple: 0.96 });
      }
    });
    s.addText("Cycle: hotels 2-4 mo · hospitals 3-6 mo · developers 6-9 mo   |   Crews: 2 of our own in FY27, growing to 3 own + 2 partner by FY29 (~8 installs per crew a year)   |   KPIs: pipeline cover, proposal-to-win %, DSO, install cycle, AMC attach, uptime, repeat share", {
      x: 0.5, y: 6.22, w: 7.4, h: 0.34, isTextBox: true, margin: 0, fontFace: F, fontSize: 6.9, color: C.gray, lineSpacingMultiple: 1.0,
    });
    // revenue chart
    sec2(s, ICONS, "chartline_" + BR, "Revenue build, ₹cr (base)", 8.3, 5.12, { w: 4.5, size: 12 });
    s.addChart("bar", [
      { name: "Existing base (5%/yr)", labels: ["FY26", "FY27", "FY28", "FY29"], values: [11.7, 12.3, 12.9, 13.5] },
      { name: "New private-market", labels: ["FY26", "FY27", "FY28", "FY29"], values: [0, 2.4, 6.4, 11.9] },
    ], {
      x: 8.3, y: 5.40, w: 4.5, h: 1.14, barDir: "col", barGrouping: "stacked",
      chartColors: [C.brand, C.amber], showLegend: true, legendPos: "r", legendFontSize: 7, legendColor: C.ink, legendFontFace: F,
      showTitle: false, showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 6.8, dataLabelFontFace: F, dataLabelFormatCode: "0.#;;",
      catAxisLabelColor: C.ink, catAxisLabelFontSize: 7.5, catAxisLabelFontFace: F,
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMaxVal: 30, barGapWidthPct: 55,
    });
    ribbon(s, ICONS, "flag_" + WH, "The rule", "We open a new city only after the last one passes its gate. Service quality and cash discipline grow first, geography second.", 6.66, 0.40, 11);
    footer2(s, "Targets from the p.4 model; distances from Bicholim, Goa. Investment funded by internal accruals + IPO working capital (problem statement).", 5);
  })();

  /* ============ S6 RISKS ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "3", "Deliverable 3 · Risk assessment & mitigation", "What can go wrong, ", "and what we would do about it", 6);

    // heatmap
    sec2(s, ICONS, "alert_" + BR, "Likelihood × impact heatmap", 0.5, 1.44, { w: 4.3, size: 12.5 });
    const hx = 0.86, hy = 1.86, cwd = 0.74, chd = 0.66;
    for (let li = 1; li <= 5; li++) for (let im = 1; im <= 5; im++) {
      const sev = li + im;
      const col = sev >= 8 ? C.redT : sev >= 6 ? C.amberT : C.greenT;
      s.addShape("rect", { x: hx + (li - 1) * cwd, y: hy + (5 - im) * chd, w: cwd, h: chd, fill: { color: col }, line: { color: "FFFFFF", width: 1.5 } });
    }
    for (let i = 1; i <= 5; i++) {
      s.addText(String(i), { x: hx + (i - 1) * cwd, y: hy + 5 * chd + 0.02, w: cwd, h: 0.16, isTextBox: true, margin: 0, align: "center", fontFace: F, fontSize: 6.8, color: C.faint });
      s.addText(String(i), { x: hx - 0.18, y: hy + (5 - i) * chd + chd / 2 - 0.08, w: 0.14, h: 0.16, isTextBox: true, margin: 0, align: "center", fontFace: F, fontSize: 6.8, color: C.faint });
    }
    const R = [["R1", 4, 5, 0], ["R2", 4, 3, 0], ["R3", 3, 4, -0.19], ["R4", 3, 3, 0], ["R5", 3, 4, 0.19], ["R6", 2, 4, 0], ["R7", 3, 2, 0], ["R8", 2, 5, 0]];
    R.forEach(([code, li, im, dxo]) => {
      const px = hx + (li - 1) * cwd + cwd / 2 - 0.155 + dxo;
      const pyy = hy + (5 - im) * chd + chd / 2 - 0.155;
      const hot = li + im >= 8;
      s.addShape("ellipse", { x: px, y: pyy, w: 0.31, h: 0.31, fill: { color: hot ? C.red : C.brandDk }, line: { color: "FFFFFF", width: 1 } });
      s.addText(code, { x: px - 0.05, y: pyy + 0.02, w: 0.41, h: 0.25, isTextBox: true, margin: 0, align: "center", fontFace: F, fontSize: 7.3, bold: true, color: "FFFFFF" });
    });
    s.addText("Likelihood →", { x: hx, y: hy + 5 * chd + 0.20, w: 5 * cwd, h: 0.18, isTextBox: true, margin: 0, align: "center", fontFace: F, fontSize: 7.2, color: C.gray });
    s.addText("Impact →", { x: hx - 1.55, y: hy + 2.5 * chd - 0.09, w: 2.4, h: 0.18, isTextBox: true, margin: 0, rotate: 270, align: "center", fontFace: F, fontSize: 7.2, color: C.gray });
    s.addText([
      T("R1 ", { bold: true }), T("Developer receivables (Fin) · "), T("R2 ", { bold: true }), T("Price war (Comp) · "),
      T("R3 ", { bold: true }), T("Commissioning & inoculum (Ops) · "), T("R4 ", { bold: true }), T("Partner conflict (Distr.) · "),
      T("R5 ", { bold: true }), T("Service outrun (Ops) · "), T("R6 ", { bold: true }), T("Norm tightening (Reg.) · "),
      T("R7 ", { bold: true }), T("Cycle stalls cash (Fin) · "), T("R8 ", { bold: true }), T("Marquee failure (Reput.). "),
      T("Red = red-zone (L+I ≥ 8)", { color: C.gray }),
    ], { x: 0.5, y: hy + 5 * chd + 0.46, w: 4.15, h: 1.1, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.4, color: C.ink, lineSpacingMultiple: 1.12 });

    // mitigation table
    sec2(s, ICONS, "shield_" + BR, "The six risks that matter, and our answers", 5.05, 1.44, { w: 7.5, size: 12.5 });
    const M = (t, o = {}) => cell(t, Object.assign({ fontSize: 7.2 }, o));
    const MH = (t) => hcell(t, { fontSize: 7.5 });
    const mit = [
      [MH("Risk (cat.)"), MH("Root cause & impact"), MH("Early warning"), MH("Preventive control"), MH("Contingency"), MH("Owner")],
      [M("R1 Developer receivables (Financial)", { bold: true, color: C.red }), M("Milestone slippage, RERA escrow; ₹2-3 cr locked, growth stalls"), M("DSO >75; billing-collection gap >2 mo"), M("30-40-25-5 milestones + advance; credit checks + PDCs; 25% exposure cap"), M("Stop-work clause; invoice discounting"), M("CFO")],
      [M("R2 Price-led rivalry (Competitive)", { bold: true }), M("SUSBIO ₹35k/KLD; Daiki KA plant; NCR bidders erode margin"), M("Win rate <25%; discount >8%"), M("Lifecycle-cost selling; compliance + AMC bundle; 28% GM walk-away floor"), M("Value-engineered Lite SKU"), M("Sales head")],
      [M("R3 Commissioning & inoculum variation (Operational)", { bold: true }), M("Site variability; biology stabilises 4-8 weeks"), M(">2 sites off-norm at day-30"), M("Factory acceptance test; inoculum batch QC; 30/60/90-day NABL tests"), M("Rapid-response; ozone-assist retrofit"), M("Tech head")],
      [M("R4 Partner conflict (Distribution)", { bold: true }), M("Territory overlap, poaching; channel stalls"), M("Partner pipeline <30% plan; duplicate leads"), M("≤2 partners/territory; registered-lead lock; installer academy; tiers"), M("Territory reassignment; direct cover"), M("Channel mgr")],
      [M("R5 Expansion outruns service (Operational)", { bold: true, color: C.red }), M("Install base grows faster than technicians; SLA breach"), M("Response >48h; uptime <95%"), M("KPI gates; hub per ~150 km; 1 technician : 25 AMC sites"), M("Freeze clusters; contract service partners"), M("COO")],
      [M("R6 Norms tighten (Regulatory, our added category)", { bold: true }), M("NGT / CPCB revisions strand designs"), M("Draft notifications; consent queries"), M("Design margin to stricter norms; IISc tertiary pipeline"), M("Paid retrofit-upgrade programme"), M("MD + Tech")],
    ];
    s.addTable(mit, { x: 5.05, y: 1.80, w: 7.78, colW: [1.38, 1.70, 1.10, 1.95, 1.05, 0.60], autoPage: false });

    // watch metrics for R7/R8
    card(s, 5.05, 5.05, 7.78, 1.28, { fill: C.tint2, noShadow: true });
    sec2(s, ICONS, "eye_" + BR, "The two risks we watch rather than fix upfront", 5.2, 5.17, { w: 7, size: 11.5 });
    s.addText([
      T("R7 Long cycles stall cash (Fin):  ", { bold: true, color: C.brandDk, fontSize: 8 }),
      T("we track pipeline cover weekly (at least 3x the next quarter's target); the audit entry offer keeps hotel cycles down to 2-4 months.\n", { color: C.ink, fontSize: 8 }),
      T("R8 A big-name site fails (Reputation):  ", { bold: true, color: C.red, fontSize: 8 }),
      T("IoT uptime alerts on every AMC site, a 48-hour response promise, a preventive maintenance calendar, and a yearly NABL effluent audit at reference sites.", { color: C.ink, fontSize: 8 }),
    ], { x: 5.2, y: 5.52, w: 7.45, h: 0.75, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.06 });

    ribbon(s, ICONS, "shield_" + WH, "In short", "Milestone billing, exposure caps and gated expansion keep the plan self-funding. R7 and R8 sit on watch metrics, not in the red zone.", 6.58, 0.42, 11);
    footer2(s, "Likelihood/impact: team scoring from competitor research, CPCB 2021 utilisation gap and SME receivable norms. Impact scale: 3 = ₹0.5-1 cr; 5 = >₹2 cr or franchise damage.", 6);
  })();

  /* ============ S7 PORTFOLIO ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "4", "Deliverable 4 · Portfolio expansion: adjacent products & technologies", "Three add-ons worth building, ", "in a set order", 7);

    sec2(s, ICONS, "chart_" + BR, "Weighted adjacency scores (7 criteria, 100 pts)", 0.5, 1.44, { w: 5, size: 12.5 });
    const adjLabels = ["Biogas & nutrient recovery", "Sludge / faecal-sludge svcs", "Water-as-a-service (BOOT)", "Constructed wetlands / DEWATS", "MBR premium line", "Advanced disinfection", "Greywater recycling", "Water-reuse module (tertiary)", "IoT monitoring & dashboards", "STP retrofit + O&M takeover"];
    s.addChart("bar", [
      { name: "Evaluated", labels: adjLabels, values: [2.30, 3.00, 3.05, 3.20, 3.20, 3.55, 3.55, null, null, null] },
      { name: "Selected", labels: adjLabels, values: [null, null, null, null, null, null, null, 4.30, 4.55, 4.65] },
    ], {
      x: 0.5, y: 1.78, w: 4.9, h: 3.55, barDir: "bar", barGrouping: "stacked",
      chartColors: ["A9C7EF", C.brand], showLegend: false, showTitle: false,
      showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 7.4, dataLabelFontFace: F, dataLabelFormatCode: "0.00;;",
      catAxisLabelColor: C.ink, catAxisLabelFontSize: 7.6, catAxisLabelFontFace: F,
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMaxVal: 5.4, barGapWidthPct: 36,
    });
    card(s, 0.5, 5.48, 4.9, 0.60, { fill: C.tint2, noShadow: true });
    s.addText([
      T("CRITERIA (WEIGHTS)  ", { bold: true, color: C.brand, fontSize: 6.8 }),
      T("demand 20 · synergy & feasibility 20 · capital 15 (inverse) · margin 15 · complexity 10 (inverse) · time-to-market 10 · recurring 10. Scored 1 to 5; full matrix on p.9", { color: C.gray, fontSize: 6.9 }),
    ], { x: 0.6, y: 5.52, w: 4.7, h: 0.52, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.04, valign: "middle" });

    // three chosen cards
    const cx = 5.72, cw2 = 7.11;
    const chosen = [
      {
        ic: "wrench_" + BR, nm: "STP Rescue: retrofit + O&M takeover", tag: "NOW (M0-3) · BUILD IN-HOUSE", h: 1.28,
        rows: [
          ["bulb_" + BR, "Why", "CPCB found a third of installed capacity idle or off-norm, so demand is certain and capex is zero"],
          ["rupee_" + BR, "Price", "₹3-15 L per retrofit plus ₹0.5-3 L a year for O&M (about 35% margin)"],
          ["pin_" + BR, "Pilot", "10 audits at Goa hotels"],
          ["target_" + BR, "Metric", "25 retrofits and 40 O&M contracts by FY29; this also seeds the AMC fleet"],
        ],
      },
      {
        ic: "sensors_" + BR, nm: "SmartSTP: IoT monitoring & compliance", tag: "M6 · WHITE-LABEL + OWN DASHBOARD", h: 1.28,
        rows: [
          ["bulb_" + BR, "Why", "Consent renewals increasingly ask for data, and it makes every EPBL AMC harder to replace"],
          ["rupee_" + BR, "Price", "₹10-15k to install plus ₹3-5k a month per site; ₹50-70 L to set up"],
          ["pin_" + BR, "Pilot", "20 AMC sites in Goa"],
          ["target_" + BR, "Metric", "150 connected sites by FY29, with churn under 10%"],
        ],
      },
      {
        ic: "recycle_" + BR, nm: "AquaLoop: treated-water reuse module", tag: "M9-12 · DEVELOP WITH IISc", h: 1.28,
        rows: [
          ["bulb_" + BR, "Why", "Hotels pay tanker rates for water that CGWA already tells them to recycle; builds on the oxy-STP line and the IISc MoU"],
          ["rupee_" + BR, "Price", "₹6-18 L add-on skid (UF, carbon, UV/ozone); ₹1-1.5 cr to develop"],
          ["pin_" + BR, "Pilot", "2 Goa resorts and 1 Kolhapur society"],
          ["target_" + BR, "Metric", "On 25% of new STP orders by FY29"],
        ],
      },
    ];
    let cy2 = 1.44;
    chosen.forEach(cd => {
      card(s, cx, cy2, cw2, cd.h);
      chip(s, ICONS, cd.ic, cx + 0.13, cy2 + 0.12, 0.38);
      s.addText(cd.nm, { x: cx + 0.62, y: cy2 + 0.10, w: 4.4, h: 0.24, isTextBox: true, margin: 0, fontFace: F, fontSize: 10.5, bold: true, color: C.brandDk });
      s.addShape("roundRect", { x: cx + cw2 - 2.42, y: cy2 + 0.11, w: 2.30, h: 0.24, rectRadius: 0.12, fill: { color: C.amberT }, line: { type: "none" } });
      s.addText(cd.tag, { x: cx + cw2 - 2.42, y: cy2 + 0.11, w: 2.30, h: 0.24, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 6.8, bold: true, color: "9A6A0F" });
      // 2x2 rows
      const colw = (cw2 - 0.4) / 2;
      cd.rows.forEach(([ic2, lb, tx], j) => {
        const rx2 = cx + 0.14 + (j % 2) * (colw + 0.12);
        const ry2 = cy2 + 0.44 + Math.floor(j / 2) * 0.42;
        s.addImage({ data: ICONS[ic2], x: rx2, y: ry2 + 0.01, w: 0.14, h: 0.14 });
        s.addText([
          T(lb.toUpperCase() + "  ", { bold: true, color: C.brand, fontSize: 6.4 }),
          T(tx, { color: C.ink, fontSize: 7.0 }),
        ], { x: rx2 + 0.20, y: ry2 - 0.02, w: colw - 0.22, h: 0.42, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 0.95 });
      });
      cy2 += cd.h + 0.13;
    });
    // sequence strip
    sec2(s, ICONS, "route_" + BR, "Sequencing", cx, cy2 + 0.02, { w: 3, size: 11.5 });
    const seq = [["wrench_" + BR, "M0-3", "STP Rescue"], ["sensors_" + BR, "M6", "SmartSTP"], ["recycle_" + GN, "M9-12", "AquaLoop"], ["briefcase_" + BR, "FY29", "WaaS pilot"]];
    seq.forEach(([ic, tm, nm], i) => {
      const x = cx + i * 1.82;
      s.addShape("roundRect", { x, y: cy2 + 0.36, w: 1.62, h: 0.42, rectRadius: 0.09, fill: { color: i === 3 ? C.tint2 : C.tint }, line: { color: "9FC2EE", width: 0.75 } });
      s.addImage({ data: ICONS[ic], x: x + 0.09, y: cy2 + 0.475, w: 0.18, h: 0.18 });
      s.addText([T(tm + "  ", { bold: true, color: C.brand, fontSize: 7.2 }), T(nm, { bold: true, color: C.ink, fontSize: 7.8 })],
        { x: x + 0.32, y: cy2 + 0.36, w: 1.28, h: 0.42, isTextBox: true, margin: 0, fontFace: F, valign: "middle" });
      if (i < 3) s.addText("→", { x: x + 1.60, y: cy2 + 0.36, w: 0.26, h: 0.42, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 12, bold: true, color: C.amber });
    });
    s.addText("Parked for now: full WaaS (partner-financed pilot only), an MBR line, FSTP and biogas. Too much capex, too municipal, or too small. The three we picked add about ₹2.4 cr a year of recurring revenue by FY29 at 35-40% margins.", {
      x: cx, y: cy2 + 0.86, w: cw2, h: 0.36, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.0, color: C.gray, lineSpacingMultiple: 1.0,
    });

    ribbon(s, ICONS, "recycle_" + WH, "Bottom line", "The add-ons sell into plants we already service and lift recurring revenue to about 10% of sales by FY29, with no new manufacturing.", 6.58, 0.42, 10.5);
    footer2(s, "CPCB 2021 (26,869 operational vs 31,841 MLD installed; 20,235 utilised); CGWA 2020 reuse mandate; IISc MoU (ANI, Feb 2026); Boson Whitewater WaaS benchmark (Zerodha Rainmatter).", 7);
  })();

  /* ============ S8 REFERENCES ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "", "Supporting material", "References ", "& methodology", 8);
    const G = (t) => T(t + "\n", { bold: true, color: C.brand, fontSize: 8.6 });
    const Ii = (t) => T(t + "\n", { color: C.ink, fontSize: 7.1 });
    const colL = [
      G("CASE"),
      Ii("BGCC Case Consilium 2026 Round 2, EP Biocomposites Ltd problem statement, BITS Pilani Goa (all slides). Company FY26 financials, price ranges, IISc MoU and Unkal Nullah reference cited from this document."),
      G("EPBL & GROUP"),
      Ii("EPBL product pages: epbiocomposites.com/bio-digester-toilet-manufacturer-in-goa/; /sewage-and-effluent-treatment-plant-manufacturer-in-goa/ (acc. Sep 2026), slides 3-5"),
      Ii("EPBL IPO & pre-IPO financials: chittorgarh.com/ipo/ep-biocomposites-ipo/1286/ (2022), slides 2,5"),
      Ii("ONGC 100-KLD MBR STP order ₹72.27 L: equitybulls.com/category.php?id=340437 (Dec 2023), slides 3,4"),
      Ii("IISc Bengaluru MoU: aninews.in/news/business/ep-biocomposites-strengthens-technology-capabilities... (Feb 2026), slides 2,7"),
      Ii("EPBL incorporation, Bicholim: zaubacorp.com/EP-BIOCOMPOSITES-LIMITED-U28900GA2020PLC014240, slide 5"),
      G("GOVERNMENT & REGULATORY"),
      Ii("CPCB, National Inventory of STPs, Mar 2021: cpcb.gov.in (report id 1228); Goa gap via navhindtimes.in (Oct 2021), slides 2,4,6,7"),
      Ii("Bio-medical Waste Mgmt Rules 2016 (amend. 2018), >10-bed ETP mandate: cpcb.gov.in / MoEFCC gazette, slides 3,4"),
      Ii("Karnataka apartment STP rules & 2024 revision: deccanherald.com/india/karnataka/karnataka-government-relaxes-rules-stp-not-must-for-apartments-with-less-than-120-units-2933606, slides 3,4"),
      Ii("EIA Notification 2006 item 8(a) ≥20,000 sqm: lexology.com/library/detail.aspx?g=8b0e2b16 (2025), slides 3,4"),
      Ii("NGT OA 593/2017 order 28.08.2019: greentribunal.gov.in, slide 4"),
      Ii("CGWA guidelines 24 Sep 2020 (recycled-water mandate): cgwa-noc.gov.in via thesustainabilitycloud.com/blog/cgwa-guidelines/, slides 4,7"),
      Ii("CSR ₹34,908.75 cr FY24; health & sanitation ~₹8,739 cr: csr.gov.in via indiacsr.in (2024); proteantech.in, slide 4"),
      Ii("Census 2011: 38.2% urban households on septic tanks: censusindia.gov.in (HL-08), slide 4"),
    ];
    const colR = [
      G("MARKET & DEMAND"),
      Ii("Goa tourist arrivals 2024 (10.41 mn): goa-tourism.com/news/goa-records-robust-21-percent-growth-in-tourism..., slides 3,4"),
      Ii("Goa registered accommodation ~9,000 units (2024): Goa DoT via traveltrendstoday.in, slides 4,9"),
      Ii("HVS ANAROCK India Hospitality Overview 2024 (Tier-2 28% + Tier-3/4 46% of new room signings): hvs.com/article/10158, slides 4,9"),
      Ii("MahaRERA 50,162 registered projects: constructionworld.in (2025), slides 4,9"),
      Ii("K-RERA ~5,672 & Goa RERA ~1,250 (portal counts, secondary): 99acres.com/rera-registered-projects-in-karnataka-ffid; ...-in-goa-ffid, slides 4,9"),
      Ii("India wastewater treatment market USD 10.4 bn 2025: imarcgroup.com; plants market USD 1.33 bn 2024: techsciresearch.com (4514), slide 4"),
      G("COMPETITORS & PRICING"),
      Ii("Daiki Axis India (Johkasou; ₹200 cr Tumakuru plant): daikiaxis.in; biltraxmedia.com/daiki-axis-to-invest-200-inr-crore..., slides 4,6"),
      Ii("Ion Exchange INDION: ionexchangeglobal.com; Thermax FabX/BioCask: thermaxglobal.com, slide 4"),
      Ii("Banka BioLoo financials: screener.in/company/BANKA/consolidated/, slide 4"),
      Ii("SUSBIO ECOTREAT from ₹35k/KLD: susbio.in; susbio.in/stp-plant-cost-per-kld-in-india-2026/, slides 4,6"),
      Ii("Netsol Water / Kelvin (NCR): netsolwater.com/service-locations.php; kelvinindia.in, slide 4"),
      Ii("CDD Society DEWATS: cddindia.org; Boson Whitewater WaaS: zerodha.com/z-connect/rainmatter/introducing-boson-whitewater, slides 4,7"),
      Ii("Packaged-STP & AMC price benchmarks: studiomatrx.org/guides/stp-cost-per-kld-india; teamonebiotech.com (O&M 2026), slides 3,4,9"),
      Ii("DRDO bio-digester ToT licensees (49 firms, 2012): indiatvnews.com/news/india/drdo-licensing-eco-toilets-private-companies-16612.html, slide 4"),
      Ii("All URLs accessed 10 Sep 2026. Secondary sources marked; problem-statement-only figures cite the problem statement."),
    ];
    s.addText(colL, { x: 0.5, y: 1.40, w: 5.9, h: 5.55, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.12, valign: "top" });
    s.addText(colR, { x: 6.6, y: 1.40, w: 4.45, h: 5.55, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.12, valign: "top" });
    card(s, 11.25, 1.40, 1.58, 5.55, { fill: C.tint2, noShadow: true });
    s.addImage({ data: K("flask", BR), x: 11.38, y: 1.54, w: 0.26, h: 0.26 });
    s.addText([
      T("METHODOLOGY\n", { bold: true, color: C.brand, fontSize: 8.5 }),
      T("\nSizing: bottom-up per segment per state, as units x share lacking treatment x fit x conversion x ticket. No top-down report allocation.\n", { color: C.ink, fontSize: 7 }),
      T("\nScenarios: conversion, trigger-share, win-rate flexed; conservative = lowest defensible; upside = capacity-bound.\n", { color: C.ink, fontSize: 7 }),
      T("\nScoring: segmentation 10 factors / portfolio 7 criteria; weights on slides 3 & 7; evidence-based 1-5.\n", { color: C.ink, fontSize: 7 }),
      T("\nRounding: ₹cr to 1 decimal; estimates labelled; no false precision.", { color: C.ink, fontSize: 7 }),
    ], { x: 11.36, y: 1.86, w: 1.38, h: 5.0, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.05, valign: "top" });
    footer2(s, "", 8);
  })();

  /* ============ S9 BACKUP ============ */
  (() => {
    const s = pres.addSlide();
    s.background = { color: "FFFFFF" };
    header2(s, "", "Supporting material", "Glossary, assumptions ", "& calculation backup", 9);
    const y0 = 1.40;
    sec2(s, ICONS, "doc_" + BR, "Glossary", 0.5, y0, { w: 3, size: 12 });
    const gl = [
      ["STP / ETP", "Sewage / Effluent Treatment Plant"], ["KLD / MLD", "Kilo / Million Litres per Day"],
      ["MBBR", "Moving Bed Biofilm Reactor"], ["SBR", "Sequencing Batch Reactor"], ["MBR", "Membrane Bioreactor"],
      ["DEWATS", "Decentralised Wastewater Treatment Systems (nature-based)"], ["FRP", "Fibre-Reinforced Plastic"],
      ["O&M / AMC", "Operation & Maintenance / Annual Maintenance Contract"],
      ["TAM/SAM/SOM", "Total / Serviceable Addressable / Obtainable Market"], ["DSO", "Days Sales Outstanding"],
      ["ToT", "Transfer of Technology (DRDO licence)"], ["EC / OC", "Environmental Clearance / Occupancy Certificate"],
      ["CTE / CTO", "Consent to Establish / Operate (pollution boards)"], ["BMW Rules", "Bio-medical Waste Management Rules, 2016"],
      ["CGWA", "Central Ground Water Authority"], ["WaaS / BOOT", "Water-as-a-Service / Build-Own-Operate-Transfer"],
    ];
    s.addTable(gl.map(([a, bb]) => [
      cell(a, { bold: true, color: C.brandDk, fontSize: 7.1, fill: { color: C.tint2 } }),
      cell(bb, { fontSize: 7.1 }),
    ]), { x: 0.5, y: y0 + 0.32, w: 3.55, colW: [1.05, 2.50], autoPage: false });

    const ax = 4.35, aw = 8.43;
    sec2(s, ICONS, "chart_" + BR, "TAM build (annual, ₹cr): units × %lacking × fit × conversion × ticket", ax, y0, { w: 8.4, size: 12 });
    const A = (t, o = {}) => cell(t, Object.assign({ fontSize: 6.8, align: "center", valign: "middle" }, o));
    const AH = (t) => hcell(t, { fontSize: 7.0, align: "center" });
    const tam = [
      [AH("Segment"), AH("Eligible units (basis)"), AH("% lack"), AH("Fit"), AH("Conv./yr"), AH("Ticket ₹L"), AH("Proj./yr"), AH("₹cr/yr")],
      [A("Hospitality (≥20 keys)", { align: "left" }), A("4,000 stock (Goa DoT ~9,000 units; HVS Tier-2/3) + 110 new/yr", { align: "left" }), A("55%"), A("60%"), A("8% + new"), A("24-28"), A("166"), A("42.3")],
      [A("Residential developers", { align: "left" }), A("517 STP-trigger launches/yr (RERA run-rates × Tier-2/3 × trigger share)", { align: "left" }), A("n/a"), A("60%"), A("flow"), A("48"), A("310"), A("148.9")],
      [A("Housing societies (retrofit)", { align: "left" }), A("900 with failing/aged STPs", { align: "left" }), A("100%"), A("60%"), A("12%"), A("14"), A("65"), A("9.1")],
      [A("Hospitals >10 beds", { align: "left" }), A("5,500 private HCFs (BMW Rules base)", { align: "left" }), A("50%"), A("50%"), A("6%"), A("16"), A("82"), A("13.2")],
      [A("Education & CSR campuses", { align: "left" }), A("3,000 residential campuses", { align: "left" }), A("55%"), A("45%"), A("5%"), A("14"), A("37"), A("5.2")],
      [A("MSME industrial (compact ETP)", { align: "left" }), A("2,600 consented units, simple effluents", { align: "left" }), A("45%"), A("40%"), A("7%"), A("40"), A("33"), A("13.1")],
      [A("Commercial & mixed-use", { align: "left" }), A("1,200 properties", { align: "left" }), A("50%"), A("50%"), A("7%"), A("35"), A("21"), A("7.4")],
      [A("Homes (bio-digester)", { align: "left" }), A("220,000 new unsewered Tier-2/3 homes/yr", { align: "left" }), A("n/a"), A("2.5% adopt"), A("flow"), A("0.55"), A("5,500"), A("30.3")],
      [A("Homestays & small hospitality", { align: "left" }), A("3,500 stock", { align: "left" }), A("60%"), A("50%"), A("8%"), A("2.2"), A("84"), A("1.8")],
      [A("TOTAL TAM", { bold: true, align: "left", fill: { color: C.amberT } }), A("", { fill: { color: C.amberT } }), A("", { fill: { color: C.amberT } }), A("", { fill: { color: C.amberT } }), A("", { fill: { color: C.amberT } }), A("", { fill: { color: C.amberT } }), A("~6,300", { bold: true, fill: { color: C.amberT } }), A("271.2", { bold: true, fill: { color: C.amberT } })],
    ];
    s.addTable(tam, { x: ax, y: y0 + 0.32, w: aw, colW: [1.55, 2.80, 0.62, 0.62, 0.72, 0.72, 0.65, 0.75], autoPage: false });

    const by2 = y0 + 3.28;
    sec2(s, ICONS, "trend_" + BR, "SOM bridge, base case (₹cr)", ax, by2, { w: 3.7, size: 12 });
    const som = [
      [AH("₹cr"), AH("FY27"), AH("FY28"), AH("FY29")],
      [A("Existing base (+5%/yr)", { align: "left" }), A("12.3"), A("12.9"), A("13.5")],
      [A("New private-market", { align: "left" }), A("2.4"), A("6.4"), A("11.9")],
      [A("Total revenue", { align: "left", bold: true }), A("14.7", { bold: true }), A("19.3", { bold: true }), A("25.4", { bold: true })],
    ];
    s.addTable(som, { x: ax, y: by2 + 0.32, w: 3.6, colW: [1.65, 0.65, 0.65, 0.65], autoPage: false });

    sec2(s, ICONS, "star_" + AM, "Adjacency scoring, top 5 of 10 (Cap & Op inverse: 5 = low)", 8.15, by2, { w: 4.6, size: 11 });
    const AJ = (t, o = {}) => cell(t, Object.assign({ fontSize: 6.2, align: "center", valign: "middle" }, o));
    const AJH = (t) => hcell(t, { fontSize: 6.3, align: "center" });
    const adj = [
      [AJH("Option"), AJH("D20"), AJH("S20"), AJH("C15"), AJH("M15"), AJH("O10"), AJH("T10"), AJH("R10"), AJH("Wtd")],
      [AJ("STP retrofit + O&M", { align: "left" }), AJ("5"), AJ("5"), AJ("5"), AJ("4"), AJ("3"), AJ("5"), AJ("5"), AJ("4.65", { bold: true, fill: { color: C.amberT } })],
      [AJ("IoT monitoring", { align: "left" }), AJ("4"), AJ("5"), AJ("5"), AJ("4"), AJ("4"), AJ("5"), AJ("5"), AJ("4.55", { bold: true, fill: { color: C.amberT } })],
      [AJ("Water-reuse module", { align: "left" }), AJ("5"), AJ("5"), AJ("4"), AJ("4"), AJ("3"), AJ("4"), AJ("4"), AJ("4.30", { bold: true, fill: { color: C.amberT } })],
      [AJ("Greywater recycling", { align: "left" }), AJ("3"), AJ("4"), AJ("4"), AJ("3"), AJ("4"), AJ("4"), AJ("3"), AJ("3.55")],
      [AJ("Advanced disinfection", { align: "left" }), AJ("3"), AJ("4"), AJ("4"), AJ("3"), AJ("4"), AJ("4"), AJ("3"), AJ("3.55")],
    ];
    s.addTable(adj, { x: 8.15, y: by2 + 0.32, w: 4.63, colW: [1.43, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.60], autoPage: false });

    card(s, ax, by2 + 1.72, 8.43, 0.78, { fill: C.tint2, noShadow: true });
    s.addText([
      T("FY29 new-business mix: ", { bold: true, color: C.brandDk, fontSize: 7.4 }),
      T("26 STP/ETP (avg ₹32 L) ₹8.3 cr + 8 retrofits ₹1.0 cr + ~230 bio-digesters ₹1.8 cr + AMC/monitoring/O&M ₹0.8 cr = ₹11.9 cr.  ", { color: C.ink, fontSize: 7.4 }),
      T("Working capital: ", { bold: true, color: C.brandDk, fontSize: 7.4 }),
      T("at 75 receivable days that is ₹5.2 cr locked up, against net worth above ₹12 cr plus IPO working capital.  ", { color: C.ink, fontSize: 7.4 }),
      T("Segment scores: ", { bold: true, color: C.brandDk, fontSize: 7.4 }),
      T("hoteliers 4.50 · developers 3.80 · hospitals 3.75 · homeowners 3.45 · societies 3.20 · MSME 3.20 · schools 3.05 · commercial 3.05.", { color: C.ink, fontSize: 7.4 }),
    ], { x: ax + 0.12, y: by2 + 1.78, w: 8.2, h: 0.66, isTextBox: true, margin: 0, fontFace: F, lineSpacingMultiple: 1.06, valign: "top" });

    footer2(s, "All FY27-29 figures are team estimates; stock counts marked 'est.' are transparent proxies built from the sources on p.8 (RERA portals, Goa DoT, HVS-ANAROCK, BMW Rules registers).", 9);
  })();

  await pres.writeFile({ fileName: "CaseConsilium_Wookies.pptx" });
  console.log("deck v2 written");
}

main().catch(e => { console.error(e); process.exit(1); });
