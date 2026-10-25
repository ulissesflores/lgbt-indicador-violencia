# Briefing C — F8: orientação ideológica do governo e violência contra mulheres, negros e pessoas LGBT

Data: 2026-10-11 · Playbook: paper-deep-dive · Ledger: `research-2026-10-11/sources.jsonl` (arquivo compartilhado com os briefings A, B, D, E, que usam a mesma `origem`; as 51 fontes deste briefing são os ids listados no Apêndice, emitidas entre 17:53Z e 18:07Z)
PDFs e dados baixados: `fontes/p2-f8-governos/`

> [!IMPORTANT]
> Regra de status usada: ✅ = número conferido por mim no texto/abstract/PDF da fonte primária; ⚠️ = número vindo de fonte secundária, de preprint/nota não revisada, ou só o desenho foi conferido; 🚫 = não confirmado ou descartado. "Peer-reviewed" só quando há periódico confirmado por Crossref.

## 0. Cinco achados decisivos

1. Não existe estudo revisado por pares com desenho causal ligando ideologia do governo federal ou estadual a violência contra LGBT, negros ou mulheres no Brasil. A única tentativa achada com governador como variável (Silva 2025, UF x ano, escala Power-Zucco) é trabalho de GT de mestrando, versão preliminar, desfecho letalidade policial; o abstract diz "no influence", mas o corpo traz coeficientes positivos e significativos em alguns modelos (resultado instável, não é nulo limpo).
2. A série de feminicídios do Anuário FBSP sobe quase monotonicamente 2016-2025 (929 -> 1.571), atravessando Temer, Bolsonaro e Lula; mas é série de registro (Lei 13.104/2015, Lei 14.994/2024) e não separa incidência de classificação.
3. A queda de homicídios pós-2017 tem explicação consistente com trégua entre facções + demografia (FBSP, Feltran et al. 2022), começou antes de 2019, e o Atlas 2025 mostra que parte da queda registrada é degradação de dados (diferença estimado x registrado foi de 1,8 para 2,6 por 100 mil). Isso enfraquece tanto "Bolsonaro reduziu homicídios" quanto "os decretos não aumentaram".
4. Decretos de armas 2019: a estimativa quantitativa existente (elasticidade 1,1; 6.379 vidas) é nota técnica do FBSP, não periódico; os artigos revisados achados não avaliam os decretos (Santos 2024 é descritivo; Baculi et al. 2021 usa dados até 2016; Eleuterio-da-Rocha 2026, que dá nulo, só tive o título).
5. No exterior, eventos políticos discretos mexem nas contagens de crime de ódio e o efeito costuma ser curto (Devine: +19-23% pós-Brexit, sem aumento longo), mas o maior número do "efeito Trump" (+226% em condados com comício) foi contestado e a versão publicada não repete o número. Efeito de registro está documentado nos dois sentidos (Levy & Levy; Marinho Neto et al. para o Sinan).

## 1. Alvo 1 — "Trump effect" e crime de ódio (EUA)

