"""Catálogo dos 23 arquivos de microdados do Disque 100: URL, tamanho anunciado e local, Last-Modified,
data de acesso, formato (pelo cabeçalho) e sha256 do arquivo inteiro baixado (ou 'parcial, sem sha').

Uso: /opt/homebrew/bin/python3.14 -I scripts/d100_catalogo.py
Saída: saidas/catalogo.tsv
"""

import csv
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d100_comum as dc  # noqa: E402

ACESSO = "2026-10-24"
PAGINA = "https://www.gov.br/mdh/pt-br/acesso-a-informacao/dados-abertos/disque100/"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main():
    linhas = list(csv.DictReader(open(dc.BASE / "scripts/urls.tsv", encoding="utf-8"), delimiter="\t"))
    out = []
    for r in linhas:
        p = dc.RAW / Path(r["url"]).name
        n = int(r["bytes_anunciados"])
        local = p.stat().st_size if p.exists() else 0
        completo = local == n
        fmt = ""
        if completo:
            with open(p, encoding="utf-8-sig") as f:
                fmt = dc.formato([c.strip() for c in f.readline().strip().split(";")])
        out.append(dict(periodo=r["periodo"], formato=fmt, url=r["url"], pagina_catalogo=PAGINA + r["pagina_catalogo"],
                        bytes_anunciados=n, bytes_local=local, last_modified=r["last_modified"], data_acesso=ACESSO,
                        sha256=sha256(p) if completo else "", status="completo" if completo else "parcial_sem_sha"))
        print(r["periodo"], out[-1]["status"], out[-1]["sha256"][:12], flush=True)
    with open(dc.BASE / "saidas/catalogo.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
