# Reproducibility

This repository distributes **derived data**, code, source ledgers and pre-registrations. It does not distribute raw
microdata, third-party PDFs or nominal data. Reproduction therefore has two tracks, plus a set of steps that cannot be
re-run.

## Two seals

1. **Reproducible derivation (Track 1).** Every published number that depends only on the distributed derived data is
   recomputed by `python3 -I run_all.py` in a separate copy (`.run/replica`) and compared, file by file, with the
   distributed one: identical bytes, or a difference of at most one unit in the last printed decimal place (rounding
   between math libraries), or, when either side is printed at full precision (15 or more significant digits), a
   relative difference of at most 1e-10 (multithreaded sums and the math library of another operating system move the
   last bits; on Linux this happens in `figures/valores_plotados.json`). The runner says when it accepted one.
2. **Frozen evidence, not re-runnable.** Collections that depend on the state of the world on a given day (news, web
   pages, search counts, preliminary DATASUS files, reading of PDFs) do not come back identical. Each has a URL, an
   access date and, when a file was saved, a SHA-256 in `manifest/MANIFESTO-FONTES.csv`; what was read, coded or counted
   is in the derived CSV and JSON files.

The **integrity seal** is a separate thing: `python3 -I make_provenance.py --verify` checks that every distributed file
has the SHA-256 recorded in `manifest/SHA256SUMS.txt` and that the chain hash in `output/provenance.json` closes. The
paper PDF (`docs/paper/`) is outside the seal, because the paper cites the repository; its hash is in
`docs/paper/SHA256SUMS.txt`.

## Every number the article prints

`paper_numbers.json` lists the 5,457 numbers printed in the Brazilian Portuguese edition of the article (the one the
other editions are translated from). For each one it records the article line, the value as printed, the class of its
origin and, when the class has one, the place in the repository that holds it: the file, the locator inside the file
(CSV row and column, Markdown table section, row and column, JSON path, or a text pattern), the script that writes the
file, and the SHA-256 of both. The locators were written by reading each table and paragraph, never by searching for
the value.

```bash
python3 -I verify_paper_numbers.py           # 137 hashes + every located value at the printed precision
python3 -I verify_paper_numbers.py --rerun   # also regenerates the outputs (scripts/reproduzir.py) and checks them
```

A hash proves that nothing changed; only the rerun shows that the code produces the number. `tests/test_paper_numbers.py`
runs the same checks inside `run_all.py`, with negative controls: a printed value moved by one unit of its last digit,
or a source value changed in a copy of the file, must fail.

| Class | Printed numbers | Checked against |
|---|---|---|
| output | 4,437 | a file that a distributed script writes |
| third-party | 313 | the transcription of the cited source, with page (`analysis/article-numbers/terceiros_transcritos.csv`); this proves the article copies the source correctly, not that the repository computes it |
| hand-written | 165 | a file no distributed script writes (pre-registration, its SHA-256 record, dated report, `analysis/discourse/midia/_estimativas.txt`); each entry states why |
| text-arithmetic | 132 | the arithmetic the text does on published numbers, recomputed by `analysis/article-numbers/contas_do_texto.py` |
| parameter | 376 | not checked: a design choice (year, threshold, confidence level, pre-registration date), listed with its reason |
| declared-limit | 23 | not checked: counts over the nominal LiHS spreadsheet, which is not distributed |
| pending-source | 7 | not checked: cited source not yet opened (Fernández Turuelo, 2024; Pettis et al., 2022; Ferguson & Malouff, 2016) |
| manual-conditional | 4 | not checked: Table H1 pages counted by publication date, which depends on the dating rule |

One printed number is wrong in the frozen 1.3.0 edition: the lower bound of the finite-population interval in
Appendix F, printed 26.3, is 26.4 (26.35 before rounding). Its entry carries the corrected value, and the verifier
accepts it only because the erratum of 2026-11-25 in `docs/corrections.md` documents it and the calculation rounds to
26.4, not to 26.3.

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
agreement of the LGBT+ death sources, the ideology-score sensitivity, the identifiability simulation, the arithmetic the
paper text does on published numbers (`analysis/article-numbers/contas_do_texto.py`), Table C18, the R7 parliament
sensitivity and the repository figures (`figures/make_figures.py`: the plotted values in `figures/*.json` are compared;
the PNG, SVG and PDF images and `figures/SHA256SUMS` are informative, because matplotlib writes its own version into
them and draws slightly differently from one version to the next).

