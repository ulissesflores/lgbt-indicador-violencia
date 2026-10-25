# F5 — Economia política do dado: hipóteses testáveis com dados brasileiros publicados

Rodada 3, 2026-10-21. Pasta: `research-2026-10-21-rodada3/F5-economia-politica/`.
Base: dossiê `DOSSIE-CONSOLIDADO-2026-10-12.md`, Parte A §4 e §8. Nada de pesquisa de campo; só dado já publicado.
Reprodução: todos os scripts rodam com `/opt/homebrew/bin/python3.14 -I` (numpy, pandas, scipy; sem statsmodels), semente fixa, ordem em "Arquivos". Hashes dos insumos e saídas em `SHA256SUMS.txt`.

> [!IMPORTANT]
> Placar: **H1 testada, nula e com pouco poder. H2 testada, nula, direção oposta à prevista, quase sem poder. H3 testada só em série nacional (painel UF tem 3 anos), indeterminada. H4 NÃO testada (microdado exige aceite de termos; item sobre IBGE não existe). H5 entregue como linha do tempo + séries de execução orçamentária, com um limite duro (sem custo por pesquisa individual).**
> Nenhum resultado aqui sustenta "metas escondem homicídio" nem "estrutura especializada reduz zero cerimonial" nem "militância infla por cobertura". Nenhum refuta. O que muda no dossiê está na seção "O que muda no dossiê".

## Placar (uma linha por hipótese)

| H | O que foi medido | Resultado | Poder / limite | Estado |
|---|---|---|---|---|
| H1 | Parcela de mortes de intenção indeterminada (Y10-Y34) depois do início de programa de metas, 7 UFs x 20 UFs sem programa achado, 1996-2024 | efeito ≈ 0 (+0,25 p.p.; IC95% −3,2 a +3,7 p.p.; p randomização 0,92) | efeito mínimo detectável 6,3 p.p. sobre média de 14,3%; controles podem ter programa que não achei | ✅ rodado, nulo |
| H2 | UFs que não informam "racismo por homofobia/transfobia" no Anuário x estrutura estadual LGBT (ESTADIC 2019/2023) | associação na direção OPOSTA à prevista, não significativa (AUC 0,375; Fisher p 0,24) | poder 26% para OR 4; 27 UFs | ✅ rodado, nulo |
| H3 | Contagem do GGB x internet, controlando homicídios SIM | níveis: internet +1,2%/p.p. (tendência comum); diferenças: nulo; painel UF: nulo | série nacional n=25 colinear com tendência; painel UF só 2021, 2023, 2024 | ⚠️ indeterminada |
| H4 | Confiança em estatística/polícia por ideologia | NÃO medido | microdado LAPOP exige aceite de termos; nenhuma pesquisa de confiança no IBGE por ideologia achada | 🚫 fila |
| H5 | Linha do tempo + execução orçamentária | 17 eventos: 9 com trecho verbatim conferido (8 documentos + PNS), 1 evidência negativa interna (PNDS), 7 recalculados de CSV | sem custo por pesquisa/suplemento; execução aberta só 2007+ | ✅ com limite |

## H1 — número baixo serve à gestão por metas?

**Hipótese operacional.** UFs que adotaram programa formal de redução de homicídios com metas passam a ter MAIOR parcela de mortes de intenção indeterminada (MVCI) do que antes e do que UFs sem programa.

**Dados.**
- SIM/DATASUS por UF de residência, 1996-2024, grandes grupos CID-10 X85-Y09, Y10-Y34, Y35-Y36 (`dados/h1_sim_tabnet_uf_ano.csv`; bruto TabNet em `dados/raw/`; sha256 em `dados/raw/SHA256SUMS.txt`). Conferido contra o Atlas 2026 Tabela 3.5: MVCI Brasil 2014=9.468, 2019=16.648, 2023=13.896, 2024=17.207, idênticos; soma das 27 UFs = linha Brasil em todas as tabelas parseadas (`dados/h1_atlas_parse_checks.txt`). Não usei o `agrega_sim.py` da frente principal (estava rodando); os totais anuais dele (2010: 9.703 indeterminadas; 2023: 13.896; 2024: 17.207) batem com os meus.
- "Homicídios ocultos" = ESTIMATIVA de aprendizado de máquina de Cerqueira & Lins (2024), não contagem: TD Ipea 3015 (`fontes/q1-textointegral/F5/TD3015.pdf`, sha256 `238560a5...e4e98`) e Tabelas A.4/A.5 em xlsx do repositório (1996-2021); Atlas 2025 Tabela 3.3 e Atlas 2026 Tabelas 2.2, 3.3, 3.5. Séries coincidem onde se sobrepõem (2021: 5.152 nas duas). Reporto as duas medidas separadas: **Y1 = Y10-Y34 / (X85-Y09 + Y35-Y36 + Y10-Y34)** (contagem bruta do SIM) e **Y2 = ocultos / (registrados + ocultos)** (modelo, 1996-2021).
- Programas e anos de início: `dados/h1_programas_metas.csv`, cada trecho verbatim conferido no arquivo local por `scripts/h1_00_verifica_citacoes_programas.py` (7 de 7 OK).

