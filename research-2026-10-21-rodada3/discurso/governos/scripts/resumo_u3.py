"""Resumo: regime (RoW 2025, V-Dem v16) dos 65 Estados-membros da ONU que criminalizam (ILGA DB 2026-10-22) x os 128 que nao criminalizam. Saida ../u3_resumo.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import json, pyreadr, pycountry, pandas as pd
F = (REPO_ROOT + "/fontes/q1-textointegral/discurso/governos/")
O = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/governos/u3_resumo.md")
vd = pyreadr.read_r(F + "vdemdata-vdem.RData")["vdem"]
R = {0: "autocracia fechada", 1: "autocracia eleitoral", 2: "democracia eleitoral", 3: "democracia liberal"}
rows = []
for e in json.load(open(F + "ilga-db-csssa-all.json"))["data"]["entriesCsssa"]:
    m = e["motherEntry"]; j = m["jurisdiction"]
    if m["subjurisdiction"] or not j["un_member"]: continue
    a3 = pycountry.countries.get(alpha_2=j["a2_code"]).alpha_3
    r = vd[(vd.country_text_id == a3) & vd.v2x_regime.notna()].sort_values("year")
    rows.append(dict(pais=j["name"], criminaliza=not e["legal"], regime=(R[int(r.iloc[-1].v2x_regime)] if len(r) else "sem_dado")))
d = pd.DataFrame(rows)
ct = pd.crosstab(d.regime, d.criminaliza)
L = ["# Regime (V-Dem RoW, ano mais recente com dado) dos Estados-membros da ONU, por criminalizar ou nao (ILGA DB, 2026-10-22)", "",
     f"n = {len(d)} Estados-membros ({d.criminaliza.sum()} criminalizam por lei ou de fato; {(~d.criminaliza).sum()} nao).", "",
     "| regime | nao criminalizam | criminalizam | % que criminaliza dentro do regime |", "|---|---|---|---|"]
for rg in ["autocracia fechada", "autocracia eleitoral", "democracia eleitoral", "democracia liberal", "sem_dado"]:
    a = int(ct.loc[rg, False]) if rg in ct.index else 0; b = int(ct.loc[rg, True]) if rg in ct.index else 0
    L.append(f"| {rg} | {a} | {b} | {b/(a+b):.0%} |" if a + b else f"| {rg} | 0 | 0 | - |")
L += ["", "Leitura: associacao descritiva entre regime e criminalizacao; nao ha desenho causal (sem contrafactual). 'Criminaliza' inclui os 2 casos de criminalizacao de fato da ILGA."]
open(O, "w").write("\n".join(L) + "\n"); print("\n".join(L))
