# Corrections

**English** · [Português (Brasil)](corrections.pt-BR.md)

Dated record of what changed after each version was published. The v1.2.0 tag was not rewritten; the corrections below enter version 1.3.0 of the package and the corrected edition of the article (Codex Hash Research Report 2026-10). The numbers cited here are locked by tests in `tests/test_paper_numbers.py`. Numbers are written with a decimal point, as in the English edition of the article.

## Erratum of 2026-11-22 14:41 (GMT-3): pre-registered cuts (b) and (c) omitted in v1.2.0

**What was wrong.** The pre-registration `data/exposicao/PREREGISTRO-C10.md` (section 4, "Recortes (todos exibidos, nenhum filtrado)", that is, all cuts shown, none filtered) requires four cuts of the 67 changes of governor's party to be shown: (P) all 67; (a) full window of three years before and three after (47); (b) full window and not contaminated by another change in the same state (21); (c) only changes at an elected governor's inauguration (45). The v1.2.0 article (section 3.6 and Appendix G, in all four editions) showed cut (P) with every direction and group, and for cut (a) only the median and the p-value of the total group, without the Holm correction. Cuts (b) and (c) did not appear.

**Why it matters.** The result of cut (b) differs from what the text said. In `data/exposicao/c10_e2_resumo.csv` (total group, assault deaths):

| cut | direction | changes | rose | fell | median % | reference (median) % | p median | Holm p |
|---|---|---|---|---|---|---|---|---|
| (P) all | all | 67 | 31 | 36 | −0.7 | +4.6 | .0162 | .0732 |
| (a) full window | all | 47 | 20 | 27 | −0.8 | +5.9 | .008 | .0156 |
| (b) full and not contaminated | all | 21 | 8 | 13 | −10.2 | +6.7 | .0016 | .0064 |
| (b) full and not contaminated | to the right | 10 | 2 | 8 | −11.2 | +7.5 | .0058 | .0232 |
| (b) full and not contaminated | to the left | 11 | 6 | 5 | +1.3 | +6.7 | .3782 | 1 |
| (c) after an election | all | 45 | 21 | 24 | −0.8 | +4.6 | .0264 | .1056 |

As a result, the sentences "in both directions the result cannot be distinguished from what happens in the states that did not change government" (Appendix G) and "the analyses found no association" (section 3.6, on the exposure analysis) did not hold for every cut. The sentence "with undetermined intent added, the difference is no longer distinguishable" does not hold for cut (b) either: there the median with undetermined intent added is −6.3% (p .0016); in cuts (P), (a) and (c), with undetermined intent added, the p-value of the median is above .05.

**What did not change.** No v1.2.0 number was miscalculated: `c10_e2_resumo.csv` and the tests in `tests/test_c10_exposicao.py` remain valid. The governor panel (two-way fixed effects, interval −12.3% to +12.4%) is a different analysis and is not affected. The reading stays descriptive: the chance reference is small and not neutral (addendum 1 of the pre-registration), and no causal reading is made.

**Correction.** Appendix G of the corrected edition shows the four pre-registered cuts (total group in every direction; every group in cuts a, b and c; all 189 cells are in `c10_e2_resumo.csv`), with n, how many rose and how many fell, median, p and Holm p. Section 3.6, the Abstract and the conclusion describe the result of each cut, including the fall relative to the reference in cut (b), treated as exploratory, with a small n and no causal reading.

## Erratum of 2026-11-22 22:18 (GMT-3): "50 confirmed in news reports" in v1.2.0

**What was wrong.** The Abstract of the v1.2.0 article said that, of the 160 cases sampled from the 2019 Grupo Gay da Bahia list, 50 were "confirmed in news reports on the case itself", and the v1.2.0 READMEs, in all five languages, repeated the sentence. The text also called all 106 recovered cited sources "news reports".

