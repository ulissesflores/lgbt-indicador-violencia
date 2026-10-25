"""H5: séries de execução orçamentária (empenhado) das ações que sustentam (ou deveriam sustentar) a medição de violência/vitimização, em R$ nominais e em R$ de dez/2025 (IPCA SIDRA 1737, número-índice de dezembro de cada ano).
CGU 2014-2025 e SIOP-RDF 2007-2013 NÃO se emendam (fontes e conceitos de valor diferentes); a série é cortada em 2013/2014 na tabela. Ações-chave escolhidas ANTES de olhar os valores pelo critério: IBGE (pesquisas/censos) + ações cujo nome é de informação/pesquisa sobre segurança, direitos humanos ou LGBT.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h5_02_series_chave.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import json, unicodedata, pandas as pd, numpy as np
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
d = pd.read_csv(f"{B}/dados/h5_orcamento_acoes.csv")
ip = {int(x["D3C"][:4]): float(x["V"]) for x in json.load(open(f"{B}/dados/raw/sidra1737_ipca_indice.json"))[1:] if x["D3C"].endswith("12")}
f = {a: ip[2025] / ip[a] for a in range(2007, 2026)}
d["empenhado_real_dez2025"] = d.empenhado * d.ano.map(f)
sem = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().upper()
d["uo"] = d.uo.map(sem); d["acao"] = d.acao.map(sem)
up = d.uo; ac = d.acao
chave = (up.str.contains("GEOGRAFIA") & ac.str.contains("PESQUISAS E ESTUDOS ESTAT|CENSO")) \
      | (ac.str.contains("NUCLEOS DE PESQUISA SOBRE CIDADANIA HOMOSSEXUAL")) | ac.str.contains("SISTEMA NACIONAL DE GESTAO DO CONHECIMENTO E DE INFORMACOES CRIMINAIS|REDE DE INTEGRACAO NACIONAL DE INFORMACOES DE SEGURANCA|IMPLANTACAO DO SISTEMA NACIONAL DE GESTAO DO CONHECIMENTO") \
      | ac.str.contains("SISTEMA NACIONAL DE INFORMACOES EM DIREITOS HUMANOS|DESENVOLVIMENTO DE ESTUDOS, PESQUISAS E INDICADORES EM DIREITOS HUMANOS|PRODUCAO E DISSEMINACAO DE INFORMACOES, ESTUDOS E PESQUISAS") \
      | (ac.str.contains("ESTATISTICA E PESQUISA NO PODER JUDICIARIO"))
k = d[chave].copy()
def cat(r):
    u, a = r.uo.upper(), r.acao.upper()
    if "GEOGRAFIA" in u: return "IBGE: pesquisas e estudos estatisticos (acao 20U6 em 2014+)" if "PESQUISAS E ESTUDOS ESTAT" in a else "IBGE: censos (acao 20U7 em 2014+; Censo 2006/2010 nos anos RDF)"
    if "NUCLEOS DE PESQUISA SOBRE CIDADANIA HOMOSSEXUAL" in a: return "SEDH: Nucleos de pesquisa sobre cidadania homossexual e combate a homofobia (8810)"
    if "INFORMACOES CRIMINAIS" in a or "REDE DE INTEGRACAO NACIONAL" in a: return "FNSP: sistema/rede nacional de informacoes criminais e de seguranca (8994, 2C56, 5000)"
    if "DIREITOS HUMANOS" in a and ("SISTEMA NACIONAL" in a or "INDICADORES" in a): return "SEDH/MDH: sistema nacional de informacoes e indicadores em direitos humanos (4904, 8942)"
    if "PODER JUDICIARIO" in a: return "CNJ: estatistica e pesquisa no Judiciario (2B66)"
    if "PRODUCAO E DISSEMINACAO DE INFORMACOES" in a: return "MJ: producao e disseminacao de informacoes, estudos e pesquisas (8198)"
    return "outra"
k["categoria"] = k.apply(cat, axis=1)
t = k.groupby(["categoria", "fonte", "ano"])[["empenhado", "empenhado_real_dez2025"]].sum().reset_index()
t.to_csv(f"{B}/dados/h5_series_chave_acoes.csv", index=False)
pd.set_option("display.width", 330); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 70)
for col, nome in (("empenhado", "NOMINAL R$ milhoes"), ("empenhado_real_dez2025", "REAL dez/2025 R$ milhoes")):
    piv = (t.pivot_table(index=["categoria"], columns="ano", values=col, aggfunc="sum") / 1e6).round(2); print(nome); print(piv.to_string())
