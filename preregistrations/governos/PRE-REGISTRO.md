# PRE-REGISTRO: governos e perseguição a homossexuais (frente discurso/governos)

Gravado em 2026-10-22T21:29:37Z (hora exata e sha256 no arquivo irmão `PRE-REGISTRO.sha256`, gerado logo após esta gravação). Nada abaixo foi reescrito depois da classificação; qualquer regra nova entra só na seção final **ADENDO pós-classificação**.

## 0. O que já tinha visto ANTES de gravar (honestidade do "declarado antes")

Exploração prévia, sem classificar nenhum país no eixo esquerda-direita e sem ler nenhum valor de `v2pariglef`/`v2palgbt`/`v2x_regime` por país:
- a lista nacional da ILGA (7 países "Death Penalty / Yes" e 5 "No legal certainty", conferida com a página ILGA de junho/2026: "The death penalty is the legally prescribed penalty ... in 7 UN member States. In 5 more, there is no full legal certainty");
- os nomes e rótulos das variáveis V-Dem/V-Party e a escala do `v2pariglef` (codebook V-Party v2, p. 30: 0 far-left ... 3 center ... 6 far-right, **eixo ECONÔMICO**, não cultural);
- o texto do relatório F8-literatura (CNV, OSCE Chechênia, Lapunov) já lido por outra frente.
O que decide o resultado (classificações, vereditos) foi definido nas seções 1 a 6 antes de qualquer tabela ser montada.

## 1. Universo

**U1 (lei e execução hoje).** As 12 entradas nacionais da ILGA World Database (consulta GraphQL pública `entriesCsssa`, 2026-10-22T21:19:21Z, sha256 de `ilga-db-csssa-all.json` = `55d53d6a...c3ea`) com pena de morte `Yes` (Brunei, Irã, Mauritânia, Nigéria [12 estados do norte, sharia], Arábia Saudita, Uganda, Iêmen) ou `No legal certainty` (Afeganistão, Paquistão, Catar, Somália, Emirados). Nigéria: o crime nacional é 10 anos a prisão perpétua; a pena de morte é **subnacional** e é codificada `legal_subnacional`; o executivo avaliado é o federal e isso é declarado.
**U2 (leis recentes de repressão, nomeadas pelo dono ou pela ILGA 2026).** Uganda 2023 (AHA), Rússia 2023 ("movimento internacional LGBT" extremista), Chechênia 2017, Hungria (lei de 2021 + proibição da Parada 2025), Polônia (zonas "LGBT free", 2019-2021), Iraque 2024, Burkina Faso 2025, Senegal (2025-26, "since June 2025"), Trinidad e Tobago 2025. Cada linha só entra com fonte primária lida (lei, relatório de órgão, acórdão) ou a entrada ILGA DB com seu rodapé.
**U3 (sistemático).** Todos os 65 Estados-membros da ONU que a ILGA DB marca `legal = false` (criminalizam) no dia da consulta, para a tabela de regime e de legitimação ideológica (sem pena de morte: coluna `execucoes` = `n/a`).
**U4 (históricos).** Alemanha 1933-45, Espanha franquista, URSS (art. 121, 1934), Cuba (UMAP 1965-68), Irã pós-1979, Brasil 1964-85. Entram com 1 fonte primária ou secundária lida por caso; quartil conferido em `fontes/scimago/quartis-sjr-2026-10-10.md` e `-10-11.md`; fora das tabelas = `quartil=nao_verificado`.
**U5 (Brasil recente).** Governos Dilma II (até 31/08/2016), Temer (2016-18), Bolsonaro (2019-22), Lula III (2023-24).

## 2. Regime

