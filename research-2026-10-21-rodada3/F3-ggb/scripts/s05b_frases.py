"""S05b. Para ordens dadas, imprime so as frases da fonte com termos de identidade (LGBT) e de motivo/desfecho.
Uso: python3.14 -I s05b_frases.py <ordem> [<ordem>...]"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, sys
from pathlib import Path
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"
amo = {r["ordem_sorteio"]: r["id"] for r in csv.DictReader((ROOT/"research-2026-10-21-rodada3/F3-ggb/dados/amostra.csv").open())}
ID = re.compile(r"gay|homossex|homoafet|travest|\btrans|transex|l[eé]sbic|bissex|lgbt|homofob|transfob|namorad|companheir|casal|orienta[cç][aã]o|gen[eê]ro|vestid|maquiad", re.I)
MO = re.compile(r"motiv|ci[uú]me|roubo|roub|latroc|d[ií]vida|briga|discuss|confess|preso|presa|apreend|foragid|inqu[eé]rito|suspeit|autores?|dinheiro|drog|tr[aá]fico|acerto|vingan", re.I)
for k in sys.argv[1:]:
    t = re.sub(r"\s+", " ", (RAW/"news_txt"/f"{amo[k]}.txt").read_text())
    ss = list(dict.fromkeys(s.strip() for s in re.split(r"(?<=[.!?])\s+", t)))
    a = [s for s in ss if ID.search(s)][:6]; b = [s for s in ss if MO.search(s) and s not in a][:6]
    print(f"\n## {k}  ID:"); [print("  I>", s[:230]) for s in a]
    print("  MOTIVO/DESFECHO:"); [print("  M>", s[:230]) for s in b]
