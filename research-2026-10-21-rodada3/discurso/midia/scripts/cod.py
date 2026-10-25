"""Auxiliar de codificacao: grava/atualiza _codif/<universo>.json. Uso: from cod import grava
grava(universo, indices_range, default=[...8 campos...], overrides={idx:[...]}, texto='so_titulo')"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import json, os
D = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia/_codif")
def grava(uni, rng, overrides, default=("FORA", "", "nenhuma", "", 0, 0, 0, 0), texto="so_titulo"):
    fn = f"{D}/{uni}.json"
    cur = json.load(open(fn)) if os.path.exists(fn) else {}
    for i in rng:
        cur[str(i)] = list(default) + [texto]
    for i, v in overrides.items():
        v = list(v) + ['', 'nenhuma', '', 0, 0, 0, 0][len(v) - 1:] if len(v) < 8 else list(v)
        cur[str(i)] = v + [texto]
    json.dump(cur, open(fn, "w"))
    print(uni, len(cur))
