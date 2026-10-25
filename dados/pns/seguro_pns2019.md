# Violência segundo a orientação sexual, PNS 2019 (gerado por seguro_pns2019.py)

Desenho complexo (574 estratos, 8.027 UPA, peso calibrado). IC95% entre colchetes. LEIA os limites no cabeçalho do script: uma onda, autorrelato, sem motivo do agressor, sem homicídio. ICs de Wald linear (os do artigo de Vasconcelos usam transformação logit: os pontos coincidem, os limites diferem pouco, mais perto de 0/100%). Com n de LGB+ de 88 a 916 por subgrupo, as diferenças ENTRE subgrupos (regiões, idades) têm ICs sobrepostos: NÃO sustentam ranking de regiões nem de faixas.

## 0. Reprodução do artigo publicado (Vasconcelos et al. 2023, Tabela 2; tolerância 0,05 p.p.)

| desfecho | grupo | publicado | recalculado | confere |
|---|---|---|---|---|
| fisica | lgb | 14.70% | 14.70% | sim |
| fisica | het | 3.82% | 3.82% | sim |
| qualquer | lgb | 41.63% | 41.63% | sim |
| qualquer | het | 17.61% | 17.61% | sim |
| sexual | lgb | 4.86% | 4.86% | sim |
| sexual | het | 0.68% | 0.68% | sim |

Divergências: 0.

## 1. Prevalência em 12 meses, por orientação sexual (adultos 18+)

| desfecho | heterossexual | LGB+ | homossexual | bissexual | RP LGB+/het [IC] | diferença LGB+ - het (p.p.) |
|---|---|---|---|---|---|---|
| física | 3.82% [3.57; 4.08] | 14.70% [10.72; 18.67] | 12.85% [8.33; 17.38] | 18.27% [10.59; 25.96] | 3.84 [2.92; 5.06] | +10.9 [+6.9; +14.8] |
| sexual | 0.68% [0.55; 0.80] | 4.86% [2.87; 6.84] | 2.85% [0.85; 4.85] | 8.58% [4.29; 12.88] | 7.17 [4.57; 11.26] | +4.2 [+2.2; +6.2] |
| psicológica | 16.73% [16.20; 17.26] | 40.03% [35.48; 44.58] | 35.24% [29.89; 40.58] | 48.66% [40.49; 56.82] | 2.39 [2.12; 2.69] | +23.3 [+18.7; +27.9] |
| qualquer | 17.61% [17.08; 18.15] | 41.63% [37.06; 46.20] | 37.21% [31.77; 42.64] | 49.78% [41.67; 57.89] | 2.36 [2.11; 2.65] | +24.0 [+19.4; +28.6] |

Escala (peso calibrado à população): LGB+ ≈ 3.01 milhões de adultos; vítimas de violência física em 12 meses entre LGB+ ≈ 442 mil (IC95% ≈ ±132 mil).

## 2. Violência FÍSICA (12 meses): LGB+ x heterossexual por subgrupo (RP e diferença; n LGB+ no subgrupo)

| subgrupo | n LGB+ | het | LGB+ | RP [IC95%] | diferença p.p. |
|---|---|---|---|---|---|
| Homens | 796 | 3.71% [3.38; 4.04] | 13.45% [7.95; 18.95] | 3.62 [2.39; 5.50] | +9.7 |
| Mulheres | 758 | 3.92% [3.53; 4.32] | 15.84% [10.20; 21.47] | 4.04 [2.81; 5.80] | +11.9 |
| Negros (pretos+pardos) | 916 | 4.58% [4.24; 4.92] | 18.48% [12.26; 24.70] | 4.03 [2.87; 5.67] | +13.9 |
| Não negros | 637 | 2.90% [2.56; 3.23] | 9.81% [6.05; 13.57] | 3.39 [2.27; 5.05] | +6.9 |
| Idade 18-29 | 697 | 6.66% [5.97; 7.35] | 19.54% [13.19; 25.90] | 2.93 [2.08; 4.13] | +12.9 |
| Idade 30-44 | 506 | 4.28% [3.81; 4.74] | 9.69% [4.94; 14.44] | 2.27 [1.37; 3.76] | +5.4 |
| Idade 45-59 | 263 | 3.02% [2.61; 3.43] | 4.87% [1.42; 8.32] | 1.61 [0.79; 3.31] | +1.9 |
| Idade 60+ | 88 | 1.49% [1.23; 1.75] | 8.63% [0.00; 17.96] | 5.80 [1.93; 17.36] | +7.1 |
| Instrução baixa | 188 | 3.63% [3.24; 4.02] | 26.04% [13.68; 38.40] | 7.18 [4.42; 11.64] | +22.4 |
| Instrução média | 669 | 4.41% [4.02; 4.79] | 18.13% [11.43; 24.83] | 4.11 [2.84; 5.96] | +13.7 |
| Instrução alta | 697 | 2.93% [2.40; 3.47] | 7.58% [4.46; 10.70] | 2.58 [1.64; 4.06] | +4.6 |
| Região Norte | 256 | 4.17% [3.67; 4.68] | 15.18% [6.76; 23.61] | 3.64 [2.06; 6.41] | +11.0 |
| Região Nordeste | 458 | 4.25% [3.84; 4.66] | 14.27% [8.15; 20.39] | 3.36 [2.17; 5.21] | +10.0 |
| Região Sudeste | 403 | 3.55% [3.07; 4.04] | 16.87% [9.54; 24.20] | 4.75 [3.04; 7.42] | +13.3 |
| Região Sul | 232 | 3.65% [3.11; 4.19] | 11.66% [5.84; 17.48] | 3.19 [1.89; 5.40] | +8.0 |
| Região Centro-Oeste | 205 | 3.89% [3.27; 4.50] | 7.13% [3.21; 11.05] | 1.83 [1.04; 3.24] | +3.2 |
| Urbano | 1427 | 3.96% [3.67; 4.25] | 14.07% [9.99; 18.15] | 3.55 [2.64; 4.77] | +10.1 |
| Rural | 127 | 2.97% [2.57; 3.37] | 23.86% [7.20; 40.51] | 8.02 [4.01; 16.05] | +20.9 |

