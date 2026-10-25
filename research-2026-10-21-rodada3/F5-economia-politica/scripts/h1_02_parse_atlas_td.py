"""H1 insumo 2: tabelas por UF-ano do Atlas da Violência 2026 (Tab 2.2 registrados, 3.3 ocultos, 3.5 MVCI; anos 2014-2024),
do Atlas 2025 (Tab 3.3 ocultos, 2013-2023) e do TD Ipea 3015 (Cerqueira & Lins 2024; Tabelas A.4 registrados e A.5 ocultos 1996-2021, xlsx do repositório).
Saída: dados/h1_atlas_td_uf_ano.csv (fonte,tabela,cod_uf,ano,valor) + dados/h1_atlas_parse_checks.txt (totais Brasil lidos x soma das UFs).
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h1_02_parse_atlas_td.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, hashlib
import pandas as pd
P = REPO_ROOT
B = f"{P}/research-2026-10-21-rodada3/F5-economia-politica"
COD = {"Rondônia":11,"Acre":12,"Amazonas":13,"Roraima":14,"Pará":15,"Amapá":16,"Tocantins":17,"Maranhão":21,"Piauí":22,"Ceará":23,"Rio Grande do Norte":24,
       "Paraíba":25,"Pernambuco":26,"Alagoas":27,"Sergipe":28,"Bahia":29,"Minas Gerais":31,"Espírito Santo":32,"Rio de Janeiro":33,"São Paulo":35,"Paraná":41,
       "Santa Catarina":42,"Rio Grande do Sul":43,"Mato Grosso do Sul":50,"Mato Grosso":51,"Goiás":52,"Distrito Federal":53,"Brasília":53}
def num(s): return int(s.replace(".", ""))
def tabela(txt_path, marca, anos):
    L = open(txt_path, encoding="utf-8").read().split("\n")
    i = next(k for k, l in enumerate(L) if l.strip() == marca)
    out, br = {}, None
    for l in L[i + 1:i + 120]:
        m = re.match(r"^\s*(Brasil|[A-Za-zÀ-ÿ ]+?)\s{2,}((?:\d{1,3}(?:\.\d{3})*\s+){%d}\d{1,3}(?:\.\d{3})*)(?=\s|$)" % (len(anos) - 1), l)
        if not m: continue
        v = [num(x) for x in m.group(2).split()]
        if m.group(1) == "Brasil": br = v
        elif m.group(1) in COD: out[COD[m.group(1)]] = v
    assert len(out) == 27, (marca, len(out))
    return out, br
rows, chk = [], []
fontes = [("atlas2026", f"{P}/fontes/t1-atlas-2026/atlas2026.txt", list(range(2014, 2025)), [("TABELA 2.2", "registrados"), ("TABELA 3.3", "ocultos"), ("TABELA 3.5", "mvci_Y10_Y34")]),
          ("atlas2025", f"{P}/fontes/t1-atlas-2025/atlas2025.txt", list(range(2013, 2024)), [("TABELA 3.3", "ocultos")])]
for nome, path, anos, tabs in fontes:
    for marca, tag in tabs:
        d, br = tabela(path, marca, anos)
        for cod, v in d.items():
            for a, x in zip(anos, v): rows.append((nome, tag, cod, a, x))
        s = [sum(d[c][k] for c in d) for k in range(len(anos))]
        chk.append(f"{nome} {marca} {tag}: soma UFs {s} | Brasil lido {br} | dif {[a-b for a,b in zip(s,br)]}")
for t, tag in (("A.4", "registrados"), ("A.5", "ocultos")):
    x = pd.read_excel(f"{P}/fontes/q1-textointegral/F5/TABELA_{t}.xlsx")
    for _, r in x.iterrows():
        for a in range(1996, 2022): rows.append(("td3015", tag, COD[r["UF"]], a, int(r[a])))
    chk.append(f"td3015 {t} {tag}: {len(x)} UFs x {x.shape[1]-1} anos; soma Brasil 2021 = {int(x[2021].sum())}")
with open(f"{B}/dados/h1_atlas_td_uf_ano.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["fonte", "tabela", "cod_uf", "ano", "valor"]); w.writerows(rows)
open(f"{B}/dados/h1_atlas_parse_checks.txt", "w").write("\n".join(chk) + "\n")
print("\n".join(chk)); print(len(rows), "linhas")
