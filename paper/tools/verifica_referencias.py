#!/usr/bin/env python3
"""Quatro probes sobre as referencias e o vocabulario do paper (exit = numero de falhas).

1. PERTENCIMENTO: todo DOI/URL da lista tem linha em algum dos 17 ledgers `sources.jsonl` do
   projeto privado. Excecao declarada (lista EXCECOES): fonte lida pela frente "simetria", que
   nao emite ledger jsonl; a proveniencia e o arquivo baixado com sha256 em SHA256SUMS-cuba.txt.
2. AUTORIA: para referencia com DOI, o 1o sobrenome e o ano da lista batem com os metadados
   Crossref/DataCite em cache (tools/cache/doi_meta.json, gerado por crossref_meta.py).
3. CITACAO <-> LISTA: toda referencia e citada no corpo (autor e ano) e todo "(Autor, ano)" do
   corpo tem referencia.
4. VOCABULARIO: frases proibidas pela regra de evidencia ("primeira vez", "inédito",
   "ninguém", "nenhum estudo", "falso/falsa" como veredito) e strings proibidas pelo canon.

Uso: python3 -I tools/verifica_referencias.py [paper.md alternativo]   (precisa do projeto privado para o probe 1)
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PAPER = AQUI.parent / "paper.md"
PRIVADO = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[2])  # raiz do repositório (ledgers sources.jsonl)
CANON = Path(os.environ.get("CODEX_HASH_CANON", "codex-hash-canon.json"))  # canon da casa (opcional; não distribuído)
EXCECOES = {"cidh.oas.org/countryrep/cuba83sp/capitulo10.htm":
            "research-2026-10-21-rodada3/escrutinio/simetria/SHA256SUMS-cuba.txt (frente sem ledger jsonl)",
            # v0.3: dados oficiais lidos por script, sem linha em ledger jsonl; proveniência no manifesto ou nas contagens
            "cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2022.zip":
            "manifest/MANIFESTO-FONTES.csv (linhas B-bruto TSE, SHA-256 de cada arquivo)",
            "dadosabertos.camara.leg.br/api/v2":
            "research-2026-10-21-rodada3/discurso/midia/contagens.csv e scripts/camara_baixar.py (API pública)",
            "legis.senado.leg.br/dadosabertos":
            "research-2026-10-21-rodada3/discurso/midia/contagens.csv e scripts/senado_baixar.py (API pública)",
            # v0.4: auto-citação do repositório companion (é a origem dos dados, não fonte de ledger)
            "github.com/ulissesflores/lgbt-indicador-violencia": "auto-citação: o próprio repositório companion"}
CORPORATIVOS = ["Tribunal Europeu dos Direitos Humanos", "Câmara dos Deputados", "Senado Federal", "Ministério da Saúde",
                "DATASUS", "MDHC", "ONS", "TSE", "Comissão Nacional da Verdade", "Statistics Canada",
                "Ministry of Justice", "Bundeskriminalamt", "Home Office", "IPEA & FBSP", "OSCE/ODIHR", "OSCE",
                "UNODC", "IBGE", "FBSP", "GGB", "CIDH", "FRA", "Brasil", "España"]


def sem_acento(t: str) -> str:
    """Minusculas sem diacriticos, para comparar sobrenomes."""
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()


def norm(u: str) -> str:
    """Forma canonica de DOI/URL."""
    u = u.strip().rstrip(".,;)").lower()
    u = re.sub(r"^https?://(dx\.)?doi\.org/", "", u)
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.rstrip("/")


def partes(texto: str) -> tuple[str, list[str]]:
    """Corpo (antes de ## Referências) e itens da lista de referencias."""
    texto = texto.split("\n---\n", 1)[1] if texto.startswith("---") else texto
    ini, fim = texto.index("## Referências"), texto.index("## Apêndice A")
    # v0.4: APA 7 em paragrafos (uma referencia por paragrafo); o formato antigo, em lista "- ", continua aceito
    linhas = [l.strip() for l in texto[ini:fim].splitlines()[1:] if l.strip() and not l.startswith(("#", "*Nota", "*Nível"))]
    itens = [l[2:] if l.startswith("- ") else l for l in linhas]
    corpo = texto[:ini] + texto[fim:]
    return corpo, itens


def rotulo(item: str) -> tuple[str, str]:
    """(primeiro autor ou entidade, ano) de um item da lista."""
    ano = re.search(r"\((\d{4}[a-z]?)(?:, [^)]*)?\)", item).group(1)  # sufixo de letra (2026a) e data APA "(2015, 24 de agosto)"
    for c in CORPORATIVOS:
        if item.startswith(c):
            return c, ano
    corp = re.match(r"^([^,(]+?)\. \(\d{4}", item)  # autor institucional sem vírgula: "Deutscher Bundestag. (2017)"
    return (corp.group(1).strip() if corp else item.split(",")[0].strip()), ano


def chaves_ledger() -> set[str]:
    """Todos os ids e urls dos ledgers, normalizados."""
    out: set[str] = set()
    for f in PRIVADO.glob("**/sources.jsonl"):
        if "/fontes/" in str(f) or "/.run/" in str(f):
            continue
        for linha in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(linha)
            except json.JSONDecodeError:
                continue
            for k in ("id", "url"):
                if r.get(k):
                    out.add(norm(str(r[k])))
    return out


def main() -> int:
    """Roda os quatro probes e imprime uma linha por achado."""
    texto = (Path(sys.argv[1]) if len(sys.argv) > 1 else PAPER).read_text(encoding="utf-8")
    corpo, itens = partes(texto)
    falhas = 0

    # 1. pertencimento
    if PRIVADO.exists():
        led = chaves_ledger()
        ok = 0
        for it in itens:
            ids = [norm(m) for m in re.findall(r"https?://\S+", it)]
            ids = [i for i in ids if "[repo_url]" not in i]
            if not ids:
                if "[REPO_URL]" in it:
                    print(f"  [info] auto-citação sem URL pública ainda: {it[:60]}")
                    ok += 1
                    continue
                print(f"[FAIL] sem DOI/URL: {it[:70]}")
                falhas += 1
                continue
            if any(i in led for i in ids):
                ok += 1
            elif any(i in EXCECOES for i in ids):
                print(f"  [exceção declarada] {it[:60]} -> {EXCECOES[[i for i in ids if i in EXCECOES][0]]}")
                ok += 1
            else:
                print(f"[FAIL] fora dos ledgers: {it[:70]} {ids}")
                falhas += 1
        print(f"1. pertencimento: {ok}/{len(itens)} referências com DOI/URL em ledger (ou exceção declarada)")
    else:
        print("1. pertencimento: PULADO (projeto privado ausente nesta máquina)")

    # 2. autoria
    meta = json.loads((AQUI / "cache" / "doi_meta.json").read_text(encoding="utf-8"))
    n_doi = 0
    for it in itens:
        m = re.search(r"https://doi\.org/(\S+)", it)
        if not m:
            continue
        n_doi += 1
        doi = m.group(1).rstrip(".").lower()
        md = meta.get(doi)
        if not md or md.get("fonte") == "erro":
            print(f"[FAIL] DOI sem metadado em cache: {doi}")
            falhas += 1
            continue
        autor, ano = rotulo(it)
        fam = sem_acento(md["autores"][0][0] or "")
        if sem_acento(autor.split()[0]) not in fam and fam.split()[-1] not in sem_acento(autor):
            print(f"[FAIL] autoria: lista '{autor}' x Crossref '{md['autores'][0][0]}' ({doi})")
            falhas += 1
        anos_ok = {str(md["ano"])}
        if doi == "10.56645/jmde.v7i15.297":
            anos_ok.add("1979")  # reimpressao de 2011 do original de 1979, declarada no item
        if ano.rstrip("abcdefgh") not in anos_ok:
            print(f"[FAIL] ano: lista {ano} x registro {md['ano']} ({doi})")
            falhas += 1
    print(f"2. autoria e ano: {n_doi} referências com DOI conferidas contra Crossref/DataCite")

    # 3. citacao <-> lista
    corpo_flat = re.sub(r"\s+", " ", corpo)
    nao_citadas = []
    for it in itens:
        autor, ano = rotulo(it)
        sob = autor.split(" &")[0].split(" —")[0]
        if not re.search(re.escape(sob) + r"[^()]{0,80}?\(?" + ano, corpo_flat):
            nao_citadas.append(f"{sob} ({ano})")
    for n in nao_citadas:
        print(f"[FAIL] referência não citada no corpo: {n}")
    falhas += len(nao_citadas)
    rotulos = {(rotulo(it)[0].split(" &")[0], rotulo(it)[1]) for it in itens}
    orfas = []
    for m in re.finditer(r"\(([A-ZÀ-Ú][^()]*?),\s*(\d{4}[a-z]?)\)", corpo_flat):
        for cit in m.group(0)[1:-1].split(";"):
            mm = re.match(r"\s*(.+?),\s*(\d{4}[a-z]?)", cit)
            if not mm:
                continue
            nome, ano = mm.group(1), mm.group(2)
            nome1 = re.split(r" et al\.| & ", nome)[0].strip()
            if not any(nome1.startswith(r[0].split(" ")[0]) and ano == r[1] for r in rotulos) and \
               not any(r[0] == nome1 and ano == r[1] for r in rotulos):
                orfas.append(cit.strip())
    for o in sorted(set(orfas)):
        print(f"[FAIL] citação sem referência: ({o})")
    falhas += len(set(orfas))
    print(f"3. citação <-> lista: {len(itens) - len(nao_citadas)}/{len(itens)} citadas; {len(set(orfas))} citação(ões) órfã(s)")

    # 4. vocabulario
    proibidas = [r"\bprimeir[ao] vez\b", r"\binédit[oa]s?\b", r"\bninguém\b", r"\bnenhum estudo\b",
                 r"\bé fals[oa]\b", r"\bfals[oa]s? \(veredito\)", r"\bAG" r"TU\b", r"American " r"Global",
                 r"Mestrando em Intelig"]
    if CANON.exists():
        canon = json.loads(CANON.read_text(encoding="utf-8"))
        proibidas += [re.escape(x) for x in canon["document"]["forbidden_strings"]]
    else:
        print("  [info] canon da casa ausente (CODEX_HASH_CANON): vocabulário conferido só com a lista fixa")
    achados = []
    # o título ditado pelo autor ("Gays morrem mais no Brasil? Ninguém sabe! ...") é citação literal dele, não asserção
    # de ausência do texto: fica fora da varredura (v0.2)
    titulo = re.search(r'^title:\s*"(.+)"', texto, re.M)
    if titulo:
        texto = texto.replace(titulo.group(1), "[título ditado]")
    for p in proibidas:
        for m in re.finditer(p, texto, flags=re.I):
            ctx = texto[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")
            achados.append(f"'{m.group(0)}' em …{ctx}…")
    # "falso" so e permitido quando cita o texto antigo corrigido (apendice B) ou a regra de vocabulario
    for m in re.finditer(r"\bfals[oa]s?\b", corpo, flags=re.I):
        ctx = corpo[max(0, m.start() - 60):m.end() + 40]
        if not re.search(r"palavra \"falso\"|\"falso\"|'Não existe' é falso|provadamente falsa|alegação falsa|denúncia falsa|"
                         r"falsas alegações|Falsas alegações|julgada intencionalmente falsa|alegações falsas", ctx):
            achados.append(f"'falso' fora do uso permitido: …{ctx.strip()}…")
    for a in achados:
        print(f"[FAIL] vocabulário: {a}")
    falhas += len(achados)
    print(f"4. vocabulário: {len(achados)} achado(s)")
    print("[PASS]" if falhas == 0 else f"[FAIL] {falhas} falha(s)")
    return falhas


if __name__ == "__main__":
    sys.exit(main())
