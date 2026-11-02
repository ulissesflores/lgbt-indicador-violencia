#!/usr/bin/env python3
"""Juiz externo da rubrica-academica (0-1000) por um modelo de outra família, pela assinatura do fornecedor (custo zero).

Quem escreveu não pontua: o juiz é de outra família de modelo. O script congela o sha256 do
paper.md ANTES de montar o prompt e o reconfere DEPOIS da resposta; se o arquivo mudou, a
rodada é descartada (alvo em movimento). O prompt leva a rubrica verbatim, as saídas reais das
ferramentas determinísticas (densidade, E-E-A-T, referências, testes de figura) e o paper
inteiro. Saída: build/juiz/rodada-<n>.json (resposta) e .prompt.txt (prompt exato).

Uso: /opt/homebrew/bin/python3.14 -I tools/juiz_rubrica.py <n_rodada> [--backend=astra|grok|gemini] [--parte=tudo|principal|corpo] [--dry-run]
v0.3: `--parte principal` julga so o artigo principal (paper.md ate o marcador `<!-- parte:anexos -->`,
o mesmo corte de make_export.py); o prompt diz ao juiz que os anexos estao em PDF separado, fora do
texto julgado, e lista os anexos e as figuras que ficaram no Anexo F (lidos do proprio paper.md).
O hash conferido continua sendo o do paper.md inteiro (o canonico).

v0.4 (2026-10-25; absorve a copia usada na rodada v4-1): regra (4b) descreve o canonico v0.4 (referencias APA 7
em paragrafo; export tools/export_v04.py via tools/build_v04.sh; estilo `Referencia`); a evidencia de build NAO
executa build nenhum (o PDF da v0.4 e gerado pelo Word, fora do alcance deste script; tools/build.sh e o pipeline
LEGADO da v0.3): cola o log da construcao mais recente do autor (build/v04-build*.log), a linha de
PAPER-SHA256.txt, `qpdf --check` e `pdfinfo` ao vivo (so leitura) e o estilo `Referencia` do DOCX v0.4;
`--parte=corpo` (reserva) corta em "## Apêndice A"; `--dry-run` grava o prompt sem chamar o juiz. PAPER_DIR = a
pasta paper/ deste repositorio (sobrescrevivel por variavel de ambiente).

v0.5 (2026-10-26, frente G; medição em research-2026-10-24-v03/G-GROK-CORTE.md do projeto de origem):
- O `grok -p` (CLI 1.0.62) CORTA prompt de 100.000 B ou mais: entrega ao modelo só o começo (~94,3 KB) e o fim (3.988 B), com o
  meio num arquivo que o modelo teria de ler com ferramenta. Até 99.974 B chega inteiro. Todas as rodadas do Grok da v0.2 à v0.4.1
  (prompts de 134 a 252 KB) foram parciais. Com `--verbatim` o CLI entrega o prompt inteiro (medido com 130.000 e 260.000 B).
  E `--tools ""` NÃO removia ferramenta nenhuma (25 definições, inclusive read_file e grep); `--disallowed-tools <os 25 nomes>` remove.
- `--backend`: `astra` (PADRÃO: `codex exec -m gpt-6-astra`, prompt pelo stdin, só leitura, sem web; o método das rodadas v4-3 e
  v4-4, com leitura integral comprovada), `grok` (`--verbatim` + `--disallowed-tools`; RECUSA prompt acima de GROK_LIMITE_B se a
  versão do CLI não for a medida, porque só nela o --verbatim foi medido) e `gemini` (`agy`, stream-json com o prompt em partes de
  até 150.000 B, porque o `agy -p` corta perto de 191.581 B; sem --json-schema, que no agy força a ferramenta interna "finish").
  Os três rodam numa pasta de trabalho vazia e temporária.
- PROVA DE LEITURA (todos os backends): o script insere no texto julgado, perto de 60% dele e entre dois parágrafos de texto
  corrido, a linha `<!-- prova-leitura -->`; o esquema JSON ganha `leitura_integral` com `ultima_frase` (a última frase do texto
  julgado) e `frase_apos_marcador` (a primeira frase do parágrafo logo depois do marcador), copiadas verbatim. A rodada só é
  válida (`_valida`) com hash conferido E as duas frases certas E a entrega conferida no registro do próprio CLI (`_entrega`).
- Julgar por partes (`--partes`) NÃO foi implementado: exigiria somar pontuações de textos parciais, o que a rubrica não prevê;
  com `--verbatim` (grok) e os backends astra/gemini não é necessário.
- A 2ª linha do prompt dizia "se a interface deixar parte dele fora da mensagem, leia TODO o restante"; com a regra (8) (sem ferramentas,
  sem arquivos) virou "está inteiro nesta mensagem: leia-o todo ... sem buscar nada fora dela" (um modelo obediente tentaria ler o disco
  e invalidaria a rodada pela conferência de isolamento).
- Para rodada de teste sobre outro texto: JUIZ_PAPER=<arquivo> (texto julgado e hash) e JUIZ_OUT=<pasta> (saídas fora do
  repositório); a evidência das ferramentas continua sendo a do paper.md do repositório.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

PAPER_DIR = Path(os.environ.get("PAPER_DIR") or Path(__file__).resolve().parents[1])
PAPER = Path(os.environ.get("JUIZ_PAPER") or PAPER_DIR / "paper.md")
# FERRAMENTA DO AUTOR (não reproduzível só com este repositório): chama o CLI de um modelo de linguagem pela assinatura do autor
# (GROK_BIN, CODEX_BIN, AGY_BIN) e lê a rubrica do laboratório (RUBRICA_ACADEMICA_MD, não distribuída). Os vereditos usados no
# AUDIT.md estão em build/juiz/*.json.
RUBRICA = Path(os.environ.get("RUBRICA_ACADEMICA_MD", "rubrica-academica.md"))
GROK = os.environ.get("GROK_BIN", "grok")
CODEX = os.environ.get("CODEX_BIN", "codex")
AGY = os.environ.get("AGY_BIN", "agy")
PY = sys.executable
OUT = Path(os.environ.get("JUIZ_OUT") or PAPER_DIR / "build" / "juiz")
PARTE = "<!-- parte:anexos -->"  # mesmo marcador de tools/make_export.py
MARCA = "<!-- prova-leitura -->"  # inserido pelo script no texto julgado; não existe no paper.md

# Medição da frente G (2026-10-26, grok 1.0.62): sem --verbatim, 99.974 B chegam inteiros e 100.000 B já são cortados.
GROK_VERSAO_MEDIDA = "1.0.62"
GROK_LIMITE_B = 99_974
GROK_FERRAMENTAS = ("run_terminal_command,read_file,search_replace,list_dir,grep,kill_command_or_subagent,todo_write,"
                    "get_command_or_subagent_output,spawn_subagent,scheduler_create,scheduler_delete,scheduler_list,monitor,"
                    "search_tool,use_tool,workflow,enter_plan_mode,exit_plan_mode,ask_user_question,send_feedback,image_gen,"
                    "image_edit,image_to_video,reference_to_video,write")  # as 25 do tool_definitions.json do 1.0.62
ASTRA_TOKENS_BASE = 12_940  # tokens de entrada do codex com prompt curto (rodada v4-3)
AGY_PARTE_MAX = 150_000  # o agy -p cortou em 191.581 B (rodada v4-3, tentativa 1)
GEMINI_ID = os.environ.get("JUIZ_GEMINI_MODELO", "gemini-4-argon-high")


def estrito(s: dict) -> dict:
    """Esquema com additionalProperties false em todo objeto (o codex exige)."""
    if s.get("type") == "object":
        s = dict(s, additionalProperties=False, properties={k: estrito(v) for k, v in s["properties"].items()})
    elif s.get("type") == "array":
        s = dict(s, items=estrito(s["items"]))
    return s


SCHEMA = estrito({
    "type": "object",
    "properties": {
        "sha256_conferido": {"type": "string"},
        "dimensoes": {"type": "object", "properties": {
            k: {"type": "object", "properties": {"pontos": {"type": "number"}, "maximo": {"type": "number"},
                                                  "descontos": {"type": "array", "items": {"type": "string"}}},
                "required": ["pontos", "maximo", "descontos"]}
            for k in ("estrutura_formal", "densidade_tecnica", "fundamentacao_teorica", "originalidade_tese",
                      "consistencia_interna", "correcao_factual")},
            "required": ["estrutura_formal", "densidade_tecnica", "fundamentacao_teorica", "originalidade_tese",
                         "consistencia_interna", "correcao_factual"]},
        "total": {"type": "number"},
        "achados_criticos": {"type": "array", "items": {"type": "string"}},
        "veredito": {"type": "string"},
        "leitura_integral": {"type": "object", "properties": {"ultima_frase": {"type": "string"},
                                                              "frase_apos_marcador": {"type": "string"}},
                             "required": ["ultima_frase", "frase_apos_marcador"]},
    },
    "required": ["sha256_conferido", "dimensoes", "total", "achados_criticos", "veredito", "leitura_integral"],
})


def sha(p: Path) -> str:
    """sha256 do arquivo."""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def saida(cmd: list[str]) -> str:
    """Saida combinada de um comando local (evidencia deterministica para o juiz)."""
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=PAPER_DIR)
    return (r.stdout + r.stderr).strip()


def artigo(parte: str) -> tuple[str, str]:
    """Texto julgado e o aviso de escopo (vazio quando o juiz le o paper.md inteiro)."""
    t = PAPER.read_text(encoding="utf-8")
    if parte == "tudo":
        return t, ""
    if parte == "corpo":  # reserva S2: corta antes dos apendices (espelho do --parte principal da P2B)
        corpo, sep, resto = t.partition("\n## Apêndice A")
        if not sep:
            raise SystemExit("[FATAL] '## Apêndice A' não encontrado")
        apend = re.findall(r"^## (Apêndice [A-Z] .+)$", sep.lstrip("\n") + resto, re.M)
        aviso = ("===== ESCOPO DO TEXTO JULGADO =====\n"
                 "Julgue o artigo até as Referências (inclusive). Os apêndices abaixo estão no MESMO PDF, depois das "
                 "Referências, mas ficam fora do texto julgado por limite de tamanho do prompt: não desconte o que só eles "
                 "contêm e não dê ponto por eles. Remissões \"ver Apêndice X\" são válidas.\n"
                 "Apêndices (fora do texto julgado): " + "; ".join(apend) + ".\n\n")
        return corpo + "\n", aviso
    if t.count(PARTE) != 1:
        raise SystemExit(f"[FATAL] o canonico precisa de exatamente um {PARTE!r} (achados: {t.count(PARTE)})")
    corpo, resto = t.split(PARTE)
    anexos = re.findall(r"^## (Anexo [A-Z] .+)$", resto, re.M)
    figs = re.findall(r"^!\[Figura (\d+)", resto, re.M)
    aviso = ("===== ESCOPO DO TEXTO JULGADO =====\n"
             "Julgue SÓ o artigo principal abaixo (paper.md até o marcador de parte). Os anexos saem num PDF "
             "separado (build/anexos.pdf), gerado do mesmo markdown, e ficam FORA do texto julgado: não desconte "
             "o que só eles contêm, e não dê ponto por eles. Remissões do tipo \"ver Anexo X\" e \"no PDF de anexos\" "
             "são válidas. As Referências estão no artigo principal.\n"
             "Anexos (no PDF separado): " + "; ".join(anexos) + ".\n"
             "Figuras numeradas no artigo principal e impressas só no Anexo F: " + ", ".join(figs) + ".\n\n")
    return corpo, aviso


def prosa(linha: str) -> bool:
    """Linha de parágrafo de texto corrido (não tabela, título, figura, lista, citação, comentário, código)."""
    s = linha.lstrip()
    return len(s) >= 80 and not s.startswith(("|", "#", "!", "```", "-", "*", ">", "<", "$", "[", "+")) and not re.match(r"\d+\.", s)


def marca(texto: str, frac: float = 0.6) -> tuple[str, dict]:
    """Insere MARCA na primeira fronteira de parágrafos de prosa depois de `frac` do texto (fora de bloco de código)."""
    alvo, pos, codigo = int(len(texto) * frac), 0, False
    linhas = texto.split("\n")
    for i, l in enumerate(linhas):
        if l.lstrip().startswith("```"):
            codigo = not codigo
        if (pos >= alvo and not codigo and i > 0 and not l.strip() and i + 1 < len(linhas) and prosa(linhas[i + 1])
                and not linhas[i - 1].lstrip().startswith("|")):
            k = pos + len(l) + 1  # início do parágrafo marcado
            marcado = texto[:k] + MARCA + "\n\n" + texto[k:]
            assert marcado.replace(MARCA + "\n\n", "", 1) == texto
            par = []
            for m in linhas[i + 1:]:
                if not m.strip():
                    break
                par.append(m.strip())
            blocos = [b.strip() for b in re.split(r"\n\s*\n", texto) if b.strip()]
            return marcado, {"pct": round(100 * k / len(texto), 1), "paragrafo_marcado": " ".join(par),
                             "ultimo_paragrafo": " ".join(blocos[-1].split("\n"))}
        pos += len(l) + 1
    raise SystemExit("[FATAL] não achei fronteira de parágrafos de prosa depois de 60% do texto para a prova de leitura")


def norm(s: str) -> str:
    """Tolerância da prova (a mesma das rodadas v4-3/v4-4): espaços colapsados, ênfase markdown fora, aspas retas, ponto final opcional."""
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'").replace("*", "").replace("_", "")
    s = re.sub(r"\s+", " ", s).strip().strip('"').strip()
    return s.rstrip(".").strip()


def prova(li: dict, esp: dict) -> dict:
    """Confere as duas frases: sufixo do último parágrafo (>= 20 car.) e prefixo do parágrafo marcado (>= 40 car.)."""
    u, f = norm(str(li.get("ultima_frase", ""))), norm(str(li.get("frase_apos_marcador", "")))
    pu, pm = norm(esp["ultimo_paragrafo"]), norm(esp["paragrafo_marcado"])
    r = {"ultima_frase": bool(u) and pu.endswith(u) and len(u) >= min(20, len(pu)),
         "frase_apos_marcador": bool(f) and pm.startswith(f) and len(f) >= min(40, len(pm)),
         "marcador_em_pct": esp["pct"]}
    r["ok"] = r["ultima_frase"] and r["frase_apos_marcador"]
    return r


def _texto(e: dict) -> str:
    c = e.get("content")
    return c if isinstance(c, str) else "".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))


def versao_grok() -> str:
    m = re.search(r"\d+\.\d+\.\d+", subprocess.run([GROK, "--version"], capture_output=True, text=True).stdout)
    return m.group(0) if m else "?"


def guarda_grok(n: int) -> str:
    """Recusa (SystemExit) o que não tem entrega integral medida; devolve a descrição do método."""
    v = versao_grok()
    if n > GROK_LIMITE_B and v != GROK_VERSAO_MEDIDA:
        raise SystemExit(f"[RECUSA] prompt de {n} B acima do limite medido do grok ({GROK_LIMITE_B} B) e CLI {v} != "
                         f"{GROK_VERSAO_MEDIDA}: a entrega integral por --verbatim só foi medida no {GROK_VERSAO_MEDIDA}. "
                         "Meça de novo (prompt sintético com sentinelas) ou use --backend=astra.")
    if n > 900_000:
        raise SystemExit(f"[RECUSA] prompt de {n} B não cabe como argumento de linha de comando")
    return f"grok {v} -p --verbatim --disallowed-tools <25> (prompt {n} B; limite sem --verbatim {GROK_LIMITE_B} B)"


def juiz_grok(prompt: str) -> tuple[object, str, dict]:
    """grok -p --verbatim sem ferramentas; confere a entrega pela sessão gravada pelo próprio CLI."""
    with tempfile.TemporaryDirectory(prefix="juiz-grok-") as cwd:
        r = subprocess.run([GROK, "-p", prompt, "--verbatim", "--output-format", "json", "--json-schema", json.dumps(SCHEMA),
                            "--disable-web-search", "--disallowed-tools", GROK_FERRAMENTAS,
                            "--max-turns", os.environ.get("JUIZ_MAX_TURNS", "3")],
                           capture_output=True, text=True, timeout=1800, cwd=cwd)
    bruto = r.stdout.strip() + "\n--- stderr ---\n" + r.stderr
    try:
        env = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, bruto, {"ok": False, "motivo": "stdout do grok não é JSON"}
    ent = {"metodo": "grok -p --verbatim --disallowed-tools <25>", "modelo": ",".join(env.get("modelUsage") or {}),
           "num_turns": env.get("num_turns"), "input_tokens": (env.get("usage") or {}).get("input_tokens")}
    ses = Path.home() / ".grok" / "sessions" / urllib.parse.quote(str(env.get("cwd")), safe="") / str(env.get("sessionId"))
    ch = ses / "chat_history.jsonl"
    if not ch.exists():
        ent.update(ok=False, motivo="sessão do CLI não encontrada: entrega não conferida")
    else:
        L = [json.loads(x) for x in ch.read_text(encoding="utf-8").splitlines() if x.strip()]
        users = [_texto(e) for e in L if e.get("type") == "user"]
        td = ses / "tool_definitions.json"
        defs = [t.get("name") for t in json.loads(td.read_text())] if td.exists() else []
        chamadas = [c.get("name") for e in L for c in (e.get("tool_calls") or [])]
        # o CLI tira o \n final do prompt (medido na rodada de teste da frente G): compara sem espaço nas pontas
        ent.update(mensagem_igual_ao_prompt=any(u.strip() == prompt.strip() for u in users),
                   aviso_de_corte=any("[Full request offloaded" in u or "middle omitted" in u for u in users),
                   ferramentas_definidas=defs, chamadas_de_ferramenta=chamadas)
        so_saida = {"StructuredOutput"}  # a saída com --json-schema passa por esta ferramenta interna
        ent["ok"] = (ent["mensagem_igual_ao_prompt"] and not ent["aviso_de_corte"] and set(defs) <= so_saida
                     and set(chamadas) <= so_saida)
    res = env.get("structuredOutput") or env.get("structured_output") or env.get("result") or env.get("text")
    return res, bruto, ent


def juiz_astra(prompt: str) -> tuple[object, str, dict]:
    """codex exec -m gpt-6-astra (como as rodadas v4-3/v4-4): CODEX_HOME temporário, só leitura, sem web, prompt pelo stdin."""
    with tempfile.TemporaryDirectory(prefix="juiz-astra-") as d:
        d = Path(d)
        home, vazio, sch, ult = d / "codexhome", d / "vazio", d / "schema.json", d / "ultima.txt"
        home.mkdir()
        vazio.mkdir()
        shutil.copy(Path.home() / ".codex" / "auth.json", home)
        os.chmod(home / "auth.json", 0o600)
        sch.write_text(json.dumps(SCHEMA), encoding="utf-8")
        r = subprocess.run([CODEX, "exec", "-m", "gpt-6-astra", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
                            "-c", 'web_search="disabled"', "-c", 'model_reasoning_effort="high"', "-C", str(vazio),
                            "--json", "--output-schema", str(sch), "-o", str(ult), "-"],
                           input=prompt, capture_output=True, text=True, timeout=3300, env=dict(os.environ, CODEX_HOME=str(home)),
                           cwd=vazio)
        res = ult.read_text(encoding="utf-8") if ult.exists() else None
    tipos, tin = {}, 0
    for linha in r.stdout.splitlines():
        try:
            e = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "item.completed":
            k = e.get("item", {}).get("type", "?")
            tipos[k] = tipos.get(k, 0) + 1
        if e.get("type") == "turn.completed":
            tin += e.get("usage", {}).get("input_tokens", 0)
    minimo = ASTRA_TOKENS_BASE + len(prompt.encode()) // 5  # corte do prompt apareceria aqui (~2,8 B por token em português)
    ent = {"metodo": "codex exec -m gpt-6-astra (stdin; só leitura; sem web)", "modelo": "gpt-6-astra", "rc": r.returncode,
           "itens": tipos, "input_tokens": tin, "tokens_minimos": minimo}
    ent["ok"] = r.returncode == 0 and set(tipos) <= {"agent_message", "reasoning"} and tin >= minimo
    return res, r.stdout[-200000:] + "\n--- stderr ---\n" + r.stderr[-20000:], ent


def partes_agy(prompt: str) -> list[str]:
    """Corta o prompt em fronteiras de parágrafo, cada parte com até AGY_PARTE_MAX bytes."""
    out, ini = [], 0
    while len(prompt[ini:].encode()) > AGY_PARTE_MAX:
        lim = ini + AGY_PARTE_MAX // 2  # 2 B por caractere no pior caso do português: a parte cabe
        while len(prompt[ini:lim].encode()) < AGY_PARTE_MAX * 0.9 and lim < len(prompt):
            lim += 1000
        cut = prompt.rfind("\n\n", ini, lim)
        cut = (cut + 2) if cut > ini else prompt.rfind("\n", ini, lim) + 1
        out.append(prompt[ini:cut])
        ini = cut
    out.append(prompt[ini:])
    assert "".join(out) == prompt and all(len(p.encode()) <= AGY_PARTE_MAX for p in out)
    return out


def juiz_gemini(prompt: str) -> tuple[object, str, dict]:
    """agy (Gemini) em stream-json, uma mensagem por parte; confere a entrega pelo transcript do próprio agy."""
    ps = partes_agy(prompt)
    n = len(ps)
    msgs = ([f"[PARTE {k} de {n} do prompt, dividido só porque a ferramenta corta mensagens grandes; o texto continua na "
             f"mensagem seguinte. Não pontue ainda e não use ferramentas: responda apenas RECEBIDO {k}/{n}.]\n\n{p}"
             for k, p in enumerate(ps[:-1], 1)]
            + [(f"[PARTE {n} de {n}, continuação exata da anterior.]\n\n" if n > 1 else "") + ps[-1]
               + "\n\n[Fim do prompt. Cumpra as instruções do início sobre o texto inteiro, sem ferramentas, e devolva só o objeto JSON.]"])
    nd = "".join(json.dumps({"event": "user", "message": {"role": "user", "content": m}}, ensure_ascii=False) + "\n" for m in msgs)
    with tempfile.TemporaryDirectory(prefix="juiz-gemini-") as vazio:
        r = subprocess.run([AGY, "--model", GEMINI_ID, "--sandbox", "--disable-slash-commands", "--input-format", "stream-json",
                            "--output-format", "stream-json", "--print-timeout", "3300s"],
                           input=nd, capture_output=True, text=True, timeout=3400, cwd=vazio)
    tipos, results, cid, modelo = {}, [], None, None
    for linha in r.stdout.splitlines():
        try:
            e = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if e.get("event") == "init":
            cid, modelo = e["init"].get("conversation_id") or e.get("conversation_id"), e["init"].get("model")
        elif e.get("event") == "step_update":
            su = e["step_update"]
            cid = cid or su.get("conversation_id")
            tipos[su.get("step_type", "?")] = tipos.get(su.get("step_type", "?"), 0) + 1
        elif e.get("event") == "result":
            results.append(e["result"])
    final = results[-1] if results else {}
    ent = {"metodo": f"agy stream-json, {n} mensagem(ns)", "modelo": modelo, "partes_bytes": [len(p.encode()) for p in ps],
           "passos": tipos, "status": final.get("status")}
    tf = Path.home() / ".gemini" / "antigravity-cli" / "brain" / str(cid) / ".system_generated" / "logs" / "transcript_full.jsonl"
    if not tf.exists():
        ent.update(ok=False, motivo="transcript do agy não encontrado: entrega não conferida")
    else:
        ents = [ev.get("content") or "" for ev in map(json.loads, tf.read_text(encoding="utf-8").splitlines()) if ev.get("type") == "USER_INPUT"]
        ent.update(entradas_bytes=[len(c.encode()) for c in ents], marcas_truncated=sum(c.count("<truncated") for c in ents),
                   partes_inteiras=all(any(p in c for c in ents) for p in ps))
        ent["ok"] = (r.returncode == 0 and ent["partes_inteiras"] and ent["marcas_truncated"] == 0
                     and set(tipos) <= {"user_input", "agent_response", "finish"})
    res = final.get("structured_output") or final.get("response")
    return res, r.stdout[-200000:] + "\n--- stderr ---\n" + r.stderr[-20000:], ent


def como_json(res: object):
    """Resposta do backend -> dict (aceita dict, JSON em texto ou em bloco de código)."""
    if isinstance(res, dict):
        return res
    if not isinstance(res, str):
        return None
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", res.strip())
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", s, re.S)
        try:
            return json.loads(m.group(0)) if m else None
        except json.JSONDecodeError:
            return None


def main() -> int:
    """Monta o prompt, chama o juiz, confere hash, entrega e prova de leitura, e grava a rodada."""
    seco = "--dry-run" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    parte = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--parte=")), "tudo")
    backend = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--backend=")), "astra")
    if parte not in ("tudo", "principal", "corpo"):
        raise SystemExit("[FATAL] --parte=tudo|principal|corpo")
    if backend not in ("astra", "grok", "gemini"):
        raise SystemExit("[FATAL] --backend=astra|grok|gemini")
    if "--partes" in sys.argv[1:]:
        raise SystemExit("[FATAL] --partes não implementado (ver docstring); use --backend=astra ou o grok com --verbatim")
    n = args[0] if args else "1"
    texto, aviso = artigo(parte)
    texto, esperado = marca(texto)
    OUT.mkdir(parents=True, exist_ok=True)
    h0 = sha(PAPER)
    logs = sorted((PAPER_DIR / "build").glob("v04-build*.log"), key=lambda q: int(re.search(r"(\d+)", q.stem.split("build")[-1]).group(1)))
    if not logs:
        raise SystemExit("[FATAL] nenhum build/v04-build*.log: construa o PDF (tools/build_v04.sh) e grave o log antes do juiz")
    LOG = logs[-1]
    evid = {
        "densidade (tools/densidade_paper.py)": saida([PY, "-I", "tools/densidade_paper.py"]),
        "E-E-A-T (tools/eeat_referencias.py; lê as referências do próprio paper.md)": saida([PY, "-I", "tools/eeat_referencias.py"]),
        "referências (tools/verifica_referencias.py)": saida([PY, "-I", "tools/verifica_referencias.py"]),
        "figura <-> dado (tests/test_figuras.py)": saida([PY, "-I", "tests/test_figuras.py"]),
        "build DOCX/PDF v0.4 (tools/build_v04.sh: log da construção final do autor NESTE MESMO sha, não execução ao vivo; "
        "qpdf/pdfinfo ao vivo) e estilo das referências no DOCX": (
            f"[log] build/{LOG.name} (construção mais recente; Word gera o PDF a partir do DOCX de tools/export_v04.py):\n"
            + LOG.read_text(encoding="utf-8").strip()
            + "\n[amarração] paper/PAPER-SHA256.txt:\n" + (PAPER_DIR / "PAPER-SHA256.txt").read_text(encoding="utf-8").strip()
            + "\n[ao vivo] qpdf --check build/v04/paper-v04.pdf: "
            + " ".join(l.strip() for l in saida(["qpdf", "--check", "build/v04/paper-v04.pdf"]).splitlines()[-2:])
            + "\n[ao vivo] pdfinfo: " + " | ".join(l for l in saida(["pdfinfo", "build/v04/paper-v04.pdf"]).splitlines()
                                                  if l.split(":")[0] in ("Title", "Author", "Creator", "Pages", "File size"))
            + "\n" + saida(
            [PY, "-I", "-c", "import zipfile,re;z=zipfile.ZipFile('build/v04/paper-v04.docx');x=z.read('word/document.xml').decode();"
             "print('[ao vivo] parágrafos com estilo Referencia (lista de referências):',len(re.findall(r'w:pStyle w:val=\"Referencia\"',x)));"
             "s=z.read('word/styles.xml').decode();"
             "m=re.search(r'w:styleId=\"Referencia\".*?</w:style>',s,re.S);print('[ao vivo] estilo Referencia:',re.search(r'<w:ind[^>]*>',m.group(0)).group(0))"])),
    }
    prompt = f"""Você é auditor acadêmico ADVERSARIAL e independente. Não foi você quem escreveu este artigo.
