# F3 — Auditoria empírica das contagens do Grupo Gay da Bahia (GGB)

Data: 2026-10-21. Frente F3 da rodada 3 do LGBT-INDICADOR. Pasta: `research-2026-10-21-rodada3/F3-ggb/`.
Sem juízo de valor sobre a organização: o que segue mede o que a lista do GGB permite medir, com semente fixa e planilha rastreável.

> [!IMPORTANT]
> **Desvio do pedido, declarado antes de tudo.** O pedido era validar por amostra "o ano mais recente com lista caso a caso (2023 ou 2024)". **Nenhum relatório do GGB de 2020 a 2025 publica lista nominal nem link por caso.** Os releases 2023, 2024 e 2025 são agregados com 3-4 exemplos nominais. O único ano com lista nominal (Anexo 3, 329 casos) e fonte por caso (Anexo 4) é **2019** (publicado em 2020). Toda a validação por amostra vale para 2019. **Para 2023, 2024 e 2025 (os números 257, 291, 257 que o dossiê usa como numerador) a contagem é inauditável com o que o GGB publica.** O release 2025 diz que existe a planilha "Lista Geral - 2025 - GGB.xlsx" (PDF p. 12); ela não é publicada. Condição de volta: essa planilha (ver `fila-aquisicao.jsonl`, item `ggb-planilhas-2020-2025`).

## 0. Resposta em 11 linhas

1. **Verificável hoje, 2019, pela fonte citada pelo próprio GGB:** em amostra aleatória de 160 dos 329 casos (semente 20261021), **50 (31,3%; IC95% Wilson 24,6-38,8%)** têm a matéria do caso recuperada, confirmam morte violenta e identificam a vítima como LGBT+ de forma explícita. É um **piso**: 54 casos (33,8%) não tiveram a fonte recuperada (link morto, domínio morto, sem link) e entram como "não verificados". Limites de pior/melhor caso: 31% a 65%.
2. **Condicionado à fonte ser a matéria do caso** (88 de 160): **56,8% (IC95% 46,4-66,7%)** verificáveis; morte violenta confirmada em 83,0% (73/88; 73,8-89,4%); em 26,0% (19/73) a fonte cita a morte mas **não menciona orientação nem identidade** (a ausência na fonte citada não prova que a vítima não fosse LGBT+; prova que aquela fonte sozinha não verifica).
3. **O motivo reportado na própria fonte** (73 casos com morte violenta confirmada): LGBTfobia atribuída por alguém (polícia, família, testemunha, veículo) em **4,1% (3/73; IC 1,4-11,4%)**; motivo desconhecido 47,9% (35/73); conflito interpessoal 17,8%; roubo/latrocínio 17,8%; passional 8,2%; suicídio 4,1%. A contagem do GGB mede **mortes de pessoas identificadas pela mídia como LGBT+**, não crimes de ódio. O próprio GGB diz que latrocínio e toda profissional do sexo trans morta "devem sempre ser incluídos" (release 2025, PDF p. 12).
4. **Duplicata é desprezível:** 1 par provável em 329 (0,3%; mesma pessoa, categorias diferentes). Nove links compartilhados são nove eventos de 2 vítimas, conferidos um a um.
5. **Captura-recaptura (só trans/travestis 2019; GGB x TDoR/TGEU):** 88 dos 118 casos trans do GGB aparecem na lista TDoR Brasil (139); Chapman N = 186 (IC95% 175-198; cenários 151-221). O GGB cobre **53-69%** do total estimado para esse subgrupo. Não há sinal de inflação nesse recorte; há subcobertura relativa à união das listas. **Piso, não ponto:** listas positivamente dependentes (ambas de mídia; 7 casos GGB citam o próprio TDoR) subestimam N.
6. **"Infla com a internet?" não se sustenta nos dados que consegui montar:** entre 27 UFs, a taxa GGB por milhão **cai** com a cobertura de internet (rho de Spearman -0,43; IRR 0,78 por DP) e **sobe** com a taxa geral de homicídio (rho 0,39; IRR 1,33 por DP, IC 1,13-1,57, já controlando internet). Na série nacional 2016-2025 o GGB cai (445 em 2017 para 257 em 2025) enquanto o uso de internet sobe de 66,0% para 90,5%. A distribuição por UF do GGB **espelha a violência geral**, não a notificação específica de LGBTfobia (Sinan campo 55: rho 0,11, p=0,60). **Ressalva:** isso só cobre 2016-2025 (série em queda) e o corte UF de 2019; **não refuta** o crescimento 2002-2016 (+253% em Mendes & Silva 2020), período que não testei (sem série de internet por UF antes de 2016).
7. **A série GGB não é tendência:** composição e critério mudam (suicídios 58 em 2017, 100 em 2018, 32 em 2019, 13 em 2020; travestis/trans 49% em 2023, 33% em 2024, 25% em 2025; 2025 com região "não informada" em 32,7% e idade "não informada" em 59,9%). A manchete **não muda de sinal** com a definição (todas as mortes, sem suicídio, só homicídio estrito), mas o **nível** muda 6% a 21%.
8. **Ressalva de método:** a amostra mede **precisão** (o que está na lista é o que diz ser?), não **cobertura** (o que falta na lista?). Só o recorte trans permite uma estimativa de cobertura, e ela é piso.
9. **Dupla codificação cega por outra família de modelo** (Gemini 3.8 Flash, via Antigravity; 23 casos): kappa 0,91 (identificação LGBT+), 0,92 (base da identificação), 0,85 (motivo), 0,92 (desfecho), 0,73 (tipo), 0,64 (correspondência), **0,46 (morte confirmada)**. A morte "violenta" é o item frágil: 2 dos 6 desacordos são "encontrado morto, causa não informada" (eu: indeterminada; ele: violenta).
10. **Dossiê:** a cópia local `fontes/t6-ggb-release-2025/` citada no dossiê **está vazia** (0 arquivos). Passou a existir em `fontes/p3-ggb/_raw/pdf/` (gitignorado).
11. **Nada aqui prova fraude nem prova confiabilidade como taxa.** Seção 7 diz o que pode e o que não pode ser afirmado.