**What the data say.** In `analysis/ggb-audit/dados/codificacao_A.csv`, of the 106 recovered cited sources, 84 are news reports; the others are a site's home page, a page that no longer carries the content, social media, a secondary list and one other type. Of the 50 cases in which the cited source confirms the violent death of an LGBT+ person, 48 are confirmed by a news report and 2 by a secondary list.

**Correction.** The corrected edition and the v1.3.0 READMEs say that 50 cases were confirmed **by the cited source (48 by news reports)**. The total of 50 (31.3%, 95% interval 24.6% to 38.8%) does not change.

## Erratum of 2026-11-24 (GMT-3): five readings in v1.2.0 that the data or the cited source do not support

**What was wrong.** Checking every number in the article against the scripts of this repository and against the cited sources (`analysis/article-numbers/`) found five readings in the v1.2.0 text, present in all four editions (Portuguese, English, Spanish and Italian):

1. **Table H1 (Appendix H), column "Pages published during the term":** 6/10 for Dilma Rousseff, 6/8 for Michel Temer, 23/51 in total.
2. **Section 4.2, ODIHR (2025):** official hate crime statistics "in 46 States" of the Organization for Security and Co-operation in Europe.
3. **Section 4.2, FRA (2024):** "13% to 14%" of respondents attacked over five years, attributed to the European Union.
4. **Appendix E, Frisch & Brønnum-Hansen (2009):** a same-sex marriage indicator covering 1% to 6% "of gay men".
5. **Appendix K:** 329,644 adults to be contacted.

**What the data and the sources say.**

1. Each of the 51 pages read in the symmetric search was dated by its publication date, read on the current version of each page on 2026-11-24, and compared with the date each president took office (Dilma Rousseff until 2016-05-11, Michel Temer from 2016-05-12). The column is 5/10, 5/8 and 21/51. Counting by calendar year gives 7/10, 6/8 and 24/51; the printed 6/10, 6/8 and 23/51 follows from neither rule. Three pages without a legible publication date (all from the same journal article) are not counted as published during the term. Dates: `analysis/article-numbers/datas_publicacao_C18.tsv`; recount: `analysis/article-numbers/contas_do_texto.py`.
2. ODIHR (2025), PDF p. 2: 42 of the 57 participating States have official statistics, and 47 sent some data or information. The number 46 is not in the source.
3. FRA (2024): the 2023 survey covers 30 countries, not only the European Union. 14% is the figure for all 30 countries (PDF p. 24 and p. 58); 13% is the figure for the European Union (PDF p. 68).
4. Frisch & Brønnum-Hansen (2009), Discussion: the estimated 1% to 6% refers to gay or lesbian people, not to gay men.
5. 329,643: the number of LGB+ adults needed, 5,786.288 before rounding (printed as 5,786.3), divided by the unweighted fraction of LGB+ adults (1,554 of 88,531) is 329,643.4. Dividing the rounded 5,786.3 gives 329,644.1, the printed value.

Source, page and value for items 2 to 4 are in `analysis/article-numbers/terceiros_transcritos.csv`; the calculations for items 1 and 5 are in `analysis/article-numbers/contas_do_texto.csv`. The test `test_errata_2026_11_24_cinco_leituras` (`tests/test_paper_numbers.py`) regenerates that file from its script and locks the five corrected values.

**Correction.** The corrected edition, in all five languages, prints 5/10, 5/8 and 21/51 in Table H1; "In 42 of the 57 States"; "In 30 European countries ... 14% ..., and 13% in the European Union"; "1% to 6% of gay or lesbian people"; and 329,643. `analysis/robustness/simetria/scripts/tabela_C18.py`, `TABELA_C18.md` and `SIMETRIA.md` carry the same correction to Table H1.

**What did not change.** The other columns of Table H1 (searches, pages read 51/55, events by type) and the text of Appendix H, which draws on the episode columns, not on this one; the values 13% and 14% themselves, only the scope each one belongs to; "about 330 thousand" in Appendix K; the mortality ratios reported by Frisch & Brønnum-Hansen.

## Erratum of 2026-11-25 (GMT-3): lower bound of the finite-population interval in Appendix F

