"""Violência segundo a orientação sexual, PNS 2019 (microdados oficiais do IBGE), com desenho amostral complexo: "é seguro ser LGB+ no Brasil? quanto, onde, quem, por quê?"
Responde, com o que a PNS permite, à pergunta de pesquisa do autor (ponto 5 da lista de verificação). SEM pesquisa de campo: só o microdado público.
Método (declarado antes de rodar; todas as comparações por subgrupo são REPORTADAS, não só as significativas; análise exploratória, sem correção de multiplicidade):
  - População: morador selecionado de 18+ que respondeu o módulo V (violência) = 88.531 (mesmo n de Vasconcelos et al. 2023). Estrato V0024, UPA UPA_PNS, peso V00291 (calibrado).
  - Desfechos (12 meses): psicológica (V00201-05), física (V01401-05), sexual (V02701-02), qualquer. 'LGB+' = Y008 em {2 bissexual, 3 homossexual, 4 outra}; heterossexual = 1; não sabe/recusou ficam fora das comparações.
  - Estimação: proporção ponderada por domínio; variância por linearização de Taylor (estimador de último conglomerado: UPA dentro do estrato); diferença, razão de prevalências (RP, delta no log) e RP AJUSTADA por regressão de Poisson ponderada com variância robusta de desenho
    (ajuste: sexo, faixa etária, cor, instrução, região, situação urbana/rural).
  - Reprodução obrigatória antes de qualquer resultado novo: prevalências e ICs publicados por Vasconcelos et al. 2023 (Tabela 2) em tolerância de 0,05 p.p.
  - 'Onde/quem' (V006/V007, V018/V019, V032/V033) referem-se ao episódio mais grave e só existem entre as vítimas.
LIMITES: uma única onda (2019): NÃO há "quando"/tendência; autorrelato de orientação sexual em survey domiciliar (subestima LGB+ por estigma e revelação); LGB+ ~1,9% => n pequeno por região; violência não letal (não responde à pergunta sobre homicídio, que o SIM não registra por orientação);
o módulo não pergunta o MOTIVO ("por quê") do agressor: só quem e onde.
Rodar: /opt/homebrew/bin/python3.14 -I dados/pns/seguro_pns2019.py   Saídas: dados/pns/seguro_pns2019.md e .csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import math, re, sys
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(REPO_ROOT)
P = BASE / "fontes/q1-textointegral/F2/pns2019"
MICRO = P / "x/PNS_2019.txt"; LAYOUT = P / "input_PNS_2019_utf8.txt"
OUT = BASE / "dados/pns"; OUT.mkdir(exist_ok=True)

pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
spec = {m.group(2): (int(m.group(1)), int(m.group(3))) for l in LAYOUT.read_text(encoding="utf8", errors="replace").splitlines() if (m := pat.match(l))}
V12 = ["V00201", "V00202", "V00203", "V00204", "V00205", "V01401", "V01402", "V01403", "V01404", "V01405", "V02701", "V02702"]
want = ["V0001", "V0024", "UPA_PNS", "V0026", "C006", "C008", "C009", "VDD004A", "Y008", "V00291", "V001"] + V12 + ["V018", "V019"]
raw = pd.read_fwf(MICRO, colspecs=[(spec[k][0] - 1, spec[k][0] - 1 + spec[k][1]) for k in want], names=want, header=None, dtype=str)
d = raw[raw.V001.notna()].copy()
assert len(d) == 88531, len(d)
d["w"] = d.V00291.astype(float)
for k in V12: d[k] = d[k].map({"1": 1.0, "2": 0.0})
d["psico"] = d[V12[0:5]].max(axis=1); d["fisica"] = d[V12[5:10]].max(axis=1); d["sexual"] = d[V12[10:12]].max(axis=1)
d["qualquer"] = d[["psico", "fisica", "sexual"]].max(axis=1)
d["lgb"] = d.Y008.isin(["2", "3", "4"]); d["het"] = d.Y008 == "1"; d["homo"] = d.Y008 == "3"; d["bi"] = d.Y008 == "2"
d["mulher"] = d.C006 == "2"; d["homem"] = d.C006 == "1"
d["negro"] = d.C009.isin(["2", "4"]); d["naonegro"] = d.C009.isin(["1", "3", "5"])
age = d.C008.astype(float); d["faixa"] = pd.cut(age, [17, 29, 44, 59, 200], labels=["18-29", "30-44", "45-59", "60+"])
d["regiao"] = d.V0001.str[0].map({"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"})
d["urbano"] = d.V0026 == "1"
d["instr"] = d.VDD004A.map({"1": "baixa", "2": "baixa", "3": "média", "4": "média", "5": "média", "6": "alta", "7": "alta"})
strat = d.V0024.values; psu = (d.V0024 + "-" + d.UPA_PNS).values
w = d.w.values
cod_psu = pd.factorize(psu)[0]; cod_str = pd.factorize(strat)[0]
psu_str = pd.Series(cod_str).groupby(cod_psu).first().values  # estrato de cada UPA
n_psu_str = pd.Series(psu_str).value_counts()


def var_from_u(u):
    """variância (último conglomerado) de um estimador com função de influência u (vetor por observação). u: n x k -> matriz k x k."""
    u = u.reshape(len(u), -1)
    t = np.zeros((cod_psu.max() + 1, u.shape[1])); np.add.at(t, cod_psu, u)
    V = np.zeros((u.shape[1], u.shape[1]))
    for h, n_h in n_psu_str.items():
        if n_h < 2: continue
        th = t[psu_str == h]; c = th - th.mean(axis=0)
        V += n_h / (n_h - 1) * (c.T @ c)
    return V


def prop(y, dom):
    """proporção ponderada no domínio; devolve p, função de influência."""
    dd = dom.values.astype(float); yy = np.nan_to_num(y.values.astype(float))
    W = (w * dd).sum(); p = (w * dd * yy).sum() / W
    return p, w * dd * (yy - p) / W


def ci_prop(y, dom):
    p, u = prop(y, dom); se = math.sqrt(var_from_u(u)[0, 0]); return p, se


def fmt(p, se): return f"{100*p:.2f}% [{100*max(p-1.96*se,0):.2f}; {100*(p+1.96*se):.2f}]"


def rp(y, dom1, dom2):
    p1, u1 = prop(y, dom1); p2, u2 = prop(y, dom2)
    if p1 <= 0 or p2 <= 0: return None
    se = math.sqrt(var_from_u(u1 / p1 - u2 / p2)[0, 0]); r = p1 / p2
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se)


def dif(y, dom1, dom2):
    p1, u1 = prop(y, dom1); p2, u2 = prop(y, dom2); se = math.sqrt(var_from_u(u1 - u2)[0, 0]); return p1 - p2, se


def poisson_rp(y, X, names, alvo):
    """Poisson ponderado (log-link) com variância robusta de desenho; devolve RP e IC da variável alvo."""
    yy = np.nan_to_num(y.values.astype(float)); b = np.zeros(X.shape[1]); b[0] = math.log(max(yy.mean(), 1e-6))
    for _ in range(50):
        mu = np.exp(X @ b); W = w * mu; z = X @ b + (yy - mu) / mu
        nb = np.linalg.solve((X * W[:, None]).T @ X, (X * W[:, None]).T @ z)
        if np.max(np.abs(nb - b)) < 1e-9: b = nb; break
        b = nb
    mu = np.exp(X @ b); bread = np.linalg.inv((X * (w * mu)[:, None]).T @ X)
    s = X * (w * (yy - mu))[:, None]; V = bread @ var_from_u(s) @ bread
    j = names.index(alvo); se = math.sqrt(V[j, j]); return math.exp(b[j]), math.exp(b[j] - 1.96 * se), math.exp(b[j] + 1.96 * se)


rows = []; L = ["# Violência segundo a orientação sexual, PNS 2019 (gerado por seguro_pns2019.py)", "",
                "Desenho complexo (574 estratos, 8.027 UPA, peso calibrado). IC95% entre colchetes. LEIA os limites no cabeçalho do script: uma onda, autorrelato, sem motivo do agressor, sem homicídio. ICs de Wald linear (os do artigo de Vasconcelos usam transformação logit: os pontos coincidem, os limites diferem pouco, mais perto de 0/100%). Com n de LGB+ de 88 a 916 por subgrupo, as diferenças ENTRE subgrupos (regiões, idades) têm ICs sobrepostos: NÃO sustentam ranking de regiões nem de faixas."]
OUTC = [("fisica", "física"), ("sexual", "sexual"), ("psico", "psicológica"), ("qualquer", "qualquer")]

# ---- validação contra Vasconcelos et al. 2023 (Tabela 2)
L += ["", "## 0. Reprodução do artigo publicado (Vasconcelos et al. 2023, Tabela 2; tolerância 0,05 p.p.)", "", "| desfecho | grupo | publicado | recalculado | confere |", "|---|---|---|---|---|"]
PUB = {("fisica", "lgb"): 14.70, ("fisica", "het"): 3.82, ("qualquer", "lgb"): 41.63, ("qualquer", "het"): 17.61, ("sexual", "lgb"): 4.86, ("sexual", "het"): 0.68}
falhas = 0
for (o, g), v in PUB.items():
    p, se = ci_prop(d[o], d[g]); ok = abs(100 * p - v) <= 0.05; falhas += (not ok)
    L.append(f"| {o} | {g} | {v:.2f}% | {100*p:.2f}% | {'sim' if ok else '**NÃO**'} |")
L.append(f"\nDivergências: {falhas}.")
assert falhas == 0, "reprodução falhou"

# ---- 1. nível
L += ["", "## 1. Prevalência em 12 meses, por orientação sexual (adultos 18+)", "", "| desfecho | heterossexual | LGB+ | homossexual | bissexual | RP LGB+/het [IC] | diferença LGB+ - het (p.p.) |", "|---|---|---|---|---|---|---|"]
for o, nome in OUTC:
    c = {g: ci_prop(d[o], d[g]) for g in ("het", "lgb", "homo", "bi")}; r = rp(d[o], d.lgb, d.het); df = dif(d[o], d.lgb, d.het)
    L.append(f"| {nome} | {fmt(*c['het'])} | {fmt(*c['lgb'])} | {fmt(*c['homo'])} | {fmt(*c['bi'])} | {r[0]:.2f} [{r[1]:.2f}; {r[2]:.2f}] | {100*df[0]:+.1f} [{100*(df[0]-1.96*df[1]):+.1f}; {100*(df[0]+1.96*df[1]):+.1f}] |")
    rows.append(["nivel", nome, "LGB+", c["lgb"][0], c["het"][0], r[0], r[1], r[2]])
adultos = (w * d.lgb).sum(); L += ["", f"Escala (peso calibrado à população): LGB+ ≈ {adultos/1e6:.2f} milhões de adultos; vítimas de violência física em 12 meses entre LGB+ ≈ {(w*d.lgb*d.fisica.fillna(0)).sum()/1e3:.0f} mil (IC95% ≈ ±{1.96*math.sqrt(var_from_u(w*d.lgb.values*np.nan_to_num(d.fisica.values.astype(float)))[0,0])/1e3:.0f} mil)."]

# ---- 2. por sexo, cor, idade, instrução, região, urbano
L += ["", "## 2. Violência FÍSICA (12 meses): LGB+ x heterossexual por subgrupo (RP e diferença; n LGB+ no subgrupo)", "", "| subgrupo | n LGB+ | het | LGB+ | RP [IC95%] | diferença p.p. |", "|---|---|---|---|---|---|"]
SUB = [("Homens", d.homem), ("Mulheres", d.mulher), ("Negros (pretos+pardos)", d.negro), ("Não negros", d.naonegro)] + \
      [(f"Idade {k}", d.faixa == k) for k in ("18-29", "30-44", "45-59", "60+")] + [(f"Instrução {k}", d.instr == k) for k in ("baixa", "média", "alta")] + \
      [(f"Região {k}", d.regiao == k) for k in ("Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste")] + [("Urbano", d.urbano), ("Rural", ~d.urbano)]
for nome, m in SUB:
    nl = int((d.lgb & m).sum()); a = ci_prop(d.fisica, d.het & m); b = ci_prop(d.fisica, d.lgb & m); r = rp(d.fisica, d.lgb & m, d.het & m); df = dif(d.fisica, d.lgb & m, d.het & m)
    L.append(f"| {nome} | {nl} | {fmt(*a)} | {fmt(*b)} | " + (f"{r[0]:.2f} [{r[1]:.2f}; {r[2]:.2f}]" if r else "n/d") + f" | {100*df[0]:+.1f} |")
    rows.append(["subgrupo", nome, "LGB+", b[0], a[0], r[0] if r else None, r[1] if r else None, r[2] if r else None])

# ---- 3. RP ajustada
L += ["", "## 3. Razão de prevalências AJUSTADA (Poisson ponderado, variância robusta de desenho): LGB+ x heterossexual", "", "Ajuste: sexo, faixa etária, cor, instrução, região, urbano/rural. Amostra: LGB+ e heterossexuais.", "", "| desfecho | RP bruta | RP ajustada [IC95%] |", "|---|---|---|"]
sel = d.lgb | d.het; ds = d[sel]
X = [np.ones(len(ds)), ds.lgb.values.astype(float), ds.mulher.values.astype(float)]; nm = ["const", "lgb", "mulher"]
for k in ("30-44", "45-59", "60+"): X.append((ds.faixa == k).values.astype(float)); nm.append("f" + k)
X.append(ds.negro.values.astype(float)); nm.append("negro")
for k in ("média", "alta"): X.append((ds.instr == k).values.astype(float)); nm.append("i" + k)
for k in ("Nordeste", "Sudeste", "Sul", "Centro-Oeste"): X.append((ds.regiao == k).values.astype(float)); nm.append("r" + k)
X.append(ds.urbano.values.astype(float)); nm.append("urbano"); X = np.column_stack(X)
completos = ~np.isnan(X).any(axis=1)
_w_full = w; w = ds.w.values  # variância usa o vetor completo: reindexa abaixo
# reconstrói influências no vetor completo (UPA/estrato do d inteiro) preenchendo zeros fora da amostra de análise
idx = np.where(sel.values & ~pd.isna(d.faixa).values & d.instr.notna().values & d.regiao.notna().values)[0]
dd_ = d.iloc[idx]; Xf = []
for col in nm:
    if col == "const": Xf.append(np.ones(len(dd_)))
    elif col == "lgb": Xf.append(dd_.lgb.values.astype(float))
    elif col == "mulher": Xf.append(dd_.mulher.values.astype(float))
    elif col.startswith("f"): Xf.append((dd_.faixa == col[1:]).values.astype(float))
    elif col == "negro": Xf.append(dd_.negro.values.astype(float))
    elif col.startswith("i"): Xf.append((dd_.instr == col[1:]).values.astype(float))
    elif col.startswith("r"): Xf.append((dd_.regiao == col[1:]).values.astype(float))
    elif col == "urbano": Xf.append(dd_.urbano.values.astype(float))
Xf = np.column_stack(Xf)
w = _w_full
_cp, _cs = cod_psu, cod_str


def poisson_full(yname):
    y = np.nan_to_num(d[yname].values.astype(float)); yy = y[idx]; ww = w[idx]
    b = np.zeros(Xf.shape[1]); b[0] = math.log(max(yy.mean(), 1e-6))
    for _ in range(60):
        mu = np.exp(Xf @ b); W = ww * mu; z = Xf @ b + (yy - mu) / mu
        nb = np.linalg.solve((Xf * W[:, None]).T @ Xf, (Xf * W[:, None]).T @ z)
        if np.max(np.abs(nb - b)) < 1e-10: b = nb; break
        b = nb
    mu = np.exp(Xf @ b); bread = np.linalg.inv((Xf * (ww * mu)[:, None]).T @ Xf)
    s_full = np.zeros((len(d), Xf.shape[1])); s_full[idx] = Xf * (ww * (yy - mu))[:, None]
    V = bread @ var_from_u(s_full) @ bread; j = nm.index("lgb"); se = math.sqrt(V[j, j])
    return math.exp(b[j]), math.exp(b[j] - 1.96 * se), math.exp(b[j] + 1.96 * se)


for o, nome in OUTC:
    br = rp(d[o], d.lgb, d.het); aj = poisson_full(o)
    L.append(f"| {nome} | {br[0]:.2f} | {aj[0]:.2f} [{aj[1]:.2f}; {aj[2]:.2f}] |"); rows.append(["rp_ajustada", nome, "LGB+", None, None, aj[0], aj[1], aj[2]])

# ---- 4. quem e onde (episódio mais grave de violência física)
L += ["", "## 4. Entre as VÍTIMAS de violência física em 12 meses: quem agrediu e onde (episódio mais grave; V018/V019)", "", "| categoria | heterossexuais | LGB+ |", "|---|---|---|"]
QUEM = {"01": "Cônjuge/companheiro(a)", "02": "Ex-cônjuge/ex-companheiro(a)", "03": "Parceiro(a)/namorado(a)/ex", "04": "Pai/mãe/padrasto/madrasta", "05": "Filho(a)/enteado(a)", "06": "Irmão(ã)", "07": "Outro parente",
        "08": "Amigo(a)/colega/vizinho(a)", "09": "Empregado(a)", "10": "Patrão/chefe", "11": "Pessoa desconhecida", "12": "Policial", "13": "Outro"}
ONDE = {"1": "Domicílio", "2": "Trabalho", "3": "Escola/faculdade", "4": "Bar/restaurante", "5": "Via pública/local público", "6": "Outro"}
vit = d.fisica == 1
for nome_var, mapa, col in (("QUEM (V018)", QUEM, "V018"), ("ONDE (V019)", ONDE, "V019")):
    L.append(f"| **{nome_var}** | n het = {int((vit & d.het).sum())} | n LGB+ = {int((vit & d.lgb).sum())} |")
    for cod, nome in mapa.items():
        y = (d[col] == cod).astype(float)
        a = ci_prop(y, vit & d.het); b = ci_prop(y, vit & d.lgb)
        if b[0] > 0 or a[0] > 0.02: L.append(f"| {nome} | {fmt(*a)} | {fmt(*b)} |")
    # cônjuge+ex+parceiro agregado
L.append("")
parc = d.V018.isin(["01", "02", "03"]).astype(float); fam = d.V018.isin(["04", "05", "06", "07"]).astype(float)
for nome, y in (("parceiro ou ex (cônjuge, ex, namorado)", parc), ("família (pai/mãe/filho/irmão/outro parente)", fam)):
    a = ci_prop(y, vit & d.het); b = ci_prop(y, vit & d.lgb); r = rp(y, vit & d.lgb, vit & d.het)
    L.append(f"- Agressor = {nome}: heterossexuais {fmt(*a)}; LGB+ {fmt(*b)}" + (f"; RP {r[0]:.2f} [{r[1]:.2f}; {r[2]:.2f}]" if r else ""))
L += ["", "Leitura: a PNS NÃO pergunta o motivo do agressor. 'Por quê' só pode ser lido como associação (quem agride, onde, perfil), nunca como motivação por orientação (N4 do dossiê).", ""]
(OUT / "seguro_pns2019.md").write_text("\n".join(L) + "\n", encoding="utf-8")
pd.DataFrame(rows, columns=["bloco", "rotulo", "grupo", "prev_grupo", "prev_ref", "rp", "ic_lo", "ic_hi"]).to_csv(OUT / "seguro_pns2019.csv", index=False)
print("\n".join(L))
