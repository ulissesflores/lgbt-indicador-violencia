# Briefing B (f4 Brasil oficial): qualidade dos dados de violência no Brasil

Data da pesquisa: 2026-10-11. Playbook: factual-context (canal Wikipedia/Wikidata do playbook não se aplica a fontes oficiais; mantidas a tag de proveniência e a política de retry).
Ledger: `research-2026-10-11/sources.jsonl`. Registros desta frente (origem factual-context): 14, 0 rejeitadas. O arquivo tem 28 linhas no total porque outras frentes gravaram no mesmo ledger durante a rodada.

Legenda de proveniência nas tabelas: F = página lida diretamente (WebFetch com resposta); S = trecho de resumo de busca ou reportagem secundária, não conferido na fonte primária.

## Limites desta rodada (ler antes dos números)

- planalto.gov.br não respondeu (ECONNRESET no WebFetch e no curl, 4 tentativas). Nenhum texto de lei foi lido na fonte primária. Mirrors testados: lexml (página do Senado com verificação de conexão, sem o texto), normas.leg.br (página sem texto consolidado), web.archive.org (302, não seguido). Lei 15.380/2026 e a consolidação da Lei 12.318 seguem sem leitura primária.
- camara.leg.br e senado.leg.br foram lidos diretamente via WebFetch (F).
- CNJ (cnj.jus.br/programas-e-acoes/violencia-contra-a-mulher/) respondeu 403 ao WebFetch. Painel de Monitoramento e Justiça em Números não acessados.
- IBGE (ibge.gov.br/.../29540-pesquisa-nacional-de-saude.html) respondeu 403 ao WebFetch. Confirmação primária da ausência de PNS 2024 não obtida.
- FBSP Anuário 2026: PDF oficial confirmado por HEAD (HTTP 200) em `https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf`, baixado em `fontes/p2-f4-brasil-oficial/anuario-2026.pdf`, SHA-256 `9c202ab77fdf81c92f8154db027ccfd7e9db539e0cbce854be7cd97b90f01f88`. Os números vêm do texto local extraído antes desta rodada, `fontes/t2-anuario-2026-dados2025/anuario.txt`, e foram conferidos por leitura das tabelas.
- Painel do Disque 100 (gov.br/mdh) não foi acessado. Os números do item 7 vêm de reportagens (S).

## 1. Lei 12.318/2010 (alienação parental): status em 2026

**Achado central: a lei continua em vigor. Há dois projetos de revogação, em estágios diferentes.**

| Fonte | Número | Dado | Trecho verbatim | URL | Data |
|---|---|---|---|---|---|
| Senado (F) | PL 1372/2023, autor Sen. Magno Malta | Situação atual | "Em tramitação" | https://www25.senado.leg.br/web/atividade/materias/-/materia/156451 | última movimentação 22/08/2023 |
| Senado (F) | PL 1372/2023 | Ementa | "Revoga a Lei nº 12.318, de 26 de agosto de 2010, que dispõe sobre a alienação parental." | idem | idem |
| Senado (F) | PL 1372/2023 | Estado da última movimentação | "22/08/2023 - AGUARDANDO DESIGNAÇÃO DO RELATOR" | idem | idem |
| Câmara (F) | PL 2812/2022, rel. Laura Carneiro (PSD-RJ), apenso PL 642/2024 | CCJ aprova revogação | "Em votação nominal, foi aprovado o parecer da relatora ... por 37 votos a favor e 28 contra." | https://www.camara.leg.br/noticias/1229444-COMISSAO-DE-CONSTITUICAO-E-JUSTICA-APROVA-REVOGACAO-DA-LEI-QUE-TRATA-DA-ALIENACAO-PARENTAL | 2025-12-03 (o texto diz "quarta-feira (4)", data inconsistente) |
| Câmara (F) | PL 2812/2022 | Tramitação | "tramita em caráter conclusivo e pode seguir para análise do Senado." | idem | idem |

Leitura:

