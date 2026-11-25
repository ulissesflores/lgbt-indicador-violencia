# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Draw the README artwork as code: banner, icon and finding cards in five languages.

The script draws, with matplotlib, the SVG banners, the four-finding cards and the results
figures for each README language (en, pt-BR, es, it, he; Hebrew mirrored right to left) in a
light and a dark theme, plus the project icon. It derives the dark laboratory lockup PNG from
the light one. Every number printed on the cards is read from a data file of the repository.

Inputs
------
- data/pns/seguro_pns2019.csv (PNS 2019 prevalences and adjusted ratio)
- analysis/ggb-audit/dados/codificacao_A.csv (stages of the 2019 list sample)
- analysis/simulation/resumo.json (registered counts and simulated incidence scenarios)
- assets/brand/lab-lockup-light.png (original laboratory mark)

Outputs
-------
- assets/brand/banner-<language>-<light|dark>.svg
- assets/brand/findings-<language>-<light|dark>.svg
- assets/brand/results-<language>-<light|dark>.svg
- assets/brand/lab-lockup-dark.png and assets/brand/icon.svg
- prints the number of figures written

Usage
-----
python3 -I assets/brand/make_brand.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Arte do README desenhada por código: banner, ícone e cartões de achado, em 5 idiomas.

Mapa de afirmações (nenhuma figura sem afirmação)
--------------------------------------------------
- ``icon.svg`` e o ícone do banner: quatro colunas de fonte pública; a quarta, tracejada e
  vazia, é a taxa nacional de mortalidade LGBT+ que o registro de óbito não permite calcular.
  Não é marca do laboratório.
- ``lab-lockup-{light,dark}.png``: a marca do Codex Hash Research Laboratory. A clara é o
  arquivo original do laboratório, sem alteração; a escura é derivada dela aqui (cor do traço
  invertida, transparência mantida). Marca, não figura: fica fora da CC BY 4.0 (ver NOTICE).
- ``banner-<idioma>-{light,dark}.svg``: título e tese do artigo, "o que o dado público permite
  afirmar".
- ``findings-<idioma>-{light,dark}.svg``: os quatro achados do Resumo, cada número lido do
  arquivo que o produziu (``dados()``) e travado em ``tests/test_readme_arte.py``:
  (a) PNS 2019, violência física em 12 meses: 14,70% LGB+ x 3,82% heterossexuais, razão
  ajustada 2,82 (2,16 a 3,68) <- ``data/pns/seguro_pns2019.csv``;
  (b) SIM: sem orientação sexual nem identidade de gênero no óbito, não há taxa nacional
  (afirmação sem número);
  (c) lista do Grupo Gay da Bahia, amostra de 2019: 160 -> 106 -> 88 -> 74 -> 50
  <- ``analysis/ggb-audit/dados/codificacao_A.csv``;
  (d) boletins de "racismo por homofobia ou transfobia": 783 -> 3.481 (2022 a 2025), três
  trajetórias de incidência com o mesmo erro <- ``analysis/simulation/resumo.json``.
  O painel de governadores fica fora da arte: é comparação exploratória.
- ``results-<idioma>-{light,dark}.svg``: figura da seção Results, violência física, sexual e
  psicológica em 12 meses, LGB+ x heterossexuais (PNS 2019: 14,70 x 3,82; 4,86 x 0,68;
  40,03 x 16,73) <- ``data/pns/seguro_pns2019.csv`` (bloco ``nivel``); travada no mesmo teste.

Cada README usa as peças do seu idioma (``en``, ``pt-BR``, ``es``, ``it``, ``he``); os números
saem no formato da língua e o hebraico é desenhado espelhado, da direita para a esquerda (a
ordem bidirecional do texto exige matplotlib 3.11 ou mais novo, que traz a libraqm). O texto
vira contorno (``svg.fonttype = path``) e o ``svg.hashsalt`` é fixo, para o SVG não depender de
fonte instalada nem mudar entre execuções.

Uso
---
    python3 -I assets/brand/make_brand.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import csv
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.ft2font  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parent
RAIZ = OUT.parents[1]
TEMAS = {
    "light": {
        "bg": "#F6F8FA",
        "ink": "#0B1B2B",
        "muted": "#57606A",
        "line": "#D0D7DE",
        "card": "#FFFFFF",
        "accent": "#8250DF",
        "accent2": "#0F766E",
        "warn": "#B35900",
    },
    "dark": {
        "bg": "#0D1117",
        "ink": "#E6EDF3",
        "muted": "#9BA7B4",
        "line": "#30363D",
        "card": "#161B22",
        "accent": "#B392F0",
        "accent2": "#2DD4BF",
        "warn": "#F0883E",
    },
}
plt.rcParams.update(
    {"font.family": "DejaVu Sans", "svg.fonttype": "path", "svg.hashsalt": "lgbt-indicador"}
)

