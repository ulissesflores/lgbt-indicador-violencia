# GOVERNOS: o que as evidências mostram sobre "governo de direita que tira ou mata homossexuais" (e a simétrica à esquerda)

Rodada 3, frente discurso/governos, 2026-10-22. Pasta: `research-2026-10-21-rodada3/discurso/governos/`. Brutos (fora do git): `fontes/q1-textointegral/discurso/governos/`.
Regras escritas antes de classificar: `PRE-REGISTRO.md` (sha256 do texto pré-registrado em `PRE-REGISTRO.sha256`, gravado 2026-10-22T21:29:37Z; tudo que mudou depois está no ADENDO, A1 a A11). Dados por linha: `paises.csv` (30 linhas, 68 citações verificadas por código), `u3_65_criminalizam.csv`, `brasil_itens.csv` (16 itens, 21 citações verificadas), `brasil_dados_governo.csv`. Ledger: `sources.jsonl` (53). Sem contato com ninguém; só fonte pública sem login.

## Resposta

1. **Existe governo que mata ou persegue homossexuais por política de Estado? Sim, mas a evidência de execução é bem mais fraca que a de lei.** Lei com pena de morte para atos consensuais: 7 Estados da ONU (Brunei, Irã, Mauritânia, Nigéria [12 estados do norte], Arábia Saudita, Uganda, Iêmen) e mais 5 sem certeza jurídica (Afeganistão, Paquistão, Catar, Somália, Emirados), pelo banco da ILGA em 2026-10-22. Todas as execuções que achei são **contagem declarada** (ILGA, IHRDC, Monash, Amnesty): nenhum documento da ONU lido confirma uma execução por ato consensual. Uganda 2023 tem a lei e nenhuma execução achada; Brunei diz ter moratória de fato.
2. **Perseguição documentada por fonte primária:** Chechênia 2017 (detenção e tortura "confirmadas" pela OSCE e reconhecidas pelo TEDH em Lapunov; mortes só "alegadas"), Espanha de Franco (a Ley 20/2022 reconhece a repressão), Cuba (UMAP, trabalho agrícola forçado) e Brasil 1964-85 (CNV).
3. **Relação com o eixo esquerda-direita: fraca e quase sempre indeterminável.** Em 2025 (V-Dem), dos 12 Estados com pena de morte, 6 são autocracias fechadas, 4 autocracias eleitorais, 1 democracia eleitoral (Nigéria, e só em 12 estados; era autocracia eleitoral em 2021-24) e Brunei não tem dado; 7 têm executivo sem partido (Líder Supremo, rei, Talibã, emir, conselho): `não aplicável`. Dos classificáveis, Uganda sai centro-direita (econômico) e Nigéria centro-esquerda. Os partidos da extrema direita (Franco, FET: econ 6) e da extrema esquerda (PCUS e PCC: econ 0) têm a mesma nota na igualdade LGBT: 0, "opõe-se fortemente". O regime pesa mais que o eixo: dos 65 Estados que criminalizam, 44 são autocracias; 70% das autocracias fechadas criminalizam contra 3% das democracias liberais.
4. **Brasil:** a CNV documenta perseguição de Estado em 1964-85 (e nega política formal de extermínio). Em 2016-2024 não achei, em nenhum governo, ato de perseguição por agentes do Estado nem política de extermínio (T5/T6). O que há: retórica hostil (Bolsonaro 2019), omissão ou corte (Dilma 2011 e a verba que cai desde 2015, Temer 2017, Decreto 9.883/2019, verba baixa em 2025) e ação protetiva (Dilma 2016, Lula 2023). "Não achei" vale para o espaço de busca enumerado abaixo, não prova inexistência.
5. **Dado oficial por governo não permite comparar governos** (seção 3.2): a contagem sobe com o volume de notificações, a Disque 100 cai 49,8% em 2019 e sobe 54% em 2023 sem explicação do relatório, e o óbito não registra orientação.

## 1. Mundo: leis e violência de Estado

Fontes: ILGA World Database (GraphQL público, 2026-10-22T21:19:21Z, sha256 `55d53d6a...c3ea`; "65 criminalizam, 7+5 pena de morte" coincide com a ILGA de 01/06/2026, `ilga-news-pride-2026.html`), ILGA *Laws on Us* 2024, ILGA SSH 2020 (último "State-Sponsored Homophobia"; tabela de pena de morte no PDF p.38), V-Dem v16 (regime RoW), V-Party v2 (até 2019), ONU A/HRC/43/61 e 46/50, Amnesty, texto da lei de Uganda (OCR). Níveis, códigos E e regras: PRE-REGISTRO. `econ` e `LGBT` = nota 0-6 (0 extrema esquerda) e 0-4 (0 "opõe-se fortemente") do partido do chefe no V-Party; `(defas.)` = eleição V-Party a mais de 4 anos, partido contínuo no V-Dem.

