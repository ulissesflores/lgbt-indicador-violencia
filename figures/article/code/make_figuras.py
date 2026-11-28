# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Draw the 22 article figures in Portuguese or English as vector files, no background.

Reads the figure source data copied into the repository and draws figures 1, 2, 3, 6, 8, 9, 10,
11, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27 and 28 as SVG and PDF with a transparent
background. It is an adapted copy of the repository figure generator: only the language and the
output format change. Every drawn text goes through a translation function, and the run aborts
listing all English keys that lack an entry. Title and source are recorded, not drawn. Final
English texts are checked for accents and Portuguese words, and the PDF text is read with
pdftotext.

Inputs
------
- figures/fontes/ (copies of the source data of the figures)
- figures/article/code/rotulos/<language>.json (label tables)
- figures/article/code/bidi_he.py (loaded for Hebrew)

Outputs
-------
- .run/figuras-artigo/<language>/<figure>.svg and .pdf (default folder, not tracked in git;
  changed with --saida)
- .run/figuras-artigo/valores/<language>/valores_plotados.json
- .run/figuras-artigo/valores/<language>/textos_fora_da_imagem.json

Usage
-----
PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras.py --lang en
[--saida <folder>]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Figuras do paper em duas versoes (pt-BR e en), vetoriais (SVG + PDF) e SEM fundo, a partir das copias de dados
do repositorio publicado (SOMENTE LEITURA): figures/fontes/ na raiz do pacote.

Derivado de `figures/make_figures.py` do repositorio (copia adaptada, nao import): o desenho, a PALETA, os tamanhos e as
quebras sao os do original; muda so o idioma e o formato de saida. As 22 figuras usadas no paper:
fig1, 2, 3, 6, 8, 9, 10, 11, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28 (as demais do original, 4, 5, 7, 12,
16 e 24, nao entram).

Idioma. `--lang pt-BR|en`. Todo texto desenhado dentro da imagem (rotulos, anotacoes, legendas, titulos de painel, ticks
textuais) passa por `T()`, instalada em `Text.set_text` do matplotlib: nenhum texto escapa. O texto-fonte e sempre o
portugues; em pt-BR `T()` devolve o proprio texto; em en procura o texto na tabela `EN` (chave = texto pt com os numeros
trocados por `{}` e os espacos/quebras normalizados). Numeros: `br()` e `miles()` formatam por idioma (pt: virgula decimal
e ponto de milhar; en: ponto decimal e virgula de milhar), com o mesmo arredondamento ROUND_HALF_UP; numeros literais
escritos no texto-fonte em formato pt sao convertidos para en. Sem entrada na tabela, `--lang en` FALHA (SystemExit) listando
todas as chaves que faltam; depois conferimos que nenhum texto final em en tem acento nem palavra portuguesa obvia.

Saidas (e nada em outro lugar), sob --saida (padrao <raiz>/.run/figuras-artigo/):
  <saida>/<lang>/<nome>.svg e .pdf     (fundo transparente; texto em contorno no SVG)
  <saida>/valores/<lang>/valores_plotados.json e textos_fora_da_imagem.json
Titulo e "Fonte:" da figura nao sao desenhados (`moldura()` so registra), como no original.

Uso: PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras.py --lang en [--saida <pasta>]
A raiz do pacote vem de Path(__file__).resolve().parents[3]; a variavel de ambiente REPO_ROOT a substitui.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.text import Text  # noqa: E402
from matplotlib.ticker import ScalarFormatter  # noqa: E402

REPO_ROOT = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[3])   # raiz do pacote
FONTES = REPO_ROOT / "figures" / "fontes"   # somente leitura
LANG = "pt-BR"                 # definido em main()
TAB: dict = {}                 # tabela de rotulos do idioma (en = EN; es/it/he = rotulos/<lang>.json), definida em main()


def _virgula() -> bool:
    """Formato de NUMERO (nao de idioma-fonte): pt-BR, es e it usam virgula decimal e ponto de milhar; en e he, o inverso."""
    return LANG in ("pt-BR", "es", "it")
SAIDA: Path = REPO_ROOT / ".run" / "figuras-artigo"   # trocada por --saida em main()

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
    "svg.fonttype": "path",          # texto em contorno: o SVG nao depende de fonte instalada
    "savefig.transparent": True,     # sem fundo (figura e eixos transparentes)
    "pdf.fonttype": 42,
})

VALORES: dict = {}


# Numeros dinamicos saem de br()/miles() envolvidos por dois marcadores invisiveis: T() os reconhece como parametros ja
# formatados no idioma (os marcadores nunca chegam ao arquivo final).
S0, S1 = "\u2063", "\u2064"


def _arred(x: float, casas: int) -> Decimal:
    """Arredonda MEIO PARA CIMA (31,25 -> 31,3), como o texto do paper; nao o arredondamento do banqueiro do Python."""
    return Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)


def br(x: float, casas: int = 1) -> str:
    """Numero com `casas` decimais no idioma da execucao: pt-BR com virgula decimal (31,3); en com ponto decimal (31.3)."""
    t = f"{_arred(x, casas):.{casas}f}".replace("-", "\u2212")   # sinal de menos (U+2212), como no texto; o hifen nao e menos (r35)
    return S0 + (t.replace(".", ",") if _virgula() else t) + S1


def apa(x: float, casas: int) -> str:
    """Valor que nao passa de 1 em modulo (p, rho) em APA 7, como no texto: sem zero a esquerda (,58; −,43) (r40)."""
    return br(x, casas).replace("0,", ",", 1).replace("0.", ".", 1)


# p em italico (APA 7) pelo mathtext do matplotlib; no texto em negrito, italico negrito (r40)
P_IT, P_IT_NEGRITO = "$p$", r"$\mathbfit{p}$"


def miles(n: float) -> str:
    """Inteiro com separador de milhar no idioma da execucao: pt-BR 3.481; en 3,481."""
    t = f"{int(_arred(n, 0)):,}".replace("-", "\u2212")   # sinal de menos (U+2212) (r35)
    return S0 + (t.replace(",", ".") if _virgula() else t) + S1


def num_pt_en(tok: str) -> str:
    """Converte um numero literal escrito no texto-fonte em formato pt (3.481 / 2,82) para en (3,481 / 2.82)."""
    return tok.replace(".", "\0").replace(",", ".").replace("\0", ",")


def wilson(k: int, n: int) -> tuple[float, float]:
    """IC95% de Wilson para k de n (mesma formula usada nos scripts de origem)."""
    z, p = 1.959963984540054, k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def ler_tsv(nome: str) -> list[dict]:
    """TSV de `sources/public/` como lista de dicts."""
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8"), delimiter="\t"))


def ler_csv(nome: str) -> list[dict]:
    """CSV de `sources/public/` como lista de dicts."""
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8")))


class _Virgula(ScalarFormatter):
    """Rotulo numerico de eixo com virgula decimal (PT-BR): 0,25 e nao 0.25."""

    def __call__(self, x, pos=None):
        return super().__call__(x, pos).replace(".", ",")


def salvar(fig, nome: str) -> None:
    """Grava SVG e PDF (sem fundo, sem data nos metadados) em docs/paper/figuras/<lang>/; eixos numericos no idioma."""
    global _FIG_ATUAL
    _FIG_ATUAL = nome
    if _virgula():
        for ax in fig.axes:
            for eixo in (ax.xaxis, ax.yaxis):
                if type(eixo.get_major_formatter()) is ScalarFormatter:
                    eixo.set_major_formatter(_Virgula())
    TEXTOS[nome] = dict(_PENDENTE)
    _PENDENTE.clear()
    fig.canvas.draw()                  # materializa os rotulos dos eixos (passam por T) antes da conferencia
    conferir_textos(fig, nome)
    if _FALTAM:
        raise SystemExit(f"[ERRO] {len(_FALTAM)} texto(s) sem traducao em EN (a figura nao e confiavel e nao foi gravada):\n" +
                         "\n".join(f"  {f}: {k!r}" for k, f in _FALTAM.items()))
    _NOMES.append(nome)
    pasta = SAIDA / LANG
    pasta.mkdir(parents=True, exist_ok=True)
    kw = {"bbox_inches": "tight", "pad_inches": 0.12}
    fig.savefig(pasta / f"{nome}.pdf", metadata={"CreationDate": None, "ModDate": None}, **kw)
    fig.savefig(pasta / f"{nome}.svg", metadata={"Date": None}, **kw)
    plt.close(fig)


def erros_de(eb) -> list[list[float]]:
    """Extremos (lo, hi) de cada barra de erro horizontal, lidos dos segmentos desenhados."""
    segs = eb.lines[2][0].get_segments()
    return [[float(s[0][0]), float(s[1][0])] for s in segs]


# ---------------------------------------------------------------- moldura: textos fora da imagem (regra APA)
def moldura(fig, titulo: str, subtitulo: str, como_ler: str, termos: str, fonte: str) -> None:
    """Registra titulo-conclusao, subtitulo, 'Como ler', termos e fonte da figura SEM desenha-los.

    Regra APA do artigo: esses textos ficam no documento (titulo acima; Nota e Fonte abaixo), e a imagem
    leva so o grafico com as suas chaves de leitura. `salvar()` grava o registro pendente em
    `textos_fora_da_imagem.json`, com o nome do arquivo da figura.
    """
    _PENDENTE.clear()
    _PENDENTE.update({k: limpa(v) for k, v in dict(titulo_conclusao=titulo, subtitulo=subtitulo, como_ler=como_ler, termos=termos, fonte=fonte).items()})


_PENDENTE: dict = {}
TEXTOS: dict = {}


def seta(ax, texto: str, alvo: tuple, ponto_texto: tuple, rad: float = 0.15, **kw) -> None:
    """Anotacao com seta para a mensagem principal (texto em tinta escura, seta cinza); `rad` = curvatura da seta."""
    ax.annotate(texto, xy=alvo, xytext=ponto_texto, fontsize=MIN_PT + 0.5, color=INK, fontweight="bold",
                arrowprops={"arrowstyle": "->", "color": INK2, "lw": 1.3, "shrinkA": 2, "shrinkB": 3,
                            "connectionstyle": f"arc3,rad={rad}"}, **kw)


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
            "figures/fontes/seguro_pns2019.csv (origem data/pns/seguro_pns2019.csv), desenho amostral complexo.")
    salvar(fig, "fig1_pns2019_vitimizacao")


