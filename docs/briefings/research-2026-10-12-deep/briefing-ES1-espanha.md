# Briefing ES-1 — Espanha: dispensa (art. 416 LECrim), denúncias falsas, crimes de ódio, literatura em espanhol

Data da coleta: 2026-10-11/12 · célula ES-1 · modo deep · playbook loaded: factual-context + paper-deep-dive
Fontes brutas em disco: `fontes/p2-deep-es/`
Ledger: `research-2026-10-12-deep/sources.jsonl` (42 linhas desta célula, 0 rejeitadas; o arquivo tem mais linhas de outras células)
Convenção de tag: `[SOURCE: multilingual-term-expansion:es:<base>:<chave>]`. Página impressa = página citada; quando diferente do PDF, está dito.

> [!IMPORTANT]
> Resumo executivo. (1) Os 10-11% de mulheres que se acolhem à dispensa são número oficial do CGPJ, confirmado em tabela (2024: 18.629 de 183.908 = 10,13%; 2025: 20.977 de 185.188 = 11,33%; 1T2026: 5.337 de 45.220 = 11,80%). (2) A cifra "0,006%" de denúncias falsas é real, mas mede CAUSAS acompanhadas (12 de 199.282 denúncias em 2023), não condenações; "0,0069%" não aparece em nenhuma Memoria lida. (3) Interior 2024: 1.955 fatos de ódio, 528 por orientação sexual e identidade de gênero (+1,15%); a pesquisa de vitimização da própria ONDOD (2024) dá 6,8% de vítimas que denunciaram. (4) A literatura espanhola revisada por pares sobre denúncias falsas é escassa e de qualidade desigual; a única peça com "mito ou realidade" no título é um ensaio com posição declarada, não estimativa.

---

## Alvo 1 — CGPJ: mulheres que se acolhem à dispensa (art. 416 LECrim)

### 1.1 Série nacional anual 2015-2025

Fonte canônica da série: planilha oficial "Series anuales Procesos de Violencia de Género - Año 2025" (aba "Denuncias, Víctimas y Renuncias", linhas 12, 17, 21, 24), baixada de poderjudicial.es; sha256 no ledger. `[SOURCE: multilingual-term-expansion:es:poderjudicial.es:series-anuales-2025.xlsx]`

| Ano | Denúncias | Mulheres vítimas | Casos de dispensa | Dispensa / vítimas (calculado) | Razão publicada na planilha |
|---|---|---|---|---|---|
| 2015 | 129.193 | 123.725 | 15.321 | 12,38% | 12,4% |
| 2016 | 142.893 | 134.620 | 16.118 | 11,97% | 12,0% |
| 2017 | 166.260 | 158.217 | 16.464 | 10,41% | 10,4% |
| 2018 | 166.961 | 158.590 | 17.347 | 10,94% | 10,9% |
| 2019 | 168.057 | 161.378 | 17.205 | 10,66% | 10,66% |
| 2020 | 150.785 | 145.731 | 14.932 | 10,25% | 10,25% |
| 2021 | 162.848 | 159.352 | 15.720 | 9,86% | 9,86% |
| 2022 | 182.065 | 176.483 | 16.900 | 9,58% | 9,58% |
| 2023 | 199.282 | 194.658 | 19.500 | 10,02% | 10,02% |
| 2024 | 199.094 | 183.908 | 18.629 | 10,13% | 10,13% |
| 2025 | 204.342 | 185.188 | 20.977 | 11,33% | 11,33% |

Ressalvas da série (todas verificadas nos arquivos):

