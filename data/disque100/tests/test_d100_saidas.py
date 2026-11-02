"""Travas sobre as SAÍDAS (rodam sem raw/): selo do pré-registro, coerência interna e números publicados no relatório.
Rodar: /opt/homebrew/bin/python3.14 -m pytest -q tests"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
SAI = BASE / "saidas"
sys.path.insert(0, str(BASE / "scripts"))

pytestmark = pytest.mark.skipif(not (SAI / "d100_por_periodo.csv").exists(), reason="tabulação ainda não rodou")


def ler(nome, delim=","):
    return list(csv.DictReader(open(SAI / nome, encoding="utf-8"), delimiter=delim))


def por_periodo():
    d = defaultdict(int)
    for r in ler("d100_por_periodo.csv"):
        d[(r["periodo"], r["recorte"], r["dimensao"], r["unidade"], r["categoria"])] = int(r["n"])
    return d


def test_selo_confere():
    import d100_selo
    assert d100_selo.conferir()


def test_23_periodos_e_catalogo_completo():
    cat = ler("catalogo.tsv", "\t")
    assert len(cat) == 23
    selados = {r["periodo"] for r in ler("d100_qualidade.csv")}
    assert all(r["status"] == "completo" and len(r["sha256"]) == 64 for r in cat if r["periodo"] in selados)
    assert {r["periodo"] for r in ler("d100_por_periodo.csv")} == selados and len(selados) == 23


def test_sha_da_frente_L():
    cat = {r["periodo"]: r["sha256"] for r in ler("catalogo.tsv", "\t")}
    assert cat["2011"].startswith("fd6d3bdf") and cat["2011"].endswith("bd11")
    assert cat["2020S1"].startswith("aed18437") and cat["2020S1"].endswith("d2bb")


def test_soma_das_categorias_igual_ao_total():
    d = por_periodo()
    periodos = {k[0] for k in d}
    for p in periodos:
        for rec in ("canal", "grupo_lgbt"):
            tot = d[(p, rec, "total", "linhas", "")]
            for dim in ("uf", "sexo_vitima", "sexo_suspeito", "sogi_vitima"):
                assert sum(v for k, v in d.items() if k[:4] == (p, rec, dim, "linhas")) == tot, (p, rec, dim)


def test_intersecao_soma_o_canal():
    d = por_periodo()
    for p in {k[0] for k in d}:
        assert sum(v for k, v in d.items() if k[:4] == (p, "canal", "intersecao", "linhas")) == d[(p, "canal", "total", "linhas", "")]


def test_recortes_dentro_do_canal():
    d = por_periodo()
    for p in {k[0] for k in d}:
        for un in ("linhas", "denuncias", "pares_vitima_suspeito"):
            c = d.get((p, "canal", "total", un, ""))
            if c is None:
                continue
            for rec in ("grupo_lgbt", "sogi_lgbt", "motivacao_sogi"):
                assert d.get((p, rec, "total", un, ""), 0) <= c


def test_c_denuncias_todas_le_qualquer():
    d = por_periodo()
    for p in {k[0] for k in d}:
        a = d.get((p, "grupo_lgbt", "total", "denuncias_todas_as_linhas", ""))
        if a is not None:
            assert a <= d[(p, "grupo_lgbt", "total", "denuncias", "")]


def test_qualidade_linhas_batem_com_estrutura():
    import json
    q = {r["periodo"]: int(r["linhas"]) for r in ler("d100_qualidade.csv")}
    for p, n in q.items():
        e = json.loads((SAI / "estrutura" / f"{p}.json").read_text(encoding="utf-8"))
        assert e["linhas_lidas"] == n, p


def serie():
    return {(int(r["ano"]), r["recorte"], r["unidade"]): r for r in ler("d100_serie_anual.csv")}


@pytest.mark.parametrize("ano,rec,un,n", [
    (2011, "grupo_lgbt", "linhas", 1592), (2019, "grupo_lgbt", "linhas", 1331), (2012, "grupo_lgbt", "linhas", 4787),
    (2021, "grupo_lgbt", "denuncias", 1367), (2022, "grupo_lgbt", "denuncias", 4163), (2023, "grupo_lgbt", "denuncias", 6173),
    (2023, "grupo_lgbt", "denuncias_todas_as_linhas", 1827), (2023, "canal", "denuncias", 432309),
    (2023, "motivacao_sogi", "denuncias", 1872), (2023, "sogi_lgbt", "denuncias", 6073),
    (2024, "grupo_lgbt", "denuncias", 8176), (2025, "grupo_lgbt", "denuncias", 9346), (2026, "grupo_lgbt", "denuncias", 10461),
    (2025, "grupo_lgbt", "denuncias_todas_as_linhas", 39), (2025, "canal", "denuncias", 637890), (2024, "motivacao_sogi", "denuncias", 0)])
def test_numeros_do_relatorio(ano, rec, un, n):
    assert int(serie()[(ano, rec, un)]["n"]) == n


def test_porta_balanco_nao_bate():
    """Seção 9: linhas de A no grupo LGBT > vítimas do balanço em todos os anos -> unidade de A fica 'linha'."""
    p = {int(r["ano"]): r for r in ler("d100_porta_balanco.csv") if r["uf"] == "TOTAL"}
    assert sorted(p) == list(range(2011, 2020))
    assert all(int(r["diferenca"]) > 0 for r in p.values())
    assert (int(p[2011]["balanco_total_vitimas"]), int(p[2019]["balanco_total_vitimas"])) == (1206, 926)


def test_comparacao_uf():
    c = {(int(r["ano"]), r["comparada_com"]): r for r in ler("d100_comparacao_uf.csv")}
    assert float(c[(2023, "sinan")]["rho_parcial_dado_pop"]) == 0.448
    assert float(c[(2023, "anuario")]["rho_parcial_dado_pop"]) == 0.279
    assert float(c[(2019, "sinan")]["ic95_parcial_lo"]) == 0.101


def test_comparacao_uf_2024_2025():
    c = {(int(r["ano"]), r["comparada_com"]): r for r in ler("d100_comparacao_uf.csv")}
    assert float(c[(2025, "sinan")]["rho_parcial_dado_pop"]) == 0.544
    assert float(c[(2024, "anuario")]["ic95_parcial_lo"]) == 0.073
    assert (2026, "sinan") not in c  # 2026 parcial fica fora
