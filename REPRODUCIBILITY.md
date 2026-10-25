# Reprodutibilidade

Este repositório distribui **derivados**, código, ledgers e pré-registros. Não distribui microdado bruto, PDF de terceiros nem dado nominal.
Por isso a reprodução tem duas trilhas e um conjunto de coisas que não se pode refazer.

## Dois selos

1. **Derivação reproduzível (Trilha 1).** Todo número publicado que depende só dos derivados distribuídos é recalculado por
   `python3 -I run_all.py` e comparado com o commitado. O recálculo roda numa réplica (`.run/replica`), nunca sobre os arquivos do repositório.
   Resultado verificado em 2026-10-23, macOS arm64, Python 3.14.8, numpy 2.4.6, pandas 3.0.2, scipy 1.17.1, matplotlib 3.10.9
   (`requirements.lock`): ver a seção "Evidência desta montagem" abaixo.
2. **Evidência congelada, não re-rodável.** Coletas que dependem do mundo naquele dia (reportagens, páginas da Wikipédia, buscas em
   Google News RSS/OpenAlex/GDELT, arquivos preliminares do DATASUS, leitura de PDFs) não voltam idênticas. Cada uma tem URL, data de acesso
   e, quando houve download, SHA-256 em `manifest/MANIFESTO-FONTES.csv`; o que foi lido, codificado ou contado fica nos CSV/JSON derivados.

O **selo de integridade** é outra coisa: `python3 -I make_provenance.py --verify` confere que cada arquivo distribuído tem o SHA-256
registrado em `manifest/SHA256SUMS.txt` e que o `chain_hash` de `output/provenance.json` fecha.

**O artigo fica fora do selo (decisão de arquitetura do autor).** O repositório vem primeiro, com a cadeia de hashes, e o artigo deriva
dele: o artigo cita a URL do repositório e o `chain_hash`, o que seria impossível se o selo cobrisse o próprio artigo. Por isso
`make_provenance.excluido()` (regra única, usada também pelo inventário, pelos testes de privacidade e pelo auditor) deixa fora do
conjunto selado `paper/paper.md`, `paper/AUDIT.md`, `paper/build/` (PDF, DOCX, saídas do juiz), `paper/tools/` (ferramentas de export e
auditoria), `paper/tests/test_anexo.py` (testa o build do artigo) e `paper/PAPER-SHA256.txt`. As figuras (`paper/figures/`) e os testes
de figura entram no selo. O primeiro commit público não contém o artigo; ele entra num commit posterior, final, e o sha256 do PDF final
será gravado em `paper/PAPER-SHA256.txt` (arquivo à parte, criado depois do PDF, fora do selo).

## Trilha 1: leve (conferência dos derivados, ~6 min)

```bash
python3 -m pip install -r requirements.txt     # numpy, pandas, scipy, matplotlib
python3 -I run_all.py                          # integridade -> recálculo na réplica -> testes -> selo
python3 -I run_all.py --rapido                 # sem o recálculo (segundos): integridade + testes + selo
python3 -I scripts/reproduzir.py --only painel # só um passo do recálculo
```

Passos do recálculo (`scripts/reproduzir.py`, 28): concordância Sinan x Anuário (`concordancia_v2.py`), painel de governos em 3 especificações e
diagnósticos (`painel_f8.py`, `painel_diagnosticos.py`), reanálises pré-registradas C02 e C03 (`painel_c02_indet.py`, `painel_c03_event_pesos.py`),
intervalo do painel por inversão do wild-cluster (R6, `painel_r6_ic_wild_invertido.py`), troca de presidente (C09, `dados/presidencia/c09_*.py`),
exposição por governo (C10, `dados/exposicao/c10_*.py`), taxas padronizadas e projeção (`padroniza_idade.py`, `projecao_grupos.py`,
`contexto_local.py`), tabelas do Sinan, curadoria de governadores, amostra e sensibilidade da manchete do GGB, DiD/event study e proxies da F5,
séries e concordância das fontes de mortes LGBT+ (`s06_analises.py`), sensibilidade do TWFE a escores de ideologia, simulação de
identificabilidade. Cada um é comparado, arquivo a arquivo, com o commitado: bytes idênticos, ou diferença de no máximo 1 unidade da última
casa decimal impressa (arredondamento entre bibliotecas matemáticas; o script diz quando aceitou isso). Número impresso em precisão total
(repr do float, 15 ou mais algarismos significativos) aceita diferença relativa de até 1e-10: nos CSV de C02 e C03 os últimos bits mudam de uma
execução para outra NA MESMA máquina (soma em BLAS multithread, Accelerate no macOS), sem mudar nenhum número arredondado dos .md.

