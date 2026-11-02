# F-LAUDO — revisão hostil nível Q1 do paper v0.4 (2026-10-25)

> Cópia distribuída no repositório (2026-10-25, frente E5): caminhos absolutos da máquina do autor trocados por caminhos relativos à raiz do repositório ou por "pasta de trabalho do autor" (arquivos que não são distribuídos); nenhum outro texto mudou. Original: `F-LAUDO.md`, SHA-256 `30a6508a39b4453c70fa08b96d00eeef3e005df4fa960829139206fe12089795`.

> [!NOTE]
> Modelo: Fable 5.1 (`claude-fable-5-1`) do início ao fim, sem fallback. Frente somente leitura: nenhum arquivo do repositório ou do paper foi editado; o único comando executado no repo foi `python3 -I make_provenance.py --verify` (só lê e imprime; árvore conferida antes e depois: 106 arquivos modificados/não rastreados nas duas contagens). Objeto: `paper/paper.md` (1.469 linhas; "l." abaixo = linha desse arquivo) e `paper/build/v04/render/p-001.png … p-126.png` ("p." = página do PDF). Progresso e lista completa de recálculos: `pasta de trabalho do autor/research-2026-10-24-v03/F-PROGRESSO.md`.

## 1. Veredito em uma linha

**Publicável como preprint depois de uma rodada curta de correções textuais: os números conferem, os 15 ataques do Astra estão respondidos no corpo, mas o Resumo e a Figura 25 ainda dizem coisas que o próprio corpo nega, e o repositório público hoje não é a versão que o paper cita.**

Toda correção de Resumo (l.18) espelha no Abstract (l.24). Régua de severidade usada na tabela: **alta** = muda um veredito, um número de manchete ou bloqueia a publicação; **média** = Resumo, corpo ou figura dizem coisas diferentes, ou frase recortável contra o próprio texto; **baixa** = polimento.

## 2. Achados, por severidade

### 2.1. Alta

| # | Onde (trecho) | Por que é problema | Correção mínima |
|---|---|---|---|
| A1 | §6, l.649 (p. 84): "A versão do repositório da qual este artigo deriva tem o selo 5cf914b0…, calculado sobre 721 arquivos"; Tabela D1 l.1461 aponta `dados/regimes/` | **Sequência de publicação, não erro de conteúdo.** O selo 5cf914…/721 fecha na árvore de trabalho local (verificado), mas o commit público (`0601c65`, único em `origin/main`) tem selo `6bf05c72…` (716 arquivos) e **não contém** `paper/paper.md` nem `dados/regimes/` (verificado com `git cat-file -e HEAD:…`); há 106 arquivos modificados ou não rastreados. Quem clonar hoje não acha o que a §6, a Tabela 3 e a Tabela D1 prometem; num clone desse commit, `--verify` passa, mas imprime 6bf05c72…/716, que não é o selo que o paper cita. | Segundo commit + push (com OK do autor no turno) ANTES de qualquer divulgação; depois, num clone limpo, `python3 -I make_provenance.py --verify` tem de imprimir 5cf914…/721; gravar `paper/PAPER-SHA256.txt` com o hash do PDF final. Nada no texto muda. |
| A2 | Figura 25, l.584-590 (p. 75): coluna N4 com X vinho "não sustentada pelo que foi medido" nas linhas "LGB+ sofrem mais violência não letal" e "Gays morrem mais que héteros"; nota l.590: "quer dizer que nenhuma fração nacional foi estimada" | A figura é o recorte mais provável da esquerda: X vermelho + "não sustentada" ao lado de "o agressor agiu por causa do atributo?" lê-se como "o estudo nega a motivação LGBTfóbica". O texto (l.32, l.594) diz o oposto: nada foi medido. Pelo vocabulário da §2.2 (l.95), "nenhuma fração estimada" é **"não testável"**, não "não sustentada". A linha "Gays morrem mais que héteros?" também viola a regra LGB+/LGBT+ da l.34. | Na célula N4 das três linhas, usar o cinza de "não testável" com rótulo "não estimada (nenhum dado nacional)", reservando o vinho a vereditos "contrariada"; renomear a linha para "Pessoas LGBT+ morrem mais que as demais?". Nenhum valor desenhado muda; só cor e rótulo (`make_figures.py`, teste de figura). |
| A3 | Resumo l.18 e Abstract l.24 (pp. 2-3): "A contagem do Grupo Gay da Bahia não é taxa nem total: 50 de 160 casos sorteados de 2019 (31,3%) são verificáveis." | O dois-pontos faz da fração verificável a prova de "não é total", e o corpo diz o contrário (l.247: "não delimita o total nem por baixo nem por cima"). Recortável nos dois sentidos: "69% são inventados" (direita) e "o artigo desqualifica o GGB por link morto" (esquerda). | Resumo: "A contagem do Grupo Gay da Bahia não é taxa (não tem denominador) nem total auditável: dos 160 casos sorteados de 2019, 50 (31,3%) puderam ser verificados hoje na fonte citada, fração que não delimita o total por baixo nem por cima." Abstract: idem em inglês. |

