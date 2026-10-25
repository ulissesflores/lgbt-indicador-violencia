"""C10 (frente E) — EXPOSIÇÃO POR GOVERNO, federal (E1) e estadual (E2). DESCRITIVO: nenhum número aqui é efeito causal do governo.
Pré-registro: PREREGISTRO-C10.md (corpo com sha256 em PREREGISTRO-C10.sha256, gravado ANTES deste script; conferido abaixo, aborta se mudou).
E1: taxa nacional padronizada por idade (dados/sim/asr_brasil.csv; arma gerada com dados/sim/padroniza_idade.py como em c09_d1_its.py) no ano-base e no ano-fim de cada governo.
E2: 67 trocas reais de governador (c10_estrutura.py); excesso relativo r = 100[(D_uf/A_uf)/(D_br/A_br) - 1] entre as médias dos 3 anos antes (e-3..e-1) e dos 3 depois (e..e+2),
    truncadas a 2012-2024; referência de acaso = UFs sem troca em e-2..e+2 no mesmo ano, reamostragem pareada por ano (B = 9999, semente 20261024 por célula).
Rodar: /opt/homebrew/bin/python3.14 -I c10_exposicao.py   Saídas: c10_e1_federal.csv, c10_e1_serie_longo.csv, c10_e2_trocas_longo.csv, c10_e2_resumo.csv, c10_resultados.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import sys; sys.dont_write_bytecode = True   # não deixar __pycache__ em dados/ ao importar módulos irmãos
import csv, collections, hashlib, importlib.util, json, math, re
from datetime import date
import numpy as np
import pandas as pd

BASE = REPO_ROOT
D = f"{BASE}/dados"
AQUI = f"{BASE}/dados/exposicao"
SCR = f"{BASE}/fontes/p2-f8-dados-uf/sidra"
B, SEMENTE = 9999, 20261024


def _imp(nome, arq):
    s = importlib.util.spec_from_file_location(nome, arq); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ---------- o pré-registro não mudou ----------
_pre = open(f"{AQUI}/PREREGISTRO-C10.md", "rb").read()
HASH = hashlib.sha256(_pre[:_pre.index(b"\n---\n\n**ADENDOS")]).hexdigest()
assert HASH == open(f"{AQUI}/PREREGISTRO-C10.sha256", encoding="utf-8").read().split()[0], "corpo do pré-registro mudou"

pdz = _imp("padroniza", f"{D}/sim/padroniza_idade.py")
est = _imp("c10est", f"{AQUI}/c10_estrutura.py")
ANOS = list(range(2010, 2025))
F = lambda v: f"{v:.10g}" if isinstance(v, float) else v

# ======================= E1 FEDERAL =======================
GR = ["Brasil", "Mulheres negras", "Mulheres não negras", "Homens negros", "Homens não negros"]
pub = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{D}/sim/asr_brasil.csv", encoding="utf-8")): pub[(r["grupo"], r["desfecho"])][int(r["ano"])] = float(r["taxa_padronizada"])
m_ag, _ = pdz.redistribui(pdz.carrega_mortes(["agressao"])); m_ai, _ = pdz.redistribui(pdz.carrega_mortes(["agressao", "indet"]))
SER = {}   # (grupo, desfecho) -> {ano: (taxa, lo, hi)}
for g in GR:
    sx, rc = pdz.GRUPOS[g]
    for des, m in (("agressao", m_ag), ("agressao+indet", m_ai)):
        v = {a: pdz.asr(m, a, sx, rc)[:3] for a in ANOS}
        assert all(abs(round(v[a][0], 2) - pub[(g, des)][a]) < 0.005 + 1e-9 for a in ANOS), ("porta asr_brasil", g, des)
        SER[(g, des)] = v
df = pd.read_csv(f"{D}/sim/sim_agressoes_agregado.csv")
da = df[(df.grupo == "agressao") & (df.arma == 1)].copy()
da["faixa"] = da.faixa.map(lambda f: pdz.faixa17(f) if f != "ign" else "ign")
m_ar, _ = pdz.redistribui(da.groupby(["ano", "sexo", "raca", "faixa"], as_index=False).n.sum())
SER[("Arma de fogo", "agressao")] = {a: pdz.asr(m_ar, a, *pdz.GRUPOS["Brasil"])[:3] for a in ANOS}
c09 = next(l for l in open(f"{BASE}/dados/presidencia/c09_d1_resultados.md", encoding="utf-8") if l.startswith("| Brasil | arma | ") and l.count("|") > 15)
c09v = [float(x) for x in c09.strip().strip("|").split("|")[2:]]
assert len(c09v) == 15 and all(abs(round(SER[("Arma de fogo", "agressao")][a][0], 2) - c09v[i]) < 0.005 + 1e-9 for i, a in enumerate(ANOS)), "porta arma C09"
cnt = df.groupby(["ano", "grupo"]).n.sum()
RAZ = {a: 100.0 * cnt[(a, "indet")] / (cnt[(a, "agressao")] + cnt[(a, "indet")]) for a in ANOS}

GOV = est.janelas_federais()


def governo_do_ano(a):
    a0, a1 = date(a, 1, 1), date(a, 12, 31); tot = (a1 - a0).days + 1; out = []
    for p in csv.DictReader(open(est.PRES, encoding="utf-8")):
        i, f = max(a0, date.fromisoformat(p["inicio"])), min(a1, date.fromisoformat(p["fim"]))
        if f >= i: out.append(f"{p['presidente'].split(' (')[0]} {((f - i).days + 1) / tot:.3f}")
    return "; ".join(out)


E1 = []
for j in GOV:
    for (g, des), v in SER.items():
        b, f, t0 = j["ano_base"], j["ano_fim"], j["tendencia_de"]
        row = dict(governo=j["presidente"], partido=j["partido"], inicio=j["inicio"], fim_exercicio=j["fim_exercicio"], em_curso=int(j["em_curso"]), serie=g, desfecho=des,
                   ano_base=b, ano_fim=f, taxa_base="", taxa_fim="", var_pct="", var_pct_lo="", var_pct_hi="", var_pontos="", var_anual_pct="",
                   pre_de=t0, taxa_pre="", pre_var_pct="", pre_anual_pct="", razao_indet_base="", razao_indet_fim="", nota="")
        if b not in v:
            row["nota"] = "n/d: SIM em disco começa em 2010 (ano-base fora da série)"; E1.append(row); continue
        (tb, lb, _), (tf, lf, _) = v[b], v[f]
        vb, vf = ((tb - lb) / 1.96 / tb) ** 2, ((tf - lf) / 1.96 / tf) ** 2; lr = math.log(tf / tb); h = 1.96 * math.sqrt(vb + vf)
        row.update(taxa_base=tb, taxa_fim=tf, var_pct=100 * (tf / tb - 1), var_pct_lo=100 * (math.exp(lr - h) - 1), var_pct_hi=100 * (math.exp(lr + h) - 1),
                   var_pontos=tf - tb, var_anual_pct=100 * ((tf / tb) ** (1 / (f - b)) - 1), razao_indet_base=RAZ[b], razao_indet_fim=RAZ[f])
        if t0 in v:
            tp = v[t0][0]; row.update(taxa_pre=tp, pre_var_pct=100 * (tb / tp - 1), pre_anual_pct=100 * ((tb / tp) ** (1 / 3) - 1))
        else: row["nota"] = "tendência pré n/d (sem dado antes de 2010)"
        if j["em_curso"]: row["nota"] = (row["nota"] + "; " if row["nota"] else "") + "em curso: 2 de 4 anos; denominador 2023-24 extrapolado"
        E1.append(row)
with open(f"{AQUI}/c10_e1_federal.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(E1[0])); w.writeheader(); w.writerows([{k: F(x) for k, x in r.items()} for r in E1])
with open(f"{AQUI}/c10_e1_serie_longo.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["ano", "serie", "desfecho", "taxa_padronizada", "ic_lo", "ic_hi", "razao_indet_brasil_pct", "governo_fracao_do_ano"])
    for (g, des), v in SER.items():
        for a in ANOS: w.writerow([a, g, des, F(v[a][0]), F(v[a][1]), F(v[a][2]), F(RAZ[a]), governo_do_ano(a)])

# ======================= E2 ESTADUAL =======================
rows = list(csv.DictReader(open(f"{D}/painel/painel_uf_ano_tse_brc.csv", encoding="utf-8")))
assert len(rows) == 351
COL = {"total": "tx_total", "homens": "tx_homens", "mulheres": "tx_mulheres", "negros": "tx_negros", "nao_negros": "tx_nao_negros", "arma": "tx_arma"}
GRUPOS2 = ["total", "homens", "mulheres", "negros", "nao_negros", "arma", "total_agr_indet"]
# população: cópia literal de dados/presidencia/c09_d2_painel.py (que copia painel_f8.py)
SIGLA = {'RO': 'Rondônia', 'AC': 'Acre', 'AM': 'Amazonas', 'RR': 'Roraima', 'PA': 'Pará', 'AP': 'Amapá', 'TO': 'Tocantins', 'MA': 'Maranhão', 'PI': 'Piauí', 'CE': 'Ceará', 'RN': 'Rio Grande do Norte',
         'PB': 'Paraíba', 'PE': 'Pernambuco', 'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia', 'MG': 'Minas Gerais', 'ES': 'Espírito Santo', 'RJ': 'Rio de Janeiro', 'SP': 'São Paulo', 'PR': 'Paraná',
         'SC': 'Santa Catarina', 'RS': 'Rio Grande do Sul', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso', 'GO': 'Goiás', 'DF': 'Distrito Federal'}
pop = collections.defaultdict(dict)
for x in json.load(open(f"{SCR}/sidra6407_n3_606_c2all_c58tot_pall.json"))[1:]:
    if x['V'] in ('..', '-', '...'): continue
    pop[(x['D1N'], int(x['D3N']))][x['D4N']] = float(x['V']) * 1000
acc = collections.defaultdict(lambda: collections.defaultdict(list))
for x in json.load(open(f"{SCR}/sidra6403_n3_606_c86all_pall.json"))[1:]:
    if x['V'] in ('..', '-', '...'): continue
    ano = int(x['D3N'].split()[-1]); acc[(x['D1N'], ano)][x['D4N']].append(float(x['V']) * 1000)
for k, v in acc.items():
    pop[k]['negros'] = np.mean(v['Preta']) + np.mean(v['Parda']); pop[k]['total_raca'] = np.mean(v['Total']); pop[k]['nao_negros'] = pop[k]['total_raca'] - pop[k]['negros']
for (uf, ano) in list(pop):
    if 'negros' not in pop[(uf, ano)] and (uf, ano - 1) in acc and (uf, ano + 1) in acc:
        for c in ('negros', 'nao_negros', 'total_raca'): pop[(uf, ano)][c] = (pop[(uf, ano - 1)][c] + pop[(uf, ano + 1)][c]) / 2
atl = {(r["uf"], int(r["ano"]), r["variavel"]): float(r["valor"]) for r in csv.DictReader(open(f"{D}/atlas_uf_series.csv", encoding="utf-8")) if r["valor"] != "" and r["variavel"].endswith("_n")}
sim = collections.Counter()
for r in csv.DictReader(open(f"{D}/sim/sim_agressoes_agregado.csv", encoding="utf-8")):
    if r["grupo"] in ("agressao", "indet") and r["uf"] in SIGLA: sim[(SIGLA[r["uf"]], int(r["ano"]), r["grupo"])] += int(r["n"])


def num_den(uf, a, g):
    o = lambda v: atl[(uf, a, v)]; p = pop[(uf, a)]
    if g == "total": return o("homicidios_total_n"), p["Total"]
    if g == "mulheres": return o("homicidios_mulheres_n"), p["Mulheres"]
    if g == "homens": return o("homicidios_total_n") - o("homicidios_mulheres_n"), p["Homens"]
    if g == "negros": return o("homicidios_negros_n"), p["negros"]
    if g == "nao_negros": return o("homicidios_nao_negros_n"), p["nao_negros"]
    if g == "arma": return o("homicidios_arma_fogo_n"), p["Total"]
    if g == "total_agr_indet": return sim[(uf, a, "agressao")] + sim[(uf, a, "indet")], p["Total"]


UFS = sorted({r["uf"] for r in rows}); ANOS2 = list(range(2012, 2025))
TX = {}   # (uf, ano, grupo) -> taxa por 100 mil
maxd = 0.0; mism = 0
for r in rows:
    u, a = r["uf"], int(r["ano"])
    for g in GRUPOS2:
        n, p = num_den(u, a, g); TX[(u, a, g)] = n / p * 1e5
        if g in COL: maxd = max(maxd, abs(TX[(u, a, g)] - float(r[COL[g]])))
    mism += sim[(u, a, "agressao")] != atl[(u, a, "homicidios_total_n")]
assert len(UFS) == 27 and maxd < 1e-9 and mism == 0, ("porta painel/atlas/SIM", maxd, mism)
NAC = {}   # Brasil = soma das 27 UFs (numerador e denominador)
for a in ANOS2:
    for g in GRUPOS2:
        nd = [num_den(u, a, g) for u in UFS]; NAC[(a, g)] = sum(n for n, _ in nd) / sum(p for _, p in nd) * 1e5

by = est.exposicoes(); EV, onda = est.trocas(by); AT = est.anos_troca(EV)
assert len(EV) == 67 and onda == 27


def janela(e):
    return [y for y in range(e - 3, e) if y >= 2012], [y for y in range(e, e + 3) if y <= 2024]


def excesso(u, e, g):
    pre, pos = janela(e); m = lambda uf, ys: np.mean([TX[(uf, y, g)] for y in ys]); n = lambda ys: np.mean([NAC[(y, g)] for y in ys])
    Au, Du, Ab, Db = m(u, pre), m(u, pos), n(pre), n(pos)
    return 100 * ((Du / Au) / (Db / Ab) - 1), (Du - Au) - (Db - Ab), Au, Du, Ab, Db


LONG = []
for u, e, pa, pb, ia, ib in EV:
    pre, pos = janela(e); refs = est.referencias(by, AT, e)
    meta = dict(uf=u, ano_troca=e, partido_antes=pa, partido_depois=pb, ideologia_antes=ia, ideologia_depois=ib, sentido="para a direita" if ib > ia else "para a esquerda",
                direcao_bloco=est.direcao_bloco(ia, ib), n_antes=len(pre), n_depois=len(pos), janela_completa=int(est.janela_completa(e)),
                contaminada=int(est.contaminada(u, e, AT)), posse_eleitoral=int(e in (2015, 2019, 2023) and "|" not in pb), n_referencias=len(refs))
    for g in GRUPOS2:
        r, pts, Au, Du, Ab, Db = excesso(u, e, g)
        LONG.append(dict(meta, grupo=g, taxa_uf_antes=Au, taxa_uf_depois=Du, var_uf_pct=100 * (Du / Au - 1), taxa_br_antes=Ab, taxa_br_depois=Db, var_br_pct=100 * (Db / Ab - 1),
                         excesso_rel_pct=r, excesso_pontos=pts, sentido_rel="subiu" if r > 0 else ("caiu" if r < 0 else "igual"),
                         ref_excesso_pct="; ".join(f"{x}:{excesso(x, e, g)[0]:.4f}" for x in refs)))
with open(f"{AQUI}/c10_e2_trocas_longo.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(LONG[0])); w.writeheader(); w.writerows([{k: F(x) for k, x in r.items()} for r in LONG])

RECORTES = {"P_todas_67": lambda r: True, "a_janela_completa": lambda r: r["janela_completa"] == 1,
            "b_completa_nao_contaminada": lambda r: r["janela_completa"] == 1 and r["contaminada"] == 0, "c_posse_eleitoral": lambda r: r["posse_eleitoral"] == 1}
DIRS = [("todas", lambda r: True), ("sentido: para a direita", lambda r: r["sentido"] == "para a direita"), ("sentido: para a esquerda", lambda r: r["sentido"] == "para a esquerda")] + \
       [(f"bloco: {d}", (lambda d: lambda r: r["direcao_bloco"] == d)(d)) for d in ("esquerda->direita", "direita->esquerda", "envolve centro", "mesmo bloco")]
REFR = {(u, e, g): np.array([excesso(x, e, g)[0] for x in est.referencias(by, AT, e)]) for u, e, *_ in EV for g in GRUPOS2}


def p2(ref, obs):
    return min(1.0, 2 * min((np.sum(ref <= obs) + 1) / (B + 1), (np.sum(ref >= obs) + 1) / (B + 1)))


def holm(ps):
    o = sorted(range(len(ps)), key=lambda i: ps[i]); out = [0.0] * len(ps); run = 0.0
    for k, i in enumerate(o): run = max(run, min(1.0, (len(ps) - k) * ps[i])); out[i] = run
    return out


RES = []
for rec, frec in RECORTES.items():
    for dn, fd in DIRS:
        fam = []
        for g in GRUPOS2:
            sel = [r for r in LONG if r["grupo"] == g and frec(r) and fd(r)]
            if not sel: continue
            x = np.array([r["excesso_rel_pct"] for r in sel]); rng = np.random.default_rng(SEMENTE)
            M = np.vstack([REFR[(r["uf"], r["ano_troca"], g)][rng.integers(0, len(REFR[(r["uf"], r["ano_troca"], g)]), size=B)] for r in sel])
            rmed, rfra = np.median(M, axis=0), np.mean(M > 0, axis=0)
            med, fra = float(np.median(x)), float(np.mean(x > 0))
            RES.append(dict(recorte=rec, direcao=dn, grupo=g, n=len(sel), n_subiu=int(np.sum(x > 0)), n_caiu=int(np.sum(x < 0)), mediana_pct=med,
                            p25_pct=float(np.percentile(x, 25)), p75_pct=float(np.percentile(x, 75)), min_pct=float(x.min()), max_pct=float(x.max()),
                            mediana_pontos=float(np.median([r["excesso_pontos"] for r in sel])),
                            ref_mediana_p2_5=float(np.percentile(rmed, 2.5)), ref_mediana_p50=float(np.median(rmed)), ref_mediana_p97_5=float(np.percentile(rmed, 97.5)),
                            p_mediana=p2(rmed, med), fracao_subiu=fra, ref_fracao_p2_5=float(np.percentile(rfra, 2.5)), ref_fracao_media=float(np.mean(rfra)),
                            ref_fracao_p97_5=float(np.percentile(rfra, 97.5)), p_fracao=p2(rfra, fra)))
            if g != "total_agr_indet": fam.append(RES[-1])
        for k, h in zip(("p_mediana", "p_fracao"), (holm([r["p_mediana"] for r in fam]), holm([r["p_fracao"] for r in fam]))):
            for r, v in zip(fam, h): r[k + "_holm6"] = v
for r in RES: r.setdefault("p_mediana_holm6", ""); r.setdefault("p_fracao_holm6", "")
with open(f"{AQUI}/c10_e2_resumo.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(RES[0])); w.writeheader(); w.writerows([{k: F(x) for k, x in r.items()} for r in RES])

# ======================= relatório técnico =======================
NOME = {"total": "total", "homens": "homens", "mulheres": "mulheres", "negros": "negros", "nao_negros": "não negros", "arma": "arma de fogo", "total_agr_indet": "total, agressão + indeterminada"}
f1 = lambda v, d=1: "n/d" if v == "" else f"{v:+.{d}f}"
L = ["# C10 — exposição por governo (gerado por c10_exposicao.py; DESCRITIVO, sem atribuição causal)", "", "> [!NOTE]",
     f"> Pré-registro `PREREGISTRO-C10.md` (corpo sha256 {HASH}, conferido nesta execução). Nada aqui é sobre violência contra pessoas LGBT: o SIM não registra orientação, identidade nem motivação.", "",
     "## E1 — federal: taxa nacional padronizada por idade (por 100 mil) no ano-base e no ano-fim de cada governo", "",
     "Portas: 5 grupos x 2 desfechos = `asr_brasil.csv` (0,005); arma = série do C09 (2 casas). IC da variação = só incerteza de contagem (Poisson).", "",
     "| governo | série | desfecho | base -> fim | taxa base -> fim | variação % [IC contagem] | pontos | % ao ano | 3 anos antes da posse (% total; % ao ano) | indeterminadas base -> fim | nota |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in E1:
    if r["taxa_base"] == "": L.append(f"| {r['governo']} | {r['serie']} | {r['desfecho']} | {r['ano_base']} -> {r['ano_fim']} | n/d | n/d | n/d | n/d | n/d | n/d | {r['nota']} |"); continue
    pre = "n/d" if r["pre_var_pct"] == "" else f"{r['pre_de']}->{r['ano_base']}: {r['pre_var_pct']:+.1f}%; {r['pre_anual_pct']:+.1f}%/ano"
    L.append(f"| {r['governo']} | {r['serie']} | {r['desfecho']} | {r['ano_base']} -> {r['ano_fim']} | {r['taxa_base']:.2f} -> {r['taxa_fim']:.2f} | {r['var_pct']:+.1f}% [{r['var_pct_lo']:+.1f}; {r['var_pct_hi']:+.1f}] | {r['var_pontos']:+.2f} | {r['var_anual_pct']:+.1f} | {pre} | {r['razao_indet_base']:.1f}% -> {r['razao_indet_fim']:.1f}% | {r['nota']} |")
L += ["", "## E2 — estadual: excesso relativo ao Brasil nas 67 trocas reais de governador (3 anos antes x 3 depois)", "",
      f"Portas: taxas por UF-ano recalculadas = painel (máx. diferença {maxd:.1e}); agressão SIM = Atlas em todos os 351 UF-anos; Brasil = soma das 27 UFs. Referência = UFs sem troca em e-2..e+2 no mesmo ano, B = {B}, semente {SEMENTE}.", "",
      "| recorte | direção | grupo | n | subiu / caiu | mediana % [p25; p75] | referência: mediana 95% | p (mediana) | fração subiu | referência: fração 95% | p (fração) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in RES:
    if r["direcao"] != "todas" and r["grupo"] != "total": continue
    L.append(f"| {r['recorte']} | {r['direcao']} | {NOME[r['grupo']]} | {r['n']} | {r['n_subiu']} / {r['n_caiu']} | {r['mediana_pct']:+.1f} [{r['p25_pct']:+.1f}; {r['p75_pct']:+.1f}] | "
             f"[{r['ref_mediana_p2_5']:+.1f}; {r['ref_mediana_p97_5']:+.1f}] | {r['p_mediana']:.3f} | {r['fracao_subiu']:.2f} | [{r['ref_fracao_p2_5']:.2f}; {r['ref_fracao_p97_5']:.2f}] | {r['p_fracao']:.3f} |")
L += ["", f"Células no resumo completo (`c10_e2_resumo.csv`): {len(RES)}; a 5%, esperam-se ~{0.05 * len(RES):.0f} p < 0,05 só por acaso (duas estatísticas por célula, não independentes). A tabela acima mostra todas as direções só para o total e todos os grupos só para 'todas'.",
      "Limites: trocas coincidem com eleições, ciclos nacionais e outras políticas; trocas sobrepostas da mesma UF não são independentes; 2023-24 com até 2 anos de 'depois' e denominador extrapolado; a referência compara com UFs que não trocaram no mesmo ano, o que NÃO é contrafactual."]
open(f"{AQUI}/c10_resultados.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
