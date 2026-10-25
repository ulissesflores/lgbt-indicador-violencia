"""Gera as Figuras 1 a 28 do paper a partir das copias de dados em `fontes/` (PDF + SVG + PNG).

Cada figura le arquivos de `fontes/` (procedencia e sha256 em `fontes/SOURCES.tsv`) e nada mais: nenhum
numero e digitado aqui (titulos e legendas usam f-strings sobre os dados lidos). Depois de desenhar, o script
le de volta os valores DOS PROPRIOS ARTISTAS do matplotlib (largura das barras, centro e extremos das barras
de erro, posicao dos quadrados) e grava em `valores_plotados.json`; `tests/test_figuras.py` confere esses
valores contra os arquivos de origem com um parser independente.

PADRAO VISUAL (v0.2). Toda figura passa por `moldura()`: titulo-conclusao em negrito, subtitulo (o que esta
plotado), cartao "Como ler" (linguagem comum), notas de termos tecnicos e rodape "Fonte:". Cores: dicionario
unico `PALETA` com nome semantico. Azul e laranja SO significam LGB+ e heterossexuais; estatistica (razao
bruta/ajustada, cenarios, estimativas) usa roxo/cinza-escuro e a FORMA do marcador (vazado = bruta, cheio =
ajustada); sexo usa verde-azulado e dourado; veredito, prioridade e fonte tem escalas proprias.

Claim-map (figura -> afirmacao do paper -> arquivo-fonte em `fontes/`):
  fig1  violencia fisica/sexual/qualquer LGB+ x hetero e razao                 -> seguro_pns2019.csv/.md
  fig2  cobertura implicita da contagem do GGB                                  -> c08_numeradores.csv
  fig3  painel de governadores e estudo de eventos                              -> c02_indet_resultados.csv, c03_event_pesos_resultados.csv
  fig4  funil de evidencia                                                      -> dashboard_extrato.json
  fig5  fontes por idioma e tipo                                                -> dashboard_extrato.json
  fig6  "1 em 7" x "1 em 26" (violencia fisica em 12 meses) + razao             -> seguro_pns2019.csv
  fig7  mapa pergunta x nivel N1-N4 com veredito por celula                     -> vereditos_tabela1_tabela5.tsv (trecho literal do v0.1)
  fig8  taxa de agressao padronizada, 4 grupos, media 2022-24                   -> asr_brasil.csv
  fig9  efeitos que o painel de governadores exclui (IC95%)                     -> c02_indet_resultados.csv
  fig10 tres incidencias, mesma serie de BOs (783 -> 3.481)                     -> sim_identificabilidade_resumo.json
  fig11 quatro frases no Parlamento e fonte primaria (1/49 literal; 0/49 sens.)             -> contagens.csv, r7_parlamento_sensibilidade.csv
  fig12 33 clusters da revisao hostil por lado e decisao                        -> TRIAGEM.csv
  fig13 PNS x Sinan: parcela LGB+ entre vitimas de violencia fisica             -> triangulacao_pns_sinan.md/.csv, c05_razao_direta.md, seguro_pns2019.md
  fig14 Sinan x Anuario por UF: concordancia some ao descontar o tamanho        -> concordancia_v2.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv, sidra_9514.json
  fig15 ideologia do governador x taxa de agressao (351 UF-anos), residuos      -> painel_uf_ano_tse_brc.csv, c02_indet_resultados.csv
  fig16 linha do tempo do que cada fonte cobre                                  -> asr_brasil.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv, serie_ggb_vs_cobertura.csv, cobertura_fontes.tsv
  fig17 tamanho de survey: o que a PNS 2019 detecta x o que se precisa          -> capacidade_por_opcao.csv, cenarios_n_custo.csv
  fig18 motivacao no Sinan por ano: o registro nao da incidencia                -> serie_campo55_uf_ano.csv
  fig19 GGB x homicidio por UF                                                  -> uf_2019.csv, inflacao_uf_serie.json
  fig20 serie nacional e trocas de presidente (2016, 2019, 2023) com placebo   -> c09_d1_resultados.csv, asr_brasil.csv
  fig21 alinhamento governador x presidente, 16 analises, efeito minimo        -> c09_d2_resultados.csv, RELATORIO-C09.md
  fig22 taxa nacional por governo (exposicao, sem atribuicao)                   -> c10_e1_federal.csv, c10_e1_serie_longo.csv
  fig23 67 trocas de governador, excesso relativo ao Brasil, referencia sem troca -> c10_e2_trocas_longo.csv, c10_e2_resumo.csv
  fig24 O caminho do dado (esquema das fontes)                                    -> seguro_pns2019.csv, serie_campo55_uf_ano.csv, anuario..., serie_ggb_vs_cobertura.csv
  fig25 mapa da evidencia internacional de mortalidade                            -> estudos_mortalidade.tsv (L-SECAO-3-3-PROPOSTA.md)
  fig26 verificabilidade da lista do GGB de 2019 (160 -> 50)                     -> ggb_validacao_resumo.json
  fig27 curva de hipoteses da cobertura do GGB                                    -> c08_numeradores.csv
  fig28 Disque 100: modulo LGBT, canal inteiro e quebras de serie (2011-2026)        -> d100_serie_anual.csv

Saidas deterministicas (sem data nos metadados, sal fixo no SVG): rodar duas vezes da os mesmos bytes;
`SHA256SUMS` lista todos os arquivos gerados.

Uso: /opt/homebrew/bin/python3.14 -I make_figures.py   (matplotlib 3.10, numpy)
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import textwrap
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

AQUI = Path(__file__).resolve().parent
FONTES = AQUI / "fontes"

# Dicionario unico de cores, por SIGNIFICADO. Contraste do texto: rotulo direto em tinta escura, nunca cor sozinha.
PALETA = {
    # grupos comparados (so aqui azul e laranja)
    "lgb": "#2a78d6", "lgb_cl": "#9ec5f4", "hetero": "#eb6834", "hetero_cl": "#f5b08f",
    # estatistica: estimativa, razao, cenario, fonte principal do dado
    "estat": "#6b3fa0", "estat_cl": "#cdbde6", "estat_esc": "#3f2468",
    "ref": "#4b4a46",          # cinza-escuro: referencia, linha de base, segunda estimativa
    "excl": "#e6e5e0",         # zona excluida, sombra
    # sexo (fig8, fig19): nunca azul/laranja
    "mulheres": "#1b8f8a", "mulheres_cl": "#9fd8d4", "homens": "#a87c0a", "homens_cl": "#e8cf86",
    # veredito
    "ok": "#1b8f66", "ok_bg": "#e3f5ee", "parcial": "#9a6a00", "parcial_bg": "#fbf0d4",
    "nao": "#b03a6e", "nao_bg": "#f8e6ee", "nt": "#4b4a46", "nt_bg": "#e4e3df", "sv": "#8b8a85", "sv_bg": "#f7f7f5",
    # prioridade (fig12)
    "p1": "#0f5e5a", "p2": "#6fc1b8", "p3": "#dcf1ee",
    # fontes de dado (fig13, fig14, fig16, fig18, fig19)
    "fonte_a": "#6b3fa0", "fonte_b": "#1b8f8a",
    # tipografia e fundo
    "ink": "#1f1f1e", "ink2": "#5b5a55", "grade": "#d9d8d3", "card": "#f3f2ee", "card_borda": "#d9d8d3",
}
INK, INK2, GRADE = PALETA["ink"], PALETA["ink2"], PALETA["grade"]
MIN_PT = 8

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.hashsalt": "lgbt-indicador-paper",
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

VALORES: dict = {}


def br(x: float, casas: int = 1) -> str:
    """Numero com virgula decimal (PT-BR), arredondado MEIO PARA CIMA (31,25 -> 31,3), como o texto do paper; nao o arredondamento do banqueiro do Python."""
    d = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)
    return f"{d:.{casas}f}".replace(".", ",")


def miles(n: float) -> str:
    """Inteiro com ponto de milhar (PT-BR)."""
    return f"{int(Decimal(repr(float(n))).quantize(Decimal(1), rounding=ROUND_HALF_UP)):,}".replace(",", ".")


def wilson(k: int, n: int) -> tuple[float, float]:
    """IC95% de Wilson para k de n (mesma formula usada nos scripts de origem)."""
    z, p = 1.959963984540054, k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def ler_tsv(nome: str) -> list[dict]:
    """TSV de `fontes/` como lista de dicts."""
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8"), delimiter="\t"))


def ler_csv(nome: str) -> list[dict]:
    """CSV de `fontes/` como lista de dicts."""
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8")))


def salvar(fig, nome: str) -> None:
    """Grava PDF, SVG e PNG (300 dpi, para o DOCX) sem data nos metadados."""
    kw = {"bbox_inches": "tight", "pad_inches": 0.12}
    fig.savefig(AQUI / f"{nome}.pdf", metadata={"CreationDate": None, "ModDate": None}, **kw)
    fig.savefig(AQUI / f"{nome}.svg", metadata={"Date": None}, **kw)
    fig.savefig(AQUI / f"{nome}.png", dpi=300, metadata={"Software": None}, **kw)
    plt.close(fig)


def erros_de(eb) -> list[list[float]]:
    """Extremos (lo, hi) de cada barra de erro horizontal, lidos dos segmentos desenhados."""
    segs = eb.lines[2][0].get_segments()
    return [[float(s[0][0]), float(s[1][0])] for s in segs]


# ---------------------------------------------------------------- moldura padrao (G2, G3, G4)
CPI_CORPO, CPI_TITULO, CPI_SUB = 16.0, 9.8, 15.0     # caracteres por polegada (DejaVu Sans, 8,2 / 12 / 8,8 pt)


def _quebra(txt: str, largura_in: float, cpi: float) -> list[str]:
    return textwrap.wrap(txt, max(20, int(largura_in * cpi)))


def moldura(fig, titulo: str, subtitulo: str, como_ler: str, termos: str, fonte: str) -> None:
    """Titulo-conclusao + subtitulo no alto; cartao 'Como ler' + termos + rodape 'Fonte:' embaixo.

    Mede o conteudo ja desenhado (get_tightbbox) e empilha a moldura fora dele. As posicoes sao
    calculadas em polegadas e convertidas para fracao da figura (transFigure), porque o
    `bbox_inches='tight'` do `salvar` desloca transFigure e nao desloca coordenadas em polegadas.
    Texto da moldura >= 8 pt.
    """
    fig.canvas.draw()
    tb = fig.get_tightbbox(fig.canvas.get_renderer())
    x0, y0, y1 = float(tb.x0), float(tb.y0), float(tb.y1)
    W, H = fig.get_size_inches()
    w = max(float(tb.x1) - x0, 6.9)
    fx = lambda v: v / W   # noqa: E731
    fy = lambda v: v / H   # noqa: E731
    lt, ls, lc = _quebra(titulo, w, CPI_TITULO), _quebra(subtitulo, w, CPI_SUB), _quebra(como_ler, w - 0.3, CPI_CORPO)
    ln = _quebra(termos, w - 0.3, CPI_CORPO) if termos else []
    ht, hs, hl = 0.205 * len(lt), 0.155 * len(ls), 0.142
    topo = y1 + 0.14 + hs + 0.05 + ht
    fig.text(fx(x0), fy(topo), "\n".join(lt), ha="left", va="top", fontsize=12, fontweight="bold", color=INK, linespacing=1.15)
    fig.text(fx(x0), fy(topo - ht - 0.04), "\n".join(ls), ha="left", va="top", fontsize=8.8, color=INK2)
    hcard = 0.1 + 0.17 + hl * len(lc) + (0.08 + 0.17 + hl * len(ln) if ln else 0) + 0.1
    ytop = y0 - 0.16
    r = 0.08
    fig.add_artist(FancyBboxPatch((fx(x0), fy(ytop - hcard)), fx(w), fy(hcard), boxstyle=f"round,pad=0,rounding_size={r / W}",
                                  mutation_aspect=W / H, transform=fig.transFigure, fc=PALETA["card"], ec=PALETA["card_borda"], lw=0.8))
    y = ytop - 0.1
    fig.text(fx(x0 + 0.13), fy(y), "Como ler", ha="left", va="top", fontsize=8.6, fontweight="bold", color=INK)
    fig.text(fx(x0 + 0.13), fy(y - 0.17), "\n".join(lc), ha="left", va="top", fontsize=8.2, color=INK, linespacing=1.18)
    if ln:
        y2 = y - 0.17 - hl * len(lc) - 0.08
        fig.text(fx(x0 + 0.13), fy(y2), "Termos", ha="left", va="top", fontsize=8.6, fontweight="bold", color=INK)
        fig.text(fx(x0 + 0.13), fy(y2 - 0.17), "\n".join(ln), ha="left", va="top", fontsize=8.2, color=INK2, linespacing=1.18)
    fig.text(fx(x0), fy(ytop - hcard - 0.07), "\n".join(_quebra("Fonte: " + fonte, w, CPI_CORPO + 0.8)), ha="left", va="top", fontsize=8,
             color=INK2)


def seta(ax, texto: str, alvo: tuple, ponto_texto: tuple, **kw) -> None:
    """Anotacao com seta para a mensagem principal (texto em tinta escura, seta cinza)."""
    ax.annotate(texto, xy=alvo, xytext=ponto_texto, fontsize=MIN_PT + 0.5, color=INK, fontweight="bold",
                arrowprops={"arrowstyle": "->", "color": INK2, "lw": 1.3, "shrinkA": 2, "shrinkB": 3,
                            "connectionstyle": "arc3,rad=0.15"}, **kw)


def estat_cheio(ax, x, y, **kw):
    """Marcador de estatistica 'ajustada/estimativa': quadrado cheio roxo."""
    return ax.errorbar(x, y, fmt="s", ms=6.5, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=2, capsize=3, **kw)


def estat_vazado(ax, x, y, **kw):
    """Marcador de estatistica 'bruta': circulo vazado roxo."""
    return ax.errorbar(x, y, fmt="o", ms=7, mfc="white", mec=PALETA["estat"], mew=1.8, color=PALETA["estat"],
                       ecolor=PALETA["estat"], elinewidth=2, capsize=3, **kw)


NOME_PNS = "Pesquisa Nacional de Saúde (PNS 2019, IBGE)"
GLOSSARIO_PNS = ("LGB+ = lésbicas, gays, bissexuais e outras orientações · PNS = Pesquisa Nacional de Saúde do IBGE · "
                 "IC95% = faixa em que o valor verdadeiro provavelmente está · razão = quantas vezes mais")


# ---------------------------------------------------------------- Figura 1: PNS 2019
def ler_pns() -> dict:
    """Prevalencias e razoes (CSV) + IC das prevalencias (tabela 1 do .md gerado pelo mesmo script)."""
    rows = ler_csv("seguro_pns2019.csv")
    out: dict = {}
    for r in rows:
        if r["bloco"] == "nivel":
            out.setdefault(r["rotulo"], {}).update(
                lgb=100 * float(r["prev_grupo"]), het=100 * float(r["prev_ref"]),
                rp=float(r["rp"]), rp_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
        elif r["bloco"] == "rp_ajustada":
            out[r["rotulo"]].update(rpaj=float(r["rp"]), rpaj_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
    md = (FONTES / "seguro_pns2019.md").read_text(encoding="utf-8")
    sec = md.split("## 1.")[1].split("## 2.")[0]
    for linha in sec.splitlines():
        m = re.match(r"\| (física|sexual|psicológica|qualquer) \| ([\d.]+)% \[([\d.]+); ([\d.]+)\] \| "
                     r"([\d.]+)% \[([\d.]+); ([\d.]+)\]", linha)
        if m:
            k = m.group(1)
            out[k].update(het_ic=[float(m.group(3)), float(m.group(4))], lgb_ic=[float(m.group(6)), float(m.group(7))])
    return out


def n_adultos_pns() -> int:
    """Adultos da PNS 2019 (linha B' da tabela de capacidade)."""
    return int(next(r["adultos"] for r in ler_csv("capacidade_por_opcao.csv") if r["indicador"] == "fisica" and "PNS 2019" in r["opcao"]))


def figura1() -> None:
    """Prevalencia em 12 meses (LGB+ x hetero) e razao de prevalencias bruta e ajustada."""
    d = ler_pns()
    ordem = ["física", "sexual", "qualquer"]
    nomes = {"física": "Física", "sexual": "Sexual", "qualquer": "Qualquer tipo"}
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.5), gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.38})
    y = list(range(len(ordem)))[::-1]
    off = 0.16
    for grupo, cor, dy, rot in (("lgb", PALETA["lgb"], off, "LGB+"), ("het", PALETA["hetero"], -off, "Heterossexuais")):
        xs = [d[k][grupo] for k in ordem]
        lo = [d[k][grupo] - d[k][grupo + "_ic"][0] for k in ordem]
        hi = [d[k][grupo + "_ic"][1] - d[k][grupo] for k in ordem]
        eb = a.errorbar(xs, [v + dy for v in y], xerr=[lo, hi], fmt="o", ms=5.5, color=cor,
                        ecolor=cor, elinewidth=1.8, capsize=2.5, label=rot)
        VALORES.setdefault("fig1", {})[grupo] = {
            "pontos": [float(v) for v in eb.lines[0].get_xdata()], "ic": erros_de(eb)}
        for k, xv, yv in zip(ordem, xs, y):
            a.annotate(f"{br(xv, 2)}%", (d[k][grupo + "_ic"][1], yv + dy), xytext=(4, -3),
                       textcoords="offset points", fontsize=MIN_PT, color=INK)
    a.set_yticks(y, [nomes[k] for k in ordem], fontsize=9)
    a.set_xlabel("Adultos que sofreram violência em 12 meses (%)", fontsize=MIN_PT + 0.5)
    a.set_xlim(-2, 60)
    a.set_xticks([0, 10, 20, 30, 40, 50, 60])
    a.tick_params(labelsize=MIN_PT)
    a.grid(axis="x", color=GRADE, lw=0.6)
    a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=MIN_PT + 0.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    a.set_title("(a) Quantos sofreram", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    a.set_ylim(-0.6, 2.75)
    seta(a, f"{br(d['física']['rp'], 1)} vezes mais", (d["física"]["lgb"] + 0.6, y[0] + off + 0.12), (27, y[0] + 0.5), va="center")
    for tipo, mk, rot in (("rp", "o", "razão bruta"), ("rpaj", "s", "razão ajustada")):
        dy = off if tipo == "rp" else -off
        xs = [d[k][tipo] for k in ordem]
        lo = [d[k][tipo] - d[k][tipo + "_ic"][0] for k in ordem]
        hi = [d[k][tipo + "_ic"][1] - d[k][tipo] for k in ordem]
        fn = estat_vazado if tipo == "rp" else estat_cheio
        eb = fn(b, xs, [v + dy for v in y], xerr=[lo, hi], label=rot)
        VALORES["fig1"][tipo] = {"pontos": [float(v) for v in eb.lines[0].get_xdata()], "ic": erros_de(eb)}
        for k, xv, yv in zip(ordem, xs, y):
            b.annotate(br(xv, 2), (d[k][tipo + "_ic"][1], yv + dy), xytext=(4, -3),
                       textcoords="offset points", fontsize=MIN_PT, color=INK)
    b.set_xscale("log")
    b.axvline(1, color=INK2, lw=0.9, ls="--")
    b.text(1.05, y[0] + 0.5, "1 = igual", fontsize=MIN_PT, color=INK2, va="bottom")
    b.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"])
    b.set_xlim(0.8, 22)
    b.set_ylim(a.get_ylim())
    b.set_yticks(y, [nomes[k] for k in ordem], fontsize=9)
    b.set_xlabel("Quantas vezes mais entre LGB+ (escala log)", fontsize=MIN_PT + 0.5)
    b.tick_params(labelsize=MIN_PT)
    b.grid(axis="x", color=GRADE, lw=0.6)
    b.set_axisbelow(True)
    b.legend(frameon=False, fontsize=MIN_PT + 0.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    b.set_title("(b) A razão entre os dois grupos", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    f = d["física"]
    moldura(fig, f"Adultos LGB+ sofrem violência física {br(f['rp'], 1)} vezes mais que heterossexuais, e a diferença não some ao descontar idade, cor e instrução",
            "Brasil, adultos de 18 anos ou mais, últimos 12 meses; três tipos de violência; barras = IC95%",
            "No painel (a), cada ponto é a parte dos adultos do grupo que sofreu violência no último ano (azul: LGB+; laranja: heterossexuais). "
            "No painel (b), cada símbolo diz quantas vezes a violência é mais comum entre LGB+: 1 = igual; quanto mais à direita, maior a diferença. "
            "O círculo vazado é o número direto; o quadrado cheio é o número depois de descontar diferenças entre os grupos.",
            GLOSSARIO_PNS + f" · PNS = {miles(n_adultos_pns())} adultos · ajustada = descontando sexo, idade, cor, instrução, região e zona urbana ou rural · "
            "“Qualquer tipo” = física, sexual ou psicológica",
            "paper/figures/fontes/seguro_pns2019.csv (origem dados/pns/seguro_pns2019.csv), desenho amostral complexo.")
    salvar(fig, "fig1_pns2019_vitimizacao")


# ---------------------------------------------------------------- Figura 2: cobertura do GGB
def ler_c08() -> list[dict]:
    """Linhas do teste de escala com desfecho agressao e prevalencia 1,89%, anos com SIM (2023, 2024)."""
    rows = ler_csv("c08_numeradores.csv")
    return [r for r in rows if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False"]


def figura2() -> None:
    """Cobertura implicita (n / esperado) por ano, numerador e cenario de risco relativo."""
    rows = ler_c08()
    nomes = {"N0": "total declarado", "N1": "numerador A: homicídios e latrocínios", "N2": "numerador B: cenário de subtração (sem pessoas trans)"}
    fig = plt.figure(figsize=(7.2, 4.4))
    ax = fig.add_subplot(111)
    h = 0.27
    rrs = [("cob_RR1.0", "risco igual ao dos pares", PALETA["estat_esc"]),
           ("cob_RR2.82", "risco 2,82 vezes maior", PALETA["estat"]),
           ("cob_RR3.84", "risco 3,84 vezes maior", PALETA["estat_cl"])]
    ys, rotulos = [], []
    for i, r in enumerate(rows):
        ys.append(len(rows) - 1 - i)
        rotulos.append(f"{r['ano']} · {nomes[r['numerador']]}\n{r['n']} declaradas; esperadas: {miles(float(r['E_RR1.0']))}")
    VALORES["fig2"] = {"linhas": [f"{r['ano']}-{r['numerador']}" for r in rows]}
    for j, (col, rot, cor) in enumerate(rrs):
        vals = [100 * float(r[col]) for r in rows]
        bars = ax.barh([y + (1 - j) * h for y in ys], vals, height=h - 0.03, color=cor, label=rot)
        VALORES["fig2"][col] = [float(p.get_width()) for p in bars]
        for p, v in zip(bars, vals):
            ax.text(v + 0.4, p.get_y() + p.get_height() / 2, f"{br(v)}%", va="center", fontsize=MIN_PT, color=INK)
    ax.set_yticks(ys, rotulos, fontsize=MIN_PT)
    ax.set_xlabel("Mortes declaradas ÷ mortes esperadas (%)", fontsize=MIN_PT + 0.5)
    ax.set_xlim(0, 36)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.grid(axis="x", color=GRADE, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.36, -0.14), ncol=3,
              title="Se adultos LGB+ tivessem este risco de morte por agressão…", title_fontsize=MIN_PT)
    r0 = rows[0]
    seta(ax, f"{r0['n']} contadas de {miles(float(r0['E_RR1.0']))} esperadas\n= {br(100 * float(r0['cob_RR1.0']))}%",
         (100 * float(r0["cob_RR1.0"]) + 3.4, ys[0] + h), (28, ys[0] + 0.95), va="center")
    top = max(100 * float(r["cob_RR1.0"]) for r in rows)
    moldura(fig, f"Nos cenários exibidos, a razão entre a contagem do GGB e as mortes esperadas chega a {br(top)}% se LGB+ morressem como seus pares; não estima a cobertura real",
            "Mortes declaradas pelo Grupo Gay da Bahia ÷ mortes esperadas, por ano, tipo de contagem e risco suposto",
            "Cada grupo de três barras compara o número que o GGB contou com o que se esperaria se adultos LGB+ morressem por agressão no mesmo ritmo "
            "(ou 2,82 e 3,84 vezes mais) que pessoas do mesmo sexo, raça e idade. Barra curta = a contagem está longe de cobrir todas as mortes. "
            "Isto mede escala, não conta mortes de LGB+; o numerador B é um cenário de subtração, não um limite inferior.",
            "GGB = Grupo Gay da Bahia, associação que conta mortes de LGBT+ a partir de notícias · pares = pessoas do mesmo sexo, raça e faixa de idade · "
            "latrocínio = roubo seguido de morte · “sem pessoas trans” porque a base de comparação (PNS) só pergunta orientação sexual · "
            "esperadas = taxa de agressão dos pares × adultos LGB+ (1,89% dos adultos, PNS 2019)",
            "paper/figures/fontes/c08_numeradores.csv (origem dados/ggb/c08_numeradores.csv), prevalência LGB+ de 1,89%.")
    salvar(fig, "fig2_ggb_cobertura_implicita")


# ---------------------------------------------------------------- Figura 3: governos
def pct5(b: float) -> float:
    """Variacao exata da taxa (%) numa troca de 5 pontos de ideologia: 100[exp(5b)-1]."""
    return 100 * (math.exp(5 * b) - 1)


def ler_c02() -> dict:
    """b e IC95% por grupo e desfecho do painel TWFE (registrado e agressao+indeterminada)."""
    out: dict = {}
    for r in ler_csv("c02_indet_resultados.csv"):
        if r["desfecho"] in ("registrado_ln", "agressao_mais_indet_ln"):
            out[(r["grupo"], r["desfecho"])] = (float(r["b"]), float(r["ic_lo"]), float(r["ic_hi"]))
    return out


def ler_c03() -> list[dict]:
    """Media dos pos-periodos (log-pontos) do estudo de eventos empilhado, desfecho total, painel BRC."""
    rows = ler_csv("c03_event_pesos_resultados.csv")
    return [r for r in rows if r["painel"] == "BRC (principal)" and r["desfecho"] == "tx_total"]


def figura3() -> None:
    """(a) limites do painel continuo numa troca de 5 pontos; (b) estudo de eventos (inconclusivo)."""
    c02 = ler_c02()
    grupos = ["total", "homens", "mulheres", "negros", "nao_negros", "arma"]
    nomes = {"total": "Total", "homens": "Homens", "mulheres": "Mulheres", "negros": "Negros",
             "nao_negros": "Não negros", "arma": "Arma de fogo"}
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.2, 6.9), gridspec_kw={"height_ratios": [1.3, 1], "hspace": 0.62})
    y = list(range(len(grupos)))[::-1]
    off = 0.15
    VALORES["fig3"] = {}
    for desf, fn, dy, rot in (("registrado_ln", estat_cheio, off, "mortes por agressão registradas"),
                              ("agressao_mais_indet_ln", estat_vazado, -off, "agressão + causa indeterminada")):
        gs = [g for g in grupos if (g, desf) in c02]
        yy = [y[grupos.index(g)] + dy for g in gs]
        pts = [pct5(c02[(g, desf)][0]) for g in gs]
        lo = [pct5(c02[(g, desf)][0]) - pct5(c02[(g, desf)][1]) for g in gs]
        hi = [pct5(c02[(g, desf)][2]) - pct5(c02[(g, desf)][0]) for g in gs]
        eb = fn(a, pts, yy, xerr=[lo, hi], label=rot)
        VALORES["fig3"][desf] = {"grupos": gs, "pontos": [float(v) for v in eb.lines[0].get_xdata()], "ic": erros_de(eb)}
        if desf == "registrado_ln":
            for g, (l_, h_), yv in zip(gs, erros_de(eb), yy):
                a.annotate(f"{br(l_)}% a +{br(h_)}%", (h_, yv), xytext=(5, -3), textcoords="offset points", fontsize=MIN_PT, color=INK)
    a.axvline(0, color=INK2, lw=0.9, ls="--")
    a.set_yticks(y, [nomes[g] for g in grupos], fontsize=9)
    a.set_xlim(-24, 40)
    a.tick_params(axis="x", labelsize=MIN_PT)
    a.set_xlabel("Variação da taxa ao trocar o governador do PT por DEM ou PL (5 pontos de ideologia), %", fontsize=MIN_PT)
    a.grid(axis="x", color=GRADE, lw=0.6)
    a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2)
    a.set_title("(a) Painel por estado e ano", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    seta(a, "a faixa inclui zero:\nnão se enxerga efeito", (0.6, y[0] + off + 0.25), (15, y[0] + 0.85), va="center")

    c03 = ler_c03()
    lado = {"esquerda->direita": "de esquerda para direita", "direita->esquerda": "de direita para esquerda"}
    jan = {"estrito": "janela completa", "truncado": "janela curta"}
    rot_ev, pts, lo, hi = [], [], [], []
    for r in c03:
        p = float(r["p_antecipacoes"])
        aviso = f"já mudava antes da troca (p = {br(p, 3)})" if p < 0.05 else f"sem mudança antes da troca (p = {br(p, 2)})"
        rot_ev.append(f"{lado[r['direcao']]}, {jan[r['desenho']]}\n{r['n_eventos']} trocas; {aviso}")
        m, l_, h_ = (100 * (math.exp(float(r[k])) - 1) for k in ("media_pos", "media_pos_lo", "media_pos_hi"))
        pts.append(m), lo.append(m - l_), hi.append(h_ - m)
    yb = list(range(len(c03)))[::-1]
    eb = estat_cheio(b, pts, yb, xerr=[lo, hi])
    VALORES["fig3"]["event_study"] = {"rotulos": [f"{r['desenho']}|{r['direcao']}" for r in c03],
                                      "pontos": [float(v) for v in eb.lines[0].get_xdata()], "ic": erros_de(eb)}
    for xv, yv in zip(pts, yb):
        b.annotate(f"{br(xv)}%", (xv, yv), xytext=(0, 7), textcoords="offset points", fontsize=MIN_PT, color=INK, ha="center")
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_yticks(yb, rot_ev, fontsize=MIN_PT)
    b.set_xlim(-40, 10)
    b.set_ylim(-0.6, 3.75)
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel("Variação média da taxa nos anos depois da troca, comparada a estados sem troca (%)", fontsize=MIN_PT)
    b.grid(axis="x", color=GRADE, lw=0.6)
    b.set_axisbelow(True)
    b.set_title("(b) Antes e depois de uma troca de lado: sinais contraditórios", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    t = c02[("total", "registrado_ln")]
    moldura(fig, f"O painel de governadores só descarta efeitos fora de {br(pct5(t[1]))}% a +{br(pct5(t[2]))}% na taxa de homicídios; dentro dessa faixa não distingue nada",
            "Variação da taxa de morte por agressão ao trocar o partido do governador, por grupo (a) e em trocas reais de lado (b)",
            "Em (a), cada ponto é a melhor estimativa e a barra é a faixa compatível com os dados: se ela passa por zero, o painel não consegue dizer se houve efeito. "
            "Em (b), olha-se a taxa nos anos antes e depois de cada troca de lado: a queda aparece nas duas direções, e em duas das quatro análises a taxa já mudava antes da troca, "
            "o que impede ler a queda como efeito do governador.",
            "painel = 351 combinações de estado e ano (2012-2024) · IC95% = faixa em que o efeito verdadeiro provavelmente está · "
            "janela completa = acompanha 3 anos antes e depois, só com trocas limpas; janela curta = recorte menor, com mais trocas · "
            "p = chance de ver tamanha mudança antes da troca se nada estivesse acontecendo (p < 0,05 invalida a leitura causal) · "
            "causa indeterminada = óbitos sem causa definida (CID-10 Y10-Y34)",
            "paper/figures/fontes/c02_indet_resultados.csv e c03_event_pesos_resultados.csv (origem dados/painel/). Exploratório, não causal.")
    salvar(fig, "fig3_governos_painel_eventos")


# ---------------------------------------------------------------- Figuras 4 e 5: fontes
def ler_dashboard() -> dict:
    """Extrato publico dos numeros do painel de publicacao."""
    return json.loads((FONTES / "dashboard_extrato.json").read_text(encoding="utf-8"))


def figura4() -> None:
    """Funil de evidencia em escala linear: registradas -> texto integral -> Q1 -> usadas."""
    f = ler_dashboard()["funil"]
    etapas = [("registradas", "Fontes únicas registradas"), ("lido", "Texto integral lido\n(artigos com DOI)"),
              ("q1_lido", "Lidas e em periódico\nde primeira linha (Q1)"), ("q1_usado", "Q1 lidas e usadas\nem alguma conclusão")]
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    vals = [f[k] for k, _ in etapas]
    y = list(range(len(etapas)))[::-1]
    bars = ax.barh(y, vals, height=0.62, color=PALETA["estat"])
    VALORES["fig4"] = {"etapas": [k for k, _ in etapas], "larguras": [float(p.get_width()) for p in bars]}
    for p, v in zip(bars, vals):
        ax.text(v + 10, p.get_y() + p.get_height() / 2, f"{v}  ({br(100 * v / vals[0])}% das registradas)", va="center", fontsize=MIN_PT + 0.5, color=INK)
    ax.set_yticks(y, [r for _, r in etapas], fontsize=MIN_PT + 0.5)
    ax.set_xlim(0, 1250)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.set_xlabel("Número de fontes (escala linear)", fontsize=MIN_PT + 0.5)
    ax.grid(axis="x", color=GRADE, lw=0.6)
    ax.set_axisbelow(True)
    seta(ax, "o funil afunila rápido:\nler por inteiro é o gargalo", (vals[1] * 0.55, y[1] - 0.33), (430, y[2] - 0.05), va="center")
    moldura(fig, f"Das {vals[0]} fontes registradas, só {vals[3]} são artigos de primeira linha lidos por inteiro e usados em conclusões",
            "Fontes únicas do projeto, de 10 a 23 de outubro de 2026, em quatro etapas",
            "Cada barra é quantas fontes sobraram depois de um filtro mais exigente. A primeira é tudo o que foi registrado; a última é só o que foi lido por inteiro, "
            "está num periódico de primeira linha e sustentou alguma conclusão. A queda mostra por que o paper separa o que leu do que apenas encontrou.",
            "fonte única = mesmo DOI ou endereço, contado uma vez · Q1 = o melhor quarto dos periódicos da área, segundo o ranking SJR · "
            "texto integral = o artigo inteiro foi lido, não só o resumo",
            "paper/figures/fontes/dashboard_extrato.json (origem dashboard/dashboard_dados.publico.json).")
    salvar(fig, "fig4_funil_evidencia")


def figura5() -> None:
    """Fontes unicas por idioma e por tipo (cada painel soma o total de fontes unicas)."""
    d = ler_dashboard()
    tipos_nome = {"oficial": "Oficial / governamental", "per_semq": "Periódico, quartil\nainda não conferido",
                  "per_q1": "Periódico Q1 conferido", "ong": "Sociedade civil (ONG)", "dado": "Base de dados",
                  "imprensa": "Imprensa", "enciclopedia": "Enciclopédia", "nao_classificado": "Não classificado",
                  "preprint": "Preprint (sem revisão)", "per_q2": "Periódico Q2", "livro": "Livro",
                  "per_q34": "Periódico Q3-Q4"}
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.9), gridspec_kw={"wspace": 0.7})
    idi = sorted(d["idiomas"].items(), key=lambda kv: -kv[1])
    ya = list(range(len(idi)))[::-1]
    ba = a.barh(ya, [v for _, v in idi], height=0.62, color=PALETA["estat"])
    for p, (_, v) in zip(ba, idi):
        a.text(v + 6, p.get_y() + p.get_height() / 2, str(v), va="center", fontsize=MIN_PT, color=INK)
    a.set_yticks(ya, [k for k, _ in idi], fontsize=MIN_PT + 0.5)
    a.set_xlim(0, 450)
    a.tick_params(axis="x", labelsize=MIN_PT)
    a.set_title(f"(a) Por idioma (n = {d['fontes_unicas']})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    a.grid(axis="x", color=GRADE, lw=0.6)
    a.set_axisbelow(True)
    tp = sorted(d["tipos"].items(), key=lambda kv: -kv[1])
    yb = list(range(len(tp)))[::-1]
    destaque = {"per_q1", "per_semq"}
    bb = b.barh(yb, [v for _, v in tp], height=0.62, color=[PALETA["estat"] if k in destaque else PALETA["estat_cl"] for k, _ in tp])
    for p, (_, v) in zip(bb, tp):
        b.text(v + 6, p.get_y() + p.get_height() / 2, str(v), va="center", fontsize=MIN_PT, color=INK)
    b.set_yticks(yb, [tipos_nome[k] for k, _ in tp], fontsize=MIN_PT)
    b.set_xlim(0, 360)
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_title(f"(b) Por tipo (n = {sum(d['tipos'].values())})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    b.grid(axis="x", color=GRADE, lw=0.6)
    b.set_axisbelow(True)
    VALORES["fig5"] = {"idiomas": {k: float(p.get_width()) for (k, _), p in zip(idi, ba)},
                       "tipos": {k: float(p.get_width()) for (k, _), p in zip(tp, bb)}}
    iq = list(dict(tp)).index("per_semq")
    seta(b, f"{d['tipos']['per_q1']} têm quartil conferido;\n{d['tipos']['per_semq']} ainda não", (d["tipos"]["per_semq"] * 0.9, yb[iq] - 0.05),
         (190, yb[iq] - 2.4), va="center")
    moldura(fig, f"{d['idiomas']['Inglês']} das {d['fontes_unicas']} fontes estão em inglês e {d['idiomas']['Português']} em português; só {d['tipos']['per_q1']} são periódicos de primeira linha conferidos",
            "Fontes únicas por idioma (a) e por tipo (b); cada painel soma o total de fontes",
            "Cada barra conta fontes. Em (a), o idioma do texto; em (b), de que tipo de fonte se trata. As barras roxas fortes em (b) destacam os periódicos: "
            "os 'Q1 conferido' passaram no teste do paper e os de 'quartil ainda não conferido' aparecem com aviso e não decidem nenhuma conclusão.",
            "quartil Q1 = o melhor quarto dos periódicos da área (ranking SJR, 2023-2025) · oficial = governo e organismos internacionais · "
            "ONG = organização da sociedade civil · preprint = texto ainda sem revisão por pares · pt e pt-BR somados em Português",
            "paper/figures/fontes/dashboard_extrato.json (origem dashboard/dashboard_dados.publico.json).")
    salvar(fig, "fig5_fontes_idioma_tipo")


# ---------------------------------------------------------------- Figura 6: 1 em 7 x 1 em 26
def figura6() -> None:
    """Quadradinhos (100 por grupo) da violencia fisica em 12 meses + razao de prevalencias bruta e ajustada."""
    d = ler_pns()["física"]
    fig = plt.figure(figsize=(7.2, 3.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.45], wspace=0.22, left=0.01, right=0.985, top=0.9, bottom=0.14)
    VALORES["fig6"] = {}
    for col, (chave, cor, nome) in enumerate((("lgb", PALETA["lgb"], "LGB+"), ("het", PALETA["hetero"], "Heterossexuais"))):
        ax = fig.add_subplot(gs[0, col])
        prev = d[chave]
        for i in range(100):
            r, c = divmod(i, 10)
            ax.add_patch(Rectangle((c + 0.06, r + 0.06), 0.88, 0.88, fc=PALETA["excl"], ec="none"))
            frac = min(max(prev - i, 0.0), 1.0)
            if frac > 0:
                ax.add_patch(Rectangle((c + 0.06, r + 0.06), 0.88 * frac, 0.88, fc=cor, ec="none", gid="cheio"))
        ax.set_xlim(0, 10), ax.set_ylim(0, 10), ax.set_aspect("equal"), ax.axis("off")
        VALORES["fig6"][chave] = {"fracoes": [float(p.get_width() / 0.88) for p in ax.patches if p.get_gid() == "cheio"],
                                  "um_em": int(round(100 / prev))}
        ax.text(5, 12.6, nome, ha="center", va="bottom", fontsize=10, color=INK, fontweight="bold")
        ax.text(5, 10.5, f"{br(prev, 2)}%", ha="center", va="bottom", fontsize=15, color=cor, fontweight="bold")
        ax.text(5, -0.6, f"cerca de 1 em {VALORES['fig6'][chave]['um_em']}", ha="center", va="top", fontsize=10.5, color=INK, fontweight="bold")
        ax.text(5, -2.0, "cada quadrado = 1 em 100 adultos", ha="center", va="top", fontsize=MIN_PT, color=INK2)
    ax = fig.add_subplot(gs[0, 2])
    pontos, ics = [], []
    for y, (tipo, fn, rot) in zip((1, 0), (("rp", estat_vazado, "razão direta (bruta)"), ("rpaj", estat_cheio, "razão ajustada"))):
        v, (lo, hi) = d[tipo], d[tipo + "_ic"]
        eb = fn(ax, [v], [y], xerr=[[v - lo], [hi - v]])
        pontos.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0])
        ax.text(v, y + 0.24, f"{br(v, 2)} vezes", ha="center", va="bottom", fontsize=11.5, color=INK, fontweight="bold")
        ax.text(v, y - 0.2, f"{rot}\nIC95% {br(lo, 2)} a {br(hi, 2)}", ha="center", va="top", fontsize=MIN_PT, color=INK2)
    VALORES["fig6"]["rp"] = {"pontos": pontos, "ic": ics}
    ax.axvline(1, color=INK2, lw=0.9, ls="--")
    ax.text(1.05, 1.62, "1 = risco igual", fontsize=MIN_PT, color=INK2, va="bottom")
    ax.set_xlim(0, 6.2), ax.set_ylim(-0.95, 1.85)
    ax.set_yticks([])
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax.tick_params(labelsize=MIN_PT)
    ax.set_xlabel("Quantas vezes mais entre LGB+", fontsize=MIN_PT + 0.5)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=GRADE, lw=0.6)
    ax.set_title("Quantas vezes mais", loc="left", fontsize=10, color=INK, fontweight="bold")
    moldura(fig, f"1 em {VALORES['fig6']['lgb']['um_em']} adultos LGB+ sofreu violência física em um ano, contra 1 em {VALORES['fig6']['het']['um_em']} heterossexuais",
            "Violência física nos últimos 12 meses, adultos de 18 anos ou mais (PNS 2019)",
            "Os dois quadriculados têm 100 quadrados cada: os coloridos mostram quantos adultos de cada grupo, em cada 100, sofreram violência física no último ano "
            "(azul: LGB+; laranja: heterossexuais). À direita, a razão diz quantas vezes mais é comum entre LGB+: 1 seria igual. "
            "O círculo vazado é o número direto; o quadrado cheio é o número depois de descontar diferenças de sexo, idade, cor, instrução, região e zona.",
            GLOSSARIO_PNS + f" · PNS = {miles(n_adultos_pns())} adultos entrevistados",
            "paper/figures/fontes/seguro_pns2019.csv (origem dados/pns/seguro_pns2019.csv).")
    salvar(fig, "fig6_proporcao_1_em_7")