# ---------------------------------------------------------------- Figura 2: cobertura do GGB
def ler_c08() -> list[dict]:
    """Linhas do teste de escala com desfecho agressao e prevalencia 1,89%, anos com SIM (2023, 2024)."""
    rows = ler_csv("c08_numeradores.csv")
    return [r for r in rows if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False"]


def figura2() -> None:
    """Cobertura implicita (n / esperado) por ano, numerador e cenario de risco relativo."""
    rows = ler_c08()
    # rotulos em ate 3 linhas curtas: com o rotulo numa linha so a figura passava de 10 polegadas e, na largura unica do
    # artigo (14 cm), o texto encolhia para menos de 5 pt
    nomes = {"N0": "total declarado", "N1": "numerador A: homicídios\ne latrocínios", "N2": "numerador B: cenário de\nsubtração (sem pessoas trans)"}
    fig = plt.figure(figsize=(7.2, 4.8))
    fig.subplots_adjust(left=0.31, right=0.97)
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
            "figures/fontes/c08_numeradores.csv (origem data/ggb/c08_numeradores.csv), prevalência LGB+ de 1,89%.")
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
    F3 = 9.5  # E5: menor corpo desta figura (cerca de 7 pol impressas a 14 cm -> >= 7 pt)
    fig, (a, b) = plt.subplots(2, 1, figsize=(6.9, 7.5), gridspec_kw={"height_ratios": [1.12, 1], "hspace": 0.62})
    fig.subplots_adjust(left=0.30, right=0.97, top=0.95, bottom=0.085)
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
    # r35: o rotulo (IC da barra cheia) comeca depois da ponta mais a direita das duas barras do grupo, com 8 pt de folga; antes
    # ele partia da ponta da barra cheia e a ponta da barra vazada, logo abaixo, encostava no inicio do texto
    ic_vazado = dict(zip(VALORES["fig3"]["agressao_mais_indet_ln"]["grupos"], VALORES["fig3"]["agressao_mais_indet_ln"]["ic"]))
    for g, (l_, h_) in zip(VALORES["fig3"]["registrado_ln"]["grupos"], VALORES["fig3"]["registrado_ln"]["ic"]):
        x_rot = max(h_, ic_vazado.get(g, (0, h_))[1])
        a.annotate(f"{br(l_)}% a +{br(h_)}%", (x_rot, y[grupos.index(g)] + off), xytext=(8, -3), textcoords="offset points", fontsize=F3, color=INK)
    a.axvline(0, color=INK2, lw=0.9, ls="--")
    a.set_yticks(y, [nomes[g] for g in grupos], fontsize=F3 + 0.5)
    a.set_xlim(-24, 46)
    a.tick_params(axis="x", labelsize=F3)
    a.set_xlabel("Variação da taxa ao trocar o governador do PT\npor DEM ou PL (5 pontos de ideologia), %", fontsize=F3)
    # r35: sem grade vertical (a de 20 e a de 30 cortavam os rotulos de intervalo; o zero tracejado fica)
    a.legend(frameon=False, fontsize=F3, loc="upper center", bbox_to_anchor=(0.38, -0.28), ncol=2, columnspacing=1.0, handletextpad=0.4)
    a.set_ylim(-0.6, y[0] + 1.6)
    a.set_title("(a) Painel por estado e ano", loc="left", fontsize=F3 + 1, fontweight="bold", color=INK)
    a.annotate("a faixa inclui zero:\nnão se distingue de zero", xy=(0.6, y[0] + off + 0.25), xytext=(9, y[0] + 1.05), fontsize=F3, color=INK,
               fontweight="bold", va="center", arrowprops={"arrowstyle": "->", "color": INK2, "lw": 1.3, "shrinkA": 2, "shrinkB": 3,
                                                          "connectionstyle": "arc3,rad=0.15"})

    c03 = ler_c03()
    lado = {"esquerda->direita": "deslocamento para a direita", "direita->esquerda": "deslocamento para a esquerda"}  # sinal do escore, não troca de bloco (AST-03, r5)
    jan = {"estrito": "janela completa", "truncado": "janela curta"}
    rot_ev, pts, lo, hi = [], [], [], []
    for r in c03:
        p = float(r["p_antecipacoes"])
        aviso = f"já mudava antes ({P_IT} = {apa(p, 3)})" if p < 0.05 else f"mudança anterior não detectada ({P_IT} = {apa(p, 2)})"  # não significância não prova ausência (AST-R2-09)
        rot_ev.append(f"{lado[r['direcao']]}\n{jan[r['desenho']]}, {r['n_eventos']} trocas\n{aviso}")
        m, l_, h_ = (100 * (math.exp(float(r[k])) - 1) for k in ("media_pos", "media_pos_lo", "media_pos_hi"))
        pts.append(m), lo.append(m - l_), hi.append(h_ - m)
    yb = list(range(len(c03)))[::-1]
    eb = estat_cheio(b, pts, yb, xerr=[lo, hi])
    VALORES["fig3"]["event_study"] = {"rotulos": [f"{r['desenho']}|{r['direcao']}" for r in c03],
                                      "pontos": [float(v) for v in eb.lines[0].get_xdata()], "ic": erros_de(eb)}
    for xv, yv in zip(pts, yb):
        b.annotate(f"{br(xv)}%", (xv, yv), xytext=(0, 7), textcoords="offset points", fontsize=F3, color=INK, ha="center")
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_yticks(yb, rot_ev, fontsize=F3)
    b.set_xlim(-40, 10)
    b.set_ylim(-0.6, 3.75)
    b.tick_params(axis="x", labelsize=F3)
    b.set_xlabel("Variação média da taxa depois da troca,\ncomparada a estados sem troca (%)", fontsize=F3)
    # r35: sem grade vertical (a de -20 cortava "-19,9%" e "-18,6%")
    b.set_title("(b) Deslocamento do escore: a mesma queda nos dois sentidos", loc="left", fontsize=F3 + 1, fontweight="bold", color=INK)
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
            "figures/fontes/c02_indet_resultados.csv e c03_event_pesos_resultados.csv (origem data/painel/). Exploratório, não causal.")
    salvar(fig, "fig3_governos_painel_eventos")



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
            "figures/fontes/seguro_pns2019.csv (origem data/pns/seguro_pns2019.csv).")
    salvar(fig, "fig6_proporcao_1_em_7")



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
            "figures/fontes/asr_brasil.csv (origem data/sim/asr_brasil.csv; SIM, Ministério da Saúde).")
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
    ax.set_xticks([-30, -20, -10, 0, 10, 20, 30], ["\u221230", "\u221220", "\u221210", "0", "+10", "+20", "+30"], fontsize=MIN_PT)
    ax.set_xlabel("Variação da taxa de homicídio ao trocar PT por DEM ou PL (5 pontos de ideologia), %", fontsize=MIN_PT)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, fc=PALETA["excl"]), Rectangle((0, 0), 1, 1, fc=PALETA["estat_cl"]), pts[0]],
              labels=["excluído pelos dados", "compatível com os dados", "melhor estimativa"], frameon=False, fontsize=MIN_PT,
              loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3)
    seta(ax, "faixa compatível\ncom os dados", (lims[0][1] + 0.3, y[0] + 0.3), (17, y[0] + 1.05), va="center")
    ax.set_ylim(-0.6, 6.3)
    VALORES["fig9"] = {"grupos": grupos,
                       "ic": [[float(p.get_x()), float(p.get_x() + p.get_width())] for p in azuis],
                       "pontos": [float(q.get_xdata()[0]) for q in pts]}
    minimo = min(min(-lo, hi) for lo, hi in lims)
    maximo = max(max(-lo, hi) for lo, hi in lims)
    moldura(fig, f"No painel de governadores, as variações da taxa de homicídios compatíveis com os dados chegam a {br(minimo)}% a {br(maximo)}%, conforme o grupo e o sentido, e todos os intervalos incluem zero",
            "Faixa de variação da taxa registrada de morte por agressão compatível com os dados, por grupo, numa troca de PT por DEM ou PL",
            "A barra roxa clara é o que os dados ainda permitem: do que seria uma queda ao que seria uma alta. O cinza é o que o painel exclui. "
            "Como a barra sempre inclui zero, o resultado é “não sei se houve efeito”, e não “não houve efeito”: efeitos pequenos, dentro da barra clara, continuam compatíveis com os dados.",
            "intervalo normal (a inversão do bootstrap wild-cluster, na Tabela 6 do paper, é um pouco mais larga) · painel = 351 combinações de estado e ano, 2012-2024 · 5 pontos de ideologia = distância média entre o PT (2,97) e DEM ou PL (cerca de 8) numa escala de 0 a 10 · "
            "exploratório: não prova causa · base: a taxa registrada, que pode esconder mortes de causa indeterminada",
            "figures/fontes/c02_indet_resultados.csv (origem data/painel/c02_indet_resultados.csv); IC95% com erro-padrão agrupado por estado.")
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
    a.set_yticks([0, 1000, 2000, 3000, 4000], ["0", miles(1000), miles(2000), miles(3000), miles(4000)])
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
            "figures/fontes/sim_identificabilidade_resumo.json (origem analysis/simulation/resumo.json); incidência e propensão recalculadas da fórmula do paper.")
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
    ghost = a.barh(y, [d["v1"][f] for f in fam], height=0.72, color=PALETA["excl"], label="dicionário pré-registrado (casa palavras demais)")
    sol = a.barh(y, [d["v2"][f] for f in fam], height=0.4, color=PALETA["estat"], label="dicionário revisto (contagem usada)")
    for f, yy in zip(fam, y):
        a.text(d["v1"][f] + 12, yy, f"{d['v1'][f]}", va="center", fontsize=MIN_PT, color=INK2)
        v2 = d["v2"][f]
        a.text(1.04, yy, f"{v2} falas  ({br(10000 * v2 / d['denominador'])} por 10 mil)", transform=a.get_yaxis_transform(),
               va="center", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
    a.text(1.04, 1.02, "dicionário revisto", transform=a.transAxes, fontsize=MIN_PT + 0.5, color=INK, fontweight="bold", va="bottom")
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
    b.text(40.4, 1.5, f"contra 2 de 38, teste de Fisher:\n1 de 49 (principal): {P_IT_NEGRITO} = {apa(lit['p'], 2)}\n0 de 49 (sensibilidade): {P_IT_NEGRITO} = {apa(apl['p'], 2)}\nnenhum distinguível do acaso", ha="right", va="center",
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
            "figures/fontes/contagens.csv e r7_parlamento_sensibilidade.csv (origens em analysis/discourse/midia/ e escrutinio/simetria/).")
    salvar(fig, "fig11_circulacao_parlamento")



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
              ("PNS 2019, simulação\n(todos os não-LGB+ no denominador)", t["mc"]["B"], estat_vazado, None),
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
    # E5 (A2-02): sem a seta "para o Sinan igualar a PNS" -- as duas parcelas descrevem universos diferentes
    ax.text(1.03, 1.03, "estimativa [faixa]", transform=ax.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    VALORES["fig13"] = {"pontos": pts, "ic": ics, "lgb_pop": t["lgb_pop"]}
    moldura(fig, f"LGB+ são cerca de {br(t['direto'][0], 0)}% das vítimas de violência física na pesquisa de população e {br(t['sinan'][2023]['pct'], 0)}% nas fichas de saúde, ambos bem acima de {br(t['lgb_pop'], 2)}% da população",
            "Parcela de LGB+ entre adultos que sofreram violência física, vista por duas janelas: a pesquisa de domicílios (PNS) e as notificações dos serviços de saúde (Sinan)",
            "Cada linha é a parcela de LGB+ entre vítimas adultas de violência física num universo diferente: pessoas vitimadas, na pesquisa de domicílios, e notificações elegíveis, nas fichas de saúde. "
            "A linha tracejada mostra a parcela de LGB+ na população. As duas parcelas ficam acima dela e diferem em magnitude; uma não valida nem contradiz a outra; no Sinan, a barra fina mostra o intervalo possível "
            "quando um quarto das fichas não tem orientação registrada.",
            "PNS = pesquisa de domicílios do IBGE (amostra) · Sinan = sistema de notificação de violência dos serviços de saúde (quem procurou atendimento, não amostra) · "
            "orientação válida = ficha em que a orientação sexual foi preenchida · pior/melhor caso = se nenhuma ou todas as fichas sem resposta fossem de LGB+ · "
            "faixa da PNS = IC95% (o Sinan não tem IC: é contagem)",
            "figures/fontes/triangulacao_pns_sinan.md e c05_razao_direta.md (origens data/sinan/ e data/pns/).")
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
    a.text(0.03, 0.96, f"bolha = população\nSpearman das contagens: {apa(rho_c, 2)}", transform=a.transAxes, va="top", fontsize=MIN_PT, color=INK2)
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
            "figures/fontes/concordancia_v2.csv, serie_campo55_uf_ano.csv, anuario_lgbtfobia_uf_ano_v2.csv (edição 2026), sidra_9514.json (Censo 2022).")
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
    ax.set_xlabel("Ideologia do governador, comparada à média do próprio estado e do ano\n(pontos, de 0 = esquerda a 10 = direita)", fontsize=MIN_PT)
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
            "figures/fontes/painel_uf_ano_tse_brc.csv (origem data/painel/) e c02_indet_resultados.csv (faixa).")
    salvar(fig, "fig15_ideologia_taxa_residuos")


