"""C27 passo 2: codifica as cegas via `grok -p` (assinatura do fornecedor, sem API paga). Uso:
  rodar_C27.py itens   -> itens_C27.jsonl   (lotes de 10 da mesma familia, embaralhados com semente)
  rodar_C27.py base    -> baseline_itens.jsonl (afirmacao-alvo = estatistica)
Salva a resposta bruta de cada lote em brutos_C27/ e o consolidado em codif_segundo_*.json.
Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import json, os, random, subprocess, sys, tempfile, time, hashlib
from concurrent.futures import ThreadPoolExecutor
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
GROK = _os.environ.get("GROK_BIN", "grok")  # FERRAMENTA DO AUTOR (não re-executável no clone): chama CLIs de modelos de linguagem pela assinatura do autor; defina GROK_BIN com o caminho do executável. As saídas gravadas no repositório são as da execução original.
SEMENTE = 20261023
ALVO = {
 "F1": "\"gays/LGBT morrem mais que heterossexuais\" (qualquer forma comparativa: risco, expectativa de vida, suicídio, homicídio).",
 "F2": "\"o Brasil é o país que mais mata LGBT/pessoas trans\" e variantes (\"a cada X horas morre um LGBT\", \"recorde de mortes\").",
 "F3": "\"governo de direita/Bolsonaro mata/persegue/quer eliminar/tirar direitos de homossexuais\" e variantes (\"extermínio\", \"cura gay\", \"licença para matar\").",
 "F4": "afirmações simétricas contrárias (\"não existe homofobia no Brasil\", \"o dado LGBT é inventado/inflado\", \"gays não morrem mais\").",
 "BASE": "uma ESTATÍSTICA apresentada como fato sobre a realidade (percentual, frequência \"a cada N horas\", quantidade em mil/milhões/bilhões). NÃO é estatística: número de artigo, lei ou projeto, data, hora, valor de emenda ou de orçamento específico, contagem de votos ou de sessão (nesses casos a postura é FORA).",
}
FORMAS = {
 "F1": "taxa_risco_comparativo | expectativa_vida_comparativa | suicidio_comparativo | contagem_absoluta | outro",
 "F2": "ranking_pais_que_mais_mata | frequencia_a_cada_N_horas | recorde_serie | numero_absoluto_sem_ranking | outro",
 "F3": "extermino_genocidio | perseguicao | tirar_direitos | incentivo_violencia | cura_gay_politica | outro",
 "F4": "nega_existencia | dados_inflados_inventados | ggb_fraude | outro",
 "BASE": "(omitida nesta rodada: use \"\" em forma)",
}
POSTURA = ["AFIRMA", "ATRIBUI", "NEGA/CRITICA", "MENCIONA", "FORA"]
FONTE = ["primaria_verificavel", "secundaria_ONG", "secundaria_imprensa", "oficial_sem_referencia", "nenhuma"]
SCHEMA = {"type": "object", "properties": {"itens": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "postura": {"type": "string", "enum": POSTURA}, "forma": {"type": "string"},
    "fonte_citada": {"type": "string", "enum": FONTE}, "fonte_nomeada": {"type": "string"},
    "cita_GGB": {"type": "integer"}, "cita_ANTRA": {"type": "integer"}, "cita_TGEU": {"type": "integer"}, "cita_ONU": {"type": "integer"}},
    "required": ["id", "postura", "forma", "fonte_citada", "fonte_nomeada", "cita_GGB", "cita_ANTRA", "cita_TGEU", "cita_ONU"]}}},
    "required": ["itens"]}
TPL = open(OUT + "/prompt_C27.txt").read()

def prompt(fam, lote):
    itens = "\n".join(json.dumps({"id": i["id"], "texto": i["texto"]}, ensure_ascii=False) for i in lote)
    return TPL.replace("{FAMILIA}", fam).replace("{ALVO}", ALVO[fam]).replace("{FORMAS}", FORMAS[fam]).replace("{ITENS}", itens)

def valida(fam, lote, resp):
    ids = {i["id"] for i in lote}
    got = {r["id"]: r for r in resp["itens"]}
    if set(got) != ids:
        raise ValueError("ids divergentes")
    for r in got.values():
        if r["postura"] == "FORA" and r["forma"] != "":
            r["forma"] = ""   # regra do codebook: forma vazia se FORA
        if r["postura"] != "FORA" and fam != "BASE" and r["forma"] not in FORMAS[fam].split(" | "):
            raise ValueError("forma fora da lista: " + r["forma"])
        if r["postura"] == "FORA":
            r["fonte_citada"] = "nenhuma"
    return got

def chama(args):
    nome, fam, lote = args
    p = prompt(fam, lote)
    for tent in range(3):
        bruto = f"{OUT}/brutos_C27/{nome}_t{tent}.json"
        with tempfile.TemporaryDirectory() as d:
            t0 = time.time()
            r = subprocess.run([GROK, "-p", p, "--output-format", "json", "--json-schema", json.dumps(SCHEMA),
                                "--disable-web-search", "--tools", "", "--max-turns", "1"],
                               cwd=d, capture_output=True, text=True, timeout=600)
        open(bruto, "w").write(json.dumps({"rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr, "seg": round(time.time() - t0, 1)}, ensure_ascii=False))
        try:
            j = json.loads(r.stdout)
            resp = json.loads(j["text"])
            return nome, valida(fam, lote, resp), j.get("total_cost_usd", 0), list(j.get("modelUsage", {}))
        except Exception as e:
            print(nome, "tentativa", tent, "falhou:", repr(e)[:200], flush=True)
    return nome, None, 0, []

if __name__ == "__main__":
    modo = sys.argv[1]
    limite = int(sys.argv[2]) if len(sys.argv) > 2 else None
    os.makedirs(OUT + "/brutos_C27", exist_ok=True)
    if modo == "itens":
        itens = [json.loads(l) for l in open(OUT + "/itens_C27.jsonl")]
        por_fam = {}
        for i in itens:
            por_fam.setdefault(i["familia"], []).append(i)
        lotes = []
        for fam in sorted(por_fam):
            L = sorted(por_fam[fam], key=lambda i: i["id"]); random.Random(f"{SEMENTE}-{fam}").shuffle(L)
            for k in range(0, len(L), 10):
                lotes.append((f"itens_{fam}_{k // 10:02d}", fam, L[k:k + 10]))
        destino = "codif_segundo_itens.json"
    else:
        itens = [{"id": hashlib.sha256(json.loads(l)["id"].encode()).hexdigest()[:12], "texto": json.loads(l)["trecho"]} for l in open(OUT + "/baseline_itens.jsonl")]
        random.Random(f"{SEMENTE}-BASE").shuffle(itens)
        lotes = [(f"base_{k // 10:02d}", "BASE", itens[k:k + 10]) for k in range(0, len(itens), 10)]
        destino = "codif_segundo_base.json"
    if limite:
        lotes = lotes[:limite]
    print(len(lotes), "lotes", flush=True)
    res, custo, modelos = {}, 0.0, set()
    with ThreadPoolExecutor(4) as ex:
        for nome, got, c, m in ex.map(chama, lotes):
            custo += c; modelos.update(m)
            if got is None:
                print("LOTE FALHOU", nome, flush=True); continue
            res.update(got)
    json.dump({"codificacao": res, "total_cost_usd_lista": round(custo, 4), "modelos": sorted(modelos), "n": len(res)}, open(f"{OUT}/{destino}", "w"), ensure_ascii=False, indent=0)
    print("feito", len(res), round(custo, 3), modelos)
