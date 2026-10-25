# Disque 100: o que o canal público permite contar, 2011-2026 (v0.3, 2026-10-24)

O Disque Direitos Humanos (Disque 100) é o canal federal de denúncias de violações de direitos humanos. Este diretório caracteriza os 23 arquivos
públicos de microdados do canal (2011 a setembro de 2026) e tabula **contagens de registros** do módulo LGBT. Não mede pessoas nem violência
ocorrida: um aumento de denúncias não é um aumento de violência, os arquivos não trazem chave de pessoa (o total de vítimas únicas não é
calculável em nenhum período) e a série muda de formato três vezes (quebras em 2020S1, 2020S2, 2022S2 e, para o campo de motivação, em 2024).
Resumo, a frase que se pode e as que não se pode dizer: [`RELATORIO-DISQUE100.md`](RELATORIO-DISQUE100.md). **Nenhum resultado do artigo depende
deste diretório**; ele alimenta só um parágrafo da seção 3.14 e a Figura 28 (Anexo F).

| Arquivo | O que é |
| --- | --- |
| `PREREGISTRO-D100.md`, `PREREGISTRO-D100.sha256` | pré-registro (unidades, recortes LGBT, períodos, duplicatas, faltantes, comparações); hash do corpo gravado em 2026-10-24T22:52:55Z antes de qualquer contagem por categoria; 2 adendos datados (2º: de 17 para os 23 arquivos, mesmas regras) |
| `DICIONARIO-D100.md`, `saidas/dicionario_rotulos.csv` | dicionário harmonizado entre os 3 formatos e os 775 rótulos de categoria, com a classe aplicada e os períodos |
| `saidas/catalogo.tsv`, `scripts/urls.tsv` | catálogo dos 23 arquivos: URL pública, tamanho, `Last-Modified`, data de acesso, sha256 |
| `scripts/` | `baixar.py` (download retomável), `d100_catalogo.py`, `d100_estrutura.py` (rótulos, sem contagem), `d100_dicionario.py`, `d100_selo.py`, `d100_tabular.py` (contagens), `d100_series.py` (séries e comparações) e as regras em `d100_comum.py` |
| `saidas/d100_serie_anual.csv`, `d100_por_periodo.csv`, `d100_composicao.csv`, `d100_uf_ano.csv`, `d100_qualidade.csv`, `d100_sobreposicao_hash.csv` | séries por ano e período, composição, UF, qualidade e sobreposição de identificadores entre semestres (CSV longos) |
| `saidas/d100_porta_balanco.csv`, `d100_comparacao_nacional.csv`, `d100_comparacao_uf.csv` | porta de entrada contra o balanço oficial 2011-2019 e comparação descritiva com Sinan e Anuário (nada é somado e nenhuma taxa é calculada) |
| `saidas/estrutura/*.json` | rótulos de categoria por arquivo (nenhuma linha de microdado) |
| `entradas/balanco-lgbt-perfil-das-vitimas-uf.csv` | balanço oficial 2011-2019 do próprio MDHC (36 KB), usado só na porta de entrada |
| `tests/` | 63 testes (regras, em arquivos sintéticos de `tests/fixtures/`; e travas das saídas). Rodar da raiz: `python3 -m pytest -q dados/disque100/tests` |

## O que NÃO está aqui, e como reproduzir

Os 23 CSV brutos (57 MB a 1,93 GB; cerca de 14 GB no total) **não são distribuídos**. `raw/` fica fora do git. Cada arquivo baixa sem cadastro, aceite de termos
ou login do endereço do catálogo (`saidas/catalogo.tsv`, coluna `url`), e o sha256 conferido está na mesma linha.

- **Trilha 1 (recalcula aqui):** `python3 -I dados/disque100/scripts/d100_series.py` refaz as séries, a porta de entrada e as comparações a partir de
  `saidas/d100_por_periodo.csv`, `entradas/` e dos derivados de Sinan, Anuário e população já distribuídos; `scripts/reproduzir.py` confere que as 6
  saídas (`d100_serie_anual`, `d100_composicao`, `d100_uf_ano`, `d100_porta_balanco`, `d100_comparacao_nacional`, `d100_comparacao_uf`) saem byte a byte iguais.
- **Trilha 2 (exige o bruto, não exercida na réplica):** `python3 -I dados/disque100/scripts/baixar.py --workers 36` (retomável; o servidor limita cerca de
  85 KB/s por conexão, ~1,2 MB/s no total), depois `d100_catalogo.py`, `d100_estrutura.py`, `d100_dicionario.py`, `d100_tabular.py` (todos conferem o selo do
  pré-registro antes de contar) e `d100_series.py`.

## Notas de proveniência

- **Pasta de trabalho de origem:** `research-2026-10-24-disque100/` do projeto privado. O pré-registro e `scripts/d100_comum.py` ficam byte a byte (o hash
  gravado cobre o corpo do pré-registro e as regras); por isso o pré-registro cita caminhos da pasta de origem (`research-2026-10-24-v03/L-fontes/...`), que
  não existem aqui: o balanço oficial que ele cita é `entradas/balanco-lgbt-perfil-das-vitimas-uf.csv`. `python3 -I dados/disque100/scripts/d100_selo.py` confere o selo.
- **Única adaptação em `scripts/d100_series.py`:** as constantes de caminho (`PROJ` e `BALANCO`) apontam para a raiz do repositório e para `entradas/`, e o balanço (latin-1 na origem) é lido em UTF-8, porque o
  arquivo foi recodificado sem mudar o conteúdo; a lógica e as saídas são as mesmas (conferido: as 6 saídas regeneradas no repositório têm o mesmo sha256 das da pasta de origem). O sha256 do original está em `manifest/MODIFICACOES.tsv`.
- **Séries comparáveis e não comparáveis:** em 2011-2019 a unidade é a linha (vítima x suspeito de um atendimento, sem chave); em 2020S1, o par vítima-suspeito; desde
  2020S2, a violação x vítima x suspeito dentro de uma denúncia (a denúncia tem chave). Em `d100_comparacao_nacional.csv`, 2020 soma linhas de B e denúncias de C e
  por isso vem marcado `misto`; a série anual por unidade está em `d100_serie_anual.csv`. 2026 vai de janeiro a setembro (parcial).
- Os testes de `tests/` usam só arquivos sintéticos; nenhum microdado, identificador de denúncia ou nome entra no repositório.
