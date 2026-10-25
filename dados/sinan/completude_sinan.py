"""[2026-10-21] Saída movida de resumo.md (que era sobrescrito, apagando as seções anexadas depois) para completude_2023_2024.md.
Completude e distribuição dos campos 55 (VIOL_MOTIV), 36 (ORIENT_SEX) e 37 (IDENT_GEN) do Sinan VIVA, Brasil e UF, 2023-2024,
e assimetria de contexto (relação vítima-autor) por sexo. Entrada: VIOLBR23/24.dbf (FTP DATASUS, convertidos de .dbc). Saída: CSVs + resumo.md."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import os, collections, csv, sys
from dbfread import DBF
SRC=(REPO_ROOT + "/fontes/p2-sinan-microdados"); OUT=os.path.dirname(os.path.abspath(__file__))
UF={'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA','31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS','51':'MT','52':'GO','53':'DF'}
MOTIV={'01':'sexismo','02':'LGBTfobia','03':'racismo','04':'intol_religiosa','05':'xenofobia','06':'conflito_geracional','07':'situacao_rua','08':'deficiencia','09':'outros','88':'nao_se_aplica','99':'ignorado','':'branco'}
ORI={'1':'hetero','2':'homo','3':'bi','8':'nao_se_aplica','9':'ignorado','':'branco'}
IDG={'1':'travesti','2':'mulher_trans','3':'homem_trans','8':'nao_se_aplica','9':'ignorado','':'branco'}
mot=collections.Counter(); ori=collections.Counter(); idg=collections.Counter(); ctx=collections.Counter(); tot=collections.Counter()
REL=['REL_CONJ','REL_EXCON','REL_NAMO','REL_EXNAM','REL_PAI','REL_MAE','REL_PAD','REL_MAD','REL_FILHO','REL_IRMAO','REL_CONHEC','REL_DESCO','REL_POL','REL_PROPRI']
for y in ('2023','2024'):
    for r in DBF(f"{SRC}/VIOLBR{y[2:]}.dbf", encoding='latin-1', load=False):
        uf=UF.get(str(r.get('SG_UF_NOT') or '').strip(),'??'); sx=str(r.get('CS_SEXO') or '').strip()
        m=str(r.get('VIOL_MOTIV') or '').strip(); o=str(r.get('ORIENT_SEX') or '').strip(); g=str(r.get('IDENT_GEN') or '').strip()
        # autoprovocada (LES_AUTOP=1) fica fora do denominador de motivação? campo 55 e' "essa violencia foi motivada por" -> vale p/ interpessoal; mantemos todos e marcamos
        auto=str(r.get('LES_AUTOP') or '').strip()=='1'
        for k in ((y,uf),(y,'BR')):
            tot[k]+=1
            if auto: tot[(k[0],k[1],'auto')]+=1
            mot[(k, MOTIV.get(m, 'cod_'+m))]+=1; ori[(k, ORI.get(o,'cod_'+o))]+=1; idg[(k, IDG.get(g,'cod_'+g))]+=1
        if not auto and sx in ('F','M'):
            tot[(y,'sexo',sx)]+=1
            for c in REL:
                if str(r.get(c) or '').strip()=='1': ctx[(y,sx,c)]+=1
def dump(name, cnt, cats):
    keys=sorted({k[0] for k in cnt}); 
    with open(f"{OUT}/{name}.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(['ano','uf','total']+cats+['pct_'+c for c in cats])
        for (y,uf) in keys:
            n=tot[(y,uf)]; vals=[cnt[((y,uf),c)] for c in cats]
            w.writerow([y,uf,n]+vals+[round(v/n*100,1) if n else '' for v in vals])
dump('campo55_motivacao', mot, list(dict.fromkeys(MOTIV.values())))
dump('campo36_orientacao', ori, list(dict.fromkeys(ORI.values())))
dump('campo37_identidade', idg, list(dict.fromkeys(IDG.values())))
with open(f"{OUT}/contexto_por_sexo.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(['ano','sexo','notificacoes_interpessoais']+REL+['pct_'+c for c in REL])
    for y in ('2023','2024'):
        for sx in ('F','M'):
            n=tot[(y,'sexo',sx)]; vals=[ctx[(y,sx,c)] for c in REL]; w.writerow([y,sx,n]+vals+[round(v/n*100,1) if n else '' for v in vals])
# resumo
L=[]
for y in ('2023','2024'):
    n=tot[(y,'BR')]; a=tot[(y,'BR','auto')]
    L.append(f"\n## {y}: {n:,} notificações no Brasil (autoprovocadas: {a:,}, {a/n*100:.1f}%)")
    for nome,cnt,cats in (('campo 55 motivação',mot,list(dict.fromkeys(MOTIV.values()))),('campo 36 orientação sexual',ori,list(dict.fromkeys(ORI.values()))),('campo 37 identidade de gênero',idg,list(dict.fromkeys(IDG.values())))):
        L.append(f"- {nome}: "+"; ".join(f"{c} {cnt[((y,'BR'),c)]:,} ({cnt[((y,'BR'),c)]/n*100:.1f}%)" for c in cats if cnt[((y,'BR'),c)]))
    L.append("- contexto (interpessoal, % das notificações do sexo): "+"; ".join(f"{c[4:]} F {ctx[(y,'F',c)]/tot[(y,'sexo','F')]*100:.1f}% / M {ctx[(y,'M',c)]/tot[(y,'sexo','M')]*100:.1f}%" for c in ['REL_CONJ','REL_EXCON','REL_NAMO','REL_PAI','REL_MAE','REL_CONHEC','REL_DESCO','REL_POL']))
    # pior/melhor UF em ignorado+branco do campo 55
    ufs=[(uf,(mot[((y,uf),'ignorado')]+mot[((y,uf),'branco')])/tot[(y,uf)]*100, mot[((y,uf),'LGBTfobia')]/tot[(y,uf)]*100, tot[(y,uf)]) for uf in UF.values() if tot[(y,uf)]]
    ufs.sort(key=lambda x:-x[1])
    L.append("- campo 55 ignorado+branco por UF (pior 5): "+"; ".join(f"{u} {p:.0f}% (LGBTfobia {l:.1f}%, n={n:,})" for u,p,l,n in ufs[:5]))
    L.append("- campo 55 ignorado+branco por UF (melhor 5): "+"; ".join(f"{u} {p:.0f}% (LGBTfobia {l:.1f}%, n={n:,})" for u,p,l,n in ufs[-5:]))
open(f"{OUT}/completude_2023_2024.md","w").write("# Sinan VIVA — completude dos campos 55/36/37 e contexto por sexo (microdados DATASUS, VIOLBR23/24)\n"+"\n".join(L)+"\n")
print("\n".join(L))
