# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Draw five figures of the article (1, 2, 3, 4 and 8) as vector files without background.

Reads the figure source data copied into the repository and draws the five figures in one of
five languages (Brazilian Portuguese, English, Spanish, Italian, Hebrew), as SVG and PDF with a
transparent background. Every drawn text goes through a translation function, and an English
key with no entry aborts the run. Title, note and source are not drawn in the image. The
drawing code is a self-contained copy of the repository figure generators; the repository is
only read. Hebrew uses the right-to-left rules of bidi_he.py.

Inputs
------
- figures/fontes/ (copies of the source data of the figures)
- figures/article/code/rotulos/<language>.json (label tables)
- figures/article/code/bidi_he.py (loaded for Hebrew)

Outputs
-------
- .run/figuras-artigo/<language>/<figure>.svg and .pdf (default folder, not tracked in git;
  changed with --saida)

Usage
-----
PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras_v05.py
--lang pt-BR|en|es|it|he [--saida <folder>]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Cinco figuras da v0.5 do artigo (1, 2, 3, 4 e 8) em versao bilingue, vetorial e sem fundo.

Autossuficiente: o codigo de desenho foi COPIADO de lgbt-indicador-violencia (figures/make_figures.py e dos geradores
data/exposicao/fig_caminho_v05.py, data/pns/fig_pns_v05.py, data/pns/fig_agressor_pns2019.py,
data/disque100/fig_disque_v05.py, data/exposicao/fig_series_por_governo.py). O repositorio e SOMENTE LEITURA: aqui ele
so e lido, a partir da raiz do pacote (REPO_ROOT). Titulo, nota e fonte nao sao desenhados na imagem (regra dos originais).

Todo texto desenhado passa por T(chave_pt); em --lang en uma chave sem entrada em EN aborta (SystemExit), e o texto
final de cada figura e conferido contra palavras e acentos do portugues. Numeros: br()/miles() por idioma.

Uso: PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras_v05.py --lang pt-BR|en|es|it|he [--saida <pasta>]
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
import sys
import textwrap
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.text as mtext  # noqa: E402
from matplotlib.transforms import Bbox  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

REPO = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[3])   # raiz do pacote
FONTES = REPO / "figures" / "fontes"
SAIDA_BASE = REPO / ".run" / "figuras-artigo"

PALETA = {
    "lgb": "#2a78d6", "hetero": "#eb6834",
    "estat": "#6b3fa0", "estat_cl": "#cdbde6", "ref": "#4b4a46",
    "nao": "#b03a6e", "sv": "#8b8a85",
    "fonte_a": "#6b3fa0", "fonte_a_cl": "#cdbde6", "fonte_b": "#1b8f8a", "fonte_b_cl": "#9fd8d4", "ref_cl": "#e6e5e0",
}
INK, INK2, GRADE = "#1f1f1e", "#5b5a55", "#d9d8d3"
MIN_PT = 8
LGB, HET, ESTAT = "#2a78d6", "#eb6834", "#6b3fa0"

# ---------------------------------------------------------------- idioma
LANG = "pt-BR"

