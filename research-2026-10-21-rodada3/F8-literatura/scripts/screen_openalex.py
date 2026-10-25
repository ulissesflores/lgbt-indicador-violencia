#!/usr/bin/env python3
"""Triagem reprodutível: consulta booleana no OpenAlex (título+resumo), pagina TODOS os resultados (até 600),
marca desenho causal por termos no resumo reconstruído e grava TSV. Uso: screen_openalex.py <id> "<boolean>" [from_year]"""
import sys,json,urllib.request,urllib.parse,re,time,datetime
qid,q=sys.argv[1],sys.argv[2]; fy=sys.argv[3] if len(sys.argv)>3 else "2016"
UA={"User-Agent":"F8-literatura/1.0 (mailto:seu-email@exemplo.org)"}
CAUSAL=re.compile(r"difference-in-difference|diff-in-diff|event[- ]study|synthetic control|regression discontinuity|instrumental variable|quasi-experiment|natural experiment|causal|interrupted time series|diferenças em diferenças|diferença em diferenças|quase-experiment",re.I)
rows=[];page=1;total=None
while len(rows)<600:
    u="https://api.openalex.org/works?"+urllib.parse.urlencode({"filter":f"title_and_abstract.search:{q},from_publication_date:{fy}-01-01","per-page":100,"page":page,"mailto":"seu-email@exemplo.org","select":"id,doi,title,publication_year,primary_location,abstract_inverted_index,type"})
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
    total=d["meta"]["count"]
    for w in d["results"]:
        inv=w.get("abstract_inverted_index") or {}
        words=sorted(((p,t) for t,ps in inv.items() for p in ps))
        ab=" ".join(t for p,t in words)
        src=((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        rows.append((w.get("publication_year"),src,w.get("doi") or "",(w.get("title") or "").replace("\t"," "),bool(CAUSAL.search(ab+" "+(w.get('title') or ''))),w.get("type")))
    page+=1; time.sleep(0.2)
    if not d["results"] or len(rows)>=total: break
fn=f"triagem-{qid}.tsv"
with open(fn,"w") as f:
    f.write(f"# consulta={q} | from={fy} | total_openalex={total} | lidos={len(rows)} | gerado={datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
    f.write("ano\tperiodico\tdoi\ttitulo\ttermo_causal_no_resumo\ttipo\n")
    for r in sorted(rows,key=lambda x:(not x[4],-(x[0] or 0))): f.write("\t".join(map(str,r))+"\n")
print(qid,"total",total,"lidos",len(rows),"com termo causal",sum(1 for r in rows if r[4]))
