#!/opt/homebrew/bin/python3.14
"""Cenarios de n e custo (R$ de set/2026) para as 3 opcoes de desenho. Le: deff_pns2019.csv, n_necessario.csv, n_regiao.csv,
validacao.txt (denominadores), custos-fontes.csv (parametros com id), IPCA (SIDRA 1737) e PTAX (BCB). Escreve cenarios_n_custo.csv e n_regiao_custo.csv.

Rodar: /opt/homebrew/bin/python3.14 -I cenarios_custo.py        (sem argumentos)

MODELO (todas as premissas explicitas; nada daqui e pesquisa de campo):
  adultos a triar   = n_total_por_rodada do n_necessario.csv = n_LGB_necessario (sem arredondar) / pi_LGB, arredondado uma vez (v0.3; pi = 1,89% da PNS 2019; sobreamostra NAO reduz a triagem)
  domicilios        = adultos / rendimento                           (rendimento = adultos 18+ com modulo V / domicilios na amostra PNS 2019 = 0,816)
  A (modulo PNADC)  = IT unico + domicilios x custo variavel por domicilio-visita (TED 02/2021 MJSP-IBGE, corrigido por IPCA)
  B (PNS dedicada)  = domicilios x (valor do TED da PNS / domicilios da amostra), corrigido por IPCA; central = media entre 140 mil e 108,5 mil domicilios
  C (painel/web)    = completos x (contrato GSGB / completos de 4 anos), benchmark estrangeiro, cambio PTAX nominal, SEM paridade de poder de compra
  Custo = custeio marginal ao financiador (sem folha permanente do IBGE nas opcoes A e B). Ver README: limites.
ponytail: n_duas_prop e a bissecao de MDE sao copiadas de deff_pns2019.py (importar rodaria o script inteiro).
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, json, math, re
from pathlib import Path
from statistics import NormalDist

AQUI = Path(__file__).resolve().parent
F2 = Path((REPO_ROOT + "/fontes/q1-textointegral/F2/custos"))


def lerc(nome):
    return list(csv.DictReader(open(AQUI / nome, encoding="utf8")))


custos = {r["id"]: r for r in lerc("custos-fontes.csv")}
v = lambda i: float(custos[i]["valor"])
den = {}
for l in (AQUI / "validacao.txt").read_text().splitlines():
    m = re.match(r"\s+(\S+) = (\d+)$", l)
    if m: den[m.group(1)] = int(m.group(2))
REND = den["adultos_18mais_com_modulo_V"] / den["domicilios_na_amostra_arquivo"]          # 88.531 / 108.458

ipca = {x["D3C"]: float(x["V"]) for x in json.load(open(F2 / "sidra1737_ipca_indice.json"))[1:]}
infl = lambda de: ipca["202609"] / ipca[de]                                                # fator de correcao -> set/2026
fx = {m: json.load(open(F2 / f"ptax_{m}_2026-10-20.json"))["value"][-1]["cotacaoVenda"] for m in ("GBP", "USD", "EUR", "CAD")}

# ---- unitarios (R$ set/2026) ----
var_hh_A = (v("C05") + v("C06") + v("C07")) / v("C11") * infl("202109")      # custo variavel por domicilio visitado (modulo), TED 02/2021
it_A = v("C08") * infl("202109")                                              # TI, unico
tot_hh_A = v("C04") / v("C11") * infl("202109")                               # R$ por domicilio-trimestre, 2 modulos, tudo incluso
pns_hh_140 = v("C01") / 140_000 * infl("202312")                              # TED PNS / 140 mil (PNS 2026, noticia, ALERTA)
pns_hh_108 = v("C01") / v("C14") * infl("202312")                             # TED PNS / 108.525 (PNS 2019, primario)
pns_hh = (pns_hh_140 + pns_hh_108) / 2
gsgb_complete_gbp = v("C29") / (v("C30") * (4 + 2 / 12))                      # 4 anos e 2 meses (1/11/2025-31/12/2029)
gsgb_complete_brl = gsgb_complete_gbp * fx["GBP"]
csew_gbp = v("C23") / (v("C22") * 5)                                          # 5 anos (2024-2029), >= 70.000/ano
csew_brl = csew_gbp * fx["GBP"]
ncvs_usd = v("C24") / v("C25")
ncvs_brl = ncvs_usd * fx["USD"]
fra_eur = v("C26") / 100_000                                                  # ~100 mil respostas (ILGA-Europe, secundaria)

H_A_ANO = v("C11") + 3 * v("C11") / 5                                         # todos no 1o trimestre + so 1a visita (1/5) nos 3 seguintes
PI = float([r for r in lerc("deff_pns2019.csv") if r["indicador"] == "lgb"][0]["est"])


def n_duas_prop(p1, p2, alpha=0.05, power=0.8):
    z = NormalDist().inv_cdf
    za, zb = z(1 - alpha / 2), z(power)
    pb = (p1 + p2) / 2
    return ((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p1 - p2)) ** 2


def mde(p1, n_eff):
    lo, hi = 1e-4, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if n_duas_prop(p1, min(p1 * (1 + mid), 0.9999)) > n_eff: lo = mid
        else: hi = mid
    return hi


rows = []
NEC = lerc("n_necessario.csv")
for r in NEC:
    if r["sobreamostra_k"] != "1":
        continue                                                              # triagem e a mesma com k=5; ver README
    ind, p1, dl, deff, deffc = r["indicador"], float(r["p_base"]), float(r["mudanca_rel"]), float(r["deff_lgb"]), float(r["deff_c_lgb"])
    # v0.3 (2026-10-24, R1): adultos a triar = n_total_* de n_necessario.csv (n LGB+ SEM arredondar / pi, arredondado UMA vez no fim).
    # Antes: 5.787 (ja arredondado) / pi = 305.993, contra 305.955 do n_necessario.csv (arredondamento duplo; diferenca de 38 adultos).
    for rotulo, nl, adultos in (("deff medido", float(r["n_lgb_desenho_por_rodada"]), float(r["n_total_por_rodada"])),
                                ("autoponderado (contrafactual)", float(r["n_lgb_autoponderado_por_rodada"]), float(r["n_total_autoponderado_por_rodada"]))):
        dom = adultos / REND
        # A
        cap_A = H_A_ANO * REND                                                # adultos/ano
        anos_A = adultos / cap_A
        custoA = it_A + dom * var_hh_A
        # B
        custoB_c, custoB_lo, custoB_hi = dom * pns_hh, dom * pns_hh_140, dom * pns_hh_108
        # C
        custoC = adultos * gsgb_complete_brl
        rows.append(dict(indicador=ind, mudanca_rel=dl, deff_base=rotulo, n_lgb_necessario=round(nl), adultos_a_triar=round(adultos),
                         domicilios_a_visitar=round(dom), A_anos_de_modulo_PNADC=round(anos_A, 2), A_custo_BRL=round(custoA),
                         B_rodadas_PNS_140mil=round(dom / 140_000, 2), B_custo_central_BRL=round(custoB_c),
                         B_custo_min_BRL=round(min(custoB_lo, custoB_hi)), B_custo_max_BRL=round(max(custoB_lo, custoB_hi)),
                         C_custo_BRL=round(custoC)))
with open(AQUI / "cenarios_n_custo.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---- capacidade de cada opcao em UM ciclo: variacao minima detectavel (LGB+, deff medido) ----
cap = []
# v0.3 (2026-10-24, R1): a linha B' (PNS 2019 OBSERVADA) usa o n de LGB+ efetivamente entrevistados (dominio LGB+ do deff_pns2019.csv: 1.554),
# nao 88.531 x pi ponderada (1.674, contagem esperada sob amostra autoponderada). O deff foi medido sobre n = 1.554. A e B seguem projecoes (x pi).
N_LGB_OBS = int([r for r in lerc("deff_pns2019.csv") if r["indicador"] == "fisica" and r["dominio"] == "LGB+"][0]["n"])
for ind in ("fisica", "qualquer", "sexual12"):
    g = [r for r in lerc("deff_pns2019.csv") if r["indicador"] == ind and r["dominio"] == "LGB+"][0]
    p1, deff, deffc = float(g["est"]), float(g["deff"]), float(g["deff_c"])
    for nome, adultos in (("A: modulo PNADC (1 ano, ~337,6 mil dom.)", H_A_ANO * REND), ("B: 1 rodada PNS 140 mil dom.", 140_000 * REND),
                          ("B': PNS 2019 (observado, 88.531 adultos)", den["adultos_18mais_com_modulo_V"])):
        nl = N_LGB_OBS if nome.startswith("B'") else adultos * PI
        cap.append(dict(indicador=ind, opcao=nome, adultos=round(adultos), n_lgb=round(nl), mde_deff_medido=round(mde(p1, nl / deff), 3),
                        mde_autoponderado=round(mde(p1, nl / deffc), 3), mde_AAS_ingenuo=round(mde(p1, nl), 3)))
with open(AQUI / "capacidade_por_opcao.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(cap[0].keys())); w.writeheader(); w.writerows(cap)

# ---- outros dominios (raca/genero): variacao minima detectavel na opcao A e no tamanho da PNS 2019 ----
dom_rows = []
T1 = lerc("deff_pns2019.csv")
for ind in ("fisica", "sexual12", "qualquer"):
    for dom in ("mulher", "homem", "negro (preta+parda)", "branco", "mulher negra", "homem negro"):
        g = [r for r in T1 if r["indicador"] == ind and r["dominio"] == dom][0]
        share = float(g["n"]) / den["adultos_18mais_com_modulo_V"]
        for nome, adultos in (("A: modulo PNADC (1 ano)", H_A_ANO * REND), ("PNS 2019 (observado)", den["adultos_18mais_com_modulo_V"])):
            nd = adultos * share
            dom_rows.append(dict(indicador=ind, dominio=dom, p_base=round(float(g["est"]), 4), deff=round(float(g["deff"]), 2), opcao=nome, n_dominio=round(nd),
                                 mde_deff_medido=round(mde(float(g["est"]), nd / float(g["deff"])), 3)))
with open(AQUI / "mde_outros_dominios.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(dom_rows[0].keys())); w.writeheader(); w.writerows(dom_rows)


# ---- resumo das 3 opcoes em UM ciclo (capacidade, MDE, custo central e faixa em R$ de set/2026) ----
T1x = lerc("deff_pns2019.csv")
gL = lambda ind: [r for r in T1x if r["indicador"] == ind and r["dominio"] == "LGB+"][0]
res = []
def linha(nome, adultos, hh, c_c, c_lo, c_hi, base):
    nl = adultos * PI
    res.append(dict(opcao=nome, domicilios=round(hh), adultos=round(adultos), n_lgb=round(nl), n_vitimas_lgb_fisica=round(nl * float(gL("fisica")["est"])),
                    n_vitimas_lgb_qualquer=round(nl * float(gL("qualquer")["est"])),
                    mde_fisica=round(mde(float(gL("fisica")["est"]), nl / float(gL("fisica")["deff"])), 3),
                    mde_qualquer=round(mde(float(gL("qualquer")["est"]), nl / float(gL("qualquer")["deff"])), 3),
                    custo_central_BRL=round(c_c), custo_faixa_min_BRL=round(c_lo), custo_faixa_max_BRL=round(c_hi),
                    custo_por_LGB_completo_BRL=round(c_c / nl), base_do_custo=base))
linha("1. Modulo PNADC (1 ano)", H_A_ANO * REND, H_A_ANO, it_A + H_A_ANO * var_hh_A, it_A + H_A_ANO * var_hh_A, H_A_ANO * pns_hh,
      "min/central = TED 02/2021 MJSP-IBGE (marginal, IPCA); max = se o modulo exigisse visita propria ao custo/domicilio do TED da PNS")
linha("2. Rodada dedicada tipo PNS (140 mil dom.)", 140_000 * REND, 140_000, 140_000 * pns_hh, 140_000 * pns_hh_140, 140_000 * pns_hh_108,
      "TED 'PNS-2024' R$22,29 mi dividido por 140 mil (min) ou 108,5 mil (max) domicilios, IPCA")
nC = 140_000 * REND
linha("3. Painel/web probabilistico (mesmo n da opcao 2)", nC, nC / REND, nC * gsgb_complete_brl, nC * gsgb_complete_brl, nC * csew_brl,
      "min/central = GSGB GBP/completo x PTAX; max = CSEW GBP/entrevista (face a face/misto); benchmark estrangeiro nominal")
with open(AQUI / "opcoes_resumo.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
for x in res: print(x)

# ---- regiao: custo no formato B (domicilio dedicado) ----
rg = lerc("n_regiao.csv")
for x in rg:
    dom = float(x["n_total_regiao_por_rodada"]) / REND if x["sobreamostra_k"] == "1" else float(x["n_lgb_por_rodada"]) / float(x["pi_lgb_regional"]) / REND
    x["domicilios_a_visitar"] = round(dom); x["B_custo_central_BRL"] = round(dom * pns_hh)
    x["nota"] = "triagem independe de k; k=5 so reduz completos" if x["sobreamostra_k"] == "5" else ""
with open(AQUI / "n_regiao_custo.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rg[0].keys())); w.writeheader(); w.writerows(rg)

# ---- resumo ----
print(f"rendimento adulto/domicilio = {REND:.4f} ; PI = {PI:.4f} ; IPCA fator 2021-09->2026-09 = {infl('202109'):.4f} ; 2023-12 = {infl('202312'):.4f}")
print(f"A: var/dom = R$ {var_hh_A:.2f}  TI unico = R$ {it_A:,.0f}  total 2 modulos/dom-trim = R$ {tot_hh_A:.2f} ; dom/ano = {H_A_ANO:,.0f} ; adultos/ano = {H_A_ANO*REND:,.0f} ; LGB/ano = {H_A_ANO*REND*PI:,.0f}")
print(f"B: R$/dom PNS (TED/140 mil) = {pns_hh_140:.2f} ; (TED/108,5 mil) = {pns_hh_108:.2f} ; central = {pns_hh:.2f}")
print(f"C: GSGB £/completo = {gsgb_complete_gbp:.1f} = R$ {gsgb_complete_brl:.0f} ; CSEW £/entrevista = {csew_gbp:.1f} = R$ {csew_brl:.0f} ; NCVS US$/pessoa = {ncvs_usd:.0f} (2013) = R$ {ncvs_brl:.0f} nominal ; FRA EUR/resposta = {fra_eur:.1f} (opt-in)")
for r in rows:
    if r["deff_base"] == "deff medido":
        print({k: r[k] for k in ("indicador", "mudanca_rel", "n_lgb_necessario", "adultos_a_triar", "domicilios_a_visitar", "A_anos_de_modulo_PNADC", "A_custo_BRL", "B_custo_central_BRL", "B_custo_min_BRL", "B_custo_max_BRL", "C_custo_BRL")})
for c in cap: print(c)
