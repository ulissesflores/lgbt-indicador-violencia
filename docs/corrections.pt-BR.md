# Correções

[English](corrections.md) · **Português (Brasil)**

Registro datado do que mudou depois da publicação de cada versão. A tag v1.2.0 não foi reescrita; as correções abaixo entram na versão 1.3.0 do pacote e na edição corrigida do artigo (Codex Hash Research Report 2026-10). Os números citados aqui são travados por teste em `tests/test_paper_numbers.py`.

## Errata de 2026-11-22 14:41 (GMT-3): recortes pré-registrados (b) e (c) omitidos na v1.2.0

**O que estava errado.** O pré-registro `data/exposicao/PREREGISTRO-C10.md` (seção 4, "Recortes (todos exibidos, nenhum filtrado)") manda mostrar quatro recortes das 67 trocas de governador: (P) todas as 67; (a) janela completa de três anos antes e três depois (47); (b) janela completa e não contaminada por outra troca da mesma UF (21); (c) só posse eleitoral (45). O artigo da v1.2.0 (seção 3.6 e Apêndice G, nas quatro edições) mostrava o recorte (P) com todas as direções e grupos, e do recorte (a) só a mediana e o p do grupo total, sem a correção de Holm. Os recortes (b) e (c) não apareciam.

**Por que importa.** O resultado do recorte (b) é diferente do que o texto dizia. Em `data/exposicao/c10_e2_resumo.csv` (grupo total, agressão):

| recorte | direção | trocas | subiu | caiu | mediana % | referência (mediana) % | p mediana | p de Holm |
|---|---|---|---|---|---|---|---|---|
| (P) todas | todas | 67 | 31 | 36 | −0,7 | +4,6 | ,0162 | ,0732 |
| (a) janela completa | todas | 47 | 20 | 27 | −0,8 | +5,9 | ,008 | ,0156 |
| (b) completa e não contaminada | todas | 21 | 8 | 13 | −10,2 | +6,7 | ,0016 | ,0064 |
| (b) completa e não contaminada | para a direita | 10 | 2 | 8 | −11,2 | +7,5 | ,0058 | ,0232 |
| (b) completa e não contaminada | para a esquerda | 11 | 6 | 5 | +1,3 | +6,7 | ,3782 | 1 |
| (c) posse eleitoral | todas | 45 | 21 | 24 | −0,8 | +4,6 | ,0264 | ,1056 |

Com isso, as frases "nos dois sentidos o resultado não se distingue do que ocorre nos estados que não trocaram de governo" (Apêndice G) e "as análises não acharam associação" (seção 3.6, sobre a exposição) não valiam para todos os recortes. Também a frase "somando a causa indeterminada, a diferença deixa de se distinguir" não vale para o recorte (b), em que a mediana com causa indeterminada é −6,3% (p ,0016); nos recortes (P), (a) e (c), com a causa indeterminada somada, o p da mediana fica acima de ,05.

**O que não mudou.** Nenhum número da v1.2.0 estava calculado errado: `c10_e2_resumo.csv` e os testes de `tests/test_c10_exposicao.py` continuam válidos. O painel de governadores (efeitos fixos duplos, intervalo de −12,3% a +12,4%) é outra análise e não é afetado. A leitura continua descritiva: a referência de acaso é pequena e não neutra (adendo 1 do pré-registro), e nenhuma leitura causal é feita.

**Correção.** A edição corrigida do artigo traz no Apêndice G os quatro recortes pré-registrados (grupo total em todas as direções; todos os grupos nos recortes a, b e c; as 189 células completas ficam em `c10_e2_resumo.csv`), com n, quantas subiram e quantas caíram, mediana, p e p de Holm; a seção 3.6, o Resumo e a conclusão descrevem o resultado de cada recorte, inclusive a queda em relação à referência no recorte (b), tratada como exploratória, com n pequeno e sem leitura causal.

## Errata de 2026-11-22 22:18 (GMT-3): "50 confirmados em notícia" na v1.2.0

