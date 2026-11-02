## D1 — série temporal interrompida nacional (gerado por c09_d1_its.py; DESCRITIVO, sem contrafactual)

Portas: taxas de agressão e agressão+indet dos 5 grupos recalculadas = `asr_brasil.csv` (tolerância 0,005); óbitos por arma de fogo (agressão) no agregado = soma das UFs do Atlas em 2010-2024 (0 de diferença). Modelo nível + inclinação, 15 pontos, 7 gl, IC t(7); placebo 1 ano antes.

| série | desfecho | quebra | mudança de nível [IC95%] | p | MDE 80% (±) | placebo 1 ano antes [IC95%] | leitura pré-registrada | sigma residual |
|---|---|---|---|---|---|---|---|---|
| Brasil | agressao | 2016 | +2.6% [-9.1; +15.9] | 0.629 | -15.4% / +18.3% | 2015: -5.0% [-20.4; +13.5] | não distinguível de zero | 0.0395 |
| Brasil | agressao | 2019 | -17.0% [-29.5; -2.4] | 0.030 | -20.1% / +25.1% | 2018: -21.8% [-37.4; -2.4] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0395 |
| Brasil | agressao | 2023 | -3.9% [-17.1; +11.3] | 0.540 | -18.4% / +22.6% | 2022: +6.4% [-12.5; +29.3] | não distinguível de zero | 0.0395 |
| Brasil | agressao+indet | 2016 | +2.7% [-4.0; +9.8] | 0.380 | -8.8% / +9.7% | 2015: -3.5% [-10.5; +4.1] | não distinguível de zero | 0.0217 |
| Brasil | agressao+indet | 2019 | -9.6% [-17.3; -1.2] | 0.032 | -11.6% / +13.1% | 2018: -13.2% [-21.1; -4.5] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0217 |
| Brasil | agressao+indet | 2023 | -3.4% [-11.0; +4.7] | 0.341 | -10.6% / +11.8% | 2022: +5.0% [-3.4; +14.1] | não distinguível de zero | 0.0217 |
| Homens negros | agressao | 2016 | +3.9% [-9.1; +18.8] | 0.521 | -16.9% / +20.3% | 2015: -4.3% [-20.6; +15.3] | não distinguível de zero | 0.0435 |
| Homens negros | agressao | 2019 | -17.9% [-31.4; -1.8] | 0.035 | -21.9% / +28.0% | 2018: -23.0% [-39.0; -2.8] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0435 |
| Homens negros | agressao | 2023 | -4.9% [-19.2; +11.9] | 0.489 | -20.1% / +25.1% | 2022: +4.6% [-14.8; +28.4] | não distinguível de zero | 0.0435 |
| Homens negros | agressao+indet | 2016 | +3.7% [-4.6; +12.8] | 0.334 | -10.9% / +12.3% | 2015: -2.9% [-11.2; +6.1] | não distinguível de zero | 0.0272 |
| Homens negros | agressao+indet | 2019 | -11.0% [-20.4; -0.4] | 0.044 | -14.3% / +16.7% | 2018: -15.9% [-24.7; -5.9] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0272 |
| Homens negros | agressao+indet | 2023 | -3.6% [-13.0; +6.7] | 0.418 | -13.1% / +15.1% | 2022: +4.8% [-4.9; +15.6] | não distinguível de zero | 0.0272 |
| Homens não negros | agressao | 2016 | +0.5% [-8.8; +10.8] | 0.902 | -12.6% / +14.4% | 2015: -5.0% [-19.1; +11.6] | não distinguível de zero | 0.0317 |
| Homens não negros | agressao | 2019 | -13.4% [-24.0; -1.4] | 0.035 | -16.5% / +19.7% | 2018: -19.5% [-34.3; -1.5] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0317 |
| Homens não negros | agressao | 2023 | -2.2% [-13.1; +10.1] | 0.669 | -15.1% / +17.8% | 2022: +12.1% [-6.1; +33.9] | não distinguível de zero | 0.0317 |
| Homens não negros | agressao+indet | 2016 | +1.0% [-4.8; +7.1] | 0.709 | -7.8% / +8.4% | 2015: -4.2% [-10.4; +2.5] | não distinguível de zero | 0.0190 |
| Homens não negros | agressao+indet | 2019 | -6.4% [-13.4; +1.2] | 0.087 | -10.2% / +11.4% | 2018: -9.4% [-16.8; -1.5] | não distinguível de zero | 0.0190 |
| Homens não negros | agressao+indet | 2023 | -2.2% [-8.9; +5.0] | 0.481 | -9.3% / +10.3% | 2022: +7.2% [-0.5; +15.4] | não distinguível de zero | 0.0190 |
| Mulheres negras | agressao | 2016 | -0.2% [-10.1; +10.8] | 0.965 | -13.5% / +15.5% | 2015: -6.9% [-22.1; +11.4] | não distinguível de zero | 0.0340 |
| Mulheres negras | agressao | 2019 | -19.7% [-30.2; -7.6] | 0.008 | -17.6% / +21.3% | 2018: -16.6% [-33.4; +4.3] | coincide com a troca (descritivo; não causal) | 0.0340 |
| Mulheres negras | agressao | 2023 | +2.5% [-9.8; +16.3] | 0.665 | -16.1% / +19.2% | 2022: +7.4% [-11.8; +30.8] | não distinguível de zero | 0.0340 |
| Mulheres negras | agressao+indet | 2016 | -0.6% [-8.0; +7.4] | 0.867 | -10.1% / +11.2% | 2015: -4.4% [-11.9; +3.7] | não distinguível de zero | 0.0251 |
| Mulheres negras | agressao+indet | 2019 | -6.1% [-15.3; +4.1] | 0.192 | -13.3% / +15.3% | 2018: -4.7% [-14.0; +5.6] | não distinguível de zero | 0.0251 |
| Mulheres negras | agressao+indet | 2023 | -3.0% [-11.7; +6.5] | 0.468 | -12.1% / +13.8% | 2022: +2.6% [-6.2; +12.3] | não distinguível de zero | 0.0251 |
| Mulheres não negras | agressao | 2016 | -4.3% [-14.0; +6.4] | 0.357 | -13.6% / +15.8% | 2015: -7.5% [-16.8; +2.8] | não distinguível de zero | 0.0344 |
| Mulheres não negras | agressao | 2019 | -11.5% [-23.2; +2.0] | 0.082 | -17.8% / +21.6% | 2018: -13.7% [-24.4; -1.4] | não distinguível de zero | 0.0344 |
| Mulheres não negras | agressao | 2023 | -1.9% [-13.8; +11.5] | 0.732 | -16.3% / +19.4% | 2022: +12.1% [-0.1; +25.9] | não distinguível de zero | 0.0344 |
| Mulheres não negras | agressao+indet | 2016 | -0.6% [-5.5; +4.5] | 0.775 | -6.7% / +7.2% | 2015: -2.1% [-8.9; +5.1] | não distinguível de zero | 0.0163 |
| Mulheres não negras | agressao+indet | 2019 | -3.1% [-9.4; +3.6] | 0.303 | -8.8% / +9.7% | 2018: +4.9% [-4.1; +14.7] | não distinguível de zero | 0.0163 |
| Mulheres não negras | agressao+indet | 2023 | -5.2% [-10.8; +0.7] | 0.077 | -8.1% / +8.8% | 2022: +1.8% [-5.9; +10.1] | não distinguível de zero | 0.0163 |
| Brasil | arma | 2016 | +4.1% [-10.0; +20.2] | 0.536 | -18.1% / +22.1% | 2015: -5.1% [-24.2; +18.8] | não distinguível de zero | 0.0469 |
| Brasil | arma | 2019 | -21.7% [-35.4; -5.0] | 0.020 | -23.4% / +30.5% | 2018: -25.6% [-43.9; -1.4] | não atribuível à troca (placebo dispara com o mesmo sinal) | 0.0469 |
| Brasil | arma | 2023 | -6.4% [-21.4; +11.6] | 0.404 | -21.5% / +27.3% | 2022: +6.9% [-16.4; +36.9] | não distinguível de zero | 0.0469 |
| Brasil | razao_indet_pp | 2016 | -0.1 p.p. [-5.5; +5.3] | 0.968 | -7.4 p.p. / +7.4 p.p. | 2015: +1.2 p.p. [-7.5; +9.9] | não distinguível de zero | 1.7391 |
| Brasil | razao_indet_pp | 2019 | +6.5 p.p. [-0.6; +13.7] | 0.068 | -9.9 p.p. / +9.9 p.p. | 2018: +8.3 p.p. [-2.6; +19.2] | não distinguível de zero | 1.7391 |
| Brasil | razao_indet_pp | 2023 | +0.4 p.p. [-6.1; +6.9] | 0.897 | -9.0 p.p. / +9.0 p.p. | 2022: -1.0 p.p. [-10.6; +8.6] | não distinguível de zero | 1.7391 |

