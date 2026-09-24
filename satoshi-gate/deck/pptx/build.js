const pptxgen = require('pptxgenjs');
const P = new pptxgen(); P.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5
P.author = 'Team ETERNAL'; P.title = 'Project Satoshi Gate';
const NAVY='0B2A5B', BLUE='1E63D6', CYAN='00B4E6', INK='1C2433', BODY='3A4658', MUTED='6B7A90', LINE='D9E2F0', TINT='E9F0FB', GREEN='1B8A4C', RED='C63C3C', AMBER='D98A1B', WHITE='FFFFFF', BG='F6F8FC';
const HF='Arial', BF='Calibri';
const sh = () => ({ type:'outer', color:'0B2A5B', blur:6, offset:1.5, angle:90, opacity:0.10 });
let n=0;
function slide(tag, title, accent){
  const s=P.addSlide(); n++; s.background={color:BG};
  s.addText(tag.toUpperCase(),{x:0.4,y:0.28,w:8,h:0.25,fontFace:BF,fontSize:9,bold:true,color:BLUE,charSpacing:2,margin:0,isTextBox:true});
  s.addText([{text:title+' ',options:{color:NAVY}},{text:accent,options:{color:BLUE}}],{x:0.4,y:0.5,w:10.4,h:0.62,fontFace:HF,fontSize:18,bold:true,margin:0,valign:'top',isTextBox:true});
  s.addShape(P.ShapeType.roundRect,{x:10.95,y:0.38,w:1.98,h:0.5,fill:{color:WHITE},line:{color:LINE,width:0.75},rectRadius:0.08});
  s.addShape(P.ShapeType.roundRect,{x:11.08,y:0.5,w:0.26,h:0.26,fill:{color:NAVY},line:{color:NAVY},rectRadius:0.05});
  s.addText([{text:'Project Satoshi Gate',options:{bold:true,color:NAVY,breakLine:true}},{text:'Paytm × Liminal · Team ETERNAL',options:{color:MUTED}}],{x:11.4,y:0.38,w:1.5,h:0.5,fontFace:BF,fontSize:7.5,margin:0,valign:'middle',isTextBox:true});
  s.addText('CF = case fact · CALC = arithmetic on case facts · TA = team assumption (slide 7) · ₹ in Cr',{x:0.4,y:7.1,w:9,h:0.25,fontFace:BF,fontSize:8,color:MUTED,margin:0,isTextBox:true});
  s.addText(String(n).padStart(2,'0'),{x:12.4,y:7.1,w:0.53,h:0.25,fontFace:BF,fontSize:8,bold:true,color:MUTED,align:'right',margin:0,isTextBox:true});
  return s;
}
function box(s,x,y,w,h,fill=WHITE,line=LINE){ s.addShape(P.ShapeType.roundRect,{x,y,w,h,fill:{color:fill},line:{color:line,width:0.75},rectRadius:0.1,shadow:sh()}); }
function circ(s,x,y,d,color,txt){ s.addShape(P.ShapeType.ellipse,{x,y,w:d,h:d,fill:{color},line:{color}}); if(txt) s.addText(txt,{x,y,w:d,h:d,fontFace:HF,fontSize:d>0.3?9:8,bold:true,color:WHITE,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function sq(s,x,y,d,color,txt){ s.addShape(P.ShapeType.roundRect,{x,y,w:d,h:d,fill:{color},line:{color},rectRadius:0.05}); s.addText(txt,{x,y,w:d,h:d,fontFace:HF,fontSize:9,bold:true,color:WHITE,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function rich(str){ // **bold** markup
  const parts=str.split('**'); return parts.map((t,i)=>({text:t,options:{bold:i%2===1}}));
}
function card(s,x,y,w,h,title,items,color=BLUE,num=null,fs=9.5){
  box(s,x,y,w,h); circ(s,x+0.15,y+0.14,0.3,color,num); 
  s.addText(title,{x:x+0.52,y:y+0.1,w:w-0.62,h:0.38,fontFace:HF,fontSize:10.5,bold:true,color:NAVY,margin:0,valign:'middle',isTextBox:true});
  const paras=[]; items.forEach((it,i)=>{ const r=rich(it).filter(p=>p.text!==''); r.forEach(p=>p.options.bullet={indent:9}); r[r.length-1].options.breakLine = i<items.length-1; paras.push(...r); });
  s.addText(paras,{x:x+0.12,y:y+0.5,w:w-0.24,h:h-0.58,fontFace:BF,fontSize:fs,color:BODY,valign:'top',margin:0,paraSpaceAfter:3,isTextBox:true});
}
function panelTitle(s,x,y,w,title,color=BLUE){ circ(s,x+0.15,y+0.13,0.3,color); s.addText(title,{x:x+0.52,y:y+0.08,w:w-0.62,h:0.4,fontFace:HF,fontSize:10.5,bold:true,color:NAVY,margin:0,valign:'middle',isTextBox:true}); }
function para(s,x,y,w,h,str,fs=9.5,color=BODY,opts={}){ s.addText(rich(str),{x,y,w,h,fontFace:BF,fontSize:fs,color,valign:'top',margin:0,isTextBox:true,...opts}); }
function kpi(s,x,y,w,value,label,sub,color=BLUE,subcolor=GREEN){
  box(s,x,y,w,0.95); s.addShape(P.ShapeType.roundRect,{x:x+0.12,y:y+0.17,w:0.09,h:0.6,fill:{color},line:{color},rectRadius:0.04});
  s.addText(value,{x:x+0.3,y:y+0.08,w:w-0.4,h:0.4,fontFace:HF,fontSize:17,bold:true,color,margin:0,valign:'middle',isTextBox:true});
  s.addText(label,{x:x+0.3,y:y+0.46,w:w-0.4,h:0.22,fontFace:BF,fontSize:9,bold:true,color:INK,margin:0,isTextBox:true});
  s.addText(sub,{x:x+0.3,y:y+0.67,w:w-0.4,h:0.22,fontFace:BF,fontSize:8.5,color:subcolor,margin:0,isTextBox:true});
}
function banner(s,x,y,w,h,str,fill=NAVY,fs=9.5){ s.addShape(P.ShapeType.roundRect,{x,y,w,h,fill:{color:fill},line:{color:fill},rectRadius:0.08}); circ(s,x+0.15,y+h/2-0.13,0.26,CYAN,'!'); s.addText(rich(str),{x:x+0.5,y,w:w-0.6,h,fontFace:BF,fontSize:fs,color:WHITE,valign:'middle',margin:0,isTextBox:true}); }
function tbl(s,x,y,w,rows,colW,fs=8.5,rowH=null){
  const tw=colW.reduce((a,b)=>a+b,0); const cw=colW.map(c=>c/tw*w);
  const data=rows.map((r,i)=>r.map((c,j)=>({text:String(c).replace(/\*\*/g,''),options:{bold:i===0,color:i===0?WHITE:INK,fill:{color:i===0?NAVY:(i%2===0?TINT:WHITE)},align:j===0?'left':'center',valign:'middle',fontFace:BF,fontSize:fs,margin:[2,4,2,4]}})));
  const o={x,y,w,colW:cw,border:{type:'solid',color:LINE,pt:0.5},autoPage:false}; if(rowH) o.rowH=rowH; s.addTable(data,o);
}
function bars(s,x,y,w,h,labels,values,colors,fmt,opts={}){
  s.addChart(P.ChartType.bar,[{name:'v',labels,values}],{x,y,w,h,barDir:'col',chartColors:colors,chartColorsOpacity:100,showValue:true,dataLabelPosition:'outEnd',dataLabelFontSize:8,dataLabelFontBold:true,dataLabelColor:INK,dataLabelFormatCode:fmt,catAxisLabelFontSize:8,catAxisLabelColor:BODY,valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},showLegend:false,barGapWidthPct:45,valAxisMinVal:0,...opts});
}
function pill(s,x,y,w,txt,fill=BLUE){ s.addShape(P.ShapeType.roundRect,{x,y,w,h:0.28,fill:{color:fill},line:{color:fill},rectRadius:0.14}); s.addText(txt,{x,y,w,h:0.28,fontFace:BF,fontSize:8.5,bold:true,color:WHITE,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function arrowR(s,x,y,color=BLUE){ s.addShape(P.ShapeType.rightArrow,{x,y,w:0.3,h:0.22,fill:{color},line:{color}}); }

// ================= 1 COVER =================
{ const s=P.addSlide(); n++; s.background={color:WHITE};
  s.addShape(P.ShapeType.rect,{x:8.2,y:0,w:5.13,h:7.5,fill:{color:TINT},line:{color:TINT}});
  s.addShape(P.ShapeType.rect,{x:9.0,y:0.85,w:4.33,h:6.65,fill:{color:NAVY},line:{color:NAVY}});
  s.addShape(P.ShapeType.rect,{x:10.3,y:0,w:3.03,h:3.6,fill:{color:BLUE},line:{color:BLUE}});
  s.addShape(P.ShapeType.rect,{x:11.5,y:4.5,w:1.83,h:3.0,fill:{color:CYAN},line:{color:CYAN}});
  s.addShape(P.ShapeType.roundRect,{x:0.65,y:1.0,w:0.06,h:4.6,fill:{color:BLUE},line:{color:BLUE},rectRadius:0.03});
  s.addShape(P.ShapeType.roundRect,{x:1.05,y:1.0,w:0.3,h:0.3,fill:{color:NAVY},line:{color:NAVY},rectRadius:0.06});
  s.addText([{text:'Paytm',options:{bold:true,color:NAVY}},{text:'  ×  ',options:{color:MUTED}},{text:'Liminal Custody Solutions',options:{bold:true,color:BLUE}}],{x:1.45,y:0.95,w:6.5,h:0.4,fontFace:HF,fontSize:16,margin:0,valign:'middle',isTextBox:true});
  s.addText('BOARD TRANSACTION RECOMMENDATION · SEPTEMBER 2026',{x:1.05,y:1.5,w:7,h:0.3,fontFace:BF,fontSize:10,bold:true,color:BLUE,charSpacing:3,margin:0,isTextBox:true});
  s.addText([{text:'Project',options:{color:NAVY,breakLine:true}},{text:'Satoshi Gate',options:{color:BLUE}}],{x:1.05,y:1.85,w:7,h:1.9,fontFace:HF,fontSize:54,bold:true,margin:0,valign:'top',lineSpacingMultiple:0.95,isTextBox:true});
  s.addText('Strategic access today.\nControl only when the economics are proven.',{x:1.05,y:3.85,w:6.8,h:0.8,fontFace:BF,fontSize:17,bold:true,color:INK,margin:0,isTextBox:true});
  s.addText('A 26% strategic stake, a commercial custody/MPC partnership and a pre-agreed call option, instead of a ₹4,000 Cr full acquisition — supported by an auditable accretion/dilution and PAT/FCF breakeven model.',{x:1.05,y:4.75,w:6.8,h:0.8,fontFace:BF,fontSize:11,color:BODY,margin:0,isTextBox:true});
  // team block
  box(s,1.05,5.8,6.8,1.25,WHITE,LINE);
  s.addText('TEAM ETERNAL',{x:1.25,y:5.9,w:3,h:0.3,fontFace:HF,fontSize:12,bold:true,color:NAVY,charSpacing:2,margin:0,isTextBox:true});
  const team=['Raunak Jain','Sambhav Khandelwal','Surya Swarup','Naman Ghosh','Akshith Aitha'];
  team.forEach((t,i)=>{ const cx=1.25+i*1.3; circ(s,cx,6.3,0.28,i%2?CYAN:BLUE,t.split(' ').map(w=>w[0]).join('')); s.addText(t,{x:cx-0.15,y:6.6,w:1.3,h:0.35,fontFace:BF,fontSize:8.5,bold:true,color:INK,align:'center',margin:0,isTextBox:true}); });
  const tiles=[['₹1,040 Cr','Unconditional cheque: 26% stake, cash-funded'],['≤ ₹2,960 Cr','Control tranche, paid only against retained ARR'],['6 gates','Consents · Capital · Valuation · PAT · FCF · Compliance']];
  tiles.forEach((t,i)=>{ const y=1.5+i*1.55; s.addShape(P.ShapeType.roundRect,{x:9.5,y,w:3.4,h:1.25,fill:{color:'1D3F7A'},line:{color:'2E5296'},rectRadius:0.08}); s.addText(t[0],{x:9.7,y:y+0.1,w:3.0,h:0.6,fontFace:HF,fontSize:26,bold:true,color:WHITE,margin:0,valign:'middle',isTextBox:true}); s.addText(t[1],{x:9.7,y:y+0.72,w:3.0,h:0.45,fontFace:BF,fontSize:9.5,color:'DCE7FA',margin:0,isTextBox:true}); });
  s.addNotes('Open with the one-line thesis: buy access and an option now; pay for control only after client retention and regulatory capital treatment are observable.');
}

// ================= 2 RECOMMENDATION =================
{ const s=slide('Slide 1 · Recommendation','Board recommendation:','buy access and an option, not full control');
  const k=[['₹1,040 Cr','Phase-1 investment','26% stake · cash · 0.9% of mkt cap',BLUE,GREEN],['−29%','Full-deal year-1 EPS','₹5.29 vs ₹7.50 at headline mix',RED,RED],['₹750 Cr/yr','Capital drag at control','117% of EBITDA · NPV ₹4,238 Cr',RED,RED],['26–33×','Retained-ARR multiple','18.2× headline after 30–45% churn',AMBER,AMBER],['Hold','Base-case outcome','Control only if Liminal earns it',GREEN,GREEN]];
  k.forEach((t,i)=>kpi(s,0.4+i*2.53,1.25,2.4,...t));
  // left panel
  box(s,0.4,2.35,6.0,3.55); panelTitle(s,0.4,2.35,6.0,'Recommendation: a staged structure, not a full acquisition',BLUE);
  const rec=['**Invest ₹1,040 Cr in cash for 26%** — one share above the 25% special-resolution threshold: negative control without operational control (TA).','**Commercial custody/MPC partnership** for tokenized-treasury, e₹ and cross-border settlement use cases.','**Ring-fence Liminal**: standalone brand, arm’s-length board, information barriers, independent compliance.','**Call option on the remaining 74%**, months 12–24, capped at ₹2,960 Cr: ₹1,650 Cr upfront + up to ₹1,310 Cr retention earn-out. Never more than ₹4,000 Cr in total; never more than ₹1,040 Cr unconditional.'];
  rec.forEach((t,i)=>{ const y=2.85+i*0.72; s.addShape(P.ShapeType.roundRect,{x:0.55,y,w:5.7,h:0.64,fill:{color:BG},line:{color:LINE,width:0.5},rectRadius:0.06}); sq(s,0.65,y+0.17,0.3,BLUE,String(i+1)); para(s,1.05,y+0.06,5.1,0.55,t,9,BODY,{valign:'middle'}); });
  // right panel
  box(s,6.6,2.35,6.33,3.55); panelTitle(s,6.6,2.35,6.33,'Why not 100% today — four numbers the Board should hold',RED);
  tbl(s,6.75,2.85,6.03,[['Pressure','Case fact → calc','So what'],['Client revolt','30–45% ARR lost in 12 months (CF)','18.2× becomes 26–33× retained ARR'],['Capital trap','₹750 Cr/yr FCF drag (CF)','Larger than Paytm EBITDA; NPV > price'],['Earnings','Liminal ~breakeven (CF)','Y1 EPS ₹5.29 (−29%); ₹6.08 at 0% churn'],['Breakeven','Drag vs ₹115 Cr MDR (CF)','FCF never breaks even in 10 yrs; MDR ≤15%']],[22,38,40],8.5);
  banner(s,6.75,4.95,6.03,0.85,'Base expectation, stated plainly: under the case’s own assumptions the modal outcome is **Hold**. The option is insurance and a block on PhonePe–Mastercard, not a plan to buy.',NAVY,9);
  // board ask
  s.addShape(P.ShapeType.roundRect,{x:0.4,y:6.05,w:12.53,h:0.9,fill:{color:WHITE},line:{color:BLUE,width:1.5},rectRadius:0.1});
  s.addText('BOARD ASK',{x:0.55,y:6.12,w:1.3,h:0.75,fontFace:HF,fontSize:11,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true});
  para(s,1.8,6.1,7.2,0.8,'Approve **Invest → Validate (12 months) → Exercise / Hold / Walk away**; authorise the ₹1,040 Cr investment, option negotiation and guardrails (cash ≥ ₹5,000 Cr, gross debt/EBITDA ≤ 1.5×, no unconditional equity); delegate gate reviews to the M&A/Risk committee.',9,BODY,{valign:'middle'});
  ['Consents','Capital','Valuation','PAT','FCF','Compliance'].forEach((g,i)=>pill(s,9.15+ (i%3)*1.25, 6.18+Math.floor(i/3)*0.36,1.15,g));
  s.addNotes('Lead with the five tiles, then the four pressures. Say the word Hold before anyone asks whether this is just a minority stake.');
}

// ================= 3 STRATEGIC RATIONALE =================
{ const s=slide('Slide 2 · Strategic rationale','Strategic rationale:','access captures the value, ownership adds the risk');
  box(s,0.4,1.25,12.53,1.05); s.addText('STRATEGIC BRIDGE',{x:0.55,y:1.25,w:1.2,h:1.05,fontFace:HF,fontSize:9.5,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true});
  const st=[['Payments','UPI · merchants · consumer (CF)',NAVY],['Custody & MPC','Liminal: ISO 27001, SOC 2 (CF)',BLUE],['Tokenized assets','Treasury, digital assets',BLUE],['e₹ / CBDC rails','RBI pilot alignment (CF)',CYAN],['B2B & cross-border','Settlement infrastructure',CYAN]];
  st.forEach((t,i)=>{ const x=1.85+i*2.2; s.addShape(P.ShapeType.roundRect,{x,y:1.4,w:1.85,h:0.75,fill:{color:t[2]},line:{color:t[2]},rectRadius:0.08}); s.addText([{text:t[0],options:{bold:true,fontSize:10.5,breakLine:true}},{text:t[1],options:{fontSize:8.5,color:'E3ECFA'}}],{x,y:1.4,w:1.85,h:0.75,fontFace:BF,color:WHITE,align:'center',valign:'middle',margin:0,isTextBox:true}); if(i<4) arrowR(s,x+1.9,1.66); });
  card(s,0.4,2.45,4.1,2.15,'Paytm today (CF)',['₹1,18,750 Cr market cap on a turnaround re-rating','UPI and checkout growth slowing; PhonePe and Google Pay dominate volume','Regulatory scrutiny since RBI’s 2024 Paytm Payments Bank restrictions','Stated ambition: tokenized treasury and cross-border settlement aligned with e₹'],NAVY);
  card(s,4.62,2.45,4.1,2.15,'Liminal adds (CF)',['Institutional digital-asset custody + MPC infrastructure, founded 2021 (Mahin Gupta)','Clients: exchanges, hedge funds, OTC desks','HDFC Bank, Axis Bank, CoinDCX, ZebPay = 60% of ₹220 Cr ARR','Approximately PAT breakeven today'],BLUE);
  card(s,8.83,2.45,4.1,2.15,'Why it matters (TA)',['Custody/MPC is the trust layer every tokenized-settlement product needs; certifications take years to build','Adjacent to the core, not a replacement for it','A hedge on the e₹ thesis: if it scales Paytm holds the rail; if not, the cheque is ₹1,040 Cr, not ₹4,000 Cr'],CYAN);
  box(s,0.4,4.75,7.4,2.2); panelTitle(s,0.4,4.75,7.4,'Could a partnership alone do the job? (5.1)',BLUE);
  para(s,0.55,5.25,7.1,1.65,'For the **capability**, largely yes. For **security of supply**, no: a pure partnership leaves Liminal for sale, and the case says the consortium buys it if Paytm walks. Then Paytm’s critical custody supplier is owned by its main competitor. The 26% stake + ROFR/ROFO + call option buys the blocking right and the information rights to run the validation; the partnership captures the capability. Together they cost 26% of the headline price.',10.5);
  box(s,7.93,4.75,5.0,2.2); panelTitle(s,7.93,4.75,5.0,'Large enough to leave the core?',NAVY);
  para(s,8.08,5.25,4.7,1.65,'Large enough for a 26% position and a partnership; not large enough, on the case’s numbers, for a ₹4,000 Cr control cheque with a ₹750 Cr/yr carrying cost. **We size the bet to the evidence.** Walking away costs the neutral custodian and a 24–36 month build-or-partner path (TA). On pure earnings no structure is accretive before year 5.',10.5);
  s.addNotes('The bridge is the story: each stage needs the one before it. Then answer 5.1 directly: partnership-only fails on security of supply.');
}

// ================= 4 PARADOX =================
{ const s=slide('Slide 3 · Ownership paradox','The ownership paradox:','control impairs the asset; the drag alone outweighs the price');
  const c=[['1','Customer conflict',['Top-4 = ₹132 Cr of ₹220 Cr ARR (CF)','Case: ₹66–99 Cr leaves in 12 months = 50–75% of the top-4 book','Trigger: a competing consumer wallet owning the custodian'],RED],['2','Regulatory capital',['₹750 Cr/yr = 117% of EBITDA, 156% of PAT, 3.4× Liminal revenue','Liminal needs ~₹4,000 Cr ARR (18× today) to self-fund it','16 years away at 20% growth, 11 at 30% (TA)'],RED],['3','Earnings',['Liminal ~breakeven: no earnings to offset the deal’s own cost (CF)','Year-1 EPS ₹5.29 (−29%) at the headline mix (TA)','The “share-count only” ₹7.38 hides 95% of the dilution'],AMBER],['4','Valuation',['18.2× headline → 26–33× retained ARR','Each 10 pts of churn destroys ₹400 Cr at the paid multiple','Paytm at ~247× trailing P/E: a −29% print invites the buyback debate (CF §3.3)'],AMBER]];
  c.forEach((t,i)=>card(s,0.4+i*3.16,1.25,3.05,1.95,t[1],t[2],t[3],t[0],9));
  box(s,0.4,3.35,4.3,3.6); panelTitle(s,0.4,3.35,4.3,'The drag in context — ₹ Cr per year',RED);
  bars(s,0.5,3.8,4.1,2.5,['Liminal ARR','Paytm PAT','Paytm EBITDA','Capital drag/yr'],[220,480,640,750],[BLUE,NAVY,NAVY,RED],'"₹"#,##0');
  para(s,0.55,6.35,4.0,0.55,'10-year NPV of the drag at 12% WACC: **₹4,238 Cr**, more than the ₹4,000 Cr price (TA).',8.5,MUTED);
  box(s,4.85,3.35,4.3,3.6); panelTitle(s,4.85,3.35,4.3,'Effective multiple on retained ARR',AMBER);
  bars(s,4.95,3.8,4.1,2.5,['0% churn','30%','37.5%','45%'],[18.2,26.0,29.1,33.1],[BLUE,AMBER,AMBER,RED],'0.0"×"');
  para(s,5.0,6.35,4.0,0.55,'₹4,000 Cr ÷ retained ARR. Growth needed just to recover ₹220 Cr: +42.9% after 30% churn, +81.8% after 45% (CALC).',8.5,MUTED);
  banner(s,9.3,3.35,3.63,1.7,'**CORE DEAL PARADOX** — Paytm wants Liminal for its institutional franchise. Taking control is what breaks that franchise and what triggers the capital requirement.',NAVY,9.5);
  banner(s,9.3,5.2,3.63,1.75,'**BOARD IMPLICATION** — Separate the strategic attractiveness of Liminal (high) from the economic attractiveness of owning 100% today (negative under the case’s own assumptions).',BLUE,9.5);
  s.addNotes('Point at the red bar: the drag alone exceeds Paytm’s EBITDA. Everything else follows from that.');
}

// ================= 5 OPTIONS =================
{ const s=slide('Slide 4 · Strategic options','Strategic options:','only minority + option secures access and blocks the bid');
  tbl(s,0.4,1.25,12.53,[['Dimension','Full acquisition','26% minority + option  ★ recommended','Joint venture','Walk away'],
  ['Strategic access','Full','High: partnership + board seat + info rights','High inside JV scope only','None; 24–36 mo build (TA)'],
  ['Control','Full, now','Negative now; positive optional (months 12–24)','Shared','None'],
  ['Counter-bid defence','Complete','ROFR/ROFO + 26% veto + call option','Weak: Liminal still for sale','None: consortium acquires'],
  ['Churn exposure','30–45% (CF)','Not triggered (TA), tested via consents','Not triggered (TA)','Nil'],
  ['₹750 Cr capital drag','Applies (CF)','Not expected at 26% (TA); RBI comfort is a CP','Depends on JV custody scope','Nil'],
  ['Upfront commitment','₹2,100 Cr cash + 1.02 Cr shares','₹1,040 Cr cash; no shares, no debt','Capital + IP licence (TA)','Nil'],
  ['Year-1 EPS vs ₹7.50','₹5.29 (−29%)','₹6.81 (−9%): foregone interest only','Not modelled','₹7.50'],
  ['FCF profile','Never breaks even (drag)','Return is equity value; no cash yield','Not modelled','n/a'],
  ['Reversibility','Low','Medium–high (tag-along, ROFO)','Medium','High'],
  ['Future-control optionality','Already spent','Preserved and priced','Negotiable','Lost']],[18,20,26,18,18],8.5,0.33);
  box(s,0.4,5.1,4.9,1.85); panelTitle(s,0.4,5.1,4.9,'The JV, if needed (TA)',NAVY);
  para(s,0.55,5.55,4.6,1.35,'A Paytm-majority “SettleCo” for e₹/tokenized-treasury settlement: Liminal licenses MPC and runs custody ops; Paytm brings distribution, merchants and capital; Liminal’s institutional book stays outside. No revolt, no reserve on Paytm, but it does not block the consortium and splits governance. **Our fallback if RBI applies a reserve at minority level.**',10);
  box(s,5.45,5.1,4.0,1.85); panelTitle(s,5.45,5.1,4.0,'Conclusion',GREEN);
  para(s,5.6,5.55,3.7,1.35,'Minority + partnership + call option defers the two largest unresolved risks — **client response** and **capital treatment** — until they are observable, at 26% of the cheque, while removing the consortium’s easiest path.',10);
  box(s,9.6,5.1,3.33,1.85); panelTitle(s,9.6,5.1,3.33,'Discipline',RED);
  para(s,9.75,5.55,3.05,1.35,'We do **not** assume a minority automatically eliminates churn or the ₹750 Cr requirement. Both are gates, tested before any control is exercised.',10);
  s.addNotes('Walk the table column by column; the starred column wins on defence, drag and reversibility at once.');
}

// ================= 6 ARCHITECTURE =================
{ const s=slide('Slide 5 · Transaction architecture','Transaction architecture:','pay for access now, pay for control against retained ARR');
  const ph=[['1','Strategic entry · ₹1,040 Cr',['Secondary purchase of 26% at pro-rata of the ₹4,000 Cr headline = ceiling; target ₹850–950 Cr (bull-DCF pro-rata)','100% balance-sheet cash; no debt, no shares; equity-method associate','1 of 5 board seats + observer; info/audit rights; ROFR/ROFO; tag-along; anti-dilution; reserved matters'],BLUE],['2','Partnership + ring-fence',['Multi-year custody/MPC agreement for tokenized-treasury, e₹ and cross-border pilots, at arm’s length','Standalone brand, independent chair, information barriers, published client charter','Founder and MPC-engineering retention pool vesting over validation'],CYAN],['3','Call option on 74%',['Window months 12–24; a right, not an obligation; ROFR/ROFO persist after lapse','Cap ₹2,960 Cr = ₹1,650 Cr at exercise + earn-out ≤ ₹1,310 Cr, linear 55–100% retained ARR at month 18','Earn-out in Paytm shares (≤0.71 Cr, ±15% collar) or cash at Paytm’s election'],NAVY]];
  ph.forEach((t,i)=>card(s,0.4+i*4.21,1.25,4.11,1.95,t[1],t[2],t[3],t[0],9));
  box(s,0.4,3.35,6.9,3.6); panelTitle(s,0.4,3.35,6.9,'Control consideration vs post-control churn (₹ Cr)',BLUE);
  bars(s,0.5,3.75,6.7,2.45,['0%','10%','20%','30%','37.5%','45%','55%'],[2960,2669,2378,2087,1868,1650,1650],[GREEN,GREEN,BLUE,BLUE,AMBER,RED,RED],'#,##0');
  para(s,0.55,6.25,6.6,0.65,'Tracks 74% × 18.2× × retained ARR within 1–2%: the upfront covers the worst case, the earn-out pays only for revenue that survives control. Measured on the pre-control client base, audited, Paytm-related revenue excluded. Grand total: ₹4,000 Cr at 0% churn → ₹2,690 Cr at ≥45%.',8.5,MUTED);
  box(s,7.45,3.35,5.48,1.72); panelTitle(s,7.45,3.35,5.48,'Why 26%, not 25%',NAVY);
  para(s,7.6,3.8,5.2,1.2,'One share above 25% blocks special resolutions (new-investor allotment, charter changes, schemes). The veto does not stop a secondary sale; the ROFR/ROFO does. With the call option they close every route to the consortium.',10);
  box(s,7.45,5.22,5.48,1.73); panelTitle(s,7.45,5.22,5.48,'Why Liminal’s shareholders say yes (TA)',GREEN);
  para(s,7.6,5.67,5.2,1.2,'₹1,040 Cr of liquidity now; a defined path to the full ₹4,000 Cr; Paytm as anchor client; retention pool; and the alternative buyer carries the same wallet conflict. If the option is refused: 26% + ROFR/ROFO without the call still blocks and still gives access.',10);
  s.addNotes('The earn-out chart is the mechanism: green is full value, red is the floor. Fundamental value of 26% is ₹456–951 Cr, so the ₹1,040 Cr ceiling carries a disclosed premium.');
}

// ================= 7 ASSUMPTIONS =================
{ const s=slide('Slide 6 · Assumptions','Assumptions slide:','case facts vs calculations vs team assumptions');
  box(s,0.4,1.25,5.9,3.2); panelTitle(s,0.4,1.25,5.9,'Case facts (CF)',NAVY);
  tbl(s,0.5,1.7,5.7,[['Paytm','Value','Liminal / deal','Value'],['Market cap','₹1,18,750 Cr','Headline value','₹4,000 = ₹2,100 cash + ₹1,900 equity'],['Diluted shares','64 Cr','ARR','₹220 Cr'],['Cash / gross debt','₹8,900 / ₹350','PAT','~breakeven'],['Rev / EBITDA / PAT','₹8,450 / ₹640 / ₹480','Top-4 clients','60% of ARR'],['Diluted EPS (start)','₹7.50','Full-acq. churn','30–45% within 12 months'],['Rating','CRISIL AA− (Stable)','Capital drag','₹750 Cr/yr recurring FCF'],['Cash-portion funding','Cash, debt, or mix','UPI MDR (standalone)','₹115 Cr/yr net revenue']],[23,24,23,30],8);
  box(s,0.4,4.6,5.9,1.15); panelTitle(s,0.4,4.6,5.9,'Derived calculations (CALC)',BLUE);
  para(s,0.55,5.02,5.6,0.7,'Share price ₹1,855 (market cap ÷ shares) · 18.2× headline ARR · ₹1,900 Cr equity = 1.02 Cr shares · trailing P/E ≈ 247× · churn-adjusted multiples and values · drag ratios.',8.5);
  banner(s,0.4,5.9,5.9,1.05,'CASE FACT ≠ DERIVED CALCULATION ≠ TEAM ASSUMPTION. No case input is replaced by an external figure; every TA is flexed in the model.',NAVY,9);
  box(s,6.45,1.25,6.48,5.7); panelTitle(s,6.45,1.25,6.48,'Team assumptions (TA) — the values in the model',BLUE);
  tbl(s,6.55,1.7,6.28,[['#','Assumption','Base','Range'],['1','Stake / price','26% / ₹1,040 Cr (ceiling)','20–30%'],['2','Yield on surplus cash (pre-tax)','6.0%','5–7%'],['3','Cost of new debt (pre-tax)','8.5%','8–10%'],['4','Tax rate','25%','—'],['5','Liminal ARR growth','20% (bear 10%, bull 30%)','10–40%'],['6','EBITDA margin','0% → +5 pp/yr to 25%','20–30%'],['7','PAT / FCF','PAT = 75% EBITDA; FCF ≈ PAT','—'],['8','Churn under minority / JV','0% (consent gate)','0–20%'],['9','Churn at control','37.5% counterfactual; ≤20% to exercise','0–55%'],['10','Cost stickiness after churn','50% for one year','—'],['11','Drag at minority','0 (RBI comfort CP); tested ₹195 / ₹750','—'],['12','Drag treatment','FCF only; PPA not modelled','—'],['13','MDR conversion','80% flow-through → ₹69 Cr PAT/FCF','60–100%'],['14','One-time costs','Fees ₹15; integration ₹100','—'],['15','Synergies','₹0 base; upside only','—'],['16','WACC / terminal growth','12% / 5%','11–14%'],['17','Control tranche','₹1,650 up (₹1,150 cash + ₹500 debt) + ≤₹1,310 earn-out','—'],['18','Guardrails','Cash ≥ ₹5,000; GD/EBITDA ≤ 1.5×; collar ±15%','—'],['19','Validation / option window','12 months / months 12–24','—'],['20','Control gate on breakeven','PAT and FCF ≤ 5 yrs after exercise','—'],['21','Build-or-partner alternative','24–36 months','—']],[5,33,45,17],7.5,0.225);
  s.addNotes('This is the slide the Modeling Clarification asks for: 21 assumptions with values and ranges.');
}

// ================= 8 VALUATION =================
{ const s=slide('Slide 7 · Valuation & churn','Valuation & churn:','18.2× becomes 26–33×; the price needs 31% growth for 10 years');
  box(s,0.4,1.25,6.4,2.75); panelTitle(s,0.4,1.25,6.4,'Churn sensitivity (CALC) — ₹ Cr',AMBER);
  tbl(s,0.5,1.7,6.2,[['Churn','ARR lost','Retained','Eff. multiple','Value @18.2×','Gap','Recovery growth'],['0%','₹0','₹220','18.2×','₹4,000','—','—'],['30%','₹66','₹154','26.0×','₹2,800','₹1,200','+42.9%'],['37.5%','₹82.5','₹137.5','29.1×','₹2,500','₹1,500','+60.0%'],['45%','₹99','₹121','33.1×','₹2,200','₹1,800','+81.8%']],[12,13,13,15,16,14,17],8.5,0.33);
  para(s,0.55,3.5,6.1,0.45,'Every 10 points of churn destroys ₹400 Cr of value at the paid multiple.',8.5,MUTED);
  box(s,6.95,1.25,5.98,2.75); panelTitle(s,6.95,1.25,5.98,'What you need to believe — standalone DCF vs ₹4,000 Cr (TA)',BLUE);
  bars(s,7.0,1.65,5.85,1.75,['10% bear','20% base','30% bull','31.3% b/e','40%'],[811,1753,3658,4000,7345],[MUTED,BLUE,BLUE,AMBER,GREEN],'"₹"#,##0');
  para(s,7.1,3.42,5.75,0.55,'12% WACC, 5% TG, margin → 25%. Break-even growth **31.3% p.a. for 10 years** with zero churn and no drag. WACC 11–14% moves base value ₹2,127 → ₹1,265 Cr.',8.5,MUTED);
  card(s,0.4,4.15,4.1,2.8,'Is the valuation supportable? (5.3)',['Not as an unconditional ₹4,000 Cr','Only as a cap reached through retained ARR: ₹3,127 Cr total at 30% churn, ₹2,690 Cr at 45%','If Liminal delivers 30% growth, the cap sits 16% below the then-DCF of ~₹4,756 Cr','Add the drag NPV (₹4,238 Cr) and 100% ownership is negative below 40% growth'],BLUE,null,10);
  card(s,4.62,4.15,4.1,2.8,'Churn tolerance (5.2)',['At the headline price, **any churn above 0%** makes the deal unattractive: the price is unsupported before churn','Under our structure the price self-corrects down to 55% retention','Below 55% retention (churn > 45%) control is **never** exercised — the Board’s tolerance lives in the earn-out floor, not in a fixed price'],RED,null,10);
  card(s,8.83,4.15,4.1,2.8,'Structuring response',['Deferred consideration · retention earn-out · CVR-style payout on retained ARR · valuation cap at headline','Fundamental value of 26%: ₹456 Cr (base) – ₹951 Cr (bull); the ₹1,040 Cr ceiling carries a disclosed premium for blocking and access','Do not pay ₹4,000 Cr unconditionally for revenue that may disappear because of the acquisition itself'],NAVY,null,10);
  s.addNotes('The amber bar is the hinge: 31.3% growth for ten years with zero churn just to break even on price.');
}

// ================= 9 FINANCING =================
{ const s=slide('Slide 8 · Financing & EPS','Financing & EPS:','stage the capital; every full-deal mix is 12–46% dilutive');
  box(s,0.4,1.25,7.7,2.75); panelTitle(s,0.4,1.25,7.7,'Full-acquisition year-1 EPS by financing mix (TA: 6% cash yield, 8.5% debt, 25% tax, 37.5% churn)',RED);
  tbl(s,0.5,1.7,7.5,[['Structure','New shares','Y1 EPS','vs ₹7.50','+MDR','Cash after','Gross debt','GD/EBITDA'],['₹2,100 cash + ₹1,900 equity (case)','1.02 Cr','₹5.29','−29%','₹6.36','₹6,800','₹350','0.5×'],['₹2,100 debt + ₹1,900 equity','1.02 Cr','₹4.69','−38%','₹5.75','₹8,900','₹2,450','3.8× ⚠'],['₹1,400 cash + ₹700 debt + ₹1,900 eq.','1.02 Cr','₹5.09','−32%','₹6.15','₹7,500','₹1,050','1.6× ⚠'],['All cash ₹4,000','—','₹4.04','−46%','₹5.12','₹4,900 ⚠','₹350','0.5×'],['All equity ₹4,000','2.16 Cr','₹6.63','−12%','₹7.68','₹8,900','₹350','0.5×'],['Share-count-only view of case mix','1.02 Cr','₹7.38','−1.6%','—','—','—','—']],[30,10,9,9,9,11,11,11],8,0.3);
  box(s,8.25,1.25,4.68,2.75); panelTitle(s,8.25,1.25,4.68,'Year-1 EPS (₹/share)',BLUE);
  bars(s,8.3,1.65,4.55,2.3,['Baseline','Case mix','Debt+eq.','Mix','All cash','All equity','Phase 1'],[7.50,5.29,4.69,5.09,4.04,6.63,6.81],[NAVY,RED,RED,RED,RED,AMBER,GREEN],'"₹"0.00');
  box(s,0.4,4.15,5.5,1.95); panelTitle(s,0.4,4.15,5.5,'Recommended Phase 1 — ₹1,040 Cr cash for 26%',GREEN);
  para(s,0.55,4.6,5.2,1.45,'• Year-1 EPS **₹6.81 (−9.2% vs ₹7.50; −8.1% vs the ₹8.58 standalone-with-MDR baseline)**: entirely foregone treasury income (₹46.8 Cr/yr) less ₹2.6 Cr associate share. This is the option premium.\n• Sensitivity: ₹6.93 at 5% yield, ₹6.69 at 7%. With MDR added: ₹7.89.\n• Share-count dilution nil; new debt nil; cash after ₹7,860 Cr; GD/EBITDA 0.5×; net cash ₹7,510 Cr.',8.5);
  box(s,6.05,4.15,6.88,1.95); panelTitle(s,6.05,4.15,6.88,'Sources & uses (TA)',NAVY);
  tbl(s,6.15,4.58,6.68,[['','Uses','Sources'],['Phase 1','26% stake ₹1,040 + fees ₹15 = ₹1,055','Balance-sheet cash ₹1,055; debt 0; equity 0'],['Control (if exercised)','Upfront ₹1,650 + integration ₹100 + earn-out ≤ ₹1,310','Cash ₹1,250 + new debt ₹500 + shares ≤ ₹1,310 (≤0.71 Cr, collared)'],['Maximum ever','₹4,000 Cr total = headline','Unconditional maximum ₹1,040 Cr']],[20,40,40],8,0.3);
  para(s,6.15,5.8,6.7,0.3,'Post-control: cash ₹6,710 Cr, gross debt ₹850 Cr (1.3×), net cash ₹5,860 Cr — inside both guardrails. Cost of funds after control ₹130 Cr/yr.',8,MUTED);
  banner(s,0.4,6.25,12.53,0.7,'How to read it: at ~247× P/E equity is Paytm’s cheapest currency in EPS terms and cash its most expensive (4.5% post-tax yield vs 0.4% earnings yield); but all-equity issues 3.3% of the company for a breakeven asset, and debt-funding the cash leg breaches AA− headroom (3.8× EBITDA). **No mix rescues a full acquisition. Financing follows risk resolution.**',NAVY,8.5);
  s.addNotes('The green bar is the recommended path; the only way to stay near ₹7.50 is not to do the full deal.');
}

// ================= 10 BREAKEVEN =================
{ const s=slide('Slide 9 · PAT & FCF breakeven','PAT & FCF breakeven:','the full deal never gets there; control only if Liminal earns it');
  box(s,0.4,1.25,7.2,3.25); panelTitle(s,0.4,1.25,7.2,'EPS path by route (₹/share, TA base) — dashed = ₹7.50 baseline',BLUE);
  const yrs=['Y1','Y2','Y3','Y4','Y5','Y6','Y7'];
  s.addChart(P.ChartType.line,[{name:'Control end-Y1, bull 30%',labels:yrs,values:[6.81,5.83,6.24,6.86,7.77,8.48,9.40]},{name:'Control end-Y1, base 20%',labels:yrs,values:[6.81,5.77,6.06,6.46,6.99,7.31,7.69]},{name:'Full acquisition today',labels:yrs,values:[5.29,6.16,6.34,6.59,6.92,7.11,7.35]},{name:'₹7.50 baseline',labels:yrs,values:[7.5,7.5,7.5,7.5,7.5,7.5,7.5]}],{x:0.5,y:1.65,w:7.0,h:2.8,chartColors:[GREEN,AMBER,RED,MUTED],lineSize:2.5,lineDataSymbol:'circle',lineDataSymbolSize:5,showLegend:true,legendPos:'b',legendFontSize:8,legendColor:BODY,catAxisLabelFontSize:8,catAxisLabelColor:BODY,valAxisLabelFontSize:8,valAxisLabelColor:BODY,valAxisMinVal:4,valAxisMaxVal:10,valGridLine:{color:LINE,size:0.5},catGridLine:{style:'none'},valAxisLabelFormatCode:'0.0'});
  box(s,7.75,1.25,5.18,3.25); panelTitle(s,7.75,1.25,5.18,'₹750 Cr drag vs ₹115 Cr MDR (5.3)',RED);
  s.addChart(P.ChartType.bar,[{name:'v',labels:['Drag','MDR gross','MDR after PAT/FCF conv.'],values:[750,115,69]}],{x:7.85,y:1.65,w:5.0,h:1.35,barDir:'bar',chartColors:[RED,BLUE,CYAN],showValue:true,dataLabelPosition:'outEnd',dataLabelFontSize:8,dataLabelFormatCode:'"₹"#,##0',catAxisLabelFontSize:8,catAxisLabelColor:BODY,valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},showLegend:false,barGapWidthPct:35,valAxisMinVal:0});
  para(s,7.9,3.05,4.9,1.4,'MDR covers **15.3%** of the drag at the revenue line, **9.2%** after conversion. Net cash cost of full ownership ~₹681 Cr/yr. The MDR accrues whether or not Paytm buys Liminal: a standalone tailwind (+₹1.08 EPS), never a deal synergy. Even a **₹100 Cr/yr** recurring capital cost fails the 5-year FCF gate in every trajectory; ₹50 Cr passes only in bull with zero churn.',8.5);
  box(s,0.4,4.65,12.53,2.3); panelTitle(s,0.4,4.65,12.53,'Breakeven results — two tests, both required: PAT (accounting) and FCF (cash, after drag). TA base: 20% growth, margin ramp; 37.5% churn in the full-acquisition counterfactual',NAVY);
  tbl(s,0.5,5.1,12.33,[['Path','Y1 EPS','PAT breakeven','FCF breakeven','Read-across'],['Full acquisition today (case mix)','₹5.29','Year 8 (Y3 only if MDR credited)','Never in 10 yrs; Y1 FCF −₹986 Cr; cum. −₹9,965 Cr by Y10','Even 0% churn + 30% growth + MDR: no FCF breakeven'],['Phase 1: 26% minority','₹6.81','Associate income covers interest Y9 base / Y6 bull','No cash yield until dividends or exit; return is equity value','Cost ₹47 Cr/yr; a pro-rata drag would make it ₹242 Cr'],['Control end-Y1, base 20%','₹5.77 trough','Year 7','Year 7','Fails ≤5-yr gate → Hold'],['Control end-Y1, bull 30%','₹5.83 → ₹7.77 (Y5)','Year 5','Year 5','Passes → Exercise (Y6 with 20% churn)']],[22,12,22,24,20],8,0.34);
  s.addNotes('Green line crosses the baseline in year 5: the only route that passes both gates. Red never does on cash.');
}

// ================= 11 GOVERNANCE =================
{ const s=slide('Slide 10 · Retention & governance','Customer retention & governance:','independence clients can verify');
  box(s,0.4,1.25,5.2,2.05); panelTitle(s,0.4,1.25,5.2,'Concentration risk (CF → CALC)',RED);
  s.addChart(P.ChartType.doughnut,[{name:'ARR',labels:['Top-4 clients','Other clients'],values:[60,40]}],{x:0.45,y:1.6,w:1.7,h:1.65,chartColors:[BLUE,LINE],holeSize:60,showLegend:false,showValue:false,showLabel:false,showPercent:false,dataLabelFontSize:8});
  s.addText('60%',{x:0.45,y:2.15,w:1.7,h:0.4,fontFace:HF,fontSize:15,bold:true,color:NAVY,align:'center',margin:0,isTextBox:true});
  para(s,2.25,1.7,3.25,1.5,'**HDFC Bank + Axis Bank + CoinDCX + ZebPay = ₹132 Cr** of ₹220 Cr ARR.\nCase churn ₹66–99 Cr = **50–75% of the top-4 book**.\nRevolt trigger: a competing wallet operator seeing custody flows.',9);
  box(s,5.75,1.25,7.18,2.05); panelTitle(s,5.75,1.25,7.18,'How significant is the risk of losing the top-4? (5.2)',AMBER);
  para(s,5.9,1.7,6.9,1.55,'Under full control, **existential**: the case removes half to three-quarters of top-4 revenue. Under the ring-fenced minority, **manageable**: no change of control occurs, contracts are unaffected, and the consent process tells the Board in advance what control would cost. Governance converts a 30–45% churn assumption into a ≤20% consent gate — and the earn-out pays sellers to protect the same clients.',9.5);
  const g=[['Standalone brand & entity','No Paytm branding or shared front-ends'],['Arm’s-length board','Independent chair; Paytm 1 of 5 (2 of 7 on control); reserved matters exclude custody ops'],['Information barriers','No client data to Paytm; MPC key shares never on Paytm infrastructure; segregated desk'],['Independent compliance & cyber','CCO/CISO report to Liminal risk committee; annual attestation shared with clients'],['Neutral service standards','Published client charter: no preferential pricing, routing or SLAs'],['Client-protection framework','Change-of-control consent rights, data portability, top-4 soundings, named owners'],['Retention-linked consideration','Earn-out and management pool scale with retained ARR: ₹291 Cr per 10 pts'],['Founder & engineer retention','Mahin Gupta and MPC core on vesting economics through validation']];
  g.forEach((t,i)=>{ const x=0.4+(i%4)*3.16, y=3.45+Math.floor(i/4)*1.35; box(s,x,y,3.05,1.22); sq(s,x+0.12,y+0.12,0.3,BLUE,String(i+1)); s.addText(t[0],{x:x+0.5,y:y+0.1,w:2.5,h:0.34,fontFace:HF,fontSize:9.5,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true}); para(s,x+0.12,y+0.5,2.82,0.7,t[1],8.5); });
  banner(s,0.4,6.3,12.53,0.62,'Governance is not cosmetic: it is the valuation-protection mechanism, designed to be audited by clients, not just described to them.',NAVY,9.5);
  s.addNotes('Eight mechanisms, each with an owner; number seven aligns sellers with retention.');
}

// ================= 12 REGULATORY =================
{ const s=slide('Slide 11 · Regulatory path','Regulatory & closing:','answer the capital question in writing before control');
  const lanes=[['Before signing','Phase 1 · indicative 8–12 weeks (TA)',['RBI consultation: PA-licence holder at 26% of a custody provider; capital treatment at minority vs control. **Signing condition: written comfort that no bank-like reserve applies at 26%**','Diligence: AML programme and FIU-IND standing; data protection and key-material localisation; ISO 27001 / SOC 2 evidence; client change-of-control clauses','Top-4 soundings under NDA; competition and securities notifiability analysis'],BLUE],['Signing → closing','Phase 1 conditions precedent',['RBI comfort letter','No material adverse regulatory change on either side','Key-client consents where contracts bite at minority level','FIU-IND registration in good standing; clean cyber audit','Stock-exchange disclosure on signing'],CYAN],['At control exercise','Phase 3 · indicative 4–6 months (TA)',['RBI change-in-control approval','Competition clearance','SEBI/exchange approvals for share-settled earn-out (preferential-issue rules, shareholder resolution)','Client change-of-control consents (Gate 1)','Refreshed AML/cyber audit'],NAVY],['Post-close','All phases',['Standalone compliance framework','AML transaction monitoring and reporting','Segregated data and key infrastructure','Continuous cyber monitoring and incident reporting','Independent compliance reporting to both boards’ risk committees'],GREEN]];
  lanes.forEach((t,i)=>{ const x=0.4+i*3.16; box(s,x,1.25,3.05,3.55); circ(s,x+0.15,1.38,0.3,t[3],String(i+1)); s.addText(t[0],{x:x+0.52,y:1.32,w:2.4,h:0.3,fontFace:HF,fontSize:10.5,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true}); s.addText(t[1],{x:x+0.52,y:1.6,w:2.4,h:0.25,fontFace:BF,fontSize:8.5,bold:true,color:t[3],margin:0,isTextBox:true}); const paras=[]; t[2].forEach((it,k)=>{const r=rich(it).filter(p=>p.text!==''); r.forEach(p=>p.options.bullet={indent:9}); r[r.length-1].options.breakLine=k<t[2].length-1; paras.push(...r);}); s.addText(paras,{x:x+0.12,y:1.95,w:2.82,h:2.75,fontFace:BF,fontSize:9.5,color:BODY,valign:'top',margin:0,paraSpaceAfter:4,isTextBox:true}); });
  box(s,0.4,4.95,4.1,2.0); panelTitle(s,0.4,4.95,4.1,'Does owning custody add requirements? (5.4)',NAVY);
  para(s,0.55,5.4,3.8,1.5,'Yes, per the case: bank-like reserves against custodied assets at full ownership (₹750 Cr/yr). Our design keeps the custody licence, the custodied assets and any reserves inside Liminal, and keeps Paytm at negative control until the treatment is written down.',10);
  box(s,4.62,4.95,4.1,2.0); panelTitle(s,4.62,4.95,4.1,'The one question that decides the deal',RED);
  para(s,4.77,5.4,3.8,1.5,'Does minority ownership avoid, reduce or still trigger the ₹750 Cr requirement? The case does not say. Slide 10 shows why it decides everything: even a **₹100 Cr/yr** recurring cost defeats the five-year FCF gate in every trajectory.',10);
  box(s,8.83,4.95,4.1,2.0); panelTitle(s,8.83,4.95,4.1,'Hard decision gate',GREEN);
  para(s,8.98,5.4,3.8,1.5,'**No control without written regulatory capital treatment incorporated into the FCF model.** If a reserve applies at minority level, Phase 1 is restructured toward the JV/licence path before signing.',10);
  s.addNotes('Four lanes, left to right in time. The signing condition in lane one is the most important line on the slide.');
}

// ================= 13 DOWNSIDE =================
{ const s=slide('Slide 12 · Competitive & downside','Competitive & downside:','set the walk-away line now; the structure absorbs the rest');
  card(s,0.4,1.25,4.1,2.15,'PhonePe–Mastercard threat (CF)',['Exploratory consortium if Paytm walks; no competing price, terms, synergies or certainty in the case','If they win: they get the rail + Mastercard cross-border; Paytm builds or partners elsewhere (24–36 mo, TA)','They inherit the same wallet conflict, price and capital question; Mastercard’s bank ties are their one real edge'],NAVY,null,9.5);
  card(s,4.62,1.25,4.1,2.15,'Paytm’s response (5.5)',['Reservation value: total ≤ ₹4,000 Cr, ≤ ₹1,040 Cr unconditional, no tranche above 18.2× retained ARR, no control at a drag that defeats 5-yr FCF breakeven','**If outbid on unconditional terms: let them** — the winner’s curse the case describes','Fallback: alternative custodian partnership; redeploy toward buybacks and organic e₹ build'],BLUE,null,9.5);
  card(s,8.83,1.25,4.1,2.15,'If Paytm’s multiple compresses',['Phase 1 is cash: independent of the stock','A 25% price fall lifts the ₹1,900 Cr equity leg from 1.02 to 1.37 Cr shares — still ~2%; the real risk is the narrative of a −29% print at ~247× P/E','Answer: no unconditional equity, ±15% collar, cash-settle election; the unconditional cheque is 0.9% of market cap'],AMBER,null,9.5);
  box(s,0.4,3.55,7.3,2.65); panelTitle(s,0.4,3.55,7.3,'Downside matrix — how the recommendation changes',BLUE);
  tbl(s,0.5,4.0,7.1,[['Consents / churn ↓ · Capital drag →','None / structured away','Pro-rata at 26% (≈₹195 Cr)','Full ₹750 Cr at any ownership'],['≥80% consents (churn ≤20%)','EXERCISE if bull trajectory and cap hold','Hold; JV/licence for capability','Hold 26% only if drag-free, else restructure/exit'],['55–80% (churn 20–45%)','HOLD; earn-out floor protects; re-test m24','Hold or restructure to JV','Restructure or exit'],['<55% (churn >45%)','NO CONTROL; remediation ladder','Exit','Exit']],[28,24,24,24],8,0.5);
  box(s,7.85,3.55,5.08,2.65); panelTitle(s,7.85,3.55,5.08,'Remediation & unwind ladder if churn breaches 45% (5.6)',RED);
  [['30d','Independent cause review; CEO outreach to each top-4 client; Paytm director steps back to observer',AMBER],['90d','Governance reset; published barrier attestation; fee holidays / SLA guarantees funded from the sellers’ earn-out at risk',AMBER],['180d','Still <55% retention: no exercise; ROFO/tag process to a neutral buyer, or convert to licence + warrants. Sunk cost never justifies escalation',RED]].forEach((t,i)=>{ const y=4.0+i*0.7; sq(s,8.0,y+0.12,0.38,t[2],t[0]); para(s,8.5,y,4.3,0.66,t[1],8.5,BODY,{valign:'middle'}); });
  banner(s,0.4,6.35,12.53,0.6,'Competitive pressure may change timing; it must not change valuation discipline.',NAVY,9.5);
  s.addNotes('The matrix answers the Mission’s “show how your recommendation changes”: capital treatment decides the column, consents decide the row.');
}

// ================= 14 ROADMAP =================
{ const s=slide('Slide 13 · Roadmap & gates','Roadmap & decision gates:','Invest → Validate → Exercise / Hold / Walk away');
  const tl=[['Months 0–3 · INVEST',1,BLUE],['Months 3–12 · VALIDATE',3,CYAN],['Months 12–24 · DECIDE: Exercise / Hold / Walk away',4,NAVY]]; let x=0.4; const tot=8, W=12.53;
  tl.forEach(t=>{ const w=W*t[1]/tot-0.08; s.addShape(P.ShapeType.roundRect,{x,y:1.25,w,h:0.2,fill:{color:t[2]},line:{color:t[2]},rectRadius:0.1}); s.addText(t[0],{x,y:1.47,w,h:0.25,fontFace:BF,fontSize:8.5,bold:true,color:t[2],align:'center',margin:0,isTextBox:true}); x+=w+0.08; });
  card(s,0.4,1.85,4.7,1.7,'Invest · months 0–3',['Close 26% for ≤ ₹1,040 Cr; partnership live; ring-fence installed','Option, earn-out, ROFR/ROFO documented; RBI comfort obtained','Retention pool in place; Board model with quarterly gate reporting'],BLUE,'1',9.5);
  card(s,0.4,3.65,4.7,2.45,'Validate · months 3–12',['Customers: retention, top-4 renewals, written consents to control','Regulation: written capital treatment; approval path; AML standing','Financials: month-12 ARR ≥ ₹286 Cr = bull, ~₹264 Cr = base; margins; cash; MDR tracked separately','Risk: cyber, AML, data segregation, barrier attestation'],CYAN,'2',9.5);
  box(s,5.25,1.85,7.68,4.25); panelTitle(s,5.25,1.85,7.68,'Decide · months 12–24 — six quantified gates',NAVY);
  tbl(s,5.35,2.3,7.48,[['Gate','Threshold to exercise control'],['1 · Client consents','≥80% of ARR consents in writing to Paytm control under the ring-fence; implied churn ≤20%'],['2 · Regulatory capital','Written RBI treatment; recurring cost nil or structured away (₹50 Cr passes only in bull/0% churn; ₹100 Cr fails every case)'],['3 · Valuation','Control price ≤ ₹2,960 Cr and ≤ 18.2× retained ARR; total ≤ ₹4,000 Cr'],['4 · PAT','Consolidated PAT breakeven ≤5 yrs after exercise on the Board model (bull passes; base does not)'],['5 · FCF','Consolidated FCF breakeven ≤5 yrs after confirmed capital cost; cash ≥ ₹5,000 Cr; GD/EBITDA ≤ 1.5×'],['6 · Compliance','Clean AML/cyber/data audit; ISO 27001 and SOC 2 maintained; no unresolved regulatory matter']],[24,76],8,0.36);
  para(s,5.4,4.95,7.4,1.1,'**EXERCISE** all six clear · **HOLD** any gate open: Liminal can remain an arm’s-length associate indefinitely, and after control an arm’s-length subsidiary · **WALK AWAY / UNWIND** churn >45%, drag defeats returns, top-4 reject ownership, regulatory deterioration, price above reservation value — including after signing where CPs and termination rights allow.',8.5);
  banner(s,0.4,6.25,12.53,0.7,'**FINAL BOARD MESSAGE** — Paytm should not pay today for risks it can observe tomorrow. Secure the infrastructure through a 26% stake and a partnership; preserve the right, not the obligation, to acquire control; commit the remaining ₹2,960 Cr only after client trust, capital treatment, valuation and cash flow are proven. **Strategic access now. Control only when value is protected.**',NAVY,8.5);
  s.addNotes('Close on the six gates and the final message. Each gate is auditable by the committee with the model.');
}

// ================= 15 APPENDIX: MODEL =================
{ const s=slide('Appendix · Transaction model','Appendix:','EPS bridge, 10-year breakeven table and Phase-1 returns');
  box(s,0.4,1.25,4.3,5.7); panelTitle(s,0.4,1.25,4.3,'EPS / dilution bridge (year 1, full acquisition)',RED);
  [['₹7.50','Baseline diluted EPS (CF)',NAVY],['−0.12','New shares: 1.02 Cr at ₹1,855 (the “mechanical” ₹7.38)',AMBER],['−1.45','Foregone post-tax interest on ₹2,100 Cr cash (₹94.5 Cr, TA 6% yield)',RED],['−0.63','Post-churn Liminal loss ₹41 Cr, no group relief (TA)',RED],['₹5.29','Year-1 EPS, headline mix, 37.5% churn (−29%)',RED],['+1.08','Standalone MDR ₹69 Cr PAT — shown beside, never inside, the deal',BLUE]].forEach((t,i)=>{ const y=1.75+i*0.62; s.addShape(P.ShapeType.roundRect,{x:0.52,y,w:4.06,h:0.55,fill:{color:BG},line:{color:LINE,width:0.5},rectRadius:0.06}); s.addShape(P.ShapeType.roundRect,{x:0.6,y:y+0.1,w:0.7,h:0.35,fill:{color:t[2]},line:{color:t[2]},rectRadius:0.05}); s.addText(t[0],{x:0.6,y:y+0.1,w:0.7,h:0.35,fontFace:HF,fontSize:9,bold:true,color:WHITE,align:'center',valign:'middle',margin:0,isTextBox:true}); para(s,1.4,y+0.04,3.1,0.5,t[1],8.5,BODY,{valign:'middle'}); });
  para(s,0.55,5.55,4.0,1.3,'Phase 1: ₹7.50 → −₹0.73 foregone interest → +₹0.04 associate share → **₹6.81**. Not modelled: PPA amortisation; one-time integration ₹100 Cr (in FCF). Model: Python, 17 sections, reprints every figure in this deck.',8.5,MUTED);
  box(s,4.85,1.25,8.08,3.5); panelTitle(s,4.85,1.25,8.08,'10-year PAT & FCF table — full acquisition, case mix, 20% growth, 37.5% churn (₹ Cr; EPS ₹/share)',NAVY);
  tbl(s,4.95,1.7,7.88,[['Yr','Lim rev','Lim PAT','Incr PAT','EPS','EPS+MDR','Incr FCF','Cum FCF'],['1','165','−41','−136','5.29','6.36','−986','−3,086'],['2','198','15','−80','6.16','7.22','−830','−3,915'],['3','238','27','−68','6.34','7.40','−818','−4,733'],['4','285','43','−52','6.59','7.65','−802','−5,535'],['5','342','64','−30','6.92','7.98','−780','−6,315'],['6','411','77','−18','7.11','8.17','−768','−7,083'],['7','493','92','−2','7.35','8.41','−752','−7,835'],['8','591','111','16','7.63','8.69','−734','−8,569'],['9','709','133','39','7.97','9.04','−711','−9,280'],['10','851','160','65','8.38','9.44','−685','−9,965']],[7,12,12,13,11,13,15,17],7.5,0.225);
  para(s,4.95,4.4,7.8,0.3,'PAT breakeven year 8; FCF never (₹750 drag + ₹94.5 cost of funds exceed Liminal FCF every year). Cumulative includes the ₹2,100 Cr outlay and ₹100 Cr integration.',8,MUTED);
  box(s,4.85,4.9,8.08,2.05); panelTitle(s,4.85,4.9,8.08,'Phase-1 stake IRR — exit end-Y5 at multiple × ARR₅, 26% stake, no dividends (TA)',GREEN);
  tbl(s,4.95,5.35,4.3,[['Growth ↓ · exit multiple →','6×','10×','14×','18.2×'],['10%','−11.9%','−2.4%','4.4%','10.0%'],['20% (base)','−3.9%','6.5%','13.9%','20.0%'],['30% (bull)','4.1%','15.3%','23.4%','30.0%']],[32,17,17,17,17],8,0.3);
  para(s,9.4,5.35,3.45,1.5,'Against a 12% hurdle the stake earns its cost of capital at ≥20% growth and ≥13× exit, or ≥30% growth and ≥9×. Fundamental value of 26%: ₹456 Cr (base) – ₹951 Cr (bull) vs the ₹1,040 Cr ceiling — the premium buys blocking and access.',8.5);
  s.addNotes('Backup for the finance panel; the bridge shows where the blueprint’s 1.6% went.');
}

P.writeFile({fileName:'ETERNAL_Project_Satoshi_Gate.pptx'}).then(f=>console.log('written',f,'slides',n));