**O que estava errado.** O Resumo do artigo da v1.2.0 dizia que, dos 160 casos sorteados da lista do Grupo Gay da Bahia de 2019, "50 foram confirmados em notícia sobre o próprio caso", e os READMEs da v1.2.0, nos cinco idiomas, repetiam a frase ("50 were confirmed in news reports on the case itself"). O texto também chamava de "notícia" todas as 106 fontes citadas que foram recuperadas.

**O que os dados dizem.** Em `analysis/ggb-audit/dados/codificacao_A.csv`, das 106 fontes citadas recuperadas, 84 são notícias; as demais são página inicial de site, página que não traz mais o conteúdo, rede social, lista secundária e outro tipo. Dos 50 casos em que a fonte citada confirma morte violenta de pessoa LGBT+, 48 são confirmados por notícia e 2 por lista secundária.

**Correção.** A edição corrigida e os READMEs da v1.3.0 dizem que 50 casos foram confirmados **pela fonte citada (48 por notícia)**. O total de 50 (31,3%, intervalo de 95% de 24,6% a 38,8%) não muda.

## Errata de 2026-11-24 (GMT-3): cinco leituras da v1.2.0 que os dados ou a fonte citada não sustentam

**O que estava errado.** A conferência de cada número do artigo contra os *scripts* deste repositório e contra as fontes citadas (`analysis/article-numbers/`) achou cinco leituras no texto da v1.2.0, presentes nas quatro edições (português, inglês, espanhol e italiano):

1. **Tabela H1 (Apêndice H), coluna "Páginas publicadas durante o mandato":** 6/10 para Dilma Rousseff, 6/8 para Michel Temer, 23/51 no total.
2. **Seção 4.2, ODIHR (2025):** estatística oficial de crime de ódio "em 46 Estados" da Organização para a Segurança e Cooperação na Europa.
3. **Seção 4.2, FRA (2024):** "de 13% a 14%" de respondentes atacados em cinco anos, atribuídos à União Europeia.
4. **Apêndice E, Frisch e Brønnum-Hansen (2009):** indicador de casamento do mesmo sexo que cobre de 1% a 6% "dos homens gays".
5. **Apêndice K:** 329.644 adultos a contatar.

**O que os dados e as fontes dizem.**

1. Cada uma das 51 páginas lidas na busca simétrica foi datada pela data de publicação, lida na versão atual de cada página em 2026-11-24, e comparada com a data em que cada presidente assumiu (Dilma Rousseff até 2016-05-11, Michel Temer a partir de 2016-05-12). A coluna é 5/10, 5/8 e 21/51. Pela regra do ano civil, seria 7/10, 6/8 e 24/51; o impresso 6/10, 6/8 e 23/51 não sai de nenhuma das duas regras. Três páginas sem data de publicação legível (todas do mesmo artigo de periódico) não contam como publicadas no mandato. Datas: `analysis/article-numbers/datas_publicacao_C18.tsv`; recontagem: `analysis/article-numbers/contas_do_texto.py`.
2. ODIHR (2025), p. 2 do PDF: 42 dos 57 Estados participantes têm estatística oficial, e 47 enviaram algum dado ou informação. O número 46 não está na fonte.
3. FRA (2024): a pesquisa de 2023 cobre 30 países, não só a União Europeia. 14% é o número do conjunto dos 30 países (p. 24 e p. 58 do PDF); 13% é o da União Europeia (p. 68 do PDF).
4. Frisch e Brønnum-Hansen (2009), Discussão: a estimativa de 1% a 6% se refere a pessoas gays ou lésbicas, não a homens gays.
5. 329.643: o número necessário de adultos LGB+, 5.786,288 antes do arredondamento (impresso como 5.786,3), dividido pela fração não ponderada de adultos LGB+ (1.554 de 88.531) dá 329.643,4. A divisão com o 5.786,3 arredondado dá 329.644,1, o valor impresso.

