"""A API da Camara devolve HTTP 500 em certas paginas (a ultima) de deputados com muitos discursos.
Recuperacao para os deputados com falha em camara_baixar.py: janelas de 1 ano; se uma pagina da 500,
tenta itens menores (50, 20, 10) e, persistindo, janelas mensais. Salva {id}_y{ano}_{pag}.json (ou _m{mes}).
Registra o que NAO foi recuperado em _recuperacao_perdas.json."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import calendar, hashlib, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
RAW = (REPO_ROOT + "/fontes/q1-textointegral/discurso/midia/camara")
API = "https://dadosabertos.camara.leg.br/api/v2"


def get(u):
    for t in range(3):
        try:
            req = urllib.request.Request(u, headers={"Accept": "application/json", "User-Agent": "pesquisa-lgbt-midia/1.0 (leitura publica)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 500:
                return None
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None


def janela(did, tag, ini, fim, perdas):
    pag, itens = 1, 100
    while True:
        fn = f"{RAW}/{did}_{tag}_{pag}.json"
        if os.path.exists(fn):
            body = open(fn, "rb").read()
        else:
            body = get(f"{API}/deputados/{did}/discursos?dataInicio={ini}&dataFim={fim}&itens={itens}&pagina={pag}&ordenarPor=dataHoraInicio&ordem=ASC")
            if body is None:
                # 500: reduzir itens, depois dividir a janela
                for it in (50, 20, 10, 5):
                    body = get(f"{API}/deputados/{did}/discursos?dataInicio={ini}&dataFim={fim}&itens={it}&pagina=1&ordenarPor=dataHoraInicio&ordem=ASC")
                    if body is not None:
                        break
                if body is None:
                    perdas.append([did, tag, ini, fim, pag])
                    return
                # com itens menores a paginacao muda: baixar tudo da janela com esse tamanho
                return janela_itens(did, tag, ini, fim, it, perdas)
            open(fn, "wb").write(body)
        d = json.loads(body)
        if not any(l["rel"] == "next" for l in d["links"]):
            return
        pag += 1


def janela_itens(did, tag, ini, fim, it, perdas):
    pag = 1
    while True:
        fn = f"{RAW}/{did}_{tag}i{it}_{pag}.json"
        body = open(fn, "rb").read() if os.path.exists(fn) else get(f"{API}/deputados/{did}/discursos?dataInicio={ini}&dataFim={fim}&itens={it}&pagina={pag}&ordenarPor=dataHoraInicio&ordem=ASC")
        if body is None:
            perdas.append([did, tag + f"i{it}", ini, fim, pag]); return
        open(fn, "wb").write(body)
        if not any(l["rel"] == "next" for l in json.loads(body)["links"]):
            return
        pag += 1


def dep(did):
    perdas = []
    for a in range(2015, 2027):
        fim = f"{a}-12-31" if a < 2026 else "2026-10-21"
        janela(did, f"y{a}", f"{a}-01-01", fim, perdas)
    return did, perdas


if __name__ == "__main__":
    falhas = json.load(open(RAW + "/_falhas.json"))
    perdas = []
    with ThreadPoolExecutor(4) as ex:
        for did, p in ex.map(dep, falhas):
            perdas += p
            print(did, len(p), flush=True)
    json.dump(perdas, open(RAW + "/_recuperacao_perdas.json", "w"))
    print("PERDAS", len(perdas))
