// NAADI — India Chem 2026 Youth Innovation Challenge concept deck (8 slides)
// Team: Raunak Jain & Anushriya Bhattacharya, NIT Warangal.
// DRAFT generated for team review — all content decisions require team ratification.
// Build: node build_deck.js   →  India_Chem_2026_NITW_Raunak_Anushriya.pptx

const pptxgen = require("pptxgenjs");

const NAVY = "12212F";
const TEAL = "087E8B";
const GREEN = "2E9D66";
const AMBER = "F59E0B";
const AMBER_DARK = "B45309"; // readable amber for text on white
const LIGHT = "F4F7F8";
const BORDER = "D9E2E7";
const GREY = "5A6B78";
const WHITE = "FFFFFF";
const FONT = "Arial";

const W = 13.333, H = 7.5;
const MX = 0.55; // side margin
const CW = W - 2 * MX; // content width

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Raunak Jain, Anushriya Bhattacharya — NIT Warangal";
pres.title = "NAADI — Predictive maintenance for critical pumps";

let slideNo = 0;

function newSlide(bg) {
  slideNo += 1;
  const s = pres.addSlide();
  s.background = { color: bg || WHITE };
  return s;
}

function footer(s, sources) {
  if (sources) {
    s.addText(sources, {
      x: MX, y: 7.02, w: CW, h: 0.22, fontFace: FONT, fontSize: 8.5,
      color: GREY, isTextBox: true, margin: 0, valign: "middle",
    });
  }
  s.addText(
    "India Chem 2026 · Youth Innovation Challenge — NIT Warangal · Raunak Jain & Anushriya Bhattacharya",
    { x: MX, y: 7.24, w: 9.5, h: 0.2, fontFace: FONT, fontSize: 8.5, color: GREY, isTextBox: true, margin: 0 });
  s.addText(String(slideNo).padStart(2, "0") + " / 08",
    { x: W - MX - 1.0, y: 7.24, w: 1.0, h: 0.2, fontFace: FONT, fontSize: 8.5, color: GREY, align: "right", isTextBox: true, margin: 0 });
}

// Takeaway title: runs = [{t, accent?}]
function title(s, runs, opts = {}) {
  s.addText(runs.map(r => ({
    text: r.t, options: { color: r.accent ? (opts.accent || TEAL) : NAVY, bold: true },
  })), {
    x: MX, y: 0.32, w: CW, h: opts.h || 0.95, fontFace: FONT,
    fontSize: opts.size || 25, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.04,
  });
}

function kicker(s, text, color) {
  s.addText(text.toUpperCase(), {
    x: MX, y: 0.12, w: CW, h: 0.2, fontFace: FONT, fontSize: 10.5, bold: true,
    color: color || TEAL, charSpacing: 2, isTextBox: true, margin: 0,
  });
}

function card(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.055,
    fill: { color: fill || WHITE },
    line: { color: BORDER, width: 1 },
  });
}

function sectionHead(s, x, y, w, text, color) {
  s.addText(text, {
    x, y, w, h: 0.26, fontFace: FONT, fontSize: 12.5, bold: true,
    color: color || NAVY, isTextBox: true, margin: 0,
  });
}

function body(s, x, y, w, h, items, opts = {}) {
  const arr = items.map((it, i) => ({
    text: it,
    options: {
      bullet: opts.bullet === false ? false : { code: "2022", indent: 10 },
      breakLine: true,
      paraSpaceAfter: opts.space == null ? 5 : opts.space,
      color: opts.color || NAVY,
    },
  }));
  s.addText(arr, {
    x, y, w, h, fontFace: FONT, fontSize: opts.size || 15,
    isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.06,
  });
}

