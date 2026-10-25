# Briefing BECOS (2026-10-12) - 3 becos de evidência

> [!NOTE]
> Playbook carregado: factual-context. Sem subagentes, sem Playwright, sem scimagojr, sem OpenAlex. Ledger: `research-2026-10-12-deep/sources.jsonl` (28 registrados por esta rodada via `emit_sources.py`, 0 rejeitados; o arquivo já tinha outras linhas de rodadas anteriores).
> Arquivos baixados: `fontes/p2-deep-becos/` (dado não confiável: lido só com `pdftotext`/`python3 -I`, nunca executado).

| Beco | Status | Resumo |
|---|---|---|
| 1. Interior (Espanha) 2025 | ✅ PDF oficial obtido (via Wayback) | SOGI = 571 hechos (delitos); total 2.417 = 2.242 delitos + 175 infrac. adm./incidentes; metodologia SEC pp. 55-58 |
| 2. Mascarenhas 2018 PW 2550 | ✅ abstract verbatim + versão completa (Sousa 2020) | só completude; sem motivação; sem desagregação por UF |
| 3. RNFJA (Argentina) | ✅ bases abertas 2017-2024 baixadas; 🚫 "notas 2023/2024/2025" separadas não existem; 🚫 base 2025 ainda não publicada | reclassificação ex post: remoções 0-0,9% a.a., remoções+adições 0-3,2% a.a. (2017-2022) |

---

## 1. Ministerio del Interior - Informe 2025 (delitos e incidentes de odio) - ✅

**Documento.** "Informe sobre la evolución de los delitos e incidentes de odio en España 2025", PDF de 62 páginas, metadados do PDF: autor "Ministerio del Interior (España)", CreationDate 2026-05-28. Apresentado em 03/06/2026 (nota de prensa, El Pardo, Comisión de Seguimiento do III Plan de Acción 2025-2028).

**Arquivos locais:**

- `fontes/p2-deep-becos/interior_odio_2025.pdf` (sha256 `14ad2f1caf3d72e9dfaaed902d37afd6e6b1a41f1e5489095a61feb6e6495635`)
- `fontes/p2-deep-becos/nota_interior_wayback.html` e `nota_interior_wayback.txt` (nota de prensa)
- `fontes/p2-deep-becos/balances_wb.html` (índice "Balances e informes", de onde saiu o link do PDF)

**URL oficial do PDF** (ao vivo é 403 Cloudflare; baixado do snapshot Wayback 2026-09-10, `.../web/20260910005759if_/...`):
`https://www.interior.gob.es/opencms/export/sites/default/.galleries/galeria-de-prensa/documentos-y-multimedia/balances-e-informes/2025/Informe-sobre-la-evolucion-de-los-delitos-e-incidentes-de-odio-en-Espana-2025.pdf`

**Números (tabela "Hechos conocidos", PDF p. 9, verbatim):**

| Ámbito | 2023 | 2024 | 2025 | Var. 25/24 |
|---|---|---|---|---|
| ORIENTACIÓN SEXUAL E IDENTIDAD DE GÉNERO | 522 | 528 | 571 | 8,14% |
| RACISMO/XENOFOBIA | 856 | 804 | 934 | 16,17% |
| TOTAL DELITOS | 2150 | 1869 | 2242 | 19,96% |
| INFRAC.ADM. Y RESTO DE INCIDENTES | 118 | 86 | 175 | 103,49% |
| TOTAL DELITOS E INCIDENTES DE ODIO | 2268 | 1955 | 2417 | 23,63% |

- **Total de hechos (manchete): 2.417** (delitos + infrações administrativas/incidentes). Os ámbitos somam 2.242 = "TOTAL DELITOS" (soma conferida: 20+69+29+75+11+15+183+59+241+35+571+934 = 2.242); as 175 infrações administrativas/incidentes NÃO estão distribuídas por ámbito na tabela da p. 9. Ou seja, **571 = SOGI dentro dos delitos** (25,5% dos delitos; 23,6% do total 2.417). Os percentuais do gráfico da p. 9 (SOGI 24,45%, racismo 42,95%) não são consistentes com um único denominador (571/0,2445 = 2.335; 934/0,4295 = 2.175); não usar o gráfico, usar a tabela.
- **Esclarecidos SOGI**: 437 (2025) vs 398 (2024) (p. 9), 76,5% de 571.
- **Victimizaciones SOGI** (p. 13, verbatim): "ORIENTACIÓN SEXUAL E IDENTIDAD DE GÉNERO  445 (Hombre)  170 (Mujer)  0 (Per.Jur.)  0 (Desc.)  615 (Total)"; total geral de victimizaciones 2.294 (delitos 2.231 + infrac./incidentes 63).
- Nota de prensa (confere): 2.417 (+23,6%), SOGI 571, racismo/xenofobia 934, ideologia 241 (+64%), 65,6% esclarecidos, 1.018 detidos/investigados.
- **Erro na nota de prensa**: diz "esclarecieron en 2024 el 65,6%" (deveria ser 2025). Não é erro do PDF.

