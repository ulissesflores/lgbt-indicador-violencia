# R6 — Pré-registro de FORMA: IC95% por inversão do teste wild-cluster bootstrap-t (painel de governadores)

Data: 2026-10-24. Escrito ANTES de qualquer script que calcule os limites invertidos. O sha256 deste arquivo e a hora UTC vão para `R6-PREREGISTRO-FORMA.sha256`.
O que já era conhecido ao escrever: b, EP (CR1) e p wild publicados dos 6 desfechos (`c02_indet_resultados.csv`, `resultados_tse_brc.md`, `diagnosticos.md`).
O que NÃO era conhecido: os limites do intervalo por inversão e os p da grade.

## Motivo

O escrutínio do Astra (2026-10-24, item 1.14) apontou que os limites publicados ("o desenho exclui só efeitos fora de -10,8% a +13,1%") vêm de b ± 1,96 EP
(normal, CR1), enquanto a referência de inferência do painel é o bootstrap wild-cluster (27 clusters). Este adendo acrescenta o intervalo por inversão desse
teste. Não substitui nada: os números antigos continuam publicados ao lado.

## Dados e modelo (idênticos ao painel principal)

- `dados/painel/painel_uf_ano_tse_brc.csv`, 351 UF-anos (27 UFs x 2012-2024), sem alteração.
- Desfechos: `tx_total`, `tx_homens`, `tx_mulheres`, `tx_negros`, `tx_nao_negros`, `tx_arma` (ln da taxa; linhas com taxa > 0, como no painel).
- ln(taxa) = b x ideologia (0-10) + EF(UF) + EF(ano); funções `dummies`, `residuador`, `ols_fwl` (EP CR1, G = 27) importadas de `painel_diagnosticos.py` sem alterá-lo.
- Conferência obrigatória (aborta se falhar): b e EP de cada desfecho iguais aos de `c02_indet_resultados.csv` (desfecho `registrado_ln`) em 1e-9.

## Procedimento

1. Para um valor hipotético b0: y0 = y - b0 x; resíduo restrito u = M y0 (M = residuador dos EF); t_obs(b0) = (b - b0) / EP.
2. Bootstrap: y* = b0 x + (y0 - u) + u * w, com w = +1 ou -1 por UF (Rademacher), sorteado por UF; reestima b* e EP* (CR1) e t*(b0) = (b* - b0) / EP*.
3. B = 9.999 sorteios por desfecho, os MESMOS pesos para todos os b0 do desfecho (números aleatórios comuns), gerador `numpy.random.default_rng(20261024)`
   independente do RNG de `painel_diagnosticos.py`; a matriz de pesos é sorteada uma vez por desfecho, na ordem total, homens, mulheres, negros, não negros, arma.
4. p(b0) = (1 + #{ |t*| >= |t_obs| }) / (B + 1). IC95% = { b0 : p(b0) > 0,05 }.
5. Limites por bisseção em cada lado (tolerância 1e-7 em b), partindo de b -/+ 1,96 EP e expandindo o lado de fora em passos de 1 EP até p < 0,05.
   Se o conjunto não for um intervalo (p não monótono), reportar a envoltória e marcar a linha.
6. Conversão para o contraste do paper (troca de 5 pontos de ideologia): 100 [exp(5 b) - 1], nos dois limites.
7. Sensibilidade sem bootstrap: b ± t(0,975; 26) EP, com o quantil t calculado numericamente (sem tabela digitada).
8. Conferência de coerência (não aborta): p(0) da grade comparado ao p wild publicado (B = 4.999, outra semente); diferença esperada só de Monte Carlo.

## Regra de leitura (fixada antes)

- Se o intervalo invertido contém 0, o veredito publicado "não distinguível de zero" fica. O paper passa a reportar, para cada desfecho, o intervalo
  normal publicado E o invertido (e o t26 como sensibilidade), sem escolher o mais estreito.
- Nenhum outro desfecho, especificação ou variante entra neste adendo.

## Saídas

`dados/painel/painel_r6_ic_wild_invertido.py`, `dados/painel/r6_ic_wild_invertido.csv`, `dados/painel/r6_ic_wild_invertido.md`.
