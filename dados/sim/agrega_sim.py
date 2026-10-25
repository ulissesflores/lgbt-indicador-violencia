"""Agrega os microdados do SIM (DATASUS FTP, DOBR<ano>.dbc, 2010-2024) para mortes por agressão, intenção indeterminada e intervenção legal,
por ano x UF de residência x sexo x raça/cor x faixa etária (5 anos) x arma de fogo x local do óbito.
Saída: dados/sim/sim_agressoes_agregado.csv (+ sha256 dos .dbc em fontes/p2-sim-microdados/SHA256SUMS.txt).
Grupos de causa (CID-10, causa básica): agressao X85-Y09 | indet Y10-Y34 | interv_legal Y35-Y36. arma=1 se X93-X95 (só dentro de agressao).
IDADE do SIM: 1º dígito = unidade (0 min,1 h,2 dia,3 mês,4 ano,5 = 100+ anos); 000/999/branco = ignorada.
Rodar: python  # venv com pyreaddbc + dbfread -I dados/sim/agrega_sim.py [ano ...]   (sem argumentos: 2010-2024; pula ano já agregado)
Intermediários .dbf são apagados após cada ano."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import collections, csv, hashlib, os, subprocess, sys
import pyreaddbc
from dbfread import DBF

BASE = REPO_ROOT
SRC = f"{BASE}/fontes/p2-sim-microdados"; OUT = f"{BASE}/dados/sim/sim_agressoes_agregado.csv"
UF = {'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA',
      '31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS','51':'MT','52':'GO','53':'DF'}
FAIXAS = ["<1"] + ["1-4"] + [f"{a}-{a+4}" for a in range(5, 80, 5)] + ["80+"]


def faixa(idade):
    s = str(idade or "").strip()
    if len(s) != 3 or s in ("000", "999") or not s.isdigit():
        return "ign"
    u, v = s[0], int(s[1:])
    if u in "0123":
        return "<1"
    anos = v + (100 if u == "5" else 0) if u in "45" else None
    if anos is None:
        return "ign"
    if anos < 1: return "<1"
    if anos < 5: return "1-4"
    if anos >= 80: return "80+"
    a = anos // 5 * 5
    return f"{a}-{a+4}"


def grupo(cb):
    cb = (cb or "").strip().upper()
    if len(cb) < 3: return None
    l, n = cb[0], cb[1:3]
    if not n.isdigit(): return None
    n = int(n)
    if l == "X" and n >= 85 or l == "Y" and n <= 9: return "agressao"
    if l == "Y" and 10 <= n <= 34: return "indet"
    if l == "Y" and n in (35, 36): return "interv_legal"
    return None


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def processa(ano):
    dbc = f"{SRC}/DOBR{ano}.dbc"; dbf = f"{SRC}/DOBR{ano}.dbf"
    if not os.path.exists(dbc):
        r = subprocess.run(["curl", "-sS", "-m", "900", "-o", dbc, f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DOBR{ano}.dbc"], capture_output=True, text=True)
        assert r.returncode == 0 and os.path.getsize(dbc) > 1_000_000, f"download {ano}: {r.stderr[:200]}"
        with open(f"{SRC}/SHA256SUMS.txt", "a") as f: f.write(f"{sha(dbc)}  DOBR{ano}.dbc\n")
    if not os.path.exists(dbf): pyreaddbc.dbc2dbf(dbc, dbf)
    c = collections.Counter(); tot = 0
    for r in DBF(dbf, encoding="latin-1", load=False):
        tot += 1
        g = grupo(r.get("CAUSABAS"))
        if g is None: continue
        cb = str(r.get("CAUSABAS")).strip().upper()
        arma = int(g == "agressao" and cb[:3] in ("X93", "X94", "X95"))
        sx = {"1": "M", "2": "F"}.get(str(r.get("SEXO") or "").strip(), "I")
        rc = {"1": "branca", "2": "preta", "3": "amarela", "4": "parda", "5": "indigena"}.get(str(r.get("RACACOR") or "").strip(), "ign")
        uf = UF.get(str(r.get("CODMUNRES") or "")[:2], "XX")
        loc = str(r.get("LOCOCOR") or "").strip() if g == "agressao" else ""
        c[(ano, uf, sx, rc, faixa(r.get("IDADE")), g, arma, loc)] += 1
    os.remove(dbf)
    return c, tot


def main():
    anos = [int(a) for a in sys.argv[1:]] or list(range(2010, 2025))
    feitos = set()
    if os.path.exists(OUT):
        feitos = {int(r["ano"]) for r in csv.DictReader(open(OUT, encoding="utf-8"))}
    novo = not os.path.exists(OUT)
    for ano in anos:
        if ano in feitos:
            print(ano, "já agregado", flush=True); continue
        c, tot = processa(ano)
        with open(OUT, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if novo: w.writerow(["ano", "uf", "sexo", "raca", "faixa", "grupo", "arma", "lococor", "n"]); novo = False
            for k, n in sorted(c.items()): w.writerow(list(k) + [n])
        print(ano, "óbitos totais no arquivo:", tot, "| agressao:", sum(n for k, n in c.items() if k[5] == "agressao"), "| indet:", sum(n for k, n in c.items() if k[5] == "indet"),
              "| interv_legal:", sum(n for k, n in c.items() if k[5] == "interv_legal"), flush=True)


if __name__ == "__main__":
    main()
