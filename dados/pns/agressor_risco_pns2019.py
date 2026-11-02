"""Quem agrediu e o risco por tipo de agressor, LGB+ x heterossexuais, PNS 2019; sensibilidade com estado civil.

Pedido do autor (2026-10-29, conversa sobre a afirmação A1): mostrar com números de desenho amostral
(1) a composição dos agressores entre as vítimas de violência física, com intervalo e com a diferença LGB+ - het;
(2) o RISCO na população por tipo de agressor (proporção de adultos que sofreram violência física por aquele tipo de
    agressor em 12 meses), com razão LGB+/het e intervalo: a fatia entre vítimas não é risco;
(3) a razão de prevalências ajustada de violência física com o estado civil acrescentado ao ajuste do
    seguro_pns2019.py. ANÁLISE FEITA DEPOIS DE VER OS RESULTADOS (não pré-registrada): declarada como desvio.
(4) [2026-10-29, revisão por três modelos, críticas GRO-01 e AST-01] razão AJUSTADA por tipo de agressor (mesmo ajuste
    do 2,82, e o mesmo + estado civil): o risco por agressor das seções 1 e 2 é bruto;
(5) [crítica GRO-11] razão de violência física separada por quem preencheu o módulo (V00101: o próprio morador ou o
    entrevistador), porque a fatia que se declara LGB+ muda com o modo; e o fluxo da amostra (88.531 -> n analítico).
(6) [2026-11-01, decisão do autor; críticas ARG-02 e AST-R2-02 da r6] razão por tipo de agressor também com o cônjuge
    no domicílio no ajuste; e todas as razões ajustadas refeitas SEM os adultos de cor ou raça ignorada (C009 = 9), que
    no ajuste publicado entram na categoria de referência com os não negros. Sensibilidades: os números publicados não mudam.
Mesmo método do seguro_pns2019.py (linearização de Taylor, último conglomerado; Poisson ponderado com variância robusta
de desenho). Reprodução obrigatória antes do novo: as fatias de parceiro/ex e família publicadas em seguro_pns2019.md.
LIMITES: a PNS não pergunta o motivo do agressor nem a orientação sexual dele; V018 é o episódio mais grave; 179
vítimas LGB+ (fatias com intervalo largo); uma única edição (2019). Nada aqui atribui motivo a nenhum agressor.
Rodar: /opt/homebrew/bin/python3.14 -I dados/pns/agressor_risco_pns2019.py   (REPO_ROOT = pasta que contém fontes/)
Saídas: dados/pns/agressor_risco_pns2019.md e .csv
"""
import math
import os
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[2])
P = BASE / "fontes/q1-textointegral/F2/pns2019"
OUT = Path(__file__).resolve().parent
LAYOUT = P / "input_PNS_2019_utf8.txt"
pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
spec = {m.group(2): (int(m.group(1)), int(m.group(3))) for l in LAYOUT.read_text(encoding="utf8", errors="replace").splitlines() if (m := pat.match(l))}
V12 = ["V00201", "V00202", "V00203", "V00204", "V00205", "V01401", "V01402", "V01403", "V01404", "V01405", "V02701", "V02702"]
want = ["V0001", "V0024", "UPA_PNS", "V0026", "C006", "C008", "C009", "VDD004A", "Y008", "V00291", "V001", "V00101", "C011", "C01001"] + V12 + ["V018"]
cols = [(spec[k][0] - 1, spec[k][0] - 1 + spec[k][1]) for k in want]
txt = P / "x/PNS_2019.txt"
if txt.exists():
    raw = pd.read_fwf(txt, colspecs=cols, names=want, header=None, dtype=str)
else:  # lê direto do zip oficial do IBGE, sem extrair
    with zipfile.ZipFile(P / "PNS_2019_20220525.zip") as z, z.open("PNS_2019.txt") as f:
        raw = pd.read_fwf(f, colspecs=cols, names=want, header=None, dtype=str)
d = raw[raw.V001.notna()].copy()
assert len(d) == 88531, len(d)

