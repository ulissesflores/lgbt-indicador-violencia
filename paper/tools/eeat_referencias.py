#!/usr/bin/env python3
"""Score E-E-A-T (0-100) das referencias do paper, pela formula da skill `citation-eeat`.

    Score = 0.30*Recency + 0.40*Authority + 0.15*Diversity + 0.15*Relevance   (+5 se DOI)

A formula e aritmetica; o que exige julgamento e a CLASSIFICACAO de cada referencia, que fica
DECLARADA na tabela CLASSE abaixo, linha a linha. A LISTA de referencias, o ano e o DOI NAO sao
declarados aqui: sao lidos da secao "## Referências" do paper.md (v0.4.1, E5: a versao anterior
trazia uma lista fixa de 78 entradas montada para a v0.3 e deixou de acompanhar o artigo). O script
falha (exit 2) se uma referencia do paper nao tiver classificacao ou se sobrar classificacao sem
referencia, para que a tabela nao envelheca em silencio.

Regras de classificacao deste paper (conservadoras):

  authority  85 = periodico revisado por pares (nenhum periodico recebeu 100, mesmo Q1)
             90 = norma oficial (lei, vigente ou historica) ou padrao estatistico internacional (ICCS, ODIHR)
             80 = relatorio ou microdado de orgao estatal/intergovernamental; livro academico revisado
             70 = conjunto de dados de replicacao (Dataverse); texto para discussao; auto-citacao
             50 = relatorio de organizacao da sociedade civil (contagem declarada); texto de divulgacao
  recency    pela tabela da skill (<=1 ano 100; <=3 80; <=5 60; <=10 40; >10 20);
             +30 para classico seminal (Holland 1986, Campbell 1979); norma vigente = 80 forcado
  relevance  100 tema direto; 70 adjacente; 40 tangencial
  boost      +5 so com DOI (lido do paper); o boost de URL acessivel NAO e aplicado (HTTP 200 nao verificado em lote)

Tambem calcula a fracao de referencias dos ultimos 3 anos (2023-2026) e o numero de tipos.

    python3 -I tools/eeat_referencias.py [paper.md]
"""
from __future__ import annotations

import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HOJE = 2026
PAPER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "paper.md"

