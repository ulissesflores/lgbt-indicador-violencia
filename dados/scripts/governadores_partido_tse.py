"""Cruza os mandatos de governador (Wikipédia, curados em governadores_uf_2011_2026.csv) com o TSE: troca o partido pelo PARTIDO PELO QUAL A PESSOA FOI ELEITA
(governador ou vice, eleição ordinária ou suplementar) no ciclo da época. Saída: dados/governadores_uf_2011_2026_tse.csv (mesmas colunas + partido_wiki, fonte_partido)
e dados/governadores_tse_validacao.md (toda divergência, lado a lado).
Ciclo do ano: 2011-14 -> eleição 2010; 2015-18 -> 2014 (inclui suplementares de AM 2017 e TO 2018 que o TSE guarda no arquivo de 2014); 2019-22 -> 2018; 2023-26 -> 2022.
Casamento por nome: primeiro e último token (sem partículas/JUNIOR/FILHO/NETO, sem acento) do nome da Wikipédia dentro dos tokens do nome completo OU do nome de urna do TSE, restrito ao ciclo e à UF.
Sem casamento (interinos não eleitos: presidente da Assembleia/TJ) -> mantém o partido da Wikipédia e marca fonte_partido=fallback_wiki.
Rodar: /opt/homebrew/bin/python3.14 -I dados/scripts/governadores_partido_tse.py (depois de governadores_tse.py)"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, unicodedata, collections
BASE = (REPO_ROOT + "/dados")
UFN = {"Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA", "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA", "Piauí": "PI", "Ceará": "CE",
       "Rio Grande do Norte": "RN", "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE", "Bahia": "BA", "Minas Gerais": "MG", "Espírito Santo": "ES",
       "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR", "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT",
       "Goiás": "GO", "Distrito Federal": "DF"}
# rótulos do TSE -> rótulos usados no painel/Bolognesi (painel_f8.py: score() tenta o rótulo, MAP e o inverso)
TSE2PAINEL = {"UNIÃO": "União Brasil", "REPUBLICANOS": "Republicanos", "PODE": "Podemos", "NOVO": "Novo", "PC do B": "PCdoB", "PCDOB": "PCdoB", "PATRI": "Patriota",
              "SOLIDARIEDADE": "SD", "PT do B": "Avante", "AVANTE": "Avante", "CIDADANIA": "Cidadania", "REDE": "Rede"}
PART = {"DE", "DA", "DO", "DOS", "DAS", "E", "JUNIOR", "JR", "FILHO", "NETO", "SOBRINHO"}


def toks(n):
    s = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().upper().replace(".", " ").replace("-", " ")
    return [t for t in s.split() if t not in PART]


def ciclo(ano):
    return 2010 if ano <= 2014 else 2014 if ano <= 2018 else 2018 if ano <= 2022 else 2022


tse = collections.defaultdict(list)  # (ciclo, uf) -> [(nome, partido, cargo)]
for r in csv.DictReader(open(f"{BASE}/governadores_tse_eleitos.csv", encoding="utf-8")):
    tse[(int(r["ano_eleicao"]), r["uf"])].append((r["nome"] + " " + r["nome_urna"], r["partido"], r["cargo"]))


def acha(nome, uf, ano):
    t = toks(nome); first, last = t[0], t[-1]
    cand = {(p) for n, p, c in tse[(ciclo(ano), uf)] if first in toks(n) and last in toks(n)}
    return cand


rows = list(csv.DictReader(open(f"{BASE}/governadores_uf_2011_2026.csv", encoding="utf-8")))
out, val = [], []
cont = collections.Counter()
for r in rows:
    uf = UFN[r["uf"]]; ano = int(r["ano"]); p_wiki = r["partido"]
    c = acha(r["governador"], uf, ano)
    if len(c) == 1:
        p = next(iter(c)); p = TSE2PAINEL.get(p, p); fonte = "tse"
    else:
        p, fonte = p_wiki, ("fallback_wiki" if not c else "ambiguo_wiki")
    cont[fonte] += 1
    out.append(dict(r, partido=p, partido_wiki=p_wiki, fonte_partido=fonte))
    if fonte != "tse" or p != p_wiki:
        val.append((r["uf"], ano, r["governador"], p_wiki, p, fonte, sorted(c)))
fn = list(rows[0].keys()) + ["partido_wiki", "fonte_partido"]
with open(f"{BASE}/governadores_uf_2011_2026_tse.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(out)
L = ["# Partido do governador: Wikipédia x TSE (partido pelo qual a pessoa foi eleita no ciclo)", "",
     f"Linhas UF-ano-governador: {len(rows)}; casadas com o TSE: {cont['tse']}; fallback Wikipédia (sem registro eleito no ciclo): {cont['fallback_wiki']}; ambíguas: {cont['ambiguo_wiki']}.", "",
     "| UF | ano | governador | partido Wikipédia | partido usado (TSE) | fonte | candidatos TSE |", "|---|---|---|---|---|---|---|"]
L += [f"| {a} | {b} | {c} | {d} | {e} | {f} | {', '.join(g)} |" for a, b, c, d, e, f, g in val]
open(f"{BASE}/governadores_tse_validacao.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print(L[2]); print("divergências/fallbacks listados:", len(val))
