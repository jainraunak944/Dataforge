// Design system for CaseConsilium_Wookies deck
// 16:9 wide = 13.333 x 7.5 in. White background, deep navy + teal + restrained green, amber highlight.

const C = {
  navy: "0B2E4F",      // primary: titles, headers, dark panels
  navy2: "123F63",     // lighter navy for chart series / subheads
  teal: "0E7C7B",      // secondary
  tealLt: "E7F2F1",    // teal tint panel background
  green: "3E7D5C",     // restrained green
  greenLt: "EAF3EE",   // green tint panel
  aqua: "5BA7A6",      // aqua mid-tone (charts)
  amber: "D98E1F",     // ONE highlight colour for key recommendations
  amberLt: "FBF1DE",   // amber tint panel
  ink: "26313B",       // body text
  mut: "5D6A75",       // muted text
  faint: "8A959E",     // footnotes
  line: "C9D3DA",      // hairlines
  panel: "F2F5F7",     // neutral light panel
  white: "FFFFFF",
  red: "B3442E",       // risk high (use sparingly, heatmap only)
  redLt: "F5E3DE",
  yellowLt: "FDF3D7",
};

const PAGE = { w: 13.333, h: 7.5, mL: 0.55, mR: 0.55, mT: 0.42 };
const FONT = "Calibri";

// Slide header: kicker + action title. Returns y where content starts.
function header(slide, kicker, title, opts = {}) {
  slide.addText(kicker.toUpperCase(), {
    x: PAGE.mL, y: 0.30, w: 12.23, h: 0.28, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 10.5, color: C.teal, charSpacing: 2, bold: true,
  });
  slide.addText(title, {
    x: PAGE.mL, y: 0.56, w: 12.23, h: opts.titleH || 0.62, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: opts.titleSize || 21, color: C.navy, bold: true, lineSpacingMultiple: 1.02,
  });
  return 0.56 + (opts.titleH || 0.62) + 0.10;
}

// Footer: source line left, team + page number right.
function footer(slide, sourceText, pageNum) {
  if (sourceText) {
    slide.addText(sourceText, {
      x: PAGE.mL, y: 7.08, w: 10.6, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 8, color: C.faint, valign: "top", lineSpacingMultiple: 1.0,
    });
  }
  slide.addText([
    { text: "Team Wookies", options: { color: C.faint, fontSize: 8 } },
    { text: "   " + String(pageNum).padStart(2, "0"), options: { color: C.mut, fontSize: 9, bold: true } },
  ], {
    x: 11.35, y: 7.12, w: 1.45, h: 0.26, isTextBox: true, margin: 0,
    fontFace: FONT, align: "right",
  });
}

// Conclusion band at bottom of a core slide ("so what")
function soWhat(slide, label, text, y, h = 0.52, size = 12.5) {
  slide.addShape("roundRect", {
    x: PAGE.mL, y, w: 12.23, h, rectRadius: 0.055, fill: { color: C.navy },
    line: { type: "none" },
  });
  slide.addText([
    { text: label.toUpperCase() + "   ", options: { color: C.amber, bold: true, fontSize: 10.5, charSpacing: 1.5 } },
    { text, options: { color: "FFFFFF", fontSize: size } },
  ], {
    x: PAGE.mL + 0.22, y, w: 12.23 - 0.44, h, isTextBox: true, margin: 0,
    fontFace: FONT, valign: "middle", lineSpacingMultiple: 1.03,
  });
}

// Small section label
function secLabel(slide, text, x, y, w, opts = {}) {
  slide.addText(text, {
    x, y, w, h: opts.h || 0.26, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: opts.size || 11.5, bold: true, color: opts.color || C.navy,
    charSpacing: opts.sp === undefined ? 0.5 : opts.sp,
  });
}

module.exports = { C, PAGE, FONT, header, footer, soWhat, secLabel };
