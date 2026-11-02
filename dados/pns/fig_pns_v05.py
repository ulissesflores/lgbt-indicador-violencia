"""Figura 2 da v0.5: violência relatada em 12 meses por adultos LGB+ e heterossexuais (PNS 2019).

Painel a: prevalência de violência física, sexual, psicológica e de qualquer tipo, com IC95% (desenho complexo).
Painel b: razão de prevalências bruta (círculo vazado) e ajustada (quadrado cheio) por sexo, idade, cor, instrução,
região e moradia urbana ou rural, com IC95%, em escala log. Mesmos dados e leitura de ler_pns() em
paper/figures/make_figures.py (seguro_pns2019.csv + tabela 1 de seguro_pns2019.md); acrescenta a psicológica, que a
figura da v0.4.4 não mostrava. Fundo branco; título, nota e fonte ficam no documento (regra APA do pipeline).

Uso: /opt/homebrew/bin/python3.11 dados/pns/fig_pns_v05.py <saida.png>
"""
from __future__ import annotations

import csv
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AQUI = Path(__file__).resolve().parent
INK, INK2, GRADE = "#1f1f1e", "#5b5a55", "#d9d8d3"
LGB, HET, ESTAT = "#2a78d6", "#eb6834", "#6b3fa0"  # PALETA de make_figures.py: azul LGB+, laranja hetero, roxo estatística
ORDEM = ["física", "sexual", "psicológica", "qualquer"]
NOMES = {"física": "Física", "sexual": "Sexual", "psicológica": "Psicológica", "qualquer": "Qualquer tipo"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})


def br(x: float, casas: int) -> str:
    return f"{Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP):.{casas}f}".replace(".", ",")


def ler() -> dict:
    out: dict = {}
    for r in csv.DictReader(open(AQUI / "seguro_pns2019.csv", encoding="utf-8")):
        if r["bloco"] == "nivel":
            out.setdefault(r["rotulo"], {}).update(lgb=100 * float(r["prev_grupo"]), het=100 * float(r["prev_ref"]),
                                                   rp=float(r["rp"]), rp_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
        elif r["bloco"] == "rp_ajustada":
            out[r["rotulo"]].update(rpaj=float(r["rp"]), rpaj_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
    sec = (AQUI / "seguro_pns2019.md").read_text(encoding="utf-8").split("## 1.")[1].split("## 2.")[0]
    for ln in sec.splitlines():
        m = re.match(r"\| (física|sexual|psicológica|qualquer) \| ([\d.]+)% \[([\d.]+); ([\d.]+)\] \| ([\d.]+)% \[([\d.]+); ([\d.]+)\]", ln)
        if m:
            out[m.group(1)].update(het_ic=[float(m.group(3)), float(m.group(4))], lgb_ic=[float(m.group(6)), float(m.group(7))])
    return out


def main(saida: Path) -> None:
    d = ler()
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.6), dpi=300, gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.45})
    y = list(range(len(ORDEM)))[::-1]
    off = 0.17
    for g, cor, dy, rot in (("lgb", LGB, off, "LGB+"), ("het", HET, -off, "Heterossexuais")):
        for k, yv in zip(ORDEM, y):
            v, (lo, hi) = d[k][g], d[k][g + "_ic"]
            a.errorbar([v], [yv + dy], xerr=[[v - lo], [hi - v]], fmt="o", ms=5, color=cor, ecolor=cor, elinewidth=1.6,
                       capsize=2.2, label=rot if k == ORDEM[0] else None)
            a.annotate(f"{br(v, 2)}%", (hi, yv + dy), xytext=(4, -3), textcoords="offset points", fontsize=7, color=INK)
    a.set_yticks(y, [NOMES[k] for k in ORDEM], fontsize=8.5)
    a.set_xlabel("Adultos que relataram violência em 12 meses (%)", fontsize=7.5)
    a.set_xlim(-1, 62)
    a.grid(axis="x", color=GRADE, lw=0.5); a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    a.set_title("a  Quantos relataram", loc="left", fontsize=9, color=INK)
    a.set_ylim(-0.6, len(ORDEM) - 0.4)
    for tipo, mk, fc, rot in (("rp", "o", "white", "razão bruta"), ("rpaj", "s", ESTAT, "razão ajustada")):
        dy = off if tipo == "rp" else -off
        for k, yv in zip(ORDEM, y):
            v, (lo, hi) = d[k][tipo], d[k][tipo + "_ic"]
            b.errorbar([v], [yv + dy], xerr=[[v - lo], [hi - v]], fmt=mk, ms=5, mfc=fc, mec=ESTAT, color=ESTAT,
                       elinewidth=1.6, capsize=2.2, label=rot if k == ORDEM[0] else None)
            b.annotate(br(v, 2), (hi, yv + dy), xytext=(4, -3), textcoords="offset points", fontsize=7, color=INK)
    b.set_xscale("log")
    b.axvline(1, color=INK2, lw=0.8, ls=(0, (3, 2)))
    b.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"]); b.minorticks_off()
    b.set_xlim(0.8, 25)
    b.set_ylim(a.get_ylim())
    b.set_yticks(y, [NOMES[k] for k in ORDEM], fontsize=8.5)
    b.set_xlabel("Razão LGB+ / heterossexuais (escala log; 1 = igual)", fontsize=7.5)
    b.grid(axis="x", color=GRADE, lw=0.5); b.set_axisbelow(True)
    b.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    b.set_title("b  A razão entre os dois grupos", loc="left", fontsize=9, color=INK)
    fig.savefig(saida, dpi=300, facecolor="white", bbox_inches="tight")
    print(saida, {k: (br(d[k]["lgb"], 2), br(d[k]["het"], 2), br(d[k]["rpaj"], 2)) for k in ORDEM})


if __name__ == "__main__":
    main(Path(sys.argv[1]))