| UF | Programa | Início (primário) | Fonte lida | Confiança |
|---|---|---|---|---|
| PE | Pacto pela Vida | 2007 | SDS-PE, Boletim Trimestral 2T/2022: "O Programa Pacto pela Vida–PPV foi lançado em maio de 2007" | alta |
| MG | Fica Vivo! (Decreto 43.334/2003) | 2003 | Portal MG: "Decreto estadual 43.334/2003, que cria o Programa de Controle de Homicídios" | média (prevenção focalizada; não achei meta formal no que li) |
| RJ | Sistema de metas (Decreto 41.931, 25/06/2009) | 2009 | Decreto 42.780 (texto na base legisweb) altera o 41.931 e fala em "sistema de definição e gerenciamento de metas" | média (original do 41.931 não lido) |
| ES | Estado Presente em Defesa da Vida | 2011 | IJSN-ES: "foi lançado, em maio de 2011" | média (ato de criação não lido) |
| BA | Pacto pela Vida (Lei 12.357, 26/09/2011) | 2011 | Legislabahia, texto da lei | alta |
| PB | Paraíba Unida pela Paz | 2011 | documento institucional da PM-PB: "instituiu, em 2011" | baixa (texto da Lei 11.049/2017 deu 403) |
| CE | Pacto por um Ceará Pacífico | 2015 | notícia oficial SEDUC-CE 07/08/2015: "Decreto que institui o Pacto foi assinado" | média (número do decreto veio de resumo de busca, não li o texto) |

Controles = as 20 UFs **sem programa encontrado nesta busca**. Isso NÃO é "UF sem programa": RS, SP, GO e outras podem ter programa que não procurei. Contaminação dos controles puxa o efeito para zero.

**Desenho** (`scripts/h1_03_analise.py`, semente 20261021). DiD por coorte: para cada UF tratada, (média dos 4 anos antes do início) contra (média dos H anos a partir do início, com defasagem 0 ou 1 ano), menos a mesma diferença nas UFs controle; média das 7 UFs. IC95% por bootstrap de UFs dentro de cada braço (5.000). Inferência por randomização: sorteio de 7 UFs entre as 27 recebendo os mesmos 7 anos de início (10.000 sorteios). Event study 2x2 limpo. TWFE com wild-cluster bootstrap Rademacher, H0 imposta, 27 clusters, 9.999 reamostragens.

**Resultados** (`dados/h1_resultados_did.csv`, `dados/h1_resultados_por_uf.csv`, `dados/h1_event_study.csv`; unidade = ponto percentual de parcela, média geral Y1 = 14,3%, DP entre UF-anos 13,1 p.p.).

| Especificação | ATT | IC95% (bootstrap) | p randomização | efeito mínimo detectável (80%) |
|---|---|---|---|---|
| Y1, defasagem 0, janela 4 anos (principal) | +0,25 p.p. | −3,15 a +3,68 | 0,92 | 6,3 p.p. |
| Y1, defasagem 1, janela 4 | +1,09 | −2,59 a +4,79 | 0,67 | 7,0 |
| Y1, defasagem 0, janela 7 | +1,13 | −2,43 a +4,84 | 0,66 | 7,0 |
| Y1, defasagem 1, janela 7 | +1,40 | −2,73 a +5,45 | 0,61 | 7,6 |
| Y2 (ocultos), defasagem 0, janela 4 | −0,71 | −2,37 a +0,95 | 0,66 | 4,4 |
| Robustez, UF retirada SAI do painel (não vira controle): sem MG / sem ES / só 5 com meta formal (sem MG e ES) / sem RJ / sem 2023-24 | +1,86 / −0,55 / +1,23 / −0,06 / +0,25 | todos cruzam zero (ex.: sem MG −0,67 a +4,57) | 0,36 / 0,82 / 0,57 / 0,98 / 0,91 | 5,8-6,9 |
| TWFE Y1 (29 anos) | +4,89 p.p. (t = 1,14) | — | p wild-cluster 0,30 | — |
| TWFE Y2 (26 anos) | +0,51 p.p. (t = 0,19) | — | p wild-cluster 0,86 | — |

