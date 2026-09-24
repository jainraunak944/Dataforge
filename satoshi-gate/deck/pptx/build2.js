const pptxgen = require('pptxgenjs');
const P = new pptxgen(); P.layout='LAYOUT_WIDE'; P.author='Team ETERNAL'; P.title='Project Satoshi Gate';
const NAVY='0B2A5B', BLUE='1F5FBF', SKY='2F80ED', LIGHT='DCE8FA', PALE='EEF3FB', INK='1A2433', BODY='333D4D', MUTED='6A7383', LINE='BFC9DA', GREY='F3F5F9', WHITE='FFFFFF', RED='B23A3A', GREEN='1F7A45', AMBER='C2790F';
const HF='Cambria', BF='Calibri';
const SECTIONS=['RECOMMENDATION','RATIONALE','STRUCTURE','FINANCIALS','RISK & GOVERNANCE','ROADMAP','APPENDIX'];
let n=0;
const R=(str,base={})=>str.split('**').map((t,i)=>({text:t,options:{...base,bold:i%2===1||base.bold}})).filter(p=>p.text!=='');
function T(s,x,y,w,h,str,o={}){ const {fs=11,color=BODY,bold=false,align='left',valign='top',font=BF,italic=false,fill}=o; const opt={x,y,w,h,fontFace:font,fontSize:fs,color,align,valign,margin:0,isTextBox:true,italic}; if(fill) opt.fill={color:fill}; s.addText(typeof str==='string'?R(str,{bold}):str,opt); }
function rect(s,x,y,w,h,fill,line=null,lw=0.75){ s.addShape(P.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:line?{color:line,width:lw}:{color:fill,width:0}}); }
function hline(s,x,y,w,color=LINE,pt=0.75){ s.addShape(P.ShapeType.line,{x,y,w,h:0,line:{color,width:pt}}); }
function footer(s,sec){
  rect(s,0,6.72,13.33,0.78,GREY); rect(s,0,6.72,13.33,0.05,NAVY); rect(s,0,6.79,13.33,0.03,SKY);
  const labels=SECTIONS; let x=0.45; const widths=[1.85,1.35,1.4,1.45,2.25,1.25,1.3];
  labels.forEach((l,i)=>{ const w=widths[i]; if(l===sec) rect(s,x-0.08,6.95,w-0.1,0.4,LIGHT); T(s,x,6.95,w-0.1,0.4,l,{fs:11,bold:true,color:NAVY,valign:'middle',align:'center'}); x+=w; });
  rect(s,12.2,6.9,0.03,0.5,NAVY); T(s,12.3,6.85,0.9,0.6,String(n),{fs:22,bold:true,color:NAVY,valign:'middle',font:HF});
}
function slide(sec,title,tagline){ const s=P.addSlide(); n++; s.background={color:WHITE};
  T(s,0.45,0.3,12.4,0.5,title,{fs:24,bold:true,color:NAVY,font:HF,valign:'middle'});
  T(s,0.45,0.8,12.4,0.35,tagline,{fs:13,color:BLUE,italic:true,valign:'middle'});
  hline(s,0.45,1.2,12.43,NAVY,1.5); footer(s,sec); return s; }
function hdr(s,x,y,w,text,color=NAVY){ rect(s,x,y,w,0.34,color); T(s,x+0.12,y,w-0.2,0.34,text,{fs:11,bold:true,color:WHITE,valign:'middle'}); }
function panel(s,x,y,w,h,title,color=NAVY){ rect(s,x,y,w,h,WHITE,LINE); hdr(s,x,y,w,title,color); }
function bullets(s,x,y,w,h,items,fs=10.5,gap=4,color=BODY){ const paras=[]; items.forEach((it,i)=>{ const r=R(it); r[0].options.bullet={indent:10}; r[0].options.paraSpaceAfter=gap; r[r.length-1].options.breakLine=i<items.length-1; paras.push(...r); }); s.addText(paras,{x,y,w,h,fontFace:BF,fontSize:fs,color,valign:'top',margin:0,isTextBox:true}); }
function numrows(s,x,y,w,items,rowh=0.5,fs=10.5,color=BLUE){ items.forEach((it,i)=>{ const yy=y+i*(rowh+0.08); rect(s,x,yy,w,rowh,PALE); rect(s,x,yy,0.42,rowh,color); T(s,x,yy,0.42,rowh,String(i+1),{fs:12,bold:true,color:WHITE,align:'center',valign:'middle',font:HF}); T(s,x+0.55,yy,w-0.65,rowh,it,{fs,valign:'middle'}); }); }
function stat(s,x,y,w,h,value,label,color=NAVY,sub=null){ rect(s,x,y,w,h,WHITE,LINE); rect(s,x,y,w,0.06,color); T(s,x+0.12,y+0.12,w-0.24,0.5,value,{fs:22,bold:true,color,font:HF,valign:'middle'}); T(s,x+0.12,y+0.62,w-0.24,h-0.66,label,{fs:10,color:BODY}); }
function chips(s,x,y,w,items,h=0.42,fs=10.5,fill=PALE,color=NAVY,gap=0.12){ const cw=(w-gap*(items.length-1))/items.length; items.forEach((it,i)=>{ rect(s,x+i*(cw+gap),y,cw,h,fill,LINE); T(s,x+i*(cw+gap),y,cw,h,it,{fs,bold:true,color,align:'center',valign:'middle'}); }); }
function chevrons(s,x,y,w,h,items,colors){ const cw=w/items.length; items.forEach((it,i)=>{ s.addShape(i===0?P.ShapeType.homePlate:P.ShapeType.chevron,{x:x+i*cw,y,w:cw+0.02,h,fill:{color:colors[i]},line:{color:WHITE,width:1}}); T(s,x+i*cw+(i?0.3:0.12),y,cw-0.45,h,it,{fs:10.5,bold:true,color:WHITE,align:'center',valign:'middle'}); }); }
function tbl(s,x,y,w,rows,colW,fs=10,rowH=null,opts={}){ if(colW.length===2&&colW[1]===0){ colW=[100]; rows=rows.map(r=>[r[0]]); } const tw=colW.reduce((a,b)=>a+b,0); const cw=colW.map(c=>c/tw*w); const {firstBold=true,align='center'}=opts;
  const data=rows.map((r,i)=>r.map((c,j)=>({text:String(c).replace(/\*\*/g,''),options:{bold:i===0||(j===0&&firstBold)||/\*\*/.test(String(c)),color:i===0?WHITE:INK,fill:{color:i===0?NAVY:(i%2===0?PALE:WHITE)},align:j===0?'left':align,valign:'middle',fontFace:BF,fontSize:fs,margin:[3,5,3,5]}})));
  const o={x,y,w,colW:cw,border:{type:'solid',color:LINE,pt:0.5},autoPage:false}; if(rowH) o.rowH=rowH; s.addTable(data,o); }
