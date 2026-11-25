# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Apply right-to-left drawing rules for Hebrew to the article figures.

Patches matplotlib so that figures drawn with the Hebrew language setting follow right-to-left
layout: legend markers on the right of the text, a right-to-left mark at the start of each line
with Hebrew, left-to-right marks around signed numbers, leading-dot decimals and Latin
abbreviations ending in a plus sign, visual-order conversion for lines that contain a formula,
mirrored placement of side-by-side panels, panel letters and shared axes, and reversed legend
columns. The rules are applied once per figure at its first save and need matplotlib 3.11 and
python-bidi 0.4.2.

Inputs
------
- none (library module imported by make_figuras.py and make_figuras_v05.py; it receives
  matplotlib objects and label text from them)

Outputs
-------
- none (library module imported by make_figuras.py and make_figuras_v05.py)

Usage
-----
Imported by figures/article/code/make_figuras.py and figures/article/code/make_figuras_v05.py;
not run directly.

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Regras de desenho do hebraico nas figuras (make_figuras.py e make_figuras_v05.py), fase es/it/he, 2026-11-24.

Exige matplotlib >= 3.11 (libraqm: ordem bidirecional e forma das letras) e python-bidi 0.4.2 (a 0.6 reordena mas
nao espelha parenteses). Tres regras, so para --lang he:
1. legenda com o marcador a direita do texto (`legend.markerfirst` nao e rcParam: padrao trocado em Legend.__init__);
   legenda de FIGURA ancorada a esquerda vai para a direita (linhas alinhadas a direita invadiam o rotulo do eixo no
   fig23); legenda dentro do eixo fica onde esta, porque o eixo de dados nao se espelha;
2. toda linha com hebraico comeca com RLM (U+200F), senao uma linha que comeca por numero vira paragrafo da
   esquerda para a direita; numero com sinal (-10.8%, +13.1%), decimal sem zero (APA: .59, -.25) e "LGBT+" ficam da
   esquerda para a direita: marca LRM (U+200E) antes do sinal ou do ponto e depois do "+" colado em letra latina; sem
   ela o sinal ou o ponto vai para o outro lado do numero (".59" saia "59.", fig14);
3. linha com formula ($p$) nao passa pela libraqm (o matplotlib desenha a formula glifo a glifo, da esquerda para a
   direita) e o hebraico sairia invertido: essa linha e convertida para a ordem visual antes do desenho, com a
   formula protegida. O python-bidi 0.4.2 nao tem o pareamento de parenteses do Unicode 6.3 (regra N0, que a
   libraqm aplica): parentese com conteudo latino cujo primeiro caractere forte antes dele e latino (ou a marca LRM
   de um numero com sinal) ganha LRM no fim e fica no trecho da esquerda para a direita ("-0.7% (p = .016)"), como a
   libraqm faz nas outras linhas. Conferencia: inspecao dos PDFs he gerados.
4. disposicao da direita para a esquerda, como a amostra de referencia aprovada (fig_v05_02): titulo de
   painel alinhado a direita (a letra hebraica vem da tabela rotulos/he.json, inclusive "(א) {}" da fig27); paineis
   lado a lado trocam de lugar (o primeiro na leitura fica a direita), refletindo a caixa de cada painel COM os rotulos
   dele dentro da faixa da linha; letra de painel solta (texto de uma letra so, fig_v05_03) vai para o canto direito;
   eixo y compartilhado (fig27): numeros e titulo do eixo passam para o painel que ficou a esquerda; legenda de varias
   colunas com as colunas invertidas (primeira entrada a direita; coluna curta completada com entrada vazia em baixo).
   Dentro do eixo nada muda (o eixo de dados nao se espelha). Figura de quadro unico com eixos embutidos (fig25) fica
   como esta. Aplicada uma vez por figura, no primeiro savefig (svg e pdf saem iguais).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import re

import matplotlib
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.patches import Rectangle
from matplotlib.text import Text

LRM, RLM = "\u200e", "\u200f"
_HEB = re.compile(r"[א-ת]")
_SINAL = re.compile(r"(?<![\w.,])([−+\-]\.?|\.)(?=\d)")  # sinal de numero (nao hifen) e ponto de decimal sem zero
_MAIS_LATINO = re.compile(r"(?<=[A-Za-z])\+")            # LGBT+, LGB+
_FORMULA = re.compile(r"\$[^$]+\$")
_PAR = re.compile(r"\([^()]*\)")
_LATINO = re.compile(r"[A-Za-z\ue000-\ue0ff]")