## 1. Metodologia declarada pelo GGB e quebras de série (passo 1)

Fonte dos trechos, páginas (índice do PDF, não numeração impressa) e sha256: `dados/metodologia_trechos.csv`. Arquivos em `fontes/p3-ggb/_raw/pdf/`; ledger em `sources.jsonl` (14 entradas, via `emit_sources.py`).

| ano | total | composição publicada | lista nominal | fonte por caso | observação verbatim / quebra |
|---|---|---|---|---|---|
| 2017 | 445 | 387 H + 58 S | não | não | série "desde 1980"; sem detalhe de latrocínio |
| 2018 | 420 | 320 H + 100 S (24%) | não | não | hemeroteca digital "Homotransfobia Mata"; suicídios saltam de 58 para 100 |
| 2019 | 329 | 272 H + 32 S + 19 L + 5 atropelamento + 1 silicone | **sim (Anexo 3)** | **sim (Anexo 4: veículo + link)** | "158 casos com indícios ... descartados" (p. 24); "retirado 58 casos da nossa lista original" (p. 37); busca diária no Google com "encontrado morto", "professor morto"; inclusão por inferência ("profissão mais associada ao segmento", p. 27) |
| 2020 | 237 | 215 H + 13 S + 9 L | não | não | coleta por Google Alerts (p. 17); relatório assinado "Acontece LGBTI+; Grupo Gay da Bahia"; suicídios caem de 32 para 13 |
| 2021 | 300 | 276 H (inclui 34 L) + 24 S | não | não | amplia termos ("mulher trans", "morte suspeita", "estado de putrefação"); fontes: delegacias, listas de óbito de serviços fúnebres, Facebook/Instagram (p. 17) |
| 2022 | 256 (derivado) | sem detalhe | não | não | `relatorio2022.pdf` é balanço do 1º semestre (135 mortes), **não** o anual; 256 vem de "um caso a mais" no release 2023; o Observatório (Acontece/ANTRA/ABGLT) publicou 273 para 2022 (busca web; PDF não lido) |
| 2023 | 257 | 204 H + 20 S + 17 L + 16 outras ("221 homicídios incluídos os latrocínios e feminicídios") | não | 3 exemplos | 20 casos "em limbo" fora da conta |
| 2024 | 291 | 273 "homicídios" + 18 S | não | 4 exemplos | 32 casos "no limbo"; "aprimoramento nas técnicas de coleta e depuração dos dados" (p. 3) **sem reconciliação** com a série; 6 heterossexuais incluídos (p. 3) |
| 2025 | 257 | corpo: 204 H + 20 S + 17 L + 16 outras; **destaque: "237 homicídios"** | não (planilha citada, não publicada) | exemplos | 237 = 204+17+16 (inclui latrocínio e outras); região NI 84/257, idade NI 154/257, meio NI 58,4%, local NI 41,2% |