# ponytail: preparo e estimadores copiados de seguro_pns2019.py, que roda tudo ao ser importado; mesmo método, mesma ordem
d["w"] = d.V00291.astype(float)
for k in V12: d[k] = d[k].map({"1": 1.0, "2": 0.0})
d["fisica"] = d[V12[5:10]].max(axis=1)
d["psico"] = d[V12[0:5]].max(axis=1); d["sexual"] = d[V12[10:12]].max(axis=1)
d["qualquer"] = d[["psico", "fisica", "sexual"]].max(axis=1)
d["lgb"] = d.Y008.isin(["2", "3", "4"]); d["het"] = d.Y008 == "1"
d["mulher"] = d.C006 == "2"; d["negro"] = d.C009.isin(["2", "4"])
d["faixa"] = pd.cut(d.C008.astype(float), [17, 29, 44, 59, 200], labels=["18-29", "30-44", "45-59", "60+"])
d["regiao"] = d.V0001.str[0].map({"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"})
d["urbano"] = d.V0026 == "1"
d["instr"] = d.VDD004A.map({"1": "baixa", "2": "baixa", "3": "média", "4": "média", "5": "média", "6": "alta", "7": "alta"})
d["civil"] = d.C011.map({"1": "casado", "2": "separado", "3": "viúvo", "4": "solteiro"})  # 9 = ignorado -> fora
d["conjuge_mora"] = d.C01001.map({"1": 1.0, "2": 0.0})
w = d.w.values
cod_psu = pd.factorize((d.V0024 + "-" + d.UPA_PNS).values)[0]; cod_str = pd.factorize(d.V0024.values)[0]
psu_str = pd.Series(cod_str).groupby(cod_psu).first().values
n_psu_str = pd.Series(psu_str).value_counts()


def var_from_u(u):
    u = u.reshape(len(u), -1)
    t = np.zeros((cod_psu.max() + 1, u.shape[1])); np.add.at(t, cod_psu, u)
    V = np.zeros((u.shape[1], u.shape[1]))
    for h, n_h in n_psu_str.items():
        if n_h < 2: continue
        th = t[psu_str == h]; c = th - th.mean(axis=0)
        V += n_h / (n_h - 1) * (c.T @ c)
    return V


def prop(y, dom):
    dd = dom.values.astype(float); yy = np.nan_to_num(y.values.astype(float))
    W = (w * dd).sum(); p = (w * dd * yy).sum() / W
    return p, w * dd * (yy - p) / W


def ci(y, dom):
    p, u = prop(y, dom); se = math.sqrt(var_from_u(u)[0, 0]); return p, p - 1.96 * se, p + 1.96 * se


def dif(y, dom1, dom2):
    p1, u1 = prop(y, dom1); p2, u2 = prop(y, dom2); se = math.sqrt(var_from_u(u1 - u2)[0, 0])
    return p1 - p2, p1 - p2 - 1.96 * se, p1 - p2 + 1.96 * se


def rp(y, dom1, dom2):
    p1, u1 = prop(y, dom1); p2, u2 = prop(y, dom2)
    if p1 <= 0 or p2 <= 0: return (float("nan"),) * 3
    se = math.sqrt(var_from_u(u1 / p1 - u2 / p2)[0, 0]); r = p1 / p2
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se)


