// NAADI v2, India Chem 2026 Youth Innovation Challenge concept deck (8 slides).
// Team: Raunak Jain and Anushriya Bhattacharya, NIT Warangal.
// Purple-led redesign on white. DRAFT for team review and ratification.
// Build: node build_deck_v2.cjs -> India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx
// House rule: no em dashes and no en dashes anywhere in this deck.

const pptxgen = require("pptxgenjs");

const PURPLE = "5B2A86";
const PURPLE2 = "7A4AA5";
const LAV = "EFE8F6";
const LAV2 = "F8F5FA";
const INK = "17131D";
const INK2 = "625D68";
const BORDER = "DED9E5";
const GREEN = "2F7D69";
const AMBER = "C8792A";
const WHITE = "FFFFFF";
const FONT = "Arial";

const W = 13.333, H = 7.5, MX = 0.55, CW = W - 2 * MX;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Raunak Jain, Anushriya Bhattacharya, NIT Warangal";
pres.title = "NAADI: plant-owned predictive maintenance for critical pumps";

let pageNo = 0;
function newSlide() {
  pageNo += 1;
  const s = pres.addSlide();
  s.background = { color: WHITE };
  return s;
}

function footer(s) {
  s.addText("India Chem 2026 · NIT Warangal", {
    x: MX, y: 7.2, w: 5, h: 0.2, fontFace: FONT, fontSize: 8.5, color: INK2,
    isTextBox: true, margin: 0,
  });
  s.addText(`${pageNo} / 8`, {
    x: W - MX - 0.8, y: 7.2, w: 0.8, h: 0.2, fontFace: FONT, fontSize: 8.5,
    color: INK2, align: "right", isTextBox: true, margin: 0,
  });
}

function sectionTag(s, text) {
  s.addText(text, {
    x: MX, y: 0.22, w: 6, h: 0.22, fontFace: FONT, fontSize: 10, bold: true,
    color: PURPLE2, isTextBox: true, margin: 0,
  });
}

// Title with one purple phrase. runs: [{t, p?}]
function slideTitle(s, runs, h = 1.0, size = 27) {
  s.addText(runs.map(r => ({
    text: r.t, options: { color: r.p ? PURPLE : INK, bold: true },
  })), {
    x: MX, y: 0.46, w: CW, h, fontFace: FONT, fontSize: size,
    isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.03,
  });
}

function txt(s, text, o) {
  s.addText(text, {
    fontFace: FONT, isTextBox: true, margin: 0, valign: "top",
    color: INK, lineSpacingMultiple: 1.05, ...o,
  });
}

function rect(s, x, y, w, h, fill, line) {
  s.addShape(pres.ShapeType.rect, {
    x, y, w, h,
    fill: fill ? { color: fill } : { color: WHITE },
    line: line === null ? { type: "none" } : (line || { color: BORDER, width: 0.75 }),
  });
}

function hline(s, x, y, w, color = BORDER, width = 0.75, dash) {
  s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color, width, dashType: dash || "solid" } });
}
function vline(s, x, y, h, color = BORDER, width = 0.75, dash) {
  s.addShape(pres.ShapeType.line, { x, y, w: 0, h, line: { color, width, dashType: dash || "solid" } });
}
function arrowR(s, x, y, w, color = PURPLE, width = 1.75) {
  s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color, width, endArrowType: "triangle" } });
}
function arrowD(s, x, y, h, color = PURPLE, width = 1.75) {
  s.addShape(pres.ShapeType.line, { x, y, w: 0, h, line: { color, width, endArrowType: "triangle" } });
}

function estTag(s, x, y, w, kind = "Team estimate", color = AMBER) {
  txt(s, kind, { x, y, w, h: 0.16, fontSize: 8, color, bold: false });
}

// small thin-line icon inside a 0.34 box: variants drawn from primitives
function icon(s, x, y, kind, color = PURPLE) {
  const L = { color, width: 1.4 };
  switch (kind) {
    case "signal": // dot + two arcs approximated by short slanted lines
      s.addShape(pres.ShapeType.ellipse, { x: x + 0.03, y: y + 0.2, w: 0.09, h: 0.09, fill: { color }, line: { type: "none" } });
      s.addShape(pres.ShapeType.line, { x: x + 0.15, y: y + 0.1, w: 0.1, h: 0.1, line: L, flipV: true });
      s.addShape(pres.ShapeType.line, { x: x + 0.15, y: y + 0.22, w: 0.1, h: 0.1, line: L });
      s.addShape(pres.ShapeType.line, { x: x + 0.24, y: y + 0.04, w: 0.09, h: 0.12, line: L, flipV: true });
      s.addShape(pres.ShapeType.line, { x: x + 0.24, y: y + 0.26, w: 0.09, h: 0.12, line: L });
      break;
    case "features": // three mini bars
      s.addShape(pres.ShapeType.rect, { x: x + 0.02, y: y + 0.18, w: 0.07, h: 0.16, fill: { color }, line: { type: "none" } });
      s.addShape(pres.ShapeType.rect, { x: x + 0.13, y: y + 0.08, w: 0.07, h: 0.26, fill: { color }, line: { type: "none" } });
      s.addShape(pres.ShapeType.rect, { x: x + 0.24, y: y + 0.13, w: 0.07, h: 0.21, fill: { color }, line: { type: "none" } });
      break;
    case "data": // square + inner dot
      s.addShape(pres.ShapeType.rect, { x: x + 0.03, y: y + 0.06, w: 0.28, h: 0.28, fill: { color: WHITE }, line: L });
      s.addShape(pres.ShapeType.ellipse, { x: x + 0.13, y: y + 0.16, w: 0.08, h: 0.08, fill: { color }, line: { type: "none" } });
      break;
    case "retrofit": // circle + down arrow into it
      s.addShape(pres.ShapeType.ellipse, { x: x + 0.05, y: y + 0.14, w: 0.24, h: 0.2, fill: { color: WHITE }, line: L });
      s.addShape(pres.ShapeType.line, { x: x + 0.17, y: y + 0.0, w: 0, h: 0.16, line: { color, width: 1.4, endArrowType: "triangle" } });
      break;
    case "cmms": // two rects linked
      s.addShape(pres.ShapeType.rect, { x: x + 0.02, y: y + 0.08, w: 0.12, h: 0.1, fill: { color: WHITE }, line: L });
      s.addShape(pres.ShapeType.rect, { x: x + 0.2, y: y + 0.22, w: 0.12, h: 0.1, fill: { color: WHITE }, line: L });
      s.addShape(pres.ShapeType.line, { x: x + 0.14, y: y + 0.13, w: 0.09, h: 0.14, line: L });
      break;
    case "check":
      s.addShape(pres.ShapeType.line, { x: x + 0.04, y: y + 0.2, w: 0.09, h: 0.09, line: { color, width: 1.8 } });
      s.addShape(pres.ShapeType.line, { x: x + 0.12, y: y + 0.08, w: 0.16, h: 0.21, line: { color, width: 1.8 }, flipV: true });
      break;
  }
}

// mini waveform: sequence of line segments inside width w
function waveform(s, x, y, w, color = PURPLE2, amp = 0.16, width = 1.6) {
  const pts = [0, 0.35, -0.5, 0.8, -1, 1, -0.4, 0.55, -0.7, 0.2];
  const seg = w / (pts.length - 1);
  for (let i = 0; i < pts.length - 1; i++) {
    const y1 = y + pts[i] * amp, y2 = y + pts[i + 1] * amp;
    s.addShape(pres.ShapeType.line, {
      x: x + i * seg, y: Math.min(y1, y2), w: seg, h: Math.abs(y2 - y1) || 0.008,
      line: { color, width }, flipV: pts[i + 1] < pts[i],
    });
  }
}

