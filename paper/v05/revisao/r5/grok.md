Vou conferir no repositório os pontos em que o manuscrito e o Material Complementar podem divergir, sem alterar nada.Os números centrais batem com o quadro conferido. Vou checar no repositório os pontos em que o texto pode ir além do que os arquivos mostram.Vou fechar três trechos no repositório antes de redigir o parecer: a função do efeito mínimo, a definição de LGB+ no script e a frase dos diplomatas.# Parecer — Grok 4.7 (grok-4.7)

## Avaliação geral

O artigo é uma auditoria de fontes, e o núcleo se sustenta. A reanálise da Pesquisa Nacional de Saúde (PNS) de 2019 reproduz as prevalências publicadas, a razão ajustada de violência física é 2,82 (intervalo de 95%, 2,16 a 3,68) com o desenho amostral, e as séries administrativas são lidas como registro. A contribuição cabe em preprint de métodos e saúde pública: separa ocorrência, resíduo após ajuste, contexto e motivo, e recusa taxa nacional, "35 anos" e "país que mais mata". A clareza para o leigo é alta. O custo é o resumo e duas frases de resultado comprimirem limites que o corpo e o Material Complementar já medem. Recomendação: revisão menor. Os reparos são de redação e de inferência. Não pedem outro desenho nem derrubam a disparidade da PNS. As figuras em `paper/v05/figures/` não foram abertas; a leitura usa títulos, notas e texto.

## Críticas

### GRO-01 — O resumo trata o efeito mínimo como mudança nos dois sentidos

- Local: Resumo, segundo parágrafo; Abstract, a frase correspondente. A Tabela 2, linha 7, e a seção 3.1 já estão corretas.
- Trecho ou alegação: "Repetir essa amostra só detectaria mudança de 60,7% ou mais na violência física." No inglês: "would only detect a 60.7% or greater change".
- Problema: O cálculo só procura aumentos relativos. Uma queda de 60,7% não é o limiar, e o limiar de queda não foi calculado. "Mudança" e "change" afirmam os dois sentidos. É a frase que o resumo faz circular.
- Evidência ou raciocínio verificável: Seção 3.1: "só aumentos relativos de 60,7% ou mais na violência física. Para quedas, o limiar é outro e não foi calculado aqui". Em `tests/test_correcoes_v03.py`, `_mde` define `p2 = min(p1 * (1 + mid), 0.9999)`, só acima da prevalência inicial. A mesma função está em `research-2026-10-21-rodada3/F2-custos/deff_pns2019.py`. FONTE 1, linha A15: a coluna "por quê" ainda diz "variação de 60,7%"; a coluna do que os dados mostram, e a Tabela 2, dizem "aumento relativo".
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: No resumo em português e no abstract, trocar "mudança"/"change" por "aumento relativo" e repetir que o limiar de queda não foi calculado. O número 60,7%, como alta, pode ficar.
- Incerteza: Baixa. O sentido do cálculo está no código. Não refiz o bootstrap do efeito de desenho; o teste trava 0,607 sobre o n observado de 1.554.

### GRO-02 — Ajustar pelo modo de entrevista não corrige quem deixa de se declarar LGB+

- Local: Seção 3.1, parágrafo do modo de preenchimento; seção 5, primeira limitação; definição de LGB+ só no script.
- Trecho ou alegação: "a ajustada com o modo fica em 2,68 (intervalo de 95%, 2,05 a 3,49)".
- Problema: A fração que se declara LGB+ é 3,51% quando o morador preenche e 1,38% quando o entrevistador preenche. Incluir o modo na regressão compara grupos dentro de cada modo. Não corrige classificação diferencial da orientação. Se parte de quem não se declara entra como heterossexual e tem mais violência, a razão atenua; se a vitimização muda a chance de declarar, o viés pode ir para qualquer lado. Não há cenário quantitativo. As razões brutas parecidas nos dois modos (3,21 e 3,84) mostram que a disparidade não é um artefato óbvio do modo; não delimitam o viés. O script ainda põe em LGB+ o código "outra", e o corpo não diz isso.
- Evidência ou raciocínio verificável: FONTE 4, seção 5 (3,51% e 1,38%; razão ajustada 2,68; fluxo 88.531, 85.913, 849 "não sabe", 1.769 recusas). FONTE 6, variável V00101. `dados/pns/seguro_pns2019.py`, cabeçalho: "LGB+' = Y008 em {2 bissexual, 3 homossexual, 4 outra}". A seção 5 do manuscrito fala em estigma e em diferença de quem preenche, sem limite numérico.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Dizer no corpo que LGB+ inclui "outra". Dizer que 2,68 não é correção de subdeclaração. Acrescentar pelo menos um cenário extremo de realocação dos não respondentes e de uma fração dos entrevistados pelo entrevistador.
- Incerteza: A direção do viés não está identificada nestes dados. O que está demonstrado é que o ajuste publicado não a identifica.

