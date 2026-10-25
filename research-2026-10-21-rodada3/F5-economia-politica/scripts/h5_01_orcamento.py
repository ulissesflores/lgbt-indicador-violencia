"""H5 insumo: orçamento federal EXECUTADO por ação, IBGE e ações de informação/estatística de segurança pública.
Duas fontes oficiais SEM emenda entre elas (conceitos de valor diferem; NÃO somar nem emendar):
 (a) 2014-2025: Portal da Transparência/CGU, arquivo anual 'OrcamentoDespesa' (https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa/<ano>); colunas ORÇAMENTO INICIAL/ATUALIZADO/EMPENHADO/REALIZADO.
 (b) 2007-2013: SIOP/Ministério do Planejamento, dados abertos em RDF da LOA (https://www1.siop.planejamento.gov.br/downloads/rdf/loa<ano>.zip); valores Empenhado/Liquidado/Pago e Dotação Inicial/Projeto de Lei.
Filtro: unidade orçamentária cujo nome contém 'GEOGRAFIA E ESTAT' (IBGE) + (qualquer UO) ações cujo nome casa com VITIMIZ|SINESP|ESTATIST... em Segurança/Justiça. Zips guardados em dados/raw/orcamento (F5_CACHE sobrescreve); sha256 de cada zip em dados/h5_orcamento_hashes.txt.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h5_01_orcamento.py [cgu|rdf|tudo]"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, hashlib, io, os, re, subprocess, sys, zipfile, unicodedata
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
import os
SC = os.environ.get("F5_CACHE", f"{B}/dados/raw/orcamento")  # zips ficam na pasta do projeto (*.zip está no .gitignore); sobrevivem à sessão
os.makedirs(SC, exist_ok=True)
UA = "Mozilla/5.0 (research; seu-email@exemplo.org)"
def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
SEG = re.compile(r"VITIMIZ|SINESP|ESTATIST|PESQUISA|DIAGNOST|INFORMACOES (CRIMIN|DE SEGURANCA)|SISTEMA NACIONAL DE (INFORMA|ESTAT)")
def baixa(url, dest):
    if not os.path.exists(dest):
        subprocess.run(["curl", "-sSL", "-m", "400", "-A", UA, "-o", dest, url], check=True)
    h = hashlib.sha256(open(dest, "rb").read()).hexdigest(); return h
def num(s): return float(s.replace(".", "").replace(",", ".")) if s else 0.0
hashes, rows = [], []
modo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
if modo in ("cgu", "tudo"):
    for ano in range(2014, 2026):
        url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/orcamento-despesa/{ano}_OrcamentoDespesa.zip"
        z = f"{SC}/od{ano}.zip"; hashes.append(f"{baixa(url, z)}  {url}")
        with zipfile.ZipFile(z) as zf:
            nome = zf.namelist()[0]
            rd = csv.reader(io.TextIOWrapper(zf.open(nome), encoding="latin-1"), delimiter=";")
            hdr = next(rd); ix = {h.strip(): i for i, h in enumerate(hdr)}
            for r in rd:
                uo = norm(r[ix["NOME UNIDADE ORÇAMENTÁRIA"]]); ac = norm(r[ix["NOME AÇÃO"]])
                ibge = "GEOGRAFIA E ESTAT" in uo
                if ibge or (SEG.search(ac) and re.search(r"JUSTICA|SEGURANCA|MINISTERIO DA JUSTICA|DIREITOS HUMANOS|CONSELHO NACIONAL DE JUSTICA", uo + " " + norm(r[ix["NOME ÓRGÃO SUPERIOR"]]))):
                    rows.append(dict(fonte="CGU-OrcamentoDespesa", ano=ano, uo_cod=r[ix["CÓDIGO UNIDADE ORÇAMENTÁRIA"]], uo=r[ix["NOME UNIDADE ORÇAMENTÁRIA"]], acao_cod=r[ix["CÓDIGO AÇÃO"]], acao=r[ix["NOME AÇÃO"]],
                                     grupo_despesa=r[ix["NOME GRUPO DE DESPESA"]], inicial=num(r[ix["ORÇAMENTO INICIAL (R$)"]]), atualizado=num(r[ix["ORÇAMENTO ATUALIZADO (R$)"]]),
                                     empenhado=num(r[ix["ORÇAMENTO EMPENHADO (R$)"]]), liquidado_ou_realizado=num(r[ix["ORÇAMENTO REALIZADO (R$)"]]), pago=""))
if modo in ("rdf", "tudo"):
    P = lambda s: f"<http://vocab.e.gov.br/2013/09/loa#{s}>"
    LIT = re.compile(r'^<([^>]+)> <([^>]+)> (?:<([^>]+)>|"((?:[^"\\]|\\.)*)"(?:\^\^<[^>]+>)?) \.$')
    for ano in range(2007, 2014):
        url = f"https://www1.siop.planejamento.gov.br/downloads/rdf/loa{ano}.zip"
        z = f"{SC}/loa{ano}.zip"; hashes.append(f"{baixa(url, z)}  {url}")
        lab, it = {}, {}
        with zipfile.ZipFile(z) as zf:
            nt = next(n for n in zf.namelist() if n.endswith(".nt"))
            for line in io.TextIOWrapper(zf.open(nt), encoding="utf-8", errors="replace"):
                m = LIT.match(line.rstrip("\n"))
                if not m: continue
                s, p, o_uri, o_lit = m.groups(); p = p.rsplit("#", 1)[-1]
                if p == "label": lab[s] = o_lit
                elif p in ("temUnidadeOrcamentaria", "temAcao", "temGND"): it.setdefault(s, {})[p] = o_uri
                elif p in ("valorEmpenhado", "valorLiquidado", "valorPago", "valorDotacaoInicial", "valorProjetoLei", "valorLeiMaisCredito"): it.setdefault(s, {})[p] = float(o_lit)
        agg = {}
        for s, d in it.items():
            if "temAcao" not in d: continue
            uo = lab.get(d.get("temUnidadeOrcamentaria"), ""); ac = lab.get(d["temAcao"], d["temAcao"].rsplit("/", 1)[-1]); orgao = ""
            ibge = "GEOGRAFIA E ESTAT" in norm(uo)
            if not (ibge or (SEG.search(norm(ac)) and re.search(r"JUSTICA|SEGURANCA|DIREITOS HUMANOS", norm(uo)))): continue
            k = (d.get("temUnidadeOrcamentaria", "").rsplit("/", 1)[-1], uo, d["temAcao"].rsplit("/", 1)[-1], ac)
            a = agg.setdefault(k, dict(inicial=0.0, atualizado=0.0, empenhado=0.0, liq=0.0, pago=0.0))
            a["inicial"] += d.get("valorDotacaoInicial", 0.0); a["atualizado"] += d.get("valorDotacaoInicial", 0.0) + d.get("valorLeiMaisCredito", 0.0)
            a["empenhado"] += d.get("valorEmpenhado", 0.0); a["liq"] += d.get("valorLiquidado", 0.0); a["pago"] += d.get("valorPago", 0.0)
        for (uc, uo, ac_c, ac), a in agg.items():
            rows.append(dict(fonte="SIOP-RDF-LOA", ano=ano, uo_cod=uc, uo=uo, acao_cod=ac_c, acao=ac, grupo_despesa="(todos)", inicial=a["inicial"], atualizado=a["atualizado"],
                             empenhado=a["empenhado"], liquidado_ou_realizado=a["liq"], pago=a["pago"]))
        print(ano, "ok", len(agg), "acoes", flush=True)
out = f"{B}/dados/h5_orcamento_acoes.csv" if modo == "tudo" else f"{B}/dados/h5_orcamento_acoes_{modo}.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
open(f"{B}/dados/h5_orcamento_hashes_{modo}.txt", "w").write("\n".join(hashes) + "\n"); print(len(rows), "linhas ->", out)