**What was wrong.** The note to the agreement table of Appendix F (check of the 160 cases of 2019), in all editions of the 1.3.0 article and in the supplementary material, says that the finite-population correction (160 of 329 cases) would narrow the Wilson interval of the 50 verifiable cases "to 26.3% to 36.6%". The lower bound is 26.4%, not 26.3%.

**What the data say.** The Wilson interval for 50 of 160 with z multiplied by the finite-population factor, the square root of (329 − 160) / (329 − 1), gives 26.350265% to 36.607962% (`analysis/ggb-audit/dados/validacao_resumo.json`; calculation in `analysis/article-numbers/contas_do_texto.py`, row `ggb_wilson_fpc_lo` of `contas_do_texto.csv`). Rounded to one decimal place, the lower bound is 26.4 and the upper bound is 36.6. No variant of the formula gives 26.3 (without the −1 in the factor: 26.357; Agresti-Coull: 26.58; Wald: 26.08); 26.3 comes from cutting 26.35 instead of rounding it. Entry `l1221|6` of `paper_numbers.json` records the printed 26.3 and the corrected 26.4, and `verify_paper_numbers.py` accepts the printed value only because this paragraph exists and the calculation rounds to 26.4.

**What did not change.** The 50 verifiable cases, the main interval of 24.6% to 38.8% and the upper bound of 36.6%. The article edition is frozen and keeps printing 26.3; the correction is recorded here and enters the next edition of the article.

**Addendum of 2026-11-26 (GMT-3).** The article editions were reissued on 2026-11-26, before their DOIs were minted, and all five languages now print 26.4. Entry `l1221|6` of `paper_numbers.json` now records the printed 26.4 with no correction; `tests/test_paper_numbers.py` (`test_paper_numbers_impresso_corrigido`) keeps checking the correction mechanism on a copy of that entry that prints 26.3. The paragraphs above are kept as written on 2026-11-25.

## Fix of 2026-11-25 (GMT-3): data folder of four scripts of the GGB list audit