# ---------------------------------------------------------------- Figura 16: linha do tempo das fontes
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
        # o cálculo só procura aumento relativo, com 80% de poder (AST-06)
        ax.text(n / 1000 + 6, yy - 0.04, f"80% de poder para aumento de {br(100 * mde, 1)}% ou mais", va="top", fontsize=MIN_PT, color=INK2)
    ax.set_yticks(y, [r for r, *_ in linhas], fontsize=MIN_PT + 0.5)
    ax.set_xlim(0, 520)
    ax.tick_params(axis="x", labelsize=MIN_PT)
    ax.set_xlabel("Adultos entrevistados ou triados por rodada (milhares)", fontsize=MIN_PT + 0.5)
    # r35: sem grade vertical; cada barra traz o numero exato no rotulo e a linha de 400 cortava "31,7% ou mais" e "30,0% ou mais"
    falta = (int(need["adultos_a_triar"]) - int(cap["B'"]["adultos"]))
    ax.set_ylim(-1.55, 3.55)
    ax.annotate("", xy=(int(need["adultos_a_triar"]) / 1000, -0.72), xytext=(int(cap["B'"]["adultos"]) / 1000, -0.72),
                arrowprops={"arrowstyle": "<->", "color": INK2, "lw": 1.4})
    ax.text((int(need["adultos_a_triar"]) + int(cap["B'"]["adultos"])) / 2000, -0.9, f"faltam {miles(falta)} adultos\npara detectar aumento de 30%",
            ha="center", va="top", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
    VALORES["fig17"] = {"rotulos": [r for r, *_ in linhas], "adultos_mil": [float(p.get_width()) for p in bars], "mde": [m for *_, m, _ in linhas], "deff": deff}
    moldura(fig, f"Uma PNS como a de 2019 só detecta variações de {br(100 * linhas[0][2], 0)}% na violência contra LGB+; detectar 30% exige cerca de {miles(round(int(need['adultos_a_triar']), -3))} adultos",
            "Violência física em 12 meses: tamanho de amostra de cada desenho de pesquisa e a menor mudança entre rodadas que ele consegue ver",
            "Cada barra é quantos adultos seriam entrevistados; o texto diz a menor mudança na violência física entre duas rodadas que esse tamanho permitiria enxergar. "
            "Para ver uma variação de 30% seriam precisos cerca de 306 mil adultos triados, porque só uma pequena fração dos adultos é LGB+ e a amostra é sorteada por conglomerados, com pesos desiguais.",
            f"detectar = distinguir uma mudança real de variação por acaso (poder de 80%, erro de 5%) · efeito de desenho = {br(deff, 1)}: a amostra complexa vale {br(deff, 1)} vezes menos que uma amostra aleatória simples do mesmo tamanho · "
            "triar = visitar domicílios para achar adultos LGB+ · PNAD Contínua = pesquisa trimestral de domicílios do IBGE",
            "figures/fontes/capacidade_por_opcao.csv, cenarios_n_custo.csv, n_necessario.csv (origem analysis/survey-cost/).")
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
            "Como o motivo fica sem informação útil em 42% a 53% das fichas, conforme o ano, e o preenchimento muda de um ano para o outro, o número de casos registrados como LGBTfobia não mostra quanta violência acontece.",
            "Sinan = Sistema de Informação de Agravos de Notificação, dos serviços de saúde · notificação = ficha preenchida quando alguém atendido sofreu violência · "
            "“não se aplica” = a ficha marca que o campo não cabe ao caso · incidência = quantos casos acontecem de verdade",
            "figures/fontes/serie_campo55_uf_ano.csv (origem data/sinan/), linha Brasil.")
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
    a.set_title(f"(a) Homicídio: acompanha (ρ = {apa(ra['rho'], 2)})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    b.set_title(f"(b) Internet: some com o homicídio (ρ = {apa(rb['rho'], 2)})", loc="left", fontsize=9.5, fontweight="bold", color=INK)
    seta(a, f"razão da contagem por\ndesvio-padrão de homicídio:\n{f2(hom, 0)} ({ic(hom, 0)})\nsó com homicídio;\n{f2(both, 1)} ({ic(both, 1)})\ncom internet no modelo",
         (max(float(r["hom_taxa_100mil"]) for r in rs) - 3.9, 2.78), (6.5, 5.6), rad=-0.15, va="center", ha="left")
    # r35: a seta curva para cima (rad -0,15), longe do rotulo MT que ela raspava; na en a ultima linha da anotacao parte em
    # duas ("with internet" / "in the model") para nao passar por cima da bolha de RO
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
            "figures/fontes/uf_2019.csv e inflacao_uf_serie.json (origem analysis/ggb-audit/dados/; README do F3-ggb, linhas 16 e 137).")
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
    # r35: altura 6,3 -> 5,9 pol (mesma largura e corpo; os paineis encolhem na vertical): na en a Figura G5 nao cabia na
    # pagina em que e citada e deixava 94% dela em branco (en p. 149 do 1o export r35)
    fig = plt.figure(figsize=(7.2, 5.9))
    a = fig.add_axes([0.30, 0.60, 0.66, 0.35])
    b = fig.add_axes([0.30, 0.13, 0.44, 0.35])
    anos = sorted(ser["agressao"])
    la, = a.plot(anos, [ser["agressao"][x] for x in anos], "-o", color=PALETA["estat"], lw=2.4, ms=4.5, label="agressão (X85-Y09)")
    li, = a.plot(anos, [ser["agressao+indet"][x] for x in anos], "--", color=PALETA["ref"], lw=1.8, label="agressão + causa indeterminada")
    quem = {2016: "Temer\nassume", 2019: "Bolsonaro\nassume", 2023: "Lula\nassume"}   # em duas linhas: o rotulo nao cruza a linha da troca seguinte
    for t, nome in quem.items():
        a.axvline(t, color=INK2, lw=1, ls=":")
        a.text(t + 0.15, 42.2, f"{t}: {nome}", fontsize=MIN_PT, color=INK, va="top", ha="left")
    a.set_ylim(15, 42.6), a.set_xlim(2009.6, 2024.8)
    a.set_xticks(range(2010, 2025, 2))
    a.tick_params(labelsize=MIN_PT)
    a.set_ylabel("Mortes por agressão por 100 mil,\nigual padrão de idade", fontsize=MIN_PT + 0.3)
    # r35: sem grade horizontal e legenda numa linha so, embaixo do eixo do painel a: dentro do grafico as pontilhadas das trocas
    # cortavam o texto da legenda (embaixo a direita, 2019 e 2023; no alto a esquerda, 2016 em "causa indeterminada")
    a.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    seta(a, "a queda já começou em 2018,\nantes da troca de 2019", (2018, ser["agressao"][2018] - 0.4), (2010.2, 19.0), va="center", ha="left")
    a.set_title("(a) A taxa nacional cai a partir de 2018", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
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
        rotulos.append(f"{t}: troca" if tipo == "troca" else f"{d1[t]['placebo_quebra']}: quebra um ano antes")
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
    # r35: sem grade vertical (a de 20 e a de 40 cortavam a anotacao "quebra em 2018")
    b.legend(frameon=False, fontsize=MIN_PT, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    seta(b, f"quebra em 2018:\nqueda de {br(abs(d1[2019]['placebo_pct']))}%;\ndepende da data", (d1[2019]["placebo_pct_hi"] + 1.0, y[3]), (6, y[3]), va="center", ha="left")
    b.text(1.03, 1.03, "variação [IC95%]", transform=b.transAxes, fontsize=MIN_PT + 0.5, fontweight="bold", color=INK, va="bottom")
    # sensibilidade à data, com a série inteira, e não estimativa anterior à posse (AST-R2-01)
    b.set_title("(b) Cada troca x a mesma conta com a quebra um ano antes", loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.45)
    VALORES["fig20"] = {"anos": anos, "agressao": [float(v) for v in la.get_ydata()], "agressao_indet": [float(v) for v in li.get_ydata()],
                        "quebras": [t for t, *_ in linhas], "tipos": [x[1] for x in linhas], "pontos": pts, "ic": ics,
                        "mde": [[float(m[0]), float(m[1])] for m in mn]}
    ai = {r["quebra"]: float(r["pct"]) for r in ler_csv("c09_d1_resultados.csv") if r["serie"] == "Brasil" and r["desfecho"] == "agressao+indet"}
    moldura(fig, f"A queda de {br(abs(d1[2019]['pct']), 0)}% na taxa nacional em 2019 também aparece com a quebra deslocada para 2018 ({br(d1[2019]['placebo_pct'])}%), e a taxa já caía de 2017 para 2018: os dados não a atribuem ao presidente",
            "Taxa nacional de morte por agressão, 2010-2024, e a variação de nível em cada troca de presidente (2016, 2019, 2023), comparada à mesma conta com as quebras um ano antes",
            "Em (a), a linha roxa é a taxa por 100 mil; as linhas pontilhadas marcam as trocas. Em (b), cada quadrado roxo é a mudança de nível estimada depois da troca e o círculo vazado é a mesma conta "
            "com as quebras deslocadas um ano para trás e a série inteira: queda parecida mostra que a estimativa depende da data. Os traços pretos mostram o menor efeito que a análise conseguiria ver; "
            "a queda de 2019 é distinguível de zero, mas a conta com a quebra em 2018 também cai, e a taxa já caía de 2017 para 2018, por isso a queda não é atribuível à troca; 2016 e 2023 não se distinguem de zero, com poder baixo.",
            f"nível = salto da taxa no ano da troca · quebra um ano antes = a mesma conta com as datas deslocadas, ajustada à série inteira · IC95% = faixa de incerteza · efeito mínimo detectável = menor efeito que a análise veria com 80% de chance · "
            f"só 15 pontos (2010-2024) e a análise é descritiva, não causal · somando as mortes de causa indeterminada, a queda de 2019 é {br(ai['2019'])}% · o óbito não registra orientação sexual: nada aqui é sobre violência contra LGBT+",
            "figures/fontes/c09_d1_resultados.csv e asr_brasil.csv (origens data/presidencia/ e data/sim/); RELATORIO-C09.md; pré-registro PREREGISTRO-C09.")
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
    seta(ax, "além dos traços pretos,\npoder de 80% ou mais", (float(por[("S7_copartidarismo", "total")]["mde_pos"]), ys[5] - 0.3), (26, ys[5] - 1.05), va="center", ha="left")
    todas = ler_d2()
    VALORES["fig21"] = {"linhas": [f"{a}|{g}" for a, g in ordem], "pontos": pts, "ic": ics, "mde": mdes, "n_estimativas": len(todas),
                        "n_distinguiveis": sum(r["distinguivel"] != "False" for r in todas)}
    moldura(fig, f"Nenhuma das {len(todas)} estimativas da interação entre a ideologia do governador e a do presidente se distingue de zero, e o painel só teria 80% de poder para efeitos de cerca de {br(abs(float(prim['mde_neg'])), 0)}% para menos ou {br(float(prim['mde_pos']), 0)}% para mais",
            "Interação entre os escores de ideologia do governador e do presidente (principal) e variações, na taxa de homicídio; 351 combinações de estado e ano (2012-2024); 16 análises em %",
            f"Cada quadrado é a melhor estimativa e a barra é a faixa compatível com os dados; todas as barras passam por zero, então o painel não consegue dizer se a interação mudou a taxa. "
            f"Os traços pretos mostram o menor efeito que a análise detectaria com 80% de chance ({br(float(prim['mde_neg']))}% e +{br(float(prim['mde_pos']))}% na principal): efeitos menores têm chance de detecção abaixo de 80%; a barra, e não o traço, mostra os valores compatíveis com os dados. "
            "O resultado é “não distinguível de zero, com poder baixo”; não é prova de que o presidente não importa.",
            "interação = produto do escore de ideologia do governador (0 a 10) pelo do presidente: mede se o efeito de um depende do outro; “distância entre governador e presidente” e “mesmo partido” são variações separadas · o efeito do presidente em si não é identificável: o efeito de ano o absorve, só a interação aparece · "
            "IC95% = faixa de incerteza (erro-padrão agrupado por estado) · efeito mínimo detectável = menor efeito que a análise veria com 80% de chance · 27 estados e 3 trocas de presidente · "
            "a razão de óbitos indeterminados (teste de falsificação, em pontos percentuais, 5 estimativas) está na tabela do relatório, não nesta figura · o óbito não registra orientação sexual",
            "figures/fontes/c09_d2_resultados.csv e RELATORIO-C09.md (origem data/presidencia/); pré-registro PREREGISTRO-C09 gravado antes dos desfechos.")
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
    F22 = 9.5  # E5: menor corpo desta figura (cerca de 7,2 pol impressas a 14 cm -> 7,2 pt)
    fig = plt.figure(figsize=(7.0, 7.2))
    a = fig.add_axes([0.13, 0.70, 0.84, 0.27])
    b = fig.add_axes([0.38, 0.075, 0.30, 0.495])   # r35: 0,525 -> 0,495, abre lugar para o titulo subir acima do cabecalho
    anos = sorted(ser["agressao"])
    # faixas por governo (limites a partir da fracao de cada ano; 2016 dividido Dilma/Temer)
    lim = {"Dilma": (2010.5, 2015.5 + 0.361), "Temer": (2015.5 + 0.361, 2018.5), "Bolsonaro": (2018.5, 2022.5), "Lula": (2022.5, 2024.5)}
    assert "Dilma Rousseff 0.361" in gov_ano[2016]   # a fracao 0,361 de 2016 vem do arquivo
    for k, (nome, (x0, x1)) in enumerate(lim.items()):
        a.axvspan(x0, x1, color=PALETA["card"] if k % 2 == 0 else "none", zorder=0)
        a.text((x0 + x1) / 2, 41.2, nome, ha="center", va="top", fontsize=F22, fontweight="bold", color=INK)
    la, = a.plot(anos, [ser["agressao"][x] for x in anos], "-o", color=PALETA["estat"], lw=2.4, ms=4.5, label="agressão (X85-Y09)")
    li, = a.plot(anos, [ser["agressao+indet"][x] for x in anos], "--", color=PALETA["ref"], lw=1.8, label="agressão + causa indeterminada")
    a.set_ylim(15, 42), a.set_xlim(2009.6, 2024.6)
    a.set_xticks(range(2010, 2025, 2))
    a.tick_params(labelsize=F22)
    a.set_ylabel("Mortes por 100 mil,\npadronizada por idade", fontsize=F22)
    # r35: sem grade horizontal (a de 20 cortava a legenda e "a queda começou em 2018"); as faixas de governo ficam
    # he (2026-11-24): a legenda RTL poe o traco a DIREITA do texto (bidi_he regra 1), e no canto de baixo ele caia sobre o
    # fim da linha roxa em 2024; no he a legenda sobe para o canto de cima, livre (y 33-38; a tracejada fica abaixo de 31)
    a.legend(frameon=False, fontsize=F22, **({"loc": "upper right", "bbox_to_anchor": (1, 0.87)} if LANG == "he" else {"loc": "lower right"}))
    a.annotate("a queda começou\nem 2018", xy=(2018, ser["agressao"][2018] - 0.5), xytext=(2010.6, 19.2), fontsize=F22, color=INK, fontweight="bold",
               va="center", ha="left", arrowprops={"arrowstyle": "->", "color": INK2, "lw": 1.3, "shrinkA": 2, "shrinkB": 3, "connectionstyle": "arc3,rad=0.15"})
    a.set_title("(a) A taxa nacional por governo", loc="left", fontsize=F22 + 1, fontweight="bold", color=INK, x=-0.1)
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
            b.text(-1.22, y0, f"{nome}: {a0} → {a1}", transform=b.get_yaxis_transform(), fontsize=F22 + 0.5, fontweight="bold", color=INK, ha="left", va="center")
            continue
        r = por.get((g, kind)) if kind != "pre" else por[(g, "agressao")]
        if kind == "pre":
            if r["pre_var_pct"] == "":
                b.text(1.03, y0, "n/d (série desde 2010)", transform=b.get_yaxis_transform(), va="center", fontsize=F22, color=INK2)
                continue
            v = float(r["pre_var_pct"])
            m = b.plot([v], [y0], "D", mfc="white", mec=PALETA["ref"], mew=1.6, ms=6.5)[0]
            pts.append(float(m.get_xdata()[0])), ics.append(None), tip.append("pre"), gvs.append(g)
            b.text(1.03, y0, f"{br(v)}%  ({r['pre_de']} → {int(r['ano_base'])})", transform=b.get_yaxis_transform(), va="center", fontsize=F22, color=INK2)
            continue
        v, lo, hi = float(r["var_pct"]), float(r["var_pct_lo"]), float(r["var_pct_hi"])
        if kind == "agressao":
            eb = b.errorbar([v], [y0], xerr=[[v - lo], [hi - v]], fmt="s", ms=7, color=PALETA["estat"], ecolor=PALETA["estat"], elinewidth=2.2, capsize=3)
        else:
            eb = b.errorbar([v], [y0], xerr=[[v - lo], [hi - v]], fmt="o", ms=6.5, mfc="white", mec=PALETA["ref"], mew=1.6, color=PALETA["ref"], ecolor=PALETA["ref"], elinewidth=1.6, capsize=3)
        pts.append(float(eb.lines[0].get_xdata()[0])), ics.append(erros_de(eb)[0]), tip.append(kind), gvs.append(g)
        b.text(1.03, y0, f"{br(v)}%  [{br(lo)}; {br(hi)}]", transform=b.get_yaxis_transform(), va="center", fontsize=F22, color=INK,
               fontweight="bold" if kind == "agressao" else "normal")
    rot = {"agressao": "agressão", "agressao+indet": "+ indeterminada", "pre": "3 anos antes da posse"}
    b.set_yticks([y0 for k, g, y0 in linhas if k != "cab"], [rot[k] for k, g, y0 in linhas if k != "cab"], fontsize=F22)
    b.axvline(0, color=INK2, lw=0.9, ls="--")
    b.set_xlim(-30, 22), b.set_ylim(yy + 0.3, 0.2)
    b.tick_params(axis="x", labelsize=F22)
    b.set_xlabel("Variação da taxa do ano-base\nao último ano do governo, %", fontsize=F22)
    b.grid(axis="x", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.text(1.03, 1.0, "variação\n[intervalo de contagem]", transform=b.transAxes, fontsize=F22, fontweight="bold", color=INK, va="bottom")
    b.set_title("(b) Quanto a taxa variou em cada governo", loc="left", fontsize=F22 + 1, fontweight="bold", color=INK, x=-1.22, pad=30)
    bol, bol_i = por[("Jair Bolsonaro", "agressao")], por[("Jair Bolsonaro", "agressao+indet")]
    VALORES["fig22"] = {"anos": anos, "agressao": [float(v) for v in la.get_ydata()], "agressao_indet": [float(v) for v in li.get_ydata()],
                        "governos": gvs, "tipos": tip, "pontos": pts, "ic": ics, "limites": {k: [float(v[0]), float(v[1])] for k, v in lim.items()}}
    moldura(fig, f"A taxa nacional caiu {br(abs(float(bol['var_pct'])))}% entre {bol['ano_base']} e {bol['ano_fim']} ({br(abs(float(bol_i['var_pct'])))}% somando causa indeterminada); a queda começou em 2018; isto não é prova de causa",
            "Taxa nacional de morte por agressão, padronizada por idade, por governo (2010-2024), e variação do ano anterior à posse ao último ano inteiro de cada governo",
            "Em (a), cada faixa cinza ou branca é um governo e a linha roxa é a taxa por 100 mil. Em (b), cada quadrado roxo é quanto a taxa variou do ano anterior à posse ao último ano inteiro do governo; "
            "o círculo vazado faz a mesma conta somando as mortes de causa indeterminada; o losango mostra o que a taxa vinha fazendo nos 3 anos antes da posse, só como contexto. "
            "Isto é exposição: mostra o que aconteceu enquanto cada governo estava no cargo, não que o governo causou a mudança.",
            "taxa padronizada por idade = taxa recalculada como se a população tivesse sempre a mesma distribuição de idades · causa indeterminada = óbito cuja causa não foi definida (CID-10 Y10-Y34); "
            "sua fração sobe de 14% (2015) para 30% (2024), então a queda somando-as é sempre menor · intervalo de contagem = só a incerteza do número de mortes, não mede tendência nem causa · "
            "2016 é dividido entre Dilma (até 11/05) e Temer · Lula está em curso (2 de 4 anos; denominadores de 2023-24 estimados) · o governo Lula de 2007-10 não aparece: a série usada começa em 2010, ano do Censo que ancora os denominadores · o óbito não registra orientação sexual",
            "figures/fontes/c10_e1_federal.csv e c10_e1_serie_longo.csv, RELATORIO-EXPOSICAO.md (origem data/exposicao/); pré-registro PREREGISTRO-C10 gravado antes dos desfechos.")
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
        b.text(1.03, yy, f"{r['n_subiu']} subiram, {r['n_caiu']} caíram\nmediana {br(float(r['mediana_pct']))}%  ({P_IT} = {apa(float(r['p_mediana']), 3)})", transform=b.get_yaxis_transform(), va="center", fontsize=MIN_PT + 0.3, color=INK)
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
            "figures/fontes/c10_e2_trocas_longo.csv e c10_e2_resumo.csv, RELATORIO-EXPOSICAO.md (origem data/exposicao/); pré-registro PREREGISTRO-C10.")
    salvar(fig, "fig23_trocas_de_governador_exposicao")


def ler_estudos() -> dict:
    """Numeros de estudos de mortalidade de sources/public/estudos_mortalidade.tsv (id -> linha)."""
    return {r["id"]: r for r in ler_tsv("estudos_mortalidade.tsv")}


def _quebra_barra(txt: str, n: int) -> str:
    """Quebra em linhas de ate n caracteres, podendo quebrar depois de '/' (sem partir palavra: 'LGB+/heterossexuais')."""
    return "\n".join(ln.replace("/ ", "/") for ln in textwrap.wrap(txt.replace("/", "/ "), n, break_long_words=False))


def figura25() -> None:
    """Mapa da evidencia internacional de mortalidade: uma linha por estudo, cada painel com a sua propria medida."""
    E = ler_estudos()
    fl = lambda k, f="valor": float(E[k][f])   # noqa: E731
    W, H = 8.3, 7.85   # razao altura/largura <= 1 para caber a 14 cm com rotulo, titulo e Nota na mesma pagina
    fig = plt.figure(figsize=(W, H))
    tx = fig.add_axes([0, 0, 1, 1]); tx.set_xlim(0, W), tx.set_ylim(H, 0), tx.axis("off")
    xc = [0.05, 1.3, 2.8]
    for x, t in zip(xc, ("Estudo", "População e país", "Causa e medida")):
        tx.text(x, 0.08, t, ha="left", va="center", fontsize=MIN_PT + 0.5, fontweight="bold", color=INK)
    tx.text(4.9, 0.08, "Resultado (escala própria em cada linha)", ha="left", va="center", fontsize=MIN_PT + 0.5, fontweight="bold", color=INK)
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
    top, rh = 0.5, 1.0
    VALORES["fig25"] = {"paineis": {}}
    fs = MIN_PT
    for i, (nome, tags, pop, causa) in enumerate(linhas):
        y = top + i * rh
        # fundo branco (regra do autor: nada de faixa cinza); filete fino separa as linhas sob as colunas de texto
        if i:
            tx.plot([0.02, 0.55 * W], [y - 0.03, y - 0.03], color="#B0B0B0", lw=0.5, zorder=0)  # só sob as colunas de texto: o rótulo do eixo de cada painel fica abaixo da fronteira
        tx.text(xc[0], y + 0.12, nome, ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=INK)
        for j, tg in enumerate(tags):
            tx.text(xc[0], y + 0.36 + 0.4 * j, "\n".join(textwrap.wrap(tg, 9)), ha="left", va="center", fontsize=MIN_PT, fontweight="bold", color=PALETA["estat"] if tg == "É BRASIL" else PALETA["nao"])
        tx.text(xc[1], y + 0.08, _quebra_barra(pop, 21), ha="left", va="top", fontsize=MIN_PT, color=INK)
        tx.text(xc[2], y + 0.08, _quebra_barra(causa, 21), ha="left", va="top", fontsize=MIN_PT, color=INK2)
        ax = fig.add_axes([6.55 / W, 1 - (y + rh - 0.3) / H, 1.6 / W, 0.5 / H])
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
    moldura(fig, "Fora do Brasil, a mortalidade geral de pessoas LGB+ e trans aparece maior em populações bem definidas; nenhuma fonte lida dá razão de homicídio por orientação sexual, e o estudo brasileiro não tem denominador",
            "Evidência brasileira e internacional de mortalidade e violência publicada entre 2023 e 2026: o que cada estudo mede, em quem e em que país",
            "Cada linha é um estudo e cada painel tem a sua própria escala: as medidas são diferentes (razão de taxas, taxa por 100 mil, fator de aceleração, contagem de estudos) e por isso não se comparam entre si, nem formam um único “risco”. "
            "Os rótulos em vinho avisam o que o estudo NÃO é: não é Brasil, não é homicídio. Só o estudo de Luis (2026) é brasileiro e não traz taxa, por falta de denominador.",
            "razão de taxas = quantas vezes a mortalidade de um grupo é maior que a do outro, depois de igualar as idades · LGB+ = lésbicas, gays, bissexuais e outras orientações · fator de aceleração = menor que 1 quer dizer que o tempo até o óbito é mais curto · "
            "causas violentas = homicídio, suicídio e intenção indeterminada, juntos · Sinan = ficha de notificação de violência de serviço de saúde · SIM = base de atestados de óbito · "
            "estudos descritivos: nenhum deles permite dizer que a orientação sexual causa a diferença",
            "figures/fontes/estudos_mortalidade.tsv, com números literais de L-SECAO-3-3-PROPOSTA.md (frente L, tabela “De onde vem cada número”).")
    salvar(fig, "fig25_mortalidade_internacional")


def figura26() -> None:
    """Fluxo de verificabilidade da lista do GGB de 2019: 160 sorteados -> recuperados -> correspondentes -> morte violenta -> critérios; motivo entre as mortes violentas."""
    js = json.loads((FONTES / "ggb_validacao_resumo.json").read_text(encoding="utf-8"))
    n0, n1, n2, n3, n4 = js["n_amostra"], js["recuperadas"], js["correspondem"], js["morte_violenta"], js["verificavel_estrito"]
    mot = js["motivo_entre_morte_violenta_confirmada"]
    nr = js["motivo_nao_recuperacao"]
    # r35: altura 7,2 -> 6,25 pol, so tirando o vao vazio entre os paineis (mesma largura, mesmo corpo de letra), para a
    # Figura 7 caber na pagina em que e citada (export r34: pt p. 36 e en p. 37 com mais de 2/3 em branco antes dela)
    H26 = 6.25
    fig = plt.figure(figsize=(7.2, H26))
    a = fig.add_axes([0.02, 2.85 / H26, 0.96, 3.0 / H26])
    b = fig.add_axes([0.40, 0.65 / H26, 0.2, 1.94 / H26])
    etapas = [(n0, "casos sorteados da lista de 2019"), (n1, "com a matéria recuperada"), (n2, "em que a matéria é do caso"), (n3, "com morte violenta confirmada"), (n4, "e a fonte diz expressamente que a vítima é LGBT+")]
    saidas = [f"{n0 - n1} sem matéria recuperada: {nr['link_morto_404']} link morto, {nr['dominio_inacessivel']} site inacessível, {nr['bloqueio_ou_erro_servidor']} bloqueio ou erro, {nr['sem_link_no_anexo4']} sem link: não dá para verificar",
              f"{n1 - n2} em que a matéria não é a do caso",
              f"{n2 - n3} sem morte violenta confirmada (indeterminada ou não violenta)",
              f"{n3 - n4} com morte violenta, mas sem a identificação expressa como LGBT+ na fonte", ""]
    y = list(range(5))[::-1]
    bars = a.barh(y, [e[0] for e in etapas], height=0.62, left=[-e[0] / 2 for e in etapas], color=[PALETA["estat"] if i in (0, 4) else PALETA["estat_cl"] for i in range(5)])
    for (n, rot), yy in zip(etapas, y):
        a.text(0, yy, f"{n}", ha="center", va="center", fontsize=11, fontweight="bold", color="white" if n in (n0, n4) else INK)
        a.text(-149, yy, "\n".join(textwrap.wrap(rot, 20)), ha="left", va="center", fontsize=MIN_PT, color=INK, clip_on=False, transform=a.transData)
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
    # r35: sem grade vertical (a de 40 cortava "36  (48,6%)" e encostava nos rotulos "(17,6%)")
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
            "figures/fontes/ggb_validacao_resumo.json (origem analysis/ggb-audit/dados/validacao_resumo.json); conferido contra codificacao_A.csv no teste.")
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
        ax.set_xticks([0.1, 0.25, 0.5, 1, 2.82, 3.84], [br(0.1), br(0.25, 2), br(0.5), "1", br(2.82, 2), br(3.84, 2)], fontsize=MIN_PT)
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
            "figures/fontes/c08_numeradores.csv (origem data/ggb/c08_numeradores.csv), agressão, prevalência de 1,89%, sem proxy.")
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
            "figures/fontes/d100_serie_anual.csv (origem data/disque100/saidas/d100_serie_anual.csv; microdados oficiais do Disque 100 em dadosabertos.mdh.gov.br, catálogo com sha256 em data/disque100/saidas/catalogo.tsv).")
    salvar(fig, "fig28_disque100_serie")


