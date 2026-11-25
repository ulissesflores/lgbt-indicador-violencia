# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Recompute two article numbers that only come from public raw data (PNS 2019, House speeches).

Block 1 computes the weighted share of LGB+ adults aged 18 to 29 in the PNS 2019 microdata
(weight V00291, orientation variable Y008). Block 2 matches the 13 coded House speeches on life
expectancy to the downloaded full text by hash, extracts the ages they attribute to the
population with a fixed rule (and an amended rule), and counts them. The tables feed the
article-number check.

Inputs
------
- sources/public/q1-textointegral/F2/pns2019/input_PNS_2019_utf8.txt and x/PNS_2019.txt
- sources/public/q1-textointegral/discurso/midia/camara/*.json (not tracked in git)
- analysis/discourse/midia/amostra_codificada.csv

Outputs
-------
- analysis/article-numbers/numeros_do_bruto.csv
- analysis/article-numbers/falas_expectativa.csv
- prints one line per recomputed number and whether it matches the printed value

Usage
-----
.run/venv/bin/python -I analysis/article-numbers/numeros_do_bruto.py

Status
------
Feeds numbers printed in the article (listed in paper_numbers.json).

Notes
-----
Original description (Portuguese), kept verbatim:

Números do artigo que só saem do dado bruto público (PNS 2019 e discursos da Câmara).

Dois blocos, cada um com a regra escrita ANTES de rodar sobre o conjunto completo
(2026-11-24, registrado no PUBLICACOES-STATE do autor e aqui):

1. PNS 2019, l.736 da edição pt-BR: "57% dos adultos LGB+ têm de 18 a 29 anos". Parcela
   ponderada pelo peso calibrado V00291, entre os adultos do módulo V (n = 88.531) com Y008 em
   {2, 3, 4} (LGB+), dos que têm C008 (idade) de 18 a 29. Mesmo universo e mesma leitura do
   microdado de data/pns/pns_c05_razao_direta.py. Entrada: o microdado baixado por
   scripts/acquire_pns2019.py (hash conferido por aquele script).

2. Discursos da Câmara, l.340 e l.1715: "11 discursos atribuem a essa população uma vida média
   mais curta, entre 27 e 36 anos". Universo: as 13 falas do Parlamento codificadas com forma
   ``expectativa_vida_comparativa`` em analysis/discourse/midia/amostra_codificada.csv. O texto
   integral de cada uma é achado no bruto baixado por
   analysis/discourse/midia/scripts/camara_baixar.py pela MESMA chave da amostra:
   sha256(idDeputado + dataHoraInicio + transcricao + " " + sumario + " " + keywords), como em
   analise_parlamento.py. Chave igual = texto idêntico ao que foi codificado.
   Regra de idade (fixada antes de ver as 13): em cada ocorrência de "expectativa de vida",
   "vida média", "média de vida", "vivem" ou "sobrevida", toma-se
   todo inteiro de 15 a 90 seguido de "anos" nos 120 caracteres seguintes, sem atravessar ponto
   final (duas das 13 falas, d35539a35e e 04a3b4ab22, foram vistas antes de a regra ser fixada,
   ao testar o casamento por chave). Uma fala "atribui idade" se tiver ao menos um desses inteiros. Saem: quantas falas
   atribuem idade, quantas têm postura AFIRMA, e o menor e o maior inteiro achados.
   EMENDA DATADA (2026-11-24, feita DEPOIS de ver o resultado da regra acima, e declarada como tal):
   a regra fixa deu máximo 40, vindo da fala cf627406e98d, "expectativa de vida média de pouco mais
   de 30 anos, por volta de 40 anos a menos do que a população brasileira": o 40 é diferença, não
   idade. A emenda descarta inteiro seguido de "a menos" ou "a mais". As duas saídas ficam gravadas:
   exp_idade_* (regra fixa) e exp_idade_*_emenda (regra emendada).

Saída: numeros_do_bruto.csv nesta pasta (mesmas colunas de contas_do_texto.csv) e
falas_expectativa.csv (uma linha por fala: hash, data, postura, idades achadas, casou).
Rodar: ``.run/venv/bin/python -I analysis/article-numbers/numeros_do_bruto.py`` (pandas, para a PNS).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import csv
import glob
import hashlib
import json
import math
import os
import re
from pathlib import Path

RAIZ = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[2])
AQUI = Path(__file__).resolve().parent
PNS = RAIZ / "sources/public/q1-textointegral/F2/pns2019"
CAM = RAIZ / "sources/public/q1-textointegral/discurso/midia/camara"
TERMO = re.compile(r"(?i)expectativa de vida|vida m[ée]dia|m[ée]dia de vida|\bvivem\b|sobrevida")
IDADE = re.compile(r"\b(\d{2})\s*anos\b")
DIFERENCA = re.compile(r"\b(\d{2})\s*anos\s+a\s+(?:menos|mais)\b", re.I)  # emenda de 2026-11-24
LINHAS = []


def registra(ident, linha_pt, impresso, formula, entradas, calculado, escala=1.0):
    """Guarda um número recalculado e se ele bate com o impresso (arredondado como impresso)."""
    t = impresso.strip().rstrip("%")
    casas = len(t.split(",")[1]) if "," in t else 0
    alvo = round(calculado * escala, casas)
    bate = math.isclose(alvo, float(t.replace(".", "").replace(",", ".")), abs_tol=1e-9)
    LINHAS.append({"id": ident, "linha_pt": linha_pt, "impresso": impresso, "formula": formula, "entradas": entradas,
                   "calculado": repr(round(float(calculado) * escala, 6)), "bate": "sim" if bate else "NAO"})


def pns_57():
    """Parcela ponderada de LGB+ de 18 a 29 anos entre os adultos LGB+ da PNS 2019."""
    import pandas as pd

    pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
    layout = (PNS / "input_PNS_2019_utf8.txt").read_text(encoding="utf8", errors="replace").splitlines()
    spec = {m.group(2): (int(m.group(1)), int(m.group(3))) for linha in layout if (m := pat.match(linha))}
    want = ["C008", "Y008", "V00291", "V001"]
    cols = [(spec[k][0] - 1, spec[k][0] - 1 + spec[k][1]) for k in want]
    raw = pd.read_fwf(PNS / "x/PNS_2019.txt", colspecs=cols, names=want, header=None, dtype=str)
    d = raw[raw.V001.notna()].copy()
    assert len(d) == 88531, len(d)
    w = d.V00291.astype(float)
    idade = d.C008.astype(float)
    lgb = d.Y008.isin(["2", "3", "4"])
    jovem = lgb & (idade >= 18) & (idade < 30)
    ent = f"PNS 2019 microdado (scripts/acquire_pns2019.py): LGB+ n={int(lgb.sum())}; 18-29 n={int(jovem.sum())}; peso V00291"
    registra("pns_lgb_18_29", 736, "57%", "soma(w, LGB+ 18-29) / soma(w, LGB+)", ent, w[jovem].sum() / w[lgb].sum(), 100)


def falas_expectativa():
    """Casa as 13 falas de expectativa de vida com o texto integral e extrai as idades pela regra fixa."""
    amostra = [r for r in csv.DictReader(open(RAIZ / "analysis/discourse/midia/amostra_codificada.csv", encoding="utf-8"))
               if r["universo"] == "Parlamento" and r["forma"] == "expectativa_vida_comparativa"]
    alvo = {r["hash"]: r for r in amostra}
    texto = {}
    for fn in sorted(glob.glob(str(CAM / "[0-9]*_*.json"))):
        did = os.path.basename(fn).split("_")[0]
        for x in json.load(open(fn, encoding="utf-8"))["dados"]:
            tx = (x.get("transcricao") or "") + " " + (x.get("sumario") or "") + " " + (x.get("keywords") or "")
            k = hashlib.sha256((did + x["dataHoraInicio"] + tx).encode()).hexdigest()
            if k in alvo:
                texto[k] = tx
    linhas = []
    for h, r in sorted(alvo.items(), key=lambda kv: kv[1]["data"]):
        idades, emenda = [], []
        tx = texto.get(h, "")
        for m in TERMO.finditer(tx):
            janela = tx[m.end(): m.end() + 120].split(".")[0]
            idades += [int(n) for n in IDADE.findall(janela) if 15 <= int(n) <= 90]
            dif = {int(n) for n in DIFERENCA.findall(janela)}
            emenda += [int(n) for n in IDADE.findall(janela) if 15 <= int(n) <= 90 and int(n) not in dif]
        linhas.append({"hash": h[:12], "data": r["data"], "postura": r["postura"], "fonte_citada": r["fonte_citada"],
                       "casou": "sim" if h in texto else "nao", "idades": ";".join(map(str, sorted(set(idades)))),
                       "idades_emenda": ";".join(map(str, sorted(set(emenda))))})
    with open(AQUI / "falas_expectativa.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    casadas = sum(1 for x in linhas if x["casou"] == "sim")
    com_idade = [x for x in linhas if x["idades"]]
    todas = [int(i) for x in com_idade for i in x["idades"].split(";")]
    afirma = sum(1 for x in linhas if x["postura"] == "AFIRMA")
    ent = f"analysis/discourse/midia/amostra_codificada.csv: {len(linhas)} falas; casadas no bruto {casadas}; falas_expectativa.csv"
    registra("exp_afirma", 340, "11", "falas de expectativa com postura AFIRMA", ent, afirma)
    registra("exp_com_idade", 340, "11", "falas que atribuem idade (regra fixa)", ent, len(com_idade))
    if todas:
        registra("exp_idade_min", 340, "27", "menor idade atribuída", ent, min(todas))
        registra("exp_idade_max", 340, "36", "maior idade atribuída", ent, max(todas))
    em = [int(i) for x in linhas if x["idades_emenda"] for i in x["idades_emenda"].split(";")]
    com_em = sum(1 for x in linhas if x["idades_emenda"])
    registra("exp_com_idade_emenda", 340, "11", "falas que atribuem idade (regra emendada)", ent, com_em)
    if em:
        registra("exp_idade_min_emenda", 340, "27", "menor idade atribuída (regra emendada)", ent, min(em))
        registra("exp_idade_max_emenda", 340, "36", "maior idade atribuída (regra emendada)", ent, max(em))
    return casadas, len(linhas)


def main():
    """Roda os dois blocos e grava a tabela."""
    pns_57()
    casadas, total = falas_expectativa()
    with open(AQUI / "numeros_do_bruto.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(LINHAS[0]))
        w.writeheader()
        w.writerows(LINHAS)
    print(f"falas casadas no bruto: {casadas}/{total}")
    for r in LINHAS:
        print(f"{r['id']:<16} l.{r['linha_pt']:<5} impresso {r['impresso']:>4} calculado {r['calculado']:>12} {r['bate']}")
    regra_final = [r for r in LINHAS if r["id"] not in ("exp_com_idade", "exp_idade_min", "exp_idade_max")]
    return 0 if casadas == total and all(r["bate"] == "sim" for r in regra_final) else 1


if __name__ == "__main__":
    raise SystemExit(main())
