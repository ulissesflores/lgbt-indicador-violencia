"""C27 passo 1: monta os itens a codificar as cegas. Le do CSV original SOMENTE hash/familia/universo
(nunca postura/forma/fonte). Texto vem dos _amostra_*.jsonl. Saida: ../itens_C27.jsonl (id opaco, estrato,
familia, texto) e ../sorteio_100.json. Python: /opt/homebrew/bin/python3.14 -I."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, json, random, hashlib
M = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
SEMENTE = 20261023
txt = {}
for u in ("GNRSS-mundo", "GNRSS-pt", "OpenAlex", "Parlamento", "Wikipedia"):
    for l in open(f"{M}/_amostra_{u}.jsonl"):
        r = json.loads(l)
        t = (r.get("titulo", "") + ("\n" + r["trecho"] if r.get("trecho") else "")).strip()
        txt[(r["hash"], r["familia"], u)] = t[:1500]
chaves = []
with open(f"{M}/amostra_codificada.csv", newline="") as f:
    for r in csv.DictReader(f):
        chaves.append((r["hash"], r["familia"], r["universo"]))   # so estas 3 colunas
assert len(chaves) == len(set(chaves)), "chave duplicada"
faltam = [c for c in chaves if c not in txt]
assert not faltam, faltam[:3]
par = lambda fam: sorted(c for c in chaves if c[2] == "Parlamento" and c[1] == fam)
f2, f3 = par("F2"), par("F3")
pop = sorted(c for c in chaves if not (c[2] == "Parlamento" and c[1] in ("F2", "F3")))
sorteio = random.Random(SEMENTE).sample(pop, 100)
itens = []
for estrato, lista in (("F2-Parlamento", f2), ("F3-Parlamento", f3), ("Outras-100", sorteio)):
    for c in lista:
        itens.append({"id": hashlib.sha256(f"{estrato}|{c[0]}|{c[1]}|{c[2]}".encode()).hexdigest()[:12],
                      "estrato": estrato, "hash": c[0], "familia": c[1], "universo": c[2], "texto": txt[c]})
print(len(f2), len(f3), len(pop), len(sorteio), len(itens))
with open(f"{OUT}/itens_C27.jsonl", "w") as f:
    for i in itens:
        f.write(json.dumps(i, ensure_ascii=False) + "\n")
json.dump(sorteio, open(f"{OUT}/sorteio_100.json", "w"))
from collections import Counter
print(Counter((i["universo"], i["familia"]) for i in itens if i["estrato"] == "Outras-100"))
