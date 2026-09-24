from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule, FormulaRule

FN='Times New Roman'
F=lambda **k: Font(name=FN, **k)
GREY=PatternFill('solid',fgColor='1F3864'); LBLUE=PatternFill('solid',fgColor='2F5597'); LGREEN=PatternFill('solid',fgColor='E2EFDA'); LYEL=PatternFill('solid',fgColor='FFF2CC'); WHITE=PatternFill('solid',fgColor='FFFFFF'); BAND=PatternFill('solid',fgColor='DDEBF7'); INFILL=PatternFill('solid',fgColor='FFF9DB'); PAGE=PatternFill('solid',fgColor='F7F9FC')
thin=Side(style='thin',color='8EA9DB'); BOX=Border(left=thin,right=thin,top=thin,bottom=thin); BOT=Border(bottom=Side(style='medium',color='000000'))
INPUT=F(color='0000FF'); LINK=F(color='008000'); BOLD=F(bold=True); HDR=F(bold=True); TITLE=F(bold=True,size=14); SUB=F(italic=True,size=10,color='595959')
NUM='#,##0;(#,##0);-'; NUM1='#,##0.0;(#,##0.0);-'; NUM2='#,##0.00;(#,##0.00);-'; PCT='0.0%;(0.0%);-'; MULT='0.0"x"'; RS='"₹"#,##0;("₹"#,##0);-'

wb=Workbook()
for k in ('creator','lastModifiedBy','title','subject','description','keywords','category','company','manager'):
    try: setattr(wb.properties,k,None)
    except Exception: pass
wb.properties.creator=''; wb.properties.lastModifiedBy=''

TABS={'Cover':'1F3864','Summary':'375623','Inputs':'BF8F00','Valuation & Churn':'2F5597','Financing & EPS':'2E75B6','Liminal Projection':'44546A','PAT & FCF Breakeven':'C00000','Call Option & Earn-out':'0E7C7B','Sensitivities':'7F6000'}
def sheet(name,widths):
    ws=wb.create_sheet(name)
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.sheet_view.showGridLines=True
    ws.sheet_properties.tabColor=TABS.get(name,'1F3864')
    return ws
def title(ws,t,sub):
    ws['B2']=t; ws['B2'].font=TITLE; ws['B3']=sub; ws['B3'].font=SUB
def hdr(ws,row,cols,vals,fill=GREY):
    for c,v in zip(cols,vals):
        cell=ws.cell(row=row,column=c,value=v); cell.font=F(bold=True,color='FFFFFF'); cell.fill=fill; cell.border=BOX; cell.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
def put(ws,ref,val,fmt=None,font=None,fill=None,bold=False,align=None,border=True):
    c=ws[ref]; c.value=val
    c.font=font or (F(bold=True) if bold else F())
    if fmt: c.number_format=fmt
    if fill: c.fill=fill
    elif font is INPUT: c.fill=INFILL
    if border: c.border=BOX
    if align: c.alignment=Alignment(horizontal=align,vertical='center',wrap_text=True)
    else:
        col=''.join(ch for ch in ref if ch.isalpha())
        c.alignment=Alignment(horizontal='left' if col=='B' and isinstance(val,str) else 'center',vertical='center',wrap_text=isinstance(val,str) and col!='B' and len(val)>28)
    return c
def section(ws,row,text,span=6):
    c=ws.cell(row=row,column=2,value=text); c.font=F(bold=True,size=11,color='FFFFFF'); c.fill=LBLUE; c.alignment=Alignment(vertical='center')
    for col in range(2,2+span): ws.cell(row=row,column=col).fill=LBLUE; ws.cell(row=row,column=col).border=BOX
