# Parecer de pré-publicação — GPT-6 Astra (gpt-6-astra)

Auditoria local, sem internet e sem alteração de arquivos. PDF conferido: **166 páginas**, SHA-256 `0247ec1f2bc782fb29c6044de66b96e6924c1f5d6150ef99822f7c9fb0bf0b67`. Examinei o texto integral e inspecionei visualmente cinco páginas. Executei **94 testes: todos passaram**, com outros **três pulados**, contabilizados separadamente.

Reprodução completa dos microdados, inspeção visual de todas as páginas, execução do validador externo da casa, situação pública do GitHub e integração com o Zenodo: **não verificado**. Os totais declarados de 185 testes e 122 verificações não foram integralmente reexecutados.

## Conferência

Cada ID aparece uma vez. Nos IDs que combinam alegações procedentes e improcedentes, explicito a decisão sobre ambas.

| ID original | Situação | Por quê | Evidência |
|---|---|---|---|
| AST-P01 | resolvida | O texto distingue classificação pela imprensa e leitura posterior da portaria; acrescentou referência e eliminou a autorremissão. | PDF, pp. 59, 145, 147–148. |
| AST-P02 | resolvida em parte | Versões e datas foram alinhadas; o auditor ainda não implementa uma verificação efetiva da fase final. | `CITATION.cff`, `codemeta.json`, `.zenodo.json`, `pyproject.toml`; `scripts/auditar_publicacao.py`, função `check_release`. |
| AST-P03 | resolvida | Ruff passou sem erros; a verificação de formatação também passou. | `ruff check --no-cache`; `ruff format --check --no-cache`: 13 arquivos formatados. |
| AST-P04 | resolvida em parte | Os pontos de entrada agora identificam a v0.5; resta uma indicação de seção incorreta na Tabela M1. | `README.md:31`; `REPRODUCIBILITY.md:153`; PDF, p. 165. |
| AST-N01 | resolvida em parte | Algumas remissões foram corrigidas, mas a Tabela B2 e outras passagens ainda usam destinos antigos ou errados. | PDF, pp. 72, 77, 93, 102 e 165. |
| AST-N02 | resolvida | O README da v0.5 agora delimita os quatro conjuntos de números cobertos pelo teste específico. | `paper/v05/README.md:5`; `tests/test_numeros_v05.py`, oito testes aprovados. |
| AST-N03 | resolvida | Contrato britânico e câmbio receberam referências e chamadas nas duas tabelas. | PDF, pp. 48, 50, 55 e 160. |
| AST-N04 | resolvida | A promessa de apresentar números foi substituída por uma descrição compatível com o apêndice. | PDF, p. 30: “Essas coortes são descritas”; p. 100. |
| AST-N05 | resolvida | A célula passou a apresentar `< 0,001`, compatível com o valor preservado no CSV. | PDF, p. 140; `dados/exposicao/c10_e2_resumo.csv`. |
| AST-N06 | resolvida | Os dois Clark foram distinguidos pelas iniciais; ODIHR e OSCE foram identificados e padronizados. | PDF, pp. 27, 30, 43, 96, 100, 150 e 162. |
| AST-N07 | resolvida | Comentário, cadeia e manifesto concordam em 772 arquivos. | `paper/PAPER-SHA256.txt`; `output/provenance.json`; `runs/20261031T233520Z/manifest.json`. |
| AST-N08 | resolvida em parte | As frases operacionais e o rótulo MC5.C1 foram corrigidos; ainda há abreviações de saída técnica no Apêndice C. | PDF, pp. 81–85; `paper/v05/README.md`. |
| GRO-P01 | resolvida em parte | Metadados e apresentação principal foram atualizados; persistem resíduos documentais identificados abaixo. | Quatro metadados; `README.md:79`; PDF, p. 165. |
| GRO-P02 | resolvida | O caminho público da LiHS foi corrigido; o PDF de 169 páginas está explicitamente identificado como rascunho substituído e não distribuído. | `README.md:280`; `paper/v05/README.md`; `CHANGELOG.md`, “Adicionado (PDF em APA 7, pré-DOI)”. |
| GRO-P03 | não resolvida | O único manifesto distribuído ainda registra o commit antigo e árvore suja. | `runs/20261031T233520Z/manifest.json`: `0601c65…`, `working_tree_dirty: true`. |
| GRO-N01 | resolvida | A contradição documental do Apêndice H foi conciliada. | PDF, pp. 145, 147–148; referência na p. 59. |
| GRO-N02 | resolvida em parte | O veredito remete corretamente ao Apêndice E; o controle positivo agora aponta para 3.4, embora esteja em 3.3. | PDF, pp. 71 e 102; seção 3.3, pp. 26–27. |
| GRO-N03 | resolvida | A contagem documental corresponde à cadeia atual, efetivamente verificada. | `paper/PAPER-SHA256.txt`; `output/hash-chain.md`. |
| GRO-N04 | resolvida em parte | O alcance dos testes foi delimitado e o destaque do README corrigido; a tabela “Em resumo” mantém os números antigos. | `paper/v05/README.md`; `README.md:21,79`. |
| GRO-N05 | resolvida | A afirmação sobre TGEU foi atribuída expressamente à reprodução jornalística, com referência correspondente. | PDF, pp. 50 e 120. |
| GRO-N06 | resolvida | O README agora usa Tabela F4. | `paper/v05/README.md`, item “Planilha da LiHS”. |
| ARG-P01 | resolvida | A frase das coortes foi corrigida; aceita-se a não procedência da alegação de quadro órfão, pois ele está apresentado como Tabela 2. | PDF, pp. 13–15 e 30; `paper/v05/QUADRO-E2.md`. |
| ARG-P02 | resolvida em parte | A Tabela M1 recebeu fontes, análises e revisões da v0.5; resta o destino incorreto da busca de atos de governo. | PDF, pp. 164–166, especialmente p. 165. |
| ARG-P03 | resolvida | O Apêndice H esclarece a origem da classificação e a leitura posterior do instrumento. | PDF, pp. 145–148. |
| ARG-P04 | não procedência aceita | A remissão contém a letra B; não há o vazio alegado. | PDF, p. 46. |
| ARG-N01 | resolvida | O Apêndice D passou a informar explicitamente as 39 denúncias sob a regra estrita. | PDF, p. 94. |
| ARG-N02 | resolvida em parte | A localização dos arquivos melhorou, mas permanecem remissões incompatíveis com a estrutura atual. | PDF, pp. 72, 77, 93, 102 e 165. |
| ARG-N03 | resolvida em parte | Os resíduos mais evidentes foram removidos; `het` ainda aparece em cabeçalhos e células. | PDF, pp. 81–85. |
| ARG-N04 | resolvida | As expressões e autorias foram corrigidas; aceitam-se as não procedências relativas ao intervalo e à URL da lei. | PDF, pp. 20, 39, 51, 64, 150 e 162. |
| ARG-N05 | resolvida | A identidade da versão foi alinhada; aceita-se a não procedência sobre o arquivo de horas, que contém dois carimbos completos. | Quatro metadados; `research-2026-10-21-rodada3/escrutinio/simetria/ADENDO-2.hora.txt`. |

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | **pronto com ressalvas** | Não encontrei nova divergência numérica demonstrada; persistem remissões erradas e pequenos resíduos editoriais. |
| 2. Repositório atualizado | **com ressalvas** | Artefatos e hashes conferem, mas restam uma tabela desatualizada, o auditor final incompleto e a evidência de commit pendente. |
| 3. DOI | **pode depois de corrigir os bloqueantes** | Falta demonstrar que a rc1 será criada sobre o commit completo e verificado, conforme o próprio fluxo acordado. |