### 2.2. Média

| # | Onde (trecho) | Por que é problema | Correção mínima |
|---|---|---|---|
| M1 | Tabela 11 l.580 e §4.1 l.566: Hipótese 7 = "não sustentada" com "1 de 49 falas com fonte primária, contra 2 de 38 (p = 0,58)" | Com 1/49 contra 2/38, o teste não tem poder para distinguir nada (o próprio texto diz na l.522: "com n pequeno isso não prova equivalência"). A linha 5 da mesma Tabela 11 usa a forma completa "não sustentada pelo que foi medido; efeitos menores que as faixas não detectáveis"; a linha 7 usa só "não sustentada", sem "pelo que foi medido" e sem a ressalva de poder. Inconsistência entre linhas da mesma tabela, que um revisor marca em vermelho. ("Não testável" não serve aqui: o paper reserva o termo para "não há dado", e aqui há dado, só não há poder.) | Tabela 11, linha 7, e l.566: "não sustentada pelo que foi medido; com 1 de 49 contra 2 de 38, a diferença não é detectável (p = 0,58)". Manter a segunda metade ("a frase também não é sustentada por comparação de taxas"). |
| M2 | Resumo l.18 / Abstract l.24: "No Parlamento, 1 de 49 falas que chamam o Brasil de 'o país que mais mata' cita fonte primária." | Sem a linha de base (2 de 38), o Resumo diz o contrário do resultado: o achado é que a falta de fonte **não é traço do tema** (l.522). Isolado, o número vira "parlamentares de esquerda inventam". | Acrescentar: "contra 2 de 38 falas com outras estatísticas ditas em plenário; a diferença não se distingue do acaso". |
| M3 | Resumo l.18 / Abstract l.24 e Conclusão l.657: "Uma busca pré-registrada de 60 consultas não localizou perseguição por agentes do Estado entre 2003 e 2026." | Só o resultado zero vai ao Resumo; os episódios localizados (omissão ou corte em 5 dos 6 mandatos; retórica hostil e ato administrativo hostil em 2019; Tabela 8) ficam de fora. Assimetria recortável: a esquerda lê absolvição de 2019; a direita lê que o PT ficou fora da conta. | "…não localizou perseguição por agentes do Estado entre 2003 e 2026; localizou omissão ou corte de política em cinco dos seis mandatos e um episódio de retórica hostil e um de ato administrativo hostil, ambos em 2019." |
| M4 | Resumo l.18 / Abstract l.24: "O partido do governador não mostrou associação detectável com a taxa de homicídio" | Sem "geral/registrado", o leitor do Resumo entende homicídio de pessoas LGBT+; o corpo diz que nenhum desfecho identifica o grupo (l.359). | "…com a taxa geral de homicídio registrado (que não identifica pessoas LGBT+)". |
| M5 | Resumo l.18 e Abstract l.24 ("with pre-registered rules"): "com regras pré-registradas e régua igual" | Generalização: foram pré-registrados 8 componentes (Tabela 3); o painel principal "foi escolhido depois de ver as variantes" (l.359; Tabela B1 l.1381), e PNS, Sinan, concordância e validação do GGB não têm pré-registro. Revisor metodológico checa a Tabela B1 contra o Resumo. | "com oito componentes pré-registrados (Tabela 3) e a mesma régua para os dois lados do debate". |
| M6 | §1 l.43 e §3.9 l.481-506 (pp. 63-64): Hipótese 6b "a perseguição estatal de homossexuais é própria de regimes de um só tipo político"; Tabela 9 reúne Alemanha nazista, URSS, Cuba, Chechênia | Não há proponente citado para a frase 6b; sem ele, a seção lê-se como "a esquerda também perseguiu" (ataque da esquerda: *whataboutism*) ou como "equiparação de Cuba a Auschwitz" (ataque da direita por outro motivo). O corpo já diz que os casos são ilustrativos, mas a hipótese sem dono fragiliza a Tabela 11. | Na l.43 ou l.483, citar onde a frase circula: `docs/laudos/MIDIA.md` registra que 10 das 33 falas F3 do Parlamento "acusam regimes ou grupos estrangeiros". Alternativa: rebaixar §3.9 a resultado de contexto (como 3.11-3.13) e tirar 6b da Tabela 11. |
| M7 | Tabela 8, nota l.479: "Retórica hostil de ministro ou aliado, contada à parte: zero em todos os mandatos." | Com 10 consultas por mandato, "zero" para 2019-2022 é o alvo mais fácil da esquerda (declarações ministeriais amplamente noticiadas). O limite genérico está na l.645 ("dez consultas por mandato não garantem igual recuperação"), mas não ao lado dessa célula. | Na nota da Tabela 8: "as consultas foram desenhadas para o governante, não para ministros; o zero nessa linha é limite do espaço de busca, não ausência de episódios". |
| M8 | §3.5 l.329: "O Anuário registra 783, 1.633, 2.567 e 3.481 boletins… de 2022 a 2025" | O paper não diz que cada ano vem da edição mais recente nem que o Anuário **revisa** a própria série: 2023 = 2.090 na edição 2024 e 1.633 na edição 2025 (-22%); 2024 = 2.480 (ed. 2025) e 2.567 (ed. 2026) (`dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv`, linhas BR). Revisor: "a série modelada na Figura 14 depende da edição lida". A revisão reforça o argumento do paper (registro instável), mas tem de estar dita. | Uma frase após a série: "cada ano é o da edição mais recente do Anuário; a edição anterior trazia 2.090 para 2023 e 2.480 para 2024, revisão de -22% e +3,5% que o próprio compilador atribui a atualização dos estados (`dados/anuario/README.md`)". |
| M9 | §3.9 l.483 (p. 63): citação literal da CNV "de 300 a 500 pessoas eram levadas por dia para delegacias" (pp. 301, 307) | A §2.6 (l.152) promete trecho entre aspas conferido por script; o ledger `dados/regimes/sources.jsonl` e o `H-RELATORIO.md` (102 partes conferidas) trazem para a CNV só "Não houve uma política de Estado formalizada…" e "172 pessoas presas, segundo o delegado Richetti" (Operação Cidade, 1980). O trecho "300 a 500 por dia" não tem âncora no repositório. | Ancorar: adicionar o trecho ao ledger com página e sha256 do PDF da CNV, ou trocar pelo trecho já ancorado ("172 pessoas presas" na Operação Cidade de 1980). |
| M10 | §4.1 l.564 e Tabela 11 l.576: "contrariada como invenção, porque 50 de 160 casos… são verificáveis, a duplicata é de 0,3%, e o levantamento oficial mostra disparidade de vitimização" | A terceira razão é *non sequitur*: a PNS (violência não letal) não diz nada sobre a lista de mortes do GGB. E "invenção" não está definida: a F3 achou 2 atropelamentos fora do critério do próprio GGB e 15 de 88 mortes não confirmadas como violentas (`docs/laudos/F3-ggb-README.md`, item (a)); um leitor hostil dirá que "inclusão fora do critério" é invenção. | Definir na l.564: "invenção, aqui, é fabricação de casos"; tirar a PNS da lista; manter 50/160 e duplicata 0,3%, e acrescentar "a amostra achou 2 casos fora do critério declarado pelo GGB (atropelamentos sem indício de intenção) em 88 matérias correspondentes". |
| M11 | Figura 11, nota l.307: "Cada linha é uma estimativa da mesma grandeza… As linhas descrevem universos diferentes… e não validam uma à outra." | Resíduo do ataque 1.1 do Astra: "mesma grandeza" e "universos diferentes" na mesma nota. | "Cada linha é uma parcela de LGB+ entre vítimas adultas de violência física, estimada em universos diferentes (pessoas vitimadas na PNS; notificações elegíveis no Sinan)…". |
| M12 | §3.5 l.309: "A completude varia de 11% de faltante em Roraima a 61% no Distrito Federal", logo depois de definir "faltante efetivo" como ignorado + branco + "não se aplica" | O 11%-61% é **só ignorado + branco, de 2023** (`dados/sinan/resumo.md`, l.14-15); com "não se aplica" e em 2025, Roraima dá 22% e o DF 53% (`serie_campo55_uf_ano.csv`). Métrica e ano trocam dentro do parágrafo. | "O motivo ignorado ou em branco variou, em 2023, de 11% em Roraima a 61% no Distrito Federal." |
| M13 | §2.2 l.97, §3.2 l.216, Tabela B1 l.1377, Resumo l.18 e Abstract l.24 ("a mortalidade por todas as causas é maior (razão de 1,31…)" / "all-cause mortality is higher (ratio of 1.31…)") | O veredito "sustentada" fora do Brasil depende da regra complementar "definida em 24 de outubro, depois de identificados estudos que a regra original não admitia" (l.97): é HARKing declarado, e o Resumo apresenta o 1,31 sem dizer que a regra pré-registrada dava "parcial". O corpo faz tudo certo (dois vereditos lado a lado); o Resumo não. | No Resumo: "fora do Brasil, em dado oficial de registro ligado ao censo, a mortalidade por todas as causas é maior (razão de 1,31…)". Manter Tabela 11 como está. |
| M14 | §3.13 l.534: "A sobreamostra não reduz esse número, porque encontrar os mesmos adultos LGB+ exige contatar os mesmos domicílios." | Absoluta demais: triagem dirigida, amostragem adaptativa, painéis por internet ou marcos auxiliares reduzem contatos; a própria Tabela 10 lista "painel… pela internet" com o mesmo n. Revisor de amostragem marca. | "Num desenho domiciliar sem informação prévia sobre quem mora em cada endereço, a sobreamostra não reduz esse número…". |
| M15 | Dimensão: 126 páginas, 25 figuras, 11 tabelas no corpo e 21 nos apêndices; Tabelas A6 (36 linhas), A11 (44), A12 (49), A13 (36), A14 (22) | Editor de Q1 pede material suplementar para o Apêndice A inteiro e corte de figuras redundantes: Figuras 3 e 4 mostram a mesma prevalência de violência física; Figuras 16, 17 e 18(a) mostram o mesmo intervalo do painel. | Apêndice A como suplemento (o texto já cita os caminhos no repositório); fundir 3 e 4; manter 16 e 18, cortar 17. |