Fonte, página e valor dos itens 2 a 4 estão em `analysis/article-numbers/terceiros_transcritos.csv`; as contas dos itens 1 e 5, em `analysis/article-numbers/contas_do_texto.csv`. O teste `test_errata_2026_11_24_cinco_leituras` (`tests/test_paper_numbers.py`) regera esse arquivo a partir do *script* e trava os cinco valores corrigidos.

**Correção.** A edição corrigida, nos cinco idiomas, traz 5/10, 5/8 e 21/51 na Tabela H1; "Em 42 dos 57 Estados"; "Em 30 países europeus ... 14% ..., e 13% na União Europeia"; "de 1% a 6% das pessoas gays ou lésbicas"; e 329.643. `analysis/robustness/simetria/scripts/tabela_C18.py`, `TABELA_C18.md` e `SIMETRIA.md` trazem a mesma correção da Tabela H1.

**O que não mudou.** As outras colunas da Tabela H1 (consultas, páginas lidas 51/55, eventos por tipo) e o texto do Apêndice H, que se apoia nas colunas de episódios, e não nesta; os valores 13% e 14%, só o recorte a que cada um pertence; o "cerca de 330 mil" do Apêndice K; as razões de mortalidade relatadas por Frisch e Brønnum-Hansen.

## Errata de 2026-11-25 (GMT-3): limite inferior do intervalo com correção para população finita no Apêndice F

**O que estava errado.** A nota da tabela de concordância do Apêndice F (conferência dos 160 casos de 2019), em todas as edições do artigo da 1.3.0 e no material complementar, diz que a correção para população finita (160 de 329 casos) estreitaria o intervalo de Wilson dos 50 casos verificáveis "para 26,3% a 36,6%". O limite inferior é 26,4%, não 26,3%.

**O que os dados dizem.** O intervalo de Wilson de 50 em 160 com z multiplicado pelo fator de população finita, a raiz de (329 − 160) / (329 − 1), dá 26,350265% a 36,607962% (`analysis/ggb-audit/dados/validacao_resumo.json`; conta em `analysis/article-numbers/contas_do_texto.py`, linha `ggb_wilson_fpc_lo` de `contas_do_texto.csv`). Arredondado a uma casa, o limite inferior é 26,4 e o superior, 36,6. Nenhuma variante da fórmula dá 26,3 (sem o −1 no fator: 26,357; Agresti-Coull: 26,58; Wald: 26,08); 26,3 sai de cortar 26,35 em vez de arredondar. A entrada `l1221|6` do `paper_numbers.json` registra o 26,3 impresso e o 26,4 corrigido, e o `verify_paper_numbers.py` só aceita o impresso porque o parágrafo correspondente de `docs/corrections.md` existe e a conta arredonda para 26,4.

**O que não mudou.** Os 50 casos verificáveis, o intervalo principal de 24,6% a 38,8% e o limite superior de 36,6%. A edição do artigo está congelada e continua imprimindo 26,3; a correção fica registrada aqui e entra na próxima edição do artigo.

**Adendo de 2026-11-26 (GMT-3).** As edições do artigo foram reemitidas em 2026-11-26, antes de seus DOIs serem cunhados, e os cinco idiomas imprimem agora 26,4. A entrada `l1221|6` do `paper_numbers.json` registra agora o 26,4 impresso, sem correção; `tests/test_paper_numbers.py` (`test_paper_numbers_impresso_corrigido`) continua conferindo o mecanismo de correção numa cópia dessa entrada que imprime 26,3. Os parágrafos acima ficam como foram escritos em 2026-11-25.

## Conserto de 2026-11-25 (GMT-3): pasta de dados de quatro scripts da auditoria da lista do GGB

