"""H1: UFs com programas formais de metas/redução de homicídios têm MAIOR parcela de mortes de intenção indeterminada (Y10-Y34) depois do início do programa?
Desenho: diferenças-em-diferenças por coorte (janela pré 4 anos x janela pós H anos) contra UFs sem programa documentado na busca (NÃO é "sem programa";
é "sem programa achado em fonte oficial"), event study 2x2 limpo, TWFE com wild-cluster bootstrap, inferência por randomização (placebo de atribuição de UFs).
Desfechos: Y1 = Y10-Y34/(X85-Y09 + Y35-Y36 + Y10-Y34) (SIM/TabNet 1996-2024, contagem bruta); Y2 = ocultos/(registrados+ocultos) (Cerqueira & Lins 2024, modelo ML; TD 3015 1996-2021).
Semente fixa. Rodar: /opt/homebrew/bin/python3.14 -I scripts/h1_03_analise.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import numpy as np, pandas as pd, itertools, json
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
SEED = 20261021
sim = pd.read_csv(f"{B}/dados/h1_sim_tabnet_uf_ano.csv")
sim["reg"] = sim.agressao_X85_Y09 + sim.interv_Y35_Y36
sim["y1"] = sim.indet_Y10_Y34 / (sim.reg + sim.indet_Y10_Y34)
at = pd.read_csv(f"{B}/dados/h1_atlas_td_uf_ano.csv")
td = at[at.fonte == "td3015"].pivot_table(index=["cod_uf", "ano"], columns="tabela", values="valor").reset_index()
td["y2"] = td.ocultos / (td.registrados + td.ocultos)
sim = sim.merge(td[["cod_uf", "ano", "y2"]], on=["cod_uf", "ano"], how="left")
prog = pd.read_csv(f"{B}/dados/h1_programas_metas.csv")
UFS = sorted(sim.cod_uf.unique()); TREAT = dict(zip(prog.cod_uf, prog.ano_inicio_primario))
rng = np.random.default_rng(SEED)

def wide(col, df=sim): return df.pivot(index="cod_uf", columns="ano", values=col)

class Painel:
    """matriz UF x ano em numpy (NaN = sem dado) para acelerar bootstrap/randomização."""
    def __init__(self, W):
        self.A = W.values.astype(float); self.u = {u: i for i, u in enumerate(W.index)}; self.a = {a: j for j, a in enumerate(W.columns)}
    def cols(self, anos): return [self.a[x] for x in anos if x in self.a]

def att_coorte(W, treated, starts, ctrl, lag=0, H=4, npre=4):
    """média sobre UFs tratadas de (pós-pré tratada) - (pós-pré média dos controles); janelas por coorte; retorna {uf: att}."""
    if not isinstance(W, Painel): W = Painel(W)
    out = {}; ci = [W.u[c] for c in ctrl]
    for u, s in zip(treated, starts):
        pre = W.cols(range(s - npre, s)); post = W.cols(range(s + lag, s + lag + H))
        if len(pre) < 2 or len(post) < 2: continue
        A = W.A
        d_t = np.nanmean(A[W.u[u], post]) - np.nanmean(A[W.u[u], pre])
        d_c = np.nanmean(np.nanmean(A[np.ix_(ci, post)], axis=1) - np.nanmean(A[np.ix_(ci, pre)], axis=1))
        out[u] = d_t - d_c
    return out

def media(d): return float(np.mean(list(d.values()))) if d else np.nan

def inferir(W, tag, lag=0, H=4, B_=5000, R=10000):
    W = Painel(W)
    treated = list(TREAT); starts = [TREAT[u] for u in treated]; ctrl = [u for u in UFS if u not in TREAT]
    obs = att_coorte(W, treated, starts, ctrl, lag, H); a = media(obs)
    # bootstrap de UFs dentro de cada braço
    bs = []
    for _ in range(B_):
        ti = rng.integers(0, len(treated), len(treated)); ci = rng.integers(0, len(ctrl), len(ctrl))
        d = att_coorte(W, [treated[i] for i in ti], [starts[i] for i in ti], [ctrl[i] for i in ci], lag, H); bs.append(media(d))
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    # randomização: atribui os mesmos 7 anos de início a 7 UFs sorteadas das 27 (hipótese nula forte: sem efeito em ninguém)
    perm = []
    for _ in range(R):
        pick = rng.choice(UFS, len(treated), replace=False); st = rng.permutation(starts)
        c = [u for u in UFS if u not in pick]
        perm.append(media(att_coorte(W, list(pick), list(st), c, lag, H)))
    perm = np.array(perm); p = float(np.mean(np.abs(perm) >= abs(a) - 1e-12))
    return dict(desfecho=tag, lag=lag, H=H, n_tratadas=len(obs), att=a, ic95_boot_lo=lo, ic95_boot_hi=hi, p_randomizacao=p,
                nulo_p2_5=float(np.percentile(perm, 2.5)), nulo_p97_5=float(np.percentile(perm, 97.5)), sd_nulo=float(perm.std()),
                mde_80pct=float(2.8 * perm.std()), por_uf=obs)

def event_study(W0, kmin=-5, kmax=7):
    W = W0
    treated = list(TREAT); ctrl = [u for u in UFS if u not in TREAT]; rows = []
    for k in range(kmin, kmax + 1):
        if k == -1: continue
        v = []
        for u in treated:
            s = TREAT[u]
            if s + k in W.columns and s - 1 in W.columns:
                v.append((W.loc[u, s + k] - W.loc[u, s - 1]) - (W.loc[ctrl, s + k] - W.loc[ctrl, s - 1]).mean())
        v = np.array(v)
        bs = [np.mean(rng.choice(v, len(v))) for _ in range(5000)]
        rows.append(dict(k=k, n_ufs=len(v), att=v.mean(), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5)))
    return pd.DataFrame(rows)

def twfe_wild(W, B_=9999):
    """TWFE y ~ D + efeitos fixos de UF e ano em painel balanceado (anos com qualquer NaN são descartados); D=1 a partir do ano de início primário.
    Dentro-transformação exata (x - média linha - média coluna + média geral). Wild cluster bootstrap (Rademacher, H0 imposta) com 27 clusters."""
    W = W.dropna(axis=1, how="any"); ufs = list(W.index); anos = list(W.columns)
    Y = W.values.astype(float); D = np.array([[1.0 if (u in TREAT and a >= TREAT[u]) else 0.0 for a in anos] for u in ufs])
    dm = lambda X: X - X.mean(1, keepdims=True) - X.mean(0, keepdims=True) + X.mean()
    Dw = dm(D); den = (Dw ** 2).sum()
    def est(Yy):
        Yw = dm(Yy); b = (Dw * Yw).sum() / den; e = Yw - b * Dw
        se = np.sqrt(((Dw * e).sum(1) ** 2).sum()) / den
        return b, b / se
    b0, t0 = est(Y)
    Yw0 = dm(Y); fit = Y - Yw0  # modelo restrito (sem D): parte explicada pelos efeitos fixos
    tb = np.empty(B_)
    for i in range(B_):
        w = rng.choice([-1.0, 1.0], len(ufs))[:, None]
        tb[i] = est(fit + Yw0 * w)[1]
    return dict(b=float(b0), t=float(t0), p_wild=float(np.mean(np.abs(tb) >= abs(t0))), n_anos=len(anos), anos=f"{anos[0]}-{anos[-1]}")

if __name__ == "__main__":
    res = []; es_tabs = {}
    W1 = wide("y1"); W2 = wide("y2")
    for tag, W in (("y1_mvci_share", W1), ("y2_ocultos_share_TD3015", W2)):
        for lag, H in ((0, 4), (1, 4), (0, 7), (1, 7)):
            r = inferir(W, tag, lag, H); res.append(r)
            print(tag, lag, H, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "por_uf"})
        es_tabs[tag] = event_study(W); print(es_tabs[tag].round(3).to_string())
        print("TWFE", tag, twfe_wild(W))
    # robustez (a UF retirada sai do painel, não passa a controle): sem MG (sem meta formal), sem ES (descontinuado), sem CE/BA/PB (conservador), exclui 2023-24 (efeito exposição Atlas 2024)
    robust = []
    base_treat = dict(TREAT); UFS_full = list(UFS)
    for nome, drop in (("sem_MG", [31]), ("sem_ES", [32]), ("so_meta_formal(PE,RJ,BA,PB,CE)", [31, 32]), ("sem_RJ", [33])):
        TREAT.clear(); TREAT.update({u: s for u, s in base_treat.items() if u not in drop})
        UFS[:] = [u for u in UFS_full if u not in drop]   # a UF retirada sai do painel (NÃO vira controle)
        r = inferir(W1, "y1_" + nome, 0, 4, B_=2000, R=4000); robust.append(r)
        print("ROB", nome, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "por_uf"})
    TREAT.clear(); TREAT.update(base_treat)
    UFS[:] = UFS_full
    W1x = W1.drop(columns=[2023, 2024]); r = inferir(W1x, "y1_sem_2023_2024", 0, 4, B_=2000, R=4000); robust.append(r)
    print("ROB sem 2023-24", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "por_uf"})
    rows = [{k: v for k, v in r.items() if k != "por_uf"} for r in res + robust]
    pd.DataFrame(rows).to_csv(f"{B}/dados/h1_resultados_did.csv", index=False)
    pu = []
    for r in res:
        for u, v in r["por_uf"].items(): pu.append(dict(desfecho=r["desfecho"], lag=r["lag"], H=r["H"], cod_uf=u, att_uf=v))
    pd.DataFrame(pu).to_csv(f"{B}/dados/h1_resultados_por_uf.csv", index=False)
    pd.concat([t.assign(desfecho=k) for k, t in es_tabs.items()]).to_csv(f"{B}/dados/h1_event_study.csv", index=False)