`v2x_regime` (Regimes of the World, V-Dem; 0 autocracia fechada, 1 eleitoral, 2 democracia eleitoral, 3 liberal) do **ano mais recente com valor** até 2025 no pacote `vdemdata` v16.0 (`vdemdata-vdem.RData`, sha256 `39b412d3...3ea5`, baixado de github.com/vdeminstitute/vdemdata). Casos históricos: ano do evento. País que a base não cobre (ex.: Brunei se faltar) = `sem_dado`, nunca inferido. Não uso "teocracia" como categoria de regime (V-Dem não a tem); descrevo o que a legitimação oficial diz pela seção 3.

## 3. Ideologia do executivo (regras R1 a R4)

- **R1 Executivo partidário (vale só onde a base tem o partido).** Partido do chefe de governo = o partido com `v2pagovsup == 0` ("Yes, as senior partner. The Head of Government belongs to this party") na eleição V-Party mais recente com data ≤ ano de referência (`vdemdata-vparty.RData`, V-Party v2, cobre eleições até 2019, sha256 `a4bde75e...b964`). Reporto `v2pariglef_ord` (**econômico**: 0-2 esquerda, 3 centro, 4-6 direita, pelos rótulos do codebook) e `v2palgbt_ord` (0 "strongly opposes" ... 4 "strongly supports"). A defasagem (ano da eleição versus ano de referência) vai numa coluna; defasagem > 4 anos = `defasado`. Brasil: BRC/BLS de `dados/ideologia/`.
- **R2 Sem partido na base (monarquias, emirados, talibã, regimes de partido único não codificado).** Eixo esquerda-direita = `nao_aplicavel`. Em vez disso reporto as categorias oficiais V-Dem `v2exl_legitideolcr_0..4` (nacionalista; socialista ou comunista; restauradora ou conservadora; separatista ou autonomista; religiosa) do ano de referência, mais `v2exl_legitideol` (0-4, o quanto o governo justifica o regime por uma ideologia).
- **R3 Histórico.** Categorias V-Dem do ano do evento; mais a classificação que a própria fonte lida enunciar, entre aspas. Não atribuo "direita/extrema direita/esquerda" por julgamento meu.
- **R4 Proibido:** rótulo de Wikipedia, de imprensa ou meu como substituto das regras R1-R3. Se nenhuma regra classifica, o campo é `nao_classificado`, e o placar diz "não testável nesse quesito".

Limites declarados de antemão: o eixo do V-Party é econômico e pode divergir da posição sobre o tema LGBT (por isso `v2palgbt` vem junto); escores de especialista mudam com o líder (Bolognesi et al., p. 19-20 em `ideologia/README.md`); V-Party v2 não tem eleição após 2019, então Uganda 2023, Hungria 2025, Polônia 2021 etc. usam defasagem declarada.

## 4. Violência de Estado: níveis e códigos (definidos antes de ler os casos)

| Nível | Definição |
|---|---|
| L0 | sem lei de criminalização (ILGA) |
| L1 | criminalização sem pena de morte |
| L2 | pena de morte prevista em lei (`Yes`) ou possível (`No legal certainty`) |
| L3 | execução, tortura ou detenção em massa por agentes do Estado ou por autoridade de fato **documentada por órgão internacional, tribunal ou relatório oficial lido** (ONU, OSCE, TEDH, Estado pesquisando a si mesmo, comissão da verdade); conta do ILGA/ONG sem fonte primária lida = `L3_declarado` |
| L4 | campanha coordenada de eliminação física com autoria estatal reconhecida em fonte primária |

Código de execução (coluna `execucoes`): `E1` judicial pelo Estado; `E2` por autoridade de fato não internacionalmente reconhecida (milícia que controla território, ex.: huthis, talibã, Al-Shabaab); `E3` extrajudicial por agentes do Estado; `E0` nenhuma achada nas fontes lidas (**não** significa que não houve); `ND` não avaliado. Cada código leva o nome da fonte e se é primária (ONU/tribunal/órgão) ou secundária (ONG; ILGA compilando).

## 5. Placar: veredito por afirmação-tipo (escala fixa)

