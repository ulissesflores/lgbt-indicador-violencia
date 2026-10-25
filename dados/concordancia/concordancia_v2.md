# Concordância Sinan x Anuário por UF, 2022-2025 - v2 (líquida de tamanho)

Gerado por dados/concordancia/concordancia_v2.py (semente 20261021). Substitui a leitura da v1: o Spearman de CONTAGENS (0,49-0,74) é efeito de tamanho da UF.

## 1. Resultado principal (pop = Censo 2022; Anuário = edição mais recente de cada ano)

| ano | n UFs | rho contagens (v1) | rho(Sinan,pop) | rho(BO,pop) | rho esperado só por tamanho | rho taxas/100 mil [IC95%] (p) | **rho parcial dado pop** [IC95% bootstrap] (p perm.) | leave-one-out parcial |
|---|---|---|---|---|---|---|---|---|
| 2022 | 22 | 0.53 | 0.77 | 0.59 | 0.45 | 0.01 [-0.42; 0.43] (p=0.980) | **0.14** [-0.33; 0.62] (p=0.539) | -0.02 a 0.31 |
| 2023 | 23 | 0.58 | 0.89 | 0.58 | 0.51 | 0.08 [-0.32; 0.46] (p=0.712) | **0.17** [-0.30; 0.56] (p=0.443) | 0.02 a 0.29 |
| 2024 | 23 | 0.59 | 0.87 | 0.61 | 0.53 | 0.12 [-0.29; 0.47] (p=0.589) | **0.15** [-0.28; 0.51] (p=0.493) | 0.04 a 0.22 |
| 2025 | 22 | 0.74 | 0.87 | 0.73 | 0.63 | 0.36 [-0.07; 0.66] (p=0.101) | **0.32** [-0.16; 0.68] (p=0.146) | 0.22 a 0.45 |

**Pooled 2022-25 (média de Fisher das correlações parciais anuais): 0.20 [IC95% bootstrap por UF: -0.13; 0.50]**

Leitura: o tamanho sozinho (produto das correlações de cada série com a população) prevê rho de 0,45 a 0,63 dos 0,53 a 0,74 observados em contagens; o que sobra é pequeno e estatisticamente indistinguível de zero em todos os anos (parcial 0,14 a 0,32, IC95% sempre incluindo zero). O controle de especificidade (racismo no Sinan x BO LGBT) dá resíduo parecido, então o pouco que sobra não é específico de LGBTfobia (sistema, tamanho não capturado).

## 2. Sensibilidades e controle (rho parcial | pop, por ano; entre colchetes IC95% bootstrap)

| especificação | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| S0 principal (censo 2022, edição nova, '-'=NA) | 0.14 [-0.33; 0.62] (n=22) | 0.17 [-0.30; 0.56] (n=23) | 0.15 [-0.28; 0.51] (n=23) | 0.32 [-0.16; 0.68] (n=22) |
| S1 pop = estimativa anual SIDRA 6579 (2022 = Censo; 2023 interpolado) | 0.14 [-0.33; 0.61] (n=22) | 0.17 [-0.31; 0.55] (n=23) | 0.17 [-0.29; 0.52] (n=23) | 0.32 [-0.14; 0.68] (n=22) |
| S2 Anuário: edição mais antiga de cada ano | 0.14 [-0.35; 0.61] (n=22) | 0.24 [-0.28; 0.65] (n=24) | -0.08 [-0.53; 0.48] (n=23) | 0.32 [-0.14; 0.68] (n=22) |
| S3 '-' (fenômeno inexistente) tratado como 0 | 0.08 [-0.32; 0.55] (n=23) | 0.22 [-0.24; 0.56] (n=24) | 0.04 [-0.41; 0.44] (n=24) | 0.20 [-0.31; 0.62] (n=23) |
| S6 regra da v1 (por UF, edição mais recente COM valor; mistura edições) | 0.14 [-0.33; 0.61] (n=22) | 0.15 [-0.30; 0.54] (n=24) | 0.02 [-0.41; 0.40] (n=25) | 0.32 [-0.16; 0.68] (n=22) |
| C1 controle: Sinan RACISMO x BO LGBT (mesma metodologia) | 0.17 [-0.36; 0.57] (n=22) | 0.04 [-0.50; 0.53] (n=23) | 0.34 [-0.11; 0.64] (n=23) | 0.01 [-0.35; 0.45] (n=22) |