// =====================================================================
// SLIDE 1 — Title
// =====================================================================
{
  const s = newSlide(NAVY);

  s.addText("INDIA CHEM 2026 · YOUTH INNOVATION CHALLENGE", {
    x: MX, y: 0.55, w: 8.0, h: 0.3, fontFace: FONT, fontSize: 12, bold: true,
    color: AMBER, charSpacing: 3, isTextBox: true, margin: 0,
  });

  s.addText([
    { text: "NAADI", options: { color: WHITE, bold: true, fontSize: 54 } },
    { text: "  — listening to the pulse of the plant", options: { color: TEAL, fontSize: 20, bold: false } },
  ], { x: MX, y: 1.15, w: 8.0, h: 1.0, fontFace: FONT, isTextBox: true, margin: 0, valign: "top" });

  s.addText([
    { text: "Cut unplanned pump downtime ", options: { color: WHITE } },
    { text: "35–45%", options: { color: "F7B84B", bold: true } },
    { text: " in Indian chemical plants with a vendor-neutral, plant-owned vibration-intelligence stack.", options: { color: WHITE } },
  ], {
    x: MX, y: 2.25, w: 7.6, h: 1.1, fontFace: FONT, fontSize: 21,
    isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.12,
  });

  s.addText("Continuous vibration sensing and interpretable machine learning on 25 bad-actor pumps: " +
    "~₹37 lakh to install, ~11-month payback, prototype already validated on a public bearing benchmark.", {
    x: MX, y: 3.45, w: 7.3, h: 0.95, fontFace: FONT, fontSize: 15, color: "C9D6DE",
    isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.15,
  });

  // Problem statement chip
  s.addShape(pres.ShapeType.roundRect, {
    x: MX, y: 4.62, w: 7.3, h: 0.72, rectRadius: 0.06,
    fill: { color: "1B3242" }, line: { color: "2E4A5C", width: 1 },
  });
  s.addText([
    { text: "Problem statement (Annexure): ", options: { bold: true, color: TEAL } },
    { text: "AI-driven predictive maintenance to improve asset reliability and maintenance efficiency in the chemicals & petrochemicals sector.", options: { color: "C9D6DE" } },
  ], { x: MX + 0.18, y: 4.68, w: 7.0, h: 0.62, fontFace: FONT, fontSize: 12.5, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });

  // Team block
  s.addText([
    { text: "Raunak Jain", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "B.Tech Mechanical Engineering", options: { color: "8FA6B3", breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Anushriya Bhattacharya", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "B.Tech Chemical Engineering", options: { color: "8FA6B3", breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "National Institute of Technology Warangal", options: { bold: true, color: TEAL, breakLine: true } },
  ], { x: MX, y: 5.62, w: 5.4, h: 1.5, fontFace: FONT, fontSize: 13, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });

  // ---- right-side vector motif: pump + sensor + waveform + alert (native shapes)
  const cx = 8.7;
  s.addShape(pres.ShapeType.roundRect, { x: cx, y: 1.0, w: 4.0, h: 5.3, rectRadius: 0.08, fill: { color: "182C3B" }, line: { color: "2E4A5C", width: 1 } });
  // pump: casing circle + flange rects
  s.addShape(pres.ShapeType.ellipse, { x: cx + 0.55, y: 1.55, w: 1.15, h: 1.15, fill: { color: "223D50" }, line: { color: TEAL, width: 2 } });
  s.addShape(pres.ShapeType.ellipse, { x: cx + 0.93, y: 1.93, w: 0.39, h: 0.39, fill: { color: TEAL } });
  s.addShape(pres.ShapeType.rect, { x: cx + 1.7, y: 1.95, w: 1.5, h: 0.36, fill: { color: "223D50" }, line: { color: TEAL, width: 1.5 } }); // shaft/motor
  s.addShape(pres.ShapeType.rect, { x: cx + 3.2, y: 1.72, w: 0.55, h: 0.82, fill: { color: "223D50" }, line: { color: TEAL, width: 1.5 } });
  // sensor dot on bearing housing
  s.addShape(pres.ShapeType.ellipse, { x: cx + 1.62, y: 1.68, w: 0.22, h: 0.22, fill: { color: AMBER } });
  s.addText("wireless vibration sensor", { x: cx + 1.9, y: 1.52, w: 1.9, h: 0.3, fontFace: FONT, fontSize: 9.5, color: "8FA6B3", isTextBox: true, margin: 0 });
  // waveform (zigzag line segments)
  const wy = 3.35;
  const pts = [0, .18, -.28, .38, -.5, .55, -.2, .3, -.35, .15];
  for (let i = 0; i < pts.length - 1; i++) {
    s.addShape(pres.ShapeType.line, {
      x: cx + 0.55 + i * 0.31, y: Math.min(wy + pts[i], wy + pts[i + 1]),
      w: 0.31, h: Math.abs(pts[i + 1] - pts[i]) || 0.01,
      line: { color: GREEN, width: 2.25 },
      flipV: pts[i + 1] < pts[i],
    });
  }
  s.addText("vibration signature → 16 interpretable features", { x: cx + 0.55, y: 4.05, w: 3.2, h: 0.3, fontFace: FONT, fontSize: 9.5, color: "8FA6B3", isTextBox: true, margin: 0 });
  // arrow to work order
  s.addShape(pres.ShapeType.line, { x: cx + 1.95, y: 4.45, w: 0, h: 0.42, line: { color: GREY, width: 1.5, endArrowType: "triangle" } });
  s.addShape(pres.ShapeType.roundRect, { x: cx + 0.55, y: 4.95, w: 2.9, h: 0.85, rectRadius: 0.06, fill: { color: "223D50" }, line: { color: GREEN, width: 1.5 } });
  s.addText([
    { text: "14 days early warning → ", options: { color: "C9D6DE" } },
    { text: "planned work order", options: { color: GREEN, bold: true } },
  ], { x: cx + 0.72, y: 5.02, w: 2.6, h: 0.72, fontFace: FONT, fontSize: 11.5, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });

  s.addText("Final round: Bombay Exhibition Centre, Mumbai · 24 October 2026", {
    x: MX, y: 7.24, w: 9.0, h: 0.2, fontFace: FONT, fontSize: 8.5, color: "8FA6B3", isTextBox: true, margin: 0 });
  s.addText("01 / 08", { x: W - MX - 1.0, y: 7.24, w: 1.0, h: 0.2, fontFace: FONT, fontSize: 8.5, color: "8FA6B3", align: "right", isTextBox: true, margin: 0 });

  s.addNotes(
    "Good morning. We are Raunak Jain, mechanical engineering, and Anushriya Bhattacharya, chemical engineering, from NIT Warangal. " +
    "Our proposal is NAADI — the Sanskrit word for pulse — a predictive-maintenance stack for the pumps that keep a chemical plant alive. " +
    "The one-line thesis: continuous vibration monitoring with interpretable machine learning on a plant's 25 worst pumps costs about 37 lakh rupees, " +
    "pays back in roughly eleven months, and unlike proprietary cloud offerings, leaves the data and the models with the plant. " +
    "The 35 to 45 percent downtime-reduction range is the US Department of Energy's published band for functioning predictive-maintenance programmes — not our invention. " +
    "Everything you will see is either sourced, or computed by us in code we can hand you. [~60 s]");
}

// =====================================================================
// SLIDE 2 — Existing scenario, quantified problem
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Existing scenario · the quantified problem", TEAL);
  title(s, [
    { t: "Twenty-five bad-actor pumps expose a mid-size plant to " },
    { t: "~₹1.4 crore a year", accent: true },
    { t: " because maintenance runs on the calendar, not on machine condition" },
  ], { h: 1.15, size: 24 });

  // KPI strip
  const kpis = [
    ["60 h/yr", "unplanned outage caused by these pumps (est.)"],
    ["₹1.9 lakh/h", "contribution margin lost while down (est.)"],
    ["12 /yr", "repair events across the 25 pumps (est.)"],
    ["~₹1.4 Cr", "annual exposure: lost margin + repairs (est.)"],
  ];
  kpis.forEach((k, i) => {
    const x = MX + i * (CW / 4 + 0.02) - i * 0.02;
    const w = CW / 4 - 0.15;
    card(s, x, 1.62, w, 1.05, LIGHT);
    s.addText(k[0], { x: x + 0.15, y: 1.72, w: w - 0.3, h: 0.4, fontFace: FONT, fontSize: 21, bold: true, color: TEAL, isTextBox: true, margin: 0 });
    s.addText(k[1], { x: x + 0.15, y: 2.12, w: w - 0.3, h: 0.5, fontFace: FONT, fontSize: 10.5, color: GREY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.0 });
  });

  // Left: use case & boundary
  card(s, MX, 2.92, 5.9, 2.55);
  sectionHead(s, MX + 0.22, 3.08, 5.4, "USE CASE & SYSTEM BOUNDARY", TEAL);
  body(s, MX + 0.22, 3.42, 5.5, 1.95, [
    "Representative mid-size speciality-chemicals plant: ₹500 Cr revenue, 8,000 operating h/yr, ~200 pumps.",
    "Boundary: the 25 critical API 610-class centrifugal pumps in continuous service whose trip stops production.",
    "Practice today: calendar-based preventive maintenance plus breakdown response; no continuous condition data.",
  ], { size: 13.5, space: 6 });

  // Right: root causes
  card(s, MX + 6.15, 2.92, 6.08, 2.55);
  sectionHead(s, MX + 6.37, 3.08, 5.6, "WHY IT FAILS — ROOT CAUSES", TEAL);
  body(s, MX + 6.37, 3.42, 5.65, 1.95, [
    "Failures strike at random: the foundational RCM study found 89% of failure modes have no wear-out age — fixed-interval PM cannot anticipate them [4].",
    "Bearing and seal degradation dominates pump failures [5], and develops over days-to-weeks — invisible between monthly rounds.",
    "Repair only after functional failure → secondary damage, emergency spares, multi-hour restarts.",
  ], { size: 13.5, space: 6 });

  // Problem statement bar
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: 5.68, w: CW, h: 0.95, rectRadius: 0.055, fill: { color: NAVY } });
  s.addText([
    { text: "The problem we solve: ", options: { bold: true, color: "F7B84B" } },
    { text: "detect developing faults on these 25 pumps at least two weeks before functional failure, and convert every detection into a planned work order — without replacing any existing plant system.", options: { color: WHITE } },
  ], { x: MX + 0.25, y: 5.78, w: CW - 0.5, h: 0.75, fontFace: FONT, fontSize: 14.5, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.08 });

  footer(s,
    "Sources: [4] Nowlan & Heap, Reliability-Centered Maintenance, U.S. DoD report AD-A066579, 1978. [5] McKee et al., A review of major centrifugal pump failure modes, ICOMS, 2011. Plant figures: team estimates for a representative plant (assumption register), to be replaced by pilot-plant history.");

  s.addNotes(
    "Our use case is deliberately narrow: not 'the chemical industry', but the 25 worst centrifugal pumps in one mid-size speciality-chemicals plant. " +
    "Using our assumption register — 500 crore revenue, 8,000 hours — each hour down costs about 1.9 lakh in contribution margin. " +
    "Sixty hours of pump-caused outage plus twelve repairs a year is roughly 1.4 crore of annual exposure. These are labelled estimates; phase zero of the pilot replaces them with the plant's own 24-month history. " +
    "The root cause is structural: the classic reliability-centred-maintenance finding is that 89 percent of failure modes show no fixed wear-out age, so calendar-based maintenance is blind to them. " +
    "Bearings and seals — which dominate pump failures — degrade over weeks. That window is our opportunity. [~70 s]");
}

