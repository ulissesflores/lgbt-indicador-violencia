"""Trava os números publicados: cada número do artigo/dossiê que o repositório consegue sustentar é uma asserção sobre os derivados.

Lê só os CSV/JSON/MD derivados distribuídos (nada de microdado bruto). Compatível com pytest e com `python run_all.py`
(que roda cada função test_* sem pytest). Tolerâncias: arredondamento de publicação; nenhuma tolerância esconde divergência de 2º dígito.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import R3, celulas, csv_rows, json_, linha_md, nums, perto, texto  # noqa: E402


# ------------------------------------------------------------------ PNS 2019 (autorrelato, 12 meses)
def _pns(bloco, rotulo, grupo="LGB+"):
    for r in csv_rows("dados/pns/seguro_pns2019.csv"):
        if r["bloco"] == bloco and r["rotulo"] == rotulo and r["grupo"] == grupo:
            return r
    raise AssertionError((bloco, rotulo, grupo))


def test_pns_violencia_fisica_14_70_x_3_82():
    r = _pns("nivel", "física")
    assert perto(100 * float(r["prev_grupo"]), 14.70, 0.005)
    assert perto(100 * float(r["prev_ref"]), 3.82, 0.005)
    assert perto(r["rp"], 3.84, 0.005) and perto(r["ic_lo"], 2.92, 0.005) and perto(r["ic_hi"], 5.06, 0.005)


def test_pns_rp_ajustada_2_82():
    r = _pns("rp_ajustada", "física")
    assert perto(r["rp"], 2.82, 0.005) and perto(r["ic_lo"], 2.16, 0.005) and perto(r["ic_hi"], 3.68, 0.005)
    assert perto(_pns("rp_ajustada", "sexual")["rp"], 5.00, 0.005)


def test_pns_reproduz_artigo_vasconcelos_sem_divergencia():
    t = texto("dados/pns/seguro_pns2019.md")
    assert "Divergências: 0." in t
    assert all(f"| {c} |" in t for c in ("14.70%", "3.82%", "4.86%", "0.68%", "41.63%", "17.61%"))


def test_pns_escala_populacional():
    assert "≈ 3.01 milhões de adultos" in texto("dados/pns/seguro_pns2019.md")


# ------------------------------------------------------------------ triangulação PNS x Sinan
def test_triangulacao_pns_sinan():
    md = texto("dados/sinan/triangulacao_pns_sinan.md")
    assert "Divergências: 0." in md
    assert "| B. denominador antigo do dossiê (todos os não-LGB+ com a taxa dos heterossexuais) | 6.90% | 5.25% a 9.03% |" in md
    assert "| A. só respondentes de orientação válida (hetero + LGB+), comparável ao Sinan | 7.13% | 5.43% a 9.32% |" in md
    por_ano = {r["ano"]: r for r in csv_rows("dados/sinan/triangulacao_pns_sinan.csv")}
    assert por_ano["2023"]["n_fisica_adultos"] == "197779" and por_ano["2024"]["n_fisica_adultos"] == "202416"
    assert perto(por_ano["2023"]["pct_lgb_entre_validas_sinan"], 4.12, 0.005)
    assert perto(por_ano["2024"]["pct_lgb_entre_validas_sinan"], 4.08, 0.005)
    assert perto(por_ano["2023"]["pct_lgb_implicito_pns_cenarioA"], 7.13, 0.005)


def test_sinan_campo55_lgbtfobia_e_faltante():
    t = texto("dados/sinan/resumo.md")
    assert "## 2023: 588,388 notificações no Brasil" in t and "## 2024: 616,548 notificações no Brasil" in t
    assert "LGBTfobia 2,714 (0.5%)" in t and "LGBTfobia 2,818 (0.5%)" in t
    assert "LGBTfobia 0.54% (2,173)" in t and "LGBTfobia 0.53% (2,264)" in t
    # faltante efetivo do campo 55 entre interpessoais: 29,3% + 14,9% (2023) = 44,2%; 27,7% + 14,8% (2024) = 42,5%
    assert "ignorado+branco 29.3%, não se aplica 14.9%" in t and "ignorado+branco 27.7%, não se aplica 14.8%" in t


# ------------------------------------------------------------------ concordância Sinan x Anuário
def test_concordancia_pooled_0_20():
    md = texto("dados/concordancia/concordancia_v2.md")
    assert "0.20 [IC95% bootstrap por UF: -0.13; 0.50]" in md
    s0 = {r["ano"]: r for r in csv_rows("dados/concordancia/concordancia_v2.csv") if r["especificacao"].startswith("S0")}
    for ano, rho in (("2022", 0.142), ("2023", 0.166), ("2024", 0.152), ("2025", 0.324)):
        assert perto(s0[ano]["rho_parcial"], rho, 0.0005), ano
        assert float(s0[ano]["ic_parcial_lo"]) < 0 < float(s0[ano]["ic_parcial_hi"]), f"IC95% inclui zero em {ano}"
    assert [s0[a]["n_ufs"] for a in ("2022", "2023", "2024", "2025")] == ["22", "23", "23", "22"]


def test_concordancia_contagens_brutas_eram_tamanho_da_uf():
    s0 = {r["ano"]: r for r in csv_rows("dados/concordancia/concordancia_v2.csv") if r["especificacao"].startswith("S0")}
    assert [round(float(s0[a]["rho_contagens"]), 3) for a in ("2022", "2023", "2024", "2025")] == [0.527, 0.575, 0.590, 0.740]
    assert [round(float(s0[a]["rho_taxas"]), 3) for a in ("2022", "2023", "2024", "2025")] == [0.006, 0.081, 0.120, 0.363]


# ------------------------------------------------------------------ painel de governos (UF x ano)
def _painel(arq):
    out = {}
    for ln in texto(arq).splitlines():
        m = re.match(r"^\| (tx_\w+) \| ([+-][\d.]+) \| ([\d.]+) \| \[([+-][\d.]+), ([+-][\d.]+)\] \| (\d+) \|", ln)
        if m:
            out[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)), int(m.group(6)))
    return out


def test_painel_tse_brc_coeficientes_e_ic():
    p = _painel("dados/painel/resultados_tse_brc.md")
    esperado = {"tx_total": (0.0009, 0.0121, -0.023, 0.025), "tx_homens": (0.0005, 0.0125, -0.024, 0.025),
                "tx_mulheres": (-0.0007, 0.0105, -0.021, 0.020), "tx_negros": (-0.0070, 0.0146, -0.036, 0.021),
                "tx_nao_negros": (-0.0016, 0.0171, -0.035, 0.032), "tx_arma": (0.0009, 0.0185, -0.035, 0.037)}
    assert set(p) == set(esperado)
    for k, (b, ep, lo, hi) in esperado.items():
        assert p[k][:4] == (b, ep, lo, hi), k
        assert p[k][4] == 351 and lo < 0 < hi, k  # IC95% cruza zero em todos os desfechos
    assert "Observações: 351 UF-anos" in texto("dados/painel/resultados_tse_brc.md")


def test_painel_72_coeficientes_ic_cruzando_zero():
    """Os 72 coeficientes de sensibilidade (3 variantes de partido x 6 desfechos x 4 escores de ideologia, mais binária): todos com IC95% cruzando zero."""
    t = texto("research-2026-10-21-rodada3/ideologia/sensibilidade_twfe.md")
    ics = re.findall(r"\[([+-]\d\.\d+), ([+-]\d\.\d+)\]", t)
    assert len(ics) == 72
    assert all(float(lo) < 0 < float(hi) for lo, hi in ics)
    # e as três tabelas principais do painel (15 linhas cada) e os diagnósticos
    for arq in ("resultados.md", "resultados_tse.md", "resultados_tse_brc.md"):
        ics = re.findall(r"\[([+-]\d\.\d+), ([+-]\d\.\d+)\]", texto(f"dados/painel/{arq}"))
        assert len(ics) == 15 and all(float(lo) < 0 < float(hi) for lo, hi in ics), arq


def test_painel_wild_cluster_p_0_66_a_0_97():
    t = texto("dados/painel/diagnosticos.md")
    bloco = t.split("## Secundária")[0]
    ps = [float(re.match(r"^\| tx_\w+ \| [^|]+ \| ([\d.]+) \|", ln).group(1)) for ln in bloco.splitlines() if re.match(r"^\| tx_\w+ \| [^|]+ \| [\d.]+ \|", ln)]
    assert ps == [0.943, 0.970, 0.951, 0.661, 0.911, 0.970]
    assert min(ps) == 0.661 and max(ps) == 0.970
    assert "UFs com mudança > 1 ponto no período: 21 de 27" in bloco


def test_painel_dimensoes():
    painel = csv_rows("dados/painel/painel_uf_ano_tse_brc.csv")
    assert len(painel) == 351
    assert len({r["uf"] for r in painel}) == 27
    atlas = csv_rows("dados/atlas_uf_series.csv")
    assert len(atlas) == 3456 and {r["ano"] for r in atlas} == {str(a) for a in range(2010, 2026)}


# ------------------------------------------------------------------ cobertura implícita do GGB
def test_cobertura_implicita_ggb_23_e_29_por_cento():
    base = [r for r in csv_rows("dados/ggb/cobertura_implicita.csv")
            if r["desfecho"] == "agressao" and r["prevalencia_LGB"].startswith("1,89%") and r["medida_GGB"] == "todas"]
    por = {(r["ano"], r["RR_cenario"]): r for r in base}
    r23, r24 = por[("2023", "1.0")], por[("2024", "1.0")]
    assert (r23["ggb"], r24["ggb"]) == ("257", "291")
    assert (round(100 * float(r23["cobertura_implicita"])), round(100 * float(r24["cobertura_implicita"]))) == (23, 29)
    assert (round(float(r23["mortes_esperadas"])), round(float(r24["mortes_esperadas"]))) == (1122, 1013)
    assert (r23["pop_LGB_adulta"], r24["pop_LGB_adulta"]) == ("3025764", "3027156")
    for rr, c23, c24 in (("2.82", 8, 10), ("3.84", 6, 8)):
        assert round(100 * float(por[("2023", rr)]["cobertura_implicita"])) == c23
        assert round(100 * float(por[("2024", rr)]["cobertura_implicita"])) == c24


# ------------------------------------------------------------------ SIM: taxas padronizadas por sexo x raça
def test_asr_sexo_x_raca_2022_24():
    t = texto("dados/sim/asr_brasil.md")
    assert "| homens / mulheres (padronizado) | 10.8 | taxas 38.8 e 3.6 por 100 mil |" in t
    assert "| negros / não negros (padronizado, raça ignorada redistribuída) | 2.56 | taxas 27.9 e 10.9 |" in t
    assert "| Homens negros / Mulheres não negras (padronizado) | 19.9 | taxas 51.7 e 2.6 |" in t
    assert "| Mulheres negras / Mulheres não negras (padronizado) | 1.7 | taxas 4.3 e 2.6 |" in t
    ordem = re.findall(r"^\d\. ([^:]+): ([\d.]+) por 100 mil$", t, re.M)
    assert ordem == [("Mulheres não negras", "2.6"), ("Mulheres negras", "4.3"), ("Homens não negros", "20.0"), ("Homens negros", "51.7")]
    assert "| Negros - Não negros | 18.5 | +1.7 | +16.8 | 91% |" in t


def test_asr_serie_brasil():
    r = {(x["grupo"], x["ano"], x["desfecho"]): x for x in csv_rows("dados/sim/asr_brasil.csv")}
    assert r[("Brasil", "2010", "agressao")]["obitos"] == "52214"
    assert perto(r[("Brasil", "2022", "agressao")]["taxa_padronizada"], 21.8, 0.05)
    assert perto(r[("Brasil", "2024", "agressao")]["taxa_padronizada"], 19.5, 0.05)
    assert perto(r[("Homens negros", "2016", "agressao")]["taxa_padronizada"], 77.2, 0.05)


def test_sim_agregado_sem_campo_individual():
    cab = texto("dados/sim/sim_agressoes_agregado.csv").splitlines()[0]
    assert cab == "ano,uf,sexo,raca,faixa,grupo,arma,lococor,n"


# ------------------------------------------------------------------ GGB: séries, concordância e captura-recaptura
def test_ggb_vs_sim_variacoes_r_0_20():
    r = json_("research-2026-10-21-rodada3/GGB-completo/series/dados_analises/resultados.json")
    todo = r["ggb_vs_sim_variacoes"]["todo"]
    assert todo["n"] == 24 and todo["anos"] == "2001-2024"
    assert todo["pearson"] == [0.2, -0.37, 0.6] and todo["sinal_igual"] == "13/24"
    assert r["acumulado_2017_2024"] == {"GGB": -34.6, "SIM": -37.3, "ANTRA": -31.8, "TDoR": -49.2, "TMM_ciclo": -37.6}
    assert r["acumulado_2000_2017"] == {"GGB": 242.3, "SIM": 40.3}
    assert r["ggb_por_mil_sim"]["2000"] == 2.87 and r["ggb_por_mil_sim"]["2017"] == 6.99


def test_ggb_captura_recaptura_2019():
    c = json_("research-2026-10-21-rodada3/GGB-completo/series/dados_analises/resultados.json")["captura_recaptura_2019"]
    assert (c["ggb_trans"], c["tdor"], c["sobreposicao"], c["uniao_observada"]) == (118, 139, 88, 169)
    assert c["chapman"] == 186.2 and c["ic95_normal"] == [174.5, 197.9]
    assert c["cobertura_ggb_sobre_chapman"] == 0.634 and c["cobertura_ggb_ic"] == [0.596, 0.676]


def test_ggb_dependencia_entre_series():
    r = json_("research-2026-10-21-rodada3/GGB-completo/series/dados_analises/resultados.json")
    assert r["suicidios_pct_do_total"]["2018"] == 23.8 and r["suicidios_pct_do_total"]["2017"] == 13.0
    assert r["consistencia_composicao"]["2020"] == {"soma_categorias": 230, "total_declarado": 237, "falta": 7}
    assert r["consistencia_composicao"]["2021"]["falta"] == 19
    assert r["tmm_dependencia"]["2015"]["pct_GGB"] == 100.0 and r["tmm_dependencia"]["2017"]["pct_GGB"] == 0.0


def test_ggb_validacao_2019_31_3_por_cento():
    v = json_("research-2026-10-21-rodada3/F3-ggb/dados/validacao_resumo.json")
    assert (v["n_amostra"], v["N_universo"], v["recuperadas"], v["correspondem"], v["verificavel_estrito"]) == (160, 329, 106, 88, 50)
    est = {r["medida"]: r for r in csv_rows("research-2026-10-21-rodada3/F3-ggb/dados/resultados.csv")}
    chave = "VERIFICAVEL ESTRITO: corresponde + morte violenta + LGBT+ explicito na fonte"
    assert est[chave]["k"] == "50" and perto(est[chave]["proporcao"], 0.3125, 5e-5)
    assert perto(est[chave]["ic95_wilson_inf"], 0.2458, 5e-5) and perto(est[chave]["ic95_wilson_sup"], 0.388, 5e-5)


def test_ggb_universo_2019_somente_hash():
    for r in csv_rows("research-2026-10-21-rodada3/F3-ggb/dados/ggb2019_universo_hash.csv"):
        assert re.fullmatch(r"[0-9a-f]{10}", r["id"])
    cab = texto("research-2026-10-21-rodada3/F3-ggb/dados/ggb2019_universo_hash.csv").splitlines()[0]
    assert cab == "id,uf,cat_ggb,tem_nome,fonte_tipo,dominio" and len(csv_rows("research-2026-10-21-rodada3/F3-ggb/dados/ggb2019_universo_hash.csv")) == 329


# ------------------------------------------------------------------ poder, custo e identificabilidade
def test_survey_efeito_de_desenho_5_1_e_306_mil_adultos():
    lin = [r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/n_necessario.csv")
           if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["sobreamostra_k"] == "1"][0]
    assert perto(lin["deff_lgb"], 5.10688, 5e-6) and lin["n_lgb_desenho_por_rodada"] == "5787"
    assert lin["n_total_por_rodada"] == "305955" and lin["n_total_duas_rodadas"] == "611910"  # ~306 mil adultos triados por rodada
    d = [r for r in csv_rows("research-2026-10-21-rodada3/F2-custos/deff_pns2019.csv") if r["indicador"] == "lgb" and r["dominio"] == "adultos"][0]
    assert d["n"] == "88531" and d["n_upa"] == "8027" and d["n_estr"] == "574" and perto(d["est"], 0.0189122, 5e-8)


def test_simulacao_identificabilidade():
    r = json_("simulacao/resumo.json")
    assert r["observado"] == {"2022": 783, "2023": 1633, "2024": 2567, "2025": 3481}
    sse = {k: v["sse_log"] for k, v in r["cenarios"].items()}
    assert set(sse.values()) == {0.0472}  # três incidências opostas, mesmo ajuste: série não identifica
    assert r["cenarios"]["S1 incidencia constante"]["R_2030_mediana"] == 22026
    pw = {x["mudanca_relativa"]: x for x in csv_rows("simulacao/poder-survey.csv")}
    assert pw["0.3"]["n_total_sem_sobreamostra"] == "59948" and pw["0.1"]["n_LGB_por_rodada"] == "9481"


# ------------------------------------------------------------------ discurso: mídia, mortalidade, governos
def test_midia_parlamento_contagem_corrigida_14_56_148_2():
    est = {(ln.split("|")[0], ln.split("|")[1]): ln.split("|") for ln in texto("research-2026-10-21-rodada3/discurso/midia/_estimativas.txt").splitlines()
           if ln.split("|")[0] in ("F1", "F2", "F3", "F4") and ln.split("|")[1] == "Parlamento"}
    assert [est[(f, "Parlamento")][2] for f in ("F1", "F2", "F3", "F4")] == ["14", "56", "148", "2"]


def test_midia_amostra_sem_texto_de_terceiros():
    rows = csv_rows("research-2026-10-21-rodada3/discurso/midia/amostra_codificada.csv")
    assert len(rows) == 871
    assert "texto" not in rows[0] and "trecho_sha256" in rows[0]
    assert all(r["trecho_verbatim"] == "" for r in rows if r["universo"] != "Parlamento")
    assert all(re.fullmatch(r"[0-9a-f]{64}", r["trecho_sha256"]) for r in rows)


def test_governos_pais_e_brasil():
    assert len(csv_rows("research-2026-10-21-rodada3/discurso/governos/paises.csv")) == 30
    assert len(csv_rows("research-2026-10-21-rodada3/discurso/governos/u3_65_criminalizam.csv")) == 65
    resumo = texto("research-2026-10-21-rodada3/discurso/governos/u3_resumo.md")
    assert "n = 193 Estados-membros (65 criminalizam por lei ou de fato; 128 nao)." in resumo
    assert "| democracia liberal | 29 | 1 | 3% |" in resumo and "| autocracia fechada | 10 | 23 | 70% |" in resumo


# ------------------------------------------------------------------ ledgers e inventário
def test_ledger_consolidado_571_e_495_ids():
    ids = [json.loads(ln)["id"] for ln in texto("research-consolidado/sources.jsonl").splitlines() if ln.strip()]
    assert len(ids) == 571 and len(set(ids)) == 495


def test_governadores_e_ideologia():
    assert len(csv_rows("dados/governadores_uf_2011_2026_tse.csv")) == 475
    assert len(csv_rows("dados/governadores_uf_2011_2026.csv")) == 475
    assert len(csv_rows("dados/ideologia_partidos.csv")) == 95
    assert len(csv_rows("dados/governadores_tse_eleitos.csv")) == 195


def test_determinismo_semente_registrada():
    """As sementes do estudo são fixas e declaradas nos scripts (20261021 para bootstraps e permutações)."""
    for rel in ("dados/concordancia/concordancia_v2.py", "dados/painel/painel_diagnosticos.py"):
        assert "default_rng(20261021)" in texto(rel), rel
    assert "seed=20261021" in texto("dados/sinan/triangulacao_pns_sinan.py")
    assert "default_rng(20261011)" in texto("simulacao/sim_identificabilidade.py")
    assert math.isfinite(1.0)