EN = {
    # ---- Figura 1
    "1. Acontece": "1. It happens",
    "2. A pessoa\nprocura serviço\nou polícia": "2. The person\nseeks a service\nor the police",
    "3. Fica\num papel": "3. A paper\nrecord is made",
    "4. Alguém\nclassifica o motivo\ne o grupo": "4. Someone\nclassifies the\nmotive and group",
    "5. Sai a\ncontagem": "5. The count\ncomes out",
    "PNS": "PNS", "Sinan": "Sinan", "BO (Anuário)": "Police report\n(Yearbook)", "Disque 100": "Disque 100", "SIM": "SIM", "GGB": "GGB",
    "pergunta direto à pessoa": "asks the person directly",
    "procura serviço de saúde": "seeks health care",
    "ficha de notificação": "notification form",
    "profissional anota a orientação e o motivo": "professional records the orientation and the motive",
    "sem motivo útil: {}% (2015); {}% a {}% (2023-25)": "motive missing: {}% (2015); {}% to {}% (2023-25)",
    "{}% x {}%": "{}% vs {}%",
    "vai à polícia": "goes to the police",
    "boletim de ocorrência": "police report",
    "a polícia dá o enquadramento penal": "the police assign the criminal charge",
    "liga e denuncia": "calls and reports",
    "registro da denúncia": "complaint record",
    "o atendente classifica†": "the operator classifies†",
    "só contagem de registros": "record counts only",
    "morre": "dies",
    "declaração de óbito": "death certificate",
    "causa da morte, sim; orientação: nenhum campo": "cause of death, yes; orientation: no field",
    "sem número de LGBT+": "no LGBT+ count",
    "vira notícia": "makes the news",
    "matéria": "news story",
    "quem coleta decide “é LGBT+” e o motivo": "the collector decides “is LGBT+” and the motive",
    "{}, {} e {} (2023-2025)": "{}, {} and {} (2023-2025)",
    "pula as etapas 2 a 4": "skips steps 2 to 4",
    "não depende de a pessoa procurar ajuda": "does not depend on the person seeking help",
    "a pessoa diz a orientação; sem motivo do agressor": "the person states the orientation; no perpetrator motive",
    "Quem fica de fora": "Who is left out",
    "quem não procurou serviço e quem não registrou": "those who did not seek care and those not recorded",
    "o que não virou notícia": "what did not make the news",
    "o que ninguém anotou": "what nobody recorded",
    "O TSE e o escore de ideologia dos partidos classificam governos; Câmara e Senado registram o que se diz.\nNenhum dos dois mede violência. † etapa não descrita neste artigo":
        "The TSE (Brazil's electoral court) and the party ideology score classify governments;\nthe Chamber and the Senate record what is said. Neither measures violence.\n† step not described in this article",
    "✗": "✗",
    # ---- Figura 2
    "Física": "Physical", "Sexual": "Sexual", "Psicológica": "Psychological", "Qualquer tipo": "Any type",
    "LGB+": "LGB+", "Heterossexuais": "Heterosexual",
    "Adultos que relataram violência em 12 meses (%)": "Adults reporting violence in 12 months (%)",
    "a  Quantos relataram": "a  How many reported",
    "razão bruta": "crude ratio", "razão ajustada": "adjusted ratio",
    "Razão LGB+ / heterossexuais (escala log; 1 = igual)": "Ratio, LGB+ / heterosexual (log scale; 1 = equal)",
    "b  A razão entre os dois grupos": "b  The ratio between the two groups",
    # ---- Figura 3
    "Parceiro(a) ou ex": "Partner or ex-partner",
    "Familiar": "Family member",
    "Amigo(a), colega\nou vizinho(a)": "Friend, colleague\nor neighbor",
    "Pessoa desconhecida": "Stranger",
    "Empregado(a), patrão ou chefe": "Employee, boss or supervisor",
    "Empregado, patrão,\npolicial ou outro": "Employee, boss,\npolice officer or other",
    "Parceiro ou ex": "Partner or ex",
    "Amigo, colega\nou vizinho": "Friend, colleague\nor neighbor",
    "Desconhecido": "Stranger",
    "Qualquer conhecido": "Any acquaintance",
    "por 100": "per 100",
    "a": "a", "b": "b",
    "Razão ajustada de risco,\nLGB+ / heterossexuais": "Adjusted risk ratio,\nLGB+ / heterosexual",
    # ---- Figura 4
    "2020S1: formato B": "2020 H1: format B",
    "2020S2: formato C": "2020 H2: format C",
    "2022S2: formulário novo": "2022 H2: new form",
    "2024: motivação sai": "2024: motive dropped",
    "Registros do módulo LGBT por ano": "LGBT-module records per year",
    "(2 formatos)": "(2 formats)",
    "até setembro": "to September",
    "2011-2019: linhas do arquivo\n(vítima x suspeito, sem chave de pessoa)": "2011-2019: file rows\n(victim vs suspect, no person key)",
    "2021-2026: denúncias\ncom ao menos uma linha\nno módulo LGBT": "2021-2026: complaints\nwith at least one row\nin the LGBT module",
    "(a) O módulo LGBT em cada ano: a unidade e o formato mudam ao longo da série": "(a) The LGBT module in each year: unit and format change along the series",
    "Registros do canal inteiro\n(milhares)": "Records of the whole channel\n(thousands)",
    "unidade: linhas": "unit: rows",
    "unidade: denúncias": "unit: complaints",
    "(b) O canal inteiro cresce; em cima de cada barra, a parte do módulo LGBT": "(b) The whole channel grows; above each bar, the LGBT-module share",
    # ---- Figura 8
    "Lula": "Lula", "Dilma": "Dilma", "Temer": "Temer", "Bolsonaro": "Bolsonaro",
    "agressão": "assault", "agressão + causa indeterminada": "assault + undetermined cause",
    "por 100 mil": "per 100,000",
    "a  Homicídio de toda a população (taxa padronizada; único painel que não é registro LGBT+)":
        "a  Homicide in the whole population (standardized rate; only panel that is not an LGBT+ record)",
    "b  Lista do GGB: mortes noticiadas na imprensa (contagem da organização)": "b  GGB list: deaths reported in the press (the organization's count)",
    "c  Disque 100, módulo LGBT: linhas até 2019 e denúncias desde 2021 (unidades diferentes)":
        "c  Disque 100, LGBT module: rows through 2019 and complaints since 2021 (different units)",
    "d  Fichas do SUS com motivo marcado como LGBTfobia": "d  SUS forms with the motive marked as LGBTphobia",
    "e  Boletins de ocorrência por homofobia ou transfobia (Anuário)": "e  Police reports for homophobia or transphobia (Yearbook)",
    "registros": "records",
}
_AUSENTES: list[str] = []


def T(pt: str) -> str:
    """Texto desenhado: pt-BR devolve a chave; en exige entrada em EN (senao falha alto)."""
    if LANG == "pt-BR":
        return pt
    tab = EN if LANG == "en" else TAB
    if pt not in tab:
        _AUSENTES.append(pt)
        raise SystemExit(f"ERRO: T() sem entrada na tabela {LANG} para {pt!r}")
    return tab[pt]


TAB: dict = {}   # es/it/he: scripts/figuras/rotulos/<lang>.json, secao v05 (fase es/it/he, 2026-11-24)


def _virgula() -> bool:
    """Formato de NUMERO (nao de idioma-fonte): pt-BR, es e it com virgula decimal; en e he com ponto."""
    return LANG in ("pt-BR", "es", "it")


def br(x: float, casas: int = 1) -> str:
    """Decimal por idioma (pt: virgula; en: ponto), ROUND_HALF_UP como nos originais."""
    d = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)
    s = f"{d:.{casas}f}"
    return s.replace(".", ",") if _virgula() else s


