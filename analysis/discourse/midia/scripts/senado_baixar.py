# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Download Senate floor speeches month by month and the full text of candidate speeches.

Fetches the list of plenary speeches for each month from 2015-01 to 2026-10 from the public
Senate open data API (no key), keeps the raw list, filters candidate speeches whose summary and
indexing contain a group term, downloads the full text only for those, and writes a manifest
with the sha256 of every saved file.

Inputs
------
- https://legis.senado.leg.br/dadosabertos (public API, network access)
- the query dictionary module dicionario

Outputs
-------
- sources/public/q1-textointegral/discurso/midia/senado/lista_<yyyymm>.json
- senado/textos/<code>.txt and _candidatos.json (not tracked in git)
- senado/_MANIFESTO.sha256
- prints progress, the total of speeches and the number of candidates

Usage
-----
python3 -I analysis/discourse/midia/scripts/senado_baixar.py

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Senado: lista de pronunciamentos mes a mes (API publica, sem chave), 2015-01..2026-10.
Salva bruto em RAW/lista_AAAAMM.json. Depois filtra candidatos (Resumo+Indexacao com termo do grupo)
e baixa o texto integral (TextoIntegralTxt) so desses. Python: python3 -I.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import calendar, hashlib, json, os, re, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d

RAW = (REPO_ROOT + "/sources/public/q1-textointegral/discurso/midia/senado")
API = "https://legis.senado.leg.br/dadosabertos"
# filtro largo e simples para decidir quais textos integrais baixar
CAND = re.compile(r"lgbt|homossexua|homofob|transfob|\bgays?\b|travesti|transexua|trans\b|orientacao sexual|identidade de genero|"
                  r"diversidade sexual|cura gay|homoafetiv|genero|exterminio|genocidio", re.I)


def get(u, tent=6, accept="application/json"):
    for t in range(tent):
        try:
            req = urllib.request.Request(u, headers={"Accept": accept, "User-Agent": "pesquisa-lgbt-midia/1.0 (leitura publica)"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return b""
            time.sleep(3 * (t + 1))
        except Exception:
            time.sleep(3 * (t + 1))
    raise RuntimeError("falhou " + u)


def meses():
    for a in range(2015, 2027):
        for m in range(1, 13):
            if (a, m) > (2026, 10):
                return
            yield a, m


def itens_mes(body):
    j = json.loads(body)
    ss = j["DiscursosSessao"]["Sessoes"]
    if not ss:
        return []
    ss = ss["Sessao"]
    if isinstance(ss, dict):
        ss = [ss]
    out = []
    for s in ss:
        ps = (s.get("Pronunciamentos") or {}).get("Pronunciamento") or []
        if isinstance(ps, dict):
            ps = [ps]
        for p in ps:
            out.append(p)
    return out


if __name__ == "__main__":
    os.makedirs(RAW + "/textos", exist_ok=True)
    cands = []
    total = 0
    for a, m in meses():
        fn = f"{RAW}/lista_{a}{m:02d}.json"
        if not os.path.exists(fn):
            ult = calendar.monthrange(a, m)[1]
            if (a, m) == (2026, 10):
                ult = 21
            body = get(f"{API}/plenario/lista/discursos/{a}{m:02d}01/{a}{m:02d}{ult:02d}")
            open(fn, "wb").write(body)
        body = open(fn, "rb").read()
        if not body:
            continue
        its = itens_mes(body)
        total += len(its)
        for p in its:
            txt = d.norm((p.get("Resumo") or "") + " " + (p.get("Indexacao") or ""))
            if CAND.search(txt):
                cands.append((p["CodigoPronunciamento"], p["Data"], p.get("TextoIntegralTxt")))
        print(a, m, len(its), total, len(cands), flush=True)
    json.dump(cands, open(RAW + "/_candidatos.json", "w"))
    for cod, data, u in cands:
        fn = f"{RAW}/textos/{cod}.txt"
        if os.path.exists(fn) or not u:
            continue
        open(fn, "wb").write(get(u, accept="text/plain"))
    print("TOTAL pronunciamentos", total, "candidatos", len(cands))
    with open(RAW + "/_MANIFESTO.sha256", "w") as f:
        for root, _, fs in os.walk(RAW):
            for n in sorted(fs):
                if n.startswith("_MANIFESTO"):
                    continue
                p = os.path.join(root, n)
                f.write(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + os.path.relpath(p, RAW) + "\n")
