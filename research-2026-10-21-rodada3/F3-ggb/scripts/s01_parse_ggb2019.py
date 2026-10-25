"""S01. Extrai do PDF GGB 2019 (texto pdftotext -layout) o Anexo 3 (lista nominal, 329 casos)
e o Anexo 4 (fonte + link por caso). Saida NOMINAL so em fontes/p3-ggb/_raw (fora do git).
Saida publica: so ids hash. Uso: python3.14 -I s01_parse_ggb2019.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import re, csv, hashlib, json, sys, unicodedata
from pathlib import Path
ROOT = Path(REPO_ROOT)
RAW = ROOT/"fontes/p3-ggb/_raw"
OUT = ROOT/"research-2026-10-21-rodada3/F3-ggb/dados"
txt = (RAW/"txt/ggb2019.txt").read_text().splitlines()
i3 = next(i for i,l in enumerate(txt) if l.startswith("Anexo 3 – Lista"))
i4 = next(i for i,l in enumerate(txt) if l.startswith("Anexo 4 – Lista"))
CAT = r"(Gay|Lésbica|Travesti|Transexual|Mulher Trans|Bissexual|Homem Trans|Homem trans|Heterossexual|Não binário|NI|Intersexo|Bisexual)"
r3 = re.compile(r"^\s*(\d+)\s+(.+?)\s{2,}([A-Z]{2})\s+(.*?)\s*"+CAT+r"\s*$")
cases = {}
for l in txt[i3:i4]:
    m = r3.match(l)
    if m:
        n = int(m.group(1)); cases[n] = dict(n=n, cidade=m.group(2).strip(), uf=m.group(3), nome=m.group(4).strip(), cat=m.group(5))
    elif re.match(r"^\s*94\s+Boa Vista\s{2,}\S", l):
        # linha 94 do PDF perdeu a UF e traz dois nomes na coluna Nome; UF inferida RR (capital Boa Vista), registrada no README
        nomes = re.split(r"\s{2,}", l.strip())[2:-1]
        cases[94] = dict(n=94, cidade="Boa Vista", uf="RR", nome=" / ".join(nomes), cat="Travesti")
    elif re.match(r"^\s*\d+\s+\S", l):
        print("NAO CASOU:", l, file=sys.stderr)
# Anexo 4: "N.  Fonte   Link" com continuacao de linha
rows = {}; cur = None
r4 = re.compile(r"^(\d+)\s{2,}(\S.*?)(?:\s{2,}(\S+))?\s*$")
for l in txt[i4+3:]:
    if not l.strip() or l.strip().isdigit(): continue
    m = r4.match(l)
    if m and 1 <= int(m.group(1)) <= 329 and (cur is None or int(m.group(1)) == cur+1 or int(m.group(1)) == cur):
        cur = int(m.group(1)); fonte, link = m.group(2).strip(), (m.group(3) or "")
        if link and not link.startswith("http") and not fonte.startswith("http"):
            fonte = (fonte+" "+link).strip(); link = ""
        elif fonte.startswith("http"):
            link, fonte = fonte, ""
        rows[cur] = dict(fonte=fonte, link=link)
    elif cur:
        s = l.strip(); toks = s.split()
        # continuacao: pode ter nome de fonte (coluna 2) e/ou parte do link (coluna 3)
        parts = re.split(r"\s{2,}", s)
        for p in parts:
            if p.startswith("http") or (rows[cur]["link"] and not rows[cur]["link"].endswith(("/",".html",".ghtml")) and " " not in p and ("/" in p or "-" in p or "?" in p) and len(parts)>=1 and p is parts[-1] and re.match(r"^[\w%\-/\.\?=&~#:;,+]+$", p)):
                rows[cur]["link"] += p
            else:
                rows[cur]["fonte"] += " "+p
print("casos Anexo3:", len(cases), "| fontes Anexo4:", len(rows))
SALT = (RAW/"salt.txt")
if not SALT.exists(): SALT.write_text(hashlib.sha256(b"ggb-p3-salt-2026-10-21").hexdigest())
salt = SALT.read_text().strip()
def hid(n, c): return hashlib.sha256(f"{salt}|2019|{n}|{c['nome'].lower()}|{c['cidade'].lower()}".encode()).hexdigest()[:10]
with (RAW/"ggb2019_lista_nominal.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["id","n","nome","cidade","uf","cat","fonte","link"])
    for n in sorted(cases):
        c = cases[n]; r = rows.get(n, dict(fonte="", link=""))
        c["id"] = hid(n, c); w.writerow([c["id"], n, c["nome"], c["cidade"], c["uf"], c["cat"], r["fonte"], r["link"]])
with (OUT/"ggb2019_universo_hash.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["id","uf","cat_ggb","tem_nome","fonte_tipo","dominio"])
    from urllib.parse import urlparse
    for n in sorted(cases):
        c = cases[n]; r = rows.get(n, dict(fonte="", link=""))
        dom = urlparse(r["link"]).netloc.lower().removeprefix("www.") if r["link"] else ""
        tipo = "link" if r["link"] else ("SI" if r["fonte"].strip() in ("SI","") else "sem_link:"+r["fonte"][:30])
        w.writerow([c["id"], c["uf"], c["cat"], int(bool(c["nome"])), tipo, dom])
from collections import Counter
print(Counter(c["cat"] for c in cases.values()))
print("sem link:", sum(1 for n in cases if not rows.get(n,{}).get("link")))
missing = [n for n in range(1,330) if n not in cases]; print("faltando no Anexo3:", missing)
