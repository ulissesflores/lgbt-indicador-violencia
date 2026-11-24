# Origem dos números da Figura E1 (mortalidade internacional)

Tabela de origem extraída da proposta de 2026-10-24 (registro da versão 1.2.0, DOI de conceito 10.5281/zenodo.23873858).

## De onde vem cada número

Raiz dos arquivos: `<pasta-de-trabalho>/v03/L-fontes/`. sha256 de cada arquivo no ledger.

| número no texto | trecho verbatim (curto) | arquivo local | página / aba-linha |
|---|---|---|---|
| 59 variáveis, 9 blocos | "composta por 59 variáveis distribuídas em 9 blocos" | `manual-do/manual-do-ms-2022.pdf` | p. 10 (PDF p. 11); também p. 30 |
| DO sem orientação/identidade | busca por palavra isolada no texto extraído: "orientação" 1 ocorrência (l. 1045, sobre "Pessoa não identificada", não é campo), "identidade" 1 (l. 1748, documento de identidade), "gênero" 0, "sexual" 0, "nome social" 0 | `manual-do/manual.txt` (de `manual-do-ms-2022.pdf`) | documento inteiro, 68 p. |
| 36.452; 1.325; 563; 42,5% | "1.325 foram pareados a óbitos (3,6% do total das notificações) e, destes, 563 (42,5%)" | `luis-ress-2026/luis-pt.pdf` | p. 5, Resultados e Tabela 1 |
| causas violentas = homicídio + suicídio + indeterminada | "X85-Y09, Y35, Y87.1 (homicídios); X60-X84, Y87.0 (suicídios); e Y10-Y34 (causas indeterminadas)" | `luis-ress-2026/luis-pt.pdf` | p. 3, Variáveis; p. 4, Controle de viés |
| nome, nome da mãe; termo de confidencialidade | "obtidos por meio de solicitação à Secretaria de Vigilância em Saúde e Ambiente, com assinatura ... do registro de responsabilidade e confidencialidade" | `luis-ress-2026/luis-pt.pdf` | p. 4, Acesso aos dados |
| 28.659.465 pessoas | "Our final study population comprised 28,659,465 individuals" | `ons-mortalidade-2026/bulletin.html` | seção 9, Data sources and quality |
| 982,8 x 752,6 por 100 mil | "the age-standardised rate was 982.8 per 100,000 people for the LGB+ group, compared with 752.6" | `ons-mortalidade-2026/bulletin.html` | seção 1, Main points |
| razão 1,31 (1,28-1,33) | linha "England and Wales, Total, Total, LGB+, Straight or Heterosexual, 1.31, 1.28, 1.33" | `ons-mortalidade-2026/tabelas.xlsx` | aba Table_5, linha 7 |
| gay/lésbica 1,31 (1,28-1,35); bissexual 1,33 (1,28-1,38) | linhas "Gay or Lesbian ... 1.31, 1.28, 1.35" e "Bisexual ... 1.33, 1.28, 1.38" | `ons-mortalidade-2026/tabelas.xlsx` | aba Table_5, linhas 8 e 9 |
| homens gays 1,23 (1,20-1,27) | linha "England and Wales, Sex, Male, Gay or Lesbian, Straight or Heterosexual, 1.23, 1.2, 1.27" | `ons-mortalidade-2026/tabelas.xlsx` | aba Table_5, linha 40 |
| taxas do período, não anuais | "rates were calculated per 100,000 people between 21 March 2021 and 30 November 2024 and were not calculated as annual rates" | `ons-mortalidade-2026/bulletin.html` | seção 2 |
| padronização pela idade dos LGB+ | "standardised using age-specific weights representing the age distribution of the observed LGB+ study population" | `ons-mortalidade-2026/bulletin.html` | seção 8, Glossary |
| não causal | "It is not possible to say whether sexual orientation is a causal risk factor" | `ons-mortalidade-2026/bulletin.html` | seção 2 (caixa) |
| homicídio só no top-10; LGB+ mulheres 16-24, 5 óbitos | linha "Female, 16 to 24 years, LGB+, U50.9, X85-Y09, Y87.1, Homicide and probable homicide, 5, 3.23" | `ons-mortalidade-2026/tabelas.xlsx` | aba Table_3, linha 467 |
| arredondamento a múltiplos de 5 | "all calculations are based on estimates rounded to the nearest multiple of five" | `ons-mortalidade-2026/tabelas.xlsx` | aba Notes, Note 1 |
| suicídio 50,3 x 23,1; 2,2 vezes | "age-standardised rate of suicide ... was 50.3 per 100,000 people, compared with 23.1" | `ons-suicidio-2025/bulletin.html` | seção 1, Main points |
| suicídio inclui intenção indeterminada | "deaths caused by injury or poisoning where the intent was undetermined" | `ons-suicidio-2025/bulletin.html` | seção 6, Glossary |
| -1,2 ano (59,4 x 60,7); -0,9 ano (63,0 x 64,0) | "life expectancy was 59.4 years for LGB+ men and 60.7 years for straight or heterosexual men" | `ons-expectativa-2026/bulletin.html` | seção 1, Main points |
| diferenças sobre valores não arredondados; estimativas superestimadas | "Any differences are based on unrounded figures."; "these experimental estimates are likely to overestimate life expectancy" | `ons-expectativa-2026/bulletin.html` | seção 1 (caixa) |
| sem teste formal | "No formal statistical significance testing was applied." | `ons-expectativa-2026/bulletin.html` | seção 3, Glossary |
| 90.833; 81 óbitos LGB; 27 anos | "8.0% (n = 81) for LGB participants"; "over the 27-year study period" | `mcketta-jama-2024/pmc.html` | Results, 1º parágrafo |
| fator de aceleração 0,74 (0,64-0,84) | "adjusted acceleration factor, 0.74 [95% CI, 0.64-0.84]" | `mcketta-jama-2024/pmc.html` | Abstract, Results |
| 3.759 pessoas trans | "a total of 3759 individuals (0.06%) were identified as having a transgender identity" | `erlangsen-jama-2023/pmc.html` | Results, 1º parágrafo |
| aIRR todas as causas 2,0 (1,7-2,4) | "an aIRR of 2.0 (95% CI, 1.7-2.4)" | `erlangsen-jama-2023/pmc.html` | Results, All-Cause Mortality |
| aIRR suicídio 3,5 (2,0-6,3); 12 suicídios | "Twelve transgender individuals died by suicide"; "an aIRR of 3.5 (95% CI, 2.0-6.3)" | `erlangsen-jama-2023/pmc.html` | Results, Suicide Mortality |
| Zachry: 43 estudos; 14 / 28 / 1; homicídio n = 7 | "14 studies (32.6%) supported higher mortality for SGM, 28 studies (65.1%) provided partial support ... one study (2.3%) found no evidence"; "homicide (n = 7)" | `<pasta-de-trabalho>/fontes/q1-textointegral/discurso/mortalidade/10.1371_journal.pone.0307688.PMC12140117.xml` (sha256 `1030fbd3…be93`) | Abstract |
| Zachry: síntese positiva | "Although mixed, findings suggest elevated mortality for SGM versus non-SGM populations" | idem | Abstract |
| McLellan: 94 estudos, 137 artigos; 64,23% (47,38-78,17) | "A total of 94 studies published in 137 of the 29 987 identified articles"; "64.23% (9 studies; 95% CI, 47.38%-78.17%)" | `mclellan-jamano-2026/artigo.md` | Abstract, Results (linha 185 do .md) |
| McLellan: nenhum estudo de homicídio | "While we would have included homicide, we identified no studies that reported its prevalence." | `mclellan-jamano-2026/artigo.md` | Discussion (linha 342 do .md) |
| correção sem mudar estimativas | "panel A should have been labeled ... Supplement 1 was missing the eFigure" | `mclellan-jamano-2026/correcao.md` | texto da correção |
| Halliwell: 229; 78,6% | "with 229 documented acts of fatal violence against transgender women; Black transgender women accounted for 78.6%" | `halliwell-vaw-2024/halliwell.pdf` | p. 1, Abstract |
| Halliwell: não representativa | "our data are not nationally representative" | `halliwell-vaw-2024/halliwell.pdf` | p. 15, Limitations |

> [!CAUTION]
> Dois números que o estudo **não** usa: (1) a frase do resumo de Luis et al. (2026) "36.452 casos ..., dos quais 563 (42,5%)" sugere denominador errado; o 42,5% é dos 1.325 óbitos pareados (Tabela 1). (2) Halliwell et al. dão 54% de autoria identificada no resumo (p. 1) e 58,3% nos resultados (p. 8); a inconsistência é da fonte, e o número fica fora do texto.
