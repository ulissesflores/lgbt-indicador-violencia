# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Lock every number the article cites from the state exposure, the corrections and the Abstract.

Each expected value is the number printed in the article, typed as a constant with the section
or table that prints it; the observed value is read from the frozen file named in each test.
Tolerance is half a unit of the last printed digit. It also regenerates the article-numbers
table with its script into a temporary file and requires it to equal the stored one, checks
that every number listed in paper_numbers.json equals the file it names at the printed
precision (with negative controls), and checks the erratum figures in the corrections notes.

Inputs
------
- paper_numbers.json and verify_paper_numbers.py
- make_provenance.py (loaded as a module)
- docs/corrections.md
- analysis/article-numbers/contas_do_texto.py, contas_do_texto.csv and terceiros_transcritos.csv
- data/exposicao/c10_e2_resumo.csv and data/exposicao/c10_trocas.csv
- data/pns/seguro_pns2019.csv and data/ggb/cobertura_implicita.csv
- analysis/discourse/midia/ (_estimativas.txt, amostra_codificada.csv)
- analysis/ggb-audit/dados/ (codificacao_A.csv, validacao_resumo.json)
- analysis/ggb-series/series/painel_mortes_lgbt.csv and analysis/simulation/resumo.json
- sources/public/p2-f8-dados-uf/sidra/censo9606_n1_raca_sexo_idade_2010_2022.json

Outputs
-------
- none (assertions only; the regenerated table goes to a temporary file)

Usage
-----
python3 -I -m pytest tests/test_paper_numbers.py

Status
------
Test that locks every number printed in the article against paper_numbers.json; it makes
no analysis claim of its own.

Notes
-----
Original description (Portuguese), kept verbatim:

Lock every number the article cites from the state exposure, the corrections and the Abstract.

Each expected value is the number printed in the article (Codex Hash Research Report 2026-10,
Brazilian Portuguese and English editions), typed here as a constant with the section or table
that prints it; the observed value is read from the frozen file of the repository named in each
function. The article itself is not in the repository, so the test locks the numbers, not the
sentences. Tolerance is half a unit of the last printed digit: a change in the data that moves a
printed number fails the test.

Same style as ``test_numeros_v05.py``: standard library only, no raw microdata, and every
``test_*`` function runs without arguments (pytest and ``python run_all.py``).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import csv
import json
import os
import re
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


# ------------------------- Section 3.5: other columns of Table 19, FBSP Yearbook 2026 (p. 135)
def test_anuario2026_tabela19_linha_brasil():
    """Homicide 218 and 187, bodily injury 5,079 and 5,452, rape 471 and 480 (2024 and 2025).

    The Brazil row of Table 19 is kept verbatim, with page and PDF SHA-256, in the panel of LGBT+
    death sources; its first block is the 2,567 -> 3,481 column of ``data/anuario/``.
    """
    painel = csv_rows("analysis/ggb-series/series/painel_mortes_lgbt.csv")
    linhas = [r for r in painel if r["fonte"] == "anu2026"]
    assert {int(r["ano"]): int(r["valor"]) for r in linhas} == {2024: 218, 2025: 187}
    for r in linhas:
        assert r["pagina_pdf"] == "135"
        cel = r["trecho_verbatim"].split()
        assert cel[0] == "Brasil" and cel[1:3] == ["2.567", "3.481"]
        assert cel[4:6] == ["5.079", "5.452"] and cel[7:9] == ["218", "187"]
        assert cel[10:12] == ["471", "480"]


