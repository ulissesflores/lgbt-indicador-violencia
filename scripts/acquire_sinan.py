"""Baixa e confere o microdado oficial: DATASUS Sinan (VIOLBR15-25.dbc, ~300 MB).

Uso: python3 -I scripts/acquire_sinan.py [--check]
    (--check só confere o que já está em disco, sem rede)
Destino: $REPO_ROOT/fontes/p2-sinan-microdados/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Saída: 0 tudo confere; 1 falta/rede; 2 hash divergente (versão diferente da usada no estudo).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

if __name__ == "__main__":
    sys.exit(a.principal("Sinan", "fontes/p2-sinan-microdados", "--check" in sys.argv))
