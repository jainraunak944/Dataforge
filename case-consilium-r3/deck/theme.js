// Shared design system and helpers for the BGCC R3 deck (reference-informed, not an official FanCode brand spec)
const React = require('react'); const RDS = require('react-dom/server'); const sharp = require('sharp');
const T = { blue:'007AFF', deep:'0B66C3', dark:'18212B', pale:'EAF3FF', neutral:'F5F6F7', rule:'D9E0E7', orange:'EF5E16', paleOrange:'FDEFE6',
  grey:'5B6672', lightGrey:'8A95A1', white:'FFFFFF', green:'1E8E3E', paleGreen:'E8F5EC', red:'C62828', paleRed:'FBE9E7', ink:'18212B' };
const F = { head:'Poppins', body:'Inter' };
const W = 13.333, H = 7.5, MX = 0.35;
const iconCache = {};
async function iconData(Icon, color, px=256){ const key=(Icon.name||'')+color+px; if(iconCache[key]) return iconCache[key];
  const svg = RDS.renderToStaticMarkup(React.createElement(Icon,{color:'#'+color,size:px}));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer(); iconCache[key]='image/png;base64,'+buf.toString('base64'); return iconCache[key]; }
function linesFor(text, wIn, pt, bold){ const cw = pt*(bold?0.58:0.53)/72; const cpl = Math.max(1, Math.floor((wIn-0.12)/cw)); let n=0;
  String(text==null?'':text).split('\n').forEach(p=>{ n += Math.max(1, Math.ceil(p.length/cpl)); }); return n; }
function cellText(c){ if(c==null) return ''; if(typeof c!=='object') return String(c); if(Array.isArray(c.text)) return c.text.map(r=>r.text).join(''); return String(c.text==null?'':c.text); }
function rowHeight(cells, colW, pt, pad){ let mx=0.16; cells.forEach((c,i)=>{ const o=(c&&c.options)||{}; const fs=o.fontSize||pt; const span=o.colspan||1; let w=0; for(let k=0;k<span;k++) w+=colW[i+k]||0;
  mx=Math.max(mx, linesFor(cellText(c), w, fs, o.bold)*fs*1.22/72); }); return mx + (pad==null?0.1:pad); }
// Builds a table with computed row heights; returns total height
function table(slide, rows, o){ const pt=o.fontSize||11; const colW=o.colW; const heights = rows.map((r,i)=> o.rowH && o.rowH[i] ? o.rowH[i] : rowHeight(r, colW, pt, o.pad));
  const styled = rows.map((r,ri)=> r.map((c,ci)=>{ const cell = (c&&typeof c==='object'&&!Array.isArray(c)) ? {...c, options:{...(c.options||{})}} : {text:c==null?'':c, options:{}};
    const op=cell.options; op.fontFace = op.fontFace||F.body; op.fontSize = op.fontSize||pt; op.color = op.color||T.dark; op.valign=op.valign||'top'; op.align=op.align||'left';
    if(ri===0 && o.header!==false){ op.bold=true; op.fill = op.fill||{color:T.pale}; op.color = op.color===T.dark? T.deep : op.color; }
    if(o.zebra && ri>0 && ri%2===0 && !op.fill) op.fill={color:'FAFBFC'}; return cell; }));
  slide.addTable(styled, {x:o.x, y:o.y, w:colW.reduce((a,b)=>a+b,0), colW, rowH:heights, fontFace:F.body, fontSize:pt, color:T.dark, border:{type:'solid', pt:0.5, color:T.rule}, margin:[0.03,0.05,0.03,0.05], valign:'top', autoPage:false});
  return heights.reduce((a,b)=>a+b,0); }
