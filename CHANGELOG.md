# Changelog

Formato: Keep a Changelog; versionamento semântico. Versão `0.x` até o DOI: nenhum release do GitHub antes do aval do autor.

## [Não lançado] - v0.3 (2026-10-24) e commit inicial público (2026-10-25)

### Alterado (commit inicial público, frente R0)
- O repositório vem primeiro e o artigo deriva dele: o selo (`make_provenance.py`) deixa de cobrir `paper/paper.md`, `paper/AUDIT.md`, `paper/build/`,
  `paper/tools/`, `paper/tests/test_anexo.py` e `paper/PAPER-SHA256.txt` (regra única `make_provenance.excluido()`, usada também pelo inventário,
  pelos testes de privacidade e pelo auditor). O primeiro commit público não contém o artigo; ele entra depois, citando a URL e o `chain_hash`, com o
  sha256 do PDF final em `paper/PAPER-SHA256.txt`. As figuras e os testes de figura ficam no selo.
- `scripts/auditar_publicacao.py --check literatura`: a conferência artigo x ledger sai "NÃO EXERCIDA" enquanto o artigo não está no repositório.
- `tests/test_integridade.py`: percorre o mesmo conjunto do selo; o teste do interior do DOCX do artigo saiu (volta com o artigo).
- README, `REPRODUCIBILITY.md`, `CITATION.cff`, `codemeta.json` e `.zenodo.json` não descrevem mais o artigo como parte do conjunto; o artigo e o hash do PDF
  não aparecem como entrega deste commit.
- Selo regravado uma vez com a nova regra; histórico do git passa a ser o registro de mudanças (`manifest/MODIFICACOES.tsv` fica só com a sincronização inicial; as 12 linhas de arquivos do artigo saem junto com ele e voltam no commit do artigo).

### Adicionado
- `dados/presidencia/` (C09, troca de presidente) e `dados/exposicao/` (C10, exposição por governo sem atribuição de causa): pré-registros com
  hash do corpo, scripts, saídas, relatórios; testes em `tests/test_c09_presidencia.py` e `tests/test_c10_exposicao.py`; os 5 scripts entram
  no recálculo de `scripts/reproduzir.py` (28 passos).
- Ledgers `research-2026-10-21-rodada3/A-textointegral/sources.jsonl` (antes só na árvore privada) e `research-2026-10-24-v03/L-ledger/sources.jsonl`
  (literatura de mortalidade da v0.3); `A-textointegral/verificacao-metadados.csv` (139 conferências de texto integral: periódico, quartil,
  texto lido, veredito; sem trecho de terceiros).
- `scripts/inventario_publico.py` -> `manifest/INVENTARIO-PUBLICO.{md,json}`: fontes, idiomas, tipos e scripts contados só com os arquivos
  distribuídos; com os 17 ledgers do painel reproduz 829 / 10 / tipos.
- `scripts/auditar_publicacao.py` (`--check literatura|inventario|privacidade|release`; 0 ok, 1 falhou, 2 não exercido) e
  `tests/test_auditar_publicacao.py` (com controles negativos).
- `REPRODUCIBILITY.md`: matriz de reprodução (recalcula, só confere, não se refaz) e o que o hash prova e não prova.

### Adicionado (frente P3, 2026-10-24)
- `dados/disque100/`: Disque 100 (23 arquivos públicos, 2011 a setembro de 2026): catálogo com sha256, pré-registro com hash gravado antes das contagens
  (2 adendos), dicionário, séries e comparações (CSV), scripts e 63 testes em arquivos sintéticos; **sem os microdados** (14 GB; `raw/` ignorado pelo git).
  `scripts/reproduzir.py` ganhou o passo `d100_series.py` (29 passos); `pyproject.toml` inclui `dados/disque100/tests` no pytest (173 testes; `run_all.py`: 110).
  Nenhuma conclusão depende dele: não há chave de pessoa, o total de vítimas únicas não é calculável, a série tem quatro quebras.
- Figura do Disque 100 (`paper/figures/fig28_disque100_serie.*`, teste com controle negativo): módulo LGBT por ano com a unidade e as quebras, e canal inteiro.
  A figura de revisores hostis passa a ser a de número 28 na numeração dos arquivos.

