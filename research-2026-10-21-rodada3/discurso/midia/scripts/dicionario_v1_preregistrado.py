"""Dicionario pre-registrado (frente MIDIA, discurso, rodada 3, 2026-10-22).

Fonte unica das consultas. PRE-REGISTRO.md cita o sha256 deste arquivo.
Cada entrada: id, familia, idioma, rotulo, tipo ('frase' = frase exata; 'coocc' = coocorrencia
no mesmo texto/artigo, mais ampla), gdelt (string de consulta), local (regex sobre texto
normalizado: minusculo, sem acento), oa (consulta OpenAlex title_and_abstract.search),
wp (consulta Wikipedia, so frases exatas entre aspas).
Texto normalizado = NFKD, sem marcas combinantes, minusculo, espacos colapsados.
"""
import re
import unicodedata

PERIODO_INI = "2015-01-01"
PERIODO_FIM = "2026-10-21"
SEMENTE = 20261022

# grupo-alvo (texto normalizado)
G = (r"(?:lgbt\w*|gays?|homossexua\w+|lesbic\w+|bissexua\w+|travestis?|transexua\w+|"
     r"transgener\w+|trans|homoafetiv\w+|diversidade sexual|minorias sexuais)")
G_EN = r"(?:lgbt\w*|gays?|homosexuals?|lesbians?|bisexuals?|trans|transgender\w*|queer|sexual minorit\w+)"
HET = r"(?:heterossexua\w+|heteros|cisgener\w+|heterosexuals?|straight people|heterosexuales)"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", s)


def near(a: str, b: str, n: int = 12) -> str:
    """a e b a ate n palavras de distancia, em qualquer ordem."""
    w = r"\W+(?:\w+\W+){0,%d}?" % n
    return r"(?:%s)%s(?:%s)|(?:%s)%s(?:%s)" % (a, w, b, b, w, a)


E = []


def add(id, fam, lang, rotulo, tipo, gdelt, local, oa=None, wp=None):
    E.append(dict(id=id, fam=fam, lang=lang, rotulo=rotulo, tipo=tipo, gdelt=gdelt,
                  local=local, oa=oa, wp=wp))


# ---------------- F1: "gays/LGBT morrem mais que heterossexuais" ----------------
add("F1-PT-01", "F1", "pt", "gays morrem mais", "frase",
    '("gays morrem mais" OR "homossexuais morrem mais" OR "LGBTs morrem mais" OR "LGBT morrem mais")',
    near(G, r"morr\w+\s+(?:muito\s+)?mais", 4), wp='"morrem mais"')
add("F1-PT-02", "F1", "pt", "morrem mais que heterossexuais", "frase",
    '("morrem mais que heterossexuais" OR "morrem mais do que heterossexuais" OR "morrem mais que os heterossexuais" OR "morrem mais do que os heterossexuais" OR "morrem mais que héteros")',
    r"morr\w+\s+(?:muito\s+)?mais\s+(?:do\s+)?que\s+(?:os\s+|as\s+)?" + HET, wp='"morrem mais que heterossexuais"')
add("F1-PT-03", "F1", "pt", "expectativa de vida de LGBT/gays", "frase",
    '("expectativa de vida de gays" OR "expectativa de vida de homossexuais" OR "expectativa de vida de LGBT" OR "expectativa de vida da população LGBT" OR "expectativa de vida de pessoas LGBT" OR "expectativa de vida dos gays" OR "expectativa de vida dos homossexuais")',
    r"expectativa de vida (?:d[eao]s?\s+)?(?:(?:pessoas|populacao|comunidade)\s+)?(?:lgbt\w*|gays?|homossexua\w+)",
    wp='"expectativa de vida" gays')
add("F1-PT-04", "F1", "pt", "expectativa de vida + grupo (coocorrencia)", "coocc",
    '"expectativa de vida" (LGBT OR LGBTI OR gays OR homossexuais OR homossexualidade)',
    near(r"expectativa de vida", G, 15))
add("F1-PT-05", "F1", "pt", "risco/taxa de suicidio + grupo (coocorrencia)", "coocc",
    '("risco de suicídio" OR "taxa de suicídio" OR "taxas de suicídio" OR "tentativas de suicídio") (LGBT OR gays OR homossexuais)',
    near(r"(?:risco|taxas?|tentativas?) de suicidio", G, 15))
