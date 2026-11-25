# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Download and check the PNS 2019 microdata and its dictionary and layout files.

Uses the shared acquisition routine to fetch the PNS 2019 files listed in the manifest and
verify their SHA-256. When all files are present and valid, it extracts the microdata text file
from the zip archive and rewrites the layout file from latin-1 to UTF-8, the form read by the
PNS analysis script. With --check it only verifies files already on disk, without network.

Inputs
------
- manifest/MANIFESTO-FONTES.csv
- official PNS 2019 download URLs listed in the manifest (network)
- sources/public/q1-textointegral/F2/pns2019/PNS_2019_20220525.zip (not tracked in git)
- sources/public/q1-textointegral/F2/pns2019/Dicionario_e_input_20220530.zip (not tracked in
  git)

Outputs
-------
- sources/public/q1-textointegral/F2/pns2019/x/PNS_2019.txt (not tracked in git)
- sources/public/q1-textointegral/F2/pns2019/input_PNS_2019_utf8.txt (not tracked in git)
- prints one status line per file to stdout; exit code 0, 1 or 2 as in scripts/_acquire.py

Usage
-----
python3 -I scripts/acquire_pns2019.py [--check]

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Baixa e confere a PNS 2019 (microdados + dicionário/layout).

Prepara os arquivos que data/pns/seguro_pns2019.py lê.

Uso: python3 -I scripts/acquire_pns2019.py [--check]
Destino: $REPO_ROOT/fontes/q1-textointegral/F2/pns2019/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Prepara: x/PNS_2019.txt (extraído do zip, 455 MB) e input_PNS_2019_utf8.txt (layout
input_PNS_2019.txt decodificado de latin-1 para UTF-8, byte a byte igual ao usado no estudo: sha256
c569fd59...8f78).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

PASTA = "sources/public/q1-textointegral/F2/pns2019"

if __name__ == "__main__":
    so = "--check" in sys.argv
    rc = a.principal("PNS 2019", PASTA, so)
    if rc == 0 and not so:
        base = a.REPO_ROOT / PASTA
        with zipfile.ZipFile(base / "PNS_2019_20220525.zip") as z:
            if not (base / "x" / "PNS_2019.txt").exists():
                z.extract("PNS_2019.txt", base / "x")
        with zipfile.ZipFile(base / "Dicionario_e_input_20220530.zip") as z:
            (base / "input_PNS_2019_utf8.txt").write_bytes(
                z.read("input_PNS_2019.txt").decode("latin-1").encode("utf-8")
            )
        print("[ok] x/PNS_2019.txt e input_PNS_2019_utf8.txt prontos")
    sys.exit(rc)