# ---------------------------------------------------------------- idioma: T(), conferencia e tabela pt -> en
_FIG_ATUAL = ""
_NOMES: list = []        # figuras gravadas nesta execucao
_FALTAM: dict = {}          # chave pt -> figura (so em en)
_CHAVES: dict = {}          # chave pt -> exemplo com as quebras originais (so para --chaves)
_SAIDAS: set = set()        # textos ja traduzidos: set_text repetido sobre o proprio resultado e idempotente
_NUM_LIT = re.compile(r"(?<![\w.,])\d+(?:\.\d{3})*(?:,\d+)?(?!\w)")   # numero literal em formato pt (nao casa N1, Y09, X85)
_PARAM = re.compile(f"{S0}(.*?){S1}")


def limpa(t: str) -> str:
    """Tira os marcadores invisiveis de br()/miles()."""
    return t.replace(S0, "").replace(S1, "") if isinstance(t, str) else t


def _gabarito(texto: str) -> tuple[str, list[str]]:
    """Texto pt com numeros -> (modelo com `{}` e espacos normalizados, parametros ja no idioma da execucao)."""
    partes = _PARAM.split(texto)           # indices pares = texto literal; impares = numero de br()/miles()
    modelo, params = [], []
    for k, parte in enumerate(partes):
        if k % 2:
            modelo.append("{}"), params.append(parte)
        else:
            def troca(m):
                params.append(m.group(0) if _virgula() else num_pt_en(m.group(0)))
                return "{}"
            modelo.append(_NUM_LIT.sub(troca, parte))
    return " ".join("".join(modelo).split()), params


