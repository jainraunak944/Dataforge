import json, os, html
ROOT = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(ROOT, 'project', 'slides')
NAVY='#0B2A5B'; BLUE='#1E63D6'; CYAN='#00B4E6'; INK='#1C2433'; BODY='#3A4658'; MUTED='#6B7A90'
BG='#F4F7FC'; CARD='#FDFDFE'; LINE='#D9E2F0'; TINT='#E9F0FB'; GREEN='#1B8A4C'; RED='#C63C3C'; AMBER='#D98A1B'
HF="'Poppins', Arial, sans-serif"; BF="'Inter', Arial, sans-serif"

order=[]; notes={}
def slide(id_, title, accent, body, note, tag='', num=None, bg=BG):
    order.append(id_)
    n = len(order)
    h = f'''<section id="{id_}" data-transition="fade" style="background:{bg}; color:{INK}; font-family:{BF}; padding:48px 64px 40px; display:flex; flex-direction:column; gap:22px">
<div style="display:flex; align-items:end; justify-content:space-between; gap:24px">
  <div style="display:flex; flex-direction:column; gap:6px">
    <p style="font-size:24px; font-weight:600; color:{BLUE}; letter-spacing:2px; text-transform:uppercase">{tag}</p>
    <h2 style="font-family:{HF}; font-size:44px; font-weight:700; line-height:1.1; color:{NAVY}">{title} <span style="color:{BLUE}">{accent}</span></h2>
    <hr style="width:120px; height:5px; background:{BLUE}; border:none; border-radius:3px">
  </div>
  <div style="display:flex; align-items:center; gap:14px; background:{CARD}; border:1px solid {LINE}; border-radius:12px; padding:10px 18px">
    <x-shape kind="rounded" style="width:34px; height:34px; background:{NAVY}; border-radius:8px"></x-shape>
    <p style="font-size:24px; font-weight:600; color:{NAVY}">Project Satoshi Gate</p><p style="font-size:24px; color:{MUTED}">Paytm × Liminal</p>
  </div>
</div>
{body}
<div style="flex:1"></div>
<div style="display:flex; justify-content:space-between; align-items:center">
  <p style="font-size:24px; color:{MUTED}">CF = case fact · CALC = arithmetic on case facts · TA = team assumption (Slide 7) · ₹ in Cr</p>
  <p style="font-size:24px; color:{MUTED}; font-weight:600">{n:02d}</p>
</div>
<aside>{html.escape(note)}</aside>
</section>'''
    open(os.path.join(S, id_+'.html'),'w').write(h)

def card(title, items, icon='Check', color=BLUE, flex='1', extra=''):
    lis=''.join(f'<li>{i}</li>' for i in items)
    return f'''<div style="flex:{flex}; display:flex; flex-direction:column; gap:10px; background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:18px 20px; box-shadow:0 4px 14px rgba(11,42,91,0.06){extra}">
  <div style="display:flex; align-items:center; gap:12px"><div style="display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:{color}; border-radius:22px"><x-icon name="{icon}" style="width:24px; height:24px; color:#FFFFFF"></x-icon></div><h3 style="font-size:26px; font-weight:700; color:{NAVY}">{title}</h3></div>
  <ul style="font-size:24px; line-height:1.3; color:{BODY}; padding:0 0 0 26px">{lis}</ul>
</div>'''

def kpi(value, label, sub, color=BLUE, subcolor=GREEN):
    return f'''<div style="flex:1; display:flex; align-items:center; gap:14px; background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:14px 18px; box-shadow:0 4px 14px rgba(11,42,91,0.06)">
  <x-shape kind="rounded" style="width:12px; height:64px; background:{color}; border-radius:6px"></x-shape>
  <div style="display:flex; flex-direction:column; gap:2px"><p style="font-family:{HF}; font-size:38px; font-weight:700; color:{color}; line-height:1.1">{value}</p><p style="font-size:24px; font-weight:600; color:{INK}">{label}</p><p style="font-size:24px; color:{subcolor}">{sub}</p></div>
</div>'''

def numbox(n, color=BLUE):
    return f'<div style="display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:{color}; border-radius:8px"><p style="font-size:24px; font-weight:700; color:#FFFFFF">{n}</p></div>'

def numrow(n, text, color=BLUE):
    return f'<div style="display:flex; align-items:center; gap:14px; background:{CARD}; border:1px solid {LINE}; border-radius:10px; padding:10px 14px">{numbox(n,color)}<p style="font-size:24px; line-height:1.3; color:{BODY}">{text}</p></div>'

def panel(title, inner, icon='Chart', color=BLUE, flex='1'):
    return f'''<div style="flex:{flex}; display:flex; flex-direction:column; gap:12px; background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:18px 20px; box-shadow:0 4px 14px rgba(11,42,91,0.06)">
  <div style="display:flex; align-items:center; gap:12px"><div style="display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:{color}; border-radius:22px"><x-icon name="{icon}" style="width:24px; height:24px; color:#FFFFFF"></x-icon></div><h3 style="font-size:26px; font-weight:700; color:{NAVY}">{title}</h3></div>
  {inner}</div>'''

def table(rows, widths, size=24, head_bg=NAVY, band=True, first_bold=True):
    out=f'<table style="font-size:{size}px; color:{INK}; border:1px solid {LINE}; border-radius:8px; background:{CARD}; padding:6px 10px">'
    for r,row in enumerate(rows):
        if r==0:
            out+=f'<tr style="background:{head_bg}">'+''.join(f'<th style="width:{w}%; color:#FFFFFF; text-align:{"left" if c==0 else "center"}">{cell}</th>' for c,(cell,w) in enumerate(zip(row,widths)))+'</tr>'
        else:
            bg=f' style="background:{TINT}"' if band and r%2==0 else ''
            out+=f'<tr{bg}>'+''.join(f'<td style="text-align:{"left" if c==0 else "center"}; color:{INK}">{cell}</td>' for c,cell in enumerate(row))+'</tr>'
    return out+'</table>'

def bars(data, h=220, maxv=None, color=BLUE, colors=None, fmt=lambda v: f'{v:g}', w=None, label_size=24):
    maxv = maxv or max(v for _,v in data)
    cols=''
    for i,(lab,v) in enumerate(data):
        c=(colors[i] if colors else color)
        bh=max(6,int(h*v/maxv))
        cols+=f'''<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px">
<p style="font-size:24px; font-weight:700; color:{c}">{fmt(v)}</p>
<x-shape kind="rounded" style="width:{w or 64}px; height:{bh}px; background:{c}; border-radius:6px"></x-shape>
<p style="font-size:{label_size}px; color:{BODY}; text-align:center; line-height:1.15">{lab}</p></div>'''
    return f'<div style="display:flex; align-items:end; gap:10px; border-bottom:2px solid {LINE}; padding:0 0 4px">{cols}</div>'

def hbars(data, maxv=None, color=BLUE, colors=None, fmt=lambda v: f'{v:g}', trackw=520):
    maxv = maxv or max(v for _,v in data)
    rows=''
    for i,(lab,v) in enumerate(data):
        c=(colors[i] if colors else color); bw=max(8,int(trackw*v/maxv))
        rows+=f'''<div style="display:flex; align-items:center; gap:12px"><p style="width:250px; font-size:24px; color:{BODY}; text-align:right">{lab}</p>
<div style="width:{trackw}px; display:flex; align-items:center; background:{TINT}; border-radius:6px"><x-shape kind="rounded" style="width:{bw}px; height:30px; background:{c}; border-radius:6px"></x-shape></div>
<p style="font-size:24px; font-weight:700; color:{c}">{fmt(v)}</p></div>'''
    return f'<div style="display:flex; flex-direction:column; gap:10px">{rows}</div>'

def pill(text, bg=BLUE, fg='#FFFFFF'):
    return f'<p style="font-size:24px; font-weight:600; color:{fg}; background:{bg}; padding:6px 16px; border-radius:20px; white-space:nowrap">{text}</p>'

def banner(text, bg=NAVY):
    return f'<div style="display:flex; align-items:center; gap:16px; background:{bg}; border-radius:12px; padding:14px 22px"><x-icon name="Lightbulb" style="width:30px; height:30px; color:{CYAN}"></x-icon><p style="font-size:26px; font-weight:600; color:#FFFFFF; line-height:1.25">{text}</p></div>'

