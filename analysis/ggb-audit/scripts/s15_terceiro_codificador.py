"""S15. Terceira leitura, cega, dos 6 casos em que os codificadores A (Claude Sonnet 5.5) e B (Gemini 3.8 Flash)
discordaram (kappa.json, "desacordos"); pedido do autor em 2026-11-01 (parecer AST-01 da r5: efeito dos desacordos
sobre as contagens).

Regra fixada ANTES de rodar: o codificador C é de uma terceira família (GPT-6 Astra, pela assinatura do ChatGPT,
`codex exec` sem internet nem arquivos); recebe o mesmo codebook e o mesmo cabeçalho do pacote do codificador B, com o
nome da vítima trocado por [VITIMA], mas o TEXTO INTEIRO da matéria (B recebeu uma janela de 3.500 caracteres) e sem ver
os códigos de A nem de B. Código final de cada variável em desacordo = o que dois dos três codificadores marcaram; se os
três divergirem, fica o de A (a codificação publicada) e o caso é listado. O autor confere a tabela antes de as
contagens mudarem (s11_validacao.py lê adjudicacao.json). O kappa continua sendo A contra B.

Uso: REPO_ROOT=<pasta com sources/public/p3-ggb/_raw> python3.14 -I s15_terceiro_codificador.py [--so-pacote]
Saídas: _raw/pacote_C.json, _raw/prompt_C.txt, _raw/saida_C.txt (fora do git: texto das matérias) e
data/adjudicacao.json (só número do caso e códigos, sem nome).
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv
import json
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

ROOT = Path(REPO_ROOT); RAW = ROOT / "sources/public/p3-ggb/_raw"
F3 = ROOT / "analysis/ggb-audit"; D = F3 / "dados"
CODEX = "/opt/homebrew/bin/codex"
VARS = ["corresp", "morte", "tipo", "lgbt", "base", "motivo", "desfecho"]


def nz(x):
    return unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode()


desac = json.loads((D / "kappa.json").read_text())["desacordos"]
casos_alvo = [x["caso"] for x in desac]
nom = {r["id"]: r for r in csv.DictReader((RAW / "ggb2019_lista_nominal.csv").open())}
amo = {r["ordem_sorteio"]: r for r in csv.DictReader((D / "amostra.csv").open())}
pac = []
for k in casos_alvo:
    r = amo[k]; n = nom[r["id"]]; t = re.sub(r"\s+", " ", (RAW / "news_txt" / f'{r["id"]}.txt').read_text())
    toks = [w for w in nz(n["nome"]).replace("/", " ").split() if len(w) >= 4 and w not in ("silva", "santos", "souza", "filho", "junior")]
    for w in toks:
        t = re.sub(re.escape(w), "[VITIMA]", t, flags=re.I)
    # o mascaramento de s06 compara sem acento; aqui o texto inteiro também passa pela forma sem acento do nome
    tn = nz(t)
    assert not any(w in tn for w in toks), f"nome não mascarado no caso {k}"
    pac.append(dict(caso=k, categoria_ggb=n["cat"], cidade_uf=f'{n["cidade"]}/{n["uf"]}', titulo=t.split("\n")[0][:160], texto=t))
(RAW / "pacote_C.json").write_text(json.dumps(pac, ensure_ascii=False, indent=1))
cab = (RAW / "prompt_B.txt").read_text().split("CASOS (JSON):")[0]
prompt = cab + "CASOS (JSON):\n" + json.dumps(pac, ensure_ascii=False, indent=1) + "\n"
(RAW / "prompt_C.txt").write_text(prompt)
print(len(pac), "casos; caracteres do texto:", sum(len(c["texto"]) for c in pac))
if "--so-pacote" in sys.argv:
    raise SystemExit(0)

t0 = time.time()
with tempfile.TemporaryDirectory() as vazio, tempfile.TemporaryDirectory() as home:
    Path(home, "auth.json").symlink_to(Path.home() / ".codex/auth.json")
    out = Path(home, "resp.txt")
    r = subprocess.run([CODEX, "exec", "--skip-git-repo-check", "-s", "read-only", "-m", "gpt-6-astra", "-c", "model_reasoning_effort=high",
                        "--output-last-message", str(out), "-"], input=prompt, capture_output=True, text=True, timeout=3600,
                       cwd=vazio, env={**_os.environ, "CODEX_HOME": home})
    resp = out.read_text() if out.exists() else ""
m = re.search(r"^model: (\S+)", r.stderr + r.stdout, re.M)
(RAW / "saida_C.txt").write_text(resp)
C = {x["caso"]: x for x in json.loads(resp[resp.index("["):resp.rindex("]") + 1])}
assert sorted(C) == sorted(casos_alvo), sorted(C)

A = {}
for l in open(D / "codificacao_A_raw.txt"):
    if l[:1].isdigit():
        p = l.rstrip("\n").split("|"); A[p[0]] = dict(zip(["ordem"] + VARS, p, strict=False))  # tipo_fonte e obs sobram
B = {x["caso"]: x for x in json.loads((RAW / "saida_B.txt").read_text())}
linhas = []
for k in casos_alvo:
    for v in VARS:
        a, b, c = A[k][v], B[k][v], C[k][v]
        if a == b:
            continue
        if a == c:
            final, regra = a, "dois de três (A e C)"
        elif b == c:
            final, regra = b, "dois de três (B e C)"
        else:
            final, regra = a, "três divergem: fica A"
        linhas.append(dict(caso=k, variavel=v, A=a, B=b, C=c, final=final, regra=regra))
saida = dict(regra="código final = o de dois dos três codificadores; três divergentes = fica A (publicado)",
             codificador_C=dict(modelo_pedido="gpt-6-astra", modelo_registrado=m.group(1) if m else "?", segundos=round(time.time() - t0),
                                rc=r.returncode, texto="matéria inteira, nome mascarado; sem ver A nem B"),
             conferido_pelo_autor=False, desacordos=linhas, C=C)
(D / "adjudicacao.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1))
print(json.dumps(linhas, ensure_ascii=False, indent=1))
