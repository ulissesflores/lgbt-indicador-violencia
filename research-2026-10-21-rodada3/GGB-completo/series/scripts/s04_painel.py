"""Monta series/painel_mortes_lgbt.csv (fonte x ano x categoria) a partir de DOCUMENTOS PUBLICOS ja baixados.
Cada linha carrega: trecho verbatim (validado por busca no texto do PDF), pagina (indice do PDF), caminho absoluto, sha256, URL.
Se um trecho nao for encontrado, o script ABORTA (nao ha linha sem prova). Python 3.14 stdlib + pdftotext.
Uso: /opt/homebrew/bin/python3.14 -I s04_painel.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, json, pathlib, re, subprocess, sys

BASE = pathlib.Path(REPO_ROOT)
RAW = BASE / "fontes/p3-ggb/_raw"
OUT = pathlib.Path((REPO_ROOT + "/research-2026-10-21-rodada3/GGB-completo/series"))
G = "https://grupogaydabahia.com.br/wp-content/uploads/"
GB = G + "bsk-pdf-manager/2024/02/"
A = "https://antrabrasil.org/wp-content/uploads/"

# chave: (caminho, url, titulo, canal)
DOCS = {
 "ggb2011": (RAW/"pdf_ggb_old/ggb2011.pdf", GB+"relatc3b3rio-2011.pdf", "GGB/Homofobia Mata, Relatorio 2011", "ong"),
 "ggb2012": (RAW/"pdf_ggb_old/ggb2012.pdf", "https://homofobiamata.wordpress.com/wp-content/uploads/2020/02/relatorio-2012.pdf", "GGB/Homofobia Mata, Relatorio 2012 (blog Homofobia Mata)", "ong"),
 "ggb2016": (RAW/"pdf_ggb_old/ggb2016.pdf", "https://homofobiamata.wordpress.com/wp-content/uploads/2020/02/relatc3b3rio.2016.pdf", "GGB/Homofobia Mata, Relatorio 2016 (blog Homofobia Mata)", "ong"),
 "ggb2013": (RAW/"pdf_ggb_old/ggb2013.pdf", GB+"relatorio-2013.pdf", "GGB/Homofobia Mata, Relatorio 2013", "ong"),
 "ggb2014": (RAW/"pdf_ggb_old/ggb2014.pdf", GB+"relatorio-2014.pdf", "GGB/Homofobia Mata, Relatorio 2014", "ong"),
 "ggb2015": (RAW/"pdf_ggb_old/ggb2015.pdf", GB+"relatc3b3rio-2015.pdf", "GGB/Homofobia Mata, Relatorio 2015", "ong"),
 "ggb2017": (RAW/"pdf/ggb2017.pdf", GB+"relatorio-2017.pdf", "GGB, Mortes de LGBT no Brasil 2017", "ong"),
 "ggb2018": (RAW/"pdf/ggb2018.pdf", GB+"relatorio-2018.pdf", "GGB, Mortes de LGBT no Brasil 2018", "ong"),
 "ggb2019": (RAW/"pdf/ggb2019.pdf", GB+"relatorio-2019.pdf", "GGB, Mortes violentas de LGBT+ no Brasil 2019", "ong"),
 "ggb2020": (RAW/"pdf/ggb2020.pdf", GB+"relatorio-2020.pdf", "Acontece LGBTI+/GGB, Observatorio das Mortes Violentas de LGBTI+ 2020", "ong"),
 "ggb2021": (RAW/"pdf/ggb2021.pdf", GB+"mortes-violentas-de-lgbt-2021-versao-final.pdf", "GGB, Mortes violentas de LGBT 2021", "ong"),
 "ggb2022s": (RAW/"pdf/ggb2022.pdf", GB+"relatorio2022.pdf", "GGB, balanco 1o semestre 2022", "ong"),
 "ggb2023": (RAW/"pdf/ggb2023.pdf", GB+"observatorio-2023-de-mortes-violentas-de-lgbt-1.pdf", "GGB, Observatorio 2023 (release)", "ong"),
 "ggb2024": (RAW/"pdf/ggb2024.pdf", G+"2025/01/Observatorio_2024_de_Mortes_Violentas_de_LGBT-release-20-jan.-2024.pdf", "GGB, Observatorio 2024 (release)", "ong"),
 "ggb2025": (RAW/"pdf/ggb2025.pdf", G+"2026/01/RELEASE-Mortes-Violentas-de-LGBT%5EM%5EJ-2025-GGB.pdf", "GGB, Mortes violentas de LGBT 2025 (release)", "ong"),
 "antra2017": (RAW/"pdf/antra2017.pdf", A+"2018/02/relatc3b3rio-mapa-dos-assassinatos-2017-antra.pdf", "ANTRA, Mapa dos assassinatos 2017", "ong"),
 "antra2018": (RAW/"pdf/antra2018.pdf", A+"2019/12/dossie-dos-assassinatos-e-violencia-contra-pessoas-trans-em-2018.pdf", "ANTRA, Dossie 2018", "ong"),
 "antra2019": (RAW/"pdf/antra2019.pdf", A+"2020/01/dossic3aa-dos-assassinatos-e-da-violc3aancia-contra-pessoas-trans-em-2019.pdf", "ANTRA, Dossie 2019", "ong"),
 "antra2020": (RAW/"pdf/antra2020.pdf", A+"2021/01/dossie-trans-2021-29jan2021.pdf", "ANTRA, Dossie 2020 (pub. 2021)", "ong"),
 "antra2021": (RAW/"pdf_antra2126/dossieantra2022-web.pdf", A+"2022/01/dossieantra2022-web.pdf", "ANTRA, Dossie 2021 (pub. 2022)", "ong"),
 "antra2022": (RAW/"pdf_antra2126/dossieantra2023.pdf", A+"2023/01/dossieantra2023.pdf", "ANTRA, Dossie 2022 (pub. 2023)", "ong"),
 "antra2023": (RAW/"pdf_antra2126/dossieantra2024-web.pdf", A+"2024/01/dossieantra2024-web.pdf", "ANTRA, Dossie 2023 (pub. 2024)", "ong"),
 "antra2024": (RAW/"pdf_antra2126/dossie-antra-2025.pdf", A+"2025/01/dossie-antra-2025.pdf", "ANTRA, Dossie 2024 (pub. 2025)", "ong"),
 "antra2025": (RAW/"pdf_antra2126/dossie-antra-2026.pdf", A+"2026/01/dossie-antra-2026.pdf", "ANTRA, Dossie 2025 (pub. 2026)", "ong"),
 "obs2021": (RAW/"obs/obs2021.pdf", "https://static.poder360.com.br/2022/05/Dossie-de-Mortes-e-Violencias-Contra-LGBTI-no-Brasil-2021.pdf", "Observatorio (Acontece/ANTRA/ABGLT), Dossie 2021 (copia Poder360)", "ong"),
 "obs2022": (RAW/"obs/obs2022.pdf", "https://zenodo.org/records/7957710", "Observatorio, Dossie 2022 (copia Zenodo)", "ong"),
 "obs2023": (RAW/"obs/obs2023.pdf", "https://zenodo.org/records/14715580", "Observatorio, Dossie 2023 (copia Zenodo)", "ong"),
 "obs2026q1": (BASE/"fontes/t6-observatorio-parcial-2026q1/abglt.pdf", "https://www.abglt.org/_files/ugd/dcb2da_64aa144d3bda419fac83ce9aaad42093.pdf", "Observatorio LGBTI+ Janaina Dutra, parcial jan-mar 2026", "ong"),
 "anu2022": (BASE/"fontes/p3-ggb/anuarios/anuario2022.pdf", "https://forumseguranca.org.br/wp-content/uploads/2022/06/anuario-2022.pdf", "FBSP, Anuario 2022 (dados 2020-2021)", "oficial_ou_ong_oficial"),
 "anu2023": (BASE/"fontes/p3-ggb/anuarios/anuario2023.pdf", "https://static.poder360.com.br/2023/07/Anuario-Brasileiro-de-Seguranca-Publica-2023-Forum-Brasileiro-de-Seguranca-Publica.pdf", "FBSP, Anuario 2023 (copia Poder360)", "oficial_ou_ong_oficial"),
 "anu2024": (BASE/"fontes/t2-anuario-2024-dados2023/anuario-2024.pdf", "https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/", "FBSP, Anuario 2024 (dados 2022-2023)", "oficial_ou_ong_oficial"),
 "anu2025": (BASE/"fontes/t2-anuario-2025-dados2024/anuario-2025.pdf", "https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/", "FBSP, Anuario 2025 (dados 2023-2024)", "oficial_ou_ong_oficial"),
 "anu2026": (BASE/"fontes/t2-anuario-2026-dados2025/anuario-2026.pdf", "https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/", "FBSP, Anuario 2026 (dados 2024-2025)", "oficial_ou_ong_oficial"),
 "atlas2020": (BASE/"fontes/p3-ggb/disque100/ipea_24747b9b.pdf", "https://repositorio.ipea.gov.br/server/api/core/bitstreams/24747b9b-db29-48a0-9d8f-761006420fa6/content", "IPEA/FBSP, Atlas da Violencia 2020, cap. 6 (Disque 100/MMFDH 2011-2018)", "oficial"),
 "atlas2026": (BASE/"fontes/t1-atlas-2026/atlas2026.pdf", "https://www.ipea.gov.br/atlasviolencia/", "IPEA/FBSP, Atlas da Violencia 2026 (cap. 7, Sinan)", "oficial"),
}

_cache = {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def pages(k):
    if k not in _cache:
        p = DOCS[k][0]
        t1 = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
        t2 = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True).stdout  # ordem de leitura (PDFs em 2 colunas)
        a, b = t1.split("\f"), t2.split("\f")
        _cache[k] = [re.sub(r"\s+", " ", x + " " + (b[i] if i < len(b) else "")) for i, x in enumerate(a)], sha(p)
    return _cache[k]
def find(k, snippet):
    ps, _ = pages(k); s = re.sub(r"\s+", " ", snippet).strip()
    for i, p in enumerate(ps):
        if s in p: return i + 1
    for i in range(len(ps) - 1):  # trecho que atravessa a quebra de pagina
        if s in ps[i] + " " + ps[i + 1]: return i + 1
    return None

rows = []; FAIL = []
def R(doc, ano, cat, val, tipo, defn, snip, obs="", ano_fim=None, snip_pagina=None):
    pg = find(doc, snip_pagina or snip)
    if pg is None:
        FAIL.append(f"{doc} {ano} {cat}: {snip[:110]!r}"); return
    p, url, tit, canal = DOCS[doc]
    rows.append(dict(fonte=doc.rstrip("0123456789s") if False else doc, doc_id=doc, ano=ano, ano_fim=ano_fim or ano, categoria=cat, valor=val, tipo_contagem=tipo,
                     definicao_declarada=defn, trecho_verbatim=re.sub(r"\s+", " ", snip).strip(), pagina_pdf=pg, arquivo=str(p), sha256=pages(doc)[1], url=url, titulo=tit, observacao=obs))

# ---------------- definicoes declaradas ----------------
D_GGB = "mortes violentas de LGBT+ documentadas (homicidios + suicidios [+ latrocinios/outras causas conforme o ano]); base = noticias de midia/internet e informacoes de colaboradores; inclui heterossexuais 'confundidos'"
D_GGB_PRE = "homicidios de LGBT (gays, travestis, lesbicas) a partir de noticias de jornal e internet (Homofobia Mata); suicidios entram so a partir do relatorio 2016 segundo o GGB 2018, mas o relatorio 2013 ja inclui 10 suicidas gays"
D_ANTRA = "assassinatos de pessoas trans (travestis, mulheres trans, homens trans/transmasculinos) a partir de noticias; apos 2024 so CVLI (crimes violentos letais intencionais), descartados os demais"
D_OBS = "mortes violentas de LGBTI+ (assassinatos + suicidios + outras causas) em base compartilhada Acontece/ANTRA/ABGLT a partir de noticias"
D_ANU = "registros de homicidio doloso com vitima LGBT nas secretarias estaduais de seguranca (campo/marca de orientacao ou motivacao varia por UF; RJ, SP e outras UFs sem dado em varios anos)"

# ---------------- GGB: serie anual 2000-2019 (Tabela 1 do relatorio 2019) ----------------
tab = {2000:130,2001:132,2002:126,2003:125,2004:158,2005:135,2006:112,2007:142,2008:187,2009:199,2010:260,2011:266,2012:338,2013:314,2014:329,2015:319,2016:343,2017:445,2018:420,2019:329}
blk = "Ano N. Vítimas 2000 130 2001 132 2002 126 2003 125 2004 158 2005 135 2006 112 2007 142 2008 187 2009 199 2010 260 2011 266 2012 338 2013 314 2014 329 2015 319 2016 343 2017 445 2018 420 2019 329 Total 4809"
for y, v in tab.items():
    R("ggb2019", y, "total", v, "contagem_declarada", D_GGB, f"{y} {v}", "Tabela 1 do relatorio GGB 2019 (serie 2000-2019); bloco da tabela validado inteiro em s04", snip_pagina=blk)

# GGB: 2020 e 2021 (relatorios proprios), 2022 (nao ha anual no site), 2023-2025
R("ggb2020", 2020, "total", 237, "contagem_declarada", D_GGB, "Em 2020 registrou-se um total de 237 mortes motivadas pela LGBTIfobia")
R("ggb2021", 2021, "total", 300, "contagem_declarada", D_GGB, "contabilizam mais de seis mil mortes, dos quais 300 casos ocorreram somente em 2021")
R("ggb2023", 2023, "total", 257, "contagem_declarada", D_GGB, "257 mortes violentas documentadas, um caso a mais do registrado em 2022")
R("ggb2023", 2022, "total", 256, "derivado", "derivado: 257 (2023) menos 1 ('um caso a mais do registrado em 2022'); o GGB nao publica relatorio anual 2022 no site (so balanco do 1o semestre: 135)", "257 mortes violentas documentadas, um caso a mais do registrado em 2022",
  "o Anuario FBSP 2023 cita 256 (MOTT et al., 2023) para o GGB 2022: concorda com a derivacao")
R("ggb2022s", 2022, "total_1o_semestre", 135, "contagem_declarada", "balanco jan-jun 2022", "135 mortes violentas de LGBT+, nos primeiros seis meses de 2022", "NAO e o anual")
R("ggb2024", 2024, "total", 291, "contagem_declarada", D_GGB, "Foram registradas 291 mortes violentas, 34 casos a mais do que")
R("ggb2025", 2025, "total", 257, "contagem_declarada", D_GGB, "257 mortes violentas documentadas")

# GGB composicao por categoria (relatorios originais de cada ano)
def comp(doc, ano, itens, defn=D_GGB, extra_obs=""):
    for cat, val, snip in itens:
        R(doc, ano, cat, val, "contagem_declarada", defn, snip, extra_obs)

comp("ggb2011", 2011, [("homens_gays", 162, "Os gays lideram os “homocídios”: 162 (60%), seguidos de 98 travestis (37%) e 7 lésbicas (3%)"), ("trans_travestis", 98, "98 travestis (37%) e 7 lésbicas (3%)"), ("lesbicas", 7, "98 travestis (37%) e 7 lésbicas (3%)")], D_GGB_PRE)
comp("ggb2012", 2012, [("total_relatorio_original", 338, "Foram documentados 338 assassinatos de gays, travestis e lésbicas no Brasil"), ("homens_gays", 188, "Os gays lideram os “homocídios”: 188 (56%), seguidos de 128 travestis (37%), 19 lésbicas (5%) e 2 bissexuais (1%)"), ("trans_travestis", 128, "seguidos de 128 travestis (37%), 19 lésbicas (5%) e 2 bissexuais (1%)"), ("lesbicas", 19, "128 travestis (37%), 19 lésbicas (5%) e 2 bissexuais (1%)"), ("bissexuais", 2, "19 lésbicas (5%) e 2 bissexuais (1%)")], D_GGB_PRE)
comp("ggb2016", 2016, [("total_relatorio_original", 343, "343 LGBT (lésbicas, gays, bissexuais e transexuais) foram assassinados no Brasil em 2016"), ("homens_gays", 173, "Dos 343 assassinatos, 173 eram gays (50%), 144 (42%) trans (travestis e transexuais), 10 lésbicas (3%)"), ("trans_travestis", 144, "144 (42%) trans (travestis e transexuais), 10 lésbicas (3%)"), ("lesbicas", 10, "144 (42%) trans (travestis e transexuais), 10 lésbicas (3%)"), ("bissexuais", 4, "4 bissexuais (1%), incluindo 12 heterossexuais"), ("heterossexuais", 12, "incluindo 12 heterossexuais, como os amantes de transexuais"), ("suicidios", 26, "Nessas estatísticas foram incluídos também os suicídios de 26 LGBT")], D_GGB_PRE, "dentro do total 343 ha 26 suicidios (o texto fala 'assassinatos' e 'incluidos tambem os suicidios')")
comp("ggb2013", 2013, [("total_relatorio_original", 312, "Foram documentados 312 assassinatos de gays, travestis e lésbicas no Brasil"), ("homens_gays", 186, "Os gays lideram os “homocídios”: 186 (59%), seguidos de 108 travestis (35%), 14 lésbicas (4%), 2 bissexuais (1%) e 2 heterossexuais"), ("trans_travestis", 108, "seguidos de 108 travestis (35%), 14 lésbicas (4%), 2 bissexuais (1%) e 2 heterossexuais"), ("lesbicas", 14, "108 travestis (35%), 14 lésbicas (4%), 2 bissexuais (1%) e 2 heterossexuais"), ("bissexuais", 2, "14 lésbicas (4%), 2 bissexuais (1%) e 2 heterossexuais"), ("heterossexuais", 2, "2 bissexuais (1%) e 2 heterossexuais"), ("suicidios", 10, "Nessa lista foram incluídos 10 suicidas gays")], D_GGB_PRE, "relatorio original de 2013: total 312; Tabela 2019 = 314; relatorio 2014 diz 313")
comp("ggb2014", 2014, [("total_relatorio_original", 326, "Foram documentados 326 mortes de gays, travestis e lésbicas no Brasil, incluindo 9 suicídios"), ("suicidios", 9, "Foram documentados 326 mortes de gays, travestis e lésbicas no Brasil, incluindo 9 suicídios"), ("homens_gays", 163, "Dos 326 mortos, 163 eram gays, 134 travestis, 14 lésbicas, 3 bissexuais e 7 amantes de travestis (T-lovers)"), ("trans_travestis", 134, "163 eram gays, 134 travestis, 14 lésbicas, 3 bissexuais e 7 amantes de travestis"), ("lesbicas", 14, "134 travestis, 14 lésbicas, 3 bissexuais e 7 amantes de travestis"), ("bissexuais", 3, "14 lésbicas, 3 bissexuais e 7 amantes de travestis"), ("heterossexuais", 7, "Foram igualmente assassinados 7 heterossexuais")], D_GGB_PRE, "relatorio original de 2014: total 326; Tabela 2019 = 329. Soma das categorias do texto = 328 (163+134+14+3+7+7), nao 326")
comp("ggb2015", 2015, [("total_relatorio_original", 318, "318 LGBT foram assassinados no Brasil em 2015"), ("suicidios", 5, "Foram incluídos também 5 suicídios de homossexuais masculinos"), ("trans_travestis", 119, "as 119 travestis brasileiras assassinadas em 2015")], D_GGB_PRE, "relatorio original de 2015: total 318; Tabela 2019 = 319. Percentuais do texto (52% gays, 37% travestis, 16% lesbicas, 10% bi, 7% hetero, 1% amantes) somam 123%")
comp("ggb2017", 2017, [("homens_gays", 194, "194 eram gays (43,6%), 191 trans (42,9%), 43 lésbicas (9,7%), 5 bissexuais (1,1%) e 12 heterossexuais (2,7%)"), ("trans_travestis", 191, "191 trans (42,9%), 43 lésbicas (9,7%), 5 bissexuais (1,1%) e 12 heterossexuais"), ("lesbicas", 43, "43 lésbicas (9,7%), 5 bissexuais (1,1%) e 12 heterossexuais (2,7%)"), ("bissexuais", 5, "5 bissexuais (1,1%) e 12 heterossexuais (2,7%)"), ("heterossexuais", 12, "5 bissexuais (1,1%) e 12 heterossexuais (2,7%)"), ("homicidios", 387, "387 assassinatos e 58 suicídios"), ("suicidios", 58, "387 assassinatos e 58 suicídios")])
comp("ggb2018", 2018, [("homens_gays", 191, "predominaram as mortes de 191 Gays (45%)"), ("trans_travestis", 164, "seguido de 164 Trans (39%), 52 Lésbicas (12%), 8 Bissexuais (2%) e 5 Heterossexuais (1%)"), ("lesbicas", 52, "164 Trans (39%), 52 Lésbicas (12%), 8 Bissexuais (2%) e 5 Heterossexuais (1%)"), ("bissexuais", 8, "52 Lésbicas (12%), 8 Bissexuais (2%) e 5 Heterossexuais (1%)"), ("heterossexuais", 5, "8 Bissexuais (2%) e 5 Heterossexuais (1%)"), ("suicidios", 100, "subiu para 100 (23,8%) dos casos documentadas"), ("homicidios", 320, "320 homicídios (76%)")])
comp("ggb2019", 2019, [("homens_gays", 174, "predominaram as mortes de 174 Gays (52,8%), seguidos de 118 Travestis e Transexuais (35,8%)"), ("trans_travestis", 118, "seguidos de 118 Travestis e Transexuais (35,8%)"), ("lesbicas", 32, "32 Lésbicas (9,7%) e 5 bissexuais (1,5%)"), ("bissexuais", 5, "32 Lésbicas (9,7%) e 5 bissexuais (1,5%)"), ("homicidios", 297, "297 homicídios (90,3%) e 32 suicídios (9,8%)"), ("suicidios", 32, "297 homicídios (90,3%) e 32 suicídios (9,8%)")])
comp("ggb2020", 2020, [("trans_travestis", 161, "acumulando um total de 161 (70%) mortes motivadas pela transfobia, seguido de gays com 51 (22%) mortes motivadas pela homofobia"), ("homens_gays", 51, "seguido de gays com 51 (22%) mortes motivadas pela homofobia"), ("lesbicas", 10, "seguido de lésbicas com 10 (5%) mortes motivas pela lesbofobia"), ("homens_trans", 3, "seguido de homens trans com 3 (1%) casos de mortes motivadas pela transfobia"), ("bissexuais", 3, "bissexuais com 3 (1%) mortes motivas pela bifobia"), ("heterossexuais", 2, "2 (1%) heterossexuais que por apresentarem comportamentos"), ("homicidios", 215, "predominaram os homicídios com 215 (90,71%) registros, seguido de 13 (5,48%) suicídios"), ("suicidios", 13, "seguido de 13 (5,48%) suicídios")], D_GGB, "composicao por identidade do texto soma 230, nao 237; duas tabelas do mesmo relatorio divergem (homens trans 2 ou 3; nao informado 8 ou 7)")
comp("ggb2021", 2021, [("homens_gays", 153, "153 gays (51%), seguidos das travestis e transexuais com 110 casos (36,67%), lésbicas com 12 casos (4%)"), ("trans_travestis", 110, "seguidos das travestis e transexuais com 110 casos (36,67%), lésbicas com 12 casos (4%)"), ("lesbicas", 12, "lésbicas com 12 casos (4%), bissexuais e homens trans 4 casos (1,33%)"), ("bissexuais_e_homens_trans", 4, "bissexuais e homens trans 4 casos (1,33%)"), ("homicidios", 276, "foram documentados 276 homicídios (92%) e 24 suicídios (8%)"), ("suicidios", 24, "foram documentados 276 homicídios (92%) e 24 suicídios (8%)"), ("latrocinio_dentro_de_homicidios", 34, "Registramos 34 gays (11%) que sofreram latrocínio")], D_GGB, "composicao por identidade do texto soma 281 de 300 (19 sem classificacao no texto)")
comp("ggb2023", 2023, [("trans_travestis", 127, "documentou a morte violenta de 127 travestis e transgêneros, 118 gays, 9 lésbicas e três bissexuais, totalizando 257 vítimas"), ("homens_gays", 118, "127 travestis e transgêneros, 118 gays, 9 lésbicas e três bissexuais, totalizando 257 vítimas"), ("lesbicas", 9, "118 gays, 9 lésbicas e três bissexuais, totalizando 257 vítimas"), ("bissexuais", 3, "9 lésbicas e três bissexuais, totalizando 257 vítimas")])
comp("ggb2024", 2024, [("homens_gays", 165, "incluindo 165 gays, 96 travestis e mulheres transgêneros, 11 lésbicas, 7 bissexuais e 6 homens tans"), ("trans_travestis", 96, "165 gays, 96 travestis e mulheres transgêneros, 11 lésbicas, 7 bissexuais e 6 homens tans"), ("lesbicas", 11, "96 travestis e mulheres transgêneros, 11 lésbicas, 7 bissexuais e 6 homens tans"), ("bissexuais", 7, "11 lésbicas, 7 bissexuais e 6 homens tans"), ("homens_trans", 6, "7 bissexuais e 6 homens tans"), ("heterossexuais", 6, "Os seis (6) heterossexuais foram incluídos neste rol"), ("homicidios", 273, "Nesse total estão incluídos 273 homicídios e 18 suicídios"), ("suicidios", 18, "Nesse total estão incluídos 273 homicídios e 18 suicídios")])
comp("ggb2025", 2025, [("homens_gays", 156, "Gay 156 60,7%"), ("trans_travestis", 64, "Mulher Trans 46 17,9% Travesti 18 7,0%"), ("bissexuais", 9, "Bissexual 9 3,5%"), ("lesbicas", 4, "Lésbica 4 1,6%"), ("homens_trans", 3, "Homem Trans 3 1,2%"), ("heterossexuais", 3, "Heterossexual* 3 1,2%"), ("nao_informado", 16, "Não informado 16 6,2%"), ("homicidios", 204, "204 homicídios, 20 suicídios, 17 latrocínios e 16 casos de outras causas"), ("suicidios", 20, "204 homicídios, 20 suicídios, 17 latrocínios e 16 casos de outras causas"), ("latrocinios", 17, "204 homicídios, 20 suicídios, 17 latrocínios e 16 casos de outras causas"), ("outras_causas", 16, "204 homicídios, 20 suicídios, 17 latrocínios e 16 casos de outras causas")], D_GGB, "trans_travestis 2025 = mulher trans 46 + travesti 18 (soma feita aqui); manchete do release: '237 homicidios' = 204+17+16")

# GGB 1990-1999 e decadas: serie digitalizada do grafico + tabela por decada
R("ggb2020", 1990, "total", None, "digitalizado", D_GGB, "Gráfico 1 - Número de mortes de LGBTI+ por ano 1990 a 2020", "valores 1990-1999 digitalizados do grafico vetorial (marcadores) por s05_digitaliza_ggb.py: ver dados_ggb_1990_1999_digitalizado.csv; o valor aqui fica vazio de proposito", ano_fim=1999)
dec = [(1963,1969,30),(1970,1979,41),(1980,1989,369),(1990,1999,1256),(2000,2009,1429),(2010,2019,3029),(2020,2021,537)]
for a, b, v in dec:
    R("ggb2021", a, "total_periodo", v, "contagem_declarada", D_GGB, f"{a}-{b}" if False else {1963:"1963-1969 30",1970:"1970-1979 41",1980:"1980-1989 369",1990:"1990-1999 1.256",2000:"2000-2009 1.429",2010:"2010-2019 3.029",2020:"2020-2021 537"}[a], "Tabela 1 do GGB 2021 (total do periodo)", ano_fim=b)

# ---------------- ANTRA ----------------
R("antra2017", 2016, "trans_assassinatos", 144, "contagem_declarada", D_ANTRA, "Houve um aumento de 15% em relação aos 144 casos notificados em 2016", "o proprio relatorio ANTRA 2017 diz que a serie 2008-2016 e do GGB: 'Em 2008, o Grupo Gay da Bahia - o único que contabilizava até então os crimes - noticiou 58 assassinatos de pessoas trans. O número subiu para 68 em 2009, 99 em 2010, 128 em 2012, 134 em 2014, 144 em 2016'")
R("antra2017", 2008, "trans_assassinatos_GGB", 58, "contagem_declarada", "contagem do GGB reproduzida pela ANTRA", "o Grupo Gay da Bahia - o único que contabilizava até então os crimes - noticiou 58 assassinatos de pessoas trans")
R("antra2017", 2017, "trans_assassinatos", 179, "contagem_declarada", D_ANTRA, "ocorreram 179 Assassinatos de pessoas Trans, sendo 169 Travestis e Mulheres")
R("antra2018", 2018, "trans_assassinatos", 163, "contagem_declarada", D_ANTRA, "ocorreram 163 Assassinatos de pessoas Trans, sendo 158 Travestis e Mulheres")
R("antra2019", 2019, "trans_assassinatos", 124, "contagem_declarada", D_ANTRA, "chegamos ao número de 124 assassinatos que serão considerados", "127 registros no Mapa, 124 considerados")
R("antra2020", 2020, "trans_assassinatos", 175, "contagem_declarada", D_ANTRA, "chegamos ao número de 175 assassinatos, todos contra pessoas que expressavam o gênero", "184 registros no Mapa, 175 considerados; todos do genero feminino")
R("antra2021", 2021, "trans_assassinatos", 140, "contagem_declarada", D_ANTRA, "140 assassinatos em 2021")
R("antra2022", 2022, "trans_assassinatos", 131, "contagem_declarada", D_ANTRA, "tivemos pelo menos 131 assassinatos de pessoas trans, sendo 130 travestis e mulheres transexuais")
R("antra2023", 2023, "trans_assassinatos", 145, "contagem_declarada", D_ANTRA, "foram 155 casos, sendo 145 casos de assassinatos e 10 pessoas trans suicidadas")
R("antra2023", 2023, "trans_suicidios", 10, "contagem_declarada", D_ANTRA, "foram 155 casos, sendo 145 casos de assassinatos e 10 pessoas trans suicidadas")
R("antra2024", 2024, "trans_assassinatos", 122, "contagem_declarada", D_ANTRA, "serão consideradas, para fins deste dossiê, 122 mortes por assassinatos", "137 catalogados, 15 descartados por nao serem CVLI")
R("antra2025", 2025, "trans_assassinatos", 80, "contagem_declarada", D_ANTRA, "serão consideradas, para fins deste dossiê, 80 mortes por assassinato", "92 catalogados, 12 descartados por nao serem CVLI")
for doc, ano, cat, v, sn in [("antra2017",2017,"trans_homens",10,"169 Travestis e Mulheres Transexuais e 10 Homens Trans"),
        ("antra2022",2022,"trans_homens",1,"130 travestis e mulheres transexuais e 1homem trans"),
        ("antra2024",2024,"trans_homens",5,"117 assassinatos foram contra travestis e mulheres trans/transexuais e 5 contra homens trans"),
        ("antra2025",2025,"trans_homens",3,"77 assassinatos foram contra travestis e mulheres trans/transexuais e 3 contra homens trans")]:
    R(doc, ano, cat, v, "contagem_declarada", D_ANTRA, sn)

# ---------------- Observatorio (Acontece/ANTRA/ABGLT) ----------------
def obs(doc, ano, itens):
    for cat, val, snip in itens:
        R(doc, ano, cat, val, "contagem_declarada", D_OBS, snip, "base compartilhada Acontece/ANTRA/ABGLT (texto do dossie); series 2000-2020 do grafico = GGB")
obs("obs2021", 2021, [("total", 316, "morte violenta de 316 pessoas LGBTI+ no Brasil, sendo 285 assassinatos, 26 suicídios e 5 mortes por outras causas"), ("homicidios", 285, "sendo 285 assassinatos, 26 suicídios e 5 mortes por outras causas"), ("suicidios", 26, "sendo 285 assassinatos, 26 suicídios e 5 mortes por outras causas"), ("outras_causas", 5, "sendo 285 assassinatos, 26 suicídios e 5 mortes por outras causas"), ("homens_gays", 145, "homens gays, representando 45,89% do total (145 mortes)"), ("trans_travestis", 141, "as travestis e mulheres trans, com 44,62% dos casos (141 mortes)"), ("lesbicas", 12, "mulheres lésbicas, com 3,80% das mortes (12 casos)"), ("homens_trans", 8, "homens trans e pessoas transmasculinas corresponderam a 2,53% dos casos (oito mortes)"), ("bissexuais", 3, "as pessoas bissexuais equivaleram a menos de um por cento (três mortes)")])
obs("obs2022", 2022, [("total", 273, "273 pessoas LGBTI+ morreram de forma violenta no Brasil, sendo 228 assassinatos, 30 suicídios e 15 mortes por outras causas"), ("homicidios", 228, "sendo 228 assassinatos, 30 suicídios e 15 mortes por outras causas"), ("suicidios", 30, "sendo 228 assassinatos, 30 suicídios e 15 mortes por outras causas"), ("outras_causas", 15, "sendo 228 assassinatos, 30 suicídios e 15 mortes por outras causas"), ("trans_travestis", 159, "travestis e mulheres trans, com 58,24% dos casos (159 mortes)"), ("homens_gays", 96, "os homens gays, representando 35,16% do total (96 mortes)")])
obs("obs2023", 2023, [("total", 230, "Em 2023 foram registradas 230 mortes violentas"), ("homicidios", 184, "184 assassinatos, 18 suicídios e 28 mortes por outras causas"), ("suicidios", 18, "184 assassinatos, 18 suicídios e 28 mortes por outras causas"), ("outras_causas", 28, "184 assassinatos, 18 suicídios e 28 mortes por outras causas"), ("trans_travestis", 142, "com 61,74% dos casos (142 mortes)"), ("homens_gays", 59, "representando 25,65% do total (59 mortes)"), ("homens_trans", 13, "homens trans e pessoas transmasculinas (13 mortes, 5,65% dos casos)"), ("lesbicas", 7, "mulheres lésbicas, com 3,04% dos casos (7 mortes)")])
R("obs2026q1", 2026, "total_jan_mar", 50, "contagem_declarada", D_OBS, "De janeiro a março de 2026, nossa equipe técnica registrou 50", "parcial")
R("obs2026q1", 2024, "total", None, "nao_publicado", D_OBS, "Entre 2024 e 2025, o Observatório precisou suspender suas ati", "o proprio Observatorio diz que suspendeu atividades em 2024-2025 por falta de recursos: ha dossie anual 2024 e 2025? NAO. Achado, nao lacuna", ano_fim=2025, snip_pagina="Entre 2024 e 2025, o Observatório precisou suspender suas ati")

# ---------------- Anuario FBSP: homicidio doloso com vitima LGBT (registros oficiais estaduais) ----------------
R("anu2022", 2020, "homicidio_doloso_oficial", 167, "oficial_estadual_agregado", D_ANU, "Brasil 1.271 1.719 35,2 167 179 7,2 95 179 88,4", "edicao 2022 (dados 2020-2021); SP, BA, MA e outras UFs sem dado")
R("anu2022", 2021, "homicidio_doloso_oficial", 179, "oficial_estadual_agregado", D_ANU, "Brasil 1.271 1.719 35,2 167 179 7,2 95 179 88,4", "edicao 2022; a edicao 2023 cita 176 para 2021 segundo imprensa (nao conferido no texto)")
R("anu2023", 2022, "homicidio_doloso_oficial", 163, "oficial_estadual_agregado", D_ANU, "O Estado deu conta de contar 163, 63% do que contabilizou a organização da sociedade civil", "edicao 2023: o Anuario compara 163 (Estado) com GGB 256, ANTRA 131")
R("anu2024", 2022, "homicidio_doloso_oficial", 151, "oficial_estadual_agregado", D_ANU, "Brasil 3.024 3.673 21,5 151 214 41,7 252 354 40,5", "2022 revisto na edicao 2024 (era 163 na edicao 2023)")
R("anu2024", 2023, "homicidio_doloso_oficial", 214, "oficial_estadual_agregado", D_ANU, "Brasil 3.024 3.673 21,5 151 214 41,7 252 354 40,5")
R("anu2025", 2023, "homicidio_doloso_oficial", 274, "oficial_estadual_agregado", D_ANU, "Brasil 4.836 4.929 1,9 274 202 -26,3 520 444 -14,6", "2023 revisto na edicao 2025 (era 214 na edicao 2024)")
R("anu2025", 2024, "homicidio_doloso_oficial", 202, "oficial_estadual_agregado", D_ANU, "Brasil 4.836 4.929 1,9 274 202 -26,3 520 444 -14,6")
R("anu2026", 2024, "homicidio_doloso_oficial", 218, "oficial_estadual_agregado", D_ANU, "Brasil 2.567 3.481 35,6 5.079 5.452 7,3 218 187 -14,2 471 480 1,9", "2024 revisto na edicao 2026 (era 202 na edicao 2025)")
R("anu2026", 2025, "homicidio_doloso_oficial", 187, "oficial_estadual_agregado", D_ANU, "Brasil 2.567 3.481 35,6 5.079 5.452 7,3 218 187 -14,2 471 480 1,9", "o texto do Anuario 2026 compara com 'GGB registrou 237 homicidios dolosos, 50 a mais que o proprio Estado'")

# ---------------- Atlas 2026 (Sinan): notificacoes de violencia, NAO mortes ----------------
sinan_hb = {2015:3278,2016:3602,2017:4369,2018:5057,2019:5548,2020:4933,2021:5759,2022:7276,2023:9718,2024:10250}
fm = lambda v: f"{v:,}".replace(",", ".")
for y, v in sinan_hb.items():
    R("atlas2026", y, "notificacoes_violencia_homo_bi", v, "oficial_saude", "casos de violencia interpessoal notificados no Sinan com vitima homossexual ou bissexual (exclui autoprovocada); NAO sao mortes", f"{y} {fm(v)}", "Tabela 7.1; microdados 2023-24 preliminares")
sinan_tr = {2015:"468 1.777 259 2.504",2016:"650 2.358 344 3.352",2017:"573 1.971 438 2.982",2018:"539 2.154 484 3.177",2019:"517 2.079 467 3.063",2020:"443 1.859 441 2.743",2021:"565 2.120 418 3.103",2022:"753 2.540 555 3.848",2023:"1.307 3.470 655 5.432",2024:"1.299 3.594 682 5.575"}
for y, row in sinan_tr.items():
    v = int(row.split()[-1].replace(".", ""))
    R("atlas2026", y, "notificacoes_violencia_trans", v, "oficial_saude", "pessoas trans e travestis vitimas de violencia no Sinan (exclui autoprovocada); NAO sao mortes", f"{y} {row}", "Tabela 7.2")

# ---------------- Disque 100 ----------------
for y, v in {2011:"1.159",2012:"3.031",2013:"1.695",2014:"1.013",2015:"1.983",2016:"1.876",2017:"1.720",2018:"1.685"}.items():
    R("atlas2020", y, "denuncias_disque100", int(v.replace(".", "")), "denuncia_oficial_agregada", "denuncias de violencia contra pessoas LGBTQI+ registradas no Disque 100/MMFDH (denuncia, NAO fato; muda com divulgacao do canal)", v,
      "valor lido do rotulo do Grafico 19 (2011-2018) do Atlas 2020; anos pareados com a ordem dos rotulos", snip_pagina="1.695 1.720 1.685")
R("atlas2020", 2017, "denuncias_disque100_homicidio", 193, "denuncia_oficial_agregada", "denuncias de HOMICIDIO contra pessoas LGBTQI+ no Disque 100 (denuncia, nao morte confirmada)", "O incremento de 127% nas denúncias de homicídio, entre 2011 e 2017, foi revertido no último ano, com redução de 28% na passagem a 2018", "193 (2017) e 138 (2018) lidos dos rotulos do Grafico 21; 127% e -28% conferem com o texto", snip_pagina="O incremento de 127% nas denúncias de homicídio, entre 2011 e 2017, foi revertido no último ano")
R("atlas2020", 2018, "denuncias_disque100_homicidio", 138, "denuncia_oficial_agregada", "idem", "com redução de 28% na passagem a 2018", "ver 2017", snip_pagina="com redução de 28% na passagem a 2018")
# imprensa (copia local do HTML)
_dp = BASE/"fontes/p3-ggb/disque100/diariodopara_lgbt_disque100.txt"
_t = re.sub(r"\s+", " ", _dp.read_text())
for y, v, sn in [(2022, 3948, "2.122 a mais que em 2022 (3.948)"), (2023, 6070, "No ano anterior, foram feitas 6.070 denúncias"), (2024, 5741, "5.741 casos foram registrados até setembro deste ano")]:
    assert sn in _t, sn
    rows.append(dict(fonte="diariodopara_agenciabrasil", doc_id="diario_para_20241026", ano=y, ano_fim=y, categoria="denuncias_disque100" if y < 2024 else "denuncias_disque100_ate_setembro", valor=v, tipo_contagem="secundaria_imprensa",
         definicao_declarada="denuncias de LGBTQIA+fobia no Disque 100/MDHC segundo a Agencia Brasil (republicada pelo Diario do Para, 26/10/2024); 2022 so tinha a opcao 'homossexual' no formulario; painel oficial NAO acessivel sem navegador (fila-chrome)",
         trecho_verbatim=sn, pagina_pdf="", arquivo=str(BASE/"fontes/p3-ggb/disque100/diariodopara_lgbt_disque100.html"), sha256=hashlib.sha256((BASE/"fontes/p3-ggb/disque100/diariodopara_lgbt_disque100.html").read_bytes()).hexdigest(),
         url="https://diariodopara.com.br/noticias/brasil/populacao-lgbtqia-denuncia-mais-casos-de-violencia-no-pais", titulo="Diario do Para/Agencia Brasil 2024-10-26", observacao="imprensa citando o MDHC; serie nao comparavel com 2011-2018 (outro formulario)"))
rows.append(dict(fonte="dossie_projeto", doc_id="dossie_consolidado", ano=2019, ano_fim=2019, categoria="denuncias_disque100", valor=846, tipo_contagem="citado_nao_conferido",
     definicao_declarada="denuncias do grupo LGBT, relatorio oficial 2019 do MDHC segundo o dossie do projeto", trecho_verbatim="1.685 (2018) -> 846 (2019), -49,8%", pagina_pdf="", arquivo=str(BASE/"DOSSIE-CONSOLIDADO-2026-10-12.md"),
     sha256="", url="", titulo="Dossie consolidado 2026-10-12 (cita relatorio MDHC 2019)", observacao="⚠️ o PDF do MDHC 2019 nao esta em disco nem foi localizado pela busca de hoje (so 2017=1.720 e 2018=1.685 confirmados no Atlas 2020); nao usar em testes"))

# ---------------- TGEU TMM (API publica) e TDoR (export publico) ----------------
import collections, datetime
TMM = RAW/"tmm"; TD = RAW/"tdor/anual"
_tm = list(csv.DictReader(open(TMM/"tmm_brasil.csv")))
_tmlog = json.loads((TMM/"fetch_log.json").read_text()); _tdlog = {r["ano"]: r for r in json.loads((TD/"fetch_log.json").read_text())}
def fam(rb):
    r = rb.lower()
    if "grupo gay" in r or "homofobiamata" in r or "athos gls" in r: return "GGB/HomofobiaMata"
    if "antra" in r: return "ANTRA"
    if "ibte" in r or "instituto brasileiro trans" in r: return "IBTE"
    if "rede trans brasil" in r: return "RedeTransBrasil"
    if "trans lives matter" in r: return "TDoR/TLM"
    if "centro de apoyo" in r or "cait" in r: return "CAIT(Mexico)"
    return "outra/imprensa/NI"
dep = collections.defaultdict(collections.Counter); cy = collections.Counter(); pr = collections.Counter()
for r in _tm:
    cy[r["ano"]] += 1; pr[r["tdor_period"]] += 1; dep[r["ano"]][fam(r["reported_by"])] += 1
fams = ["GGB/HomofobiaMata", "ANTRA", "IBTE", "RedeTransBrasil", "TDoR/TLM", "CAIT(Mexico)", "outra/imprensa/NI"]
with open(OUT/"dados_tmm_dependencia.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano_civil", "n_tmm_brasil"] + ["n_" + x for x in fams] + ["pct_GGB"])
    for y in sorted(cy):
        w.writerow([y, cy[y]] + [dep[y][x] for x in fams] + [round(100 * dep[y]["GGB/HomofobiaMata"] / cy[y], 1)])
_tmpath = TMM/"tmm_all.json"
for y in sorted(cy):
    rows.append(dict(fonte="TGEU_TMM", doc_id="tmm_api", ano=int(y), ano_fim=int(y), categoria="tmm_casos_brasil_ano_civil", valor=cy[y], tipo_contagem="derivado_de_base_publica",
        definicao_declarada="assassinatos de pessoas trans e de genero diverso monitorados pelo TGEU TMM (base Uwazi, titulos anonimizados), pais=Brazil, ano civil do incidente; periodo Out-Set e outra coluna",
        trecho_verbatim=f"calendar_year={y}; country_territory_of_the_murder=Brazil; n={cy[y]} de {_tmlog['total_rows']} registros globais", pagina_pdf="", arquivo=str(_tmpath), sha256=_tmlog["sha256"],
        url="https://transmurdermonitoring.tgeu.org/api/search", titulo="TGEU Trans Murder Monitoring (API publica, coletada 2026-10-22)", observacao="2025 parcial (TMM vai ate set/2025)" if y == "2025" else ""))
for p in sorted(pr):
    yy = int(p.split()[-1])
    rows.append(dict(fonte="TGEU_TMM", doc_id="tmm_api", ano=yy, ano_fim=yy, categoria="tmm_casos_brasil_periodo_TDoR_out_set", valor=pr[p], tipo_contagem="derivado_de_base_publica",
        definicao_declarada="idem, periodo TDoR = 1 out do ano anterior a 30 set do ano rotulado", trecho_verbatim=f"tdor_period__oct_sept_={p}; n={pr[p]}", pagina_pdf="", arquivo=str(_tmpath), sha256=_tmlog["sha256"],
        url="https://transmurdermonitoring.tgeu.org/api/search", titulo="TGEU Trans Murder Monitoring (API publica)", observacao="o GGB 2023 cita 'sendo 100 no Brasil' (TDoR 2023) e a ANTRA cita o TMM: conferem"))
for y in range(2008, 2026):
    rr = list(csv.DictReader(open(TD/f"tdor_br_{y}.csv", encoding="utf-8-sig")))
    c = collections.Counter(x["Category"] for x in rr)
    rows.append(dict(fonte="TDoR_lista", doc_id="tdor_export", ano=y, ano_fim=y, categoria="tdor_casos_brasil_ano_civil", valor=len(rr), tipo_contagem="derivado_de_base_publica",
        definicao_declarada="registros do Brasil no 'Remembering Our Dead' (TDoR, lista nominal publica; inclui violencia, suicidio, medico, nao classificado)", trecho_verbatim=f"export publico 1 jan-31 dez {y}, country=Brazil; categorias: {dict(c)}",
        pagina_pdf="", arquivo=str(TD/f"tdor_br_{y}.csv"), sha256=_tdlog[y]["sha256_zip"], url=_tdlog[y]["url"], titulo="TDoR Remembering Our Dead, export publico", observacao="nomes apenas em _raw (fora do git); lista pode ser atualizada depois"))
    rows.append(dict(fonte="TDoR_lista", doc_id="tdor_export", ano=y, ano_fim=y, categoria="tdor_casos_brasil_violencia", valor=c["violence"], tipo_contagem="derivado_de_base_publica",
        definicao_declarada="subconjunto Category=violence", trecho_verbatim=f"Category=violence: {c['violence']}", pagina_pdf="", arquivo=str(TD/f"tdor_br_{y}.csv"), sha256=_tdlog[y]["sha256_zip"], url=_tdlog[y]["url"], titulo="TDoR export", observacao=""))

# ---------------- SIM (microdados DATASUS ja agregados) ----------------
_sim = collections.Counter()
_ar = BASE/"dados/sim/asr_brasil.csv"
for r in csv.DictReader(open(_ar)):
    if r["grupo"] == "Brasil" and r["desfecho"] == "agressao" and r["obitos"]: _sim[int(r["ano"])] = int(r["obitos"])
_s0 = OUT/"dados_sim_2000_2009.csv"
_sim_src = {y: (str(_ar), sha(_ar)) for y in _sim}
if _s0.exists():
    for r in csv.DictReader(open(_s0)):
        _sim[int(r["ano"])] = int(r["agressao"]); _sim_src[int(r["ano"])] = (str(_s0), sha(_s0))
for y in sorted(_sim):
    rows.append(dict(fonte="SIM_DATASUS", doc_id="sim", ano=y, ano_fim=y, categoria="obitos_agressao_sim_brasil", valor=_sim[y], tipo_contagem="oficial_sim",
        definicao_declarada="obitos por agressao (CID-10 X85-Y09, causa basica), Brasil, por ano do obito; NAO ha campo de orientacao sexual/identidade de genero no SIM: serve de CONTEXTO, nao de denominador LGBT",
        trecho_verbatim=f"X85-Y09 {y}: {_sim[y]}", pagina_pdf="", arquivo=_sim_src[y][0], sha256=_sim_src[y][1], url="ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/", titulo="SIM/DATASUS DOBR (agregado local)", observacao=""))

# ---------------- salva ----------------
if FAIL:
    print("TRECHOS NAO ENCONTRADOS:"); print("\n".join(FAIL)); sys.exit(1)
cols = ["fonte", "doc_id", "ano", "ano_fim", "categoria", "valor", "tipo_contagem", "definicao_declarada", "trecho_verbatim", "pagina_pdf", "arquivo", "sha256", "url", "titulo", "observacao"]
rows.sort(key=lambda r: (r["fonte"], r["categoria"], int(r["ano"])))
with open(OUT / "painel_mortes_lgbt.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), "linhas; todos os trechos de PDF validados")