// simplified centrifugal pump drawing (thin line), origin x,y, ~w 1.9 x h 1.15
function pumpDrawing(s, x, y, scale = 1) {
  const L = { color: INK2, width: 1.4 };
  const k = scale;
  // volute casing
  s.addShape(pres.ShapeType.ellipse, { x, y: y + 0.15 * k, w: 0.85 * k, h: 0.85 * k, fill: { color: WHITE }, line: L });
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.3 * k, y: y + 0.45 * k, w: 0.25 * k, h: 0.25 * k, fill: { color: LAV }, line: { color: INK2, width: 1 } });
  // discharge nozzle (up)
  s.addShape(pres.ShapeType.rect, { x: x + 0.3 * k, y, w: 0.25 * k, h: 0.18 * k, fill: { color: WHITE }, line: L });
  // shaft
  s.addShape(pres.ShapeType.rect, { x: x + 0.85 * k, y: y + 0.5 * k, w: 0.55 * k, h: 0.14 * k, fill: { color: WHITE }, line: L });
  // motor
  s.addShape(pres.ShapeType.rect, { x: x + 1.4 * k, y: y + 0.32 * k, w: 0.5 * k, h: 0.5 * k, fill: { color: LAV2 }, line: L });
  // bearing sensor dots: DE (near pump), NDE (far end of motor)
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.88 * k, y: y + 0.36 * k, w: 0.1 * k, h: 0.1 * k, fill: { color: PURPLE }, line: { type: "none" } });
  s.addShape(pres.ShapeType.ellipse, { x: x + 1.78 * k, y: y + 0.2 * k, w: 0.1 * k, h: 0.1 * k, fill: { color: PURPLE }, line: { type: "none" } });
}

// =====================================================================
// SLIDE 1 : Title
// =====================================================================
{
  const s = newSlide();
  vline(s, MX, 0.55, 5.6, PURPLE, 2.5);

  txt(s, "India Chem 2026 Youth Innovation Challenge", {
    x: MX + 0.3, y: 0.55, w: 7, h: 0.28, fontSize: 12.5, bold: true, color: PURPLE2,
  });

  txt(s, "NAADI", { x: MX + 0.28, y: 1.05, w: 6.5, h: 1.05, fontSize: 60, bold: true, color: PURPLE });
  txt(s, "Plant-owned predictive maintenance for critical pumps", {
    x: MX + 0.3, y: 2.2, w: 5.9, h: 0.85, fontSize: 22, bold: true, color: INK, lineSpacingMultiple: 1.05,
  });
  txt(s, "A six-month pilot to test early fault detection across 25 critical pumps in a mid-sized speciality chemicals plant.", {
    x: MX + 0.3, y: 3.15, w: 5.7, h: 0.75, fontSize: 14.5, color: INK2, lineSpacingMultiple: 1.15,
  });
  txt(s, [
    { text: "Annexure problem statement: ", options: { bold: true, color: INK2 } },
    { text: "AI-driven predictive maintenance to improve asset reliability and maintenance efficiency in the chemicals and petrochemicals sector [1]", options: { color: INK2 } },
  ], { x: MX + 0.3, y: 4.1, w: 5.7, h: 0.7, fontSize: 10.5, lineSpacingMultiple: 1.1 });

  // right infographic: pump -> sensors -> waveform -> gateway -> alert
  const px = 7.1, py = 1.0, pw = 5.65, ph = 4.55;
  rect(s, px, py, pw, ph, LAV2, null);
  txt(s, "From bearing vibration to a drafted work order", {
    x: px + 0.3, y: py + 0.2, w: pw - 0.6, h: 0.24, fontSize: 11, bold: true, color: INK,
  });
  pumpDrawing(s, px + 0.35, py + 0.75, 1.15);
  txt(s, "DE", { x: px + 1.28, y: py + 1.32, w: 0.4, h: 0.16, fontSize: 8, color: PURPLE, bold: true });
  txt(s, "NDE", { x: px + 2.3, y: py + 0.85, w: 0.5, h: 0.16, fontSize: 8, color: PURPLE, bold: true });
  txt(s, "centrifugal pump with vibration and temperature sensors on both bearing housings", {
    x: px + 0.35, y: py + 2.05, w: 2.6, h: 0.5, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.05,
  });

  waveform(s, px + 0.4, py + 3.0, 2.4, PURPLE2, 0.2);
  txt(s, "vibration signature, sampled continuously", { x: px + 0.4, y: py + 3.3, w: 2.5, h: 0.2, fontSize: 8.5, color: INK2 });

  arrowR(s, px + 2.95, py + 1.5, 0.4);
  rect(s, px + 3.45, py + 1.15, 1.85, 0.75, WHITE);
  txt(s, "Area gateway", { x: px + 3.6, y: py + 1.26, w: 1.6, h: 0.2, fontSize: 10.5, bold: true, color: INK });
  txt(s, "edge feature extraction", { x: px + 3.6, y: py + 1.48, w: 1.6, h: 0.34, fontSize: 8.5, color: INK2 });

  arrowD(s, px + 4.37, py + 1.95, 0.5);
  rect(s, px + 3.45, py + 2.5, 1.85, 1.15, WHITE);
  txt(s, "Maintenance alert", { x: px + 3.6, y: py + 2.62, w: 1.6, h: 0.2, fontSize: 10.5, bold: true, color: INK });
  s.addShape(pres.ShapeType.ellipse, { x: px + 3.6, y: py + 2.93, w: 0.09, h: 0.09, fill: { color: GREEN }, line: { type: "none" } });
  txt(s, "bearing wear trend rising: work order drafted for the reliability engineer", {
    x: px + 3.74, y: py + 2.87, w: 1.5, h: 0.7, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.08,
  });
  arrowR(s, px + 2.9, py + 3.0, 0.45, PURPLE2, 1.4);

  // bottom strip
  hline(s, MX, 6.35, CW, BORDER, 1);
  txt(s, [
    { text: "Raunak Jain", options: { bold: true, color: INK } },
    { text: "   B.Tech Mechanical Engineering", options: { color: INK2 } },
  ], { x: MX, y: 6.55, w: 4.4, h: 0.25, fontSize: 12 });
  txt(s, [
    { text: "Anushriya Bhattacharya", options: { bold: true, color: INK } },
    { text: "   B.Tech Chemical Engineering", options: { color: INK2 } },
  ], { x: 5.0, y: 6.55, w: 4.7, h: 0.25, fontSize: 12 });
  txt(s, "National Institute of Technology Warangal", {
    x: 9.85, y: 6.55, w: 2.95, h: 0.4, fontSize: 12, bold: true, color: PURPLE, align: "right", lineSpacingMultiple: 1.02,
  });
  footer(s);

  s.addNotes(
    "Good morning. We are Raunak Jain, mechanical engineering, and Anushriya Bhattacharya, chemical engineering, from NIT Warangal. " +
    "Our proposal is NAADI, a predictive maintenance system for the critical pumps of a chemical plant. " +
    "The idea in one sentence: continuous vibration sensing on a plant's 25 most failure-prone pumps, with interpretable machine learning that drafts work orders for the reliability engineer, while all data and models stay on the plant's own network. " +
    "We are proposing a six-month pilot. The base-case economics, a public benchmark validation of our prototype, and the pilot design follow in the next seven slides. About 60 seconds.");
}

