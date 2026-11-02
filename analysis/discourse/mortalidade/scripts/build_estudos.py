"""Gera ../estudos.csv a partir de rows.py + Crossref (referência) + sha256 dos arquivos locais. Python: /opt/homebrew/bin/python3.14 -I"""
import csv,json,hashlib,os,sys,time,urllib.request,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from rows import R,SJR
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
def cr(doi):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works/'+doi,headers={'User-Agent':'research-lab (mailto-free)'}),timeout=40))['message']
        except Exception: time.sleep(2*(i+1))
def ref(m):
    au=m.get('author',[]); nm=[f"{a.get('family','')}, {a.get('given','')[:1]}." if a.get('given') else a.get('family','') for a in au]
    a=', '.join(nm[:6])+(' et al.' if len(nm)>6 else '')
    y=(m.get('issued',{}).get('date-parts') or [[None]])[0][0]
    t=(m.get('title') or [''])[0]; j=(m.get('container-title') or [''])[0]
    return f"{a} ({y}). {t}. {j}, {m.get('volume','')}{'('+m['issue']+')' if m.get('issue') else ''}{', '+m['page'] if m.get('page') else ''}.".replace('  ',' ')
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
rows=[]
for r in R:
    if r['doi']:
        m=cr(r['doi']); rf=ref(m) if m else '(Crossref indisponível)'
    elif r['id']=='M38': rf="Truman, J. L.; Morgan, R. E. (2022). Violent Victimization by Sexual Orientation and Gender Identity, 2017-2020. Bureau of Justice Statistics, Statistical Brief NCJ 304277. U.S. Department of Justice."
    else: rf="DATASUS/Ministério da Saúde. Microdados do SIM, Declarações de Óbito CID-10 (DOBR2023.dbc e DOBR2024.dbc). FTP DATASUS."
    q=SJR.get(r['j'],'nao_verificado') if r['doi'] else 'oficial_nao_periodico'
    ret = 'RETRATADO' if r['id']=='M10' else ''
    rows.append(dict(id=r['id'],referencia=rf,doi=r['doi'],periodico=r['j'],quartil_sjr=q,pais_periodo=r['pais'],desenho=r['des'],amostra=r['n'],
        definicao_orientacao_identidade=r['defo'],desfecho=r['des_out'],estimativa_IC=r['est'],trecho_verbatim=r['tr'],secao_pagina=r['loc'],
        populacao=r['pop'],causa=r['causa'],papel_no_veredito=r['papel'],limitacoes=r['lim'],observacao=(r['extra']+(' | '+ret if ret else '')).strip(' |'),
        arquivo_lido=r['arq'],formato=os.path.splitext(r['arq'])[1].lstrip('.'),sha256=sha(r['arq']),estado='lido_texto_integral' if not r['id'] in ('M13','M26') else 'lido_manuscrito_aceito'))
cols=list(rows[0].keys())
with open(os.path.join(OUT,'estudos.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows),'linhas'); 
import collections; print(collections.Counter(x['quartil_sjr'] for x in rows))
