#!/usr/bin/env python3
"""build_dashboard.py -- gera TODO o material do dashboard do artigo LGBT-INDICADOR.

FERRAMENTA DO AUTOR, NÃO REPRODUZÍVEL A PARTIR DESTE REPOSITÓRIO: conta arquivos da árvore completa do projeto de origem
(inclusive fontes/ com PDFs e microdados que não são distribuídos) e lê os rótulos (labels.<locale>.json), os textos do
artigo (index.<locale>.mdx, na pasta-mãe da saída) e os tipos do site em que o painel foi publicado. Está aqui para auditoria da lógica de contagem; os números que ela gerou estão em
dashboard/dashboard_dados.publico.json e dashboard/KPIS-FINAIS.md.

Rodar:  LGBT_PROJETO=<raiz do projeto de origem> DASHBOARD_OUT=<pasta de saída> [SITE_TIPOS=<artigos-charts.ts> SITE_TSC=<tsc>] python3 -I build_dashboard.py

Saidas (mesma pasta): dashboard_dados.json, lgbt-violencia.data.ts, DASHBOARD-SPEC.md, SHA256SUMS.txt.
Regra: todo numero exibido e CONTADO aqui, a partir de arquivos reais do projeto; nenhum numero e digitado
a mao. Sem aleatoriedade (SEED fixo so documenta isso). P8 le a base (k pontos) e os limites exatos da reanalise C03 em dados/painel/.
Somente leitura nas fontes; so escreve na pasta do dashboard. Sem rede.
"""
import csv
import datetime as dt
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

SEED = 20261023  # sem uso: nao ha amostragem aleatoria; ordenacao sempre deterministica
PROJ = os.environ.get("LGBT_PROJETO") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("DASHBOARD_OUT") or os.path.dirname(os.path.abspath(__file__))
SITE_TIPOS = os.environ.get("SITE_TIPOS", "")  # tipos TypeScript do site (opcional)
PY = sys.executable
NODE = os.environ.get("NODE_BIN", "node")

DATA_INI = dt.date(2026, 10, 10)  # início do projeto (primeira pergunta de pesquisa, 2026-10-10)
DATA_FIM = dt.date(2026, 10, 23)  # dia da publicacao do artigo

# paleta do site (cabecalho de data/artigos-charts.ts): so estes hex
OURO, AZUL, AMBAR, CINZA, CINZA_ESC, CINZA_CLARO = "#a48f65", "#60a5fa", "#fbbf24", "#64748b", "#3f3f46", "#d4d4d8"
PALETA = {OURO, AZUL, AMBAR, CINZA, CINZA_ESC, CINZA_CLARO}

ENTRADAS = set()  # arquivos lidos (vao para o SHA256SUMS)
NUM = {}  # chave -> {valor, origem}


def P(*parts):
    return os.path.join(PROJ, *parts)


def ler(path):
    ENTRADAS.add(path)
    return open(path, encoding="utf-8")


COMANDOS = {  # equivalentes de shell para as contagens simples (as demais: o script, funcao calcular())
    "scripts": f"find {PROJ} -name '*.py' -not -path '*/__pycache__/*' -not -path '{PROJ}/fontes/*' | wc -l",
    "revisores": f"ls {PROJ}/research-2026-10-21-rodada3/escrutinio/revisao_*.md | wc -l",
    "ledgers": f"find {PROJ} -name sources.jsonl | wc -l",
    "registros_brutos": f"find {PROJ} -name sources.jsonl -exec cat {{}} + | grep -c .",
    "dias": "python3 -c \"import datetime as d; print((d.date(2026,10,23)-d.date(2026,10,10)).days+1)\"",
    "pdfs": f"find {PROJ}/fontes -iname '*.pdf' -not -path '{PROJ}/fontes/q1-textointegral/discurso/*' -exec shasum -a 256 {{}} + | cut -d' ' -f1 | sort -u | wc -l",
}


def reg(chave, valor, arquivos, como):
    cmd = COMANDOS.get(chave, f"{PY} -I {OUT}/build_dashboard.py  # funcao calcular(), chave '{chave}'")
    NUM[chave] = {"valor": valor, "origem": {"arquivos": [a.replace(PROJ + "/", "") if a.startswith(PROJ) else a for a in arquivos], "como": como, "comando": cmd}}
    return valor


# ------------------------------------------------------------------ formatacao pt-br (espelha Intl pt-BR do .ts)
def fmt_pt(v, d=0, sinal=False):
    if isinstance(v, str):
        return v
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    neg = round(v, d) < 0
    if neg:
        return "-" + s
    return ("+" + s) if (sinal and round(v, d) != 0) else s


MESES_PT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def dia_pt(p):
    """espelha dia() do .ts em pt-BR: fim = '23 de outubro de 2026'; inicio = '10' (mesmo mes e ano) ou '10 de outubro'."""
    ini, fim = dt.date.fromisoformat(p["ini"]), dt.date.fromisoformat(p["fim"])
    if p["papel"] == "fim":
        return f"{fim.day} de {MESES_PT[fim.month - 1]} de {fim.year}"
    if (ini.year, ini.month) == (fim.year, fim.month):
        return str(ini.day)
    return f"{ini.day} de {MESES_PT[ini.month - 1]}"


def par_data(papel):
    return {"ini": DATA_INI.isoformat(), "fim": DATA_FIM.isoformat(), "papel": papel}


def param_pt(p):
    if isinstance(p, dict):
        return dia_pt(p)
    if isinstance(p, (list, tuple)):
        return fmt_pt(p[0], p[1], len(p) > 2)
    if isinstance(p, str):
        return p
    return fmt_pt(p, 0)


# ================================================================== 1. LEDGERS
def carregar_ledgers():
    arqs = sorted(glob.glob(P("**", "sources.jsonl"), recursive=True))
    regs = []
    for f in arqs:
        with ler(f) as fh:
            for ln in fh:
                if ln.strip():
                    r = json.loads(ln)
                    r["_f"] = os.path.relpath(f, PROJ)
                    regs.append(r)
    return arqs, regs


def chave_id(r):
    i = r["id"].strip()
    if r["id_kind"] == "doi":
        return "doi:" + i.lower()
    m = re.search(r"doi\.org/(10\.\d{4,9}/\S+)", i, re.I)
    if m:
        return "doi:" + m.group(1).lower()
    return r["id_kind"] + ":" + i.rstrip("/").lower()


def lang_norm(x):
    return "pt" if x in ("pt", "pt-BR") else x


def ano_int(a):
    try:
        return int(str(a).strip())
    except (ValueError, TypeError):
        return None


LANG_ORDEM_PREF = "research-consolidado/sources.jsonl"


def agrupar(regs):
    g = defaultdict(list)
    for r in regs:
        g[chave_id(r)].append(r)
    return g


def idioma_do_id(recs):
    """maioria entre os registros (pt e pt-BR fundidos); empate -> registro do research-consolidado, senao o 1o."""
    c = Counter(lang_norm(r["idioma"]) for r in recs)
    top = max(c.values())
    cand = sorted(k for k, v in c.items() if v == top)
    if len(cand) == 1:
        return cand[0], len(c) > 1, False
    pref = [lang_norm(r["idioma"]) for r in recs if r["_f"] == LANG_ORDEM_PREF and lang_norm(r["idioma"]) in cand]
    return (pref[0] if pref else lang_norm(recs[0]["idioma"])), True, True


# ---- tipo de fonte (P2). Regras EXPLICITAS; o ledger nao tem campo de tipo.
CANAIS_PERIODICO = {"crossref", "pubmed", "openalex", "scielo", "europepmc", "literatura", "doi", "unpaywall", "lilacs", "dialnet", "academico", "econstor"}
CANAIS_OFICIAL = {"fonte-oficial", "governo", "ibge", "oficial", "planalto", "gov-br", "governo-estadual", "legislacao-estadual", "ipea-repositorio",
                  "moj-japan", "nz-justice", "find-a-tender", "onu-ods", "stats-sa", "uganda-police", "gambling-commission", "omb", "bjs",
                  "open-canada", "contracts-finder", "bcb", "ons", "cnj", "fiocruz", "nap-edu", "worldbank", "ufrgs-cep", "unodc", "ministerio-da-justica",
                  "nhrck-korea", "mogef-korea", "kemenpppa-unfpa", "south-africa-gazette", "hcwg-south-africa", "khrc-kenya"}
CANAIS_DADO = {"dhs-program", "dataverse", "v-dem", "sidra", "ibge-sidra", "ibge-ftp", "datasus", "ted-api", "lapop"}
CANAIS_ONG = {"ong", "ilga-world", "ilga-database"}
# hosts: igual ao dominio ou subdominio dele (ver host_em)
HOSTS_ONG = ("grupogaydabahia.com.br", "antrabrasil.org", "ilga.org", "tgeu.net", "translivesmatter.info", "abglt.org", "homofobiamata.files.wordpress.com",
             "amnesty.org", "hrw.org", "aaiusa.org", "apoyovictimas.cl", "cnafal.org", "frauen-gegen-gewalt.de", "cilip.de")
HOSTS_IMPRENSA = ("congressoemfoco.com.br", "opovo.com.br", "poder360.com.br", "folha.uol.com.br", "globo.com", "bbc.com", "theguardian.com", "lex.com.br",
                  "noticias-do-brasil.news", "cartacapital.com.br", "uol.com.br", "gazetadopovo.com.br", "nexojornal.com.br", "bahianoticias.com.br",
                  "bnews.com.br", "viva.com.br", "legaltoday.com", "brightspotcdn.com", "chequeado.com", "franceinfo.fr")
HOSTS_DADO = ("dhsprogram.com", "tabnet.datasus.gov.br", "apisidra.ibge.gov.br", "ftp.ibge.gov.br", "datos.csjn.gob.ar", "cde.ucr.cjis.gov", "githubusercontent.com",
              "github.com", "dataverse.harvard.edu", "zenodo.org")
HOSTS_OFICIAL = ("forumseguranca.org.br", "poderjudicial.es", "fiscal.es", "inegi.org.mx", "snieg.mx", "istat.it", "bka.de", "polizei.nrw", "osce.org", "unwomen.org", "unodc.org",
                 "who.int", "europa.eu", "un.org", "cepal.org", "vie-publique.fr", "senat.fr", "assemblee-nationale.fr", "bra.se", "bpb.de",
                 "centre-hubertine-auclert.fr", "everycrsreport.com")
LABELS_GOV = {"gov", "gob", "gouv", "govt", "gub", "leg", "jus", "go", "gc", "mp", "mil"}
HOSTS_ACAD = ("arca.fiocruz.br", "ri.ufs.br", "sites.usp.br", "scholarlycommons.law.northwestern.edu", "uni-tuebingen.de", "docs.iza.org", "even3.com")
HOSTS_PERIODICO = ("scielo.br", "aeaweb.org")
HOSTS_ENCICLOPEDIA = ("wikipedia.org",)


def host_em(host, lista):
    return any(host == h or host.endswith("." + h) for h in lista)


PREF_DADO = ("10.7910/",)  # Dataverse
PREF_PREPRINT = ("10.2139/", "10.3386/", "10.21203/", "10.31235/", "10.48550/", "10.1101/", "10.5281/", "10.31219/", "10.17605/")  # SSRN, NBER, ResearchSquare, SocArXiv, arXiv, bio/medRxiv, Zenodo, OSF
TIPOS = ["per_q1", "per_q2", "per_q34", "per_semq", "oficial", "preprint", "ong", "imprensa", "dado", "livro", "enciclopedia", "nao_classificado"]


def tipo_um(r, quartil):
    idk, canal, host = r["id_kind"], r["canal"], urlparse(r.get("url") or "").netloc.lower().replace("www.", "")
    chave = chave_id(r)
    if idk == "isbn" or chave.startswith("doi:10.2307/jj."):
        return "livro"
    if idk in ("doi", "pmid") or chave.startswith("doi:"):
        d = chave[4:] if chave.startswith("doi:") else ""
        if r.get("acesso") == "preprint" or d.startswith(PREF_PREPRINT):
            return "preprint"
        if d.startswith(PREF_DADO) or canal in CANAIS_DADO:
            return "dado"
        if canal in CANAIS_PERIODICO or canal == "web":
            q = quartil.get(d) if d else quartil.get("pmid:" + r["id"].strip())
            return {"Q1": "per_q1", "Q2": "per_q2", "Q3": "per_q34", "Q4": "per_q34"}.get(q, "per_semq")
        return "nao_classificado"
    # id_kind url/other
    rotulos = set(host.split("."))
    if host_em(host, HOSTS_ENCICLOPEDIA):
        return "enciclopedia"
    if canal in CANAIS_ONG or host_em(host, HOSTS_ONG):
        return "ong"
    if canal == "imprensa" or host_em(host, HOSTS_IMPRENSA):
        return "imprensa"
    if canal in CANAIS_DADO or host_em(host, HOSTS_DADO):
        return "dado"
    if canal in CANAIS_OFICIAL or host_em(host, HOSTS_OFICIAL) or (rotulos & LABELS_GOV):
        return "oficial"
    if host_em(host, HOSTS_ACAD) or host.startswith("repositorio.") or host.startswith("ri."):
        return "preprint"
    if host_em(host, HOSTS_PERIODICO) or host.startswith("revistas."):
        return "per_semq"
    if canal in ("pubmed", "scielo", "lilacs", "dialnet", "crossref", "openalex", "europepmc"):
        return "per_semq"
    return "nao_classificado"