def test_errata_2026_11_24_cinco_leituras():
    """Os cinco números da errata de 2026-11-24 (docs/corrections.md) saem do script e das fontes.

    Roda ``analysis/article-numbers/contas_do_texto.py`` numa saída temporária, exige que ela seja
    idêntica ao CSV distribuído, e confere a Tabela H1 pela data (5/10, 5/8, 21/51), o 329.643 do
    Apêndice K e a transcrição de ODIHR (42 de 57), FRA (30 países; 14% e 13%) e Frisch.
    """
    import importlib.util
    import tempfile
    from pathlib import Path

    pasta = RAIZ / "analysis/article-numbers"
    spec = importlib.util.spec_from_file_location(
        "contas_do_texto_errata", pasta / "contas_do_texto.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # dentro do repositório porque o script imprime a saída relativa à raiz; a pasta some no fim
    with tempfile.TemporaryDirectory(dir=pasta, prefix=".teste-") as tmp:
        mod.SAIDA = Path(tmp) / "contas_do_texto.csv"
        mod.main()
        gerado = mod.SAIDA.read_bytes()
    assert gerado == (pasta / "contas_do_texto.csv").read_bytes(), (
        "contas_do_texto.csv difere do que o script gera"
    )

    contas = {
        r["id"]: r for r in csv.DictReader((pasta / "contas_do_texto.csv").open(encoding="utf-8"))
    }
    for ident, valor in [("h1_nomand_G3", 5), ("h1_nomand_G4", 5), ("h1_nomand_total", 21)]:
        assert float(contas[ident]["calculado"]) == valor, ident
    assert round(float(contas["survey_adultos"]["calculado"])) == 329643
    assert (
        round(float(contas["survey_n_lgb"]["calculado"]), 1) == 5786.3
    )  # 5.786,3 arredondado dá 329.644

    terc = list(csv.DictReader((pasta / "terceiros_transcritos.csv").open(encoding="utf-8")))

    def fonte(ref, impresso):
        """Row of ``terceiros_transcritos.csv`` for one reference and printed value."""
        achadas = [
            r
            for r in terc
            if r["referencia_apa_curta"].startswith(ref) and r["impresso"] == impresso
        ]
        assert achadas and all(r["status"] == "conferido" for r in achadas), (ref, impresso)
        return achadas[0]

    assert fonte("ODIHR (2025)", "42")["valor_na_fonte"].startswith(
        "42 Estados com estatísticas oficiais"
    )
    assert fonte("ODIHR (2025)", "57")["valor_na_fonte"].startswith("57")
    assert fonte("FRA (2024)", "30")["valor_na_fonte"] == "30 países"
    assert "30 países" in fonte("FRA (2024)", "14%")["unidade_ou_recorte"]
    assert "UE" in fonte("FRA (2024)", "13%")["unidade_ou_recorte"]
    for impresso in ("1%", "6%"):
        assert (
            "gays ou lésbicas"
            in fonte("Frisch & Brønnum-Hansen (2009)", impresso)["unidade_ou_recorte"]
        )


def test_sem_hash_so_cobre_o_que_o_selo_regrava():
    """Files exempt from the hash table are only those the seal rewrites and leaves out of itself.

    Negative control: a script or data file added to ``SEM_HASH`` would silence its hash check;
    this test fails if the exemption holds anything the seal covers.
    """
    import importlib.util

    v = _verificador()
    spec = importlib.util.spec_from_file_location("make_provenance", RAIZ / "make_provenance.py")
    prov = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prov)
    assert v.SEM_HASH, "SEM_HASH vazio: a exceção some e o teste perde o objeto"
    for rel in v.SEM_HASH:
        assert prov.excluido(rel), f"{rel} está no selo; isentá-lo do hash esconderia mudança"
        assert rel not in v.carrega()["sha256"], f"{rel} isento e ainda gravado na tabela"
    assert not prov.excluido("paper_numbers.json") and not prov.excluido("make_provenance.py")


