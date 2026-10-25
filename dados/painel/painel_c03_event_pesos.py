"""C03 (TRIAGEM, rodada 3) — Painel F8: (1) conversão exata de b em %, (2) event study empilhado nas trocas de governante, (3) pesos do TWFE contínuo.
Critérios de decisão escritos ANTES de rodar: research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md (hash em CRITERIOS.sha256).
Dados: dados/painel/painel_uf_ano_tse_brc.csv (principal; partido de eleição TSE + ideologia BRC por período, 351 UF-anos) e, como conferência, painel_uf_ano_tse.csv (escore único de 2018).
Reprodução obrigatória (aborta): b e EP dos 6 desfechos e da robustez BLS9 (resultados_tse_brc.md); 94 = 67 trocas reais + 27 trocas de onda (painel BRC); 68 mudanças = 37 direita + 31 esquerda (painel tse).
MÉTODO
 (1) 100[exp(k b)-1] aplicado aos limites b ± 1,96 EP publicados (k = 5 pontos; BLS9: k = distância BLS9-2021 PT->DEM e PT->PL).
 (2) Evento = UF-ano em que o PARTIDO do governador muda e a ideologia muda (Δ != 0); trocas de onda no mesmo partido NÃO são eventos nem contaminação. Direção pelo sinal de Δ (maior = direita).
     Pilha por evento: UF tratada + UFs controle limpas, anos e-3..e+3, ln(taxa); EF de UF x pilha e de ano x pilha (FWL via mínimos quadrados); beta_tau, tau em {-3,-2,0,1,2,3}, referência tau=-1.
     Desenho ESTRITO (principal): janela completa (evento 2015-2021), tratado e controles sem outra troca real em (e-3, e+3]. Desenho TRUNCADO (sensibilidade, pré-fixado): janela dentro da faixa de ideologia constante
     (tau de max(-3, 2012-e, ano da troca anterior - e) a min(+3, ano da próxima troca - e - 1, 2024 - e), exigindo tau_min <= -2); controles sem troca na janela usada.
     EP agrupado por UF (CR1 com K = p + FE de ano x pilha: os FE de UF x pilha estão aninhados no cluster e não entram em K, convenção reghdfe); IC95% com t(G-1); testes conjuntos F(q, G-1) de antecipações (tau=-3,-2) e pós (tau=0..3).
 (3) eps = resíduo de D (ideologia) nos EF de UF e ano; b+ = soma(eps+ y~)/soma(eps+ eps), b- análogo (y~ = desfecho residualizado), EP por UF (IV com instrumento eps+ / eps-), IC95% t(26);
     massa de peso negativo sob eps, eps x (D - D_i) e eps x (D - D_bar).
LIMITES: poucos eventos limpos (ver n em cada tabela); 27 clusters (testes conjuntos anticonservadores); event study com tratamento de ideologia reversível e controles que já tiveram/terão troca em outro ano (limpeza só dentro da janela);
 tendências paralelas condicionais a EF de pilha NÃO testadas além das antecipações; sem poder para efeitos pequenos; "pesos negativos" de um regressor contínuo dependem da origem de D (3 variantes mostradas);
 exploratório, NÃO causal; SIM sem motivação; o 'estimado' do Atlas não entra.
Rodar: /opt/homebrew/bin/python3.14 -I dados/painel/painel_c03_event_pesos.py   Saídas: dados/painel/c03_event_pesos_resultados.md e c03_event_pesos_resultados.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, math, re, collections
import numpy as np
from scipy import stats

D = (REPO_ROOT + "/dados")
ZP = (REPO_ROOT + "/fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab")
OUT = ["tx_total", "tx_homens", "tx_mulheres", "tx_negros", "tx_nao_negros", "tx_arma"]
EVOUT = ["tx_total", "tx_mulheres", "tx_negros", "tx_arma"]
TAUS = [-3, -2, 0, 1, 2, 3]; Y0, Y1 = 2012, 2024


def carrega(arq):
    r = list(csv.DictReader(open(f"{D}/painel/{arq}", encoding="utf-8")))
    by = collections.defaultdict(dict)
    for x in r: by[x["uf"]][int(x["ano"])] = x
    return r, by


def demean2(v, uf, ano):
    v = v.copy()
    for _ in range(100):
        for g in (uf, ano):
            for k in np.unique(g): v[g == k] -= v[g == k].mean()
    return v


def twfe(y, x, uf, ano):
    y = np.array(y, float); x = np.array(x, float); uf = np.array(uf); ano = np.array(ano)
    yd, xd = demean2(y, uf, ano), demean2(x, uf, ano)
    b = (xd @ yd) / (xd @ xd); e = yd - b * xd
    S = sum((xd[uf == k] @ e[uf == k]) ** 2 for k in np.unique(uf)); G = len(np.unique(uf)); n = len(y); k = 1 + G + len(np.unique(ano)) - 1
    return b, math.sqrt(S / (xd @ xd) ** 2 * G / (G - 1) * (n - 1) / (n - k)), yd, xd


# ================= reprodução =================
rows, by = carrega("painel_uf_ano_tse_brc.csv"); rowsT, byT = carrega("painel_uf_ano_tse.csv")
assert len(rows) == 351 and len(by) == 27
pub = {}; pubz = {}; sec = 0
for l in open(f"{D}/painel/resultados_tse_brc.md", encoding="utf-8"):
    m = re.match(r"\| (tx_\w+) \| ([+-]\d\.\d{4}) \| (\d\.\d{4}) \| \[([+-]\d\.\d{3}), ([+-]\d\.\d{3})\]", l)
    if m: pub.setdefault(m.group(1), (float(m.group(2)), float(m.group(3))))
    m = re.match(r"\| (tx_\w+) \| ([+-]\d\.\d{4}) \| (\d\.\d{4}) \| \[([+-]\d\.\d{3}), ([+-]\d\.\d{3})\] \|$", l)
    if "BLS9" in l: sec = 1
    if sec and m: pubz[m.group(1)] = (float(m.group(2)), float(m.group(3)))
assert len(pub) == 6 and len(pubz) == 6, (pub, pubz)
B = {}
for o in OUT:
    r = [x for x in rows if float(x[o]) > 0]
    b, se, _, _ = twfe([math.log(float(x[o])) for x in r], [float(x["ideologia"]) for x in r], [x["uf"] for x in r], [int(x["ano"]) for x in r])
    assert abs(b - pub[o][0]) < 5.1e-5 and abs(se - pub[o][1]) < 5.1e-5 and len(r) == 351, (o, b, se, pub[o])
    B[o] = (b, se)
# BLS9 (cópia da lógica do painel_f8.py: escore Zucco & Power 2021 pesado por meses de mandato; partidos sem escore descartados)
zp = {}
for r in csv.DictReader(open(ZP)):
    if r["year"] == "2021": zp[r["party.or.pres"].upper()] = float(r["ideo"])
ZMAP = {'PMDB': 'MDB', 'PP': 'PP', 'PROGRESSISTAS': 'PP', 'PR': 'PL', 'PRB': 'REPUBLICANOS', 'PPS': 'CIDADANIA', 'SD': 'SOLIDARIEDADE', 'SDD': 'SOLIDARIEDADE', 'UNIÃO BRASIL': 'DEM', 'UNIÃO': 'DEM', 'PATRIOTA': 'PATRIOTA', 'PROS': 'PROS', 'PTB': 'PTB'}
def zscore(p):
    P = p.strip().upper()
    for c in (P, ZMAP.get(P, "")):
        if c in zp: return zp[c]
    return None
from datetime import date
gov2 = collections.defaultdict(list)
for r in csv.DictReader(open(f"{D}/governadores_uf_2011_2026_tse.csv", encoding="utf-8")):
    s = zscore(r["partido"])
    if s is None: continue
    try: a = date.fromisoformat(r["inicio"]); b_ = date.fromisoformat(r["fim"]); meses = max(1, (b_ - a).days / 30.4)
    except Exception: meses = 12
    gov2[(r["uf"], int(r["ano"]))].append((s, meses))
rows2 = []
for r in rows:
    g = gov2.get((r["uf"], int(r["ano"])))
    if g: rows2.append(dict(r, zp=sum(s * m for s, m in g) / sum(m for _, m in g)))
BZ = {}
for o in OUT:
    r = [x for x in rows2 if float(x[o]) > 0]
    b, se, _, _ = twfe([math.log(float(x[o])) for x in r], [x["zp"] for x in r], [x["uf"] for x in r], [int(x["ano"]) for x in r])
    assert abs(b - pubz[o][0]) < 5.1e-5 and abs(se - pubz[o][1]) < 5.1e-5 and len(rows2) == 341, ("BLS9", o, b, se, pubz[o], len(rows2))
    BZ[o] = (b, se)
dPT, dDEM, dPL = zp["PT"], zp["DEM"], zp["PL"]; kz = {"DEM": dDEM - dPT, "PL": dPL - dPT}


def eventos(by_):
    """trocas reais: partido muda E ideologia muda; trocas de onda: ideologia muda com o mesmo partido."""
    real = []; onda = 0; mud = 0; up = dn = 0
    for u, d in by_.items():
        ys = sorted(d)
        for a, b in zip(ys, ys[1:]):
            di = float(d[b]["ideologia"]) - float(d[a]["ideologia"])
            if abs(di) > 1e-9:
                mud += 1; up += di > 0; dn += di < 0
                if d[b]["partido"] != d[a]["partido"]: real.append((u, b, 1 if di > 0 else -1))
                else: onda += 1
    return real, onda, mud, up, dn


ev1, onda1, mud1, up1, dn1 = eventos(by); ev2, onda2, mud2, up2, dn2 = eventos(byT)
assert mud1 == 94 and len(ev1) == 67 and onda1 == 27, (mud1, len(ev1), onda1)
assert mud2 == 68 and up2 == 37 and dn2 == 31 and onda2 == 0, (mud2, up2, dn2, onda2)
dirs1 = collections.Counter(d for *_, d in ev1)

# ================= (2) event study empilhado =================
def monta_pilhas(by_, ev, direcao, desenho):
    evy = collections.defaultdict(list)
    for u, e, d in ev: evy[u].append(e)
    pilhas = []
    for (u, e, d) in ev:
        if d != direcao: continue
        outros = [y for y in evy[u] if y != e]
        if desenho == "estrito":
            if e - 3 < Y0 or e + 3 > Y1: continue
            if any(e - 3 < y <= e + 3 for y in outros): continue
            tmin, tmax = -3, 3
        else:
            prev = max([y for y in outros if y < e], default=None); nxt = min([y for y in outros if y > e], default=None)
            tmin = max(-3, Y0 - e, (prev - e) if prev is not None else -99)
            tmax = min(3, (nxt - e - 1) if nxt is not None else 99, Y1 - e)
            if tmin > -2 or tmax < 0: continue
        ctrl = [v for v in by_ if v != u and not any(e + tmin < y <= e + tmax for y in evy[v])]
        pilhas.append((u, e, tmin, tmax, ctrl))
    return pilhas


def estima_event(by_, pilhas, outcome):
    Y = []; Xc = []; fe_u = []; fe_a = []; cl = []
    cols = [t for t in TAUS if any(tmin <= t <= tmax for _, _, tmin, tmax, _ in pilhas)]
    for k, (u, e, tmin, tmax, ctrl) in enumerate(pilhas):
        for v in [u] + ctrl:
            for t in range(tmin, tmax + 1):
                x = by_[v].get(e + t)
                if x is None or float(x[outcome]) <= 0: continue
                Y.append(math.log(float(x[outcome]))); cl.append(v); fe_u.append((k, v)); fe_a.append((k, e + t))
                Xc.append([1.0 if (v == u and t == c) else 0.0 for c in cols])
    Y = np.array(Y); X = np.array(Xc); cl = np.array(cl)
    uu = {z: i for i, z in enumerate(sorted(set(fe_u)))}; aa = {z: i for i, z in enumerate(sorted(set(fe_a)))}
    F = np.zeros((len(Y), len(uu) + len(aa)))
    for i, (zu, za) in enumerate(zip(fe_u, fe_a)): F[i, uu[zu]] = 1; F[i, len(uu) + aa[za]] = 1
    Z = np.column_stack([X, Y]); coef = np.linalg.lstsq(F, Z, rcond=None)[0]; R = Z - F @ coef
    Xt, yt = R[:, :-1], R[:, -1]
    b = np.linalg.solve(Xt.T @ Xt, Xt.T @ yt); e = yt - Xt @ b
    G = len(set(cl)); n = len(Y); p = X.shape[1]
    Kfe = np.linalg.matrix_rank(F) - len(uu)            # FE de UF x pilha aninhados no cluster: fora de K
    A = np.linalg.inv(Xt.T @ Xt); meat = sum(np.outer(Xt[cl == g].T @ e[cl == g], Xt[cl == g].T @ e[cl == g]) for g in set(cl))
    V = G / (G - 1) * (n - 1) / (n - (p + Kfe)) * A @ meat @ A
    return cols, b, V, G, n, len(set(c for _, _, _, _, ctrl in pilhas for c in ctrl))


def waldF(cols, b, V, G, sel):
    idx = [cols.index(t) for t in sel if t in cols]
    if not idx: return None, None
    bb = b[idx]; VV = V[np.ix_(idx, idx)]; W = float(bb @ np.linalg.solve(VV, bb)); q = len(idx)
    return W / q, 1 - stats.f.cdf(W / q, q, G - 1)


def media_pos(cols, b, V, G):
    idx = [cols.index(t) for t in (0, 1, 2, 3) if t in cols]
    w = np.zeros(len(cols)); w[idx] = 1.0 / len(idx)
    m = float(w @ b); se = math.sqrt(float(w @ V @ w)); tc = stats.t.ppf(0.975, G - 1)
    return m, m - tc * se, m + tc * se


EVROWS = []; EVMD = []
for nome_painel, by_, ev_ in (("BRC (principal)", by, ev1), ("tse escore único (conferência)", byT, ev2)):
    for desenho in ("estrito", "truncado"):
        for direcao, rot in ((1, "esquerda->direita"), (-1, "direita->esquerda")):
            pil = monta_pilhas(by_, ev_, direcao, desenho)
            n_ev = len(pil)
            EVMD.append(f"\n### {nome_painel} — desenho {desenho} — {rot}: {n_ev} eventos" + (f" (anos: {dict(sorted(collections.Counter(e for _, e, *_ in pil).items()))})" if n_ev else ""))
            if n_ev < 2:
                EVMD.append("sem eventos suficientes."); EVROWS.append([nome_painel, desenho, rot, "-", n_ev, 0, 0, "n<2"] + [""] * 10); continue
            for oc in EVOUT:
                cols, b, V, G, n, nctrl = estima_event(by_, pil, oc)
                tc = stats.t.ppf(0.975, G - 1); se = np.sqrt(np.diag(V))
                Fl, pl = waldF(cols, b, V, G, (-3, -2)); Fp, pp = waldF(cols, b, V, G, (0, 1, 2, 3)); m, mlo, mhi = media_pos(cols, b, V, G)
                lead_ic = any((b[i] - tc * se[i] > 0 or b[i] + tc * se[i] < 0) for i, t in enumerate(cols) if t < 0)
                EVROWS.append([nome_painel, desenho, rot, oc, n_ev, nctrl, G, n] + [f"{b[i]:.4f}|{b[i]-tc*se[i]:.4f}|{b[i]+tc*se[i]:.4f}" if t in cols and (i := cols.index(t)) is not None else "" for t in TAUS] + [pl, pp, m, mlo, mhi, lead_ic])
                if oc == "tx_total" or desenho == "estrito":
                    EVMD.append(f"\n**{oc}** (n eventos {n_ev}, UFs controle distintas {nctrl}, clusters G={G}, obs {n})\n")
                    EVMD.append("| tau | " + " | ".join(str(t) for t in cols) + " |"); EVMD.append("|---|" + "---|" * len(cols))
                    EVMD.append("| beta [IC95% t] | " + " | ".join(f"{b[i]:+.3f} [{b[i]-tc*se[i]:+.3f}; {b[i]+tc*se[i]:+.3f}]" for i in range(len(cols))) + " |")
                    EVMD.append(f"\nAntecipações conjuntas (tau=-3,-2): " + (f"F={Fl:.2f}, p={pl:.3f}" if pl is not None else "n/d") + f"; algum IC de antecipação exclui 0: {lead_ic}. Pós conjunto (0..3): " + (f"F={Fp:.2f}, p={pp:.3f}" if pp is not None else "n/d") + f". Média dos pós: {m:+.4f} [{mlo:+.4f}; {mhi:+.4f}] = [{100*(math.exp(mlo)-1):+.1f}%; {100*(math.exp(mhi)-1):+.1f}%].")

# ================= (2b) PÓS-HOC (NÃO pré-registrado; fora dos critérios): quem são tratados/controles e se um coorte puxa o resultado =================
PH = ["", "## 2b. PÓS-HOC (não pré-registrado, não entra em veredito): composição e coortes do desenho estrito, painel BRC, desfecho tx_total", ""]
pil_all = {}
for direcao, rot in ((1, "esquerda->direita"), (-1, "direita->esquerda")):
    pil = monta_pilhas(by, ev1, direcao, "estrito"); pil_all[direcao] = pil
    for e_ in sorted({e for _, e, *_ in pil}):
        sub = [x for x in pil if x[1] == e_]
        PH.append(f"- {rot}, evento em {e_}: tratados {sorted(u for u, *_ in sub)}; controles limpos {sorted(set(c for *_, ctrl in sub for c in ctrl))}")
PH += ["", "| recorte | n eventos | média dos pós (tx_total) [IC95% t] | % exato | p antecipações |", "|---|---|---|---|---|"]
def linha(rot, pil):
    cols, b_, V_, G_, n_, nc_ = estima_event(by, pil, "tx_total"); m, lo, hi = media_pos(cols, b_, V_, G_); Fl, pl = waldF(cols, b_, V_, G_, (-3, -2))
    return f"| {rot} | {len(pil)} | {m:+.3f} [{lo:+.3f}; {hi:+.3f}] | [{100*(math.exp(lo)-1):+.1f}%; {100*(math.exp(hi)-1):+.1f}%] | " + (f"{pl:.3f}" if pl is not None else "n/d") + " |"
for direcao, rot in ((1, "esq->dir"), (-1, "dir->esq")):
    for e_ in (2015, 2019):
        sub = [x for x in pil_all[direcao] if x[1] == e_]
        if len(sub) >= 2: PH.append(linha(f"{rot}, só evento {e_}", sub))
PH.append(linha("ambas as direções juntas (qualquer troca de governo, ignorando o sentido)", pil_all[1] + pil_all[-1]))
PH += ["", "Leitura pós-hoc: se a ideologia importasse, as duas direções teriam sinais opostos; o mesmo sinal nas duas aponta para efeito de qualquer troca de governo, de seleção dos controles (UFs sem troca em 7 anos) ou de tendência pré-existente, e não para ideologia. Pós-hoc: serve para NÃO ler o event study como corroboração nem como refutação.", ""]
EVMD += PH

# ================= (3) pesos =================
PES = []
r_ = rows; uf_ = np.array([x["uf"] for x in r_]); an_ = np.array([int(x["ano"]) for x in r_]); Dv = np.array([float(x["ideologia"]) for x in r_])
eps = demean2(Dv, uf_, an_)
Di = np.array([Dv[uf_ == u].mean() for u in uf_]); Dbar = Dv.mean()
def massa_neg(w): return float(np.abs(w[w < 0]).sum() / np.abs(w).sum())
masses = (float((eps < 0).mean()), massa_neg(eps), massa_neg(eps * (Dv - Di)), massa_neg(eps * (Dv - Dbar)))
tc26 = stats.t.ppf(0.975, 26)
for o in OUT:
    y = np.log(np.array([float(x[o]) for x in r_])); yt = demean2(y, uf_, an_)
    bT = float(eps @ yt / (eps @ eps)); res = {}
    for nome, z in (("b+", np.where(eps > 0, eps, 0.0)), ("b-", np.where(eps < 0, eps, 0.0))):
        bz = float(z @ yt / (z @ eps)); u = z * (yt - bz * eps)
        S = sum(float(u[uf_ == g].sum()) ** 2 for g in np.unique(uf_)); G = len(np.unique(uf_))
        se = math.sqrt(S * G / (G - 1)) / abs(float(z @ eps)); res[nome] = (bz, se)
    PES.append((o, bT, B[o][1], res))

# ================= (1) conversão =================
K = 5
CONV = []
for o in OUT:
    b, se = B[o]; lo, hi = b - 1.96 * se, b + 1.96 * se
    CONV.append((o, b, se, lo, hi, 100 * K * lo, 100 * K * hi, 100 * (math.exp(K * lo) - 1), 100 * (math.exp(K * hi) - 1)))
CONVZ = []
for o in OUT:
    b, se = BZ[o]; lo, hi = b - 1.96 * se, b + 1.96 * se
    for dest, k in kz.items(): CONVZ.append((o, dest, k, 100 * k * lo, 100 * k * hi, 100 * (math.exp(k * lo) - 1), 100 * (math.exp(k * hi) - 1)))

L = ["# C03 — painel F8: conversão exata, event study empilhado e pesos do TWFE (gerado por painel_c03_event_pesos.py)", "",
     "> [!NOTE]", "> Exploratório, NÃO causal; poucos eventos limpos; 27 clusters. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. Cabeçalho do script traz método e LIMITES.", "",
     "## 0. Reprodução e contagens", "",
     f"- b e EP dos 6 desfechos (BRC) e da robustez BLS9 (341 UF-anos) = `resultados_tse_brc.md` (4 casas).",
     f"- Painel BRC: {mud1} mudanças de escore = {len(ev1)} trocas reais (partido muda) + {onda1} trocas de onda no mesmo partido (todas em {sorted({e for u,d in by.items() for e in d if e>2012 and by[u][e]['partido']==by[u][e-1]['partido'] and abs(float(by[u][e]['ideologia'])-float(by[u][e-1]['ideologia']))>1e-9})}); trocas reais: {dirs1[1]} para a direita, {dirs1[-1]} para a esquerda.",
     f"- Painel `tse` (escore único): {mud2} mudanças = {up2} para a direita + {dn2} para a esquerda, 0 trocas de onda. **O \"68 trocas\" do dossiê pertence a este painel; o \"27 de 94\", ao BRC; as duas contagens não são da mesma especificação** (no BRC são 67 trocas reais).", "",
     "## 1. Conversão exata 100[exp(5b)-1] dos limites do IC95% (k = 5 pontos; PT 2,97 -> DEM/PL ~8)", "",
     "| desfecho | b | EP | IC95% de b | linear 100x5x limite (%) | exato 100[exp(5 limite)-1] (%) | diferença nos limites (p.p.) |", "|---|---|---|---|---|---|---|"]
for o, b, se, lo, hi, l1, l2, e1, e2 in CONV:
    L.append(f"| {o} | {b:+.4f} | {se:.4f} | [{lo:+.4f}; {hi:+.4f}] | [{l1:+.1f}; {l2:+.1f}] | [{e1:+.1f}; {e2:+.1f}] | [{e1-l1:+.1f}; {e2-l2:+.1f}] |")
L += ["", f"BLS9 2021 (Zucco & Power): PT {dPT:+.2f}, DEM {dDEM:+.2f}, PL {dPL:+.2f}; k = {kz['DEM']:.2f} (PT->DEM) e {kz['PL']:.2f} (PT->PL).", "",
      "| desfecho (BLS9) | destino | k | linear (%) | exato (%) |", "|---|---|---|---|---|"]
for o, dest, k, l1, l2, e1, e2 in CONVZ: L.append(f"| {o} | {dest} | {k:.2f} | [{l1:+.1f}; {l2:+.1f}] | [{e1:+.1f}; {e2:+.1f}] |")
L += ["", "## 2. Event study empilhado (stacked DD), ln(taxa), referência tau=-1, IC95% com t(G-1), EP agrupado por UF"] + EVMD
L += ["", "## 3. Pesos do TWFE contínuo (painel BRC, 351 UF-anos balanceados)", "",
      f"- Observações com eps < 0: {100*masses[0]:.1f}% (mecânico: ~50% num painel balanceado; não é defeito por si).",
      f"- Massa de peso negativo: sob eps {100*masses[1]:.1f}%; sob eps x (D - D_UF) {100*masses[2]:.1f}%; sob eps x (D - D_médio) {100*masses[3]:.1f}% (depende da origem de D: variantes, não verdades).", "",
      "| desfecho | b TWFE | b+ (eps>0) [IC95% t(26)] | b- (eps<0) [IC95% t(26)] | razão b_TWFE/b+ |", "|---|---|---|---|---|"]
for o, bT, seT, res in PES:
    (bp, sp), (bm, sm) = res["b+"], res["b-"]
    raz = f"{bT/bp:.2f}" if abs(bT) > 2 * seT else "não reportada (|b TWFE| <= 2 EP)"
    L.append(f"| {o} | {bT:+.4f} | {bp:+.4f} [{bp-tc26*sp:+.4f}; {bp+tc26*sp:+.4f}] | {bm:+.4f} [{bm-tc26*sm:+.4f}; {bm+tc26*sm:+.4f}] | {raz} |")
open(f"{D}/painel/c03_event_pesos_resultados.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
with open(f"{D}/painel/c03_event_pesos_resultados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["painel", "desenho", "direcao", "desfecho", "n_eventos", "n_ufs_controle", "G", "n_obs"] + [f"beta_tau{t}|lo|hi" for t in TAUS] + ["p_antecipacoes", "p_pos", "media_pos", "media_pos_lo", "media_pos_hi", "antecipacao_ic_exclui_zero"])
    for r in EVROWS: w.writerow(r)
print("\n".join(L))
