#!/opt/homebrew/bin/python3.14
"""Efeito de desenho (deff) da PNS 2019 para violencia e orientacao sexual, e n necessario.

Rodar:  /opt/homebrew/bin/python3.14 -I deff_pns2019.py --micro <PNS_2019.txt> --layout <input_PNS_2019_utf8.txt> --out <pasta>
(o input oficial do IBGE esta em latin-1; a copia utf8 usada esta em fontes/q1-textointegral/F2/pns2019/; o script le com errors="replace", sem efeito nos nomes de variavel)
Dependencias: numpy, pandas (nada mais).

O que faz
1. Le os microdados de largura fixa (layout = input oficial do IBGE; colunas por posicao).
2. Restringe ao morador selecionado de 18+ que respondeu o modulo V (violencia): n = 88.531,
   o mesmo n de Vasconcelos et al. 2023 (Rev Bras Epidemiol), conferido abaixo.
3. Desenho: estrato = V0024 (574), UPA = UPA_PNS (8.027), peso = V00291 (morador selecionado, calibrado).
   Variancia por linearizacao de Taylor, estimador de "ultimo conglomerado" (UPA dentro do estrato,
   sem fpc; fracao amostral da UPA e desprezivel). Dominios por estimacao de subpopulacao (zerando fora do dominio).
4. Conferencia independente: jackknife de UPA (JKn) calculado sobre totais por UPA; precisa bater com Taylor.
5. deff = Var_complexa / Var_AAS, com Var_AAS = p(1-p)/n do dominio (convencao do `estat effects` do Stata).
   Decomposicao: deff_w (Kish, so peso) = n*sum(w^2)/(sum w)^2 ; deff_c = deff/deff_w (parte conglomerado/estratificacao);
   rho implicito = (deff_c-1)/(b-1), b = n do dominio / n de UPAs com o dominio.
6. n necessario para detectar variacao relativa entre duas rodadas independentes (alfa 5% bilateral, poder 80%),
   mesma formula de duas proporcoes do dossie (simulacao/sim_identificabilidade.py), multiplicada pelo deff do dominio.

Saidas em --out: deff_pns2019.csv, deff_regiao_lgb.csv, n_necessario.csv, mde.csv, n_regiao.csv, sogi_modo.csv, deff_bootstrap_lgb.csv, validacao.txt
NAO interpreta politicamente. Limites: ver README.md (secao de limites).
"""
import argparse, math, re, sys
from pathlib import Path
import numpy as np
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--micro", required=True)
ap.add_argument("--layout", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
OUT = Path(a.out); OUT.mkdir(parents=True, exist_ok=True)

# ---------- leitura ----------
pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
spec = {}
for l in Path(a.layout).read_text(encoding="utf8", errors="replace").splitlines():
    m = pat.match(l)
    if m:
        spec[m.group(2)] = (int(m.group(1)), int(m.group(3)))
V = ["V00201", "V00202", "V00203", "V00204", "V00205", "V01401", "V01402", "V01403", "V01404", "V01405",
     "V02701", "V02702", "V02801", "V02802"]
want = ["V0001", "V0024", "UPA_PNS", "V0006_PNS", "V0015", "V0025A", "V0026", "C006", "C008", "C009", "V001", "V00101", "Y008", "V00291"] + V
cs = [(spec[k][0] - 1, spec[k][0] - 1 + spec[k][1]) for k in want]
raw = pd.read_fwf(a.micro, colspecs=cs, names=want, header=None, dtype=str)
# denominadores de custo: domicilios distintos (UPA_PNS + V0006_PNS) por situacao da entrevista do domicilio
raw["dom"] = raw.UPA_PNS + "-" + raw.V0006_PNS
dom_tot = raw.groupby("dom").V0015.first()
DENOM = {
    "domicilios_na_amostra_arquivo": int(dom_tot.size),
    "domicilios_com_entrevista_realizada (V0015=1)": int((dom_tot == "01").sum()),
    "moradores_selecionados_15mais (V0025A=1)": int((raw.V0025A == "1").sum()),
    "adultos_18mais_com_modulo_V": int(raw.V001.notna().sum()),
    "domicilios_distintos_com_adulto_modulo_V": int(raw[raw.V001.notna()].dom.nunique()),
    "upas_distintas": int(raw.UPA_PNS.nunique()),
}
d = raw[raw.V001.notna()].copy()                      # morador selecionado 18+ (modulo V aplicado)
d["w"] = d.V00291.astype(float)
for k in V:
    d[k] = d[k].map({"1": 1.0, "2": 0.0})
# V28 (vida) so e perguntada a quem NAO disse sim em V27 (12m): ausente = ja respondeu sim em 12m => vida = 1
assert d[V[:12]].notna().all().all(), "modulo V (12m) com ausentes"
assert d[V[12:]].isna().sum().sum() == 2 * 672 and (d[V[12]].isna() == (d[V[10:12]].max(axis=1) == 1)).all()
d[V[12:]] = d[V[12:]].fillna(1.0)
d["psico"] = d[V[0:5]].max(axis=1)
d["fisica"] = d[V[5:10]].max(axis=1)
d["sexual12"] = d[V[10:12]].max(axis=1)
d["sexual_vida"] = d[V[12:14]].max(axis=1)
d["qualquer"] = d[["psico", "fisica", "sexual12"]].max(axis=1)
d["lgb"] = d.Y008.isin(["2", "3", "4"]).astype(float)
d["het"] = (d.Y008 == "1").astype(float)
d["sogi_nresp"] = d.Y008.isin(["5", "6"]).astype(float)
d["mulher"] = (d.C006 == "2").astype(float)
d["homem"] = (d.C006 == "1").astype(float)
d["negro"] = d.C009.isin(["2", "4"]).astype(float)       # preta + parda
d["branco"] = (d.C009 == "1").astype(float)
d["mulher_negra"] = d.mulher * d.negro
d["homem_negro"] = d.homem * d.negro
d["priv_nao"] = (d.V001 == "2").astype(float)
d["entrev_preenche"] = (d.V00101 == "2").astype(float)
reg = {"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"}
d["regiao"] = d.V0001.str[0].map(reg)
d["h"] = d.V0024
d["c"] = d.UPA_PNS
assert len(d) == 88531, len(d)
Z975 = 1.959963984540054


# ---------- estimacao ----------
def psu_totals(dd, ycol, dom):
    """totais por UPA de w*dom*y e w*dom (so UPAs do dominio contribuem com valor; as demais entram com zero)."""
    t = pd.DataFrame({"h": d.h, "c": d.c, "num": d.w * dom * d[ycol], "den": d.w * dom})
    return t.groupby(["h", "c"], sort=False).sum().reset_index()


def estimate(ycol, domcol=None, dom_mask=None):
    dom = np.ones(len(d)) if domcol is None else d[domcol].to_numpy()
    if dom_mask is not None:
        dom = dom * dom_mask.to_numpy()
    t = psu_totals(d, ycol, dom)
    N, D = t.num.sum(), t.den.sum()
    p = N / D
    # Taylor: z_hc = (num_hc - p*den_hc)/D ; variancia ultimo conglomerado
    t["z"] = (t.num - p * t.den) / D
    g = t.groupby("h").z
    nh = g.transform("size"); zbar = g.transform("mean")
    ok = nh > 1
    var = (nh / (nh - 1) * (t.z - zbar) ** 2)[ok].sum()
    # jackknife JKn (conferencia): retira cada UPA c do estrato h
    Nh = t.groupby("h").num.transform("sum"); Dh = t.groupby("h").den.transform("sum")
    f = nh / (nh - 1)
    Nr = N - Nh + f * (Nh - t.num); Dr = D - Dh + f * (Dh - t.den)
    th = Nr / Dr
    vjk = ((nh - 1) / nh * (th - p) ** 2)[ok].sum()
    m = dom > 0
    n = int(m.sum()); w = d.w.to_numpy()[m]
    psu_dom = d.loc[m, ["h", "c"]].drop_duplicates()
    npsu = len(psu_dom)
    nstr = psu_dom.h.nunique()
    srs = p * (1 - p) / n if n else float("nan")
    deff = var / srs if srs and srs > 0 else float("nan")
    deffw = n * (w ** 2).sum() / w.sum() ** 2
    deffc = deff / deffw if deffw else float("nan")
    b = n / npsu if npsu else float("nan")
    rho = (deffc - 1) / (b - 1) if b >= 2 else float("nan")   # b<2: rho nao identificavel (quase 1 pessoa por UPA)
    df = max(npsu - nstr, 1)                              # gl de projeto do dominio (aprox.)
    lo = deff * df / _chi2_ppf(0.975, df); hi = deff * df / _chi2_ppf(0.025, df)
    return dict(est=p, se=math.sqrt(var), se_jk=math.sqrt(vjk), n=n, n_upa=npsu, n_estr=nstr, deff=deff,
                deft=math.sqrt(deff), deff_w=deffw, deff_c=deffc, b=b, rho=rho, deff_lo95=lo, deff_hi95=hi,
                cv=math.sqrt(var) / p if p else float("nan"))


def _chi2_ppf(q, df):
    """quantil da qui-quadrado por Wilson-Hilferty (aprox. boa para gl >= 30; suficiente p/ IC do deff)."""
    z = {0.975: 1.959963984540054, 0.025: -1.959963984540054}[q]
    return df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3


# ---------- tabela 1: deff por indicador x dominio ----------
IND = {"lgb": "prevalencia LGB+ (Y008 in 2,3,4; denom. todos)", "sogi_nresp": "nao resposta de orientacao (Y008 in 5,6)",
       "fisica": "violencia fisica 12m", "psico": "violencia psicologica 12m", "sexual12": "violencia sexual 12m",
       "sexual_vida": "violencia sexual na vida (V28, nao 12m)", "qualquer": "qualquer violencia 12m (psico/fisica/sexual)",
       "priv_nao": "privacidade NAO assegurada no modulo V", "entrev_preenche": "modulo V preenchido pelo entrevistador"}
DOM = {"adultos": None, "LGB+": "lgb", "heterossexual": "het", "mulher": "mulher", "homem": "homem",
       "negro (preta+parda)": "negro", "branco": "branco",
       "mulher negra": "mulher_negra", "homem negro": "homem_negro"}
rows = []
for ik, il in IND.items():
    for dn, dc in DOM.items():
        if ik == "lgb" and dn != "adultos":
            continue
        if ik == "sogi_nresp" and dn in ("LGB+", "heterossexual"):
            continue
        r = estimate(ik, dc)
        rows.append(dict(indicador=ik, descricao=il, dominio=dn, **r))
T1 = pd.DataFrame(rows)
T1.to_csv(OUT / "deff_pns2019.csv", index=False, float_format="%.6g")

# ---------- tabela 2: LGB+ por regiao ----------
rows = []
for rg in list(reg.values()) + ["Brasil"]:
    mk = None if rg == "Brasil" else (d.regiao == rg)
    pi = estimate("lgb", None, mk)
    for ik in ["fisica", "qualquer", "sexual12"]:
        r = estimate(ik, "lgb", mk)
        rows.append(dict(regiao=rg, indicador=ik, pi_lgb=pi["est"], pi_lgb_deff=pi["deff"], **r))
T2 = pd.DataFrame(rows)
T2.to_csv(OUT / "deff_regiao_lgb.csv", index=False, float_format="%.6g")



# ---------- incerteza do proprio deff: bootstrap de UPAs dentro dos estratos (B=500) ----------
def boot_deff(ycol, domcol, B=500, seed=20261021):
    dom = np.ones(len(d)) if domcol is None else d[domcol].to_numpy()
    t = pd.DataFrame({"h": d.h, "c": d.c, "num": d.w * dom * d[ycol], "den": d.w * dom, "cnt": dom, "w2": (d.w * dom) ** 2})
    t = t.groupby(["h", "c"], sort=True).sum().reset_index()
    hid = pd.factorize(t.h)[0]; nh = np.bincount(hid); start = np.concatenate([[0], np.cumsum(nh)[:-1]])
    rng = np.random.default_rng(seed)
    S = len(nh); num, den, cnt, w2 = (t[k].to_numpy() for k in ("num", "den", "cnt", "w2"))
    rep_start = np.repeat(start, nh); rep_n = np.repeat(nh, nh); rep_h = np.repeat(np.arange(S), nh)
    out = []
    for _ in range(B):
        idx = rep_start + np.floor(rng.random(len(rep_n)) * rep_n).astype(int)
        N, D, C, W2 = num[idx].sum(), den[idx].sum(), cnt[idx].sum(), w2[idx].sum()
        if D == 0 or C < 5: continue
        p = N / D
        z = (num[idx] - p * den[idx]) / D
        s1 = np.bincount(rep_h, z, S); s2 = np.bincount(rep_h, z * z, S)
        var = (nh / (nh - 1) * (s2 - s1 ** 2 / nh)).sum()
        out.append(var / (p * (1 - p) / C))
    return np.array(out)


rows = []
for ik, dn, dc in [("lgb", "adultos", None), ("fisica", "LGB+", "lgb"), ("qualquer", "LGB+", "lgb"), ("sexual12", "LGB+", "lgb"), ("psico", "LGB+", "lgb")]:
    b = boot_deff(ik, dc); pt = float(T1[(T1.indicador == ik) & (T1.dominio == dn)].iloc[0].deff)
    rows.append(dict(indicador=ik, dominio=dn, deff_ponto=pt, deff_boot_p2_5=np.percentile(b, 2.5), deff_boot_mediana=np.median(b), deff_boot_p97_5=np.percentile(b, 97.5), B=len(b)))
pd.DataFrame(rows).to_csv(OUT / "deff_bootstrap_lgb.csv", index=False, float_format="%.4g")
BOOT = pd.DataFrame(rows)

# ---------- n necessario ----------
def zq(p):  # quantil normal (Acklam nao e necessario: usa erfinv via numpy)
    from statistics import NormalDist
    return NormalDist().inv_cdf(p)


def n_duas_prop(p1, p2, alpha=0.05, power=0.8):
    za, zb = zq(1 - alpha / 2), zq(power)
    pb = (p1 + p2) / 2
    return ((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p1 - p2)) ** 2


rows = []
get = lambda ind, dom: T1[(T1.indicador == ind) & (T1.dominio == dom)].iloc[0]
pi_lgb = float(get("lgb", "adultos").est)
deff_pi = float(get("lgb", "adultos").deff)
for ik in ["fisica", "qualquer", "sexual12"]:
    g = get(ik, "LGB+")
    p1, deff = float(g.est), float(g.deff)
    deffc = float(g.deff_c)
    for delta in [0.10, 0.20, 0.30]:
        n_aas = n_duas_prop(p1, p1 * (1 + delta))
        n_lgb = n_aas * deff                              # entrevistas de LGB+ por rodada, com o desenho da PNS
        for k in [1, 5]:
            share = k * pi_lgb / (k * pi_lgb + 1 - pi_lgb)  # fracao de LGB+ na amostra com sobreamostra k
            rows.append(dict(indicador=ik, p_base=p1, mudanca_rel=delta, sobreamostra_k=k, deff_lgb=deff,
                             n_lgb_aas_por_rodada=math.ceil(n_aas), n_lgb_desenho_por_rodada=math.ceil(n_lgb), deff_c_lgb=deffc,
                             n_lgb_autoponderado_por_rodada=math.ceil(n_aas * deffc),
                             frac_lgb_amostra=share,
                             n_total_por_rodada=math.ceil(n_lgb / share),
                             n_total_duas_rodadas=2 * math.ceil(n_lgb / share),
                             n_total_autoponderado_por_rodada=math.ceil(n_aas * deffc / share),
                             n_total_AAS_ingenuo_por_rodada=math.ceil(n_aas / share)))
N = pd.DataFrame(rows)
N.to_csv(OUT / "n_necessario.csv", index=False, float_format="%.6g")


# ---------- variacao minima detectavel (MDE) por tamanho total de amostra, por rodada ----------
def mde(p1, n_eff, alpha=0.05, power=0.8):
    lo, hi = 1e-4, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        p2 = min(p1 * (1 + mid), 0.9999)
        if n_duas_prop(p1, p2, alpha, power) > n_eff: lo = mid
        else: hi = mid
    return hi


rows = []
for ik in ["fisica", "qualquer", "sexual12"]:
    g = get(ik, "LGB+"); p1 = float(g.est)
    for Ntot in [50_000, 88_531, 133_000, 200_000, 500_000]:
        for k in [1, 5]:
            share = k * pi_lgb / (k * pi_lgb + 1 - pi_lgb)
            nl = Ntot * share
            rows.append(dict(indicador=ik, N_total_por_rodada=Ntot, sobreamostra_k=k, n_lgb=round(nl),
                             mde_rel_deff_medido=mde(p1, nl / float(g.deff)),
                             mde_rel_autoponderado=mde(p1, nl / float(g.deff_c)),
                             mde_rel_AAS_ingenuo=mde(p1, nl)))
pd.DataFrame(rows).to_csv(OUT / "mde.csv", index=False, float_format="%.6g")
MDE = pd.DataFrame(rows)

# ---------- n por regiao (alvo: detectar a variacao DENTRO da regiao; baseline e deff nacionais de LGB+, pi regional) ----------
rows = []
for rg in reg.values():
    pi_r = float(T2[(T2.regiao == rg) & (T2.indicador == "fisica")].pi_lgb.iloc[0])
    n_lgb_r = int(T2[(T2.regiao == rg) & (T2.indicador == "fisica")].n.iloc[0])
    for ik in ["fisica", "qualquer"]:
        g = get(ik, "LGB+"); p1 = float(g.est)
        for delta in [0.10, 0.20, 0.30]:
            n_l = n_duas_prop(p1, p1 * (1 + delta)) * float(g.deff)
            for k in [1, 5]:
                sh = k * pi_r / (k * pi_r + 1 - pi_r)
                rows.append(dict(regiao=rg, pi_lgb_regional=pi_r, n_lgb_pns2019_na_regiao=n_lgb_r, indicador=ik,
                                 mudanca_rel=delta, sobreamostra_k=k, n_lgb_por_rodada=math.ceil(n_l),
                                 n_total_regiao_por_rodada=math.ceil(n_l / sh)))
pd.DataFrame(rows).to_csv(OUT / "n_regiao.csv", index=False, float_format="%.6g")

# ---------- SOGI: nao resposta e prevalencia LGB+ por modo de preenchimento / privacidade / idade ----------
d["faixa"] = pd.cut(d.C008.astype(int), [17, 29, 44, 59, 200], labels=["18-29", "30-44", "45-59", "60+"])
rows = []
for modo, mk in [("modulo V preenchido pelo proprio morador", d.V00101 == "1"), ("modulo V preenchido pelo entrevistador", d.V00101 == "2"),
                 ("privacidade assegurada", d.V001 == "1"), ("privacidade NAO assegurada", d.V001 == "2")]:
    for fx in [None] + list(d.faixa.cat.categories):
        m = mk if fx is None else (mk & (d.faixa == fx))
        for ik in ["lgb", "sogi_nresp", "fisica", "psico", "sexual12", "qualquer"]:
            r = estimate(ik, None, m)
            rows.append(dict(modo=modo, faixa_idade=fx or "18+", indicador=ik, **{k: r[k] for k in ["est", "se", "n", "deff"]}))
pd.DataFrame(rows).to_csv(OUT / "sogi_modo.csv", index=False, float_format="%.6g")

# ---------- validacao ----------
v = []
v.append(f"n adultos 18+ com modulo V = {len(d)} ; UPAs = {d.c.nunique()} ; estratos = {d.h.nunique()} ; soma pesos = {d.w.sum():.0f}")
# IC95% publicados (Stata svy, IC por logit) para conferir a VARIANCIA (nao so a estimativa pontual)
chk = [("lgb", "adultos", 0.0189, (0.0173, 0.0207), "Vasconcelos 2023, Tab.1 (1,89%; IC 1,73-2,07)"),
       ("fisica", "LGB+", 0.1470, (0.1116, 0.1912), "Vasconcelos 2023 (14,70%; IC 11,16-19,12)"),
       ("fisica", "heterossexual", 0.0382, (0.0357, 0.0409), "Vasconcelos 2023 (3,82%; IC 3,57-4,09)"),
       ("sexual12", "LGB+", 0.0486, (0.0321, 0.0728), "Vasconcelos 2023 (4,86%; IC 3,21-7,28)"),
       ("sexual12", "heterossexual", 0.0068, (0.0056, 0.0082), "Vasconcelos 2023 (0,68%; IC 0,56-0,82)"),
       ("qualquer", "LGB+", 0.4163, (0.3714, 0.4627), "Vasconcelos 2023 (41,63%; IC 37,14-46,27)"),
       ("qualquer", "heterossexual", 0.1761, (0.1708, 0.1816), "Vasconcelos 2023 (17,61%; IC 17,08-18,16)")]
for ik, dn, ref, ci, src in chk:
    r = get(ik, dn)
    lg = math.log(r.est / (1 - r.est)); sl = r.se / (r.est * (1 - r.est))
    lo, hi = 1 / (1 + math.exp(-(lg - Z975 * sl))), 1 / (1 + math.exp(-(lg + Z975 * sl)))
    v.append(f"{ik:9s} {dn:14s} meu={100*r.est:6.2f}% [IC logit {100*lo:5.2f}-{100*hi:5.2f}]  publicado={100*ref:6.2f}% [{100*ci[0]:5.2f}-{100*ci[1]:5.2f}]  dif ponto={100*(r.est-ref):+.2f} pp  [{src}]")
mx = float(np.nanmax(np.abs(T1.se / T1.se_jk - 1)))
v.append(f"Taylor x jackknife JKn (SE): maior diferenca relativa em {len(T1)} linhas = {100*mx:.3f}%")
mx2 = float(np.nanmax(np.abs(T2.se / T2.se_jk - 1)))
v.append(f"Taylor x jackknife JKn (SE) tabela regiao: maior diferenca relativa = {100*mx2:.3f}%")
v += ["DENOMINADORES (microdado, contagem de linhas distintas):"] + [f"  {k} = {x}" for k, x in DENOM.items()]
(OUT / "validacao.txt").write_text("\n".join(v) + "\n")
print("\n".join(v))
pd.set_option("display.width", 250, "display.max_columns", 30)
print(T1[["indicador", "dominio", "n", "n_upa", "est", "se", "deff", "deff_w", "deff_c", "rho", "deff_lo95", "deff_hi95"]].round(4).to_string())
print(T2[["regiao", "indicador", "n", "n_upa", "est", "deff", "pi_lgb", "pi_lgb_deff"]].round(4).to_string())
print(N.round(4).to_string())
print(BOOT.round(3).to_string())
print(MDE.round(3).to_string())