- Revisão do denominador de 2023. O Informe anual 2024 (tabela da p. 37) usa 193.516 vítimas em 2023 e ratio 10,08; a nota de imprensa de 2024, a Memoria da FGE e a planilha de 2025 usam 194.658 e 10,02. Usar a planilha como canônica e anotar a revisão.
- Descontinuidade 2016-2017: vítimas saem de 134.620 para 158.217 (+17,5%) e a razão cai de 12,0% para 10,4%. As fontes lidas não explicam a quebra. Não comparar 2015-2016 com 2017+ sem checar.
- Nas séries trimestrais antigas (2012-2016) a linha "Total víctimas" é igual ao número de denúncias (2016: 142.893), logo as razões trimestrais antigas não são dispensa/vítimas.
- Aviso de não comparabilidade: nota do TSJ Extremadura de 23-06-2025 (1T2025) diz que o total de dispensas "no puede ponerse en relación con las registradas en los ejercicios anteriores" por "nuevos controles estadísticos". O Informe anual 2025 compara 18.629 com 20.977 (+12,60%) sem esse aviso (zero ocorrências na busca no PDF). O salto de 2025 pode ser em parte metodológico. Hipótese, não provada.
- Duas séries oficiais do CGPJ não reconciliam. "La violencia de género en 10 indicadores 2025" (p. 2, gráfico "Renuncias") traz 14,2% (2016), 12,2% (2017), 11,4% (2020), 10,5% (2023), 9,9% (2024), 10,8% (2025), contra 11,97%, 10,41%, 10,25%, 10,02%, 10,13%, 11,33% do informe anual. Testei dispensa/vítimas e dispensa/denúncias: nenhuma bate. Denominador não declarado. Não misturar as duas séries; usar o informe anual.
- "Casos" vs "mulheres": as tabelas dizem "Casos en los que la víctima se acoge a la dispensa" e a nota de imprensa diz "mujeres víctimas que se acogieron". A razão é casos/mulheres vítimas, não mulheres únicas/mulheres únicas. Nota de imprensa de 2024 também escreve 10,02% para 2023 enquanto a tabela do PDF diz 10,08 (ver revisão acima).

### 1.2 Trechos verbatim e páginas (informes anuais)

- Informe anual 2024, p. 37 (tabela "Diferencia Denuncias, mujeres víctimas de Violencia de Género y casos en que la víctima se acoge a la Dispensa"): "Casos en que la víctima se acoge a la dispensa a la obligación de declarar 19.500 | 18.629 | -4,47%"; "Ratio-casos en que la víctima se acoge a la dispensa a la obligación de declarar/mujeres víctimas de violencia de género 10,08 | 10,13 | 0,52%". `[SOURCE: multilingual-term-expansion:es:poderjudicial.es:informe-anual-2024]`
- Informe anual 2024, p. 7: "Españolas 10.269 ... 8,87; Extranjeras 8.360 ... 12,26" (dispensa por 100 vítimas, por nacionalidade). Nota de imprensa: "El número de mujeres víctimas que se acogieron a la dispensa del deber de declarar (18.629) disminuyó un 4,47 % respecto a 2023."
- Informe anual 2025, p. 37: "Casos en que la víctima se acoge a la dispensa a la obligación de declarar 18.629 | 20.977 | 12,60%"; "Ratio ... 10,13 | 11,33 | 11,83%". P. 7: españolas 11.607 (10,17), extranjeras 9.370 (13,19). `[SOURCE: multilingual-term-expansion:es:poderjudicial.es:informe-anual-2025]`
- Nota de imprensa 2025: "El número de mujeres víctimas que se acogieron a la dispensa del deber de declarar (20.977) aumentó un 12,60 % respecto a 2024. En otros términos, tomaron esta decisión 11 mujeres víctimas de cada cien (11,33 %)."
- A numeração das páginas do PDF é a impressa + 1 (a tabela da p. 37 está no pdf 38; a de nacionalidade, p. 7, no pdf 8).

### 1.3 Dado trimestral mais recente

- 1T2026 (publicado 24-06-2026), Informe trimestral, p. 37: Denúncias 47.865 -> 50.911 (+6,36%); Mulheres vítimas 43.586 -> 45.220 (+3,75%); "Casos en que la víctima se acoge a la dispensa" 4.913 -> 5.337 (+8,63%); "Ratio ... 11,27 | 11,80 | 4,70%". Planilha "Datos y Evoluciones" (aba Evolución Renuncias): 2.953 por espanholas, 2.384 por estrangeiras. `[SOURCE: multilingual-term-expansion:es:poderjudicial.es:1T2026]`
- Atenção: a coluna "ratio" por CCAA dessa planilha usa outro denominador (renuncias/denúncias: Espanha 10,48%), não vítimas. Para o nacional use 11,80% (5.337/45.220).
- 2T2026 e 3T2026: não encontrados na página do Observatório em 2026-10-11 (último item listado = 1T2026). Beco, não "ausência confirmada".

### 1.4 A "nota metodológica" de 2015

Não existe documento metodológico autônomo; é nota de rodapé de planilha. Verbatim, planilha "Series anuales ... Año 2018", aba "Denuncias, Víctimas y Renuncias", linha 25, repetida na de 2025 (linha 28) e na "Series ... 3T2017": "* Desde 2015 se sustituyo el concepto de renuncia por el de La victima se acoge a la dispensa a la obligación de declarar como testigo (art. 416 LECrim.)". O rótulo "Renuncias en el año" ainda sobrevive no informe anual 2025 (p. 7). `[SOURCE: multilingual-term-expansion:es:poderjudicial.es:series-2016-2018.xlsx]`