def miles(n: float) -> str:
    """Inteiro com separador de milhar por idioma (pt: ponto; en: virgula)."""
    s = f"{int(Decimal(repr(float(n))).quantize(Decimal(1), rounding=ROUND_HALF_UP)):,}"
    return s.replace(",", ".") if _virgula() else s


# ---------------------------------------------------------------- leitura (somente leitura no repositorio)
def ler_csv(nome: str) -> list[dict]:
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8")))


def ler_p(p: Path) -> list[dict]:
    return list(csv.DictReader(open(p, encoding="utf-8")))


def ler_pns(base: Path) -> dict:
    """Prevalencias e razoes (CSV) + IC das prevalencias (tabela 1 do .md)."""
    out: dict = {}
    for r in ler_p(base / "seguro_pns2019.csv"):
        if r["bloco"] == "nivel":
            out.setdefault(r["rotulo"], {}).update(lgb=100 * float(r["prev_grupo"]), het=100 * float(r["prev_ref"]),
                                                   rp=float(r["rp"]), rp_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
        elif r["bloco"] == "rp_ajustada":
            out[r["rotulo"]].update(rpaj=float(r["rp"]), rpaj_ic=[float(r["ic_lo"]), float(r["ic_hi"])])
    sec = (base / "seguro_pns2019.md").read_text(encoding="utf-8").split("## 1.")[1].split("## 2.")[0]
    for ln in sec.splitlines():
        m = re.match(r"\| (física|sexual|psicológica|qualquer) \| ([\d.]+)% \[([\d.]+); ([\d.]+)\] \| ([\d.]+)% \[([\d.]+); ([\d.]+)\]", ln)
        if m:
            out[m.group(1)].update(het_ic=[float(m.group(3)), float(m.group(4))], lgb_ic=[float(m.group(6)), float(m.group(7))])
    return out


D100_QUEBRAS = [(2020.0, "2020S1: formato B"), (2020.5, "2020S2: formato C"), (2022.5, "2022S2: formulário novo"), (2024.0, "2024: motivação sai")]


def ler_d100() -> dict:
    lin = {(int(r["ano"]), r["recorte"], r["unidade"]): int(r["n"]) for r in ler_csv("d100_serie_anual.csv")}
    out: dict = {}
    for ano in range(2011, 2027):
        un = "linhas" if ano <= 2020 else "denuncias"
        out[ano] = {"unidade": un, "lgbt": lin[(ano, "grupo_lgbt", un)], "canal": lin[(ano, "canal", un)]}
    return out


# ---------------------------------------------------------------- rc por figura (cada original tinha o seu)
def rc(tamanho: float, labelcolor: str | None):
    d = {"font.family": "DejaVu Sans", "font.size": tamanho, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
         "axes.spines.top": False, "axes.spines.right": False}
    if labelcolor:
        d["axes.labelcolor"] = labelcolor
    return plt.rc_context(d)


# ================================================================ Figura 1
def _caixa(ax, x, y, w, h, txt, ec, fc, fs=MIN_PT, bold=False, cpl=15, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, "\n".join(textwrap.wrap(txt, cpl)), ha="center", va="center", fontsize=fs, color=tc or INK,
            fontweight="bold" if bold else "normal", linespacing=1.12)


# largura (caracteres por linha) das caixas: en precisa de outra quebra; chave = texto em pt
CPL_EN = {"profissional anota a orientação e o motivo": 14, "quem coleta decide “é LGBT+” e o motivo": 15,
          "causa da morte, sim; orientação: nenhum campo": 13, "quem não procurou serviço e quem não registrou": 15}


def fig1():
    pns = ler_pns(FONTES)["física"]
    f55 = [r for r in ler_csv("serie_campo55_uf_ano.csv") if r["uf"] == "BR"]
    falt = {int(r["ano"]): float(r["pct_m_ign"]) + float(r["pct_m_na"]) for r in f55}
    f_ini, f_lo, f_hi = falt[2015], min(falt[a] for a in (2023, 2024, 2025)), max(falt[a] for a in (2023, 2024, 2025))
    anu = {(r["edicao"], r["ano_dado"]): int(r["registros"]) for r in ler_csv("anuario_lgbtfobia_uf_ano_v2.csv") if r["uf"] == "BR" and r["registros"]}
    bo0, bo1 = anu[("2024", "2022")], anu[("2026", "2025")]
    ggb = {int(r["ano"]): int(r["ggb"]) for r in ler_csv("serie_ggb_vs_cobertura.csv") if r["ggb"] != ""}
    # r35: altura so do desenho (6,55 -> 5,80 pol): cabecalho mais perto da 1a linha (0,8 -> 0,52), vao entre linhas 0,1 -> 0,04
    # (0,12 depois da PNS, cuja linha traz texto embaixo da seta) e sem a faixa vazia no pe; mesma largura e mesmo corpo. Na
    # edicao en a figura nao cabia na p. 11 (73% em branco, export r34)
    rh, y0, vao, pos_pns = 0.64, 0.52, 0.04, 0.08
    W, H = 7.4, y0 + 6 * (rh + vao) + pos_pns + 0.02 + 1.1
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W), ax.set_ylim(H, 0), ax.axis("off")
    x0, wc, gap = 1.2, 1.13, 0.1
    cx = [x0 + k * (wc + gap) for k in range(5)]
    etapas = ["1. Acontece", "2. A pessoa\nprocura serviço\nou polícia", "3. Fica\num papel", "4. Alguém\nclassifica o motivo\ne o grupo", "5. Sai a\ncontagem"]
    for k, e in enumerate(etapas):
        ax.text(cx[k] + wc / 2, 0.05, T(e), ha="center", va="top", fontsize=MIN_PT, fontweight="bold", color=INK)
    faixas = [
        ("PNS", "fonte_b", "pergunta direto à pessoa", None, None, None, T("{}% x {}%").format(br(pns["lgb"], 2), br(pns["het"], 2))),
        ("Sinan", "fonte_a", None, "procura serviço de saúde", "ficha de notificação", "profissional anota a orientação e o motivo",
         T("sem motivo útil: {}% (2015); {}% a {}% (2023-25)").format(br(f_ini, 1), br(f_lo, 1), br(f_hi, 1))),
        ("BO (Anuário)", "fonte_a", None, "vai à polícia", "boletim de ocorrência", "a polícia dá o enquadramento penal", f"{miles(bo0)} → {miles(bo1)} (2022-2025)"),
        ("Disque 100", "fonte_a", None, "liga e denuncia", "registro da denúncia", "o atendente classifica†", "só contagem de registros"),
        ("SIM", "fonte_a", None, "morre", "declaração de óbito", "causa da morte, sim; orientação: nenhum campo", "sem número de LGBT+"),
        ("GGB", "ref", None, "vira notícia", "matéria", "quem coleta decide “é LGBT+” e o motivo",
         T("{}, {} e {} (2023-2025)").format(ggb[2023], ggb[2024], ggb[2025])),
    ]
    cor = {"fonte_b": (PALETA["fonte_b"], PALETA["fonte_b_cl"]), "fonte_a": (PALETA["fonte_a"], PALETA["fonte_a_cl"]), "ref": (PALETA["ref"], PALETA["ref_cl"])}

    def tx(pt, **kw):  # texto de caixa: traduz e devolve (texto, cpl)
        cpl = kw.get("cpl", 15)
        if LANG != "pt-BR":
            cpl = CPL_EN.get(pt, cpl)
        return T(pt), cpl

    for i, (nome, tipo, e1, e2, e3, e4, e5) in enumerate(faixas):
        y = y0 + i * (rh + vao) + (pos_pns if i else 0)
        ec, fc = cor[tipo][0], "white"
        ax.text(0.1, y + rh / 2, T(nome), ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=ec, linespacing=1.12)
        if e1:
            t, c = tx(e1)
            _caixa(ax, cx[0], y, wc, rh, t, ec, fc, cpl=c)
            ax.annotate("", xy=(cx[4], y + rh / 2), xytext=(cx[0] + wc, y + rh / 2),
                        arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.8, "connectionstyle": "arc3,rad=-0.0", "linestyle": "--"})
            xm = (cx[1] + cx[3] + wc) / 2
            ax.text(xm, y + rh / 2 - 0.2, T("pula as etapas 2 a 4"), ha="center", va="center", fontsize=MIN_PT + 0.5, color=INK, fontweight="bold")
            ax.text(xm, y + rh / 2 - 0.05 + 0.2, T("não depende de a pessoa procurar ajuda"), ha="center", va="center", fontsize=MIN_PT, color=INK)
            ax.text(xm, y + rh / 2 + 0.3, T("a pessoa diz a orientação; sem motivo do agressor"), ha="center", va="center", fontsize=MIN_PT, color=INK2)
        else:
            ax.plot([cx[0] + wc / 2], [y + rh / 2], "o", color=PALETA["sv"], ms=6)
            for k, txt in zip((1, 2, 3), (e2, e3, e4)):
                t, c = tx(txt, cpl=13 if (nome == "SIM" and k == 3) else 15)
                _caixa(ax, cx[k], y, wc, rh, t, ec, fc, cpl=c)
                ax.annotate("", xy=(cx[k], y + rh / 2), xytext=(cx[k - 1] + (wc if k > 1 else wc / 2 + 0.08), y + rh / 2),
                            arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.4})
            ax.annotate("", xy=(cx[4], y + rh / 2), xytext=(cx[3] + wc, y + rh / 2), arrowprops={"arrowstyle": "->", "color": ec, "lw": 1.4})
            if nome == "SIM":
                ax.text(cx[3] + wc - 0.13, y + 0.13, T("✗"), ha="center", va="center", fontsize=17, color=PALETA["nao"], fontweight="bold")
        if e5 in EN:  # texto fixo (nao e numero montado): passa por T
            e5 = T(e5)
        _caixa(ax, cx[4], y, wc, rh, e5, ec, "white", bold=True, cpl=13 if len(e5) < 28 else 15)
    yb = y0 + 6 * (rh + vao) + pos_pns + 0.02
    ax.text(0.1, yb + 0.28, T("Quem fica de fora"), ha="left", va="center", fontsize=MIN_PT + 0.8, fontweight="bold", color=INK)
    for k, txt in ((1, "quem não procurou serviço e quem não registrou"), (2, "o que não virou notícia"), (3, "o que ninguém anotou")):
        t, c = tx(txt)
        _caixa(ax, cx[k], yb, wc, 0.62, t, PALETA["sv"], "white", cpl=c, tc=INK2)
    ax.text(0.05, yb + 0.82, T("O TSE e o escore de ideologia dos partidos classificam governos; Câmara e Senado registram o que se diz.\nNenhum dos dois mede violência. † etapa não descrita neste artigo"),
            ha="left", va="center", fontsize=MIN_PT, color=INK2)
    return fig, {}


