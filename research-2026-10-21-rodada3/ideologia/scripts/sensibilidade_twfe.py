#!/opt/homebrew/bin/python3.14
"""Sensibilidade do TWFE do painel F8 a safra do escore de ideologia. NAO altera o painel: le os desfechos de dados/painel/painel_uf_ano*.csv
e as variantes de ideologia de impacto_painel_{wiki,tse}.csv (gerado por build_ideologia.py). TWFE copiado de dados/painel/painel_f8.py (mesma funcao).
Rodar: /opt/homebrew/bin/python3.14 -I scripts/sensibilidade_twfe.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, math, numpy as np
R = REPO_ROOT; H = f"{R}/research-2026-10-21-rodada3/ideologia"
def twfe(y, x, uf, ano):
    y=np.array(y,float); x=np.array(x,float); uf=np.array(uf); ano=np.array(ano)
    def demean(v):
        v=v.copy()
        for _ in range(50):
            for g in (uf,ano):
                for k in np.unique(g): v[g==k]-=v[g==k].mean()
        return v
    yd, xd = demean(y), demean(x)
    b=(xd@yd)/(xd@xd); e=yd-b*xd
    S=sum((xd[uf==k]@e[uf==k])**2 for k in np.unique(uf)); G=len(np.unique(uf)); n=len(y); k=1+G+len(np.unique(ano))-1
    se=math.sqrt(S/(xd@xd)**2 * G/(G-1)*(n-1)/(n-k))
    return b, se, n
VARS = [('ideo_painel_atual', 'atual (BRC 2018 p/ todos os anos)'), ('ideo_BRC_periodo', 'BRC por periodo (<=2020 onda 2018; >=2021 onda 2022)'),
        ('ideo_BLS_periodo_0_10', 'BLS por legislatura (0-10)'), ('ideo_media_BRC_BLS', 'media BRC periodo e BLS (0-10)'),
        ('ideo_BRC_2022_todos', 'BRC onda 2022 p/ todos os anos (limite oposto ao atual)'), ('esq_share', 'binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala)')]
OUTS = ['tx_total', 'tx_homens', 'tx_mulheres', 'tx_negros', 'tx_nao_negros', 'tx_arma']
md = ["# Sensibilidade do TWFE (painel F8) a safra do escore de ideologia\n",
      "Mesmo modelo do painel (log(taxa) ~ ideologia + EF UF + EF ano, EP agrupado por UF); so muda a coluna de ideologia. Gerado por scripts/sensibilidade_twfe.py. O painel NAO foi alterado.\n"]
for modo in ('wiki', 'tse'):
    P = {(r['uf'], int(r['ano'])): r for r in csv.DictReader(open(f"{R}/dados/painel/painel_uf_ano{'_tse' if modo=='tse' else ''}.csv"))}
    I = {(r['uf'], int(r['ano'])): r for r in csv.DictReader(open(f"{H}/impacto_painel_{modo}.csv"))}
    md += [f"\n## Variante de partido: {modo} ({'partido em exercicio, Wikipedia curada' if modo=='wiki' else 'partido pelo qual foi eleito, TSE'})\n",
           "| desfecho | variante de ideologia | n | b por ponto | EP | IC95% |", "|---|---|---|---|---|---|"]
    for col in OUTS:
        for v, lab in VARS:
            sel = [(k, p) for k, p in P.items() if float(p[col]) > 0 and I[k][v] != '']
            b, se, n = twfe([math.log(float(p[col])) for k, p in sel], [float(I[k][v]) for k, p in sel], [k[0] for k, p in sel], [k[1] for k, p in sel])
            md.append(f"| {col} | {lab} | {n} | {b:+.4f} | {se:.4f} | [{b-1.96*se:+.3f}, {b+1.96*se:+.3f}] |")
    # variacao intra-UF: quanto da ideologia varia dentro da UF (fonte da identificacao)
    import collections
    for v, lab in VARS[:2]:
        bu = collections.defaultdict(list)
        for k, r in I.items():
            if r[v] != '': bu[k[0]].append(float(r[v]))
        dentro = sum(sum((x - sum(a)/len(a))**2 for x in a) for a in bu.values()); tot_mean = sum(sum(a) for a in bu.values()) / sum(len(a) for a in bu.values())
        total = sum(sum((x - tot_mean)**2 for x in a) for a in bu.values())
        md.append(f"\nVariancia intra-UF / total de `{v}` ({modo}): {dentro/total:.3f}")
open(f"{H}/sensibilidade_twfe.md", "w").write("\n".join(md) + "\n"); print("\n".join(md))
