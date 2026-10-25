"""Séries anuais, composição, porta de entrada (balanço oficial 2011-2019) e comparação com Sinan e Anuário.
Lê SÓ saidas/d100_por_periodo.csv (sem raw/) e arquivos públicos já no projeto. PREREGISTRO-D100.md, seções 5, 6, 9 e 10.

Uso: /opt/homebrew/bin/python3.14 -I scripts/d100_series.py
Saídas: saidas/d100_serie_anual.csv, d100_composicao.csv, d100_uf_ano.csv, d100_porta_balanco.csv,
        d100_comparacao_nacional.csv, d100_comparacao_uf.csv, d100_resultados.md
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d100_comum as dc  # noqa: E402

SAI = dc.BASE / "saidas"
PROJ = dc.BASE.parents[1]  # raiz do repositório (dados/disque100 -> raiz)
BALANCO = dc.BASE / "entradas" / "balanco-lgbt-perfil-das-vitimas-uf.csv"
SINAN = PROJ / "dados/sinan/serie_campo55_uf_ano.csv"
ANUARIO = PROJ / "dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv"
POP = PROJ / "fontes/p2-f8-dados-uf/tabnet/raw/sidra_9514.json"
EDICAO_NOVA = {2022: 2024, 2023: 2025, 2024: 2026, 2025: 2026}  # mesma regra do concordancia_v2.py
NOME2UF = {"Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA", "Amapá": "AP",
           "Tocantins": "TO", "Maranhão": "MA", "Piauí": "PI", "Ceará": "CE", "Rio Grande do Norte": "RN",
           "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE", "Bahia": "BA",
           "Minas Gerais": "MG", "Espírito Santo": "ES", "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR",
           "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT",
           "Goiás": "GO", "Distrito Federal": "DF"}
SEMENTE = 20261024
B_BOOT = 5000
# unidade principal por formato (seção 3): A linha, B par vítima-suspeito, C denúncia
UNID = {"A": "linhas", "B": "pares_vitima_suspeito", "C": "denuncias"}


def ano_de(p):
    return int(p[:4])


def ler_periodos():
    d = defaultdict(int)
    fmt = {}
    for r in csv.DictReader(open(SAI / "d100_por_periodo.csv", encoding="utf-8")):
        d[(r["periodo"], r["recorte"], r["dimensao"], r["unidade"], r["categoria"])] += int(r["n"])
        fmt[r["periodo"]] = r["formato"]
    return d, fmt


def marca_ano(ano, fmts):
    m = []
    if len(set(fmts)) > 1:
        m.append("quebra_de_formato_no_ano")
    if ano == 2026:
        m.append("parcial_jan_set")
    return ";".join(m)


def serie_anual(d, fmt):
    out = []
    per_ano = defaultdict(list)
    for p, _ in dc.PERIODOS:
        if p in fmt:
            per_ano[ano_de(p)].append(p)
    unidades = ["linhas", "pares_vitima_suspeito", "denuncias", "denuncias_todas_as_linhas", "vitimas_declaradas"]
    for ano, ps in sorted(per_ano.items()):
        fmts = [fmt[p] for p in ps]
        for rec in ["canal", "grupo_lgbt", "sogi_lgbt", "motivacao_sogi"]:
            for un in unidades:
                vals = [d.get((p, rec, "total", un, "")) for p in ps]
                if all(v is None for v in vals):
                    continue
                n = sum(v or 0 for v in vals)
                completo = all(v is not None for v in vals)
                canal = sum(d.get((p, "canal", "total", un, ""), 0) for p in ps)
                out.append(dict(ano=ano, periodos="+".join(ps), formatos="+".join(fmts), recorte=rec, unidade=un, n=n,
                                pct_do_canal=round(100 * n / canal, 3) if canal and rec != "canal" else "",
                                unidade_em_todos_os_periodos=int(completo), marca=marca_ano(ano, fmts)))
    return out


def composicao(d, fmt):
    out = []
    for p, _ in dc.PERIODOS:
        if p not in fmt:
            continue
        for dim, un in [("uf", "linhas"), ("sexo_vitima", "linhas"), ("sexo_suspeito", "linhas"),
                        ("sogi_vitima", "linhas"), ("macro_violacao", "itens"), ("violacao_sogi", "itens")]:
            cats = {k[4]: v for k, v in d.items() if k[0] == p and k[1] == "grupo_lgbt" and k[2] == dim and k[3] == un}
            tot = sum(cats.values())
            for cat, n in sorted(cats.items()):
                out.append(dict(periodo=p, formato=fmt[p], recorte="grupo_lgbt", dimensao=dim, unidade=un, categoria=cat,
                                n=n, pct=round(100 * n / tot, 3) if tot else ""))
    return out


def uf_ano(d, fmt):
    """Grupo LGBT por UF e ano, na unidade principal do formato (C: UF da 1ª linha LGBT da denúncia)."""
    acc = defaultdict(int)
    fm = defaultdict(set)
    for (p, rec, dim, un, cat), n in d.items():
        if rec == "grupo_lgbt" and dim == "uf" and un == ("linhas" if fmt[p] in "AB" else "denuncias"):
            acc[(ano_de(p), cat)] += n
            fm[ano_de(p)].add(fmt[p])
    return [dict(ano=a, uf=u, n=n, formatos="+".join(sorted(fm[a])), unidade="linhas" if fm[a] <= {"A", "B"} else
                 ("denuncias" if fm[a] == {"C"} else "misto"), marca=marca_ano(a, fm[a])) for (a, u), n in sorted(acc.items())]


def ler_balanco():
    """Tabela 'Perfil das Vítimas - Sexo' do balanço LGBT 2011-2019: linha 'Total' por ano e UF."""
    rows = list(csv.reader(open(BALANCO, encoding="utf-8")))
    out = {}
    for i, r in enumerate(rows):
        for j, cel in enumerate(r):
            if "Perfil das V" in cel and cel.strip().endswith("Sexo"):
                ano = int(cel.split("Ano")[1].strip()[:4])
                cab = rows[i + 1]
                k = i + 2
                while rows[k][j].strip() != "Total":
                    k += 1
                tot = rows[k]
                for c in range(j + 1, len(cab)):
                    nome = cab[c].strip()
                    if nome == "%":
                        break
                    v = tot[c].strip()
                    out[(ano, nome)] = int(v) if v else 0
    return out


def porta(d, fmt):
    bal = ler_balanco()
    out = []
    for p, _ in dc.PERIODOS:
        if fmt.get(p) != "A":
            continue
        a = ano_de(p)
        for u in dc.UFS + ["NA", "TOTAL"]:
            if u == "TOTAL":
                mic = d.get((p, "grupo_lgbt", "total", "linhas", ""), 0)
            elif u == "NA":  # coluna 'NA' do balanço x UF não informada/ausente nos microdados
                mic = sum(d.get((p, "grupo_lgbt", "uf", "linhas", k), 0) for k in ("nao_informado", "ausente", "nao_se_aplica"))
            else:
                mic = d.get((p, "grupo_lgbt", "uf", "linhas", u), 0)
            b = bal.get((a, u))
            out.append(dict(ano=a, uf=u, microdados_linhas_grupo_lgbt=mic, balanco_total_vitimas=b if b is not None else "",
                            diferenca=(mic - b) if b is not None else ""))
    return out


# ---- comparação (seção 10) ----
def rank(x):
    from scipy.stats import rankdata
    return rankdata(x)


def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


def residuo(a, z):
    A = np.column_stack([np.ones_like(z), z])
    return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]


def parcial(x, y, z):
    rz = rank(z)
    return corr(residuo(rank(x), rz), residuo(rank(y), rz))


def comparacao(ufano):
    pop = {NOME2UF[x["D1N"]]: float(x["V"]) for x in json.load(open(POP, encoding="utf-8"))[1:]}
    sin = {}
    sin_br = {}
    for r in csv.DictReader(open(SINAN, encoding="utf-8")):
        (sin_br if r["uf"] == "BR" else sin)[(int(r["ano"]), r["uf"]) if r["uf"] != "BR" else int(r["ano"])] = int(r["m_lgbtfobia"])
    anu, anu_br = {}, {}
    for r in csv.DictReader(open(ANUARIO, encoding="utf-8")):
        a, ed = int(r["ano_dado"]), int(r["edicao"])
        if EDICAO_NOVA.get(a) != ed or r["registros"] == "":
            continue
        if r["uf"] == "BR":
            anu_br[a] = int(r["registros"])
        else:
            anu[(a, r["uf"])] = int(r["registros"])
    dis = {(r["ano"], r["uf"]): r["n"] for r in ufano}
    un = {r["ano"]: (r["unidade"], r["marca"]) for r in ufano}
    rng = np.random.default_rng(SEMENTE)
    nac, ufc = [], []
    anos = sorted({r["ano"] for r in ufano})
    for a in anos:
        dbr = sum(n for (aa, u), n in dis.items() if aa == a)
        nac.append(dict(ano=a, disque100_grupo_lgbt=dbr, disque100_unidade=un[a][0], disque100_marca=un[a][1],
                        sinan_notificacoes_motivacao_lgbtfobia=sin_br.get(a, ""), anuario_bo_racismo_homofobia_transfobia=anu_br.get(a, "")))
    for a in anos:
        if un[a][0] == "misto" or un[a][1]:
            continue  # 2020 (dois formatos) e 2026 (parcial) fora da comparação por UF (seção 10)
        for nome, ref in [("sinan", sin), ("anuario", anu)]:
            ufs = [u for u in dc.UFS if (a, u) in ref]
            if len(ufs) < 10:
                continue
            x = np.array([dis.get((a, u), 0) for u in ufs], float)
            y = np.array([ref[(a, u)] for u in ufs], float)
            z = np.array([pop[u] for u in ufs], float)
            rho = corr(rank(x), rank(y))
            rxz, ryz = corr(rank(x), rank(z)), corr(rank(y), rank(z))
            pr = parcial(x, y, z)
            boot = []
            n = len(ufs)
            for _ in range(B_BOOT):
                i = rng.integers(0, n, n)
                try:
                    v = parcial(x[i], y[i], z[i])
                except Exception:
                    continue
                if np.isfinite(v):
                    boot.append(v)
            lo, hi = np.percentile(boot, [2.5, 97.5])
            ufc.append(dict(ano=a, comparada_com=nome, n_ufs=n, disque100_unidade=un[a][0], rho_contagens=round(rho, 3),
                            rho_disque_pop=round(rxz, 3), rho_ref_pop=round(ryz, 3), rho_so_tamanho=round(rxz * ryz, 3),
                            rho_parcial_dado_pop=round(pr, 3), ic95_parcial_lo=round(lo, 3), ic95_parcial_hi=round(hi, 3)))
    return nac, ufc


def grava(nome, linhas):
    if not linhas:
        return
    with open(SAI / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def main():
    import d100_selo
    d100_selo.conferir()
    d, fmt = ler_periodos()
    sa = serie_anual(d, fmt)
    comp = composicao(d, fmt)
    ua = uf_ano(d, fmt)
    pt = porta(d, fmt)
    nac, ufc = comparacao(ua)
    grava("d100_serie_anual.csv", sa)
    grava("d100_composicao.csv", comp)
    grava("d100_uf_ano.csv", ua)
    grava("d100_porta_balanco.csv", pt)
    grava("d100_comparacao_nacional.csv", nac)
    grava("d100_comparacao_uf.csv", ufc)
    print("ok", len(sa), len(comp), len(ua), len(pt), len(nac), len(ufc))


if __name__ == "__main__":
    main()