**Metodologia (SEC) - PDF pp. 55-58 (cap. 8 "Metodología estadística"):**

- 8.1 Origem: "Los datos han sido obtenidos del Sistema Estadístico de Criminalidad (SEC), incluido en el Área del Sistema Estadístico y Atención a Víctimas de la Dirección General de Coordinación y Estudios de la Secretaría de Estado de Seguridad." Corpos policiais computados: Policía Nacional, Guardia Civil, polícias autonômicas (Ertzaintza, Mossos d'Esquadra, Policía Foral de Navarra) e Policías Locales que facilitam dados ao SEC (p. 55).
- 8.2: delitos de ódio (agravante genérico art. 22.4.ª CP + discurso de ódio art. 510 CP) separados de "infracciones administrativas y otros incidentes" desde o informe 2019; "los datos publicados hasta ese año no coinciden" (p. 55). Definição acordada entre as instituições do Acuerdo para cooperar contra racismo, xenofobia, LGTBIfobia (p. 56).
- Ámbito SOGI (p. 56): "cualquier hecho que señala la existencia de un móvil de odio o discriminación hacia la víctima por su orientación sexual/identidad de género."
- Explotação (p. 58): "se hace en base a la fecha de comisión y a la localización del hecho ... independientemente de la unidad policial que lo conozca y de la fecha de instrucción". "Hechos conocidos" = infrações penais e administrativas + incidentes conhecidos pelas FCS por denúncia ou atuação de ofício; "esclarecidos" inclui o caso em que "la investigación revele que, en realidad, no hubo infracción".
- Ressalva: SEC = hechos **conocidos pela polícia**, não vítimas que denunciam a ONGs; a fonte não informa taxa de subnotificação.

**Tentativas (todas):**

1. WebSearch: achou nota de prensa e mídia (sem link direto do PDF).
2. WebFetch / curl direto em interior.gob.es: 403 (Cloudflare "Just a moment").
3. Wayback `available` do PDF: snapshot 2026-07-18 existe; da página de nota: 2026-09-26; do índice Balances e informes: 2026-09-10. Link do PDF extraído do índice arquivado (`balances_wb.html`).
4. Download do PDF via Wayback `20260910005759if_`: 1ª tentativa truncou em 5,2 MB (timeout), retomada com `curl -C -` até 10.423.025 bytes; `pdfinfo` = 62 páginas, abre OK.
5. Não foi preciso OBERAXE / datos abiertos.

---

## 2. Mascarenhas et al. 2018, PW 2550 (Injury Prevention 24 Suppl 2, Safety 2018) - ✅

**Metadados (Crossref, `crossref_331.json`):** "PW 2550 Data quality of the interpersonal and self-inflicted violence notification information system - brazil, 2011-2014"; autores Mascarenhas, Sousa, Lima, Rodrigues, Lima (Federal University of Piauí State, Teresina); tipo proceedings-article; publicado 2018-11 (impresso), 2018-09-20 (online); páginas A119.2-A119; DOI 10.1136/injuryprevention-2018-safety.331; sem abstract no Crossref.

**Acesso:** `injuryprevention.bmj.com` e `doi.org` = 403; Wayback não tem snapshot; Europe PMC = 0 resultados (não indexado); Unpaywall `is_oa=false`. O **abstract verbatim veio da API Semantic Scholar** (`mascarenhas2018_s2.json`, `fontes/p2-deep-becos/mascarenhas2018_s2.json`).

**Abstract verbatim (Semantic Scholar):**

> Introduction The notification of interpersonal and self-inflicted violence (ISV) is a component of the epidemiological surveillance of this public health issue. Brazil has a large network of Health Information Systems that allows to describe the epidemiological reality and to manage the health services, but it is fundamental that the information provided by these systems be reliable and real. Thus, completeness is one of the attributes used to evaluate the quality of the information in public health surveillance systems. Objective Evaluate the data quality of the Interpersonal and Self-inflicted Violence Notification Information System (ISVNIS) in Brazil, from 2011 to 2014. Methods a descriptive study of the ISVNIS data was carried out considering de percentage of incompleteness of essential e mandatory variables among all variables of ISV notification form. Percentages of incompleteness were calculated on the basis of the not filled fields (filled in with ignored or blank) for each variable by year of notification. The annual average of incompleteness was calculated and classified as follow: Excellent (incompleteness <5%), Good (5%-9.9%), Regular (10%-19.9%), Bad (20%-49.9%) and Too Bad (≥50%). Findings from 2011 to 2014, the number of ISV notifications increased 84.3%. In general, the average incompleteness of the variables analyzed was classified as Bad (22.4%), ranging from Regular for the individual notification (14.4%) and the victim identification (14.6%) variables, to Bad for closure of notification (30.8%) and case referral (32.9%) variables. Conclusion and policy implications The ISV notification data presented bad completion quality, despite the increase in the number of notifications in the analyzed period. Data monitoring and training of professionals in the correct filling of ISV notifications is recommended.

**Respostas às 3 perguntas:**

| Pergunta | Resposta |
|---|---|
| Quais variáveis avalia? | **Só completude** (% de campos "ignorado"/em branco), variáveis "essential and mandatory". Não avalia consistência nem duplicidade. Blocos citados: notificação individual, identificação da vítima, conclusão e encaminhamento. |
| Inclui o campo de motivação? | **Não consta no abstract.** No texto completo (Sousa 2020, abaixo) a palavra "motivação/motivo" não aparece nenhuma vez, e os campos orientação sexual / identidade de gênero também não são avaliados. |
| Desagrega por UF? | **Não.** Análise nacional por variável/bloco/ano (2011-2014). "Unidade da Federação de notificação" só aparece como variável 100% completa, excluída das médias. |

**Versão completa (OA) do mesmo estudo:** Sousa CMS, Mascarenhas MDM, Lima PVC, Rodrigues MTP. "Incompletude do preenchimento das notificações compulsórias de violência - Brasil, 2011-2014." Cad Saúde Colet 2020; 28(4):477-487. DOI 10.1590/1414-462x202028040139 (mesmos autores, mesma base e mesmos números 22,4% / 14,4% / 14,6% / 30,8% / 32,9%). Texto integral em `fontes/p2-deep-becos/sousa2020_scielo.txt` (HTML extraído; HTML bruto em `sousa2020_scielo.html`). Confirma no Método: banco do Ministério da Saúde (DANTPS/SVS/MS) "previamente submetido à exclusão de casos com inconsistências de informação e duplicidades"; ficha com blocos "dados gerais, notificação individual, residência, pessoa atendida, ocorrência, violência, violência sexual, provável autor, encaminhamento, dados finais"; critério Romero e Cunha; software Stata 14. A Tabela 2 lista tipo de violência e meio de agressão, sem campo de motivação. Inferência para o projeto: o estudo de 2011-2014 **não serve** para estimar a completude do campo de motivação/orientação sexual/identidade de gênero.

**Achado lateral (relevante ao indicador):** `fontes/p2-deep-becos/rj2018_cadsc_qualidade_notificacoes_violencia.pdf` (Cad Saúde Colet 2018; 26(3):318-326, Rio de Janeiro 2009-2016) diz que a penúltima versão da ficha incluiu "orientação sexual", "identidade de gênero" e "motivo da violência", e que esses dados "por enquanto, só estão disponíveis no site do estado do Rio de Janeiro" (p. 2). Dados de identidade de gênero disponíveis só a partir de 2014 (p. 3). Obs.: o arquivo foi baixado primeiro por engano como suposto Sousa 2020 (o ID SciELO pertencia a este artigo); a entrada do ledger tem essa nota.

**Tentativas:** WebSearch (3x), Europe PMC (DOI e título), Crossref, Semantic Scholar (sucesso), Unpaywall (closed), Wayback BMJ (vazio), doi.org/BMJ direto (403), SciELO (sucesso para Sousa 2020; PDF `?format=pdf` 503/404 em outras URLs, HTML funcionou na 1ª tentativa). Não tentado: ResearchGate, Lattes, ARCA/Fiocruz (desnecessário após obter texto integral do estudo irmão).

---

## 3. RNFJA (Argentina) - bases abertas e reclassificação ex post - ✅ parcial

**Onde está:**

- Página oficial: `https://www.csjn.gov.ar/omrecopilacion/omfemicidio/registroFemicidiosDatosAbiertos.html` (OM-CSJN). O portal CKAN `https://datos.csjn.gov.ar` hospeda 8 datasets "BASES DE DATOS DE FEMICIDIOS 2017 ... 2024" (causas, víctimas, sujeitos ativos em xlsx e sav + libro de códigos em PDF por ano). Ano 2025: **não publicado** (a página lista até 2024; frequência anual, "31 de diciembre").
- `datos.jus.gob.ar` tem outro registro (URSSF, Ministério da Justiça, legado 2017-2020, csv). **Não é o RNFJA.**
- Arquivos baixados: `fontes/p2-deep-becos/rnfja/open_data/` (xlsx 2017-2023 e causas 2024; 2024 víctimas só em `.sav`, lido com pyreadstat `encoding='latin1'`: 247 vítimas, Tipo_victima=1 -> 228 diretas, igual ao relatório), `fontes/p2-deep-becos/rnfja/informes/` (relatórios 2021-2025 + anexo + resumos), `fontes/p2-deep-becos/rnfja/notas_metodologicas_id1.bin` (PDF) e `.txt`.

**"Notas metodológicas 2023/2024/2025":** 🚫 **não existem como documentos separados.** A API pública da OM-CSJN (`getDocumentosPublicosByTipoDocumento?idTipoDocumento=6`) devolve **um único** arquivo "Notas metodológicas - datos abiertos RNFJA" (idDocumento=1, 8 páginas, PDF). Ele lista adições/remoções por jurisdição dos observatórios 2017, 2018, 2019, 2017-2020 (corte 30/06/2022) e 2017-2022 (corte 30/06/2024). Não há nota para as bases 2023/2024; o relatório 2025 (id384) diz que 6 causas "informadas en seguimiento" (Córdoba, Chubut, Jujuy, Santiago del Estero, Santa Fe, Tucumán) "podrían ser agregadas".

**Declaração institucional (verbatim, anexo `id337.txt` p. 2 e relatório 2025 `id384.txt`):** "los totales anuales aquí citados difieren levemente de los publicados oportunamente en cada informe anual del RNFJA, ya que han sido rectificados posteriormente en función de las revisiones hechas a raíz de los informes del Observatorio". Relatório 2022 (id170, nota 16): "se agregaron 12 víctimas directas: 3 en 2017, 5 en 2019 y 4 en 2020".

**Cálculo (arquivo CSV: `fontes/p2-deep-becos/rnfja/reclassificacao_rnfja_2017_2024.csv`):** "preliminar" = valor publicado no relatório anual (corte 31/12); "final" = base aberta; adições/remoções = itens da nota metodológica (cada item citado é 1 causa / 1 vítima direta).

| Ano | Publicado (diretas) | Base aberta (diretas) | Delta líquido | Removidas (nota) | Adicionadas (nota) | Removidas / publicado | (Rem. + adic.) / publicado |
|---|---|---|---|---|---|---|---|
| 2017 | 251 | 252 | +1 | 2 | 5 | 0,80% | 2,79% |
| 2018 | 255 | 257 | +2 | 2 | 4 | 0,78% | 2,35% |
| 2019 | 252 | 260 | +8 | 0 | 8 | 0,00% | 3,17% |
| 2020 | 251 | 254 | +3 | 1 | 4 | 0,40% | 1,99% |
| 2021 | 231 | 231 | 0 | 0 | 0 | 0,00% | 0,00% |
| 2022 | 226 | 226 | 0 | 2 | 2 | 0,88% | 1,77% |
| 2023 | 250 | 250 | 0 | 0 | 0 | 0,00% | 0,00% |
| 2024 | 228 | 228 | 0 | 0 | 0 | 0,00% | 0,00% |

- Agregado 2017-2022: publicado 1.466 diretas; removidas 7 (**0,48%**); adicionadas 23 (**1,57%**). O padrão dominante é **adição tardia (sub-registro inicial)**, não remoção. Em 2021, 2023 e 2024 o delta é zero porque o observatório ainda não revisou esses anos (o próprio relatório 2022 diz que "todavía no se agregaron para 2021 y 2022, ya que son muy recientes"), então 0% **não é prova de estabilidade**, é censura à direita.
- Reconciliação: o delta líquido bate com a soma dos itens da nota em 2018 (+4-2=+2), 2019 (+8), 2020 (+4-1=+3), 2022 (+2-2=0). **2017 não fecha**: itens da nota dão +3 e a diferença observada é +1 (252 vs 251); também a nota diz que Salta teve 19 causas de 2017 incorporadas depois ("no habían sido informados oportunamente"). Não resolvido.
- Fraqueza das fontes: os publicados 2017-2019 (251/255/252) vêm da **imprensa/Chequeado/Diario de Cuyo/El Litoral/Diario Libre** (relatórios originais 2017-2020 não estão na API da OM-CSJN; não baixados). 2020 (251 diretas, 36 vinculadas, 287 total) confirmado no relatório 2021 (id115: "pasa de 287 casos a 251") e na imprensa. 2021-2024 são de relatórios primários baixados (231 / 226 / 250 / 228).
- Contradição interna das fontes: a nota (p. 4-6) diz que as correções dos observatórios foram "rectificados y/o completados en las bases de datos, pero no actualizados para las bases abiertas", enquanto o anexo e o relatório 2022/2025 dizem que as bases abertas "se encuentran publicadas rectificadas". Os números das bases (252/257/260/254) refletem as correções, então vale a segunda versão.
- Outras remoções não quantificadas: a nota cita a retirada de sujeitos ativos (não vítimas) em várias jurisdições; não entram na taxa.
- Métrica pedida ("removidos / preliminares"): é um **limite inferior** (só o que a nota lista) e mede reclassificação **dentro de um registro de causas já definido**, não a taxa de reclassificação de homicídio para femicídio (o RNFJA inclui causas "em que não se pôde descartar" a hipótese; ver critério no relatório 2024).

**Tentativas / URLs:** `om.csjn.gob.ar/consultaTK/web/vistaRegistroNacionalFemicidios` (redireciona a `/om/`, sem dados), `csjn.gov.ar/omrecopilacion/omfemicidio/home.html` (404), `datos.jus.gob.ar` (existe, mas outro registro), `datos.csjn.gov.ar` API CKAN (OK), `om.csjn.gob.ar/consultaTalleresWeb/.../getDocumentosPublicosByTipoDocumento?idTipoDocumento=1..60` (varredura; tipos 4 = relatórios, 5 = bases, 6 = notas, 7 = provinciais), download de cada PDF por `verDocumentoById?idDocumento=N`. pyreadstat (venv no scratchpad): `.sav` 2024 de vítimas só abre com `encoding='latin1'`. Libros de códigos 2023 e 2024 grepados (nota metodol/rectific/agreg/retir/elimin): sem registro de revisão por caso, 🚫 reforçado.

---

## Becos

- Interior: os percentuais do gráfico da p. 9 (SOGI 24,45%) não fecham com nenhum denominador único; usar a tabela (571). Volta se: precisar do percentual oficial por ámbito.
- Interior: as 175 infrações administrativas/incidentes não têm quebra por ámbito no PDF lido (p. 9); não dá para saber quantas são SOGI. Volta se: o anexo estatístico (pp. 42-52) ou o portal estadisticasdecriminalidad.es trouxer a quebra.
- Mascarenhas 2018: texto completo do pôster não existe/indisponível; vale o abstract + Sousa 2020. Volta se: precisar de tabelas por variável do pôster (não necessário).
- RNFJA: relatórios originais 2017-2019 não obtidos (publicados vêm de imprensa); reclassificação 2021-2024 censurada. Volta se: aparecer nota do observatório 2023-2024 ou base 2025 (31/12/2026).
- Dois erros menores de fonte registrados: a nota de prensa do Interior escreve "esclarecieron en 2024" onde é 2025; o arquivo `rj2018_...pdf` não é Sousa 2020.
