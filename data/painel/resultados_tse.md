# F8 — painel UF x ano 2012-2024 (exploratório, NÃO causal)

Observações: 351 UF-anos. Partidos sem escore (linhas descartadas): {'sem partido': 1, '': 1}

Modelo: log(taxa) = b x ideologia_governador(0-10) + EF(UF) + EF(ano); EP agrupado por UF. b x 1 ponto = variação % aproximada da taxa por 1 ponto para a direita.

| desfecho | b (por 1 ponto de ideologia) | EP | IC95% | n | leitura |
|---|---|---|---|---|---|
| tx_total | +0.0009 | 0.0130 | [-0.025, +0.026] | 351 | não distinguível de zero |
| tx_homens | +0.0007 | 0.0136 | [-0.026, +0.027] | 351 | não distinguível de zero |
| tx_mulheres | -0.0011 | 0.0109 | [-0.022, +0.020] | 351 | não distinguível de zero |
| tx_negros | -0.0070 | 0.0158 | [-0.038, +0.024] | 351 | não distinguível de zero |
| tx_nao_negros | -0.0010 | 0.0167 | [-0.034, +0.032] | 351 | não distinguível de zero |
| tx_arma | +0.0014 | 0.0203 | [-0.039, +0.041] | 351 | não distinguível de zero |

Robustez (ideologia defasada 1 ano):

| desfecho | b | EP | IC95% |
|---|---|---|---|
| tx_total | -0.0051 | 0.0135 | [-0.031, +0.021] |
| tx_mulheres | -0.0055 | 0.0127 | [-0.030, +0.019] |
| tx_negros | -0.0126 | 0.0160 | [-0.044, +0.019] |

Descritivo nacional por período federal (taxa por 100 mil do grupo; soma das UFs do painel):

| período | total | homens | mulheres | negros | não negros |
|---|---|---|---|---|---|
| 2015-2018 (Dilma/Temer) | 29.3 | 55.3 | 4.5 | 39.0 | 15.2 |
| 2019-2022 (Bolsonaro) | 21.7 | 40.8 | 3.6 | 29.6 | 10.8 |
| 2023-2024 (Lula 3) | 19.7 | 36.8 | 3.5 | 26.9 | 9.9 |

Caveats: (1) SIM = óbitos por agressão, sem motivação; (2) raça/cor do óbito tem 'ignorado' que não entra em negros nem não negros (viés para baixo nas duas taxas); (3) COVID 2020-21 e a queda nacional 2018-19 estão absorvidos pelos EF de ano, mas não os choques locais (facções, armas) correlacionados com eleição; (4) ideologia é do partido do governador, escore de 2018 aplicado a todos os anos; (5) 2025 excluído (preliminar); (6) população por cor/raça de 2021 interpolada (PNADC 6403 não publica 2021). Denominadores: PNAD Contínua (SIDRA 6407 e 6403, médias anuais).
## Robustez — escala Zucco & Power (BLS9 2021, -1 esquerda .. +1 direita); 341 UF-anos; partidos sem escore: {'sem partido': 1, 'PMN': 4, 'PRB': 1, 'Republicanos': 11, '': 1, 'PHS': 7}

| desfecho | b (por 1 unidade da escala; ~meio do intervalo esquerda-direita) | EP | IC95% |
|---|---|---|---|
| tx_total | +0.0151 | 0.0582 | [-0.099, +0.129] |
| tx_homens | +0.0157 | 0.0608 | [-0.103, +0.135] |
| tx_mulheres | -0.0040 | 0.0505 | [-0.103, +0.095] |
| tx_negros | -0.0162 | 0.0707 | [-0.155, +0.122] |
| tx_nao_negros | -0.0034 | 0.0836 | [-0.167, +0.160] |
| tx_arma | +0.0205 | 0.0888 | [-0.154, +0.195] |

Leitura: 1 unidade da escala BLS9 ≈ distância PT (−0,69) -> DEM/PL (+0,43/+0,49) mais um pouco; nenhum coeficiente distinguível de zero nas duas escalas.