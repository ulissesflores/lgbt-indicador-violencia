"""Regras pré-registradas e tabulação em arquivos SINTÉTICOS (tests/fixtures: A.csv, B.csv, C.csv, sem dado real).
Rodar: /opt/homebrew/bin/python3.14 -m pytest -q tests  (sem -I: o pytest está no site do usuário)."""

import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "scripts"))
import d100_comum as dc  # noqa: E402
import d100_tabular as dt  # noqa: E402

FX = AQUI / "fixtures"


@pytest.mark.parametrize("rot,esperado", [
    ("NULL", "ausente"), ("", "ausente"), ("N/D", "nao_informado"), ("Não informado", "nao_informado"),
    ("DENUNCIANTE NÃO SOUBE INFORMAR", "nao_informado"), ("NÃO SE APLICA - VÍTIMA COMUNIDADE/FAMÍLIA", "nao_se_aplica"),
    ("NA", "nao_informado"), ("MASCULINO", None), ("0", None)])
def test_faltante(rot, esperado):
    assert dc.faltante(rot) == esperado


@pytest.mark.parametrize("rot,esperado", [
    ("LGBT", True), ("Violência Contra População LGBTQIA+", True), ("VIOLÊNCIA CONTRA POPULAÇÃO LGBTQIA+", True),
    ("Pessoa idosa", False), ("VIOLÊNCIA CONTRA A MULHER", False)])
def test_grupo(rot, esperado):
    assert dc.grupo_lgbt(rot) is esperado


@pytest.mark.parametrize("rot,esperado", [
    ("VIDA>HOMICÍDIO", "vida"), ("VIOLÊNCIA FÍSICA.TENTATIVA DE HOMICÍDIO", "vida"), ("LIBERDADE>SEXUAL>FÍSICA>ESTUPRO", "sexual"),
    ("IGUALDADE>DISCRIMINAÇÃO", "discriminacao"), ("DISCRIMINAÇÃO.POR ORIENTAÇÃO SEXUAL", "discriminacao"),
    ("VIOLÊNCIA INSTITUCIONAL.HOMOFOBIA INSTITUCIONAL", "discriminacao"), ("INTEGRIDADE>FÍSICA>ABANDONO", "negligencia"),
    ("violencia_agressao_honra.INJÚRIA", "psicologica"), ("violencia_violacoes_gerais.CRIMES CONTRA A SEGURANÇA PSÍ QUICA", "psicologica"),
    ("INTEGRIDADE>FÍSICA>LESÃO CORPORAL", "fisica"), ("violencia_fisica.AGRESSÃO/VIAS DE FATO", "fisica"),
    ("INTEGRIDADE>PATRIMONIAL>INDIVIDUAL", "patrimonial"), ("LIBERDADE>DIREITOS INDIVIDUAIS>CÁRCERE PRIVADO", "liberdade_trabalho"),
    ("violencia_agressao_direito_liberdade.CÁRCERE PRIVADO", "liberdade_trabalho"), ("DIREITOS SOCIAIS>SAÚDE", "direitos_sociais_civis"),
    ("VIOLÊNCIA INSTITUCIONAL", "institucional"), ("violencia_violacoes_gerais.CRIMES CONTRA O MEIO AMBIENTE", "outros")])
def test_macro(rot, esperado):
    assert dc.macro_violacao(rot) == esperado


def test_motivacao_e_violacao_sogi():
    assert dc.RE_SOGI.search(dc.norm("Motivação.EM RAZÃO DE ORIENTAÇÃO SEXUAL/IDEOLOGIA DE GÊNERO"))
    assert dc.RE_SOGI.search(dc.norm("MOTIVAÇÃO.EM RAZÃO DE ORIENTAÇÃO SEXUAL"))
    assert not dc.RE_SOGI.search(dc.norm("MOTIVAÇÃO.EM RAZÃO DE DISCURSO DE ÓDIO"))
    assert dc.violacao_sogi("DISCRIMINAÇÃO.POR IDENTIDADE DE GÊNERO")
    assert not dc.violacao_sogi("IGUALDADE>DISCRIMINAÇÃO")


