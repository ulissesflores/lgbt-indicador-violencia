#!/usr/bin/env python3
"""Gera o Apêndice A do artigo (tabelas completas) a partir dos arquivos do repositório, sem digitar número.

Cada tabela é copiada de um .md gerado por script do projeto ou montada de um .csv do repositório; o texto do
artigo só ganha a vírgula decimal (PT-BR), rótulos internos em português comum (mapa ROTULOS, nunca número) e o
formato APA 7 (rótulo "Tabela A<n>" em negrito, título em itálico acima, "Nota." abaixo). O bloco vai entre os
marcadores `<!-- apendice-a:inicio -->` e `<!-- apendice-a:fim -->` de `paper/paper.md`, no mesmo documento que o
corpo (um PDF só; os apêndices A a D seguem as Referências).

    python3 -I tools/make_anexos.py              # imprime o bloco
    python3 -I tools/make_anexos.py --escrever   # grava o bloco no paper.md
    python3 -I tools/make_anexos.py --conferir   # exit 1 se o bloco do paper.md divergir do gerado
    python3 -I tools/make_anexos.py --provar     # exit 1 se alguma célula mudar fora do mapa de rótulos
"""
from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parents[1]
REPO = PAPER_DIR.parent
PAPER = PAPER_DIR / "paper.md"
INI, FIM = "<!-- apendice-a:inicio -->", "<!-- apendice-a:fim -->"
FONTES = PAPER_DIR / "figures" / "fontes"  # cópias com SHA-256 em SOURCES.tsv (C09 e C10, v0.3)


def virgula(t: str) -> str:
    """Vírgula decimal só entre dígitos (PT-BR)."""
    return re.sub(r"(?<=\d)\.(?=\d)", ",", t)


def secao_md(rel: str, inicio: str, fim: str | None) -> str:
    """Linhas de tabela GFM entre dois títulos de um .md do repositório."""
    texto = (REPO / rel).read_text(encoding="utf-8")
    a = texto.index(inicio)
    b = texto.index(fim, a + len(inicio)) if fim else len(texto)
    linhas = [l for l in texto[a:b].splitlines() if l.startswith("|")]
    return virgula("\n".join(linhas))


