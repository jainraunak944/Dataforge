"""Slide-building helpers extending the Round 1 visual identity (see work/spec/style_spec.md)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
import re

# ---- palette (sampled from Round 1) ----
NAVY = RGBColor(0x00, 0x24, 0x44)      # headline navy (title slide)
NAVY2 = RGBColor(0x2C, 0x46, 0x62)     # section header navy
DEEPNAVY = RGBColor(0x00, 0x1D, 0x57)  # table header / numbered circles
GREEN = RGBColor(0x2A, 0x76, 0x5D)     # primary green accent
DEEPGREEN = RGBColor(0x01, 0x6F, 0x49)
DARKGREEN = RGBColor(0x0B, 0x3D, 0x2E)
MINT = RGBColor(0xC3, 0xED, 0xD9)
MINT2 = RGBColor(0xDD, 0xF1, 0xE3)
MINTPALE = RGBColor(0xE5, 0xF2, 0xEC)
GREY = RGBColor(0xE9, 0xE9, 0xE9)
GREY2 = RGBColor(0xE1, 0xE6, 0xED)
MIDGREY = RGBColor(0x78, 0x79, 0x74)
DARKGREY = RGBColor(0x3D, 0x3D, 0x3B)
LIGHTBLUE = RGBColor(0xDE, 0xE9, 0xF5)
CHARTBLUE = RGBColor(0x8C, 0xC5, 0xFC)
TAGBLUE = RGBColor(0x25, 0x6B, 0x98)
SUZUKIBLUE = RGBColor(0x15, 0x44, 0x8C)
YELLOW = RGBColor(0xFF, 0xF3, 0xB0)
AMBER = RGBColor(0xF5, 0xC2, 0x42)
RED = RGBColor(0xB0, 0x3A, 0x2E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
FONT = "Arial"

SLIDE_W = Inches(20)
SLIDE_H = Inches(11.25)
MARGIN = Inches(0.55)


def new_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE
    return s


def add_title_slide(prs, image_path):
    """Exact reproduction of Round 1 page 1: white page, native 1376x768 image placed as in the source PDF."""
    s = blank_slide(prs)
    s.shapes.add_picture(image_path, 0, Pt(3.1395), width=Pt(1440.0), height=Pt(804.0))
    return s


def _apply_runs(paragraph, text, size, color, bold=False, italic=False, font=FONT):
    """Supports **bold** and _italic_ markup inside text; subscript for H2 via 'H₂' literal."""
    parts = re.split(r'(\*\*.+?\*\*|__.+?__)', text)
    for part in parts:
        if not part:
            continue
        r = paragraph.add_run()
        if part.startswith('**') and part.endswith('**'):
            r.text = part[2:-2]
            r.font.bold = True
        elif part.startswith('__') and part.endswith('__'):
            r.text = part[2:-2]
            r.font.italic = True
        else:
            r.text = part
            r.font.bold = bold
            r.font.italic = italic
        r.font.size = Pt(size)
        r.font.name = font
        r.font.color.rgb = color


def textbox(slide, x, y, w, h, lines, size=18, color=DARKGREY, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, bullets=False, line_spacing=1.08, space_after=4, italic=False,
            margins=(0.05, 0.03, 0.05, 0.03), autofit=False, font=FONT):
    """lines: str or list of str (each a paragraph). A line may be a tuple (text, dict(size=, color=, bold=, bullet=, level=))."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    if isinstance(lines, str):
        lines = [lines]
    first = True
    for ln in lines:
        opts = {}
        if isinstance(ln, tuple):
            ln, opts = ln
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = opts.get('align', align)
        p.line_spacing = opts.get('line_spacing', line_spacing)
        p.space_after = Pt(opts.get('space_after', space_after))
        lvl = opts.get('level', 0)
        use_bullet = opts.get('bullet', bullets)
        txt = ln
        if use_bullet:
            txt = ("•  " if lvl == 0 else "–  ") + ln
            if lvl:
                p.level = 1
        _apply_runs(p, txt, opts.get('size', size), opts.get('color', color), opts.get('bold', bold), opts.get('italic', italic), font)
    return tb