Taxas por 100 mil (rho Spearman), mesmas especificações:

| especificação | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| S0 principal (censo 2022, edição nova, '-'=NA) | 0.01 | 0.08 | 0.12 | 0.36 |
| S1 pop = estimativa anual SIDRA 6579 (2022 = Censo; 2023 interpolado) | 0.01 | 0.09 | 0.10 | 0.36 |
| S2 Anuário: edição mais antiga de cada ano | 0.01 | 0.23 | 0.05 | 0.36 |
| S3 '-' (fenômeno inexistente) tratado como 0 | 0.03 | 0.13 | 0.02 | 0.26 |
| S6 regra da v1 (por UF, edição mais recente COM valor; mistura edições) | 0.01 | 0.09 | 0.03 | 0.36 |
| C1 controle: Sinan RACISMO x BO LGBT (mesma metodologia) | 0.22 | -0.02 | 0.30 | 0.21 |

Pearson em log(taxa+0,5) e Spearman de taxas por notificação Sinan (S0):

| medida | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Pearson log-taxas | 0.07 | 0.13 | 0.14 | 0.37 |
| Spearman taxas por notificação Sinan | -0.12 | -0.02 | -0.27 | 0.06 |


Reconciliação com a v1 (rho de CONTAGENS publicado: 0,53 / 0,56 / 0,49 / 0,74): a regra da v1 (S6) reproduz esses valores; a diferença para a tabela principal vem de a v1 completar UFs com NA na edição nova usando a edição anterior. A v2 usa uma única edição por ano (definição consistente).

| rho de contagens | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| S6 (regra v1) | 0.53 | 0.56 | 0.49 | 0.74 |
| S0 (edição única) | 0.53 | 0.58 | 0.59 | 0.74 |

Pooled (média de Fisher das parciais anuais) por especificação:

| especificação | pooled [IC95%] |
|---|---|
| S0 principal | 0.20 [-0.13; 0.50] |
| S1 pop anual | 0.20 [-0.16; 0.51] |
| S2 edição antiga | 0.16 [-0.23; 0.53] |
| S3 '-'=0 | 0.14 [-0.24; 0.45] |
| C1 controle racismo | 0.14 [-0.19; 0.47] |

## 3. O que NÃO muda: o NÍVEL relativo dos dois sistemas

A razão BO/Sinan (mediana das UFs com Sinan>0) usa contagem contra contagem na mesma UF, então o tamanho se cancela; a v1 reportou 0,78 (2022) -> 1,21 (2025). Esta v2 confirma o cálculo:

| ano | mediana BO/Sinan |
|---|---|
| 2022 | 0.78 |
| 2023 | 0.81 |
| 2024 | 1.19 |
| 2025 | 1.21 |

### 3b. Candidatos a zero cerimonial (Anuário '-' = fenômeno inexistente, mas o Sinan notificou LGBTfobia na mesma UF e ano; edição mais recente)

| ano | UF (notificações Sinan de LGBTfobia) |
|---|---|
| 2022 | PA (39) |
| 2023 | PA (36) |
| 2024 | TO (18) |
| 2025 | TO (17) |

A v1 dizia 'nenhuma UF com BO=0 e Sinan>0' porque descartava '-' como NA; lido como zero, essas UFs são o candidato empírico a 'zero cerimonial' do lado policial (ou ausência de tipificação/campo).

## 4. Limites que valem para qualquer leitura

- n de 22 a 25 UFs por ano: baixo poder (simulação, teste de Spearman bicaudal a 5%, n=23): rho=0.3: poder 0.29; rho=0.5: poder 0.69; rho=0.7: poder 0.97. IC largo = AUSÊNCIA DE EVIDÊNCIA de concordância líquida, não evidência de discordância.
- Sinan conta notificação (serviço de saúde), BO conta ocorrência com marcação de motivação (polícia): construtos distintos; correlação baixa pode refletir isso e não 'erro' de um deles.
- 2025 do Sinan é arquivo preliminar quando o FINAL não existia; UFs sem dado no Anuário (4-5 por ano) saem; 'ceremonial zeros' (S3) mudam pouco.
- A população usada é denominador de tamanho, não de exposição; nenhuma das duas fontes mede incidência (ver dossiê §3: não identificabilidade).

