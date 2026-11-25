# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Download state-by-year death counts from the SIM TabNet, 1996-2024.

Posts three queries to the DATASUS TabNet service (extended ICD-10 file ext10uf) for deaths by
state of residence and year of death in three cause groups: aggression (X85-Y09), undetermined
intent (Y10-Y34) and legal intervention (Y35-Y36). Each query is retried up to five times
because the service is unstable. The raw responses are stored with their SHA-256 and the
parsed table is written in long form. Years 2025 and later are excluded as preliminary.

Inputs
------
- http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10uf.def (public service, via curl)

Outputs
-------
- analysis/political-economy/dados/raw/tabnet_<group>.prn (raw responses)
- analysis/political-economy/dados/raw/SHA256SUMS.txt
- analysis/political-economy/dados/h1_sim_tabnet_uf_ano.csv
- prints the number of states per group to stderr and the output path to stdout

Usage
-----
python3 -I analysis/political-economy/scripts/h1_01_tabnet_sim_1996_2024.py

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

H1 insumo: óbitos por UF de residência x ano 1996-2024 do SIM/DATASUS (TabNet ext10uf), 3 grandes grupos CID-10:
4 = X85-Y09 agressões | 5 = Y10-Y34 intenção indeterminada (MVCI) | 6 = Y35-Y36 intervenções legais/guerra.
Bruto (.prn latin1) vai para data/raw/ com sha256 em data/raw/SHA256SUMS.txt. Saída: data/h1_sim_tabnet_uf_ano.csv.
Rodar: python3 -I scripts/h1_01_tabnet_sim_1996_2024.py   (TabNet é instável: o script tenta 5x por consulta)

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, hashlib, html, io, os, re, subprocess, sys, time, urllib.parse
BASE = (REPO_ROOT + "/analysis/political-economy")
RAW = f"{BASE}/dados/raw"; OUT = f"{BASE}/dados/h1_sim_tabnet_uf_ano.csv"
CGI = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10uf.def"
ANOS = list(range(1996, 2025))  # 2025/2026 preliminares: fora
GRUPOS = {"agressao_X85_Y09": "4", "indet_Y10_Y34": "5", "interv_Y35_Y36": "6"}

def consulta(tag, grupo):
    pares = [("Linha", "Unidade_da_Federação"), ("Coluna", "Ano_do_Óbito"), ("Incremento", "Óbitos_p/Residênc"),
             ("formato", "prn"), ("mostre", "Mostra"), ("SGrande_Grupo_CID10", grupo)]
    pares += [("Arquivos", f"extuf{str(a)[2:]}.dbf") for a in ANOS]
    body = urllib.parse.urlencode(pares, encoding="latin-1")
    path = f"{RAW}/tabnet_{tag}.prn"
    for t in range(5):
        r = subprocess.run(["curl", "-sS", "-m", "180", "-o", path, "-w", "%{http_code}", "-X", "POST", "--data", body, CGI], capture_output=True, text=True)
        txt = open(path, "rb").read().decode("latin1")
        if r.stdout.strip() == "200" and "Unidade da Federa" in txt and "1996" in txt:
            return path, txt
        time.sleep(15)
    raise SystemExit(f"TabNet não respondeu com tabela para {tag}")

def parse(txt):
    header, rows = None, {}
    for rec in csv.reader(io.StringIO(txt), delimiter=";", quotechar='"'):
        if not rec: continue
        first = html.unescape(rec[0]).strip()
        if first.startswith("Unidade da Federação"):
            header = [html.unescape(h).strip() for h in rec]; continue
        if header is None or first == "Total": continue
        m = re.match(r"^(\d{2}) (.+)$", first)
        if not m: continue
        rows[m.group(1)] = {int(h): (0 if v.strip() == "-" else int(v)) for h, v in zip(header[1:], rec[1:]) if h.isdigit() and (v.strip() == "-" or v.strip().isdigit())}
    return rows

def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()

def main():
    os.makedirs(RAW, exist_ok=True)
    dados, sums = {}, []
    for tag, g in GRUPOS.items():
        p, txt = consulta(tag, g); dados[tag] = parse(txt); sums.append(f"{sha(p)}  tabnet_{tag}.prn")
        print(tag, len(dados[tag]), "UFs", file=sys.stderr)
    open(f"{RAW}/SHA256SUMS.txt", "w").write("\n".join(sums) + "\n")
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["cod_uf", "ano"] + list(GRUPOS))
        for cod in sorted(dados["agressao_X85_Y09"]):
            for a in ANOS:
                w.writerow([cod, a] + [dados[t].get(cod, {}).get(a, "") for t in GRUPOS])
    print("ok", OUT)
main()
