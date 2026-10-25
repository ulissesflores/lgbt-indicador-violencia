"""C05 (TRIAGEM, rodada 3) — PNS 2019: estimativa DIRETA de P(LGB+ | violência física em 12 meses, adulto 18+), com desenho amostral complexo,
no lugar do Monte Carlo sobre marginais publicadas (triangulacao_pns_sinan.md, que assume insumos independentes).
Critérios de decisão escritos ANTES de rodar: research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md (hash em CRITERIOS.sha256).
Método: razão de totais ponderados R = soma(w x LGB+ x física) / soma(w x física), w = V00291 (peso calibrado), estrato V0024, UPA = V0024 + UPA_PNS; módulo V (n = 88.531, mesmo universo do seguro_pns2019.py).
  Variância (1) linearização de Taylor de último conglomerado (funções copiadas do seguro_pns2019.py, que não é alterado) e (2) jackknife JKn por UPA dentro do estrato (estratos com 1 UPA saltados; reponderação n_h/(n_h-1)).
  IC95% de desenho = R ± 1,96 EP (Wald, como no seguro_pns2019.py) e, ao lado, IC por logit (para checar se o veredito depende da forma).
  Bases: (a) TODOS os adultos vítimas (denominador inclui quem respondeu "não sabe/recusou" em Y008); (b) só quem declarou hetero ou LGB+ (comparável ao Sinan, parcela entre orientação válida).
  Cortes: total, 18-29, 30-44, 45+, homens, mulheres. LGB+ = Y008 em {2,3,4}; hetero = 1. Violência física = V01401-05 (qualquer "sim" em 12 meses).
Reprodução obrigatória (aborta): prevalências do artigo (14,70/3,82/41,63/17,61/4,86/0,68, tolerância 0,05 p.p.), RP bruta 3,84 [2,92; 5,06], 442 mil vítimas LGB+, e os pontos do Monte Carlo (6,90% e 7,13%) a partir dos insumos publicados.
LIMITES: (1) a base (a) NÃO é o cenário B do Monte Carlo: o cenário B imputou aos não-LGB+ a taxa dos heterossexuais; (a) só conta LGB+ declarados sobre todas as vítimas, e as duas coisas não são equivalentes;
  (2) n bruto de LGB+ vítimas é pequeno (179 no total; dezenas nos cortes): ICs largos, cortes descritivos, sem multiplicidade corrigida; (3) uma onda, autorrelato de orientação (subestima LGB+), sem motivo do agressor;
  (4) mesmo que o IC contenha 4,1%, o Sinan é registro de quem buscou serviço de saúde (24% sem orientação preenchida; limites 3,1% a 27,4%), não amostra: a comparação não é de estimadores equivalentes;
  (5) a razão de totais cobre vítimas de violência física de qualquer autor e local; o Sinan cobre violência física interpessoal notificada (definições próximas, não idênticas).
Rodar: /opt/homebrew/bin/python3.14 -I dados/pns/pns_c05_razao_direta.py   Saídas: dados/pns/c05_razao_direta.md e c05_razao_direta.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, math, re
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(REPO_ROOT)
P = BASE / "fontes/q1-textointegral/F2/pns2019"
MICRO = P / "x/PNS_2019.txt"; LAYOUT = P / "input_PNS_2019_utf8.txt"
OUT = BASE / "dados/pns"

pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
spec = {m.group(2): (int(m.group(1)), int(m.group(3))) for l in LAYOUT.read_text(encoding="utf8", errors="replace").splitlines() if (m := pat.match(l))}
V12 = ["V00201", "V00202", "V00203", "V00204", "V00205", "V01401", "V01402", "V01403", "V01404", "V01405", "V02701", "V02702"]
want = ["V0001", "V0024", "UPA_PNS", "C006", "C008", "Y008", "V00291", "V001"] + V12
raw = pd.read_fwf(MICRO, colspecs=[(spec[k][0] - 1, spec[k][0] - 1 + spec[k][1]) for k in want], names=want, header=None, dtype=str)
d = raw[raw.V001.notna()].copy()
assert len(d) == 88531, len(d)
d["w"] = d.V00291.astype(float)
for k in V12: d[k] = d[k].map({"1": 1.0, "2": 0.0})
d["psico"] = d[V12[0:5]].max(axis=1); d["fisica"] = d[V12[5:10]].max(axis=1); d["sexual"] = d[V12[10:12]].max(axis=1)
d["qualquer"] = d[["psico", "fisica", "sexual"]].max(axis=1)
d["lgb"] = d.Y008.isin(["2", "3", "4"]); d["het"] = d.Y008 == "1"
d["mulher"] = d.C006 == "2"; d["homem"] = d.C006 == "1"
age = d.C008.astype(float)
w = d.w.values
strat = d.V0024.values; psu = (d.V0024 + "-" + d.UPA_PNS).values
cod_psu = pd.factorize(psu)[0]; cod_str = pd.factorize(strat)[0]
psu_str = pd.Series(cod_str).groupby(cod_psu).first().values
n_psu_str = pd.Series(psu_str).value_counts()
NP = cod_psu.max() + 1


def var_from_u(u):
    u = u.reshape(len(u), -1)
    t = np.zeros((NP, u.shape[1])); np.add.at(t, cod_psu, u)
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


def ci_prop(y, dom):
    p, u = prop(y, dom); return p, math.sqrt(var_from_u(u)[0, 0])


def rp(y, dom1, dom2):
    p1, u1 = prop(y, dom1); p2, u2 = prop(y, dom2)
    se = math.sqrt(var_from_u(u1 / p1 - u2 / p2)[0, 0]); r = p1 / p2
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se)


# ---------- reprodução ----------
PUB = {("fisica", "lgb"): 14.70, ("fisica", "het"): 3.82, ("qualquer", "lgb"): 41.63, ("qualquer", "het"): 17.61, ("sexual", "lgb"): 4.86, ("sexual", "het"): 0.68}
for (o, g), v in PUB.items():
    p, _ = ci_prop(d[o], d[g]); assert abs(100 * p - v) <= 0.05, (o, g, p)
r_, lo_, hi_ = rp(d.fisica, d.lgb, d.het); assert abs(r_ - 3.84) < 0.006 and abs(lo_ - 2.92) < 0.006 and abs(hi_ - 5.06) < 0.006, (r_, lo_, hi_)
k442 = (w * d.lgb * d.fisica.fillna(0)).sum() / 1e3; assert abs(k442 - 442) < 1, k442
lgb_, fl_, fh_ = 0.0189, 0.147, 0.0382
mcB = 100 * lgb_ * fl_ / (lgb_ * fl_ + (1 - lgb_) * fh_); lgbA = 1.89 / (1.89 + 94.75); mcA = 100 * lgbA * fl_ / (lgbA * fl_ + (1 - lgbA) * fh_)
assert abs(mcB - 6.90) < 0.01 and abs(mcA - 7.13) < 0.01, (mcB, mcA)


# ---------- jackknife JKn ----------
def jackknife(num, den):
    """num, den: vetores por observação (w x indicadores). R = soma(num)/soma(den). Retorna R, EP_JKn."""
    tn = np.bincount(cod_psu, weights=num, minlength=NP); td = np.bincount(cod_psu, weights=den, minlength=NP)
    Tn, Td = tn.sum(), td.sum(); R = Tn / Td
    nh = np.array([n_psu_str[h] for h in psu_str], float)
    Tnh = np.bincount(psu_str, weights=tn, minlength=psu_str.max() + 1)[psu_str]; Tdh = np.bincount(psu_str, weights=td, minlength=psu_str.max() + 1)[psu_str]
    ok = nh >= 2
    Rhj = np.full(NP, np.nan)
    Rhj[ok] = (Tn - Tnh[ok] + nh[ok] / (nh[ok] - 1) * (Tnh[ok] - tn[ok])) / (Td - Tdh[ok] + nh[ok] / (nh[ok] - 1) * (Tdh[ok] - td[ok]))
    V = 0.0
    for h in np.unique(psu_str[ok]):
        sel = (psu_str == h) & ok; r = Rhj[sel]; n_h = sel.sum()
        V += (n_h - 1) / n_h * ((r - r.mean()) ** 2).sum()
    return R, math.sqrt(V)


vit = d.fisica == 1
base = {"(a) todos os adultos vítimas": vit, "(b) só hetero ou LGB+ (comparável ao Sinan)": vit & (d.lgb | d.het)}
cortes = {"total": d.lgb | ~d.lgb, "18-29": (age >= 18) & (age < 30), "30-44": (age >= 30) & (age < 45), "45+": age >= 45, "homens": d.homem, "mulheres": d.mulher}
rows = []
for bnome, bdom in base.items():
    for cnome, cdom in cortes.items():
        dom = bdom & cdom
        p, u = prop(d.lgb.astype(float), dom); se_t = math.sqrt(var_from_u(u)[0, 0])
        R, se_j = jackknife(w * dom.values * d.lgb.values, w * dom.values)
        assert abs(R - p) < 1e-12
        logit = math.log(p / (1 - p)); sel_ = se_t / (p * (1 - p))
        lg = (1 / (1 + math.exp(-(logit - 1.96 * sel_))), 1 / (1 + math.exp(-(logit + 1.96 * sel_))))
        rows.append(dict(base=bnome, corte=cnome, n_vit=int(dom.sum()), n_lgb=int((dom & d.lgb).sum()), R=100 * p, se_taylor=100 * se_t, se_jk=100 * se_j,
                         lo=100 * (p - 1.96 * se_t), hi=100 * (p + 1.96 * se_t), lo_jk=100 * (p - 1.96 * se_j), hi_jk=100 * (p + 1.96 * se_j), lo_logit=100 * lg[0], hi_logit=100 * lg[1]))
df = pd.DataFrame(rows)
df.to_csv(OUT / "c05_razao_direta.csv", index=False)

prim = df[(df.base.str.startswith("(b)")) & (df.corte == "total")].iloc[0]; prima = df[(df.base.str.startswith("(a)")) & (df.corte == "total")].iloc[0]
SINAN = {"2023": 4.12, "2024": 4.08}
def contem(r, v): return bool(r.lo <= v <= r.hi)
w_direto = prim.hi - prim.lo; w_mc = 9.32 - 5.43
se_ratio = max(prim.se_taylor, prim.se_jk) / min(prim.se_taylor, prim.se_jk)
L = ["# C05 — PNS 2019: P(LGB+ | violência física 12 m, 18+) estimada DIRETAMENTE no microdado (gerado por pns_c05_razao_direta.py)", "",
     "> [!NOTE]", "> Leia o cabeçalho do script (limites). Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. Taylor de último conglomerado + jackknife JKn por UPA; 574 estratos, 8.027 UPA.", "",
     "## 0. Reprodução (passou; senão o script aborta)", "",
     f"- Prevalências do artigo (14,70 / 3,82 / 41,63 / 17,61 / 4,86 / 0,68) dentro de 0,05 p.p.; RP bruta {r_:.2f} [{lo_:.2f}; {hi_:.2f}] (publicado 3,84 [2,92; 5,06]); vítimas LGB+ ≈ {k442:.0f} mil (publicado ≈ 442 mil).",
     f"- Pontos do Monte Carlo recalculados dos insumos publicados: cenário B {mcB:.2f}% (publicado 6,90%), cenário A {mcA:.2f}% (publicado 7,13%).", "",
     "## 1. Resultado: parcela LGB+ entre as vítimas de violência física (12 meses), adultos 18+", "",
     "| base | corte | n vítimas | n LGB+ | R (%) | EP Taylor | EP jackknife | IC95% de desenho (Taylor) | IC95% logit | IC95% (EP jackknife) |", "|---|---|---|---|---|---|---|---|---|---|"]
for _, r in df.iterrows():
    L.append(f"| {r.base} | {r.corte} | {r.n_vit} | {r.n_lgb} | {r.R:.2f} | {r.se_taylor:.2f} | {r.se_jk:.2f} | [{r.lo:.2f}; {r.hi:.2f}] | [{r.lo_logit:.2f}; {r.hi_logit:.2f}] | [{r.lo_jk:.2f}; {r.hi_jk:.2f}] |")
L += ["", "## 2. Comparação com o Monte Carlo e com o Sinan (teste primário: base (b), total)", "",
      f"- Direto, base (b), total: **{prim.R:.2f}%**, IC95% de desenho [{prim.lo:.2f}; {prim.hi:.2f}] (largura {w_direto:.2f} p.p.); Monte Carlo cenário A: 7,13% [5,43; 9,32] (largura {w_mc:.2f}); razão de larguras direto/MC = {w_direto/w_mc:.2f}.",
      f"- Base (a), total: {prima.R:.2f}% [{prima.lo:.2f}; {prima.hi:.2f}] (Monte Carlo cenário B: 6,90% [5,25; 9,03]; as duas NÃO são o mesmo estimando: ver limite 1).",
      f"- Sinan 2023 = 4,12% está {'DENTRO' if contem(prim, 4.12) else 'FORA'} do IC de desenho (b, total); Sinan 2024 = 4,08% está {'DENTRO' if contem(prim, 4.08) else 'FORA'}. Com IC logit [{prim.lo_logit:.2f}; {prim.hi_logit:.2f}]: 4,12% {'dentro' if prim.lo_logit <= 4.12 <= prim.hi_logit else 'fora'}, 4,08% {'dentro' if prim.lo_logit <= 4.08 <= prim.hi_logit else 'fora'}; com EP jackknife [{prim.lo_jk:.2f}; {prim.hi_jk:.2f}]: 4,12% {'dentro' if prim.lo_jk <= 4.12 <= prim.hi_jk else 'fora'}, 4,08% {'dentro' if prim.lo_jk <= 4.08 <= prim.hi_jk else 'fora'}.",
      f"- Razão entre EP Taylor e EP jackknife (maior/menor, base (b) total): {se_ratio:.2f}.",
      f"- Distância do Sinan ao ponto: {prim.R/4.10:.2f}x (ponto da PNS / 4,10); em EPs: {(prim.R-4.12)/prim.se_taylor:.2f} (2023) e {(prim.R-4.08)/prim.se_taylor:.2f} (2024).", ""]
(OUT / "c05_razao_direta.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
