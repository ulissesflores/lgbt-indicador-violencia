# MIDIA: quantas vezes circulam 4 famílias de afirmação sobre mortes de LGBT (2015 a 2026-10-21)

Pasta: `research-2026-10-21-rodada3/discurso/midia/`. Pré-registro: `PRE-REGISTRO.md` (corpo gravado 2026-10-22T21:37:13Z, sha256 `1d1856c0...40b`, cópia exata em `PRE-REGISTRO.original.md`; tudo que mudou depois está nos ADENDOS, A1 a A8). Brutos fora do git: `fontes/q1-textointegral/discurso/midia/`. Contagem mede circulação, não validade.

## 1. Resposta
- **Não consegui medir "quantas vezes vemos" na imprensa.** O GDELT responde sem cadastro, mas devolve 429 a quase todo pedido deste IP e `{}` no controle positivo em português: só saíram as séries de controle em inglês e espanhol (beco, ver §3.5). O único universo completo é o **Parlamento**: 219.562 discursos da Câmara + 38.449 pronunciamentos do Senado (piso, ver §3.1).
- Parlamento: F1 em 14 falas, F2 em 56, F3 em 148, F4 em 2 (de 258.011). **F1 e F2 são quase só um bordão**: 13 das 14 falas F1 tratam da expectativa de vida do grupo (11 dão "27 a 36 anos" para pessoas trans) e 49 das 56 falas F2 afirmam ou atribuem "o Brasil é o país que mais mata". **Nenhuma cita fonte primária com denominador (0/14 e 0/49); 7 das 49 de F2 nomeiam GGB, ANTRA, TGEU ou o Observatório (contagens de ONG por mídia)**. F3 no Parlamento não é uma só acusação: das 33 falas que afirmam, 18 acusam governo, bancada ou instituição brasileira, 4 falam de extermínio por pastor ou sociedade, 10 acusam regimes ou grupos estrangeiros e 1 inverte a vítima; 10 rebatem.
- Pela amostra codificada de imprensa e literatura, a maior parte do que o dicionário recupera NÃO é a afirmação (só 0% a 22% dos itens de imprensa e 0% a 18% da literatura afirmam ou relatam a alegação, ver §4). O número bruto de imprensa/literatura sem a proporção ao lado engana.
- Veredito: F1 não sustentada como frase geral e **não testável no Brasil**; F2 sustentada só em parte (contagem absoluta de ONG por mídia, nunca taxa nem ranking provado); F3 sustentada só em parte (retórica e cortes documentados; extermínio e perseguição por agentes do Estado em 2016-2024 não achados); F4 não sustentada nas formas fortes.

## 2. Universos pedidos x entregues
| universo | status | o que há | limite principal |
|---|---|---|---|
| GDELT DOC 2.0 | **beco parcial** | só controles EN/ES (série diária 2017-2026) | 429 em quase tudo; sem 2015-2016 ("Invalid query start date"); PT `{}`; união de entradas impossível (A1) |
| Google News RSS (fallback, A2) | piso | itens únicos por link, 2015-2026 | ≤ ~100 por consulta; o filtro de data NÃO foi respeitado (no teste de F2 pt, 87% dos itens têm ano diferente do da célula; ano = data de publicação); só título |
| Câmara + Senado | completo exceto 111 janelas e Senado só por resumo | 258.011 falas | A3, A4; Senado: texto integral só de 375 candidatos |
| OpenAlex (título+resumo) | completo | 4 famílias, por ano | volume de tema, não de afirmação (F1 = 94% suicídio) |
| Wikipédia pt/en/es | frase exata, retrato do dia | 14 entradas | sem série; ES traz James Bond |
| CIDH, ONU, HRW, Anistia, MDH | **não contado** | tentativa de busca direta | 403/404/302/JavaScript; em `fila-chrome.jsonl` (a coordenação do projeto decide) |