function text(slide, str, o){ slide.addText(str, {isTextBox:true, fontFace:F.body, fontSize:11, color:T.dark, margin:0, valign:'top', ...o}); }
function rect(slide, x,y,w,h, o={}){ slide.addShape(o.round? 'roundRect':'rect', {x,y,w,h, fill:{color:o.fill||T.white}, line:o.line? {color:o.line, width:o.lw||0.75} : {color:o.fill||T.white, width:0}, rectRadius:o.round? (o.r||0.08):undefined, shadow:o.shadow}); }
function line(slide, x1,y1,x2,y2, o={}){ slide.addShape('line', {x:x1, y:y1, w:x2-x1, h:y2-y1, line:{color:o.color||T.rule, width:o.width||0.75, dashType:o.dash||'solid'}, flipV:o.flipV}); }
function circle(slide, x,y,d, fill, o={}){ slide.addShape('ellipse', {x,y,w:d,h:d, fill:{color:fill}, line:{color:o.line||fill, width:o.lw||0}}); }
function numCircle(slide, x,y,d,n,o={}){ circle(slide,x,y,d,o.fill||T.blue); text(slide, String(n), {x,y,w:d,h:d, align:'center', valign:'middle', bold:true, color:o.color||T.white, fontFace:F.head, fontSize:o.fontSize||10}); }
function sectionLabel(slide, x,y,w,str,o={}){ rect(slide, x, y+0.03, 0.05, (o.h||0.26)-0.06, {fill:o.color||T.blue}); text(slide, str, {x:x+0.12, y, w:w-0.12, h:o.h||0.26, fontFace:F.head, bold:true, fontSize:o.fontSize||11.5, color:o.color||T.deep, valign:'middle'}); }
// Title with accent runs: parts = [{t:'plain'},{t:'accent', a:true}]
function frame(slide, o){ const runs = o.title.map(p=>({text:p.t, options:{color:p.a? T.blue : T.dark}}));
  slide.addText(runs, {isTextBox:true, x:MX, y:0.22, w:W-2*MX-2.3, h:0.86, fontFace:F.head, bold:true, fontSize:o.titleSize||20, color:T.dark, margin:0, valign:'top', lineSpacingMultiple:1.0});
  rect(slide, MX, 1.10, 0.6, 0.045, {fill:T.blue});
  if(o.tag){ text(slide, o.tag, {x:W-MX-2.3, y:0.22, w:2.3, h:0.28, align:'right', fontFace:F.head, bold:true, fontSize:9.5, color:T.deep}); }
  if(o.sub){ text(slide, o.sub, {x:W-MX-2.3, y:0.48, w:2.3, h:0.4, align:'right', fontSize:8.5, color:T.grey}); }
  if(o.sources){ text(slide, o.sources, {x:MX, y:7.06, w:W-2*MX-0.5, h:0.42, fontSize:7.6, color:T.lightGrey, valign:'top', lineSpacingMultiple:1.0}); }
  if(o.page){ text(slide, String(o.page), {x:W-MX-0.5, y:7.12, w:0.5, h:0.3, fontSize:8, color:T.lightGrey, align:'right'}); } }
function takeaway(slide, str, o={}){ const y=o.y||6.56, h=o.h||0.46; rect(slide, MX, y, W-2*MX, h, {fill:T.paleOrange, round:true, r:0.06});
  text(slide, 'TAKEAWAY', {x:MX+0.14, y, w:1.0, h, fontFace:F.head, bold:true, fontSize:9.5, color:T.orange, valign:'middle'});
  text(slide, str, {x:MX+1.15, y:y+0.02, w:W-2*MX-1.3, h:h-0.04, fontSize:o.fontSize||9.8, color:T.dark, valign:'middle'}); }
function kpi(slide, x,y,w,h, o){ rect(slide, x,y,w,h,{fill:T.white, line:T.rule, round:true, r:0.06});
  text(slide, o.value, {x:x+0.14, y:y+0.08, w:w-0.28, h:0.42, fontFace:F.head, bold:true, fontSize:o.vs||20, color:o.color||T.blue, valign:'middle'});
  text(slide, o.label, {x:x+0.14, y:y+0.5, w:w-0.28, h:h-0.56, fontSize:o.ls||9, color:T.grey, valign:'top'}); }
function tagChip(slide, x,y,w,h,str,o={}){ rect(slide,x,y,w,h,{fill:o.fill||T.paleOrange, round:true, r:0.05}); text(slide,str,{x,y,w,h,align:'center',valign:'middle',fontFace:F.head,bold:true,fontSize:o.fontSize||8,color:o.color||T.orange}); }
const fmt = { inr:(x)=>'₹'+Math.round(x).toLocaleString('en-IN'), n:(x)=>Math.round(x).toLocaleString('en-IN'), lakh:(x)=>{ const v=x/1e5; return (v<0?'−':'')+'₹'+Math.abs(v).toFixed(1)+' lakh'; }, pct:(x,d=0)=>(x*100).toFixed(d)+'%' };
module.exports = { T,F,W,H,MX, iconData, table, text, rect, line, circle, numCircle, sectionLabel, frame, takeaway, kpi, tagChip, fmt, rowHeight, linesFor };
