"""C02 (TRIAGEM, rodada 3) — Painel F8 com causa INDETERMINADA: o desfecho "registrado" (X85-Y09) é afetado pelo próprio governo?
Critérios de decisão escritos ANTES de rodar: research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md (hash em CRITERIOS.sha256).
Método: variante `tse brc` do painel_f8.py (351 UF-anos 2012-2024; ln(taxa) = b x ideologia(0-10) + EF(UF) + EF(ano); EP agrupado por UF, CR1, G=27;
  IC95% = b ± 1,96 EP; p do bootstrap wild-cluster-t Rademacher com H0 imposta, B=4999, funções IMPORTADAS de painel_diagnosticos.py sem alterá-lo).
  Desfechos novos: (i) ln taxa de (agressão X85-Y09 + indeterminada Y10-Y34) por 100 mil do grupo; (ii) razão indet/(agressão+indet) em pontos percentuais (modelo linear,
  mesmos EF), desfecho de FALSIFICAÇÃO. Numeradores de dados/sim/sim_agressoes_agregado.csv (mesma agregação do agrega_sim.py: negros = preta+parda; não negros = branca+amarela+indígena;
  mulheres = sexo F; homens = total - mulheres; raça/sexo ignorados só entram no total). Denominadores: SIDRA 6407/6403 exatamente como no painel_f8.py.
Reprodução obrigatória (aborta se falhar): b e EP dos 6 desfechos registrados (resultados_tse_brc.md), p wild (diagnosticos.md, 1º bloco; semente 20261021, mesma ordem de sorteio),
  taxas registradas = painel_uf_ano_tse_brc.csv, contagens SIM agressão = Atlas.
Sementes: 20261021 (reprodução dos p publicados), 20261023 (desfechos novos).
LIMITES: (1) o agregado só marca `arma` dentro de X85-Y09 (Y22-Y24 sem marca): a linha "arma de fogo" é n/d nas colunas novas, sem imputação; (2) raça/cor ignorada: o CRITERIOS.md presumiu que seria muito
  maior nas indeterminadas; o MEDIDO (seção 5 da saída) é 4,1% das indeterminadas contra 3,7% das agressões no Brasil 2010-2024 (a presunção não se confirmou nacionalmente; por UF-ano pode variar); (3) a razão indet pode variar com a ideologia por causas que não são
  manipulação (capacidade de perícia, mudança de código, composição de mortes): rejeitar H0 não prova manipulação, e não rejeitar não prova ausência (reportado o viés máximo implícito do IC);
  (4) nenhum teste do 'estimado' do Atlas (série por UF-ano não está em disco); (5) 27 clusters: o IC b±1,96EP é o publicado (CR1 normal), mais curto que o de t(26); o wild p é a referência de inferência;
  (6) exploratório, NÃO causal; seis grupos x três colunas = muitas comparações: Holm declarado nos critérios.
Rodar: /opt/homebrew/bin/python3.14 -I dados/painel/painel_c02_indet.py   Saídas: dados/painel/c02_indet_resultados.md e c02_indet_resultados.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, importlib.util, json, math, re, collections
import numpy as np

D = (REPO_ROOT + "/dados")
SCR = (REPO_ROOT + "/fontes/p2-f8-dados-uf/sidra")
spec = importlib.util.spec_from_file_location("pdiag", f"{D}/painel/painel_diagnosticos.py")
pdg = importlib.util.module_from_spec(spec); spec.loader.exec_module(pdg)   # RNG nasce em 20261021 (nenhum sorteio antes da reprodução)

GRUPOS = ["total", "homens", "mulheres", "negros", "nao_negros", "arma"]
COL = {"total": "tx_total", "homens": "tx_homens", "mulheres": "tx_mulheres", "negros": "tx_negros", "nao_negros": "tx_nao_negros", "arma": "tx_arma"}
ATLAS = {"total": "homicidios_total_n", "mulheres": "homicidios_mulheres_n", "negros": "homicidios_negros_n", "nao_negros": "homicidios_nao_negros_n", "arma": "homicidios_arma_fogo_n"}
SIGLA = {'RO': 'Rondônia', 'AC': 'Acre', 'AM': 'Amazonas', 'RR': 'Roraima', 'PA': 'Pará', 'AP': 'Amapá', 'TO': 'Tocantins', 'MA': 'Maranhão', 'PI': 'Piauí', 'CE': 'Ceará', 'RN': 'Rio Grande do Norte',
         'PB': 'Paraíba', 'PE': 'Pernambuco', 'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia', 'MG': 'Minas Gerais', 'ES': 'Espírito Santo', 'RJ': 'Rio de Janeiro', 'SP': 'São Paulo', 'PR': 'Paraná',
         'SC': 'Santa Catarina', 'RS': 'Rio Grande do Sul', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso', 'GO': 'Goiás', 'DF': 'Distrito Federal'}

# ---------- painel registrado (do CSV do dossiê) ----------
rows0 = list(csv.DictReader(open(f"{D}/painel/painel_uf_ano_tse_brc.csv", encoding="utf-8")))
assert len(rows0) == 351
ufs = sorted({r["uf"] for r in rows0})
assert len(ufs) == 27

# ---------- reprodução 1: b, EP (método iterativo do painel_f8.py) contra resultados_tse_brc.md ----------
def twfe_iter(y, x, uf, ano):
    y = np.array(y, float); x = np.array(x, float); uf = np.array(uf); ano = np.array(ano)
    def demean(v):
        v = v.copy()
        for _ in range(50):
            for g in (uf, ano):
                for k in np.unique(g): v[g == k] -= v[g == k].mean()
        return v
    yd, xd = demean(y), demean(x)
    b = (xd @ yd) / (xd @ xd); e = yd - b * xd
    S = sum((xd[uf == k] @ e[uf == k]) ** 2 for k in np.unique(uf)); G = len(np.unique(uf)); n = len(y); k = 1 + G + len(np.unique(ano)) - 1
    return b, math.sqrt(S / (xd @ xd) ** 2 * G / (G - 1) * (n - 1) / (n - k))

pub = {}
for l in open(f"{D}/painel/resultados_tse_brc.md", encoding="utf-8"):
    m = re.match(r"\| (tx_\w+) \| ([+-]\d\.\d{4}) \| (\d\.\d{4}) \| \[", l)
    if m and m.group(1) not in pub: pub[m.group(1)] = (float(m.group(2)), float(m.group(3)))
assert len(pub) == 6, pub
for g in GRUPOS:
    r = [x for x in rows0 if float(x[COL[g]]) > 0]
    b, se = twfe_iter([math.log(float(x[COL[g]])) for x in r], [float(x["ideologia"]) for x in r], [x["uf"] for x in r], [int(x["ano"]) for x in r])
    assert abs(b - pub[COL[g]][0]) < 5.1e-5 and abs(se - pub[COL[g]][1]) < 5.1e-5 and len(r) == 351, (g, b, se, pub[COL[g]])

# ---------- reprodução 2: p wild publicados (diagnosticos.md, 1º bloco), mesma semente e ordem ----------
pubp = {}
txt = open(f"{D}/painel/diagnosticos.md", encoding="utf-8").read().split("## Secundária")[0]
for l in txt.splitlines():
    m = re.match(r"\| (tx_\w+) \| ([+-]\d\.\d{4}) \((\d\.\d{4})\) \| (\d\.\d{3}) \|", l)
    if m: pubp[m.group(1)] = float(m.group(4))
assert len(pubp) == 6, pubp

def modelo(rows, ycol_vals, wild=True):
    """b, EP (CR1), p wild para um vetor y alinhado a rows (FE de UF e ano, como painel_diagnosticos)."""
    y = np.array(ycol_vals, float); x = np.array([float(r["ideologia"]) for r in rows]); cl = np.array([r["uf"] for r in rows])
    F = pdg.dummies(rows); M = pdg.residuador(F); kfe = np.linalg.matrix_rank(F)
    b, se, _, _, _ = pdg.ols_fwl(y, x, M, cl, kfe)
    p = pdg.wild_p(y, x, M, cl, kfe)[0] if wild else None
    return b[0], se[0], p

reg = {}
for g in GRUPOS:   # ordem idêntica à do bloco() de painel_diagnosticos.py: total, homens, mulheres, negros, não negros, arma
    r = [x for x in rows0 if float(x[COL[g]]) > 0]
    reg[g] = modelo(r, [math.log(float(x[COL[g]])) for x in r])
    assert abs(reg[g][2] - pubp[COL[g]]) < 5e-4, ("p wild não reproduz", g, reg[g][2], pubp[COL[g]])
REPRO_P = {g: (reg[g][2], pubp[COL[g]]) for g in GRUPOS}

# ---------- populações (cópia literal da lógica do painel_f8.py) ----------
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

# ---------- SIM agregado ----------
cnt = collections.Counter()   # (nome_uf, ano, grupo_causa, recorte) -> n
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
    if r["raca"] == "ign": cnt[(uf, a, g, "raca_ign")] += n
def n_(uf, a, g, rec):
    if rec == "homens": return cnt[(uf, a, g, "total")] - cnt[(uf, a, g, "mulheres")]
    return cnt[(uf, a, g, rec)]

# reprodução 3: SIM agressão = Atlas (contagens) e taxa registrada recomputada = CSV
atl = {}
for r in csv.DictReader(open(f"{D}/atlas_uf_series.csv", encoding="utf-8")):
    if r["valor"] != "" and r["variavel"].endswith("_n"): atl[(r["uf"], int(r["ano"]), r["variavel"])] = float(r["valor"])
mism = collections.Counter(); chk = 0; maxdiff = 0.0
for r in rows0:
    uf, a = r["uf"], int(r["ano"])
    for g in ATLAS:
        chk += 1
        if n_(uf, a, "agressao", g) != atl[(uf, a, ATLAS[g])]: mism[g] += 1
    for g in ("total", "homens", "mulheres", "negros", "nao_negros"):
        t = n_(uf, a, "agressao", g) / pop[(uf, a)][POPG[g]] * 1e5; maxdiff = max(maxdiff, abs(t - float(r[COL[g]])))
    maxdiff = max(maxdiff, abs(n_(uf, a, "agressao", "arma") / pop[(uf, a)]["Total"] * 1e5 - float(r["tx_arma"])))
assert not mism and maxdiff < 1e-9, (mism, maxdiff)

# ---------- desfechos novos (5 grupos avaliáveis) ----------
rng_new = np.random.default_rng(20261023); pdg.RNG = rng_new
G5 = ["total", "homens", "mulheres", "negros", "nao_negros"]
new = {}; razao_media = {}
for g in G5:
    y1 = []; y2 = []
    for r in rows0:
        uf, a = r["uf"], int(r["ano"]); ag = n_(uf, a, "agressao", g); ind = n_(uf, a, "indet", g)
        y1.append(math.log((ag + ind) / pop[(uf, a)][POPG[g]] * 1e5)); y2.append(100.0 * ind / (ag + ind))
    razao_media[g] = float(np.mean(y2))
    new[(g, "agr_ind")] = modelo(rows0, y1)
    new[(g, "razao")] = modelo(rows0, y2)

def holm(ps):
    o = sorted(range(len(ps)), key=lambda i: ps[i]); adj = [0] * len(ps); run = 0.0
    for rank, i in enumerate(o):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj
h_agr = dict(zip(G5, holm([new[(g, "agr_ind")][2] for g in G5])))
sec = [g for g in G5 if g != "total"]; h_raz = dict(zip(sec, holm([new[(g, "razao")][2] for g in sec])))

def ic(b, se): return b - 1.96 * se, b + 1.96 * se
def ex(b, k=5): return 100 * (math.exp(k * b) - 1)
def fmt(b, se, p, nd=4):
    lo, hi = ic(b, se); return f"{b:+.{nd}f} [{lo:+.{nd}f}; {hi:+.{nd}f}] p={p:.3f}"

# descritivos de completude e nível da razão
nat = collections.defaultdict(lambda: collections.Counter())
for (uf, a, g, rec), n in cnt.items():
    if rec == "total": nat[g]["tot"] += n
    if rec == "raca_ign": nat[g]["ign"] += n
L = ["# C02 — painel F8 com causa indeterminada (gerado por painel_c02_indet.py; semente 20261021 reprodução, 20261023 desfechos novos)", "",
     "> [!NOTE]", "> Leia o cabeçalho do script: exploratório, NÃO causal; arma de fogo n/d nas colunas novas; viés de completude racial; 27 clusters. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`.", "",
     "## 0. Reprodução dos números publicados (todas passaram; senão o script aborta)", "",
     f"- b e EP dos 6 desfechos registrados = `resultados_tse_brc.md` (4 casas); n = 351.",
     "- p wild dos 6 registrados (mesma semente/ordem): " + "; ".join(f"{g} {REPRO_P[g][0]:.3f} (pub. {REPRO_P[g][1]:.3f})" for g in GRUPOS) + ".",
     f"- Contagens SIM agressão X85-Y09 por UF-ano = Atlas em {chk} comparações (total, mulheres, negros, não negros, arma de fogo), 0 divergências; taxas recomputadas = CSV do painel (dif. máxima {maxdiff:.1e}).", "",
     "## 1. Tabela principal: b por 1 ponto de ideologia (escala 0-10; maior = mais à direita), IC95% = b ± 1,96 EP (CR1), p do wild-cluster-t", "",
     "| grupo | (a) registrado X85-Y09, ln taxa | (b) agressão + indeterminada, ln taxa | (c) razão indet/(agressão+indet), p.p. |", "|---|---|---|---|"]
for g in GRUPOS:
    a_ = fmt(*reg[g]) if True else ""
    if g == "arma": L.append(f"| arma de fogo | {a_} | n/d | n/d |"); continue
    L.append(f"| {g.replace('nao_negros','não negros')} | {a_} | {fmt(*new[(g,'agr_ind')])} | {fmt(*new[(g,'razao')], nd=3)} |")
L += ["", "Razão média indet/(agressão+indet) por grupo (nível, %): " + "; ".join(f"{g} {razao_media[g]:.1f}%" for g in G5) + ".", "",
      "## 2. Limites exatos 100[exp(5b)-1] (troca PT 2,97 -> ~8) do IC95% de (a) e (b)", "", "| grupo | (a) registrado | (b) agressão + indet |", "|---|---|---|"]
for g in G5:
    la = ic(*reg[g][:2]); lb = ic(*new[(g, "agr_ind")][:2])
    L.append(f"| {g.replace('nao_negros','não negros')} | [{ex(la[0]):+.1f}%; {ex(la[1]):+.1f}%] | [{ex(lb[0]):+.1f}%; {ex(lb[1]):+.1f}%] |")
L += ["", "## 3. Teste de falsificação (c): viés máximo implícito em b registrado", "",
      "Se a razão r = indet/(agressão+indet) mudasse com a ideologia, o registrado seria (1-r) x total: d ln(registrado) = -(d r)/(1-r). Com b_c em p.p. por ponto e r média do grupo, o IC95% de b_c implica, numa troca de 5 pontos, variação do registrado (só por reclassificação) entre:", "",
      "| grupo | b razão (p.p./ponto) [IC95%] | p wild | p Holm (4 secundários) | viés implícito em 5 pontos (%) |", "|---|---|---|---|---|"]
for g in G5:
    b, se, p = new[(g, "razao")]; lo, hi = ic(b, se); rm = razao_media[g] / 100
    v = sorted([100 * (math.exp(-5 * (x / 100) / (1 - rm)) - 1) for x in (lo, hi)])
    L.append(f"| {g.replace('nao_negros','não negros')} | {b:+.3f} [{lo:+.3f}; {hi:+.3f}] | {p:.3f} | " + (f"{h_raz[g]:.3f}" if g in h_raz else "primário (sem ajuste)") + f" | [{v[0]:+.1f}%; {v[1]:+.1f}%] |")
L += ["", "## 4. Holm sobre os 5 grupos de (b)", "", "| grupo | p wild | p Holm |", "|---|---|---|"]
for g in G5: L.append(f"| {g.replace('nao_negros','não negros')} | {new[(g,'agr_ind')][2]:.3f} | {h_agr[g]:.3f} |")
L += ["", "## 5. Completude racial (limite do negros/não negros nas colunas novas)", "",
      f"Raça/cor ignorada no Brasil 2010-2024 (soma): agressão {100*nat['agressao']['ign']/nat['agressao']['tot']:.1f}% dos óbitos; indeterminada {100*nat['indet']['ign']/nat['indet']['tot']:.1f}%. Taxas por raça das indeterminadas subestimam e podem variar com a completude por UF-ano.", ""]
open(f"{D}/painel/c02_indet_resultados.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
with open(f"{D}/painel/c02_indet_resultados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["grupo", "desfecho", "b", "ep", "ic_lo", "ic_hi", "p_wild", "p_holm", "razao_media_pct"])
    for g in GRUPOS:
        b, se, p = reg[g]; w.writerow([g, "registrado_ln", b, se, *ic(b, se), p, "", ""])
    for g in G5:
        for nome in ("agr_ind", "razao"):
            b, se, p = new[(g, nome)]
            ph = h_agr[g] if nome == "agr_ind" else (h_raz.get(g, ""))
            w.writerow([g, {"agr_ind": "agressao_mais_indet_ln", "razao": "razao_indet_pp"}[nome], b, se, *ic(b, se), p, ph, razao_media[g]])
print("\n".join(L))
