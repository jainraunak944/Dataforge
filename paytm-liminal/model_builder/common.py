"""Shared helpers for the Paytm x Liminal model builder."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment

FONT = "Arial"
BLUE = "0000FF"; BLACK = "000000"; GREEN = "008000"; RED = "FF0000"; GREY = "595959"; WHITE = "FFFFFF"
FILL_INPUT = PatternFill("solid", fgColor="FFFF00")        # key levers
FILL_CASE = PatternFill("solid", fgColor="DDEBF7")         # case facts
FILL_HDR = PatternFill("solid", fgColor="1F3864")          # section headers
FILL_SUB = PatternFill("solid", fgColor="D9E1F2")
FILL_OUT = PatternFill("solid", fgColor="E2EFDA")          # key outputs
FILL_WARN = PatternFill("solid", fgColor="FCE4D6")
FILL_EXT = PatternFill("solid", fgColor="FFF2CC")          # external facts
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)

F_INR = '#,##0;(#,##0);"-"'
F_INR1 = '#,##0.0;(#,##0.0);"-"'
F_INR2 = '#,##0.00;(#,##0.00);"-"'
F_PCT = '0.0%;(0.0%);"-"'
F_PCT0 = '0%;(0%);"-"'
F_X = '0.0"x";(0.0"x");"-"'
F_X2 = '0.00"x"'
F_EPS = '"₹"0.00;("₹"0.00);"-"'
F_YR = '0'
F_GEN = 'General'

class Book:
    def __init__(self):
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self.names = {}

    def sheet(self, title, tab_color=None, widths=None):
        ws = self.wb.create_sheet(title)
        ws.sheet_view.showGridLines = False
        if tab_color: ws.sheet_properties.tabColor = tab_color
        if widths:
            for col, w in widths.items():
                ws.column_dimensions[col].width = w
        return ws

    def name(self, nm, ws, cell):
        """Define a workbook-scoped name pointing at ws!cell (absolute)."""
        col = ''.join(ch for ch in cell if ch.isalpha()); row = ''.join(ch for ch in cell if ch.isdigit())
        ref = f"'{ws.title}'!${col}${row}"
        dn = DefinedName(nm, attr_text=ref)
        self.wb.defined_names[nm] = dn
        self.names[nm] = ref
        return nm

def style(c, bold=False, color=BLACK, fill=None, fmt=None, italic=False, size=10, align=None, wrap=False, border=False):
    c.font = Font(name=FONT, bold=bold, color=color, italic=italic, size=size)
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    if align or wrap: c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if border: c.border = BOX
    return c

def header(ws, row, text, ncols=12, size=12):
    c = ws.cell(row=row, column=1, value=text)
    style(c, bold=True, color=WHITE, fill=FILL_HDR, size=size)
    for j in range(2, ncols + 1):
        style(ws.cell(row=row, column=j), fill=FILL_HDR)
    ws.row_dimensions[row].height = 18
    return row + 1

def subheader(ws, row, text, ncols=12):
    c = ws.cell(row=row, column=1, value=text)
    style(c, bold=True, fill=FILL_SUB)
    for j in range(2, ncols + 1):
        style(ws.cell(row=row, column=j), fill=FILL_SUB)
    return row + 1

def note(ws, row, text, col=1, italic=True, color=GREY, wrap=False):
    c = ws.cell(row=row, column=col, value=text)
    style(c, italic=italic, color=color, wrap=wrap)
    return row + 1

def label(ws, row, text, col=1, bold=False, indent=0):
    c = ws.cell(row=row, column=col, value=("   " * indent) + text)
    style(c, bold=bold)
    return c

def inp(ws, row, col, value, fmt=F_INR, kind="assump", comment=None):
    """kind: case (blue text, light-blue fill), assump (blue text, yellow fill), ext (blue text, orange fill)"""
    c = ws.cell(row=row, column=col, value=value)
    fill = {"case": FILL_CASE, "assump": FILL_INPUT, "ext": FILL_EXT, "plain": None}[kind]
    style(c, color=BLUE, fill=fill, fmt=fmt, border=True)
    if comment:
        c.comment = Comment(comment, "Deal team")
    return c

def calc(ws, row, col, formula, fmt=F_INR, bold=False, fill=None, color=BLACK, border=False):
    c = ws.cell(row=row, column=col, value=formula)
    style(c, bold=bold, fill=fill, fmt=fmt, color=color, border=border)
    return c

def link(ws, row, col, formula, fmt=F_INR, bold=False):
    return calc(ws, row, col, formula, fmt=fmt, bold=bold, color=GREEN)

def out(ws, row, col, formula, fmt=F_INR, bold=True):
    return calc(ws, row, col, formula, fmt=fmt, bold=bold, fill=FILL_OUT, border=True)

def text(ws, row, col, value, bold=False, color=BLACK, wrap=False, italic=False, fill=None):
    c = ws.cell(row=row, column=col, value=value)
    style(c, bold=bold, color=color, wrap=wrap, italic=italic, fill=fill)
    return c

def col(n):
    return get_column_letter(n)