add("F1-PT-06", "F1", "pt", "mais propensos a morrer", "coocc",
    '("mais propensos a morrer" OR "maior risco de morte" OR "maior mortalidade") (LGBT OR gays OR homossexuais)',
    near(r"(?:mais propensos? a morrer|maior risco de morte|maior mortalidade|mortalidade (?:mais )?alta)", G, 15))
add("F1-EN-01", "F1", "en", "gay/LGBT people die earlier", "frase",
    '("gay men die earlier" OR "gay people die earlier" OR "LGBT people die earlier" OR "gay men die younger" OR "LGBT people die younger" OR "gay people die younger" OR "die earlier than heterosexual" OR "die younger than heterosexual" OR "die sooner than heterosexual")',
    near(G_EN, r"die\s+(?:much\s+)?(?:earlier|younger|sooner)", 5) + r"|die\s+(?:earlier|younger|sooner)\s+than\s+(?:straight|heterosexual)",
    oa='"die earlier" OR "die younger" OR "shorter life expectancy" OR "reduced life expectancy"')
add("F1-EN-02", "F1", "en", "life expectancy + group (cooc)", "coocc",
    '"life expectancy" (gay OR LGBT OR homosexual OR "sexual minority" OR transgender)',
    near(r"life expectancy", G_EN, 15))
add("F1-EN-03", "F1", "en", "mortality/death risk + group (cooc)", "coocc",
    '("higher mortality" OR "higher death rate" OR "excess mortality" OR "more likely to die") (gay OR LGBT OR homosexual OR "sexual minority")',
    near(r"(?:higher mortality|higher death rate|excess mortality|more likely to die|elevated mortality)", G_EN, 15))
add("F1-EN-04", "F1", "en", "suicide risk + group (cooc)", "coocc",
    '("suicide risk" OR "suicide rate" OR "suicide attempts") (gay OR LGBT OR homosexual OR "sexual minority") ("higher" OR "more likely")',
    near(r"(?:suicide (?:risk|rates?|attempts?)|suicidality)", G_EN, 15))
add("F1-ES-01", "F1", "es", "los gays mueren mas", "frase",
    '("los gays mueren más" OR "los homosexuales mueren más" OR "mueren más que los heterosexuales" OR "mueren más que heterosexuales" OR "esperanza de vida de los gays" OR "esperanza de vida de las personas LGBT")',
    near(G, r"mueren\s+(?:mucho\s+)?mas", 4) + r"|mueren\s+mas\s+que\s+(?:los\s+)?heterosexuales|esperanza de vida de (?:los|las)\s+(?:gays|homosexuales|personas lgbt\w*)")
add("F1-ES-02", "F1", "es", "riesgo de suicidio + grupo (cooc)", "coocc",
    '("riesgo de suicidio" OR "tasa de suicidio") (LGBT OR gays OR homosexuales)',
    near(r"(?:riesgo|tasas?) de suicidio", G, 15))

# ---------------- F2: "Brasil e o pais que mais mata LGBT/trans" ----------------
add("F2-PT-01", "F2", "pt", "pais que mais mata LGBT/trans", "frase",
    '("país que mais mata LGBT" OR "país que mais mata pessoas trans" OR "país que mais mata travestis" OR "país que mais mata transexuais" OR "país que mais mata gays" OR "país que mais mata homossexuais" OR "país que mais mata LGBTs" OR "país que mais mata a população LGBT" OR "país que mais mata pessoas LGBT" OR "país que mais mata transgêneros" OR "país que mais mata mulheres trans")',
    r"pais que mais (?:mata|assassina|mata e assassina)\s+(?:a\s+|as\s+|os\s+)?(?:pessoas\s+|populacao\s+|mulheres\s+)?" + G,
    wp='"país que mais mata"')
add("F2-PT-02", "F2", "pt", "pais que mais mata (+grupo, coocorrencia)", "coocc",
    '"país que mais mata" (LGBT OR trans OR travestis OR transexuais OR homossexuais OR gays)',
    near(r"pais que mais (?:mata|assassina)", G, 12))
