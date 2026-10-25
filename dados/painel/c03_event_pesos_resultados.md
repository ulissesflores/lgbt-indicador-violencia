# C03 — painel F8: conversão exata, event study empilhado e pesos do TWFE (gerado por painel_c03_event_pesos.py)

> [!NOTE]
> Exploratório, NÃO causal; poucos eventos limpos; 27 clusters. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. Cabeçalho do script traz método e LIMITES.

## 0. Reprodução e contagens

- b e EP dos 6 desfechos (BRC) e da robustez BLS9 (341 UF-anos) = `resultados_tse_brc.md` (4 casas).
- Painel BRC: 94 mudanças de escore = 67 trocas reais (partido muda) + 27 trocas de onda no mesmo partido (todas em [2021]); trocas reais: 38 para a direita, 29 para a esquerda.
- Painel `tse` (escore único): 68 mudanças = 37 para a direita + 31 para a esquerda, 0 trocas de onda. **O "68 trocas" do dossiê pertence a este painel; o "27 de 94", ao BRC; as duas contagens não são da mesma especificação** (no BRC são 67 trocas reais).

## 1. Conversão exata 100[exp(5b)-1] dos limites do IC95% (k = 5 pontos; PT 2,97 -> DEM/PL ~8)

| desfecho | b | EP | IC95% de b | linear 100x5x limite (%) | exato 100[exp(5 limite)-1] (%) | diferença nos limites (p.p.) |
|---|---|---|---|---|---|---|
| tx_total | +0.0009 | 0.0121 | [-0.0228; +0.0246] | [-11.4; +12.3] | [-10.8; +13.1] | [+0.6; +0.8] |
| tx_homens | +0.0005 | 0.0125 | [-0.0240; +0.0251] | [-12.0; +12.5] | [-11.3; +13.4] | [+0.7; +0.8] |
| tx_mulheres | -0.0007 | 0.0105 | [-0.0213; +0.0199] | [-10.6; +10.0] | [-10.1; +10.5] | [+0.5; +0.5] |
| tx_negros | -0.0070 | 0.0146 | [-0.0356; +0.0215] | [-17.8; +10.7] | [-16.3; +11.3] | [+1.5; +0.6] |
| tx_nao_negros | -0.0016 | 0.0171 | [-0.0352; +0.0320] | [-17.6; +16.0] | [-16.1; +17.3] | [+1.5; +1.3] |
| tx_arma | +0.0009 | 0.0185 | [-0.0353; +0.0371] | [-17.7; +18.5] | [-16.2; +20.4] | [+1.5; +1.8] |

BLS9 2021 (Zucco & Power): PT -0.69, DEM +0.43, PL +0.49; k = 1.12 (PT->DEM) e 1.18 (PT->PL).

| desfecho (BLS9) | destino | k | linear (%) | exato (%) |
|---|---|---|---|---|
| tx_total | DEM | 1.12 | [-11.1; +14.5] | [-10.5; +15.6] |
| tx_total | PL | 1.18 | [-11.7; +15.3] | [-11.1; +16.5] |
| tx_homens | DEM | 1.12 | [-11.6; +15.1] | [-11.0; +16.4] |
| tx_homens | PL | 1.18 | [-12.3; +16.0] | [-11.5; +17.3] |
| tx_mulheres | DEM | 1.12 | [-11.5; +10.7] | [-10.9; +11.2] |
| tx_mulheres | PL | 1.18 | [-12.2; +11.2] | [-11.5; +11.9] |
| tx_negros | DEM | 1.12 | [-17.4; +13.7] | [-16.0; +14.7] |
| tx_negros | PL | 1.18 | [-18.3; +14.5] | [-16.8; +15.6] |
| tx_nao_negros | DEM | 1.12 | [-18.8; +18.0] | [-17.1; +19.7] |
| tx_nao_negros | PL | 1.18 | [-19.8; +19.0] | [-18.0; +20.9] |
| tx_arma | DEM | 1.12 | [-17.2; +21.8] | [-15.8; +24.4] |
| tx_arma | PL | 1.18 | [-18.2; +23.0] | [-16.6; +25.9] |