def test_datas():
    assert dc.data_iso("2011-08-03 19:22:39.000") == "2011-08-03"
    assert dc.data_iso("05/07/2020 10:58") == "2020-07-05"
    assert dc.data_iso("NULL") is None


def test_tabular_A():
    p, fmt, c, q, _ = dt.tabular("2015", FX / "A.csv")
    assert fmt == "A" and q["linhas"] == 5 and q["linhas_data_fora_do_periodo"] == 1
    assert c[("grupo_lgbt", "total", "linhas", "")] == 3
    assert c[("grupo_lgbt", "uf", "linhas", "SP")] == 2 and c[("grupo_lgbt", "uf", "linhas", "nao_informado")] == 1
    assert c[("grupo_lgbt", "sogi_vitima", "linhas", "lgb")] == 2 and c[("grupo_lgbt", "sogi_vitima", "linhas", "trans")] == 1
    assert c[("canal", "sogi_vitima", "linhas", "nao_lgbt")] == 2
    assert c[("grupo_lgbt", "macro_violacao", "itens", "psicologica")] == 2
    assert c[("grupo_lgbt", "macro_violacao", "itens", "fisica")] == 1
    assert c[("grupo_lgbt", "macro_violacao", "itens", "discriminacao")] == 1
    assert c[("grupo_lgbt", "violacao_sogi", "itens", "1")] == 1
    assert c[("motivacao_sogi", "total", "linhas", "")] == 0
    assert c[("canal", "intersecao", "linhas", "i1=1|sogi=lgb|i3=na")] == 2


def test_tabular_B():
    p, fmt, c, q, _ = dt.tabular("2020S1", FX / "B.csv")
    assert fmt == "B" and q["linhas"] == 3 and q["linhas_data_fora_do_periodo"] == 1
    assert c[("canal", "total", "pares_vitima_suspeito", "")] == 2
    assert c[("grupo_lgbt", "total", "pares_vitima_suspeito", "")] == 1
    assert c[("grupo_lgbt", "total", "linhas", "")] == 2
    assert c[("motivacao_sogi", "total", "linhas", "")] == 2
    assert c[("grupo_lgbt", "sogi_vitima", "linhas", "trans")] == 2
    assert c[("canal", "sogi_vitima", "linhas", "ausente")] == 1
    assert c[("grupo_lgbt", "macro_violacao", "itens", "fisica")] == 2


def test_tabular_C():
    p, fmt, c, q, hs = dt.tabular("2022S2", FX / "C.csv")
    assert fmt == "C" and q["linhas"] == 5 and q["linhas_identicas_repetidas"] == 1
    assert q["linhas_data_fora_do_periodo"] == 2 and len(hs) == 3
    assert c[("canal", "total", "denuncias", "")] == 3
    assert c[("grupo_lgbt", "total", "denuncias", "")] == 2
    assert c[("grupo_lgbt", "total", "denuncias_todas_as_linhas", "")] == 1
    assert c[("grupo_lgbt", "total", "vitimas_declaradas", "")] == 3
    assert c[("canal", "total", "vitimas_declaradas", "")] == 4
    assert c[("grupo_lgbt", "total", "linhas", "")] == 3
    assert c[("sogi_lgbt", "total", "denuncias", "")] == 2
    assert c[("motivacao_sogi", "total", "denuncias", "")] == 1
    assert c[("grupo_lgbt", "uf", "denuncias", "SP")] == 1
    assert c[("grupo_lgbt", "uf", "denuncias", "nao_informado")] == 1
    assert c[("canal", "sogi_vitima", "linhas", "nao_rotulo_nao")] == 1
    assert c[("canal", "intersecao", "denuncias", "i1=1|sogi_lgbt=1|i3=1")] == 1
    assert c[("grupo_lgbt", "macro_violacao", "itens", "discriminacao")] == 2
