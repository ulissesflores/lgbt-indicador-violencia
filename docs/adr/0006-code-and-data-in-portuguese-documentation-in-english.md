# 0006. Code and data in Portuguese, documentation in English

- **Date:** 2026-11-01 (reorganisation of the repository for v1.1.0)
- **Status:** Accepted; amended 2026-11-25 (v1.3.0, file headers)

## Context

The study was written in Portuguese, about Brazilian sources whose variables and categories are Portuguese. The paper
and the package are meant for readers outside Brazil too.

## Decision

- Code, comments, data columns and the labels of the figure code keep the study's original Portuguese; translating them
  would change hashed files and the names the tests lock.
- Reader-facing documentation is in English with a Portuguese version (`docs/*.pt-BR.md`); the README is in English with
  Portuguese, Spanish, Italian and Hebrew versions.
- Each edition of the paper has its figures labelled in its own language.

## Alternatives (reconstructed)

- **Translate the code and the data.** Rejected: it would break the seal and the pre-registration hashes, and would
  separate the published column names from the official sources' names.

## Consequences

Expected terminal output is in Portuguese (`testes: ... passaram`, `arquivos`), and the READMEs say so.

## Amendment (2026-11-25, v1.3.0): file headers in English

**Context.** A reader opening a script could not tell, in English, what it does, who wrote it or under which license:
the module descriptions were in Portuguese and no code file carried a license line.

**Decision.** Every code file that no pre-registration fixes by hash opens with an English header: the
`SPDX-License-Identifier: Apache-2.0` and copyright lines, and an English module docstring (summary, purpose, inputs,
outputs, how to run it, registration status, author with ORCID and repository URL). The original Portuguese description
is kept word for word in the docstring's `Notes` section. The body of the file (code, comments, names, printed
messages) does not change, so the rest of this decision stands.

**Files left without the header.** Twelve scripts are named next to a SHA-256 in a pre-registration (ADR 0003);
editing them would break that proof. They are documented file by file in [`docs/code-reference.md`](../code-reference.md)
and keep the license stated in `NOTICE`.

**How to check that only the header changed.** `docs/corrections.md` states this change class. For any file, removing
the header lines and the module docstring from the v1.2.0 file and from the v1.3.0 file leaves the same bytes. The
per-folder `SHA256SUMS` lists written when each step ran record the files as they were then; the seal of this version
is `manifest/SHA256SUMS.txt` and the chain hash (ADR 0001).