# chave (1o sobrenome ou autor institucional + ano do paper) -> (n_autores, instituicoes_distintas, authority, relevance,
# seminal, norma_vigente, tipo)
CLASSE = {
    "Asal 2013": (3, True, 85, 70, False, False, "periódico"),
    "Benevides 2026": (1, False, 50, 100, False, False, "sociedade civil"),
    "Bolognesi 2023": (3, True, 85, 70, False, False, "periódico"),
    "Bolognesi 2025": (4, True, 70, 70, False, False, "dataset"),
    "Brasil 2026": (5, False, 90, 70, False, True, "lei"),
    "Bundeskriminalamt 2026": (5, False, 80, 70, False, False, "relatório oficial"),
    "Câmara dos Deputados 2026": (5, False, 80, 70, False, False, "dataset oficial"),
    "Campbell 1979": (1, False, 85, 100, True, False, "periódico"),
    "Cerqueira 2017": (2, False, 70, 70, False, False, "working paper"),
    "CIDH 1983": (5, True, 80, 70, False, False, "relatório oficial"),
    "Clark 2024": (2, True, 85, 100, False, False, "periódico"),
    "Clark 2026": (6, True, 85, 70, False, False, "periódico"),
    "Cochran 2015": (2, False, 85, 100, False, False, "periódico"),
    "Comissão Nacional da Verdade 2014": (5, True, 80, 70, False, False, "relatório oficial"),
    "DATASUS 2026a": (5, False, 80, 100, False, False, "dataset oficial"),
    "DATASUS 2026b": (5, False, 80, 100, False, False, "dataset oficial"),
    "Deutscher Bundestag 2017": (5, False, 80, 70, False, False, "relatório oficial"),
    "D'Ignazio 2022": (8, True, 85, 70, False, False, "periódico"),
    "Dinno 2017": (1, False, 85, 100, False, False, "periódico"),
    "Encarnación 2014": (1, False, 85, 70, False, False, "periódico"),
    "Erlangsen 2023": (6, True, 85, 100, False, False, "periódico"),
    "España 1970": (5, False, 90, 70, False, False, "lei"),
    "España 1979": (5, False, 90, 70, False, False, "lei"),
    "España 2022": (5, False, 90, 70, False, True, "lei"),
    "FBSP 2026": (5, True, 80, 100, False, False, "relatório oficial"),
    "Feldman 2017": (4, True, 85, 70, False, False, "periódico"),
    "Ferguson 2016": (2, False, 85, 70, False, False, "periódico"),
    "Fernández Turuelo 2024": (1, False, 85, 70, False, False, "periódico"),
    "Flores 2026": (1, False, 70, 100, False, False, "auto-citação"),
    "FRA 2024": (5, False, 80, 100, False, False, "relatório oficial"),
    "Frisch 2009": (2, False, 85, 100, False, False, "periódico"),
    "GGB 2020": (2, False, 50, 100, False, False, "sociedade civil"),
    "GGB 2026": (1, False, 50, 100, False, False, "sociedade civil"),
    "Goodman-Bacon 2021": (1, False, 85, 70, False, False, "periódico"),
    "Greiner 2011": (2, True, 85, 100, False, False, "periódico"),
    "Halliwell 2025": (5, True, 85, 70, False, False, "periódico"),
    "Hatzenbuehler 2014": (6, True, 85, 100, False, False, "periódico"),
    "Hatzenbuehler 2020": (5, True, 85, 100, False, False, "periódico"),
    "Henningsmeier 2025": (5, True, 80, 70, False, False, "livro"),
    "Holland 1986": (1, False, 85, 100, True, False, "periódico"),
    "Home Office 2025": (5, False, 80, 100, False, False, "relatório oficial"),
    "Hsu 2025": (8, True, 85, 70, False, False, "periódico"),
    "Human Rights Watch 2017": (5, False, 50, 70, False, False, "sociedade civil"),
    "IBGE 2022a": (5, False, 80, 100, False, False, "dataset oficial"),
    "IBGE 2022b": (5, False, 80, 100, False, False, "relatório oficial"),
    "IBGE 2023": (5, False, 80, 70, False, False, "relatório oficial"),
    "IBGE 2026": (5, False, 80, 70, False, False, "dataset oficial"),
    "ILGA World 2020": (5, False, 50, 70, False, False, "sociedade civil"),
    "IPEA & FBSP 2025": (5, True, 80, 100, False, False, "relatório oficial"),
    "IPEA & FBSP 2026": (5, True, 80, 100, False, False, "relatório oficial"),
    "Kahan 2017": (4, True, 85, 70, False, False, "periódico"),
    "Kondakov 2022": (1, False, 80, 40, False, False, "livro"),
    "Levy 2017": (2, True, 85, 100, False, False, "periódico"),
    "Luis 2026": (10, True, 85, 100, False, False, "periódico"),
    "Lum 2013": (3, True, 85, 70, False, False, "periódico"),
    "Marinho Neto 2024": (3, True, 85, 100, False, False, "periódico"),
    "McKetta 2024": (8, True, 85, 100, False, False, "periódico"),
    "McKetta 2026": (6, True, 85, 70, False, False, "periódico"),
    "McLellan 2026": (7, True, 85, 70, False, False, "periódico"),
    "MDHC 2026": (5, False, 80, 40, False, False, "dataset oficial"),
    "Mendes 2020": (2, True, 85, 100, False, False, "periódico"),
    "Ministério da Justiça e Segurança Pública & IBGE 2021": (5, True, 80, 70, False, False, "relatório oficial"),
    "Ministério da Saúde & IBGE 2023": (5, True, 80, 70, False, False, "relatório oficial"),
    "Ministério da Saúde 2022": (5, False, 80, 100, False, False, "relatório oficial"),
    "Ministério da Saúde 2024": (5, False, 80, 100, False, False, "relatório oficial"),
    "Ministry of Justice 2025": (5, False, 80, 100, False, False, "relatório oficial"),
    "ONS 2025": (5, False, 80, 100, False, False, "relatório oficial"),
    "ONS 2026a": (5, False, 80, 100, False, False, "relatório oficial"),
    "ONS 2026b": (5, False, 80, 100, False, False, "relatório oficial"),
    "OSCE 2018": (1, False, 80, 70, False, False, "relatório oficial"),
    "OSCE/ODIHR 2014": (5, False, 90, 70, False, True, "padrão internacional"),
    "OSCE/ODIHR 2025": (5, False, 80, 100, False, False, "relatório oficial"),
    "OutRight Action International 2015": (5, False, 50, 40, False, False, "sociedade civil"),
    "Pettis 2022": (3, True, 85, 100, False, False, "periódico"),
    "Rafael 2024": (6, True, 85, 100, False, False, "periódico"),
    "Reynolds 2013": (1, False, 85, 70, False, False, "periódico"),
    "Saxby 2026": (4, True, 85, 70, False, False, "periódico"),
    "Senado Federal 2026": (5, False, 80, 70, False, False, "dataset oficial"),
    "Siegel 2018": (2, True, 85, 70, False, False, "periódico"),
    "Silva/Magalhães 2026": (8, True, 85, 100, False, False, "periódico"),
    "Silva/Pazin-Filho 2026": (2, True, 85, 70, False, False, "periódico"),
    "Sleath 2017": (2, True, 85, 70, False, False, "periódico"),
    "Statistics Canada 2026": (5, False, 80, 100, False, False, "relatório oficial"),
    # v0.4.4 (E8): acórdão do STF citado na Tabela 1 (fonte primária do enquadramento dos boletins); mesmo critério do TEDH
    "Supremo Tribunal Federal 2019": (5, False, 80, 70, False, False, "decisão judicial"),
    "Szulc 2016": (1, False, 70, 70, False, False, "working paper"),
    "Szulc 2018": (1, False, 50, 70, False, False, "divulgação"),
    "Szwarcwald 2025": (4, True, 85, 100, False, False, "periódico"),
    "Tahbaz 2013": (1, False, 85, 70, False, False, "periódico"),
    "Tribunal Europeu dos Direitos Humanos 2023": (5, False, 80, 40, False, False, "decisão judicial"),
    "TSE 2026": (5, False, 80, 70, False, False, "dataset oficial"),
    "UNAMI & OHCHR 2015": (5, True, 80, 70, False, False, "relatório oficial"),
    "United States Holocaust Memorial Museum 2021": (5, False, 80, 70, False, False, "relatório oficial"),
    "UNODC 2015": (5, False, 90, 70, False, True, "padrão internacional"),
    "Valodzin 2020": (1, False, 70, 70, False, False, "working paper"),
    "VanderWeele 2014": (2, True, 85, 70, False, False, "periódico"),
    "Vasconcelos 2023": (7, True, 85, 100, False, False, "periódico"),
    "Zachry 2025": (5, True, 85, 100, False, False, "periódico"),
    "Zucco 2023": (2, True, 70, 70, False, False, "dataset"),
}