## 3. Contagens (arquivo `contagens.csv`: família, universo, ano, n, consulta, data_acesso, sha256)
### 3.1 Parlamento (dicionário v2 corrigido, A3; v1 literal do pré-registro: F1 23, F2 161, F3 692, F4 4, inflado por `trans` sem fronteira e por F3-PT-04 sem o grupo)
| | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| falas (denominador) | 28278 | 23479 | 30693 | 18251 | 23916 | 16347 | 26920 | 18948 | 21776 | 17364 | 21894 | 10145 | 258011 |
| F1 | 0 | 0 | 2 | 2 | 3 | 2 | 0 | 1 | 3 | 0 | 0 | 1 | 14 |
| F2 | 3 | 3 | 10 | 0 | 15 | 1 | 4 | 6 | 11 | 1 | 0 | 2 | 56 |
| F3 | 6 | 10 | 32 | 8 | 22 | 6 | 6 | 10 | 23 | 6 | 14 | 5 | 148 |
| F4 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
\*até 21/10. O filtro `requer` do v2 em F3-PT-04 ("governo|bolsonaro|..." em qualquer ponto do texto) quase não filtra discurso parlamentar; a precisão de F3 vem da amostra (§4), não do filtro. Câmara: F1 14, F2 50, F3 137, F4 2; Senado: F2 6, F3 11. Pontos altos de F2 coincidem com 17 de maio (Dia contra a Homofobia) e 8 de março; não testei causa. Perdas conhecidas: ≤ 5,1% da Câmara (A4); Senado é piso.

### 3.2 Imprensa (Google News RSS, itens únicos por link; PISO; precisão no §4)
| | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 pt | 7 | 12 | 11 | 10 | 18 | 11 | 18 | 15 | 13 | 11 | 9 | 10 | 145 |
| F1 mundo | 44 | 47 | 58 | 54 | 24 | 62 | 65 | 75 | 71 | 82 | 56 | 53 | 691 |
| F2 pt | 12 | 33 | 73 | 76 | 48 | 74 | 157 | 133 | 112 | 82 | 94 | 111 | 1005 |
| F2 mundo | 4 | 10 | 12 | 14 | 18 | 30 | 18 | 18 | 11 | 10 | 11 | 8 | 164 |
| F3 pt | 18 | 13 | 134 | 50 | 56 | 38 | 28 | 37 | 74 | 42 | 41 | 35 | 566 |
| F3 mundo | 4 | 9 | 17 | 46 | 56 | 29 | 28 | 34 | 21 | 16 | 31 | 70 | 361 |
| F4 pt | 1 | 3 | 9 | 7 | 8 | 10 | 5 | 6 | 18 | 9 | 17 | 47 | 140 |
| F4 mundo | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | 1 | 3 | 2 | 10 |
Por entrada, F3 pt: "cura gay" 550 de 566; "extermínio/genocídio" 2; "licença para matar" + grupo 14; governo/Bolsonaro + perseguição e "quer matar/eliminar" 0 (as consultas não devolveram nada). F2 pt: "país que mais mata" + grupo 46; "a cada N horas" 115 (muito ruído). Fontes mais frequentes (itens únicos, piso, antes de qualquer filtro de precisão): F2 pt O Globo 48, G1 42, UOL 26, CartaCapital 24, Observatório G 24, CNN Brasil 23, Esquerda Diário 22, Agência Brasil 20; F3 pt O Globo 42, G1 34, UOL 27, Folha 24, Notícias da TV 23. Não é série temporal: o recorte da lista pelo Google e a cobertura de fontes mudam com os anos; o pico de F3 pt em 2017 (134) é o caso "cura gay" (liminar de setembro). Não use como tendência.

### 3.3 Literatura (OpenAlex, título+resumo, 2015-2026-10-21; 21 pedidos, cerca de US$ 0,03)
| | total | 2015 | 2019 | 2023 | 2025 | maior consulta |
|---|---|---|---|---|---|---|
| F1 | 5535 | 279 | 393 | 540 | 595 | suicídio + grupo: 5190 |
| F2 | 270 | 4 | 29 | 34 | 33 | cita "Grupo Gay da Bahia": 70; ANTRA/TMM/TGEU + grupo: 121 |
| F3 | 622 | 17 | 60 | 60 | 64 | extermínio/genocídio + grupo: 358; "cura gay"/terapia de conversão + Brasil: 46 |
| F4 | 369 | 13 | 24 | 51 | 28 | homofobia + mito/negação: 276 |

### 3.4 Wikipédia (páginas com a frase exata, 2026-10-22)
F1 0 (3 frases PT, 1 EN, 1 ES); F2 9 (pt 8, en 1: "país que mais mata" em Apolo, Transfeminicídio, Direitos LGBT no Brasil etc., quase todas em citação de manchete); F3 197 (cura gay pt 67; ES 120, quase todas James Bond ou "cura" = padre); F4 0.

