#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Build the evidence table README of the literature review.

Combines a fixed top and bottom text with one table per evidence level, listing for each work in
rows.py the reference, quartile status, local file with its SHA-256, study design, verbatim
finding with page and main limitation.

Inputs
------
- analysis/literature/scripts/rows.py
- analysis/literature/scripts/readme_top.md and readme_bottom.md
- the local source files listed in rows.py (hashed)

Outputs
-------
- analysis/literature/README.md
- prints the number of rows to stdout

Usage
-----
python3 -I analysis/literature/scripts/build_readme.py

Status
------
No registration status is claimed for this file.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import sys, os, hashlib, datetime
sys.path.insert(0, os.path.dirname(__file__))
import rows
BASE = (REPO_ROOT + "/")
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def esc(t): return t.replace("|","/").replace("\n"," ")
def short(p): return p.replace(BASE,"")
TOP = open(os.path.join(os.path.dirname(__file__),"readme_top.md"),encoding="utf-8").read()
BOT = open(os.path.join(os.path.dirname(__file__),"readme_bottom.md"),encoding="utf-8").read()
out = [TOP]
out.append("\n## Tabela de evidência (texto integral lido; verbatim com página)\n")
out.append("Convenções: página = página do PDF, salvo \"impresso\"; XML = sem paginação. Caminhos relativos a ``. Grau: **C** causal quase-experimental, **A** associativa, **D** descritiva, **J** documento jurídico/oficial, **E** ensaio ou revisão. \"Q1\" só onde a tabela SJR do projeto (`sources/public/scimago/quartis-sjr-2026-10-10.md` e `-10-11.md`) traz o periódico; fora delas, `nao_verificado`.\n")
for nv,tit in (("A","Nível A: perseguição estatal ou organizada (política de Estado, forças de segurança, extermínio)"),
               ("B","Nível B: violência por viés de indivíduos e grupos (crime de ódio), incluindo os registros e seus limites"),
               ("C","Nível C: violência estrutural e omissão do Estado (leis, instituições, dados)"),
               ("D","Nível D: retórica e clima político (emboldenment)")):
    out.append(f"\n### {tit}\n")
    out.append("| # | Referência | Q1? | Arquivo lido e sha256 | Desenho (grau) | Achado verbatim e página | Limitação principal |")
    out.append("|---|---|---|---|---|---|---|")
    for r in [x for x in rows.ROWS if x["nivel"]==nv]:
        out.append(f"| {r['id']} | {esc(r['ref'])} | {esc(r['q1'])} | `{short(r['file'])}` sha256 `{sha(r['file'])}` | {esc(r['grau'])} | {esc(r['quote'])} | {esc(r['limit'])} |")
out.append(BOT)
open(os.path.join(os.path.dirname(__file__),"..","README.md"),"w",encoding="utf-8").write("\n".join(out))
print("ok", len(rows.ROWS))
