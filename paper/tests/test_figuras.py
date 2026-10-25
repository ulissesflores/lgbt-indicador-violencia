"""Testes figura <-> dado de origem do paper (roda com ou sem pytest).

Os valores conferidos aqui sao os que `make_figures.py` leu de volta dos ARTISTAS do matplotlib
(`figures/valores_plotados.json`): largura de barra, centro e extremos de barra de erro. Este
arquivo NAO importa `make_figures.py`; reabre os arquivos de `figures/fontes/` com parser proprio
e compara. Assim uma figura que desenhe o numero errado (coluna trocada, conversao errada,
filtro de linha errado) reprova aqui.

Tambem confere: (i) sha256 de cada copia contra `fontes/SOURCES.tsv`; (ii) sha256 da copia contra o
arquivo de origem na raiz do repositorio (dados/...) e o extrato contra dashboard/dashboard_dados.publico.json; (iii) SHA256SUMS das
figuras; (iv) os numeros que o texto do paper cita para cada figura.

Uso: /opt/homebrew/bin/python3.14 -I tests/test_figuras.py   (ou pytest)
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import math
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
FIG = PAPER / "figures"
FONTES = FIG / "fontes"
PRIVADO = PAPER.parent  # raiz do repositorio: as copias de figures/fontes/ vieram de dados/ (mesmos caminhos relativos)
DASH_PUBLICO = PRIVADO / "dashboard" / "dashboard_dados.publico.json"
TOL = 1e-6


def _v() -> dict:
    return json.loads((FIG / "valores_plotados.json").read_text(encoding="utf-8"))


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _br(x: float, casas: int = 1) -> str:
    """Formata com virgula e arredondamento MEIO PARA CIMA (31,25 -> 31,3), como o texto do paper; independente de make_figures.py."""
    from decimal import ROUND_HALF_UP, Decimal
    return f"{Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP):.{casas}f}".replace(".", ",")


def _perto(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_sources_tsv_bate_com_copias():
    """Cada copia em fontes/ tem o sha256 registrado em SOURCES.tsv."""
    linhas = list(csv.reader(open(FONTES / "SOURCES.tsv", encoding="utf-8"), delimiter="\t"))[1:]
    assert len(linhas) == len([p for p in FONTES.iterdir() if p.is_file()]) - 1   # todo arquivo de fontes/ (menos o proprio SOURCES.tsv) esta registrado
    for arq, _origem, sha in linhas:
        assert _sha(FONTES / arq) == sha, arq


def test_copias_iguais_a_origem_quando_disponivel():
    """Copia == arquivo de origem no repositorio; extrato == extrato publico completo do painel."""
    pares = {"seguro_pns2019.csv": "dados/pns/seguro_pns2019.csv", "seguro_pns2019.md": "dados/pns/seguro_pns2019.md",
             "c08_numeradores.csv": "dados/ggb/c08_numeradores.csv",
             "c02_indet_resultados.csv": "dados/painel/c02_indet_resultados.csv",
             "c03_event_pesos_resultados.csv": "dados/painel/c03_event_pesos_resultados.csv",
             "asr_brasil.csv": "dados/sim/asr_brasil.csv", "sim_identificabilidade_resumo.json": "simulacao/resumo.json",
             "contagens.csv": "research-2026-10-21-rodada3/discurso/midia/contagens.csv",
             "estatisticas_amostra.txt": "research-2026-10-21-rodada3/discurso/midia/_estatisticas_amostra.txt",
             "baseline_resumo_C27.json": "research-2026-10-21-rodada3/escrutinio/simetria/baseline_resumo_C27.json",
             "fisher_C27.txt": "research-2026-10-21-rodada3/escrutinio/simetria/fisher_C27.txt",
             "TRIAGEM.csv": "research-2026-10-21-rodada3/escrutinio/TRIAGEM.csv",
             "triangulacao_pns_sinan.md": "dados/sinan/triangulacao_pns_sinan.md", "triangulacao_pns_sinan.csv": "dados/sinan/triangulacao_pns_sinan.csv",
             "c05_razao_direta.md": "dados/pns/c05_razao_direta.md", "concordancia_v2.csv": "dados/concordancia/concordancia_v2.csv",
             "serie_campo55_uf_ano.csv": "dados/sinan/serie_campo55_uf_ano.csv",
             "anuario_lgbtfobia_uf_ano_v2.csv": "dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv",
             "sidra_9514.json": "fontes/p2-f8-dados-uf/tabnet/raw/sidra_9514.json", "painel_uf_ano_tse_brc.csv": "dados/painel/painel_uf_ano_tse_brc.csv",
             "uf_2019.csv": "research-2026-10-21-rodada3/F3-ggb/dados/uf_2019.csv",
             "inflacao_uf_serie.json": "research-2026-10-21-rodada3/F3-ggb/dados/inflacao_uf_serie.json",
             "serie_ggb_vs_cobertura.csv": "research-2026-10-21-rodada3/F3-ggb/dados/serie_ggb_vs_cobertura.csv",
             "cenarios_n_custo.csv": "research-2026-10-21-rodada3/F2-custos/cenarios_n_custo.csv",
             "capacidade_por_opcao.csv": "research-2026-10-21-rodada3/F2-custos/capacidade_por_opcao.csv",
             "n_necessario.csv": "research-2026-10-21-rodada3/F2-custos/n_necessario.csv",
             "d100_serie_anual.csv": "dados/disque100/saidas/d100_serie_anual.csv"}
    for copia, origem in pares.items():
        assert _sha(FONTES / copia) == _sha(PRIVADO / origem), copia
    dash = DASH_PUBLICO
    ext = json.loads((FONTES / "dashboard_extrato.json").read_text(encoding="utf-8"))
    # o que trava a figura sao os VALORES do painel; o sha256 liga os dois extratos ao mesmo original
    d = json.loads(dash.read_text(encoding="utf-8"))
    assert ext["origem_sha256"] == d["_extrato_publico"]["origem_sha256"]  # os dois extratos vêm do mesmo original
    assert ext["funil"] == d["numeros"]["funil"]["valor"]
    assert ext["tipos"] == d["numeros"]["tipos"]["valor"]
    assert ext["fontes_unicas"] == d["numeros"]["fontes_unicas"]["valor"]
    itens = d["datasets_ptbr"]["countryBars"]["lgbt-violencia-fontes-idiomas"]["groups"][0]["items"]
    assert ext["idiomas"] == {i["name"]: i["value"] for i in itens}


def test_fig1_pns_pontos_e_ic():
    """Fig. 1: prevalencias (pontos do CSV, IC da tabela 1 do .md) e RP bruta/ajustada com IC."""
    v = _v()["fig1"]
    ordem = ["física", "sexual", "qualquer"]
    rows = {(r["bloco"], r["rotulo"]): r for r in csv.DictReader(open(FONTES / "seguro_pns2019.csv", encoding="utf-8"))}
    for i, k in enumerate(ordem):
        r = rows[("nivel", k)]
        assert _perto(v["lgb"]["pontos"][i], 100 * float(r["prev_grupo"]))
        assert _perto(v["het"]["pontos"][i], 100 * float(r["prev_ref"]))
        assert _perto(v["rp"]["pontos"][i], float(r["rp"]))
        assert _perto(v["rp"]["ic"][i][0], float(r["ic_lo"])) and _perto(v["rp"]["ic"][i][1], float(r["ic_hi"]))
        a = rows[("rp_ajustada", k)]
        assert _perto(v["rpaj"]["pontos"][i], float(a["rp"]))
        assert _perto(v["rpaj"]["ic"][i][0], float(a["ic_lo"])) and _perto(v["rpaj"]["ic"][i][1], float(a["ic_hi"]))
    # IC das prevalencias: tabela 1 do .md, lida aqui por split simples (parser diferente do script)
    md = (FONTES / "seguro_pns2019.md").read_text(encoding="utf-8").split("## 1.")[1].split("## 2.")[0]
    ic = {}
    for linha in md.splitlines():
        cel = [c.strip() for c in linha.strip("|").split("|")]
        if cel and cel[0] in ordem:
            het = cel[1].split("[")[1].rstrip("]").split(";")
            lgb = cel[2].split("[")[1].rstrip("]").split(";")
            ic[cel[0]] = ([float(x) for x in lgb], [float(x) for x in het])
    for i, k in enumerate(ordem):
        assert _perto(v["lgb"]["ic"][i][0], ic[k][0][0], 1e-4) and _perto(v["lgb"]["ic"][i][1], ic[k][0][1], 1e-4)
        assert _perto(v["het"]["ic"][i][0], ic[k][1][0], 1e-4) and _perto(v["het"]["ic"][i][1], ic[k][1][1], 1e-4)
    # numeros citados no texto do paper
    assert round(v["lgb"]["pontos"][0], 2) == 14.70 and round(v["het"]["pontos"][0], 2) == 3.82
    assert round(v["rp"]["pontos"][0], 2) == 3.84 and round(v["rpaj"]["pontos"][0], 2) == 2.82


def test_fig2_cobertura_ggb():
    """Fig. 2: cobertura = n/E por ano x numerador x RR, agressao, prevalencia 1,89%, sem proxy."""
    v = _v()["fig2"]
    esperado = {}
    for r in csv.DictReader(open(FONTES / "c08_numeradores.csv", encoding="utf-8")):
        if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["ano"] in ("2023", "2024"):
            esperado[f"{r['ano']}-{r['numerador']}"] = {rr: int(r["n"]) / float(r[f"E_RR{rr}"]) for rr in ("1.0", "2.82", "3.84")}
    assert sorted(v["linhas"]) == sorted(esperado)
    for col, rr in (("cob_RR1.0", "1.0"), ("cob_RR2.82", "2.82"), ("cob_RR3.84", "3.84")):
        for lab, largura in zip(v["linhas"], v[col]):
            assert _perto(largura, 100 * esperado[lab][rr], 1e-9), (lab, rr)
    cob = dict(zip(v["linhas"], v["cob_RR1.0"]))
    assert round(cob["2023-N2"], 1) == 8.4 and round(cob["2024-N2"], 1) == 16.5 and round(cob["2024-N1"], 1) == 26.6


def test_fig3_painel_e_eventos():
    """Fig. 3a: 100[exp(5b)-1] de b e do IC do TWFE; 3b: exp(media dos pos)-1 do estudo de eventos."""
    v = _v()["fig3"]
    c02 = {(r["grupo"], r["desfecho"]): r for r in csv.DictReader(open(FONTES / "c02_indet_resultados.csv", encoding="utf-8"))}
    for desf in ("registrado_ln", "agressao_mais_indet_ln"):
        for g, p, (lo, hi) in zip(v[desf]["grupos"], v[desf]["pontos"], v[desf]["ic"]):
            r = c02[(g, desf)]
            assert _perto(p, 100 * math.expm1(5 * float(r["b"])))
            assert _perto(lo, 100 * math.expm1(5 * float(r["ic_lo"])))
            assert _perto(hi, 100 * math.expm1(5 * float(r["ic_hi"])))
    assert len(v["registrado_ln"]["grupos"]) == 6 and len(v["agressao_mais_indet_ln"]["grupos"]) == 5
    tot = v["registrado_ln"]["ic"][0]
    assert (round(tot[0], 1), round(tot[1], 1)) == (-10.8, 13.1)
    ev = {(r["desenho"], r["direcao"]): r for r in csv.DictReader(open(FONTES / "c03_event_pesos_resultados.csv", encoding="utf-8"))
          if r["painel"] == "BRC (principal)" and r["desfecho"] == "tx_total"}
    for rot, p, (lo, hi) in zip(v["event_study"]["rotulos"], v["event_study"]["pontos"], v["event_study"]["ic"]):
        r = ev[tuple(rot.split("|"))]
        assert _perto(p, 100 * math.expm1(float(r["media_pos"])))
        assert _perto(lo, 100 * math.expm1(float(r["media_pos_lo"])))
        assert _perto(hi, 100 * math.expm1(float(r["media_pos_hi"])))
    assert [round(x) for x in v["event_study"]["pontos"][:2]] == [-20, -19]


def test_fig4_e_fig5_fontes():
    """Fig. 4 (funil) e Fig. 5 (idioma e tipo) == extrato do painel; cada bloco da Fig. 5 soma 829."""
    v = _v()
    ext = json.loads((FONTES / "dashboard_extrato.json").read_text(encoding="utf-8"))
    assert v["fig4"]["larguras"] == [float(ext["funil"][k]) for k in v["fig4"]["etapas"]]
    assert v["fig4"]["larguras"] == [829.0, 79.0, 50.0, 46.0]
    assert v["fig5"]["idiomas"] == {k: float(x) for k, x in ext["idiomas"].items()}
    assert v["fig5"]["tipos"] == {k: float(x) for k, x in ext["tipos"].items()}
    assert sum(v["fig5"]["idiomas"].values()) == ext["fontes_unicas"] == sum(v["fig5"]["tipos"].values()) == 829


def test_sha256sums_das_figuras():
    """Toda linha de figures/SHA256SUMS confere e as 28 figuras existem em PDF, SVG e PNG."""
    for linha in (FIG / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        sha, rel = linha.split("  ", 1)
        if rel in ("SHA256SUMS",):
            continue
        assert _sha(FIG / rel) == sha, rel
    for n in ("fig1_pns2019_vitimizacao", "fig2_ggb_cobertura_implicita", "fig3_governos_painel_eventos",
              "fig4_funil_evidencia", "fig5_fontes_idioma_tipo", "fig6_proporcao_1_em_7", "fig7_mapa_de_respostas",
              "fig8_taxas_sim_grupos", "fig9_governos_forest", "fig10_identificabilidade", "fig11_circulacao_parlamento",
              "fig12_escrutinio_dois_lados", "fig13_pns_sinan_janelas", "fig14_concordancia_sinan_anuario", "fig15_ideologia_taxa_residuos",
              "fig16_linha_do_tempo_fontes", "fig17_tamanho_de_survey", "fig18_motivacao_sinan", "fig19_ggb_homicidio_uf",
              "fig20_serie_nacional_trocas", "fig21_alinhamento_governador_presidente", "fig22_taxa_nacional_por_governo", "fig23_trocas_de_governador_exposicao", "fig24_caminho_do_dado",
              "fig25_mortalidade_internacional", "fig26_ggb_verificabilidade", "fig27_ggb_curva_de_hipoteses", "fig28_disque100_serie"):
        assert all((FIG / f"{n}.{ext}").exists() for ext in ("pdf", "svg", "png")), n


# ---------------------------------------------------------------- Figuras 6 a 12 (v0.2)
# Cada _chk_figN(v) recebe o bloco da figura em valores_plotados.json e CONFERE contra o arquivo de origem com parser proprio.
# test_controle_negativo corrompe um numero de cada bloco e exige que o mesmo conferidor reprove.
import copy
import re

PAPER_V01_SHA = "8f6cd9f100de042849a48995f0161895ce229943c33f9a29ffb8cbfeadccb2a6"


def _csv(nome: str, delim: str = ",") -> list[dict]:
    return list(csv.DictReader(open(FONTES / nome, encoding="utf-8"), delimiter=delim))


def _dash() -> dict:
    return json.loads(DASH_PUBLICO.read_text(encoding="utf-8"))["numeros"]


def _chk_fig6(v: dict) -> None:
    rows = {(r["bloco"], r["rotulo"]): r for r in _csv("seguro_pns2019.csv")}
    n = rows[("nivel", "física")]
    for chave, prev in (("lgb", 100 * float(n["prev_grupo"])), ("het", 100 * float(n["prev_ref"]))):
        fr = v[chave]["fracoes"]
        assert _perto(sum(fr), prev, 1e-9), chave                      # a area preenchida soma a prevalencia
        assert len(fr) == math.ceil(prev) and all(0 < f <= 1 for f in fr), chave   # 15 e 4 quadrados, so o ultimo parcial
        assert all(f == 1 for f in fr[:-1]), chave
        assert v[chave]["um_em"] == round(100 / prev), chave
    assert (v["lgb"]["um_em"], v["het"]["um_em"]) == (7, 26)
    a = rows[("rp_ajustada", "física")]
    assert _perto(v["rp"]["pontos"][0], float(n["rp"])) and _perto(v["rp"]["pontos"][1], float(a["rp"]))
    assert _perto(v["rp"]["ic"][0][0], float(n["ic_lo"])) and _perto(v["rp"]["ic"][0][1], float(n["ic_hi"]))
    assert _perto(v["rp"]["ic"][1][0], float(a["ic_lo"])) and _perto(v["rp"]["ic"][1][1], float(a["ic_hi"]))
    assert [round(x, 2) for x in v["rp"]["pontos"]] == [3.84, 2.82]
    assert (round(v["rp"]["ic"][1][0], 2), round(v["rp"]["ic"][1][1], 2)) == (2.16, 3.68)


def test_fig6_proporcao_1_em_7():
    """Fig. 6: 100 quadrados por grupo (14,70% e 3,82% da violencia fisica), 'um em 7' x 'um em 26', RP 3,84 e 2,82 [2,16-3,68]."""
    _chk_fig6(_v()["fig6"])


CATEGORIAS = {"sustentada", "parcial", "não sustentada pelo que foi medido", "não testável", "sem veredito"}
ROTULO_EXIBIDO = {"sem veredito": "sem veredito (só descrito)"}


def tsv_ancora_v03(tsv: list) -> str:
    return next(r["ancora_v03"] for r in tsv if r["linha"] == "L2" and r["coluna"] == "N1")


def _chk_fig7(v: dict) -> None:
    tsv = _csv("vereditos_tabela1_tabela5.tsv", "\t")
    cel = {f"{r['linha']}|{r['coluna']}": r for r in tsv if r["linha"] != "COL"}
    assert sorted(v["celulas"]) == sorted(cel) and len(cel) == 12          # 3 perguntas x 4 niveis, nenhuma celula faltando
    corpo = " ".join((FONTES / "paper_v0.1.md").read_text(encoding="utf-8").split())
    assert _sha(FONTES / "paper_v0.1.md") == PAPER_V01_SHA                 # o texto-fonte e o v0.1 congelado
    cor_de: dict = {}
    for k, r in cel.items():
        assert r["categoria"] in CATEGORIAS and "falso" not in r["categoria"], k   # so o vocabulario unico (2.3)
        assert " ".join(r["texto_verbatim"].split()) in corpo, k           # cada celula tem trecho literal do paper v0.1
        assert v["celulas"][k]["rotulo_exibido"] == ROTULO_EXIBIDO.get(r["categoria"], r["categoria"]), k
        cor_de.setdefault(r["categoria"], set()).add(v["celulas"][k]["fundo"])
    assert all(len(c) == 1 for c in cor_de.values())                        # mesma categoria, mesma cor
    assert len({next(iter(c)) for c in cor_de.values()}) == len(cor_de)     # categorias diferentes, cores diferentes
    for r in (x for x in tsv if x["linha"] == "COL"):
        assert " ".join(r["texto_verbatim"].split()) in corpo
    # numeros que aparecem nas celulas batem com o CSV da PNS
    p = {(r["bloco"], r["rotulo"]): r for r in _csv("seguro_pns2019.csv")}[("nivel", "física")]
    assert f"{100 * float(p['prev_grupo']):.2f}".replace(".", ",") + "%" in cel["L1|N1"]["texto_verbatim"]
    assert f"{100 * float(p['prev_ref']):.2f}".replace(".", ",") + "%" in cel["L1|N1"]["texto_verbatim"]
    assert (cel["L1|N1"]["categoria"], cel["L2|N1"]["categoria"], cel["L3|N1"]["categoria"]) == ("sustentada", "não testável", "sustentada")
    ancora = " ".join(tsv_ancora_v03(tsv).split())
    assert ancora in " ".join((FONTES / "L-SECAO-3-3-PROPOSTA.md").read_text(encoding="utf-8").split())           # mundo: "sustentada ... fora do Brasil" (adendo Q1), texto da frente L
    assert "populações definidas" in cel["L2|N1"]["texto_curto"] and "Brasil" in cel["L2|N1"]["texto_curto"]      # a celula nao diz so "nao testavel": qualifica Brasil x mundo
    assert all("fração nacional não estimada" in cel[f"{l}|N4"]["texto_curto"] for l in ("L1", "L2", "L3"))


def test_fig7_mapa_de_respostas():
    """Fig. 7: 12 celulas pergunta x nivel; categoria no vocabulario unico, trecho literal do paper v0.1, 1 cor por categoria."""
    _chk_fig7(_v()["fig7"])


GRUPOS_SIM = ["Homens negros", "Homens não negros", "Mulheres negras", "Mulheres não negras"]


def _chk_fig8(v: dict) -> None:
    anos: dict = {g: [] for g in GRUPOS_SIM}
    for r in _csv("asr_brasil.csv"):
        if r["desfecho"] == "agressao" and r["grupo"] in anos and r["ano"] in ("2022", "2023", "2024"):
            anos[r["grupo"]].append(float(r["taxa_padronizada"]))
    assert v["grupos"] == GRUPOS_SIM and all(len(x) == 3 for x in anos.values())
    for g, m in zip(GRUPOS_SIM, v["media"]):
        assert _perto(m, sum(anos[g]) / 3, 1e-9), g
    assert sorted(v["pontos"]) == sorted(x for g in GRUPOS_SIM for x in anos[g])
    d = _dash()["sim_taxa_padronizada_2022_24"]["valor"]                    # mesma media que o painel de publicacao
    for g, m in zip(GRUPOS_SIM, v["media"]):
        assert _perto(m, d[g]["media"], 1e-9) and min(anos[g]) == d[g]["min"] and max(anos[g]) == d[g]["max"], g
    # razoes e taxas da Tabela 3 do paper v0.1
    corpo = (FONTES / "paper_v0.1.md").read_text(encoding="utf-8")
    ref = v["media"][3]
    for g, m in zip(GRUPOS_SIM, v["media"]):
        fm = _br
        assert f"| {g} | {fm(m, 1)} | {fm(m / ref, 1)} |" in corpo, g
    assert v["media"][0] > v["media"][1] > v["media"][2] > v["media"][3]


def test_fig8_taxas_sim_grupos():
    """Fig. 8: media 2022-24 da taxa padronizada dos 4 grupos == asr_brasil.csv == painel == Tabela 3 (2,6 / 4,3 / 20,0 / 51,7; 1,0 / 1,7 / 7,7 / 19,9)."""
    _chk_fig8(_v()["fig8"])


GRUPOS_PAINEL = ["total", "homens", "mulheres", "negros", "nao_negros", "arma"]


def _chk_fig9(v: dict) -> None:
    c02 = {(r["grupo"], r["desfecho"]): r for r in _csv("c02_indet_resultados.csv")}
    assert v["grupos"] == GRUPOS_PAINEL
    for g, p, (lo, hi) in zip(v["grupos"], v["pontos"], v["ic"]):
        r = c02[(g, "registrado_ln")]
        assert _perto(p, 100 * math.expm1(5 * float(r["b"])), 1e-9) and _perto(lo, 100 * math.expm1(5 * float(r["ic_lo"])), 1e-9) \
            and _perto(hi, 100 * math.expm1(5 * float(r["ic_hi"])), 1e-9), g
        assert lo < p < hi
    tab = _dash()["governos_painel"]["valor"]["tabela"]                    # limites que o paper cita (arredondados a 0,1)
    for g, (lo, hi) in zip(v["grupos"], v["ic"]):
        t = tab["tx_" + g]
        assert abs(lo - t["lo_pct"]) < 0.06 and abs(hi - t["hi_pct"]) < 0.06, g
    quedas, altas = [-lo for lo, _ in v["ic"]], [hi for _, hi in v["ic"]]
    assert (round(min(quedas), 1), round(max(quedas), 1), round(min(altas), 1), round(max(altas), 1)) == (10.1, 16.3, 10.5, 20.4)


def test_fig9_governos_forest():
    """Fig. 9: IC95% de cada desfecho (100[exp(5b)-1]) == c02 == limites do paper: exclui queda de 10,1% a 16,3% e alta de 10,5% a 20,4%."""
    _chk_fig9(_v()["fig9"])


def _chk_fig10(v: dict) -> None:
    js = json.loads((FONTES / "sim_identificabilidade_resumo.json").read_text(encoding="utf-8"))
    assert v["observado"] == v["observado_plotado"] == [783.0, 1633.0, 2567.0, 3481.0] == [float(x) for x in js["observado"].values()]
    assert len({p["sse_log"] for p in js["cenarios"].values()}) == 1 and next(iter(js["cenarios"].values()))["sse_log"] == 0.0472
    for nome, p in js["cenarios"].items():
        d = v["cenarios"][nome[:2]]
        for t in range(4):
            inc = p["I0_2022"] * (1 + p["g"]) ** t
            prop = js["P0"] * (1 + p["h_registro"]) ** t
            assert _perto(d["incidencia_mil"][t], inc / 1000, 1e-9) and _perto(d["propensao_pct"][t], 100 * prop, 1e-9)
            assert _perto(d["registro_modelo"][t], inc * prop, 1e-9)
        assert abs(d["propensao_pct"][3] / 100 - p["p_2025"]) < 6e-4       # confere com o p de 2025 que o proprio arquivo traz
    inc25 = {k: d["incidencia_mil"][3] for k, d in v["cenarios"].items()}
    assert inc25["S2"] > inc25["S1"] > inc25["S3"]                          # incidencias que divergem...
    reg25 = [d["registro_modelo"][3] for d in v["cenarios"].values()]
    assert max(reg25) / min(reg25) < 1.01                                   # ...para o mesmo registrado


def test_fig10_identificabilidade():
    """Fig. 10: tres incidencias (constante, +15%, -5%) reconstruidas do JSON de simulacao dao o mesmo registrado (SSE 0,0472)."""
    _chk_fig10(_v()["fig10"])


def _chk_fig11(v: dict) -> None:
    uni: dict = {}
    den = 0
    for r in _csv("contagens.csv"):
        if r["ano"] == "total":
            continue
        if r["universo"] in ("Camara", "Senado") and r["familia"] == "TOTAL":
            den += int(r["n"])
        elif r["consulta"] == r["familia"] + "-any" or r["consulta"].startswith(r["familia"] + "-any"):
            if r["universo"] in ("Camara", "Senado", "Camara (v1 literal)", "Senado (v1 literal)") and r["familia"] in ("F1", "F2", "F3", "F4"):
                k = ("v1" if "v1" in r["universo"] else "v2", r["familia"])
                uni[k] = uni.get(k, 0) + int(r["n"])
    fam = ["F1", "F2", "F3", "F4"]
    assert v["familias"] == fam and v["denominador"] == den == 258011
    assert v["v1"] == [float(uni[("v1", f)]) for f in fam] == [23.0, 161.0, 692.0, 4.0]
    assert v["v2"] == [float(uni[("v2", f)]) for f in fam] == [14.0, 56.0, 148.0, 2.0]
    d = _dash()["discurso_parlamento"]["valor"]                             # igual ao painel de publicacao
    assert v["denominador"] == d["denominador"] and v["v2"] == [float(d["v2"][f]) for f in fam] and v["v1"] == [float(d["v1"][f]) for f in fam]
    r7 = {r["codificacao_F2"]: r for r in _csv("r7_parlamento_sensibilidade.csv") if r["variavel"] == "fonte primária"}
    lit = next(r for k, r in r7.items() if "literal" in k)
    apl = next(r for k, r in r7.items() if "aplicada" in k)
    seg = next(r for k, r in r7.items() if k.startswith("segundo"))
    est = (FONTES / "estatisticas_amostra.txt").read_text(encoding="utf-8")
    assert "F2|Parlamento|56|51|0.91 [0.81-0.96]|43|6|2|0|0/49 [0.00-0.07]|" in est and (apl["a"], apl["n1"]) == ("0", "49")   # 0 de 49 = regra aplicada
    assert [tuple(x) for x in v["fonte_primaria"]["linhas"]] == [(1, 49), (0, 49), (1, 50), (2, 38)]                     # 1/49 literal e principal; 0/49 sensibilidade
    assert (lit["a"], lit["n1"], lit["b"], lit["n2"]) == ("1", "49", "2", "38") and (seg["a"], seg["n1"]) == ("1", "50")
    pts, ic = v["fonte_primaria"]["pontos"], v["fonte_primaria"]["ic"]
    for k, (a_, n_) in enumerate([(1, 49), (0, 49), (1, 50), (2, 38)]):
        z = 1.959963984540054
        p = a_ / n_
        c = (p + z * z / (2 * n_)) / (1 + z * z / n_)
        h = z * math.sqrt(p * (1 - p) / n_ + z * z / (4 * n_ * n_)) / (1 + z * z / n_)       # Wilson recalculado
        assert _perto(pts[k], 100 * p, 1e-9) and abs(ic[k][1] - 100 * (c + h)) < 1e-6 and abs(ic[k][0] - max(0.0, 100 * (c - h))) < 1e-6, k
    base = json.loads((FONTES / "baseline_resumo_C27.json").read_text(encoding="utf-8"))
    lo, hi = (100 * x for x in base["wilson95"])
    assert abs(ic[3][0] - lo) < 1e-3 and abs(ic[3][1] - hi) < 1e-3                          # 2/38: 5,3% [1,5-17,3%]
    assert abs(v["p_fisher"]["literal"] - 0.5784) < 5e-5 and abs(v["p_fisher"]["aplicada"] - 0.1879) < 5e-5   # Fisher: 0,5784 (principal) e 0,1879 (sensibilidade), como no paper v0.3
    assert "p = 0,19" in (FONTES / "paper_v0.1.md").read_text(encoding="utf-8")


def test_fig11_circulacao_parlamento():
    """Fig. 11: 14/56/148/2 falas (v2) e 23/161/692/4 (v1) em 258.011; fonte primaria 1/49 (literal, principal), 0/49 (sensibilidade), 1/50 e base 2/38 com Wilson; Fisher 0,5784 e 0,1879."""
    _chk_fig11(_v()["fig11"])


LADO = {"DIREITA": "Direita", "DIREITA+METODOLÓGICO": "Direita", "ESQUERDA": "Esquerda", "ESQUERDA+METODOLÓGICO": "Esquerda",
        "AMBAS": "Ambas", "AMBAS (DIREITA no enquadramento; pares na independência)": "Ambas", "METODOLÓGICO": "Metodológico"}
COR_PRIOR = {"P1": "#0f5e5a", "P2": "#6fc1b8", "P3": "#dcf1ee"}


def _chk_fig12(v: dict) -> None:
    rows = _csv("TRIAGEM.csv")
    assert len(rows) == 33 and {r["flanco"] for r in rows} == set(LADO)    # mapa de flancos cobre todo valor bruto
    cl = v["clusters"]
    assert sorted(cl) == sorted(r["cluster"] for r in rows) and len(cl) == 33
    for r in rows:
        assert cl[r["cluster"]] == [LADO[r["flanco"]], r["decisão"], COR_PRIOR[r["prioridade"]]], r["cluster"]
    por_lado = {l: sum(1 for x in cl.values() if x[0] == l) for l in ("Direita", "Esquerda", "Ambas", "Metodológico")}
    assert por_lado == {"Direita": 7, "Esquerda": 6, "Ambas": 10, "Metodológico": 10}
    por_dec = {d: sum(1 for x in cl.values() if x[1] == d) for d in {x[1] for x in cl.values()}}
    assert por_dec == {"ACEITO-CORRIGIR": 15, "PARCIAL": 9, "VERIFICAR-ANALISE": 7, "ACEITO-LIMITAÇÃO": 1, "REJEITADO": 1}


def test_fig12_escrutinio_dois_lados():
    """Fig. 12: os 33 clusters da TRIAGEM.csv por lado (7/6/10/10) e decisao (15/9/7/1/1) e prioridade, posicao lida do desenho."""
    _chk_fig12(_v()["fig12"])


# ---------------------------------------------------------------- Figuras 13 a 19 (rodada 2)
import numpy as np
from scipy.stats import spearmanr


def _chk_fig13(v: dict) -> None:
    md = (FONTES / "triangulacao_pns_sinan.md").read_text(encoding="utf-8")
    c05 = (FONTES / "c05_razao_direta.md").read_text(encoding="utf-8")
    cel = lambda ln: [c.strip() for c in ln.strip().strip("|").split("|")]   # noqa: E731
    lin_b = next(cel(x) for x in c05.splitlines() if x.startswith("| (b) só hetero ou LGB+") and "| total |" in x)
    d_pt = float(lin_b[4]); d_lo, d_hi = (float(z) for z in lin_b[7].strip("[]").split(";"))
    mc = {}
    for x in md.splitlines():
        if x.startswith("| A. só respondentes") or x.startswith("| B. denominador antigo"):
            c = cel(x); mc[c[0][0]] = (float(c[1].rstrip("%")), *(float(z) for z in c[2].replace("%", "").split(" a ")))
    sin = {}
    for x in md.splitlines():
        c = cel(x)
        if len(c) == 8 and c[0] in ("2023", "2024"):
            sin[int(c[0])] = (float(c[3].rstrip("%")), float(c[6].rstrip("%")), float(c[7].rstrip("%")))
    pts, ic = v["pontos"], v["ic"]
    assert _perto(pts[0], d_pt) and _perto(ic[0][0], d_lo) and _perto(ic[0][1], d_hi)
    assert _perto(pts[1], mc["A"][0]) and _perto(ic[1][0], mc["A"][1]) and _perto(ic[1][1], mc["A"][2])
    assert _perto(pts[2], mc["B"][0]) and _perto(ic[2][0], mc["B"][1]) and _perto(ic[2][1], mc["B"][2])
    for k, ano in ((3, 2023), (4, 2024)):
        assert _perto(pts[k], sin[ano][0]) and _perto(ic[k][0], sin[ano][1]) and _perto(ic[k][1], sin[ano][2]), ano
    assert (round(pts[0], 2), round(pts[3], 2), round(pts[4], 2)) == (7.12, 4.12, 4.08)
    assert _perto(v["lgb_pop"], float(re.search(r"lgb ([\d.]+) \(", md).group(1)))
    lin = list(csv.DictReader(open(FONTES / "triangulacao_pns_sinan.csv", encoding="utf-8")))   # o CSV do Sinan confere com o .md
    assert [float(r["pct_lgb_entre_validas_sinan"]) for r in lin] == [pts[3], pts[4]]


def test_fig13_pns_sinan():
    """Fig. 13: parcela LGB+ entre vitimas: PNS direto 7,12 [5,11-9,13], simulacoes 7,13 e 6,90, Sinan 4,12 e 4,08 (pior 3,1 e melhor 27)."""
    _chk_fig13(_v()["fig13"])


def _uf2024() -> dict:
    sin = {r["uf"]: int(r["m_lgbtfobia"]) for r in _csv("serie_campo55_uf_ano.csv") if r["ano"] == "2024" and r["uf"] != "BR"}
    bo = {r["uf"]: int(r["registros"]) for r in _csv("anuario_lgbtfobia_uf_ano_v2.csv")
          if r["edicao"] == "2026" and r["ano_dado"] == "2024" and r["uf"] != "BR" and r["registros"].strip()}
    return {u: (sin[u], bo[u]) for u in bo}


def _chk_fig14(v: dict) -> None:
    d = _uf2024()
    assert sorted(v["ufs"]) == sorted(d) and len(d) == 23
    for u, x, y in zip(v["ufs"], v["sinan"], v["bo"]):
        assert (x, y) == tuple(float(z) for z in d[u]), u
    rho = spearmanr([a for a, _ in d.values()], [b for _, b in d.values()])[0]
    s0 = {int(r["ano"]): r for r in _csv("concordancia_v2.csv") if r["especificacao"].startswith("S0 principal")}
    assert abs(rho - float(s0[2024]["rho_contagens"])) < 0.006        # a dispersao reproduz o rho de contagens publicado (0,59)
    assert v["anos"] == [2022, 2023, 2024, 2025]
    for i, ano in enumerate(v["anos"]):
        r_ = s0[ano]
        assert _perto(v["rho_contagens"][i], float(r_["rho_contagens"])) and _perto(v["rho_tamanho"][i], float(r_["rho_so_tamanho"]))
        assert _perto(v["rho_parcial"][i], float(r_["rho_parcial"])) and _perto(v["ic_parcial"][i][0], float(r_["ic_parcial_lo"]))
        assert _perto(v["ic_parcial"][i][1], float(r_["ic_parcial_hi"])) and v["ic_parcial"][i][0] < 0 < v["ic_parcial"][i][1]


def test_fig14_concordancia_por_uf():
    """Fig. 14: 23 UFs (Sinan x Anuario 2024) com rho de contagens 0,59; correlacao bruta, so-tamanho e parcial por ano == concordancia_v2.csv."""
    _chk_fig14(_v()["fig14"])


def _chk_fig15(v: dict) -> None:
    rs = [r for r in _csv("painel_uf_ano_tse_brc.csv") if r["ideologia"] and r["tx_total"]]
    n = len(rs)
    assert v["n"] == n == len(v["x"]) == len(v["y"])
    uf = np.array([r["uf"] for r in rs]); ano = np.array([r["ano"] for r in rs])
    x = np.array([float(r["ideologia"]) for r in rs]); y = np.log([float(r["tx_total"]) for r in rs])

    def desc(z):  # projecoes alternadas nos efeitos de UF e de ano ate convergir (metodo diferente do lstsq com dummies)
        z = z.copy()
        for _ in range(500):
            for g in (uf, ano):
                for k in np.unique(g):
                    z[g == k] -= z[g == k].mean()
        return z
    rx, ry = desc(x), desc(y)
    b = float((rx @ ry) / (rx @ rx))
    assert abs(b - v["inclinacao"]) < 1e-6
    assert np.allclose(sorted(v["x"]), sorted(rx), atol=1e-6) and np.allclose(sorted(v["y"]), sorted(100 * np.expm1(ry)), atol=1e-4)
    c02 = {(r["grupo"], r["desfecho"]): float(r["b"]) for r in _csv("c02_indet_resultados.csv")}
    assert abs(b - c02[("total", "registrado_ln")]) < 5e-4              # a reta e o b do painel publicado
    assert abs(v["reta_y"][1] - v["reta_y"][0]) < 1.0                   # reta plana: variacao < 1 p.p. em toda a faixa


def test_fig15_ideologia_taxa_residuos():
    """Fig. 15: 351 UF-anos, residuos de ideologia e log da taxa depois de efeitos de UF e ano; inclinacao 0,0009 == b do painel (c02)."""
    _chk_fig15(_v()["fig15"])


def _chk_fig16(v: dict) -> None:
    ano = lambda arq, col, filtro=lambda r: True: sorted({int(r[col]) for r in _csv(arq) if filtro(r) and r[col]})   # noqa: E731
    esperado = {"SIM (óbitos)": ano("asr_brasil.csv", "ano", lambda r: r["grupo"] == "Brasil"),
                "Sinan (saúde)": ano("serie_campo55_uf_ano.csv", "ano"),
                "Anuário (polícia)": ano("anuario_lgbtfobia_uf_ano_v2.csv", "ano_dado"),
                "GGB": ano("serie_ggb_vs_cobertura.csv", "ano", lambda r: r["ggb"] != ""),
                "PNS (IBGE)": [2019]}
    assert v["fontes"] == list(esperado)
    for f, a in esperado.items():
        assert v["anos"][f] == [a[0], a[-1]], f
    assert v["anos"]["SIM (óbitos)"] == [2010, 2024] and v["anos"]["Sinan (saúde)"] == [2015, 2025] and v["anos"]["Anuário (polícia)"] == [2022, 2025]
    corpo = " ".join((FONTES / "paper_v0.1.md").read_text(encoding="utf-8").split())
    for r in _csv("cobertura_fontes.tsv") if False else list(csv.DictReader(open(FONTES / "cobertura_fontes.tsv", encoding="utf-8"), delimiter="\t")):
        assert " ".join(r["ancora_verbatim"].split()) in corpo, r["fonte"]     # o que a fonte nao mede tem trecho literal do paper


def test_fig16_linha_do_tempo():
    """Fig. 16: anos de cada fonte lidos dos CSVs (SIM 2010-24, Sinan 2015-25, Anuario 2022-25, GGB 2000-25, PNS 2019) e trechos literais."""
    _chk_fig16(_v()["fig16"])


def _chk_fig17(v: dict) -> None:
    cap = [r for r in _csv("capacidade_por_opcao.csv") if r["indicador"] == "fisica"]
    por = {r["opcao"][:2]: r for r in cap}
    need = next(r for r in _csv("cenarios_n_custo.csv") if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["deff_base"] == "deff medido")
    esp = [(int(por["B'"]["adultos"]), float(por["B'"]["mde_deff_medido"])), (int(por["B:"]["adultos"]), float(por["B:"]["mde_deff_medido"])),
           (int(por["A:"]["adultos"]), float(por["A:"]["mde_deff_medido"])), (int(need["adultos_a_triar"]), 0.30)]
    assert [round(a * 1000) for a in v["adultos_mil"]] == [n for n, _ in esp]
    assert v["mde"] == [m for _, m in esp]
    # v0.3 (frente R, 2026-10-24): PNS 2019 OBSERVADA = 1.554 LGB+ (detecta 60,7%, antes 58,3% com 1.674 esperados); +30% = 305.955 (arredondamento único)
    assert [n for n, _ in esp] == [88531, 114278, 275573, 305955] and [m for _, m in esp][:3] == [0.607, 0.507, 0.317]
    deff = float(next(r for r in _csv("n_necessario.csv") if r["indicador"] == "fisica" and r["mudanca_rel"] == "0.3" and r["sobreamostra_k"] == "1")["deff_lgb"])
    assert round(v["deff"], 1) == round(deff, 1) == 5.1


def test_fig17_tamanho_de_survey():
    """Fig. 17: 88.531 (PNS 2019, 1.554 LGB+, detecta 60,7%), 114.278, 275.573 (31,7%) e 305.955 adultos para +30%; efeito de desenho 5,1."""
    _chk_fig17(_v()["fig17"])


def _chk_fig18(v: dict) -> None:
    br_ = [r for r in _csv("serie_campo55_uf_ano.csv") if r["uf"] == "BR"]
    assert v["anos"] == [int(r["ano"]) for r in br_] == list(range(2015, 2026))
    for i, r in enumerate(br_):
        n = int(r["n_interpessoal"])
        for chave, col in (("ign", "m_ign_branco"), ("na", "m_nao_se_aplica"), ("lgbt", "m_lgbtfobia")):   # o CSV guarda a % com 2 casas
            assert abs(v[chave][i] - 100 * int(r[col]) / n) < 0.006, (chave, r["ano"])
        assert abs(v["ign"][i] + v["na"][i] + v["outros"][i] + v["lgbt"][i] - 100) < 1e-9        # cada coluna soma 100%
    assert np.allclose(v["lgbt_linha"], v["lgbt"], atol=1e-9) and max(v["lgbt"]) < 0.6 and min(v["lgbt"]) > 0.3 and 27 < v["ign"][-1] < 31


def test_fig18_motivacao_sinan():
    """Fig. 18: motivo ignorado/em branco (38% em 2015, 30% em 2025), nao se aplica, outros e LGBTfobia (0,38% a 0,54%) somam 100% por ano."""
    _chk_fig18(_v()["fig18"])


def _chk_fig19(v: dict) -> None:
    rs = list(csv.DictReader(open(FONTES / "uf_2019.csv", encoding="utf-8")))
    assert v["ufs"] == [r["uf"] for r in rs] and len(rs) == 27
    assert v["homicidio"] == [float(r["hom_taxa_100mil"]) for r in rs] and v["internet"] == [float(r["internet_dom_pct"]) for r in rs]
    assert v["ggb_por_milhao"] == [float(r["ggb_por_milhao"]) for r in rs]
    js = json.loads((FONTES / "inflacao_uf_serie.json").read_text(encoding="utf-8"))
    rho_h = spearmanr(v["ggb_por_milhao"], v["homicidio"])[0]
    rho_i = spearmanr(v["ggb_por_milhao"], v["internet"])[0]
    assert abs(rho_h - v["rho_hom"]) < 2e-3 and abs(rho_i - v["rho_internet"]) < 2e-3          # recalculado dos dados == o que o arquivo e a figura trazem
    assert v["rho_hom"] == js["spearman"]["ggb_por_milhao ~ hom_taxa_100mil"]["rho"] == 0.387
    assert v["rho_internet"] == js["spearman"]["ggb_por_milhao ~ internet_dom_pct"]["rho"] == -0.43
    p1, p2, p3 = js["poisson_ggb ~ homicidio"], js["poisson_ggb ~ internet"], js["poisson_ggb ~ internet + homicidio"]
    assert v["irr_so_homicidio"] == p1["irr_por_dp"][0] == 1.35 and p1["ic95_irr"][0] == [1.23, 1.48]      # modelo so com homicidio
    assert v["irr_hom_com_internet"] == p3["irr_por_dp"][1] == 1.332 and p3["ic95_irr"][1] == [1.13, 1.57]   # homicidio com internet no modelo (README: 1,33)
    assert v["irr_internet_sozinha"] == p2["irr_por_dp"][0] == 0.78 and p2["ic95_irr"][0] == [0.68, 0.89]
    assert v["irr_internet_com_hom"] == p3["irr_por_dp"][0] == 0.979 and p3["ic95_irr"][0][0] < 1 < p3["ic95_irr"][0][1]   # internet some: IC inclui 1


def test_fig19_ggb_homicidio_uf():
    """Fig. 19: 27 UFs, rho 0,39 (homicidio) e -0,43 (internet) recalculados; IRR 1,35 so homicidio, 1,33 com internet; internet 0,78 sozinha e 0,98 (IC inclui 1) com homicidio."""
    _chk_fig19(_v()["fig19"])



# ---------------------------------------------------------------- Figuras 20 e 21 (C09: troca de presidente)
class _Pulo(Exception):
    """Teste pulado (pasta de origem fora do repositorio nao existe nesta maquina)."""


def _pula(msg: str) -> None:
    try:
        import pytest
    except ImportError:
        raise _Pulo(msg)
    pytest.skip(msg)


def _sha_sem_home(p: Path) -> str:
    """sha256 do texto com o prefixo de home dos caminhos removido (as copias em fontes/ nao carregam caminho de home)."""
    return hashlib.sha256(p.read_bytes().replace(b"/" + b"Users" + b"/ulissesflores/", b"")).hexdigest()


def _origem(env: str, pasta: str) -> Path:
    """Pasta de trabalho fora do repo: variavel de ambiente `env` ou ~/m4/pesquisas/lgbt-indicador-violencia/<pasta> (home deduzida da posicao do repo)."""
    if os.environ.get(env):
        return Path(os.environ[env])
    return PRIVADO.parents[1] / "m4" / "pesquisas" / "lgbt-indicador-violencia" / pasta


C09_ORIGEM = _origem("LGBT_C09_ORIGEM", "research-2026-10-24-presidencia")
C10_ORIGEM = _origem("LGBT_C10_ORIGEM", "research-2026-10-24-exposicao")


def test_c09_copias_iguais_a_origem_quando_disponivel():
    """As tres copias da C09 em fontes/ batem com a pasta de trabalho (se ela existir nesta maquina)."""
    if not C09_ORIGEM.exists():
        _pula(f"pasta de origem da C09 ausente (defina LGBT_C09_ORIGEM): {C09_ORIGEM.name}")
    for a in ("c09_d1_resultados.csv", "c09_d2_resultados.csv", "RELATORIO-C09.md"):
        assert _sha_sem_home(FONTES / a) == _sha_sem_home(C09_ORIGEM / a), a


def _chk_fig20(v: dict) -> None:
    ser = {d: {int(r["ano"]): float(r["taxa_padronizada"]) for r in _csv("asr_brasil.csv") if r["grupo"] == "Brasil" and r["desfecho"] == d}
           for d in ("agressao", "agressao+indet")}
    assert v["anos"] == list(range(2010, 2025))
    assert v["agressao"] == [ser["agressao"][a] for a in v["anos"]] and v["agressao_indet"] == [ser["agressao+indet"][a] for a in v["anos"]]
    d1 = {int(r["quebra"]): r for r in _csv("c09_d1_resultados.csv") if r["serie"] == "Brasil" and r["desfecho"] == "agressao"}
    assert v["quebras"] == [2016, 2016, 2019, 2019, 2023, 2023] and v["tipos"] == ["troca", "placebo"] * 3
    for k, t in enumerate((2016, 2019, 2023)):
        r = d1[t]
        for j, pre in ((2 * k, ""), (2 * k + 1, "placebo_")):
            assert _perto(v["pontos"][j], float(r[pre + "pct"])) and _perto(v["ic"][j][0], float(r[pre + "pct_lo"]))
            assert _perto(v["ic"][j][1], float(r[pre + "pct_hi"]))
            L = float(r[pre + "L"])
            assert abs(float(r[pre + "pct"]) - 100 * math.expm1(L)) < 1e-6          # pct = 100[exp(L)-1], recalculado
        assert _perto(v["mde"][k][0], float(r["mde_neg"])) and _perto(v["mde"][k][1], float(r["mde_pos"]))
    p = v["pontos"]
    assert (round(p[2], 1), round(p[3], 1)) == (-17.0, -21.8) and p[3] < p[2]         # o placebo de 2018 cai mais que a troca de 2019
    assert d1[2019]["leitura"].startswith("não atribuível à troca") and d1[2016]["leitura"] == d1[2023]["leitura"] == "não distinguível de zero"
    rel = " ".join((FONTES / "RELATORIO-C09.md").read_text(encoding="utf-8").split())
    assert "o placebo de 2018 dispara com o mesmo sinal" in rel and "−17,0% [−29,5; −2,4]" in rel and "−21,8% [−37,4; −2,4]" in rel


def test_fig20_serie_nacional_trocas():
    """Fig. 20: serie nacional 2010-24 (asr_brasil) e quebras 2016/2019/2023 com placebo (c09_d1): 2019 -17,0%, placebo 2018 -21,8%."""
    _chk_fig20(_v()["fig20"])


def _chk_fig21(v: dict) -> None:
    todas = _csv("c09_d2_resultados.csv")
    assert v["n_estimativas"] == len(todas) == 21 and v["n_distinguiveis"] == 0 and all(r["distinguivel"] == "False" and float(r["p"]) > 0.05 for r in todas)
    log = {(r["analise"], r["grupo"]): r for r in todas if r["escala"] == "log"}
    assert len(v["linhas"]) == len(log) == 16
    for k, lin in enumerate(v["linhas"]):
        r = log[tuple(lin.split("|"))]
        b_, K = float(r["b"]), float(r["K"])
        assert _perto(v["pontos"][k], 100 * math.expm1(b_ * K), 1e-9)
        assert _perto(v["ic"][k][0], float(r["ef_lo"])) and _perto(v["ic"][k][1], float(r["ef_hi"]))
        assert abs(float(r["ef_lo"]) - 100 * math.expm1(float(r["lo"]) * K)) < 1e-6 and abs(float(r["ef_hi"]) - 100 * math.expm1(float(r["hi"]) * K)) < 1e-6
        assert _perto(v["mde"][k][0], float(r["mde_neg"])) and _perto(v["mde"][k][1], float(r["mde_pos"]))
        assert v["ic"][k][0] < 0 < v["ic"][k][1]                                       # toda faixa inclui zero
    i = v["linhas"].index("primaria|total")
    assert (round(v["ic"][i][0], 1), round(v["ic"][i][1], 1)) == (-18.3, 9.6) and (round(v["mde"][i][0], 1), round(v["mde"][i][1], 1)) == (-18.9, 23.3)
    rel = " ".join((FONTES / "RELATORIO-C09.md").read_text(encoding="utf-8").split())
    assert "Nenhuma das 21 estimativas do painel" in rel and "−18,3% e +9,6%" in rel


def test_fig21_alinhamento_governador_presidente():
    """Fig. 21: 16 analises em % (21 estimativas no total, nenhuma distinguivel de zero); principal -18,3% a +9,6%, MDE -18,9% / +23,3%."""
    _chk_fig21(_v()["fig21"])


# ---------------------------------------------------------------- Figuras 22 e 23 (C10: exposicao por governo)
def test_c10_copias_iguais_a_origem_quando_disponivel():
    """As cinco copias da C10 em fontes/ batem com a pasta de trabalho (pulado se ela nao existir nesta maquina)."""
    if not C10_ORIGEM.exists():
        _pula(f"pasta de origem da C10 ausente (defina LGBT_C10_ORIGEM): {C10_ORIGEM.name}")
    for a in ("c10_e1_federal.csv", "c10_e1_serie_longo.csv", "c10_e2_trocas_longo.csv", "c10_e2_resumo.csv", "RELATORIO-EXPOSICAO.md"):
        assert _sha_sem_home(FONTES / a) == _sha_sem_home(C10_ORIGEM / a), a


def _chk_fig22(v: dict) -> None:
    sl = [r for r in _csv("c10_e1_serie_longo.csv") if r["serie"] == "Brasil"]
    ag = {int(r["ano"]): float(r["taxa_padronizada"]) for r in sl if r["desfecho"] == "agressao"}
    ai = {int(r["ano"]): float(r["taxa_padronizada"]) for r in sl if r["desfecho"] == "agressao+indet"}
    assert v["anos"] == list(range(2010, 2025)) and v["agressao"] == [ag[a] for a in v["anos"]] and v["agressao_indet"] == [ai[a] for a in v["anos"]]
    asr = {(r["desfecho"], int(r["ano"])): float(r["taxa_padronizada"]) for r in _csv("asr_brasil.csv") if r["grupo"] == "Brasil"}
    assert all(abs(round(ag[a], 2) - asr[("agressao", a)]) < 0.0051 for a in ag)          # a serie da C10 e a do asr_brasil
    e1 = {(r["governo"], r["desfecho"]): r for r in _csv("c10_e1_federal.csv") if r["serie"] == "Brasil" and r["taxa_base"] != ""}
    esperado = []
    for g in ("Dilma Rousseff", "Michel Temer", "Jair Bolsonaro", "Luiz Inácio Lula da Silva"):
        esperado += [(g, "agressao"), (g, "agressao+indet")] + ([(g, "pre")] if e1[(g, "agressao")]["pre_var_pct"] != "" else [])
    assert list(zip(v["governos"], v["tipos"])) == esperado
    for k, (g, tipo) in enumerate(esperado):
        r = e1[(g, tipo if tipo != "pre" else "agressao")]
        if tipo == "pre":
            assert _perto(v["pontos"][k], float(r["pre_var_pct"])) and v["ic"][k] is None
            continue
        tb, tf = float(r["taxa_base"]), float(r["taxa_fim"])
        assert abs(float(r["var_pct"]) - 100 * (tf / tb - 1)) < 1e-6                      # var % recalculada das taxas
        assert _perto(v["pontos"][k], float(r["var_pct"])) and _perto(v["ic"][k][0], float(r["var_pct_lo"])) and _perto(v["ic"][k][1], float(r["var_pct_hi"]))
    assert abs(ag[2018] - float(e1[("Jair Bolsonaro", "agressao")]["taxa_base"])) < 1e-9 and abs(ag[2022] - float(e1[("Jair Bolsonaro", "agressao")]["taxa_fim"])) < 1e-9
    bol = [p for (g, t_), p in zip(esperado, v["pontos"]) if g == "Jair Bolsonaro"]
    assert (round(bol[0], 1), round(bol[1], 1)) == (-21.0, -13.7)
    assert v["limites"]["Temer"][0] == 2015.5 + 0.361 and "Dilma Rousseff 0.361" in [x["governo_fracao_do_ano"] for x in sl if x["ano"] == "2016"][0]
    rel = " ".join((FONTES / "RELATORIO-EXPOSICAO.md").read_text(encoding="utf-8").split())
    assert "−21,0% [−22,0; −20,0]" in rel and "A queda começou em 2018, ainda com Temer. Isso não é prova de causa." in rel


def test_fig22_taxa_nacional_por_governo():
    """Fig. 22: serie nacional e variacao por governo (Dilma +11,1%, Temer -4,2%, Bolsonaro -21,0%/-13,7% com indeterminada, Lula -10,6%) == c10_e1."""
    _chk_fig22(_v()["fig22"])


def _chk_fig23(v: dict) -> None:
    tr = _csv("c10_e2_trocas_longo.csv")
    res = {(r["recorte"], r["direcao"], r["grupo"]): r for r in _csv("c10_e2_resumo.csv")}
    esperado = {}
    for grupo, dirs in (("total", ["todas", "bloco: esquerda->direita", "bloco: direita->esquerda", "bloco: envolve centro", "bloco: mesmo bloco"]), ):
        for d in dirs:
            esperado[f"{grupo}|{d}"] = (grupo, d)
    esperado["total|todas_b"] = ("total", "todas")
    esperado["total_agr_indet|todas_b"] = ("total_agr_indet", "todas")
    assert sorted(v["linhas"]) == sorted(esperado)
    for chave, (grupo, d) in esperado.items():
        xs = sorted(float(r["excesso_rel_pct"]) for r in tr if r["grupo"] == grupo and (d == "todas" or "bloco: " + r["direcao_bloco"] == d))
        L = v["linhas"][chave]
        rr = res[("P_todas_67", d, grupo)]
        assert len(L["x"]) == int(rr["n"]) and np.allclose(sorted(L["x"]), xs, atol=1e-9), chave
        assert abs(float(np.median(xs)) - L["mediana"]) < 1e-6 and abs(L["mediana"] - float(rr["mediana_pct"])) < 1e-6, chave      # mediana recalculada
        assert L["n_subiu"] == int(rr["n_subiu"]) == sum(1 for x in xs if x > 0) and L["n_caiu"] == int(rr["n_caiu"]) == sum(1 for x in xs if x <= 0), chave
        assert _perto(L["ref"][0], float(rr["ref_mediana_p2_5"])) and _perto(L["ref"][1], float(rr["ref_mediana_p97_5"])), chave
    assert (v["linhas"]["total|todas"]["n_subiu"], v["linhas"]["total|todas"]["n_caiu"]) == (31, 36)
    assert (v["linhas"]["total_agr_indet|todas_b"]["n_subiu"], v["linhas"]["total_agr_indet|todas_b"]["n_caiu"]) == (34, 33)
    assert v["linhas"]["total_agr_indet|todas_b"]["ref"][0] < v["linhas"]["total_agr_indet|todas_b"]["mediana"] < v["linhas"]["total_agr_indet|todas_b"]["ref"][1]   # indeterminada: dentro da faixa
    rel = " ".join((FONTES / "RELATORIO-EXPOSICAO.md").read_text(encoding="utf-8").split())
    assert "31 subiram e 36 caíram" in rel and "34 subiram e 33 caíram" in rel and "3 a 15 UFs por ano" in rel


def test_fig23_trocas_de_governador_exposicao():
    """Fig. 23: 67 trocas (31 subiram, 36 cairam, mediana -0,7%) por direcao, referencia sem troca; com indeterminada 34/33 e mediana dentro da faixa."""
    _chk_fig23(_v()["fig23"])


# ---------------------------------------------------------------- Figuras 24 a 27 (guia de leitura, mortalidade, GGB)
V03_ORIGEM = _origem("LGBT_V03_ORIGEM", "research-2026-10-24-v03")


def test_v03_copias_iguais_a_origem_quando_disponivel():
    """As copias da frente L em fontes/ batem com a pasta de trabalho (pulado se ela nao existir nesta maquina)."""
    if not V03_ORIGEM.exists():
        _pula(f"pasta de origem da v0.3 ausente (defina LGBT_V03_ORIGEM): {V03_ORIGEM.name}")
    for a in ("L-RELATORIO.md", "L-SECAO-3-3-PROPOSTA.md"):
        assert _sha_sem_home(FONTES / a) == _sha_sem_home(V03_ORIGEM / a), a


def _chk_fig24(v: dict) -> None:
    n = v["numeros"]
    p = {(r["bloco"], r["rotulo"]): r for r in _csv("seguro_pns2019.csv")}[("nivel", "física")]
    assert _perto(n["pns"][0], 100 * float(p["prev_grupo"])) and _perto(n["pns"][1], 100 * float(p["prev_ref"]))
    br_ = {int(r["ano"]): float(r["pct_m_ign"]) + float(r["pct_m_na"]) for r in _csv("serie_campo55_uf_ano.csv") if r["uf"] == "BR"}
    assert _perto(n["campo55"][0], br_[2015]) and _perto(n["campo55"][1], min(br_[a] for a in (2023, 2024, 2025))) and _perto(n["campo55"][2], max(br_[a] for a in (2023, 2024, 2025)))
    assert (round(n["campo55"][0]), round(n["campo55"][1]), round(n["campo55"][2])) == (53, 42, 44)        # paper: 53% -> 42% a 45%
    anu = {(r["edicao"], r["ano_dado"]): int(r["registros"]) for r in _csv("anuario_lgbtfobia_uf_ano_v2.csv") if r["uf"] == "BR" and r["registros"]}
    assert n["bo"] == [anu[("2024", "2022")], anu[("2026", "2025")]] == [783, 3481]
    ggb = {int(r["ano"]): int(r["ggb"]) for r in _csv("serie_ggb_vs_cobertura.csv") if r["ggb"]}
    assert n["ggb"] == [ggb[2023], ggb[2024], ggb[2025]] == [257, 291, 257]
    assert sorted(v["faixas"]) == sorted(["PNS", "Sinan", "BO (Anuário)", "Disque 100", "SIM", "GGB e ANTRA"])
    assert v["faixas"]["SIM"] == "sem número de LGBT+" and "falso" not in " ".join(v["faixas"].values())


def test_fig24_caminho_do_dado():
    """Fig. 24: numeros do esquema (14,70% x 3,82%; 53% -> 42-44% sem motivo; 783 -> 3.481; 257/291/257) lidos dos arquivos; SIM sem numero."""
    _chk_fig24(_v()["fig24"])


def _chk_fig25(v: dict) -> None:
    E = {r["id"]: r for r in _csv("estudos_mortalidade.tsv", "\t")}
    corpo = " ".join((FONTES / "L-SECAO-3-3-PROPOSTA.md").read_text(encoding="utf-8").split())
    for k, r in E.items():
        assert " ".join(r["ancora_verbatim"].split()) in corpo, k                  # cada numero tem trecho literal da proposta da frente L
        assert "falso" not in r["ancora_verbatim"]
    P = v["paineis"]
    assert sorted(P) == sorted(["ONS 2026", "ONS 2025", "McKetta 2024", "Erlangsen 2023", "Luis 2026", "Zachry 2025", "McLellan 2026"])
    f = lambda k, c="valor": float(E[k][c])   # noqa: E731
    for (pt, ic), k in zip(P["ONS 2026"], ("ons26_lgb", "ons26_gl", "ons26_bi", "ons26_gayh")):
        assert _perto(pt, f(k)) and _perto(ic[0], f(k, "lo")) and _perto(ic[1], f(k, "hi")), k
    assert [round(x[0], 2) for x in P["ONS 2026"]] == [1.31, 1.31, 1.33, 1.23]
    assert _perto(P["ONS 2025"][0], f("ons25_sui_lgb")) and _perto(P["ONS 2025"][1], f("ons25_sui_het"))
    assert _perto(P["McKetta 2024"][0][0], f("mck24")) and _perto(P["McKetta 2024"][0][1][0], f("mck24", "lo")) and _perto(P["McKetta 2024"][0][1][1], f("mck24", "hi"))
    for (pt, ic), k in zip(P["Erlangsen 2023"], ("erl23_todas", "erl23_sui")):
        assert _perto(pt, f(k)) and _perto(ic[0], f(k, "lo")) and _perto(ic[1], f(k, "hi")), k
    assert _perto(P["Luis 2026"][0], f("luis26_violentos")) and _perto(sum(P["Luis 2026"]), f("luis26_pareados"))
    assert P["Zachry 2025"] == [f("zach25_pleno"), f("zach25_parcial"), f("zach25_nenhum")] and sum(P["Zachry 2025"]) == f("zach25_estudos") == 43
    (pt, ic), hom = P["McLellan 2026"]
    assert _perto(pt, f("mcl26_violencia")) and _perto(ic[0], f("mcl26_violencia", "lo")) and _perto(ic[1], f("mcl26_violencia", "hi")) and hom == 0
    assert round(100 * P["Luis 2026"][0] / sum(P["Luis 2026"]), 1) == 42.5                  # os 42,5% sao dos obitos pareados, nao das notificacoes


def test_fig25_mortalidade_internacional():
    """Fig. 25: 7 estudos, cada numero com trecho literal da proposta da frente L (ONS 1,31 [1,28-1,33]; 1,23 homens gays; Zachry 14/28/1; Luis 563/1.325...)."""
    _chk_fig25(_v()["fig25"])


def _chk_fig26(v: dict) -> None:
    js = json.loads((FONTES / "ggb_validacao_resumo.json").read_text(encoding="utf-8"))
    cod = list(csv.DictReader(open(PRIVADO / "research-2026-10-21-rodada3" / "F3-ggb" / "dados" / "codificacao_A.csv", encoding="utf-8")))   # a lista por caso fica no repo, nao na figura
    rec = [r for r in cod if r["fonte"] == "R"]
    corr = [r for r in rec if r["corresp"] in ("S", "P")]
    mv = [r for r in corr if r["morte"] == "S"]
    estr = [r for r in mv if r["lgbt"] == "S"]
    assert v["etapas"] == [float(x) for x in (len(cod), len(rec), len(corr), len(mv), len(estr))] == [160.0, 106.0, 88.0, 73.0, 50.0]
    assert v["etapas"] == [float(js[k]) for k in ("n_amostra", "recuperadas", "correspondem", "morte_violenta", "verificavel_estrito")]
    mot = {k: float(sum(1 for r in mv if r["motivo"] == k)) for k in ("U", "C", "R", "P", "S", "V")}
    assert v["motivos"] == mot == {"U": 35.0, "C": 13.0, "R": 13.0, "P": 6.0, "S": 3.0, "V": 3.0}
    assert sum(v["motivos"].values()) == v["etapas"][3]
    assert 100 * 50 / 160 == 31.25 and _br(100 * 50 / 160) == "31,3" and f"{100 * 50 / 160:.1f}" == "31.2"     # o teste trava o meio-para-cima (o Python puro daria 31,2)
    svg = (FIG / "fig26_ggb_verificabilidade.svg").read_text(encoding="utf-8")
    assert "50 (31,3%)" in svg and "31,2%" not in svg                                                         # o titulo desenhado concorda com o paper (31,3%)
    assert "31,3%" in " ".join((FONTES / "paper_v0.1.md").read_text(encoding="utf-8").split())
    assert js["motivo_nao_recuperacao"] == {"link_morto_404": 31, "dominio_inacessivel": 12, "bloqueio_ou_erro_servidor": 4, "sem_link_no_anexo4": 7}


def test_fig26_ggb_verificabilidade():
    """Fig. 26: 160 -> 106 -> 88 -> 73 -> 50 e motivos (35 desconhecido, 13, 13, 6, 3, 3 LGBTfobia) recontados da lista por caso; sem identificador de vitima."""
    _chk_fig26(_v()["fig26"])


def _chk_fig27(v: dict) -> None:
    rows = [r for r in _csv("c08_numeradores.csv") if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False"]
    assert sorted(v["curvas"]) == sorted(f"{r['ano']}|{r['numerador']}" for r in rows) and len(rows) == 6
    for r in rows:
        k = f"{r['ano']}|{r['numerador']}"
        n, E0 = int(r["n"]), float(r["E_RR1.0"])
        c = v["curvas"][k]
        assert all(_perto(y, 100 * n / (E0 * x), 1e-9) for x, y in zip(c["x"], c["y"])), k
        rr100 = v["rr_cobertura_100"][k]
        assert _perto(rr100, n / E0, 1e-9) and abs(100 * n / (E0 * rr100) - 100) < 1e-9, k       # no RR marcado a cobertura e 100%
        assert _perto(100 * n / (E0 * 1.0), 100 * float(r["cob_RR1.0"]), 1e-9) and _perto(100 * n / (E0 * 2.82) , 100 * float(r["cob_RR2.82"]), 1e-9)
    assert [round(v["rr_cobertura_100"][f"2023|{x}"], 2) for x in ("N0", "N1", "N2")] == [0.23, 0.20, 0.08]
    assert "cenário de subtração" in (FIG / "make_figures.py").read_text(encoding="utf-8")       # N2 e chamado de subtracao, nao de estimativa


def test_fig27_ggb_curva_de_hipoteses():
    """Fig. 27: cobertura N/(E0*RR) recalculada de c08; o RR que da 100% (0,23; 0,20; 0,08 em 2023) so e marcado, nao estimado."""
    _chk_fig27(_v()["fig27"])


def _chk_fig28(v: dict) -> None:
    """Disque 100: serie anual lida do CSV com parser proprio; unidade por ano, porcentagens meio-para-cima, quebras e rotulo de 2026."""
    lin = {(int(r["ano"]), r["recorte"], r["unidade"]): int(r["n"]) for r in _csv("d100_serie_anual.csv")}
    anos = list(range(2011, 2027))
    un = ["linhas" if a <= 2020 else "denuncias" for a in anos]
    assert v["anos"] == anos and v["unidade"] == un
    lg = [lin[(a, "grupo_lgbt", u)] for a, u in zip(anos, un)]
    ca = [lin[(a, "canal", u)] for a, u in zip(anos, un)]
    assert v["lgbt"] == [float(x) for x in lg] and v["canal_mil"] == [x / 1000 for x in ca]
    assert [round(x) for x in v["pct"]] == [round(100 * a / b) for a, b in zip(lg, ca)] and all(_perto(p, 100 * a / b, 1e-9) for p, a, b in zip(v["pct"], lg, ca))
    assert v["pct_texto"] == [_br(100 * a / b) + "%" for a, b in zip(lg, ca)]                                    # meio para cima, nao o arredondamento do banqueiro
    assert v["quebras"] == [2020.0, 2020.5, 2022.5, 2024.0]                                                        # 2020S1, 2020S2, 2022S2 e 2024
    assert lg[:9] == [1592, 4787, 2780, 1795, 1879, 1893, 2203, 1888, 1331] and lg[9] == 3412 and lg[10:] == [1367, 4163, 6173, 8176, 9346, 10461]
    assert (min(lg[:9]), max(lg[:9])) == (1331, 4787) and ca[-3:] == [551693, 637890, 550546]
    assert _br(lg[14] / lg[10]) == "6,8" and _br(ca[14] / ca[10]) == "2,9"                                          # o titulo: 6,8 e 2,9 vezes
    assert [_br(100 * lg[i] / ca[i]) for i in (10, 11, 14, 15)] == ["0,6", "1,4", "1,5", "1,9"]
    svg = (FIG / "fig28_disque100_serie.svg").read_text(encoding="utf-8")
    assert "até setembro" in svg and "2026*" in svg and "não é violência" in svg                                    # 2026 rotulado como parcial
    assert "vítimas únicas não é calculável" in svg and "taxa de vitimização" not in svg
    assert "mais violência" in svg and "aumentou" not in svg.lower().replace("não aumentou", "")                    # nada de "a violencia aumentou"


def test_fig28_disque100_serie():
    """Fig. 28: serie do Disque 100 (1.331-4.787 linhas em 2011-19; 3.412 em 2020; 1.367 a 10.461 denuncias em 2021-26), canal inteiro e fatia LGBT, 4 quebras."""
    _chk_fig28(_v()["fig28"])


def _quebrar(v: dict, fig: str) -> dict:
    """Copia de valores_plotados.json com UM numero da figura trocado (controle negativo)."""
    w = copy.deepcopy(v)[fig]
    if fig == "fig6":
        w["lgb"]["fracoes"][0] = 0.5
    elif fig == "fig7":
        w["celulas"]["L1|N1"]["rotulo_exibido"] = "não testável"
    elif fig == "fig8":
        w["media"][0] += 1.0
    elif fig == "fig9":
        w["ic"][0][1] += 1.0
    elif fig == "fig10":
        w["cenarios"]["S2"]["propensao_pct"][3] += 3.0
    elif fig == "fig11":
        w["v2"][1] = 55.0
    elif fig == "fig12":
        w["clusters"]["C01"][0] = "Direita"
    elif fig == "fig13":
        w["pontos"][3] += 1.0
    elif fig == "fig14":
        w["rho_parcial"][0] += 0.2
    elif fig == "fig15":
        w["inclinacao"] += 0.01
    elif fig == "fig16":
        w["anos"]["SIM (óbitos)"][0] = 2012
    elif fig == "fig17":
        w["adultos_mil"][0] += 5.0
    elif fig == "fig18":
        w["ign"][0] += 1.0
    elif fig == "fig20":
        w["pontos"][3] = -10.0
    elif fig == "fig24":
        w["numeros"]["bo"][1] = 3000
    elif fig == "fig25":
        w["paineis"]["ONS 2026"][0][0] = 1.5
    elif fig == "fig26":
        w["etapas"][4] = 51.0
    elif fig == "fig27":
        w["rr_cobertura_100"]["2023|N0"] = 0.5
    elif fig == "fig28":
        w["lgbt"][-1] += 1000.0
    elif fig == "fig22":
        w["pontos"][5] += 3.0
    elif fig == "fig23":
        w["linhas"]["total|todas"]["n_subiu"] = 30
    elif fig == "fig21":
        w["ic"][0][0] = 1.0
    elif fig == "fig19":
        w["irr_internet_com_hom"] = 0.78
    return w


def test_controle_negativo():
    """Um numero errado em qualquer das figuras 6-28 faz o conferidor reprovar (o teste mede a figura, nao so passa)."""
    chk = {"fig6": _chk_fig6, "fig7": _chk_fig7, "fig8": _chk_fig8, "fig9": _chk_fig9, "fig10": _chk_fig10,
           "fig11": _chk_fig11, "fig12": _chk_fig12, "fig13": _chk_fig13, "fig14": _chk_fig14, "fig15": _chk_fig15, "fig16": _chk_fig16,
           "fig17": _chk_fig17, "fig18": _chk_fig18, "fig19": _chk_fig19, "fig20": _chk_fig20, "fig21": _chk_fig21, "fig22": _chk_fig22, "fig23": _chk_fig23, "fig24": _chk_fig24, "fig25": _chk_fig25, "fig26": _chk_fig26, "fig27": _chk_fig27, "fig28": _chk_fig28}
    v = _v()
    for fig, fn in chk.items():
        fn(v[fig])  # controle positivo: o original passa
        try:
            fn(_quebrar(v, fig))
        except AssertionError:
            continue
        raise AssertionError(f"controle negativo falhou: {fig} corrompida passou")


if __name__ == "__main__":
    ok = 0
    testes = [(k, f) for k, f in sorted(globals().items()) if k.startswith("test_") and callable(f)]
    for nome, fn in testes:
        try:
            fn()
            ok += 1
            print(f"PASS {nome}")
        except AssertionError as e:
            print(f"FAIL {nome}: {e}")
        except _Pulo as e:
            ok += 1
            print(f"SKIP {nome}: {e}")
    print(f"{ok}/{len(testes)} passaram")
    raise SystemExit(0 if ok == len(testes) else 1)
