"""C09 — ESTRUTURA do desenho (roda ANTES do pré-registro; NÃO lê nenhum desfecho).
Lê só exposições: ideologia do governador por UF-ano (dados/ideologia/ideologia_painel_tse_por_uf_ano.csv: colunas uf, ano, partidos, ideo_BRC_periodo, ideo_painel_csv),
escore BRC por partido-ano (dados/ideologia/ideologia_partidos_ano.csv), escores BLS9 (Zucco & Power) e presidentes_2007_2024.csv (datas de exercício).
Calcula: série do presidente por ano (ponderada por dias em 2016), variação disponível das exposições do D2 depois dos EF, contagens de copartidarismo (D3),
e o efeito mínimo detectável do D1 em unidades de DP residual (só a matriz de desenho; o DP vem depois, do desfecho).
Rodar: /opt/homebrew/bin/python3.14 -I c09_estrutura.py   Saída: c09_estrutura.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, math, collections
from datetime import date
import numpy as np
from scipy import stats

BASE = REPO_ROOT
AQUI = f"{BASE}/dados/presidencia"
ZP = f"{BASE}/fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab"
NORM = {"MDB": "PMDB"}   # mesma linhagem (dados/ideologia/ideologia_aliases.csv)


def presidentes():
    return list(csv.DictReader(open(f"{AQUI}/presidentes_2007_2024.csv", encoding="utf-8")))


def pesos_ano(ano):
    """[(linha do presidente, fração de dias do ano em exercício)]."""
    a0, a1 = date(ano, 1, 1), date(ano, 12, 31); tot = (a1 - a0).days + 1; out = []
    for p in presidentes():
        i, f = max(a0, date.fromisoformat(p["inicio"])), min(a1, date.fromisoformat(p["fim"]))
        if f >= i: out.append((p, ((f - i).days + 1) / tot))
    assert abs(sum(w for _, w in out) - 1) < 1e-12, ano
    return out


def brc_partido_ano():
    d = {}
    for r in csv.DictReader(open(f"{BASE}/dados/ideologia/ideologia_partidos_ano.csv", encoding="utf-8")):
        if r["fonte"] == "BRC": d[(r["linhagem"], int(r["ano"]))] = float(r["escore_0_10"])
    return d


def bolognesi_unico():
    return {r["partido"]: float(r["escore"]) for r in csv.DictReader(open(f"{BASE}/dados/ideologia_partidos.csv", encoding="utf-8")) if "Bolognesi" in r["fonte"]}


def bls9():
    return {(r["party.or.pres"], int(r["year"])): float(r["ideo"]) for r in csv.DictReader(open(ZP))}


LIN = {"PT": "PT", "PMDB": "MDB", "PSL": "PSL"}   # partido de eleição -> linhagem BRC


def pres_score(ano, escala):
    """escore do presidente no ano, ponderado por dias. escala: brc (por período) | unico (Bolognesi 2018) | bls9 (escore do próprio presidente, onda mais próxima)."""
    brc, uni, bl = brc_partido_ano(), bolognesi_unico(), bls9()
    s = 0.0
    for p, w in pesos_ano(ano):
        if escala == "brc": v = brc[(LIN[p["partido_eleicao"]], ano)]
        elif escala == "unico": v = uni[{"PMDB": "MDB"}.get(p["partido_eleicao"], p["partido_eleicao"])]
        else:
            ondas = sorted(y for (k, y) in bl if k == p["bls9_rotulo"])
            onda = min(ondas, key=lambda y: (abs(y - ano), y)); v = bl[(p["bls9_rotulo"], onda)]
        s += w * v
    return s


def copart(partidos, ano):
    """fração do ano em que o presidente (partido de eleição) está entre os partidos do governador naquele UF-ano."""
    ps = {NORM.get(x.strip(), x.strip()) for x in partidos.split("|")}
    return sum(w for p, w in pesos_ano(ano) if p["partido_eleicao"] in ps)


def exposicoes():
    rows = list(csv.DictReader(open(f"{BASE}/dados/ideologia/ideologia_painel_tse_por_uf_ano.csv", encoding="utf-8")))
    out = []
    for r in rows:
        a = int(r["ano"]); g = float(r["ideo_BRC_periodo"]); p = pres_score(a, "brc")
        out.append(dict(uf=r["uf"], ano=a, partidos=r["partidos"], g=g, p=p, gp=g * p, dist=abs(g - p), cop=copart(r["partidos"], a), g_unico=float(r["ideo_painel_csv"])))
    return out


def resid(v, F):
    return v - F @ np.linalg.lstsq(F, v, rcond=None)[0]


def fe(rows, extra=()):
    ufs = sorted({r["uf"] for r in rows}); anos = sorted({r["ano"] for r in rows})
    cols = [[1.0 * (r["uf"] == u) for r in rows] for u in ufs] + [[1.0 * (r["ano"] == a) for r in rows] for a in anos[1:]]
    cols += [[r[c] for r in rows] for c in extra]
    return np.array(cols).T


def desenho_its(quebras, anos=range(2010, 2025)):
    t = np.array(list(anos), float); X = [np.ones_like(t), t - 2010]
    for T in quebras: X += [(t >= T) * 1.0, (t >= T) * (t - T)]
    return np.column_stack(X)


def main():
    L = ["# C09 — estrutura do desenho (gerado por c09_estrutura.py; só exposições, nenhum desfecho lido)", ""]
    L += ["## Presidente por ano (ponderado por dias de exercício)", "", "| ano | composição | BRC por período | Bolognesi 2018 (único) | BLS9 do próprio presidente |", "|---|---|---|---|---|"]
    for a in range(2010, 2025):
        comp = "; ".join(f"{p['presidente'].split()[0]} ({p['partido_eleicao']}) {w:.3f}" for p, w in pesos_ano(a))
        L.append(f"| {a} | {comp} | {pres_score(a,'brc'):.4f} | {pres_score(a,'unico'):.4f} | {pres_score(a,'bls9'):+.4f} |")
    ex = exposicoes()
    assert len(ex) == 351 and len({r["uf"] for r in ex}) == 27
    F = fe(ex); Fg = fe(ex, ("g",))
    L += ["", "## D2 — variação disponível das exposições depois dos EF (UF e ano) e do controle g", "",
          "| exposição | DP bruto | DP residual (EF UF+ano) | DP residual (EF + g) |", "|---|---|---|---|"]
    for c in ("g", "gp", "dist", "cop"):
        v = np.array([r[c] for r in ex])
        L.append(f"| {c} | {v.std():.4f} | {resid(v, F).std():.4f} | " + ("—" if c == "g" else f"{resid(v, Fg).std():.4f}") + " |")
    # quanto de gp residual vem de trocas de presidente com g constante vs trocas de g (inclui as 27 trocas de onda de 2021)
    by = collections.defaultdict(dict)
    for r in ex: by[r["uf"]][r["ano"]] = r
    mud_g = sum(1 for u in by for a in range(2013, 2025) if abs(by[u][a]["g"] - by[u][a - 1]["g"]) > 1e-9)
    onda = sum(1 for u in by for a in range(2013, 2025) if abs(by[u][a]["g"] - by[u][a - 1]["g"]) > 1e-9 and by[u][a]["partidos"] == by[u][a - 1]["partidos"])
    L += ["", f"Mudanças de g (governador) 2013-2024: {mud_g}, das quais {onda} com os MESMOS partidos (troca de onda BRC, ano: " +
          f"{sorted({a for u in by for a in range(2013,2025) if abs(by[u][a]['g']-by[u][a-1]['g'])>1e-9 and by[u][a]['partidos']==by[u][a-1]['partidos']})}).",
          f"Trocas de presidente no painel 2012-2024: 2016 (parcial), 2019, 2023; mudança do escore BRC do presidente também em 2021 (onda 2022 do PSL: {pres_score(2020,'brc'):.4f} -> {pres_score(2021,'brc'):.4f})."]
    # D3
    L += ["", "## D3 — copartidarismo governador-presidente (partido de eleição; PMDB = MDB)", "", "| presidente | UF-anos com cop > 0 | soma de cop (UF-anos equivalentes) | UFs distintas |", "|---|---|---|---|"]
    for nome, anos in (("Dilma 2012-2016", range(2012, 2017)), ("Temer 2016-2018", range(2016, 2019)), ("Bolsonaro 2019-2022", range(2019, 2023)), ("Lula 2023-2024", range(2023, 2025))):
        sel = [r for r in ex if r["ano"] in anos]
        alvo = "PT" if nome.startswith(("Dilma", "Lula")) else ("PMDB" if nome.startswith("Temer") else "PSL")
        cop = [r for r in sel if alvo in {NORM.get(x, x) for x in r["partidos"].split("|")}]
        L.append(f"| {nome} | {len(cop)} | {sum(r['cop'] for r in sel):.2f} | {len({r['uf'] for r in cop})} |")
    ufs_var = sorted({u for u in by if len({round(by[u][a]['cop'], 6) for a in by[u]}) > 1})
    L.append(f"\nUFs com variação de cop no tempo: {len(ufs_var)} de 27.")
    # D1
    L += ["", "## D1 — efeito mínimo detectável (MDE) do nível em cada quebra, em unidades de DP residual sigma (só a matriz X; 15 pontos 2010-2024)", "",
          "| modelo | quebras | gl residual | fator t(0,975)+t(0,80) | MDE da mudança de nível / sigma, por quebra |", "|---|---|---|---|---|"]
    for nome, q in (("primário (nível + inclinação)", (2016, 2019, 2023)), ("placebo 1 ano antes", (2015, 2018, 2022))):
        X = desenho_its(q); df = X.shape[0] - X.shape[1]; C = np.linalg.inv(X.T @ X)
        fat = stats.t.ppf(0.975, df) + stats.t.ppf(0.80, df)
        mde = [fat * math.sqrt(C[2 + 2 * k, 2 + 2 * k]) for k in range(len(q))]
        L.append(f"| {nome} | {q} | {df} | {fat:.3f} | " + "; ".join(f"{T}: {m:.2f}" for T, m in zip(q, mde)) + " |")
    open(f"{AQUI}/c09_estrutura.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
