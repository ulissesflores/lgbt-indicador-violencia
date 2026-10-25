"""Trava os números das quatro reanálises pré-registradas (C02, C03, C05, C08) que o artigo e o dossiê publicam.

Critérios escritos antes de rodar: research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md (sha256 gravado em CRITERIOS.sha256).
Lê os CSV gerados pelos scripts (dados/painel/painel_c02_indet.py, painel_c03_event_pesos.py, dados/pns/pns_c05_razao_direta.py,
dados/ggb/ggb_c08_numeradores.py). C02 e C03 são recalculados por scripts/reproduzir.py; C05 e C08 leem o microdado da PNS (Trilha 2).
Tolerâncias: arredondamento do número impresso no artigo.
"""
import hashlib
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import R3, csv_rows, perto, texto  # noqa: E402

pct5 = lambda b: 100 * (math.exp(5 * float(b)) - 1)  # conversão exata 100[exp(5b)-1] para uma troca de 5 pontos de ideologia
pct = lambda x: 100 * (math.exp(float(x)) - 1)


def _c02(grupo, desfecho):
    for r in csv_rows("dados/painel/c02_indet_resultados.csv"):
        if r["grupo"] == grupo and r["desfecho"] == desfecho:
            return r
    raise AssertionError((grupo, desfecho))


def test_criterios_da_reanalise_com_hash_gravado_antes():
    gravado = [ln.split()[0] for ln in texto(f"{R3}/escrutinio/reanalise/CRITERIOS.sha256").splitlines()
               if ln.strip() and not ln.startswith("#") and ln.split()[-1] == "CRITERIOS.md"][0]
    real = hashlib.sha256((R3 / "escrutinio" / "reanalise" / "CRITERIOS.md").read_bytes()).hexdigest()
    assert real == gravado == "c3113104e6932d93a68e55f7567517275ad859582423f5cdf8e59b3e91661053"


# ------------------------------------------------------------------ C02: causa indeterminada (teste de falsificação)
def test_c02_agressao_mais_indeterminada_sem_efeito():
    r = _c02("total", "agressao_mais_indet_ln")
    assert perto(r["b"], 0.0036, 0.00005) and perto(r["ic_lo"], -0.019, 0.0005) and perto(r["ic_hi"], 0.026, 0.0005)
    assert perto(r["p_wild"], 0.77, 0.005)
    assert perto(pct5(r["ic_lo"]), -9.1, 0.05) and perto(pct5(r["ic_hi"]), 14.0, 0.05)  # artigo: "entre -9,1% e +14,0%"
    for g in ("total", "homens", "mulheres", "negros", "nao_negros"):
        x = _c02(g, "agressao_mais_indet_ln")
        assert float(x["ic_lo"]) < 0 < float(x["ic_hi"]), g  # nenhum grupo distinguível de zero


def test_c02_parcela_indeterminada_nao_varia_com_ideologia():
    r = _c02("total", "razao_indet_pp")
    assert perto(r["b"], 0.15, 0.005) and perto(r["ic_lo"], -0.57, 0.005) and perto(r["ic_hi"], 0.86, 0.005)
    assert perto(r["p_wild"], 0.68, 0.005) and perto(r["razao_media_pct"], 13.4, 0.05)


# ------------------------------------------------------------------ C03: conversão exata, estudo de eventos, pesos do TWFE
def test_c03_conversao_exata_dos_limites():
    reg = {g: _c02(g, "registrado_ln") for g in ("total", "mulheres", "negros", "arma")}
    esperado = {"total": (-10.8, 13.1), "mulheres": (-10.1, 10.5), "negros": (-16.3, 11.3), "arma": (-16.2, 20.4)}
    for g, (lo, hi) in esperado.items():
        assert perto(pct5(reg[g]["ic_lo"]), lo, 0.05) and perto(pct5(reg[g]["ic_hi"]), hi, 0.05), g
    assert "| tx_arma | +0.0009 | 0.0185 | [-0.0353; +0.0371] | [-17.7; +18.5] | [-16.2; +20.4] | [+1.5; +1.8] |" in \
        texto("dados/painel/c03_event_pesos_resultados.md")


def test_c03_estudo_de_eventos_cai_nas_duas_direcoes():
    linhas = {(r["direcao"], r["desfecho"]): r for r in csv_rows("dados/painel/c03_event_pesos_resultados.csv")
              if r["painel"] == "BRC (principal)" and r["desenho"] == "estrito"}
    ed = linhas[("esquerda->direita", "tx_total")]
    de = linhas[("direita->esquerda", "tx_total")]
    assert ed["n_eventos"] == "9" and de["n_eventos"] == "10"
    # artigo: -20% (IC95% -30% a -8%) esquerda->direita; -19% (-31% a -4%) direita->esquerda
    assert round(pct(ed["media_pos"])) == -20 and round(pct(ed["media_pos_lo"])) == -30 and round(pct(ed["media_pos_hi"])) == -8
    assert round(pct(de["media_pos"])) == -19 and round(pct(de["media_pos_lo"])) == -31 and round(pct(de["media_pos_hi"])) == -4


def test_c03_pesos_do_twfe():
    assert "- Observações com eps < 0: 46.2%" in texto("dados/painel/c03_event_pesos_resultados.md")


# ------------------------------------------------------------------ C05: parcela LGB+ entre vítimas, direto no microdado da PNS
def test_c05_razao_direta_pns():
    r = [x for x in csv_rows("dados/pns/c05_razao_direta.csv") if x["base"].startswith("(b)") and x["corte"] == "total"][0]
    assert r["n_vit"] == "3291" and r["n_lgb"] == "179"
    assert perto(r["R"], 7.1, 0.05) and perto(r["lo"], 5.1, 0.05) and perto(r["hi"], 9.1, 0.05)
    assert perto(float(r["se_taylor"]) / float(r["se_jk"]), 1.00, 0.005)  # Taylor e jackknife concordam
    assert float(r["lo"]) > 4.12  # Sinan 2023 (4,12%) e 2024 (4,08%) fora do IC


# ------------------------------------------------------------------ C08: cobertura implícita do GGB com numeradores comparáveis
def test_c08_numeradores_e_cobertura():
    c = {(r["ano"], r["numerador"]): r for r in csv_rows("dados/ggb/c08_numeradores.csv")
         if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False"}
    assert (c[("2023", "N1")]["n"], c[("2024", "N1")]["n"], c[("2023", "N2")]["n"], c[("2024", "N2")]["n"]) == ("221", "269", "94", "167")
    esperado = {("2023", "N0"): 22.9, ("2023", "N1"): 19.7, ("2023", "N2"): 8.4, ("2024", "N0"): 28.7, ("2024", "N1"): 26.6, ("2024", "N2"): 16.5}
    for k, v in esperado.items():
        assert perto(100 * float(c[k]["cob_RR1.0"]), v, 0.05), k
