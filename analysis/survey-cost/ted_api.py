#!/opt/homebrew/bin/python3.14
"""Le campos de valor de avisos do TED (API publica v3) e grava o JSON cru. Uso: ted_api.py <pasta_saida> <pub-number> [...]"""
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