# ---------------- COVER ----------------
order.append('cover')
open(os.path.join(S,'cover.html'),'w').write(f'''<section id="cover" data-transition="fade" style="background:{CARD}; color:{INK}; font-family:{BF}; padding:0; display:flex; flex-direction:column">
<x-shape kind="rect" style="position:absolute; left:1180px; top:0px; width:740px; height:1080px; background:{TINT}"></x-shape>
<x-shape kind="rect" style="position:absolute; left:1300px; top:120px; width:620px; height:960px; background:{NAVY}"></x-shape>
<x-shape kind="rect" style="position:absolute; left:1480px; top:0px; width:440px; height:520px; background:{BLUE}"></x-shape>
<x-shape kind="rect" style="position:absolute; left:1660px; top:640px; width:260px; height:440px; background:{CYAN}"></x-shape>
<x-shape kind="rect" style="position:absolute; left:96px; top:150px; width:8px; height:640px; background:{BLUE}; border-radius:4px"></x-shape>
<div style="position:absolute; left:150px; top:140px; width:1000px; display:flex; flex-direction:column; gap:26px">
  <div style="display:flex; align-items:center; gap:14px"><x-shape kind="rounded" style="width:40px; height:40px; background:{NAVY}; border-radius:10px"></x-shape><p style="font-family:{HF}; font-size:32px; font-weight:700; color:{NAVY}">Paytm</p><p style="font-size:32px; color:{MUTED}">×</p><p style="font-family:{HF}; font-size:32px; font-weight:700; color:{BLUE}">Liminal Custody Solutions</p></div>
  <p style="font-size:26px; font-weight:600; color:{BLUE}; letter-spacing:3px; text-transform:uppercase">Board transaction recommendation · September 2026</p>
  <h1 style="font-family:{HF}; font-size:112px; font-weight:800; line-height:1.02; color:{NAVY}">Project<br><span style="color:{BLUE}">Satoshi Gate</span></h1>
  <hr style="width:110px; height:6px; background:{BLUE}; border:none; border-radius:3px">
  <p style="font-size:34px; font-weight:600; line-height:1.3; color:{INK}">Strategic access today.<br>Control only when the economics are proven.</p>
  <p style="font-size:26px; line-height:1.4; color:{BODY}">A 26% strategic stake, a commercial custody/MPC partnership and a pre-agreed call option, instead of a ₹4,000 Cr full acquisition. Supported by an auditable accretion/dilution and PAT/FCF breakeven model.</p>
</div>
<div style="position:absolute; left:1380px; top:200px; width:460px; display:flex; flex-direction:column; gap:18px">
  <div style="display:flex; flex-direction:column; gap:4px; background:rgba(255,255,255,0.10); border-radius:12px; padding:18px 22px"><p style="font-family:{HF}; font-size:52px; font-weight:700; color:#FFFFFF">₹1,040 Cr</p><p style="font-size:24px; color:#DCE7FA">Unconditional cheque: 26% stake, cash-funded</p></div>
  <div style="display:flex; flex-direction:column; gap:4px; background:rgba(255,255,255,0.10); border-radius:12px; padding:18px 22px"><p style="font-family:{HF}; font-size:52px; font-weight:700; color:#FFFFFF">≤ ₹2,960 Cr</p><p style="font-size:24px; color:#DCE7FA">Control tranche, paid only against retained ARR</p></div>
  <div style="display:flex; flex-direction:column; gap:4px; background:rgba(255,255,255,0.10); border-radius:12px; padding:18px 22px"><p style="font-family:{HF}; font-size:52px; font-weight:700; color:#FFFFFF">6 gates</p><p style="font-size:24px; color:#DCE7FA">Consents · Capital · Valuation · PAT · FCF · Compliance</p></div>
</div>
<aside>Open with the one-line thesis: Paytm should buy access and an option now, and pay for control only after client retention and regulatory capital treatment are observable.</aside>
</section>''')

# ---------------- SLIDE 1 RECOMMENDATION ----------------
WHYNOT=f'''{table([['Pressure','Case fact → calc','So what'],
   ['Client revolt','30–45% ARR lost in 12 months (CF)','18.2× becomes 26–33× retained ARR'],
   ['Capital trap','₹750 Cr/yr FCF drag (CF)','Larger than Paytm EBITDA; NPV > price'],
   ['Earnings','Liminal ~breakeven (CF)','Year-1 EPS ₹5.29 (−29%); ₹6.08 at 0% churn'],
   ['Breakeven','Drag vs ₹115 Cr MDR (CF)','FCF never breaks even in 10 yrs; MDR covers ≤15%']],[22,38,40])}
   {banner('Base expectation, stated plainly: under the case’s own assumptions the modal outcome is <b>Hold</b>. The option is insurance and a block on PhonePe–Mastercard, not a plan to buy.')}'''
body=f'''
<div style="display:flex; gap:16px">
{kpi('₹1,040 Cr','Phase-1 investment','26% stake · cash · 0.9% of market cap',BLUE)}
{kpi('−29%','Full-deal year-1 EPS','₹5.29 vs ₹7.50 at the headline mix',RED,RED)}
{kpi('₹750 Cr/yr','Capital drag at control','117% of Paytm EBITDA · NPV ₹4,238 Cr',RED,RED)}
{kpi('26–33×','Retained-ARR multiple','18.2× headline after 30–45% churn',AMBER,AMBER)}
{kpi('Hold','Base-case outcome','Control only if Liminal earns it',GREEN,GREEN)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('Recommendation: a staged structure, not a full acquisition',
   numrow(1,'<b>Invest ₹1,040 Cr in cash for 26%</b> — one share above the 25% special-resolution threshold: negative control without operational control (TA).')+
   numrow(2,'<b>Commercial custody/MPC partnership</b> for tokenized-treasury, e₹ and cross-border settlement use cases.')+
   numrow(3,'<b>Ring-fence Liminal</b>: standalone brand, arm’s-length board, information barriers, independent compliance.')+
   numrow(4,'<b>Call option on the remaining 74%</b>, months 12–24, capped at ₹2,960 Cr: ₹1,650 Cr upfront + up to ₹1,310 Cr retention earn-out. Never more than ₹4,000 Cr in total.'),
   'Verified',BLUE,'1.25')}
 {panel('Why not 100% today', WHYNOT,'Warning',RED,'1.35')}
</div>
<div style="display:flex; align-items:center; gap:16px; background:{CARD}; border:2px solid {BLUE}; border-radius:14px; padding:12px 22px">
 <p style="font-size:26px; font-weight:700; color:{NAVY}">BOARD ASK</p><p style="font-size:24px; color:{BODY}">Approve <b>Invest → Validate (12 months) → Exercise / Hold / Walk Away</b>; authorise the ₹1,040 Cr investment, option negotiation and guardrails (cash ≥ ₹5,000 Cr, gross debt/EBITDA ≤ 1.5×, no unconditional equity); delegate gate reviews to the M&A/Risk committee.</p>
 <div style="flex:1"></div>{pill('Consents')}{pill('Capital')}{pill('Valuation')}{pill('PAT')}{pill('FCF')}{pill('Compliance')}
</div>'''
slide('rec','Board recommendation:','buy access and an option, not full control',body,'Lead with the five tiles, then the four pressures. Say the word Hold before anyone asks whether this is just a minority stake.','Slide 1 · Recommendation')

# ---------------- SLIDE 2 STRATEGIC RATIONALE ----------------
def stage(label, sub, color):
    return f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:6px; background:{color}; border-radius:12px; padding:14px 10px"><p style="font-size:26px; font-weight:700; color:#FFFFFF; text-align:center; line-height:1.15">{label}</p><p style="font-size:24px; color:#E3ECFA; text-align:center; line-height:1.15">{sub}</p></div>'
