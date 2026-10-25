# PRÉ-REGISTRO C10 — EXPOSIÇÃO POR GOVERNO: o que aconteceu com a taxa de homicídio quando o governo mudou (federal e estadual), sem atribuir causa

Gravado em 2026-10-24 (hora UTC exata e sha256 no arquivo irmão `PREREGISTRO-C10.sha256`, gerado logo após esta gravação e ANTES de qualquer script que leia desfecho). O corpo abaixo não muda depois disso; erro, desvio ou regra nova entra só na seção final **ADENDOS** (datada), nunca por edição do corpo. Pasta: `/Users/ulissesflores/m4/pesquisas/lgbt-indicador-violencia/research-2026-10-24-exposicao/`. Python: `/opt/homebrew/bin/python3.14 -I`. Pedido: frente E de `research-2026-10-24-v03/V03-BRIEFING.md` e pedido 4 de `MEGA-PROJETO-V1.md` ("se um governo mudou, e aumentou ou abaixou é isso que estamos medindo; decidir se é por conta dele não fazemos, apenas estamos expondo").

## 0. O que já tinha visto ANTES de gravar (honestidade do "declarado antes")

- **Todo o `research-2026-10-24-presidencia/RELATORIO-C09.md`**, inclusive: a série nacional padronizada sobe até 2017 e cai a partir de 2018 (com Temer); D1 2019 −17,0% [−29,5; −2,4] com placebo 2018 −21,8%; 2016 +2,6%; 2023 −3,9%; mulheres negras 2019 −19,7%; razão nacional de indeterminadas 13,3% (2017), 18,0% (2018), 27,4% (2019), 30,1% (2024); agressão + indeterminada atenua a queda de 2019 (−9,6% contra −17,0%). Logo **já sei o sinal provável do E1 para Temer (base 2015 -> fim 2018) e Bolsonaro (base 2018 -> fim 2022): queda**. O E1 é descritivo e não tem veredito; isso não muda nenhuma regra abaixo, mas fica declarado.
- `dados/sim/asr_brasil.csv`: cabeçalho e as 2 primeiras linhas (Brasil 2010: agressão 25,93; agressão + indeterminada 31,72); contagem de linhas por grupo e desfecho (9 grupos x 15 anos x 2 desfechos).
- `dados/painel/painel_uf_ano_tse_brc.csv`: cabeçalho e a 1ª linha (Acre 2012, tx_total 26,80 e demais tx_*). Nenhuma outra taxa por UF foi lida.
- `research-2026-10-24-presidencia/c09_d1_resultados.md`: início da linha `Brasil | arma` (2010-2017: 17,81; 17,84; 19,44; 19,62; 20,80; 20,44; 21,76; 23,...).
- `dados/painel/resultados_tse_brc.md`/`diagnosticos.md` só pelo que o RELATORIO-C09 cita (painel de governadores sem efeito distinguível de zero).
- Estrutura das exposições, SEM desfecho: `c10_estrutura.py` -> `c10_estrutura.md` e `c10_trocas.csv` (lê só uf, ano, ideologia, partido e as datas dos presidentes). Dali: 67 trocas reais (partido muda E escore BRC muda; regra do C03) + 27 trocas de onda (não são trocas); por ano da troca: 2013: 1, 2014: 6, 2015: 16, 2017: 1, 2018: 8, 2019: 18, 2022: 4, 2023: 12, 2024: 1; 47 com janela completa 3+3, 39 "contaminadas" (outra troca real da mesma UF em e−2..e+2), 21 completas e não contaminadas; 19 trocas em que o ano e tem mais de um partido no ano (transição no meio do ano; partido com `|`: 2013: 1, 2014: 5, 2017: 1, 2018: 7, 2022: 4, 2023: 1); 45 trocas de posse eleitoral (e em 2015, 2019 ou 2023, partido único no ano e); direção por bloco: esquerda->direita 12, direita->esquerda 8, envolve centro 8, mesmo bloco 39; sinal do escore: 38 para a direita, 29 para a esquerda; UFs de referência sem troca em e−2..e+2: 10 (2013-2015), 3 (2017), 9 (2018-2019), 15 (2022-2024).
- `ASTRA-B-lacunas.md` não foi lido para esta frente.