Por UF (Y1, defasagem 0, janela 4): PE +5,7; MG −9,4; RJ +2,1; ES +5,0; BA −3,8; PB +0,6; CE +1,5 p.p. Heterogeneidade grande e de sinal misto.
Duas ressalvas que o IC sozinho não mostra. (1) Os programas começaram onde o dado já era ruim: parcela média de MVCI nos 4 anos antes do início foi 31% (MG), 27% (RJ), 27% (BA) contra 9% (PE), 6% (ES), 5% (PB), 10% (CE). O momento do tratamento pode responder ao dado, e regressão à média trabalha contra a hipótese. (2) Nos anos 1996-2002 tratadas e controles eram parecidas (17,9% x 19,5%); de 2003 em diante as tratadas ficam acima (15,6-22,3% x 9,1-14,6%, médias por período). O DiD não transforma essa diferença descritiva em efeito, e eu não a apresento como efeito.

**Frase que o resultado permite.** "Com 7 UFs que adotaram programas de metas ou de redução de homicídios entre 2003 e 2015 e 20 UFs sem programa achado, a parcela de mortes de intenção indeterminada não mudou de forma detectável depois do início (+0,25 p.p., IC95% −3,2 a +3,7), e o desenho só detectaria aumentos acima de ~6 p.p."
**Frase que NÃO permite.** "Programas de metas não escondem homicídio" (o IC admite −3 a +4 p.p. e o desenho não detecta efeitos menores que ~6 p.p.), nem "metas escondem homicídio" (ponto estimado ≈ 0; sinal por UF misto).
**Condição de volta.** (a) Texto original de Decreto 41.931/2009, ato do ES, texto da Lei 11.049/2017 e Decreto 31.787/2015 (fila-aquisicao). (b) Lista completa de programas por UF, incluindo os dos controles, com data (hoje 7 de 27). (c) Dado municipal ou por delegacia de MVCI, que multiplicaria as unidades. Sem isso o resultado fica nulo com baixo poder.

### H1b — achado exploratório (NÃO pré-especificado; olhado depois de ler o Atlas 2025)

O Atlas 2025 atribui a queda dos homicídios ocultos em 2023 à reação dos governos ao próprio Atlas 2024: "após a repercussão acerca da divulgação do número de homicídios ocultos no Atlas da Violência de 2024, os governos de muitas UFs se mobilizaram para melhorar a qualidade dos dados, fazendo diminuir as MVCI" (`fontes/t1-atlas-2025/atlas2025.txt` linha 1021; sha256 do .txt `7debccd7...2016`) e dá o caso do ES: "enquanto a estimativa de homicídio oculto no ES em 2022 foi de 205 casos, em 2023 esse indicador passou para apenas sete casos" (linhas 1025-1026). O Atlas 2026 diz que em 2024 voltou: "houve aumento acentuado das Mortes Violentas com Causa Indeterminada (MVCI), de 3.311 casos, ou crescimento de 23,8%" (`fontes/t1-atlas-2026/atlas2026.txt` linha 303; sha256 `1e9f0cb6...1f983`).
Números das tabelas (Atlas 2026 Tab. 3.3 e 3.5, parseados): ocultos Brasil 5.982 (2022), 3.755 (2023), 7.083 (2024); 21 UFs reduziram ocultos de 2022 para 2023 e 23 UFs aumentaram de 2023 para 2024. ES 205 -> 7 -> 96; PE 237 -> 50 -> 124. Nas 7 UFs com programa, ocultos 2.589 -> 933 -> 3.255; nas outras 20, 3.393 -> 2.822 -> 3.828.
Teste (`scripts/h1_04_exposicao_2023_exploratorio.py`; `dados/h1_exposicao_2023_exploratorio.csv`): variação do log de MVCI bruta (Y10-Y34), tratadas menos controles, permutação de rótulos de UF: 2021->22 +0,39 (p 0,009); 2022->23 −0,30 (p 0,18); 2023->24 +0,12 (p 0,41); 2022->24 −0,18 (p 0,44). Quatro janelas, nenhuma pré-especificada: só a primeira (2021->22, antes do Atlas 2024, portanto não é o ano de exposição) passa de 0,05 e passaria mesmo com Bonferroni sobre as 4 (limiar 0,0125), mas a escolha das janelas e da própria pergunta veio depois de ver os dados (caminhos bifurcados). É pista, não achado.
**Frase permitida.** "O próprio Ipea/FBSP documenta que a MVCI caiu em 2023 após a divulgação do Atlas 2024 e subiu de novo em 2024; nas UFs com programa a oscilação foi maior em valor relativo (ocultos −64% e depois +249%), sem teste formal significativo."
**Frase NÃO permitida.** "Programas de metas causam manipulação da causa da morte." (volatilidade maior não distingue melhora de registro, mudança de codificação e ruído; o modelo de ocultos depende da MVCI.)