### 3.5 GDELT
Controle positivo EN ("homophobia", 2017-2026): 53.861 artigos em 2017 e 4.888 em 2025, mas o total monitorado cai de 227,8 M para 56,0 M no mesmo filtro: contagem bruta de GDELT não é tendência. PT: `sourcelang:portuguese` devolveu `{}`. Ver `_gdelt_resultados.jsonl`, `gdelt_sonda.log`.

## 4. Amostra codificada (`amostra_codificada.csv`, 871 itens, semente 20261022; 1 codificador; recodificação de 20: 19 iguais, não cega)
AFIRMA+ATRIBUI = o texto afirma ou relata a alegação; N estimado = N do universo x proporção (IC95 de Wilson). "Fonte primária" = documento/dado com nome e ano localizável; "GGB/ANTRA/TGEU/ONU" = nomeado no trecho.
| fam | universo | N | amostra | afirma+atribui | N estimado [IC95] | rebate | primária | cita GGB/ANTRA/TGEU/ONU |
|---|---|---|---|---|---|---|---|---|
| F1 | Parlamento | 14 | 14 (censo) | 14 | 14 | 0 | 0/14 | 0/14 |
| F1 | imprensa pt (título) | 145 | 60 | 2 | 5 [1-16] | 0 | 0/2 | 0/2 |
| F1 | imprensa mundo (título) | 691 | 60 | 5 | 58 [25-125] | 1 | 1/5 | 0/5 |
| F1 | OpenAlex | 5535 | 60 | 4 | 369 [145-881] | 0 | 4/4 (o próprio estudo) | 0/4 |
| F2 | Parlamento | 56 | 56 (censo) | 49 | 49 [43-53] | 2 | 0/49 | 7/49 |
| F2 | imprensa pt (título) | 1005 | 60 | 13 | 218 [132-338] | 1 | 0/13 | 0/13 |
| F2 | imprensa mundo (título) | 164 | 60 | 8 | 22 [11-40] | 0 | 0/8 | 1/8 |
| F2 | OpenAlex | 270 | 60 | 11 | 50 [29-81] | 0 | 0/11 | 7/11 |
| F2 | Wikipédia | 9 | 9 (censo) | 9 | 9 | 0 | 0/9 | 0/9 |
| F3 | Parlamento | 148 | 60 | 33 | 81 [63-99] | 10 | 0/33 | 0/33 |
| F3 | imprensa pt (título) | 566 | 60 | 0 | 0 [0-34] | 0 | n/a | n/a |
| F3 | imprensa mundo (título) | 361 | 60 | 7 | 42 [21-80] | 0 | 0/7 | 0/7 |
| F3 | OpenAlex | 622 | 60 | 5 | 52 [22-112] | 0 | 1/5 | 0/5 |
| F4 | Parlamento | 2 | 2 (censo) | 2 | 2 | 0 | 0/2 | 0/2 |
| F4 | imprensa pt (título) | 140 | 60 | 3 | 7 [2-19] | 2 | 0/3 | 0/3 |
| F4 | OpenAlex / imprensa mundo | 369 / 10 | 60 / 10 | 0 / 0 | 0 [0-22] / 0 | 0 | n/a | n/a |
"Cita GGB/ANTRA/TGEU/ONU" = nomeado no trecho como fonte da frase (a co-menção por regex no texto todo é maior: F2 Parlamento 8 de 56, F1 1 de 14 por citar o TGEU em outro ponto da fala). Imprensa só por título: "fonte" só conta se o título a nomeia (piso). F3 Parlamento: 33 = 18 governo/bancada BR + 4 pastor/sociedade + 10 regimes ou grupos estrangeiros + 1 inversão. F3 imprensa pt: 53 de 60 são notícias sobre "cura gay" (decisão judicial de 2017, projetos de lei, relatos pessoais), 0 acusam governo de matar ou perseguir. Wikipédia F3: 16 de 60 mencionam, 1 afirma.

