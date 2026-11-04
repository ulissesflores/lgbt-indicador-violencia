<div align="center">

# Mortalidade e violência contra pessoas LGBT+ no Brasil: o que os dados públicos permitem afirmar

**Uma auditoria de fontes e indicadores, 2010–2026**

[English](README.md) · **Português (Brasil)** · [Español](README.es.md) · [Italiano](README.it.md) · [עברית](README.he.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873858.svg)](https://doi.org/10.5281/zenodo.23873858)
![License: Apache-2.0 (code)](https://img.shields.io/badge/code-Apache--2.0-blue)
![License: CC BY 4.0 (data, text, figures)](https://img.shields.io/badge/data%20%26%20text-CC%20BY%204.0-lightgrey)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Reproducible: SHA-256 chain](https://img.shields.io/badge/reproducible-SHA--256_chain-green)

</div>

> [!IMPORTANT]
> Na Pesquisa Nacional de Saúde de 2019, 14,70% dos adultos lésbicas, gays, bissexuais ou de outra orientação não
> heterossexual (LGB+) relataram violência física no ano anterior, contra 3,82% dos adultos heterossexuais; a razão
> ajustada é 2,82 (intervalo de 95%, 2,16 a 3,68). Os registros de óbito brasileiros não trazem orientação sexual nem
> identidade de gênero, por isso não existe taxa nacional de mortalidade LGBT+. Dos 160 casos amostrados da lista do
> Grupo Gay da Bahia de 2019, 50 foram confirmados em notícias sobre o próprio caso: a lista não é taxa nem total, e caso
> não verificado não é caso inventado.

## O artigo

| Idioma | Arquivo |
|---|---|
| Português (Brasil), original | [`docs/paper/paper-final.pdf`](docs/paper/paper-final.pdf) |
| Inglês, tradução | [`docs/paper/paper-final.en.pdf`](docs/paper/paper-final.en.pdf) |
| Espanhol, tradução | [`docs/paper/paper-final.es.pdf`](docs/paper/paper-final.es.pdf) |
| Italiano, tradução | [`docs/paper/paper-final.it.pdf`](docs/paper/paper-final.it.pdf) |

As figuras do artigo estão em português; a nota de cada figura explica seus rótulos. Leitores de hebraico contam com a
versão em inglês.

## O que há neste repositório

| Pasta ou arquivo | Conteúdo |
|---|---|
| `data/` | Dados derivados e o código que os produz: reanálise da pesquisa (`pns/`), taxas de mortalidade (`sim/`), notificações de violência (`sinan/`), registros policiais (`anuario/`), o serviço telefônico de denúncias Disque 100 (`disque100/`), o painel de governadores (`painel/`, `presidencia/`, `exposicao/`) |
| `analysis/` | As demais análises em que o artigo se apoia: auditoria da lista do Grupo Gay da Bahia (`ggb-audit/`, `ggb-series/`, `counterpoint/`), poder estatístico e custo da pesquisa (`survey-cost/`), simulação de identificabilidade (`simulation/`), discurso público (`discourse/`), testes de robustez (`robustness/`), escores de ideologia (`ideology/`), literatura (`literature/`, `full-text/`) |
| `figures/` | Código e dados de cada figura (`make_figures.py`, `fontes/` com os valores plotados) e as figuras do artigo (`article/`) |
| `preregistrations/` | Pré-registros com seus carimbos de tempo e SHA-256, conforme citados no artigo |
| `sources/` | Cópias de fontes públicas usadas pelos scripts (`public/`), os registros de fontes (`ledgers/`) e os quartis de periódicos |
| `manifest/` | Manifesto de fontes (URL, data de acesso e, quando um arquivo foi salvo, SHA-256), inventário público e as somas de verificação do selo |
| `tests/` | Testes que vinculam cada número publicado ao arquivo que o produziu |
| `scripts/` | Download dos microdados oficiais (com o SHA-256 esperado), o executor da reprodução e as auditorias |
| `run_all.py`, `make_provenance.py`, `output/` | Verificação de integridade, recálculo e a cadeia SHA-256 |

O manifesto de fontes (`manifest/MANIFESTO-FONTES.csv`) e o inventário público (`manifest/INVENTARIO-PUBLICO.md`) contam
1025 identificadores de 20 registros; o repositório contém 172 scripts. Código, comentários e colunas de dados mantêm o
português original do estudo.

## Como verificar

```bash
python3 -m pip install -r requirements.txt
python3 -I make_provenance.py --verify     # SHA-256 of every distributed file and the chain hash
python3 -I run_all.py --rapido             # integrity, tests and seal (seconds)
python3 -I run_all.py                      # also recomputes the derived results in a separate copy (minutes)
shasum -a 256 -c docs/paper/SHA256SUMS.txt # the paper PDF
```

Saída esperada do primeiro comando:

```text
provenance verified: <chain hash> (<n> arquivos)
```

O hash da cadeia desta versão está em [`output/hash-chain.md`](output/hash-chain.md). O que pode e o que não pode ser
executado de novo, e por quê, está em [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## O que se afirma e o que não se afirma

| Afirmado | Não afirmado |
|---|---|
| Adultos LGB+ relatam mais violência física, sexual e psicológica que adultos heterossexuais (2019) | Que essa diferença mede discriminação ou estilo de vida: os dados não separam as duas coisas |
| Nenhum registro público permite uma taxa nacional de mortalidade LGBT+ | Que pessoas LGBT+ são ou não são mortas com mais frequência que as demais |
| Registros policiais, denúncias telefônicas e notificações medem o registro | Que a violência subiu ou caiu sob qualquer governo |
| 50 dos 160 casos amostrados da lista de 2019 (31,3%) são verificáveis a partir da fonte que a própria lista cita | Que a lista é completa, ou que é inventada |

## Autor

Carlos Ulisses Flores · Codex Hash Research Laboratory ·
[ORCID 0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) ·
[Lattes](https://lattes.cnpq.br/6905246706890561)

## Citação

```bibtex
@dataset{flores_lgbt_indicador_violencia,
  author    = {Flores, Carlos Ulisses},
  title     = {Mortality and violence against LGBT+ people in Brazil: what public data allow us to claim --- an audit of sources and indicators, 2010--2026},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23873858},
  url       = {https://doi.org/10.5281/zenodo.23873858}
}
```

O DOI acima sempre resolve para a versão mais recente. Veja também [`CITATION.cff`](CITATION.cff).

## Licença

Código: Apache-2.0 ([`LICENSE`](LICENSE), [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)). Dados derivados, texto e
figuras: CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). Os microdados oficiais do IBGE, do DATASUS e do
TSE mantêm seus próprios termos e não são redistribuídos. Veja [`NOTICE`](NOTICE).