## 2. Event study empilhado (stacked DD), ln(taxa), referência tau=-1, IC95% com t(G-1), EP agrupado por UF

### BRC (principal) — desenho estrito — esquerda->direita: 9 eventos (anos: {2015: 4, 2019: 5})

**tx_total** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.047 [-0.071; +0.164] | +0.020 [-0.060; +0.100] | -0.066 [-0.152; +0.021] | -0.168 [-0.295; -0.041] | -0.329 [-0.556; -0.101] | -0.325 [-0.532; -0.117] |

Antecipações conjuntas (tau=-3,-2): F=0.39, p=0.685; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=3.01, p=0.055. Média dos pós: -0.2217 [-0.3627; -0.0807] = [-30.4%; -7.8%].

**tx_mulheres** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.004 [-0.168; +0.159] | -0.126 [-0.297; +0.046] | -0.098 [-0.245; +0.050] | -0.231 [-0.382; -0.080] | -0.265 [-0.430; -0.100] | -0.273 [-0.471; -0.076] |

Antecipações conjuntas (tau=-3,-2): F=1.76, p=0.209; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=3.83, p=0.026. Média dos pós: -0.2167 [-0.3423; -0.0910] = [-29.0%; -8.7%].

**tx_negros** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.039 [-0.114; +0.191] | -0.005 [-0.102; +0.091] | -0.106 [-0.188; -0.024] | -0.235 [-0.371; -0.099] | -0.401 [-0.633; -0.170] | -0.393 [-0.621; -0.164] |

Antecipações conjuntas (tau=-3,-2): F=0.34, p=0.719; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=4.88, p=0.011. Média dos pós: -0.2836 [-0.4322; -0.1351] = [-35.1%; -12.6%].

**tx_arma** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.053 [-0.118; +0.224] | +0.044 [-0.086; +0.174] | -0.133 [-0.237; -0.029] | -0.244 [-0.413; -0.076] | -0.477 [-0.831; -0.124] | -0.491 [-0.815; -0.167] |

Antecipações conjuntas (tau=-3,-2): F=0.34, p=0.715; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=2.90, p=0.061. Média dos pós: -0.3365 [-0.5557; -0.1173] = [-42.6%; -11.1%].

### BRC (principal) — desenho estrito — direita->esquerda: 10 eventos (anos: {2015: 6, 2019: 4})

**tx_total** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.186 [-0.336; -0.037] | -0.071 [-0.201; +0.059] | -0.098 [-0.205; +0.008] | -0.200 [-0.393; -0.007] | -0.265 [-0.479; -0.052] | -0.261 [-0.486; -0.036] |

Antecipações conjuntas (tau=-3,-2): F=6.50, p=0.009; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=2.03, p=0.142. Média dos pós: -0.2062 [-0.3741; -0.0382] = [-31.2%; -3.7%].

**tx_mulheres** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.214 [-0.393; -0.035] | -0.151 [-0.376; +0.074] | -0.113 [-0.256; +0.030] | -0.282 [-0.437; -0.128] | -0.230 [-0.525; +0.065] | -0.285 [-0.562; -0.007] |

Antecipações conjuntas (tau=-3,-2): F=3.36, p=0.062; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=7.36, p=0.002. Média dos pós: -0.2275 [-0.4179; -0.0372] = [-34.2%; -3.6%].

**tx_negros** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.241 [-0.383; -0.100] | -0.129 [-0.263; +0.006] | -0.113 [-0.231; +0.005] | -0.201 [-0.406; +0.003] | -0.248 [-0.503; +0.008] | -0.268 [-0.548; +0.013] |

Antecipações conjuntas (tau=-3,-2): F=8.61, p=0.003; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=1.43, p=0.272. Média dos pós: -0.2073 [-0.4022; -0.0125] = [-33.1%; -1.2%].

**tx_arma** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.250 [-0.432; -0.068] | -0.097 [-0.261; +0.068] | -0.158 [-0.292; -0.024] | -0.259 [-0.478; -0.040] | -0.389 [-0.677; -0.100] | -0.374 [-0.661; -0.087] |

