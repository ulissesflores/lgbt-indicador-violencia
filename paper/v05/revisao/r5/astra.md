# Parecer — GPT-6 Astra (gpt-6-astra)

## Avaliação geral

O artigo contribui ao distinguir violência relatada, registro administrativo, mortalidade e motivação, com linguagem geralmente acessível e documentação extensa.
Recomendo **revisão maior**: há omissões relevantes sobre a codificação do GGB e discrepâncias entre os métodos executados e as interpretações publicadas.
As verificações realizadas não identificaram erro que derrube o contraste principal da PNS; os problemas encontrados exigem correções localizadas, não rejeição integral.
O trabalho é adequado a um preprint metodológico, desde que essas correções alcancem também tabelas, figuras e Material Complementar.
Examinei as oito figuras principais, conferi o selo vigente e executei testes selecionados: **157 passaram e 3 foram ignorados**, sem acessar a internet ou alterar arquivos.
Reexecução a partir dos microdados brutos e confirmação direta das fontes primárias ausentes: **não verificado**.

## Críticas

### AST-01 — Concordância da auditoria do GGB omitida
- Local: Seções 2.6, 3.5 e 5; MC5, validação dos 160 casos.
- Trecho ou alegação: “Modelos participaram, porém, da codificação dos discursos”.
- Problema: A participação dos modelos não se restringiu aos discursos. A auditoria do GGB também depende de codificação por modelos, cuja concordância foi medida, mas não apresentada no artigo nem no MC5. Isso omite uma informação diretamente pertinente às classificações que produzem os 73 casos de morte violenta e os 50 casos verificáveis.
- Evidência ou raciocínio verificável: `docs/laudos/F3-ggb-README.md`, seção “Concordância entre codificadores”, identifica Claude Sonnet e Gemini como codificadores. `research-2026-10-21-rodada3/F3-ggb/dados/kappa.json` registra 23 casos duplamente codificados; para morte violenta, 21 pares válidos, concordância de 90,5% e κ = 0,462. Dois desacordos envolvem causa indeterminada versus morte violenta. Para identificação LGBT+, κ = 0,912.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Declarar essa utilização dos modelos; apresentar concordância por variável, seleção dos casos duplamente codificados e procedimento de adjudicação. Mostrar eventual efeito dos desacordos sobre as contagens. Explicitar que Wilson quantifica incerteza amostral, não erro de classificação.
- Incerteza: κ baixo com concordância bruta alta não prova classificação ruim, especialmente com categorias desequilibradas. O acerto caso a caso, sem o vínculo nominal às fontes, permanece **não verificado**.

### AST-02 — Denominador e ausência de informação no Sinan
- Local: Seção 3.2, parágrafo sobre o Sinan; Figuras 1 e 6; Tabela 2, linha 12.
- Trecho ou alegação: “Cada coluna do painel a soma 100% das fichas do ano”.
- Problema: As porcentagens não usam todas as fichas: excluem aquelas marcadas como autoprovocadas. Além disso, os 42,5%–44,5% somam ignorado, branco e “não se aplica”; não representam simplesmente campo vazio, como afirma a Figura 1. A distinção altera a descrição do problema de preenchimento.
- Evidência ou raciocínio verificável: `dados/sinan/serie_campo55_uf_ano.py:24` exclui `LES_AUTOP == "1"`; as linhas 29–37 distinguem `m_ign_branco` e `m_nao_se_aplica`. `dados/sinan/resumo.md` informa, para 2025, 29,72% ignorado/branco e 14,75% “não se aplica”, totalizando aproximadamente 44,5%. Para 2023, o denominador analisado é 405.941, enquanto o total de notificações é 588.388.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Identificar consistentemente o universo como notificações não marcadas como autoprovocadas, esclarecendo o tratamento de respostas desconhecidas. Separar ausência estrita de informação e ausência efetiva, justificando a inclusão do código “não se aplica” nesta última.
- Incerteza: A deficiência informacional permanece. Não foi demonstrado que essa correção altere a conclusão sobre a impossibilidade de estimar incidência motivada.

