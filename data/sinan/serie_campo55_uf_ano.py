# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Build the 2015-2025 state-by-year series of Sinan VIVA completeness for fields 55, 36 and 37.

For each year it downloads the yearly Sinan VIVA violence file from the DATASUS FTP when it is
missing (final data first, preliminary data as fallback), converts it to DBF, and counts
interpersonal notifications (self-inflicted injuries excluded) by state and for Brazil: unknown
or blank, not applicable, LGBT-phobia, racism and sexism motivation; orientation unknown, not
applicable and homo or bisexual; gender identity unknown and trans. It writes counts and
percentages, then deletes the DBF except for 2023 and 2024.

Inputs
------
- ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/FINAIS/VIOLBR<yy>.dbc (network)
- ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/PRELIM/VIOLBR<yy>.dbc (network,
  fallback)
- sources/public/p2-sinan-microdados/VIOLBR<yy>.dbc (not tracked in git)

Outputs
-------
- data/sinan/serie_campo55_uf_ano.csv
- prints one summary line per year to stdout

Usage
-----
python3 -I data/sinan/serie_campo55_uf_ano.py (needs pyreaddbc and dbfread)

Status
------
Feeds numbers printed in the article (listed in paper_numbers.json).

Notes
-----
Original description (Portuguese), kept verbatim:

Série 2015-2025 por UF x ano da completude do campo 55 (VIOL_MOTIV) e dos campos 36/37, Sinan VIVA, só violência interpessoal.
Baixa VIOLBRyy.dbc do FTP DATASUS (se ausente), converte p/ .dbf, agrega e APAGA o .dbf (mantém .dbc + sha256). Saída: serie_campo55_uf_ano.csv

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import os, sys, csv, subprocess, collections, hashlib
import pyreaddbc
from dbfread import DBF
SRC=(REPO_ROOT + "/sources/public/p2-sinan-microdados"); OUT=os.path.dirname(os.path.abspath(__file__))
UF={'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA','31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS','51':'MT','52':'GO','53':'DF'}
anos=[a for a in range(2015,2026)]
rows=[]
for ano in anos:
    yy=str(ano)[2:]; dbc=f"{SRC}/VIOLBR{yy}.dbc"; dbf=f"{SRC}/VIOLBR{yy}.dbf"
    if not os.path.exists(dbc):
        r=subprocess.run(["curl","-sS","-m","600","-o",dbc,f"ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/FINAIS/VIOLBR{yy}.dbc"],capture_output=True,text=True)
        if r.returncode!=0 or os.path.getsize(dbc)<100000:
            r=subprocess.run(["curl","-sS","-m","600","-o",dbc,f"ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/PRELIM/VIOLBR{yy}.dbc"],capture_output=True,text=True)
        print(ano,"download",os.path.getsize(dbc) if os.path.exists(dbc) else "FALHA",flush=True)
    if not os.path.exists(dbf): pyreaddbc.dbc2dbf(dbc,dbf)
    c=collections.Counter()
    for r in DBF(dbf,encoding='latin-1',load=False):
        if str(r.get('LES_AUTOP') or '').strip()=='1': continue
        uf=UF.get(str(r.get('SG_UF_NOT') or '').strip(),'??')
        m=str(r.get('VIOL_MOTIV') or '').strip(); o=str(r.get('ORIENT_SEX') or '').strip(); g=str(r.get('IDENT_GEN') or '').strip()
        for k in (uf,'BR'):
            c[(k,'n')]+=1
            c[(k,'m_ign')]+= m in ('99',''); c[(k,'m_na')]+= m=='88'; c[(k,'m_lgbt')]+= m=='02'; c[(k,'m_rac')]+= m=='03'; c[(k,'m_sex')]+= m=='01'
            c[(k,'o_ign')]+= o in ('9',''); c[(k,'o_na')]+= o=='8'; c[(k,'o_hb')]+= o in ('2','3')
            c[(k,'g_ign')]+= g in ('9',''); c[(k,'g_trans')]+= g in ('1','2','3')
    for uf in list(UF.values())+['BR']:
        n=c[(uf,'n')]
        if not n: continue
        rows.append([ano,uf,n]+[c[(uf,k)] for k in ('m_ign','m_na','m_lgbt','m_rac','m_sex','o_ign','o_na','o_hb','g_ign','g_trans')]+[round(c[(uf,k)]/n*100,2) for k in ('m_ign','m_na','m_lgbt','o_ign','o_hb','g_trans')])
    with open(f"{OUT}/serie_campo55_uf_ano.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(['ano','uf','n_interpessoal','m_ign_branco','m_nao_se_aplica','m_lgbtfobia','m_racismo','m_sexismo','o_ign_branco','o_nao_se_aplica','o_homo_bi','g_ign_branco','g_trans','pct_m_ign','pct_m_na','pct_m_lgbt','pct_o_ign','pct_o_homo_bi','pct_g_trans']); w.writerows(rows)
    br=[r for r in rows if r[0]==ano and r[1]=='BR'][0]
    print(ano,"BR n=",br[2],"campo55 ign+branco %",br[-6],"NA %",br[-5],"LGBTfobia %",br[-4],"orient ign %",br[-3],"homo+bi %",br[-2],flush=True)
    if ano not in (2023,2024): os.remove(dbf)
print("FIM",flush=True)
