# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Draw the audit sample from the 329 GGB 2019 cases with a fixed seed.

Simple random sample without replacement (n = 160) of the hashed universe, with the seed
20261021, plus a double-coding subsample of 32 cases (20 percent) with the seed 20261022. Only
hash ids are written.

Inputs
------
- analysis/ggb-audit/dados/ggb2019_universo_hash.csv

Outputs
-------
- analysis/ggb-audit/dados/amostra.csv (ids only)
- prints the sample size and the double-coding subsample size

Usage
-----
python3 -I analysis/ggb-audit/scripts/s03_sorteio.py

Status
------
Sample drawn before any source was read, as stated in the original docstring below. No
registration document is claimed.

Notes
-----
Original description (Portuguese), kept verbatim:

S03. Sorteio da amostra (AAS sem reposicao) do universo GGB 2019 (329 casos) ANTES de ler qualquer fonte.
Semente fixa 20261021. n=160. Subamostra de dupla codificacao: 32 (20%), semente 20261022.
Saida: data/amostra.csv (somente ids). Uso: python3.14 -I s03_sorteio.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, random
from pathlib import Path
ROOT = Path((REPO_ROOT + "/analysis/ggb-audit/dados"))
ids = [r["id"] for r in csv.DictReader((ROOT/"ggb2019_universo_hash.csv").open())]  # ordem do Anexo 3 (n=1..329)
assert len(ids) == 329 and len(set(ids)) == 329
amostra = random.Random(20261021).sample(ids, 160)
dupla = set(random.Random(20261022).sample(amostra, 32))
with (ROOT/"amostra.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["ordem_sorteio", "id", "dupla_codificacao"])
    for i, x in enumerate(amostra, 1): w.writerow([i, x, int(x in dupla)])
print(len(amostra), sum(1 for x in amostra if x in dupla))
