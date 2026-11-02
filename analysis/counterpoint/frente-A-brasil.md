# Frente A (Brasil) - contraponto às estatísticas de mortes LGBT+ (2026-10-30)

playbook loaded: factual-context + paper-deep-dive

Pergunta: no Brasil, que estudos, bases, relatórios ou contagens de autores conservadores, de direita, religiosos ou críticos do movimento LGBT contestam ou oferecem alternativa às estatísticas do GGB, ANTRA, Disque 100, Atlas da Violência e à frase "o Brasil é o país que mais mata LGBT"?

Regra de afiliação: só consta quando a própria fonte a declara. Nada inferido.

## Resposta curta

1. Só existe UMA contra-base com dados auditáveis e método descrito: a checagem caso a caso do relatório GGB 2016 (347 vítimas), da Liga Humanista Secular (LiHS), publicada em 01/05/2019, com planilha pública. Resultado dos autores: 31 casos (8,9%) com motivação homofóbica comprovada.
2. Há uma segunda revisão caso a caso, mais antiga e de autor individual (Dario Di Martino, PDF de 02/2016, sobre o GGB 2013): 313 mortes, 9 classificadas por ele como crime homofóbico.
3. A revisão do dossiê Lesbocídio (2 de 126) é de Daniel Barbosa Reynaldo. A versão primária dessa análise NÃO foi aberta (Wayback caiu). Abri só dois posts de 2020 do mesmo blog.
4. Tudo o mais é crítica de método (opinião, parlamentar, press) sem base própria. Nenhum artigo revisado por pares de autor crítico foi achado. Nenhuma crítica conservadora a Disque 100 ou Atlas da Violência foi achada.
5. As únicas checagens jornalísticas da frase "país que mais mata" não a chamam de falsa: Truco "impossível de provar" (2018), Lupa "insustentável" (2019), Aos Fatos "impreciso" (para trans, 2018).

## Tabela de itens ranqueados

Ordem: dado próprio auditável primeiro, depois crítica com números, depois só crítica.

| # | Item | Autor / data | Tipo | Dado próprio auditável? | Números principais |
|---|------|--------------|------|-------------------------|--------------------|
| 1 | Checagem LiHS do GGB 2016 | Eli Vieira, Camila Mano, Daniel Reynaldo, David Agape, Vanessa Bigaran; 01/05/2019 (a página exibe também 10/05/2019) | think tank (Liga Humanista Secular, associação) | SIM: planilha com 347 linhas, fontes por caso, código R | 31/347 = 9% "sim"; ver tabulação abaixo |
| 2 | "A Farsa dos Crimes Homofóbicos no Brasil" | Dario Di Martino; PDF criado 02/2016 (metadado) | livro autopublicado (blog) | SIM, parcial: lista caso a caso com link de notícia, sem planilha | 313 mortes GGB 2013; 9 homofóbicas; 47 gay mata gay; 257 outras |
| 3 | Blog "Quem a homotransfobia não matou hoje?" | Daniel Barbosa Reynaldo; posts de 2020 abertos | blog | Casos citados com links; a análise 2/126 não aberta | ver item 3 |
| 4 | Gazeta do Povo, 02/05/2019 | Tiago Cordeiro | imprensa (seção Ideias) | NÃO (relata o item 1) | 347 / 31 / 9% |
| 5 | Gazeta do Povo, 01/03/2019 | Tiago Cordeiro | imprensa (Ideias) | NÃO | ponto de partida |
| 6 | Gazeta do Povo, 25/06/2023 | Eli Vieira | imprensa (opinião) | NÃO | Observatório 2022: 273; só 3 casos detalhados |
| 7 | Gazeta do Povo, 05/07/2023 | Eli Vieira | imprensa (opinião) | NÃO | sem número novo |
| 8 | Gazeta do Povo, 02/02/2021 | Eli Vieira | imprensa (opinião) | NÃO | ANTRA 175 (2020); 43% (cálculo de terceiro, não aberto) |
| 9 | MATRIA / Substack de Marina Colerato, 25/11/2024 | MATRIA | associação / blog | cálculos próprios sobre TGEU; sem planilha | 8º lugar per capita entre 38 países |
| 10 | Instituto Liberal, 2015 | Enézio de Deus | think tank (blog) | NÃO | sem número |
| 11 | Agência Câmara, 15/10/2014 | Ronaldo Fonseca (Pros-DF) | parlamentar | NÃO | "infundadas" |
| 12 | Fact-checks Truco / Lupa / Aos Fatos | Rudnitzki 2018; Marés e Moraes 2019; Menezes 2018 | fact-check | n.a. | ver seção |