# Textos de cada idioma. Campos entre chaves recebem os números de dados(), já formatados.
# "dec" é o separador decimal da língua (o de milhar é o outro); "rtl" espelha o desenho.
# LRM (U+200E) depois de "LGB+" mantém o "+" colado à sigla dentro do texto hebraico, e em
# volta do travessão impede que o intervalo de anos se inverta.
_LRM = "‎"
TEXTOS = {
    "en": {
        "dec": ".",
        "rtl": False,
        "banner": (
            "What public data allow us to claim",
            "Mortality and violence against LGBT+ people in Brazil",
            "An audit of sources and indicators, 2010–2026",
            "Pre-registered · the same yardstick for both sides · SHA-256 sealed",
        ),
        "pns_rotulo": "2019 NATIONAL HEALTH SURVEY (PNS)",
        "pns_titulo": "Physical violence, past 12 months",
        "pns_grupos": ("LGB+ adults", "Heterosexual adults"),
        "pns_razao": "Adjusted ratio {rp} (95% interval {lo} to {hi})",
        "sim_rotulo": "DEATH RECORDS (SIM)",
        "sim_titulo": "No national LGBT+ mortality rate",
        "sim_texto": (
            "Death certificates record neither",
            "sexual orientation nor gender",
            "identity.",
        ),
        "sim_aviso": ("The rate cannot be estimated,", "in either direction."),
        "ggb_rotulo": "GRUPO GAY DA BAHIA LIST, 2019 SAMPLE",
        "ggb_titulo": "Cases checked against the cited source",
        "ggb_etapas": (
            "sampled",
            "source found",
            "source matches",
            "violent death",
            "LGBT+ victim",
        ),
        "ggb_rodape": "{n} of {n0} confirmed ({pct}%). Not a rate, not a total.",
        "bo_rotulo": "POLICE REPORTS, FBSP YEARBOOK",
        "bo_titulo": "Records of homophobia or transphobia",
        "bo_texto": (
            "The same series fits with the",
            "same error if violence was",
            "flat, +{sobe}% or −{cai}% a year.",
        ),
        "bo_aviso": "Records, not incidence.",
        "res_titulo": "Violence reported in the past 12 months, by type",
        "res_tipos": ("Physical", "Sexual", "Psychological"),
        "res_grupos": ("LGB+", "Heterosexual"),
        "res_rodape": "Share of adults, survey-weighted. The survey does not ask about the "
        "perpetrator's motive and does not identify trans people.",
    },
    "pt-BR": {
        "dec": ",",
        "rtl": False,
        "banner": (
            "O que os dados públicos permitem afirmar",
            "Mortalidade e violência contra pessoas LGBT+ no Brasil",
            "Uma auditoria de fontes e indicadores, 2010–2026",
            "Pré-registrado · a mesma régua para os dois lados · selado com SHA-256",
        ),
        "pns_rotulo": "PESQUISA NACIONAL DE SAÚDE (PNS) 2019",
        "pns_titulo": "Violência física nos últimos 12 meses",
        "pns_grupos": ("Adultos LGB+", "Adultos heterossexuais"),
        "pns_razao": "Razão ajustada {rp} (intervalo de 95%: {lo} a {hi})",
        "sim_rotulo": "REGISTROS DE ÓBITO (SIM)",
        "sim_titulo": "Não há taxa nacional de mortalidade LGBT+",
        "sim_texto": (
            "A declaração de óbito não registra",
            "orientação sexual nem identidade",
            "de gênero.",
        ),
        "sim_aviso": ("A taxa não pode ser estimada,", "nem para mais, nem para menos."),
        "ggb_rotulo": "LISTA DO GRUPO GAY DA BAHIA, AMOSTRA DE 2019",
        "ggb_titulo": "Casos conferidos na fonte citada",
        "ggb_etapas": (
            "sorteados",
            "fonte encontrada",
            "fonte confere",
            "morte violenta",
            "vítima LGBT+",
        ),
        "ggb_rodape": "{n} de {n0} confirmados ({pct}%). Não é taxa nem total.",
        "bo_rotulo": "BOLETINS DE OCORRÊNCIA, ANUÁRIO DO FBSP",
        "bo_titulo": "Registros de homofobia ou transfobia",
        "bo_texto": (
            "A mesma série se ajusta,",
            "com o mesmo erro, a uma",
            "violência parada, +{sobe}%",
            "ou −{cai}% ao ano.",
        ),
        "bo_aviso": "Registros, não incidência.",
        "res_titulo": "Violência relatada nos últimos 12 meses, por tipo",
        "res_tipos": ("Física", "Sexual", "Psicológica"),
        "res_grupos": ("LGB+", "Heterossexuais"),
        "res_rodape": "Proporção de adultos, com peso amostral. A pesquisa não pergunta o "
        "motivo do agressor e não identifica pessoas trans.",
    },
    "es": {
        "dec": ",",
        "rtl": False,
        "banner": (
            "Lo que los datos públicos permiten afirmar",
            "Mortalidad y violencia contra personas LGBT+ en Brasil",
            "Una auditoría de fuentes e indicadores, 2010–2026",
            "Prerregistrado · la misma vara de medir para ambos lados · sellado con SHA-256",
        ),
        "pns_rotulo": "ENCUESTA NACIONAL DE SALUD (PNS) 2019",
        "pns_titulo": "Violencia física en los últimos 12 meses",
        "pns_grupos": ("Adultos LGB+", "Adultos heterosexuales"),
        "pns_razao": "Razón ajustada {rp} (intervalo del 95%: {lo} a {hi})",
        "sim_rotulo": "REGISTROS DE DEFUNCIÓN (SIM)",
        "sim_titulo": "No hay tasa nacional de mortalidad LGBT+",
        "sim_texto": (
            "El certificado de defunción no",
            "registra ni la orientación sexual",
            "ni la identidad de género.",
        ),
        "sim_aviso": ("La tasa no puede estimarse,", "ni al alza ni a la baja."),
        "ggb_rotulo": "LISTA DEL GRUPO GAY DA BAHIA, MUESTRA DE 2019",
        "ggb_titulo": "Casos cotejados con la fuente citada",
        "ggb_etapas": (
            "sorteados",
            "fuente encontrada",
            "fuente coincide",
            "muerte violenta",
            "víctima LGBT+",
        ),
        "ggb_rodape": "{n} de {n0} confirmados ({pct}%). No es una tasa ni un total.",
        "bo_rotulo": "DENUNCIAS POLICIALES, ANUARIO DEL FBSP",
        "bo_titulo": "Registros de homofobia o transfobia",
        "bo_texto": (
            "La misma serie encaja, con",
            "el mismo error, con una",
            "violencia estable, +{sobe}%",
            "o −{cai}% al año.",
        ),
        "bo_aviso": "Registros, no incidencia.",
        "res_titulo": "Violencia declarada en los últimos 12 meses, por tipo",
        "res_tipos": ("Física", "Sexual", "Psicológica"),
        "res_grupos": ("LGB+", "Heterosexuales"),
        "res_rodape": "Proporción de adultos, con ponderación muestral. La encuesta no pregunta "
        "el motivo del agresor ni identifica a las personas trans.",
    },
    "it": {
        "dec": ",",
        "rtl": False,
        "banner": (
            "Che cosa i dati pubblici consentono di affermare",
            "Mortalità e violenza contro le persone LGBT+ in Brasile",
            "Un audit delle fonti e degli indicatori, 2010–2026",
            "Preregistrato · lo stesso metro per entrambe le parti · sigillato con SHA-256",
        ),
        "pns_rotulo": "INDAGINE NAZIONALE SULLA SALUTE (PNS) 2019",
        "pns_titulo": "Violenza fisica negli ultimi 12 mesi",
        "pns_grupos": ("Adulti LGB+", "Adulti eterosessuali"),
        "pns_razao": "Rapporto aggiustato {rp} (intervallo al 95%: da {lo} a {hi})",
        "sim_rotulo": "REGISTRI DI MORTE (SIM)",
        "sim_titulo": "Nessun tasso nazionale di mortalità LGBT+",
        "sim_texto": (
            "Il certificato di morte non",
            "registra né l'orientamento",
            "sessuale né l'identità di genere.",
        ),
        "sim_aviso": ("Il tasso non si può stimare,", "né per eccesso né per difetto."),
        "ggb_rotulo": "LISTA DEL GRUPO GAY DA BAHIA, CAMPIONE DEL 2019",
        "ggb_titulo": "Casi verificati sulla fonte citata",
        "ggb_etapas": (
            "campionati",
            "fonte trovata",
            "fonte corrisponde",
            "morte violenta",
            "vittima LGBT+",
        ),
        "ggb_rodape": "{n} su {n0} confermati ({pct}%). Non è un tasso né un totale.",
        "bo_rotulo": "DENUNCE ALLA POLIZIA, ANNUARIO FBSP",
        "bo_titulo": "Registrazioni di omofobia o transfobia",
        "bo_texto": (
            "La stessa serie si adatta,",
            "con lo stesso errore, a una",
            "violenza stabile, +{sobe}%",
            "o −{cai}% l'anno.",
        ),
        "bo_aviso": "Registrazioni, non incidenza.",
        "res_titulo": "Violenza dichiarata negli ultimi 12 mesi, per tipo",
        "res_tipos": ("Fisica", "Sessuale", "Psicologica"),
        "res_grupos": ("LGB+", "Eterosessuali"),
        "res_rodape": "Quota di adulti, con pesi campionari. L'indagine non chiede il movente "
        "dell'aggressore e non identifica le persone trans.",
    },
    "he": {
        "dec": ".",
        "rtl": True,
        "banner": (
            "מה הנתונים הציבוריים מאפשרים לנו לטעון",
            "תמותה ואלימות כלפי אנשים להט״ב+ בברזיל",
            "ביקורת של מקורות ומדדים, 2010" + _LRM + "–" + _LRM + "2026",  # sem LRM vira 2026–2010
            "רישום מוקדם · אותה מידה לשני הצדדים · חתום ב־SHA-256",
        ),
        "pns_rotulo": "סקר הבריאות הלאומי (PNS) 2019",
        "pns_titulo": "אלימות פיזית ב־12 החודשים האחרונים",
        "pns_grupos": (f"מבוגרים LGB+{_LRM}", "מבוגרים הטרוסקסואלים"),
        "pns_razao": "יחס מתוקן {rp} (רווח של 95%: {lo} עד {hi})",
        "sim_rotulo": "רישומי פטירה (SIM)",
        "sim_titulo": "אין שיעור תמותה לאומי של להט״ב+",
        "sim_texto": (
            "תעודת הפטירה אינה רושמת",
            "לא נטייה מינית ולא זהות",
            "מגדרית.",
        ),
        "sim_aviso": ("אי אפשר לאמוד את השיעור,", "לא כלפי מעלה ולא כלפי מטה."),
        "ggb_rotulo": "רשימת Grupo Gay da Bahia, מדגם 2019",
        "ggb_titulo": "מקרים שנבדקו מול המקור המצוטט",
        "ggb_etapas": ("נדגמו", "המקור נמצא", "המקור תואם", "מוות אלים", "קורבן להט״ב+"),
        "ggb_rodape": "{n} מתוך {n0} אושרו ({pct}%). לא שיעור ולא סך כולל.",
        "bo_rotulo": "תלונות במשטרה, השנתון של FBSP",
        "bo_titulo": "רישומים של הומופוביה או טרנספוביה",
        # בעברית בלי סימן לפני המספר: "עולה ב־15%" במקום "+15%", כדי שהסימן לא יתהפך
        "bo_texto": (
            "אותה סדרה מתאימה, באותה",
            "שגיאה, לאלימות יציבה,",
            "עולה ב־{sobe}% או יורדת",
            "ב־{cai}% בשנה.",
        ),
        "bo_aviso": "רישומים, לא שכיחות.",
        "res_titulo": "אלימות שדווחה ב־12 החודשים האחרונים, לפי סוג",
        "res_tipos": ("פיזית", "מינית", "פסיכולוגית"),
        "res_grupos": (f"LGB+{_LRM}", "הטרוסקסואלים"),
        "res_rodape": "שיעור המבוגרים, בשקלול המדגם. הסקר אינו שואל על מניע התוקף ואינו "
        "מזהה אנשים טרנסים.",
    },
}