---

## Alvo 2 — Fiscalía General del Estado: "denuncias falsas"

Rotulagem para não errar a edição: a URL `memoriaYYYY+1` cobre o ejercicio YYYY. A URL `memoria2026` (HTML com título "Memoria ... 2025") cobre o ejercicio 2025, publicada em 2026. A mesma tabela é "dinâmica" e revisada retroativamente, então a Memoria 2026 (ejercicio 2025) é a canônica para 2009-2025.

### 2.1 Onde está e o que diz

Memoria FGE (ejercicio 2025, publicada 2026), cap. III.1 Violencia sobre la Mujer, seção 1.4.2 "Retiradas de acusación y denuncias falsas", pp. 611-613. `[SOURCE: multilingual-term-expansion:es:fiscal.es:memoria2026-cap_III_1_4]`

- p. 611: "En cuanto a las deducciones de testimonio por denuncia falsa, durante el año 2025 se han comunicado seis asuntos, siendo esencial para la solicitud de esta deducción la acreditación inequívoca de que la denunciante ha faltado a la verdad en su declaración, como en aquellos supuestos en los que ella misma reconoce esta circunstancia. En uno de los procedimientos ha recaído sentencia condenatoria firme."
- p. 611: "...han sido notificados cuatro asuntos [de falso testimonio], todos en Madrid capital."
- p. 612: "A continuación, se inserta un cuadro con los datos estadísticos de las denuncias falsas desde el año 2009, así como la proporción que suponen respecto del número total de denuncias. Se trata de un cuadro dinámico, que se revisa continuamente... las deducciones de testimonio se contabilizan en el año en el que se acordó la deducción, con independencia del momento en que se conozca... El total de denuncias es el publicado por el Observatorio contra la Violencia Doméstica y de Género del CGPJ."
- p. 613 (linha 2025 e total): "2025 | 204.342 | 6 | 0,003 | 4 | 0,002 | 2 | 0,0010 | 1 | 0,0005 | 0 | 0,0000" e "Total | 2.655.581 | 442 | 0,017 | 39 | 0,001 | 33 | 0,0015 | 191 | 0,007 | 180 | 0,0068". Colunas: causas em seguimento por denúncia; não consta incoação; em trâmite; sentenças condenatórias; sentença absolutória, sobreseimento provisório ou não incoação (cada uma seguida de %).
- p. 613: "El cuadro, que abarca el análisis desde el año 2009 al 2025, refleja cómo el porcentaje de sentencias condenatorias por denuncia falsa es ínfimo. El promedio entre los años 2009 y 2025 es del 0,007 %."

### 2.2 Como está calculado o percentual (numerador / denominador)

- Numerador: "causas en seguimiento por denuncia [falsa]" = deduções de testemunho por denúncia falsa comunicadas à Unidade de Violencia sobre la Mujer pelos fiscais delegados (e, em parte, pela Inspección Fiscal), contadas no ano em que a dedução foi acordada. Não é número de denúncias provadas falsas; é número de casos em que se pediu ou acordou investigar a denunciante.
- Denominador: total de denúncias do CGPJ no ano (não mulheres vítimas).
- Coluna de condenações: sentenças condenatórias por denúncia falsa / total de denúncias do mesmo ano.

### 2.3 A cifra "0,006%" e a cifra "0,0069%"

| Cifra | O que é, exatamente | Fonte |
|---|---|---|
| 0,006% | 12 causas em seguimento por denúncia falsa em 2023 / 199.282 denúncias de 2023 = 0,00602%. É incoação/dedução, NÃO condenação. As condenações de 2023 são 3 (0,0015%). | Memoria ejercicio 2023 (URL memoria2024), pp. 529-531; repetida na tabela de 2026, p. 613 |
| 0,0069% | NÃO aparece verbatim em nenhuma das 6 Memorias que conferi (ejercicios 2020 a 2025, tabelas e texto). Candidatos próximos: 0,0068% (coluna "absolutória/SP/não incoação", total 2009-2025 = 180/2.655.581) e 0,007% (condenações 191/2.655.581 = 0,0072%). Provável arredondamento ou citação de segunda mão. | Memoria 2026, p. 613 |
| Média histórica citada pela FGE | 0,0074% (ejercicio 2020: 134 condenações desde 2009), 0,0084% (ejercicio 2021), 0,0083% (2022), 0,0084% (2023; com causas em trâmite somadas, 0,00945%, Memoria 2024 p. 531), 0,0082% (2024), 0,007% (2025) | Memorias dos ejercicios 2020-2025 |