function bar(s,x,y,w,h,labels,values,colors,fmt,extra={}){ s.addChart(P.ChartType.bar,[{name:'v',labels,values}],{x,y,w,h,barDir:'col',chartColors:colors,showValue:true,dataLabelPosition:'outEnd',dataLabelFontSize:9,dataLabelFontBold:true,dataLabelColor:INK,dataLabelFormatCode:fmt,catAxisLabelFontSize:9,catAxisLabelColor:BODY,valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},showLegend:false,barGapWidthPct:50,valAxisMinVal:0,...extra}); }
function note(s,x,y,w,h,label,text,fill=NAVY){ rect(s,x,y,w,h,fill); T(s,x+0.15,y,1.6,h,label,{fs:10.5,bold:true,color:'BFD3F5',valign:'middle'}); T(s,x+1.75,y,w-1.9,h,text,{fs:11,color:WHITE,valign:'middle'}); }

// ===== TITLE =====
{ const s=P.addSlide(); n++; s.background={color:WHITE};
  rect(s,0,0,13.33,0.12,NAVY); rect(s,0,0.12,13.33,0.05,SKY);
  rect(s,0.45,1.7,0.1,3.0,NAVY);
  T(s,0.8,1.6,8,0.4,'PAYTM  ×  LIMINAL CUSTODY SOLUTIONS',{fs:14,bold:true,color:BLUE});
  T(s,0.8,2.05,11.5,1.2,'PROJECT SATOSHI GATE',{fs:46,bold:true,color:NAVY,font:HF,valign:'middle'});
  T(s,0.8,3.4,9,0.5,'Board Transaction Recommendation',{fs:22,color:INK,font:HF});
  T(s,0.8,4.1,9,0.5,'Strategic access today. Control only when the economics are proven.',{fs:15,italic:true,color:BLUE});
  rect(s,0.45,5.2,12.43,0.02,LINE);
  T(s,0.45,5.35,2.5,0.35,'TEAM ETERNAL',{fs:13,bold:true,color:NAVY});
  const team=['Raunak Jain','Sambhav Khandelwal','Surya Swarup','Naman Ghosh','Akshith Aitha'];
  team.forEach((t,i)=>{ rect(s,0.45+i*2.5,5.8,2.35,0.5,PALE,LINE); T(s,0.45+i*2.5,5.8,2.35,0.5,t,{fs:12,bold:true,color:INK,align:'center',valign:'middle'}); });
  rect(s,0,6.72,13.33,0.78,GREY); rect(s,0,6.72,13.33,0.05,NAVY); rect(s,0,6.79,13.33,0.03,SKY);
  T(s,0.45,6.85,8,0.6,'DataForge 2026  ·  Case: Project Satoshi Gate  ·  Board deck',{fs:11,bold:true,color:NAVY,valign:'middle'});
  rect(s,12.2,6.9,0.03,0.5,NAVY); T(s,12.3,6.85,0.9,0.6,'1',{fs:22,bold:true,color:NAVY,valign:'middle',font:HF});
}

// ===== SLIDE 1 RECOMMENDATION =====
{ const s=slide('RECOMMENDATION','Board recommendation','Secure the capability — not the full-control risk');
  panel(s,0.45,1.4,6.1,2.55,'RECOMMENDATION');
  T(s,0.6,1.85,5.8,0.4,'**Do not acquire 100% of Liminal today.**',{fs:13,color:RED});
  T(s,0.6,2.2,5.8,0.5,'Pursue a **20–30% strategic minority investment**, anchored at **25%** as a midpoint team assumption, combined with:',{fs:11});
  chips(s,0.6,2.8,5.8,['Commercial custody/MPC partnership','Standalone governance'],0.45,10);
  chips(s,0.6,3.35,5.8,['Pre-agreed call option for future control','Retention- and performance-linked future consideration'],0.45,10);
  panel(s,6.78,1.4,6.1,2.55,'WHY THIS STRUCTURE');
  bullets(s,6.93,1.85,5.8,2.1,['**Strategic fit is real:** Liminal provides institutional custody and MPC infrastructure relevant to tokenized assets, e₹/CBDC infrastructure and cross-border settlement.','**Full control creates value leakage:** the case assumes **30–45% ARR churn** within 12 months after a full acquisition.','**Regulatory economics are severe:** full ownership creates an assumed **₹750 Cr recurring annual FCF drag**.','**Near-term earnings support is limited:** Liminal is currently approximately **PAT breakeven**.','**Staging preserves optionality:** Paytm secures strategic access while delaying irreversible control until customer and regulatory outcomes are observable.'],10,3);
  panel(s,0.45,4.15,12.43,2.4,'BOARD ASK');
  chevrons(s,0.6,4.65,7.2,0.6,['INVEST','VALIDATE','EXERCISE / HOLD / WALK AWAY'],[NAVY,BLUE,SKY]);
  T(s,8.0,4.65,4.7,0.6,'Exercise control **only after clearing all six gates:**',{fs:11.5,valign:'middle'});
  chips(s,0.6,5.65,12.13,['Client Retention','Regulatory Capital','Valuation','PAT','FCF','Compliance'],0.5,11,NAVY,WHITE);
}

// ===== SLIDE 2 STRATEGIC RATIONALE =====
{ const s=slide('RATIONALE','Strategic rationale','Liminal can extend Paytm from payments into institutional digital settlement infrastructure');
  panel(s,0.45,1.4,6.1,1.35,'PAYTM TODAY — exposure across'); chips(s,0.6,1.9,5.8,['UPI','Merchant Payments','Consumer Financial Services'],0.6,11);
  panel(s,6.78,1.4,6.1,1.35,'LIMINAL ADDS — institutional-grade'); chips(s,6.93,1.9,5.8,['Digital-Asset Custody','Multi-Party Computation','Secure Asset Infrastructure'],0.6,11);
  panel(s,0.45,2.95,12.43,1.25,'STRATEGIC BRIDGE');
  chevrons(s,0.6,3.42,12.13,0.62,['Payments','Institutional Custody & MPC','Tokenized Assets / Treasury','e₹ / CBDC Infrastructure','B2B & Cross-Border Settlement'],[NAVY,NAVY,BLUE,BLUE,SKY]);
  panel(s,0.45,4.4,7.4,2.15,'STRATEGIC VALUE');
  numrows(s,0.6,4.87,7.1,['Extends Paytm into **infrastructure adjacent to its core payments capabilities**.','Supports Paytm’s stated interest in **tokenized treasury and cross-border settlement**.','Creates **optionality** across future regulated digital-asset and settlement use cases.','Adds an **institutional capability layer** without requiring Paytm to immediately own every underlying activity.'],0.34,10);
  panel(s,8.08,4.4,4.8,2.15,'KEY QUESTION → OUR VIEW');
  T(s,8.23,4.85,4.5,0.7,'Does Paytm need **100% ownership today** to capture this strategic value?',{fs:11.5});
  rect(s,8.23,5.6,4.5,0.8,NAVY); T(s,8.38,5.6,4.2,0.8,'**No** — strategic access can precede strategic control.',{fs:13,color:WHITE,valign:'middle'});
}

