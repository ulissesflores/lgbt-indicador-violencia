"""S09. Testes de 'inflacao' (descritivos, ecologicos, n=27 UFs): (b) GGB 2019 por UF x populacao, internet (PNAD C TIC 2019,
% domicilios com uso de internet), taxa de homicidio (Atlas/SIM 2019), notificacoes Sinan campo 55 LGBTfobia 2019;
(c) serie anual GGB 2000-2025 x uso de internet (PNAD C, 2016-2025) x Sinan LGBTfobia x homicidios (SIM); (d) sensibilidade da manchete.
Uso: python3.14 -I s09_uf_series.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, json, math
from pathlib import Path
import numpy as np
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"
IB = ROOT/"fontes/p3-ggb/ibge"; F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"; D = ROOT/"dados"
UFS = {"11":"RO","12":"AC","13":"AM","14":"RR","15":"PA","16":"AP","17":"TO","21":"MA","22":"PI","23":"CE","24":"RN","25":"PB","26":"PE","27":"AL","28":"SE","29":"BA","31":"MG","32":"ES","33":"RJ","35":"SP","41":"PR","42":"SC","43":"RS","50":"MS","51":"MT","52":"GO","53":"DF"}
ggb = list(csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()))
cnt = {}
for g in ggb: cnt[g["uf"]] = cnt.get(g["uf"], 0) + 1
pop = {UFS[x["D1C"]]: float(x["V"]) for x in json.load(open(IB/"sidra6579_pop_uf_2019.json"))[1:]}
net = {}; tot = {}
for x in json.load(open(IB/"sidra7307_uf_2019.json"))[1:]:
    if x["D5N"] == "Total": tot[UFS[x["D1C"]]] = float(x["V"])
    else: net[UFS[x["D1C"]]] = float(x["V"])
internet = {u: 100 * net[u] / tot[u] for u in tot}
nom = {"Rondônia":"RO","Acre":"AC","Amazonas":"AM","Roraima":"RR","Pará":"PA","Amapá":"AP","Tocantins":"TO","Maranhão":"MA","Piauí":"PI","Ceará":"CE","Rio Grande do Norte":"RN","Paraíba":"PB","Pernambuco":"PE","Alagoas":"AL","Sergipe":"SE","Bahia":"BA","Minas Gerais":"MG","Espírito Santo":"ES","Rio de Janeiro":"RJ","São Paulo":"SP","Paraná":"PR","Santa Catarina":"SC","Rio Grande do Sul":"RS","Mato Grosso do Sul":"MS","Mato Grosso":"MT","Goiás":"GO","Distrito Federal":"DF"}
hom = {nom[r["uf"]]: float(r["valor"]) for r in csv.DictReader((D/"atlas_uf_series.csv").open()) if r["ano"] == "2019" and r["variavel"] == "homicidios_total_taxa"}
sin = {r["uf"]: int(r["m_lgbtfobia"]) for r in csv.DictReader((D/"sinan/serie_campo55_uf_ano.csv").open()) if r["ano"] == "2019"}
ufs = sorted(pop)
rows = [dict(uf=u, ggb=cnt.get(u, 0), pop=pop[u], ggb_por_milhao=1e6*cnt.get(u, 0)/pop[u], internet_dom_pct=internet[u], hom_taxa_100mil=hom[u], sinan_lgbtfobia_n=sin[u], sinan_por_milhao=1e6*sin[u]/pop[u]) for u in ufs]
with (F3/"dados/uf_2019.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows([{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in rows])
def rank(a): 
    o = np.argsort(a, kind="mergesort"); r = np.empty(len(a)); r[o] = np.arange(len(a)); 
    for v in set(a):  # empates -> media dos ranks
        ix = [i for i, x in enumerate(a) if x == v]
        if len(ix) > 1: r[ix] = r[ix].mean()
    return r
def spearman(a, b): 
    ra, rb = rank(list(a)), rank(list(b)); return float(np.corrcoef(ra, rb)[0, 1])
def perm_p(a, b, n=20000, seed=7):
    rng = np.random.default_rng(seed); r0 = spearman(a, b); b = np.array(b); c = 0
    for _ in range(n):
        if abs(spearman(a, rng.permutation(b))) >= abs(r0) - 1e-12: c += 1
    return (c + 1) / (n + 1)
X = lambda k: [r[k] for r in rows]
out = {"n_uf": len(rows), "total_ggb_uf": sum(X("ggb")), "spearman": {}}
for nome, a, b in [("ggb_n ~ populacao", X("ggb"), X("pop")), ("ggb_por_milhao ~ internet_dom_pct", X("ggb_por_milhao"), X("internet_dom_pct")),
                   ("ggb_por_milhao ~ hom_taxa_100mil", X("ggb_por_milhao"), X("hom_taxa_100mil")), ("ggb_por_milhao ~ sinan_por_milhao", X("ggb_por_milhao"), X("sinan_por_milhao")),
                   ("sinan_por_milhao ~ internet_dom_pct", X("sinan_por_milhao"), X("internet_dom_pct")), ("hom_taxa ~ internet_dom_pct", X("hom_taxa_100mil"), X("internet_dom_pct"))]:
    out["spearman"][nome] = dict(rho=round(spearman(a, b), 3), p_perm=round(perm_p(a, b), 4))
# Poisson GLM (IRLS) com offset log(pop): ggb ~ internet_z + hom_z ; erro-padrao robusto (sanduiche HC0)
def poisson(y, Xm, off, it=100):
    b = np.zeros(Xm.shape[1]); b[0] = math.log(y.sum() / np.exp(off).sum())
    for _ in range(it):
        mu = np.exp(Xm @ b + off); W = mu; z = Xm @ b + (y - mu) / mu
        bn = np.linalg.solve(Xm.T @ (W[:, None] * Xm), Xm.T @ (W * z))
        if np.max(abs(bn - b)) < 1e-10: b = bn; break
        b = bn
    mu = np.exp(Xm @ b + off); bread = np.linalg.inv(Xm.T @ (mu[:, None] * Xm)); meat = Xm.T @ (((y - mu) ** 2)[:, None] * Xm)
    cov = bread @ meat @ bread; return b, np.sqrt(np.diag(cov)), float(2 * np.sum(np.where(y > 0, y * np.log(np.where(y > 0, y / mu, 1)), 0) - (y - mu)))
y = np.array(X("ggb")); off = np.log(np.array(X("pop")) / 1e6)
z = lambda a: (np.array(a) - np.mean(a)) / np.std(a)
for nome, cols in [("ggb ~ internet", [z(X("internet_dom_pct"))]), ("ggb ~ internet + homicidio", [z(X("internet_dom_pct")), z(X("hom_taxa_100mil"))]), ("ggb ~ homicidio", [z(X("hom_taxa_100mil"))])]:
    Xm = np.column_stack([np.ones(len(y))] + cols); b, se, dev = poisson(y, Xm, off)
    out["poisson_" + nome] = dict(coef=[round(float(v), 3) for v in b], irr_por_dp=[round(float(math.exp(v)), 3) for v in b[1:]], ep_robusto=[round(float(v), 3) for v in se], ic95_irr=[[round(math.exp(b[i] - 1.96 * se[i]), 2), round(math.exp(b[i] + 1.96 * se[i]), 2)] for i in range(1, len(b))], deviance=round(dev, 1), dispersao=round(dev / (len(y) - Xm.shape[1]), 2))
# ---- (c) serie anual ----
ggb_ano = {2000:130,2001:132,2002:126,2003:125,2004:158,2005:135,2006:112,2007:142,2008:187,2009:199,2010:260,2011:266,2012:338,2013:314,2014:329,2015:319,2016:343,2017:445,2018:420,2019:329,2020:237,2021:300,2022:256,2023:257,2024:291,2025:257}
net_br = {}
for x in json.load(open(IB/"sidra7331_br_2016_2025.json"))[1:]:
    if x["D3C"] == "10659" and x["D4N"] == "Total" and x["D5N"] in ("Total", "10 anos ou mais") : net_br[int(x["D2N"])] = float(x["V"])
sin_ano = {}; sin_br = {}
# v0.3 (2026-10-24, correção R2): o CSV traz 27 UFs + a linha "BR" (total nacional). Antes a soma incluía a linha BR e DOBRAVA o total;
# agora soma só as 27 UFs e confere a identidade soma(UFs) == BR em todo ano (aborta se falhar).
for r in csv.DictReader((D/"sinan/serie_campo55_uf_ano.csv").open()):
    if r["uf"] == "BR": sin_br[int(r["ano"])] = int(r["m_lgbtfobia"]); continue
    sin_ano[int(r["ano"])] = sin_ano.get(int(r["ano"]), 0) + int(r["m_lgbtfobia"])
assert sin_ano == sin_br, ("soma das 27 UFs difere da linha BR", sin_ano, sin_br)
atl = {}
for r in csv.DictReader((D/"atlas_uf_series.csv").open()):
    if r["variavel"] == "homicidios_total_n": atl[int(r["ano"])] = atl.get(int(r["ano"]), 0) + float(r["valor"])
ser = [dict(ano=a, ggb=ggb_ano[a], internet_pct_10mais=net_br.get(a, ""), sinan_lgbtfobia_n=sin_ano.get(a, ""), homicidios_sim=int(atl[a]) if a in atl else "") for a in sorted(ggb_ano)]
with (F3/"dados/serie_ggb_vs_cobertura.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ser[0].keys())); w.writeheader(); w.writerows(ser)
def sp(k1, k2, a0, a1):
    p = [(r[k1], r[k2]) for r in ser if a0 <= r["ano"] <= a1 and r[k1] != "" and r[k2] != ""]
    return dict(n=len(p), rho=round(spearman([x for x, _ in p], [y_ for _, y_ in p]), 3)) if len(p) >= 4 else None
out["serie"] = {"ggb~internet 2016-2025": sp("ggb", "internet_pct_10mais", 2016, 2025), "ggb~sinan_lgbtfobia 2015-2025": sp("ggb", "sinan_lgbtfobia_n", 2015, 2025),
                "ggb~homicidios_sim 2015-2023": sp("ggb", "homicidios_sim", 2015, 2023), "sinan_lgbtfobia~internet 2016-2025": sp("sinan_lgbtfobia_n", "internet_pct_10mais", 2016, 2025)}
# variacao
out["variacao"] = dict(ggb_2000_2017=ggb_ano[2017] / ggb_ano[2000], ggb_2017_2025=ggb_ano[2025] / ggb_ano[2017], internet_2016_2025=net_br.get(2025, 0) / net_br.get(2016, 1) if net_br else None,
                       sinan_lgbtfobia_2015_2025=sin_ano[2025] / sin_ano[2015])
(F3/"dados/inflacao_uf_serie.json").write_text(json.dumps(out, ensure_ascii=False, indent=1)); print(json.dumps(out, ensure_ascii=False, indent=1)); print(net_br)
