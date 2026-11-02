# Parecer — Gemini 4 Argon (gemini-4-argon-high)

> Transcrição do texto da página https://gemini.google.com/app/a06ba58389edb5dc (app do Gemini, conta Pro, 4 Argon, Thinking High), lida com `get_page_text` em 2026-10-30. Fórmulas reescritas em linha; nenhuma palavra mudada fora disso. Rodada de verificação da r7 (manuscrito sha `d75cb1b6…`), com o repositório anexo em .zip.

## Avaliação geral

A versão revisada (r7) consolida um trabalho de auditoria estatística e documental de altíssimo rigor sobre os indicadores de violência e mortalidade LGBT+ no Brasil. O autor respondeu de forma efetiva e transparente à quase totalidade das pendências anteriores dos três revisores no corpo principal do manuscrito, qualificando adequadamente o teste de sensibilidade temporal de 2018, os denominadores das mortes de intenção indeterminada, a regra de filtro do Sinan, o alcance dos intervalos por tipo de agressor na PNS 2019 e as premissas de modo de entrevista e efeito de desenho na Tabela 6. Restam apenas desalinhamentos pontuais de sincronização entre o texto atualizado do manuscrito e passagens herdadas no Material Complementar (MC2, MC3, MC5 e MC6), todos de baixa gravidade e rápida resolução textual. Recomendação: aceitar com revisão menor.

## Verificação

