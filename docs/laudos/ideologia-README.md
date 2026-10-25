# Frente IDEOLOGIA: escores de ideologia partidária mais recentes que 2018/2021 (rodada 3, 2026-10-21)

## Recomendação (1 página)

**Principal: escore BRC por período.** É o survey de especialistas de Bolognesi, Ribeiro, Codato & Silva (ABCP/UFPR), 0-10, usando a **onda de jul/2018 para os anos 2012-2020 e a onda de jul/2022 para 2021-2024**, com as regras de sucessão de `ideologia_mapeamento.md` (fusão DEM+PSL ponderada por cadeiras; incorporações mantêm o escore do absorvedor; rótulos obsoletos via `ideologia_aliases.csv`). Os dados da onda 2022 são abertos (Dataverse 10.7910/DVN/MFIXKW) e cobrem **todos** os partidos: 351 de 351 UF-anos do painel ficam com escore, nas variantes wiki e tse. Nenhuma outra fonte cobre PMN, PHS e Avante, e as demais terminam em 2018-2020 (V-Party, PREPPS, CHES-LA, GPS) ou em 2021 (BLS), exceto por extrapolação.

**Robustez, nesta ordem:**

1. **BLS por legislatura** (Zucco & Power; ondas 2009/2013/2017/2021, convertidas para 0-10): independente do BRC, com onda dentro de cada legislatura. Cobre 348 de 351 UF-anos (não tem PMN, PHS, Avante nem PROS na onda 2013; 2023-24 é extrapolação da onda 2021 porque a BLS10, de 2025, ainda não foi publicada).
2. **Média BRC período e BLS** (0-10).
3. **Binária "governo de esquerda" (PT, PSB, PDT, PCdoB, PSOL) contra o resto**: não depende da escala de nenhuma fonte, e é o único contraste que todas as fontes sustentam (ver riscos).
4. **Subamostra com V-Party v2** (`v2pariglef` econômico e `v2palgbt` apoio a igualdade LGBT): só ~11 partidos por eleição e só mandatos até 2021. O `v2palgbt` é a única medida **do posicionamento do partido sobre o tema do desfecho**; use como controle positivo (partido sem escore = fora), não como principal.

**Variante por período é melhor que escore único, mas não resolve tudo.** Os autores do BRC escrevem (p. 10) que **não pretendem** que a classificação "viaje no tempo e possa ser utilizada para extrapolação em anos anteriores ou posteriores". Aplicar o escore de 2018 a 2012-2024 (o painel atual) viola isso; o período reduz a violação só para 2021-2024. Os anos 2012-2017 continuam retroprojeção de 1 a 6 anos, e é por isso que o BLS (ondas de 2013 e 2017) entra como a primeira robustez.

**O resultado do painel não depende da safra.** Reestimado o TWFE com 5 variantes contínuas de ideologia (atual, BRC período, BLS, média, BRC 2022 para todos os anos), 6 desfechos e 2 variantes de partido (`sensibilidade_twfe.md`): 60 coeficientes, todos entre −0,0102 e +0,0107 por ponto, **60 de 60 com IC95% cruzando zero**; a variante binária (esquerda x resto) também cruza zero em 12 de 12. O escore atual e o BRC por período têm Pearson 0,995 e Spearman 0,96 no nível UF-ano; só 2 UF-anos (wiki) ou 5 (tse) mudam mais de 1 ponto. Ou seja: atualizar é correção de procedência e de conduta com a fonte, não muda a conclusão. Declare isso no dossiê.

