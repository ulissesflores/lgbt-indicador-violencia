# PLANO — Parte 2: "temos dados plausíveis para política pública?" (rascunho da coordenação do projeto, 2026-10-11)

Pergunta do autor (2026-10-11, literal, decomposta em frentes):
| # | Frente (palavras dele) | Tipo |
|---|---|---|
| F1 | "determinar se temos ou não dados plausíveis pra construir políticas públicas" | decidir |
| F2 | "se não, sugestões pra criar esses dados" | propor |
| F3 | "como separar tentativa política ideológica nesses dados, às vezes inflados por militância" | método |
| F4 | "casos de abuso feminino em que a mulher usa a criança como testemunha ... depois volta atrás dizendo que foi por ódio, vingança ou emocional" | investigar |
| F5 | "dados poluídos ajuda alguém? por que não resolvemos isso antes?" | explicar (economia política do dado) |
| F6 | "agentes haiku/sonnet em diversos âmbitos e nível global pra comparar" | executar |
| F7 | "simular os dados futuros como sempre faço" | simular |
| F8 | "aumento de violência contra mulheres, negros ou LGBT em governos de direita, país e estados" | investigar |
| F9 | "o que mais podemos abordar? falta algo?" | propor |

## Diagnóstico de partida (o que a Parte 1 já permite afirmar)
- A pergunta "existe dado?" tem resposta diferente por grupo. Mulheres e negros: o SIM (óbitos por sexo e raça/cor) é a melhor série do país, contínua desde 1996, comparável entre UFs. LGBT: só 1 ponto de prevalência (PNS 2019) e registros administrativos cuja variação 2022-2025 (783 -> 3.481) é de REGISTRO, não de incidência.
- Logo, o estudo não é "temos dados?", é "que decisão cada dado sustenta?" -> matriz de adequação ao uso (fitness-for-purpose).