Critérios de inclusão e denominador (verbatim, release 2025): "Latrocínio contra LGBT devem sempre ser incluídos como crimes homofóbicos" e "toda profissional do sexo trans ou travesti vítima de morte violenta na 'pista' ou na cena de prostituição, deve ser incluída nessa estatística de crimes homotransfóbicos" (p. 12 do PDF); "mais de 10% da população brasileira que é LGBT+" (2025, p. 3; 2024, p. 2), contra 1,89% (PNS 2019, no dossiê).

**Contradição com o dossiê (§4, "viés declarado só para baixo"):** o GGB declara subnotificação (para baixo) **e** regras de inclusão amplas (latrocínio, suicídio, heterossexuais "confundidos", profissionais do sexo trans) e um denominador >10%. Mendes & Silva 2020 (`fontes/p2-f3f5-politica-dos-numeros/mendes-silva2020-csc.pdf`, sha256 `3a9cf765d7dae6a42bb8471fa17fd99eed95dde4f05ddc8425bba00724f02ce4`) escrevem que os homicídios do GGB "necessariamente não ocorreram por motivações homofóbicas" e que "para cada homicídio de LGBT registrado e noticiado existem dois outros que não foram notificados" (p. 1710; a referência da estimativa "dois outros" não resolvi: ⚠️). A frase correta é: o GGB **declara** subnotificação e **adota** critério largo de inclusão; as duas coisas coexistem.

Quebras de série que impedem leitura de tendência: (i) suicídios 58 -> 100 -> 32 -> 13 -> 24; (ii) latrocínio dentro ou fora de "homicídio" conforme o ano; (iii) 2020 coproduzido com Acontece; (iv) 2022 sem anual; (v) 2024 "aprimoramento" sem tabela de reconciliação; (vi) 2025 com campos "não informado" de 33% a 60%; (vii) 2023 inclui feminicídios em "homicídio".

## 2. Validação por amostra (passo 2)

**Universo:** Anexo 3 do relatório 2019 = 329 casos (`pdftotext`; 329/329 linhas casadas; caso 94 sem UF no PDF, UF inferida RR). Fonte por caso: Anexo 4 (308 com link; 21 sem link: "SI", "Mãe da vítima", "Facebook", grupos de WhatsApp).
**Sorteio (feito antes de ler qualquer fonte):** amostra aleatória simples sem reposição, n = 160 (fração 48,6%, FPC 0,72), semente 20261021 (`scripts/s03_sorteio.py`, `dados/amostra.csv`). Dupla codificação: 32 pré-sorteados (semente 20261022), 23 com fonte recuperada.
**Codebook congelado antes de codificar:** `scripts/CODEBOOK.md` (corresponde, morte confirmada, LGBT+ explícito e base, motivo reportado, desfecho). Regra: só vale o que a página diz.
**Coleta:** `scripts/s02_fetch_fontes.py` (HTTP direto; Wayback como fallback; cópias em `fontes/p3-ggb/_raw/news/`, gitignoradas). Páginas de erro com HTTP 200 detectadas em `s04_extrair_texto.py` (404 disfarçado, conta suspensa, home, spam, login do Facebook) e tratadas como "não corresponde".

### Funil (n = 160)

IC de Wilson **sem correção para população finita** (fração amostral 48,6%, FPC 0,72): são conservadores; com FPC ficariam ~28% mais estreitos.

