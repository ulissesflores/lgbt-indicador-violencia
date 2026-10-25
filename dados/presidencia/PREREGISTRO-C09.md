# PRÉ-REGISTRO C09 — a troca de PRESIDENTE incide sobre a violência letal, como se testou para governador?

Gravado em 2026-10-24 (hora UTC exata e sha256 no arquivo irmão `PREREGISTRO-C09.sha256`, gerado logo após esta gravação e ANTES de qualquer script que leia desfecho). O corpo abaixo não muda depois disso; erro, desvio ou regra nova entra só na seção final **ADENDOS** (datada), nunca por edição do corpo. Pasta: `/Users/ulissesflores/m4/pesquisas/lgbt-indicador-violencia/research-2026-10-24-presidencia/`. Python: `/opt/homebrew/bin/python3.14 -I`. Pedido: `BRIEFING-C09.md` (mesma pasta).

## 0. O que já tinha visto ANTES de gravar (honestidade do "declarado antes")

- Desfechos NACIONAIS já vistos: `dados/sim/asr_brasil.md` seção 1 (taxas padronizadas de agressão de 2012, 2016, 2020, 2022, 2023 e 2024 para os 9 grupos) e as 20 primeiras linhas de `dados/sim/asr_brasil.csv` (Brasil 2010-2019, agressão e agressão+indeterminada). Logo eu já sabia que a série nacional sobe até 2017 e cai a partir de 2018, isto é, ANTES da posse de 2019. O D1 abaixo foi desenhado sabendo disso (por isso a quebra placebo).
- Resultados do painel de governadores já publicados (linha `tx_total` de `dados/painel/resultados_tse_brc.md`: b = +0,0009, EP 0,0121; e de `dados/painel/diagnosticos.md`: p wild 0,943), além do resumo do briefing (efeitos não distinguíveis de zero). Nenhum coeficiente envolvendo o presidente foi estimado.
- Estrutura das exposições, sem nenhum desfecho: `c09_estrutura.md` (gerado por `c09_estrutura.py`, que lê só ideologia, partidos e datas; sha256 do .py `23dbf192...fb8a`, do .md `0a5ed5c7...84e2`, de `presidentes_2007_2024.csv` `b2afc31d...c0e`). Dali: série do presidente por ano; DP residual da interação g x p depois de EF e de g = 4,93 (bruto 19,47); da distância = 1,86; do copartidarismo = 0,31; 94 mudanças de g, 27 delas trocas de onda BRC sem troca de partido, todas em 2021; copartidarismo com 24 UF-anos (Dilma), 22 (Temer), 12 em 3 UFs (Bolsonaro), 8 em 4 UFs (Lula), 16 UFs com variação; MDE do D1 em unidades de DP residual: 4,25 sigma (2016), 5,68 (2019), 5,16 (2023), com 7 gl.
- `research-2026-10-24-astra/ASTRA-B-lacunas.md` NÃO existe no momento da gravação (`B.run.out` com 0 byte); nenhuma sugestão do Astra foi incorporada.

## 1. Pergunta e hipóteses (todas bicaudais, alfa = 0,05)

- **H-D2 (primária).** O efeito da ideologia do governador sobre ln(taxa de homicídio) depende da ideologia do presidente (alinhamento federal-estadual): b2 != 0 no modelo da seção 3. Leitura do sinal: se a violência sobe com a distância quadrática (g - p)^2 = g^2 - 2gp + p^2, o termo gp entra com sinal negativo; **b2 < 0 = UF governada por alguém ideologicamente próximo do presidente tem taxa relativamente menor**; b2 > 0 = o contrário.
- **H-D1 (descritiva).** Há mudança de nível da taxa nacional padronizada por idade em 2016 (Dilma -> Temer), 2019 (Temer -> Bolsonaro) e 2023 (Bolsonaro -> Lula). Sem contrafactual: o D1 não tem veredito causal em nenhum resultado.
- **H-D3 (secundária).** UF governada por partido do presidente (copartidarismo) tem taxa diferente.

