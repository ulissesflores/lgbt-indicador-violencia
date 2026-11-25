# 0001. One SHA-256 chain hash over every distributed file

- **Date:** 2026-10-25 (first commit of `make_provenance.py`)
- **Status:** Accepted

## Context

The paper cites hundreds of numbers derived from public sources by the scripts in this repository. A reader needs a cheap way to know
that the files in front of them are the files that produced the paper, before deciding whether to spend minutes or
hours recomputing anything. Some steps cannot be re-run at all (news searches, reading of PDFs), so recomputation alone
cannot be the integrity check.

## Decision

`make_provenance.py` writes the SHA-256 of every distributed file to `manifest/SHA256SUMS.txt` and one chain hash,
the SHA-256 of `"<path>\0<sha256>\n"` for every file in lexicographic order of path, to `output/provenance.json` and
`output/hash-chain.md`. `--verify` recomputes both with the standard library alone. The seal covers bytes, not
recomputation: whether the scripts recompute the derived files is a separate step (`scripts/reproduzir.py`, run by
`run_all.py`).

Outside the seal, by design: the seal itself; local state and caches; raw microdata and nominal data (ADR 0002); the
paper (`paper/` and `docs/paper/`), because the paper cites the seal; `runs/`, which records the chain hash of a sealed
run; and `assets/demo/`, whose recording shows the chain hash (ADR 0007). Each would make the seal circular or would
publish what may not be published.

## Alternatives (reconstructed)

- **Recomputation as the only check.** Rejected: frozen evidence cannot be recomputed, and recomputation can differ in
  the last binary digit across systems, which would make a byte check fail for no reason.
- **A Merkle tree with one root per folder.** More structure than a single reader-facing check needs; a flat list with
  one chain hash is enough to locate a changed file (`SHA256SUMS.txt` names it).
- **A signed release only.** A signature proves who published, not what each file was; it can be added on top.

## Consequences

- Any edit to a distributed file, including a README, changes the chain hash; a new version is sealed once, at the
  end (`run_all.py --selar`).
- CI runs `make_provenance.py --verify` as its first check, before the tests and the recomputation
  (`.github/workflows/verify.yml`).
- The paper PDF has its own `docs/paper/SHA256SUMS.txt`.
