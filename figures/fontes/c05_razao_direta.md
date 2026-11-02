# C05 — PNS 2019: P(LGB+ | violência física 12 m, 18+) estimada DIRETAMENTE no microdado (gerado por pns_c05_razao_direta.py)

> [!NOTE]
> Leia o cabeçalho do script (limites). Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. Taylor de último conglomerado + jackknife JKn por UPA; 574 estratos, 8.027 UPA.

## 0. Reprodução (passou; senão o script aborta)

- Prevalências do artigo (14,70 / 3,82 / 41,63 / 17,61 / 4,86 / 0,68) dentro de 0,05 p.p.; RP bruta 3.84 [2.92; 5.06] (publicado 3,84 [2,92; 5,06]); vítimas LGB+ ≈ 442 mil (publicado ≈ 442 mil).
- Pontos do Monte Carlo recalculados dos insumos publicados: cenário B 6.90% (publicado 6,90%), cenário A 7.13% (publicado 7,13%).

## 1. Resultado: parcela LGB+ entre as vítimas de violência física (12 meses), adultos 18+

| base | corte | n vítimas | n LGB+ | R (%) | EP Taylor | EP jackknife | IC95% de desenho (Taylor) | IC95% logit | IC95% (EP jackknife) |
|---|---|---|---|---|---|---|---|---|---|
| (a) todos os adultos vítimas | total | 3440 | 179 | 6.70 | 0.97 | 0.97 | [4.80; 8.60] | [5.03; 8.87] | [4.79; 8.61] |
| (a) todos os adultos vítimas | 18-29 | 1123 | 106 | 12.54 | 2.20 | 2.21 | [8.23; 16.84] | [8.83; 17.51] | [8.20; 16.88] |
| (a) todos os adultos vítimas | 30-44 | 1229 | 52 | 3.73 | 0.97 | 0.98 | [1.83; 5.64] | [2.23; 6.18] | [1.82; 5.64] |
| (a) todos os adultos vítimas | 45+ | 1088 | 21 | 1.46 | 0.45 | 0.45 | [0.57; 2.35] | [0.79; 2.67] | [0.57; 2.35] |
| (a) todos os adultos vítimas | homens | 1572 | 81 | 6.40 | 1.41 | 1.42 | [3.64; 9.16] | [4.14; 9.78] | [3.63; 9.18] |
| (a) todos os adultos vítimas | mulheres | 1868 | 98 | 6.95 | 1.34 | 1.35 | [4.33; 9.58] | [4.74; 10.08] | [4.30; 9.60] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | total | 3291 | 179 | 7.12 | 1.03 | 1.03 | [5.11; 9.13] | [5.36; 9.41] | [5.10; 9.14] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | 18-29 | 1047 | 106 | 13.82 | 2.39 | 2.41 | [9.15; 18.50] | [9.77; 19.20] | [9.10; 18.55] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | 30-44 | 1194 | 52 | 3.85 | 1.00 | 1.01 | [1.89; 5.82] | [2.30; 6.37] | [1.88; 5.82] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | 45+ | 1050 | 21 | 1.52 | 0.47 | 0.47 | [0.59; 2.45] | [0.83; 2.79] | [0.59; 2.45] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | homens | 1505 | 81 | 6.87 | 1.50 | 1.51 | [3.92; 9.81] | [4.45; 10.46] | [3.90; 9.83] |
| (b) só hetero ou LGB+ (comparável ao Sinan) | mulheres | 1786 | 98 | 7.34 | 1.41 | 1.42 | [4.58; 10.09] | [5.01; 10.61] | [4.55; 10.12] |

## 2. Comparação com o Monte Carlo e com o Sinan (teste primário: base (b), total)

- Direto, base (b), total: **7.12%**, IC95% de desenho [5.11; 9.13] (largura 4.02 p.p.); Monte Carlo cenário A: 7,13% [5,43; 9,32] (largura 3.89); razão de larguras direto/MC = 1.03.
- Base (a), total: 6.70% [4.80; 8.60] (Monte Carlo cenário B: 6,90% [5,25; 9,03]; as duas NÃO são o mesmo estimando: ver limite 1).
- Sinan 2023 = 4,12% está FORA do IC de desenho (b, total); Sinan 2024 = 4,08% está FORA. Com IC logit [5.36; 9.41]: 4,12% fora, 4,08% fora; com EP jackknife [5.10; 9.14]: 4,12% fora, 4,08% fora.
- Razão entre EP Taylor e EP jackknife (maior/menor, base (b) total): 1.00.
- Distância do Sinan ao ponto: 1.74x (ponto da PNS / 4,10); em EPs: 2.93 (2023) e 2.97 (2024).