| etapa | k | n | proporção | IC95% Wilson |
|---|---|---|---|---|
| fonte citada recuperada | 106 | 160 | 66,3% | 58,6-73,1% |
| ... que não é a matéria do caso (home, 404, suspensa, login) | 18 | 106 | 17,0% | 11,0-25,3% |
| matéria corresponde ao caso (S ou P) | 88 | 160 | 55,0% | 47,3-62,5% |
| morte violenta confirmada (entre 88) | 73 | 88 | 83,0% | 73,8-89,4% |
| morte indeterminada ou não violenta (entre 88) | 15 | 88 | 17,0% | 10,6-26,2% |
| **verificável estrito (piso)** | **50** | **160** | **31,3%** | **24,6-38,8%** |
| verificável estrito, entre fontes recuperadas | 50 | 106 | 47,2% | 37,9-56,6% |
| verificável estrito, entre matérias que correspondem | 50 | 88 | 56,8% | 46,4-66,7% |
| verificável largo (inclui indício), entre 88 | 54 | 88 | 61,4% | 50,9-70,9% |
| LGBT+ não mencionado na fonte (entre 73 com morte violenta) | 19 | 73 | 26,0% | 17,3-37,1% |

Falhas de recuperação (54): 31 links 404, 12 domínios inacessíveis, 4 bloqueio/erro de servidor, 7 sem link no Anexo 4. Wayback recuperou 6 casos na primeira passada e 5 nas seguintes no universo (respostas 404/429/500 na maioria das tentativas); na amostra, a passada dirigida foi interrompida depois de recuperar 2 casos (o log dessa execução não foi gravado; as contagens vêm dos arquivos). **Link rot de 2019 a 2026 enviesa contra a verificação: "não verificável hoje" não é "falso".**

Projeção ao universo (ilustrativa, só precisão): 31,3% x 329 = ~103 casos (81-128) verificáveis hoje na fonte citada; se a condicional de 56,8% valesse para todo o universo, ~187 (153-219).

### Tabela de motivos (entre 73 com morte violenta confirmada; `dados/tabela_motivos.csv`)

| motivo reportado na fonte | k | % | IC95% |
|---|---|---|---|
| desconhecido / não reportado | 35 | 47,9 | 36,9-59,2 |
| conflito interpessoal (briga, dívida, facção, ponto de prostituição) | 13 | 17,8 | 10,7-28,1 |
| roubo / latrocínio | 13 | 17,8 | 10,7-28,1 |
| passional / ciúmes / ex-parceiro | 6 | 8,2 | 3,8-16,8 |
| LGBTfobia atribuída por alguém na fonte | 3 | 4,1 | 1,4-11,4 |
| suicídio | 3 | 4,1 | 1,4-11,4 |

Entre os 73: tipo homicídio 60, latrocínio 10, suicídio 3. Desfecho reportado: inquérito sem autor 46, preso/apreendido 14, autor identificado foragido 7, suspeito morto 1, não informado 5. Base da identificação LGBT+ nos 50 verificáveis: **imprensa sem atribuir 33 (66%)**, polícia 11, família/amigos 4, autodeclaração 2. Não discuto intenção; meço o que a fonte diz.

### Concordância entre codificadores (23 casos; `dados/kappa.json`)

Codificador A: eu (Claude Sonnet 5.5). Codificador B: Gemini 3.8 Flash (Antigravity, assinatura do fornecedor), cego, pacote sem nomes (`[VITIMA]`), mesmo codebook, janela de texto maior que a minha. Mesma família de modelo daria kappa inflado; por isso outra família.

| variável | n | concordância | kappa |
|---|---|---|---|
| LGBT+ identificado | 21 | 95,2% | 0,91 |
| base da identificação | 21 | 95,2% | 0,92 |
| desfecho | 21 | 95,2% | 0,92 |
| motivo | 21 | 90,5% | 0,85 |
| tipo | 21 | 85,7% | 0,73 |
| correspondência | 23 | 91,3% | 0,64 |
| **morte violenta confirmada** | 21 | 90,5% | **0,46** |

n pequeno: os kappas têm IC largo; tratar como indicação, não como certificação. A fragilidade é "encontrado morto sem causa" (indeterminada x violenta).

### Casos em que a categoria do GGB diverge da fonte

3 divergências de categoria/cidade entre 106 fontes recuperadas (ex.: "travesti" no GGB e "homossexual" na PM; "transexual" no GGB e "homossexual assumido" na cunhada). Fontes que são o próprio memorial TDoR (3) ou post de rede social (6) não são reportagem: o GGB usa fonte secundária em parte dos casos.

## 3. Captura-recaptura (passo 3)

