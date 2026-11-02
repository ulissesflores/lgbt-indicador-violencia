"""Fisher exato bicaudal (hipergeometrica) para comparar taxas F2 x linha de base. Python: /opt/homebrew/bin/python3.14 -I"""
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
