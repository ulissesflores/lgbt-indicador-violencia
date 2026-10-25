import json,sys
fn,fam=sys.argv[1],sys.argv[2]; a=int(sys.argv[3]) if len(sys.argv)>3 else 0; b=int(sys.argv[4]) if len(sys.argv)>4 else 999
n=int(sys.argv[5]) if len(sys.argv)>5 else 230
for i,l in enumerate(open(fn)):
    j=json.loads(l)
    if j['familia']!=fam or not (a<=i<b): continue
    t=(j.get('trecho') or j.get('titulo') or '')
    if 'titulo' in j and j.get('trecho'): t=j['titulo']+' || '+j['trecho']
    print(i,j['data'][:16] if j.get('data') else '',(j.get('fonte') or ''),(';'.join(j.get('entradas',[])))[:14],'|',t[:n].replace('\n',' '))
