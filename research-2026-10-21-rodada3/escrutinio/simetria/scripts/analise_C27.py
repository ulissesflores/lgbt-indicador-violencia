"""C27 passo 3 (so aqui o rotulo original e lido): kappa de Cohen por campo e estrato, IC95% bootstrap (2000, semente 20261023),
matrizes de confusao, PABAK, Gwet AC1, recontagem do x/49 e linha de base. Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, json, math, random
from collections import Counter
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
M = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia")
orig = {(r["hash"], r["familia"], r["universo"]): r for r in csv.DictReader(open(M + "/amostra_codificada.csv"))}
seg = json.load(open(OUT + "/codif_segundo_itens.json"))["codificacao"]
itens = [json.loads(l) for l in open(OUT + "/itens_C27.jsonl")]
rows = []
for i in itens:
    o = orig[(i["hash"], i["familia"], i["universo"])]; s = seg[i["id"]]
    rows.append(dict(id=i["id"], estrato=i["estrato"], familia=i["familia"], universo=i["universo"], hash=i["hash"],
                     o_postura=o["postura"], s_postura=s["postura"], o_forma=o["forma"], s_forma=s["forma"],
                     o_fonte=o["fonte_citada"], s_fonte=s["fonte_citada"], s_nome=s["fonte_nomeada"], o_nome=o["fonte_nomeada"],
                     **{f"o_{k}": o[k] for k in ("cita_GGB", "cita_ANTRA", "cita_TGEU", "cita_ONU")},
                     **{f"s_{k}": str(s[k]) for k in ("cita_GGB", "cita_ANTRA", "cita_TGEU", "cita_ONU")}))
with open(OUT + "/itens_cruzados_C27.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def kappa(a, b):
    n = len(a)
    if n == 0: return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    if pe >= 1 - 1e-12: return None
    return (po - pe) / (1 - pe)
def pabak(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; k = len(set(a) | set(b))
    return (k * po - 1) / (k - 1) if k > 1 else None
def ac1(a, b):
    n = len(a); cats = sorted(set(a) | set(b)); q = len(cats)
    if q < 2: return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pi = {c: (a.count(c) + b.count(c)) / (2 * n) for c in cats}
    pe = sum(pi[c] * (1 - pi[c]) for c in cats) / (q - 1)
    return (po - pe) / (1 - pe) if pe < 1 else None
rng = random.Random(20261023)
def boot(a, b, B=2000):
    n = len(a); ks = []; ind = 0
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        k = kappa([a[i] for i in idx], [b[i] for i in idx])
        if k is None: ind += 1
        else: ks.append(k)
    ks.sort()
    if len(ks) < 100: return None, None, ind
    return ks[int(0.025 * len(ks))], ks[int(0.975 * len(ks)) - 1], ind
def f(x): return "indef." if x is None else f"{x:.2f}"
ESTR = {"F2-Parlamento": lambda r: r["estrato"] == "F2-Parlamento", "F3-Parlamento": lambda r: r["estrato"] == "F3-Parlamento",
        "Parlamento (F2+F3)": lambda r: r["estrato"] in ("F2-Parlamento", "F3-Parlamento"), "Outras-100": lambda r: r["estrato"] == "Outras-100", "Tudo-216": lambda r: True}
AF = ("AFIRMA", "ATRIBUI")
CAMPOS = [("postura (todos)", lambda r: True, "postura"),
          ("fonte_citada (a: todos)", lambda r: True, "fonte"),
          ("fonte_citada (b: ambos AFIRMA/ATRIBUI)", lambda r: r["o_postura"] in AF and r["s_postura"] in AF, "fonte"),
          ("forma (primaria: ambos != FORA)", lambda r: r["o_postura"] != "FORA" and r["s_postura"] != "FORA", "forma"),
          ("forma (sensibilidade: todos, vazio=categoria)", lambda r: True, "forma")]
res = []; conf = {}
for en, ef in ESTR.items():
    base = [r for r in rows if ef(r)]
    for cn, cf, campo in CAMPOS:
        sub = [r for r in base if cf(r)]
        a = [r["o_" + campo] for r in sub]; b = [r["s_" + campo] for r in sub]
        n = len(sub)
        if n == 0: res.append([en, cn, 0, "", "", "", "", "", "", "", "", ""]); continue
        k = kappa(a, b); lo, hi, ind = boot(a, b) if k is not None else (None, None, 0)
        degenerada = (len(set(a)) == 1) or (len(set(b)) == 1)
        concord = sum(x == y for x, y in zip(a, b)) / n
        res.append([en, cn, n, f"{concord:.3f}", f(k), f(lo), f(hi), ind, f(pabak(a, b)), f(ac1(a, b)), "SIM" if degenerada else "nao", len(set(a) | set(b))])
        conf[(en, cn)] = Counter(zip(a, b))
with open(OUT + "/concordancia_C27.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["estrato", "campo", "n", "concordancia", "kappa", "IC95_lo", "IC95_hi", "replicas_indefinidas_de_2000", "PABAK", "Gwet_AC1", "marginal_degenerada_em_um_codificador", "n_categorias"]); w.writerows(res)
# cita_* (concordancia simples)
with open(OUT + "/cita_entes_C27.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["estrato", "ente", "n", "concordancia", "n_orig_1", "n_seg_1"])
    for en, ef in ESTR.items():
        base = [r for r in rows if ef(r)]
        for k in ("cita_GGB", "cita_ANTRA", "cita_TGEU", "cita_ONU"):
            a = [r["o_" + k] for r in base]; b = [r["s_" + k] for r in base]
            w.writerow([en, k, len(base), f"{sum(x == y for x, y in zip(a, b)) / len(base):.3f}", a.count("1"), b.count("1")])
# matrizes
with open(OUT + "/matrizes_confusao_C27.md", "w") as fh:
    for (en, cn), c in conf.items():
        if en not in ("Parlamento (F2+F3)", "F2-Parlamento", "F3-Parlamento", "Outras-100"): continue
        if "sensibilidade" in cn or "(a:" in cn and en != "Parlamento (F2+F3)": continue
        la = sorted({a for a, b in c}); lb = sorted({b for a, b in c})
        fh.write(f"\n### {en} | {cn} (linhas = original/Claude, colunas = segundo/Grok)\n\n| orig \\ seg | " + " | ".join(x or "(vazio)" for x in lb) + " |\n|---|" + "---|" * len(lb) + "\n")
        for x in la: fh.write(f"| {x or '(vazio)'} | " + " | ".join(str(c.get((x, y), 0)) for y in lb) + " |\n")
# recontagem x/49
def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)
out = []
for en in ("F2-Parlamento", "F3-Parlamento", "Outras-100"):
    sub = [r for r in rows if r["estrato"] == en]
    for quem, p, fo in (("original(Claude)", "o_postura", "o_fonte"), ("segundo(Grok)", "s_postura", "s_fonte")):
        den = [r for r in sub if r[p] in AF]; num = [r for r in den if r[fo] == "primaria_verificavel"]
        anyf = [r for r in den if r[fo] != "nenhuma"]
        lo, hi = wilson(len(num), len(den))
        out.append([en, quem, len(sub), len(den), len(num), f(lo) if lo is not None else "", f(hi) if hi is not None else "", len(anyf), dict(Counter(r[fo] for r in den))])
# itens em que o segundo achou primaria_verificavel
prim = [r for r in rows if r["s_fonte"] == "primaria_verificavel" or r["o_fonte"] == "primaria_verificavel"]
with open(OUT + "/recontagem_x49_C27.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["estrato", "codificador", "n_itens", "n_AFIRMA+ATRIBUI", "n_primaria_verificavel", "Wilson_lo", "Wilson_hi", "n_com_alguma_fonte", "distribuicao_fonte_nos_AFIRMA+ATRIBUI"]); w.writerows(out)
with open(OUT + "/itens_com_primaria_C27.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["id", "estrato", "familia", "universo", "o_postura", "s_postura", "o_fonte", "s_fonte", "s_fonte_nomeada"])
    for r in prim: w.writerow([r["id"], r["estrato"], r["familia"], r["universo"], r["o_postura"], r["s_postura"], r["o_fonte"], r["s_fonte"], r["s_nome"]])
# linha de base
sb = json.load(open(OUT + "/codif_segundo_base.json"))["codificacao"]
import hashlib
bl = [json.loads(l) for l in open(OUT + "/baseline_itens.jsonl")]
bro = []
for r in bl:
    i = hashlib.sha256(r["id"].encode()).hexdigest()[:12]; s = sb[i]
    bro.append(dict(id=i, data=r["data"], postura=s["postura"], fonte=s["fonte_citada"], nome=s["fonte_nomeada"], trecho=r["trecho"]))
with open(OUT + "/baseline_resultado_C27.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(bro[0])); w.writeheader(); w.writerows(bro)
den = [r for r in bro if r["postura"] in AF]; num = [r for r in den if r["fonte"] == "primaria_verificavel"]; anyf = [r for r in den if r["fonte"] != "nenhuma"]
lo, hi = wilson(len(num), len(den))
summ = {"baseline_n": len(bro), "postura": dict(Counter(r["postura"] for r in bro)), "den_AFIRMA+ATRIBUI": len(den), "primaria_verificavel": len(num),
        "wilson95": [lo, hi], "alguma_fonte": len(anyf), "fonte_dist_den": dict(Counter(r["fonte"] for r in den))}
sb2 = [r for r in rows if r["estrato"] == "F2-Parlamento" and r["s_postura"] in AF]
n2 = len(sb2); k2 = sum(r["s_fonte"] == "primaria_verificavel" for r in sb2)
summ["F2_parlamento_segundo"] = {"den": n2, "primaria": k2, "alguma_fonte": sum(r["s_fonte"] != "nenhuma" for r in sb2), "wilson95": wilson(k2, n2)}
json.dump(summ, open(OUT + "/baseline_resumo_C27.json", "w"), ensure_ascii=False, indent=1)
print(open(OUT + "/concordancia_C27.csv").read()); print(json.dumps(summ, ensure_ascii=False, indent=1))
for o in out: print(o)