## 2. Dados (todos públicos e já em disco; nada é baixado)

- Painel UF x ano: `dados/painel/painel_uf_ano_tse_brc.csv` (351 UF-anos, 27 UFs, 2012-2024; partido de ELEIÇÃO pelo TSE + escore BRC por período; o "principal" do C02/C03). Conferência: `painel_uf_ano_tse.csv` (escore único Bolognesi 2018).
- Numeradores de agressão+indeterminada por UF-ano: `dados/sim/sim_agressoes_agregado.csv`, com a agregação e os denominadores (SIDRA 6407/6403) do `dados/painel/painel_c02_indet.py`, copiados literalmente; contagens de agressão conferidas contra o Atlas (`dados/atlas_uf_series.csv`) como porta de entrada.
- Série nacional: `dados/sim/asr_brasil.csv` (taxa padronizada por idade, padrão Brasil 2022, 9 grupos, agressão e agressão+indeterminada, 2010-2024). Arma de fogo NÃO existe nesse arquivo: será gerada pelo c09 com as funções de `dados/sim/padroniza_idade.py` (importadas, não alteradas), filtrando `grupo == agressao` e `arma == 1`; agressão+indet de arma = n/d (o agregado não marca arma em Y22-Y24, mesmo limite do C02).
- Presidente: `presidentes_2007_2024.csv` (partido de ELEIÇÃO, mesma convenção do painel tse; datas de exercício; 2016 = Dilma até 11/05, Temer desde 12/05, lido em pt.wikipedia.org em 2026-10-24). Escores: BRC por partido-ano (`dados/ideologia/ideologia_partidos_ano.csv`), Bolognesi 2018 único (`dados/ideologia_partidos.csv`), BLS9 do próprio presidente (`fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab`, onda mais próxima do ano). Ano com dois presidentes = média ponderada por dias (2016: 0,361 Dilma, 0,639 Temer). Valores BRC: PT 2,9742 (até 2020) e 2,6786 (2021+); PMDB/MDB 7,0155; PSL 8,1104 (até 2020) e 8,4852 (2021+).

## 3. Especificação PRIMÁRIA única (D2, interação)

ln(tx_total)_it = b1 x g_it + **b2 x (g_it x p_t)** + EF(UF) + EF(ano), no painel `painel_uf_ano_tse_brc.csv` (351 UF-anos), com g = coluna `ideologia` (BRC por período) e p = escore BRC do presidente do ano. O efeito principal do presidente é absorvido pelo EF de ano; só b2 é identificado (centralizar g ou p não muda b2).
Inferência: EP agrupado por UF (CR1, convenção de `dados/painel/painel_diagnosticos.py`, k = posto de [EF, g] + 1); IC95% = b2 ± 1,96 EP (convenção publicada do painel) e, ao lado, IC com t(26); p do bootstrap wild-cluster-t (Rademacher, B = 4999) com H0 b2 = 0 IMPOSTA, isto é, modelo restrito = EF + g (implementado incluindo g na matriz de controles do `wild_p` de `painel_diagnosticos.py`, importado sem alteração). Semente 20261021 SÓ para reproduzir o p 0,943 de `tx_total` (primeiro sorteio, mesma ordem); depois a semente vira **20261024** e os sorteios seguem a ordem desta seção e da seção 4.
Contraste de leitura: governador 5 pontos mais à direita, presidente PT (2,9742) -> PSL (8,1104): K = 5 x 5,1362 = 25,681; efeito % = 100[exp(K b2) - 1] nos dois limites do IC. MDE (80% de poder, alfa 5%, bicaudal) = 2,8 x EP x K, convertido em % do mesmo jeito.

**Regra de decisão (só a primária decide):**