### GRO-03 — "Contraria a ideia de lista inventada" vale só para o que a notícia confirma

- Local: Seção 2.2, último parágrafo. O resumo e a seção 3.5 são mais estreitos.
- Trecho ou alegação: "Nos casos verificáveis, isso contraria a ideia de lista inventada".
- Problema: Em 50 dos 160 casos sorteados a notícia confirma morte violenta e vítima LGBT+. Nos outros 110, não. Em 23 das 73 mortes violentas confirmadas, a notícia não traz a condição LGBT+. A lista é montada com notícias: recuperar a matéria citada confere a cadeia notícia–notícia, não inquérito, instituto médico-legal ou processo. A frase contraria a invenção apenas dos casos em que a matéria foi achada e diz as duas coisas. De 2023 a 2025 não há lista nominal.
- Evidência ou raciocínio verificável: Seção 3.5 do manuscrito (50/160 = 31,3%, Wilson 24,6% a 38,8%; 73/88; 40 com nome; 3 de 73 com ódio atribuído pela fonte). FONTE 2, bloco A8/A9, confere 160, 106, 88, 73, 50, 40, 3 e 35, com "DIVERGÊNCIAS: 0". FONTE 10, MC5: a ligação caso–fonte não é reproduzível sem a lista nominal.
- Tipo: erro demonstrado
- Gravidade: maior
- Correção proposta: Limitar a frase à fração cuja notícia confirma morte violenta e condição LGBT+, e repetir que caso sem notícia achada permanece não verificável. Manter a ressalva de 2023–2025 na mesma frase da seção 2.2.
- Incerteza: Baixa quanto à lógica e às contagens de rótulos. A planilha com nomes não está no repositório.

### GRO-04 — A fatia "firme" do agressor policial repousa em cinco vítimas

- Local: Seção 3.1, parágrafo anterior à Tabela 3; nota da Tabela 3; seção 5.
- Trecho ou alegação: "a única diferença firme de fatia é a de policial, menor entre as vítimas LGB+".
- Problema: Há 5 vítimas LGB+ não ponderadas na categoria policial. O intervalo de Wald da diferença de fatia exclui zero (−1,6 ponto percentual; −2,7 a −0,5), numa de várias comparações feitas depois de ver os resultados, sem correção para o número de testes. A razão bruta de "empregado, patrão ou chefe", 16,52 (3,78 a 72,23), usa o mesmo tamanho e entra na Tabela 3. "Firme", aqui, é o intervalo nominal. A seção 5 avisa que o bloco é exploratório e que a diferença é pequena, e mesmo assim o resultado a destaca como a exceção firme.
- Evidência ou raciocínio verificável: FONTE 4, seção 1 (policial: diferença firme no critério do intervalo) e seção 6 (policial 66 e 5; empregado/patrão 39 e 5). O manuscrito, na nota da Tabela 3, informa o n = 5 só para "outro". A função de diferença em `dados/pns/agressor_risco_pns2019.py` usa estimativa ± 1,96 erro-padrão.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Retirar "firme" dessa célula, ou condicioná-la ao n = 5 e à ausência de correção. Na Tabela 3, pôr o n não ponderado ao lado de 16,52.
- Incerteza: Não refiz a linearização. O intervalo publicado confere com o arquivo. A crítica é de leitura, não de conta.

### GRO-05 — A Tabela 2 junta ajustes que foram feitos separados

- Local: Tabela 2, linha 6. A seção 3.1 os separa.
- Trecho ou alegação: "A diferença persiste depois do ajuste por sexo, idade, cor, instrução, região, estado civil e modo de entrevista (razão de 2,65 a 2,82)".
- Problema: 2,82 é o ajuste-base. 2,65 é esse ajuste mais estado civil. 2,68 é o ajuste-base mais o modo. 2,64 é o ajuste-base mais cônjuge no domicílio. Não há um modelo com estado civil e modo ao mesmo tempo. A faixa 2,65 a 2,82 deixa 2,64 de fora e lê duas especificações como uma.
- Evidência ou raciocínio verificável: FONTE 4, seção 3 (2,82; 2,65; 2,64) e seção 5 (2,68). FONTE 1, linha A25, repete a formulação "razão de 2,65 a 2,82".
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: "Em ajustes separados: 2,82; com estado civil, 2,65; com cônjuge no domicílio, 2,64; com o modo, 2,68."
- Incerteza: Nenhuma sobre os quatro números.