arrow=f'<div style="display:flex; align-items:center"><x-shape kind="arrow-right" style="width:44px; height:24px; background:{BLUE}"></x-shape></div>'
body=f'''
<div style="display:flex; align-items:stretch; gap:10px; background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:16px 20px">
 <p style="font-size:24px; font-weight:700; color:{NAVY}; width:150px; align-self:center; line-height:1.2">STRATEGIC BRIDGE</p>
 {stage('Payments','UPI · merchants · consumer (CF)',NAVY)}{arrow}{stage('Custody & MPC','Liminal: ISO 27001, SOC 2 (CF)',BLUE)}{arrow}{stage('Tokenized assets','Treasury, digital assets',BLUE)}{arrow}{stage('e₹ / CBDC rails','RBI pilot alignment (CF)',CYAN)}{arrow}{stage('B2B & cross-border','Settlement infrastructure',CYAN)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {card('Paytm today (CF)',['₹1,18,750 Cr market cap on a turnaround re-rating','UPI and checkout growth slowing; PhonePe and Google Pay dominate volume','Regulatory scrutiny since RBI’s 2024 Paytm Payments Bank restrictions','Stated ambition: tokenized treasury and cross-border settlement aligned with e₹'],'Home',NAVY)}
 {card('Liminal adds (CF)',['Institutional digital-asset custody + MPC infrastructure, founded 2021','Clients: exchanges, hedge funds, OTC desks','HDFC Bank, Axis Bank, CoinDCX, ZebPay = 60% of ₹220 Cr ARR','Approximately PAT breakeven today'],'Lock',BLUE)}
 {card('Why it matters (TA)',['Custody/MPC is the trust layer every tokenized-settlement product needs; certifications take years to build','Adjacent to the core, not a replacement for it','A hedge on the e₹ thesis: if it scales Paytm holds the rail; if not, the cheque is ₹1,040 Cr, not ₹4,000 Cr'],'Lightbulb',CYAN)}
</div>
<div style="display:flex; gap:18px">
 {panel('Could a partnership alone do the job?', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">For the <b>capability</b>, largely yes. For <b>security of supply</b>, no: a pure partnership leaves Liminal for sale, and the case says the consortium buys it if Paytm walks. The 26% stake + ROFR/ROFO + call option buys the blocking right and the information rights to run the validation; the partnership captures the capability. Together they cost 26% of the headline price.</p>','Link',BLUE,'1.4')}
 {panel('Large enough to leave the core?', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Large enough for a 26% position and a partnership; not large enough, on the case’s numbers, for a ₹4,000 Cr control cheque with a ₹750 Cr/yr carrying cost. <b>We size the bet to the evidence.</b> Walking away costs the neutral custodian and a 24–36 month build-or-partner path (TA).</p>','Activity',NAVY,'1')}
</div>'''
slide('rationale','Strategic rationale:','access captures the value, ownership adds the risk',body,'The bridge is the story: each stage needs the one before it. Then answer 5.1 directly: partnership-only fails on security of supply.','Slide 2 · Strategic rationale')

# ---------------- SLIDE 3 OWNERSHIP PARADOX ----------------
drag_chart = bars([('Liminal ARR',220),('Paytm PAT',480),('Paytm EBITDA',640),('Capital drag / yr',750)],h=210,colors=[BLUE,NAVY,NAVY,RED],fmt=lambda v:f'₹{v:,}')
mult_chart = bars([('0% churn',18.2),('30%',26.0),('37.5%',29.1),('45%',33.1)],h=210,colors=[BLUE,AMBER,AMBER,RED],fmt=lambda v:f'{v}×')
body=f'''
<div style="display:flex; gap:16px">
 {card('1 · Customer conflict',['Top-4 = ₹132 Cr of ₹220 Cr ARR (CF)','Case: ₹66–99 Cr leaves in 12 months = 50–75% of the top-4 book','Trigger: a competing consumer wallet owning the custodian'],'Users',RED)}
 {card('2 · Regulatory capital',['₹750 Cr/yr drag = 117% of EBITDA, 156% of PAT, 3.4× Liminal revenue','Liminal needs ~₹4,000 Cr ARR (18× today) to self-fund it','16 years away at 20% growth, 11 at 30% (TA)'],'Lock',RED)}
 {card('3 · Earnings',['Liminal ~breakeven: no earnings to offset the deal’s own cost (CF)','Year-1 EPS ₹5.29 (−29%) at the headline mix (TA)','The “share-count only” ₹7.38 hides 95% of the dilution'],'Chart',AMBER)}
 {card('4 · Valuation',['18.2× headline → 26–33× retained ARR','Each 10 pts of churn destroys ₹400 Cr at the paid multiple','Paytm at ~247× trailing P/E: a −29% print invites the buyback debate (CF §3.3)'],'Warning',AMBER)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('The drag in context — ₹ Cr per year', drag_chart+f'<p style="font-size:24px; color:{MUTED}">10-year NPV of the drag at 12% WACC: <b>₹4,238 Cr</b>, more than the ₹4,000 Cr price (TA).</p>','Chart',RED)}
 {panel('Effective multiple on retained ARR', mult_chart+f'<p style="font-size:24px; color:{MUTED}">₹4,000 Cr ÷ retained ARR. Growth needed just to recover ₹220 Cr: +42.9% after 30% churn, +81.8% after 45% (CALC).','Chart',AMBER)}
 <div style="flex:0.9; display:flex; flex-direction:column; gap:14px">
  {banner('CORE DEAL PARADOX — Paytm wants Liminal for its institutional franchise. Taking control is what breaks that franchise and what triggers the capital requirement.',NAVY)}
  {banner('BOARD IMPLICATION — Separate the <b>strategic attractiveness of Liminal</b> (high) from the <b>economic attractiveness of owning 100% today</b> (negative under the case’s own assumptions).',BLUE)}
 </div>
</div>'''
slide('paradox','The ownership paradox:','control impairs the asset and the drag is worth more than the company',body,'Point at the red bar: the drag alone exceeds Paytm’s EBITDA. Everything else on the slide follows from that.','Slide 3 · Ownership paradox')

# ---------------- SLIDE 4 OPTIONS ----------------
rows=[['Dimension','Full acquisition','26% minority + option ★','Joint venture','Walk away'],
['Strategic access','Full','High: partnership + board seat + info rights','High inside JV scope','None; 24–36 mo build (TA)'],
['Control','Full, now','Negative now; positive optional (m12–24)','Shared','None'],
['Counter-bid defence','Complete','ROFR/ROFO + 26% veto + call option','Weak: Liminal still for sale','None: consortium acquires'],
['Churn exposure','30–45% (CF)','Not triggered (TA), tested via consents','Not triggered (TA)','Nil'],
['₹750 Cr drag','Applies (CF)','Not expected at 26% (TA); RBI comfort is a CP','Depends on JV custody scope','Nil'],
['Upfront commitment','₹2,100 Cr cash + 1.02 Cr shares','₹1,040 Cr cash; no shares, no debt','Capital + IP licence (TA)','Nil'],
['Year-1 EPS vs ₹7.50','₹5.29 (−29%)','₹6.81 (−9%): foregone interest only','Not modelled','₹7.50'],
['FCF profile','Never breaks even (drag)','Return is equity value; no cash yield','Not modelled','n/a'],
['Reversibility','Low','Medium–high (tag, ROFO)','Medium','High'],
['Future-control optionality','Already spent','Preserved and priced','Negotiable','Lost']]
body=f'''
{table(rows,[18,20,24,19,19],size=24)}
<div style="display:flex; gap:18px; flex:1">
 {panel('The JV, if needed (TA)', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">A Paytm-majority “SettleCo” for e₹/tokenized-treasury settlement: Liminal licenses MPC and runs custody ops; Paytm brings distribution, merchants and capital; Liminal’s institutional book stays outside. No revolt, no reserve on Paytm, but it does not block the consortium and splits governance. <b>Our fallback if RBI applies a reserve at minority level.</b></p>','Settings',NAVY,'1')}
 {panel('Conclusion', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Minority + partnership + call option defers the two largest unresolved risks — <b>client response</b> and <b>capital treatment</b> — until they are observable, at 26% of the cheque, while removing the consortium’s easiest path.</p>','Verified',GREEN,'1')}
 {panel('Discipline', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">We do <b>not</b> assume a minority automatically eliminates churn or the ₹750 Cr requirement. Both are gates, tested before any control is exercised.</p>','Warning',RED,'0.8')}
</div>'''
slide('options','Strategic options:','only the minority with an option secures access and blocks the bid',body,'Walk the table column by column; the star column wins on defence, drag and reversibility at once.','Slide 4 · Strategic options')

