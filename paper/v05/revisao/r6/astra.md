# Parecer — GPT-6 Astra (gpt-6-astra)

## Verificação

Conferi o manuscrito, o Material Complementar, a matriz, os pareceres anteriores e os arquivos citados abaixo. Inspecionei visualmente as oito figuras do corpo e a Figura MC6.18. Não acessei a internet nem alterei arquivos.

O selo dos **754 arquivos** conferiu, assim como todos os hashes de `paper/v05/SHA256SUMS.txt`. Executei diretamente, sem gravação, **62 funções de teste** de seis arquivos em `tests/`: todas passaram. Isso verifica consistência dos derivados, não constitui reprodução integral dos microdados nem validação independente das fontes primárias ausentes.

| ID original | Situação | Fundamentação |
|---|---|---|
| AST-01 | resolvida em parte | A participação dos modelos, os κ e o limite de Wilson estão explícitos; MC5.C0 ainda declara não estimado o efeito dos desacordos e não esclarece sua adjudicação final (`research-2026-10-21-rodada3/F3-ggb/dados/kappa.json`). |
| AST-02 | resolvida em parte | Corpo e Figura 6 melhoraram, mas o filtro exclui apenas respostas afirmativas à autoprovocação, retendo desconhecidas; falta uniformizar essa definição no MC3 e nas sínteses (`dados/sinan/serie_campo55_uf_ano.py`). |
| AST-03 | resolvida em parte | MC6 e MC6.A10 foram corrigidos; a imagem de MC6.18 continua dizendo “Troca de lado” e “esquerda → direita” (`paper/figures/fig3_governos_painel_eventos.png`). |
| AST-04 | resolvida | Corpo e Tabela 5 distinguem condenações de pessoas e apresentam a ressalva sobre estupro/menores, conforme os trechos registrados em `dados/regimes/H-RELATORIO.md` e `dados/regimes/sources.jsonl`. |
| AST-05 | resolvida | A seção 3.4 identifica a ampliação retrospectiva e informa os dois vereditos, em conformidade com MC1 e MC4. |
| AST-06 / GRO-01 | resolvida em parte | Resumos corrigidos; Tabela 2 ainda apresenta detecção como limiar absoluto, e MC10, sua tabela e legenda conservam “variação”/“mudanças” para um cálculo restrito a aumentos. |
| AST-07 | resolvida em parte | MC2.A4 foi corrigida, mas a tabela de estado civil ainda apresenta, para 15 viúvos LGB+, `0,00 (0,00 a 0,00)` (`paper/v05/MATERIAL-COMPLEMENTAR.md:307`). |
| AST-08 | resolvida em parte | A seção 4.2 agora identifica corretamente a amostra não probabilística; MC11 ainda reproduz os percentuais sem essa qualificação. |
| AST-09 | resolvida | A base dos extremos foi corrigida. Recalculei dos agregados: **2,602783** e **2,419558**; a redistribuição preservou os **127.520 óbitos** de sexo conhecido considerados em 2022–2024 (`dados/sim/padroniza_idade.py`). |
| AST-10 | resolvida em parte | Tabela 6 corrigida; MC10.10 mantém “R$ de setembro de 2026” para o conjunto que inclui conversão cambial de outubro. |
| AST-11 | resolvida | A Figura 1 agora atribui a linha exclusivamente ao GGB, em conformidade com os dados utilizados (`paper/v05/figures/fig_v05_01_caminho.png`). |
| AST-12 | resolvida | A referência do IBGE inclui a tabela SIDRA 9606, utilizada em `dados/sim/padroniza_idade.py`. |
| AST-13 | resolvida em parte | O selo histórico foi separado do atual e há mapa de seções; persiste remissão corrompida: “Tabela MC1.2 de Vasconcelos et al.”, que transforma uma tabela externa em tabela interna (`paper/v05/MATERIAL-COMPLEMENTAR.md:126`). |
| GRO-02 | resolvida em parte | O corpo inclui “outra orientação” e reconhece que o ajuste não corrige subdeclaração; a sensibilidade quantitativa permanece não realizada e os resumos ainda expandem LGB+ apenas como lésbicas, gays e bissexuais. |
| GRO-03 | resolvida | A seção 2.2 restringe a contestação aos 50 casos com ambas as confirmações e mantém os demais sem verificação; não extrapola validação integral da lista. |
| GRO-04 | resolvida em parte | O parágrafo informa as cinco vítimas, mas a nota da Tabela 3 e a seção 5 conservam “firme”; o n pequeno da categoria empregado/patrão também continua ausente da tabela principal. |
| GRO-05 | resolvida | A linha 6 da Tabela 2 distingue os ajustes separados, conforme `dados/pns/agressor_risco_pns2019.md`. |
| GRO-06 | resolvida | A seção 3.2 distingue taxas de violência fixadas e taxa de registro ajustada, conforme `simulacao/sim_identificabilidade.py`. |
| GRO-07 | resolvida | Goodman-Bacon passou a fundamentar uma limitação, e MC1 reconhece que sua decomposição não se aplica literalmente ao desenho empregado. |
| GRO-08 | resolvida | A Tabela 5 coincide com MC8 e com o trecho da CNV registrado em `dados/regimes/sources.jsonl`: 15 cassados, sete pela razão indicada; conferência da página original: **não verificado**. |
| GRO-09 | resolvida | A seção 3.3 informa separadamente as razões por sexo e raça e declara a extrapolação dos denominadores. |
| GRO-10 | resolvida em parte | Janela do suicídio e advertência sobre expectativa de vida foram acrescentadas; a unidade temporal exata das taxas de suicídio permanece **não verificado** no material primário disponível. |
| GRO-11 | resolvida | A conclusão identifica a vinculação Sinan–óbitos e exclui sua leitura como taxa LGBT+; reprodução da acurácia a partir do estudo original: **não verificado**. |
| GRO-12 | resolvida | O texto agora fala em discursos baixados, remete às falhas de cobertura e informa o intervalo do κ, conforme MC9 e `docs/laudos/MIDIA.md`. |
| GRO-13 | refutação aceita | Manter a busca de atos no MC7 é defensável: o recorte está anunciado e os resultados assimétricos permanecem acessíveis; não é necessário repetir essa análise no corpo. |