Semente: 20261021 (bootstraps, permutações, wild-cluster, Monte Carlo), 20261011 (simulação), outras declaradas no topo de cada script.
Com semente fixa e a mesma versão do numpy a saída é idêntica byte a byte (observado aqui para todos os passos acima, exceto os CSV em
precisão total de C02 e C03, que ficam dentro da tolerância relativa de 1e-10).

Verificação independente (outra álgebra, outra biblioteca): `dados/verificacao_independente.py` recalcula a correlação parcial de Spearman
(inversa da matriz de correlação), o IC da parcela LGB+ implícita na PNS (método delta em vez de Monte Carlo) e o painel TWFE (MQO com todas as
dummies explícitas e CR1 direto) e confere com os arquivos gerados e com o texto dos dossiês. Roda como teste (`tests/test_integridade.py`).

## Matriz de reprodução (v0.3)

Três situações, sem mistura: **recalcula** (o script roda a partir do que está aqui e o resultado é comparado byte a byte com o publicado),
**só confere** (o número publicado é relido e conferido por teste ou por outra conta, mas o cálculo original exige algo que não está aqui) e
**não se refaz** (depende do mundo naquele dia ou de dado nominal).

| Etapa | Entrada | Saída | Situação | Como |
| --- | --- | --- | --- | --- |
| Concordância saúde x polícia, painel de governos (3 especificações + diagnósticos), C02, C03, R6 | `dados/sinan`, `dados/anuario`, `dados/painel`, `dados/ideologia`, SIDRA, Power & Zucco | `dados/concordancia/`, `dados/painel/` | recalcula | `scripts/reproduzir.py` |
| **C09** troca de presidente (estrutura, D2 painel, D1 série nacional) | `dados/painel`, `dados/ideologia`, `dados/sim`, `dados/atlas_uf_series.csv`, SIDRA, Power & Zucco, `dados/presidencia/presidentes_2007_2024.csv` | `dados/presidencia/` | recalcula | `scripts/reproduzir.py` (3 passos, ~35 s) |
| **C10** exposição por governo (estrutura, E1 federal, E2 estadual) | as mesmas + `dados/presidencia/` | `dados/exposicao/` | recalcula | `scripts/reproduzir.py` (2 passos) |
| **Disque 100** séries e comparações (a partir de `saidas/d100_por_periodo.csv`) | `dados/disque100/saidas/`, `dados/disque100/entradas/`, `dados/sinan`, `dados/anuario`, SIDRA | `dados/disque100/saidas/d100_*.csv` | recalcula (6 saídas, byte a byte) | `scripts/reproduzir.py` (1 passo, `d100_series.py`) |
| **Disque 100** tabulação dos 23 microdados (14 GB) | os 23 CSV de `dadosabertos.mdh.gov.br`, baixados por `dados/disque100/scripts/baixar.py` (sha256 em `saidas/catalogo.tsv`) | `d100_por_periodo.csv` | só confere (feita no projeto do autor; o bruto não é distribuído nem baixado na réplica) | `dados/disque100/tests` (63 testes sobre as saídas e sobre as regras, em arquivos sintéticos) |
| Taxas padronizadas, projeção, contexto local, tabelas do Sinan, governadores (curadoria), F3/F5/GGB/ideologia, simulação | derivados de `dados/` e das frentes | idem | recalcula | `scripts/reproduzir.py` |
| Números publicados e valores desenhados nas figuras | todos os derivados | asserções | só confere | `pytest -q` (`tests/`, `paper/tests/`) |
| Verificação independente (Spearman parcial, IC delta, TWFE explícito) | derivados | asserções | só confere (outra álgebra) | `dados/verificacao_independente.py` |
| Inventário de fontes, idiomas, tipos e scripts | 18 ledgers, `verificacao-metadados.csv`, dossiês, `dashboard/dashboard_dados.publico.json` | `manifest/INVENTARIO-PUBLICO.{md,json}` | recalcula (e reproduz o painel com os 17 ledgers dele) | `scripts/inventario_publico.py --check` |
| PNS 2019 (C05, C08, cobertura, poder) | microdado do IBGE | `dados/pns/`, `dados/ggb/` | recalcula sob demanda (Trilha 2) | `scripts/acquire_pns2019.py` + scripts |
| SIM e Sinan agregados | microdado do DATASUS | `dados/sim/`, `dados/sinan/` | só confere (aquisição e hash testados; re-agregação não reexecutada nesta montagem) | `scripts/acquire_{sim,sinan}.py` |
| Universo nominal do GGB 2019, captura-recaptura, validação das 160 fontes | lista nominal + sal (não publicados) | `research-2026-10-21-rodada3/F3-ggb/dados/` | não se refaz aqui | lógica auditável em `s01`-`s14` |
| Notícias, buscas, Wikipédia, GDELT, leitura de PDFs, painel de contagens | o mundo na data da coleta; árvore privada | contagens, ledgers, `dashboard/` | não se refaz | URL, data e sha256 no manifesto |
| Export do artigo (DOCX/PDF) e juiz da rubrica | modelo DOCX, canon da casa, CLI de modelo | `paper/build/` (não distribuído neste commit) | não se refaz aqui (ferramenta do autor) | ver a seção Artigo |