### GRO-06 — "As taxas que melhor se ajustam" são três valores fixados de antemão

- Local: Seção 3.2, parágrafo da Equação 1 e da Figura 5.
- Trecho ou alegação: "As taxas a seguir são as que melhor se ajustam aos quatro anos, e não a taxa entre a primeira e a última contagem."
- Problema: Violência parada, +15% ao ano e −5% ao ano estão fixos no programa. O ajuste estima o nível e a propensão de registro. Qualquer par com o mesmo produto (1 + crescimento da violência) × (1 + crescimento do registro) tem o mesmo erro. "Melhor se ajustam" sugere que os dados escolheram essas três histórias.
- Evidência ou raciocínio verificável: `simulacao/sim_identificabilidade.py`: `CENARIOS = {"S1 incidencia constante": 0.00, "S2 incidencia +15%/ano": 0.15, "S3 incidencia -5%/ano": -0.05}`. FONTE 10, MC3, passo 3: as três histórias têm soma de quadrados em log de 0,0472; os produtos 1,00 × 1,637, 1,15 × 1,423 e 0,95 × 1,723 coincidem. A série 783, 1.633, 2.567 e 3.481 confere com o texto.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: "Três histórias compatíveis com o mesmo crescimento do produto, com o crescimento da violência escolhido e o do registro ajustado."
- Incerteza: Baixa. A não identificabilidade, que é o ponto do artigo, permanece.

### GRO-07 — Goodman-Bacon é citado como apoio de um modelo ao qual o próprio material diz que ele não se aplica

- Local: Seção 2.5, frase do painel de governos.
- Trecho ou alegação: "modelos de painel com efeitos fixos duplos descrevem se trocas de partido acompanham variações nas mortes, sem atribuir causa (Goodman-Bacon, 2021)".
- Problema: A citação funciona como fundamento da descrição "sem atribuir causa". O Material Complementar diz o contrário sobre o alcance do método: a decomposição foi feita para tratamento binário com adoção escalonada e "não se aplica literalmente" a um escore contínuo e reversível.
- Evidência ou raciocínio verificável: FONTE 10, MC1, parágrafo do painel de governadores. O PDF de Goodman-Bacon (2021) não está no pacote nem nesta cópia do repositório: o conteúdo integral do artigo, não verificado. O descompasso entre a frase do corpo e a descrição do MC1 está no pacote.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Citar Goodman-Bacon como limite do estimador de efeitos fixos, não como respaldo da frase descritiva. A ressalva de tendências paralelas, já na seção 5, pode subir para a seção 2.5.
- Incerteza: O teor do artigo de 2021, fora a descrição do próprio MC, não verificado.

### GRO-08 — A tabela histórica conta 7 diplomatas onde o material conta 15, dos quais 7

- Local: Tabela 5, linha "Brasil, ditadura militar, 1964 a 1985".
- Trecho ou alegação: "Demissões (7 diplomatas em 1969), censura e rondas policiais, sem política formal de extermínio".
- Problema: No material do próprio estudo, 15 diplomatas foram cassados em 1969, e 7 o foram por "prática de homossexualismo". A célula do corpo transforma o subconjunto na contagem inteira.
- Evidência ou raciocínio verificável: `paper/v05/MATERIAL-COMPLEMENTAR.md`, Tabela MC8.9: "15 diplomatas cassados em 1969, 7 deles por 'prática de homossexualismo'". `dados/regimes/H-RELATORIO.md` e `dados/regimes/ASTRA-B2.md` repetem 15 e 7. O PDF da Comissão Nacional da Verdade não foi reaberto nesta leitura: a página da fonte, não verificado.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: "15 diplomatas cassados em 1969, 7 pela justificativa de homossexualismo".
- Incerteza: O contraste interno está verificado. A conferência direta com a página da Comissão, não verificado nesta leitura.

### GRO-09 — O controle positivo empilha sexo e raça e apresenta o produto como o que "a variável" mede

