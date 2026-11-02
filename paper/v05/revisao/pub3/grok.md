A conferência começa pelos pontos da matriz e pelos arquivos que travam número, versão e hash. Vou cruzar o PDF com o repositório antes dos vereditos.Vou fechar a conferência nos pontos que ainda mudam o veredito: a frase da seção 2.6, os caminhos citados e a diagramação do PDF.A rc1 ainda não pode sair. A seção 2.6 do PDF afirma que o efeito dos desacordos do GGB sobre as contagens não foi estimado, e o próprio artigo já publicou esse efeito (73 para 74).

## Conferência

| ID | Situação | Por quê | Evidência |
|---|---|---|---|
| AST-R2-02 | resolvida | O ajuste sem os 9 adultos de cor ou raça ignorada (C009 = 9) está publicado; a física fica em 2,82 e a sexual passa de 5,00 (3,17 a 7,89) para 5,02 (3,18 a 7,92), n = 85.904. | PDF, nota da Tabela C2 e Tabela C12; `paper/v05/MATERIAL-COMPLEMENTAR.md`; o teste `test_pns_razoes_sem_cor_ignorada_mudam_no_maximo_0_02` em `tests/test_numeros_v05.py` trava a seção 8 de `dados/pns/agressor_risco_pns2019.md`. Pytest não executado nesta conferência. |
| ARG-02 | resolvida | A coluna com cônjuge no domicílio está na Tabela C10: familiar 4,31 (2,33 a 7,99); parceiro 2,42 (1,44 a 4,07); desconhecido 1,91 (1,12 a 3,26); amigo, colega ou vizinho 1,85 (0,89 a 3,83), intervalo que inclui 1. O corpo repete o familiar e a perda de firmeza. | PDF, p. 19 e Tabela C10; `tests/test_numeros_v05.py` (`test_pns_razao_por_agressor_com_conjuge_no_domicilio`) trava a linha do familiar e o intervalo do amigo no bloco `rp_ajustada_agressor_conjuge`. Pytest não executado. |
| ARG-01 | resolvida | A nota da Tabela 6 separa os denominadores: 1,35% com entrevistador e 3,26% com autopreenchimento sobre todos os adultos do modo; 1,38% e 3,51% entre quem declarou orientação. O módulo na PNAD Contínua fica em 37,9% ou 23,8% (31,7% com 1,89%). O painel pela internet aparece só com autopreenchimento. | PDF, nota da Tabela 6 e Tabela K2; `tests/test_numeros_v05.py` trava `research-2026-10-21-rodada3/F2-custos/opcoes_por_modo.csv` em 0,0135 / 0,379 e 0,0326 / 0,238. Pytest não executado. |
| AST-01 | resolvida em parte | Contagens, Tabela 2, seção 3.5, Figura F1 (legenda), nota da Tabela F3 e o JSON passaram a 74 mortes violentas, 36 motivos desconhecidos e 24 notícias sem a condição LGBT+; os 50 de 160 e o kappa A contra B ficam. A seção 2.6 continua dizendo que o efeito não foi estimado. | PDF, p. 12, contra p. 31–32 e nota da Tabela F3; `paper/v05/MANUSCRITO.md`, linha 90; `paper/figures/fontes/ggb_validacao_resumo.json` (`morte_violenta` 74, motivo `U` 36); `tests/test_numeros_v05.py` (`test_ggb_terceira_leitura_dos_desacordos_muda_so_um_caso`). |
| GRO-02 | não resolvida | O cenário numérico de subdeclaração não foi feito. A omissão está declarada como limite e não entra como defeito desta rodada. | PDF, seção 3.1 (“efeito que não foi estimado”) e seção 5; `CHANGELOG.md`, linha 24. |
| Diagramação | resolvida | Os quatro pontos pedidos estão no PDF impresso: carimbos da Tabela B3 inteiros; intervalos da Tabela 3 dentro da célula; a impressão digital longa em linha própria, à esquerda; a nota da Tabela I1 cola na continuação da tabela. | PDF, pp. 75, 20, 166 e 154. |
| Processo | resolvida | O registro novo separa tokens novos dos lidos do cache e marca o Argon como estimativa. A Tabela M1 aponta o arquivo. | `docs/processo-e-custo.md`; PDF, Tabela M1. |

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | não pronto | A p. 12 nega uma estimativa que a seção 3.5, a Tabela 2 e o Apêndice F já publicam (73 para 74). |
| 2. Repositório atualizado | com ressalvas | O texto-fonte repete a frase falsa da p. 12; o laudo de 21/10 e um caminho do changelog ficaram na contagem antiga. |
| 3. DOI | pode depois de corrigir os bloqueantes | A rc1 congela o PDF; a frase da seção 2.6 tem de sair antes. A ausência do DOI, hoje, é o fluxo da casa. |

## Bloqueantes

### GRO-P01

- Local: PDF, p. 12, seção 2.6; o mesmo período em `paper/v05/MANUSCRITO.md`, linha 90.
- Trecho literal curto: “O efeito dos desacordos sobre as contagens não foi estimado.”
- Problema: a frase é o texto da r8, escrito quando a terceira leitura ainda não existia. A leitura de 2026-11-01 entrou nas contagens e a frase ficou. Quem lê o método conclui que o efeito dos 6 desacordos não foi medido; o resultado diz o contrário.
- Evidência verificável: na p. 12, κ = 0,46 e, em seguida, a frase acima. Na seção 3.5 e na Tabela 2 (linhas 17 e 18), 74 de 88 (84,1%) e 36 motivos desconhecidos. Na nota da Tabela F3, um caso muda as contagens, 73 para 74, e os 50 de 160 não mudam. `paper/figures/fontes/ggb_validacao_resumo.json` traz `"morte_violenta": 74` e motivo `"U": 36`. `tests/test_numeros_v05.py` trava (74, 50, 36) e não trava a frase da seção 2.6. Nenhum teste do repositório contém “não foi estimado”.
- Correção proposta: trocar a frase pelo resultado da terceira leitura (um caso, 73 para 74; motivo desconhecido, 35 para 36; 24 notícias sem a condição LGBT+; 50 de 160 iguais; kappa continua A contra B) e remeter à nota da Tabela F3. Refazer o PDF antes da rc1. Acrescentar ao teste uma trava da frase nova, porque a trava atual não pega prosa.