**Listas obtidas:** GGB 2019 trans/travesti (Anexo 3: 89 travestis + 27 transexuais + 2 mulheres trans = 118) x **TDoR/TGEU-TMM Brasil 2019** (139 registros, export oficial do site; 112 violência, 20 suicídio, 5 não classificados, 2 médicos; `fontes/p3-ggb/_raw/tdor/`). Casamento por URL da fonte (54), nome + UF + cidade (27), nome (2 tokens) + UF (7); pares conferidos à mão. **Desvio:** a lista do GGB não traz data, então não há critério de ±3 dias; usei URL, nome e cidade.

| cenário | n GGB | n TDoR | sobreposição | N Chapman (EP) | cobertura GGB |
|---|---|---|---|---|---|
| base | 118 | 139 | 88 | 186,2 (6,0) | 63,4% |
| estrito (URL ou >=2 tokens de nome) | 118 | 139 | 74 | 221,1 (10,6) | 53,4% |
| TDoR só violência + suicídio | 118 | 132 | 87 | 178,9 (5,7) | 66,0% |
| TDoR só violência | 118 | 112 | 77 | 171,4 (6,3) | 68,8% |
| GGB sem casos cuja fonte é o TDoR | 111 | 139 | 82 | 187,9 (6,7) | 59,1% |
| só casos com nome nas duas listas | 96 | 126 | 80 | 151,1 (4,1) | 63,5% |

IC95% do cenário base: 175-198 (normal) e 178-202 (log). União observada: 169 casos distintos.
**Dependência declarada:** (i) TDoR cita a mesma matéria que o GGB em 54 pares; (ii) 7 casos do GGB têm o próprio TDoR como fonte; (iii) o relatório GGB 2020 é produzido com a Acontece ("Fonte e Organização: Acontece LGBTI+; Grupo Gay da Bahia", ✅ lido) e o relatório 2019 lista a Acontece entre os colaboradores (✅ lido); a Acontece é parceira fundadora do Observatório (relatório parcial 2026, ✅ lido) e uma notícia (⚠️ não lida na íntegra) diz que o GGB também o fundou: **tratar GGB x Observatório como par não independente**; (iv) o TGEU obtém dados do Brasil em parte da ANTRA (não confirmei em texto metodológico: ⚠️, ver `fila-aquisicao.jsonl`). Dependência positiva **subestima N** (Feldman et al. 2017, PLOS Medicine, p. 7: "often there is positive list dependence, which leads to underestimated population sizes").
**Não exercido:** modelo log-linear com 3 ou mais listas. A terceira lista nominal possível (ANTRA, "Mapa dos assassinatos") está 404 e o PDF do dossiê 2019 não tem nomes; o Observatório não é independente. Implementar log-linear sem dado seria teatro. **Sem lista de gays e lésbicas independente, a cobertura do GGB para esse bloco (gays, lésbicas e bissexuais: 211 de 329, 64% da lista 2019) é desconhecida.**

## 4. Testes de "inflação" (passo 4)

**(a) Duplicatas e fora de critério na própria lista** (`dados/duplicatas_resumo.json`): 1 par provável de duplicata em 329 (0,3%; mesma pessoa em Itu/SP, "transexual" e "lésbica"); 17 casos sem nome e 31 sem nome ou só com iniciais (9,4%); 9 links com 2 casos (todos eventos de 2 vítimas; um deles registra como "bissexual" o acompanhante morto junto com a travesti, sem que a matéria diga a orientação). Morte **não confirmada como violenta** pela fonte: **15/88 (17%; 10,6-26,2%)** das matérias que correspondem, a saber 13 de causa não informada ou circunstância aberta ("encontrado morto", "morte suspeita"; isso é não confirmado, não fora de critério) e **2 atropelamentos sem indício de intenção** (travesti atropelada ao atravessar rodovia; travesti atropelada por viatura da PM em investigação), que ficam fora do critério que o próprio GGB declara para atropelamento ("O atropelamento foi incluído no cômputo das tipificações, devido ao ato ter sido intencional", relatório 2019, p. 61 do PDF). O GGB declara 158 descartes e 58 retiradas (2019): há filtro, e também há inclusão por inferência.

**(b) Contagem por UF (27 UFs, ecológico, não causal)** (`dados/uf_2019.csv`, `dados/inflacao_uf_serie.json`; internet = % de domicílios com uso de internet, PNAD Contínua TIC 2019, SIDRA 7307; população SIDRA 6579; homicídio = Atlas/SIM; fontes IBGE gravadas com sha256 em `fontes/p3-ggb/ibge/`):

