# Séries públicas de mortes LGBT+ no Brasil: concordância entre fontes (2026-10-22)

Pasta: `research-2026-10-21-rodada3/GGB-completo/series/`. Só material público, nada pedido a ninguém. Painel: `painel_mortes_lgbt.csv` (306 linhas; cada linha com trecho verbatim validado por busca no PDF, página, caminho absoluto, sha256). Scripts com semente 20261022 em `scripts/`. Tabelas: `dados_analises/`.

> [!IMPORTANT]
> Nenhum teste abaixo prova fraude nem prova confiabilidade. As séries são contagens declaradas de ONG a partir de notícias. O IC mede só a instabilidade entre poucos anos (n de 3 a 24), não erro de medida, e as séries são autocorrelacionadas.

## 0. Resposta em 9 linhas

1. **Independência é o achado central.** A série trans da ANTRA 2008-2016 é a do GGB (ANTRA 2017: "o Grupo Gay da Bahia - o único que contabilizava até então os crimes - noticiou 58 assassinatos... 144 em 2016"). O TMM/TDoR Brasil cita GGB/Homofobia Mata em 72-94% dos registros de 2013 a 2018 e em ~0% desde 2019. O Observatório (Acontece/ANTRA/ABGLT) usa o gráfico do GGB até 2020 e "base compartilhada". Só há comparação limpa a partir de 2019-2020.
2. GGB trans x ANTRA (variações anuais, n=6): Pearson 0,97 (IC95 bootstrap 0,64-1,00); sinal igual 6/6. É concordância de **direção** entre duas listas de mídia, não validação de nível.
3. A razão GGB trans / ANTRA cai de 1,07 (2017) para 0,80 (2025) (rho -0,83, p=0,01): a cobertura relativa do recorte trans pelo GGB encolhe, coerente com a fatia trans do GGB ir de 43% (2017) para 25% (2025).
4. GGB total x SIM (agressão): variações anuais com r=0,20 (IC -0,37 a 0,60; n=24), sinal igual 13/24 (54%, IC 33-74%): **não** acompanha o SIM ano a ano. Em nível, GGB/SIM sobe de 2,9 para 7,0 por mil mortes (2000-2017) e fica em 5-7,5 depois.
5. De 2017 a 2024 todas caem juntas: GGB -34,6%, SIM -37,3%, ANTRA -31,8%, TMM -37,6%, TDoR -49,2%. De 2000 a 2017 o GGB sobe 242% e o SIM 40%.
6. Captura-recaptura por ano **não é estimável**: só 2019 tem duas listas nominais públicas (GGB x TDoR): N=186 (IC 175-198), cobertura GGB 60-68% (cenários 53-69%).
7. O GGB tem inconsistências internas verificáveis (seção 6) e 2023 e 2025 trazem **a mesma decomposição por causa** (204/20/17/16, total 257).
8. O Observatório **não publicou 2024 nem 2025**: ele mesmo diz que suspendeu atividades por falta de recursos. Isso é resposta, não lacuna.
9. A manchete GGB não muda de sinal com a definição (-42% todas as mortes, -39% sem suicídio, 2017-2025), mas 2017->2018 vai de -5,6% a -17,3% conforme se contam suicídios.

## 1. O que existe publicado e o que não (espaço de busca enumerado)

| fonte | anos coletados | lista nominal pública | observação |
|---|---|---|---|
| GGB totais | 1990-2025 (1990-99 digitalizado do gráfico; 1980-89 só total decenal 369) | só 2019 (Anexo 3, 329 casos) | 2022: sem anual; derivado 256 (Anuário 2023 confirma 256) |
| GGB composição | 2011-2021, 2023-2025 | não | relatórios de 2012 e 2016 estão no blog Homofobia Mata |
| ANTRA | 2016-2025 (179, 163, 124, 175, 140, 131, 145, 122, 80 em 2017-2025) | **não**: Mapa com "acesso restrito... a quem solicitar" (ANTRA 2020, nota 18) | link Google Maps 2017 dá 403: `fila-chrome.jsonl` |
| Observatório | 2021 (316), 2022 (273), 2023 (230), jan-mar 2026 (50) | não | 2024 e 2025: não produzidos |
| TGEU TMM | Brasil 2008-2025 (2.031 casos, API pública do app, IDs anônimos) | IDs sem nome | campo `reported_by` mostra a origem |
| TDoR | Brasil 2008-2025 (export público) | sim (nomes só em `_raw`) | |
| Disque 100 | 2011-2018 (Atlas 2020, MMFDH), 2022-2024 (só imprensa) | n/a | painel oficial: `fila-chrome.jsonl`; 846 (2019) do dossiê **não confirmado** |
| Anuário FBSP | homicídio doloso LGBT 2020-2025 | n/a | cobertura por UF incompleta (RJ, SP...) |
| Atlas da Violência | só notificações Sinan (não mortes), 2015-2024 | n/a | |
| SIM | agressão X85-Y09, 2000-2024 | n/a | sem campo de orientação |

