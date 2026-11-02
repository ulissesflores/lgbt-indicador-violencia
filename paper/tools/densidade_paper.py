#!/usr/bin/env python3
"""Density checker do `paper.md` (fase A8 / F4 da `codex-hash-research`), em codigo.

As tres metricas sao aritmeticas -- contagem de termos, de filler e de ancoras -- entao rodam
como codigo deterministico e nao como julgamento de modelo. O julgamento fica com o juiz externo
da rubrica; aqui so entram numeros que qualquer um recomputa.

  TDI          = termos tecnicos DISTINTOS x 500 / palavras          alvo >= 3
  filler_ratio = palavras casadas por padrao de filler / palavras    alvo < 0,12
  info_density = (citacoes + numeros + ancoras de resultado) / (palavras/500)   alvo >= 0,15

A lista de termos e DECLARADA aqui e e do dominio deste paper (epidemiologia de violencia,
inferencia causal, survey e auditoria de fontes) -- a lista do template e de outra disciplina.
Adaptado de um artigo anterior do laboratório (repositório privado). Lista declarada
em arquivo e auditavel; lista na cabeca de quem mede, nao.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1] / "paper.md"

TERMOS = [
    "identificabilidade", "identifica", "TWFE", "efeitos fixos", "Goodman-Bacon", "wild-cluster", "bootstrap",
    "efeito de desenho", "deff", "unidade primária", "Taylor", "jackknife", "razão de prevalências",
    "razão de chances", "razão de mortalidade padronizada", "Poisson", "Kitagawa", "padronizada por idade",
    "Chapman", "captura-recaptura", "κ", "Wilson", "Fisher", "N1", "N2", "N3", "N4", "X85-Y09", "Y10-Y34",
    "campo 55", "Sinan", "SIM", "PNS", "PNAD Contínua", "CID-10", "Lei de Campbell", "pré-registro", "sha256",
    "ledger", "estudo de eventos", "antecipações", "tendências paralelas", "falsificação", "IC95%",
    "cobertura implícita", "subnotificação", "linkage", "Q1", "SJR", "texto integral", "espaço enumerado",
    "steel-man", "adendo", "codificador", "livro de códigos", "linha de base", "disparidade residual",
    "contrafactual", "desenho complexo", "peso calibrado", "sobreamostra", "triagem", "poder", "heterogeneidade",
    "I²", "meta-análise", "retratação", "não substanciada", "TDoR", "chain_hash", "determinística",
    "controle negativo", "controle positivo", "ODIHR", "ICCS", "ADO 26", "proxy", "numerador", "denominador",
    "propensão de registro", "incidência", "UF-anos", "clusters", "escore", "post hoc", "ceteris paribus",
    # v0.3 (2026-10-24): termos técnicos das seções novas (mortalidade no mundo, exposição por governo, correções)
    "vinculação", "fator de aceleração", "razão de taxas", "inversão do teste", "placebo", "efeito mínimo detectável",
    "faltante efetivo", "intenção indeterminada", "Holm", "Spearman", "correlação parcial", "elegibilidade",
    "regra literal", "cenário de subtração", "marginais", "autorrelato", "prevalência", "interação", "ONS",
    "expectativa de vida", "padronização", "graus de liberdade", "intervalo de contagem", "razão contagem/esperado",
]

FILLER = [
    r"\bé importante (notar|destacar|salientar|frisar)\b",
    r"\bvale (a pena |a )?(ressaltar|destacar|mencionar)\b",
    r"\bde (certa |alguma )?forma\b",
    r"\bno final das contas\b",
    r"\bao fim e ao cabo\b",
    r"\bdiversos? (autores?|estudos?)\s*(?!\()",
    r"\b(como|conforme) já (mencionado|dito) anteriormente\b",
    r"\bao longo do trabalho\b",
    r"\bem conclusão\b",
    r"\bcabe (ressaltar|destacar|notar)\b",
    r"\bnesse sentido\b",
    r"\bpode-se dizer que\b",
    # padroes verbatim da skill density-checker (lista do laboratório, privada; copiada aqui)
    r"\barguably|seems?|appears?|might|may|could\b",
    r"\bem (relação|termos) (a|de)\s+(\w+\s+){3,}\bque\b",
    r"\ba (maioria|grande parte) dos?\s+\w+\s+\w+",
    r"\bpode-se afirmar que\b",
    r"\b(robusto|moderno|inovador|eficiente|escalável|eficaz)\b(?!\s+(em|para|de|por|com))",
]

ANCORA = re.compile(r"<!--\s*num:[A-Za-z0-9_.\[\]-]+\s*-->")
CITACAO = re.compile(r"\([A-ZÀ-Ú][\wÀ-ú.&\- ]+,\s*\d{4}[a-z]?\)|\b[A-ZÀ-Ú][\wÀ-ú-]+ (?:e|&|et al\.) [\wÀ-ú.&]* ?\(\d{4}\)")
NUMERO = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?%?(?![\w])")


def corpo(texto: str) -> str:
    """Corpo argumentativo: sem front-matter YAML, sem referencias e sem apendices."""
    if texto.startswith("---"):
        texto = texto.split("\n---\n", 1)[1]
    corte = texto.find("\n## Referências")
    return texto[:corte] if corte != -1 else texto


def main() -> int:
    if not PAPER.exists():
        print(f"[FAIL] paper ausente: {PAPER}")
        return 1
    texto = corpo(PAPER.read_text(encoding="utf-8"))
    limpo = ANCORA.sub(" ", texto)
    palavras = len(re.findall(r"\b[\wÀ-ú-]+\b", limpo))

    baixo = limpo.lower()
    # fronteira de palavra: "SIM" nao pode casar dentro de "assim" (substring inflaria o TDI)
    distintos = sorted({t for t in TERMOS
                        if re.search(r"(?<![\wÀ-ú])" + re.escape(t.lower()) + r"(?![\wÀ-ú])", baixo)})
    tdi = len(distintos) * 500 / palavras

    filler_palavras = 0
    achados: list[str] = []
    for p in FILLER:
        for m in re.finditer(p, limpo, re.IGNORECASE):
            filler_palavras += len(m.group(0).split())
            achados.append(m.group(0))
    filler = filler_palavras / palavras

    n_cit = len(CITACAO.findall(limpo))
    n_num = len(NUMERO.findall(limpo))
    n_anc = len(ANCORA.findall(texto))
    info = (n_cit + n_num + n_anc) / (palavras / 500)

    print(f"palavras (corpo, sem apêndices): {palavras}")
    print(f"TDI          = {tdi:.2f}   (alvo >= 3)      · {len(distintos)} termos distintos")
    print(f"filler_ratio = {filler:.4f} (alvo < 0,12)   · {len(achados)} ocorrência(s)")
    print(f"info_density = {info:.2f}  (alvo >= 0,15)   · {n_cit} citações + {n_num} números + {n_anc} âncoras")
    if achados:
        print("  filler encontrado: " + "; ".join(sorted(set(achados))))
    print("  termos não encontrados: " + ", ".join(t for t in TERMOS if t not in distintos))

    falhas = []
    if tdi < 3:
        falhas.append(f"TDI {tdi:.2f} < 3")
    if filler >= 0.12:
        falhas.append(f"filler {filler:.4f} >= 0,12")
    if info < 0.15:
        falhas.append(f"info_density {info:.2f} < 0,15")
    for f in falhas:
        print(f"[FAIL] {f}")
    if falhas:
        return 1
    print("[PASS] as três métricas de densidade batem o alvo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
