"""Recalculate an xlsx with LibreOffice via Python-UNO over a named pipe, then report formula errors.
Usage: python3 uno_recalc.py file.xlsx [timeout]"""
import os, sys, time, subprocess, uuid, json
from pathlib import Path
import uno
from com.sun.star.beans import PropertyValue

def prop(name, value):
    p = PropertyValue(); p.Name = name; p.Value = value; return p

def main():
    path = Path(sys.argv[1]).absolute()
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    pipe = "lo_pipe_" + uuid.uuid4().hex[:8]
    profile = f"/tmp/lo_prof_{uuid.uuid4().hex[:8]}"
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    proc = subprocess.Popen(["soffice", "--headless", "--norestore", "--nologo", f"-env:UserInstallation=file://{profile}",
                             f"--accept=pipe,name={pipe};urp;StarOffice.ComponentContext"], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    t0 = time.time()
    while time.time() - t0 < 60:
        try:
            ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext"); break
        except Exception:
            time.sleep(0.5)
    if ctx is None:
        proc.kill(); print(json.dumps({"error": "could not connect to soffice"})); return 1
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    url = uno.systemPathToFileUrl(str(path))
    t1 = time.time()
    doc = desktop.loadComponentFromURL(url, "_blank", 0, (prop("Hidden", True),))
    t2 = time.time()
    doc.calculateAll()
    t3 = time.time()
    doc.storeToURL(url, (prop("FilterName", "Calc MS Excel 2007 XML"),))
    t4 = time.time()
    doc.close(True)
    try:
        desktop.terminate()
    except Exception:
        pass
    proc.wait(timeout=30)
    # error scan
    from openpyxl import load_workbook
    wb = load_workbook(str(path), data_only=True)
    errs = {}
    total = 0; nform = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith("#") and any(e in v for e in ("#VALUE!", "#DIV/0!", "#REF!", "#NAME?", "#NULL!", "#NUM!", "#N/A")):
                    errs.setdefault(v, []).append(f"{ws.title}!{c.coordinate}"); total += 1
    print(json.dumps({"status": "errors_found" if total else "success", "total_errors": total,
                      "load_s": round(t2 - t1, 1), "calc_s": round(t3 - t2, 1), "save_s": round(t4 - t3, 1),
                      "error_summary": {k: v[:40] for k, v in errs.items()}}, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
