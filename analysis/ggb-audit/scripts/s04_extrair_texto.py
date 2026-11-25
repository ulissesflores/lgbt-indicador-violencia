# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Extract the visible text of each downloaded page and flag errors, name and city presence.

For every saved HTML page it extracts the visible text and flags (a) error pages, soft 404s and
offline Wayback pages, (b) whether the name or nickname of the victim appears, (c) whether the
city appears. Raw text stays outside git; the public flags carry no names.

Inputs
------
- sources/public/p3-ggb/_raw/ggb2019_lista_nominal.csv (not tracked in git)
- sources/public/p3-ggb/_raw/news/<id>.html (not tracked in git)

Outputs
-------
- sources/public/p3-ggb/_raw/news_txt/<id>.txt (not tracked in git)
- analysis/ggb-audit/dados/fonte_checks.csv (flags per case, no names)
- prints counts of valid files, removed offline pages and flagged names and death terms

Usage
-----
python3 -I analysis/ggb-audit/scripts/s04_extrair_texto.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

S04. Extrai texto visivel de cada HTML baixado e marca (a) pagina-erro/soft-404/Wayback offline,
(b) presenca do nome/alcunha da vitima, (c) presenca da cidade. Texto bruto em _raw/news_txt (fora do git);
flags publicas (sem nomes) em data/fonte_checks.csv. Uso: python3.14 -I s04_extrair_texto.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, html, unicodedata
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(REPO_ROOT)
RAW = ROOT/"sources/public/p3-ggb/_raw"; NEWS = RAW/"news"; TXT = RAW/"news_txt"; TXT.mkdir(exist_ok=True)
OUT = ROOT/"analysis/ggb-audit/dados"
def norm(s): return re.sub(r"[^a-z0-9 ]", " ", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.skip=0; s.buf=[]; s.title=""; s.in_title=False; s.meta=[]
    def handle_starttag(s, t, a):
        if t in ("script","style","noscript","nav","footer","header","form","aside"): s.skip+=1
        if t=="title": s.in_title=True
        if t=="meta":
            d=dict(a)
            if (d.get("property") in ("og:description","og:title") or d.get("name")=="description") and d.get("content"): s.meta.append(d["content"])
        if t in ("p","br","h1","h2","h3","li","div"): s.buf.append("\n")
    def handle_endtag(s, t):
        if t in ("script","style","noscript","nav","footer","header","form","aside") and s.skip: s.skip-=1
        if t=="title": s.in_title=False
    def handle_data(s, d):
        if s.in_title: s.title+=d
        elif not s.skip and d.strip(): s.buf.append(d.strip()+" ")
def read(f):
    b = f.read_bytes()
    m = re.search(rb"charset=[\"']?([\w-]+)", b[:4000]); enc = (m.group(1).decode() if m else "utf-8")
    try: return b.decode(enc, errors="replace")
    except LookupError: return b.decode("utf-8", errors="replace")
rows = list(csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()))
out = []
for r in rows:
    f = NEWS/f'{r["id"]}.html'
    d = dict(id=r["id"], arquivo=int(f.exists()), offline_wb=0, nome_presente=0, cidade_presente=0, termo_morte=0, nchar=0, soft404=0)
    if f.exists():
        h = read(f)
        if "Internet Archive services are temporarily offline" in h or "Temporarily Offline" in h[:3000]:
            d["offline_wb"] = 1; f.rename(NEWS/f'{r["id"]}.OFFLINE.html'); d["arquivo"] = 0
        else:
            p = P(); p.feed(h)
            t = (p.title.strip() + "\n" + "\n".join(p.meta) + "\n" + re.sub(r"[ \t]+", " ", "".join(p.buf))).strip()
            t = re.sub(r"\n\s*\n+", "\n", t)[:9000]
            (TXT/f'{r["id"]}.txt').write_text(t); d["nchar"] = len(t)
            d["soft404"] = int(bool(re.search(r"\b404\b|n[aã]o (foi )?encontrad|p[aá]gina n[aã]o|not found|conte[uú]do indispon|n[aã]o existe|removid", (p.title + " " + t[:300]), re.I)))
            nt = norm(t); nome = norm(r["nome"])
            toks = [w for w in nome.split() if len(w) >= 4 and w not in ("silva","santos","souza","filho","junior","dos","das","de","da")]
            d["nome_presente"] = int(bool(toks) and any(w in nt for w in toks))
            d["cidade_presente"] = int(norm(r["cidade"]).strip() in nt)
            d["termo_morte"] = int(bool(re.search(r"\b(morto|morta|assassinad|morre|morreu|corpo|homic|esfaque|facad|tiro|suicid|encontrad|latroc|executad|matou|mata)", nt)))
    out.append(d)
with (OUT/"fonte_checks.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
from collections import Counter
print("arquivos validos:", sum(d["arquivo"] for d in out), "| offline_wb removidos:", sum(d["offline_wb"] for d in out))
print("nome presente:", sum(d["nome_presente"] for d in out), "| termo morte:", sum(d["termo_morte"] for d in out))
