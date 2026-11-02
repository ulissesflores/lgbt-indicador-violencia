# Histórico de revisões do artigo e material retirado do texto

Este arquivo guarda, fora do artigo, o histórico das correções feitas ao longo da pesquisa e o material de processo que deixou de constar do texto na versão 0.4 (25 de outubro de 2026), quando o artigo passou a apresentar apenas o resultado vigente. O texto do artigo é a fonte do que vale; este arquivo documenta como se chegou a ele. Os trechos abaixo são copiados sem alteração da versão 0.3 do artigo (paper.md, SHA-256 59a5783dae3c495f7c7a4fd66dfad31c44b0dfddfa715eac3c1acc6e9b36ab76).

## 1. Correções feitas ao longo da pesquisa

**Tabela 13 — Correções feitas ao longo da pesquisa, com o motivo**

| O que estava escrito | O que vale | Como foi detectado |
|---|---|---|
| Concordância saúde-polícia por UF, Spearman de 0,49 a 0,74, 22 a 25 UFs | 0,53 a 0,74 e 22 a 23 UFs na especificação principal; parcial de 0,14 a 0,32, IC com zero | correlação parcial; segunda rodada de escrutínio |
| Survey de ~60 mil entrevistas detecta +30% | ~306 mil adultos triados (deff 5,1) | deff medido no microdado |
| PNS 2019 com 1.674 LGB+ detecta 58,3%; 305.993 adultos triados | 1.554 LGB+ observados; 60,7%; 305.955 (arredondamento único); 329.644 pela fração não ponderada | segunda rodada de escrutínio |
| "A declaração de óbito tem 87 campos" | formulário com 59 variáveis; arquivo do SIM com 87 campos; nenhum com orientação | manual oficial lido |
| Pessoas trans "fora do denominador da PNS"; numerador B como limite inferior | a PNS não identifica pessoas trans; B é cenário de subtração; cis LGB entre 100-118 (2023) e 164-168 (2024) | segunda rodada de escrutínio; marginais do GGB |
| "Cobertura implícita" de 8,4% a 28,7% | razão contagem/esperado de 8,2% a 28,7%, conta de cenário | idem |
| PNS e Sinan "estimam a mesma coisa" | universos distintos; regra de notificação diferente por sexo e idade | Guia de Vigilância em Saúde, p. 1222 |
| "Gays morrem mais": parcial no mundo | mortalidade geral sustentada em populações definidas fora do Brasil; homicídio sem razão populacional | dado oficial do ONS e texto integral de Zachry et al. |
| "A Lei de Campbell explica" | hipótese de leitura, não testada | segunda rodada de escrutínio |
| 829 fontes em 17 ledgers no repositório | 829 identificadores, 828 obras; 16 ledgers distribuídos | recontagem |
| "Piso" da contagem do GGB | fração verificada (31,3%), nem piso nem teto | revisão hostil |
| 273 "homicídios declarados" do GGB em 2024 | 269 (sem 4 "outras causas") | reanálise com numeradores comparáveis |
| 20 suicídios do GGB em 2024 | 18 | releitura do release |
| "+8,83%" no release de 2024 | 34/257 = 13,2% | aritmética da fonte |
| Limite do painel em aproximação linear (±10% a ±18%) | conversão exata assimétrica; três métodos de intervalo | revisão hostil; segunda rodada |
| "Em cada desfecho a faixa é mais larga que no total" | as faixas variam; a das mulheres é mais estreita | segunda rodada de escrutínio |
| Cuba "sustentada" com artigo sem quartil | provisória, depois documentada pelo informe da Comissão Interamericana (1983) | revisão hostil e busca simétrica |
| F4 com veredito "falso" para "não existe" | contrariada pela PNS no nível N1/N2 não letal | vocabulário único |
| Brasil: 2 consultas para um presidente contra 12 no total | 60 consultas, 10 por governante | revisão hostil |
| "0/49" sem comparação | 1/49 pela regra literal (principal), 0/49 pela regra aplicada; linha de base 2/38 | segundo codificador; segunda rodada |
| Estudo de eventos como "robustez adicional" | inconclusivo | critérios congelados |
| Faixa "2-10%" de falsas alegações em toda jurisdição | estudos de 2,0% a 13,7%; divergência interna em Ferguson & Malouff | leitura do texto integral e replicação |
| "3,66 a 110 por 100 mil" como taxa trans | grade de cenários; 8 de 12 abaixo de 1 | leitura do texto integral |
| Mendes & Silva (2020) como Q1 e validação | Q2, dados cedidos pelo GGB | leitura do texto integral |
| "Nenhum efeito do governador" | ausência de evidência de associação com homicídios gerais, com limites | revisão hostil |
| Série auxiliar do Sinan com o total nacional somado em dobro (não citada no texto) | soma só das 27 UFs, com teste de identidade | segunda rodada de escrutínio |

## 2. Revisão adversarial: respostas, ataques de maior risco e triagem

Na versão 0.3 do artigo, a seção 4.4 e a Tabela 11 descreviam as respostas às revisões adversariais; os relatórios completos e a triagem estão em research-2026-10-21-rodada3/escrutinio/.

Os 33 clusters da primeira revisão hostil caíram em quatro grupos, e a resposta a cada um mudou o texto ou a análise. (a) Síntese mais forte que o corpo: o padrão dominante foi a síntese afirmar mais que as seções; "nenhum efeito do governador", "piso nominal" do GGB e expressões de primazia sem espaço de busca foram substituídos por ausência de evidência com limites, fração verificada e o molde de busca enumerada. (b) Régua assimétrica: Cuba, que entrava como "sustentada" com um artigo sem quartil conferido, foi reclassificada como provisória e depois como documentada por órgão internacional ao localizar o informe da Comissão Interamericana; o veredito sobre o Brasil passou a usar a mesma busca para seis governantes; o único "falso" do texto (sobre a família F4) foi trocado por "contrariada pela PNS no nível N1/N2". (c) Conta não feita: quatro reanálises foram rodadas com critérios congelados, e uma contrariou a expectativa (o estudo de eventos, esperado como corroboração, saiu inconclusivo). (d) Ataques rejeitados: o de "números órfãos" era artefato do extrato, e o de "nenhuma taxa padronizada" já estava resolvido em disco. As assimetrias encontradas prejudicavam ora a direita, ora a esquerda, e a correção aplicou a mesma célula aos dois. A Figura 28 (no Anexo F, PDF de anexos) mostra os 33 clusters por decisão e por flanco de origem, e a Tabela 11 lista os dez ataques de maior risco com a resposta que cada um produziu.