| País e ano de referência | Regime (RoW, no ano de referência; em 2025 Irã vira 1 e Nigéria 2) | Pena de morte | Nível | Execuções | Executivo no eixo |
|---|---|---|---|---|---|
| Uganda 2023 | 1 aut. eleitoral | legal | L2 | E0 | direita: econ 4, LGBT 0 (defas.) |
| Irã 2023 | 0 aut. fechada | legal | L2 | E1 declarado | n/a (sem partido) |
| Arábia Saudita 2023 | 0 aut. fechada | legal | L2 | E1 declarado | n/a (sem partido) |
| Iêmen 2023 | 0 aut. fechada | legal | L3 | E2 | n/a (sem partido) |
| Afeganistão 2023 | 0 aut. fechada | possível | L3 declarado | E1/E2 declarado | n/a (sem partido) |
| Brunei 2019 | sem dado V-Dem | legal | L2 | E0 | não classificado |
| Mauritânia 2023 | 1 aut. eleitoral | legal | L2 | E0 | não classificado |
| Nigéria 2023 (12 estados) | 1 aut. eleitoral | legal (12 estados) | L2 | E0 (raras) | esquerda: econ 2, LGBT 1 |
| Paquistão, Catar, Emirados 2023 | 1 / 0 / 0 | possível | L2 | E0 | não classificado / n/a |
| Somália 2023 | 0 aut. fechada | possível | L3 declarado | E2 declarado | não classificado |
| Rússia 2023 (movimento "extremista") | 1 aut. eleitoral | não | LE | E0 | n/a (chefe sem partido no V-Dem) |
| Chechênia 2017 | 1 aut. eleitoral | não | L3 | E3 alegado | centro: econ 3, LGBT 1 |
| Hungria 2025 | 1 aut. eleitoral | não | LE | E0 | direita: econ 4, LGBT 1 (defas.) |
| Polônia 2019 ("zonas") | 2 dem. eleitoral | não | LE-local | E0 | esquerda: econ 2, LGBT 0 |
| Iraque 2024, Burkina 2025, Senegal 2025, Trinidad 2025 | 1 / 0 / 2 / 3 | não | L1 | ND | não classificado / n/a |
| Alemanha nazista 1936 | 0 aut. fechada | não | L4 provisório | E1/E3 | não classificado (V-Party sem escore) |
| Espanha franquista 1970 | 0 aut. fechada | não | L3 | ND | direita: econ 6, LGBT 0 |
| URSS 1979 | 0 aut. fechada | não | L1 (lei de 1934; L3 pendente) | ND | esquerda: econ 0, LGBT 0 |
| Cuba UMAP 1966 | 0 aut. fechada | não | L3 | ND | esquerda: econ 0, LGBT 0 |
| Irã pós-1979 (1980) | 1 aut. eleitoral | sim | L3 declarado | E1 declarado | n/a |
| Brasil 1964-85 (1975) | 0 aut. fechada | não | L3 | E0 (extermínio) | direita: econ 5, LGBT 1 |