Avisos de leitura (importantes para quem cita):

1. A série é retroativamente revisada e as cifras recentes estão censuradas à direita (sentenças chegam anos depois). Condenações por ano de dedução, em edições sucessivas: 2022 = 5 (Memoria 2024) -> 6 (Memoria 2025) -> 7 (Memoria 2026); 2020 = 2 -> 2 -> 5 -> 8 -> 8 (Memorias 2022 a 2026); 2024 = 1 condenatória e 0 absolutórias (Memoria 2025) -> 1 e 2 (Memoria 2026), com "em trâmite" 7 -> 5. Portanto o "1" de 2025 tende a subir e o 0,0005% de 2025 é piso, não estimativa.
2. Erro de impressão na tabela da Memoria 2026: linha 2018, coluna "En trámite", mostra 0,0060 para 1/166.936; o valor correto é ~0,0006 (a Memoria 2025 traz 0,00060). Não propagar.
3. A própria FGE (Memoria ejercicio 2020) escreve "de cada 12.747 denuncias, una es falsa", o que equivale a 0,0078%, enquanto no mesmo parágrafo diz 0,0074%. Inconsistência interna da fonte (134/1.708.075 = 0,0078%).
4. O indicador subestima denúncias falsas não perseguidas e não distingue falsidade de retratação: a própria Memoria 2025 (p. 614, ejercicio 2024) descreve vítimas que "se muestran vagas e imprecisas... manifiestan no recordar lo acontecido o, abiertamente, reconocen que los hechos denunciados no eran ciertos" e atribui a "la dependencia emocional con el agresor o el profundo temor hacia él". Ou seja, retratação em juízo não implica denúncia falsa.
5. Retiradas de acusação ligadas à dispensa colapsaram depois da LO 8/2021: Memoria ejercicio 2023 (URL memoria2024), p. 529: "Ninguna de las retiradas comunicadas a la Unidad ha venido motivada por la circunstancia de haberse acogido la víctima al artículo 416 LECrim", contra 0,5% em 2022, 8% e 15,38% em 2021 (1º e 2º semestres), 50% e 72,7% em 2020. Ejercicio 2025: 12 retiradas (36 em 2024).
6. Contexto oposto sobre a dispensa: Memoria ejercicio 2024 (URL memoria2025), p. 626: "Se confirma por varias fiscalías que va disminuyendo el número de mujeres que desean acogerse a la dispensa", enquanto o CGPJ mostra 10,13% estável em 2024 e 11,33% em 2025. Na p. 627 a FGE cita 10,12% para 2024 (CGPJ: 10,13%) e 3,40% das mulheres nos Juzgados de lo Penal (1.117 de 32.845), 4,41% em 2023.

---

## Alvo 3 — Ministerio del Interior: delitos de odio

### 3.1 Informe 2024 (ejercicio 2024, publicado 2025)

Leitura via Chrome real (curl 403 Cloudflare; Wayback truncado em 5 MiB). Transcrição verbatim em `interior-odio-2024-trechos-lidos-chrome.md`; o sha256 do ledger é da transcrição, não do PDF. Página impressa = página do PDF. `[SOURCE: multilingual-term-expansion:es:interior.gob.es:informe-odio-2024]`

| Item | Valor | Página |
|---|---|---|
| Total delitos e incidentes de ódio 2024 | 1.955 (-13,8% vs 2.268 em 2023; 1.869 em 2022) | pp. 9 e 38 |
| Só "delitos" (sem infrações administrativas e resto de incidentes) | 1.869 em 2024 (2023: 2.150) | p. 9 |
| Orientação sexual e identidade de gênero | 528 (2022: 459; 2023: 522; var. +1,15%) | pp. 9 e 38 |
| Racismo/xenofobia | 804 (-6,07%) | p. 9 |
| Discriminação por sexo/gênero | 181 (-12,14%) | p. 9 |

