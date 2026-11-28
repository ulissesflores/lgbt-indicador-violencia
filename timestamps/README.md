# Independent time-stamps

These files let a third party check, without trusting the author or GitHub, that the
pre-registrations and the sealed results of this package already existed at 2026-11-28 00:13:30 UTC
(27 November 2026, 21:13 in Brasília, UTC−3), the time of the RFC 3161 stamp.

| File | What it is |
|---|---|
| `carimbo-lgbt-indicador-violencia-e68396f.sha256` | Manifest in `sha256sum` format: the three pre-registrations (current and original text), their `.sha256` files and the three seal files (`output/hash-chain.md`, `output/provenance.json`, `manifest/SHA256SUMS.txt`) at commit `e68396f51746a83dfd696e93cf4d79e66b3048fe`. Its first line is a comment in Portuguese; the file is kept byte for byte because it is the stamped object. |
| `*.sha256.ots` | OpenTimestamps proof, anchored in Bitcoin block 977874. |
| `*.sha256.tsq`, `*.sha256.tsr` | RFC 3161 request and response from the FreeTSA time-stamp authority (2026-11-28 00:13:30 UTC). |
| `freetsa-cacert.pem`, `freetsa-tsa.crt` | FreeTSA public certificates, reproduced unmodified (`LicenseRef-FreeTSA-public-certificate`); they contain the authority's published contact address. |

Only the hash of the manifest left the author's machine. The stamp proves that these files
existed at that time (the Bitcoin anchor, block 977874, is from 2026-11-28 00:46:11 UTC); it does not prove the October dates of the pre-registrations, for
which the `.sha256` files in `preregistrations/` and the git history apply.

The manifest refers to commit `e68396f`, so it is checked on that commit, not on later ones
(the seal is recomputed whenever the package changes). This folder is outside the seal
(`make_provenance.py`, rule `EXCLUI_PAPER_DIRS`), because it holds proofs about the seal.

## Verify

```bash
git clone https://github.com/ulissesflores/lgbt-indicador-violencia.git
cd lgbt-indicador-violencia
cp -r timestamps /tmp/lgbt-timestamps        # the folder does not exist at e68396f
git checkout e68396f51746a83dfd696e93cf4d79e66b3048fe
T=/tmp/lgbt-timestamps/carimbo-lgbt-indicador-violencia-e68396f.sha256

# 1. the files at e68396f match the stamped manifest
shasum -a 256 -c "$T"

# 2. RFC 3161 (FreeTSA): expect "Verification: OK"
openssl ts -verify -in "$T.tsr" -data "$T" \
  -CAfile /tmp/lgbt-timestamps/freetsa-cacert.pem \
  -untrusted /tmp/lgbt-timestamps/freetsa-tsa.crt

# 3. OpenTimestamps (Bitcoin): needs a Bitcoin node, or check the block header online
uv run --with opentimestamps-client ots verify "$T.ots"
uv run --with opentimestamps-client ots info "$T.ots"   # shows the block height
```
