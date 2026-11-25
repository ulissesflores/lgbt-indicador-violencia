# 0003. Pre-registrations kept byte for byte and locked by hash

- **Date:** 2026-10-22 (first recorded pre-registration, Table B2 of the English edition)
- **Status:** Accepted

## Context

Eight components of the analysis were pre-registered between 2026-10-22 and 2026-10-24 (Table B2 of the English
edition), and the Disque 100 analysis has its own pre-registration (2026-10-24), outside that table. The PNS
re-analysis, the Sinan series and the draw of the 160 list cases have no prior time-stamped record. A pre-registration is worth
only what a reader can check: that the text read today is the text that existed before the data.

## Decision

- Each pre-registration is kept byte for byte, with its recorded time and SHA-256, in `preregistrations/` or beside
  the analysis it fixes (`data/presidencia/`, `data/exposicao/`, `data/painel/`, `data/disque100/`,
  `analysis/robustness/`). Changes after the fact are dated addenda; the original text is not rewritten.
- The tests recompute every hash.
- Deviations are listed in Appendix B of the paper.

## Alternatives (reconstructed)

- **An external registry (OSF, AsPredicted).** Not used; it would have added an external timestamp, which these
  components do not have.
- **Clean up the texts before publication.** Rejected: any edit breaks the hash. That is why six dated documents still
  carry one line with the path of the author's working folder ([`docs/corrections.md`](../corrections.md)).

## Consequences

The hash proves the text has not changed since the hash was recorded. That the text existed before the data were seen
rests on the recorded time, which, without an external timestamp, is the author's declaration
([`REPRODUCIBILITY.md`](../../REPRODUCIBILITY.md)).