- Texto (p. 38): "...seguido de los ámbitos de 'orientación sexual e identidad de género' con 528 hechos conocidos, que representa un ascenso de 1,15% con respecto a las cifras del año 2023".
- Metodologia (pp. 55-58): origem dos dados = Sistema Estadístico de Criminalidad (SEC) da Secretaría de Estado de Seguridad, com fatos conhecidos por Policía Nacional, Guardia Civil, polícias autonômicas (Ertzaintza, Mossos d'Esquadra, Policía Foral) e Policías Locales que alimentam o SEC (p. 55). "Hechos conocidos" = "infracciones penales y administrativas y resto de incidentes... bien por medio de denuncia interpuesta o por actuación policial realizada motu proprio" (p. 58). Definição consensuada com o acordo interinstitucional contra racismo, xenofobia, LGTBIfobia: "Todo delito al que sea de aplicación la circunstancia agravante genérica del artículo 22.4ª CP..." (p. 56). Definição do âmbito (p. 56): "Orientación sexual e identidad de género: cualquier hecho que señala la existencia de un móvil de odio o discriminación hacia la víctima por su orientación sexual/identidad de género." "Discriminación por razón de sexo/género" exclui os fatos contra orientação sexual e identidade de gênero.
- Lacuna de leitura: não encontrei nas páginas lidas um critério explícito sobre quem atribui o móvel (vítima, agente, instrutor). A leitura das pp. 55-58 foi por fatias de ~950 caracteres e ficou incompleta no fim da p. 56. Não afirmar o contrário.
- Contagem distingue "delitos" de "infracciones administrativas y resto de incidentes" desde o informe de 2019 (p. 55), o que quebra comparação com séries anteriores a 2019.

### 3.2 Informe 2025 (ejercicio 2025, publicado em junho de 2026)

Só a nota de imprensa do Interior (Chrome real): "...investigaron en 2025 un total de 2.417 infracciones penales e incidentes de odio en España, lo que supone un incremento del 23,6 por ciento respecto a 2024 y la cifra más alta de la serie histórica, iniciada en 2014"; "Los delitos de odio por racismo y xenofobia, con 934 hechos... aumento del 16,1 por ciento... Le siguen... orientación sexual e identidad de género (571 hechos)". 571 vs 528 = +8,1% (cálculo meu, não consta na nota). PDF do informe 2025 NÃO localizado (a listagem pública de publicações para em 2023 e na encuesta ONDOD 2024); portanto o número 2025 está em ⚠️ (só comunicado, sem página de PDF). Note a diferença de rótulo: 2025 diz "infracciones penales e incidentes", 2024 diz "delitos e incidentes".

### 3.3 Infradenúncia, fontes governamentais

- ONDOD/Interior, "Informe de la encuesta sobre delitos de odio (2024): víctimas y testigos", pp. 55-56 impressas (pdf 62-63): "De las 602 personas identificadas como víctimas, solo 41 (6,8%) responde haber interpuesto denuncia ante Fuerzas y Cuerpos de Seguridad. Esto sitúa la tasa de infradenuncia en 9 de cada 10 víctimas." Em 2021: 10,76% denunciaram. Metodologia (pp. 7-8): participação "voluntaria y anónima" via web, a partir de 14 anos; é amostra de autosseleção (inferência minha), logo a taxa não é prevalência populacional. Não é específica de LGBTI. Transcrição em `interior-ondod-encuesta-2024-trechos-lidos-chrome.md`.
- FRA, EU LGBTIQ survey III (2024), ficha Espanha, p. 2 (em inglês): "14% went to the police in Spain to report physical or sexual attacks. It is 11% across the EU-27." Pesquisa online com 100.577 respostas em 30 países, de autosseleção.

---

## Alvo 4 — Literatura em espanhol

Estado: ✅ = lido no texto integral e tese conferida; ⚠️ = lido com ressalva de escopo/método/idioma, ou só resumo; 🚫 = não lido ou fora do critério.

### 4.1 Denúncias falsas

| Autores, ano, periódico, DOI | Tese / número com trecho verbatim | Status |
|---|---|---|
| Pérez Fernández, F.; Bernabé Cárdaba, B. (2012). "Las Denuncias Falsas en Casos de Violencia de Género: ¿Mito o Realidad?" Anuario de Psicología Jurídica 22: 37-46. DOI 10.5093/aj2012a4 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.5093/aj2012a4]` | Ensaio não empírico com posição declarada. p. 41: "en España el asunto está prácticamente ausente de la literatura científica lo cual nos habla de un claro sesgo de autocensura en la investigación"; "ninguna de las fuentes estadísticas habituales... ofrece datos más o menos claros en este sentido". p. 42: de 480.663 procedimentos contra homens (LO 1/2004 até 2008), "132.137 varones –el 27.49% de los denunciados– jamás resultaron condenados" e "la ratio de renuncias... se cifra en torno al 10%". Cita a Memoria da FGE de 2006 (p. 357): o uso indevido da lei "no es cierto, aunque aparezcan casos aislados". Não estima prevalência de denúncia falsa; usa SAP e o "Informe Iceberg" de grupo de pais separados como apoio (p. 43, nota 4). | ⚠️ (não usar como evidência de prevalência; vale como retrato do debate em 2012. A afirmação de que as fontes oficiais não quantificam ficou superada: a Unidade da FGE registra desde 2009.) |
| Memorias FGE 2021-2026 (ver Alvo 2) | Única série oficial; limitações em 2.3. | ✅ |

### 4.2 Dispensa (art. 416 LECrim)

| Autores, ano, periódico, DOI | Tese / número com trecho verbatim | Status |
|---|---|---|
| Beltrán Montoliu, A. (2018). "Víctima de violencia de género y la dispensa del art. 416 Lecrim: evolución jurisprudencial". Revista de Derecho Penal y Criminología n.º 19: 13-46 (Crossref lança 2019). DOI 10.5944/rdpc.19.2018.24408 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.5944/rdpc.19.2018.24408]` | Resumo: a dispensa "propicia sentencias absolutorias y genera en la sociedad una percepción de impunidad judicial". p. 28: "casi la mitad de los procesos por violencia de género, terminan sin condena al acogerse la víctima... a la dispensa". Cuidado: a nota 62 sustenta isso com a Memoria da FGE (46 casos, 47,2% em 2016; 51,38% em 2015; 46% em 2014) e esses percentuais são sobre RETIRADAS DE ACUSAÇÃO, não sobre todos os processos. | ✅ doutrina e jurisprudência; ⚠️ a frase "casi la mitad" não generaliza |
| De la Herrán Ruiz-Mateos, S. (2021). "A vueltas con la dispensa del deber de declarar de las víctimas de violencia de género a propósito de la sentencia del TS 389/2020". RDPC n.º 23: 45-66. DOI 10.5944/rdpc.23.2020.28011 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.5944/rdpc.23.2020.28011]` | Conclusão (p. 19 do PDF): a posição do TS pressupõe que a dispensa seja "un hándicap en los derechos de las víctimas"; "Sin embargo, esto no es cierto"; "El número de víctimas que se ha acogido a la dispensa del deber de declarar ha sido ciertamente lineal, sin alteraciones desdeñables"; no período mais restritivo (2013-2016) a porcentagem "aumentó en un 2%". Dados: sobreseimentos livres e provisórios de 34,45% (2019) a 42,03% (2013) das denúncias; "aproximadamente el 70% de las denuncias... no han finalizado en una sentencia" (pdf p. 7). | ✅ (tese normativa pró-vítima; dados do CGPJ) |
| Villanueva, C. (2025), cap. "La dispensa de declarar de la mujer víctima de violencia de género", Nuevos retos del Derecho Probatorio, pp. 737-758. DOI 10.2307/jj.39224090.40 | Capítulo de livro, não lido. | 🚫 |

### 4.3 Retratação / desistência

| Autores, ano, periódico, DOI | Tese / número com trecho verbatim | Status |
|---|---|---|
| Cala, M. J.; Trigo, M. E.; Saavedra, F. J. (2016). "Renuncia de las mujeres al procedimiento judicial por violencia de género: variables sociodemográficas y psicológicas" / "Women's disengagement from legal proceedings for intimate partner violence". European Journal of Psychology Applied to Legal Context 8(1): 35-42. DOI 10.1016/j.ejpal.2015.10.002 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.1016/j.ejpal.2015.10.002]` | N = 345 mulheres em processo (Andaluzia): 214 (62%) seguiram até a sentença, 131 (38%) desistiram; "This last percentage is not at all representative" (amostra). Quatro fatores explicam 51% da variância: sentimento de culpa, contato com o agressor, expectativa de voltar com ele e existência de apoio psicológico. Cita 20,9% (Delegación del Gobierno, 2015) que não continuam e 12,4% que invocam o art. 416 (CGPJ 2013). | ✅ empírico; ⚠️ texto em inglês (resumo em espanhol) |
| García-Jiménez, M.; Barberá, E.; Trigo, M.; Cala, M. (2020). Psicothema 32(1): 40-46. DOI 10.7334/psicothema2019.188 | Segundo divulgação (Infocop), cerca de 20% das mulheres retiram a denúncia ou desistem; não li o artigo. | 🚫 (não lido; inglês) |
| Alegret, R. P.; García, A. C. (2022). "La retractación de denuncias penales en mujeres víctimas de violencia en la pareja". Argumentos (Córdoba, Argentina). DOI 10.5281/zenodo.7617910 | Só resumo (DOAJ). Revista argentina, fora do critério "Espanha". | 🚫 |
| Dialnet: Gudín Rodríguez-Magariños (2008, La ley penal 89-103), Martín Espinosa (2025, cap. livro 787-794), Bermúdez Requena (2013, cap. 629-646) | Dialnet devolveu 6 documentos para "retractación de la víctima violencia de género"; os três são comentário de sentença ou capítulos, jurídicos e não empíricos. Não lidos. | 🚫 |
| Macroencuesta de Violencia contra la Mujer 2024, cap. 9 (Delegación del Gobierno, não revisada por pares), Tabla 9.10, p. 8 (pdf 9) | Entre mulheres que denunciaram violência de ex-parceiros: "un 18,8% que sí la retiraron" (76,1% não); parceiro atual: 56,8% retiraram, com ressalva "la frecuencia muestral es pequeña". Motivos (Tabla 9.11, pdf 10, parceiros passados): "Es/era el padre de mis hijos/as" 31,8%, "Por miedo" 27,0%, "Sentía pena" 23,1%, "Pensó que podía cambiar" 21,2%. | ✅ dado oficial; fonte de pesquisa, não artigo |