| ID | Status | Por quê (em uma linha) |
|---|---|---|
| AST-01 | resolvida | A seção 2.6 agora explicita "23 casos tiveram dupla codificação, com 21 pares válidos nas variáveis abaixo", alinhando o corpo à Tabela MC5.C0. |
| AST-02 | resolvida | O texto da seção 3.2 e a nota da Figura 6 passaram a especificar "fichas de violência não marcadas como autoprovocada" (restando sincronizar apenas a nota da Figura MC3.12 no MC3). |
| AST-03 | resolvida | O texto do MC6 e a Tabela MC6.A10 usam "deslocamento para a direita/esquerda" e o hash foi atualizado na matriz; a inspeção visual direta do PNG fica como não verificado no pacote de texto. |
| AST-06 / GRO-01 | resolvida | A linha 7 da Tabela 2, o QUADRO-E2 (A15) e o texto/nota da Figura MC10.24 no MC10 explicitam "80% de poder só para aumento relativo de 60,7% ou mais". |
| AST-07 | resolvida | A Tabela MC2.A4 e a tabela descritiva por estado civil no MC2 substituíram 0,00 [0,00; 0,00] por nenhum caso (intervalo não estimável), com a exceção declarada na nota da Tabela MC2.A4. |
| AST-08 | resolvida em parte | A seção 4.2 qualifica a pesquisa da FRA como "sem amostra probabilística" e "respondentes"; o trecho equivalente no MC11 fica como não verificado por truncamento do final da FONTE 10 no pacote. |
| AST-10 | resolvida em parte | O título e a nota da Tabela 6 trazem "(R$ de 2026)" e a conversão pelo câmbio de 20/10/2026; a Tabela MC10.10 fica como não verificado por truncamento do final da FONTE 10 no pacote. |
| AST-13 | resolvida | A seção 3.1 do MC2 foi corrigida para "Tabela 2 de Vasconcelos et al. (2023)", eliminando o prefixo indevido na remissão à tabela de outro autor. |
| GRO-02 | resolvida em parte | A definição de LGB+ incluiu "ou de outra orientação não heterossexual" no Resumo, Abstract, Introdução, seção 2.2 e Tabela 2; a simulação de subdeclaração seletiva segue declarada como não estimada. |
| GRO-04 | resolvida | A nota da Tabela 3 e a seção 5 passaram a descrever intervalos nominais sem correção para múltiplas comparações e explicitaram as 5 vítimas LGB+ em "policial", "empregado, patrão ou chefe" e "outro". |
| AST-R2-01 | resolvida em parte | A seção 3.6 fundamenta a queda pré-posse nas taxas observadas (31,47 em 2017 para 27,61 em 2018) e trata os −21,8% como sensibilidade à data, mas o MC6 (seção 3.7, §3) manteve a redação antiga de "placebo". |
| AST-R2-02 | resolvida | A nota da Tabela MC2.A2 documenta que a cor/raça ignorada (1 caso LGB+ entre 1.554) entra como zero no indicador de negros na regressão e que o recálculo sem ignorados não foi feito. |
| AST-R2-03 | resolvida | A seção 3.6 explicita "Entre as mortes por agressão e as de intenção indeterminada, a fatia das indeterminadas subiu de 18,0% em 2018 para 30,1% em 2024". |
| AST-R2-04 | resolvida | O MC5 qualifica os antecedentes dos autores da checagem de 2016 como possível fonte de viés intelectual, distinguindo-os da participação operacional de técnico do GGB em Mendes e Silva (2020). |
| AST-R2-05 | resolvida | A linha 25 da Tabela 2 e o item A17 do QUADRO-E2 substituíram a negativa universal por "Não foi localizado cálculo de expectativa de vida de pessoas trans no Brasil". |
| AST-R2-06 | resolvida | A coluna "O que não mostram" da linha 2 da Tabela 2 e o item A1 do QUADRO-E2 foram ajustados para "A razão global não identifica o tipo de agressor nem o motivo; o agressor apontado é analisado à parte". |
| GRO-R2-01 | resolvida | O último parágrafo da Introdução (seção 1) foi corrigido para "as quatro conclusões", alinhando-se à seção 6. |
| ARG-01 | resolvida | A nota da Tabela 6 explicita que o efeito de desenho varia por desfecho (maior na física que em qualquer violência) e que atingir o número estimado de adultos LGB+ exigiria autopreenchimento privado. |
| ARG-02 | resolvida | O quinto parágrafo da seção 3.1 declara que a PNS registra apenas o agressor do episódio mais grave (subestimando riscos específicos em vitimizações múltiplas) e que a razão por familiar não desconta coabitação. |
| ARG-03 | resolvida | Os seis pontos de divergência no MC (35 anos no MC9, subgrupo de Hatzenbuehler 2020 no MC4, desacordos na Tabela MC5.C0, 1,35% vs. 1,38% no MC5, unidades do Disque 100 e 44,5%/seção 6 no MC3) foram corrigidos, e a refutação sobre os caminhos de imagens na cópia de trabalho é aceita. |
| ARG-04 | resolvida | Corrigida no último parágrafo da seção 1 ("as quatro conclusões"), junto com GRO-R2-01. |
| ARG-05 | resolvida | A nota da Tabela MC5.C0 reporta o intervalo de Wilson com correção para população finita (26,3% a 36,6%, para 160 de 329 casos), e a nota da Tabela MC2.A2 declara o tratamento da raça ignorada. |
| ARG-06 | resolvida | O texto da seção 3.1, a nota da Tabela 3 e a seção 5 dizem "só a diferença na fatia de policial tem intervalo que exclui o zero", e a seção 3.5 e o MC5 detalham "só 3 tiveram dois, e 14 não têm revisor registrado". |
| ARG-07 | resolvida | Os itens (i) denominador na seção 3.6, (ii) comparação com o segundo codificador nos dois grupos na seção 3.7 (1/50 vs. 2/38, p = 0,58) e (iv) "Kitagawa (1955)" no MC1 e MC4 foram verificados; a remoção de Atlas 2026 em referencias-mc.md fica como não verificado por truncamento da FONTE 10. |

## Críticas

### ARG-R2-01 — Desalinhamento entre a seção 3.6 e o MC6 sobre o teste de 2018 e o denominador de causas indeterminadas

