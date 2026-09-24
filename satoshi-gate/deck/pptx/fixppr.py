import zipfile, re, shutil, sys
src=__import__('sys').argv[1]; tmp='fixed.pptx'
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
pPr=re.compile(r'<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)',re.S); para=re.compile(r'<a:p>(.*?)</a:p>',re.S); fixed=0
for it in zin.infolist():
    data=zin.read(it.filename)
    if it.filename.startswith('ppt/slides/slide') and it.filename.endswith('.xml'):
        def fix(m):
            global fixed
            body=m.group(1); blocks=pPr.findall(body)
            if len(blocks)<=1: return m.group(0)
            first=True; out=[]; pos=0
            for mm in pPr.finditer(body):
                out.append(body[pos:mm.start()])
                if first: out.append(mm.group(0)); first=False
                else: fixed+=1
                pos=mm.end()
            out.append(body[pos:]); return '<a:p>'+''.join(out)+'</a:p>'
        data=para.sub(fix,data.decode()).encode()
    zout.writestr(it,data)
zout.close(); shutil.move(tmp,src); print('removed duplicate pPr blocks:',fixed)
