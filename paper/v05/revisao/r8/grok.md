Vou conferir a matriz contra o manuscrito revisado e os arquivos do repositório, sem alterar nada.A matriz afirma correções no complemento e nas figuras. Vou cruzar esses pontos com os arquivos da pasta, não só com o diff do corpo.Vou conferir no repositório as frases que sustentam o veredito, para o parecer citar o arquivo e não a matriz.## Verificação

A rodada confere o diff r7 para r8 e os arquivos do repositório. `confere_quadro.py` e `make_provenance.py --verify` não foram reexecutados nesta sessão. Os pixels dos PNG não foram abertos; o texto das figuras foi lido no SVG.

| ID | Veredito | Por quê |
|---|---|---|
| AST-02 | resolvida | O MC3 diz "fichas não marcadas como violência autoprovocada", com 53,4% em 2015 e 42,5% a 44,5% em 2023–2025; a nota da Figura MC3.12 traz "notificações do ano não marcadas como violência autoprovocada" e "42,5% a 53,4%" (`paper/v05/MATERIAL-COMPLEMENTAR.md`, linhas 370 e 378). |
| AST-06 | resolvida | O SVG traz "80% de poder para aumento de 60,7% ou mais" e "para detectar aumento de 30%" (`paper/figures/fig17_tamanho_de_survey.svg`); o cabeçalho da Tabela MC10.10 é "Aumento relativo detectável com 80% de poder (física / qualquer)" (linha 1198). |
| AST-R2-01 | resolvida em parte | A prosa, a nota da Figura MC6.20 e o título da Tabela MC6.A13 tratam o deslocamento como sensibilidade à data na série inteira, com a queda observada de 31,47 (2017) para 27,61 (2018); a coluna e as células continuam "placebo (ano)" e "placebo dispara com o mesmo sinal" (linhas 979–984). |
| ARG-R2-01 | resolvida em parte | É o mesmo conserto da linha anterior: o leitor da Tabela MC6.A13 ainda lê "placebo" na coluna e na leitura pré-registrada (linha 984). |
| ARG-R2-02 | resolvida | A nota da tabela de fatias do MC2 define "firme" como intervalo nominal de 95% sem correção para o número de comparações e apoia a categoria policial em 5 vítimas LGB+ (linha 280). |
| ARG-07 | resolvida | A seção 2.5 cita "Kitagawa (1955)"; a referência completa está no corpo (`paper/v05/MANUSCRITO.md`, linha 497) e em `paper/v05/referencias.md` (linha 87). |
| AST-01 | resolvida em parte | A nota da Tabela MC5.C0 declara que o efeito dos desacordos sobre as contagens não foi estimado (linha 662); a seção 2.6 publica κ = 0,91 e κ = 0,46 e não repete essa frase. A recontagem não foi feita. |
| GRO-02 | resolvida em parte | A seção 3.1 diz que o ajuste pelo modo "não corrige quem deixou de se declarar LGB+, efeito que não foi estimado". A realocação extrema de quem não declarou orientação continua sem cálculo. |
| AST-R2-02 | resolvida em parte | A nota da Tabela MC2.A2 registra que a cor ou raça ignorada entra na referência com os não negros e que "o efeito dessa regra sobre as razões ajustadas não foi recalculado" (linha 193). |
| ARG-01 | resolvida em parte | A nota da Tabela 6 deixou de exigir preenchimento privado; os três desenhos seguem com 1,89% (2.161 e 5.212 adultos LGB+) e não foram refeitos com 1,38% nem com 3,51%. |
| ARG-02 | resolvida em parte | A seção 3.1 declara que o ajuste por cônjuge no domicílio (razão 2,64) vale só para a violência física geral e que a razão por familiar não desconta com quem a pessoa mora. Essa razão por tipo de agressor não foi reestimada. |
| AST-R2-07 | resolvida em parte | A Tabela 2 (linha 24), a seção 3.7 e o MC5 (linha 692) descrevem comparações de mortes noticiadas de pessoas trans, sem cobertura comum, com a posição do Brasil mudando entre total e taxa. A seção 2.2 ainda diz que a busca "não encontrou" contagens equivalentes entre países (`MANUSCRITO.md`, linha 62), e a justificativa de A7 ainda diz "não existe comparação de taxas entre países" (`paper/v05/QUADRO-E2.md`, linha 49), na mesma linha em que a coluna de exibição já foi corrigida. |
| AST-R2-08 | resolvida | A nota da Tabela 6 trata 1,89% como hipótese de planejamento e diz que a diferença 1,38% / 3,51% pode vir de quem respondeu em cada modo. O script contrasta V00101 (quem preencheu), não V001 (privacidade). |
| AST-R2-09 | resolvida | `paper/figures/make_figures.py` (linha 426) rotula p ≥ 0,05 como "mudança anterior não detectada"; o SVG traz p = 0,68 e p = 0,22 nessa fórmula e p = 0,009 e p = 0,028 como "já mudava antes", alinhados a `p_antecipacoes` do desenho estrito e do truncado para `tx_total`. |
| AST-R2-10 | resolvida | O MC6 (linha 735) diz "10 estados distintos de controle em cada direção (15 e 16 estados no conjunto)". No CSV, desenho estrito e `tx_total`: `n_ufs_controle` 10 e 10, `G` 15 e 16 (`dados/painel/c03_event_pesos_resultados.csv`). |
| ARG-R2-03 | resolvida | O MC5 (linha 688) separa o recorte dos autores (227/258 = 88% e 31/258 = 12,0%) da planilha inteira (286/347 = 82,4% e 31/347 = 8,9%) e afirma que inconclusivo não é ausência de preconceito. |
| ARG-R2-04 | resolvida em parte | A seção 4.1 inclui "Para amigo, colega ou vizinho, ele só aparece sem o estado civil", e a nota da Tabela MC1.3 aponta "(MC12)" (linha 79). A seção 6 (linha 385) omite essa exceção, ao contrário do que a matriz afirma, e a seção 4.3 (linha 361) fala em excesso para parceiro ou ex, familiar e desconhecido sem estado civil e sem a exceção. Com estado civil, a razão para amigo, colega ou vizinho é 1,87 (0,90 a 3,89). |