# ================================================================ Figura 2
ORDEM = ["física", "sexual", "psicológica", "qualquer"]
NOMES = {"física": "Física", "sexual": "Sexual", "psicológica": "Psicológica", "qualquer": "Qualquer tipo"}


def fig2():
    d = ler_pns(REPO / "data" / "pns")
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.6), dpi=300, gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.45})
    y = list(range(len(ORDEM)))[::-1]
    off = 0.17
    for g, cor, dy, rot in (("lgb", LGB, off, "LGB+"), ("het", HET, -off, "Heterossexuais")):
        for k, yv in zip(ORDEM, y):
            v, (lo, hi) = d[k][g], d[k][g + "_ic"]
            a.errorbar([v], [yv + dy], xerr=[[v - lo], [hi - v]], fmt="o", ms=5, color=cor, ecolor=cor, elinewidth=1.6,
                       capsize=2.2, label=T(rot) if k == ORDEM[0] else None)
            a.annotate(f"{br(v, 2)}%", (hi, yv + dy), xytext=(4, -3), textcoords="offset points", fontsize=7, color=INK)
    a.set_yticks(y, [T(NOMES[k]) for k in ORDEM], fontsize=8.5)
    a.set_xlabel(T("Adultos que relataram violência em 12 meses (%)"), fontsize=7.5)
    a.set_xlim(-1, 62)
    a.grid(axis="x", color=GRADE, lw=0.5); a.set_axisbelow(True)
    a.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    a.set_title(T("a  Quantos relataram"), loc="left", fontsize=9, color=INK)
    a.set_ylim(-0.6, len(ORDEM) - 0.4)
    for tipo, mk, fc, rot in (("rp", "o", "white", "razão bruta"), ("rpaj", "s", ESTAT, "razão ajustada")):
        dy = off if tipo == "rp" else -off
        for k, yv in zip(ORDEM, y):
            v, (lo, hi) = d[k][tipo], d[k][tipo + "_ic"]
            b.errorbar([v], [yv + dy], xerr=[[v - lo], [hi - v]], fmt=mk, ms=5, mfc=fc, mec=ESTAT, color=ESTAT,
                       elinewidth=1.6, capsize=2.2, label=T(rot) if k == ORDEM[0] else None)
            b.annotate(br(v, 2), (hi, yv + dy), xytext=(4, -3), textcoords="offset points", fontsize=7, color=INK)
    b.set_xscale("log")
    b.axvline(1, color=INK2, lw=0.8, ls=(0, (3, 2)))
    b.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"]); b.minorticks_off()
    b.set_xlim(0.8, 25)
    b.set_ylim(a.get_ylim())
    b.set_yticks(y, [T(NOMES[k]) for k in ORDEM], fontsize=8.5)
    b.set_xlabel(T("Razão LGB+ / heterossexuais (escala log; 1 = igual)"), fontsize=7.5)
    b.grid(axis="x", color=GRADE, lw=0.5); b.set_axisbelow(True)
    b.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    b.set_title(T("b  A razão entre os dois grupos"), loc="left", fontsize=9, color=INK)
    # caixa justa medida no Agg + folga a direita: o texto vetorial do rotulo do painel b sai mais largo que a medida do Agg
    fig.canvas.draw()
    bb = fig.get_tightbbox(fig.canvas.get_renderer()).padded(0.1)
    bb = Bbox([[bb.x0, bb.y0], [bb.x1 + 0.3, bb.y1]])
    return fig, {"bbox_inches": bb}


