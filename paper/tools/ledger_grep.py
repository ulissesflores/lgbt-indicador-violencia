"""Busca por palavra-chave (regex, sem caixa) em titulo/id/url/nota dos ledgers do projeto."""
import re
import sys

from ledger_lookup import load

idx = load()
recs = {}
for v in idx.values():
    for f, r in v:
        recs[str(r.get("id"))] = (f, r)
for q in sys.argv[1:]:
    rx = re.compile(q, re.I)
    print("===", q)
    n = 0
    for i, (f, r) in recs.items():
        blob = " ".join(str(r.get(k, "")) for k in ("titulo", "id", "url", "nota"))
        if rx.search(blob):
            print("  ", r.get("ano"), "|", i[:110], "|", str(r.get("titulo"))[:110])
            n += 1
            if n >= 6:
                break
