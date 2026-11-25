# 0007. README art drawn by code from the sealed data

- **Date:** 2026-11-24
- **Status:** Accepted

## Context

The README shows the headline findings as cards and a terminal recording of the integrity check. A picture with a
number typed by hand can drift from the paper; a recording that shows the chain hash cannot be inside the seal it shows.

## Decision

- `assets/brand/make_brand.py` draws the banner, the project icon and the finding cards, light and dark. Each number
  on a card is read from the data file that produced it, and `tests/test_readme_arte.py` checks it against the paper.
  The docstring maps each picture to its claim. The governor comparison is exploratory and stays out of the art.
- Every picture is drawn in the language of the README that shows it (English, Portuguese, Spanish, Italian and
  Hebrew; `<piece>-<language>-<theme>.svg`), with numbers in that language's format; the Hebrew pictures are mirrored
  right to left, except the project icon and the time axis. Only the terminal recording stays in English. The test
  checks that each README embeds the pictures of its own language and no other.
- Text is drawn as outlines and the SVG hash salt is fixed, so the files do not depend on installed fonts.
- The terminal recording (`assets/demo/`, scripted with vhs) is outside the seal and is recorded last, after the
  final seal.
- The laboratory's mark (`assets/brand/lab-lockup-light.png`) is the laboratory's original file; the dark version is
  derived from it by the same script. The mark is not covered by the package's licences ([`NOTICE`](../../NOTICE)).

## Alternatives (reconstructed)

- **Use the paper's figures in the README.** Rejected: they are drawn for the printed page, one result each; the
  README needs the headline findings at a glance.
- **One set of pictures in English for all five READMEs.** Rejected by the author on 2026-11-24: a reader of the
  Spanish page should not meet English pictures.
- **Draw the cards by hand.** Rejected: nothing would stop a card from drifting from the data.

## Consequences

Changing a headline number in the data fails the test until the card and the paper agree.
