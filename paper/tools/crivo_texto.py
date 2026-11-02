#!/usr/bin/env python3
"""Crivo de TEXTO (P4a, para a frente de conteudo): lista os paragrafos do corpo sem lastro visivel.

    python3 tools/crivo_texto.py [paper.md] [--tudo] [--json]

So LE o markdown (nao altera nada). Escopo: do primeiro titulo numerado ("1. Introdução") ate "Referências";
`--tudo` inclui Resumo, Abstract, apendices e anexos. Por paragrafo de afirmacao (titulo, tabela, imagem,
rotulo/titulo de tabela e figura e "*Nota.*" ficam de fora: a Nota carrega a fonte), o crivo procura UM destes
quatro lastros e lista o paragrafo se nao achar nenhum:

  (a) citacao autor-data: "(Autor, 2023)", "(Autor & Outro, 2023a; ONS, 2026)", "Autor et al. (2023)";
  (b) remissao a "Tabela N" / "Figura N" (tambem "Tabela A1"): o dado esta no elemento;
  (c) remissao interna: "§", "seção 3.4", "seções 3.2 e 3.3", "Apêndice A", "Anexo C" (o artigo usa
      "seção N" onde a frente pediu "§": mesma funcao de apontar onde a afirmacao e sustentada);
  (d) fonte do dado em caminho de arquivo do repositorio entre crases (`dados/pns/seguro_pns2019.md`).

Excecoes legitimas (vao para o grupo "isento", listadas a parte para revisao, NAO contam como falha):
  E1 transicao: paragrafo curto (ate 18 palavras) ou que termina em ":" (anuncia lista ou tabela);
  E2 definicao propria de metodo: paragrafo dentro de secao cujo titulo e de metodo/desenho/regras do
     proprio estudo (Dados e métodos, Hipóteses, Busca bibliográfica, Pré-registros). Se o paragrafo afirmar
     algo de terceiros sem citar, o revisor humano ve na lista;
  E3 item de lista curto de navegacao ("Como ler este artigo").

Alem do lastro, tres varreduras de FORMA DO TEXTO que o crivo de DOCX nao ve:
  R1 remissao a dois PDFs ("PDF de anexos", "artigo principal"): agora e um PDF so;
  R2 jargao de processo ("revisor hostil", "sopa", "cluster", "flanco", "rodada", "triagem");
  R3 placeholder ("[REPO_URL]", "[SHA-...]", "a atualizar", "a criar", "ainda a ...").
Exit: 0 limpo; 1 se houver paragrafo sem lastro ou R1/R2/R3.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ANO = r"(?:19|20)\d{2}[a-z]?"
RE_ROTULO = re.compile(r"^\*\*(Tabela|Figura|Quadro) [A-Z]?\d+\*\*\s*$")
RE_TITULO_ELEM = re.compile(r"^\*(?!\*)[^*].*\*\s*$")
RE_TAB_FIG = re.compile(r"\b(?:Tabelas?|Figuras?|Quadros?)\s+[A-Z]?\d+")
RE_INTERNA = re.compile(r"§|\bseç(?:ão|ões)\s+\d|\bApêndices?\s+[A-Z]\b|\bAnexos?\s+[A-Z]\b")
RE_DADO = re.compile(r"`[\w./\-]+\.(?:md|csv|tsv|py|txt|json|pdf)`")
RE_AUTOR_ANO = re.compile(r"^[A-ZÀ-Ý][^\d()]{1,100}?,?\s*" + ANO + r"\b")
RE_PRECEDE_AUTOR = re.compile(r"(?:[A-ZÀ-Ý][\wÀ-ÿ’'\-\.]+|et al\.)\s*$")
SECOES_METODO = re.compile(r"dados e métodos|métodos|hipóteses|busca bibliográfica|pré-regist|desenho|regras", re.I)
SECOES_FORA = re.compile(r"^(resumo|abstract|palavras-chave|keywords|como ler|quem é quem|respostas diretas)", re.I)
RE_R1 = re.compile(r"PDF de anexos|artigo principal|PDF principal|segundo PDF")
RE_R2 = re.compile(r"revisor(?:es)? hostis?|\bhostis\b|\bsopa\b|\bclusters? d[aeo]s? (?:revis|ataques?|crític)|\bflancos?\b|primeira rodada|"
                   r"segunda rodada|\btriagem\b", re.I)
RE_R3 = re.compile(r"\[(?:REPO_URL|SHA[-\w…\.]*|[A-Z]{2,}(?:_[A-Z0-9]+)+|TODO|TBD)\]|a atualizar|ainda a (?:criar|definir)|"
                   r"a ser atribu[ií]do")


def tem_citacao(p: str) -> bool:
    for m in re.finditer(r"\(([^()]*)\)", p):
        g = m.group(1)
        if not re.search(ANO, g):
            continue
        if any(RE_AUTOR_ANO.match(parte.strip()) for parte in g.split(";")):
            return True
        if re.fullmatch(r"\s*" + ANO + r"(?:,?\s*pp?\.\s*[\d\-–]+)?\s*", g) and RE_PRECEDE_AUTOR.search(p[:m.start()]):
            return True
    return False


def paragrafos(texto: str) -> list[tuple[int, str, str]]:
    """(linha, secao, texto) de cada bloco de prosa; descarta titulo, tabela, imagem, rotulo, nota e comentario."""
    out, secao = [], ""
    bloco, ini = [], 0
    em_codigo = False

    def fecha() -> None:
        nonlocal bloco
        if bloco:
            txt = " ".join(x.strip() for x in bloco).strip()
            out.append((ini, secao, txt))
        bloco = []

    for n, ln in enumerate(texto.splitlines(), 1):
        if ln.startswith("```"):
            fecha()
            em_codigo = not em_codigo
            continue
        if em_codigo:
            continue
        if ln.startswith("#"):
            fecha()
            secao = ln.lstrip("#").strip()
            continue
        if not ln.strip():
            fecha()
            continue
        if ln.startswith(("|", "![", "<!--", ":::")):
            fecha()
            continue
        if not bloco:
            ini = n
        bloco.append(ln)
    fecha()
    saida = []
    for n, sec, txt in out:
        if RE_ROTULO.match(txt) or txt.startswith(("*Nota", "Nota.", "Fonte:")):
            continue
        if RE_TITULO_ELEM.match(txt) and len(txt) < 400 and not txt.startswith("*Nota"):
            continue
        saida.append((n, sec, txt))
    return saida


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", nargs="?", default=str(Path(__file__).resolve().parents[1] / "paper.md"))
    ap.add_argument("--tudo", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    texto = Path(a.md).read_text(encoding="utf-8")
    texto = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.S)
    texto = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)
    ps = paragrafos(texto)
    # escopo
    corpo, dentro = [], a.tudo
    for n, sec, txt in ps:
        if re.match(r"^1\.\s", sec):
            dentro = True
        if sec.strip() == "Referências":
            dentro = a.tudo
        if dentro:
            corpo.append((n, sec, txt))
    sem, isento = [], []
    for n, sec, txt in corpo:
        nw = len(txt.split())
        if tem_citacao(txt) or RE_TAB_FIG.search(txt) or RE_INTERNA.search(txt) or RE_DADO.search(txt):
            continue
        if nw <= 18 or txt.endswith(":"):
            isento.append((n, sec, nw, txt, "E1 transição"))
        elif SECOES_METODO.search(sec):
            isento.append((n, sec, nw, txt, "E2 método próprio"))
        elif SECOES_FORA.match(sec):
            isento.append((n, sec, nw, txt, "E3 navegação"))
        else:
            sem.append((n, sec, nw, txt))
    stale = [(n, sec, m.group(0)) for n, sec, txt in ps for m in [RE_R1.search(txt)] if m]
    jarg = [(n, sec, m.group(0)) for n, sec, txt in ps for m in [RE_R2.search(txt)] if m]
    plac = [(n, sec, m.group(0)) for n, sec, txt in ps for m in [RE_R3.search(txt)] if m]
    if a.json:
        print(json.dumps({"sem_lastro": [list(x) for x in sem], "isentos": [list(x) for x in isento],
                          "R1": stale, "R2": jarg, "R3": plac}, ensure_ascii=False, indent=1))
    else:
        print(f"# crivo de texto: {a.md}\n")
        print(f"Parágrafos de prosa no escopo: {len(corpo)}; com lastro (a-d): {len(corpo) - len(sem) - len(isento)}; "
              f"isentos (E1-E3): {len(isento)}; SEM lastro: {len(sem)}\n")
        print("## Sem lastro (nenhuma citação autor-data, Tabela/Figura, seção/§ nem arquivo de dado)")
        for n, sec, nw, txt in sem:
            print(f"- L{n} [{sec[:48]}] {nw} palavras: \"{txt[:110]}...\"")
        print("\n## Isentos (revisar rapidamente; não contam como falha)")
        for n, sec, nw, txt, motivo in isento:
            print(f"- L{n} [{sec[:40]}] {motivo}, {nw} palavras: \"{txt[:80]}...\"")
        for titulo, lista in (("R1 remissão a dois PDFs", stale), ("R2 jargão de processo", jarg), ("R3 placeholder", plac)):
            print(f"\n## {titulo}: {len(lista)}")
            for n, sec, achado in lista:
                print(f"- L{n} [{sec[:40]}] {achado!r}")
    return 1 if (sem or stale or jarg or plac) else 0


if __name__ == "__main__":
    sys.exit(main())