## 1. Pergunta e enquadramento

Pergunta: **quando o governo mudou, a taxa de homicídio subiu ou caiu, e quanto?** É EXPOSIÇÃO DESCRITIVA. Nenhum número deste estudo é efeito causal do governo, e nenhuma frase do relatório atribui a variação ao governante: a taxa muda por COVID, política de armas, dinâmica de facções, demografia, degradação do registro (indeterminadas crescentes desde 2018) e acaso, que coincidem com as trocas. A atribuição é impossível com este desenho e não será feita. Nada aqui é sobre violência CONTRA PESSOAS LGBT: o SIM não registra orientação sexual, identidade de gênero nem motivação.

## 2. Dados (todos públicos e já em disco; nada é baixado)

- E1: `dados/sim/asr_brasil.csv` (taxa padronizada por idade, padrão Brasil 2022, por 100 mil, IC95% Poisson; 2010-2024). Arma de fogo (agressão com `arma == 1`) gerada com as funções de `dados/sim/padroniza_idade.py` importadas sem alteração, exatamente como `research-2026-10-24-presidencia/c09_d1_its.py`. Razão indeterminada/(agressão + indeterminada), Brasil, das contagens brutas de `dados/sim/sim_agressoes_agregado.csv` (contexto).
- E2: `dados/painel/painel_uf_ano_tse_brc.csv` (351 UF-anos, 2012-2024; partido de eleição TSE + escore BRC por período; o painel principal do C02/C03/C09). Comparador nacional = soma dos óbitos das 27 UFs / soma da população das 27 UFs, com os MESMOS insumos do painel: contagens `dados/atlas_uf_series.csv` (SIM/TabNet) e população SIDRA 6407/6403 (cópia literal da leitura de `c09_d2_painel.py`). Agressão + indeterminada por UF: contagens de `sim_agressoes_agregado.csv` com a agregação copiada de `c09_d2_painel.py`.
- Presidentes: `research-2026-10-24-presidencia/presidentes_2007_2024.csv` (datas de exercício). Blocos ideológicos: cortes do próprio artigo BRC, `fontes/p2-f8-governos/bolognesi.txt` linhas 601-607 (sha256 `6a8d0d37...9bd02`): 0-1,5 extrema-esquerda; 1,51-3 esquerda; 3,01-4,49 centro-esquerda; 4,5-5,5 centro; 5,51-7 centro-direita; 7,01-8,5 direita; 8,51-10 extrema-direita. Agrupados em 3 blocos: **esquerda < 4,5; centro 4,5 a 5,5; direita > 5,5** (escore do painel, 2 casas).

## 3. E1 — FEDERAL (descritivo)