- Local: Material Complementar MC6 (seção 3.6, §2; seção 3.7, §2 e §3; Nota da Figura MC6.20) e FONTE 1 (QUADRO-E2.md, linha A10), em contraste com a seção 3.6 (§4) do manuscrito.
- Trecho ou alegação: "mas o placebo de 2018, um ano antes da troca de presidente, dá -21,8% (-37,4% a -2,4%): a queda não pode ser atribuída à troca presidencial, porque já aparece antes dela (Figura MC6.20 e Tabela MC6.A13)." e "A parcela de óbitos de causa indeterminada subiu de 18,0% em 2018 para 25,9% em 2022 e 30,1% em 2024".
- Problema: Na revisão r7, a seção 3.6 (§4) do manuscrito foi devidamente corrigida (em resposta a AST-R2-01 e AST-R2-03/ARG-07) para mostrar que: (a) a anterioridade da queda em relação à posse presidencial de 2019 vem das próprias taxas padronizadas observadas (de 31,47 em 2017 para 27,61 em 2018), enquanto a estimativa de −21,8% vem de um modelo ajustado à série completa (2010 a 2024) com as três quebras deslocadas um ano para trás (logo, é um teste de sensibilidade à data da quebra, e não uma estimativa pré-posse livre de dados pós-2019); e (b) os percentuais de 18,0% e 30,1% têm como denominador a soma das mortes por agressão e das de intenção indeterminada. Contudo, o texto do MC6 (seção 3.7, §2 e §3, e nota da Figura MC6.20) e a justificativa da linha A10 no QUADRO-E2.md mantiveram a formulação anterior, tratando o "placebo de 2018" como demonstração direta de que a queda antecedeu a posse e omitindo que o denominador de 18,0%, 25,9%, 30,1% (e dos 13,4% na seção 3.6, §2 do MC6) é a soma de agressões e mortes de intenção indeterminada.
- Evidência ou raciocínio verificável: Comparação direta entre o diff da seção 3.6 (§4) do manuscrito e a FONTE 10 (MATERIAL-COMPLEMENTAR.md, seção MC6, subseções 3.6 e 3.7) e a FONTE 1 (QUADRO-E2.md, linha A10).
- Tipo: erro demonstrado.
- Gravidade: menor.
- Correção proposta: Sincronizar os parágrafos 2 e 3 da seção 3.7 do MC6, a nota da Figura MC6.20 (e o §2 da seção 3.6 do MC6 para os 13,4%) com a redação já adotada no §4 da seção 3.6 do manuscrito principal, explicitando o denominador (agressões mais intenção indeterminada), citando a queda observada de 31,47 (2017) para 27,61 (2018) e descrevendo o cálculo de −21,8% como teste de sensibilidade com a série inteira e as quebras deslocadas um ano para trás.
- Incerteza: Nenhuma quanto à divergência textual entre o corpo revisado e o MC6.

### ARG-R2-02 — Falta de qualificação sobre o filtro de violência não autoprovocada na nota da Figura MC3.12 e de ressalva na tabela de fatias do MC2