Two scripts only print to the screen, so the runner has no file to compare. `analysis/robustness/simetria/scripts/fisher_C27.py`
prints exactly the content of `analysis/robustness/simetria/fisher_C27.txt` (check: `diff <(python3 -I
analysis/robustness/simetria/scripts/fisher_C27.py) analysis/robustness/simetria/fisher_C27.txt`).
`analysis/discourse/governos/scripts/tabela_md.py` prints table rows from `paises.csv` for a working note that is not
distributed.

## Track 2: from the official microdata (heavy, on demand)

These scripts download from the official source and **check the expected SHA-256** (from the manifest); a mismatch means
a different release from the one used. Files go to `sources/public/` and are ignored by git.

| Source | Download script | Size | Scripts that use it |
|---|---|---|---|
| SIM/DATASUS, DOBR2010–2024 (deaths by residence) | `scripts/acquire_sim.py` | ~1.6 GB | `data/sim/agrega_sim.py`, `data/sinan/sim_adultos_18mais.py`, `analysis/discourse/mortalidade/sim_campos.py` (lists the DBF field names) |
| Sinan/DATASUS, VIOLBR15–25 | `scripts/acquire_sinan.py` | ~300 MB | `data/sinan/serie_campo55_uf_ano.py`, `completude_sinan.py`, `triangulacao_pns_sinan.py` |
| PNS 2019 microdata and layout (IBGE) | `scripts/acquire_pns2019.py` | ~30 MB (455 MB unzipped) | `data/pns/seguro_pns2019.py`, `data/pns/agressor_risco_pns2019.py`, `data/pns/pns_c05_razao_direta.py`, `data/ggb/cobertura_implicita.py`, `data/ggb/ggb_c08_numeradores.py`, `analysis/survey-cost/deff_pns2019.py`, `analysis/article-numbers/numeros_do_bruto.py` (block 1: share of LGB+ adults aged 18 to 29; block 2 also needs the Chamber speeches downloaded by `analysis/discourse/midia/scripts/camara_baixar.py`, matched by a hash of the text: without them the script still rewrites `falas_expectativa.csv` and `numeros_do_bruto.csv` with no speech matched and exits with code 1) |
| TSE, consulta_cand 2010/2014/2018/2022 | `scripts/acquire_tse.py` | 4 zips | `data/scripts/governadores_tse.py` |
| Disque 100 (human rights hotline), 23 CSV files | `data/disque100/scripts/baixar.py` | ~13 GB | `data/disque100/scripts/d100_tabular.py` (pre-registered tabulation; Track 1 recomputes the series from its output `saidas/d100_por_periodo.csv`) |

DATASUS `.dbc` files need `pyreaddbc` and `dbfread` (separate environment; not in `requirements.txt`). Preliminary
DATASUS files (SIM 2023–2024, recent Sinan) are regenerated at the source: the manifest hash identifies the release used.

## What cannot be re-run

