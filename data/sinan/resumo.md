# Sinan VIVA — completude dos campos 55/36/37 e contexto por sexo (microdados DATASUS, VIOLBR23/24)

> [2026-10-21] Nota de números: 'precisariam ter 15,6%/15,7% LGB+' abaixo é o cenário B (PNS 6,90%, denominador antigo do dossiê); em `triangulacao_pns_sinan.md` o cenário A (PNS 7,13%, só quem respondeu orientação, comparável ao Sinan) dá 16,5%/16,7%; os dois estão certos no próprio cenário.

> [2026-10-21] Reprodução: as seções 'Denominador só INTERPESSOAL', 'Triangulação' e 'Sensibilidade' saem de `triangulacao_pns_sinan.py` (48 números conferidos sem divergência; versão com IC em `triangulacao_pns_sinan.md`); as duas tabelas da série saem de `serie_tabelas.py` (conferidas linha a linha). `completude_sinan.py` agora escreve `completude_2023_2024.md` e não sobrescreve este arquivo.

Nota de denominadores: "não se aplica" (88) é código previsto para violência autoprovocada; em notificações interpessoais conta como faltante EFETIVO. Reportar sempre os dois: estrito (ignorado+branco) e efetivo (ignorado+branco+NA). SIM via TabNet usa só X85-Y09 (o Atlas soma Y35-Y36).

## 2023: 588,388 notificações no Brasil (autoprovocadas: 182,447, 31.0%)
- campo 55 motivação: sexismo 83,772 (14.2%); LGBTfobia 2,714 (0.5%); racismo 576 (0.1%); intol_religiosa 283 (0.0%); xenofobia 297 (0.1%); conflito_geracional 53,938 (9.2%); situacao_rua 6,162 (1.0%); deficiencia 4,606 (0.8%); outros 161,862 (27.5%); nao_se_aplica 92,863 (15.8%); ignorado 176,750 (30.0%); branco 4,565 (0.8%)
- campo 36 orientação sexual: hetero 322,538 (54.8%); homo 13,353 (2.3%); bi 4,752 (0.8%); nao_se_aplica 111,796 (19.0%); ignorado 133,737 (22.7%); branco 2,212 (0.4%)
- campo 37 identidade de gênero: travesti 1,143 (0.2%); mulher_trans 5,551 (0.9%); homem_trans 2,332 (0.4%); nao_se_aplica 402,658 (68.4%); ignorado 169,851 (28.9%); branco 6,853 (1.2%)
- contexto (interpessoal, % das notificações do sexo): CONJ F 20.2% / M 6.0%; EXCON F 10.2% / M 1.7%; NAMO F 5.2% / M 1.2%; PAI F 8.1% / M 17.4%; MAE F 9.1% / M 23.6%; CONHEC F 12.1% / M 14.7%; DESCO F 9.4% / M 16.0%; POL F 0.3% / M 1.6%
- campo 55 ignorado+branco por UF (pior 5): DF 61% (LGBTfobia 0.3%, n=11,421); PB 56% (LGBTfobia 0.4%, n=5,085); MS 55% (LGBTfobia 0.7%, n=13,077); RN 50% (LGBTfobia 0.3%, n=5,156); AC 49% (LGBTfobia 0.2%, n=2,263)
- campo 55 ignorado+branco por UF (melhor 5): ES 21% (LGBTfobia 0.3%, n=17,028); MT 19% (LGBTfobia 0.5%, n=5,606); AM 19% (LGBTfobia 0.2%, n=8,398); MA 15% (LGBTfobia 0.8%, n=5,199); RR 11% (LGBTfobia 0.0%, n=2,620)