// =====================================================================
// SLIDE 2 : Existing problem
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Existing scenario");
  slideTitle(s, [
    { t: "Twenty-five critical pumps can put nearly " },
    { t: "₹1.4 crore", p: true },
    { t: " of annual production value at risk" },
  ], 0.95, 26);

  // ---- left: asset filtering funnel
  const fx = MX, fy = 1.72, fw = 3.55;
  txt(s, "Where the risk concentrates", { x: fx, y: fy - 0.24, w: fw, h: 0.22, fontSize: 12, bold: true, color: INK });
  const steps = [
    { w: 2.95, fill: LAV2, ink: INK, t: "≈200 pumps in the plant", tag: "Plant assumption" },
    { w: 2.35, fill: LAV, ink: INK, t: "25 critical bad-actor pumps", tag: "Pilot scope" },
    { w: 1.85, fill: PURPLE2, ink: WHITE, t: "60 outage hours per year", tag: "Team estimate" },
    { w: 1.5, fill: PURPLE, ink: WHITE, t: "≈₹1.4 crore annual exposure", tag: "Team calculation" },
  ];
  const fcx = fx + 1.55; // funnel centre line (bars centred here, tags to the right)
  let yy = fy + 0.05;
  steps.forEach((st, i) => {
    const x = fcx - st.w / 2;
    rect(s, x, yy, st.w, 0.62, st.fill, i < 2 ? { color: BORDER, width: 0.75 } : null);
    txt(s, st.t, { x: x + 0.08, y: yy + 0.06, w: st.w - 0.16, h: 0.52, fontSize: 10, bold: i >= 2, color: st.ink, align: "center", valign: "middle", lineSpacingMultiple: 1.0 });
    txt(s, st.tag, { x: fcx + 1.55, y: yy + 0.14, w: 1.35, h: 0.4, fontSize: 7.5, color: i >= 2 ? (i === 3 ? INK2 : AMBER) : INK2, lineSpacingMultiple: 1.0 });
    if (i < 3) vline(s, fcx, yy + 0.62, 0.16, PURPLE2, 1.2);
    yy += 0.78;
  });

  // ---- middle: failure pathway
  const mx2 = 4.85, my = 1.72, mw = 3.35;
  txt(s, "How a routine fault becomes an outage", { x: mx2, y: my - 0.24, w: mw, h: 0.22, fontSize: 12, bold: true, color: INK });
  const path = [
    "Bearing or seal degradation begins [4]",
    "Monthly inspection misses the developing fault",
    "Pump trips without warning",
    "Production interruption",
    "Emergency repair and restart",
  ];
  let py2 = my + 0.05;
  path.forEach((p, i) => {
    const last = i === path.length - 1;
    rect(s, mx2, py2, mw, 0.5, last ? LAV : WHITE, last ? null : { color: BORDER, width: 0.75 });
    txt(s, p, { x: mx2 + 0.12, y: py2 + 0.04, w: mw - 0.24, h: 0.42, fontSize: 10, color: INK, valign: "middle", lineSpacingMultiple: 1.0 });
    if (!last) arrowD(s, mx2 + mw / 2, py2 + 0.5, 0.14, PURPLE2, 1.2);
    py2 += 0.64;
  });

  // ---- right: 89% statistic + implication
  const rx = 8.75, ry = 1.62, rw = 4.0;
  txt(s, "89%", { x: rx, y: ry, w: 2.0, h: 0.62, fontSize: 40, bold: true, color: PURPLE });
  txt(s, "of failure modes in the foundational reliability study for RCM showed no predictable wear-out age [3]", {
    x: rx + 1.5, y: ry + 0.1, w: rw - 1.5, h: 0.75, fontSize: 10, color: INK2, lineSpacingMultiple: 1.08,
  });
  txt(s, "Fixed-interval maintenance cannot anticipate faults that arrive at random. Bearing and seal problems develop over days to weeks [4]; that window is where condition data helps.", {
    x: rx, y: ry + 0.95, w: rw, h: 1.0, fontSize: 11.5, color: INK, lineSpacingMultiple: 1.12,
  });
  rect(s, rx, ry + 2.1, rw, 1.0, LAV2, null);
  txt(s, [
    { text: "What NAADI must do: ", options: { bold: true, color: PURPLE } },
    { text: "flag developing faults on these 25 pumps about two weeks before failure and turn each one into a planned work order.", options: { color: INK } },
  ], { x: rx + 0.15, y: ry + 2.2, w: rw - 0.3, h: 0.8, fontSize: 11, lineSpacingMultiple: 1.1, valign: "middle" });

  // ---- bottom KPI strip
  const ky = 5.6;
  hline(s, MX, ky, CW, BORDER, 1);
  const kpis = [
    ["60 h/yr", "unplanned outage from these pumps", "Team estimate", AMBER],
    ["₹1.9 lakh/h", "contribution margin lost while down", "Team calculation", INK2],
    ["12 events/yr", "pump repairs across the 25 units", "Team estimate", AMBER],
    ["≈₹1.4 Cr", "annual exposure, margin plus repairs", "Team calculation", INK2],
  ];
  const kw = CW / 4;
  kpis.forEach((k, i) => {
    const x = MX + i * kw;
    if (i > 0) vline(s, x, ky + 0.18, 1.05, BORDER, 0.75);
    txt(s, k[0], { x: x + (i ? 0.22 : 0), y: ky + 0.16, w: kw - 0.3, h: 0.4, fontSize: 23, bold: true, color: PURPLE });
    txt(s, k[1], { x: x + (i ? 0.22 : 0), y: ky + 0.6, w: kw - 0.35, h: 0.36, fontSize: 9.5, color: INK2, lineSpacingMultiple: 1.02 });
    txt(s, k[2], { x: x + (i ? 0.22 : 0), y: ky + 0.98, w: kw - 0.35, h: 0.16, fontSize: 8, color: k[3] });
  });
  footer(s);

  s.addNotes(
    "The use case is one representative mid-sized speciality chemicals plant, and inside it the 25 pumps whose trips actually stop production. " +
    "The funnel on the left shows the filtering: about 200 pumps, 25 critical ones, an estimated 60 outage hours a year, and roughly 1.4 crore of annual exposure once lost margin and repairs are added. " +
    "These plant figures are labelled estimates and the pilot's first phase replaces them with the plant's own 24-month history. " +
    "The middle shows why this keeps happening: monthly inspection rounds leave long blind windows, and the foundational reliability study found 89 percent of failure modes have no predictable wear-out age, so calendar-based maintenance misses them. " +
    "Bearing and seal problems develop over days to weeks. That is the window NAADI is designed to use. About 70 seconds.");
}

// =====================================================================
// SLIDE 3 : Global practices and the gap
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Global best practices");
  slideTitle(s, [
    { t: "Continuous monitoring works, but " },
    { t: "proprietary systems remain difficult", p: true },
    { t: " for mid-sized plants to adopt" },
  ], 0.95, 26);

  // ---- left: weighted matrix
  const tx = MX, ty = 1.85, tw = 6.9;
  txt(s, "Five approaches, six weighted criteria", { x: tx, y: ty - 0.26, w: tw, h: 0.22, fontSize: 12, bold: true, color: INK });
  const hd = { fill: { color: WHITE }, color: INK, bold: true, fontSize: 8.5, valign: "middle" };
  const c = (t, o = {}) => ({ text: t, options: { fontFace: FONT, fontSize: 9, color: INK, valign: "middle", ...o } });
  const rows = [
    [c("Approach", hd), c("Lead time (30)", hd), c("Cost (20)", hd), c("Skill need (10)", hd), c("Data control (10)", hd), c("Retrofit (10)", hd), c("MSME fit (20)", hd)],
    [c("Run to failure"), c("none"), c("poor"), c("low"), c("n/a"), c("n/a"), c("poor")],
    [c("Calendar preventive (common in India)"), c("none for random faults"), c("medium"), c("low"), c("n/a"), c("n/a"), c("medium")],
    [c("Monthly offline vibration rounds"), c("up to route interval"), c("medium"), c("high"), c("plant"), c("good"), c("poor")],
    [c("OEM cloud monitoring"), c("days to weeks"), c("high"), c("low"), c("vendor silo"), c("medium"), c("poor")],
    [c("NAADI: on-site continuous stack", { bold: true, color: PURPLE, fill: { color: LAV } }), c("days to weeks", { bold: true, fill: { color: LAV } }), c("low to medium", { bold: true, fill: { color: LAV } }), c("medium", { bold: true, fill: { color: LAV } }), c("plant", { bold: true, color: PURPLE, fill: { color: LAV } }), c("good", { bold: true, fill: { color: LAV } }), c("good", { bold: true, color: PURPLE, fill: { color: LAV } })],
  ];
  s.addTable(rows, {
    x: tx, y: ty, w: tw, colW: [1.9, 1.0, 0.85, 0.8, 0.85, 0.7, 0.8],
    border: { type: "solid", color: BORDER, pt: 0.5 },
    fontFace: FONT, rowH: 0.34, margin: 0.05, autoPage: false,
  });
  // highlight proposed row background
  rect(s, tx, ty + 0.34 * 5 + 0.34, 0, 0, WHITE, null); // no-op keeper
  txt(s, "Weights in brackets, sum 100. Scores and marks are team judgement based on the documented behaviour of each approach class [2][6].", {
    x: tx, y: ty + 2.55, w: tw, h: 0.4, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.05,
  });

  // ---- right: weighted score bars
  const bx = 7.85, by = 1.85, bw = 4.9;
  txt(s, "Weighted score out of 5", { x: bx, y: by - 0.26, w: bw, h: 0.22, fontSize: 12, bold: true, color: INK });
  const scores = [
    ["Run to failure", 2.3, BORDER, INK2],
    ["Calendar preventive", 3.0, BORDER, INK2],
    ["Offline vibration rounds", 2.9, BORDER, INK2],
    ["OEM cloud monitoring", 2.9, BORDER, INK2],
    ["NAADI on-site stack", 4.3, PURPLE, PURPLE],
  ];
  const track = 2.55, bh = 0.26;
  scores.forEach((sc, i) => {
    const y = by + 0.08 + i * 0.47;
    txt(s, sc[0], { x: bx, y: y + 0.02, w: 1.85, h: 0.4, fontSize: 9.5, color: sc[3] === PURPLE ? PURPLE : INK, bold: sc[3] === PURPLE, lineSpacingMultiple: 0.95 });
    rect(s, bx + 1.9, y, track, bh, LAV2, null);
    rect(s, bx + 1.9, y, track * sc[1] / 5, bh, sc[2], null);
    txt(s, sc[1].toFixed(1), { x: bx + 1.9 + track + 0.08, y: y + 0.015, w: 0.45, h: 0.24, fontSize: 10.5, bold: true, color: sc[3] });
  });
  txt(s, "The gap is not sensing or algorithms. It is cost, data control and fit for mid-sized plants.", {
    x: bx, y: by + 2.5, w: bw, h: 0.55, fontSize: 11, color: INK, lineSpacingMultiple: 1.1,
  });

  // ---- bottom: design choices strip
  const dy = 5.75;
  hline(s, MX, dy - 0.12, CW, BORDER, 1);
  txt(s, "Design choices", { x: MX, y: dy, w: 2.2, h: 0.5, fontSize: 13, bold: true, color: PURPLE });
  const choices = [
    ["signal", "Continuous sensing", "no month-long blind windows"],
    ["features", "Explainable vibration features", "auditable by plant engineers"],
    ["data", "Plant-controlled data", "no vendor silo"],
    ["retrofit", "Retrofit installation", "no shutdown, no cabling"],
    ["cmms", "Connection to the existing CMMS", "alerts become work orders"],
  ];
  const cwid = (CW - 2.2) / 5;
  choices.forEach((ch, i) => {
    const x = MX + 2.2 + i * cwid;
    icon(s, x, dy + 0.02, ch[0]);
    txt(s, ch[1], { x: x + 0.42, y: dy, w: cwid - 0.5, h: 0.42, fontSize: 9.5, bold: true, color: INK, lineSpacingMultiple: 0.95 });
    txt(s, ch[2], { x: x + 0.42, y: dy + 0.44, w: cwid - 0.5, h: 0.42, fontSize: 8.5, color: INK2, lineSpacingMultiple: 0.98 });
  });
  footer(s);

  s.addNotes(
    "We compared five realistic approaches on the six criteria that decide adoption, weighting detection lead time and fit for mid-sized plants highest. " +
    "Run to failure and calendar-based maintenance give no lead time for random faults, and calendar maintenance is still the common practice in Indian plants. " +
    "Monthly offline vibration rounds help but leave blind windows of several weeks and depend on scarce analysts. " +
    "OEM cloud monitoring is the global best practice and it works, but it scores poorly here on total cost and on data control, because the plant's condition history ends up in a vendor system. " +
    "So the gap is architectural rather than technical. That analysis gives the five design choices at the bottom, and those choices define NAADI. " +
    "The scores are our judgement and are labelled as such. About 65 seconds.");
}

