"""S13. (4d) Sensibilidade da manchete do GGB a definicoes, com os numeros PUBLICADOS (paginas em dados/metodologia_trechos.csv).
A = manchete (todas as mortes violentas incl. suicidio, latrocinio, outras); B = A - suicidios; C = homicidio estrito (sem latrocinio/outras/suicidio), quando publicado.
2019 extra: projecao de 'so com LGBTfobia atribuida na fonte' a partir da amostra (ILUSTRATIVA; ver README). Uso: python3.14 -I s13_sensibilidade_manchete.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, json
from pathlib import Path
F3 = Path((REPO_ROOT + "/research-2026-10-21-rodada3/F3-ggb/dados"))
# ano: (total, homicidio_publicado, suicidio, latrocinio, outras, homicidio_estrito, nota)
S = {2017: (445, 387, 58, None, None, None, "sem detalhamento de latrocinio"),
     2018: (420, 320, 100, None, None, None, "suicidios 24% da contagem"),
     2019: (329, 297, 32, 19, 6, 272, "homicidio publicado 297 = 272 H + 19 L + 5 atropelamento + 1 silicone"),
     2020: (237, 215, 13, 9, 0, 215, "latrocinio separado (9)"),
     2021: (300, 276, 24, 34, 0, 242, "34 latrocinios estao DENTRO dos 276 homicidios"),
     2022: (256, None, None, None, None, None, "derivado da 'um caso a mais' em 2023; sem detalhamento publicado; Observatorio (Acontece/ANTRA/ABGLT) publicou 273"),
     2023: (257, 221, 20, 17, 16, 204, "homicidio publicado 221 inclui latrocinio e feminicidio; tabela: 204 H + 20 S + 17 L + 16 outras"),
     2024: (291, 273, 18, None, None, None, "273 'homicidios' sem separar latrocinio/outras"),
     2025: (257, 237, 20, 17, 16, 204, "destaque diz 237 homicidios; corpo: 204 H + 17 L + 16 outras + 20 S")}
rows = []
for a, (t, hp, s, l, o, hs, nota) in S.items():
    B = t - s if s is not None else None
    rows.append(dict(ano=a, A_manchete=t, B_sem_suicidio=B, C_homicidio_estrito=hs, razao_B_A=round(B/t, 3) if B else "", razao_C_A=round(hs/t, 3) if hs else "", suicidio_pct_A=round(100*s/t, 1) if s is not None else "", nota=nota))
with (F3/"sensibilidade_manchete.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
# variacao 2017->2025 sob cada definicao (onde existe)
print("A: 2017->2025", 445, "->", 257, round(257/445, 3), "| B: 2017->2025", 445-58, "->", 257-20, round((257-20)/(445-58), 3), "| 2018->2025 A", round(257/420, 3), "B", round((257-20)/(420-100), 3))
print("A 2019->2020", round(237/329, 3), "B", round((237-13)/(329-32), 3), "C", round(215/272, 3))