# ---------------------------------------------------------------- Figura 7: mapa de respostas
ESTILO_VEREDITO = {
    "sustentada": (PALETA["ok"], PALETA["ok_bg"], "✓"),
    "parcial": (PALETA["parcial"], PALETA["parcial_bg"], "◐"),
    "não sustentada pelo que foi medido": (PALETA["nao"], PALETA["nao_bg"], "✗"),
    "não testável": (PALETA["nt"], PALETA["nt_bg"], "?"),
    "sem veredito": (PALETA["sv"], PALETA["sv_bg"], "–"),
}
ROTULO_VEREDITO = {"sem veredito": "sem veredito (só descrito)"}
PERGUNTAS_MAPA = {"L1": "LGB+ sofrem mais violência não letal que heterossexuais?",
                  "L2": "Gays morrem mais que héteros?",
                  "L3": "Mulheres e negros: dá para saber?"}


def figura7() -> None:
    """Matriz pergunta x nivel (N1-N4) com veredito por celula, lida de vereditos_tabela1_tabela5.tsv."""
    linhas = ler_tsv("vereditos_tabela1_tabela5.tsv")
    cab = {r["coluna"]: r for r in linhas if r["linha"] == "COL"}
    cel = {(r["linha"], r["coluna"]): r for r in linhas if r["linha"] != "COL"}
    larg, alt = 7.4, 6.3
    x_rot, w_col, gap, h_cel, topo = 1.75, 1.34, 0.06, 1.5, 0.85
    fig = plt.figure(figsize=(larg, alt))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, larg), ax.set_ylim(alt, 0), ax.axis("off")
    nomes_n = {"N1": "N1\nincidência", "N2": "N2 disparidade\nresidual", "N3": "N3\ncontexto", "N4": "N4\nmotivação"}
    for j, n in enumerate(("N1", "N2", "N3", "N4")):
        x = x_rot + j * (w_col + gap)
        ax.text(x + w_col / 2, 0.02, nomes_n[n], ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w_col / 2, 0.42, "\n".join(textwrap.wrap(cab[n]["texto_curto"].split(": ", 1)[1], 22)), ha="center",
                va="top", fontsize=MIN_PT, color=INK2)
    VALORES["fig7"] = {"celulas": {}}
    for i, (lin, perg) in enumerate(PERGUNTAS_MAPA.items()):
        y = topo + i * (h_cel + gap)
        ax.text(0.05, y + h_cel / 2, "\n".join(textwrap.wrap(perg, 20)), ha="left", va="center", fontsize=9, fontweight="bold", color=INK)
        for j, n in enumerate(("N1", "N2", "N3", "N4")):
            r = cel[(lin, n)]
            borda, fundo, simb = ESTILO_VEREDITO[r["categoria"]]
            rotulo = ROTULO_VEREDITO.get(r["categoria"], r["categoria"])
            x = x_rot + j * (w_col + gap)
            caixa = FancyBboxPatch((x, y), w_col, h_cel, boxstyle="round,pad=0,rounding_size=0.06", fc=fundo, ec=borda, lw=1.3)
            ax.add_patch(caixa)
            ax.text(x + 0.09, y + 0.07, simb, ha="left", va="top", fontsize=13, color=borda, fontweight="bold")
            rot_txt = ax.text(x + 0.31, y + 0.09, "\n".join(textwrap.wrap(rotulo, 15)), ha="left", va="top", fontsize=MIN_PT,
                              fontweight="bold", color=INK)
            ax.text(x + 0.09, y + h_cel - 0.07, "\n".join(textwrap.wrap(r["texto_curto"], 20)), ha="left", va="bottom",
                    fontsize=MIN_PT, color=INK2)
            VALORES["fig7"]["celulas"][f"{lin}|{n}"] = {
                "rotulo_exibido": rot_txt.get_text().replace("\n", " "), "fundo": matplotlib.colors.to_hex(caixa.get_facecolor())}
    y = topo + 3 * (h_cel + gap) + 0.12
    x = x_rot
    for cat, (borda, fundo, simb) in ESTILO_VEREDITO.items():
        ax.add_patch(FancyBboxPatch((x, y - 0.02), 0.2, 0.2, boxstyle="round,pad=0,rounding_size=0.03", fc=fundo, ec=borda, lw=1.1))
        ax.text(x + 0.1, y + 0.08, simb, ha="center", va="center", fontsize=MIN_PT, color=borda, fontweight="bold")
        txt = {"sustentada": "sustentada", "parcial": "parcial", "não sustentada pelo que foi medido": "não sustentada",
               "não testável": "não testável", "sem veredito": "só descrito"}[cat]
        ax.text(x + 0.27, y + 0.08, txt, fontsize=MIN_PT, color=INK, va="center")
        x += 0.32 + 0.072 * len(txt) + 0.1
    moldura(fig, "No Brasil, só a violência não letal contra LGB+ e as mortes de mulheres e negros são medidas; “gays morrem mais?” não é testável com o dado público, e fora do país só vale para mortalidade geral",
            "Resposta do paper a cada pergunta, para o Brasil, em cada nível (N1 a N4); cor e símbolo dizem a força da evidência",
            "Cada linha é uma pergunta; cada coluna, um jeito de olhar para ela, de “quantos?” (N1) a “por quê?” (N4). Verde com ✓: o dado sustenta a resposta. "
            "Cinza com ?: não há dado que permita testar. Vinho com ✗: os dados lidos não alcançam a afirmação. Cinza claro: o paper só descreve, sem dar veredito.",
            "não letal = violência que não matou · letal = morte · N2 = a diferença persiste depois de descontar idade, cor, instrução e região? · "
            "“sem veredito” = há números descritivos, mas o paper não classifica a célula · N4 “não sustentada pelo que foi medido” = fração nacional não estimada · fora do Brasil, “gays morrem mais?” é sustentada para mortalidade geral em populações definidas pela regra ampliada do adendo de 24/10 sobre o quartil Q1 (pela regra original seria “parcial”), sem razão de homicídio · RP = quantas vezes mais",
            "paper/figures/fontes/vereditos_tabela1_tabela5.tsv: cada célula cita um trecho literal da Tabela 1 e das seções 3 e 4 do paper v0.1; a categoria é a classificação desta figura.")
    salvar(fig, "fig7_mapa_de_respostas")


