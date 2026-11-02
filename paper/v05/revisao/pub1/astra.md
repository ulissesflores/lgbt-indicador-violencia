# Parecer de pré-publicação — GPT-6 Astra (gpt-6-astra)

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | **não pronto** | Há contradição sobre a documentação consultada no Apêndice H e indicação desatualizada do texto-fonte. |
| 2. Repositório atualizado | **não** | Os arquivos finais estão presentes e íntegros, mas metadados, apresentação e parte da documentação continuam em versões anteriores; o lint obrigatório falha. |
| 3. DOI | **pode depois de corrigir os bloqueantes** | Corrigir AST-P01 a AST-P04 antes da rc1; a ausência atual do DOI é compatível com o fluxo informado. |

Auditoria exclusivamente local, sem internet e sem alteração de arquivos. Conferi a extração das 163 páginas, com inspeção visual de 11 páginas, os hashes, os metadados e os arquivos citados abaixo. Foram **94 testes aprovados e 3 pulados**, nos conjuntos executados. Não reexecutei a reprodução completa nem os microdados. Inspeção visual integral, validação externa das fontes, publicação efetiva no GitHub, releases existentes e ligação ao Zenodo: **não verificado**.

**Antes da rc1:** corrigir os quatro bloqueantes, atualizar os selos afetados e repetir as verificações. **Depois da emissão do DOI:** inserir o identificador nos arquivos previstos, inclusive na referência de Flores e na disponibilidade de dados; refazer PDF/DOCX, atualizar seus hashes e preparar a release final. Os ajustes não bloqueantes podem acompanhar essa remontagem, antes da versão final. O vínculo entre o DOI utilizado e a versão efetivamente depositada deverá ser conferido nessa etapa.

## Bloqueantes

### AST-P01 — O Apêndice H contradiz o próprio estado da evidência

- **Local:** PDF, pp. 144, 146–147; `paper/v05/MATERIAL-COMPLEMENTAR.md:1118`.
- **Trechos literais:** “sem instrumento normativo lido”; posteriormente, “O texto suspende por 180 dias o edital inteiro” e “acolhida em decisão liminar”.
- **Problema:** primeiro o artigo declara que a classificação depende da imprensa, sem leitura do instrumento; depois descreve o conteúdo da portaria e uma decisão judicial, sem identificar a fonte dessa verificação. A remissão ao próprio Apêndice H é circular.
- **Evidência verificável:** a Tabela H1 mantém a ressalva de que as fontes são de imprensa. Em `research-2026-10-21-rodada3/escrutinio/simetria/eventos_C18.csv`, o episódio **E20** está classificado como `imprensa`, com URL `https://gcn.ie/?p=94458`. A lista única de referências não contém a Portaria nº 1.576/2019 nem a decisão mencionada. Não localizei documentação identificável desses dois atos no acervo pesquisado; seus teores permanecem **não verificados** nesta auditoria.
- **Correção proposta:** identificar e referenciar a portaria e a decisão, registrando a consulta posterior e atualizando a ressalva anterior. Se o conhecimento veio apenas de reportagem, atribuir expressamente as informações a ela. Isso não exige reabrir o julgamento de mérito sobre o episódio.

### AST-P02 — A identidade da versão a depositar está contraditória

- **Local:** PDF, pp. 49 e 54; `CITATION.cff:23–24`; `codemeta.json`; `.zenodo.json:4–6`; `pyproject.toml`; `README.md:395`; `scripts/auditar_publicacao.py:290–337`.
- **Trechos literais:** PDF: “versão 1.0.0”; metadados: `version: 0.1.0`; Zenodo: `"access_right": "closed"`.
- **Problema:** o artigo identifica um depósito 1.0.0, enquanto os metadados que o acompanharão descrevem 0.1.0. O CFF conserva a data de 23 de outubro. A configuração fechada é compreensível durante a preparação, mas precisa ser alterada no pacote que disparará o depósito público.
- **Evidência verificável:** os quatro arquivos de metadados concordam entre si em **0.1.0**, mas divergem da referência de Flores no PDF. Além disso, `check_release()` exige versão iniciada por `0.` e acesso `closed` mesmo quando recebe `final=True`; portanto, seu resultado não valida o fluxo final proposto.
- **Correção proposta:** fixar a versão da rc1 e a versão final, sincronizando metadados, citação, datas e documentação. Preparar `access_right: open` para a release autorizada. Ajustar o verificador para distinguir preparação, rc1 e final. **Não preencher DOI fictício.**

### AST-P03 — A verificação obrigatória de código já reprova localmente

- **Local:** `.github/workflows/verify.yml`, job `lint`; `make_provenance.py:60`; `scripts/registra_run.py`.
- **Trechos literais:** `args: check`; `args: format --check`; resultado: `Found 12 errors.`
- **Problema:** o workflow publicado contém uma etapa obrigatória que falha no estado atual, independentemente dos resultados científicos.
- **Evidência verificável:** executei, sem cache nem correções:
  - `python3.14 -B -m ruff check --no-cache --output-format concise`: **12 erros**, sendo 11 de comprimento de linha e um `UP017`.
  - `python3.14 -B -m ruff format --check --no-cache`: reprova `scripts/registra_run.py`.
  
  Ambos retornaram código **1**. O job `lint` não está marcado como informativo; essa exceção pertence apenas a `lint-pesquisa`.