# ================================================================ Figura 3
TIPOS = [("Parceiro(a) ou ex", "Parceiro(a) ou ex", "#6250d6"), ("Familiar", "Familiar", "#1baf7a"),
         ("Amigo(a), colega ou vizinho(a)", "Amigo(a), colega\nou vizinho(a)", "#eda100"),
         ("Pessoa desconhecida", "Pessoa desconhecida", "#e34948")]
OUTRO = (["Empregado(a), patrão ou chefe", "Policial", "Outro"], "Empregado, patrão,\npolicial ou outro", "#8b8a85")


def fig3():
    linhas = ler_p(REPO / "data" / "pns" / "agressor_risco_pns2019.csv")
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
    rmax, buraco = 1.0, 0.56
    centros = {"LGB+": (0.0, 0.0), "Heterossexuais": (1.62, -0.35)}
    for nome in ("LGB+", "Heterossexuais"):
        R = rmax * math.sqrt(total[nome] / total["LGB+"])
        cx, cy = centros[nome]
        ax.pie(fatias[nome], radius=R, center=(cx, cy), colors=cores, startangle=90, counterclock=False,
               wedgeprops={"width": R * (1 - buraco), "edgecolor": "white", "linewidth": 1.2})
        ax.text(cx, cy + 0.04 * R / rmax, br(total[nome], 2), ha="center", va="center", fontsize=11 if R > 0.7 else 8,
                fontweight="bold", color=INK)
        ax.text(cx, cy - 0.17 * (R / rmax) ** 0.5, T("por 100"), ha="center", va="center", fontsize=7, color=INK2)
        ax.text(cx, cy - R - 0.13, T(nome), ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        if nome == "LGB+":
            ang = 90.0
            for v, c in zip(fatias[nome], cores):
                meio = math.radians(ang - 360 * v / total[nome] / 2)
                ang -= 360 * v / total[nome]
                if v >= 1.8:
                    rr = R * (1 + buraco) / 2
                    ax.text(cx + rr * math.cos(meio), cy + rr * math.sin(meio), br(v, 2), ha="center", va="center",
                            fontsize=7.5, color="white" if c in ("#6250d6", "#e34948") else INK, fontweight="bold")
    ax.set_xlim(-1.08, 2.25); ax.set_ylim(-1.25, 1.08)
    ax.text(-1.06, 1.06, T("a"), fontsize=10, fontweight="bold", color=INK, va="top")
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in cores], labels=[T(r).replace("\n", " ") for r in rotulos],
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
        bx.text(hi * 1.12, y, br(m, 2), va="center", fontsize=7.5, color=INK)
    bx.axvline(1, color=INK2, lw=0.8, ls=(0, (3, 2)))
    bx.set_xscale("log"); bx.set_xlim(0.8, 25)
    bx.set_xticks([1, 2, 5, 10, 20]); bx.set_xticklabels(["1", "2", "5", "10", "20"])
    bx.minorticks_off()
    bx.set_yticks(range(len(itens))); bx.set_yticklabels([T(r) for _, r, _ in itens][::-1], fontsize=7.5)
    bx.set_xlabel(T("Razão ajustada de risco,\nLGB+ / heterossexuais"), fontsize=7.5, color=INK)
    bx.tick_params(axis="y", length=0)
    bx.spines["left"].set_visible(False)
    bx.grid(axis="x", color=GRADE, lw=0.5); bx.set_axisbelow(True)
    fig.text(0.56, 0.96, T("b"), fontsize=10, fontweight="bold", color=INK, va="top")
    return fig, {}