Não há crítica ARG identificada na matriz fornecida; portanto, não atribuo situação a parecer pendente.

## Avaliação geral

O artigo oferece contribuição útil ao separar vitimização, registro, mortalidade e motivação, com documentação computacional substancial e linguagem geralmente acessível. A revisão corrigiu problemas importantes sem apagar resultados inconvenientes. Recomendo **revisão maior**, sobretudo pela propagação incompleta das correções ao complemento e às figuras e pela interpretação excessiva do placebo presidencial. Os problemas abaixo não demonstram que a razão ajustada de 2,82 esteja errada nem invalidam a distinção central entre ocorrência e registro. A aprovação exige, porém, alinhar todas as peças publicadas e delimitar melhor algumas inferências.

## Críticas

### AST-R2-01 — O placebo não é uma estimativa feita antes da posse

- Local: Seção 3.6, parágrafo “Dois fatos”; MC6, exposição federal, Figura MC6.20 e Tabela MC6.A13.
- Trecho ou alegação: “O mesmo teste, aplicado em 2018, um ano antes da posse, já dava −21,8%”.
- Problema: A redação permite interpretar −21,8% como resultado obtido exclusivamente antes da posse. O programa ajusta o placebo à série inteira de 2010–2024, incluindo os anos posteriores a 2019. Além disso, desloca simultaneamente as três quebras. Portanto, esse resultado mostra sensibilidade à especificação das datas; não isola uma mudança ocorrida antes da posse nem identifica qual mudança posterior pertence a cada governo. Comparar significância da quebra e do placebo também não testa formalmente a diferença entre eles.
- Evidência ou raciocínio verificável: `dados/presidencia/c09_d1_its.py` aplica ao mesmo vetor completo `its(y, (2016, 2019, 2023))` e `its(y, (2015, 2018, 2022))`. `dados/presidencia/c09_estrutura.py`, função `desenho_its`, mantém observações até 2024. Separadamente, `dados/sim/asr_brasil.csv` efetivamente registra queda de **31,47 em 2017 para 27,61 em 2018**: esse contraste sustenta diretamente que a queda começou antes da posse.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Apresentar o placebo como análise de sensibilidade às datas de quebra, calculada com toda a série. Sustentar o início anterior da queda com os valores observados de 2017–2018. Manter a conclusão de ausência de identificação causal, sem apresentar o placebo como prova de localização temporal do efeito.
- Incerteza: A queda anterior a 2019 está documentada. A crítica atinge a interpretação do teste, não esse fato nem demonstra efeito causal presidencial.