17 linhas: 10 resolvidas, 7 resolvidas em parte, 0 não resolvidas, 0 refutações. Nenhuma crítica nova.

# Parecer — Grok 4.7 (grok-4.7)

## Avaliação geral

Revisão menor. O núcleo permanece de pé: na PNS 2019, adultos LGB+ relatam violência física de 14,70% contra 3,82%, com razão de prevalência ajustada 2,82 (intervalo de 95%, 2,16 a 3,68), e as bases públicas não sustentam taxa nacional de mortalidade LGBT+, indicador de motivo nem leitura causal de governo. A Equação 1 (*R* = *I* × *p*) continua a separar registro de ocorrência. Os consertos desta rodada fecham filtro do Sinan, poder da figura, Kitagawa (1955), LiHS em dois universos, modo de preenchimento, rótulos da Figura MC6.18 e a contagem de estados de controle. Ficam três propagações curtas, já marcadas em parte na tabela: a seção 2.2 e a justificativa de A7; a coluna "placebo" da Tabela MC6.A13; a exceção de amigo, colega ou vizinho ausente nas seções 4.3 e 6. As cinco análises declaradas como não feitas (AST-01, GRO-02, AST-R2-02, ARG-01, ARG-02) seguem como limite, sem cálculo novo. Isso pede revisão menor, não revisão maior.

## Críticas

Nenhuma crítica nova. Os resíduos desta rodada são propagação incompleta de AST-R2-07, AST-R2-01, ARG-R2-01 e ARG-R2-04 e estão na tabela acima. Não há regressão introduzida pelo diff.

## Pontos fortes

- A reanálise da PNS reproduz as prevalências publicadas e separa razão de prevalência de razão de chance, com a fatia entre vítimas distinta do risco na população e com a análise por agressor marcada como posterior aos resultados.
- O controle positivo por sexo e raça (51,7 contra 2,6 mortes por agressão por 100 mil) mostra o que o sistema mede quando o campo existe, e o texto recusa a inferência de que criar o campo bastaria.
- O dado da Inglaterra e do País de Gales entra como mortalidade geral descritiva (razão 1,31), com a ressalva de que não é homicídio nem vale para o Brasil.
- A mesma régua alcança a frase parlamentar sem fonte e a checagem da Liga Humanista, com inconclusivo separado de ausência de preconceito.
- O depósito de dados é citado uma vez, na disponibilidade de dados.

Nada pendente nesta rodada além das sete linhas "resolvida em parte".