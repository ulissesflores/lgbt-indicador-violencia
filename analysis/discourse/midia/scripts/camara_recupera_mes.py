# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Recover House speech pages month by month after the yearly recovery failed.

Second recovery stage: for each yearly window listed as lost by camara_recupera.py, repeats the
request month by month (100 items per page) and, if the API still returns 500, by fortnight.
The module runs its main function when imported or executed.

Inputs
------
- sources/public/q1-textointegral/discurso/midia/camara/_recuperacao_perdas.json
- https://dadosabertos.camara.leg.br/api/v2 (via camara_recupera.py, network access)

Outputs
-------
- sources/public/q1-textointegral/discurso/midia/camara/<deputy>_m<yyyymm>_<page>.json
- _recuperacao_perdas2.json in the same folder (final losses)
- prints progress and the number of final losses

Usage
-----
python3 -I analysis/discourse/midia/scripts/camara_recupera_mes.py

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

2a etapa: para cada janela anual com perda (500 persistente na ultima pagina), repete mes a mes (itens=100)
e, se ainda 500, quinzena. Salva {id}_m{AAAAMM}_{pag}.json. Perdas finais em _recuperacao_perdas2.json.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import calendar, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import camara_recupera as c
RAW = c.RAW


def main():
    perdas = json.load(open(RAW + "/_recuperacao_perdas.json"))
    janelas = sorted({(p[0], int(p[2][:4])) for p in perdas})
    novas = []
    for did, ano in janelas:
        for m in range(1, 13):
            if (ano, m) > (2026, 10):
                break
            ult = calendar.monthrange(ano, m)[1]
            p2 = []
            c.janela(did, f"m{ano}{m:02d}", f"{ano}-{m:02d}-01", f"{ano}-{m:02d}-{ult:02d}", p2)
            if p2:
                # quinzenas
                p3 = []
                c.janela(did, f"q{ano}{m:02d}a", f"{ano}-{m:02d}-01", f"{ano}-{m:02d}-15", p3)
                c.janela(did, f"q{ano}{m:02d}b", f"{ano}-{m:02d}-16", f"{ano}-{m:02d}-{ult:02d}", p3)
                novas += p3
        print(did, ano, len(novas), flush=True)
    json.dump(novas, open(RAW + "/_recuperacao_perdas2.json", "w"))
    print("PERDAS2", len(novas))


main()
