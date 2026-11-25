# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Check that each quoted passage in rows.py appears literally in the local full text.

For every study row it normalizes quotes, dashes and spaces, extracts the text of the local
file (HTML directly, PDF through pdftotext, a text file for one scanned article) and checks
that each verbatim passage is found. Prints each passage not found and the number of failures.

Inputs
------
- analysis/discourse/mortalidade/scripts/rows.py (rows and quoted passages)
- the local full-text files named in the rows (not tracked in git)
- pdftotext (external tool)

Outputs
-------
- prints each passage not found and the number of failures; nothing is written to disk

Usage
-----
python3 -I analysis/discourse/mortalidade/scripts/verifica_trechos.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Confere que cada trecho entre aspas em rows.py aparece literalmente no texto local lido. Uso: verifica_trechos.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import re,subprocess,html,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from rows import R
def norm(s):
    s=html.unescape(s).replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('–','-').replace('—','-').replace('–','-').replace('—','-').replace('\xa0',' ')
    return re.sub(r'\s+',' ',s).lower()
def texto(p):
    if p.endswith('.pdf'):
        if 'avb.2009' in p:
            p=os.path.dirname(p)+'/_ocr/10_10.1016_j.avb.2009.01.006_publishedVersion_scan.txt'; return open(p,errors='ignore').read()
        return subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
    if p.endswith('.dbc'): return ''
    b=open(p,'rb').read().decode('utf8','ignore')
    b=re.sub(r'<(script|style)[^>]*>.*?</\1>','',b,flags=re.S); b=re.sub(r'<[^>]+>',' ',b); return b
bad=0
for r in R:
    if r['arq'].endswith('.dbc'): continue
    t=norm(texto(r['arq']))
    # junta pontas hifenizadas de PDF
    t=t.replace('- ','-') if r['arq'].endswith('.pdf') else t
    for field in ('tr','lim','extra'):
        for seg in re.findall(r'"([^"]{12,})"',r[field]):
            parts=[x for x in re.split(r'\.\.\.|…',seg) if len(x.strip())>10]
            for p in parts:
                q=norm(p).strip(' .')
                q=q.replace('- ','-') if r['arq'].endswith('.pdf') else q
                if q not in t:
                    bad+=1; print('NAO ACHEI',r['id'],field,'::',p[:110])
print('falhas:',bad)
