# C09 — estrutura do desenho (gerado por c09_estrutura.py; só exposições, nenhum desfecho lido)

## Presidente por ano (ponderado por dias de exercício)

| ano | composição | BRC por período | Bolognesi 2018 (único) | BLS9 do próprio presidente |
|---|---|---|---|---|
| 2010 | Luiz (PT) 1.000 | 2.9742 | 2.9700 | -0.4198 |
| 2011 | Dilma (PT) 1.000 | 2.9742 | 2.9700 | -0.4207 |
| 2012 | Dilma (PT) 1.000 | 2.9742 | 2.9700 | -0.4207 |
| 2013 | Dilma (PT) 1.000 | 2.9742 | 2.9700 | -0.4207 |
| 2014 | Dilma (PT) 1.000 | 2.9742 | 2.9700 | -0.4207 |
| 2015 | Dilma (PT) 1.000 | 2.9742 | 2.9700 | -0.4207 |
| 2016 | Dilma (PT) 0.361; Michel (PMDB) 0.639 | 5.5580 | 5.5530 | +0.1659 |
| 2017 | Michel (PMDB) 1.000 | 7.0155 | 7.0100 | +0.5448 |
| 2018 | Michel (PMDB) 1.000 | 7.0155 | 7.0100 | +0.5448 |
| 2019 | Jair (PSL) 1.000 | 8.1104 | 8.1100 | +0.8620 |
| 2020 | Jair (PSL) 1.000 | 8.1104 | 8.1100 | +0.8620 |
| 2021 | Jair (PSL) 1.000 | 8.4852 | 8.1100 | +0.8620 |
| 2022 | Jair (PSL) 1.000 | 8.4852 | 8.1100 | +0.8620 |
| 2023 | Luiz (PT) 1.000 | 2.6786 | 2.9700 | -0.4989 |
| 2024 | Luiz (PT) 1.000 | 2.6786 | 2.9700 | -0.4989 |

## D2 — variação disponível das exposições depois dos EF (UF e ano) e do controle g

| exposição | DP bruto | DP residual (EF UF+ano) | DP residual (EF + g) |
|---|---|---|---|
| g | 2.0653 | 1.2593 | — |
| gp | 19.4706 | 8.4619 | 4.9280 |
| dist | 2.0298 | 1.8556 | 1.8555 |
| cop | 0.3665 | 0.3206 | 0.3128 |

Mudanças de g (governador) 2013-2024: 94, das quais 27 com os MESMOS partidos (troca de onda BRC, ano: [2021]).
Trocas de presidente no painel 2012-2024: 2016 (parcial), 2019, 2023; mudança do escore BRC do presidente também em 2021 (onda 2022 do PSL: 8.1104 -> 8.4852).

## D3 — copartidarismo governador-presidente (partido de eleição; PMDB = MDB)

| presidente | UF-anos com cop > 0 | soma de cop (UF-anos equivalentes) | UFs distintas |
|---|---|---|---|
| Dilma 2012-2016 | 24 | 25.28 | 8 |
| Temer 2016-2018 | 22 | 21.28 | 8 |
| Bolsonaro 2019-2022 | 12 | 12.00 | 3 |
| Lula 2023-2024 | 8 | 8.00 | 4 |

UFs com variação de cop no tempo: 16 de 27.

## D1 — efeito mínimo detectável (MDE) do nível em cada quebra, em unidades de DP residual sigma (só a matriz X; 15 pontos 2010-2024)

| modelo | quebras | gl residual | fator t(0,975)+t(0,80) | MDE da mudança de nível / sigma, por quebra |
|---|---|---|---|---|
| primário (nível + inclinação) | (2016, 2019, 2023) | 7 | 3.261 | 2016: 4.25; 2019: 5.68; 2023: 5.16 |
| placebo 1 ano antes | (2015, 2018, 2022) | 7 | 3.261 | 2015: 4.53; 2018: 5.68; 2022: 4.98 |