Ambientes exercidos: macOS arm64 com Python 3.14.8 (selo e réplica) e, na v0.3, a suíte de testes também em Python 3.12 e 3.13 (venv
descartável, mesmas versões mínimas de `requirements.txt`; ver a seção Evidência). A CI do GitHub (Linux) continua não exercida.

## Trilha 2: do microdado oficial (pesada, sob demanda)

Os scripts abaixo baixam do órgão oficial e **conferem o SHA-256 esperado** (de `manifest/MANIFESTO-FONTES.csv`); divergência = versão diferente da usada.
O destino é `fontes/` (ignorado pelo git).

| Fonte | Script de aquisição | Tamanho | Scripts que a consomem |
| --- | --- | --- | --- |
| SIM/DATASUS, DOBR2010-2024 (óbitos por residência) | `scripts/acquire_sim.py` | ~1,6 GB | `dados/sim/agrega_sim.py` (gera `sim_agressoes_agregado.csv`), `dados/sinan/sim_adultos_18mais.py` |
| Sinan/DATASUS, VIOLBR15-25 | `scripts/acquire_sinan.py` | ~300 MB | `dados/sinan/serie_campo55_uf_ano.py`, `completude_sinan.py`, `triangulacao_pns_sinan.py` |
| PNS 2019, microdados e layout (IBGE) | `scripts/acquire_pns2019.py` | ~30 MB (455 MB descompactado) | `dados/pns/seguro_pns2019.py`, `dados/pns/pns_c05_razao_direta.py` (C05), `dados/ggb/cobertura_implicita.py`, `dados/ggb/ggb_c08_numeradores.py` (C08), `research-2026-10-21-rodada3/F2-custos/deff_pns2019.py` |
| TSE, consulta_cand 2010/2014/2018/2022 | `scripts/acquire_tse.py` | 4 zips | `dados/scripts/governadores_tse.py` |

`.dbc` do DATASUS exige `pyreaddbc` e `dbfread` (ambiente à parte; não estão em `requirements.txt`).
Arquivos **preliminares** do DATASUS (SIM 2023-2024, Sinan recente) são regerados pela origem: o hash do manifesto identifica a versão
usada; se o seu download divergir, os números de 2023-2025 podem diferir sem que haja erro de código.

## O que NÃO pode ser re-rodado (e onde isso aparece)

| Etapa | Por quê | O que há no repositório |
| --- | --- | --- |
| Universo nominal do GGB 2019 (329 casos), pareamento com o TDoR, captura-recaptura, validação das 160 fontes | exige a lista nominal e o sal do hash, **que não são publicados** (privacidade das vítimas) | ids de 10 hex (sha256 com sal não publicado), UF, categoria, domínio, codificação e resultados em `research-2026-10-21-rodada3/F3-ggb/dados/`; scripts `s01`-`s14` para auditoria da lógica |
| Fontes de notícia da amostra do GGB (links) | 31 de 160 links já estavam mortos (404) ao serem lidos; o web muda | tabela de recuperação e motivo da não recuperação em `F3-ggb/dados/` |
| Mídia e discurso (Google News RSS, OpenAlex, Wikipédia, GDELT, Câmara, Senado) | buscas e contagens dependem do dia; texto de notícia é de terceiros | contagens por consulta/ano com data e SHA-256 do bruto (`contagens.csv`, `SHA256SUMS-brutos.txt`), amostra codificada sem o texto (só `trecho_sha256`; o trecho do Parlamento fica) |
| Leitura de literatura (F8, mortalidade, falsas alegações) | leitura de PDFs de acesso restrito ou protegido por direito autoral | ledgers (`sources.jsonl`, 571 registros no consolidado), planilhas de triagem, trechos verbatim curtos com página e SHA-256 do PDF; marcas ✅/⚠️/🚫 nos dossiês |
| Governadores (Wikipédia) | curadoria manual de 27 páginas; parser automático foi descartado por erro | `mandatos_wiki.json`, `governadores_uf_2011_2026*.csv` e a validação contra o TSE (`governadores_tse_validacao.md`) |
| F5 (economia política: Atlas, orçamento, LAPOP, ESTADIC) | dependem de PDFs/planilhas oficiais baixados em 2026-10-21/22 | séries derivadas em `F5-economia-politica/dados/`, `SHA256SUMS.txt` dos brutos, scripts de parsing |
| `ideologia/` (survey de especialistas Bolognesi et al.) | microdado de terceiros | escores derivados e mapeamento de partidos; Power & Zucco (CC0) incluído |