## 2. Dependências documentadas (quem alimenta quem)

| par | evidência | janela |
|---|---|---|
| ANTRA <- GGB | ANTRA 2017: série 2008-2016 é a do GGB (2016: 144 = GGB 2016 "144 trans") | ate 2016 |
| TMM <- GGB | `reported_by` = GGB em 100% (2008), 52% (2010), 71% (2013), 96% (2014), 100% (2015) | 2008-2015 |
| TDoR <- GGB/Homofobia Mata (texto do registro) | 73% (2016), 91% (2017), 78% (2018); 0,7% em 2019 | 2012-2018 |
| Observatório <- GGB, ANTRA | gráfico 2000-2020 idêntico ao do GGB; "base compartilhada"; trans 2023 = 142+13 = 155 = ANTRA 145+10 suicídios | 2020-2023 |
| GGB <- Acontece | relatório 2020 "Fonte e Organização: Acontece LGBTI+; GGB" | 2020-21 |
| GGB cita TDoR | 7 casos do GGB 2019 têm o TDoR como fonte (F3) | 2019 |

Nenhuma dessas ligações mostra erro; mostram que contagens "concordantes" dessas fontes antes de 2019 repetem a mesma coleta.

## 3. (a) Correlação das variações anuais (log-diferença; bootstrap por anos, B=20000; permutação 5000)

| par | n | Pearson [IC95] | Spearman | sinal igual |
|---|---|---|---|---|
| GGB trans x ANTRA (2018-25, sem 2022-23) | 6 | 0,97 [0,64; 1,00] | 0,94 | 6/6 |
| GGB trans+homens trans x ANTRA | 6 | 0,98 [0,65; 1,00] | 0,94 | 6/6 |
| GGB trans x TMM ciclo, 2020+ | 4 | 0,84 [0,72; 1,00] | 1,00 | 3/4 |
| ANTRA x TMM ciclo, 2018+ | 8 | 0,74 [0,08; 0,97] | 0,52 | 7/8 |
| ANTRA x TMM ciclo, 2020+ | 6 | 0,72 [-0,30; 1,00] | 0,54 | 5/6 |
| ANTRA x TDoR ano civil, 2020+ | 6 | 0,91 [0,25; 1,00] | 0,94 | 6/6 |
| GGB total x ANTRA (2018-25) | 8 | -0,34 [-0,91; 0,57] | -0,21 | 5/8 |
| GGB total x TMM ciclo, 2020+ | 6 | -0,21 [-0,96; 1,00] | -0,03 | 4/6 |
| GGB total x TDoR ano civil, 2020+ | 6 | -0,72 [-1,00; 0,27] | -0,71 | 3/6 |
| GGB total x TDoR, 2010-2018 (**janela dependente**) | 9 | 0,94 [0,86; 0,99] | 0,98 | 9/9 |
| GGB total x Anuário FBSP (2021-25) | 5 | 0,15 [-1,00; 1,00] | 0,20 | 4/5 |

Leitura permitida: o **recorte trans** do GGB e as listas trans (ANTRA, TMM, TDoR) andam juntos desde 2018-2020; o **total** do GGB (com gays, suicídios, latrocínios) não anda com elas. O 0,94 de 2010-2018 vale pouco: é a mesma coleta. Não permitida: "as fontes se confirmam em nível". n=4 a 8, IC largos, 2022 sem composição do GGB.

## 4. (b) Razões entre contagens