// ===== SLIDE 3 OWNERSHIP PARADOX =====
{ const s=slide('RATIONALE','The ownership paradox','Full ownership risks impairing the very asset Paytm is paying to acquire');
  T(s,0.45,1.35,12.4,0.35,'₹4,000 Cr FULL ACQUISITION CREATES FOUR IMMEDIATE PRESSURES',{fs:12,bold:true,color:NAVY});
  const c=[['1. CUSTOMER CONFLICT','Liminal’s major institutional clients may resist having their custody provider owned by a competing payments platform.','Case assumption','**30–45% ARR lost** within 12 months'],['2. REGULATORY CAPITAL','Full ownership is assumed to trigger bank-like reserves against custodied assets.','Case assumption','**₹750 Cr recurring annual FCF drag**'],['3. FINANCIAL PRESSURE','Liminal is currently approximately PAT breakeven.','Implication','Limited acquired earnings initially offset new-share dilution or financing costs.'],['4. VALUATION PRESSURE','Paytm pays ₹4,000 Cr ÷ ₹220 Cr ARR = **18.2× headline ARR** before accounting for acquisition-driven churn.','Multiple','**18.2×** headline ARR, pre-churn']];
  c.forEach((t,i)=>{ const x=0.45+i*3.14; panel(s,x,1.75,3.0,2.75,t[0]); T(s,x+0.15,2.2,2.7,1.15,t[1],{fs:10.5}); rect(s,x+0.15,3.4,2.7,0.95,PALE,LINE); T(s,x+0.27,3.45,2.5,0.3,t[2].toUpperCase(),{fs:9,bold:true,color:BLUE}); T(s,x+0.27,3.72,2.5,0.6,t[3],{fs:10.5,valign:'middle'}); });
  panel(s,0.45,4.7,6.1,1.85,'CORE DEAL PARADOX',RED);
  T(s,0.6,5.15,5.8,1.3,'Paytm wants Liminal for its **institutional franchise** — but taking control may **weaken that franchise**.',{fs:13,valign:'middle'});
  panel(s,6.78,4.7,6.1,1.85,'BOARD IMPLICATION — separate the two questions');
  rect(s,6.93,5.15,2.55,1.25,PALE,LINE); T(s,7.03,5.15,2.35,1.25,'**Strategic attractiveness** of Liminal',{fs:12,align:'center',valign:'middle'});
  T(s,9.5,5.15,0.75,1.25,'from',{fs:11,italic:true,color:MUTED,align:'center',valign:'middle'});
  rect(s,10.27,5.15,2.46,1.25,PALE,LINE); T(s,10.37,5.15,2.26,1.25,'**Economic attractiveness** of owning 100% today',{fs:12,align:'center',valign:'middle'});
}

// ===== SLIDE 4 STRATEGIC OPTIONS =====
{ const s=slide('RATIONALE','Strategic options','Four paths — assessed on strategic access, control, downside and reversibility');
  tbl(s,0.45,1.4,12.43,[['','FULL ACQUISITION','MINORITY STAKE','JOINT VENTURE','WALK AWAY'],['Strategic access','High','**High** through partnership','High within JV scope','Low'],['Control','Full','Limited','Shared','None'],['Full-control churn exposure','30–45% case assumption','Not specified — validate','Not specified — validate','None'],['₹750 Cr capital treatment','Case assumes applicable','Not specified — validate','Not specified — validate','None'],['Upfront commitment','Highest','**Lower**','Structure-dependent','Nil'],['Reversibility','Low','**High**','Medium','High'],['Future-control optionality','Already exercised','**Can be preserved**','Can be negotiated','Lost unless partnership retained']],[22,19.5,19.5,19.5,19.5],10.5,0.4);
  panel(s,0.45,4.85,7.4,1.7,'CONCLUSION',GREEN);
  T(s,0.6,5.3,7.1,0.55,'**Minority + partnership + call option** is the strongest starting structure because it defers the two largest unresolved risks:',{fs:11});
  chips(s,0.6,5.9,7.1,['Customer response','Regulatory capital treatment'],0.45,11,NAVY,WHITE);
  panel(s,8.08,4.85,4.8,1.7,'DISCIPLINE',RED);
  T(s,8.23,5.3,4.5,0.7,'We do **not** assume minority ownership automatically eliminates churn or the ₹750 Cr capital requirement.',{fs:11});
  rect(s,8.23,6.0,4.5,0.4,PALE,LINE); T(s,8.23,6.0,4.5,0.4,'These become **validation gates**.',{fs:11,align:'center',valign:'middle'});
}

// ===== SLIDE 5 ARCHITECTURE =====
{ const s=slide('STRUCTURE','Recommended transaction architecture','Buy optionality first — pay for control only after uncertainty reduces');
  panel(s,0.45,1.4,4.4,3.15,'PHASE 1 — STRATEGIC ENTRY');
  T(s,0.6,1.85,4.1,0.5,'Team assumption: **25% stake** as the midpoint of the permitted 20–30% range. If priced pro-rata to the ₹4,000 Cr headline value:',{fs:10.5});
  rect(s,0.6,2.45,4.1,0.55,PALE,LINE); T(s,0.6,2.45,4.1,0.55,'Illustrative upfront investment = **₹1,000 Cr**',{fs:12,align:'center',valign:'middle'});
  T(s,0.6,3.08,4.1,0.3,'Proposed Phase-1 funding:',{fs:10.5,bold:true,color:NAVY});
  bullets(s,0.6,3.38,4.1,1.15,['**₹1,000 Cr** existing balance-sheet cash','**No** new debt','**No** new equity issuance','Paytm gross cash remains approximately **₹7,900 Cr** before fees'],10.5,2);
  const adds=[['+ COMMERCIAL PARTNERSHIP','Secure contractual access to Liminal’s custody/MPC infrastructure for agreed Paytm use cases.'],['+ GOVERNANCE RING-FENCE','Preserve operational, client-data and institutional independence.'],['+ PRE-AGREED CALL OPTION','Paytm receives the **right — not obligation** — to acquire control after a defined validation period.']];
  adds.forEach((a,i)=>{ const y=1.4+i*1.07; panel(s,5.05,y,3.7,0.97,a[0],BLUE); T(s,5.2,y+0.4,3.4,0.55,a[1],{fs:10,valign:'middle'}); });
  panel(s,8.95,1.4,3.93,3.15,'FUTURE-CONTROL PRICING PRINCIPLE');
  T(s,9.1,1.85,3.65,0.3,'Future consideration capped at the **lower of:**',{fs:10.5});
  numrows(s,9.1,2.18,3.65,['Agreed headline valuation mechanics','Retained-ARR / performance-based value'],0.36,10);
  T(s,9.1,3.1,3.65,0.3,'subject to:',{fs:10.5,bold:true,color:NAVY});
  chips(s,9.1,3.4,3.65,['client retention','regulatory capital treatment'],0.32,9);
  chips(s,9.1,3.78,3.65,['financial performance','agreed valuation cap'],0.32,9);
  chips(s,9.1,4.16,3.65,['customary transaction adjustments'],0.32,9);
  panel(s,0.45,4.75,12.43,1.8,'TRANSACTION LOGIC');
  rect(s,0.6,5.2,5.95,1.15,PALE,LINE); T(s,0.75,5.2,5.65,1.15,'Pay for **strategic access** today.',{fs:15,color:NAVY,align:'center',valign:'middle',font:HF});
  rect(s,6.78,5.2,5.95,1.15,NAVY); T(s,6.93,5.2,5.65,1.15,'Pay for **control** only after the retained value is observable.',{fs:15,color:WHITE,align:'center',valign:'middle',font:HF});
}