def _strip_style(shp):
    from pptx.oxml.ns import qn
    st = shp._element.find(qn('p:style'))
    if st is not None:
        shp._element.remove(st)


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None, line_width=0.75):
    shp = slide.shapes.add_shape(shape, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = radius
    shp.shadow.inherit = False
    _strip_style(shp)
    shp.text_frame.text = ""
    return shp


def shape_text(shp, text, size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
               margins=(0.08, 0.03, 0.08, 0.03), font=FONT, line_spacing=1.0):
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        _apply_runs(p, ln, size, color, bold, font=font)
    return shp


HEADER_BOTTOM = {1: Inches(1.95), 2: Inches(2.35)}


def header(slide, headline, subline=None, wordmark=True, size=32):
    """Finding-based headline + one-line takeaway, Round 1 style (bold, upper band).
    Returns the y position where content may start."""
    n = len(headline)
    two = n > 64 or "\n" in headline
    if n > 165: size = 24
    elif n > 140: size = 26
    elif n > 64: size = 29
    textbox(slide, MARGIN, Inches(0.36), Inches(15.9), Inches(1.5 if two else 0.85), headline, size=size, color=NAVY, bold=True,
            anchor=MSO_ANCHOR.TOP, line_spacing=1.0, space_after=0)
    sub_y = Inches(1.6) if two else Inches(1.22)
    if subline:
        ssize = 18 if len(subline) <= 190 else 16
        textbox(slide, MARGIN, sub_y, Inches(16.2), Inches(0.62), subline, size=ssize, color=DARKGREY,
                line_spacing=1.0, space_after=0)
    rule_y = Inches(2.22) if two else Inches(1.82)
    if wordmark:
        # H2-SHIFT wordmark, top right, as on Round 1 pages 3-4
        tb = slide.shapes.add_textbox(Inches(16.7), Inches(0.35), Inches(2.9), Inches(1.0))
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = Inches(0.02)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        r = p.add_run(); r.text = "H"; r.font.size = Pt(30); r.font.bold = True; r.font.italic = True; r.font.name = FONT; r.font.color.rgb = SUZUKIBLUE
        r = p.add_run(); r.text = "₂"; r.font.size = Pt(30); r.font.bold = True; r.font.italic = True; r.font.name = FONT; r.font.color.rgb = SUZUKIBLUE
        r = p.add_run(); r.text = "-SHIFT"; r.font.size = Pt(30); r.font.bold = True; r.font.italic = True; r.font.name = FONT; r.font.color.rgb = DEEPGREEN
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.RIGHT
        r = p2.add_run(); r.text = "Convert. Don't Replace."; r.font.size = Pt(13); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = NAVY
    ln = slide.shapes.add_connector(1, MARGIN, rule_y, SLIDE_W - MARGIN, rule_y)
    ln.line.color.rgb = GREEN
    ln.line.width = Pt(1.5)
    _strip_style(ln)
    return rule_y + Inches(0.18)


def footer(slide, source_text, slide_no=None, width=Inches(14.6)):
    textbox(slide, MARGIN, Inches(10.52), width, Inches(0.6), source_text, size=12.5, color=MIDGREY,
            line_spacing=1.0, space_after=0)
    if slide_no is not None:
        textbox(slide, Inches(18.9), Inches(10.72), Inches(0.6), Inches(0.35), str(slide_no), size=11, color=MIDGREY,
                align=PP_ALIGN.RIGHT, space_after=0)


def panel(slide, x, y, w, h, title, fill=NAVY2, body_fill=WHITE, title_size=17, title_h=Inches(0.46), line=GREY2):
    """Rounded panel with a coloured header bar. Returns (body_x, body_y, body_w, body_h)."""
    outer = rect(slide, x, y, w, h, body_fill, line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
    rect(slide, x, y + int(title_h * 0.5), w, int(title_h * 0.5), fill)
    head = rect(slide, x, y, w, title_h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    textbox(slide, x + Inches(0.08), y, w - Inches(0.16), title_h, title, size=title_size, color=WHITE, bold=True,
            anchor=MSO_ANCHOR.MIDDLE, space_after=0, line_spacing=1.0)
    return x + Inches(0.12), y + title_h + Inches(0.08), w - Inches(0.24), h - title_h - Inches(0.16)


def stat_tile(slide, x, y, w, h, value, label, fill=MINT2, value_color=DEEPNAVY, value_size=30, label_size=14, note=None):
    rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    textbox(slide, x, y + Inches(0.05), w, Inches(0.6), value, size=value_size, color=value_color, bold=True,
            align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
    textbox(slide, x + Inches(0.05), y + Inches(0.62), w - Inches(0.1), h - Inches(0.65), label, size=label_size, color=DARKGREY,
            align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
    if note:
        textbox(slide, x, y + h - Inches(0.3), w, Inches(0.3), note, size=10.5, color=MIDGREY, align=PP_ALIGN.CENTER, space_after=0)


def table(slide, x, y, w, h, data, col_widths=None, header_fill=DEEPNAVY, font_size=14, header_size=14,
          highlight_col=None, highlight_fill=MINT2, row_fills=None, first_col_bold=True, align_center_from=1,
          bold_rows=(), row_heights=None):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, x, y, w, h)
    tbl = gt.table
    # disable banding style
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    tblPr.set('bandRow', '0'); tblPr.set('firstRow', '0')
    if col_widths:
        total = sum(col_widths)
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = int(w * cw / total)
    if row_heights:
        for i, rh in enumerate(row_heights):
            tbl.rows[i].height = rh
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            txt = data[r][c]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if (c >= align_center_from and r >= 0) else PP_ALIGN.LEFT
            if r == 0:
                _apply_runs(p, str(txt), header_size, WHITE, True)
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
                p.alignment = PP_ALIGN.CENTER if c >= align_center_from else PP_ALIGN.LEFT
            else:
                bold = (c == 0 and first_col_bold) or (r in bold_rows)
                _apply_runs(p, str(txt), font_size, DARKGREY if c else DEEPNAVY, bold)
                cell.fill.solid()
                if highlight_col is not None and c == highlight_col:
                    cell.fill.fore_color.rgb = highlight_fill
                elif row_fills and row_fills.get(r):
                    cell.fill.fore_color.rgb = row_fills[r]
                else:
                    cell.fill.fore_color.rgb = WHITE if r % 2 else RGBColor(0xF6, 0xF7, 0xF8)
    return tbl


def callout(slide, x, y, w, h, text, fill=YELLOW, color=DARKGREY, size=14, bold=False, align=PP_ALIGN.LEFT, line=None):
    shp = rect(slide, x, y, w, h, fill, line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    shape_text(shp, text, size=size, color=color, bold=bold, align=align, anchor=MSO_ANCHOR.MIDDLE, margins=(0.12, 0.05, 0.12, 0.05))
    return shp


def numbered_circle(slide, x, y, d, n, fill=DEEPNAVY, size=15):
    c = rect(slide, x, y, d, d, fill, shape=MSO_SHAPE.OVAL)
    shape_text(c, str(n), size=size, color=WHITE, bold=True, margins=(0, 0, 0, 0))
    return c


def chevron(slide, x, y, w, h, text, fill, color=WHITE, size=15, first=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.PENTAGON if first else MSO_SHAPE.CHEVRON, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    _strip_style(shp)
    shape_text(shp, text, size=size, color=color, bold=True, margins=(0.25, 0.02, 0.15, 0.02))
    return shp


def arrow(slide, x1, y1, x2, y2, color=GREEN, width=2.0):
    ln = slide.shapes.add_connector(1, x1, y1, x2, y2)
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    # add arrow head via XML
    from pptx.oxml.ns import qn
    lnxml = ln.line._get_or_add_ln()
    tail = lnxml.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
    lnxml.append(tail)
    return ln


def bar_chart(slide, x, y, w, h, categories, series, colors, number_format='0.0', title=None, legend=True,
              font_size=13, stacked=False, horizontal=False, gap_width=60, value_axis_title=None, max_val=None,
              data_labels=True, label_size=12, overlap=None):
    cd = CategoryChartData()
    cd.categories = categories
    for name, vals in series:
        cd.add_series(name, vals)
    if horizontal:
        ct = XL_CHART_TYPE.BAR_STACKED if stacked else XL_CHART_TYPE.BAR_CLUSTERED
    else:
        ct = XL_CHART_TYPE.COLUMN_STACKED if stacked else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = slide.shapes.add_chart(ct, x, y, w, h, cd)
    ch = gf.chart
    ch.font.size = Pt(font_size); ch.font.name = FONT
    ch.has_legend = legend and len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(font_size)
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(font_size + 1)
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.color.rgb = DEEPNAVY
    else:
        ch.has_title = False
    plot = ch.plots[0]
    plot.gap_width = gap_width
    if overlap is not None:
        plot.overlap = overlap
    if data_labels:
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format = number_format
        dl.number_format_is_linked = False
        dl.font.size = Pt(label_size)
        dl.font.color.rgb = DARKGREY
        if not stacked:
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
        else:
            dl.position = XL_LABEL_POSITION.CENTER
    for i, s in enumerate(plot.series):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = colors[i % len(colors)]
        s.format.line.fill.background()
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GREY
    va.major_gridlines.format.line.width = Pt(0.5)
    va.tick_labels.font.size = Pt(font_size)
    va.tick_labels.number_format = number_format
    va.tick_labels.number_format_is_linked = False
    va.format.line.fill.background()
    if max_val is not None:
        va.maximum_scale = max_val
        va.minimum_scale = 0
    if value_axis_title:
        va.has_title = True
        va.axis_title.text_frame.text = value_axis_title
        va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(font_size)
        va.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(font_size)
    ca.format.line.color.rgb = MIDGREY
    ca.has_major_gridlines = False
    return ch


def line_chart(slide, x, y, w, h, categories, series, colors, number_format='0', font_size=13, legend=True,
               value_axis_title=None, smooth=False, marker=True, min_val=None, max_val=None, data_labels=False):
    cd = CategoryChartData()
    cd.categories = categories
    for name, vals in series:
        cd.add_series(name, vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS if marker else XL_CHART_TYPE.LINE, x, y, w, h, cd)
    ch = gf.chart
    ch.font.size = Pt(font_size); ch.font.name = FONT
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(font_size)
    ch.has_title = False
    plot = ch.plots[0]
    for i, s in enumerate(plot.series):
        s.format.line.color.rgb = colors[i % len(colors)]
        s.format.line.width = Pt(2.5)
        s.smooth = smooth
        if marker:
            s.marker.format.fill.solid()
            s.marker.format.fill.fore_color.rgb = colors[i % len(colors)]
            s.marker.format.line.color.rgb = colors[i % len(colors)]
    if data_labels:
        plot.has_data_labels = True
        plot.data_labels.number_format = number_format
        plot.data_labels.number_format_is_linked = False
        plot.data_labels.font.size = Pt(font_size - 1)
        plot.data_labels.position = XL_LABEL_POSITION.ABOVE
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GREY
    va.tick_labels.font.size = Pt(font_size)
    va.tick_labels.number_format = number_format
    va.tick_labels.number_format_is_linked = False
    va.format.line.fill.background()
    if min_val is not None: va.minimum_scale = min_val
    if max_val is not None: va.maximum_scale = max_val
    if value_axis_title:
        va.has_title = True
        va.axis_title.text_frame.text = value_axis_title
        va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(font_size)
        va.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(font_size)
    ca.format.line.color.rgb = MIDGREY
    return ch


def picture(slide, path, x, y, w=None, h=None):
    return slide.shapes.add_picture(path, x, y, width=w, height=h)