# ================================================================ Figura 4
def fig4():
    d = ler_d100()
    anos = sorted(d)
    xm = {a: a + 0.5 for a in anos}
    fig = plt.figure(figsize=(7.2, 6.7))
    a = fig.add_axes([0.11, 0.545, 0.86, 0.385])
    b = fig.add_axes([0.11, 0.09, 0.86, 0.34])
    cor_u = {"linhas": PALETA["ref"], "denuncias": PALETA["estat"]}
    seg_a = [x for x in anos if x <= 2019]
    seg_c = [x for x in anos if x >= 2021]
    a.plot([xm[x] for x in seg_a], [d[x]["lgbt"] for x in seg_a], "-o", color=cor_u["linhas"], lw=2.2, ms=5)
    a.plot([xm[2020]], [d[2020]["lgbt"]], "D", color=cor_u["linhas"], mfc="white", mew=1.8, ms=7)
    a.plot([xm[x] for x in seg_c], [d[x]["lgbt"] for x in seg_c], "-o", color=cor_u["denuncias"], lw=2.4, ms=5.5)
    a.plot([xm[2026]], [d[2026]["lgbt"]], "o", color=cor_u["denuncias"], mfc="white", mew=2, ms=7)
    for xq, rot in D100_QUEBRAS:
        a.axvline(xq, color=INK2, lw=1, ls=":")
        a.text(xq - 0.07, 14850, T(rot), rotation=90, ha="right", va="top", fontsize=MIN_PT, color=INK)
    a.set_xlim(2010.6, 2027.3), a.set_ylim(0, 15000)
    a.set_xticks([xm[x] for x in anos], [str(x) if x < 2026 else "2026*" for x in anos], fontsize=MIN_PT)
    a.tick_params(axis="y", labelsize=MIN_PT)
    a.set_yticks(range(0, 13001, 2000), [miles(v) for v in range(0, 13001, 2000)])
    a.set_ylabel(T("Registros do módulo LGBT por ano"), fontsize=MIN_PT + 0.3)
    a.grid(axis="y", color=GRADE, lw=0.6), a.set_axisbelow(True)
    for ano, dy, ha_ in ((2011, -850, "center"), (2012, 380, "center"), (2019, -820, "center")):
        a.text(xm[ano], d[ano]["lgbt"] + dy, miles(d[ano]["lgbt"]), ha=ha_, fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2021] - 0.25, d[2021]["lgbt"] + 350, miles(d[2021]["lgbt"]), ha="right", va="bottom", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2025] - 0.3, d[2025]["lgbt"] + 350, miles(d[2025]["lgbt"]), ha="right", va="bottom", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(xm[2020], d[2020]["lgbt"] + 650, f"{miles(d[2020]['lgbt'])}\n{T('(2 formatos)')}", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold", linespacing=1.1, bbox={"fc": "white", "ec": "none", "pad": 1.0})
    a.text(xm[2026] - 0.1, d[2026]["lgbt"] + 560, f"{miles(d[2026]['lgbt'])}\n{T('até setembro')}", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold")
    a.text(2013.1, 6900, T("2011-2019: linhas do arquivo\n(vítima x suspeito, sem chave de pessoa)"), fontsize=MIN_PT + 0.2, color=PALETA["ref"], ha="left", va="bottom", linespacing=1.15)
    a.text(2027.2, 250, T("2021-2026: denúncias\ncom ao menos uma linha\nno módulo LGBT"), fontsize=MIN_PT + 0.2, color=PALETA["estat"], ha="right", va="bottom", linespacing=1.15, fontweight="bold", bbox={"fc": "white", "ec": "none", "pad": 1.0})
    a.set_title(T("(a) O módulo LGBT em cada ano: a unidade e o formato mudam ao longo da série"), loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.1)
    alt = [d[x]["canal"] for x in anos]
    cores = [cor_u[d[x]["unidade"]] for x in anos]
    barras = b.bar([xm[x] for x in anos], [v / 1000 for v in alt], width=0.72, color=[PALETA["estat_cl"] if d[x]["unidade"] == "denuncias" else "white" for x in anos],
                   edgecolor=cores, linewidth=1.6)
    for p_, x in zip(barras, anos):
        if x == 2026:
            p_.set_hatch("///"), p_.set_edgecolor(PALETA["estat"])
    for x, p_ in zip(anos, barras):
        pc = 100 * d[x]["lgbt"] / d[x]["canal"]
        b.text(p_.get_x() + p_.get_width() / 2, p_.get_height() + 12, f"{br(pc, 1)}%", ha="center", fontsize=MIN_PT, color=INK, fontweight="bold")
    b.set_xlim(2010.6, 2027.3), b.set_ylim(0, 760)
    b.set_xticks([xm[x] for x in anos], [str(x) if x < 2026 else "2026*" for x in anos], fontsize=MIN_PT)
    b.tick_params(axis="y", labelsize=MIN_PT)
    b.set_ylabel(T("Registros do canal inteiro\n(milhares)"), fontsize=MIN_PT + 0.3)
    b.grid(axis="y", color=GRADE, lw=0.6), b.set_axisbelow(True)
    b.axvline(2021.0, color=INK2, lw=1, ls=":")
    b.text(2020.9, 735, T("unidade: linhas"), ha="right", va="top", fontsize=MIN_PT, color=INK2)
    b.text(2021.1, 735, T("unidade: denúncias"), ha="left", va="top", fontsize=MIN_PT, color=PALETA["estat"])
    b.set_title(T("(b) O canal inteiro cresce; em cima de cada barra, a parte do módulo LGBT"), loc="left", fontsize=9.5, fontweight="bold", color=INK, x=-0.1)
    return fig, {}


# ================================================================ Figura 8
POSSES = [(2003, "Lula"), (2011, "Dilma"), (2016.37, "Temer"), (2019, "Bolsonaro"), (2023, "Lula")]


def series() -> dict:
    s = {}
    asr = ler_p(REPO / "data/sim/asr_brasil.csv")
    s["hom"] = {int(r["ano"]): float(r["taxa_padronizada"]) for r in asr if r["grupo"] == "Brasil" and r["desfecho"] == "agressao"}
    s["hom_ind"] = {int(r["ano"]): float(r["taxa_padronizada"]) for r in asr if r["grupo"] == "Brasil" and r["desfecho"] == "agressao+indet"}
    ggb = {}
    for r in ler_p(REPO / "analysis/ggb-series/series/painel_mortes_lgbt.csv"):
        if r["fonte"].startswith("ggb") and r["categoria"] == "total" and r["ano"] == r["ano_fim"] and r["valor"]:
            ggb[int(r["ano"])] = float(r["valor"])
    s["ggb"] = ggb
    d100 = ler_p(REPO / "data/disque100/saidas/d100_serie_anual.csv")
    s["d100_linhas"] = {int(r["ano"]): float(r["n"]) for r in d100 if r["recorte"] == "grupo_lgbt" and r["unidade"] == "linhas" and int(r["ano"]) <= 2019}
    s["d100_den"] = {int(r["ano"]): float(r["n"]) for r in d100 if r["recorte"] == "grupo_lgbt" and r["unidade"] == "denuncias" and 2021 <= int(r["ano"]) <= 2025}
    s["sinan"] = {int(r["ano"]): float(r["m_lgbtfobia"]) for r in ler_p(REPO / "data/sinan/serie_campo55_uf_ano.csv") if r["uf"] == "BR"}
    bo = {}
    for r in sorted((r for r in ler_p(REPO / "data/anuario/anuario_lgbtfobia_uf_ano_v2.csv") if r["uf"] == "BR" and r["marca"] == "valor"), key=lambda r: int(r["edicao"])):
        bo[int(r["ano_dado"])] = float(r["registros"])
    s["bo"] = bo
    return s


def posses(ax, rotulo=False):
    for x, nome in POSSES:
        ax.axvline(x, color=INK2, lw=0.6, ls=(0, (2, 2)), zorder=0)
        if rotulo:
            ax.text(x + 0.15, 1.0, T(nome), transform=ax.get_xaxis_transform(), fontsize=7, color=INK2, va="bottom")


def linha(ax, d, **kw):
    xs = sorted(d); ax.plot(xs, [d[x] for x in xs], marker="o", ms=2.8, lw=1.6, **kw)


def fig8():
    s = series()
    fig, axs = plt.subplots(5, 1, figsize=(6.6, 8.6), dpi=300, sharex=True)
    ax = axs[0]
    linha(ax, s["hom"], color=INK, label=T("agressão"))
    linha(ax, s["hom_ind"], color=INK2, ls=(0, (3, 2)), label=T("agressão + causa indeterminada"))
    ax.set_ylabel(T("por 100 mil"), fontsize=7.5)
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.set_title(T("a  Homicídio de toda a população (taxa padronizada; único painel que não é registro LGBT+)"), loc="left", fontsize=8, color=INK, pad=14)
    painéis = [("b  Lista do GGB: mortes noticiadas na imprensa (contagem da organização)", [("ggb", {})]),
               ("c  Disque 100, módulo LGBT: linhas até 2019 e denúncias desde 2021 (unidades diferentes)",
                [("d100_linhas", {"color": INK2}), ("d100_den", {})]),
               ("d  Fichas do SUS com motivo marcado como LGBTfobia", [("sinan", {})]),
               ("e  Boletins de ocorrência por homofobia ou transfobia (Anuário)", [("bo", {})])]
    for ax, (tit, ss) in zip(axs[1:], painéis):
        for k, kw in ss:
            linha(ax, s[k], **({"color": ESTAT} | kw))
        ax.set_title(T(tit), loc="left", fontsize=8, color=INK)
        ax.set_ylabel(T("registros"), fontsize=7.5)
    for i, ax in enumerate(axs):
        posses(ax, rotulo=(i == 0))
        ax.grid(axis="y", color=GRADE, lw=0.5); ax.set_axisbelow(True)
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: miles(v)))
    axs[-1].set_xlim(1999.5, 2026.5)
    axs[-1].set_xticks(range(2000, 2027, 2))
    fig.align_ylabels(axs)
    fig.tight_layout(h_pad=1.0)
    return fig, {}


