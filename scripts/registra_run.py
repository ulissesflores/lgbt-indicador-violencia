"""Registro de uma execucao selada em runs/<UTC>/ (norma Codex Hash).

Roda depois de ``run_all.py --selar``: confere o selo com ``make_provenance.py --verify`` e grava
``manifest.json`` (commit, ambiente, pip freeze verbatim do ambiente que rodou, chain_hash) e
``checksums.sha256`` dos arquivos que o selo produz. ``runs/`` fica fora do selo porque guarda o
proprio chain_hash.

Uso: .run/venv/bin/python scripts/registra_run.py
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def main() -> int:
    """Confere o selo e grava o manifesto da execucao."""
    ver = subprocess.run(
        [sys.executable, str(RAIZ / "make_provenance.py"), "--verify"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
    )
    linha = ver.stdout.strip().splitlines()[-1] if ver.stdout.strip() else ""
    if ver.returncode or not linha.startswith("provenance verified:"):
        print(f"[FALHA] selo nao confere: {linha or ver.stderr.strip()}")
        return 1
    chain = linha.split()[2]
    agora = datetime.now(UTC)
    run_id = agora.strftime("%Y%m%dT%H%M%SZ")
    pasta = RAIZ / "runs" / run_id
    pasta.mkdir(parents=True)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True
    ).stdout.strip()
    sujo = bool(
        subprocess.run(
            ["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True
        ).stdout
    )
    freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True
    ).stdout.split()
    manifesto = {
        "run_id": run_id,
        "created_utc": agora.isoformat(),
        "command": "python run_all.py --selar && python scripts/registra_run.py",
        "git": {"commit": commit, "working_tree_dirty": sujo},
        "chain_hash": chain,
        "sealed_files": int(linha.split("(")[1].split()[0]),
        "environment": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "architecture": platform.machine(),
            "pip_freeze": freeze,
        },
    }
    (pasta / "manifest.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    arqs = [
        "output/hash-chain.md",
        "output/provenance.json",
        "requirements.txt",
        "requirements.lock",
    ]
    linhas = [
        f"{hashlib.sha256((RAIZ / a).read_bytes()).hexdigest()}  {a}"
        for a in arqs
        if (RAIZ / a).exists()
    ]
    (pasta / "checksums.sha256").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(
        f"[OK] runs/{run_id}: chain {chain[:12]}…, {len(freeze)} pacotes, {len(linhas)} checksums"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