## 2024: 616,548 notificações no Brasil (autoprovocadas: 189,926, 30.8%)
- campo 55 motivação: sexismo 88,207 (14.3%); LGBTfobia 2,818 (0.5%); racismo 787 (0.1%); intol_religiosa 321 (0.1%); xenofobia 309 (0.1%); conflito_geracional 59,919 (9.7%); situacao_rua 6,133 (1.0%); deficiencia 5,025 (0.8%); outros 173,412 (28.1%); nao_se_aplica 96,658 (15.7%); ignorado 177,885 (28.9%); branco 5,074 (0.8%)
- campo 36 orientação sexual: hetero 339,486 (55.1%); homo 13,736 (2.2%); bi 4,742 (0.8%); nao_se_aplica 120,916 (19.6%); ignorado 134,875 (21.9%); branco 2,793 (0.5%)
- campo 37 identidade de gênero: travesti 1,151 (0.2%); mulher_trans 5,622 (0.9%); homem_trans 2,522 (0.4%); nao_se_aplica 426,453 (69.2%); ignorado 172,171 (27.9%); branco 8,629 (1.4%)
- contexto (interpessoal, % das notificações do sexo): CONJ F 19.4% / M 5.5%; EXCON F 10.0% / M 1.7%; NAMO F 5.2% / M 1.1%; PAI F 8.6% / M 18.3%; MAE F 10.2% / M 25.6%; CONHEC F 12.6% / M 15.0%; DESCO F 9.7% / M 15.9%; POL F 0.3% / M 1.6%
- campo 55 ignorado+branco por UF (pior 5): PB 58% (LGBTfobia 0.3%, n=5,993); MS 53% (LGBTfobia 0.5%, n=13,553); RN 51% (LGBTfobia 0.4%, n=5,548); DF 51% (LGBTfobia 0.3%, n=11,070); BA 47% (LGBTfobia 0.6%, n=22,505)
- campo 55 ignorado+branco por UF (melhor 5): AM 17% (LGBTfobia 0.5%, n=9,211); AP 17% (LGBTfobia 0.3%, n=988); ES 16% (LGBTfobia 0.3%, n=20,914); MA 16% (LGBTfobia 0.7%, n=6,089); RR 13% (LGBTfobia 0.2%, n=2,470)

## Denominador só INTERPESSOAL (LES_AUTOP != 1)
- 2023: 405,941 interpessoais. Campo 55: ignorado+branco 29.3%, não se aplica 14.9%, sexismo 20.3%, LGBTfobia 0.54% (2,173); entre as com resposta válida (excl. ign/branco/NA): LGBTfobia 0.96%. Campo 36: ignorado+branco 19.0%, não se aplica 24.7%, homo 1.80%, bi 0.67%; entre válidas: homo+bi 4.39%. Campo 37: ignorado+branco 26.1%, NA 72.5%, trans 1.39% (5,659).
- 2024: 426,622 interpessoais. Campo 55: ignorado+branco 27.7%, não se aplica 14.8%, sexismo 20.4%, LGBTfobia 0.53% (2,264); entre as com resposta válida (excl. ign/branco/NA): LGBTfobia 0.92%. Campo 36: ignorado+branco 18.4%, não se aplica 25.6%, homo 1.74%, bi 0.67%; entre válidas: homo+bi 4.31%. Campo 37: ignorado+branco 25.7%, NA 73.0%, trans 1.34% (5,716).

## Triangulação PNS x Sinan: violência FÍSICA, adultos 18+, interpessoal (ORIENT_SEX entre respostas válidas)
- 2023: 197,779 notificações de violência física em adultos 18+; orientação ignorado+branco 20.4%, 'não se aplica' 3.9%, válidas 75.7%; homo+bi entre válidas = 4.12% (6,169). Campo 55 neste recorte: ignorado+branco 27.5%, NA 11.5% -> faltante efetivo 39.0%.
- 2024: 202,416 notificações de violência física em adultos 18+; orientação ignorado+branco 20.2%, 'não se aplica' 4.0%, válidas 75.8%; homo+bi entre válidas = 4.08% (6,260). Campo 55 neste recorte: ignorado+branco 27.0%, NA 11.5% -> faltante efetivo 38.5%.
- PNS 2019 implica: parcela LGB+ entre adultos que sofreram violência física em 12 meses ≈ 6.9% (1,89% x 14,70% vs 98,11% x 3,82%).

