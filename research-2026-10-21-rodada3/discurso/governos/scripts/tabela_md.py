"""Gera as linhas da tabela de GOVERNOS.md a partir de paises.csv (evita transcricao manual)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, re
rows = list(csv.DictReader(open((REPO_ROOT + "/research-2026-10-21-rodada3/discurso/governos/paises.csv"))))
def sr(s):
    m = re.match(r"(\d) ([^(]+)\((\d+)\)", s)
    return f"{m.group(1)} {m.group(2).strip().replace('autocracia ', 'aut. ').replace('democracia ', 'dem. ')}" if m else "sem dado V-Dem"
for r in rows:
    pm = r["pena_morte"].split(" ")[0].replace("legal_subnacional", "legal (12 estados)").replace("possivel(sem", "possível")
    ex = r["execucoes_documentadas"].split(":")[0].split(" ")[0]
    niv = re.split(r" \(|\(", r["nivel"])[0].strip().replace("L4 PROVISORIO", "L4 prov.")
    ideo = r["ideologia_executivo"]; cls = r["classificacao_eixo(V-Party econ; BRC geral)"]
    m = re.search(r"econ (\d)=([^;]+); LGBT (\d)", ideo); b = re.search(r"BRC (\w+) \d+ = ([\d.]+)/10", ideo)
    c0 = cls.split("(")[0]
    if cls.startswith("nao_classificado") or "defasado sem" in cls: e = "não classif."
    elif cls.startswith("nao_aplicavel"): e = "n/a (sem partido)"
    elif b: e = f"{c0}: BRC {b.group(1)} {b.group(2)}; LGBT {re.search(r'LGBT (\d)', ideo).group(1)}"
    elif m: e = f"{c0}: econ {m.group(1)}, LGBT {m.group(3)}" + (" (defas.)" if "defasado" in cls else "")
    else: e = "não classif."
    print(f"| {r['pais']} {r['ano_ref']} | {sr(r['regime_RoW'])} | {pm} | {niv} | {ex} | {e} |")