## H2 — zeros cerimoniais de crime de ódio e estrutura especializada

**Dados.** Anuário FBSP "racismo por homofobia ou transfobia" por UF-ano (`dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv`, 3 edições, anos de dado 2022-2025; uso a última edição que traz cada UF-ano). Estrutura: ESTADIC/IBGE 2019 e 2023 (bases .xlsx oficiais; sha256 em `dados/raw/estadic/SHA256SUMS.txt`), seis itens por UF (códigos IBGE): EDHU086 (órgão de direitos humanos executa programas para LGBT), EDHU5410 (comitê gestor de enfrentamento à violência LGBTfóbica), EDHU576 (política/programa de promoção LGBT), ESEG4413 (capacitação continuada da PM com tema LGBTfobia), ESEG487 (ações da PM voltadas à população com tema LGBTfobia), ESEG5913 (capacitação da Polícia Civil com tema LGBTfobia).
**Achado de construto.** Nenhum UF informou "0" numérico em nenhuma edição. O "zero cerimonial" do Anuário aparece como "..." (informação não disponível: BA e RJ em todos os anos; MA, SC, AM, SP em alguns) ou "-" (fenômeno inexistente: PA em 2022-2023 na edição 2024/25, TO em 2024-2025). A edição 2026 traz PA 2024=38, que a edição 2025 dava como "-": revisão sem nota. 8 de 27 UFs não informaram em pelo menos um UF-ano.
**Limites do dado.** O ESTADIC não tem item de delegacia especializada em crime racial/LGBT por tipo (varri o dicionário por "delegacia" e "crimes raciais/ódio"); tem só o TOTAL de delegacias especializadas da Polícia Civil (ESEG5134, sem tipo, inclui as de mulheres). A parte "delegacia" da hipótese só pode ser testada por esse proxy fraco (linha extra abaixo, pós-hoc) e a versão específica fica na fila-aquisicao. 'Recusa' (1 UF em 2023) e '-' tratados como ausentes.

**Resultados** (`scripts/h2_02_analise.py`, semente 20261024; `dados/h2_resultados.csv`, `dados/h2_uf_resumo.csv`).

| Teste | Resultado |
|---|---|
| Fisher: não informou x comitê LGBT (EDHU5410) em alguma edição | tabela [[13,6],[6,2]], OR 0,72, p 1,00 |
| Fisher: não informou x índice de estrutura >= mediana | tabela [[10,9],[2,6]], OR 3,3 (não informantes com MAIS estrutura), p 0,24 |
| Spearman: nº de UF-anos sem informação x índice de estrutura | rho +0,18, p permutação 0,37 (sinal oposto ao previsto) |
| AUC: P(índice do informante > índice do não informante) | 0,375 (IC95% 0,13 a 0,64; previsto > 0,5) |
| Spearman: taxa 2024 por 100 mil (informantes, n=23) x índice | rho +0,18, p 0,40 |
| Poder do Fisher (simulação 4.000, marginais observadas) | 7% para OR 2; 26% para OR 4; 57% para OR 8 |
| PÓS-HOC (olhado depois do resultado nulo; proxy sem tipo): Spearman, nº de UF-anos sem informação x delegacias especializadas por milhão de habitantes (ESTADIC 2019, n=26; `scripts/h2_03_delegacias_proxy.py`, `dados/h2_resultados_delegacias_proxy.csv`) | rho −0,35 (direção prevista), p permutação 0,084 |

**Frase permitida.** "Entre as 27 UFs, as que deixaram de informar (ou informaram 'inexistente') crimes de ódio contra pessoas LGBT em ao menos um ano de 2022-2025 não têm menos estrutura estadual LGBT no ESTADIC 2019/2023 do que as demais (direção oposta, p 0,24); com 8 UFs sem informação o teste só detectaria associações muito fortes (poder 26% para OR 4)."
**Frase NÃO permitida.** "Estrutura especializada reduz o zero cerimonial" ou "o zero cerimonial não tem relação com estrutura". O índice do ESTADIC mede treinamento, comitê e programa; o único sinal na direção prevista (delegacias especializadas totais, rho −0,35, p 0,084) é pós-hoc, sem tipo e não significativo; e BA e RJ, que nunca informam, são UFs com estrutura média/alta no índice.
**Condição de volta.** Dado de delegacias e serviços especializados por UF (leis estaduais, SSPs, MUNIC) e segunda onda de ESTADIC (2014/2017, baixados e não varridos; fila-aquisicao), e pelo menos 2 anos a mais de Anuário.