A versão 0.2 passou por uma segunda rodada de escrutínio, feita por um quinto modelo de linguagem, de outra família, com acesso ao repositório. Cada ataque foi conferido nos arquivos antes de qualquer correção, e o que não procedia foi registrado como tal. Procederam e mudaram o texto: a amostra LGB+ observada (1.554, não 1.674) e o efeito mínimo detectável correspondente (60,7%); o total nacional do Sinan somado em dobro numa série auxiliar, que não chegava ao texto; a troca entre o arquivo do SIM (87 campos) e o formulário da declaração de óbito (59 variáveis); a premissa de que pessoas trans estavam fora do denominador da PNS e de que o numerador B do GGB seria limite inferior; as contagens de fontes (829 identificadores, 828 obras); os intervalos do painel por três métodos; a regra literal do Parlamento como principal; a regra de notificação do Sinan, que desfaz a leitura de que PNS e Sinan medem a mesma coisa; o veredito de mortalidade, que ignorava o dado oficial britânico e a síntese positiva de Zachry et al. (2025); e a Lei de Campbell como explicação, rebaixada a hipótese. Não procedeu a crítica de que faltava a lista dos 139 scripts do título: ela está em `dashboard/dashboard_dados.publico.json`. A lista completa de mudanças está no Apêndice B.

**Tabela 11 — Os dez ataques de maior risco da primeira rodada e o que mudou no artigo**

| Cluster | Flanco do ataque | Ataque | O que mudou |
|---|---|---|---|
| C16 | ambos | Cuba entrava como perseguição "sustentada" com um artigo sem quartil conferido | provisória e depois documentada pelo informe da Comissão Interamericana (1983), com ressalvas |
| C20 | direita | o veredito "falso" para "não existe homofobia" saltava do nível N1/N2 para a motivação (N4) | "contrariada pela PNS no nível N1/N2"; a disparidade ganhou item próprio |
| C17 | ambos | Brasil: 2 consultas para um presidente contra 12 no total; "parcial" só à direita | busca simétrica de 60 consultas, 10 por governante |
| C06 | ambos | GGB chamado de "piso" em um trecho e de "não permitido concluir" em outro | fração verificada; teste de escala como razão de cenário (v0.3: numerador B como cenário, não limite) |
| C01 | esquerda e método | coeficiente nulo do painel lido como "nenhum efeito" | ausência de evidência com intervalos por três métodos; falsificação; estudo de eventos |
| C14 | esquerda | síntese de mortalidade apagava excessos medidos depois de 1995 | veredito por causa e população (v0.3: mortalidade geral sustentada fora do Brasil em populações definidas) |
| C04 | ambos | PNS x Sinan como "dois canais independentes" que "passam no teste" | intervalo direto de 5,1% a 9,1% (v0.3: universos distintos, sem teste de concordância) |
| C21 | direita | "país que mais mata" como "sustentada em parte" sem comparação entre países | não sustentada pelo que foi medido |
| C12 | ambos | identificabilidade escrita como propriedade da série, sem o teto p = 1 | restrita ao modelo e a p < 1 |
| C19 | método | afirmações de ausência e de primazia sem espaço de busca declarado | molde "não localizado em [espaço]; não equivale a inexistência" |

*Nota.* Fonte: `research-2026-10-21-rodada3/escrutinio/TRIAGEM.md` e `TRIAGEM.csv` (flanco = primeiro rótulo do cluster).

**Tabela 32 — Triagem dos quatro revisores hostis: decisão por prioridade**

| decisão | P1 | P2 | P3 | total |
|---|---|---|---|---|
| ACEITO-CORRIGIR | 9 | 6 | 0 | 15 |
| PARCIAL | 0 | 6 | 3 | 9 |
| VERIFICAR-ANALISE | 0 | 6 | 1 | 7 |
| ACEITO-LIMITAÇÃO | 0 | 0 | 1 | 1 |
| REJEITADO | 0 | 0 | 1 | 1 |
| FORA-DE-ESCOPO | 0 | 0 | 0 | 0 |
| total | 9 | 18 | 6 | 33 |

*Nota.* Fonte no repositório: `research-2026-10-21-rodada3/escrutinio/TRIAGEM.md` (copiada sem alteração de valor; só a vírgula decimal).

## 3. Contagens do processo de pesquisa (antiga seção 3.14 e título da versão 0.3)

Título da versão 0.3: "Gays morrem mais no Brasil? Ninguém sabe! Passei 14 dias, 829 fontes em 10 idiomas, 139 scripts e 4 revisores hostis atrás da resposta".

A pesquisa registrou 829 identificadores de fonte em 17 arquivos de registro (um "livro de fontes", o ledger, por frente de pesquisa), com registros datados de 2026-10-11 a 2026-10-23; eles correspondem a 828 obras distintas, porque um preprint foi registrado com e sem o sufixo de versão /v1. O repositório da versão 0.3 traz os 17 ledgers, inclusive o 17º, `research-2026-10-21-rodada3/A-textointegral/sources.jsonl` (23 registros só de metadados, distribuído desde a versão 0.3 e o único a conter a versão sem sufixo); o inventário gerado só com os arquivos distribuídos (`manifest/INVENTARIO-PUBLICO.md`) reproduz os 829 e os 828 quando restrito a esses 17 ledgers. Os 139 scripts do título são os da árvore do projeto em 2026-10-23 (lista em `dashboard/dashboard_dados.publico.json`); 128 deles estão no repositório e 11 ficaram fora (aquisição e ferramentas de lote); o repositório tem hoje 180 arquivos Python no total, porque traz também testes, reprodução, figuras e as análises da versão 0.3, entre elas os 8 scripts do Disque 100. O funil é estreito por desenho (Figura 25, no Anexo F do PDF de anexos): 79 artigos com DOI (identificador permanente de artigo) tiveram o texto integral lido e conferido contra o dossiê, 50 deles em periódico Q1, e 46 desses confirmam ou corrigem ao menos uma afirmação. As fontes estão em 10 idiomas, das quais 377 identificadores em inglês (376 obras: o preprint duplicado é em inglês), 288 em português e 108 em espanhol, e por tipo 280 são oficiais, 326 são artigos em periódico (61 com quartil Q1 conferido) e 64 vêm de organizações da sociedade civil (Figura 26, no Anexo F do PDF de anexos). A versão 0.3 acrescentou 30 registros de literatura e verificação externa num ledger próprio (`research-2026-10-24-v03/L-ledger/sources.jsonl`), fora dessas contagens: com ele, o inventário do repositório tem 18 ledgers, 1.599 registros, 853 identificadores e 852 obras. Número de fontes, idiomas e scripts descreve o processo; não mede a validade dos resultados.

