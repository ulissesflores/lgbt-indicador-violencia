# F8 — painel UF x ano 2012-2024 (exploratório, NÃO causal)

Observações: 351 UF-anos. Partidos sem escore (linhas descartadas): {'sem partido': 1, '': 2}

Modelo: log(taxa) = b x ideologia_governador(0-10) + EF(UF) + EF(ano); EP agrupado por UF. b x 1 ponto = variação % aproximada da taxa por 1 ponto para a direita.

| desfecho | b (por 1 ponto de ideologia) | EP | IC95% | n | leitura |
|---|---|---|---|---|---|
| tx_total | +0.0028 | 0.0123 | [-0.021, +0.027] | 351 | não distinguível de zero |
| tx_homens | +0.0033 | 0.0129 | [-0.022, +0.028] | 351 | não distinguível de zero |
| tx_mulheres | -0.0074 | 0.0116 | [-0.030, +0.015] | 351 | não distinguível de zero |
| tx_negros | -0.0102 | 0.0166 | [-0.043, +0.022] | 351 | não distinguível de zero |
| tx_nao_negros | -0.0093 | 0.0187 | [-0.046, +0.027] | 351 | não distinguível de zero |
| tx_arma | +0.0049 | 0.0193 | [-0.033, +0.043] | 351 | não distinguível de zero |

Robustez (ideologia defasada 1 ano):

| desfecho | b | EP | IC95% |
|---|---|---|---|
| tx_total | -0.0039 | 0.0124 | [-0.028, +0.020] |
| tx_mulheres | -0.0100 | 0.0130 | [-0.035, +0.015] |
| tx_negros | -0.0174 | 0.0168 | [-0.050, +0.015] |

Descritivo nacional por período federal (taxa por 100 mil do grupo; soma das UFs do painel):

| período | total | homens | mulheres | negros | não negros |
|---|---|---|---|---|---|
| 2015-2018 (Dilma/Temer) | 29.3 | 55.3 | 4.5 | 39.0 | 15.2 |
| 2019-2022 (Bolsonaro) | 21.7 | 40.8 | 3.6 | 29.6 | 10.8 |
| 2023-2024 (Lula 3) | 19.7 | 36.8 | 3.5 | 26.9 | 9.9 |

Caveats: (1) SIM = óbitos por agressão, sem motivação; (2) raça/cor do óbito tem 'ignorado' que não entra em negros nem não negros (viés para baixo nas duas taxas); (3) COVID 2020-21 e a queda nacional 2018-19 estão absorvidos pelos EF de ano, mas não os choques locais (facções, armas) correlacionados com eleição; (4) ideologia é do partido do governador, escore de 2018 aplicado a todos os anos; (5) 2025 excluído (preliminar); (6) população por cor/raça de 2021 interpolada (PNADC 6403 não publica 2021). Denominadores: PNAD Contínua (SIDRA 6407 e 6403, médias anuais).
## Robustez — escala Zucco & Power (BLS9 2021, -1 esquerda .. +1 direita); 343 UF-anos; partidos sem escore: {'sem partido': 1, '': 2, 'Republicanos': 11, 'PHS': 6}

| desfecho | b (por 1 unidade da escala; ~meio do intervalo esquerda-direita) | EP | IC95% |
|---|---|---|---|
| tx_total | +0.0232 | 0.0557 | [-0.086, +0.132] |
| tx_homens | +0.0248 | 0.0580 | [-0.089, +0.139] |
| tx_mulheres | -0.0186 | 0.0539 | [-0.124, +0.087] |
| tx_negros | -0.0256 | 0.0725 | [-0.168, +0.116] |
| tx_nao_negros | -0.0222 | 0.0859 | [-0.191, +0.146] |
| tx_arma | +0.0385 | 0.0865 | [-0.131, +0.208] |

Leitura: 1 unidade da escala BLS9 ≈ distância PT (−0,69) -> DEM/PL (+0,43/+0,49) mais um pouco; nenhum coeficiente distinguível de zero nas duas escalas.