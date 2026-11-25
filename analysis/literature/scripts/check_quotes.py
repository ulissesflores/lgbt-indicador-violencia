#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Check that every quoted passage in the evidence rows exists in its local file.

For each row of rows.py it extracts the quoted passages and searches them in the text of the
local file (pdftotext for PDFs, tag-stripped text for HTML or XML) after normalizing spaces,
ligatures, dashes and quotation marks, tolerating editorial brackets and ellipses. It prints
each passage not found and a final verdict.

Inputs
------
- analysis/literature/scripts/rows.py
- the local source files listed in rows.py (not tracked in git when large)
- poppler tool pdftotext on the PATH

Outputs
-------
- prints "NAO ACHADO" lines for missing passages and a final "ok" or the count to stdout

Usage
-----
python3 -I analysis/literature/scripts/check_quotes.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Confere que cada trecho entre aspas das linhas de rows.py existe no arquivo local (normalizando espaços, ligaduras e aspas).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import sys, os, re, subprocess, html, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import rows
def norm(t):
    t=unicodedata.normalize("NFKC",t).replace("\u00ad","")
    t=t.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("‐","-").replace("‑","-").replace("–","-").replace("−","-")
    t=re.sub(r"-\n(?=[a-zà-ú])","",t)
    t=re.sub(r"\s+"," ",t)
    return t.lower()
cache={}
def text(p):
    if p in cache: return cache[p]
    if p.endswith(".pdf"):
        t=subprocess.run(["pdftotext",p,"-"],capture_output=True,text=True).stdout
    else:
        raw=open(p,'rb').read()
        try: t=raw.decode('utf-8')
        except UnicodeDecodeError: t=raw.decode('latin-1')
        t=re.sub(r"<script.*?</script>|<style.*?</style>","",t,flags=re.S); t=html.unescape(re.sub(r"<[^>]+>"," ",t))
    cache[p]=norm(t); return cache[p]
bad=0
for r in rows.ROWS:
    segs=re.findall(r'"([^"]{12,})"',r["quote"])
    for s in segs:
        for part in re.split(r"\s*\.\.\.\s*",s):
            part=part.strip(" .;,")
            if len(part)<12: continue
            pn=norm(part)
            pn=re.sub(r"\[[^\]]*\]","",pn)
            if pn not in text(r["file"]):
                # tolera colchetes editoriais dividindo
                subs=[x for x in re.split(r"\[[^\]]*\]",norm(part)) if len(x.strip())>10]
                if all(x.strip() in text(r["file"]) for x in subs) and subs: continue
                bad+=1; print("NAO ACHADO",r["id"],"::",part[:110])
print("ok" if not bad else f"{bad} trechos nao achados")