`analysis/ggb-audit/scripts/s08_captura_recaptura.py` e `analysis/ggb-audit/scripts/s10_duplicatas.py` gravavam as saídas em `analysis/ggb-audit/data/`, pasta que o pacote não tem; os arquivos que eles produzem são distribuídos em `analysis/ggb-audit/dados/` (`captura_recaptura_trans2019.json`, `captura_recaptura_sensibilidade.json`, `cr_ggb_trans_hash.csv`, `duplicatas_candidatas_hash.csv`, `duplicatas_resumo.json`). Mais dois scripts tinham a mesma pasta errada: `analysis/ggb-audit/scripts/s06_pacote_codificador_B.py` lia dela as entradas (`amostra.csv` e a codificação bruta do primeiro codificador, que não é distribuída) e `analysis/ggb-audit/scripts/s09_uf_series.py` gravava nela `uf_2019.csv`, `serie_ggb_vs_cobertura.csv` e `inflacao_uf_serie.json`. Na v1.3.0 os onze caminhos dos quatro scripts apontam para `dados/`. Nenhum número mudou: os quatro scripts leem a lista nominal, que não é distribuída, então não se re-rodam a partir do pacote (REPRODUCIBILITY.md, "What cannot be re-run"), e as saídas distribuídas são as que o artigo cita.

## Correções de 2026-11-26 (GMT-3): três fontes citadas lidas por inteiro antes do DOI

**O que estava em aberto.** Seis números que o artigo atribui a três fontes estavam transcritos em `analysis/article-numbers/terceiros_transcritos.csv` com o status `pagina-pendente`: o texto integral não tinha sido aberto, e o repositório não podia mostrar onde cada número está na fonte. Os três textos foram então lidos por inteiro: Pettis et al. (2022) no PDF da revista, Ferguson & Malouff (2016) na versão submetida no SSRN (resumo 2924906, a única cópia aberta, sem a paginação da revista) e Fernández Turuelo (2024) no PDF da revista.

**O que as fontes dizem, e o que mudou no texto.**

1. **Pettis et al. (2022), Apêndice G.** A queda de cerca de 30% está na p. 822 ("a 30 percent decrease from the baseline of .37 per 100,000 persons"). O texto dizia que o efeito deixa de ser significativo "com tendências estaduais"; na Tabela 5 (pp. 828–829), ele deixa de ser estatisticamente significativo quando o modelo inclui tendências estaduais **e** agrupa os erros-padrão por estado e trimestre. A edição corrigida diz isso e cita as pp. 822 e 828–829.
2. **Ferguson & Malouff (2016), Apêndice L.** A taxa combinada de 5,2% (intervalo de 95% de 3,0% a 8,9%) está nas p. 2 e 13 da versão submetida; a faixa de 2,0% (Heenan & Murray, 2006) a 13,7% (Spohn et al., 2014) está na Tabela 1 (p. 24); os 4,5% que o texto dá para Spohn et al. estão na p. 12. O artigo não relata I²: relata *Q*(6) = 128, *p* < ,001 (p. 13). A edição corrigida imprime esse *Q* e diz que o I² de cerca de 95% é calculado a partir dele ((128 − 6) / 128 = 95,3%). A página "p. 1189" não se confere na versão aberta e foi trocada por "Tabela 1 e resultados, na versão submetida disponível no SSRN". A frase de que a estimativa combinada só se reproduz com o valor da tabela para um dos estudos ganhou conta pública: um modelo de DerSimonian-Laird na escala logit sobre os sete estudos da Tabela 1 (`analysis/article-numbers/ferguson_malouff_2016_tabela1.csv`), com as contagens reconstruídas como taxa vezes N, dá ,052 com o ,137 da tabela para Spohn et al. e ,044 com os 4,5% do texto (linhas `ferguson_dl_tabela1` e `ferguson_dl_spohn_texto` de `contas_do_texto.csv`; o intervalo e o *Q* das contagens reconstruídas ficam como informativos, porque uma taxa com três casas admite mais de uma contagem).
3. **Fernández Turuelo (2024), Tabela I1.** Os 12 expedientes de Valladolid em 1971 e 1972 são a amostra do estudo, limitada a esses anos pelo acesso ao arquivo (p. 114 e nota 16), não a contagem de todos os casos; as 4 condenações são "las cuatro sentencias condenatorias" (p. 112). A edição corrigida diz que os 12 são a amostra do estudo.