## Pré-registros

`docs/PRE-REGISTROS/{governos,mortalidade,midia}/`: texto original, hash gravado **antes** da coleta, hora de gravação e adendo posterior (quando houve).
Os testes recomputam esses hashes (`tests/test_integridade.py`). As reanálises da revisão hostil têm critérios próprios, gravados antes de
qualquer script novo: `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md` (sha256 em `CRITERIOS.sha256`, conferido em
`tests/test_reanalises_publicadas.py`); a busca simétrica, em `escrutinio/simetria/CRITERIOS.md` e adendos datados (`SHA256SUMS-pre-execucao.txt`). O pré-registro de mídia teve um desvio declarado: a contagem corrigida do
Parlamento (14/56/148/2) difere do dicionário pré-registrado (23/161/692/4); o texto original e a emenda estão lado a lado.
Um caminho de pasta do projeto privado permanece em `docs/PRE-REGISTROS/midia/PRE-REGISTRO*.md` (linha 76) e em
`research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md` (linha 3): reescrevê-los quebraria o hash gravado. Pelo mesmo motivo os
pré-registros guardam termos de operação do projeto (glossário em `docs/INDEX.md`).

Na v0.3 entram mais três: `dados/presidencia/PREREGISTRO-C09.md` (C09), `dados/exposicao/PREREGISTRO-C10.md` (C10) e
`dados/painel/R6-PREREGISTRO-FORMA.md` (forma do intervalo por inversão do wild-cluster). Nos dois primeiros, a 1ª linha do `.sha256` é o
hash do corpo até a seção de adendos, de modo que adendos datados não mudam o hash; os testes `tests/test_c09_presidencia.py`,
`tests/test_c10_exposicao.py` e `tests/test_correcoes_v03.py` o recomputam.
O pré-registro do Disque 100 (`dados/disque100/PREREGISTRO-D100.md`) vale a mesma regra: o `.sha256` guarda o hash do corpo até a linha dos adendos e o de `scripts/d100_comum.py` (as regras de classificação); `python3 -I dados/disque100/scripts/d100_selo.py` o confere.

**O que o hash prova e o que não prova.** O hash verifica correspondência de conteúdo: o texto lido hoje é o mesmo que gerou o hash
gravado. A anterioridade (que o texto existia antes de os dados serem vistos) depende de evidência temporal independente; sem carimbo
externo, a hora gravada no `.sha256` é declaração do protocolo do autor, conferível só pela coerência com o resto do registro. Registro
externo (OSF, carimbo de tempo) está no `ROADMAP.md`.

## Alterações em relação aos arquivos do projeto privado