def poisson_lgb(yname, extras=(), sem_cor_ignorada=False):
    """RP ajustada LGB+/het (Poisson ponderado, variância robusta de desenho), ajuste do seguro_pns2019.py + extras.

    sem_cor_ignorada: tira da amostra do ajuste quem tem C009 = 9 (no ajuste publicado, o indicador de negros vale 0 para eles).
    """
    base = d.lgb | d.het
    ok = base & d.faixa.notna() & d.instr.notna() & d.regiao.notna()
    if sem_cor_ignorada:
        ok &= d.C009 != "9"
    for e in extras:
        ok &= d[e].notna()
    idx = np.where(ok.values)[0]; s = d.iloc[idx]
    X = [np.ones(len(s)), s.lgb.values.astype(float), s.mulher.values.astype(float)]
    X += [(s.faixa == k).values.astype(float) for k in ("30-44", "45-59", "60+")]
    X += [s.negro.values.astype(float)] + [(s.instr == k).values.astype(float) for k in ("média", "alta")]
    X += [(s.regiao == k).values.astype(float) for k in ("Nordeste", "Sudeste", "Sul", "Centro-Oeste")]
    X += [s.urbano.values.astype(float)]
    for e in extras:
        if e == "civil":
            X += [(s.civil == k).values.astype(float) for k in ("separado", "viúvo", "solteiro")]  # referência: casado
        else:
            X += [s[e].values.astype(float)]
    X = np.column_stack(X)
    yy = np.nan_to_num(s[yname].values.astype(float)); ww = w[idx]
    b = np.zeros(X.shape[1]); b[0] = math.log(max(yy.mean(), 1e-6))
    for _ in range(80):
        mu = np.exp(X @ b); z = X @ b + (yy - mu) / mu
        nb = np.linalg.solve((X * (ww * mu)[:, None]).T @ X, (X * (ww * mu)[:, None]).T @ z)
        if np.max(np.abs(nb - b)) < 1e-10: b = nb; break
        b = nb
    mu = np.exp(X @ b); bread = np.linalg.inv((X * (ww * mu)[:, None]).T @ X)
    sf = np.zeros((len(d), X.shape[1])); sf[idx] = X * (ww * (yy - mu))[:, None]
    V = bread @ var_from_u(sf) @ bread; se = math.sqrt(V[1, 1])
    return math.exp(b[1]), math.exp(b[1] - 1.96 * se), math.exp(b[1] + 1.96 * se), len(idx)


GRUPOS = [("Parceiro(a) ou ex", ["01", "02", "03"]), ("Familiar", ["04", "05", "06", "07"]),
          ("Amigo(a), colega ou vizinho(a)", ["08"]), ("Empregado(a), patrão ou chefe", ["09", "10"]),
          ("Pessoa conhecida (todos acima)", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]),
          ("Pessoa desconhecida", ["11"]), ("Policial", ["12"]), ("Outro", ["13"])]
vit = d.fisica == 1
AGR_COL = {}  # coluna do desfecho de cada tipo de agressor (seção 4), reusada na seção 8
pc = lambda x: f"{100 * x:.2f}".replace(".", ",")
faixa = lambda a, b: f"{pc(a)} a {pc(b)}"
L = ["# Quem agrediu e o risco por tipo de agressor, PNS 2019 (gerado por agressor_risco_pns2019.py)", "",
     "Desenho complexo; intervalos de 95%. A PNS não pergunta o motivo nem a orientação sexual do agressor. "
     f"Vítimas de violência física em 12 meses: {int((vit & d.het).sum())} heterossexuais e {int((vit & d.lgb).sum())} LGB+ (n da amostra)."]

# ---- 0. reprodução do que já está publicado em seguro_pns2019.md
PUB = {("Parceiro(a) ou ex", "het"): 37.10, ("Parceiro(a) ou ex", "lgb"): 32.92, ("Familiar", "het"): 19.25, ("Familiar", "lgb"): 31.17,
       ("Pessoa desconhecida", "het"): 23.02, ("Pessoa desconhecida", "lgb"): 16.29}
falhas = 0
for (g, grp), v in PUB.items():
    cods = dict(GRUPOS)[g]; p = ci(d.V018.isin(cods).astype(float), vit & d[grp])[0]
    falhas += abs(100 * p - v) > 0.01
L += ["", f"Reprodução de seguro_pns2019.md (6 fatias, tolerância 0,01 p.p.): divergências = {falhas}."]
assert falhas == 0, "reprodução falhou"

rows = []
# ---- 1. composição entre vítimas
L += ["", "## 1. Entre as vítimas de violência física: quem agrediu (fatia, %)", "",
      "| Agressor | Heterossexuais | LGB+ | Diferença LGB+ − het (p.p.) | A diferença é firme? |", "|---|---|---|---|---|"]
