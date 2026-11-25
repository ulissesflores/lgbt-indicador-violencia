# Code reference: files kept without an English header

Every code file in this repository opens with an English header (license, author, purpose, inputs, outputs, how to
run it), except the twelve scripts described here. Each of them is named next to a SHA-256 in a pre-registration, so
editing it, even only to add a header, would break the proof that the file is the one the pre-registration refers to
(see [ADR 0003](adr/0003-pre-registrations-kept-byte-for-byte-and-locked-by-hash.md) and the amendment of 2026-11-25
in [ADR 0006](adr/0006-code-and-data-in-portuguese-documentation-in-english.md)). This page documents them file by file
instead.

- **License:** Apache-2.0 for all twelve files, as stated in [`NOTICE`](../NOTICE).
- **Author:** Carlos Ulisses Flores (Codex Hash Research Laboratory), ORCID <https://orcid.org/0000-0002-6034-7765>.
- **Repository:** <https://github.com/ulissesflores/lgbt-indicador-violencia>.

The SHA-256 written in a pre-registration may no longer match the file as it is now. For each file below, the
**Registration** line states the result of comparing the SHA-256 computed on the current file (`shasum -a 256`, checked
on 2026-11-25) with the one recorded in the pre-registration, and gives both values when they differ. Where the file
also changed in v1.3.0, [`docs/corrections-files.tsv`](corrections-files.tsv) lists its SHA-256 at the v1.2.0 tag and
in v1.3.0 with the reason ([`docs/corrections.md`](corrections.md)). In six files the v1.2.0 hash already differed
from the recorded one; this page states that fact and does not explain a change it cannot document. A file whose
current SHA-256 no longer matches is still left without a header: the pre-registration names it, so the only
differences a reader finds between the two should be the documented ones, never a later header added here.

All commands are meant to be run from the repository root. The three `*_C27.py` scripts, `c09_estrutura.py`,
`c10_estrutura.py` and `painel_r6_ic_wild_invertido.py` read the repository folder from the environment variable
`REPO_ROOT` when it is set, and otherwise derive it from the location of the script. The Disque 100 scripts derive it
from their own location.

## `data/disque100/scripts/d100_comum.py`

- **Purpose:** Shared reading and classification rules for the Disque 100 microdata, in three file layouts (A: 2011 to
  2019; B: first half of 2020; C: second half of 2020 to the third quarter of 2026). It detects the layout from the
  header, maps columns to harmonized fields, and defines the classification rules of the pre-registration: missing-value
  taxonomy, declared sexual orientation and gender identity of the victim, LGBT group, motivation, violation macro
  categories, sex and state. It uses only the standard library and streams the files.
- **Inputs:** the semester and annual CSV files in `data/disque100/raw/` (names listed in `PERIODOS` in the file). The
  official microdata are not redistributed (see
  [ADR 0002](adr/0002-official-microdata-and-nominal-data-are-not-redistributed.md)).
- **Outputs:** none. It only defines functions and constants.
- **Usage:** imported by `d100_estrutura.py`, `d100_tabular.py` and `d100_series.py` (same folder).
- **Registration:** `data/disque100/PREREGISTRO-D100.md` and `PREREGISTRO-D100.sha256`; this file is one of the two
  items sealed there. SHA-256 matches (`4d81f752833323fd...e2102f0`).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/disque100/scripts/d100_estrutura.py`

- **Purpose:** Describes the structure of the Disque 100 files before any outcome is counted. For each period it writes
  the layout, rows read and malformed, date range, the distinct labels (without frequencies) of the categorical
  columns, and a diagnosis of the unit of analysis (rows per key and what varies within a key). No key, municipality
  or free text is written.
- **Inputs:** the raw CSV file of each period given on the command line (through `d100_comum.py`), or a sample file
  given as `<period>=<file>`.
- **Outputs:** `data/disque100/saidas/estrutura/<period>.json` (`amostra-<period>.json` for a sample file).
- **Usage:** `python3 -I data/disque100/scripts/d100_estrutura.py 2019 2020S1` (one or more periods).
- **Registration:** listed as information only (not locked; "a change becomes an addendum") in
  `data/disque100/PREREGISTRO-D100.sha256`. SHA-256 matches
  (`27a6d187c2d4a26280f2b14dab37069b293267bb5aaccb29e10d8116d69746b3`).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/disque100/scripts/d100_tabular.py`