## Ideias próprias (o que eu faria diferente de um levantamento comum)
1. **Matriz decisão x dado x dimensão de qualidade.** Linhas = decisões de política (dimensionar abrigo, alocar delegacia especializada, avaliar lei, treinar polícia). Colunas = fontes (SIM, Sinan, BO/Anuário, PNS, Disque 100, GGB/ANTRA). Células = 6 dimensões: cobertura, completude, validade do rótulo, comparabilidade no tempo (quebras legais: Lei 13.104/2015, ADO 26/2019, Lei 14.994/2024), independência de quem conta, verificabilidade (microdado aberto?). Veredito por célula, não um "sim/não" geral.
2. **Teste de independência de fonte (F3).** Um número só entra na política se >=2 canais INDEPENDENTES concordam na direção: registro administrativo, survey de vitimização (sem intermediário) e contagem militante. Complementos: (a) análise de sensibilidade à definição: recalcular a série do GGB/Anuário sob definição estreita e larga; se a manchete muda de sinal, é definição, não incidência; (b) teste de zeros cerimoniais: UF com 0 motivação = dado ausente, não ausência de crime; (c) definições de indicador pré-registradas e versionadas com changelog (o Anuário reviu 2023 de 2.090 p/ 1.633 e 2024 de 2.480 p/ 2.567 sem nota metodológica suficiente).
3. **F4 exige separar 3 fenômenos que o debate mistura** (TODOS os números abaixo são de memória: A VERIFICAR NA FONTE pelo agente A antes de entrar no dossiê): (i) alegação FALSA provada; (ii) alegação NÃO SUBSTANCIADA (não provada, não desmentida); (iii) RETRATAÇÃO (a vítima retira a denúncia). A literatura mundial mede (i) em 2-10% (Ferguson & Malouff 2016 meta: ~5%; Lisak 2010; CPS 2013) e (iii) em 30-60% nos processos de violência doméstica, por dependência econômica, medo e pressão, não por falsidade. Alegações de abuso infantil em disputas de guarda: Trocmé & Bala 2005 (Canadá, n=7.672): 4% intencionalmente falsas no geral, 12% em disputa de guarda, a maioria feita pelo genitor NÃO guardião. Brasil: NÃO existe medida nacional; proxies possíveis: retratação do art. 16 da Lei Maria da Penha nos TJs, denunciação caluniosa (art. 339 CP), processos de alienação parental (Lei 12.318/2010; status da revogação em 2026 a verificar), protocolo de depoimento especial (Lei 13.431/2017) e sugestionabilidade infantil (Ceci & Bruck; protocolo NICHD). Aviso crítico: a hipótese "a mulher usa a criança e depois recua por vingança" é uma narrativa específica; o desenho tem de MEDIR a taxa, não assumi-la. Proposta: auditoria de amostra de processos (TJSP/TJ de 3 UFs) com categorias mutuamente exclusivas.
4. **F8 como painel UF x ano (2010-2024).** Desfechos: taxa de homicídio de mulheres, de negros, feminicídio, notificações Sinan LGBT. Exposição: ideologia do governador (escala Power & Zucco / classificação partidária) + período federal (2019-2022). Desenho: evento/diferenças-em-diferenças com controles (renda, urbanização, armas) e COVID 2020-21 como confundidor explícito (sobrepõe o período federal e distorceu incidência e registro). O teste é SIMÉTRICO: ideologia como variável contínua/categórica em todas as direções, nunca pré-comprometido com o sinal "direita". Literatura de partida: "Trump effect" em hate crimes (Edwards & Rushin 2018; Müller & Schwarz), decretos de armas 2019 e feminicídio (Cerqueira), queda geral de homicídios 2018-2019. Dados: séries por UF baixáveis em https://www.atlasviolencia.ipea.gov.br (não parsear PDF) e microdados do SIM no TabNet/DATASUS; ideologia partidária: Power & Zucco (BLS) e Bolognesi, Ribeiro & Codato 2023 (Dados), a verificar. Aviso: o sinal não será simples (homicídios caíram em 2019-2022, feminicídio subiu em todos os governos).
5. **F7 simulação (identificabilidade).** Monte Carlo 2026-2030 da série REGISTRADA sob 3 cenários: incidência constante + registro subindo; incidência subindo; incidência caindo + registro subindo. Mostrar que os três geram a mesma curva registrada (não identificável) e calcular o n de um survey bienal de vitimização que separa os cenários (poder estatístico). Script Python com semente fixa, CSV + PNG no projeto.
6. **F5 economia política.** Hipóteses a documentar com fonte: registro policial serve à persecução, não à medição; 27 sistemas estaduais; o único survey nacional de vitimização GERAL foi a PNAD 2009 suplementar + a Pesquisa Nacional de Vitimização 2013 (Senasp/Crisp/Datafolha), nunca repetidos; para mulheres existe a série FBSP/Datafolha "Visível e Invisível" desde 2017 (muda o veredito de F1 para mulheres); sociedade civil preenche o vácuo com números de advocacy citados como oficiais; polarização faz cada lado preferir o seu número (zeros cerimoniais de um lado, inflação do outro). Literatura: Best "Damned Lies and Statistics"; Andreas & Greenhill "Sex, Drugs and Body Counts" (2010); Merry "The Seductions of Quantification" (2016); Mills/Lantz/Wenger 2024.
7. **F9 o que falta (minhas adições):** (a) violência contra HOMENS como denominador (90%+ dos homicídios), senão "violência contra X" não tem base de comparação; (b) qualidade do campo raça/cor nos BOs (ignorado); (c) quebras de série por mudança de lei tratadas explicitamente; (d) piloto de LINKAGE SIM-Sinan-SSP como padrão-ouro (microdados DATASUS abertos); (e) governança: definição versionada + dados abertos + auditoria externa; (f) LGPD para atributos sensíveis; (g) custo do dado ruim (orçamento mal alocado).