def referencias(caminho: Path) -> list[tuple[str, int, bool]]:
    """(chave, ano, tem_doi) de cada paragrafo da secao Referencias do paper.md."""
    texto = caminho.read_text(encoding="utf-8")
    bloco = texto.split("\n## Referências", 1)[1].split("\n## Apêndice A", 1)[0]
    paragrafos = [p.strip() for p in bloco.split("\n\n") if re.search(r"\((19|20)\d\d", p)]
    saida, vistos = [], {}
    for p in paragrafos:
        autor = p.split(" (", 1)[0]
        ano_txt = re.search(r"\(((?:19|20)\d\d[a-z]?)", p).group(1)
        primeiro = re.split(r",|\.$", autor, maxsplit=1)[0].strip().rstrip(".")
        chave = f"{primeiro} {ano_txt}"
        vistos.setdefault(chave, []).append((autor, int(ano_txt[:4]), "doi.org/" in p))
    for chave, itens in vistos.items():
        if len(itens) == 1:
            saida.append((chave, itens[0][1], itens[0][2]))
            continue
        for autor, ano, doi in itens:  # mesma chave: desempata pelo 2o sobrenome
            segundo = re.split(r",\s*(?:&\s*)?", autor)[2].strip()
            saida.append((f"{chave.split(' ')[0]}/{segundo} {chave.rsplit(' ', 1)[1]}", ano, doi))
    return saida