// =====================================================================
// SLIDE 3 — Benchmark & gap
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Existing approaches · global best practice · the gap", TEAL);
  title(s, [
    { t: "Continuous monitoring is proven worldwide — but OEM cloud lock-in prices out mid-size Indian plants: the gap is an " },
    { t: "open, plant-owned stack", accent: true },
  ], { h: 1.1, size: 24 });

  // Comparison table
  const hdr = { fill: { color: NAVY }, color: "FFFFFF", bold: true, fontSize: 11, valign: "middle" };
  const c = (t, o = {}) => ({ text: t, options: { fontFace: FONT, fontSize: 11, color: NAVY, valign: "middle", ...o } });
  const rows = [
    [c("Approach", hdr), c("Detection lead time (30)", hdr), c("Total cost of ownership (20)", hdr), c("Skill dependence (10)", hdr), c("Data ownership (10)", hdr), c("Retrofit ease (10)", hdr), c("MSME scalability (20)", hdr), c("Score /5", hdr)],
    [c("Reactive (run-to-failure)"), c("None"), c("Poor — downtime pays"), c("Low"), c("—"), c("—"), c("Poor"), c("2.3")],
    [c("Calendar preventive (Indian default)"), c("None for random faults"), c("Medium"), c("Low"), c("—"), c("—"), c("Medium"), c("3.0")],
    [c("Monthly offline vibration rounds"), c("≤ route interval"), c("Medium"), c("High (analyst)"), c("Plant"), c("Good"), c("Poor"), c("2.9")],
    [c("OEM / proprietary cloud monitoring"), c("Days–weeks"), c("High (per-point + subscription)"), c("Low"), c("Vendor silo"), c("Medium"), c("Poor"), c("2.9")],
    [c("Open edge stack (proposed)", { bold: true, color: GREEN }), c("Days–weeks", { bold: true }), c("Low–medium", { bold: true }), c("Medium", { bold: true }), c("Plant-owned", { bold: true, color: GREEN }), c("Good", { bold: true }), c("Good — shared clusters", { bold: true }), c("4.3", { bold: true, color: GREEN })],
  ];
  s.addTable(rows, {
    x: MX, y: 1.62, w: CW, colW: [2.6, 1.75, 2.1, 1.35, 1.3, 1.15, 1.55, 0.7],
    border: { type: "solid", color: BORDER, pt: 0.75 },
    fontFace: FONT, rowH: 0.4, valign: "middle", margin: 0.06,
    fill: { color: "FFFFFF" },
    autoPage: false,
  });
  s.addText("Weights in brackets (sum 100); scores 1–5 are team judgment from the sourced characteristics of each approach — full scoring note in our research log.",
    { x: MX, y: 4.42, w: CW, h: 0.25, fontFace: FONT, fontSize: 9.5, italic: true, color: GREY, isTextBox: true, margin: 0 });

  // Design principles
  card(s, MX, 4.85, CW, 1.7, LIGHT);
  sectionHead(s, MX + 0.22, 5.0, 8.0, "FIVE DESIGN PRINCIPLES THIS ANALYSIS FIXES", GREEN);
  const dp = [
    "Continuous, not periodic — no month-long blind windows",
    "Interpretable features a reliability engineer can audit — no black box",
    "Open protocols (OPC UA) and plant-owned data — no vendor silo",
    "Ex-certified wireless retrofit — no shutdown, no cabling",
    "Human-in-loop: every alert becomes a CMMS work order, never an automatic action",
  ];
  body(s, MX + 0.22, 5.32, CW - 0.5, 1.15, dp.slice(0, 3), { size: 12.5, space: 3 });
  body(s, MX + 6.5, 5.32, CW - 6.6, 1.15, dp.slice(3), { size: 12.5, space: 3 });

  footer(s,
    "Sources: [3] US DOE FEMP, O&M Best Practices Guide R3.0, 2010 (PdM effectiveness ranges). [7] ISO 17359:2018, ISO 13374-1:2003 (condition-monitoring practice). Approach characteristics: vendor/product-class documentation reviewed in research log; scores are team judgment.");

  s.addNotes(
    "We compared five realistic approaches on the six criteria that actually decide adoption, with detection lead time and MSME scalability weighted highest. " +
    "Reactive and calendar-based maintenance fail on lead time — that is the current Indian default. Monthly offline rounds help but leave four-week blind windows and depend on scarce analysts. " +
    "Global best practice — continuous OEM cloud monitoring — is technically excellent but scores poorly for India: high per-point cost, subscriptions, and the plant's own condition data locked in a vendor silo. " +
    "So the gap is not a sensing gap or an algorithm gap; it is an architecture-and-affordability gap. " +
    "That analysis gives us five design principles — continuous, interpretable, open, retrofit-friendly, human-in-loop — and those principles, not a product preference, define NAADI. [~70 s]");
}