Governos = linhas de `presidentes_2007_2024.csv` (Dilma 2011 a 11/05/2016 é um governo contínuo; não é partida em Dilma 1/Dilma 2). Regra única:
- **ano-base** = último ano civil inteiro ANTES do 1º dia do governo; **ano-fim** = último ano civil inteiro DENTRO do governo; governo em curso (Lula 2023-) termina no último dado, 2024 (marcado "em curso, 2 de 4 anos; denominador 2023-24 extrapolado").
- Resultado: Lula 2007-10 base 2006 -> **n/d** (o SIM em disco começa em 2010; só o nível de 2010 é mostrado); Dilma 2010 -> 2015; Temer 2015 -> 2018 (2016, ano dividido, fica dentro do intervalo de Temer e no fim do de Dilma: nenhum dos dois o tem como ponta); Bolsonaro 2018 -> 2022; Lula 2022 -> 2024.
- Para cada governo e série: taxa no ano-base, taxa no ano-fim, **variação em %** = 100(fim/base − 1), **variação em pontos** (por 100 mil) = fim − base, variação anual média = 100[(fim/base)^(1/(fim−base)) − 1] (governos têm durações diferentes). Incerteza: IC95% da variação % só de CONTAGEM (Poisson), exp(ln(fim/base) ± 1,96·raiz(v_base + v_fim)), v = ((taxa − ic_lo)/1,96/taxa)²; rotulado "incerteza de contagem, não de causa nem de tendência".
- **Contexto pré (nunca contrafactual):** variação % de (base−3) a base e anual média. Dilma (2007 -> 2010) e Lula 2007-10 -> **n/d** (sem dado antes de 2010).
- Séries: agressão — Brasil, mulheres negras, mulheres não negras, homens negros, homens não negros, arma de fogo; agressão + indeterminada — os mesmos 5 grupos sem arma (arma + indeterminada = n/d: o agregado não marca arma em Y22-Y24). Contexto: razão de indeterminadas (%) no ano-base e no ano-fim, Brasil.
- Porta (aborta): taxas recalculadas com `padroniza_idade` = `asr_brasil.csv` (tolerância 0,005) para os 5 grupos e 2 desfechos; série de arma = a de `c09_d1_resultados.md` (2 casas).

## 4. E2 — ESTADUAL (descritivo, com referência de acaso)

**Eventos:** as 67 trocas reais de `c10_trocas.csv` (UF u, ano e = 1º ano com o partido novo). Regra única de janela: **antes = anos e−3, e−2, e−1; depois = anos e, e+1, e+2**, cada um restrito a 2012-2024; exige ≥ 1 ano de cada lado (todas as 67 cumprem); colunas n_antes e n_depois registram a truncagem. Nas 19 trocas com transição no meio do ano o ano e é misto e entra no "depois" (mesma regra para todas).
**Estatística por troca e grupo:** excesso relativo **r = 100·[ (D_uf/A_uf) / (D_br/A_br) − 1 ]**, em %, onde A e D são as MÉDIAS simples das taxas brutas por 100 mil nos anos de "antes" e "depois", e o Brasil usa exatamente os mesmos anos. Também em pontos: (D_uf − A_uf) − (D_br − A_br). "Subiu" = r > 0; "caiu" = r < 0.
**Grupos:** os 6 do painel: total (leitura principal), homens, mulheres, negros, não negros, arma de fogo (não há sexo x raça cruzado por UF; declarado). Sensibilidade do registro: total em agressão + indeterminada.
**Recortes (todos exibidos, nenhum filtrado):** (P) todas as 67 [principal]; (a) janela completa 3+3 (47); (b) completa e não contaminada (21); (c) só posse eleitoral: e ∈ {2015, 2019, 2023} e partido do ano e sem `|`. Direção por duas classificações: sinal do Δ escore (para a direita 38 / para a esquerda 29; convenção do C03) e bloco (esquerda->direita, direita->esquerda, envolve centro, mesmo bloco).
**Resumo por recorte x direção x grupo:** n, quantas subiram, quantas caíram, mediana de r, quartis (p25, p75), mínimo e máximo.
**Referência de acaso (pré-especificada):** referências do ano e = UFs SEM troca real em e−2..e+2 (antes e depois com o mesmo governo), r calculado com a MESMA janela truncada do evento. Reamostragem pareada por ano: em cada sorteio, para cada troca do recorte, sorteia-se 1 referência do mesmo ano e (com reposição; uniforme), e calcula-se a mediana de r e a fração que subiu. **B = 9999, semente 20261024**, um gerador `numpy.random.default_rng` por célula reiniciado com a mesma semente (célula = recorte x direção x grupo; reprodutível e independente da ordem). Reporta-se, para mediana e fração: o intervalo central de 95% da referência e o p bicaudal = min(1, 2·min(P(ref ≤ obs), P(ref ≥ obs))) com a correção (contagem + 1)/(B + 1). Leitura: "as trocas se parecem / não se parecem com UFs sem troca no mesmo ano". **Não é teste de efeito do governo.** Multiplicidade: todas as células são reportadas; leitura principal = total, recorte P, todas as direções; demais células: Holm dentro de cada família (recorte x direção, 6 grupos) é mostrado ao lado; declara-se o número de células e os falsos positivos esperados a 5%.
**Porta (aborta):** taxas por UF-ano recalculadas de contagens + população = colunas tx_* do painel (diferença < 1e-9); soma das 27 UFs = numerador e denominador nacionais (por construção) e contagens de agressão do SIM = Atlas por UF-ano.