// =====================================================================
// SLIDE 4 : Proposed solution architecture
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Proposed solution");
  slideTitle(s, [
    { t: "NAADI links vibration sensing to maintenance action " },
    { t: "while keeping operational data on site", p: true },
  ], 0.9, 26);

  // architecture field
  const ax = MX, ay = 1.6, aw = CW, ah = 3.9;
  rect(s, ax, ay, aw, ah, LAV2, null);
  s.addShape(pres.ShapeType.rect, { x: ax, y: ay, w: aw, h: ah, fill: { type: "none" }, line: { color: BORDER, width: 1, dashType: "dash" } });
  txt(s, "All data and models stay on the plant network", {
    x: ax + aw - 3.4, y: ay + 0.1, w: 3.25, h: 0.2, fontSize: 9, color: INK2, align: "right",
  });

  const nodeW = 2.18, nodeH = 1.02, gap = 0.5;
  function node(x, y, head, sub, accent) {
    rect(s, x, y, nodeW, nodeH, WHITE, { color: accent || BORDER, width: accent ? 1.5 : 0.9 });
    txt(s, head, { x: x + 0.11, y: y + 0.08, w: nodeW - 0.22, h: 0.4, fontSize: 10.5, bold: true, color: INK, lineSpacingMultiple: 0.95 });
    txt(s, sub, { x: x + 0.11, y: y + 0.46, w: nodeW - 0.22, h: 0.52, fontSize: 8, color: INK2, lineSpacingMultiple: 1.0 });
  }

  // row A (left to right)
  const rowAy = ay + 0.55;
  pumpDrawing(s, ax + 0.3, rowAy + 0.05, 0.95);
  txt(s, "critical pump, DE and NDE sensor points", { x: ax + 0.25, y: rowAy + 1.15, w: 2.0, h: 0.35, fontSize: 8, color: INK2, lineSpacingMultiple: 1.0 });
  arrowR(s, ax + 2.35, rowAy + 0.5, 0.35);
  node(ax + 2.75, rowAy, "Vibration + temperature sensors", "wireless, on both bearing housings; hardware meeting applicable PESO and IECEx requirements [10]");
  arrowR(s, ax + 2.75 + nodeW + 0.03, rowAy + 0.5, gap - 0.06);
  node(ax + 2.75 + nodeW + gap, rowAy, "Area gateway", "one per plant area; buffers data locally");
  arrowR(s, ax + 2.75 + 2 * (nodeW + gap) - gap + nodeW + 0.03 - nodeW, rowAy + 0.5, gap - 0.06);
  node(ax + 2.75 + 2 * (nodeW + gap), rowAy, "Edge feature extraction", "16 vibration indicators per window, per ISO 13374 [6]");
  // corner elbow down to row B
  const lastAx = ax + 2.75 + 2 * (nodeW + gap);
  const rowBy = ay + 2.3;
  s.addShape(pres.ShapeType.line, { x: lastAx + nodeW + 0.03, y: rowAy + 0.5, w: 0.29, h: 0, line: { color: PURPLE, width: 1.75 } });
  s.addShape(pres.ShapeType.line, { x: lastAx + nodeW + 0.32, y: rowAy + 0.5, w: 0, h: rowBy + 0.5 - (rowAy + 0.5), line: { color: PURPLE, width: 1.75 } });
  s.addShape(pres.ShapeType.line, { x: lastAx + nodeW + 0.06, y: rowBy + 0.5, w: 0.26, h: 0, line: { color: PURPLE, width: 1.75, beginArrowType: "triangle" } });

  // row B (right to left)
  const bx4 = lastAx; // classification under edge features
  node(bx4, rowBy, "Anomaly + fault classification", "per-pump anomaly score and fault type; benchmark result on slide 5 [5]");
  const bx3 = bx4 - nodeW - gap;
  const bx2 = bx3 - nodeW - gap;
  const bx1 = bx2 - nodeW - gap;
  node(bx3, rowBy, "Reliability dashboard", "trends, alarm zones per ISO 20816-3 [6]");
  node(bx2, rowBy, "CMMS work order", "drafted automatically in the plant's existing system");
  node(bx1, rowBy, "Engineer validation", "accepts or rejects every action; nothing is automatic", GREEN);
  icon(s, bx1 + nodeW - 0.42, rowBy + 0.06, "check", GREEN);
  // right-to-left arrows (beginArrowType so head points left)
  [bx3, bx2, bx1].forEach((xx) => {
    s.addShape(pres.ShapeType.line, {
      x: xx + nodeW + 0.06, y: rowBy + 0.5, w: gap - 0.12, h: 0,
      line: { color: PURPLE, width: 1.75, beginArrowType: "triangle" },
    });
  });
  // feedback dashed: engineer validation up to classification
  s.addShape(pres.ShapeType.line, { x: bx1 + 0.5, y: rowBy + nodeH + 0.06, w: 0, h: 0.28, line: { color: PURPLE2, width: 1.25, dashType: "dash" } });
  s.addShape(pres.ShapeType.line, { x: bx1 + 0.5, y: rowBy + nodeH + 0.34, w: bx4 + 1.2 - bx1 - 0.5, h: 0, line: { color: PURPLE2, width: 1.25, dashType: "dash" } });
  s.addShape(pres.ShapeType.line, { x: bx4 + 1.2, y: rowBy + nodeH + 0.06, w: 0, h: 0.28, line: { color: PURPLE2, width: 1.25, dashType: "dash", beginArrowType: "triangle" } });
  txt(s, "confirmed maintenance findings retrain the model and tighten alarm limits", {
    x: bx1 + 0.75, y: rowBy + nodeH + 0.16, w: 5.4, h: 0.2, fontSize: 8.5, color: INK2,
  });

  // bottom three modules
  const my2 = 5.85;
  const mods = [
    ["data", "Open data protocols", "OPC UA and standard historian interfaces; nothing proprietary between plant and models"],
    ["features", "Interpretable features", "every model input is a standard vibration indicator an engineer can check"],
    ["check", "Human-approved action", "no maintenance decision changes without the reliability engineer's sign-off"],
  ];
  const mw2 = (CW - 0.8) / 3;
  mods.forEach((m, i) => {
    const x = MX + i * (mw2 + 0.4);
    icon(s, x, my2 + 0.04, m[0], i === 2 ? GREEN : PURPLE);
    txt(s, m[1], { x: x + 0.44, y: my2, w: mw2 - 0.5, h: 0.24, fontSize: 11.5, bold: true, color: INK });
    txt(s, m[2], { x: x + 0.44, y: my2 + 0.26, w: mw2 - 0.5, h: 0.6, fontSize: 9.5, color: INK2, lineSpacingMultiple: 1.05 });
  });
  footer(s);

  s.addNotes(
    "This is the whole system on one picture. Wireless vibration and temperature sensors sit on both bearing housings of each pump, using hardware that meets the applicable PESO and IECEx requirements for hazardous areas. " +
    "An area gateway extracts sixteen standard vibration indicators per measurement window, following ISO 13374, and ISO 20816-3 alarm zones give usable limits from day one. " +
    "The model layer produces a per-pump anomaly score and a fault type. Results feed a reliability dashboard, and each alert arrives as a drafted work order inside the plant's existing CMMS. " +
    "The reliability engineer approves or rejects every action, and confirmed findings feed back to retrain the model. " +
    "Everything inside the dashed boundary runs on the plant network, so the condition history stays with the plant. " +
    "What is genuinely ours is the model layer and the workflow integration; sensors and gateways are mature industrial products. About 70 seconds.");
}

