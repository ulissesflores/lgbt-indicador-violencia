# Projeção 2025-2030 da taxa padronizada de agressão por sexo x raça (gerado por projecao_grupos.py)

Escala log; seleção por backtest de origem móvel; intervalos = quantis empíricos dos erros de backtest. LEIA os limites no cabeçalho do script.

## Desfecho: agressao

Backtest (erro absoluto médio na escala log, pooled 9 grupos x origens 2016-2023 x h=1..5; MASE contra rw):

| modelo | MAE log | MASE |
|---|---|---|
| rw | 0.147 | 1.00 |
| drift8 | 0.159 | 1.08 |
| damp | 0.152 | 1.04 |
| holt | 0.192 | 1.31 |
| ols7 | 0.175 | 1.20 |

Modelo escolhido (menor MAE): **rw**.

Viés médio do erro (real - previsto, log) por modelo: rw -0.137; drift8 -0.116; damp -0.097; holt -0.075; ols7 -0.124 (negativo = a queda recente foi subestimada: as origens de backtest caem no regime de queda).
Cobertura empírica do IC80 nos próprios erros de backtest (otimista, por construção): 80%.

| grupo | 2024 obs | 2025: persistência / tendência (damp) [IC80 da persistência] | 2027: persistência / tendência (damp) [IC80 da persistência] | 2030: persistência / tendência (damp) [IC80 da persistência] |
|---|---|---|---|---|
| Brasil | 19.5 | 19.5 / 19.2 [17.2; 22.2] | 19.5 / 18.7 [14.6; 26.1] | 19.5 / 18.3 [13.2; 28.7] |
| Homens | 36.2 | 36.2 / 35.6 [31.9; 41.2] | 36.2 / 34.7 [27.1; 48.5] | 36.2 / 33.9 [24.6; 53.4] |
| Mulheres | 3.4 | 3.4 / 3.4 [3.0; 3.9] | 3.4 / 3.4 [2.6; 4.6] | 3.4 / 3.3 [2.3; 5.1] |
| Negros | 25.9 | 25.9 / 25.4 [22.8; 29.5] | 25.9 / 24.6 [19.4; 34.7] | 25.9 / 23.9 [17.6; 38.2] |
| Não negros | 10.2 | 10.2 / 10.1 [9.0; 11.6] | 10.2 / 9.8 [7.6; 13.7] | 10.2 / 9.6 [6.9; 15.1] |
| Homens negros | 48.0 | 48.0 / 47.0 [42.2; 54.6] | 48.0 / 45.5 [35.9; 64.3] | 48.0 / 44.2 [32.6; 70.7] |
| Homens não negros | 18.7 | 18.7 / 18.4 [16.4; 21.2] | 18.7 / 17.9 [14.0; 25.0] | 18.7 / 17.6 [12.7; 27.5] |
| Mulheres negras | 4.1 | 4.1 / 4.1 [3.6; 4.7] | 4.1 / 4.0 [3.1; 5.5] | 4.1 / 3.9 [2.8; 6.1] |
| Mulheres não negras | 2.5 | 2.5 / 2.5 [2.2; 2.9] | 2.5 / 2.5 [1.9; 3.4] | 2.5 / 2.5 [1.7; 3.7] |

## Desfecho: agressao+indet

Backtest (erro absoluto médio na escala log, pooled 9 grupos x origens 2016-2023 x h=1..5; MASE contra rw):

| modelo | MAE log | MASE |
|---|---|---|
| rw | 0.080 | 1.00 |
| drift8 | 0.091 | 1.14 |
| damp | 0.078 | 0.97 |
| holt | 0.096 | 1.19 |
| ols7 | 0.101 | 1.26 |

Modelo escolhido (menor MAE): **damp**.

Viés médio do erro (real - previsto, log) por modelo: rw -0.069; drift8 -0.064; damp -0.053; holt -0.046; ols7 -0.066 (negativo = a queda recente foi subestimada: as origens de backtest caem no regime de queda).
Cobertura empírica do IC80 nos próprios erros de backtest (otimista, por construção): 80%.

| grupo | 2024 obs | 2025: persistência / tendência (damp) [IC80 da persistência] | 2027: persistência / tendência (damp) [IC80 da persistência] | 2030: persistência / tendência (damp) [IC80 da persistência] |
|---|---|---|---|---|
| Brasil | 27.6 | 27.6 / 27.2 [26.1; 29.3] | 27.6 / 26.6 [23.2; 32.9] | 27.6 / 26.1 [20.6; 37.0] |
| Homens | 49.0 | 49.0 / 48.2 [46.3; 51.9] | 49.0 / 47.0 [41.2; 58.3] | 49.0 / 46.0 [36.6; 65.6] |
| Mulheres | 7.3 | 7.3 / 7.3 [6.9; 7.7] | 7.3 / 7.3 [6.1; 8.7] | 7.3 / 7.4 [5.5; 9.8] |
| Negros | 34.8 | 34.8 / 34.1 [32.9; 36.9] | 34.8 / 33.0 [29.2; 41.4] | 34.8 / 32.2 [26.0; 46.6] |
| Não negros | 17.2 | 17.2 / 17.1 [16.2; 18.2] | 17.2 / 16.9 [14.4; 20.5] | 17.2 / 16.7 [12.8; 23.0] |
| Homens negros | 62.3 | 62.3 / 60.9 [58.8; 66.0] | 62.3 / 59.0 [52.4; 74.2] | 62.3 / 57.3 [46.6; 83.4] |
| Homens não negros | 29.1 | 29.1 / 28.8 [27.5; 30.9] | 29.1 / 28.4 [24.5; 34.7] | 29.1 / 28.0 [21.8; 39.0] |
| Mulheres negras | 7.8 | 7.8 / 7.7 [7.4; 8.3] | 7.8 / 7.7 [6.5; 9.3] | 7.8 / 7.6 [5.8; 10.4] |
| Mulheres não negras | 6.4 | 6.4 / 6.5 [6.1; 6.8] | 6.4 / 6.6 [5.4; 7.7] | 6.4 / 6.7 [4.8; 8.6] |

