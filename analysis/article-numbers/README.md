# Article numbers: public origin of the numbers computed in the text

**English** · [Português (Brasil)](README.pt-BR.md)

Every number in the article comes from a script and an output in this repository, from a third-party source with its
location transcribed, or is a declared limit. This folder holds the numbers that the article computed in its own
sentences (ratios, sums, rescalings), those that only come out of the raw public data, and the transcription of the
third-party numbers. Line numbers (`linha_pt`) refer to the Brazilian Portuguese edition of the article.

| File | What it holds | How it is produced |
|---|---|---|
| `contas_do_texto.py` -> `contas_do_texto.csv` | each sentence-level computation, with the file and key of every term, the recomputed value, and whether it matches the printed value | `python3 -I analysis/article-numbers/contas_do_texto.py` (standard library only) |
| `numeros_do_bruto.py` -> `numeros_do_bruto.csv`, `falas_expectativa.csv` | numbers that need the raw public data: the weighted share of LGB+ adults aged 18 to 29 (PNS 2019) and the life-expectancy speeches in the Chamber of Deputies | download with `scripts/acquire_pns2019.py` and `analysis/discourse/midia/scripts/camara_baixar.py`, then `.run/venv/bin/python -I analysis/article-numbers/numeros_do_bruto.py` (needs pandas) |
| `terceiros_transcritos.csv` | third-party numbers: reference, DOI or URL, page/table/section, value as found in the source, status | read by hand from the open source on 2026-11-24/25; values and locations only, no verbatim text (copyright) |
| `datas_publicacao_C18.tsv` | publication date of each of the 51 pages read in the symmetric search (Table H1, "published during the term") | read from the current version of each page on 2026-11-24; the raw pages of the original reading are not redistributed |

The speeches are matched to the coded sample by the same key used in `analysis/discourse/midia/scripts/analise_parlamento.py`
(SHA-256 of deputy id, start time and text), so a match means the text is identical to the one that was coded. The age
rule in `numeros_do_bruto.py` was fixed before the full run; a dated amendment made after seeing the result (a number
followed by "anos a menos/a mais" is a difference, not an age) is declared in the script, and both outputs are kept.

## What cannot be recomputed from this repository

- **LiHS check of the 2016 GGB list** (31, 127, 159 and 23 of 347 cases; 8.9%, 36.6%, 45.8%; 3 and 14): a count over a
  third-party spreadsheet with victims' and suspects' names, which this repository does not redistribute. Its SHA-256,
  reading date and tabulation are in `analysis/counterpoint/dados/lihs-checagem-ggb2016.META.md`; whoever holds the
  spreadsheet can check the hash and recount.
- **Open items of this folder** (rows whose `bate` or `status` is not `sim`/`conferido`): they are listed in the CSV files
  themselves and are not hidden or adjusted.