## Não bloqueantes

### GRO-N01

- Local: `docs/laudos/F3-ggb-README.md`, linhas 12–13 e a tabela da linha 61. Data no cabeçalho: 2026-10-21.
- Trecho literal curto: “morte violenta confirmada em 83,0% (73/88”; “motivo desconhecido 47,9% (35/73)”.
- Problema: o laudo continua com o funil anterior à terceira leitura. O PDF e `ggb_validacao_resumo.json` estão em 74/88 e 36. O `README.md` da raiz não repete 73/88, e a Tabela M1 aponta `research-2026-10-21-rodada3/F3-ggb/`, não este laudo.
- Evidência verificável: linhas 12–13 e 61 do laudo, contra `"morte_violenta": 74` em `paper/figures/fontes/ggb_validacao_resumo.json`.
- Correção proposta: datar o laudo como anterior a 2026-11-01 e apontar o funil vigente, ou atualizar 73/88, 19/73 e 35/73 para 74/88, 24/74 e 36/74.

### GRO-N02

- Local: `CHANGELOG.md`, linhas 16–18.
- Trecho literal curto: “conferida pelo autor (`dados/adjudicacao.json`)”.
- Problema: esse caminho não é o arquivo. O script grava em `research-2026-10-21-rodada3/F3-ggb/dados/adjudicacao.json`. A nota da Tabela F3 usa o caminho certo. `output/provenance.json` também.
- Evidência verificável: `CHANGELOG.md`, linha 18; `tests/test_numeros_v05.py`, linha 288; `output/provenance.json` lista o caminho longo.
- Correção proposta: substituir `dados/adjudicacao.json` pelo caminho longo no changelog.

### GRO-N03

- Local: PDF, lista de referências; `paper/v05/referencias.md`, linhas 33 e 77; as mesmas URLs em `paper/v05/MANUSCRITO.md`, linhas 443 e 487.
- Trecho literal curto: `https://web.archive.org/web/2016id_/http://cnv.memoriasreveladas.gov.br/...` e `.../RELEASE-Mortes-Violentas-de-LGBT%5EM%5EJ-2025-GGB.pdf`.
- Problema: `2016id_` não é carimbo Wayback de 14 dígitos. `%5EM%5EJ` é a sequência de carriage return e line feed (`^M^J`) no nome do arquivo, no lugar de um `+` (`%2B`). Título e autor identificam as duas obras. O sítio ao vivo não foi consultado (esta conferência não acessa a rede). O defeito já estava no juiz da v0.4 e permanece no PDF final.
- Evidência verificável: as duas linhas de `paper/v05/referencias.md`; o mesmo carimbo `2016id_` em `paper/build/juiz/rodada-v4-5.json`.
- Correção proposta: recolocar o carimbo Wayback de 14 dígitos da cópia lida e o nome de arquivo do release de 2025 sem `%5EM%5EJ`, e refazer o PDF no mesmo passe da GRO-P01.

### GRO-N04

- Local: capa do PDF (“Data: 31 de outubro de 2026”); `CITATION.cff` e `codemeta.json`, `date-released` / `dateModified` = 2026-10-31.
- Trecho literal curto: “31 de outubro de 2026”.
- Problema: a terceira leitura, a Tabela C12 e `docs/processo-e-custo.md` estão datados em 1º de novembro de 2026. A capa fica um dia antes do último resultado que o PDF publica.
- Evidência verificável: capa; `CHANGELOG.md`, cabeçalho “2026-10-30 a 2026-11-01”; `docs/processo-e-custo.md`.
- Correção proposta: acertar a data da capa na refeitura do PDF. Pode ir no mesmo passe que insere o DOI.

## O que está bom

- As razões novas da PNS fecham entre o PDF, o material complementar e o código do teste: física 2,82 inalterada, sexual 5,02, familiar com cônjuge 4,31 (2,33 a 7,99), e 1,35% / 3,26% por modo na Tabela K2.
- Fora da frase da seção 2.6, o funil do GGB está alinhado: 74 de 88, 36 motivos desconhecidos, 50 de 160, kappa ainda A contra B.
- Metadados em 1.0.0 com o texto em v0.5, autor, ORCID e afiliação batem em `CITATION.cff`, `codemeta.json` e `.zenodo.json`. O DOI ainda ausente e o `access_right` fechado estão escritos como etapa anterior à rc1.
- O selo registrado `6c407be26f71c6e0c228e36ba67596811f76d7e11d56cfae65b16ea731503436` (781 arquivos) é o mesmo em `output/hash-chain.md`, `paper/PAPER-SHA256.txt` e `runs/20261101T234846Z/manifest.json`. O byte do PDF não foi recalculado aqui. O manifest marca `working_tree_dirty: true`; não conferi se algum arquivo sujo entra nos 781.
- A diagramação conferida nas pp. 20, 75, 154 e 166 sustenta os quatro acertos pedidos. A varredura APA nos dois sentidos, linha a linha, não foi refeita; nos pontos lidos não apareceu citação órfã nova.

Nada pendente nesta conferência além de corrigir a GRO-P01 e refazer o PDF antes da tag `v1.0.0-rc1`.