add("F2-PT-03", "F2", "pt", "lider/campeao mundial de assassinatos de LGBT/trans", "frase",
    '("campeão mundial" OR "líder mundial" OR "lidera o ranking" OR "lidera ranking" OR "primeiro lugar no ranking" OR "ranking mundial") (assassinatos OR homicídios OR mortes) (LGBT OR trans OR travestis OR transexuais)',
    near(r"(?:campeao mundial|lider mundial|lidera (?:o )?ranking|ranking mundial|primeiro lugar)", G, 15) + r"|" + near(r"(?:assassinatos|homicidios|mortes)", r"(?:campeao mundial|lider mundial|lidera (?:o )?ranking|ranking mundial)", 10))
add("F2-PT-04", "F2", "pt", "a cada N horas morre/e morto um LGBT", "frase",
    '("a cada 19 horas" OR "a cada 20 horas" OR "a cada 23 horas" OR "a cada 24 horas" OR "a cada 25 horas" OR "a cada 26 horas" OR "a cada 27 horas" OR "a cada 28 horas" OR "a cada 32 horas" OR "a cada 34 horas" OR "a cada 36 horas" OR "a cada 48 horas") (LGBT OR LGBTI OR LGBTQIA OR homossexuais OR gays OR travestis OR trans)',
    near(r"a cada \d+ horas", G, 15))
add("F2-PT-05", "F2", "pt", "recorde de mortes LGBT/trans", "coocc",
    '("recorde de mortes" OR "recorde de assassinatos" OR "recorde de homicídios" OR "número recorde") (LGBT OR LGBTI OR travestis OR transexuais OR homossexuais OR "pessoas trans")',
    near(r"(?:recorde de (?:mortes|assassinatos|homicidios)|numero recorde)", G, 15))
add("F2-PT-06", "F2", "pt", "Brasil lidera / mais perigoso para trans", "frase",
    '("país mais perigoso para" OR "país que mais assassina" OR "país que mais mata travestis" OR "Brasil lidera" OR "Brasil é o país") (LGBT OR trans OR travestis OR transexuais) (assassinatos OR mortes OR homicídios)',
    near(r"(?:pais mais perigoso para|brasil lidera|brasil e o pais)", G, 15))
add("F2-EN-01", "F2", "en", "country that kills the most LGBT/trans", "frase",
    '("country that kills the most" OR "most dangerous country for trans" OR "most dangerous country for LGBT" OR "deadliest country for trans" OR "deadliest country for LGBT" OR "deadliest country for transgender" OR "most dangerous place for trans" OR "country with the most trans murders" OR "highest number of trans murders" OR "kills more trans" OR "most murders of trans")',
    near(r"(?:most dangerous|deadliest|kills the most|kills more|most murders)", G_EN, 8))
add("F2-EN-02", "F2", "en", "Brazil + world's highest murders trans (cooc)", "coocc",
    'Brazil (trans OR transgender OR LGBT OR LGBTQ) ("highest in the world" OR "in the world" OR "world leader") (murders OR killings OR homicides)',
    near(r"brazil", r"(?:highest (?:number|rate) of (?:trans|transgender)|highest in the world|most (?:trans|transgender) (?:murders|killings))", 20))
add("F2-ES-01", "F2", "es", "pais que mas mata LGBT/trans", "frase",
    '("país que más mata" OR "país más peligroso para las personas trans" OR "país donde más matan" OR "el país que más asesina") (LGBT OR trans OR travestis OR gays OR homosexuales)',
    near(r"pais (?:que mas (?:mata|asesina)|donde mas matan|mas peligroso para)", G, 12))
add("F2-ES-02", "F2", "es", "cada N horas + LGBT", "frase",
    '("cada 19 horas" OR "cada 20 horas" OR "cada 23 horas" OR "cada 25 horas" OR "cada 26 horas" OR "cada 32 horas") (LGBT OR trans OR homosexuales OR gays) Brasil',
    near(r"(?<!\ba )cada \d+ horas", G, 15))