- PL 1372/2023 (Senado) está parado desde 2023, aguardando designação de relator, segundo a página do Senado lida hoje. Trata-se de dado de página, não de confirmação de inatividade.
- PL 2812/2022 (Câmara) foi aprovado na CCJ em dezembro de 2025, em caráter conclusivo. Depois disso só há notícia de expectativa de tramitação no Senado em 2026 (secundária, sem data de confirmação). Estágio posterior a dezembro de 2025 não verificado.
- Lei 14.340/2022: NÃO VERIFICADA. Não encontrei fonte que confirme se alterou a Lei 12.318. Não afirmo nem nego.
- Lei 15.380/2026 (6 de abril de 2026): altera a Lei Maria da Penha (art. 16) para restringir a audiência de retratação aos casos em que a vítima a solicita expressamente antes do recebimento da denúncia. Fonte: https://www.lex.com.br/lei-no-15-380-de-6-de-abril-de-2026/ (secundária; planalto não acessível). Relevante para a pergunta 2 e não para a 12.318.
- CNJ: não encontrei recomendação ou resolução do CNJ específica sobre alienação parental. A Resolução CNJ 492/2023 (17/03/2023) torna obrigatório o Protocolo para Julgamento com Perspectiva de Gênero (antes Recomendação CNJ 128/2022). Fonte secundária: https://www.tjpr.jus.br/ (informativo) e material de curso. Não verifiquei no ato original (atos.cnj.jus.br). Não encontrei menção específica a alienação parental no texto do protocolo. Há tentativa legislativa de anular a resolução (PDL 89/2023, status não verificado).

## 2. Art. 16 Maria da Penha (retratação) e estatísticas de retratação/arquivamento

**Achado: não encontrei estatística oficial de retratações ou de arquivamentos por retratação (CNJ, TJSP, MP). Ausência registrada como achado.**

- Jurisprudência (secundária, não verificada no acórdão): STJ, Tema 1.167 (recurso repetitivo), "a audiência prevista no artigo 16 da Lei 11.340/2006 tem por objetivo confirmar a retratação, não a representação, e não pode ser designada de ofício pelo juiz." Fonte: https://jus.com.br/artigos/20053/jurisprudencia-comentada-do-superior-tribunal-de-justica-art-16-da-lei-maria-da-penha
- A ADI 4424 (STF 2012) e a Súmula 542 STJ não foram conferidas na fonte nesta rodada.
- Controvérsia: a Conamp questionou no STF a leitura de que a ausência da vítima equivale a renúncia tácita, com efeito de arquivamento (secundária).
- Painel CNJ de Monitoramento e Justiça em Números 2025/2026: NÃO CONSULTADOS. A busca não retornou os painéis. Sem dados de casos novos ou medidas protetivas concedidas nesta rodada.
- Dados do Anuário 2026 (lidos localmente, ver item 5): feminicídios com MPU ativa no momento do óbito, Tabela 22: Brasil 67 em 2024 e 70 em 2025. Registros de descumprimento de MPU (art. 24-A), Tabela 27: 112.695 em 2024 e 132.025 em 2025, +16,7%, taxa 53,0 e 61,9 por 100 mil.

Descumprimento de MPU, texto do Anuário (linha 7734 do txt): "Brasil e Unidades da Federação – 2024-2025 ... Brasil 112.695 132.025 53,0 61,9 16,7". Nota (1): "O crime de descumprimento de medida protetiva de urgência foi incluído na Lei Maria da Penha (lei 11.340/2006) em 2018, pela lei 13.641."

Anuário, texto do capítulo (linha 1097): "Mesmo diante da queda dos homicídios em geral, os feminicídios continuam crescendo. ... especialmente diante da persistência da violência doméstica e do aumento do descumprimento das medidas protetivas."

## 3. Lei 13.431/2017 (depoimento especial / escuta protegida)

- Resolução CNJ 299/2019: data citada em fonte secundária como 05/11/2019. Art. 7 (obrigação de salas em todas as comarcas) e art. 8 (protocolo, Protocolo Brasileiro de Entrevista Forense). Fonte: https://www.tjes.jus.br/institucional/coordenadorias/coordenadoria-da-infancia-e-da-juventude-2/depoimento-especial-lei-no-13-431-2017/ (página sem data, lida por busca).
- Exemplo estadual (TJES, página sem data): 13 comarcas com sala em funcionamento; cinco salas autorizadas para o interior.
- Número nacional de salas: NÃO ENCONTRADO. Sem painel CNJ consultado.
- Avaliação oficial do depoimento especial: NÃO ENCONTRADA. Achado de ausência.
- Distinção "escuta especializada" x "depoimento especial": contestada, sem fonte oficial confirmada.