## 4. Artigos citados no dossiê lidos só pelo resumo (antigo Anexo D)

Doze trabalhos ficaram sem texto integral lido por meio legítimo; nenhum decide veredito neste artigo. Dois estão na lista de referências, com aviso no texto: Szwarcwald et al. (2025), no §3.1, e Silva et al. (2026), na Introdução.

| Trabalho | Periódico | DOI | Estado |
|---|---|---|---|
| McVeigh, Welch e Bjarnason, 2003 | American Sociological Review | 10.1177/000312240306800603 | não verificado em texto integral |
| Mills, Lantz e Wenger, 2024 | Criminology | 10.1111/1745-9125.12378 | não verificado em texto integral |
| Pezzella, Fetzer e Keller, 2019 | American Behavioral Scientist | 10.1177/0002764218823844 | não verificado em texto integral |
| Szwarcwald, Souza Júnior, Almeida e Castilho, 2025 | Journal of Interpersonal Violence | 10.1177/08862605241303957 | não verificado em texto integral |
| Silva, Magalhães, Carvalho et al., 2026 | Revista DCS | 10.54899/dcs.v23i94.6713 | lido só pelo resumo; quartil não conferido |
| Thoennes e Tjaden, 1990 | Child Abuse & Neglect | 10.1016/0145-2134(90)90026-P | não verificado em texto integral |
| Spohn, White e Tellis, 2014 | Law & Society Review | 10.1111/lasr.12060 | não verificado em texto integral |
| Katz-Wise e Hyde, 2012 | Journal of Sex Research | não registrado no dossiê | não verificado em texto integral |
| Grattet e Jenness, 2005 | Law & Society Review | 10.1111/j.1540-5893.2005.00248.x | não verificado em texto integral |
| King, 2007 | Law & Society Review | 10.1111/j.1540-5893.2007.00295.x | não verificado em texto integral |
| Baía, Alberto e Dell'Aglio, 2021 | Child Abuse & Neglect | 10.1016/j.chiabu.2021.105006 | não verificado em texto integral |
| Devine, 2021 | Social Science Quarterly | 10.1111/ssqu.12896 | não verificado em texto integral |

## 5. O que não está no repositório, e por quê (antigo Anexo E)

| Ausente | Motivo |
|---|---|
| Microdados brutos do SIM, do Sinan, da PNS e do TSE | arquivos oficiais grandes; há script de aquisição com SHA-256 esperado (`scripts/acquire_*.py`) |
| Microdados do Disque 100 | 23 arquivos oficiais de 57 MB a 1,93 GB (cerca de 14 GB), baixáveis sem cadastro no catálogo do MDHC; o repositório traz o catálogo com sha256, o script de download, as contagens e os testes (`dados/disque100/`), e nenhum resultado do artigo depende deles |
| PDFs e páginas de terceiros (artigos, relatórios, notícias, manuais) | direitos de terceiros; o ledger traz URL ou DOI, data de acesso e SHA-256 de cada arquivo lido |
| Nomes de vítimas e listas nominais do GGB | privacidade; a validação usa identificadores sem nome, e por isso a ligação entre caso e fonte não é reproduzível publicamente |
| Lista de casos do GGB de 2023 a 2025 | não publicada pela organização; por isso essas contagens são inauditáveis (achado, não pendência) |
| Lista nominal da ANTRA | não publicada (mapa de acesso restrito) |
| Texto integral de notícias e de abstracts usados na codificação de discurso | direitos de terceiros; o repositório guarda o SHA-256 de cada trecho |
| Identificadores do pareamento Sinan-SIM de Luis et al. (2026) | obtidos pelos autores por solicitação com termo de confidencialidade; este projeto não pede dado a pessoa ou instituição |
| Modelo de documento e regras de exportação da casa | recursos internos do laboratório; o PDF e o DOCX publicados são os gerados pelo autor |
| Prompts e respostas cruas do juiz da rubrica | trazem caminhos locais e identificadores de sessão; os vereditos estruturados estão em `paper/build/juiz/` |

## 6. Resumo para leitor não cientista da versão 0.3

- Uma pesquisa oficial de 2019, que bateu de porta em porta em casas sorteadas, mostrou que, em um ano, cerca de 1 em cada 7 adultos lésbicas, gays e bissexuais sofreu violência física, contra cerca de 1 em cada 26 heterossexuais. A diferença continua grande depois de comparar pessoas de mesma idade, cor, escolaridade e região.
- Essa pesquisa não pergunta se o agressor agiu por preconceito, e não conta mortes.
- No Brasil, a certidão de óbito não diz a orientação sexual de quem morreu. Por isso não dá para saber, com dados públicos, se gays morrem mais que heterossexuais no país.
- Na Inglaterra e no País de Gales, onde o censo foi ligado aos registros de óbito, lésbicas, gays e bissexuais morreram cerca de 1,3 vez mais, por todas as causas juntas. Os estudos lidos não medem, por orientação sexual, o risco de ser assassinado.
- As listas de mortes feitas por associações a partir de notícias são úteis, mas não são uma taxa: dependem do que virou notícia.
- O número de boletins de ocorrência por homofobia subiu 4,4 vezes de 2022 a 2025, mas isso pode ser mais violência, mais gente registrando, ou as duas coisas; o número sozinho não diz qual.
- Quando o governo federal ou estadual mudou, a taxa de homicídio de toda a população às vezes subiu e às vezes caiu; no país, a queda começou em 2018, ainda no governo Temer. O artigo mostra o que aconteceu; dizer que foi por causa do governo não é possível com estes dados.
- O que resolveria: uma pesquisa repetida, perguntando às pessoas sobre violência; e, para as mortes, registrar a orientação sexual no óbito ou ligar o óbito a outra fonte que a registre.