## 5. Cadeia de citação até a fonte primária
- **F1** ("expectativa de vida trans 27/32/33/35/36 anos"): 13 falas (11 com número); só 2 nomeiam algo: "CELGBT" (conselho estadual, sem documento) e "Observatório dos Direitos Humanos". A fala de 30/08/2017 traz o par 35 anos x 74,9 anos, o mesmo par que o **dossiê da ANTRA** escreve: "Apesar de não haver estudos sistemáticos sobre a expectativa de vida das travestis e transexuais femininas, Antunes (2013) afirma que a expectativa de vida desta população seja de 35 anos de idade, enquanto a da população brasileira em geral, é de 74,9 anos (IBGE 2013)" (ANTRA 2019, `fontes/p3-ggb/_raw/txt/antra2019.txt` l.1302-1304, sha256 `68b2aa85...dadef`; idêntico em `antra2018.txt` l.626-636, sha256 `aa1f257d...a8e1`). Ou seja, a cadeia termina em uma única autora citada (Antunes 2013), que a própria ONG diz não ser estudo sistemático; o 27 e o 36 não aparecem nesses textos. O Portal VIVA (29/01/2026, Alexandre Barreto, ⚠️ 1 fonte secundária que li, não primária) diz: "os 35 anos frequentemente citados na mídia dizem respeito à média de idade das vítimas assassinadas no Brasil, e não à expectativa de vida"; atribui 69 anos ao dossiê 2026 da Rede Trans Brasil (cruzamento de título de eleitor e nome social). Não verifiquei a ANTRA.
- **F2**: fontes nomeadas nas 56 falas: Procuradora Federal dos Direitos do Cidadão (fala de 17/05/2017), Disque Defesa Homossexual 2012 + GGB + ANTRA + TGEU (17/05/2017), GGB 2013 (21/05/2015), "um grupo da Bahia" (17/05/2023), Observatório de Mortes e Violências contra LGBTI+ (17/05/2022). Todas terminam em **contagens declaradas por mídia**; nenhuma em dado com denominador.
- **F3**: nenhuma das 33 falas que afirmam cita documento; os fatos institucionais (liminar de 2017, projeto de 2011 apelidado "cura gay", Decreto 9.883/2019) são citados sem número.
- **F4**: as 2 falas e as manchetes (Gazeta do Povo 01/03/2019 "Os verdadeiros números sobre a morte de LGBTs", 02/02/2021 e 25/06/2023) não trazem série oficial alternativa no trecho.

## 6. Veredito por família (só o que o dossiê, F3, GGB-completo, mortalidade, governos ou o que li sustentam)
**F1 "gays/LGBT morrem mais que héteros": não sustentada como frase geral; não testável no Brasil.** `discurso/mortalidade/MORTALIDADE.md` §1: nenhum governo registra orientação no óbito; excesso real de HIV pré-1996 e de suicídio (óbito) em parceria registrada na Dinamarca/Suécia (razão 2 a 3, em queda); mortalidade geral de gays "ora elevada, ora nula"; trans com excesso em coortes clínicas (razão 1,4 a 4); homicídio sem taxa em lugar nenhum. SIM 2023-2024: 87 campos, nenhum de orientação. Tentativa de suicídio mais frequente (RR 2,47) não é "morrem mais". Vitimização não fatal: PNS 2019 OR 2,52 (IC95 2,08-3,07) para LGB+ (dossiê). "35 anos" é tema de F1 mais citado: a ANTRA 2018/2019 o apresenta como afirmação de Antunes (2013) "sem estudos sistemáticos" e o VIVA (⚠️) o chama de média de idade das vítimas; sem fonte primária localizada, **não testável**. Variante da outra ponta: "no Governo Lula morreram mais ... homossexuais" (Luiz Lima, 14/07/2026, cita Atlas, Anuário, MJSP, Min. Saúde): não testável, o óbito não registra orientação e o dado oficial por governo não é comparável (`governos/GOVERNOS.md`, resposta 5).
**F2 "país que mais mata LGBT/trans": sustentada só em parte.** Parte sustentável: listas de ONG por mídia contam mais mortes trans no Brasil em número absoluto (a fala de 07/07/2017 já diz "em números absolutos"). Não sustentável: taxa ou ranking mundial para LGBT/gays. GGB-completo `perfil/GGB-O-QUE-E.md` §7 "Não pode: taxa ou 'país que mais mata'"; Truco/Agência Pública 29/08/2018: ranking mundial "impossível de provar"; o TMM/TDoR Brasil cita GGB/Homofobia Mata em 72-94% dos registros de 2013-2018 (`series/analises.md`), logo não confirma o GGB de forma independente; o dossiê marca o "no topo há 18 anos" do TGEU como NÃO VERIFICADO na fonte. "A cada N horas" é a divisão do total anual do GGB (inclui suicídio e latrocínio).
**F3 "governo de direita/Bolsonaro mata, persegue, quer eliminar": sustentada só em parte.** Em 2016-2024 não há ato de perseguição por agentes do Estado nem política de extermínio achados (negativo enumerado, `governos/GOVERNOS.md`); há retórica hostil (Bolsonaro 2019), omissão/corte (Decreto 9.883/2019, verba) e ação protetiva (Dilma 2016, Lula 2023). A CNV documenta perseguição na ditadura e diz: "Não houve uma política de Estado formalizada ... de exterminar os homossexuais" (p. 301). A "cura gay" de 2017 foi decisão de um juiz federal, não de governo. **Os dois flancos usam o mesmo molde:** das 33 falas que afirmam, 18 acusam governo, bancada ou instituição brasileira ("Quer-se retirar tudo isso", 26/09/2023; "estimula a violência contra ... a comunidade LGBT", 01/06/2022), 4 falam de extermínio por pastor ou sociedade, 10 acusam regimes ou grupos estrangeiros ("Fidel Castro matava e perseguia homossexuais em Cuba", 05/12/2023; Irã, Hamas) e 1 inverte ("quem são perseguidos somos nós"); 10 falas rebatem ("Falou-se tanto que o Presidente Bolsonaro ia perseguir, matar gays, mas ele cumpriu toda a Constituição", 14/08/2024). Cuba (UMAP) e a Espanha de Franco têm perseguição documentada em fonte primária (`governos`).
**F4 "não existe homofobia / dado inventado": não sustentada nas formas fortes; sustentada na forma fraca.** "Homofobia não existe": falsa para vitimização (PNS 2019, OR 3,00 para violência física, 14,70% x 3,82%). "Dado inventado": o F3 do GGB mediu duplicata 0,3% e sem sinal de inflação por internet; o que se sustenta é "contagem declarada de mídia, inclusão ampla, não é taxa nem crime de ódio comprovado" (31,3% verificáveis em 2019, piso; LGBTfobia atribuída na fonte em 4,1%). Falas: "dados manipulados e não oficiais de mortes de homossexuais, como se todas as mortes tivessem como causa a homofobia, o que é mentira" (Otoni de Paula, 26/03/2019); "sem vitimismo! Qualquer coisa agora é homofobia aqui" (Bibo Nunes, 26/06/2019).

