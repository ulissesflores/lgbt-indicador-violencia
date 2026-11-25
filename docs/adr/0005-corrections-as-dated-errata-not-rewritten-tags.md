# 0005. Corrections as dated errata, not rewritten tags

- **Date:** 2026-11-22 (the two errata of version 1.3.0)
- **Status:** Accepted

## Context

After v1.2.0 was published with a DOI, two readings were found to be wrong: two pre-registered cuts of the governor
analysis had been omitted, and "50 confirmed in news reports" should have read "by the cited source (48 by news
reports)". A privacy review found material that exposed third parties or the author's working environment.

## Decision

- The v1.2.0 tag is not rewritten. Corrections enter version 1.3.0 and are recorded, dated, in
  [`docs/corrections.md`](../corrections.md), with what was wrong, why it matters, what did not change and the
  correction.
- Every file changed or withdrawn by the privacy cleanup is listed in `docs/corrections-files.tsv`, with its category
  and its SHA-256 at v1.2.0 and in v1.3.0; a test checks the table against the files.
- The Spanish and Italian editions of the paper, which carry both corrected readings, leave `docs/paper/` and return
  once corrected, each with its own DOI.

## Alternatives (reconstructed)

- **Rewrite v1.2.0.** Rejected: a DOI record is permanent, and a reader who cited v1.2.0 must be able to see what
  changed.
- **Keep the Spanish and Italian PDFs with a note.** Rejected: a reader of a PDF does not see the note.

## Consequences

Version 1.3.0 ships two editions of the paper (Portuguese and English); the Spanish, Italian and Hebrew READMEs point to
the English edition until their own exists.
