// v2 generator: Wookies_BGCCR3.pptx (12 pages). Numbers from ../model/outputs/model_outputs.json (model v2).
const fs=require('fs'), path=require('path'), pptxgen=require('pptxgenjs');
const { T,F,W,H,MX,SZ, slideStart, text, rect, line, circle, chip, title, source, pageNo, conclusion, table, fmt, report, count } = require('./theme2');
const M = JSON.parse(fs.readFileSync(path.join(__dirname,'../model/outputs/model_outputs.json'),'utf8'));
const BF=M.base_full, B1=M.base_stage1, SC=M.scenarios, P=M.pathways, Et=M.E_t, Es=M.E_s, U=M.units;
const RF=Object.fromEntries(M.rows_base_full.map(r=>[r.id,r])), R1=Object.fromEntries(M.rows_base_stage1.map(r=>[r.id,r]));
const TEAM='Wookies', MEMBERS='Raunak Jain · Khushi Jha · Dhruv Mundra · Sambhav Khandelwal';
const r0=x=>Math.round(x); const L=(x,d=1)=>fmt.lakh(x,d); const c2a=r0(BF.c2_cac_attr), c2i=r0(BF.c2_cac_incr), gateCac=r0(BF.c2_value.m24);
const beAttr24=BF.breakeven.attr_m24, beIncr24=BF.breakeven.incr_m24, beAttr12=BF.breakeven.attr_m12; const gateUp=Math.ceil(beAttr24*100);
(async()=>{
const pres=new pptxgen(); pres.layout='LAYOUT_WIDE'; pres.author=TEAM; pres.company=TEAM; pres.title='Wookies: FanCode ATP growth (BGCC Case Consilium 2026, Round 3)';
// ============================================================ 1 COVER
{ const s=slideStart(pres,'p1');
  s.addShape('rtTriangle',{x:9.4,y:0,w:3.933,h:2.6,fill:{color:T.pale},line:{color:T.pale,width:0},flipH:true});
  rect(s, 8.35, 1.15, 4.5, 5.2, {fill:T.deep, round:true, r:0.14});
  const cx=8.75, cy=1.55, cw=3.7, ch=4.4, lc='9CC4F2';
  s.addShape('rect',{x:cx,y:cy,w:cw,h:ch,fill:{color:T.deep},line:{color:lc,width:1.5}});
  const sx=cw*0.11; line(s,cx+sx,cy,cx+sx,cy+ch,{color:lc,width:1.25}); line(s,cx+cw-sx,cy,cx+cw-sx,cy+ch,{color:lc,width:1.25});
  const sy=ch*0.24; line(s,cx+sx,cy+sy,cx+cw-sx,cy+sy,{color:lc,width:1.25}); line(s,cx+sx,cy+ch-sy,cx+cw-sx,cy+ch-sy,{color:lc,width:1.25});
  line(s,cx+cw/2,cy+sy,cx+cw/2,cy+ch-sy,{color:lc,width:1.25}); line(s,cx-0.2,cy+ch/2,cx+cw+0.2,cy+ch/2,{color:T.white,width:2.5}); circle(s,cx+cw*0.64,cy+ch*0.3,0.36,T.orange);
  text(s,'BGCC Case Consilium 2026  ·  Round 3  ·  Case partner: FanCode',{x:MX,y:1.05,w:7.5,h:0.35,fontFace:F.head,bold:true,fontSize:13,color:T.deep});
  s.addText([{text:'From ATP peaks to ',options:{color:T.dark}},{text:'retained paying subscribers',options:{color:T.blue}}],{isTextBox:true,x:MX,y:1.55,w:7.4,h:2.0,fontFace:F.head,bold:true,fontSize:40,margin:0,valign:'top',lineSpacingMultiple:0.98}); count('From ATP peaks to retained paying subscribers');
  rect(s,MX,3.62,0.8,0.05,{fill:T.blue});
  text(s,'Converting irregular ATP Tour interest into incremental, retained subscription growth for FanCode in India',{x:MX,y:3.85,w:7.3,h:0.8,fontSize:17,color:T.grey,lineSpacingMultiple:1.1});
  text(s,TEAM,{x:MX,y:4.85,w:7,h:0.6,fontFace:F.head,bold:true,fontSize:30,color:T.dark});
  text(s,MEMBERS,{x:MX,y:5.5,w:7.6,h:0.4,fontSize:16,color:T.dark});
  text(s,'Submission deck · 12 pages · prices in ₹, times in IST',{x:MX,y:6.9,w:7,h:0.3,fontSize:SZ.source,color:T.lightGrey,source:true});
}
// ============================================================ 2 EXECUTIVE SUMMARY
{ const s=slideStart(pres,'p2');
  title(s,[{t:'Buy intent, sell the season, prove the lift: '},{t:'₹4 lakh now, ₹6 lakh on evidence',a:true}],{tag:'Executive summary'});
  const bw=3.85, gap=0.39, y=1.65, h=1.95; const heads=['1 · Eligible audience','2 · Relevant paid occasion','3 · Repeat value'];
  const bodies=['Acquire never-paid tennis intent, reactivate lapsed 2025 buyers, cross-sell F1, MotoGP, LaLiga payers; defer the broad base.',
    'Sessions ₹29-₹39 with morning replay, tournaments ₹79-₹99, rest of season ₹199; each rung credited to the next.',
    'Race to Turin, a 30-day upgrade credit, a season-end bridge and a ₹349 loyalty price for 2027.'];
  heads.forEach((hd,i)=>{ const x=MX+i*(bw+gap); rect(s,x,y,bw,h,{fill:T.pale,round:true,r:0.1}); text(s,hd,{x:x+0.2,y:y+0.14,w:bw-0.4,h:0.36,fontFace:F.head,bold:true,fontSize:16,color:T.deep}); text(s,bodies[i],{x:x+0.2,y:y+0.58,w:bw-0.4,h:h-0.7,fontSize:15,lineSpacingMultiple:1.08});
    if(i<2) line(s,x+bw+0.04,y+h/2,x+bw+gap-0.04,y+h/2,{color:T.blue,width:2,arrow:'triangle'}); });
  const ky=3.8, kh=1.3; const kp=[[`₹${c2a} / ₹${c2i}`,'Attributed / incremental CAC per new payer, search + retargeting row only, base case',T.blue],
    [`₹${r0(B1.cost_per_new_incr)} to ₹${fmt.n(BF.cost_per_new_incr_incl_impl)}`,'Cost per incremental new payer: Stage 1 (₹4 lakh, no engineering) to the full ₹14 lakh incl. implementation',T.blue],
    [`${L(B1.net_incr.m24)} / ${L(BF.net_incr_incl_impl.m24)}`,'24-month incremental contribution net of spend: Stage 1 / full programme incl. ₹4 lakh engineering',T.red]];
  kp.forEach((k,i)=>{ const x=MX+i*(bw+gap); rect(s,x,ky,bw,kh,{fill:T.white,line:T.rule,round:true,r:0.1}); text(s,k[0],{x:x+0.2,y:ky+0.1,w:bw-0.4,h:0.45,fontFace:F.head,bold:true,fontSize:22,color:k[2]}); text(s,k[1],{x:x+0.2,y:ky+0.58,w:bw-0.4,h:0.68,fontSize:SZ.small,color:T.grey}); });
  rect(s,MX,5.35,W-2*MX,1.15,{fill:T.paleOrange,round:true,r:0.1});
  s.addText([{text:'Decision: ',options:{bold:true,color:T.orange}},{text:`commit Stage 1 (₹4 lakh: owned channels, reactivation, one paid search cell, 10% holdout). Release Stage 2 (₹6 lakh) and ₹4 lakh engineering only if day-45 incremental CAC ≤ ₹${gateCac} and upgrade share ≥ ${gateUp}%. The base case misses this gate: the pilot buys measurement, not a return.`,options:{color:T.dark}}],{isTextBox:true,x:MX+0.25,y:5.4,w:W-2*MX-0.5,h:1.05,fontFace:F.body,fontSize:15.5,margin:0,valign:'middle',lineSpacingMultiple:1.06});
  count(`Decision: commit Stage 1 (₹4 lakh: owned channels, reactivation, one paid search cell, 10% holdout). Release Stage 2 (₹6 lakh) and ₹4 lakh engineering only if day-45 incremental CAC ≤ ₹${gateCac} and upgrade share ≥ ${gateUp}%. The base case misses this gate: the pilot buys measurement, not a return.`);
  source(s,'Case facts CF1-CF19 from the Round 3 brief (see References). Model v2, base case; contribution before marketing excludes the fixed ATP rights fee. CAC = customer acquisition cost.'); pageNo(s,2);
}
// ============================================================ 3 SOLUTION 1: AUDIENCE MAP
{ const s=slideStart(pres,'p3');
  title(s,[{t:'Intent and payment state decide the action: '},{t:'acquire, reactivate, cross-sell or retain',a:true}],{tag:'Solution 1 of 8'});
  const x0=1.75,y0=1.6,x1=8.55,y1=5.6; rect(s,x0,y0,x1-x0,y1-y0,{fill:'FAFCFF',line:T.rule});
  const ylev=['All-sport pass (ATP included)','Paying ATP','Paying, no ATP','Lapsed 2025 buyer','Never paid']; const yy=i=>y0+(i+0.5)*(y1-y0)/5;
  ylev.forEach((l,i)=>{ text(s,l,{x:MX,y:yy(i)-0.2,w:1.2,h:0.4,fontSize:SZ.small,color:T.grey,align:'right',valign:'middle'}); line(s,x0,y0+(i+1)*(y1-y0)/5,x1,y0+(i+1)*(y1-y0)/5,{color:'EDF1F5',width:0.75}); });
  text(s,'Observable tennis intent →',{x:x0,y:y1+0.06,w:x1-x0,h:0.3,fontSize:SZ.small,color:T.grey,align:'center'}); text(s,'none',{x:x0,y:y1+0.06,w:1,h:0.3,fontSize:SZ.small,color:T.lightGrey}); text(s,'high',{x:x1-1,y:y1+0.06,w:1,h:0.3,fontSize:SZ.small,color:T.lightGrey,align:'right'});
  const xx=f=>x0+f*(x1-x0);
  const marks=[ [0.86,4,'1','Never paid, tennis signals (free highlights, page visits, 90 d)','ACQUIRE',T.orange],
    [0.62,3,'2','Lapsed 2025 ATP buyers','REACTIVATE (reported apart)',T.orange],
    [0.86,1,'3','ATP core: 2026 passes, season holders','REPEAT · UPGRADE · RENEW',T.blue],
    [0.3,2,'4','F1 · MotoGP · LaLiga pass holders, no ATP','CROSS-SELL A SESSION',T.orange],
    [0.72,0,'5','Monthly / Yearly holders','ENGAGE · RENEW, never new payers',T.blue],
    [0.08,4,'6','Broad base, no tennis signal (240M registered)','DEFER · BOUNDED TEST',T.grey]];
  marks.forEach(([fx,lev,n,lab,act,col])=>{ const cxm=xx(fx), cym=yy(lev); circle(s,cxm-0.19,cym-0.19,0.38,col); text(s,n,{x:cxm-0.19,y:cym-0.19,w:0.38,h:0.38,align:'center',valign:'middle',fontFace:F.head,bold:true,fontSize:13,color:T.white});
    const left = fx>0.5; const lw = (n==='6')? 2.2 : 2.6; const lx = left? cxm-0.3-lw : cxm+0.3; text(s,lab,{x:lx,y:cym-0.36,w:lw,h:0.36,fontSize:SZ.small,color:T.dark,align:left?'right':'left',valign:'bottom'}); const cwid=Math.max(1.6, act.length*0.105+0.35); chip(s, left? cxm-0.3-cwid : cxm+0.3, cym+0.04, cwid, 0.3, act, {fill: col===T.grey? T.neutral : (col===T.orange? T.paleOrange : T.pale), color: col===T.grey? T.grey : (col===T.orange? T.orange : T.deep), fontSize:12}); });
  text(s,'F1 weeknights\nMotoGP mornings\nLaLiga late nights',{x:xx(0.3)+0.3+2.45+0.15,y:yy(2)-0.32,w:1.9,h:0.64,fontSize:12,color:T.grey,valign:'middle',lineSpacingMultiple:1.0});
  const rx=9.0, rw=3.83; s.addChart(pres.ChartType.bar,[{name:'index',labels:['Ordinary week','India-friendly Masters week'],values:[100,150]}],{x:rx,y:1.55,w:rw,h:1.9,barDir:'col',chartColors:[T.blue],showValue:true,dataLabelPosition:'outEnd',dataLabelFontSize:12,dataLabelColor:T.dark,dataLabelFontFace:F.body,catAxisLabelFontSize:12,catAxisLabelColor:T.grey,catAxisLabelFontFace:F.body,valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},showLegend:false,showTitle:true,title:'Viewership index (case, CF3)',titleFontSize:12,titleColor:T.grey,titleFontFace:F.body,valAxisMaxVal:190,valAxisMinVal:0,barGapWidthPct:60}); count('Viewership index (case, CF3) Ordinary week India-friendly Masters week 100 150');
  text(s,[{text:'Priority. ',options:{bold:true,color:T.deep}},{text:'1 acquire, 2 reactivate, 3 cross-sell; ATP core is a retention audience.'}],{x:rx,y:3.65,w:rw,h:0.95,fontSize:SZ.body,lineSpacingMultiple:1.08});
  text(s,'Equal markers: no audience sizes are verified (CF1). Signals use first-party consented data only.',{x:rx,y:4.7,w:rw,h:0.8,fontSize:SZ.small,color:T.grey});
  conclusion(s,'Ordinary weeks are retention weeks: about 90% of their viewers are already fans (CF4).',{y:6.2});
  source(s,'Sources: CF1-CF4, CF17 (case brief); S3 ATP calendar; S15 LaLiga on FanCode. Adjacent-sport rows are existing-payer cross-sell and never enter the new-payer count.'); pageNo(s,3);
}
// ============================================================ 4 SOLUTION 2: TIMELINE
{ const s=slideStart(pres,'p4');
  title(s,[{t:'Owned channels build the occasion from T-7 days; '},{t:'paid conversion fires at T-48 hours',a:true}],{tag:'Solution 2 of 8'});
  const ax=2.45, bx=12.75, ay=1.9; line(s,ax,ay,bx,ay,{color:T.dark,width:1.5,arrow:'triangle'});
  const ticks=[['T-7 days',0.05],['T-48 hours',0.27],['Match time',0.5],['Next morning 07:00 IST',0.72],['Next event',0.93]]; const tx=f=>ax+f*(bx-ax);
  ticks.forEach(([l,f])=>{ line(s,tx(f),ay-0.08,tx(f),ay+0.08,{color:T.dark,width:1.5}); text(s,l,{x:tx(f)-1.15,y:1.52,w:2.3,h:0.3,fontSize:SZ.small,color:T.dark,align:'center',bold:true}); });
  const lanes=[['Owned / editorial',2.15],['Paid conversion',2.85],['After the view',3.55]]; lanes.forEach(([l,y])=>{ rect(s,MX,y,W-2*MX,0.62,{fill:T.neutral,round:true,r:0.06}); text(s,l,{x:MX+0.12,y,w:1.8,h:0.62,fontFace:F.head,bold:true,fontSize:SZ.small,color:T.deep,valign:'middle'}); });
  const box=(f1,f2,y,str,o={})=>{ const x=tx(f1), w=tx(f2)-x; rect(s,x,y+0.07,w,0.48,{fill:o.fill||T.pale,round:true,r:0.06}); text(s,str,{x:x+0.08,y:y+0.07,w:w-0.16,h:0.48,fontSize:12,color:o.color||T.dark,valign:'middle',align:'center'}); };
  box(0.0,0.2,2.15,'Race-to-Turin preview, IST times'); box(0.2,0.42,2.15,'Session / tournament offer to segments'); box(0.83,1.0,2.15,'Next-event push, day-20 credit reminder');
  box(0.24,0.52,2.85,'Search + retargeting, control IDs excluded',{fill:T.paleOrange,color:T.orange}); box(0.83,1.0,2.85,'No paid spend in ordinary weeks',{fill:T.white,color:T.grey});
  box(0.44,0.6,3.55,'Live: Shanghai night 17:00 IST'); box(0.62,0.85,3.55,'Spoiler-free replay push: Paris evening 00:00 IST → 07:00');
  text(s,'India-friendly occasion = live; overnight occasion = next-morning replay (times typical, illustrative)',{x:2.45,y:4.2,w:10.3,h:0.28,fontSize:12,color:T.grey,italic:true});
  const rows=[['Persona','Trigger','Offer → next paid step','Sample message (≤ 15 words)'],
    ['ATP core (paying)','After each final','Upgrade credit → ₹199',''],
    ['Marquee followers, never paid','T-48 h, Shanghai','₹89 pass; credit within 30 days',{text:'"Shanghai starts Wednesday, 17:00 IST. ₹89 covers all 12 days and counts toward your season."',options:{color:T.orange}}],
    ['F1 pass holders','Tue-Fri, never race Sunday','₹39 night session',''],
    ['MotoGP pass holders','Asian-swing mornings','₹39 day session',''],
    ['LaLiga late-night viewers','Fri / Sat, Paris and Turin weeks','₹39 evening session + 07:00 replay',{text:'"Kick-off at 1:30 AM? So is Paris. ₹39: watch live, or spoiler-free at 7 AM."',options:{color:T.orange}}]];
  table(s,rows,{x:MX,y:4.55,colW:[2.5,2.5,3.1,4.23],fontSize:SZ.small,rowH:[0.3,0.3,0.42,0.3,0.3,0.42]});
  source(s,'Sources: CF6, CF11 (case brief); S3 ATP 2026 calendar. Session start times are typical of recent editions and illustrative until the 2026 orders of play are published. Copy is original and subject to commercial approval.'); pageNo(s,4);
}
// ============================================================ 5 SOLUTION 3: PRICE LADDER
{ const s=slideStart(pres,'p5');
  title(s,[{t:'One public ladder, session to tournament to rest of season: '},{t:'each rung is credited to the next',a:true}],{tag:'Solution 3 of 8'});
  const base=6.05, bw=2.3; const blocks=[ {x:MX,h:2.35,name:'Session',price:'₹29 / ₹39',lines:['ATP 250/500 ₹29 · Masters, Finals ₹39','one session, live + 48 h replay'],tag:'proposed',tc:T.orange},
    {x:3.25,h:3.0,name:'Tournament',price:'₹79 / ₹89 / ₹99',lines:['ATP 250/500 · Masters 1000 · Finals','whole event, live + replays'],tag:'existing (case)',tc:T.grey},
    {x:6.0,h:3.7,name:'Rest of season',price:'₹199',lines:['5 Oct-22 Nov 2026 · all events','price already used late-season (S12)','new: credits in, loyalty renewal out'],tag:'existing price, new treatment',tc:T.orange} ];
  blocks.forEach(b=>{ const y=base-b.h; rect(s,b.x,y,bw,b.h,{fill:T.pale,round:true,r:0.1}); text(s,b.name,{x:b.x+0.15,y:y+0.12,w:bw-0.3,h:0.32,fontFace:F.head,bold:true,fontSize:16,color:T.deep}); text(s,b.price,{x:b.x+0.15,y:y+0.46,w:bw-0.3,h:0.5,fontFace:F.head,bold:true,fontSize: b.price.length>9? 20:28,color:T.dark,valign:'middle'});
    text(s,b.lines.join('\n'),{x:b.x+0.15,y:y+1.0,w:bw-0.3,h:b.h-1.45,fontSize:12,color:T.dark,lineSpacingMultiple:1.12}); chip(s,b.x+0.15,base-0.38,bw-0.3,0.27,b.tag,{fill:T.white,color:b.tc,fontSize:12}); });
  // credit arrows: from the top edge of the lower block into the next block, labels in the free space above the lower block
  line(s,1.65,3.7,1.65,3.45,{color:T.blue,width:2.25}); line(s,1.65,3.45,3.25,3.45,{color:T.blue,width:2.25,arrow:'triangle'});
  text(s,'₹29 paid + ₹50 = ₹79\nsession price credited to the same event',{x:MX-0.1,y:2.6,w:2.75,h:0.8,fontSize:12,color:T.deep,align:'center',bold:true,valign:'bottom'});
  line(s,4.4,3.05,4.4,2.6,{color:T.blue,width:2.25}); line(s,4.4,2.6,6.0,2.6,{color:T.blue,width:2.25,arrow:'triangle'});
  text(s,'₹89 paid + ₹110 = ₹199\ncap ₹99 · one credit per account · 30 days',{x:3.15,y:1.8,w:2.85,h:0.75,fontSize:12,color:T.deep,align:'center',bold:true,valign:'bottom'});
  rect(s,6.0,1.45,bw,0.62,{fill:T.white,line:T.rule,round:true,r:0.08}); text(s,'2027 season: ₹399 assumed list · ₹349 loyalty by 15 Jan (proposed)',{x:6.1,y:1.45,w:bw-0.2,h:0.62,fontSize:12,color:T.dark,valign:'middle'}); line(s,7.15,2.35,7.15,2.1,{color:T.blue,width:2,arrow:'triangle',dash:'dash'});
  const rx=8.7, rw=4.13;
  rect(s,rx,1.45,rw,0.9,{fill:T.neutral,round:true,r:0.08}); s.addText([{text:'Timing examples. ',options:{bold:true,color:T.deep}},{text:'Shanghai night, 17:00 IST: ₹39 session. Vienna evening, 00:00 IST: ₹29 session with the 07:00 replay.'}],{isTextBox:true,x:rx+0.15,y:1.45,w:rw-0.3,h:0.9,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'middle'}); count('Timing examples. Shanghai night, 17:00 IST: ₹39 session. Vienna evening, 00:00 IST: ₹29 session with the 07:00 replay.');
  rect(s,rx,2.45,rw,0.85,{fill:T.neutral,round:true,r:0.08}); s.addText([{text:'Folded or rejected. ',options:{bold:true,color:T.deep}},{text:'Replay rental folded into the session pass; player bundle rejected (participation cannot be guaranteed).'}],{isTextBox:true,x:rx+0.15,y:2.45,w:rw-0.3,h:0.85,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'middle'}); count('Folded or rejected. Replay rental folded into the session pass; player bundle rejected (participation cannot be guaranteed).');
  rect(s,rx,3.4,rw,0.8,{fill:T.paleOrange,round:true,r:0.08}); s.addText([{text:'Caveat. ',options:{bold:true,color:T.orange}},{text:"Monthly Pass ₹179 covers 'all applicable' tours (S11): confirm inclusions before promising F1 or LaLiga."}],{isTextBox:true,x:rx+0.15,y:3.4,w:rw-0.3,h:0.8,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'middle'}); count("Caveat. Monthly Pass ₹179 covers 'all applicable' tours (S11): confirm inclusions before promising F1 or LaLiga.");
  table(s,[['Product','Upfront price · period','ATP'],['FanCode tournament','₹79-₹99 · 1 event','Yes'],['FanCode rest of season','₹199 · 7 weeks','Yes'],['JioHotstar Mobile (S5)','₹79 · month','No'],['SonyLIV Mobile (S6)','₹699 · year','No']],{x:rx,y:4.32,colW:[1.95,1.65,0.53],fontSize:12,rowH:[0.32,0.32,0.32,0.32,0.32]});
  conclusion(s,'Ladder totals equal direct prices (₹29 + ₹50 = ₹79; ₹89 + ₹110 = ₹199), so no path undercuts a direct purchase.',{y:6.25});
  source(s,'Sources: CF15, CF16 (case); S5, S6, S10-S12. Prices assumed GST-inclusive. Tennis TV is not listed as a local competitor: India availability under FanCode exclusivity is unverified (S7-S8).'); pageNo(s,5);
}
// ============================================================ 6 SOLUTION 4: ECONOMICS
{ const s=slideStart(pres,'p6');
  title(s,[{t:'Rest-of-season entrants clear the acquisition hurdle; '},{t:'tournament entrants do not without upgrades',a:true}],{tag:'Solution 4 of 8'});
  const rowsC=[['Direct rest-of-season buyer (₹199)',P.fts_direct],['Upgrade via credit (₹89 + ₹110)',P.upgrade_via_credit],['Repeat buyer, no upgrade',P.repeat_no_upgrade],['Expected tournament entrant',Et],['Session entrant (₹35 blended)',Es],['Entry-only (₹89, never returns)',P.entry_only]];
  const lx=MX, lw=2.7, bx0=3.35, bx1=8.05, vmax=500, top=1.85, rh=0.6; const vx=v=>bx0+(v/vmax)*(bx1-bx0); const bot=top+rowsC.length*rh;
  text(s,'Contribution before marketing per entrant, ₹ (base case)',{x:MX,y:1.42,w:3.0,h:0.4,fontSize:12,color:T.grey,valign:'bottom'});
  rect(s,vx(150),top-0.1,vx(200)-vx(150),bot-top+0.1,{fill:T.paleOrange}); text(s,'case target ₹150-₹200',{x:vx(150)-0.75,y:top-0.4,w:1.9,h:0.28,fontSize:12,color:T.orange,align:'center'});
  line(s,vx(c2a),top-0.1,vx(c2a),bot+0.05,{color:T.deep,width:1.25,dash:'dash'}); text(s,`₹${c2a} attributed CAC`,{x:vx(c2a)-1.0,y:bot+0.06,w:2.0,h:0.26,fontSize:12,color:T.deep,align:'center'});
  line(s,vx(c2i),top-0.1,vx(c2i),bot+0.05,{color:T.orange,width:1.25,dash:'dash'}); text(s,`₹${c2i} incremental CAC`,{x:vx(c2i)+0.05,y:top-0.4,w:2.2,h:0.28,fontSize:12,color:T.orange});
  count(`case target ₹150-₹200 ₹${c2a} attributed CAC ₹${c2i} incremental CAC`);
  rowsC.forEach(([lab,v],i)=>{ const y=top+i*rh; text(s,lab,{x:lx,y,w:lw,h:rh-0.08,fontSize:SZ.small,color:T.dark,valign:'middle',align:'right'});
    rect(s,bx0,y+0.05,vx(v.m12)-bx0,0.2,{fill:T.midBlue}); text(s,fmt.inr(v.m12),{x:vx(v.m12)+0.05,y:y+0.02,w:0.7,h:0.26,fontSize:12,color:T.grey,valign:'middle'});
    rect(s,bx0,y+0.29,vx(v.m24)-bx0,0.2,{fill:T.deep}); text(s,fmt.inr(v.m24),{x:vx(v.m24)+0.05,y:y+0.26,w:0.7,h:0.26,fontSize:12,color:T.dark,valign:'middle',bold:true});
    const ok=v.m24>=c2i; chip(s,bx1+0.1,y+0.14,0.62,0.3, ok?'clears':'fails',{fill:ok?T.paleGreen:T.paleRed,color:ok?T.green:T.red,fontSize:12}); });
  line(s,bx0,top-0.1,bx0,bot,{color:T.dark,width:1});
  const ly=bot+0.45; rect(s,bx0,ly,0.3,0.16,{fill:T.midBlue}); text(s,'12 months',{x:bx0+0.36,y:ly-0.06,w:1.0,h:0.28,fontSize:12,color:T.grey}); rect(s,bx0+1.4,ly,0.3,0.16,{fill:T.deep}); text(s,'24 months (rights horizon)',{x:bx0+1.76,y:ly-0.06,w:2.2,h:0.28,fontSize:12,color:T.grey}); text(s,`clears: ≥ ₹${c2i} at 24 months`,{x:bx0+4.0,y:ly-0.06,w:2.7,h:0.28,fontSize:12,color:T.grey});
  const rx=8.85, rw=3.98;
  rect(s,rx,1.45,rw,1.3,{fill:T.pale,round:true,r:0.08}); s.addText([{text:'Break-even upgrade share, tournament entrants, 24 months: ',options:{bold:true,color:T.deep}},{text:`${fmt.pct(beAttr24)} at ₹${c2a} attributed, ${fmt.pct(beIncr24)} at ₹${c2i} incremental (not achievable); base assumption 20%. u* = (CAC − C entry) ÷ (C upgrade − C entry).`}],{isTextBox:true,x:rx+0.15,y:1.45,w:rw-0.3,h:1.3,fontFace:F.body,fontSize:12,margin:0,valign:'middle',lineSpacingMultiple:1.04}); count(`Break-even upgrade share, tournament entrants, 24 months: ${fmt.pct(beAttr24)} at ₹${c2a} attributed, ${fmt.pct(beIncr24)} at ₹${c2i} incremental (not achievable); base assumption 20%. u* = (CAC − C entry) ÷ (C upgrade − C entry).`);
  const LS=(x)=>fmt.lakhS(x); table(s,[['24-month net, ₹ lakh','Down','Base','Up'],['Stage 1: ₹4 lakh, no engineering',LS(SC.downside_stage1.net_incr.m24),LS(SC.base_stage1.net_incr.m24),LS(SC.upside_stage1.net_incr.m24)],['Full: ₹10 lakh + ₹4 lakh engineering',LS(SC.downside_full.net_incr_incl_impl.m24),LS(SC.base_full.net_incr_incl_impl.m24),LS(SC.upside_full.net_incr_incl_impl.m24)],['Full, attributed',LS(SC.downside_full.net_attr.m24),LS(SC.base_full.net_attr.m24),LS(SC.upside_full.net_attr.m24)]],{x:rx,y:2.9,colW:[1.58,0.8,0.8,0.8],fontSize:12,rowH:[0.32,0.46,0.46,0.34]});
  text(s,'Incremental basis, net of cannibalisation, cash at purchase; the fixed ATP rights fee is excluded, so this is not profit.',{x:rx,y:4.7,w:rw,h:1.0,fontSize:SZ.small,color:T.grey,lineSpacingMultiple:1.05});
  conclusion(s,`Base case: the full programme loses ${L(BF.net_incr_incl_impl.m24).replace('−','')} over the rights horizon; Stage 1 nearly breaks even (${L(B1.net_incr.m24)}).`,{y:6.25});
  source(s,'Sources: CF7-CF9, CF15, CF16, CF18 (case); model v2 (pathway mix 40/40/20, repeaters 1.5/2.5 more passes, loyalty renewal 35%/60%, 90% for 2028, GST 18%, 4% gateway and support, ₹2 per streaming hour). All values modelled.'); pageNo(s,6);
}
// ============================================================ 7 SOLUTION 5: JOURNEY
{ const s=slideStart(pres,'p7');
  title(s,[{t:'Retention runs on the next occasion: '},{t:'first purchase, next viewing, next paid decision, renewal',a:true}],{tag:'Solution 5 of 8'});
  const cw=2.85, gap=0.31, y=1.6, h=3.35; const stages=[
    {h:'1  First purchase',trig:'Any rung bought',act:'Pick 2 players and a viewing window; spoiler preference',out:'Qualified first view (≥ 20 min)',own:'CRM'},
    {h:'2  Next viewing occasion',trig:'Next session of the event',branch:['Live, 17:00 IST (India-friendly)','Morning replay 07:00, spoiler-free (overnight)'],out:'Second qualified view; next-event return',own:'Product · Editorial'},
    {h:'3  Next paid decision',trig:'Tournament ends; day 20 of the credit window',branch:['Credit upgrade ₹110 → ₹199 rest of season','Next tournament ₹79-₹99'],out:'Upgrade share; repeat purchase',own:'CRM · Commercial'},
    {h:'4  Expiry and renewal',trig:'22 Nov expiry; 2027 opens 5 Jan',branch:['Monthly Pass ₹179 (paid; inclusions to confirm)','2027 loyalty ₹349 by 15 Jan (paid)'],out:'Renewal (event-based); off-season replays, Next Gen Finals = engagement',own:'CRM · Commercial'} ];
  stages.forEach((st,i)=>{ const x=MX+i*(cw+gap); rect(s,x,y,cw,h,{fill:T.white,line:T.rule,round:true,r:0.1}); rect(s,x,y,cw,0.46,{fill:T.deep,round:true,r:0.1}); text(s,st.h,{x:x+0.15,y,w:cw-0.3,h:0.46,fontFace:F.head,bold:true,fontSize:14,color:T.white,valign:'middle'});
    let yy=y+0.58; s.addText([{text:'Trigger: ',options:{bold:true,color:T.deep}},{text:st.trig}],{isTextBox:true,x:x+0.15,y:yy,w:cw-0.3,h:0.5,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'top'}); count('Trigger: '+st.trig); yy+=0.58;
    if(st.branch){ st.branch.forEach((b,k)=>{ rect(s,x+0.15,yy,cw-0.3,0.5,{fill:k===0?T.pale:T.paleOrange,round:true,r:0.06}); text(s,b,{x:x+0.25,y:yy,w:cw-0.5,h:0.5,fontSize:12,valign:'middle',color:T.dark}); yy+=0.58; }); }
    else { s.addText([{text:'Action: ',options:{bold:true,color:T.deep}},{text:st.act}],{isTextBox:true,x:x+0.15,y:yy,w:cw-0.3,h:1.1,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'top'}); count('Action: '+st.act); yy+=1.16; }
    s.addText([{text:'Outcome: ',options:{bold:true,color:T.deep}},{text:st.out}],{isTextBox:true,x:x+0.15,y:yy,w:cw-0.3,h:0.72,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'top'}); count('Outcome: '+st.out);
    chip(s,x+0.15,y+h-0.4,cw-0.3,0.28,st.own,{fill:T.neutral,color:T.grey,fontSize:12});
    if(i<3) line(s,x+cw+0.03,y+1.6,x+cw+gap-0.03,y+1.6,{color:T.blue,width:2,arrow:'triangle'}); });
  rect(s,MX,5.15,6.0,1.05,{fill:T.pale,round:true,r:0.08}); s.addText([{text:'Portfolio branches. ',options:{bold:true,color:T.deep}},{text:'F1, MotoGP and LaLiga: an engagement nudge when already entitled; a paid purchase when not. Never new payers.'}],{isTextBox:true,x:MX+0.15,y:5.15,w:5.7,h:1.05,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'middle'}); count('Portfolio branches. F1, MotoGP and LaLiga: an engagement nudge when already entitled; a paid purchase when not. Never new payers.');
  rect(s,6.83,5.15,6.0,1.05,{fill:T.neutral,round:true,r:0.08}); s.addText([{text:'Controls. ',options:{bold:true,color:T.deep}},{text:'Entitlement checked before every send; caps 3 / 2 / 1 pushes a week (new payers / others / replay); refunds suppress offers 30 days.'}],{isTextBox:true,x:6.98,y:5.15,w:5.7,h:1.05,fontFace:F.body,fontSize:SZ.small,margin:0,valign:'middle'}); count('Controls. Entitlement checked before every send; caps 3 / 2 / 1 pushes a week (new payers / others / replay); refunds suppress offers 30 days.');
  conclusion(s,'Behavioural return, paid access and renewal are three different measures, reported separately (Solution 7).',{y:6.3});
  source(s,'Sources: CF6, CF7, CF17 (case); S3 calendar (2027 season opens 5 Jan; no Slam rights); S9 spoiler control exists in the ATP\'s own service; S10-S11 Monthly Pass scope; S13 weekly show.'); pageNo(s,7);
}
// ============================================================ 8 SOLUTION 6: ALLOCATION
{ const s=slideStart(pres,'p8');
  title(s,[{t:'₹10 lakh in two stages: '},{t:'₹4 lakh now, ₹6 lakh only if the gate is met',a:true}],{tag:'Solution 6 of 8'});
  const short={C1:'C1 Prospecting, bounded test',C2:'C2 Search + retargeting',C3:'C3 CRM activation',C3b:'C3b Reactivation',C4:'C4 Contests',C5:'C5 Editorial',C6:'C6 ESPN.in geo test',C7:'C7 Retention comms',C8:'C8 Measurement'};
  const chs=[...M.channels].sort((a,b)=>b.spend-a.spend); const labels=chs.map(c=>`${short[c.id]} · ${fmt.pct(c.spend/1e6)} · ₹${(c.spend/1e5).toFixed(1)}L`);
  s.addChart(pres.ChartType.bar,[{name:'Stage 1 (now)',labels,values:chs.map(c=>c.stage1/1e5)},{name:'Stage 2 (at gate G2)',labels,values:chs.map(c=>c.stage2/1e5)}],{x:MX,y:1.5,w:7.3,h:3.75,barDir:'bar',barGrouping:'stacked',chartColors:[T.deep,T.midBlue],showValue:true,dataLabelPosition:'ctr',dataLabelFormatCode:'0.0;−0.0;;',dataLabelFontSize:12,dataLabelColor:T.white,dataLabelFontFace:F.body,catAxisLabelFontSize:12,catAxisLabelColor:T.dark,catAxisLabelFontFace:F.body,valAxisLabelFontSize:12,valAxisLabelColor:T.grey,valAxisLabelFontFace:F.body,valAxisMaxVal:3.5,valAxisMinVal:0,valGridLine:{color:'EDF1F5',size:0.5},catGridLine:{style:'none'},showLegend:true,legendPos:'b',legendFontSize:12,legendFontFace:F.body,showTitle:true,title:'Allocation by row, ₹ lakh (total ₹10.0 lakh = 100%)',titleFontSize:12,titleColor:T.grey,titleFontFace:F.body,barGapWidthPct:45,catAxisOrientation:'maxMin'});
  count(labels.join(' ')+' Stage 1 (now) Stage 2 (at gate G2) Allocation by row, ₹ lakh (total ₹10.0 lakh = 100%)');
  const cacRows=['C1','C2','C3','C4']; const cl={C1:'C1 Prospecting',C2:'C2 Search',C3:'C3 CRM',C4:'C4 Contests'}; s.addChart(pres.ChartType.bar,[{name:'Attributed',labels:cacRows.map(i=>cl[i]),values:cacRows.map(i=>r0(RF[i].cac_new_attr))},{name:'Incremental',labels:cacRows.map(i=>cl[i]),values:cacRows.map(i=>r0(RF[i].cac_new_incr))}],{x:8.05,y:1.5,w:4.78,h:2.7,barDir:'bar',chartColors:[T.deep,T.orange],showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'"₹"#,##0',dataLabelFontSize:12,dataLabelColor:T.dark,dataLabelFontFace:F.body,catAxisLabelFontSize:12,catAxisLabelColor:T.dark,catAxisLabelFontFace:F.body,valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},valAxisMaxVal:3200,valAxisMinVal:0,showLegend:true,legendPos:'b',legendFontSize:12,legendFontFace:F.body,showTitle:true,title:'CAC per new payer, ₹ (rows with a new-payer denominator)',titleFontSize:12,titleColor:T.grey,titleFontFace:F.body,barGapWidthPct:40,catAxisOrientation:'maxMin'});
  count('C1 Prospecting, bounded test C2 Search + retargeting C3 CRM activation C4 Contests Attributed Incremental CAC per new payer, ₹ (rows with a new-payer denominator)');
  text(s,`Not directly attributed: C5, C6, C7, C8 (₹4.0 lakh) sit in programme cost with no CAC. Performance share: 65-70% today → ${fmt.pct(BF.performance_share)} (C1 + C2 + C4).`,{x:8.05,y:4.3,w:4.78,h:0.9,fontSize:SZ.small,color:T.grey,lineSpacingMultiple:1.05});
  const ty=5.35, th=0.95, tw=3.95, tg=0.24; const tiles=[[`Stage 1 (₹4 lakh): ${fmt.n(B1.new_attr)} attributed / ${fmt.n(B1.new_incr)} incremental new payers, ${fmt.n(B1.react_attr)} reactivated; ₹${r0(B1.cost_per_new_incr)} per incremental new payer.`,T.pale,T.dark],
    [`Full programme: ₹${r0(BF.cost_per_new_attr)} attributed, ₹${r0(BF.cost_per_new_incr)} incremental, ₹${fmt.n(BF.cost_per_new_incr_incl_impl)} with ₹4 lakh implementation, per new payer.`,T.pale,T.dark],
    [`Gate G2 (day 45): release Stage 2 paid rows only if C2 incremental CAC ≤ ₹${gateCac} and upgrade share ≥ ${gateUp}%. The base case fails this gate.`,T.paleOrange,T.dark]];
  tiles.forEach((t,i)=>{ const x=MX+i*(tw+tg); rect(s,x,ty,tw,th,{fill:t[1],round:true,r:0.08}); text(s,t[0],{x:x+0.15,y:ty,w:tw-0.3,h:th,fontSize:SZ.small,color:t[2],valign:'middle',lineSpacingMultiple:1.05}); });
  source(s,`Sources: CF9-CF13 (case); model v2 (CPM ₹120, CPC ₹7 / ₹5 / ₹7.5, CVR 1.5% / 4.0% / 7.0% / 7.8%, class mixes, 8% dedup, planning pools; all assumptions). ₹${gateCac} = 24-month contribution of a C2 entrant.`); pageNo(s,8);
}
// ============================================================ 9 SOLUTION 7: EXPERIMENT
{ const s=slideStart(pres,'p9');
  title(s,[{t:'A persistent 10% holdout turns attributed sales into '},{t:'measured incremental payers',a:true}],{tag:'Solution 7 of 8'});
  const bx=(x,y,w,h,str,o={})=>{ rect(s,x,y,w,h,{fill:o.fill||T.pale,round:true,r:0.08,line:o.line}); text(s,str,{x:x+0.12,y,w:w-0.24,h,fontSize:o.fs||SZ.small,color:o.color||T.dark,valign:'middle',align:o.align||'center',bold:o.bold}); };
  bx(MX,1.55,2.3,0.95,'Eligible users per segment (day 0), N',{bold:true}); line(s,2.8,2.02,3.2,2.02,{color:T.blue,width:2,arrow:'triangle'});
  bx(3.2,1.55,2.6,0.95,'Treatment 90% (N_T): ATP CRM + retargeting; control IDs excluded'); bx(3.2,2.65,2.6,1.0,'Holdout 10% (N_C): no ATP marketing; persistent; stratified by payment state, sport, viewing window',{fill:T.neutral});
  line(s,2.8,2.02,3.2,3.15,{color:T.blue,width:2,arrow:'triangle'});
  line(s,5.8,2.02,6.2,2.02,{color:T.blue,width:2,arrow:'triangle'}); line(s,5.8,3.15,6.2,3.15,{color:T.blue,width:2,arrow:'triangle'});
  bx(6.2,1.55,2.35,2.1,'Outcomes per eligible user at day 30 and day 90: new-payer rate p_T vs p_C; retained-payer rate r_T vs r_C');
  line(s,8.55,2.6,8.95,2.6,{color:T.blue,width:2,arrow:'triangle'});
  bx(8.95,1.55,3.88,2.1,'Incremental new payers = (p_T − p_C) × N_T\nIncremental CAC = spend ÷ incremental new payers\nIncremental D90 retained = (r_T − r_C) × N_T\nLift ≤ 0 → unfavourable, never a positive CAC',{fill:T.paleOrange,align:'left'});
  text(s,'Detecting a 50% lift on a 0.36% purchase rate with a 90/10 split needs about 128,000 eligible users (12,800 held out). Cohorts mature at day 90: 22 Dec-16 Jan for October buyers.',{x:MX,y:3.8,w:12.33,h:0.55,fontSize:SZ.small,color:T.grey,lineSpacingMultiple:1.05});
  table(s,[['Measure','Definition and window','Threshold'],
    [{text:'North star: incremental D90 retained payers ÷ incremental new payers',options:{bold:true,color:T.orange}},'Paid entitlement on day 90 and ≥ 1 qualified view (≥ 20 min, any FanCode content) in days 61-90; fixed window; treatment minus control','≥ 30%'],
    ['Incremental CAC, search + retargeting row','Row spend ÷ incremental new payers',`≤ ₹${gateCac}`],
    ['Upgrade share within 30 days','Rest-of-season purchases ÷ tournament entrants whose window closed',`≥ ${gateUp}% (break-even at ₹${c2a})`],
    ['Next-event return','Qualified view in the next tournament ÷ new payers whose next tournament ended','≥ 45%'],
    ['2027 ATP renewal (event-based)','Season purchases by 15 Feb ÷ eligible 2026 rest-of-season holders','≥ 50%']],{x:MX,y:4.45,colW:[3.6,6.3,2.43],fontSize:12,rowH:[0.3,0.5,0.3,0.3,0.36,0.3]});
  source(s,'Sources: CF9, CF17 (case). Sample sizes: two-sided α 0.05, power 0.80, 90/10 allocation, 0.36% baseline (model v2). Organic F1/football demand sits in the control group; subscribers already entitled to ATP are never counted as new.'); pageNo(s,9);
}
// ============================================================ 10 SOLUTION 8: ROADMAP
{ const s=slideStart(pres,'p10');
  title(s,[{t:'Release ₹4 lakh now; '},{t:'₹6 lakh and engineering wait for measured lift at day 45',a:true}],{tag:'Solution 8 of 8'});
  const pw=2.95, pg=0.18, py=1.55; const phases=[['Days 0-14 · 23 Sep-6 Oct',['CRM counts, segments, holdout (Growth analytics)','Rate card, credits, refunds (Commercial, Legal)','Contests (Community); replay v0 (CRM)'],'₹4 lakh Stage 1 committed'],
    ['Days 15-45 · 7 Oct-6 Nov',['Paid search cell at T-48 h (Growth)','Ladder live; reactivation wave (CRM)','Race to Turin on the weekly show (Editorial)'],'No engineering yet'],
    ['Days 46-90 · 7 Nov-21 Dec',['Season-end bridge; loyalty renewal (CRM, Commercial)','If G2 passed: ₹6 lakh Stage 2 + ₹4 lakh engineering (Product)','Day-30 / 45 readouts (Analytics)'],'Spend released only on G2'],
    ['Days 91-120 · 22 Dec-20 Jan',['Day-90 readout, Sept-Oct cohorts (Analytics)','2027 season-start push (CRM)','Feb-Mar 2027 wave decision'],'Scale decision at G3']];
  phases.forEach((p,i)=>{ const x=MX+i*(pw+pg); s.addText(p[0],{shape: i===0?'homePlate':'chevron', x,y:py,w:pw,h:0.55,fill:{color:T.deep},line:{color:T.deep,width:0},fontFace:F.head,bold:true,fontSize:12.5,color:T.white,align:'center',valign:'middle',margin:0}); count(p[0]);
    rect(s,x,py+0.7,pw,2.3,{fill:T.white,line:T.rule,round:true,r:0.08}); s.addText(p[1].map((d,k)=>({text:d,options:{bullet:true,breakLine:k<p[1].length-1}})),{isTextBox:true,x:x+0.12,y:py+0.8,w:pw-0.24,h:1.7,fontFace:F.body,fontSize:12,color:T.dark,margin:0,valign:'top',paraSpaceAfter:4}); count(p[1].join(' '));
    chip(s,x+0.12,py+2.6,pw-0.24,0.3,p[2],{fill:i===0?T.paleOrange:T.neutral,color:i===0?T.orange:T.grey,fontSize:12}); });
  const gates=[['G1 · day 14','holdout live; rate card signed'],['G2 · day 45',`CAC ≤ ₹${gateCac} incremental and upgrade ≥ ${gateUp}%: release; else owned rows only`],['G3 · day 90','next-event return ≥ 45%; D90 for cohorts observed 90 days']];
  line(s,MX,py+3.38,W-MX,py+3.38,{color:T.rule,width:1});
  gates.forEach((g,i)=>{ const x=MX+(i+1)*(pw+pg)-pg/2-0.7; chip(s,x+0.05,py+3.2,1.3,0.36,g[0],{fill:T.orange,color:T.white,fontSize:12}); text(s,g[1],{x:x-0.75,y:py+3.62,w:2.9,h:0.62,fontSize:12,color:T.dark,align:'center'}); });
  rect(s,MX,5.95,6.4,0.85,{fill:T.neutral,round:true,r:0.08}); s.addText([{text:'Risks. ',options:{bold:true,color:T.deep}},{text:'Cannibalisation → one credit per account, loyalty price for prior holders. Weak lift → stop rules; owned rows continue. Withdrawals → event-defined SKUs, automatic credits.'}],{isTextBox:true,x:MX+0.12,y:5.95,w:6.15,h:0.85,fontFace:F.body,fontSize:12,margin:0,valign:'middle'}); count('Risks. Cannibalisation → one credit per account, loyalty price for prior holders. Weak lift → stop rules; owned rows continue. Withdrawals → event-defined SKUs, automatic credits.');
  rect(s,7.1,5.95,5.73,0.85,{fill:T.paleOrange,round:true,r:0.08}); s.addText([{text:'Decision. ',options:{bold:true,color:T.orange}},{text:`₹14 lakh maximum exposure; ₹4 lakh committed now. Base 24-month incremental net: Stage 1 ${L(B1.net_incr.m24)}, full ${L(BF.net_incr_incl_impl.m24)}: Stage 2 is released only if results beat the base case.`}],{isTextBox:true,x:7.22,y:5.95,w:5.5,h:0.85,fontFace:F.body,fontSize:12,margin:0,valign:'middle'}); count(`Decision. ₹14 lakh maximum exposure; ₹4 lakh committed now. Base 24-month incremental net: Stage 1 ${L(B1.net_incr.m24)}, full ${L(BF.net_incr_incl_impl.m24)}: Stage 2 is released only if results beat the base case.`);
  source(s,'Sources: CF18 (rights through 2028); S3 calendar. Engineering (spoiler-free surfaces, replay automation, checkout credits) and ATP Media clip rights are dependencies released at G2. Implementation budget is an assumption.'); pageNo(s,10);
}
// ============================================================ 11-12 REFERENCES
const ledger=fs.readFileSync(path.join(__dirname,'../research/source_ledger.csv'),'utf8');
function parseCSV(txt){ const out=[]; let row=[],cell='',q=false; for(let i=0;i<txt.length;i++){ const ch=txt[i]; if(q){ if(ch==='"'){ if(txt[i+1]==='"'){cell+='"';i++;} else q=false; } else cell+=ch; } else { if(ch==='"') q=true; else if(ch===','){row.push(cell);cell='';} else if(ch==='\n'){row.push(cell);out.push(row);row=[];cell='';} else if(ch!=='\r') cell+=ch; } } if(cell||row.length){row.push(cell);out.push(row);} return out; }
const Lg=parseCSV(ledger); const hdr=Lg[0]; const srcs=Lg.slice(1).filter(r=>r.length>=10).map(r=>Object.fromEntries(hdr.map((h,i)=>[h,r[i]])));
const shortTitle={S1:'FanCode signs exclusive ATP Tour multi-year broadcast deal',S2:'FanCode strikes exclusive multi-year ATP Tour deal (56 events)',S3:'What is the 2026 ATP Tour calendar?',S4:'TV schedule: broadcaster list (India: FanCode)',S5:'JioHotstar introduces monthly plans across tiers (prices from 28 Jan 2026)',S6:'What are the types of subscription available? / How much does Sony LIV cost?',S7:'How much does Tennis TV cost?',S8:'Tennis TV app listing, India storefront (in-app prices)',S9:'What is Spoiler Mode on Tennis TV?',S10:'FanCode subscription page (Monthly Pass ₹179)',S11:'FanCode terms and conditions (pass definitions)',S12:'Indian Tennis Daily posts on FanCode ATP passes (X, Instagram)',S13:'ATP Tour This Week, episode 35 (weekly show page)',S14:'F1 2026: FanCode and F1 TV India subscription prices',S15:'LALIGA 2026-27: live on FanCode (tour page)',S16:'Case Consilium 2026 competition page (Unstop)',S17:'Round 3 case brief (not available in the build session)'};
const shortDate={S1:'Jan 2026',S2:'Jan 2026',S3:'27 Nov 2025',S4:'2026',S5:'21 Jan 2026',S6:'undated help article',S7:'undated help article',S8:'current listing',S9:'undated help article',S10:'current page',S11:'current page',S12:'Mar 2026 and in-season 2026',S13:'2026',S14:'early 2026',S15:'2026',S16:'2026, not reachable from the build environment',S17:'case PDF'};
function refEntry(s, x, y, w, src){ const url=(src.url||'').split(' ; ')[0]; const runs=[{text:src.id+'  ',options:{bold:true,color:T.deep}},{text:src.organisation+'. ',options:{bold:true}}, url.startsWith('http')? {text:shortTitle[src.id]||src.title,options:{hyperlink:{url},color:T.deep}} : {text:shortTitle[src.id]||src.title,options:{color:T.dark}}, {text: src.id==='S17'? '. Facts quoted via the master prompt register with PDF page indices; verify before upload.' : `. ${shortDate[src.id]||src.published_or_updated}; accessed 21 Sep 2026.`,options:{color:T.grey}}];
  s.addText(runs,{isTextBox:true,x,y,w,h:0.62,fontFace:F.body,fontSize:SZ.ref,color:T.dark,margin:0,valign:'top',lineSpacingMultiple:1.05}); }
{ const s=slideStart(pres,'p11'); title(s,[{t:'References (1 of 2): '},{t:'sources',a:true}],{tag:'References'});
  const colW=(W-2*MX-0.4)/2; srcs.slice(0,10).forEach((src,i)=>{ const col=i<5?0:1; refEntry(s, MX+col*(colW+0.4), 1.6+(i%5)*0.95, colW, src); });
  text(s,'Evidence cut-off: sources published on or before 19 September 2026, accessed 21 September 2026 through search-index copies (the build environment could not open the sites directly). Case facts (CF) come from the Round 3 brief and govern where public figures differ.',{x:MX,y:6.45,w:W-2*MX,h:0.7,fontSize:SZ.ref,color:T.grey,source:true}); pageNo(s,11); }
{ const s=slideStart(pres,'p12'); title(s,[{t:'References (2 of 2): '},{t:'sources, definitions, assumptions',a:true}],{tag:'References'});
  const colW=(W-2*MX-0.4)/2; srcs.slice(10).forEach((src,i)=>{ const col=i<4?0:1; refEntry(s, MX+col*(colW+0.4), 1.5+(i%4)*0.78, colW, src); });
  const dy=5.05; text(s,'Definitions',{x:MX,y:dy-0.35,w:4,h:0.3,fontFace:F.head,bold:true,fontSize:13,color:T.deep});
  const defs=[['New payer','First-ever FanCode payment is an ATP pass. Reactivated = a lapsed 2025 buyer returning. Existing-payer ATP purchase = a current F1, MotoGP, LaLiga or Monthly payer buying ATP.'],['CAC','Attributed = row spend ÷ attributed new payers. Incremental = spend ÷ (attributed × validated share from the holdout). Programme cost per payer uses the whole budget, with or without implementation.'],['Contribution','Price ÷ 1.18 (GST assumed included) − 4% of gross (gateway, support) − ₹2 per streaming hour; cash basis; the fixed ATP rights fee is excluded.'],['Horizons','90 days, 12 and 24 months from a 7 Oct 2026 purchase; 24 months sits inside the rights term to 2028 (CF18).']]; 
  defs.forEach((d,i)=>{ s.addText([{text:d[0]+'. ',options:{bold:true,color:T.deep}},{text:d[1]}],{isTextBox:true,x:MX,y:dy+i*0.4,w:W-2*MX,h:0.4,fontFace:F.body,fontSize:SZ.ref,color:T.dark,margin:0,valign:'top'}); });
  text(s,'Assumptions and limits: CRM pools (150k / 120k / 40k / 60k), CPC, CPM, CVR, class mixes, pathway shares, renewals and session start times are model assumptions. Unverified: the case PDF (quoted via the master prompt register), Tennis TV live availability in India, the 2027 season tariff, Monthly Pass tour inclusions. ATP = Association of Tennis Professionals; CRM = customer relationship management; D90 = day 90 after first purchase; IST = India Standard Time.',{x:MX,y:6.62,w:W-2*MX-0.5,h:0.8,fontSize:SZ.ref,color:T.grey,source:true}); pageNo(s,12); }
const out=path.join(__dirname,'out',`${TEAM}_BGCCR3.pptx`); await pres.writeFile({fileName:out}); console.log('written',out);
const rep=report(); Object.entries(rep).forEach(([k,v])=>console.log(`${k}: ${v.words} words (+${v.sources} source)${v.words>220?'  <-- OVER 220':(v.words>180?'  (over 180)':'')}`));
})().catch(e=>{console.error(e);process.exit(1);});