// =====================================================================
// SLIDE 4 — Proposed solution architecture
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Proposed solution", GREEN);
  title(s, [
    { t: "NAADI is a four-layer retrofit: " },
    { t: "sense → edge → learn → act", accent: true },
    { t: ", closing the loop from bearing vibration to a planned CMMS work order" },
  ], { h: 0.85, size: 24, accent: GREEN });

  const layY = 1.75, layH = 3.1, gap = 0.22;
  const layW = (CW - 3 * gap - 0.55) / 4;
  const layers = [
    {
      name: "1 · SENSE", tag: "proven", tagColor: GREY,
      items: ["Wireless tri-axial vibration + temperature sensor on each bearing housing (DE + NDE)", "Ex/intrinsically-safe certified for hazardous areas (PESO-approved for India)", "Magnet-mount: installed in normal operation, no cabling, no shutdown"],
    },
    {
      name: "2 · EDGE", tag: "adapted", tagColor: TEAL,
      items: ["Gateway per plant area; vibration snapshot every 10 min, temperature every 1 min", "Extracts 16 interpretable features per window (RMS, kurtosis, crest, band energies) per ISO 13374 [7]", "ISO 20816-3 velocity zones give day-one alarm limits before any data accumulates [7]"],
    },
    {
      name: "3 · LEARN", tag: "new for this context", tagColor: GREEN,
      items: ["Tier 1: per-pump anomaly score against its own healthy baseline", "Tier 2: fault-type classifier (bearing race / rolling-element / imbalance signatures) — our prototype: 97.9% on unseen load [6]", "Retrained from confirmed maintenance findings — the loop learns the plant"],
    },
    {
      name: "4 · ACT", tag: "adapted", tagColor: TEAL,
      items: ["Alert → auto-drafted CMMS work order with evidence plot attached", "Reliability engineer validates — human decides, always", "Weekly review: alert precision tracked as a plant KPI, not a vendor claim"],
    },
  ];
  layers.forEach((L2, i) => {
    const x = MX + i * (layW + gap);
    card(s, x, layY, layW, layH, i === 2 ? "F0F7F3" : WHITE);
    s.addText(L2.name, { x: x + 0.14, y: layY + 0.12, w: layW - 0.28, h: 0.26, fontFace: FONT, fontSize: 13, bold: true, color: NAVY, isTextBox: true, margin: 0 });
    s.addText(L2.tag, { x: x + 0.14, y: layY + 0.4, w: layW - 0.28, h: 0.2, fontFace: FONT, fontSize: 9, bold: true, color: L2.tagColor, charSpacing: 1, isTextBox: true, margin: 0 });
    body(s, x + 0.14, layY + 0.68, layW - 0.28, layH - 0.8, L2.items, { size: 11, space: 5 });
    if (i < 3) {
      s.addShape(pres.ShapeType.line, { x: x + layW + 0.015, y: layY + layH / 2, w: gap - 0.03, h: 0, line: { color: GREEN, width: 2.5, endArrowType: "triangle" } });
    }
  });
  // feedback loop arrow (learn <- act findings)
  s.addShape(pres.ShapeType.line, { x: MX + 1.2, y: layY + layH + 0.14, w: CW - 2.4, h: 0, line: { color: GREY, width: 1.5, dashType: "dash", beginArrowType: "triangle" } });
  s.addText("feedback: confirmed findings retrain the models and tighten alarm limits",
    { x: MX + 1.2, y: layY + layH + 0.2, w: CW - 2.4, h: 0.22, fontFace: FONT, fontSize: 10, italic: true, color: GREY, align: "center", isTextBox: true, margin: 0 });

  // Why this is different
  card(s, MX, 5.5, CW, 1.18, LIGHT);
  sectionHead(s, MX + 0.22, 5.62, 6.0, "WHY THIS IS DIFFERENT — THREE DEFENSIBLE POINTS", GREEN);
  s.addText([
    { text: "Openly validated: ", options: { bold: true, color: NAVY } },
    { text: "detection metrics published from a public benchmark with reproducible code — judge the evidence, not a brochure [6].   ", options: { color: NAVY } },
    { text: "Plant-owned: ", options: { bold: true, color: NAVY } },
    { text: "open protocols, models and data stay with the plant — no subscription lock-in.   ", options: { color: NAVY } },
    { text: "Priced for India: ", options: { bold: true, color: NAVY } },
    { text: "~₹1.5 lakh per pump all-in (est.), an architecture MSME clusters can share.", options: { color: NAVY } },
  ], { x: MX + 0.22, y: 5.9, w: CW - 0.5, h: 0.7, fontFace: FONT, fontSize: 12.5, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });

  footer(s,
    "Sources: [6] Prototype trained on CWRU Bearing Data Center public dataset — engineering.case.edu/bearingdatacenter (metrics: slide 5). [7] ISO 20816-3:2022; ISO 13374-1:2003. Layer tags: grey = established practice, teal = adapted to this context, green = new contribution. Cost/pump: team estimate.");

  s.addNotes(
    "The architecture is four layers, and we are explicit about what is ours and what is not. Sensing is commodity and proven — Ex-certified wireless accelerometers that magnet-mount during normal operation. " +
    "The edge layer computes sixteen interpretable condition indicators, and ISO 20816 velocity zones give usable alarm limits from day one, before any learning. " +
    "The learning layer is our contribution: an anomaly tier per pump, plus a fault-type classifier whose honest, leakage-free benchmark results we show next slide. " +
    "The act layer keeps a human in the loop — every alert becomes a drafted work order that the reliability engineer accepts or rejects, and those decisions retrain the system. " +
    "Three differences we will defend: openly validated metrics, plant-owned data, and a cost architecture — about one and a half lakh per pump — that a cluster of MSMEs can realistically share. [~75 s]");
}