### 2.3. Baixa

| # | Onde (trecho) | Por que é problema | Correção mínima |
|---|---|---|---|
| B1 | §3.7 l.408: "O governo Lula de 2007 a 2010 não aparece, porque a série do SIM usada começa em 2010." | O SIM existe desde 1996; sem o motivo (denominadores por célula do Censo 2010), a direita lê janela que exclui a alta de 2003-2010. | "…começa em 2010, ano do Censo que fornece os denominadores por sexo, raça e idade". |
| B2 | §3.6 l.359: "para o Democratas ou o Partido Liberal (cerca de 8)" | O DEM foi incorporado ao União Brasil em 2022. | "Democratas (DEM, hoje União Brasil)". |
| B3 | §2.2 l.95: "em dez idiomas" | O README fala em 11 idiomas com os 19 ledgers da v0.3. | Harmonizar com `manifest/INVENTARIO-PUBLICO.md`. |
| B4 | §3.13 l.534: "5.786,3 LGB+ divididos pela prevalência de 1,89%" | 5.786,3 / 0,0189 = 306.153, não 305.955; o CSV usa 1,8912%. | "pela prevalência não arredondada (1,891%)". |
| B5 | Figura 1 (p. 11), rodapé da imagem: "TSE/BRC classificam governos"; "42,5% a 44,5%" | "BRC" não é definido em lugar nenhum do texto (o G1 já apontou); o corpo diz "42% a 45%". | Trocar "BRC" por "escore de ideologia"; harmonizar os arredondamentos. |
| B6 | Figura 18(b) (p. 51), título interno: "Antes e depois de uma troca de lado: sinais contraditórios" | Os sinais são iguais (queda nos dois sentidos); "contraditórios" é com a hipótese, não entre si. | "a mesma queda nos dois sentidos da troca". |
| B7 | Figura 19(a) (p. 53), anotação: "a queda começou em 2018, ainda com Temer" | A figura diz não atribuir causa e a anotação nomeia um governo. | "a queda começou em 2018". |
| B8 | Tabela 1 l.68 e §3.4 l.245: GGB = "associação privada de ativismo"; ANTRA e FBSP = "sociedade civil" | Rótulo assimétrico num paper que promete régua igual. | "associação da sociedade civil (ativismo LGBT+)" para GGB e ANTRA. |
| B9 | Referências (pp. 87-101): Erlangsen l.701 ("329(24), 2145") e McKetta l.773 ("331(19), 1638") com só a primeira página; Campbell l.675 sem fascículo e páginas (2(1), 67-90); Rafael l.809 sem número de artigo | APA 7 pede intervalo de páginas ou número de artigo. Sem *running head* (aceitável em preprint). | Completar os quatro registros. |
| B10 | §3.1 l.158: "cerca de 442 mil vítimas… (IC95% de aproximadamente mais ou menos 132 mil)" | A largura do IC da prevalência (10,72-18,67) sobre 3,01 milhões dá ±120 mil; 132 mil inclui a incerteza do total ponderado, e o texto não diz. | "(IC95% ± 132 mil, incluindo a incerteza do total de adultos LGB+)". |
| B11 | §3.10 l.512: "Das 13 falas da família F1 sobre expectativa de vida" vs Tabela A17 (F1 Parlamento N = 14) | Confere (`MIDIA.md`: 13 das 14 tratam de expectativa de vida), mas o leitor não tem como saber. | "Das 14 falas da família F1, 13 tratam da expectativa de vida; 11 dão…". |

