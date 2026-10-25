"""S02. Baixa a fonte primaria de cada caso (link do Anexo 4 do GGB 2019), com fallback Wayback.
Bruto em fontes/p3-ggb/_raw/news/<id>.html (fora do git). Registro publico: dados/fetch_log.csv (sem URL, so dominio).
Uso: python3.14 -I s02_fetch_fontes.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, json, re, ssl, time, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(REPO_ROOT)
RAW = ROOT/"fontes/p3-ggb/_raw"; NEWS = RAW/"news"; NEWS.mkdir(exist_ok=True)
OUT = ROOT/"research-2026-10-21-rodada3/F3-ggb/dados"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
def clean(u):
    u = u.replace(" ", "")
    p = urllib.parse.urlsplit(u); q = [kv for kv in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if kv[0].lower() not in ("fbclid",)]
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path), safe="/%:@,;=+$~!*'()-._"), urllib.parse.urlencode(q), ""))
def get(u, t=25):
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=t, context=ctx) as r:
        return r.status, r.geturl(), r.read(3_000_000)
def one(row):
    id_, link = row["id"], row["link"]
    res = dict(id=id_, dominio=urllib.parse.urlsplit(link).netloc.lower().removeprefix("www.") if link else "", via="", status="", bytes=0)
    if not link: res["via"] = "sem_link"; return res
    f = NEWS/f"{id_}.html"
    if f.exists() and f.stat().st_size > 0:
        res.update(via="cache", status="200", bytes=f.stat().st_size); return res
    u = clean(link)
    try:
        s, fu, b = get(u); res.update(via="direto", status=str(s), bytes=len(b))
        if s == 200 and len(b) > 2000: f.write_bytes(b); return res
    except Exception as e:
        res.update(via="direto_erro", status=type(e).__name__ + ":" + str(getattr(e, "code", ""))[:12])
    # Wayback
    try:
        api = "https://archive.org/wayback/available?timestamp=20191231&url=" + urllib.parse.quote(u, safe="")
        s, _, b = get(api, 30); j = json.loads(b); snap = j.get("archived_snapshots", {}).get("closest")
        if snap and snap.get("available"):
            su = snap["url"].replace("http://", "https://", 1)
            su = re.sub(r"(/web/\d+)/", r"\1id_/", su, count=1)  # id_ = conteudo original sem barra do Wayback
            s2, _, b2 = get(su, 40)
            if s2 == 200 and len(b2) > 2000:
                f.write_bytes(b2); res.update(via="wayback", status="200", bytes=len(b2)); return res
        res["via"] += "+wayback_sem_snapshot"
    except Exception as e:
        res["via"] += "+wayback_erro:" + type(e).__name__
    return res
rows = list(csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()))
t0 = time.time()
with ThreadPoolExecutor(8) as ex: out = list(ex.map(one, rows))
with (OUT/"fetch_log.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(o["via"] for o in out)); print("s", round(time.time()-t0))
