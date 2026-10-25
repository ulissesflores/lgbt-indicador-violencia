"""Gera dados/ideologia_partidos.csv a partir de dois brutos baixados (sem rede):
(a) Bolognesi, Ribeiro & Codato 2023 (Dados 66(2)), Tabela 1 do HTML SciELO (doi 10.1590/dados.2023.66.2.303);
(b) Zucco & Power, party.estimates.csv (Dataverse doi:10.7910/DVN/ZLAV8S, v2 2024-10-19), ondas 1990-2005.
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, html, os, re

BASE = REPO_ROOT
RAW = os.path.join(BASE, "fontes/p2-f8-dados-uf/ideologia")
OUT = os.path.join(BASE, "dados/ideologia_partidos.csv")
DOI_BOL = "https://doi.org/10.1590/dados.2023.66.2.303"
DV_ZP = "https://dataverse.harvard.edu/api/access/datafile/1412580"
DV_ZP_PAGE = "https://doi.org/10.7910/DVN/ZLAV8S"


def bolognesi():
    t = open(os.path.join(RAW, "doi_303.html"), "rb").read().decode("utf-8", "replace")
    m = next(m for m in re.finditer(r"<table.*?</table>", t, re.S | re.I)
             if "Descritivas" in t[max(0, m.start() - 400):m.start()] or
             ("Partido" in re.sub(r"<[^>]+>", " ", m.group(0))[:80] and "Média" in m.group(0)[:600]))
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", m.group(0), re.S | re.I):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)]
        if len(cells) >= 2 and cells[0] != "Partido":
            rows.append({"partido": cells[0], "escore": cells[1].replace(",", "."),
                         "escala": "0-10 (media de classificacao por especialistas; 0=esquerda, 10=direita)",
                         "fonte": "Bolognesi, Ribeiro & Codato 2023, Dados 66(2), Tabela 1 (survey ABCP/UFPR)",
                         "ano_fonte": "2018", "url": DOI_BOL})
    return rows


def zucco_power():
    rows = []
    with open(os.path.join(RAW, "party.estimates.csv"), encoding="ascii") as f:
        rd = csv.reader(f)
        header = next(rd)
        cols = [(i, h.split(".")[-1]) for i, h in enumerate(header) if h.startswith("party.estimates.")]
        for rec in rd:
            partido = rec[0].strip('"')
            for i, ano in cols:
                v = rec[i]
                if v == "NA":
                    continue
                rows.append({"partido": partido, "escore": f"{float(v):.4f}",
                             "escala": "autoposicionamento 1-10 rescalado (Power & Zucco; valores observados 1,7-7,3)",
                             "fonte": "Power & Zucco, party.estimates.csv (Brazilian legislators surveys 1990-2005)",
                             "ano_fonte": ano, "url": DV_ZP})
    return rows


def main():
    rows = bolognesi() + zucco_power()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["partido", "escore", "escala", "fonte", "ano_fonte", "url"])
        w.writeheader()
        w.writerows(rows)
    b = sum(1 for r in rows if r["ano_fonte"] == "2018")
    print("linhas:", len(rows), "| Bolognesi:", b, "| Zucco&Power:", len(rows) - b)


if __name__ == "__main__":
    main()
