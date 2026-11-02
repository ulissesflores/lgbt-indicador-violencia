"""Trava os números novos do artigo v0.5, cada um lido de arquivo do repositório.

Mesmo estilo de ``test_numeros_publicados.py``: só biblioteca padrão, nada de microdado bruto, e
cada função ``test_*`` roda sem argumento (compatível com pytest e com ``python run_all.py``).
Os valores esperados são os publicados no artigo; a fonte de cada um é o arquivo citado
na função.
"""

import csv
import hashlib
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import RAIZ, celulas, csv_rows, texto  # noqa: E402

LIHS = "analysis/counterpoint"
LIHS_CSV = RAIZ / LIHS / "dados" / "lihs-checagem-ggb2016.csv"
LIHS_META = f"{LIHS}/dados/lihs-checagem-ggb2016.META.md"
SHA_LIHS = "0dc25783bfc422ec635826009fbdfbda4efc41ecd7dca0fa05fc469a9179d5ad"
# (governo, último ano inteiro antes da posse, último ano inteiro do governo)
GOVERNOS = (
    ("Dilma", 2010, 2015),
    ("Temer", 2015, 2018),
    ("Bolsonaro", 2018, 2022),
    ("Lula", 2022, 2024),
)


# ------------------------------------------------------------ checagem da LiHS (Motivacao_Homof)
def _tabulacao_lihs():
    """Conta a coluna ``Motivacao_Homof``: do CSV, se estiver no repositório; senão, do META.

    Returns
    -------
    dict
        Rótulo da coluna -> número de casos.
    """
    if LIHS_CSV.is_file():  # o CSV tem nomes de vítimas e de acusados: não é distribuído
        assert hashlib.sha256(LIHS_CSV.read_bytes()).hexdigest() == SHA_LIHS
        linhas = list(csv.reader(LIHS_CSV.read_text(encoding="utf-8").splitlines()))
        col = linhas[1].index("Motivacao_Homof")  # 1ª linha = título da planilha; cabeçalho = 2ª
        cont = {}
        for r in linhas[2:]:
            cont[r[col]] = cont.get(r[col], 0) + 1
        return cont
    cont = {}
    for ln in texto(LIHS_META).splitlines():
        c = celulas(ln) if ln.startswith("|") else []
        if len(c) == 3 and c[1].isdigit() and c[0] != "Total":
            cont[c[0]] = int(c[1])
    return cont


def test_lihs_planilha_nominal_nao_e_distribuida():
    """A planilha da LiHS (nomes de vítimas e de acusados) fica fora; só o META é distribuído."""
    assert (RAIZ / LIHS_META).is_file()
    nominais = list((RAIZ / LIHS).rglob("lihs-checagem-ggb2016*.csv"))
    assert not nominais, f"CSV nominal da LiHS no repositório: {nominais}"


def test_lihs_sha256_gravado_em_todos_os_lugares():
    """O SHA-256 da planilha é o mesmo no META e na frente A."""
    assert SHA_LIHS in texto(LIHS_META)
    assert SHA_LIHS in texto(f"{LIHS}/frente-A-brasil.md")


def test_lihs_tabulacao_motivacao_homof_347_casos():
    """Sim 31, Não 127, Inconclusivo 159, Não localizado 23, Exterior 6, Duplicado 1: total 347."""
    cont = _tabulacao_lihs()
    esperado = {
        "Sim": 31,
        "Não": 127,
        "Inconclusivo": 159,
        "Não localizado": 23,
        "Exterior": 6,
        "Duplicado": 1,
    }
    assert cont == esperado
    assert sum(cont.values()) == 347


# ------------------------------------------- homicídio por governo (taxa padronizada por idade)
def _meio_para_cima(v, casas="0.1"):
    """Arredonda meio para cima (regra de publicação); ``casas`` é o passo, 0.1 por padrão."""
    return Decimal(v).quantize(Decimal(casas), ROUND_HALF_UP)


def _variacoes(rel, coluna_grupo, desfecho):
    """Variação % da taxa do Brasil, do último ano antes da posse ao último ano inteiro.

    Parameters
    ----------
    rel : str
        CSV (relativo à raiz) com ``ano``, ``taxa_padronizada`` e ``desfecho``.
    coluna_grupo : str
        Nome da coluna que traz o grupo ("Brasil").
    desfecho : str
        ``agressao`` ou ``agressao+indet``.

    Returns
    -------
    list of Decimal
        Uma variação por governo, na ordem de ``GOVERNOS``, com 1 casa.
    """
    t = {
        int(r["ano"]): Decimal(r["taxa_padronizada"])
        for r in csv_rows(rel)
        if r[coluna_grupo] == "Brasil" and r["desfecho"] == desfecho
    }
    return [_meio_para_cima((t[b] / t[a] - 1) * 100) for _, a, b in GOVERNOS]


def _d(*valores):
    """Lista de ``Decimal`` a partir de textos."""
    return [Decimal(v) for v in valores]