| razão | anos | média [IC95 bootstrap entre anos] | tendência (rho vs ano) |
|---|---|---|---|
| GGB trans / ANTRA | 2017-25 (n=8) | 0,90 [0,83; 0,97] | -0,83 (p=0,01) |
| ANTRA / TDoR ano civil | 2017-25 | 1,03 [0,95; 1,10] | +0,78 (p=0,013) |
| ANTRA / TMM ciclo Out-Set | 2017-25 | 1,13 [1,03; 1,25] | +0,20 |
| Observatório trans / ANTRA | 2021-23 (n=3) | 1,07 [0,98; 1,21] | n pequeno |
| Observatório total / GGB total | 2021-23 | 1,00 [0,90; 1,07]: 316/300, 273/256, 230/257 | n pequeno |
| Anuário FBSP / GGB total | 2020-25 | 0,74 [0,63; 0,88] | +0,54 |
| GGB por mil mortes por agressão (SIM) | 2000-24 (n=25) | 4,8 [4,2; 5,5] | +0,87 (p<0,001) |

GGB trans / ANTRA por ano: 1,07; 1,01; 0,95; 0,92; 0,79; (2022 n/d); 0,88; 0,79; 0,80. O Estado (Anuário) registra cerca de 3/4 do que o GGB conta, mas por registros de BO com marca de orientação que várias UFs não têm (SP e RJ sem dado). Os mesmos autores publicam dois totais no mesmo ano (2021: 300 GGB vs 316 Observatório; 2023: 257 vs 230): diferença de critério, não de realidade. IC das razões: só variação entre anos.

## 5. (c) Captura-recaptura (Chapman) por ano

**Não estimável por ano.** Cada ano exige duas listas nominais públicas e independentes (`dados_analises/captura_recaptura_disponibilidade.csv`): GGB só 2019; ANTRA nenhuma; Observatório nenhuma; TMM e TDoR são a mesma base. Pior: 2012-2018 TDoR cita GGB/HM em 73-94% dos registros, então GGB x TDoR nesses anos violaria a independência de saída.

Único ano válido, 2019 (F3, `F3-ggb/dados/captura_recaptura_trans2019.json`): GGB trans 118, TDoR 139, sobreposição 88, **N=186 (IC95 175-198; cenários 151-221)**, união observada 169. Comparado ao agregado: GGB trans 118 = 63% de N (IC 60-68%); **ANTRA 124 = 67% de N** e 73% da união; TMM 130, TDoR violência 112. A união observada (169) já excede os 124 da ANTRA em 45 casos (definições diferentes: a ANTRA exclui suicídios e adota CVLI). N é **piso**: listas de mídia com dependência positiva subestimam N (Feldman 2017). Para 2020-2025 o agregado do GGB trans só pode ser comparado a ANTRA e TMM, sem estimativa de N.

## 6. (d) GGB x SIM (homicídios por agressão, CID-10 X85-Y09)

| janela | n | Pearson [IC95] | Spearman | sinal igual [IC exato] | inclinação dlogGGB~dlogSIM [IC] |
|---|---|---|---|---|---|
| 2001-2024 | 24 | 0,20 [-0,37; 0,60] | 0,13 | 13/24 [33%-74%] | 0,50 [-1,37; 1,23] |
| 2001-2017 | 17 | 0,07 [-0,43; 0,62] | 0,21 | 10/17 [33%-82%] | 0,29 [-1,74; 3,26] |
| 2018-2024 | 7 | -0,04 [-0,90; 0,90] | -0,14 | 3/7 [10%-82%] | -0,09 [-3,42; 1,97] |

- Níveis: GGB por mil mortes por agressão 2,9 (2000), 5,0 (2010), 7,0 (2017), 7,5 (2019), 5,0 (2020), 7,3 (2024). O GGB cresce muito mais que o SIM até 2017 (+242% vs +40%, 2000-2017; +71% vs +22%, 2010-2017). Isso é compatível com cobertura crescente da coleta e com aumento real; **este teste não distingue** (F3 já mostrou que o GGB por UF acompanha a violência geral).
- Direção ano a ano: coincide ao acaso. Correlação parcial GGB total x ANTRA controlando o SIM: -0,78 (IC -1,00 a 0,96; n=7), sem informação.
- 2017-2024: GGB -34,6% e SIM -37,3%: mesma ordem de grandeza. O SIM cai de 63,6 mil (2017) para 44,0 mil (2019); a causa dessa queda abrupta não foi testada aqui.

