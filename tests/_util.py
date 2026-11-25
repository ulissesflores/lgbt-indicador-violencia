# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Provide minimal standard-library readers of derived files for the test modules.

Defines the repository root and small helpers that read a CSV file as a list of dictionaries,
a text file, or a JSON file, all by path relative to the repository root, and a helper that
tests whether two numbers differ by at most a tolerance.

Inputs
------
- none (library module imported by the test files; the files it reads are chosen by the caller)

Outputs
-------
- none (library module imported by the test files)

Usage
-----
Imported by the test files in tests/; not run directly.

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Leitores mínimos (biblioteca padrão) dos arquivos derivados usados pelos testes.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R3 = RAIZ / "analysis"


def csv_rows(rel):
    """Linhas de um CSV (relativo à raiz do repo) como lista de dicionários."""
    with open(RAIZ / rel, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def texto(rel):
    """Conteúdo UTF-8 de um arquivo (relativo à raiz)."""
    return (RAIZ / rel).read_text(encoding="utf-8")


def json_(rel):
    """JSON de um arquivo (relativo à raiz)."""
    return json.loads(texto(rel))


def perto(a, b, tol):
    """True se |a-b| <= tol."""
    return abs(float(a) - float(b)) <= tol


def linha_md(rel, prefixo):
    """Primeira linha de um .md que começa com prefixo (após strip)."""
    for ln in texto(rel).splitlines():
        if ln.strip().startswith(prefixo):
            return ln
    raise AssertionError(f"linha com prefixo {prefixo!r} não encontrada em {rel}")


def celulas(ln):
    """Células de uma linha de tabela GFM."""
    return [c.strip() for c in ln.strip().strip("|").split("|")]


def nums(s):
    """Todos os números (com sinal e ponto decimal) de uma string."""
    return [float(x) for x in re.findall(r"[-+]?\d+(?:\.\d+)?", s.replace("−", "-"))]