O prompt é longo e está inteiro nesta mensagem: leia-o todo antes de pontuar, sem buscar nada fora dela;
o artigo só termina na linha "===== FIM DO ARTIGO =====" (o que vier antes dela é o artigo inteiro).
Pontue o artigo abaixo pela rubrica a seguir (0-1000, 6 dimensões), sub-critério por sub-critério,
SEM inflar: cada ponto descontado vira uma linha em "descontos" com o motivo concreto (seção e frase).
Regras: (1) a cap dura vale (densidade técnica < 100 => total <= 600); (2) não dê ponto por
critério que o texto não cumpre; (3) as saídas de ferramenta abaixo são medidas determinísticas
reais: use-as para TDI, filler, E-E-A-T, recência e verificação de referências, e não as refaça
de cabeça; (4) critérios de outro gênero (por exemplo "Análise Técnica e Arquitetural" de
disciplina) não se aplicam: o artigo é de pesquisa empírica em ciências sociais/epidemiologia;
o "trade-off com nome próprio" pode ser qualquer lei/efeito nomeado da literatura; os tipos
RFC/NIST/builder's library do menu de 6 são de computação: use a equivalência declarada pela
ferramenta de E-E-A-T (norma oficial, padrão estatístico, documentação oficial de dados);
(4b) o markdown canônico traz as referências como parágrafos em APA 7: o export (tools/export_v04.py,
chamado por tools/build_v04.sh) as converte no estilo Referencia do DOCX, com recuo deslocado de 0,5"
(hanging 720 twips), como mostra a saída do build abaixo; o PDF é um só (artigo + Apêndices A-D); (5) correção
factual: você não tem acesso às fontes; desconte só por inconsistência interna, afirmação sem
citação, suposição não marcada ou número sem origem declarada; (6) devolva em
"sha256_conferido" exatamente o hash informado abaixo; (7) "total" = soma das dimensões.
(8) Prova de leitura integral (obrigatória; se falhar, a rodada é inválida): julgue só com o texto deste prompt, sem
ferramentas, sem ler arquivos e sem web. O programa que montou este prompt inseriu no artigo, perto de 60% do texto, uma
linha só com {MARCA}; ela não faz parte do paper.md e não conta na pontuação. Devolva UM objeto JSON, sem texto fora dele,
com os campos "sha256_conferido", "dimensoes" (as 6 chaves da rubrica, cada uma com "pontos", "maximo" e "descontos"),
"total", "achados_criticos", "veredito" e "leitura_integral", este com "ultima_frase" = a última frase do artigo (a que vem
imediatamente antes da linha "===== FIM DO ARTIGO ====="), copiada verbatim, e "frase_apos_marcador" = a primeira frase do
parágrafo que vem logo depois da linha {MARCA}, copiada verbatim.

