"""Projeção 2025-2030 da taxa de mortalidade por agressão PADRONIZADA POR IDADE, por sexo x raça (F7: "simular os dados futuros").
Entrada: dados/sim/asr_brasil.csv (padroniza_idade.py; desfecho 'agressao' e 'agressao+indet'). Série 2010-2024 (15 pontos): curta e com quebras (pico 2017, queda desde 2018, COVID 2020).
Método (declarado antes de rodar): modelos simples na escala log, selecionados por BACKTEST de origem móvel (origens 2016-2023, horizontes 1-5), não por ajuste dentro da amostra:
  rw (último valor) | drift8 (tendência média das últimas 8 diferenças) | damp (tendência média das últimas 5 diferenças amortecida por phi=0,8) |
  holt (nível+tendência por suavização exponencial, alfa/beta em grade, mínimo SSE) | ols7 (reta nos últimos 7 pontos).
  Métrica: MASE contra rw; escolhe-se o modelo de menor erro absoluto médio pooled; ponto = previsão do modelo SEM correção de viés; intervalos 80%/95% SIMÉTRICOS na escala log = quantis (80% e 95%) do ERRO ABSOLUTO de backtest por horizonte (poolado entre grupos);
  (revisão 2026-10-21: a 1ª versão somava a mediana dos erros, que é negativa porque as origens 2016-2023 caem no regime de queda, e isso embutia 'a queda continua' no centro; removido.)
  Dois cenários de centro: 'persistencia' (rw: taxa de 2024 constante) e 'tendencia' (damp: queda recente amortecida). O backtest favorece o de menor erro, mas o regime recente de queda torna a escolha frágil.
  h>5 extrapolado com crescimento sqrt(h/5) do erro de h=5 (limitação declarada).
LIMITES (valem para a leitura): série curta; denominador de 2023-24 extrapolado (padroniza_idade.py); degradação do registro desde 2018 (mortes de intenção indeterminada: usar 'agressao+indet' como cenário alternativo);
  é projeção CONDICIONAL à continuidade da dinâmica recente, NÃO previsão de políticas ou choques (facções, armas, COVID); o intervalo mede erro histórico de método, não incerteza estrutural.
Rodar: /opt/homebrew/bin/python3.14 -I dados/sim/projecao_grupos.py   Saídas: dados/sim/projecao_grupos.csv/.md e fig-projecao_grupos.png"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = (REPO_ROOT + "/dados/sim")
GRUPOS = ["Brasil", "Homens", "Mulheres", "Negros", "Não negros", "Homens negros", "Homens não negros", "Mulheres negras", "Mulheres não negras"]
H = 5


def f_rw(y, h): return np.repeat(y[-1], h)
def f_drift8(y, h):
    d = np.diff(y)[-8:].mean(); return y[-1] + d * np.arange(1, h + 1)
def f_damp(y, h, phi=0.8):
    d = np.diff(y)[-5:].mean(); return y[-1] + d * np.cumsum(phi ** np.arange(1, h + 1))
def f_ols7(y, h):
    x = np.arange(7); b, a = np.polyfit(x, y[-7:], 1); return a + b * (7 - 1 + np.arange(1, h + 1))
def f_holt(y, h):
    best = None
    for al in (0.2, 0.5, 0.8):
        for be in (0.1, 0.3, 0.6):
            l, t = y[0], y[1] - y[0]; sse = 0.0
            for v in y[1:]:
                e = v - (l + t); sse += e * e
                ln = l + t + al * e; t = t + al * be * e; l = ln
            if best is None or sse < best[0]: best = (sse, l, t)
    _, l, t = best; return l + t * np.cumsum(0.9 ** np.arange(1, h + 1))
MODELOS = {"rw": f_rw, "drift8": f_drift8, "damp": f_damp, "holt": f_holt, "ols7": f_ols7}


def main():
    df = pd.read_csv(f"{BASE}/asr_brasil.csv")
    out_rows = []; L = ["# Projeção 2025-2030 da taxa padronizada de agressão por sexo x raça (gerado por projecao_grupos.py)", "",
                        "Escala log; seleção por backtest de origem móvel; intervalos = quantis empíricos dos erros de backtest. LEIA os limites no cabeçalho do script.", ""]
    for desf in ("agressao", "agressao+indet"):
        S = {g: df[(df.grupo == g) & (df.desfecho == desf)].sort_values("ano").set_index("ano").taxa_padronizada for g in GRUPOS}
        anos = list(S["Brasil"].index); assert anos[0] == 2010 and anos[-1] == 2024
        # ---- backtest
        err = {m: {h: [] for h in range(1, H + 1)} for m in MODELOS}; naive_abs = {h: [] for h in range(1, H + 1)}
        for g in GRUPOS:
            y = np.log(S[g].values)
            for T in range(2016, 2024):  # origem: último ano observado = T
                k = T - 2010 + 1
                for h in range(1, min(H, 2024 - T) + 1):
                    real = y[k - 1 + h]
                    naive_abs[h].append(abs(real - y[k - 1]))
                    for m, fm in MODELOS.items():
                        err[m][h].append(real - fm(y[:k], h)[-1])
        mae = {m: np.mean([abs(e) for h in err[m] for e in err[m][h]]) for m in MODELOS}
        mase = {m: np.mean([abs(e) for h in err[m] for e in err[m][h]]) / np.mean([a for h in naive_abs for a in naive_abs[h]]) for m in MODELOS}
        melhor = min(mae, key=mae.get)
        L += [f"## Desfecho: {desf}", "", "Backtest (erro absoluto médio na escala log, pooled 9 grupos x origens 2016-2023 x h=1..5; MASE contra rw):", "",
              "| modelo | MAE log | MASE |", "|---|---|---|"] + [f"| {m} | {mae[m]:.3f} | {mase[m]:.2f} |" for m in MODELOS] + ["", f"Modelo escolhido (menor MAE): **{melhor}**.", ""]
        qa = {}
        for h in range(1, H + 1):
            ea = np.abs(np.array(err[melhor][h])); qa[h] = (np.percentile(ea, 80), np.percentile(ea, 95))
        cob80 = np.mean([abs(e) <= qa[h][0] for h in range(1, H + 1) for e in err[melhor][h]])
        viés = {m: np.mean([e for h in err[m] for e in err[m][h]]) for m in MODELOS}
        L += [f"Viés médio do erro (real - previsto, log) por modelo: " + "; ".join(f"{m} {v:+.3f}" for m, v in viés.items()) + " (negativo = a queda recente foi subestimada: as origens de backtest caem no regime de queda).",
              f"Cobertura empírica do IC80 nos próprios erros de backtest (otimista, por construção): {cob80:.0%}.", "",
              "| grupo | 2024 obs | " + " | ".join(f"{a}: persistência / tendência (damp) [IC80 da persistência]" for a in (2025, 2027, 2030)) + " |", "|---|---|---|---|---|"]
        for g in GRUPOS:
            y = np.log(S[g].values); fcs = {"persistencia": f_rw(y, 7), "tendencia": f_damp(y, 7)}
            cel = []
            for ano in (2025, 2027, 2030):
                h = ano - 2024; hh = min(h, H); esc = math.sqrt(h / H) if h > H else 1.0
                a80, a95 = qa[hh][0] * esc, qa[hh][1] * esc
                cel.append(f"{math.exp(fcs['persistencia'][h-1]):.1f} / {math.exp(fcs['tendencia'][h-1]):.1f} [{math.exp(fcs['persistencia'][h-1]-a80):.1f}; {math.exp(fcs['persistencia'][h-1]+a80):.1f}]")
            L.append(f"| {g} | {math.exp(y[-1]):.1f} | " + " | ".join(cel) + " |")
            for cen, fc in fcs.items():
                for ano in range(2025, 2031):
                    h = ano - 2024; hh = min(h, H); esc = math.sqrt(h / H) if h > H else 1.0
                    a80, a95 = qa[hh][0] * esc, qa[hh][1] * esc
                    out_rows.append([desf, g, ano, cen, round(math.exp(fc[h-1]), 2), round(math.exp(fc[h-1] - a80), 2), round(math.exp(fc[h-1] + a80), 2), round(math.exp(fc[h-1] - a95), 2), round(math.exp(fc[h-1] + a95), 2)])
        L.append("")
    open(f"{BASE}/projecao_grupos.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(f"{BASE}/projecao_grupos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["desfecho", "grupo", "ano", "cenario_centro", "ponto", "ic80_lo", "ic80_hi", "ic95_lo", "ic95_hi"]); w.writerows(out_rows)
    fig, ax = plt.subplots(2, 3, figsize=(15, 7)); ax = ax.ravel()
    d0 = df[df.desfecho == "agressao"]; pr = pd.DataFrame(out_rows, columns=["desfecho", "grupo", "ano", "modelo", "med", "l80", "h80", "l95", "h95"]); pr = pr[(pr.desfecho == "agressao") & (pr.modelo == "persistencia")]
    for i, g in enumerate(["Mulheres não negras", "Mulheres negras", "Homens não negros", "Homens negros", "Negros", "Não negros"]):
        s = d0[d0.grupo == g].sort_values("ano"); p = pr[pr.grupo == g]
        ax[i].plot(s.ano, s.taxa_padronizada, "k-o", ms=3); ax[i].plot(p.ano, p.med, "r--"); ax[i].fill_between(p.ano, p.l80, p.h80, color="r", alpha=0.2); ax[i].fill_between(p.ano, p.l95, p.h95, color="r", alpha=0.08)
        ax[i].set_title(g, fontsize=9); ax[i].set_ylim(bottom=0)
    plt.tight_layout(); plt.savefig(f"{BASE}/fig-projecao_grupos.png", dpi=120)
    print("\n".join(L))


if __name__ == "__main__":
    main()
