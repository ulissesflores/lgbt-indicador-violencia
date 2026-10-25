"""Baixa o export publico do TDoR (Remembering Our Dead, tdor.translivesmatter.info) para o Brasil, ano civil 2008-2025.
Sem login, sem cadastro. Saida (com nomes) so em _raw/ (fora do git). Uso: python3.14 -I s01_fetch_tdor.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import urllib.request, zipfile, io, hashlib, json, pathlib, time
RAW = pathlib.Path((REPO_ROOT + "/fontes/p3-ggb/_raw/tdor/anual"))
RAW.mkdir(parents=True, exist_ok=True)
LOG = []
for y in range(2008, 2026):
    url = f"https://tdor.translivesmatter.info/reports?from={y}-01-01&to={y}-12-31&country=Brazil&filter=&action=export&sortby=date&sortup=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pesquisa academica; leitura publica)"})
        data = urllib.request.urlopen(req, timeout=120).read()
    except Exception as e:
        LOG.append(dict(ano=y, url=url, erro=str(e))); print(y, "ERRO", e); continue
    sha = hashlib.sha256(data).hexdigest()
    try:
        z = zipfile.ZipFile(io.BytesIO(data)); csvb = z.read("tdor_export.csv")
        (RAW / f"tdor_br_{y}.csv").write_bytes(csvb)
        n = csvb.decode("utf-8-sig").count("\n,") # placeholder, contagem real em s02
    except Exception as e:
        (RAW / f"tdor_br_{y}.bin").write_bytes(data); LOG.append(dict(ano=y, url=url, sha256_zip=sha, erro="nao-zip:" + str(e))); print(y, "nao zip", len(data)); continue
    LOG.append(dict(ano=y, url=url, sha256_zip=sha, bytes=len(data))); print(y, "ok", len(data))
    time.sleep(1)
(RAW / "fetch_log.json").write_text(json.dumps(LOG, indent=1, ensure_ascii=False))
