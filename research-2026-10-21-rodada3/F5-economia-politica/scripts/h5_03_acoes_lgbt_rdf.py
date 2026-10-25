"""H5: ações LGBT/homofobia/vitimização em QUALQUER unidade orçamentária, LOA em RDF (SIOP) 2007-2013 (zips baixados por h5_01 em dados/raw/orcamento), valores empenhado/liquidado/pago.
Complementa h5_01 (que filtra por unidade) para a pergunta 'existiu linha orçamentária específica?'. Saída: dados/h5_acoes_lgbt_rdf_2007_2013.csv.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h5_03_acoes_lgbt_rdf.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, io, re, unicodedata, zipfile
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
import os
SC = os.environ.get("F5_CACHE", f"{B}/dados/raw/orcamento")  # zips ficam na pasta do projeto (*.zip está no .gitignore); sobrevivem à sessão
sem = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().upper()
PAT = re.compile(r"LGBT|HOMOSSEX|HOMOFOB|DIVERSIDADE SEXUAL|TRAVEST|TRANSEXUAL|VITIMIZ|DISCRIMINACAO|PROMOCAO DOS DIREITOS HUMANOS|DISQUE")
LIT = re.compile(r'^<([^>]+)> <([^>]+)> (?:<([^>]+)>|"((?:[^"\\]|\\.)*)"(?:\^\^<[^>]+>)?) \.$')
rows = []
for ano in range(2007, 2014):
    lab, it = {}, {}
    with zipfile.ZipFile(f"{SC}/loa{ano}.zip") as zf:
        nt = next(n for n in zf.namelist() if n.endswith(".nt"))
        for line in io.TextIOWrapper(zf.open(nt), encoding="utf-8", errors="replace"):
            m = LIT.match(line.rstrip("\n"))
            if not m: continue
            s, p, ou, ol = m.groups(); p = p.rsplit("#", 1)[-1]
            if p == "label": lab[s] = ol
            elif p in ("temUnidadeOrcamentaria", "temAcao"): it.setdefault(s, {})[p] = ou
            elif p in ("valorEmpenhado", "valorLiquidado", "valorPago", "valorDotacaoInicial", "valorLeiMaisCredito"): it.setdefault(s, {})[p] = float(ol)
    agg = {}
    for s, d in it.items():
        if "temAcao" not in d: continue
        ac = lab.get(d["temAcao"], ""); 
        if not PAT.search(sem(ac)): continue
        k = (lab.get(d.get("temUnidadeOrcamentaria"), ""), d["temAcao"].rsplit("/", 1)[-1], ac); a = agg.setdefault(k, [0.0] * 4)
        a[0] += d.get("valorDotacaoInicial", 0.0) + d.get("valorLeiMaisCredito", 0.0); a[1] += d.get("valorEmpenhado", 0.0); a[2] += d.get("valorLiquidado", 0.0); a[3] += d.get("valorPago", 0.0)
    for (uo, c, ac), a in agg.items(): rows.append(dict(ano=ano, uo=uo, acao_cod=c, acao=ac, dotacao_atualizada=a[0], empenhado=a[1], liquidado=a[2], pago=a[3]))
    print(ano, len(agg), flush=True)
with open(f"{B}/dados/h5_acoes_lgbt_rdf_2007_2013.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("FIM", len(rows))
