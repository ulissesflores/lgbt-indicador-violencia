"""H1 insumo: óbitos por UF de residência x ano 1996-2024 do SIM/DATASUS (TabNet ext10uf), 3 grandes grupos CID-10:
4 = X85-Y09 agressões | 5 = Y10-Y34 intenção indeterminada (MVCI) | 6 = Y35-Y36 intervenções legais/guerra.
Bruto (.prn latin1) vai para dados/raw/ com sha256 em dados/raw/SHA256SUMS.txt. Saída: dados/h1_sim_tabnet_uf_ano.csv.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h1_01_tabnet_sim_1996_2024.py   (TabNet é instável: o script tenta 5x por consulta)"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, hashlib, html, io, os, re, subprocess, sys, time, urllib.parse
BASE = (REPO_ROOT + "/research-2026-10-21-rodada3/F5-economia-politica")
RAW = f"{BASE}/dados/raw"; OUT = f"{BASE}/dados/h1_sim_tabnet_uf_ano.csv"
CGI = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10uf.def"
ANOS = list(range(1996, 2025))  # 2025/2026 preliminares: fora
GRUPOS = {"agressao_X85_Y09": "4", "indet_Y10_Y34": "5", "interv_Y35_Y36": "6"}

def consulta(tag, grupo):
    pares = [("Linha", "Unidade_da_Federação"), ("Coluna", "Ano_do_Óbito"), ("Incremento", "Óbitos_p/Residênc"),
             ("formato", "prn"), ("mostre", "Mostra"), ("SGrande_Grupo_CID10", grupo)]
    pares += [("Arquivos", f"extuf{str(a)[2:]}.dbf") for a in ANOS]
    body = urllib.parse.urlencode(pares, encoding="latin-1")
    path = f"{RAW}/tabnet_{tag}.prn"
    for t in range(5):
        r = subprocess.run(["curl", "-sS", "-m", "180", "-o", path, "-w", "%{http_code}", "-X", "POST", "--data", body, CGI], capture_output=True, text=True)
        txt = open(path, "rb").read().decode("latin1")
        if r.stdout.strip() == "200" and "Unidade da Federa" in txt and "1996" in txt:
            return path, txt
        time.sleep(15)
    raise SystemExit(f"TabNet não respondeu com tabela para {tag}")

def parse(txt):
    header, rows = None, {}
    for rec in csv.reader(io.StringIO(txt), delimiter=";", quotechar='"'):
        if not rec: continue
        first = html.unescape(rec[0]).strip()
        if first.startswith("Unidade da Federação"):
            header = [html.unescape(h).strip() for h in rec]; continue
        if header is None or first == "Total": continue
        m = re.match(r"^(\d{2}) (.+)$", first)
        if not m: continue
        rows[m.group(1)] = {int(h): (0 if v.strip() == "-" else int(v)) for h, v in zip(header[1:], rec[1:]) if h.isdigit() and (v.strip() == "-" or v.strip().isdigit())}
    return rows

def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()

def main():
    os.makedirs(RAW, exist_ok=True)
    dados, sums = {}, []
    for tag, g in GRUPOS.items():
        p, txt = consulta(tag, g); dados[tag] = parse(txt); sums.append(f"{sha(p)}  tabnet_{tag}.prn")
        print(tag, len(dados[tag]), "UFs", file=sys.stderr)
    open(f"{RAW}/SHA256SUMS.txt", "w").write("\n".join(sums) + "\n")
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["cod_uf", "ano"] + list(GRUPOS))
        for cod in sorted(dados["agressao_X85_Y09"]):
            for a in ANOS:
                w.writerow([cod, a] + [dados[t].get(cod, {}).get(a, "") for t in GRUPOS])
    print("ok", OUT)
main()
