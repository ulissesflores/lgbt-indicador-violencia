"""S03. Sorteio da amostra (AAS sem reposicao) do universo GGB 2019 (329 casos) ANTES de ler qualquer fonte.
Semente fixa 20261021. n=160. Subamostra de dupla codificacao: 32 (20%), semente 20261022.
Saida: dados/amostra.csv (somente ids). Uso: python3.14 -I s03_sorteio.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, random
from pathlib import Path
ROOT = Path((REPO_ROOT + "/research-2026-10-21-rodada3/F3-ggb/dados"))
ids = [r["id"] for r in csv.DictReader((ROOT/"ggb2019_universo_hash.csv").open())]  # ordem do Anexo 3 (n=1..329)
assert len(ids) == 329 and len(set(ids)) == 329
amostra = random.Random(20261021).sample(ids, 160)
dupla = set(random.Random(20261022).sample(amostra, 32))
with (ROOT/"amostra.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["ordem_sorteio", "id", "dupla_codificacao"])
    for i, x in enumerate(amostra, 1): w.writerow([i, x, int(x in dupla)])
print(len(amostra), sum(1 for x in amostra if x in dupla))