def numero(v, casas, lingua):
    """Formata um número no padrão da língua (decimal e milhar).

    Parameters
    ----------
    v : float or int or Decimal
        Valor.
    casas : int
        Casas decimais.
    lingua : dict
        Entrada de ``TEXTOS``.

    Returns
    -------
    str
        ``3,481`` e ``14.70`` em inglês e hebraico; ``3.481`` e ``14,70`` nas outras.
    """
    s = f"{v:,.{casas}f}"
    return s.translate(str.maketrans(",.", ".,")) if lingua["dec"] == "," else s


def dados():
    """Lê dos arquivos selados os números que a arte mostra.

    Returns
    -------
    dict
        ``pns`` (prevalências em %, razão ajustada e intervalo), ``tipos`` (prevalência LGB+ e
        heterossexual em % por tipo de violência), ``ggb`` (as cinco etapas da amostra de 2019) e
        ``bo`` (boletins por ano e as três taxas de incidência simuladas).
    """
    with open(RAIZ / "data/pns/seguro_pns2019.csv", encoding="utf-8", newline="") as fh:
        pns = {(r["bloco"], r["rotulo"], r["grupo"]): r for r in csv.DictReader(fh)}
    nivel, aj = pns[("nivel", "física", "LGB+")], pns[("rp_ajustada", "física", "LGB+")]
    with open(
        RAIZ / "analysis/ggb-audit/dados/codificacao_A.csv", encoding="utf-8", newline=""
    ) as fh:
        cod = list(csv.DictReader(fh))
    rec = [r for r in cod if r["fonte"] == "R"]
    corr = [r for r in rec if r["corresp"] in ("S", "P")]
    mv = [r for r in corr if r["morte"] == "S"]
    estr = [r for r in mv if r["lgbt"] == "S"]
    sim = json.loads((RAIZ / "analysis/simulation/resumo.json").read_text(encoding="utf-8"))
    return {
        "pns": {
            "lgb": 100 * float(nivel["prev_grupo"]),
            "het": 100 * float(nivel["prev_ref"]),
            "rp": float(aj["rp"]),
            "ic": (float(aj["ic_lo"]), float(aj["ic_hi"])),
        },
        "tipos": {
            rot: (
                100 * float(pns[("nivel", rot, "LGB+")]["prev_grupo"]),
                100 * float(pns[("nivel", rot, "LGB+")]["prev_ref"]),
            )
            for rot in ("física", "sexual", "psicológica")
        },
        "ggb": [len(cod), len(rec), len(corr), len(mv), len(estr)],
        "bo": {int(ano): int(n) for ano, n in sim["observado"].items()},
        "g": sorted(c["g"] for c in sim["cenarios"].values()),
    }


