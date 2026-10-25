"""OpenAlex (API publica sem chave): contagem por ano de obras cujo TITULO+RESUMO casam cada consulta OA.
Cota sem chave compartilhada (US$ 0,10/dia/IP); cada consulta ~US$ 0,001. Salva bruto + sha256.
Uso: openalex_contar.py contar | amostra"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, json, os, sys, time, urllib.parse, urllib.request, urllib.error, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d
RAW = (REPO_ROOT + "/fontes/q1-textointegral/discurso/midia/openalex")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia/_bruto_openalex.csv")
UA = {"User-Agent": "pesquisa-lgbt-midia/1.0 (leitura publica)"}


def get(u):
    for t in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read()[:300]
            sys.stderr.write("HTTP %s %r\n" % (e.code, body))
            if e.code in (429, 402) and b"Insufficient budget" in body:
                raise SystemExit("cota OpenAlex esgotada: " + repr(body))
            time.sleep(4)
        except Exception as e:
            time.sleep(3)
    raise RuntimeError(u)


def filtro(q, extra=""):
    return "title_and_abstract.search:" + q + ",from_publication_date:2015-01-01,to_publication_date:2026-10-21" + extra


if __name__ == "__main__":
    modo = sys.argv[1]
    os.makedirs(RAW, exist_ok=True)
    hoje = datetime.date.today().isoformat()
    if modo == "contar":
        novo = not os.path.exists(OUT)
        f = open(OUT, "a", newline="")
        w = csv.writer(f)
        if novo:
            w.writerow(["familia", "universo", "ano", "n", "consulta", "data_acesso", "sha256"])
        gasto = 0
        for id_, fam, rot, q in d.OA:
            u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": filtro(q), "group_by": "publication_year", "per-page": "200"}, quote_via=urllib.parse.quote)
            body = get(u)
            h = hashlib.sha256(body).hexdigest()
            open(f"{RAW}/{id_}_{h[:10]}.json", "wb").write(body)
            j = json.loads(body)
            gasto += j["meta"].get("cost_usd", 0)
            tot = 0
            for g in j["group_by"]:
                w.writerow([fam, "OpenAlex", g["key"], g["count"], id_ + " | " + q, hoje, h]); tot += g["count"]
            w.writerow([fam, "OpenAlex", "total", tot, id_ + " | " + q, hoje, h])
            print(id_, tot, flush=True)
            time.sleep(1)
        print("gasto US$", gasto)
        amostra_e_uniao()


def reconstroi(inv):
    if not inv:
        return ""
    pos = {}
    for pal, ps in inv.items():
        for p in ps:
            pos[p] = pal
    return " ".join(pos[i] for i in sorted(pos))


def uniao(fam):
    qs = [q for (_, f, _, q) in d.OA if f == fam]
    return " OR ".join("(" + q + ")" for q in qs)


def amostra_e_uniao():
    hoje = datetime.date.today().isoformat()
    w = csv.writer(open(OUT, "a", newline=""))
    for fam in ("F1", "F2", "F3", "F4"):
        q = uniao(fam)
        u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": filtro(q), "group_by": "publication_year", "per-page": "200"}, quote_via=urllib.parse.quote)
        body = get(u); h = hashlib.sha256(body).hexdigest()
        open(f"{RAW}/{fam}-any_{h[:10]}.json", "wb").write(body)
        tot = 0
        for g in json.loads(body)["group_by"]:
            w.writerow([fam, "OpenAlex", g["key"], g["count"], fam + "-any | " + q, hoje, h]); tot += g["count"]
        w.writerow([fam, "OpenAlex", "total", tot, fam + "-any | " + q, hoje, h])
        u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": filtro(q), "sample": "60", "seed": str(d.SEMENTE), "per-page": "60",
            "select": "id,doi,title,publication_year,abstract_inverted_index,primary_location"}, quote_via=urllib.parse.quote)
        body = get(u); h = hashlib.sha256(body).hexdigest()
        open(f"{RAW}/{fam}-amostra60_{h[:10]}.json", "wb").write(body)
        print(fam, "uniao", tot, "amostra", len(json.loads(body)["results"]), flush=True)
        time.sleep(1)


if __name__ == "__main__" and sys.argv[1] == "amostra":
    amostra_e_uniao()