- **Purpose:** The pre-registered tabulation of the Disque 100 microdata (sections 3 to 8 of the pre-registration).
  One process per file, one pass per file. For each period it counts rows, reports, victims and cuts (all rows, LGBT
  group, declared LGBT orientation or identity, motivation) by state, sex, victim classification and violation
  category, in long format, and records quality counters. It checks the seal (`d100_selo.py`) and aborts if the
  pre-registration or the rules changed. No key, municipality or free text leaves the process.
- **Inputs:** the raw CSV files in `data/disque100/raw/` (through `d100_comum.py`); `data/disque100/scripts/urls.tsv`
  (announced file sizes, used to skip incomplete downloads); the seal files checked by `d100_selo.py`.
- **Outputs:** `data/disque100/saidas/d100_por_periodo.csv`, `d100_qualidade.csv` and `d100_sobreposicao_hash.csv`.
- **Usage:** `python3 -I data/disque100/scripts/d100_tabular.py [--workers 4] [--so 2011,2012]`
  (`--so` limits the periods).
- **Registration:** listed as information only (not locked; "a change becomes an addendum") in
  `data/disque100/PREREGISTRO-D100.sha256`. SHA-256 matches
  (`2ac15f1742ce247e1c6aaab8a1480157bd822293703b3e34de2c6c5b3f91a5a0`).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/disque100/scripts/d100_series.py`

- **Purpose:** Builds the annual series, the composition tables, the LGBT group by state and year, the "entry door"
  comparison with the official 2011 to 2019 balance, and the comparison with the Sinan notifications and the Yearbook
  records (national totals, and rank correlations by state with a bootstrap interval for the partial correlation given
  state population; seed 20261024, 5,000 resamples). It checks the seal first (`d100_selo.py`).
- **Inputs:** `data/disque100/saidas/d100_por_periodo.csv` (no raw data);
  `data/disque100/entradas/balanco-lgbt-perfil-das-vitimas-uf.csv`;
  `data/sinan/serie_campo55_uf_ano.csv`; `data/anuario/anuario_lgbtfobia_uf_ano_v2.csv`;
  `sources/public/p2-f8-dados-uf/tabnet/raw/sidra_9514.json`.
- **Outputs:** in `data/disque100/saidas/`: `d100_serie_anual.csv`, `d100_composicao.csv`, `d100_uf_ano.csv`,
  `d100_porta_balanco.csv`, `d100_comparacao_nacional.csv`, `d100_comparacao_uf.csv`. It needs `numpy` and `scipy`.
- **Usage:** `python3 -I data/disque100/scripts/d100_series.py`
- **Registration:** listed as information only (not locked; "a change becomes an addendum") in
  `data/disque100/PREREGISTRO-D100.sha256`. SHA-256 does not match: recorded
  `69f2c12295a9d79834afb9f87be43508fefe31b15060baad37be8d1dc6bbd075`, current
  `f44c29679dcaa7b46eefd14a63d8946d8c28450b478f3381066b811ff1be5553`. The file is listed in
  `docs/corrections-files.tsv` (reason `local-environment`, SHA-256 at v1.2.0 `cd5d341f...0287b4`, which also differs
  from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `analysis/discourse/midia/scripts/dicionario.py`

- **Purpose:** The executable dictionary of the media and discourse pre-registration: the single source of every query.
  Each entry has an identifier, a claim family (F1 to F4), a language, a label, a type (exact phrase or
  co-occurrence), the GDELT query string, a regular expression for local texts (applied to lower-case, accent-free
  text), an OpenAlex query and, for exact phrases, a Wikipedia query. It also defines the date range, the seed and the
  text normalization.
- **Inputs:** none (it defines constants and functions).
- **Outputs:** none.
- **Usage:** imported as a module by the counting and analysis scripts in the same folder (for example
  `analise_parlamento.py`, which loads a dictionary module named on its command line).
- **Registration:** `preregistrations/midia/PRE-REGISTRO.md` and `PRE-REGISTRO.original.md` cite
  `scripts/dicionario.py` with SHA-256 `283c259aacb3149ab3d5450598f374cb8434ccb9c776c106037df7b1f360e85d`. SHA-256
  matches.
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `analysis/discourse/midia/scripts/dicionario_v1_preregistrado.py`

- **Purpose:** A copy of `dicionario.py` with the same bytes (`cmp` reports no difference), kept under a name that
  marks it as the version that was pre-registered. The corrected version used after the first count is
  `dicionario_v2.py` (addendum A3 of the pre-registration); this file is not that version.
- **Inputs:** none.
- **Outputs:** none.
- **Usage:** no script of the repository imports it (a text search finds the name only in hash lists and in
  generated files); it is a stored copy of the pre-registered dictionary.
- **Registration:** same pre-registration as `dicionario.py`
  (`preregistrations/midia/PRE-REGISTRO.md` and `PRE-REGISTRO.original.md`); the pre-registration names the file
  `dicionario.py`, and this file has the same SHA-256,
  `283c259aacb3149ab3d5450598f374cb8434ccb9c776c106037df7b1f360e85d`. SHA-256 matches. The folder's `SHA256SUMS`
  lists it with the same value.
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `analysis/robustness/simetria/scripts/baseline_C27.py`

- **Purpose:** Draws the baseline sample of the symmetry check: 60 speeches of the Chamber of Deputies that contain a
  statistic outside the themes of the study (a percentage, a "every N hours" frequency, or a quantity in thousands,
  millions or billions). It removes duplicate speeches, drops those that match the theme filter of
  `analise_parlamento.py`, and draws with the seed 20261023, following section 3 of `CRITERIOS.md`.
- **Inputs:** the Chamber of Deputies speech files read through `analise_parlamento.py` (folder
  `sources/public/q1-textointegral/discurso/midia/camara`, with `_deputados.json`);
  `analysis/discourse/midia/scripts/analise_parlamento.py` and the dictionary module it loads.
- **Outputs:** `analysis/robustness/simetria/baseline_itens.jsonl` and `baseline_pool_stats.json`.
- **Usage:** `python3 -I analysis/robustness/simetria/scripts/baseline_C27.py`
- **Registration:** `analysis/robustness/simetria/SHA256SUMS-pre-execucao.txt` (hashes written before the check was
  run). SHA-256 does not match: recorded `71839f1abb6597e381e1f944f35ac15a786eeec54d940e0d0eaacc48fcaf96f0`, current
  `3e278229c7fe9af2921b74b7125ead351812ef0f2655d0557cbeb4431808cefe`. The file is listed in
  `docs/corrections-files.tsv` (reason `local-environment`, SHA-256 at v1.2.0 `c5c7ac81...766386`, which also differs
  from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `analysis/robustness/simetria/scripts/prep_C27.py`

- **Purpose:** Step 1 of the symmetry check: builds the items for the second, blind coding. From the original coded
  sample it reads only the hash, family and universe of each item (never the stance, form or source labels), takes the
  texts from the sample files, defines three strata (Parliament F2, Parliament F3 and a random draw of 100 other
  items, seed 20261023) and gives each item an opaque identifier.
- **Inputs:** `analysis/discourse/midia/amostra_codificada.csv` (columns hash, family and universe only) and the
  `_amostra_<universe>.jsonl` files in `analysis/discourse/midia/` (universes GNRSS-mundo, GNRSS-pt, OpenAlex,
  Parliament, Wikipedia).
- **Outputs:** `analysis/robustness/simetria/itens_C27.jsonl` and `sorteio_100.json`.
- **Usage:** `python3 -I analysis/robustness/simetria/scripts/prep_C27.py`
- **Registration:** `analysis/robustness/simetria/SHA256SUMS-pre-execucao.txt`. SHA-256 does not match: recorded
  `af93c8ec33633f582099b71149fb8926d4c2d661234c99710275f3305dcbed06`, current
  `4523759828db1bd9f858925875eed1ac3c6ce7b4c93e5194f6865b8a458cb9e2`. The file is listed in
  `docs/corrections-files.tsv` (reason `local-environment`, SHA-256 at v1.2.0 `85912c79...9f750f`, which also
  differs from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `analysis/robustness/simetria/scripts/rodar_C27.py`

- **Purpose:** Step 2 of the symmetry check: sends the items to an external command-line language-model client for a
  blind second coding, in groups of 10 items of the same family, shuffled with a fixed seed (20261023). The prompt
  template is frozen in `prompt_C27.txt`; the response must follow a JSON schema (stance, form, cited source, and
  whether four named organizations are cited). A group is tried up to three times; the raw response of each attempt is
  saved. It has two modes: `itens` (the items of step 1) and `base` (the baseline sample).
- **Inputs:** `analysis/robustness/simetria/prompt_C27.txt`, and `itens_C27.jsonl` (mode `itens`) or
  `baseline_itens.jsonl` (mode `base`). The client executable is read from the environment variable `GROK_BIN`
  (default `grok`) and must be installed and authenticated by the user; the outputs stored in the repository are those
  of the original run.
- **Outputs:** raw responses in `analysis/robustness/simetria/brutos_C27/`, and the consolidated coding in
  `codif_segundo_itens.json` or `codif_segundo_base.json` in `analysis/robustness/simetria/`.
- **Usage:** `python3 -I analysis/robustness/simetria/scripts/rodar_C27.py itens` or `... rodar_C27.py base`
  (an optional second argument limits the number of groups).
- **Registration:** `analysis/robustness/simetria/SHA256SUMS-pre-execucao.txt`. SHA-256 does not match: recorded
  `cb7f5f4a449a0df075ab7218af9f4b26775596ae2bdbf5f6bb832d20e624df2e`, current
  `7b7455d8f331d934b7743db05128c9c557b99b0e531fcc0f74f969b385ec9235`. The file is listed in
  `docs/corrections-files.tsv` (reasons `local-environment` and `internal-notes`, SHA-256 at v1.2.0 `04e4a727...270105`,
  which also differs from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/exposicao/c10_estrutura.py`