def caixa(ax, x, y, w, h, fc, ec="none", lw=0.0, r=6, **kw):
    """Desenha um retângulo de cantos arredondados.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Eixos de destino.
    x, y, w, h : float
        Canto inferior esquerdo, largura e altura.
    fc, ec : str
        Cores de preenchimento e de borda.
    lw : float
        Espessura da borda.
    r : float
        Raio dos cantos.
    **kw
        Repassado a ``FancyBboxPatch`` (ex.: ``linestyle``).
    """
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, **kw
        )
    )


class Tela:
    """Figura cujos eixos cobrem a tela inteira, em pontos, desenhada da esquerda ou da direita.

    Todo o desenho passa por ``texto`` e ``caixa``: com ``rtl`` verdadeiro, a coordenada x é
    espelhada (``x -> largura - x``) e o alinhamento horizontal inverte, de modo que o mesmo
    código de layout serve ao hebraico.

    Parameters
    ----------
    largura, altura : int
        Tamanho em pontos (uma unidade = um ponto, a mesma escala das fontes).
    cor : str
        Cor de fundo.
    rtl : bool
        Desenhar espelhado, da direita para a esquerda.
    """

    def __init__(self, largura, altura, cor, rtl=False):
        self.fig = plt.figure(figsize=(largura / 72, altura / 72), facecolor=cor)
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_xlim(0, largura)
        self.ax.set_ylim(0, altura)
        self.ax.axis("off")
        self.largura, self.rtl = largura, rtl

    def ordem(self, i, n):
        """Posição da i-ésima de ``n`` peças de uma fila que NÃO deve inverter (ícone, anos).

        O espelho inverte a fila; aqui ela é invertida antes, para sair na ordem original.
        """
        return n - 1 - i if self.rtl else i

    def caixa(self, x, y, w, h, *a, **kw):
        """Retângulo arredondado (ver ``caixa``), espelhado em ``rtl``."""
        caixa(self.ax, self.largura - x - w if self.rtl else x, y, w, h, *a, **kw)

    def texto(self, x, y, s, maxw=None, ha="left", **kw):
        """Escreve ``s`` em (x, y); se passar de ``maxw`` pontos de largura, reduz a fonte.

        Parameters
        ----------
        x, y : float
            Ponto de ancoragem, na orientação da esquerda para a direita.
        s : str
            Texto.
        maxw : float, optional
            Largura máxima em pontos; as traduções variam de tamanho e não podem vazar do cartão.
        ha : str
            Alinhamento horizontal (``left``, ``right`` ou ``center``), invertido em ``rtl``.
        **kw
            Repassado a ``Axes.text``.
        """
        if self.rtl:
            x, ha = self.largura - x, {"left": "right", "right": "left"}.get(ha, ha)
        t = self.ax.text(x, y, s, ha=ha, **kw)
        if maxw:
            r = self.fig.canvas.get_renderer()
            w = t.get_window_extent(r).width * 72 / self.fig.dpi
            if w > maxw:
                t.set_fontsize(t.get_fontsize() * maxw / w * 0.98)
                print(f"  fonte x{maxw / w * 0.98:.2f}: {s}")  # para olhar a peça

    def salvar(self, nome, cor):
        """Grava o SVG em ``OUT`` sem data no metadado e fecha a figura."""
        self.fig.savefig(OUT / nome, facecolor=cor, metadata={"Date": None})
        plt.close(self.fig)


