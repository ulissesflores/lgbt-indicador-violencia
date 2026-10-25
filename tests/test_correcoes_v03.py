"""Trava as correções da frente R da v0.3 (2026-10-24), feitas depois do escrutínio do Astra: R1 (amostra LGB+ observada e n necessário),
R2 (total nacional do Sinan duplicado), R4 (N2 como cenário, não limite), R6 (IC por inversão do wild-cluster), R7 (Parlamento 0/49 e 1/49).
Cada teste recalcula por conta própria (outra implementação, biblioteca padrão) o que o arquivo publica; os testes de identidade têm controle negativo.
"""
import hashlib
import math
import os
import sys
from statistics import NormalDist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import RAIZ, csv_rows, perto, texto  # noqa: E402

CONTAGENS = ("n_interpessoal", "m_ign_branco", "m_nao_se_aplica", "m_lgbtfobia", "m_racismo", "m_sexismo", "o_ign_branco", "o_nao_se_aplica",
             "o_homo_bi", "g_ign_branco", "g_trans")


# ------------------------------------------------------------------ R2: soma das 27 UFs = BR
def _sinan():
    return csv_rows("dados/sinan/serie_campo55_uf_ano.csv")


def test_r2_soma_das_27_ufs_igual_a_linha_br_em_todas_as_colunas():
    rows = _sinan()
    anos = sorted({r["ano"] for r in rows})
    assert anos == [str(a) for a in range(2015, 2026)]
    for a in anos:
        ufs = [r for r in rows if r["ano"] == a and r["uf"] != "BR"]
        br = [r for r in rows if r["ano"] == a and r["uf"] == "BR"]
        assert len(ufs) == 27 and len(br) == 1, a
        for c in CONTAGENS:
            assert sum(int(r[c]) for r in ufs) == int(br[0][c]), (a, c)


def test_r2_serie_auxiliar_usa_o_total_nacional_sem_duplicar():
    br = {r["ano"]: int(r["m_lgbtfobia"]) for r in _sinan() if r["uf"] == "BR"}
    ser = {r["ano"]: r["sinan_lgbtfobia_n"] for r in csv_rows("research-2026-10-21-rodada3/F3-ggb/dados/serie_ggb_vs_cobertura.csv")}
    for a, v in br.items():
        assert int(ser[a]) == v, (a, ser[a], v)
    assert (br["2023"], br["2024"], br["2025"]) == (2173, 2264, 2410)
    # controle negativo: somar TODAS as linhas (o erro antigo) dá o dobro, e o teste acima o reprovaria
    todas = sum(int(r["m_lgbtfobia"]) for r in _sinan() if r["ano"] == "2023")
    assert todas == 2 * br["2023"] == 4346 and todas != int(ser["2023"])
    assert 'if r["uf"] == "BR"' in texto("research-2026-10-21-rodada3/F3-ggb/scripts/s09_uf_series.py")


# ------------------------------------------------------------------ R1: 1.554 observados, MDE 60,7%, 305.955 adultos
def _n2(p1, p2):
    z = NormalDist().inv_cdf
    za, zb, pb = z(0.975), z(0.8), (p1 + p2) / 2
    return ((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p1 - p2)) ** 2


def _mde(p1, n_eff):
    lo, hi = 1e-4, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _n2(p1, min(p1 * (1 + mid), 0.9999)) > n_eff else (lo, mid)
    return hi


