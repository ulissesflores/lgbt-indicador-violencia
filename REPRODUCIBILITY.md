# Reproducibility

This repository distributes **derived data**, code, source ledgers and pre-registrations. It does not distribute raw
microdata, third-party PDFs or nominal data. Reproduction therefore has two tracks, plus a set of steps that cannot be
re-run.

## Two seals

1. **Reproducible derivation (Track 1).** Every published number that depends only on the distributed derived data is
   recomputed by `python3 -I run_all.py` in a separate copy (`.run/replica`) and compared, file by file, with the
   distributed one: identical bytes, or a difference of at most one unit in the last printed decimal place (rounding
   between math libraries; the runner says when it accepted one).
2. **Frozen evidence, not re-runnable.** Collections that depend on the state of the world on a given day (news, web
   pages, search counts, preliminary DATASUS files, reading of PDFs) do not come back identical. Each has a URL, an
   access date and, when a file was saved, a SHA-256 in `manifest/MANIFESTO-FONTES.csv`; what was read, coded or counted
   is in the derived CSV and JSON files.

The **integrity seal** is a separate thing: `python3 -I make_provenance.py --verify` checks that every distributed file
has the SHA-256 recorded in `manifest/SHA256SUMS.txt` and that the chain hash in `output/provenance.json` closes. The
paper PDF (`docs/paper/`) is outside the seal, because the paper cites the repository; its hash is in
`docs/paper/SHA256SUMS.txt`.

## Track 1: light (derived data, a few minutes)

```bash
python3 -m pip install -r requirements.txt   # numpy, pandas, scipy, matplotlib
python3 -I run_all.py                        # integrity -> recomputation in the replica -> tests -> seal
python3 -I run_all.py --rapido               # without the recomputation (seconds)
python3 -I scripts/reproduzir.py --only painel
```

The recomputation (`scripts/reproduzir.py`) covers the governor panel and its diagnostics, the pre-registered
re-analyses, the inverted wild-cluster interval, the president change and exposure analyses, age-standardised rates and
projections, the notification tables, the governor curation, the list sample and headline sensitivity, the series and
agreement of the LGBT+ death sources, the ideology-score sensitivity and the identifiability simulation.

## Track 2: from the official microdata (heavy, on demand)

These scripts download from the official source and **check the expected SHA-256** (from the manifest); a mismatch means
a different release from the one used. Files go to `sources/public/` and are ignored by git.

| Source | Download script | Size | Scripts that use it |
|---|---|---|---|
| SIM/DATASUS, DOBR2010–2024 (deaths by residence) | `scripts/acquire_sim.py` | ~1.6 GB | `data/sim/agrega_sim.py`, `data/sinan/sim_adultos_18mais.py` |
| Sinan/DATASUS, VIOLBR15–25 | `scripts/acquire_sinan.py` | ~300 MB | `data/sinan/serie_campo55_uf_ano.py`, `completude_sinan.py`, `triangulacao_pns_sinan.py` |
| PNS 2019 microdata and layout (IBGE) | `scripts/acquire_pns2019.py` | ~30 MB (455 MB unzipped) | `data/pns/seguro_pns2019.py`, `data/pns/agressor_risco_pns2019.py`, `data/pns/pns_c05_razao_direta.py`, `data/ggb/cobertura_implicita.py`, `data/ggb/ggb_c08_numeradores.py`, `analysis/survey-cost/deff_pns2019.py`, `analysis/survey-cost/cenarios_custo.py` |
| TSE, consulta_cand 2010/2014/2018/2022 | `scripts/acquire_tse.py` | 4 zips | `data/scripts/governadores_tse.py` |

DATASUS `.dbc` files need `pyreaddbc` and `dbfread` (separate environment; not in `requirements.txt`). Preliminary
DATASUS files (SIM 2023–2024, recent Sinan) are regenerated at the source: the manifest hash identifies the release used.

## What cannot be re-run

| Step | Why | What the repository holds |
|---|---|---|
| Nominal 2019 Grupo Gay da Bahia list (329 cases), its source links, the 160-case verification and the third reading of coder disagreements | needs the nominal list and the news texts, which are not published (victims' privacy) | 10-hex salted ids, state, category, domain, coding, adjudication and results in `analysis/ggb-audit/` |
| Media and discourse (Google News RSS, OpenAlex, Wikipedia, GDELT, Chamber, Senate) | searches and counts depend on the day; news text belongs to third parties | counts per query and year with date and SHA-256 of the raw file; coded sample without the text |
| Literature reading | restricted or copyrighted PDFs | ledgers, screening tables, short verbatim excerpts with page and PDF SHA-256 |
| Governors (Wikipedia) | manual curation of 27 pages | `data/scripts/mandatos_wiki.json`, `data/governadores_uf_2011_2026*.csv` and the check against TSE |
| Political economy (Atlas, budget, LAPOP, ESTADIC) | official PDFs and spreadsheets downloaded on given days | derived series in `analysis/political-economy/dados/`, SHA-256 of the raw files, parsing scripts |
| Expert ideology survey | third-party microdata | derived scores and party mapping; Power & Zucco (CC0) included |

## Pre-registrations

`preregistrations/{governos,mortalidade,midia}/` hold the original text, the hash recorded **before** data collection,
the recording time and later addenda. `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md`,
`data/painel/R6-PREREGISTRO-FORMA.md`, `data/disque100/PREREGISTRO-D100.md` and the criteria in
`analysis/robustness/reanalise/CRITERIOS.md` and `analysis/robustness/simetria/CRITERIOS.md` follow the same rule. The tests
recompute every hash. These files are kept byte for byte, so some still carry folder names of the working project.

**What the hash proves.** It proves that the text read today is the text that produced the recorded hash. That the text
existed before the data were seen rests on the recorded time, which, without an external timestamp, is the author's
declaration.