for g, cods in GRUPOS:
    y = d.V018.isin(cods).astype(float)
    a = ci(y, vit & d.het); b = ci(y, vit & d.lgb); df = dif(y, vit & d.lgb, vit & d.het)
    firme = "sim" if df[1] > 0 or df[2] < 0 else "não (o intervalo inclui zero)"
    L.append(f"| {g} | {pc(a[0])} ({faixa(max(a[1], 0), a[2])}) | {pc(b[0])} ({faixa(max(b[1], 0), b[2])}) | "
             f"{100 * df[0]:+.1f} ({100 * df[1]:+.1f} a {100 * df[2]:+.1f}) | {firme} |".replace(".", ","))
    rows.append(["fatia_entre_vitimas", g, a[0], b[0], df[0], df[1], df[2]])

# ---- 2. risco na população
L += ["", "## 2. Risco na população: adultos agredidos fisicamente em 12 meses por cada tipo de agressor (por 100 adultos)", "",
      "| Agressor | Heterossexuais | LGB+ | Razão LGB+/het |", "|---|---|---|---|"]
for g, cods in GRUPOS:
    y = (vit & d.V018.isin(cods)).astype(float)
    a = ci(y, d.het); b = ci(y, d.lgb); r = rp(y, d.lgb, d.het)
    L.append(f"| {g} | {pc(a[0])} ({faixa(max(a[1], 0), a[2])}) | {pc(b[0])} ({faixa(max(b[1], 0), b[2])}) | "
             f"{r[0]:.2f} ({r[1]:.2f} a {r[2]:.2f}) |".replace(".", ","))
    rows.append(["risco_populacao", g, a[0], b[0], r[0], r[1], r[2]])

# ---- 3. sensibilidade com estado civil (pós-hoc)
L += ["", "## 3. Razão de prevalências ajustada de violência física: o ajuste de seguro_pns2019.py e o mesmo + estado civil (análise feita depois de ver os resultados)", "",
      "| Ajuste | Razão LGB+/het | n |", "|---|---|---|"]
for nome, ex in (("sexo, idade, cor, instrução, região, urbano/rural (publicado: 2,82; 2,16 a 3,68)", ()),
                 ("o mesmo + estado civil (casado, separado, viúvo, solteiro)", ("civil",)),
                 ("o mesmo + cônjuge ou companheiro(a) mora no domicílio", ("conjuge_mora",))):
    r = poisson_lgb("fisica", ex)
    L.append(f"| {nome} | {r[0]:.2f} ({r[1]:.2f} a {r[2]:.2f}) | {r[3]} |".replace(".", ",", 3))
    rows.append(["rp_ajustada_fisica", nome, None, None, r[0], r[1], r[2]])
civ = [(k, ci(d.fisica, d.het & (d.civil == k)), ci(d.fisica, d.lgb & (d.civil == k)), int((d.lgb & (d.civil == k)).sum()))
       for k in ("casado", "separado", "viúvo", "solteiro")]
L += ["", "Prevalência de violência física por estado civil (descritivo):", "", "| Estado civil | Heterossexuais | LGB+ | n LGB+ |", "|---|---|---|---|"]
for k, a, b, n in civ:
    L.append(f"| {k} | {pc(a[0])} ({faixa(max(a[1], 0), a[2])}) | {pc(b[0])} ({faixa(max(b[1], 0), b[2])}) | {n} |")
sol = lambda grp: ci((d.civil == "solteiro").astype(float), d[grp] & d.civil.notna())[0]
L += ["", f"Solteiros entre os adultos: heterossexuais {pc(sol('het'))}%, LGB+ {pc(sol('lgb'))}%.",
      "", "Leitura: a razão que sobra depois de qualquer ajuste não é parcela causada por discriminação nem por "
      "'estilo de vida'; os dados não separam as duas explicações (VanderWeele & Robinson, 2014)."]
