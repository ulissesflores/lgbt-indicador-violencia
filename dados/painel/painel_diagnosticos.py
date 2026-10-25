"""Diagnósticos metodológicos do painel UF x ano (ideologia do governador x taxa de homicídio por grupo). NÃO altera o modelo principal; testa suas premissas.
Entradas: painel_uf_ano_tse_brc.csv (partido de ELEIÇÃO, TSE + ideologia BRC por período; apresentado primeiro por ser a especificação mais defensável, ESCOLHIDA DEPOIS de ver os resultados das variantes: sem pré-especificação), painel_uf_ano_tse.csv e painel_uf_ano.csv (escore único de 2018). Todas concluem o mesmo.
Modelo base: ln(taxa) = b*ideologia + EF(UF) + EF(ano), EP agrupado por UF (CR1).
Diagnósticos:
  D1 inferência com poucos clusters (G=27): bootstrap wild-cluster-t (Rademacher, hipótese nula imposta), B=4999.
  D2 teste de lead (placebo temporal): adiciona ideologia(t+1); se o governo FUTURO "prevê" o homicídio de hoje, há tendência/seleção, não efeito. Só se identifica nas transições de governador: poder baixo, "sem pré-tendência" = ausência de evidência de pré-tendência.
  D3 tendência por UF: adiciona UF x tendência linear (captura melhora de completude/queda secular diferenciada por UF).
  D4 completude racial: para negros/não negros, controla pela parcela de óbitos sem raça/cor informada no UF-ano (total - negros - não negros).
  D5 variação disponível: quanto da ideologia varia DENTRO da UF (a identificação vem só daí) e limites de efeito que o desenho consegue excluir (IC95%; IC90 sem margem de equivalência declarada).
  D6 tratamento binário direita/esquerda (limiar Bolognesi 5,5) em vez de contínuo.
Rodar: /opt/homebrew/bin/python3.14 -I dados/painel/painel_diagnosticos.py   (semente fixa)
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, math
import numpy as np

BASE = (REPO_ROOT + "/dados")
RNG = np.random.default_rng(20261021)
OUTCOMES = ["tx_total", "tx_homens", "tx_mulheres", "tx_negros", "tx_nao_negros", "tx_arma"]


def carrega(arq):
    return list(csv.DictReader(open(f"{BASE}/painel/{arq}", encoding="utf-8")))


def completude():
    """parcela de óbitos por agressão sem raça/cor (UF-ano): 1 - (negros+não negros)/total, de dados/atlas_uf_series.csv."""
    v = {}
    for r in csv.DictReader(open(f"{BASE}/atlas_uf_series.csv", encoding="utf-8")):
        if r["valor"] and r["variavel"] in ("homicidios_total_n", "homicidios_negros_n", "homicidios_nao_negros_n"):
            v.setdefault((r["uf"], int(r["ano"])), {})[r["variavel"]] = float(r["valor"])
    return {k: 1 - (x["homicidios_negros_n"] + x["homicidios_nao_negros_n"]) / x["homicidios_total_n"] for k, x in v.items() if x.get("homicidios_total_n")}


def dummies(rows, trend=False):
    ufs = sorted({r["uf"] for r in rows}); anos = sorted({int(r["ano"]) for r in rows})
    cols = [[1.0 if r["uf"] == u else 0.0 for r in rows] for u in ufs]                 # EF(UF) completo (sem constante)
    cols += [[1.0 if int(r["ano"]) == a else 0.0 for r in rows] for a in anos[1:]]      # EF(ano), uma de referência
    if trend:
        t0 = anos[0]
        cols += [[(int(r["ano"]) - t0) if r["uf"] == u else 0.0 for r in rows] for u in ufs[1:]]
    return np.array(cols).T


def residuador(F):
    return np.eye(len(F)) - F @ np.linalg.pinv(F)


def cr1(xt, e, cl, k):
    """EP clusterizado CR1 do coeficiente único de x (já residualizado em FE). xt pode ser matriz n x p; devolve cov p x p."""
    xt = xt.reshape(len(xt), -1); n, p = xt.shape; G = len(set(cl))
    XtX_inv = np.linalg.inv(xt.T @ xt)
    meat = sum(np.outer(xt[cl == g].T @ e[cl == g], xt[cl == g].T @ e[cl == g]) for g in set(cl))
    return (G / (G - 1)) * ((n - 1) / (n - k)) * XtX_inv @ meat @ XtX_inv


def ols_fwl(y, X, M, cl, kfe):
    """coeficientes de X (n x p) controlando FE via M; EP CR1; devolve b, se, e residual."""
    X = X.reshape(len(y), -1); xt = M @ X; yt = M @ y
    b = np.linalg.solve(xt.T @ xt, xt.T @ yt); e = yt - xt @ b
    V = cr1(xt, e, cl, kfe + X.shape[1])
    return b, np.sqrt(np.diag(V)), e, xt, yt


def wild_p(y, x, M, cl, kfe, B=4999):
    """bootstrap wild-cluster-t com H0: b=0 imposta (modelo restrito = só FE). p bicaudal."""
    xt = M @ x; yt = M @ y
    b, se, _, _, _ = ols_fwl(y, x, M, cl, kfe); t_obs = b[0] / se[0]
    ycs = sorted(set(cl)); idx = {g: np.where(cl == g)[0] for g in ycs}
    er = yt  # resíduo do modelo restrito = y residualizado nos EF
    fit = y - yt
    cont = 0
    for _ in range(B):
        w = np.empty(len(y)); sig = RNG.choice([-1.0, 1.0], len(ycs))
        for s, g in zip(sig, ycs):
            w[idx[g]] = s
        ys = fit + er * w
        bs, ses, _, _, _ = ols_fwl(ys, x, M, cl, kfe)
        cont += abs(bs[0] / ses[0]) >= abs(t_obs) - 1e-12
    return (1 + cont) / (B + 1), t_obs


def prepara(rows, outcome, extra=None):
    rows = [r for r in rows if float(r[outcome]) > 0]
    return rows


def bloco(nome, arq, L, comp):
    rows0 = carrega(arq)
    L += [f"## {nome}", ""]
    ufs = sorted({r["uf"] for r in rows0})
    # D5 variação dentro da UF
    ide = {(r["uf"], int(r["ano"])): float(r["ideologia"]) for r in rows0}
    dentro = []; mud = 0
    for u in ufs:
        v = [ide[(u, a)] for a in sorted(a for (uu, a) in ide if uu == u)]
        dentro += list(np.array(v) - np.mean(v)); mud += (max(v) - min(v) > 1.0)
    L += [f"D5. Variação de ideologia: DP total {np.std(list(ide.values())):.2f}; DP DENTRO da UF {np.std(dentro):.2f} (é daí que vem a identificação); UFs com mudança > 1 ponto no período: {mud} de {len(ufs)}.", ""]
    L += ["| desfecho | b (EP) base | wild-cluster p | b com lead(t+1): coef ideologia(t) / coef lead(t+1) (p lead) | b com tendência por UF (EP) | b binário direita (EP) | IC90 base (sem margem de equivalência declarada) |", "|---|---|---|---|---|---|---|"]
    for oc in OUTCOMES:
        rows = prepara(rows0, oc)
        y = np.log(np.array([float(r[oc]) for r in rows])); x = np.array([float(r["ideologia"]) for r in rows])
        cl = np.array([r["uf"] for r in rows]); F = dummies(rows); M = residuador(F); kfe = np.linalg.matrix_rank(F)
        b, se, _, _, _ = ols_fwl(y, x, M, cl, kfe)
        p, _ = wild_p(y, x, M, cl, kfe)
        # lead
        key = {(r["uf"], int(r["ano"])): r for r in rows}
        sub = [r for r in rows if (r["uf"], int(r["ano"]) + 1) in key]
        ys = np.log(np.array([float(r[oc]) for r in sub])); xs = np.array([[float(r["ideologia"]), float(key[(r["uf"], int(r["ano"]) + 1)]["ideologia"])] for r in sub])
        cls = np.array([r["uf"] for r in sub]); Fs = dummies(sub); Ms = residuador(Fs)
        bl, sel, _, _, _ = ols_fwl(ys, xs, Ms, cls, np.linalg.matrix_rank(Fs))
        pl = 2 * (1 - 0.5 * (1 + math.erf(abs(bl[1] / sel[1]) / math.sqrt(2))))
        # tendência por UF
        Ft = dummies(rows, True); Mt = residuador(Ft)
        bt, set_, _, _, _ = ols_fwl(y, x, Mt, cl, np.linalg.matrix_rank(Ft))
        # binário
        xb = (x > 5.5).astype(float)
        bb, seb, _, _, _ = ols_fwl(y, xb, M, cl, kfe)
        L.append(f"| {oc} | {b[0]:+.4f} ({se[0]:.4f}) | {p:.3f} | {bl[0]:+.4f} / {bl[1]:+.4f} (p={pl:.2f}) | {bt[0]:+.4f} ({set_[0]:.4f}) | {bb[0]:+.3f} ({seb[0]:.3f}) | [{b[0]-1.645*se[0]:+.3f}; {b[0]+1.645*se[0]:+.3f}] |")
    # D4 completude racial
    L += ["", "D4. Desfechos por raça com controle da parcela de óbitos sem raça/cor no UF-ano:", "", "| desfecho | b base (EP) | b com controle de completude (EP) |", "|---|---|---|"]
    for oc in ("tx_negros", "tx_nao_negros"):
        rows = [r for r in prepara(rows0, oc) if (r["uf"], int(r["ano"])) in comp]
        y = np.log(np.array([float(r[oc]) for r in rows])); x = np.array([float(r["ideologia"]) for r in rows])
        c = np.array([comp[(r["uf"], int(r["ano"]))] for r in rows]); cl = np.array([r["uf"] for r in rows])
        F = dummies(rows); M = residuador(F); kfe = np.linalg.matrix_rank(F)
        b, se, _, _, _ = ols_fwl(y, x, M, cl, kfe)
        b2, se2, _, _, _ = ols_fwl(y, np.column_stack([x, c]), M, cl, kfe)
        L.append(f"| {oc} | {b[0]:+.4f} ({se[0]:.4f}) | {b2[0]:+.4f} ({se2[0]:.4f}) |")
    L.append("")


def main():
    comp = completude()
    L = ["# Diagnósticos do painel UF x ano (gerado por painel_diagnosticos.py, semente 20261021)", "",
         "Convenção: b = variação aproximada de ln(taxa) por 1 ponto de ideologia (escala 0-10, 5 pontos ≈ distância PT -> DEM); b=0,01 ≈ 1% por ponto. EP agrupado por UF (CR1, G=27).", ""]
    bloco("Versão principal (2026-10-21): partido de ELEIÇÃO (TSE) + ideologia BRC POR PERÍODO (onda 2018 p/ 2012-20; onda 2022 p/ 2021-24)", "painel_uf_ano_tse_brc.csv", L, comp)
    bloco("Secundária: partido de ELEIÇÃO (TSE) + escore único Bolognesi 2018", "painel_uf_ano_tse.csv", L, comp)
    bloco("Secundária: partido em exercício (Wikipédia curada e corrigida) + escore único Bolognesi 2018", "painel_uf_ano.csv", L, comp)
    open(f"{BASE}/painel/diagnosticos.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
