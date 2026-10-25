"""Analises de concordancia entre series publicas de mortes LGBT+ no Brasil. Entrada: ../painel_mortes_lgbt.csv (+ F3-ggb para a captura-recaptura 2019).
Semente fixa 20261022. Bootstrap por pares de ANOS (B=20000, percentil 95%). Saidas: ../dados_analises/*.csv e ../dados_analises/resultados.json.
LIMITE GERAL: series curtas (n de 2 a 24 variacoes), autocorrelacionadas, nao amostrais; IC mede so a instabilidade entre anos, NAO erro de medida.
Uso: /opt/homebrew/bin/python3.14 -I s06_analises.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, json, math, pathlib, collections, itertools
import numpy as np
from scipy import stats

SEED = 20261022
HERE = pathlib.Path(__file__).resolve().parent
S = HERE.parent
OUT = S / "dados_analises"; OUT.mkdir(exist_ok=True)
F3 = pathlib.Path((REPO_ROOT + "/research-2026-10-21-rodada3/F3-ggb/dados"))
rng = np.random.default_rng(SEED)
B = 20000

P = list(csv.DictReader(open(S / "painel_mortes_lgbt.csv")))
def ser(fonte, cat, tipos=None):
    d = {}
    for r in P:
        if r["fonte"] == fonte and r["categoria"] == cat and r["valor"] not in ("", None) and r["ano"] == r["ano_fim"]:
            d[int(r["ano"])] = float(r["valor"])
    return d
GGB = ser("ggb2019", "total")  # 2000-2019 (tabela)
for y, f in [(2020, "ggb2020"), (2021, "ggb2021"), (2023, "ggb2023"), (2024, "ggb2024"), (2025, "ggb2025")]:
    GGB.update(ser(f, "total"))
GGB[2022] = 256.0  # derivado (ver painel)
GGB_orig = {}  # valor do relatorio original quando difere da tabela 2019
for f in ["ggb2011", "ggb2012", "ggb2013", "ggb2014", "ggb2015", "ggb2016"]:
    GGB_orig.update(ser(f, "total_relatorio_original"))
SUIC = {2013: 10, 2014: 9, 2015: 5, 2016: 26, 2017: 58, 2018: 100, 2019: 32, 2020: 13, 2021: 24, 2023: 20, 2024: 18, 2025: 20}  # 2016 = GGB 2018 p. (26 em 2016); demais do painel
for f in ["ggb2017", "ggb2018", "ggb2019", "ggb2020", "ggb2021", "ggb2024", "ggb2025"]:
    SUIC.update({k: v for k, v in ser(f, "suicidios").items()})
SUIC.update(ser("ggb2013", "suicidios")); SUIC.update(ser("ggb2016", "suicidios")); SUIC.update(ser("ggb2014", "suicidios")); SUIC.update(ser("ggb2015", "suicidios"))
GT = {}  # GGB trans/travestis (como publicado)
for f in ["ggb2011", "ggb2012", "ggb2013", "ggb2014", "ggb2015", "ggb2016", "ggb2017", "ggb2018", "ggb2019", "ggb2020", "ggb2021", "ggb2023", "ggb2024", "ggb2025"]:
    GT.update(ser(f, "trans_travestis"))
GHT = {}
for f in ["ggb2020", "ggb2024", "ggb2025"]:
    GHT.update(ser(f, "homens_trans"))
GT_plus = {y: v + GHT.get(y, 0) for y, v in GT.items()}
ANT = {}
for f in [f"antra{y}" for y in range(2017, 2026)]:
    ANT.update(ser(f, "trans_assassinatos"))
ANT.pop(2016, None)
TMM_C = ser("TGEU_TMM", "tmm_casos_brasil_ano_civil"); TMM_P = ser("TGEU_TMM", "tmm_casos_brasil_periodo_TDoR_out_set")
TDOR = ser("TDoR_lista", "tdor_casos_brasil_ano_civil"); TDOR_V = ser("TDoR_lista", "tdor_casos_brasil_violencia")
OBS = {}; OBS_T = {}
for f in ["obs2021", "obs2022", "obs2023"]:
    OBS.update(ser(f, "total")); OBS_T.update(ser(f, "trans_travestis"))
ANU = {2020: 167, 2021: 179, 2022: 151, 2023: 274, 2024: 218, 2025: 187}  # ultima revisao publicada de cada ano
SIM = ser("SIM_DATASUS", "obitos_agressao_sim_brasil")

def dlog(d):
    ys = sorted(d); return {y: math.log(d[y] / d[y - 1]) for y in ys if y - 1 in d and d[y] > 0 and d[y - 1] > 0}
def boot_corr(x, y, kind):
    n = len(x); x = np.array(x); y = np.array(y)
    f = (lambda a, b: stats.pearsonr(a, b)[0]) if kind == "pearson" else (lambda a, b: stats.spearmanr(a, b)[0])
    r0 = f(x, y); bs = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        if len(set(x[i])) < 2 or len(set(y[i])) < 2: continue
        bs.append(f(x[i], y[i]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    # permutacao
    pm = [abs(f(x, rng.permutation(y))) for _ in range(5000)]
    p = (1 + sum(v >= abs(r0) - 1e-12 for v in pm)) / (len(pm) + 1)
    return float(r0), float(lo), float(hi), float(p)
res = {}

# ---------------- (a) correlacao de variacoes anuais ----------------
IND = "janela independente: 2020-2025 (TDoR/TMM deixa de citar GGB/Homofobia Mata em 2019; ver dados_tdor_dependencia.csv)"
DEP = "janela DEPENDENTE: ate 2018 o TDoR/TMM Brasil cita GGB/Homofobia Mata em 73-94% dos registros (2012-2018)"
pairs = [
 ("GGB total x SIM agressao", GGB, SIM, "contexto: o SIM nao tem orientacao/identidade", None),
 ("GGB total x ANTRA trans", GGB, ANT, "ANTRA independente do GGB so a partir de 2017 (ANTRA 2017: serie 2008-2016 = GGB)", (2018, 2025)),
 ("GGB trans x ANTRA trans", GT, ANT, "so anos consecutivos com ambos (GGB sem composicao em 2022)", None),
 ("GGB trans+homens trans x ANTRA", GT_plus, ANT, "sensibilidade: soma homens trans onde o GGB publica", None),
 ("GGB trans x TMM (ciclo TDoR), 2020+", GT, TMM_P, IND, (2020, 2025)),
 ("GGB total x TMM (ciclo TDoR), 2020+", GGB, TMM_P, IND, (2020, 2025)),
 ("GGB total x TDoR (ano civil), 2020+", GGB, TDOR, IND, (2020, 2025)),
 ("GGB total x TDoR (ano civil), 2010-2018", GGB, TDOR, DEP, (2010, 2018)),
 ("ANTRA x TMM (ciclo TDoR), 2018+", ANT, TMM_P, "inclui 2018 (TDoR 78% GGB/HM)", (2018, 2025)),
 ("ANTRA x TMM (ciclo TDoR), 2020+", ANT, TMM_P, IND, (2020, 2025)),
 ("ANTRA x TDoR (ano civil), 2020+", ANT, TDOR, IND, (2020, 2025)),
 ("GGB total x Anuario FBSP homicidio LGBT", GGB, ANU, "2021-2025; cobertura por UF muda", None),
]
cor_rows = []
for nome, a, b, nota, rng_anos in pairs:
    da, db = dlog(a), dlog(b)
    ys = sorted(set(da) & set(db))
    if rng_anos: ys = [y for y in ys if rng_anos[0] <= y <= rng_anos[1]]
    if len(ys) < 3:
        cor_rows.append(dict(par=nome, n=len(ys), pearson="", p_lo="", p_hi="", p_perm="", spearman="", s_lo="", s_hi="", sinal_igual="", nota=nota)); continue
    x = [da[y] for y in ys]; y_ = [db[y] for y in ys]
    pr = boot_corr(x, y_, "pearson"); sp = boot_corr(x, y_, "spearman")
    conc = sum(1 for u, v in zip(x, y_) if (u > 0) == (v > 0)); lo, hi = stats.binomtest(conc, len(ys)).proportion_ci(0.95, "exact")
    cor_rows.append(dict(par=nome, n=len(ys), anos=f"{ys[0]}-{ys[-1]}", pearson=round(pr[0], 2), p_lo=round(pr[1], 2), p_hi=round(pr[2], 2), p_perm=round(pr[3], 3), spearman=round(sp[0], 2), s_lo=round(sp[1], 2), s_hi=round(sp[2], 2),
                         sinal_igual=f"{conc}/{len(ys)} ({conc/len(ys):.0%}; IC95 exato {lo:.0%}-{hi:.0%})", nota=nota))
with open(OUT / "cor_variacoes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["par", "n", "anos", "pearson", "p_lo", "p_hi", "p_perm", "spearman", "s_lo", "s_hi", "sinal_igual", "nota"]); w.writeheader(); w.writerows(cor_rows)
res["cor_variacoes"] = cor_rows

# ---------------- (b) razoes por ano ----------------
def ratio(a, b, ys=None):
    ys = sorted(set(a) & set(b)) if ys is None else ys
    return {y: a[y] / b[y] for y in ys if b.get(y)}
raz = {
 "GGB trans / ANTRA": ratio(GT, ANT), "GGB trans+homens trans / ANTRA": ratio(GT_plus, ANT), "ANTRA / TDoR(ano civil)": ratio(ANT, TDOR), "ANTRA / TMM(ciclo TDoR)": ratio(ANT, TMM_P), "GGB trans / TMM(ciclo)": ratio(GT, TMM_P),
 "Obs trans(travestis+mulheres) / ANTRA": ratio(OBS_T, ANT), "Obs total / GGB total": ratio(OBS, GGB), "Anuario FBSP / GGB total": ratio(ANU, GGB), "GGB total por mil mortes por agressao (SIM)": {y: 1000 * GGB[y] / SIM[y] for y in sorted(set(GGB) & set(SIM))},
}
raz_rows = []
for nome, d in raz.items():
    ys = sorted(d)
    if len(ys) < 3: m = lo = hi = None
    else:
        v = np.array([d[y] for y in ys]); bs = [np.mean(v[rng.integers(0, len(v), len(v))]) for _ in range(B)]; m = float(v.mean()); lo, hi = np.percentile(bs, [2.5, 97.5])
        rho, pv = stats.spearmanr(ys, v)
    raz_rows.append(dict(razao=nome, n_anos=len(ys), anos=f"{ys[0]}-{ys[-1]}" if ys else "", media=round(m, 3) if m is not None else "", ic_lo=round(float(lo), 3) if lo is not None else "", ic_hi=round(float(hi), 3) if hi is not None else "",
                         rho_vs_ano=round(float(rho), 2) if len(ys) >= 3 else "", p_rho=round(float(pv), 3) if len(ys) >= 3 else "", valores="; ".join(f"{y}:{d[y]:.2f}" for y in ys)))
with open(OUT / "razoes_por_ano.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(raz_rows[0])); w.writeheader(); w.writerows(raz_rows)
res["razoes"] = raz_rows

# ---------------- (c) captura-recaptura ----------------
cr = json.loads((F3 / "captura_recaptura_trans2019.json").read_text()); crs = json.loads((F3 / "captura_recaptura_sensibilidade.json").read_text())
c19 = dict(chapman=cr["chapman"], ic95_normal=cr["ic95_normal"], uniao_observada=cr["n_uniao_observada"], ggb_trans=118, tdor=139, sobreposicao=cr["sobreposicao"], antra_agregado=ANT[2019], tmm_ciclo2019=TMM_P[2019], tdor_violencia=TDOR_V[2019],
           cenarios=[(s["cenario"], s["chapman"]) for s in crs])
c19["cobertura_antra_sobre_chapman"] = round(ANT[2019] / cr["chapman"], 3)
c19["cobertura_antra_sobre_uniao"] = round(ANT[2019] / cr["n_uniao_observada"], 3)
c19["cobertura_ggb_sobre_chapman"] = round(118 / cr["chapman"], 3)
# IC aproximado da cobertura do GGB: 118/N com N~[174.5,197.9]
c19["cobertura_ggb_ic"] = [round(118 / 197.9, 3), round(118 / 174.5, 3)]
res["captura_recaptura_2019"] = c19
disp = []
for y in range(2017, 2026):
    disp.append(dict(ano=y, GGB_lista_nominal_publica="sim (Anexo 3, 329 casos)" if y == 2019 else "nao", ANTRA_lista_nominal_publica="nao (Mapa: 'acesso restrito... a quem solicitar', ANTRA 2020 nota 18)", TDoR_lista_nominal_publica="sim",
                     TMM="IDs anonimizados (mesma base do TDoR)", Observatorio_lista="nao", par_independente_estimavel="sim, so 2019 (GGBxTDoR)" if y == 2019 else "NAO"))
with open(OUT / "captura_recaptura_disponibilidade.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(disp[0])); w.writeheader(); w.writerows(disp)

# dependencia TMM <- GGB
dep = list(csv.DictReader(open(S / "dados_tmm_dependencia.csv")))
res["tmm_dependencia"] = {r["ano_civil"]: dict(n=int(r["n_tmm_brasil"]), pct_GGB=float(r["pct_GGB"])) for r in dep}

# colisao exata da decomposicao por causa GGB 2023 vs 2025 (204/20/17/16, n=257)
n = 257; cnt = np.array([204, 20, 17, 16]); p = cnt / n
def pmf(a, b, c, d): return stats.multinomial.pmf([a, b, c, d], n, p)
tot = 0.0
for a in range(0, n + 1):
    for b_ in range(0, n - a + 1):
        for c_ in range(0, n - a - b_ + 1):
            d_ = n - a - b_ - c_; pr = pmf(a, b_, c_, d_)
            tot += pr * pr
res["colisao_2023_2025"] = dict(prob_identidade_exata=float(tot), nota="P(duas sorteios independentes da mesma multinomial coincidirem em TODAS as 4 caixas), p = proporcoes observadas; descritivo, nao prova copia")

# ---------------- (d) SIM ----------------
sim_rows = []
ys = sorted(set(GGB) & set(SIM))
for y in ys:
    sim_rows.append(dict(ano=y, ggb=GGB[y], sim_agressao=SIM[y], ggb_por_mil_sim=round(1000 * GGB[y] / SIM[y], 2)))
with open(OUT / "ggb_vs_sim.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(sim_rows[0])); w.writeheader(); w.writerows(sim_rows)
dg, ds = dlog(GGB), dlog(SIM); yy = sorted(set(dg) & set(ds))
def sub(a, b): return [y for y in yy if a <= y <= b]
dres = {}
for nome, (a, b) in {"todo": (min(yy), max(yy)), "ate_2017": (min(yy), 2017), "2018_em_diante": (2018, max(yy)), "2018_2024_sem_2020": (2018, 2024)}.items():
    ys_ = sub(a, b)
    if nome == "2018_2024_sem_2020": ys_ = [y for y in ys_ if y != 2020]
    if len(ys_) < 4: continue
    x = [dg[y] for y in ys_]; z = [ds[y] for y in ys_]
    pr = boot_corr(x, z, "pearson"); sp = boot_corr(x, z, "spearman"); conc = sum(1 for u, v in zip(x, z) if (u > 0) == (v > 0)); lo, hi = stats.binomtest(conc, len(ys_)).proportion_ci(0.95, "exact")
    # inclinacao da regressao dlog GGB ~ dlog SIM com bootstrap
    xa, za = np.array(z), np.array(x); sl = np.polyfit(xa, za, 1)[0]; bs = []
    for _ in range(B):
        i = rng.integers(0, len(xa), len(xa))
        if len(set(xa[i])) > 1: bs.append(np.polyfit(xa[i], za[i], 1)[0])
    dres[nome] = dict(anos=f"{ys_[0]}-{ys_[-1]}", n=len(ys_), pearson=[round(pr[0], 2), round(pr[1], 2), round(pr[2], 2)], p_perm=round(pr[3], 3), spearman=[round(sp[0], 2), round(sp[1], 2), round(sp[2], 2)],
                      sinal_igual=f"{conc}/{len(ys_)}", sinal_igual_ic=[round(lo, 2), round(hi, 2)], inclinacao=round(float(sl), 2), inclinacao_ic=[round(float(v), 2) for v in np.percentile(bs, [2.5, 97.5])])
res["ggb_vs_sim_variacoes"] = dres
# niveis: razao ao longo do tempo
r_ = np.array([sim_rows[i]["ggb_por_mil_sim"] for i in range(len(sim_rows))]); yrs = np.array([r["ano"] for r in sim_rows])
res["ggb_por_mil_sim"] = {int(y): float(v) for y, v in zip(yrs, r_)}
rho, pv = stats.spearmanr(yrs, r_); res["ggb_por_mil_sim_tendencia"] = dict(rho_vs_ano=round(float(rho), 2), p=round(float(pv), 4))
# variacao acumulada 2017->2024
def pct(d, a, b): return round(100 * (d[b] / d[a] - 1), 1)
res["acumulado_2017_2024"] = dict(GGB=pct(GGB, 2017, 2024), SIM=pct(SIM, 2017, 2024), ANTRA=pct(ANT, 2017, 2024), TDoR=pct(TDOR, 2017, 2024), TMM_ciclo=pct(TMM_P, 2017, 2024))
res["acumulado_2000_2017"] = dict(GGB=pct(GGB, 2000, 2017), SIM=pct(SIM, 2000, 2017)) if 2000 in SIM else {}
res["acumulado_2010_2017"] = dict(GGB=pct(GGB, 2010, 2017), SIM=pct(SIM, 2010, 2017))
# correlacao parcial: dlog ANTRA e dlog GGB, controlando dlog SIM
def partial(a, b, c):
    ys_ = sorted(set(a) & set(b) & set(c)); x = np.array([a[y] for y in ys_]); y = np.array([b[y] for y in ys_]); z = np.array([c[y] for y in ys_])
    rx = x - np.polyval(np.polyfit(z, x, 1), z); ry = y - np.polyval(np.polyfit(z, y, 1), z)
    r0 = stats.pearsonr(rx, ry)[0]; bs = []
    for _ in range(B):
        i = rng.integers(0, len(z), len(z))
        if len(set(z[i])) < 2: continue
        xi, yi, zi = x[i], y[i], z[i]; rxi = xi - np.polyval(np.polyfit(zi, xi, 1), zi); ryi = yi - np.polyval(np.polyfit(zi, yi, 1), zi)
        if rxi.std() > 0 and ryi.std() > 0: bs.append(stats.pearsonr(rxi, ryi)[0])
    return dict(n=len(ys_), r=round(float(r0), 2), ic=[round(float(v), 2) for v in np.percentile(bs, [2.5, 97.5])])
res["parcial_GGBtotal_ANTRA_dado_SIM"] = partial(dlog(GGB), dlog(ANT), dlog(SIM))
res["bruta_GGBtotal_ANTRA"] = next(r for r in cor_rows if r["par"] == "GGB total x ANTRA trans")

# ---------------- (e) quebras e sensibilidade ----------------
sens = []
F3S = list(csv.DictReader(open(F3 / "sensibilidade_manchete.csv")))
for r in F3S:
    sens.append(r)
A = {int(r["ano"]): float(r["A_manchete"]) for r in F3S if r["A_manchete"]}
Bv = {int(r["ano"]): float(r["B_sem_suicidio"]) for r in F3S if r["B_sem_suicidio"]}
C = {int(r["ano"]): float(r["C_homicidio_estrito"]) for r in F3S if r["C_homicidio_estrito"]}
def chg(d, a, b):
    if a in d and b in d:
        x1, x2 = d[a], d[b]; k = int(x2); n_ = int(x1 + x2); lo, hi = stats.binomtest(k, n_).proportion_ci(0.95, "exact")
        return dict(de=a, para=b, v1=int(x1), v2=int(x2), pct=round(100 * (x2 / x1 - 1), 1), ic_poisson=[round(100 * (lo / (1 - lo) - 1), 1), round(100 * (hi / (1 - hi) - 1), 1)])
    return None
sens_chg = []
for (a, b) in [(2017, 2025), (2017, 2018), (2018, 2019), (2019, 2020), (2019, 2023), (2023, 2025), (2023, 2024)]:
    sens_chg.append(dict(janela=f"{a}->{b}", A_todas=chg(A, a, b), B_sem_suicidio=chg(Bv, a, b), C_homicidio_estrito=chg(C, a, b)))
res["sensibilidade_variacao"] = sens_chg
# soma de suicidios e contribuicao
res["suicidios_pct_do_total"] = {y: round(100 * SUIC[y] / GGB[y], 1) for y in sorted(SUIC) if y in GGB}
# quebras: z robusto das variacoes anuais do GGB total e ANTRA
def robz(d):
    dl = dlog(d); ys = sorted(dl); v = np.array([dl[y] for y in ys]); med = np.median(v); mad = np.median(abs(v - med)) * 1.4826
    return {y: round(float((dl[y] - med) / mad), 2) for y in ys}
res["robz_GGB_total"] = robz({y: v for y, v in GGB.items() if y >= 2000}); res["robz_ANTRA"] = robz(ANT)
BR = {2018: "suicidios 58->100 (GGB 2018)", 2019: "relatorio com lista nominal; 158 casos descartados/58 retirados", 2020: "coprodutor Acontece; coleta por Google Alerts; pandemia", 2021: "novos termos de busca, delegacias, servicos funerarios, redes sociais",
      2022: "sem relatorio anual", 2024: "'aprimoramento nas tecnicas de coleta e depuracao' sem reconciliacao; 32 casos 'no limbo'", 2025: "destaque '237 homicidios' (=204+17+16); regiao NI 33%, idade NI 60%"}
res["quebras_declaradas_GGB"] = BR
# discrepancia GGB: tabela por decada (2021) vs soma da serie anual
dec = {"2000-2009": (1429, sum(GGB[y] for y in range(2000, 2010))), "2010-2019": (3029, sum(GGB[y] for y in range(2010, 2020)))}
res["ggb2021_decadas_vs_serie_anual"] = {k: dict(tabela_ggb2021=v[0], soma_anual_ggb2019=int(v[1]), diferenca=int(v[1] - v[0])) for k, v in dec.items()}
# revisao ex post
rev = {y: dict(original=GGB_orig[y], tabela2019=GGB[y], dif=GGB[y] - GGB_orig[y]) for y in sorted(GGB_orig) if y in GGB}
res["revisao_ggb_original_vs_tabela2019"] = rev
# consistencia interna composicao x total (GGB)
cons = {2017: (194 + 191 + 43 + 5 + 12, 445), 2018: (191 + 164 + 52 + 8 + 5, 420), 2019: (174 + 118 + 32 + 5, 329), 2020: (161 + 51 + 10 + 3 + 3 + 2, 237), 2021: (153 + 110 + 12 + 4 + 1 + 1, 300), 2023: (127 + 118 + 9 + 3, 257), 2024: (165 + 96 + 11 + 7 + 6 + 6, 291), 2025: (156 + 46 + 18 + 9 + 4 + 3 + 3 + 16, 257)}
res["consistencia_composicao"] = {y: dict(soma_categorias=a, total_declarado=b, falta=b - a) for y, (a, b) in cons.items()}
# divergencia GGB trans x ANTRA etc. (descritivo)
tab = []
for y in range(2017, 2026):
    tab.append(dict(ano=y, GGB_total=GGB.get(y), GGB_trans=GT.get(y), ANTRA=ANT.get(y), TMM_ciclo=TMM_P.get(y), TDoR_ano=TDOR.get(y), Obs_total=OBS.get(y), Obs_trans=OBS_T.get(y), Anuario=ANU.get(y), SIM=SIM.get(y)))
with open(OUT / "painel_wide_2017_2025.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(tab[0])); w.writeheader(); w.writerows(tab)
(OUT / "resultados.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
print(json.dumps({k: res[k] for k in ["ggb_vs_sim_variacoes", "acumulado_2017_2024", "acumulado_2000_2017", "acumulado_2010_2017", "parcial_GGBtotal_ANTRA_dado_SIM", "colisao_2023_2025", "ggb2021_decadas_vs_serie_anual", "consistencia_composicao", "revisao_ggb_original_vs_tabela2019"] if k in res}, ensure_ascii=False, indent=1, default=float))
for r in cor_rows: print(r)
for r in raz_rows: print({k: r[k] for k in r if k != "valores"})