## 3. O que o Astra apontou e o que foi de fato resolvido

Fonte: `pasta de trabalho do autor/research-2026-10-24-astra/ASTRA-A-escrutinio.md` (15 ataques, 8 divergências, 5 condições) e `ASTRA-C-manual-e-projeto.md` (portão F5 e cinco decisões).

| Item do Astra | Estado | Onde a v0.4 responde |
|---|---|---|
| 1.1 PNS-Sinan sem elegibilidade comum | ✅ resolvido (⚙️ resíduo M11) | l.299 (Guia de Vigilância, p. 1222); Tabela 1 nota l.75; §4.3 objeção 6 |
| 1.2 "não testável no Brasil" como verdade universal | ✅ | l.182 ("não é testável com dado público"), Rafael et al. e Luis et al. integrados; Tabela 11 "Brasil: não testável com dado público" |
| 1.3 trans "fora da PNS"; N2 como limite inferior | ✅ | l.277, l.295, Tabela A7, glossário "cenário de subtração" |
| 1.4 "cobre no máximo 28,7%" | ✅ | l.277 ("não estimam cobertura real"); Figura 10 (RR* = N/E₀) |
| 1.5 N4 confunde efeito causal com motivação | ✅ no texto (❌ na Figura 25, ver A2) | l.32, l.594, nota l.590 |
| 1.6 painel não testa violência LGBT+ | ✅ | l.359 primeira frase; Tabela 11 "N1 (homicídio geral)" |
| 1.7 pesos do TWFE não fecham heterogeneidade | ✅ | l.144, l.384 ("descreve a residualização e não demonstra ausência de efeitos heterogêneos") |
| 1.8 1.674 -> 1.554; MDE 60,7% | ✅ | l.158, l.534 |
| 1.9 87 campos são do arquivo | ✅ | l.182 (59 variáveis em 9 blocos; arquivo sem o número) |
| 1.10 auditoria do GGB não reconstruível | ✅ | l.247, l.653 (declarado como não reproduzível por privacidade) |
| 1.11 SHA-256 não prova anterioridade | ✅ | l.121, l.645, l.649 |
| 1.12 0/49 como principal | ✅ | l.512 (1/49 principal, 0/49 sensibilidade); Tabela A18 |
| 1.13 Campbell "explica" | ✅ | l.30, l.596 ("O mecanismo não foi testado") |
| 1.14 limites do painel | ✅ | Tabela 6 (três métodos); l.384 (viés de reclassificação condicionado à fórmula) |
| 1.15 Sinan duplicado na série auxiliar | ✅ no repositório | README v0.3; identidade "soma das 27 UFs = BR" testada (l.152) |
| Div. 1-3 (1.554; 305.955; Sinan 2.173) | ✅ | l.158, l.534; README |
| Div. 4-6 (17/829 ledgers; 843 fontes; 139 scripts) | ✅ | O paper não cita mais esses totais; README qualifica (19 ledgers, 929 pares, 464 com SHA-256, 166 scripts) |
| Div. 7 (concordância 0,49-0,74 / 22-25 UFs) | ✅ | l.319 (0,53 a 0,74; 22 a 23 estados) |
| Div. 8 ("piso" no README) | ✅ | README: "fração verificada hoje, não piso nem teto" |
| Condição 5 ("versão auditável e estável", `[REPO_URL]`) | ⚙️ parcial | URL real no texto, mas o HEAD público não é a versão citada (A1) |
| Manual C, decisão 1 (título) | ✅ | Título novo, sem "ninguém sabe" nem contagem de fontes/scripts |
| Manual C, portão F5 (repo online antes do DOI) | ⚙️ pendente | Idem A1 |