Antecipações conjuntas (tau=-3,-2): F=10.16, p=0.002; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=2.81, p=0.064. Média dos pós: -0.2948 [-0.5006; -0.0890] = [-39.4%; -8.5%].

### BRC (principal) — desenho truncado — esquerda->direita: 26 eventos (anos: {2014: 3, 2015: 4, 2018: 2, 2019: 6, 2022: 4, 2023: 7})

**tx_total** (n eventos 26, UFs controle distintas 27, clusters G=27, obs 1822)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.030 [-0.047; +0.107] | +0.060 [+0.013; +0.108] | -0.001 [-0.036; +0.033] | -0.102 [-0.186; -0.017] | -0.297 [-0.486; -0.107] | -0.293 [-0.472; -0.115] |

Antecipações conjuntas (tau=-3,-2): F=4.10, p=0.028; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=3.15, p=0.031. Média dos pós: -0.1732 [-0.2793; -0.0672] = [-24.4%; -6.5%].

### BRC (principal) — desenho truncado — direita->esquerda: 20 eventos (anos: {2014: 2, 2015: 7, 2017: 1, 2018: 5, 2019: 4, 2023: 1})

**tx_total** (n eventos 20, UFs controle distintas 26, clusters G=27, obs 1277)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.067 [-0.189; +0.055] | -0.006 [-0.099; +0.087] | -0.070 [-0.171; +0.030] | -0.148 [-0.300; +0.004] | -0.194 [-0.378; -0.010] | -0.205 [-0.393; -0.017] |

Antecipações conjuntas (tau=-3,-2): F=1.61, p=0.219; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=1.39, p=0.264. Média dos pós: -0.1542 [-0.2921; -0.0164] = [-25.3%; -1.6%].

### tse escore único (conferência) — desenho estrito — esquerda->direita: 9 eventos (anos: {2015: 4, 2019: 5})

**tx_total** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.047 [-0.071; +0.164] | +0.020 [-0.060; +0.100] | -0.066 [-0.152; +0.021] | -0.168 [-0.295; -0.041] | -0.329 [-0.556; -0.101] | -0.325 [-0.532; -0.117] |

Antecipações conjuntas (tau=-3,-2): F=0.39, p=0.685; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=3.01, p=0.055. Média dos pós: -0.2217 [-0.3627; -0.0807] = [-30.4%; -7.8%].

**tx_mulheres** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.004 [-0.168; +0.159] | -0.126 [-0.297; +0.046] | -0.098 [-0.245; +0.050] | -0.231 [-0.382; -0.080] | -0.265 [-0.430; -0.100] | -0.273 [-0.471; -0.076] |

Antecipações conjuntas (tau=-3,-2): F=1.76, p=0.209; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=3.83, p=0.026. Média dos pós: -0.2167 [-0.3423; -0.0910] = [-29.0%; -8.7%].

**tx_negros** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.039 [-0.114; +0.191] | -0.005 [-0.102; +0.091] | -0.106 [-0.188; -0.024] | -0.235 [-0.371; -0.099] | -0.401 [-0.633; -0.170] | -0.393 [-0.621; -0.164] |

Antecipações conjuntas (tau=-3,-2): F=0.34, p=0.719; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=4.88, p=0.011. Média dos pós: -0.2836 [-0.4322; -0.1351] = [-35.1%; -12.6%].

**tx_arma** (n eventos 9, UFs controle distintas 10, clusters G=15, obs 476)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | +0.053 [-0.118; +0.224] | +0.044 [-0.086; +0.174] | -0.133 [-0.237; -0.029] | -0.244 [-0.413; -0.076] | -0.477 [-0.831; -0.124] | -0.491 [-0.815; -0.167] |

Antecipações conjuntas (tau=-3,-2): F=0.34, p=0.715; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=2.90, p=0.061. Média dos pós: -0.3365 [-0.5557; -0.1173] = [-42.6%; -11.1%].

### tse escore único (conferência) — desenho estrito — direita->esquerda: 10 eventos (anos: {2015: 6, 2019: 4})

