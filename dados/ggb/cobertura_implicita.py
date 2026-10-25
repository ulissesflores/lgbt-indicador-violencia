"""Cobertura IMPLÍCITA da contagem do GGB: quantas mortes por agressão seriam ESPERADAS entre adultos LGB+ se tivessem o mesmo risco de morte por agressão
que os pares do mesmo sexo, raça (negro/não negro) e faixa etária, e quanto da expectativa a contagem do GGB representa.
NÃO é estimativa de mortes de LGB+ nem taxa: é um exercício de LIMITE/ESCALA. Isso evita comparar a taxa 'implícita' do GGB (8,8-10,0) com a taxa
geral sem ajustar a composição (LGB+ são mais jovens e mais negros? o ajuste diz).
Método (declarado antes de rodar):
  1. Taxas específicas por (ano, sexo, raça agrupada, faixa de 5 anos) do SIM (óbitos X85-Y09, idade/raça ignoradas redistribuídas como em padroniza_idade.py) / Censo 2010-22 interpolado.
  2. Composição LGB+ adulta: prevalência de LGB+ (Y008 em 2,3,4) por célula sexo x raça x faixa, PNS 2019 (peso V00291), entre respondentes do módulo V com Y008 válido (1-4);
     aplicada à população adulta da célula no ano (faixa 15-19: só 2/5 são adultos; 18-19 da PNS representam a célula).
  3. Esperado E = soma(população LGB+ da célula x taxa da célula) x RR, com RR = 1 (mesmo risco dos pares), 2,82 (RP ajustada de violência física, PNS 2019; cenário, NÃO é razão de risco de morte) e 3,84 (bruta).
  4. Cobertura implícita = contagem GGB / E. IC: só pela prevalência (IC95% 1,73-2,07% da PNS, escalado linearmente); a incerteza da composição não entra.
LIMITES: GGB inclui pessoas trans (a PNS não mede identidade de gênero) e menores; PNS autorrelato subestima LGB+ (cenários de prevalência 3% e 5% como sensibilidade, NÃO como fato); denominador 2023-24 extrapolado; GGB = mortes noticiadas (não só agressão); o pareamento é só por sexo, raça e idade (NÃO ajusta escolaridade, UF nem urbano/rural: homicídio se concentra em periferias e UFs específicas, então se LGB+ forem mais urbanos/escolarizados o esperado cai; o sentido do viés não foi medido).
Rodar: /opt/homebrew/bin/python3.14 -I dados/ggb/cobertura_implicita.py   Saídas: dados/ggb/cobertura_implicita.md/.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import importlib.util, csv, re
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(REPO_ROOT)
spec_ = importlib.util.spec_from_file_location("pi", BASE / "dados/sim/padroniza_idade.py"); pi = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(pi)
NEG, NNEG = ["preta", "parda"], ["branca", "amarela", "indigena"]
G17 = pi.G17

# ---- PNS 2019: prevalência LGB+ por sexo x raça x faixa
P = BASE / "fontes/q1-textointegral/F2/pns2019"
pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
sp = {m.group(2): (int(m.group(1)), int(m.group(3))) for l in (P / "input_PNS_2019_utf8.txt").read_text(encoding="utf8", errors="replace").splitlines() if (m := pat.match(l))}
want = ["C006", "C008", "C009", "Y008", "V00291", "V001"]
raw = pd.read_fwf(P / "x/PNS_2019.txt", colspecs=[(sp[k][0] - 1, sp[k][0] - 1 + sp[k][1]) for k in want], names=want, header=None, dtype=str)
d = raw[raw.V001.notna() & raw.Y008.isin(["1", "2", "3", "4"])].copy()
assert d.V001.notna().all()
d["w"] = d.V00291.astype(float); d["age"] = d.C008.astype(int)
d["sx"] = d.C006.map({"1": "M", "2": "F"}); d["rc"] = np.where(d.C009.isin(["2", "4"]), "neg", np.where(d.C009.isin(["1", "3", "5"]), "nneg", None))
d = d[d.sx.notna() & d.rc.notna()]
def faixa(a):
    if a < 20: return "15-19"
    if a >= 80: return "80+"
    return f"{a//5*5}-{a//5*5+4}"
d["g"] = d.age.map(faixa); d["lgb"] = d.Y008.isin(["2", "3", "4"])
tot = d.groupby(["sx", "rc", "g"]).w.sum(); lg = d[d.lgb].groupby(["sx", "rc", "g"]).w.sum()
prev = (lg / tot).fillna(0.0)
pesos_lgb = d[d.lgb].w.sum(); pesos_tot = d.w.sum()
prev_global = pesos_lgb / pesos_tot
# distribuição etária/racial dos LGB+ x geral (para o texto)
comp = {}
for nome, sel in {"18-29": d.age < 30, "30-44": (d.age >= 30) & (d.age < 45), "45+": d.age >= 45}.items():
    comp[nome] = (d[d.lgb & sel].w.sum() / pesos_lgb, d[sel].w.sum() / pesos_tot)
comp_neg = (d[d.lgb & (d.rc == "neg")].w.sum() / pesos_lgb, d[d.rc == "neg"].w.sum() / pesos_tot)
comp_h = (d[d.lgb & (d.sx == "M")].w.sum() / pesos_lgb, d[d.sx == "M"].w.sum() / pesos_tot)

# ---- SIM
def esperado(ano, mortes, escala_prev=1.0):
    E = 0.0; lgb_pop = 0.0
    for sx in "MF":
        for rc, racas in (("neg", NEG), ("nneg", NNEG)):
            for g in G17:
                if g not in prev.index.get_level_values(2).unique(): continue
                pop = sum(pi.pop_ano(ano, sx, r, g) for r in racas)
                if g == "15-19": pop *= 0.4
                taxa = sum(mortes.get((ano, sx, r, g), 0.0) for r in racas) / sum(pi.pop_ano(ano, sx, r, g) for r in racas)
                p = prev.get((sx, rc, g), 0.0) * escala_prev
                E += pop * p * taxa; lgb_pop += pop * p
    return E, lgb_pop

GGB = {2023: {"todas": 257, "homicidios_decl": 221}, 2024: {"todas": 291, "homicidios_decl": 273}}
rows = []; L = []
for desf, grp in (("agressao", ["agressao"]), ("agressao+indet", ["agressao", "indet"])):
    mortes, _ = pi.redistribui(pi.carrega_mortes(grp))
    for ano in (2023, 2024):
        for prev_cen, esc in (("1,89% (PNS 2019, publicado; não resposta = não LGB+)", 0.0189 / prev_global), (f"{100*prev_global:.2f}% (PNS, só respostas válidas)".replace(".", ","), 1.0), ("3% (cenário)", 0.03 / prev_global), ("5% (cenário)", 0.05 / prev_global)):
            E, pl = esperado(ano, mortes, esc)
            for rr in (1.0, 2.82, 3.84):
                for medida, ggb in GGB[ano].items():
                    rows.append([desf, ano, prev_cen, rr, medida, ggb, round(pl), round(E * rr, 1), round(ggb / (E * rr), 3)])
# IC por prevalência (1,73-2,07 sobre 1,89)
ic = {}
mortes, _ = pi.redistribui(pi.carrega_mortes(["agressao"]))
for ano in (2023, 2024):
    E, pl = esperado(ano, mortes); ic[ano] = (E, pl)
df = pd.DataFrame(rows, columns=["desfecho", "ano", "prevalencia_LGB", "RR_cenario", "medida_GGB", "ggb", "pop_LGB_adulta", "mortes_esperadas", "cobertura_implicita"])
df.to_csv(BASE / "dados/ggb/cobertura_implicita.csv", index=False)

L += ["# Cobertura implícita da contagem do GGB (gerado por cobertura_implicita.py)", "",
      "**Exercício de escala, não estimativa de mortes nem taxa.** Leia o cabeçalho do script. E = mortes por agressão ESPERADAS entre adultos LGB+ se tivessem o risco dos pares (mesmo sexo, raça, faixa etária).", "",
      f"Prevalência LGB+ entre respondentes com orientação válida: {100*prev_global:.2f}% (a composição por célula vem daí); o resultado principal escala para 1,89% (publicado por Vasconcelos et al., não resposta contada como não LGB+); 1,96% e cenários maiores entram na sensibilidade.",
      f"Composição LGB+ vs adultos em geral (PNS): 18-29 anos {100*comp['18-29'][0]:.0f}% vs {100*comp['18-29'][1]:.0f}%; 30-44 {100*comp['30-44'][0]:.0f}% vs {100*comp['30-44'][1]:.0f}%; 45+ {100*comp['45+'][0]:.0f}% vs {100*comp['45+'][1]:.0f}%; negros {100*comp_neg[0]:.0f}% vs {100*comp_neg[1]:.0f}%; homens {100*comp_h[0]:.0f}% vs {100*comp_h[1]:.0f}%.", ""]
main = df[(df.desfecho == "agressao") & (df.prevalencia_LGB.str.startswith("1,89")) & (df.medida_GGB == "todas")]
L += ["## Resultado principal (desfecho agressão X85-Y09; prevalência 1,89%; GGB = todas as mortes da contagem)", "",
      "| ano | pop. LGB+ adulta | GGB | esperado RR=1 (mesmo risco dos pares) | cobertura implícita | esperado RR=2,82 | cobertura | esperado RR=3,84 | cobertura |", "|---|---|---|---|---|---|---|---|---|"]
for ano in (2023, 2024):
    r = {rr: main[(main.ano == ano) & (main.RR_cenario == rr)].iloc[0] for rr in (1.0, 2.82, 3.84)}
    L.append(f"| {ano} | {int(r[1.0].pop_LGB_adulta):,} | {int(r[1.0].ggb)} | {r[1.0].mortes_esperadas:.0f} | {100*r[1.0].cobertura_implicita:.0f}% | {r[2.82].mortes_esperadas:.0f} | {100*r[2.82].cobertura_implicita:.0f}% | {r[3.84].mortes_esperadas:.0f} | {100*r[3.84].cobertura_implicita:.0f}% |".replace(",", "."))
L += ["", "IC95% só pela prevalência (1,73-2,07% vs 1,89%): esperado e cobertura variam ~±9% (linear).", "",
      "## Sensibilidade: prevalência maior que a autodeclarada (cenários, NÃO fatos) e desfecho 'agressão + intenção indeterminada'", "",
      "| desfecho | ano | prevalência | RR | GGB (medida) | esperado | cobertura implícita |", "|---|---|---|---|---|---|---|"]
for _, r in df[(df.RR_cenario == 1.0)].iterrows():
    L.append(f"| {r.desfecho} | {r.ano} | {r.prevalencia_LGB} | {r.RR_cenario} | {r.ggb} ({r.medida_GGB}) | {r.mortes_esperadas:.0f} | {100*r.cobertura_implicita:.0f}% |")
L += ["", "## Como ler", "",
      "- Se LGB+ tivessem o MESMO risco de morte por agressão dos pares, o esperado superaria em várias vezes a contagem do GGB: a cobertura implícita da contagem seria baixa. A contagem do GGB só 'fecha' com o esperado se LGB+ tivessem risco MUITO MENOR que os pares, o que contraria a PNS (risco de violência física 2,8x a 3,8x maior).",
      "- Isso NÃO prova que o GGB capta só uma fração: o numerador do GGB inclui menores (fora do denominador adulto) e pessoas trans (a PNS 2019 não perguntou identidade de gênero: trans que declararam orientação LGB estão no denominador sem identificação, as demais não; correção v0.3, 2026-10-24), e a prevalência autodeclarada pode subestimar. Prova que numerador de mídia e denominador de survey não casam, e que a leitura 'GGB = todas as mortes LGB+' é inconsistente com qualquer cenário de risco igual ou maior que o dos pares.",
      "- Limite do pareamento: só sexo x raça x idade; sem escolaridade, UF e urbano/rural (não medido o quanto isso reduziria o esperado).",
      "- Não usar como taxa. Não usar para 'país que mais mata'. Serve para limitar o que a contagem do GGB pode significar."]
(BASE / "dados/ggb/cobertura_implicita.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[:20]))
