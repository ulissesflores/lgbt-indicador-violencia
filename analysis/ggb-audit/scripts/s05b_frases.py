# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Print only the source sentences with identity terms and with motive or outcome terms.

For the given draw-order numbers of the sample, it prints the sentences of the saved source
text that match the LGBT identity pattern and those that match the motive or outcome pattern.
It only reads; it does not write to disk.

Inputs
------
- analysis/ggb-audit/dados/amostra.csv
- sources/public/p3-ggb/_raw/news_txt/<id>.txt (not tracked in git)

Outputs
-------
- prints the sentences to stdout; nothing is written to disk

Usage
-----
python3 -I analysis/ggb-audit/scripts/s05b_frases.py <order> [<order> ...]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

S05b. Para ordens dadas, imprime so as frases da fonte com termos de identidade (LGBT) e de motivo/desfecho.
Uso: python3.14 -I s05b_frases.py <ordem> [<ordem>...]

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, sys
from pathlib import Path
ROOT = Path(REPO_ROOT); RAW = ROOT/"sources/public/p3-ggb/_raw"
amo = {r["ordem_sorteio"]: r["id"] for r in csv.DictReader((ROOT/"analysis/ggb-audit/dados/amostra.csv").open())}
ID = re.compile(r"gay|homossex|homoafet|travest|\btrans|transex|l[eé]sbic|bissex|lgbt|homofob|transfob|namorad|companheir|casal|orienta[cç][aã]o|gen[eê]ro|vestid|maquiad", re.I)
MO = re.compile(r"motiv|ci[uú]me|roubo|roub|latroc|d[ií]vida|briga|discuss|confess|preso|presa|apreend|foragid|inqu[eé]rito|suspeit|autores?|dinheiro|drog|tr[aá]fico|acerto|vingan", re.I)
for k in sys.argv[1:]:
    t = re.sub(r"\s+", " ", (RAW/"news_txt"/f"{amo[k]}.txt").read_text())
    ss = list(dict.fromkeys(s.strip() for s in re.split(r"(?<=[.!?])\s+", t)))
    a = [s for s in ss if ID.search(s)][:6]; b = [s for s in ss if MO.search(s) and s not in a][:6]
    print(f"\n## {k}  ID:"); [print("  I>", s[:230]) for s in a]
    print("  MOTIVO/DESFECHO:"); [print("  M>", s[:230]) for s in b]