### AST-R2-02 — O ajuste incorpora raça ignorada à categoria de referência

- Local: Seção 3.1, razão ajustada; MC2, definição racial e modelos principais e de sensibilidade.
- Trecho ou alegação: “Descontados sexo, idade, cor, instrução, região e moradia urbana ou rural”.
- Problema: A codificação utilizada na regressão transforma raça ignorada em zero no indicador “negro”, incorporando-a à referência junto às raças conhecidas não negras. Nas tabelas descritivas, porém, o registro ignorado fica fora dos dois grupos. Essa diferença de tratamento não está declarada.
- Evidência ou raciocínio verificável: `dados/pns/seguro_pns2019.py:40` define `negro` por pertencimento aos códigos 2 e 4; a seleção do modelo, nas linhas 135–155, não exclui C009 ignorado. `dados/pns/agressor_risco_pns2019.py:100`–107 repete a operação. MC2 registra expressamente um adulto LGB+ com C009 = 9, excluído das linhas raciais descritivas (`paper/v05/MATERIAL-COMPLEMENTAR.md:193`).
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Estabelecer tratamento explícito para raça ignorada e aplicá-lo consistentemente. Recalcular os modelos com a regra corrigida e informar se as razões e intervalos publicados mudam.
- Incerteza: O tratamento pelo código é verificável; o impacto numérico sobre 2,82 e sobre as sensibilidades é **não verificado**, pois o microdado não está nesta cópia. Não há demonstração de alteração substantiva do resultado.

### AST-R2-03 — O denominador das mortes indeterminadas está ampliado no texto

- Local: Seção 3.6, parágrafo “Dois fatos”, e descrição correspondente no MC6.
- Trecho ou alegação: “A fatia de mortes violentas com causa indeterminada subiu de 18,0% em 2018 para 30,1% em 2024”.
- Problema: Os percentuais usam como denominador somente agressões mais mortes de intenção indeterminada. “Mortes violentas” abrange outras causas externas, como acidentes e suicídios, ausentes desse denominador. A conta está correta; a população à qual ela é atribuída está incorreta.
- Evidência ou raciocínio verificável: Recontagem de `dados/sim/sim_agressoes_agregado.csv`: em 2018, **12.310/(55.914 + 12.310) = 18,04%**; em 2024, **17.207/(39.946 + 17.207) = 30,11%**. Essa mesma fórmula consta de `dados/presidencia/c09_d1_its.py` e do teste correspondente em `tests/test_numeros_v05.py`.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Escrever “proporção de mortes de intenção indeterminada no conjunto formado por agressões e mortes de intenção indeterminada”. Distinguir esse indicador da proporção calculada sobre todas as causas externas.
- Incerteza: Nenhuma quanto ao denominador utilizado. A parcela desse aumento atribuível especificamente à piora da classificação de homicídios não é estimada pela divisão.

### AST-R2-04 — Posição prévia não demonstra falta de independência

