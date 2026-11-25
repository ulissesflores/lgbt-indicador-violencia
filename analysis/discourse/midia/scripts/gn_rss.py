# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Collect Google News RSS results as a declared fallback while GDELT was blocked.

Queries the public Google News RSS search (no key) for each dictionary entry and year. The feed
is truncated at about 100 items per query, so each entry and year is split (half year, quarter,
month) while it returns 95 items or more; a cell that still saturates at month level is marked
saturated and its count is a floor, not a universe count. One request about every 4 seconds;
resumable.

Inputs
------
- https://news.google.com/rss/search (network access)
- analysis/discourse/midia/_gnrss_celulas.jsonl (finished cells, if it exists)
- the query dictionary module dicionario

Outputs
-------
- sources/public/q1-textointegral/discurso/midia/gnrss/<id>_<start>_<end>_<hash>.xml
  (raw XML with sha256 in the name; not tracked in git)
- analysis/discourse/midia/_gnrss_celulas.jsonl
- prints the entry, year and number of items

Usage
-----
python3 -I analysis/discourse/midia/scripts/gn_rss.py

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

FALLBACK declarado (ADENDO pos-contagem) para imprensa quando o GDELT esta bloqueado:
Google News RSS (publico, sem chave/cadastro). Lista TRUNCADA em ~100 itens por consulta; por isso cada
entrada x ano e dividida (semestre, trimestre, mes) enquanto devolver >= 95 itens. Celula que satura no mes
e marcada 'saturada' (n e piso). NAO e contagem do universo; e piso e quadro de amostra.
Salva XML bruto + sha256 em RAW. 1 pedido a cada ~4 s. Retomavel.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, datetime, hashlib, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d

BASE = REPO_ROOT
RAW = BASE + "/sources/public/q1-textointegral/discurso/midia/gnrss"
OUT = BASE + "/analysis/discourse/midia"
LOC = {"pt": ("pt-BR", "BR", "BR:pt-419"), "en": ("en-US", "US", "US:en"), "es": ("es-419", "MX", "MX:es-419")}
UA = {"User-Agent": "Mozilla/5.0 (pesquisa-lgbt-midia leitura publica)"}
_last = [0.0]


def get(u):
    for t in range(6):
        dt = time.time() - _last[0]
        if dt < 4:
            time.sleep(4 - dt)
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                _last[0] = time.time()
                return r.read()
        except urllib.error.HTTPError as e:
            _last[0] = time.time()
            sys.stderr.write("HTTP %s\n" % e.code)
            time.sleep(30 * (t + 1))
        except Exception:
            time.sleep(10 * (t + 1))
    raise RuntimeError(u)


def celula(e, ini, fim):
    hl, gl, ceid = LOC[e["lang"]]
    q = e["gdelt"] + f" after:{ini} before:{fim}"
    u = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, "hl": hl, "gl": gl, "ceid": ceid}, quote_via=urllib.parse.quote_plus)
    body = get(u)
    h = hashlib.sha256(body).hexdigest()
    open(f"{RAW}/{e['id']}_{ini}_{fim}_{h[:10]}.xml", "wb").write(body)
    root = ET.fromstring(body)
    its = []
    for it in root.iter("item"):
        its.append({"titulo": (it.findtext("title") or ""), "link": it.findtext("link") or "", "data": it.findtext("pubDate") or "",
                    "fonte": (it.find("source").text if it.find("source") is not None else "")})
    return its, h


def periodos(a, m1, m2):
    """divide o intervalo [m1,m2] de meses do ano a em dois"""
    meio = (m1 + m2) // 2
    return (m1, meio), (meio + 1, m2)


def datas(a, m1, m2):
    ini = datetime.date(a, m1, 1)
    fim = datetime.date(a + (m2 == 12), 1 if m2 == 12 else m2 + 1, 1)
    return ini.isoformat(), fim.isoformat()


def varre(e, a, m1, m2, saida):
    ini, fim = datas(a, m1, m2)
    if datetime.date.fromisoformat(ini) > datetime.date(2026, 10, 21):
        return
    its, h = celula(e, ini, fim)
    if len(its) >= 95 and m1 < m2:
        for (x, y) in periodos(a, m1, m2):
            varre(e, a, x, y, saida)
        return
    saida.append({"entrada": e["id"], "ano": a, "ini": ini, "fim": fim, "n": len(its), "saturada": len(its) >= 95, "sha": h, "itens": its})


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    arq = OUT + "/_gnrss_celulas.jsonl"
    feitas = set()
    if os.path.exists(arq):
        for l in open(arq):
            j = json.loads(l); feitas.add((j["entrada"], j["ano"]))
    f = open(arq, "a")
    for e in d.E:
        for a in range(2015, 2027):
            if (e["id"], a) in feitas:
                continue
            saida = []
            varre(e, a, 1, 12, saida)
            for s in saida:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
            f.flush()
            print(e["id"], a, sum(s["n"] for s in saida), flush=True)