def test_homicidio_por_governo_asr_brasil():
    """Em ``asr_brasil.csv`` (2 casas), 7 das 8 variações publicadas batem; a 8ª está abaixo."""
    f = "data/sim/asr_brasil.csv"
    assert _variacoes(f, "grupo", "agressao") == _d("11.1", "-4.2", "-21.0", "-10.6")
    # agressao+indet: Dilma, Temer e Lula batem. Bolsonaro, 34,09 -> 29,44, dá -13,64 nas 2 casas;
    # o -13,7 publicado sai da precisão cheia (teste seguinte). O valor não é ajustado aqui.
    v = _variacoes(f, "grupo", "agressao+indet")
    assert [v[0], v[1], v[3]] == _d("7.9", "-0.4", "-6.1")


def test_homicidio_por_governo_precisao_cheia():
    """Na série de precisão cheia (``c10_e1_serie_longo.csv``), as 8 publicadas, com -13,7."""
    f = "data/exposicao/c10_e1_serie_longo.csv"
    assert _variacoes(f, "serie", "agressao") == _d("11.1", "-4.2", "-21.0", "-10.6")
    assert _variacoes(f, "serie", "agressao+indet") == _d("7.9", "-0.4", "-13.7", "-6.1")


def test_asr_brasil_e_a_serie_de_precisao_cheia_dizem_o_mesmo():
    """``asr_brasil.csv`` é a série de precisão cheia arredondada a 2 casas (Brasil, 30 pontos)."""
    cheia = {
        (r["desfecho"], r["ano"]): Decimal(r["taxa_padronizada"])
        for r in csv_rows("data/exposicao/c10_e1_serie_longo.csv")
        if r["serie"] == "Brasil"
    }
    arred = {
        (r["desfecho"], r["ano"]): Decimal(r["taxa_padronizada"])
        for r in csv_rows("data/sim/asr_brasil.csv")
        if r["grupo"] == "Brasil"
    }
    assert len(arred) == 30 and arred.keys() == cheia.keys()
    assert all(abs(arred[k] - cheia[k]) <= Decimal("0.005") for k in arred)


# ---------------------------------------------------------------- fatia de causa indeterminada
def test_fatia_indeterminada_18_0_em_2018_e_30_1_em_2024():
    """Indeterminadas / (agressão + indeterminadas): 18,0% em 2018 e 30,1% em 2024."""
    n = {}
    for r in csv_rows("data/sim/sim_agressoes_agregado.csv"):  # óbitos do SIM por ano e grupo
        chave = (int(r["ano"]), r["grupo"])
        n[chave] = n.get(chave, 0) + int(r["n"])

    def fatia(ano):
        return _meio_para_cima(
            100 * Decimal(n[ano, "indet"]) / (n[ano, "agressao"] + n[ano, "indet"])
        )

    assert fatia(2018) == Decimal("18.0") and fatia(2024) == Decimal("30.1")
    saida = {  # a mesma razão, na saída que o relatório cita
        int(r["ano"]): r["razao_indet_brasil_pct"]
        for r in csv_rows("data/exposicao/c10_e1_serie_longo.csv")
        if r["serie"] == "Brasil"
    }
    assert _meio_para_cima(saida[2018]) == Decimal("18.0")
    assert _meio_para_cima(saida[2024]) == Decimal("30.1")
    rel = texto("data/exposicao/RELATORIO-EXPOSICAO.md")
    assert "18,0% (2018)" in rel and "30,1% (2024)" in rel


# ---------------------------------------------------------------------- coabitação (PNS 2019)
def test_pns_mora_com_conjuge_29_49_lgb_e_62_39_het():
    """Moram com cônjuge no domicílio: 29,49% dos adultos LGB+ e 62,39% dos heterossexuais."""
    # neste bloco a coluna "het" guarda a proporção do grupo inteiro e "lgb", a dos solteiros
    # (agressor_risco_pns2019.py grava [rótulo, total, solteiros, ...])
    linhas = csv_rows("data/pns/agressor_risco_pns2019.csv")
    r = {x["rotulo"]: x for x in linhas if x["bloco"] == "mora_conjuge"}
    pct = {g: _meio_para_cima(100 * Decimal(r[g]["het"]), "0.01") for g in r}
    assert pct == {"LGB+": Decimal("29.49"), "heterossexuais": Decimal("62.39")}
    md = texto("data/pns/agressor_risco_pns2019.md")  # a seção 7 do relatório diz o mesmo
    assert "## 7. Mora com cônjuge" in md
    assert "LGB+: moram com cônjuge 29,49%" in md
    assert "heterossexuais: moram com cônjuge 62,39%" in md


