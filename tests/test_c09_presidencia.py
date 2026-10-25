"""Trava os números do C09 (presidência x violência letal). Pré-registro: PREREGISTRO-C09.md (hash em PREREGISTRO-C09.sha256).
Lê os CSV/MD gerados por c09_estrutura.py, c09_d2_painel.py e c09_d1_its.py. Tolerâncias = arredondamento do número impresso no RELATORIO-C09.md.
Rodar: /opt/homebrew/bin/python3.14 -m pytest -q tests/   (sem -I: o pytest está no site do usuário)."""
import csv, hashlib, math
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1] / "dados" / "presidencia"  # no repositório: tests/ -> dados/presidencia


def _csv(nome):
    with open(RAIZ / nome, encoding="utf-8", newline="") as fh: return list(csv.DictReader(fh))


def _d2(analise, grupo="total", desfecho=None):
    for r in _csv("c09_d2_resultados.csv"):
        if r["analise"] == analise and r["grupo"] == grupo and (desfecho is None or r["desfecho"] == desfecho): return r
    raise AssertionError((analise, grupo))


def _d1(serie, desfecho, quebra):
    for r in _csv("c09_d1_resultados.csv"):
        if r["serie"] == serie and r["desfecho"] == desfecho and int(r["quebra"]) == quebra: return r
    raise AssertionError((serie, desfecho, quebra))


perto = lambda a, b, tol: abs(float(a) - float(b)) <= tol


def test_preregistro_corpo_inalterado():
    b = (RAIZ / "PREREGISTRO-C09.md").read_bytes()
    real = hashlib.sha256(b[:b.index(b"\n---\n\n**ADENDOS")]).hexdigest()
    gravado = (RAIZ / "PREREGISTRO-C09.sha256").read_text(encoding="utf-8").split()[0]
    assert real == gravado == "f48b1ee4172ea0870ebdf7b186b338f65c25e28943becb6f7fa828e2a047a41a"
    assert "# gravado 2026-10-24T20:06:38Z" in (RAIZ / "PREREGISTRO-C09.sha256").read_text(encoding="utf-8")


def test_estrutura_citada_no_preregistro():
    s = (RAIZ / "c09_estrutura.md").read_text(encoding="utf-8")
    assert "| 2016 | Dilma (PT) 0.361; Michel (PMDB) 0.639 | 5.5580 |" in s
    assert "| gp | 19.4706 | 8.4619 | 4.9280 |" in s and "2016: 4.25; 2019: 5.68; 2023: 5.16" in s


def test_d2_primaria_nao_distinguivel():
    r = _d2("primaria")
    assert perto(r["b"], -0.00214, 5e-6) and perto(r["se"], 0.00292, 5e-6) and perto(r["p"], 0.459, 5e-4) and r["n"] == "351"
    assert perto(r["K"], 25.681, 5e-4)
    assert perto(r["ef_lo"], -18.3, 0.05) and perto(r["ef_hi"], 9.6, 0.05)          # "entre -18,3% e +9,6%"
    assert perto(r["mde_neg"], -18.9, 0.05) and perto(r["mde_pos"], 23.3, 0.05)
    assert r["distinguivel"] == "False"
    assert "**Veredito da primária (regra pré-registrada): não distinguível de zero.**" in (RAIZ / "c09_d2_resultados.md").read_text(encoding="utf-8")


def test_d2_falsificacao_e_secundarias():
    rz = _d2("S3_razao_indet", "total")
    assert perto(rz["p"], 0.182, 5e-4) and perto(rz["ef_lo"], -1.1, 0.05) and perto(rz["ef_hi"], 5.6, 0.05)
    assert perto(_d2("S1_distancia")["ef_lo"], -5.4, 0.05) and perto(_d2("S1_distancia")["ef_hi"], 11.1, 0.05)
    assert perto(_d2("S4_escore_unico")["b"], -0.00288, 5e-6)                    # mesmo sinal da primária (sem artefato de onda)
    assert perto(_d2("S7_copartidarismo")["ef_lo"], -9.8, 0.05) and perto(_d2("S7_copartidarismo")["ef_hi"], 12.5, 0.05)
    assert all(r["distinguivel"] == "False" for r in _csv("c09_d2_resultados.csv"))  # nenhuma das 21 estimativas


def test_d1_quebras():
    r = _d1("Brasil", "agressao", 2019)
    assert perto(r["pct"], -17.0, 0.05) and perto(r["pct_lo"], -29.5, 0.05) and perto(r["pct_hi"], -2.4, 0.05)
    assert perto(r["placebo_pct"], -21.8, 0.05) and r["leitura"].startswith("não atribuível")
    assert perto(_d1("Brasil", "razao_indet_pp", 2019)["pct"], 6.5, 0.05)
    mn = _d1("Mulheres negras", "agressao", 2019)
    assert mn["leitura"].startswith("coincide") and perto(mn["pct"], -19.7, 0.05)
    assert not _d1("Mulheres negras", "agressao+indet", 2019)["leitura"].startswith("coincide")
    co = [r for r in _csv("c09_d1_resultados.csv") if r["leitura"].startswith("coincide")]
    assert len(co) == 1 and len(_csv("c09_d1_resultados.csv")) == 36
    for q in (2016, 2023):
        assert _d1("Brasil", "agressao", q)["leitura"] == "não distinguível de zero"