- **Correção proposta:** corrigir a formatação e o uso de `timezone.utc` apontados, repetir os comandos e regenerar o selo, pois esses arquivos integram a cadeia.

### AST-P04 — Os pontos de entrada ainda encaminham ao artigo anterior

- **Local:** `README.md:31,264,270,376`; `REPRODUCIBILITY.md`, seção “Artigo”; PDF, Tabela M1, pp. 162–163; `CHANGELOG.md:34–38`.
- **Trechos literais:** “Artigo (versão 0.4.4)”; “versão 0.5 (em preparação; não lançada)”; “Texto-fonte do artigo […] `paper/paper.md`”.
- **Problema:** o leitor que segue a apresentação principal ou a tabela de rastreabilidade do próprio PDF chega ao texto anterior. O repositório contém a versão final nova, mas ainda não a apresenta consistentemente como produto corrente.
- **Evidência verificável:**
  - `docs/paper/paper-final.pdf` existe e tem **163 páginas**.
  - `paper/paper.md` e `paper/build/v04/paper-v04.pdf` são os artefatos anteriores, mantidos separadamente.
  - A Tabela M1 não identifica `paper/v05/MANUSCRITO.md`, `MATERIAL-COMPLEMENTAR.md`, as figuras novas e `paper/v05/revisao/` como os componentes atuais.
  - O CHANGELOG registra um PDF de **169 páginas** em `paper/build/v05/paper-v05.pdf`, caminho ausente nesta distribuição, sem esclarecer ali que esse artefato foi substituído.
- **Correção proposta:** atualizar apresentação, instrução de citação, matriz de reprodução e Tabela M1 para os caminhos atuais. Preservar o histórico, identificando explicitamente os artefatos anteriores e os intermediários substituídos.

## Não bloqueantes

### AST-N01 — As remissões históricas funcionam por uma tabela de tradução, mas prejudicam a leitura final

- **Local:** PDF, pp. 68–71, 91–92, 148, 151 e 161–163.
- **Trechos literais:** “A seção 3.2 apresenta o veredito”; “dimensionamento da seção 3.13”.
- **Problema:** esses números pertencem à v0.4.4. No artigo atual, 3.2 trata de registros e não existe seção 3.13.
- **Evidência verificável:** a Tabela B1 e sua nota **declaram expressamente** essa convenção e permitem recuperar os destinos. Por isso, não trato todas essas remissões como referências irrecuperáveis. Entretanto, o leitor precisa traduzir números antigos durante a leitura.
- **Correção proposta:** substituir as remissões correntes pelos apêndices ou seções atuais: por exemplo, mortalidade internacional → seção 3.4/Apêndice E; dimensionamento → seção 6/Apêndice K. Conservar a tabela histórica apenas para rastrear versões anteriores.

### AST-N02 — A cobertura dos testes é menor que a formulação das promessas

- **Local:** PDF, pp. 12 e 161–162; `paper/v05/README.md`; `tests/test_numeros_v05.py`; `paper/tests/test_figuras.py`; `scripts/auditar_publicacao.py`.
- **Trechos literais:** “um programa conferiu cada número e cada citação”; “trava os números novos da v0.5”.
- **Problema:** o acervo comprova verificações relevantes, mas não uma trava automática integral do PDF atual.
- **Evidência verificável:** os **oito testes** de `test_numeros_v05.py` passaram; cobrem LiHS, variações federais, indeterminadas e coabitação. Não leem o PDF e não travam os demais resultados novos por agressor. Os testes de figuras executados conferem a infraestrutura legada; o auditor de referências continua acionando, por padrão, `paper/paper.md`.
- **Correção proposta:** delimitar precisamente a cobertura publicada e apontar a auditoria para a versão atual. Se mantida a promessa abrangente, acrescentar verificações dos resultados e figuras novos. O cumprimento histórico de “cada número e cada citação” permanece **não verificado**.

### AST-N03 — As fontes estrangeiras dos custos não chegaram à bibliografia do artigo

- **Local:** PDF, Tabelas 6 e K1, pp. 48 e 158.
- **Trecho literal:** “é a referência de um contrato estrangeiro convertida pelo câmbio de 20 de outubro de 2026”.
- **Problema:** as notas citam instituições brasileiras, mas não identificam o contrato estrangeiro nem a fonte cambial que sustentam os R$ 42 milhões.
- **Evidência verificável:** `research-2026-10-21-rodada3/F2-custos/custos-fontes.csv`, registro **C29**, identifica o contrato do *Gambling Survey for Great Britain*, de £4,5 milhões. `cenarios_custo.py` utiliza esse contrato e arquivos PTAX. Essas fontes não aparecem como entradas correspondentes em `paper/v05/referencias.md`.
- **Correção proposta:** acrescentar as referências do contrato e do câmbio e citá-las nas notas pertinentes. A rastreabilidade existe no repositório; falta completá-la no artigo.