**tx_total** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.186 [-0.336; -0.037] | -0.071 [-0.201; +0.059] | -0.098 [-0.205; +0.008] | -0.200 [-0.393; -0.007] | -0.265 [-0.479; -0.052] | -0.261 [-0.486; -0.036] |

Antecipações conjuntas (tau=-3,-2): F=6.50, p=0.009; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=2.03, p=0.142. Média dos pós: -0.2062 [-0.3741; -0.0382] = [-31.2%; -3.7%].

**tx_mulheres** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.214 [-0.393; -0.035] | -0.151 [-0.376; +0.074] | -0.113 [-0.256; +0.030] | -0.282 [-0.437; -0.128] | -0.230 [-0.525; +0.065] | -0.285 [-0.562; -0.007] |

Antecipações conjuntas (tau=-3,-2): F=3.36, p=0.062; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=7.36, p=0.002. Média dos pós: -0.2275 [-0.4179; -0.0372] = [-34.2%; -3.6%].

**tx_negros** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.241 [-0.383; -0.100] | -0.129 [-0.263; +0.006] | -0.113 [-0.231; +0.005] | -0.201 [-0.406; +0.003] | -0.248 [-0.503; +0.008] | -0.268 [-0.548; +0.013] |

Antecipações conjuntas (tau=-3,-2): F=8.61, p=0.003; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=1.43, p=0.272. Média dos pós: -0.2073 [-0.4022; -0.0125] = [-33.1%; -1.2%].

**tx_arma** (n eventos 10, UFs controle distintas 10, clusters G=16, obs 518)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.250 [-0.432; -0.068] | -0.097 [-0.261; +0.068] | -0.158 [-0.292; -0.024] | -0.259 [-0.478; -0.040] | -0.389 [-0.677; -0.100] | -0.374 [-0.661; -0.087] |

Antecipações conjuntas (tau=-3,-2): F=10.16, p=0.002; algum IC de antecipação exclui 0: True. Pós conjunto (0..3): F=2.81, p=0.064. Média dos pós: -0.2948 [-0.5006; -0.0890] = [-39.4%; -8.5%].

### tse escore único (conferência) — desenho truncado — esquerda->direita: 25 eventos (anos: {2014: 3, 2015: 4, 2018: 2, 2019: 6, 2022: 3, 2023: 7})

**tx_total** (n eventos 25, UFs controle distintas 27, clusters G=27, obs 1692)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.005 [-0.091; +0.081] | +0.050 [-0.001; +0.101] | -0.016 [-0.056; +0.024] | -0.121 [-0.201; -0.042] | -0.312 [-0.496; -0.128] | -0.309 [-0.485; -0.133] |

Antecipações conjuntas (tau=-3,-2): F=2.01, p=0.154; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=3.81, p=0.014. Média dos pós: -0.1898 [-0.2904; -0.0891] = [-25.2%; -8.5%].

### tse escore único (conferência) — desenho truncado — direita->esquerda: 22 eventos (anos: {2014: 2, 2015: 7, 2017: 1, 2018: 5, 2019: 4, 2022: 1, 2023: 2})

**tx_total** (n eventos 22, UFs controle distintas 27, clusters G=27, obs 1443)

| tau | -3 | -2 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| beta [IC95% t] | -0.046 [-0.168; +0.077] | +0.003 [-0.096; +0.102] | -0.049 [-0.148; +0.049] | -0.103 [-0.250; +0.044] | -0.175 [-0.361; +0.012] | -0.186 [-0.374; +0.002] |

Antecipações conjuntas (tau=-3,-2): F=1.33, p=0.282; algum IC de antecipação exclui 0: False. Pós conjunto (0..3): F=1.22, p=0.327. Média dos pós: -0.1282 [-0.2658; +0.0094] = [-23.3%; +0.9%].

## 2b. PÓS-HOC (não pré-registrado, não entra em veredito): composição e coortes do desenho estrito, painel BRC, desfecho tx_total