// ===== SLIDE 6 FACTS VS ASSUMPTIONS =====
{ const s=slide('STRUCTURE','Case facts vs team assumptions','Keep the model auditable: separate facts, calculations and assumptions');
  panel(s,0.45,1.4,4.05,4.35,'CASE FACTS — PAYTM');
  tbl(s,0.55,1.85,3.85,[['Metric','Value'],['Market capitalization','₹1,18,750 Cr'],['Diluted shares','64 Cr'],['Cash','₹8,900 Cr'],['Gross debt','₹350 Cr'],['Revenue','₹8,450 Cr'],['EBITDA','₹640 Cr'],['PAT','₹480 Cr'],['Diluted EPS','₹7.50'],['Credit rating','CRISIL AA− Stable']],[52,48],10,0.36,{firstBold:false});
  panel(s,4.65,1.4,4.05,4.35,'CASE FACTS — LIMINAL / DEAL');
  tbl(s,4.75,1.85,3.85,[['Metric','Value'],['Headline acquisition value','₹4,000 Cr'],['Headline consideration','₹2,100 Cr cash + ₹1,900 Cr equity'],['ARR','₹220 Cr'],['Current PAT','~ breakeven'],['Four largest clients','60% of ARR'],['Full-acquisition churn','30–45%'],['Full-control capital drag','₹750 Cr annual FCF'],['UPI MDR benefit to Paytm','₹115 Cr/year incremental net revenue']],[48,52],10,0.36,{firstBold:false});
  panel(s,8.85,1.4,4.03,4.35,'TEAM ASSUMPTIONS',BLUE);
  bullets(s,9.0,1.85,1.85,3.85,['Initial ownership: **25%** midpoint','Indicative minority investment: **₹1,000 Cr** pro-rata','Initial funding: existing cash','Validation period','Minority/JV churn','Minority/JV regulatory capital treatment','Liminal ARR growth','EBITDA / PAT / FCF margins'],9.5,3);
  bullets(s,10.95,1.85,1.85,3.85,['Debt cost and tax rate','WACC / required return','Integration costs','Synergies','MDR-to-PAT / FCF conversion','Call-option mechanics','Future-control valuation methodology'],9.5,3);
  rect(s,0.45,5.9,12.43,0.65,NAVY);
  T(s,0.6,5.9,7.9,0.65,'MODELING PRINCIPLE:   CASE FACT  ≠  DERIVED CALCULATION  ≠  TEAM ASSUMPTION',{fs:11.5,bold:true,color:WHITE,valign:'middle'});
  T(s,8.6,5.9,4.15,0.65,'Every material assumption must be **disclosed and sensitivity-tested**.',{fs:11.5,color:WHITE,valign:'middle',align:'right'});
}

// ===== SLIDE 7 VALUATION & CHURN =====
{ const s=slide('FINANCIALS','Valuation & churn','18.2× headline ARR becomes 26–33× on retained ARR under full-control churn');
  panel(s,0.45,1.4,6.1,2.75,'HEADLINE VALUATION  ·  ₹4,000 Cr ÷ ₹220 Cr ARR = 18.2× ARR');
  tbl(s,0.55,1.85,5.9,[['Full-control churn','ARR lost','Retained ARR','₹4,000 Cr / Retained ARR'],['0%','₹0 Cr','₹220 Cr','**18.2×**'],['30%','₹66 Cr','₹154 Cr','**26.0×**'],['37.5%','₹82.5 Cr','₹137.5 Cr','**29.1×**'],['45%','₹99 Cr','₹121 Cr','**33.1×**']],[26,22,24,28],10.5,0.4,{firstBold:false});
  panel(s,6.78,1.4,6.1,2.75,'EFFECTIVE MULTIPLE ON RETAINED ARR');
  bar(s,6.9,1.78,5.85,2.3,['0% churn','30% churn','37.5% churn','45% churn'],[18.2,26.0,29.1,33.1],[NAVY,BLUE,AMBER,RED],'0.0"×"');
  panel(s,0.45,4.3,4.6,2.25,'VALUE AT THE ORIGINAL 18.2× MULTIPLE');
  tbl(s,0.55,4.75,4.4,[['Churn','Retained ARR','Implied value'],['30%','₹154 Cr','**~₹2,800 Cr**'],['37.5%','₹137.5 Cr','**~₹2,500 Cr**'],['45%','₹121 Cr','**~₹2,200 Cr**']],[26,34,40],10.5,0.38,{firstBold:false});
  panel(s,5.2,4.3,3.7,2.25,'REVENUE RECOVERY HURDLE');
  stat(s,5.35,4.75,1.65,1.1,'+42.9%','growth required after **30% churn**: ₹154 Cr → ₹220 Cr',AMBER);
  stat(s,7.1,4.75,1.65,1.1,'+81.8%','growth required after **45% churn**: ₹121 Cr → ₹220 Cr',RED);
  T(s,5.35,5.95,3.4,0.5,'…just to **recover the original ARR base**.',{fs:10.5,italic:true,color:MUTED,valign:'middle'});
  panel(s,9.05,4.3,3.83,2.25,'STRUCTURING RESPONSE');
  chips(s,9.2,4.75,3.55,['Deferred Consideration','Earn-Out'],0.38,9.5); chips(s,9.2,5.2,3.55,['CVR','Retention-Linked Payout'],0.38,9.5);
  rect(s,9.2,5.68,3.55,0.75,NAVY); T(s,9.3,5.68,3.35,0.75,'**KEY MESSAGE:** Do not pay ₹4,000 Cr unconditionally for revenue that may disappear because of the acquisition itself.',{fs:9.5,color:WHITE,valign:'middle'});
}