// =====================================================================
// SLIDE 5 : Technical feasibility and validation
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Technical feasibility");
  slideTitle(s, [
    { t: "The benchmark result is promising; " },
    { t: "the plant pilot must now test performance", p: true },
    { t: " under real operating conditions" },
  ], 0.95, 25);

  // ---- pipeline band
  const py3 = 1.72, pn = [
    ["Raw vibration signal", "12 kHz accelerometer"],
    ["Windowing", "2,048 samples, 0.17 s"],
    ["16 engineering features", ""],
    ["Random forest", "300 trees"],
    ["Output", "fault category + anomaly score"],
  ];
  const pw3 = 2.15, pg = 0.42;
  txt(s, "Feature pipeline", { x: MX, y: py3 - 0.26, w: 4, h: 0.22, fontSize: 12, bold: true, color: INK });
  pn.forEach((p, i) => {
    const x = MX + i * (pw3 + pg);
    rect(s, x, py3, pw3, 0.88, i === 2 ? LAV : WHITE, i === 2 ? null : { color: BORDER, width: 0.9 });
    txt(s, p[0], { x: x + 0.1, y: py3 + 0.08, w: pw3 - 0.2, h: 0.36, fontSize: 10, bold: true, color: INK, lineSpacingMultiple: 0.95 });
    if (i === 0) waveform(s, x + 0.15, py3 + 0.62, pw3 - 0.45, PURPLE2, 0.09, 1.2);
    else if (i === 2) txt(s, "RMS · kurtosis · crest factor · band energy", { x: x + 0.1, y: py3 + 0.44, w: pw3 - 0.2, h: 0.4, fontSize: 8, color: PURPLE, bold: true, lineSpacingMultiple: 1.0 });
    else txt(s, p[1], { x: x + 0.1, y: py3 + 0.5, w: pw3 - 0.2, h: 0.34, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.0 });
    if (i < 4) arrowR(s, x + pw3 + 0.04, py3 + 0.44, pg - 0.08);
  });

  // ---- left: three metric tiles + caveat
  const my3 = 3.05;
  const tiles = [
    ["97.9%", "four-class benchmark accuracy, unseen 3 hp load [5]"],
    ["0 of 237", "healthy benchmark windows misclassified [5]"],
    ["98.9%", "grouped cross-validation accuracy [5]"],
  ];
  const tw3 = 2.28;
  txt(s, "Prototype benchmark results", { x: MX, y: my3 - 0.26, w: 5, h: 0.22, fontSize: 12, bold: true, color: INK });
  tiles.forEach((t, i) => {
    const x = MX + i * (tw3 + 0.22);
    rect(s, x, my3, tw3, 1.06, WHITE, { color: BORDER, width: 0.9 });
    txt(s, t[0], { x: x + 0.12, y: my3 + 0.08, w: tw3 - 0.24, h: 0.4, fontSize: 22, bold: true, color: PURPLE });
    txt(s, t[1], { x: x + 0.12, y: my3 + 0.52, w: tw3 - 0.24, h: 0.5, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.02 });
  });
  rect(s, MX, my3 + 1.22, 3 * tw3 + 0.44, 0.62, LAV2, null);
  txt(s, "CWRU is a controlled test-rig dataset with seeded faults. These results do not represent proven chemical-plant performance.", {
    x: MX + 0.14, y: my3 + 1.3, w: 3 * tw3 + 0.2, h: 0.48, fontSize: 10, color: INK, valign: "middle", lineSpacingMultiple: 1.05,
  });
  txt(s, "Evaluation note: whole recordings and one entire motor load were held out; windows from one recording never appear in both training and test.", {
    x: MX, y: my3 + 1.95, w: 3 * tw3 + 0.44, h: 0.42, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.05,
  });

  // ---- right: confusion matrix
  const cmx = 8.55, cmy = 2.95, cell = 0.78, cellH = 0.44;
  txt(s, "Confusion matrix, unseen 3 hp load [5]", { x: cmx, y: cmy - 0.26, w: 4.2, h: 0.22, fontSize: 12, bold: true, color: INK });
  const labels = ["Normal", "Inner race", "Ball", "Outer race"];
  const cm = [[237, 0, 0, 0], [0, 216, 21, 0], [0, 0, 236, 0], [0, 0, 3, 410]];
  txt(s, "actual", { x: cmx + 0.08, y: cmy + 0.16, w: 0.75, h: 0.2, fontSize: 8, color: INK2 });
  labels.forEach((l, j) => {
    txt(s, l, { x: cmx + 0.85 + j * cell, y: cmy + 0.05, w: cell - 0.04, h: 0.3, fontSize: 8, color: INK2, align: "center", lineSpacingMultiple: 0.9 });
  });
  labels.forEach((l, i) => {
    txt(s, l, { x: cmx + 0.08, y: cmy + 0.42 + i * cellH + 0.1, w: 0.75, h: 0.3, fontSize: 8, color: INK2, lineSpacingMultiple: 0.9 });
    for (let j = 0; j < 4; j++) {
      const v = cm[i][j];
      const diag = i === j;
      const off = !diag && v > 0;
      rect(s, cmx + 0.85 + j * cell, cmy + 0.42 + i * cellH, cell - 0.03, cellH - 0.03,
        diag ? (v > 300 ? PURPLE2 : LAV) : WHITE, { color: BORDER, width: 0.6 });
      txt(s, String(v), {
        x: cmx + 0.85 + j * cell, y: cmy + 0.42 + i * cellH + 0.08, w: cell - 0.03, h: 0.28,
        fontSize: 10.5, bold: diag || off, align: "center",
        color: diag ? (v > 300 ? WHITE : PURPLE) : (off ? AMBER : BORDER),
      });
    }
  });
  txt(s, "1,123 test windows. Confusions occur only between fault types, never between fault and healthy.", {
    x: cmx, y: cmy + 0.42 + 4 * cellH + 0.08, w: 4.2, h: 0.4, fontSize: 8.5, color: INK2, lineSpacingMultiple: 1.05,
  });

  // ---- bottom: established vs to validate
  const by5 = 5.85;
  hline(s, MX, by5 - 0.14, CW, BORDER, 1);
  txt(s, "Already established", { x: MX, y: by5, w: 2.6, h: 0.22, fontSize: 11.5, bold: true, color: GREEN });
  const est = ["Industrial vibration sensors", "Wireless gateways", "OPC UA", "CMMS APIs", "ISO vibration guidance [6]"];
  let ex = MX + 2.1;
  est.forEach((e) => {
    const wch = 0.16 + e.length * 0.062;
    s.addShape(pres.ShapeType.ellipse, { x: ex, y: by5 + 0.07, w: 0.07, h: 0.07, fill: { color: GREEN }, line: { type: "none" } });
    txt(s, e, { x: ex + 0.12, y: by5, w: wch, h: 0.22, fontSize: 9.5, color: INK });
    ex += wch + 0.28;
  });
  txt(s, "Still to be validated in the pilot", { x: MX, y: by5 + 0.42, w: 2.6, h: 0.22, fontSize: 11.5, bold: true, color: AMBER });
  const tov = ["Real plant noise", "Variable loading", "Fault lead time", "Sensor placement", "False-alert rate", "Model transfer"];
  let vx = MX + 2.55;
  tov.forEach((e) => {
    const wch = 0.16 + e.length * 0.062;
    s.addShape(pres.ShapeType.ellipse, { x: vx, y: by5 + 0.49, w: 0.07, h: 0.07, fill: { color: AMBER }, line: { type: "none" } });
    txt(s, e, { x: vx + 0.12, y: by5 + 0.42, w: wch, h: 0.22, fontSize: 9.5, color: INK });
    vx += wch + 0.28;
  });
  footer(s);

  s.addNotes(
    "How the detection works. A bearing defect makes the vibration signal impulsive and shifts energy into characteristic frequency bands. " +
    "We compute sixteen standard indicators per window, things like RMS, kurtosis, crest factor and band energies, and a random forest classifies them. " +
    "We trained and tested this ourselves on the public Case Western bearing dataset. Under a strict protocol, whole recordings held out and one motor load never seen in training, four-class accuracy is 97.9 percent, and none of the 237 healthy benchmark windows was misclassified. " +
    "The confusion matrix shows the only errors are between fault types, not between faulty and healthy. " +
    "And the caveat is printed on the slide: this is a controlled test rig with seeded faults, not a chemical plant. " +
    "Sensors, gateways and integration standards are mature; what still needs proof is plant noise, lead time and false-alert rate, which is exactly what the pilot measures. About 75 seconds.");
}