def T(texto_pt: str) -> str:
    """Texto desenhado na imagem, no idioma da execucao. pt-BR: devolve o proprio texto. en: procura o texto pt (numeros
    -> `{}`, espacos/quebras normalizados) na tabela EN e preenche os numeros; sem entrada, registra a falta (a execucao
    termina em SystemExit)."""
    if not texto_pt or texto_pt in _SAIDAS:
        return texto_pt
    if texto_pt.startswith("$") and texto_pt.endswith("$"):          # rotulo matematico do matplotlib (10^1)
        return texto_pt
    modelo, params = _gabarito(texto_pt)
    if not any(c.isalpha() for c in modelo.replace("{}", "")):         # so numero e simbolo: nada a traduzir
        return limpa(texto_pt)
    if LANG == "pt-BR":
        _CHAVES.setdefault(modelo, limpa(texto_pt))
        return limpa(texto_pt)
    alvo = TAB.get(modelo)
    if alvo is None:
        _FALTAM.setdefault(modelo, _FIG_ATUAL)
        return limpa(texto_pt)
    pedacos = alvo.split("{}")
    if len(pedacos) - 1 != len(params):
        raise SystemExit(f"[ERRO] T(): a entrada EN de {modelo!r} tem {len(pedacos) - 1} lacunas e o texto tem {len(params)} numeros")
    saida = pedacos[0] + "".join(p_ + q for p_, q in zip(params, pedacos[1:]))
    _SAIDAS.add(saida)
    return saida


