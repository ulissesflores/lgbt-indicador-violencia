# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Count adult aggression deaths in the SIM microdata for Brazil, 2023 and 2024.

Downloads the 2023 and 2024 SIM death files from the DATASUS FTP when absent, converts each to
DBF, and counts deaths with underlying cause X85-Y09 by age (18 or older, under 18, unknown) and
by sex among adults. It writes a CSV, appends a section to the Sinan summary with an approximate
adult rate per 100,000 using the 2022 census adult population typed in the script, and deletes
the temporary DBF files.

Inputs
------
- ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DOBR<year>.dbc (network)
- sources/public/p2-sim-microdados/DOBR2023.dbc (not tracked in git)
- sources/public/p2-sim-microdados/DOBR2024.dbc (not tracked in git)

Outputs
-------
- data/sinan/sim_adultos_18mais.csv
- data/sinan/resumo.md (section appended)
- prints the counts and the appended section to stdout

Usage
-----
python3 -I data/sinan/sim_adultos_18mais.py (needs pyreaddbc and dbfread)

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Numerador adulto (18+) de óbitos por agressão (X85-Y09) no SIM, Brasil 2023 e 2024, a partir dos microdados DOBRyyyy.dbc (FTP DATASUS).
IDADE no SIM: código de 3 dígitos: 4xx = xx anos (400=0? não: 4 = anos, 2 dígitos), 5xx = 100+xx anos; 9xx/branco = ignorada. Saída: CSV + linhas no resumo.md.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import os, subprocess, csv, collections
import pyreaddbc
from dbfread import DBF
SRC=(REPO_ROOT + "/sources/public/p2-sim-microdados"); OUT=(REPO_ROOT + "/data/sinan")
rows=[]
for ano in (2023,2024):
    dbc=f"{SRC}/DOBR{ano}.dbc"; dbf=f"{SRC}/DOBR{ano}.dbf"
    if not os.path.exists(dbc):
        subprocess.run(["curl","-sS","-m","900","-o",dbc,f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DOBR{ano}.dbc"],check=True)
    print(ano,"dbc",os.path.getsize(dbc),flush=True)
    if not os.path.exists(dbf): pyreaddbc.dbc2dbf(dbc,dbf)
    c=collections.Counter()
    for r in DBF(dbf,encoding='latin-1',load=False):
        cb=str(r.get('CAUSABAS') or '').strip().upper()
        if not (cb.startswith('X8') and cb[:3] in ('X85','X86','X87','X88','X89') or cb.startswith('X9') or cb[:3] in ('Y00','Y01','Y02','Y03','Y04','Y05','Y06','Y07','Y08','Y09')): continue
        idade=str(r.get('IDADE') or '').strip()
        c['total']+=1
        if len(idade)==3 and idade[0] in '45':
            anos=int(idade[1:])+(100 if idade[0]=='5' else 0)
            c['18+' if anos>=18 else '<18']+=1
        else: c['ignorada']+=1
        sexo=str(r.get('SEXO') or '').strip()
        if len(idade)==3 and idade[0] in '45' and int(idade[1:])+(100 if idade[0]=='5' else 0)>=18: c['18+_sexo_'+sexo]+=1
    rows.append([ano,c['total'],c['18+'],c['<18'],c['ignorada'],c['18+_sexo_1'],c['18+_sexo_2']])
    print(ano,dict(c),flush=True)
    os.remove(dbf)
with open(f"{OUT}/sim_adultos_18mais.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(['ano','agressoes_total','agressoes_18mais','agressoes_menor18','idade_ignorada','18mais_homens','18mais_mulheres']); w.writerows(rows)
adult=154346198
L=["\n## SIM microdados: óbitos por agressão (X85-Y09) em adultos 18+ (DOBR2023/2024.dbc, FTP DATASUS)"]
for ano,tot,a18,m18,ign,h,m in rows:
    L.append(f"- {ano}: total {tot:,}; 18+ {a18:,} ({a18/tot*100:.1f}%); <18 {m18:,}; idade ignorada {ign:,}; 18+ homens {h:,}, mulheres {m:,}. Taxa adulta aproximada (denominador Censo 2022 18+ = 154.346.198): {a18/adult*1e5:.1f} por 100 mil adultos.")
open(f"{OUT}/resumo.md","a").write("\n".join(L)+"\n"); print("\n".join(L)); print("FIM")
