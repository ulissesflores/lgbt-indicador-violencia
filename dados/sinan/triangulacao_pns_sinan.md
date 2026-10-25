# Triangulação PNS 2019 x Sinan VIVA, adultos 18+, violência física interpessoal (gerado por triangulacao_pns_sinan.py)

## 1. Reprodução dos números já publicados em resumo.md (2026-10-12)

| indicador | ano | publicado | recalculado | confere |
|---|---|---|---|---|
| n_interp | 2023 | 405941 | 405941 | sim |
| f55_ign | 2023 | 29.3 | 29.27 | sim |
| f55_na | 2023 | 14.9 | 14.88 | sim |
| sexismo | 2023 | 20.3 | 20.34 | sim |
| lgbtf | 2023 | 2173 | 2173 | sim |
| lgbtf_pct | 2023 | 0.54 | 0.54 | sim |
| lgbtf_valid | 2023 | 0.96 | 0.96 | sim |
| f36_ign | 2023 | 19.0 | 19.01 | sim |
| f36_na | 2023 | 24.7 | 24.71 | sim |
| homo | 2023 | 1.8 | 1.80 | sim |
| bi | 2023 | 0.67 | 0.67 | sim |
| hb_valid | 2023 | 4.39 | 4.39 | sim |
| f37_ign | 2023 | 26.1 | 26.09 | sim |
| f37_na | 2023 | 72.5 | 72.51 | sim |
| trans | 2023 | 5659 | 5659 | sim |
| trans_pct | 2023 | 1.39 | 1.39 | sim |
| n_fis | 2023 | 197779 | 197779 | sim |
| o_ign | 2023 | 20.4 | 20.39 | sim |
| o_na | 2023 | 3.9 | 3.91 | sim |
| o_valid | 2023 | 75.7 | 75.70 | sim |
| hb_fis | 2023 | 4.12 | 4.12 | sim |
| hb_fis_n | 2023 | 6169 | 6169 | sim |
| f55_fis_ign | 2023 | 27.5 | 27.48 | sim |
| f55_fis_na | 2023 | 11.5 | 11.52 | sim |
| n_interp | 2024 | 426622 | 426622 | sim |
| f55_ign | 2024 | 27.7 | 27.66 | sim |
| f55_na | 2024 | 14.8 | 14.81 | sim |
| sexismo | 2024 | 20.4 | 20.37 | sim |
| lgbtf | 2024 | 2264 | 2264 | sim |
| lgbtf_pct | 2024 | 0.53 | 0.53 | sim |
| lgbtf_valid | 2024 | 0.92 | 0.92 | sim |
| f36_ign | 2024 | 18.4 | 18.37 | sim |
| f36_na | 2024 | 25.6 | 25.60 | sim |
| homo | 2024 | 1.74 | 1.74 | sim |
| bi | 2024 | 0.67 | 0.67 | sim |
| hb_valid | 2024 | 4.31 | 4.31 | sim |
| f37_ign | 2024 | 25.7 | 25.68 | sim |
| f37_na | 2024 | 73.0 | 72.98 | sim |
| trans | 2024 | 5716 | 5716 | sim |
| trans_pct | 2024 | 1.34 | 1.34 | sim |
| n_fis | 2024 | 202416 | 202416 | sim |
| o_ign | 2024 | 20.2 | 20.24 | sim |
| o_na | 2024 | 4.0 | 3.96 | sim |
| o_valid | 2024 | 75.8 | 75.80 | sim |
| hb_fis | 2024 | 4.08 | 4.08 | sim |
| hb_fis_n | 2024 | 6260 | 6260 | sim |
| f55_fis_ign | 2024 | 27.0 | 27.03 | sim |
| f55_fis_na | 2024 | 11.5 | 11.46 | sim |

Divergências: 0.

## 2. PNS 2019: parcela LGB+ implícita entre adultos com violência física (12 meses)

| cenário | estimativa pontual | IC95% (Monte Carlo, 200 mil sorteios) |
|---|---|---|
| B. denominador antigo do dossiê (todos os não-LGB+ com a taxa dos heterossexuais) | 6.90% | 5.25% a 9.03% |
| A. só respondentes de orientação válida (hetero + LGB+), comparável ao Sinan | 7.13% | 5.43% a 9.32% |

Insumos (PNS, % e IC95%): lgb 1.89 (1.73-2.07); hetero 94.75 (94.46-95.03); fis_lgb 14.7 (11.16-19.12); fis_het 3.82 (3.57-4.09); fis_total 4.15 (3.89-4.42). Insumos independentes entre si (hipótese; a PNS é uma só amostra, a covariância não é publicada, logo o intervalo é aproximado).

## 3. Sinan: parcela LGB+ entre notificações de violência física de adultos, e razão com a PNS

| ano | n | orientação válida | LGB+ entre válidas | razão Sinan/PNS(A) | cenário MCAR | pior caso (0% LGB+ entre não respondidas) | melhor caso (100%) |
|---|---|---|---|---|---|---|---|
| 2023 | 197,779 | 75.7% | 4.12% | 0.58 | 4.12% | 3.12% | 27.42% |
|  | para igualar a PNS(A), as 24.3% não respondidas precisariam ter 16.5% LGB+ | | | | | | |
| 2024 | 202,416 | 75.8% | 4.08% | 0.57 | 4.08% | 3.09% | 27.29% |
|  | para igualar a PNS(A), as 24.2% não respondidas precisariam ter 16.7% LGB+ | | | | | | |

Leitura: ver dossiê. O Sinan é registro da população que procurou serviço de saúde, não amostra; por isso não se atribui IC amostral à parcela do Sinan (é contagem de notificações, não estimativa). A comparação de interesse é a razão em relação à prevalência populacional (LGB+ = 1,89% de todos os adultos; 1,96% entre os que responderam hetero/LGB+).