- Local: MC5, “Checagens críticas da lista”, terceiro item dos limites da checagem LiHS.
- Trecho ou alegação: “A checagem não é de terceiros independentes, apesar do título”.
- Problema: A conclusão decorre de um autor já criticar a lista e de outros terem fundado uma agência de dossiês. Isso pode justificar transparência sobre posições e possíveis conflitos, mas não demonstra dependência institucional, financeira ou operacional em relação à produção da lista auditada. O texto confunde independência com ausência de posicionamento prévio e aplica ao contraponto uma desqualificação que a evidência apresentada não estabelece.
- Evidência ou raciocínio verificável: A FONTE 11 e `research-2026-10-30-contraponto/briefing.md` apresentam esses antecedentes como fundamento da conclusão. Já a crítica a Mendes e Silva, no próprio MC5, identifica uma dependência operacional concreta: dados fornecidos e revistos com técnico do GGB. Não é apresentado vínculo equivalente para a LiHS.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Descrever os antecedentes e classificá-los como possíveis fontes de viés ou conflitos intelectuais. Avaliar a checagem pelos critérios observáveis já identificados — classificação dos inconclusivos, revisão predominantemente individual e ausência de concordância — e reservar a conclusão sobre independência para vínculos documentados.
- Incerteza: A independência efetiva dos autores é **não verificado**; o erro demonstrado é inferi-la dos antecedentes apresentados, não a existência comprovada de independência.

### AST-R2-05 — Ausência na busca transformada em inexistência universal

- Local: Tabela 2, linha 25.
- Trecho ou alegação: “Ninguém calculou a expectativa de vida de pessoas trans no Brasil”.
- Problema: A busca documentada pode estabelecer que não foi localizado cálculo adequado e que a cadeia do número de 35 anos não apresenta tal cálculo. Ela não estabelece que ninguém jamais o tenha calculado. A frase ultrapassa inclusive a regra de ausência adotada pelo próprio protocolo.
- Evidência ou raciocínio verificável: MC1 determina que toda afirmação de ausência seja expressa como “não localizado no espaço enumerado de busca”, porque ausência nesse espaço não equivale a inexistência (`paper/v05/MATERIAL-COMPLEMENTAR.md:35`). A seção 3.7 documenta a cadeia dos 35 anos, mas não fornece prova adicional para a negativa universal da Tabela 2.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Substituir por “Não foi localizado cálculo de expectativa de vida que sustente os 35 anos no Brasil” e manter a distinção entre expectativa de vida e idade média das vítimas.
- Incerteza: A existência de outro cálculo é **não verificado**. A crítica não valida os 35 anos; limita a abrangência da conclusão negativa.

### AST-R2-06 — O quadro contradiz a informação sobre o agressor

- Local: Tabela 2, linha 2, coluna “O que não mostram”.
- Trecho ou alegação: “Não mede quem agrediu, nem por quê”.
- Problema: A PNS pergunta quem agrediu, e essa informação sustenta a Tabela 3, a Figura 3 e parte relevante da contribuição anunciada. O limite é que a razão global de prevalências não identifica o agressor nem a motivação; não que a fonte deixe de medir o vínculo com o agressor.
- Evidência ou raciocínio verificável: A seção 3.1 afirma que o módulo pergunta “quem agrediu e onde”; `dados/pns/agressor_risco_pns2019.py` utiliza V018 para construir as categorias apresentadas na Tabela 3.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Escrever “A razão global não identifica o tipo de agressor nem demonstra o motivo; o agressor apontado é analisado separadamente”.
- Incerteza: Nenhuma quanto à contradição interna; permanece o limite já declarado de uma única resposta por vítima.

## Pontos fortes

- Distinção consistente entre violência relatada, registro administrativo e motivação.
- Tratamento do desenho amostral na PNS, incluindo influências dos domínios nas unidades amostrais.
- Transparência sobre análises posteriores aos resultados e mudança retrospectiva de elegibilidade.
- Repositório com integridade verificável, derivados rastreáveis e testes úteis.
- Reconhecimento explícito de que casos não verificados não são casos inventados e de que resultados não significativos não provam ausência de efeito.