A numeração abaixo é desta rodada; os IDs anteriores estão preservados na Conferência.

## Bloqueantes

### AST-P01 — Falta concluir a vinculação do pacote ao commit publicável  
*Remanescente de GRO-P03; pendência operacional já reconhecida pelo autor.*

- **Local:** `runs/20261031T233520Z/manifest.json`; `REPRODUCIBILITY.md:24`.
- **Trecho literal curto:** `"commit": "0601c65e13280dcc6c82c5468997930517dedad0"`; `"working_tree_dirty": true`.
- **Problema:** o selo confirma os arquivos desta cópia, mas o manifesto ainda não demonstra que esse conteúdo está integralmente no commit que receberá a tag. A documentação informa que o commit citado não contém o artigo.
- **Evidência verificável:** a cadeia `170b0718…486806f` confere em **772 arquivos**; o único manifesto distribuído associa essa cadeia à árvore suja. Esta cópia não contém `.git`; eventual commit posterior é **não verificado**.
- **Correção proposta:** concluir o commit do pacote completo, verificar o selo e os hashes sobre a árvore commitada e assegurar que `v1.0.0-rc1` aponta para essa árvore. No pacote autorizado da rc1, aplicar também a mudança já prevista de `access_right` para `open`. O `closed` atual é coerente com a preparação e não constitui, sozinho, erro editorial.

## Não bloqueantes

### AST-N01 — A atualização das remissões ficou incompleta

