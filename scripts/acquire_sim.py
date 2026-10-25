"""Baixa e confere o microdado oficial: DATASUS SIM (DOBR2010-2024.dbc, ~1,6 GB).

Uso: python3 -I scripts/acquire_sim.py [--check]
    (--check só confere o que já está em disco, sem rede)
Destino: $REPO_ROOT/fontes/p2-sim-microdados/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Saída: 0 tudo confere; 1 falta/rede; 2 hash divergente (versão diferente da usada no estudo).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

if __name__ == "__main__":
    sys.exit(a.principal("SIM", "fontes/p2-sim-microdados", "--check" in sys.argv))