Escala: **sustentada** (existe ≥ 1 caso que cumpre o critério exato, com fonte primária lida); **parcial** (parte da afirmação cumprida; a lacuna nomeada); **não sustentada** (a fonte lida contradiz, ou o espaço enumerado não achou caso); **não testável** (a base não classifica ou não registra o que a afirmação exige).

As afirmações são lidas como **existenciais** ("há governo ..."), porque as universais ("todo governo de direita ...") são refutáveis por um só contraexemplo e ninguém as sustenta; cada uma é testada em dois escopos, **Mundo** e **Brasil**:
- (a) "governo de direita X quer matar gays": sustentada se há caso com executivo de direita (R1 `v2pariglef_ord` ≥ 4, ou R3 com a fonte dizendo "direita/extrema direita") e L3 ou L4; parcial se só L2 (lei) ou só retórica documentada; não sustentada se nenhum caso de direita passa de L1; não testável se R1-R3 não classificam nenhum.
- (b) "governo de esquerda Y persegue gays": mesma régua com `v2pariglef_ord` ≤ 2, ou R3 `socialista/comunista` + fonte; "persegue" = L3 (prisão, internação, trabalho forçado), "mata" = L3 com E1/E3 documentado.
- (c) "o Estado brasileiro nunca perseguiu gays": sustentada só se nenhum documento primário lido registra perseguição; vale a CNV vol. II (já lida em F8-literatura/README.md, A1) para 1964-85.
- (d) "em governos extremos nunca houve isso": lida como "nunca houve perseguição de Estado a gays em governo [de direita ou de esquerda] extremo". Refutada por UM caso L3 documentado em cada flanco (teste simétrico) e, no Brasil, por 1964-85; para 2019-22 e 2023-24 a escala da seção 6 se aplica.

Registro/ONG/imprensa nunca fecha um veredito sozinho: vale só como "contagem declarada" (regras do BRIEFING-COMUM).

## 6. Brasil: tipologia e dicionário de coleta

**Tipologia (mutuamente exclusiva por item):** T1 retórica hostil; T2 retórica protetiva ou neutra; T3 omissão/corte de política (decreto, extinção de órgão ou programa, veto, contingenciamento) ; T4 ação de proteção (decreto, lei sancionada, criação de órgão, canal de denúncia); T5 perseguição por agentes do Estado (operação policial, expurgo, internação); T6 política de extermínio (ordem ou programa de eliminação física). Declaração = verbatim com URL, data e página salva (sha256) em `fontes/q1-textointegral/discurso/governos/`; nunca de memória.

**Agentes (os mesmos para os dois flancos):** presidente; vice; ministro/a de Direitos Humanos (ou da Mulher, Família e Direitos Humanos); ministro da Educação; ministro das Relações Exteriores; ministro da Justiça/Segurança; secretário nacional LGBT quando existir. Governos: Dilma II, Temer, Bolsonaro, Lula III.

**Dicionário de consulta (WebSearch standard, uma passada, sem reescrever depois; PT/EN/ES):**
- `"<agente>" homossexuais declaração "entrevista" site:gov.br OR planalto.gov.br OR camara.leg.br OR folha.uol.com.br OR g1.globo.com`
- `"<agente>" gays "kit anti-homofobia" OR "ideologia de gênero" OR "casamento homoafetivo" OR "conselho LGBT" OR "Disque 100"`
- EN: `"<agent>" homosexuals Brazil statement government`; ES: `"<agente>" homosexuales Brasil declaración gobierno`
- ações: `decreto 9.883 OR 9.465 OR 10.883 conselho nacional LGBT` e `decreto 11.* conselho LGBTQIA+ 2023`, `veto kit anti-homofobia 2011`, `Brasil Sem Homofobia`, `extinção SECADI`, `portaria Ministério dos Direitos Humanos LGBT 2023`; a lista é fechada aqui; item achado fora dela entra no ADENDO.
Contagem de tentativas por consulta registrada no `GOVERNOS.md`. Negativo = "espaço de busca enumerado", nunca "não existe".

