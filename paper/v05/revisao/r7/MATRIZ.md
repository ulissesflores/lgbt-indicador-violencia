# Matriz de respostas da rodada r7 (verificação dos três: Astra e Grok por script, Argon pelo navegador)

Manuscrito verificado: `revisao/r7/MANUSCRITO.md` (sha256 `d75cb1b6…`). Corrigido: `revisao/r8/MANUSCRITO.md`. Recomendações: Astra, revisão maior (coerência documental); Grok, revisão menor, sem crítica nova; Argon, aceitar com revisão menor. Trava 0 falhas nos 6 blocos; quadro 0 divergências.

## Pendências em parte que foram fechadas

| ID | O que faltava | Resposta |
|---|---|---|
| AST-02 | MC3 e nota da Figura MC3.12 sem o filtro | "notificações do ano não marcadas como violência autoprovocada"; "53,4%" e "42,5% a 53,4%" no MC3 |
| AST-06 | imagem da Figura MC10.24 e cabeçalho da Tabela MC10.10 | figura 17 regenerada ("80% de poder para aumento de...", "para detectar aumento de 30%"); título da figura e cabeçalho da tabela no MC |
| AST-R2-01 / ARG-R2-01 | MC6, nota da Figura MC6.20 e Tabela MC6.A13 ainda falavam em placebo anterior à posse | MC6 reescrito: quebras deslocadas com a série inteira = sensibilidade à data; início da queda pelos valores de 2017 e 2018; títulos da figura e da tabela; denominador da parcela de indeterminadas (18,0%, 25,9%, 30,1% e 13,4%) dito no MC6 |
| ARG-R2-02 | tabela "firme" do MC2 sem a ressalva | nota após a tabela: intervalo nominal sem correção e 5 vítimas LGB+ em policial |
| Grok (ARG-07 resto) | "Kitagawa" sem ano no corpo | "Kitagawa (1955)" na seção 2.5; a referência passa da lista do MC para a do artigo |

## Pendências que seguem em parte (declaradas, análise nova não feita)

AST-01 (adjudicação final e efeito dos desacordos do GGB), GRO-02 (cenário de subdeclaração), AST-R2-02 (regressão sem raça ignorada), ARG-01 (Tabela 6 refeita com a fração por modo), ARG-02 (coabitação por tipo de agressor). As cinco estão declaradas no texto como não feitas.

## Críticas novas

| ID | Crítica | Conferência | Resposta | Onde |
|---|---|---|---|---|
| AST-R2-07 | "a busca não encontrou comparação entre países" contradiz o registro da busca | `frente-A-brasil.md`: MATRIA (TGEU, 38 países, Brasil 8º em taxa); Truco 1º absoluto e 4º por milhão; Aos Fatos 3º por milhão | Aceita. "A busca só achou comparações de mortes noticiadas de pessoas trans; a posição do Brasil muda com a taxa; nenhuma tem cobertura e definições comuns"; MC5 descreve as comparações (TGEU declara não estimar o número real) | bloco-3c, QUADRO-E2, mc5-contraponto.md |
| AST-R2-08 | "precisaria de preenchimento privado" é inferência causal não identificada | `agressor_risco_pns2019.py` usa V00101 (quem preencheu), não V001 (privacidade); nada randomizado | Aceita. 1,89% vira hipótese de planejamento; a diferença por modo pode vir de quem respondeu; o modo é escolha a testar em piloto. (Diverge do texto que o Argon aprovou em ARG-01; prevalece a evidência do código) | bloco-4 (nota da Tabela 6) |
| AST-R2-09 | "sem mudança antes" na Figura MC6.18 | `make_figures.py:426` rotula p ≥ 0,05 assim | Aceita. "mudança anterior não detectada"; figura 3 regenerada | repo `paper/figures/` |
| AST-R2-10 | "15 a 16 estados no grupo de comparação" | `c03_event_pesos_resultados.csv`: n_ufs_controle 10 e 10; G 15 e 16 | Aceita. "10 estados distintos de controle em cada direção (15 e 16 no conjunto)" | monta_mc.py |
| ARG-R2-03 | 227/258 × 8,9% de 347 | recontagem: 286/347 = 82,4%; 31/258 = 12,0% | Aceita. MC5 separa os dois universos | mc5-contraponto.md |
| ARG-R2-04 | resumo das razões por agressor omite amigo/colega/vizinho; "(Apêndice D)" no MC1 | seção 3.1: com estado civil, amigo/colega/vizinho deixa de excluir 1 | Aceita. Seções 4.1 e 6 dizem "também com o estado civil"; "Para amigo, colega ou vizinho, só sem o estado civil"; "(MC12)" no MC1 e "(Tabela MC12.D1)" no MC12 | bloco-4, monta_mc.py |
