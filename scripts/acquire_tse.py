# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Download and check the official TSE microdata.

Uses the shared acquisition routine to fetch the TSE candidate registries for 2010, 2014, 2018
and 2022 listed in the manifest and compare each
SHA-256 with the expected value. With --check it only verifies files already on disk, without
network. Exit code 0 means all files match, 1 a missing file or network failure, 2 a hash
different from the version used in the study.

Inputs
------
- manifest/MANIFESTO-FONTES.csv (rows of group TSE)
- official source URLs listed in the manifest (network)

Outputs
-------
- sources/public/p2-f8-governos/tse/ (downloaded files, not tracked in git)
- prints one status line per file to stdout

Usage
-----
python3 -I scripts/acquire_tse.py [--check]

Status
------
Data acquisition step; no analysis claim.

Notes
-----
Original description (Portuguese), kept verbatim:

Baixa e confere o microdado oficial: TSE consulta_cand 2010/2014/2018/2022.

Uso: python3 -I scripts/acquire_tse.py [--check]
    (--check só confere o que já está em disco, sem rede)
Destino: $REPO_ROOT/fontes/p2-f8-governos/tse/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Saída: 0 tudo confere; 1 falta/rede; 2 hash divergente (versão diferente da usada no estudo).

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

if __name__ == "__main__":
    sys.exit(a.principal("TSE", "sources/public/p2-f8-governos/tse", "--check" in sys.argv))
