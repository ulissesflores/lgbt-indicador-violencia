"""Trava os números do C10 (exposição por governo). Pré-registro: PREREGISTRO-C10.md (hash em PREREGISTRO-C10.sha256).
Lê os CSV gerados por c10_estrutura.py e c10_exposicao.py. Tolerâncias = arredondamento do número impresso no RELATORIO-EXPOSICAO.md.
Rodar: /opt/homebrew/bin/python3.14 -B -m pytest -q -p no:cacheprovider tests/   (sem -I: o pytest está no site do usuário)."""
import csv, collections, hashlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1] / "dados" / "exposicao"  # no repositório: tests/ -> dados/exposicao
DADOS = RAIZ.parent


def _csv(p):
    with open(p, encoding="utf-8", newline="") as fh: return list(csv.DictReader(fh))


def _e1(gov, serie, des):
    for r in _csv(RAIZ / "c10_e1_federal.csv"):
        if r["governo"].startswith(gov) and r["serie"] == serie and r["desfecho"] == des: return r
    raise AssertionError((gov, serie, des))


def _e2(rec, dirc, g):
    for r in _csv(RAIZ / "c10_e2_resumo.csv"):
        if r["recorte"] == rec and r["direcao"] == dirc and r["grupo"] == g: return r
    raise AssertionError((rec, dirc, g))


perto = lambda a, b, tol: abs(float(a) - float(b)) <= tol


def test_preregistro_corpo_inalterado():
    b = (RAIZ / "PREREGISTRO-C10.md").read_bytes()
    real = hashlib.sha256(b[:b.index(b"\n---\n\n**ADENDOS")]).hexdigest()
    sha = (RAIZ / "PREREGISTRO-C10.sha256").read_text(encoding="utf-8")
    assert real == sha.split()[0] == "83c4ef0f7e73bce22aaff9097f336b7a57a1438926f9a72709ab1845de496f14"
    assert "# gravado 2026-10-24T20:43:46Z" in sha


def test_contagens_de_trocas():
    t = _csv(RAIZ / "c10_trocas.csv")
    assert len(t) == 67
    assert sum(int(r["janela_completa"]) for r in t) == 47
    assert sum(1 for r in t if r["janela_completa"] == "1" and r["contaminada"] == "0") == 21
    assert sum(1 for r in t if r["ano_troca"] in ("2015", "2019", "2023") and "|" not in r["partido_depois"]) == 45
    assert collections.Counter(r["sentido"] for r in t) == {"direita": 38, "esquerda": 29}
    assert "trocas de onda (mesmo partido, só o escore muda): 27" in (RAIZ / "c10_estrutura.md").read_text(encoding="utf-8")


def test_brasil_e_a_soma_das_27_ufs():
    """Independente do script: população implícita = óbitos do Atlas / taxa do painel; Brasil = soma dos óbitos / soma das populações."""
    pan = _csv(DADOS / "painel" / "painel_uf_ano_tse_brc.csv")
    n = {(r["uf"], int(r["ano"])): float(r["valor"]) for r in _csv(DADOS / "atlas_uf_series.csv") if r["variavel"] == "homicidios_total_n" and r["valor"]}
    num, den = collections.Counter(), collections.Counter()
    for r in pan:
        k = (r["uf"], int(r["ano"])); num[k[1]] += n[k]; den[k[1]] += n[k] / float(r["tx_total"]) * 1e5
    assert all(sum(1 for r in pan if int(r["ano"]) == a) == 27 for a in num)
    nac = {a: num[a] / den[a] * 1e5 for a in num}
    for r in _csv(RAIZ / "c10_e2_trocas_longo.csv"):
        if r["grupo"] != "total": continue
        e = int(r["ano_troca"]); pre = [y for y in range(e - 3, e) if y >= 2012]; pos = [y for y in range(e, e + 3) if y <= 2024]
        assert perto(r["taxa_br_antes"], sum(nac[y] for y in pre) / len(pre), 1e-6)
        assert perto(r["taxa_br_depois"], sum(nac[y] for y in pos) / len(pos), 1e-6)