## 4. Recálculos a partir dos CSVs do repositório

| Número no paper | Fonte recalculada | Resultado | Status |
|---|---|---|---|
| RP bruta 3,84 e ajustada 2,82 (2,16-3,68) (l.158) | `dados/pns/seguro_pns2019.csv`: 0,14696/0,03825 = 3,8425; rp_ajustada 2,8201 [2,1613; 3,6798] | confere | ✅ |
| 50/160 = 31,3% (24,6-38,8); 50/88 = 56,8%; 73/88 = 83,0%; 3/73 = 4,1% (1,4-11,4) (l.247) | `paper/figures/fontes/ggb_validacao_resumo.json`; Wilson recalculado à mão | 31,25%, [24,6; 38,8]; 56,8%; 83,0%; 4,1%, [1,4; 11,4] | ✅ |
| Fisher p = 0,19 e p = 0,58 (l.522) | `research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv` | 0,1879 e 0,5784 | ✅ |
| Cobertura 22,9% e 28,7%; numeradores A/B 19,7/8,4/26,6/16,5% (l.273-274) | `dados/ggb/c08_numeradores.csv`: 257/1.122,2; 291/1.012,7; 221, 94, 269, 167 | confere | ✅ |
| Chapman 186 (175-198), 63% (l.257) | n = 118, 139, sobreposição 88: (119×140)/89 − 1 = 186,2; 118/186 = 63,4% | confere | ✅ |
| Painel: -10,8% a +13,1% para 5 pontos (Tabela 6) | `dados/painel/c02_indet_resultados.csv`: b 0,000896, EP 0,012081 -> 100[exp(5(b ± 1,96 EP)) − 1] | -10,77% / +13,07% | ✅ |
| Governos: +11,1 / -4,2 / -21,0 / -10,6% e +7,9 / -0,4 / -13,7 / -6,1% (Tabela 7) | `dados/exposicao/c10_e1_federal.csv`: 25,93->28,81; 28,81->27,61; 27,61->21,81; 21,81->19,50; indeterminada 31,72->34,22 etc.; parcela indeterminada 18,0% (2018), 25,9% (2022), 30,1% (2024) | confere | ✅ |
| 67 trocas: 31 subiram, 36 caíram, mediana -0,7%, p 0,016 (Holm 0,073); blocos 8/12 (+9,5%, p 0,36) e 5/8 (+3,5%, p 0,74) (l.449) | `dados/exposicao/c10_e2_resumo.csv` | confere | ✅ |
| Taxas 2,6 / 4,3 / 20,0 / 51,7 e razões 1,7 / 7,7 / 19,9; 10,8; 2,56 (2,42-2,60) (Tabela 5) | `dados/sim/asr_brasil.md` | confere | ✅ |
| Série do Disque 100: 1.331 a 4.787 (2011-19); 1.367 / 4.163 / 6.173 / 8.176 / 9.346; 10.461 (2026); canal 222 mil -> 638 mil (2,9×); módulo 6,8× (l.347) | `dados/disque100/saidas/d100_comparacao_nacional.csv` e `d100_serie_anual.csv` (canal 222.010 e 637.890) | confere | ✅ |
| Anuário 783 / 1.633 / 2.567 / 3.481; 4,4× (l.329) | `dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv` (linhas BR, edição mais recente por ano) | confere; **revisões entre edições não ditas** (M8) | ✅/⚙️ |
| Simulação: SSE 0,0472; 63,7% / 42,3% / 72,3% (l.333) | `simulacao/resumo.md` | confere | ✅ |
| Sinan: faltante 53% (2015) e 42-45% (2023-25); "não se aplica" ~15%; LGBTfobia 0,4-0,5%; orientação válida 75,7%; 4,12% / 4,08% (l.299, l.309) | `dados/sinan/serie_campo55_uf_ano.csv` (BR: 38,35+15,02 = 53,4%; 44,2 / 42,5 / 44,5%; 14,75-17,44%; 0,38-0,54%); `triangulacao_pns_sinan.csv` | confere (11%-61% é outra métrica: M12) | ✅/⚙️ |
| PNS parcela 7,1% (5,1-9,1), 179 de 3.291 (l.299) | `dados/pns/c05_razao_direta.csv`: 7,123 [5,112; 9,134] | confere | ✅ |
| deff 5,1 (2,6-6,4); 5.787 LGB+; 305.955; 60,7%; 329.644; Tabela 10 275.573 / 5.212 / 31,7% (l.534, l.552) | `research-2026-10-21-rodada3/F2-custos/{deff_bootstrap_lgb,n_necessario,capacidade_por_opcao}.csv` | confere (B4: a prevalência usada é 1,8912%) | ✅ |
| Tabela 8: somas e contagens por mandato (l.471-477) | soma das linhas | 60; 51/55; 23/51; 1/8/1/0/10; omissão em 5 de 6; proteção em 4 de 6; 1 de 13 páginas publicadas nos dois primeiros mandatos de Lula | ✅ |
| Tabela 9: 100 mil / 53,4 mil / 5-15 mil; 64 mil (50 mil até 1969); 12 expedientes e 4 condenações; 15 diplomatas e 7; >38 mil; ~35 mil; ~11 mil; 2 episódios e 30; >100 (l.493-502) | `dados/regimes/H-RELATORIO.md` (102 trechos conferidos por script contra as fontes) | confere, **exceto** a citação "300 a 500 por dia" da CNV (M9) | ✅/⚙️ |
| Tabela 3: 16 primeiros dígitos dos 8 hashes e horas (l.129-136) | os 8 arquivos `.sha256` / `.hora.txt` do repositório | conferem (inclusive a nota do hash supersedido dos CRITERIOS) | ✅ |
| Selo 5cf914…, 721 arquivos (l.649) | `python3 -I make_provenance.py --verify` na árvore local | "provenance verified: 5cf914…(721 arquivos)" | ✅ local / ❌ no commit público (A1) |
| ONS 1,31 (982,8/752,6 = 1,306); Luis 563/1.325 = 42,5%; 258.011 = 219.562 + 38.449; κ 0,73 (0,46-0,92) e 0,66 (0,31-0,93); 442 mil ± 132 mil; 8,8 e 10,0 por 100 mil; 26,4 e 24,2 | `paper/figures/fontes/estudos_mortalidade.tsv`; `escrutinio/simetria/concordancia_C27.csv`; `seguro_pns2019.md`; `sim_adultos_18mais.csv` | conferem contra os derivados locais (não contra a fonte externa) | ✅ (derivado) |

