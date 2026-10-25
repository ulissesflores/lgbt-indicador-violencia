"""Baixa e confere o microdado oficial: TSE consulta_cand 2010/2014/2018/2022.

Uso: python3 -I scripts/acquire_tse.py [--check]
    (--check só confere o que já está em disco, sem rede)
Destino: $REPO_ROOT/fontes/p2-f8-governos/tse/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Saída: 0 tudo confere; 1 falta/rede; 2 hash divergente (versão diferente da usada no estudo).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

if __name__ == "__main__":
    sys.exit(a.principal("TSE", "fontes/p2-f8-governos/tse", "--check" in sys.argv))