# ---------------- SLIDE 5 ARCHITECTURE ----------------
eo=[(0,2960),(10,2669),(20,2378),(30,2087),(37.5,1868),(45,1650),(55,1650)]
eo_chart=bars([(f'{c:g}%',v) for c,v in eo],h=190,maxv=3200,colors=[GREEN,GREEN,BLUE,BLUE,AMBER,RED,RED],fmt=lambda v:f'{v:,}',w=54)
def phase(n,title,lines,color):
    return f'''<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{CARD}; border:1px solid {LINE}; border-top:8px solid {color}; border-radius:14px; padding:14px 16px">
<div style="display:flex; align-items:center; gap:10px">{numbox(n,color)}<h3 style="font-size:26px; font-weight:700; color:{NAVY}">{title}</h3></div>
<ul style="font-size:24px; line-height:1.3; color:{BODY}; padding:0 0 0 24px">{''.join(f'<li>{l}</li>' for l in lines)}</ul></div>'''
body=f'''
<div style="display:flex; gap:14px">
 {phase(1,'Strategic entry · ₹1,040 Cr',['Secondary purchase of 26% at pro-rata of the ₹4,000 Cr headline = ceiling; target ₹850–950 Cr (bull-DCF pro-rata)','100% balance-sheet cash; no debt, no shares; equity-method associate','1 of 5 board seats + observer; info/audit rights; ROFR/ROFO; tag-along; anti-dilution; reserved matters'],BLUE)}
 {phase(2,'Partnership + ring-fence',['Multi-year custody/MPC agreement for tokenized-treasury, e₹ and cross-border pilots, at arm’s length','Standalone brand, independent chair, information barriers, published client charter','Founder and MPC-engineering retention pool vesting over validation'],CYAN)}
 {phase(3,'Call option on 74%',['Window months 12–24; a right, not an obligation; ROFR/ROFO persist after lapse','Cap ₹2,960 Cr = ₹1,650 Cr at exercise + earn-out ≤ ₹1,310 Cr, linear 55–100% retained ARR at month 18','Earn-out in Paytm shares (≤ 0.71 Cr, ±15% collar) or cash at Paytm’s election'],NAVY)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('Control consideration vs post-control churn (₹ Cr)', eo_chart+f'<p style="font-size:24px; color:{MUTED}">Tracks 74% × 18.2× × retained ARR within 1–2%: the upfront covers the worst case, the earn-out pays only for revenue that survives control. Measured on the pre-control client base, audited, Paytm-related revenue excluded.</p>','Chart',BLUE,'1.3')}
 <div style="flex:1; display:flex; flex-direction:column; gap:14px">
  {panel('Why 26%, not 25%', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">One share above 25% blocks special resolutions (new-investor allotment, charter changes, schemes). The veto does not stop a secondary sale; the ROFR/ROFO does. With the call option they close every route to the consortium.</p>','Key',NAVY)}
  {panel('Why Liminal’s shareholders say yes (TA)', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">₹1,040 Cr of liquidity now; a defined path to the full ₹4,000 Cr; Paytm as anchor client; retention pool; and the alternative buyer carries the same wallet conflict. If the option is refused: 26% + ROFR/ROFO without the call still blocks and still gives access.</p>','ThumbsUp',GREEN)}
 </div>
</div>'''
slide('architecture','Transaction architecture:','pay for access now, pay for control only against retained ARR',body,'The earn-out chart is the mechanism: green is full value, red is the floor. Fundamental value of 26% is ₹456–951 Cr, so the ₹1,040 Cr ceiling carries a disclosed premium.','Slide 5 · Transaction architecture')

# ---------------- SLIDE 6 ASSUMPTIONS ----------------
facts=[['Paytm (CF)','Value','Liminal / deal (CF)','Value'],
['Market cap','₹1,18,750 Cr','Headline value','₹4,000 Cr = ₹2,100 cash + ₹1,900 equity'],
['Diluted shares','64 Cr','ARR','₹220 Cr'],
['Cash / gross debt','₹8,900 / ₹350 Cr','PAT','~breakeven'],
['Revenue / EBITDA / PAT','₹8,450 / ₹640 / ₹480 Cr','Top-4 clients','60% of ARR'],
['Diluted EPS (start point)','₹7.50','Full-acquisition churn','30–45% of ARR within 12 months'],
['Rating','CRISIL AA− (Stable)','Capital drag at full ownership','₹750 Cr/yr recurring FCF'],
['Cash-portion funding','Cash, new debt, or mix','UPI MDR (Paytm standalone)','₹115 Cr/yr incremental net revenue']]
tas=[['#','Team assumption','Base','Range'],
['1','Stake / price','26% / ₹1,040 Cr (ceiling)','20–30%'],['2','Yield on surplus cash (pre-tax)','6.0%','5–7%'],['3','Cost of new debt (pre-tax)','8.5%','8–10%'],['4','Tax rate','25%','—'],
['5','Liminal ARR growth','20% (bear 10%, bull 30%)','10–40%'],['6','EBITDA margin','0% → +5 pp/yr to 25%','20–30%'],['7','PAT / FCF','PAT = 75% EBITDA; FCF ≈ PAT','—'],
['8','Churn under minority / JV','0% (consent gate)','0–20%'],['9','Churn at control','37.5% counterfactual; ≤20% to exercise','0–55%'],['10','Cost stickiness after churn','50% for one year','—'],
['11','Drag at minority','0 (RBI comfort CP); tested ₹195 / ₹750','—'],['12','Drag treatment','FCF only; PPA not modelled','—'],['13','MDR conversion','80% flow-through → ₹69 Cr PAT/FCF','60–100%'],
['14','One-time costs','Fees ₹15; integration ₹100','—'],['15','Synergies','₹0 base; upside only','—'],['16','WACC / terminal growth','12% / 5%','11–14%'],
['17','Control tranche','₹1,650 up (₹1,150 cash + ₹500 debt) + ≤₹1,310 earn-out','—'],['18','Guardrails','Cash ≥ ₹5,000; GD/EBITDA ≤ 1.5×; collar ±15%','—'],
['19','Validation / option window','12 months / months 12–24','—'],['20','Control gate on breakeven','PAT and FCF ≤ 5 yrs after exercise','—'],['21','Build-or-partner alternative','24–36 months','—']]
body=f'''
<div style="display:flex; gap:18px; flex:1">
 <div style="flex:1; display:flex; flex-direction:column; gap:14px">
  {panel('Case facts (CF)', table(facts,[24,26,24,26],size=24), 'Book', NAVY, 'none')}
  {panel('Derived calculations (CALC)', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Share price ₹1,855 (market cap ÷ shares) · 18.2× headline ARR · ₹1,900 Cr equity = 1.02 Cr shares · trailing P/E ≈ 247× · churn-adjusted multiples and values · drag ratios.</p>','Code',BLUE,'none')}
  {banner('CASE FACT ≠ DERIVED CALCULATION ≠ TEAM ASSUMPTION. No case input is replaced by an external figure; every TA is flexed in the model.')}
 </div>
 {panel('Team assumptions (TA) — the values in the model', table(tas,[6,38,38,18],size=24), 'Settings', BLUE, '1.15')}
</div>'''
slide('assumptions','Assumptions slide:','case facts vs calculations vs team assumptions',body,'This is the slide the Modeling Clarification asks for: 21 assumptions with values and ranges.','Slide 6 · Assumptions')

# ---------------- SLIDE 7 VALUATION ----------------
churn=[['Churn','ARR lost','Retained','Eff. multiple','Value @18.2×','Gap','Recovery growth'],
['0%','₹0','₹220','18.2×','₹4,000','—','—'],['30%','₹66','₹154','26.0×','₹2,800','₹1,200','+42.9%'],['37.5%','₹82.5','₹137.5','29.1×','₹2,500','₹1,500','+60.0%'],['45%','₹99','₹121','33.1×','₹2,200','₹1,800','+81.8%']]
dcf=bars([('10% bear',811),('20% base',1753),('30% bull',3658),('31.3% b/e',4000),('40%',7345)],h=200,colors=[MUTED,BLUE,BLUE,AMBER,GREEN],fmt=lambda v:f'₹{v:,}',w=60)
body=f'''
<div style="display:flex; gap:18px">
 {panel('Churn sensitivity (CALC) — ₹ Cr', table(churn,[12,13,13,15,16,14,17],size=24),'Chart',AMBER,'1.2')}
 {panel('What you need to believe — standalone DCF vs ₹4,000 Cr (TA: 12% WACC, 5% TG, margin → 25%)', dcf+f'<p style="font-size:24px; color:{MUTED}">Break-even growth <b>31.3% p.a. for 10 years</b> with zero churn and no drag. WACC 11–14% moves base value ₹2,127 → ₹1,265 Cr. Add the drag NPV (₹4,238 Cr) and 100% ownership is negative below 40% growth.</p>','Activity',BLUE,'1')}
</div>
<div style="display:flex; gap:18px; flex:1">
 {card('Is the valuation supportable?',['Not as an unconditional ₹4,000 Cr','Only as a cap reached through retained ARR: ₹3,127 Cr total at 30% churn, ₹2,690 Cr at 45%','If Liminal delivers 30% growth, the cap sits 16% below the then-DCF of ~₹4,756 Cr'],'Verified',BLUE)}
 {card('Churn tolerance (answer to 5.2)',['At the headline price, <b>any churn above 0%</b> makes the deal unattractive: the price is unsupported before churn','Under our structure the price self-corrects down to 55% retention','Below 55% retention (churn > 45%) control is <b>never</b> exercised'],'Warning',RED)}
 {card('Structuring response',['Deferred consideration · retention earn-out · CVR-style payout on retained ARR · valuation cap at headline','Fundamental value of 26%: ₹456 Cr (base) – ₹951 Cr (bull); the ₹1,040 Cr ceiling carries a disclosed premium for blocking and access','Do not pay ₹4,000 Cr unconditionally for revenue that may disappear because of the acquisition itself'],'Key',NAVY)}
</div>'''
slide('valuation','Valuation & churn:','18.2× becomes 26–33× and the price needs 31% growth for a decade',body,'The amber bar is the hinge: 31.3% growth for ten years with zero churn just to break even on price.','Slide 7 · Valuation & churn')

