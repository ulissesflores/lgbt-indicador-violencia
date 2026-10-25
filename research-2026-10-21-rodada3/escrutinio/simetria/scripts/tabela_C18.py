"""C18: gera TABELA_C18.md e consultas_C18.tsv a partir de eventos_C18.csv, picks_C18.tsv, downloads_C18.tsv. Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv
from collections import Counter, defaultdict
S = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
NOME = {"G1": ("Lula", "2003 2004 2005 2006"), "G2": ("Lula", "2007 2008 2009 2010"), "G3": ("Dilma Rousseff", "2011 2012 2013 2014 2015 2016"),
        "G4": ("Michel Temer", "2016 2017 2018"), "G5": ("Jair Bolsonaro", "2019 2020 2021 2022"), "G6": ("Lula", "2023 2024 2025 2026")}
ROT = {"G1": "Lula 1 (2003-06)", "G2": "Lula 2 (2007-10)", "G3": "Dilma (2011-16)", "G4": "Temer (2016-18)", "G5": "Bolsonaro (2019-22)", "G6": "Lula 3 (2023-26)"}
TPL = [("D1", "{N} declaração contra homossexuais gays LGBT fala polêmica {P}", "{N} statement against homosexuals gays LGBT controversial remark {P}"),
       ("D2", "{N} omissão governo política LGBT homossexuais sem resposta silêncio {P}", "{N} government omission inaction LGBT homosexuals silence policy {P}"),
       ("D3", "{N} corte de verba programa LGBT homofobia suspenso cancelado extinto {P}", "{N} budget cut program LGBT anti-homophobia suspended cancelled abolished {P}"),
       ("D4", "{N} perseguição homossexuais LGBT censura proibição repressão ato do governo {P}", "{N} persecution homosexuals LGBT censorship ban repression government act {P}"),
       ("D5", "{N} decreto programa direitos LGBT homossexuais proteção criação conselho {P}", "{N} decree program LGBT rights homosexuals protection created council {P}")]
with open(S + "/consultas_C18.tsv", "w") as f:
    f.write("gov\tqid\tdescritor\tidioma\tconsulta_exata\n")
    for g, (n, p) in NOME.items():
        k = 0
        for d, pt, en in TPL:
            for idi, tpl in (("pt", pt), ("en", en)):
                k += 1; f.write(f"{g}\tQ{k}\t{d}\t{idi}\t{tpl.format(N=n, P=p)}\n")
ev = list(csv.DictReader(open(S + "/eventos_C18.csv")))
dl = list(csv.DictReader(open(S + "/downloads_C18.tsv"), delimiter="\t"))
lidas = Counter(); falhas = Counter()
ILEGIVEL = {("G1","Q6"),("G2","Q8")}   # repositorio ufsc: Wayback devolveu binario ilegivel (1479 chars de lixo)
for r in dl:
    if r["via"] == "FALHOU" or int(r["chars_texto"]) < 200 or (r["gov"], r["qid"]) in ILEGIVEL: falhas[r["gov"]] += 1
    else: lidas[r["gov"]] += 1
NOMAND = {"G1": (0, 6), "G2": (1, 7), "G3": (6, 10), "G4": (6, 8), "G5": (7, 10), "G6": (3, 10)}   # publicadas no mandato / lidas (data lida na pagina)
SEC = {"G3": "T1b: 1 (secundario)"}
c = defaultdict(Counter)
for e in ev:
    if e["id"] == "E09": continue   # mesmo evento de E08
    t = e["tipo"]; ag = e["agente"]
    key = "T1" if t == "T1" and ag == "governante" else "T1aux" if t == "T1" else t
    c[e["governante_do_mandato"]][key] += 1
cols = ["T1", "T1aux", "T3", "T3?", "T4", "T5/T6", "P"]
with open(S + "/TABELA_C18.md", "w") as f:
    f.write("| governante | consultas | páginas lidas (útil/selec.) | publicadas no mandato | T1 próprio | T1 aux. | T3 | T3? (não soma) | T4 | T5/T6 | P |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    for g in NOME:
        a, b = NOMAND[g]
        f.write(f"| {ROT[g]} | 10 | {lidas[g]}/{lidas[g] + falhas[g]} | {a}/{b} | " + " | ".join(str(c[g][k]) for k in cols) + " |\n")
    tot = {k: sum(c[g][k] for g in NOME) for k in cols}
    f.write("| total | 60 | " + f"{sum(lidas.values())}/{sum(lidas.values()) + sum(falhas.values())}" + " | " + f"{sum(a for a, b in NOMAND.values())}/{sum(b for a, b in NOMAND.values())}" + " | " + " | ".join(str(tot[k]) for k in cols) + " |\n")
print(open(S + "/TABELA_C18.md").read())