// =====================================================================
// SLIDE 5 — Technical feasibility
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Technical feasibility", TEAL);
  title(s, [
    { t: "A prototype we trained on the public CWRU benchmark separates faulty from healthy bearings with " },
    { t: "zero false alarms", accent: true },
    { t: " — under leakage-free evaluation on an unseen load" },
  ], { h: 1.1, size: 24 });

  // Left: mechanism + eval note
  card(s, MX, 1.7, 5.75, 3.0);
  sectionHead(s, MX + 0.22, 1.85, 5.3, "MECHANISM — WHY VIBRATION WORKS", TEAL);
  body(s, MX + 0.22, 2.18, 5.35, 1.6, [
    "A spalling bearing race strikes every rolling element at a defect-specific frequency; energy shifts into characteristic bands and the signal turns impulsive (kurtosis, crest factor rise).",
    "16 classical indicators per 0.17 s window — every input auditable by a vibration analyst; a random forest maps them to fault classes.",
  ], { size: 12.5, space: 5 });
  s.addShape(pres.ShapeType.roundRect, { x: MX + 0.22, y: 3.85, w: 5.3, h: 0.72, rectRadius: 0.05, fill: { color: "FDF3E1" }, line: { color: AMBER, width: 1 } });
  s.addText([
    { text: "Evaluation honesty: ", options: { bold: true, color: AMBER_DARK } },
    { text: "no random window splits (they leak near-duplicates). We hold out whole recordings and an entire unseen 3 hp load condition.", options: { color: NAVY } },
  ], { x: MX + 0.36, y: 3.92, w: 5.05, h: 0.6, fontFace: FONT, fontSize: 11.5, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.03 });

  // Right: results table
  card(s, MX + 6.0, 1.7, 6.23, 3.0);
  sectionHead(s, MX + 6.22, 1.85, 5.8, "PROTOTYPE RESULTS — CWRU BENCHMARK [6]", TEAL);
  const hdr2 = { fill: { color: LIGHT }, color: NAVY, bold: true, fontSize: 10.5, valign: "middle" };
  const d = (t, o = {}) => ({ text: t, options: { fontFace: FONT, fontSize: 10.5, color: NAVY, valign: "middle", ...o } });
  s.addTable([
    [d("Metric (test = unseen 3 hp load)", hdr2), d("Result", hdr2), d("Protocol", hdr2)],
    [d("Fault vs healthy — precision / recall"), d("100% / 100%", { bold: true, color: GREEN }), d("1,123 windows")],
    [d("Healthy windows misflagged"), d("0 of 237", { bold: true, color: GREEN }), d("false-alarm proxy")],
    [d("4-class fault-type accuracy"), d("97.9%", { bold: true }), d("fault-type mixups only")],
    [d("Grouped 5-fold CV (by recording)"), d("98.9%", { bold: true }), d("no recording crosses folds")],
    [d("Logistic baseline (same features)"), d("97.2%"), d("features carry the signal")],
  ], {
    x: MX + 6.22, y: 2.12, w: 5.8, colW: [2.75, 1.25, 1.8],
    border: { type: "solid", color: BORDER, pt: 0.75 },
    fontFace: FONT, rowH: 0.32, margin: 0.045, autoPage: false,
  });
  s.addText("64 recordings → 4,367 windows · 12 kHz drive-end accel. · code + metrics in our open repository",
    { x: MX + 6.22, y: 4.44, w: 5.8, h: 0.2, fontFace: FONT, fontSize: 8.5, italic: true, color: GREY, isTextBox: true, margin: 0 });

  // Bottom: TRL + limitations
  card(s, MX, 4.95, 5.75, 1.75);
  sectionHead(s, MX + 0.22, 5.08, 5.3, "READINESS & INTEGRATION", TEAL);
  body(s, MX + 0.22, 5.38, 5.35, 1.25, [
    "Sensors, gateways, OPC UA, CMMS APIs: mature industrial products (TRL 9); the integrated NAADI workflow is TRL 6–7 — exactly what the pilot derisks.",
    "Alarm limits from ISO 20816-3 zones on day one; learning takes over as data accumulates [7].",
  ], { size: 12, space: 4 });

  s.addShape(pres.ShapeType.roundRect, { x: MX + 6.0, y: 4.95, w: 6.23, h: 1.75, rectRadius: 0.055, fill: { color: "FDF3E1" }, line: { color: AMBER, width: 1 } });
  sectionHead(s, MX + 6.22, 5.08, 5.8, "LIMITS WE ARE NOT HIDING", AMBER_DARK);
  body(s, MX + 6.22, 5.38, 5.8, 1.25, [
    "CWRU is a clean test rig with seeded faults — plant noise, variable speed and real degradations will cut performance; the pilot KPI is set at ≥70% detection, not 97%.",
    "Real failure examples are scarce at first → anomaly-first strategy; MEMS sensors trade bandwidth vs piezo — chosen for cost, validated in Phase 2.",
  ], { size: 12, space: 4 });

  footer(s,
    "Sources: [6] CWRU Bearing Data Center seeded-fault dataset, engineering.case.edu/bearingdatacenter; metrics computed by the team's code (open repository — train_fault_model.py). [7] ISO 20816-3:2022; ISO 13374-1:2003.");

  s.addNotes(
    "Why does this work technically? A defect in a bearing race strikes the rolling elements at a defect-specific frequency — energy moves into characteristic bands and the waveform becomes impulsive. Sixteen classical indicators capture that, and a random forest classifies it. " +
    "We did not take anyone's word for this: we trained the prototype ourselves on Case Western's public bearing benchmark. Under the strictest split — whole recordings held out, and an entire motor-load condition never seen in training — fault-versus-healthy separation is perfect on this benchmark, and fault-type accuracy is 97.9 percent. " +
    "One honesty point: most student projects quote random window splits, which leak near-identical windows into the test set. We refuse to. " +
    "And the limits are on the slide, not hidden: a test rig is not a plant, which is why our pilot success threshold is seventy percent early detection, not ninety-seven. [~75 s]");
}

