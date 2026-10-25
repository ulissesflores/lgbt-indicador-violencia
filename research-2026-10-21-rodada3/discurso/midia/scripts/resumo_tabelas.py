"""Tabelas de resumo para MIDIA.md (lê contagens.csv, _parlamento_matches.jsonl, _v1prereg_parlamento.csv)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, json, sys
from collections import defaultdict, Counter
B = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia")
rows = list(csv.DictReader(open(B + "/contagens.csv")))
anos = [str(a) for a in range(2015, 2027)]
def get(fam, uni, cons_prefix):
    d = {}
    for r in rows:
        if r["familia"] == fam and r["universo"] == uni and r["consulta"].startswith(cons_prefix):
            d[r["ano"]] = int(r["n"])
    return d
print("== PARLAMENTO v2 (Camara+Senado) uniao familia por ano; denominador = discursos")
tot = defaultdict(int)
for r in rows:
    if r["familia"] == "TOTAL" and r["universo"] in ("Camara", "Senado"):
        tot[r["ano"]] += int(r["n"])
print("ano|" + "|".join(anos)); print("TOTAL discursos|" + "|".join(str(tot[a]) for a in anos))
for fam in ("F1", "F2", "F3", "F4"):
    c = defaultdict(int)
    for r in rows:
        if r["familia"] == fam and r["universo"] in ("Camara", "Senado") and r["consulta"].endswith("-any (uniao das entradas PT)"):
            c[r["ano"]] += int(r["n"])
    print(fam + "|" + "|".join(str(c[a]) for a in anos) + "|soma " + str(sum(c.values())))
print("== PARLAMENTO v1 literal (pre-registro)")
for fam in ("F1", "F2", "F3", "F4"):
    c = defaultdict(int)
    for r in rows:
        if r["familia"] == fam and r["universo"].endswith("(v1 literal)") and r["consulta"].endswith("-any (uniao das entradas PT)"):
            c[r["ano"]] += int(r["n"])
    print(fam + "|" + "|".join(str(c[a]) for a in anos) + "|soma " + str(sum(c.values())))
print("== PARLAMENTO v2 por entrada (soma anos)")
pe = defaultdict(int)
for r in rows:
    if r["universo"] in ("Camara", "Senado") and r["familia"] in ("F1", "F2", "F3", "F4") and not r["consulta"].endswith("-any (uniao das entradas PT)"):
        pe[r["consulta"]] += int(r["n"])
print(dict(sorted(pe.items())))
print("== co-mencao de fonte nos discursos casados (v2, census)")
fam_fonte = defaultdict(Counter); fam_n = Counter()
for l in open(B + "/_parlamento_matches.jsonl"):
    j = json.loads(l)
    for f in j["familias"]:
        fam_n[f] += 1
        for s in j["fontes"]:
            fam_fonte[f][s] += 1
        if any(s in j["fontes"] for s in ("GGB", "ANTRA", "TGEU", "ONU")): fam_fonte[f]["GGB/ANTRA/TGEU/ONU"] += 1
for f in sorted(fam_n): print(f, fam_n[f], dict(fam_fonte[f]))
print("== GN-RSS (piso) por familia e grupo, uniao deduplicada por link")
for fam in ("F1", "F2", "F3", "F4"):
    for u in ("GNRSS-pt", "GNRSS-mundo"):
        d = {r["ano"]: int(r["n"]) for r in rows if r["familia"] == fam and r["universo"] == u and r["consulta"].startswith(fam + "-any")}
        print(fam, u, "|".join(str(d.get(a, 0)) for a in anos), "soma", sum(d.values()))
print("== OpenAlex uniao por ano (title+abstract)")
for fam in ("F1", "F2", "F3", "F4"):
    d = {r["ano"]: int(r["n"]) for r in rows if r["familia"] == fam and r["universo"] == "OpenAlex" and r["consulta"].startswith(fam + "-any")}
    print(fam, "|".join(str(d.get(a, 0)) for a in anos), "total", d.get("total"))
print("== OpenAlex por consulta (total)")
for r in rows:
    if r["universo"] == "OpenAlex" and r["ano"] == "total" and r["consulta"].startswith("OA-"):
        print(r["consulta"][:9], r["n"])
print("== Wikipedia")
for r in rows:
    if r["universo"].startswith("Wikipedia"): print(r["universo"], r["consulta"].split("|")[0], r["n"])

print("== ESTIMATIVA: itens que AFIRMAM ou ATRIBUEM a alegacao (AFIRMA+ATRIBUI) = N_universo x p_amostral (IC95 Wilson)")
import math
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; den = 1 + z*z/n; c = (p + z*z/(2*n))/den
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return max(0, c-h), min(1, c+h)
N = {("F1","Parlamento"):14,("F2","Parlamento"):56,("F3","Parlamento"):148,("F4","Parlamento"):2,
     ("F1","GNRSS-pt"):145,("F2","GNRSS-pt"):1005,("F3","GNRSS-pt"):566,("F4","GNRSS-pt"):140,
     ("F1","GNRSS-mundo"):691,("F2","GNRSS-mundo"):164,("F3","GNRSS-mundo"):361,("F4","GNRSS-mundo"):10,
     ("F1","OpenAlex"):5535,("F2","OpenAlex"):270,("F3","OpenAlex"):622,("F4","OpenAlex"):369,
     ("F2","Wikipedia"):9,("F3","Wikipedia"):197}
cod = list(csv.DictReader(open(B + "/amostra_codificada.csv")))
agg = defaultdict(Counter)
for r in cod:
    agg[(r["familia"], r["universo"])][r["postura"]] += 1
print("familia|universo|N|n_amostra|AFIRMA+ATRIBUI|p[IC95]|N_estimado[IC95]|NEGA/CRITICA|MENCIONA")
for k in sorted(agg):
    c = agg[k]; n = sum(c.values()); aa = c["AFIRMA"] + c["ATRIBUI"]; lo, hi = wilson(aa, n); Nn = N.get(k)
    est = f"{round(Nn*aa/n)} [{round(Nn*lo)}-{round(Nn*hi)}]" if Nn else "?"
    print(f"{k[0]}|{k[1]}|{Nn}|{n}|{aa}|{aa/n:.2f} [{lo:.2f}-{hi:.2f}]|{est}|{c['NEGA/CRITICA']}|{c['MENCIONA']}")
