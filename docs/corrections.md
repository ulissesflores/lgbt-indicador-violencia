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

## The v1.2.0 article PDFs

The four article PDFs distributed in v1.2.0 (Portuguese, English, Spanish and Italian) carry both readings corrected above. They leave `docs/paper/` in v1.3.0. The folder now holds only the corrected editions, each with its own DOI. The Spanish and Italian editions return once they carry the correction and their own DOI; until then, the Spanish, Italian and Hebrew READMEs point to the English and Portuguese editions.

## Checked, and not a correction

- **Primary source in Parliament (1 of 49).** v1.2.0 already reported 1 of 49 speeches under the codebook's literal rule as the main analysis and 0 of 49 under the original coder's rule as a sensitivity analysis. Nothing changed.
- **1.89% and 1.93%.** 1.89% is the prevalence of LGB+ adults in the 2019 PNS and remains correct. The 1.93% of the corrected edition (Appendix F) is a new computation, not the correction of an old number: 3,025,764 LGB+ adults estimated for 2023, divided by 156,554,235 adults estimated for 2023 (156.6 million), because the 2023 composition by sex, race and age differs from that of 2019.

## Privacy cleanup in v1.3.0

An independent privacy review of the package, run before this version, found material that exposed third parties or the author's working environment. It was removed or replaced; no number in the article changes, and the tests that lock the published numbers still pass. What changed, by category:

- **Third parties (`third-party`).** In `analysis/ggb-audit/dados/ggb2019_universo_hash.csv`, 12 values `sem_link:<text>` in `fonte_tipo` carried free text copied from the GGB annex (one of them a personal name); they now read only `sem_link`, and `s01_parse_ggb2019.py` writes only that. The `obs` column of `codificacao_A.csv` and `planilha_codificacao.csv`, with free-text notes per case, was replaced by the indicator `diverge_cat_ou_cidade` (1 when the cited source disagrees with the GGB category or city, 0 otherwise, empty when the source was not recovered); `s11_validacao.py` counts that indicator, and the count of 3 cases is unchanged (locked by `tests/test_paper_numbers.py`). The direct URLs of the LiHS spreadsheet (names of victims and of the accused), of the app built on it and of the archived 2016 GGB victim list were replaced by `[URL de lista nominal retirada na v1.3.0]` ("nominal-list URL removed in v1.3.0"); the LiHS institutional page stays, and so do the TDoR URLs, a public memorial made for that purpose. A sentence in `analysis/counterpoint/frente-B-internacional.md` that named a person in a litigation claim was removed. A parliamentary speech excerpt with a criminal allegation about a private person, and its transcript locator, were redacted in two files of the symmetry study; the record, with the SHA-256 before and after, is `analysis/robustness/simetria/REDACTIONS.md`. `.gitignore` and a test keep the LiHS spreadsheet out of the repository and out of the seal. The case ids were kept: they are pseudonymous, not anonymous, with respect to the list the GGB itself publishes with names, and the package adds to that list only the coding of each case (`REPRODUCIBILITY.md`).
- **Author's working folder (`author-path`).** Paths and names of the author's private working folders, outside the repository, were replaced by `<pasta-de-trabalho>/` ("working folder") or `trabalho-nao-publicado/` ("unpublished work"); the tests that compare copies with their origin take the origin folder only from an environment variable.
- **Local environment (`local-environment`).** The path of the local Python interpreter was replaced by `python3`, and the location of a model tool's credentials file left `s15_terceiro_codificador.py` (the tool now comes from the environment).
- **Internal notes (`internal-notes`).** Working-session notes, references to internal briefings and reviews, and cost and account details of the language-model tools were removed from code comments and reports. How language models were used is described in `docs/language-model-use.md`.
- **References to withdrawn files (`follows-withdrawal`).** Files that pointed to the withdrawn files below were updated.

**Files withdrawn in v1.3.0 (`withdrawn`).** `analysis/robustness/TRIAGEM.md`, `analysis/robustness/TRIAGEM.csv`, `figures/fontes/TRIAGEM.csv`, `figures/fontes/L-SECAO-3-3-PROPOSTA.md` and `figures/fontes/L-RELATORIO.md` are no longer distributed: model reviews and internal drafting proposals are not part of the package. Figure 12, drawn from `TRIAGEM.csv` and not cited in the article, left the package with it. The Figure E1 numbers are now anchored to `figures/fontes/estudos_mortalidade_origem.md`, the table of primary sources (source excerpt, file and page) copied verbatim from the withdrawn proposal; only the note below the table (line 45) had an internal working expression reworded. `analysis/ggb-audit/resultados.csv`, a copy left at the top of that folder by the v1.1.0 reorganization, also left the package: it predates the third reading of the GGB cases (case 159, violent death changed from I to S by the two-of-three rule in `analysis/ggb-audit/dados/adjudicacao.json`) and said 73 of 88, 15 of 88 and 19 of 73, while the article and `analysis/ggb-audit/dados/resultados.csv`, the file that `s11_validacao.py` writes and the tests lock, give 74 of 88, 14 of 88 and 20 of 74. No script read the old copy.

**Auditable record.** `docs/corrections-files.tsv` lists every file changed or withdrawn by this cleanup, with its category and the SHA-256 at the v1.2.0 tag and in v1.3.0 (`withdrawn` when the file left the package). The v1.3.0 hash covers every change to the file in this version, including the corrections described above. The test `test_tabela_da_errata_bate_com_os_arquivos` (`tests/test_integridade.py`) checks that each v1.3.0 hash is that of the distributed file. The table gives categories, not the removed text, so as not to republish it.

**Historical local path kept.** Six dated documents still cite the path of the author's working folder, on a single line each: `preregistrations/midia/PRE-REGISTRO.md` and `PRE-REGISTRO.original.md` (line 76), `analysis/robustness/reanalise/CRITERIOS.md` (line 3), `data/presidencia/PREREGISTRO-C09.md`, `data/exposicao/PREREGISTRO-C10.md` and `data/disque100/PREREGISTRO-D100.md` (line 3). They are pre-registrations and criteria whose SHA-256 was recorded before the results; rewriting them would break the proof that the text did not change. The path has been public since v1.0.0 and leads to no data. These files are listed in `tests/test_integridade.py` (`CAMINHO_HASH_TRAVADO`). For the same reason, a few frozen files still cite the local interpreter path or the name of an earlier working folder.
