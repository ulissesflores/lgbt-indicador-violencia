"""Baixa os 23 CSV de microdados do Disque 100 para raw/ por pedaços (HTTP Range), com retomada.

Por quê por pedaços: o servidor (dadosabertos.mdh.gov.br) responde o GET inteiro em
`Transfer-Encoding: chunked` sem Content-Length e limita cada conexão a ~50-85 KB/s
(medido em 2026-10-24); com Range ele devolve 206 e o tamanho total. Só stdlib, sem cookie
persistido, sem cadastro, sem aceite de termos.

Uso: /opt/homebrew/bin/python3.14 -I scripts/baixar.py [--workers 24] [--pedaco-mb 4]
Saída: raw/<arquivo>.csv (arquivo final só aparece quando todos os pedaços chegaram e o
tamanho bate com o anunciado em scripts/urls.tsv); estado de retomada em raw/<arquivo>.csv.partes.
"""

import argparse
import concurrent.futures as cf
import os
import sys
import threading
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "raw"
UA = "Mozilla/5.0 (pesquisa academica; download de dados abertos)"


def ler_urls():
    linhas = (BASE / "scripts" / "urls.tsv").read_text(encoding="utf-8").splitlines()
    cab = linhas[0].split("\t")
    for ln in linhas[1:]:
        d = dict(zip(cab, ln.split("\t")))
        yield d["url"], int(d["bytes_anunciados"])


def baixar_pedaco(url, ini, fim, tentativas=12):
    esperado = fim - ini + 1
    for t in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={ini}-{fim}", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                if r.status != 206:
                    raise OSError(f"status {r.status}")
                dados = r.read()
            if len(dados) != esperado:
                raise OSError(f"tamanho {len(dados)} != {esperado}")
            return dados
        except Exception as e:  # rede instável: tenta de novo com espera crescente
            if t == tentativas - 1:
                raise
            time.sleep(min(60, 5 * (t + 1)))
            print(f"  retry {Path(url).name} {ini}: {e}", file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--pedaco-mb", type=int, default=4)
    a = ap.parse_args()
    passo = a.pedaco_mb * 1024 * 1024
    RAW.mkdir(exist_ok=True)
    tarefas, arquivos = [], {}
    for url, n in ler_urls():
        final = RAW / Path(url).name
        if final.exists() and final.stat().st_size == n:
            continue
        part = final.with_suffix(".csv.part")
        estado = final.with_suffix(".csv.partes")
        feitos = set(int(x) for x in estado.read_text().split()) if estado.exists() else set()
        if not part.exists() or part.stat().st_size != n:
            with open(part, "wb") as f:
                f.truncate(n)
            feitos = set()
            estado.write_text("")
        total = (n + passo - 1) // passo
        arquivos[url] = {"final": final, "part": part, "estado": estado, "faltam": total - len(feitos),
                         "lock": threading.Lock(), "n": n}
        for i in range(total):
            if i not in feitos:
                tarefas.append((url, i, i * passo, min(n, (i + 1) * passo) - 1))
    print(f"{len(arquivos)} arquivos, {len(tarefas)} pedaços", flush=True)

    def fazer(t):
        url, i, ini, fim = t
        dados = baixar_pedaco(url, ini, fim)
        info = arquivos[url]
        with info["lock"]:
            fd = os.open(info["part"], os.O_WRONLY)
            try:
                os.pwrite(fd, dados, ini)
                os.fsync(fd)
            finally:
                os.close(fd)
            with open(info["estado"], "a") as f:
                f.write(f"{i}\n")
            info["faltam"] -= 1
            if info["faltam"] == 0:
                os.replace(info["part"], info["final"])
                info["estado"].unlink()
                print(f"fim {info['final'].name} {info['final'].stat().st_size} esperado {info['n']}", flush=True)

    erros = 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for fut in cf.as_completed([ex.submit(fazer, t) for t in tarefas]):
            if fut.exception():
                erros += 1
                print(f"ERRO {fut.exception()}", file=sys.stderr, flush=True)
    print(f"concluido; pedaços com erro: {erros}", flush=True)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