## 7. Elementos retirados do artigo na versão 0.4 e motivo

| Elemento da versão 0.3 | Motivo da retirada |
|---|---|
| Resumo e Abstract em tópicos com negrito | o resumo passou a ser um parágrafo único em prosa |
| "Resumo para quem não é cientista", "Como ler este artigo" e "Respostas diretas" (Tabela 2 antiga) | repetiam as conclusões; os termos passaram a ser definidos no texto corrido e no glossário (Apêndice C), e os vereditos ficaram na Tabela 11 da Discussão |
| Caixas de destaque por seção e caixas de demonstração | o paper não usa caixas; as demonstrações viraram listas numeradas no texto |
| Contagens de fontes, scripts e revisores no título e na antiga seção 3.14; figuras do funil de evidência, das fontes por idioma e tipo e dos pontos de ataque da revisão | ilustração de processo, sem dado de resultado; a busca é descrita numa frase do Método e o inventário fica no repositório |
| Tabela 13 (correções) e anotações de correção no corpo | o texto deve apresentar o resultado vigente; o histórico fica neste arquivo |
| Seção 4.4 e Tabela 11 (respostas à revisão adversarial) e Tabela 32 (triagem) | material de processo; a Discussão traz as objeções que mudam a interpretação, com resposta e dado |
| Anexo C (índice do repositório), Anexo D (lidos só pelo resumo), Anexo E (o que não está no repositório) e PDF separado de anexos | o artigo passou a um PDF único; o índice virou a Tabela D1, e os demais itens ficam neste arquivo |

## 8. Correções da versão 0.4.1 (25 de outubro de 2026)

A versão 0.4 (paper.md, SHA-256 f283475e8853e8cec20278a46503bd756f0f68bc288249e8cc367e9980c7f69f) passou por um segundo exame: um juiz de rubrica (811 de 1.000; o prompt tinha o texto inteiro com os apêndices, mas o juiz leu só parte dele, ver seção 9), o mesmo modelo de outra família que revisou a v0.2 e um terceiro modelo. Os relatórios e a triagem item a item estão em [`revisao/`](revisao/) (`S2-TRIAGEM.md`, `S2-ASTRA-A2.md`, `F-LAUDO.md`). A versão 0.4.1 aplicou todos os itens que procederam ou procederam em parte; nenhuma análise nova foi feita, e todo número inserido vem de arquivo do repositório indicado abaixo.

| O que estava escrito (v0.4) | O que vale (v0.4.1) | Origem do achado; arquivo |
|---|---|---|
| Resumo: mortalidade fora do Brasil "é maior (1,31)", sem a regra que dá o veredito | "sustentada" pela regra complementar, posterior aos estudos, e "parcial" pela pré-registrada; dado oficial de registro ligado ao censo | J01, S01, M13 |
| Resumo: "50 de 160 (31,3%) são verificáveis" como prova de que a contagem não é total | fração verificada na fonte citada, que não é piso nem teto do total; 40 de 160 (25,0%) com correspondência estrita | A3, J15, A2-07; `research-2026-10-21-rodada3/F3-ggb/dados/codificacao_A.csv` |
| "A busca de 60 consultas não localizou perseguição por agentes do Estado" (Resumo, seções 3.8, 4.1 e 7) | a busca cobre os seis governos federais (nome do presidente e período); agentes estaduais e locais não foram inventariados; omissão em cinco mandatos e dois episódios de hostilidade em 2019 no Resumo | A2-04, M3; `research-2026-10-21-rodada3/escrutinio/simetria/CRITERIOS.md` |
| Nota da Figura 20: a queda de 2019 é "não distinguível de zero, com poder baixo" | a queda de 2019 é distinguível de zero (-17,0%; -29,5% a -2,4%; p = 0,030), mas o placebo de 2018 também cai, e por isso não é atribuível à troca | A2-03; `dados/presidencia/c09_d1_resultados.csv` |
| Captura-recaptura: só 186 (175 a 198) | 186 (175 a 198); de 151 a 221 conforme a regra de pareamento e o recorte, parcela do GGB de 53% a 69% | A2-08; `research-2026-10-21-rodada3/F3-ggb/dados/captura_recaptura_sensibilidade.json` |
| Intervalo do painel lido como "efeitos menores não são detectáveis" (seção 3.6, Tabela 11, Figuras 16 e 21, glossário) | intervalo = valores compatíveis com os dados; efeito mínimo detectável = efeito com 80% de poder; efeitos menores têm poder abaixo de 80% | A2-05 |
| Hipótese 7 "não sustentada", sem ressalva de poder | "não sustentada pelo que foi medido; com 1 de 49 contra 2 de 38, a diferença não é detectável (p = 0,58)" | M1 |
| Figura 25: coluna N4 "não sustentada" (vinho); linha "Gays morrem mais que héteros?" | coluna N4 "não testável" (cinza: nenhuma fração nacional estimada); linha "LGBT+ morrem mais que as demais pessoas?"; N1 "ocorrência" | F-LAUDO A2, A2-22; `paper/figures/fontes/vereditos_tabela1_tabela5.tsv` |
| Nota da Figura 11: "estimativa da mesma grandeza", "concordam no sentido"; Tabela A5 "comparável ao Sinan" | parcelas de universos diferentes, que não se validam; "mesmo recorte de orientação do Sinan" | A2-02, M11 |
| Anotações dentro das imagens: "o painel não enxerga efeitos menores que isto" (Figura 16), "só efeitos além dos traços pretos seriam detectados" (Figura 21), "não se enxerga efeito" (Figura 18), seta "para o Sinan igualar a PNS" (Figura 11) | "faixa compatível com os dados"; "além dos traços pretos, poder de 80% ou mais"; "não se distingue de zero"; seta retirada | A2-05, A2-02; `paper/figures/make_figures.py` |
| Figuras 18 e 19: letra interna de cerca de 5 pt impressa a 14 cm; título do painel (b) "sinais contraditórios"; anotação "ainda com Temer" | 9,5 pt na figura (7,4 e 7,6 pt impressos); "a mesma queda nos dois sentidos"; "a queda começou em 2018" | pedido do autor (E5); F-LAUDO B6, B7 |
| Campo de motivo do Sinan: faltante "de 42% a 45%" (2023-2025) e "45%" em 2025 | 42% a 44% e 44% (arredondamento meio para cima sobre as contagens; 2025 = 44,47%) | conferência E5; `dados/sinan/serie_campo55_uf_ano.csv` |
| "11% de faltante em Roraima a 61% no Distrito Federal" | motivo ignorado ou em branco, em 2023 | M12; `dados/sinan/resumo.md` |
| Disque 100: "1,4% a 1,5% desde 2022" | 1,4% a 1,5% de 2022 a 2025; 1,9% em 2026, até setembro | A2-20; `dados/disque100/saidas/d100_serie_anual.csv` |
| Anuário: série sem menção a revisões | 2023 = 2.090 na edição de 2024 e 1.633 na de 2025; 2024 = 2.480 e 2.567 | M8; `dados/anuario/README.md` |
| Comissão Nacional da Verdade: "de 300 a 500 pessoas eram levadas por dia" | retirado (trecho sem âncora no registro de fontes do repositório); entra o trecho ancorado da p. 301 sobre a ideologia homofóbica do regime | M9, A2-14; `dados/regimes/sources.jsonl` |
| ONS: população do estudo sem seleção | 59,0% das pessoas de 16 anos ou mais do Censo; vinculação de 94,6% e 90,2%, com pesos de pós-estratificação | A2-10 |
| Tabela 4 e Figura 5: "fora do Brasil", com estudo brasileiro e meta-análise de violência | "evidência brasileira e internacional"; McLellan et al. (2026) na Tabela 4 | J03, A2-24 |
| GGB e ANTRA: "associação privada de ativismo" | "associação da sociedade civil (ativismo LGBT+)", como as demais organizações | F-LAUDO B8 |
| Selo "de cada arquivo do repositório"; trilha leve "recalcula todos os números" | selo dos arquivos distribuídos, exceto o artigo, seu PDF e as ferramentas que o constroem; trilha leve = etapas da matriz de reprodução | A2-16, S04, A2-17 |

