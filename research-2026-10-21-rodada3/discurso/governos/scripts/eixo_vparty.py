"""ADENDO exploratorio (nao pre-registrado): relacao entre eixo economico (v2pariglef_ord) e posicao LGBT (v2palgbt_ord)
nos partidos do V-Party v2 (1965-2019), todos e so os que formaram governo (v2pagovsup==0). Descritivo, sem inferencia causal.
Requer pyreadr, pandas. Saida: ../eixo_vparty.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import pyreadr, pandas as pd
F = (REPO_ROOT + "/fontes/q1-textointegral/discurso/governos/")
O = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/governos/eixo_vparty.md")
vp = pyreadr.read_r(F + "vdemdata-vparty.RData")["vparty"]
vd = pyreadr.read_r(F + "vdemdata-vdem.RData")["vdem"][["country_text_id", "year", "v2x_regime"]]
d = vp[["country_text_id", "year", "v2paenname", "v2pariglef_ord", "v2palgbt_ord", "v2pagovsup"]].dropna(subset=["v2pariglef_ord", "v2palgbt_ord"])
d = d.merge(vd, on=["country_text_id", "year"], how="left")
rk = lambda s: s.rank()
def sp(x): return round(rk(x.v2pariglef_ord).corr(rk(x.v2palgbt_ord)), 2)
side = lambda s: pd.cut(s, [-1, 2, 3, 6], labels=["esquerda(0-2)", "centro(3)", "direita(4-6)"])
L = ["# Eixo economico x posicao LGBT no V-Party v2 (exploratorio, ADENDO)", "",
     f"Base: {len(d)} partido-eleicoes com os dois escores, {d.country_text_id.nunique()} paises, {int(d.year.min())}-{int(d.year.max())}. Escalas: pariglef 0 extrema esquerda..6 extrema direita (economico); palgbt 0 opoe-se fortemente..4 apoia fortemente.", "",
     f"Spearman (todos os partidos): {sp(d)}. Spearman (so partidos do chefe de governo, pagovsup=0, n={len(d[d.v2pagovsup==0])}): {sp(d[d.v2pagovsup==0])}.", "",
     "## Partidos do chefe de governo desde 1990: posicao LGBT por lado do eixo economico", "",
     "| lado economico | n | opoe/opoe-se fortemente (palgbt<=1) | ambigua (2) | apoia (>=3) |", "|---|---|---|---|---|"]
g = d[(d.v2pagovsup == 0) & (d.year >= 1990)]
for lab, sub in g.groupby(side(g.v2pariglef_ord), observed=True):
    L.append(f"| {lab} | {len(sub)} | {(sub.v2palgbt_ord<=1).mean():.0%} | {(sub.v2palgbt_ord==2).mean():.0%} | {(sub.v2palgbt_ord>=3).mean():.0%} |")
L += ["", "## Por regime (RoW no ano da eleicao), partidos do chefe de governo desde 1990", "", "| regime RoW | n | Spearman econ x LGBT | % opoe (palgbt<=1) |", "|---|---|---|---|"]
R = {0: "autocracia fechada", 1: "autocracia eleitoral", 2: "democracia eleitoral", 3: "democracia liberal"}
for rg, sub in g.groupby("v2x_regime"):
    L.append(f"| {R.get(int(rg), rg)} | {len(sub)} | {sp(sub)} | {(sub.v2palgbt_ord<=1).mean():.0%} |")
L += ["", "Leitura: descritiva. O V-Party mede o PARTIDO (expert survey), nao a conduta do governo; nao cobre monarquias, teocracias nem partidos sem codificacao; vai ate 2019."]
open(O, "w").write("\n".join(L) + "\n")
print("\n".join(L))
