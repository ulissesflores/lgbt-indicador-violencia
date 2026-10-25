#!/usr/bin/env python3
"""Espaço de busca enumerado (rodada 3, F8-literatura). Cada consulta -> contagem total por base (OpenAlex search relevância-ordenada, Europe PMC).
Saída: busca-enumerada.json. Contagem é de resultados da base para a string literal, não de relevantes."""
import json, urllib.request, urllib.parse, sys, datetime, time
UA={"User-Agent":"F8-literatura/1.0 (mailto:seu-email@exemplo.org)"}
Q=[
 # Brasil 2016-2024: causal / ciclo eleitoral / política federal
 ("BR-causal-1","Bolsonaro election violence against LGBT","en"),
 ("BR-causal-2","Bolsonaro difference-in-differences hate crime","en"),
 ("BR-causal-3","Brazil 2018 election homophobic violence","en"),
 ("BR-causal-4","Brazil LGBT policy Bolsonaro government dismantling","en"),
 ("BR-causal-5","eleições 2018 violência contra LGBT","pt"),
 ("BR-causal-6","governo Bolsonaro violência LGBT efeito discurso","pt"),
 ("BR-causal-7","violencia contra personas LGBT Brasil elecciones 2018 Bolsonaro","es"),
 ("BR-causal-8","desmonte política pública LGBT governo federal 2019","pt"),
 ("BR-causal-9","violência política eleitoral Brasil 2018 homofobia","pt"),
 # Estado perseguição Brasil
 ("BR-estado-1","ditadura militar perseguição homossexuais Brasil","pt"),
 ("BR-estado-2","Operação Limpeza Richetti travestis polícia São Paulo","pt"),
 ("BR-estado-3","violência policial contra travestis Brasil","pt"),
 ("BR-estado-4","Brazilian military dictatorship homosexuals persecution","en"),
 # Comparados
 ("RU-1","gay propaganda law hate crimes Russia","en"),
 ("RU-2","закон о гей-пропаганде преступления ненависти ЛГБТ","ru"),
 ("CH-1","Chechnya LGBT persecution report","en"),
 ("PL-1","Poland LGBT-free zones violence","en"),
 ("PL-2","strefy wolne od LGBT przemoc","pl"),
 ("HU-1","Hungary anti-LGBT law violence","en"),
 ("HU-2","LMBTQ törvény erőszak Magyarország","hu"),
 ("UG-1","Uganda Anti-Homosexuality Act violence","en"),
 ("NG-1","Nigeria Same Sex Marriage Prohibition Act violence","en"),
 ("GH-1","Ghana anti-LGBT bill violence","en"),
 ("US-1","Trump election hate crimes sexual orientation","en"),
 ("US-2","Trump rallies hate incidents","en"),
 ("UK-1","Brexit referendum hate crime","en"),
 ("UK-2","Brexit homophobic hate crime sexual orientation","en"),
 ("MA-1","systematic review anti-LGBT laws violence","en"),
 ("MA-2","meta-analysis political events hate crime","en"),
 ("MA-3","structural stigma LGBT systematic review","en"),
 ("ME-1","sexual orientation death certificate homicide","en"),
 ("ME-2","orientação sexual declaração de óbito homicídio","pt"),
]
out=[]
for qid,q,lang in Q:
    row={"id":qid,"q":q,"lang":lang,"ts":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    row["openalex"]=None
    for tent in range(6):
        try:
            u="https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":1,"mailto":"seu-email@exemplo.org"})
            row["openalex"]=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))["meta"]["count"]; break
        except Exception as e:
            row["openalex"]=f"erro:{str(e)[:40]}"; time.sleep(25)
    try:
        u="https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode({"query":q,"format":"json","pageSize":1})
        row["europepmc"]=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))["hitCount"]
    except Exception as e: row["europepmc"]=f"erro:{str(e)[:40]}"
    out.append(row); print(row,flush=True); time.sleep(0.3)
json.dump(out,open("busca-enumerada.json","w"),ensure_ascii=False,indent=1)