def allfont(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name!=FN: c.font=F(bold=c.font.bold,italic=c.font.italic,color=c.font.color,size=c.font.size or 11)

# ================= COVER =================
ws=wb.active; ws.title='Cover'; ws.sheet_view.showGridLines=True; ws.sheet_properties.tabColor=TABS['Cover']
ws.column_dimensions['A'].width=3; ws.column_dimensions['B'].width=34; ws.column_dimensions['C'].width=80
ws['B2']='PROJECT SATOSHI GATE'; ws['B2'].font=F(bold=True,size=18)
ws['B3']='Paytm × Liminal Custody Solutions — Accretion/Dilution and Transaction Model'; ws['B3'].font=F(size=12)
ws['B4']='Board Transaction Recommendation · Team ETERNAL · September 2026'; ws['B4'].font=SUB
ws['B6']='Recommendation'; ws['B6'].font=BOLD
ws['C6']='Do not acquire 100% of Liminal today. Pursue a 20–30% strategic minority investment (25% midpoint) with a commercial custody/MPC partnership, standalone governance, a pre-agreed call option for future control and retention-linked future consideration.'; ws['C6'].alignment=Alignment(wrap_text=True,vertical='top'); ws['C6'].font=F()
ws.row_dimensions[6].height=48
r=8; ws.cell(row=r,column=2,value='Sheet').font=HDR; ws.cell(row=r,column=3,value='Purpose').font=HDR
for c in (2,3): ws.cell(row=r,column=c).fill=GREY; ws.cell(row=r,column=c).border=BOX
idx=[('1. Inputs','Case facts (source: case document) and team assumptions. Blue cells are the only cells to edit.'),
('2. Valuation & Churn','Headline multiple, churn sensitivity, implied value at 18.2× and revenue recovery hurdle.'),
('3. Financing & EPS','Full-acquisition financing mixes (cash / debt / equity), mechanical and full EPS dilution from the ₹7.50 baseline; Phase-1 minority structure.'),
('4. Liminal Projection','10-year Liminal ARR, EBITDA, PAT and FCF under team growth and margin assumptions; churned path for the full-acquisition counterfactual.'),
('5. PAT & FCF Breakeven','Incremental PAT and FCF by year for full acquisition, Phase-1 minority and control exercise; ₹750 Cr capital drag; ₹115 Cr UPI MDR treated as a Paytm standalone offset.'),
('6. Call Option & Earn-out','Retention-linked control consideration: valuation cap, upfront and earn-out tied to retained ARR.'),
('7. Sensitivities','Year-1 EPS and FCF sensitivity grids across churn, growth, cash yield and capital-drag treatment; downside triggers.')]
for i,(a,b) in enumerate(idx,1):
    ws.cell(row=r+i,column=2,value=a).font=F(); ws.cell(row=r+i,column=3,value=b).font=F(); ws.cell(row=r+i,column=3).alignment=Alignment(wrap_text=True,vertical='top')
    for c in (2,3): ws.cell(row=r+i,column=c).border=BOX
r=r+len(idx)+2
ws.cell(row=r,column=2,value='Legend').font=HDR
leg=[('Blue font','Hard-coded input (case fact or team assumption)',INPUT),('Black font','Formula',F()),('Green font','Link to another sheet',LINK),('Light blue fill','Section header',F()),('Light yellow fill','Key output',F())]
for i,(a,b,f) in enumerate(leg,1):
    c=ws.cell(row=r+i,column=2,value=a); c.font=f; ws.cell(row=r+i,column=3,value=b).font=F()
    if a=='Light blue fill': c.fill=LBLUE
    if a=='Light yellow fill': c.fill=LYEL
r=r+len(leg)+2
ws.cell(row=r,column=2,value='Conventions').font=HDR
for i,t in enumerate(['All amounts in ₹ Cr unless stated; shares in Cr; EPS in ₹ per share.','CASE FACT ≠ DERIVED CALCULATION ≠ TEAM ASSUMPTION — every input is labelled by category on the Inputs sheet.','The ₹115 Cr/year UPI MDR benefit is Paytm standalone net revenue, not a Liminal transaction synergy; it is modelled as a separate offset.','Negative numbers in parentheses; zero shown as "-".'],1):
    ws.cell(row=r+i,column=3,value=t).font=F(); ws.cell(row=r+i,column=2,value=f'{i}.').font=F()

# ================= INPUTS =================
ws=sheet('Inputs',[3,44,16,14,50])
title(ws,'1. Inputs','Blue cells are inputs. Category: CF = case fact · TA = team assumption. Source noted per line.')
I={}  # name -> cell ref on Inputs
def inp(row,label,val,fmt,cat,src,name):
    put(ws,f'B{row}',label); c=put(ws,f'C{row}',val,fmt,INPUT); put(ws,f'D{row}',cat,align='center'); put(ws,f'E{row}',src,font=F(size=9,color='595959'))
    I[name]=f"Inputs!$C${row}"
hdr(ws,5,[2,3,4,5],['Item','Value','Category','Source / note'])
section(ws,6,'PAYTM — baseline financials',4)
rows=[('Market capitalisation (₹ Cr)',118750,NUM,'CF','Case §1: ₹1,18,750 Cr (~$14B), mid-September 2026','mcap'),
('Diluted shares outstanding (Cr)',64,NUM,'CF','Case §1 baseline financials','shares'),
('Cash (₹ Cr)',8900,NUM,'CF','Case §1','cash'),
('Gross debt (₹ Cr)',350,NUM,'CF','Case §1','debt'),
('Trailing revenue (₹ Cr)',8450,NUM,'CF','Case §1','rev'),
('EBITDA (₹ Cr)',640,NUM,'CF','Case §1','ebitda'),
('PAT (₹ Cr)',480,NUM,'CF','Case §1','pat'),
('Diluted EPS (₹) — starting point for all dilution',7.50,NUM2,'CF','Case §1: use as starting point for Section 5.3','eps'),
('Credit rating','CRISIL AA− (Stable)',None,'CF','Case §1','rating')]
r=7
for lab,v,fm,cat,src,nm in rows: inp(r,lab,v,fm,cat,src,nm); r+=1
r+=1; section(ws,r,'LIMINAL / DEAL — case terms',4); r+=1
rows=[('Headline acquisition value (₹ Cr)',4000,NUM,'CF','Case §2: ₹4,000 Cr (~$470M)','deal'),
('Headline cash consideration (₹ Cr)',2100,NUM,'CF','Case §2','dealcash'),
('Headline equity consideration (₹ Cr)',1900,NUM,'CF','Case §2','dealeq'),
('Liminal ARR (₹ Cr)',220,NUM,'CF','Case §2: ₹220 Cr (~$26M)','arr'),
('Liminal current PAT (₹ Cr)',0,NUM,'CF','Case §2: approximately breakeven at net income level','lpat'),
('Four largest clients — share of ARR',0.60,PCT,'CF','Case §2: HDFC Bank, Axis Bank, CoinDCX, ZebPay','top4'),
('Full-acquisition ARR churn — low',0.30,PCT,'CF','Case §3.1: 30% to 45% lost within 12 months','churnlo'),
('Full-acquisition ARR churn — high',0.45,PCT,'CF','Case §3.1','churnhi'),
('Full-control capital drag — recurring annual FCF (₹ Cr)',750,NUM,'CF','Case §3.2: bank-like capital reserves','drag'),
('UPI MDR — incremental net revenue to Paytm (₹ Cr/yr)',115,NUM,'CF','Case §3.4: real, effective 15 Oct 2026; Paytm standalone','mdr')]
for lab,v,fm,cat,src,nm in rows: inp(r,lab,v,fm,cat,src,nm); r+=1
r+=1; section(ws,r,'TEAM ASSUMPTIONS — transaction structure',4); r+=1
rows=[('Initial minority ownership',0.25,PCT,'TA','Midpoint of the permitted 20–30% range','stake'),
('Minority priced pro-rata to headline value? (1 = yes)',1,NUM,'TA','Illustrative: ₹1,000 Cr = 25% × ₹4,000 Cr','prorata'),
('Phase-1 funding — share from existing cash',1.00,PCT,'TA','No new debt, no new equity issuance in Phase 1','p1cash'),
('Phase-1 transaction fees (₹ Cr)',15,NUM,'TA','One-time','p1fees'),
('Validation period before option window (months)',12,NUM,'TA','Phase 2 · 3–12 months','valid'),
('Call-option window (months, after validation)',12,NUM,'TA','Phase 3 · ~12 months+','window'),
('Control-tranche upfront share of cap',0.55,PCT,'TA','Balance is retention-linked earn-out','upfront'),
('Earn-out floor — retained ARR at which earn-out is zero',0.55,PCT,'TA','Mirrors case high-churn bound (45% churn)','eofloor'),
('Earn-out paid in Paytm shares? (1 = shares, 0 = cash)',1,NUM,'TA','Contingent equity, collared','eoshares'),
('Integration cost at control (₹ Cr, one-time)',100,NUM,'TA','Cash and P&L, year of exercise','integ'),
('Control-exercise cash portion (₹ Cr)',1200,NUM,'TA','Balance of upfront funded by new debt','ctrlcash')]
for lab,v,fm,cat,src,nm in rows: inp(r,lab,v,fm,cat,src,nm); r+=1
r+=1; section(ws,r,'TEAM ASSUMPTIONS — financing, tax, returns',4); r+=1
rows=[('Pre-tax yield on Paytm surplus cash',0.06,PCT,'TA','Foregone treasury income on cash used','yield'),
('Pre-tax cost of new debt (CRISIL AA− issuer)',0.085,PCT,'TA','Financing cost on debt-funded consideration','kd'),
('Corporate tax rate',0.25,PCT,'TA','Applied to interest, foregone income and Liminal profits','tax'),
('WACC / required return',0.12,PCT,'TA','Discount rate for NPV of drag and DCF','wacc'),
('Terminal growth',0.05,PCT,'TA','For DCF cross-check','tg'),
('Minimum cash guardrail (₹ Cr)',5000,NUM,'TA','Liquidity floor','mincash'),
('Maximum gross debt / EBITDA guardrail',1.5,MULT,'TA','Rating headroom','maxlev')]
for lab,v,fm,cat,src,nm in rows: inp(r,lab,v,fm,cat,src,nm); r+=1
r+=1; section(ws,r,'TEAM ASSUMPTIONS — Liminal operating model',4); r+=1
rows=[('Liminal ARR growth — base case',0.20,PCT,'TA','Bear 10% / Bull 30% tested on Sensitivities','g'),
('EBITDA margin step-up per year (pp)',0.05,PCT,'TA','From 0% today','mstep'),
('EBITDA margin cap',0.25,PCT,'TA','Asset-light custody / MPC infrastructure','mcapm'),
('PAT as % of EBITDA',0.75,PCT,'TA','Tax at 25%; D&A ≈ capex','patconv'),
('FCF as % of PAT',1.00,PCT,'TA','Asset-light; working capital neutral','fcfconv'),
('Churn applied in full-acquisition counterfactual',0.375,PCT,'TA','Midpoint of case 30–45% range','churnbase'),
('Cost stickiness in churn year (share of lost revenue)',0.50,PCT,'TA','Half of the lost revenue’s cost base persists one year','sticky'),
('Churn under minority / JV structure',0.00,'0.0%','TA','No change of control — validated through client consents','churnmin'),
('Capital drag applied at minority level (₹ Cr/yr)',0,'#,##0','TA','Case does not specify; RBI treatment is a validation gate','dragmin'),
('Capital drag applied at control (₹ Cr/yr)',750,NUM,'TA','Default = case ₹750 Cr; flex to test gate','dragctrl'),
('Churn applied at control exercise',0.20,PCT,'TA','Maximum acceptable under client-consent gate','churnctrl'),
('UPI MDR — EBITDA flow-through',0.80,PCT,'TA','Net revenue with minimal incremental cost','mdrflow'),
('Synergies in base case (₹ Cr/yr)',0,'#,##0','TA','Conservative: zero in base; upside only','syn')]
for lab,v,fm,cat,src,nm in rows: inp(r,lab,v,fm,cat,src,nm); r+=1
r+=1; section(ws,r,'DERIVED CALCULATIONS (formulas)',4); r+=1
def calc(row,label,formula,fmt,note,name):
    put(ws,f'B{row}',label); put(ws,f'C{row}',formula,fmt); put(ws,f'D{row}','CALC',align='center'); put(ws,f'E{row}',note,font=F(size=9,color='595959')); I[name]=f"Inputs!$C${row}"
calc(r,'Implied Paytm share price (₹)',f"={I['mcap']}/{I['shares']}",NUM,'Market cap ÷ diluted shares ≈ ₹1,855','price'); r+=1
calc(r,'Headline multiple (deal value / ARR)',f"={I['deal']}/{I['arr']}",MULT,'≈ 18.2× (case rounds to 18×)','mult'); r+=1
calc(r,'Trailing P/E',f"={I['mcap']}/{I['pat']}",MULT,'≈ 247×','pe'); r+=1
calc(r,'Phase-1 investment (₹ Cr)',f"=IF({I['prorata']}=1,{I['stake']}*{I['deal']},0)",NUM,'25% × ₹4,000 Cr = ₹1,000 Cr','p1inv'); r+=1
calc(r,'Remaining stake after Phase 1',f"=1-{I['stake']}",PCT,'75%','rem'); r+=1
calc(r,'Control-tranche valuation cap (₹ Cr)',f"={I['rem']}*{I['deal']}",NUM,'Never more than headline in total','ctrlcap'); r+=1
calc(r,'Control-tranche upfront (₹ Cr)',f"={I['ctrlcap']}*{I['upfront']}",NUM,'Paid at exercise','ctrlup'); r+=1
calc(r,'Control-tranche earn-out maximum (₹ Cr)',f"={I['ctrlcap']}-{I['ctrlup']}",NUM,'Paid at month 18 post-control on retained ARR','ctrleo'); r+=1
calc(r,'Control-exercise new debt (₹ Cr)',f"=MAX({I['ctrlup']}-{I['ctrlcash']},0)",NUM,'Upfront less cash portion','ctrldebt'); r+=1
calc(r,'UPI MDR — PAT / FCF contribution (₹ Cr/yr)',f"={I['mdr']}*{I['mdrflow']}*(1-{I['tax']})",NUM,'Paytm standalone offset ≈ ₹69 Cr','mdrpat'); r+=1
calc(r,'MDR as % of ₹750 Cr drag — gross',f"={I['mdr']}/{I['drag']}",PCT,'≈ 15%','mdrgross'); r+=1
calc(r,'MDR as % of ₹750 Cr drag — after conversion',f"={I['mdrpat']}/{I['drag']}",PCT,'≈ 9%','mdrnet'); r+=1
calc(r,'NPV of capital drag — 10-year annuity at WACC (₹ Cr)',f"={I['drag']}*(1-(1+{I['wacc']})^-10)/{I['wacc']}",NUM,'≈ ₹4,238 Cr vs ₹4,000 Cr price','dragnpv'); r+=1
calc(r,'Capital drag as % of Paytm EBITDA',f"={I['drag']}/{I['ebitda']}",PCT,'≈ 117%','dragebitda'); r+=1

# ================= VALUATION & CHURN =================
ws=sheet('Valuation & Churn',[3,30,16,16,18,18,20])
title(ws,'2. Valuation & Churn','18.2× headline ARR becomes 26–33× on retained ARR under full-control churn')
put(ws,'B5','Headline valuation'); put(ws,'C5',f"={I['deal']}",NUM,LINK); put(ws,'D5','÷ ARR'); put(ws,'E5',f"={I['arr']}",NUM,LINK); put(ws,'F5','→ multiple'); put(ws,'G5',f"={I['mult']}",MULT,fill=LYEL,bold=True)
hdr(ws,7,[2,3,4,5,6,7],['Full-control churn','ARR lost (₹ Cr)','Retained ARR (₹ Cr)','₹4,000 Cr / retained ARR','Implied value at headline multiple (₹ Cr)','Value gap vs ₹4,000 Cr'])
churns=[0,f"={I['churnlo']}",f"={I['churnbase']}",f"={I['churnhi']}"]
for i,cv in enumerate(churns):
    r=8+i; put(ws,f'B{r}',cv,'0.0%',INPUT if i==0 else LINK); put(ws,f'C{r}',f"={I['arr']}*B{r}",NUM1); put(ws,f'D{r}',f"={I['arr']}-C{r}",NUM1); put(ws,f'E{r}',f"={I['deal']}/D{r}",MULT,bold=True); put(ws,f'F{r}',f"={I['mult']}*D{r}",NUM); put(ws,f'G{r}',f"={I['deal']}-F{r}",NUM)
put(ws,'B13','Value destroyed per 10 pts of churn at headline multiple (₹ Cr)'); put(ws,'E13',f"={I['mult']}*{I['arr']}*0.1",NUM,fill=LYEL,bold=True)
hdr(ws,15,[2,3,4,5],['Revenue recovery hurdle','Retained ARR (₹ Cr)','Original ARR (₹ Cr)','Growth required to recover'])
put(ws,'B16','After 30% churn'); put(ws,'C16','=D9',NUM1); put(ws,'D16',f"={I['arr']}",NUM,LINK); put(ws,'E16','=D16/C16-1',PCT,bold=True)
put(ws,'B17','After 45% churn'); put(ws,'C17','=D11',NUM1); put(ws,'D17',f"={I['arr']}",NUM,LINK); put(ws,'E17','=D17/C17-1',PCT,bold=True)
put(ws,'B19','Top-4 client concentration'); put(ws,'C19',f"={I['top4']}",PCT,LINK); put(ws,'D19','ARR (₹ Cr)'); put(ws,'E19',f"={I['arr']}*C19",NUM)
put(ws,'B20','Case churn as % of top-4 ARR — low'); put(ws,'E20',f"={I['churnlo']}*{I['arr']}/E19",PCT)
put(ws,'B21','Case churn as % of top-4 ARR — high'); put(ws,'E21',f"={I['churnhi']}*{I['arr']}/E19",PCT)
section(ws,23,'DCF cross-check — what growth does ₹4,000 Cr require? (team assumptions, standalone, no churn, no drag)',6)
hdr(ws,24,[2,3,4,5,6,7],['Year','ARR (₹ Cr)','EBITDA margin','FCF (₹ Cr)','Discount factor','PV (₹ Cr)'])
for y in range(1,11):
    r=24+y; put(ws,f'B{r}',y,NUM); put(ws,f'C{r}',f"={I['arr']}*(1+{I['g']})^B{r}",NUM1); put(ws,f'D{r}',f"=MIN({I['mstep']}*B{r},{I['mcapm']})",PCT); put(ws,f'E{r}',f"=C{r}*D{r}*{I['patconv']}*{I['fcfconv']}",NUM1); put(ws,f'F{r}',f"=1/(1+{I['wacc']})^B{r}",NUM2); put(ws,f'G{r}',f"=E{r}*F{r}",NUM1)
put(ws,'B35','Terminal value at year 10'); put(ws,'E35',f"=E34*(1+{I['tg']})/({I['wacc']}-{I['tg']})",NUM); put(ws,'F35','=F34',NUM2); put(ws,'G35','=E35*F35',NUM)
put(ws,'B36','Standalone DCF value (₹ Cr)'); put(ws,'G36','=SUM(G25:G35)',NUM,fill=LYEL,bold=True)
put(ws,'B37','Implied DCF multiple of ARR'); put(ws,'G37',f"=G36/{I['arr']}",MULT)
put(ws,'B38','Headline price supported by base-case DCF?'); put(ws,'G38',f'=IF(G36>={I["deal"]},"Supported","Not supported")',bold=True)
put(ws,'B39','Note: DCF value scales with the growth input on Inputs (base 20%). The Sensitivities sheet shows the value at 10% / 30% / 40%.',font=F(size=9,italic=True,color='595959'),border=False)

# ================= FINANCING & EPS =================
ws=sheet('Financing & EPS',[3,44,16,16,16,16,16])
title(ws,'3. Financing & EPS','Year-1 accretion / dilution from the ₹7.50 baseline under alternative financing mixes; recommended Phase-1 structure')
section(ws,5,'A. Mechanical dilution — headline mix, share count only (as in the deck)',5)
put(ws,'B6','Implied Paytm share price (₹)'); put(ws,'C6',f"={I['price']}",NUM,LINK)
put(ws,'B7','₹1,900 Cr equity consideration → new shares (Cr)'); put(ws,'C7',f"={I['dealeq']}/C6",NUM2)
put(ws,'B8','Pro-forma diluted shares (Cr)'); put(ws,'C8',f"={I['shares']}+C7",NUM2)
put(ws,'B9','EPS if PAT remains ₹480 Cr (₹)'); put(ws,'C9',f"={I['pat']}/C8",NUM2,fill=LYEL,bold=True)
put(ws,'B10','Mechanical dilution vs ₹7.50 baseline'); put(ws,'C10',f"=C9/{I['eps']}-1",PCT,bold=True)
put(ws,'B11','Cash after ₹2,100 Cr funded from balance sheet (₹ Cr)'); put(ws,'C11',f"={I['cash']}-{I['dealcash']}",NUM)
section(ws,13,'B. Full-acquisition year-1 EPS — including financing costs and post-churn Liminal result',5)
hdr(ws,14,[2,3,4,5,6,7],['Line item (₹ Cr unless stated)','Case headline: ₹2,100 cash + ₹1,900 equity','Debt-funded: ₹2,100 debt + ₹1,900 equity','Mix: ₹1,400 cash + ₹700 debt + ₹1,900 equity','All cash ₹4,000','All equity ₹4,000'])
cols='CDEFG'; mixes=[(2100,0,1900),(0,2100,1900),(1400,700,1900),(4000,0,0),(0,0,4000)]
labels=['Cash from balance sheet','New debt','Equity issued','New shares issued (Cr)','Pro-forma diluted shares (Cr)','Foregone post-tax interest on cash used','Post-tax interest on new debt','Liminal year-1 PAT after churn (from Projection)','Synergies (base)','Incremental PAT','Pro-forma PAT','Year-1 EPS (₹)','Accretion / (dilution) vs ₹7.50','+ UPI MDR standalone offset → EPS (₹)','Cash after transaction','Gross debt after transaction','Gross debt / EBITDA','Within guardrails? (cash ≥ floor and leverage ≤ max)']
for i,l in enumerate(labels): put(ws,f'B{15+i}',l, bold=(l in ('Year-1 EPS (₹)','Accretion / (dilution) vs ₹7.50')))
for c,(cash,debt,eq) in zip(cols,mixes):
    put(ws,f'{c}15',cash,NUM,INPUT); put(ws,f'{c}16',debt,NUM,INPUT); put(ws,f'{c}17',eq,NUM,INPUT)
    put(ws,f'{c}18',f"={c}17/{I['price']}",NUM2); put(ws,f'{c}19',f"={I['shares']}+{c}18",NUM2)
    put(ws,f'{c}20',f"=-{c}15*{I['yield']}*(1-{I['tax']})",NUM1); put(ws,f'{c}21',f"=-{c}16*{I['kd']}*(1-{I['tax']})",NUM1)
    put(ws,f'{c}22',"='Liminal Projection'!$D$25",NUM1,LINK); put(ws,f'{c}23',f"={I['syn']}",NUM,LINK)
    put(ws,f'{c}24',f"=SUM({c}20:{c}23)",NUM1); put(ws,f'{c}25',f"={I['pat']}+{c}24",NUM1)
    put(ws,f'{c}26',f"={c}25/{c}19",NUM2,fill=LYEL,bold=True); put(ws,f'{c}27',f"={c}26/{I['eps']}-1",PCT,bold=True)
    put(ws,f'{c}28',f"=({c}25+{I['mdrpat']})/{c}19",NUM2)
    put(ws,f'{c}29',f"={I['cash']}-{c}15",NUM); put(ws,f'{c}30',f"={I['debt']}+{c}16",NUM); put(ws,f'{c}31',f"={c}30/{I['ebitda']}",MULT)
    put(ws,f'{c}32',f'=IF(AND({c}29>={I["mincash"]},{c}31<={I["maxlev"]}),"Yes","No")',align='center')
put(ws,'B34','Note: Liminal year-1 PAT after churn is negative because 50% of the lost revenue’s cost base is assumed to persist for one year (Inputs). No group tax relief is assumed on Liminal losses.',font=F(size=9,italic=True,color='595959'),border=False)
section(ws,36,'C. Recommended Phase-1 structure — 25% minority for ₹1,000 Cr, funded from existing cash',5)
put(ws,'B37','Phase-1 investment (₹ Cr)'); put(ws,'C37',f"={I['p1inv']}",NUM,LINK)
put(ws,'B38','Funded from existing cash (₹ Cr)'); put(ws,'C38',f"=C37*{I['p1cash']}",NUM)
put(ws,'B39','New debt (₹ Cr)'); put(ws,'C39','=C37-C38',NUM)
put(ws,'B40','New shares issued (Cr)'); put(ws,'C40',0,NUM,INPUT)
put(ws,'B41','Cash remaining (₹ Cr)'); put(ws,'C41',f"={I['cash']}-C38-{I['p1fees']}",NUM,fill=LYEL,bold=True)
put(ws,'B42','Gross debt / EBITDA after Phase 1'); put(ws,'C42',f"=({I['debt']}+C39)/{I['ebitda']}",MULT)
put(ws,'B43','Immediate share-count dilution'); put(ws,'C43',f"=C40/{I['shares']}",PCT)
put(ws,'B44','Foregone post-tax interest on cash used (₹ Cr/yr)'); put(ws,'C44',f"=-C38*{I['yield']}*(1-{I['tax']})",NUM1)
put(ws,'B45','Paytm share of Liminal year-1 PAT (equity method, ₹ Cr)'); put(ws,'C45',f"={I['stake']}*'Liminal Projection'!$D$8",NUM1,LINK)
put(ws,'B46','Year-1 EPS — Phase 1 (₹)'); put(ws,'C46',f"=({I['pat']}+C44+C45)/({I['shares']}+C40)",NUM2,fill=LYEL,bold=True)
put(ws,'B47','Accretion / (dilution) vs ₹7.50 — economic (incl. foregone interest)'); put(ws,'C47',f"=C46/{I['eps']}-1",PCT,bold=True)
put(ws,'B48','Accretion / (dilution) vs ₹7.50 — share count only'); put(ws,'C48',f"=({I['pat']}/({I['shares']}+C40))/{I['eps']}-1",PCT)
put(ws,'B49','Year-1 EPS with UPI MDR standalone offset (₹)'); put(ws,'C49',f"=({I['pat']}+C44+C45+{I['mdrpat']})/({I['shares']}+C40)",NUM2)
put(ws,'B50','Standalone Paytm EPS with MDR, no transaction (₹)'); put(ws,'C50',f"=({I['pat']}+{I['mdrpat']})/{I['shares']}",NUM2)

# ================= LIMINAL PROJECTION =================
ws=sheet('Liminal Projection',[3,40]+[12]*11)
title(ws,'4. Liminal Projection','Standalone path (no churn) and churned path for the full-acquisition counterfactual — team assumptions')
years=list(range(0,11)); ycols=[get_column_letter(3+i) for i in range(11)]
section(ws,5,'A. Standalone path — no change of control (basis for Phase-1 minority)',12)
hdr(ws,6,[2]+[3+i for i in range(11)],['Year']+[f'Y{y}' for y in years])
put(ws,'B7','ARR / revenue (₹ Cr)'); put(ws,'B8','PAT (₹ Cr)'); put(ws,'B9','EBITDA margin'); put(ws,'B10','EBITDA (₹ Cr)'); put(ws,'B11','FCF (₹ Cr)'); put(ws,'B12','Paytm 25% share of PAT (₹ Cr)')
for i,c in enumerate(ycols):
    y=years[i]
    put(ws,f'{c}7',f"={I['arr']}*(1+{I['g']})^{y}",NUM1)
    put(ws,f'{c}9',f"=MIN({I['mstep']}*{y},{I['mcapm']})",PCT)
    put(ws,f'{c}10',f"={c}7*{c}9",NUM1)
    put(ws,f'{c}8',f"=IF({c}10>0,{c}10*{I['patconv']},{c}10)",NUM1)
    put(ws,f'{c}11',f"={c}8*{I['fcfconv']}",NUM1)
    put(ws,f'{c}12',f"={I['stake']}*{c}8",NUM1)
section(ws,14,'B. Churned path — full acquisition today; churn in Y1, then growth on the retained base',12)
put(ws,'B15','Churn applied'); put(ws,'C15',f"={I['churnbase']}",PCT,LINK); put(ws,'D15','Sticky cost share'); put(ws,'E15',f"={I['sticky']}",PCT,LINK)
hdr(ws,16,[2]+[3+i for i in range(11)],['Year']+[f'Y{y}' for y in years])
put(ws,'B17','Revenue before churn (₹ Cr)'); put(ws,'B18','Revenue after churn (₹ Cr)'); put(ws,'B19','Lost revenue (₹ Cr)'); put(ws,'B20','EBITDA margin'); put(ws,'B21','EBITDA before sticky cost (₹ Cr)'); put(ws,'B22','Sticky cost penalty (₹ Cr)'); put(ws,'B23','EBITDA (₹ Cr)'); put(ws,'B24','PAT (₹ Cr) — no group tax relief on losses'); put(ws,'B25','PAT — year 1 (₹ Cr)'); put(ws,'B26','FCF (₹ Cr)')
for i,c in enumerate(ycols):
    y=years[i]
    put(ws,f'{c}17',f"={c}7",NUM1); put(ws,f'{c}18',f"={c}17*(1-IF({y}>=1,$C$15,0))",NUM1); put(ws,f'{c}19',f"={c}17-{c}18",NUM1); put(ws,f'{c}20',f"={c}9",PCT)
    put(ws,f'{c}21',f"={c}18*{c}20",NUM1); put(ws,f'{c}22',f"=IF({y}=1,$E$15*{c}19,0)",NUM1); put(ws,f'{c}23',f"={c}21-{c}22",NUM1)
    put(ws,f'{c}24',f"=IF({c}23>0,{c}23*{I['patconv']},{c}23)",NUM1); put(ws,f'{c}26',f"={c}24*{I['fcfconv']}",NUM1)
put(ws,'D25','=D24',NUM1,fill=LYEL)
section(ws,28,'C. Control-exercise path — 25% held Y1; control at end-Y1; churn per consent gate in Y2, then growth',12)
put(ws,'B29','Churn at control'); put(ws,'C29',f"={I['churnctrl']}",PCT,LINK)
hdr(ws,30,[2]+[3+i for i in range(11)],['Year']+[f'Y{y}' for y in years])
put(ws,'B31','Revenue after churn (₹ Cr)'); put(ws,'B32','EBITDA (₹ Cr)'); put(ws,'B33','PAT (₹ Cr)'); put(ws,'B34','FCF (₹ Cr)')
for i,c in enumerate(ycols):
    y=years[i]
    put(ws,f'{c}31',f"={c}7*(1-IF({y}>=2,$C$29,0))",NUM1)
    put(ws,f'{c}32',f"={c}31*{c}9-IF({y}=2,$E$15*({c}7-{c}31),0)",NUM1)
    put(ws,f'{c}33',f"=IF({c}32>0,{c}32*{I['patconv']},{c}32)",NUM1); put(ws,f'{c}34',f"={c}33*{I['fcfconv']}",NUM1)

# ================= BREAKEVEN =================
ws=sheet('PAT & FCF Breakeven',[3,46]+[12]*10)
title(ws,'5. PAT & FCF Breakeven','Two separate hurdles: accounting accretion (PAT / EPS) and cash-flow viability (FCF after the ₹750 Cr capital drag)')
yc=[get_column_letter(3+i) for i in range(10)]; pc=[get_column_letter(4+i) for i in range(10)]  # projection cols D..M for Y1..Y10
def block(r0,name,notes):
    section(ws,r0,name,11); hdr(ws,r0+1,[2]+[3+i for i in range(10)],['Year (₹ Cr)']+[f'Y{y}' for y in range(1,11)])
    return r0+2
# A. Full acquisition
r=block(5,'A. Full acquisition today — case headline mix (₹2,100 Cr cash from balance sheet + ₹1,900 Cr equity)','')
rowsA=['Liminal PAT (churned path)','Foregone post-tax interest on ₹2,100 Cr cash','Post-tax interest on new debt','Synergies (base)','Integration / one-time costs — excluded from run-rate EPS (in FCF below)','Incremental PAT','Pro-forma PAT','Pro-forma diluted shares (Cr)','Pro-forma EPS (₹)','Accretion / (dilution) vs ₹7.50','Pro-forma EPS incl. UPI MDR standalone offset (₹)','','Liminal FCF (churned path)','Foregone post-tax interest (cash)','Post-tax interest on new debt (cash)','UPI MDR standalone offset (shown separately, not deal-driven)','Capital drag — ₹750 Cr recurring annual FCF','Integration / one-time cash costs (Y1)','Incremental FCF (excluding MDR)','Incremental FCF (crediting MDR)','Cumulative incremental FCF incl. upfront cash','PAT breakeven reached?','FCF breakeven reached?']
for i,l in enumerate(rowsA): put(ws,f'B{r+i}',l,bold=l.startswith(('Incremental','Pro-forma EPS','Accretion')))
for k,(c,p) in enumerate(zip(yc,pc)):
    y=k+1
    put(ws,f'{c}{r}',f"='Liminal Projection'!{p}24",NUM1,LINK)
    put(ws,f'{c}{r+1}',f"=-{I['dealcash']}*{I['yield']}*(1-{I['tax']})",NUM1)
    put(ws,f'{c}{r+2}',f"=-0*{I['kd']}*(1-{I['tax']})",NUM1)
    put(ws,f'{c}{r+3}',f"={I['syn']}",NUM1,LINK)
    put(ws,f'{c}{r+4}',0,NUM1,INPUT)
    put(ws,f'{c}{r+5}',f"=SUM({c}{r}:{c}{r+4})",NUM1)
    put(ws,f'{c}{r+6}',f"={I['pat']}+{c}{r+5}",NUM1)
    put(ws,f'{c}{r+7}',f"='Financing & EPS'!$C$19",NUM2,LINK)
    put(ws,f'{c}{r+8}',f"={c}{r+6}/{c}{r+7}",NUM2,fill=LYEL,bold=True)
    put(ws,f'{c}{r+9}',f"={c}{r+8}/{I['eps']}-1",PCT)
    put(ws,f'{c}{r+10}',f"=({c}{r+6}+{I['mdrpat']})/{c}{r+7}",NUM2)
    put(ws,f'{c}{r+12}',f"='Liminal Projection'!{p}26",NUM1,LINK)
    put(ws,f'{c}{r+13}',f"={c}{r+1}",NUM1); put(ws,f'{c}{r+14}',f"={c}{r+2}",NUM1)
    put(ws,f'{c}{r+15}',f"={I['mdrpat']}",NUM1,LINK)
    put(ws,f'{c}{r+16}',f"=-{I['dragctrl']}",NUM1,LINK)
    put(ws,f'{c}{r+17}',f"=IF({y}=1,-{I['integ']},0)",NUM1)
    put(ws,f'{c}{r+18}',f"={c}{r+12}+{c}{r+13}+{c}{r+14}+{c}{r+16}+{c}{r+17}",NUM1,fill=LYEL,bold=True)
    put(ws,f'{c}{r+19}',f"={c}{r+18}+{c}{r+15}",NUM1)
    prev = f"-{I['dealcash']}" if y==1 else f"{yc[k-1]}{r+20}"
    put(ws,f'{c}{r+20}',f"={prev}+{c}{r+18}",NUM)
    put(ws,f'{c}{r+21}',f'=IF({c}{r+5}>=0,"Yes","No")',align='center'); put(ws,f'{c}{r+22}',f'=IF({c}{r+18}>=0,"Yes","No")',align='center')
rA=r
put(ws,f'B{r+24}','First year of PAT breakeven'); put(ws,f'C{r+24}',f'=IFERROR(MATCH("Yes",C{r+21}:L{r+21},0),"Not within 10 years")',fill=LYEL,bold=True)
put(ws,f'B{r+25}','First year of FCF breakeven (excluding MDR)'); put(ws,f'C{r+25}',f'=IFERROR(MATCH("Yes",C{r+22}:L{r+22},0),"Not within 10 years")',fill=LYEL,bold=True)
put(ws,f'B{r+26}','Liminal FCF needed to cover the drag from its own cash flow (₹ Cr)'); put(ws,f'C{r+26}',f"={I['dragctrl']}",NUM,LINK); put(ws,f'D{r+26}','→ ARR required at cap margin (₹ Cr)'); put(ws,f'G{r+26}',f"={I['dragctrl']}/({I['mcapm']}*{I['patconv']}*{I['fcfconv']})",NUM,bold=True)
# B. Phase 1
r=block(r+28,'B. Phase-1 minority — 25% for ₹1,000 Cr from existing cash; no consolidation (equity method)','')
rowsB=['Paytm 25% share of Liminal PAT (standalone path)','Foregone post-tax interest on cash used','Phase-1 fees — excluded from run-rate EPS (in FCF below)','Incremental PAT','Pro-forma EPS (₹)','Accretion / (dilution) vs ₹7.50','','Foregone post-tax interest (cash)','Capital drag applied at minority level (gate)','Phase-1 fees (Y1)','Dividends received (none assumed)','Incremental FCF','Cumulative incremental FCF incl. ₹1,000 Cr investment','Associate income covers foregone interest?']
for i,l in enumerate(rowsB): put(ws,f'B{r+i}',l,bold=l.startswith(('Incremental','Pro-forma EPS','Accretion')))
for k,(c,p) in enumerate(zip(yc,pc)):
    y=k+1
    put(ws,f'{c}{r}',f"='Liminal Projection'!{p}12",NUM1,LINK)
    put(ws,f'{c}{r+1}',f"=-{I['p1inv']}*{I['p1cash']}*{I['yield']}*(1-{I['tax']})",NUM1)
    put(ws,f'{c}{r+2}',0,NUM1,INPUT)
    put(ws,f'{c}{r+3}',f"=SUM({c}{r}:{c}{r+2})",NUM1)
    put(ws,f'{c}{r+4}',f"=({I['pat']}+{c}{r+3})/{I['shares']}",NUM2,fill=LYEL,bold=True)
    put(ws,f'{c}{r+5}',f"={c}{r+4}/{I['eps']}-1",PCT)
    put(ws,f'{c}{r+7}',f"={c}{r+1}",NUM1); put(ws,f'{c}{r+8}',f"=-{I['dragmin']}",NUM1,LINK); put(ws,f'{c}{r+9}',f"=IF({y}=1,-{I['p1fees']},0)",NUM1); put(ws,f'{c}{r+10}',0,NUM1,INPUT)
    put(ws,f'{c}{r+11}',f"=SUM({c}{r+7}:{c}{r+10})",NUM1,fill=LYEL,bold=True)
    prev = f"-{I['p1inv']}" if y==1 else f"{yc[k-1]}{r+12}"
    put(ws,f'{c}{r+12}',f"={prev}+{c}{r+11}",NUM)
    put(ws,f'{c}{r+13}',f'=IF({c}{r}>=-{c}{r+1},"Yes","No")',align='center')
put(ws,f'B{r+15}','First year associate income covers foregone interest'); put(ws,f'C{r+15}',f'=IFERROR(MATCH("Yes",C{r+13}:L{r+13},0),"Not within 10 years")',fill=LYEL,bold=True)
put(ws,f'B{r+16}','Note: on a cash basis the minority stake yields nothing until dividends or exit; its return is the equity value of the stake plus the option (see Call Option & Earn-out).',font=F(size=9,italic=True,color='595959'),border=False)
# C. Control exercise
r=block(r+18,'C. Control exercised at end of Y1 (gates cleared) — consolidated from Y2; churn per consent gate; capital drag per Inputs','')
rowsC=['Liminal PAT (control path) / 25% share in Y1','Foregone post-tax interest — Phase-1 cash','Foregone post-tax interest — control cash portion (from Y2)','Post-tax interest on control new debt (from Y2)','Integration cost — excluded from run-rate EPS (in FCF below)','Incremental PAT','Pro-forma diluted shares (Cr) — earn-out shares from Y3','Pro-forma EPS (₹)','Accretion / (dilution) vs ₹7.50','','Liminal FCF (control path) — consolidated from Y2','Cost of funds (cash items above)','Capital drag at control (from Y2)','Integration cash (Y2)','Incremental FCF','PAT breakeven reached?','FCF breakeven reached?']
for i,l in enumerate(rowsC): put(ws,f'B{r+i}',l,bold=l.startswith(('Incremental','Pro-forma EPS','Accretion')))
for k,(c,p) in enumerate(zip(yc,pc)):
    y=k+1
    put(ws,f'{c}{r}',f"=IF({y}=1,{I['stake']}*'Liminal Projection'!{p}33,'Liminal Projection'!{p}33)",NUM1,LINK)
    put(ws,f'{c}{r+1}',f"=-{I['p1inv']}*{I['p1cash']}*{I['yield']}*(1-{I['tax']})",NUM1)
    put(ws,f'{c}{r+2}',f"=IF({y}>=2,-{I['ctrlcash']}*{I['yield']}*(1-{I['tax']}),0)",NUM1)
    put(ws,f'{c}{r+3}',f"=IF({y}>=2,-{I['ctrldebt']}*{I['kd']}*(1-{I['tax']}),0)",NUM1)
    put(ws,f'{c}{r+4}',0,NUM1,INPUT)
    put(ws,f'{c}{r+5}',f"=SUM({c}{r}:{c}{r+4})",NUM1)
    put(ws,f'{c}{r+6}',f"={I['shares']}+IF({y}>=3,'Call Option & Earn-out'!$C$22,0)",NUM2,LINK)
    put(ws,f'{c}{r+7}',f"=({I['pat']}+{c}{r+5})/{c}{r+6}",NUM2,fill=LYEL,bold=True)
    put(ws,f'{c}{r+8}',f"={c}{r+7}/{I['eps']}-1",PCT)
    put(ws,f'{c}{r+10}',f"=IF({y}=1,0,'Liminal Projection'!{p}34)",NUM1,LINK)
    put(ws,f'{c}{r+11}',f"={c}{r+1}+{c}{r+2}+{c}{r+3}",NUM1)
    put(ws,f'{c}{r+12}',f"=IF({y}>=2,-{I['dragctrl']},0)",NUM1,LINK)
    put(ws,f'{c}{r+13}',f"=IF({y}=2,-{I['integ']},0)",NUM1)
    put(ws,f'{c}{r+14}',f"=SUM({c}{r+10}:{c}{r+13})",NUM1,fill=LYEL,bold=True)
    put(ws,f'{c}{r+15}',f'=IF(AND({y}>=2,{c}{r+5}>=0),"Yes","No")',align='center'); put(ws,f'{c}{r+16}',f'=IF(AND({y}>=2,{c}{r+14}>=0),"Yes","No")',align='center')
put(ws,f'B{r+18}','First year of PAT breakeven after control'); put(ws,f'C{r+18}',f'=IFERROR(MATCH("Yes",C{r+15}:L{r+15},0),"Not within 10 years")',fill=LYEL,bold=True)
put(ws,f'B{r+19}','First year of FCF breakeven after control'); put(ws,f'C{r+19}',f'=IFERROR(MATCH("Yes",C{r+16}:L{r+16},0),"Not within 10 years")',fill=LYEL,bold=True)
put(ws,f'B{r+20}','Control-exercise rule: do not exercise unless credible PAT/EPS breakeven AND credible FCF breakeven after regulatory capital requirements. Flex "Capital drag applied at control" on Inputs to test the regulatory gate (the case default ₹750 Cr defeats FCF breakeven).',font=F(size=9,italic=True,color='595959'),border=False)
section(ws,r+22,'D. UPI MDR offset vs capital drag (Paytm standalone; not created by acquiring Liminal)',11)
put(ws,f'B{r+23}','₹750 Cr capital drag (₹ Cr/yr)'); put(ws,f'C{r+23}',f"={I['drag']}",NUM,LINK)
put(ws,f'B{r+24}','UPI MDR incremental net revenue (₹ Cr/yr)'); put(ws,f'C{r+24}',f"={I['mdr']}",NUM,LINK); put(ws,f'D{r+24}','gross offset'); put(ws,f'F{r+24}',f"={I['mdrgross']}",PCT,bold=True)
put(ws,f'B{r+25}','UPI MDR after PAT/FCF conversion (₹ Cr/yr)'); put(ws,f'C{r+25}',f"={I['mdrpat']}",NUM,LINK); put(ws,f'D{r+25}','offset after conversion'); put(ws,f'F{r+25}',f"={I['mdrnet']}",PCT,bold=True)
put(ws,f'B{r+26}','Net annual cash cost of full ownership after MDR (₹ Cr/yr)'); put(ws,f'C{r+26}',f"={I['drag']}-{I['mdrpat']}",NUM,fill=LYEL,bold=True)
put(ws,f'B{r+27}','10-year NPV of the drag at WACC (₹ Cr) vs headline price'); put(ws,f'C{r+27}',f"={I['dragnpv']}",NUM,LINK); put(ws,f'D{r+27}',f"={I['deal']}",NUM,LINK)

# ================= CALL OPTION & EARN-OUT =================
ws=sheet('Call Option & Earn-out',[3,44,16,16,16,16,18])
title(ws,'6. Call Option & Earn-out','Future-control consideration capped at the lower of headline mechanics and retained-ARR value; upfront = strategic access, contingent = retained value')
put(ws,'B5','Remaining stake acquired on exercise'); put(ws,'C5',f"={I['rem']}",PCT,LINK)
put(ws,'B6','Control-tranche valuation cap (₹ Cr) = remaining stake × headline'); put(ws,'C6',f"={I['ctrlcap']}",NUM,LINK)
put(ws,'B7','Upfront at exercise (₹ Cr)'); put(ws,'C7',f"={I['ctrlup']}",NUM,LINK)
put(ws,'B8','Earn-out maximum (₹ Cr)'); put(ws,'C8',f"={I['ctrleo']}",NUM,LINK)
put(ws,'B9','Earn-out floor — retained ARR'); put(ws,'C9',f"={I['eofloor']}",PCT,LINK)
put(ws,'B10','Maximum total consideration incl. Phase 1 (₹ Cr)'); put(ws,'C10',f"={I['p1inv']}+C6",NUM,fill=LYEL,bold=True); put(ws,'D10','equals headline; never exceeded')
put(ws,'B11','Maximum unconditional consideration (₹ Cr)'); put(ws,'C11',f"={I['p1inv']}",NUM,LINK)
hdr(ws,13,[2,3,4,5,6,7],['Post-control churn','Retained ARR','Earn-out paid (₹ Cr)','Control total (₹ Cr)','Grand total incl. Phase 1 (₹ Cr)','Remaining stake × headline multiple × retained ARR (₹ Cr)'])
for i,cv in enumerate([0,0.10,0.20,0.30,0.375,0.45,0.55]):
    r=14+i; put(ws,f'B{r}',cv,'0.0%',INPUT); put(ws,f'C{r}',f"=1-B{r}",PCT); put(ws,f'D{r}',f"=$C$8*MIN(MAX((C{r}-$C$9)/(1-$C$9),0),1)",NUM); put(ws,f'E{r}',f"=$C$7+D{r}",NUM,bold=True); put(ws,f'F{r}',f"={I['p1inv']}+E{r}",NUM); put(ws,f'G{r}',f"={I['rem']}*{I['mult']}*{I['arr']}*C{r}",NUM)
put(ws,'B22','Earn-out shares if settled in Paytm stock at current price (Cr, maximum)'); put(ws,'C22',f"=IF({I['eoshares']}=1,C8/{I['price']},0)",NUM2,fill=LYEL); put(ws,'D22','% of share count'); put(ws,'E22',f"=C22/{I['shares']}",PCT)
put(ws,'B23','Earn-out per 10 points of retained ARR (₹ Cr)'); put(ws,'C23','=C8/(1-C9)*0.1',NUM)
put(ws,'B25','Pricing principle: consideration = lower of (1) agreed headline valuation mechanics and (2) retained-ARR / performance-based value, subject to client retention, regulatory capital treatment, financial performance, the valuation cap and customary adjustments. Column G shows the retained-ARR value; column E shows what the schedule pays.',font=F(size=9,italic=True,color='595959'),border=False)
section(ws,27,'Phase-1 stake — illustrative return if exited at end of Y5 at a multiple of Y5 ARR (no dividends)',6)
hdr(ws,28,[2,3,4,5,6],['Exit multiple of ARR →','6.0x','10.0x','14.0x','Headline'])
put(ws,'C28',6,MULT,INPUT); put(ws,'D28',10,MULT,INPUT); put(ws,'E28',14,MULT,INPUT); put(ws,'F28',f"={I['mult']}",MULT,LINK)
for i,g in enumerate([0.10,0.20,0.30]):
    r=29+i; put(ws,f'B{r}',g,PCT,INPUT)
    for c in 'CDEF': put(ws,f'{c}{r}',f"=(({I['stake']}*{c}$28*{I['arr']}*(1+$B{r})^5)/{I['p1inv']})^(1/5)-1",PCT)
put(ws,'B32','Growth ↓ (rows) · IRR vs hurdle (WACC)'); put(ws,'C32',f"={I['wacc']}",PCT,LINK)

# ================= SENSITIVITIES =================
ws=sheet('Sensitivities',[3,40,14,14,14,14,14,14])
title(ws,'7. Sensitivities','Year-1 EPS and FCF under key downside scenarios — churn and capital requirements — plus DCF value by growth')
section(ws,5,'A. Full acquisition (headline mix) — year-1 EPS by churn and cash-yield assumption',7)
hdr(ws,6,[2,3,4,5,6,7],['Cash yield ↓ · Churn →','0%','30%','37.5%','45%','55%'])
churn_vals=[0,0.30,0.375,0.45,0.55]
for j,cv in enumerate(churn_vals): put(ws,f'{"CDEFG"[j]}6',cv,'0.0%',INPUT)
for i,yv in enumerate([0.05,0.06,0.07]):
    r=7+i; put(ws,f'B{r}',yv,PCT,INPUT)
    for j in range(5):
        c='CDEFG'[j]
        # EPS = (PAT - dealcash*yield*(1-t) + liminal Y1 PAT after churn c - integ) / shares_pf ; liminal Y1 PAT = rev1*(1-c)*m1*patconv - sticky*rev1*c  (if EBITDA>0 else raw)
        f=(f"=({I['pat']}-{I['dealcash']}*$B{r}*(1-{I['tax']})"
           f"+IF(({I['arr']}*(1+{I['g']})*(1-{c}$6)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$6)>0,"
           f"({I['arr']}*(1+{I['g']})*(1-{c}$6)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$6)*{I['patconv']},"
           f"({I['arr']}*(1+{I['g']})*(1-{c}$6)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$6)))"
           f"/({I['shares']}+{I['dealeq']}/{I['price']})")
        put(ws,f'{c}{r}',f,NUM2)
put(ws,'B10','Baseline EPS for reference (₹)'); put(ws,'C10',f"={I['eps']}",NUM2,LINK)
section(ws,12,'B. Full acquisition — year-1 incremental FCF by churn and capital-drag treatment (₹ Cr)',7)
hdr(ws,13,[2,3,4,5,6,7],['Capital drag ↓ · Churn →','0%','30%','37.5%','45%','55%'])
for j,cv in enumerate(churn_vals): put(ws,f'{"CDEFG"[j]}13',cv,'0.0%',INPUT)
for i,dv in enumerate([0,195,375,750]):
    r=14+i; put(ws,f'B{r}',dv,'#,##0',INPUT)
    for j in range(5):
        c='CDEFG'[j]
        lim=(f"IF(({I['arr']}*(1+{I['g']})*(1-{c}$13)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$13)>0,"
             f"({I['arr']}*(1+{I['g']})*(1-{c}$13)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$13)*{I['patconv']}*{I['fcfconv']},"
             f"({I['arr']}*(1+{I['g']})*(1-{c}$13)*MIN({I['mstep']},{I['mcapm']})-{I['sticky']}*{I['arr']}*(1+{I['g']})*{c}$13))")
        put(ws,f'{c}{r}',f"={lim}-{I['dealcash']}*{I['yield']}*(1-{I['tax']})-$B{r}-{I['integ']}",NUM)
put(ws,'B19','Reading: the ₹750 Cr row is the case assumption; ₹195 Cr ≈ pro-rata at 25%+; ₹0 = drag avoided or structured away. No cell in the ₹750 Cr row is positive at any churn level.',font=F(size=9,italic=True,color='595959'),border=False)
section(ws,21,'C. Phase-1 minority — year-1 EPS by cash yield and minority-level capital drag (economic basis)',7)
hdr(ws,22,[2,3,4,5,6],['Cash yield ↓ · Drag at minority (₹ Cr) → (EPS unaffected: drag is a cash item; see FCF row)','0','100','195','750'])
for j,dv in enumerate([0,100,195,750]): put(ws,f'{"CDEF"[j]}22',dv,'#,##0',INPUT)
for i,yv in enumerate([0.05,0.06,0.07]):
    r=23+i; put(ws,f'B{r}',yv,PCT,INPUT)
    for j in range(4):
        c='CDEF'[j]
        put(ws,f'{c}{r}',f"=({I['pat']}-{I['p1inv']}*$B{r}*(1-{I['tax']})+{I['stake']}*'Liminal Projection'!$D$8)/{I['shares']}",NUM2)
put(ws,'B26','Year-1 FCF effect of a minority-level drag (₹ Cr/yr)'); 
for j in range(4):
    c='CDEF'[j]; put(ws,f'{c}26',f"=-{I['p1inv']}*{I['yield']}*(1-{I['tax']})-{c}$22",NUM)
section(ws,28,'D. Standalone DCF value of Liminal by growth rate (team assumptions; no churn, no drag)',7)
hdr(ws,29,[2,3,4,5,6,7],['Growth p.a. for 10 years →','10%','20%','30%','40%','Required for ₹4,000 Cr'])
gs=[0.10,0.20,0.30,0.40]
for j,g in enumerate(gs): put(ws,f'{"CDEF"[j]}29',g,PCT,INPUT)
put(ws,'B30','DCF value (₹ Cr)')
for j in range(4):
    c='CDEF'[j]
    terms='+'.join([f"({I['arr']}*(1+{c}$29)^{y}*MIN({I['mstep']}*{y},{I['mcapm']})*{I['patconv']}*{I['fcfconv']})/(1+{I['wacc']})^{y}" for y in range(1,11)])
    tv=f"({I['arr']}*(1+{c}$29)^10*{I['mcapm']}*{I['patconv']}*{I['fcfconv']})*(1+{I['tg']})/({I['wacc']}-{I['tg']})/(1+{I['wacc']})^10"
    put(ws,f'{c}30',f"={terms}+{tv}",NUM,bold=True)
put(ws,'B31','Multiple of ARR'); 
for j in range(4): c='CDEF'[j]; put(ws,f'{c}31',f"={c}30/{I['arr']}",MULT)
put(ws,'B32','Supports ₹4,000 Cr headline?')
for j in range(4): c='CDEF'[j]; put(ws,f'{c}32',f'=IF({c}30>={I["deal"]},"Yes","No")',align='center')
put(ws,'G30','≈ 31% p.a. (solve by entering a growth rate on Inputs; read Valuation & Churn!G36)',font=F(size=9,italic=True,color='595959'),align='left'); ws['G30'].alignment=Alignment(horizontal='left',vertical='center',wrap_text=False)
section(ws,34,'E. Downside playbook — triggers read from the model',7)
hdr(ws,35,[2,3,4],['Trigger','Model reading','Response'])
dp=[('Churn > 45%',"='Valuation & Churn'!E11",'Do not exercise control / activate price protection / reassess partnership'),
('Capital requirement unacceptable',"='PAT & FCF Breakeven'!C32",'Remain minority / restructure / exit'),
('Key clients resist',"='Valuation & Churn'!E21",'Strengthen ring-fence; no control exercise without acceptable retention'),
('Paytm share price compresses',"='Call Option & Earn-out'!E22",'Avoid fixed-value equity issuance that creates excessive dilution'),
('PAT / FCF case fails',"='PAT & FCF Breakeven'!C31",'Do not escalate capital because of sunk cost'),
('Regulatory / security conditions fail','Gate (qualitative)','Suspend exercise / terminate where contractual rights permit')]
for i,(a,b,c) in enumerate(dp):
    r=36+i; put(ws,f'B{r}',a,bold=True); put(ws,f'C{r}',b,font=LINK if b.startswith('=') else F()); put(ws,f'D{r}',c)
    if 'Churn'==a[:5] or 'Key' in a: ws[f'C{r}'].number_format=MULT if 'Churn >' in a else PCT
    if 'share price' in a: ws[f'C{r}'].number_format=PCT
ws.column_dimensions['D'].width=70

# ================= SUMMARY =================
ws=sheet('Summary',[3,58,18,50])
title(ws,'Summary of key outputs','Live links to the model — recommendation: 25% minority + partnership + call option; control only after gates clear')
hdr(ws,5,[2,3,4],['Output','Value','Where'])
rowsS=[('Headline multiple (deal value / ARR)',f"={I['mult']}",MULT,'Inputs / Valuation & Churn'),
('Effective multiple at 45% churn',"='Valuation & Churn'!E11",MULT,'Valuation & Churn'),
('Implied value at 18.2× after 30% / 45% churn (₹ Cr)',"='Valuation & Churn'!F9",NUM,'Valuation & Churn (see F11 for 45%)'),
('Growth required to recover ₹220 Cr after 45% churn',"='Valuation & Churn'!E17",PCT,'Valuation & Churn'),
('Mechanical EPS dilution — headline mix (share count only)',"='Financing & EPS'!C10",PCT,'Financing & EPS'),
('Year-1 EPS — full acquisition, headline mix, incl. financing costs (₹)',"='Financing & EPS'!C26",NUM2,'Financing & EPS'),
('Year-1 EPS — Phase-1 minority, economic basis (₹)',"='Financing & EPS'!C46",NUM2,'Financing & EPS'),
('Cash remaining after Phase 1 (₹ Cr)',"='Financing & EPS'!C41",NUM,'Financing & EPS'),
('Full acquisition — first year of PAT breakeven',"='PAT & FCF Breakeven'!C31",None,'PAT & FCF Breakeven'),
('Full acquisition — first year of FCF breakeven (after ₹750 Cr drag)',"='PAT & FCF Breakeven'!C32",None,'PAT & FCF Breakeven'),
('Control exercise — first year of FCF breakeven (drag per Inputs)',"='PAT & FCF Breakeven'!C76",None,'PAT & FCF Breakeven'),
('UPI MDR as % of capital drag — gross / after conversion',f"={I['mdrgross']}",PCT,'Inputs (see next line)'),
('UPI MDR as % of capital drag — after conversion',f"={I['mdrnet']}",PCT,'Inputs'),
('10-year NPV of capital drag at WACC (₹ Cr)',f"={I['dragnpv']}",NUM,'Inputs'),
('Maximum total consideration incl. Phase 1 (₹ Cr)',"='Call Option & Earn-out'!C10",NUM,'Call Option & Earn-out'),
('Maximum unconditional consideration (₹ Cr)',"='Call Option & Earn-out'!C11",NUM,'Call Option & Earn-out'),
('Standalone DCF value at base growth (₹ Cr) and verdict',"='Valuation & Churn'!G36",NUM,'Valuation & Churn')]
for i,(a,f,fm,w) in enumerate(rowsS):
    r=6+i; put(ws,f'B{r}',a); put(ws,f'C{r}',f,fm,LINK,fill=LYEL if i in (5,6,9) else None); put(ws,f'D{r}',w,font=F(size=9,color='595959'))
wb.move_sheet('Summary', offset=-(len(wb.sheetnames)-2))
# sheet order / fonts
for w in wb.worksheets:
    allfont(w)
    w.sheet_properties.tabColor=TABS.get(w.title,'1F3864')
# ---- banding, alignment and conditional formatting ----
REDF=Font(name=FN,color='C00000'); GREENF=Font(name=FN,color='375623')
YES=PatternFill('solid',fgColor='C6EFCE'); NO=PatternFill('solid',fgColor='FFC7CE')
for w in wb.worksheets:
    mr=w.max_row; mc=w.max_column; last=get_column_letter(mc)
    for row in w.iter_rows(min_row=1,max_row=mr):
        for c in row:
            if c.value is None: continue
            a=c.alignment; c.alignment=Alignment(horizontal=a.horizontal or 'center',vertical='center',wrap_text=a.wrap_text)
    if w.title in ('Cover',): continue
    rng=f"C1:{last}{mr}"
    w.conditional_formatting.add(rng,CellIsRule(operator='lessThan',formula=['0'],font=REDF))
    w.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['"Yes"'],fill=YES,font=GREENF))
    w.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['"No"'],fill=NO,font=REDF))
    w.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['"Not within 10 years"'],fill=NO,font=REDF))
    w.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['"Not supported"'],fill=NO,font=REDF))
    w.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['"Supported"'],fill=YES,font=GREENF))
