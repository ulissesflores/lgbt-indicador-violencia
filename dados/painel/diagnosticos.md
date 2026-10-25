# Diagnósticos do painel UF x ano (gerado por painel_diagnosticos.py, semente 20261021)

Convenção: b = variação aproximada de ln(taxa) por 1 ponto de ideologia (escala 0-10, 5 pontos ≈ distância PT -> DEM); b=0,01 ≈ 1% por ponto. EP agrupado por UF (CR1, G=27).

## Versão principal (2026-10-21): partido de ELEIÇÃO (TSE) + ideologia BRC POR PERÍODO (onda 2018 p/ 2012-20; onda 2022 p/ 2021-24)

D5. Variação de ideologia: DP total 2.07; DP DENTRO da UF 1.31 (é daí que vem a identificação); UFs com mudança > 1 ponto no período: 21 de 27.

| desfecho | b (EP) base | wild-cluster p | b com lead(t+1): coef ideologia(t) / coef lead(t+1) (p lead) | b com tendência por UF (EP) | b binário direita (EP) | IC90 base (sem margem de equivalência declarada) |
|---|---|---|---|---|---|---|
| tx_total | +0.0009 (0.0121) | 0.943 | +0.0082 / -0.0109 (p=0.42) | +0.0151 (0.0127) | +0.017 (0.060) | [-0.019; +0.021] |
| tx_homens | +0.0005 (0.0125) | 0.970 | +0.0073 / -0.0106 (p=0.44) | +0.0149 (0.0129) | +0.015 (0.062) | [-0.020; +0.021] |
| tx_mulheres | -0.0007 (0.0105) | 0.951 | +0.0097 / -0.0116 (p=0.40) | +0.0144 (0.0121) | +0.017 (0.048) | [-0.018; +0.017] |
| tx_negros | -0.0070 (0.0146) | 0.661 | +0.0028 / -0.0158 (p=0.32) | +0.0157 (0.0146) | +0.000 (0.069) | [-0.031; +0.017] |
| tx_nao_negros | -0.0016 (0.0171) | 0.911 | +0.0011 / +0.0073 (p=0.63) | -0.0047 (0.0176) | -0.042 (0.080) | [-0.030; +0.027] |
| tx_arma | +0.0009 (0.0185) | 0.970 | +0.0067 / -0.0080 (p=0.71) | +0.0162 (0.0152) | +0.025 (0.094) | [-0.029; +0.031] |

D4. Desfechos por raça com controle da parcela de óbitos sem raça/cor no UF-ano:

| desfecho | b base (EP) | b com controle de completude (EP) |
|---|---|---|
| tx_negros | -0.0070 (0.0146) | -0.0006 (0.0134) |
| tx_nao_negros | -0.0016 (0.0171) | +0.0016 (0.0178) |

## Secundária: partido de ELEIÇÃO (TSE) + escore único Bolognesi 2018

D5. Variação de ideologia: DP total 2.01; DP DENTRO da UF 1.29 (é daí que vem a identificação); UFs com mudança > 1 ponto no período: 21 de 27.

| desfecho | b (EP) base | wild-cluster p | b com lead(t+1): coef ideologia(t) / coef lead(t+1) (p lead) | b com tendência por UF (EP) | b binário direita (EP) | IC90 base (sem margem de equivalência declarada) |
|---|---|---|---|---|---|---|
| tx_total | +0.0009 (0.0130) | 0.952 | +0.0067 / -0.0096 (p=0.50) | +0.0155 (0.0125) | +0.017 (0.060) | [-0.021; +0.022] |
| tx_homens | +0.0007 (0.0136) | 0.967 | +0.0058 / -0.0093 (p=0.52) | +0.0155 (0.0127) | +0.015 (0.062) | [-0.022; +0.023] |
| tx_mulheres | -0.0011 (0.0109) | 0.912 | +0.0082 / -0.0104 (p=0.47) | +0.0137 (0.0122) | +0.017 (0.048) | [-0.019; +0.017] |
| tx_negros | -0.0070 (0.0158) | 0.705 | +0.0009 / -0.0139 (p=0.41) | +0.0156 (0.0143) | +0.000 (0.069) | [-0.033; +0.019] |
| tx_nao_negros | -0.0010 (0.0167) | 0.945 | +0.0016 / +0.0074 (p=0.62) | -0.0032 (0.0174) | -0.042 (0.080) | [-0.029; +0.027] |
| tx_arma | +0.0014 (0.0203) | 0.960 | +0.0045 / -0.0056 (p=0.81) | +0.0174 (0.0152) | +0.025 (0.094) | [-0.032; +0.035] |

D4. Desfechos por raça com controle da parcela de óbitos sem raça/cor no UF-ano:

| desfecho | b base (EP) | b com controle de completude (EP) |
|---|---|---|
| tx_negros | -0.0070 (0.0158) | -0.0005 (0.0146) |
| tx_nao_negros | -0.0010 (0.0167) | +0.0021 (0.0174) |

## Secundária: partido em exercício (Wikipédia curada e corrigida) + escore único Bolognesi 2018

D5. Variação de ideologia: DP total 2.02; DP DENTRO da UF 1.36 (é daí que vem a identificação); UFs com mudança > 1 ponto no período: 21 de 27.

| desfecho | b (EP) base | wild-cluster p | b com lead(t+1): coef ideologia(t) / coef lead(t+1) (p lead) | b com tendência por UF (EP) | b binário direita (EP) | IC90 base (sem margem de equivalência declarada) |
|---|---|---|---|---|---|---|
| tx_total | +0.0028 (0.0123) | 0.834 | +0.0085 / -0.0088 (p=0.52) | +0.0156 (0.0127) | +0.021 (0.059) | [-0.017; +0.023] |
| tx_homens | +0.0033 (0.0129) | 0.816 | +0.0085 / -0.0088 (p=0.53) | +0.0161 (0.0130) | +0.021 (0.062) | [-0.018; +0.024] |
| tx_mulheres | -0.0074 (0.0116) | 0.514 | +0.0018 / -0.0089 (p=0.53) | +0.0090 (0.0118) | -0.011 (0.050) | [-0.026; +0.012] |
| tx_negros | -0.0102 (0.0166) | 0.545 | -0.0031 / -0.0128 (p=0.45) | +0.0127 (0.0145) | -0.028 (0.073) | [-0.038; +0.017] |
| tx_nao_negros | -0.0093 (0.0187) | 0.622 | +0.0008 / +0.0006 (p=0.97) | -0.0032 (0.0189) | -0.048 (0.077) | [-0.040; +0.022] |
| tx_arma | +0.0049 (0.0193) | 0.834 | +0.0060 / -0.0029 (p=0.90) | +0.0177 (0.0155) | +0.029 (0.093) | [-0.027; +0.037] |

D4. Desfechos por raça com controle da parcela de óbitos sem raça/cor no UF-ano:

| desfecho | b base (EP) | b com controle de completude (EP) |
|---|---|---|
| tx_negros | -0.0102 (0.0166) | +0.0029 (0.0142) |
| tx_nao_negros | -0.0093 (0.0187) | -0.0033 (0.0209) |