# ---- 4. razão AJUSTADA por tipo de agressor (crítica GRO-01/AST-01: o risco das seções 1-2 é bruto)
L += ["", "## 4. Razão de risco AJUSTADA por tipo de agressor (análise feita depois de ver os resultados)", "",
      "Desfecho: ter sofrido violência física em 12 meses e ter apontado esse tipo de agressor em V018 (uma resposta por pessoa). "
      "Colunas ajustadas: a primeira com o mesmo ajuste do 2,82; a segunda com o estado civil somado; a terceira com o cônjuge ou "
      "companheiro(a) no domicílio somado. O n é o mesmo nas três.", "",
      "| Agressor | Bruta | Ajustada (sexo, idade, cor, instrução, região, urbano/rural) | Ajustada + estado civil | "
      "Ajustada + cônjuge no domicílio | n |", "|---|---|---|---|---|---|"]
for g, cods in GRUPOS:
    if g in ("Empregado(a), patrão ou chefe", "Policial", "Outro"):
        continue  # poucos casos: o modelo ajustado não é informativo
    col = "ag_" + str(abs(hash(g)) % 10**6); d[col] = (vit & d.V018.isin(cods)).astype(float)
    br_ = rp(d[col], d.lgb, d.het); a1 = poisson_lgb(col); a2 = poisson_lgb(col, ("civil",)); a3 = poisson_lgb(col, ("conjuge_mora",))
    L.append(f"| {g} | {br_[0]:.2f} ({br_[1]:.2f} a {br_[2]:.2f}) | {a1[0]:.2f} ({a1[1]:.2f} a {a1[2]:.2f}) | "
             f"{a2[0]:.2f} ({a2[1]:.2f} a {a2[2]:.2f}) | {a3[0]:.2f} ({a3[1]:.2f} a {a3[2]:.2f}) | {a1[3]} |".replace(".", ","))
    rows.append(["rp_ajustada_agressor", g, None, None, a1[0], a1[1], a1[2]])
    rows.append(["rp_ajustada_agressor_civil", g, None, None, a2[0], a2[1], a2[2]])
    rows.append(["rp_ajustada_agressor_conjuge", g, None, None, a3[0], a3[1], a3[2]])
    assert a1[3] == a2[3] == a3[3], (g, a1[3], a2[3], a3[3])  # o texto da seção diz que o n é o mesmo nas três
    AGR_COL[g] = col

# ---- 5. modo de preenchimento (crítica GRO-11) e fluxo da amostra (AST-08)
d["auto"] = (d.V00101 == "1").astype(float)
L += ["", "## 5. Quem preencheu o módulo de violência (V00101) e fluxo da amostra", ""]
for nome, m in (("próprio morador", d.V00101 == "1"), ("entrevistador", d.V00101 == "2")):
    sh = ci(d.lgb.astype(float), m & (d.lgb | d.het))[0]
    pl = ci(d.fisica, m & d.lgb); ph = ci(d.fisica, m & d.het); r = rp(d.fisica, m & d.lgb, m & d.het)
    L.append(f"- {nome}: n = {int(m.sum())}; LGB+ entre quem declarou het ou LGB+ = {pc(sh)}%; violência física LGB+ "
             f"{pc(pl[0])} ({faixa(max(pl[1], 0), pl[2])}), het {pc(ph[0])} ({faixa(max(ph[1], 0), ph[2])}); razão bruta "
             f"{r[0]:.2f} ({r[1]:.2f} a {r[2]:.2f}); n LGB+ = {int((m & d.lgb).sum())}".replace(".", ","))
    rows.append(["modo_" + ("auto" if "morador" in nome else "entrevistador"), "fisica_rp_bruta", ph[0], pl[0], r[0], r[1], r[2]])
ra = poisson_lgb("fisica", ("auto",))
L.append(f"- Razão ajustada com o modo de preenchimento no ajuste: {ra[0]:.2f} ({ra[1]:.2f} a {ra[2]:.2f}); n = {ra[3]}".replace(".", ","))
rows.append(["rp_ajustada_fisica", "o mesmo + modo de preenchimento", None, None, ra[0], ra[1], ra[2]])
ori = d.Y008.value_counts().to_dict()
L += ["", f"Fluxo: {len(d)} adultos responderam o módulo V; {int((d.lgb | d.het).sum())} declararam orientação heterossexual ou "
      f"LGB+ (fora: não sabe {ori.get('5', 0)}, recusou {ori.get('6', 0)}, sem resposta {int(d.Y008.isna().sum())}); "
      f"n analítico do ajuste = {poisson_lgb('fisica')[3]} (com faixa, instrução e região conhecidas)."]