# ---------------------------------------------------------------- Figura 8: taxas SIM por grupo
GRUPOS_SIM = ["Homens negros", "Homens não negros", "Mulheres negras", "Mulheres não negras"]
COR_SIM = {"Homens negros": PALETA["homens"], "Homens não negros": PALETA["homens_cl"],
           "Mulheres negras": PALETA["mulheres"], "Mulheres não negras": PALETA["mulheres_cl"]}


def ler_asr() -> dict:
    """Taxa padronizada por idade (agressao X85-Y09) dos 4 grupos em 2022, 2023, 2024."""
    out: dict = {g: {} for g in GRUPOS_SIM}
    for r in ler_csv("asr_brasil.csv"):
        if r["desfecho"] == "agressao" and r["grupo"] in out and r["ano"] in ("2022", "2023", "2024"):
            out[r["grupo"]][int(r["ano"])] = float(r["taxa_padronizada"])
    return out


def figura8() -> None:
    """Barras horizontais: media 2022-24 da taxa padronizada, com os tres anos como tracos."""
    asr = ler_asr()
    media = {g: sum(asr[g].values()) / 3 for g in GRUPOS_SIM}
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    y = list(range(4))[::-1]
    bars = ax.barh(y, [media[g] for g in GRUPOS_SIM], height=0.58, color=[COR_SIM[g] for g in GRUPOS_SIM])
    pts = ax.scatter([v for g in GRUPOS_SIM for v in asr[g].values()], [yy for g, yy in zip(GRUPOS_SIM, y) for _ in range(3)],
                     s=60, marker="|", linewidths=1.6, color=INK, zorder=3)
    ref = media["Mulheres não negras"]
    ax.text(66, 3.62, "vezes a taxa de\nmulheres não negras", va="bottom", ha="left", fontsize=MIN_PT, color=INK2)
    for g, yy, p in zip(GRUPOS_SIM, y, bars):
        v = p.get_width()
        ax.text(max(asr[g].values()) + 2.0, yy, f"{br(v)}", va="center", ha="left", fontsize=11.5, fontweight="bold", color=INK)
        ax.text(66, yy, f"×{br(v / ref)}", va="center", ha="left", fontsize=11.5, color=INK)
    ax.set_yticks(y, GRUPOS_SIM, fontsize=9)
    ax.set_xlim(0, 80), ax.set_ylim(-0.6, 4.4)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.set_xlabel("Mortes por agressão por 100 mil pessoas do grupo, já descontada a idade (média 2022-24)", fontsize=MIN_PT + 0.3)
    ax.grid(axis="x", color=GRADE, lw=0.6)
    ax.set_axisbelow(True)
    seta(ax, "a taxa de todos os grupos\né medida contra esta barra (×1,0)", (media["Mulheres não negras"] + 0.3, y[3]), (20, y[3] + 0.35), va="center")
    VALORES["fig8"] = {"grupos": GRUPOS_SIM, "media": [float(p.get_width()) for p in bars],
                       "pontos": [float(v) for v in pts.get_offsets()[:, 0]]}
    moldura(fig, f"A taxa de morte por agressão dos homens negros é {br(media['Homens negros'] / ref)} vezes a das mulheres não negras",
            "Brasil, óbitos por agressão por 100 mil pessoas do grupo, padronizados por idade, média de 2022 a 2024",
            "Cada barra é a média de três anos; cada traço preto é um dos anos (2022, 2023, 2024). Na coluna da direita, ×19,9 quer dizer “19,9 vezes a taxa das mulheres não negras”, "
            "que serve de referência. Quanto maior a barra, mais mortes por agressão para cada 100 mil pessoas do grupo.",
            "padronizada por idade = taxa recalculada como se todos os grupos tivessem a mesma distribuição de idades · agressão = homicídios e outras agressões "
            "registradas no atestado de óbito (CID-10 X85-Y09) · negros = pretos e pardos · denominadores de 2023 e 2024 estimados a partir do Censo 2022",
            "paper/figures/fontes/asr_brasil.csv (origem dados/sim/asr_brasil.csv; SIM, Ministério da Saúde).")
    salvar(fig, "fig8_taxas_sim_grupos")


# ---------------------------------------------------------------- Figura 9: o que o painel exclui
def figura9() -> None:
    """Para cada desfecho do painel principal, faixa de efeitos compatíveis (IC95%) e faixas excluidas."""
    c02 = ler_c02()
    grupos = ["total", "homens", "mulheres", "negros", "nao_negros", "arma"]
    nomes = {"total": "Total", "homens": "Homens", "mulheres": "Mulheres", "negros": "Negros",
             "nao_negros": "Não negros", "arma": "Arma de fogo"}
    x0, x1 = -32, 32
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    fig.subplots_adjust(left=0.14, right=0.66, top=0.9, bottom=0.2)
    y = list(range(len(grupos)))[::-1]
    azuis, pts, lims = [], [], []
    for g, yy in zip(grupos, y):
        b, lo_b, hi_b = c02[(g, "registrado_ln")]
        pt, lo, hi = pct5(b), pct5(lo_b), pct5(hi_b)
        lims.append((lo, hi))
        ax.barh(yy, lo - x0, left=x0, height=0.5, color=PALETA["excl"])
        ax.barh(yy, x1 - hi, left=hi, height=0.5, color=PALETA["excl"])
        azuis.append(ax.barh(yy, hi - lo, left=lo, height=0.5, color=PALETA["estat_cl"])[0])
        pts.append(ax.plot([pt], [yy], "s", color=PALETA["estat"], ms=7, zorder=3)[0])
        ax.text(1.03, yy, f"queda > {br(abs(lo))}%  ·  alta > {br(hi)}%", transform=ax.get_yaxis_transform(), va="center",
                ha="left", fontsize=MIN_PT + 0.5, color=INK)
    ax.text(1.03, 1.03, "Efeitos que o painel exclui", transform=ax.transAxes, fontsize=9, fontweight="bold", color=INK, va="bottom")
    ax.axvline(0, color=INK2, lw=0.9, ls="--")
    ax.set_yticks(y, [nomes[g] for g in grupos], fontsize=9)
    ax.set_xlim(x0, x1)
    ax.set_xticks([-30, -20, -10, 0, 10, 20, 30], ["-30", "-20", "-10", "0", "+10", "+20", "+30"], fontsize=MIN_PT)
    ax.set_xlabel("Variação da taxa de homicídio ao trocar PT por DEM ou PL (5 pontos de ideologia), %", fontsize=MIN_PT)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, fc=PALETA["excl"]), Rectangle((0, 0), 1, 1, fc=PALETA["estat_cl"]), pts[0]],
              labels=["excluído pelos dados", "compatível com os dados", "melhor estimativa"], frameon=False, fontsize=MIN_PT,
              loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3)
    seta(ax, "o painel não enxerga\nefeitos menores que isto", (lims[0][1] + 0.3, y[0] + 0.3), (17, y[0] + 1.05), va="center")
    ax.set_ylim(-0.6, 6.3)
    VALORES["fig9"] = {"grupos": grupos,
                       "ic": [[float(p.get_x()), float(p.get_x() + p.get_width())] for p in azuis],
                       "pontos": [float(q.get_xdata()[0]) for q in pts]}
    minimo = min(min(-lo, hi) for lo, hi in lims)
    maximo = max(max(-lo, hi) for lo, hi in lims)
    moldura(fig, f"O painel de governadores só enxergaria efeitos maiores que {br(minimo)}% a {br(maximo)}% na taxa de homicídios; abaixo disso, não diz nada",
            "Faixa de variação da taxa registrada de morte por agressão compatível com os dados, por grupo, numa troca de PT por DEM ou PL",
            "A barra roxa clara é o que os dados ainda permitem: do que seria uma queda ao que seria uma alta. O cinza é o que o painel exclui. "
            "Como a barra sempre inclui zero, o resultado é “não sei se houve efeito”, e não “não houve efeito”: efeitos pequenos passam despercebidos.",
            "intervalo normal (a inversão do bootstrap wild-cluster, na Tabela 6 do paper, é um pouco mais larga) · painel = 351 combinações de estado e ano, 2012-2024 · 5 pontos de ideologia = distância média entre o PT (2,97) e DEM ou PL (cerca de 8) numa escala de 0 a 10 · "
            "exploratório: não prova causa · base: a taxa registrada, que pode esconder mortes de causa indeterminada",
            "paper/figures/fontes/c02_indet_resultados.csv (origem dados/painel/c02_indet_resultados.csv); IC95% com erro-padrão agrupado por estado.")
    salvar(fig, "fig9_governos_forest")


# ---------------------------------------------------------------- Figura 10: identificabilidade
def figura10() -> None:
    """Tres incidencias (constante, +15%, -5%) que reproduzem a mesma serie de BOs de LGBTfobia 2022-2025."""
    js = json.loads((FONTES / "sim_identificabilidade_resumo.json").read_text(encoding="utf-8"))
    obs, p0 = js["observado"], js["P0"]
    anos = [int(a) for a in obs]
    t = [a - anos[0] for a in anos]
    cores = [PALETA["ref"], PALETA["estat"], PALETA["fonte_b"]]
    estilos = [("-", 3.4), ("--", 2.4), (":", 2.8)]
    rot = {"S1": "incidência constante", "S2": "incidência +15% ao ano", "S3": "incidência −5% ao ano"}
    fig = plt.figure(figsize=(7.2, 5.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.55, wspace=0.36, left=0.1, right=0.97, top=0.92, bottom=0.09)
    a = fig.add_subplot(gs[0, :])
    b = fig.add_subplot(gs[1, 0])
    c = fig.add_subplot(gs[1, 1])
    VALORES["fig10"] = {"observado": [float(v) for v in obs.values()], "cenarios": {}}
    for (nome, par), cor, (ls, lw) in zip(js["cenarios"].items(), cores, estilos):
        k = nome[:2]
        g, i0, h = par["g"], par["I0_2022"], par["h_registro"]
        r_mod = [i0 * (1 + g) ** tt * p0 * (1 + h) ** tt for tt in t]
        inc = [i0 * (1 + g) ** tt for tt in t]
        prop = [100 * p0 * (1 + h) ** tt for tt in t]
        la, = a.plot(anos, r_mod, ls, color=cor, lw=lw, label=f"{rot[k]} e registro +{br(100 * h)}% ao ano")
        lb, = b.plot(anos, [v / 1000 for v in inc], "-", color=cor, lw=2.4)
        lc, = c.plot(anos, prop, "-", color=cor, lw=2.4)
        VALORES["fig10"]["cenarios"][k] = {"registro_modelo": [float(v) for v in la.get_ydata()],
                                           "incidencia_mil": [float(v) for v in lb.get_ydata()],
                                           "propensao_pct": [float(v) for v in lc.get_ydata()]}
        b.annotate(rot[k].replace("incidência ", ""), (anos[-1], inc[-1] / 1000), xytext=(-4, 6 if g >= 0 else -12),
                   textcoords="offset points", ha="right", fontsize=MIN_PT, color=INK)
        c.annotate(f"+{br(100 * h, 0)}%/ano", (anos[-1], prop[-1]), xytext=(4, -3), textcoords="offset points",
                   fontsize=MIN_PT, color=INK)
    ob = a.plot(anos, list(obs.values()), "D", color=INK, ms=7, zorder=5, label="registrado de fato (Anuário FBSP)")[0]
    VALORES["fig10"]["observado_plotado"] = [float(v) for v in ob.get_ydata()]
    mod1 = VALORES["fig10"]["cenarios"]["S1"]["registro_modelo"]
    for an, v, mv in zip(anos, obs.values(), mod1):
        a.annotate(miles(v), (an, v), xytext=(0, 12 if v > mv else -18), textcoords="offset points", ha="center", fontsize=MIN_PT + 0.5,
                   color=INK, fontweight="bold")
    a.set_xticks(anos)
    a.set_ylabel("BOs por ano", fontsize=MIN_PT + 0.5)
    a.set_ylim(0, 4300)
    a.set_yticks([0, 1000, 2000, 3000, 4000], ["0", "1.000", "2.000", "3.000", "4.000"])
    a.grid(axis="y", color=GRADE, lw=0.6)
    a.legend(frameon=False, fontsize=MIN_PT, loc="upper left")
    a.set_title("(a) A série registrada: as três linhas coincidem de propósito", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    sse = next(iter(js["cenarios"].values()))["sse_log"]
    seta(a, f"as três linhas têm o mesmo erro\n(soma de quadrados em log = {br(sse, 4)})", (anos[2] + 0.02, VALORES["fig10"]["cenarios"]["S1"]["registro_modelo"][2] - 30),
         (2024.35, 600), va="center")
    b.set_xticks(anos), c.set_xticks(anos)
    b.set_xlim(anos[0] - 0.1, anos[-1] + 0.1), c.set_xlim(anos[0] - 0.1, anos[-1] + 0.55)
    b.set_ylim(0, 40), c.set_ylim(0, 25)
    b.set_ylabel("ocorrências reais, em milhares", fontsize=MIN_PT + 0.5), c.set_ylabel("% das ocorrências que viram BO", fontsize=MIN_PT + 0.5)
    b.set_title("(b) O que realmente aconteceu (invisível)", loc="left", fontsize=9, fontweight="bold", color=INK)
    c.set_title("(c) A chance de virar BO (invisível)", loc="left", fontsize=9, fontweight="bold", color=INK)
    for ax_ in (a, b, c):
        ax_.tick_params(labelsize=MIN_PT)
    b.grid(axis="y", color=GRADE, lw=0.6), c.grid(axis="y", color=GRADE, lw=0.6)
    sp = js["sse_por_p0"]
    p0s = " / ".join(f"{int(round(100 * float(k)))}%" for k in sp)
    iguais = len({round(v, 4) for d in sp.values() for v in d.values()}) == 1
    hs_ = [p["h_registro"] for p in js["cenarios"].values()]
    hmin, hmax = min(hs_), max(hs_)
    moldura(fig, "A série de BOs sobe 4,4 vezes, mas cabe numa incidência constante, crescente ou decrescente: ela sozinha não mede a violência".replace("4,4", br(list(obs.values())[-1] / list(obs.values())[0], 1)),
            "Boletins de ocorrência de racismo por homofobia ou transfobia, 2022 a 2025, e três explicações opostas que reproduzem a mesma série",
            "Em (a), os losangos são o que foi registrado e as três linhas são o que cada história prevê: elas coincidem. Em (b) e (c), o que cada história supõe por trás: "
            f"violência estável, subindo ou caindo, compensada por uma chance de registro que cresce de {br(100 * hmin, 0)}% a {br(100 * hmax, 0)}% ao ano. Sem dado externo, não dá para escolher.",
            "BO = boletim de ocorrência · incidência = quantas ocorrências aconteceram de verdade · propensão de registro = fração delas que vira BO · "
            "erro de ajuste = distância entre a linha do modelo e os pontos reais, em escala de logaritmo" +
            (f" · teste de sensibilidade: o erro é o mesmo com propensão inicial de {p0s}" if iguais else ""),
            "paper/figures/fontes/sim_identificabilidade_resumo.json (origem simulacao/resumo.json); incidência e propensão recalculadas da fórmula do paper.")
    salvar(fig, "fig10_identificabilidade")


# ---------------------------------------------------------------- Figura 11: circulacao no Parlamento
FAMILIAS = [("F1", "gays/LGBT morrem mais"), ("F2", "o país que mais mata"), ("F3", "governo mata ou persegue"),
            ("F4", "não existe / dado inventado")]


def ler_discurso() -> dict:
    """Contagens de falas por familia (v1 literal e v2 corrigido) e denominador, como no painel de publicacao."""
    cont: dict = {}
    den = 0
    anos = set()
    for r in ler_csv("contagens.csv"):
        if r["ano"] == "total":
            continue
        uniao = r["consulta"].startswith(r["familia"] + "-any")
        if r["universo"] in ("Camara", "Senado"):
            if r["familia"] in dict(FAMILIAS) and uniao:
                cont[("v2", r["familia"])] = cont.get(("v2", r["familia"]), 0) + int(r["n"])
            elif r["familia"] == "TOTAL":
                den += int(r["n"])
                anos.add(int(r["ano"]))
        elif r["universo"] in ("Camara (v1 literal)", "Senado (v1 literal)") and r["familia"] in dict(FAMILIAS) and uniao:
            cont[("v1", r["familia"])] = cont.get(("v1", r["familia"]), 0) + int(r["n"])
    return {"v1": {f: cont[("v1", f)] for f, _ in FAMILIAS}, "v2": {f: cont[("v2", f)] for f, _ in FAMILIAS},
            "denominador": den, "anos": [min(anos), max(anos)]}


def ler_fonte_primaria() -> list[dict]:
    """Linhas de fonte primaria (a, n1, base b, n2, p de Fisher) de r7_parlamento_sensibilidade.csv, mais o 2o codificador."""
    rows = [x for x in ler_csv("r7_parlamento_sensibilidade.csv") if x["variavel"] == "fonte primária"]
    return [{"rotulo": x["codificacao_F2"], "a": int(x["a"]), "n": int(x["n1"]), "b": int(x["b"]), "n2": int(x["n2"]), "p": float(x["p_fisher"])} for x in rows]


def figura11() -> None:
    """(a) falas por frase no Parlamento (busca ampla x corrigida); (b) taxa de citacao de fonte primaria com IC de Wilson."""
    d, fp = ler_discurso(), ler_fonte_primaria()
    fig = plt.figure(figsize=(7.2, 5.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1], hspace=0.78, left=0.25, right=0.74, top=0.92, bottom=0.12)
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    y = list(range(4))[::-1]
    fam = [f for f, _ in FAMILIAS]
    ghost = a.barh(y, [d["v1"][f] for f in fam], height=0.72, color=PALETA["excl"], label="primeira busca (palavras demais)")
    sol = a.barh(y, [d["v2"][f] for f in fam], height=0.4, color=PALETA["estat"], label="busca corrigida (a que vale)")
    for f, yy in zip(fam, y):
        a.text(d["v1"][f] + 12, yy, f"{d['v1'][f]}", va="center", fontsize=MIN_PT, color=INK2)
        v2 = d["v2"][f]
        a.text(1.04, yy, f"{v2} falas  ({br(10000 * v2 / d['denominador'])} por 10 mil)", transform=a.get_yaxis_transform(),
               va="center", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
    a.text(1.04, 1.02, "busca corrigida", transform=a.transAxes, fontsize=MIN_PT + 0.5, color=INK, fontweight="bold", va="bottom")
    a.set_yticks(y, [f"{f}  “{n}”" for f, n in FAMILIAS], fontsize=9)
    a.set_xlim(0, 800), a.tick_params(axis="x", labelsize=MIN_PT)
    a.set_xlabel("Falas encontradas na Câmara e no Senado", fontsize=MIN_PT + 0.5)
    a.grid(axis="x", color=GRADE, lw=0.6), a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.3, -0.27), ncol=2)
    a.set_title(f"(a) Quatro frases em {miles(d['denominador'])} falas ({d['anos'][0]} a {d['anos'][1]})", loc="left", fontsize=9.5,
                fontweight="bold", color=INK, x=-0.35)
    lit = next(x for x in fp if "literal" in x["rotulo"])
    apl = next(x for x in fp if "aplicada" in x["rotulo"])
    seg = next(x for x in fp if x["rotulo"].startswith("segundo"))
    linhas = [(lit["a"], lit["n"], "“O país que mais mata”: regra literal\ndo livro de códigos (principal)", "s", False, PALETA["estat"]),
              (apl["a"], apl["n"], "mesmas falas, regra aplicada pelo\ncodificador original (sensibilidade)", "s", True, PALETA["estat"]),
              (seg["a"], seg["n"], "mesmas falas, 2º codificador\n(outra família de modelo)", "D", True, PALETA["estat"]),
              (lit["b"], lit["n2"], "linha de base: outras estatísticas\nde plenário na Câmara", "o", False, PALETA["ref"])]
    yb = [3, 2, 1, 0]
    pts, ics = [], []
    for (k, n, rot, mk, oco, cor), yy in zip(linhas, yb):
        lo, hi = wilson(k, n)
        eb = b.errorbar([100 * k / n], [yy], xerr=[[max(0.0, 100 * k / n - 100 * lo)], [100 * hi - 100 * k / n]], fmt=mk, ms=7, mfc="white" if oco else cor, mec=cor,
                        mew=1.8, color=cor, ecolor=cor, elinewidth=2.2, capsize=3, clip_on=False)
        pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0])
        b.text(1.04, yy, f"{k} de {n}  ({br(100 * k / n)}%)", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.5,
               color=INK, fontweight="bold" if yy == 3 else "normal")
    b.set_yticks(yb, [x[2] for x in linhas], fontsize=MIN_PT + 0.5)
    b.set_ylim(-0.6, 3.6), b.set_xlim(-0.6, 42)
    b.set_xticks([0, 5, 10, 15, 20])
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel("Falas que citam fonte primária, % (barra = faixa de incerteza)", fontsize=MIN_PT + 0.5)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.annotate("", xy=(41, -0.1), xytext=(41, 3.1), arrowprops={"arrowstyle": "<->", "color": INK2, "lw": 1.2})
    b.text(40.4, 1.5, f"contra 2 de 38, teste de Fisher:\n1 de 49 (principal): p = {br(lit['p'], 4)}\n0 de 49 (sensibilidade): p = {br(apl['p'], 4)}\nnenhum distinguível do acaso", ha="right", va="center",
           fontsize=MIN_PT, color=INK, fontweight="bold")
    b.set_title("(b) A taxa de fonte primária é baixa, e a linha de base também", loc="left", fontsize=9.5, fontweight="bold",
                color=INK, x=-0.35)
    VALORES["fig11"] = {"familias": fam, "v1": [float(p.get_width()) for p in ghost], "v2": [float(p.get_width()) for p in sol],
                        "denominador": d["denominador"], "fonte_primaria": {"pontos": pts, "ic": ics, "linhas": [[x[0], x[1]] for x in linhas]},
                        "p_fisher": {"literal": lit["p"], "aplicada": apl["p"]}}
    moldura(fig, "Só 1 das 49 falas parlamentares sobre “o país que mais mata” cita fonte primária pela regra literal (0 pela regra aplicada); outras estatísticas de plenário também quase nunca citam",
            f"Quatro frases em {miles(d['denominador'])} falas da Câmara e do Senado, {d['anos'][0]} a {d['anos'][1]}, e a fonte que cada fala apresenta",
            "Em (a), as barras mostram quantas falas contêm cada frase. Em (b), o ponto é a fração das falas que citam um documento oficial ou estudo com nome e ano, "
            "e a barra é a faixa de incerteza. A regra literal do livro de códigos (1 de 49) é a principal desta versão; a regra aplicada pelo primeiro codificador (0 de 49) fica como sensibilidade. Em nenhuma delas as falas se distinguem de outras estatísticas de plenário.",
            "fonte primária = documento oficial ou estudo com referência · primeira busca = lista de palavras que casava demais (por exemplo, “trans” dentro de “transporte”); "
            "a versão corrigida foi escrita depois de ver o resultado e está declarada como desvio · faixa de incerteza = IC95% de Wilson, adequado a proporções pequenas · "
            "teste de Fisher = compara duas proporções (p alto = a diferença pode ser acaso)",
            "paper/figures/fontes/contagens.csv e r7_parlamento_sensibilidade.csv (origens em research-2026-10-21-rodada3/discurso/midia/ e escrutinio/simetria/).")
    salvar(fig, "fig11_circulacao_parlamento")