def br(x: float, casas: int = 1) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def t_ggb() -> str:
    """Cobertura implícita do GGB, de dados/ggb/c08_numeradores.csv."""
    rows = list(csv.DictReader(open(REPO / "dados/ggb/c08_numeradores.csv", encoding="utf-8")))
    out = ["| desfecho | ano | prevalência | numerador | n | esperado (RR 1) | razão RR 1 | RR 2,82 | RR 3,84 | ano sem SIM (proxy) |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    nome = {"N0": "total declarado", "N1": "A: homicídio + latrocínio", "N2": "B: cenário de subtração (A sem pessoas trans)"}
    for r in rows:
        out.append(f"| {r['desfecho']} | {r['ano']} | {r['prevalencia']} | {nome[r['numerador']]} | {r['n']} | "
                   f"{br(float(r['E_RR1.0']))} | {br(100 * float(r['cob_RR1.0']))}% | {br(100 * float(r['cob_RR2.82']))}% | "
                   f"{br(100 * float(r['cob_RR3.84']))}% | {'sim' if r['proxy'] == 'True' else 'não'} |")
    return "\n".join(out)


def t_painel() -> str:
    """Painel TWFE e teste de falsificação, de dados/painel/c02_indet_resultados.csv."""
    rows = list(csv.DictReader(open(REPO / "dados/painel/c02_indet_resultados.csv", encoding="utf-8")))
    desf = {"registrado_ln": "log taxa registrada (X85-Y09)", "agressao_mais_indet_ln": "log taxa agressão + indeterminada",
            "razao_indet_pp": "parcela indeterminada (p.p. por ponto)"}
    out = ["| grupo | desfecho | b por ponto | IC95% | troca de 5 pontos (%) | p wild |", "|---|---|---|---|---|---|"]
    for r in rows:
        b, lo, hi = float(r["b"]), float(r["ic_lo"]), float(r["ic_hi"])
        if r["desfecho"] == "razao_indet_pp":
            troca = "n/a"
        else:
            troca = f"{br(100 * math.expm1(5 * lo))} a {br(100 * math.expm1(5 * hi))}"
        out.append(f"| {r['grupo'].replace('nao_negros', 'não negros')} | {desf[r['desfecho']]} | {br(b, 4)} | "
                   f"[{br(lo, 4)}; {br(hi, 4)}] | {troca} | {br(float(r['p_wild']), 2)} |")
    return "\n".join(out)


def t_eventos() -> str:
    """Estudo de eventos empilhado (painel BRC), de dados/painel/c03_event_pesos_resultados.csv."""
    rows = [r for r in csv.DictReader(open(REPO / "dados/painel/c03_event_pesos_resultados.csv", encoding="utf-8"))
            if r["painel"].startswith("BRC")]
    out = ["| desenho | direção | desfecho | eventos | clusters | média pós (%) [IC95%] | p antecipações | p pós |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        m, lo, hi = (100 * math.expm1(float(r[k])) for k in ("media_pos", "media_pos_lo", "media_pos_hi"))
        out.append(f"| {r['desenho']} | {r['direcao'].replace('->', ' -> ')} | {r['desfecho'].replace('tx_', '')} | "
                   f"{r['n_eventos']} | {r['G']} | {br(m)} [{br(lo)}; {br(hi)}] | {br(float(r['p_antecipacoes']), 3)} | "
                   f"{br(float(r['p_pos']), 3)} |")
    return "\n".join(out)


def t_pns_direta() -> str:
    """Parcela de LGB+ entre vítimas adultas de violência física, de dados/pns/c05_razao_direta.csv."""
    rows = list(csv.DictReader(open(REPO / "dados/pns/c05_razao_direta.csv", encoding="utf-8")))
    out = ["| base | corte | vítimas (n) | LGB+ (n) | % LGB+ | IC95% de desenho (Taylor) |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['base']} | {r['corte']} | {r['n_vit']} | {r['n_lgb']} | {br(float(r['R']), 2)} | "
                   f"[{br(float(r['lo']), 2)}; {br(float(r['hi']), 2)}] |")
    return "\n".join(out)


def pct(x: str, casas: int = 1) -> str:
    v = float(x)
    return ("+" if v > 0 else "") + br(v, casas)


def t_ggb_marginais() -> str:
    """Cenários de numerador do GGB pelas marginais publicadas, de dados/ggb/c08_cenarios_marginais.csv (v0.3, R4)."""
    rows = list(csv.DictReader(open(REPO / "dados/ggb/c08_cenarios_marginais.csv", encoding="utf-8")))
    out = ["| ano | cenário | n | esperado (RR 1) | razão RR 1 |", "|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['ano']} | {r['cenario']} | {r['n']} | {br(float(r['E_RR1']))} | {br(100 * float(r['cob_RR1']))}% |")
    return "\n".join(out)


def t_r6() -> str:
    """Intervalo do painel por três métodos, de dados/painel/r6_ic_wild_invertido.csv (v0.3, R6)."""
    rows = list(csv.DictReader(open(REPO / "dados/painel/r6_ic_wild_invertido.csv", encoding="utf-8")))
    out = ["| grupo | b (EP) | normal (%) | wild invertido (%) | t26 (%) | p(0) da grade | p wild publicado |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        f = lambda a, b: f"{br(float(r[a]))} a {pct(r[b])}"
        out.append(f"| {r['grupo'].replace('nao_negros', 'não negros')} | {br(float(r['b']), 5)} ({br(float(r['ep']), 5)}) | "
                   f"{f('pct5_normal_lo', 'pct5_normal_hi')} | {f('pct5_wild_inv_lo', 'pct5_wild_inv_hi')} | {f('pct5_t26_lo', 'pct5_t26_hi')} | "
                   f"{br(float(r['p0_grade']), 3)} | {br(float(r['p_wild_publicado']), 3)} |")
    return "\n".join(out)


def t_r7() -> str:
    """Parlamento, fonte nomeada e fonte primária nas duas codificações, de r7_parlamento_sensibilidade.csv (v0.3, R7)."""
    rows = list(csv.DictReader(open(REPO / "research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv", encoding="utf-8")))
    out = ["| variável | codificação das falas F2 | F2 | linha de base | mesmo codificador | p (Fisher) |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['variavel']} | {r['codificacao_F2']} | {r['a']}/{r['n1']} | {r['b']}/{r['n2']} | {r['mesmo_codificador']} | "
                   f"{br(float(r['p_fisher']), 4)} |")
    return "\n".join(out)


def t_c10_federal() -> str:
    """Exposição federal por governo e grupo, de paper/figures/fontes/c10_e1_federal.csv (v0.3, C10)."""
    rows = [r for r in csv.DictReader(open(FONTES / "c10_e1_federal.csv", encoding="utf-8")) if r["var_pct"]]
    out = ["| governo | grupo | desfecho | anos | taxa | variação % [intervalo de contagem] | 3 anos antes (%) |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        pre = pct(r["pre_var_pct"]) if r["pre_var_pct"] else "n/d"
        out.append(f"| {r['governo']} | {r['serie']} | {r['desfecho'].replace('agressao', 'agressão').replace('+indet', ' + indeterminada')} | "
                   f"{r['ano_base']} -> {r['ano_fim']} | {br(float(r['taxa_base']), 2)} -> {br(float(r['taxa_fim']), 2)} | "
                   f"{pct(r['var_pct'])} [{pct(r['var_pct_lo'])}; {pct(r['var_pct_hi'])}] | {pre} |")
    return "\n".join(out)


def t_c10_estadual() -> str:
    """Exposição estadual, 67 trocas, de paper/figures/fontes/c10_e2_resumo.csv (recorte principal; v0.3, C10)."""
    rows = [r for r in csv.DictReader(open(FONTES / "c10_e2_resumo.csv", encoding="utf-8")) if r["recorte"] == "P_todas_67"]
    out = ["| direção | grupo | trocas | subiu | caiu | mediana % [p25; p75] | referência 95% da mediana | p mediana | p Holm |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        holm = br(float(r["p_mediana_holm6"]), 3) if r["p_mediana_holm6"] else "n/a"
        out.append(f"| {r['direcao']} | {r['grupo'].replace('nao_negros', 'não negros').replace('total_agr_indet', 'total, agressão + indeterminada')} | "
                   f"{r['n']} | {r['n_subiu']} | {r['n_caiu']} | {pct(r['mediana_pct'])} [{pct(r['p25_pct'])}; {pct(r['p75_pct'])}] | "
                   f"{pct(r['ref_mediana_p2_5'])} a {pct(r['ref_mediana_p97_5'])} | {br(float(r['p_mediana']), 3)} | {holm} |")
    return "\n".join(out)


def t_c09_d2() -> str:
    """Troca de presidente, painel de alinhamento, de paper/figures/fontes/c09_d2_resultados.csv (v0.3, C09)."""
    rows = list(csv.DictReader(open(FONTES / "c09_d2_resultados.csv", encoding="utf-8")))
    out = ["| análise | grupo | desfecho | b [IC95%] | efeito no contraste [IC95%] | p wild | efeito mínimo detectável |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        u = " p.p." if r["escala"] == "pp" else "%"
        out.append(f"| {r['analise']} | {r['grupo'].replace('nao_negros', 'não negros')} | {r['desfecho']} | {br(float(r['b']), 5)} "
                   f"[{br(float(r['lo']), 5)}; {br(float(r['hi']), 5)}] | {pct(r['ef_lo'])}{u} a {pct(r['ef_hi'])}{u} | {br(float(r['p']), 3)} | "
                   f"{pct(r['mde_neg'])}{u} / {pct(r['mde_pos'])}{u} |")
    return "\n".join(out)


def t_c09_d1() -> str:
    """Troca de presidente, série nacional com placebo, de paper/figures/fontes/c09_d1_resultados.csv (v0.3, C09)."""
    rows = list(csv.DictReader(open(FONTES / "c09_d1_resultados.csv", encoding="utf-8")))
    out = ["| série | desfecho | troca | variação de nível [IC95%] | placebo (ano) [IC95%] | leitura pré-registrada |", "|---|---|---|---|---|---|"]
    for r in rows:
        u = " p.p." if r["desfecho"].endswith("_pp") else "%"
        out.append(f"| {r['serie']} | {r['desfecho']} | {r['quebra']} | {pct(r['pct'])}{u} [{pct(r['pct_lo'])}; {pct(r['pct_hi'])}] | "
                   f"{pct(r['placebo_pct'])}{u} ({r['placebo_quebra']}) [{pct(r['placebo_pct_lo'])}; {pct(r['placebo_pct_hi'])}] | {r['leitura']} |")
    return "\n".join(out)


TABELAS = [
    ("Violência em 12 meses por orientação sexual, adultos, PNS 2019", "dados/pns/seguro_pns2019.md",
     lambda: secao_md("dados/pns/seguro_pns2019.md", "## 1.", "## 2.")),
    ("Violência física em 12 meses, LGB+ e heterossexuais, por subgrupo", "dados/pns/seguro_pns2019.md",
     lambda: secao_md("dados/pns/seguro_pns2019.md", "## 2.", "## 3.")),
    ("Razão de prevalências ajustada por sexo, idade, cor, instrução, região e situação urbana ou rural", "dados/pns/seguro_pns2019.md",
     lambda: secao_md("dados/pns/seguro_pns2019.md", "## 3.", "## 4.")),
    ("Quem agrediu e onde, entre vítimas de violência física (nível de contexto, não letal)", "dados/pns/seguro_pns2019.md",
     lambda: secao_md("dados/pns/seguro_pns2019.md", "## 4.", None)),
    ("Parcela de LGB+ entre vítimas adultas de violência física, estimativa direta no microdado", "dados/pns/c05_razao_direta.csv", t_pns_direta),
    ("Razão entre a contagem do Grupo Gay da Bahia e as mortes esperadas, por ano, numerador, prevalência e risco suposto", "dados/ggb/c08_numeradores.csv", t_ggb),
    ("Numerador da contagem do Grupo Gay da Bahia: cenários compatíveis com as marginais publicadas", "dados/ggb/c08_cenarios_marginais.csv", t_ggb_marginais),
    ("Painel de governadores (efeitos fixos duplos) e teste de falsificação com a causa indeterminada", "dados/painel/c02_indet_resultados.csv", t_painel),
    ("Painel de governadores: troca de 5 pontos por três métodos de intervalo", "dados/painel/r6_ic_wild_invertido.csv", t_r6),
    ("Estudo de eventos empilhado, painel principal, quatro desfechos", "dados/painel/c03_event_pesos_resultados.csv", t_eventos),
    ("Exposição federal: taxa nacional padronizada por governo, por grupo e desfecho", "paper/figures/fontes/c10_e1_federal.csv", t_c10_federal),
    ("Exposição estadual: 67 trocas de governador, taxa do estado relativa ao Brasil, por direção e grupo", "paper/figures/fontes/c10_e2_resumo.csv", t_c10_estadual),
    ("Troca de presidente: série nacional, mudança de nível em cada troca e placebo", "paper/figures/fontes/c09_d1_resultados.csv", t_c09_d1),
    ("Troca de presidente: interação entre a ideologia do governador e a do presidente no painel", "paper/figures/fontes/c09_d2_resultados.csv", t_c09_d2),
    ("Taxa de óbito por agressão padronizada por idade, por ano, por 100 mil", "dados/sim/asr_brasil.md",
     lambda: secao_md("dados/sim/asr_brasil.md", "## 1.", "## 2.")),
    ("Razões padronizadas e alocação da raça ignorada, 2022-2024", "dados/sim/asr_brasil.md",
     lambda: secao_md("dados/sim/asr_brasil.md", "## 2.", "## 3.")),
    ("Amostra codificada de discurso: quem afirma, quem rebate e quem cita fonte", "docs/laudos/MIDIA.md",
     lambda: secao_md("docs/laudos/MIDIA.md", "## 4. Amostra codificada", "\"Cita GGB")),
    ("Parlamento: fonte nomeada e fonte primária nas duas regras de codificação, com teste exato de Fisher", "research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv", t_r7),
]
# A adjudicação da revisão adversarial (escrutinio/TRIAGEM.md) fica no repositório, não no artigo.

# v0.4.4 (E8, rodada v4-5 do juiz): frase extra na Nota de uma tabela, chave = título em TABELAS; só texto, nenhuma célula
NOTA_EXTRA = {
    "Violência física em 12 meses, LGB+ e heterossexuais, por subgrupo":
        "Negros são pretos e pardos (códigos 2 e 4 da variável C009, cor ou raça) e não negros são brancos, amarelos e "
        "indígenas (códigos 1, 3 e 5), pela regra de dados/pns/seguro_pns2019.py; 1 adulto LGB+ tem cor ou raça ignorada "
        "(código 9) e não entra em nenhuma das duas linhas, por isso 916 + 637 = 1.553 dos 1.554.",
    "Parcela de LGB+ entre vítimas adultas de violência física, estimativa direta no microdado":
        "A coluna % LGB+ é a razão de totais ponderados pelo peso do desenho amostral; as colunas de n são contagens da "
        "amostra, sem ponderação, e a razão entre elas não reproduz o percentual.",
}
assert set(NOTA_EXTRA) <= {t for t, _, _ in TABELAS}, "NOTA_EXTRA com título fora de TABELAS"


# rótulo de célula (texto inteiro da célula) -> rótulo em português comum; números nunca entram aqui
ROTULOS = {
    "agressao": "agressão",
    "agressao+indet": "agressão + indeterminada",
    "arma": "arma de fogo",
    "razao_indet_pp": "parcela de indeterminadas (p.p.)",
    "registrado_ln": "log da taxa registrada",
    "agressao_mais_indet_ln": "log da taxa de agressão + indeterminada",
    "primaria": "principal",
    "S1_distancia": "S1: distância ideológica",
    "S2_grupos": "S2: por grupo",
    "S3_agr_indet": "S3: agressão + indeterminada",
    "S3_razao_indet": "S3: parcela de indeterminadas",
    "S4_escore_unico": "S4: escore único de ideologia",
    "S5_sem_2016": "S5: sem o ano de 2016",
    "S6_BLS9": "S6: outra escala de ideologia (Zucco e Power)",
    "S7_copartidarismo": "S7: mesmo partido do presidente",
    "**QUEM (V018)**": "Quem agrediu (V018)",
    "**ONDE (V019)**": "Onde (V019)",
    "N1 homicídio + latrocínio (inclui trans e heterossexuais)": "A: homicídio + latrocínio (inclui pessoas trans e heterossexuais)",
    "N2 cenário: N1 menos TODAS as trans da tabela (publicado)": "B: cenário de subtração (A menos todas as pessoas trans da tabela publicada)",
    "cis LGB dentro de N1: mínimo compatível com as marginais": "cis LGB dentro de A: mínimo compatível com as marginais",
    "cis LGB dentro de N1: máximo compatível com as marginais": "cis LGB dentro de A: máximo compatível com as marginais",
    "contraexemplo do Astra: 269 - 99 trans (102 - 3 suicidas) - 6 heterossexuais":
        "contraexemplo: 269 - 99 trans (102 - 3 suicidas) - 6 heterossexuais",
    "segundo codificador (Grok)": "segundo codificador (modelo de outra família)",
    "original, regra literal do codebook (nome + ano)": "original, regra literal do livro de códigos (nome + ano)",
    "fam": "família",
    "clusters": "grupos (estados)",
    "p wild publicado": "p wild (bootstrap)",
    "esquerda -> direita": "esquerda para direita",
    "direita -> esquerda": "direita para esquerda",
    "bloco: esquerda->direita": "bloco: esquerda para direita",
    "bloco: direita->esquerda": "bloco: direita para esquerda",
    # E5 (v0.4.1, A2-02 da S2): o recorte (b) repete o recorte de orientação do Sinan; não é a mesma grandeza
    "(b) só hetero ou LGB+ (comparável ao Sinan)": "(b) só heterossexuais ou LGB+ (mesmo recorte de orientação do Sinan)",
}


def celulas(linha: str) -> list[str]:
    """Células de uma linha de tabela GFM."""
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def _separador(linha: str) -> bool:
    return not linha.startswith("|") or set(linha.replace("|", "").strip()) <= set("-: ")


def traduz_linha(linha: str) -> str:
    """Troca só rótulos (mapa ROTULOS) e a seta entre anos ou números ("2010 -> 2015" vira "2010 a 2015")."""
    if _separador(linha):
        return linha
    cs = [ROTULOS.get(c, c) for c in celulas(linha)]
    cs = [re.sub(r"^(\d{4}) -> (\d{4})$", r"\1 a \2", c) for c in cs]
    cs = [re.sub(r"^([\d,]+) -> ([\d,]+)$", r"\1 a \2", c) for c in cs]
    return "| " + " | ".join(cs) + " |"


def bloco() -> str:
    """Bloco do Apêndice A em APA 7: Tabela A1..An, título em itálico, tabela, Nota com o arquivo de origem."""
    partes = [INI, ""]
    for i, (titulo, fonte, fn) in enumerate(TABELAS):
        linhas = "\n".join(traduz_linha(ln) for ln in fn().splitlines())
        extra = f"{NOTA_EXTRA[titulo]} " if titulo in NOTA_EXTRA else ""
        partes += [f"**Tabela A{i + 1}**", "", f"*{titulo}*", "", linhas, "",
                   f"*Nota.* Valores copiados sem alteração do arquivo {fonte} do repositório, com vírgula decimal. "
                   f"{extra}Fonte: Flores (2026).", ""]
    partes.append(FIM)
    return "\n".join(partes)


def provar() -> int:
    """Célula a célula: igual ao arquivo de origem, ou trocada só pelo mapa de rótulos (seta entre anos vira 'a')."""
    falhas = 0
    for _titulo, fonte, fn in TABELAS:
        for ln in fn().splitlines():
            if _separador(ln):
                continue
            a, b = celulas(ln), celulas(traduz_linha(ln))
            if len(a) != len(b):
                falhas += 1
                print("[FAIL] número de células", fonte, ln)
                continue
            for x, y in zip(a, b):
                if not (x == y or ROTULOS.get(x) == y or re.sub(r" -> ", " a ", x) == y):
                    falhas += 1
                    print("[FAIL]", fonte, repr(x), "->", repr(y))
    print("[PASS] só rótulos e setas mudaram; nenhum número" if falhas == 0 else f"[FAIL] {falhas} células")
    return 1 if falhas else 0


def main() -> int:
    if "--provar" in sys.argv:
        return provar()
    novo = bloco()
    if "--escrever" in sys.argv or "--conferir" in sys.argv:
        texto = PAPER.read_text(encoding="utf-8")
        a, b = texto.index(INI), texto.index(FIM) + len(FIM)
        if "--conferir" in sys.argv:
            ok = texto[a:b] == novo
            print("[PASS] Apêndice A idêntico ao gerado dos arquivos do repositório" if ok else "[FAIL] Apêndice A diverge do gerado")
            return 0 if ok else 1
        PAPER.write_text(texto[:a] + novo + texto[b:], encoding="utf-8")
        print(f"[OK] Apêndice A gravado ({len(TABELAS)} tabelas)")
        return 0
    print(novo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