FIGURAS = [("fig_v05_01_caminho", fig1, (9, None)), ("fig_v05_02_pns", fig2, (8, None)),
           ("fig_v05_03_agressor", fig3, (9, None)), ("fig_v05_04_disque100", fig4, (9, INK)),
           ("fig_v05_08_governos_series", fig8, (8, None))]
FIGURAS[0] = ("fig_v05_01_caminho", fig1, (9, INK))

# ---------------------------------------------------------------- conferencia do texto em ingles
PT_PALAVRAS = {"não", "nao", "que", "para", "uma", "com", "dos", "das", "pela", "pelo", "por", "sem", "mais", "quem", "ficha", "fichas",
               "pessoa", "polícia", "policia", "morre", "vira", "notícia", "matéria", "denúncia", "denuncia", "ou", "ao", "aos",
               "são", "os", "um", "uns", "linhas", "registros", "razão", "razao", "bruta", "ajustada", "mortes", "onde",
               "do", "da", "na", "em", "de", "dois", "grupos", "anotou", "ninguém", "agressão", "até", "desde", "cada", "ano"}
ACENTOS = re.compile(r"[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]")


def conferir_en(fig, nome):
    fig.canvas.draw()
    erros = []
    for t in fig.findobj(mtext.Text):
        s = t.get_text()
        if not s or not t.get_visible():
            continue
        if ACENTOS.search(s):
            erros.append(f"acento: {s!r}")
        for w in re.findall(r"[A-Za-zÀ-ÿ]+", s):
            if w in PT_PALAVRAS:
                erros.append(f"palavra pt {w!r}: {s!r}")
    if erros:
        raise SystemExit(f"ERRO ({nome}, en): texto com portugues: " + "; ".join(sorted(set(erros))))