# ---------------- SLIDE 8 FINANCING ----------------
eps=bars([('Baseline',7.50),('Headline mix',5.29),('Debt + equity',4.69),('Mix 1,400/700',5.09),('All cash',4.04),('All equity',6.63),('Phase 1 (26%)',6.81)],h=190,maxv=8,colors=[NAVY,RED,RED,RED,RED,AMBER,GREEN],fmt=lambda v:f'₹{v:.2f}',w=56)
mix=[['Structure','New shares','Y1 EPS','vs ₹7.50','+MDR','Cash after','Gross debt','GD/EBITDA'],
['₹2,100 cash + ₹1,900 equity (case)','1.02 Cr','₹5.29','−29%','₹6.36','₹6,800','₹350','0.5×'],
['₹2,100 debt + ₹1,900 equity','1.02 Cr','₹4.69','−38%','₹5.75','₹8,900','₹2,450','3.8× ⚠'],
['₹1,400 cash + ₹700 debt + ₹1,900 eq.','1.02 Cr','₹5.09','−32%','₹6.15','₹7,500','₹1,050','1.6× ⚠'],
['All cash ₹4,000','—','₹4.04','−46%','₹5.12','₹4,900 ⚠','₹350','0.5×'],
['All equity ₹4,000','2.16 Cr','₹6.63','−12%','₹7.68','₹8,900','₹350','0.5×'],
['Share-count-only view of case mix','1.02 Cr','₹7.38','−1.6%','—','—','—','—']]
su=[['','Uses','Sources'],['Phase 1','26% stake ₹1,040 + fees ₹15 = ₹1,055','Balance-sheet cash ₹1,055; debt 0; equity 0'],['Control (if exercised)','Upfront ₹1,650 + integration ₹100 + earn-out ≤ ₹1,310','Cash ₹1,250 + new debt ₹500 + shares ≤ ₹1,310 (≤0.71 Cr, collared)'],['Maximum ever','₹4,000 Cr total = headline','Unconditional maximum ₹1,040 Cr']]
P1TXT=f'<ul style="font-size:24px; line-height:1.3; color:{BODY}; padding:0 0 0 24px"><li>Year-1 EPS <b>₹6.81 (−9.2% vs ₹7.50; −8.1% vs the ₹8.58 standalone-with-MDR baseline)</b>: entirely foregone treasury income (₹46.8 Cr/yr) less ₹2.6 Cr associate share. This is the option premium.</li><li>Sensitivity: ₹6.93 at 5% yield, ₹6.69 at 7%. With MDR added: ₹7.89.</li><li>Share-count dilution nil; new debt nil; cash after ₹7,860 Cr; GD/EBITDA 0.5×; net cash ₹7,510 Cr.</li></ul>'
body=f'''
<div style="display:flex; gap:18px">
 {panel('Full-acquisition year-1 EPS by financing mix (TA: 6% cash yield, 8.5% debt, 25% tax, 37.5% churn)', table(mix,[30,10,9,9,9,11,11,11],size=24),'Chart',RED,'1.45')}
 {panel('Year-1 EPS (₹/share)', eps, 'Activity', BLUE, '1')}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('Recommended Phase 1 — ₹1,040 Cr cash for 26%', P1TXT,'Verified',GREEN,'1')}
 {panel('Sources & uses (TA)', table(su,[22,39,39],size=24)+f'<p style="font-size:24px; color:{MUTED}">Post-control: cash ₹6,710 Cr, gross debt ₹850 Cr (1.3×), net cash ₹5,860 Cr — inside both guardrails. Cost of funds after control ₹130 Cr/yr.</p>','Database',NAVY,'1.2')}
</div>
{banner('How to read it: at ~247× P/E equity is Paytm’s cheapest currency in EPS terms and cash its most expensive (4.5% post-tax yield vs 0.4% earnings yield); but all-equity issues 3.3% of the company for a breakeven asset, and debt-funding the cash leg breaches AA− headroom (3.8× EBITDA). <b>No mix rescues a full acquisition. Financing follows risk resolution.</b>')}'''
slide('financing','Financing & EPS:','stage the capital, every full-deal mix is 12–46% dilutive',body,'The green bar is the recommended path; the only way to be near ₹7.50 is to not do the full deal.','Slide 8 · Financing & EPS')

# ---------------- SLIDE 9 BREAKEVEN ----------------
# EPS path line chart: full acquisition vs bull-control vs baseline, years 1-7
full=[5.29,6.16,6.34,6.59,6.92,7.11,7.35]; bull=[6.81,5.83,6.24,6.86,7.77,8.48,9.40]; base=[6.81,5.77,6.06,6.46,6.99,7.31,7.69]
W,H=760,300; x0,y0=40,20; ymin,ymax=4.0,10.0
def pts(vals):
    return ' '.join(f'{x0+i*(W-80)/6:.0f},{y0+(H-50)*(1-(v-ymin)/(ymax-ymin)):.0f}' for i,v in enumerate(vals))
svg=f'''<svg aria-label="Year-1 to year-7 EPS: full acquisition, control on bull trajectory, control on base trajectory, baseline 7.50" viewBox="0 0 {W} {H}" style="width:{W}px; height:{H}px"><line x1="{x0}" y1="{y0+(H-50)*(1-(7.5-ymin)/(ymax-ymin)):.0f}" x2="{W-40}" y2="{y0+(H-50)*(1-(7.5-ymin)/(ymax-ymin)):.0f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="8 6"/>
<polyline points="{pts(full)}" fill="none" stroke="{RED}" stroke-width="5"/><polyline points="{pts(base)}" fill="none" stroke="{AMBER}" stroke-width="5"/><polyline points="{pts(bull)}" fill="none" stroke="{GREEN}" stroke-width="5"/>
{''.join(f'<circle cx="{x0+i*(W-80)/6:.0f}" cy="{y0+(H-50)*(1-(v-ymin)/(ymax-ymin)):.0f}" r="7" fill="{GREEN}"/>' for i,v in enumerate(bull))}
{''.join(f'<circle cx="{x0+i*(W-80)/6:.0f}" cy="{y0+(H-50)*(1-(v-ymin)/(ymax-ymin)):.0f}" r="7" fill="{RED}"/>' for i,v in enumerate(full))}
</svg>'''
yrs=''.join(f'<p style="flex:1; font-size:24px; color:{BODY}; text-align:center">Y{i+1}</p>' for i in range(7))
legend=f'<div style="display:flex; gap:22px; align-items:center"><x-shape kind="rounded" style="width:28px; height:8px; background:{GREEN}"></x-shape><p style="font-size:24px; color:{BODY}">Control end-Y1, bull 30%</p><x-shape kind="rounded" style="width:28px; height:8px; background:{AMBER}"></x-shape><p style="font-size:24px; color:{BODY}">Control end-Y1, base 20%</p><x-shape kind="rounded" style="width:28px; height:8px; background:{RED}"></x-shape><p style="font-size:24px; color:{BODY}">Full acquisition today</p><x-shape kind="rounded" style="width:28px; height:8px; background:{MUTED}"></x-shape><p style="font-size:24px; color:{BODY}">₹7.50 baseline</p></div>'
be=[['Path','Y1 EPS','PAT breakeven','FCF breakeven','Read-across'],
['Full acquisition today (case mix)','₹5.29','Year 8 (Y3 only if MDR credited)','Never in 10 yrs; Y1 FCF −₹986 Cr','Even 0% churn + 30% growth + MDR: no FCF b/e'],
['Phase 1: 26% minority','₹6.81','Associate income covers interest Y9 base / Y6 bull','No cash yield until dividends or exit','Cost ₹47 Cr/yr; pro-rata drag would make it ₹242 Cr'],
['Control end-Y1, base 20%','₹5.77 trough','Year 7','Year 7','Fails ≤5-yr gate → Hold'],
['Control end-Y1, bull 30%','₹5.83 → ₹7.77 (Y5)','Year 5','Year 5','Passes → Exercise (Y6 with 20% churn)']]
mdr=hbars([('Drag ₹750 Cr',750),('MDR gross ₹115 Cr',115),('MDR after PAT/FCF conv.',69)],colors=[RED,BLUE,CYAN],fmt=lambda v:f'₹{v:g}',trackw=300)
body=f'''
<div style="display:flex; gap:18px">
 {panel('EPS path by route (₹/share, TA base)', svg+f'<div style="display:flex; padding:0 40px">{yrs}</div>'+legend,'Activity',BLUE,'1.15')}
 <div style="flex:1; display:flex; flex-direction:column; gap:14px">
  {panel('₹750 Cr drag vs ₹115 Cr MDR (answer to 5.3)', mdr+f'<p style="font-size:24px; line-height:1.3; color:{BODY}">MDR covers <b>15.3%</b> of the drag at the revenue line, <b>9.2%</b> after conversion. Net cash cost of full ownership ~₹681 Cr/yr. The MDR accrues whether or not Paytm buys Liminal: a standalone tailwind (+₹1.08 EPS), never a deal synergy.</p>','Chart',RED)}
  {banner('Two tests, both required: PAT test (accounting) and FCF test (cash, after drag). Even a ₹100 Cr/yr recurring capital cost fails the 5-year FCF gate in every trajectory; ₹50 Cr passes only in bull with zero churn.')}
 </div>
</div>
{panel('Breakeven results (TA base: 20% growth, margin ramp; 37.5% churn in the full-acquisition counterfactual)', table(be,[24,13,21,21,21],size=24),'Verified',NAVY,'none')}'''
slide('breakeven','PAT & FCF breakeven:','the full deal never gets there; control breaks even only if Liminal earns it',body,'Green line crosses the dashed baseline in year 5: that is the only route that passes both gates. Red never does on cash.','Slide 9 · PAT & FCF breakeven')