# ------------------------------- análises feitas em 2026-11-01 (decisão do autor, antes do DOI)
def test_pns_razao_por_agressor_com_conjuge_no_domicilio():
    """Com o cônjuge no domicílio no ajuste, familiar 4,31 (2,33 a 7,99).

    Amigo, colega ou vizinho deixa de ser firme.
    """
    r = {
        x["rotulo"]: x
        for x in csv_rows("data/pns/agressor_risco_pns2019.csv")
        if x["bloco"] == "rp_ajustada_agressor_conjuge"
    }
    arred = {
        g: tuple(_meio_para_cima(Decimal(r[g][k]), "0.01") for k in ("medida", "ic_lo", "ic_hi"))
        for g in r
    }
    assert arred["Familiar"] == tuple(_d("4.31", "2.33", "7.99"))
    assert (
        arred["Amigo(a), colega ou vizinho(a)"][1] < 1 < arred["Amigo(a), colega ou vizinho(a)"][2]
    )
    assert set(r) == {
        "Parceiro(a) ou ex",
        "Familiar",
        "Amigo(a), colega ou vizinho(a)",
        "Pessoa conhecida (todos acima)",
        "Pessoa desconhecida",
    }
    assert (
        "| Familiar | 6,22 (3,26 a 11,90) | 4,79 (2,58 a 8,90) | 4,43 (2,38 a 8,26) | "
        "4,31 (2,33 a 7,99) | 85913 |" in texto("data/pns/agressor_risco_pns2019.md")
    )


def test_pns_razoes_sem_cor_ignorada_mudam_no_maximo_0_02():
    """Sem os 9 adultos de cor ou raça ignorada (8 het, 1 LGB+), as razões mudam até 0,02."""
    md = texto("data/pns/agressor_risco_pns2019.md")
    assert "8 heterossexuais e 1 LGB+ na amostra" in md
    linhas = [
        x for x in md.split("## 8.")[1].splitlines() if x.startswith("| ") and "Desfecho" not in x
    ]
    assert len(linhas) == 9
    dif = [
        abs(
            Decimal(c[1].split(" ")[0].replace(",", "."))
            - Decimal(c[2].split(" ")[0].replace(",", "."))
        )
        for c in (x.split(" | ") for x in linhas)
    ]
    assert max(dif) == Decimal("0.02") and all(x.endswith("| 85904 |") for x in linhas)
    assert "| Violência física | 2,82 (2,16 a 3,68) | 2,82 (2,16 a 3,68) | 85904 |" in md


def test_custo_fracao_lgb_por_modo_tabela_k2():
    """Fração LGB+ de cada modo (todos os adultos): 1,35% e 3,26%.

    O módulo na PNAD Contínua detecta 37,9% ou 23,8%.
    """
    r = {
        (x["opcao"][0], x["fracao"]): x
        for x in csv_rows("analysis/survey-cost/opcoes_por_modo.csv")
    }
    pnad = {
        f: (x["pi_lgb"], x["n_lgb"], x["mde_fisica"], x["mde_qualquer"])
        for (o, f), x in r.items()
        if o == "1"
    }
    assert pnad == {
        "PNS 2019, todos os modos": ("0.0189", "5212", "0.317", "0.122"),
        "modulo preenchido pelo entrevistador": ("0.0135", "3723", "0.379", "0.144"),
        "modulo preenchido pelo proprio morador": ("0.0326", "8976", "0.238", "0.093"),
    }
    # a linha "todos os modos" repete a Tabela 6 (opcoes_resumo.csv): só a fração muda
    res = {x["opcao"]: x for x in csv_rows("analysis/survey-cost/opcoes_resumo.csv")}
    for (o, f), x in r.items():
        if f == "PNS 2019, todos os modos":
            base = [v for k, v in res.items() if k.startswith(o + ".")][0]
            assert (x["n_lgb"], x["mde_fisica"], x["mde_qualquer"]) == (
                base["n_lgb"],
                base["mde_fisica"],
                base["mde_qualquer"],
            )


def test_ggb_terceira_leitura_dos_desacordos_muda_so_um_caso():
    """Dois de três nos 6 desacordos: só o caso 159 muda as contagens (morte I->S).

    Fica 74 de 88; os 50 de 160 não mudam.
    """
    import json

    a = json.loads(texto("analysis/ggb-audit/dados/adjudicacao.json"))
    assert (
        a["conferido_pelo_autor"] is True
        and a["codificador_C"]["modelo_registrado"] == "gpt-6-astra"
    )
    muda = {(x["caso"], x["variavel"]): x["final"] for x in a["desacordos"] if x["final"] != x["A"]}
    assert muda == {("1", "desfecho"): "ND", ("159", "morte"): "S", ("159", "tipo"): "H"}
    v = json.loads(texto("analysis/ggb-audit/dados/validacao_resumo.json"))
    assert (
        v["morte_violenta"],
        v["verificavel_estrito"],
        v["motivo_entre_morte_violenta_confirmada"]["U"],
    ) == (74, 50, 36)
    k = json.loads(texto("analysis/ggb-audit/dados/kappa.json"))  # o kappa continua A original x B
    assert (k["morte"]["kappa"], k["lgbt"]["kappa"], len(k["desacordos"])) == (0.462, 0.912, 6)
    assert texto("analysis/ggb-audit/planilha_codificacao.csv") == texto(
        "analysis/ggb-audit/dados/codificacao_A.csv"
    )