| Fonte | Periódico, DOI | Desenho e dados | Efeito e citação verbatim | Status |
|---|---|---|---|---|
| Müller & Schwarz (2023), From Hashtag to Hate Crime | AEJ: Applied Economics 15(3):270-312. 10.1257/app.20210211 | IV (adotantes iniciais do Twitter no SXSW 2007) + event study, condados, FBI | Abstract: "higher Twitter use in a county is associated with a sizeable increase in anti-Muslim hate crimes after the 2016 presidential primaries". Número "1 DP de uso de Twitter -> +7% de crimes antimuçulmanos por ano": só no destaque da AEA (https://www.aeaweb.org/research/charts/twitter-antiminority-sentiment-trump), não li o PDF | ⚠️ número; ✅ existência e desenho. |
| Müller & Schwarz (2021), Fanning the Flames of Hate | JEEA 19(4):2131-2167. 10.1093/jeea/jvaa045 | Alemanha, sentimento antirrefugiado no Facebook + quedas de Facebook/internet como variação exógena | "antirefugee sentiment on Facebook predicts crimes against refugees in otherwise similar municipalities with higher social media usage" | ✅ abstract. Mede mídia social, não ideologia de governo |
| Edwards & Rushin (2018), The Effect of President Trump's Election on Hate Crimes | SSRN 3102652 (10.2139/ssrn.3102652); sem periódico confirmado | Série temporal e painel, UCR 1992-2017 | Não consegui o texto (SSRN 403). Resumo secundário: aumento significativo após a eleição, maior em condados de maior margem pró-Trump | ⚠️ desenho/direção só por secundária; 🚫 número "2.048 crimes adicionais" (Christian Post, nunca conferido, não citar) |
| Feinberg, Branton & Martinez-Ebers (2022), The Trump Effect | PS: Political Science & Politics 55(2):257-265. 10.1017/s1049096521001621 | Condados que sediaram comícios 2016 x demais; incidentes de ódio (SPLC/ADL) | Abstract: "a limited size but significant rise in the likelihood of reported hate and bias incidents". O "226%" é do preprint de 2019, não está no abstract publicado | ✅ abstract publicado; 🚫 "226%" como achado da versão revista |
| Lilley & Wheaton (2019), Trump Rallies and Hate Crimes: A Comment | nota no GitHub, não revisada por pares | Réplica com os mesmos dados, controla população, repete para comícios de Clinton | Abstract: "After correcting their analysis for various problems, we find no effect of rallies on hate incidents." Texto: Clinton aplicada à mesma metodologia dá efeito "as large as the supposed Trump effect, if not larger" | ✅ (PDF lido). Resposta dos autores originais (Fox News, 10/09/2019): análise com população ainda mostra aumento, citado 118%, não publicado: ⚠️. Não achei correção formal nem resposta publicada no periódico |
| Newman et al. (2021), The Trump Effect | BJPS 51(3):1138-1159 (online 2020-02). 10.1017/s0007123419000590 | Experimento de survey em painel online | "the prejudiced are emboldened to both express and act upon their prejudices" (quando a fala não é condenada por outras elites) | ✅ abstract. Correção do alvo: ano de impressão 2021 ok; **não mede crime de ódio**, mede expressão de preconceito em experimento |
| Dugan & Chenoweth (2020), Threat, emboldenment, or both? | Criminology 58(4):714-746. 10.1111/1745-9125.12259 | VAR, atos do governo federal dos EUA x crimes de ódio violentos (FBI) 1992-2012 | "vector autoregression models provide support for both hypotheses, depending on the protected group involved" (ameaça política -> afro-americanos; emboldenment -> latinos) | ✅ abstract. É o teste mais simétrico da frente: atenção positiva OU negativa do governo pode aumentar violência |
| Souza et al. (2022), Political Parties and Hate Crimes | Int. J. Economics and Finance 14(11):46. 10.5539/ijef.v14n11p46 | Painel 47 estados, 1997-2019 | "a Democratic president is correlated with fewer crimes of hate if compared with a Republican"; governadores democratas positivamente correlacionados, "only true for Southern states" | ✅ abstract; correlacional, periódico de baixo prestígio: só como modelo de desenho |
| Brightman, Lenning, Lurie & DeJong (2024), Anti-Transgender Ideology, Laws, and Homicide: The Trifecta of Violence | Homicide Studies 28(3). 10.1177/10887679231201803 | EUA 2015-2022, correlação entre retórica, leis estaduais antitrans e homicídios de pessoas trans | Resumo (secundário): os três componentes subiram no período e se correlacionam; sem efeito causal | ⚠️ abstract só por secundária; correlacional; única fonte achada sobre legislação antitrans x violência |
| Mills, Lantz & Wenger (2024) | Criminology 62. 10.1111/1745-9125.12378 | Multinível, adesão de agências ao reporte UCR | "a particular tendency toward ceremonious compliance in Republican-leaning locales" (reportam zero) | ✅ abstract. Registro: locais republicanos reportam zero com mais frequência |

Literatura nula/contrária: Lilley & Wheaton (acima); Dugan & Chenoweth (direção depende do grupo). Lacuna: nenhum estudo achado isola crimes contra orientação sexual no "efeito Trump".

## 2. Alvo 2 — Europa

| Fonte | Periódico, DOI | Desenho | Efeito (citação) | Status |
|---|---|---|---|---|
| Devine (2021), Discrete Events and Hate Crimes: Brexit | Social Science Quarterly 102(1):374-386. 10.1111/ssqu.12896 | Modelos de intervenção em séries diárias/mensais, Home Office + polícias, controla atentados | "The Brexit referendum led to a 19-23 percent increase in hate crimes, but did not lead to a longer-term increase" | ✅ (confirma a hipótese de memória "Devine 2021") |
| Williams et al. (2022), Brexit vote and RR hate crimes | Br. J. Criminology. 10.1093/bjc/azac071 | Painel nacional + dados de rede social para controlar variação de reporte | Abstract lista 5 contribuições; não traz número | ⚠️ número não conferido; desenho ✅ |
| Jäckle & König (2018), Threatening events and anti-refugee violence | European Sociological Review. 10.1093/esr/jcy038 | Alemanha 2015-16, eventos + falas de partidos anti-imigração | "such negative public cueing indeed boosts the probability of attacks", mas falas "prompted in part by preceding threatening events" | ✅ abstract; sobre AfD só indireto (partidos anti-imigração) |
| Frey (2020), 'Cologne Changed Everything' | ESR. 10.1093/esr/jcaa007 | Série diária de ataques a refugiados | Ano Novo de Colônia -> "dramatic surge in the daily rate of violence", maior em distritos com baixo apoio prévio à extrema-direita | ✅ abstract |
| Entorf & Lange (2023), Refugees welcome? | Regional Science & Urban Economics 101:103913. 10.1016/j.regsciurbeco.2023.103913 | Atribuição quase-experimental de requerentes de asilo | Homogeneidade étnica, crimes de ódio nos anos 1990 e apoio nazista em Weimar predizem resposta (resumo secundário) | ⚠️ conferido só por resumo de terceiros |
| Romarri (2019), Far-right mayors and hate crime, Itália | SSRN 3506811, sem periódico confirmado | Eleições municipais 2008-2018 com margem estreita | "from 4.3 to 5.3 percentage points" (resumo de seminário, Bocconi CLEAN). Dado: ONG Lunaria (não há base oficial) | ⚠️ preprint; desenho de eleição apertada é o mais próximo de "governo de direita -> crime de ódio" |
| Rees et al. (2019), Climate of Hate | Frontiers in Psychology. 10.3389/fpsyg.2019.02328 | Municípios alemães, voto AfD 2017 x crimes de ódio contra refugiados | Mesmas variáveis socioestruturais correlacionam com ambos; correlacional | ✅ abstract |
| Dancygier (2023), Hate crime supporters | PNAS. 10.1073/pnas.2212757120 | Surveys e experimento de candidatos, Alemanha | "a significant number of citizens empower potential perpetrators from the bottom-up" | ✅ abstract; opinião, não incidência |
| Dancygier, Egami & Jamal (2021), Hate crimes and gender imbalances | AJPS. 10.1111/ajps.12595 | Atribuição de refugiados | abstract não conferido | ⚠️ só desenho |
| Benier et al. (2025), PROTOCOL: correlates and antecedents of hate crime | Campbell Systematic Reviews. 10.1002/cl2.70048 | Protocolo de revisão sistemática | Sem resultados | ✅ prova de que **não há meta-análise concluída** achada; 🚫 meta-análise/revisão sobre partidos de direita e crime de ódio |

Suécia: 🚫 não confirmado. Nenhuma fonte revisada por pares achada em busca por OpenAlex/Crossref.

## 3. Alvo 3 — Brasil nacional

### 3a. Decretos de armas de 2019

| Fonte | Tipo | Desenho | Número e citação | Status |
|---|---|---|---|---|
| Cerqueira, Lins, Kahn & Bueno (FBSP, 2022), Armas de fogo e homicídios no Brasil | Nota técnica FBSP, literatura cinzenta | Painel de UFs 2008-2021, variável instrumental, proxy de difusão = proporção de suicídios com arma de fogo | "a cada 1% a mais na difusão de armas há aumento de 1,1% na taxa de homicídio" (Sumário, p. 6); "6.379 vidas teriam sido poupadas" sem o aumento de armas (p. 4 e p. 7); "crescimento de 476,6% nos registros ativos de CACs entre 2018 e 2022" (p. 4) | ✅ número na fonte; ⚠️ não revisada por pares; identificação (proxy + IV) é discutível; o estoque pós-2019 é estimado |
| Santos (2024), Legal and illegal firearms markets | J. Illicit Economies & Development 6(1):16-29. 10.31389/jied.247 | Descritivo: 29 normas, 962.782 armas de CACs (5/2019-2022), apreensões SP e RJ | Apreensões de fuzis +50% em SP e +16% no RJ, 2017-2022 (paráfrase do resumo da página); o artigo não mede taxa de homicídio | ✅ conferido via página do periódico; não é avaliação causal |
| Baculi et al. (2021), Uma nota sobre homicídios e a entrada de armas legais nas regiões brasileiras | Revista Brasileira de Economia 75(1). 10.5935/0034-7140.20210001 | Painel FE + System-GMM, 27 UFs, 2008-2016 | "o aumento de 1% em novos registros de pessoas físicas aumentou em 0,10% o número de óbitos para cada 100 mil habitantes"; no Sul "o aumento de arma legal não representou um aumento de homicídios" | ✅ (resumo e Tabela 3 via SciELO); período **anterior** aos decretos |
| Eleuterio-da-Rocha et al. (2026), Legal gun ownership and carrying are not associated with homicides in Brazil: a Bayesian analysis | Int. J. Comparative & Applied Criminal Justice. 10.1080/01924036.2026.2731244 | Bayesiano (detalhe não lido) | Só título; resumo inacessível (403) | ⚠️ título; 🚫 qualquer número. Único achado "nulo" sobre armas legais: ler antes de citar |
| Atlas da Violência 2026, Anuário FBSP e Atlas 2025 | Oficial FBSP/Ipea | Texto sobre mudanças regulatórias 2019-2022 | Atlas 2026: "A ampliação do mercado legal contribuiu para o aumento do desvio de armamentos para o mercado ilegal" | ✅ (fontes locais lidas); narrativa, não estimativa |

Busca específica por avaliação com DiD/controle sintético dos decretos em Ciência & Saúde Coletiva, Cad. Saúde Pública e Rev. Saúde Pública: **nada achado** (🚫). Não confirmei "Cerqueira & Mello 2013" nem "Schneider 2019" como periódicos: aparecem só como citados pela nota do FBSP.

### 3b. Queda de homicídios 2018-2019

| Fonte | Tipo | Conteúdo | Status |
|---|---|---|---|
| FBSP (2022) Sumário Executivo, p. 4 | Cinzenta | MVI recorde em 2017 (64.078; 30,9/100 mil); queda em 2018 e 2019, alta em 2020, recuo em 2021 (22,3). Três hipóteses: demografia (shift-share: 23% da queda 2004-2020), políticas estaduais, "armistício" PCC-CV desde 2018, com quedas maiores em AC, RR, PA, CE, PE, RN | ✅ |
| Feltran et al. (2022), Variações nas taxas de homicídios no Brasil | Dilemas 15(spe4). 10.4322/dilemas.v15esp4.52509 | Comparação etnográfica em 4 capitais + decomposição por perfil; queda em Porto Alegre com o fim da guerra BNC x Antibala em 2018; São Luís de ~90 para 29,4/100 mil (2014-2019) (paráfrase do texto em inglês da página, não verbatim) | ✅ via SciELO; revisado por pares |
| Atlas da Violência 2025, cap. 3 (PDF p. 18) | Oficial | "parcela da queda dos homicídios registrados a partir de 2018 pode ser creditada a uma piora na qualidade dos dados". Diferença média entre taxa estimada e registrada: 1,8 (2013-17) -> 2,6 por 100 mil (2018-23); 51.608 homicídios ocultos 2013-2023 | ✅ (PDF local `fontes/t1-atlas-2025/atlas2025.pdf`) |

Descartado: resumo de WebSearch que citava "Population Health Metrics" sobre a campanha de desarmamento: não achei o artigo; 🚫.

### 3c. "Efeito Bolsonaro" sobre violência contra LGBT ou negros

| Fonte | Periódico, DOI | Desenho | Resultado | Status |
|---|---|---|---|---|
| Marinho Neto et al. (2024), Tendência temporal... violência na população trans, 2015-2022 | Epidemiol. Serv. Saúde 33. 10.1590/s2237-96222024v33e2024296.especial.en | Painel repetido de notificações Sinan, Prais-Winsten | Notificações trans caíram (β = -0,07; p = 0,010), mas houve +45,8% de municípios notificantes; "Notification of violence does not yet fully reflect the reality of this population" | ✅ abstract. Mostra que expansão da cobertura de notificação contamina a tendência |
| Rios et al. (2025), Notificações de violência contra travestis e transexuais, 2015-2022 | Epidemiol. Serv. Saúde 34. 10.1590/s2237-96222025v34e20240350.en | Série temporal descritiva Sinan | 37.104 notificações; aumento +182,0% entre travestis | ✅ abstract; sem comparação entre governos |
| Pinto et al. (2020), Perfil das notificações... LGBT 2015-2017 | Rev. Bras. Epidemiol 23. 10.1590/1980-549720200006.supl.1 | Descritivo Sinan | **24.564** notificações | ✅ abstract (um resumo automático de busca trouxe "778.527", que está errado) |
| Vasconcelos et al. (2023) PNS 2019 | já no dossiê de 10/10 | Autorrelato, corte transversal | ver DOSSIE-2026-10-10.md | fora desta frente |

Resultado da busca por desenho causal sobre Bolsonaro e violência contra LGBT/negros (DiD, event study, controle sintético): **nenhum estudo revisado por pares achado** (🚫). O que existe é contagem jornalística de incidentes de campanha em 2018 (sem grupo de comparação).

### 3d. Feminicídio 2015-2025

Fonte: Anuário Brasileiro de Segurança Pública 2026, Gráfico 35, p. 159 (dados das secretarias estaduais). ✅ lido no PDF `fontes/t2-anuario-2026-dados2025/anuario-2026.pdf`.

| Ano | Homicídios de mulheres (incl. feminicídio) | Feminicídios | Governo federal |
|---|---|---|---|
| 2016 | 4.245 | 929 | Dilma (até 31/08) / Temer |
| 2017 | 4.556 | 1.075 | Temer |
| 2018 | 4.340 | 1.229 | Temer |
| 2019 | 3.966 | 1.330 | Bolsonaro |
| 2020 | 3.999 | 1.354 | Bolsonaro |
| 2021 | 3.869 | 1.347 | Bolsonaro |
| 2022 | 3.934 | 1.455 | Bolsonaro |
| 2023 | 3.937 | 1.475 | Lula |
| 2024 | 3.728 | 1.504 | Lula |
| 2025 | 3.539 | 1.571 | Lula |

Leitura: feminicídios subiram em todos os governos (queda só em 2021, -0,5%); homicídios de mulheres em geral caíram. 2025: 44,4% dos homicídios de mulheres classificados como feminicídio, "o maior percentual desde 2015" (Anuário 2026, p. 159-160). Mudanças de registro que impedem ler a série como incidência: Lei 13.104/2015 (tipificação) e Lei 14.994/2024 (feminicídio autônomo, 2025 é o primeiro ano completo) – nota (1) da Tabela 21. COVID: Nascimento et al. (2025, BMC Public Health, 10.1186/s12889-025-24814-6), ITS 2017-2022, 23.727 homicídios femininos, taxa ajustada 5,09/100 mil (+16,0% após correção de subnotificação/causa indeterminada); efeito regional (Nordeste RR = 1,236, p = 0,002) ✅ abstract; não estima efeito de governo.

## 4. Alvo 4 — ideologia de partido/governador (Brasil)

### 4a. Tabelas de escore (lado a lado; escalas diferentes)

> [!WARNING]
> As duas medidas **discordam na cauda direita**. Bolognesi et al. (survey com associados da ABCP, 20 dias de jul/2018, N de 431 a 514 respondentes por partido, escala 0-10) põe o DEM no extremo (8,57) e Patriota (8,55), com o PSL em 8,11 (empatado com o DC). Zucco & Power (legisladores, onda BLS9 de 2021, escala contínua estimada, aprox. -1 a +1) põe PSL (+0,80) e Novo (+0,71) à frente, com o DEM em +0,43. Codifique governadores com **uma** escala e rode a outra como robustez. União Brasil (DEM+PSL, 2022) não está em nenhuma; Zucco & Power imputam +0,66 para 2023 (média ponderada, Apêndice A).

| Partido | Bolognesi, Ribeiro & Codato (2018; Dados 66(2), Tab. 1): média 0-10 | Zucco & Power BLS9 (2021; Apêndice Tab. C1): estimativa (EP) |
|---|---|---|
| PSOL | 1,28 | -0,874 (0,045) |
| PCdoB | 1,92 | -0,822 (0,101) |
| PT | 2,97 | -0,691 (0,042) |
| PSB | 4,05 | -0,427 (0,038) |
| PDT | 3,92 | -0,356 (0,038) |
| MDB | 7,01 | +0,137 (0,037) |
| PSDB | 7,11 | +0,157 (0,037) |
| PSD | 7,09 | +0,296 (0,037) |
| Podemos | 7,24 | +0,386 (0,039) |
| DEM | 8,57 | +0,431 (0,038) |
| PTB | 6,10 | +0,455 (0,039) |
| PL (era PR até 2019) | 7,78 (como PR) | +0,493 (0,039) |
| PP (Progressistas) | 8,20 | +0,510 (0,040) |
| Republicanos (era PRB) | 7,78 (como PRB) | +0,550 (0,040) |
| Novo | 8,13 | +0,711 (0,041) |
| PSL | 8,11 | +0,803 (0,043) |
| União Brasil | ausente | ausente (imputado +0,66 em 2023) |

✅ Ambas as tabelas conferidas nos arquivos: `fontes/p2-f8-governos/bolognesi-2023-dados.pdf` (Tab. 1, p. 6-7) e `fontes/p2-f8-governos/zucco-power-dataverse/appendix.pdf` + `bls9_estimates_partiespresidents_long.tab` (Harvard Dataverse 10.7910/DVN/6KVTUV, CC0). Estimativas BLS9 aparecem nas ondas 1990-2021; presidentes (Tab. C2): Lula -0,50 (2017), Bolsonaro +0,87 (2021). Observação sobre citação: o ledger traz o Bolognesi com ano 2022 (versão OpenAlex), mas o número é Dados 66(2), 2023, e o DOI codifica 2023; o survey é de 2018, anterior à eleição de Bolsonaro, logo não captura a realocação posterior do PL e do Republicanos.

Observação de método: os dois são classificação de **partido**, não de governador; governador-ano exige juntar com TSE e lidar com troca de partido (Silva 2025 usa Power-Zucco e cai para Tarouco & Madeira / Bolognesi quando falta).

### 4b. Artigos com ideologia/partido de governante em painel (modelos de desenho)

| Fonte | Periódico/venue | Desenho | Resultado | Status |
|---|---|---|---|---|
| Silva (2025), gubernatorial ideology and police punitiveness | Trabalho de GT 12 (mestrando UnB), DOI 10.29327/9786527217374.1205487; PDF `fontes/p2-f8-governos/silva-2025-gubernatorial-ideology-police.pdf` | UFs 2011-2024, Pooled OLS e primeiras diferenças, escala 1-10 Power-Zucco e dummy direita (>5,5) | Abstract: "Preliminary results suggest that governors' ideological positions have no influence on police punitiveness rates". O corpo contradiz em parte: Tabela 7 (mortes de cidadãos em operações da Polícia Civil, variação %) ideologia +1,5456, p=0,000; Tabela 11 (mortes de PMs em serviço) dummy direita +619,65, p=0,040; outros modelos p>0,2 (ex.: ideologia 40,67, p=0,420) | ✅ lido; ⚠️ não revisado por pares; resultados instáveis entre especificações, R² baixo; serve de modelo de desenho, não de evidência |
| Gouvêa & Girardi (2021), Partisanship and local fiscal policy | J. Development Economics. 10.1016/j.jdeveco.2021.102637 | RDD, prefeitos de esquerda x outros, 2004-2016 | "no effect of left-wing mayors on the size of the city government"; "approximately 0.6 percentage points on the social expenditures share" | ✅ abstract (via KCL); modelo de RDD municipal |
| Bennouna et al. (2021), Pandemic policymaking in presidential federations | Publius 51(4):570. 10.1093/publius/pjab025 | UFs do Brasil, México, EUA | Variação de rigor das políticas explicada por "political factors"; Brasil sem coordenação | ✅ abstract; modelo de painel de UFs com partido/governador |
| Carreras & Visconti (2022) | Electoral Studies. 10.1016/j.electstud.2022.102522 | DiD no Chile e México | Governos de direita nem sempre punidos por crime | só citado; fora do alvo causal (não registrado no ledger) |

## 5. Alvo 5 — métodos (DiD escalonado e event study)

| Referência | Periódico, DOI | Para quê | Status |
|---|---|---|---|
| Callaway & Sant'Anna (2021) | J. Econometrics 225(2). 10.1016/j.jeconom.2020.12.001 | ATT(g,t) com tratamento escalonado, controles nunca/ainda não tratados | ✅ Crossref |
| Goodman-Bacon (2021) | J. Econometrics 225(2). 10.1016/j.jeconom.2021.03.014 | Decomposição do TWFE; mostra o viés de comparações com já tratados | ✅ Crossref |
| Sun & Abraham (2021) | J. Econometrics. 10.1016/j.jeconom.2020.09.006 | Event study com efeitos heterogêneos | ✅ Crossref |
| de Chaisemartin & D'Haultfoeuille (2020) | AER. 10.1257/aer.20181169 | TWFE com efeitos heterogêneos | ✅ Crossref |
| Borusyak, Jaravel & Spiess (2024) | Review of Economic Studies. 10.1093/restud/rdae007 | Estimador de imputação para event study | ✅ Crossref |
| Roth, Sant'Anna, Bilinski & Poe (2023) | J. Econometrics. 10.1016/j.jeconom.2023.03.008 | Síntese da literatura de DiD | ✅ Crossref |
| Rambachan & Roth (2023) | Review of Economic Studies. 10.1093/restud/rdad018 | Sensibilidade a violações de tendências paralelas | ✅ Crossref |

Aplicação a esta frente: tratamento = troca de partido do governador (entrada/saída de esquerda/direita), simétrico; confundidores com datas fixas (decretos 2019, COVID 2020-21, mudança de registro) entram como choques comuns por ano (efeito fixo de ano) e como testes de placebo; a mudança de registro (Lei 14.994/2024; ficha Sinan; cobertura municipal) precisa de desfecho alternativo menos sensível a registro (óbito do SIM, não BO).

## 6. Alvo 6 — registro x incidência

| Fonte | Periódico, DOI | Como separa (ou não) | Citação | Status |
|---|---|---|---|---|
| Levy & Levy (2017), When love meets hate | Social Science Research 61:142-159. 10.1016/j.ssresearch.2016.06.008 | Painel de estados 2000-2012; reconhecimento de parcerias x leis de crime de ódio e de emprego | Leis de crime de ódio e antidiscriminação no emprego com orientação sexual associadas a menos crimes; reconhecimento de parcerias "increases reported hate crimes, though it may not increase actual crime incidence" | ⚠️ conferido só por resumo de busca (WebSearch), PDF e abstract oficial não lidos; a frase entre aspas é paráfrase do resultado, não verbatim; desenho de separação explícito |
| Pettis, Valencia & Williams (2022), Pride and Prejudice | J. Law & Economics 65(4):811. 10.1086/721700 | DiD escalonado com event study; anúncios de legalização do casamento | "reduces the anti-LGBT hate crime rate by .112 per 100,000 people, although some additional analyses have weaker results"; efeito "fade after 1 year" | ✅ abstract |
| McVeigh, Welch & Bjarnason (2003) | American Sociological Review 68(6). 10.1177/000312240306800603 | Cada crime reportado como "resultado de mobilização": organizações de direitos civis elevam o número reportado | "The presence of resourceful civil rights organizations in a county can lead to higher numbers of reported hate crimes" | ✅ abstract |
| Mills, Lantz & Wenger (2024) | ver §1 | Locais republicanos com conformidade "cerimonial" (zero reportado) | ver §1 | ✅ |
| Kondakov (2019/2021) | European J. Criminology. 10.1177/1477370819887511 | Usa decisões judiciais, não estatística policial, para estimar vitimização antes e depois da lei de 2013 | abstract só parcial | ⚠️ |
| Marinho Neto et al. (2024) | ver §3c | Cobertura de municípios notificantes cresceu 45,8% | "does not yet fully reflect the reality" | ✅ |
| Müller & Schwarz (2021) JEEA | ver §1 | Quedas de internet como variação exógena de **incidência** | ver §1 | ✅ |
| Devine (2021) | ver §2 | Testa se cobertura de mídia/saliência explica; controla ataques terroristas | "no evidence of a relationship between media coverage of hate crime or immigration salience and hate crimes" | ✅ |
| Pezzella, Fetzer & Keller (2019), The dark figure of hate crime underreporting | Am. Behavioral Scientist. 10.1177/0002764218823844 | Subnotificação | abstract não conferido | ⚠️ |

## 7. O que a literatura permite e não permite afirmar sobre direita x violência no Brasil

**Permite afirmar (com a fonte ao lado)**
- Eventos políticos discretos (eleição, referendo, comício, fala de líder, ataque terrorista) coincidem com aumento de contagens de crime de ódio no exterior, em geral de curta duração: Devine (2021) para o Brexit; Jäckle & König (2018) e Frey (2020) para a Alemanha; Müller & Schwarz (2021, 2023) para mídia social como canal. A direção não é só "direita": Dugan & Chenoweth (2020) mostram ameaça política (atenção positiva ao grupo) e emboldenment (atenção negativa) com efeitos conforme o grupo.
- Anúncios de legalização do casamento entre pessoas do mesmo sexo reduziram a taxa de crimes de ódio anti-LGBT em DiD escalonado nos EUA, por cerca de um ano (Pettis et al. 2022, ✅ abstract); Levy & Levy (2017) corrobora para leis de crime de ódio e de emprego, e sugere que o reconhecimento de parcerias aumenta o **registro** (⚠️, só por resumo de busca). Ou seja, "esquerda/reconhecimento -> mais registro" e "direita/evento hostil -> mais incidência" coexistem nos dados, e o teste simétrico precisa separar os dois.
- No Brasil, feminicídio registrado cresceu em todos os governos entre 2016 e 2025 (Anuário FBSP 2026, Gráfico 35), e a queda de homicídios depois de 2017 é compatível com trégua entre facções e demografia, e começou antes do governo Bolsonaro (FBSP 2022; Feltran et al. 2022).
- A taxa de homicídios registrada pós-2018 está parcialmente contaminada por piora de qualidade (Atlas 2025).
- Há duas escalas de ideologia partidária com estimativas por partido (Bolognesi et al. 2023; Zucco & Power 2024), aptas a codificar o partido do governador, com divergência conhecida na cauda direita.

**Não permite afirmar**
- Que a orientação do governo federal ou estadual **causou** mais ou menos violência contra mulheres, negros ou LGBT no Brasil: nenhum estudo revisado por pares com desenho causal foi achado. O único painel de UFs com ideologia de governador (Silva 2025) é preliminar, trata de letalidade policial e tem abstract "sem influência" mas coeficientes significativos em alguns modelos do corpo, com resultados instáveis entre especificações.
- Que os decretos de armas de 2019 aumentaram homicídios ou feminicídios: a estimativa existente (elasticidade 1,1; 6.379 vidas) é nota técnica do FBSP com proxy e instrumentos discutíveis, sem revisão por pares; os artigos revisados achados não avaliam os decretos.
- Que os decretos **não** aumentaram: a única fonte "nula" (Eleuterio-da-Rocha 2026) só tive o título.
- Que a queda de homicídios 2018-2019 seja mérito ou demérito de um governo: causas conhecidas são anteriores ou externas (trégua, demografia) e o dado registrado piorou em qualidade.
- Que o "efeito Trump" tenha magnitude de 226%: o número saiu do preprint de 2019; a versão publicada fala em "limited size", e há réplica sem efeito após controlar população. Edwards & Rushin não têm número conferido.
- Que tendências de notificação (Sinan) ou de BO sejam tendências de incidência: a cobertura municipal e as mudanças legais mudam o registro (Marinho Neto 2024; Lei 14.994/2024).
- Qualquer afirmação sobre a Suécia ou sobre meta-análise: nada confirmado; só o protocolo da Campbell (2025).

## Becos

- Edwards & Rushin 2018: SSRN 403; sem número; sem periódico. Volta se achar PDF aberto (CORE, ICPSR).
- Eleuterio-da-Rocha 2026 (Taylor & Francis 403) e CrimRxiv 403: resumo não lido. Volta se achar versão do preprint.
- Cambridge (Zucco & Power, artigo) bloqueia curl com 429; contornado pela replicação no Harvard Dataverse (CC0).
- OpenAlex deu 429 depois de ~60 chamadas (rate limit compartilhado entre agentes); troquei por Crossref + Europe PMC.
- Resumos automáticos da WebSearch erraram detalhes (ex.: "778.527 notificações" para Pinto et al., corrigido para 24.564 pelo abstract). Tratei toda afirmação de WebSearch como pista e só registrei o que li na fonte.
- Scimago não consultado (regra); quartil dos periódicos fica para o dossiê.
- Sem artigos de periódico para Suécia, para "decreto de armas x feminicídio" e para "efeito Bolsonaro" em violência contra LGBT/negros.
- Cerqueira & Mello 2013, Hartung 2009, Justus 2012, Schneider 2019, Cerqueira 2014: citados pela nota do FBSP, não confirmados em Crossref/OpenAlex como periódico.

## Apêndice — ids registrados no ledger por este briefing (51)

DOIs (44): 10.1257/app.20210211, 10.1093/jeea/jvaa045, 10.1017/s1049096521001621, 10.1017/s0007123419000590, 10.2139/ssrn.3102652, 10.1111/ssqu.12896, 10.1093/esr/jcy038, 10.1093/esr/jcaa007, 10.1093/bjc/azac071, 10.1111/1745-9125.12259, 10.1111/1745-9125.12378, 10.1073/pnas.2212757120, 10.2139/ssrn.3506811, 10.1016/j.jeconom.2020.12.001, 10.1016/j.jeconom.2021.03.014, 10.1590/dados.2023.66.2.303, 10.1017/lap.2023.24, 10.31389/jied.247, 10.4322/dilemas.v15esp4.52509, 10.5935/0034-7140.20210001, 10.1016/j.jeconom.2020.09.006, 10.1257/aer.20181169, 10.1093/restud/rdae007, 10.1016/j.jeconom.2023.03.008, 10.1093/restud/rdad018, 10.1016/j.jdeveco.2021.102637, 10.1093/publius/pjab025, 10.5539/ijef.v14n11p46, 10.1086/721700, 10.1016/j.ssresearch.2016.06.008, 10.1177/000312240306800603, 10.1177/0002764218823844, 10.1177/1477370819887511, 10.1177/10887679231201803, 10.1186/s12889-025-24814-6, 10.1080/01924036.2026.2731244, 10.1590/s2237-96222025v34e20240350.en, 10.1590/s2237-96222024v33e2024296.especial.en, 10.1590/1980-549720200006.supl.1, 10.1016/j.regsciurbeco.2023.103913, 10.3389/fpsyg.2019.02328, 10.1111/ajps.12595, 10.1002/cl2.70048, 10.7910/DVN/6KVTUV.

URLs (7): nota Lilley & Wheaton (GitHub), destaque AEA de Müller & Schwarz, FBSP armas e homicídios (sumário e informe), Anuário FBSP 2026, Atlas 2025 (handle Ipea 11058/17165), Silva 2025 (Even3).

Duplicata conhecida: 10.1111/1745-9125.12378 (Mills et al.) também foi emitido por outro briefing; não afeta a contagem acima. O Bolognesi saiu no ledger com ano 2022 (OpenAlex); a citação correta é Dados 66(2), 2023.
