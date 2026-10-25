"""Entry-point único: integridade, recálculo, testes e selo de proveniência.

Cadeia: integridade -> recálculo na réplica -> testes dos números publicados -> selo de
proveniência.

Uso:
    python3 -I run_all.py            # completo (~5 min): Trilha 1 (ver REPRODUCIBILITY.md)
    python3 -I run_all.py --rapido   # sem o recálculo: integridade + testes + selo (segundos)
    python3 -I run_all.py --selar    # regrava o inventário público, manifest/SHA256SUMS.txt
                                     # e output/provenance.json (só depois de mudar dado ou código)
                                     # e roda o resto

Dependências: numpy, pandas, scipy, matplotlib (requirements.txt). Os testes rodam com ou sem
pytest.
"""

import runpy
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def py(*args):
    """Roda um script Python da raiz em modo isolado e devolve o código de saída."""
    return subprocess.run([sys.executable, "-B", "-I", *map(str, args)], cwd=str(RAIZ)).returncode


def rodar_testes():
    """Roda cada função test_* de tests/test_*.py sem depender de pytest.

    Teste que se pula sozinho (pasta de origem fora do repositório ausente: ``pytest.skip`` ou
    ``_Pulo``) é contado à parte, nunca como passou.

    Returns
    -------
    tuple of (int, int, int)
        (passaram, total sem os pulados, pulados).
    """
    ok = total = pulados = 0
    for arq in sorted(
        [*(RAIZ / "tests").glob("test_*.py"), *(RAIZ / "paper" / "tests").glob("test_*.py")]
    ):
        mod = runpy.run_path(str(arq))
        for nome, fn in mod.items():
            if nome.startswith("test_") and callable(fn):
                try:
                    fn()
                    ok += 1
                    total += 1
                    print(f"[ok] {arq.name}::{nome}")
                except AssertionError as erro:
                    total += 1
                    print(f"[FALHOU] {arq.name}::{nome}: {str(erro)[:400]}")
                except BaseException as erro:  # Skipped do pytest herda de BaseException
                    if type(erro).__name__ not in ("Skipped", "_Pulo"):
                        raise
                    pulados += 1
                    print(f"[pulado] {arq.name}::{nome}: {str(erro)[:200]}")
    return ok, total, pulados


def main():
    """Roda integridade, recálculo, testes e selo; devolve 0 só se tudo passar.

    Com ``--selar``, antes regrava o inventário público (``scripts/inventario_publico.py``) e o
    selo.
    """
    if "--selar" in sys.argv and (
        py("scripts/inventario_publico.py") or py("make_provenance.py", "--build")
    ):
        return 1
    if py("make_provenance.py", "--verify"):
        print(
            "integridade FALHOU: arquivo alterado depois do selo "
            "(rode --selar só se a mudança foi intencional)"
        )
        return 1
    if "--rapido" not in sys.argv and py("scripts/reproduzir.py"):
        print("recálculo FALHOU")
        return 1
    ok, total, pulados = rodar_testes()
    print(f"testes: {ok}/{total} passaram" + (f" ({pulados} pulados)" if pulados else ""))
    if ok != total:
        return 1
    return py("make_provenance.py", "--verify")


if __name__ == "__main__":
    sys.exit(main())