Séries usadas (taxa padronizada por 100 mil; razão em %):

| série | desfecho | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Brasil | agressao | 25.93 | 25.94 | 27.87 | 28.09 | 29.50 | 28.81 | 30.25 | 31.47 | 27.61 | 21.77 | 23.51 | 22.45 | 21.81 | 21.28 | 19.50 |
| Brasil | agressao+indet | 31.72 | 32.07 | 33.68 | 33.69 | 34.78 | 34.22 | 35.84 | 36.74 | 34.09 | 30.34 | 30.66 | 29.38 | 29.44 | 27.97 | 27.63 |
| Homens negros | agressao | 65.52 | 64.95 | 70.01 | 70.73 | 74.26 | 72.97 | 77.18 | 81.15 | 70.92 | 55.31 | 60.15 | 57.11 | 54.49 | 52.66 | 48.03 |
| Homens negros | agressao+indet | 75.49 | 75.11 | 80.28 | 80.67 | 83.57 | 82.96 | 87.52 | 90.61 | 82.36 | 71.85 | 72.77 | 68.44 | 67.86 | 63.82 | 62.32 |
| Homens não negros | agressao | 29.12 | 29.19 | 30.77 | 30.33 | 31.67 | 30.26 | 31.05 | 30.23 | 26.10 | 20.75 | 21.85 | 20.58 | 20.91 | 20.37 | 18.69 |
| Homens não negros | agressao+indet | 36.85 | 37.46 | 38.11 | 37.62 | 38.44 | 36.76 | 37.83 | 36.93 | 34.60 | 31.22 | 31.23 | 29.98 | 30.70 | 29.42 | 29.15 |
| Mulheres negras | agressao | 5.43 | 5.60 | 5.90 | 5.79 | 5.87 | 5.67 | 5.76 | 6.10 | 5.62 | 4.48 | 4.60 | 4.58 | 4.36 | 4.52 | 4.11 |
| Mulheres negras | agressao+indet | 7.88 | 8.46 | 8.63 | 8.39 | 8.47 | 8.32 | 8.47 | 8.62 | 8.48 | 8.07 | 7.90 | 7.97 | 7.96 | 7.68 | 7.79 |
| Mulheres não negras | agressao | 3.44 | 3.35 | 3.39 | 3.56 | 3.53 | 3.34 | 3.22 | 3.33 | 2.95 | 2.59 | 2.57 | 2.58 | 2.68 | 2.62 | 2.51 |
| Mulheres não negras | agressao+indet | 6.53 | 6.57 | 6.31 | 6.20 | 6.03 | 5.82 | 5.73 | 5.77 | 6.03 | 6.05 | 5.90 | 6.16 | 6.32 | 6.04 | 6.44 |
| Brasil | arma | 17.81 | 17.84 | 19.44 | 19.62 | 20.80 | 20.44 | 21.76 | 23.26 | 20.20 | 15.15 | 16.72 | 16.26 | 15.59 | 15.13 | 13.46 |
| Brasil | razao_indet_pp | 15.66 | 16.55 | 15.14 | 14.70 | 13.69 | 14.44 | 14.39 | 13.32 | 18.04 | 27.44 | 22.75 | 23.30 | 25.93 | 24.23 | 30.11 |

Limites: 15 pontos e 8 parâmetros (7 gl); EP clássico ignora autocorrelação; o segmento 2023-2024 tem 2 pontos e denominador extrapolado (⚠️ em `asr_brasil.md`); choques nacionais simultâneos (COVID, armas, facções, degradação do SIM) não são separáveis da troca. Nenhuma linha desta tabela é efeito do presidente.
