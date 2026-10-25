"""H1 (EXPLORATÓRIO, não pré-especificado: a ideia surgiu depois de ler o texto do Atlas 2025 p.21, onde o próprio Ipea/FBSP atribui a queda de ocultos em 2023 à 'repercussão' do Atlas 2024):
as UFs com programa de metas (7 de h1_programas_metas.csv) reagiram mais do que as demais à exposição pública da MVCI em 2023, e isso reverteu em 2024?
Estatística: média de log(MVCI_t/MVCI_t-1) (Y10-Y34, SIM/TabNet) tratadas - controles; p por permutação de rótulos (UF), 20000 sorteios, semente fixa.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h1_04_exposicao_2023_exploratorio.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import numpy as np, pandas as pd
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
s = pd.read_csv(f"{B}/dados/h1_sim_tabnet_uf_ano.csv"); p = pd.read_csv(f"{B}/dados/h1_programas_metas.csv")
tr = set(p.cod_uf); M = s.pivot(index="cod_uf", columns="ano", values="indet_Y10_Y34").astype(float)
rng = np.random.default_rng(20261022); out = []
for a, b in ((2021, 2022), (2022, 2023), (2023, 2024), (2022, 2024)):
    d = np.log((M[b] + 1) / (M[a] + 1)); t = d[d.index.isin(tr)]; c = d[~d.index.isin(tr)]
    obs = t.mean() - c.mean(); idx = d.index.values; perm = []
    for _ in range(20000):
        pick = rng.choice(len(idx), len(t), replace=False); m = np.zeros(len(idx), bool); m[pick] = True
        perm.append(d.values[m].mean() - d.values[~m].mean())
    perm = np.array(perm)
    out.append(dict(de=a, para=b, dlog_tratadas=t.mean(), dlog_controles=c.mean(), diferenca=obs, p_perm=float(np.mean(np.abs(perm) >= abs(obs))),
                    n_trat=len(t), n_ctrl=len(c), mvci_trat_ini=int(M.loc[list(tr), a].sum()), mvci_trat_fim=int(M.loc[list(tr), b].sum()),
                    mvci_ctrl_ini=int(M.loc[~M.index.isin(tr), a].sum()), mvci_ctrl_fim=int(M.loc[~M.index.isin(tr), b].sum())))
r = pd.DataFrame(out); r.to_csv(f"{B}/dados/h1_exposicao_2023_exploratorio.csv", index=False); print(r.round(3).to_string())
