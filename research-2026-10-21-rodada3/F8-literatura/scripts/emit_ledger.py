#!/usr/bin/env python3
"""Emite sources.jsonl desta frente SÓ via emit_sources.py (porta única do ledger). Reexecutar apaga e refaz o arquivo."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import json, subprocess, hashlib, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import rows
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/F8-literatura")
EMIT = _os.environ.get("EMIT_SOURCES", "emit_sources.py")
PY = "/opt/homebrew/bin/python3.14"
# id da linha -> metadados do ledger
M = {
 "A1": dict(url="https://web.archive.org/web/2016id_/http://cnv.memoriasreveladas.gov.br/images/pdf/relatorio/volume_2_digital.pdf", id="cnv-2014-vol2-texto7", kind="other", acesso="wayback", idioma="pt", canal="fonte-oficial", ano=2014, titulo="CNV Relatorio vol. II, texto 7 Ditadura e homossexualidades"),
 "A2": dict(url="https://www.osce.org/files/Moscow%20Mechanism%20Document_ENG.pdf", id="osce-odihr-gal-76-18-corr1", kind="other", acesso="oa", idioma="en", canal="fonte-oficial", ano=2018, titulo="OSCE Moscow Mechanism report on Chechnya (Benedek)"),
 "A3": dict(url="https://hudoc.echr.coe.int/app/conversion/pdf/?library=ECHR&id=001-226449&filename=CASE%20OF%20LAPUNOV%20v.%20RUSSIA.pdf", id="echr-28834-19", kind="other", acesso="oa", idioma="en", canal="fonte-oficial", ano=2023, titulo="ECtHR Lapunov v. Russia"),
 "A4": dict(url="https://doi.org/10.7440/histcrit71.2019.05", id="10.7440/histcrit71.2019.05", kind="doi", acesso="oa", idioma="es", canal="crossref", ano=2019, titulo="Los primeros anos de la Revolucion cubana y las UMAP"),
 "A5": dict(url="https://doi.org/10.1590/18094449201800520013", id="10.1590/18094449201800520013", kind="doi", acesso="oa", idioma="pt", canal="scielo", ano=2018, titulo="Autoritarismo e homofobia: Cuba e Brasil"),
 "B1": dict(url="https://doi.org/10.1016/j.ssresearch.2016.06.008", id="10.1016/j.ssresearch.2016.06.008", kind="doi", acesso="wayback", idioma="en", canal="crossref", ano=2017, titulo="When love meets hate"),
 "B2": dict(url="https://doi.org/10.1086/721700", id="10.1086/721700", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2022, titulo="Pride and Prejudice (preprint SSRN 3362835 lido)"),
 "B3": dict(url="https://doi.org/10.1093/bjc/azac071", id="10.1093/bjc/azac071", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2022, titulo="Brexit vote RR hate crimes (Williams et al.)"),
 "B4": dict(url="https://hdl.handle.net/10419/232654", id="10.2139/ssrn.3738844", kind="doi", acesso="preprint", idioma="en", canal="econstor", ano=2020, titulo="Love Thy Neighbour? Brexit and Hate Crime (IZA DP 13902)"),
 "B5": dict(url="https://doi.org/10.1111/1745-9125.12259", id="10.1111/1745-9125.12259", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2020, titulo="Threat, emboldenment, or both?"),
 "B6": dict(url="https://doi.org/10.1017/s1049096521001621", id="10.1017/s1049096521001621", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2022, titulo="The Trump Effect (preprint 2019 lido)"),
 "B7": dict(url="https://github.com/lilleymatthew/Trump_Rallies_Replication_Materials/blob/master/Trump_Rallies_and_Hate_Crimes.pdf", id="https://github.com/lilleymatthew/Trump_Rallies_Replication_Materials/blob/master/Trump_Rallies_and_Hate_Crimes.pdf", kind="url", acesso="preprint", idioma="en", canal="github", ano=2019, titulo="Trump rallies and hate crimes: a comment (lido em rodada anterior)"),
 "B8": dict(url="https://doi.org/10.1257/app.20210211", id="10.1257/app.20210211", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2023, titulo="From Hashtag to Hate Crime (preprint 2019 lido)"),
 "B9": dict(url="https://discovery.ucl.ac.uk/10153556/1/Violent-Affections.pdf", id="10.14324/111.9781800082939", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2022, titulo="Violent Affections (Kondakov)"),
 "B10": dict(url="https://fra.europa.eu/sites/default/files/fra_uploads/fra-2024-lgbtiq-equality_en.pdf", id="fra-eu-lgbtiq-survey-iii-2024", kind="other", acesso="oa", idioma="en", canal="fonte-oficial", ano=2024, titulo="FRA LGBTIQ equality at a crossroads"),
 "B11": dict(url="https://doi.org/10.34019/1981-2140.2021.29394", id="10.34019/1981-2140.2021.29394", kind="doi", acesso="oa", idioma="pt", canal="crossref", ano=2021, titulo="Percepcao do impacto das eleicoes 2018 sobre a violencia contra LGBT"),
 "B12": dict(url="https://www.gov.br/mdh/pt-br/assuntos/noticias/2020-2/junho/balanco-anual-disque-100-atendeu-2-7-milhoes-de-ligacoes-em-2019/copy_of_Relatorio_Disque_100_final.pdf", id="mdhc-disque-direitos-humanos-relatorio-2019", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2020, titulo="Disque Direitos Humanos Relatorio 2019"),
 "B13": dict(url="https://doi.org/10.1590/s2237-96222024v33e2024296.especial.en", id="10.1590/s2237-96222024v33e2024296.especial.en", kind="doi", acesso="oa", idioma="en", canal="scielo", ano=2024, titulo="Temporal trend of violence in the transgender population (Marinho Neto et al.)"),
 "B14": dict(url="https://doi.org/10.1007/s13178-026-01331-8", id="10.1007/s13178-026-01331-8", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2026, titulo="Family and IPV reports against LGBT population in Brazil"),
 "B15": dict(url="https://doi.org/10.2471/BLT.17.197251", id="10.2471/blt.17.197251", kind="doi", acesso="oa", idioma="en", canal="pubmed", ano=2018, titulo="Violence motivated by perception of SOGI: systematic review"),
 "B16": dict(url="https://doi.org/10.1371/journal.pone.0147156", id="10.1371/journal.pone.0147156", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2016, titulo="Human rights violations among MSM in Southern Africa"),
 "B17": dict(url="https://doi.org/10.2139/ssrn.3102652", id="10.2139/ssrn.3102652", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2018, titulo="The Effect of President Trump's Election on Hate Crimes"),
 "C1": dict(url="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/decreto/D9883.htm", id="decreto-9883-2019", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2019, titulo="Decreto 9.883/2019 Conselho Nacional de Combate a Discriminacao"),
 "C2": dict(url="https://doi.org/10.1590/dados.2024.67.4.339", id="10.1590/dados.2024.67.4.339", kind="doi", acesso="oa", idioma="en", canal="scielo", ano=2024, titulo="Between Deinstitutionalization and Resilience (Dados)"),
 "C3": dict(url="https://doi.org/10.1007/s13178-023-00931-y", id="10.1007/s13178-023-00931-y", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2024, titulo="Paths Towards LGBT Rights Recognition in Brazil"),
 "C4": dict(url="https://doi.org/10.17645/pag.v10i4.5871", id="10.17645/pag.v10i4.5871", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2022, titulo="The Anti-Homophobia Bill (PLC 122) in Brazil"),
 "C5": dict(url="https://www.oas.org/pt/cidh/relatorios/pdfs/Brasil2021-pt.pdf", id="cidh-brasil-2021", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2021, titulo="CIDH Situacao dos direitos humanos no Brasil"),
 "C6": dict(url="https://portal.stf.jus.br/processos/downloadPeca.asp?id=15344606459&ext=.pdf", id="stf-ado-26-mi-4733", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2019, titulo="STF ADO 26 e MI 4733 acordao"),
 "C7": dict(url="https://portal.stf.jus.br/processos/downloadPeca.asp?id=15339649246&ext=.pdf", id="stf-adi-4275-acordao", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2018, titulo="STF ADI 4275 acordao inteiro teor"),
 "C8": dict(url="https://doi.org/10.1016/s2352-3018(15)00078-8", id="10.1016/s2352-3018(15)00078-8", kind="doi", acesso="oa", idioma="en", canal="pubmed", ano=2015, titulo="Immediate effect of the Same-Sex Marriage Prohibition Act (TRUST cohort)"),
 "C9": dict(url="https://doi.org/10.3386/w31702", id="10.3386/w31702", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2023, titulo="Polish LGBT-free zones and population mental health"),
 "C10": dict(url="https://doi.org/10.1002/jia2.70030", id="10.1002/jia2.70030", kind="doi", acesso="oa", idioma="en", canal="pubmed", ano=2025, titulo="Impact of the Anti-Homosexuality Act on HIV service delivery in Uganda"),
 "C11": dict(url="https://doi.org/10.1371/journal.pmed.1001658", id="10.1371/journal.pmed.1001658", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2014, titulo="Pushback: anti-homosexuality laws and impacts on health"),
 "C12": dict(url="https://www.gov.br/participamaisbrasil/blob/baixar/9986", id="cndh-nota-repudio-violencia-lgbt", kind="other", acesso="oa", idioma="pt", canal="fonte-oficial", ano=2015, titulo="CNDH Nota de repudio a violencia contra LGBT"),
 "C13": dict(url="https://osf.io/8e7wh/download", id="10.31235/osf.io/8e7wh", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2023, titulo="When do local governments discriminate? LGBT Free Zones in Poland (preprint)"),
 "D1": dict(url="https://doi.org/10.1017/s0007123419000590", id="10.1017/s0007123419000590", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2021, titulo="The Trump Effect: experimental investigation of the emboldening effect"),
 "D2": dict(url="https://doi.org/10.1257/aer.20171175", id="10.1257/aer.20171175", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2020, titulo="From Extreme to Mainstream (NBER WP lido)"),
 "D3": dict(url="https://doi.org/10.1177/1948550617750735", id="10.1177/1948550617750735", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2018, titulo="Changing norms following the 2016 US presidential election"),
 "D4": dict(url="https://doi.org/10.1257/pol.20210284", id="10.1257/pol.20210284", kind="doi", acesso="wayback", idioma="en", canal="crossref", ano=2023, titulo="More than words: leaders speech and risky behavior during a pandemic"),
 "D5": dict(url="https://doi.org/10.1017/s0007123423000613", id="10.1017/s0007123423000613", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2023, titulo="Religion, sexuality politics, and Latin American electorates"),
 "D6": dict(url="https://doi.org/10.1017/s1049096524001161", id="10.1017/s1049096524001161", kind="doi", acesso="oa", idioma="en", canal="crossref", ano=2025, titulo="Gender ideology, the far right, and LGBTQ politics"),
 "D7": dict(url="https://doi.org/10.1017/s0007123419000449", id="10.1017/s0007123419000449", kind="doi", acesso="preprint", idioma="en", canal="crossref", ano=2021, titulo="Global racist contagion following Trump's election (manuscrito aceito)"),
}
# fontes SEM texto integral (acesso closed/human): id, url, ano, titulo, nota
PEND = [
 ("10.1111/ssqu.12896","https://doi.org/10.1111/ssqu.12896",2021,"Devine - Discrete events and hate crimes: Brexit (SSQ)","Wiley 403; Southampton eprints 479486 indisponivel; fila-aquisicao"),
 ("10.1111/1745-9125.12378","https://doi.org/10.1111/1745-9125.12378",2024,"Mills, Lantz, Wenger - community hate crimes (Criminology)","Wiley 403, sem copia aberta achada; fila-aquisicao"),
 ("10.1177/1477370819887511","https://doi.org/10.1177/1477370819887511",2019,"Kondakov - gay-propaganda law and violence in Russia (EJC)","Sage 403; fila-aquisicao"),
 ("10.1080/15564886.2023.2167142","https://doi.org/10.1080/15564886.2023.2167142",2023,"Katsuba/Kondakov - Decade of Violence, Russia (Victims & Offenders)","T&F 403 mesmo sendo OA; fila-aquisicao"),
 ("10.1016/s2468-2667(23)00312-2","https://doi.org/10.1016/s2468-2667(23)00312-2",2024,"Structural stigma and LGBTQ+ health: narrative review (Lancet Public Health)","pendente de aquisicao-out3 ou fila"),
 ("10.1177/10780874251382453","https://doi.org/10.1177/10780874251382453",2025,"Stenberg & O'Dwyer - LGBT Free Zones diffusion (Urban Affairs Review)","versao publicada sem texto; preprint OSF lido (C13)"),
 ("10.1177/08862605241303957","https://doi.org/10.1177/08862605241303957",2024,"Sexual orientation-motivated violent victimizations in Brazil, PNS 2019 (J Interpers Violence)","Sage restrito; frente A tambem falhou; fila-aquisicao"),
]
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
def emit(rec, nota):
    a = [PY, EMIT, "--out", OUT, "--url", rec["url"], "--id", rec["id"], "--id-kind", rec["kind"], "--acesso", rec["acesso"],
         "--idioma", rec["idioma"], "--canal", rec["canal"], "--titulo", rec["titulo"], "--ano", str(rec["ano"]),
         "--origem", "rodada3-F8-literatura", "--nota", nota]
    if rec.get("sha"): a += ["--sha256", rec["sha"]]
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: print("ERRO", rec["id"], r.stderr[:300]); sys.exit(1)
dst = os.path.join(OUT, "sources.jsonl")
if os.path.exists(dst): os.remove(dst)
n = 0
for r in rows.ROWS:
    m = dict(M[r["id"]]); m["sha"] = sha(r["file"])
    emit(m, f"linha {r['id']}; nivel {r['nivel']}; arquivo={r['file']}; q1={r['q1']}")
    n += 1
for (i,u,ano,t,nota) in PEND:
    emit(dict(url=u,id=i,kind="doi",acesso="closed",idioma="en",canal="crossref",ano=ano,titulo=t), "SEM TEXTO INTEGRAL: "+nota)
    n += 1
print("emitidas", n)