# ---- 6. contagens não ponderadas por tipo de agressor (crítica AST-R2-03: esparsidade e critério de omissão do ajuste)
L += ["", "## 6. Vítimas na amostra (não ponderado) por tipo de agressor", "",
      "Critério de omissão do ajuste por tipo de agressor: menos de 10 vítimas LGB+ na categoria.", "",
      "| Agressor | Vítimas heterossexuais | Vítimas LGB+ |", "|---|---|---|"]
for g, cods in GRUPOS:
    nh = int((vit & d.het & d.V018.isin(cods)).sum()); nl = int((vit & d.lgb & d.V018.isin(cods)).sum())
    L.append(f"| {g} | {nh} | {nl} |")
    rows.append(["n_vitimas", g, nh, nl, None, None, None])

# ---- 7. convivência com cônjuge (proposta de revisão, 2026-10-30): "solteiro" é estado civil, não ausência de cônjuge em casa
L += ["", "## 7. Mora com cônjuge ou companheiro(a) no domicílio (C01001), por grupo e estado civil (ponderado)", ""]
for grp, nome in (("het", "heterossexuais"), ("lgb", "LGB+")):
    dom = d[grp] & d.conjuge_mora.notna()
    tot = ci(d.conjuge_mora, dom)
    sol = ci(d.conjuge_mora, dom & (d.civil == "solteiro"))
    L.append(f"- {nome}: moram com cônjuge {pc(tot[0])}% ({faixa(max(tot[1], 0), tot[2])}); entre os de estado civil solteiro, "
             f"{pc(sol[0])}% ({faixa(max(sol[1], 0), sol[2])}); n com resposta = {int(dom.sum())}")
    rows.append(["mora_conjuge", nome, tot[0], sol[0], None, tot[1], tot[2]])

# ---- 8. cor ou raça ignorada fora do ajuste (crítica AST-R2-02): no ajuste publicado, C009 = 9 fica na referência
ign = d.C009 == "9"
n_ign_h, n_ign_l = int((ign & d.het).sum()), int((ign & d.lgb).sum())
L += ["", "## 8. Razões ajustadas sem os adultos de cor ou raça ignorada", "",
      f"No ajuste do artigo, quem tem cor ou raça ignorada (C009 = 9) entra na categoria de referência, com os não negros: "
      f"{n_ign_h} heterossexuais e {n_ign_l} LGB+ na amostra. Aqui eles saem do ajuste.", "",
      "| Desfecho | Ajustada (como no artigo) | Ajustada sem cor ou raça ignorada | n sem cor ignorada |", "|---|---|---|---|"]
DESF = [("Violência física", "fisica"), ("Violência sexual", "sexual"), ("Violência psicológica", "psico"), ("Qualquer violência", "qualquer")]
DESF += [(f"Violência física por {g[0].lower() + g[1:]}", c) for g, c in AGR_COL.items()]
for nome, col in DESF:
    a0 = poisson_lgb(col); a9 = poisson_lgb(col, sem_cor_ignorada=True)
    L.append(f"| {nome} | {a0[0]:.2f} ({a0[1]:.2f} a {a0[2]:.2f}) | {a9[0]:.2f} ({a9[1]:.2f} a {a9[2]:.2f}) | {a9[3]} |".replace(".", ","))
    rows.append(["rp_ajustada_sem_cor_ignorada", nome, None, None, a9[0], a9[1], a9[2]])
L += ["", "Leitura: a diferença entre as duas colunas é o peso da regra de codificação da cor ou raça ignorada nas razões ajustadas."]

(OUT / "agressor_risco_pns2019.md").write_text("\n".join(L) + "\n", encoding="utf-8")
pd.DataFrame(rows, columns=["bloco", "rotulo", "het", "lgb", "medida", "ic_lo", "ic_hi"]).to_csv(OUT / "agressor_risco_pns2019.csv", index=False)
print("\n".join(L))
