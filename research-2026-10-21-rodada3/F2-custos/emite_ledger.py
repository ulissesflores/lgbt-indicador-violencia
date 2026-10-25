#!/opt/homebrew/bin/python3.14
"""Emite o ledger sources.jsonl da frente F2 SOMENTE pela porta oficial (emit_sources.py). Rodar uma vez; apaga e recria sources.jsonl."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import hashlib, json, subprocess
from pathlib import Path
R = Path((REPO_ROOT + "/fontes/q1-textointegral/F2"))
OUT = Path(__file__).resolve().parent
X = _os.environ.get("EMIT_SOURCES", "emit_sources.py")
(OUT / "sources.jsonl").unlink(missing_ok=True)
sha = lambda rel: hashlib.sha256((R / rel).read_bytes()).hexdigest() if rel else None
# (url, id, id_kind, acesso, idioma, canal, titulo, ano, arquivo_local, nota)
S = [
 ("https://www.ibge.gov.br/np_download/novoportal/documentos_institucionais/ted/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "ted119-2023-pns-minuta", "url", "oa", "pt", "ibge", "Plano de Trabalho do TED n.o XX/2023 (MS-IBGE): Pesquisa Nacional da Saude 2024 [MINUTA]", 2023, "custos/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "valor R$ 22.291.444,00; minuta; so abre com www."),
 ("https://www.ibge.gov.br/np_download/novoportal/documentos_institucionais/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "ted02-2021-mj-ibge", "url", "oa", "pt", "ibge", "Plano de Trabalho do TED 02/2021 MJSP-IBGE: Aspectos da Vitimizacao e da Seguranca (modulos PNAD Continua)", 2021, "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "R$ 3.596.904,00"),
 ("https://www.gov.br/mds/pt-br/acesso-a-informacao/licitacoes-e-contratos/termos-de-cooperacao-e-termos-de-execucao-descentralizada/CadastroTEDIBGE2023EspelhoTransferegov.pdf", "ted-mds-ibge-2023", "url", "oa", "pt", "gov-br", "Espelho Transferegov: TED MDS-IBGE 2023, modulo PNAD Continua (seguranca alimentar)", 2023, "custos/MDS_CadastroTEDIBGE2023_Transferegov.pdf", "R$ 3.797.283,00"),
 ("https://biblioteca.ibge.gov.br/visualizacao/livros/liv101726.pdf", "liv101726", "url", "oa", "pt", "ibge", "PNAD COVID19: plano amostral e ponderacao (amostra-base PNADC 211.000 domicilios)", 2020, "custos/liv101726.pdf", ""),
 ("https://biblioteca.ibge.gov.br/visualizacao/periodicos/3100/rdpc_2023.pdf", "rdpc2023", "url", "oa", "pt", "ibge", "Rendimento domiciliar per capita 2023: notas metodologicas PNAD Continua (rotacao 1-2(5))", 2024, "custos/IBGE_rdpc_2023.pdf", ""),
 ("https://biblioteca.ibge.gov.br/visualizacao/livros/liv101988.pdf", "liv101988", "url", "oa", "pt", "ibge", "PNAD Continua Nota tecnica 05/2022: modulos Sensacao de seguranca e Furtos e roubos 2021", 2022, "custos/liv101988.pdf", ""),
 ("https://biblioteca.ibge.gov.br/visualizacao/livros/liv101800.pdf", "liv101800", "url", "oa", "pt", "ibge", "PNS 2019: Acidentes, violencias, doencas transmissiveis, atividade sexual (plano amostral, 108.525 domicilios)", 2020, "pns2019/liv101800.pdf", ""),
 ("https://biblioteca.ibge.gov.br/visualizacao/livros/liv101846.pdf", "liv101846", "url", "oa", "pt", "ibge", "PNS 2019: Ciclos de vida (notas tecnicas: DMC smartphones, Conep ago/2019)", 2021, "pns2019/liv101846.pdf", ""),
 ("https://ftp.ibge.gov.br/PNS/2019/Microdados/Dados/PNS_2019_20220525.zip", "pns2019-microdados", "url", "oa", "pt", "ibge-ftp", "Microdados PNS 2019 (20220525)", 2022, "pns2019/PNS_2019_20220525.zip", "usado em deff_pns2019.py"),
 ("https://ftp.ibge.gov.br/PNS/2019/Microdados/Documentacao/Dicionario_e_input_20220530.zip", "pns2019-dicionario", "url", "oa", "pt", "ibge-ftp", "Dicionario e input PNS 2019", 2022, "pns2019/Dicionario_e_input_20220530.zip", ""),
 ("https://www.pns.icict.fiocruz.br/wp-content/uploads/2021/02/Questionario-PNS-2019.pdf", "questionario-pns2019", "url", "oa", "pt", "fiocruz", "Questionario PNS 2019 (modulos V e Y; item Y8 orientacao sexual)", 2019, "sogi/Questionario-PNS-2019.pdf", "V1/V1a p.68; Y8 p.72"),
 ("https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/db450d396a021e9bebabb1b436dcd7f8.pdf", "pnds2023-lancamento", "url", "oa", "pt", "ibge", "Lancamento da PNDS 2023 (133 mil domicilios; orientacao sexual e identidade de genero 18+)", 2023, "sogi/IBGE_PNDS2023_lancamento.pdf", ""),
 ("https://doi.org/10.1590/1980-549720230005.supl.1", "10.1590/1980-549720230005.supl.1", "doi", "oa", "en", "scielo", "Violence against LGB+ people in Brazil: analysis of the 2019 National Survey of Health (Vasconcelos et al.)", 2023, "../../pns-vasconcelos/vasconcelos.html", "Q2 em 2023 (tabela 2026-10-10); usado so para conferir o script (IC publicados)"),
 ("https://www.find-tender.service.gov.uk/Notice/019482-2022", "ft-019482-2022", "url", "oa", "en", "find-a-tender", "CSEW contract PU-18/0001: modification notice 2022/S 000-019482", 2022, "custos/FT-019482-2022.html", ""),
 ("https://www.find-tender.service.gov.uk/Notice/017318-2022", "ft-017318-2022", "url", "oa", "en", "find-a-tender", "CSEW 2024-2029: prior information notice 2022/S 000-017318", 2022, "custos/FT-017318-2022.html", ""),
 ("https://www.find-tender.service.gov.uk/Notice/013329-2025", "ft-013329-2025", "url", "oa", "en", "find-a-tender", "CSEW: contract change notice 2025/S 000-013329 (Verian)", 2025, "custos/FT-013329-2025.html", ""),
 ("https://www.find-tender.service.gov.uk/Notice/019477-2022", "ft-019477-2022", "url", "oa", "en", "find-a-tender", "CSEW: notice 2022/S 000-019477 (valor apos modificacao)", 2022, "custos/FT-019477-2022.html", "lido; valores coincidem com 019482"),
 ("https://obamawhitehouse.archives.gov/omb/statistical-programs-2014", "omb-statprog-2014", "url", "oa", "en", "omb", "Statistical Programs of the United States Government FY2014 (NCVS $36.0M)", 2014, "custos/OMB_stat2014.html", ""),
 ("https://bjs.ojp.gov/content/pub/pdf/cv13.pdf", "bjs-cv13", "url", "oa", "en", "bjs", "Criminal Victimization, 2013 (BJS NCJ 247648)", 2014, "custos/BJS_cv13.pdf", "90.630 domicilios, 160.040 pessoas"),
 ("https://ted.europa.eu/en/notice/732580-2022", "ted-732580-2022", "url", "oa", "en", "ted-api", "TED API: EU-LGBTIQ III survey, contract award notice (EUR 800.000)", 2022, "custos/TEDAPI-732580-2022.json", ""),
 ("https://ted.europa.eu/en/notice/732639-2022", "ted-732639-2022", "url", "oa", "en", "ted-api", "TED API: Violence against Women Survey II, contract award notice (EUR 2.100.000)", 2022, "custos/TEDAPI-732639-2022.json", ""),
 ("https://search.open.canada.ca/qpnotes/record/wage%2CWAGE-2019-QP-00021", "qp-wage-2019-00021", "url", "oa", "en", "open-canada", "Question Period Note: Survey of Safety in Public and Private Spaces, 2018 ($9.6M)", 2019, "custos/QP-2019-00021.html", ""),
 ("https://www.contractsfinder.service.gov.uk/Notice/380ef02e-39ac-4210-8d17-375ec5697b11", "cf-gsgb-2025", "url", "oa", "en", "contracts-finder", "Gambling Survey for Great Britain: awarded contract notice (GBP 4.5M)", 2025, "custos/CF_GSGB.html", ""),
 ("https://www.gamblingcommission.gov.uk/statistics-and-research/publication/statistics-on-gambling-participation-annual-report-year-2-2024-official", "gsgb-year2", "url", "oa", "en", "gambling-commission", "Statistics on gambling participation annual report year 2 (2024): 19,714 adults, push-to-web", 2025, "custos/GC_GSGB_year2.html", ""),
 ("https://www.gamblingcommission.gov.uk/report/gambling-survey-for-great-britain-technical-report/gsgb-2024-technical-report-methodology", "gsgb-tech", "url", "oa", "en", "gambling-commission", "GSGB technical report: methodology (address-level response 19%)", 2025, "custos/GC_GSGB_tech.html", ""),
 ("https://apisidra.ibge.gov.br/values/t/1737/n1/1/v/2266/p/201801-202609?formato=json", "sidra1737", "url", "oa", "pt", "sidra", "IPCA numero-indice (SIDRA 1737, v2266), 2018-01 a 2026-09", 2026, "custos/sidra1737_ipca_indice.json", ""),
 ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/", "ptax-bcb", "url", "oa", "pt", "bcb", "PTAX BCB 2026-10-20 (GBP; USD, EUR e CAD em arquivos irmaos)", 2026, "custos/ptax_GBP_2026-10-20.json", ""),
 ("https://nap.nationalacademies.org/read/26424", "nasem-26424", "url", "oa", "en", "nap-edu", "Measuring Sex, Gender Identity, and Sexual Orientation (NASEM 2022): texto das paginas HTML do leitor NAP", 2022, "sogi/nasem2022_texto.txt", "texto extraido das paginas 'html' do leitor; pag. = numeracao do leitor NAP; DOI 10.17226/26424"),
 ("https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/genderidentity/methodologies/collectingandprocessingdataongenderidentityenglandandwalescensus2021", "ons-genderid-census2021", "url", "oa", "en", "ons", "ONS: Collecting and processing data on gender identity, Census 2021 (94% responderam)", 2023, "sogi/ONS_gender_identity_census2021_method.html", ""),
 ("https://doi.org/10.1093/poq/nfj023", "10.1093/poq/nfj023", "doi", "oa", "en", "unpaywall", "Same-gender sex in the United States: impact of T-ACASI on prevalence estimates (Villarroel et al.)", 2006, "sogi/10.1093_poq_nfj023.pdf", "Public Opinion Quarterly; quartil=nao_verificado; manuscrito do autor (PMC)"),
 ("https://doi.org/10.2478/jos-2019-0034", "10.2478/jos-2019-0034", "doi", "oa", "en", "unpaywall", "Asking about Sexual Identity on the National Health Interview Survey: Does Mode Matter? (Dahlhamer et al.)", 2019, "sogi/10.2478_jos-2019-0034.pdf", "J Official Statistics; quartil=nao_verificado"),
 ("https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm", "lgpd-13709", "url", "oa", "pt", "planalto", "Lei 13.709/2018 (LGPD) compilada", 2018, "legal/LGPD_l13709.html", "arts. 4, 5 II e XVIII, 7, 11, 13"),
 ("https://www.planalto.gov.br/ccivil_03/leis/l5534.htm", "lei5534-1968", "url", "oa", "pt", "planalto", "Lei 5.534/1968: obrigatoriedade de prestacao de informacoes estatisticas e sigilo", 1968, "legal/Lei5534_1968.html", ""),
 ("https://www.gov.br/conselho-nacional-de-saude/pt-br/atos-normativos/resolucoes/2012/resolucao-no-466.pdf", "cns466-2012", "url", "oa", "pt", "gov-br", "Resolucao CNS 466/2012", 2012, "legal/CNS466_2012.pdf", ""),
 ("https://www.gov.br/conselho-nacional-de-saude/pt-br/atos-normativos/resolucoes/2016/resolucao-no-510.pdf", "cns510-2016", "url", "oa", "pt", "gov-br", "Resolucao CNS 510/2016", 2016, "legal/CNS510_2016_gov.pdf", ""),
 ("https://www.ufrgs.br/cep/wp-content/uploads/2022/07/Oficio_Circular_0027884544.html", "conep-oficio-17-2022", "url", "oa", "pt", "ufrgs-cep", "Oficio-Circular CONEP 17/2022 (orientacoes sobre o art. 1 da Res. CNS 510/2016): copia institucional", 2022, "legal/CONEP_OficioCircular17-2022.html", "copia da UFRGS; original no site do CNS nao aberto"),
 ("https://doi.org/10.1037/0033-2909.133.5.859", "10.1037/0033-2909.133.5.859", "doi", "closed", "en", "crossref", "Sensitive questions in surveys (Tourangeau & Yan)", 2007, None, "NAO LIDO; Psychological Bulletin Q1 (tabela 2026-10-11); acquire_fulltext: ForbiddenHost no degrau s2 -> fila-aquisicao"),
 ("https://doi.org/10.1080/00224499.2012.690110", "10.1080/00224499.2012.690110", "doi", "closed", "en", "crossref", "A two-question method for assessing gender categories in the social and medical sciences (Tate et al.)", 2013, None, "NAO LIDO; J Sex Res Q1 (tabela 2026-10-10); fila-aquisicao"),
 ("https://doi.org/10.1093/aje/kwae341", "10.1093/aje/kwae341", "doi", "closed", "en", "crossref", "Comparing two-step approaches to measuring gender identity: reliability and applications", 2024, None, "NAO LIDO; quartil=nao_verificado; fila-aquisicao"),
 ("https://doi.org/10.1215/23289252-2848877", "10.1215/23289252-2848877", "doi", "closed", "en", "crossref", "Counting Transgender and Gender-Nonconforming Adults in Health Research: Recommendations from GenIUSS", 2015, None, "NAO LIDO; quartil=nao_verificado; fila-aquisicao"),
]
n = 0
for (url, i, kind, acc, lang, canal, tit, ano, arq, nota) in S:
    cmd = ["/opt/homebrew/bin/python3.14", X, "--out", str(OUT), "--url", url, "--id", i, "--id-kind", kind, "--acesso", acc, "--idioma", lang, "--canal", canal,
           "--titulo", tit, "--ano", str(ano), "--origem", "rodada3-F2", "--nota", nota]
    if arq:
        assert (R / arq).exists(), arq
        cmd += ["--sha256", sha(arq)]
    subprocess.run(cmd, check=True, capture_output=True); n += 1
print(n, "registros emitidos em", OUT / "sources.jsonl")
