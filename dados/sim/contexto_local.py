"""N3 (contexto) do F10 a partir dos microdados do SIM: onde ocorrem e com que meio as mortes por agressão, por sexo x raça, 2022-2024 agregado.
LOCOCOR: 1 hospital, 2 outro estabelecimento de saúde, 3 domicílio, 4 via pública, 5 outros, 6 aldeia indígena, 9/branco ignorado. arma = X93-X95.
Proporções BRUTAS (não padronizadas: o interesse é o perfil do contexto, não a taxa); local ignorado/branco excluído do denominador e reportado.
Proxy (⚠️): 'domicílio' NÃO é 'violência doméstica' (inclui crimes de rua cujo óbito é no domicílio e exclui a violência doméstica cuja morte ocorre no hospital): é o proxy que o Atlas usa (35,2% das mulheres em 2024).
Rodar: /opt/homebrew/bin/python3.14 -I dados/sim/contexto_local.py   Saída: dados/sim/contexto_local.md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import pandas as pd
BASE = (REPO_ROOT + "/dados/sim")
df = pd.read_csv(f"{BASE}/sim_agressoes_agregado.csv", dtype={"lococor": str})
d = df[(df.grupo == "agressao") & df.ano.isin([2022, 2023, 2024]) & df.sexo.isin(["M", "F"]) & df.raca.isin(["branca", "preta", "amarela", "parda", "indigena"])].copy()
d["negro"] = d.raca.isin(["preta", "parda"]); d["lococor"] = d.lococor.fillna("").str.strip()
LOC = {"1": "hospital", "2": "outro serviço de saúde", "3": "domicílio", "4": "via pública", "5": "outros", "6": "aldeia"}
d["loc"] = d.lococor.map(LOC).fillna("ignorado")
L = ["# Contexto do óbito por agressão (SIM 2022-2024 agregado; proporções brutas)", "", "| grupo | óbitos | % domicílio | % via pública | % hospital/saúde | % outros | local ignorado (% do grupo) | % arma de fogo |", "|---|---|---|---|---|---|---|---|"]
for nome, f in (("Mulheres negras", (d.sexo == "F") & d.negro), ("Mulheres não negras", (d.sexo == "F") & ~d.negro), ("Homens negros", (d.sexo == "M") & d.negro), ("Homens não negros", (d.sexo == "M") & ~d.negro), ("Mulheres", d.sexo == "F"), ("Homens", d.sexo == "M")):
    g = d[f]; n = g.n.sum(); c = g[g["loc"] != "ignorado"]; nc = c.n.sum()
    p = lambda k: 100 * c[c["loc"].isin(k)].n.sum() / nc
    L.append(f"| {nome} | {n:,} | {p(['domicílio']):.1f} | {p(['via pública']):.1f} | {p(['hospital','outro serviço de saúde']):.1f} | {p(['outros','aldeia']):.1f} | {100*(n-nc)/n:.1f} | {100*g[g.arma==1].n.sum()/n:.1f} |")
L += ["", "Leitura: contexto por sexo (domicílio/arma) é o proxy de padrão de gênero sem campo de motivação (N3). NÃO é motivação (N4): ver dossiê §1.", ""]
open(f"{BASE}/contexto_local.md", "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