// ===== SLIDE 8 FINANCING & EPS =====
{ const s=slide('FINANCIALS','Financing & EPS impact','Stage the capital commitment to protect liquidity, leverage and dilution');
  panel(s,0.45,1.4,4.0,5.15,'FULL-ACQUISITION COUNTERFACTUAL');
  T(s,0.6,1.85,3.7,0.3,'Headline consideration',{fs:10,bold:true,color:NAVY});
  rect(s,0.6,2.15,3.7,0.45,PALE,LINE); T(s,0.6,2.15,3.7,0.45,'**₹2,100 Cr cash + ₹1,900 Cr equity**',{fs:11,align:'center',valign:'middle'});
  T(s,0.6,2.7,3.7,0.45,'If ₹2,100 Cr is funded entirely from existing cash:',{fs:10.5});
  tbl(s,0.6,3.15,3.7,[['Cash','Before','After'],['Balance-sheet cash','₹8,900 Cr','**₹6,800 Cr**']],[44,28,28],10.5,0.38,{firstBold:false});
  T(s,0.6,4.05,3.7,0.3,'Illustrative equity dilution',{fs:10,bold:true,color:NAVY});
  tbl(s,0.6,4.35,3.7,[['Step','Value'],['Implied Paytm share price (₹1,18,750 Cr ÷ 64 Cr)','≈ ₹1,855/share'],['₹1,900 Cr equity consideration','≈ **1.02 Cr** new shares'],['Pro-forma diluted shares','≈ **65.02 Cr**'],['EPS if PAT remains ₹480 Cr','≈ **₹7.38** vs ₹7.50 baseline']],[62,38],9.5,0.38,{firstBold:false});
  panel(s,4.6,1.4,4.0,5.15,'MECHANICAL DILUTION');
  stat(s,4.75,1.85,3.7,1.1,'≈ 1.6%','mechanical EPS dilution: **₹7.38 vs ₹7.50** baseline',RED);
  T(s,4.75,3.05,3.7,0.3,'…before:',{fs:10.5,bold:true,color:NAVY});
  bullets(s,4.75,3.35,3.7,1.6,['financing costs','acquired earnings','synergies','integration costs','other transaction effects'],10.5,3);
  rect(s,4.75,5.1,3.7,1.3,NAVY); T(s,4.9,5.1,3.4,1.3,'**BOARD MESSAGE**\nFinancing should follow risk resolution — not precede it.',{fs:11.5,color:WHITE,valign:'middle'});
  panel(s,8.75,1.4,4.13,2.45,'RECOMMENDED PHASE-1 STRUCTURE',GREEN);
  T(s,8.9,1.85,3.85,0.3,'Illustrative **₹1,000 Cr cash investment for 25%**',{fs:10.5});
  tbl(s,8.9,2.2,3.85,[['Item','Phase 1'],['Cash remaining','**~₹7,900 Cr**'],['New debt','Nil'],['New shares','Nil'],['Immediate share-count dilution','**Nil**']],[62,38],10,0.3,{firstBold:false});
  panel(s,8.75,4.0,4.13,2.55,'FUTURE-CONTROL FINANCING PRINCIPLE');
  T(s,8.9,4.45,3.85,0.3,'**Do not pre-commit** the full financing mix today. At exercise:',{fs:10.5});
  bullets(s,8.9,4.85,3.85,1.65,['preserve sufficient liquidity','protect rating headroom','cap leverage','avoid excessive equity dilution','use contingent consideration where value remains uncertain'],10,2);
}

// ===== SLIDE 9 PAT & FCF BREAKEVEN =====
{ const s=slide('FINANCIALS','PAT & FCF breakeven','The deal must clear two separate hurdles: accounting accretion and cash-flow viability');
  panel(s,0.45,1.4,4.0,3.0,'1. ACCOUNTING / PAT TEST');
  tbl(s,0.6,1.85,3.7,[['Incremental PAT =',''],['Liminal PAT',''],['+ Realized operating synergies',''],['− Financing costs',''],['− Integration / operating costs',''],['− Other incremental expenses','']],[100,0],10,0.3,{firstBold:false});
  rect(s,0.6,3.75,3.7,0.5,PALE,LINE); T(s,0.6,3.75,3.7,0.5,'**Pro-Forma EPS = Pro-Forma PAT ÷ Diluted Shares**',{fs:10.5,align:'center',valign:'middle'});
  panel(s,4.6,1.4,4.0,3.0,'2. CASH / FCF TEST');
  tbl(s,4.75,1.85,3.7,[['Incremental FCF =',''],['Liminal FCF',''],['+ Realized cash synergies',''],['+ Applicable MDR cash contribution',''],['− **₹750 Cr capital drag**',''],['− Integration / other cash costs','']],[100,0],10,0.3,{firstBold:false});
  rect(s,4.75,3.75,3.7,0.5,PALE,LINE); T(s,4.75,3.75,3.7,0.5,'**Starting position:** Liminal ≈ PAT breakeven → limited acquired earnings to offset dilution or financing costs',{fs:9,align:'center',valign:'middle'});
  panel(s,8.75,1.4,4.13,3.0,'CRITICAL DISTINCTION — THE ₹115 Cr UPI MDR');
  T(s,8.9,1.85,3.85,0.3,'The ₹115 Cr UPI MDR benefit is **incremental Paytm net revenue**. It is:',{fs:10.5});
  bullets(s,8.9,2.35,3.85,0.9,['**not** automatically ₹115 Cr PAT','**not** automatically ₹115 Cr FCF','**not** created by acquiring Liminal'],10.5,2);
  rect(s,8.9,3.3,3.85,0.95,PALE,LINE); T(s,9.0,3.3,3.65,0.95,'**Treatment:** model it separately as a Paytm standalone corporate benefit / offset, using an explicit revenue-to-PAT / FCF conversion assumption.',{fs:9.5,valign:'middle'});
  panel(s,0.45,4.55,6.1,2.0,'WHAT THE CASE DOES NOT PROVIDE FOR LIMINAL');
  chips(s,0.6,5.0,5.8,['FCF','margins','capex'],0.36,10); chips(s,0.6,5.42,5.8,['working capital','growth','financing costs'],0.36,10);
  T(s,0.6,5.85,5.8,0.6,'Therefore, a specific breakeven year must be **assumption-driven and sensitivity-tested**.',{fs:10.5,valign:'middle'});
  panel(s,6.78,4.55,6.1,2.0,'CONTROL-EXERCISE RULE',RED);
  T(s,6.93,5.0,5.8,0.4,'Do **not** exercise control until the model demonstrates:',{fs:11});
  rect(s,6.93,5.45,2.8,0.9,NAVY); T(s,7.03,5.45,2.6,0.9,'credible **PAT / EPS breakeven**',{fs:11,color:WHITE,align:'center',valign:'middle'});
  T(s,9.73,5.45,0.5,0.9,'+',{fs:18,bold:true,color:NAVY,align:'center',valign:'middle'});
  rect(s,10.23,5.45,2.5,0.9,NAVY); T(s,10.33,5.45,2.3,0.9,'credible **FCF breakeven** after regulatory capital requirements',{fs:10,color:WHITE,align:'center',valign:'middle'});
}

