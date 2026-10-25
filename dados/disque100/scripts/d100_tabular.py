"""Tabulação PRÉ-REGISTRADA do Disque 100 (PREREGISTRO-D100.md, seções 3 a 8). Só roda se o hash do
pré-registro e do d100_comum.py baterem com PREREGISTRO-D100.sha256.

Uma passada por arquivo (processos em paralelo, um por arquivo). Para cada período grava contagens em
formato longo; nenhuma chave, município ou texto livre sai do processo.

Uso: /opt/homebrew/bin/python3.14 -I scripts/d100_tabular.py [--workers 4] [--so 2011,2012]
Saídas: saidas/d100_por_periodo.csv (longo), saidas/d100_qualidade.csv, saidas/d100_sobreposicao_hash.csv
"""

import argparse
import concurrent.futures as cf
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d100_comum as dc  # noqa: E402

SAIDAS = dc.BASE / "saidas"
CLASSES = ["trans", "lgb", "intersexo", "lgbt_genero", "nao_lgbt", "nao_rotulo_nao", "cis_ou_indef",
           "nao_informado", "ausente", "nao_se_aplica", "outro"]
BIT = {c: 1 << i for i, c in enumerate(CLASSES)}
F_I1, F_I2, F_I3 = 1, 2, 4  # bits de recorte por linha
RECORTES = [("canal", 0), ("grupo_lgbt", F_I1), ("sogi_lgbt", F_I2), ("motivacao_sogi", F_I3)]


def intervalo(periodo):
    a = periodo[:4]
    if len(periodo) == 4:
        return f"{a}-01-01", f"{a}-12-31"
    return {"S1": (f"{a}-01-01", f"{a}-06-30"), "S2": (f"{a}-07-01", f"{a}-12-31"),
            "T3": (f"{a}-07-01", f"{a}-09-30")}[periodo[4:]]


def dig(s):
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest(), "big")