- **Local:** PDF, pp. 72, 77, 93, 102 e 165; `paper/v05/MATERIAL-COMPLEMENTAR.md`.
- **Trecho literal curto:** “As seções 3.11 a 3.13 trazem resultados de contexto”.
- **Problema:** a Tabela B2 continua usando a estrutura anterior, apesar de a nota da Tabela B1 afirmar que as remissões foram atualizadas. Outros ponteiros também levam ao assunto errado.
- **Evidência verificável:** na p. 72, GGB aponta para 3.4, registros para 3.5 e Parlamento para 3.10; atualmente estão em 3.5, 3.2 e 3.7. Não existem seções 3.8 a 3.13. Na p. 93, a equação remete a 2.5, mas está em 2.3.
- **Correção proposta:** atualizar a coluna inteira da B2: mortalidade → 3.3–3.4/E; GGB → 3.5/F; registros → 3.2/D; governos → 3.6/G; atos e regimes → 3.7/H–I; Parlamento → 3.7/J. Na nota, usar Apêndices L e K. Corrigir também Cuba → Apêndice I, na p. 77; controle positivo → 3.3, na p. 102; busca de atos → 3.7/Apêndice H, na M1.

### AST-N02 — A tabela-resumo do README conserva os percentuais antigos

- **Local:** `README.md:79`.
- **Trecho literal curto:** “LGBTfobia em 0,5% […] 42-44% das interpessoais”.
- **Problema:** a correção foi aplicada ao destaque inicial, mas não à segunda apresentação do mesmo resultado.
- **Evidência verificável:** `README.md:21` e PDF, pp. 25 e 90, informam **0,4% a 0,5%** e **42,5% a 44,5%**, no universo de notificações não marcadas como autoprovocadas.
- **Correção proposta:** repetir esses intervalos e essa definição do universo na linha “O Sinan resolve?”.

### AST-N03 — Restam abreviações técnicas sem explicação nas tabelas da PNS

- **Local:** PDF, pp. 81–85; `paper/v05/MATERIAL-COMPLEMENTAR.md:159,172,214,228,273`.
- **Trecho literal curto:** “RP LGB+/het”; “n het = 3112”; “Diferença LGB+ − het”.
- **Problema:** o acabamento prometido não alcançou todos os cabeçalhos e células. É um problema de apresentação, sem alteração demonstrada dos números.
- **Evidência verificável:** as Tabelas C1, C2, C4 e C6 ainda usam `het`, enquanto outras tabelas escrevem “heterossexuais”.
- **Correção proposta:** escrever o termo por extenso ou definir uma abreviação uniforme nas notas.

### AST-N04 — O modo final do auditor não verifica a fase final

- **Local:** `scripts/auditar_publicacao.py`, função `check_release`, a partir da linha 290.
- **Trecho literal curto:** `True para --stage final (exige URL pública, release e DOI)`.
- **Problema:** essa exigência documentada não foi implementada. O argumento `final` apenas altera o rótulo da mensagem; a função continua rejeitando DOI próprio no CFF e aceitando acesso fechado.
- **Evidência verificável:** a condição que acusa “CITATION.cff traz DOI próprio antes do release” é incondicional; `final` só participa de `etapa = "final" if final else "pré-release"`. A execução atual terminou como **NÃO EXERCIDO**, não como validação final.
- **Correção proposta:** separar os critérios de preparação e finalização. Na fase final, conferir DOI presente e consistente, acesso aberto e identidade da versão; verificações externas indisponíveis devem continuar explicitamente não exercidas. Pode ser concluído depois da emissão do DOI, antes da release final.

**Depois do DOI:** os ajustes não bloqueantes podem acompanhar a remontagem já prevista. Inserir o identificador nos arquivos exigidos pelo fluxo, inclusive na referência de Flores e na disponibilidade de dados; refazer PDF/DOCX, atualizar os hashes e verificar o pacote antes de `v1.0.0`. Recomendo aproveitar a preparação da rc1 para corrigir também as remissões, pois seu PDF já integrará o primeiro depósito.

## O que está bom

- Selo dos **772 arquivos**, hashes do artigo, somas da pasta v0.5 e checksums da execução conferem.
- **94 testes aprovados**, três pulados por ausência das origens privadas; Ruff limpo.
- Crivo do DOCX/PDF: **zero violações de forma e zero pendências de conteúdo** dentro do alcance desse programa.
- Apêndices e destinos do mapa existem; não encontrei chamadas a tabelas ou figuras inexistentes na varredura dos rótulos.
- Lista única com **105 referências**, concordante com o manuscrito; as novas fontes e a conciliação do Apêndice H foram incorporadas.