// ===== SLIDE 10 RETENTION & GOVERNANCE =====
{ const s=slide('RISK & GOVERNANCE','Customer retention & governance','Protect the institutional franchise through structural independence');
  panel(s,0.45,1.4,4.3,5.15,'CONCENTRATION RISK');
  s.addChart(P.ChartType.doughnut,[{name:'ARR',labels:['Top-4 clients','Other'],values:[60,40]}],{x:0.5,y:1.8,w:2.0,h:1.9,chartColors:[NAVY,LIGHT],holeSize:58,showLegend:false,showValue:false,showLabel:false,showPercent:false});
  T(s,0.5,2.5,2.0,0.5,'60%',{fs:20,bold:true,color:NAVY,align:'center',valign:'middle',font:HF});
  bullets(s,2.55,1.9,2.1,1.8,['HDFC Bank','Axis Bank','CoinDCX','ZebPay'],11,3);
  T(s,2.55,3.2,2.1,0.5,'= **60% of Liminal ARR**\n= **₹132 Cr** of ₹220 Cr',{fs:10.5});
  hline(s,0.6,3.85,4.0);
  T(s,0.6,3.95,4.0,0.3,'Full-control churn assumption',{fs:10,bold:true,color:NAVY});
  stat(s,0.6,4.3,4.0,1.0,'₹66–99 Cr ARR lost','equivalent to approximately **50–75%** of the ARR represented by the four largest relationships',RED);
  rect(s,0.6,5.45,4.0,0.95,NAVY); T(s,0.7,5.45,3.8,0.95,'**CORE MESSAGE:** Governance is not cosmetic — it is a valuation-protection mechanism.',{fs:11,color:WHITE,valign:'middle'});
  panel(s,4.9,1.4,7.98,5.15,'GOVERNANCE ARCHITECTURE');
  const g=[['Standalone Liminal brand','Preserve institutional neutrality.'],['Arm’s-length board','Independent directors + clearly defined reserved matters.'],['Strict information barriers','No unrestricted Paytm access to client-sensitive custody or transaction data.'],['Independent compliance & cybersecurity oversight','Separate monitoring, escalation and reporting.'],['Neutral service standards','No preferential treatment for Paytm-linked activity.'],['Client-protection framework','Structured communication, consent and change-of-control management.'],['Retention-linked consideration','Align seller economics with preservation of the institutional franchise.']];
  tbl(s,5.05,1.85,7.68,[['#','Mechanism','What it does'],...g.map((r,i)=>[String(i+1),'**'+r[0]+'**',r[1]])],[6,38,56],10.5,0.55,{firstBold:false,align:'left'});
}

// ===== SLIDE 11 REGULATORY =====
{ const s=slide('RISK & GOVERNANCE','Regulatory & closing architecture','Resolve regulatory capital treatment before committing to control');
  chevrons(s,0.45,1.4,12.43,0.5,['BEFORE SIGNING','SIGNING → CLOSING','POST-CLOSE'],[NAVY,BLUE,SKY]);
  rect(s,0.45,2.0,4.05,2.75,WHITE,LINE); bullets(s,0.6,2.15,3.8,2.5,['Confirm feasibility of **minority ownership and commercial partnership**.','Determine expected **regulatory treatment of minority vs control**.','Conduct AML, data, cybersecurity and compliance diligence.','Conduct structured **key-client soundings**.','Define regulatory and customer conditions precedent.'],10.5,3);
  rect(s,4.64,2.0,4.05,2.75,WHITE,LINE); T(s,4.79,2.1,3.8,0.3,'Address, as applicable:',{fs:10,italic:true,color:MUTED}); bullets(s,4.79,2.4,3.8,2.3,['**RBI approval** / regulatory path','Competition clearance','Securities-related approvals','Client consents / retention protections','Information-security readiness','No material adverse regulatory change'],10.5,3);
  rect(s,8.83,2.0,4.05,2.75,WHITE,LINE); bullets(s,8.98,2.15,3.8,2.5,['Standalone compliance framework','AML controls','Data segregation','Cybersecurity monitoring','Independent compliance reporting','Board-level risk oversight'],10.5,3);
  panel(s,0.45,4.9,7.4,1.65,'MOST IMPORTANT UNRESOLVED QUESTION',RED);
  T(s,0.6,5.35,7.1,0.6,'Does minority ownership **avoid, reduce or still trigger** the ₹750 Cr capital requirement?',{fs:12.5});
  T(s,0.6,5.95,7.1,0.45,'The case does not specify the answer.',{fs:11,italic:true,color:MUTED});
  panel(s,8.08,4.9,4.8,1.65,'HARD DECISION GATE');
  rect(s,8.23,5.35,4.5,1.05,NAVY); T(s,8.35,5.35,4.25,1.05,'Do **not** exercise full control until regulatory capital treatment is **known and incorporated into the FCF model**.',{fs:11,color:WHITE,valign:'middle'});
}

// ===== SLIDE 12 COMPETITIVE & DOWNSIDE =====
{ const s=slide('RISK & GOVERNANCE','Competitive & downside response','Strategic urgency must not become a winner’s curse');
  panel(s,0.45,1.4,4.0,2.8,'PHONEPE–MASTERCARD THREAT');
  T(s,0.6,1.85,3.7,0.55,'The exploratory consortium creates a **strategic opportunity cost** if Paytm walks away. However, the case provides:',{fs:10.5});
  bullets(s,0.6,2.5,3.7,1.2,['no competing valuation','no competing transaction terms','no quantified bidder synergies','no certainty of completion'],10.5,3);
  panel(s,4.6,1.4,4.0,2.8,'PAYTM RESPONSE');
  T(s,4.75,1.85,3.7,0.3,'**Do not automatically match a higher bid.**',{fs:10.5,color:RED});
  T(s,4.75,2.15,3.7,0.3,'Set a risk-adjusted reservation value based on:',{fs:10.5});
  chips(s,4.75,2.5,3.7,['retained ARR','capital treatment'],0.32,9); chips(s,4.75,2.88,3.7,['client retention','financing impact'],0.32,9); chips(s,4.75,3.26,3.7,['PAT / FCF economics','strategic optionality'],0.32,9);
  T(s,4.75,3.6,3.7,0.55,'If another bidder exceeds Paytm’s reservation value: **walk away** rather than destroy shareholder value.',{fs:10,valign:'middle'});
  panel(s,8.75,1.4,4.13,2.8,'BOARD PRINCIPLE');
  rect(s,8.9,1.85,3.85,2.2,NAVY); T(s,9.05,1.85,3.55,2.2,'Competitive pressure may change **timing** — it should **not** change valuation discipline.',{fs:15,color:WHITE,valign:'middle',align:'center',font:HF});
  panel(s,0.45,4.35,12.43,2.2,'DOWNSIDE PLAYBOOK');
  tbl(s,0.6,4.8,12.13,[['Trigger','Response'],['**Churn > 45%**','Do not exercise control / activate price protection / reassess partnership.'],['**Capital requirement unacceptable**','Remain minority / restructure / exit.'],['**Key clients resist**','Strengthen ring-fence; no control exercise without acceptable retention.'],['**Paytm share price compresses**','Avoid fixed-value equity issuance that creates excessive dilution.'],['**PAT / FCF case fails**','Do not escalate capital because of sunk cost.'],['**Regulatory / security conditions fail**','Suspend exercise / terminate where contractual rights permit.']],[30,70],9.5,0.22,{firstBold:false,align:'left'});
}