**Dados oficiais por governo (Brasil 2016-2024):** (i) Sinan campo 55 (`dados/sinan/serie_campo55_uf_ano.csv`, soma de `m_lgbtfobia` por ano) com o faltante de campo; (ii) Anuário FBSP "racismo por homofobia ou transfobia" (`dados/anuario/`, só 2022-2025); (iii) Disque 100/Ouvidoria MDHC: só o que estiver publicado sem login nem pedido (relatório 2019 já lido; demais anos: tentar `dados.gov.br`/gov.br anônimo, e se exigir cadastro registro "não publicado/inacessível sem pedir"); (iv) SIM: não registra orientação, fica de fora. Regra de leitura: média anual por governo, razão entre governos, **sem teste de hipótese**, porque o registro não é incidência (dossiê) e o campo 55 muda de cobertura. Veredito sobre "mais violência sob o governo X": `não testável`, salvo se houver série com cobertura constante.

## 7. Proibições operacionais

Não contatar ninguém; só fonte pública sem login; sem Playwright (fila em `fila-chrome.jsonl`); nomes de vítimas fora dos entregáveis; ledger só por `emit_sources.py`; nada em /tmp.

## ADENDO pós-classificação

(vazio no momento da gravação)

---

**ADENDO pós-classificação (escrito DEPOIS de ver os dados; cada item diz o que mudou e por quê; nada acima foi reescrito).**
Hora de início deste adendo: ver `PRE-REGISTRO.sha256` (o arquivo acima não foi alterado depois do hash; este bloco foi anexado depois e portanto o sha256 final do arquivo é outro: ver `PRE-REGISTRO-COM-ADENDO.sha256`).