def test_e1_federal():
    r = _e1("Jair", "Brasil", "agressao")
    assert perto(r["taxa_base"], 27.61, 0.005) and perto(r["taxa_fim"], 21.81, 0.005)
    assert perto(r["var_pct"], -21.0, 0.05) and perto(r["var_pct_lo"], -22.0, 0.05) and perto(r["var_pct_hi"], -20.0, 0.05) and perto(r["pre_var_pct"], -4.2, 0.05)
    assert perto(_e1("Jair", "Brasil", "agressao+indet")["var_pct"], -13.7, 0.05)
    assert perto(_e1("Michel", "Brasil", "agressao")["var_pct"], -4.2, 0.05) and perto(_e1("Michel", "Brasil", "agressao")["pre_var_pct"], 3.4, 0.05)
    assert perto(_e1("Michel", "Brasil", "agressao+indet")["var_pct"], -0.4, 0.05)
    assert perto(_e1("Dilma", "Brasil", "agressao")["var_pct"], 11.1, 0.05) and _e1("Dilma", "Brasil", "agressao")["pre_var_pct"] == ""
    lula3 = [r for r in _csv(RAIZ / "c10_e1_federal.csv") if r["governo"] == "Luiz Inácio Lula da Silva" and r["serie"] == "Brasil" and r["desfecho"] == "agressao"][0]
    assert perto(lula3["var_pct"], -10.6, 0.05) and lula3["em_curso"] == "1"
    lula2 = _e1("Luiz Inácio Lula da Silva (2º", "Brasil", "agressao")
    assert lula2["taxa_base"] == "" and lula2["nota"].startswith("n/d")
    assert perto(_e1("Jair", "Mulheres negras", "agressao")["var_pct"], -22.4, 0.05) and perto(_e1("Jair", "Mulheres negras", "agressao+indet")["var_pct"], -6.1, 0.05)
    assert perto(_e1("Jair", "Arma de fogo", "agressao")["var_pct"], -22.8, 0.05)
    assert perto(_e1("Jair", "Brasil", "agressao")["razao_indet_base"], 18.0, 0.05) and perto(_e1("Jair", "Brasil", "agressao")["razao_indet_fim"], 25.9, 0.05)


def test_e2_estadual():
    r = _e2("P_todas_67", "todas", "total")
    assert (r["n"], r["n_subiu"], r["n_caiu"]) == ("67", "31", "36")
    assert perto(r["mediana_pct"], -0.7, 0.05) and perto(r["p25_pct"], -9.4, 0.05) and perto(r["p75_pct"], 12.1, 0.05)
    assert perto(r["ref_mediana_p2_5"], 0.8, 0.05) and perto(r["ref_mediana_p97_5"], 7.8, 0.05) and perto(r["p_mediana"], 0.016, 0.0005)
    assert perto(r["fracao_subiu"], 0.46, 0.005) and perto(r["p_fracao"], 0.006, 0.0005)
    ai = _e2("P_todas_67", "todas", "total_agr_indet")
    assert (ai["n_subiu"], ai["n_caiu"]) == ("34", "33") and perto(ai["mediana_pct"], 0.5, 0.05) and perto(ai["p_mediana"], 0.538, 0.0005)
    b = _e2("b_completa_nao_contaminada", "todas", "total")
    assert (b["n"], b["n_subiu"], b["n_caiu"]) == ("21", "8", "13") and perto(b["mediana_pct"], -10.2, 0.05)
    c = _e2("c_posse_eleitoral", "todas", "total")
    assert (c["n"], c["n_subiu"], c["n_caiu"]) == ("45", "21", "24") and perto(c["mediana_pct"], -0.8, 0.05) and perto(c["p_mediana"], 0.026, 0.0005)
    for d, n, s, k in (("bloco: esquerda->direita", "12", "8", "4"), ("bloco: direita->esquerda", "8", "5", "3"), ("bloco: envolve centro", "8", "2", "6"), ("bloco: mesmo bloco", "39", "16", "23")):
        x = _e2("P_todas_67", d, "total"); assert (x["n"], x["n_subiu"], x["n_caiu"]) == (n, s, k)
    assert perto(_e2("P_todas_67", "bloco: esquerda->direita", "total")["mediana_pct"], 9.5, 0.05)
    assert perto(_e2("P_todas_67", "bloco: direita->esquerda", "total")["mediana_pct"], 3.5, 0.05)
    assert len(_csv(RAIZ / "c10_e2_resumo.csv")) == 189
