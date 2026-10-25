"""H2: UFs que não informam (ou informam inexistente) 'racismo por homofobia/transfobia' no Anuário FBSP têm MENOS estrutura estadual especializada (ESTADIC 2019/2023)?
Anuário: dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv (UF x ano de dados 2022-2025, última edição que traz o ano). Nenhum UF informou '0' numérico: o 'zero cerimonial' aparece como '...' (nd) ou '-' (inexistente).
Desfechos: Z = nº de UF-anos 2022-2025 com nd/inexistente (0-4); Zbin = Z>=1; taxa 2024 por 100 mil (SIM/IBGE pop de dados/atlas_uf_series.csv) entre UFs informantes.
Estrutura: índice S = média de Sim (0/1) em 6 itens da ESTADIC (2019 e 2023; 'Não'=0, 'Sim'=1, Recusa/-=ausente), e binário C = comitê de enfrentamento à violência LGBTfóbica em alguma edição (EDHU5410).
Testes: Fisher exato (Zbin x C e Zbin x S>=mediana), Spearman Z x S com p por permutação (20000, semente fixa), AUC de S para discriminar Zbin com IC por bootstrap. Poder declarado por simulação.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h2_02_analise.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import numpy as np, pandas as pd
from scipy import stats
B = REPO_ROOT; F = f"{B}/research-2026-10-21-rodada3/F5-economia-politica"
rng = np.random.default_rng(20261024)
an = pd.read_csv(f"{B}/dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv"); an = an[an.uf != "BR"].sort_values("edicao")
latest = an.groupby(["uf", "ano_dado"]).tail(1)      # última edição que traz o UF-ano
COD = {"RO":11,"AC":12,"AM":13,"RR":14,"PA":15,"AP":16,"TO":17,"MA":21,"PI":22,"CE":23,"RN":24,"PB":25,"PE":26,"AL":27,"SE":28,"BA":29,"MG":31,"ES":32,"RJ":33,"SP":35,"PR":41,"SC":42,"RS":43,"MS":50,"MT":51,"GO":52,"DF":53}
latest = latest.assign(cod_uf=latest.uf.map(COD))
g = latest.groupby("cod_uf")
U = pd.DataFrame({"uf": g.uf.first(), "Z": g.marca.apply(lambda s: int((s != "valor").sum())), "n_anos": g.size()})
U["Zbin"] = (U.Z >= 1).astype(int)
est = pd.read_csv(f"{F}/dados/h2_estadic_lgbt_uf.csv"); V = ["EDHU086", "EDHU5410", "EDHU576", "ESEG4413", "ESEG487", "ESEG5913"]
for v in V: est[v] = est[v].map({"Sim": 1.0, "Não": 0.0})
est["S_ed"] = est[V].mean(axis=1, skipna=True)
S = est.groupby("cod_uf").agg(S=("S_ed", "mean"), C=("EDHU5410", "max"), S2019=("S_ed", lambda s: s.iloc[0]), n_edicoes=("EDHU086", "size"))
U = U.join(S)
at = pd.read_csv(f"{B}/dados/atlas_uf_series.csv"); pop = at[at.variavel == "homicidios_total_taxa"].merge(at[at.variavel == "homicidios_total_n"], on=["codigo_uf", "ano"], suffixes=("_t", "_n"))
pop["pop"] = pop.valor_n / pop.valor_t * 1e5; pop24 = pop[pop.ano == 2024].set_index("codigo_uf")["pop"]
l24 = latest[latest.ano_dado == 2024].set_index("cod_uf").registros; U["rate24"] = (l24 / pop24 * 1e5).reindex(U.index)
U.to_csv(f"{F}/dados/h2_uf_resumo.csv"); print(U.round(2).to_string())
res = []
def reg(nome, **k): res.append(dict(teste=nome, **k)); print(nome, k)
tab = pd.crosstab(U.Zbin, U.C.fillna(0)); reg("Fisher Zbin x C(comite LGBT em alguma edicao)", tabela=tab.values.tolist(), odds=stats.fisher_exact(tab)[0], p=stats.fisher_exact(tab)[1])
U["S_hi"] = (U.S >= U.S.median()).astype(int); tab2 = pd.crosstab(U.Zbin, U.S_hi); reg("Fisher Zbin x S>=mediana", tabela=tab2.values.tolist(), odds=stats.fisher_exact(tab2)[0], p=stats.fisher_exact(tab2)[1])
rho = stats.spearmanr(U.Z, U.S); perm = np.array([stats.spearmanr(rng.permutation(U.Z.values), U.S)[0] for _ in range(20000)])
reg("Spearman Z x S", rho=rho[0], p_perm=float(np.mean(np.abs(perm) >= abs(rho[0]))), n=len(U))
x1, x0 = U.S[U.Zbin == 1].values, U.S[U.Zbin == 0].values
auc = stats.mannwhitneyu(x0, x1).statistic / (len(x0) * len(x1))   # P(S nao-informante < S informante) -> AUC de S para 'informa'
bs = []
for _ in range(10000):
    a = rng.choice(x0, len(x0)); b = rng.choice(x1, len(x1)); bs.append((a[:, None] > b[None, :]).mean() + 0.5 * (a[:, None] == b[None, :]).mean())
reg("AUC S(informante) > S(nao informante)", auc=float(auc), ic95=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], n_nao_inf=int(len(x1)), n_inf=int(len(x0)))
# taxa 2024 entre informantes x S
ok = U.dropna(subset=["rate24", "S"]); r2 = stats.spearmanr(ok.rate24, ok.S)
pp = np.array([stats.spearmanr(rng.permutation(ok.rate24.values), ok.S)[0] for _ in range(20000)])
reg("Spearman taxa24/100k (informantes) x S", rho=r2[0], p_perm=float(np.mean(np.abs(pp) >= abs(r2[0]))), n=len(ok))
# poder: simula efeito verdadeiro em que S desloca a prob. de nao informar (OR 4) com as marginais observadas
def poder(or_, R=4000):
    n = len(U); hit = 0; p0 = U.Zbin.mean()
    for _ in range(R):
        s = rng.permutation(U.S_hi.values); lo = np.log(p0 / (1 - p0)); pz = 1 / (1 + np.exp(-(lo - np.log(or_) * (s - s.mean()))))
        z = rng.random(n) < pz; t = pd.crosstab(z, s).reindex(index=[False, True], columns=[0, 1], fill_value=0).values
        hit += stats.fisher_exact(t)[1] < 0.05
    return hit / R
for o in (2, 4, 8): reg(f"Poder Fisher (simulado) para OR verdadeiro de {o} (nao informar vs estrutura alta)", poder=poder(o))
pd.DataFrame(res).to_csv(f"{F}/dados/h2_resultados.csv", index=False)
