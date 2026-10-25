"""Dependencia da lista TDoR/TMM (Brasil) em relacao ao GGB/Homofobia Mata e a ANTRA, medida pelo TEXTO publico de cada registro (campo Description do export TDoR).
Conta registros cujo texto cita (a) Homofobia Mata / homofobiamata.wordpress.com, (b) Grupo Gay da Bahia / GGB, (c) ANTRA. Citar a fonte nao prova copia do caso, mostra a rota de descoberta.
Uso: /opt/homebrew/bin/python3.14 -I s08_dep_tdor.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, re, pathlib
RAW = pathlib.Path((REPO_ROOT + "/fontes/p3-ggb/_raw/tdor/anual"))
OUT = pathlib.Path(__file__).resolve().parent.parent / "dados_tdor_dependencia.csv"
HM = re.compile(r"homofobiamata|homofobia mata|homotransfobia mata", re.I); GG = re.compile(r"grupo gay|gay da bahia|\bggb\b", re.I); AN = re.compile(r"\bantra\b", re.I)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano", "n_tdor_brasil", "n_cita_HomofobiaMata", "n_cita_GGB", "n_cita_HM_ou_GGB", "pct_HM_ou_GGB", "n_cita_ANTRA", "pct_ANTRA"])
    for y in range(2008, 2026):
        r = list(csv.DictReader(open(RAW / f"tdor_br_{y}.csv", encoding="utf-8-sig"))); n = len(r)
        h = sum(bool(HM.search(x["Description"])) for x in r); g = sum(bool(GG.search(x["Description"])) for x in r); hg = sum(bool(HM.search(x["Description"]) or GG.search(x["Description"])) for x in r); a = sum(bool(AN.search(x["Description"])) for x in r)
        w.writerow([y, n, h, g, hg, round(100 * hg / n, 1), a, round(100 * a / n, 1)])
print(open(OUT).read())