def test_r1_pns_2019_observada_tem_1554_lgb_e_detecta_60_7_por_cento():
    g = [r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/deff_pns2019.csv") if r["indicador"] == "fisica" and r["dominio"] == "LGB+"][0]
    assert g["n"] == "1554"
    cap = {r["indicador"]: r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/capacidade_por_opcao.csv") if r["opcao"].startswith("B'")}
    assert {r["n_lgb"] for r in cap.values()} == {"1554"}
    mde = _mde(float(g["est"]), 1554 / float(g["deff"]))
    assert round(mde, 3) == float(cap["fisica"]["mde_deff_medido"]) == 0.607
    assert round(_mde(float(g["est"]), 1674 / float(g["deff"])), 3) == 0.583   # o número antigo vinha de 1.674 = 88.531 x 1,89% (esperado, não observado)


def test_r1_adultos_a_triar_arredondados_uma_vez():
    nec = [r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/n_necessario.csv")
           if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["sobreamostra_k"] == "1"][0]
    cen = [r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/cenarios_n_custo.csv")
           if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["deff_base"] == "deff medido"][0]
    assert cen["adultos_a_triar"] == nec["n_total_por_rodada"] == "305955" and cen["n_lgb_necessario"] == nec["n_lgb_desenho_por_rodada"] == "5787"
    pi = float([r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/deff_pns2019.csv") if r["indicador"] == "lgb"][0]["est"])
    assert math.ceil(5787 / pi) == 305993                                   # controle: o arredondamento duplo antigo dá outro número


# ------------------------------------------------------------------ R4: N2 é cenário; faixas pelas marginais do GGB
def test_r4_n2_nao_e_limite_e_o_contraexemplo_de_2024_vale():
    c = {(r["ano"], r["cenario"][:22]): int(r["n"]) for r in csv_rows("dados/ggb/c08_cenarios_marginais.csv")}
    assert c[("2024", "contraexemplo do Astra")] == 269 - (96 + 6 - 3) - 6 == 164 < 167
    mins = {a: int(r["n"]) for r in csv_rows("dados/ggb/c08_cenarios_marginais.csv") for a in [r["ano"]] if "mínimo compatível com" in r["cenario"]}
    maxs = {a: int(r["n"]) for r in csv_rows("dados/ggb/c08_cenarios_marginais.csv") for a in [r["ano"]] if "máximo compatível com" in r["cenario"]}
    assert (mins["2023"], maxs["2023"], mins["2024"], maxs["2024"]) == (100, 118, 164, 168)
    assert 94 < mins["2023"] and mins["2024"] < 167 <= maxs["2024"]       # N2 abaixo da faixa em 2023, dentro em 2024: não é limite
    py = texto("dados/ggb/ggb_c08_numeradores.py")
    assert "N2 é LIMITE INFERIOR do numerador cis LGB:" not in py and "CENÁRIO DE SUBTRAÇÃO" in py
    assert "fora do denominador PNS)" not in texto("dados/ggb/cobertura_implicita.md")


# ------------------------------------------------------------------ R6: IC por inversão do wild-cluster (forma pré-registrada)
def test_r6_preregistro_intacto_e_intervalos_contem_zero():
    linha = texto("dados/painel/R6-PREREGISTRO-FORMA.sha256").split()
    assert hashlib.sha256((RAIZ / "dados/painel/R6-PREREGISTRO-FORMA.md").read_bytes()).hexdigest() == linha[0]
    r6 = {r["grupo"]: r for r in csv_rows("dados/painel/r6_ic_wild_invertido.csv")}
    c02 = {r["grupo"]: r for r in csv_rows("dados/painel/c02_indet_resultados.csv") if r["desfecho"] == "registrado_ln"}
    assert set(r6) == set(c02) and len(r6) == 6
    pct = lambda b: 100 * (math.exp(5 * b) - 1)
    for g, r in r6.items():
        b, ep = float(c02[g]["b"]), float(c02[g]["ep"])
        assert perto(r["b"], b, 1e-9) and perto(r["ep"], ep, 1e-9)
        assert float(r["ic_wild_inv_lo"]) < 0 < float(r["ic_wild_inv_hi"]) and r["inclui_zero"] == "True" and r["intervalo_contiguo"] == "True"
        assert perto(r["pct5_normal_lo"], pct(b - 1.96 * ep), 1e-6) and perto(r["pct5_normal_hi"], pct(b + 1.96 * ep), 1e-6)
        assert abs(float(r["p0_grade"]) - float(r["p_wild_publicado"])) < 0.02     # mesmo teste em 0, outra semente: só erro de Monte Carlo
    assert perto(r6["total"]["t26"], 2.0555, 5e-5)
    assert (round(float(r6["total"]["pct5_t26_lo"]), 2), round(float(r6["total"]["pct5_t26_hi"]), 2)) == (-11.28, 13.73)


# ------------------------------------------------------------------ R7: Parlamento, as duas codificações com Fisher
def _fisher(a, n1, b, n2):
    K, N = a + b, n1 + n2
    p = [math.comb(n1, x) * math.comb(n2, K - x) / math.comb(N, K) for x in range(max(0, K - n2), min(n1, K) + 1)]
    p0 = math.comb(n1, a) * math.comb(n2, K - a) / math.comb(N, K)
    return sum(v for v in p if v <= p0 * (1 + 1e-9))


def test_r7_fisher_das_duas_codificacoes():
    r7 = {(r["variavel"], r["a"], r["n1"]): r for r in csv_rows("research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv")}
    assert round(float(r7[("fonte primária", "0", "49")]["p_fisher"]), 4) == round(_fisher(0, 49, 2, 38), 4) == 0.1879
    assert round(float(r7[("fonte primária", "1", "49")]["p_fisher"]), 4) == round(_fisher(1, 49, 2, 38), 4) == 0.5784
    assert r7[("fonte nomeada (qualquer fonte)", "8", "49")]["b"] == "3"
    assert "não codificada" in texto("research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.md")
