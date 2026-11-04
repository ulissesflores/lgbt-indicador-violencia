<div align="center">

# Mortality and violence against LGBT+ people in Brazil: what public data allow us to claim

**An audit of sources and indicators, 2010–2026**

**English** · [Português (Brasil)](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · [עברית](README.he.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873858.svg)](https://doi.org/10.5281/zenodo.23873858)
![License: Apache-2.0 (code)](https://img.shields.io/badge/code-Apache--2.0-blue)
![License: CC BY 4.0 (data, text, figures)](https://img.shields.io/badge/data%20%26%20text-CC%20BY%204.0-lightgrey)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Reproducible: SHA-256 chain](https://img.shields.io/badge/reproducible-SHA--256_chain-green)

</div>

> [!IMPORTANT]
> In the 2019 National Health Survey, 14.70% of lesbian, gay, bisexual or other non-heterosexual (LGB+) adults reported
> physical violence in the previous year, against 3.82% of heterosexual adults; the adjusted ratio is 2.82 (95% interval,
> 2.16 to 3.68). Brazilian death records carry neither sexual orientation nor gender identity, so no national LGBT+
> mortality rate exists. Of 160 cases sampled from the Grupo Gay da Bahia list for 2019, 50 were confirmed in news reports
> on the case itself: the list is neither a rate nor a total, and unverified cases are not invented cases.

## The paper

| Language | File |
|---|---|
| Portuguese (Brazil), original | [`docs/paper/paper-final.pdf`](docs/paper/paper-final.pdf) |
| English, translation | [`docs/paper/paper-final.en.pdf`](docs/paper/paper-final.en.pdf) |
| Spanish, translation | [`docs/paper/paper-final.es.pdf`](docs/paper/paper-final.es.pdf) |
| Italian, translation | [`docs/paper/paper-final.it.pdf`](docs/paper/paper-final.it.pdf) |

The paper's figures are in Portuguese; each figure note explains its labels. Hebrew readers are served by the English
version.

## What is in this repository

| Folder or file | Contents |
|---|---|
| `data/` | Derived data and the code that produces them: survey re-analysis (`pns/`), mortality rates (`sim/`), violence notifications (`sinan/`), police reports (`anuario/`), the Disque 100 hotline (`disque100/`), the governor panel (`painel/`, `presidencia/`, `exposicao/`) |
| `analysis/` | The other analyses the paper relies on: audit of the Grupo Gay da Bahia list (`ggb-audit/`, `ggb-series/`, `counterpoint/`), survey power and cost (`survey-cost/`), identifiability simulation (`simulation/`), public discourse (`discourse/`), robustness checks (`robustness/`), ideology scores (`ideology/`), literature (`literature/`, `full-text/`) |
| `figures/` | Code and data for every figure (`make_figures.py`, `fontes/` with the plotted values) and the figures of the paper (`article/`) |
| `preregistrations/` | Pre-registrations with their timestamps and SHA-256, as cited in the paper |
| `sources/` | Public source copies used by the scripts (`public/`), the source ledgers (`ledgers/`) and journal quartiles |
| `manifest/` | Source manifest (URL, access date and, when a file was saved, SHA-256), public inventory and the seal's checksums |
| `tests/` | Tests that lock every published number to the file that produced it |
| `scripts/` | Download of the official microdata (with the expected SHA-256), the reproduction runner and the audits |
| `run_all.py`, `make_provenance.py`, `output/` | Integrity check, recomputation and the SHA-256 chain |

The source manifest (`manifest/MANIFESTO-FONTES.csv`) and the public inventory (`manifest/INVENTARIO-PUBLICO.md`) count
1025 identifiers from 20 ledgers; the repository holds 172 scripts. Code, comments and data columns keep the original
Portuguese of the study.

## How to check it

```bash
python3 -m pip install -r requirements.txt
python3 -I make_provenance.py --verify     # SHA-256 of every distributed file and the chain hash
python3 -I run_all.py --rapido             # integrity, tests and seal (seconds)
python3 -I run_all.py                      # also recomputes the derived results in a separate copy (minutes)
shasum -a 256 -c docs/paper/SHA256SUMS.txt # the paper PDF
```

Expected output of the first command:

```text
provenance verified: <chain hash> (<n> arquivos)
```

The chain hash of this version is in [`output/hash-chain.md`](output/hash-chain.md). What can and cannot be re-run, and
why, is in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## What is and is not claimed

| Claimed | Not claimed |
|---|---|
| LGB+ adults report more physical, sexual and psychological violence than heterosexual adults (2019) | That this gap measures discrimination or lifestyle: the data do not separate the two |
| No public record allows a national LGBT+ mortality rate | That LGBT+ people are or are not killed more often than others |
| Police reports, hotline complaints and notifications measure recording | That violence rose or fell under any government |
| 50 of the 160 sampled 2019 list cases (31.3%) are verifiable from the source the list itself cites | That the list is complete, or that it is invented |

## Author

Carlos Ulisses Flores · Codex Hash Research Laboratory ·
[ORCID 0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) ·
[Lattes](https://lattes.cnpq.br/6905246706890561)

## Citation

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

The DOI above always resolves to the latest version. See also [`CITATION.cff`](CITATION.cff).

## License

Code: Apache-2.0 ([`LICENSE`](LICENSE), [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)). Derived data, text and
figures: CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). Official microdata from IBGE, DATASUS and TSE
keep their own terms and are not redistributed. See [`NOTICE`](NOTICE).