| # | O que mudou | Motivo observado | Efeito |
|---|---|---|---|
| A0 | Correção do item 0 acima: antes da gravação a checagem de esquema da base V-Dem imprimiu `v2x_regime` de Uganda (1,0, anos 2023-25). Era a única linha por país vista; não definiu nenhuma regra | honestidade do "declarado antes" | nenhum |
| A1 | `v2exl_legitideolcr_*` são FRAÇÕES de codificadores que marcaram a categoria (0 a 1), não 0/1. "Marcada" = fração >= 0,5; `v2exl_legitideol` é uma escala intervalar (z), não 0-4 como escrevi na seção 3 | ao abrir os dados (ex.: Irã 2023, religiosa = 0,80; Arábia Saudita 2023, religiosa = 1,00) | tabela reporta as frações; nenhuma classificação depende do corte |
| A2 | R1 trocada: partido do chefe = `v2exparhos` (V-Dem, chefe de Estado) no ano de referência, casado por sobreposição de palavras (>= 0,5) com o partido do V-Party; abandonei o critério `v2pagovsup == 0` | `v2pagovsup == 0` devolveu para o Irã "Pervasive Coalition of Reformists" (presidente subordinado ao Líder Supremo), o que não identifica quem governa de fato; `v2exparhos` diz `technical` para Irã, Arábia, Afeganistão, Iêmen, Catar | executivos sem partido saem como `nao_aplicavel` em vez de receber um rótulo falso |
| A2b | Em sistemas onde o poder efetivo é do chefe de GOVERNO (V-Dem `v2ex_hogw` >= 0,5 e `v2ex_hosw` < 0,5: Paquistão, Emirados, Somália, Hungria, Polônia, Iraque, Trinidad e Tobago), o partido vem do V-Party (`v2pagovsup == 0`, eleição mais recente <= ano de referência) e a continuidade é o NOME do chefe de governo (V-Dem `v2exnamhog`) constante entre a eleição e o ano de referência; poder dividido 0,5/0,5 (Mauritânia, Irã com Líder sem partido) fica `nao_classificado`/`nao_aplicavel` | `v2exparhos` é só do chefe de Estado e, nesses países, ele não manda (ex.: Iraque 2024: HoS do PUK, HoG de outra coalizão) | Paquistão, Somália, Iraque e Trinidad e Tobago saem `nao_classificado`; Hungria e Polônia seguem classificadas |
| A3 | Defasagem > 4 anos entre o ano de referência e a eleição V-Party só é aceita se o rótulo de partido do chefe no V-Dem for o mesmo em todos os anos do intervalo (checado por código); rotulado "defasado>4a, partido continuo no V-Dem" | V-Party v2 acaba em 2019; Uganda/Hungria/Paquistão/Iraque têm referência em 2023-25 | 4 linhas entram com ressalva |
| A4 | Ano de referência histórico: URSS 1979 (primeira eleição V-Party do PCUS dentro da vigência do art. 121, 1960-93); Espanha 1970 (Lei 16/1970); Cuba 1966 (UMAP); Alemanha 1936; Brasil 1975; Irã 1980 | a seção 1 não fixou ano para U4 | declarado na coluna `ano_ref` |
| A5 | Brasil: limiar para o BRC (0 a 10, esquerda-direita geral): < 4 esquerda, 4 a 6 centro, > 6 direita | a seção 3 só fixou limiar para o V-Party | PT 2,7-3,0; MDB 6,5-7,0; PSL 8,1; PL 8,8 (nenhum caso cai perto do corte) |
| A6 | Níveis novos: `LE` (restrição legal de expressão/associação/extremismo, sem criminalizar o ato) e `LE-local` (resoluções municipais não vinculantes); `L3_declarado` (conta de ILGA/ONG sem fonte primária lida); `L4 PROVISORIO` para a Alemanha nazista, porque a escala vem de fonte institucional (USHMM) e a seção 4 exige fonte primária | Rússia 2023, Hungria e Polônia não cabiam em L0-L4 | nenhum veredito depende de L4 |
| A7 | Brasil: T1 dividido em T1a (hostil a pessoas/grupo) e T1b (contesta decisão/política); `T3?` marca omissão sem linha de base comparável | a fala de 14/06/2019 critica uma decisão do STF e não ataca pessoas; o rol de 2019 repete o de 2017 | classificação é minha e vem na coluna `julgamento_meu` |
| A8 | Acrescentei duas variáveis culturais do V-Party (`v2paculsup_ord`, `v2parelig_ord`) e a leitura "eixo econômico não é proxy da posição LGBT" | PiS (Polônia) sai "centro-esquerda" (2) no eixo econômico e "opõe-se fortemente" à igualdade LGBT (0); CPSU (extrema esquerda, 0) também "opõe-se fortemente" (0) | o veredito (a)/(b) é lido com `v2palgbt` ao lado |
| A9 | Duas análises exploratórias NÃO pré-registradas: `eixo_vparty.md` (Spearman e tabela econômico x LGBT) e `u3_resumo.md` (regime x criminalizar) | pergunta do dono sobre a "relação com o eixo" | descritivas, sem teste de hipótese |
| A10 | Fontes além das previstas: API GraphQL pública da ILGA World Database (a própria página usa; sem login), Amnesty (ONG), USHMM (instituição), imprensa brasileira como veículo de fala | ILGA SSH 2020 é o último relatório "State-Sponsored Homophobia"; os dados vivos estão no banco (consulta de 2026-10-22T21:19Z) | cada uso marcado `L3_declarado`/"contagem declarada" |
| A11 | Em jan-jun/2026 a ILGA já publica "65 criminalizam" e "7 pena de morte legal + 5 sem certeza", e o banco consultado coincide (checado por código); o relatório "Laws on Us 2024" (maio/2024) traz 61+1 | números mudam com a data | usei o banco de 2026-10-22 como universo e o relatório de 2024 só para texto |
