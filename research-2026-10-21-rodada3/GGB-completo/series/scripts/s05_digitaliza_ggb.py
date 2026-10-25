"""Digitaliza o Grafico 1 do relatorio GGB 2020 (mortes de LGBTI+ por ano, 1990-2020; p. 9 do PDF), que NAO traz rotulos de dados.
Metodo: pdftocairo -svg da p. 9; lê os 31 marcadores vermelhos (cx,cy em pontos); calibra y -> valor por regressao linear contra 2010-2020, anos cujos valores
sao os da Tabela do GGB 2019/2020 (260,266,338,314,329,319,343,445,420,329,237). Erro de calibracao (max |residuo|) e gravado. Sem numpy.
Saida: ../dados_ggb_1990_1999_digitalizado.csv (todos os anos 1990-2020, com tabela 2019 quando existe)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import re, subprocess, csv, pathlib, tempfile, hashlib
PDF = (REPO_ROOT + "/fontes/p3-ggb/_raw/pdf/ggb2020.pdf")
OUT = pathlib.Path(__file__).resolve().parent.parent / "dados_ggb_1990_1999_digitalizado.csv"
with tempfile.TemporaryDirectory() as td:
    svg = f"{td}/p9.svg"; subprocess.run(["pdftocairo", "-svg", "-f", "9", "-l", "9", PDF, svg], check=True)
    s = open(svg).read()
pts = []
for m in re.finditer(r'<path[^>]*stroke="rgb\(100%, 0%, 0%\)"[^>]*transform="matrix\(([^)]*)\)"', s):
    a = [float(x) for x in m.group(1).split(",")]; pts.append((a[4], a[5]))
leg = max(pts, key=lambda p: p[1]); pts.remove(leg); pts.sort()  # remove marcador da legenda
assert len(pts) == 31, len(pts)
cal = {2010:260,2011:266,2012:338,2013:314,2014:329,2015:319,2016:343,2017:445,2018:420,2019:329,2020:237}
xs = [pts[y-1990][1] for y in cal]; vs = list(cal.values()); n = len(xs); mx, mv = sum(xs)/n, sum(vs)/n
k = sum((x-mx)*(v-mv) for x, v in zip(xs, vs)) / sum((x-mx)**2 for x in xs); b = mv - k*mx
maxres = max(abs(v-(k*x+b)) for x, v in zip(xs, vs))
tab = {2000:130,2001:132,2002:126,2003:125,2004:158,2005:135,2006:112,2007:142,2008:187,2009:199}
with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano", "valor_digitalizado", "valor_tabela_ggb2019", "diferenca", "erro_calibracao_max", "sha256_pdf"])
    sha = hashlib.sha256(open(PDF, "rb").read()).hexdigest()
    for i, (x, y) in enumerate(pts):
        a = 1990 + i; v = round(k*y + b); t = tab.get(a, "")
        w.writerow([a, v, t, (v - t) if t != "" else "", round(maxres, 2), sha])
print("residuo max (anos de calibracao):", round(maxres, 2))
