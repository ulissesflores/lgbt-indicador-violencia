"""C09 — D2: alinhamento federal-estadual no painel UF x ano (primária + S1-S7 do PREREGISTRO-C09.md, seções 3 e 4).
Pré-registro: PREREGISTRO-C09.md (sha256 em PREREGISTRO-C09.sha256, gravado ANTES deste script existir).
Modelo primário: ln(tx_total) = b1 g + b2 (g x p) + EF(UF) + EF(ano); painel dados/painel/painel_uf_ano_tse_brc.csv (351 UF-anos); g = coluna `ideologia`; p = escore BRC do
presidente do ano (partido de eleição, ponderado por dias; c09_estrutura.pres_score). EP CR1 por UF e bootstrap wild-cluster-t (Rademacher, B = 4999, H0 imposta com g no modelo
restrito) com as funções de dados/painel/painel_diagnosticos.py IMPORTADAS sem alteração. Numeradores agressão+indet e denominadores: cópia literal da lógica de painel_c02_indet.py.
Portas de reprodução (abortam): b e EP dos 6 desfechos de resultados_tse_brc.md; p wild 0,943 de tx_total (semente 20261021, primeiro sorteio); SIM agressão = Atlas;
ideologia do painel = BRC por período arredondado; BLS9 tx_total = resultados_tse_brc.md (341 UF-anos).
Rodar: /opt/homebrew/bin/python3.14 -I c09_d2_painel.py   Saídas: c09_d2_resultados.md, c09_d2_resultados.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import sys; sys.dont_write_bytecode = True   # não deixar __pycache__ nas pastas de dados/ ao importar módulos irmãos
import csv, importlib.util, json, math, re, collections
from datetime import date
import numpy as np
from scipy import stats

BASE = REPO_ROOT
D = f"{BASE}/dados"; AQUI = f"{BASE}/dados/presidencia"
SCR = f"{BASE}/fontes/p2-f8-dados-uf/sidra"
ZP = f"{BASE}/fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab"


def _imp(nome, arq):
    s = importlib.util.spec_from_file_location(nome, arq); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


pdg = _imp("pdiag", f"{D}/painel/painel_diagnosticos.py")      # RNG nasce em 20261021
est = _imp("c09est", f"{AQUI}/c09_estrutura.py")

COL = {"total": "tx_total", "homens": "tx_homens", "mulheres": "tx_mulheres", "negros": "tx_negros", "nao_negros": "tx_nao_negros", "arma": "tx_arma"}
G5 = ["total", "homens", "mulheres", "negros", "nao_negros"]


def modelo(rows, y, x, controles=()):
    """b, EP (CR1), p wild do coeficiente de x; EF de UF e ano + colunas de controle no modelo restrito."""
    y = np.array(y, float); x = np.array(x, float); cl = np.array([r["uf"] for r in rows])
    F = pdg.dummies(rows)
    if controles: F = np.column_stack([F] + [np.array(c, float) for c in controles])
    M = pdg.residuador(F); kfe = np.linalg.matrix_rank(F)
    b, se, _, _, _ = pdg.ols_fwl(y, x, M, cl, kfe)
    p = pdg.wild_p(y, x, M, cl, kfe)[0]
    return float(b[0]), float(se[0]), float(p), len(y)


def holm(ps):
    o = sorted(range(len(ps)), key=lambda i: ps[i]); adj = [0.0] * len(ps); run = 0.0
    for rank, i in enumerate(o):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj


# ================= porta 1: b, EP e p wild publicados do painel de governadores =================
rows = list(csv.DictReader(open(f"{D}/painel/painel_uf_ano_tse_brc.csv", encoding="utf-8")))
assert len(rows) == 351 and len({r["uf"] for r in rows}) == 27 and all(float(r[c]) > 0 for r in rows for c in COL.values())
pub = {}
for l in open(f"{D}/painel/resultados_tse_brc.md", encoding="utf-8"):
    m = re.match(r"\| (tx_\w+) \| ([+-]\d\.\d{4}) \| (\d\.\d{4}) \| \[", l)
    if m and m.group(1) not in pub: pub[m.group(1)] = (float(m.group(2)), float(m.group(3)))
assert len(pub) == 6
pwild_pub = float(re.search(r"\| tx_total \| [+-]\d\.\d{4} \(\d\.\d{4}\) \| (\d\.\d{3}) \|", open(f"{D}/painel/diagnosticos.md", encoding="utf-8").read()).group(1))
g_ = [float(r["ideologia"]) for r in rows]
b0, se0, p0, _ = modelo(rows, [math.log(float(r["tx_total"])) for r in rows], g_)        # primeiro sorteio da semente 20261021
assert abs(b0 - pub["tx_total"][0]) < 5.1e-5 and abs(se0 - pub["tx_total"][1]) < 5.1e-5 and abs(p0 - pwild_pub) < 5e-4, (b0, se0, p0)
cl_ = np.array([r["uf"] for r in rows]); F_ = pdg.dummies(rows); M_ = pdg.residuador(F_); k_ = np.linalg.matrix_rank(F_)
for c in COL.values():
    b, se, _, _, _ = pdg.ols_fwl(np.log([float(r[c]) for r in rows]), np.array(g_), M_, cl_, k_)
    assert abs(b[0] - pub[c][0]) < 5.1e-5 and abs(se[0] - pub[c][1]) < 5.1e-5, c
REPRO = f"b/EP dos 6 desfechos = resultados_tse_brc.md; tx_total b {b0:+.4f} EP {se0:.4f} p wild {p0:.3f} (publicado {pwild_pub:.3f}, semente 20261021)"

# ================= exposições =================
ideo = {(r["uf"], int(r["ano"])): r for r in csv.DictReader(open(f"{D}/ideologia/ideologia_painel_tse_por_uf_ano.csv", encoding="utf-8"))}
for r in rows:
    assert abs(float(r["ideologia"]) - round(float(ideo[(r["uf"], int(r["ano"]))]["ideo_BRC_periodo"]), 2)) < 1e-9, r
P = {a: est.pres_score(a, "brc") for a in range(2012, 2025)}
PU = {a: est.pres_score(a, "unico") for a in range(2012, 2025)}
PB = {a: est.pres_score(a, "bls9") for a in range(2012, 2025)}
p_ = [P[int(r["ano"])] for r in rows]
gp = [g * p for g, p in zip(g_, p_)]; dist = [abs(g - p) for g, p in zip(g_, p_)]
cop = [est.copart(ideo[(r["uf"], int(r["ano"]))]["partidos"], int(r["ano"])) for r in rows]
brc = est.brc_partido_ano(); K = 5 * (brc[("PSL", 2018)] - brc[("PT", 2018)])

# ================= numeradores agressão+indet (cópia literal de painel_c02_indet.py) =================
SIGLA = {'RO': 'Rondônia', 'AC': 'Acre', 'AM': 'Amazonas', 'RR': 'Roraima', 'PA': 'Pará', 'AP': 'Amapá', 'TO': 'Tocantins', 'MA': 'Maranhão', 'PI': 'Piauí', 'CE': 'Ceará', 'RN': 'Rio Grande do Norte',
         'PB': 'Paraíba', 'PE': 'Pernambuco', 'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia', 'MG': 'Minas Gerais', 'ES': 'Espírito Santo', 'RJ': 'Rio de Janeiro', 'SP': 'São Paulo', 'PR': 'Paraná',
         'SC': 'Santa Catarina', 'RS': 'Rio Grande do Sul', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso', 'GO': 'Goiás', 'DF': 'Distrito Federal'}
pop = collections.defaultdict(dict)
for x in json.load(open(f"{SCR}/sidra6407_n3_606_c2all_c58tot_pall.json"))[1:]:
    if x['V'] in ('..', '-', '...'): continue
    pop[(x['D1N'], int(x['D3N']))][x['D4N']] = float(x['V']) * 1000
acc = collections.defaultdict(lambda: collections.defaultdict(list))
for x in json.load(open(f"{SCR}/sidra6403_n3_606_c86all_pall.json"))[1:]:
    if x['V'] in ('..', '-', '...'): continue
    ano = int(x['D3N'].split()[-1]); acc[(x['D1N'], ano)][x['D4N']].append(float(x['V']) * 1000)
for k, v in acc.items():
    pop[k]['negros'] = np.mean(v['Preta']) + np.mean(v['Parda']); pop[k]['total_raca'] = np.mean(v['Total']); pop[k]['nao_negros'] = pop[k]['total_raca'] - pop[k]['negros']
for (uf, ano) in list(pop):
    if 'negros' not in pop[(uf, ano)] and (uf, ano - 1) in acc and (uf, ano + 1) in acc:
        for c in ('negros', 'nao_negros', 'total_raca'): pop[(uf, ano)][c] = (pop[(uf, ano - 1)][c] + pop[(uf, ano + 1)][c]) / 2
POPG = {"total": "Total", "homens": "Homens", "mulheres": "Mulheres", "negros": "negros", "nao_negros": "nao_negros"}
cnt = collections.Counter()
for r in csv.DictReader(open(f"{D}/sim/sim_agressoes_agregado.csv", encoding="utf-8")):
    g = r["grupo"]
    if g not in ("agressao", "indet"): continue
    uf = SIGLA.get(r["uf"]); n = int(r["n"]); a = int(r["ano"])
    if uf is None: continue
    cnt[(uf, a, g, "total")] += n
    if r["sexo"] == "F": cnt[(uf, a, g, "mulheres")] += n
    if r["raca"] in ("preta", "parda"): cnt[(uf, a, g, "negros")] += n
    if r["raca"] in ("branca", "amarela", "indigena"): cnt[(uf, a, g, "nao_negros")] += n
    if g == "agressao" and r["arma"] == "1": cnt[(uf, a, g, "arma")] += n
def n_(uf, a, g, rec):
    if rec == "homens": return cnt[(uf, a, g, "total")] - cnt[(uf, a, g, "mulheres")]
    return cnt[(uf, a, g, rec)]
ATLAS = {"total": "homicidios_total_n", "mulheres": "homicidios_mulheres_n", "negros": "homicidios_negros_n", "nao_negros": "homicidios_nao_negros_n", "arma": "homicidios_arma_fogo_n"}
atl = {(r["uf"], int(r["ano"]), r["variavel"]): float(r["valor"]) for r in csv.DictReader(open(f"{D}/atlas_uf_series.csv", encoding="utf-8")) if r["valor"] != "" and r["variavel"].endswith("_n")}
mism = sum(n_(r["uf"], int(r["ano"]), "agressao", g) != atl[(r["uf"], int(r["ano"]), ATLAS[g])] for r in rows for g in ATLAS)
maxd = max(abs(n_(r["uf"], int(r["ano"]), "agressao", g) / pop[(r["uf"], int(r["ano"]))][POPG[g]] * 1e5 - float(r[COL[g]])) for r in rows for g in G5)
assert mism == 0 and maxd < 1e-9, (mism, maxd)

# ================= estimação (semente 20261024; ordem = PREREGISTRO-C09.md seção 4) =================
pdg.RNG = np.random.default_rng(20261024)
RES = []   # (analise, grupo, desfecho, b, se, p, n, K, escala)
def roda(analise, grupo, desfecho, rows_, y, x, ctrl, Kc, escala):
    b, se, p, n = modelo(rows_, y, x, ctrl); RES.append(dict(analise=analise, grupo=grupo, desfecho=desfecho, b=b, se=se, p=p, n=n, K=Kc, escala=escala)); return RES[-1]
lny = lambda c, rr=rows: [math.log(float(r[c])) for r in rr]
roda("primaria", "total", "registrado_ln", rows, lny("tx_total"), gp, [g_], K, "log")
roda("S1_distancia", "total", "registrado_ln", rows, lny("tx_total"), dist, [g_], 5.0, "log")
for g in ["homens", "mulheres", "negros", "nao_negros", "arma"]:
    roda("S2_grupos", g, "registrado_ln", rows, lny(COL[g]), gp, [g_], K, "log")
y_ai = {g: [math.log((n_(r["uf"], int(r["ano"]), "agressao", g) + n_(r["uf"], int(r["ano"]), "indet", g)) / pop[(r["uf"], int(r["ano"]))][POPG[g]] * 1e5) for r in rows] for g in G5}
y_rz = {g: [100.0 * n_(r["uf"], int(r["ano"]), "indet", g) / (n_(r["uf"], int(r["ano"]), "agressao", g) + n_(r["uf"], int(r["ano"]), "indet", g)) for r in rows] for g in G5}
for g in G5: roda("S3_agr_indet", g, "agressao_mais_indet_ln", rows, y_ai[g], gp, [g_], K, "log")
for g in G5: roda("S3_razao_indet", g, "razao_indet_pp", rows, y_rz[g], gp, [g_], K, "pp")
rowsT = list(csv.DictReader(open(f"{D}/painel/painel_uf_ano_tse.csv", encoding="utf-8"))); assert len(rowsT) == 351
gT = [float(r["ideologia"]) for r in rowsT]
roda("S4_escore_unico", "total", "registrado_ln", rowsT, lny("tx_total", rowsT), [g * PU[int(r["ano"])] for g, r in zip(gT, rowsT)], [gT], 5 * (PU[2019] - PU[2015]), "log")
r5 = [i for i, r in enumerate(rows) if r["ano"] != "2016"]; rows5 = [rows[i] for i in r5]
roda("S5_sem_2016", "total", "registrado_ln", rows5, lny("tx_total", rows5), [gp[i] for i in r5], [[g_[i] for i in r5]], K, "log")
# S6: BLS9 (cópia da lógica de robustez do painel_f8.py / painel_c03_event_pesos.py)
zp = {}
for r in csv.DictReader(open(ZP)):
    if r["year"] == "2021": zp[r["party.or.pres"].upper()] = float(r["ideo"])
ZMAP = {'PMDB': 'MDB', 'PP': 'PP', 'PROGRESSISTAS': 'PP', 'PR': 'PL', 'PRB': 'REPUBLICANOS', 'PPS': 'CIDADANIA', 'SD': 'SOLIDARIEDADE', 'SDD': 'SOLIDARIEDADE', 'UNIÃO BRASIL': 'DEM', 'UNIÃO': 'DEM', 'PATRIOTA': 'PATRIOTA', 'PROS': 'PROS', 'PTB': 'PTB'}
def zscore(p):
    P_ = p.strip().upper()
    for c in (P_, ZMAP.get(P_, "")):
        if c in zp: return zp[c]
    return None
gov2 = collections.defaultdict(list)
for r in csv.DictReader(open(f"{D}/governadores_uf_2011_2026_tse.csv", encoding="utf-8")):
    s = zscore(r["partido"])
    if s is None: continue
    try: a = date.fromisoformat(r["inicio"]); b_ = date.fromisoformat(r["fim"]); meses = max(1, (b_ - a).days / 30.4)
    except Exception: meses = 12
    gov2[(r["uf"], int(r["ano"]))].append((s, meses))
rowsZ = []; zg = []
for r in rows:
    g = gov2.get((r["uf"], int(r["ano"])))
    if g: rowsZ.append(r); zg.append(sum(s * m for s, m in g) / sum(m for _, m in g))
assert len(rowsZ) == 341
bz, sez, _, _, _ = pdg.ols_fwl(np.log([float(r["tx_total"]) for r in rowsZ]), np.array(zg), pdg.residuador(pdg.dummies(rowsZ)), np.array([r["uf"] for r in rowsZ]), np.linalg.matrix_rank(pdg.dummies(rowsZ)))
assert abs(bz[0] - 0.0151) < 5.1e-5 and abs(sez[0] - 0.0582) < 5.1e-5, (bz, sez)   # resultados_tse_brc.md, robustez BLS9, tx_total
bl = est.bls9(); KZ = (zp["DEM"] - zp["PT"]) * (bl[("BOLSONARO", 2021)] - bl[("DILMA", 2013)])
roda("S6_BLS9", "total", "registrado_ln", rowsZ, lny("tx_total", rowsZ), [z * PB[int(r["ano"])] for z, r in zip(zg, rowsZ)], [zg], KZ, "log")
roda("S7_copartidarismo", "total", "registrado_ln", rows, lny("tx_total"), cop, [g_], 1.0, "log")

# Holm
for fam in ("S2_grupos", "S3_agr_indet"):
    sel = [x for x in RES if x["analise"] == fam]
    for x, h in zip(sel, holm([x["p"] for x in sel])): x["p_holm"] = h
sel = [x for x in RES if x["analise"] == "S3_razao_indet" and x["grupo"] != "total"]
for x, h in zip(sel, holm([x["p"] for x in sel])): x["p_holm"] = h
t26 = stats.t.ppf(0.975, 26)
for x in RES:
    x["lo"], x["hi"] = x["b"] - 1.96 * x["se"], x["b"] + 1.96 * x["se"]
    x["lo_t"], x["hi_t"] = x["b"] - t26 * x["se"], x["b"] + t26 * x["se"]
    if x["escala"] == "log":
        x["ef_lo"], x["ef_hi"] = 100 * (math.exp(x["K"] * x["lo"]) - 1), 100 * (math.exp(x["K"] * x["hi"]) - 1)
        x["mde_neg"], x["mde_pos"] = 100 * (math.exp(-2.8 * x["se"] * x["K"]) - 1), 100 * (math.exp(2.8 * x["se"] * x["K"]) - 1)
    else:
        x["ef_lo"], x["ef_hi"] = x["K"] * x["lo"], x["K"] * x["hi"]; x["mde_neg"], x["mde_pos"] = -2.8 * x["se"] * x["K"], 2.8 * x["se"] * x["K"]
    x["distinguivel"] = (x["lo"] > 0 or x["hi"] < 0) and x["p"] < 0.05

# ================= veredito (regra da seção 3) =================
pri = RES[0]; s4 = next(x for x in RES if x["analise"] == "S4_escore_unico"); rz = next(x for x in RES if x["analise"] == "S3_razao_indet" and x["grupo"] == "total")
if pri["distinguivel"]:
    if math.copysign(1, s4["b"]) != math.copysign(1, pri["b"]): VER = "inconclusivo: provável artefato das 27 trocas de onda BRC de 2021"
    elif rz["p"] < 0.05: VER = "indeterminado: a classificação da causa varia com o alinhamento"
    else: VER = "há associação entre alinhamento e a taxa (não causal)"
else:
    VER = "não distinguível de zero"

NOMES = {"primaria": "PRIMÁRIA g x p (BRC)", "S1_distancia": "S1 distância |g - p|", "S2_grupos": "S2 g x p", "S3_agr_indet": "S3 g x p, agressão+indet", "S3_razao_indet": "S3 g x p, razão indet (p.p.)",
         "S4_escore_unico": "S4 g x p, escore único 2018", "S5_sem_2016": "S5 g x p, sem 2016", "S6_BLS9": "S6 g x p, BLS9", "S7_copartidarismo": "S7 copartidarismo"}
L = ["## D2 — alinhamento federal-estadual (gerado por c09_d2_painel.py; semente 20261024)", "",
     f"Porta de reprodução: {REPRO}; SIM agressão = Atlas (0 divergências); ideologia do painel = BRC por período (2 casas); BLS9 tx_total = publicado (341 UF-anos).", "",
     f"Contraste K da primária = 5 pontos de governador x (PSL 2018 {brc[('PSL',2018)]:.4f} - PT 2018 {brc[('PT',2018)]:.4f}) = {K:.3f}. Efeito % = 100[exp(K x limite) - 1]. S1: 5 pontos de distância. S4: K = {5*(PU[2019]-PU[2015]):.3f}. S6: K = (DEM - PT, BLS9 2021) x (BOLSONARO 2021 - DILMA 2013) = {KZ:.4f}. S7: cop 0 -> 1. Razão: efeito em p.p.", "",
     f"**Veredito da primária (regra pré-registrada): {VER}.**", "",
     "| análise | grupo | desfecho | b [IC95% b ± 1,96 EP] | EP | IC95% t(26) | p wild | p Holm | n | efeito no contraste K [IC95%] | MDE 80% (±) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for x in RES:
    u = "%" if x["escala"] == "log" else " p.p."
    L.append(f"| {NOMES[x['analise']]} | {x['grupo']} | {x['desfecho']} | {x['b']:+.5f} [{x['lo']:+.5f}; {x['hi']:+.5f}] | {x['se']:.5f} | [{x['lo_t']:+.5f}; {x['hi_t']:+.5f}] | {x['p']:.3f} | "
             + (f"{x['p_holm']:.3f}" if "p_holm" in x else "—") + f" | {x['n']} | [{x['ef_lo']:+.1f}{u}; {x['ef_hi']:+.1f}{u}] | {x['mde_neg']:+.1f}{u} / {x['mde_pos']:+.1f}{u} |")
L += ["", "Leitura do sinal (seção 1 do pré-registro): b2 < 0 = UF com governador ideologicamente próximo do presidente tem taxa relativamente menor. Arma de fogo: n/d em agressão+indet e na razão (agregado não marca arma em Y22-Y24)."]
open(f"{AQUI}/c09_d2_resultados.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
with open(f"{AQUI}/c09_d2_resultados.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["analise", "grupo", "desfecho", "b", "se", "lo", "hi", "lo_t", "hi_t", "p", "p_holm", "n", "K", "escala", "ef_lo", "ef_hi", "mde_neg", "mde_pos", "distinguivel"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    # floats com 10 algarismos significativos: o último dígito binário varia entre execuções (ordem de soma do BLAS); p e tabelas não mudam
    for x in RES: w.writerow({c: (f"{x[c]:.10g}" if isinstance(x.get(c), float) else x.get(c, "")) for c in cols})
print("\n".join(L))
