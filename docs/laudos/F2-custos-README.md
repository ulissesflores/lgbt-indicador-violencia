# F2 — Custos e desenho dos dados que faltam (violência por orientação sexual, identidade de gênero, raça e gênero)

Rodada 3, 2026-10-21. Escopo: só dado e texto já publicados; nenhuma pesquisa de campo. Valores em R$ de set/2026 (IPCA, SIDRA 1737) salvo indicação; estrangeiros convertidos a PTAX de 2026-10-20, nominal, sem paridade de poder de compra.

## 0. Resposta

1. **O dossiê (Parte A §3 e §9) subestima o tamanho de amostra por um fator de 5,1 no indicador central.** Ele usou amostragem aleatória simples. Com o efeito de desenho medido no microdado da PNS 2019, detectar +30% de violência física entre LGB+ exige ~5.800 LGB+ por rodada, não 1.133, ou seja ~306 mil adultos triados, não ~60 mil. Uma PNS do tamanho de 2019 (88.531 adultos) só detecta variação de ~58%, não de 25-30%.
2. **"Sobreamostra de 5x" não reduz a triagem.** Com 1,89% de LGB+, achar 5.787 LGB+ custa triar ~306 mil adultos com ou sem sobreamostra; a sobreamostra só corta as entrevistas completas de quem não é LGB+. O custo está no número de domicílios contatados.
3. **Opção recomendada: módulo anual na PNAD Contínua** (rotação 1-2(5), seleção de 1 morador adulto, opção de entrevista por telefone). Custo central R$ 6,8 milhões por ano, faixa R$ 6,8-69,9 milhões; ~275,6 mil adultos, ~5,2 mil LGB+; detecta ~32% (física) e ~12% (qualquer violência). É a única das três que chega perto de 30% por menos de R$ 10 milhões, e só porque usa visitas que o IBGE já faz.
4. **Mudança de 10% em violência física LGB+ não é detectável em um ano por nenhuma das três opções** (2,56 milhões de adultos triados, ~9 anos de módulo PNADC ou R$ 650 milhões em campo dedicado). 20% exige ~2,4 anos de módulo PNADC acumulado (R$ 15 milhões) ou R$ 169 milhões em campo dedicado.
5. **Custo da PNS: o único documento é uma MINUTA** (TED "n.º XX/2023", objeto "PNS-2024", R$ 22.291.444,00, coleta prevista nov/2024-fev/2025), mas a coleta real da PNS está em campo agora (jul-nov/2026, ~140 mil domicílios segundo notícia). Valor final e aditivos não verificados. Custo de PNS 2019, PNDS 2023 e PNV 2012: **não encontrados em fonte primária** (fila-aquisicao.jsonl).
6. **Medida de SOGI:** a PNS 2019 mede só orientação (item Y8, 6 categorias) e não mede identidade de gênero; a PNDS 2023 é a primeira do IBGE com os dois. Para identidade de gênero o padrão oficial lido é o de duas etapas (NASEM 2022). Não resposta de orientação na PNS é 3,35% (comparável à NCVS 2016: 2,8%).

## 1. Contradição com o dossiê (achado de maior peso)