**O que não mudou.** Os números em si (30%, 5,2%, 3,0% a 8,9%, 2,0%, 13,7%, 4,5%, 12 e 4) e as conclusões que os usam. As seis linhas do arquivo de transcrição trazem agora a página e o trecho, com o status `conferido`, e o `paper_numbers.json` não lista mais nenhum número como `pending-source`.

## Errata de 2026-11-28 (GMT-3): duas afirmações do pacote v1.3.0

1. **A seção "PDFs do artigo da v1.2.0", abaixo,** diz que `docs/paper/` tem traduções novas para o espanhol, o italiano e o hebraico e que cada README aponta a edição no seu idioma. A versão 1.3.0 distribui só a edição de referência em português e a tradução para o inglês, como diz o `README.md`; os READMEs em espanhol, italiano e hebraico apontam a edição em inglês, e as outras edições virão com DOI próprio.
2. **As descrições da versão 1.3.0** em `.zenodo.json`, `CITATION.cff`, `codemeta.json` e no ADR 0005 dizem que ela corrige "duas leituras" do artigo da v1.2.0. As correções são as entradas datadas deste arquivo de 2026-11-22 a 2026-11-26: onze leituras ou fontes citadas corrigidas e um conserto da pasta de dados de scripts. A descrição do registro da v1.3.0 no Zenodo (DOI 10.5281/zenodo.24635451) foi corrigida em 2026-11-28.

**O que não mudou.** Nenhum número do artigo, arquivo de dados em `data/`, script de análise ou conclusão. As duas afirmações ficam como estão no arquivo da v1.3.0, cujo selo o artigo imprime (ADR 0008).

## PDFs do artigo da v1.2.0

Os quatro PDFs do artigo distribuídos na v1.2.0 (português, inglês, espanhol e italiano) trazem as leituras corrigidas acima. Eles saem de `docs/paper/` na v1.3.0. A pasta passa a ter só o texto corrigido: a edição de referência em português e a tradução para o inglês, cada uma com DOI próprio, e traduções novas para o espanhol, o italiano e o hebraico, feitas do texto corrigido. Cada README aponta a edição no seu idioma.

## O que foi conferido e não é correção

- **Fonte primária no Parlamento (1 de 49).** A v1.2.0 já trazia 1 de 49 falas pela regra literal do livro de códigos como análise principal e 0 de 49 pela regra do codificador original como sensibilidade. Nada mudou.
- **1,89% e 1,93%.** O 1,89% é a prevalência de adultos LGB+ na PNS de 2019 e continua certo. O 1,93% da edição corrigida (Apêndice F) é uma conta nova, e não a correção de um número antigo: 3.025.764 adultos LGB+ estimados para 2023, divididos por 156.554.235 adultos estimados para 2023 (156,6 milhões), porque a composição por sexo, raça e idade de 2023 difere da de 2019.

## Limpeza de privacidade da v1.3.0

Uma revisão independente de privacidade do pacote, feita antes desta versão, achou material que expunha terceiros ou o ambiente de trabalho do autor. Ele foi retirado ou substituído; nenhum número do artigo muda, e os testes que travam os números publicados continuam passando. O que mudou, por categoria:

- **Terceiros (`third-party`).** Em `analysis/ggb-audit/dados/ggb2019_universo_hash.csv`, 12 valores `sem_link:<texto>` em `fonte_tipo` traziam texto livre copiado do anexo do GGB (um deles com nome de pessoa); agora são só `sem_link`, e o `s01_parse_ggb2019.py` grava só isso. A coluna `obs` de `codificacao_A.csv` e `planilha_codificacao.csv`, com notas em texto livre por caso, foi trocada pelo indicador `diverge_cat_ou_cidade` (1 quando a fonte citada diverge da categoria ou da cidade do GGB, 0 quando não diverge, vazio quando a fonte não foi recuperada); o `s11_validacao.py` conta esse indicador, e a contagem de 3 casos não muda (travada em `tests/test_paper_numbers.py`). As URLs diretas da planilha da LiHS (nomes de vítimas e de acusados), do app construído sobre ela e da lista de vítimas do GGB 2016 arquivada foram trocadas por `[URL de lista nominal retirada na v1.3.0]`; a página institucional da LiHS fica, e as URLs do TDoR também, por ser um memorial público feito para isso. Uma frase de `analysis/counterpoint/frente-B-internacional.md` que nomeava uma pessoa numa alegação de processo foi removida. Um trecho de discurso parlamentar com alegação criminal sobre pessoa privada, e o localizador da nota taquigráfica, foram redigidos em dois arquivos do estudo de simetria; o registro, com o SHA-256 antes e depois, está em `analysis/robustness/simetria/REDACTIONS.md`. O `.gitignore` e um teste mantêm a planilha da LiHS fora do repositório e fora do selo. Os ids dos casos foram mantidos: são pseudônimos, não anônimos, diante da lista que o próprio GGB publica com nomes (o sal é uma constante no `s01_parse_ggb2019.py` e as linhas seguem a ordem do anexo do GGB), e o pacote acrescenta a essa lista só a codificação de cada caso (`REPRODUCIBILITY.md`).
- **Pasta de trabalho do autor (`author-path`).** Caminhos e nomes das pastas de trabalho privadas do autor, fora do repositório, foram trocados por `<pasta-de-trabalho>/` ou `trabalho-nao-publicado/`; os testes que comparam cópias com a origem só recebem a pasta de origem por variável de ambiente.
- **Ambiente local (`local-environment`).** O caminho do interpretador Python local foi trocado por `python3`, e o local do arquivo de credenciais de uma ferramenta de modelo saiu do `s15_terceiro_codificador.py` (a ferramenta agora vem do ambiente).
- **Notas internas (`internal-notes`).** Notas de sessão de trabalho, menções a roteiros e pareceres internos e detalhes de custo e de conta das ferramentas de modelos de linguagem saíram de comentários de código e de relatórios. Arquivos cujo SHA-256 foi gravado antes dos resultados mantêm essas notas, porque reescrevê-los quebraria essa prova: os pré-registros `preregistrations/governos/PRE-REGISTRO.md`, `preregistrations/mortalidade/PRE-REGISTRO.md` (e o seu `.original.md`), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` e `data/disque100/PREREGISTRO-D100.md`, e os critérios e o segundo adendo das verificações de robustez, `analysis/robustness/reanalise/CRITERIOS.md`, `analysis/robustness/simetria/CRITERIOS.md` e `analysis/robustness/simetria/ADENDO-2-execucao-e-desvios.md`. Eles citam roteiros e arquivos de trabalho internos, um cita o pedido do autor ao modelo de linguagem, e dois trazem a linha de comando das ferramentas de modelo. Uma linha de dados, a de 2026-10-11 em `analysis/political-economy/dados/h5_linha_do_tempo.csv` (e o script que a escreve), citava como fonte um arquivo interno de andamento; agora diz "registro interno (não distribuído)" e mantém o SHA-256 desse arquivo como prova. O uso de modelos de linguagem está descrito em `docs/language-model-use.pt-BR.md`.
- **Referências a arquivos retirados (`follows-withdrawal`).** Arquivos que apontavam para os arquivos retirados abaixo foram atualizados.

**Arquivos retirados na versão 1.3.0 (`withdrawn`).** `analysis/robustness/TRIAGEM.md`, `analysis/robustness/TRIAGEM.csv`, `figures/fontes/TRIAGEM.csv`, `figures/fontes/L-SECAO-3-3-PROPOSTA.md` e `figures/fontes/L-RELATORIO.md` deixam de ser distribuídos: pareceres de modelos e propostas internas de redação não fazem parte do pacote. A Figura 12, desenhada a partir de `TRIAGEM.csv` e não citada no artigo, saiu do pacote com ele. Os números da Figura E1 passam a se ancorar em `figures/fontes/estudos_mortalidade_origem.md`, a tabela de fontes primárias (trecho da fonte, arquivo e página) copiada verbatim da proposta retirada; só a nota abaixo da tabela (linha 45) teve uma expressão de trabalho interno reescrita. Também saiu do pacote `analysis/ggb-audit/resultados.csv`, cópia deixada no alto da pasta pela reorganização da versão 1.1.0: ela é anterior à terceira leitura dos casos do GGB (caso 159, morte violenta de I para S pela regra de dois de três em `analysis/ggb-audit/dados/adjudicacao.json`) e dizia 73 de 88, 15 de 88 e 19 de 73, enquanto o artigo e `analysis/ggb-audit/dados/resultados.csv`, o arquivo que `s11_validacao.py` grava e os testes travam, dão 74 de 88, 14 de 88 e 20 de 74. Nenhum script lia a cópia antiga.

**Registro auditável.** `docs/corrections-files.tsv` lista cada arquivo alterado ou retirado nesta limpeza, com a categoria e o SHA-256 na tag v1.2.0 e na v1.3.0 (`withdrawn` quando o arquivo saiu do pacote). O hash da v1.3.0 cobre toda mudança do arquivo nesta versão, inclusive as correções descritas acima. O teste `test_tabela_da_errata_bate_com_os_arquivos` (`tests/test_integridade.py`) confere que cada hash da v1.3.0 é o do arquivo distribuído. A tabela dá categorias, não o texto retirado, para não republicá-lo.

**Caminho local histórico mantido.** Seis documentos datados ainda citam o caminho da pasta de trabalho do autor, numa só linha cada: `preregistrations/midia/PRE-REGISTRO.md` e `PRE-REGISTRO.original.md` (linha 76), `analysis/robustness/reanalise/CRITERIOS.md` (linha 3), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` e `data/disque100/PREREGISTRO-D100.md` (linha 3). São pré-registros e critérios cujo SHA-256 foi gravado antes dos resultados; reescrevê-los quebraria a prova de que o texto não mudou. O caminho é público desde a v1.0.0 e não leva a dado nenhum. A lista desses arquivos está em `tests/test_integridade.py` (`CAMINHO_HASH_TRAVADO`). Pelo mesmo motivo, alguns arquivos congelados ainda citam o caminho do interpretador local ou o nome de uma pasta de trabalho anterior. Três docstrings de script também ainda trazem o caminho do interpretador: `data/disque100/scripts/d100_tabular.py` e `d100_estrutura.py`, cujo SHA-256 está gravado ao lado do pré-registro do Disque 100 (mudança ali vira adendo), e `analysis/robustness/simetria/scripts/fisher_C27.py`.