Itens que procederam como limite e foram declarados no texto: fonte primária como categoria documental (A2-09), o nível de documento na régua de regimes (A2-13), literatura de tratamento contínuo e reversível (A2-11), coortes com HIV e seleção pela imprensa (M05, M06), hipótese do efeito de desenho em painel e da sobreamostra (A2-18, M14). Itens não aplicados e motivo: suplemento separado e corte de figuras (F-LAUDO M15; contraria a decisão do autor de um PDF único com figuras e tabelas no artigo); faixa de ±132 mil "incluindo a incerteza do total" (F-LAUDO B10; a decomposição não está no arquivo de origem); "Democratas, hoje União Brasil" (F-LAUDO B2; exigiria fonte nova); a PNS de 2026 "em coleta" (A2-23: exigiria fonte nova com registro no ledger; a agenda cita a edição seguinte da PNS pelo plano de trabalho já referenciado).

## 9. Correções da versão 0.4.2 (25 de outubro de 2026)

A versão 0.4.1 (paper.md, SHA-256 4a775cccceb6d7b5eb112b98320d938a7358a16c62c78093b60a25f05127bc02) passou por um terceiro exame, agora com leitura integral comprovada: o mesmo prompt do juiz de rubrica, com o artigo inteiro, enviado a dois modelos de famílias distintas pela assinatura do fornecedor (Astra, 868 de 1.000; Gemini, 941 pela soma das dimensões e 881 com a regra de pontuação do próprio prompt), cada um obrigado a citar a última frase do Apêndice D e uma frase da seção 3.9 como prova de que leu até o fim. Dos 16 descontos, 9 procederam ou procederam em parte (nenhum de severidade alta), 3 eram limites já declarados e 2 não procederam; notas, prova de leitura e triagem em [`../paper/AUDIT.md`](../paper/AUDIT.md). A versão 0.4.2 aplicou os itens que procederam; nenhuma análise nova foi feita, e todo número inserido já estava no arquivo do repositório indicado abaixo.

