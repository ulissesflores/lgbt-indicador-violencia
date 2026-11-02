# Quem agrediu e o risco por tipo de agressor, PNS 2019 (gerado por agressor_risco_pns2019.py)

Desenho complexo; intervalos de 95%. A PNS não pergunta o motivo nem a orientação sexual do agressor. Vítimas de violência física em 12 meses: 3112 heterossexuais e 179 LGB+ (n da amostra).

Reprodução de seguro_pns2019.md (6 fatias, tolerância 0,01 p.p.): divergências = 0.

## 1. Entre as vítimas de violência física: quem agrediu (fatia, %)

| Agressor | Heterossexuais | LGB+ | Diferença LGB+ − het (p.p.) | A diferença é firme? |
|---|---|---|---|---|
| Parceiro(a) ou ex | 37,10 (33,23 a 40,97) | 32,92 (18,42 a 47,43) | -4,2 (-19,1 a +10,8) | não (o intervalo inclui zero) |
| Familiar | 19,25 (16,79 a 21,70) | 31,17 (15,38 a 46,96) | +11,9 (-4,0 a +27,8) | não (o intervalo inclui zero) |
| Amigo(a), colega ou vizinho(a) | 15,15 (12,77 a 17,54) | 12,60 (4,25 a 20,96) | -2,5 (-11,2 a +6,1) | não (o intervalo inclui zero) |
| Empregado(a), patrão ou chefe | 1,10 (0,59 a 1,61) | 4,74 (0,00 a 11,31) | +3,6 (-3,0 a +10,2) | não (o intervalo inclui zero) |
| Pessoa conhecida (todos acima) | 72,60 (69,66 a 75,55) | 81,43 (72,85 a 90,02) | +8,8 (-0,2 a +17,8) | não (o intervalo inclui zero) |
| Pessoa desconhecida | 23,02 (20,28 a 25,77) | 16,29 (8,06 a 24,52) | -6,7 (-15,4 a +1,9) | não (o intervalo inclui zero) |
| Policial | 2,19 (1,32 a 3,07) | 0,61 (0,00 a 1,26) | -1,6 (-2,7 a -0,5) | sim |
| Outro | 2,18 (1,24 a 3,12) | 1,67 (0,00 a 3,33) | -0,5 (-2,4 a +1,4) | não (o intervalo inclui zero) |

## 2. Risco na população: adultos agredidos fisicamente em 12 meses por cada tipo de agressor (por 100 adultos)

| Agressor | Heterossexuais | LGB+ | Razão LGB+/het |
|---|---|---|---|
| Parceiro(a) ou ex | 1,42 (1,23 a 1,61) | 4,84 (2,34 a 7,34) | 3,41 (2,01 a 5,79) |
| Familiar | 0,74 (0,63 a 0,84) | 4,58 (1,64 a 7,52) | 6,22 (3,26 a 11,90) |
| Amigo(a), colega ou vizinho(a) | 0,58 (0,48 a 0,68) | 1,85 (0,60 a 3,11) | 3,20 (1,59 a 6,42) |
| Empregado(a), patrão ou chefe | 0,04 (0,02 a 0,06) | 0,70 (0,00 a 1,67) | 16,52 (3,78 a 72,23) |
| Pessoa conhecida (todos acima) | 2,78 (2,55 a 3,01) | 11,97 (8,09 a 15,85) | 4,31 (3,10 a 5,99) |
| Pessoa desconhecida | 0,88 (0,77 a 0,99) | 2,39 (1,21 a 3,57) | 2,72 (1,63 a 4,53) |
| Policial | 0,08 (0,05 a 0,12) | 0,09 (0,00 a 0,18) | 1,07 (0,35 a 3,25) |
| Outro | 0,08 (0,05 a 0,12) | 0,24 (0,01 a 0,48) | 2,93 (1,01 a 8,51) |

## 3. Razão de prevalências ajustada de violência física: o ajuste de seguro_pns2019.py e o mesmo + estado civil (análise feita depois de ver os resultados)

| Ajuste | Razão LGB+/het | n |
|---|---|---|
| sexo, idade, cor, instrução, região, urbano/rural (publicado: 2,82; 2,16 a 3,68) | 2,82 (2,16 a 3,68) | 85913 |
| o mesmo + estado civil (casado, separado, viúvo, solteiro) | 2,65 (2,04 a 3,46) | 85913 |
| o mesmo + cônjuge ou companheiro(a) mora no domicílio | 2,64 (2,02 a 3,44) | 85913 |

Prevalência de violência física por estado civil (descritivo):

| Estado civil | Heterossexuais | LGB+ | n LGB+ |
|---|---|---|---|
| casado | 2,48 (2,09 a 2,88) | 7,23 (2,15 a 12,31) | 165 |
| separado | 4,66 (3,82 a 5,50) | 9,41 (1,86 a 16,96) | 74 |
| viúvo | 2,23 (1,55 a 2,91) | 0,00 (0,00 a 0,00) | 15 |
| solteiro | 5,43 (5,00 a 5,85) | 15,99 (11,43 a 20,56) | 1300 |

Solteiros entre os adultos: heterossexuais 40,79%, LGB+ 84,91%.

Leitura: a razão que sobra depois de qualquer ajuste não é parcela causada por discriminação nem por 'estilo de vida'; os dados não separam as duas explicações (VanderWeele & Robinson, 2014).

## 4. Razão de risco AJUSTADA por tipo de agressor (análise feita depois de ver os resultados)