def _forte_antes_e_latino(s: str) -> bool:
    """Regra N0: o primeiro caractere forte antes do parentese e da esquerda para a direita? (numero nao e forte)."""
    forte = next((c for c in reversed(s) if c == LRM or c.isalpha() or "\ue000" <= c <= "\ue0ff"), "")
    return forte == LRM or bool(_LATINO.fullmatch(forte))


def _parenteses_n0(s: str) -> str:
    """Parentese com conteudo latino em contexto latino ganha LRM no fim (o que a regra N0 faria)."""
    return _PAR.sub(lambda m: m.group() + (LRM if _LATINO.search(m.group()) and _forte_antes_e_latino(s[:m.start()]) else ""), s)


def ltr_numeros(s: str) -> str:
    """Regra 2: LRM antes do sinal de numero ou do ponto de decimal sem zero, e depois do '+' de sigla latina."""
    return _MAIS_LATINO.sub("+" + LRM, _SINAL.sub(LRM + r"\1", s))


def ordem_visual(s: str) -> str:
    """Regra 3: linha com formula -> ordem visual (base RTL), formula intacta, sem marcas invisiveis no fim."""
    from bidi.algorithm import get_display

    formulas = _FORMULA.findall(s)
    guarda = [chr(0xE000 + i) for i in range(len(formulas))]   # uso privado: classe L, um caractere por formula
    for f, g in zip(formulas, guarda):
        s = s.replace(f, g, 1)
    s = _parenteses_n0(ltr_numeros(s))
    v = get_display(s, base_dir="R").replace(LRM, "")
    for f, g in zip(formulas, guarda):
        v = v.replace(g, f)
    return v


def colunas_rtl(handles: list, labels: list, ncols: int) -> tuple:
    """Regra 4, legenda: inverte a ordem das COLUNAS (o matplotlib enche coluna a coluna, as primeiras mais cheias)."""
    n = len(handles)
    nc = min(ncols, n)
    if nc < 2:
        return handles, labels
    linhas, maiores = divmod(n, nc)
    tamanhos = [linhas + 1] * maiores + [linhas] * (nc - maiores)
    cheia = max(tamanhos)
    cols, i = [], 0
    for t in tamanhos:
        vazio = [(Rectangle((0, 0), 0, 0, visible=False), "")] * (cheia - t)
        cols.append(list(zip(handles[i:i + t], labels[i:i + t])) + vazio)
        i += t
    pares = [p for c in reversed(cols) for p in c]
    return [h for h, _ in pares], [rotulo for _, rotulo in pares]


def _caixa(ax, r):
    """Caixa do painel com rotulos e titulo, em fracao da figura."""
    return ax.get_tightbbox(r).transformed(ax.figure.transFigure.inverted())


def _linhas_de_paineis(axs: list) -> list:
    """Agrupa paineis cujas faixas verticais se cruzam (mesma linha), cada linha ordenada da esquerda para a direita."""
    grupos = []
    for a in sorted(axs, key=lambda a: -a.get_position().y1):
        p = a.get_position()
        cruza = (lambda q: min(p.y1, q.get_position().y1) > max(p.y0, q.get_position().y0))  # noqa: B023
        g = next((g for g in grupos if any(cruza(q) for q in g)), None)
        (g.append(a) if g is not None else grupos.append([a]))
    return [sorted(g, key=lambda a: a.get_position().x0) for g in grupos if len(g) > 1]