| O que estava escrito (v0.4.1) | O que vale (v0.4.2) | Origem do achado; arquivo |
|---|---|---|
| Objeção 7 (seção 4.3): a busca de atos de governo "contou episódios de hostilidade e de proteção nos dois lados" | o procedimento é simétrico (10 consultas por mandato, a mesma regra de leitura e os mesmos tipos de ato), e o resultado não: proteção só nos quatro mandatos do PT (10 episódios); retórica hostil e ato administrativo hostil, um episódio cada, só em 2019; omissão ou corte de política nos dois lados (4 e 4) | Astra v4-3 (consistência); Tabela 8; `research-2026-10-21-rodada3/escrutinio/simetria/` |
| Seção 4.4: com o levantamento de vitimização, "a série policial, o campo de motivação do Sinan e as contagens da sociedade civil passariam a ser calibráveis" | os registros de ocorrência e de notificação passariam a ser calibráveis; as contagens de mortes da sociedade civil, não, porque dependem do registro da orientação e da identidade no óbito (terceira implicação), como diz a seção 3.13 | Astra v4-3 (contradição com a seção 3.13) |
| Seção 3.7: trocas de governador comparadas "entre os três anos anteriores e os três posteriores", sem dizer que a janela é cortada | as janelas ficam dentro de 2012 a 2024, com ao menos um ano de cada lado; 47 das 67 trocas têm janela completa, e as 20 de 2013, 2014, 2023 e 2024, janela mais curta; a referência usa a mesma janela; só com janela completa, 20 subiram e 27 caíram (mediana -0,8%; referência +0,8% a +11,0%; p = 0,008) | Astra v4-3 (omissão de método); `dados/exposicao/PREREGISTRO-C10.md`, `dados/exposicao/c10_resultados.md` (recorte "a_janela_completa") |
| Tabela A17 e laudo de mídia: 16 linhas, que somam 811 itens, contra os 871 da amostra codificada citados no texto | a linha que faltava, F3 na Wikipédia (universo 197, amostra 60, 1 que afirma ou atribui, N estimado 3 [1-17], 1 que rebate, 0 de 1 com fonte primária, 0 de 1 citando GGB, ANTRA, TGEU ou ONU), entra no laudo e na tabela; a soma passa a 871 | Gemini v4-3 (a causa que o juiz apontou, a linha de base da Tabela A18, não procede); `research-2026-10-21-rodada3/discurso/midia/amostra_codificada.csv`, `_estimativas.txt`, `_estatisticas_amostra.txt`; `docs/laudos/MIDIA.md` |
| Sete palavras-chave (violência; LGBT+; mortalidade; subnotificação; identificabilidade; pré-registro; reprodutibilidade) e as sete em inglês | seis: sai "reprodutibilidade" ("reproducibility"); a reprodutibilidade é propriedade do pacote, descrita na seção 6, e as seis restantes nomeiam o objeto, o problema de medida e o método | Astra e Gemini v4-3 (máximo de seis na rubrica) |
| Latim: um uso (post hoc, seção 5.4) | três usos, cada um explicado na própria frase: a priori (seção 2.4, pré-registro), ceteris paribus (seção 3.6, leitura do coeficiente com os efeitos de estado e de ano mantidos) e post hoc | Astra e Gemini v4-3 (regressão da reescrita da v0.4, que tinha quatro) |
| Tabela A16: "negros / não negros: limite inferior (raça ignorada descartada)" = 2,56, com o extremo B (2,42) abaixo dele | "negros / não negros: cenário (raça ignorada descartada)"; o rótulo mudou no gerador e no arquivo de saída, e nenhum número mudou | Astra v4-3 (vocabulário); `dados/sim/padroniza_idade.py`, `dados/sim/asr_brasil.md` |
| Glossário: numerador B = "contagem do GGB menos todas as pessoas trans da tabela de identidade" | "numerador A (homicídios mais latrocínios da contagem do GGB) menos todas as pessoas trans da tabela de identidade", como na seção 3.4 | Astra v4-3 (vocabulário) |
| Seção 5.2: o escore partidário "tem ruído que atenua o coeficiente" | atenua se o erro de medida for clássico (independente do escore verdadeiro e dos demais termos do modelo); se não for, a direção do viés não é garantida | Astra v4-3 (suposição não declarada) |
| `docs/revisao/S2-TRIAGEM.md`: "811 (v4-1) julgou o paper.md INTEIRO, com os Apêndices A–D" | o prompt continha o artigo inteiro, mas o juiz leu só parte (corte do programa do juiz em prompts de 100.000 bytes ou mais (descarga do programa grok 1.0.62, corrigida com --verbatim; correção de 2026-10-26)); correção datada no topo da cópia, original intacto | terceiro exame; raciocínio gravado das rodadas v4-1 e v4-2 (fora do git) |
| Seção 8 deste arquivo: "811 de 1.000, texto inteiro com os apêndices" | "o prompt tinha o texto inteiro com os apêndices, mas o juiz leu só parte dele" | idem |

Itens não aplicados e motivo: E-E-A-T (a média das 97 referências é 80,1, acima do limiar de 75; nota individual baixa não é critério); "Lei de Campbell" (o autor já é nomeado e citado, Campbell, 1979). Limites já declarados e mantidos: densidade técnica (TDI 1,94, abaixo de 3, pela escrita para leitor não especialista, decisão do autor); fontes de imprensa e instrumento normativo não lido nos dois episódios de 2019 (Nota da Tabela 8 e seção 3.8). Também mudam, sem correção de conteúdo, a versão do texto (0.4.2) e o selo citado na seção 6 (o selo é refeito porque o laudo de mídia, o gerador da Tabela A16, esta lista e a cópia da triagem estão dentro dele).

## 10. Correções da versão 0.4.3 (25 de outubro de 2026)

A versão 0.4.2 (paper.md, SHA-256 3469a16764dc4f5382634a39c6d627b8065a6cbb51666402b64a460d6e01e23b) recebeu a rodada final do juiz de rubrica, com leitura integral comprovada (Astra, 885 de 1.000; notas e leitura de cada desconto em [`../paper/AUDIT.md`](../paper/AUDIT.md)). Três descontos procederam (um médio, dois baixos) e ficaram como pendências; a versão 0.4.3 os aplica, aponta o terceiro exame no próprio artigo e corrige uma página com duas linhas do glossário. São mudanças de texto, sem número novo e sem análise nova; a versão 0.4.3 não foi julgada de novo.

