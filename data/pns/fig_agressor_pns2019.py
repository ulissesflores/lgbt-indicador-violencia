"""Figura 'quem agrediu' da v0.5 (PNS 2019, violência física em 12 meses), lida SÓ de agressor_risco_pns2019.csv.

Painel a: dois anéis, um por grupo, com ÁREA proporcional ao risco total (14,70 contra 3,82 adultos agredidos por
100); cada fatia é o risco por tipo de agressor, de modo que fatia de mesma área = mesmo risco nos dois grupos.
Painel b: razão de risco LGB+/heterossexual AJUSTADA (mesmo ajuste da razão 2,82) por tipo de agressor, com intervalo de
95% (eixo em escala log); revisão de 2026-10-30 (críticas GRO-01/AST-01: a razão bruta não tinha ajuste).
Patrão ou chefe (n muito pequeno), policial e outro vão juntos em "Outro" no anel; no painel b só entram os tipos
com intervalo informativo. Título, nota e fonte ficam no documento (regra APA do pipeline).

Uso: /opt/homebrew/bin/python3.11 data/pns/fig_agressor_pns2019.py <saida.png>
"""
from __future__ import annotations

import csv
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AQUI = Path(__file__).resolve().parent
INK, INK2, GRADE = "#1f1f1e", "#5b5a55", "#d9d8d3"
# cores por tipo de agressor (azul e laranja ficam reservados aos grupos, como em make_figures.py);
# validadas com o validate_palette.js do skill dataviz: CVD adjacente >= 8,8; cinza = "Outro", neutro de propósito
TIPOS = [("Parceiro(a) ou ex", "Parceiro(a) ou ex", "#6250d6"), ("Familiar", "Familiar", "#1baf7a"),
         ("Amigo(a), colega ou vizinho(a)", "Amigo(a), colega\nou vizinho(a)", "#eda100"),
         ("Pessoa desconhecida", "Pessoa desconhecida", "#e34948")]
OUTRO = (["Empregado(a), patrão ou chefe", "Policial", "Outro"], "Empregado, patrão,\npolicial ou outro", "#8b8a85")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})


def br(x: float, casas: int = 2) -> str:
    d = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)
    return f"{d:.{casas}f}".replace(".", ",")


def main(saida: Path) -> None:
    linhas = list(csv.DictReader(open(AQUI / "agressor_risco_pns2019.csv", encoding="utf-8")))
    risco = {r["rotulo"]: r for r in linhas if r["bloco"] == "risco_populacao"}
    ajust = {r["rotulo"]: r for r in linhas if r["bloco"] == "rp_ajustada_agressor"}
    grupos = {"LGB+": "lgb", "Heterossexuais": "het"}
    fatias = {}
    for nome, col in grupos.items():
        v = [100 * float(risco[k][col]) for k, _, _ in TIPOS]
        v.append(100 * sum(float(risco[k][col]) for k in OUTRO[0]))
        fatias[nome] = v
    total = {n: sum(v) for n, v in fatias.items()}
    cores = [c for _, _, c in TIPOS] + [OUTRO[2]]
    rotulos = [r for _, r, _ in TIPOS] + [OUTRO[1]]

    fig = plt.figure(figsize=(6.9, 3.9), dpi=300)
    ax = fig.add_axes([0.0, 0.2, 0.52, 0.76])
    ax.set_aspect("equal"); ax.axis("off")
    rmax, buraco = 1.0, 0.56  # mesma razão interno/externo nos dois anéis: área do anel proporcional a R²
    centros = {"LGB+": (0.0, 0.0), "Heterossexuais": (1.62, -0.35)}
    for nome in ("LGB+", "Heterossexuais"):
        R = rmax * math.sqrt(total[nome] / total["LGB+"])
        cx, cy = centros[nome]
        ax.pie(fatias[nome], radius=R, center=(cx, cy), colors=cores, startangle=90, counterclock=False,
               wedgeprops={"width": R * (1 - buraco), "edgecolor": "white", "linewidth": 1.2})
        ax.text(cx, cy + 0.04 * R / rmax, br(total[nome]), ha="center", va="center", fontsize=11 if R > 0.7 else 8,
                fontweight="bold", color=INK)
        ax.text(cx, cy - 0.17 * (R / rmax) ** 0.5, "por 100", ha="center", va="center", fontsize=7, color=INK2)
        ax.text(cx, cy - R - 0.13, nome, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        if nome == "LGB+":  # rótulo direto das fatias grandes (valor por 100); as demais estão na Tabela
            ang = 90.0
            for v, c in zip(fatias[nome], cores):
                meio = math.radians(ang - 360 * v / total[nome] / 2)
                ang -= 360 * v / total[nome]
                if v >= 1.8:
                    rr = R * (1 + buraco) / 2
                    ax.text(cx + rr * math.cos(meio), cy + rr * math.sin(meio), br(v), ha="center", va="center",
                            fontsize=7.5, color="white" if c in ("#6250d6", "#e34948") else INK, fontweight="bold")
    ax.set_xlim(-1.08, 2.25); ax.set_ylim(-1.25, 1.08)
    ax.text(-1.06, 1.06, "a", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in cores], labels=[r.replace("\n", " ") for r in rotulos],
               loc="lower left", bbox_to_anchor=(0.01, 0.0), ncol=3, frameon=False, fontsize=7, handlelength=1.0,
               columnspacing=1.2)

    bx = fig.add_axes([0.74, 0.3, 0.24, 0.64])
    itens = [(k, {"Amigo(a), colega\nou vizinho(a)": "Amigo, colega\nou vizinho", "Parceiro(a) ou ex": "Parceiro ou ex", "Pessoa desconhecida": "Desconhecido"}.get(r, r), c) for k, r, c in TIPOS] + [("Pessoa conhecida (todos acima)", "Qualquer conhecido", INK)]
    itens = [itens[i] for i in (0, 1, 2, 4, 3)]
    for i, (k, rot, c) in enumerate(itens):
        y = len(itens) - 1 - i
        m, lo, hi = (float(ajust[k][x]) for x in ("medida", "ic_lo", "ic_hi"))
        bx.plot([lo, hi], [y, y], color=c, lw=2, solid_capstyle="round")
        bx.plot(m, y, "o", color=c, ms=7, mec="white", mew=1.2, zorder=3)
        bx.text(hi * 1.12, y, br(m), va="center", fontsize=7.5, color=INK)
    bx.axvline(1, color=INK2, lw=0.8, ls=(0, (3, 2)))
    bx.set_xscale("log"); bx.set_xlim(0.8, 25)
    bx.set_xticks([1, 2, 5, 10, 20]); bx.set_xticklabels(["1", "2", "5", "10", "20"])
    bx.minorticks_off()
    bx.set_yticks(range(len(itens))); bx.set_yticklabels([r for _, r, _ in itens][::-1], fontsize=7.5)
    bx.set_xlabel("Razão ajustada de risco,\nLGB+ / heterossexuais", fontsize=7.5, color=INK)
    bx.tick_params(axis="y", length=0)
    bx.spines["left"].set_visible(False)
    bx.grid(axis="x", color=GRADE, lw=0.5); bx.set_axisbelow(True)
    fig.text(0.56, 0.96, "b", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.savefig(saida, dpi=300, facecolor="white")
    print(saida, {n: br(t) for n, t in total.items()})


if __name__ == "__main__":
    main(Path(sys.argv[1]))