def icone(tl, x, y, s, t):
    """Desenha o ícone: três colunas cheias e a quarta tracejada e vazia (marca: não espelha).

    Parameters
    ----------
    tl : Tela
        Tela de destino.
    x, y : float
        Canto inferior esquerdo.
    s : float
        Lado do quadrado.
    t : dict
        Cores do tema.
    """
    tl.caixa(x, y, s, s, t["card"], t["line"], 1.5, r=s * 0.18)
    w, gap, base = s * 0.13, s * 0.06, y + s * 0.18
    for i, h in enumerate((0.38, 0.56, 0.46)):
        cor = (t["accent"], t["accent2"], t["accent"])[i]
        tl.caixa(x + s * 0.16 + tl.ordem(i, 4) * (w + gap), base, w, s * h, cor, r=s * 0.03)
    tl.caixa(
        x + s * 0.16 + tl.ordem(3, 4) * (w + gap),
        base,
        w,
        s * 0.64,
        "none",
        t["warn"],
        1.6,
        r=s * 0.03,
        linestyle=(0, (3, 2)),
    )


def banner(lg, tema, t):
    """Desenha o banner do README para um idioma e um tema.

    Parameters
    ----------
    lg : str
        Código do idioma (chave de ``TEXTOS``).
    tema : str
        Nome do tema (vai no nome do arquivo).
    t : dict
        Cores do tema.
    """
    L = TEXTOS[lg]
    tl = Tela(1280, 300, t["bg"], L["rtl"])
    # do lado oposto ao título, as mesmas quatro colunas do ícone, grandes e apagadas
    for i, h in enumerate((0.38, 0.56, 0.46, 0.64)):
        xx = 1010 + tl.ordem(i, 4) * 62
        if i < 3:
            tl.caixa(xx, 0, 44, 300 * h, t["line"], r=6)
        else:
            tl.caixa(xx, 0, 44, 300 * h, "none", t["warn"], 1.6, r=6, linestyle=(0, (5, 4)))
    icone(tl, 64, 86, 128, t)
    titulo, sub, auditoria, selo = L["banner"]
    tl.texto(232, 186, titulo, 760, color=t["ink"], fontsize=38, fontweight="bold")
    tl.texto(232, 140, sub, 760, color=t["ink"], fontsize=24)
    tl.texto(232, 96, auditoria, 760, color=t["accent"], fontsize=18)
    tl.texto(232, 60, selo, 760, color=t["muted"], fontsize=14)
    tl.salvar(f"banner-{lg}-{tema}.svg", t["bg"])


