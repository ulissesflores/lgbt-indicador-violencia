# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Catalogue the 23 Disque 100 microdata files with size, format and SHA-256.

For each row of scripts/urls.tsv the script compares the announced size with the local file in
raw/. For complete files it reads the header line to detect the file format and hashes the
whole file with SHA-256; incomplete files are marked as partial without a hash. The access
date and the catalogue page URL are constants in the script.

Inputs
------
- data/disque100/scripts/urls.tsv
- data/disque100/raw/<file>.csv (not tracked in git)
- data/disque100/scripts/d100_comum.py (shared rules, imported)

Outputs
-------
- data/disque100/saidas/catalogo.tsv
- prints one line per period with its status and the start of the hash

Usage
-----
python3 -I scripts/d100_catalogo.py   (run from data/disque100)

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Catálogo dos 23 arquivos de microdados do Disque 100: URL, tamanho anunciado e local, Last-Modified,
data de acesso, formato (pelo cabeçalho) e sha256 do arquivo inteiro baixado (ou 'parcial, sem sha').

Uso: python3 -I scripts/d100_catalogo.py
Saída: saidas/catalogo.tsv

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
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
