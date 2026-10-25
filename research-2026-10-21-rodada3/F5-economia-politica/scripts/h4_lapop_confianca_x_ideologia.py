"""H4 (proxy): confiança em instituições x autoposição esquerda-direita, Brasil, microdados LAPOP/AmericasBarometer (2021, 2023).
O QUESTIONÁRIO Brasil 2023 foi lido (fontes/q1-textointegral/F5/lapop_bra2023_questionario.pdf, sha256 58c55ca9...): tem B18 (confiança na Polícia Militar, 1-7), B12 (Forças Armadas), B13 (Legislativo), B47A (eleições),
L1N (esquerda 1 - direita 10), e NENHUM item sobre IBGE/estatísticas oficiais. Logo o construto 'confiança em estatística oficial' NÃO é medido; B18 e B47A são proxies de confiança em instituição de Estado que produz/registra dado.
Uso: python3.14 -I h4_lapop_confianca_x_ideologia.py <arquivo.dta> <ano>   (o .dta exige aceite dos termos de uso do LAPOP no site e NÃO é redistribuído: guardar em fontes/q1-textointegral/F5/lapop/, ignorada pelo git)
Saída: dados/h4_lapop_<ano>.csv. Semente fixa. Pesos: variável 'wt' (documentação LAPOP). Bootstrap de 5000 reamostragens ponderadas."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import sys, numpy as np, pandas as pd
B = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
def main(path, ano):
    d = pd.read_stata(path, convert_categoricals=False); d.columns = [c.lower() for c in d.columns]
    pick = [c for c in ("b18", "b12", "b13", "b47a", "l1n", "l1", "wt") if c in d.columns]
    d = d[pick].copy(); ideol = "l1n" if "l1n" in d.columns else "l1"
    for c in pick:
        d[c] = pd.to_numeric(d[c], errors="coerce"); d.loc[d[c] > 100, c] = np.nan      # códigos 888888/988888 = NS/NR
    d["grupo"] = pd.cut(d[ideol], [0, 3, 7, 10], labels=["esquerda(1-3)", "centro(4-7)", "direita(8-10)"])
    rng = np.random.default_rng(20261025); rows = []
    w = d["wt"].fillna(1.0) if "wt" in d.columns else pd.Series(1.0, index=d.index)
    for item in [c for c in ("b18", "b12", "b13", "b47a") if c in d.columns]:
        x = d[[item, "grupo"]].assign(w=w).dropna(); x["conf_0_100"] = (x[item] - 1) / 6 * 100
        def wm(df): return np.average(df.conf_0_100, weights=df.w) if len(df) else np.nan
        for g, s in x.groupby("grupo", observed=True): rows.append(dict(ano=ano, item=item, grupo=g, n=len(s), media_0_100=wm(s)))
        e, dr = x[x.grupo == "esquerda(1-3)"], x[x.grupo == "direita(8-10)"]
        bs = [wm(dr.sample(len(dr), replace=True, random_state=int(rng.integers(1 << 30)))) - wm(e.sample(len(e), replace=True, random_state=int(rng.integers(1 << 30)))) for _ in range(5000)]
        rows.append(dict(ano=ano, item=item, grupo="DIFERENCA direita-esquerda", n=len(e) + len(dr), media_0_100=wm(dr) - wm(e), ic95_lo=np.percentile(bs, 2.5), ic95_hi=np.percentile(bs, 97.5)))
    out = pd.DataFrame(rows); out.to_csv(f"{B}/dados/h4_lapop_{ano}.csv", index=False); print(out.round(2).to_string())
if __name__ == "__main__": main(sys.argv[1], int(sys.argv[2]))