- Local: Seção 3.3, parágrafo do controle positivo; Tabela 2, linha 14.
- Trecho ou alegação: "51,7 contra 2,6 mortes por agressão por 100 mil... 19,9 vezes menos. Isso mostra que o sistema mede a desigualdade quando a variável está preenchida."
- Problema: O par é homem negro contra mulher não negra. No mesmo cálculo, a razão homens/mulheres é 10,8 e a razão negros/não negros é 2,56. O corpo usa o cruzamento extremo para dizer que o sistema mede a desigualdade quando o campo existe. Os denominadores de 2023 e 2024 são extrapolados do Censo de 2022, a sensibilidade não foi testada, e o corpo não diz isso. A conta 51,7/2,6 = 19,9 está certa.
- Evidência ou raciocínio verificável: FONTE 10, MC4, texto da seção 3.3 e Tabelas MC4.5 e MC4.A16. FONTE 2 marca A19 como conferido contra `dados/sim/asr_brasil.md`.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Ao lado de 19,9, informar as razões de sexo e de raça, e dizer no corpo que 2023–2024 usam população extrapolada.
- Incerteza: Baixa para as três razões, que estão no MC4. Não reabri o microdado do Sistema de Informações sobre Mortalidade.

### GRO-10 — A taxa de suicídio do escritório britânico entra sem janela e sem unidade de tempo

- Local: Seção 3.4, segundo parágrafo. A expectativa de vida experimental está no parágrafo seguinte da mesma seção.
- Trecho ou alegação: "a taxa padronizada de suicídio, que inclui mortes de intenção indeterminada, foi de 50,3 contra 23,1 por 100 mil, cerca de 2,2 vezes (ONS, 2025)".
- Problema: O corpo não informa março de 2021 a dezembro de 2023 nem se 50,3 é taxa anual ou do período. Para todas as causas, o registro interno cita o boletim: as taxas não foram calculadas como taxas anuais. Para o suicídio, o mesmo registro não traz essa frase. A razão 50,3/23,1 ≈ 2,2 independe dessa escolha; o nível absoluto, não. No mesmo bloco, o Material Complementar registra o aviso de que a expectativa de vida experimental tende a superestimar; o corpo dá −1,2 e −0,9 ano aos 20 anos sem esse aviso.
- Evidência ou raciocínio verificável: FONTE 10, MC4, traz a janela do suicídio na mesma frase e o aviso sobre a expectativa de vida. `paper/figures/fontes/L-SECAO-3-3-PROPOSTA.md` cita, para todas as causas, "were not calculated as annual rates" e localiza 1,31 (1,28 a 1,33) na Tabela 5, linha 7, da planilha oficial. `paper/figures/fontes/estudos_mortalidade.tsv` rotula 982,8 e 752,6 como "por 100 mil no período" e 50,3 só como "suicídio por 100 mil". Os boletins em HTML não estão nesta cópia: não verificado além dessas transcrições. FONTE 1 diz que o intervalo 1,28 a 1,33 "não foi amarrado a uma célula"; o arquivo de proposta, posterior, cita a célula. Não reabri a planilha.
- Tipo: suspeita que exige verificação
- Gravidade: menor
- Correção proposta: Repetir a janela no corpo. Chamar 50,3 e 23,1 de taxa anual só se o boletim de 2025 o disser. Incluir o aviso de superestimação da expectativa de vida experimental.
- Incerteza: Alta para a unidade de tempo do suicídio. A omissão da janela no corpo, em relação ao MC4, está verificada.

### GRO-11 — "Acurácia de 93,3%" fica sem o que foi medido

- Local: Seção 6, parágrafo das três mudanças que alterariam as respostas.
- Trecho ou alegação: "A ligação entre bases brasileiras já mostrou acurácia de 93,3% no Rio de Janeiro (Rafael et al., 2024)."
- Problema: A frase vem depois de "registrar orientação e identidade no óbito, ou ligar o óbito a uma fonte que as registre". O Material Complementar lê 93,3% como acurácia da vinculação probabilística entre fichas de violência e óbitos no Rio de Janeiro, sem taxa populacional. O corpo não diz o numerador dessa acurácia. A leitura como acerto na identificação de mortes LGBT+ fica disponível.
- Evidência ou raciocínio verificável: FONTE 10, MC4: "vinculação probabilística entre as fichas do Sinan e os óbitos do SIM no Rio de Janeiro tem acurácia de 93,3%, sem gerar taxa populacional". O PDF de Rafael et al. (2024) não está no pacote: não verificado contra o artigo.
- Tipo: suspeita que exige verificação
- Gravidade: menor
- Correção proposta: "acurácia de 93,3% na vinculação probabilística entre fichas e óbitos no Rio de Janeiro, sem produzir taxa de mortalidade LGBT+".
- Incerteza: O número no artigo-fonte, não verificado. O descompasso entre a frase solta e o MC4 está no pacote.