// =====================================================================
// SLIDE 6 : Pilot and scale-up
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Methodology for execution and way forward");
  slideTitle(s, [
    { t: "Shadow-mode deployment validates alerts " },
    { t: "before maintenance teams rely on the system", p: true },
  ], 0.85, 26);

  // ---- gantt
  const gx = MX, gy = 1.75, gw = 7.6, laneH = 0.4, months = 6;
  txt(s, "Six-month pilot plan", { x: gx, y: gy - 0.26, w: 4, h: 0.22, fontSize: 12, bold: true, color: INK });
  const axisX = gx + 2.35, axisW = gw - 2.35;
  for (let m = 0; m <= months; m++) {
    const x = axisX + (axisW / months) * m;
    vline(s, x, gy, laneH * 4 + 0.5, LAV, 0.75);
    txt(s, `M${m}`, { x: x - 0.14, y: gy + laneH * 4 + 0.52, w: 0.3, h: 0.18, fontSize: 8, color: INK2, align: "center" });
  }
  const bars = [
    ["Baseline and asset selection", 0, 1, PURPLE2],
    ["Sensor installation and integration", 1, 2, PURPLE2],
    ["Commissioning and healthy baselines", 2, 3, PURPLE2],
    ["Shadow-mode validation", 3, 6, PURPLE],
  ];
  bars.forEach((b, i) => {
    const y = gy + 0.1 + i * laneH;
    txt(s, b[0], { x: gx, y: y + 0.02, w: 2.25, h: 0.36, fontSize: 9, color: INK, lineSpacingMultiple: 0.92 });
    rect(s, axisX + (axisW / months) * b[1], y, (axisW / months) * (b[2] - b[1]), 0.24, b[3], null);
  });
  // go / no-go diamond at M6
  s.addShape(pres.ShapeType.diamond, { x: axisX + axisW - 0.11, y: gy + 0.1 + 3 * laneH - 0.34, w: 0.22, h: 0.22, fill: { color: PURPLE }, line: { type: "none" } });
  txt(s, "go or no-go decision", { x: axisX + axisW - 1.55, y: gy + 0.1 + 3 * laneH - 0.36, w: 1.4, h: 0.18, fontSize: 8, color: PURPLE, align: "right", bold: true });

  // swimlane roles
  const ry6 = gy + 4 * laneH + 0.78;
  txt(s, "Roles:", { x: gx, y: ry6, w: 0.6, h: 0.2, fontSize: 9, bold: true, color: INK });
  txt(s, "Reliability engineer: baseline, adjudication, gate · Instrumentation team: install · CMMS administrator: work-order flow · NAADI team: features, models, dashboards", {
    x: gx + 0.6, y: ry6, w: gw - 0.6, h: 0.4, fontSize: 9, color: INK2, lineSpacingMultiple: 1.05,
  });

  // ---- right: KPI gauges
  const kx = 8.55, ky6 = 1.75, kw6 = 4.22;
  txt(s, "Pilot success criteria", { x: kx, y: ky6 - 0.26, w: kw6, h: 0.22, fontSize: 12, bold: true, color: INK });
  const kpis6 = [
    ["≥70%", "of confirmed developing faults detected", 0.7],
    ["≥14 days", "warning before functional failure", 0.67],
    ["≤2", "false alerts per pump per month", 0.25],
    ["≥95%", "sensor data availability", 0.95],
  ];
  kpis6.forEach((k, i) => {
    const y = ky6 + 0.06 + i * 0.62;
    txt(s, k[0], { x: kx, y, w: 1.15, h: 0.34, fontSize: 17, bold: true, color: PURPLE });
    txt(s, k[1], { x: kx + 1.2, y: y + 0.03, w: kw6 - 1.25, h: 0.3, fontSize: 9, color: INK2, lineSpacingMultiple: 0.95 });
    rect(s, kx, y + 0.36, kw6 - 0.1, 0.07, LAV, null);
    rect(s, kx, y + 0.36, (kw6 - 0.1) * k[2], 0.07, PURPLE2, null);
  });
  txt(s, "Alerts run in shadow mode for three months and are compared weekly with actual maintenance findings before any alert changes a maintenance decision.", {
    x: kx, y: ky6 + 2.62, w: kw6, h: 0.66, fontSize: 9, color: INK2, lineSpacingMultiple: 1.08,
  });

  // ---- bottom: roadmap + pilot requirement
  const by6 = 5.55;
  hline(s, MX, by6 - 0.12, CW, BORDER, 1);
  txt(s, "Scale-up after the gate", { x: MX, y: by6, w: 3, h: 0.22, fontSize: 12, bold: true, color: INK });
  const road = [
    ["Months 0 to 6", "pilot: 25 pumps, one plant"],
    ["Months 6 to 12", "100 or more rotating assets: compressors, agitators, fans"],
    ["Months 12 to 24", "shared deployment across chemical clusters [7][8]"],
  ];
  const rw6 = 2.62;
  road.forEach((r, i) => {
    const x = MX + i * (rw6 + 0.38);
    rect(s, x, by6 + 0.3, rw6, 0.92, i === 2 ? LAV : LAV2, null);
    txt(s, r[0], { x: x + 0.12, y: by6 + 0.38, w: rw6 - 0.24, h: 0.22, fontSize: 9.5, bold: true, color: PURPLE });
    txt(s, r[1], { x: x + 0.12, y: by6 + 0.6, w: rw6 - 0.24, h: 0.58, fontSize: 9, color: INK, lineSpacingMultiple: 1.02 });
    if (i < 2) arrowR(s, x + rw6 + 0.05, by6 + 0.76, 0.28, PURPLE2, 1.5);
  });
  const px6 = MX + 3 * rw6 + 2 * 0.38 + 0.35;
  rect(s, px6, by6 + 0.3, W - MX - px6, 0.92, WHITE, { color: PURPLE, width: 1.25 });
  txt(s, "Pilot requirement", { x: px6 + 0.14, y: by6 + 0.37, w: 2.5, h: 0.2, fontSize: 9.5, bold: true, color: PURPLE });
  txt(s, "one plant partner · 25 critical pumps · historical CMMS data · six months of site access", {
    x: px6 + 0.14, y: by6 + 0.58, w: W - MX - px6 - 0.28, h: 0.6, fontSize: 9, color: INK, lineSpacingMultiple: 1.05,
  });
  footer(s);

  s.addNotes(
    "Execution is a six-month pilot with one principle: the system must earn trust before anyone relies on it. " +
    "Months zero to one build the baseline from the plant's own maintenance records and fix the success criteria together with the plant, so the pass bar is agreed before installation. " +
    "Month two is installation: wireless sensors magnet-mounted during routine access, no shutdown, permits handled through the plant's normal process. " +
    "Month three commissions healthy baselines, and months three to six run in shadow mode: alerts are logged and compared weekly with what maintenance actually finds, but no decision depends on them yet. " +
    "The month-six gate is numeric and is on the slide: seventy percent of confirmed developing faults caught at least fourteen days ahead, at most two false alerts per pump per month, and ninety-five percent data availability. " +
    "Pass the gate and the system goes live, then scales to other rotating assets and, between months twelve and twenty-four, to a shared deployment across chemical clusters. " +
    "What we need is one plant partner, the pumps, their history and six months of access. About 75 seconds.");
}