## 7. O que pode e o que não pode ser afirmado sobre "quantas vezes vemos"
**Pode:** (1) em 258 mil falas da Câmara e do Senado (2015-10/2026), 56 trazem a frase "país que mais mata" e 14 trazem "expectativa de vida" de grupo LGBT, 49 e 14 afirmando ou relatando; 0 com documento verificável; (2) várias falas F2 caem em 17 de maio e 8 de março (não testei causa); (3) na imprensa PT recuperada (piso, só título), ~218 [132-338] dos 1005 itens afirmam F2 (22%), e nenhum dos 60 de F3 acusa governo de matar; (4) a literatura em título/resumo sobre F2 cita o GGB em 70 obras e ANTRA/TMM/TGEU em 121, sem validação independente.
**Não pode:** número de vezes que uma pessoa vê a afirmação (TV, rádio, redes, WhatsApp e YouTube não foram medidos); tendência temporal na imprensa (GDELT bloqueado, Google News sem filtro de data válido); comparação de frequência entre os dois flancos (dicionários de tamanhos diferentes); prevalência na população; "a afirmação é verdadeira porque circula" ou "falsa porque circula pouco".

## 8. Limites e becos
- Um codificador, mesma sessão, recodificação não cega. Imprensa codificada pelo título. Sobreposição: um discurso pode contar em duas famílias.
- Beco GDELT: fila parada em 2026-10-23 ~15:25 (hora local, UTC-3); `_gdelt_resultados.jsonl` tem 4 linhas = controles EN e ES (séries) + 2 corpos `{}` (F1-PT-01 e controle PT, não lidos como zero). 429 persistente neste IP (`gdelt_tentativas.err.log`: 429 na fila final, pedidos espaçados de 5 min; `gdelt_sonda.log`: 4 sondas, 1 aberta por minutos), sem chave e sem contato; volta se a API liberar o IP. Beco organismos: ver `fila-chrome.jsonl`.
- Arquivos: `contagens.csv`, `amostra_codificada.csv` (871), `scripts/` com `SHA256SUMS`, `SHA256SUMS-brutos.txt` (9.259 brutos), `_estimativas.txt`, `_estatisticas_amostra.txt`, `_recode_resultado.json`, `sources.jsonl`.
