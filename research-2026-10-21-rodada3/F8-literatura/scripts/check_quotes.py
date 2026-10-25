#!/usr/bin/env python3
"""Confere que cada trecho entre aspas das linhas de rows.py existe no arquivo local (normalizando espaços, ligaduras e aspas)."""
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