## Série 2015-2025 (só interpessoal; serie_campo55_uf_ano.csv; microdados DATASUS VIOLBR15-25, 2025 = arquivo FINAIS/PRELIM conforme disponível)
| ano | n | campo 55 ign+branco % | NA % | faltante efetivo % | LGBTfobia % | orient. ign % | homo+bi % (de todas) | trans % |
|---|---|---|---|---|---|---|---|---|
| 2015 | 188,212 | 38.35 | 15.02 | 53.4 | 0.5 | 30.72 | 1.81 | 1.37 |
| 2016 | 197,770 | 33.3 | 17.44 | 50.7 | 0.39 | 24.99 | 1.88 | 1.73 |
| 2017 | 239,166 | 33.11 | 16.15 | 49.3 | 0.38 | 24.6 | 1.89 | 1.25 |
| 2018 | 261,082 | 31.34 | 16.1 | 47.4 | 0.45 | 22.43 | 2.04 | 1.31 |
| 2019 | 278,819 | 30.13 | 15.67 | 45.8 | 0.49 | 19.67 | 2.07 | 1.17 |
| 2020 | 229,213 | 31.24 | 15.26 | 46.5 | 0.46 | 18.73 | 2.24 | 1.27 |
| 2021 | 256,993 | 31.19 | 15.64 | 46.8 | 0.49 | 19.68 | 2.31 | 1.27 |
| 2022 | 302,524 | 30.26 | 15.74 | 46.0 | 0.5 | 20.72 | 2.49 | 1.34 |
| 2023 | 405,941 | 29.27 | 14.88 | 44.1 | 0.54 | 19.01 | 2.47 | 1.39 |
| 2024 | 426,622 | 27.66 | 14.81 | 42.5 | 0.53 | 18.37 | 2.41 | 1.34 |
| 2025 | 475,857 | 29.72 | 14.75 | 44.5 | 0.51 | 23.17 | 2.39 | 1.3 |

| UF | faltante efetivo 2015-17 % | 2023-25 % | variação p.p. | LGBTfobia média % | n 2015-25 |
|---|---|---|---|---|---|
| PB | 53.5 | 75.3 | +21.8 | 0.76 | 27,190 |
| TO | 64.1 | 67.0 | +2.9 | 0.43 | 39,748 |
| MS | 58.8 | 63.0 | +4.2 | 0.41 | 82,927 |
| AC | 50.5 | 61.6 | +11.0 | 0.25 | 13,524 |
| BA | 68.1 | 59.2 | -8.9 | 0.58 | 122,102 |
| RN | 68.5 | 59.0 | -9.5 | 0.40 | 23,801 |
| RO | 69.0 | 57.1 | -11.8 | 0.38 | 11,052 |
| AL | 57.3 | 56.4 | -0.9 | 0.46 | 38,917 |
| CE | 65.8 | 51.7 | -14.1 | 0.62 | 116,878 |
| GO | 49.5 | 50.4 | +0.9 | 0.50 | 89,099 |
| DF | 71.2 | 47.8 | -23.4 | 0.57 | 36,021 |
| AM | 67.9 | 47.8 | -20.2 | 0.44 | 57,524 |
| RJ | 76.0 | 47.1 | -28.9 | 0.41 | 377,846 |
| MG | 43.4 | 46.2 | +2.8 | 0.39 | 348,154 |
| PR | 29.9 | 45.0 | +15.1 | 0.36 | 299,597 |
| MT | 43.7 | 44.6 | +0.9 | 0.56 | 28,371 |
| AP | 62.1 | 43.0 | -19.1 | 0.30 | 5,825 |
| PI | 62.6 | 42.5 | -20.0 | 0.28 | 32,071 |
| PE | 48.0 | 41.2 | -6.8 | 0.45 | 165,745 |
| SC | 42.1 | 40.9 | -1.3 | 0.45 | 106,421 |
| SE | 87.6 | 39.3 | -48.3 | 0.36 | 17,667 |
| SP | 48.8 | 38.1 | -10.7 | 0.61 | 813,266 |
| PA | 59.4 | 36.2 | -23.2 | 0.37 | 86,496 |
| MA | 49.1 | 35.6 | -13.5 | 0.59 | 34,102 |
| RS | 43.7 | 29.5 | -14.2 | 0.39 | 189,443 |
| RR | 49.1 | 24.1 | -25.0 | 0.33 | 12,997 |
| ES | 45.3 | 21.9 | -23.5 | 0.40 | 85,415 |