// ===== SLIDE 13 ROADMAP =====
{ const s=slide('ROADMAP','Implementation roadmap & decision gates','Invest → Validate → Exercise / Hold / Walk Away');
  const ph=[['PHASE 1 | 0–3 MONTHS','INVEST',NAVY],['PHASE 2 | 3–12 MONTHS','VALIDATE',BLUE],['PHASE 3 | ~12 MONTHS+','DECIDE',SKY]];
  ph.forEach((p,i)=>{ const x=0.45+i*4.19; s.addShape(i===0?P.ShapeType.homePlate:P.ShapeType.chevron,{x,y:1.4,w:4.07,h:0.55,fill:{color:p[2]},line:{color:WHITE,width:1}}); T(s,x+0.3,1.4,3.5,0.55,'**'+p[0]+'**   ·   '+p[1],{fs:11,color:WHITE,valign:'middle',align:'center'}); });
  rect(s,0.45,2.05,4.05,3.35,WHITE,LINE); bullets(s,0.6,2.2,3.8,3.1,['Acquire strategic minority stake','Sign commercial custody/MPC partnership','Establish standalone governance','Negotiate call option','Define future-control pricing mechanics','Establish client and regulatory gates','Build integrated transaction model'],10.5,3);
  rect(s,4.64,2.05,4.05,3.35,WHITE,LINE);
  const v=[['CUSTOMERS','ARR retention · Key-client renewals · Concentration trajectory · Customer willingness under potential control'],['REGULATION','Capital treatment · Approval path · Compliance requirements'],['FINANCIALS','ARR trajectory · PAT progression · FCF generation · MDR conversion · Synergy realization'],['RISK','Cybersecurity · AML · Data segregation · Operational resilience']];
  v.forEach((r,i)=>{ const y=2.17+i*0.8; T(s,4.79,y,1.1,0.7,r[0],{fs:9.5,bold:true,color:BLUE,valign:'middle'}); T(s,5.9,y,2.7,0.7,r[1],{fs:9.5,valign:'middle'}); if(i<3) hline(s,4.79,y+0.76,3.75); });
  rect(s,8.83,2.05,4.05,3.35,WHITE,LINE);
  T(s,8.98,2.12,3.8,0.25,'EXERCISE CONTROL — only if:',{fs:9.5,bold:true,color:GREEN});
  bullets(s,8.98,2.37,3.8,1.3,['client retention remains acceptable','regulatory capital treatment is economically viable','valuation remains within Paytm’s reservation value','PAT/EPS economics are supportable','FCF economics are supportable','governance / compliance conditions are satisfied'],8.5,0);
  T(s,8.98,3.62,3.8,0.25,'HOLD MINORITY',{fs:9.5,bold:true,color:AMBER}); T(s,8.98,3.85,3.8,0.4,'If strategic value remains attractive but control economics remain unresolved.',{fs:8.5});
  T(s,8.98,4.27,3.8,0.25,'WALK AWAY / UNWIND — if:',{fs:9.5,bold:true,color:RED});
  T(s,8.98,4.5,3.8,0.85,'churn exceeds tolerance · capital drag destroys returns · key clients reject ownership · regulatory conditions deteriorate · valuation exceeds risk-adjusted value · PAT / FCF economics fail',{fs:8.5});
  rect(s,0.45,5.52,12.43,1.03,NAVY);
  T(s,0.6,5.52,1.6,1.03,'FINAL BOARD MESSAGE',{fs:10.5,bold:true,color:'BFD3F5',valign:'middle'});
  T(s,2.2,5.52,10.5,1.03,'Paytm should not pay today for risks it can observe tomorrow. Secure Liminal’s strategic infrastructure through a **minority investment and commercial partnership**. Preserve the **right — not obligation** — to acquire control. Commit the remaining capital only after **client trust, regulatory capital treatment, valuation and cash-flow economics are proven**. **Strategic access now. Control only when value is protected.**',{fs:10,color:WHITE,valign:'middle'});
}

// ===== APPENDIX A1 + A2 =====
{ const s=slide('APPENDIX','Appendix A1–A2','Transaction model key inputs · Churn sensitivity');
  panel(s,0.45,1.4,3.05,5.15,'A1 · PAYTM');
  tbl(s,0.55,1.85,2.85,[['Input','Value'],['Market capitalization','₹1,18,750 Cr'],['Diluted shares','64 Cr'],['Cash','₹8,900 Cr'],['Gross debt','₹350 Cr'],['Revenue','₹8,450 Cr'],['EBITDA','₹640 Cr'],['PAT','₹480 Cr'],['EPS','₹7.50'],['Rating','CRISIL AA− Stable']],[55,45],9.5,0.34,{firstBold:false});
  panel(s,3.65,1.4,3.05,5.15,'A1 · LIMINAL & RISKS');
  tbl(s,3.75,1.85,2.85,[['Input','Value'],['Headline value','₹4,000 Cr'],['ARR','₹220 Cr'],['Headline multiple','18.2× ARR'],['Current PAT','~ breakeven'],['Top-four-client concentration','60%'],['ARR churn (full control)','30–45%'],['Capital FCF drag (full control)','₹750 Cr/year']],[58,42],9.5,0.34,{firstBold:false});
  rect(s,3.75,4.75,2.85,1.65,PALE,LINE); T(s,3.85,4.8,2.65,1.55,'**PAYTM CORPORATE OFFSET**\nUPI MDR: **₹115 Cr/year** incremental net revenue.\n\n**Not** a Liminal transaction synergy.',{fs:9.5,valign:'middle'});
  panel(s,6.85,1.4,6.03,5.15,'A2 · CHURN SENSITIVITY');
  tbl(s,6.95,1.85,5.83,[['Churn','ARR lost','Retained ARR','Effective multiple'],['0%','₹0 Cr','₹220 Cr','**18.2×**'],['30%','₹66 Cr','₹154 Cr','**26.0×**'],['37.5%','₹82.5 Cr','₹137.5 Cr','**29.1×**'],['45%','₹99 Cr','₹121 Cr','**33.1×**']],[22,24,27,27],10.5,0.4,{firstBold:false});
  T(s,6.95,4.05,5.8,0.3,'RECOVERY HURDLE',{fs:10.5,bold:true,color:NAVY});
  stat(s,6.95,4.4,2.8,1.1,'+42.9%','30% churn: ₹154 Cr → ₹220 Cr',AMBER); stat(s,9.95,4.4,2.83,1.1,'+81.8%','45% churn: ₹121 Cr → ₹220 Cr',RED);
  T(s,6.95,5.65,5.8,0.6,'Growth required **merely to recover the original ARR base**.',{fs:10.5,italic:true,color:MUTED,valign:'middle'});
}