def tabular(periodo, path=None):
    c = Counter()  # (recorte, dimensao, unidade, categoria) -> n
    q = Counter()
    ini, fim = intervalo(periodo)
    vistas = set()
    pares = {r: set() for r, _ in RECORTES}       # B
    den = {}                                      # C: hash -> [flags_any, flags_all, qtd, uf_canal, uf_i1, uf_var, classes]
    fmt = None
    for fmt, row in dc.ler(periodo, path):
        if row is None:
            q["linhas_malformadas"] += 1
            continue
        q["linhas"] += 1
        h = dig("\x1f".join(row.values()))
        if h in vistas:
            q["linhas_identicas_repetidas"] += 1
        else:
            vistas.add(h)
        d = dc.data_iso(dc.campo(fmt, row, "data"))
        if d is None:
            q["linhas_sem_data"] += 1
        elif not (ini <= d <= fim):
            q["linhas_data_fora_do_periodo"] += 1
        i1 = dc.grupo_lgbt(dc.campo(fmt, row, "grupo"))
        cls = dc.sogi_vitima(fmt, row)
        i2 = cls in dc.SOGI_LGBT
        m = dc.motivacao_sogi(fmt, row)
        flags = (F_I1 if i1 else 0) | (F_I2 if i2 else 0) | (F_I3 if m else 0)
        uf = dc.uf(dc.campo(fmt, row, "uf"))
        sv = dc.sexo(dc.campo(fmt, row, "sexo_vitima"))
        ss = dc.sexo(dc.campo(fmt, row, "sexo_suspeito"))
        viol = dc.violacoes(fmt, row)
        # interseção completa (unidade: linha)
        c[("canal", "intersecao", "linhas", f"i1={int(i1)}|sogi={cls}|i3={'na' if m is None else int(m)}")] += 1
        for rec, bit in RECORTES:
            if bit and not (flags & bit):
                continue
            c[(rec, "total", "linhas", "")] += 1
            c[(rec, "uf", "linhas", uf)] += 1
            c[(rec, "sexo_vitima", "linhas", sv)] += 1
            c[(rec, "sexo_suspeito", "linhas", ss)] += 1
            c[(rec, "sogi_vitima", "linhas", cls)] += 1
            if not viol:
                c[(rec, "macro_violacao", "itens", "sem_violacao")] += 1
            for v in viol:
                c[(rec, "macro_violacao", "itens", dc.macro_violacao(v))] += 1
                c[(rec, "violacao_sogi", "itens", str(int(dc.violacao_sogi(v))))] += 1
            if fmt == "B":
                pares[rec].add(dig(row["hash_par_vitima_suspeito"]))
        if fmt == "C":
            k = dig(row["hash"])
            qtd = row["sl_quantidade_vitimas"].strip()
            qtd = int(qtd) if qtd.isdigit() else 0
            r = den.get(k)
            if r is None:
                den[k] = [flags, flags, qtd, uf, uf if i1 else None, 0, BIT[cls]]
            else:
                r[0] |= flags
                r[1] &= flags
                r[2] = max(r[2], qtd)
                if uf != r[3]:
                    r[5] = 1
                if i1 and r[4] is None:
                    r[4] = uf
                r[6] |= BIT[cls]
    if fmt == "B":
        for rec, _ in RECORTES:
            c[(rec, "total", "pares_vitima_suspeito", "")] = len(pares[rec])
    hashes = set()
    if fmt == "C":
        hashes = set(den)
        q["denuncias_com_uf_variando"] = sum(r[5] for r in den.values())
        for rec, bit in RECORTES:
            sel = [r for r in den.values() if (not bit) or (r[0] & bit)]
            c[(rec, "total", "denuncias", "")] = len(sel)
            c[(rec, "total", "vitimas_declaradas", "")] = sum(r[2] for r in sel)
            for r in sel:
                c[(rec, "uf", "denuncias", (r[4] if rec == "grupo_lgbt" else r[3]))] += 1
                for cl in CLASSES:
                    if r[6] & BIT[cl]:
                        c[(rec, "sogi_vitima", "denuncias_com_a_classe", cl)] += 1
        c[("grupo_lgbt", "total", "denuncias_todas_as_linhas", "")] = sum(1 for r in den.values() if r[1] & F_I1)
        for r in den.values():
            c[("canal", "intersecao", "denuncias", f"i1={int(bool(r[0] & F_I1))}|sogi_lgbt={int(bool(r[0] & F_I2))}"
                                                    f"|i3={int(bool(r[0] & F_I3))}")] += 1
    return periodo, fmt, c, q, hashes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--so", default="")
    a = ap.parse_args()
    import d100_selo
    d100_selo.conferir()  # aborta se o pré-registro ou as regras mudaram
    tam = {Path(r["url"]).name: int(r["bytes_anunciados"]) for r in
           csv.DictReader(open(dc.BASE / "scripts/urls.tsv", encoding="utf-8"), delimiter="\t")}
    periodos = [p for p, f in dc.PERIODOS if (not a.so or p in a.so.split(","))
                and dc.caminho(p).exists() and dc.caminho(p).stat().st_size == tam[f]]
    faltam = [p for p, _ in dc.PERIODOS if p not in periodos]
    print("tabulados:", periodos, "| AUSENTES (incompletos ou fora do selo):", faltam, flush=True)
    res = {}
    with cf.ProcessPoolExecutor(a.workers) as ex:
        for p, fmt, c, q, hs in ex.map(tabular, periodos):
            res[p] = (fmt, c, q, hs)
            print(p, fmt, q["linhas"], flush=True)
    SAIDAS.mkdir(exist_ok=True)
    sufixo = ""
    with open(SAIDAS / f"d100_por_periodo{sufixo}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["periodo", "formato", "recorte", "dimensao", "unidade", "categoria", "n"])
        for p in periodos:
            fmt, c, _, _ = res[p]
            for (rec, dim, un, cat), n in sorted(c.items()):
                w.writerow([p, fmt, rec, dim, un, cat, n])
    with open(SAIDAS / f"d100_qualidade{sufixo}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        chaves = ["linhas", "linhas_malformadas", "linhas_identicas_repetidas", "linhas_sem_data",
                  "linhas_data_fora_do_periodo", "denuncias_com_uf_variando"]
        w.writerow(["periodo", "formato"] + chaves)
        for p in periodos:
            fmt, _, q, _ = res[p]
            w.writerow([p, fmt] + [q.get(k, 0) for k in chaves])
    cs = [p for p in periodos if res[p][0] == "C"]
    with open(SAIDAS / f"d100_sobreposicao_hash{sufixo}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["periodo_a", "periodo_b", "denuncias_a", "denuncias_b", "hashes_em_comum"])
        for x, y in zip(cs, cs[1:]):
            w.writerow([x, y, len(res[x][3]), len(res[y][3]), len(res[x][3] & res[y][3])])


if __name__ == "__main__":
    main()
