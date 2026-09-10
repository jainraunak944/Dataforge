// Infographic design system (reference-matched): white bg, one vivid brand hue + black,
// icon chips, stat cards with soft shadows, numbered badges, takeaway ribbons.

const C = {
  brand: "1568DC",     // vivid water blue
  brandDk: "0C3E86",   // deep blue (numbers, emphasis)
  ink: "16202B",       // near-black headlines/body
  gray: "55616D",      // secondary text
  faint: "8C99A6",     // captions/footnotes
  line: "DCE5EE",      // hairlines
  tint: "E8F1FC",      // light blue chip/panel
  tint2: "F5F9FE",     // lighter panel
  green: "129454",     // eco/positive
  greenT: "E4F5EB",
  amber: "ED9B12",     // highlight
  amberT: "FCF1DA",
  red: "D64226",       // risk
  redT: "FBE8E3",
  white: "FFFFFF",
  // competitor column colours
  daiki: "D95F2B", ionx: "7C4DBE", thermax: "A16A1B", susbio: "2E9E5B", banka: "18809B", ncr: "6B7A89",
};

const PAGE = { w: 13.333, h: 7.5, mL: 0.5, mR: 0.5 };
const F = "Arial";

const shadow = () => ({ type: "outer", color: "A8B4C2", blur: 7, offset: 2, angle: 90, opacity: 0.38 });
const shadowSm = () => ({ type: "outer", color: "B6C1CD", blur: 4, offset: 1, angle: 90, opacity: 0.3 });

// white rounded card with soft shadow
function card(s, x, y, w, h, opts = {}) {
  s.addShape("roundRect", {
    x, y, w, h, rectRadius: opts.r === undefined ? 0.08 : opts.r,
    fill: { color: opts.fill || C.white },
    line: opts.noLine ? { type: "none" } : { color: opts.lineColor || C.line, width: opts.lineW || 1 },
    shadow: opts.noShadow ? undefined : shadow(),
  });
}

// icon chip: rounded-square tint + centred icon image
function chip(s, ICONS, key, x, y, size, opts = {}) {
  s.addShape("roundRect", {
    x, y, w: size, h: size, rectRadius: size * 0.24,
    fill: { color: opts.bg || C.tint }, line: { type: "none" },
  });
  const pad = size * 0.21;
  s.addImage({ data: ICONS[key], x: x + pad, y: y + pad, w: size - 2 * pad, h: size - 2 * pad });
}

// two-tone page header with numbered deliverable badge + underline + wordmark; returns content top y
function header2(s, num, kicker, tBlack, tBlue, page) {
  if (num) {
    s.addShape("ellipse", { x: PAGE.mL, y: 0.34, w: 0.42, h: 0.42, fill: { color: C.brand }, line: { type: "none" } });
    s.addText(num, { x: PAGE.mL, y: 0.345, w: 0.42, h: 0.42, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F, fontSize: 17, bold: true, color: "FFFFFF" });
  }
  s.addText(kicker.toUpperCase(), {
    x: PAGE.mL + (num ? 0.56 : 0), y: 0.30, w: 8.5, h: 0.24, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 9.5, bold: true, color: C.gray, charSpacing: 2,
  });
  s.addText([
    { text: tBlack, options: { color: C.ink } },
    { text: tBlue, options: { color: C.brand } },
  ], {
    x: PAGE.mL + (num ? 0.56 : 0), y: 0.50, w: 11.0, h: 0.50, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 25, bold: true,
  });
  s.addShape("roundRect", { x: PAGE.mL + (num ? 0.56 : 0), y: 1.06, w: 0.85, h: 0.055, rectRadius: 0.02, fill: { color: C.brand }, line: { type: "none" } });
  // wordmark top-right
  s.addText([
    { text: "EPBL", options: { color: C.brand, bold: true, fontSize: 12 } },
    { text: "  ×  TEAM WOOKIES", options: { color: C.faint, bold: true, fontSize: 8.5, charSpacing: 1.5 } },
  ], { x: 9.6, y: 0.34, w: 3.23, h: 0.3, isTextBox: true, margin: 0, fontFace: F, align: "right" });
  s.addText("CASE CONSILIUM 2026", { x: 9.6, y: 0.60, w: 3.23, h: 0.2, isTextBox: true, margin: 0, fontFace: F, fontSize: 7.5, color: C.faint, charSpacing: 2, align: "right" });
  return 1.30;
}

// section heading: icon chip + bold heading
function sec2(s, ICONS, icon, text, x, y, opts = {}) {
  const size = 0.30;
  chip(s, ICONS, icon, x, y, size, { bg: opts.bg || C.tint });
  s.addText(text, {
    x: x + size + 0.12, y: y - 0.025, w: opts.w || 5, h: 0.36, isTextBox: true, margin: 0,
    fontFace: F, fontSize: opts.size || 13, bold: true, color: opts.color || C.brandDk, valign: "middle",
  });
}

// KPI stat card
function statCard(s, ICONS, x, y, w, h, icon, big, label, sub, subColor) {
  card(s, x, y, w, h);
  chip(s, ICONS, icon, x + 0.14, y + 0.16, 0.44);
  s.addText(big, { x: x + 0.70, y: y + 0.10, w: w - 0.8, h: 0.4, isTextBox: true, margin: 0, fontFace: F, fontSize: 20, bold: true, color: C.brandDk });
  s.addText(label, { x: x + 0.70, y: y + 0.50, w: w - 0.8, h: 0.34, isTextBox: true, margin: 0, fontFace: F, fontSize: 8, color: C.gray, lineSpacingMultiple: 1.0 });
  if (sub) s.addText(sub, { x: x + 0.14, y: y + h - 0.26, w: w - 0.28, h: 0.2, isTextBox: true, margin: 0, fontFace: F, fontSize: 8, bold: true, color: subColor || C.green });
}

// takeaway ribbon: solid brand band, white icon + white bold text
function ribbon(s, ICONS, iconWhiteKey, label, text, y, h = 0.46, size = 11.5) {
  s.addShape("roundRect", { x: PAGE.mL, y, w: 12.33, h, rectRadius: 0.09, fill: { color: C.brand }, line: { type: "none" }, shadow: shadowSm() });
  s.addImage({ data: ICONS[iconWhiteKey], x: PAGE.mL + 0.18, y: y + h / 2 - 0.13, w: 0.26, h: 0.26 });
  s.addText([
    { text: label.toUpperCase() + "   ", options: { color: "FFD98A", bold: true, fontSize: 10, charSpacing: 1.5 } },
    { text, options: { color: "FFFFFF", fontSize: size, bold: true } },
  ], { x: PAGE.mL + 0.56, y, w: 12.33 - 0.75, h, isTextBox: true, margin: 0, fontFace: F, valign: "middle", lineSpacingMultiple: 1.0 });
}

function footer2(s, source, page) {
  if (source) s.addText(source, { x: PAGE.mL, y: 7.13, w: 10.9, h: 0.3, isTextBox: true, margin: 0, fontFace: F, fontSize: 6.8, color: C.faint, lineSpacingMultiple: 1.0 });
  s.addText(String(page).padStart(2, "0"), { x: 12.45, y: 7.13, w: 0.4, h: 0.22, isTextBox: true, margin: 0, fontFace: F, fontSize: 9, bold: true, color: C.brand, align: "right" });
}

module.exports = { C, PAGE, F, card, chip, header2, sec2, statCard, ribbon, footer2, shadow, shadowSm };
