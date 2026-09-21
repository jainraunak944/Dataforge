// v2 design system: white/blue consulting style, readable sizes, per-slide word counting
const T = { blue:'007AFF', deep:'0B66C3', dark:'18212B', pale:'EAF3FF', rule:'D9E0E7', neutral:'F5F6F7', orange:'EF5E16', paleOrange:'FDEFE6', grey:'5B6672', lightGrey:'8A95A1', white:'FFFFFF', green:'1E8E3E', paleGreen:'E3F3E7', red:'C62828', paleRed:'FBE9E7', midBlue:'A9CBF2' };
const F = { head:'Poppins', body:'Inter' };
const W = 13.333, H = 7.5, MX = 0.5;
const SZ = { title:26, body:16, label:12.5, small:12, source:10, tag:12, ref:11 };
const counts = {}; let current = null;
function slideStart(pres, key){ current = key; counts[key] = {words:0, sources:0}; const s = pres.addSlide(); s.background={color:T.white}; return s; }
function wc(str){ return String(str||'').trim().split(/\s+/).filter(w=>/[A-Za-z0-9₹%]/.test(w)).length; }
function runsText(v){ if(v==null) return ''; if(typeof v!=='object') return String(v); if(Array.isArray(v)) return v.map(r=>runsText(r.text!==undefined? r.text : r)).join(' '); return runsText(v.text); }
function count(v, isSource){ if(!current) return; const n = wc(runsText(v)); if(isSource) counts[current].sources += n; else counts[current].words += n; }
function text(slide, str, o={}){ count(str, o.source); slide.addText(str, {isTextBox:true, fontFace:o.fontFace||F.body, fontSize:o.fontSize||SZ.body, color:o.color||T.dark, margin:0, valign:o.valign||'top', ...o}); }
function rect(slide, x,y,w,h, o={}){ slide.addShape(o.round? 'roundRect':'rect', {x,y,w,h, fill: o.fill? {color:o.fill} : {color:T.white, transparency:100}, line: o.line? {color:o.line, width:o.lw||1} : {color:o.fill||T.white, width:0}, rectRadius:o.round? (o.r||0.1):undefined}); }
function line(slide, x1,y1,x2,y2, o={}){ const props={x:Math.min(x1,x2), y:Math.min(y1,y2), w:Math.abs(x2-x1), h:Math.abs(y2-y1), line:{color:o.color||T.rule, width:o.width||1, dashType:o.dash||'solid', endArrowType:o.arrow, beginArrowType:o.beginArrow}}; if((x2<x1)!==(y2<y1)) props.flipV=true; slide.addShape('line', props); }
function circle(slide, x,y,d, fill, o={}){ slide.addShape('ellipse', {x,y,w:d,h:d, fill:{color:fill}, line:{color:o.line||fill, width:o.lw||0}}); }
function chip(slide, x,y,w,h, str, o={}){ rect(slide,x,y,w,h,{fill:o.fill||T.pale, round:true, r:0.08}); text(slide,str,{x,y,w,h,align:'center',valign:'middle',fontFace:F.head,bold:true,fontSize:o.fontSize||12,color:o.color||T.deep}); }
function title(slide, parts, o={}){ const runs = parts.map(p=>({text:p.t, options:{color:p.a? T.blue : T.dark}})); count(parts.map(p=>p.t).join(' '));
  slide.addText(runs, {isTextBox:true, x:MX, y:0.38, w:W-2*MX-2.0, h:0.95, fontFace:F.head, bold:true, fontSize:o.size||SZ.title, margin:0, valign:'top', lineSpacingMultiple:0.98});
  if(o.tag){ text(slide, o.tag, {x:W-MX-1.9, y:0.42, w:1.9, h:0.3, align:'right', fontFace:F.head, bold:true, fontSize:SZ.tag, color:T.deep}); } }
function source(slide, str){ text(slide, str, {x:MX, y:6.9, w:W-2*MX-0.4, h:0.42, fontSize:SZ.source, color:T.grey, valign:'top', source:true}); }
function pageNo(slide, n){ slide.addText(String(n), {isTextBox:true, x:W-MX-0.4, y:6.95, w:0.4, h:0.3, fontFace:F.body, fontSize:SZ.source, color:T.lightGrey, align:'right', margin:0}); }
function conclusion(slide, str, o={}){ const y=o.y||6.35; rect(slide, MX, y, W-2*MX, 0.42, {fill:T.paleOrange, round:true, r:0.08}); text(slide, str, {x:MX+0.2, y, w:W-2*MX-0.4, h:0.42, fontSize:o.fontSize||14, color:T.dark, valign:'middle', bold:false}); }
function table(slide, rows, o){ const pt=o.fontSize||SZ.small; const colW=o.colW; rows.forEach(r=>r.forEach(c=>count(c)));
  const styled = rows.map((r,ri)=> r.map(c=>{ const cell = (c&&typeof c==='object'&&!Array.isArray(c)) ? {...c, options:{...(c.options||{})}} : {text:c==null?'':c, options:{}}; const op=cell.options;
    op.fontFace=op.fontFace||F.body; op.fontSize=op.fontSize||pt; op.color=op.color||T.dark; op.valign=op.valign||'middle'; op.align=op.align||'left';
    if(ri===0 && o.header!==false){ op.bold=true; op.fill=op.fill||{color:T.pale}; op.color= op.color===T.dark? T.deep : op.color; } return cell; }));
  slide.addTable(styled, {x:o.x, y:o.y, w:colW.reduce((a,b)=>a+b,0), colW, rowH:o.rowH, fontFace:F.body, fontSize:pt, color:T.dark, border:{type:'solid', pt:0.75, color:T.rule}, margin:[0.04,0.08,0.04,0.08], valign:'middle', autoPage:false}); }
const fmt = { inr:(x)=>'₹'+Math.round(x).toLocaleString('en-IN'), n:(x)=>Math.round(x).toLocaleString('en-IN'), lakh:(x,d=1)=>{ const v=x/1e5; return (v<0?'−':'')+'₹'+Math.abs(v).toFixed(d)+' lakh'; }, lakhS:(x,d=1)=>{ const v=x/1e5; return (v<0?'−':'+')+'₹'+Math.abs(v).toFixed(d)+'L'; }, pct:(x,d=0)=>(x*100).toFixed(d)+'%' };
function report(){ return counts; }
module.exports = { T,F,W,H,MX,SZ, slideStart, text, rect, line, circle, chip, title, source, pageNo, conclusion, table, fmt, report, count };