// ===== APPENDIX A3 + A4 =====
{ const s=slide('APPENDIX','Appendix A3–A4','Retention-linked value framework · EPS / dilution bridge');
  panel(s,0.45,1.4,6.1,5.15,'A3 · RETENTION-LINKED VALUE — at the original 18.2× ARR multiple');
  tbl(s,0.55,1.85,5.9,[['Churn','Retained ARR','Implied value','Value gap vs ₹4,000 Cr'],['0%','₹220 Cr','₹4,000 Cr','—'],['30%','₹154 Cr','**~₹2,800 Cr**','~₹1,200 Cr'],['37.5%','₹137.5 Cr','**~₹2,500 Cr**','~₹1,500 Cr'],['45%','₹121 Cr','**~₹2,200 Cr**','~₹1,800 Cr']],[18,26,28,28],10.5,0.4,{firstBold:false});
  T(s,0.6,4.05,5.8,0.3,'STRUCTURING PRINCIPLE',{fs:10.5,bold:true,color:NAVY});
  rect(s,0.6,4.4,2.85,0.8,PALE,LINE); T(s,0.7,4.4,2.65,0.8,'Upfront consideration = **strategic access**',{fs:11,align:'center',valign:'middle'});
  rect(s,3.6,4.4,2.8,0.8,NAVY); T(s,3.7,4.4,2.6,0.8,'Contingent consideration = **retained economic value**',{fs:11,color:WHITE,align:'center',valign:'middle'});
  T(s,0.6,5.35,5.8,0.3,'Future-control price should remain subject to:',{fs:10.5});
  chips(s,0.6,5.7,5.8,['valuation cap','retained ARR','performance','regulatory outcome'],0.4,10);
  panel(s,6.78,1.4,6.1,5.15,'A4 · EPS / DILUTION BRIDGE — full-acquisition illustration');
  tbl(s,6.88,1.85,5.9,[['Step','Value'],['Implied Paytm share price: ₹1,18,750 Cr ÷ 64 Cr','≈ **₹1,855**'],['₹1,900 Cr equity consideration','≈ **1.02 Cr** new shares'],['Pro-forma diluted shares','≈ **65.02 Cr**'],['EPS, assuming PAT remains ₹480 Cr','≈ **₹7.38**'],['Baseline EPS','₹7.50'],['Approximate mechanical dilution','**~1.6%**']],[62,38],10.5,0.4,{firstBold:false});
  T(s,6.93,4.8,5.8,0.3,'…before:',{fs:10.5,bold:true,color:NAVY});
  chips(s,6.93,5.15,5.8,['financing expense','acquired earnings','synergies'],0.38,9.5); chips(s,6.93,5.6,5.8,['integration costs','other transaction effects'],0.38,9.5);
}

// ===== APPENDIX A5 =====
{ const s=slide('APPENDIX','Appendix A5','PAT vs FCF breakeven');
  panel(s,0.45,1.4,6.1,4.0,'ACCOUNTING / PAT');
  tbl(s,0.55,1.85,5.9,[['Component',''],['Liminal PAT',''],['+ Synergies',''],['− Financing costs',''],['− Integration / operating costs',''],['**= Incremental PAT**','']],[100,0],11,0.42,{firstBold:false});
  rect(s,0.55,4.45,5.9,0.7,NAVY); T(s,0.65,4.45,5.7,0.7,'↓   **Pro-Forma EPS**',{fs:13,color:WHITE,align:'center',valign:'middle'});
  panel(s,6.78,1.4,6.1,4.0,'CASH / FCF');
  tbl(s,6.88,1.85,5.9,[['Component',''],['Liminal FCF',''],['+ Cash synergies',''],['+ Applicable MDR cash contribution',''],['− **₹750 Cr capital drag**',''],['− Integration cash costs',''],['**= Incremental FCF**','']],[100,0],11,0.42,{firstBold:false});
  rect(s,0.45,5.6,12.43,0.95,NAVY);
  T(s,0.6,5.6,1.6,0.95,'KEY RULE',{fs:11,bold:true,color:'BFD3F5',valign:'middle'});
  T(s,2.2,5.6,10.5,0.95,'**PAT breakeven ≠ FCF breakeven.** Both must be demonstrated **independently** before exercising full control.',{fs:13,color:WHITE,valign:'middle'});
}

// ===== APPENDIX A6 + A7 =====
{ const s=slide('APPENDIX','Appendix A6–A7','Risk register & mitigants · Board decision tree');
  panel(s,0.45,1.4,6.6,5.15,'A6 · RISK REGISTER & MITIGANTS');
  tbl(s,0.55,1.85,6.4,[['Risk','Transaction response'],['30–45% full-control churn','Minority first + retention-linked consideration'],['60% top-client concentration','Standalone governance + client protections'],['₹750 Cr annual capital drag','Regulatory gate before control'],['18.2× headline valuation','Retained-value pricing + valuation cap'],['Immediate equity dilution','Stage consideration; avoid Phase-1 issuance'],['Rating / leverage pressure','No Phase-1 debt; reassess at control exercise'],['PhonePe–Mastercard counterbid','Reservation value + walk-away discipline'],['Paytm stock compression','Avoid excessive fixed-value equity dilution'],['AML / data / cyber risk','Independent compliance + information barriers'],['>45% churn','No control exercise / remediation / unwind'],['Regulatory deterioration','Condition precedent / termination protection'],['Weak PAT / FCF economics','Do not escalate capital']],[42,58],9.5,0.34,{align:'left'});
  panel(s,7.2,1.4,5.68,5.15,'A7 · BOARD DECISION TREE');
  const steps=[['STEP 1','Is Liminal strategically valuable to Paytm?','YES ↓',GREEN],['STEP 2','Can Paytm secure strategic access without immediate full control?','YES — Minority + Commercial Partnership ↓',GREEN],['STEP 3','Are client retention and regulatory capital outcomes acceptable after validation?','YES → Test valuation + PAT + FCF economics  |  NO → Hold minority / restructure / exit',AMBER],['STEP 4','Does full control clear Paytm’s risk-adjusted financial and governance hurdles?','YES → Exercise call option  |  NO → Do not acquire control',AMBER]];
  steps.forEach((st,i)=>{ const y=1.85+i*0.98; rect(s,7.35,y,0.8,0.88,NAVY); T(s,7.35,y,0.8,0.88,st[0],{fs:9,bold:true,color:WHITE,align:'center',valign:'middle'}); rect(s,8.15,y,4.58,0.88,WHITE,LINE); T(s,8.25,y+0.04,4.4,0.42,st[1],{fs:9.5,bold:true,color:INK,valign:'middle'}); T(s,8.25,y+0.46,4.4,0.4,st[2],{fs:9,color:st[3],bold:true,valign:'middle'}); });
  rect(s,7.35,5.8,5.38,0.6,NAVY); T(s,7.45,5.8,5.2,0.6,'**END STATE:** Control becomes an earned option — not a day-one commitment.',{fs:10.5,color:WHITE,valign:'middle',align:'center'});
}

P.writeFile({fileName:'ETERNAL_Project_Satoshi_Gate_v2.pptx'}).then(()=>console.log('written',n,'slides'));