S=wb['Sensitivities']
for r in ('C7:G9','C23:F25'): S.conditional_formatting.add(r,ColorScaleRule(start_type='min',start_color='F8CBAD',mid_type='percentile',mid_value=50,mid_color='FFFFFF',end_type='max',end_color='C6EFCE'))
S.conditional_formatting.add('C14:G17',ColorScaleRule(start_type='min',start_color='F8CBAD',end_type='max',end_color='FFFFFF'))
S.conditional_formatting.add('C30:F30',ColorScaleRule(start_type='min',start_color='FFFFFF',end_type='max',end_color='C6EFCE'))
C=wb['Call Option & Earn-out']; C.conditional_formatting.add('D14:D20',DataBarRule(start_type='num',start_value=0,end_type='max',color='2F5597'))
C.conditional_formatting.add('C29:F31',ColorScaleRule(start_type='min',start_color='F8CBAD',mid_type='num',mid_value=0.12,mid_color='FFFFFF',end_type='max',end_color='C6EFCE'))
V=wb['Valuation & Churn']; V.conditional_formatting.add('E8:E11',DataBarRule(start_type='num',start_value=0,end_type='max',color='C65911'))
# band alternate rows in tables that were left white (Valuation churn table, projection rows, breakeven rows)
def band(ws,r1,r2,c1,c2):
    for r in range(r1,r2+1):
        if (r-r1)%2==1:
            for c in range(c1,c2+1):
                cell=ws.cell(row=r,column=c)
                if cell.fill is None or cell.fill.fgColor is None or cell.fill.fgColor.rgb in ('00000000',None,'FFFFFFFF'): cell.fill=BAND
band(V,8,11,2,7); band(V,25,34,2,7)
L=wb['Liminal Projection']; band(L,7,12,2,13); band(L,17,26,2,13); band(L,31,34,2,13)
B=wb['PAT & FCF Breakeven']; band(B,7,29,2,12); band(B,37,50,2,12); band(B,57,73,2,12)
band(C,14,20,2,7); band(S,7,9,2,7); band(S,14,17,2,7); band(S,23,25,2,6)
Fi=wb['Financing & EPS']; band(Fi,15,32,2,7)
for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if c.font.name!=FN: c.font=F(bold=c.font.bold,italic=c.font.italic,color=c.font.color,size=c.font.size or 11)
wb.save('ETERNAL_Satoshi_Gate_Transaction_Model.xlsx'); print('saved')
