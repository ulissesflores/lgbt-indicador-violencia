"""C09 — D1: série temporal interrompida NACIONAL (descritiva; PREREGISTRO-C09.md seção 5).
ln(taxa padronizada por idade) = a + b(t-2010) + soma_k [L_k 1(t>=T_k) + S_k (t-T_k) 1(t>=T_k)], T = 2016, 2019, 2023; 15 pontos 2010-2024; MQO; EP clássico; IC95% t(7).
Placebo pré-fixado: T = 2015, 2018, 2022. Mudança de nível "coincide com a troca" só se o IC da quebra exclui 0 E o placebo 1 ano antes NÃO exclui 0 com o mesmo sinal.
Séries: dados/sim/asr_brasil.csv (Brasil e 4 grupos sexo x raça; agressão e agressão+indet); arma de fogo (agressão, arma == 1) GERADA aqui com as funções de
dados/sim/padroniza_idade.py importadas sem alteração; razão indet/(agressão+indet) Brasil em p.p. das contagens brutas de dados/sim/sim_agressoes_agregado.csv.
Portas (abortam): recalcular com padroniza_idade as taxas de agressão e agressão+indet dos 5 grupos e bater asr_brasil.csv (0,005); contagem nacional de arma = soma das UFs no Atlas.
Rodar DEPOIS de c09_d2_painel.py: /opt/homebrew/bin/python3.14 -I c09_d1_its.py
Saídas: c09_d1_resultados.md, c09_d1_resultados.csv e c09_resultados.md (= cabeçalho + c09_d2_resultados.md + c09_d1_resultados.md)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import sys; sys.dont_write_bytecode = True   # não deixar __pycache__ nas pastas de dados/ ao importar módulos irmãos
import csv, importlib.util, math, collections, hashlib
import numpy as np
import pandas as pd
from scipy import stats

BASE = REPO_ROOT
AQUI = f"{BASE}/dados/presidencia"


def _imp(nome, arq):
    s = importlib.util.spec_from_file_location(nome, arq); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


pdz = _imp("padroniza", f"{BASE}/dados/sim/padroniza_idade.py")
est = _imp("c09est", f"{AQUI}/c09_estrutura.py")
ANOS = list(range(2010, 2025))
GR = ["Brasil", "Homens negros", "Homens não negros", "Mulheres negras", "Mulheres não negras"]

# ---------- porta: reproduzir asr_brasil.csv ----------
pub = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{BASE}/dados/sim/asr_brasil.csv", encoding="utf-8")): pub[(r["grupo"], r["desfecho"])][int(r["ano"])] = float(r["taxa_padronizada"])
m_ag, _ = pdz.redistribui(pdz.carrega_mortes(["agressao"])); m_ai, _ = pdz.redistribui(pdz.carrega_mortes(["agressao", "indet"]))
SER = {}
for g in GR:
    sx, rc = pdz.GRUPOS[g]
    for des, m in (("agressao", m_ag), ("agressao+indet", m_ai)):
        v = {a: pdz.asr(m, a, sx, rc)[0] for a in ANOS}
        assert all(abs(round(v[a], 2) - pub[(g, des)][a]) < 0.005 + 1e-9 for a in ANOS), (g, des)
        SER[(g, des)] = v
# ---------- arma de fogo (agressão, arma == 1) ----------
df = pd.read_csv(f"{BASE}/dados/sim/sim_agressoes_agregado.csv")
da = df[(df.grupo == "agressao") & (df.arma == 1)].copy()
da["faixa"] = da.faixa.map(lambda f: pdz.faixa17(f) if f != "ign" else "ign")
m_ar, _ = pdz.redistribui(da.groupby(["ano", "sexo", "raca", "faixa"], as_index=False).n.sum())
SER[("Brasil", "arma")] = {a: pdz.asr(m_ar, a, *pdz.GRUPOS["Brasil"])[0] for a in ANOS}
atl = collections.Counter()
for r in csv.DictReader(open(f"{BASE}/dados/atlas_uf_series.csv", encoding="utf-8")):
    if r["variavel"] == "homicidios_arma_fogo_n" and r["valor"] != "": atl[int(r["ano"])] += float(r["valor"])
n_arma = da.groupby("ano").n.sum().to_dict()
dif_arma = {a: n_arma[a] - atl[a] for a in ANOS}
assert all(d == 0 for d in dif_arma.values()), dif_arma
# ---------- razão indet Brasil (contagens brutas, todas as idades e sexos) ----------
cnt = df.groupby(["ano", "grupo"]).n.sum()
SER[("Brasil", "razao_indet_pp")] = {a: 100.0 * cnt[(a, "indet")] / (cnt[(a, "agressao")] + cnt[(a, "indet")]) for a in ANOS}


def its(y, quebras, log=True):
    X = est.desenho_its(quebras); yy = np.log(y) if log else np.array(y, float)
    b = np.linalg.lstsq(X, yy, rcond=None)[0]; e = yy - X @ b; dfr = len(yy) - X.shape[1]
    s2 = float(e @ e) / dfr; C = np.linalg.inv(X.T @ X); tc = stats.t.ppf(0.975, dfr); fat = stats.t.ppf(0.975, dfr) + stats.t.ppf(0.80, dfr)
    out = []
    for k, T in enumerate(quebras):
        j = 2 + 2 * k; L = b[j]; se = math.sqrt(s2 * C[j, j]); lo, hi = L - tc * se, L + tc * se; mde = fat * math.sqrt(s2) * math.sqrt(C[j, j])
        conv = (lambda z: 100 * (math.exp(z) - 1)) if log else (lambda z: z)
        out.append(dict(T=T, L=L, se=se, lo=lo, hi=hi, pct=conv(L), pct_lo=conv(lo), pct_hi=conv(hi), mde_neg=conv(-mde), mde_pos=conv(mde),
                        p=2 * (1 - stats.t.cdf(abs(L / se), dfr)), exclui=(lo > 0 or hi < 0), sigma=math.sqrt(s2), df=dfr))
    return out


ROWS = []; L = ["## D1 — série temporal interrompida nacional (gerado por c09_d1_its.py; DESCRITIVO, sem contrafactual)", "",
                f"Portas: taxas de agressão e agressão+indet dos 5 grupos recalculadas = `asr_brasil.csv` (tolerância 0,005); óbitos por arma de fogo (agressão) no agregado = soma das UFs do Atlas em 2010-2024 (0 de diferença). Modelo nível + inclinação, 15 pontos, 7 gl, IC t(7); placebo 1 ano antes.", "",
                "| série | desfecho | quebra | mudança de nível [IC95%] | p | MDE 80% (±) | placebo 1 ano antes [IC95%] | leitura pré-registrada | sigma residual |", "|---|---|---|---|---|---|---|---|---|"]
for (g, des), v in SER.items():
    y = [v[a] for a in ANOS]; log = des != "razao_indet_pp"; u = "%" if log else " p.p."
    pri, pla = its(y, (2016, 2019, 2023), log), its(y, (2015, 2018, 2022), log)
    for a, b in zip(pri, pla):
        if not a["exclui"]: leit = "não distinguível de zero"
        elif b["exclui"] and math.copysign(1, b["L"]) == math.copysign(1, a["L"]): leit = "não atribuível à troca (placebo dispara com o mesmo sinal)"
        else: leit = "coincide com a troca (descritivo; não causal)"
        ROWS.append(dict(serie=g, desfecho=des, quebra=a["T"], L=a["L"], se=a["se"], lo=a["lo"], hi=a["hi"], pct=a["pct"], pct_lo=a["pct_lo"], pct_hi=a["pct_hi"], p=a["p"],
                         mde_neg=a["mde_neg"], mde_pos=a["mde_pos"], placebo_quebra=b["T"], placebo_L=b["L"], placebo_lo=b["lo"], placebo_hi=b["hi"], placebo_pct=b["pct"],
                         placebo_pct_lo=b["pct_lo"], placebo_pct_hi=b["pct_hi"], leitura=leit, sigma=a["sigma"], df=a["df"]))
        L.append(f"| {g} | {des} | {a['T']} | {a['pct']:+.1f}{u} [{a['pct_lo']:+.1f}; {a['pct_hi']:+.1f}] | {a['p']:.3f} | {a['mde_neg']:+.1f}{u} / {a['mde_pos']:+.1f}{u} | {b['T']}: {b['pct']:+.1f}{u} [{b['pct_lo']:+.1f}; {b['pct_hi']:+.1f}] | {leit} | {a['sigma']:.4f} |")
L += ["", "Séries usadas (taxa padronizada por 100 mil; razão em %):", "", "| série | desfecho | " + " | ".join(str(a) for a in ANOS) + " |", "|---|---|" + "---|" * len(ANOS)]
for (g, des), v in SER.items(): L.append(f"| {g} | {des} | " + " | ".join(f"{v[a]:.2f}" for a in ANOS) + " |")
L += ["", "Limites: 15 pontos e 8 parâmetros (7 gl); EP clássico ignora autocorrelação; o segmento 2023-2024 tem 2 pontos e denominador extrapolado (⚠️ em `asr_brasil.md`); choques nacionais simultâneos (COVID, armas, facções, degradação do SIM) não são separáveis da troca. Nenhuma linha desta tabela é efeito do presidente."]
open(f"{AQUI}/c09_d1_resultados.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
with open(f"{AQUI}/c09_d1_resultados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys())); w.writeheader(); w.writerows([{k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()} for r in ROWS])
# ---------- c09_resultados.md ----------
pre = open(f"{AQUI}/PREREGISTRO-C09.md", "rb").read(); h = hashlib.sha256(pre[:pre.index(b"\n---\n\n**ADENDOS")]).hexdigest()
grav = open(f"{AQUI}/PREREGISTRO-C09.sha256", encoding="utf-8").read().split()[0]
assert h == grav, "corpo do pré-registro mudou"
cab = ["# C09 — resultados (presidência x violência letal; gerados por c09_d2_painel.py e c09_d1_its.py)", "",
       "> [!NOTE]", f"> Pré-registro `PREREGISTRO-C09.md` (corpo sha256 {h}, conferido nesta execução). Exploratório, NÃO causal. Nada aqui é sobre violência contra pessoas LGBT: o SIM não registra orientação, identidade nem motivação.", ""]
open(f"{AQUI}/c09_resultados.md", "w", encoding="utf-8").write("\n".join(cab) + "\n" + open(f"{AQUI}/c09_d2_resultados.md", encoding="utf-8").read() + "\n" + "\n".join(L) + "\n")
print("\n".join(L))