def espelhar_paineis(fig) -> None:
    """Regra 4 na figura inteira, uma vez so (marca no objeto)."""
    if getattr(fig, "_he_espelhada", False):
        return
    fig._he_espelhada = True
    axs = [a for a in fig.axes if a.get_visible()]
    for a in axs:   # titulo de painel a direita
        # ponytail: _left_title/_right_title sao privados, mas set_title(loc="right") zeraria o afastamento (pad) que o
        # roteiro deu ao titulo, e ele desceria sobre o que esta no topo do eixo (fig_v05_08: nomes dos governos)
        t, d = a._left_title, a._right_title
        if t.get_text():
            d.set_text(t.get_text())
            d.set_fontproperties(t.get_fontproperties())
            d.set_color(t.get_color())
            d.set_y(t.get_position()[1])
            t.set_text("")
    pos = [a.get_position() for a in axs]
    if any(i != j and p.x0 <= q.x0 and q.x1 <= p.x1 and p.y0 <= q.y0 and q.y1 <= p.y1
           for i, p in enumerate(pos) for j, q in enumerate(pos)):
        return   # quadro unico com eixos embutidos (fig25): fica como esta
    r = fig.canvas.get_renderer()
    for linha in _linhas_de_paineis(axs):
        if any(b.get_position().x0 < a.get_position().x1 for a, b in zip(linha, linha[1:])):
            continue   # paineis que se sobrepoem na horizontal nao sao lado a lado
        if all(b in linha[0].get_shared_y_axes().get_siblings(linha[0]) for b in linha):
            # eixo y compartilhado: troca as caixas na ordem inversa e passa numeros e titulo do eixo para a esquerda
            caixas = [a.get_position() for a in linha]
            rotulo = (linha[0].get_ylabel(), linha[0].yaxis.label.get_fontsize())
            for a, c in zip(reversed(linha), caixas):
                a.set_position(c)
            for k, a in enumerate(reversed(linha)):
                a.tick_params(axis="y", labelleft=k == 0)
                a.set_ylabel(rotulo[0] if k == 0 else "", fontsize=rotulo[1])
            continue
        caixas = [_caixa(a, r) for a in linha]
        esq, dir_ = min(c.x0 for c in caixas), max(c.x1 for c in caixas)
        letras = [t for t in list(fig.texts) + [t for a in linha for t in a.texts]
                  if len(t.get_text().strip()) == 1 and _HEB.fullmatch(t.get_text().strip())]
        extensoes = [t.get_window_extent(r).transformed(fig.transFigure.inverted()) for t in letras]
        for a, c in zip(linha, caixas):
            p = a.get_position()
            a.set_position([p.x0 + (esq + dir_ - c.x1) - c.x0, p.y0, p.width, p.height])
        for t, e in zip(letras, extensoes):   # letra de painel: a borda esquerda refletida vira o canto direito
            if not (min(c.y0 for c in caixas) - 0.1 <= e.y0 and e.y1 <= max(c.y1 for c in caixas) + 0.1):
                continue
            t.set_transform(fig.transFigure)
            t.set_position((esq + dir_ - e.x0, e.y1))
            t.set_horizontalalignment("right")
            t.set_verticalalignment("top")


def instalar() -> None:
    """Liga as tres regras para o processo inteiro (chamar uma vez, so com --lang he)."""
    assert tuple(int(x) for x in matplotlib.__version__.split(".")[:2]) >= (3, 11), matplotlib.__version__
    legenda = Legend.__init__

    def init(self, parent, *a, **k):
        k.setdefault("markerfirst", False)
        nc = k.get("ncols", k.get("ncol", 1))
        if len(a) >= 2 and nc > 1:
            a = (*colunas_rtl(list(a[0]), list(a[1]), nc), *a[2:])
        loc, ancora = k.get("loc"), k.get("bbox_to_anchor")
        if isinstance(parent, Figure) and isinstance(loc, str) and "left" in loc and ancora is not None and len(ancora) == 2:
            k["loc"], k["bbox_to_anchor"] = loc.replace("left", "right"), (1 - ancora[0], ancora[1])
        legenda(self, parent, *a, **k)
    Legend.__init__ = init

    # ponytail: _preprocess_math e privado, mas e o unico ponto por onde passa CADA linha antes do desenho (o
    # matplotlib decide formula linha a linha); a versao minima esta travada pelo assert acima.
    preprocessa = Text._preprocess_math

    def por_linha(self, s):
        s, formula = preprocessa(self, s)
        if not _HEB.search(s):
            return s, formula
        return (ordem_visual(s) if formula is True else RLM + ltr_numeros(s)), formula
    Text._preprocess_math = por_linha

    salvar = Figure.savefig

    def savefig(self, *a, **k):
        espelhar_paineis(self)
        return salvar(self, *a, **k)
    Figure.savefig = savefig