- Local: Material Complementar MC3 (seção 3.5, §2 e Nota da Figura MC3.12) e MC2 ("Análises novas da v0.5", subseção 1), na FONTE 10.
- Trecho ou alegação: "Cada coluna do painel (a) soma 100% das notificações do ano" (Nota da Figura MC3.12) e coluna "A diferença é firme?" com valor "sim" na linha Policial da subseção 1 das análises novas do MC2.
- Problema: Dois ajustes de precisão aplicados ao corpo na r7 não foram espelhados nas passagens correspondentes do Material Complementar: (1) A Figura MC3.12 reproduz exatamente o mesmo arquivo gráfico da Figura 6 do corpo (fig18_motivacao_sinan.png), cuja nota no corpo foi corrigida (AST-02) para "soma 100% das fichas de violência não marcadas como autoprovocada do ano" (e o texto da seção 3.2 traz "53,4%"), enquanto no MC3 o texto traz "53%" e a nota da Figura MC3.12 continua dizendo "100% das notificações do ano" sem mencionar o filtro que exclui a marcação afirmativa de violência autoprovocada; (2) Na subseção 1 das análises novas do MC2 (copiada de dados/pns/agressor_risco_pns2019.md), a tabela mantém a coluna "A diferença é firme?" com "sim" para Policial sem a nota adicionada à Tabela 3 do corpo (GRO-04 / ARG-06) de que a estimativa se apoia em 5 vítimas LGB+ e usa intervalos nominais sem correção para múltiplas comparações.
- Evidência ou raciocínio verificável: Comparação entre a seção 3.1 (Nota da Tabela 3) e a seção 3.2 (texto e Nota da Figura 6) do manuscrito revisado com a FONTE 4 (dados/pns/agressor_risco_pns2019.md §1) e a FONTE 10 (MATERIAL-COMPLEMENTAR.md, seções MC2 e MC3).
- Tipo: preferência editorial.
- Gravidade: menor.
- Correção proposta: Na seção 3.5 do MC3 e na nota da Figura MC3.12, especificar "fichas de violência não marcadas como autoprovocada" e "53,4%"; na subseção 1 das análises novas do MC2 (e em agressor_risco_pns2019.md), acrescentar nota informando que os intervalos são nominais (sem correção para múltiplas comparações) e que a categoria "Policial" tem 5 vítimas LGB+ na amostra.
- Incerteza: Nenhuma.

### ARG-R2-03 — Transição entre o universo de 347 casos da planilha e o subconjunto de 258 homicídios no MC5

- Local: Material Complementar MC5, subseção "Checagens críticas da lista e busca por contrapontos", Tabela MC5.C1 e segundo item de "Limites da checagem" (FONTE 10).
- Trecho ou alegação: "A página dos autores conta como erro a soma de 'não' e 'inconclusivo' (227 de 258 homicídios, 88%). Inconclusivo não é ausência de preconceito, de modo que 8,9% é um piso sob o critério dos autores, e não uma estimativa da fração verdadeira."
- Problema: Na Tabela MC5.C1, tabulada sobre todos os 347 casos da planilha de Vieira et al. (2019), a soma de "Sem indício ('Não')" (127) e "Inconclusivo" (159) é 127 + 159 = 286 casos (82,4% de 347), e os 31 casos "Com indício de preconceito ('Sim')" representam 31/347 = 8,9%. Já os números "227 de 258 homicídios, 88%" citados no item seguinte referem-se ao subconjunto de 258 homicídios destacado no texto da página dos autores (excluindo suicídios e casos não localizados/no exterior/duplicados), universo no qual os mesmos 31 casos "Sim" equivalem a 31/258 = 12,0% (258 − 227 = 31). Como a frase passa diretamente de "(227 de 258 homicídios, 88%)" para "de modo que 8,9% é um piso", o leitor que compara o texto com a Tabela MC5.C1 pode estranhar por que 127 + 159 daria 227 e por que o complementar de 88% seria 8,9% (em vez de 12,0% nos 258 homicídios).
- Evidência ou raciocínio verificável: Recontagem aritmética na Tabela MC5.C1 da FONTE 10: no total da planilha (N = 347), 31 + 127 + 159 + 23 + 6 + 1 = 347, com Não + Inconclusivo = 127 + 159 = 286 (82,4%) e Sim = 31/347 = 8,93%; no subconjunto de homicídios (n = 258), 227/258 = 87,98% e (258 − 227)/258 = 31/258 = 12,02%.
- Tipo: preferência editorial.
- Gravidade: menor.
- Correção proposta: Explicitar no segundo item de "Limites da checagem" do MC5 que na planilha inteira (347 casos, incluindo suicídios) "não" e "inconclusivo" somam 286 casos (82,4%, contra 8,9% com indício), enquanto no recorte de 258 homicídios usado no texto da página dos autores somam 227 (88,0%, contra 12,0% com indício).
- Incerteza: Nenhuma.