### AST-N04 — O texto promete números de três coortes que o apêndice não apresenta

- **Local:** PDF, p. 30 e Apêndice E, pp. 95–105.
- **Trecho literal:** “Os números dessas coortes estão no Apêndice E.”
- **Problema:** a promessa não corresponde ao conteúdo.
- **Evidência verificável:** o Apêndice E menciona Saxby, Hsu e Clark na p. 99, mas não apresenta suas estimativas numéricas. A Tabela E1 também não contém essas três coortes.
- **Correção proposta:** trocar por “Essas coortes são discutidas no Apêndice E” ou acrescentar as estimativas, com população, medida e intervalo.

### AST-N05 — Um p-valor foi publicado como zero por arredondamento

- **Local:** PDF, Tabela G7, p. 139; `paper/v05/MATERIAL-COMPLEMENTAR.md:994`.
- **Trecho literal:** linha “bloco: envolve centro”, mulheres: `0,000`.
- **Problema:** a apresentação transforma um valor pequeno em zero; em APA, a forma adequada aqui é uma desigualdade.
- **Evidência verificável:** em `dados/exposicao/c10_e2_resumo.csv`, recorte `P_todas_67`, direção `bloco: envolve centro`, grupo `mulheres`, consta `p_mediana = 0.0002`.
- **Correção proposta:** publicar **p < 0,001**, preservando o valor completo no CSV.

### AST-N06 — Há ajustes pontuais de identificação de autores e siglas em APA

- **Local:** PDF, pp. 27, 30, 51, 149–150 e 160.
- **Trechos literais:** “Clark & Blosnich, 2024”; “Clark et al., 2026”; “OSCE/ODIHR, 2025”.
- **Problema:** há primeiros autores distintos chamados Clark; as iniciais permitem distingui-los. Nos apêndices, OSCE e OSCE/ODIHR não são apresentados de maneira consistente com os nomes usados na lista única.
- **Evidência verificável:** as referências identificam **Clark, K. A.** e **Clark, K. D.**; o documento de 2025 está sob **Office for Democratic Institutions and Human Rights**, já citado como ODIHR no corpo.
- **Correção proposta:** distinguir os Clark pelas iniciais nas citações e padronizar ODIHR; introduzir formalmente OSCE quando necessário. Não faltam essas obras na bibliografia.

### AST-N07 — O comentário do arquivo de hashes informa uma contagem antiga

- **Local:** `paper/PAPER-SHA256.txt:9`; `output/hash-chain.md`; `output/provenance.json`; `runs/20261031T221125Z/manifest.json`.
- **Trecho literal:** “767 arquivos”.
- **Problema:** a contagem do comentário diverge do selo que ele próprio identifica.
- **Evidência verificável:** `make_provenance.py --verify` confirmou a cadeia `2aac3f60…163ced9` com **768 arquivos**; o manifesto da execução também informa 768. Os hashes dos artefatos conferem.
- **Correção proposta:** corrigir somente a contagem documental. Não há evidência de corrupção do conjunto.

### AST-N08 — Restaram marcas editoriais internas fora dos documentos históricos

- **Local:** PDF, pp. 11–12 e 83; `paper/v05/README.md`.
- **Trechos literais:** “A reescrita deste texto (versão 0.5)”; “Reprodução de seguro_pns2019.md […] divergências = 0”; “nota da Tabela MC5.C1”.
- **Problema:** são resíduos de apresentação do processo, sem impacto demonstrado nos resultados. O último rótulo já deveria acompanhar a conversão.
- **Evidência verificável:** `paper/v05/mapa-apendices.json` converte `Tabela|MC5.C1` em **F4**. Não encontrei rótulos MC remanescentes no texto extraído do PDF.
- **Correção proposta:** atualizar o README para Tabela F4 e, no PDF, converter a saída operacional em nota metodológica legível. Preservar os rótulos antigos nos pareceres históricos e no mapa.

## O que está bom

- **Integridade confirmada:** cadeia de 768 arquivos, hashes do PDF/DOCX/fontes, hashes de `paper/v05/` e checksums da execução conferem.
- **Resultados conferidos sem divergências:** 94 testes aprovados; os três pulados foram contabilizados separadamente.
- **Apêndices completos:** B a M presentes; todos os destinos do mapa de tabelas e figuras existem, sem rótulos MC no texto do PDF.
- **Bibliografia consolidada:** 101 entradas, idênticas entre `referencias.md` e o manuscrito; todas têm chamada no corpo ou nos apêndices. Antunes e Martins estão corretamente tratados como citações secundárias.
- **Autoria e apresentação consistentes:** nome, ORCID, afiliação e divisão de licenças concordam; PDF com fontes incorporadas e sem cortes aparentes nas páginas inspecionadas.