def cartao(tl, x, y, t, rotulo, titulo):
    """Desenha a moldura de um cartão de achado (600 x 300), com fonte e pergunta.

    Parameters
    ----------
    tl : Tela
        Tela de destino.
    x, y : float
        Canto inferior esquerdo do cartão.
    t : dict
        Cores do tema.
    rotulo, titulo : str
        Fonte em versalete e a pergunta do cartão.
    """
    tl.caixa(x, y, 600, 300, t["card"], t["line"], 1.4, r=14)
    tl.texto(x + 28, y + 262, rotulo, 544, color=t["accent"], fontsize=13, fontweight="bold")
    tl.texto(x + 28, y + 228, titulo, 544, color=t["ink"], fontsize=19, fontweight="bold")


def achados(lg, tema, t, d):
    """Desenha os quatro cartões de achado (2 x 2) para um idioma e um tema.

    Parameters
    ----------
    lg : str
        Código do idioma (chave de ``TEXTOS``).
    tema : str
        Nome do tema (vai no nome do arquivo).
    t : dict
        Cores do tema.
    d : dict
        Saída de ``dados()``.
    """
    L = TEXTOS[lg]
    tl = Tela(1280, 680, t["bg"], L["rtl"])
    # (a) PNS 2019
    x, y = 30, 350
    p = d["pns"]
    cartao(tl, x, y, t, L["pns_rotulo"], L["pns_titulo"])
    for i, (rot, v, cor) in enumerate(
        zip(L["pns_grupos"], (p["lgb"], p["het"]), (t["accent"], t["muted"]), strict=True)
    ):
        yy = y + 150 - i * 62
        tl.texto(x + 28, yy + 30, rot, 544, color=t["ink"], fontsize=15)
        tl.caixa(x + 28, yy, 420, 22, t["line"], r=5)
        tl.caixa(x + 28, yy, 420 * v / 20, 22, cor, r=5)
        tl.texto(
            x + 28 + 420 * v / 20 + 10,
            yy + 4,
            f"{numero(v, 2, L)}%",
            color=t["ink"],
            fontsize=17,
            fontweight="bold",
        )
    razao = L["pns_razao"].format(
        rp=numero(p["rp"], 2, L), lo=numero(p["ic"][0], 2, L), hi=numero(p["ic"][1], 2, L)
    )
    tl.texto(x + 28, y + 30, razao, 544, color=t["muted"], fontsize=14)
    # (b) SIM
    x = 650
    cartao(tl, x, y, t, L["sim_rotulo"], L["sim_titulo"])
    tl.caixa(x + 28, y + 70, 120, 130, "none", t["warn"], 2.0, r=8, linestyle=(0, (5, 4)))
    tl.texto(x + 88, y + 128, "?", color=t["warn"], fontsize=44, fontweight="bold", ha="center")
    for k, linha in enumerate(L["sim_texto"]):
        tl.texto(x + 176, y + 168 - 26 * k, linha, 400, color=t["ink"], fontsize=15)
    for k, linha in enumerate(L["sim_aviso"]):
        tl.texto(
            x + 176, y + 76 - 24 * k, linha, 400, color=t["warn"], fontsize=15, fontweight="bold"
        )
    # (c) lista do GGB
    x, y = 30, 20
    cartao(tl, x, y, t, L["ggb_rotulo"], L["ggb_titulo"])
    n0 = d["ggb"][0]
    for i, (rot, n) in enumerate(zip(L["ggb_etapas"], d["ggb"], strict=True)):
        yy = y + 172 - i * 32
        cor = t["accent2"] if i == len(d["ggb"]) - 1 else t["line"]
        tl.caixa(x + 170, yy, 300 * n / n0, 22, cor, r=4)
        tl.texto(x + 160, yy + 4, rot, 134, color=t["muted"], fontsize=13, ha="right")
        tl.texto(
            x + 178 + 300 * n / n0, yy + 4, f"{n}", color=t["ink"], fontsize=14, fontweight="bold"
        )
    # meio-para-cima, como o artigo (31,25 -> 31,3); o float do Python daria 31,2
    pct = Decimal(100 * d["ggb"][-1]) / Decimal(n0)
    pct = pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    rodape = L["ggb_rodape"].format(n=d["ggb"][-1], n0=n0, pct=numero(pct, 1, L))
    tl.texto(x + 28, y + 14, rodape, 544, color=t["ink"], fontsize=13)
    # (d) boletins de ocorrência
    x = 650
    cartao(tl, x, y, t, L["bo_rotulo"], L["bo_titulo"])
    anos = sorted(d["bo"])
    topo = max(d["bo"].values())
    for i, ano in enumerate(anos):
        n = d["bo"][ano]
        h = 130 * n / topo
        xx = x + 34 + tl.ordem(i, len(anos)) * 78  # o tempo corre da esquerda para a direita
        tl.caixa(xx, y + 58, 56, h, t["accent"], r=4)
        tl.texto(
            xx + 28,
            y + 64 + h,
            numero(n, 0, L),
            color=t["ink"],
            fontsize=13,
            ha="center",
            fontweight="bold",
        )
        tl.texto(xx + 28, y + 36, str(ano), color=t["muted"], fontsize=12, ha="center")
    # as três taxas simuladas, em módulo: o sinal vem do texto de cada língua
    cai, _, sobe = (numero(abs(100 * v), 0, L) for v in d["g"])
    linhas = [s.format(sobe=sobe, cai=cai) for s in L["bo_texto"]]
    for k, linha in enumerate([*linhas, L["bo_aviso"]]):
        aviso = k == len(linhas)
        tl.texto(
            x + 364,
            y + 186 - 26 * k,
            linha,
            222,
            color=t["warn"] if aviso else t["ink"],
            fontsize=14,
            fontweight="bold" if aviso else "normal",
        )
    tl.salvar(f"findings-{lg}-{tema}.svg", t["bg"])


