# Parecer de pré-publicação — GPT-6 Astra (gpt-6-astra)

Auditoria local, sem internet e sem alteração de arquivos. PDF conferido: **169 páginas**, SHA-256 `62150314b322e0ca4897e917781f8f4a04f7371a16154809cc5d5067a69c991e`. Conferi texto, remissões, arquivos e hashes; inspecionei visualmente sete páginas e executei **49 testes numéricos, todos aprovados**.

Suíte completa, recálculo dos microdados, inspeção visual das demais páginas, validador externo da casa, situação pública do GitHub e integração com o Zenodo: **não verificado**. A suíte de figuras não pôde ser importada por ausência de `numpy`; a recontagem do GGB foi conferida separadamente.

## Conferência

| ID original | Situação | Por quê | Evidência |
|---|---|---|---|
| AST-R2-02 | resolvida | A exclusão dos nove adultos está implementada e documentada; as estimativas publicadas conferem, com diferença máxima de 0,02. | PDF, pp. 84 e 90; `dados/pns/agressor_risco_pns2019.py`, função `poisson_lgb`; `tests/test_numeros_v05.py`. |
| ARG-02 | resolvida | A coluna com coabitação existe, coincide com os derivados e foi incorporada à interpretação do texto. | PDF, pp. 19 e 88; `dados/pns/agressor_risco_pns2019.csv`, bloco `rp_ajustada_agressor_conjuge`. |
| ARG-01 | resolvida em parte | Os denominadores e cálculos conferem; resta uma inconsistência de apresentação dos cenários do painel pela internet. | PDF, pp. 49 e 163; `research-2026-10-21-rodada3/F2-custos/opcoes_por_modo.csv`; AST-N02 abaixo. |
| AST-01 | resolvida em parte | A adjudicação e as contagens foram atualizadas, inclusive nas figuras, mas a seção 2.6 ainda declara que a análise não foi feita. | PDF, pp. 12, 32, 111 e 120; `research-2026-10-21-rodada3/F3-ggb/dados/adjudicacao.json`. |
| GRO-02 | não resolvida | O cenário numérico continua não realizado por decisão expressa; o limite está declarado e não constitui, por si, erro de pré-publicação. | PDF, p. 21; `CHANGELOG.md`, seção das análises de 2026-11-01. |
| Diagramação | resolvida | Os alvos conferidos mostram carimbos íntegros, intervalos preservados, nota com hash alinhada à esquerda e nota da I1 junto da tabela. | PDF, pp. 20, 75, 121 e 154; `paper/tools/export_v04.py`. |
| Processo | resolvida em parte | O registro existe e identifica estimativas e registros privados, mas exagera a cobertura dos hashes das fontes. | `docs/processo-e-custo.md`; PDF, p. 169; `manifest/MANIFESTO-FONTES.csv`; AST-N03 abaixo. |

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | **pronto com ressalvas** | Os resultados novos conferem; permanecem uma declaração metodológica desatualizada e uma nota imprecisa. |
| 2. Repositório atualizado | **com ressalvas** | Artefatos, metadados de versão e hashes conferem, mas há documentação desatualizada e falta comprovar o commit publicável. |
| 3. DOI | **pode depois de corrigir os bloqueantes** | A rc1 precisa apontar para o pacote completo e verificado; essa vinculação continua não demonstrada. |

## Bloqueantes

### AST-P01 — Falta comprovar o commit completo que receberá a rc1

- **Local:** `runs/20261101T234846Z/manifest.json`; `REPRODUCIBILITY.md`; `paper/v05/revisao/pub2/MATRIZ.md`.
- **Trecho literal curto:** `"commit": "0601c65e13280dcc6c82c5468997930517dedad0"`; `"working_tree_dirty": true`.
- **Problema:** permanece a pendência operacional reconhecida na pub2. O selo comprova o conteúdo desta cópia, mas o manifesto não demonstra que esse conteúdo está integralmente no commit que receberá a tag.
- **Evidência verificável:** o manifesto associa o selo atual `6c407be2…503436`, de **781 arquivos**, a uma árvore suja. `REPRODUCIBILITY.md` informa que o commit `0601c65` não contém o artigo. Esta cópia não contém `.git`; eventual commit posterior está **não verificado**.
- **Correção proposta:** concluir e publicar o commit completo, conferir nele o selo e os hashes do artigo e registrar a validação do commit que servirá de base à `v1.0.0-rc1`. No commit da rc1, aplicar também a abertura de acesso já prevista em `.zenodo.json`. O `closed` atual é coerente com a preparação e não é, isoladamente, defeito.

## Não bloqueantes

### AST-N01 — A seção 2.6 nega uma análise agora realizada