### 4.4 Cifra negra (violência de gênero)

| Fonte | Número com trecho verbatim | Status |
|---|---|---|
| Macroencuesta 2024, cap. 9, Tabla 9.1 (p. 2, pdf 3) `[SOURCE: multilingual-term-expansion:es:igualdad.gob.es:macroencuesta2024-cap9]` | "El 16,8% de las mujeres que han sufrido VFSEM [violencia física, sexual, emocional o miedo] de alguna pareja actual o pasada ha denunciado... en la policía o en el juzgado": 5,2% (parceiro atual), 19,1% (parceiros passados); para violência física ou sexual: 26,3% (11,3% atual, 28,3% passados). Nota p. 1: "Este porcentaje no puede compararse directamente con el de la macroencuesta 2019"; comparação restrita aos últimos 12 meses: 21,1% (2024) vs 22,6% (2019), "p > 0,10", sem mudança significativa. Motivo mais citado para não denunciar: "Lo resolvió sola" 50,3% (Tabla 9.7). | ✅ |
| Macroencuesta 2019, "Principales resultados", p. 25 | Violência da parceria, "% de mujeres que han sufrido violencia de la pareja y han denunciado ... (la propia mujer u otra persona o institución)": 21,7% (física, sexual ou emocional) e 32,1% (física e/ou sexual); parceiro atual 5,4% / 12,5%, passados 25,0% / 34,3%. "3.118.723 mujeres no han denunciado ni acudido a servicios de ayuda formal." | ✅ |