### AST-03 — Deslocamento ideológico não é troca entre blocos
- Local: MC6, estudo de eventos; Tabela MC6.A10 e Figura MC6.18.
- Trecho ou alegação: “−20% da esquerda para a direita”.
- Problema: O programa classifica qualquer aumento do escore como “esquerda para direita”, inclusive transições entre partidos já situados à direita. O contraste estimado não corresponde ao contraste político anunciado.
- Evidência ou raciocínio verificável: Em `dados/painel/painel_c03_event_pesos.py:104`, `eventos()` exige mudança de partido e usa somente o sinal da diferença de escore. Em `dados/painel/painel_uf_ano_tse_brc.csv`, o Rio de Janeiro passa de PMDB, escore 7,01 em 2018, para PSC, 8,33 em 2019. `dados/painel/c03_event_pesos_resultados.md` inclui esse evento no grupo “esquerda->direita”. O próprio MC6.A12 distingue corretamente movimento de escore e mudança de bloco.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Renomear esses contrastes para “deslocamento para a direita” e “deslocamento para a esquerda”. Se a pergunta substantiva exigir alternância entre blocos, definir seus limites e refazer a seleção dos eventos.
- Incerteza: A discrepância semântica é certa. Os resultados de uma análise restrita a mudanças entre blocos não foram calculados neste parecer.

### AST-04 — Condenações soviéticas não equivalem integralmente a perseguição por relações consensuais
- Local: Seção 3.7, segundo parágrafo; Tabela 5, União Soviética.
- Trecho ou alegação: “mais de 38 mil condenações judiciais, sem contar o Gulag”.
- Problema: Inserido numa tabela de perseguição estatal a homossexuais, o total sugere que todas essas condenações correspondem à repressão de relações consensuais. O próprio Material Complementar informa que a série mistura situações juridicamente e substantivamente diferentes.
- Evidência ou raciocínio verificável: MC8 e `dados/regimes/H-RELATORIO.md` registram a estimativa aproximada de Valodzin de que cerca de metade dos casos envolvia coerção ou menores. Também esclarecem que são condenações, não necessariamente pessoas distintas, e que 1934–1945 não está coberto.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Levar essa ressalva ao corpo e à Tabela 5. Apresentar 38 mil como total da série judicial heterogênea, sem convertê-lo em número de perseguidos por relações consensuais. Não substituir automaticamente por 19 mil: a proporção é aproximada e as categorias exigem interpretação histórica.
- Incerteza: A ressalva não nega a perseguição documentada nem demonstra que acusações de coerção fossem sempre verdadeiras. O total específico de condenações por relações consensuais permanece indeterminado.

### AST-05 — Regra retrospectiva apresentada como anterior à análise
- Local: Seção 3.4, terceiro parágrafo; MC1 e MC4.
- Trecho ou alegação: “Pela regra escrita antes da análise”.
- Problema: O parágrafo fundamenta a confirmação no vínculo censitário do ONS, cuja admissibilidade decorreu de uma ampliação retrospectiva dos critérios. A descrição do corpo não preserva essa distinção, embora o complemento a documente corretamente.
- Evidência ou raciocínio verificável: `paper/v05/MATERIAL-COMPLEMENTAR.md`, MC1, declara que a regra complementar foi definida em 24 de outubro, “depois de identificados estudos recentes” e que “não é prospectiva”. MC4 distingue o resultado sob a regra original, restrita a periódicos Q1, daquele sob a regra ampliada que admite o ONS.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Identificar no corpo a ampliação retrospectiva e os resultados sob cada regra. Justificar a seleção por desenho e qualidade do estudo; o quartil do periódico não deve substituir essa avaliação. A inclusão do ONS pode ser substantivamente correta sem ser apresentada como prospectiva.
- Incerteza: A inconsistência de apresentação está demonstrada. Não há evidência, neste exame, de que a ampliação tenha produzido uma estimativa numérica falsa ou de que a conclusão descritiva do ONS deva ser descartada.

### AST-06 — Poder apresentado como limite absoluto de detecção
- Local: Resumo, Abstract, Tabela 2, linha 7, e formulações do MC10.
- Trecho ou alegação: “só detectaria mudança de 60,7% ou mais”.
- Problema: O efeito mínimo detectável não é um limiar abaixo do qual a detecção seja impossível. É o efeito associado ao poder escolhido. Além disso, o cálculo citado trata de aumento, não de qualquer mudança.
- Evidência ou raciocínio verificável: `research-2026-10-21-rodada3/F2-custos/deff_pns2019.py`, funções `n_duas_prop()` e `mde()`, usa poder de 80% e procura alternativas com `p2 = p1 * (1 + mid)`. A seção 3.1 reconhece que o limiar para quedas não foi calculado; o glossário explica corretamente que efeitos menores têm poder inferior a 80%.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Escrever: “Sob as hipóteses adotadas, duas rodadas independentes teriam 80% de poder para detectar aumento relativo de aproximadamente 61%”. Uniformizar resumo, tradução, tabela e complemento.
- Incerteza: Não identifiquei erro no valor de 60,7% sob as hipóteses do cálculo. A precisão aparente continua condicionada ao efeito de desenho estimado.

