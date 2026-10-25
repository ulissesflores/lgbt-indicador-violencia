"""Escreve sources.jsonl desta frente SO via emit_sources.py (porta unica). Calcula sha256 dos arquivos em disco."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import hashlib, os, subprocess, sys
ROOT = (REPO_ROOT + "/")
F = ROOT + "fontes/q1-textointegral/discurso/governos/"
F8 = ROOT + "fontes/q1-textointegral/F8-literatura/"
OUT = ROOT + "research-2026-10-21-rodada3/discurso/governos"
EM = _os.environ.get("EMIT_SOURCES", "emit_sources.py")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def emit(path, url, id_, idk, acesso, idioma, canal, titulo, ano, nota, lic=None):
    assert os.path.exists(path), path
    cmd = ["/opt/homebrew/bin/python3.14", "-I", EM, "--out", OUT, "--url", url, "--id", id_, "--id-kind", idk, "--acesso", acesso, "--sha256", sha(path),
           "--idioma", idioma, "--canal", canal, "--titulo", titulo, "--ano", str(ano), "--origem", "rodada3-discurso-governos", "--nota", f"arquivo={path}; {nota}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print("ERRO", id_, r.stderr[:200], file=sys.stderr)
L = []
A = L.append
# ILGA
A((F + "ilga-db-csssa-all.json", "https://database.ilga.org/graphql", "ilga-db-graphql-entriesCsssa-2026-10-22", "other", "oa", "en", "ilga-database", "ILGA World Database: criminalisation of consensual same-sex sexual acts (GraphQL entriesCsssa, todos os 364 registros)", 2026, "consulta publica sem login, 2026-10-22T21:19:21Z; universo U1/U3"))
A((F + "ilga-db-enforcement-dp-countries.json", "https://database.ilga.org/graphql", "ilga-db-graphql-enforcement-13paises-2026-10-22", "other", "oa", "en", "ilga-database", "ILGA World Database: enforcement text + sources, 13 jurisdicoes", 2026, "consulta publica sem login; contagens ILGA = L3_declarado"))
A((F + "ilga-laws-on-us-2024.pdf", "https://ilga.org/wp-content/uploads/2024/05/Laws_On_Us_2024.pdf", "ilga-laws-on-us-2024", "url", "oa", "en", "ilga-world", "Laws on Us 2024: A Global Overview of Legal Progress and Backtracking", 2024, "relatorio ILGA, jan/2023-abr/2024"))
A((F + "ilga-ssh-2020-dec-update.pdf", "https://www.ecoi.net/en/file/local/2044751/ILGA_World_State_Sponsored_Homophobia_report_global_legislation_overview_update_December_2020.pdf", "ilga-ssh-2020-12", "url", "oa", "en", "ilga-world", "State-Sponsored Homophobia 2020 global legislation overview update (ultimo da serie SSH)", 2020, "copia ecoi.net do PDF de ilga.org"))
A((F + "ilga-news-pride-2026.html", "https://ilga.org/news/pride-month-2026-lgbti-maps-data/", "ilga-news-pride-2026", "url", "oa", "en", "ilga-world", "Pride Month: new ILGA World data and maps (01/06/2026)", 2026, "65 criminalizam; 7 pena de morte legal + 5 sem certeza"))
A((F + "ilga-news-pride-2025.html", "https://ilga.org/news/pride-month-2025-lgbti-data-maps/", "ilga-news-pride-2025", "url", "oa", "en", "ilga-world", "Pride Month 2025: ILGA World data and maps", 2025, "baixado; nao usado em citacao"))
# V-Dem
for fn, nm in [("vdemdata-vdem.RData", "V-Dem country-year v16 (pacote vdemdata)"), ("vdemdata-vparty.RData", "V-Party v2 (pacote vdemdata)"), ("vdemdata-codebook.RData", "V-Dem codebook (pacote vdemdata)")]:
    A((F + fn, "https://raw.githubusercontent.com/vdeminstitute/vdemdata/master/data/" + fn.replace("vdemdata-", ""), "vdemdata-16.0-" + fn.replace("vdemdata-", "").replace(".RData", ""), "url", "oa", "en", "v-dem", nm, 2026, "github.com/vdeminstitute/vdemdata, DESCRIPTION Version 16.0; sem formulario"))
# ONU
for s, t, a in [("A_HRC_43_61", "A/HRC/43/61 Situation of human rights in the Islamic Republic of Iran (SR J. Rehman)", 2020), ("A_HRC_46_50", "A/HRC/46/50 Situation of human rights in the Islamic Republic of Iran (SR)", 2021), ("A_HRC_52_67", "A/HRC/52/67 (baixado; nao usado)", 2023), ("A_HRC_53_21", "A/HRC/53/21 Afghanistan (SR; nao cita LGBT)", 2023)]:
    A((F + f"onu/{s}.pdf", "https://documents.un.org/api/symbol/access?s=" + s.replace("_", "/") + "&l=en&t=pdf", "un-" + s, "url", "oa", "en", "onu-ods", t, a, "documento oficial ONU via ODS"))
# primarias
A((F + "primarias/uganda-aha-2023-parlamento.pdf", "https://www.parliament.go.ug/sites/default/files/The%20Anti-Homosexuality%20Act%2C%202023.pdf", "uganda-aha-2023", "url", "oa", "en", "fonte-oficial", "The Anti-Homosexuality Act, 2023 (Parlamento de Uganda)", 2023, "PDF escaneado; OCR local em uganda-aha-2023-parlamento.ocr.txt; s.3 'suffer death' na p.8"))
A((F + "primarias/amnesty-yemen-2024-02.html", "https://www.amnesty.org/en/latest/news/2024/02/yemen-huthis-must-stop-executions-and-release-dozens-facing-lgbti-charges/", "amnesty-yemen-2024-02-09", "url", "oa", "en", "ong", "Yemen: Huthis must stop executions and release dozens facing LGBTI charges (9/2/2024)", 2024, "ONG; contagem declarada"))
A((F + "primarias/ushmm-persecution-of-homosexuals-in-the-third-reich.html", "https://encyclopedia.ushmm.org/content/en/article/persecution-of-homosexuals-in-the-third-reich", "ushmm-gay-men-nazi", "url", "oa", "en", "instituicao", "Gay Men under the Nazi Regime (USHMM Holocaust Encyclopedia)", 2026, "fonte institucional secundaria, nao Q1; Q1 pendente na fila"))
A((F + "primarias/boe-ley-20-2022-memoria-democratica.html", "https://www.boe.es/buscar/act.php?id=BOE-A-2022-17099", "boe-ley-20-2022", "url", "oa", "es", "fonte-oficial", "Ley 20/2022 de Memoria Democratica (BOE)", 2022, "exposicao de motivos reconhece perseguicao a pessoas LGTBI"))
A((F + "primarias/muller-2020-brunei-spco-jil.pdf", "https://doi.org/10.53484/jil.v1.muller", "10.53484/jil.v1.muller", "doi", "oa", "en", "crossref", "Brunei's Sharia Penal Code Order: Punitive Turn or the Art of Non-Punishment?", 2020, "J Islamic Law; quartil nao_verificado; via Unpaywall pela escada acquire_fulltext"))
# F8 reaproveitados
A((F8 + "osce-moscow-mechanism-chechnya-2018.pdf", "https://www.osce.org/files/Moscow%20Mechanism%20Document_ENG.pdf", "osce-odihr-gal-76-18-corr1", "url", "oa", "en", "fonte-oficial", "OSCE Moscow Mechanism report on Chechnya (Benedek, 21/12/2018)", 2018, "lido pela frente F8; citacoes reverificadas aqui"))
A((F8 + "tedh-lapunov-v-russia-2023.pdf", "https://hudoc.echr.coe.int/app/conversion/pdf/?library=ECHR&id=001-226449&filename=CASE%20OF%20LAPUNOV%20v.%20RUSSIA.pdf", "echr-28834-19", "url", "oa", "en", "fonte-oficial", "Lapunov v. Russia (ECtHR, app. 28834/19, 12/09/2023)", 2023, "lido pela frente F8"))
A((F8 + "cnv-volume2-oficial-site-cnv-via-wayback.pdf", "https://web.archive.org/web/2016id_/http://cnv.memoriasreveladas.gov.br/images/pdf/relatorio/volume_2_digital.pdf", "cnv-2014-vol2", "url", "wayback", "pt-BR", "fonte-oficial", "CNV Relatorio vol. II texto 7 Ditadura e homossexualidades", 2014, "lido pela frente F8"))
A((F8 + "10.7440_histcrit71.2019.05.pdf", "https://doi.org/10.7440/histcrit71.2019.05", "10.7440/histcrit71.2019.05", "doi", "oa", "es", "crossref", "Los primeros anos de la Revolucion cubana y las UMAP (Garces Marrero)", 2019, "quartil nao_verificado; lido pela frente F8"))
A((F8 + "kondakov-2022-violent-affections-uclpress.pdf", "https://discovery.ucl.ac.uk/10153556/1/Violent-Affections.pdf", "10.14324/111.9781800082939", "doi", "oa", "en", "crossref", "Violent Affections: Queer Sexuality, Techniques of Power, and Law in Russia (Kondakov, UCL Press)", 2022, "livro peer-reviewed OA; fora da regua Q1; p.102 recriminalizacao 1934"))
A((F8 + "mdhc-disque-direitos-humanos-relatorio-2019.pdf", "https://www.gov.br/mdh/pt-br/assuntos/noticias/2020-2/junho/balanco-anual-disque-100-atendeu-2-7-milhoes-de-ligacoes-em-2019/copy_of_Relatorio_Disque_100_final.pdf", "mdhc-disque-direitos-humanos-relatorio-2019", "url", "oa", "pt-BR", "fonte-oficial", "Disque Direitos Humanos: Relatorio 2019 (MDHC, maio/2020)", 2020, "lido pela frente F8; LGBT 1.685 -> 846"))
A((ROOT + "fontes/q1-textointegral/entregues-pelo-autor/36_10.1177_10780874251382453_publishedVersion.pdf", "https://doi.org/10.1177/10780874251382453", "10.1177/10780874251382453", "doi", "oa", "en", "crossref", "Stenberg & O'Dwyer: When Do Local Governments Discriminate? 'LGBT Free Zones' in Poland (Urban Affairs Review 62(4))", 2026, "entregue pelo autor; quartil nao_verificado"))
# Brasil
BR = F + "brasil/"
urls = {
 "aosfatos-temer-zero-homofobia-2017.html": "https://www.aosfatos.org/noticias/temer-reduz-a-zero-repasses-a-politicas-de-combate-homofobia/",
 "congressoemfoco-bolsonaro-mundo-gay-2019.html": "https://congressoemfoco.com.br/noticia/25843/governo-do-maranhao-faz-campanha-contra-turismo-sexual-apos-declaracao-de-bolsonaro",
 "congressoemfoco-bolsonaro-mundo-gay-materia.html": "https://congressoemfoco.com.br/noticia/25843/governo-do-maranhao-faz-campanha-contra-turismo-sexual-apos-declaracao-de-bolsonaro",
 "congressoemfoco-bolsonaro-stf-homofobia-2019-06-14.html": "https://www.congressoemfoco.com.br/area/governo/para-bolsonaro-criminalizacao-da-homofobia-prejudica-homossexuais/",
 "congressoemfoco-lider-lgbt-damares-2019-01.html": "https://www.congressoemfoco.com.br/noticia/26477/lider-lgbt-ve-confusao-em-analise-de-nova-estrutura-de-ministerio-e-descarta-prejuizo-para-comunidade",
 "congressoemfoco-quem-financia-lgbti-2025.html": "https://www.congressoemfoco.com.br/artigo/108513/quem-financia-as-politicas-publicas-lgbti-no-brasil",
 "cut-disque100-2017.html": "https://www.cut.org.br/noticias/disque-100-recebeu-142-mil-denuncias-de-violacoes-de-direitos-humanos-em-2017-22f2",
 "emol-bolsonaro-2019.html": "https://www.emol.com/noticias/Internacional/2019/04/26/945941/Bolsonaro-asegura-que-No-podemos-dejar-que-Brasil-sea-conocido-como-un-paraiso-para-el-turismo-gay.html",
 "exame-dilma-kit-2011.html": "https://exame.com/brasil/apos-pressao-religiosa-dilma-suspende-producao-de-kit-homofobia/",
 "ihu-dilma-kit-frase-2011.html": "https://ihu.unisinos.br/noticias/43726-frase-levou-a-suspensao-do-kit-anti-homofobia",
 "metropoles-bolsonaro-twitter-minorias-2019-01.html": "https://www.metropoles.com/brasil/politica-br/no-twitter-bolsonaro-diz-que-minorias-nao-perderao-direitos",
 "mpf-disque100-trans.html": "https://www.mpf.mp.br/o-mpf/unidades/pr-ac/noticias/mpf-apura-falhas-no-atendimento-do-201cdisque-100201d-a-pessoas-trans",
 "opovo-bolsonaro-stf-2019-06-14.html": "https://www.opovo.com.br/noticias/politica/2019/06/14/bolsonaro-critica-decisao-do-stf-de-criminalizar-homofobia.html",
 "sul21-mp870-2019.html": "https://www.sul21.com.br/ultimas-noticias/politica/2019/01/bolsonaro-exclui-politicas-para-lgbts-das-diretrizes-do-ministerio-de-direitos-humanos/",
 "agenciabrasil-lgbt-disque-2024-10.html": "https://agenciabrasil.ebc.com.br/direitos-humanos/noticia/2024-10/populacao-lgbtqia-denuncia-mais-casos-de-violencia-no-pais",
}
for fn, u in urls.items():
    A((BR + fn, u, fn.replace(".html", ""), "url", "oa", "pt-BR", "imprensa", fn.replace(".html", "").replace("-", " "), int(fn.split("-")[-1][:4]) if fn.split("-")[-1][:4].isdigit() else 2019, "imprensa/veiculo da fala; cita como contagem declarada ou fato nomeado"))
plan = {"planalto-decreto11341-2023": "ato2023-2026/2023/decreto/D11341", "planalto-decreto11471-2023": "ato2023-2026/2023/decreto/D11471", "planalto-decreto8727-2016": "ato2015-2018/2016/decreto/D8727",
        "planalto-decreto9673-2019": "ato2019-2022/2019/decreto/D9673", "planalto-decreto9883-2019": "ato2019-2022/2019/decreto/D9883", "planalto-lei13502-2017": "ato2015-2018/2017/lei/l13502",
        "planalto-lei13844-2019": "ato2019-2022/2019/lei/l13844", "planalto-lei14600-2023": "ato2023-2026/2023/lei/L14600", "planalto-mpv870-2019": "ato2019-2022/2019/mpv/mpv870",
        "planalto-lei10683-2003": "leis/2003/l10.683", "planalto-lei13266-2016": "ato2015-2018/2016/lei/l13266", "planalto-lei13341-2016": "ato2015-2018/2016/lei/L13341", "planalto-decreto8785-2016": "ato2015-2018/2016/decreto/D8785"}
for k, p in plan.items():
    A((BR + k + ".html", "https://www.planalto.gov.br/ccivil_03/" + p + ".htm", k, "url", "oa", "pt-BR", "fonte-oficial", k.replace("-", " ") + " (Planalto)", int(k[-4:]), "norma oficial; texto da pagina do Planalto"))
for a in L: emit(*a)
print(len(L), "entradas")
