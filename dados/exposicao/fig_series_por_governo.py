"""Figura da v0.5: o que cada série mostra por período de governo federal (pedido do autor, 2026-10-30:
"o que estamos verificando é se os crimes contra eles aumentam ou diminuem nesse período de governo").

Painel a: homicídio geral padronizado (SIM), com e sem as mortes de causa indeterminada, 2010-2024 (asr_brasil.csv).
Painéis b-e: as quatro séries LGBT+ disponíveis, todas de REGISTRO (R = I x p): lista do GGB (notícias, 2000-2025),
Disque 100 módulo LGBT (2011-2019 linhas; 2021-2026 denúncias com ao menos uma linha; 2020 mistura formatos, fora),
fichas do SUS com motivo LGBTfobia (2015-2025) e boletins de ocorrência do Anuário (2022-2025, edição mais recente).
Nenhuma série LGBT+ separa violência de registro; a figura não atribui causa a governo. Lê só arquivos do repositório.
Fundo branco; linhas verticais = posse presidencial. Título, nota e fonte ficam no documento (regra APA do pipeline).

Uso: /opt/homebrew/bin/python3.11 dados/exposicao/fig_series_por_governo.py <saida.png>
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

R = Path(__file__).resolve().parents[2]
INK, INK2, GRADE = "#1f1f1e", "#5b5a55", "#d9d8d3"
COR = "#6b3fa0"  # cor de "estatística/registro" do make_figures.py; azul e laranja ficam para grupos comparados
POSSES = [(2003, "Lula"), (2011, "Dilma"), (2016.37, "Temer"), (2019, "Bolsonaro"), (2023, "Lula")]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})


def ler(p: Path) -> list[dict]:
    return list(csv.DictReader(open(p, encoding="utf-8")))


def series() -> dict:
    s = {}
    asr = ler(R / "dados/sim/asr_brasil.csv")
    s["hom"] = {int(r["ano"]): float(r["taxa_padronizada"]) for r in asr if r["grupo"] == "Brasil" and r["desfecho"] == "agressao"}
    s["hom_ind"] = {int(r["ano"]): float(r["taxa_padronizada"]) for r in asr if r["grupo"] == "Brasil" and r["desfecho"] == "agressao+indet"}
    painel = ler(R / "research-2026-10-21-rodada3/GGB-completo/series/painel_mortes_lgbt.csv")
    ggb = {}
    for r in painel:  # total por ano: relatório de 2019 para 2000-2019; relatórios anuais depois; 2022 é derivado (256)
        if r["fonte"].startswith("ggb") and r["categoria"] == "total" and r["ano"] == r["ano_fim"] and r["valor"]:
            ggb[int(r["ano"])] = float(r["valor"])
    s["ggb"] = ggb
    d100 = ler(R / "dados/disque100/saidas/d100_serie_anual.csv")
    s["d100_linhas"] = {int(r["ano"]): float(r["n"]) for r in d100 if r["recorte"] == "grupo_lgbt" and r["unidade"] == "linhas" and int(r["ano"]) <= 2019}
    s["d100_den"] = {int(r["ano"]): float(r["n"]) for r in d100 if r["recorte"] == "grupo_lgbt" and r["unidade"] == "denuncias" and 2021 <= int(r["ano"]) <= 2025}
    sinan = ler(R / "dados/sinan/serie_campo55_uf_ano.csv")
    s["sinan"] = {int(r["ano"]): float(r["m_lgbtfobia"]) for r in sinan if r["uf"] == "BR"}
    anu = ler(R / "dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv")
    bo = {}
    for r in sorted((r for r in anu if r["uf"] == "BR" and r["marca"] == "valor"), key=lambda r: int(r["edicao"])):
        bo[int(r["ano_dado"])] = float(r["registros"])  # a edição mais recente sobrescreve a anterior
    s["bo"] = bo
    return s


def posses(ax, rotulo=False):
    for x, nome in POSSES:
        ax.axvline(x, color=INK2, lw=0.6, ls=(0, (2, 2)), zorder=0)
        if rotulo:
            ax.text(x + 0.15, 1.0, nome, transform=ax.get_xaxis_transform(), fontsize=7, color=INK2, va="bottom")


def linha(ax, d, **kw):
    xs = sorted(d); ax.plot(xs, [d[x] for x in xs], marker="o", ms=2.8, lw=1.6, **kw)


def main(saida: Path) -> None:
    s = series()
    fig, axs = plt.subplots(5, 1, figsize=(6.6, 8.6), dpi=300, sharex=True)
    ax = axs[0]
    linha(ax, s["hom"], color=INK, label="agressão")
    linha(ax, s["hom_ind"], color=INK2, ls=(0, (3, 2)), label="agressão + causa indeterminada")
    ax.set_ylabel("por 100 mil", fontsize=7.5)
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.set_title("a  Homicídio de toda a população (taxa padronizada; único painel que não é registro LGBT+)", loc="left", fontsize=8, color=INK, pad=14)
    painéis = [("b  Lista do GGB: mortes noticiadas na imprensa (contagem da organização)", [("ggb", {})]),
               ("c  Disque 100, módulo LGBT: linhas até 2019 e denúncias desde 2021 (unidades diferentes)",
                [("d100_linhas", {"color": INK2}), ("d100_den", {})]),
               ("d  Fichas do SUS com motivo marcado como LGBTfobia", [("sinan", {})]),
               ("e  Boletins de ocorrência por homofobia ou transfobia (Anuário)", [("bo", {})])]
    for ax, (tit, ss) in zip(axs[1:], painéis):
        for k, kw in ss:
            linha(ax, s[k], **({"color": COR} | kw))
        ax.set_title(tit, loc="left", fontsize=8, color=INK)
        ax.set_ylabel("registros", fontsize=7.5)
    for i, ax in enumerate(axs):
        posses(ax, rotulo=(i == 0))
        ax.grid(axis="y", color=GRADE, lw=0.5); ax.set_axisbelow(True)
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    axs[-1].set_xlim(1999.5, 2026.5)
    axs[-1].set_xticks(range(2000, 2027, 2))
    fig.align_ylabels(axs)
    fig.tight_layout(h_pad=1.0)
    fig.savefig(saida, dpi=300, facecolor="white")
    print(saida, {k: (min(v), max(v)) for k, v in s.items() if v})


if __name__ == "__main__":
    main(Path(sys.argv[1]))
