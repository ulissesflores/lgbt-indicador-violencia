# Taxas de agressão padronizadas por idade, Brasil (gerado por padroniza_idade.py)

Padrão: população do Brasil 2022 (17 faixas). Denominador: Censo 2010/2022 com interpolação geométrica por célula (2023-24 extrapolados, ⚠️). IC95% Poisson (aproximado).

## 1. Taxa padronizada por 100 mil (agressão X85-Y09), anos selecionados

| grupo | 2012 | 2016 | 2020 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Brasil | 27.9 [27.6; 28.1] (bruta 29.3) | 30.3 [30.0; 30.5] (bruta 31.3) | 23.5 [23.3; 23.7] (bruta 23.8) | 21.8 [21.6; 22.0] (bruta 21.8) | 21.3 [21.1; 21.5] (bruta 21.2) | 19.5 [19.3; 19.7] (bruta 19.3) |
| Homens | 51.9 [51.5; 52.4] (bruta 55.0) | 56.8 [56.4; 57.3] (bruta 59.3) | 44.1 [43.6; 44.5] (bruta 45.0) | 40.7 [40.3; 41.1] (bruta 41.1) | 39.6 [39.2; 40.0] (bruta 39.8) | 36.2 [35.9; 36.6] (bruta 36.2) |
| Mulheres | 4.7 [4.6; 4.8] (bruta 4.8) | 4.6 [4.4; 4.7] (bruta 4.6) | 3.7 [3.6; 3.8] (bruta 3.7) | 3.6 [3.5; 3.8] (bruta 3.6) | 3.7 [3.6; 3.8] (bruta 3.7) | 3.4 [3.3; 3.5] (bruta 3.4) |
| Negros | 38.0 [37.6; 38.3] (bruta 41.2) | 41.4 [41.1; 41.8] (bruta 44.4) | 32.3 [32.0; 32.6] (bruta 34.0) | 29.3 [29.0; 29.6] (bruta 30.5) | 28.5 [28.2; 28.8] (bruta 29.5) | 25.9 [25.7; 26.2] (bruta 26.7) |
| Não negros | 16.5 [16.2; 16.8] (bruta 16.7) | 16.6 [16.3; 16.8] (bruta 16.5) | 11.8 [11.6; 12.0] (bruta 11.5) | 11.4 [11.2; 11.6] (bruta 11.0) | 11.1 [10.9; 11.3] (bruta 10.6) | 10.2 [10.0; 10.4] (bruta 9.7) |
| Homens negros | 70.0 [69.3; 70.7] (bruta 76.4) | 77.2 [76.4; 77.9] (bruta 83.2) | 60.2 [59.5; 60.8] (bruta 63.8) | 54.5 [53.9; 55.1] (bruta 57.2) | 52.7 [52.1; 53.2] (bruta 55.0) | 48.0 [47.5; 48.6] (bruta 49.9) |
| Homens não negros | 30.8 [30.3; 31.3] (bruta 31.2) | 31.1 [30.5; 31.6] (bruta 31.0) | 21.8 [21.4; 22.3] (bruta 21.4) | 20.9 [20.5; 21.3] (bruta 20.2) | 20.4 [19.9; 20.8] (bruta 19.6) | 18.7 [18.3; 19.1] (bruta 17.9) |
| Mulheres negras | 5.9 [5.7; 6.1] (bruta 6.2) | 5.8 [5.6; 6.0] (bruta 5.9) | 4.6 [4.4; 4.8] (bruta 4.7) | 4.4 [4.2; 4.5] (bruta 4.5) | 4.5 [4.3; 4.7] (bruta 4.6) | 4.1 [3.9; 4.3] (bruta 4.2) |
| Mulheres não negras | 3.4 [3.2; 3.6] (bruta 3.4) | 3.2 [3.1; 3.4] (bruta 3.2) | 2.6 [2.4; 2.7] (bruta 2.5) | 2.7 [2.5; 2.8] (bruta 2.6) | 2.6 [2.5; 2.8] (bruta 2.5) | 2.5 [2.4; 2.7] (bruta 2.4) |

## 2. Razões padronizadas (pooled 2022-2024 para estabilidade; ⚠️ 2023-24 com denominador extrapolado)

| razão | valor | observação |
|---|---|---|
| homens / mulheres (padronizado) | 10.8 | taxas 38.8 e 3.6 por 100 mil |
| negros / não negros (padronizado, raça ignorada redistribuída) | 2.56 | taxas 27.9 e 10.9 |
| negros / não negros: limite inferior (raça ignorada descartada) | 2.56 | |
| negros / não negros: extremo A (toda raça ignorada -> negros) | 2.60 | cota máxima possível a favor de negros mais expostos |
| negros / não negros: extremo B (toda raça ignorada -> não negros) | 2.42 | cota mínima |
| Homens negros / Mulheres não negras (padronizado) | 19.9 | taxas 51.7 e 2.6 |
| Homens não negros / Mulheres não negras (padronizado) | 7.7 | taxas 20.0 e 2.6 |
| Mulheres negras / Mulheres não negras (padronizado) | 1.7 | taxas 4.3 e 2.6 |
| Homens negros / Homens não negros (padronizado) | 2.6 | taxas 51.7 e 20.0 |

## 3. Decomposição de Kitagawa da diferença de taxas BRUTAS (2022-2024 médios): composição etária x taxas por idade

| comparação | diferença bruta | efeito idade | efeito taxas | % da diferença devido a taxas |
|---|---|---|---|---|
| Homens - Mulheres | 35.5 | +0.4 | +35.1 | 99% |
| Negros - Não negros | 18.5 | +1.7 | +16.8 | 91% |
| Homens negros - Homens não negros | 34.7 | +3.0 | +31.8 | 91% |
| Mulheres negras - Mulheres não negras | 1.9 | +0.2 | +1.7 | 89% |

## 4. Ordem de 'segurança' (menor para maior taxa padronizada de agressão, 2022-24 agregado)

1. Mulheres não negras: 2.6 por 100 mil
2. Mulheres negras: 4.3 por 100 mil
3. Homens não negros: 20.0 por 100 mil
4. Homens negros: 51.7 por 100 mil
