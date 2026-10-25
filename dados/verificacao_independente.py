"""Verificação INDEPENDENTE dos resultados-chave: cada número é recalculado por um caminho de cálculo DIFERENTE do script que o gerou
(outra álgebra, outra biblioteca de leitura) e comparado com o arquivo gerado e com o texto dos dossiês.
  V1 correlação parcial de Spearman: v2 usa regressão dos postos; aqui, inversa da matriz de correlação (fórmula da precisão), dados lidos com pandas.
  V2 IC da parcela LGB+ implícita na PNS: v1 usa Monte Carlo; aqui, método delta (forma fechada) sobre o logit.
  V3 painel TWFE: o script usa Frisch-Waugh com matriz projetora; aqui, MQO com TODAS as dummies explícitas (lstsq) e CR1 pelo estimador sanduíche direto.
  V4 consistência texto x arquivo: números citados nos dossiês são procurados, formatados em PT-BR, nos arquivos gerados.
Rodar: /opt/homebrew/bin/python3.14 -I dados/verificacao_independente.py ; exit 1 se algum teste numérico falhar (tolerâncias declaradas em cada V)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[1])  # raiz configurável
import csv, json, math, re, sys
import numpy as np
import pandas as pd

BASE = REPO_ROOT
D = f"{BASE}/dados"
falhas = []


def confere(nome, a, b, tol):
    ok = abs(a - b) <= tol
    if not ok:
        falhas.append(nome)
    print(f"  {'OK ' if ok else 'FALHA'} {nome}: independente={a:.4f} gerado={b:.4f} (tol {tol})")


# ---------- V1 ----------
print("V1 correlação parcial de Spearman (fórmula da inversa da matriz de correlação, pandas)")
sin = pd.read_csv(f"{D}/sinan/serie_campo55_uf_ano.csv"); sin = sin[sin.uf != "BR"]
anu = pd.read_csv(f"{D}/anuario/anuario_lgbtfobia_uf_ano_v2.csv")
EDN = {2022: 2024, 2023: 2025, 2024: 2026, 2025: 2026}
nome2uf = {"Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA", "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA", "Piauí": "PI", "Ceará": "CE",
           "Rio Grande do Norte": "RN", "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE", "Bahia": "BA", "Minas Gerais": "MG", "Espírito Santo": "ES",
           "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR", "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT",
           "Goiás": "GO", "Distrito Federal": "DF"}
pop = pd.DataFrame([{"uf": nome2uf[x["D1N"]], "pop": float(x["V"])} for x in json.load(open(f"{BASE}/fontes/p2-f8-dados-uf/tabnet/raw/sidra_9514.json"))[1:]])
gerado = pd.read_csv(f"{D}/concordancia/concordancia_v2.csv"); gerado = gerado[gerado.especificacao.str.startswith("S0")].set_index("ano")
for ano in (2022, 2023, 2024, 2025):
    a = anu[(anu.ano_dado == ano) & (anu.edicao == EDN[ano]) & anu.registros.notna()][["uf", "registros"]]
    m = sin[sin.ano == ano][["uf", "m_lgbtfobia"]].merge(a, on="uf").merge(pop, on="uf")
    r = m[["m_lgbtfobia", "registros", "pop"]].rank().corr().values          # correlação de Pearson dos postos = Spearman
    P = np.linalg.inv(r); rho = -P[0, 1] / math.sqrt(P[0, 0] * P[1, 1])        # correlação parcial 0,1 | 2 pela matriz de precisão
    confere(f"parcial {ano} (n={len(m)})", rho, float(gerado.loc[ano, "rho_parcial"]), 0.0015)

# ---------- V2 ----------
print("V2 IC95% da parcela LGB+ implícita na PNS (método delta no logit) vs Monte Carlo do triangulacao_pns_sinan.md")
PNS = {"lgb": (1.89, 1.73, 2.07), "het": (94.75, 94.46, 95.03), "fl": (14.70, 11.16, 19.12), "fh": (3.82, 3.57, 4.09)}
se = {k: (math.log(h) - math.log(l)) / (2 * 1.96) for k, (e, l, h) in PNS.items()}
lg = lambda p: math.log(p / (1 - p))
a, b = PNS["lgb"][0] * PNS["fl"][0], PNS["het"][0] * PNS["fh"][0]
p = a / (a + b); s = math.sqrt(sum(v * v for v in se.values()))
lo, hi = 1 / (1 + math.exp(-(lg(p) - 1.96 * s))), 1 / (1 + math.exp(-(lg(p) + 1.96 * s)))
tri = open(f"{D}/sinan/triangulacao_pns_sinan.md", encoding="utf-8").read()
m = re.search(r"\| A\. só respondentes.*?\| ([\d.]+)% \| ([\d.]+)% a ([\d.]+)% \|", tri)
confere("PNS cenário A ponto (%)", 100 * p, float(m.group(1)), 0.01)
confere("PNS cenário A IC inf (%)", 100 * lo, float(m.group(2)), 0.15)
confere("PNS cenário A IC sup (%)", 100 * hi, float(m.group(3)), 0.15)

# ---------- V3 ----------
print("V3 painel TWFE: MQO com dummies explícitas + CR1 direto (sem Frisch-Waugh) vs resultados_tse_brc.md")
pt = pd.read_csv(f"{D}/painel/painel_uf_ano_tse_brc.csv")
res = open(f"{D}/painel/resultados_tse_brc.md", encoding="utf-8").read()
for oc in ("tx_total", "tx_homens", "tx_mulheres", "tx_negros", "tx_nao_negros", "tx_arma"):
    d = pt[pt[oc] > 0].reset_index(drop=True)
    y = np.log(d[oc].values); X = np.column_stack([d.ideologia.values, pd.get_dummies(d.uf).values.astype(float), pd.get_dummies(d.ano).values[:, 1:].astype(float)])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta; XtXi = np.linalg.pinv(X.T @ X)
    meat = sum(np.outer(X[g.index].T @ e[g.index], X[g.index].T @ e[g.index]) for _, g in d.groupby("uf"))
    n, k, G = X.shape[0], np.linalg.matrix_rank(X), d.uf.nunique()
    V = (G / (G - 1)) * ((n - 1) / (n - k)) * XtXi @ meat @ XtXi
    mm = re.search(rf"\| {oc} \| ([+-][\d.]+) \| ([\d.]+) \|", res)
    confere(f"{oc} b", beta[0], float(mm.group(1)), 0.0002)
    confere(f"{oc} EP", math.sqrt(V[0, 0]), float(mm.group(2)), 0.0005)

# ---------- V4 ----------
print("V4 texto dos dossiês x arquivos gerados (números formatados em PT-BR)")
cons = open(f"{BASE}/docs/dossies/DOSSIE-CONSOLIDADO-2026-10-12.md", encoding="utf-8").read()
par2 = open(f"{BASE}/docs/dossies/DOSSIE-2026-10-11-parte2.md", encoding="utf-8").read()
resumo = open(f"{D}/concordancia/resumo.md", encoding="utf-8").read()
v2 = open(f"{D}/concordancia/concordancia_v2.md", encoding="utf-8").read()
pt_br = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
checks = []
for ano in (2022, 2023, 2024, 2025):
    checks.append((f"parcial {ano}", pt_br(gerado.loc[ano, "rho_parcial"]), resumo))
pool = re.search(r"Pooled 2022-25.*?: (-?[\d.]+) \[IC95% bootstrap por UF: (-?[\d.]+); (-?[\d.]+)\]", v2)
checks.append(("pooled", f"{pt_br(float(pool.group(1)))} [{pt_br(float(pool.group(2)))}; {pt_br(float(pool.group(3)))}]", resumo.replace("-", "-")))
checks.append(("pooled no consolidado", f"{pt_br(float(pool.group(1)))} [{pt_br(float(pool.group(2)))}; {pt_br(float(pool.group(3)))}]", cons))
checks.append(("IC PNS 5,3-9,0 no consolidado", "5,3%-9,0%", cons)); checks.append(("IC PNS na parte2", "5,3% a 9,0%", par2))
rot = {"tx_total": "total", "tx_homens": "homens", "tx_mulheres": "mulheres", "tx_negros": "negros", "tx_nao_negros": "não negros", "tx_arma": "arma de fogo"}
sg = lambda v: ("+" if v >= 0 else "−") + f"{abs(round(v, 3)):.3f}".replace(".", ",")
for oc, rotulo in rot.items():
    mm = re.search(rf"\| {oc} \| ([+-][\d.]+) \| [\d.]+ \| \[([+-][\d.]+), ([+-][\d.]+)\]", res)
    linha = f"| {rotulo} | {sg(float(mm.group(1)))} | [{sg(float(mm.group(2)))}; {sg(float(mm.group(3)))}] |"
    checks.append((f"painel {rotulo} (b e IC95%)", linha, cons)); checks.append((f"painel {rotulo} na parte2", linha, par2))
for nome, token, doc in checks:
    ok = token.replace("-", "−") in doc.replace("-", "−") or token in doc
    if not ok:
        falhas.append("V4 " + nome)
    print(f"  {'OK ' if ok else 'FALHA'} {nome}: procurado {token!r}")
print("\nRESULTADO:", "TUDO OK" if not falhas else f"FALHAS: {falhas}")
sys.exit(1 if falhas else 0)
