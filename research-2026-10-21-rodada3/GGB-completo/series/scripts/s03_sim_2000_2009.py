"""SIM/DATASUS: obitos por agressao (CID-10 X85-Y09), intencao indeterminada (Y10-Y34) e intervencao legal (Y35-Y36), Brasil, por ano de OCORRENCIA?
Nota: o DOBRyyyy do FTP e por ano do OBITO (DTOBITO). Estende para 2000-2009 a serie ja agregada em dados/sim (2010-2024).
Uso: python  # venv com pyreaddbc + dbfread -I s03_sim_2000_2009.py   (precisa de pyreaddbc + dbfread; arquivos grandes em _raw/sim_pre2010, fora do git)"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, collections, hashlib, os, subprocess, sys
import pyreaddbc
from dbfread import DBF
RAW = (REPO_ROOT + "/fontes/p3-ggb/_raw/sim_pre2010")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados_sim_2000_2009.csv")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def grupo(cb):
    cb = (cb or "").strip().upper()
    if len(cb) < 3 or not cb[1:3].isdigit(): return None
    l, n = cb[0], int(cb[1:3])
    if l == "X" and n >= 85 or l == "Y" and n <= 9: return "agressao"
    if l == "Y" and 10 <= n <= 34: return "indet"
    if l == "Y" and n in (35, 36): return "interv_legal"
    return None
rows = []
for ano in range(2000, 2010):
    dbc = f"{RAW}/DOBR{ano}.dbc"; dbf = f"{RAW}/DOBR{ano}.dbf"
    if not os.path.exists(dbc):
        r = subprocess.run(["curl", "-sS", "-m", "900", "-o", dbc, f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DOBR{ano}.dbc"], capture_output=True, text=True)
        assert r.returncode == 0 and os.path.getsize(dbc) > 1_000_000, f"download {ano}: {r.stderr[:200]}"
    if not os.path.exists(dbf): pyreaddbc.dbc2dbf(dbc, dbf)
    c = collections.Counter(); tot = 0
    for r in DBF(dbf, encoding="latin-1", load=False):
        tot += 1
        g = grupo(r.get("CAUSABAS"))
        if g: c[g] += 1
    os.remove(dbf)
    rows.append(dict(ano=ano, obitos_total_arquivo=tot, agressao=c["agressao"], indet=c["indet"], interv_legal=c["interv_legal"], sha256_dbc=sha(dbc)))
    print(rows[-1], flush=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