`analysis/ggb-audit/scripts/s08_captura_recaptura.py` and `analysis/ggb-audit/scripts/s10_duplicatas.py` wrote their outputs to `analysis/ggb-audit/data/`, a folder the package does not have; the files they produce are distributed in `analysis/ggb-audit/dados/` (`captura_recaptura_trans2019.json`, `captura_recaptura_sensibilidade.json`, `cr_ggb_trans_hash.csv`, `duplicatas_candidatas_hash.csv`, `duplicatas_resumo.json`). Two more scripts had the same wrong folder: `analysis/ggb-audit/scripts/s06_pacote_codificador_B.py` read its inputs from it (`amostra.csv` and the first coder's raw coding, which is not distributed) and `analysis/ggb-audit/scripts/s09_uf_series.py` wrote `uf_2019.csv`, `serie_ggb_vs_cobertura.csv` and `inflacao_uf_serie.json` to it. In v1.3.0 the eleven paths of the four scripts point to `dados/`. No number changed: the four scripts read the nominal list, which is not distributed, so they cannot be re-run from the package (REPRODUCIBILITY.md, "What cannot be re-run"), and the distributed outputs are the ones the article cites.

## Corrections of 2026-11-26 (GMT-3): three cited sources read in full before the DOI

**What was open.** Six numbers that the article attributes to three sources were transcribed in `analysis/article-numbers/terceiros_transcritos.csv` with the status `pagina-pendente` ("page pending"): the full text had not been opened, so the repository could not show where each number is in the source. The three texts were then read in full: Pettis et al. (2022) in the journal PDF, Ferguson & Malouff (2016) in the submitted version on SSRN (abstract 2924906, the only open copy, without the journal's page numbers) and Fernández Turuelo (2024) in the journal PDF.

**What the sources say, and what changed in the text.**

1. **Pettis et al. (2022), Appendix G.** The decrease of about 30% is on p. 822 ("a 30 percent decrease from the baseline of .37 per 100,000 persons"). The text said the effect is no longer significant "with state trends"; in Table 5 (pp. 828–829) it stops being statistically significant when the model includes state trends **and** clusters the standard errors by state and quarter. The corrected edition says so and cites pp. 822 and 828–829.
2. **Ferguson & Malouff (2016), Appendix L.** The pooled rate of 5.2% (95% interval 3.0% to 8.9%) is on pp. 2 and 13 of the submitted version; the range of 2.0% (Heenan & Murray, 2006) to 13.7% (Spohn et al., 2014) is in Table 1 (p. 24); the 4.5% the text gives for Spohn et al. is on p. 12. The article does not report I²: it reports *Q*(6) = 128, *p* < .001 (p. 13). The corrected edition prints that *Q* and says that the I² of about 95% is calculated from it ((128 − 6) / 128 = 95.3%). The page "p. 1189" cannot be checked in the open version and was replaced by "Table 1 and results, in the submitted version available on SSRN". The sentence that the pooled estimate only reproduces with the table's value for one study now has a public calculation: a DerSimonian-Laird model on the logit scale over the seven studies of Table 1 (`analysis/article-numbers/ferguson_malouff_2016_tabela1.csv`), with counts rebuilt as rate times N, gives .052 with the table's .137 for Spohn et al. and .044 with the text's 4.5% (rows `ferguson_dl_tabela1` and `ferguson_dl_spohn_texto` of `contas_do_texto.csv`; the interval and *Q* of the rebuilt counts are recorded as informative, because a rate with three decimals admits more than one count).
3. **Fernández Turuelo (2024), Table I1.** The 12 case files in Valladolid in 1971 and 1972 are the study's sample, limited to those years by access to the archive (p. 114 and note 16), not a count of every case; the 4 convictions are "las cuatro sentencias condenatorias" (p. 112). The corrected edition says that the 12 are the study's sample.

**What did not change.** The numbers themselves (30%, 5.2%, 3.0% to 8.9%, 2.0%, 13.7%, 4.5%, 12 and 4) and the conclusions that use them. The six rows of the transcription file now carry the page and the passage, with the status `conferido` ("checked"), and `paper_numbers.json` no longer lists any number as `pending-source`.

## Erratum of 2026-11-28 (GMT-3): two statements of the v1.3.0 package

1. **Section "The v1.2.0 article PDFs" below** says that `docs/paper/` holds new Spanish, Italian and Hebrew translations and that each README points to the edition in its own language. Version 1.3.0 distributes only the Portuguese edition of record and the English translation, as `README.md` says; the Spanish, Italian and Hebrew READMEs point to the English edition, and the other editions will come with their own DOI.
2. **The descriptions of version 1.3.0** in `.zenodo.json`, `CITATION.cff`, `codemeta.json` and ADR 0005 say that it corrects "two readings" of the v1.2.0 article. The corrections are the dated entries of this file from 2026-11-22 to 2026-11-26: eleven corrected readings or cited sources and one fix of a script's data folder. The description of the Zenodo record of v1.3.0 (DOI 10.5281/zenodo.24635451) was corrected on 2026-11-28.

**What did not change.** No number of the article, data file under `data/`, analysis script or conclusion. Both statements are kept as they are in the v1.3.0 archive, whose seal the article prints (ADR 0008).

## The v1.2.0 article PDFs

The four article PDFs distributed in v1.2.0 (Portuguese, English, Spanish and Italian) carry the readings corrected above. They leave `docs/paper/` in v1.3.0. The folder now holds only the corrected text: the Portuguese edition of record and its English translation, each with its own DOI, and new Spanish, Italian and Hebrew translations made from the corrected text. Each README points to the edition in its own language.

## Checked, and not a correction

- **Primary source in Parliament (1 of 49).** v1.2.0 already reported 1 of 49 speeches under the codebook's literal rule as the main analysis and 0 of 49 under the original coder's rule as a sensitivity analysis. Nothing changed.
- **1.89% and 1.93%.** 1.89% is the prevalence of LGB+ adults in the 2019 PNS and remains correct. The 1.93% of the corrected edition (Appendix F) is a new computation, not the correction of an old number: 3,025,764 LGB+ adults estimated for 2023, divided by 156,554,235 adults estimated for 2023 (156.6 million), because the 2023 composition by sex, race and age differs from that of 2019.

## Privacy cleanup in v1.3.0

An independent privacy review of the package, run before this version, found material that exposed third parties or the author's working environment. It was removed or replaced; no number in the article changes, and the tests that lock the published numbers still pass. What changed, by category:

- **Third parties (`third-party`).** In `analysis/ggb-audit/dados/ggb2019_universo_hash.csv`, 12 values `sem_link:<text>` in `fonte_tipo` carried free text copied from the GGB annex (one of them a personal name); they now read only `sem_link`, and `s01_parse_ggb2019.py` writes only that. The `obs` column of `codificacao_A.csv` and `planilha_codificacao.csv`, with free-text notes per case, was replaced by the indicator `diverge_cat_ou_cidade` (1 when the cited source disagrees with the GGB category or city, 0 otherwise, empty when the source was not recovered); `s11_validacao.py` counts that indicator, and the count of 3 cases is unchanged (locked by `tests/test_paper_numbers.py`). The direct URLs of the LiHS spreadsheet (names of victims and of the accused), of the app built on it and of the archived 2016 GGB victim list were replaced by `[URL de lista nominal retirada na v1.3.0]` ("nominal-list URL removed in v1.3.0"); the LiHS institutional page stays, and so do the TDoR URLs, a public memorial made for that purpose. A sentence in `analysis/counterpoint/frente-B-internacional.md` that named a person in a litigation claim was removed. A parliamentary speech excerpt with a criminal allegation about a private person, and its transcript locator, were redacted in two files of the symmetry study; the record, with the SHA-256 before and after, is `analysis/robustness/simetria/REDACTIONS.md`. `.gitignore` and a test keep the LiHS spreadsheet out of the repository and out of the seal. The case ids were kept: they are pseudonymous, not anonymous, with respect to the list the GGB itself publishes with names (the salt is a constant in `s01_parse_ggb2019.py` and the rows follow the order of the GGB annex), and the package adds to that list only the coding of each case (`REPRODUCIBILITY.md`).
- **Author's working folder (`author-path`).** Paths and names of the author's private working folders, outside the repository, were replaced by `<pasta-de-trabalho>/` ("working folder") or `trabalho-nao-publicado/` ("unpublished work"); the tests that compare copies with their origin take the origin folder only from an environment variable.
- **Local environment (`local-environment`).** The path of the local Python interpreter was replaced by `python3`, and the location of a model tool's credentials file left `s15_terceiro_codificador.py` (the tool now comes from the environment).
- **Internal notes (`internal-notes`).** Working-session notes, references to internal briefings and reviews, and cost and account details of the language-model tools were removed from code comments and reports. Files whose SHA-256 was recorded before the results keep such notes, because rewriting them would break that proof: the pre-registrations `preregistrations/governos/PRE-REGISTRO.md`, `preregistrations/mortalidade/PRE-REGISTRO.md` (and its `.original.md`), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` and `data/disque100/PREREGISTRO-D100.md`, and the criteria and second addendum of the robustness checks, `analysis/robustness/reanalise/CRITERIOS.md`, `analysis/robustness/simetria/CRITERIOS.md` and `analysis/robustness/simetria/ADENDO-2-execucao-e-desvios.md`. They name internal briefings and working files, one quotes the author's request to the language model, and two give the command lines of the model tools. One data row, the 2026-10-11 line of `analysis/political-economy/dados/h5_linha_do_tempo.csv` (and the script that writes it), named an internal progress file as its source; it now reads "registro interno (não distribuído)" ("internal record, not distributed") and keeps that file's SHA-256 as evidence. How language models were used is described in `docs/language-model-use.md`.
- **References to withdrawn files (`follows-withdrawal`).** Files that pointed to the withdrawn files below were updated.

**Files withdrawn in v1.3.0 (`withdrawn`).** `analysis/robustness/TRIAGEM.md`, `analysis/robustness/TRIAGEM.csv`, `figures/fontes/TRIAGEM.csv`, `figures/fontes/L-SECAO-3-3-PROPOSTA.md` and `figures/fontes/L-RELATORIO.md` are no longer distributed: model reviews and internal drafting proposals are not part of the package. Figure 12, drawn from `TRIAGEM.csv` and not cited in the article, left the package with it. The Figure E1 numbers are now anchored to `figures/fontes/estudos_mortalidade_origem.md`, the table of primary sources (source excerpt, file and page) copied verbatim from the withdrawn proposal; only the note below the table (line 45) had an internal working expression reworded. `analysis/ggb-audit/resultados.csv`, a copy left at the top of that folder by the v1.1.0 reorganization, also left the package: it predates the third reading of the GGB cases (case 159, violent death changed from I to S by the two-of-three rule in `analysis/ggb-audit/dados/adjudicacao.json`) and said 73 of 88, 15 of 88 and 19 of 73, while the article and `analysis/ggb-audit/dados/resultados.csv`, the file that `s11_validacao.py` writes and the tests lock, give 74 of 88, 14 of 88 and 20 of 74. No script read the old copy.

**Auditable record.** `docs/corrections-files.tsv` lists every file changed or withdrawn by this cleanup, with its category and the SHA-256 at the v1.2.0 tag and in v1.3.0 (`withdrawn` when the file left the package). The v1.3.0 hash covers every change to the file in this version, including the corrections described above. The test `test_tabela_da_errata_bate_com_os_arquivos` (`tests/test_integridade.py`) checks that each v1.3.0 hash is that of the distributed file. The table gives categories, not the removed text, so as not to republish it.

**Historical local path kept.** Six dated documents still cite the path of the author's working folder, on a single line each: `preregistrations/midia/PRE-REGISTRO.md` and `PRE-REGISTRO.original.md` (line 76), `analysis/robustness/reanalise/CRITERIOS.md` (line 3), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` and `data/disque100/PREREGISTRO-D100.md` (line 3). They are pre-registrations and criteria whose SHA-256 was recorded before the results; rewriting them would break the proof that the text did not change. The path has been public since v1.0.0 and leads to no data. These files are listed in `tests/test_integridade.py` (`CAMINHO_HASH_TRAVADO`). For the same reason, a few frozen files still cite the local interpreter path or the name of an earlier working folder. Three script docstrings also still give the interpreter path: `data/disque100/scripts/d100_tabular.py` and `d100_estrutura.py`, whose SHA-256 is recorded beside the Disque 100 pre-registration (a change there becomes an addendum), and `analysis/robustness/simetria/scripts/fisher_C27.py`.

## File headers in v1.3.0 (not a correction)

Every code file that no pre-registration fixes by hash now opens with an English header: the
`SPDX-License-Identifier: Apache-2.0` and copyright lines and an English module docstring (purpose, inputs, outputs,
how to run, registration status, author). The original Portuguese description stays word for word in the docstring's
`Notes` section, and the body of each file is unchanged, so no number moves (ADR 0006, amendment of 2026-11-25).
Files that changed only by this header are not listed in `docs/corrections-files.tsv`; the script that writes that
table admits a file outside it only when the file without its header lines and module docstring is byte for byte the
v1.2.0 file without its module docstring. The twelve scripts named next to a hash in a pre-registration keep no header
and are described in [`docs/code-reference.md`](code-reference.md). The per-folder `SHA256SUMS` lists were written when
each step ran and record the files as they were then; several no longer match (raw files that are not distributed, paths reorganised in v1.1.0, the
cleanup above, these headers). The seal of this version is `manifest/SHA256SUMS.txt` with the chain hash.
