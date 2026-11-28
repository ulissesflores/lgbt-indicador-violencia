# 0008. The article certifies the v1.3.0 seal; later commits carry their own

- **Date:** 2026-11-28
- **Status:** Accepted

## Context

The pt-BR and English editions of the article print the seal of version 1.3.0 of this package:
`3fd2c2bf9c6c5f6a607e32360255d8a7f4cf526ecc30e0531f236d400ba86264` over 768 files. That seal is time-stamped
(OpenTimestamps and RFC 3161, `timestamps/`) and is the one the signed tag `v1.3.0` and its Zenodo record
(DOI 10.5281/zenodo.24635451) verify to. After the release, two security tools were added to the repository, both
inside the sealed tree: CodeQL static analysis (`.github/workflows/codeql.yml`) and monthly Dependabot update checks
(`.github/dependabot.yml`). Any change to a sealed file gives a new seal.

## Decision

- Version 1.3.0 keeps the seal the article prints. The two tools enter `main` after the release, with a new seal,
  and change no data under `data/`, no analysis script and no result. The files that change are: the two CI files
  above; the release date in `CITATION.cff` and `codemeta.json`; the dated erratum in `docs/corrections.md` and
  `docs/corrections.pt-BR.md`; this record and the ADR index; in `paper_numbers.json`, the locator of the printed
  "768 sealed files" and the recorded SHA-256 of the files the table names; the seal files (`output/hash-chain.md`,
  `output/provenance.json`, `manifest/SHA256SUMS.txt`); and, outside the seal, `timestamps/README.md` and
  `timestamps/seal-v1.3.0.json`.
- The test that locks the "768 sealed files" printed in the article reads the frozen record
  `timestamps/seal-v1.3.0.json` (copied from `output/provenance.json` at the tag), not the live seal.
- `python3 -I make_provenance.py --verify` on `main` checks the current seal; on the v1.3.0 archive it checks the seal
  the article prints.

## Alternatives

- **Reseal inside v1.3.0 and reprint the article.** Rejected: the article and the time-stamps already certify
  `3fd2c2bf…`; reprinting the article editions to add CI configuration buys nothing a reader can check.
- **Leave the tools out until the next version.** Rejected: they guard the repository now, and the change is limited to
  configuration files listed here.

## Consequences

A reader of the article checks the v1.3.0 archive (tag or Zenodo) and gets the printed seal. A reader of `main` gets a
newer seal; the difference is the files listed above.
