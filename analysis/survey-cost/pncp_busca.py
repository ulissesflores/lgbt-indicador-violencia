#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Scan Brazilian public procurement contracts by agency and year and filter them by a regex.

The script queries the public consultation API of the national procurement portal (PNCP), page
by page, for the contracts signed by one agency (CNPJ) in each year of a range. It keeps the
contracts whose object matches a case-insensitive regular expression and prints the totals and
the matches.

Inputs
------
- network: https://pncp.gov.br/api/consulta/v1/contratos (public API)
- command line: agency CNPJ, first year, last year, regular expression

Outputs
-------
- prints the number of contracts scanned, the number of matches and one tuple per match (year,
  agency, supplier, value, signature date, object, control number)

Usage
-----
python3 -I analysis/survey-cost/pncp_busca.py <cnpj> <first_year> <last_year> <regex>

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Varre contratos do PNCP (API publica de consulta) por orgao e ano e filtra o objeto por regex. Uso: pncp_busca.py <cnpj> <ano_ini> <ano_fim> <regex>

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import json, re, sys, time, urllib.parse, urllib.request
cnpj, a0, a1, rx = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), re.compile(sys.argv[4], re.I)
tot = 0; hit = []
for ano in range(a0, a1 + 1):
    pag = 1
    while True:
        u = "https://pncp.gov.br/api/consulta/v1/contratos?" + urllib.parse.urlencode({"dataInicial": f"{ano}0101", "dataFinal": f"{ano}1231", "cnpjOrgao": cnpj, "pagina": pag, "tamanhoPagina": 500})
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}), timeout=90))
        except Exception as e:
            print("ERRO", ano, pag, e); break
        d = r.get("data") or []
        tot += len(d)
        for c in d:
            if rx.search(c.get("objetoContrato") or ""):
                hit.append((ano, c["orgaoEntidade"]["razaoSocial"][:30], c.get("nomeRazaoSocialFornecedor", "")[:40], c.get("valorGlobal"), c.get("dataAssinatura"), (c.get("objetoContrato") or "")[:160], c.get("numeroControlePNCP")))
        if pag >= (r.get("totalPaginas") or 1): break
        pag += 1; time.sleep(0.3)
print(f"{cnpj} {a0}-{a1}: {tot} contratos varridos; {len(hit)} casam /{rx.pattern}/")
for h in hit: print(h)
