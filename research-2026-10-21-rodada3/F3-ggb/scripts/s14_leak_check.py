"""S14. Verifica que nenhum nome de vitima (tokens >=5 letras da lista nominal e do TDoR) aparece em arquivo publico da frente F3.
Uso: python3.14 -I s14_leak_check.py  (exit 1 se vazar)"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, sys, unicodedata
from pathlib import Path
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"; F3 = ROOT/"research-2026-10-21-rodada3/F3-ggb"
def nz(x): return re.sub(r"[^a-z ]", " ", unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode())
STOP = {"santos","silva","souza","oliveira","pereira","filho","junior","costa","ribeiro","rodrigues","ferreira","alves","lima","gomes","martins","carvalho","moura","araujo","barbosa","trans","gay","travesti","unknown","campos","mendes","paulo","nascimento"}  # sobrenomes muito comuns, rotulos e palavras comuns que colidem com nomes (sao paulo, campos, autores citados); prenomes de vitima NAO ficam isentos
tok = set()
for r in csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open()):
    for w in nz(r["nome"]).split():
        if len(w) >= 5 and w not in STOP: tok.add(w)
for r in csv.DictReader((RAW/"tdor/x/tdor_export.csv").open(encoding="utf-8-sig")):
    for w in nz(r["Name"]).split():
        if len(w) >= 5 and w not in STOP: tok.add(w)
bad = []
for p in F3.rglob("*"):
    if not p.is_file() or p.suffix in (".pdf", ".html") or "00-material-fonte" in str(p) or p.name == "s14_leak_check.py": continue
    try: t = nz(p.read_text(errors="ignore"))
    except Exception: continue
    words = set(t.split())
    hit = sorted(tok & words)
    if hit: bad.append((str(p), hit[:8]))
print("tokens de nome verificados:", len(tok))
for b in bad: print("VAZAMENTO:", b)
print("OK sem vazamento" if not bad else f"{len(bad)} arquivo(s) com possivel vazamento"); sys.exit(1 if bad else 0)
