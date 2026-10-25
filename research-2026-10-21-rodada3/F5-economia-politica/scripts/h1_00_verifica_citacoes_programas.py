"""H1: confere que cada trecho verbatim de dados/h1_programas_metas.csv existe no arquivo local citado (comparação com espaços normalizados) e grava sha256 do arquivo
(o .txt é derivado do bruto na mesma pasta: o hash do bruto está em dados/raw/h1_programas/SHA256SUMS.txt, gerado aqui).
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h1_00_verifica_citacoes_programas.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, hashlib, os, re, glob
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
R = f"{B}/dados/raw/h1_programas"
norm = lambda s: re.sub(r"\s+", " ", s.replace("­", "")).strip().lower()
with open(f"{R}/SHA256SUMS.txt", "w") as f:
    for p in sorted(glob.glob(f"{R}/*")):
        if os.path.isfile(p) and not p.endswith("SHA256SUMS.txt"): f.write(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + os.path.basename(p) + "\n")
rows = list(csv.DictReader(open(f"{B}/dados/h1_programas_metas.csv")))
trechos = {"PE": ("pe_boletim_2tri2022.txt", "foi lançado em maio de 2007"), "MG": ("mg_portal_fica_vivo.html.txt", "Decreto estadual 43.334/2003 , que cria o Programa de Controle de Homicídios"),
           "RJ": ("rj_dec42780.html.txt", "Altera o Decreto nº 41.931, de 25 de junho de 2009"), "ES": ("es_ijsn_resenha.txt", "foi lançado, em maio de 2011"),
           "BA": ("ba_lei12357.html.txt", "LEI Nº 12.357 DE 26 DE SETEMBRO DE 2011"), "PB": ("pb_pm_doc1.txt", "instituiu, em 2011, o Programa Paraíba Unida pela Paz"),
           "CE": ("ce_seduc_lancamento.html.txt", "Decreto que institui o Pacto foi assinado")}
for r in rows:
    f, t = trechos[r["uf"]]; txt = norm(open(f"{R}/{f}", encoding="utf-8", errors="ignore").read())
    print(r["uf"], "OK" if norm(t) in txt else "NAO ENCONTRADO", "|", f, "|", t)