**Riscos que o dossiê deve declarar:**
- **Partidos sem escore.** No painel só ficam de fora 3 linhas de governador ("sem partido" x1, rótulo em branco x2, como já era). O BLS perde PMN, PHS, Avante e PROS em 2013; V-Party/CHES-LA/GPS cobrem 8-11 partidos; PSOL, PCdoB, Novo e Rede não estão no V-Party.
- **Ordem dentro da direita é frágil.** Sem o bloco de esquerda, o acordo entre fontes cai a 0,5-0,88 (Spearman, n=6-20) e BLS 2017 x BLS 2021 dá 0,65. No BRC 2018, MDB, PSDB e PSD estão a 0,1 ponto uns dos outros (erro-padrão ≈ 0,08). Por isso a binária.
- **Personalismo e contágio.** Os próprios autores atribuem o salto do PL (7,78→8,80) à candidatura de Bolsonaro em 2022 e o do PTB (6,10→7,72) a Roberto Jefferson (p. 19-20); PV, Rede e Cidadania "migram" por contágio da federação. Escore de especialista mede o partido percebido, que se mexe com o líder; para os UF-anos de 2023-24 sob PL (SC, RJ) o escore sobe 1,02.
- **Alinhamento governo/oposição no BLS.** O BLS é percepção de legisladores: em 2017 (após o impeachment) o PSB aparece em −0,17 (era −0,43 em 2013 e 2021) e o PSDB em 0,48. Esse componente de coalizão é o motivo de o BLS ser robustez e não principal.
- **Partidos de aluguel / legendas rasas.** PMN, PMB, PRTB, Avante e Agir têm não resposta de 7-17% em 2018 e 25-29% em 2022 (PSDB: 4% e 21%) e DP 1,7-2,3 (PT: 1,1-1,3), recomputado do CSV; o escore deles é pouco informativo. No painel só o PMN aparece (3 UF-anos, variante tse; Avante em nenhum).
- **Fonte do painel atual não é Q1.** `Dados` (Bolognesi, Ribeiro & Codato 2023) é Q2/Q2/Q3 no SJR (tabela de quartis do projeto). O artigo atualizado (Opinião Pública) está com quartil **não verificado** (fila). O único artigo Q1 da área (Zucco & Power, LAPS, Q1) teve só o apêndice lido; o texto principal está bloqueado (HTTP 429), na fila. Posição defensável: o dado é primário, aberto e reproduzido aqui (519/571 respondentes), e a conclusão do painel não depende dele; mas a regra "Q1 + texto integral" não está cumprida para o artigo de ideologia.

## O que está nesta pasta

| arquivo | conteúdo |
|---|---|
| `ideologia_partidos_ano.csv` | 1.432 linhas: partido (rótulo vigente), linhagem, ano 2010-2024, fonte, dimensão, escore nativo, escala, escore orientado (+ = direita), escore 0-10 (quando há limites), onda de origem, tipo (onda/alocado), distância em anos, n de avaliadores, DP, `existia_no_ano`, nota de mapeamento |
| `ideologia_ondas_observadas.csv` | 280 observações brutas por fonte-onda-partido (sem alocação) |
| `ideologia_mapeamento.md` | regras de sucessão/fusão/incorporação e de alocação, tabela partido x onda, correlações entre fontes (todas e sem bloco de esquerda), impacto no painel, achados laterais |
| `ideologia_correlacoes.csv`, `ideologia_correlacoes_por_ano.csv` | Spearman/Pearson por par de ondas (296 linhas, dois subconjuntos) e por ano-calendário (250 linhas) |
| `ideologia_aliases.csv` | rótulo nos CSV de governadores -> linhagem |
| `impacto_painel_{wiki,tse}.csv`, `impacto_painel_resumo.json` | por UF-ano: escore atual (replicado: 351/351 idêntico ao painel), BRC período, BLS, média, BRC 2022 para todos, fração de esquerda |
| `sensibilidade_twfe.md` | TWFE do painel com cada variante |
| `sources.jsonl` (14), `fila-aquisicao.jsonl` (9) | ledger via `emit_sources.py`; pendências |
| `scripts/`, `raw/` | `build_ideologia.py`, `gerar_mapeamento_md.py`, `sensibilidade_twfe.py` (rodam com `python3.14 -I`); entradas com sha256 em `raw/SHA256SUMS.txt` |

Para trocar o painel: `ideologia_partidos_ano.csv` filtrado em `fonte == BRC`, junte por `linhagem` (via `ideologia_aliases.csv`) e `ano`; ou use a coluna `ideo_BRC_periodo` de `impacto_painel_*.csv`, que já está agregada por UF-ano com os mesmos pesos em meses do painel.

## Espaço de busca enumerado (o que foi varrido, com resultado)

