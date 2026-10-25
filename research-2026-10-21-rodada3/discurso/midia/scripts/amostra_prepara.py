"""Monta os quadros de amostra (60 por familia x universo, semente pre-registrada) a partir dos itens casados.
Saida: midia/_amostra_<universo>.jsonl (um item por linha, com id/hash, url, data, familia, entrada, trecho, fontes)
Universos: Parlamento (Camara+Senado), GNRSS-pt, GNRSS-mundo (en+es), OpenAlex, Wikipedia.
Uso: amostra_prepara.py parlamento|gnrss|openalex|wikipedia"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import hashlib, json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d

BASE = REPO_ROOT
OUT = BASE + "/research-2026-10-21-rodada3/discurso/midia"
FONTES = {k: re.compile(v, re.I) for k, v in d.FONTES.items()}


def sorteia(itens, fam, universo, n=60):
    itens = sorted(itens, key=lambda x: x["hash"])  # ordem canonica antes do sorteio
    rnd = random.Random(f"{d.SEMENTE}-{fam}-{universo}")
    if len(itens) <= n:
        return itens, "censo"
    return rnd.sample(itens, n), "amostra60"


def grava(universo, por_fam):
    f = open(f"{OUT}/_amostra_{universo}.jsonl", "w")
    resumo = {}
    for fam in ("F1", "F2", "F3", "F4"):
        its = por_fam.get(fam, [])
        amostra, modo = sorteia(its, fam, universo)
        resumo[fam] = (len(its), len(amostra), modo)
        for x in amostra:
            x.update({"familia": fam, "universo": universo, "modo": modo, "n_universo_familia": len(its)})
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    print(universo, resumo)


if __name__ == "__main__":
    modo = sys.argv[1]
    por = {}
    if modo == "parlamento":
        for l in open(OUT + "/_parlamento_matches.jsonl"):
            j = json.loads(l)
            for fam in j["familias"]:
                por.setdefault(fam, []).append({"hash": j["id"], "url": j["url"], "data": j["data"][:10], "autor": j["autor"], "casa": j["casa"],
                                                "entradas": [e for e in j["entradas"] if e.startswith(fam)], "trecho": j["trecho"], "fontes": j["fontes"]})
        grava("Parlamento", por)
    elif modo == "gnrss":
        vistos = {}
        for l in open(OUT + "/_gnrss_celulas.jsonl"):
            c = json.loads(l)
            fam = c["entrada"][:2]
            lang = c["entrada"].split("-")[1].lower()
            for it in c["itens"]:
                chave = (fam, hashlib.sha256((it["link"] or it["titulo"]).encode()).hexdigest())
                v = vistos.setdefault(chave, {"hash": chave[1], "url": it["link"], "data": it["data"], "titulo": it["titulo"], "fonte": it["fonte"], "lang": lang, "entradas": []})
                v["entradas"].append(c["entrada"])
        pt, mundo = {}, {}
        for (fam, _), v in vistos.items():
            (pt if v["lang"] == "pt" else mundo).setdefault(fam, []).append(v)
        grava("GNRSS-pt", pt)
        grava("GNRSS-mundo", mundo)
    elif modo == "openalex":
        raw = BASE + "/fontes/q1-textointegral/discurso/midia/openalex"
        import glob
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import openalex_contar as oc
        f = open(OUT + "/_amostra_OpenAlex.jsonl", "w")
        for fam in ("F1", "F2", "F3", "F4"):
            fn = sorted(glob.glob(f"{raw}/{fam}-amostra60_*.json"))
            if not fn:
                continue
            for r in json.load(open(fn[-1]))["results"]:
                f.write(json.dumps({"hash": hashlib.sha256(r["id"].encode()).hexdigest(), "url": r.get("doi") or r["id"], "data": str(r["publication_year"]),
                                    "familia": fam, "universo": "OpenAlex", "titulo": r.get("title"), "trecho": oc.reconstroi(r.get("abstract_inverted_index"))[:700]}, ensure_ascii=False) + "\n")
    elif modo == "wikipedia":
        pag = json.load(open(OUT + "/_paginas_wikipedia.json"))
        for eid, ps in pag.items():
            fam = eid[:2]
            for p in ps:
                lang = eid.split("-")[1].lower()
                por.setdefault(fam, []).append({"hash": hashlib.sha256(f"{lang}-{p['pageid']}".encode()).hexdigest(), "url": f"https://{lang}.wikipedia.org/?curid={p['pageid']}",
                                                "data": "snapshot-2026-10-22", "titulo": p["title"], "trecho": re.sub("<[^>]+>", "", p["snippet"]), "entradas": [eid], "frase": p["frase"]})
        # uma pagina pode casar varias entradas: dedupe por hash dentro da familia
        for fam in por:
            u = {}
            for x in por[fam]:
                if x["hash"] in u:
                    u[x["hash"]]["entradas"] += x["entradas"]
                else:
                    u[x["hash"]] = x
            por[fam] = list(u.values())
        grava("Wikipedia", por)
