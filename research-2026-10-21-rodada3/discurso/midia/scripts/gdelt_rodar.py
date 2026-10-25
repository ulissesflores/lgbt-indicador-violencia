"""Fila de consultas GDELT DOC 2.0 (sem chave). O servico devolve 429 de forma errática neste IP (compartilhado
com outras frentes): espera 25 s entre pedidos OK e 120 s apos 429, sem desistir. Resultado de cada tarefa
anexado em _gdelt_resultados.jsonl (retomavel); bruto + sha256 em fontes/.../midia/gdelt."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import hashlib, json, os, subprocess, sys, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicionario as d

BASE = REPO_ROOT
RAW = BASE + "/fontes/q1-textointegral/discurso/midia/gdelt"
RES = BASE + "/research-2026-10-21-rodada3/discurso/midia/_gdelt_resultados.jsonl"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
INI, FIM = "20170101000000", "20261021235959"
LANG = {"pt": "sourcelang:portuguese", "en": "sourcelang:english", "es": "sourcelang:spanish"}


def tarefas():
    """Sintaxe validada na sondagem de 2026-10-23: GDELT so aceita parenteses em torno de OR; logo NAO ha uniao
    de entradas distintas e a entrada nao pode vir entre parenteses externos. Uma consulta por entrada.
    Controle positivo PT: 'homofobia sourcelang:portuguese' devolveu {} (falha) -> entradas PT usam
    sourcecountry:brazil; ordem: controles, EN, ES, PT-BR (a API limita este IP com 429)."""
    T = [("CTRL-pt-sem-filtro", "CTRL", "timelinevolraw", "homofobia"),
         ("CTRL-pt-BR", "CTRL", "timelinevolraw", "homofobia sourcecountry:brazil")]
    for lang in ("en", "es"):
        for e in d.E:
            if e["lang"] == lang:
                T.append((e["id"], e["fam"], "timelinevolraw", f"{e['gdelt']} {LANG[lang]}"))
    for e in d.E:
        if e["lang"] == "pt":
            T.append((e["id"] + "-BR", e["fam"], "timelinevolraw", f"{e['gdelt']} sourcecountry:brazil"))
    return T


NUCLEO_DOM = ["F1-PT-01", "F2-PT-01", "F3-PT-01", "F3-PT-03", "F4-PT-01"]


def tarefas_dom():
    T = []
    for e in d.E:
        if e["id"] in NUCLEO_DOM:
            for dom in d.DOMINIOS_BR:
                T.append((f"{e['id']}-dom-{dom}", e["fam"], "timelinevolraw", f"{e['gdelt']} sourcelang:portuguese domainis:{dom}"))
    for e in d.E:
        if e["id"] in NUCLEO_DOM or e["id"] in ("F2-EN-01", "F3-EN-01"):
            for dom in d.DOMINIOS_ORG:
                T.append((f"{e['id']}-org-{dom}", e["fam"], "timelinevolraw", f"{e['gdelt']} domainis:{dom}"))
    return T


def pedido(q, modo, extra=None):
    p = {"query": q, "mode": modo, "format": "json", "startdatetime": INI, "enddatetime": FIM}
    if extra:
        p.update(extra)
    u = API + "?" + urllib.parse.urlencode(p, quote_via=urllib.parse.quote)
    espera = 300
    for t in range(40):
        r = subprocess.run(["curl", "-s", "-m", "120", "-w", "\n%{http_code}", u], capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        code = code.decode(errors="ignore").strip()
        if code == "200" and body.strip() and not body.startswith(b"Please limit"):
            return body, u
        sys.stderr.write(f"{time.strftime('%H:%M:%S')} 429/erro codigo={code} {body[:40]!r}\n"); sys.stderr.flush()
        time.sleep(espera)
    return None, u


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    feitas = set()
    if os.path.exists(RES):
        feitas = {json.loads(l)["id"] for l in open(RES)}
    fila = tarefas() + (tarefas_dom() if "dom" in sys.argv else [])
    for id_, fam, modo, q in fila:
        if id_ in feitas:
            continue
        body, u = pedido(q, modo)
        if body is None:
            continue
        h = hashlib.sha256(body).hexdigest()
        arq = f"{RAW}/{id_}_{h[:10]}.json"
        open(arq, "wb").write(body)
        open(RES, "a").write(json.dumps({"id": id_, "familia": fam, "modo": modo, "consulta": q, "url": u, "sha256": h, "arquivo": arq,
                                         "data_acesso": time.strftime("%Y-%m-%d"), "tam": len(body)}, ensure_ascii=False) + "\n")
        print(id_, len(body), flush=True)
        time.sleep(45)