// =====================================================================
// SLIDE 6 — Execution methodology & pilot
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Methodology for execution · pilot design", GREEN);
  title(s, [
    { t: "A six-month, " },
    { t: "shadow-mode pilot", accent: true },
    { t: " on 25 pumps proves the value before a single maintenance decision depends on it" },
  ], { h: 0.8, size: 24, accent: GREEN });

  // Timeline
  const phases = [
    ["P0 · M0–1", "Baseline", "24-month downtime & repair history from CMMS; criticality ranking (ISO 14224 [7]); freeze success criteria with plant"],
    ["P1 · M2", "Install & integrate", "50 sensor points + 5 gateways, magnet-mount in normal operation; historian link via OPC UA; hot-work & Ex permits"],
    ["P2 · M3", "Commission", "Per-pump healthy baselines; ISO 20816-3 alarm zones live; dashboards + CMMS work-order flow tested"],
    ["P3 · M3–6", "Shadow mode", "Alerts logged, not acted on; every alert adjudicated weekly against actual maintenance findings"],
    ["P4 · M6", "Go / No-Go gate", "KPIs met → alerts go live & scale plan; missed → root-cause review with published post-mortem"],
  ];
  const pw = (CW - 4 * 0.18) / 5;
  phases.forEach((p, i) => {
    const x = MX + i * (pw + 0.18);
    card(s, x, 1.6, pw, 2.5, i === 4 ? "F0F7F3" : WHITE);
    s.addText(p[0], { x: x + 0.12, y: 1.72, w: pw - 0.24, h: 0.22, fontFace: FONT, fontSize: 10, bold: true, color: GREEN, isTextBox: true, margin: 0 });
    s.addText(p[1], { x: x + 0.12, y: 1.95, w: pw - 0.24, h: 0.26, fontFace: FONT, fontSize: 13, bold: true, color: NAVY, isTextBox: true, margin: 0 });
    s.addText(p[2], { x: x + 0.12, y: 2.26, w: pw - 0.24, h: 1.75, fontFace: FONT, fontSize: 10.5, color: NAVY, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    if (i < 4) s.addShape(pres.ShapeType.line, { x: x + pw + 0.01, y: 2.85, w: 0.16, h: 0, line: { color: GREEN, width: 2, endArrowType: "triangle" } });
  });

  // KPIs + operations
  card(s, MX, 4.3, 6.6, 2.35, LIGHT);
  sectionHead(s, MX + 0.22, 4.44, 6.0, "GO / NO-GO KPIs — MEASURED, NOT CLAIMED", GREEN);
  body(s, MX + 0.22, 4.76, 6.2, 1.8, [
    "≥ 70% of confirmed developing faults flagged ≥ 14 days before functional failure",
    "≤ 2 false alerts per pump per month by month 6 (trust guardrail)",
    "100% of validated alerts become CMMS work orders within 24 h",
    "≥ 95% sensor data availability; baseline dataset handed to plant in open formats",
  ], { size: 12.5, space: 4 });

  card(s, MX + 6.85, 4.3, 5.38, 2.35);
  sectionHead(s, MX + 7.07, 4.44, 5.0, "OWNERS, DATA & DISRUPTION", TEAL);
  body(s, MX + 7.07, 4.76, 4.95, 1.8, [
    "Owners: plant reliability engineer (validation) · instrumentation team (install) · CMMS admin (workflow) · our team (features, models, dashboards)",
    "Monitoring: vibration every 10 min, temperature every 1 min, model scoring hourly, review weekly",
    "Zero production disruption: wireless magnet-mount fitting during routine access; shadow mode means no maintenance decision changes until the gate",
  ], { size: 12, space: 4 });

  footer(s,
    "Sources: [7] ISO 14224:2016 (criticality & reliability-data taxonomy); ISO 20816-3:2022. Pilot design: team proposal — decision gates and KPI thresholds to be frozen with the host plant in P0.");

  s.addNotes(
    "Execution is a six-month pilot designed around one principle: earn trust before touching anyone's maintenance schedule. " +
    "Phase zero builds the baseline from the plant's own CMMS history and freezes the success criteria jointly with the plant — so the pass bar is agreed before we install anything. " +
    "Installation is a month: wireless magnet-mount sensors fitted during routine access, no shutdown, with hazardous-area permits handled properly. " +
    "Then the crucial part: three months of shadow mode. Alerts are logged and adjudicated weekly against what maintenance actually finds — but nobody acts on them. The system earns its precision statistics in the open. " +
    "The month-six gate is numeric: seventy percent early detection, under two false alerts per pump-month, every alert becoming a work order within a day. Pass, and it goes live and scales. Fail, and we publish the post-mortem. Either way the plant keeps the data. [~75 s]");
}

// =====================================================================
// SLIDE 7 — Economic, environmental, risk feasibility
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Economic · environmental · risk feasibility", AMBER_DARK);
  title(s, [
    { t: "₹37 lakh installed, ~₹41 lakh net benefit a year: " },
    { t: "payback in about 11 months", accent: true },
    { t: ", and under 24 months even in the stacked downside" },
  ], { h: 0.8, size: 24, accent: AMBER_DARK });

  // Left: calculation logic
  card(s, MX, 1.6, 5.9, 3.3);
  sectionHead(s, MX + 0.22, 1.74, 5.4, "THE CALCULATION, NOT JUST THE ANSWER", AMBER_DARK);
  const mono = { fontFace: "Courier New", fontSize: 11.5, color: NAVY };
  s.addText([
    { text: "Lost margin  = ₹500Cr × 30% ÷ 8,000h = ₹1.9 L/h\n", options: mono },
    { text: "Downtime cut = 60h × 35% [3] × 1.9   = ₹39.4 L\n", options: mono },
    { text: "Repair save  = 12 × ₹2.5L × 10% [3] = ₹ 3.0 L\n", options: mono },
    { text: "Catastrophic avoided = 2 × ₹2.5L    = ₹ 5.0 L\n", options: mono },
    { text: "Benefit ₹47.4L − OpEx ₹6L            = ₹41.4 L/yr\n", options: { ...mono, bold: true } },
    { text: "CapEx ₹37L ÷ 41.4 × 12              ≈ 11 months\n", options: { ...mono, bold: true } },
    { text: "5-yr NPV @12% ≈ ₹1.1 Cr  ·  ₹0.64L per avoided hour", options: mono },
  ], { x: MX + 0.22, y: 2.06, w: 5.5, h: 1.95, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.18 });
  s.addText("CapEx: 50 Ex-rated sensor points (₹17.5 L) + 5 gateways (₹7.5 L) + integration (₹10 L) + training (₹2 L). DOE FEMP ranges applied at the low end [3]; plant figures are labelled estimates — full live-formula workbook in our repository.",
    { x: MX + 0.22, y: 4.1, w: 5.5, h: 0.72, fontFace: FONT, fontSize: 10, italic: true, color: GREY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.05 });

  // Right: sensitivity chart (native bar)
  card(s, MX + 6.15, 1.6, 6.08, 3.3);
  sectionHead(s, MX + 6.37, 1.74, 5.6, "SENSITIVITY — PAYBACK IN MONTHS", AMBER_DARK);
  s.addChart(pres.ChartType.bar, [{
    name: "Payback (months)",
    labels: ["Downside stack: 20% cut + CapEx +30%", "Downtime cut only 20%", "Lost margin 1/3 lower", "CapEx +30%", "Base case (35% cut)", "DOE top of band (45% cut)"],
    values: [23.6, 18.1, 15.7, 14.0, 10.7, 8.4],
  }], {
    x: MX + 6.32, y: 2.05, w: 5.75, h: 2.7,
    barDir: "bar", chartColors: [AMBER],
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: NAVY, dataLabelFontSize: 10, dataLabelFontFace: FONT,
    showLegend: false, showTitle: false,
    catAxisLabelColor: NAVY, catAxisLabelFontSize: 9.5, catAxisLabelFontFace: FONT,
    valAxisLabelColor: GREY, valAxisLabelFontSize: 9, valAxisLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 26, valAxisMajorUnit: 6,
    valGridLine: { color: BORDER, size: 0.5 }, catGridLine: { style: "none" },
    barGapWidthPct: 45,
  });

  // Bottom: environment + risks
  card(s, MX, 5.02, 5.9, 1.62);
  sectionHead(s, MX + 0.22, 5.14, 5.4, "ENVIRONMENT & SAFETY GAINS", GREEN);
  body(s, MX + 0.22, 5.44, 5.5, 1.1, [
    "Seal failures are a leading release path [5]: early detection means fewer leak events, spills and emergency flaring/venting.",
    "Pumping ≈ 20% of world electric-motor demand [10]: the same condition data flags cavitation and off-BEP running for energy fixes.",
  ], { size: 11.5, space: 4 });

  card(s, MX + 6.15, 5.02, 6.08, 1.62);
  sectionHead(s, MX + 6.37, 5.14, 5.6, "TOP RISKS → SPECIFIC MITIGATIONS", AMBER_DARK);
  body(s, MX + 6.37, 5.44, 5.65, 1.1, [
    "False alarms erode trust → shadow mode + ≤2/pump-month gate.  Hazardous areas → PESO/IECEx intrinsically-safe sensors only.",
    "OT cybersecurity → one-way data flow, segregated network.  Skills → weekly analyst review + operator training in CapEx.",
  ], { size: 11.5, space: 4 });

  footer(s,
    "Sources: [3] US DOE FEMP, O&M Best Practices Guide R3.0, 2010 — PdM: 35–45% downtime reduction, 8–12% saving vs preventive. [5] McKee et al., ICOMS 2011. [10] Hydraulic Institute, Europump & US DOE, Pump Life Cycle Costs, 2001. All plant-specific values: labelled team estimates (assumption register + live workbook).");

  s.addNotes(
    "The economics are shown as the calculation, not just the answer. Every hour of avoided downtime is worth about 1.9 lakh in contribution margin. Applying the Department of Energy's published effectiveness ranges at the conservative end — 35 percent downtime reduction, 10 percent repair savings — the annual benefit is about 47 lakh against 6 lakh of operating cost. " +
    "Against 37 lakh of CapEx, that is an eleven-month payback and roughly 1.1 crore of five-year NPV at a twelve percent discount rate. " +
    "We stress-tested it: if the programme only achieves 20 percent reduction — below DOE's band — or CapEx overruns 30 percent, payback stays under 24 months. Both together: still under two years. " +
    "Environmentally, fewer seal blow-outs mean fewer releases, and the same data stream exposes cavitation and off-best-efficiency operation for energy savings. " +
    "The risk we respect most is false alarms killing operator trust — that is exactly why the pilot runs in shadow mode with a hard false-alert gate. [~75 s]");
}