| situação | veredito |
|---|---|
| IC95% de b2 exclui zero E p wild < 0,05 E mesmo sinal no painel de escore único (S4) E razão indet total (S3) com p wild >= 0,05 | "há associação entre alinhamento federal-estadual e a taxa" (sinal e magnitude), NÃO causal |
| idem, mas sinal oposto no escore único (S4) | "inconclusivo: provável artefato das 27 trocas de onda BRC de 2021" |
| idem, mas razão indet total (S3) com p wild < 0,05 | "indeterminado: a classificação da causa varia com o alinhamento; o óbito registrado não sustenta a leitura" |
| IC95% inclui zero OU p wild >= 0,05 | "não distinguível de zero": reportar o IC em % do contraste K e dizer quais efeitos ele EXCLUI; nunca "sem efeito" solto; reportar o MDE |

## 4. Secundárias (descritivas; não mudam o veredito salvo as duas condições acima)

- **S1 distância (D2a):** ln(tx_total) = b1 g + b3 |g - p| + EF(UF) + EF(ano); contraste = 5 pontos de distância; mesmo EP/wild (restrito = EF + g).
- **S2 outros grupos:** modelo primário para tx_homens, tx_mulheres, tx_negros, tx_nao_negros, tx_arma; Holm sobre esses 5 p wild.
- **S3 causa indeterminada (falsificação):** modelo primário com (i) ln taxa de agressão+indeterminada e (ii) razão indet/(agressão+indet) em p.p. (linear), para total, homens, mulheres, negros, não negros (arma n/d). A razão do TOTAL é o teste de falsificação primário (entra na regra acima); os outros 4 da razão e os 5 de (i) levam Holm dentro de cada família.
- **S4 escore único:** modelo primário em `painel_uf_ano_tse.csv`, p = Bolognesi único do partido do presidente (PT 2,97; MDB 7,01; PSL 8,11), tx_total.
- **S5 sem 2016:** modelo primário excluindo 2016 (ano de dois presidentes), tx_total.
- **S6 escala BLS9:** g = escore BLS9 onda 2021 do partido do governador (mesma lógica da robustez do `painel_f8.py`, que dá 341 UF-anos), p = BLS9 do próprio presidente (onda mais próxima); contraste = (DEM - PT, BLS9 2021) x (BOLSONARO 2021 - DILMA 2013); tx_total.
- **S7 copartidarismo (D3):** ln(tx_total) = b1 g + b4 cop + EF(UF) + EF(ano), cop = fração do ano em que o partido de eleição do presidente está entre os partidos do governador (PMDB = MDB); efeito % = 100[exp(b4) - 1]; mesmo EP/wild (restrito = EF + g). Copartidarismo NÃO é coalizão (não há dado de coalizão em disco; declarado). Bolsonaro: só 3 UFs copartidárias.
- **Ordem dos sorteios wild (semente 20261024):** primária; S1; S2 (homens, mulheres, negros, não negros, arma); S3 (i) total, homens, mulheres, negros, não negros; S3 (ii) mesma ordem; S4; S5; S6; S7.

## 5. D1 — série temporal interrompida nacional (descritiva)

Modelo: ln(taxa padronizada)_t = a + b(t - 2010) + soma_k [L_k 1(t >= T_k) + S_k (t - T_k) 1(t >= T_k)], T = 2016, 2019, 2023 (2016 entra no segmento Temer, 64% do ano), 15 pontos 2010-2024, MQO, EP clássico, IC95% com t(7). Estimando: L_k (mudança imediata de nível) em % = 100[exp(L_k) - 1]; MDE_k = 3,261 x sigma-hat x raiz(c_kk) (fatores da `c09_estrutura.md`). Grupos: Brasil (leitura principal do D1), homens negros, homens não negros, mulheres negras, mulheres não negras, arma de fogo (agressão). Mesma série com agressão+indeterminada (5 grupos não arma) e razão indet/(agressão+indet) Brasil em p.p. a partir das contagens brutas do agregado (falsificação: se a razão tem quebra onde a agressão tem, a quebra da agressão pode ser reclassificação).
Placebo pré-fixado: mesmo modelo com quebras em 2015, 2018 e 2022. Regra: uma mudança de nível em 2019 só é descrita como "coincide com a troca" se o IC de 2019 exclui zero E o placebo de 2018 NÃO exclui zero com o mesmo sinal; caso contrário, "não atribuível à troca (a mudança já estava em curso ou é ruído)". Idem 2016/2015 e 2023/2022. Mesmo no melhor caso o D1 não identifica efeito de presidente (choques nacionais simultâneos).
Porta de entrada: recalcular a taxa padronizada Brasil e os 4 grupos sexo x raça com as funções importadas e bater `asr_brasil.csv` (tolerância 0,005, arredondamento de 2 casas); senão aborta.
Autocorrelação: com 7 gl não é estimável de forma útil; declarada como limite (EP clássico provavelmente otimista).