# ---------------- SLIDE 10 GOVERNANCE ----------------
# donut: 60% top-4
r=80; C=2*3.14159*r
donut=f'''<div style="position:relative; width:220px; height:220px; align-self:center"><svg aria-label="Top-4 clients are 60% of ARR" viewBox="0 0 220 220" style="width:220px; height:220px"><circle cx="110" cy="110" r="{r}" fill="none" stroke="{TINT}" stroke-width="40"/><circle cx="110" cy="110" r="{r}" fill="none" stroke="{BLUE}" stroke-width="40" stroke-dasharray="{C*0.6:.0f} {C:.0f}" transform="rotate(-90 110 110)"/></svg><p style="position:absolute; left:0px; top:78px; width:220px; text-align:center; font-family:{HF}; font-size:40px; font-weight:700; color:{NAVY}">60%</p><p style="position:absolute; left:0px; top:126px; width:220px; text-align:center; font-size:24px; color:{MUTED}">top-4 of ARR</p></div>'''
gov=[('Standalone brand & entity','No Paytm branding or shared front-ends','Home'),('Arm’s-length board','Independent chair; Paytm 1 of 5 (2 of 7 on control); reserved matters exclude custody ops','Users'),('Information barriers','No client data to Paytm; MPC key shares never on Paytm infrastructure; segregated desk','Lock'),('Independent compliance & cyber','CCO/CISO report to Liminal risk committee; annual attestation shared with clients','Verified'),('Neutral service standards','Published client charter: no preferential pricing, routing or SLAs','Star'),('Client-protection framework','Change-of-control consent rights, data portability, top-4 soundings, named owners','Trust'),('Retention-linked consideration','Earn-out and management pool scale with retained ARR: ₹291 Cr per 10 pts','Chart'),('Founder & engineer retention','Mahin Gupta and MPC core on vesting economics through validation','Key')]
govgrid=f'<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px">'+''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:{CARD}; border:1px solid {LINE}; border-radius:12px; padding:12px 14px"><div style="display:flex; align-items:center; gap:10px"><div style="display:flex; align-items:center; justify-content:center; width:40px; height:40px; background:{BLUE}; border-radius:20px"><x-icon name="{ic}" style="width:22px; height:22px; color:#FFFFFF"></x-icon></div>{numbox(i+1,NAVY)}</div><h3 style="font-size:24px; font-weight:700; color:{NAVY}; line-height:1.15">{t}</h3><p style="font-size:24px; line-height:1.25; color:{BODY}">{d}</p></div>' for i,(t,d,ic) in enumerate(gov))+'</div>'
CONC=f'''<div style="display:flex; gap:18px; align-items:center">{donut}<div style="display:flex; flex-direction:column; gap:8px"><p style="font-size:24px; line-height:1.3; color:{BODY}"><b>HDFC Bank + Axis Bank + CoinDCX + ZebPay = ₹132 Cr</b> of ₹220 Cr ARR.</p><p style="font-size:24px; line-height:1.3; color:{BODY}">Case churn ₹66–99 Cr = <b>50–75% of the top-4 book</b>.</p><p style="font-size:24px; line-height:1.3; color:{BODY}">Revolt trigger: a competing wallet operator seeing custody flows.</p></div></div>'''
body=f'''
<div style="display:flex; gap:18px">
 {panel('Concentration risk (CF → CALC)', CONC,'Users',RED,'1')}
 {panel('How significant is the risk?', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Under full control, <b>existential</b>: the case removes half to three-quarters of top-4 revenue. Under the ring-fenced minority, <b>manageable</b>: no change of control occurs, contracts are unaffected, and the consent process tells the Board in advance what control would cost. Governance converts a 30–45% churn assumption into a ≤20% consent gate — and the earn-out pays sellers to protect the same clients.</p>','Warning',AMBER,'1.2')}
</div>
{govgrid}
{banner('Governance is not cosmetic: it is the valuation-protection mechanism, and it is designed to be audited by clients, not just described to them.')}'''
slide('governance','Customer retention & governance:','independence clients can verify',body,'Eight mechanisms, each with an owner; number seven is the one that aligns sellers with retention.','Slide 10 · Retention & governance')

# ---------------- SLIDE 11 REGULATORY ----------------
def lane(title, sub, items, color):
    return f'''<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{CARD}; border:1px solid {LINE}; border-top:8px solid {color}; border-radius:14px; padding:14px 16px">
<h3 style="font-size:26px; font-weight:700; color:{NAVY}">{title}</h3><p style="font-size:24px; color:{color}; font-weight:600">{sub}</p>
<ul style="font-size:24px; line-height:1.3; color:{BODY}; padding:0 0 0 24px">{''.join(f'<li>{i}</li>' for i in items)}</ul></div>'''
body=f'''
<div style="display:flex; gap:14px">
 {lane('Before signing','Phase 1 · indicative 8–12 weeks (TA)',['RBI consultation: PA-licence holder at 26% of a custody provider; capital treatment at minority vs control. <b>Signing condition: written comfort that no bank-like reserve applies at 26%</b>','Diligence: AML programme and FIU-IND standing; data protection and key-material localisation; ISO 27001 / SOC 2 evidence; client change-of-control clauses','Top-4 soundings under NDA; competition and securities notifiability analysis'],BLUE)}
 {lane('Signing → closing','Phase 1 conditions precedent',['RBI comfort letter','No material adverse regulatory change on either side','Key-client consents where contracts bite at minority level','FIU-IND registration in good standing; clean cyber audit','Stock-exchange disclosure on signing'],CYAN)}
 {lane('At control exercise','Phase 3 · indicative 4–6 months (TA)',['RBI change-in-control approval','Competition clearance','SEBI/exchange approvals for share-settled earn-out (preferential-issue rules, shareholder resolution)','Client change-of-control consents (Gate 1)','Refreshed AML/cyber audit'],NAVY)}
 {lane('Post-close','All phases',['Standalone compliance framework','AML transaction monitoring and reporting','Segregated data and key infrastructure','Continuous cyber monitoring and incident reporting','Independent compliance reporting to both boards’ risk committees'],GREEN)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('Does owning custody create additional requirements?', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Yes, per the case: bank-like reserves against custodied assets at full ownership (₹750 Cr/yr). Our design keeps the custody licence, the custodied assets and any reserves inside Liminal, and keeps Paytm at negative control until the treatment is written down.</p>','Lock',NAVY)}
 {panel('The one question that decides the deal', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Does minority ownership avoid, reduce or still trigger the ₹750 Cr requirement? The case does not say. Slide 9 shows why it decides everything: even a <b>₹100 Cr/yr</b> recurring cost defeats the five-year FCF gate in every trajectory.</p>','Warning',RED)}
 {panel('Hard decision gate', f'<p style="font-size:24px; line-height:1.35; color:{BODY}"><b>No control without written regulatory capital treatment incorporated into the FCF model.</b> If a reserve applies at minority level, Phase 1 is restructured toward the JV/licence path before signing.</p>','Verified',GREEN)}
</div>'''
slide('regulatory','Regulatory & closing architecture:','answer the capital question in writing before control',body,'Four lanes, left to right in time. The signing condition in lane one is the single most important line on the slide.','Slide 11 · Regulatory path')