**O que cada linha tem de pior, verbatim.**
- Uganda, AHA 2023, s.3(1), PDF p.8: "commits the offence of aggravated homosexuality and is liable, on conviction, to suffer death". Execução: nenhuma achada (a ILGA conta cerca de 65 casos de aplicação e alvo estatal em 2005-2023).
- Irã, ONU A/HRC/43/61 par.18 (p.6): "The death penalty may be applied ... for certain cases of consensual same-sex intercourse between men"; A/HRC/46/50 par.27: autoridades chamam a comunidade de "subhuman" e "diseased". Execuções: IHRDC, 20 de ~760 em 1979-81, e Monash, pelo menos 241 em 1979-2020, ambas só via ILGA; a ILGA 2020 marca "YES (UNCLEAR)".
- Iêmen, Amnesty 9/2/2024: em 23/1/2024, Dhamar condenou nove à morte (sete apedrejamento, dois crucificação); em 1/2, Ibb, 13 estudantes. Autoridade huthi de fato (E2). Sentença, não execução confirmada.
- Chechênia, OSCE 2018 p.14-15: "Persons suspected of being homosexuals were picked up without any particular reason ... by police officers and military personnel"; "This demonstrates that the campaign had happened with the support of the state"; mortes: "In extreme cases they were raped and killed" (alegado). As 27 execuções extrajudiciais de janeiro/2017 são, segundo o Comitê da ONU contra a Tortura citado pela OSCE, de "presumed jihadists", não de gays: confundir os dois é erro comum. A frase "exterminated by Ramadan" é atribuída a Kadyrov via PACE (nota 33); a Rússia rejeita o relatório. TEDH, Lapunov, p.29: a Corte conclui que o governo não refutou a alegação de detenção e maus-tratos pela polícia em Grozny entre 16 e 28/3/2017 (inversão do ônus da prova).
- Rússia 2023 (ILGA *Laws on Us*, PDF p.91): em 30/11/2023 a Corte Suprema declarou o "international LGBT movement" "extremist"; não há criminalização do ato; a ILGA 2026 relata "dozens of raids against clubs". Hungria (ILGA 2026): proibição de Paradas e "threatening arrests". Polônia (Stenberg e O'Dwyer 2026, Urban Affairs Review, quartil `nao_verificado`): 64 unidades locais, resoluções "non-binding", "symbolic violence"; nada de violência física de Estado no artigo.
- Espanha, Ley 20/2022 (BOE), exposição de motivos: a Lei de Vagos y Maleantes foi alterada em 1954 "para incluir a «los homosexuales»"; a de 1970 definia como perigosos "los que realicen actos de homosexualidad". Cuba, Garcés Marrero 2019 (quartil `nao_verificado`) p.3: UMAP para "homosexuales, religiosos ... delincuentes y desafectos". URSS, Kondakov 2022 (livro revisado por pares, OA) p.102: em 1934 o ato "returned to the Criminal Code"; contagem de condenados: Healey 2002 e Giles 2002 (ficaram paywall, fila).
- Alemanha nazista: USHMM (instituição, não Q1): "between 5,000 and 15,000 men were imprisoned in concentration camps". Fica L4 **provisório**: a regra do pré-registro exige fonte primária.

## 2. Relação com o eixo esquerda-direita (o que a base permite e o que não)

- **Não permite:** classificar Irã, Arábia, Talibã, huthis, Catar, Emirados, Brunei (sem partido ou sem dado), nem a Alemanha nazista (V-Party sem escore; V-Dem só diz `nacionalista` = 1,00). Isso é 10 das 12 linhas de pena de morte (7 sem partido ou sem dado, 3 sem correspondência no V-Party) e o caso de maior mortandade histórica. Eixo esquerda-direita não é a ferramenta certa para teocracias e monarquias absolutas.
- **O eixo econômico não é proxy de hostilidade LGBT** (ADENDO A8). PiS (Polônia 2019) é "centro-esquerda" no econômico (2) e "opõe-se fortemente" à igualdade LGBT (0); PCUS e PCC são extrema esquerda (0) e também 0 em LGBT; FET (Franco) é extrema direita (6) e 0. Em `eixo_vparty.md` (V-Party, 6.303 partido-eleições, exploratório): entre partidos que governaram desde 1990, 27% dos de esquerda (n=373) e 40% dos de direita (n=454) "se opõem" à igualdade LGBT; Spearman -0,10 entre econômico e LGBT entre partidos de governo.
- **O regime pesa mais:** entre partidos de governo desde 1990, 51% se opõem à igualdade LGBT em autocracias (eleitorais e fechadas), 32% em democracias eleitorais, 4% em democracias liberais. E dos 193 Estados da ONU, criminalizam 23 de 33 autocracias fechadas (70%), 21 de 54 eleitorais (39%), 13 de 55 democracias eleitorais (24%) e 1 de 30 liberais (3%): `u3_resumo.md`. Associação descritiva, sem contrafactual.
- **Cautela:** só Uganda (NRM), Brunei (Sultão), Iraque, Rússia, Hungria, Polônia, Burkina e Senegal legislaram sob o executivo da linha; Irã, Mauritânia, Iêmen e Paquistão têm leis herdadas (ILGA SSH 2020, p.38: Código Penal de 1983 e 1994, Hudood de 1979). Classificar o executivo de hoje não atribui a lei a ele.

## 3. Brasil

### 3.1 Declarações e ações (verbatim, URL, página salva com sha256 em `brasil_itens.csv`)

Tipos: T1a retórica hostil a pessoas; T1b contesta decisão ou política; T2 retórica protetiva ou neutra; T3 omissão ou corte; T4 ação de proteção; T5 perseguição por agentes do Estado; T6 extermínio. A classificação é minha onde há `julgamento_meu`.

| Gov. | Data | Agente | Tipo | Trecho |
|---|---|---|---|---|
| Ditadura | CNV 2014 | relatório oficial | T5 | "de 300 a 500 pessoas eram levadas por dia para delegacias" (p.307); "Não houve uma política de Estado formalizada ... de exterminar os homossexuais" (p.301) |
| Dilma I | 25/5/2011 | G. Carvalho pela presidente | T3 | "A presidente decidiu suspender esse material e suspender também a distribuição" (após reunião com a bancada religiosa) |
| Dilma II | 28/4/2016 | decreto 8.727 | T4 | nome social e identidade de gênero na administração federal |
| Temer | 2017 | execução orçamentária | T3 | "zerou em 2017 os já escassos repasses ... LGBT"; de R$ 3,06 mi (2008) a R$ 518 mil (2016): o corte **começa em 2015** (Aos Fatos/UOL) |
| Temer | 1/11/2017 | Lei 13.502, art.35 | T3? | rol do Ministério sem "LGBT" ("direitos das minorias") |
| Bolsonaro | MP 1/1/2019; Lei 18/6/2019 | MP 870, Lei 13.844 art.43 | T3? | rol **igual ao de 2017**, sem "LGBT"; o Decreto 9.673 mantém a "Diretoria de Promoção dos Direitos de Lésbicas, Gays, Bissexuais, Travestis e Transexuais" |
| Bolsonaro | 3/1/2019 | presidente (Twitter) | T2 | "Não haverá abandono de auxílio a qualquer indivíduo nas diretrizes de Direitos Humanos" |
| Bolsonaro | jan/2019 | ministra Damares | T2 | "Nenhum direito conquistado pela comunidade LGBT será violado" |
| Bolsonaro | 25/4/2019 | presidente (via Crusoé) | T1a | "o Brasil não pode ser um país do mundo gay, de turismo gay. Temos famílias" (segunda mão) |
| Bolsonaro | 14/6/2019 | presidente | T1b | sobre a decisão do STF: "E essa decisão prejudica os próprios homossexuais" |
| Bolsonaro | 27/6/2019 | Decreto 9.883 | T3 | Conselho de Combate à Discriminação, 7 membros (1 + 3 órgãos + 3 sociedade civil), sem "LGBT" no nome |
| Lula III | 1/1/2023; 6/4/2023; 19/6/2023 | decretos 11.341, 11.471, Lei 14.600 | T4 | Secretaria Nacional dos Direitos das Pessoas LGBTQIA+; Conselho recriado (6/4/2023); rol com "d) das pessoas LGBTQIA+" |
| Lula III | 2025 | artigo de opinião | T3 | "destinou apenas R$6,4 milhões para a pauta em 2025" (-20%); não conferido no Portal da Transparência |

Correção de narrativa: "Bolsonaro retirou o LGBT do Ministério" vale para a comparação com 2023, não com 2017; a própria Congresso em Foco (2/1/2019) anota que a lei de Temer "também não incluía a população LGBT". Declaração direta de Lula sobre o tema: nenhuma achada em 2 consultas (não prova que não exista). Votos do Itamaraty na ONU: não verificado.

**Espaço de busca (Brasil):** 12 consultas WebSearch em PT/EN (declarações de Bolsonaro, Damares, Dilma, Temer, Lula; MP 870; STF; Disque 100 em 3 recortes; votos na ONU) e fetch direto de Planalto (13 normas). Negativo = "não achado nesse espaço".

### 3.2 Dados oficiais por governo (`brasil_dados_governo.csv`)

| Governo (ano-calendário) | Sinan campo 55 LGBTfobia, média/ano e % das notificações | Disque 100, denúncias LGBT | Anuário "racismo por homofobia ou transfobia" |
|---|---|---|---|
| Dilma II (2015-16) | 863 (0,50% e 0,39%) | 2016 não lido | n/d |
| Temer (2017-18) | 1.046 (0,38% e 0,45%) | 1.720 (2017); 1.685 (2018) | n/d |
| Bolsonaro (2019-22) | 1.294 (0,49; 0,46; 0,49; 0,50%) | 846 (2019); 2020-21 não obtido; 3.948 (2022) | 783 (2022) |
| Lula III (2023-24) | 2.219 (0,54 e 0,53%) | 6.070 (2023); "mais de 7 mil" (2024, MPF) | 2.090 ou 1.633 (2023); 2.480 ou 2.567 (2024) |

Leitura (sem teste de hipótese): a **proporção** de notificações marcadas como LGBTfobia fica entre 0,38% e 0,54% em todos os governos; a contagem sobe porque o total de notificações interpessoais sobe de 188 mil (2015) para 427 mil (2024), e 42% a 53% das fichas ficam sem motivação preenchida. A Disque 100 mistura unidades (denúncia, violação), cai 49,8% em 2019 (relatório oficial, p.23 e 36: "a classificação ... manteve-se a mesma desde 2011" e a queda não é explicada) e sobe com mudança de protocolo em 2023 (justificativa oficial não lida: página fora do ar). O Anuário muda o mesmo ano entre edições (2023: 2.090 e 1.633). O SIM não registra orientação. **Veredito: não testável** se um governo tem mais violência; o dado de registro não é incidência (dossiê). F8-literatura/README.md e a CNV vol. II seguem valendo sem refazer.

## 4. Placar

| Afirmação-tipo | Mundo | Brasil |
|---|---|---|
| (a) "governo de direita X quer matar gays" | **parcial.** Sustentado: lei de morte sob executivo de direita (Uganda, econ 4, LGBT 0, defasado) e perseguição L3 sob direita (Franco, ARENA 1964-85). Não sustentado: execução documentada por fonte primária sob executivo classificado de direita: nenhuma; as declaradas estão em executivos sem partido ou não classificados | **não sustentada** para T5/T6 em Bolsonaro 2019-22; **sustentada só em parte** para T1 e T3 (PSL: econ 5, LGBT 0) |
| (b) "governo de esquerda Y persegue gays" | **sustentada** para "persegue" (Cuba UMAP, L3; PCC econ 0, LGBT 0); "mata" **não testável** (URSS: só a lei lida; contagem pendente) | **não sustentada** para T5/T6 (Dilma, Lula: T3 e T4); T3 existe nos dois flancos |
| (c) "O Estado brasileiro nunca perseguiu gays" | **não sustentada**: CNV vol. II, p.301-307 (perseguição sim, extermínio formal não) | idem |
| (d) "em governos extremos nunca houve isso" | **não sustentada** como regra: extrema direita (Franco), extrema esquerda (PCUS, PCC) e a Alemanha nazista (provisório) têm perseguição documentada | 1964-85 **não sustentada**; 2019-24 **compatível, não provado** (sem T5/T6 no espaço de busca; sem orientação no óbito) |

## 5. O que muda no dossiê, limites e becos

- **Achados:** (i) o eixo econômico não prevê hostilidade LGBT (PiS, PCUS, PCC); (ii) a pena de morte é fenômeno de autocracia (10 de 11 com dado; a exceção, Nigéria, só em 12 estados sharia), não de lado do eixo; (iii) as execuções são todas "declaradas": falta a fonte primária da ONU; (iv) a Chechênia tem detenção e tortura confirmadas e mortes alegadas, e os 27 mortos de 2017 não eram gays segundo a ONU; (v) o corte de verba LGBT federal começa em 2015 e atravessa quatro governos, e a proporção de notificações LGBTfobia é estável.
- **Limites:** V-Party termina em 2019 e mede o partido, não o governo; o chefe de governo de várias linhas não está na base (A2b); ILGA é ONG compilando mídia e relatórios; USHMM, Garcés, Müller, Stenberg, Kondakov não são Q1 verificado; quatro artigos Q1 históricos ficaram paywall.
- **Becos (`fila-aquisicao.jsonl`, `fila-chrome.jsonl`):** OpenAlex (limite de uso por IP), OHCHR/ULII/EUR-Lex (Cloudflare), gov.br (JavaScript), Agência Gov (desativada por lei eleitoral), API do dados.gov.br (exige token), Giles 2002, Healey 2002, Fernández-Galeano 2016, Lautmann 1981, CRP.7 do Iêmen, número do IHRDC, quartis SJR. Volta se: navegador real, ou se o autor liberar cadastro (hoje proibido).
- **Reproduzir:** `/opt/homebrew/bin/python3.14 -m venv v && v/bin/pip install pyreadr pandas pycountry`, depois rodar `scripts/build_u3.py`, `build_paises.py`, `build_brasil.py`, `eixo_vparty.py`, `resumo_u3.py`, `emit_all.py` (os `.py` citam um venv de scratchpad que não persiste).
