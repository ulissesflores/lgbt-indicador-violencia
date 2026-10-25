"""S10. (4a) Duplicatas e casos fora do criterio na PROPRIA lista GGB 2019 (329). Nomes so em _raw; saida publica = contagens + ids hash.
- mesmo link para varios casos (pode ser evento com varias vitimas: legitimo) ; - nomes quase iguais na mesma cidade/UF ; - nome vazio/iniciais.
Uso: python3.14 -I s10_duplicatas.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, unicodedata, json
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlsplit
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"; F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"
def nz(x): return re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode()).strip()
def nurl(u): p = urlsplit(u.replace(" ", "")); return p.netloc.lower().removeprefix("www.") + p.path.rstrip("/").lower() if u else ""
g = list(csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()))
res = {"n": len(g)}
res["sem_nome_ou_iniciais"] = sum(1 for r in g if not r["nome"].strip() or re.fullmatch(r"([A-ZÁ-Ú]\.?\s?)+(de |da |dos |do )?([A-Z]\.?\s?)*", r["nome"].strip()) is not None)
res["sem_nome"] = sum(1 for r in g if not r["nome"].strip())
grp = {}
for r in g:
    k = nurl(r["link"])
    if k: grp.setdefault(k, []).append(r)
mult = {k: v for k, v in grp.items() if len(v) > 1}
res["links_com_mais_de_um_caso"] = len(mult); res["casos_em_link_compartilhado"] = sum(len(v) for v in mult.values())
res["link_compartilhado_dist"] = {str(n): sum(1 for v in mult.values() if len(v) == n) for n in sorted({len(v) for v in mult.values()})}
pares = []
for i in range(len(g)):
    for j in range(i + 1, len(g)):
        a, b = g[i], g[j]
        if a["uf"] != b["uf"]: continue
        na, nb = nz(a["nome"]), nz(b["nome"])
        if len(na) < 4 or len(nb) < 4: continue
        r = SequenceMatcher(None, na, nb).ratio()
        if r >= 0.85 and nz(a["cidade"])[:5] == nz(b["cidade"])[:5]: pares.append((a, b, round(r, 2)))
res["pares_nome_quase_igual_mesma_uf_cidade"] = len(pares)
(F3/"dados/duplicatas_candidatas_hash.csv").write_text("id_a,id_b,similaridade,mesma_cat,mesmo_link\n" + "".join(f'{a["id"]},{b["id"]},{r},{int(a["cat"]==b["cat"])},{int(bool(a["link"]) and nurl(a["link"])==nurl(b["link"]))}\n' for a, b, r in pares))
(RAW/"duplicatas_candidatas_nominal.txt").write_text("\n".join(f'{a["n"]}|{a["nome"]}|{a["cat"]}|{a["cidade"]}  ~  {b["n"]}|{b["nome"]}|{b["cat"]}|{b["cidade"]}  r={r}' for a, b, r in pares))
cats = {}
for r in g: cats[r["cat"]] = cats.get(r["cat"], 0) + 1
res["por_categoria_ggb"] = cats
# casos cujo mesmo link cobre evento com multiplas vitimas (informativo)
res["exemplo_tamanhos_link_compartilhado"] = sorted([len(v) for v in mult.values()], reverse=True)[:10]
(F3/"dados/duplicatas_resumo.json").write_text(json.dumps(res, ensure_ascii=False, indent=1)); print(json.dumps(res, ensure_ascii=False, indent=1))
print(open(RAW/"duplicatas_candidatas_nominal.txt").read())