# ---------------- F3: "governo de direita/Bolsonaro mata/persegue/quer eliminar LGBT" ----------------
add("F3-PT-01", "F3", "pt", "extermino/genocidio de homossexuais/LGBT", "frase",
    '("extermínio de homossexuais" OR "extermínio de gays" OR "extermínio de LGBT" OR "extermínio de LGBTs" OR "extermínio da população LGBT" OR "extermínio LGBT" OR "extermínio de pessoas LGBT" OR "genocídio LGBT" OR "genocídio da população LGBT" OR "genocídio de homossexuais" OR "genocídio de gays" OR "genocídio de pessoas trans" OR "genocídio trans")',
    r"(?:exterminio|genocidio)\s+(?:d[eao]s?\s+)?(?:(?:pessoas|populacao|comunidade)\s+)?(?:(?:lgbt\w*|gays?|homossexua\w+|travestis?|transexua\w+|trans)\b)",
    wp='"extermínio" LGBT')
add("F3-PT-02", "F3", "pt", "licenca para matar + grupo", "coocc",
    '"licença para matar" (gays OR LGBT OR homossexuais OR travestis OR trans OR homofobia)',
    near(r"licenca para matar", G, 15))
add("F3-PT-03", "F3", "pt", "cura gay", "frase",
    '("cura gay" OR "tratamento para homossexualidade" OR "terapia de reversão sexual" OR "reversão sexual" OR "cura da homossexualidade")',
    r"cura gay|cura da homossexualidade|cura para a homossexualidade|reversao sexual|terapia de reversao",
    wp='"cura gay"')
add("F3-PT-04", "F3", "pt", "Bolsonaro/governo + persegue/incentiva violencia/tira direitos LGBT", "coocc",
    '(Bolsonaro OR "governo federal" OR "extrema direita" OR "governo de direita") ("perseguição a LGBT" OR "perseguição aos LGBT" OR "perseguição aos homossexuais" OR "perseguição às pessoas LGBT" OR "perseguição a gays" OR "perseguição a homossexuais" OR "caça aos gays" OR "caça aos homossexuais" OR "incentiva a violência contra" OR "incentiva violência contra" OR "estimula a violência contra" OR "retirada de direitos" OR "retirar direitos" OR "tirar direitos" OR "retrocesso") (LGBT OR homossexuais OR gays OR travestis OR trans)',
    near(r"(?:bolsonaro|governo federal|extrema direita|governo de direita|governo da direita|governos de direita)",
         r"(?:persegu\w+|cacada?|incentiv\w+ (?:a )?violencia|estimul\w+ (?:a )?violencia|retirad\w+ de direitos|tirar direitos|retirar direitos|matar|mata\b|matam|eliminar)", 25)
)
add("F3-PT-05", "F3", "pt", "governo quer matar/eliminar gays/LGBT", "frase",
    '("quer matar gays" OR "quer matar homossexuais" OR "quer matar LGBT" OR "quer eliminar os gays" OR "quer eliminar LGBT" OR "quer acabar com os gays" OR "governo mata LGBT" OR "governo que mata LGBT" OR "governo assassino" OR "governo homofóbico" OR "governo LGBTfóbico")',
    r"(?:quer|querem|pretende\w*)\s+(?:matar|eliminar|acabar com|exterminar)\s+(?:os\s+|as\s+)?" + G + r"|governos?\s+(?:que\s+)?(?:mata|matam)\s+" + G + r"|governo\s+(?:homofobico|lgbtfobico|transfobico)")
add("F3-EN-01", "F3", "en", "extermination/genocide of gays/LGBT", "frase",
    '("extermination of gays" OR "extermination of homosexuals" OR "extermination of LGBT" OR "genocide of LGBT" OR "genocide against LGBT" OR "genocide of gay" OR "genocide of trans" OR "license to kill" gay OR "licence to kill" gay)',
    r"(?:extermination|genocide)\s+(?:of|against)\s+(?:the\s+)?(?:lgbt\w*|gays?|homosexuals?|trans\w*|queer)|(?:license|licence) to kill\W+(?:\w+\W+){0,10}?(?:gays?|lgbt\w*|homosexuals?)")
add("F3-EN-02", "F3", "en", "Bolsonaro + anti-gay/homophobic (cooc)", "coocc",
    'Bolsonaro (homophobic OR "anti-gay" OR "anti-LGBT" OR "war on LGBT" OR "persecution of LGBT" OR "persecution of gay") ',
    near(r"bolsonaro", r"(?:homophobi\w+|anti-gay|anti-lgbt\w*|persecut\w+ (?:of )?(?:lgbt\w*|gays?|homosexuals?)|war on (?:lgbt\w*|gays?))", 20))
