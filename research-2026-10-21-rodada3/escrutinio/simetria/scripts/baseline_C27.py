"""C27 linha de base: 60 falas da Camara com ESTATISTICA fora dos temas (regras em CRITERIOS.md secao 3).
Reusa por import GATE/norm_map/d de analise_parlamento.py. Saida: ../baseline_itens.jsonl, ../baseline_pool_stats.json.
Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import glob, hashlib, importlib.util, json, os, random, re, sys
SC = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia/scripts/analise_parlamento.py")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
sys.argv = [sys.argv[0]]                      # evita MOD != dicionario_v2
spec = importlib.util.spec_from_file_location("ap", SC); ap = importlib.util.module_from_spec(spec); spec.loader.exec_module(ap)
STAT = re.compile(r"\b\d{1,3}(?:[.,]\d+)?\s?(?:%|por cento)|\ba cada \d+ (?:horas?|minutos?|segundos?|dias?|anos?)|\b\d+(?:[.,]\d+)?\s(?:mil|milhao|milhoes|bilhao|bilhoes)\b", re.I)
vistos, pool, n_tot, n_gate = set(), [], 0, 0
deps = json.load(open(ap.CAM + "/_deputados.json"))
for fn in sorted(glob.glob(ap.CAM + "/[0-9]*_*.json")):
    did = os.path.basename(fn).split("_")[0]
    for x in json.load(open(fn))["dados"]:
        tx = (x.get("transcricao") or "") + " " + (x.get("sumario") or "") + " " + (x.get("keywords") or "")
        chave = hashlib.sha256((did + x["dataHoraInicio"] + tx).encode()).hexdigest()
        if chave in vistos:
            continue
        vistos.add(chave); n_tot += 1
        if ap.GATE.search(ap.d.norm(tx)):
            n_gate += 1; continue
        t, idx = ap.norm_map(tx)
        m = STAT.search(t)
        if not m:
            continue
        a, b = max(0, m.start() - 220), min(len(t), m.end() + 220)
        pool.append({"id": chave, "data": x["dataHoraInicio"], "autor": deps.get(did, did), "url": x.get("urlTexto", ""),
                     "trecho": tx[idx[a]:idx[min(b, len(idx)) - 1] + 1].replace("\n", " ")})
pool.sort(key=lambda r: r["id"])
amostra = random.Random(20261023).sample(pool, 60)
json.dump({"discursos_dedup": n_tot, "excluidos_por_GATE": n_gate, "elegiveis_com_estatistica": len(pool)}, open(OUT + "/baseline_pool_stats.json", "w"))
with open(OUT + "/baseline_itens.jsonl", "w") as f:
    for r in amostra:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(n_tot, n_gate, len(pool), len(amostra))
