# Reproducibility and location of each result in the repository

**English** · [Português (Brasil)](reproducibility-and-result-locations.pt-BR.md)

## Reproducibility

The public repository is the primary reference for this study, and the article is derived from it (this study; https://github.com/ulissesflores/lgbt-indicador-violencia). The repository holds the derived data, the code, the pre-registrations with their fingerprints, the reports of the adversarial review, and the tests that lock the published numbers. A provenance seal verifies the integrity of the set. The seal is a chain hash calculated from the SHA-256 of each file distributed in the repository, except the article, its PDF, and the tools that build it. It changes if any of those files changes, and it can be checked with a single command (Table M1). The seal of the current version changes whenever the sealed files are altered; it is in output/hash-chain.md and is checked with python3 -I make_provenance.py --verify. The article's PDF is not part of the sealed set; its SHA-256 fingerprint is published in a separate file in the repository, so that readers can check that the PDF they are reading is the one derived from the version analyzed. The seal verifies that the files are the same; by itself, it does not verify when they were written.

Reproduction has two tracks (this study). The light track recalculates, in about six minutes, the numbers of the steps listed in the repository's reproduction matrix; the remaining numbers, such as the sizing in Appendix K, are checked by tests. The heavy track starts from the official microdata and was run end to end for the 2019 PNS, whose file was downloaded from IBGE with its SHA-256 checked; this run reproduced four derived files byte for byte (IBGE, 2022a). The SIM and Sinan aggregates were not rerun from the raw data (DATASUS, 2026a, 2026b). The tables of Appendix C are copied by script from the repository files, with no number typed by hand. The figures are generated with deterministic output and checked by tests that compare the plotted values with the source files and fail when a plotted value is altered; this negative control has been exercised.

The following are not redistributed:

– the raw microdata of the SIM, Sinan, PNS, TSE, and Disque 100, which are large official files that can be downloaded by acquisition scripts with an expected SHA-256 (DATASUS, 2026a, 2026b; IBGE, 2022a; TSE, 2026; MDHC, 2026);

– third-party texts, because of copyright. For these, the repository keeps the web address, the access date, and, when the file was saved, the SHA-256;

– lists of victims' names, for privacy. For this reason, the link between case and source in the validation of the 2019 Grupo Gay da Bahia (GGB) count cannot be reproduced publicly (GGB, 2020).

The complete inventory of sources and scripts, the index of what the repository contains, and the record of corrections ([`docs/corrections.md`](corrections.md)) are in the repository itself (Table M1).

## Location of Results and Verification Elements in the Repository

**Table M1**

*Path, in the public repository, of each result and each verification element of this version*

| Result or element | Section, table, or figure | Path in the repository |
|---|---|---|
| Provenance seal and its verification | section 2.4 | `output/hash-chain.md`; `output/provenance.json`; `manifest/SHA256SUMS.txt`; command `python3 -I make_provenance.py --verify` |
| Article PDF and its fingerprint | entire article | `docs/paper/paper-final-en.pdf` (English edition); `docs/paper/paper-final.pdf` (Brazilian Portuguese edition); `docs/paper/SHA256SUMS.txt` |
| Figures, plotted values, and figure texts | Figures 1 to 8; figures of Appendices C to K | `figures/article/`; `figures/` (`make_figures.py`, `valores_plotados.json`, `textos_fora_da_imagem.json`, `fontes/SOURCES.tsv`); `data/exposicao/fig_caminho_v05.py`; `data/pns/fig_pns_v05.py`; `data/pns/fig_agressor_pns2019.py`; `data/disque100/fig_disque_v05.py`; `data/exposicao/fig_series_por_governo.py` |
| Tests that lock the published numbers | section 2.4 | `tests/` (`tests/test_paper_numbers.py` locks the numbers of the Abstract, the state exposure and the corrections) |
| Nonlethal victimization and who assaulted (PNS) | section 3.1; Table 3; Tables C1 to C12 | `data/pns/` |
| Health notification forms and agreement with police reports | section 3.2; Figure 6 | `data/sinan/`; `data/concordancia/` |
| Disque 100 | section 3.2; Figure 4; Figure D3 | `data/disque100/` |
| Identifiability and sizing of a survey | sections 2.3 and 6; Figure 5; Table 6; Table K1 | `analysis/simulation/`; `analysis/survey-cost/` |
| Standardized SIM rates and series by government term | sections 3.3 and 3.6; Figure 8; Tables E2 to E4; Tables G2, G6, and G7 | `data/sim/`; `data/exposicao/` |
| Mortality outside Brazil | section 3.4; Table E1; Figure E1 | `figures/fontes/estudos_mortalidade.tsv`; `analysis/discourse/mortalidade/` |
| GGB list: 2019 verification, agreement, scale, and critical checks | section 3.5; Figure 7; Tables F1 to F4 | `data/ggb/`; `figures/fontes/ggb_validacao_resumo.json`; `analysis/ggb-audit/`; `analysis/ggb-series/`; `analysis/counterpoint/` |
| Governor panel, event study, and change of president | section 3.6; Tables G1 and G3 to G11 | `data/painel/`; `data/ideologia/`; `data/presidencia/`; `data/exposicao/` |
| Symmetric search for government acts | sections 1 and 3.7; Table H1 | `analysis/robustness/simetria/` |
| State violence under different types of regime | section 3.7; Table 5; Table I1 | `data/regimes/` |
| Circulation in Parliament and the press | section 3.7; Tables J1 and J2 | `analysis/discourse/`; `analysis/robustness/simetria/` |
| Pre-registrations and addenda | section 2.4; Tables B2 and B3 | `preregistrations/`; `analysis/robustness/reanalise/`; `analysis/robustness/simetria/`; `data/painel/R6-PREREGISTRO-FORMA.md`; `data/presidencia/`; `data/exposicao/` |
| Inventory of sources and scripts | section 2.5 | `manifest/INVENTARIO-PUBLICO.md`; `manifest/MANIFESTO-FONTES.csv`; `sources/` |
| Acquisition of the official microdata | section 2.4 | `scripts/` and `data/disque100/scripts/` (acquisition scripts with expected SHA-256) |

*Note.* Paths are relative to the root of the repository https://github.com/ulissesflores/lgbt-indicador-violencia. Source: this study.
