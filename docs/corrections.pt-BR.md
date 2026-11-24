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

## PDFs do artigo da v1.2.0

Os quatro PDFs do artigo distribuídos na v1.2.0 (português, inglês, espanhol e italiano) trazem as duas leituras corrigidas acima. Eles saem de `docs/paper/` na v1.3.0. A pasta passa a ter só as edições corrigidas, cada uma com DOI próprio. As edições em espanhol e italiano voltam quando tiverem a correção e DOI próprio; até lá, os READMEs em espanhol, italiano e hebraico apontam as edições em inglês e em português.

## O que foi conferido e não é correção

- **Fonte primária no Parlamento (1 de 49).** A v1.2.0 já trazia 1 de 49 falas pela regra literal do livro de códigos como análise principal e 0 de 49 pela regra do codificador original como sensibilidade. Nada mudou.
- **1,89% e 1,93%.** O 1,89% é a prevalência de adultos LGB+ na PNS de 2019 e continua certo. O 1,93% da edição corrigida (Apêndice F) é uma conta nova, e não a correção de um número antigo: 3.025.764 adultos LGB+ estimados para 2023, divididos por 156.554.235 adultos estimados para 2023 (156,6 milhões), porque a composição por sexo, raça e idade de 2023 difere da de 2019.

## Limpeza de privacidade da v1.3.0

Uma revisão independente de privacidade do pacote, feita antes desta versão, achou material que expunha terceiros ou o ambiente de trabalho do autor. Ele foi retirado ou substituído; nenhum número do artigo muda, e os testes que travam os números publicados continuam passando. O que mudou, por categoria:

- **Terceiros (`third-party`).** Em `analysis/ggb-audit/dados/ggb2019_universo_hash.csv`, 12 valores `sem_link:<texto>` em `fonte_tipo` traziam texto livre copiado do anexo do GGB (um deles com nome de pessoa); agora são só `sem_link`, e o `s01_parse_ggb2019.py` grava só isso. A coluna `obs` de `codificacao_A.csv` e `planilha_codificacao.csv`, com notas em texto livre por caso, foi trocada pelo indicador `diverge_cat_ou_cidade` (1 quando a fonte citada diverge da categoria ou da cidade do GGB, 0 quando não diverge, vazio quando a fonte não foi recuperada); o `s11_validacao.py` conta esse indicador, e a contagem de 3 casos não muda (travada em `tests/test_paper_numbers.py`). As URLs diretas da planilha da LiHS (nomes de vítimas e de acusados), do app construído sobre ela e da lista de vítimas do GGB 2016 arquivada foram trocadas por `[URL de lista nominal retirada na v1.3.0]`; a página institucional da LiHS fica, e as URLs do TDoR também, por ser um memorial público feito para isso. Uma frase de `analysis/counterpoint/frente-B-internacional.md` que nomeava uma pessoa numa alegação de processo foi removida. Um trecho de discurso parlamentar com alegação criminal sobre pessoa privada, e o localizador da nota taquigráfica, foram redigidos em dois arquivos do estudo de simetria; o registro, com o SHA-256 antes e depois, está em `analysis/robustness/simetria/REDACTIONS.md`. O `.gitignore` e um teste mantêm a planilha da LiHS fora do repositório e fora do selo. Os ids dos casos foram mantidos: são pseudônimos, não anônimos, diante da lista que o próprio GGB publica com nomes, e o pacote acrescenta a essa lista só a codificação de cada caso (`REPRODUCIBILITY.md`).
- **Pasta de trabalho do autor (`author-path`).** Caminhos e nomes das pastas de trabalho privadas do autor, fora do repositório, foram trocados por `<pasta-de-trabalho>/` ou `trabalho-nao-publicado/`; os testes que comparam cópias com a origem só recebem a pasta de origem por variável de ambiente.
- **Ambiente local (`local-environment`).** O caminho do interpretador Python local foi trocado por `python3`, e o local do arquivo de credenciais de uma ferramenta de modelo saiu do `s15_terceiro_codificador.py` (a ferramenta agora vem do ambiente).
- **Notas internas (`internal-notes`).** Notas de sessão de trabalho, menções a roteiros e pareceres internos e detalhes de custo e de conta das ferramentas de modelos de linguagem saíram de comentários de código e de relatórios. O uso de modelos de linguagem está descrito em `docs/language-model-use.pt-BR.md`.
- **Referências a arquivos retirados (`follows-withdrawal`).** Arquivos que apontavam para os arquivos retirados abaixo foram atualizados.

**Arquivos retirados na versão 1.3.0 (`withdrawn`).** `analysis/robustness/TRIAGEM.md`, `analysis/robustness/TRIAGEM.csv`, `figures/fontes/TRIAGEM.csv`, `figures/fontes/L-SECAO-3-3-PROPOSTA.md` e `figures/fontes/L-RELATORIO.md` deixam de ser distribuídos: pareceres de modelos e propostas internas de redação não fazem parte do pacote. A Figura 12, desenhada a partir de `TRIAGEM.csv` e não citada no artigo, saiu do pacote com ele. Os números da Figura E1 passam a se ancorar em `figures/fontes/estudos_mortalidade_origem.md`, a tabela de fontes primárias (trecho da fonte, arquivo e página) copiada verbatim da proposta retirada; só a nota abaixo da tabela (linha 45) teve uma expressão de trabalho interno reescrita. Também saiu do pacote `analysis/ggb-audit/resultados.csv`, cópia deixada no alto da pasta pela reorganização da versão 1.1.0: ela é anterior à terceira leitura dos casos do GGB (caso 159, morte violenta de I para S pela regra de dois de três em `analysis/ggb-audit/dados/adjudicacao.json`) e dizia 73 de 88, 15 de 88 e 19 de 73, enquanto o artigo e `analysis/ggb-audit/dados/resultados.csv`, o arquivo que `s11_validacao.py` grava e os testes travam, dão 74 de 88, 14 de 88 e 20 de 74. Nenhum script lia a cópia antiga.

**Registro auditável.** `docs/corrections-files.tsv` lista cada arquivo alterado ou retirado nesta limpeza, com a categoria e o SHA-256 na tag v1.2.0 e na v1.3.0 (`withdrawn` quando o arquivo saiu do pacote). O hash da v1.3.0 cobre toda mudança do arquivo nesta versão, inclusive as correções descritas acima. O teste `test_tabela_da_errata_bate_com_os_arquivos` (`tests/test_integridade.py`) confere que cada hash da v1.3.0 é o do arquivo distribuído. A tabela dá categorias, não o texto retirado, para não republicá-lo.

**Caminho local histórico mantido.** Seis documentos datados ainda citam o caminho da pasta de trabalho do autor, numa só linha cada: `preregistrations/midia/PRE-REGISTRO.md` e `PRE-REGISTRO.original.md` (linha 76), `analysis/robustness/reanalise/CRITERIOS.md` (linha 3), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` e `data/disque100/PREREGISTRO-D100.md` (linha 3). São pré-registros e critérios cujo SHA-256 foi gravado antes dos resultados; reescrevê-los quebraria a prova de que o texto não mudou. O caminho é público desde a v1.0.0 e não leva a dado nenhum. A lista desses arquivos está em `tests/test_integridade.py` (`CAMINHO_HASH_TRAVADO`). Pelo mesmo motivo, alguns arquivos congelados ainda citam o caminho do interpretador local ou o nome de uma pasta de trabalho anterior.
