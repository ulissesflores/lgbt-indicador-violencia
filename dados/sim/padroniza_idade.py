"""Taxas de mortalidade por agressão PADRONIZADAS POR IDADE (padronização direta), Brasil 2010-2024, por sexo x raça/cor, com decomposição de Kitagawa.
Resolve a pendência de rigor do F10 ("grupos mais seguros"): as taxas do dossiê eram brutas e as de homens (~37, ~52, ~19) eram aritmética sobre o Atlas.
Entradas: dados/sim/sim_agressoes_agregado.csv (microdados SIM, dados/sim/agrega_sim.py) e Censo 2010/2022 por raça x sexo x idade
(SIDRA 9606; fontes/p2-f8-dados-uf/sidra/censo9606_n1_raca_sexo_idade_2010_2022.json; sha256 em SHA256SUMS.txt).
Método (declarado antes de rodar):
  - Óbito: causa básica X85-Y09 (agressão); sensibilidade com Y10-Y34 (intenção indeterminada) somada como limite superior.
  - Faixas de 5 anos (0-4 ... 75-79, 80+). Padrão = população do Brasil 2022 (todas as raças, ambos os sexos) - mesmo padrão para todos os grupos.
  - Denominador anual: interpolação GEOMÉTRICA intercensitária por célula (raça x sexo x faixa) entre Censo 2010 e 2022; 2023-24 EXTRAPOLADOS pela mesma taxa de crescimento (limitação declarada: a autodeclaração de cor mudou entre censos).
  - Idade ignorada: redistribuída proporcionalmente entre faixas dentro de ano x sexo x raça. Raça ignorada: redistribuída proporcionalmente entre as raças conhecidas dentro de ano x sexo x faixa;
    limites sem redistribuição (inferior) e com TODA a raça ignorada atribuída a negros ou a não negros (extremos) para a razão negros/não negros.
  - IC95% de Poisson sobre óbitos redistribuídos (aproximação; ignora a incerteza da redistribuição e dos denominadores).
  - Negros = preta + parda; não negros = branca + amarela + indígena (convenção do Atlas/dossiê).
Rodar: /opt/homebrew/bin/python3.14 -I dados/sim/padroniza_idade.py   Saídas: dados/sim/asr_brasil.csv, dados/sim/asr_brasil.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, json, math
import numpy as np
import pandas as pd

BASE = REPO_ROOT
G17 = ["0-4"] + [f"{a}-{a+4}" for a in range(5, 80, 5)] + ["80+"]
RACAS = ["branca", "preta", "amarela", "parda", "indigena"]
CENSO_RACA = {"Branca": "branca", "Preta": "preta", "Amarela": "amarela", "Parda": "parda", "Indígena": "indigena"}


def faixa17(f):
    if f in ("<1", "1-4"): return "0-4"
    return f


def carrega_pop():
    d = json.load(open(f"{BASE}/fontes/p2-f8-dados-uf/sidra/censo9606_n1_raca_sexo_idade_2010_2022.json", encoding="utf-8"))[1:]
    pop = {}
    for x in d:
        lab = x["D6N"]; ano = int(x["D3N"]); sx = {"Homens": "M", "Mulheres": "F"}[x["D5N"]]; rc = CENSO_RACA[x["D4N"]]
        if lab in ("80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais"): g = "80+"
        else: g = lab.replace(" a ", "-").replace(" anos", "")
        v = float(x["V"]) if x["V"] not in ("-", "...", "X", "..") else 0.0
        pop[(ano, sx, rc, g)] = pop.get((ano, sx, rc, g), 0.0) + v
    return pop


POP = carrega_pop()


def pop_ano(ano, sx, rc, g):
    p10, p22 = POP[(2010, sx, rc, g)], POP[(2022, sx, rc, g)]
    return p10 * (p22 / p10) ** ((ano - 2010) / 12.0)


PADRAO = {g: sum(POP[(2022, s, r, g)] for s in "MF" for r in RACAS) for g in G17}
PADRAO = {g: v / sum(PADRAO.values()) for g, v in PADRAO.items()}


def carrega_mortes(grupos):
    df = pd.read_csv(f"{BASE}/dados/sim/sim_agressoes_agregado.csv")
    df = df[df.grupo.isin(grupos)].copy()
    df["faixa"] = df.faixa.map(lambda f: faixa17(f) if f != "ign" else "ign")
    return df.groupby(["ano", "sexo", "raca", "faixa"], as_index=False).n.sum()


def redistribui(df):
    """devolve dict[(ano,sexo,raca,faixa)] -> óbitos com idade e raça ignoradas redistribuídas; e o total sem redistribuir raça."""
    out = {}; nr = {}
    anos = sorted(df.ano.unique())
    for ano in anos:
        d = df[(df.ano == ano) & df.sexo.isin(["M", "F"])]
        for sx in "MF":
            e = d[d.sexo == sx]
            # 1) idade ignorada -> proporcional entre faixas, dentro de raça (incluindo raça 'ign')
            tab = {}
            for rc in RACAS + ["ign"]:
                er = e[e.raca == rc]
                conhecido = {g: float(er[er.faixa == g].n.sum()) for g in G17}
                ign = float(er[er.faixa == "ign"].n.sum()); tot = sum(conhecido.values())
                for g in G17:
                    tab[(rc, g)] = conhecido[g] + (ign * conhecido[g] / tot if tot > 0 else 0.0)
            # 2) raça ignorada -> proporcional às raças conhecidas, dentro de faixa
            for g in G17:
                kn = {rc: tab[(rc, g)] for rc in RACAS}; s = sum(kn.values()); ig = tab[("ign", g)]
                for rc in RACAS:
                    out[(ano, sx, rc, g)] = kn[rc] + (ig * kn[rc] / s if s > 0 else 0.0)
                    nr[(ano, sx, rc, g)] = kn[rc]
                out[(ano, sx, "ign", g)] = ig
    return out, nr


def asr(mortes, ano, sx_list, raca_list, extra_ign_to=None):
    """ASR (por 100 mil), IC95% Poisson, óbitos, população; agrega sexo/raça somando óbitos e população por faixa."""
    num = {}; den = {}
    for g in G17:
        d = sum(mortes.get((ano, sx, rc, g), 0.0) for sx in sx_list for rc in raca_list)
        n = sum(pop_ano(ano, sx, rc, g) for sx in sx_list for rc in raca_list)
        if extra_ign_to is not None:  # todos os 'ign' atribuídos ao grupo
            d += sum(mortes.get((ano, sx, "ign", g), 0.0) for sx in sx_list)
        num[g] = d; den[g] = n
    taxa = sum(PADRAO[g] * num[g] / den[g] for g in G17) * 1e5
    var = sum((PADRAO[g] / den[g]) ** 2 * num[g] for g in G17) * 1e10
    bruta = sum(num.values()) / sum(den.values()) * 1e5
    return taxa, taxa - 1.96 * math.sqrt(var), taxa + 1.96 * math.sqrt(var), bruta, sum(num.values()), sum(den.values())


GRUPOS = {
    "Brasil": ("MF", RACAS), "Homens": ("M", RACAS), "Mulheres": ("F", RACAS),
    "Negros": ("MF", ["preta", "parda"]), "Não negros": ("MF", ["branca", "amarela", "indigena"]),
    "Homens negros": ("M", ["preta", "parda"]), "Homens não negros": ("M", ["branca", "amarela", "indigena"]),
    "Mulheres negras": ("F", ["preta", "parda"]), "Mulheres não negras": ("F", ["branca", "amarela", "indigena"]),
}


def kitagawa(mortes, ano, g1, g2):
    """Decompõe taxa bruta(g1) - taxa bruta(g2) em efeito de composição etária e efeito de taxas por idade (Kitagawa)."""
    def comp(sxl, rcl):
        n = {g: sum(pop_ano(ano, s, r, g) for s in sxl for r in rcl) for g in G17}
        d = {g: sum(mortes.get((ano, s, r, g), 0.0) for s in sxl for r in rcl) for g in G17}
        N = sum(n.values())
        return {g: n[g] / N for g in G17}, {g: d[g] / n[g] for g in G17}
    c1, r1 = comp(*GRUPOS[g1]); c2, r2 = comp(*GRUPOS[g2])
    efeito_taxa = sum((r1[g] - r2[g]) * (c1[g] + c2[g]) / 2 for g in G17) * 1e5
    efeito_comp = sum((c1[g] - c2[g]) * (r1[g] + r2[g]) / 2 for g in G17) * 1e5
    return efeito_comp + efeito_taxa, efeito_comp, efeito_taxa


def main():
    L = ["# Taxas de agressão padronizadas por idade, Brasil (gerado por padroniza_idade.py)", "",
         "Padrão: população do Brasil 2022 (17 faixas). Denominador: Censo 2010/2022 com interpolação geométrica por célula (2023-24 extrapolados, ⚠️). IC95% Poisson (aproximado).", ""]
    rows = []
    m_ag, nr_ag = redistribui(carrega_mortes(["agressao"]))
    m_ai, _ = redistribui(carrega_mortes(["agressao", "indet"]))
    anos = sorted({k[0] for k in m_ag})
    L += ["## 1. Taxa padronizada por 100 mil (agressão X85-Y09), anos selecionados", "", "| grupo | " + " | ".join(str(a) for a in (2012, 2016, 2020, 2022, 2023, 2024)) + " |", "|---|" + "---|" * 6]
    for gname, (sxl, rcl) in GRUPOS.items():
        cel = []
        for a in anos:
            t, lo, hi, br, d, n = asr(m_ag, a, sxl, rcl)
            rows.append([gname, a, round(t, 2), round(lo, 2), round(hi, 2), round(br, 2), round(d), round(n), "agressao"])
            ti, _, _, _, _, _ = asr(m_ai, a, sxl, rcl)
            rows.append([gname, a, round(ti, 2), "", "", "", "", "", "agressao+indet"])
            if a in (2012, 2016, 2020, 2022, 2023, 2024): cel.append(f"{t:.1f} [{lo:.1f}; {hi:.1f}] (bruta {br:.1f})")
        L.append(f"| {gname} | " + " | ".join(cel) + " |")
    # razões
    L += ["", "## 2. Razões padronizadas (pooled 2022-2024 para estabilidade; ⚠️ 2023-24 com denominador extrapolado)", "", "| razão | valor | observação |", "|---|---|---|"]

    def pooled(gn, base=m_ag, ign=None):
        sxl, rcl = GRUPOS[gn]; num = {g: 0.0 for g in G17}; den = {g: 0.0 for g in G17}
        for a in (2022, 2023, 2024):
            for g in G17:
                num[g] += sum(base.get((a, s, r, g), 0.0) for s in sxl for r in rcl) + (sum(base.get((a, s, "ign", g), 0.0) for s in sxl) if ign else 0.0)
                den[g] += sum(pop_ano(a, s, r, g) for s in sxl for r in rcl)
        return sum(PADRAO[g] * num[g] / den[g] for g in G17) * 1e5
    hm, mu = pooled("Homens"), pooled("Mulheres"); ng, nn = pooled("Negros"), pooled("Não negros")
    L.append(f"| homens / mulheres (padronizado) | {hm/mu:.1f} | taxas {hm:.1f} e {mu:.1f} por 100 mil |")
    L.append(f"| negros / não negros (padronizado, raça ignorada redistribuída) | {ng/nn:.2f} | taxas {ng:.1f} e {nn:.1f} |")
    ng_x, nn_x = pooled("Negros", m_ag, ign=True), pooled("Não negros", m_ag, ign=True)
    ng_i = pooled("Negros", nr_ag); nn_i = pooled("Não negros", nr_ag)
    L.append(f"| negros / não negros: limite inferior (raça ignorada descartada) | {ng_i/nn_i:.2f} | |")
    L.append(f"| negros / não negros: extremo A (toda raça ignorada -> negros) | {pooled('Negros', m_ag, True)/pooled('Não negros'):.2f} | cota máxima possível a favor de negros mais expostos |")
    L.append(f"| negros / não negros: extremo B (toda raça ignorada -> não negros) | {pooled('Negros')/pooled('Não negros', m_ag, True):.2f} | cota mínima |")
    for (a_, b_) in (("Homens negros", "Mulheres não negras"), ("Homens não negros", "Mulheres não negras"), ("Mulheres negras", "Mulheres não negras"), ("Homens negros", "Homens não negros")):
        L.append(f"| {a_} / {b_} (padronizado) | {pooled(a_)/pooled(b_):.1f} | taxas {pooled(a_):.1f} e {pooled(b_):.1f} |")
    # kitagawa
    L += ["", "## 3. Decomposição de Kitagawa da diferença de taxas BRUTAS (2022-2024 médios): composição etária x taxas por idade", "", "| comparação | diferença bruta | efeito idade | efeito taxas | % da diferença devido a taxas |", "|---|---|---|---|---|"]
    for g1, g2 in (("Homens", "Mulheres"), ("Negros", "Não negros"), ("Homens negros", "Homens não negros"), ("Mulheres negras", "Mulheres não negras")):
        ds = np.array([kitagawa(m_ag, a, g1, g2) for a in (2022, 2023, 2024)]).mean(axis=0)
        L.append(f"| {g1} - {g2} | {ds[0]:.1f} | {ds[1]:+.1f} | {ds[2]:+.1f} | {100*ds[2]/ds[0]:.0f}% |")
    # ordem de segurança
    L += ["", "## 4. Ordem de 'segurança' (menor para maior taxa padronizada de agressão, 2022-24 agregado)", ""]
    ordem = sorted(((pooled(g), g) for g in ("Mulheres não negras", "Mulheres negras", "Homens não negros", "Homens negros")))
    L += [f"{i+1}. {g}: {v:.1f} por 100 mil" for i, (v, g) in enumerate(ordem)]
    open(f"{BASE}/dados/sim/asr_brasil.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(f"{BASE}/dados/sim/asr_brasil.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["grupo", "ano", "taxa_padronizada", "ic_lo", "ic_hi", "taxa_bruta", "obitos", "pop", "desfecho"]); w.writerows(rows)
    print("\n".join(L))


if __name__ == "__main__":
    main()