def um_decimal(x: float) -> float:
    """Arredonda a 1 casa MEIO PARA CIMA (regra do projeto), e nao o arredondamento do banqueiro do Python."""
    return float(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def recency(ano: int, seminal: bool, norma: bool) -> int:
    """Pontos de recencia pela tabela da skill, com as excecoes declaradas."""
    if norma:
        return 80
    idade = HOJE - ano
    base = 100 if idade <= 1 else 80 if idade <= 3 else 60 if idade <= 5 else 40 if idade <= 10 else 20
    return min(100, base + (30 if seminal else 0))


def diversity(n: int, inst: bool) -> int:
    """Pontos de diversidade de autoria pela tabela da skill."""
    base = 50 if n == 1 else 70 if n == 2 else 90 if n <= 4 else 100
    return min(100, base + (10 if inst else 0))


def main() -> int:
    """Imprime a tabela, a media, a fracao recente e os tipos; exit 1 se media < 75; exit 2 se a tabela nao cobre o paper."""
    refs = referencias(PAPER)
    chaves = [c for c, _, _ in refs]
    faltam, sobram = sorted(set(chaves) - set(CLASSE)), sorted(set(CLASSE) - set(chaves))
    if faltam or sobram or len(chaves) != len(set(chaves)):
        print(f"[FAIL] classificação não cobre o paper: sem classe {faltam}; classe sem referência {sobram}")
        return 2
    total, abaixo, recentes, tipos = 0.0, [], 0, set()
    print(f"{'referência':<52} {'ano':>4} {'rec':>4} {'aut':>4} {'div':>4} {'rel':>4} {'score':>6}")
    for chave, ano, doi in refs:
        n, inst, aut, rel, sem, norma, tipo = CLASSE[chave]
        r, d = recency(ano, sem, norma), diversity(n, inst)
        s = min(100.0, um_decimal(0.30 * r + 0.40 * aut + 0.15 * d + 0.15 * rel + (5 if doi else 0)))
        total += s
        recentes += ano >= HOJE - 3
        tipos.add(tipo)
        if s < 75:
            abaixo.append((chave, s))
        print(f"{chave:<52} {ano:>4} {r:>4} {aut:>4} {d:>4} {rel:>4} {s:>6.1f}")
    media = total / len(refs)
    print(f"\nreferências lidas do paper: {len(refs)} ({PAPER.name}) · tipos distintos: {len(tipos)} ({', '.join(sorted(tipos))})")
    menu = {"paper": {"periódico", "working paper"}, "livro": {"livro"},
            "norma oficial (RFC/NIST no gênero)": {"lei", "decisão judicial"},
            "framework / padrão": {"padrão internacional"},
            "documentação oficial de dados (builder's library no gênero)": {"dataset oficial", "dataset", "relatório oficial"}}
    cobertos = [k for k, v in menu.items() if v & tipos]
    print(f"menu de 6 tipos da rubrica, equivalência declarada: {len(cobertos)}/5 aplicáveis cobertos -> {'; '.join(cobertos)}")
    print(f"últimos 3 anos (>= {HOJE - 3}): {recentes}/{len(refs)} = {um_decimal(100 * recentes / len(refs)):.1f}%")
    print(f"média E-E-A-T = {um_decimal(media):.1f}/100 (limiar 75) · abaixo de 75: {len(abaixo)}"
          + (" -> " + "; ".join(f"{r} {s:.1f}" for r, s in abaixo) if abaixo else ""))
    ok = media >= 75
    print("[PASS] média E-E-A-T >= 75" if ok else "[FAIL] média abaixo de 75")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