_set_text_original = Text.set_text


def _set_text_traduzido(self, s):
    _set_text_original(self, T("" if s is None else str(s)))


# palavras portuguesas obvias que nao podem aparecer num texto em ingles (conferencia de seguranca, nao dicionario)
_PT_PALAVRAS = {"de", "do", "da", "dos", "das", "para", "com", "sem", "em", "na", "nos", "nas", "um", "uma", "que", "por", "pelo", "pela",
                "ao", "ou", "mais", "menos", "entre", "ano", "anos", "vezes", "são", "não", "mortes", "taxa", "sobre", "como", "foi",
                "ser", "pessoas", "estados", "estado", "queda", "alta", "risco", "só", "já", "também", "esperadas", "faixa"}
_ACENTO = re.compile("[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]")


NOMES_PROPRIOS = ("Contínua",)   # nome oficial (PNAD Contínua): o acento e legitimo


def _suspeitas(texto: str) -> list[str]:
    """Acentos portugueses e palavras portuguesas obvias num texto que deveria estar em ingles."""
    for n in NOMES_PROPRIOS:
        texto = texto.replace(n, "")
    achados = _ACENTO.findall(texto)
    for w in re.findall(r"[^\W\d_]+", texto):
        if w in _PT_PALAVRAS or (w.lower() in _PT_PALAVRAS and w[0].isupper() and len(w) >= 3 and w.upper() != w):
            achados.append(w)
    return achados


def conferir_textos(fig, nome: str) -> None:
    """Em en: todo texto desenhado (ax.texts, anotacoes, ticks, legendas, rotulos, titulos) sem acento nem palavra pt.
    es/it/he: a conferencia e a da tabela (conferencia da tabela de rotulos), e T() ja reprova chave ausente."""
    if LANG != "en":
        return
    ruins = []
    for t in fig.findobj(Text):
        txt = t.get_text()
        if txt and (a := _suspeitas(txt)):
            ruins.append((txt, a))
    if ruins:
        raise SystemExit(f"[ERRO] {nome}: texto em portugues na versao en: " + "; ".join(f"{t!r} -> {a}" for t, a in ruins))


def conferir_pdf(nome: str) -> None:
    """Em en: o texto extraido do PDF final tambem nao pode ter portugues (o SVG leva texto em contorno, sem texto a extrair)."""
    if LANG != "en" or not shutil.which("pdftotext"):
        return
    txt = subprocess.run(["pdftotext", "-q", str(SAIDA / LANG / f"{nome}.pdf"), "-"], capture_output=True, text=True, check=True).stdout
    if a := _suspeitas(txt):
        raise SystemExit(f"[ERRO] {nome}.pdf (en): portugues no texto extraido: {sorted(set(a))}")


def _w(t: str, n: int) -> str:
    """Quebra o texto em ingles na mesma largura que o original em portugues usava."""
    return "\n".join(textwrap.wrap(t, n))