## H3 — contagem militante cresce com cobertura, não só com incidência?

**Dados.** GGB, mortes violentas de LGBT+: série nacional 2000-2020 (Tabela 1 do relatório de 2020, Acontece/GGB; `fontes/p3-ggb/_raw/txt/ggb2020.txt`, sha256 do .txt `29feb5c3...ad68`), 2021=300, 2022=256 (derivado de "257 ... um caso a mais do registrado em 2022"), 2023=257, 2024=291 (`dados/h3_ggb_nacional_2000_2024.csv`, com trecho e linha). Só contagem agregada, nenhum dado nominal. UF x ano: tabelas completas só para 2021 (soma 297 + 3 "não informado" = 300), 2023 (soma das UFs = 255, o total impresso diz 257) e 2024 (291) (`dados/h3_ggb_uf_ano_agregado.csv`); 2017-2020 e 2022 têm só rankings parciais (2022: 135 das 256). Cobertura: % de pessoas que usaram internet (ITU/Banco Mundial, Brasil, 2000-2024; `dados/raw/wb_internet_bra.json`) e, por UF, % de domicílios com internet (PNAD Contínua TIC, SIDRA 7307, 2016-2025 sem 2020). Incidência: homicídios registrados do SIM (X85-Y09 + Y35-Y36). Número de veículos de imprensa por UF: NÃO ENCONTRADO como série pública (declarado).
**Inconsistência interna do GGB (achado lateral).** A soma anual publicada em 2021 para 2010-2019 é 3.363; o relatório de 2023 dá 3.029 para a mesma década (−334, −10%); 2000-2009: 1.446 contra 1.429. Séries revisadas sem tabela de reconciliação, como o dossiê já aponta para o Anuário (§4 regra 7).

**Resultados** (`scripts/h3_analise.py`, semente 20261023; `dados/h3_resultados_nacional.csv`, `dados/h3_resultados_painel_uf.csv`, `dados/h3_serie_nacional_insumos.csv`).

| Modelo (série nacional) | n | coeficiente da internet (por p.p.) | coeficiente dos homicídios (elasticidade) |
|---|---|---|---|
| Níveis: log GGB ~ internet | 25 | +0,0129 (EP HAC 0,0026; IC bloco 0,0074 a 0,0216) | — |
| Níveis: log GGB ~ log homicídios | 25 | — | 2,03 (IC bloco −0,28 a 4,02) |
| Níveis: ambos | 25 | +0,0122 (IC 0,0091 a 0,0163) | 1,77 (IC 0,91 a 2,50) |
| Diferenças: ambos | 24 | −0,0253 (IC −0,062 a +0,019) | +0,69 (IC −1,00 a +1,35) |
| Antes do pico (2000-2017), diferenças | 17 | −0,0083 (IC −0,062 a +0,052) | +0,31 (IC −1,55 a +2,92) |
| Depois do pico (2017-2024), níveis: log GGB ~ internet | 8 | **−0,0325 (IC −0,047 a −0,0015)** | — |
| Painel UF (Poisson EF UF+ano; 2021, 2023, 2024; 81 obs) | 81 | +0,0026 (EP 0,026; p permutação 0,93) | 0,54 (EP 0,52; p 0,31) |

Fatos: GGB e homicídios registrados têm o pico no mesmo ano (2017: 445 e 65.602); Spearman GGB x homicídios 0,51, GGB x internet 0,70; internet 67,5% (2017) -> 84,5% (2024) enquanto a contagem cai de 445 para 291 (237 em 2020).
**Frase permitida.** "Em níveis, a contagem do GGB cresce com a internet (+1,2% por p.p.) mas isso é tendência comum 2000-2017; em diferenças e no painel por UF o efeito da internet é indistinguível de zero (IC −6 a +2% por p.p.), e depois de 2017 a contagem CAI enquanto a internet sobe, o que uma explicação só de cobertura não prevê."
**Frase NÃO permitida.** "A contagem militante é inflada por cobertura" ou "não é". A série nacional (n=25) não separa cobertura de incidência (ambas culminam em 2017), o painel por UF tem 3 anos, e a contagem é piso de imprensa, não taxa.
**Condição de volta.** Tabela agregada UF x ano do GGB 2000-2024 (sem nomes) e cobertura de imprensa/internet municipal; com 25 anos x 27 UFs o painel passa a ter poder. Fila-aquisicao F5-H3.