## Execução proposta (barata)
| Agente | Modelo | Frente | Entrega |
|---|---|---|---|
| A | Sonnet | F4 literatura Q1 (falsas alegações, retratação, testemunho infantil, alienação parental) | briefing + ledger |
| B | Haiku | F4 Brasil oficial (CNJ, TJs, Lei 12.318 status 2026, art. 16 LMP, depoimento especial) | briefing + ledger |
| C | Sonnet | F8 literatura (Trump effect, Bolsonaro, armas, ideologia de governadores) | briefing + ledger |
| D | Haiku | F6 inventário global (surveys de vitimização c/ motivação, registro policial obrigatório, estatísticas oficiais de falsa alegação) | tabela + ledger |
| E | Sonnet | F3/F5 literatura (política dos números, qualidade de dado em hate crime, quebras de série) | briefing + ledger |
| F | Haiku | F8 dados: séries por UF do portal do Atlas/IPEA + TabNet SIM -> CSV; governadores 2011-2026 por partido; conferir se a PNS 2024/25 repete a pergunta de orientação sexual (2º ponto de prevalência LGBT) | CSV |
| coordenação | aqui | simulação F7, matriz F1, síntese, quartis Scimago (Chrome), advisor, dossiê | DOSSIE-2026-10-11-parte2.md |

Custo: 6 agentes baratos em paralelo (~1-2 h); julgamento e síntese nesta sessão.

## Regras de execução
- Saída em research-2026-10-11/; ledger SÓ via emit_sources.py; cada filho grava em disco e devolve caminhos + linha `Becos:`; sem subagente aninhado.
- Nenhum número de literatura entra no dossiê sem conferência na fonte (pdftotext/abstract).

## Status
- 2026-10-11: plano apresentado e APROVADO (+F10); 7 agentes + D2 executados; dossiê DOSSIE-2026-10-11-parte2.md montado; advisor final consultado (7 ajustes aplicados).

## F10 (adendo do autor, 2026-10-11, aprovado o plano): "morreu PORQUE é X" x "pessoas X morrem por n outros fatores" — e os grupos mais seguros
Pedido literal: "o mais importante é distinguir. Morreu porque é mulher / negro / lgbt / homem / branco ou morreu esses tipos de pessoas por conta de n outros fatores. Separar com clareza e de forma científica a afirmação que o indivíduo morre por pertencer a uma classe do indivíduo é morto por crime passional e etc. e depois determinar os grupos mais seguros."

Taxonomia causal em 4 níveis (cada nível = pergunta diferente, dado diferente, método diferente):
| Nível | Pergunta | Quantidade | Dado que responde | Método |
|---|---|---|---|---|
| N1 Incidência | Quantos de cada grupo morrem? | taxa por 100 mil, padronizada por idade | SIM (sexo, raça/cor); LGBT: numerador GGB/Sinan x denominador PNS (1,89%) | descritivo; ranking = "grupos mais seguros" no sentido DESCRITIVO |
| N2 Risco atribuível ao pertencimento | Se a mesma pessoa não fosse X, morreria igual? | diferença de risco ajustada por idade, renda, local, ocupação, horário | microdados SIM + Censo/PNAD | decomposição Oaxaca-Blinder, pareamento, mediação (ex.: Cerqueira & Coelho, IPEA, jovens negros SP) |
| N3 Contexto do crime | Em que circunstância? (íntimo/familiar, roubo, conflito, execução, policial) | distribuição de contexto por grupo | BO/inquérito; UNODC (parcela de mortes de mulheres por parceiro/família ~ vs homens) | assimetria de contexto como PROXY de padrão de gênero sem campo de motivação |
| N4 Motivação do agressor | O agressor agiu POR CAUSA do atributo? | parcela com motivação de viés comprovada | campo de motivação (Sinan 55, BO LGBTfobia, inciso II do feminicídio), indicadores de viés (ODIHR), confissão/símbolos | só é bem definida como "a PERCEPÇÃO do atributo pelo agressor causou o ato" (Greiner & Rubin 2011; Holland 1986) |
Observações: (a) a Lei 13.104/2015 mistura N3 (inciso I: violência doméstica e familiar) e N4 (inciso II: menosprezo à condição de mulher) na MESMA estatística de feminicídio; (b) "crime passional" é N3 íntimo, e só vira N4 se houver evidência de motivação pelo atributo; (c) "grupos mais seguros" só é respondível em N1 e N2, nunca a partir de N4.
Agente G (Sonnet): literatura de N2-N4 + cálculo ilustrativo do limite inferior da taxa LGBT (numerador GGB x denominador PNS) no dossiê.