### Item 1 - Checagem LiHS (primário, aberto)

[SOURCE: factual-context:web:https://lihs.org.br/sociedade/homofobia/]
[SOURCE: factual-context:web:https://docs.google.com/spreadsheets/d/1QdVdDhPLsFomf9edOscMz-hZhIitqwkSuSi3I7XV3Po/]

- Título na página: "Principais estatísticas brasileiras de morte por homofobia são falsas, conclui checagem independente".
- Afiliação declarada na própria página: Eli Vieira "biólogo geneticista e presidente da Liga Humanista"; Daniel Reynaldo "administrador do blog Quem a Homotransfobia Não Matou Hoje?"; David Agape e Vanessa Bigaran "fundadores da Agência Dossiê"; página pertence à LiHS. A mesma página não declara afiliação política.
- Método dos autores: refizeram o GGB 2016, buscaram online cada nome e local, recuperaram fontes que o GGB não divulgou, classificaram cada caso em "sim / não / inconclusivo". Critério citado: "houve motivação homofóbica se há indícios de motivação homofóbica".
- Números da página: 347 vítimas; 30 excluídas (exterior, duplicadas, sem fonte); 20 suicídios retirados; 258 homicídios restantes; 31 motivados por homofobia; "227 de 258 (88%)" tratados como erro; "31 de 347 (9%)".
- Dados que ABRI e tabulei eu mesmo (CSV exportado do Google Sheets, 347 linhas, copiado para `data/lihs-checagem-ggb2016.csv` na pasta de trabalho do autor e não distribuído aqui, porque tem nomes de vítimas e de acusados (metadados e tabulação em `data/lihs-checagem-ggb2016.META.md`), sha256 `0dc25783bfc422ec635826009fbdfbda4efc41ecd7dca0fa05fc469a9179d5ad`):

| Coluna Motivacao_Homof | Casos | % de 347 |
|------------------------|-------|----------|
| Sim | 31 | 8,9% |
| Não | 127 | 36,6% |
| Inconclusivo | 159 | 45,8% |
| Não localizado | 23 | 6,6% |
| Exterior | 6 | 1,7% |
| Duplicado | 1 | 0,3% |

- Coluna Revisor: um revisor por caso na quase totalidade (DA 175, CM 81, EV 32, VDB 24, DR 18, sem revisor 14; 3 casos com dois). Não vi nenhum cálculo de concordância entre revisores.
- Ressalvas para quem for citar (minhas, de leitura da planilha):
  - 9% é o piso "comprovado" sob o critério dos autores, não uma estimativa da fração verdadeira. 159 casos (45,8%) ficaram inconclusivos, e o "88% erro" da página soma não e inconclusivo.
  - Reconciliado com a planilha: as categorias Homicídio, Latrocínio, Culposo e Triplo somam 266; menos 8 linhas marcadas Exterior ou Não localizado = 258, que bate com a página. Idem suicídios: 23 na coluna Crime menos 3 "Não localizado" = 20, que bate com a página. Dos 258, a planilha dá Sim 31, Não 100 (55+6+39), Inconclusivo 127 (125+2): então "227 de 258 = erro" soma 100 "não" e 127 "inconclusivo".
  - Um revisor por caso e critério "indício" são escolhas que um revisor externo vai atacar, em qualquer direção.
  - Os autores incluem quem já tinha publicado crítica ao GGB (Reynaldo) e fundadores de agência de dossiês; não é checagem de terceiros independentes, apesar do título.
- Réplica do GGB: não achei documento de resposta. A Gazeta (item 5) atribui a Luiz Mott "erros não chegam a 5%". A Gazeta 2023 afirma que as ONGs "jamais responderam" à checagem de 2019; isso é afirmação do jornal, não verifiquei.
- Também no ledger, abertos: planilha GGB 2016 arquivada (4 págs, sha256 `d2c29ddab2ab30d5b954d23425414a44cbc525ac1811ab06ae6aefa7238ec5fe`) [SOURCE: factual-context:web:https://web.archive.org/web/20190208184923/https://homofobiamata.files.wordpress.com/2017/01/planilha-2016.pdf]; app R/Shiny `https://app.elivieira.com/checagemhomofobia` (HTTP 200, conteúdo não inspecionado).
- Sobre o "6% de 2017, ainda parcial" citado no ponto de partida: não achei versão primária (nem planilha, nem post, nem vídeo). A checagem pública cobre 2016, não 2017. Tratar o 6%/42% de 2017 como não verificável.

### Item 2 - Di Martino (primário, aberto)

[SOURCE: factual-context:web:https://web.archive.org/web/20210519175129/https://jornalistadimartino.webnode.com/_files/200000241-eafa8ebf42/A%20farsa%20%20dos%20crimes%20homofobicos%20no%20Brasil-4de2.pdf]

- PDF de 137 páginas (sha256 `58ff97750ca5af1489ce264313e805a276189b2d79cd5a208e3aa60e56bdd625`), metadado de criação 05/02/2016; o texto cita os relatórios GGB 2014 (326) e 2015 (318).
- Método declarado: pega a lista do GGB de 2013 (313 mortes) e analisa "caso a caso"; crime de latrocínio, briga de casal ou gay matando gay não conta; caso sem informação de motivo "decidi não contabilizar".
- Resultado dele: 9 crimes homofóbicos; 47 mortes entre gays; 257 "por outras razões (latrocínio, desavenças e até suicídios)". Conclusão dele: um por 40 dias em vez de um por 28 horas.
- Afiliação como consta no próprio livro (seção "Quem é Di Martino?"): jornalista; ex-membro do diretório estadual do extinto Prona; ex-assessor de deputado estadual (RS). O autor escreve na introdução que o livro "será rechaçado pelos ativistas gays como uma obra reacionária e de direita"; é previsão dele, não autodefinição.
- Auditável: cada caso traz link de notícia; não há planilha. Critério muito mais restritivo que o do item 1 (caso sem motivo conhecido = não). Não é revisado por terceiros. Wikipedia (en) o cita como crítica ao GGB.

### Item 3 - Blog de Daniel Barbosa Reynaldo

[SOURCE: factual-context:web:https://naomatouhoje.blog/]
[SOURCE: factual-context:web:https://web.archive.org/web/20210811222905/https://naomatouhoje.blog/2020/10/04/processo-aberto-por-autoras-do-dossie-lesbocidio-e-arquivado/]
[SOURCE: factual-context:web:https://web.archive.org/web/20201105003552/https://naomatouhoje.blog/2020/11/04/relembre-alguns-dos-casos-mais-marcantes-da-longa-historia-de-fraude-do-grupo-gay-da-bahia/]

- Site vivo devolveu corpo vazio por curl (WebFetch: HTTP 429). Li o snapshot Wayback de 11/08/2021 (autor do perfil: `danielreynaldo1979`) e dois posts.
- Post de 04/11/2020: o autor diz ter criado a página no fim de 2017, "diretamente inspirada" em Milo Yiannopoulos (livro Dangerous), e que o nome é ironia com a página do GGB. Afirma que, depois da página, GGB, ANTRA, Rede Trans e UFRJ pararam de publicar as listas de casos. Isso é afirmação dele, NÃO verifiquei.
- Post de 04/10/2020: relata processo cível 0027541-28.2018.8.19.0210 (autoras do Lesbocídio contra ele); diz que foi condenado em 1ª instância (R$ 18 mil) e absolvido por 3 a 0 na Turma Recursal. Fonte é o próprio réu; não abri a decisão judicial.
- A análise "2 de 126" do dossiê: o número vem da Gazeta 01/03/2019 (item 5). NÃO achei o post ou planilha primária; o Wayback ficou indisponível (429, depois "Temporarily Offline") quando tentei listar os posts de 2018. Fica como lacuna aberta.
- Contraparte: carta aberta de Maria Clara Dias (ANPOF) citada pela Gazeta, não aberta. O dossiê (Peres, Soares e Dias, 2018) declara 126 mortes de lésbicas em 2014-2017 e coleta por redes, sites e jornais; segundo a descrição que li, os autores admitem incompletude.

### Itens 4 a 8 - Gazeta do Povo (seção Ideias)

[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/os-verdadeiros-numeros-sobre-a-morte-de-lgbts-no-brasil-95bmcp4302gyjdozzpjmiuhyl/]
[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/estatisticas-sobre-morte-provocada-por-homofobia-sao-infladas-conclui-estudo/]
[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/ideias-111-a-verdade-sobre-as-estatisticas-sobre-a-morte-de-lgbts/]
[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/brasil-lidera-mortes-de-lgbt-a-verdade-por-tras-das-estatisticas/]
[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/ministerio-dos-direitos-humanos-usa-como-fonte-coalizao-de-ongs-lgbt-que-produz-numeros-questionaveis/]
[SOURCE: factual-context:web:https://www.gazetadopovo.com.br/ideias/estatisticas-sobre-trans-no-brasil/]

- 01/03/2019, Cordeiro (item 5): linha que o ponto de partida citou. Contém os links primários do blog de Reynaldo, do relatório GGB 2018 e da nota de Maria Clara Dias. A própria página é artigo de opinião e diz que as pesquisadoras da UFRJ não responderam aos pedidos de entrevista.
- 02/05/2019, Cordeiro (item 4): relata o item 1; diz 347 casos, 31 "indiscutíveis", 9%, 6 mortes no exterior, duplicados.
- 17/06/2019: podcast "Ideias #111" com Eli Vieira, Guilherme Fiuza e Rodrigo Constantino; sem link para o estudo; repete 9%.
- 25/06/2023, Eli Vieira: Observatório de Mortes e Violências contra LGBTI+ (2022: 273 mortes: 228 assassinatos, 30 suicídios, 15 outras); o jornal diz ter pedido a planilha completa e não obteve resposta; reavalia 3 casos individuais e considera ao menos 2 incertos; critica falta de transparência e cobertura desigual. Também faz argumento de financiamento (Fundo Brasil, Ford, Open Society), que é de natureza distinta e não é auditoria de dado.
- 05/07/2023, Eli Vieira: o relatório do Ministério dos Direitos Humanos sobre discurso de ódio cita o Observatório; sem número novo. A própria Gazeta diz que o relatório ministerial não cita estatísticas das ONGs.
- 02/02/2021, Eli Vieira: ANTRA (175 assassinatos em 2020; "expectativa de vida de 35 anos" seria média de idade de assassinados). Cita a análise de Ágata Cahill (1.593 de 3.664 casos TGEU 2008-2020 = 43%) via link do Twitter e thread; não abri. Remete ao Aos Fatos para dizer que a ANTRA admitiu que, em termos relativos, o Brasil não lidera. Afirma que os dados da ANTRA não são públicos.
- Afiliação: a página não declara afiliação política do jornal nem do autor; Vieira é descrito como biólogo/geneticista. Gazeta 2019: Vieira é "mestre em genética e biologia molecular, doutorado em genética por Cambridge" (a matéria).

### Item 9 - MATRIA (trans, taxa per capita)

[SOURCE: factual-context:web:https://marinacolerato.substack.com/p/transmatematica-taxas-baixas-que]

- 25/11/2024. Tese: "país que mais mata trans" só vale em número absoluto. Números do texto: TGEU 350 assassinatos em 38 países em 2024; Brasil 106, 8º em taxa; população trans estimada 1,88% (3.817.918); taxa trans 2,8 por 100 mil contra 22,8 geral e 3,8 para mulheres; subnotificação necessária para igualar: mais de 8 vezes.
- Faz cálculos e gráficos próprios sobre dados públicos (TGEU, Anuário FBSP, IBGE); não publica planilha. A página não declara afiliação ideológica. Um ponto fraco evidente: a taxa usa uma estimativa populacional de 1,88% que a própria literatura discute; o texto ainda assume que o TGEU é confiável.

### Item 10 - Instituto Liberal (blog, 2015)

[SOURCE: factual-context:web:https://www.institutoliberal.org.br/blog/foi-mesmo-a-homofobia/]
[SOURCE: factual-context:web:https://www.institutoliberal.org.br/blog/mais-um-gay-assassinado-e-as-lesbicas/]

- Enézio de Deus, advogado e doutorando (UCSAL) segundo a página; datas 26/06/2015 e 05/10/2015. Nota do editor: opiniões dos colunistas não representam necessariamente o IL.
- Tese: homofobia "NÃO tem sido motivo das reiteradas mortes de gays"; causa recorrente seria vingança por acordo descumprido. Afirma basear-se em inquéritos e processos, mas não os apresenta. Sem números, sem links. Chama bases de ONGs de "menos confiáveis" sem evidência. Crítica de método apenas.

### Item 11 - Parlamentar

[SOURCE: factual-context:web:https://www.camara.leg.br/noticias/443053-CRIMINALIZACAO-DA-HOMOFOBIA-DIVIDE-OPINIOES-NA-CAMARA]
[SOURCE: factual-context:web:https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/clp/noticias/brasil-e-o-pais-que-mais-mata-populacao-lgbtqia-clp-aprova-seminario-sobre-o-tema]

- Agência Câmara, 15/10/2014: deputado Ronaldo Fonseca (Pros-DF) chama as estatísticas dos movimentos LGBT de "infundadas": "Elas não apresentam a motivação do crime. Não dizem quem matou e por que matou." Sem contra-dado. A mesma matéria traz Sinara Gumieri (Instituto Anis) dizendo que os dados são "frágeis, porque vêm de coletas de notícias ou de denúncias".
- Agência Câmara, 24/05/2022 (CLP): usa "o Brasil é o país com maior número de assassinatos dessa população" sem contestação (GGB 2021: 276 homicídios + 24 suicídios; categorias somam 281). Mostra o uso institucional da frase, não contra-dado.
- Procurei discursos, pareceres e documentos da Frente Parlamentar Evangélica e da Católica com contra-dados: nada achado com o instrumental disponível. Isso não prova ausência (WebSearch não varre o acervo da Câmara).
- Notas taquigráficas da CDH do Senado de 24/06/2015 (`legis.senado.leg.br/escriba-servicosweb/reuniao/pdf/3484`) apareceram em três buscas, mas o host do Senado não resolveu (DNS/curl código 000, duas URLs), então NÃO foi aberta. Não sei se há contestação ali. Lacuna a refazer.
- Lupa 19/02/2019 registra que o advogado da Frente Parlamentar Mista da Família e Apoio à Vida no STF falou em "mais de 60 mil homicídios por ano" (selo: verdadeiro, mas); é enquadramento de contexto, não contra-contagem LGBT.

### Revista Oeste

[SOURCE: factual-context:web:https://revistaoeste.com/politica/governo-lula-quer-criar-banco-de-dados-sobre-crimes-de-homofobia/]

- 13/05/2023, redação, sobre banco de dados de homofobia do governo: não contesta os números. Registra só que os grupos "usam notícias como a principal fonte". Não achei texto da Oeste com contra-contagem. A edição 324 ("A farsa dos direitos humanos") devolveu 403; não aberta.

### Checagens jornalísticas da frase (não são autores conservadores; são o que existe)

[SOURCE: factual-context:web:https://apublica.org/2018/08/truco-dados-sobre-assassinato-de-lgbts-sao-incompletos/]
[SOURCE: factual-context:web:https://piaui.folha.uol.com.br/lupa/2019/02/19/stf-homofobia-crime/]
[SOURCE: factual-context:web:https://www.aosfatos.org/noticias/o-que-e-fato-no-que-diz-manuela-davila-de-assassinatos-de-trans-investimento-estatal/]

| Fact-check | Data | Frase checada | Selo | Núcleo da conclusão |
|------------|------|---------------|------|---------------------|
| Truco (Agência Pública), Ethel Rudnitzki | 29/08/2018 | "o que mais mata LGBTs no mundo. Uma vítima a cada 19 horas" (plano de governo de Vera Lúcia, PSTU) | Impossível de provar | sem registro oficial nem dados da maioria dos países; GGB 445 em 2017; trans: Brasil 1º absoluto, 4º por milhão segundo o texto |
| Lupa, Chico Marés e Maurício Moraes | 19/02/2019 | "o país que mais mata LGBTIs no mundo" (advogada do Grupo Dignidade no STF) | Insustentável | ILGA aponta maior número nas Américas, mas a própria ILGA diz que faltam estatísticas e não há comparação mundial; GGB 343 em 2016 |
| Aos Fatos, Luiz Fernando Menezes | 05/02/2018 | "campeão mundial de assassinato de pessoas trans" (Manuela D'Ávila) | Impreciso | absoluto: Brasil 1.071 de 2.609 (41%) TGEU 2008-2017; por milhão: 3º |

- Nota: o Truco dá 4º por milhão e o Aos Fatos dá 3º; períodos e bases do TGEU diferem. Não reconciliei.
- Comprova e Estadão Verifica: nenhuma checagem localizada nas buscas feitas.

### Academia (peer-reviewed e teses)

- Nenhum artigo revisado por pares de autor crítico às contagens foi achado em OpenAlex, Crossref e BDTD.
- Achados que usam o GGB sem crítica: Mendes e Silva 2020, Ciência & Saúde Coletiva [SOURCE: factual-context:openalex:10.1590/1413-81232020255.33672019] (afirma que o Brasil lidera; análise espacial); Santos e Silva 2021 [SOURCE: factual-context:openalex:10.17648/diversitas-journal-v6i1-1725] (leitura comparada dos relatórios 2011-2019, sem checar casos).
- Contexto metodológico (não são críticos conservadores): mapeamento de fontes de dados LGBTQIA+ (REBEP 2026) [SOURCE: factual-context:openalex:10.20947/s0102-3098a0338] e dissertação de Galbieri (UFSCar 2024) sobre estatísticas como estratégia política dos movimentos [SOURCE: factual-context:bdtd:SCAR_2b6c9f23f88752051bf6dd7e458cea32]; Carlessi e Nalli 2018 sobre discursos do dossiê [SOURCE: factual-context:crossref:10.5433/sgpp.2018v5.p175]. Resumos lidos, texto integral não.

## Não achado (resultado negativo)

- Crítica de autores conservadores ao Disque 100 ou ao Atlas da Violência: nenhuma. A crítica metodológica ao Disque 100 que apareceu (dissertação UFMG, RBE) é de natureza acadêmica sobre subnotificação, não contesta o número para baixo.
- Instituto Mises Brasil, Instituto Millenium, Brasil Paralelo, Senso Incomum, Terça Livre, Jornal da Cidade: nenhuma peça sobre o tema nas buscas por domínio feitas (Mises e Millenium e Senso Incomum numa busca; Brasil Paralelo/Terça Livre/JCO só em busca de texto livre). Sem prova de ausência.
- Material religioso (CNBB, FPE, igrejas): nada de contra-base achado.
- Espanhol e inglês: nenhuma crítica externa; os resultados reproduzem a contagem do GGB ou repetem a Wikipedia en (que cita Di Martino, Reynaldo e Cordeiro).
- Versão primária do "6% de 2017" e do "2 de 126 do Lesbocídio": não encontradas.

## Observação de leitura (para o artigo)

- A cadeia crítica inteira (Gazeta 2019-2023, Wikipedia en) se apoia em três pessoas: Vieira, Reynaldo e Di Martino. Eles se citam entre si e Reynaldo é coautor do item 1. Não é convergência independente de fontes.
- Crítica dos três vai na mesma direção (GGB sobrecontaria homofobia por incluir mortes sem motivo comprovado), mas nenhuma delas prova a hipótese contrária de que o número real seja baixo: 46% do item 1 ficou inconclusivo, e o GGB e o Observatório afirmam subcontagem. Para o contraponto honesto, o item 1 vale como "piso comprovável de casos com indício documentado", não como taxa.

## PRISMA-S (termo x idioma x base, contagens observadas)

WebSearch não devolve total de resultados; para web, o número é a contagem aproximada de links devolvidos por consulta (±2). Para OpenAlex, Crossref e BDTD, é o total reportado pela API.

| Termo (resumo) | Idioma | Base | Hits observados |
|----------------|--------|------|-----------------|
| Eli Vieira GGB 6% 2017 | pt | web | 18 links; primário não achado |
| Daniel Barbosa Reynaldo lesbocídio 126 | pt | web | 16 links |
| "país que mais mata LGBT" + fact-check | pt | web | 12 links (Truco, Lupa entre eles) |
| GGB metodologia clipping inflados | pt | web | 10 links |
| Revista Oeste + GGB | pt | web (domínio) | 10 links; 0 contestando |
| Gazeta do Povo + GGB estatística falsa | pt | web (domínio) | 10 links (5 críticos) |
| Mises/Liberal/Millenium/Senso Incomum | pt | web (domínio) | 9 links (4 do IL) |
| Câmara/Senado + GGB contestação | pt | web (domínio) | 10 links |
| Disque 100 / Atlas crítica | pt | web | 10 links; 0 críticas conservadoras |
| "Brasil Paralelo/JCO/Terça Livre" + GGB | pt | web | 18 links; 0 |
| Senado CDH + checagem | pt | web | 18 links; 0 |
| Brazil LGBT murders claim methodology | en | web | 10 links; 0 externas |
| Brasil país más peligroso LGBT cifras | es | web | 10 links; 0 externas |
| GGB metodologia crítica mortes LGBT | pt | OpenAlex | 1140 (relevância baixa) |
| mortes homofobia subnotificação crítica GGB | pt | OpenAlex | 137 |
| lesbocídio dossiê crítica metodologia | pt | OpenAlex | 31 |
| Who did homotransphobia kill today | en | OpenAlex | 3 |
| mesmas 5 consultas, filtro 2019-2026 | pt | OpenAlex | 0 / 1 / 2824 / 50 / 5 |
| GGB estatísticas mortes homofobia metodologia | pt | Crossref | 2.227.294 (ruído) |
| lesbocídio dossiê | pt | Crossref | 3568 |
| homicídios LGBT subnotificação dados | pt | Crossref | 255.675 (ruído) |
| "Grupo Gay da Bahia" metodologia | pt | BDTD | 15 |
| "Grupo Gay da Bahia" subnotificação | pt | BDTD | 2 |
| mortes LGBT estatísticas crítica dados ONG | pt | BDTD | 1 |
| lesbocídio | pt | BDTD | 8 |
| "crimes de ódio" LGBT dados oficiais | pt | BDTD | 0 |
| Grupo Gay da Bahia | pt, en | Wikipedia REST / Wikidata | Q512983 nas duas |
| "Grupo Gay da Bahia" | pt | SciELO search | 403, não consultado |

Termos da lista NÃO rodados como consulta própria: "ideologia de gênero estatística", "mortes LGBT números verdadeiros" (coberto por "Os verdadeiros números" via título), "homofobia dados inflados" (coberto por resultado da Gazeta), "Terça Livre/Jornal da Cidade" isolados.

Canais pulados: notas taquigráficas da CDH do Senado 24/06/2015 (host sem resolução); busca do SciELO (desafio 403 do site); Wayback Machine (429 repetido e depois "Temporarily Offline", impediu abrir posts de 2018 do blog de Reynaldo com a análise do Lesbocídio); WebFetch em piaui.folha.uol.com.br (bloqueado; aberto por curl); Revista Oeste ed. 324 (403); naomatouhoje.blog vivo (corpo vazio); thread/tweet de Ágata Cahill, vídeo de Eli Vieira de 2013 e carta de Maria Clara Dias (ANPOF), não abertos; app Shiny da checagem (HTTP 200, não inspecionado); Facebook; Playwright (proibido, não usado).

Ledger: 29 registered, 0 rejected by schema. Nota: a primeira rodada de 29 chamadas falhou por módulo `jsonschema` ausente no python do sistema (nada foi escrito); refiz com `uv run --with jsonschema` e a primeira entrada (LiHS) já constava, somando 29 no total desta frente. O arquivo `sources.jsonl` é compartilhado com outras frentes (102 linhas antes da minha primeira escrita).