def marca_escura():
    """Deriva ``lab-lockup-dark.png`` do original claro: traço preto vira o ``ink`` escuro."""
    from PIL import Image  # dependência do matplotlib

    clara = Image.open(OUT / "lab-lockup-light.png").convert("RGBA")
    r, g, b = (int(TEMAS["dark"]["ink"][i : i + 2], 16) for i in (1, 3, 5))
    escura = Image.new("RGBA", clara.size, (r, g, b, 0))
    escura.putalpha(clara.getchannel("A"))
    escura.save(OUT / "lab-lockup-dark.png", optimize=True)


def tipos(lg, tema, t, d):
    """Desenha a figura de Results: os três tipos de violência, LGB+ x heterossexuais.

    Parameters
    ----------
    lg : str
        Código do idioma (chave de ``TEXTOS``).
    tema : str
        Nome do tema (vai no nome do arquivo).
    t : dict
        Cores do tema.
    d : dict
        Saída de ``dados()``.
    """
    L = TEXTOS[lg]
    tl = Tela(1280, 330, t["bg"], L["rtl"])
    tl.caixa(30, 20, 1220, 290, t["card"], t["line"], 1.4, r=14)
    tl.texto(58, 272, L["pns_rotulo"], 1160, color=t["accent"], fontsize=13, fontweight="bold")
    tl.texto(58, 238, L["res_titulo"], 1160, color=t["ink"], fontsize=19, fontweight="bold")
    escala = 300 / 55  # 55% ocupa a barra inteira: o rótulo da maior (40,03%) cabe dentro da trilha
    for i, (nome_tipo, (lgb, het)) in enumerate(
        zip(L["res_tipos"], d["tipos"].values(), strict=True)
    ):
        x = 58 + i * 398
        tl.texto(x, 186, nome_tipo, 360, color=t["ink"], fontsize=16, fontweight="bold")
        for j, (rotulo, v, cor) in enumerate(
            zip(L["res_grupos"], (lgb, het), (t["accent"], t["muted"]), strict=True)
        ):
            yy = 140 - j * 46
            tl.texto(x, yy + 26, rotulo, 360, color=t["muted"], fontsize=13)
            tl.caixa(x, yy, 300, 18, t["line"], r=4)
            tl.caixa(x, yy, max(escala * v, 4), 18, cor, r=4)
            tl.texto(
                x + max(escala * v, 4) + 8,
                yy + 2,
                f"{numero(v, 2, L)}%",
                color=t["ink"],
                fontsize=15,
                fontweight="bold",
            )
    tl.texto(58, 40, L["res_rodape"], 1164, color=t["muted"], fontsize=13)
    tl.salvar(f"results-{lg}-{tema}.svg", t["bg"])


def principal():
    """Gera ícone, banners, cartões e figura de Results em cada idioma e tema, e a marca escura."""
    if not hasattr(matplotlib.ft2font, "__libraqm_version__"):
        raise SystemExit("o hebraico precisa de matplotlib >= 3.11 (libraqm) para a ordem do texto")
    d = dados()
    for lg in TEXTOS:
        for tema, t in TEMAS.items():
            banner(lg, tema, t)
            achados(lg, tema, t, d)
            tipos(lg, tema, t, d)
    tl = Tela(128, 128, "none")
    icone(tl, 2, 2, 124, TEMAS["light"])
    tl.fig.savefig(OUT / "icon.svg", transparent=True, metadata={"Date": None})
    plt.close(tl.fig)
    marca_escura()
    print(f"{3 * len(TEXTOS) * len(TEMAS) + 1} figuras -> {OUT.relative_to(RAIZ)}")


if __name__ == "__main__":
    principal()