def tipo_do_id(recs, quartil):
    ts = [tipo_um(r, quartil) for r in sorted(recs, key=lambda x: (x["_f"] != LANG_ORDEM_PREF, x["_f"]))]
    for t in ts:
        if t != "nao_classificado":
            return t
    return "nao_classificado"


# ---- quartis: verificacao-*.csv (coluna quartil_sjr) + tabelas de referencia dos dossies (DOI | Qn)
def carregar_quartis():
    q = {}
    base = P("research-2026-10-21-rodada3", "A-textointegral")
    for f in sorted(glob.glob(os.path.join(base, "verificacao-*.csv"))):
        with ler(f) as fh:
            for r in csv.DictReader(fh):
                m = re.match(r"\s*Q([1-4])", r.get("quartil_sjr", ""))
                if m:
                    q.setdefault(r["doi"].strip().lower(), "Q" + m.group(1))
    fonte_csv = len(q)
    for f in ("DOSSIE-CONSOLIDADO-2026-10-12.md", "DOSSIE-2026-10-11-parte2.md", "DOSSIE-2026-10-10.md"):
        with ler(P(f)) as fh:
            for ln in fh:
                for m in re.finditer(r"\|\s*(10\.\d{4,9}/[^\s|]+)\s*\|\s*(Q[1-4])", ln):
                    q.setdefault(m.group(1).lower(), m.group(2))
    return q, fonte_csv


def faixa_ano(a):
    if a is None:
        return "sem_ano"
    for (lo, hi), nome in zip(FAIXA_LIM, FAIXAS[:-1]):
        if (lo is None or a >= lo) and (hi is None or a <= hi):
            return nome


# ================================================================== 2. VERIFICACAO DE TEXTO INTEGRAL (P3)
def doi_canon(d):
    """a verificacao as vezes trunca o sufixo '>3.0.co;2-4' de DOIs SICI; compara sem ele."""
    return re.sub(r">.*$", "", d.strip().lower())


def verificacao_texto_integral():
    base = P("research-2026-10-21-rodada3", "A-textointegral")
    arqs = sorted(glob.glob(os.path.join(base, "verificacao-*.csv"))) + sorted(glob.glob(os.path.join(base, "entregues", "verificacao-G*.csv")))
    por = defaultdict(list)
    n_linhas = 0
    for f in arqs:
        with ler(f) as fh:
            for r in csv.DictReader(fh):
                r["doi"] = doi_canon(r["doi"])
                por[r["doi"]].append(r)
                n_linhas += 1
    with ler(os.path.join(base, "DOIS-CITADOS.json")) as fh:
        citados = {doi_canon(d["doi"]) for d in json.load(fh)}
    lido = {d for d, v in por.items() if any(x["veredito"] != "SEM_TEXTO_INTEGRAL" for x in v)}
    usado = {d for d, v in por.items() if any(x["veredito"] in ("CONFIRMADO", "CONFIRMADO_COM_RESSALVA", "CONTRADITO") for x in v)}
    quart_csv = {}
    for d, v in por.items():
        for x in v:
            m = re.match(r"\s*Q([1-4])", x.get("quartil_sjr", ""))
            if m:
                quart_csv.setdefault(d, "Q" + m.group(1))
    return {"por": por, "arquivos": [os.path.relpath(a, PROJ) for a in arqs], "linhas": n_linhas, "dois": set(por), "citados": citados, "lido": lido,
            "usado": usado, "quart": quart_csv, "vereditos": Counter(x["veredito"] for v in por.values() for x in v)}


def conferir_dossie(g, tipo_por_id):
    """Cada DOI/URL das secoes 5.1 (periodico), 5.2 (oficial) e 5.3 (ONG) do DOSSIE-CONSOLIDADO tem de cair na classe que o dossie lhe da."""
    with ler(P("DOSSIE-CONSOLIDADO-2026-10-12.md")) as fh:
        txt = fh.read()
    a, b = txt.index("#### 5.1 Peer-reviewed"), txt.index("### 6. O que NÃO foi encontrado")
    secoes = {"5.1": ({"per_q1", "per_q2", "per_q34", "per_semq"}, txt[a:txt.index("#### 5.2 Fontes oficiais")]),
              "5.2": ({"oficial"}, txt[txt.index("#### 5.2 Fontes oficiais"):txt.index("#### 5.3 Sociedade civil")]),
              "5.3": ({"ong"}, txt[txt.index("#### 5.3 Sociedade civil"):b])}
    res = {"conferidos": 0, "sem_linha_no_registro": 0, "divergencias": []}
    for sec, (ok, trecho) in secoes.items():
        itens = [("doi:" + d.rstrip(".,;)>").lower()) for d in re.findall(r"10\.\d{4,9}/[^\s|)>,;]+", trecho)]
        itens += [("url:" + u.rstrip(".,;)>/").lower()) for u in re.findall(r"https?://[^\s|)>`]+", trecho)]
        for k in itens:
            if k not in g:
                res["sem_linha_no_registro"] += 1
                continue
            res["conferidos"] += 1
            if tipo_por_id[k] not in ok:
                res["divergencias"].append([sec, k[:90], tipo_por_id[k]])
    return res


# ================================================================== 3. KPIs de arquivos
def contar_scripts():
    achados = []
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        rel = os.path.relpath(root, PROJ)
        if rel == "fontes" or rel.startswith("fontes" + os.sep):
            continue  # material baixado, nao codigo do projeto
        for f in files:
            if f.endswith(".py"):
                achados.append(os.path.join(rel, f))
    return sorted(achados)


def contar_pdfs():
    hashes = set()
    n = 0
    for root, dirs, files in os.walk(P("fontes")):
        rel = os.path.relpath(root, P("fontes"))
        if rel.startswith(os.path.join("q1-textointegral", "discurso")):
            continue
        for f in files:
            if f.lower().endswith(".pdf"):
                n += 1
                h = hashlib.sha256()
                with open(os.path.join(root, f), "rb") as fh:
                    for bloco in iter(lambda: fh.read(1 << 20), b""):
                        h.update(bloco)
                hashes.add(h.hexdigest())
    return n, len(hashes)


def contar_analises():
    achados = []
    for f in sorted(glob.glob(P("**", "*.md"), recursive=True)):
        rel = os.path.relpath(f, PROJ)
        if rel.startswith("fontes" + os.sep):
            continue
        with ler(f) as fh:
            cab = fh.read(4000)
        if re.search(r"gerado por [A-Za-z0-9_./-]+\.py", cab, re.I):
            achados.append(rel)
    return achados


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


