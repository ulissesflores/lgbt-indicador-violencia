# Inventário público (gerado por `scripts/inventario_publico.py`; não editar à mão)

sha256 de `manifest/INVENTARIO-PUBLICO.json`: `71ef65bb1179771aa77b33f4c7e0a5d2f971b9fbe9bb55af95cd724d23c877ac`

Contado só com os arquivos deste repositório (o mesmo conjunto do selo), com as regras de identidade, idioma e tipo do painel do artigo.

| Item | Repositório | Painel do artigo (árvore privada, até 2026-10-23) |
| --- | --- | --- |
| Ledgers `sources.jsonl` | 20 | 17 |
| Registros nos ledgers | 1783 | 1569 |
| Fontes únicas (identificadores) | 1025 | 829 |
| Obras distintas (sem sufixo de versão) | 1024 | - |
| Idiomas | 11 | 10 |
| Scripts Python | 172 | 139 |

## Regras

- **conjunto**: arquivos distribuídos segundo make_provenance.arquivos() (o mesmo conjunto do selo)
- **ledger**: todo sources*.jsonl do conjunto; registro = linha não vazia
- **fonte_unica**: chave_id do painel: DOI minúsculo; URL minúscula sem barra final; URL doi.org vira DOI
- **obra_distinta**: fonte única sem o sufixo /vN de DOI (mesmo preprint com e sem versão conta uma vez)
- **idioma**: idioma_do_id do painel: pt e pt-BR fundidos; maioria entre registros; empate pelo ledger consolidado
- **tipo**: tipo_do_id do painel; quartis de A-textointegral/verificacao-metadados.csv (extraída das planilhas privadas de verificação, só metadados) e das tabelas dos sources/quartiles-from-literature-reviews.csv, nessa ordem
- **scripts**: todo *.py do conjunto; cruzado com a lista dos 139 do título (painel); análise = data/ e analysis/; o resto é empacotamento do repositório

## Fontes por idioma (identificadores únicos)

| Idioma | n |
| --- | --- |
| en | 510 |
| pt | 339 |
| es | 116 |
| fr | 29 |
| de | 20 |
| ja | 5 |
| ko | 2 |
| id | 1 |
| ro | 1 |
| tr | 1 |
| zh-Hans | 1 |

## Fontes por tipo (identificadores únicos)

| Tipo | Repositório | Painel |
| --- | --- | --- |
| per_q1 | 61 | 61 |
| per_q2 | 10 | 10 |
| per_q34 | 3 | 3 |
| per_semq | 332 | 252 |
| oficial | 305 | 280 |
| preprint | 22 | 22 |
| ong | 71 | 64 |
| imprensa | 39 | 32 |
| dado | 46 | 46 |
| livro | 11 | 6 |
| enciclopedia | 27 | 27 |
| nao_classificado | 98 | 26 |

Diferenças de tipo vêm só das fontes novas da v0.3 (ledgers posteriores ao painel, abaixo).

**Reconciliação.** O mesmo cálculo, restrito aos 17 ledgers que o painel contou, dá 1569 registros, 829 identificadores, 10 idiomas e a mesma contagem por tipo: **igual ao painel em tudo**. Os 196 identificadores a mais vêm dos ledgers posteriores ao painel.

## Pares de versão fundidos em obra única

- `doi:10.21203/rs.3.rs-2864681` = `doi:10.21203/rs.3.rs-2864681/v1`

## Scripts

- Lista do título (painel): 139; no repositório: 126; fora: 13 (aquisição e ferramentas de lote, que leem material de terceiros não distribuído).
  - `analysis/full-text/_lote4_aquisicao/fetch_legit.py`
  - `analysis/full-text/entregues/G1-replicacao-ferguson-malouff.py`
  - `analysis/full-text/entregues/aplicar_rodada5.py`
  - `analysis/full-text/entregues/aplicar_rodada6.py`
  - `analysis/literature/aquisicao-out/adquirir.py`
  - `analysis/literature/aquisicao-out/consolidar.py`
  - `analysis/literature/aquisicao-out/delegado-download.py`
  - `analysis/literature/aquisicao-out2/adquirir.py`
  - `analysis/literature/aquisicao-out3/adquirir-publicos.py`
  - `analysis/regimes-asia-africa/raw/_tools/fp.py`
  - `analysis/regimes-asia-africa/raw/_tools/h2t.py`
  - `analysis/robustness/_build_triagem.py`
  - `analysis/robustness/rodar_externos.py`
- Fora da lista, de análise (25): criados depois do painel (v0.3) ou em pastas de dados.
  - `analysis/ggb-audit/scripts/s15_terceiro_codificador.py`
  - `analysis/robustness/simetria/scripts/r7_parlamento_sensibilidade.py`
  - `data/build_dashboard.py`
  - `data/disque100/fig_disque_v05.py`
  - `data/disque100/scripts/baixar.py`
  - `data/disque100/scripts/d100_catalogo.py`
  - `data/disque100/scripts/d100_comum.py`
  - `data/disque100/scripts/d100_dicionario.py`
  - `data/disque100/scripts/d100_estrutura.py`
  - `data/disque100/scripts/d100_selo.py`
  - `data/disque100/scripts/d100_series.py`
  - `data/disque100/scripts/d100_tabular.py`
  - `data/disque100/tests/test_d100_regras.py`
  - `data/disque100/tests/test_d100_saidas.py`
  - `data/exposicao/c10_estrutura.py`
  - `data/exposicao/c10_exposicao.py`
  - `data/exposicao/fig_caminho_v05.py`
  - `data/exposicao/fig_series_por_governo.py`
  - `data/painel/painel_r6_ic_wild_invertido.py`
  - `data/pns/agressor_risco_pns2019.py`
  - `data/pns/fig_agressor_pns2019.py`
  - `data/pns/fig_pns_v05.py`
  - `data/presidencia/c09_d1_its.py`
  - `data/presidencia/c09_d2_painel.py`
  - `data/presidencia/c09_estrutura.py`
- Fora da lista, de empacotamento (21): (raiz) 2; figures 1; scripts 8; tests 10.

## Ledgers

- `analysis/counterpoint/sources.jsonl`
- `analysis/discourse/governos/sources.jsonl`
- `analysis/discourse/midia/sources.jsonl`
- `analysis/discourse/mortalidade/sources.jsonl`
- `analysis/full-text/sources.jsonl`
- `analysis/ggb-audit/lit/sources.jsonl`
- `analysis/ggb-audit/sources.jsonl`
- `analysis/ggb-series/perfil/sources.jsonl`
- `analysis/ggb-series/series/sources.jsonl`
- `analysis/ideology/sources.jsonl`
- `analysis/literature/sources.jsonl`
- `analysis/political-economy/sources.jsonl`
- `analysis/regimes-asia-africa/sources.jsonl`
- `analysis/survey-cost/sources.jsonl`
- `data/regimes/sources.jsonl`
- `sources/ledgers/ledger-01/sources.jsonl`
- `sources/ledgers/ledger-02/sources.jsonl`
- `sources/ledgers/ledger-03/sources.jsonl`
- `sources/ledgers/ledger-04/sources.jsonl`
- `sources/ledgers/ledger-05/sources.jsonl`

Posteriores ao painel: `analysis/counterpoint/sources.jsonl`, `data/regimes/sources.jsonl`, `sources/ledgers/ledger-04/sources.jsonl`.
Do painel e ausentes aqui: nenhum.
