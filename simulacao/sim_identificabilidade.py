"""Simulacao F7 — identificabilidade da serie REGISTRADA de LGBTfobia (Anuario FBSP).

Pergunta: a alta 783 -> 3.481 (2022-2025) nos BOs pode vir de incidencia subindo, constante ou caindo?
Modelo: R_t ~ Poisson(I_t * p_t); I_t = I0*(1+g)^(t-2022); p_t = min(1, p0*(1+h)^(t-2022)).
Para g fixo (cenario), ajusta I0 e h por minimos quadrados em log; depois projeta 2026-2030 com ruido Poisson
e incerteza parametrica (bootstrap de residuos). Em seguida: tamanho de survey bienal que separa os cenarios.
Semente fixa. Saidas: CSV + PNG + resumo.md nesta pasta.
"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20261011)
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ANOS_OBS = np.array([2022, 2023, 2024, 2025])
R_OBS = np.array([783, 1633, 2567, 3481])          # Anuario FBSP, valores revisados (ed. 2024/25/26)
ANOS_PROJ = np.arange(2026, 2031)
P0 = 0.04   # fracao de incidentes verdadeiros que vira BO com motivacao em 2022 (suposicao; sensibilidade abaixo)
CENARIOS = {"S1 incidencia constante": 0.00, "S2 incidencia +15%/ano": 0.15, "S3 incidencia -5%/ano": -0.05}

def rec(I0, h, g, anos, p0=P0):
    t = anos - 2022
    I = I0 * (1 + g) ** t
    p = np.minimum(1.0, p0 * (1 + h) ** t)
    return I, p, I * p

def fit(g, p0=P0):
    def sse(x):
        I0, h = math.exp(x[0]), x[1]
        _, _, mu = rec(I0, h, g, ANOS_OBS, p0)
        return float(np.sum((np.log(mu) - np.log(R_OBS)) ** 2))
    res = minimize(sse, x0=[math.log(R_OBS[0] / p0), 0.3], method="Nelder-Mead")
    return math.exp(res.x[0]), res.x[1], res.fun

linhas = []; resumo = {}
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for nome, g in CENARIOS.items():
    I0, h, sse = fit(g)
    I_proj, p_proj, mu_proj = rec(I0, h, g, ANOS_PROJ)
    # incerteza: bootstrap de residuos log + Poisson
    sims = []
    _, _, mu_obs = rec(I0, h, g, ANOS_OBS)
    resid = np.log(R_OBS) - np.log(mu_obs)
    for _ in range(2000):
        Rb = np.exp(np.log(mu_obs) + rng.choice(resid, size=len(resid), replace=True))
        def sse_b(x, Rb=Rb):
            _, _, m = rec(math.exp(x[0]), x[1], g, ANOS_OBS); return float(np.sum((np.log(m) - np.log(Rb)) ** 2))
        rb = minimize(sse_b, x0=[math.log(I0), h], method="Nelder-Mead")
        _, _, m = rec(math.exp(rb.x[0]), rb.x[1], g, ANOS_PROJ)
        sims.append(rng.poisson(m))
    sims = np.array(sims)
    lo, med, hi = np.percentile(sims, [5, 50, 95], axis=0)
    resumo[nome] = {"g": g, "I0_2022": round(I0), "h_registro": round(h, 3), "sse_log": round(sse, 4),
                    "p_2025": round(float(np.minimum(1, P0 * (1 + h) ** 3)), 3),
                    "I_2030": round(float(I_proj[-1])), "R_2030_mediana": int(med[-1]), "R_2030_IC90": [int(lo[-1]), int(hi[-1])]}
    for a, l, m_, hh, I_, p_ in zip(ANOS_PROJ, lo, med, hi, I_proj, p_proj):
        linhas.append([nome, int(a), int(l), int(m_), int(hh), round(float(I_)), round(float(p_), 3)])
    ax[0].plot(ANOS_PROJ, med, label=nome); ax[0].fill_between(ANOS_PROJ, lo, hi, alpha=0.15)
    ax[1].plot(np.r_[ANOS_OBS, ANOS_PROJ], np.r_[rec(I0, h, g, ANOS_OBS)[0], I_proj], label=nome)
ax[0].scatter(ANOS_OBS, R_OBS, c="k", zorder=5, label="Anuário (observado)")
ax[0].set_title("Série REGISTRADA (BO c/ motivação LGBTfobia) — 3 cenários, IC90%"); ax[0].legend(fontsize=8)
ax[1].set_title("Incidência VERDADEIRA implícita (não observada)"); ax[1].set_yscale("log"); ax[1].legend(fontsize=8)
for a_ in ax: a_.set_xlabel("ano")
plt.tight_layout(); plt.savefig(f"{OUT}/fig-identificabilidade.png", dpi=130)

# sensibilidade a P0
sens = {}
for p0 in [0.02, 0.04, 0.08, 0.15]:
    sens[p0] = {n: round(fit(g, p0)[2], 4) for n, g in CENARIOS.items()}

# --- survey bienal: n necessario para separar cenarios (duas proporcoes, alfa 5%, poder 80%)
PREV_LGB = 0.0189          # PNS 2019 (Vasconcelos et al. 2023)
VIT_FISICA = 0.147         # PNS 2019: violencia fisica 12 m entre LGB+ (14,70%)
def n_duas_prop(p1, p2, alpha=0.05, power=0.8):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    pb = (p1 + p2) / 2
    return math.ceil(((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p1 - p2)) ** 2)
poder = []
for delta in [0.10, 0.20, 0.30, 0.50]:
    n_lgb = n_duas_prop(VIT_FISICA, VIT_FISICA * (1 + delta))
    poder.append({"mudanca_relativa": delta, "n_LGB_por_rodada": n_lgb, "n_total_sem_sobreamostra": math.ceil(n_lgb / PREV_LGB),
                  "n_total_com_sobreamostra_5x": math.ceil(n_lgb / (PREV_LGB * 5))})

import csv
with open(f"{OUT}/projecao-registrada-2026-2030.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["cenario", "ano", "R_p5", "R_mediana", "R_p95", "I_verdadeira", "p_registro"]); w.writerows(linhas)
with open(f"{OUT}/poder-survey.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(poder[0].keys())); w.writeheader(); w.writerows(poder)
with open(f"{OUT}/resumo.json", "w") as f:
    json.dump({"observado": dict(zip(map(int, ANOS_OBS), map(int, R_OBS))), "P0": P0, "cenarios": resumo, "sse_por_p0": sens, "poder_survey": poder}, f, indent=1, ensure_ascii=False)
print(json.dumps({"cenarios": resumo, "sse_por_p0": sens, "poder": poder}, indent=1, ensure_ascii=False))