## 5. O que está bem e NÃO deve ser mexido

- **Tabela 1** (l.58-75) com "quem produz / o que conta e quem entra / o que não diz": resolve a "sopa de letras" do G1 e é o melhor dispositivo do paper para o leigo. Não reduzir.
- **Figura 1, "caminho do dado"** (p. 11): a seta da PNS que pula as etapas 2-4 e o X no SIM dizem em um olhar o que a §3.2 leva três parágrafos para dizer. Só o rodapé (B5).
- **As demonstrações em cinco passos** da §3.4 (l.269-275, teste de escala) e da §3.5 (l.331-335, identificabilidade): são o trecho mais legível e mais difícil de atacar; a inversão da conta (RR* = N/E₀, Figura 10) desarma o ataque 1.4 do Astra por construção.
- **Tabela 6** (três métodos de intervalo lado a lado) e **Tabela B1** (17 desvios declarados com efeito): um revisor metodológico não tem o que pedir além do que já está lá; é o que sustenta M5 como correção de Resumo, não de método.
- **§4.3, as oito objeções** (l.598-609): cada uma aponta o dado e a seção. Acrescentar, não reescrever (as lacunas estão em M6, M7, M8 e M13).
- **A frase "não localizado no espaço enumerado de busca"** (l.95) e seu uso consistente em 3.2, 3.8, 3.9 e 3.11.
- **Numerador B como "cenário de subtração"** em todos os lugares (l.274, l.277, Tabela A7, glossário): coerente de ponta a ponta.
- **§3.7 e Tabela 7**: descrever o que a taxa fez em cada governo com placebo (Figura 20) e causa indeterminada ao lado é a única forma de não ser acusado por nenhum dos dois lados; manter os dois números (-21,0% e -13,7%) sempre juntos como está.
- **Resumo e Abstract no tamanho** (250 e 235 palavras); **Tabela 9 com cabeçalho repetido** na quebra de página (p. 64); figuras legíveis a 14 cm com título, nota e fonte fora da imagem (regra APA aplicada); referências com DOI em quase todas as entradas; nenhuma citação sem referência (conferido por script).
- **A regra LGB+/LGBT+** (l.34) aplicada no texto inteiro (a exceção é a Figura 25, A2).

