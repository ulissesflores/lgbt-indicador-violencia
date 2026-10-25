"""SUPERADO em 2026-10-21 por concordancia_v2.py (este script mede CONTAGENS, que refletem tamanho da UF; ver concordancia_v2.md). Mantido só para reprodução da v1: saída em resumo_v1_contagens.md.
Concordância Sinan (campo 55 = LGBTfobia, notificações interpessoais, por UF-ano) x Anuário FBSP (BO 'racismo por homofobia ou transfobia', por UF-ano).
Anos comuns: 2022-2025. Para cada ano usa a edição MAIS RECENTE do Anuário que traz o ano. Métricas: Spearman e Pearson (log) entre contagens; razão BO/Sinan; concordância de ranking; gráfico."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, collections, math, os
import numpy as np
from scipy.stats import spearmanr, pearsonr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D=(REPO_ROOT + "/dados"); OUT=os.path.dirname(os.path.abspath(__file__))
sin={}
for r in csv.DictReader(open(f"{D}/sinan/serie_campo55_uf_ano.csv")):
    if r['uf']!='BR': sin[(int(r['ano']),r['uf'])]=(int(r['m_lgbtfobia']), int(r['n_interpessoal']))
anu={}
for r in csv.DictReader(open(f"{D}/anuario/anuario_lgbtfobia_uf_ano.csv")):
    if r['uf']=='BR' or not r['registros'].strip(): continue
    k=(int(r['ano_dado']),r['uf']); ed=int(r['edicao'])
    if k not in anu or ed>anu[k][1]: anu[k]=(int(r['registros']),ed)
rows=[]; L=["# Concordância Sinan x Anuário (LGBTfobia por UF-ano, 2022-2025)\n","| ano | n UFs | Spearman (IC via n) | Pearson log | mediana BO/Sinan | UFs com BO=NA | UFs Sinan>0 e BO=0 |","|---|---|---|---|---|---|---|"]
fig,axs=plt.subplots(1,4,figsize=(16,4))
for i,ano in enumerate([2022,2023,2024,2025]):
    xs=[];ys=[];ufs=[];na=0;zero=0
    for uf in sorted({u for (a,u) in sin if a==ano}):
        s=sin.get((ano,uf)); b=anu.get((ano,uf))
        if s is None: continue
        if b is None: na+=1; rows.append([ano,uf,s[0],s[1],'',''] ); continue
        if s[0]>0 and b[0]==0: zero+=1
        xs.append(s[0]); ys.append(b[0]); ufs.append(uf); rows.append([ano,uf,s[0],s[1],b[0],round(b[0]/s[0],2) if s[0] else ''])
    xs=np.array(xs); ys=np.array(ys)
    rho,p=spearmanr(xs,ys); rl,pl=pearsonr(np.log1p(xs),np.log1p(ys))
    ratio=np.median(ys[xs>0]/xs[xs>0])
    L.append(f"| {ano} | {len(xs)} | {rho:.2f} (p={p:.3f}) | {rl:.2f} (p={pl:.3f}) | {ratio:.2f} | {na} | {zero} |")
    ax=axs[i]; ax.scatter(xs+1,ys+1); [ax.annotate(u,(x+1,y+1),fontsize=7) for u,x,y in zip(ufs,xs,ys)]
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_title(f"{ano}: Sinan (x) vs BO (y), log1p"); ax.plot([1,1e4],[1,1e4],'k--',lw=0.5)
plt.tight_layout(); plt.savefig(f"{OUT}/fig-concordancia.png",dpi=120)
with open(f"{OUT}/concordancia_uf_ano.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(['ano','uf','sinan_lgbtfobia','sinan_interpessoal_total','anuario_bo_lgbtfobia','razao_bo_sinan']); w.writerows(rows)
L.append("\nLeitura: Spearman mede se os estados que mais notificam LGBTfobia na saúde são os que mais registram na polícia (ordem), independentemente de escala; a razão BO/Sinan mostra a divergência de nível entre os dois sistemas; 'BO=0 com Sinan>0' é o candidato a zero cerimonial do lado policial. Anuário: edição mais recente por ano (2023 = ed. 2025; 2024 = ed. 2026). Fontes: dados/sinan/serie_campo55_uf_ano.csv (microdados DATASUS) e dados/anuario/anuario_lgbtfobia_uf_ano.csv (pdftotext dos Anuários 2024-2026, somas conferidas).")
open(f"{OUT}/resumo_v1_contagens.md","w").write("\n".join(L)+"\n"); print("\n".join(L))