| associação | rho (Spearman) | p (permutação) |
|---|---|---|
| GGB (n) x população | 0,85 | <0,001 |
| GGB por milhão x internet | **-0,43** | 0,028 |
| GGB por milhão x taxa de homicídio | 0,39 | 0,048 |
| GGB por milhão x Sinan campo 55 LGBTfobia por milhão | 0,11 | 0,60 |
| taxa de homicídio x internet | -0,51 | 0,007 |

Poisson com offset de população e erro robusto (HC0): internet sozinha IRR 0,78 por DP (0,68-0,89); internet + homicídio: internet 0,98 (0,83-1,16), **homicídio 1,33 (1,13-1,57)**; sobredispersão 1,8-2,4. Leitura: a distribuição por UF acompanha a violência geral; "mais internet, mais GGB" não aparece. Ressalva: n = 27, uma única edição, confusão ecológica.

**(c) Série anual** (`dados/serie_ggb_vs_cobertura.csv`): GGB 130 (2000) -> 445 (2017) (x3,4) -> 257 (2025). Uso de internet (PNAD C, 10+ anos): 66,0% (2016) -> 90,5% (2025); 2020 não existe. Sinan campo 55 LGBTfobia (notificações, não mortes): 948 (2015) -> 2.410 (2025) (x2,5; corrigido em 2026-10-24: a versão anterior somava as 27 UFs e a linha nacional BR e mostrava 1.896 -> 4.820, o dobro; razão e correlações não mudam), correlação 0,98 com internet em 2016-2025 (padrão de cobertura/notificação), ao passo que o GGB tem rho -0,82 com internet (n=9) e -0,57 com o Sinan (n=11). **O crescimento 2000-2017 do GGB é compatível com cobertura crescente (não testei: sem série de internet por UF antes de 2016), e é justamente o período em que o dossiê cita +253% (Mendes & Silva); só desde 2017 a série não acompanha nenhuma das duas coberturas.** Descritivo, n pequeno; não é refutação do efeito cobertura no período de alta.

**(d) Sensibilidade da manchete** (`dados/sensibilidade_manchete.csv`): A = todas as mortes violentas; B = sem suicídios; C = homicídio estrito (sem latrocínio e outras). 2019: A 329, B 297 (0,90), C 272 (0,83). 2021: A 300, B 276, C 242 (0,81). 2023: A 257, B 237, C 204 (0,79). 2025: A 257, B 237, C 204 (0,79). **A manchete não muda de sinal** (2017->2025: -42% em A, -39% em B; 2019->2020: -28% A, -25% B, -21% C), mas 2017->2018 vale -5,6% em A e -17% em B, porque os suicídios foram de 58 para 100. "Só com LGBTfobia atribuída na fonte" em 2019: 4,1% dos casos com morte violenta confirmada (1,4-11,4%) numa amostra de 73; **projetar isso para 329 daria ~13 casos e é ilustrativo apenas** (não é contagem de crimes de ódio: a ausência de atribuição na matéria não é ausência de motivação).

## 5. Literatura Q1 (passo 5), com a profundidade de leitura declarada

Ledger: `lit/sources.jsonl`; arquivos: `lit/00-material-fonte/` e `fontes/q1-textointegral/`. Quartis: tabelas locais `fontes/scimago/quartis-sjr-2026-10-10.md` e `...-10-11.md`. "Lido" = texto principal lido; o que ficou só escaneado está dito.