- **Local:** PDF, p. 12; `paper/v05/MANUSCRITO.md:90`; `docs/paper/paper-final.docx`.
- **Trecho literal curto:** “O efeito dos desacordos sobre as contagens não foi estimado.”
- **Problema:** a frase ficou desatualizada após a adjudicação e contradiz a nota da Tabela F3.
- **Evidência verificável:** a p. 120 registra a terceira leitura e a mudança de 73 para 74 mortes violentas. A recontagem de `F3-ggb/dados/codificacao_A.csv` confirma **160 → 106 → 88 → 74 → 50**, com **36** motivos desconhecidos. Os valores desenhados nas figuras também conferem.
- **Correção proposta:** substituir a frase por uma síntese da adjudicação, informando que ela alterou uma confirmação de morte violenta, preservou os 50 casos verificáveis e manteve o κ entre os codificadores originais. Preservar a ressalva de que Wilson não incorpora erro de classificação.

### AST-N02 — A descrição dos cenários do painel pela internet não coincide inteiramente com a tabela e o CSV

- **Local:** PDF, p. 163, nota da Tabela K2; `research-2026-10-21-rodada3/F2-custos/opcoes_por_modo.csv` e `cenarios_custo.py`.
- **Trecho literal curto:** “por isso só aparece com a fração de autopreenchimento”.
- **Problema:** a tabela também apresenta o painel com **1,89%, todos os modos**; o CSV acrescenta uma terceira linha, **com entrevistador**, omitida do PDF sem explicação explícita.
- **Evidência verificável:** a K2 tem duas linhas do painel, enquanto o CSV tem três. A linha adicional usa 1,35%, 1.544 LGB+ e aumento detectável de 60,9%. As linhas efetivamente publicadas conferem numericamente.
- **Correção proposta:** escrever “além do cenário de referência, apresenta-se apenas o cenário de autopreenchimento” e identificar no arquivo derivado a linha com entrevistador como cenário hipotético não utilizado, ou excluí-la da saída destinada à K2.

### AST-N03 — Processo e metadados prometem hashes para todas as fontes

- **Local:** `docs/processo-e-custo.md:74`; descrições de `CITATION.cff`, `codemeta.json` e `.zenodo.json`.
- **Trecho literal curto:** “URL, data e SHA-256 de cada fonte”.
- **Problema:** a promessa é mais ampla que o manifesto entregue.
- **Evidência verificável:** `manifest/MANIFESTO-FONTES.csv` contém **1.139 registros**, todos com data de acesso, mas apenas **554** com `sha256` preenchido; **585** não têm hash. O próprio PDF, p. 167, usa a formulação correta: hash “quando o arquivo foi salvo”.
- **Correção proposta:** harmonizar esses arquivos com o PDF: “URL, data de acesso e, quando houve arquivo salvo, SHA-256”. Não é necessário produzir hashes retrospectivos das fontes não arquivadas.

### AST-N04 — A documentação de reprodução conserva informações anteriores à montagem atual

- **Local:** `REPRODUCIBILITY.md:8–12,38`; `scripts/reproduzir.py`, lista `PASSOS`.
- **Trecho literal curto:** “Todo número publicado […] é recalculado”; “31/10/2026”; “28”.
- **Problema:** a abertura promete recálculo universal, embora parte dos números seja apenas conferida por testes; a data da execução mais recente e o número de passos também estão desatualizados.
- **Evidência verificável:** o manifesto distribuído é de **2026-11-01**; `PASSOS` contém **29 entradas** e não inclui `F2-custos/cenarios_custo.py`, responsável pela nova K2. O PDF, p. 166, distingue corretamente etapas recalculadas e dimensionamento conferido por teste.
- **Correção proposta:** adotar a descrição delimitada do PDF, atualizar a data e os 29 passos e indicar expressamente como as novas análises são verificadas. Não é necessário ampliar o recálculo para corrigir a documentação.

**Depois do DOI:** inserir o identificador em README, CITATION, codemeta, CHANGELOG e artigo, incluindo a referência de Flores e a disponibilidade de dados; refazer PDF/DOCX, atualizar hashes e selo quando aplicável e conferir o pacote antes da release final. Os ajustes não bloqueantes podem acompanhar essa remontagem, embora seja preferível incorporá-los antes da rc1, cujo PDF já será depositado.

## O que está bom

- Selo dos **781 arquivos**, seis hashes de `paper/PAPER-SHA256.txt` e entradas existentes de `paper/v05/SHA256SUMS.txt` conferem.
- **49 testes numéricos aprovados**, incluindo os **12 da v0.5**; recontagem independente do GGB consistente.
- Todos os destinos do mapa de apêndices existem; nenhuma chamada singular a tabela ou figura inexistente foi encontrada.
- Lista única com **105 referências**, idêntica entre manuscrito e `referencias.md`; sem citação órfã demonstrada na conferência.
- Autor, afiliação, licenças e versão **1.0.0** estão alinhados; a distinção entre versão do texto e do repositório está explícita.