sha256 do paper.md auditado: {h0}{" (arquivo inteiro; o texto julgado é o trecho até o marcador de parte)" if aviso else ""}

===== RUBRICA (verbatim) =====
{RUBRICA.read_text(encoding="utf-8")}

===== SAÍDAS REAIS DAS FERRAMENTAS =====
""" + "\n\n".join(f"--- {k} ---\n{v}" for k, v in evid.items()) + f"""

{aviso}===== ARTIGO (paper.md, markdown canônico{", artigo principal" if aviso else ""}) =====
{texto}
===== FIM DO ARTIGO =====
"""
    nb = len(prompt.encode())
    (OUT / f"rodada-{n}.prompt.txt").write_text(prompt, encoding="utf-8")
    metodo = guarda_grok(nb) if backend == "grok" else (
        f"agy stream-json em {len(partes_agy(prompt))} parte(s)" if backend == "gemini" else "codex exec -m gpt-6-astra, stdin")
    if seco:
        print(f"[DRY-RUN] backend {backend}: {metodo}; prompt {nb} B gravado em", OUT / f"rodada-{n}.prompt.txt", "· sha", h0)
        print(f"[DRY-RUN] marcador {MARCA} em {esperado['pct']}% do texto julgado; parágrafo marcado começa:",
              esperado["paragrafo_marcado"][:90], "| último parágrafo termina:", esperado["ultimo_paragrafo"][-90:])
        return 0
    t0 = time.time()
    res, bruto, entrega = {"grok": juiz_grok, "astra": juiz_astra, "gemini": juiz_gemini}[backend](prompt)
    entrega["segundos"] = round(time.time() - t0, 1)
    h1 = sha(PAPER)
    (OUT / f"rodada-{n}.raw.txt").write_text(bruto + "\n--- entrega ---\n" + json.dumps(entrega, ensure_ascii=False), encoding="utf-8")
    res = como_json(res)
    if not isinstance(res, dict) or "dimensoes" not in res:  # ex.: "max turns reached" sem saída estruturada
        print("[FAIL] rodada sem saída estruturada (inválida); ver", OUT / f"rodada-{n}.raw.txt", "· entrega:", entrega)
        return 2
    pv = prova(res.get("leitura_integral") or {}, esperado)
    res["_sha256_antes"], res["_sha256_depois"] = h0, h1
    res["_hash_ok"] = (h0 == h1 == res.get("sha256_conferido"))
    res["_backend"], res["_modelo"] = backend, entrega.get("modelo")
    res["_prompt_bytes"], res["_prompt_sha256"] = nb, hashlib.sha256(prompt.encode()).hexdigest()
    res["_prova_leitura"] = pv
    res["_entrega"] = entrega  # só contagens e booleanos (sem caminho local nem id de sessão: o .json entra no git)
    res["_soma_dimensoes"] = sum(float(v.get("pontos", 0)) for v in res["dimensoes"].values())
    res["_valida"] = bool(res["_hash_ok"] and pv["ok"] and entrega.get("ok"))
    (OUT / f"rodada-{n}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in res["dimensoes"].items():
        print(f"{k:<24} {v['pontos']:>6}/{v['maximo']}")
    print(f"TOTAL {res['total']} (soma {res['_soma_dimensoes']}) · backend {backend} · hash {res['_hash_ok']} · prova de leitura "
          f"{pv['ok']} (última {pv['ultima_frase']}, marcador {pv['frase_apos_marcador']}) · entrega {entrega.get('ok')}")
    print("VÁLIDA" if res["_valida"] else "[INVÁLIDA] a nota não vale (ver _hash_ok, _prova_leitura, _entrega)")
    for a in res.get("achados_criticos", []):
        print("  crítico:", a)
    return 0 if res["_valida"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