# ================================================================== 4. CALCULO
def calcular():
    out = {}
    # ---------- ledgers
    arqs, regs = carregar_ledgers()
    g = agrupar(regs)
    n_regs, n_unicos = len(regs), len(g)
    ts_min = min(r["ts"] for r in regs)[:10]
    ts_max = max(r["ts"] for r in regs)[:10]
    assert ts_min >= DATA_INI.isoformat() and ts_max <= DATA_FIM.isoformat(), (ts_min, ts_max)
    reg("fontes_unicas", n_unicos, arqs, "ids unicos: doi em minusculas; URL sem barra final e em minusculas; URL doi.org dobrada em doi; 17 sources.jsonl")
    reg("registros_brutos", n_regs, arqs, "linhas nao vazias dos 17 sources.jsonl (inclui repeticoes entre ledgers)")
    reg("ledgers", len(arqs), arqs, "glob **/sources.jsonl")
    reg("ledger_ts_min", ts_min, arqs, "menor campo ts")
    reg("ledger_ts_max", ts_max, arqs, "maior campo ts")
    # ---------- idiomas
    lang_por_id, n_conf, n_emp = {}, 0, 0
    for k, recs in g.items():
        l, conf, emp = idioma_do_id(recs)
        lang_por_id[k] = l
        n_conf += conf
        n_emp += emp
    c_lang = Counter(lang_por_id.values())
    reg("idiomas", len(c_lang), arqs, "codigos distintos do campo idioma (pt e pt-BR fundidos), por id unico")
    reg("idiomas_ids_com_conflito", n_conf, arqs, "ids cujo campo idioma difere entre registros mesmo apos fundir pt/pt-BR")
    reg("idiomas_empate_desfeito_pelo_consolidado", n_emp, arqs, "empates na maioria, desfeitos pelo registro do research-consolidado")
    out["idiomas"] = sorted(c_lang.items(), key=lambda kv: (-kv[1], kv[0]))
    # ---------- tipo / ano
    quartil, n_quart_csv = carregar_quartis()
    tipo_por_id = {k: tipo_do_id(recs, quartil) for k, recs in g.items()}
    c_tipo = Counter(tipo_por_id.values())
    ano_por_id = {}
    for k, recs in g.items():
        anos = [a for a in (ano_int(r.get("ano")) for r in recs) if a is not None]
        ano_por_id[k] = Counter(anos).most_common(1)[0][0] if anos else None
    c_faixa = Counter(faixa_ano(a) for a in ano_por_id.values())
    assert sum(c_tipo.values()) == n_unicos == sum(c_faixa.values())
    out["tipos"] = {t: c_tipo.get(t, 0) for t in TIPOS}
    out["faixas"] = {f: c_faixa.get(f, 0) for f in ["ate2009", "2010_14", "2015_19", "2020_24", "2025_26", "sem_ano"]}
    reg("tipos", out["tipos"], arqs + [P("DOSSIE-CONSOLIDADO-2026-10-12.md")], "classificar() por canal + id_kind + prefixo de DOI + host; quartil de verificacao-*.csv e tabelas dos dossies")
    reg("faixas_ano", out["faixas"], arqs, "campo ano (moda entre registros do id)")
    out["periodicos_com_doi_pmid"] = sum(c_tipo[t] for t in ("per_q1", "per_q2", "per_q34", "per_semq"))
    out["quartil_n_fontes"] = {"csv": n_quart_csv, "total_dois_com_quartil": len(quartil)}
    # ---------- P3 funil
    v = verificacao_texto_integral()
    chaves_doi = {doi_canon(k[4:]) for k in g if k.startswith("doi:")}
    lido_reg = v["lido"] & chaves_doi
    q1_lido = {d for d in lido_reg if (v["quart"].get(d) or quartil.get(d)) == "Q1"}
    usado_q1 = q1_lido & v["usado"]
    v_por = v["por"]
    so_contradito = {d for d in usado_q1 if {x["veredito"] for x in v_por[d] if x["veredito"] in ("CONFIRMADO", "CONFIRMADO_COM_RESSALVA", "CONTRADITO")} == {"CONTRADITO"}}
    out["funil_q1_so_contradito"] = len(so_contradito)
    out["funil"] = {"registradas": n_unicos, "lido": len(lido_reg), "q1_lido": len(q1_lido), "q1_usado": len(usado_q1)}
    assert n_unicos >= len(lido_reg) >= len(q1_lido) >= len(usado_q1)
    out["verif"] = {"dois_verificados": len(v["dois"]), "dois_no_ledger": len(v["dois"] & chaves_doi), "citados_dossie": len(v["citados"]),
                    "citados_no_ledger": len(v["citados"] & chaves_doi), "lido_nao_registrado": len(v["lido"] - chaves_doi), "linhas": v["linhas"],
                    "vereditos": dict(v["vereditos"]), "verificados_fora_dos_citados": len(v["dois"] - v["citados"])}
    reg("funil", out["funil"], v["arquivos"] + [P("research-2026-10-21-rodada3/A-textointegral/DOIS-CITADOS.json")],
        "por DOI: lido = algum veredito != SEM_TEXTO_INTEGRAL; Q1 = quartil_sjr começa em Q1 (ou tabela dos dossies); usado = veredito CONFIRMADO/CONFIRMADO_COM_RESSALVA/CONTRADITO; tudo interseccionado com os DOIs do ledger")
    reg("afirmacoes_verificadas_linhas", v["linhas"], v["arquivos"], "linhas dos 9 CSVs de verificacao (uma por afirmacao do dossie x DOI)")
    out["conf_dossie"] = conferir_dossie(g, tipo_por_id)
    assert not out["conf_dossie"]["divergencias"], out["conf_dossie"]["divergencias"]
    reg("conferencia_tipo_dossie", out["conf_dossie"], [P("DOSSIE-CONSOLIDADO-2026-10-12.md")], "DOIs/URLs das secoes 5.1, 5.2 e 5.3 do dossie consolidado: a classe do script tem de coincidir com a do dossie")
    # ---------- P4 PNS
    pns = {}
    with ler(P("dados/pns/seguro_pns2019.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["bloco"] == "nivel":
                pns[r["rotulo"]] = {k: float(r[k]) for k in ("prev_grupo", "prev_ref", "rp", "ic_lo", "ic_hi")}
    out["pns"] = {k: pns[k] for k in ("física", "sexual", "qualquer")}
    reg("pns_2019", out["pns"], [P("dados/pns/seguro_pns2019.csv")], "linhas bloco=nivel, grupo LGB+ (prev_grupo, prev_ref=heterossexual, rp, ic)")
    # ---------- P5 GGB: numeradores N0/N1/N2 (c08_numeradores.csv), conferidos contra cobertura_implicita.csv e RESULTADOS.md da reanalise
    antigo = {}
    with ler(P("dados/ggb/cobertura_implicita.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["desfecho"] == "agressao" and r["medida_GGB"] == "todas" and r["prevalencia_LGB"].startswith("1,89%"):
                antigo[(int(r["ano"]), r["RR_cenario"])] = (int(r["ggb"]), float(r["mortes_esperadas"]))
    c08 = {}
    prev_txt = None
    with ler(P("dados/ggb/c08_numeradores.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["desfecho"] == "agressao" and r["prevalencia"] == "1,89%" and r["proxy"] == "False":
                c08[(int(r["ano"]), r["numerador"])] = r
                prev_txt = r["prevalencia"]
    out["ggb_prev"] = float(prev_txt.split("%")[0].replace(",", "."))
    out["ggb"] = {}
    RRS = ("1.0", "2.82", "3.84")
    for ano in sorted({a for a, _ in c08}):
        num = {}
        for nm in ("N0", "N1", "N2"):
            r = c08[(ano, nm)]
            num[nm] = {"n": int(r["n"]), "cob": [float(r["cob_RR1.0"]), float(r["cob_RR2.82"]), float(r["cob_RR3.84"])]}
        esp = {rr: float(c08[(ano, "N0")]["E_RR" + rr]) for rr in RRS}
        for rr in RRS:  # N0 e E do c08 == cobertura_implicita.csv (script antigo)
            assert num["N0"]["n"] == antigo[(ano, rr)][0] and abs(esp[rr] - antigo[(ano, rr)][1]) < 0.06, (ano, rr)
        for nm in num:  # cobertura do CSV == n/esperado
            for j, rr in enumerate(RRS):
                assert abs(num[nm]["n"] / esp[rr] - num[nm]["cob"][j]) < 0.0006
        out["ggb"][ano] = {"num": num, "esperado": esp}
    assert sorted(out["ggb"]) == [2023, 2024]
    # conferencia com a frase da reanalise (RESULTADOS.md, C08): N0 22,9/28,7; N1 19,7/26,6; N2 8,4/16,5 (RR 1); RR 2,82/3,84 no maximo 10,2
    esperado_c08 = {(2023, "N0"): 22.9, (2024, "N0"): 28.7, (2023, "N1"): 19.7, (2024, "N1"): 26.6, (2023, "N2"): 8.4, (2024, "N2"): 16.5}
    for (a_, nm_), v_ in esperado_c08.items():
        assert round(100 * out["ggb"][a_]["num"][nm_]["cob"][0], 1) == v_, (a_, nm_)
    out["ggb_max_rr_alto"] = max(100 * x["cob"][j] for d_ in out["ggb"].values() for x in d_["num"].values() for j in (1, 2))
    assert round(out["ggb_max_rr_alto"], 1) == 10.2, out["ggb_max_rr_alto"]
    with ler(P("dados/pns/seguro_pns2019.csv")) as fh:
        adj = next(float(r["rp"]) for r in csv.DictReader(fh) if r["bloco"] == "rp_ajustada" and r["rotulo"] == "física")
    assert round(adj, 2) == 2.82 and round(pns["física"]["rp"], 2) == 3.84, (adj, pns["física"]["rp"])  # os RR do GGB sao as RP fisicas da PNS (ajustada e bruta)
    reg("ggb_cobertura", {str(k): v_ for k, v_ in out["ggb"].items()}, [P("dados/ggb/c08_numeradores.csv"), P("dados/ggb/cobertura_implicita.csv")],
        "desfecho=agressao, prevalencia 1,89%, numeradores N0/N1/N2, 2023 e 2024 (2025 e proxy, fora); RR 1,0 / 2,82 / 3,84")
    # ---------- P6 SIM
    sim = defaultdict(dict)
    with ler(P("dados/sim/asr_brasil.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["desfecho"] == "agressao" and r["ano"] in ("2022", "2023", "2024"):
                sim[r["grupo"]][int(r["ano"])] = float(r["taxa_padronizada"])
    out["sim_anos"] = sorted({a for gname in sim for a in sim[gname]})
    out["sim"] = {}
    for gname in ("Mulheres não negras", "Mulheres negras", "Homens não negros", "Homens negros"):
        anos = sim[gname]
        assert len(anos) == 3
        out["sim"][gname] = {"media": sum(anos.values()) / 3, "min": min(anos.values()), "max": max(anos.values())}
    reg("sim_taxa_padronizada_2022_24", out["sim"], [P("dados/sim/asr_brasil.csv")], "media simples das taxas padronizadas por idade (agressao X85-Y09) de 2022, 2023, 2024; reproduz asr_brasil.md secao 4")
    with ler(P("dados/sim/asr_brasil.csv")) as fh:
        obitos_sim = sum(int(r["obitos"]) for r in csv.DictReader(fh) if r["grupo"] == "Brasil" and r["desfecho"] == "agressao")
    # ---------- P7 discurso
    base = P("research-2026-10-21-rodada3/discurso/midia")
    cont = defaultdict(int)
    den = 0
    with ler(os.path.join(base, "contagens.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["ano"] == "total":
                continue
            uniao = r["consulta"].startswith(r["familia"] + "-any")  # linha de uniao das entradas (evita contar duas vezes)
            if r["universo"] in ("Camara", "Senado"):
                if r["familia"] in ("F1", "F2", "F3", "F4"):
                    if uniao:
                        cont[("v2", r["familia"])] += int(r["n"])
                elif r["familia"] == "TOTAL":
                    den += int(r["n"])
            elif r["universo"] in ("Camara (v1 literal)", "Senado (v1 literal)") and r["familia"] in ("F1", "F2", "F3", "F4") and uniao:
                cont[("v1", r["familia"])] += int(r["n"])
    v2 = {f: cont[("v2", f)] for f in ("F1", "F2", "F3", "F4")}
    v1 = {f: cont[("v1", f)] for f in ("F1", "F2", "F3", "F4")}
    assert v2 == {"F1": 14, "F2": 56, "F3": 148, "F4": 2}, v2  # confere com MIDIA.md 3.1
    assert den == 258011, den
    afirma = Counter()
    n_amostra = Counter()
    with ler(os.path.join(base, "amostra_codificada.csv")) as fh:
        linhas_amostra = 0
        for r in csv.DictReader(fh):
            linhas_amostra += 1
            if r["universo"] == "Parlamento":
                n_amostra[r["familia"]] += 1
                if r["postura"] in ("AFIRMA", "ATRIBUI"):
                    afirma[r["familia"]] += 1
    est_f3 = None
    lo, hi = wilson(afirma["F3"], n_amostra["F3"])
    est_f3 = {"k": afirma["F3"], "n": n_amostra["F3"], "N": v2["F3"], "est": v2["F3"] * afirma["F3"] / n_amostra["F3"], "lo": v2["F3"] * lo, "hi": v2["F3"] * hi}
    assert (round(est_f3["est"]), round(est_f3["lo"]), round(est_f3["hi"])) == (81, 63, 99), est_f3  # confere com _estimativas.txt
    anos_disc = sorted(int(r["ano"]) for r in csv.DictReader(ler(os.path.join(base, "contagens.csv"))) if r["universo"] in ("Camara", "Senado") and r["familia"] == "TOTAL")
    out["discurso_anos"] = [anos_disc[0], anos_disc[-1]]
    out["discurso"] = {"v1": v1, "v2": v2, "denominador": den, "afirma": {f: afirma[f] for f in ("F1", "F2", "F3", "F4")},
                       "amostra_n": {f: n_amostra[f] for f in ("F1", "F2", "F3", "F4")}, "est_f3": est_f3, "itens_codificados": linhas_amostra}
    reg("discurso_parlamento", out["discurso"], [os.path.join(base, "contagens.csv"), os.path.join(base, "amostra_codificada.csv")],
        "soma anual Camara+Senado por familia (v1 literal e v2); AFIRMA+ATRIBUI na amostra Parlamento; F3 por Wilson 95% x N (censo em F1/F2/F4)")
    kap = {}
    with ler(P("research-2026-10-21-rodada3/escrutinio/simetria/concordancia_C27.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["campo"] == "postura (todos)" and r["estrato"] in ("F2-Parlamento", "F3-Parlamento"):
                kap[r["estrato"][:2]] = float(r["kappa"])
    assert set(kap) == {"F2", "F3"} and kap["F2"] >= 0.60 > kap["F3"], kap  # criterio da reanalise: kappa < 0,60 => indicativo
    out["discurso"]["kappa_postura"] = kap
    reg("kappa_segundo_codificador", kap, [P("research-2026-10-21-rodada3/escrutinio/simetria/concordancia_C27.csv")], "kappa de postura (todos) do 2o codificador (Grok) em F2 e F3 do Parlamento; F3 < 0,60 => indicativo")
    # ---------- P8 governos
    tab = {}
    txt = ler(P("dados/painel/resultados_tse_brc.md")).read()
    m = re.search(r"\n\| desfecho \| b \(por 1 ponto de ideologia\).*?\n((?:\|.*\n)+)", txt)
    for ln in m.group(1).strip().splitlines()[1:]:
        c = [x.strip() for x in ln.strip("|").split("|")]
        ic = re.findall(r"[-+]\d\.\d+", c[3])
        tab[c[0]] = {"b": float(c[1]), "ep": float(c[2]), "lo": float(ic[0]), "hi": float(ic[1]), "n": int(c[4])}
    for k, t in tab.items():  # IC95% = b +- 1,96 EP (confere com a tabela arredondada)
        assert abs((t["b"] - 1.96 * t["ep"]) - t["lo"]) < 0.0009 and abs((t["b"] + 1.96 * t["ep"]) - t["hi"]) < 0.0009, k
    painel = list(csv.DictReader(ler(P("dados/painel/painel_uf_ano_tse_brc.csv"))))
    # limites EXATOS da reanalise C03(1): 100[exp(k*limite)-1], k lido do cabecalho da secao 1 de c03_event_pesos_resultados.md
    txt3 = ler(P("dados/painel/c03_event_pesos_resultados.md")).read()
    sec = txt3[txt3.index("## 1. Conversão exata"):txt3.index("BLS9 2021")]
    mk = re.search(r"\(k = (\d+) pontos; ([^)]*)\)", sec)
    k_pts, base_txt = int(mk.group(1)), mk.group(2)
    gov = {}
    for m_ in re.finditer(r"^\| (tx_\w+) \| ([+-]\d\.\d+) \| (\d\.\d+) \| \[([+-]\d\.\d+); ([+-]\d\.\d+)\] \| \[[^\]]*\] \| \[([+-]\d+\.\d); ([+-]\d+\.\d)\] \|", sec, re.M):
        nome, b_, ep_, lo_, hi_, elo, ehi = m_.group(1), *(float(x) for x in m_.groups()[1:])
        assert abs(b_ - tab[nome]["b"]) < 1e-9 and abs(ep_ - tab[nome]["ep"]) < 1e-9, nome  # b e EP da reanalise == tabela principal
        plo, phi = 100 * (math.exp(k_pts * lo_) - 1), 100 * (math.exp(k_pts * hi_) - 1)
        assert abs(plo - elo) < 0.06 and abs(phi - ehi) < 0.06, (nome, plo, elo, phi, ehi)  # calculado aqui == impresso pela reanalise
        gov[nome] = {"b": b_, "ep": ep_, "lo": lo_, "hi": hi_, "lo_pct": elo, "hi_pct": ehi, "lo_pct_recalc": plo, "hi_pct_recalc": phi, "n": tab[nome]["n"]}  # exibe o valor da reanalise (IC com mais casas); o recalculo com 4 casas confere a +-0,06
    assert sorted(gov) == sorted(tab) and len(gov) == 6, gov.keys()
    for nome, (el, eh) in {"tx_total": (-10.8, 13.1), "tx_mulheres": (-10.1, 10.5), "tx_arma": (-16.2, 20.4)}.items():  # conferencia com a frase da reanalise
        assert (round(gov[nome]["lo_pct"], 1), round(gov[nome]["hi_pct"], 1)) == (el, eh), nome
    assert "inconclusivo, não nulo" in ler(P("research-2026-10-21-rodada3/escrutinio/reanalise/RESULTADOS.md")).read()  # legenda: event study inconclusivo
    out["painel_anos"] = [min(int(r["ano"]) for r in painel), max(int(r["ano"]) for r in painel)]
    out["governos"] = {"tabela": gov, "k": k_pts, "base": base_txt, "n_uf_anos": len(painel)}
    reg("governos_painel", out["governos"], [P("dados/painel/c03_event_pesos_resultados.md"), P("dados/painel/resultados_tse_brc.md"), P("dados/painel/painel_uf_ano_tse_brc.csv"),
                                             P("research-2026-10-21-rodada3/escrutinio/reanalise/RESULTADOS.md")],
        "limites exatos 100*[exp(k*limite)-1] impressos pela reanalise C03 (secao 1), k lido do cabecalho; recalculados aqui a partir do IC de b com 4 casas e conferidos a +-0,06")
    # ---------- KPIs
    scripts = contar_scripts()
    n_pdf, n_pdf_unicos = contar_pdfs()
    revisores = sorted(glob.glob(P("research-2026-10-21-rodada3/escrutinio/revisao_*.md")))
    origens = sorted({r["origem"] for r in regs})
    analises = contar_analises()
    with ler(P("dados/sinan/serie_campo55_uf_ano.csv")) as fh:
        sinan = sum(int(r["n_interpessoal"]) for r in csv.DictReader(fh) if r["uf"] != "BR")
    kp = {
        "dias": (DATA_FIM - DATA_INI).days + 1,
        "fontes": n_unicos,
        "idiomas": len(c_lang),
        "scripts": len(scripts),
        "revisores": len(revisores),
        "pdfs": n_pdf_unicos,
        "textos_integrais": len(v["lido"]),
        "textos_sem_registro": len(v["lido"] - chaves_doi),
        "agentes": len(origens),
        "analises": len(analises),
        "obitos_sim": obitos_sim,
        "notificacoes_sinan": sinan,
        "falas": den,
        "itens_codificados": linhas_amostra,
        "uf_anos": len(painel),
        "observacoes": obitos_sim + sinan + den + linhas_amostra,
    }
    out["kpis"] = kp
    reg("dias", kp["dias"], [], f"(2026-10-23 - 2026-10-10) + 1 dias; datas do registro do projeto; ts dos ledgers entre {ts_min} e {ts_max}")
    reg("scripts", kp["scripts"], [], "find PROJ -name '*.py' (sem __pycache__ e sem fontes/, que e material baixado)")
    NUM["scripts"]["origem"]["lista"] = scripts
    reg("revisores", kp["revisores"], revisores, "ls escrutinio/revisao_*.md (agy, codex, grok, opus)")
    reg("pdfs", kp["pdfs"], [], f"sha256 distintos de *.pdf em fontes/ (exceto q1-textointegral/discurso); {n_pdf} arquivos no disco")
    reg("textos_integrais", kp["textos_integrais"], v["arquivos"], "DOIs com veredito != SEM_TEXTO_INTEGRAL em algum CSV de verificacao (inclui os sem linha no ledger)")
    reg("agentes", kp["agentes"], arqs, "valores distintos do campo origem dos ledgers (piso: so quem gravou fonte)")
    NUM["agentes"]["origem"]["lista"] = origens
    reg("analises", kp["analises"], [], "arquivos .md fora de fontes/ cujo cabecalho diz 'gerado por <script>.py'")
    NUM["analises"]["origem"]["lista"] = analises
    reg("observacoes", kp["observacoes"], [P("dados/sim/asr_brasil.csv"), P("dados/sinan/serie_campo55_uf_ano.csv")],
        "obitos SIM por agressao 2010-24 (Brasil) + notificacoes Sinan interpessoais 2015-25 (sem a linha BR) + falas varridas + itens codificados")
    reg("itens_codificados", linhas_amostra, [os.path.join(base, "amostra_codificada.csv")], "linhas de amostra_codificada.csv")
    reg("uf_anos", len(painel), [P("dados/painel/painel_uf_ano_tse_brc.csv")], "linhas do painel principal")
    out["conferencia_titulo"] = {"fontes_titulo": 826, "scripts_titulo": 127, "revisores_titulo": 4, "dias_titulo": 14, "idiomas_titulo": 10}
    out["ledger_datas"] = [ts_min, ts_max]
    out["pdf_arquivos_no_disco"] = n_pdf
    return out, regs, arqs


# ================================================================== 5. TEXTOS pt-br (LABELS) + SPEC
LABELS_PT = {
    # idiomas dos sources
    "lang.en": "Inglês", "lang.pt": "Português", "lang.es": "Espanhol", "lang.fr": "Francês", "lang.de": "Alemão",
    "lang.ja": "Japonês", "lang.ko": "Coreano", "lang.zh-Hans": "Chinês", "lang.id": "Indonésio", "lang.tr": "Turco",
    # P0
    "kpi.dias": "dias de projeto", "kpi.dias.nota": "de {d1} a {d2}",
    "kpi.fontes": "fontes únicas registradas", "kpi.fontes.nota": "{reg} linhas em {led} registros, sem repetição",
    "kpi.idiomas": "idiomas das fontes", "kpi.idiomas.nota": "pt e pt-BR somados",
    "kpi.scripts": "scripts em Python", "kpi.scripts.nota": "do projeto; fora do material baixado",
    "kpi.revisores": "revisores hostis", "kpi.revisores.nota": "modelos de IA diferentes, cada um com uma revisão escrita",
    "kpi.pdfs": "PDFs arquivados", "kpi.pdfs.nota": "arquivos distintos (por hash)",
    "kpi.textos": "textos integrais lidos", "kpi.textos.nota": "artigos com DOI conferidos contra o dossiê; {sem} sem linha no registro de fontes",
    "kpi.agentes": "agentes que registraram fontes", "kpi.agentes.nota": "frentes de pesquisa distintas; é piso",
    "kpi.analises": "análises reproduzíveis", "kpi.analises.nota": "resultados gerados por script",
    "kpi.obs": "registros analisados", "kpi.obs.nota": "{sim} óbitos (SIM) + {sinan} notificações (Sinan) + {falas} falas + {itens} itens codificados",
    # P1
    "p1.title": "Fontes registradas por idioma", "p1.subtitle": "{n} fontes únicas em {k} idiomas",
    "p1.source": "Fonte: registros de fontes do projeto, de {d1} a {d2}; uma contagem por fonte única.",
    "p1.g1": "Fontes únicas por idioma", "p1.vl": "{n} ({pct}%)",
    "p1.desc": "Barras horizontais com as {n} fontes únicas por idioma: inglês {en}, português {pt}, espanhol {es} e {outros} fontes em outros {ko} idiomas.",
    # P2
    "p2.title": "O que são as fontes", "p2.subtitle": "Tipo e período de publicação; cada bloco soma {n}",
    "p2.source": "Fonte: registros do projeto; tipo por canal, DOI e domínio; quartil SJR só onde conferido.",
    "p2.g1": "Por tipo de fonte", "p2.g2": "Por período de publicação",
    "p2.t.per_q1": "Periódico Q1", "p2.t.per_q2": "Periódico Q2", "p2.t.per_q34": "Periódico Q3-Q4", "p2.t.per_semq": "Periódico sem Q",
    "p2.t.oficial": "Oficial", "p2.t.preprint": "Preprint/WP/tese", "p2.t.ong": "ONG / sociedade", "p2.t.imprensa": "Imprensa",
    "p2.t.dado": "Dado / microdado", "p2.t.livro": "Livro", "p2.t.enciclopedia": "Enciclopédia", "p2.t.nao_classificado": "Não classificado",
    "p2.f.ate": "até {a}", "p2.f.de_a": "{a} a {b}", "p2.f.desde": "{a} em diante", "p2.f.sem_ano": "sem ano",
    "p2.vl": "{n} ({pct}%)",
    "p2.desc": "Dois blocos de barras, cada um somando {n} fontes. Por tipo: {oficial} oficiais, {per} em periódicos ({q1} com quartil Q1 conferido), {ong} de ONGs e {ncl} sem classificação. Por período: {rec} publicadas de {ano_rec} em diante.",
    # P3
    "p3.title": "Do que foi achado ao que sustenta uma conclusão", "p3.subtitle": "Escala linear: a lasca é o dado",
    "p3.source": "Fonte: verificações de texto integral dos artigos com DOI; Q1 = melhor quartil SJR conferido.",
    "p3.s1": "Fontes registradas", "p3.s1.sub": "{n} fontes únicas, de qualquer tipo",
    "p3.s2": "Texto integral lido", "p3.s2.sub": "{n} ({pct}%) artigos com DOI no registro, conferidos contra o dossiê",
    "p3.s3": "Dessas, em periódico Q1", "p3.s3.sub": "{n} ({pct}% das lidas)",
    "p3.s4": "Q1 e usadas em alguma conclusão", "p3.s4.sub": "{n} ({pct}% das Q1 lidas) confirmam ou corrigem ao menos uma afirmação do dossiê",
    "p3.desc": "Funil em escala linear: {reg} fontes registradas, {lido} com texto integral lido, {q1} delas em periódico Q1 e {usado} usadas em alguma conclusão.",
    # P4
    "p4.title": "Violência sofrida em 12 meses, PNS 2019", "p4.subtitle": "Adultos LGB+ e heterossexuais; RP = razão de prevalências",
    "p4.source": "Fonte: IBGE, PNS 2019 (microdados), desenho amostral completo; reproduz Vasconcelos et al. 2023.",
    "p4.g1": "LGB+", "p4.g2": "Heterossexuais",
    "p4.i.fisica": "Violência física", "p4.i.sexual": "Violência sexual", "p4.i.qualquer": "Qualquer violência",
    "p4.vl.lgb": "{p}% · RP {rp} (IC95% {lo}–{hi})", "p4.vl.het": "{p}%",
    "p4.desc": "Barras horizontais com a violência sofrida em 12 meses. Física: {fl}% entre LGB+ e {fh}% entre heterossexuais. Sexual: {sl}% e {sh}%. Qualquer violência: {ql}% e {qh}%.",
    # P5
    "p5.title": "Quantas mortes o registro do GGB cobre", "p5.subtitle": "Contagem do GGB em três recortes contra o esperado: risco igual (RR {rr1}) ou o da violência física na PNS (RR {rr2}; {rr3})",
    "p5.source": "Fonte: GGB, SIM/DATASUS e PNS 2019; exercício de escala ({prev}% da população adulta), não é estimativa de mortes.",
    "p5.g": "Ano {ano}",
    "p5.i.n0": "N0 total do GGB", "p5.i.n1": "N1 homic. + latroc.", "p5.i.n2": "N2 N1 sem trans", "p5.i.rr": "Esperado, RR {rr}",
    "p5.vl.num": "{n} ({cob}% do esperado)", "p5.vl.esp1": "{n}", "p5.vl.esp": "{n} (N0 {c0}%; N2 {c2}%)",
    "p5.desc": "Barras horizontais. N0 é o total declarado pelo GGB; N1, só homicídio e latrocínio; N2, N1 sem as pessoas trans. Sob risco igual ao dos pares, o GGB cobria {c10}% (N0), {c11}% (N1) e {c12}% (N2) do esperado em {a1}, e {c20}%, {c21}% e {c22}% em {a2}; com RR {rr2} ou {rr3}, no máximo {mx}%.",
    # P6
    "p6.title": "Taxa de homicídio por idade, quatro grupos", "p6.subtitle": "Por 100 mil, padronizada por idade, média de {y0} a {y1}",
    "p6.source": "Fonte: SIM/DATASUS (X85-Y09) e IBGE; não há campo de orientação sexual no atestado de óbito.",
    "p6.g1": "Agressões por 100 mil habitantes",
    "p6.i.mulheres_nao_negras": "Mulheres não negras", "p6.i.mulheres_negras": "Mulheres negras",
    "p6.i.homens_nao_negros": "Homens não negros", "p6.i.homens_negros": "Homens negros",
    "p6.vl": "{n} por 100 mil",
    "p6.desc": "Barras horizontais com a taxa de agressões padronizada por idade: de {mnn} por 100 mil entre mulheres não negras a {hn} entre homens negros, razão de {razao} para 1.",
    # P7
    "p7.title": "Quatro frases sobre mortes de LGBT no Parlamento", "p7.subtitle": "Câmara e Senado, {a0} a {a1}, {n} falas varridas",
    "p7.source": "Fonte: Câmara e Senado, falas varridas por dicionário; leitura por dois codificadores (outra família de IA); F3 é estimativa indicativa.",
    "p7.g1": "Dicionário literal (v1), antes da correção", "p7.g2": "Dicionário corrigido (v2): falas com a frase",
    "p7.g3": "Dessas, afirmam ou relatam a alegação",
    "p7.i.f1": "F1 morrem mais", "p7.i.f2": "F2 mais mata", "p7.i.f3": "F3 governo mata", "p7.i.f4": "F4 não existe",
    "p7.vl": "{n}", "p7.vl.censo": "{n} (todas lidas)", "p7.vl.censo_k": "{n} (todas lidas; 2º codificador κ {kap})", "p7.vl.est": "≈{n} (IC95% {lo}–{hi}; indicativo, κ {kap})",
    "p7.desc": "Barras horizontais em três blocos. F1: gays morrem mais; F2: o Brasil é o país que mais mata; F3: governo de direita mata ou persegue; F4: homofobia não existe ou o dado é inventado. Com o dicionário literal: {v1_1}, {v1_2}, {v1_3} e {v1_4} falas; com o corrigido: {v2_1}, {v2_2}, {v2_3} e {v2_4}; afirmam ou relatam: {c1}, {c2}, cerca de {c3} (estimativa) e {c4}. Um segundo codificador, de outra família de IA, concorda em F2 (κ {k2}) e só de forma indicativa em F3 (κ {k3}).",
    # P8
    "p8.title": "O que o painel de governos consegue excluir", "p8.subtitle": "{n} UF-anos, {y0} a {y1}; troca de {k} pontos na escala do escore, do PT para DEM/PL",
    "p8.source": "Fonte: SIM/DATASUS, TSE, escore BRC de ideologia; painel exploratório com efeitos fixos, não causal; limites 100[exp(k·limite)−1].",
    "p8.g1": "Queda máxima compatível com o IC95% (%)", "p8.g2": "Alta máxima compatível com o IC95% (%)",
    "p8.i.tx_total": "Total", "p8.i.tx_homens": "Homens", "p8.i.tx_mulheres": "Mulheres", "p8.i.tx_negros": "Negros",
    "p8.i.tx_nao_negros": "Não negros", "p8.i.tx_arma": "Arma de fogo",
    "p8.vl.lo": "{x}% · b {b}", "p8.vl.hi": "{x}% · IC de b {lo} a {hi}",
    "p8.legenda": "Nulo não é ausência de efeito: o painel exclui só quedas maiores que {a}% a {b}% e altas maiores que {c}% a {d}%; e o event study sobre trocas de governo foi inconclusivo.",
    "p8.desc": "Barras horizontais com os limites do IC95%, em por cento da taxa, para uma troca de {k} pontos: total entre {tl}% e {tu}%, mulheres entre {ml}% e {mu}%, arma de fogo entre {al}% e {au}%. Nenhum coeficiente se distingue de zero; o event study sobre trocas de governo foi inconclusivo.",
}
PAINEIS = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]
PAINEL_DATASETS = {"p1": ["lgbt-violencia-fontes-idiomas"], "p2": ["lgbt-violencia-fontes-tipos"], "p3": ["lgbt-violencia-funil-evidencia"],
                   "p4": ["lgbt-violencia-pns-2019"], "p5": ["lgbt-violencia-ggb-cobertura"], "p6": ["lgbt-violencia-sim-taxa"],
                   "p7": ["lgbt-violencia-circulacao"], "p8": ["lgbt-violencia-governos"]}
PAINEL_COMP = {"p1": "CountryBarsChart", "p2": "CountryBarsChart", "p3": "FunnelChart", "p4": "CountryBarsChart", "p5": "CountryBarsChart",
               "p6": "CountryBarsChart", "p7": "CountryBarsChart", "p8": "CountryBarsChart"}


def nice_ceil(x):
    for k in range(-3, 8):
        for esc in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8):
            c = round(esc * 10 ** k, 6)
            if c >= x - 1e-12:
                return c
    return x


def encaixa_max(grupos, textos_pt):
    """max do eixo tal que barra + rotulo caibam no viewBox (CountryBarsChart: PAD.left 150, plotW 506, W 720); folga de 25% p/ traducoes."""
    need = 0.0
    for g, tx in zip(grupos, textos_pt):
        for it, rot in zip(g["items"], tx):
            livre = 712 - 158 - len(rot) * 6.4 * 1.25
            assert livre > 150, (rot, livre)
            need = max(need, it["value"] * 506 / livre)
    return nice_ceil(need)


def T(chave, /, **p):
    return {"k": chave, "p": p} if p else {"k": chave}


FAIXAS = ["ate2009", "2010_14", "2015_19", "2020_24", "2025_26", "sem_ano"]
FAIXA_LIM = [(None, 2009), (2010, 2014), (2015, 2019), (2020, 2024), (2025, None)]  # limites das faixas (definicao)


def faixa_nomes():
    nomes = []
    for (a, b), f in zip(FAIXA_LIM, FAIXAS):
        if a is None:
            nomes.append(T("p2.f.ate", a=str(b)))
        elif b is None:
            nomes.append(T("p2.f.desde", a=str(a)))
        else:
            nomes.append(T("p2.f.de_a", a=str(a), b=str(b)))
    nomes.append(T("p2.f.sem_ano"))
    return nomes


def montar_spec(c):
    """Especificacao neutra de idioma: so chaves de LABELS + numeros. Python (pt-br) e TS renderizam a MESMA estrutura."""
    spec = {"countryBars": {}, "funnel": {}}
    n_unicos = NUM["fontes_unicas"]["valor"]

    def pct(x, tot):
        return [100.0 * x / tot, 1]

    def montar_cb(id_, grupos, rotulos_pt):
        spec["countryBars"][id_] = {"max": encaixa_max(grupos, rotulos_pt), "groups": grupos}

    # P1 idiomas
    items, rot = [], []
    for lang, cnt in c["idiomas"]:
        vl = T("p1.vl", n=cnt, pct=pct(cnt, n_unicos))
        items.append({"name": T("lang." + lang), "value": cnt, "valueLabel": vl})
        rot.append(render_pt(vl))
    montar_cb("lgbt-violencia-fontes-idiomas", [{"label": T("p1.g1"), "color": AZUL, "items": items}], [rot])
    # P2 tipos + faixas
    ti, rt = [], []
    for t in TIPOS:
        cnt = c["tipos"][t]
        vl = T("p2.vl", n=cnt, pct=pct(cnt, n_unicos))
        ti.append({"name": T("p2.t." + t), "value": cnt, "valueLabel": vl})
        rt.append(render_pt(vl))
    fi, rf = [], []
    for f, nome in zip(FAIXAS, faixa_nomes()):
        cnt = c["faixas"][f]
        vl = T("p2.vl", n=cnt, pct=pct(cnt, n_unicos))
        fi.append({"name": nome, "value": cnt, "valueLabel": vl})
        rf.append(render_pt(vl))
    montar_cb("lgbt-violencia-fontes-tipos", [{"label": T("p2.g1"), "color": OURO, "items": ti}, {"label": T("p2.g2"), "color": AZUL, "items": fi}], [rt, rf])
    # P3 funil
    f = c["funil"]
    spec["funnel"]["lgbt-violencia-funil-evidencia"] = {"steps": [
        {"label": T("p3.s1"), "sublabel": T("p3.s1.sub", n=f["registradas"]), "color": AZUL, "value": f["registradas"]},
        {"label": T("p3.s2"), "sublabel": T("p3.s2.sub", n=f["lido"], pct=pct(f["lido"], f["registradas"])), "color": OURO, "value": f["lido"]},
        {"label": T("p3.s3"), "sublabel": T("p3.s3.sub", n=f["q1_lido"], pct=pct(f["q1_lido"], f["lido"])), "color": AMBAR, "value": f["q1_lido"]},
        {"label": T("p3.s4"), "sublabel": T("p3.s4.sub", n=f["q1_usado"], pct=pct(f["q1_usado"], f["q1_lido"])), "color": CINZA_CLARO, "value": f["q1_usado"]},
    ]}
    # P4 PNS
    pns = c["pns"]
    lgb, het, rl, rh = [], [], [], []
    for k, ik in (("física", "fisica"), ("sexual", "sexual"), ("qualquer", "qualquer")):
        r = pns[k]
        v1 = T("p4.vl.lgb", p=[100 * r["prev_grupo"], 2], rp=[r["rp"], 2], lo=[r["ic_lo"], 2], hi=[r["ic_hi"], 2])
        v2 = T("p4.vl.het", p=[100 * r["prev_ref"], 2])
        lgb.append({"name": T("p4.i." + ik), "value": round(100 * r["prev_grupo"], 2), "valueLabel": v1, "emphasis": True})
        het.append({"name": T("p4.i." + ik), "value": round(100 * r["prev_ref"], 2), "valueLabel": v2})
        rl.append(render_pt(v1))
        rh.append(render_pt(v2))
    montar_cb("lgbt-violencia-pns-2019", [{"label": T("p4.g1"), "color": OURO, "items": lgb}, {"label": T("p4.g2"), "color": CINZA, "items": het}], [rl, rh])
    # P5 GGB (numeradores N0/N1/N2 e esperado)
    grupos, rots = [], []
    for ano in sorted(c["ggb"]):
        d = c["ggb"][ano]
        its, rs = [], []
        for nm in ("N0", "N1", "N2"):
            x = d["num"][nm]
            v = T("p5.vl.num", n=x["n"], cob=[100 * x["cob"][0], 1])
            its.append({"name": T("p5.i." + nm.lower()), "value": x["n"], "valueLabel": v, **({"emphasis": True} if nm == "N0" else {})})
            rs.append(render_pt(v))
        for j, rr in enumerate(("1.0", "2.82", "3.84")):
            e = d["esperado"][rr]
            v = T("p5.vl.esp1", n=round(e)) if j == 0 else T("p5.vl.esp", n=round(e), c0=[100 * d["num"]["N0"]["cob"][j], 1], c2=[100 * d["num"]["N2"]["cob"][j], 1])
            its.append({"name": T("p5.i.rr", rr=[float(rr), 2]), "value": round(e), "valueLabel": v})
            rs.append(render_pt(v))
        grupos.append({"label": T("p5.g", ano=str(ano)), "color": AZUL, "items": its})
        rots.append(rs)
    montar_cb("lgbt-violencia-ggb-cobertura", grupos, rots)
    # P6 SIM
    its, rs = [], []
    for gname, ik in (("Mulheres não negras", "mulheres_nao_negras"), ("Mulheres negras", "mulheres_negras"), ("Homens não negros", "homens_nao_negros"), ("Homens negros", "homens_negros")):
        val = round(c["sim"][gname]["media"], 1)
        v = T("p6.vl", n=[val, 1])
        its.append({"name": T("p6.i." + ik), "value": val, "valueLabel": v})
        rs.append(render_pt(v))
    montar_cb("lgbt-violencia-sim-taxa", [{"label": T("p6.g1"), "color": AZUL, "items": its}], [rs])
    # P7 discurso
    d = c["discurso"]
    g1, g2, g3, r1, r2, r3 = [], [], [], [], [], []
    for fam in ("F1", "F2", "F3", "F4"):
        ik = "p7.i." + fam.lower()
        v = T("p7.vl", n=d["v1"][fam])
        g1.append({"name": T(ik), "value": d["v1"][fam], "valueLabel": v})
        r1.append(render_pt(v))
        v = T("p7.vl", n=d["v2"][fam])
        g2.append({"name": T(ik), "value": d["v2"][fam], "valueLabel": v, "emphasis": True})
        r2.append(render_pt(v))
        if fam == "F3":
            e = d["est_f3"]
            v = T("p7.vl.est", n=round(e["est"]), lo=round(e["lo"]), hi=round(e["hi"]), kap=[d["kappa_postura"]["F3"], 2])
            val = round(e["est"])
        else:
            val = d["afirma"][fam]
            v = T("p7.vl.censo_k", n=val, kap=[d["kappa_postura"]["F2"], 2]) if fam == "F2" else T("p7.vl.censo", n=val)
        g3.append({"name": T(ik), "value": val, "valueLabel": v})
        r3.append(render_pt(v))
    montar_cb("lgbt-violencia-circulacao", [{"label": T("p7.g1"), "color": CINZA, "items": g1}, {"label": T("p7.g2"), "color": OURO, "items": g2},
                                            {"label": T("p7.g3"), "color": AZUL, "items": g3}], [r1, r2, r3])
    # P8 governos: limites exatos (queda e alta) em dois blocos
    gv = c["governos"]["tabela"]
    gl, gu, rl, ru = [], [], [], []
    for k_ in ("tx_total", "tx_homens", "tx_mulheres", "tx_negros", "tx_nao_negros", "tx_arma"):
        t = gv[k_]
        v = T("p8.vl.lo", x=[t["lo_pct"], 1, "s"], b=[t["b"], 4, "s"])
        gl.append({"name": T("p8.i." + k_), "value": round(abs(t["lo_pct"]), 1), "valueLabel": v})
        rl.append(render_pt(v))
        v = T("p8.vl.hi", x=[t["hi_pct"], 1, "s"], lo=[t["lo"], 4, "s"], hi=[t["hi"], 4, "s"])
        gu.append({"name": T("p8.i." + k_), "value": round(t["hi_pct"], 1), "valueLabel": v})
        ru.append(render_pt(v))
    montar_cb("lgbt-violencia-governos", [{"label": T("p8.g1"), "color": OURO, "items": gl}, {"label": T("p8.g2"), "color": AZUL, "items": gu}], [rl, ru])
    return spec


def fill_pt(tpl, params, extra=None):
    def rep(m):
        n = m.group(1)
        if extra and n in extra:
            return extra[n]
        return param_pt(params[n])
    return re.sub(r"\{(\w+)\}", rep, tpl)


def render_pt(t, extra=None):
    return fill_pt(LABELS_PT[t["k"]], t.get("p", {}), extra)


def render_dataset_pt(kind, ds):
    """Replica em Python a renderizacao do .ts (pt-br) para comparar com a saida do Node."""
    if kind == "countryBars":
        return {"max": ds["max"], "groups": [{"label": render_pt(g["label"]), "color": g["color"], "items": [
            {k: v for k, v in {"name": render_pt(i["name"]), "value": i["value"], "valueLabel": render_pt(i["valueLabel"]),
                               "emphasis": i.get("emphasis")}.items() if v is not None} for i in g["items"]]} for g in ds["groups"]]}
    return {"steps": [{"label": render_pt(s["label"]), "sublabel": render_pt(s["sublabel"]), "color": s["color"], "value": s["value"]} for s in ds["steps"]]}


def paineis_params(c):
    n = NUM["fontes_unicas"]["valor"]
    idi = dict(c["idiomas"])
    top3 = [k for k, _ in c["idiomas"][:3]]
    assert top3 == ["en", "pt", "es"], top3  # a descricao de P1 nomeia estes tres
    tp, fx = c["tipos"], c["faixas"]
    per = tp["per_q1"] + tp["per_q2"] + tp["per_q34"] + tp["per_semq"]
    f, pns, gg, sim, d, gv = c["funil"], c["pns"], c["ggb"], c["sim"], c["discurso"], c["governos"]["tabela"]
    anos = sorted(gg)
    g1, g2 = gg[anos[0]], gg[anos[1]]
    s_anos = sorted(int(a) for a in c["sim_anos"])
    pc = lambda x: [100 * x, 2]  # noqa: E731
    assert min(sim, key=lambda k_: sim[k_]["media"]) == "Mulheres não negras" and max(sim, key=lambda k_: sim[k_]["media"]) == "Homens negros"  # P6 desc
    return {
        "p1": {"n": n, "k": NUM["idiomas"]["valor"], "d1": par_data("ini"), "d2": par_data("fim"), "en": idi["en"], "pt": idi["pt"], "es": idi["es"],
               "outros": n - idi["en"] - idi["pt"] - idi["es"], "ko": NUM["idiomas"]["valor"] - 3},
        "p2": {"n": n, "oficial": tp["oficial"], "per": per, "q1": tp["per_q1"], "ong": tp["ong"], "ncl": tp["nao_classificado"],
               "rec": fx["2020_24"] + fx["2025_26"], "ano_rec": str(FAIXA_LIM[3][0])},
        "p3": {"reg": f["registradas"], "lido": f["lido"], "q1": f["q1_lido"], "usado": f["q1_usado"]},
        "p4": {"fl": pc(pns["física"]["prev_grupo"]), "fh": pc(pns["física"]["prev_ref"]), "sl": pc(pns["sexual"]["prev_grupo"]), "sh": pc(pns["sexual"]["prev_ref"]),
               "ql": pc(pns["qualquer"]["prev_grupo"]), "qh": pc(pns["qualquer"]["prev_ref"])},
        "p5": {"prev": [c["ggb_prev"], 2], "a1": str(anos[0]), "a2": str(anos[1]), "rr1": [1.0, 2], "rr2": [2.82, 2], "rr3": [3.84, 2], "mx": [c["ggb_max_rr_alto"], 1],
               **{f"c1{i}": [100 * g1["num"][f"N{i}"]["cob"][0], 1] for i in range(3)}, **{f"c2{i}": [100 * g2["num"][f"N{i}"]["cob"][0], 1] for i in range(3)}},
        "p6": {"y0": str(s_anos[0]), "y1": str(s_anos[-1]), "mnn": [round(sim["Mulheres não negras"]["media"], 1), 1], "hn": [round(sim["Homens negros"]["media"], 1), 1],
               "razao": [sim["Homens negros"]["media"] / sim["Mulheres não negras"]["media"], 1]},
        "p7": {"n": d["denominador"], "a0": str(c["discurso_anos"][0]), "a1": str(c["discurso_anos"][1]),
               **{f"v1_{i+1}": d["v1"][fm] for i, fm in enumerate(("F1", "F2", "F3", "F4"))}, **{f"v2_{i+1}": d["v2"][fm] for i, fm in enumerate(("F1", "F2", "F3", "F4"))},
               "c1": d["afirma"]["F1"], "c2": d["afirma"]["F2"], "c3": round(d["est_f3"]["est"]), "c4": d["afirma"]["F4"], "k2": [d["kappa_postura"]["F2"], 2], "k3": [d["kappa_postura"]["F3"], 2]},
        "p8": {"n": c["governos"]["n_uf_anos"], "y0": str(c["painel_anos"][0]), "y1": str(c["painel_anos"][1]), "k": c["governos"]["k"],
               "tl": [gv["tx_total"]["lo_pct"], 1, "s"], "tu": [gv["tx_total"]["hi_pct"], 1, "s"], "ml": [gv["tx_mulheres"]["lo_pct"], 1, "s"], "mu": [gv["tx_mulheres"]["hi_pct"], 1, "s"],
               "al": [gv["tx_arma"]["lo_pct"], 1, "s"], "au": [gv["tx_arma"]["hi_pct"], 1, "s"],
               "a": [min(abs(t["lo_pct"]) for t in gv.values()), 1], "b": [max(abs(t["lo_pct"]) for t in gv.values()), 1],
               "c": [min(t["hi_pct"] for t in gv.values()), 1], "d": [max(t["hi_pct"] for t in gv.values()), 1]},
    }


def legendas_pt(spec, c):
    """title/subtitle/source/description por painel, em pt-br (o .ts calcula igual)."""
    par = paineis_params(c)
    res = {}
    for p in PAINEIS:
        dados = par[p]
        f = lambda key: fill_pt(LABELS_PT[key], dados)  # noqa: E731
        res[p] = {"title": LABELS_PT[p + ".title"], "subtitle": f(p + ".subtitle"), "source": f(p + ".source"), "description": f(p + ".desc")}
    res["p8"]["legenda"] = fill_pt(LABELS_PT["p8.legenda"], par["p8"])
    return res, par, None


def kpis_lista(c):
    k = c["kpis"]
    return [
        ("dias", [k["dias"], 0], {"d1": par_data("ini"), "d2": par_data("fim")}),
        ("fontes", [k["fontes"], 0], {"reg": [NUM["registros_brutos"]["valor"], 0], "led": [NUM["ledgers"]["valor"], 0]}),
        ("idiomas", [k["idiomas"], 0], {}),
        ("scripts", [k["scripts"], 0], {}),
        ("revisores", [k["revisores"], 0], {}),
        ("pdfs", [k["pdfs"], 0], {}),
        ("textos", [k["textos_integrais"], 0], {"sem": [k["textos_sem_registro"], 0]}),
        ("agentes", [k["agentes"], 0], {}),
        ("analises", [k["analises"], 0], {}),
        ("obs", [k["observacoes"], 0], {"sim": [k["obitos_sim"], 0], "sinan": [k["notificacoes_sinan"], 0], "falas": [k["falas"], 0], "itens": [k["itens_codificados"], 0]}),
    ]


# ================================================================== 6. GERACAO DO .ts
TS_TEMPLATE = r"""/**
 * lgbt-violencia.data.ts -- datasets do dashboard de abertura do artigo LGBT-INDICADOR.
 * GERADO por build_dashboard.py. NAO EDITAR A MAO: os numeros vem de arquivos do projeto e o script os recontou.
 *
 * Como usar no site (o publicador decide):
 *   - copiar para data/ e espalhar nos registros de artigos-charts.ts:
 *       countryBarsDatasets = { ...countryBarsDatasets, ...lgbtCountryBarsDatasets }
 *       funnelDatasets      = { ...funnelDatasets, ...lgbtFunnelDatasets }
 *     (so `import type` do artigos-charts: sem ciclo em tempo de execucao).
 *   - ids: `lgbt-violencia-<painel>` (pt-br) e o mesmo id + `-en` / `-es` / `-it` / `-he` por locale (convencao do site).
 *   - cada locale entra SO se LABELS[locale] estiver COMPLETO (todas as chaves de 'pt-br'); incompleto = erro na carga.
 *
 * TRADUCOES: LABELS.en / es / it / he vem de labels.<locale>.json (mesmas 134 chaves do pt-br, mesmos {placeholders});
 * o build falha se faltar ou sobrar chave. Para mudar um texto, editar o json e rodar o build_dashboard.py de novo.
 * Nao editar SPEC, KPIS nem PAINEIS (numeros). Limites de largura (pt-br): nomes de linha <= 19 caracteres,
 * titulo <= 70, subtitulo e fonte de 1 linha; o eixo ja tem 25% de folga para rotulos mais longos.
 * Cores: so a paleta do site (ver cabecalho de artigos-charts.ts).
 */
import type { CountryBarsDataset, FunnelDataset } from './artigos-charts';

export type Locale = 'pt-br' | 'en' | 'es' | 'it' | 'he';
export const LOCALES: readonly Locale[] = ['pt-br', 'en', 'es', 'it', 'he'];
const SUFIXO: Record<Locale, string> = { 'pt-br': '', en: '-en', es: '-es', it: '-it', he: '-he' };
const INTL: Record<Locale, string> = { 'pt-br': 'pt-BR', en: 'en-US', es: 'es-ES', it: 'it-IT', he: 'he-IL' };

/** Numero: n | [n, casas] | [n, casas, 's'] (com sinal) | texto literal | data ({ini, fim, papel}: formatada por locale). */
type DataPar = { ini: string; fim: string; papel: 'ini' | 'fim' };
type Num = number | string | readonly [number, number] | readonly [number, number, string] | DataPar;
interface Tx {
  k: string;
  p?: Record<string, Num>;
}
interface SpecItem {
  name: Tx;
  value: number;
  valueLabel: Tx;
  emphasis?: boolean;
}
interface SpecGroup {
  label: Tx;
  color: string;
  items: SpecItem[];
}
interface SpecStep {
  label: Tx;
  sublabel: Tx;
  color: string;
  value: number;
}
interface Spec {
  countryBars: Record<string, { max: number; groups: SpecGroup[] }>;
  funnel: Record<string, { steps: SpecStep[] }>;
}

/* ── TEXTOS (únicos que mudam por idioma) ───────────────────────────── */
export const LABELS: Record<Locale, Record<string, string>> = {
  'pt-br': __LABELS__,
  en: __LABELS_EN__,
  es: __LABELS_ES__,
  it: __LABELS_IT__,
  he: __LABELS_HE__,
};

/* ── NÚMEROS (gerados; não traduzir) ────────────────────────────────── */
const SPEC: Spec = __SPEC__;

const KPIS: { id: string; valor: Num; params: Record<string, Num> }[] = __KPIS__;

export const PAINEIS: Record<string, { componente: string; datasets: string[]; params: Record<string, Num> }> = __PAINEIS__;

/** Datas do periodo: `fim` = data completa; `ini` = so o dia quando o mes e o ano sao os do fim e o locale escreve dia antes do mes. */
function dia(loc: Locale, p: DataPar): string {
  const ini = new Date(`${p.ini}T00:00:00Z`);
  const fim = new Date(`${p.fim}T00:00:00Z`);
  const L = INTL[loc];
  if (p.papel === 'fim') return new Intl.DateTimeFormat(L, { timeZone: 'UTC', dateStyle: 'long' }).format(fim);
  const f = new Intl.DateTimeFormat(L, { timeZone: 'UTC', day: 'numeric', month: 'long' });
  const partes = f.formatToParts(ini);
  const iDia = partes.findIndex((x) => x.type === 'day');
  const iMes = partes.findIndex((x) => x.type === 'month');
  const mesmoMes = ini.getUTCFullYear() === fim.getUTCFullYear() && ini.getUTCMonth() === fim.getUTCMonth();
  if (mesmoMes && iDia < iMes) return new Intl.NumberFormat(L).format(ini.getUTCDate());
  return f.format(ini);
}

function numero(loc: Locale, n: Num): string {
  if (typeof n === 'string') return n;
  if (typeof n === 'object' && 'papel' in n) return dia(loc, n);
  const v = typeof n === 'number' ? n : n[0];
  const d = typeof n === 'number' ? 0 : n[1];
  const sinal = typeof n !== 'number' && n.length > 2;
  return new Intl.NumberFormat(INTL[loc], {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
    signDisplay: sinal ? 'exceptZero' : 'auto',
  }).format(v);
}

function tx(loc: Locale, t: Tx, extra?: Record<string, string>): string {
  const tpl = LABELS[loc][t.k];
  if (tpl === undefined) throw new Error(`LABELS["${loc}"] sem a chave "${t.k}"`);
  return tpl.replace(/\{(\w+)\}/g, (_m: string, nome: string) => {
    if (extra && nome in extra) return extra[nome];
    const p = t.p?.[nome];
    if (p === undefined) throw new Error(`"${t.k}": falta o parâmetro {${nome}}`);
    return numero(loc, p);
  });
}

function ativo(loc: Locale): boolean {
  if (loc === 'pt-br') return true;
  if (Object.keys(LABELS[loc]).length === 0) return false;
  const falta = Object.keys(LABELS['pt-br']).filter((k) => !(k in LABELS[loc]));
  if (falta.length > 0) throw new Error(`LABELS["${loc}"] incompleto; faltam: ${falta.join(', ')}`);
  return true;
}

function montarBarras(loc: Locale): Record<string, CountryBarsDataset> {
  const out: Record<string, CountryBarsDataset> = {};
  for (const [id, ds] of Object.entries(SPEC.countryBars)) {
    out[id + SUFIXO[loc]] = {
      max: ds.max,
      groups: ds.groups.map((g) => ({
        label: tx(loc, g.label),
        color: g.color,
        items: g.items.map((i) => ({
          name: tx(loc, i.name),
          value: i.value,
          valueLabel: tx(loc, i.valueLabel),
          ...(i.emphasis ? { emphasis: true } : {}),
        })),
      })),
    };
  }
  return out;
}

function montarFunil(loc: Locale): Record<string, FunnelDataset> {
  const out: Record<string, FunnelDataset> = {};
  for (const [id, ds] of Object.entries(SPEC.funnel)) {
    out[id + SUFIXO[loc]] = {
      steps: ds.steps.map((s) => ({ label: tx(loc, s.label), sublabel: tx(loc, s.sublabel), color: s.color, value: s.value })),
    };
  }
  return out;
}

const ATIVOS = LOCALES.filter(ativo);
export const lgbtCountryBarsDatasets: Record<string, CountryBarsDataset> = Object.assign({}, ...ATIVOS.map(montarBarras));
export const lgbtFunnelDatasets: Record<string, FunnelDataset> = Object.assign({}, ...ATIVOS.map(montarFunil));

/** Faixa de KPIs (P0): vira tabela GFM no MDX; nao ha componente. */
export function lgbtKpis(loc: Locale): { id: string; label: string; valor: string; nota: string }[] {
  return KPIS.map((k) => ({
    id: k.id,
    label: tx(loc, { k: `kpi.${k.id}` }),
    valor: numero(loc, k.valor),
    nota: tx(loc, { k: `kpi.${k.id}.nota`, p: k.params }),
  }));
}

/** Props de texto do MDX por painel (title, subtitle, source, description, e `legenda` no p8). Descrição curta com os números-chave. */
export function lgbtLegendas(loc: Locale, painel: string): { title: string; subtitle: string; source: string; description: string; legenda?: string } {
  const meta = PAINEIS[painel];
  const t = (k: string) => tx(loc, { k: `${painel}.${k}`, p: meta.params });
  const out: { title: string; subtitle: string; source: string; description: string; legenda?: string } = {
    title: t('title'),
    subtitle: t('subtitle'),
    source: t('source'),
    description: t('desc'),
  };
  if (painel === 'p8') out.legenda = t('legenda');
  return out;
}
"""


def carregar_labels():
    """labels.<loc>.json (traducoes): mesmas chaves e mesmos {placeholders} do pt-br; qualquer divergencia derruba o build."""
    res = {"pt-br": LABELS_PT}
    for loc in ("en", "es", "it", "he"):
        f = os.path.join(OUT, f"labels.{loc}.json")
        with ler(f) as fh:
            j = json.load(fh)
        falta, sobra = sorted(set(LABELS_PT) - set(j)), sorted(set(j) - set(LABELS_PT))
        if falta or sobra:
            raise SystemExit(f"labels.{loc}.json: faltam {falta}; sobram {sobra}")
        for k_, v_ in j.items():
            if not isinstance(v_, str) or not v_.strip():
                raise SystemExit(f"labels.{loc}.json[{k_}] vazio ou nao-texto")
            if sorted(re.findall(r"\{\w+\}", v_)) != sorted(re.findall(r"\{\w+\}", LABELS_PT[k_])):
                raise SystemExit(f"labels.{loc}.json[{k_}]: placeholders diferentes do pt-br: {v_!r}")
        res[loc] = j
    return res


def gerar_ts(spec, c, par, labels):
    kp = [{"id": i, "valor": v, "params": p} for i, v, p in kpis_lista(c)]
    paineis = {p: {"componente": PAINEL_COMP[p], "datasets": PAINEL_DATASETS[p], "params": par[p]} for p in PAINEIS}
    t = TS_TEMPLATE
    j = lambda o: json.dumps(o, ensure_ascii=False, indent=2)  # noqa: E731
    # vetores de escalares numa linha so (NAO aplicar a LABELS: textos trazem colchetes)
    jc = lambda o: re.sub(r"\[\s+([^\[\]{}]*?)\s+\]", lambda m: "[" + re.sub(r"\s+", " ", m.group(1)) + "]", j(o))  # noqa: E731
    return t.replace("__LABELS__", j(LABELS_PT)).replace("__LABELS_EN__", j(labels["en"])).replace("__LABELS_ES__", j(labels["es"])).replace("__LABELS_IT__", j(labels["it"])).replace("__LABELS_HE__", j(labels["he"])).replace("__SPEC__", jc(spec)).replace("__KPIS__", jc(kp)).replace("__PAINEIS__", jc(paineis))


def rodar_node(ts_path):
    runner = (
        "const m = await import(process.argv[1]); const loc = {};"
        "for (const l of ['pt-br','en','es','it','he']) { const L = {};"
        " for (const p of ['p1','p2','p3','p4','p5','p6','p7','p8']) L[p] = m.lgbtLegendas(l, p);"
        " loc[l] = {legendas: L, kpis: m.lgbtKpis(l)}; }"
        "console.log(JSON.stringify({countryBars: m.lgbtCountryBarsDatasets, funnel: m.lgbtFunnelDatasets, loc}));"
    )
    r = subprocess.run([NODE, "--input-type=module", "-e", runner, ts_path], capture_output=True, text=True, cwd=OUT, timeout=60)
    if r.returncode != 0:
        raise SystemExit("node falhou:\n" + r.stderr)
    res = json.loads(r.stdout)
    res["legendas"], res["kpis"] = res["loc"]["pt-br"]["legendas"], res["loc"]["pt-br"]["kpis"]
    return res


LOCALES = ["pt-br", "en", "es", "it", "he"]
SUFIXO = {"pt-br": "", "en": "-en", "es": "-es", "it": "-it", "he": "-he"}


def conferir_locales_e_mdx(node, c):
    """(3) todo dataset existe nos 5 locales, com os MESMOS numeros; os MDX usam o componente e o id certos, na ordem dos paineis."""
    res = {"datasets_por_locale": {}, "mdx": {}, "avisos_kpi_no_mdx": []}

    def numeros(ds):  # estrutura sem texto: so valores, cores, max, emphasis
        if "groups" in ds:
            return [ds["max"]] + [(g["color"], [(i["value"], i.get("emphasis")) for i in g["items"]]) for g in ds["groups"]]
        return [(s_["color"], s_["value"]) for s_ in ds["steps"]]

    for p in PAINEIS:
        base = PAINEL_DATASETS[p][0]
        kind = "funnel" if p == "p3" else "countryBars"
        ref = numeros(node[kind][base])
        for loc in LOCALES:
            id_ = base + SUFIXO[loc]
            assert id_ in node[kind], f"dataset ausente: {id_}"
            assert numeros(node[kind][id_]) == ref, f"numeros divergem em {id_}"
    res["datasets_por_locale"] = {"ids": sum(len(v) for v in (node["countryBars"], node["funnel"])), "esperado": len(PAINEIS) * len(LOCALES)}
    assert res["datasets_por_locale"]["ids"] == res["datasets_por_locale"]["esperado"], res["datasets_por_locale"]
    mdx_dir = os.path.dirname(OUT)
    for loc in LOCALES:
        f = os.path.join(mdx_dir, f"index.{loc}.mdx")
        with ler(f) as fh:
            txt = fh.read()
        tags = re.findall(r"<(CountryBarsChart|FunnelChart)\s+(.*?)/>", txt, re.S)
        assert len(tags) == len(PAINEIS), (loc, len(tags))
        for (comp, attrs), p in zip(tags, PAINEIS):
            props = dict(re.findall(r'(\w+)="(.*?)"', attrs, re.S))
            assert comp == PAINEL_COMP[p], (loc, p, comp)
            assert props.get("dataset") == PAINEL_DATASETS[p][0] + SUFIXO[loc], (loc, p, props.get("dataset"))
            for k_ in ("title", "subtitle", "source", "description"):
                assert props.get(k_, "").strip(), (loc, p, "falta " + k_)
        res["mdx"][loc] = {"tags": len(tags), "ids_ok": True}
        for kp in node["loc"][loc]["kpis"]:  # avisos: valor do KPI nao aparece no texto do MDX
            if kp["id"] in ("fontes", "scripts", "pdfs", "textos", "obs") and kp["valor"] not in txt:
                res["avisos_kpi_no_mdx"].append([loc, kp["id"], kp["valor"]])
    return res


def typecheck(ts_path):
    """tsc --strict do proprio site (somente leitura) sobre copia em pasta temporaria do sistema; None se o tsc nao existir."""
    import shutil
    import tempfile
    tsc = os.environ.get("SITE_TSC", "")
    if not tsc or not SITE_TIPOS or not os.path.exists(tsc):
        return None
    with tempfile.TemporaryDirectory() as td:
        shutil.copy(SITE_TIPOS, os.path.join(td, "artigos-charts.ts"))
        shutil.copy(ts_path, os.path.join(td, "lgbt-violencia.data.ts"))
        r = subprocess.run([tsc, "--noEmit", "--strict", "--target", "ES2017", "--lib", "dom,esnext", "--module", "esnext", "--moduleResolution", "bundler",
                            "--skipLibCheck", "--isolatedModules", "lgbt-violencia.data.ts"], capture_output=True, text=True, cwd=td, timeout=240)
        return {"codigo": r.returncode, "saida": (r.stdout + r.stderr).strip()[:2000]}


def verificar_forma(node, spec):
    """Checagem de FORMA contra as interfaces do site (sem tsc: a pasta do site e somente leitura)."""
    erros = []
    for id_, ds in node["countryBars"].items():
        assert set(ds) == {"max", "groups"}, id_
        assert isinstance(ds["max"], (int, float)) and ds["max"] > 0
        for g in ds["groups"]:
            assert set(g) == {"label", "color", "items"} and isinstance(g["label"], str) and g["color"] in PALETA, (id_, g["color"])
            assert len(g["label"]) <= 60, ("rotulo de grupo longo", g["label"])
            for i in g["items"]:
                assert set(i) <= {"name", "value", "valueLabel", "emphasis"} and {"name", "value", "valueLabel"} <= set(i), i
                assert isinstance(i["name"], str) and isinstance(i["valueLabel"], str) and isinstance(i["value"], (int, float))
                assert 0 <= i["value"] <= ds["max"], (id_, i)
                if len(i["name"]) > 19:
                    erros.append(f"nome longo ({len(i['name'])}): {i['name']}")
                livre = 712 - (150 + i["value"] / ds["max"] * 506 + 8)
                if len(i["valueLabel"]) * 6.4 > livre:
                    erros.append(f"rotulo de valor pode vazar: {i['valueLabel']}")
    for id_, ds in node["funnel"].items():
        assert set(ds) == {"steps"}
        vals = [s["value"] for s in ds["steps"]]
        assert vals == sorted(vals, reverse=True), vals
        for s in ds["steps"]:
            assert set(s) == {"label", "sublabel", "color", "value"} and s["color"] in PALETA
    return erros


# ================================================================== 7. SPEC.md
def gerar_spec(c, node_leg, par, ext, erros, conf_loc):
    k = c["kpis"]
    f = c["funil"]
    nu = NUM["fontes_unicas"]["valor"]
    t = c["tipos"]
    lg = {p: node_leg[p] for p in PAINEIS}
    fp = lambda x, d=0: fmt_pt(x, d)  # noqa: E731
    L = []
    A = L.append
    A("# DASHBOARD-SPEC: abertura do artigo LGBT-INDICADOR")
    A("")
    A("Gerado por `dashboard/build_dashboard.py` (`/opt/homebrew/bin/python3.14 -I`, sem aleatoriedade, só leitura, SHA256SUMS ao lado). Números em `dashboard_dados.json`, com arquivo e comando de origem.")
    A("Reuso total: `CountryBarsChart` e `FunnelChart` do site; nenhum componente novo. Datasets em `lgbt-violencia.data.ts` (ids `lgbt-violencia-*`, sufixo `-en|-es|-it|-he`; textos em `LABELS`).")
    A("Insumos de texto: `labels.en.json`, `labels.es.json`, `labels.it.json`, `labels.he.json` (134 chaves cada, lidas pelo build; falta ou sobra de chave, ou {placeholder} diferente, derruba o build). Datas do período formatadas por locale com `Intl` no `.ts`.")
    A("")
    A("## Ordem no topo: P0 faixa de KPIs (tabela) -> P1 idiomas -> P2 tipos e períodos -> P3 funil -> P4 PNS -> P5 GGB -> P6 SIM -> P7 circulação -> P8 governos")
    A("")
    A("## P0 Faixa de KPIs (tabela GFM no MDX; `lgbtKpis(locale)`; sem componente)")
    A("| KPI | valor | como foi contado |")
    A("|---|---|---|")
    for kp in node_leg["_kpis"]:
        A(f"| {kp['label']} | {kp['valor']} | {kp['nota']} |")
    A("")
    for p in PAINEIS:
        titulo = lg[p]["title"]
        A(f"## {p.upper()} {titulo}")
        A(f"- {PAINEL_COMP[p]} · dataset `{PAINEL_DATASETS[p][0]}` · legenda: {lg[p]['subtitle']}. · fonte: {lg[p]['source']}")
        if p == "p8":
            A(f"- Legenda fixa: {lg['p8']['legenda']}")
            A(f"- Base declarada (lida de `dados/painel/c03_event_pesos_resultados.md`, seção 1): troca de {fp(c['governos']['k'])} pontos na escala do escore ({c['governos']['base']}); limite = 100[exp(k·limite do IC95% de b)−1], recalculado por script e igual ao impresso pela reanálise.")
    A("")
    A("## O que não deu para classificar / limites (contados)")
    A(f"- Tipo de fonte: {fp(t['nao_classificado'])} de {fp(nu)} ({fp(100*t['nao_classificado']/nu,1)}%) ficaram `Não classificado` (o ledger não tem campo de tipo; regra por canal, DOI e domínio no script). {fp(t['per_semq'])} periódicos sem quartil conferido: o quartil SJR só existe para {fp(c['quartil_n_fontes']['total_dois_com_quartil'])} DOIs (CSVs de verificação e tabelas dos dossiês).")
    A(f"- Período: {fp(c['faixas']['sem_ano'])} fontes sem ano. P2 junta tipo e período no mesmo gráfico (dois blocos, cada um soma {fp(nu)}).")
    A(f"- Funil: só artigos com DOI entram em \"texto integral lido\" ({fp(c['verif']['dois_verificados'])} DOIs verificados; {fp(c['verif']['dois_no_ledger'])} estão no ledger). Relatórios oficiais lidos em PDF não entram.")
    A(f"- KPI \"textos integrais lidos\" = {fp(k['textos_integrais'])} (todos os DOIs lidos); o funil mostra {fp(f['lido'])}, só os que constam no registro de fontes ({fp(k['textos_sem_registro'])} lidos não têm linha), porque o funil é aninhado. Q1 e usadas: {fp(c['funil_q1_so_contradito'])} só com veredito CONTRADITO.")
    A(f"- Idiomas: {fp(NUM['idiomas_ids_com_conflito']['valor'])} ids com idioma divergente entre registros; maioria decide, {fp(NUM['idiomas_empate_desfeito_pelo_consolidado']['valor'])} empates desfeitos pelo registro consolidado.")
    A(f"- P7: F3 (governo mata) é estimativa de amostra de {fp(c['discurso']['est_f3']['n'])} falas (IC95% de Wilson) e INDICATIVA: o segundo codificador (Grok) concorda pouco (κ de postura {fp(c['discurso']['kappa_postura']['F3'],2)}); em F2 κ = {fp(c['discurso']['kappa_postura']['F2'],2)}. F1, F2 e F4 foram todas lidas pelo codificador original.")
    A("- P8: `CountryBarsChart` não desenha barra negativa nem intervalo; dois blocos de barras positivas mostram a queda máxima e a alta máxima compatíveis com o IC95% (sinal no rótulo). Event study sobre trocas de governo: inconclusivo (reanálise C03).")
    A(f"- P5: numeradores N0 (total), N1 (homicídio + latrocínio) e N2 (N1 sem pessoas trans) de `dados/ggb/c08_numeradores.csv`, só 2023 e 2024 (2025 é proxy e fica fora); RR 2,82 e 3,84 mantidos; com esses RR a cobertura é no máximo {fp(c['ggb_max_rr_alto'],1)}%.")
    A("- Não usados: `WaffleChart` e `DailyColumnsChart` (nenhum painel pede). Se a regra de 8 painéis incluir a faixa P0, fundir P1 em P2 (datasets já separados).")
    A(f"- Conferência do título: contagem hoje = {fp(k['fontes'])} fontes (título: {fp(c['conferencia_titulo']['fontes_titulo'])}), {fp(k['scripts'])} scripts (título: {fp(c['conferencia_titulo']['scripts_titulo'])}; cresce com as frentes novas), {fp(k['idiomas'])} idiomas, {fp(k['revisores'])} revisores, {fp(k['dias'])} dias.")
    cd = c["conf_dossie"]
    A(f"- Tipo conferido contra o dossiê (§5.1 periódico, §5.2 oficial, §5.3 ONG): {fp(cd['conferidos'])} fontes presentes no registro, {fp(len(cd['divergencias']))} divergências; {fp(cd['sem_linha_no_registro'])} sem linha no registro.")
    A(f"- Locales: {fp(conf_loc['datasets_por_locale']['ids'])} datasets (8 painéis x 5 locales) com os mesmos números; os 5 `index.<locale>.mdx` têm 8 tags cada, com componente e id certos na ordem dos painéis. Avisos de KPI fora do texto do MDX: {fp(len(conf_loc['avisos_kpi_no_mdx']))}.")
    A("- Acessibilidade: cada gráfico tem `description` curta com os números-chave (`lgbtLegendas`); os valores completos estão nos rótulos das barras. Cores só da paleta do site. Tipos conferidos com o `tsc --strict` do próprio site (cópia temporária; pasta do site intocada) e forma conferida por script.")
    if erros:
        A(f"- Avisos de largura: {len(erros)} (ver `dashboard_dados.json` > verificacao_forma).")
    assert len(L) <= 80, len(L)
    return "\n".join(L) + "\n"


# ================================================================== 8. MAIN
def sha256_arquivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    c, regs, arqs = calcular()
    spec = montar_spec(c)
    labels = carregar_labels()
    ts = gerar_ts(spec, c, paineis_params(c), labels)
    ts_path = os.path.join(OUT, "lgbt-violencia.data.ts")
    with open(ts_path, "w", encoding="utf-8") as fh:
        fh.write(ts)
    node = rodar_node(ts_path)
    # 1) .ts (Intl, Node) == renderizacao independente em Python, em pt-br
    esperado_cb = {k: render_dataset_pt("countryBars", v) for k, v in spec["countryBars"].items()}
    esperado_fn = {k: render_dataset_pt("funnel", v) for k, v in spec["funnel"].items()}
    assert {k_: node["countryBars"][k_] for k_ in esperado_cb} == esperado_cb, "countryBars: .ts diverge do render Python"
    assert {k_: node["funnel"][k_] for k_ in esperado_fn} == esperado_fn, "funnel: .ts diverge do render Python"
    leg_py, par, ext = legendas_pt(spec, c)
    for p in PAINEIS:
        assert node["legendas"][p] == leg_py[p], (p, node["legendas"][p], leg_py[p])
    kp_py = [{"id": i, "label": LABELS_PT["kpi." + i], "valor": param_pt(v), "nota": fill_pt(LABELS_PT["kpi." + i + ".nota"], p)} for i, v, p in kpis_lista(c)]
    assert node["kpis"] == kp_py, "kpis divergem"
    erros = verificar_forma(node, spec)
    conf_loc = conferir_locales_e_mdx(node, c)
    tsc = typecheck(ts_path)
    assert tsc is None or tsc["codigo"] == 0, tsc
    node["legendas"]["_kpis"] = node["kpis"]
    spec_md = gerar_spec(c, node["legendas"], par, ext, erros, conf_loc)
    with open(os.path.join(OUT, "DASHBOARD-SPEC.md"), "w", encoding="utf-8") as fh:
        fh.write(spec_md)
    dados = {
        "versao": 1,
        "projeto": "LGBT-INDICADOR",
        "reproduzir": f"{PY} -I {OUT}/build_dashboard.py",
        "regras": {
            "fonte_unica": "id unico: DOI em minusculas; URL sem barra final, minuscula; URL doi.org dobrada em DOI; 17 sources.jsonl",
            "idioma": "pt e pt-BR fundidos; divergencia entre registros decidida pela maioria, empate pelo research-consolidado",
            "scripts": "*.py do projeto fora de fontes/ (material baixado) e fora de __pycache__",
            "numero_digitado": "nenhum para exibicao; asserts de teste comparam com as frases da reanalise (RESULTADOS.md) e do MIDIA.md",
        },
        "numeros": NUM,
        "paineis": {p: {"componente": PAINEL_COMP[p], "datasets": PAINEL_DATASETS[p], "ordem": i + 1} for i, p in enumerate(PAINEIS)},
        "datasets_ptbr": {"countryBars": esperado_cb, "funnel": esperado_fn},
        "legendas_ptbr": leg_py,
        "kpis_ptbr": kp_py,
        "verificacao_funil_dois": c["verif"],
        "quartil_cobertura": c["quartil_n_fontes"],
        "p8_base": {"k_pontos": c["governos"]["k"], "base_lida_do_cabecalho": c["governos"]["base"], "formula": "100*(exp(k*limite_IC95_de_b)-1)"},
        "locales": {"labels_json": [f"labels.{l_}.json" for l_ in ("en", "es", "it", "he")], "chaves_por_locale": len(LABELS_PT), **conf_loc},
        "conferencia_titulo": c["conferencia_titulo"],
        "verificacao_forma": {"ok": True, "avisos": erros, "tsc": ("tsc --strict do site, sobre copia em pasta temporaria: sem erros" if tsc else "nao rodado: tsc do site ausente")},
    }
    with open(os.path.join(OUT, "dashboard_dados.json"), "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")
    k = c["kpis"]
    kf = [("fontes únicas registradas", k["fontes"], "ids únicos nos 17 registros de fontes (DOI em minúsculas; URL sem barra final)"),
          ("scripts .py", k["scripts"], "arquivos .py do projeto, fora de fontes/ (material baixado) e de __pycache__"),
          ("idiomas", k["idiomas"], "códigos de idioma distintos das fontes únicas (pt e pt-BR somados)"),
          ("revisores hostis", k["revisores"], "arquivos revisao_*.md em escrutinio/"),
          ("dias", k["dias"], f"de {DATA_INI.isoformat()} a {DATA_FIM.isoformat()}, inclusive"),
          ("PDFs arquivados", k["pdfs"], "PDFs distintos por hash em fontes/"),
          ("textos integrais lidos", k["textos_integrais"], "DOIs com texto integral lido nos CSVs de verificação"),
          ("registros analisados", k["observacoes"], "óbitos SIM + notificações Sinan + falas varridas + itens codificados")]
    linhas_kf = ["# KPIs FINAIS (o título do artigo copia estes números)", "",
                 "Gerado por `build_dashboard.py`; congelado pelo `SHA256SUMS.txt`. Nova rodada sobre registros que mudaram dá outros números.", "",
                 "| KPI | valor | regra |", "|---|---|---|"] + [f"| {a} | {fmt_pt(b)} | {r} |" for a, b, r in kf]
    linhas_kf += ["", f"Título anterior: {c['conferencia_titulo']['fontes_titulo']} fontes, {c['conferencia_titulo']['scripts_titulo']} scripts, 10 idiomas, 4 revisores, 14 dias."]
    with open(os.path.join(OUT, "KPIS-FINAIS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas_kf) + "\n")
    print("KPIS FINAIS:", "; ".join(f"{a} = {fmt_pt(b)}" for a, b, _ in kf))
    # SHA256SUMS: entradas lidas + saidas
    pdfs = hashes_pdfs()
    linhas = []
    for pth in sorted(ENTRADAS):
        linhas.append((sha256_arquivo(pth), pth))
    for pth, h in sorted(pdfs.items()):
        linhas.append((h, pth))
    for nome in ("dashboard_dados.json", "lgbt-violencia.data.ts", "DASHBOARD-SPEC.md", "KPIS-FINAIS.md", "build_dashboard.py"):
        pth = os.path.join(OUT, nome)
        linhas.append((sha256_arquivo(pth), pth))
    with open(os.path.join(OUT, "SHA256SUMS.txt"), "w", encoding="utf-8") as fh:
        for h, pth in linhas:
            fh.write(f"{h}  {pth}\n")
    print("OK", len(linhas), "hashes; spec", spec_md.count("\n"), "linhas; avisos:", erros)


def hashes_pdfs():
    res = {}
    for root, _d, files in os.walk(P("fontes")):
        rel = os.path.relpath(root, P("fontes"))
        if rel.startswith(os.path.join("q1-textointegral", "discurso")):
            continue
        for f in files:
            if f.lower().endswith(".pdf"):
                pth = os.path.join(root, f)
                res[pth] = sha256_arquivo(pth)
    return res


if __name__ == "__main__":
    sys.exit(main())
