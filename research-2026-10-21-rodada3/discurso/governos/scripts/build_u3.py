"""U3 do PRE-REGISTRO: 65 Estados-membros da ONU que a ILGA DB marca como criminalizadores.
Entradas: ilga-db-csssa-all.json, vdemdata-vdem.RData, vdemdata-vparty.RData (em fontes/q1-textointegral/discurso/governos/).
Saida: ../u3_65_criminalizam.csv. Requer pyreadr e pycountry (venv do scratchpad). Nao inventa: campo ausente = vazio."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import json, sys, csv, math
import pyreadr, pycountry, pandas as pd
F = (REPO_ROOT + "/fontes/q1-textointegral/discurso/governos/")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/governos/u3_65_criminalizam.csv")
ilga = json.load(open(F + "ilga-db-csssa-all.json"))["data"]["entriesCsssa"]
vd = pyreadr.read_r(F + "vdemdata-vdem.RData")["vdem"]
vp = pyreadr.read_r(F + "vdemdata-vparty.RData")["vparty"]
ROW = {0: "autocracia fechada", 1: "autocracia eleitoral", 2: "democracia eleitoral", 3: "democracia liberal"}
LEG = ["nacionalista", "socialista/comunista", "restauradora/conservadora", "separatista/autonomista", "religiosa"]
OVR = {"XK": "XKX", "PS": "PSE"}  # nao usados: UN members only
rows = []
for e in ilga:
    m = e["motherEntry"]; j = m["jurisdiction"]
    if m["subjurisdiction"] or not j["un_member"] or e["legal"]:
        continue
    a3 = pycountry.countries.get(alpha_2=j["a2_code"]).alpha_3
    pen = (e["entry_csssa_penalty"] or {}).get("name", "")
    dpv = (e["entry_csssa_death_penalty_value"] or {}).get("name", "")
    pm = {"Yes": "legal" if a3 != "NGA" else "legal_subnacional(12 estados)", "No legal certainty": "possivel(sem certeza legal)"}.get(dpv, "nao")
    c = vd[vd.country_text_id == a3].sort_values("year")
    r = c[c.v2x_regime.notna()]
    rr = r.iloc[-1] if len(r) else None
    l = c[c.v2exl_legitideol.notna()]
    ll = l.iloc[-1] if len(l) else None
    cats = ""; cy = ""
    k = c[c.v2exl_legitideolcr_0.notna()]
    if len(k):
        kk = k.iloc[-1]; cy = int(kk.year)
        cats = ";".join(f"{LEG[i]}={kk.get(f'v2exl_legitideolcr_{i}'):.2f}" for i in range(5))  # fracao de codificadores que marcou (ADENDO do PRE-REGISTRO)
    # R1 (apos ADENDO): partido do chefe = V-Dem v2exparhos (chefe de Estado) no ultimo ano com dado; 'technical'/'independent' = sem partido.
    ch = c[c.v2exnamhos.notna()]
    hos = ch.iloc[-1] if len(ch) else None
    hosp = (hos.v2exparhos if hos is not None else "")
    party = ""; pyear = ""; plr = ""; plg = ""; defas = ""; vpn = ""
    if hos is not None and str(hosp).lower() not in ("technical", "independent", "nan", ""):
        pv = vp[vp.country_text_id == a3]
        toks = lambda x: set(w for w in "".join(ch_ if ch_.isalnum() else " " for ch_ in str(x).lower()).split() if len(w) > 2)
        best = None
        for n, g in pv.groupby("v2paenname"):
            sc = len(toks(n) & toks(hosp)) / max(1, len(toks(n) | toks(hosp)))
            if sc >= 0.5 and (best is None or sc > best[0]): best = (sc, n)
        if best:
            g = pv[(pv.v2paenname == best[1])].sort_values("year").iloc[-1]
            party = best[1]; pyear = int(g.year); plr = g.get("v2pariglef_ord"); plg = g.get("v2palgbt_ord"); defas = 2025 - int(g.year)
    rows.append(dict(pais=j["name"], iso3=a3, penalidade_ilga=pen, pena_morte=pm,
        regime_row=(int(rr.v2x_regime) if rr is not None else ""), regime_row_rotulo=(ROW[int(rr.v2x_regime)] if rr is not None else "sem_dado"),
        regime_ano=(int(rr.year) if rr is not None else ""),
        legit_ideol_intervalo_z=(round(ll.v2exl_legitideol, 3) if ll is not None else ""), legit_ideol_ano=(int(ll.year) if ll is not None else ""), legit_categorias=cats, legit_categorias_ano=cy,
        hos_nome=(hos.v2exnamhos if hos is not None else ""), hos_titulo=(hos.v2extithos if hos is not None else ""), hos_ano=(int(hos.year) if hos is not None else ""), hos_partido_vdem=hosp, partido_vparty_casado=party, vparty_eleicao=pyear, vparty_defasagem_anos_ate_2025=defas, pariglef_ord_0a6_economico=plr, palgbt_ord_0a4=plg))
df = pd.DataFrame(rows).sort_values("pais")
df.to_csv(OUT, index=False)
print(len(df)); print(df.regime_row_rotulo.value_counts()); print(df.pena_morte.value_counts()); print((df.partido_chefe_vparty != "").sum(), "com partido V-Party")