## 5. O que se PODE e o que NÃO se pode dizer

- Pode: "na troca X (UF, ano), a taxa do estado, relativa ao Brasil, subiu/caiu Y% entre os 3 anos antes e os 3 depois; isso não é prova de causa". "No governo Z, a taxa nacional padronizada foi de A (ano-base) a B (ano-fim), variação de C%; ela já vinha subindo/caindo D% nos 3 anos antes".
- Não pode: "o governo/governador X reduziu/aumentou a violência"; "a direita/esquerda reduz homicídios"; qualquer frase sobre violência contra pessoas LGBT; "sem efeito" (nulo descritivo não é ausência de efeito).

## 6. Saídas e testes

Script `c10_exposicao.py` (E1 e E2). Saídas em formato longo prontas para figura: `c10_e1_federal.csv` (governo x série), `c10_e1_serie_longo.csv` (ano x série, com o governo de cada ano), `c10_e2_trocas_longo.csv` (troca x grupo), `c10_e2_resumo.csv` (recorte x direção x grupo, com a referência); `c10_resultados.md`; `RELATORIO-EXPOSICAO.md` (<= 60 linhas). Testes em `tests/test_c10.py` (pytest com `/opt/homebrew/bin/python3.14 -m pytest`, SEM `-I`): re-hash do corpo deste arquivo, 67/27/47/21, soma das 27 UFs = Brasil, números citados no relatório travados com a tolerância do arredondamento impresso.

## 7. Becos já conhecidos (declarados antes)

Lula 2007-10 não computável (SIM em disco desde 2010); tendência pré de Dilma n/d; arma + indeterminada n/d; 2017 tem só 3 UFs de referência; 2023-24 com no máximo 2 anos de "depois" e denominador extrapolado; trocas sobrepostas da mesma UF (2018 e 2019) não são independentes e a reamostragem não reproduz essa dependência (o recorte (b) a remove).

---

**ADENDOS** (datados; vazio na gravação)

**ADENDO 1 — 2026-10-24T20:46:49Z, depois de rodar (só forma e uma observação PÓS-HOC; nenhuma regra, desfecho, janela, recorte, semente ou B mudou).**
- Forma: `c10_e2_trocas_longo.csv` ganhou a coluna `ref_excesso_pct` (o r de cada UF de referência na mesma janela, para auditoria); Holm (família recorte x direção, 6 grupos) sai só no CSV (`p_*_holm6`), não na tabela do .md. Duas execuções dão os mesmos sha256 nos 5 arquivos de saída.
- Observação PÓS-HOC (não muda nada do corpo; vai rotulada no relatório): o grupo de referência é pequeno e não é neutro. São 21 UFs distintas no total e, em 2018-2019, 9 UFs, 7 delas do Nordeste (AL, BA, CE, MA, PB, PE, PI) mais AP e MS; em 2017, 3 (BA, PB, PE). O p da reamostragem só mede a variação de sortear dentro desse grupo fixo: não incorpora a incerteza do próprio grupo e é anticonservador. Uma diferença entre trocas e referência pode refletir região e não a troca: em 2019, a mediana do r nas 9 UFs de referência foi +8,4% (Piauí +37%, Amapá +27%, Bahia +24%; coluna `ref_excesso_pct`).
