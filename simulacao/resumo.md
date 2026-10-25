# Simulação F7 — a série registrada de LGBTfobia identifica a incidência? (2026-10-11)

Script: simulacao/sim_identificabilidade.py (semente 20261011; numpy 2.4.6, scipy 1.17.1)
Dado observado: Anuário FBSP, BOs com motivação "racismo por homofobia ou transfobia", valores revisados: 2022 = 783, 2023 = 1.633, 2024 = 2.567, 2025 = 3.481.
Modelo: registrado R_t ~ Poisson(I_t x p_t); incidência verdadeira I_t = I0 (1+g)^t; propensão a registro p_t = p0 (1+h)^t, teto 1.

## Resultado 1 — não identificável
| Cenário (g fixo) | I0 (2022) ajustado | crescimento do registro h | erro de ajuste (SSE log) | p em 2025 | I verdadeira 2030 | R registrada 2030 (mediana, IC90) |
|---|---|---|---|---|---|---|
| S1 incidência constante | 21.948 | +63,7%/ano | 0,0472 | 0,175 | 21.948 | 22.026 (19.030–25.229) |
| S2 incidência +15%/ano | 21.947 | +42,3%/ano | 0,0472 | 0,115 | 67.136 | 45.232 (26.866–63.400) |
| S3 incidência −5%/ano | 21.946 | +72,3%/ano | 0,0472 | 0,205 | 14.559 | 14.529 (12.645–16.827) |

Os três cenários reproduzem 2022-2025 com o MESMO erro (0,0472), e isso vale para p0 = 0,02, 0,04, 0,08 e 0,15 (tabela em resumo.json). Conclusão: a série de BOs, sozinha, é compatível com incidência subindo, parada ou caindo; a alta observada é explicável integralmente por registro. As projeções 2026-2030 divergem apenas porque se assume que a tendência de registro de cada cenário continua, e essa tendência também não é observada. Nenhuma política pode ser avaliada por essa série sem um segundo canal independente.

Suposição sensível: p0 (fração de incidentes verdadeiros que vira BO com motivação em 2022). O resultado de não identificabilidade NÃO depende dela; os níveis absolutos de I0 sim (I0 escala com 1/p0).

## Resultado 2 — o que separa os cenários: survey bienal de vitimização
Base: PNS 2019 (Vasconcelos et al. 2023): LGB+ = 1,89% dos adultos; violência física em 12 meses entre LGB+ = 14,70%. Teste de duas proporções entre duas rodadas, alfa 5%, poder 80%.
| mudança relativa a detectar | n de LGB+ por rodada | n total sem sobreamostra | n total com sobreamostra 5x |
|---|---|---|---|
| 10% | 9.481 | 501.641 | 100.329 |
| 20% | 2.461 | 130.212 | 26.043 |
| 30% | 1.133 | 59.948 | 11.990 |
| 50% | 435 | 23.016 | 4.604 |

Leitura: um survey do porte da PNS (~90 mil domicílios) com pergunta de orientação sexual detecta mudança de ~25-30% na vitimização LGB+ entre rodadas; para 10% é preciso sobreamostrar (5x) e ainda assim ~100 mil entrevistas. Esse é o custo real de "ter dado" sobre incidência: não é o campo do BO, é a amostra.

Arquivos: projecao-registrada-2026-2030.csv · poder-survey.csv · resumo.json · fig-identificabilidade.png
