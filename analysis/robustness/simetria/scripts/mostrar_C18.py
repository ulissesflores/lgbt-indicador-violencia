# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Print sentences that mention the LGBT theme and an actor, for one government.

Reading aid for the C18 search. The script takes a government code (G1 to G6) and an optional
maximum number of sentences, splits each extracted page text of that government into
sentences, and keeps those that match both a theme pattern (homosexual, gay, LGBT, homophobia,
trans terms) and an actor or measure pattern specific to that government, with 40 to 700
characters.

Inputs
------
- sources/public/q1-textointegral/discurso/simetria/brasil/<gov>_Q*.txt (extracted page text)
- command line: government code (G1 to G6) and optional sentence limit per file (default 14)

Outputs
-------
- prints, per file, the character count, the number of candidate sentences and the sentences

Usage
-----
python3 -I analysis/robustness/simetria/scripts/mostrar_C18.py G1 14

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Imprime, por arquivo baixado de um governante, as frases com (tema LGBT) E (marca temporal/ator). Uso: mostrar_C18.py G1 [maxfrases]

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import re, sys, glob, os
D = (REPO_ROOT + "/sources/public/q1-textointegral/discurso/simetria/brasil")
g = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 14
ALVO = {"G1": r"Lula|governo|presidente|Brasil sem Homofobia|Ministério|Secretaria|decreto|Pelotas", "G2": r"Lula|governo|presidente|decreto|Conferência|Conselho", "G3": r"Dilma|governo|presidente|decreto|kit|veto", "G4": r"Temer|governo|presidente|decreto|Ministério|orçamento|verba|repasses", "G5": r"Bolsonaro|governo|presidente|decreto|ministr|Ancine|MP 870", "G6": r"Lula|governo|presidente|decreto|ministr|Conselho"}[g]
TEMA = re.compile(r"homossex|gays?\b|LGBT|homofob|lésbic|travest|transex|Brasil sem Homofobia", re.I)
for f in sorted(glob.glob(f"{D}/{g}_Q*.txt")):
    t = open(f).read()
    frases = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕ“\"])", t)
    sel = [s.strip() for s in frases if TEMA.search(s) and re.search(ALVO, s) and 40 < len(s) < 700]
    print(f"\n#### {os.path.basename(f)}  chars={len(t)} frases_candidatas={len(sel)}")
    for s in sel[:mx]:
        print("  -", s[:520])