Leitura: faltante efetivo nacional caiu de 53,4% (2015) para 42-45% (2023-25): melhora lenta de ~9 p.p. em 11 anos, ainda com quase metade das notificações sem motivação válida; 'não se aplica' ficou cravado em ~15% (comportamento de preenchimento padrão, não de fenômeno); pioraram >5 p.p.: ['PB', 'AC', 'PR']; melhoraram >5 p.p.: ['BA', 'RN', 'RO', 'CE', 'DF', 'AM', 'RJ', 'AP', 'PI', 'PE', 'SE', 'SP', 'PA', 'MA', 'RS', 'RR', 'ES']; UFs com LGBTfobia média <0,2% e n>20 mil (candidatas a 'zero cerimonial'): [].

## Sensibilidade à não resposta de orientação (violência física, adultos, interpessoal)
PNS 2019 implícito: 6.90% LGB+ entre adultos com violência física em 12 m.
| ano | cenário p/ não respondidas (24% das notificações) | parcela LGB+ total no Sinan | razão Sinan/PNS |
|---|---|---|---|
| 2023 | MCAR: igual à observada | 4.12% | 0.60 |
| 2023 | 0,5x observada | 3.62% | 0.52 |
| 2023 | 2x observada | 5.12% | 0.74 |
| 2023 | pior caso: 0% | 3.12% | 0.45 |
| 2023 | melhor caso: 100% | 27.42% | 3.97 |
| 2023 | para igualar a PNS, não respondidas precisariam ter 15.6% LGB+ | 6.90% | 1.00 |
| 2024 | MCAR: igual à observada | 4.08% | 0.59 |
| 2024 | 0,5x observada | 3.59% | 0.52 |
| 2024 | 2x observada | 5.07% | 0.73 |
| 2024 | pior caso: 0% | 3.09% | 0.45 |
| 2024 | melhor caso: 100% | 27.29% | 3.95 |
| 2024 | para igualar a PNS, não respondidas precisariam ter 15.7% LGB+ | 6.90% | 1.00 |
Leitura: sob MCAR o Sinan dá ~4,1% (razão 0,6 da PNS); para igualar a PNS, as 24% não respondidas precisariam ser ~15-16% LGB+ (quase 4x a parcela observada), o que é implausível como única explicação; a diferença residual é compatível com (a) não resposta diferencial moderada (LGB+ omitem mais a orientação no serviço de saúde) somada a (b) menor procura de serviço de saúde por LGB+ vitimizados e (c) diferença de instrumento (PNS = autorrelato em 12 m; Sinan = notificação do profissional). Em todos os cenários exceto o pior caso extremo, a parcela LGB+ fica entre 2x e 3,6x a prevalência populacional (1,89%): a direção da sobre-representação é robusta; a magnitude não é identificada entre 2x e 3,7x.

## SIM microdados: óbitos por agressão (X85-Y09) em adultos 18+ (DOBR2023/2024.dbc, FTP DATASUS)
- 2023: total 43,443; 18+ 40,683 (93.6%); <18 2,152; idade ignorada 608; 18+ homens 37,178, mulheres 3,504. Taxa adulta aproximada (denominador Censo 2022 18+ = 154.346.198): 26.4 por 100 mil adultos.
- 2024: total 39,946; 18+ 37,276 (93.3%); <18 2,171; idade ignorada 499; 18+ homens 33,994, mulheres 3,278. Taxa adulta aproximada (denominador Censo 2022 18+ = 154.346.198): 24.2 por 100 mil adultos.
