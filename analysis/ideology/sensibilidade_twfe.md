# Sensibilidade do TWFE (painel F8) a safra do escore de ideologia

Mesmo modelo do painel (log(taxa) ~ ideologia + EF UF + EF ano, EP agrupado por UF); so muda a coluna de ideologia. Gerado por scripts/sensibilidade_twfe.py. O painel NAO foi alterado.


## Variante de partido: wiki (partido em exercicio, Wikipedia curada)

| desfecho | variante de ideologia | n | b por ponto | EP | IC95% |
|---|---|---|---|---|---|
| tx_total | atual (BRC 2018 p/ todos os anos) | 351 | +0.0029 | 0.0123 | [-0.021, +0.027] |
| tx_total | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0033 | 0.0115 | [-0.019, +0.026] |
| tx_total | BLS por legislatura (0-10) | 348 | +0.0054 | 0.0091 | [-0.012, +0.023] |
| tx_total | media BRC periodo e BLS (0-10) | 348 | +0.0043 | 0.0105 | [-0.016, +0.025] |
| tx_total | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0037 | 0.0112 | [-0.018, +0.026] |
| tx_total | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0168 | 0.0610 | [-0.136, +0.103] |
| tx_homens | atual (BRC 2018 p/ todos os anos) | 351 | +0.0033 | 0.0129 | [-0.022, +0.028] |
| tx_homens | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0036 | 0.0120 | [-0.020, +0.027] |
| tx_homens | BLS por legislatura (0-10) | 348 | +0.0058 | 0.0095 | [-0.013, +0.025] |
| tx_homens | media BRC periodo e BLS (0-10) | 348 | +0.0044 | 0.0110 | [-0.017, +0.026] |
| tx_homens | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0041 | 0.0118 | [-0.019, +0.027] |
| tx_homens | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0168 | 0.0640 | [-0.142, +0.109] |
| tx_mulheres | atual (BRC 2018 p/ todos os anos) | 351 | -0.0074 | 0.0116 | [-0.030, +0.015] |
| tx_mulheres | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0070 | 0.0113 | [-0.029, +0.015] |
| tx_mulheres | BLS por legislatura (0-10) | 348 | -0.0016 | 0.0083 | [-0.018, +0.015] |
| tx_mulheres | media BRC periodo e BLS (0-10) | 348 | -0.0021 | 0.0096 | [-0.021, +0.017] |
| tx_mulheres | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0073 | 0.0113 | [-0.029, +0.015] |
| tx_mulheres | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | +0.0149 | 0.0514 | [-0.086, +0.116] |
| tx_negros | atual (BRC 2018 p/ todos os anos) | 351 | -0.0102 | 0.0166 | [-0.043, +0.022] |
| tx_negros | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0096 | 0.0155 | [-0.040, +0.021] |
| tx_negros | BLS por legislatura (0-10) | 348 | +0.0024 | 0.0104 | [-0.018, +0.023] |
| tx_negros | media BRC periodo e BLS (0-10) | 348 | +0.0003 | 0.0121 | [-0.023, +0.024] |
| tx_negros | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0088 | 0.0156 | [-0.039, +0.022] |
| tx_negros | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | +0.0364 | 0.0750 | [-0.111, +0.183] |
| tx_nao_negros | atual (BRC 2018 p/ todos os anos) | 351 | -0.0093 | 0.0187 | [-0.046, +0.027] |
| tx_nao_negros | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0100 | 0.0189 | [-0.047, +0.027] |
| tx_nao_negros | BLS por legislatura (0-10) | 348 | -0.0021 | 0.0182 | [-0.038, +0.033] |
| tx_nao_negros | media BRC periodo e BLS (0-10) | 348 | -0.0048 | 0.0195 | [-0.043, +0.034] |
| tx_nao_negros | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0097 | 0.0187 | [-0.046, +0.027] |
| tx_nao_negros | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | +0.0470 | 0.0804 | [-0.111, +0.204] |
| tx_arma | atual (BRC 2018 p/ todos os anos) | 351 | +0.0049 | 0.0193 | [-0.033, +0.043] |
| tx_arma | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0058 | 0.0179 | [-0.029, +0.041] |
| tx_arma | BLS por legislatura (0-10) | 348 | +0.0107 | 0.0140 | [-0.017, +0.038] |
| tx_arma | media BRC periodo e BLS (0-10) | 348 | +0.0085 | 0.0160 | [-0.023, +0.040] |
| tx_arma | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0059 | 0.0174 | [-0.028, +0.040] |
| tx_arma | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0237 | 0.0967 | [-0.213, +0.166] |

Variancia intra-UF / total de `ideo_painel_atual` (wiki): 0.451

Variancia intra-UF / total de `ideo_BRC_periodo` (wiki): 0.440

