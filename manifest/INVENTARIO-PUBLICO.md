# Inventário público (gerado por `scripts/inventario_publico.py`; não editar à mão)

sha256 de `manifest/INVENTARIO-PUBLICO.json`: `bf1ccc7d1125e85e06cbdc2b0529ba8701e1d4c29c35c05d8d0bb07608d0cc85`

Contado só com os arquivos deste repositório (o mesmo conjunto do selo), com as regras de identidade, idioma e tipo do painel do artigo.

| Item | Repositório | Painel do artigo (árvore privada, até 2026-10-23) |
| --- | --- | --- |
| Ledgers `sources.jsonl` | 18 | 17 |
| Registros nos ledgers | 1599 | 1569 |
| Fontes únicas (identificadores) | 853 | 829 |
| Obras distintas (sem sufixo de versão) | 852 | - |
| Idiomas | 10 | 10 |
| Scripts Python | 166 | 139 |

## Regras

- **conjunto**: arquivos distribuídos segundo make_provenance.arquivos() (o mesmo conjunto do selo)
- **ledger**: todo sources*.jsonl do conjunto; registro = linha não vazia
- **fonte_unica**: chave_id do painel: DOI minúsculo; URL minúscula sem barra final; URL doi.org vira DOI
- **obra_distinta**: fonte única sem o sufixo /vN de DOI (mesmo preprint com e sem versão conta uma vez)
- **idioma**: idioma_do_id do painel: pt e pt-BR fundidos; maioria entre registros; empate pelo ledger consolidado
- **tipo**: tipo_do_id do painel; quartis de A-textointegral/verificacao-metadados.csv (extraída das planilhas privadas de verificação, só metadados) e das tabelas dos dossiês em docs/dossies/, nessa ordem
- **scripts**: todo *.py do conjunto; cruzado com a lista dos 139 do título (painel); análise = dados/, simulacao/, research-*; o resto é empacotamento do repositório

## Fontes por idioma (identificadores únicos)

| Idioma | n |
| --- | --- |
| en | 388 |
| pt | 301 |
| es | 108 |
| fr | 29 |
| de | 17 |
| ja | 5 |
| ko | 2 |
| id | 1 |
| tr | 1 |
| zh-Hans | 1 |

## Fontes por tipo (identificadores únicos)

| Tipo | Repositório | Painel |
| --- | --- | --- |
| per_q1 | 61 | 61 |
| per_q2 | 10 | 10 |
| per_q34 | 3 | 3 |
| per_semq | 254 | 252 |
| oficial | 296 | 280 |
| preprint | 22 | 22 |
| ong | 64 | 64 |
| imprensa | 32 | 32 |
| dado | 46 | 46 |
| livro | 6 | 6 |
| enciclopedia | 27 | 27 |
| nao_classificado | 32 | 26 |

Diferenças de tipo vêm só das fontes novas da v0.3 (ledgers posteriores ao painel, abaixo).

**Reconciliação.** O mesmo cálculo, restrito aos 17 ledgers que o painel contou, dá 1569 registros, 829 identificadores, 10 idiomas e a mesma contagem por tipo: **igual ao painel em tudo**. Os 24 identificadores a mais vêm dos ledgers posteriores ao painel.

## Pares de versão fundidos em obra única

- `doi:10.21203/rs.3.rs-2864681` = `doi:10.21203/rs.3.rs-2864681/v1`

## Scripts

- Lista do título (painel): 139; no repositório: 128; fora: 11 (aquisição e ferramentas de lote, que leem material de terceiros não distribuído).
  - `research-2026-10-21-rodada3/A-textointegral/_lote4_aquisicao/fetch_legit.py`
  - `research-2026-10-21-rodada3/A-textointegral/entregues/G1-replicacao-ferguson-malouff.py`
  - `research-2026-10-21-rodada3/A-textointegral/entregues/aplicar_rodada5.py`
  - `research-2026-10-21-rodada3/A-textointegral/entregues/aplicar_rodada6.py`
  - `research-2026-10-21-rodada3/F6-asia-africa/raw/_tools/fp.py`
  - `research-2026-10-21-rodada3/F6-asia-africa/raw/_tools/h2t.py`
  - `research-2026-10-21-rodada3/F8-literatura/aquisicao-out/adquirir.py`
  - `research-2026-10-21-rodada3/F8-literatura/aquisicao-out/consolidar.py`
  - `research-2026-10-21-rodada3/F8-literatura/aquisicao-out/delegado-download.py`
  - `research-2026-10-21-rodada3/F8-literatura/aquisicao-out2/adquirir.py`
  - `research-2026-10-21-rodada3/F8-literatura/aquisicao-out3/adquirir-publicos.py`
- Fora da lista, de análise (17): criados depois do painel (v0.3) ou em pastas de dados.
  - `dados/disque100/scripts/baixar.py`
  - `dados/disque100/scripts/d100_catalogo.py`
  - `dados/disque100/scripts/d100_comum.py`
  - `dados/disque100/scripts/d100_dicionario.py`
  - `dados/disque100/scripts/d100_estrutura.py`
  - `dados/disque100/scripts/d100_selo.py`
  - `dados/disque100/scripts/d100_series.py`
  - `dados/disque100/scripts/d100_tabular.py`
  - `dados/disque100/tests/test_d100_regras.py`
  - `dados/disque100/tests/test_d100_saidas.py`
  - `dados/exposicao/c10_estrutura.py`
  - `dados/exposicao/c10_exposicao.py`
  - `dados/painel/painel_r6_ic_wild_invertido.py`
  - `dados/presidencia/c09_d1_its.py`
  - `dados/presidencia/c09_d2_painel.py`
  - `dados/presidencia/c09_estrutura.py`
  - `research-2026-10-21-rodada3/escrutinio/simetria/scripts/r7_parlamento_sensibilidade.py`
- Fora da lista, de empacotamento (21): (raiz) 2; dashboard 1; paper 2; scripts 8; tests 8.

## Ledgers

- `research-2026-10-10/sources.jsonl`
- `research-2026-10-11/sources.jsonl`
- `research-2026-10-12-deep/sources.jsonl`
- `research-2026-10-21-rodada3/A-textointegral/sources.jsonl`
- `research-2026-10-21-rodada3/F2-custos/sources.jsonl`
- `research-2026-10-21-rodada3/F3-ggb/lit/sources.jsonl`
- `research-2026-10-21-rodada3/F3-ggb/sources.jsonl`
- `research-2026-10-21-rodada3/F5-economia-politica/sources.jsonl`
- `research-2026-10-21-rodada3/F6-asia-africa/sources.jsonl`
- `research-2026-10-21-rodada3/F8-literatura/sources.jsonl`
- `research-2026-10-21-rodada3/GGB-completo/perfil/sources.jsonl`
- `research-2026-10-21-rodada3/GGB-completo/series/sources.jsonl`
- `research-2026-10-21-rodada3/discurso/governos/sources.jsonl`
- `research-2026-10-21-rodada3/discurso/midia/sources.jsonl`
- `research-2026-10-21-rodada3/discurso/mortalidade/sources.jsonl`
- `research-2026-10-21-rodada3/ideologia/sources.jsonl`
- `research-2026-10-24-v03/L-ledger/sources.jsonl`
- `research-consolidado/sources.jsonl`

Posteriores ao painel: `research-2026-10-24-v03/L-ledger/sources.jsonl`.
Do painel e ausentes aqui: nenhum.
