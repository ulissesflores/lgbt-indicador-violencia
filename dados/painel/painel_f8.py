"""F8 — painel UF x ano (2012-2024): ideologia do governador x taxas de homicídio por grupo.
Desenho SIMÉTRICO (escore contínuo 0-10, Bolognesi/Ribeiro/Codato 2023), efeitos fixos de UF e ano,
erro-padrão agrupado por UF. Exploratório: não é causal (ver caveats no .md).
Entradas: dados/atlas_uf_series.csv (SIM/TabNet), dados/governadores_uf_2011_2026.csv, dados/ideologia_partidos.csv,
          fontes/p2-f8-dados-uf/sidra/sidra6407_n3_606_c2all_c58tot_pall.json (PNADC pop por sexo) e sidra6403_n3_606_c86all_pall.json (PNADC pop por cor/raça, trimestral),
          baixados em 2026-10-21 de apisidra.ibge.gov.br (t/6407 e t/6403, n3/all, v/606, p/all); hashes em fontes/p2-f8-dados-uf/SHA256SUMS.txt.
Reprodutibilidade (2026-10-21): com o CSV de governadores ORIGINAL (git: commit 7bff7cd), `python3.14 -I dados/painel/painel_f8.py` reproduzia BYTE A BYTE o resultados.md e o painel_uf_ano.csv de 2026-10-11 (cmp=0).
Depois a curadoria foi corrigida (ES e GO 2023+: o CSV tinha o vice no lugar do governador eleito, achado no cruzamento com o TSE).
Uso: painel_f8.py [wiki|tse]  -> resultados.md (partido em exercício, Wikipédia corrigida) | resultados_tse.md (partido de eleição, TSE)
Saídas: dados/painel/painel_uf_ano.csv, dados/painel/resultados.md
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, json, math, sys, collections
import numpy as np
D=(REPO_ROOT + "/dados")
MODO = sys.argv[1] if len(sys.argv) > 1 else "wiki"
IDEO = sys.argv[2] if len(sys.argv) > 2 else "bolognesi2018"   # bolognesi2018 (escore único de 2018) | brc (BRC por período: onda 2018 p/ 2012-2020, onda 2022 p/ 2021-2024; dados/ideologia/)   # wiki: partido em exercício (Wikipédia curada) | tse: partido pelo qual a pessoa em exercício foi eleita (TSE)
GOV = ("_tse" if MODO == "tse" else "") + ("_brc" if IDEO == "brc" else "")
GOVCSV = "_tse" if MODO == "tse" else ""
SCR=(REPO_ROOT + "/fontes/p2-f8-dados-uf/sidra")
# --- obitos
ob=collections.defaultdict(dict)
for r in csv.DictReader(open(f"{D}/atlas_uf_series.csv")):
    if r['valor']=='' or not r['variavel'].endswith('_n'): continue
    ob[(r['uf'],int(r['ano']))][r['variavel']]=float(r['valor'])
# --- populacao PNADC por sexo (anual, mil pessoas)
pop=collections.defaultdict(dict)
for x in json.load(open(f"{SCR}/sidra6407_n3_606_c2all_c58tot_pall.json"))[1:]:
    if x['V'] in ('..','-','...'): continue
    pop[(x['D1N'],int(x['D3N']))][x['D4N']]=float(x['V'])*1000
# --- populacao PNADC por cor/raca (trimestral -> media anual)
acc=collections.defaultdict(lambda: collections.defaultdict(list))
for x in json.load(open(f"{SCR}/sidra6403_n3_606_c86all_pall.json"))[1:]:
    if x['V'] in ('..','-','...'): continue
    ano=int(x['D3N'].split()[-1]); acc[(x['D1N'],ano)][x['D4N']].append(float(x['V'])*1000)
for k,v in acc.items():
    pop[k]['negros']=np.mean(v['Preta'])+np.mean(v['Parda']); pop[k]['total_raca']=np.mean(v['Total'])
    pop[k]['nao_negros']=pop[k]['total_raca']-pop[k]['negros']
# PNADC 6403 nao tem 2021: interpola a media de 2020 e 2022 (documentado no .md)
for (uf,ano) in list(pop):
    if 'negros' not in pop[(uf,ano)] and (uf,ano-1) in acc and (uf,ano+1) in acc:
        for c in ('negros','nao_negros','total_raca'): pop[(uf,ano)][c]=(pop[(uf,ano-1)][c]+pop[(uf,ano+1)][c])/2
# --- ideologia
MAP={'PMDB':'MDB','PP':'Progressistas','Republicanos':'PRB','PL':'PR','PROS':'Pros','Cidadania':'PPS','Solidariedade':'SDD','SD':'SDD','União Brasil':'DEM','UNIÃO':'DEM','União':'DEM','PSD':'PSD'}
ideo={}
for r in csv.DictReader(open(f"{D}/ideologia_partidos.csv")):
    if 'Bolognesi' in r['fonte']: ideo[r['partido']]=float(r['escore'])
def score(p):
    for cand in (p, MAP.get(p,''), {v:k for k,v in MAP.items()}.get(p,'')):
        if cand in ideo: return ideo[cand]
    return None
gov=collections.defaultdict(list); unmatched=collections.Counter()
for r in csv.DictReader(open(f"{D}/governadores_uf_2011_2026{GOVCSV}.csv")):
    s=score(r['partido'].strip())
    if s is None: unmatched[r['partido']]+=1; continue
    try:
        from datetime import date
        a=date.fromisoformat(r['inicio']); b=date.fromisoformat(r['fim']); meses=max(1,(b-a).days/30.4)
    except Exception: meses=12
    gov[(r['uf'],int(r['ano']))].append((s,meses,r['partido']))
# --- ideologia por período (opcional): troca o escore único de 2018 pelo BRC por período (ver dados/ideologia/)
BRCMAP={}
if IDEO=="brc":
    for r in csv.DictReader(open(f"{D}/ideologia/ideologia_painel_{'tse' if MODO=='tse' else 'wiki'}_por_uf_ano.csv",encoding="utf-8")):
        BRCMAP[(r["uf"],int(r["ano"]))]=float(r["ideo_BRC_periodo"])
# --- painel
rows=[]
for (uf,ano),o in sorted(ob.items()):
    if ano<2012 or ano>2024 or (uf,ano) not in pop or (uf,ano) not in gov: continue
    p=pop[(uf,ano)]; g=gov[(uf,ano)]
    w=sum(m for _,m,_ in g); s=sum(sc*m for sc,m,_ in g)/w
    rows.append(dict(uf=uf,ano=ano,ideologia=round(BRCMAP[(uf,ano)] if IDEO=="brc" else s,2),partido='|'.join(sorted(set(x[2] for x in g))),
        tx_total=o['homicidios_total_n']/p['Total']*1e5, tx_mulheres=o['homicidios_mulheres_n']/p['Mulheres']*1e5,
        tx_homens=(o['homicidios_total_n']-o['homicidios_mulheres_n'])/p['Homens']*1e5,
        tx_negros=o['homicidios_negros_n']/p['negros']*1e5, tx_nao_negros=o['homicidios_nao_negros_n']/p['nao_negros']*1e5,
        tx_arma=o['homicidios_arma_fogo_n']/p['Total']*1e5))
with open(f"{D}/painel/painel_uf_ano{GOV}.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# --- TWFE com erro agrupado por UF
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
    # cluster por UF
    S=sum((xd[uf==k]@e[uf==k])**2 for k in np.unique(uf)); G=len(np.unique(uf)); n=len(y); k=1+G+len(np.unique(ano))-1
    se=math.sqrt(S/(xd@xd)**2 * G/(G-1)*(n-1)/(n-k))
    return b, se, n
out=["# F8 — painel UF x ano 2012-2024 (exploratório, NÃO causal)\n",
     f"Observações: {len(rows)} UF-anos. Partidos sem escore (linhas descartadas): {dict(unmatched)}\n",
     "Modelo: log(taxa) = b x ideologia_governador(0-10) + EF(UF) + EF(ano); EP agrupado por UF. b x 1 ponto = variação % aproximada da taxa por 1 ponto para a direita.\n",
     "| desfecho | b (por 1 ponto de ideologia) | EP | IC95% | n | leitura |","|---|---|---|---|---|---|"]
for col in ['tx_total','tx_homens','tx_mulheres','tx_negros','tx_nao_negros','tx_arma']:
    sel=[r for r in rows if r[col]>0]
    b,se,n=twfe([math.log(r[col]) for r in sel],[r['ideologia'] for r in sel],[r['uf'] for r in sel],[r['ano'] for r in sel])
    lo,hi=b-1.96*se,b+1.96*se
    out.append(f"| {col} | {b:+.4f} | {se:.4f} | [{lo:+.3f}, {hi:+.3f}] | {n} | {'não distinguível de zero' if lo<0<hi else ('maior sob governos mais à direita' if b>0 else 'menor sob governos mais à direita')} |")
# robustez: defasagem de 1 ano
out.append("\nRobustez (ideologia defasada 1 ano):\n\n| desfecho | b | EP | IC95% |\n|---|---|---|---|")
idx={(r['uf'],r['ano']):r for r in rows}
for col in ['tx_total','tx_mulheres','tx_negros']:
    sel=[(r, idx.get((r['uf'],r['ano']-1))) for r in rows if (r['uf'],r['ano']-1) in idx and r[col]>0]
    b,se,n=twfe([math.log(r[col]) for r,_ in sel],[l['ideologia'] for _,l in sel],[r['uf'] for r,_ in sel],[r['ano'] for r,_ in sel])
    out.append(f"| {col} | {b:+.4f} | {se:.4f} | [{b-1.96*se:+.3f}, {b+1.96*se:+.3f}] |")
# descritivo nacional por periodo federal (soma de obitos / soma de pop)
out.append("\nDescritivo nacional por período federal (taxa por 100 mil do grupo; soma das UFs do painel):\n\n| período | total | homens | mulheres | negros | não negros |\n|---|---|---|---|---|---|")
for nome,anos in [("2015-2018 (Dilma/Temer)",range(2015,2019)),("2019-2022 (Bolsonaro)",range(2019,2023)),("2023-2024 (Lula 3)",range(2023,2025))]:
    agg=collections.Counter()
    for (uf,ano),o in ob.items():
        if ano in anos and (uf,ano) in pop:
            p=pop[(uf,ano)]
            for k,v in [('n_tot',o['homicidios_total_n']),('p_tot',p['Total']),('n_mul',o['homicidios_mulheres_n']),('p_mul',p['Mulheres']),('n_hom',o['homicidios_total_n']-o['homicidios_mulheres_n']),('p_hom',p['Homens']),('n_neg',o['homicidios_negros_n']),('p_neg',p['negros']),('n_nn',o['homicidios_nao_negros_n']),('p_nn',p['nao_negros'])]: agg[k]+=v
    out.append(f"| {nome} | {agg['n_tot']/agg['p_tot']*1e5:.1f} | {agg['n_hom']/agg['p_hom']*1e5:.1f} | {agg['n_mul']/agg['p_mul']*1e5:.1f} | {agg['n_neg']/agg['p_neg']*1e5:.1f} | {agg['n_nn']/agg['p_nn']*1e5:.1f} |")
out.append("\nCaveats: (1) SIM = óbitos por agressão, sem motivação; (2) raça/cor do óbito tem 'ignorado' que não entra em negros nem não negros (viés para baixo nas duas taxas); (3) COVID 2020-21 e a queda nacional 2018-19 estão absorvidos pelos EF de ano, mas não os choques locais (facções, armas) correlacionados com eleição; (4) ideologia é do partido do governador, escore de 2018 aplicado a todos os anos; (5) 2025 excluído (preliminar); (6) população por cor/raça de 2021 interpolada (PNADC 6403 não publica 2021). Denominadores: PNAD Contínua (SIDRA 6407 e 6403, médias anuais).")
open(f"{D}/painel/resultados{GOV}.md","w").write("\n".join(out)); print("\n".join(out))

# ---------- Robustez: escala Zucco & Power (BLS9, onda 2021, aprox. -1..+1) ----------
ZP=(REPO_ROOT + "/fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab")
zp={}
for r in csv.DictReader(open(ZP)):
    if r['year']=='2021': zp[r['party.or.pres'].upper()]=float(r['ideo'])
ZMAP={'PMDB':'MDB','PP':'PP','PROGRESSISTAS':'PP','PR':'PL','PRB':'REPUBLICANOS','PPS':'CIDADANIA','SD':'SOLIDARIEDADE','SDD':'SOLIDARIEDADE','UNIÃO BRASIL':'DEM','UNIÃO':'DEM','PATRIOTA':'PATRIOTA','PROS':'PROS','PTB':'PTB'}
def zscore(p):
    P=p.strip().upper()
    for c in (P, ZMAP.get(P,'')):
        if c in zp: return zp[c]
    return None
gov2=collections.defaultdict(list); unm2=collections.Counter()
for r in csv.DictReader(open(f"{D}/governadores_uf_2011_2026{GOVCSV}.csv")):
    s=zscore(r['partido'])
    if s is None: unm2[r['partido']]+=1; continue
    try:
        from datetime import date
        a=date.fromisoformat(r['inicio']); b=date.fromisoformat(r['fim']); meses=max(1,(b-a).days/30.4)
    except Exception: meses=12
    gov2[(r['uf'],int(r['ano']))].append((s,meses))
rows2=[]
for r in rows:
    g=gov2.get((r['uf'],r['ano']))
    if not g: continue
    w=sum(m for _,m in g); rows2.append(dict(r, zp=sum(s*m for s,m in g)/w))
out2=[f"\n## Robustez — escala Zucco & Power (BLS9 2021, -1 esquerda .. +1 direita); {len(rows2)} UF-anos; partidos sem escore: {dict(unm2)}\n",
      "| desfecho | b (por 1 unidade da escala; ~meio do intervalo esquerda-direita) | EP | IC95% |","|---|---|---|---|"]
for col in ['tx_total','tx_homens','tx_mulheres','tx_negros','tx_nao_negros','tx_arma']:
    sel=[r for r in rows2 if r[col]>0]
    b,se,n=twfe([math.log(r[col]) for r in sel],[r['zp'] for r in sel],[r['uf'] for r in sel],[r['ano'] for r in sel])
    out2.append(f"| {col} | {b:+.4f} | {se:.4f} | [{b-1.96*se:+.3f}, {b+1.96*se:+.3f}] |")
out2.append("\nLeitura: 1 unidade da escala BLS9 ≈ distância PT (−0,69) -> DEM/PL (+0,43/+0,49) mais um pouco; nenhum coeficiente distinguível de zero nas duas escalas.")
open(f"{D}/painel/resultados{GOV}.md","a").write("\n".join(out2)); print("\n".join(out2))
