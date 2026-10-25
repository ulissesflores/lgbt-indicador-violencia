"""Núcleo comum dos scripts acquire_*.py.

Baixa o microdado oficial e confere o SHA-256 esperado do manifesto.

O SHA-256 esperado de cada arquivo vem de manifest/MANIFESTO-FONTES.csv (parte B-bruto), gravado no
dia do download usado no estudo. Arquivos preliminares do DATASUS (SIM 2023-24, Sinan recente) podem
ter sido regerados na origem: se o hash divergir, o arquivo novo NÃO é a versão do estudo; o script
avisa, guarda o baixado como <nome>.divergente e sai com código 2.

Destino: $REPO_ROOT/fontes/... (ignorado pelo git). Sem REPO_ROOT, usa a raiz do repositório.
"""

import csv
import hashlib
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[1])
MANIFESTO = Path(__file__).resolve().parents[1] / "manifest" / "MANIFESTO-FONTES.csv"


def sha256(path):
    """SHA-256 de um arquivo, lido em blocos de 1 MiB."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def linhas_manifesto(grupo):
    """Linhas B-bruto do manifesto para um grupo (SIM, Sinan, TSE, PNS 2019)."""
    with open(MANIFESTO, encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh) if r["parte"] == "B-bruto" and r["grupo"] == grupo]


def baixa(url, destino):
    """Baixa url (http/https/ftp) para destino com curl, retomando se interrompido."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sS", "-fL", "--retry", "3", "-C", "-", "-o", str(destino), url]
    return subprocess.run(cmd).returncode == 0


def garante(linha, pasta, so_conferir=False):
    """Garante que pasta/<nome> exista com o hash esperado.

    Devolve 0 ok, 1 falha de rede/ausência, 2 hash divergente.
    """
    nome = linha["id"]
    destino = pasta / nome
    esperado = linha["sha256"]
    if destino.exists() and sha256(destino) == esperado:
        print(f"[ok] {nome} já presente, sha256 confere")
        return 0
    if so_conferir:
        print(f"[falta] {nome}")
        return 1
    print(f"[baixando] {linha['url']}")
    if not baixa(linha["url"], destino):
        print(f"[erro] download falhou: {linha['url']}")
        return 1
    obtido = sha256(destino)
    if obtido != esperado:
        destino.rename(destino.with_name(nome + ".divergente"))
        print(
            f"[DIVERGE] {nome}: esperado {esperado}, obtido {obtido} "
            f"(guardado como {nome}.divergente)"
        )
        return 2
    print(f"[ok] {nome} sha256 confere")
    return 0


def principal(grupo, pasta_rel, so_conferir):
    """Itera todas as linhas do grupo; código de saída = maior código de falha."""
    pasta = REPO_ROOT / pasta_rel
    rc = 0
    for linha in linhas_manifesto(grupo):
        rc = max(rc, garante(linha, pasta, so_conferir))
    return rc


if __name__ == "__main__":
    sys.exit(
        "módulo de apoio; rode scripts/acquire_sim.py, acquire_sinan.py, "
        "acquire_pns2019.py ou acquire_tse.py"
    )