| Step | Why | What the repository holds |
|---|---|---|
| Nominal 2019 Grupo Gay da Bahia list (329 cases), its source links, the 160-case verification and the third reading of coder disagreements (scripts in `analysis/ggb-audit/scripts/`: `s01_parse_ggb2019.py`, `s02_fetch_fontes.py`, `s02b_wayback_retry.py`, `s04_extrair_texto.py`, `s05_visualiza_lote.py`, `s05b_frases.py`, `s06_pacote_codificador_B.py`, `s08_captura_recaptura.py`, `s10_duplicatas.py`, `s11_validacao.py`, `s12_metodologia_paginas.py`, `s14_leak_check.py`) | needs the nominal list and the news texts, which are not published (victims' privacy) | 10-hex ids (pseudonymous, not anonymous: the salt is a constant in `s01_parse_ggb2019.py` and the rows follow the order of the GGB annex, so whoever holds the list the GGB itself publishes, with names, can match the rows to it; the package adds to that list only the coding of each case), state, category, domain, coding (with a 0/1 indicator of disagreement with the cited source, no free-text notes per case), adjudication and results in `analysis/ggb-audit/`; the packets generated for coders B and C (news texts sent to the language models), their prompts and their replies are not distributed |
| Media and discourse (Google News RSS, OpenAlex, Wikipedia, GDELT, Chamber, Senate) (scripts in `analysis/discourse/midia/scripts/`: `gn_rss.py`, `gdelt_cliente.py`, `gdelt_rodar.py`, `openalex_contar.py`, `wikipedia_contar.py`, `mostra.py`, `cod.py`) | searches and counts depend on the day; news text belongs to third parties | counts per query and year with date and SHA-256 of the raw file; coded sample, whose only verbatim text is short excerpts of public parliamentary speeches (`analysis/discourse/midia/amostra_codificada.csv`, `trecho_verbatim`) |
| Literature reading (scripts: `analysis/literature/scripts/` `enum_search.py`, `screen_openalex.py`, `check_quotes.py`, `build_readme.py`, `rows.py`; `analysis/discourse/mortalidade/scripts/` `build_estudos.py`, `verifica_trechos.py`) | restricted or copyrighted PDFs | ledgers, screening tables, short verbatim excerpts with page and PDF SHA-256 |
| Governors (Wikipedia) (script: `data/scripts/governadores_parse.py`) | manual curation of 27 pages | `data/scripts/mandatos_wiki.json`, `data/governadores_uf_2011_2026*.csv` and the check against TSE |
| Political economy (Atlas, budget, LAPOP, ESTADIC) (scripts in `analysis/political-economy/scripts/`: `h1_00_verifica_citacoes_programas.py`, `h1_01_tabnet_sim_1996_2024.py`, `h1_02_parse_atlas_td.py`, `h2_01_estadic_lgbt.py`, `h2_03_delegacias_proxy.py`, `h3_analise.py`, `h4_lapop_confianca_x_ideologia.py`, `h5_01_orcamento.py`, `h5_02_series_chave.py`, `h5_03_acoes_lgbt_rdf.py`, `h5_04_linha_do_tempo.py`, `h5_05_acoes_lgbt_cgu.py`) | official PDFs and spreadsheets downloaded on given days | derived series in `analysis/political-economy/dados/`, SHA-256 of the raw files, parsing scripts |
| Expert ideology survey (script: `analysis/ideology/scripts/build_ideologia.py`) | third-party microdata | derived scores and party mapping; Power & Zucco (CC0) included |
| Countries and governments (V-Dem, V-Party, ILGA, government PDFs) | third-party datasets and PDFs saved on given days (`analysis/discourse/governos/scripts/build_brasil.py`, `build_paises.py`, `build_u3.py`, `eixo_vparty.py`, `resumo_u3.py`; the `.RData` readers also need `pyreadr` and `pycountry`, not in `requirements.txt`) | `paises.csv`, `brasil_itens.csv`, `brasil_dados_governo.csv`, `u3_65_criminalizam.csv`, `eixo_vparty.md` and `u3_resumo.md` in `analysis/discourse/governos/` |
| Speeches in Parliament and the samples drawn from them (also `senado_baixar.py`, `camara_recupera.py`, `camara_recupera_mes.py` and the pre-registered dictionaries `dicionario.py`, `dicionario_v1_preregistrado.py`, `dicionario_v2.py`) | the full texts are downloaded by `analysis/discourse/midia/scripts/camara_baixar.py` and change at the source; `analise_parlamento.py`, `amostra_prepara.py`, `consolida.py`, `resumo_tabelas.py`, the C27 symmetry check (`prep_C27.py`, `baseline_C27.py`, `analise_C27.py`) and block 2 of `analysis/article-numbers/numeros_do_bruto.py` read them | counts, coded sample, C27 items and results in `analysis/discourse/midia/` and `analysis/robustness/simetria/`; `consolida.py` run without the full texts rewrites those files with different content, which is why it is not in the runner |
| Readings by language models (third GGB coder, second C27 reading) | need an authenticated `codex` or `grok` command line (`CODEX_BIN`, `GROK_BIN`: `s15_terceiro_codificador.py`, `rodar_C27.py`) and reply differently each time | the recorded coding of the replies |
| Governments' statements for Table C18 (`baixar_C18.py`, `eventos_C18.py`, `mostrar_C18.py`) | statements and news saved on given days | `consultas_C18.tsv`, `downloads_C18.tsv`, `picks_C18.tsv`, `eventos_C18.csv`; Table C18 itself (`tabela_C18.py`) is recomputed by the runner |
| LGBT+ death series from the publishers (`analysis/ggb-series/series/scripts/s01_fetch_tdor.py`, `s02_fetch_tmm.py`, `s04_painel.py`, `s08_dep_tdor.py`) (also `s03_sim_2000_2009.py` (SIM 2000–2009, `.dbc` files) and `s05_digitaliza_ggb.py` (chart of the GGB 2020 report); the GGB profile in `analysis/ggb-series/perfil/scripts/` (`claims.py`, `build_md.py`, `gp.py`, `html2txt.py`) reads the reports' PDFs and pages) | yearly PDFs and lists downloaded from GGB, TDoR and TMM | the series and dependency tables in `analysis/ggb-series/series/` |
| Survey cost (`analysis/survey-cost/custos_fontes.py`, `pncp_busca.py`, `ted_api.py`, `cenarios_custo.py`) | contracts, prices, IPCA (SIDRA 1737) and PTAX read on given days | `custos-fontes.csv` (each value with source, page and verbatim excerpt) and the scenario tables in `analysis/survey-cost/` |
| Source ledgers (`emit_all.py`, `emit_ledger.py`, `emite_ledger.py`, `emite_ledger_f5.py`, `s07_emit_sources.py`, `build_perfil.py`) | call `emit_sources.py` (`EMIT_SOURCES`), a tool of the author's research environment that is not distributed | the ledgers in `sources/ledgers/` and the `sources.jsonl` next to each analysis |
| Dashboard (`data/build_dashboard.py`) | counts files of the author's full working project (`LGBT_PROJETO`, `DASHBOARD_OUT`; optional `SITE_TIPOS`, `SITE_TSC`, `NODE_BIN`), including PDFs and microdata that are not distributed | `data/dashboard_dados.publico.json` |

Other scripts kept outside the runner, with the reason:

- Superseded, kept as history: `data/concordancia/concordancia_sinan_anuario.py` (replaced by `concordancia_v2.py`; writes `resumo_v1_contagens.md`, not distributed) and `data/sinan/sensibilidade_pns_sinan.py` (replaced by `triangulacao_pns_sinan.py`; its inputs were typed by hand and it APPENDS to `data/sinan/resumo.md`, so running it changes a distributed file).
- Figure drafts of version 0.5, superseded by `figures/article/code/`: `data/exposicao/fig_caminho_v05.py`, `fig_series_por_governo.py`, `data/disque100/fig_disque_v05.py`, `data/pns/fig_pns_v05.py`, `fig_agressor_pns2019.py` (they read distributed files and write the image path given as argument; the images are not distributed).
- Package tools, not analyses: `scripts/_acquire.py` (shared code of the `acquire_*` scripts), `scripts/registra_run.py` (records a sealed run in `runs/`), `data/verificacao_independente.py` (recomputes key results by a second path; run by `tests/test_integridade.py`).

Every script takes the repository root from `REPO_ROOT` (default: computed from its own location). The other environment variables named above (`F5_CACHE` for the budget zips of `analysis/political-economy/`, `CODEX_BIN`, `GROK_BIN`, `EMIT_SOURCES`, `LGBT_PROJETO`, `DASHBOARD_OUT`, `SITE_TIPOS`, `SITE_TSC`, `NODE_BIN`) are only read by the steps in this table; Track 1 needs none of them.

## Pre-registrations

`preregistrations/{governos,mortalidade,midia}/` hold the original text, the hash recorded **before** data collection,
the recording time and later addenda. `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md`,
`data/painel/R6-PREREGISTRO-FORMA.md`, `data/disque100/PREREGISTRO-D100.md` and the criteria in
`analysis/robustness/reanalise/CRITERIOS.md` and `analysis/robustness/simetria/CRITERIOS.md` follow the same rule. The tests
recompute every hash. These files are kept byte for byte, so some still carry folder names of the working project.

The frozen criteria in `analysis/robustness/*/CRITERIOS.md` cite `TRIAGEM.md` and `TRIAGEM.csv`, which were withdrawn in 1.3.0 (`docs/corrections.md`).

**What the hash proves.** It proves that the text read today is the text that produced the recorded hash. That the text
existed before the data were seen rests on the recorded time, which, without an external timestamp, is the author's
declaration.