### 4.5 Infradenúncia de crimes de ódio (literatura e pesquisas)

| Autores, ano, periódico, DOI | Tese / trecho verbatim | Status |
|---|---|---|
| Azabal, M.; Arruabarena, I. (2023). "Delitos e Incidentes de Odio Hacia Personas LGTBI+: Prevalencia, Consecuencias e Impacto". International E-Journal of Criminal Sciences 18. DOI 10.1387/inecs.25062 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.1387/inecs.25062]` | Revisão narrativa. PDF p. 5: "debido a la existencia de una cifra negra en torno a esta problemática resulta relevante y necesario hacer uso de un concepto más amplio que el de 'delito'". PDF p. 8: "en España, la razón principal por la que las víctimas optan por no denunciar se trata de la percepción de que el delito no es lo suficientemente grave (Jurčić et al., 2018)"; e fala de delitos "mal registrados o infraregistrados". Não traz taxa própria. | ✅ (revisão, sem taxa nova) |
| Albertín Carbó, P.; Langarita, J.; Mas Grau, J. (2022). "Delitos de odio anti-LGTBI+. Oportunidades, límites y desafíos en el sistema jurídico penal". Revista Española de Investigación Criminológica 20(2): 1-19. DOI 10.46381/reic.v20i2.701 `[SOURCE: multilingual-term-expansion:es:crossref:doi:10.46381/reic.v20i2.701]` | Qualitativo (entrevistas). PDF p. 3: "las denuncias de este tipo de acciones continúan siendo minoritarias" (277 denúncias de ódio por orientação sexual e identidade de gênero em 2020); razões para não denunciar: "la creencia de que nada sucederá con la denuncia, la desconfianza hacia las fuerzas y cuerpos de seguridad, el miedo a posibles represalias, el desconocimiento de la legislación, la vergüenza o el temor a que se descubra la orientación sexual". Limitação declarada (PDF p. 17): não aprofundou os motivos da não denúncia. | ✅ |
| Landa Gorostiza, J. (2024). "Delitos de odio en España". InDret 4: 133-182. DOI 10.31009/indret.2024.i4.05 | Texto integral bloqueado (HTTP 403); só resumo Crossref (diagnóstico multinível). | 🚫 |
| Castillo, M.; Hernández-Prados, M. (2023). "La infradenuncia de los delitos de odio en España", cap. de livro. DOI 10.2307/jj.5076324.4 | Capítulo de livro, não periódico; não lido. | 🚫 |
| Informe RAXEN / Movimiento contra la Intolerancia | Não consultado nesta célula. | 🚫 (beco) |

---

## Achados transversais

1. Dispensa e denúncia falsa medem coisas diferentes e não se somam: dispensa (cerca de 10-11% das mulheres vítimas) é decisão processual lícita (art. 416 LECrim); a FGE conta "deduções de testemunho por denúncia falsa" (6 em 2025). A literatura (Cala 2016; Macroencuesta 2024) liga retratação a culpa, medo, filhos e dependência, não a falsidade.
2. Para citar "denúncias falsas": usar a tabela da Memoria 2026 (p. 612-613) e dizer "causas acompanhadas" (numerador) e "total de denúncias do CGPJ" (denominador). Não escrever "0,0069%".
3. Para citar a dispensa: usar a planilha de séries anuais 2025 e o informe anual 2025 (p. 7, 37); não misturar com os "10 indicadores".
4. Para ódio por orientação sexual e identidade de gênero: 528 (2024), 571 (2025, só nota de imprensa); a taxa de denúncia é 6,8% na pesquisa ONDOD e 14% na FRA; as duas são autosseleção online. Registros policiais (SEC) subestimam por construção.

## PRISMA-S

| Termo (ES) | Base | Linhas inspecionadas (`total-results` da base não informativo) | Selecionados |
|---|---|---|---|
| denuncias falsas violencia de género mito o realidad | Crossref | 12 | 1 (Pérez Fernández 2012) |
| dispensa de la obligación de declarar artículo 416 LECrim víctima violencia de género | Crossref | 10 | 1 candidato lido (Beltrán) + 1 capítulo (Villanueva) |
| víctimas violencia de género acogen dispensa declarar testigo 416 LECrim reforma | Crossref | 10 | 1 (De la Herrán) |
| retractación de la víctima violencia de género; mujeres que retiran la denuncia...; retractación víctimas... factores psicológicos | Crossref | 10 + 8 + 8 | 0 |
| retirada de la denuncia violencia de género motivos mujeres | web (WebSearch) | 9 | 2 (Cala 2016; García-Jiménez 2020) + 1 fora do critério (Alegret 2022) |
| retractación de la víctima violencia de género | Dialnet | 6 documentos | 0 lidos (3 listados no ledger) |
| dispensa..., denuncias falsas..., infradenuncia delitos de odio | Dialnet | 0 parseados (consultas intermitentes) | 0 |
| cifra negra violencia de género denuncia macroencuesta; Macroencuesta 2019/2024 denuncia | Crossref / web | 10 / 8 / 9 | 2 (Macroencuesta 2019, 2024) |
| infradenuncia delitos de odio España víctimas; delitos de odio LGTBI infradenuncia | Crossref | 10 + 8 | 3 (Azabal, Albertín, Landa só resumo) + 1 capítulo |
| FRA LGBTIQ survey III Spain reporting | web | 10 | 1 |
| denuncias falsas / dispensa / retractación | SciELO | bloqueado (HTTP 403) | 0 |
| Redalyc | Redalyc | não consultado diretamente | 0 |
| OpenAlex | n/a | não usado (cota esgotada, instrução) | 0 |

## Becos

- PDF do Informe Interior 2025: não localizado (Cloudflare 403 em nomes adivinhados; a listagem pública de publicações para em 2023 e na encuesta ONDOD 2024). Só há nota de imprensa.
- PDF Interior 2024 não está em disco; lido no Chrome real com pdf.js. O ledger guarda o sha256 da transcrição. Cópia do Wayback truncada em 5 MiB (arquivo renomeado `...TRUNCADO-5MiB-inutilizavel.pdf`).
- Um servidor local para receber o PDF do Chrome nunca recebeu o POST (travou); descartado.
- CGPJ 2T2026 e 3T2026: ainda não publicados na data da coleta.
- SciELO: HTTP 403. Dialnet: respondeu a uma consulta, 0 resultados parseados nas demais. Redalyc: não consultado.
- Landa (InDret) e Castillo e Hernández-Prados: sem texto integral.
- Não resolvido: por que o ratio dos "10 indicadores" difere do informe anual; por que as vítimas saltam 17,5% em 2017.
- Informe RAXEN / Movimiento contra la Intolerancia: não consultado.
