"""Baixa e confere a PNS 2019 (microdados + dicionário/layout).

Prepara os arquivos que dados/pns/seguro_pns2019.py lê.

Uso: python3 -I scripts/acquire_pns2019.py [--check]
Destino: $REPO_ROOT/fontes/q1-textointegral/F2/pns2019/ (ignorado pelo git). Hash esperado:
manifest/MANIFESTO-FONTES.csv.
Prepara: x/PNS_2019.txt (extraído do zip, 455 MB) e input_PNS_2019_utf8.txt (layout
input_PNS_2019.txt decodificado de latin-1 para UTF-8, byte a byte igual ao usado no estudo: sha256
c569fd59...8f78).
"""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire as a

PASTA = "fontes/q1-textointegral/F2/pns2019"

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
