"""H3: a série de contagens da sociedade civil (GGB) cresce com a COBERTURA (internet), não só com a incidência (homicídios SIM)?
(a) Série nacional 2000-2024 (n=25): log GGB ~ log homicídios SIM (+ internet % ITU/Banco Mundial), níveis com Newey-West e primeiras diferenças com bootstrap de blocos.
(b) Painel UF (2021, 2023, 2024 = os únicos anos com tabela completa por UF nos relatórios do GGB lidos; 2022 tem só 135 de 256; 2017-2020 só rankings parciais) x
    % de domicílios com internet (PNAD Contínua TIC, SIDRA 7307; 2020 não existe): Poisson com EF de UF e ano, permutação de trajetórias entre UFs.
Semente fixa. Rodar: /opt/homebrew/bin/python3.14 -I scripts/h3_analise.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import json, numpy as np, pandas as pd
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
rng = np.random.default_rng(20261023)
sim = pd.read_csv(f"{B}/dados/h1_sim_tabnet_uf_ano.csv"); sim["reg"] = sim.agressao_X85_Y09 + sim.interv_Y35_Y36
nat = sim.groupby("ano")[["reg", "indet_Y10_Y34"]].sum()
ggb = pd.read_csv(f"{B}/dados/h3_ggb_nacional_2000_2024.csv").set_index("ano").ggb_mortes_violentas
wb = {int(x["date"]): x["value"] for x in json.load(open(f"{B}/dados/raw/wb_internet_bra.json"))[1] if x["value"] is not None}
D = pd.DataFrame({"ggb": ggb, "hom": nat.reg.reindex(ggb.index), "mvci": nat.indet_Y10_Y34.reindex(ggb.index), "net": pd.Series(wb).reindex(ggb.index)})
D["ly"] = np.log(D.ggb); D["lh"] = np.log(D.hom); D["lh2"] = np.log(D.hom + D.mvci)

def ols(y, X):
    X = np.column_stack([np.ones(len(y)), X]); b, *_ = np.linalg.lstsq(X, y, rcond=None); return b, y - X @ b, X
def nw(X, e, L=3):
    n = len(e); XtXi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None])
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = (X[l:] * e[l:, None]).T @ (X[:-l] * e[:-l, None]); S += w * (G + G.T)
    return np.sqrt(np.diag(XtXi @ S @ XtXi))
def bloco(y, X, L=3, R=10000):
    n = len(y); out = []
    for _ in range(R):
        starts = rng.integers(0, n, int(np.ceil(n / L))); idx = np.concatenate([(s + np.arange(L)) % n for s in starts])[:n]
        try: out.append(ols(y[idx], X[idx])[0])
        except Exception: pass
    return np.percentile(np.array(out), [2.5, 97.5], axis=0)

rows = []
def reporta(nome, y, X, cols, hac=False, boot=False, L=3):
    b, e, Xc = ols(y, X); r = dict(modelo=nome, n=len(y))
    se = nw(Xc, e) if hac else None
    ci = bloco(y, X, L)[:, 1:] if boot else None
    for j, c in enumerate(cols):
        r[f"b_{c}"] = b[j + 1]
        if hac: r[f"hac_se_{c}"] = se[j + 1]
        if boot: r[f"ic95_bloco_{c}"] = f"[{ci[0, j]:.4f}, {ci[1, j]:.4f}]"
    r["R2"] = 1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(); rows.append(r); return r

y = D.ly.values
reporta("N1 niveis: ly ~ net", y, D[["net"]].values, ["net"], hac=True, boot=True)
reporta("N2 niveis: ly ~ lh", y, D[["lh"]].values, ["lh"], hac=True, boot=True)
reporta("N3 niveis: ly ~ lh + net", y, D[["lh", "net"]].values, ["lh", "net"], hac=True, boot=True)
reporta("N3b niveis: ly ~ lh2(reg+MVCI) + net", y, D[["lh2", "net"]].values, ["lh2", "net"], hac=True, boot=True)
d = D.diff().dropna(); yd = d.ly.values
reporta("D1 diferencas: dly ~ dnet", yd, d[["net"]].values, ["dnet"], boot=True)
reporta("D2 diferencas: dly ~ dlh", yd, d[["lh"]].values, ["dlh"], boot=True)
reporta("D3 diferencas: dly ~ dlh + dnet", yd, d[["lh", "net"]].values, ["dlh", "dnet"], boot=True)
# antes/depois do pico de 2017 (internet segue subindo; a contagem cai)
for nome, lo, hi in (("pre_pico 2000-2017", 2000, 2017), ("pos_pico 2017-2024", 2017, 2024)):
    s = D.loc[lo:hi]; sd = s.diff().dropna()
    reporta(f"S {nome}: dly ~ dlh + dnet", sd.ly.values, sd[["lh", "net"]].values, ["dlh", "dnet"], boot=True, L=2)
    reporta(f"S {nome}: ly ~ net (niveis)", s.ly.values, s[["net"]].values, ["net"], boot=True, L=2)
res = pd.DataFrame(rows); res.to_csv(f"{B}/dados/h3_resultados_nacional.csv", index=False)
D.round(4).to_csv(f"{B}/dados/h3_serie_nacional_insumos.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(res.round(4).to_string())
print("corr Spearman ggb x hom 2000-2024:", round(D.ggb.rank().corr(D.hom.rank()), 3), "| ggb x net:", round(D.ggb.rank().corr(D.net.rank()), 3))
print("pico GGB:", D.ggb.idxmax(), D.ggb.max(), "| pico homicidios registrados:", D.hom.idxmax(), int(D.hom.max()), "| net 2017/2024:", round(D.net[2017], 1), round(D.net[2024], 1))

# ---------- (b) painel UF ----------
U = pd.read_csv(f"{B}/dados/h3_ggb_uf_ano_agregado.csv")
cod = {"RO":11,"AC":12,"AM":13,"RR":14,"PA":15,"AP":16,"TO":17,"MA":21,"PI":22,"CE":23,"RN":24,"PB":25,"PE":26,"AL":27,"SE":28,"BA":29,"MG":31,"ES":32,"RJ":33,"SP":35,"PR":41,"SC":42,"RS":43,"MS":50,"MT":51,"GO":52,"DF":53}
U["cod_uf"] = U.uf.map(cod)
S = json.load(open(f"{B}/dados/raw/sidra7307_dom_internet_uf.json"))[1:]
net = pd.DataFrame([dict(cod_uf=int(x["D1C"]), ano=int(x["D3N"]), net_dom=float(x["V"])) for x in S])
P = U.merge(net, on=["cod_uf", "ano"]).merge(sim[["cod_uf", "ano", "reg"]], on=["cod_uf", "ano"])
P["lh"] = np.log(P.reg); P.to_csv(f"{B}/dados/h3_painel_uf.csv", index=False)
def poisson_fe(P, cols, iters=60):
    ufs = sorted(P.cod_uf.unique()); anos = sorted(P.ano.unique())
    Z = np.column_stack([P[c].values for c in cols] + [(P.cod_uf == u).astype(float).values for u in ufs] + [(P.ano == a).astype(float).values for a in anos[1:]])
    y = P.ggb_mortes_violentas.values.astype(float); keep = np.ones(Z.shape[1], bool)
    # descarta UFs com soma zero (EF não identificado)
    for j, u in enumerate(ufs):
        if y[P.cod_uf.values == u].sum() == 0: keep[len(cols) + j] = False
    Z = Z[:, keep]; mu = np.full(len(y), y.mean()); eta = np.log(mu); beta = np.zeros(Z.shape[1])
    for _ in range(iters):
        z = eta + (y - mu) / mu; W = mu
        beta_new = np.linalg.lstsq(np.sqrt(W)[:, None] * Z, np.sqrt(W) * z, rcond=None)[0]
        eta = Z @ beta_new; mu = np.exp(np.clip(eta, -20, 20))
        if np.abs(beta_new - beta).max() < 1e-9: beta = beta_new; break
        beta = beta_new
    bread = np.linalg.pinv(Z.T @ (mu[:, None] * Z)); sc = Z * (y - mu)[:, None]
    meat = sum(np.outer(sc[(P.cod_uf.values == u)].sum(0), sc[(P.cod_uf.values == u)].sum(0)) for u in ufs)
    V = bread @ meat @ bread; return beta[:len(cols)], np.sqrt(np.diag(V))[:len(cols)]
out = []
for cols in (["net_dom"], ["lh"], ["lh", "net_dom"]):
    b, se = poisson_fe(P, cols)
    # permutação: embaralha trajetórias (net_dom,lh) entre UFs mantendo a ordem temporal dentro da UF
    perm = []
    base = P.sort_values(["cod_uf", "ano"]).reset_index(drop=True); ufs = sorted(base.cod_uf.unique())
    for _ in range(3000):
        sh = rng.permutation(ufs); Q = base.copy()
        for c in cols:
            M = base.pivot(index="cod_uf", columns="ano", values=c).loc[sh]; M.index = ufs
            Q[c] = [M.loc[u, a] for u, a in zip(Q.cod_uf, Q.ano)]
        perm.append(poisson_fe(Q, cols)[0])
    perm = np.array(perm)
    for j, c in enumerate(cols):
        out.append(dict(modelo="Poisson EF UF+ano: " + " + ".join(cols), coef=c, b=b[j], se_cluster=se[j], p_permutacao=float(np.mean(np.abs(perm[:, j]) >= abs(b[j]))),
                        n_obs=len(P), anos="2021,2023,2024", ufs=P.cod_uf.nunique()))
pd.DataFrame(out).to_csv(f"{B}/dados/h3_resultados_painel_uf.csv", index=False); print(pd.DataFrame(out).round(4).to_string())