add("F3-EN-03", "F3", "en", "gay cure / conversion therapy Brazil", "coocc",
    '("gay cure" OR "cure gay") Brazil',
    r"gay cure|cure gay")
add("F3-ES-01", "F3", "es", "exterminio/genocidio LGBT; cura gay", "frase",
    '("exterminio de homosexuales" OR "exterminio de gays" OR "exterminio LGBT" OR "genocidio LGBT" OR "genocidio de homosexuales" OR "licencia para matar" OR "cura gay") (LGBT OR gays OR homosexuales OR trans)',
    r"(?:exterminio|genocidio)\s+(?:de\s+)?(?:(?:la\s+poblacion|personas|las\s+personas)\s+)?(?:lgbt\w*|gays?|homosexuales|trans\b)|cura gay|licencia para matar\W+(?:\w+\W+){0,10}?(?:gays?|lgbt\w*|homosexuales)")
add("F3-ES-02", "F3", "es", "Bolsonaro + homofobico/persecucion (cooc)", "coocc",
    'Bolsonaro (homofóbico OR homofobia OR "persecución" OR "discurso de odio") (LGBT OR gays OR homosexuales OR trans)',
    near(r"bolsonaro", r"(?:homofob\w+|persecucion|discurso de odio)", 20))

# ---------------- F4: afirmacoes simetricas CONTRARIAS ----------------
add("F4-PT-01", "F4", "pt", "nao existe homofobia no Brasil", "frase",
    '("não existe homofobia" OR "não existe homofobia no Brasil" OR "não há homofobia no Brasil" OR "homofobia não existe" OR "não existe LGBTfobia" OR "não existe transfobia" OR "no Brasil não existe homofobia" OR "homofobia no Brasil é um mito" OR "mito da homofobia" OR "mito da LGBTfobia")',
    r"(?:nao (?:existe|ha)|inexiste)\s+(?:essa\s+|a\s+)?(?:homofobia|lgbtfobia|transfobia)(?:\s+no brasil)?|homofobia nao existe|no brasil nao (?:existe|ha) homofobia|mito d[ao]\s+(?:homofobia|lgbtfobia|violencia contra (?:lgbt\w*|gays|homossexuais))|(?:homofobia|lgbtfobia)\s+(?:no brasil\s+)?e (?:um )?mito",
    wp='"não existe homofobia"')
add("F4-PT-02", "F4", "pt", "dados LGBT inventados/inflados/fraudados", "coocc",
    '("números inflados" OR "dados inflados" OR "estatísticas infladas" OR "números inventados" OR "dados inventados" OR "dados falsos" OR "estatística falsa" OR "números falsos" OR "dados manipulados" OR "números manipulados" OR "fraude estatística") (LGBT OR homofobia OR homossexuais OR "Grupo Gay da Bahia" OR GGB OR ANTRA)',
    near(r"(?:numeros|dados|estatisticas?) (?:inflad\w+|inventad\w+|falsos?|falsas?|manipulad\w+|fraudad\w+|forjad\w+|exagerad\w+)|fraude estatistica", r"(?:lgbt\w*|homofobia|homossexua\w+|grupo gay da bahia|ggb|antra|travestis?|trans)", 20))
add("F4-PT-03", "F4", "pt", "GGB mente/fraude", "coocc",
    '"Grupo Gay da Bahia" (fraude OR mentira OR mentiroso OR inventa OR inventado OR manipula OR manipulados OR "sem metodologia" OR "sem credibilidade" OR "números falsos")',
    near(r"(?:grupo gay da bahia|ggb)", r"(?:fraude|mentira|mentiroso\w*|invent\w+|manipul\w+|sem metodologia|sem credibilidade|numeros falsos|inflad\w+|exager\w+)", 20))
add("F4-PT-04", "F4", "pt", "gays nao morrem mais / ninguem e morto por ser gay", "frase",
    '("gays não morrem mais" OR "homossexuais não morrem mais" OR "ninguém é morto por ser gay" OR "ninguém morre por ser gay" OR "ninguém é assassinado por ser gay" OR "não se mata gay por ser gay" OR "ninguém mata gay por ser gay" OR "não morrem mais que")',
    r"(?:gays?|homossexuais|lgbt\w*)\s+nao morrem mais|ninguem (?:e|eh)? ?(?:morto|assassinado|morre|mata\w*)\s+(?:um\s+)?(?:gay\s+)?por ser (?:gay|homossexual|lgbt|travesti|trans)|nao se mata (?:gay|homossexual)\w* por ser")
