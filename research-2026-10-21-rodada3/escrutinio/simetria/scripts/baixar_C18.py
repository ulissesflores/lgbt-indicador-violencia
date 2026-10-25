"""C18: baixa as paginas listadas em picks_C18.tsv (sem login, sem aceitar termos). curl com UA comum; se falhar tenta Wayback id_.
Saidas: fontes/q1-textointegral/discurso/simetria/brasil/<gov>_<qid>.<ext>, downloads_C18.tsv (status, bytes, sha256), texto extraido .txt.
Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, html, os, re, subprocess, subprocess as sp
from concurrent.futures import ThreadPoolExecutor
S = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
D = (REPO_ROOT + "/fontes/q1-textointegral/discurso/simetria/brasil")
os.makedirs(D, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

def curl(url, out):
    r = sp.run(["curl", "-sL", "-m", "60", "-A", UA, "-o", out, "-w", "%{http_code} %{content_type}", url], capture_output=True, text=True)
    return r.stdout.strip()

def texto(path):
    raw = open(path, "rb").read()
    if raw[:4] == b"%PDF":
        r = sp.run(["pdftotext", "-layout", path, "-"], capture_output=True)
        return r.stdout.decode("utf-8", "ignore")
    t = raw.decode("utf-8", "ignore")
    t = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))

def job(row):
    gov, qid, url = row["gov"], row["qid"], row["url"]
    base = f"{D}/{gov}_{qid}"
    via = "direto"
    st = curl(url, base + ".raw")
    ok = st.startswith("200") and os.path.getsize(base + ".raw") > 1500
    low = open(base + ".raw", "rb").read(4000).lower() if os.path.exists(base + ".raw") else b""
    if ok and (b"just a moment" in low or b"attention required" in low or b"cf-chl" in low):
        ok = False
    if not ok:
        st2 = curl("https://web.archive.org/web/2id_/" + url, base + ".raw")
        ok = st2.startswith("200") and os.path.getsize(base + ".raw") > 1500
        via = "wayback" if ok else "FALHOU"
        st = st + " | " + st2
    if not ok:
        return [gov, qid, url, row["dominio_tipo"], via, st, 0, "", 0]
    raw = open(base + ".raw", "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    t = texto(base + ".raw")
    open(base + ".txt", "w").write(t)
    return [gov, qid, url, row["dominio_tipo"], via, st, len(raw), sha, len(t)]

rows = list(csv.DictReader(open(S + "/picks_C18.tsv"), delimiter="\t"))
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(job, rows))
with open(S + "/downloads_C18.tsv", "w") as f:
    f.write("gov\tqid\turl\ttipo_fonte\tvia\tstatus\tbytes\tsha256\tchars_texto\n")
    for r in res:
        f.write("\t".join(map(str, r)) + "\n")
print(sum(1 for r in res if r[4] != "FALHOU"), "ok de", len(res))