# chave = texto pt (numeros -> {}, espacos e quebras normalizados); valor = texto en com as quebras desenhadas.
# Siglas e nomes proprios entram com valor igual (SP, ONS, McKetta...): a presenca na tabela prova que foram vistos.
EN = {
    # ---- Fig 1
    "Física": "Physical", "Sexual": "Sexual", "Qualquer tipo": "Any type",
    "Adultos que sofreram violência em {} meses (%)": "Adults who experienced violence in the past {} months (%)",
    "LGB+": "LGB+", "Heterossexuais": "Heterosexuals",
    "(a) Quantos sofreram": "(a) How many experienced it",
    "{} vezes mais": "{} times higher",
    "{} = igual": "{} = equal",
    "Quantas vezes mais entre LGB+ (escala log)": "Prevalence ratio, LGB+ (log scale)",
    "razão bruta": "crude ratio", "razão ajustada": "adjusted ratio",
    "(b) A razão entre os dois grupos": "(b) Ratio between the two groups",
    # ---- Fig 2
    "{} · total declarado {} declaradas; esperadas: {}": "{} · total reported\n{} reported; expected: {}",
    "{} · numerador A: homicídios e latrocínios {} declaradas; esperadas: {}": "{} · numerator A: homicides\nand robbery-murders\n{} reported; expected: {}",
    "{} · numerador B: cenário de subtração (sem pessoas trans) {} declaradas; esperadas: {}": "{} · numerator B: subtraction\nscenario (excluding trans people)\n{} reported; expected: {}",
    "Mortes declaradas ÷ mortes esperadas (%)": "Reported deaths ÷ expected deaths (%)",
    "risco igual ao dos pares": "same risk as peers",
    "risco {} vezes maior": "{} times higher risk",
    "Se adultos LGB+ tivessem este risco de morte por agressão…": "If LGB+ adults had this risk of death by assault…",
    "{} contadas de {} esperadas = {}%": "{} counted of {} expected\n= {}%",
    "{}% a +{}%": "{}% to +{}%",
    # ---- Fig 3
    "Total": "Total", "Homens": "Men", "Mulheres": "Women", "Negros": "Black", "Não negros": "Non-Black", "Arma de fogo": "Firearm",
    "Variação da taxa ao trocar o governador do PT por DEM ou PL ({} pontos de ideologia), %":
        "Change in the rate when replacing a PT governor\nwith DEM or PL ({} ideology points), %",
    "mortes por agressão registradas": "recorded deaths by assault",
    "agressão + causa indeterminada": "assault + undetermined cause",
    "(a) Painel por estado e ano": "(a) State-year panel",
    "a faixa inclui zero: não se distingue de zero": "the interval includes zero:\nnot distinguishable from zero",
    "deslocamento para a direita janela completa, {} trocas mudança anterior não detectada ($p$ = {})":
        "shift to the right\nfull window, {} changes\nno prior change detected ($p$ = {})",
    "deslocamento para a esquerda janela completa, {} trocas já mudava antes ($p$ = {})":
        "shift to the left\nfull window, {} changes\nalready changing beforehand ($p$ = {})",
    "deslocamento para a direita janela curta, {} trocas já mudava antes ($p$ = {})":
        "shift to the right\nshort window, {} changes\nalready changing beforehand ($p$ = {})",
    "deslocamento para a esquerda janela curta, {} trocas mudança anterior não detectada ($p$ = {})":
        "shift to the left\nshort window, {} changes\nno prior change detected ($p$ = {})",
    "Variação média da taxa depois da troca, comparada a estados sem troca (%)":
        "Mean change in the rate after the change,\ncompared with states without a change (%)",
    "(b) Deslocamento do escore: a mesma queda nos dois sentidos": "(b) Score shift: the same drop in both directions",
    # ---- Fig 6
    "cerca de {} em {}": "about {} in {}",
    "cada quadrado = {} em {} adultos": "each square = {} in {} adults",
    "{} vezes": "{} times",
    "razão direta (bruta) IC95% {} a {}": "direct (crude) ratio\n95% CI {} to {}",
    "razão ajustada IC95% {} a {}": "adjusted ratio\n95% CI {} to {}",
    "{} = risco igual": "{} = equal risk",
    "Quantas vezes mais entre LGB+": "Prevalence ratio, LGB+",
    "Quantas vezes mais": "Prevalence ratio",
    # ---- Fig 8
    "vezes a taxa de mulheres não negras": "times the rate of\nnon-Black women",
    "Homens negros": "Black men", "Homens não negros": "Non-Black men", "Mulheres negras": "Black women", "Mulheres não negras": "Non-Black women",
    "Mortes por agressão por {} mil pessoas do grupo, já descontada a idade (média {}-{})":
        "Deaths by assault per {},000 people in the group, age-adjusted (mean {}-{})",
    "a taxa de todos os grupos é medida contra esta barra (×{})": "every group's rate is measured\nagainst this bar (×{})",
    # ---- Fig 9
    "queda > {}% · alta > {}%": "drop > {}% · rise > {}%",
    "Efeitos que o painel exclui": "Effects the panel rules out",
    "Variação da taxa de homicídio ao trocar PT por DEM ou PL ({} pontos de ideologia), %":
        "Change in the homicide rate when replacing PT with DEM or PL ({} ideology points), %",
    "excluído pelos dados": "ruled out by the data",
    "compatível com os dados": "compatible with the data",
    "melhor estimativa": "best estimate",
    "faixa compatível com os dados": "range compatible\nwith the data",
    # ---- Fig 10
    "constante": "constant",
    "+{}%/ano": "+{}%/yr",
    "+{}% ao ano": "+{}% per year",
    "−{}% ao ano": "−{}% per year",
    "BOs por ano": "Police reports per year",
    "incidência constante e registro +{}% ao ano": "constant incidence and reporting +{}% per year",
    "incidência +{}% ao ano e registro +{}% ao ano": "incidence +{}% per year and reporting +{}% per year",
    "incidência −{}% ao ano e registro +{}% ao ano": "incidence −{}% per year and reporting +{}% per year",
    "registrado de fato (Anuário FBSP)": "actually recorded (FBSP Yearbook)",
    "(a) A série registrada: as três linhas coincidem de propósito": "(a) The recorded series: the three lines coincide by design",
    "as três linhas têm o mesmo erro (soma de quadrados em log = {})": "the three lines have the same error\n(sum of squares in log = {})",
    "ocorrências reais, em milhares": "actual incidents, in thousands",
    "% das ocorrências que viram BO": "% reported to police",
    "(b) O que realmente aconteceu (invisível)": "(b) What really happened (unobserved)",
    "(c) A chance de virar BO (invisível)": "(c) Reporting chance (unobserved)",
    # ---- Fig 11
    "{} falas ({} por {} mil)": "{} speeches ({} per {},000)",
    "dicionário revisto": "revised dictionary",
    "F1 “gays/LGBT morrem mais”": "F1 “gay/LGBT people die more”",
    "F2 “o país que mais mata”": "F2 “the country that kills the most”",
    "F3 “governo mata ou persegue”": "F3 “government kills or persecutes”",
    "F4 “não existe / dado inventado”": "F4 “does not exist / made-up data”",
    "Falas encontradas na Câmara e no Senado": "Speeches found in the Chamber and the Senate",
    "dicionário pré-registrado (casa palavras demais)": "pre-registered dictionary (matches too many words)",
    "dicionário revisto (contagem usada)": "revised dictionary (count used)",
    "(a) Quatro frases em {} falas ({} a {})": "(a) Four phrases in {} speeches ({} to {})",
    "{} de {} ({}%)": "{} of {} ({}%)",
    "“O país que mais mata”: regra literal do livro de códigos (principal)": "“The country that kills the most”: literal\ncodebook rule (main)",
    "mesmas falas, regra aplicada pelo codificador original (sensibilidade)": "same speeches, rule as applied by the\noriginal coder (sensitivity)",
    "mesmas falas, 2º codificador (outra família de modelo)": "same speeches, 2nd coder\n(different model family)",
    "linha de base: outras estatísticas de plenário na Câmara": "baseline: other floor statistics\nin the Chamber",
    "Falas que citam fonte primária, % (barra = faixa de incerteza)": "Speeches citing a primary source, % (bar = uncertainty interval)",
    "contra {} de {}, teste de Fisher: {} de {} (principal): $\\mathbfit{p}$ = {} {} de {} (sensibilidade): $\\mathbfit{p}$ = {} nenhum distinguível do acaso":
        "vs. {} of {}, Fisher test:\n{} of {} (main): $\\mathbfit{p}$ = {}\n{} of {} (sensitivity): $\\mathbfit{p}$ = {}\nnone distinguishable from chance",
    "(b) A taxa de fonte primária é baixa, e a linha de base também": "(b) The primary-source rate is low, and so is the baseline",
    # ---- Fig 13
    "{}% [{} a {}]": "{}% [{} to {}]",
    "{}% (pior caso {}, melhor {})": "{}% (worst case {}, best {})",
    "LGB+ na população adulta: {}%": "LGB+ in the adult population: {}%",
    "PNS {}, direto no microdado (quem respondeu hetero ou LGB+)": "PNS {}, direct from microdata\n(respondents who said heterosexual or LGB+)",
    "PNS {}, simulação (só quem respondeu a orientação)": "PNS {}, simulation\n(only respondents who reported orientation)",
    "PNS {}, simulação (todos os não-LGB+ no denominador)": "PNS {}, simulation\n(all non-LGB+ in the denominator)",
    "Sinan {} (fichas com orientação válida)": "Sinan {}\n(records with valid orientation)",
    "LGB+ entre as vítimas adultas de violência física (%)": "LGB+ share of adult victims of physical violence (%)",
    "estimativa [faixa]": "estimate [interval]",
    # ---- Fig 14
    "Notificações de LGBTfobia no Sinan, {}": "LGBTphobia notifications in Sinan, {}",
    "BOs de LGBTfobia no Anuário, {}": "LGBTphobia police reports in the Yearbook, {}",
    "(a) Cada bolha é um estado (n = {})": "(a) Each bubble is a state (n = {})",
    "bolha = população Spearman das contagens: {}": "bubble = population\nSpearman of the counts: {}",
    "Correlação entre as duas séries (Spearman)": "Correlation between the two series (Spearman)",
    "só contagens": "counts only",
    "só pelo tamanho do estado": "expected from state size alone",
    "descontado o tamanho (IC95%)": "size-adjusted (95% CI)",
    "(b) Concordância por ano": "(b) Agreement by year",
    "descontado o tamanho, sobra pouco e inclui zero": "after adjusting for size,\nlittle remains and it includes zero",
    # ---- Fig 15
    "Ideologia do governador, comparada à média do próprio estado e do ano (pontos, de {} = esquerda a {} = direita)":
        "Governor's ideology, relative to the mean of the state and the year\n(points, from {} = left to {} = right)",
    "Taxa de homicídio, comparada à média do estado e do ano (%)": "Homicide rate, relative to the mean\nof the state and the year (%)",
    "faixa compatível com os dados (IC95%)": "range compatible with the data (95% CI)",
    "reta estimada": "estimated line",
    "a reta é quase plana: não há relação visível": "the line is almost flat:\nno visible relationship",
    # ---- Fig 17
    "{} adultos": "{} adults",
    "{}% de poder para aumento de {}% ou mais": "{}% power to detect an increase of {}% or more",
    "PNS {} (o que existe)": "PNS {} (what exists)",
    "Uma nova rodada dedicada tipo PNS": "A new dedicated\nPNS-style round",
    "Módulo anual na PNAD Contínua": "Annual module in PNAD Contínua",
    "Necessário para detectar +{}%": "Needed to detect +{}%",
    "Adultos entrevistados ou triados por rodada (milhares)": "Adults interviewed or screened per round (thousands)",
    "faltam {} adultos para detectar aumento de {}%": "{} more adults needed\nto detect a {}% increase",
    # ---- Fig 18
    "ignorado ou em branco": "unknown or blank",
    "não se aplica": "not applicable",
    "outro motivo (sexismo, racismo, família…)": "other motive (sexism, racism, family…)",
    "LGBTfobia": "LGBTphobia",
    "% das notificações": "% of notifications",
    "(a) O que ficou registrado como motivo da violência": "(a) What was recorded as the motive for the violence",
    "quase um terço sem motivo": "almost a third with no motive",
    "% de LGBTfobia": "% LGBTphobia",
    "(b) A fatia de LGBTfobia, ampliada": "(b) The LGBTphobia share, enlarged",
    # ---- Fig 19
    "RR": "RR",
    "Homicídios por {} mil habitantes": "Homicides per {},000 inhabitants",
    "Domicílios com internet (%)": "Households with internet (%)",
    "Mortes de LGBT+ contadas pelo GGB por milhão de habitantes": "LGBT+ deaths counted by GGB\nper million inhabitants",
    "(a) Homicídio: acompanha (ρ = {})": "(a) Homicide: tracks it (ρ = {})",
    "(b) Internet: some com o homicídio (ρ = {})": "(b) Internet: vanishes with homicide (ρ = {})",
    "razão da contagem por desvio-padrão de homicídio: {} ({} a {}) só com homicídio; {} ({} a {}) com internet no modelo":
        "count ratio per\nstandard deviation of homicide:\n{} ({} to {})\nwith homicide only;\n{} ({} to {})\nwith internet\nin the model",
    "internet sozinha: {} ({} a {}) com homicídio junto: {} ({} a {})": "internet alone:\n{} ({} to {})\nwith homicide added:\n{} ({} to {})",
    # ---- Fig 20
    "{}: Temer assume": "{}: Temer\ntakes office",
    "{}: Bolsonaro assume": "{}: Bolsonaro\ntakes office",
    "{}: Lula assume": "{}: Lula\ntakes office",
    "Mortes por agressão por {} mil, igual padrão de idade": "Deaths by assault per {},000,\nage-standardized",
    "agressão (X85-Y09)": "assault (X85-Y09)",
    "a queda já começou em {}, antes da troca de {}": "the drop began in {},\nbefore the {} change",
    "(a) A taxa nacional cai a partir de {}": "(a) The national rate falls from {}",
    "{}: troca": "{}: change of president",
    "{}: quebra um ano antes": "{}: break one year earlier",
    "Variação de nível da taxa depois da troca, %": "Change in rate level after the change, %",
    "menor efeito detectável ({}% de poder)": "minimum detectable effect ({}% power)",
    "quebra em {}: queda de {}%; depende da data": "break in {}:\ndrop of {}%;\ndepends on the date",
    "variação [IC95%]": "change [95% CI]",
    "(b) Cada troca x a mesma conta com a quebra um ano antes": "(b) Each change vs. the same estimate one year earlier",
    # ---- Fig 21
    "Principal: governador {} pontos à direita, presidente PT → PSL": "Main: governor {} points to the right,\npresident PT → PSL",
    "Distância entre governador e presidente ({} pontos)": "Distance between governor and president ({} points)",
    "Escore de ideologia único ({})": "Single ideology score ({})",
    "Sem o ano de {} (troca no meio do ano)": "Without {} (change mid-year)",
    "Outra escala de ideologia (Zucco e Power)": "Alternative ideology scale (Zucco and Power)",
    "Governador do mesmo partido do presidente": "Governor from the same party as the president",
    "Total (agressão + indeterminada)": "Total (assault + undetermined)",
    "Contraste principal e variações": "Main contrast and variations",
    "Por grupo": "By group",
    "Agressão + indeterminada, por grupo": "Assault + undetermined, by group",
    "Variação da taxa de homicídio no contraste de cada análise, %": "Change in the homicide rate in each analysis's contrast, %",
    "análise principal": "main analysis",
    "outras análises (robustez e grupos)": "other analyses (robustness and groups)",
    "além dos traços pretos, poder de {}% ou mais": "beyond the black ticks,\npower of {}% or more",
    # ---- Fig 22
    "Dilma": "Dilma", "Temer": "Temer", "Bolsonaro": "Bolsonaro", "Lula": "Lula",
    "Mortes por {} mil, padronizada por idade": "Deaths per {},000,\nage-standardized",
    "a queda começou em {}": "the decline\nbegan in {}",
    "(a) A taxa nacional por governo": "(a) The national rate by administration",
    "Dilma: {} → {}": "Dilma: {} → {}",
    "Temer: {} → {}": "Temer: {} → {}",
    "Bolsonaro: {} → {}": "Bolsonaro: {} → {}",
    "Lula (em curso): {} → {}": "Lula (ongoing): {} → {}",
    "n/d (série desde {})": "n/a (series from {})",
    "agressão": "assault",
    "+ indeterminada": "+ undetermined",
    "{} anos antes da posse": "{} years before taking office",
    "Variação da taxa do ano-base ao último ano do governo, %": "Change in the rate, base year\nto last year of the term, %",
    "variação [intervalo de contagem]": "change\n[count interval]",
    "(b) Quanto a taxa variou em cada governo": "(b) How much the rate changed under each administration",
    # ---- Fig 23
    "Todas as {} trocas": "All {} changes",
    "Esquerda → direita": "Left → right",
    "Direita → esquerda": "Right → left",
    "Envolve o centro": "Involves the center",
    "Dentro do mesmo bloco": "Within the same bloc",
    "(a) Cada ponto é uma troca de governador": "(a) Each point is a governor change",
    "troca por troca": "change by change",
    "Variação da taxa do estado menos a do Brasil, {} anos antes → {} anos depois, %":
        "State rate change minus Brazil's, {} years before → {} years after, %",
    "{} subiram, {} caíram mediana {}% (n = {})": "{} rose, {} fell\nmedian {}% (n = {})",
    "{} subiram, {} caíram mediana {}% ($p$ = {})": "{} rose, {} fell\nmedian {}% ($p$ = {})",
    "a mediana cai dentro da faixa de referência: a diferença some": "the median falls inside the\nreference range: the difference vanishes",
    "Só agressão": "Assault only",
    "Agressão + causa indeterminada": "Assault + undetermined\ncause",
    "Variação da taxa do estado menos a do Brasil, %": "State rate change minus Brazil's, %",
    "(b) Somando as mortes de causa indeterminada, a diferença some": "(b) Adding deaths of undetermined cause, the difference vanishes",
    "uma troca": "one change",
    "mediana das trocas": "median of the changes",
    "faixa de {}% da mediana nos estados sem troca (referência)": "{}% range of the median in states without a change (reference)",
    # ---- Fig 25
    "Estudo": "Study", "População e país": "Population, country", "Causa e medida": "Cause and measure",
    "Resultado (escala própria em cada linha)": "Result (own scale on each row)",
    "ONS {}": "ONS {}",
    "NÃO É BRASIL": "NOT\nBRAZIL", "NÃO É HOMICÍDIO": "NOT\nHOMICIDE", "É BRASIL": "IS BRAZIL", "NÃO É TAXA": "NOT A\nRATE",
    "SEM RAZÃO COMBINADA": "NO POOLED\nRATIO",
    "Pessoas de {} anos ou mais, Censo {} ligado aos óbitos; Inglaterra e País de Gales":
        _quebra_barra("People aged {} or older, Census {} linked to deaths; England and Wales", 21),
    "Todas as causas. Razão LGB+/ heterossexuais, padronizada por idade":
        _quebra_barra("All causes. Age-standardized ratio, LGB+/heterosexual", 21),
    "LGB+ {} [{}-{}]": "LGB+ {} [{}-{}]",
    "gays e lésbicas {} [{}-{}]": "gay men and lesbians {} [{}-{}]",
    "bissexuais {} [{}-{}]": "bisexual people {} [{}-{}]",
    "homens gays {} [{}-{}]": "gay men {} [{}-{}]",
    "razão LGB+/héteros ({} = igual)": "ratio LGB+/hetero ({} = equal)",
    "Pessoas de {} anos ou mais; Inglaterra e País de Gales, março de {} a dezembro de {}":
        _quebra_barra("People aged {} or older; England and Wales, March {} to December {}", 21),
    "Suicídio (inclui intenção indeterminada). Taxa por {} mil, padronizada por idade":
        _quebra_barra("Suicide (includes undetermined intent). Rate per {},000, age-standardized", 21),
    "LGB+ {}": "LGB+ {}", "heterossexuais {}": "heterosexual {}",
    "suicídios por {} mil, no período": "suicides per {},000, in the period",
    "McKetta {}": "McKetta {}",
    "Enfermeiras lésbicas e bissexuais (coorte), Estados Unidos; {} óbitos no grupo LGB":
        _quebra_barra("Lesbian and bisexual nurses (cohort), United States; {} deaths in the LGB group", 21),
    "Todas as causas. Fator de aceleração: menor que {} = morre mais cedo (não é razão de riscos)":
        _quebra_barra("All causes. Acceleration factor: below {} = dies earlier (not a hazard ratio)", 21),
    "lésbicas e bissexuais {} [{}-{}]": "lesbian and bisexual\n{} [{}-{}]",
    "fator de aceleração ({} = igual)": "acceleration factor ({} = equal)",
    "Erlangsen {}": "Erlangsen {}",
    "Pessoas trans identificadas por diagnóstico ou mudança legal de gênero ({}); Dinamarca, {}-{}":
        _quebra_barra("Trans people identified by diagnosis or legal gender change ({}); Denmark, {}-{}", 21),
    "Todas as causas e suicídio ({} suicídios). Razão ajustada de taxas":
        _quebra_barra("All causes and suicide ({} suicides). Adjusted rate ratio", 21),
    "todas as causas {} [{}-{}]": "all causes {} [{}-{}]",
    "suicídio {} [{}-{}]": "suicide {} [{}-{}]",
    "razão trans/não trans ({} = igual)": "trans/non-trans ratio ({} = equal)",
    "Luis {}": "Luis {}",
    "Pessoas trans notificadas por violência no Sinan e pareadas aos óbitos do SIM, {}-{}":
        _quebra_barra("Trans people reported for violence in Sinan and linked to SIM deaths, {}-{}", 21),
    "Causas violentas (homicídio, suicídio e intenção indeterminada) entre os óbitos pareados; sem denominador":
        _quebra_barra("Violent causes (homicide, suicide and undetermined intent) among linked deaths; no denominator", 21),
    "óbitos pareados: causas violentas | outras": "linked deaths:\nviolent causes | other",
    "{} óbitos ({}% violentas)": "{} deaths ({}% violent)",
    "Zachry {}": "Zachry {}",
    "Revisão sistemática de estudos de minorias sexuais e de gênero, vários países":
        _quebra_barra("Systematic review of studies on sexual and gender minorities, several countries", 21),
    "Mortalidade, por estudo. {} estudos têm homicídio como desfecho, direções divergentes":
        _quebra_barra("Mortality, by study. {} studies have homicide as an outcome, with divergent directions", 21),
    "estudos: sustenta | em parte | não acha": "studies:\nsupport | partly | find none",
    "{} estudos incluídos": "{} studies included",
    "McLellan {}": "McLellan {}",
    "Adultos trans e de gênero diverso, metanálise de {} estudos, vários países":
        _quebra_barra("Trans and gender-diverse adults, meta-analysis of {} studies, several countries", 21),
    "Violência física ou sexual ao longo da vida (prevalência). Homicídio: nenhum estudo reportou prevalência":
        _quebra_barra("Lifetime physical or sexual violence (prevalence). Homicide: no study reported prevalence", 21),
    "violência na vida {}% [{}-{}]": "lifetime violence\n{}% [{}-{}]",
    "% com violência na vida": "% with lifetime violence",
    # ---- Fig 26
    "casos sorteados da lista de {}": _w("cases sampled from the {} list", 20),
    "com a matéria recuperada": _w("with the article retrieved", 20),
    "em que a matéria é do caso": _w("where the article is about the case", 20),
    "com morte violenta confirmada": _w("with violent death confirmed", 20),
    "e a fonte diz expressamente que a vítima é LGBT+": _w("and the source expressly says the victim is LGBT+", 20),
    "{} sem matéria recuperada: {} link morto, {} site inacessível, {} bloqueio ou erro, {} sem link: não dá para verificar":
        _w("{} with no article retrieved: {} dead link, {} site unreachable, {} blocked or server error, {} no link: cannot be verified", 42),
    "{} em que a matéria não é a do caso": _w("{} where the article is not about the case", 42),
    "{} sem morte violenta confirmada (indeterminada ou não violenta)": _w("{} without confirmed violent death (undetermined or non-violent)", 42),
    "{} com morte violenta, mas sem a identificação expressa como LGBT+ na fonte":
        _w("{} with violent death, but no express identification as LGBT+ in the source", 42),
    "motivo desconhecido ou não reportado": "unknown or unreported motive",
    "conflito interpessoal": "interpersonal conflict",
    "roubo ou latrocínio": "robbery or robbery-murder",
    "passional": "crime of passion",
    "suicídio": "suicide",
    "LGBTfobia atribuída na própria fonte": "LGBTphobia attributed in the source itself",
    "mortes violentas confirmadas (n = {})": "confirmed violent deaths (n = {})",
    "(b) O motivo que a própria fonte registra": "(b) The motive recorded by the source itself",
    "(a) De {} casos sorteados a {} com todos os critérios": "(a) From {} sampled cases to {} meeting all criteria",
    # ---- Fig 27
    "RR {}": "RR {}",
    "RR hipotético (risco dos LGB+ ÷ pares)": "Hypothetical RR (LGB+ risk ÷ peers)",
    "(a) {}": "(a) {}", "(b) {}": "(b) {}",
    "Cobertura = contagem ÷ mortes esperadas, %": "Coverage = count ÷ expected deaths, %",
    "todas as mortes declaradas": "all reported deaths",
    "só homicídios e latrocínios": "homicides and robbery-murders only",
    "cenário de subtração (sem pessoas trans)": "subtraction scenario (excluding trans people)",
    "{}% de cobertura exigiria risco bem menor que o dos pares: é conta, não estimativa":
        "{}% coverage\nwould require a risk\nwell below that of\npeers: it is arithmetic,\nnot an estimate",
    # ---- Fig 28
    "2020S1: formato B": "2020H1: format B",
    "2020S2: formato C": "2020H2: format C",
    "2022S2: formulário novo": "2022H2: new form",
    "{}: motivação sai": "{}: no motive",
    "Registros do módulo LGBT por ano": "LGBT-module records per year",
    "{} ({} formatos)": "{}\n({} formats)",
    "{} até setembro": "{}\nthrough September",
    "{}-{}: linhas do arquivo (vítima x suspeito, sem chave de pessoa)": "{}-{}: file rows\n(victim x suspect, no person key)",
    "{}-{}: denúncias com ao menos uma linha no módulo LGBT": "{}-{}: complaints\nwith at least one row\nin the LGBT module",
    "(a) O módulo LGBT em cada ano: a unidade e o formato mudam ao longo da série": "(a) The LGBT module each year: unit and format change along the series",
    "Registros do canal inteiro (milhares)": "Records, whole channel\n(thousands)",
    "unidade: linhas": "unit: rows",
    "unidade: denúncias": "unit: complaints",
    "(b) O canal inteiro cresce; em cima de cada barra, a parte do módulo LGBT": "(b) The whole channel grows; above each bar, the LGBT module share",
}
# siglas de UF (anotacoes dos maiores estados): identicas nos dois idiomas
EN.update({uf: uf for uf in ("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())})


def rotulos(lang: str, secao: str) -> dict:
    """Tabela de rotulos de es/it/he (chave = texto pt com numeros -> {}), em arquivo por idioma (fase es/it/he, 2026-11-24)."""
    return json.loads((Path(__file__).resolve().parent / "rotulos" / f"{lang}.json").read_text(encoding="utf-8"))[secao]


def espelho_he() -> None:
    """Hebraico: regras de desenho em bidi_he.py (legenda, sinal de numero, linha com formula), comuns ao v05."""
    import importlib.util        # -I nao poe a pasta do roteiro no caminho de import
    sp = importlib.util.spec_from_file_location("bidi_he", Path(__file__).resolve().parent / "bidi_he.py")
    bidi_he = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(bidi_he)
    bidi_he.instalar()


def main() -> None:
    """Gera as 22 figuras no idioma pedido, mais valores_plotados.json e textos_fora_da_imagem.json."""
    global LANG, _FIG_ATUAL, TAB, SAIDA
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", choices=("pt-BR", "en", "es", "it", "he"), required=True)
    ap.add_argument("--saida", default=str(SAIDA), help="pasta de saida (padrao: <raiz>/.run/figuras-artigo)")
    ap.add_argument("--chaves", action="store_true", help="so lista (JSON) os textos pt que T() viu, para montar a tabela EN; nao grava figuras")
    arg = ap.parse_args()
    LANG = arg.lang
    SAIDA = Path(arg.saida)
    TAB = EN if LANG == "en" else ({} if LANG == "pt-BR" else rotulos(LANG, "make_figuras"))
    if LANG == "he":
        espelho_he()
    Text.set_text = _set_text_traduzido
    figs = (figura1, figura2, figura3, figura6, figura8, figura9, figura10, figura11, figura13, figura14, figura15,
            figura17, figura18, figura19, figura20, figura21, figura22, figura23, figura25, figura26, figura27, figura28)
    if arg.chaves:                       # so exercita o desenho (saida descartavel) e lista os textos pt vistos por T()
        with tempfile.TemporaryDirectory(prefix="figuras-chaves-") as tmp:
            SAIDA = Path(tmp)
            for f in figs:
                f()
        print(json.dumps(_CHAVES, ensure_ascii=False, indent=0))
        return
    for f in figs:
        _FIG_ATUAL = f.__name__          # para dizer em que figura faltou traducao
        f()
    for nome in _NOMES:
        conferir_pdf(nome)
    bruto = json.dumps(VALORES, ensure_ascii=False, indent=1) + "\n"
    assert S0 not in bruto and S1 not in bruto
    pasta = SAIDA / "valores" / LANG
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "valores_plotados.json").write_text(bruto, encoding="utf-8")
    (pasta / "textos_fora_da_imagem.json").write_text(json.dumps(TEXTOS, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] {len(figs)} figuras ({LANG}: SVG+PDF sem fundo) em {SAIDA / LANG}; valores e textos em {pasta}")


if __name__ == "__main__":
    main()