## H4 — polarização e confiança em estatística: NÃO TESTADA

- Espaço de busca enumerado: 2 consultas (PT "extended" sobre confiança em IBGE/instituições por pesquisa de opinião; EN sobre confiança em estatística oficial x ideologia/partidarismo no Brasil) + checagem do questionário LAPOP Brasil 2023. Retornaram: rankings de confiança em instituições (Datafolha, Genial/Quaest, Ipespe) sem IBGE; confiança em urnas por ideologia (Datafolha 2022: 83% Lula x 58% Bolsonaro; imprensa, não lida em texto integral); dissertação sobre comunicação do IBGE (não lida). **Nenhuma pesquisa de confiança no IBGE ou em estatística oficial por ideologia.** Isso é evidência de busca limitada, não de inexistência.
- LAPOP Brasil 2023, questionário lido (`fontes/q1-textointegral/F5/lapop_bra2023_questionario.pdf`, sha256 `58c55ca9...c3dfd`): tem B18 (confiança na Polícia Militar, escala 1-7), B12 (Forças Armadas), B13 (Legislativo), B47A (eleições) e L1N (autoposição esquerda 1 - direita 10); **não tem item sobre IBGE ou estatísticas**. O proxy é confiança em polícia/eleições, não em dado.
- Os microdados (.dta) exigem aceite dos termos de uso do LAPOP em navegador; o aceite é ato do titular, não meu. `scripts/h4_lapop_confianca_x_ideologia.py` está pronto, **testado só em dado sintético** (roda e produz tabela e IC; zero valor empírico) e aguarda `<arquivo.dta> <ano>`. Latinobarómetro e ESEB: idem, fila.
- Citado só como pista, NÃO como evidência: Rossini et al. (Harvard Misinformation Review, 2023) usa escala esquerda-direita e confiança em instituições na eleição de 2022; li só o apêndice listado na busca.
**Frase permitida.** "Não encontrei, em 2 buscas e no questionário LAPOP 2023, pesquisa brasileira publicada de confiança em estatística oficial por ideologia; o que existe é confiança em polícia/eleições, computável quando o microdado LAPOP for baixado."
**Frase NÃO permitida.** Qualquer afirmação sobre polarização e confiança em dado brasileiro com número.

## H5 — por que não foi resolvido antes: linha do tempo e execução orçamentária

`dados/h5_linha_do_tempo.csv` (17 eventos; 9 trechos verbatim conferidos por `scripts/h5_04_linha_do_tempo.py`, 9 de 9 OK, com sha256 do arquivo lido; 7 eventos orçamentários recalculados dos CSVs; 1 evidência negativa interna).

| Data | Evento | Fonte lida (arquivo local) |
|---|---|---|
| 1988 | PNAD: 1o suplemento nacional de vitimização e justiça | CNJ, Panorama do acesso à justiça (cita IBGE 1988 e 2009) |
| 2009 | PNAD 2009: reedição "vinte e um anos depois" (IBGE + CNJ) | idem |
| 2012-07-04 | Lei 12.681: institui o SINESP | planalto.gov.br |
| 2012-13 | PNV (MJ/Senasp, Datafolha, CRISP): "a única e primeira pesquisa de abrangência nacional" do Ministério | MJ, estudo sobre vitimização |
| 2018-06-11 | Lei 13.675, art. 13, VI: o ministério deve "realizar estudos e pesquisas nacionais e consolidar dados e informações estatísticas sobre criminalidade e vitimização" | planalto.gov.br |
| 2019-20 | PNS 2019: orientação sexual "experimental" | artigo da PNS já no projeto |
| 2021-T4 | PNAD Contínua: furtos e roubos "pela primeira vez" (IBGE + MJSP); não mede violência interpessoal nem motivação | IBGE, informativo |
| 2025-08 | FBSP: "o Brasil ainda não produz pesquisas de vitimização sistemáticas e regulares"; MJSP "só produziu uma única grande pesquisa do tipo em sua história, em 2012" | FBSP 2025 |
| 2026-10-11 | PNDS 2023 (orientação e identidade de gênero) sem resultados publicados (evidência negativa do registro de andamento; reverificar) | registro de andamento do projeto |

