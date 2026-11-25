# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Count aggression deaths per year in the SIM mortality files for 2000-2009.

Downloads, when absent, the yearly national death files of the Brazilian Mortality Information
System (SIM, DATASUS), converts them to DBF and counts deaths by underlying cause: aggression
(ICD-10 X85-Y09), undetermined intent (Y10-Y34) and legal intervention (Y35-Y36). The yearly
file is keyed by the year of death. The result extends to 2000-2009 the series already
aggregated in data/sim for 2010-2024.

Inputs
------
- ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DOBR<year>.dbc, fetched with curl
  into sources/public/p3-ggb/_raw/sim_pre2010/ (large files; not tracked in git)
- the Python packages pyreaddbc and dbfread

Outputs
-------
- analysis/ggb-series/series/dados_sim_2000_2009.csv (rewritten after each year)
- temporary DBF files, deleted after counting
- prints each yearly row to stdout

Usage
-----
python3.14 -I analysis/ggb-series/series/scripts/s03_sim_2000_2009.py
(run in an environment where pyreaddbc and dbfread are installed)

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

SIM/DATASUS: obitos por agressao (CID-10 X85-Y09), intencao indeterminada (Y10-Y34) e intervencao legal (Y35-Y36), Brasil, por ano de OCORRENCIA?
Nota: o DOBRyyyy do FTP e por ano do OBITO (DTOBITO). Estende para 2000-2009 a serie ja agregada em data/sim (2010-2024).
Uso: python  # venv com pyreaddbc + dbfread -I s03_sim_2000_2009.py   (precisa de pyreaddbc + dbfread; arquivos grandes em _raw/sim_pre2010, fora do git)

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, collections, hashlib, os, subprocess, sys
import pyreaddbc
from dbfread import DBF
RAW = (REPO_ROOT + "/sources/public/p3-ggb/_raw/sim_pre2010")
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