PT_SO = re.compile(r"[ãõçâêôÃÕÇÂÊÔ]")
PT_SO_PALAVRAS = {"não", "são", "com", "sem", "pela", "pelo", "ao", "aos", "ou", "em", "um", "uns", "uma", "ninguém", "até", "quem",
                  "morre", "vira", "notícia", "matéria", "denúncia", "razão", "mortes", "anotou", "linhas", "pessoas", "polícia"}
LATINAS_HE: set = set()


def conferir_traducao(fig, nome):
    """es/it: nenhum acento ou palavra SO do portugues (texto que escapou de T()); he: junta as palavras latinas para revisao."""
    fig.canvas.draw()
    erros = []
    for t in fig.findobj(mtext.Text):
        s = t.get_text()
        if not s or not t.get_visible():
            continue
        if LANG == "he":
            LATINAS_HE.update(re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ+]*", s))
        elif PT_SO.search(s) or set(re.findall(r"[^\W\d_]+", s.lower())) & PT_SO_PALAVRAS:
            erros.append(repr(s))
    if erros:
        raise SystemExit(f"ERRO ({nome}, {LANG}): texto com portugues: " + "; ".join(sorted(set(erros))))


def main() -> None:
    global LANG, TAB
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=["pt-BR", "en", "es", "it", "he"])
    ap.add_argument("--saida", default=str(SAIDA_BASE), help="pasta de saida (padrao: <raiz>/.run/figuras-artigo)")
    args = ap.parse_args()
    LANG = args.lang
    if LANG == "he":   # regras do hebraico num modulo so, comum aos dois roteiros (bidi_he.py)
        import importlib.util            # -I nao poe a pasta do roteiro no caminho de import
        sp = importlib.util.spec_from_file_location("bidi_he", Path(__file__).resolve().parent / "bidi_he.py")
        bidi_he = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(bidi_he)
        bidi_he.instalar()
    if LANG in ("es", "it", "he"):
        TAB = json.loads((Path(__file__).resolve().parent / "rotulos" / f"{LANG}.json").read_text(encoding="utf-8"))["v05"]
    plt.rcdefaults()
    plt.rcParams.update({"svg.fonttype": "path", "savefig.transparent": True, "pdf.fonttype": 42,
                         "svg.hashsalt": "lgbt-indicador-paper-v05"})
    saida = Path(args.saida) / LANG
    saida.mkdir(parents=True, exist_ok=True)
    for nome, fn, (tam, lc) in FIGURAS:
        with rc(tam, lc):
            fig, kw = fn()
            if LANG == "en":
                conferir_en(fig, nome)
            elif LANG != "pt-BR":
                conferir_traducao(fig, nome)
            fig.savefig(saida / f"{nome}.svg", metadata={"Date": None, "Creator": "make_figuras_v05"}, **kw)
            fig.savefig(saida / f"{nome}.pdf", metadata={"CreationDate": None, "ModDate": None, "Creator": "make_figuras_v05"}, **kw)
        plt.close(fig)
        print(saida / f"{nome}.svg")
    if LATINAS_HE:
        print(f"[he] palavras latinas desenhadas (revisar a olho): {sorted(LATINAS_HE)}")


if __name__ == "__main__":
    main()
