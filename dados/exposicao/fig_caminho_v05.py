"""Figura 1 da v0.5 (caminho do dado), redesenho em fundo branco da fig24 de paper/figures/make_figures.py.

Gerado por recorte do código da fig24 (mesmo desenho, mesmos arquivos de origem em paper/figures/fontes/): sem as faixas
cinza por linha, caixas com preenchimento branco e o vazio do motivo no Sinan com uma casa decimal (42,5% a 44,5%), como
o quadro de afirmações. Título, nota e fonte ficam no documento.

Uso: /opt/homebrew/bin/python3.11 dados/exposicao/fig_caminho_v05.py <saida.png>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "paper/figures"))
import make_figures as mf  # noqa: E402  (só funções e constantes; o módulo não desenha ao ser importado)
from make_figures import *  # noqa: E402,F401,F403

def _caixa(ax, x, y, w, h, txt, ec, fc, fs=MIN_PT, bold=False, cpl=15, tc=None):
    """Caixa arredondada com texto quebrado (coordenadas do eixo, em polegadas)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, "\n".join(textwrap.wrap(txt, cpl)), ha="center", va="center", fontsize=fs, color=tc or INK,
            fontweight="bold" if bold else "normal", linespacing=1.12)


def figura1_v05(saida) -> None:
    """Esquema 'O caminho do dado': onde cada fonte entra entre o fato e a contagem (sem escala)."""
    pns = ler_pns()["física"]
    f55 = [r for r in ler_csv("serie_campo55_uf_ano.csv") if r["uf"] == "BR"]
    falt = {int(r["ano"]): float(r["pct_m_ign"]) + float(r["pct_m_na"]) for r in f55}
    f_ini, f_lo, f_hi = falt[2015], min(falt[a] for a in (2023, 2024, 2025)), max(falt[a] for a in (2023, 2024, 2025))
    anu = {(r["edicao"], r["ano_dado"]): int(r["registros"]) for r in ler_csv("anuario_lgbtfobia_uf_ano_v2.csv") if r["uf"] == "BR" and r["registros"]}
    bo0, bo1 = anu[("2024", "2022")], anu[("2026", "2025")]
    ggb = {int(r["ano"]): int(r["ggb"]) for r in ler_csv("serie_ggb_vs_cobertura.csv") if r["ggb"] != ""}
    W, H = 7.4, 6.55
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W), ax.set_ylim(H, 0), ax.axis("off")
    x0, wc, gap = 1.2, 1.13, 0.1
    cx = [x0 + k * (wc + gap) for k in range(5)]
    etapas = ["1. Acontece", "2. A pessoa\nprocura serviço\nou polícia", "3. Fica\num papel", "4. Alguém\nclassifica o motivo\ne o grupo", "5. Sai a\ncontagem"]
    for k, e in enumerate(etapas):
        ax.text(cx[k] + wc / 2, 0.05, e, ha="center", va="top", fontsize=MIN_PT, fontweight="bold", color=INK)
    faixas = [
        ("PNS", "fonte_b", "pergunta direto à pessoa", None, None, None, f"{br(pns['lgb'], 2)}% x {br(pns['het'], 2)}%"),
        ("Sinan", "fonte_a", None, "procura serviço de saúde", "ficha de notificação", "profissional anota a orientação e o motivo",
         f"sem motivo útil: {br(f_ini, 1)}% (2015); {br(f_lo, 1)}% a {br(f_hi, 1)}% (2023-25)"),
        ("BO (Anuário)", "fonte_a", None, "vai à polícia", "boletim de ocorrência", "a polícia dá o enquadramento penal", f"{miles(bo0)} → {miles(bo1)} (2022-2025)"),
        ("Disque 100", "fonte_a", None, "liga e denuncia", "registro da denúncia", "o atendente classifica†", "só contagem de registros"),   # sem numero de figura: a numeracao e a do artigo
        ("SIM", "fonte_a", None, "morre", "declaração de óbito", "causa da morte, sim; orientação: nenhum campo", "sem número de LGBT+"),
        ("GGB", "ref", None, "vira notícia", "matéria", "quem coleta decide “é LGBT+” e o motivo", f"{ggb[2023]}, {ggb[2024]} e {ggb[2025]} (2023-2025)"),
    ]
    cor = {"fonte_b": (PALETA["fonte_b"], PALETA["fonte_b_cl"]), "fonte_a": (PALETA["fonte_a"], PALETA["fonte_a_cl"]), "ref": (PALETA["ref"], PALETA["ref_cl"])}
    rh, y0 = 0.64, 0.8
    for i, (nome, tipo, e1, e2, e3, e4, e5) in enumerate(faixas):
        y = y0 + i * (rh + 0.1)
        ec, fc = cor[tipo][0], "white"  # v0.5: fundo branco (pedido do autor, 2026-10-30)
        ax.text(0.1, y + rh / 2, nome, ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=ec)
        if e1:
            _caixa(ax, cx[0], y, wc, rh, e1, ec, fc)
            ax.annotate("", xy=(cx[4], y + rh / 2), xytext=(cx[0] + wc, y + rh / 2),
                        arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.8, "connectionstyle": "arc3,rad=-0.0", "linestyle": "--"})
            ax.text((cx[1] + cx[3] + wc) / 2, y + rh / 2 - 0.2, "pula as etapas 2 a 4", ha="center", va="center", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
            ax.text((cx[1] + cx[3] + wc) / 2, y + rh / 2 - 0.05 + 0.2, "não depende de a pessoa procurar ajuda", ha="center", va="center", fontsize=MIN_PT, color=INK)
            ax.text((cx[1] + cx[3] + wc) / 2, y + rh / 2 + 0.3, "a pessoa diz a orientação; sem motivo do agressor", ha="center", va="center", fontsize=MIN_PT, color=INK2)
        else:
            ax.plot([cx[0] + wc / 2], [y + rh / 2], "o", color=PALETA["sv"], ms=6)
            for k, txt in zip((1, 2, 3), (e2, e3, e4)):
                _caixa(ax, cx[k], y, wc, rh, txt, ec, fc, cpl=13 if (nome == "SIM" and k == 3) else 15)
                ax.annotate("", xy=(cx[k], y + rh / 2), xytext=(cx[k - 1] + (wc if k > 1 else wc / 2 + 0.08), y + rh / 2),
                            arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.4})
            ax.annotate("", xy=(cx[4], y + rh / 2), xytext=(cx[3] + wc, y + rh / 2), arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.4})
            if nome == "SIM":
                ax.text(cx[3] + wc - 0.13, y + 0.13, "✗", ha="center", va="center", fontsize=17, color=PALETA["nao"], fontweight="bold")
        _caixa(ax, cx[4], y, wc, rh, e5, ec, "white", bold=True, cpl=13 if len(e5) < 28 else 15)
    yb = y0 + 6 * (rh + 0.1) + 0.02
    ax.text(0.1, yb + 0.28, "Quem fica de fora", ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=INK)
    for k, txt in ((1, "quem não procurou serviço e quem não registrou"), (2, "o que não virou notícia"), (3, "o que ninguém anotou")):
        _caixa(ax, cx[k], yb, wc, 0.62, txt, PALETA["sv"], "white", cpl=15, tc=INK2)
    ax.text(0.05, yb + 0.82, "O TSE e o escore de ideologia dos partidos classificam governos; Câmara e Senado registram o que se diz.\nNenhum dos dois mede violência. † etapa não descrita neste artigo", ha="left", va="center", fontsize=MIN_PT, color=INK2)
    fig.savefig(saida, dpi=300, facecolor="white")
    print(saida)


if __name__ == "__main__":
    figura1_v05(Path(sys.argv[1]))