# ---------------------------------------------------------------- Figura 12: escrutinio dos dois lados
FLANCO_LADO = {
    "DIREITA": "Direita", "DIREITA+METODOLÓGICO": "Direita",
    "ESQUERDA": "Esquerda", "ESQUERDA+METODOLÓGICO": "Esquerda",
    "AMBAS": "Ambas", "AMBAS (DIREITA no enquadramento; pares na independência)": "Ambas",
    "METODOLÓGICO": "Metodológico",
}
LADOS = ["Direita", "Esquerda", "Ambas", "Metodológico"]
DECISOES = [("ACEITO-CORRIGIR", "Aceito e\ncorrigido", 4), ("PARCIAL", "Aceito em\nparte", 3), ("VERIFICAR-ANALISE", "Verificar com\nanálise nova", 3),
            ("ACEITO-LIMITAÇÃO", "Aceito como\nlimitação", 1), ("REJEITADO", "Rejeitado", 1)]
PRIOR_COR = {"P1": (PALETA["p1"], "white"), "P2": (PALETA["p2"], INK), "P3": (PALETA["p3"], INK)}
# os 10 clusters mais perigosos da TRIAGEM.md (secao 2), em ordem de risco, com nome em linguagem comum
PERIGOSOS = [("C16", "Cuba: a perseguição estava mal provada"), ("C20", "“Não existe” é falso: saltava de dado para motivo"),
             ("C17", "Governos do Brasil: busca desigual entre os lados"), ("C06", "Contagem do GGB: “piso” contradizia o próprio texto"),
             ("C01", "Painel: coeficiente nulo lido como “nenhum efeito”"), ("C14", "Mortalidade: resumo apagava excessos medidos"),
             ("C04", "PNS x Sinan: “independentes” e “passa” fortes demais"), ("C21", "“País que mais mata”: sem comparação entre países"),
             ("C12", "Identificabilidade: “mesmo suporte” mal formulado"), ("C19", "“Nunca”, “ninguém”, “primeira vez” sem busca declarada")]


def figura12() -> None:
    """Os 33 clusters da triagem dos 4 revisores hostis: lado do ataque (linhas) x decisao tomada (colunas)."""
    rows = ler_csv("TRIAGEM.csv")
    cel: dict = {}
    for r in rows:
        cel.setdefault((FLANCO_LADO[r["flanco"]], r["decisão"]), []).append((r["cluster"], r["prioridade"]))
    sq_w, sq_h, gp = 0.36, 0.29, 0.03
    x_rot = 1.1
    larg_col = [max(k * (sq_w + gp) + 0.14, 0.9) for _, _, k in DECISOES]
    alt_linha = {l: max(math.ceil(len(cel.get((l, dc), [])) / k) for dc, _, k in DECISOES) * (sq_h + gp) + 0.16 for l in LADOS}
    topo = 0.62
    W = x_rot + sum(larg_col) + 0.05
    H = topo + sum(alt_linha.values()) + 0.45 + 0.17 * 5
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W), ax.set_ylim(H, 0), ax.axis("off")
    tot_dec = {dc: sum(len(cel.get((lado, dc), [])) for lado in LADOS) for dc, _, _ in DECISOES}
    tot_lado = {lado: sum(len(cel.get((lado, dc), [])) for dc, _, _ in DECISOES) for lado in LADOS}
    xs, x = {}, x_rot
    for (dc, nome, k), w in zip(DECISOES, larg_col):
        xs[dc] = x
        ax.text(x + w / 2, 0.02, f"{nome}\n({tot_dec[dc]})", ha="center", va="top", fontsize=MIN_PT, fontweight="bold", color=INK)
        x += w
    ys, y = {}, topo
    for lado in LADOS:
        ys[lado] = y
        ax.add_patch(Rectangle((0.02, y), W - 0.04, alt_linha[lado] - 0.04, fc=PALETA["sv_bg"], ec="none", zorder=0))
        ax.text(0.1, y + 0.1, f"{lado}\n({tot_lado[lado]})", ha="left", va="top", fontsize=9, fontweight="bold", color=INK)
        y += alt_linha[lado]
    for (lado, dc), itens in cel.items():
        k = dict((d_, kk) for d_, _, kk in DECISOES)[dc]
        for i, (cl, pr) in enumerate(sorted(itens)):
            r_, c_ = divmod(i, k)
            fc, tc = PRIOR_COR[pr]
            px, py = xs[dc] + 0.08 + c_ * (sq_w + gp), ys[lado] + 0.08 + r_ * (sq_h + gp)
            ax.add_patch(Rectangle((px, py), sq_w, sq_h, fc=fc, ec=PALETA["p1"], lw=0.7, gid=cl))
            ax.text(px + sq_w / 2, py + sq_h / 2, cl, ha="center", va="center", fontsize=MIN_PT, color=tc, fontweight="bold")
    yl = topo + sum(alt_linha.values()) + 0.1
    ax.text(0.05, yl, "Prioridade na triagem:", fontsize=MIN_PT, fontweight="bold", color=INK, va="top")
    x = 1.7
    for pr, (fc, tc) in PRIOR_COR.items():
        ax.add_patch(Rectangle((x, yl - 0.01), 0.3, 0.2, fc=fc, ec=PALETA["p1"], lw=0.7))
        ax.text(x + 0.15, yl + 0.09, pr, ha="center", va="center", fontsize=MIN_PT, color=tc, fontweight="bold")
        x += 0.42
    ax.text(0.05, yl + 0.34, "Os 10 clusters mais perigosos, em ordem de risco:", fontsize=MIN_PT, fontweight="bold", color=INK, va="top")
    meio = W / 2
    for i, (cl, nome) in enumerate(PERIGOSOS):
        col, lin = divmod(i, 5)
        ax.text(0.05 + col * meio, yl + 0.56 + lin * 0.17, f"{i + 1}. {cl}  {nome}", fontsize=MIN_PT, color=INK, va="top")
    VALORES["fig12"] = {"clusters": {}}
    for p in ax.patches:
        if p.get_gid():
            cx, cy = p.get_x() + 0.01, p.get_y() + 0.01
            lado = next(l for l in reversed(LADOS) if cy >= ys[l])
            dec = next(dc for dc, _, _ in reversed(DECISOES) if cx >= xs[dc])
            VALORES["fig12"]["clusters"][p.get_gid()] = [lado, dec, matplotlib.colors.to_hex(p.get_facecolor())]
    moldura(fig, f"Os {len(rows)} ataques dos 4 revisores hostis vieram dos dois lados, e {tot_dec['ACEITO-CORRIGIR']} viraram correção do texto",
            "Clusters de objeções da revisão hostil por lado de origem (linhas) e decisão tomada (colunas)",
            "Cada quadrado é um grupo de objeções parecidas (C01 a C33), colocado na linha de onde veio o ataque e na coluna da decisão: a maioria foi aceita e corrigida, "
            "poucos foram rejeitados. Quanto mais escuro, mais prioritário. Nenhum ataque estava factualmente errado no todo: o que caía era a síntese, mais forte que o corpo do texto.",
            "cluster = grupo de objeções semelhantes de revisores diferentes · lado = de onde veio o ataque (“+ metodológico” conta no lado) · "
            "“ambas” = vale para direita e esquerda · revisores = 4 modelos de IA, cada um com uma revisão escrita",
            "paper/figures/fontes/TRIAGEM.csv (origem research-2026-10-21-rodada3/escrutinio/TRIAGEM.csv; ranking dos 10 de TRIAGEM.md, seção 2).")
    salvar(fig, "fig12_escrutinio_dois_lados")


# ---------------------------------------------------------------- Figura 13: PNS x Sinan
def ler_triangulacao() -> dict:
    """Parcela LGB+ entre vitimas adultas de violencia fisica: PNS (direto e Monte Carlo) e Sinan (pior e melhor caso)."""
    md = (FONTES / "triangulacao_pns_sinan.md").read_text(encoding="utf-8")
    out: dict = {"mc": {}, "sinan": {}, "necessaria": {}}
    for m in re.finditer(r"\| ([AB])\. .*? \| ([\d.]+)% \| ([\d.]+)% a ([\d.]+)% \|", md):
        out["mc"][m.group(1)] = [float(m.group(2)), float(m.group(3)), float(m.group(4))]
    for m in re.finditer(r"\| (20\d\d) \| ([\d,]+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \|", md):
        out["sinan"][int(m.group(1))] = {"valida": float(m.group(3)), "pct": float(m.group(4)), "pior": float(m.group(7)), "melhor": float(m.group(8))}
    for m, ano in zip(re.finditer(r"precisariam ter ([\d.]+)% LGB\+", md), (2023, 2024)):
        out["necessaria"][ano] = float(m.group(1))
    c05 = (FONTES / "c05_razao_direta.md").read_text(encoding="utf-8")
    m = re.search(r"\| \(b\) só hetero ou LGB\+ \(comparável ao Sinan\) \| total \| \d+ \| \d+ \| ([\d.]+) \|.*?\| \[([\d.]+); ([\d.]+)\] \|", c05)
    out["direto"] = [float(m.group(1)), float(m.group(2)), float(m.group(3))]
    m = re.search(r"lgb ([\d.]+) \(([\d.]+)-([\d.]+)\)", md)
    out["lgb_pop"] = float(m.group(1))
    return out