add("F4-PT-05", "F4", "pt", "violencia contra LGBT e exagero/narrativa/vitimismo", "coocc",
    '("violência contra LGBT" OR "violência contra homossexuais" OR "homofobia") ("é exagero" OR "exagerada" OR "narrativa" OR "vitimismo" OR "invenção da esquerda" OR "falácia" OR "militância inventa")',
    near(r"(?:violencia contra (?:lgbt\w*|homossexua\w+|gays)|homofobia|lgbtfobia)", r"(?:e exagero|exagerad\w+|vitimismo|invencao da esquerda|falacia|militancia inventa|narrativa)", 12))
add("F4-EN-01", "F4", "en", "homophobia in Brazil is a myth / stats inflated", "coocc",
    '("homophobia is a myth" OR "no homophobia in Brazil" OR "LGBT murder statistics" OR "gay murder statistics") (inflated OR exaggerated OR fake OR fabricated OR myth)',
    near(r"(?:homophobia|anti-lgbt violence|lgbt (?:murder|death|killing)s?|gay (?:murder|death|killing)s?)(?: statistics| numbers| figures| data)?", r"(?:inflated|exaggerated|fabricated|fake|a myth|myth|made[- ]up)", 12))
add("F4-ES-01", "F4", "es", "no existe homofobia / datos inflados", "coocc",
    '("no existe homofobia" OR "la homofobia no existe" OR "mito de la homofobia" OR "cifras infladas") (LGBT OR gays OR homosexuales OR Brasil)',
    r"no existe (?:la )?homofobia|la homofobia no existe|mito de la homofobia|(?:cifras|datos) (?:inflad\w+|inventad\w+|falsos?)\W+(?:\w+\W+){0,12}?(?:lgbt\w*|gays?|homosexuales)")

# ---------------- listas auxiliares ----------------
# citacao de fonte (regex local, texto normalizado) -- co-mencao no mesmo texto, NAO prova de que e a fonte da frase
FONTES = {
    "GGB": r"grupo gay da bahia|\bggb\b",
    "ANTRA": r"\bantra\b|associacao nacional de travestis",
    "TGEU": r"\btgeu\b|transgender europe|trans murder monitoring|\btmm\b|\btdor\b",
    "ONU": r"\bonu\b|nacoes unidas|\bohchr\b|united nations|naciones unidas|\bun\b women",
    "CIDH": r"\bcidh\b|\bcorte idh\b|comissao interamericana|inter-american commission|iachr",
    "Anuario": r"anuario brasileiro de seguranca|forum brasileiro de seguranca|\bfbsp\b",
    "Atlas": r"atlas da violencia|\bipea\b",
    "Disque100": r"disque 100|ouvidoria nacional de direitos humanos",
    "DATASUS_SINAN": r"\bsinan\b|datasus|\bsim\b/|sistema de informacao sobre mortalidade",
    "IBGE_PNS": r"\bibge\b|pesquisa nacional de saude|\bpns\b",
    "Observatorio": r"observatorio de mortes e violencias|acontece lgbti",
    "HRW": r"human rights watch|\bhrw\b",
    "Anistia": r"anistia internacional|amnesty international",
}

# dominios de imprensa brasileira para GDELT (domainis:)
DOMINIOS_BR = [
    "folha.uol.com.br", "g1.globo.com", "oglobo.globo.com", "estadao.com.br", "uol.com.br",
    "cnnbrasil.com.br", "correiobraziliense.com.br", "brasildefato.com.br", "cartacapital.com.br",
    "metropoles.com", "terra.com.br", "r7.com", "veja.abril.com.br", "revistaforum.com.br",
    "oantagonista.com.br", "gazetadopovo.com.br", "poder360.com.br", "brasil247.com",
    "jovempan.com.br", "istoe.com.br", "dw.com", "bbc.com", "nexojornal.com.br", "midiamax.com.br",
    "agenciabrasil.ebc.com.br", "camara.leg.br", "senado.leg.br",
]
# dominios de organismos para GDELT
DOMINIOS_ORG = ["hrw.org", "amnesty.org", "anistia.org.br", "oas.org", "ohchr.org", "un.org",
                "brasil.un.org", "gov.br", "tgeu.org", "ilga.org", "unaids.org", "who.int"]