### Alterado
- Correções do escrutínio externo (frente R, registradas como `v0.3-R` em `manifest/MODIFICACOES.tsv`): 1.554 LGB+ observados, 305.955
  adultos, série do Sinan sem duplicação do total, 59 variáveis do formulário x 87 campos do arquivo do SIM, PNS sem pergunta de identidade
  de gênero (N2 = cenário), intervalo por inversão do wild-cluster (R6), Parlamento 0/49 e 1/49 (R7).
- `manifest/MANIFESTO-FONTES.csv` cobre os 18 ledgers (antes só o consolidado e a rodada 3).
- `pyproject.toml`: lint em dois níveis (estrito no código de infraestrutura, informativo nos scripts de pesquisa copiados); CI com matriz
  3.12/3.13, lint estrito bloqueante e auditoria; o passo de diagnóstico com `|| true` saiu (o `run_all.py` já lista as divergências).
- `run_all.py --selar` regrava também o inventário público.
- `make_provenance.py`: o selo usa o mesmo conjunto do `.gitignore` (fora: cópias de figura que o build regrava em `paper/build/fig-embed/`,
  `.DS_Store` em qualquer pasta e o envelope cru da rodada v2-1 do juiz); antes o `--verify` falharia num clone limpo.
- README: seção da v0.3, fontes em linguagem comum, índice do que está exibido.
## [0.1.0] - 2026-10-23

### Adicionado
- Dados derivados, scripts e saídas de `dados/`, `simulacao/` e `research-2026-10-21-rodada3/` (frentes F2, F3, F5, F6, F8, GGB-completo, ideologia, discurso).
- Ledgers de fontes (`research-consolidado/sources.jsonl`, 571 registros) e `manifest/MANIFESTO-FONTES.csv` (URL, data de acesso, SHA-256).
- `run_all.py` (integridade -> réplica -> testes -> selo), `make_provenance.py`, `scripts/reproduzir.py`, `scripts/acquire_{sim,sinan,pns2019,tse}.py`.
- `tests/`: números publicados, integridade/privacidade e verificação independente.
- Pré-registros com hash em `docs/PRE-REGISTROS/`; dossiês e laudos em `docs/`.
- CITATION.cff, codemeta.json, .zenodo.json (`access_right: closed`, sem DOI).
- `paper/`: figuras com testes de figura (o artigo, o PDF, o DOCX e as ferramentas de export entram depois, fora do selo).
- Reanálises pré-registradas C02, C03, C05 e C08 (`dados/painel/`, `dados/pns/`, `dados/ggb/`) e `tests/test_reanalises_publicadas.py`;
  C02 e C03 entram no recálculo de `scripts/reproduzir.py`.
- `research-2026-10-21-rodada3/escrutinio/`: pacote enviado, as quatro revisões hostis, triagem, critérios e resultados das reanálises, busca simétrica.
- `dashboard/`: números do painel de contagens (extrato público) e o script de contagem (ferramenta do autor).
- Dossiês atualizados (consolidado e parte 2 com a simetria e as reanálises integradas).

### Alterado
- `scripts/reproduzir.py`: número impresso em precisão total (>= 15 algarismos) aceita diferença relativa <= 1e-10 (soma em BLAS multithread varia entre execuções).
- Linguagem interna de operação (nomes de agentes e ferramentas, números de pedido, papéis) trocada por termos neutros em 50 arquivos, sem alterar números;
  cada arquivo em `manifest/MODIFICACOES.tsv` com sha256 antes e depois. Exceção: pré-registros com hash gravado ficam intactos (ver `docs/INDEX.md`).
- `tests/`: `pytest` e `run_all.py` rodam também `paper/tests/` (testes de figura).
- `CITATION.cff`: tipo das referências de dados corrigido para o esquema 1.2.0 (`data`).

### Removido da publicação (presente no projeto privado)
- Nomes de vítimas e qualquer dado nominal; PDFs/HTML de terceiros; microdados brutos; texto integral de notícias; instruções internas de agente.
- Do escrutínio: itens com texto de notícia/resumo enviados ao segundo codificador, respostas cruas do modelo, filas de navegador e logs.
- Lista de PDFs pendentes do projeto (lista de tarefas datada; o status "não lido" já está nos ledgers e no manifesto).
