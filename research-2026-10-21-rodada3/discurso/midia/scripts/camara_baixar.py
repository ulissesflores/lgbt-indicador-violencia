"""Baixa TODOS os discursos de deputados (API publica Dados Abertos da Camara, sem chave)
2015-01-01..2026-10-21, legislaturas 55-57. Salva cada pagina bruta em RAW/<idDep>_<pag>.json
(retomavel). Depois MANIFESTO com sha256 de cada arquivo. Python: /opt/homebrew/bin/python3.14 -I."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import hashlib, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

RAW = (REPO_ROOT + "/fontes/q1-textointegral/discurso/midia/camara")
API = "https://dadosabertos.camara.leg.br/api/v2"
INI, FIM = "2015-01-01", "2026-10-21"


def get(u, tent=6):
    for t in range(tent):
        try:
            req = urllib.request.Request(u, headers={"Accept": "application/json", "User-Agent": "pesquisa-lgbt-midia/1.0 (leitura publica)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404,):
                return b'{"dados":[],"links":[]}'
            time.sleep(2 * (t + 1))
        except Exception:
            time.sleep(2 * (t + 1))
    raise RuntimeError("falhou: " + u)


def lista_deputados():
    ids = {}
    for leg in (55, 56, 57):
        pag = 1
        while True:
            d = json.loads(get(f"{API}/deputados?idLegislatura={leg}&itens=100&pagina={pag}&ordem=ASC&ordenarPor=id"))
            for x in d["dados"]:
                ids[x["id"]] = x["nome"]
            if not any(l["rel"] == "next" for l in d["links"]):
                break
            pag += 1
    return ids


JANELAS = [("2015-01-01", "2018-12-31"), ("2019-01-01", "2022-12-31"), ("2023-01-01", "2026-10-21")]  # API limita a 4 anos


def baixa_dep(did):
    n = 0
    for j, (ini, fim) in enumerate(JANELAS):
        pag = 1
        while True:
            fn = os.path.join(RAW, f"{did}_w{j}_{pag}.json")
            if os.path.exists(fn):
                body = open(fn, "rb").read()
            else:
                u = (f"{API}/deputados/{did}/discursos?dataInicio={ini}&dataFim={fim}&itens=100&pagina={pag}"
                     "&ordenarPor=dataHoraInicio&ordem=ASC")
                body = get(u)
                open(fn, "wb").write(body)
            d = json.loads(body)
            n += len(d["dados"])
            if not any(l["rel"] == "next" for l in d["links"]):
                break
            pag += 1
    return did, n


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    ids = lista_deputados()
    json.dump(ids, open(os.path.join(RAW, "_deputados.json"), "w"), ensure_ascii=False)
    print("deputados", len(ids), flush=True)
    tot = 0
    with ThreadPoolExecutor(5) as ex:
        def seguro(did):
            for _ in range(3):
                try:
                    return baixa_dep(did)
                except Exception as e:
                    time.sleep(5)
            falhas.append(did)
            return did, 0
        falhas = []
        for i, (did, n) in enumerate(ex.map(seguro, list(ids))):
            tot += n
            if i % 100 == 0:
                print(i, did, n, tot, flush=True)
    print("TOTAL discursos", tot, "falhas", falhas)
    json.dump(falhas, open(os.path.join(RAW, "_falhas.json"), "w"))
    with open(os.path.join(RAW, "_MANIFESTO.sha256"), "w") as f:
        for fn in sorted(os.listdir(RAW)):
            if fn.startswith("_MANIFESTO"):
                continue
            f.write(hashlib.sha256(open(os.path.join(RAW, fn), "rb").read()).hexdigest() + "  " + fn + "\n")