## 3. Razão de prevalências AJUSTADA (Poisson ponderado, variância robusta de desenho): LGB+ x heterossexual

Ajuste: sexo, faixa etária, cor, instrução, região, urbano/rural. Amostra: LGB+ e heterossexuais.

| desfecho | RP bruta | RP ajustada [IC95%] |
|---|---|---|
| física | 3.84 | 2.82 [2.16; 3.68] |
| sexual | 7.17 | 5.00 [3.17; 7.89] |
| psicológica | 2.39 | 1.87 [1.66; 2.11] |
| qualquer | 2.36 | 1.84 [1.64; 2.07] |

## 4. Entre as VÍTIMAS de violência física em 12 meses: quem agrediu e onde (episódio mais grave; V018/V019)

| categoria | heterossexuais | LGB+ |
|---|---|---|
| **QUEM (V018)** | n het = 3112 | n LGB+ = 179 |
| Cônjuge/companheiro(a) | 20.21% [16.29; 24.12] | 5.05% [1.25; 8.85] |
| Ex-cônjuge/ex-companheiro(a) | 12.63% [10.65; 14.61] | 16.17% [2.63; 29.72] |
| Parceiro(a)/namorado(a)/ex | 4.26% [3.27; 5.26] | 11.70% [3.95; 19.45] |
| Pai/mãe/padrasto/madrasta | 3.70% [2.38; 5.02] | 13.01% [3.73; 22.28] |
| Filho(a)/enteado(a) | 2.81% [2.00; 3.63] | 0.00% [0.00; 0.00] |
| Irmão(ã) | 4.71% [3.57; 5.85] | 15.90% [0.23; 31.56] |
| Outro parente | 8.02% [6.28; 9.77] | 2.27% [0.00; 5.12] |
| Amigo(a)/colega/vizinho(a) | 15.15% [12.77; 17.54] | 12.60% [4.25; 20.96] |
| Empregado(a) | 0.38% [0.13; 0.62] | 0.61% [0.00; 1.57] |
| Patrão/chefe | 0.73% [0.27; 1.18] | 4.13% [0.00; 10.63] |
| Pessoa desconhecida | 23.02% [20.28; 25.77] | 16.29% [8.06; 24.52] |
| Policial | 2.19% [1.32; 3.07] | 0.61% [0.00; 1.26] |
| Outro | 2.18% [1.24; 3.12] | 1.67% [0.00; 3.33] |
| **ONDE (V019)** | n het = 3112 | n LGB+ = 179 |
| Domicílio | 55.19% [51.79; 58.59] | 44.11% [29.05; 59.18] |
| Trabalho | 6.52% [5.11; 7.92] | 8.92% [1.03; 16.81] |
| Escola/faculdade | 1.42% [0.73; 2.11] | 2.10% [0.13; 4.07] |
| Bar/restaurante | 4.92% [3.72; 6.12] | 9.47% [1.89; 17.05] |
| Via pública/local público | 29.05% [26.08; 32.02] | 34.22% [19.68; 48.77] |
| Outro | 2.90% [1.77; 4.04] | 1.18% [0.00; 2.70] |

- Agressor = parceiro ou ex (cônjuge, ex, namorado): heterossexuais 37.10% [33.23; 40.97]; LGB+ 32.92% [18.42; 47.43]; RP 0.89 [0.57; 1.39]
- Agressor = família (pai/mãe/filho/irmão/outro parente): heterossexuais 19.25% [16.79; 21.70]; LGB+ 31.17% [15.38; 46.96]; RP 1.62 [0.96; 2.72]

Leitura: a PNS NÃO pergunta o motivo do agressor. 'Por quê' só pode ser lido como associação (quem agride, onde, perfil), nunca como motivação por orientação (N4 do dossiê).