## Variante de partido: tse (partido pelo qual foi eleito, TSE)

| desfecho | variante de ideologia | n | b por ponto | EP | IC95% |
|---|---|---|---|---|---|
| tx_total | atual (BRC 2018 p/ todos os anos) | 351 | +0.0009 | 0.0130 | [-0.025, +0.026] |
| tx_total | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0009 | 0.0121 | [-0.023, +0.025] |
| tx_total | BLS por legislatura (0-10) | 348 | +0.0050 | 0.0094 | [-0.013, +0.023] |
| tx_total | media BRC periodo e BLS (0-10) | 348 | +0.0032 | 0.0107 | [-0.018, +0.024] |
| tx_total | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0012 | 0.0118 | [-0.022, +0.024] |
| tx_total | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0126 | 0.0628 | [-0.136, +0.110] |
| tx_homens | atual (BRC 2018 p/ todos os anos) | 351 | +0.0007 | 0.0136 | [-0.026, +0.027] |
| tx_homens | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0005 | 0.0125 | [-0.024, +0.025] |
| tx_homens | BLS por legislatura (0-10) | 348 | +0.0054 | 0.0098 | [-0.014, +0.025] |
| tx_homens | media BRC periodo e BLS (0-10) | 348 | +0.0033 | 0.0111 | [-0.018, +0.025] |
| tx_homens | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0010 | 0.0123 | [-0.023, +0.025] |
| tx_homens | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0103 | 0.0655 | [-0.139, +0.118] |
| tx_mulheres | atual (BRC 2018 p/ todos os anos) | 351 | -0.0011 | 0.0109 | [-0.022, +0.020] |
| tx_mulheres | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0007 | 0.0105 | [-0.021, +0.020] |
| tx_mulheres | BLS por legislatura (0-10) | 348 | -0.0007 | 0.0080 | [-0.016, +0.015] |
| tx_mulheres | media BRC periodo e BLS (0-10) | 348 | -0.0008 | 0.0093 | [-0.019, +0.017] |
| tx_mulheres | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0005 | 0.0104 | [-0.021, +0.020] |
| tx_mulheres | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0117 | 0.0503 | [-0.110, +0.087] |
| tx_negros | atual (BRC 2018 p/ todos os anos) | 351 | -0.0070 | 0.0158 | [-0.038, +0.024] |
| tx_negros | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0070 | 0.0146 | [-0.036, +0.021] |
| tx_negros | BLS por legislatura (0-10) | 348 | -0.0001 | 0.0110 | [-0.022, +0.021] |
| tx_negros | media BRC periodo e BLS (0-10) | 348 | -0.0033 | 0.0127 | [-0.028, +0.022] |
| tx_negros | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0056 | 0.0144 | [-0.034, +0.023] |
| tx_negros | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | +0.0074 | 0.0720 | [-0.134, +0.149] |
| tx_nao_negros | atual (BRC 2018 p/ todos os anos) | 351 | -0.0010 | 0.0167 | [-0.034, +0.032] |
| tx_nao_negros | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | -0.0016 | 0.0171 | [-0.035, +0.032] |
| tx_nao_negros | BLS por legislatura (0-10) | 348 | +0.0021 | 0.0158 | [-0.029, +0.033] |
| tx_nao_negros | media BRC periodo e BLS (0-10) | 348 | +0.0004 | 0.0166 | [-0.032, +0.033] |
| tx_nao_negros | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | -0.0011 | 0.0172 | [-0.035, +0.033] |
| tx_nao_negros | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | +0.0408 | 0.0850 | [-0.126, +0.207] |
| tx_arma | atual (BRC 2018 p/ todos os anos) | 351 | +0.0014 | 0.0203 | [-0.038, +0.041] |
| tx_arma | BRC por periodo (<=2020 onda 2018; >=2021 onda 2022) | 351 | +0.0009 | 0.0185 | [-0.035, +0.037] |
| tx_arma | BLS por legislatura (0-10) | 348 | +0.0079 | 0.0137 | [-0.019, +0.035] |
| tx_arma | media BRC periodo e BLS (0-10) | 348 | +0.0050 | 0.0159 | [-0.026, +0.036] |
| tx_arma | BRC onda 2022 p/ todos os anos (limite oposto ao atual) | 351 | +0.0010 | 0.0181 | [-0.034, +0.036] |
| tx_arma | binaria: fracao do ano sob governo de esquerda (PT,PSB,PDT,PCdoB,PSOL; coef. por 1 = esq vs resto; sinal OPOSTO ao da escala) | 351 | -0.0194 | 0.0996 | [-0.215, +0.176] |

Variancia intra-UF / total de `ideo_painel_atual` (tse): 0.414

Variancia intra-UF / total de `ideo_BRC_periodo` (tse): 0.404