| O que estava escrito (v0.4.2) | O que vale (v0.4.3) | Origem do achado; arquivo |
|---|---|---|
| Seção 4.1: a terceira hipótese "não é sustentada em nenhuma das duas formas" e "não há evidência de invenção, entendida como fabricação de casos", contra a Tabela 11, que diz "contrariada como invenção" | um só veredito, o da Tabela 11 no vocabulário da seção 2.2: "não é sustentada como taxa ou total e é contrariada como invenção, isto é, como fabricação de casos"; a invenção "é contrariada pela evidência no nível de ocorrência (N1)", pelos mesmos números (50 de 160 casos verificáveis, 40 com correspondência estrita; duplicata de 0,3%) | Astra v4-4 (consistência) |
| Seção 2.6: "nenhum número entra no artigo sem arquivo local que o produza ou o cite com página, e nenhum modelo foi usado para gerar dado", na mesma seção que diz que modelos codificaram itens de discurso | os modelos codificaram itens de discurso, "com a dupla codificação descrita abaixo e as comparações pelo teste exato de Fisher da seção 3.10"; "nenhum número de resultado foi gerado por modelo: todo número entra no artigo a partir de arquivo local que o produza ou o cite com página, e as contagens de discurso somam os rótulos gravados item a item em arquivo" | Astra v4-4 (consistência) |
| Seção 2.6: no segundo exame, o juiz de rubrica e os outros dois modelos "examinaram o artigo inteiro" | "examinaram o artigo, o juiz só em parte, por um corte no programa que o executava" | coerência com a seção 9 deste arquivo (corte do programa do juiz em prompts de 100.000 bytes ou mais (descarga do programa grok 1.0.62, corrigida com --verbatim; correção de 2026-10-26)) |
| Seção 2.6 e Tabela D1: o terceiro exame não era apontado no artigo (só no README e em `paper/AUDIT.md`) | seção 2.6 e Tabela D1 apontam o terceiro exame: vereditos em `paper/build/juiz/rodada-v4-3-*` e `rodada-v4-4-*`, adjudicação em `paper/AUDIT.md`, correções nas seções 9 e 10 deste arquivo | pendência registrada na rodada final v4-4 |
| Tabela A17 e `docs/laudos/MIDIA.md`, seção 4: F2 × Parlamento "49 [43-53]", intervalo de Wilson numa contagem do universo inteiro (56 de 56 falas codificadas) | "49", sem intervalo, como nas outras três linhas de censo (F1 × Parlamento, F2 × Wikipédia, F4 × Parlamento); o cabeçalho da seção 4 do laudo diz que, nas linhas de censo, o N estimado é a própria contagem; a soma da coluna da amostra segue 871 | Astra v4-4 (correção factual); `research-2026-10-21-rodada3/discurso/midia/_estimativas.txt` continua a imprimir o intervalo de Wilson em todas as linhas, por construção do script que o gera |
| Glossário, verbete do numerador B: "numerador A (homicídios mais latrocínios da contagem do GGB) menos todas as pessoas trans da tabela de identidade; conta de cenário, e não limite inferior" | "numerador A (homicídios e latrocínios do GGB) menos todas as pessoas trans da tabela de identidade; não é limite inferior", com o mesmo sentido | página: na v0.4.2, o verbete ocupava três linhas e deixava as duas últimas linhas do glossário e a nota numa página própria; com duas linhas, o Apêndice C volta a duas páginas |

Também mudam, sem correção de conteúdo, a versão do texto (0.4.3) e o selo citado na seção 6 (o selo é refeito porque o laudo de mídia e esta lista estão dentro dele).

## 11. Correções da versão 0.4.4 (26 de outubro de 2026)

A versão 0.4.3 (paper.md, SHA-256 b21b2dd4a89cc61577bb481c6a9365ee69c49f363ee0e6113499a83011e5d6c3) recebeu a rodada v4-5 do juiz de rubrica, agora com o texto inteiro entregue na mensagem ao modelo que executa o juiz (opção `--verbatim` do programa de linha de comando) e prova de leitura do fim do texto e de uma frase depois de 60% dele (928 de 1.000; notas e triagem em [`../paper/AUDIT.md`](../paper/AUDIT.md)). Dos sete achados críticos, três pediam precisão e foram aplicados (Tabela A2, seção 3.5, fonte primária da ADO 26); os outros são limites já declarados no texto. São mudanças de precisão, sem número novo e sem análise nova; a versão 0.4.4 não foi julgada de novo.

| O que estava escrito (v0.4.3) | O que vale (v0.4.4) | Origem do achado; arquivo |
|---|---|---|
| Tabela A2: negros 916 e não negros 637 (soma 1.553) ao lado de 1.554 adultos LGB+ (796 homens e 758 mulheres), sem dizer onde está a diferença | a Nota da tabela diz a regra (negros = pretos e pardos, códigos 2 e 4 da variável C009, cor ou raça; não negros = brancos, amarelos e indígenas, códigos 1, 3 e 5) e que 1 adulto LGB+ tem cor ou raça ignorada (código 9) e fica fora das duas linhas; as células não mudam. Conferido no microdado da PNS 2019 com a mesma leitura de `dados/pns/seguro_pns2019.py`: entre os 1.554 LGB+, 607 brancos, 183 pretos, 10 amarelos, 733 pardos, 20 indígenas e 1 com cor ou raça ignorada | Grok v4-5 (consistência); `paper/tools/make_anexos.py` (Nota), `dados/pns/seguro_pns2019.py` (regra), `dados/pns/seguro_pns2019.md` (células) |
| Seção 3.5: "a parcela LGB+ é 7,1% (IC95% de desenho 5,1 a 9,1; 179 de 3.291)" | "a parcela LGB+ ponderada pelo desenho amostral é 7,1% (IC95% de desenho 5,1 a 9,1) [...]; na amostra não ponderada, são 179 de 3.291 vítimas, razão que não reproduz o percentual ponderado"; a Nota da Tabela A5 diz que a coluna % é a razão de totais ponderados pelo peso do desenho e que as colunas de n são contagens da amostra, sem ponderação | Grok v4-5 (consistência); `dados/pns/c05_razao_direta.csv` (base b, total: 7,12; 3.291 vítimas e 179 LGB+ na amostra) |
| Tabela 1, linha do boletim de ocorrência: "enquadramento adotado após o julgamento da Ação Direta de Inconstitucionalidade por Omissão 26 pelo Supremo Tribunal Federal, em 2019", sem a decisão nas Referências | "... pelo Supremo Tribunal Federal (2019)", e o inteiro teor do acórdão da ADO 26 entra nas Referências (Plenário, 13 de junho de 2019; fonte primária já no registro de fontes: `research-2026-10-21-rodada3/F8-literatura/sources.jsonl`, id `stf-ado-26-mi-4733`, SHA-256 1ea5266648e9099961200073c8fed5e6ea0cd1a078fa8314d5b18b3fe66e1c81; `docs/laudos/F8-literatura-README.md`, linha C6). O arquivo é o acórdão da ADO 26; o do Mandado de Injunção 4.733 é outro documento e não é citado | Grok v4-5 (correção factual) |
| Seção 2.6 e Tabela D1: o exame da versão 0.4.3 não era apontado | apontado como quarto exame: veredito em `paper/build/juiz/rodada-v4-5.json`, triagem em `paper/AUDIT.md`, correções nesta seção | coerência com `paper/AUDIT.md` e o README |
| `docs/revisao/S2-TRIAGEM.md` (nota do topo e placar), `CHANGELOG.md` (entrada da v0.4.2) e as seções 9 e 10 deste arquivo: "corte de cerca de 94 KB" do programa do juiz | corte do programa do juiz em prompts de 100.000 bytes ou mais (descarga do programa grok 1.0.62, corrigida com `--verbatim`; correção de 2026-10-26): cerca de 94 KB é o tamanho do começo entregue ao modelo, e não o limiar | medição de 2026-10-26 (`paper/AUDIT.md`, seção "Todas as rodadas do juiz") |