| obra | periódico (quartil) | profundidade | o que sustenta aqui | sha256 (16) |
|---|---|---|---|---|
| Feldman JM et al. 2017. Quantifying underreporting of law-enforcement-related deaths... capture-recapture. DOI 10.1371/journal.pmed.1002399 | PLOS Medicine (Q1) | **lido**: resumo, introdução, métodos, resultados e discussão; tabelas 1, 2, 3 e 5 lidas; tabelas 4, 6 e 7 (regressões) só escaneadas | (i) lista de mídia (The Counted) captou 93,1% (IC 91,7-94,2) das mortes por intervenção legal nos EUA em 2015, o registro vital 44,9%; (ii) Chapman/Poisson de 2 listas supõe independência; "often there is positive list dependence, which leads to underestimated population sizes" (p. 7); sensibilidade com correlação a priori até 0,93 (p. 12); (iii) **antes de comparar, os autores excluíram 60 de 1.146 casos da lista de mídia (5,2%) que não cabiam na definição** (atropelamentos acidentais, violência doméstica, mortes em custódia sem mecanismo claro; Tabela 2, p. 8): o GGB não faz o equivalente (suas manchetes incluem suicídio, atropelamento, latrocínio); (iv) casamento com o registro oficial por nome, ano de nascimento, estado e data (+-4 dias): 91,3% casaram (p. 6-7); (v) limites: não examinam o que a mídia não captou, cobertura rural menor (p. 13-14), pressupostos de independência. O estudo é de **eventos com definição estrita** (policial matou); não se transfere sem ressalva a "pessoa LGBT+ morta", em que a própria identidade depende da mídia | f91c1c5bfedcdb72 |
| Dinno A. 2017. Homicide rates of transgender individuals in the US: 2010-2014. DOI 10.2105/AJPH.2017.303878 | AJPH (Q1) | **lido**: resumo, introdução, métodos, resultados e discussão com limitações; apêndice A e planilhas suplementares não lidos | numeradores = TDoR e NCAVP, "compilation of media reports"; denominadores supostos 0,10%, 0,35%, 0,60%; taxa de 3,66 a 110 por 100 mil conforme prevalência e subnotificação (1 em 5, 1 em 2, 4 em 5); "My findings were sensitive to the assumed prevalence" (Limitations); sensibilidade, não ponto | a10198ea3d99eddc |
| Krieger N et al. 2015. Police killings... can be counted. DOI 10.1371/journal.pmed.1001915 | PLOS Medicine (Q1) | **lido** (ensaio de 7 páginas) | **ensaio de política**, não validação: argumenta contagem por mídia onde o Estado não conta e propõe notificação compulsória; não mede viés de lista | 5873048b46b5e638 |

Não obtidos (escada legítima esgotada; `fila-aquisicao.jsonl`): Lum, Price e Banks 2013 (Am Stat, Q1), Chao et al. 2001 (Stat Med, Q1), Earl et al. 2004 (Annu Rev Sociol, quartil=nao_verificado), IWGDMF 1995 (AJE, quartil=nao_verificado); documento metodológico do TMM/TGEU; NCAVP. **Lacuna que importa:** não li nenhuma validação empírica de lista de ONG de mortes LGBT+ contra registro oficial; Feldman 2017 é o análogo mais próximo (mídia x registro vital, polícia), e nele a lista de mídia **superou** o registro oficial em cobertura, mas com definição estrita, alinhamento prévio de critérios e pareamento individual com o registro, que o GGB não tem.

## 6. O que o autor pode afirmar e o que não pode

**Pode** (cada item com número e arquivo):
- "O relatório 2019 do GGB tem 329 casos nominais com uma fonte por caso (`dados/ggb2019_universo_hash.csv`). Em amostra aleatória de 160, lida hoje, 31% (IC 25-39%) têm fonte que confirma morte violenta e identifica a vítima como LGBT+; 57% (IC 46-67%) quando a fonte citada é de fato a matéria do caso; 34% das fontes não puderam ser recuperadas." (`dados/resultados.csv`)
- "Nas fontes citadas, a LGBTfobia é atribuída como motivo em 4% dos casos de morte violenta (IC 1-11%); em 48% o motivo é desconhecido; roubo/latrocínio e conflito pessoal somam 36%."
- "O GGB declara critério largo (inclui suicídio, latrocínio, atropelamento, heterossexuais confundidos, profissionais do sexo trans) e adota denominador >10% da população."
- "Não há evidência de duplicação relevante (0,3%) nem de que a contagem por UF acompanhe a cobertura de internet; ela acompanha a violência geral."
- "Para travestis e mulheres trans em 2019, 63% (53-69% conforme o cenário) do total conhecido por duas listas está na lista do GGB: subcobertura relativa, não inflação, nesse recorte."
- "Os números 2023-2025 do GGB não têm lista pública; não são auditáveis."