- **Purpose:** Structure of the design of the government-exposure analysis (C10), written before the pre-registration
  and without reading any outcome. It finds the real changes of state governor (party changes and the ideology score
  changes), classifies each by ideology block (left below 4.5, centre 4.5 to 5.5, right above 5.5) and direction,
  checks whether a full window of three years before and three after exists, whether another change of the same state
  falls inside the window, and how many reference states had no change. It also computes the federal windows (base year
  and end year per presidential term). It asserts 27 states, 67 real changes and 27 wave changes.
- **Inputs:** columns `uf`, `ano`, `ideologia` and `partido` of `data/painel/painel_uf_ano_tse_brc.csv` (outcome columns
  are not read), and `data/presidencia/presidentes_2007_2024.csv`.
- **Outputs:** `data/exposicao/c10_estrutura.md` and `data/exposicao/c10_trocas.csv`.
- **Usage:** `python3 -I data/exposicao/c10_estrutura.py`
- **Registration:** `data/exposicao/PREREGISTRO-C10.md` and `PREREGISTRO-C10.sha256`, which record SHA-256
  `87643a57f9d0e228d29eec19c09108742bed3cd4dcce62850b3796e13f8c617c` for this file. SHA-256 does not match: current
  `a72b0d6a4d8f1dc3ba19383b15bd54c21cfce83ca9b6b794b824ce3c1fa56baa`. The file is listed in
  `docs/corrections-files.tsv` (reason `local-environment`, SHA-256 at v1.2.0 `3d79fed7...fa8d4`, which also differs
  from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/presidencia/c09_estrutura.py`

- **Purpose:** Structure of the design of the presidential-exposure analysis (C09), written before the
  pre-registration and without reading any outcome. It computes the president's ideology score per year (weighted by
  days in office; three scales), the variation left in the exposures after state and year fixed effects, the counts of
  governor and president from the same party, and the minimum detectable effect of the level change at each break of the
  interrupted time series (15 points, 2010 to 2024), as a multiple of the residual standard deviation. It asserts 351
  state-years and 27 states.
- **Inputs:** `data/presidencia/presidentes_2007_2024.csv`; `data/ideologia/ideologia_painel_tse_por_uf_ano.csv`;
  `data/ideologia/ideologia_partidos_ano.csv`; `data/ideologia_partidos.csv`;
  `sources/public/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab`. It needs `numpy` and
  `scipy`.
- **Outputs:** `data/presidencia/c09_estrutura.md`.
- **Usage:** `python3 -I data/presidencia/c09_estrutura.py`
- **Registration:** `data/presidencia/PREREGISTRO-C09.md` (the text records the SHA-256 of this file as
  `23dbf192...fb8a`; `PREREGISTRO-C09.sha256` seals the pre-registration text). SHA-256 does not match: current
  `ccee67486157bf3ef1b0f21523717b7811d73271ae18d8ade0b18c5961574f3f`. The file is listed in
  `docs/corrections-files.tsv` (reason `local-environment`, SHA-256 at v1.2.0 `e4974c2f...969746`, which also differs
  from the recorded one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).

## `data/painel/painel_r6_ic_wild_invertido.py`

- **Purpose:** 95% confidence intervals by inversion of the wild-cluster bootstrap-t test, for the six outcomes of the
  governors' panel (total, men, women, Black, non-Black, firearm). The model is the one of the main panel
  (log rate on ideology with state and year fixed effects, clustered by state, 27 clusters); the functions come from
  `painel_diagnosticos.py`, which is not changed. It uses 9,999 Rademacher draws (seed 20261024), checks that the
  estimate and standard error equal the published ones, and writes the converted effect of a 5-point ideology change.
  The published normal interval is kept beside the inverted one and the t(26) one.
- **Inputs:** `data/painel/painel_uf_ano_tse_brc.csv`, `data/painel/c02_indet_resultados.csv`,
  `data/painel/painel_diagnosticos.py`, and the pre-registration of the form (`R6-PREREGISTRO-FORMA.md` and
  `.sha256`). It needs `numpy`.
- **Outputs:** `data/painel/r6_ic_wild_invertido.csv` and `data/painel/r6_ic_wild_invertido.md`.
- **Usage:** `python3 -I data/painel/painel_r6_ic_wild_invertido.py`. At start it recomputes the SHA-256 of
  `R6-PREREGISTRO-FORMA.md` and stops if it differs from `R6-PREREGISTRO-FORMA.sha256`.
- **Registration:** `data/painel/R6-PREREGISTRO-FORMA.md` and `R6-PREREGISTRO-FORMA.sha256`. The recorded SHA-256
  (`c6f07e2c0391c11745e75569dc79137647409034ece8e43675928bff9e7698bf`) is that of the pre-registration text, written
  before this script; no SHA-256 of the script itself is recorded, so there is nothing to compare it with. The
  recorded value matches the current pre-registration text. The script is listed in `docs/corrections-files.tsv`
  (reason `local-environment`; SHA-256 at v1.2.0 `8d7757d2...6d3f`, in v1.3.0
  `9462b2814ee21908a7a7ae96403d6ac77e4905548422da5f82ca5859d470bd0a`, the current one).
- **License:** Apache-2.0 ([`NOTICE`](../NOTICE)).
