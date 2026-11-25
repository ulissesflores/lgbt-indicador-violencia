# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Compute two-sided exact Fisher p-values for F2 source rates against a baseline.

The script defines a hypergeometric two-sided Fisher exact test (sum of the probabilities not
larger than the observed one) and applies it to five fixed comparisons of counts: primary
source and any source, F2 original coding and F2 second-coder coding against the baseline
sample, plus the two F2 codings against each other. The counts are written in the script.

Inputs
------
- none (the counts are literals in the script)

Outputs
-------
- prints one line per comparison with the p-value to three decimals (recorded in
  analysis/robustness/simetria/fisher_C27.txt)

Usage
-----
python3 -I analysis/robustness/simetria/scripts/fisher_C27.py

Status
------
Feeds numbers printed in the article (listed in paper_numbers.json).

Notes
-----
Original description (Portuguese), kept verbatim:

Fisher exato bicaudal (hipergeometrica) para comparar taxas F2 x linha de base. Python: /opt/homebrew/bin/python3.14 -I

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
from math import comb
def fisher(a, n1, b, n2):
    K = a + b; N = n1 + n2
    p = lambda x: comb(n1, x) * comb(n2, K - x) / comb(N, K)
    p0 = p(a)
    return sum(p(x) for x in range(max(0, K - n2), min(n1, K) + 1) if p(x) <= p0 + 1e-12)
for nome, a, n1, b, n2 in [("primaria: F2 original 0/49 x base 2/38", 0, 49, 2, 38), ("primaria: F2 Grok 1/50 x base 2/38", 1, 50, 2, 38),
                           ("alguma fonte: F2 original 8/49 x base 3/38", 8, 49, 3, 38), ("alguma fonte: F2 Grok 5/50 x base 3/38", 5, 50, 3, 38),
                           ("primaria: F2 original 0/49 x F2 Grok 1/50", 0, 49, 1, 50)]:
    print(f"{nome}: p = {fisher(a, n1, b, n2):.3f}")
