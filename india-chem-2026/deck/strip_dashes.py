"""Post-build step for the v2 deck: remove every em/en dash from package XML.

pptxgenjs writes en-dash bullet glyphs into the default slide master's
placeholder list styles. No slide uses those placeholders, but the team's
house rule for this deck is zero U+2014/U+2013 anywhere in the file, so this
rewrites them to ASCII hyphens and verifies the whole package.

Usage: python3 strip_dashes.py <deck.pptx>
"""

import shutil
import sys
import zipfile

path = sys.argv[1]
tmp = path + ".tmp"

with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith((".xml", ".rels")):
            text = data.decode("utf-8")
            text = text.replace("—", "-").replace("–", "-")
            data = text.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmp, path)

remaining = 0
with zipfile.ZipFile(path) as z:
    for name in z.namelist():
        if name.endswith((".xml", ".rels")):
            t = z.read(name).decode("utf-8", errors="ignore")
            remaining += t.count("—") + t.count("–")
print(f"em/en dashes remaining in package XML: {remaining}")
sys.exit(0 if remaining == 0 else 1)
