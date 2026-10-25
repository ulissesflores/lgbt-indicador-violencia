"""Séries UF x ano de óbitos por agressão (CID X85-Y09) e população, a partir do TabNet/DATASUS e do IBGE SIDRA.

Rotas (todas por HTTP, sem navegador):
- SIM (óbitos residentes): POST em tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10uf.def (formulário baixado).
- População por sexo: POST em tabcgi.exe?ibge/cnv/popuf.def (arquivos só até 2012 no servidor).
- População total: SIDRA 6579 (2011-2021, 2024-2025), 1378 (Censo 2010), 9514 (Censo 2022). 2023 não publicado nas tabelas testadas.

Brutos em fontes/p2-f8-dados-uf/tabnet/raw/. Saída: dados/atlas_uf_series.csv (nome herdado do plano; NÃO é o Atlas).
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, datetime, hashlib, html, io, json, os, re, subprocess, sys, urllib.parse

BASE = REPO_ROOT
RAW = os.path.join(BASE, "fontes/p2-f8-dados-uf/tabnet/raw")
OUT = os.path.join(BASE, "dados/atlas_uf_series.csv")
SIM_CGI = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10uf.def"
SIM_FORM = "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sim/cnv/ext10uf.def"
POP_CGI = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?ibge/cnv/popuf.def"
POP_FORM = "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?ibge/cnv/popuf.def"
SIDRA = {
    6579: "https://apisidra.ibge.gov.br/values/t/6579/n3/all/v/9324/p/2011-2025",
    1378: "https://apisidra.ibge.gov.br/values/t/1378/n3/all/v/93/p/2010",
    9514: "https://apisidra.ibge.gov.br/values/t/9514/n3/all/v/93/p/2022",
}
ANOS = list(range(2010, 2026))  # 2026 e parcial (2a previa): fora
DL = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

GRANDE_AGRESSOES = "4"                       # X85-Y09
SEXO_FEM = "2"
COR = {"preta": "2", "parda": "4", "branca": "1", "amarela": "3", "indigena": "5"}
CAT_ARMA = ["276", "277", "278"]             # X93, X94, X95 (disparo de arma de fogo)


def curl_to(url, path, data=None):
    os.makedirs(RAW, exist_ok=True)
    cmd = ["curl", "-sS", "-m", "150", "-o", path, "-w", "%{http_code}"]
    if data is not None:
        cmd += ["-X", "POST", "--data", data]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip() != "200":
        raise SystemExit(f"HTTP {r.stdout} em {url}: {r.stderr[:200]}")
    return path


def tabnet(cgi, tag, pares):
    body = urllib.parse.urlencode(pares, encoding="latin-1")
    path = curl_to(cgi, os.path.join(RAW, tag + ".prn"), body)
    return open(path, "rb").read().decode("latin1")


def parse_prn(txt):
    """{(codigo_uf, nome): {ano: int|None}} a partir do bloco 'Unidade da Federação';"2010";...;"Total".
    '-' no TabNet = zero não arredondado (legenda do próprio arquivo) -> 0."""
    header, rows = None, {}
    for rec in csv.reader(io.StringIO(txt), delimiter=";", quotechar='"'):
        if not rec:
            continue
        first = html.unescape(rec[0]).strip()
        if first.startswith("Unidade da Federação"):
            header = [html.unescape(h).strip() for h in rec]
            continue
        if header is None or first == "Total":
            continue
        m = re.match(r"^(\d{2}) (.+)$", first)
        if not m:
            continue
        vals = {}
        for h, v in zip(header[1:], rec[1:]):
            if h.isdigit():
                v = v.strip()
                vals[int(h)] = 0 if v == "-" else (int(v) if v.isdigit() else None)
        rows[(m.group(1), m.group(2))] = vals
    return rows


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def sim(tag, extra):
    pares = [("Linha", "Unidade_da_Federação"), ("Coluna", "Ano_do_Óbito"),
             ("Incremento", "Óbitos_p/Residênc"), ("formato", "prn"), ("mostre", "Mostra")]
    pares += [("Arquivos", f"extuf{str(a)[2:]}.dbf") for a in ANOS] + extra
    return parse_prn(tabnet(SIM_CGI, tag, pares)), os.path.join(RAW, tag + ".prn")


def popuf_feminino():
    # o popuf.def do servidor só tem arquivos até 2012
    pares = [("Linha", "Unidade_da_Federação"), ("Coluna", "Ano"), ("Incremento", "População_residente"), ("formato", "prn"),
             ("mostre", "Mostra"), ("SSexo", SEXO_FEM)]
    pares += [("Arquivos", f"popuf{str(a)[2:]}.dbf") for a in ANOS if a <= 2012]
    return parse_prn(tabnet(POP_CGI, "pop_feminino", pares)), os.path.join(RAW, "pop_feminino.prn")


def populacao_total():
    """{codigo_uf: {ano: pop}} e {ano: url da fonte}."""
    pop, fonte = {}, {}
    for chave, url in SIDRA.items():
        path = curl_to(url, os.path.join(RAW, f"sidra_{chave}.json"))
        for x in json.load(open(path, encoding="utf-8"))[1:]:
            try:
                v = int(x["V"])
            except (TypeError, ValueError):
                continue
            ano = int(x["D3N"])
            pop.setdefault(x["D1C"], {})[ano] = v
            fonte[ano] = url
    return pop, fonte


def main():
    n = {}
    consultas = {
        "n_homicidios_total": ("sim_total", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES)]),
        "n_homicidios_mulheres": ("sim_mulheres", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SSexo", SEXO_FEM)]),
        "n_preta": ("sim_preta", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SCor/raça", COR["preta"])]),
        "n_parda": ("sim_parda", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SCor/raça", COR["parda"])]),
        "n_branca": ("sim_branca", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SCor/raça", COR["branca"])]),
        "n_amarela": ("sim_amarela", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SCor/raça", COR["amarela"])]),
        "n_indigena": ("sim_indigena", [("SGrande_Grupo_CID10", GRANDE_AGRESSOES), ("SCor/raça", COR["indigena"])]),
        "n_arma_fogo": ("sim_armafogo", [("SCategoria_CID10", c) for c in CAT_ARMA]),
    }
    raw = {}
    for var, (tag, extra) in consultas.items():
        n[var], raw[tag] = sim(tag, extra)
        print(tag, "UFs:", len(n[var]), file=sys.stderr)
    pf, raw["pop_feminino"] = popuf_feminino()
    pt, fonte_pop = populacao_total()
    print("pop_total UFs:", len(pt), "| pop_feminino UFs:", len(pf), file=sys.stderr)

    pf_by_code = {k[0]: v for k, v in pf.items()}
    ufs = sorted(n["n_homicidios_total"].keys())
    out = []

    def add(uf, ano, var, valor, unid, url, status):
        out.append({"uf": uf[1], "codigo_uf": uf[0], "ano": ano, "variavel": var,
                    "valor": "" if valor is None else valor, "unidade": unid,
                    "fonte_url": url, "data_download": DL, "status_dado": status})

    for uf in ufs:
        cod = uf[0]
        for ano in ANOS:
            st = "preliminar" if ano == 2025 else "final"
            ntot = n["n_homicidios_total"][uf].get(ano)
            pop_t = pt.get(cod, {}).get(ano)
            pop_f = pf_by_code.get(cod, {}).get(ano)
            url_pop = (fonte_pop.get(ano, "") + " ; " + POP_FORM) if pop_t else ""
            add(uf, ano, "homicidios_total_n", ntot, "casos", SIM_FORM, st)
            add(uf, ano, "homicidios_total_taxa", round(ntot / pop_t * 1e5, 3) if ntot is not None and pop_t else None,
                "por 100 mil hab", SIM_FORM + " ; " + url_pop, st)
            nm = n["n_homicidios_mulheres"][uf].get(ano)
            add(uf, ano, "homicidios_mulheres_n", nm, "casos", SIM_FORM, st)
            add(uf, ano, "homicidios_mulheres_taxa", round(nm / pop_f * 1e5, 3) if nm is not None and pop_f else None,
                "por 100 mil mulheres", SIM_FORM + " ; " + POP_FORM, st)
            p = [n["n_preta"][uf].get(ano), n["n_parda"][uf].get(ano)]
            add(uf, ano, "homicidios_negros_n", sum(p) if None not in p else None, "casos (preta+parda)", SIM_FORM, st)
            p = [n["n_branca"][uf].get(ano), n["n_amarela"][uf].get(ano), n["n_indigena"][uf].get(ano)]
            add(uf, ano, "homicidios_nao_negros_n", sum(p) if None not in p else None,
                "casos (branca+amarela+indigena)", SIM_FORM, st)
            na = n["n_arma_fogo"][uf].get(ano)
            add(uf, ano, "homicidios_arma_fogo_n", na, "casos", SIM_FORM, st)
            add(uf, ano, "homicidios_arma_fogo_taxa", round(na / pop_t * 1e5, 3) if na is not None and pop_t else None,
                "por 100 mil hab", SIM_FORM + " ; " + url_pop, st)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["uf", "codigo_uf", "ano", "variavel", "valor", "unidade",
                                          "fonte_url", "data_download", "status_dado"])
        w.writeheader()
        w.writerows(out)
    print("linhas:", len(out), "| ufs:", len(ufs))
    for tag, path in sorted(raw.items()):
        print("RAW", tag, sha256(path), path)


if __name__ == "__main__":
    main()