| Item do dossiê (simulacao/poder-survey.csv; §3, §9 #1) | Dossiê (AAS) | Corrigido (deff medido, PNS 2019) |
|---|---|---|
| LGB+ por rodada p/ detectar +10% de violência física | 9.481 | 48.434 |
| LGB+ por rodada p/ +20% | 2.461 | 12.571 |
| LGB+ por rodada p/ +30% | 1.133 | 5.787 |
| Adultos a triar p/ +30% (sem sobreamostra) | 59.948 | 305.955 (v0.3: arredondado uma vez; a versão anterior dividia o 5.787 já arredondado e dava 305.993) |
| Adultos a triar p/ +30% (com sobreamostra 5x) | 11.990 entrevistas | 305.955 triados; 65.820 completos |
| Variação detectável pela PNS 2019 observada (88.531 adultos, 1.554 LGB+ entrevistados) | "~25-30%" | 60,7% (física); 22,4% (qualquer violência); 99,9% (sexual 12 m) (v0.3: antes 58,3%, 21,6% e 95,7%, calculados com 1.674 = 88.531 x 1,89%, contagem esperada sob amostra autoponderada, não a observada) |
| Instrumento #1 do §9: "~60 mil entrevistas detecta 30%" | 60 mil | ~306 mil adultos |

A diferença de 3 unidades no n em AAS (9.484 contra 9.481) é a função de quantil; a fórmula é a do dossiê (duas proporções, alfa 5% bilateral, poder 80%, aumento relativo sobre p = 14,70%).

Sensibilidade ao deff (30%, física, LGB+, por rodada): contrafactual autoponderado (só a parte de conglomerado, deff_c = 1,52) 1.723; deff típico dos outros desfechos (3,5) 3.969; medido (5,1) 5.787; limite alto do bootstrap (6,4) 7.258. O deff do desfecho físico é o mais alto dos quatro (psicológico 3,49; qualquer 3,47; sexual 3,46) e tem o intervalo mais largo (bootstrap de UPAs, 500 réplicas: 2,6-6,4). Use 5,1 como central de projeto: o desenho recomendado (módulo PNADC, com metas por UF e 1 adulto sorteado por domicílio) herda as duas fontes de variação de peso da PNS. O 1,5 ("autoponderado") é um **contrafactual, não um piso alcançável**: só vale para um desenho só-nacional, sem estimativa por UF e entrevistando todos os adultos do domicílio (o que reabre proxy e privacidade).

## 2. As três opções, ordenadas

Parâmetros comuns: π(LGB+) = 1,89% dos adultos (PNS 2019); rendimento = 0,816 adulto com módulo por domicílio da amostra (88.531 / 108.458); desfecho: violência física 12 m entre LGB+ (14,70%); dois levantamentos independentes; alfa 5%, poder 80%. Capacidade de **um ciclo**:

| Opção | Domicílios | Adultos | LGB+ | Vítimas LGB+ (física / qualquer) | Variação detectável (física / qualquer) | Custo central | Faixa (R$) | R$ por LGB+ entrevistado |
|---|---|---|---|---|---|---|---|---|
| 1. Módulo PNAD Contínua, 1 ano | 337.600 | 275.573 | 5.212 | 766 / 2.170 | 31,7% / 12,2% | R$ 6,85 mi | 6,85 mi a 69,9 mi | 1.314 |
| 2. Rodada dedicada tipo PNS | 140.000 | 114.278 | 2.161 | 318 / 900 | 50,7% / 19,0% | R$ 29,0 mi | 25,3 mi a 32,7 mi | 13.418 |
| 3. Painel/web probabilístico (mesmo n da 2) | 140.000 | 114.278 | 2.161 | 318 / 900 | 50,7% / 19,0% | R$ 42,0 mi | 42,0 mi a 89,1 mi | 19.429 |

Fonte dos números: opcoes_resumo.csv (script cenarios_custo.py). Deff usado: o medido por desfecho (físico 5,11; qualquer 3,47). Para +30% em física o ciclo precisa de 305.955 adultos: Opção 1 = 1,11 ano (R$ 7,5 mi); Opção 2 = 374.821 domicílios (R$ 77,6 mi, faixa 67,8-87,5 mi); Opção 3 = R$ 112,4 mi. Tabela completa por desfecho, variação e base de deff: cenarios_n_custo.csv.

### Opção 1 — Módulo na PNAD Contínua (recomendada)

- **Desenho.** Módulo de morador selecionado (adulto 18+) com SOGI e violência, alocado em todas as visitas do 1º trimestre (211 mil domicílios) e só na 1ª visita nos três seguintes (~42 mil por trimestre): 337,6 mil domicílios por ano. A rotação 1-2(5) "possibilita alocação de um tema da pesquisa em todas as visitas de um determinado trimestre ou em determinada visita" (IBGE, notas metodológicas RDPC 2023, p.2; C12). Precedente de módulo com morador selecionado e perguntas sensíveis: "foi oferecida a opção de se fazer a entrevista por telefone mesmo quando o morador selecionado estivesse no domicílio" (IBGE, Nota Técnica 05/2022, p.2; C13).
- **n e deff.** 275,6 mil adultos, 5.212 LGB+. Deff 5,1 (2,6-6,4); o 1,5 autoponderado é contrafactual (§4). O deff é o da PNS 2019 (12-18 domicílios por UPA, pesos calibrados): a PNAD Contínua tem outros pesos e 14 domicílios por UPA (não medido aqui).
- **Custo central R$ 6,85 mi/ano (IPCA 2021-09 a 2026-09: x1,295).** Base: TED 02/2021 MJSP-IBGE, R$ 3.596.904,00 por um trimestre de dois módulos (R$ 2,82 mi de diárias, combustível e passagens + R$ 0,78 mi de TI não recorrente), ~211 mil domicílios: R$ 17,31 por domicílio-visita em R$ de set/2026 (C04-C09, C11). Segundo precedente independente: TED MDS-IBGE 2023, R$ 3.797.283,00 por um módulo temático (C10). **Faixa alta R$ 69,9 mi** = se o módulo exigisse visita própria ao custo por domicílio do TED da PNS (R$ 207).
- **Tempo.** Precedente medido: plano de trabalho com execução set/2021-set/2022, coleta out-dez/2021, Nota Técnica 05/2022 datada de 7/12/2022 (C04, C13): ~15 meses do TED aos primeiros dados.
- **Riscos de validade.** (a) Terceiros presentes: a PNS 2019 registrou privacidade não assegurada em 8,2% dos adultos e, nesse grupo, qualquer violência 14,2% contra 18,6% (associação observacional, não causal; sogi_modo.csv); (b) a PNAD Contínua não tem pergunta de SOGI documentada nos arquivos lidos: pré-teste obrigatório; (c) o módulo de violência precisa de protocolo de segurança (telefone) e de treinamento de 1.500 entrevistadores; (d) Parecer CEP/CONEP: ver §6; (e) deff transferido da PNS.
- **Variante sem precedente (não testada):** triar LGB+ no módulo e re-contatá-los na 5ª visita para um bloco aprofundado (motivação percebida, autor). Reduz o custo de sobreamostrar (o IBGE já achou os LGB+), mas depende de retenção entre visitas (não medida aqui) e de base legal para o re-contato (§6).

### Opção 2 — Rodada dedicada tipo PNS com módulo ampliado

- **Desenho.** PNS-like (DMC, morador selecionado), módulo de SOGI em duas etapas + violência com motivação percebida, autopreenchimento privado (a PNS 2019 deixa o "entrevistador" preencher em 71,7% dos adultos no módulo V; V1a), ~140 mil domicílios.
- **n e deff.** 114,3 mil adultos, 2.161 LGB+, 318 vítimas LGB+ de violência física: **serve para níveis e disparidades (razões de prevalência), não para tendência**. Sobreamostra por triagem não muda o custo de campo.
- **Custo central R$ 29,0 mi** (R$ 22,29 mi do TED "PNS-2024" corrigidos por IPCA de dez/2023: x1,136; dividido por 140 mil dá R$ 180,91 por domicílio, por 108,5 mil dá R$ 233,38). Faixa R$ 25,3-32,7 mi. **⚠️ O TED é minuta; objeto "PNS-2024"; valor final não verificado; exclui folha permanente do IBGE (naturezas 3390.14/30/33/36/39/40) e inclui R$ 2,72 mi de manutenção de veículos (C01-C03).**
- **Tempo.** PNS: minuta de dez/2023 (metadado 21/12/2023) para coleta em jul-nov/2026 (notícia, C33 ⚠️): ~31 meses até o campo, mais análise. PNS 2019: aprovação CONEP ago/2019.
- **Riscos.** Custo por LGB+ 10x o da Opção 1; ciclo de 3 a 7 anos entre PNS; a PNS 2026 está em campo e não consta que tenha SOGI ou violência (não verificado); PNDS 2023 já tem SOGI+gênero (133 mil domicílios; mulheres 15-49 e homens 15-59, logo exclui os mais velhos) e é gratuita por já coletada, mas sem resultados publicados até onde verifiquei (dados/pns_2024_status.md).

### Opção 3 — Painel/web probabilístico

- **Desenho.** Amostra probabilística de endereços/domicílios (idealmente a amostra-mestra do IBGE) com push-to-web e papel como em GSGB (Reino Unido), ou painel recrutado.
- **Custo central R$ 42,0 mi** para o mesmo n da Opção 2 (R$ 367 por completo: contrato GBP 4,5 mi / 19.714 respondentes por ano x 4 anos e 2 meses = GBP 54,8, PTAX GBP 6,7072; C29-C31). Faixa alta R$ 89,1 mi usando o preço do CSEW (GBP 116 por entrevista, face a face/misto, contrato de GBP 40,7 mi para ≥70 mil/ano x 5 anos; C22-C23). **Não há preço público brasileiro; é benchmark estrangeiro nominal.**
- **Deff.** Desconhecido para o Brasil; usei o da PNS. A direção do erro é conhecida: amostra de endereços sem conglomerado por setor e com até 2 adultos por endereço (GSGB, C30) reduz a parte de conglomerado e a de pesos, então o deff da PNS **superestima o n e o custo da Opção 3**, que fica mais barata do que mostra a tabela por um fator que não medi.
- **Tempo.** Não documentado para o Brasil. Referência estrangeira: GSGB, contrato assinado em 1/11/2025 e relatório do ano 2 com campo jan/2024-jan/2025 (C29, C30); sem precedente de base IBGE para push-to-web.
- **Riscos de validade.** Cobertura de internet (não quantificada com fonte primária aqui); resposta por endereço de 18-19% no GSGB (C30, GC técnico); autopreenchimento aumenta privacidade, mas o NHIS (§5) não achou efeito de modo na identidade sexual com cartão-resposta. **Survey online aberto (FRA EU-LGBTIQ III: EUR 800 mil, ~100 mil respostas, ~EUR 8 por resposta) não é probabilístico e não estima incidência.**
- **Quando vira a melhor:** se houver base de recrutamento que já traga SOGI (assim sobreamostrar LGB+ custa só o convite): custo de recrutamento não documentado.

### Raça e gênero (sem SOGI)

Com a Opção 1 (275,6 mil adultos) o módulo detecta, em violência física: mulheres 11,4%; negros (pretos+pardos) 8,6%; mulheres negras 12,2%; brancos 12,8%; e, em violência sexual 12 m: mulheres 24,9%; mulheres negras 21,9% (mde_outros_dominios.csv). O custo adicional para esses domínios é zero: o gargalo é LGB+.

### Por região (tabela n_regiao_custo.csv)

Para +30% (física, LGB+, sem sobreamostra), adultos a triar por região e por rodada: Norte 305.938; Nordeste 371.404; Sudeste 275.867; Sul 297.516; Centro-Oeste 327.288 (π regional da PNS 2019; baseline e deff nacionais, porque o deff regional de LGB+ varia de 1,2 a 4,0 com 205-458 LGB+ por região). Detectar variação regional exige ~1,6 milhão de adultos; nenhuma opção entrega isso em um ano. Resultado regional só é viável como acumulado de vários anos de módulo PNADC ou com resolução menor (±50%).

## 3. Custos documentados (custos-fontes.csv: 36 linhas, 35 verificadas no arquivo, 1 ⚠️)

Cada linha: valor, moeda, ano, URL, caminho local, página/seção, trecho verbatim, sha256 do arquivo; o script custos_fontes.py **confere que o trecho existe no texto extraído do arquivo local**.

| Programa | Valor | Moeda e ano | Id | Observação |
|---|---|---|---|---|
| IBGE, TED "PNS-2024" (MINUTA) | 22.291.444,00 | R$ 2023 | C01 | Naturezas de custeio; sem folha permanente do IBGE |
| IBGE/MJSP, módulos PNADC (patrimonial + percepção) | 3.596.904,00 | R$ 2021 | C04 | 1 trimestre; ~211 mil domicílios |
| IBGE/MDS, módulo PNADC | 3.797.283,00 | R$ 2023 | C10 | espelho Transferegov |
| CSEW (Inglaterra e Gales) | 18,3 mi; 28,8 mi; 34,1 mi; 40,7 mi | GBP 2018/2021/2022/2025 | C17-C23 | ≥70 mil entrevistas/ano a partir de 2024 |
| NCVS (EUA) | 36,0 mi (dotação FY2013, com redesenho); 160.040 pessoas | USD 2013 | C24-C25 | US$ 225 por pessoa entrevistada; R$ 1.128 nominal |
| FRA EU-LGBTIQ III (online aberto) | 800.000 | EUR 2022 | C26 | API do TED |
| FRA "Violence against Women Survey II" | 2.100.000 | EUR 2022 | C27 | escopo além do título não lido |
| StatCan SSPPS 2018 | ~9,6 mi ("roughly") | CAD 2019 | C28 | investimento total, não custo por entrevista |
| GSGB (push-to-web) | 4,5 mi | GBP 2025 | C29 | NatCen; 4 anos |

**Não encontrado em fonte primária** (cada um tem linha em fila-aquisicao.jsonl, com espaço de busca): custo da PNS 2019 (convênio de 2018 MS-IBGE); da PNDS 2023; do contrato da Pesquisa Nacional de Vitimização 2012 (Senasp/CRISP/Datafolha; o relatório do MJ de 288 páginas não traz valor); da Personal Safety Survey (ABS); da EU-GBV; de painéis probabilísticos (KnowledgePanel, AmeriSpeak, Datafolha/IBOPE: 6 buscas, API do USAspending sem preço por completo; PNCP varrido para o MJSP 2021-2026, 9.189 contratos, nenhum relevante, via pncp_busca.py; outros órgãos e o Portal da Transparência não varridos); da NCVS depois de 2013. Cifras que apareceram só em resumo de busca (R$ 30 milhões MS-IBGE para PNAD + PNDS + AMS; US$ 59 milhões BJS) **não foram usadas**.

## 4. Efeito de desenho (deff) da PNS 2019

Script: deff_pns2019.py (python3.14 -I, numpy e pandas). Desenho: estrato V0024 (574), UPA UPA_PNS (8.027), peso V00291 (morador selecionado, calibrado), 88.531 adultos 18+ com módulo V. Variância por linearização de Taylor de último conglomerado, sem fpc, subpopulação por zeragem.

**Validação (validacao.txt).** Reproduz as estimativas de Vasconcelos et al. 2023 em 7 de 7 e os **intervalos de confiança publicados** (Stata svy, IC logit) com diferença ≤ 0,01 ponto percentual, por exemplo violência física LGB+ 14,70% (11,15-19,13 contra 11,16-19,12 publicado) e LGB+ 1,89% (1,73-2,07). Isso valida a variância, não só o ponto. Conferência cruzada: jackknife de UPA dá erro-padrão com diferença relativa máxima de 0,64% (71 linhas) e 3,3% (regiões).

**Resultados principais (deff_pns2019.csv; deff_bootstrap_lgb.csv).**

| Indicador | Domínio | n | Estimativa | deff | deff só pesos (Kish) | deff conglomerado | Bootstrap de UPAs (2,5-97,5%) |
|---|---|---|---|---|---|---|---|
| LGB+ (prevalência) | adultos | 88.531 | 1,89% | 3,58 | 3,21 | 1,12 | 2,7-3,8 |
| Violência física 12 m | LGB+ | 1.554 | 14,70% | 5,11 | 3,36 | 1,52 | 2,6-6,4 |
| Qualquer violência 12 m | LGB+ | 1.554 | 41,63% | 3,47 | 3,36 | 1,03 | 2,6-3,7 |
| Violência sexual 12 m | LGB+ | 1.554 | 4,86% | 3,46 | 3,36 | 1,03 | 1,9-4,2 |
| Violência física 12 m | mulheres negras | 28.885 | 5,20% | 4,40 | 3,07 | 1,43 | n/d |
| Violência sexual 12 m | mulheres negras | 28.885 | 1,02% | 2,56 | 3,07 | 0,83 | n/d |

Leitura: ~2/3 do deff vem de **variação de pesos** (3,2-3,4). Ela decorre, ao que o desenho da PNS e da PNADC indica (inferência minha, não medida aqui), de alocação não proporcional por UF e da seleção de 1 adulto por domicílio, e a Opção 1 mantém as duas; só um desenho sem metas estaduais e com todos os adultos a reduziria. O resto é conglomeração, quase nula para LGB+ (1,03-1,52) porque há ~1,16 LGB+ por UPA. O ICC implícito não é identificável com tão poucos LGB+ por UPA e foi omitido para b < 2. O deff do desfecho físico entre LGB+ (5,11) está no extremo superior da incerteza (mediana do bootstrap 4,3).

**Limites.** (1) deff da PNS 2019, não de um desenho novo; (2) dois levantamentos independentes (a sobreposição de domicílios entre trimestres consecutivos da PNADC, se explorada, reduziria a variância da diferença: não modelada); (3) alfa 5% bilateral, um desfecho, sem correção de comparações múltiplas; (4) π constante: se a medida melhorar a revelação, π sobe e a triagem cai (com π = 3,26%, o de quem se autopreenche na PNS, +30% exigiria ~177 mil adultos; com 5,8%, o da GSS 2018, ~100 mil; ambos sensíveis a quem se revela e a se as vítimas são as mesmas); (5) cluster por UPA com 12-18 domicílios (PNS) é o que existe.

## 5. Medida de SOGI (texto integral lido)

**IBGE PNS 2019 (questionário, p.68 e 72; microdado).** V1 "Foi assegurada a privacidade para aplicação desse módulo?"; V1a "O questionário será preenchido por: 1. Próprio morador 2. Entrevistador". Y8 "Qual é sua orientação sexual?": Heterossexual, Bissexual, Homossexual, Outra, Não sabe, Recusou-se a responder (só 18+, módulo Y). Não há pergunta de identidade de gênero. Distribuição: 94,75% heterossexual; 1,89% LGB+ (0,68% bi; 1,15% homo; 0,06% outra); 1,08% "não sabe"; 2,28% recusou. Nota técnica: DMC (smartphone), seleção aleatória do morador adulto, aprovação CONEP em agosto/2019 (IBGE liv101846, Notas técnicas, p.28 do PDF).

**NASEM 2022, "Measuring Sex, Gender Identity, and Sexual Orientation" (páginas do leitor NAP).**
- Rec. 2 (p.11): "Which of the following best represents how you think of yourself? ... Lesbian or gay / Straight, that is, not gay or lesbian / Bisexual / ... I use a different term / (Don't know) / (Prefer not to answer)".
- Rec. 4 (p.12), duas etapas: "Q1: What sex were you assigned at birth, on your original birth certificate?" e "Q2: What is your current gender? ... Female / Male / Transgender / ... I use a different term / (Don't know) / (Prefer not to answer)". Racional: capta pessoas com experiência trans que não se identificam com o termo "transgender".
- Não resposta (p.79): em 2020, NHIS, BRFSS, Census Pulse e outras amostras probabilísticas, "all under 3 percent"; Tabela 5-1 (p.80): NCVS 2016, não resposta 2,8%, LGB 1,9%; GSS 2018, não resposta 1,9%, LGB 5,8%.
- Modo (p.79): Dahlhamer et al. 2014 "not statistically different" entre ACASI e CAPI; **proxy: "we did not yet have sufficient evidence to endorse the use of proxy reporting"**.
- Comparação PNS 2019: não resposta 3,35% (3,2% se a privacidade foi assegurada; 4,9% se não), LGB+ 1,89% (vizinho da NCVS 2016, não da GSS 2018).

**Viés de revelação com terceiros presentes: o que a literatura lida sustenta, e o que a PNS 2019 mostra (sem causa).**
- Dahlhamer, Galinsky e Joestl 2019 (J Official Statistics; quartil não verificado; split-ballot randomizado no NHIS, CAPI com cartão-resposta contra ACASI): "No significant main effects of interview mode on sexual minority identity reporting or nonresponse"; 2 efeitos significativos em 35 subgrupos; um deles, com preocupações de privacidade, foi maior no CAPI (3,5% contra 1,4%). Conclusão dos autores: CAPI com cartão não difere sistematicamente. Não resposta 2,7% (ACASI) e 2,3% (CAPI).
- Villarroel et al. 2006 (Public Opinion Quarterly; quartil não verificado; experimento randomizado, adultos 18-45, telefone com entrevistador contra T-ACASI): respondentes em T-ACASI relataram atração, experiência e contato genital com o mesmo sexo 1,5 a 1,6 vez mais (comportamento e atração, não identidade); efeito OR 2,5 em locais menos tolerantes e OR 3,0 em domicílios com crianças.
- **PNS 2019, associações observacionais (sogi_modo.csv):** LGB+ é 3,26% quando o próprio morador preenche o módulo V (n = 21.669) e 1,35% quando é o entrevistador (n = 66.862), e a razão persiste por faixa etária (18-29: 6,8% e 3,7%; 60+: 0,54% e 0,20%); a não resposta de orientação é o contrário: 7,1% contra 1,9%; violência qualquer 24,3% contra 15,9%. **Não é efeito de modo:** o preenchimento é escolhido na V1a (autosseleção por idade, escolaridade, familiaridade com o aparelho), o NHIS randomizado não encontrou diferença e Y8 não tem campo próprio de quem preencheu. O que a associação permite dizer: a PNS 2019 mistura dois regimes de coleta e um desenho novo deve randomizar o modo de preenchimento em subamostra para medir o viés.
- **IBGE:** PNAD Contínua 2021 oferece telefone ao morador selecionado quando há risco com terceiros (C13).
- ONS, Census 2021 (voluntária, 94% responderam; proxy mitigado por código individual ou formulário em papel): confirma que proxy e sensibilidade são o risco declarado.
- **Não lido (texto integral indisponível, ver fila-aquisicao.jsonl):** Tourangeau e Yan 2007 (Psychological Bulletin, Q1), Tate et al. 2013 (J Sex Res, Q1), AJE 2024 (duas etapas) e GenIUSS 2015. Nenhuma afirmação deste README depende deles.

**O que afeta validade e custo.** (1) pergunta de identidade, não comportamento; opções "não sabe" e "prefiro não responder" separadas; (2) autopreenchimento privado (ACASI/CAPI com cartão-resposta) em vez de pergunta falada; (3) sem proxy; (4) em PNS-like, o item entra depois de módulos neutros, e a violência vem antes ou depois da SOGI conforme o objetivo (ordem não testada aqui); (5) gênero em duas etapas custa 1 item a mais e permite contar pessoas trans; a prevalência esperada é baixa (~0,24% trans e não binário, SSPPS 2018, só por resumo de busca: não usar sem leitura) e exige amostra muito maior que a de orientação.

## 6. Marco legal e ético que condiciona o desenho (textos lidos na fonte)

| Norma | O que diz | Condiciona |
|---|---|---|
| Lei 13.709/2018, art. 5º II | dado sensível inclui "dado referente à saúde ou à vida sexual" (não nomeia orientação sexual nem identidade de gênero: enquadrar orientação em "vida sexual" é interpretação, não texto) | tratar SOGI como sensível por precaução |
| LGPD, art. 11, II, c e art. 5º XVIII | sem consentimento, "realização de estudos por órgão de pesquisa, garantida, sempre que possível, a anonimização"; órgão de pesquisa = entidade pública ou pessoa jurídica de direito privado sem fins lucrativos com missão de pesquisa "histórico, científico, tecnológico ou estatístico" | IBGE e universidade enquadram-se; entidade que não seja órgão de pesquisa (art. 5º XVIII), ou instituto comercial, precisa de consentimento específico (art. 11, I) |
| LGPD, art. 13 e §§ | dados tratados "exclusivamente dentro do órgão", "em nenhuma hipótese" divulgar dado pessoal; "não permitida, em circunstância alguma, a transferência dos dados a terceiro" (estudos em saúde pública) | linkage com Sinan/SIM/polícia só dentro de um órgão de pesquisa; sem repasse |
| Lei 5.534/1968, art. 1º e parágrafo único | resposta obrigatória ao IBGE; informações "terão caráter sigiloso, serão usadas exclusivamente para fins estatísticos" e "não servirão de prova em processo" | o levantamento do IBGE não pode servir para auditoria caso a caso; protege o respondente (ajuda a revelação); pesquisa de terceiros não tem esse escudo |
| Res. CNS 466/2012 e 510/2016 | 510, art. 1º, parágrafo único, IV dispensa "pesquisa censitária"; CONEP (Ofício-Circular 17/2022) define como a realizada pelo IBGE para quantificar populações; I dispensa "opinião pública com participantes não identificados" | PNS 2019 foi à CONEP (parecer 3.529.376, 23/8/2019, Vasconcelos); para o módulo PNADC com SOGI+violência não achei decisão: tratar como risco de prazo; painel com participantes identificados NÃO se enquadra no inciso I |
| Idade | módulos V e Y da PNS são 18+ | adolescentes ficam fora (PeNSE cobre escolares): limite de validade, não escolha técnica |

Cópia institucional (UFRGS) do Ofício-Circular 17/2022; original no site do CNS não aberto.

## 7. Becos e condições de volta

- Valor da PNS 2019, PNDS 2023 e PNV 2012: Portal da Transparência/Transferegov e DOU, só no Chrome real (fila-aquisicao.jsonl F2-05 a F2-08).
- PNS 2026: módulos de violência e SOGI desconhecidos; páginas do IBGE bloqueadas a curl/WebFetch (Cloudflare). Se a PNS 2026 tiver Y8 e módulo V, a Opção 2 vira "usar o dado de 2026" e o primeiro ponto de tendência só vem na PNS seguinte.
- Painéis probabilísticos: sem preço público achado; volta com cotação formal ou contrato público brasileiro.
- Quartil SJR de POQ e JOS: não verificado (Scimago só no Chrome real).
- O pedido citou o GSS de vitimização do StatCan; entreguei só o SSPPS 2018 (Question Period Notes). O GSS (Cycle de vitimização) não foi buscado: condição de volta = StatCan aberto no Chrome real.
- Descartado: usar R$ 30 milhões (MS-IBGE 2019) como custo de qualquer pesquisa; usar o custo por entrevista da NCVS 2013 como central do Brasil.

## 8. Como reproduzir

```bash
cd research-2026-10-21-rodada3/F2-custos
M=fontes/q1-textointegral/F2/pns2019
/opt/homebrew/bin/python3.14 -I deff_pns2019.py --micro $M/x/PNS_2019.txt --layout $M/input_PNS_2019_utf8.txt --out $PWD
/opt/homebrew/bin/python3.14 -I custos_fontes.py
/opt/homebrew/bin/python3.14 -I cenarios_custo.py
```

Microdado: https://ftp.ibge.gov.br/PNS/2019/Microdados/Dados/PNS_2019_20220525.zip (sha256 a789f6b0...6057); dicionário e input: Dicionario_e_input_20220530.zip (bcfed57f...78da); baixar.sh baixa com cabeçalhos de navegador (sem eles open.canada.ca e find-tender devolvem 403). A URL do TED só abre em www.ibge.gov.br (a do pedido, sem www, falha).

## 9. Arquivos

| Arquivo | Conteúdo |
|---|---|
| deff_pns2019.py | deff, validação, bootstrap, n, MDE, SOGI por modo |
| cenarios_custo.py | custo por opção, região, domínios |
| custos_fontes.py, custos-fontes.csv | custos com fonte, página, trecho, sha256 |
| deff_pns2019.csv, deff_regiao_lgb.csv, deff_bootstrap_lgb.csv | deff por indicador, região e incerteza |
| n_necessario.csv, mde.csv, cenarios_n_custo.csv, capacidade_por_opcao.csv, opcoes_resumo.csv | n, variação detectável, custo por cenário |
| n_regiao.csv, n_regiao_custo.csv, mde_outros_dominios.csv | região, raça e gênero |
| sogi_modo.csv | LGB+, não resposta e violência por modo de preenchimento, privacidade e idade (observacional) |
| validacao.txt | reprodução de Vasconcelos 2023 e denominadores |
| sources.jsonl, emite_ledger.py | ledger (40 registros), emitido por emit_sources.py |
| fila-aquisicao.jsonl | 22 itens para o navegador real ou agente de aquisição |
| baixar.sh, ted_api.py, pncp_busca.py | aquisição (cabeçalhos de navegador, API do TED, varredura do PNCP) |
| Arquivos baixados | fontes/q1-textointegral/F2/ (fora do git) |