def figura13() -> None:
    """Pontos: parcela LGB+ entre vitimas de violencia fisica, PNS (tres calculos) e Sinan 2023-2024 (com pior e melhor caso)."""
    t = ler_triangulacao()
    linhas = [("PNS 2019, direto no microdado\n(quem respondeu hetero ou LGB+)", t["direto"], estat_cheio, None),
              ("PNS 2019, simulação\n(só quem respondeu a orientação)", t["mc"]["A"], estat_vazado, None),
              ("PNS 2019, simulação\n(denominador antigo do projeto)", t["mc"]["B"], estat_vazado, None),
              ("Sinan 2023\n(fichas com orientação válida)", None, None, 2023),
              ("Sinan 2024\n(fichas com orientação válida)", None, None, 2024)]
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    fig.subplots_adjust(left=0.3, right=0.72, top=0.92, bottom=0.2)
    y = list(range(len(linhas)))[::-1]
    pts, ics, pm = [], [], []
    for (rot, v, fn, ano), yy in zip(linhas, y):
        if ano is None:
            eb = fn(ax, [v[0]], [yy], xerr=[[v[0] - v[1]], [v[2] - v[0]]])
            pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0])
            ax.text(1.03, yy, f"{br(v[0], 2)}%  [{br(v[1], 1)} a {br(v[2], 1)}]", transform=ax.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.5, color=INK)
        else:
            s = t["sinan"][ano]
            ax.plot([s["pior"], s["melhor"]], [yy, yy], "-", color=PALETA["fonte_b"], lw=1.2, alpha=0.55)
            ax.plot([s["pior"], s["melhor"]], [yy, yy], "|", color=PALETA["fonte_b"], ms=9, alpha=0.8)
            pt = ax.plot([s["pct"]], [yy], "o", color=PALETA["fonte_b"], ms=8, zorder=3)[0]
            pts.append(float(pt.get_xdata()[0])), ics.append([s["pior"], s["melhor"]]), pm.append(ano)
            ax.text(1.03, yy, f"{br(s['pct'], 2)}%  (pior caso {br(s['pior'], 1)}, melhor {br(s['melhor'], 1)})", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=MIN_PT + 0.5, color=INK)
    ax.axvline(t["lgb_pop"], color=INK2, lw=0.9, ls="--")
    ax.text(t["lgb_pop"] + 0.25, 4.62, f"LGB+ na população adulta: {br(t['lgb_pop'], 2)}%", fontsize=MIN_PT, color=INK2, va="bottom")
    ax.set_yticks(y, [r for r, *_ in linhas], fontsize=MIN_PT + 0.5)
    ax.set_ylim(-0.6, 5.0), ax.set_xlim(0, 30)
    ax.set_xlabel("LGB+ entre as vítimas adultas de violência física (%)", fontsize=MIN_PT + 0.5)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)
    seta(ax, f"para o Sinan igualar a PNS, as fichas sem\nresposta precisariam ter {br(t['necessaria'][2023], 1)}% de LGB+", (t["sinan"][2023]["melhor"] - 0.8, y[3] + 0.12), (7.5, y[3] + 0.5), va="center", ha="left")
    ax.text(1.03, 1.03, "estimativa [faixa]", transform=ax.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    VALORES["fig13"] = {"pontos": pts, "ic": ics, "lgb_pop": t["lgb_pop"]}
    moldura(fig, f"LGB+ são cerca de {br(t['direto'][0], 0)}% das vítimas de violência física na pesquisa de população e {br(t['sinan'][2023]['pct'], 0)}% nas fichas de saúde, ambos bem acima de {br(t['lgb_pop'], 2)}% da população",
            "Parcela de LGB+ entre adultos que sofreram violência física, vista por duas janelas: a pesquisa de domicílios (PNS) e as notificações dos serviços de saúde (Sinan)",
            "Cada linha é uma estimativa da mesma pergunta: de cada 100 vítimas adultas de violência física, quantas são LGB+? A linha tracejada mostra a parcela de LGB+ na população. "
            "As duas janelas concordam no sentido (LGB+ aparecem mais entre vítimas do que na população) e discordam na magnitude; no Sinan, a barra fina mostra o intervalo possível "
            "quando um quarto das fichas não tem orientação registrada.",
            "PNS = pesquisa de domicílios do IBGE (amostra) · Sinan = sistema de notificação de violência dos serviços de saúde (quem procurou atendimento, não amostra) · "
            "orientação válida = ficha em que a orientação sexual foi preenchida · pior/melhor caso = se nenhuma ou todas as fichas sem resposta fossem de LGB+ · "
            "faixa da PNS = IC95% (o Sinan não tem IC: é contagem)",
            "paper/figures/fontes/triangulacao_pns_sinan.md e c05_razao_direta.md (origens dados/sinan/ e dados/pns/).")
    salvar(fig, "fig13_pns_sinan_janelas")


# ---------------------------------------------------------------- Figura 14: Sinan x Anuario por UF
NOME2UF = {"Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA", "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA",
           "Piauí": "PI", "Ceará": "CE", "Rio Grande do Norte": "RN", "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE",
           "Bahia": "BA", "Minas Gerais": "MG", "Espírito Santo": "ES", "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR",
           "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT", "Goiás": "GO",
           "Distrito Federal": "DF"}


def ranks(v: np.ndarray) -> np.ndarray:
    """Postos com empate pela media (para Spearman)."""
    o = np.argsort(v, kind="mergesort")
    r = np.empty(len(v))
    r[o] = np.arange(1, len(v) + 1)
    for x in np.unique(v):
        m = v == x
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def spearman(a, b) -> float:
    """Correlacao de Spearman (Pearson dos postos)."""
    return float(np.corrcoef(ranks(np.asarray(a, float)), ranks(np.asarray(b, float)))[0, 1])


def ler_uf_2024() -> list[dict]:
    """UFs com notificacao Sinan de LGBTfobia, BO do Anuario (edicao 2026) e populacao do Censo 2022, ano 2024."""
    sin = {r["uf"]: int(r["m_lgbtfobia"]) for r in ler_csv("serie_campo55_uf_ano.csv") if r["ano"] == "2024" and r["uf"] != "BR"}
    bo = {r["uf"]: int(r["registros"]) for r in ler_csv("anuario_lgbtfobia_uf_ano_v2.csv")
          if r["edicao"] == "2026" and r["ano_dado"] == "2024" and r["uf"] != "BR" and r["registros"] != ""}
    pop = {NOME2UF[x["D1N"]]: float(x["V"]) for x in json.loads((FONTES / "sidra_9514.json").read_text(encoding="utf-8"))[1:]}
    return [{"uf": u, "sinan": sin[u], "bo": bo[u], "pop": pop[u]} for u in sorted(bo)]


def figura14() -> None:
    """(a) dispersao por UF, bolhas = populacao; (b) correlacao bruta, esperada so pelo tamanho e parcial, por ano."""
    d = ler_uf_2024()
    fig = plt.figure(figsize=(7.2, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1], wspace=0.5, left=0.08, right=0.98, top=0.92, bottom=0.17)
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    xs, ys, pp = [x["sinan"] for x in d], [x["bo"] for x in d], [x["pop"] for x in d]
    sc = a.scatter(xs, ys, s=[p / 2.2e5 for p in pp], color=PALETA["fonte_b"], alpha=0.55, edgecolor=PALETA["fonte_b"], linewidth=1)
    for x in sorted(d, key=lambda r: -r["pop"])[:6]:
        a.annotate(x["uf"], (x["sinan"], x["bo"]), xytext=(6, 5), textcoords="offset points", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.set_xscale("log"), a.set_yscale("log")
    a.set_xlabel("Notificações de LGBTfobia no Sinan, 2024", fontsize=MIN_PT + 0.3)
    a.set_ylabel("BOs de LGBTfobia no Anuário, 2024", fontsize=MIN_PT + 0.3)
    a.tick_params(labelsize=MIN_PT)
    a.grid(color=GRADE, lw=0.6), a.set_axisbelow(True)
    rho_c = spearman(xs, ys)
    a.set_title(f"(a) Cada bolha é um estado (n = {len(d)})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    a.text(0.03, 0.96, f"bolha = população\nSpearman das contagens: {br(rho_c, 2)}", transform=a.transAxes, va="top", fontsize=MIN_PT, color=INK2)
    rows = [r for r in ler_csv("concordancia_v2.csv") if r["especificacao"].startswith("S0 principal")]
    anos = [int(r["ano"]) for r in rows]
    yb = list(range(len(rows)))[::-1]
    for r, yy in zip(rows, yb):
        b.plot([float(r["rho_so_tamanho"]), float(r["rho_contagens"])], [yy, yy], "-", color=INK2, lw=1, alpha=0.5)
    c1 = b.plot([float(r["rho_contagens"]) for r in rows], yb, "o", mfc="white", mec=PALETA["estat"], mew=1.8, ms=7.5, ls="", label="só contagens")[0]
    c2 = b.plot([float(r["rho_so_tamanho"]) for r in rows], yb, "x", color=PALETA["ref"], ms=7, mew=2, ls="", label="só pelo tamanho do estado")[0]
    par = float
    c3 = estat_cheio(b, [par(r["rho_parcial"]) for r in rows], yb,
                     xerr=[[par(r["rho_parcial"]) - par(r["ic_parcial_lo"]) for r in rows], [par(r["ic_parcial_hi"]) - par(r["rho_parcial"]) for r in rows]],
                     label="descontado o tamanho (IC95%)")
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_yticks(yb, [str(x) for x in anos], fontsize=MIN_PT + 0.5)
    b.set_xlim(-0.45, 1.0), b.set_ylim(-0.6, 3.6)
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel("Correlação entre as duas séries (Spearman)", fontsize=MIN_PT + 0.3)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=1)
    b.set_title("(b) Concordância por ano", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    seta(b, "descontado o tamanho,\nsobra pouco e inclui zero", (float(rows[0]["rho_parcial"]) + 0.02, yb[0] + 0.12), (0.45, yb[0] - 0.55), va="center")
    parciais = [par(r["rho_parcial"]) for r in rows]
    VALORES["fig14"] = {"ufs": [x["uf"] for x in d], "sinan": [float(v) for v in sc.get_offsets()[:, 0]], "bo": [float(v) for v in sc.get_offsets()[:, 1]],
                        "anos": anos, "rho_contagens": [float(v) for v in c1.get_xdata()], "rho_tamanho": [float(v) for v in c2.get_xdata()],
                        "rho_parcial": [float(v) for v in c3.lines[0].get_xdata()], "ic_parcial": erros_de(c3)}
    moldura(fig, f"Estados que notificam mais à saúde também têm mais BOs de LGBTfobia, mas é o tamanho: descontado, a concordância cai para {br(min(parciais), 2)} a {br(max(parciais), 2)}",
            f"Notificações de LGBTfobia no Sinan x boletins de ocorrência do Anuário de Segurança Pública, por estado ({min(int(x['n_ufs']) for x in rows)} a {max(int(x['n_ufs']) for x in rows)} estados por ano), 2022 a 2025",
            "Em (a), cada bolha é um estado: os mais populosos têm mais de tudo, então as duas contagens sobem juntas. Em (b), o círculo vazado é a concordância bruta, o ×  é quanto "
            "se esperaria só pelo tamanho e o quadrado cheio é o que sobra depois de descontá-lo: pequeno e com intervalo que inclui zero em todos os anos.",
            "Sinan = notificações de violência dos serviços de saúde · BO = boletim de ocorrência (polícia) · Spearman = correlação entre posições dos estados, de −1 a +1 · "
            "descontar o tamanho = correlação parcial controlando pela população (Censo 2022) · IC95% = faixa de incerteza, por reamostragem de estados",
            "paper/figures/fontes/concordancia_v2.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv (edição 2026), sidra_9514.json (Censo 2022).")
    salvar(fig, "fig14_concordancia_sinan_anuario")


# ---------------------------------------------------------------- Figura 15: ideologia x taxa (painel)
def ler_painel() -> tuple[list[str], list[int], np.ndarray, np.ndarray]:
    """UF, ano, ideologia e log da taxa total do painel principal (partido do TSE, escore por periodo)."""
    rs = [r for r in ler_csv("painel_uf_ano_tse_brc.csv") if r["ideologia"] not in ("", "nan") and r["tx_total"] not in ("", "nan")]
    return ([r["uf"] for r in rs], [int(r["ano"]) for r in rs], np.array([float(r["ideologia"]) for r in rs]),
            np.log(np.array([float(r["tx_total"]) for r in rs])))


def residuos(ufs, anos, v) -> np.ndarray:
    """Residuo de v depois de efeitos fixos de UF e de ano (minimos quadrados com dummies)."""
    cu, ca = sorted(set(ufs)), sorted(set(anos))
    X = np.zeros((len(v), len(cu) + len(ca) - 1))
    for i, (u, a_) in enumerate(zip(ufs, anos)):
        X[i, cu.index(u)] = 1
        if ca.index(a_) > 0:
            X[i, len(cu) + ca.index(a_) - 1] = 1
    beta, *_ = np.linalg.lstsq(X, v, rcond=None)
    return v - X @ beta


def figura15() -> None:
    """Dispersao de residuos: ideologia do governador x taxa de agressao, com a reta e a faixa de incerteza do painel."""
    ufs, anos, ideo, ly = ler_painel()
    rx, ry = residuos(ufs, anos, ideo), residuos(ufs, anos, ly)
    b = float((rx @ ry) / (rx @ rx))
    c02 = ler_c02()[("total", "registrado_ln")]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    sc = ax.scatter(rx, 100 * (np.exp(ry) - 1), s=16, color=PALETA["ref"], alpha=0.45, linewidth=0)
    xx = np.linspace(rx.min() - 0.3, rx.max() + 0.3, 50)
    ax.fill_between(xx, 100 * (np.exp(c02[1] * xx) - 1), 100 * (np.exp(c02[2] * xx) - 1), color=PALETA["estat_cl"], alpha=0.7, lw=0,
                    label="faixa compatível com os dados (IC95%)")
    ln, = ax.plot(xx, 100 * (np.exp(b * xx) - 1), "-", color=PALETA["estat"], lw=2.4, label="reta estimada")
    ax.axhline(0, color=INK2, lw=0.8, ls="--")
    ax.set_xlabel("Ideologia do governador, comparada à média do próprio estado e do ano (pontos, de 0 = esquerda a 10 = direita)", fontsize=MIN_PT)
    ax.set_ylabel("Taxa de homicídio, comparada à média\ndo estado e do ano (%)", fontsize=MIN_PT + 0.3)
    ax.tick_params(labelsize=MIN_PT)
    ax.grid(color=GRADE, lw=0.6), ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=MIN_PT, loc="upper left")
    seta(ax, "a reta é quase plana:\nnão há relação visível", (xx[-8], 100 * (np.exp(b * xx[-8]) - 1)), (1.5, 100 * (np.exp(ry).max() - 1) * 0.72), va="center", ha="left")
    VALORES["fig15"] = {"n": int(len(rx)), "x": [float(v) for v in sc.get_offsets()[:, 0]], "y": [float(v) for v in sc.get_offsets()[:, 1]],
                        "inclinacao": b, "reta_x": [float(v) for v in ln.get_xdata()[[0, -1]]], "reta_y": [float(v) for v in ln.get_ydata()[[0, -1]]]}
    moldura(fig, f"Estados com governadores mais à direita não têm mais nem menos homicídios que a média deles: a reta, de inclinação {br(b, 4)}, é plana",
            f"{len(rx)} combinações de estado e ano, 2012 a 2024: ideologia do partido do governador x taxa de morte por agressão, depois de descontar o que é de cada estado e de cada ano",
            "Cada ponto cinza é um estado num ano. O eixo horizontal diz se o governador estava mais à direita ou à esquerda que o habitual para aquele estado; "
            "o vertical, se a taxa de homicídio estava acima ou abaixo do habitual. Se governar à direita mudasse a taxa, os pontos subiriam ou desceriam para a direita. "
            "A nuvem não tem direção e a faixa roxa clara, que admite retas inclinadas para os dois lados, mostra que o painel não distingue de zero.",
            "descontar o estado e o ano = subtrair a média de cada estado e a de cada ano (efeitos fixos), para comparar cada estado só com ele mesmo · "
            "ideologia = escore de 0 (esquerda) a 10 (direita) dado por especialistas ao partido do governador · IC95% = faixa de incerteza com erro-padrão agrupado por estado · "
            "exploratório: não prova causa",
            "paper/figures/fontes/painel_uf_ano_tse_brc.csv (origem dados/painel/) e c02_indet_resultados.csv (faixa).")
    salvar(fig, "fig15_ideologia_taxa_residuos")


# ---------------------------------------------------------------- Figura 16: linha do tempo das fontes
def figura16() -> None:
    """Anos cobertos por cada fonte (lidos dos CSVs) e o que cada uma mede ou nao."""
    sim = sorted({int(r["ano"]) for r in ler_csv("asr_brasil.csv") if r["grupo"] == "Brasil"})
    sinan = sorted({int(r["ano"]) for r in ler_csv("serie_campo55_uf_ano.csv")})
    anu = sorted({int(r["ano_dado"]) for r in ler_csv("anuario_lgbtfobia_uf_ano_v2.csv")})
    ggb = sorted({int(r["ano"]) for r in ler_csv("serie_ggb_vs_cobertura.csv") if r["ggb"] != ""})
    pns = [int(re.search(r"PNS (\d{4})", (FONTES / "seguro_pns2019.md").read_text(encoding="utf-8")).group(1))]
    cov = {"SIM (óbitos)": sim, "Sinan (saúde)": sinan, "Anuário (polícia)": anu, "GGB": ggb, "PNS (IBGE)": pns}
    txt = {r["fonte"]: r for r in ler_tsv("cobertura_fontes.tsv")}
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.subplots_adjust(left=0.17, right=0.62, top=0.93, bottom=0.17)
    nomes = list(cov)
    y = list(range(len(nomes)))[::-1]
    VALORES["fig16"] = {"fontes": nomes, "anos": {}}
    for n, yy in zip(nomes, y):
        anos = cov[n]
        if len(anos) == 1:
            ax.plot(anos, [yy], "D", color=PALETA["estat"], ms=9)
        else:
            bar = ax.barh(yy, anos[-1] - anos[0] + 1, left=anos[0] - 0.5, height=0.42, color=PALETA["estat"])[0]
            rot_a = f"{anos[0]}–{anos[-1]}"
            if anos[-1] - anos[0] >= 9:
                ax.text((anos[0] + anos[-1]) / 2, yy, rot_a, ha="center", va="center", fontsize=MIN_PT + 0.5, color="white", fontweight="bold")
            else:
                ax.text(anos[0] - 0.9, yy, rot_a, ha="right", va="center", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
        VALORES["fig16"]["anos"][n] = [int(anos[0]), int(anos[-1])]
        ax.text(1.03, yy + 0.12, "mede: " + txt[n]["mede"], transform=ax.get_yaxis_transform(), va="bottom", fontsize=MIN_PT, color=INK)
        ax.text(1.03, yy + 0.1, "não mede: " + txt[n]["nao_mede"], transform=ax.get_yaxis_transform(), va="top", fontsize=MIN_PT, color=INK2)
    ax.set_yticks(y, nomes, fontsize=9)
    ax.set_xlim(1999, 2027.5), ax.set_ylim(-0.6, 4.6)
    ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)
    ax.set_xlabel("Ano", fontsize=MIN_PT + 0.5)
    seta(ax, "uma única onda", (pns[0] - 0.9, y[4]), (2006, y[4]), va="center", ha="center")
    for a_ in ("mede", "não mede"):
        pass
    moldura(fig, "Cada fonte cobre anos diferentes e mede coisas diferentes; nenhuma sozinha dá uma taxa de morte de LGBT+",
            "Anos cobertos por cada fonte de dados do projeto e o que cada uma mede ou não mede",
            "Cada barra mostra de que ano a que ano a fonte tem dados; o losango é uma pesquisa de um só ano. À direita, em linguagem simples, o que a fonte "
            "mede e o que ela não consegue medir. Quando as barras não se sobrepõem, as fontes não podem ser comparadas ano a ano.",
            "SIM = Sistema de Informações sobre Mortalidade, base de atestados de óbito · Sinan = notificações de violência nos serviços de saúde · "
            "Anuário = Anuário Brasileiro de Segurança Pública (BOs) · GGB = Grupo Gay da Bahia · PNS = pesquisa de domicílios do IBGE (autorrelato)",
            "anos lidos de paper/figures/fontes/asr_brasil.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv, serie_ggb_vs_cobertura.csv; textos de cobertura_fontes.tsv (trechos do paper v0.1).")
    salvar(fig, "fig16_linha_do_tempo_fontes")


# ---------------------------------------------------------------- Figura 17: tamanho de survey
def figura17() -> None:
    """Adultos entrevistados por desenho e menor variacao detectavel na violencia fisica; adultos necessarios para +30%."""
    cap = {r["opcao"][:2]: r for r in ler_csv("capacidade_por_opcao.csv") if r["indicador"] == "fisica"}
    need = next(r for r in ler_csv("cenarios_n_custo.csv") if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["deff_base"] == "deff medido")
    deff = float(next(r for r in ler_csv("n_necessario.csv") if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["sobreamostra_k"] == "1")["deff_lgb"])
    linhas = [("PNS 2019 (o que existe)", int(cap["B'"]["adultos"]), float(cap["B'"]["mde_deff_medido"]), PALETA["ref"]),
              ("Uma nova rodada dedicada\ntipo PNS", int(cap["B:"]["adultos"]), float(cap["B:"]["mde_deff_medido"]), PALETA["estat_cl"]),
              ("Módulo anual na PNAD Contínua", int(cap["A:"]["adultos"]), float(cap["A:"]["mde_deff_medido"]), PALETA["estat_cl"]),
              ("Necessário para detectar +30%", int(need["adultos_a_triar"]), 0.30, PALETA["estat"])]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    fig.subplots_adjust(left=0.3, right=0.98, top=0.93, bottom=0.2)
    y = list(range(len(linhas)))[::-1]
    bars = ax.barh(y, [n / 1000 for _, n, _, _ in linhas], height=0.58, color=[c for *_, c in linhas])
    for (rot, n, mde, c), yy in zip(linhas, y):
        ax.text(n / 1000 + 6, yy + 0.08, f"{miles(n)} adultos", va="bottom", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
        ax.text(n / 1000 + 6, yy - 0.04, f"detecta mudança de {br(100 * mde, 1)}% ou mais", va="top", fontsize=MIN_PT, color=INK2)
    ax.set_yticks(y, [r for r, *_ in linhas], fontsize=MIN_PT + 0.5)
    ax.set_xlim(0, 520)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.set_xlabel("Adultos entrevistados ou triados por rodada (milhares)", fontsize=MIN_PT + 0.5)
    ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)
    falta = (int(need["adultos_a_triar"]) - int(cap["B'"]["adultos"]))
    ax.set_ylim(-1.55, 3.55)
    ax.annotate("", xy=(int(need["adultos_a_triar"]) / 1000, -0.72), xytext=(int(cap["B'"]["adultos"]) / 1000, -0.72),
                arrowprops={"arrowstyle": "<->", "color": INK2, "lw": 1.4})
    ax.text((int(need["adultos_a_triar"]) + int(cap["B'"]["adultos"])) / 2000, -0.9, f"faltam {miles(falta)} adultos\npara detectar uma variação de 30%",
            ha="center", va="top", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
    VALORES["fig17"] = {"rotulos": [r for r, *_ in linhas], "adultos_mil": [float(p.get_width()) for p in bars], "mde": [m for *_, m, _ in linhas], "deff": deff}
    moldura(fig, f"Uma PNS como a de 2019 só detecta variações de {br(100 * linhas[0][2], 0)}% na violência contra LGB+; detectar 30% exige cerca de {miles(round(int(need['adultos_a_triar']), -3))} adultos",
            "Violência física em 12 meses: tamanho de amostra de cada desenho de pesquisa e a menor mudança entre rodadas que ele consegue ver",
            "Cada barra é quantos adultos seriam entrevistados; o texto diz a menor mudança na violência física entre duas rodadas que esse tamanho permitiria enxergar. "
            "Para ver uma variação de 30% seriam precisos cerca de 306 mil adultos triados, porque só uma pequena fração é LGB+ e as respostas dentro de um mesmo domicílio se parecem.",
            f"detectar = distinguir uma mudança real de variação por acaso (poder de 80%, erro de 5%) · efeito de desenho = {br(deff, 1)}: a amostra complexa vale {br(deff, 1)} vezes menos que uma amostra aleatória simples do mesmo tamanho · "
            "triar = visitar domicílios para achar adultos LGB+ · PNAD Contínua = pesquisa trimestral de domicílios do IBGE",
            "paper/figures/fontes/capacidade_por_opcao.csv, cenarios_n_custo.csv, n_necessario.csv (origem research-2026-10-21-rodada3/F2-custos/).")
    salvar(fig, "fig17_tamanho_de_survey")


# ---------------------------------------------------------------- Figura 18: motivacao no Sinan
def figura18() -> None:
    """Motivacao registrada nas notificacoes de violencia interpessoal do Sinan, por ano (Brasil)."""
    rs = [r for r in ler_csv("serie_campo55_uf_ano.csv") if r["uf"] == "BR"]
    anos = [int(r["ano"]) for r in rs]
    ign = [float(r["pct_m_ign"]) for r in rs]
    na = [float(r["pct_m_na"]) for r in rs]
    lgbt = [float(r["pct_m_lgbt"]) for r in rs]
    outros = [100 - i - n - l for i, n, l in zip(ign, na, lgbt)]
    fig = plt.figure(figsize=(7.2, 4.7))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.6, 1], hspace=0.62, left=0.1, right=0.78, top=0.93, bottom=0.1)
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    base = np.zeros(len(anos))
    VALORES["fig18"] = {"anos": anos}
    for nome, vals, cor, chave in (("ignorado ou em branco", ign, PALETA["ref"], "ign"), ("não se aplica", na, "#a9a8a2", "na"),
                                   ("outro motivo (sexismo, racismo, família…)", outros, PALETA["estat_cl"], "outros"),
                                   ("LGBTfobia", lgbt, PALETA["estat"], "lgbt")):
        bars = a.bar(anos, vals, bottom=base, color=cor, width=0.78)
        VALORES["fig18"][chave] = [float(p.get_height()) for p in bars]
        a.text(anos[-1] + 0.7, base[-1] + vals[-1] / 2, nome, va="center", fontsize=MIN_PT, color=INK)
        base = base + np.array(vals)
    a.set_ylim(0, 100), a.set_xticks(anos)
    a.tick_params(labelsize=MIN_PT)
    a.set_ylabel("% das notificações", fontsize=MIN_PT + 0.3)
    a.set_title("(a) O que ficou registrado como motivo da violência", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    a.text(anos[0], ign[0] / 2, f"{br(ign[0], 0)}%", color="white", fontsize=MIN_PT, fontweight="bold", va="center", ha="center")
    a.text(anos[-1], ign[-1] / 2, f"{br(ign[-1], 0)}%", color="white", fontsize=MIN_PT, fontweight="bold", va="center", ha="center")
    seta(a, "quase um terço sem motivo", (anos[5], ign[5] + 0.5), (anos[3] - 0.4, 64), va="center", ha="left")
    ln, = b.plot(anos, lgbt, "-s", color=PALETA["estat"], lw=2, ms=5)
    for an, v in zip(anos, lgbt):
        b.annotate(br(v, 2), (an, v), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=MIN_PT - 0.5 + 0.5, color=INK)
    b.set_ylim(0, 0.8), b.set_xticks(anos)
    b.tick_params(labelsize=MIN_PT)
    b.set_ylabel("% de LGBTfobia", fontsize=MIN_PT + 0.3)
    b.set_title("(b) A fatia de LGBTfobia, ampliada", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    b.grid(axis="y", color=GRADE, lw=0.6)
    VALORES["fig18"]["lgbt_linha"] = [float(v) for v in ln.get_ydata()]
    moldura(fig, f"Em {br(ign[-1], 0)}% das notificações de {anos[-1]} o motivo da violência ficou ignorado ou em branco, e LGBTfobia aparece em só {br(lgbt[-1], 1)}%: o registro não mede incidência",
            f"Notificações de violência interpessoal nos serviços de saúde (Sinan), Brasil, {anos[0]} a {anos[-1]}: motivo registrado na ficha",
            "Cada coluna soma 100% das notificações do ano. O cinza-escuro é o campo “motivo” deixado ignorado ou em branco; o roxo é a LGBTfobia, que mal aparece (painel b, ampliado). "
            "Como a maior parte das fichas não diz o motivo e o preenchimento muda de um ano para o outro, o número de casos registrados como LGBTfobia não mostra quanta violência acontece.",
            "Sinan = Sistema de Informação de Agravos de Notificação, dos serviços de saúde · notificação = ficha preenchida quando alguém atendido sofreu violência · "
            "“não se aplica” = a ficha marca que o campo não cabe ao caso · incidência = quantos casos acontecem de verdade",
            "paper/figures/fontes/serie_campo55_uf_ano.csv (origem dados/sinan/), linha Brasil.")
    salvar(fig, "fig18_motivacao_sinan")


# ---------------------------------------------------------------- Figura 19: GGB x homicidio por UF
def figura19() -> None:
    """Contagem do GGB por milhao x taxa de homicidio e x acesso a internet, por UF (2019)."""
    rs = ler_csv("uf_2019.csv")
    js = json.loads((FONTES / "inflacao_uf_serie.json").read_text(encoding="utf-8"))
    sp, hom = js["spearman"], js["poisson_ggb ~ homicidio"]
    inet, both = js["poisson_ggb ~ internet"], js["poisson_ggb ~ internet + homicidio"]
    f2 = lambda d, k: br(d["irr_por_dp"][k], 2)   # noqa: E731
    ic = lambda d, k: f"{br(d['ic95_irr'][k][0], 2)} a {br(d['ic95_irr'][k][1], 2)}"   # noqa: E731
    fig = plt.figure(figsize=(7.2, 3.9))
    gs = fig.add_gridspec(1, 2, wspace=0.28, left=0.08, right=0.98, top=0.92, bottom=0.17)
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    gg = [float(r["ggb_por_milhao"]) for r in rs]
    pop = [float(r["pop"]) for r in rs]
    sa = a.scatter([float(r["hom_taxa_100mil"]) for r in rs], gg, s=[p / 2e5 for p in pop], color=PALETA["fonte_b"], alpha=0.55, edgecolor=PALETA["fonte_b"])
    sb = b.scatter([float(r["internet_dom_pct"]) for r in rs], gg, s=[p / 2e5 for p in pop], color=PALETA["fonte_b"], alpha=0.55, edgecolor=PALETA["fonte_b"])
    for r in sorted(rs, key=lambda r: -float(r["ggb_por_milhao"]))[:4]:
        for ax_, col in ((a, "hom_taxa_100mil"), (b, "internet_dom_pct")):
            ax_.annotate(r["uf"], (float(r[col]), float(r["ggb_por_milhao"])), xytext=(6, 4), textcoords="offset points", fontsize=MIN_PT, color=INK, fontweight="bold")
    ra, rb = sp["ggb_por_milhao ~ hom_taxa_100mil"], sp["ggb_por_milhao ~ internet_dom_pct"]
    a.set_xlabel("Homicídios por 100 mil habitantes", fontsize=MIN_PT + 0.3), b.set_xlabel("Domicílios com internet (%)", fontsize=MIN_PT + 0.3)
    a.set_ylabel("Mortes de LGBT+ contadas pelo GGB\npor milhão de habitantes", fontsize=MIN_PT + 0.3)
    for ax_ in (a, b):
        ax_.tick_params(labelsize=MIN_PT)
        ax_.grid(color=GRADE, lw=0.6), ax_.set_axisbelow(True)
    a.set_title(f"(a) Homicídio: acompanha (ρ = {br(ra['rho'], 2)})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    b.set_title(f"(b) Internet: some com o homicídio (ρ = {br(rb['rho'], 2)})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    seta(a, f"razão da contagem por\ndesvio-padrão de homicídio:\n{f2(hom, 0)} ({ic(hom, 0)})\nsó com homicídio;\n{f2(both, 1)} ({ic(both, 1)})\ncom internet no modelo",
         (max(float(r["hom_taxa_100mil"]) for r in rs) - 3.9, 2.78), (6.5, 5.75), va="center", ha="left")
    seta(b, f"internet sozinha:\n{f2(inet, 0)} ({ic(inet, 0)})\ncom homicídio junto:\n{f2(both, 0)} ({ic(both, 0)})",
         (76.5, 2.6), (68.4, 5.5), va="center", ha="left")
    VALORES["fig19"] = {"ufs": [r["uf"] for r in rs], "homicidio": [float(v) for v in sa.get_offsets()[:, 0]], "internet": [float(v) for v in sb.get_offsets()[:, 0]],
                        "ggb_por_milhao": [float(v) for v in sa.get_offsets()[:, 1]], "rho_hom": ra["rho"], "rho_internet": rb["rho"], "irr_so_homicidio": hom["irr_por_dp"][0], "irr_hom_com_internet": both["irr_por_dp"][1], "irr_internet_sozinha": inet["irr_por_dp"][0],
                        "irr_internet_com_hom": both["irr_por_dp"][0]}
    moldura(fig, f"A contagem do GGB por estado acompanha o homicídio em geral ({f2(both, 1)} vezes por desvio-padrão); a relação com a internet some quando o homicídio entra no modelo",
            f"Mortes de LGBT+ contadas pelo GGB por milhão de habitantes x homicídio e internet, {len(rs)} estados, 2019; bolha = população",
            "Cada bolha é um estado. Em (a), estados com mais homicídios em geral têm mais mortes de LGBT+ contadas. Em (b), estados com mais internet têm menos contagem quando a internet entra sozinha no modelo, "
            f"mas o efeito some ({f2(both, 0)}, faixa que inclui 1) quando o homicídio entra junto, e o homicídio fica em {f2(both, 1)}. É uma associação entre estados, não prova de causa.",
            "GGB = Grupo Gay da Bahia, que conta mortes de LGBT+ por notícias · ρ (rô) = correlação de Spearman, de −1 a +1 · razão = quantas vezes a contagem muda por desvio-padrão "
            "(medida de quanto os estados diferem entre si), em modelo de Poisson com erro robusto · cada razão traz o modelo de onde vem · IC95% = faixa de incerteza · 27 estados, uma edição",
            "paper/figures/fontes/uf_2019.csv e inflacao_uf_serie.json (origem research-2026-10-21-rodada3/F3-ggb/dados/; README do F3-ggb, linhas 16 e 137).")
    salvar(fig, "fig19_ggb_homicidio_uf")


# ---------------------------------------------------------------- Figuras 20 e 21: troca de presidente (C09)
def ler_d1_brasil() -> dict:
    """Quebras de nivel 2016, 2019 e 2023 (e placebo 1 ano antes) da serie nacional de agressao, de c09_d1_resultados.csv."""
    out: dict = {}
    for r in ler_csv("c09_d1_resultados.csv"):
        if r["serie"] == "Brasil" and r["desfecho"] == "agressao":
            out[int(r["quebra"])] = {k: float(r[k]) for k in ("pct", "pct_lo", "pct_hi", "placebo_pct", "placebo_pct_lo", "placebo_pct_hi", "mde_neg", "mde_pos")}
            out[int(r["quebra"])]["placebo_quebra"] = int(r["placebo_quebra"])
            out[int(r["quebra"])]["leitura"] = r["leitura"]
    return out


def figura20() -> None:
    """(a) taxa nacional 2010-2024 com as trocas de 2016, 2019 e 2023; (b) queda de nivel em cada troca x placebo um ano antes."""
    ser = {d: {int(r["ano"]): float(r["taxa_padronizada"]) for r in ler_csv("asr_brasil.csv") if r["grupo"] == "Brasil" and r["desfecho"] == d}
           for d in ("agressao", "agressao+indet")}
    d1 = ler_d1_brasil()
    fig = plt.figure(figsize=(7.2, 6.3))
    a = fig.add_axes([0.30, 0.60, 0.66, 0.35])
    b = fig.add_axes([0.30, 0.13, 0.44, 0.35])
    anos = sorted(ser["agressao"])
    la, = a.plot(anos, [ser["agressao"][x] for x in anos], "-o", color=PALETA["estat"], lw=2.4, ms=4.5, label="agressão (X85-Y09)")
    li, = a.plot(anos, [ser["agressao+indet"][x] for x in anos], "--", color=PALETA["ref"], lw=1.8, label="agressão + causa indeterminada")
    quem = {2016: "Temer assume", 2019: "Bolsonaro assume", 2023: "Lula assume"}
    for t, nome in quem.items():
        a.axvline(t, color=INK2, lw=1, ls=":")
        a.text(t + 0.15, 42.2 if t != 2019 else 40.3, f"{t}: {nome}", fontsize=MIN_PT, color=INK, va="top", ha="left")
    a.set_ylim(15, 42.6), a.set_xlim(2009.6, 2024.8)
    a.set_xticks(range(2010, 2025, 2))
    a.tick_params(labelsize=MIN_PT)
    a.set_ylabel("Mortes por agressão por 100 mil,\nigual padrão de idade", fontsize=MIN_PT + 0.3)
    a.grid(axis="y", color=GRADE, lw=0.6), a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=MIN_PT, loc="lower right")
    seta(a, "a queda já começou em 2018,\nantes da troca de 2019", (2018, ser["agressao"][2018] - 0.4), (2010.2, 19.0), va="center", ha="left")
    a.set_title("(a) A taxa nacional cai desde 2017", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
    linhas = []
    for t in (2016, 2019, 2023):
        linhas.append((t, "troca", d1[t]["pct"], d1[t]["pct_lo"], d1[t]["pct_hi"]))
        linhas.append((t, "placebo", d1[t]["placebo_pct"], d1[t]["placebo_pct_lo"], d1[t]["placebo_pct_hi"]))
    y = list(range(len(linhas)))[::-1]
    pts, ics, rotulos = [], [], []
    for (t, tipo, v, lo, hi), yy in zip(linhas, y):
        if tipo == "troca":
            eb = b.errorbar([v], [yy], xerr=[[v - lo], [hi - v]], fmt="s", ms=7, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=2.2, capsize=3)
        else:
            eb = b.errorbar([v], [yy], xerr=[[v - lo], [hi - v]], fmt="o", ms=7, mfc="white", mec=PALETA["ref"], mew=1.7, color=PALETA["ref"], ecolor=PALETA["ref"], elinewidth=1.8, capsize=3)
        pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0])
        rotulos.append(f"{t}: troca" if tipo == "troca" else f"{d1[t]['placebo_quebra']}: placebo (troca de controle)")
        b.text(1.03, yy, f"{br(v)}%  [{br(lo)}; {br(hi)}]", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.5, color=INK,
               fontweight="bold" if tipo == "troca" else "normal")
    b.set_yticks(y, rotulos, fontsize=MIN_PT + 0.5)
    mn = [(d1[t]["mde_neg"], d1[t]["mde_pos"]) for t in (2016, 2019, 2023)]
    for k, t in enumerate((2016, 2019, 2023)):
        yy = y[2 * k]
        b.plot([d1[t]["mde_neg"], d1[t]["mde_pos"]], [yy, yy], "|", color=PALETA["ink"], ms=14, mew=1.6, ls="none", zorder=4)
    b.plot([], [], "|", color=INK, ms=12, mew=1.6, ls="none", label="menor efeito detectável (80% de poder)")
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_xlim(-45, 46), b.set_ylim(-0.7, 5.8)
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel("Variação de nível da taxa depois da troca, %", fontsize=MIN_PT + 0.3)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    seta(b, f"o placebo de 2018\ncai {br(abs(d1[2019]['placebo_pct']))}%, mais que\na troca de 2019", (d1[2019]["placebo_pct_hi"] + 1.0, y[3]), (6, y[3]), va="center", ha="left")
    b.text(1.03, 1.03, "variação [IC95%]", transform=b.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    b.set_title("(b) Cada troca x uma troca de controle um ano antes", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
    VALORES["fig20"] = {"anos": anos, "agressao": [float(v) for v in la.get_ydata()], "agressao_indet": [float(v) for v in li.get_ydata()],
                        "quebras": [t for t, *_ in linhas], "tipos": [x[1] for x in linhas], "pontos": pts, "ic": ics,
                        "mde": [[float(m[0]), float(m[1])] for m in mn]}
    ai = {r["quebra"]: float(r["pct"]) for r in ler_csv("c09_d1_resultados.csv") if r["serie"] == "Brasil" and r["desfecho"] == "agressao+indet"}
    moldura(fig, f"A queda de {br(abs(d1[2019]['pct']), 0)}% na taxa nacional em 2019 já aparece em 2018, num placebo, uma troca de controle um ano antes ({br(d1[2019]['placebo_pct'])}%): os dados não a atribuem ao presidente",
            "Taxa nacional de morte por agressão, 2010-2024, e a variação de nível em cada troca de presidente (2016, 2019, 2023), comparada a um placebo um ano antes",
            "Em (a), a linha roxa é a taxa por 100 mil; as linhas pontilhadas marcam as trocas. Em (b), cada quadrado roxo é a mudança de nível estimada depois da troca e o círculo vazado é a mesma conta "
            "feita um ano antes, quando nada mudou: se o círculo mostra queda parecida, a queda não pode ser creditada à troca. Os traços pretos mostram o menor efeito que a análise conseguiria ver; "
            "como as barras são largas, o resultado é “não distinguível de zero, com poder baixo”, e não “não há efeito”.",
            f"nível = salto da taxa no ano da troca · placebo = a mesma conta num ano em que não houve troca · IC95% = faixa de incerteza · efeito mínimo detectável = menor efeito que a análise veria com 80% de chance · "
            f"só 15 pontos (2010-2024) e a análise é descritiva, não causal · somando as mortes de causa indeterminada, a queda de 2019 é {br(ai['2019'])}% · o óbito não registra orientação sexual: nada aqui é sobre violência contra LGBT+",
            "paper/figures/fontes/c09_d1_resultados.csv e asr_brasil.csv (origens research-2026-10-24-presidencia/ e dados/sim/); RELATORIO-C09.md; pré-registro PREREGISTRO-C09.")
    salvar(fig, "fig20_serie_nacional_trocas")


def ler_d2() -> list[dict]:
    """21 estimativas do painel de alinhamento governador x presidente (c09_d2_resultados.csv)."""
    return ler_csv("c09_d2_resultados.csv")


ROT_D2 = {("primaria", "total"): "Principal: governador 5 pontos à direita,\npresidente PT → PSL", ("S1_distancia", "total"): "Distância entre governador e presidente (5 pontos)",
          ("S4_escore_unico", "total"): "Escore de ideologia único (2018)", ("S5_sem_2016", "total"): "Sem o ano de 2016 (troca no meio do ano)",
          ("S6_BLS9", "total"): "Outra escala de ideologia (Zucco e Power)", ("S7_copartidarismo", "total"): "Governador do mesmo partido do presidente"}
NOME_GR = {"total": "Total", "homens": "Homens", "mulheres": "Mulheres", "negros": "Negros", "nao_negros": "Não negros", "arma": "Arma de fogo"}


def figura21() -> None:
    """Efeito do alinhamento governador x presidente na taxa de homicidio (IC95%) em 16 analises, com o efeito minimo detectavel."""
    d2 = [r for r in ler_d2() if r["escala"] == "log"]
    ordem = [("primaria", "total"), ("S1_distancia", "total"), ("S4_escore_unico", "total"), ("S5_sem_2016", "total"), ("S6_BLS9", "total"), ("S7_copartidarismo", "total")]
    ordem += [("S2_grupos", g) for g in ("homens", "mulheres", "negros", "nao_negros", "arma")] + [("S3_agr_indet", g) for g in ("total", "homens", "mulheres", "negros", "nao_negros")]
    por = {(r["analise"], r["grupo"]): r for r in d2}
    ys, y = [], 0.0
    for k, (an, g) in enumerate(ordem):
        if k in (0, 6, 11):
            y -= 0.9
        ys.append(y)
        y -= 1
    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    fig.subplots_adjust(left=0.37, right=0.74, top=0.96, bottom=0.07)
    pts, ics, mdes = [], [], []
    for (an, g), yy in zip(ordem, ys):
        r = por[(an, g)]
        b_, K = float(r["b"]), float(r["K"])
        v, lo, hi = 100 * (math.exp(b_ * K) - 1), float(r["ef_lo"]), float(r["ef_hi"])
        cor = PALETA["estat"] if an == "primaria" else PALETA["ref"]
        eb = ax.errorbar([v], [yy], xerr=[[v - lo], [hi - v]], fmt="s", ms=6.5, color=cor, ecolor=cor, elinewidth=2.2 if an == "primaria" else 1.8, capsize=2.5)
        pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0])
        mn, mp = float(r["mde_neg"]), float(r["mde_pos"])
        ax.plot([mn, mp], [yy, yy], "|", color=INK, ms=10, mew=1.4, ls="none", zorder=4)
        mdes.append([mn, mp])
        ax.text(1.03, yy, f"{br(lo)}% a +{br(hi)}%", transform=ax.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.5, color=INK,
                fontweight="bold" if an == "primaria" else "normal")
    ax.plot([], [], "|", color=INK, ms=11, mew=1.4, ls="none", label="menor efeito detectável (80% de poder)")
    ax.plot([], [], "s", color=PALETA["estat"], ms=7, label="análise principal"), ax.plot([], [], "s", color=PALETA["ref"], ms=7, label="outras análises (robustez e grupos)")
    labels = [ROT_D2.get((an, g), NOME_GR[g] + (" (agressão + indeterminada)" if an == "S3_agr_indet" and g == "total" else "")) for an, g in ordem]
    ax.set_yticks(ys, labels, fontsize=MIN_PT)
    for t, yy in (("Contraste principal e variações", ys[0] + 0.85), ("Por grupo", ys[6] + 0.85), ("Agressão + indeterminada, por grupo", ys[11] + 0.85)):
        ax.text(-1.0, yy, t, transform=ax.get_yaxis_transform(), fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, ha="left", va="center")
    ax.axvline(0, color=INK2, lw=0.9, ls="--")
    ax.set_xlim(-45, 45), ax.set_ylim(ys[-1] - 0.7, 0.4)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.set_xlabel("Variação da taxa de homicídio no contraste de cada análise, %", fontsize=MIN_PT + 0.3)
    ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=1)
    ax.text(1.03, 1.005, "variação [IC95%]", transform=ax.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    prim = por[("primaria", "total")]
    seta(ax, "só efeitos além dos traços\npretos seriam detectados", (float(por[("S7_copartidarismo", "total")]["mde_pos"]), ys[5] - 0.3), (26, ys[5] - 1.05), va="center", ha="left")
    todas = ler_d2()
    VALORES["fig21"] = {"linhas": [f"{a}|{g}" for a, g in ordem], "pontos": pts, "ic": ics, "mde": mdes, "n_estimativas": len(todas),
                        "n_distinguiveis": sum(r["distinguivel"] != "False" for r in todas)}
    moldura(fig, f"Nenhuma das {len(todas)} estimativas da interação entre a ideologia do governador e a do presidente se distingue de zero, mas o painel só veria efeitos de cerca de {br(abs(float(prim['mde_neg'])), 0)}% para menos ou {br(float(prim['mde_pos']), 0)}% para mais",
            "Interação entre os escores de ideologia do governador e do presidente (principal) e variações, na taxa de homicídio; 351 combinações de estado e ano (2012-2024); 16 análises em %",
            f"Cada quadrado é a melhor estimativa e a barra é a faixa compatível com os dados; todas as barras passam por zero, então o painel não consegue dizer se a interação mudou a taxa. "
            f"Os traços pretos mostram o menor efeito que a análise detectaria com 80% de chance ({br(float(prim['mde_neg']))}% e +{br(float(prim['mde_pos']))}% na principal): efeitos menores passariam despercebidos. "
            "O resultado é “não distinguível de zero, com poder baixo”; não é prova de que o presidente não importa.",
            "interação = produto do escore de ideologia do governador (0 a 10) pelo do presidente: mede se o efeito de um depende do outro; “distância entre governador e presidente” e “mesmo partido” são variações separadas · o efeito do presidente em si não é identificável: o efeito de ano o absorve, só a interação aparece · "
            "IC95% = faixa de incerteza (erro-padrão agrupado por estado) · efeito mínimo detectável = menor efeito que a análise veria com 80% de chance · 27 estados e 3 trocas de presidente · "
            "a razão de óbitos indeterminados (teste de falsificação, em pontos percentuais, 5 estimativas) está na tabela do relatório, não nesta figura · o óbito não registra orientação sexual",
            "paper/figures/fontes/c09_d2_resultados.csv e RELATORIO-C09.md (origem research-2026-10-24-presidencia/); pré-registro PREREGISTRO-C09 gravado antes dos desfechos.")
    salvar(fig, "fig21_alinhamento_governador_presidente")


# ---------------------------------------------------------------- Figuras 22 e 23: exposicao por governo (C10)
def ler_e1() -> list[dict]:
    """Linhas do Brasil da tabela federal (governo x desfecho), sem o mandato sem dado."""
    return [r for r in ler_csv("c10_e1_federal.csv") if r["serie"] == "Brasil" and r["taxa_base"] != ""]


GOV_CURTO = {"Dilma Rousseff": "Dilma", "Michel Temer": "Temer", "Jair Bolsonaro": "Bolsonaro", "Luiz Inácio Lula da Silva": "Lula (em curso)"}


def figura22() -> None:
    """(a) taxa nacional 2010-24 com faixas por governo; (b) variacao % do ano-base ao ano-fim de cada governo, com e sem indeterminada."""
    ser = {d: {int(r["ano"]): float(r["taxa_padronizada"]) for r in ler_csv("c10_e1_serie_longo.csv") if r["serie"] == "Brasil" and r["desfecho"] == d}
           for d in ("agressao", "agressao+indet")}
    gov_ano = {int(r["ano"]): r["governo_fracao_do_ano"] for r in ler_csv("c10_e1_serie_longo.csv") if r["serie"] == "Brasil" and r["desfecho"] == "agressao"}
    e1 = ler_e1()
    por = {(r["governo"], r["desfecho"]): r for r in e1}
    govs = ["Dilma Rousseff", "Michel Temer", "Jair Bolsonaro", "Luiz Inácio Lula da Silva"]
    fig = plt.figure(figsize=(7.2, 7.3))
    a = fig.add_axes([0.30, 0.67, 0.66, 0.30])
    b = fig.add_axes([0.30, 0.08, 0.44, 0.50])
    anos = sorted(ser["agressao"])
    # faixas por governo (limites a partir da fracao de cada ano; 2016 dividido Dilma/Temer)
    lim = {"Dilma": (2010.5, 2015.5 + 0.361), "Temer": (2015.5 + 0.361, 2018.5), "Bolsonaro": (2018.5, 2022.5), "Lula": (2022.5, 2024.5)}
    assert "Dilma Rousseff 0.361" in gov_ano[2016]   # a fracao 0,361 de 2016 vem do arquivo
    for k, (nome, (x0, x1)) in enumerate(lim.items()):
        a.axvspan(x0, x1, color=PALETA["card"] if k % 2 == 0 else "white", zorder=0)
        a.text((x0 + x1) / 2, 41.2, nome, ha="center", va="top", fontsize=MIN_PT, fontweight="bold", color=INK)
    la, = a.plot(anos, [ser["agressao"][x] for x in anos], "-o", color=PALETA["estat"], lw=2.4, ms=4.5, label="agressão (X85-Y09)")
    li, = a.plot(anos, [ser["agressao+indet"][x] for x in anos], "--", color=PALETA["ref"], lw=1.8, label="agressão + causa indeterminada")
    a.set_ylim(15, 42), a.set_xlim(2009.6, 2024.6)
    a.set_xticks(range(2010, 2025, 2))
    a.tick_params(labelsize=MIN_PT)
    a.set_ylabel("Mortes por agressão por 100 mil,\nigual padrão de idade", fontsize=MIN_PT + 0.3)
    a.grid(axis="y", color=GRADE, lw=0.6), a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=MIN_PT, loc="lower right")
    seta(a, "a queda começou em 2018,\nainda com Temer", (2018, ser["agressao"][2018] - 0.5), (2010.6, 19.2), va="center", ha="left")
    a.set_title("(a) A taxa nacional por governo", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
    # (b)
    linhas, y, yy = [], [], 0.0
    for g in govs:
        yy -= 0.9
        cab = (GOV_CURTO[g], por[(g, "agressao")]["ano_base"], por[(g, "agressao")]["ano_fim"], g)
        linhas.append(("cab", cab, yy + 0.65))
        for kind in ("agressao", "agressao+indet", "pre"):
            linhas.append((kind, g, yy)), 
            yy -= 1
    pts, ics, tip, gvs = [], [], [], []
    for kind, g, y0 in linhas:
        if kind == "cab":
            nome, a0, a1, _ = g
            b.text(-1.0, y0, f"{nome}: {a0} → {a1}", transform=b.get_yaxis_transform(), fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, ha="left", va="center")
            continue
        r = por.get((g, kind)) if kind != "pre" else por[(g, "agressao")]
        if kind == "pre":
            if r["pre_var_pct"] == "":
                b.text(1.03, y0, "n/d (sem dado antes de 2010)", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT, color=INK2)
                continue
            v = float(r["pre_var_pct"])
            m = b.plot([v], [y0], "D", mfc="white", mec=PALETA["ref"], mew=1.6, ms=6.5)[0]
            pts.append(float(m.get_xdata()[0])), ics.append(None), tip.append("pre"), gvs.append(g)
            b.text(1.03, y0, f"{br(v)}%  (contexto, {r['pre_de']} → {int(r['ano_base'])})", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT, color=INK2)
            continue
        v, lo, hi = float(r["var_pct"]), float(r["var_pct_lo"]), float(r["var_pct_hi"])
        if kind == "agressao":
            eb = b.errorbar([v], [y0], xerr=[[v - lo], [hi - v]], fmt="s", ms=7, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=2.2, capsize=3)
        else:
            eb = b.errorbar([v], [y0], xerr=[[v - lo], [hi - v]], fmt="o", ms=6.5, mfc="white", mec=PALETA["ref"], mew=1.6, color=PALETA["ref"], ecolor=PALETA["ref"], elinewidth=1.6, capsize=3)
        pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0]), tip.append(kind), gvs.append(g)
        b.text(1.03, y0, f"{br(v)}%  [{br(lo)}; {br(hi)}]", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.5, color=INK,
               fontweight="bold" if kind == "agressao" else "normal")
    rot = {"agressao": "agressão", "agressao+indet": "+ causa indeterminada", "pre": "3 anos antes da posse"}
    b.set_yticks([y0 for k, g, y0 in linhas if k != "cab"], [rot[k] for k, g, y0 in linhas if k != "cab"], fontsize=MIN_PT)
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_xlim(-30, 22), b.set_ylim(yy + 0.3, 0.2)
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel("Variação da taxa do ano-base ao último ano do governo, %", fontsize=MIN_PT + 0.3)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.text(1.03, 1.0, "variação [intervalo de contagem]", transform=b.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    b.set_title("(b) Quanto a taxa variou em cada governo", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
    bol, bol_i = por[("Jair Bolsonaro", "agressao")], por[("Jair Bolsonaro", "agressao+indet")]
    VALORES["fig22"] = {"anos": anos, "agressao": [float(v) for v in la.get_ydata()], "agressao_indet": [float(v) for v in li.get_ydata()],
                        "governos": gvs, "tipos": tip, "pontos": pts, "ic": ics, "limites": {k: [float(v[0]), float(v[1])] for k, v in lim.items()}}
    moldura(fig, f"A taxa nacional caiu {br(abs(float(bol['var_pct'])))}% entre {bol['ano_base']} e {bol['ano_fim']} ({br(abs(float(bol_i['var_pct'])))}% somando causa indeterminada); a queda começou em 2018, ainda com Temer; isto não é prova de causa",
            "Taxa nacional de morte por agressão, padronizada por idade, por governo (2010-2024), e variação do ano anterior à posse ao último ano inteiro de cada governo",
            "Em (a), cada faixa cinza ou branca é um governo e a linha roxa é a taxa por 100 mil. Em (b), cada quadrado roxo é quanto a taxa variou do ano anterior à posse ao último ano inteiro do governo; "
            "o círculo vazado faz a mesma conta somando as mortes de causa indeterminada; o losango mostra o que a taxa vinha fazendo nos 3 anos antes da posse, só como contexto. "
            "Isto é exposição: mostra o que aconteceu enquanto cada governo estava no cargo, não que o governo causou a mudança.",
            "taxa padronizada por idade = taxa recalculada como se a população tivesse sempre a mesma distribuição de idades · causa indeterminada = óbito cuja causa não foi definida (CID-10 Y10-Y34); "
            "sua fração sobe de 14% (2015) para 30% (2024), então a queda somando-as é sempre menor · intervalo de contagem = só a incerteza do número de mortes, não mede tendência nem causa · "
            "2016 é dividido entre Dilma (até 11/05) e Temer · Lula está em curso (2 de 4 anos; denominadores de 2023-24 estimados) · o governo Lula de 2007-10 não aparece: o SIM em disco começa em 2010 · o óbito não registra orientação sexual",
            "paper/figures/fontes/c10_e1_federal.csv e c10_e1_serie_longo.csv, RELATORIO-EXPOSICAO.md (origem research-2026-10-24-exposicao/); pré-registro PREREGISTRO-C10 gravado antes dos desfechos.")
    salvar(fig, "fig22_taxa_nacional_por_governo")


DIRECOES23 = [("todas", "Todas as 67 trocas"), ("bloco: esquerda->direita", "Esquerda → direita"), ("bloco: direita->esquerda", "Direita → esquerda"),
              ("bloco: envolve centro", "Envolve o centro"), ("bloco: mesmo bloco", "Dentro do mesmo bloco")]


def figura23() -> None:
    """67 trocas de governador: variacao da taxa do estado relativa ao Brasil (3 anos antes x 3 depois), por direcao, com a referencia das UFs sem troca."""
    tr = ler_csv("c10_e2_trocas_longo.csv")
    res = {(r["recorte"], r["direcao"], r["grupo"]): r for r in ler_csv("c10_e2_resumo.csv")}

    def pontos(grupo: str, dirc: str) -> list[float]:
        return [float(r["excesso_rel_pct"]) for r in tr if r["grupo"] == grupo and (dirc == "todas" or "bloco: " + r["direcao_bloco"] == dirc)]

    fig = plt.figure(figsize=(7.2, 7.2))
    a = fig.add_axes([0.30, 0.43, 0.42, 0.50])
    b = fig.add_axes([0.30, 0.10, 0.42, 0.20])
    VALORES["fig23"] = {"linhas": {}}

    def painel(ax, itens, grupo, destaque_ref=True):
        n = len(itens)
        ys = [-(i * 1.0) for i in range(n)]
        for (dirc, rot), yy in zip(itens, ys):
            r = res[("P_todas_67", dirc, grupo)]
            lo, hi = float(r["ref_mediana_p2_5"]), float(r["ref_mediana_p97_5"])
            band = ax.barh(yy, hi - lo, left=lo, height=0.86, color=PALETA["excl"], zorder=0)[0]
            xs = sorted(pontos(grupo, dirc))
            off = [((k * 7) % 5 - 2) * 0.13 for k in range(len(xs))]
            sc = ax.scatter(xs, [yy + o for o in off], s=22, color=PALETA["estat"], alpha=0.75, linewidths=0, zorder=3)
            med = ax.plot([float(r["mediana_pct"])], [yy], "D", color=INK, ms=7, mfc="white", mew=1.8, zorder=5)[0]
            ax.text(1.03, yy, f"{r['n_subiu']} subiram, {r['n_caiu']} caíram\nmediana {br(float(r['mediana_pct']))}%  (n = {r['n']})", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=MIN_PT + 0.3, color=INK)
            VALORES["fig23"]["linhas"][f"{grupo}|{dirc}"] = {"x": [float(v) for v in sc.get_offsets()[:, 0]], "mediana": float(med.get_xdata()[0]),
                                                           "ref": [float(band.get_x()), float(band.get_x() + band.get_width())],
                                                           "n_subiu": int(r["n_subiu"]), "n_caiu": int(r["n_caiu"])}
        ax.set_yticks(ys, [rot for _, rot in itens], fontsize=MIN_PT + 0.5)
        ax.set_ylim(ys[-1] - 0.7, 0.7), ax.set_xlim(-45, 50)
        ax.axvline(0, color=INK2, lw=0.9, ls="--")
        ax.tick_params(axis="x", labelsize=MIN_PT)
        ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)

    painel(a, DIRECOES23, "total")
    a.set_title("(a) Cada ponto é uma troca de governador", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.42)
    a.text(1.03, 1.0, "troca por troca", transform=a.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    a.set_xlabel("Variação da taxa do estado menos a do Brasil, 3 anos antes → 3 anos depois, %", fontsize=MIN_PT)
    for k, (grupo, rot) in enumerate((("total", "Só agressão"), ("total_agr_indet", "Agressão + causa indeterminada"))):
        yy = -k
        r = res[("P_todas_67", "todas", grupo)]
        lo, hi = float(r["ref_mediana_p2_5"]), float(r["ref_mediana_p97_5"])
        band = b.barh(yy, hi - lo, left=lo, height=0.86, color=PALETA["excl"], zorder=0)[0]
        xs = sorted(pontos(grupo, "todas"))
        off = [((j * 7) % 5 - 2) * 0.13 for j in range(len(xs))]
        sc = b.scatter(xs, [yy + o for o in off], s=22, color=PALETA["estat"] if grupo == "total" else PALETA["ref"], alpha=0.75, linewidths=0, zorder=3)
        med = b.plot([float(r["mediana_pct"])], [yy], "D", color=INK, ms=7, mfc="white", mew=1.8, zorder=5)[0]
        b.text(1.03, yy, f"{r['n_subiu']} subiram, {r['n_caiu']} caíram\nmediana {br(float(r['mediana_pct']))}%  (p = {br(float(r['p_mediana']), 2)})", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.3, color=INK)
        VALORES["fig23"]["linhas"][f"{grupo}|todas_b"] = {"x": [float(v) for v in sc.get_offsets()[:, 0]], "mediana": float(med.get_xdata()[0]),
                                                         "ref": [float(band.get_x()), float(band.get_x() + band.get_width())], "n_subiu": int(r["n_subiu"]), "n_caiu": int(r["n_caiu"])}
    b.text(1.03, -1.62, "a mediana cai dentro da faixa\nde referência: a diferença some", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.3, fontweight="bold", color=INK)
    b.set_yticks([0, -1], ["Só agressão", "Agressão + causa\nindeterminada"], fontsize=MIN_PT + 0.5)
    b.set_ylim(-1.95, 0.7), b.set_xlim(-45, 50)
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.tick_params(axis="x", labelsize=MIN_PT)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.set_xlabel("Variação da taxa do estado menos a do Brasil, %", fontsize=MIN_PT)
    b.set_title("(b) Somando as mortes de causa indeterminada, a diferença some", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.42)
    handles = [plt.Line2D([], [], marker="o", color="none", mfc=PALETA["estat"], mec="none", ms=6, label="uma troca"),
               plt.Line2D([], [], marker="D", color="none", mfc="white", mec=INK, mew=1.6, ms=6, label="mediana das trocas"),
               Rectangle((0, 0), 1, 1, fc=PALETA["excl"], label="faixa de 95% da mediana nos estados sem troca (referência)")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.02, 0.075), frameon=False, fontsize=MIN_PT, ncol=1)
    t = res[("P_todas_67", "todas", "total")]
    ti = res[("P_todas_67", "todas", "total_agr_indet")]
    moldura(fig, f"Em {t['n']} trocas de governador, a taxa do estado, relativa ao Brasil, subiu em {t['n_subiu']} e caiu em {t['n_caiu']} (mediana {br(float(t['mediana_pct']))}%); isto é exposição, não prova de causa",
            "Variação da taxa de morte por agressão do estado menos a variação do Brasil, entre os 3 anos antes e os 3 anos depois de cada troca de governador (2013-2024), por direção da troca",
            "Cada ponto roxo é uma troca de governador e mostra se a taxa do estado, comparada à do Brasil, ficou mais alta (direita) ou mais baixa (esquerda) depois dela. O losango é a mediana das trocas; a faixa cinza é onde a mediana cairia por acaso "
            "nos estados que não trocaram de governo no mesmo ano. Em (b), somando as mortes de causa indeterminada, a mediana passa a "
            f"{br(float(ti['mediana_pct']))}% ({ti['n_subiu']} subiram, {ti['n_caiu']} caíram) e entra na faixa de referência. Cuidado: a referência são poucos estados (3 a 15 por ano; em 2018-2019, 9 estados, 7 do Nordeste) e não é neutra, então uma diferença pode ser de região e não da troca.",
            "troca = mudança do partido do governador, de eleição ou não · direção = lado do escore de ideologia do partido antes e depois (esquerda, direita, centro; “mesmo bloco” = os dois do mesmo lado) · "
            "taxa relativa ao Brasil = variação do estado menos a variação do país no mesmo período, para tirar a tendência nacional · estados sem troca = referência por sorteio repetido (9.999 vezes), pareado por ano · "
            "causa indeterminada = óbito sem causa definida (CID-10 Y10-Y34), cuja fração cresceu desde 2018 · não é uma comparação com contrafactual: COVID, armas, facções e o ciclo eleitoral coincidem com as trocas · o óbito não registra orientação sexual",
            "paper/figures/fontes/c10_e2_trocas_longo.csv e c10_e2_resumo.csv, RELATORIO-EXPOSICAO.md (origem research-2026-10-24-exposicao/); pré-registro PREREGISTRO-C10.")
    salvar(fig, "fig23_trocas_de_governador_exposicao")


# ---------------------------------------------------------------- Figuras 24 a 27: guia de leitura, mortalidade no mundo, verificabilidade e hipoteses do GGB
PALETA.update({"fonte_a_cl": "#e2d8f1", "fonte_b_cl": "#d3ecea", "ref_cl": "#e4e3df"})


def _caixa(ax, x, y, w, h, txt, ec, fc, fs=MIN_PT, bold=False, cpl=15, tc=None):
    """Caixa arredondada com texto quebrado (coordenadas do eixo, em polegadas)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, "\n".join(textwrap.wrap(txt, cpl)), ha="center", va="center", fontsize=fs, color=tc or INK,
            fontweight="bold" if bold else "normal", linespacing=1.12)


def figura24() -> None:
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
         f"sem motivo útil: {br(f_ini)}% (2015) → {br(f_lo)}% a {br(f_hi)}% (2023-25)"),
        ("BO (Anuário)", "fonte_a", None, "vai à polícia", "boletim de ocorrência", "a polícia dá o enquadramento penal", f"{miles(bo0)} → {miles(bo1)} (2022-2025)"),
        ("Disque 100", "fonte_a", None, "liga e denuncia", "registro da denúncia", "o atendente classifica†", "só contagem de registros (Figura 27)"),
        ("SIM", "fonte_a", None, "morre", "declaração de óbito", "causa da morte, sim; orientação: nenhum campo", "sem número de LGBT+"),
        ("GGB e ANTRA", "ref", None, "vira notícia", "matéria", "quem coleta decide “é LGBT+” e o motivo", f"{ggb[2023]}, {ggb[2024]} e {ggb[2025]} (2023-2025)"),
    ]
    cor = {"fonte_b": (PALETA["fonte_b"], PALETA["fonte_b_cl"]), "fonte_a": (PALETA["fonte_a"], PALETA["fonte_a_cl"]), "ref": (PALETA["ref"], PALETA["ref_cl"])}
    rh, y0 = 0.64, 0.8
    VALORES["fig24"] = {"faixas": {}}
    for i, (nome, tipo, e1, e2, e3, e4, e5) in enumerate(faixas):
        y = y0 + i * (rh + 0.1)
        ec, fc = cor[tipo]
        ax.add_patch(Rectangle((0.02, y - 0.03), W - 0.04, rh + 0.06, fc=PALETA["sv_bg"], ec="none", zorder=0))
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
        _caixa(ax, cx[4], y, wc, rh, e5, ec, "white", bold=True, cpl=13 if len(e5) < 28 else 17)
        VALORES["fig24"]["faixas"][nome] = e5
    yb = y0 + 6 * (rh + 0.1) + 0.02
    ax.text(0.1, yb + 0.28, "Quem fica de fora", ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=INK)
    for k, txt in ((1, "quem não procurou serviço e quem não registrou"), (2, "o que não virou notícia"), (3, "o que ninguém anotou")):
        _caixa(ax, cx[k], yb, wc, 0.62, txt, PALETA["sv"], "white", cpl=15, tc=INK2)
    ax.text(0.05, yb + 0.82, "TSE/BRC classificam governos; Câmara e Senado registram o que se diz. Nenhuma das duas mede violência.\n† não descrito no paper", ha="left", va="center", fontsize=MIN_PT, color=INK2)
    VALORES["fig24"]["numeros"] = {"pns": [pns["lgb"], pns["het"]], "campo55": [f_ini, f_lo, f_hi], "bo": [bo0, bo1], "ggb": [ggb[2023], ggb[2024], ggb[2025]]}
    moldura(fig, "Cada fonte enxerga um pedaço diferente do caminho que o dado percorre; nenhuma mostra a violência inteira",
            "De um fato de violência até o número publicado: onde cada fonte do projeto entra e quem fica de fora em cada etapa",
            "Cada linha é uma fonte e cada coluna, uma etapa do caminho do dado: acontece, a pessoa procura serviço ou polícia, fica um papel, alguém classifica o motivo, sai a contagem. "
            "A seta tracejada da PNS mostra que ela pergunta direto à pessoa e por isso não depende de ela ter procurado ajuda. O ✗ no SIM marca o ponto em que a informação de orientação sexual deixa de existir. "
            "A figura é um esquema: a largura das etapas não representa quantidade de casos.",
            "SIM = Sistema de Informações sobre Mortalidade (Ministério da Saúde) · Sinan = ficha de notificação de violência preenchida em serviço de saúde · BO = boletim de ocorrência, reunido no Anuário Brasileiro de Segurança Pública · "
            "GGB = Grupo Gay da Bahia · ANTRA = Associação Nacional de Travestis e Transexuais · PNS = Pesquisa Nacional de Saúde, do IBGE · Disque 100 = canal de denúncias do governo federal · TSE/BRC = Justiça Eleitoral e escore de ideologia dos partidos",
            "paper/figures/fontes/seguro_pns2019.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv, serie_ggb_vs_cobertura.csv; desenho conforme o guia de leitura (G1) e a Tabela 3 do paper.")
    salvar(fig, "fig24_caminho_do_dado")


def ler_estudos() -> dict:
    """Numeros de estudos de mortalidade de fontes/estudos_mortalidade.tsv (id -> linha)."""
    return {r["id"]: r for r in ler_tsv("estudos_mortalidade.tsv")}


def figura25() -> None:
    """Mapa da evidencia internacional de mortalidade: uma linha por estudo, cada painel com a sua propria medida."""
    E = ler_estudos()
    fl = lambda k, f="valor": float(E[k][f])   # noqa: E731
    W, H = 7.4, 8.9
    fig = plt.figure(figsize=(W, H))
    tx = fig.add_axes([0, 0, 1, 1]); tx.set_xlim(0, W), tx.set_ylim(H, 0), tx.axis("off")
    xc = [0.05, 1.3, 2.6]
    for x, t in zip(xc, ("Estudo", "População e país", "Causa e medida")):
        tx.text(x, 0.08, t, ha="left", va="center", fontsize=MIN_PT + 0.5, fontweight="bold", color=INK)
    tx.text(4.1, 0.08, "Resultado (escala própria em cada linha)", ha="left", va="center", fontsize=MIN_PT + 0.5, fontweight="bold", color=INK)
    linhas = [
        ("ONS 2026", ["NÃO É BRASIL", "NÃO É HOMICÍDIO"], "Pessoas de 16 anos ou mais, Censo 2021 ligado aos óbitos; Inglaterra e País de Gales",
         "Todas as causas. Razão LGB+/heterossexuais, padronizada por idade"),
        ("ONS 2025", ["NÃO É BRASIL", "NÃO É HOMICÍDIO"], "Pessoas de 16 anos ou mais; Inglaterra e País de Gales, março de 2021 a dezembro de 2023", "Suicídio (inclui intenção indeterminada). Taxa por 100 mil, padronizada por idade"),
        ("McKetta 2024", ["NÃO É BRASIL", "NÃO É HOMICÍDIO"], f"Enfermeiras lésbicas e bissexuais (coorte), Estados Unidos; {int(fl('mck24_obitos'))} óbitos no grupo LGB",
         "Todas as causas. Fator de aceleração: menor que 1 = morre mais cedo (não é razão de riscos)"),
        ("Erlangsen 2023", ["NÃO É BRASIL", "NÃO É HOMICÍDIO"], "Pessoas trans identificadas por diagnóstico ou mudança legal de gênero (3.759); Dinamarca, 1980-2021", f"Todas as causas e suicídio ({int(fl('erl23_suicidios'))} suicídios). Razão ajustada de taxas"),
        ("Luis 2026", ["É BRASIL", "NÃO É TAXA"], "Pessoas trans notificadas por violência no Sinan e pareadas aos óbitos do SIM, 2014-2022", "Causas violentas (homicídio, suicídio e intenção indeterminada) entre os óbitos pareados; sem denominador"),
        ("Zachry 2025", ["NÃO É BRASIL", "SEM RAZÃO COMBINADA"], "Revisão sistemática de estudos de minorias sexuais e de gênero, vários países", f"Mortalidade, por estudo. {int(fl('zach25_homicidio'))} estudos têm homicídio como desfecho, direções divergentes"),
        ("McLellan 2026", ["NÃO É BRASIL", "NÃO É HOMICÍDIO"], "Adultos trans e de gênero diverso, metanálise de 94 estudos, vários países", "Violência física ou sexual ao longo da vida (prevalência). Homicídio: nenhum estudo reportou prevalência"),
    ]
    top, rh = 0.55, 1.17
    VALORES["fig25"] = {"paineis": {}}
    fs = MIN_PT
    for i, (nome, tags, pop, causa) in enumerate(linhas):
        y = top + i * rh
        tx.add_patch(Rectangle((0.02, y), W - 0.04, rh - 0.06, fc=PALETA["card"] if i % 2 == 0 else "white", ec="none", zorder=0))
        tx.text(xc[0], y + 0.12, nome, ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=INK)
        for j, tg in enumerate(tags):
            tx.text(xc[0], y + 0.36 + 0.4 * j, "\n".join(textwrap.wrap(tg, 9)), ha="left", va="center", fontsize=MIN_PT, fontweight="bold", color=PALETA["estat"] if tg == "É BRASIL" else PALETA["nao"])
        tx.text(xc[1], y + 0.08, "\n".join(textwrap.wrap(pop, 16)), ha="left", va="top", fontsize=MIN_PT, color=INK)
        tx.text(xc[2], y + 0.08, "\n".join(textwrap.wrap(causa, 16)), ha="left", va="top", fontsize=MIN_PT, color=INK2)
        ax = fig.add_axes([5.5 / W, 1 - (y + rh - 0.3) / H, 1.55 / W, 0.6 / H])
        ax.tick_params(labelsize=fs)
        ax.spines["left"].set_visible(False), ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color=GRADE, lw=0.6), ax.set_axisbelow(True)
        if nome == "ONS 2026":
            ks = [("ons26_lgb", "LGB+"), ("ons26_gl", "gays e lésbicas"), ("ons26_bi", "bissexuais"), ("ons26_gayh", "homens gays")]
            vals = []
            for k, (id_, rot) in enumerate(ks):
                yy = len(ks) - 1 - k
                eb = ax.errorbar([fl(id_)], [yy], xerr=[[fl(id_) - fl(id_, "lo")], [fl(id_, "hi") - fl(id_)]], fmt="s", ms=5, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=1.8, capsize=2)
                vals.append((float(eb.lines[0].get_xdata()[0]), erros_de(eb)[0]))
            ax.set_yticks([3, 2, 1, 0], [f"{rot}  {br(fl(id_), 2)} [{br(fl(id_, 'lo'), 2)}-{br(fl(id_, 'hi'), 2)}]" for id_, rot in ks], fontsize=fs)
            ax.axvline(1, color=INK2, lw=0.9, ls="--"), ax.set_xlim(0.95, 1.45), ax.set_ylim(-0.6, 3.6)
            ax.set_xlabel("razão LGB+/héteros (1 = igual)", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = vals
        elif nome == "ONS 2025":
            v = [fl("ons25_sui_lgb"), fl("ons25_sui_het")]
            bars = ax.barh([1, 0], v, height=0.6, color=[PALETA["lgb"], PALETA["hetero"]])
            ax.set_yticks([1, 0], [f"LGB+  {br(v[0])}", f"heterossexuais  {br(v[1])}"], fontsize=fs)
            ax.set_xlim(0, 60), ax.set_ylim(-0.6, 1.6)
            ax.set_xlabel("suicídios por 100 mil, no período", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = [float(p.get_width()) for p in bars]
        elif nome == "McKetta 2024":
            eb = ax.errorbar([fl("mck24")], [0], xerr=[[fl("mck24") - fl("mck24", "lo")], [fl("mck24", "hi") - fl("mck24")]], fmt="s", ms=6, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=1.8, capsize=2)
            ax.set_yticks([0], [f"lésbicas e bissexuais\n{br(fl('mck24'), 2)} [{br(fl('mck24', 'lo'), 2)}-{br(fl('mck24', 'hi'), 2)}]"], fontsize=fs)
            ax.axvline(1, color=INK2, lw=0.9, ls="--"), ax.set_xlim(0.5, 1.3), ax.set_ylim(-0.7, 0.7)
            ax.set_xlabel("fator de aceleração (1 = igual)", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = [(float(eb.lines[0].get_xdata()[0]), erros_de(eb)[0])]
        elif nome == "Erlangsen 2023":
            vals = []
            ids = (("erl23_todas", "todas as causas"), ("erl23_sui", "suicídio"))
            for k, (id_, rot) in enumerate(ids):
                yy = 1 - k
                eb = ax.errorbar([fl(id_)], [yy], xerr=[[fl(id_) - fl(id_, "lo")], [fl(id_, "hi") - fl(id_)]], fmt="s", ms=5.5, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=1.8, capsize=2)
                vals.append((float(eb.lines[0].get_xdata()[0]), erros_de(eb)[0]))
            ax.set_yticks([1, 0], [f"{rot}  {br(fl(id_), 1)} [{br(fl(id_, 'lo'), 1)}-{br(fl(id_, 'hi'), 1)}]" for id_, rot in ids], fontsize=fs)
            ax.axvline(1, color=INK2, lw=0.9, ls="--"), ax.set_xlim(0.8, 7.0), ax.set_ylim(-0.6, 1.6)
            ax.set_xlabel("razão trans/não trans (1 = igual)", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = vals
        elif nome == "Luis 2026":
            tot, vio = fl("luis26_pareados"), fl("luis26_violentos")
            b1 = ax.barh([0], [vio], height=0.6, color=PALETA["estat"])
            ax.barh([0], [tot - vio], left=[vio], height=0.6, color=PALETA["excl"])
            ax.text(vio / 2, 0, f"{int(vio)}", ha="center", va="center", fontsize=fs + 1, color="white", fontweight="bold")
            ax.text(vio + (tot - vio) / 2, 0, f"{int(tot - vio)}", ha="center", va="center", fontsize=fs + 1, color=INK)
            ax.set_yticks([0], ["óbitos pareados:\ncausas violentas | outras"], fontsize=fs)
            ax.set_xlim(0, tot), ax.set_ylim(-0.7, 0.7)
            ax.set_xlabel(f"{miles(tot)} óbitos ({br(100 * vio / tot)}% violentas)", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = [float(b1[0].get_width()), tot - float(b1[0].get_width())]
        elif nome == "Zachry 2025":
            n1, n2, n3 = fl("zach25_pleno"), fl("zach25_parcial"), fl("zach25_nenhum")
            ws, left = [], 0.0
            for v_, c_, tc in ((n1, PALETA["estat"], "white"), (n2, PALETA["estat_cl"], INK), (n3, PALETA["ref"], "white")):
                b = ax.barh([0], [v_], left=[left], height=0.6, color=c_)
                ws.append(float(b[0].get_width()))
                if v_ > 3:
                    ax.text(left + v_ / 2, 0, f"{int(v_)}", ha="center", va="center", fontsize=fs + 1, color=tc, fontweight="bold")
                left += v_
            ax.text(left - 0.5, 0.52, f"{int(n3)}", ha="right", va="center", fontsize=fs, color=INK, fontweight="bold")
            ax.set_yticks([0], ["estudos:\nsustenta | em parte | não acha"], fontsize=fs)
            ax.set_xlim(0, fl("zach25_estudos")), ax.set_ylim(-0.7, 0.8)
            ax.set_xlabel(f"{int(fl('zach25_estudos'))} estudos incluídos", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = ws
        else:
            eb = ax.errorbar([fl("mcl26_violencia")], [0], xerr=[[fl("mcl26_violencia") - fl("mcl26_violencia", "lo")], [fl("mcl26_violencia", "hi") - fl("mcl26_violencia")]], fmt="s", ms=6, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=1.8, capsize=2)
            ax.set_yticks([0], [f"violência na vida\n{br(fl('mcl26_violencia'), 2)}% [{br(fl('mcl26_violencia', 'lo'), 2)}-{br(fl('mcl26_violencia', 'hi'), 2)}]"], fontsize=fs)
            ax.set_xlim(0, 100), ax.set_ylim(-0.7, 0.7)
            ax.set_xlabel("% com violência na vida", fontsize=fs)
            VALORES["fig25"]["paineis"][nome] = [(float(eb.lines[0].get_xdata()[0]), erros_de(eb)[0]), fl("mcl26_homicidio")]
    moldura(fig, "Fora do Brasil, a mortalidade geral de pessoas LGB+ e trans aparece maior em estudos bem definidos, mas nenhum estudo lido dá razão de homicídio por orientação sexual",
            "Sete estudos de mortalidade e violência publicados entre 2023 e 2026: o que cada um mede, em quem e em que país",
            "Cada linha é um estudo e cada painel tem a sua própria escala: as medidas são diferentes (razão de taxas, taxa por 100 mil, fator de aceleração, contagem de estudos) e por isso não se comparam entre si, nem formam um único “risco”. "
            "Os rótulos em vinho avisam o que o estudo NÃO é: não é Brasil, não é homicídio. Só o estudo de Luis (2026) é brasileiro e não traz taxa, por falta de denominador.",
            "razão de taxas = quantas vezes a mortalidade de um grupo é maior que a do outro, depois de igualar as idades · LGB+ = lésbicas, gays, bissexuais e outras orientações · fator de aceleração = menor que 1 quer dizer que o tempo até o óbito é mais curto · "
            "causas violentas = homicídio, suicídio e intenção indeterminada, juntos · Sinan = ficha de notificação de violência de serviço de saúde · SIM = base de atestados de óbito · "
            "estudos descritivos: nenhum deles permite dizer que a orientação sexual causa a diferença",
            "paper/figures/fontes/estudos_mortalidade.tsv, com números literais de L-SECAO-3-3-PROPOSTA.md (frente L, tabela “De onde vem cada número”).")
    salvar(fig, "fig25_mortalidade_internacional")


def figura26() -> None:
    """Fluxo de verificabilidade da lista do GGB de 2019: 160 sorteados -> recuperados -> correspondentes -> morte violenta -> critérios; motivo entre as mortes violentas."""
    js = json.loads((FONTES / "ggb_validacao_resumo.json").read_text(encoding="utf-8"))
    n0, n1, n2, n3, n4 = js["n_amostra"], js["recuperadas"], js["correspondem"], js["morte_violenta"], js["verificavel_estrito"]
    mot = js["motivo_entre_morte_violenta_confirmada"]
    nr = js["motivo_nao_recuperacao"]
    fig = plt.figure(figsize=(7.2, 7.2))
    a = fig.add_axes([0.02, 0.5, 0.96, 0.46])
    b = fig.add_axes([0.40, 0.09, 0.2, 0.27])
    etapas = [(n0, "casos sorteados da lista de 2019"), (n1, "com a matéria recuperada"), (n2, "em que a matéria é do caso"), (n3, "com morte violenta confirmada"), (n4, "e a fonte diz expressamente que a vítima é LGBT+")]
    saidas = [f"{n0 - n1} sem matéria recuperada: {nr['link_morto_404']} link morto, {nr['dominio_inacessivel']} site inacessível, {nr['bloqueio_ou_erro_servidor']} bloqueio ou erro, {nr['sem_link_no_anexo4']} sem link: não dá para verificar",
              f"{n1 - n2} em que a matéria não é a do caso",
              f"{n2 - n3} sem morte violenta confirmada (indeterminada ou não violenta)",
              f"{n3 - n4} com morte violenta, mas sem a identificação expressa como LGBT+ na fonte", ""]
    y = list(range(5))[::-1]
    bars = a.barh(y, [e[0] for e in etapas], height=0.62, left=[-e[0] / 2 for e in etapas], color=[PALETA["estat"] if i in (0, 4) else PALETA["estat_cl"] for i in range(5)])
    for (n, rot), yy in zip(etapas, y):
        a.text(0, yy, f"{n}", ha="center", va="center", fontsize=11, fontweight="bold", color="white" if n in (n0, n4) else INK)
        a.text(-149, yy, "\n".join(textwrap.wrap(rot, 26)), ha="left", va="center", fontsize=MIN_PT, color=INK, clip_on=False, transform=a.transData)
    for yy, s_ in zip(y, saidas):
        if s_:
            a.text(86, yy - 0.5, "\n".join(textwrap.wrap(s_, 42)), ha="left", va="center", fontsize=MIN_PT, color=INK2, clip_on=False)
    a.set_xlim(-150, 235), a.set_ylim(-0.6, 4.6), a.axis("off")
    VALORES["fig26"] = {"etapas": [float(p.get_width()) for p in bars]}
    ordem = [("U", "motivo desconhecido ou não reportado"), ("C", "conflito interpessoal"), ("R", "roubo ou latrocínio"), ("P", "passional"), ("S", "suicídio"), ("V", "LGBTfobia atribuída na própria fonte")]
    yb = list(range(len(ordem)))[::-1]
    bb = b.barh(yb, [mot[k] for k, _ in ordem], height=0.62, color=[PALETA["estat"] if k in ("U", "V") else PALETA["estat_cl"] for k, _ in ordem])
    for (k, rot), yy in zip(ordem, yb):
        b.text(mot[k] + 1, yy, f"{mot[k]}  ({br(100 * mot[k] / n3)}%)", va="center", fontsize=MIN_PT, color=INK, fontweight="bold" if k in ("U", "V") else "normal")
    b.set_yticks(yb, [r for _, r in ordem], fontsize=MIN_PT)
    b.set_xlim(0, 55), b.tick_params(axis="x", labelsize=MIN_PT)
    b.set_xlabel(f"mortes violentas confirmadas (n = {n3})", fontsize=MIN_PT + 0.3)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.set_title("(b) O motivo que a própria fonte registra", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-1.2)
    a.text(-149, 4.95, "(a) De 160 casos sorteados a 50 com todos os critérios", fontsize=9.5, fontweight="bold", color=INK, va="bottom")
    VALORES["fig26"]["motivos"] = {k: float(p.get_width()) for (k, _), p in zip(ordem, bb)}
    moldura(fig, f"Dos {n0} casos sorteados da lista do GGB de 2019, {n4} ({br(100 * n4 / n0, 1)}%) puderam ser verificados nos critérios do paper; LGBTfobia aparece como motivo em só {mot['V']} das {n3} mortes violentas",
            "Lista de casos do relatório de 2019 do GGB, amostra aleatória de 160: em cada etapa, quantos casos continuam a poder ser conferidos",
            "Em (a), cada barra é quantos casos passaram por uma etapa de conferência; a que sobra à direita explica o que saiu: casos sem matéria recuperada ou fora do critério são casos que não deu para verificar, nunca casos considerados falsos. "
            "A largura é proporcional ao número de casos. Em (b), entre as mortes violentas confirmadas, o que a própria fonte (matéria, polícia, família) diz ser o motivo; o motivo vem da fonte, não do codificador. "
            "Nenhum caso é identificado: só contagens.",
            "verificável = a matéria foi recuperada, é do caso, confirma morte violenta e identifica a vítima como LGBT+ de forma expressa · amostra de 160 de 329 casos da lista nominal de 2019 · "
            "motivo desconhecido = a fonte não informa motivo · “não dá para verificar” não é o mesmo que “falso”: o paper não usa essa palavra · GGB = Grupo Gay da Bahia · latrocínio = roubo seguido de morte",
            "paper/figures/fontes/ggb_validacao_resumo.json (origem research-2026-10-21-rodada3/F3-ggb/dados/validacao_resumo.json); conferido contra codificacao_A.csv no teste.")
    salvar(fig, "fig26_ggb_verificabilidade")


def figura27() -> None:
    """Curva de hipoteses do GGB: cobertura N/(E0*RR) para cada risco relativo hipotetico, em 2023 e 2024."""
    rows = [r for r in ler_csv("c08_numeradores.csv") if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False"]
    fig = plt.figure(figsize=(7.2, 4.6))
    gs = fig.add_gridspec(1, 2, wspace=0.12, left=0.09, right=0.98, top=0.9, bottom=0.2)
    xs = np.logspace(math.log10(0.06), math.log10(8), 80)
    est = {"N0": ("todas as mortes declaradas", PALETA["estat"], "-"), "N1": ("só homicídios e latrocínios", PALETA["estat"], "--"),
           "N2": ("cenário de subtração (sem pessoas trans)", PALETA["ref"], ":")}
    VALORES["fig27"] = {"curvas": {}, "rr_cobertura_100": {}}
    axs = []
    for k, ano in enumerate(("2023", "2024")):
        ax = fig.add_subplot(gs[k], sharey=axs[0] if axs else None)
        axs.append(ax)
        for r in [x for x in rows if x["ano"] == ano]:
            n, E0 = float(r["n"]), float(r["E_RR1.0"])
            nome, cor, ls = est[r["numerador"]]
            ln, = ax.plot(xs, 100 * n / (E0 * xs), ls, color=cor, lw=2.2, label=nome if k == 0 else None)
            VALORES["fig27"]["curvas"][f"{ano}|{r['numerador']}"] = {"x": [float(v) for v in ln.get_xdata()], "y": [float(v) for v in ln.get_ydata()]}
            rr = n / E0
            m, = ax.plot([rr], [100], "D", color=cor, mfc="white", mew=1.8, ms=7, zorder=5)
            VALORES["fig27"]["rr_cobertura_100"][f"{ano}|{r['numerador']}"] = float(m.get_xdata()[0])
            if r["numerador"] in ("N0", "N2"):
                ax.annotate(f"RR {br(rr, 2)}", (rr, 100), xytext=(-9 if r["numerador"] == "N0" else 0, 14 if r["numerador"] == "N0" else -16), textcoords="offset points", ha="right" if r["numerador"] == "N0" else "center", fontsize=MIN_PT, color=INK, fontweight="bold", bbox={"fc": "white", "ec": "none", "pad": 1.2})
        ax.set_xscale("log"), ax.set_yscale("log")
        ax.axhline(100, color=INK2, lw=0.9, ls="--")
        for rr_ in (1, 2.82, 3.84):
            ax.axvline(rr_, color=GRADE, lw=1.2, zorder=0)
        ax.set_xlim(0.06, 8), ax.set_ylim(1.5, 450)
        ax.set_xticks([0.1, 0.25, 0.5, 1, 2.82, 3.84], ["0,1", "0,25", "0,5", "1", "2,82", "3,84"], fontsize=MIN_PT)
        for lab, ha_ in zip(ax.get_xticklabels(), ("center",) * 4 + ("right", "left")):
            lab.set_ha(ha_)
        ax.set_yticks([2, 5, 10, 20, 50, 100, 200, 400], ["2", "5", "10", "20", "50", "100", "200", "400"], fontsize=MIN_PT)
        ax.set_xlabel("RR hipotético (risco dos LGB+ ÷ pares)", fontsize=MIN_PT)
        ax.grid(axis="y", color=GRADE, lw=0.5), ax.set_axisbelow(True)
        ax.set_title(f"({'ab'[k]}) {ano}", loc="left", fontsize=9.5, fontweight="bold", color=INK)
        if k == 0:
            ax.set_ylabel("Cobertura = contagem ÷ mortes esperadas, %", fontsize=MIN_PT)
        else:
            ax.legend(*axs[0].get_legend_handles_labels(), frameon=False, fontsize=MIN_PT, loc="lower left", handlelength=2.2)
            plt.setp(ax.get_yticklabels(), visible=False)
    r0 = [x for x in rows if x["ano"] == "2023" and x["numerador"] == "N0"][0]
    r1 = [x for x in rows if x["ano"] == "2024" and x["numerador"] == "N0"][0]
    seta(axs[0], "100% de cobertura\nexigiria risco bem\nmenor que o dos pares:\né conta, não estimativa", (float(r0["n"]) / float(r0["E_RR1.0"]), 100), (0.5, 250), va="center", ha="left")
    moldura(fig, f"A contagem do GGB só cobriria 100% das mortes esperadas se adultos LGB+ tivessem risco de {br(float(r0['n']) / float(r0['E_RR1.0']), 2)} a {br(float(r1['n']) / float(r1['E_RR1.0']), 2)} vezes o dos pares: é uma conta de hipótese, não uma estimativa",
            "Cobertura da contagem do GGB (mortes declaradas ÷ mortes esperadas) para cada risco de morte hipotético dos adultos LGB+, 2023 e 2024",
            "Quanto maior o risco que se supõe para os LGB+, mais mortes seriam esperadas e menor a cobertura da contagem; no eixo vertical, 100% é a contagem igual ao esperado. Cada losango mostra o risco em que a cobertura chegaria a 100%: "
            "é só uma conta feita de trás para a frente, para mostrar a escala, e não diz qual é o risco: o risco verdadeiro não foi medido. As linhas cinza claras marcam os riscos 1, 2,82 e 3,84 usados no paper.",
            "RR = risco relativo: quantas vezes o risco de morte por agressão dos LGB+ seria o dos pares (mesmo sexo, raça e idade) · esperadas = mortes que ocorreriam em 1,89% da população adulta (PNS 2019) sob esse risco · "
            "cenário de subtração = a contagem sem as pessoas trans da tabela de identidade do GGB: é um limite de comparação, não uma estimativa de mortes LGB+ · escalas logarítmicas",
            "paper/figures/fontes/c08_numeradores.csv (origem dados/ggb/c08_numeradores.csv), agressão, prevalência de 1,89%, sem proxy.")
    salvar(fig, "fig27_ggb_curva_de_hipoteses")


D100_QUEBRAS = [(2020.0, "2020S1: formato B"), (2020.5, "2020S2: formato C"), (2022.5, "2022S2: formulário novo"), (2024.0, "2024: motivação sai")]


def ler_d100() -> dict:
    """Serie anual do Disque 100 por ano: unidade usada (linhas 2011-2020; denuncias 2021-2026), modulo LGBT e canal."""
    lin = {(int(r["ano"]), r["recorte"], r["unidade"]): int(r["n"]) for r in ler_csv("d100_serie_anual.csv")}
    out: dict = {}
    for ano in range(2011, 2027):
        un = "linhas" if ano <= 2020 else "denuncias"
        out[ano] = {"unidade": un, "lgbt": lin[(ano, "grupo_lgbt", un)], "canal": lin[(ano, "canal", un)]}
    return out


def figura28() -> None:
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
    barras = b.bar([xm[x] for x in anos], [v / 1000 for v in alt], width=0.72, color=[PALETA["estat_cl"] if d[x]["unidade"] == "denuncias" else PALETA["excl"] for x in anos],
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
    VALORES["fig28"] = {"anos": anos, "lgbt": [float(v) for v in [*la.get_ydata(), *l20.get_ydata(), *lc.get_ydata()]],
                        "canal_mil": [float(p_.get_height()) for p_ in barras],
                        "pct_texto": [t_.get_text() for t_ in b.texts if t_.get_text().endswith("%")], "pct": [float(v) for v in pcts],
                        "quebras": [float(v.get_xdata()[0]) for v in vl], "unidade": [d[x]["unidade"] for x in anos]}
    r21, r25 = d[2021], d[2025]
    moldura(fig, f"Denúncia não é violência: de 2021 a 2025 o módulo LGBT do Disque 100 foi de {miles(r21['lgbt'])} a {miles(r25['lgbt'])} denúncias ({br(r25['lgbt'] / r21['lgbt'])} vezes) e o canal inteiro de {miles(round(r21['canal'], -3) / 1000)} mil a {miles(round(r25['canal'], -3) / 1000)} mil ({br(r25['canal'] / r21['canal'])} vezes), com a série quebrada em quatro pontos",
            "Registros do Disque 100 (arquivos públicos de 2011 a setembro de 2026): módulo LGBT por ano, com a unidade de cada trecho, e canal inteiro com a parte do módulo LGBT",
            "Em (a), a linha cinza é o número de linhas do módulo LGBT nos arquivos de 2011-2019 (cada linha é uma vítima em um atendimento, não uma pessoa); a roxa, de 2021 em diante, conta denúncias com ao menos uma linha do módulo; o losango é 2020, que mistura dois formatos. "
            "As linhas pontilhadas verticais marcam onde o formato do arquivo ou do formulário mudou: a série não é contínua entre elas. "
            "Em (b), cada barra é o canal inteiro na mesma unidade do painel (a) e o número em cima é a parte do módulo LGBT: o canal inteiro cresceu junto, e por isso mais denúncias não quer dizer mais violência.",
            "Disque 100 = canal federal de denúncias de violações de direitos humanos (Ministério dos Direitos Humanos e da Cidadania) · linha = uma linha do arquivo público · denúncia = um atendimento, com chave própria desde 2020S2 · "
            "módulo LGBT = linhas em que o grupo da denúncia é LGBT · não há chave de pessoa: o total de vítimas únicas não é calculável em nenhum ano · * 2026 vai de janeiro a setembro, e a barra hachurada é parcial · "
            "a unidade em (b) é a mesma de (a): linhas até 2020 e denúncias depois, por isso a barra de 2021 é menor que a de 2020",
            "paper/figures/fontes/d100_serie_anual.csv (origem dados/disque100/saidas/d100_serie_anual.csv; microdados oficiais do Disque 100 em dadosabertos.mdh.gov.br, catálogo com sha256 em dados/disque100/saidas/catalogo.tsv).")
    salvar(fig, "fig28_disque100_serie")


def main() -> None:
    """Gera as vinte e oito figuras, os valores plotados e o SHA256SUMS."""
    figs = (figura1, figura2, figura3, figura4, figura5, figura6, figura7, figura8, figura9, figura10, figura11, figura12,
            figura13, figura14, figura15, figura16, figura17, figura18, figura19, figura20, figura21, figura22, figura23, figura24, figura25, figura26, figura27, figura28)
    for f in figs:
        f()
    (AQUI / "valores_plotados.json").write_text(json.dumps(VALORES, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    arquivos = sorted(p for p in AQUI.iterdir() if p.suffix in {".pdf", ".svg", ".png", ".json", ".py"}) + \
        sorted(p for p in FONTES.iterdir() if p.is_file())
    linhas = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(AQUI)}" for p in arquivos]
    (AQUI / "SHA256SUMS").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"[OK] {len(figs)} figuras (PDF+SVG+PNG), valores_plotados.json, SHA256SUMS ({len(linhas)} arquivos)")


if __name__ == "__main__":
    main()
