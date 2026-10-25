"""Wikipedia pt/en/es: paginas que casam cada entrada (string GDELT sem filtros), via action=query&list=search.
Retrato do dia (sem serie). Salva bruto + sha256 e uma lista de paginas (pageid, titulo, snippet)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, datetime, hashlib, json, os, sys, time, urllib.parse, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d
RAW = (REPO_ROOT + "/fontes/q1-textointegral/discurso/midia/wikipedia")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia/_bruto_wikipedia.csv")
UA = {"User-Agent": "pesquisa-lgbt-midia/1.0 (leitura publica)"}


def get(u):
    for t in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(8 * (t + 1))
    raise RuntimeError(u)

import re
# ADENDO pos-contagem: a 1a rodada (string GDELT inteira) deu contagens sem sentido em entradas
# coocc e estourou o limite de 300 caracteres do CirrusSearch. Versao final: cada FRASE entre
# aspas de entradas tipo 'frase' autossuficientes e buscada isoladamente; uniao de paginas por entrada.
AUTOSSUF = {"F1-PT-01","F1-PT-02","F1-PT-03","F1-EN-01","F1-ES-01","F2-PT-01","F2-EN-01","F3-PT-01","F3-PT-03","F3-PT-05","F3-EN-01","F3-ES-01","F4-PT-01","F4-PT-04"}

if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    hoje = datetime.date.today().isoformat()
    f = open(OUT, "w", newline=""); w = csv.writer(f)
    w.writerow(["familia", "universo", "ano", "n", "consulta", "data_acesso", "sha256"])
    paginas = {}
    for e in d.E:
        if e["id"] not in AUTOSSUF:
            continue
        lg = e["lang"]
        frases = re.findall(r'"([^"]+)"', e["gdelt"].split(") (")[0] if e["id"] != "F3-EN-01" else e["gdelt"])
        frases = [x for x in frases if x.lower() not in ("licence to kill","license to kill")] if e["id"]=="F3-EN-01" else frases
        vistos = {}
        hs = []
        for fr in frases:
            u = f"https://{lg}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": '"' + fr + '"', "srnamespace": "0", "srlimit": "500", "srprop": "snippet", "format": "json"}, quote_via=urllib.parse.quote)
            try:
                body = get(u)
            except Exception:
                sys.stderr.write(f"{e['id']} {fr} FALHOU apos tentativas\n"); hs.append('FALHA'); continue
            h = hashlib.sha256(body).hexdigest(); hs.append(h)
            open(f"{RAW}/{e['id']}_{h[:10]}.json", "wb").write(body)
            j = json.loads(body)
            if "error" in j:
                sys.stderr.write(f"{e['id']} {fr} erro {j['error']['code']}\n"); continue
            for p in j["query"]["search"]:
                vistos[p["pageid"]] = {"pageid": p["pageid"], "title": p["title"], "snippet": p["snippet"], "frase": fr}
            time.sleep(0.4)
        paginas[e["id"]] = list(vistos.values())
        w.writerow([e["fam"], f"Wikipedia-{lg}", "snapshot", len(vistos), e["id"] + " | " + " ; ".join(frases), hoje, hashlib.sha256("".join(hs).encode()).hexdigest()])
        print(e["id"], lg, len(vistos), flush=True)
    json.dump(paginas, open(OUT.replace("_bruto_wikipedia.csv", "_paginas_wikipedia.json"), "w"), ensure_ascii=False)