// =====================================================================
// SLIDE 7 : Economics, environment, risk
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Economic feasibility and risks");
  slideTitle(s, [
    { t: "The base case pays back in " },
    { t: "11 months", p: true },
    { t: ", with a 24-month downside case" },
  ], 0.8, 26);

  // ---- KPI strip
  const ky7 = 1.4, kw7 = CW / 4;
  const kpis7 = [
    ["₹37 lakh", "estimated CapEx, 25 pumps", "Team estimate", AMBER],
    ["₹41.4 lakh", "annual net benefit, base case", "Team calculation", INK2],
    ["≈11 months", "base-case payback", "Team calculation", INK2],
    ["≈24 months", "stacked-downside payback", "Team calculation", INK2],
  ];
  kpis7.forEach((k, i) => {
    const x = MX + i * kw7;
    if (i > 0) vline(s, x, ky7 + 0.05, 0.85, BORDER, 0.75);
    txt(s, k[0], { x: x + (i ? 0.22 : 0), y: ky7, w: kw7 - 0.3, h: 0.38, fontSize: 21, bold: true, color: PURPLE });
    txt(s, k[1], { x: x + (i ? 0.22 : 0), y: ky7 + 0.4, w: kw7 - 0.35, h: 0.24, fontSize: 9.5, color: INK2 });
    txt(s, k[2], { x: x + (i ? 0.22 : 0), y: ky7 + 0.66, w: kw7 - 0.35, h: 0.16, fontSize: 8, color: k[3] });
  });
  hline(s, MX, ky7 + 0.95, CW, BORDER, 1);

  // ---- waterfall (left)
  const wx = MX, wy = 2.85, wwch = 5.9, wh7 = 1.58, base = wy + wh7;
  txt(s, "Annual benefit build-up, INR lakh, base case", { x: wx, y: wy - 0.28, w: wwch, h: 0.22, fontSize: 12, bold: true, color: INK });
  const scale = wh7 / 50; // 50 L full height
  const wf = [
    ["Avoided downtime value [2]", 39.4, 0, PURPLE2],
    ["Repair savings [2]", 3.0, 39.4, PURPLE2],
    ["Avoided severe failures", 5.0, 42.4, PURPLE2],
    ["Annual OpEx", -6.0, 47.4, AMBER],
    ["Net annual benefit", 41.4, 0, PURPLE],
  ];
  const bw7 = 0.82, bg7 = 0.32;
  wf.forEach((b, i) => {
    const x = wx + 0.1 + i * (bw7 + bg7);
    const v = b[1], start = b[2];
    const y0 = base - (start + Math.max(v, 0)) * scale;
    const hh = Math.abs(v) * scale;
    rect(s, x, y0, bw7, hh, b[3], null);
    txt(s, (v > 0 ? "+" : "") + v.toFixed(1), { x: x - 0.12, y: y0 - 0.22, w: bw7 + 0.24, h: 0.2, fontSize: 9.5, bold: true, color: b[3] === AMBER ? AMBER : PURPLE, align: "center" });
    txt(s, b[0], { x: x - 0.18, y: base + 0.06, w: bw7 + 0.36, h: 0.55, fontSize: 8, color: INK2, align: "center", lineSpacingMultiple: 0.95 });
    if (i < wf.length - 1 && i !== 3) {
      hline(s, x + bw7, base - (start + v) * scale, bg7, INK2, 0.75, "dash");
    }
    if (i === 3) hline(s, x + bw7, base - (start + v) * scale, bg7, INK2, 0.75, "dash");
  });
  hline(s, wx, base, wwch - 0.6, INK2, 1);
  txt(s, "downtime reduction taken at 35%, the low end of the DOE FEMP range [2]", {
    x: wx, y: base + 0.58, w: wwch, h: 0.2, fontSize: 8.5, color: INK2,
  });

  // ---- tornado (right)
  const tx7 = 7.0, ty7 = 2.85, tw7 = 5.75;
  txt(s, "Payback sensitivity, months", { x: tx7, y: ty7 - 0.28, w: tw7, h: 0.22, fontSize: 12, bold: true, color: INK });
  const sens = [
    ["45% downtime reduction", 8.4, GREEN],
    ["Base case", 10.7, PURPLE],
    ["CapEx plus 30%", 14.0, AMBER],
    ["Lost margin one-third lower", 15.7, AMBER],
    ["20% downtime reduction", 18.1, AMBER],
    ["Stacked downside", 23.6, AMBER],
  ];
  const lab = 2.15, trackW = tw7 - lab - 0.55, maxM = 26;
  sens.forEach((sc, i) => {
    const y = ty7 + i * 0.4;
    txt(s, sc[0], { x: tx7, y: y + 0.015, w: lab, h: 0.36, fontSize: 9, color: sc[2] === PURPLE ? PURPLE : INK, bold: sc[2] === PURPLE, lineSpacingMultiple: 0.9 });
    rect(s, tx7 + lab, y, trackW * sc[1] / maxM, 0.22, sc[2], null);
    txt(s, sc[1].toFixed(1), { x: tx7 + lab + trackW * sc[1] / maxM + 0.06, y: y - 0.005, w: 0.55, h: 0.22, fontSize: 9.5, bold: true, color: sc[2] });
  });
  vline(s, tx7 + lab, ty7 - 0.05, 0.4 * 6, INK2, 1);

  // ---- bottom row: risk matrix + mitigations + environment + recommendation
  const by7 = 5.42;
  hline(s, MX, by7 - 0.14, CW, BORDER, 1);
  // quadrant
  const qx = MX, qy = by7 + 0.26, qw = 2.5, qh = 1.3;
  txt(s, "Key risks", { x: qx, y: by7, w: 2.5, h: 0.2, fontSize: 12, bold: true, color: INK });
  rect(s, qx, qy, qw, qh, LAV2, null);
  vline(s, qx + qw / 2, qy, qh, BORDER, 0.75);
  hline(s, qx, qy + qh / 2, qw, BORDER, 0.75);
  txt(s, "impact ↑", { x: qx + 0.05, y: qy + 0.04, w: 0.8, h: 0.16, fontSize: 7.5, color: INK2 });
  txt(s, "likelihood →", { x: qx + qw - 0.78, y: qy + qh - 0.2, w: 0.75, h: 0.16, fontSize: 7.5, color: INK2 });
  const risks = [
    [1, 0.82, 0.28], // false-alert fatigue: high likelihood, med-high impact
    [2, 0.38, 0.2],  // hazardous-area compliance: med likelihood, high impact
    [3, 0.16, 0.3],  // OT cybersecurity: low likelihood, high impact
    [4, 0.72, 0.62], // limited failure examples: high likelihood, medium impact
  ];
  risks.forEach((r) => {
    const x = qx + r[1] * qw - 0.09, y = qy + r[2] * qh - 0.09;
    s.addShape(pres.ShapeType.ellipse, { x, y, w: 0.2, h: 0.2, fill: { color: AMBER }, line: { type: "none" } });
    txt(s, String(r[0]), { x, y: y + 0.015, w: 0.2, h: 0.17, fontSize: 8.5, bold: true, color: WHITE, align: "center" });
  });
  // mitigations
  const mx7 = 3.35, mw7 = 5.1;
  const mits = [
    ["1  False-alert fatigue", "shadow mode first; at most 2 alerts per pump-month at the gate"],
    ["2  Hazardous-area hardware", "hardware meeting applicable PESO and IECEx requirements [10]"],
    ["3  OT cybersecurity", "one-way data flow on a segregated network; no path to the DCS"],
    ["4  Few early failure examples", "anomaly-first models per pump; classifier added as data grows"],
  ];
  mits.forEach((m, i) => {
    const y = by7 + 0.02 + i * 0.42;
    txt(s, m[0], { x: mx7, y, w: 1.95, h: 0.4, fontSize: 9, bold: true, color: INK, lineSpacingMultiple: 0.9 });
    txt(s, m[1], { x: mx7 + 2.0, y, w: mw7 - 2.0, h: 0.4, fontSize: 8.5, color: INK2, lineSpacingMultiple: 0.95 });
  });
  // environment + recommendation
  const ex7 = 8.75, ew7 = 4.03;
  txt(s, "Environmental gains", { x: ex7, y: by7, w: ew7, h: 0.2, fontSize: 12, bold: true, color: GREEN });
  const envs = [
    "Earlier detection of seal degradation can reduce leak-event risk [4]",
    "The same condition data can identify cavitation and off-design operation; pumping is close to 20% of world electric-motor demand [9]",
  ];
  envs.forEach((e, i) => {
    s.addShape(pres.ShapeType.ellipse, { x: ex7, y: by7 + 0.29 + i * 0.46, w: 0.07, h: 0.07, fill: { color: GREEN }, line: { type: "none" } });
    txt(s, e, { x: ex7 + 0.14, y: by7 + 0.22 + i * 0.46, w: ew7 - 0.14, h: 0.46, fontSize: 8.5, color: INK, lineSpacingMultiple: 1.0 });
  });
  rect(s, ex7, by7 + 1.2, ew7, 0.5, LAV, null);
  txt(s, "Recommendation: proceed with a six-month shadow-mode pilot, subject to plant-data validation and vendor quotations.", {
    x: ex7 + 0.12, y: by7 + 1.24, w: ew7 - 0.24, h: 0.42, fontSize: 9, color: INK, valign: "middle", lineSpacingMultiple: 1.0,
  });
  footer(s);

  s.addNotes(
    "The economics, with the calculation visible. Each avoided downtime hour is worth about 1.9 lakh of contribution margin. " +
    "Taking the US Department of Energy's published effectiveness range at its low end, 35 percent downtime reduction and 10 percent repair savings, the waterfall builds to 47.4 lakh of annual benefit, less 6 lakh of operating cost, so 41.4 lakh net. " +
    "Against an estimated 37 lakh of CapEx that is roughly an 11-month base-case payback and about 1.1 crore of five-year NPV at a 12 percent discount rate. " +
    "The sensitivity chart stress-tests it: even if the programme delivers only 20 percent reduction, below the DOE band, or CapEx overruns by 30 percent, payback stays under 24 months in the stacked downside. " +
    "The risks we take most seriously are false-alert fatigue, hazardous-area compliance, OT security and the shortage of early failure examples; each has a specific mitigation on the slide. " +
    "Environmentally, earlier seal-fault detection reduces leak risk, and the same data helps find cavitation and off-design operation. " +
    "Our recommendation is deliberately conditional: proceed with the pilot, subject to plant-data validation and vendor quotations. About 75 seconds.");
}

