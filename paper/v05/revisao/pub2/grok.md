Vou conferir a matriz da rodada anterior no PDF e nos arquivos do repositório, e só depois marcar o que ainda bloqueia.A matriz diz que os ponteiros e os metadados foram corrigidos. Vou cruzar isso com o PDF, o selo e os arquivos que a rc1 publicaria.Vou conferir no disco os pontos que ainda podem mudar o veredito: hashes, selo, carimbos do adendo e o quadro que a rodada anterior tratou como não procedente.# Parecer de pré-publicação — Grok 4.7 (grok-4.7)

## Conferência

| ID | Conferência | Por quê | Evidência |
|---|---|---|---|
| AST-P01 | resolvida | O Apêndice H diz que as 60 consultas classificaram o ato pela imprensa e que a Portaria nº 1.576/2019 foi lida depois no Diário Oficial; o texto da portaria não cita LGBT, e a referência entrou na lista. | PDF p. 145–148; `paper/v05/referencias.md` (Ministério da Cidadania, 2019) |
| AST-P02 | resolvida em parte | Versão 1.0.0, data 31/10/2026 e descrição longa da v0.5 estão em CITATION, codemeta e .zenodo; o `pyproject.toml` está em 1.0.0 com descrição curta, sem a descrição da v0.5. `access_right: closed` é o estado previsto até o commit da rc1. | `CITATION.cff` l. 15–16; `codemeta.json`; `.zenodo.json` l. 4–6; `pyproject.toml` l. 3–4 |
| AST-P03 | não verificado | O CHANGELOG afirma `ruff` limpo; esta rodada não reexecutou `ruff check` nem `ruff format --check`. | `CHANGELOG.md` l. 21 |
| AST-P04 | resolvida em parte | A capa pública aponta `docs/paper/` e a v0.5; a Tabela M1 ainda manda a busca de atos à seção 3.6, o README-resumo arredonda o Sinan e o CHANGELOG da 1.0.0 ainda cita o caminho antigo da LiHS. | `README.md` l. 21 e 79; `paper/v05/MATERIAL-COMPLEMENTAR.md` l. 1280; `CHANGELOG.md` l. 129 |
| AST-N01 | resolvida em parte | “3,01 milhões” e o veredito de mortalidade passaram a remeter aos Apêndices C e E; a Tabela B2 e mais quatro pontas continuam na numeração da v0.4.4. | PDF p. 72, 77, 93, 102 e 165; `MATERIAL-COMPLEMENTAR.md` l. 51–58, 109, 424, 493, 1280 |
| AST-N02 | resolvida em parte | `paper/v05/README.md` delimita os oito testes de `tests/test_numeros_v05.py` e troca “Tabela MC5.C1” por “Tabela F4”; a tabela “Em resumo” do README raiz segue com 0,5% e 42-44%. | `paper/v05/README.md`; `tests/test_numeros_v05.py`; `README.md` l. 79 |
| AST-N03 | resolvida | Gambling Commission (2025) e Banco Central do Brasil (2026) estão na lista e nas notas das Tabelas 6 e K1. | PDF p. 48 e 160; `paper/v05/referencias.md` |
| AST-N04 | resolvida | A frase passou a “Essas coortes são descritas no Apêndice E”; o apêndice descreve Saxby, Hsu e K. D. Clark sem prometer os números. | PDF p. 30 e 100 |
| AST-N05 | resolvida | A Tabela G7 traz “< 0,001” onde o CSV tem 0,0002; o Holm 0,0012 aparece como 0,001. | PDF p. 140; `dados/exposicao/c10_e2_resumo.csv` (bloco centro, mulheres) |
| AST-N06 | resolvida | As citações distinguem K. A. Clark e K. D. Clark. | PDF p. 27 e 30 |
| AST-N07 | resolvida | Os três registros do selo dizem 772 arquivos e o mesmo `chain_hash` `170b0718…`; `shasum -c` e `--verify` não foram reexecutados. | `output/hash-chain.md`; `paper/PAPER-SHA256.txt` l. 9; `runs/20261031T233520Z/manifest.json` |
| AST-N08 | resolvida | As saídas cruas citadas (“divergências = 0”, “AJUSTADA”, “(publicado: 2,82”) e “Tabela MC5.C1” não aparecem no PDF nem no README da v0.5. | PDF, Apêndice C; `paper/v05/README.md` |
| GRO-P01 | resolvida em parte | Cobre o bump e a face pública: a versão científica fechou; a face pública e as remissões herdadas não. | Mesmas evidências de AST-P02, AST-P04 e AST-N01 |
| GRO-P02 | resolvida em parte | README, REPRODUCIBILITY e a Tabela M1 foram reescritos em parte; REPRODUCIBILITY ainda data a verificação em 23/10 e intitula a matriz “v0.3”. | `REPRODUCIBILITY.md` l. 10 e 56; `CHANGELOG.md` l. 11–12 |
| GRO-P03 | não resolvida | O único run selado continua com `working_tree_dirty: true` no commit `0601c65`. | `runs/20261031T233520Z/manifest.json` l. 6–7 |
| GRO-N01 | resolvida | Mesma conciliação da Portaria que AST-P01, sem “(Apêndice H)” dentro do H. | PDF p. 145–148 |
| GRO-N02 | resolvida em parte | Mesmo saldo de AST-N01: parte das remissões foi atualizada; o miolo da Tabela B2 não. | PDF p. 72 |
| GRO-N03 | resolvida | A divergência 767 contra 768 foi substituída pelo trio coerente de 772 arquivos. | `output/hash-chain.md`; `paper/PAPER-SHA256.txt`; manifesto do run |
| GRO-N04 | resolvida em parte | O alcance de `test_numeros_v05.py` foi delimitado; o arredondamento do Sinan no README raiz permanece. | `README.md` l. 21 (faixa certa) e l. 79 (faixa arredondada) |
| GRO-N05 | resolvida | A frase da TGEU ficou atribuída à reportagem “Big Data, 331 Deaths” (2019), que está na lista; o glossário expande TGEU. | PDF p. 67 e 120 |
| GRO-N06 | resolvida | O README da v0.5 aponta a Tabela F4, não “Tabela MC5.C1”. | `paper/v05/README.md` |
| ARG-P01 | resolvida | A frase das coortes foi corrigida. A alegação de que `QUADRO-E2.md` é órfão e devia ir para o Apêndice E não procede: o arquivo é o registro de trabalho da Tabela 2 e está citado na Tabela M1. | PDF p. 30; `paper/v05/QUADRO-E2.md` l. 1 e 34–36; Tabela M1, PDF p. 164 |
| ARG-P02 | resolvida em parte | Mesma face pública de AST-P04. | `README.md`; `CHANGELOG.md` l. 11–14 e 129 |
| ARG-P03 | resolvida | Mesma conciliação da Portaria. | PDF p. 145–148 |
| ARG-P04 | não procedência aceita | No extrato, a p. 46 fecha com “(Apêndice B)”. | PDF p. 46 |
| ARG-N01 | resolvida | “Exigir que todas as linhas da denúncia sejam do módulo LGBT reduz 2025 de 9.346 para 39 denúncias” está no Apêndice D. | PDF p. 94 |
| ARG-N02 | resolvida em parte | Some caminhos da v0.5 e o caso dos 3,01 milhões foram atualizados; as seções 3.8, 3.9, 3.10 e 3.11–3.13 continuam citadas como se existissem. | PDF p. 72; `MATERIAL-COMPLEMENTAR.md` l. 51–58 |
| ARG-N03 | resolvida | O acabamento tirou do Apêndice C as cadeias de saída de script citadas na matriz. | PDF, Apêndice C |
| ARG-N04 | resolvida | “Nesse apêndice”, UNAMI/OHCHR por extenso na primeira citação e ODIHR padronizado. As duas partes de não procedência procedem como alegação falsa: a Tabela 3 traz “4,79 (2,58 a 8,90)” e a Lei 15.380 aponta `lei/l15380`. | PDF p. 20, 51 e 150 |
| ARG-N05 | resolvida em parte | A parte de versão acompanha AST-P02. A parte do adendo não procede: o arquivo tem os dois carimbos completos. | `research-2026-10-21-rodada3/escrutinio/simetria/ADENDO-2.hora.txt` l. 1–2 |

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | não pronto | A Tabela B2 e quatro outras remissões ainda apontam seções da v0.4.4 que não existem ou que hoje são outro assunto, e a nota da Tabela B1 afirma que isso já foi atualizado. |
| 2. Repositório atualizado | com ressalvas | Versão, data, autoria e descrição longa fecham em CITATION, codemeta e .zenodo; o README-resumo, o CHANGELOG da 1.0.0, a REPRODUCIBILITY e o run selado não fecham com o PDF. |
| 3. DOI | pode depois de corrigir os bloqueantes | A rc1 gravaria no PDF as remissões erradas e nasceria de um selo com árvore suja; o DOI em si, a frase “será atribuído na publicação” e o `access_right: closed` são o estado previsto até esse commit. |

`ruff`, pytest, `run_all`, crivo, validador 54/54, `pdfinfo`, `shasum -c` e `python3 -I make_provenance.py --verify` não foram reexecutados nesta rodada. Os números 185, 122/122, 54/54 e 0/0 da aplicação ficam não verificados.

## Bloqueantes

### GRO-P01

Local: PDF p. 72, 77, 93, 102, 153 e 165 (`paper/v05/MATERIAL-COMPLEMENTAR.md` l. 32, 51–58, 109, 424, 493, 1147 e 1280).

Trecho: “As seções 3.11 a 3.13 trazem resultados de contexto”; “ressalvas do informe registradas na seção 3.9”; “R = I × p (seção 2.5)”; “controle positivo do argumento da seção 3.4”; “Busca simétrica de atos de governo | seção 3.6”; “seção 3.6 e Apêndices G e H”.

Problema: a coluna “Seção” da Tabela B2 não está rotulada como numeração antiga, ao contrário da Tabela B1. Hipótese 2 aponta 3.2 e 3.3 (hoje registros e mortes no Brasil; mortalidade e controle positivo estão em 3.3 e 3.4). Hipótese 3 aponta 3.4 (hoje mortes fora do Brasil; a lista do GGB é a 3.5). Hipótese 4 aponta 3.5 (hoje o GGB; registros são a 3.2). Hipótese 5 inclui a 3.7 (hoje Parlamento). Hipóteses 6 e 7 e a nota citam 3.8, 3.9, 3.10 e 3.11–3.13, que o artigo não tem. A Equação 1 está na seção 2.3, não na 2.5. O controle positivo por sexo e raça está na seção 3.3, não na 3.4. A busca de atos abre na seção 3.7 e no Apêndice H, não na 3.6. A nota da Tabela B1 e o `CHANGELOG.md` l. 14 dizem que as remissões herdadas já apontam as seções atuais.

Evidência: mapa correto na própria Tabela B1 (PDF p. 69); corpo do artigo termina na seção 3.7 (PDF p. 37).

Correção proposta: reapontar essas seis pontas pelo mapa da Tabela B1 e só então manter a nota e a linha do CHANGELOG.

### GRO-P02

Local: `runs/20261031T233520Z/manifest.json` l. 6–8.

Trecho: `"commit": "0601c65e13280dcc6c82c5468997930517dedad0"` e `"working_tree_dirty": true`, com `chain_hash` `170b0718…` e `sealed_files` 772.

Problema: o selo desta cópia foi gravado sobre árvore suja. A rc1 não pode sair desse run. `REPRODUCIBILITY.md` l. 24–26 diz que o commit `0601c65` não contém o artigo e que a v0.5 entra no commit da 1.0.0. O `--verify` não foi reexecutado aqui.

Evidência: o manifesto; `REPRODUCIBILITY.md` l. 24–26.

Correção proposta: commit novo, limpo, com `python3 -I make_provenance.py --verify` verde nesse commit, e o `access_right` só vira `open` nesse commit, com o OK do autor.

## Não bloqueantes

### GRO-N01

Local: `README.md` l. 79.

Trecho: “LGBTfobia em 0,5% das notificações; faltante efetivo do campo 55 em 42-44%”.

Problema: o PDF, o manuscrito e o próprio destaque do README (l. 21) dizem 0,4% a 0,5% e 42,5% a 44,5%. O `CHANGELOG.md` l. 12 afirma que os números do Sinan já ficaram iguais aos do PDF.

Evidência: PDF p. 15 e 25; `paper/v05/MANUSCRITO.md` (Tabela 2 e seção 3.2); `README.md` l. 21.

Correção proposta: igualar a célula “Em resumo” à faixa do PDF.

### GRO-N02

Local: `CHANGELOG.md` l. 129 e 136, dentro de `[1.0.0]`.

Trecho: “`dados/lihs-checagem-ggb2016.META.md` guarda a URL”; “Versão segue `0.x`”.

Problema: esse caminho não é o da raiz. O arquivo está em `research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md`, como o README l. 280 e o `paper/v05/README.md` l. 34 já dizem. A frase da versão 0.x contradiz o cabeçalho 1.0.0 da mesma seção.

Evidência: ausência do arquivo na raiz; `README.md` l. 280.

Correção proposta: corrigir o bullet “Adicionado” da 1.0.0 para o caminho real e tirar a frase de versão 0.x.

### GRO-N03

Local: `REPRODUCIBILITY.md` l. 10, 56 e 77.

Trecho: “Resultado verificado em 2026-10-23”; “Matriz de reprodução (v0.3)”; “`paper/build/` (não distribuído neste commit)”.

Problema: o run selado é de 31/10/2026, Python 3.14.10 (`manifest.json`). O PDF da v0.5 está em `docs/paper/paper-final.pdf`. `scripts/reproduzir.py` não nomeia os geradores `fig_*_v05`. Não verifiquei se outro teste compara o pixel das figuras.

Evidência: `REPRODUCIBILITY.md`; manifesto do run; busca em `scripts/reproduzir.py`.

Correção proposta: datar a evidência do run de 31/10, tirar o rótulo “v0.3” da matriz vigente e declarar em que trilha entram as figuras da v0.5.

### GRO-N04

Local: `paper/v05/QUADRO-E2.md` l. 34–36, citado na Tabela M1 (PDF p. 164).

Trecho: “saem do corpo para o MC7”; “as finais saem no E5”.

Problema: o arquivo se apresenta como registro de trabalho e ainda aponta um destino que não é o desta versão. A Tabela 2 publicada já está no PDF. Isso não o torna órfão nem texto do Apêndice E.

Evidência: `QUADRO-E2.md` l. 1 e 34–36; Tabela 2, PDF p. 13–15.

Correção proposta: uma linha no topo do arquivo dizendo que a Tabela 2 do PDF é a forma publicada e que MC7 é o antigo Apêndice H.

### GRO-N05

Local: PDF p. 150, Apêndice I.

Trecho: “a OSCE concluiu haver «overwhelming evidence»” antes de “(Organization for Security and Co-operation in Europe [OSCE], 2018)”.

Problema: a sigla aparece antes da forma expandida na mesma frase.

Evidência: PDF p. 150; `MATERIAL-COMPLEMENTAR.md` no parágrafo da Chechênia.

Correção proposta: expandir OSCE na primeira menção.

## O que está bom

- Os números centrais conferidos nas seções 1–6 batem com tabelas e apêndices: 14,70% e 3,82%, razão 2,82 (2,16 a 3,68), familiar 4,79 (2,58 a 8,90), 783 a 3.481, 39 denúncias, 51,7 e 2,6, razão 1,31, 50 de 160.
- CITATION.cff, codemeta.json e .zenodo.json estão em 1.0.0, data 31/10/2026, com Carlos Ulisses Flores, ORCID 0000-0002-6034-7765 e Codex Hash Research Laboratory; o PDF declara a versão 1.0.0 e deixa o identificador permanente para a publicação.
- A Portaria nº 1.576/2019, os dois Clark, o contrato britânico e o câmbio PTAX estão citados nos dois sentidos da lista única.
- A Tabela B1 separa, com rótulo, a seção antiga do apêndice atual; os apêndices do PDF vão de B a M.
- O identificador `170b0718…` e a contagem de 772 arquivos coincidem em `output/hash-chain.md`, `paper/PAPER-SHA256.txt` e no manifesto do run.

A próxima ação é corrigir as remissões do GRO-P01 no texto r10, refazer o PDF e selar de novo num commit limpo antes da rc1.