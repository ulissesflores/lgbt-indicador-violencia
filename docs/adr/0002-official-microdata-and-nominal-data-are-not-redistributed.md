# 0002. Official microdata and nominal data are not redistributed

- **Date:** 2026-10-25 (first commit of the `scripts/acquire_*.py` download scripts)
- **Status:** Accepted

## Context

The analyses start from official microdata (SIM and Sinan from DATASUS, the 2019 PNS from IBGE, candidate files from
TSE), several gigabytes under their own terms, and from the 2019 Grupo Gay da Bahia list, which names victims.

## Decision

- Official microdata are downloaded by `scripts/acquire_*.py`, which check each file against the SHA-256 recorded in
  `manifest/MANIFESTO-FONTES.csv`; a mismatch means a different release from the one used. The files go to
  `sources/public/` and are ignored by git and excluded from the seal.
- The repository distributes the derived data that the scripts produce, and the tests run on those.
- Nominal data are never distributed. Cases of the Grupo Gay da Bahia list are identified by 10-hex ids (the first 10
  hex digits of a SHA-256 over a salt, the case number, the name and the city). The ids are pseudonymous, not
  anonymous: the default salt is a constant written in `analysis/ggb-audit/scripts/s01_parse_ggb2019.py`, and
  `analysis/ggb-audit/dados/ggb2019_universo_hash.csv` lists the cases in the order of the GGB annex, so whoever holds
  the list the GGB itself publishes, with names, can match each row to its case. What the package adds to that list is
  the coding of each case. A test fails if the nominal spreadsheet of the LiHS check appears on disk inside the
  package.

## Alternatives (reconstructed)

- **Redistribute the microdata.** Rejected: size, the sources' own terms, and preliminary DATASUS files that the source
  regenerates (the manifest hash identifies the release used).
- **Redistribute the list with names.** Rejected: victims' privacy. The price is that the 160-case verification cannot
  be re-run from the repository; [`REPRODUCIBILITY.md`](../../REPRODUCIBILITY.md) says so.

## Consequences

- Track 1 of the reproduction works offline from the derived data; Track 2 needs the downloads.
- The link between each list case and its source is not reproducible from the repository.