def compilar(e):
    return re.compile(e["local"], re.I)


def entradas(fam=None, lang=None):
    return [e for e in E if (fam is None or e["fam"] == fam) and (lang is None or e["lang"] == lang)]


# ---------------- OpenAlex: filtro title_and_abstract.search (titulo + resumo) ----------------
# (id, familia, rotulo, consulta). Operadores OR/AND em maiusculas, frases entre aspas.
GRP = '("gay men" OR "gay and bisexual men" OR LGBT OR LGBTQ OR "sexual minority" OR "sexual minorities" OR homosexual OR homosexuals OR lesbian OR transgender OR "trans women" OR travesti OR travestis)'
GRP_PT = '(LGBT OR LGBTQIA OR homossexuais OR gays OR travestis OR transexuais OR "pessoas trans")'
OA = [
    ("OA-F1-01", "F1", "mortalidade/expectativa de vida + grupo (tema)",
     GRP + ' AND ("life expectancy" OR "premature mortality" OR "excess mortality" OR "all-cause mortality" OR "die earlier" OR "die younger" OR "mortality disparities")'),
    ("OA-F1-02", "F1", "suicidio + grupo (tema)", GRP + ' AND (suicide OR suicidal OR "suicide attempt")'),
    ("OA-F1-03", "F1", "PT: expectativa de vida/mortalidade + grupo",
     GRP_PT + ' AND ("expectativa de vida" OR mortalidade OR "morrem mais" OR "risco de morte")'),
    ("OA-F2-01", "F2", "Brasil + trans/LGBT + homicidio/assassinato (tema)",
     'Brazil AND ' + GRP + ' AND (murder OR murders OR homicide OR homicides OR killings OR "violent deaths" OR assassinations)'),
    ("OA-F2-02", "F2", "pais mais perigoso/que mais mata (frase)",
     '("most dangerous country" OR "deadliest country" OR "country that kills the most" OR "country with the highest number" OR "highest number of trans") AND ' + GRP),
    ("OA-F2-03", "F2", "cita GGB", '"Grupo Gay da Bahia" OR "Gay Group of Bahia" OR "Grupo Gay de Bahia"'),
    ("OA-F2-04", "F2", "cita ANTRA/TMM/TGEU",
     '("Trans Murder Monitoring" OR "ANTRA" OR "Transgender Europe" OR "TGEU") AND ' + GRP),
    ("OA-F3-01", "F3", "Bolsonaro + LGBT/homofobia (tema)",
     'Bolsonaro AND (LGBT OR LGBTQ OR homophobia OR homophobic OR "sexual minorities" OR gay OR transphobia)'),
    ("OA-F3-02", "F3", "cura gay / terapia de conversao + Brasil", '("cura gay" OR "gay cure" OR "conversion therapy" OR "reparative therapy" OR "reversão sexual") AND (Brazil OR Brasil OR Brazilian)'),
    ("OA-F3-03", "F3", "extermination/genocide + grupo",
     '(extermination OR genocide OR "license to kill" OR "licença para matar" OR extermínio OR genocídio) AND ' + GRP),
    ("OA-F3-04", "F3", "direita/right-wing + persecucao do grupo",
     '("right-wing" OR "far-right" OR "extrema direita" OR "governo de direita" OR conservative) AND (persecution OR perseguição OR "anti-LGBT policies" OR "rollback" OR "retrocesso") AND ' + GRP),
    ("OA-F4-01", "F4", "homofobia mito/negacao",
     '(homophobia OR homofobia OR LGBTfobia) AND (myth OR mito OR denial OR denialism OR negacionismo OR "does not exist" OR "não existe")'),
    ("OA-F4-02", "F4", "estatistica de violencia LGBT inflada/exagerada",
     GRP + ' AND (statistics OR estatísticas OR numbers OR data OR dados) AND (inflated OR exaggerated OR fabricated OR inflados OR inventados OR exagerados OR "falsos")'),
]