- esquerda->direita, evento em 2015: tratados ['Distrito Federal', 'Espírito Santo', 'Mato Grosso do Sul', 'Rio Grande do Sul']; controles limpos ['Acre', 'Bahia', 'Paraíba', 'Pará', 'Pernambuco', 'Rio de Janeiro']
- esquerda->direita, evento em 2019: tratados ['Acre', 'Distrito Federal', 'Mato Grosso', 'Minas Gerais', 'Rio de Janeiro']; controles limpos ['Alagoas', 'Amapá', 'Bahia', 'Mato Grosso do Sul', 'Paraíba', 'Pernambuco', 'Piauí']
- direita->esquerda, evento em 2015: tratados ['Alagoas', 'Amapá', 'Ceará', 'Maranhão', 'Mato Grosso', 'Rio Grande do Norte']; controles limpos ['Acre', 'Bahia', 'Paraíba', 'Pará', 'Pernambuco', 'Rio de Janeiro']
- direita->esquerda, evento em 2019: tratados ['Espírito Santo', 'Pará', 'Rio Grande do Norte', 'Roraima']; controles limpos ['Alagoas', 'Amapá', 'Bahia', 'Mato Grosso do Sul', 'Paraíba', 'Pernambuco', 'Piauí']

| recorte | n eventos | média dos pós (tx_total) [IC95% t] | % exato | p antecipações |
|---|---|---|---|---|
| esq->dir, só evento 2015 | 4 | -0.268 [-0.515; -0.021] | [-40.3%; -2.0%] | 0.103 |
| esq->dir, só evento 2019 | 5 | -0.186 [-0.353; -0.018] | [-29.7%; -1.8%] | 0.659 |
| dir->esq, só evento 2015 | 6 | -0.165 [-0.405; +0.075] | [-33.3%; +7.8%] | 0.125 |
| dir->esq, só evento 2019 | 4 | -0.267 [-0.534; +0.001] | [-41.4%; +0.1%] | 0.014 |
| ambas as direções juntas (qualquer troca de governo, ignorando o sentido) | 19 | -0.214 [-0.337; -0.090] | [-28.6%; -8.6%] | 0.353 |

Leitura pós-hoc: se a ideologia importasse, as duas direções teriam sinais opostos; o mesmo sinal nas duas aponta para efeito de qualquer troca de governo, de seleção dos controles (UFs sem troca em 7 anos) ou de tendência pré-existente, e não para ideologia. Pós-hoc: serve para NÃO ler o event study como corroboração nem como refutação.


## 3. Pesos do TWFE contínuo (painel BRC, 351 UF-anos balanceados)

- Observações com eps < 0: 46.2% (mecânico: ~50% num painel balanceado; não é defeito por si).
- Massa de peso negativo: sob eps 50.0%; sob eps x (D - D_UF) 0.2%; sob eps x (D - D_médio) 8.3% (depende da origem de D: variantes, não verdades).

| desfecho | b TWFE | b+ (eps>0) [IC95% t(26)] | b- (eps<0) [IC95% t(26)] | razão b_TWFE/b+ |
|---|---|---|---|---|
| tx_total | +0.0009 | -0.0015 [-0.0246; +0.0216] | +0.0030 [-0.0231; +0.0291] | não reportada (|b TWFE| <= 2 EP) |
| tx_homens | +0.0005 | -0.0014 [-0.0253; +0.0225] | +0.0022 [-0.0250; +0.0294] | não reportada (|b TWFE| <= 2 EP) |
| tx_mulheres | -0.0007 | -0.0053 [-0.0277; +0.0172] | +0.0034 [-0.0188; +0.0256] | não reportada (|b TWFE| <= 2 EP) |
| tx_negros | -0.0070 | -0.0070 [-0.0329; +0.0188] | -0.0071 [-0.0405; +0.0263] | não reportada (|b TWFE| <= 2 EP) |
| tx_nao_negros | -0.0016 | -0.0098 [-0.0511; +0.0315] | +0.0056 [-0.0255; +0.0367] | não reportada (|b TWFE| <= 2 EP) |
| tx_arma | +0.0009 | -0.0011 [-0.0360; +0.0338] | +0.0026 [-0.0379; +0.0431] | não reportada (|b TWFE| <= 2 EP) |
