# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Retry the Wayback Machine for the sources still missing a local file.

Second pass: for each case that has a link but no saved page, requests the Wayback shortcut
web.archive.org/web/2019id_/<url> one at a time with pauses. In sample mode it tries only the
drawn sample cases. The log is written only at the end of the run.

Inputs
------
- sources/public/p3-ggb/_raw/ggb2019_lista_nominal.csv (not tracked in git)
- analysis/ggb-audit/dados/amostra.csv (only in sample mode)
- web.archive.org (network access)

Outputs
-------
- sources/public/p3-ggb/_raw/news/<id>.html (pages recovered; not tracked in git)
- analysis/ggb-audit/dados/fetch_log_wayback_<mode>.csv
- prints progress and the count of results

Usage
-----
python3 -I analysis/ggb-audit/scripts/s02b_wayback_retry.py [amostra]

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

S02b. Segunda passada: para cada fonte ainda sem arquivo local, tenta o Wayback pelo atalho
web.archive.org/web/2019id_/<url>. Sequencial, com pausa. Modo "amostra" tenta so os casos sorteados.
O log (data/fetch_log_wayback_<modo>.csv) so e gravado ao fim; a execucao da amostra foi interrompida
(Wayback respondia 404/429/500) apos recuperar 2 casos. Uso: python3.14 -I s02b_wayback_retry.py [amostra]

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, ssl, time, urllib.request, urllib.parse, sys
from pathlib import Path
ROOT = Path(REPO_ROOT)
RAW = ROOT/"sources/public/p3-ggb/_raw"; NEWS = RAW/"news"
OUT = ROOT/"analysis/ggb-audit/dados"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
ctx = ssl.create_default_context()
sys.path.insert(0, str(Path(__file__).parent))
def clean(u):
    u = u.replace(" ", ""); p = urllib.parse.urlsplit(u)
    q = [kv for kv in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if kv[0].lower() != "fbclid"]
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path), safe="/%:@,;=+$~!*'()-._"), urllib.parse.urlencode(q), ""))
ONLY = set(r["id"] for r in csv.DictReader((OUT/"amostra.csv").open())) if len(sys.argv) > 1 and sys.argv[1] == "amostra" else None
rows = [r for r in csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()) if r["link"] and not (NEWS/f'{r["id"]}.html').exists() and (ONLY is None or r["id"] in ONLY)]
print("pendentes:", len(rows))
log = []
for i, r in enumerate(rows):
    u = clean(r["link"]); res = dict(id=r["id"], resultado="")
    for tent in range(2):
        try:
            req = urllib.request.Request("https://web.archive.org/web/2019id_/" + u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                b = resp.read(3_000_000)
                if resp.status == 200 and len(b) > 2000:
                    (NEWS/f'{r["id"]}.html').write_bytes(b); res["resultado"] = "wayback_ok:" + resp.geturl().split("/web/")[1][:14]
                else: res["resultado"] = f"wayback_pequeno:{resp.status}:{len(b)}"
            break
        except urllib.error.HTTPError as e:
            res["resultado"] = f"wayback_http{e.code}"
            if e.code in (429, 503): time.sleep(8); continue
            break
        except Exception as e:
            res["resultado"] = "wayback_" + type(e).__name__; time.sleep(3)
    log.append(res); time.sleep(1.2)
    if i % 20 == 0: print(i, res["resultado"], flush=True)
with (OUT/("fetch_log_wayback_%s.csv" % (sys.argv[1] if len(sys.argv)>1 else "todos"))).open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "resultado"]); w.writeheader(); w.writerows(log)
from collections import Counter
print(Counter(x["resultado"].split(":")[0] for x in log))