## 7. (e) Quebras de critério e sensibilidade da manchete

Quebras declaradas ou verificadas: suicídios 26 (2016), 58, 100, 32, 13, 24 (2017-21), 20 (2023-25); 2013 já tinha 10 suicidas, embora o GGB 2018 diga que só contou suicídios desde 2016; 2020-21 coprodução Acontece; 2021 novos termos de busca; 2024 "aprimoramento nas técnicas de coleta e depuração" sem reconciliação; 2025 região não informada 33%, idade 60%; ANTRA: 2020 só gênero feminino, 2024-25 só CVLI (descartou 15 e 12 casos).

Variação 2017->2025 (IC Poisson condicional, só ruído de contagem): todas as mortes 445->257 = -42,2% [-50,7; -32,5]; sem suicídio 387->237 = -38,8% [-48,1; -27,8]. 2017->2018: -5,6% [-17,6; +8,1] com suicídios; -17,3% [-28,9; -3,9] sem. 2019->2020: -28,0% todas; -24,6% sem suicídio; -21,0% homicídio estrito 272->215 [-34,2; -5,1]. 2023->2025: 0,0% nas três definições (257 e 257).

Inconsistências internas verificáveis (arquivo e página no painel/F3):
- GGB 2021, Tabela 1 por década: 2000-09 = 1.429 e 2010-19 = 3.029; a soma da série anual do GGB 2019 dá 1.446 (+17) e 3.363 (+334). A série "oficial" do GGB tem duas versões.
- Gráfico 1 do GGB 2020 (digitalizado, erro máx. 2,4) difere da Tabela 2019: 2005 = 81 vs 135; 2006 = 97 vs 112; 2007 = 123 vs 142; 2008 = 180 vs 187. O Observatório 2021 reproduz a tabela, não o gráfico.
- Composição por identidade não fecha o total: 2020 soma 230 de 237; 2021 soma 281 de 300; 2025 soma 255 de 257. 2020 tem duas tabelas com homens trans 2 ou 3.
- Revisão ex post pequena: 2013 312 -> 314; 2014 326 -> 329; 2015 318 -> 319.
- 2023 e 2025: mesma decomposição por causa (204 homicídios, 20 suicídios, 17 latrocínios, 16 outras; 257), com composição por identidade muito diferente (trans 127 vs 67). Probabilidade de coincidir em todas as 4 caixas por sorteio independente: 3,4 em 10 mil (descritivo). Não prova cópia; pode ser erro de edição; a planilha "Lista Geral - 2025" não é publicada.

## 8. O que cada teste permite e não permite

| teste | permite | não permite |
|---|---|---|
| correlação trans (a) | listas trans de mídia concordam na direção desde 2018-2020 | validar nível, independência plena |
| razões (b) | ver deriva da cobertura relativa (GGB trans cai, ANTRA/TDoR sobe) | dizer quem está certo |
| Chapman 2019 (c) | piso de ~186 trans em 2019; GGB e ANTRA cobrem 63-67% dele | estimar N de outros anos, cobrir gays/lésbicas (sem 2ª lista) |
| SIM (d) | nível e queda 2017-24 de mesma ordem; sem concordância ano a ano | afirmar incidência LGBT |
| quebras (e) | sinal da manchete robusto; níveis e 2017->18 sensíveis | tendência 2017-2025 sem reconciliação de critério |

## 9. Limites e reprodução

Séries curtas; 2022 GGB derivado; TMM ciclo é Out-Set; TDoR e TMM podem mudar depois de hoje; SIM 2023-24 com denominador extrapolado no que usa população (aqui só contagem). Ordem: `s01_fetch_tdor.py`, `s02_fetch_tmm.py`, `s03_sim_2000_2009.py` (venv DATASUS), `s05_digitaliza_ggb.py`, `s04_painel.py`, `s08_dep_tdor.py`, `s06_analises.py`, `s07_emit_sources.py`. Integridade: `scripts/SHA256SUMS`. Nomes de vítimas: só em `fontes/p3-ggb/_raw/` (fora do git).
