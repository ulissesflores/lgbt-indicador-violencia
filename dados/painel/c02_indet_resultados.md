# C02 — painel F8 com causa indeterminada (gerado por painel_c02_indet.py; semente 20261021 reprodução, 20261023 desfechos novos)

> [!NOTE]
> Leia o cabeçalho do script: exploratório, NÃO causal; arma de fogo n/d nas colunas novas; viés de completude racial; 27 clusters. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`.

## 0. Reprodução dos números publicados (todas passaram; senão o script aborta)

- b e EP dos 6 desfechos registrados = `resultados_tse_brc.md` (4 casas); n = 351.
- p wild dos 6 registrados (mesma semente/ordem): total 0.943 (pub. 0.943); homens 0.970 (pub. 0.970); mulheres 0.951 (pub. 0.951); negros 0.661 (pub. 0.661); nao_negros 0.911 (pub. 0.911); arma 0.970 (pub. 0.970).
- Contagens SIM agressão X85-Y09 por UF-ano = Atlas em 1755 comparações (total, mulheres, negros, não negros, arma de fogo), 0 divergências; taxas recomputadas = CSV do painel (dif. máxima 0.0e+00).

## 1. Tabela principal: b por 1 ponto de ideologia (escala 0-10; maior = mais à direita), IC95% = b ± 1,96 EP (CR1), p do wild-cluster-t

| grupo | (a) registrado X85-Y09, ln taxa | (b) agressão + indeterminada, ln taxa | (c) razão indet/(agressão+indet), p.p. |
|---|---|---|---|
| total | +0.0009 [-0.0228; +0.0246] p=0.943 | +0.0036 [-0.0190; +0.0263] p=0.768 | +0.145 [-0.574; +0.864] p=0.678 |
| homens | +0.0005 [-0.0240; +0.0251] p=0.970 | +0.0027 [-0.0209; +0.0264] p=0.833 | +0.132 [-0.536; +0.800] p=0.689 |
| mulheres | -0.0007 [-0.0213; +0.0199] p=0.951 | +0.0040 [-0.0122; +0.0203] p=0.639 | +0.142 [-0.909; +1.193] p=0.785 |
| negros | -0.0070 [-0.0356; +0.0215] p=0.661 | -0.0050 [-0.0337; +0.0238] p=0.778 | +0.119 [-0.629; +0.867] p=0.756 |
| não negros | -0.0016 [-0.0352; +0.0320] p=0.911 | +0.0012 [-0.0252; +0.0277] p=0.922 | +0.076 [-0.872; +1.023] p=0.866 |
| arma de fogo | +0.0009 [-0.0353; +0.0371] p=0.970 | n/d | n/d |

Razão média indet/(agressão+indet) por grupo (nível, %): total 13.4%; homens 11.5%; mulheres 27.9%; negros 11.6%; nao_negros 19.2%.

## 2. Limites exatos 100[exp(5b)-1] (troca PT 2,97 -> ~8) do IC95% de (a) e (b)

| grupo | (a) registrado | (b) agressão + indet |
|---|---|---|
| total | [-10.8%; +13.1%] | [-9.1%; +14.0%] |
| homens | [-11.3%; +13.4%] | [-9.9%; +14.1%] |
| mulheres | [-10.1%; +10.5%] | [-5.9%; +10.7%] |
| negros | [-16.3%; +11.3%] | [-15.5%; +12.6%] |
| não negros | [-16.1%; +17.3%] | [-11.9%; +14.8%] |

## 3. Teste de falsificação (c): viés máximo implícito em b registrado

Se a razão r = indet/(agressão+indet) mudasse com a ideologia, o registrado seria (1-r) x total: d ln(registrado) = -(d r)/(1-r). Com b_c em p.p. por ponto e r média do grupo, o IC95% de b_c implica, numa troca de 5 pontos, variação do registrado (só por reclassificação) entre:

| grupo | b razão (p.p./ponto) [IC95%] | p wild | p Holm (4 secundários) | viés implícito em 5 pontos (%) |
|---|---|---|---|---|
| total | +0.145 [-0.574; +0.864] | 0.678 | primário (sem ajuste) | [-4.9%; +3.4%] |
| homens | +0.132 [-0.536; +0.800] | 0.689 | 1.000 | [-4.4%; +3.1%] |
| mulheres | +0.142 [-0.909; +1.193] | 0.785 | 1.000 | [-7.9%; +6.5%] |
| negros | +0.119 [-0.629; +0.867] | 0.756 | 1.000 | [-4.8%; +3.6%] |
| não negros | +0.076 [-0.872; +1.023] | 0.866 | 1.000 | [-6.1%; +5.5%] |

## 4. Holm sobre os 5 grupos de (b)

| grupo | p wild | p Holm |
|---|---|---|
| total | 0.768 | 1.000 |
| homens | 0.833 | 1.000 |
| mulheres | 0.639 | 1.000 |
| negros | 0.778 | 1.000 |
| não negros | 0.922 | 1.000 |

## 5. Completude racial (limite do negros/não negros nas colunas novas)

Raça/cor ignorada no Brasil 2010-2024 (soma): agressão 3.7% dos óbitos; indeterminada 4.1%. Taxas por raça das indeterminadas subestimam e podem variar com a completude por UF-ano.

