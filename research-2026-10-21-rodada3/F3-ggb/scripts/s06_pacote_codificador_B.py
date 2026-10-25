"""S06. Monta o pacote cego para o 2o codificador (outra familia de modelo): os casos da subamostra de dupla
codificacao que tem fonte recuperada. Nome da vitima trocado por [VITIMA]. Pacote em _raw (fora do git).
Uso: python3.14 -I s06_pacote_codificador_B.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, json, unicodedata
from pathlib import Path
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"
F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"
nom = {r["id"]: r for r in csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open())}
amo = list(csv.DictReader((F3/"dados/amostra.csv").open()))
cod = {l.split("|")[0] for l in open(F3/"dados/codificacao_A_raw.txt") if l[:1].isdigit()}
def nz(x): return unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode()
casos = []
for r in amo:
    if r["dupla_codificacao"] != "1" or r["ordem_sorteio"] not in cod: continue
    n = nom[r["id"]]; t = re.sub(r"\s+", " ", (RAW/"news_txt"/f'{r["id"]}.txt').read_text()); tn = nz(t)
    toks = [w for w in nz(n["nome"]).replace("/", " ").split() if len(w) >= 4 and w not in ("silva", "santos", "souza", "filho", "junior")]
    pos = [tn.find(w) for w in toks if tn.find(w) >= 0]
    i = max(0, min(pos) - 200) if pos else 0
    jan = t[i:i+3500]
    for w in toks: jan = re.sub(re.escape(w), "[VITIMA]", jan, flags=re.I)
    casos.append(dict(caso=r["ordem_sorteio"], categoria_ggb=n["cat"], cidade_uf=f'{n["cidade"]}/{n["uf"]}', titulo=t.split("\n")[0][:160], texto=jan))
(RAW/"pacote_B.json").write_text(json.dumps(casos, ensure_ascii=False, indent=1))
print(len(casos), "casos; chars:", sum(len(c["texto"]) for c in casos))