`manifest/MODIFICACOES.tsv` lista cada arquivo alterado, com o SHA-256 original e o publicado. As alterações são só: (i) caminho absoluto -> `REPO_ROOT`
(variável de ambiente; sem ela, a raiz do repositório), (ii) remoção de texto de terceiros da amostra de mídia, (iii) e-mail pessoal -> placeholder
em 3 scripts de coleta, (iv) dossiês lidos de `docs/dossies/` por `verificacao_independente.py`, (v) linguagem interna de operação (nomes
de agentes e ferramentas, números de pedido, papéis) trocada por termos neutros, também nos nomes de pastas não distribuídas citadas
(`fila-aquisicao`, `aquisicao-out`), sempre igual no script gerador e na saída, (vi) trecho verbatim de imprensa/academia removido de
`escrutinio/simetria/eventos_C18.csv` (fica `trecho_sha256`), (vii) caminho de CLI de modelo de linguagem trocado por variável de ambiente
(`GROK_BIN`, `AGY_BIN`) nos scripts que chamam esses modelos, marcados como ferramenta do autor. A lógica e os números não foram tocados. Os
`SHA256SUMS*` que vieram dentro das pastas das frentes e de `dados/` (por exemplo `dados/{painel,pns,ggb}/SHA256SUMS-reanalise.txt`, cujos scripts
ganharam o cabeçalho `REPO_ROOT`) descrevem os arquivos **privados** de origem e não conferem com `shasum -c` nos arquivos alterados; o manifesto da
raiz é o que vale para este repositório. Pelo mesmo motivo, `escrutinio/_build_triagem.py` não regera `TRIAGEM.csv/.md` byte a byte (a execução
original embutiu caminhos absolutos, depois trocados nos dois lados).

## Artigo (`paper/`)

| Parte | Neste commit? | Roda no clone? | Como |
| --- | --- | --- | --- |
| Testes de figura (`paper/tests/test_figuras.py`) | sim, no selo | sim | `pytest -q` (ou `run_all.py`): reabre as fontes copiadas, confere com `dados/` e com `dashboard/dashboard_dados.publico.json` |
| Figuras (`paper/figures/make_figures.py`) | sim, no selo | sim (matplotlib) | determinístico; `figures/SHA256SUMS` |
| Texto do artigo, PDF, DOCX, auditoria e ferramentas de export (`paper/paper.md`, `paper/build/`, `paper/tools/`, `paper/AUDIT.md`, `paper/tests/test_anexo.py`) | não: entram depois, fora do selo | export e juiz: não (ferramenta do autor: modelo DOCX, canon da casa, pandoc, Word, CLI de modelo pela assinatura do autor) | verificação de referências, densidade e E-E-A-T rodarão no clone quando o artigo entrar |
| Hash do PDF final (`paper/PAPER-SHA256.txt`) | não: criado depois do PDF final | sim | `shasum -a 256 -c` sobre o arquivo, fora do selo |

Enquanto o artigo não estiver no repositório, `scripts/auditar_publicacao.py --check literatura` confere os ledgers e a planilha de verificação e
declara a conferência artigo x ledger como "NÃO EXERCIDA". Depois do primeiro commit, o histórico do git é o registro de mudanças;
`manifest/MODIFICACOES.tsv` registra só a sincronização inicial com o projeto de origem.

## Evidência desta montagem

Ver `BUILD-STATE.md` (local, não versionado) e a saída de `python3 -I run_all.py`. Em 2026-10-23, C05 e C08 foram rodadas contra uma cópia
local do microdado da PNS 2019 (o mesmo arquivo do IBGE usado na pesquisa, não baixado de novo nesta etapa) e reproduziram as quatro saídas byte a byte.
Trilha 2 exercida de ponta a ponta (download + hash + recálculo) só para a **PNS 2019**: `acquire_pns2019.py` baixou do IBGE (SHA-256 conferido) e `seguro_pns2019.py` e
`cobertura_implicita.py` reproduziram os 4 derivados byte a byte. Para SIM e Sinan só a aquisição de amostra (VIOLBR16, dicionário PNS) e o hash foram testados; o recálculo a partir do
microdado bruto do SIM e do Sinan **não** foi reexecutado. A CI do GitHub não havia sido exercida antes do commit inicial: o primeiro resultado é o da aba Actions desse commit (Linux, Python 3.12 e 3.13).

Na v0.3 (2026-10-24): recálculo completo (28 passos, incluindo C09, C10 e R6) em Python 3.12.12 com numpy 2.5.4, pandas 3.1.0, scipy 1.18.1 e
matplotlib 3.11.2, versões mais novas que as do `requirements.lock`: 54 arquivos idênticos byte a byte, 2 equivalentes numéricos (os CSV de
precisão total de C02 e C03), 0 divergência. Em Python 3.14.8 (ambiente do lock), `--only dados/`: 35 idênticos, 2 equivalentes, 0 divergência.
A suíte de testes rodou em 3.12, 3.13 e 3.14 (contagens no relatório da versão). Python 3.11 não é suportado: um script de pesquisa
(`research-2026-10-21-rodada3/discurso/governos/scripts/tabela_md.py`) usa sintaxe de f-string que só compila a partir da 3.12.
