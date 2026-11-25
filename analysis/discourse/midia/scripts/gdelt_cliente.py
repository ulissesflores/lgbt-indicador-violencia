# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Query the GDELT DOC 2.0 API politely and save each raw response with its sha256.

Client for the public GDELT DOC 2.0 API (no key; the service allows one request per 5 seconds).
It uses a shared file lock, keeps at least 8 seconds between requests and backs off on HTTP 429,
timeouts and suspiciously empty answers. When run directly it sends one probe query.

Inputs
------
- https://api.gdeltproject.org/api/v2/doc/doc (network access, through curl)
- command line: query, mode and optional key=value parameters

Outputs
-------
- sources/public/q1-textointegral/discurso/midia/gdelt/<tag>_<hash>.json (not tracked in git)
- lock file sources/public/q1-textointegral/discurso/.gdelt.lock
- prints status code, sha256, file path and the first 400 bytes of the answer

Usage
-----
python3 -I analysis/discourse/midia/scripts/gdelt_cliente.py <query> <mode> [key=value ...]

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Cliente GDELT DOC 2.0 (publico, sem chave). Limite do servico: 1 pedido/5 s.
Trava de arquivo compartilhada (outras frentes podem usar a mesma API/IP), espaco minimo de 8 s,
backoff em 429/timeout/vazio suspeito. Salva a resposta bruta + sha256 em RAW.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import fcntl, hashlib, json, os, subprocess, sys, time, urllib.parse
RAW = (REPO_ROOT + "/sources/public/q1-textointegral/discurso/midia/gdelt")
LOCK = (REPO_ROOT + "/sources/public/q1-textointegral/discurso/.gdelt.lock")
BASE = "https://api.gdeltproject.org/api/v2/doc/doc"
MIN_GAP = 8.0


def url(query, mode, **kw):
    p = {"query": query, "mode": mode, "format": "json"}
    p.update(kw)
    return BASE + "?" + urllib.parse.urlencode(p, quote_via=urllib.parse.quote)


def fetch(u, max_try=12, tag=""):
    """Devolve (status, corpo_bytes, sha256, caminho). Respeita trava global."""
    os.makedirs(RAW, exist_ok=True)
    fh = open(LOCK, "a+")
    espera = 60
    for t in range(max_try):
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            ts = os.path.getmtime(LOCK + ".t") if os.path.exists(LOCK + ".t") else 0
            dt = time.time() - ts
            if dt < MIN_GAP:
                time.sleep(MIN_GAP - dt)
            r = subprocess.run(["curl", "-s", "-m", "120", "-w", "\n%{http_code}", u], capture_output=True)
            open(LOCK + ".t", "w").write("x")
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
        out = r.stdout
        body, _, code = out.rpartition(b"\n")
        code = code.decode(errors="ignore").strip()
        if code == "200" and not body.startswith(b"Please limit") and body.strip():
            h = hashlib.sha256(body).hexdigest()
            path = os.path.join(RAW, (tag or h[:16]) + "_" + h[:10] + ".json")
            open(path, "wb").write(body)
            return code, body, h, path
        if code == "200" and body.strip() == b"":
            pass
        sys.stderr.write("gdelt tentativa %d codigo=%s corpo=%r espera=%ds\n" % (t, code, body[:60], espera))
        time.sleep(espera)
        espera = min(espera * 1.6, 600)
    return code, body, None, None


if __name__ == "__main__":
    u = url(sys.argv[1], sys.argv[2], **dict(a.split("=", 1) for a in sys.argv[3:]))
    c, b, h, p = fetch(u, tag="probe")
    print(c, h, p, b[:400])
