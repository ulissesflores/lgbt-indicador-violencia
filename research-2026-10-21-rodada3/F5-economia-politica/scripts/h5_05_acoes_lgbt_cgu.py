"""H5: varre TODAS as ações dos arquivos anuais da CGU (OrcamentoDespesa 2014-2025, zips baixados por h5_01 em dados/raw/orcamento; hashes em dados/h5_orcamento_hashes_tudo.txt) por nome de ação LGBT/homofobia/vitimização/etc.
Saída: dados/h5_acoes_lgbt_cgu_2014_2025.csv. Rodar: /opt/homebrew/bin/python3.14 -I scripts/h5_05_acoes_lgbt_cgu.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, io, re, unicodedata, zipfile, collections
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
import os
SC = os.environ.get("F5_CACHE", f"{B}/dados/raw/orcamento")  # zips ficam na pasta do projeto (*.zip está no .gitignore); sobrevivem à sessão
sem = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().upper()
PAT = re.compile(r"LGBT|HOMOSSEX|HOMOFOB|DIVERSIDADE SEXUAL|TRAVEST|TRANSEXUAL|VITIMIZ|DISQUE|DISCRIMINA|CRIMES? DE ODIO")
res = collections.defaultdict(float); linhas = 0
for ano in range(2014, 2026):
    with zipfile.ZipFile(f"{SC}/od{ano}.zip") as z:
        rd = csv.reader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="latin-1"), delimiter=";"); ix = {c: i for i, c in enumerate(next(rd))}
        for r in rd:
            linhas += 1; a = sem(r[ix["NOME AÇÃO"]])
            if PAT.search(a): res[(ano, r[ix["CÓDIGO AÇÃO"]], r[ix["NOME AÇÃO"]], r[ix["NOME UNIDADE ORÇAMENTÁRIA"]])] += float(r[ix["ORÇAMENTO EMPENHADO (R$)"]].replace(".", "").replace(",", ".") or 0)
with open(f"{B}/dados/h5_acoes_lgbt_cgu_2014_2025.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano", "acao_cod", "acao", "uo", "empenhado_nominal"])
    for k, v in sorted(res.items()): w.writerow(list(k) + [round(v, 2)])
print(linhas, "linhas varridas;", len(res), "combinacoes ano-ação-UO com acerto")