## 4. Denunciação caluniosa (art. 339 CP) e comunicação falsa de crime (art. 340)

**Achado: nenhuma estatística oficial encontrada (Anuário FBSP, SSP-SP, TJ). Ausência registrada.**

- Art. 339 (denunciação caluniosa) foi alterado pela Lei 14.110/2020 (secundária, 18/12/2020).
- Art. 340 (comunicação falsa de crime): distinção do art. 339 é a indicação de pessoa determinada como autora (secundária).
- Nenhum número de inquéritos, processos ou condenações foi localizado em fontes oficiais nesta rodada. Não consultei SINESP nem painéis estaduais de SSP.

## 5. Anuário Brasileiro de Segurança Pública 2026 (dados 2025)

Edição: 20ª, lançamento em 23/07/2026 (secundária: O Povo, https://www.opovo.com.br/noticias/brasil/2026/08/06/amp/feminicidios-seguem-em-alta-20-anos-apos-lei-maria-da-penha.html). Texto local: `fontes/t2-anuario-2026-dados2025/anuario.txt`.

| Indicador | 2024 | 2025 | Variação | Fonte no Anuário |
|---|---|---|---|---|
| Feminicídios (vítimas, Brasil) | 1.504 | 1.571 | +4,0% | Tabela 21, pág. 149 |
| Taxa de feminicídio (por 100 mil mulheres) | 1,4 | 1,4 | | Tabela 21 |
| Homicídios de mulheres (incl. feminicídios) | 3.728 | 3.539 | -5,5% | Tabela 21 |
| Proporção feminicídio/homicídio de mulheres (%) | 40,3 | 44,4 | | Tabela 21 |
| Vítimas de feminicídio com MPU ativa no óbito | 67 | 70 | | Tabela 22 |
| Registros de descumprimento de MPU (art. 24-A) | 112.695 | 132.025 | +16,7% | Tabela 27, pág. 155 |
| Lesão corporal dolosa, violência doméstica, vítimas mulheres | 277.916 | 286.270 | +2,6% | Tabela 24, pág. 152 |
| Ameaça, vítimas mulheres | 781.162 | 788.531 | +0,5% | Tabela 25, pág. 153 |
| Estupro (total, Brasil) | 20.551 | 19.398 | -6,0% | Tabela 29, pág. 181 |
| Estupro de vulnerável (total, Brasil) | 68.292 | 64.990 | -5,2% | Tabela 29 |
| Estupro, vítimas mulheres | 18.944 | 18.018 | -5,3% | Tabela 30, pág. 183 |
| Estupro de vulnerável, vítimas mulheres | 59.197 | 56.065 | -5,7% | Tabela 30 |

Revisão do dado de 2024 (achado de qualidade de dado): a edição anterior (Anuário 2025, dados 2024, texto em `fontes/t2-anuario-2025-dados2024/anuario.txt`, linha 7612) traz "No total do ano, foram 1.492 mulheres. É o maior número já observado desde 2015". A edição 2026 traz 1.504 para 2024 (Tabela 21, nota 3: "Atualização das informações publicadas no Anuário Brasileiro de Segurança Pública, ano 19, 2025"). A diferença de 12 casos é revisão posterior de dado, confirmada pelo próprio Anuário. Os valores de 2024 mudam entre edições; comparar sempre dentro da mesma edição ou usar a versão atualizada.

Descumprimento de MPU e feminicídio com MPU ativa são indicadores diferentes: o primeiro conta registros do crime; o segundo conta vítimas de feminicídio que tinham medida ativa no momento do óbito (70 em 2025, Tabela 22). A pergunta de retratação não pode ser respondida com nenhum dos dois.

Nota de método (Anuário, Tabela 21, nota 1, verbatim): "Em 2024, a Lei nº 14.994, de 9 de outubro, atualizou a figura do feminicídio, transformando-o em crime autônomo. Neste relatório, seguimos incluindo os feminicídios no total de homicídios dolosos para preservar a comparabilidade histórica."

Estupro (Anuário, Quadro 06, texto local linha 9975): "a variável raça/cor possui alto índice de Não Informado (NI), com ausência de dados em 31,8% dos boletins de ocorrência." Relação vítima-autor sem informação: 80,0% (mesmo quadro).

Completude de raça/cor (Anuário, texto local linha 8164, feminicídios): "raça/cor da vítima (13,1% de não preenchimento) e, sobretudo, relação entre vítima e autor, cujo percentual de ausência alcançou 74,8% dos feminicídios e 89,4% das demais mortes violentas intencionais de mulheres."

Completude em outro bloco (linha 14044, verbatim): "em apenas 65,6% dos boletins foi preenchido o perfil étnico-racial; o local do crime foi registrado como não informado em 8,7% dos casos (em 2024 havia sido 1,6%); e 79,6% dos registros não informam a relação entre vítima e agressor." Este trecho não identifica no texto extraído a tabela exata; tratar com cautela.

Medidas protetivas concedidas (número de concessões): NÃO EXTRAÍDO nesta rodada. Grep sem resultado tabular. Pendente.

Estatística de vítimas de feminicídio com MPU: 70 em 2025 (Tabela 22). Trecho de matéria secundária cita "70 mulheres ... 8,8% dos 797 casos" em 18 UFs, e nove UFs sem informação. Não verificado no texto do Anuário.

Observação do Anuário (linha 1097): queda de estupro em 2025 "pode refletir mais a diminuição da capacidade de denúncia e não necessariamente redução da incidência".

## 6. Surveys de vitimização

| Survey | Ano | Órgão | Amostra / método | O que mede | Fonte | Status |
|---|---|---|---|---|---|---|
| PNAD suplemento vitimização | 2009 | IBGE | PNAD domiciliar | Violência e acesso à justiça (primeiro suplemento de vitimização) | https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/13723-asi-ibge-da-inicio-a-coleta-da-pnad-2009 | lido via busca |
| Pesquisa Nacional de Vitimização | 2013 | Senasp/Crisp (não confirmado) | não verificado | não verificado | FBSP 2025 (secundária) menciona apenas "uma pesquisa grande ... em 2012" pelo MJ | NÃO CONFIRMADA |
| PNS módulo acidentes e violência | 2013 | IBGE | 81.767 domicílios (FBSP) | Acidentes e violência | secundária | parcial |
| PNS | 2019 | IBGE | não lido | Orientação sexual (primeira vez na PNS), violência física/sexual | BNews https://www.bnews.com.br/noticias/saude/ibge-inicia-coleta-de-dados-para-pesquisa-de-saude-da-populacao.html | secundária; resultados de orientação divulgados em 2022 (94,8% heterossexual, 1,2% homossexual, 0,7% bissexual, segundo BNews) |
| PNS | 2026 | IBGE | em coleta (DF termina em 30/11) | não verificado | Correio da Manhã DF, jul/2026 | secundária |
| PNDS | 2023 | IBGE + Min. Saúde (SAPS) | não lido | Primeiro IBGE a perguntar orientação sexual e identidade de gênero | BNews (secundária); plano de trabalho TED 119/2023 https://ibge.gov.br/np_download/novoportal/documentos_institucionais/ted/Plano_de_Trabalho_TED_119_2023_PNS.pdf | análise e publicação previstas até maio de 2027 (dado do plano, não confirmado) |
| Visível e Invisível (5ª ed.) | 2025 (campo 10-14/fev/2025; publicado 2026) | FBSP + Datafolha | 1.040 mulheres 16+, 126 municípios; 793 no subgrupo de vitimização; erro de 3 p.p. | Vitimização de mulheres nos últimos 12 meses: 37,5% (~21,4 milhões); parceiro/ex-parceiro 19,4% (2017) -> 40% (2025) | https://forumseguranca.org.br/publicacoes/visivel-e-invisivel-5ed/ (via busca, não lido na íntegra) | secundária |
| Visível e Invisível | 2017, 2019, 2021, 2023 | FBSP + Datafolha | não verificado | não verificado | hub https://forumseguranca.org.br/visivel-e-invisivel/ (F) lista só a 5ª edição (2025); edições anteriores não aparecem | NÃO VERIFICADA |

Visível e Invisível 5ª edição, dados do hub (F) e do resumo de busca (S): o hub traz os links do Relatório Final (https://forumseguranca.org.br/wp-content/uploads/2025/03/relatorio-visivel-e-invisivel-5ed-2025.pdf), do Sumário Executivo e do infográfico. Campo e n estão no relatório final, não lido. Os números de amostra (1.040 e 793) e de prevalência (37,5%) vêm de resumo de busca (S).

Correção ao pressuposto da pergunta: NÃO HÁ PNS 2024 no que foi localizado (S). Os ciclos encontrados são 2013, 2019 e 2026 (em coleta). A pergunta sobre orientação sexual em 2024/2025 aparece na PNDS 2023 (IBGE + Min. Saúde), não na PNS. Confirmar na página oficial do IBGE: https://www.ibge.gov.br/estatisticas/sociais/saude/29540-pesquisa-nacional-de-saude.html. Tentativa de leitura: 403 (bloqueio ao WebFetch), não confirmado.

## 7. Disque 100 / Ligue 180 (dados 2024-2025)

| Canal | Dado | Trecho / número | Fonte | Data |
|---|---|---|---|---|
| Disque 100 (LGBTQIA+) | Denúncias LGBTQIA+ no painel | 1.762 denúncias e 9.868 violações (Brasil) | Bahia Notícias (cita painel divulgado em janeiro): https://www.bahianoticias.com.br/noticia/303329-bahia-contabiliza-148-denuncias-e-mais-de-900-violacoes-de-direitos-contra-a-populacao-lbgtiqa-em-2025 | 2026 (período exato não especificado) |
| Disque 100 (LGBTQIA+) | Participação no total de ocorrências | 1,17% em 2025 | Juiz de Fora (secundária) | 2026 |
| Disque 100 (LGBTI+) | 2024 | "mais de 7 mil denúncias", 1.506 de pessoas trans e travestis | notícia (MPF citado) | 2025 |
| Disque 100 (LGBTI+) | 1º trimestre de 2025 | ~1.700 denúncias de vítimas LGBTI+ | MPF (via busca) | 2025 |
| Ligue 180 (mulheres) | 1/jan a 31/jul de 2025 | 86.025 denúncias de violência contra mulher | https://www.opovo.com.br/noticias/brasil/2025/08/07/ligue-180-recebe-86-mil-denuncias-de-violencia-contra-mulher-ate-julho.html | 2025-08-07 |

Achados e ressalvas:

- Os números do Disque 100 LGBTQIA+ são inconsistentes entre si em escala: 1.762 (2025, painel) x "mais de 7 mil" (2024). Não reconciliado. Não usar sem checar o painel.
- O painel da Ouvidoria Nacional (MDHC) não foi consultado. Segundo notícia, passou a ser atualizado trimestralmente e perfis de vítimas e suspeitos saem por LAI.
- Comparativo com 2022 não é possível: o formulário do Disque 100 tinha só a opção "homossexual" (secundária, citada por MDHC).

## Becos (o que não existe ou não foi acessível)

- planalto.gov.br: inacessível (ECONNRESET, 4 tentativas). Textos de lei não lidos na fonte primária.
- Lei 14.340/2022 e alteração da Lei 12.318: não verificada.
- CNJ: painéis de Monitoramento (Maria da Penha) e Justiça em Números 2025/2026 não acessados.
- Recomendação ou resolução do CNJ sobre alienação parental: não encontrada.
- Estatística de retratação/arquivamento por retratação (CNJ, TJSP, MP): não encontrada.
- Número nacional de salas de depoimento especial e avaliação oficial: não encontrado.
- Estatística de denunciação caluniosa (art. 339) e comunicação falsa (art. 340): não encontrada.
- Número de concessões de medidas protetivas no Anuário 2026: não extraído.
- Pesquisa Nacional de Vitimização 2013 (Senasp/Crisp): não confirmada.
- Visível e Invisível 2017, 2019, 2021, 2023: não localizadas.
- PNS 2024: não existe no levantamento (há PNS 2019 e PNS 2026 em coleta).
- Painel do Disque 100 em gov.br/mdh: não acessado.
- Número de medidas protetivas CONCEDIDAS no Anuário 2026: não extraído. Pendente de grep nas tabelas do PDF local (`pdftotext -layout ... -`).
- Lei 15.380/2026: texto primário não acessado (planalto, lexml e normas sem texto). Único registro é o resumo do lex.com.br (S). Tratar como hipótese até conferir no planalto.
- CNJ e IBGE: tentativas bloqueadas com 403 ao WebFetch. Não confirmados na fonte.
- Ligue 180 e Disque 100 de 2025 em painel oficial: não acessado.
- STF ADI 4424 e Súmula 542 STJ: não conferidas na fonte nesta rodada.
