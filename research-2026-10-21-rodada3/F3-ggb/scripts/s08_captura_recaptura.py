"""S08. Cruza a lista GGB 2019 (subconjunto trans/travesti, n=118) com a lista TDoR/TGEU-TMM Brasil 2019 (n=139).
Chaves: (1) URL da fonte (normalizada) igual; (2) UF + cidade + sobreposicao de tokens de nome.
A lista GGB nao traz data; por isso nao ha criterio de data +-3 dias (desvio declarado). Nomes ficam em _raw.
Saida publica: so ids hash + indicadores. Estimador: Chapman (2 listas) + IC normal e log (Chao) sobre N - n_uniao.
Uso: python3.14 -I s08_captura_recaptura.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, unicodedata, random, json
from pathlib import Path
from urllib.parse import urlsplit
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"
F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"
def nz(x): return re.sub(r"[^a-z0-9 ]", " ", unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode())
def nurl(u):
    p = urlsplit(u.strip().rstrip(").,;>\"'")); return (p.netloc.lower().removeprefix("www.") + p.path.rstrip("/").lower())
UF = {"Acre":"AC","Alagoas":"AL","Amapá":"AP","Amazonas":"AM","Bahia":"BA","Ceará":"CE","Distrito Federal":"DF","Espírito Santo":"ES","Goiás":"GO","Maranhão":"MA","Mato Grosso":"MT","Mato Grosso do Sul":"MS","Minas Gerais":"MG","Pará":"PA","Paraíba":"PB","Paraná":"PR","Pernambuco":"PE","Piauí":"PI","Rio de Janeiro":"RJ","Rio Grande do Norte":"RN","Rio Grande do Sul":"RS","Rondônia":"RO","Roraima":"RR","Santa Catarina":"SC","São Paulo":"SP","Sergipe":"SE","Tocantins":"TO"}
PART = {"dos","das","de","da","do","silva","santos","souza","filho","junior","jr"}
def toks(n): return {w for w in nz(n).split() if len(w) >= 3 and w not in PART}
ggb = list(csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()))
trans = [r for r in ggb if r["cat"] in ("Travesti", "Transexual", "Mulher Trans")]
td = list(csv.DictReader((RAW/"tdor/x/tdor_export.csv").open(encoding="utf-8-sig")))
for t in td:
    parts = [p.strip() for p in t["Location"].split(",")]; t["uf"] = UF.get(parts[-1], ""); t["cidade"] = parts[0]
    t["urls"] = {nurl(u) for u in re.findall(r"https?://[^\s)\]>\"']+", t["Description"])}
    t["toks"] = toks(t["Name"]); t["cn"] = nz(t["cidade"]).strip()
for g in trans:
    g["urls"] = {nurl(g["link"])} if g["link"] else set(); g["toks"] = toks(g["nome"]); g["cn"] = nz(g["cidade"]).strip()
pairs = []; usadoT = set()
for g in trans:
    best = None
    for k, t in enumerate(td):
        if g["urls"] & t["urls"]: m = ("url", 3)
        elif g["uf"] == t["uf"] and g["toks"] and t["toks"] and (g["toks"] & t["toks"]) and (g["cn"] == t["cn"] or g["cn"] in t["cn"] or t["cn"] in g["cn"]): m = ("nome+cidade", 2)
        elif g["uf"] == t["uf"] and g["toks"] and t["toks"] and (g["toks"] & t["toks"]) and len(g["toks"] & t["toks"]) >= 2: m = ("nome2tok+uf", 1)
        else: continue
        if best is None or m[1] > best[1][1]: best = (k, m)
    if best: pairs.append((g, best[0], best[1][0]))
# um TDoR casa com no maximo um GGB (preferencia pelo criterio mais forte)
bestT = {}
for g, k, how in pairs:
    sc = {"url": 3, "nome+cidade": 2, "nome2tok+uf": 1}[how]
    if k not in bestT or sc > bestT[k][1]: bestT[k] = (g, sc, how)
matched = {id(v[0]): (k, v[2]) for k, v in bestT.items()}
n1, n2 = len(trans), len(td); m = len(matched)
how_ct = {}
for _, h in matched.values(): how_ct[h] = how_ct.get(h, 0) + 1
chap = (n1 + 1) * (n2 + 1) / (m + 1) - 1
var = (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))
se = var ** 0.5
# conservador: so criterio URL
mu = how_ct.get("url", 0); chap_u = (n1 + 1) * (n2 + 1) / (mu + 1) - 1
# IC: normal (variancia de Seber para Chapman) e logaritmico sobre (N - n_uniao), que evita limite inferior abaixo do observado
n_obs = n1 + n2 - m
import math
d = chap - n_obs; sd_d = se
c = math.exp(1.96 * math.sqrt(math.log(1 + var / d**2))) if d > 0 else 1
lo, hi = n_obs + d / c, n_obs + d * c
res = dict(n_ggb_trans=n1, n_tdor=n2, sobreposicao=m, por_criterio=how_ct, chapman=round(chap, 1), ep=round(se, 1),
           ic95_normal=[round(chap - 1.96 * se, 1), round(chap + 1.96 * se, 1)], ic95_log=[round(lo, 1), round(hi, 1)], n_uniao_observada=n_obs,
           chapman_so_url=round(chap_u, 1), cobertura_ggb_vs_chapman=round(n1 / chap, 3), cobertura_tdor_vs_chapman=round(n2 / chap, 3),
           obs="dependencia positiva entre listas (ambas por midia; TDoR cita as mesmas materias; GGB cita TDoR em alguns casos) => Chapman subestima N")
print(json.dumps(res, ensure_ascii=False, indent=1))
(F3/"dados/captura_recaptura_trans2019.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
# casamentos (hash) e GGB trans sem par; TDoR sem par (so contagens; nomes ficam em _raw)
with (RAW/"cr_pares_nominais.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["id_ggb", "nome_ggb", "nome_tdor", "criterio"])
    for g in trans:
        if id(g) in matched: k, h = matched[id(g)]; w.writerow([g["id"], g["nome"], td[k]["Name"], h])
with (F3/"dados/cr_ggb_trans_hash.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["id_ggb", "uf", "cat", "no_tdor", "criterio"])
    for g in trans: w.writerow([g["id"], g["uf"], g["cat"], int(id(g) in matched), matched.get(id(g), (0, ""))[1]])
# fonte do GGB citando TDoR (dependencia declarada)
cit = [g for g in ggb if "tdor" in g["link"].lower() or "translivesmatter" in g["link"].lower()]
print("casos GGB (todos) cuja fonte e o proprio TDoR:", len(cit), "| desses trans:", sum(1 for g in cit if g["cat"] in ('Travesti','Transexual','Mulher Trans')))
(F3/"dados/captura_recaptura_trans2019.json").write_text(json.dumps({**res, "ggb_fonte_tdor_total": len(cit)}, ensure_ascii=False, indent=1))

# ---- sensibilidade ----
def chapman(a, b, m): 
    N = (a + 1) * (b + 1) / (m + 1) - 1
    v = (a + 1) * (b + 1) * (a - m) * (b - m) / ((m + 1) ** 2 * (m + 2)); return round(N, 1), round(v ** 0.5, 1)
sens = []
def run(nome, gset, tset, crit=None):
    gi = {id(g) for g in gset}; ti = {k for k in tset}
    mm = sum(1 for g in gset if id(g) in matched and matched[id(g)][0] in ti and (crit is None or crit(g, matched[id(g)])))
    N, e = chapman(len(gset), len(ti), mm); sens.append(dict(cenario=nome, n_ggb=len(gset), n_tdor=len(ti), m=mm, chapman=N, ep=e, cob_ggb=round(len(gset) / N, 3)))
allT = set(range(len(td)))
run("base: GGB trans x TDoR todos (URL ou nome+cidade ou nome 2 tokens+UF)", trans, allT)
def forte(g, mt): k, h = mt; return h == "url" or len(g["toks"] & td[k]["toks"]) >= 2
run("estrito: so URL ou >=2 tokens de nome", trans, allT, forte)
run("TDoR so categorias violence+suicide", trans, {k for k, t in enumerate(td) if t["Category"] in ("violence", "suicide")})
run("TDoR so violence (sem suicidio)", trans, {k for k, t in enumerate(td) if t["Category"] == "violence"})
sem_tdor = [g for g in trans if "tdor" not in g["link"].lower()]
run("GGB sem os casos cuja fonte e o proprio TDoR", sem_tdor, allT)
nomeados = {k for k, t in enumerate(td) if not t["Name"].startswith("Name Unknown")}
gn = [g for g in trans if g["toks"]]
run("so casos com nome nas duas listas", gn, nomeados)
(F3/"dados/captura_recaptura_sensibilidade.json").write_text(json.dumps(sens, ensure_ascii=False, indent=1))
for s_ in sens: print(s_)
