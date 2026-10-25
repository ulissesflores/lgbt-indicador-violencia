"""S05. Ferramenta de leitura para a codificacao manual: imprime, por ordem de sorteio, a categoria GGB,
cidade/UF e um excerto da fonte (titulo + inicio + frases com termos de identidade/motivo/desfecho).
Uso: python3.14 -I s05_visualiza_lote.py <de> <ate>   (ordem_sorteio inclusiva). So leitura; nao grava nomes."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, sys
from pathlib import Path
ROOT = Path(REPO_ROOT); RAW = ROOT/"fontes/p3-ggb/_raw"
D = ROOT/"research-2026-10-21-rodada3/F3-ggb/dados"
nom = {r["id"]: r for r in csv.DictReader((RAW/"ggb2019_lista_nominal.csv").open())}
amo = list(csv.DictReader((D/"amostra.csv").open()))
chk = {r["id"]: r for r in csv.DictReader((D/"fonte_checks.csv").open())}
lo, hi = int(sys.argv[1]), int(sys.argv[2])
KW = re.compile(r"gay|homossex|homoafet|travesti|trans[a-z]*|l[eé]sbica|bissex|lgbt|homofob|transfob|orienta[cç][aã]o|motiv|suspeit|preso|presa|apreendid|ciume|ci[uú]me|assalt|roubo|roubou|d[ií]vida|briga|discuss|namorad|companheir|confess|inqu[eé]rito|delegad|autops|laudo|causa", re.I)
for r in amo:
    k = int(r["ordem_sorteio"])
    if not lo <= k <= hi: continue
    n = nom[r["id"]]; c = chk[r["id"]]
    print(f"\n##### {k} | GGB: {n['cat']} | {n['cidade']}/{n['uf']} | nome-GGB: {n['nome'][:40]} | arq={c['arquivo']} nome_no_texto={c['nome_presente']} cidade={c['cidade_presente']} soft404={c['soft404']}")
    if not int(c["arquivo"]): print("(sem arquivo)", "| fonte-GGB:", n["fonte"][:60], "| link?", bool(n["link"])); continue
    import unicodedata
    def nz(x): return unicodedata.normalize("NFKD", x.lower()).encode("ascii","ignore").decode()
    t = (RAW/"news_txt"/f"{r['id']}.txt").read_text()
    flat = re.sub(r"\s+", " ", t); fn = nz(flat)
    toks = [w for w in nz(n["nome"]).replace("/", " ").split() if len(w) >= 4 and w not in ("silva","santos","souza","filho","junior")]
    pos = [fn.find(w) for w in toks if fn.find(w) >= 0]
    print("TITULO:", t.split("\n")[0][:160])
    if pos:
        i = max(0, min(pos) - 150); print(flat[i:i+1150])
    else:
        print("[nome nao achado] ", flat[:600])
        for s_ in [s_.strip() for s_ in re.split(r"(?<=[.!?])\s+", flat) if KW.search(s_)][:4]: print("  >>", s_[:240])
