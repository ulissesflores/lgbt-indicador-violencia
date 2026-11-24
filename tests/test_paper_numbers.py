"""Lock every number the article cites from the state exposure, the corrections and the Abstract.

Each expected value is the number printed in the article (Codex Hash Research Report 2026-10,
Brazilian Portuguese and English editions), typed here as a constant with the section or table
that prints it; the observed value is read from the frozen file of the repository named in each
function. The article itself is not in the repository, so the test locks the numbers, not the
sentences. Tolerance is half a unit of the last printed digit: a change in the data that moves a
printed number fails the test.

Same style as ``test_numeros_v05.py``: standard library only, no raw microdata, and every
``test_*`` function runs without arguments (pytest and ``python run_all.py``).
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import RAIZ, csv_rows, json_, perto  # noqa: E402

E2 = "data/exposicao/c10_e2_resumo.csv"
CODIFICACAO = "analysis/ggb-audit/dados/codificacao_A.csv"
COBERTURA = "data/ggb/cobertura_implicita.csv"
CENSO = "sources/public/p2-f8-dados-uf/sidra/censo9606_n1_raca_sexo_idade_2010_2022.json"


def _e2(recorte, direcao="todas", grupo="total"):
    """Row of ``c10_e2_resumo.csv`` for one cut, direction and group.

    Parameters
    ----------
    recorte : str
        Pre-registered cut (``P_todas_67``, ``a_janela_completa``,
        ``b_completa_nao_contaminada`` or ``c_posse_eleitoral``).
    direcao : str
        Direction of the change of party.
    grupo : str
        Outcome group (``total`` or ``total_agr_indet`` for the sensitivity with undetermined
        intent added).

    Returns
    -------
    dict
        The CSV row.
    """
    for r in csv_rows(E2):
        if (r["recorte"], r["direcao"], r["grupo"]) == (recorte, direcao, grupo):
            return r
    raise AssertionError((recorte, direcao, grupo))


def _contagem(r):
    """Count the changes, how many rose and how many fell.

    Parameters
    ----------
    r : dict
        Row of ``c10_e2_resumo.csv``.

    Returns
    -------
    tuple of int
        ``(n, rose, fell)``.
    """
    return int(r["n"]), int(r["n_subiu"]), int(r["n_caiu"])


# ---------------------------------------- state exposure, section 3.6 and Tables G6 to G8
def test_exposicao_recorte_p_67_trocas():
    """(P) 67 changes: 31 rose, 36 fell, median -0.7% vs +4.6%; p .016 (Holm .073).

    Fraction that rose .46, p .006 (Holm .032); reference interval +0.8 to +7.8.
    """
    r = _e2("P_todas_67")
    assert _contagem(r) == (67, 31, 36)
    assert perto(r["mediana_pct"], -0.7, 0.05) and perto(r["ref_mediana_p50"], 4.6, 0.05)
    assert perto(r["ref_mediana_p2_5"], 0.8, 0.05) and perto(r["ref_mediana_p97_5"], 7.8, 0.05)
    assert perto(r["p_mediana"], 0.016, 0.0005) and perto(r["p_mediana_holm6"], 0.073, 0.0005)
    assert float(r["p_mediana_holm6"]) > 0.05  # "fails correction for six tests" (Abstract)
    assert perto(r["p_mediana"], 0.0162, 0.00005) and perto(r["p_mediana_holm6"], 0.0732, 0.00005)
    assert perto(r["fracao_subiu"], 0.46, 0.005)
    assert perto(r["p_fracao"], 0.006, 0.0005) and perto(r["p_fracao_holm6"], 0.032, 0.0005)
    assert float(r["p_fracao_holm6"]) < 0.05  # the fraction "resists the correction"


def test_exposicao_recorte_a_47_trocas():
    """(a) 47 changes with full window: 20 rose, 27 fell, median -0.8%; p .008 (Holm .016).

    Reference interval +0.8 to +11.0; the difference holds after Holm.
    """
    r = _e2("a_janela_completa")
    assert _contagem(r) == (47, 20, 27)
    assert perto(r["mediana_pct"], -0.8, 0.05)
    assert perto(r["ref_mediana_p2_5"], 0.8, 0.05) and perto(r["ref_mediana_p97_5"], 11.0, 0.05)
    assert perto(r["p_mediana"], 0.008, 0.0005) and perto(r["p_mediana_holm6"], 0.016, 0.0005)
    assert perto(r["p_mediana_holm6"], 0.0156, 0.00005) and float(r["p_mediana_holm6"]) < 0.05
    assert perto(r["ref_mediana_p50"], 5.9, 0.05)  # reference median printed in the errata
    d = _e2("a_janela_completa", "sentido: para a direita")  # Table G7, first row
    assert _contagem(d) == (25, 9, 16) and perto(d["mediana_pct"], -4.6, 0.05)
    assert perto(d["p_mediana"], 0.022, 0.0005) and perto(d["p_mediana_holm6"], 0.045, 0.0005)
    assert perto(d["p_fracao"], 0.001, 0.0005) and perto(d["p_fracao_holm6"], 0.008, 0.0005)


def test_exposicao_recorte_b_21_trocas():
    """(b) 21 changes, full window and no other change nearby: 8 rose, 13 fell.

    Median -10.2% vs +6.7%; reference interval -4.9 to +17.2; p .002 (Holm .006). The errata
    prints the four-digit values: p 0.0016 and Holm 0.0064.
    """
    r = _e2("b_completa_nao_contaminada")
    assert _contagem(r) == (21, 8, 13)
    assert perto(r["mediana_pct"], -10.2, 0.05) and perto(r["ref_mediana_p50"], 6.7, 0.05)
    assert perto(r["ref_mediana_p2_5"], -4.9, 0.05) and perto(r["ref_mediana_p97_5"], 17.2, 0.05)
    assert perto(r["p_mediana"], 0.0016, 0.00005) and perto(r["p_mediana_holm6"], 0.0064, 0.00005)
    assert perto(r["p_mediana"], 0.002, 0.0005) and perto(r["p_mediana_holm6"], 0.006, 0.0005)


def test_exposicao_recorte_b_por_direcao():
    """(b) by direction: 10 to the right, 2 rose and 8 fell, -11.2%, p .006 (Holm .023).

    11 to the left: 6 rose and 5 fell, +1.3%, p .378 (Holm 1). Errata: 0.0058, 0.0232, 0.3782.
    """
    d = _e2("b_completa_nao_contaminada", "sentido: para a direita")
    assert _contagem(d) == (10, 2, 8)
    assert perto(d["mediana_pct"], -11.2, 0.05) and perto(d["ref_mediana_p50"], 7.5, 0.05)
    assert perto(d["p_mediana"], 0.0058, 0.00005) and perto(d["p_mediana_holm6"], 0.0232, 0.00005)
    e = _e2("b_completa_nao_contaminada", "sentido: para a esquerda")
    assert _contagem(e) == (11, 6, 5)
    assert perto(e["mediana_pct"], 1.3, 0.05) and perto(e["ref_mediana_p50"], 6.7, 0.05)
    assert perto(e["p_mediana"], 0.3782, 0.00005) and float(e["p_mediana_holm6"]) == 1.0


def test_exposicao_recorte_c_45_trocas():
    """(c) 45 changes after an election: 21 rose, 24 fell, median -0.8%; p .026 (Holm .106).

    The difference does not hold after Holm (errata: 0.0264 and 0.1056).
    """
    r = _e2("c_posse_eleitoral")
    assert _contagem(r) == (45, 21, 24)
    assert perto(r["mediana_pct"], -0.8, 0.05) and perto(r["ref_mediana_p50"], 4.6, 0.05)
    assert perto(r["p_mediana"], 0.0264, 0.00005) and perto(r["p_mediana_holm6"], 0.1056, 0.00005)
    assert float(r["p_mediana_holm6"]) > 0.05


def test_exposicao_com_causa_indeterminada():
    """Undetermined intent added: the difference persists only in (b), median -6.3%, p 0.0016.

    In (P) the median becomes +0.5% (34 rose, 33 fell, p .538); in (a) and (c) p is above .05.
    """
    p = {
        rec: _e2(rec, grupo="total_agr_indet")
        for rec in ("P_todas_67", "a_janela_completa", "b_completa_nao_contaminada")
        + ("c_posse_eleitoral",)
    }
    assert [rec for rec, r in p.items() if float(r["p_mediana"]) < 0.05] == [
        "b_completa_nao_contaminada"
    ]
    b = p["b_completa_nao_contaminada"]
    assert perto(b["mediana_pct"], -6.3, 0.05) and perto(b["p_mediana"], 0.0016, 0.00005)
    pp = p["P_todas_67"]
    assert _contagem(pp)[1:] == (34, 33) and perto(pp["mediana_pct"], 0.5, 0.05)
    assert perto(pp["p_mediana"], 0.538, 0.0005)


def test_exposicao_162_celulas_com_holm():
    """162 cells with Holm: 63 with median p < .05, 31 after Holm, 30 of them below zero."""
    cel = [r for r in csv_rows(E2) if r["p_mediana_holm6"] != ""]
    assert len(cel) == 162 and len(csv_rows(E2)) == 189
    assert sum(float(r["p_mediana"]) < 0.05 for r in cel) == 63
    holm = [r for r in cel if float(r["p_mediana_holm6"]) < 0.05]
    assert len(holm) == 31 and sum(float(r["mediana_pct"]) < 0 for r in holm) == 30


def test_exposicao_referencia_de_3_a_15_estados():
    """The reference is formed by few states: 3 to 15 per change (section 3.6)."""
    refs = [int(r["n_referencias"]) for r in csv_rows("data/exposicao/c10_trocas.csv")]
    assert len(refs) == 67 and (min(refs), max(refs)) == (3, 15)


# ---------------------------------------- Grupo Gay da Bahia, section 3.5 and Abstract
def test_ggb_84_noticias_de_106_e_48_de_50():
    """Of 106 cited sources recovered, 84 are news reports; 50 confirm, 48 of them by news.

    The other two are secondary lists. 74 of the 88 matching sources confirm a violent death
    (84.1%); 50 of 160 sampled cases is 31.3%.
    """
    cod = csv_rows(CODIFICACAO)
    rec = [r for r in cod if r["fonte"] == "R"]
    assert len(cod) == 160 and len(rec) == 106
    assert sum(r["tipo_fonte"] == "noticia" for r in rec) == 84
    corr = [r for r in rec if r["corresp"] in ("S", "P")]
    mv = [r for r in corr if r["morte"] == "S"]
    estr = [r for r in mv if r["lgbt"] == "S"]
    assert (len(corr), len(mv), len(estr)) == (88, 74, 50)
    tipos = sorted(r["tipo_fonte"] for r in estr)
    assert tipos.count("noticia") == 48 and tipos.count("lista_secundaria") == 2
    assert round(100 * 74 / 88, 1) == 84.1 and round(100 * 50 / 160, 2) == 31.25
    v = json_("analysis/ggb-audit/dados/validacao_resumo.json")
    assert (v["recuperadas"], v["correspondem"], v["verificavel_estrito"]) == (106, 88, 50)


def test_ggb_divergencia_sem_nota_por_caso():
    """Three recovered sources diverge from the GGB entry on category or city; no free-text note.

    Since v1.3.0 the per-case free-text column (``obs``) is not public; only the 0/1 indicator
    derived from it ships, and the summary count must still be 3.
    """
    cod = csv_rows(CODIFICACAO)
    assert "obs" not in cod[0]
    rec = [r for r in cod if r["fonte"] == "R"]
    assert {r["diverge_cat_ou_cidade"] for r in rec} == {"0", "1"}
    assert {r["diverge_cat_ou_cidade"] for r in cod if r["fonte"] == "NR"} == {""}
    n = sum(r["diverge_cat_ou_cidade"] == "1" for r in rec)
    v = json_("analysis/ggb-audit/dados/validacao_resumo.json")
    assert n == v["divergencia_categoria_ou_cidade"] == 3


# ---------------------------------------- Appendix F, step 1: 3,025,764 adults, 1.93%
def _adultos_2023():
    """Adult population of Brazil in 2023 as the scale exercise counts it.

    Same rule as ``data/ggb/cobertura_implicita.py``: geometric interpolation per cell (sex x
    race x five-year band) between the 2010 and 2022 censuses, extrapolated to 2023; the 15-19
    band counts 2/5 (ages 18 and 19). Recomputed here from the SIDRA table, without numpy.

    Returns
    -------
    float
        Estimated adults in 2023.
    """
    dados = json.loads((RAIZ / CENSO).read_text(encoding="utf-8"))[1:]
    agreg = ("80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais")
    pop = {}
    for x in dados:
        faixa = "80+" if x["D6N"] in agreg else x["D6N"].replace(" a ", "-").replace(" anos", "")
        v = float(x["V"]) if x["V"] not in ("-", "...", "X", "..") else 0.0
        chave = (int(x["D3N"]), x["D5N"], x["D4N"], faixa)
        pop[chave] = pop.get(chave, 0.0) + v
    adultas = ["15-19"] + [f"{a}-{a + 4}" for a in range(20, 80, 5)] + ["80+"]
    total = 0.0
    for ano, sexo, raca, faixa in pop:
        if ano != 2010 or faixa not in adultas:
            continue
        p10, p22 = pop[(2010, sexo, raca, faixa)], pop[(2022, sexo, raca, faixa)]
        v23 = p10 * (p22 / p10) ** ((2023 - 2010) / 12.0)
        total += v23 * (0.4 if faixa == "15-19" else 1.0)
    return total


def test_ggb_escala_3025764_adultos_lgb_1_93_por_cento():
    """3,025,764 LGB+ adults in 2023 out of 156,554,235 adults (156.6 million): 1.93%."""
    lgb = {
        r["pop_LGB_adulta"]
        for r in csv_rows(COBERTURA)
        if r["ano"] == "2023" and r["prevalencia_LGB"].startswith("1,89%")
    }
    assert lgb == {"3025764"}
    adultos = _adultos_2023()
    assert round(adultos) == 156554235 and round(adultos / 1e6, 1) == 156.6
    assert round(100 * 3025764 / adultos, 2) == 1.93


# ---------------------------------------- Abstract (Resumo): the other numbers
def test_resumo_pns_e_boletins():
    """PNS 2019: 14.70% vs 3.82%, adjusted ratio 2.82 (2.16 to 3.68); reports 783 -> 3,481."""
    with open(RAIZ / "data/pns/seguro_pns2019.csv", encoding="utf-8", newline="") as fh:
        pns = {(r["bloco"], r["rotulo"], r["grupo"]): r for r in csv.DictReader(fh)}
    nivel = pns[("nivel", "física", "LGB+")]
    assert perto(100 * float(nivel["prev_grupo"]), 14.70, 0.005)
    assert perto(100 * float(nivel["prev_ref"]), 3.82, 0.005)
    aj = pns[("rp_ajustada", "física", "LGB+")]
    assert perto(aj["rp"], 2.82, 0.005)
    assert perto(aj["ic_lo"], 2.16, 0.005) and perto(aj["ic_hi"], 3.68, 0.005)
    obs = json_("analysis/simulation/resumo.json")["observado"]
    assert (obs["2022"], obs["2025"]) == (783, 3481)


def test_resumo_exposicao():
    """Abstract: 67 changes, -0.7% vs +4.6%; 21 changes, -10.2% vs +6.7%; six groups tested."""
    p, b = _e2("P_todas_67"), _e2("b_completa_nao_contaminada")
    assert int(p["n"]) == 67 and int(b["n"]) == 21
    assert perto(p["mediana_pct"], -0.7, 0.05) and perto(p["ref_mediana_p50"], 4.6, 0.05)
    assert perto(b["mediana_pct"], -10.2, 0.05) and perto(b["ref_mediana_p50"], 6.7, 0.05)
    grupos = {r["grupo"] for r in csv_rows(E2) if r["p_mediana_holm6"] != ""}
    assert len(grupos) == 6  # the Holm family: total, men, women, Black, non-Black, firearm