# ---------------- SLIDE 12 COMPETITIVE & DOWNSIDE ----------------
mx=[['Consents / churn ↓  ·  Capital drag →','None / structured away','Pro-rata at 26% (≈₹195 Cr)','Full ₹750 Cr at any ownership'],
['≥80% consents (churn ≤20%)','EXERCISE if bull trajectory and cap hold','Hold; JV/licence for capability','Hold 26% only if drag-free, else restructure/exit'],
['55–80% (churn 20–45%)','HOLD; earn-out floor protects; re-test m24','Hold or restructure to JV','Restructure or exit'],
['<55% (churn >45%)','NO CONTROL; remediation ladder','Exit','Exit']]
body=f'''
<div style="display:flex; gap:18px">
 {card('PhonePe–Mastercard threat (CF)',['Exploratory consortium if Paytm walks; no competing price, terms, synergies or certainty in the case','If they win: they get the rail + Mastercard cross-border; Paytm builds or partners elsewhere (24–36 mo, TA)','They inherit the same wallet conflict, price and capital question; Mastercard’s bank ties are their one real edge'],'Globe',NAVY)}
 {card('Paytm’s response',['Reservation value: total ≤ ₹4,000 Cr, ≤ ₹1,040 Cr unconditional, no tranche above 18.2× retained ARR, no control at a drag that defeats 5-yr FCF breakeven','<b>If outbid on unconditional terms: let them</b> — that is the winner’s curse the case describes','Fallback: alternative custodian partnership; redeploy toward buybacks and organic e₹ build'],'Trust',BLUE)}
 {card('If Paytm’s multiple compresses',['Phase 1 is cash: independent of the stock','A 25% price fall lifts the ₹1,900 Cr equity leg from 1.02 to 1.37 Cr shares — still ~2%; the real risk is the narrative of a −29% print at ~247× P/E','Answer: no unconditional equity, ±15% collar, cash-settle election; the unconditional cheque is 0.9% of market cap'],'Chart',AMBER)}
</div>
<div style="display:flex; gap:18px; flex:1">
 {panel('Downside matrix — how the recommendation changes', table(mx,[28,24,24,24],size=24),'Settings',BLUE,'1.35')}
 {panel('Remediation & unwind ladder if churn or consents breach 45%', numrow('30d','Independent cause review; CEO outreach to each top-4 client; Paytm director steps back to observer',AMBER)+numrow('90d','Governance reset; published barrier attestation; fee holidays / SLA guarantees funded from the sellers’ earn-out at risk',AMBER)+numrow('180d','Still <55% retention: no exercise; ROFO/tag process to a neutral buyer, or convert to licence + warrants. Sunk cost never justifies escalation',RED),'Warning',RED,'1')}
</div>
{banner('Competitive pressure may change timing; it must not change valuation discipline.')}'''
slide('downside','Competitive & downside response:','set the walk-away line now, let the structure absorb the rest',body,'The matrix answers the Mission’s “show how your recommendation changes”: capital treatment decides the column, consents decide the row.','Slide 12 · Competitive & downside')

# ---------------- SLIDE 13 ROADMAP ----------------
def ph(n,title,when,items,color):
    return f'''<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:14px 16px">
<div style="display:flex; align-items:center; gap:10px">{numbox(n,color)}<div style="display:flex; flex-direction:column"><h3 style="font-size:26px; font-weight:700; color:{NAVY}">{title}</h3><p style="font-size:24px; color:{color}; font-weight:600">{when}</p></div></div>
<ul style="font-size:24px; line-height:1.3; color:{BODY}; padding:0 0 0 24px">{''.join(f'<li>{i}</li>' for i in items)}</ul></div>'''
gates=[['Gate','Threshold to exercise control'],['1 · Client consents','≥80% of ARR consents in writing to Paytm control under the ring-fence; implied churn ≤20%'],['2 · Regulatory capital','Written RBI treatment; recurring cost nil or structured away (₹50 Cr passes only in bull/0% churn; ₹100 Cr fails every case)'],['3 · Valuation','Control price ≤ ₹2,960 Cr and ≤ 18.2× retained ARR; total ≤ ₹4,000 Cr'],['4 · PAT','Consolidated PAT breakeven ≤5 yrs after exercise on the Board model (bull passes; base does not)'],['5 · FCF','Consolidated FCF breakeven ≤5 yrs after confirmed capital cost; cash ≥ ₹5,000 Cr; GD/EBITDA ≤ 1.5×'],['6 · Compliance','Clean AML/cyber/data audit; ISO 27001 and SOC 2 maintained; no unresolved regulatory matter']]
tl=f'''<div style="display:flex; align-items:center; gap:0">
<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:6px"><div style="height:16px; background:{BLUE}; border-radius:8px"></div><p style="font-size:24px; font-weight:600; color:{BLUE}">Months 0–3 · INVEST</p></div>
<div style="flex:3; display:flex; flex-direction:column; align-items:center; gap:6px"><div style="height:16px; background:{CYAN}; border-radius:8px"></div><p style="font-size:24px; font-weight:600; color:{CYAN}">Months 3–12 · VALIDATE</p></div>
<div style="flex:4; display:flex; flex-direction:column; align-items:center; gap:6px"><div style="height:16px; background:{NAVY}; border-radius:8px"></div><p style="font-size:24px; font-weight:600; color:{NAVY}">Months 12–24 · DECIDE: Exercise / Hold / Walk away</p></div></div>'''
body=f'''
{tl}
<div style="display:flex; gap:18px; flex:1">
 <div style="flex:1; display:flex; flex-direction:column; gap:12px">
  {ph(1,'Invest','Months 0–3',['Close 26% for ≤ ₹1,040 Cr; partnership live; ring-fence installed','Option, earn-out, ROFR/ROFO documented; RBI comfort obtained','Retention pool in place; Board model with quarterly gate reporting'],BLUE)}
  {ph(2,'Validate','Months 3–12',['Customers: retention, top-4 renewals, written consents to control','Regulation: written capital treatment; approval path; AML standing','Financials: month-12 ARR ≥ ₹286 Cr = bull, ~₹264 Cr = base; margins; cash; MDR tracked separately','Risk: cyber, AML, data segregation, barrier attestation'],CYAN)}
 </div>
 {panel('Phase 3 · Decide — six quantified gates', table(gates,[24,76],size=24)+f'<p style="font-size:24px; line-height:1.3; color:{BODY}"><b>EXERCISE</b> all six clear · <b>HOLD</b> any gate open: Liminal can remain an arm’s-length associate indefinitely, and after control an arm’s-length subsidiary · <b>WALK AWAY / UNWIND</b> churn >45%, drag defeats returns, top-4 reject ownership, regulatory deterioration, price above reservation value — including after signing where CPs and termination rights allow.</p>','Verified',NAVY,'1.6')}
</div>
{banner('FINAL BOARD MESSAGE — Paytm should not pay today for risks it can observe tomorrow. Secure the infrastructure through a 26% stake and a partnership; preserve the right, not the obligation, to acquire control; commit the remaining ₹2,960 Cr only after client trust, capital treatment, valuation and cash flow are proven. <b>Strategic access now. Control only when value is protected.</b>',NAVY)}'''
slide('roadmap','Implementation roadmap & decision gates:','Invest → Validate → Exercise / Hold / Walk away',body,'Close on the six gates and the final message. Each gate is auditable by the committee with the model.','Slide 13 · Roadmap & gates')

# ---------------- APPENDIX A ----------------
ten=[['Yr','Lim rev','Lim PAT','Incr PAT','EPS','EPS+MDR','Incr FCF','Cum FCF'],[1,165,-41,-136,'5.29','6.36',-986,'−3,086'],[2,198,15,-80,'6.16','7.22',-830,'−3,915'],[3,238,27,-68,'6.34','7.40',-818,'−4,733'],[4,285,43,-52,'6.59','7.65',-802,'−5,535'],[5,342,64,-30,'6.92','7.98',-780,'−6,315'],[6,411,77,-18,'7.11','8.17',-768,'−7,083'],[7,493,92,-2,'7.35','8.41',-752,'−7,835'],[8,591,111,16,'7.63','8.69',-734,'−8,569'],[9,709,133,39,'7.97','9.04',-711,'−9,280'],[10,851,160,65,'8.38','9.44',-685,'−9,965']]
ten=[[str(c) for c in r] for r in ten]
# waterfall as hbars-like steps
wf=f'''<div style="display:flex; flex-direction:column; gap:10px">
{numrow('₹7.50','Baseline diluted EPS (CF)',NAVY)}{numrow('−0.12','New shares: 1.02 Cr at ₹1,855 (the “mechanical” ₹7.38)',AMBER)}{numrow('−1.45','Foregone post-tax interest on ₹2,100 Cr cash (₹94.5 Cr, TA 6% yield)',RED)}{numrow('−0.63','Post-churn Liminal loss ₹41 Cr, no group relief (TA)',RED)}{numrow('₹5.29','Year-1 EPS, headline mix, 37.5% churn (−29%)',RED)}{numrow('+1.08','Standalone MDR ₹69 Cr PAT — shown beside, never inside, the deal',BLUE)}
</div><p style="font-size:24px; color:{MUTED}">Phase 1: ₹7.50 → −₹0.73 foregone interest → +₹0.04 associate share → ₹6.81. Not modelled: PPA amortisation; one-time integration ₹100 Cr (in FCF).</p>'''
body=f'''
<div style="display:flex; gap:18px; flex:1">
 {panel('A4 · EPS / dilution bridge (year 1, full acquisition)', wf,'Chart',RED,'1')}
 {panel('A5 · 10-year PAT & FCF table (full acquisition, case mix, 20% growth, 37.5% churn)', table(ten,[7,12,12,13,11,13,15,17],size=24)+f'<p style="font-size:24px; color:{MUTED}">PAT breakeven year 8; FCF never (₹750 drag + ₹94.5 cost of funds exceed Liminal FCF every year). Cumulative includes ₹2,100 Cr outlay and ₹100 Cr integration.</p>','Database',NAVY,'1.25')}
</div>'''
slide('appx-a','Appendix A4–A5:','EPS bridge and the 10-year breakeven table',body,'Backup for the finance panel; the bridge shows where the blueprint’s 1.6% went.','Appendix')

