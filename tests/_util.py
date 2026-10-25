"""Leitores mínimos (biblioteca padrão) dos arquivos derivados usados pelos testes."""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R3 = RAIZ / "research-2026-10-21-rodada3"


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