**Não pode**:
- "O GGB infla/fabrica casos" (nenhum teste mostrou isso; 54 das 160 fontes estão mortas ou ausentes e em 19 dos 73 casos de morte confirmada a fonte não menciona orientação: é limite de verificação, não prova de falsidade).
- "O GGB é preciso" ou "cobre X% das mortes LGBT+ do Brasil" (cobertura só estimável para trans, como piso, com listas dependentes).
- Qualquer **taxa** ou "país que mais mata" com o GGB como numerador (denominador >10% do próprio GGB; PNS 1,89%).
- Qualquer **tendência** 2017-2025 (quebras de composição e de critério, seção 1).
- Generalizar 2019 para 2023-2025.
- Chamar a contagem de "crimes de ódio": 4% de atribuição explícita na fonte, 48% de motivo desconhecido.
- Dizer que o Observatório "confirma" o GGB (não é independente).

## 7. Limites

1. Um ano (2019) e uma fonte por caso: o que o GGB sabia na época pode estar além do link; link morto não é falsidade.
2. A codificação é minha (Sonnet 5.5) com dupla codificação cega em 23 casos (Gemini 3.8 Flash); kappa moderado em "morte confirmada". Dos 18 casos sem matéria utilizável, 13 "não correspondem" (6 home pages, 6 erro 404 ou conta suspensa, 1 spam) e 5 são inverificáveis (login do Facebook): pode haver matéria correta atrás deles.
3. Busca suplementar para os 19 casos "fonte silenciosa" (fora, outra fonte identifica a vítima como LGBT+?): tentei 8 por WebSearch; a ferramenta descartou o nome da consulta e nada foi conclusivo. **Não exercido** (`fila-aquisicao.jsonl`, `fonte-silenciosa-19-casos`, com os ids).
4. Captura-recaptura: duas listas dependentes, só trans, sem data; N é piso.
5. Testes por UF: n = 27, ecológico, uma edição de PNAD TIC.
6. Wayback instável (404/429/500): parte dos links mortos pode estar arquivada.
7. Caso 94 do Anexo 3 sem UF no PDF (inferida RR); `Bisexual` x `Bissexual` normalizados na contagem.

## 8. Reprodução

`/opt/homebrew/bin/python3.14 -I <script>` (stdlib + numpy; semente fixa):
`s01_parse_ggb2019.py` (extrai Anexos 3 e 4) -> `s02_fetch_fontes.py`, `s02b_wayback_retry.py` -> `s03_sorteio.py` -> `s04_extrair_texto.py` -> `s05_visualiza_lote.py`, `s05b_frases.py` (leitura para codificar) -> `s06_pacote_codificador_B.py` -> `s11_validacao.py` (resultados, kappa) -> `s08_captura_recaptura.py` -> `s09_uf_series.py` -> `s10_duplicatas.py` -> `s12_metodologia_paginas.py` -> `s13_sensibilidade_manchete.py` -> `s14_leak_check.py` (garante que nenhum nome de vítima saiu de `_raw`).
Nomes: só em `fontes/p3-ggb/_raw/` (confirmado gitignorado em `.gitignore do projeto privado`, linha 293). Saídas públicas usam id hash (sha256 com sal em `_raw/salt.txt`, 10 hex).

Arquivos desta frente (`research-2026-10-21-rodada3/F3-ggb/`):
- `dados/codificacao_A.csv` (planilha de codificação, ids hash), `dados/resultados.csv`, `dados/tabela_motivos.csv`, `dados/kappa.json`, `dados/validacao_resumo.json`, `dados/amostra.csv`
- `dados/captura_recaptura_trans2019.json`, `dados/captura_recaptura_sensibilidade.json`, `dados/cr_ggb_trans_hash.csv`
- `dados/uf_2019.csv`, `dados/serie_ggb_vs_cobertura.csv`, `dados/inflacao_uf_serie.json`, `dados/sensibilidade_manchete.csv`, `dados/duplicatas_resumo.json`, `dados/duplicatas_candidatas_hash.csv`, `dados/metodologia_trechos.csv`
- `dados/ggb2019_universo_hash.csv`, `dados/fetch_log.csv`, `dados/fonte_checks.csv`
- `sources.jsonl` (ledger GGB/ANTRA), `lit/sources.jsonl` (ledger literatura), `fila-aquisicao.jsonl`
- `scripts/` (14 scripts + `CODEBOOK.md`)