### AST-07 — Intervalo degenerado para categoria sem casos
- Local: Tabela MC2.A4, agressor “Filho(a)/enteado(a)”, coluna LGB+.
- Trecho ou alegação: “0,00% [0,00; 0,00]”.
- Problema: Um intervalo apresentado como IC95% com ambos os limites em zero transmite certeza de ausência populacional a partir de ausência amostral. A linearização de Wald degenera nessa situação e não fornece uma quantificação informativa da incerteza.
- Evidência ou raciocínio verificável: A célula consta de `paper/v05/MATERIAL-COMPLEMENTAR.md` e de `dados/pns/seguro_pns2019.md`. Em `dados/pns/seguro_pns2019.py`, a variância deriva da função de influência; com indicador nulo em todas as observações do domínio, essa contribuição também é nula.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Informar “nenhum caso observado; intervalo não estimável pelo método empregado”, ou aplicar método adequado a proporções de fronteira que respeite o desenho amostral. Não substituir automaticamente por intervalo binomial de amostra simples.
- Incerteza: O problema é localizado nessa inferência de fronteira; não demonstra falha nas razões principais de prevalência.

### AST-08 — Pesquisa de conveniência apresentada sem qualificação
- Local: Seção 4.2, primeiro parágrafo; MC11, sistemas internacionais.
- Trecho ou alegação: “mede de 13% a 14% de pessoas atacadas em cinco anos”.
- Problema: A pesquisa europeia aparece junto de levantamentos probabilísticos, sem informar que sua amostra é não probabilística. O leitor pode interpretar a porcentagem como prevalência populacional comparável às demais.
- Evidência ou raciocínio verificável: `docs/laudos/F8-literatura-README.md`, entrada B10, classifica a FRA como “survey de conveniência” e “amostra não probabilística”. `docs/laudos/F2-custos-README.md` também descreve o levantamento como aberto pela internet e não probabilístico.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Dizer “13%–14% dos respondentes da pesquisa não probabilística” e explicitar a limitação de seleção. Preservar sua utilidade descritiva sem equiparar sua representatividade à PNS ou aos levantamentos probabilísticos citados.
- Incerteza: Não há demonstração de que a porcentagem esteja aritmeticamente errada; a magnitude e a direção do viés de seleção são desconhecidas.

### AST-09 — Extremos de raça ignorada contam óbitos duas vezes
- Local: MC4, Tabela MC4.A16; código de padronização.
- Trecho ou alegação: “extremo A (toda raça ignorada -> negros)”.
- Problema: Os cenários extremos acrescentam os óbitos de raça ignorada a uma base em que eles já foram redistribuídos proporcionalmente. Portanto, o cálculo executado não corresponde à alocação exclusiva anunciada.
- Evidência ou raciocínio verificável: `dados/sim/padroniza_idade.py`, função `redistribui()`, produz `m_ag` com redistribuição e `nr_ag` sem ela. Nas linhas 159–160, os extremos usam `m_ag` e acrescentam novamente os ignorados. Recalculando em memória com alocação única, os extremos passam de aproximadamente 2,602100 e 2,421098 para 2,602783 e 2,419558.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Construir ambos os grupos a partir dos óbitos com raça conhecida e acrescentar os ignorados uma única vez ao grupo escolhido. Acrescentar verificação de conservação do total de óbitos em cada cenário.
- Incerteza: Os valores continuam arredondando para **2,60 e 2,42**. O erro de implementação não altera a conclusão publicada nessa precisão.

### AST-10 — Custo estrangeiro com unidade monetária inadequadamente descrita
- Local: Seção 6, Tabela 6; MC10, Tabela MC10.10.
- Trecho ou alegação: “R$ de setembro de 2026”.
- Problema: O rótulo comum não descreve corretamente o custo de R$ 42 milhões do painel pela internet. Esse valor é uma referência contratual estrangeira convertida pelo câmbio nominal de outubro, enquanto o texto enfatiza documentos brasileiros e atualização pelo IPCA.
- Evidência ou raciocínio verificável: `research-2026-10-21-rodada3/F2-custos/cenarios_custo.py:42` lê PTAX de **20/10/2026**; linhas 51–52 calculam o custo por entrevista do contrato GSGB e o convertem para reais. `docs/laudos/F2-custos-README.md`, “Opção 3”, explicita “benchmark estrangeiro nominal” e ausência de preço público brasileiro. Essa origem não aparece nas referências da tabela.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Identificar separadamente moeda, data de conversão, contrato estrangeiro e hipótese de transferência do custo. Ajustar o título ou efetivamente converter todos os valores à mesma base temporal. Acrescentar as fontes contratuais e cambiais pertinentes.
- Incerteza: Não está demonstrado erro na multiplicação que produz R$ 42 milhões. A transferibilidade do preço estrangeiro para o Brasil permanece **não verificada**.