### ARG-R2-04 — Omissão da categoria "amigo, colega ou vizinho" ao resumir as razões ajustadas nas seções 4.1, 4.3 e 6, e remissão residual ao "Apêndice D" no MC1

- Local: Seção 4.1 (§1), seção 4.3 (§2) e seção 6 (§2) do manuscrito; e Nota da Tabela MC1.3 no Material Complementar MC1 (FONTE 10).
- Trecho ou alegação: "Em análise feita depois de ver os resultados, o excesso persiste no ajuste quando o agressor apontado é parceiro ou ex, familiar ou desconhecido." (seção 4.1) e "Os textos integrais e as impressões digitais completas estão no repositório (Apêndice D)." (Nota da Tabela MC1.3).
- Problema: (1) Na Tabela 3 (que reporta o ajuste principal por sexo, idade, cor, instrução, região e moradia urbana/rural), o excesso de risco para adultos LGB+ tem intervalo de 95% acima de 1 em quatro categorias específicas de agressor (além do subtotal de conhecidos): parceiro ou ex (2,50; 1,48 a 4,25), familiar (4,79; 2,58 a 8,90), amigo, colega ou vizinho (2,12; 1,02 a 4,39) e pessoa desconhecida (2,05; 1,22 a 3,45). A categoria "amigo, colega ou vizinho" só deixa de excluir 1 quando se acrescenta o estado civil ao modelo (passando a 1,87; 0,90 a 3,89, conforme a seção 3.1, §7). Nas seções 4.1, 4.3 e 6, o texto resume que o excesso persiste "no ajuste" apenas para "parceiro ou ex, familiar ou desconhecido", sem especificar que se refere aos modelos que incluem também o estado civil. (2) Na Nota da Tabela MC1.3 (FONTE 10), há uma remissão herdada a "(Apêndice D)", que não consta na Tabela MC0.1 de correspondência de seções da v0.4.4.
- Evidência ou raciocínio verificável: Tabela 3 do manuscrito, FONTE 4 (dados/pns/agressor_risco_pns2019.md §4) e FONTE 10 (MATERIAL-COMPLEMENTAR.md, Tabela MC0.1 e Nota da Tabela MC1.3).
- Tipo: preferência editorial.
- Gravidade: menor.
- Correção proposta: Nas seções 4.1, 4.3 e 6, escrever "persiste em todos os ajustes (inclusive por estado civil) quando o agressor apontado é parceiro ou ex, familiar ou desconhecido" (ou incluir "amigo, colega ou vizinho" caso se refira ao ajuste principal da Tabela 3); na Nota da Tabela MC1.3, substituir "(Apêndice D)" por "(MC12)".
- Incerteza: Nenhuma.

## Pontos fortes

- Separação rigorosa de níveis analíticos: A estrutura em quatro níveis (ocorrência bruta, disparidade condicional, contexto/vínculo e motivação) disciplina a inferência e impede saltos lógicos comuns na literatura e no debate público.
- Simetria adversarial e auditabilidade: A aplicação da mesma régua metodológica a contagens ativistas (GGB, ANTRA), checagens críticas (Liga Humanista Secular) e discursos parlamentares é exemplar e amparada por código e dados agregados abertos.
- Demonstração formal de não identificabilidade em registros: A modelagem da Equação 1 (R = I × p) sobre os boletins de ocorrência e as séries do Disque 100 e do Sinan expõe com clareza didática e matemática a impossibilidade de extrair tendência de incidência sem restrição externa.
- Reanálise aprofundada da PNS 2019: A distinção entre fatia entre as vítimas e risco populacional por tipo de agressor, somada aos testes de sensibilidade por estado civil, coabitação e modo de entrevista, oferece contribuição empírica original e nuançada.
- Transparência sobre desvios e análises pós-dados: O artigo separa com honestidade exemplar o que foi pré-registrado do que foi executado após observar os resultados ou durante a revisão por pares.
