# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Rebuild the two series tables of the Sinan summary and check them against the published text.

Reads the state-by-year completeness series and builds a national table by year and a table by
state. The effective missing share is the sum of the unknown-or-blank and not-applicable
percentages of field 55; the state table compares the simple mean of 2015-2017 with 2023-2025,
and adds the mean LGBT-phobia share and the notification count. Each generated row is looked up
in the published summary, and the script exits with status 1 if any row is not reproduced.

Inputs
------
- data/sinan/serie_campo55_uf_ano.csv
- data/sinan/resumo.md

Outputs
-------
- data/sinan/serie_tabelas.md
- prints the number of generated rows and any divergent row to stdout

Usage
-----
python3 -I data/sinan/serie_tabelas.py (exit status 1 if a published row is not reproduced)

Status
------
Feeds numbers printed in the article (listed in paper_numbers.json).

Notes
-----
Original description (Portuguese), kept verbatim:

Gera as duas tabelas da seção 'Série 2015-2025' de data/sinan/resumo.md a partir de serie_campo55_uf_ano.csv (antes sem gerador no repositório)
e confere linha a linha contra o texto publicado em resumo.md.
Convenção descoberta por engenharia reversa e confirmada pela conferência: faltante efetivo = pct_m_ign + pct_m_na (valores do CSV, 2 casas);
por UF = média SIMPLES dos três anos (2015-17 e 2023-25), com a variação calculada sobre as médias NÃO arredondadas; LGBTfobia = média simples de pct_m_lgbt em 2015-25; n = soma de n_interpessoal 2015-25.
Rodar: python3 -I data/sinan/serie_tabelas.py   (saída: serie_tabelas.md; exit 1 se alguma linha publicada não for reproduzida)

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, collections, sys
BASE = (REPO_ROOT + "/data/sinan")
rows = list(csv.DictReader(open(f"{BASE}/serie_campo55_uf_ano.csv", encoding="utf-8")))
pub = open(f"{BASE}/resumo.md", encoding="utf-8").read().split("\n")
ef = lambda r: float(r["pct_m_ign"]) + float(r["pct_m_na"])

out = ["| ano | n | campo 55 ign+branco % | NA % | faltante efetivo % | LGBTfobia % | orient. ign % | homo+bi % (de todas) | trans % |", "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["uf"] == "BR":
        out.append(f"| {r['ano']} | {int(r['n_interpessoal']):,} | {r['pct_m_ign']} | {r['pct_m_na']} | {round(ef(r), 1)} | {r['pct_m_lgbt']} | {r['pct_o_ign']} | {r['pct_o_homo_bi']} | {r['pct_g_trans']} |")
por_uf = collections.defaultdict(list)
for r in rows:
    if r["uf"] != "BR":
        por_uf[r["uf"]].append(r)
tab = []
for uf, rr in por_uf.items():
    a = [ef(r) for r in rr if r["ano"] in ("2015", "2016", "2017")]; b = [ef(r) for r in rr if r["ano"] in ("2023", "2024", "2025")]
    ma, mb = round(sum(a) / len(a), 1), round(sum(b) / len(b), 1)
    tab.append((mb, uf, ma, round(sum(b) / len(b) - sum(a) / len(a), 1), round(sum(float(r["pct_m_lgbt"]) for r in rr) / len(rr), 2), sum(int(r["n_interpessoal"]) for r in rr)))
tab.sort(key=lambda t: -t[0])
out += ["", "| UF | faltante efetivo 2015-17 % | 2023-25 % | variação p.p. | LGBTfobia média % | n 2015-25 |", "|---|---|---|---|---|---|"]
out += [f"| {uf} | {ma} | {mb} | {d:+.1f} | {lg:.2f} | {n:,} |" for mb, uf, ma, d, lg, n in tab]
falta = [l for l in out if l.startswith("| ") and not l.startswith("| ano") and not l.startswith("| UF") and l not in pub]
open(f"{BASE}/serie_tabelas.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"linhas geradas: {sum(1 for l in out if l.startswith('| ') and l[2].isalnum() and not l.startswith('| ano') and not l.startswith('| UF'))} | não reproduzidas no resumo.md publicado: {len(falta)}")
for l in falta:
    print("  DIVERGE:", l)
sys.exit(1 if falta else 0)
