"""S11. Resultados da auditoria de validacao por amostra (GGB 2019, n=160 de N=329, AAS semente 20261021).
Le: amostra.csv, fonte_checks.csv, fetch_log.csv, ggb2019_universo_hash.csv, codificacao_A_raw.txt, (opcional) codificacao_B.json.
Gera: codificacao_A.csv (planilha de codificacao, ids hash), resultados.csv, validacao_resumo.json, kappa.json.
Uso: python3.14 -I s11_validacao.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, json, math
from collections import Counter
from pathlib import Path
ROOT = Path(REPO_ROOT); F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"; D = F3/"dados"; RAW = ROOT/"fontes/p3-ggb/_raw"
def wilson(k, n, z=1.959964):
    if n == 0: return (float("nan"),) * 2
    p = k/n; d = 1 + z*z/n; c = p + z*z/(2*n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)); return ((c-h)/d, (c+h)/d)
amo = list(csv.DictReader((D/"amostra.csv").open())); N = 329
uni = {r["id"]: r for r in csv.DictReader((D/"ggb2019_universo_hash.csv").open())}
chk = {r["id"]: r for r in csv.DictReader((D/"fonte_checks.csv").open())}
flog = {r["id"]: r for r in csv.DictReader((D/"fetch_log.csv").open())}
cod = {}
for l in open(D/"codificacao_A_raw.txt"):
    if not l[:1].isdigit(): continue
    p = l.rstrip("\n").split("|"); cod[p[0]] = dict(zip(["ordem","corresp","morte","tipo","lgbt","base","motivo","desfecho","tipo_fonte","obs"], p))
def nr_motivo(i):
    u, f = uni[i], flog[i]
    if u["fonte_tipo"] != "link": return "sem_link_no_anexo4"
    via = f["via"]; st = f["status"]
    if "HTTPError:404" in st: return "link_morto_404"
    if "URLError" in st: return "dominio_inacessivel"
    if "HTTPError:403" in st or "HTTPError:5" in st: return "bloqueio_ou_erro_servidor"
    return "outro"
rows = []
for r in amo:
    i = r["id"]; k = r["ordem_sorteio"]; c = cod.get(k)
    d = dict(ordem=k, id=i, uf=uni[i]["uf"], cat_ggb=uni[i]["cat_ggb"], dominio=uni[i]["dominio"], dupla=r["dupla_codificacao"])
    if c is None:
        d.update(fonte="NR", motivo_nr=nr_motivo(i), corresp="", morte="", tipo="", lgbt="", base="", motivo="", desfecho="", tipo_fonte="", obs="")
    else:
        d.update(fonte="R", motivo_nr="", **{x: c[x] for x in ["corresp","morte","tipo","lgbt","base","motivo","desfecho","tipo_fonte","obs"]})
    rows.append(d)
with (D/"codificacao_A.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
n = len(rows); rec = [d for d in rows if d["fonte"] == "R"]; nr = [d for d in rows if d["fonte"] == "NR"]
use = [d for d in rec if d["corresp"] in ("S", "P")]; useS = [d for d in rec if d["corresp"] == "S"]
mviol = [d for d in use if d["morte"] == "S"]
Vstr = [d for d in mviol if d["lgbt"] == "S"]; Vlar = [d for d in mviol if d["lgbt"] in ("S", "I")]
VstrS = [d for d in useS if d["morte"] == "S" and d["lgbt"] == "S"]
res = []
def add(nome, k, den, den_nome, obs=""):
    lo, hi = wilson(k, den); res.append(dict(medida=nome, k=k, n=den, denominador=den_nome, proporcao=round(k/den, 4) if den else "", ic95_wilson_inf=round(lo, 4), ic95_wilson_sup=round(hi, 4), obs=obs))
add("fonte citada recuperada (pagina existe e foi lida)", len(rec), n, "amostra (160)")
add("fonte recuperada que NAO e a materia do caso (home/404/suspensa/login/spam)", sum(1 for d in rec if d["corresp"] in ("N", "X")), len(rec), "fonte recuperada")
add("materia corresponde ao caso (S ou P) ", len(use), n, "amostra (160)")
add("materia corresponde ao caso (S ou P)", len(use), len(rec), "fonte recuperada")
add("morte violenta confirmada pela fonte (S)", len(mviol), len(use), "materia que corresponde", "inclui homicidio, latrocinio, suicidio")
add("morte violenta indeterminada ou nao violenta (I/N)", sum(1 for d in use if d["morte"] in ("I", "N")), len(use), "materia que corresponde")
add("VERIFICAVEL ESTRITO: corresponde + morte violenta + LGBT+ explicito na fonte", len(Vstr), n, "amostra (160)", "piso: trata nao-recuperada como nao verificada")
add("VERIFICAVEL ESTRITO", len(Vstr), len(rec), "fonte recuperada")
add("VERIFICAVEL ESTRITO", len(Vstr), len(use), "materia que corresponde", "condicional a fonte ser a materia do caso")
add("VERIFICAVEL LARGO (LGBT+ explicito ou indicio)", len(Vlar), len(use), "materia que corresponde")
add("VERIFICAVEL ESTRITO so com correspondencia S (nome ou alcunha confere)", len(VstrS), len(useS), "materia com correspondencia S")
add("LGBT+ NAO mencionado na fonte citada (materia corresponde e morte violenta)", sum(1 for d in mviol if d["lgbt"] == "N"), len(mviol), "morte violenta confirmada", "ausencia na fonte citada nao prova que a vitima nao fosse LGBT+")
add("morte violenta + LGBT+ explicito, fonte unica = noticia (exclui memorial/rede)", sum(1 for d in Vstr if d["tipo_fonte"] == "noticia"), len(use), "materia que corresponde")
# limites de Manski para o verificavel estrito sobre n=160
res.append(dict(medida="LIMITES (pior/melhor caso) do verificavel estrito sobre 160", k="", n=n, denominador="amostra (160)", proporcao="", ic95_wilson_inf=round(len(Vstr)/n, 4), ic95_wilson_sup=round((len(Vstr)+len(nr))/n, 4), obs="inf: nao-recuperadas = nao verificadas; sup: todas verificariam"))
# extrapolacao para o universo (so condicional, com FPC): total verificavel estrito projetado = N * (p_cond) * (usable/rec)... nao fazer; reportar separadamente
tab = Counter(d["motivo"] for d in Vstr); tab_all = Counter(d["motivo"] for d in mviol)
tip = Counter(d["tipo"] for d in mviol)
base = Counter(d["base"] for d in Vstr)
des = Counter(d["desfecho"] for d in mviol)
cat = Counter(d["cat_ggb"] for d in Vstr); catuse = Counter(d["cat_ggb"] for d in use)
nrm = Counter(d["motivo_nr"] for d in nr)
fpc = math.sqrt((N - n)/(N - 1))
resumo = dict(n_amostra=n, N_universo=N, fracao_amostral=round(n/N, 3), fpc=round(fpc, 3), recuperadas=len(rec), nao_recuperadas=len(nr), motivo_nao_recuperacao=dict(nrm),
              correspondem=len(use), correspondencia_S=len(useS), morte_violenta=len(mviol), verificavel_estrito=len(Vstr), verificavel_largo=len(Vlar),
              motivo_entre_verificavel_estrito=dict(tab), motivo_entre_morte_violenta_confirmada=dict(tab_all), tipo_entre_morte_violenta=dict(tip),
              base_identificacao_entre_verificavel_estrito=dict(base), desfecho_entre_morte_violenta=dict(des), cat_ggb_entre_verificavel_estrito=dict(cat), cat_ggb_entre_correspondem=dict(catuse),
              tipo_fonte_entre_recuperadas=dict(Counter(d["tipo_fonte"] for d in rec)), dominios_nao_recuperadas_top=Counter(d["dominio"] for d in nr).most_common(8),
              divergencia_categoria_ou_cidade=sum(1 for d in rec if "DIVERGE" in d["obs"]))
# tabela de motivos com Wilson (entre morte violenta confirmada, materia que corresponde)
mot_names = {"V": "LGBTfobia atribuida por alguem na fonte", "R": "roubo/latrocinio", "C": "conflito interpessoal", "P": "passional/ciumes/ex-parceiro", "S": "suicidio", "U": "motivo desconhecido/nao reportado"}
mt = []
for m, nm in mot_names.items():
    k = tab_all.get(m, 0); lo, hi = wilson(k, len(mviol)); mt.append(dict(motivo=nm, codigo=m, k=k, n=len(mviol), proporcao=round(k/len(mviol), 4), ic95_inf=round(lo, 4), ic95_sup=round(hi, 4)))
with (D/"tabela_motivos.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(mt[0].keys())); w.writeheader(); w.writerows(mt)
with (D/"resultados.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
(D/"validacao_resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1))
print(json.dumps(resumo, ensure_ascii=False, indent=1))
for r in res: print(r["proporcao"], f'{r["k"]}/{r["n"]}', r["ic95_wilson_inf"], r["ic95_wilson_sup"], "|", r["medida"], "|", r["denominador"])
for m in mt: print(m)
# ---- kappa (dupla codificacao cega por outra familia de modelo) ----
bf = RAW/"saida_B.txt"
if bf.exists():
    B = {x["caso"]: x for x in json.load(bf.open())}
    A = {d["ordem"]: d for d in rows if d["fonte"] == "R"}
    ks = [k for k in B if k in A]
    def kappa(a, b):
        n_ = len(a); cats = sorted(set(a) | set(b)); po = sum(1 for x, y in zip(a, b) if x == y)/n_
        pe = sum((a.count(c)/n_)*(b.count(c)/n_) for c in cats); return (po, (po-pe)/(1-pe) if pe < 1 else float("nan"))
    out = {"n_casos_dupla": len(ks)}
    for v in ["corresp", "morte", "tipo", "lgbt", "base", "motivo", "desfecho"]:
        if v == "corresp": a = [A[k][v] for k in ks]; b = [B[k][v] for k in ks]
        else:
            kk = [k for k in ks if A[k]["corresp"] in ("S", "P") and B[k]["corresp"] in ("S", "P")]; a = [A[k][v] for k in kk]; b = [B[k][v] for k in kk]
        po, kp = kappa(a, b); out[v] = dict(n=len(a), concordancia=round(po, 3), kappa=round(kp, 3))
    # desacordos (sem nomes)
    out["desacordos"] = [dict(caso=k, **{v: (A[k][v], B[k][v]) for v in ["corresp", "morte", "lgbt", "motivo"] if A[k][v] != B[k][v]}) for k in ks if any(A[k][v] != B[k][v] for v in ["corresp", "morte", "lgbt", "motivo"])]
    (D/"kappa.json").write_text(json.dumps(out, ensure_ascii=False, indent=1)); print(json.dumps(out, ensure_ascii=False, indent=1))