| fonte | cobertura | escala / método | leitura | uso |
|---|---|---|---|---|
| **BRC** Bolognesi, Ribeiro, Codato & Silva 2025, *Opinião Pública* 31:e31120 (dataset 10.7910/DVN/MFIXKW) | jul/2018 (n=519) e jul/2022 (n=571 no CSV; o texto diz 978 convidados x 48,8% ≈ 477, inconsistência); 35 e 32 partidos, todos os registrados no TSE | 0-10, média de cientistas políticos da ABCP; online | artigo integral (28 p.) + codebook + microdados ✅ | **principal** |
| BRC 2023 *Dados* 66(2) (a fonte do painel) | jul/2018, 35 partidos | idem | integral ✅ (p. 3, 5) | substituída; Q2 |
| **BLS** Zucco & Power 2024, *LAPS* 66(1) (10.7910/DVN/6KVTUV) | 9 ondas 1990-2021; usadas 2009/13/17/21; 22 partidos no total, 20 em 2021 | ≈ −1..+1; legisladores avaliam partidos; modelo bayesiano | apêndice + readme ✅; texto principal ⚠️ (Cambridge 429) | robustez 1 |
| BLS10 (2025, 137 legisladores) | não publicado até hoje | | só snippet de busca ⚠️ | fila |
| **V-Party v2** (V-Dem, fev/2022) | eleições até 2018 (1970-2019); BR ~11 partidos/eleição; `v2pariglef` (econômico), `v2palgbt` (LGBT) | IRT; ≥ 4 codificadores | codebook ✅ (p. 29-31); dados pelo pacote oficial `vdemdata` (o ZIP oficial pede e-mail) | robustez 4; não existe V-Party posterior ao v2 |
| **PREPPS Latam V2** (Wiesehomeier et al.; 10.7910/DVN/JLOYIJ) | 2018/19; 17 partidos; Left-Right e Social Policy (aborto, homossexualidade, divórcio, eutanásia) | 1-20; n por partido 13-115 no Left-Right | codebook + dados ✅; V2 idêntico ao V1 nas linhas comuns | validação |
| **CHES-LA 2020** | 11 partidos + Bolsonaro; lrgen, lrecon, galtan, sociallifestyle | 0-10 | codebook + dados ✅ | validação |
| **Global Party Survey 2019** (Norris) | 8 partidos; V4 econômico, V6 valores sociais (cita casamento homoafetivo) | 0-10; 47 especialistas | codebook + dados ✅ | validação |
| MARPOR/Manifesto Project | Brasil: só programas presidenciais 1989-2018 (segundo Tarouco et al. 2022, só resumo lido) | RILE; codificação manual | **não acessado** (site em timeout) ⚠️ | fila; baixa utilidade (poucos partidos, sem 2022+, RILE pouco correlacionado com surveys segundo o resumo de Tarouco et al.) |
| PELA (Salamanca) | legisladores, auto-posicionamento | | só resultados de busca; dados por partido de 2019-2023 não localizados | não obtido |
| Pontos ideais por votações nominais 2019-2023 | | | busca (PT/EN): nenhum artigo localizado; só 2011-2015 (Scheeffer) | não obtido |

Bases e termos: WebSearch (14 consultas em PT/EN/ES: V-Party/v2palgbt, BLS/BLS10, CHES-LA, PREPPS, GPS, MARPOR Brasil, PELA, classificação por especialistas 2022, pontos ideais), API de busca da Harvard Dataverse (7 consultas), API do Zenodo (2), API do GitHub (árvore do `vdemdata`), OpenAlex (DOI do LAPS), páginas v-dem.net, chesdata.eu, QoG, B2FIND, SciELO, Unicamp/Opinião Pública. Negativos são "não localizado nestas bases com estes termos", não "não existe".

## Pendências (fila-aquisicao.jsonl)

Texto principal de Zucco & Power 2024 (CC-BY, Cambridge bloqueia), Tarouco et al. 2022 integral, MARPOR Brasil, BLS10, quartis SJR (Opinião Pública, RBCP), datas oficiais do TSE (incorporações marcadas ⚠️), ondas PREPPS 2006-2015, e a decisão do autor sobre o e-mail para o ZIP oficial do V-Party (não usei o e-mail dele).

Becos: Cambridge/LAPS (HTTP 429 a curl e WebFetch; volta pelo Chrome real); manifesto-project.wzb.eu (timeout; volta pelo Chrome real); wiesehomeier.net (sem resposta; volta por GIGA/autores); ZIP oficial do V-Party (formulário com e-mail; volta se o autor autorizar); TSE (403; volta pelo Chrome real); sjr2025.csv do projeto está corrompido (página do Cloudflare), usei só as tabelas .md de quartis.