**Execução orçamentária.** Duas fontes oficiais que NÃO se emendam: Portal da Transparência/CGU, `OrcamentoDespesa` anual 2014-2025; SIOP/Ministério do Planejamento, LOA em RDF 2007-2013 (hashes dos 19 zips em `dados/h5_orcamento_hashes_tudo.txt`). A granularidade é de ação orçamentária, **não de pesquisa individual**: o custo do suplemento de vitimização de 1988/2009, da PNV 2012 e do módulo de 2021 NÃO aparece (fila-aquisicao: DOU, extratos de contrato e termos de execução). Antes de 2007 não há série aberta. Valores "reais" = IPCA SIDRA 1737, dezembro de cada ano, para dez/2025.

| Ação / série (empenhado, R$ milhões) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| IBGE, Pesquisas e estudos estatísticos (reais dez/2025) | 50,9 | **20,1** | 22,4 | 29,6 | 49,6 | 82,6 | 107,7 |
| IBGE, Censos (nominais; Censo 2020 adiado) | 246 | 190 | 169 | 2.291 | 472 | 66 | 31 |

Queda real de 60% na ação de pesquisas estatísticas do IBGE de 2019 para 2020; só em 2023 volta quase ao patamar de 2019 (49,6 x 50,9); em 2025 é 2,1 vezes o de 2019. (Nominal e real por ano em `dados/h5_series_chave_acoes.csv`; fonte CGU, `h5_orcamento_acoes.csv`.) A ação de pesquisas inclui toda a PNAD, PNS e demais pesquisas do IBGE; o módulo de vitimização de 2021 é uma parte desconhecida dela.
**Linhas orçamentárias LGBT-nomeadas** (`dados/h5_acoes_lgbt_rdf_2007_2013.csv`, `dados/h5_acoes_lgbt_cgu_2014_2025.csv`; R$ nominais; "pago" = valorPago do RDF no exercício, restos a pagar posteriores não aparecem):
- Dados/pesquisa: "Banco de Dados sobre Cidadania Homossexual e Combate à Homofobia": 2008 dotação 0,40, empenhado 0,20, pago 0,04; 2009 empenhado 0,01. "Núcleos de Pesquisa sobre Cidadania Homossexual e Combate à Homofobia": 2008 empenhado 0; 2009 0,33 (pago 0,11); 2010 0,06 (pago 0,01); 2011 0. Produção e disseminação de conhecimento LGBT: 2012 dotação 4,70, empenhado 1,07, pago 0,004; 2013 dotação 5,00, empenhado 1,56, pago 0.
- Serviços: "Apoio a Serviços de Prevenção e Combate à Homofobia": 2011 dotação 35,34, empenhado 1,95, pago 0,37.
- 2014-2025: ação nomeada LGBT existe em 2014 (0,80), 2015 (1,01), 2019 (2,50), 2024 (26,22), 2025 (24,95); **não existe com esse nome em 2016-2018 e 2020-2023** (316.210 linhas varridas; a primeira varredura que fiz não achava nada em 2014-2023 por usar "LGBT" e não "Lésbicas...", e foi refeita). Nenhuma é de pesquisa/medição pelo nome.
**Frase permitida.** "Existiu e foi executada uma fração: nas quatro linhas de dados/pesquisa LGBT da SEDH (2008-2013) a dotação somou R$ 12,68 milhões, o empenhado R$ 3,22 milhões (25%) e o pago no exercício R$ 0,17 milhão (1,4%); na linha de apoio a serviços (2007-2011) foram R$ 72,0 milhões de dotação, R$ 10,2 milhões empenhados (14%) e R$ 5,4 milhões pagos (7,5%); a ação de pesquisas estatísticas do IBGE caiu 60% em termos reais de 2019 para 2020 e só voltou quase ao patamar em 2023." (pago = valorPago do RDF no exercício; restos a pagar posteriores não aparecem, então 1,4% é piso.)
**Frase NÃO permitida.** "O orçamento foi cortado para esconder dado" (a queda de 2020 coincide com a pandemia, que paralisou coleta presencial do IBGE, com contenção fiscal e com o adiamento do Censo; e a ação do IBGE agrega todas as pesquisas), ou qualquer valor de custo de uma pesquisa específica.
**Condição de volta.** DOU/Comprasnet/SIAFI para custo por pesquisa; série anterior a 2007.

## O que muda no dossiê (Parte A §4 e §8)

