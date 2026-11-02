"""Figura 4 da v0.5 (Disque 100), redesenho da fig28 de paper/figures/make_figures.py em fundo branco: as barras do canal
inteiro de 2011 a 2020 deixam o preenchimento cinza e ficam brancas com contorno. Mesmo código e mesmos dados (fontes/).

Uso: /opt/homebrew/bin/python3.11 dados/disque100/fig_disque_v05.py <saida.png>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "paper/figures"))
from make_figures import *  # noqa: E402,F401,F403

def figura4_v05(saida) -> None:
    """Disque 100: (a) modulo LGBT por ano, com a unidade de cada trecho e as quatro quebras de serie; (b) canal inteiro e fatia do modulo LGBT."""
    d = ler_d100()
    anos = sorted(d)
    xm = {a: a + 0.5 for a in anos}                      # ponto no meio do ano: as quebras semestrais caem em 2020,0 / 2020,5 / 2022,5 / 2024,0
    fig = plt.figure(figsize=(7.2, 6.7))
    a = fig.add_axes([0.11, 0.545, 0.86, 0.385])
    b = fig.add_axes([0.11, 0.09, 0.86, 0.34])
    cor_u = {"linhas": PALETA["ref"], "denuncias": PALETA["estat"]}
    seg_a = [x for x in anos if x <= 2019]
    seg_c = [x for x in anos if x >= 2021]
    la, = a.plot([xm[x] for x in seg_a], [d[x]["lgbt"] for x in seg_a], "-o", color=cor_u["linhas"], lw=2.2, ms=5)
    l20, = a.plot([xm[2020]], [d[2020]["lgbt"]], "D", color=cor_u["linhas"], mfc="white", mew=1.8, ms=7)
    lc, = a.plot([xm[x] for x in seg_c], [d[x]["lgbt"] for x in seg_c], "-o", color=cor_u["denuncias"], lw=2.4, ms=5.5)
    pt26, = a.plot([xm[2026]], [d[2026]["lgbt"]], "o", color=cor_u["denuncias"], mfc="white", mew=2, ms=7)
    vl = []
    for xq, rot in D100_QUEBRAS:
        v = a.axvline(xq, color=INK2, lw=1, ls=":")
        vl.append(v)
        a.text(xq - 0.07, 14850, rot, rotation=90, ha="right", va="top", fontsize=MIN_PT, color=INK)
    a.set_xlim(2010.6, 2027.3), a.set_ylim(0, 15000)
    a.set_xticks([xm[x] for x in anos], [str(x) if x < 2026 else "2026*" for x in anos], fontsize=MIN_PT)
    a.tick_params(axis="y", labelsize=MIN_PT)
    a.set_yticks(range(0, 13001, 2000), [miles(v) for v in range(0, 13001, 2000)])
    a.set_ylabel("Registros do módulo LGBT por ano", fontsize=MIN_PT + 0.3)
    a.grid(axis="y", color=GRADE, lw=0.6), a.set_axisbelow(True)
    for ano, dy, ha_ in ((2011, -850, "center"), (2012, 380, "center"), (2019, -820, "center")):
        a.text(xm[ano], d[ano]["lgbt"] + dy, miles(d[ano]["lgbt"]), ha=ha_, fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2021] - 0.25, d[2021]["lgbt"] + 350, miles(d[2021]["lgbt"]), ha="right", va="bottom", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2025] - 0.3, d[2025]["lgbt"] + 350, miles(d[2025]["lgbt"]), ha="right", va="bottom", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2020], d[2020]["lgbt"] + 650, f"{miles(d[2020]['lgbt'])}\n(2 formatos)", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold", linespacing=1.1, bbox={"fc": "white", "ec": "none", "pad": 1.0})
    a.text(xm[2026] - 0.1, d[2026]["lgbt"] + 560, f"{miles(d[2026]['lgbt'])}\naté setembro", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(2013.1, 6900, "2011-2019: linhas do arquivo\n(vítima x suspeito, sem chave de pessoa)", fontsize=MIN_PT + 0.2, color=PALETA["ref"], ha="left", va="bottom", linespacing=1.15)
    a.text(2027.2, 250, "2021-2026: denúncias\ncom ao menos uma linha\nno módulo LGBT", fontsize=MIN_PT + 0.2, color=PALETA["estat"], ha="right", va="bottom", linespacing=1.15, fontweight="bold", bbox={"fc": "white", "ec": "none", "pad": 1.0})
    a.set_title("(a) O módulo LGBT em cada ano: a unidade e o formato mudam ao longo da série", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.1)
    # painel (b): canal inteiro na mesma unidade do painel (a) + fatia do modulo LGBT
    alt = [d[x]["canal"] for x in anos]
    cores = [cor_u[d[x]["unidade"]] for x in anos]
    barras = b.bar([xm[x] for x in anos], [v / 1000 for v in alt], width=0.72, color=[PALETA["estat_cl"] if d[x]["unidade"] == "denuncias" else "white" for x in anos],
                   edgecolor=cores, linewidth=1.6)
    for p_, x in zip(barras, anos):
        if x == 2026:
            p_.set_hatch("///"), p_.set_edgecolor(PALETA["estat"])
    pcts = []
    for x, p_ in zip(anos, barras):
        pc = 100 * d[x]["lgbt"] / d[x]["canal"]
        pcts.append(pc)
        b.text(p_.get_x() + p_.get_width() / 2, p_.get_height() + 12, f"{br(pc)}%", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold")
    b.set_xlim(2010.6, 2027.3), b.set_ylim(0, 760)
    b.set_xticks([xm[x] for x in anos], [str(x) if x < 2026 else "2026*" for x in anos], fontsize=MIN_PT)
    b.tick_params(axis="y", labelsize=MIN_PT)
    b.set_ylabel("Registros do canal inteiro\n(milhares)", fontsize=MIN_PT + 0.3)
    b.grid(axis="y", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.axvline(2021.0, color=INK2, lw=1, ls=":")
    b.text(2020.9, 735, "unidade: linhas", ha="right", va="top", fontsize=MIN_PT, color=INK2)
    b.text(2021.1, 735, "unidade: denúncias", ha="left", va="top", fontsize=MIN_PT, color=PALETA["estat"])
    b.set_title("(b) O canal inteiro cresce; em cima de cada barra, a parte do módulo LGBT", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.1)
    r21, r25 = d[2021], d[2025]
    fig.savefig(saida, dpi=300, facecolor="white")
    print(saida)


if __name__ == "__main__":
    figura4_v05(Path(sys.argv[1]))