Itens não aplicados e motivo: os dois episódios hostis de 2019 (a fala de 25 de abril e a ordem de suspender verba de agosto) seguem com fonte de imprensa, porque o registro de fontes não tem transcrição oficial da fala nem instrumento normativo da ordem (`research-2026-10-21-rodada3/escrutinio/simetria/eventos_C18.csv`, eventos E17 e E20; `SIMETRIA.md`); o limite continua declarado na seção 3.8 e na Tabela 8, e nenhuma fonte foi acrescentada sem estar no registro. Limites já declarados e mantidos: densidade técnica (TDI 1,93, abaixo de 3, pela escrita para leitor não especialista, decisão do autor); a regra complementar de elegibilidade, definida depois de conhecidos os estudos (seções 2.2 e 3.2 e Tabela B1); a anterioridade dos pré-registros, que o SHA-256 não prova sem carimbo de tempo externo (seções 2.4 e 5.4); a ausência de parecerista humano (seção 2.6); a ligação entre caso e fonte da amostra do GGB de 2019, que exige a lista nominal não distribuída (seção 3.4); a recência das referências, no limite (49 de 98 de 2023 em diante, 50,0%, com a referência nova do Supremo Tribunal Federal, de 2019). Também mudam, sem correção de conteúdo, a versão do texto (0.4.4) e o selo citado na seção 6 (o selo é refeito porque esta lista, o CHANGELOG, o README e a cópia da triagem estão dentro dele).

## 12. Correções da versão 0.5 (30 de outubro de 2026)

A versão 0.4.4 (paper.md, SHA-256 fdd8e9d48b32a8bef3d0d7f226c95f665677185781f168e69562cf4b7aea0ced) deu lugar à versão 0.5 do artigo ([`../paper/v05/`](../paper/v05/)), reestruturada em dois eixos, com o Material Complementar MC1 a MC12 e o glossário como Apêndice A (lista das mudanças de estrutura no `CHANGELOG.md`). Na reconferência de cada afirmação contra o arquivo que a produziu (quadro em [`../paper/v05/QUADRO-E2.md`](../paper/v05/QUADRO-E2.md)), quatro frases da 0.4.4 precisaram de correção. São correções de precisão ou de atribuição; o número antigo fica ao lado.

| O que estava escrito (v0.4.4) | O que vale (v0.5) | Origem do achado; arquivo |
|---|---|---|
| Seção 3.1: entre as 179 vítimas LGB+ de violência física, o agressor foi "familiar em 31,2% (19,3%; razão de 1,62, IC95% 0,96 a 2,72)" | "31,2% contra 19,2%": o valor bruto dos heterossexuais é 19,2466%, e o 19,3 vinha de arredondar duas vezes (19,25 na tabela de duas casas, depois 19,3); a razão e o intervalo não mudam | conferência do quadro de afirmações (A14); `dados/pns/agressor_risco_pns2019.csv` (bloco `fatia_entre_vitimas`, linha Familiar: 0,19246602) e `agressor_risco_pns2019.md`, seção 1 (19,25). Nota: `dados/pns/seguro_pns2019.md` não traz a fatia por tipo de agressor, e o 19,3 não está nesse arquivo; a origem do erro é o arredondamento em duas etapas, e o microdado que dá o valor correto é o lido por `agressor_risco_pns2019.py` |
| Seções 2.2, 3.12 e 4.4 (ONS e Home Office): "Reino Unido" ("Escritório Nacional de Estatística do Reino Unido"; "No Reino Unido, o levantamento estima 176.000 incidentes de ódio por ano"; "como fez o Reino Unido com o Censo") | "Inglaterra e País de Gales": o Censo ligado aos óbitos (ONS) e o levantamento de vitimização e o registro policial (Home Office) cobrem a Inglaterra e o País de Gales, e não o Reino Unido inteiro | fonte primária da ONS e do Home Office; `paper/v05/QUADRO-E2.md`; ledger da revisão de literatura |
| Seção 3.5: o motivo da ficha de violência do SUS fica sem informação útil "em 42% a 44% de 2023 a 2025" | "42,5% a 44,5%": 42,5% em 2024 e 44,5% em 2025 são os extremos da série 2023-2025; arredondar 44,5 para 44 é ambíguo e escondia a casa que decide | `dados/sinan/resumo.md`, série 2015-2025 (coluna do faltante efetivo do campo 55); `QUADRO-E2.md`, afirmação A20 |
| Seção 3.10: "o valor de 35 anos leva a uma única autora citada pela ANTRA, que a própria organização diz não ser estudo sistemático (Benevides, 2026)" | o dossiê da ANTRA de 2019 diz que não há estudos sistemáticos sobre a expectativa de vida dessa população e atribui o número a Antunes (2013, como citado em Benevides & Nogueira, 2020, p. 32); mais adiante o atribui a uma reportagem da Agência Brasil (Martins, 2018, p. 77); o que o dossiê calcula é a idade média das vítimas de assassinato, de 29,7 anos em 2019 (p. 30), que não é expectativa de vida | leitura do dossiê da ANTRA de 2019 (páginas citadas); `research-2026-10-21-rodada3/discurso/` e Material Complementar MC9 (11 discursos do Congresso com 27 a 36 anos, nenhum com fonte primária) |

Também mudam, sem correção de conteúdo, a estrutura do texto (dois eixos, atos de governo no MC7, parágrafo de simetria na seção 3.5 com a checagem da LiHS, Figura 8 nova) e o selo citado, que é refeito porque esta lista, o `CHANGELOG.md`, o README e os arquivos novos de `paper/v05/` (figuras e README) estão dentro dele. A planilha da LiHS não é distribuída (nomes de vítimas e de acusados); ficam os metadados e a tabulação em [`../research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md`](../research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md). O texto do Material Complementar que diz "cópia no repositório" para essa planilha não foi alterado e deve ser lido com esta ressalva.