### GRO-12 — 258.011 discursos entram como universo fechado

- Local: Seção 3.7, parágrafo do Parlamento; seção 5, quinta limitação.
- Trecho ou alegação: "Nos 258.011 discursos da Câmara e do Senado, 49 falas afirmam ou repetem esse suposto recorde mundial... Só uma delas cita fonte primária".
- Problema: O Material Complementar registra até 5,1% da Câmara sem a última página e texto integral do Senado só para 375 candidatos. O corpo apresenta 258.011 como o conjunto em que as 49 falas foram contadas. O dicionário foi revisto depois da primeira contagem, com a família dessa frase caindo de 161 para 56, desvio que fica no complemento. Os dois codificadores são modelos de linguagem. O κ de fonte é 0,66 (0,31 a 0,93): a estimativa pontual passa o limiar de 0,60 escrito antes; o intervalo inclui valores abaixo dele. "Fonte primária" é documento com autor e ano, não fonte que meça o recorde. A seção 5 já diz que a comparação com a linha de base é indicativa.
- Evidência ou raciocínio verificável: FONTE 10, MC9 (258.011 = 219.562 + 38.449; cobertura; κ; Tabela MC9.A18, Fisher p = 0,58 e p = 0,19) e Apêndice B (dicionário revisto depois da primeira contagem). FONTE 2 confere "1 de 49" e "0 de 49" contra `r7_parlamento_sensibilidade.md`. Não recontei os discursos.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: No corpo, dizer que 258.011 é o corpus baixado, com as falhas de cobertura do MC9, e que o intervalo do κ de fonte atravessa o limiar de 0,60.
- Incerteza: A contagem bruta de 258.011, não refeita nesta leitura. A ressalva de cobertura está no MC9.

### GRO-13 — A introdução anuncia a busca de atos federais e o corpo não dá o resultado assimétrico

- Local: Seção 1, quarto parágrafo; seção 3.7, primeiro parágrafo.
- Trecho ou alegação: "Vemos ainda se os seis mandatos federais recentes perseguiram pessoas LGBT+ em 60 buscas iguais (Material Complementar MC7)."
- Problema: A seção 3.7 só remete ao MC7. O resultado que não é simétrico fica de fora do corpo: nenhuma perseguição no espaço da busca, e 10 atos de proteção, todos em mandatos do PT, com cobertura de imprensa desigual entre épocas. A retirada está registrada. O leitor que ficar no artigo não vê o lado da busca que a "mesma régua" da introdução prometeu examinar.
- Evidência ou raciocínio verificável: FONTE 1, mudanças da revisão r5 ("atos de governo só existem no papel") e linhas A12 e A22. FONTE 10, Tabela MC7.8: proteções 1, 5, 3, 0, 0 e 1 nos seis mandatos; perseguição 0; nota de cobertura desigual. FONTE 2 confere a soma.
- Tipo: preferência editorial
- Gravidade: menor
- Correção proposta: Uma frase na seção 3.7 com os três números e a ressalva de cobertura. O detalhe pode continuar no MC7.
- Incerteza: Nenhuma sobre a omissão no corpo. Não refiz as 60 consultas.

## Pontos fortes

- A escada de quatro níveis impede ler disparidade, boletim ou lista de notícias como motivo, taxa ou tendência, e o artigo aplica essa régua aos dois lados do debate.
- A reanálise da PNS reproduz as seis prevalências de Vasconcelos et al. (2023) com divergência zero na tolerância de 0,05 ponto percentual e troca razões de chance por razões de prevalência, com variância do desenho (574 estratos, 8.027 unidades primárias). O que foi feito depois de ver os resultados está rotulado na tabela, na seção 5 e na conclusão.
- A Equação R = I × p mostra, com o mesmo erro, que a série de 783 a 3.481 boletins cabe em violência parada, subindo ou caindo. O ponto metodológico permanece; o que falha é só o adjetivo "melhor".
- A genealogia de "35 anos", do estudo retratado dos "12 anos" e de "o país que mais mata" chega a documento primário ou a ausência documentada de comparação, com a idade média das vítimas separada da expectativa de vida.
- Há desvios datados em relação aos protocolos, placebo de 2018 para a queda de homicídios (−21,8% antes da posse), soma da causa indeterminada, e código que reproduz as contagens principais. O depósito de dados é citado uma vez, na disponibilidade de dados.

Nada pendente neste parecer.