def _verificador():
    """Import ``verify_paper_numbers.py`` from the repository root."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "verify_paper_numbers", RAIZ / "verify_paper_numbers.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_todo_numero_de_paper_numbers_json_bate_com_o_arquivo():
    """Every number in ``paper_numbers.json`` equals, at the printed precision, the file it names.

    One check per printed number (the table lists the article line, the value as printed, the file,
    the locator inside the file and the script that writes it); every failure is reported at once.
    The SHA-256 recorded for each file and script must also match: a change in code or data that
    the table does not know about fails here.
    """
    v = _verificador()
    tabela = v.carrega()
    falhas = v.confere_hashes(tabela) + v.confere_valores(tabela)
    assert not falhas, f"{len(falhas)} falhas:\n" + "\n".join(falhas[:40])


def test_paper_numbers_json_bem_formado():
    """Each entry has a known class; located classes name a file and a script; hashes cover them."""
    v = _verificador()
    tabela = v.carrega()
    assert tabela["numbers"], "paper_numbers.json sem números"
    ids = [e["id"] for e in tabela["numbers"]]
    assert len(ids) == len(set(ids)), "id repetido"
    for e in tabela["numbers"]:
        assert e["class"] in v.CLASSES_COM_LOCAL | v.CLASSES_SEM_LOCAL, e["id"]
        assert e["printed"] and all("line" in p and "value" in p for p in e["printed"]), e["id"]
        if e["class"] in v.CLASSES_COM_LOCAL:
            assert e["locator"]["file"] in tabela["sha256"] or e["locator"]["file"] in v.SEM_HASH, (
                e["id"]
            )
            assert all(s in tabela["sha256"] for s in e.get("scripts", [])), e["id"]
        if e["class"] == "output":
            assert e.get("scripts"), f"{e['id']}: output sem o script que grava o arquivo"
        elif e["class"] == "hand-written" or e["class"] in v.CLASSES_SEM_LOCAL:
            # text-arithmetic e third-party têm local e script/transcrição; dispensam reason
            assert e.get("reason"), f"{e['id']}: classe {e['class']} exige reason"


def test_paper_numbers_controle_negativo():
    """The checker fails when the printed value or the source file changes (it is not vacuous).

    Takes the first located entry of each locator type, alters the printed value by one unit of the
    last printed digit, then alters the located number in a temporary copy of the source file; both
    must produce a failure, and the untouched copy must produce none.
    """
    import copy
    import shutil
    import tempfile
    from pathlib import Path

    v = _verificador()
    tabela = v.carrega()
    por_tipo = {}
    for e in tabela["numbers"]:
        if e["class"] == "output":
            por_tipo.setdefault(e["locator"]["type"], e)
    assert {"csv", "md-table"} <= set(por_tipo), sorted(por_tipo)
    for e in por_tipo.values():
        alterada = copy.deepcopy(e)
        valor, casas = v.numero_impresso(e["printed"][0]["value"])
        passo = 10**-casas
        alterada["printed"][0]["value"] = f"{valor + passo:.{casas}f}".replace(".", ",")
        assert v.confere_valores({"numbers": [alterada]}), f"impresso alterado passou: {e['id']}"
        with tempfile.TemporaryDirectory() as tmp:
            rel = e["locator"]["file"]
            (Path(tmp) / rel).parent.mkdir(parents=True)
            shutil.copy(RAIZ / rel, Path(tmp) / rel)
            assert not v.confere_valores({"numbers": [e]}, Path(tmp)), e["id"]
            fonte = v.resolve(e["locator"], Path(tmp))
            texto = (Path(tmp) / rel).read_text(encoding="utf-8")
            achados = [t for t in set(re.findall(r"-?\d+(?:\.\d+)?", texto)) if float(t) == fonte]
            assert achados, f"valor {fonte} não achado como texto em {rel}"
            alvo = max(achados, key=len)
            # +1 na unidade da fonte: trocar só o último dígito de -0.002142346304 não muda o
            # impresso −0,00214; fronteiras de número para não tocar "12" dentro de "1234"
            trocado = repr(float(alvo) + 1)
            texto = re.sub(rf"(?<![\d.]){re.escape(alvo)}(?![\d])", trocado, texto)
            (Path(tmp) / rel).write_text(texto, encoding="utf-8")
            assert v.confere_valores({"numbers": [e]}, Path(tmp)), (
                f"fonte alterada passou: {e['id']}"
            )
    # limite impresso ("< ,001"): o valor da fonte tem de ficar abaixo; baixar o limite até
    # o valor da fonte faz falhar
    limites = [e for e in tabela["numbers"] if any(p.get("bound") for p in e["printed"])]
    assert limites, "nenhum número impresso como limite"
    e = copy.deepcopy(limites[0])
    assert not v.confere_valores({"numbers": [e]}), e["id"]
    fonte = v.resolve(e["locator"])
    e["printed"][0]["value"] = f"{fonte:.6f}".replace(".", ",")
    assert v.confere_valores({"numbers": [e]}), f"limite igual ao valor passou: {e['id']}"


def test_paper_numbers_impresso_corrigido():
    """A printed number marked ``corrected`` passes only with the note and the right rounding.

    The frozen 1.3.0 article prints 26,3 at line 1221 (Appendix F); the calculation gives 26.35,
    26,4 at one decimal (erratum of 2026-11-25 in ``docs/corrections.md``). Negative controls:
    the same entry fails without the note (another id), when the corrected value is not what the
    source rounds to, and when the printed value already matches (a spurious correction).
    """
    import copy

    v = _verificador()
    tabela = v.carrega()
    corrigidas = [e for e in tabela["numbers"] if any(p.get("corrected") for p in e["printed"])]
    assert [
        (e["id"], e["printed"][0]["value"], e["printed"][0]["corrected"]) for e in corrigidas
    ] == [("l1221|6", "26,3", "26,4")]
    e = corrigidas[0]
    assert not v.confere_valores({"numbers": [e]})
    assert "docs/corrections.md" in tabela["sha256"]
    assert round(v.resolve(e["locator"]), 2) == 26.35

    sem_nota = copy.deepcopy(e)
    sem_nota["id"] = "l1221|99"
    assert v.confere_valores({"numbers": [sem_nota]}), "corrigido sem nota passou"
    outro_valor = copy.deepcopy(e)
    outro_valor["printed"][0]["corrected"] = "26,5"
    assert v.confere_valores({"numbers": [outro_valor]}), "corrigido que a fonte não dá passou"
    sobra = copy.deepcopy(e)
    sobra["printed"][0]["value"] = "26,4"
    assert v.confere_valores({"numbers": [sobra]}), "correção desnecessária passou"
    notas = (RAIZ / "docs/corrections.md").read_text(encoding="utf-8")
    assert v.nota_de_correcao(notas, "l1221|6", "26,3", "26,4")
    assert not v.nota_de_correcao(notas.replace("26.3", "26.x"), "l1221|6", "26,3", "26,4")


def test_estimativas_midia_recalculadas_da_amostra():
    """Sample counts, proportions and Wilson intervals of ``_estimativas.txt`` come from the sample.

    The file has no distributed writer (the universe sizes N come from intermediate match files
    that are not distributed), so ``paper_numbers.json`` classes its numbers as hand-written. This
    test recomputes, from ``amostra_codificada.csv``, every column except N and the scaled
    estimate: sample size, claims (AFIRMA + ATRIBUI), denials, mentions and the Wilson 95%
    interval of the proportion, at the precision the file prints. The scaled estimate is then
    checked as N times the recomputed proportion and bounds.
    """
    import math
    from collections import Counter

    amostra = csv_rows("analysis/discourse/midia/amostra_codificada.csv")
    por = Counter((r["familia"], r["universo"], r["postura"]) for r in amostra)
    n_am = Counter((r["familia"], r["universo"]) for r in amostra)
    linhas = (RAIZ / "analysis/discourse/midia/_estimativas.txt").read_text(encoding="utf-8")
    vistas = 0
    for ln in linhas.splitlines()[2:]:
        fam, uni, n_univ, n, k, p_ic, est_ic, neg, men = ln.split("|")
        chave = (fam, uni)
        afirma = por[(*chave, "AFIRMA")] + por[(*chave, "ATRIBUI")]
        assert (int(n), int(k), int(neg), int(men)) == (
            n_am[chave],
            afirma,
            por[(*chave, "NEGA/CRITICA")],
            por[(*chave, "MENCIONA")],
        ), ln
        z, m = 1.959964, n_am[chave]
        prop = afirma / m
        centro = (prop + z * z / (2 * m)) / (1 + z * z / m)
        meia = z * math.sqrt(prop * (1 - prop) / m + z * z / (4 * m * m)) / (1 + z * z / m)
        lo, hi = max(0.0, centro - meia), min(1.0, centro + meia)
        assert p_ic == f"{prop:.2f} [{lo:.2f}-{hi:.2f}]", ln
        nu = int(n_univ)
        assert est_ic == f"{round(nu * prop)} [{round(nu * lo)}-{round(nu * hi)}]", ln
        vistas += 1
    assert vistas == len(n_am) == 18
