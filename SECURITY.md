# Security and privacy policy

This repository is a study package: derived data, code, pre-registrations and tests. It runs no service and holds no
credentials. The realistic risks are of two kinds, and both are in scope.

## What to report

1. **Privacy.** Anything in the package that identifies a victim, an accused person or any other third party, or that
   exposes the author's private working environment. Victims' names are never distributed
   ([ADR 0002](docs/adr/0002-official-microdata-and-nominal-data-are-not-redistributed.md)). One route is known and
   declared there: the case ids of the 2019 Grupo Gay da Bahia list can be matched to the list the GGB itself
   publishes, with names, because the rows follow its order. Any other way to re-identify a case from what is
   distributed is a report.
2. **Integrity.** A distributed file that does not match `manifest/SHA256SUMS.txt`, a chain hash that does not close,
   or a download script that accepts a file whose SHA-256 differs from the manifest.
3. **Code.** A script that writes outside the repository or the `sources/public/` download folder, or that runs code
   from the data it reads.

## How to report

**Do not open a public issue for a privacy report.** Use the contact form at https://ulissesflores.com, which
reaches the author privately.

Say which file and line, what it exposes or breaks, and how you found it. Integrity and code reports with no personal
data may be public issues.

## What happens next

A privacy report is acknowledged within 72 hours. Material that exposes a person is removed in a new version, and the
removal is recorded, file by file with SHA-256 before and after, in [`docs/corrections.md`](docs/corrections.md) and
`docs/corrections-files.tsv`, as was done in version 1.3.0. Versions already deposited on Zenodo cannot be deleted; the
record of the removal says what changed.

## Supported versions

Only the latest version is corrected. Earlier versions stay as published, with their corrections listed in
[`docs/corrections.md`](docs/corrections.md).