## Cabeçalho de arquivo na v1.3.0 (não é correção)

Todo arquivo de código que nenhum pré-registro fixa por hash abre agora com um cabeçalho em inglês: as linhas
`SPDX-License-Identifier: Apache-2.0` e de copyright e uma docstring de módulo em inglês (propósito, entradas, saídas,
como rodar, situação de registro, autor). A descrição original em português fica, palavra por palavra, na seção `Notes`
da docstring, e o corpo de cada arquivo não muda, então nenhum número se move (ADR 0006, emenda de 2026-11-25).
Arquivos que mudaram só por esse cabeçalho não entram em `docs/corrections-files.tsv`; o script que grava essa tabela
só deixa um arquivo de fora quando o arquivo sem as linhas do cabeçalho e sem a docstring de módulo é, byte a byte, o
arquivo da v1.2.0 sem a docstring de módulo. Os doze scripts citados ao lado de um hash num pré-registro ficam sem
cabeçalho e estão descritos em [`docs/code-reference.md`](code-reference.md). As listas `SHA256SUMS` por pasta foram
gravadas quando cada etapa rodou e registram os arquivos como eram naquele momento; várias já não batem (brutos não distribuídos, caminhos
reorganizados na v1.1.0, a limpeza acima, estes cabeçalhos). O selo desta versão é `manifest/SHA256SUMS.txt` com o
hash da cadeia.
