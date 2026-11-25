# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Extract elected governors and vice-governors per state and cycle from TSE candidate files.

Reads the zipped TSE candidate registries for the 2010, 2014, 2018 and 2022 elections directly
from the archive, without extracting it. It keeps ordinary-election rows for governor and
vice-governor whose final result is ELECTED, with the party the candidate ran for, and reports
state, office and year keys that have more than one record. Only the standard library is used.

Inputs
------
- sources/public/p2-f8-governos/tse/z2010/consulta_cand_2010.zip (not tracked in git)
- sources/public/p2-f8-governos/tse/z2014/consulta_cand_2014.zip (not tracked in git)
- sources/public/p2-f8-governos/tse/z2018/consulta_cand_2018.zip (not tracked in git)
- sources/public/p2-f8-governos/tse/z2022/consulta_cand_2022.zip (not tracked in git)

Outputs
-------
- data/governadores_tse_eleitos.csv
- prints the record counts and any duplicated keys to stdout

Usage
-----
python3 -I data/scripts/governadores_tse.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Governador e vice ELEITOS por UF e ciclo (2010, 2014, 2018, 2022) a partir de consulta_cand do TSE (sources/public/p2-f8-governos/tse/z<ano>/consulta_cand_<ano>.zip, baixados de https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_<ano>.zip em 2026-10-21;
sha256 em sources/public/p2-f8-governos/tse/SHA256SUMS.txt; *.zip fica fora do git). Saída: data/governadores_tse_eleitos.csv. Só stdlib.
Regras: eleição ordinária; DS_SIT_TOT_TURNO == 'ELEITO' (vale para eleito no 1º turno e no 2º). Partido = SG_PARTIDO do candidato (partido pelo qual concorreu).
Rodar: python3 -I data/scripts/governadores_tse.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, io, zipfile, collections, sys
BASE = REPO_ROOT
rows = []
for y in (2010, 2014, 2018, 2022):
    z = zipfile.ZipFile(f"{BASE}/sources/public/p2-f8-governos/tse/z{y}/consulta_cand_{y}.zip")  # lê direto do zip: sem extrair 115 MB para o repositório
    for nome in sorted(n for n in z.namelist() if len(n) == len(f"consulta_cand_{y}_SP.csv") and n.startswith(f"consulta_cand_{y}_") and n.endswith(".csv")):
        if nome.endswith("_BR.csv"):
            continue
        with z.open(nome) as raw:
            for r in csv.DictReader(io.TextIOWrapper(raw, encoding="latin-1", newline=""), delimiter=";"):
                if r["DS_CARGO"] in ("GOVERNADOR", "VICE-GOVERNADOR") and r["DS_SIT_TOT_TURNO"] == "ELEITO":
                    rows.append([y, r["SG_UF"], r["DS_CARGO"], r["NM_CANDIDATO"], r["SG_PARTIDO"], r["NR_TURNO"], r["NM_TIPO_ELEICAO"], r["DS_ELEICAO"], r["NM_URNA_CANDIDATO"]])
por = collections.defaultdict(list)
for r in rows:
    por[(r[0], r[1], r[2])].append(r)
dup = {k: v for k, v in por.items() if len(v) > 1}
print("registros eleitos:", len(rows), "| chaves ano/UF/cargo:", len(por), "| chaves com mais de 1 registro:", len(dup))
for k, v in sorted(dup.items()):
    for r in v:
        print("  DUP", r)
with open(f"{BASE}/data/governadores_tse_eleitos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["ano_eleicao", "uf", "cargo", "nome", "partido", "turno", "tipo_eleicao", "eleicao", "nome_urna"]); w.writerows(sorted(rows))