1. ⚠️ **§8, "número baixo serve à gestão sob meta" (hoje só literatura):** nos dados brasileiros, programas de metas não mudam de forma detectável a parcela de MVCI (IC −3,2 a +3,7 p.p., MDE 6 p.p.). Reescrever como hipótese NÃO confirmada e de baixo poder, não como achado.
2. ⚠️ **§8, remédio "publicar completude":** o Atlas documenta que a exposição pública de 2024 foi seguida de queda da MVCI/ocultos em 21 UFs em 2023 (ES 205 -> 7) e de reversão em 2024 (+23,8% MVCI; ocultos 3.755 -> 7.083). Sugere que a pressão move o número e que o efeito não é persistente. Exploratório.
3. ✅ **§4 regra 3 (zeros cerimoniais):** a leitura do Anuário é mais fina que "zero": nenhum UF informou 0; o zero aparece como "..." ou "-" (BA, RJ, PA, TO, MA, SC, AM, SP). A causa institucional não aparece no ESTADIC (oposta à prevista) e o ESTADIC não tem item de delegacia por tipo (só o total, com sinal fraco na direção prevista, p 0,084, pós-hoc).
4. ⚠️ **§4, "militância infla":** a contagem do GGB cai a partir de 2017 enquanto a internet sobe, e a série tem inconsistência interna (2010-2019: 3.363 somando os anos x 3.029 no relatório de 2023; UFs 2023: 255 x 257). A hipótese de cobertura não explica a queda e a série precisa de reconciliação antes de ser citada.
5. ✅ **§8, "o instrumento existe e está engavetado":** confirmado em fonte primária, e quantificado: nas linhas LGBT de dados/pesquisa de 2008-2013 foram empenhados 25% e pagos no exercício 1,4% da dotação (piso, restos a pagar fora); a ação de pesquisas do IBGE caiu 60% real em 2020; PNAD 1988/2009/2021 e PNV 2012 confirmadas (CNJ, MJ, IBGE, FBSP) e a PNAD 2021 só mediu furtos e roubos (✅ confere com o dossiê).

## Becos (condição de volta)

| Beco | Por quê | Volta se |
|---|---|---|
| Lei 11.049/2017 (PB), texto | HTTP 403 em 3 User-Agents | Chrome real ou Wayback |
| Decreto 41.931/2009 (RJ), Decreto 31.787/2015 (CE), ato do ES | não li o texto original | texto oficial lido |
| LAPOP/Latinobarómetro/ESEB microdados | aceite de termos/registro | titular aceita; script pronto |
| ESTADIC 2014/2017 | .xls antigo, sem leitor instalado | converter e varrer |
| GGB UF x ano completo | relatórios só têm ranking parcial (2017-20, 2022) | tabela agregada do GGB |
| Custo por pesquisa/suplemento | granularidade do orçamento | DOU/Comprasnet |
| Série orçamentária antes de 2007 | não há dado aberto | Câmara/Senado (PDF) |
| Controles de H1 contaminados | só achei 7 programas | levantamento completo UF a UF |

## Arquivos

Scripts (`scripts/`), em ordem: `h1_00_verifica_citacoes_programas.py`, `h1_01_tabnet_sim_1996_2024.py`, `h1_02_parse_atlas_td.py`, `h1_03_analise.py`, `h1_04_exposicao_2023_exploratorio.py`, `h2_01_estadic_lgbt.py`, `h2_02_analise.py`, `h2_03_delegacias_proxy.py`, `h3_analise.py`, `h4_lapop_confianca_x_ideologia.py`, `h5_01_orcamento.py`, `h5_02_series_chave.py`, `h5_03_acoes_lgbt_rdf.py`, `h5_04_linha_do_tempo.py`, `h5_05_acoes_lgbt_cgu.py`, `emite_ledger_f5.py`. Os scripts h5_01, h5_03 e h5_05 leem os zips em `dados/raw/orcamento/` (188 MB; `*.zip` está no `.gitignore`; variável `F5_CACHE` muda a pasta) e os baixam de novo se faltarem (hashes em `dados/h5_orcamento_hashes_tudo.txt`).
Dados e saídas em `dados/` (CSVs citados acima; brutos em `dados/raw/`). Ledger: `sources.jsonl` (23 fontes novas, `origem=rodada3-F5`, todas via `emit_sources.py`). Fila: `fila-aquisicao.jsonl` (13 itens). PDFs e xlsx em `fontes/q1-textointegral/F5/` (TD 3015, Tabelas A.4-A.6, questionário LAPOP).
Q1: nenhuma referência de periódico foi usada como evidência nesta frente; as fontes são documentos oficiais primários (IBGE, DATASUS, Ipea, CGU, SIOP, leis, relatórios de órgãos) e relatórios de ONG usados só como "contagem declarada" (GGB). Rossini et al. fica como pista, `quartil=nao_verificado`, não lido.