## 6. Poder (declarado antes)

- D2: o EP só existe depois do desfecho; o MDE será 2,8 x EP no contraste K. Com 27 clusters e 3 trocas presidenciais no painel (2016 parcial, 2019, 2023, mais a troca de onda do PSL em 2021), o poder é baixo; espera-se MDE da ordem dos limites do painel de governadores (±10-20%) ou pior. Não interpreto ausência de significância como ausência de efeito.
- D1: MDE de 4,25 / 5,68 / 5,16 DP residuais nas três quebras: só detecta saltos grandes em relação ao ruído anual. Desenho sem poder para efeitos moderados.
- D3: Bolsonaro com 3 UFs copartidárias; b4 é dominado por Dilma/Temer/Lula.

## 7. O que NÃO se poderá concluir, qualquer que seja o resultado

1. Efeito causal do presidente no nível nacional: o D1 confunde a troca com choques simultâneos (queda iniciada em 2018, COVID 2020-21, mudanças de política de armas, dinâmica de facções, degradação do SIM com indeterminadas crescentes desde 2018). O D2 absorve o efeito principal do presidente no EF de ano.
2. Nada sobre violência CONTRA PESSOAS LGBT: o SIM não registra orientação sexual nem identidade de gênero nem motivação; os desfechos são homicídio geral por grupo de sexo e raça.
3. "Sem efeito": nulo = intervalo; só se diz o que o IC exclui.
4. Alinhamento ideológico (escore do partido) não é coalizão, repasse federal nem cooperação policial; copartidarismo é um proxy grosseiro.
5. O escore BRC é do partido, não da pessoa; a BLS9 do presidente (S6) é a única medida pessoal.

## 8. Saídas e testes

Scripts: `c09_d2_painel.py` (D2, S1-S7) e `c09_d1_its.py` (D1); saídas `c09_resultados.md`, `c09_d2_resultados.csv`, `c09_d1_resultados.csv`; `RELATORIO-C09.md` (<= 60 linhas). Testes em `tests/test_c09.py` (pytest com `/opt/homebrew/bin/python3.14 -m pytest`, SEM `-I`, porque o pytest está no site do usuário): re-hash deste arquivo contra o `.sha256`, números travados com a tolerância do arredondamento impresso.

---

**ADENDOS** (datados; vazio na gravação)

**ADENDO 1 — 2026-10-24T20:12:52Z, depois de rodar (só forma; nenhuma regra, desfecho ou especificação mudou).**
- Nomes de saída: além de `c09_d2_resultados.csv` e `c09_d1_resultados.csv`, cada script grava seu .md (`c09_d2_resultados.md`, `c09_d1_resultados.md`); `c09_resultados.md` é montado por `c09_d1_its.py` (cabeçalho + os dois), que também confere o hash do corpo deste arquivo.
- Os floats dos CSV saem com 10 algarismos significativos: na 1a dupla execução o último dígito binário de alguns EP variou (ordem de soma do BLAS); tabelas .md e p wild eram idênticos. Com o arredondamento, duas execuções dão os mesmos sha256 nos 5 arquivos de saída.
