# Contributing

This repository is the study package of a published paper. The most useful contribution is a check: a number that
does not match, a reading the data do not support, a source that says something else. Every change after publication
becomes a dated correction ([ADR 0005](docs/adr/0005-corrections-as-dated-errata-not-rewritten-tags.md)).

## Report an error in a number or a reading

Open an issue with:

- the number or sentence, and where it is (paper edition and section, or file and line);
- the file in this repository that produced it (where each result lives:
  [`docs/reproducibility-and-result-locations.md`](docs/reproducibility-and-result-locations.md));
- what you expected, and the command you ran.

If the error is confirmed, it is recorded in [`docs/corrections.md`](docs/corrections.md) with what was wrong, why it
matters, what did not change and the correction, and the test that locks the number is updated.

Privacy problems are not issues: see [`SECURITY.md`](SECURITY.md).

## Check your copy before reporting

```bash
python3 -I make_provenance.py --verify   # your files are the published files
python3 -I run_all.py --rapido           # integrity, tests and seal (seconds)
python3 -I run_all.py                    # also recomputes the derived results (minutes)
```

What can and cannot be re-run is in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Pull requests

Welcome for documentation, translations of the READMEs by native speakers, and the infrastructure code
(`run_all.py`, `make_provenance.py`, `scripts/`). Before opening one:

- `ruff check` and `ruff format --check` pass, and `interrogate` stays at 100% on the infrastructure code
  (configuration in `pyproject.toml`);
- `python3 -m pytest -q` passes (the tests read only the distributed derived data). `run_all.py` stops at the
  integrity check after any edit, by design: the seal is rebuilt once per version by the author;
- code, comments and data columns keep the study's Portuguese
  ([ADR 0006](docs/adr/0006-code-and-data-in-portuguese-documentation-in-english.md)).

Not accepted: changes to pre-registrations (they are locked by hash,
[ADR 0003](docs/adr/0003-pre-registrations-kept-byte-for-byte-and-locked-by-hash.md)), nominal data of any kind, and
raw official microdata ([ADR 0002](docs/adr/0002-official-microdata-and-nominal-data-are-not-redistributed.md)).

Contributions are licensed under the terms in [`NOTICE`](NOTICE): Apache-2.0 for code, CC BY 4.0 for data and text.