## 6. Os três ataques públicos mais prováveis e se o texto já responde

| # | Ataque (como circularia) | O texto responde? | O que falta |
|---|---|---|---|
| 1 | **Esquerda, com screenshot da Figura 25 e do Resumo:** "Estudo diz que a motivação LGBTfóbica 'não é sustentada' e que 69% da lista do GGB não se confirma." | **No corpo, sim** (l.247, l.590, l.594; §4.3 objeções 1 e 2). **No Resumo e na figura, não.** | A2 e A3. Sem elas, o recorte é verdadeiro ao pé da letra. |
| 2 | **Direita, com a Figura 19 e a §3.5:** "Estudo prova que a 'LGBTfobia disparou' é só registro e que Bolsonaro derrubou os homicídios em 21%." | **Sim, e bem**: l.337 ("compatível tanto com 'a LGBTfobia disparou' quanto com 'é só registro'"); l.431 (placebo de 2018); Tabela 7 com a causa indeterminada; §4.3 objeções 4 e 5. | Só polimento: a anotação "ainda com Temer" (B7) e, na nota da Tabela 7, remeter ao placebo de 2018 (Figura 20, Tabela A13), que é de outra análise (quebra de nível da série nacional) e hoje só aparece na figura; não criar coluna na Tabela 7, que é exposição por mandato. |
| 3 | **Metodológico, revisor de Q1:** "Pré-registro de fachada: a especificação principal do painel foi escolhida depois, a regra de mortalidade mudou depois de ver os estudos, e a Hipótese 7 recebe veredito sem poder." | **Parcialmente**: a Tabela B1 declara os três desvios, e a §5.4 nomeia o risco *post hoc*. | M1 (ressalva de poder na linha 7 da Tabela 11, na forma da linha 5), M5 (Resumo e Abstract não generalizarem "pré-registradas") e M13 (Resumo e Abstract dizerem "em dado oficial"). Com isso, o ataque vira "declarado e tratado". |

