# Processo, verificação e custo da versão 1.0.0

Este arquivo registra como a versão 1.0.0 do artigo foi feita e conferida: quem fez cada parte, quantas rodadas de
verificação houve, quanto se usou de cada modelo de linguagem, quanto tempo levou e que fontes os programas do
repositório consultam. Período: 21 de outubro a 1º de novembro de 2026, com trabalho em 12 dias.

> [!NOTE]
> Os números de uso e de tempo foram medidos nos registros locais de cada ferramenta (sessões do Claude Code, sessões
> do Grok e saídas do Codex). Esses registros não são publicados: têm conversas inteiras e caminhos da máquina do autor.
> Onde a ferramenta não informa contagem, o valor é estimado e está marcado assim.

## Quem fez cada parte

| Parte | Quem |
|---|---|
| Pergunta, escopo, decisões e aprovação do texto | o autor |
| Redação das seções 1 e 2 | Gemini 4 Argon |
| Redação das demais seções, código e condução do trabalho | Claude Opus 5.5 |
| Tarefas mecânicas de leitura, coleta e conferência | Claude Sonnet 5.5, como subagente |
| Conselho antes de decisões de método | Claude Fable 5.1 |
| Revisão do artigo inteiro | GPT-6 Astra, Grok 4.7 e Gemini 4 Argon, sem ver os pareceres uns dos outros na primeira rodada |
| Juiz da rubrica nas versões 0.1 a 0.4 | Grok 4.7 |
| Segundo codificador da conferência do GGB de 2019 | Gemini 3.8 Flash, cego aos códigos do primeiro |
| Terceira leitura dos 6 desacordos da conferência do GGB | GPT-6 Astra, cego aos dois primeiros, com a matéria inteira; o autor conferiu a decisão |

Nenhum texto do artigo foi redigido pelo Grok. A redação seguiu regras escritas que proíbem número ou citação fora do
material conferido, e um programa conferiu cada número e cada citação de cada seção contra os arquivos de origem antes
da revisão do autor.

## Rodadas de verificação

| Etapa | O que foi feito | Onde está |
|---|---|---|
| Juiz da rubrica, versões 0.1 a 0.4 | 25 vereditos | `paper/build/juiz/` |
| Revisão de mérito r5 | Astra e Grok | `paper/v05/revisao/r5/` |
| Revisão de mérito r6 a r8 | Astra, Grok e Argon, com matriz de resposta a cada crítica | `paper/v05/revisao/r6/` a `r8/` |
| Pré-publicação pub1 e pub2 | os três revisores leram o PDF pronto e o repositório | `paper/v05/revisao/pub1/` e `pub2/` |
| Análises pedidas pelos revisores e feitas antes do DOI | cor ou raça ignorada (Tabela C12), cônjuge no domicílio por tipo de agressor (Tabela C10), Tabela 6 com a fração de cada modo (Tabela K2), terceira leitura dos 6 desacordos do GGB | `dados/pns/`, `research-2026-10-21-rodada3/F2-custos/`, `research-2026-10-21-rodada3/F3-ggb/` |
| Testes que travam os números publicados | conferem cada número contra o arquivo que o gerou | `tests/`, `paper/tests/` |
| Selo de proveniência | uma impressão digital SHA-256 sobre código, testes e dados | `output/hash-chain.md`, `make_provenance.py --verify` |

## Uso de modelos de linguagem

"Tokens novos" soma a entrada, a escrita em cache e a saída. "Lidos do cache" é o contexto já enviado que a ferramenta
relê a cada turno; ele infla a conta, mas não é trabalho novo, e por isso fica numa coluna à parte. Os números do Claude
cobrem todo o trabalho do projeto (pesquisa, código, texto e revisão), não só a redação.

| Modelo | Papel | Tokens novos | Dos quais, saída | Lidos do cache | Como foi medido |
|---|---|---|---|---|---|
| Claude Opus 5.5 | redação, código e condução | ~33,1 milhões | ~1,70 milhão | ~1,89 bilhão | registros das sessões e subagentes |
| Claude Sonnet 5.5 | subagentes | ~34,9 milhões | ~1,54 milhão | ~1,54 bilhão | idem |
| Claude Fable 5.1 | conselheiro | ~12,2 milhões | ~0,26 milhão | ~24 milhões | idem |
| Grok 4.7 e 4.6 | juiz e revisor | até ~20,3 milhões, em 152 chamadas | ~1,46 milhão | — | registros do Grok; o filtro por assunto pode incluir sessões de outro trabalho, por isso "até" |
| GPT-6 Astra | revisor e terceiro codificador | ao menos ~2,2 milhões, em 10 rodadas | — | — | contagem que o Codex imprime ao fim de cada rodada |
| Gemini 4 Argon | redação das seções 1 e 2 e revisor | piso estimado de ~0,8 milhão | estimado em ~35 mil | — | estimado pelo tamanho do texto enviado; o aplicativo não informa contagem e os anexos não entram |

## Tempo

| Medida | Valor | Como foi medido |
|---|---|---|
| Sessão ativa do Claude | ~30 horas | soma dos intervalos entre mensagens menores que 15 minutos; é um piso |
| Grok, tempo de máquina das rodadas registradas | ~2,2 horas | campo de duração de cada rodada |
| Astra, idem | ~1,4 hora | idem |
| Argon pelo programa de linha de comando | ~12 minutos | idem; as rodadas pelo navegador não registram duração |

## Custo

Todos os modelos foram usados pelas assinaturas dos próprios fornecedores (Claude Max, ChatGPT, Grok e o aplicativo do
Gemini), sem nenhuma interface de programação cobrada por uso. Pela tabela de preços do Grok, o uso registrado
equivaleria a cerca de US$ 29; ele foi coberto pela assinatura.

## Fontes que os programas do repositório consultam

O inventário completo, com endereço e data de acesso de cada fonte e, quando houve arquivo salvo, o SHA-256, está em `manifest/MANIFESTO-FONTES.csv`
(1.139 linhas) e `manifest/INVENTARIO-PUBLICO.md`. Os domínios que os programas chamam diretamente são estes:

| Grupo | Fontes |
|---|---|
| Saúde e população | DATASUS (TabNet, Sinan e SIM); IBGE (API do SIDRA, FTP da PNS e biblioteca); Ipea (repositório) |
| Governo, Congresso e tribunais | gov.br (Disque 100 e portais de ministérios); Planalto (legislação); Câmara dos Deputados; STF; Portal da Transparência; SIOP; Comissão Nacional da Verdade (Memórias Reveladas) |
| Sociedade civil e imprensa | Grupo Gay da Bahia; Fórum Brasileiro de Segurança Pública; TGEU (Trans Murder Monitoring) e Trans Lives Matter; ILGA; Homofobia Mata; Congresso em Foco; Poder360 |
| Contratos e preços estrangeiros | Find a Tender (Reino Unido); TED (União Europeia); Gambling Commission; portal de dados abertos do Canadá |
| Bibliografia e arquivo | doi.org (52 chamadas nos programas); OpenAlex; Wayback Machine (Internet Archive); Zenodo |
