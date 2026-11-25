#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Download value fields of European tender notices from the TED API as raw JSON.

For each publication number given on the command line the script queries the TED search API
(v3) for fields such as notice type, total value, currency, winner name and contract dates,
keeps the first matching notice, picks the English title when titles are multilingual, and
writes the notice as one JSON file. It also prints the first 900 characters of each record.

Inputs
------
- network: https://api.ted.europa.eu/v3/notices/search (public API)
- command line: output directory and one or more publication numbers

Outputs
-------
- <output directory>/TEDAPI-<publication number>.json (one file per notice)
- prints each publication number with the start of its JSON record

Usage
-----
python3 -I analysis/survey-cost/ted_api.py <output_dir> <publication_number> [...]

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Le campos de valor de avisos do TED (API publica v3) e grava o JSON cru. Uso: ted_api.py <pasta_saida> <pub-number> [...]

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import json, sys, urllib.request
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
F = ["notice-type", "publication-date", "total-value", "total-value-cur", "result-value-notice", "result-value-cur-notice",
     "tender-value", "tender-value-cur", "estimated-value-proc", "estimated-value-cur-proc", "estimated-value-lot", "estimated-value-cur-lot",
     "framework-estimated-value", "winner-name", "contract-conclusion-date", "title-proc", "contract-title", "duration-period-value-lot", "duration-period-unit-lot"]
for n in sys.argv[2:]:
    req = urllib.request.Request("https://api.ted.europa.eu/v3/notices/search",
                                 data=json.dumps({"query": f"publication-number={n}", "fields": F, "limit": 1}).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=60))
    nt = r["notices"][0] if r["notices"] else {}
    nt.pop("links", None)
    for k in ("title-proc", "contract-title"):
        if k in nt and isinstance(nt[k], dict):
            nt[k] = nt[k].get("eng") or next(iter(nt[k].values()))
    (out / f"TEDAPI-{n}.json").write_text(json.dumps(nt, ensure_ascii=False, indent=1))
    print(n, json.dumps(nt, ensure_ascii=False)[:900])