Quarto ataque, logo atrás: a esquerda sobre "zero retórica hostil de ministro" (M7); é o mais fácil de neutralizar com uma frase.

## 7. Resposta ao pedido do autor ("estamos blindados dos dois lados?")

Quase. O corpo está simétrico e cada resultado tem o número contrário ao lado; o que ainda vaza é o que o leitor apressado vê primeiro: Resumo (A3, M2-M5, M13) e a Figura 25 (A2). As 11 correções de alta e média que tocam texto cabem numa sessão da frente P; nenhuma muda número ou veredito de fundo, exceto a troca de palavra em M1 (que é para o vocabulário que o próprio paper fixou). A única pendência que bloqueia é de sequência (A1): publicar o repositório na versão citada antes de o PDF circular.

## Becos

- Não rodei `pytest` nem `run_all.py` (o `run_all` regenera 3 PNGs; frente somente leitura). O selo foi conferido só com `--verify`.
- Não abri as fontes externas: ONS (28.659.465 pessoas; taxas por 100 mil), Home Office, Statistics Canada, Ministry of Justice NZ, FRA, Bundeskriminalamt, Henningsmeier, Ferguson & Malouff, Sleath & Smith, Rafael et al. (93,3%), Clark & Blosnich (84,5%), Lei 15.380/2026, Mendes & Silva. Conferi só contra os derivados do repositório.
- Não localizei no repositório a âncora de "o texto dos registros do TDoR cita o GGB em 72% a 94% dos casos de 2013 a 2018" (l.257); a busca rápida em `docs/laudos/F3-ggb-README.md` não achou; não conferido.
- "57% dos adultos LGB+ têm de 18 a 29 anos" (l.176) exige o microdado ponderado; não recalculado (o não ponderado é 697/1.554 = 45%).
- Custos da Tabela 10 (R$ 6,85 / 29,0 / 42,0 milhões e faixas) não recalculados; não li `cenarios_n_custo.csv`.
- A citação da CNV (M9) pode existir no PDF da CNV; não abri o PDF (não está no repositório), só o ledger e o relatório H.
- Heurística de "referência sem citação" por regex deu falso positivo generalizado e foi descartada; a conferência citação -> referência (sentido inverso) passou limpa.