// =====================================================================
// SLIDE 8 : References
// =====================================================================
{
  const s = newSlide();
  sectionTag(s, "Supporting evidence");
  slideTitle(s, [{ t: "Sources, standards and calculation basis" }], 0.6, 27);

  const colW2 = (CW - 0.6) / 2;
  const L1 = MX, L2 = MX + colW2 + 0.6;
  let y1 = 1.45, y2 = 1.45;

  function group(x, yRef, title) {
    txt(s, title, { x, y: yRef.v, w: colW2, h: 0.24, fontSize: 13, bold: true, color: PURPLE });
    yRef.v += 0.32;
  }
  function ref(x, yRef, num, body, link, h = 0.42) {
    txt(s, `[${num}]`, { x, y: yRef.v, w: 0.4, h, fontSize: 10, bold: true, color: PURPLE2 });
    const runs = [{ text: body + "  ", options: { color: INK } }];
    if (link) runs.push({ text: link[0], options: { color: PURPLE2, underline: true, hyperlink: { url: link[1] } } });
    s.addText(runs, {
      x: x + 0.42, y: yRef.v, w: colW2 - 0.42, h, fontFace: FONT, fontSize: 10,
      isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.06,
    });
    yRef.v += h + 0.1;
  }

  const ya = { v: y1 };
  group(L1, ya, "Government and industry guidance");
  ref(L1, ya, 1, "Department of Chemicals and Petrochemicals (GoI) and FICCI. Youth Innovation Challenge brief, India Chem 2026. 2026. Provided competition document.", null, 0.56);
  ref(L1, ya, 2, "US Department of Energy, FEMP. Operations and Maintenance Best Practices Guide, Release 3.0 (predictive maintenance chapter). 2010.", ["energy.gov", "https://www.energy.gov/sites/prod/files/2020/04/f74/omguide_complete_w-eo-disclaimer.pdf"], 0.56);
  ref(L1, ya, 7, "NITI Aayog. National Strategy for Artificial Intelligence. 2018. And DST, National Mission on Interdisciplinary Cyber-Physical Systems. 2018.", ["dst.gov.in", "https://dst.gov.in/national-mission-interdisciplinary-cyber-physical-systems-nm-icps"], 0.56);
  ref(L1, ya, 8, "Ministry of Heavy Industries. SAMARTH Udyog Bharat 4.0 (Industry 4.0 centres). 2024.", ["samarthudyog-i40.in", "https://samarthudyog-i40.in/"], 0.42);

  ya.v += 0.12;
  group(L1, ya, "Engineering standards");
  ref(L1, ya, 6, "ISO 20816-3:2022 machine vibration evaluation; ISO 13374-1:2003 condition-monitoring data processing; ISO 17359:2018 condition-monitoring guidelines; ISO 14224:2016 reliability data collection.", ["iso.org", "https://www.iso.org/standard/78311.html"], 0.7);
  ref(L1, ya, 10, "Petroleum and Explosives Safety Organisation (PESO), DPIIT. Statutory approvals for equipment in hazardous areas.", ["peso.gov.in", "https://peso.gov.in"], 0.42);

  const yb = { v: y2 };
  group(L2, yb, "Technical literature");
  ref(L2, yb, 3, "Nowlan, F.S. and Heap, H.F. Reliability-Centered Maintenance. US DoD report AD-A066579. 1978.", null, 0.42);
  ref(L2, yb, 4, "McKee, K. et al. A review of major centrifugal pump failure modes. ICOMS Asset Management Conference. 2011.", ["espace.curtin.edu.au", "https://espace.curtin.edu.au/handle/20.500.11937/28560"], 0.42);
  ref(L2, yb, 9, "Hydraulic Institute, Europump and US DOE. Pump Life Cycle Costs: A Guide to LCC Analysis for Pumping Systems. 2001.", null, 0.42);

  yb.v += 0.12;
  group(L2, yb, "Dataset and team calculations");
  ref(L2, yb, 5, "Case Western Reserve University Bearing Data Center, seeded-fault vibration dataset. Team model code train_fault_model.py and results metrics.json, 2026. Benchmark results only; not plant performance.", ["engineering.case.edu/bearingdatacenter", "https://engineering.case.edu/bearingdatacenter"], 0.7);
  ref(L2, yb, 11, "Team economics: NAADI_pilot_economics.xlsx (live formulas and assumption register) and CALCULATIONS.md, 2026. Plant archetype values are team estimates pending pilot data.", null, 0.56);

  yb.v += 0.1;
  rect(s, L2, yb.v, colW2, 1.0, LAV2, null);
  txt(s, [
    { text: "Basis of preparation. ", options: { bold: true, color: INK } },
    { text: "Estimates and calculations are labelled where they appear. The comparison scores on slide 3 are team judgement. No plant trial, vendor quotation or primary research has been completed yet; the pilot in slide 6 is designed to supply that evidence.", options: { color: INK2 } },
  ], { x: L2 + 0.15, y: yb.v + 0.1, w: colW2 - 0.3, h: 0.85, fontSize: 9.5, lineSpacingMultiple: 1.1 });

  footer(s);
  s.addNotes(
    "The reference slide groups everything we relied on: government guidance including the Department of Energy maintenance ranges, the engineering standards for vibration evaluation and reliability data, the technical literature behind the failure statistics, and our own dataset work and economics files. " +
    "Numbers in square brackets throughout the deck point here. " +
    "The basis-of-preparation note states plainly what is estimated, what is judgement and what has not yet been proven. We are happy to take questions. About 30 seconds.");
}

pres.writeFile({ fileName: "India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx" })
  .then(() => console.log("v2 deck written"));
