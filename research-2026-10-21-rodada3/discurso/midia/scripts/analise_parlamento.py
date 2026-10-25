"""Aplica o dicionario pre-registrado (regex locais) a TODOS os discursos baixados da Camara e
aos textos integrais candidatos do Senado. Saidas (em midia/): _bruto_parlamento.csv (contagens por
entrada x ano, uniao por familia x ano, denominadores), _parlamento_matches.jsonl (itens casados com
trecho e co-mencao de fontes). Python: /opt/homebrew/bin/python3.14 -I."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, datetime, glob, hashlib, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
MOD = sys.argv[1] if len(sys.argv) > 1 else 'dicionario_v2'  # v2 = correcao pos-contagem (ver PRE-REGISTRO, ADENDO)
d = importlib.import_module(MOD)

BASE = REPO_ROOT
CAM = BASE + "/fontes/q1-textointegral/discurso/midia/camara"
SEN = BASE + "/fontes/q1-textointegral/discurso/midia/senado"
OUT = BASE + "/research-2026-10-21-rodada3/discurso/midia"
hoje = datetime.date.today().isoformat()

REG = {e["id"]: d.compilar(e) for e in d.E}
REQ = {e["id"]: re.compile(e["requer"], re.I) for e in d.E if e.get("requer")}
FAM = {e["id"]: e["fam"] for e in d.E}
LANGPT = [e["id"] for e in d.E if e["lang"] == "pt"]  # parlamento brasileiro: so entradas PT
FONTES = {k: re.compile(v, re.I) for k, v in d.FONTES.items()}
GATE = re.compile(d.G + "|" + d.G_EN + r"|homofob\w*|transfob\w*|lgbtfob\w*|cura gay|licenca para matar|exterminio|genocidio|expectativa de vida|a cada \d+ horas|dados (?:falsos|inflados)|numeros (?:falsos|inflados)|grupo gay", re.I)


def dir_sha(path, pat):
    h = hashlib.sha256()
    for f in sorted(glob.glob(path + pat)):
        h.update(hashlib.sha256(open(f, "rb").read()).digest())
    return h.hexdigest()


def norm_map(s):
    """igual a d.norm, mas devolve tambem o indice de origem de cada caractere normalizado"""
    import unicodedata
    out, idx, prev_sp = [], [], False
    for i, ch in enumerate(s or ""):
        for c in unicodedata.normalize("NFKD", ch):
            if unicodedata.combining(c):
                continue
            c = c.lower()
            if c.isspace():
                if prev_sp:
                    continue
                c, prev_sp = " ", True
            else:
                prev_sp = False
            out.append(c); idx.append(i)
    return "".join(out), idx


def processa(item, casa, cnt_ent, cnt_fam, tot, out):
    texto = item["texto"]
    ano = item["data"][:4]
    tot[(casa, ano)] += 1
    if not GATE.search(d.norm(texto)):
        return
    t, idx = norm_map(texto)
    achou = {}
    for id_ in LANGPT:
        m = REG[id_].search(t)
        if m and id_ in REQ and not REQ[id_].search(t):
            m = None
        if m:
            achou[id_] = m
    if not achou:
        return
    fams = sorted({FAM[i] for i in achou})
    for i in achou:
        cnt_ent[(casa, i, ano)] += 1
    for f in fams:
        cnt_fam[(casa, f, ano)] += 1
    m0 = achou[sorted(achou)[0]]
    a, b = max(0, m0.start() - 220), min(len(t), m0.end() + 220)
    out.write(json.dumps({
        "id": item["id"], "casa": casa, "data": item["data"], "autor": item.get("autor", ""), "url": item.get("url", ""),
        "familias": fams, "entradas": sorted(achou), "trecho": texto[idx[a]:idx[min(b, len(idx)) - 1] + 1].replace("\n", " "),
        "fontes": [k for k, r in FONTES.items() if r.search(t)], "n_chars": len(t)}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    cnt_ent, cnt_fam, tot = Counter(), Counter(), Counter()
    out = open(OUT + ("/_v1prereg_matches_novo.jsonl" if MOD != "dicionario_v2" else "/_parlamento_matches.jsonl"), "w")
    vistos = set()
    deps = json.load(open(CAM + "/_deputados.json"))
    for fn in sorted(glob.glob(CAM + "/[0-9]*_*.json")):
        did = os.path.basename(fn).split("_")[0]
        j = json.load(open(fn))
        for x in j["dados"]:
            tx = (x.get("transcricao") or "") + " " + (x.get("sumario") or "") + " " + (x.get("keywords") or "")
            chave = hashlib.sha256((did + x["dataHoraInicio"] + tx).encode()).hexdigest()
            if chave in vistos:
                continue
            vistos.add(chave)
            processa({"id": chave, "data": x["dataHoraInicio"], "autor": deps.get(did, did), "url": x.get("urlTexto", ""), "texto": tx},
                     "Camara", cnt_ent, cnt_fam, tot, out)
    # Senado: todos os pronunciamentos (denominador) e texto integral dos candidatos
    cands = {c[0]: c for c in json.load(open(SEN + "/_candidatos.json"))}
    for fn in sorted(glob.glob(SEN + "/lista_*.json")):
        b = open(fn, "rb").read()
        if not b:
            continue
        sessoes = json.loads(b)["DiscursosSessao"]["Sessoes"]
        if not sessoes:
            continue
        ss = sessoes["Sessao"]
        ss = [ss] if isinstance(ss, dict) else ss
        for s in ss:
            ps = (s.get("Pronunciamentos") or {}).get("Pronunciamento") or []
            ps = [ps] if isinstance(ps, dict) else ps
            for p in ps:
                cod = p["CodigoPronunciamento"]
                tx = (p.get("Resumo") or "") + " " + (p.get("Indexacao") or "")
                if cod in cands and os.path.exists(f"{SEN}/textos/{cod}.txt"):
                    tx += " " + open(f"{SEN}/textos/{cod}.txt", "rb").read().decode("utf-8", "ignore")
                processa({"id": "SF" + cod, "data": p["Data"], "autor": p.get("NomeAutor", ""), "url": p.get("TextoIntegral", ""), "texto": tx},
                         "Senado", cnt_ent, cnt_fam, tot, out)
    out.close()
    shaC, shaS = dir_sha(CAM, "/*.json"), dir_sha(SEN, "/lista_*.json")
    with open(OUT + ("/_v1prereg_parlamento_novo.csv" if MOD != "dicionario_v2" else "/_bruto_parlamento.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["familia", "universo", "ano", "n", "consulta", "data_acesso", "sha256"])
        for (casa, ano), n in sorted(tot.items()):
            w.writerow(["TOTAL", casa, ano, n, "denominador: discursos/pronunciamentos no universo", hoje, shaC if casa == "Camara" else shaS])
        for (casa, i, ano), n in sorted(cnt_ent.items()):
            w.writerow([FAM[i], casa, ano, n, i, hoje, shaC if casa == "Camara" else shaS])
        for (casa, fam, ano), n in sorted(cnt_fam.items()):
            w.writerow([fam, casa, ano, n, fam + "-any (uniao das entradas PT)", hoje, shaC if casa == "Camara" else shaS])
    print("discursos Camara", sum(v for (c, a), v in tot.items() if c == "Camara"), "Senado", sum(v for (c, a), v in tot.items() if c == "Senado"))
    print("familia-any total:", {k: sum(v for (c, f, a), v in cnt_fam.items() if f == k) for k in ("F1", "F2", "F3", "F4")})