# ---------------- APPENDIX B ----------------
risk=[['Risk','Transaction response'],['30–45% full-control churn','Minority first; control only on ≥80% consents; earn-out with 55% floor'],['60% top-client concentration','Standalone governance, barriers, client charter, soundings, named owners'],['₹750 Cr annual capital drag','Written RBI treatment as CP; capital gate before control; JV/licence fallback'],['18.2× headline valuation','Retained-value pricing; cap ₹4,000 Cr; ₹1,040 Cr unconditional max; target ₹850–950 Cr'],['EPS dilution / shareholder pressure','No Phase-1 issuance; option premium disclosed (−9%); no unconditional −29% print'],['Rating / leverage','No Phase-1 debt; ≤₹500 Cr at control; GD/EBITDA ≤1.5×; cash ≥₹5,000 Cr'],['PhonePe–Mastercard counter-bid','ROFR/ROFO + 26% veto + call option; reservation value; walk-away discipline'],['Paytm stock compression','Cash Phase 1; ±15% collar; cash-settle election; no fixed-value issuance'],['AML / data / cyber','Independent compliance; segregated keys and data; annual attestation'],['Founder / talent flight','Retention pool vesting over validation; founder rollover and nomination rights'],['Churn >45%','No exercise; remediation ladder; exit via ROFO/tag'],['Regulatory deterioration','Conditions precedent; termination rights; suspend exercise'],['Weak PAT / FCF','Five-year breakeven gates; no capital escalation on sunk cost']]
def node(text,color=BLUE):
    return f'<div style="display:flex; align-items:center; justify-content:center; background:{color}; border-radius:12px; padding:12px 16px"><p style="font-size:24px; font-weight:600; color:#FFFFFF; text-align:center; line-height:1.2">{text}</p></div>'
def leaf(text,color=GREEN):
    return f'<div style="display:flex; align-items:center; gap:8px; background:{CARD}; border:2px solid {color}; border-radius:10px; padding:8px 12px"><p style="font-size:24px; font-weight:600; color:{color}; line-height:1.2">{text}</p></div>'
down=f'<div style="display:flex; justify-content:center"><x-shape kind="arrow-down" style="width:24px; height:40px; background:{MUTED}"></x-shape></div>'
tree=f'''<div style="display:flex; flex-direction:column; gap:6px">
{node('1 · Is Liminal strategically valuable to Paytm?',NAVY)}<div style="display:flex; gap:12px; justify-content:center">{leaf('YES → continue')}{leaf('NO → walk away',RED)}</div>{down}
{node('2 · Can Paytm secure access without full control?',NAVY)}<div style="display:flex; gap:12px; justify-content:center">{leaf('YES → 26% + partnership + option')}</div>{down}
{node('3 · After validation: consents ≥80% and capital treatment compatible with 5-yr FCF breakeven?',BLUE)}<div style="display:flex; gap:12px; justify-content:center">{leaf('YES → test gates 3–6')}{leaf('NO → hold, restructure to JV, or exit',AMBER)}</div>{down}
{node('4 · Does control clear valuation, PAT, FCF and compliance gates?',BLUE)}<div style="display:flex; gap:12px; justify-content:center">{leaf('YES → exercise call option')}{leaf('NO → hold minority',AMBER)}</div>
<p style="font-size:24px; color:{MUTED}; text-align:center">End state: control is an earned option, not a day-one commitment.</p></div>'''
body=f'''
<div style="display:flex; gap:18px; flex:1">
 {panel('A7 · Risk register & mitigants', table(risk,[34,66],size=24),'Warning',RED,'1.3')}
 {panel('A8 · Board decision tree', tree,'Verified',NAVY,'1')}
</div>'''
slide('appx-b','Appendix A7–A8:','risk register and board decision tree',body,'Every risk has a structural response, not a hope.','Appendix')

# ---------------- APPENDIX C ----------------
lim=[['Yr','ARR','EBITDA m','EBITDA','PAT','26% share','Foregone int.','Net EPS'],['0','220','0%','0','0','0','0','0'],['1','264','5%','13','10','2.6','46.8','−0.69'],['2','317','10%','32','24','6.2','46.8','−0.63'],['3','380','15%','57','43','11.1','46.8','−0.56'],['4','456','20%','91','68','17.8','46.8','−0.45'],['5','547','25%','137','103','26.7','46.8','−0.31'],['6','657','25%','164','123','32.0','46.8','−0.23']]
irr=[['Growth ↓ · exit multiple →','6×','10×','14×','18.2×'],['10%','−11.9%','−2.4%','4.4%','10.0%'],['20% (base)','−3.9%','6.5%','13.9%','20.0%'],['30% (bull)','4.1%','15.3%','23.4%','30.0%']]
cov=[['Case ask','Where answered'],['5.1 Strategic verdict','Slides 1, 2, 4'],['5.2 Churn defence','Slides 3, 7 (tolerance), 10'],['5.3 Capital & valuation','Slides 7, 8, 9; A4, A5'],['5.4 Regulatory path','Slide 11'],['5.5 Competitive risk','Slide 12'],['5.6 Contingency','Slides 12, 13; A8'],['Modeling Clarification','Slide 6 (assumptions), Slide 9 (PAT + FCF), model']]
body=f'''
<div style="display:flex; gap:18px; flex:1">
 <div style="flex:1.2; display:flex; flex-direction:column; gap:14px">
  {panel('A6 · Liminal base case (TA) and Phase-1 EPS effect (₹ Cr)', table(lim,[7,11,13,12,11,15,17,14],size=24),'Chart',BLUE,'none')}
  {panel('A6 · Phase-1 stake IRR — exit end-Y5 at multiple × ARR₅, 26% stake, no dividends', table(irr,[32,17,17,17,17],size=24)+f'<p style="font-size:24px; color:{MUTED}">Against a 12% hurdle the stake earns its cost of capital at ≥20% growth and ≥13× exit, or ≥30% growth and ≥9×. Fundamental value of 26%: ₹456 Cr (base) – ₹951 Cr (bull) vs the ₹1,040 Cr ceiling.</p>','Activity',GREEN,'none')}
 </div>
 <div style="flex:0.8; display:flex; flex-direction:column; gap:14px">
  {panel('A9 · Case-question coverage map', table(cov,[42,58],size=24),'Book',NAVY,'none')}
  {panel('A1 · Model', f'<p style="font-size:24px; line-height:1.35; color:{BODY}">Transparent accretion/dilution and transaction model (Python, 17 sections) reprints every figure in this deck: churn sensitivity, drag context, standalone DCF, financing-mix EPS, 10-year PAT/FCF, Phase-1 returns, earn-out schedule, control gate checks, guardrails, downside matrix, sources and uses.</p>','Code',BLUE,'none')}
 </div>
</div>'''
slide('appx-c','Appendix A6, A9:','Liminal base case, Phase-1 returns and coverage map',body,'Use the IRR grid if asked what you need to believe for the minority alone.','Appendix')

deck={"v":4,"createdOnFiles":{"v":1,"at":"2026-09-24T09:00:00Z"},"title":"Project Satoshi Gate","order":order,
"sections":{"s1":{"description":"The recommendation and why full control fails on the case's own numbers","start":"cover"},
"s2":{"description":"The staged structure, its assumptions, valuation and financing","start":"architecture"},
"s3":{"description":"Breakeven, retention, regulation, downside and the roadmap","start":"breakeven"},
"s4":{"description":"Appendix: bridges, tables, risks, returns","start":"appx-a"}},
"faces":{"poppins":{"family":"Poppins","href":"https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap"},"inter":{"family":"Inter","href":"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"}},
"designSystems":[]}
json.dump(deck,open(os.path.join(ROOT,'project','deck.json'),'w'),indent=1)
print(len(order),'slides written')