Desfecho: ter sofrido violência física em 12 meses e ter apontado esse tipo de agressor em V018 (uma resposta por pessoa). Colunas ajustadas: a primeira com o mesmo ajuste do 2,82; a segunda com o estado civil somado; a terceira com o cônjuge ou companheiro(a) no domicílio somado. O n é o mesmo nas três.

| Agressor | Bruta | Ajustada (sexo, idade, cor, instrução, região, urbano/rural) | Ajustada + estado civil | Ajustada + cônjuge no domicílio | n |
|---|---|---|---|---|---|
| Parceiro(a) ou ex | 3,41 (2,01 a 5,79) | 2,50 (1,48 a 4,25) | 2,42 (1,43 a 4,10) | 2,42 (1,44 a 4,07) | 85913 |
| Familiar | 6,22 (3,26 a 11,90) | 4,79 (2,58 a 8,90) | 4,43 (2,38 a 8,26) | 4,31 (2,33 a 7,99) | 85913 |
| Amigo(a), colega ou vizinho(a) | 3,20 (1,59 a 6,42) | 2,12 (1,02 a 4,39) | 1,87 (0,90 a 3,89) | 1,85 (0,89 a 3,83) | 85913 |
| Pessoa conhecida (todos acima) | 4,31 (3,10 a 5,99) | 3,13 (2,28 a 4,29) | 2,93 (2,14 a 4,01) | 2,91 (2,13 a 3,98) | 85913 |
| Pessoa desconhecida | 2,72 (1,63 a 4,53) | 2,05 (1,22 a 3,45) | 1,93 (1,14 a 3,27) | 1,91 (1,12 a 3,26) | 85913 |

## 5. Quem preencheu o módulo de violência (V00101) e fluxo da amostra

- próprio morador: n = 21669; LGB+ entre quem declarou het ou LGB+ = 3,51%; violência física LGB+ 16,74 (10,48 a 22,99), het 5,21 (4,53 a 5,88); razão bruta 3,21 (2,18 a 4,74); n LGB+ = 677
- entrevistador: n = 66862; LGB+ entre quem declarou het ou LGB+ = 1,38%; violência física LGB+ 12,75 (7,74 a 17,76), het 3,32 (3,08 a 3,56); razão bruta 3,84 (2,58 a 5,73); n LGB+ = 877
- Razão ajustada com o modo de preenchimento no ajuste: 2,68 (2,05 a 3,49); n = 85913

Fluxo: 88531 adultos responderam o módulo V; 85913 declararam orientação heterossexual ou LGB+ (fora: não sabe 849, recusou 1769, sem resposta 0); n analítico do ajuste = 85913 (com faixa, instrução e região conhecidas).

## 6. Vítimas na amostra (não ponderado) por tipo de agressor

Critério de omissão do ajuste por tipo de agressor: menos de 10 vítimas LGB+ na categoria.

| Agressor | Vítimas heterossexuais | Vítimas LGB+ |
|---|---|---|
| Parceiro(a) ou ex | 1163 | 69 |
| Familiar | 606 | 33 |
| Amigo(a), colega ou vizinho(a) | 452 | 23 |
| Empregado(a), patrão ou chefe | 39 | 5 |
| Pessoa conhecida (todos acima) | 2260 | 130 |
| Pessoa desconhecida | 726 | 39 |
| Policial | 66 | 5 |
| Outro | 60 | 5 |

## 7. Mora com cônjuge ou companheiro(a) no domicílio (C01001), por grupo e estado civil (ponderado)

- heterossexuais: moram com cônjuge 62,39% (61,73 a 63,05); entre os de estado civil solteiro, 41,36% (40,35 a 42,37); n com resposta = 84359
- LGB+: moram com cônjuge 29,49% (25,40 a 33,57); entre os de estado civil solteiro, 21,38% (17,47 a 25,29); n com resposta = 1554

## 8. Razões ajustadas sem os adultos de cor ou raça ignorada

No ajuste do artigo, quem tem cor ou raça ignorada (C009 = 9) entra na categoria de referência, com os não negros: 8 heterossexuais e 1 LGB+ na amostra. Aqui eles saem do ajuste.

| Desfecho | Ajustada (como no artigo) | Ajustada sem cor ou raça ignorada | n sem cor ignorada |
|---|---|---|---|
| Violência física | 2,82 (2,16 a 3,68) | 2,82 (2,16 a 3,68) | 85904 |
| Violência sexual | 5,00 (3,17 a 7,89) | 5,02 (3,18 a 7,92) | 85904 |
| Violência psicológica | 1,87 (1,66 a 2,11) | 1,87 (1,66 a 2,11) | 85904 |
| Qualquer violência | 1,84 (1,64 a 2,07) | 1,84 (1,64 a 2,07) | 85904 |
| Violência física por parceiro(a) ou ex | 2,50 (1,48 a 4,25) | 2,50 (1,48 a 4,25) | 85904 |
| Violência física por familiar | 4,79 (2,58 a 8,90) | 4,79 (2,58 a 8,90) | 85904 |
| Violência física por amigo(a), colega ou vizinho(a) | 2,12 (1,02 a 4,39) | 2,12 (1,02 a 4,39) | 85904 |
| Violência física por pessoa conhecida (todos acima) | 3,13 (2,28 a 4,29) | 3,13 (2,28 a 4,29) | 85904 |
| Violência física por pessoa desconhecida | 2,05 (1,22 a 3,45) | 2,05 (1,22 a 3,45) | 85904 |

Leitura: a diferença entre as duas colunas é o peso da regra de codificação da cor ou raça ignorada nas razões ajustadas.
