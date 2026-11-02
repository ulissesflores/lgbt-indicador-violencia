"""Selo do pré-registro: confere o sha256 do PREREGISTRO-D100.md (corpo até a linha '**ADENDOS**') e dos scripts
de regras e tabulação contra PREREGISTRO-D100.sha256. Qualquer divergência aborta a tabulação.

Uso direto: /opt/homebrew/bin/python3.14 -I scripts/d100_selo.py  (imprime ok ou o que divergiu)
"""

import hashlib
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SELO = BASE / "PREREGISTRO-D100.sha256"
MARCA = "**ADENDOS**"


def corpo_prereg():
    t = (BASE / "PREREGISTRO-D100.md").read_bytes()
    i = t.find(MARCA.encode())
    if i < 0:
        raise SystemExit("PREREGISTRO-D100.md sem a marca de ADENDOS")
    return t[:i]


def atuais():
    return {
        "PREREGISTRO-D100.md#corpo": hashlib.sha256(corpo_prereg()).hexdigest(),
        "scripts/d100_comum.py": hashlib.sha256((BASE / "scripts/d100_comum.py").read_bytes()).hexdigest(),
    }


def conferir():
    if not SELO.exists():
        raise SystemExit("PREREGISTRO-D100.sha256 não existe: nada é tabulado antes do selo")
    gravado = {}
    for ln in SELO.read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            h, nome = ln.split(None, 1)
            gravado[nome.strip()] = h
    for nome, h in atuais().items():
        if gravado.get(nome) != h:
            raise SystemExit(f"selo divergente: {nome}")
    return True


def gravar(utc):
    linhas = [f"# gravado {utc} (UTC), antes de qualquer tabulação de desfecho"]
    linhas += [f"{h}  {n}" for n, h in atuais().items()]
    for n in ("scripts/d100_tabular.py", "scripts/d100_series.py", "scripts/d100_estrutura.py"):
        linhas.append(f"# info (não travado; mudança vira adendo): {hashlib.sha256((BASE / n).read_bytes()).hexdigest()}  {n}")
    SELO.write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--gravar":
        gravar(sys.argv[2])
    print("ok" if conferir() else "falhou")