### AST-11 — Figura atribui números do GGB também à ANTRA
- Local: Figura 1, última linha.
- Trecho ou alegação: “GGB e ANTRA”.
- Problema: A linha conjunta termina nos números 257, 291 e 257, que são da série do GGB. A composição gráfica permite atribuí-los às duas organizações ou a uma contagem conjunta.
- Evidência ou raciocínio verificável: A imagem `paper/v05/figures/fig_v05_01_caminho.png` apresenta essa associação. Em `dados/exposicao/fig_caminho_v05.py`, o dicionário usado para os três números lê exclusivamente a coluna `ggb`, mas a linha recebe o rótulo “GGB e ANTRA”.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Rotular a linha apenas como GGB, ou separar as organizações e suas respectivas séries. Se mantiver o esquema conjunto, identificar expressamente que os números exibidos pertencem somente ao GGB.
- Incerteza: A atribuição gráfica é inequivocamente inadequada; não implica que os três totais do GGB estejam errados.

### AST-12 — Referência do SIDRA omite a tabela efetivamente utilizada
- Local: Referência IBGE (2026); seção 3.3 e MC4, denominadores por sexo, raça e idade.
- Trecho ou alegação: “Tabelas 9514, 6579, 7307 e 1737”.
- Problema: A referência não identifica a tabela que sustenta os denominadores da padronização racial e etária. Para uma auditoria de fontes, essa omissão impede seguir a cadeia documental apenas pelas referências publicadas.
- Evidência ou raciocínio verificável: `dados/sim/padroniza_idade.py:4` identifica **SIDRA 9606**; a função `carrega_pop()` lê `fontes/p2-f8-dados-uf/sidra/censo9606_n1_raca_sexo_idade_2010_2022.json`. A tabela 9606 não consta da referência em `paper/v05/referencias.md`.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Incluir a tabela 9606 na referência pertinente e identificar seus recortes censitários. Isso pode ser feito com referência direta ao IBGE, sem acrescentar autocitação no corpo.
- Incerteza: A fonte está disponível no repositório; trata-se de falha de identificação bibliográfica, não de ausência do denominador.

### AST-13 — Complemento não identifica claramente a versão auditada
- Local: MC12, primeiro parágrafo e Tabela MC12.D1; remissões do MC1.
- Trecho ou alegação: “calculado sobre 724 arquivos e registrado em output/hash-chain.md”.
- Problema: O complemento remete ao arquivo vigente como se contivesse o selo descrito, mas ele contém outro selo e outra contagem. Também conserva referências de seções da versão anterior, dificultando localizar resultados na organização atual.
- Evidência ou raciocínio verificável: MC12 informa o selo iniciado por `d1d2e4d7`, com 724 arquivos. `output/hash-chain.md` contém `2c0c09bc…`, com **751 arquivos**, verificado nesta revisão. `paper/v05/README.md` explica que o complemento cita a versão anterior. A Tabela MC1.2 ainda remete a seções 3.8–3.10, inexistentes no corpo atual, e o MC1 menciona “Tabela MC1.6” para resultados apresentados em MC6.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Identificar explicitamente a versão histórica correspondente ao selo antigo e seu endereço imutável, distinguindo-a da distribuição atual. Atualizar as remissões e a matriz de localização para a versão 0.5.
- Incerteza: O selo vigente passou na verificação. Não há indício de adulteração; o problema é de correspondência entre versões e documentação.

## Pontos fortes

- Distinção consistente entre ocorrência, associação ajustada, contexto e motivação.
- Tratamento explícito do desenho amostral complexo da PNS e das razões de prevalência.
- Transparência sobre análises exploratórias, multiplicidade e limites causais.
- Reconhecimento de que casos não verificáveis não equivalem a casos inventados.
- Repositório com código, agregados, testes e proveniência suficientes para detectar e corrigir discrepâncias específicas.