// =====================================================================
// SLIDE 8 — Evidence, validation, way forward
// =====================================================================
{
  const s = newSlide();
  kicker(s, "Supporting evidence · way forward", TEAL);
  title(s, [
    { t: "Benchmark-validated today, plant-validated in six months — then an " },
    { t: "open reliability stack", accent: true },
    { t: " India's chemical clusters can share" },
  ], { h: 0.8, size: 24 });

  // Evidence columns
  card(s, MX, 1.6, 6.0, 2.2);
  sectionHead(s, MX + 0.22, 1.74, 5.5, "VALIDATED ALREADY (SOURCED / COMPUTED)", GREEN);
  body(s, MX + 0.22, 2.06, 5.6, 1.65, [
    "Effectiveness band: 35–45% downtime cut for working PdM programmes — US DOE FEMP [3]",
    "Failure logic: 89% of failure modes not age-related; bearings/seals dominate pumps [4][5]",
    "Detection: our prototype, leakage-free evaluation on public CWRU benchmark — 97.9% unseen-load accuracy, 0 false alarms [6]",
    "Standards path exists: ISO 20816-3 · 13374 · 17359 · 14224 [7]",
  ], { size: 11.5, space: 4 });

  card(s, MX + 6.25, 1.6, 5.98, 2.2);
  sectionHead(s, MX + 6.47, 1.74, 5.5, "STILL NEEDS PILOT PROOF (WE SAID SO ON EVERY SLIDE)", AMBER_DARK);
  body(s, MX + 6.47, 2.06, 5.55, 1.65, [
    "Detection lead time and false-alert rate under real plant noise and variable operation",
    "The 60 h/yr baseline and ₹1.9 L/h margin — replaced by the host plant's actual history in P0",
    "Indian installed cost points (sensor quotes, Ex certification, integration effort)",
    "Model transfer from benchmark features to plant-specific baselines",
  ], { size: 11.5, space: 4 });

  // Roadmap
  const ry = 4.05, rh = 1.15;
  const steps = [
    ["M0–6", "Pilot", "25 pumps, one plant · shadow → live at the gate"],
    ["M6–12", "Plant-wide", "100+ assets: compressors, agitators, fans · plant reliability dashboard"],
    ["M12–24", "Cluster scale", "Shared-service model for MSME chemical clusters · aligned with SAMARTH Udyog centres & NM-ICPS hubs [8][9]"],
  ];
  const rw = (CW - 2 * 0.2) / 3;
  steps.forEach((p, i) => {
    const x = MX + i * (rw + 0.2);
    card(s, x, ry, rw, rh, i === 2 ? "F0F7F3" : WHITE);
    s.addText([
      { text: p[0] + "  ", options: { bold: true, color: TEAL } },
      { text: p[1], options: { bold: true, color: NAVY } },
    ], { x: x + 0.14, y: ry + 0.08, w: rw - 0.28, h: 0.24, fontFace: FONT, fontSize: 12.5, isTextBox: true, margin: 0 });
    s.addText(p[2], { x: x + 0.14, y: ry + 0.34, w: rw - 0.28, h: 0.75, fontFace: FONT, fontSize: 10.5, color: NAVY, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: x + rw + 0.02, y: ry + rh / 2, w: 0.16, h: 0, line: { color: TEAL, width: 2, endArrowType: "triangle" } });
  });

  // Ask + takeaway
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: 5.42, w: 7.35, h: 1.25, rectRadius: 0.055, fill: { color: NAVY } });
  s.addText([
    { text: "Our ask of industry — one pilot partner: ", options: { bold: true, color: "F7B84B" } },
    { text: "25 critical pumps, 12 months of CMMS & historian history, and site access for 6 months. We bring sensors, models, dashboards and open code — the plant keeps the data, the models and the results, published either way.", options: { color: WHITE } },
  ], { x: MX + 0.25, y: 5.52, w: 6.9, h: 1.05, fontFace: FONT, fontSize: 13, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.1 });

  card(s, MX + 7.6, 5.42, 4.63, 1.25, "F0F7F3");
  s.addText([
    { text: "If the jury remembers one line: ", options: { bold: true, color: GREEN, breakLine: true } },
    { text: "Listen to the machines before they stop the plant — ₹37 lakh, 11-month payback, and the plant keeps the brains.", options: { color: NAVY, italic: true } },
  ], { x: MX + 7.82, y: 5.52, w: 4.2, h: 1.05, fontFace: FONT, fontSize: 12.5, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.08 });

  footer(s,
    "Sources: [2] PIB/DCPC — Indian chemicals & petrochemicals demand headed to ~USD 1 trillion by 2040 (pib.gov.in, 2023): reliability is a sector-scale lever. [3][4][5][6][7] as cited. [8] NITI Aayog Nat'l Strategy for AI, 2018; DST NM-ICPS, 2018 (₹3,660 Cr). [9] MHI SAMARTH Udyog Bharat 4.0. Full claim-by-claim register in our research log.");

  s.addNotes(
    "To close: what is already proven, and what is not. Proven, with sources: the DOE effectiveness band, the reliability-engineering failure logic, a standards pathway — and our own prototype's detection numbers on a public benchmark, reproducible from code we publish. " +
    "Not yet proven, and we have said so on every slide: real-plant lead times, false-alarm rates, and Indian cost points. That is precisely what the six-month pilot measures. " +
    "The roadmap after the pilot: plant-wide coverage in a year, and by month 24 a shared-service model for MSME chemical clusters, aligned with the SAMARTH Udyog Industry 4.0 centres — because a cluster sharing one edge stack is how this reaches plants that could never buy an OEM cloud contract. " +
    "Our ask is one pilot partner: 25 pumps, their maintenance history, six months of access. We bring everything else, and the plant keeps the data and the models, with results published either way. " +
    "One line to remember: listen to the machines before they stop the plant — 37 lakh, eleven-month payback, and the plant keeps the brains. Thank you. [~75 s]");
}

pres.writeFile({ fileName: "India_Chem_2026_NITW_Raunak_Anushriya.pptx" })
  .then(() => console.log("deck written"));
