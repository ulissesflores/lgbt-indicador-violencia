"""Consolida: contagens.csv (todas as fontes) e amostra_codificada.csv (+ estatisticas de precisao/fonte).
Entradas: _bruto_*.csv, _gnrss_celulas.jsonl, _amostra_*.jsonl, _codif/<universo>.json
Python: /opt/homebrew/bin/python3.14 -I."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, datetime, glob, hashlib, json, math, os, sys
from collections import Counter, defaultdict

BASE = (REPO_ROOT + "/research-2026-10-21-rodada3/discurso/midia")
hoje = datetime.date.today().isoformat()


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0, c - h), min(1, c + h)


def contagens():
    rows = []
    for fn in sorted(glob.glob(BASE + "/_bruto_*.csv")) + sorted(glob.glob(BASE + "/_v1prereg_parlamento.csv")):
        rows += list(csv.reader(open(fn)))[1:]
    # GN-RSS: o after:/before: do Google NAO foi respeitado na maioria dos itens (ano da data de publicacao != ano da celula),
    # logo o ano aqui e o da data de publicacao (pubDate) e os itens sao deduplicados por link no periodo todo.
    arq = BASE + "/_gnrss_celulas.jsonl"
    if os.path.exists(arq):
        import email.utils
        por_ent = defaultdict(dict)       # entrada -> link -> ano
        fam_links = defaultdict(dict)     # (fam, grupo) -> link -> ano
        sat = Counter(); cel = Counter(); shas = defaultdict(list)
        for l in open(arq):
            c = json.loads(l)
            ent = c["entrada"]; fam = ent[:2]
            lang = "pt" if ent.split("-")[1] == "PT" else "mundo"
            sat[ent] += int(c["saturada"]); cel[ent] += 1; shas[ent].append(c["sha"])
            for it in c["itens"]:
                try:
                    ano = email.utils.parsedate_to_datetime(it["data"]).year
                except Exception:
                    continue
                k = it["link"] or it["titulo"]
                por_ent[ent][k] = ano
                fam_links[(fam, lang)][k] = ano
        for ent, d in sorted(por_ent.items()):
            lang = "pt" if ent.split("-")[1] == "PT" else "mundo"
            cnt = Counter(d.values())
            for ano in range(2015, 2027):
                rows.append([ent[:2], "GNRSS-" + lang, ano, cnt.get(ano, 0), f"{ent} (itens unicos por link, ano = pubDate; PISO: lista truncada ~100/consulta, celulas={cel[ent]}, saturadas={sat[ent]})", hoje, hashlib.sha256("".join(shas[ent]).encode()).hexdigest()])
        for (fam, lang), d in sorted(fam_links.items()):
            cnt = Counter(d.values())
            for ano in range(2015, 2027):
                rows.append([fam, "GNRSS-" + lang, ano, cnt.get(ano, 0), f"{fam}-any (uniao deduplicada por link das entradas; ano = pubDate; piso)", hoje, "ver celulas"])
    # GDELT (resultados da fila gdelt_rodar.py)
    arq = BASE + "/_gdelt_resultados.jsonl"
    if os.path.exists(arq):
        for l in open(arq):
            g = json.loads(l)
            try:
                j = json.load(open(g["arquivo"]))
                assert "timeline" in j
            except Exception:
                rows.append([g["familia"], "GDELT", "erro/vazio", 0, g["id"] + " | " + g["consulta"] + f" | corpo={g['tam']} bytes (sem serie: NAO e zero validado)", g["data_acesso"], g["sha256"]])
                continue
            por, den = Counter(), Counter()
            for sr in j.get("timeline", []):
                for pt in sr["data"]:
                    por[pt["date"][:4]] += pt["value"]
                    den[pt["date"][:4]] += pt.get("norm", 0)
            for ano in sorted(por):
                rows.append([g["familia"], "GDELT", ano, por[ano], g["id"] + " | " + g["consulta"], g["data_acesso"], g["sha256"]])
            rows.append([g["familia"], "GDELT-denominador", "total", sum(den.values()), g["id"] + " | soma diaria de 'norm' (artigos monitorados no filtro)", g["data_acesso"], g["sha256"]])
    with open(BASE + "/contagens.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["familia", "universo", "ano", "n", "consulta", "data_acesso", "sha256"])
        w.writerows(rows)
    print("contagens.csv linhas", len(rows))


COLS = ["hash", "url", "data", "familia", "universo", "entrada", "postura", "forma", "fonte_citada", "fonte_nomeada",
        "cita_GGB", "cita_ANTRA", "cita_TGEU", "cita_ONU", "texto", "trecho_verbatim"]


def amostra():
    rows = []
    for fn in sorted(glob.glob(BASE + "/_amostra_*.jsonl")):
        uni = os.path.basename(fn)[len("_amostra_"):-len(".jsonl")]
        cod = json.load(open(f"{BASE}/_codif/{uni}.json")) if os.path.exists(f"{BASE}/_codif/{uni}.json") else {}
        for i, l in enumerate(open(fn)):
            j = json.loads(l)
            c = cod.get(str(i))
            if not c:
                continue
            tr = (j.get("trecho") or j.get("titulo") or "").replace("\n", " ")
            tr = tr[:200]
            ent = ";".join(j.get("entradas") or [])
            rows.append([j["hash"], j.get("url", ""), j.get("data", ""), j["familia"], j["universo"], ent] + c[:8] + [c[8] if len(c) > 8 else "completo", tr])
    with open(BASE + "/amostra_codificada.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows)
    print("amostra_codificada.csv linhas", len(rows))
    return rows


def estatisticas(rows):
    por = defaultdict(list)
    for r in rows:
        por[(r[3], r[4])].append(r)
    out = ["familia|universo|n_cod|acertos(nao FORA)|precisao[IC95]|AFIRMA|ATRIBUI|NEGA/CRITICA|MENCIONA|%fonte_primaria(AFIRMA+ATRIBUI)|%GGB/ANTRA/TGEU/ONU|%nenhuma_fonte"]
    for (fam, uni), rs in sorted(por.items()):
        n = len(rs)
        ac = [r for r in rs if r[6] != "FORA"]
        lo, hi = wilson(len(ac), n)
        cp = Counter(r[6] for r in rs)
        aa = [r for r in rs if r[6] in ("AFIRMA", "ATRIBUI")]
        prim = sum(r[8] == "primaria_verificavel" for r in aa)
        ong = sum(any(r[i] == "1" or r[i] == 1 for i in (10, 11, 12, 13)) for r in aa)
        nen = sum(r[8] == "nenhuma" for r in aa)
        plo, phi = wilson(prim, len(aa))
        out.append(f"{fam}|{uni}|{n}|{len(ac)}|{len(ac)/n:.2f} [{lo:.2f}-{hi:.2f}]|{cp['AFIRMA']}|{cp['ATRIBUI']}|{cp['NEGA/CRITICA']}|{cp['MENCIONA']}|"
                   f"{prim}/{len(aa)} [{plo:.2f}-{phi:.2f}]|{ong}/{len(aa)}|{nen}/{len(aa)}")
    open(BASE + "/_estatisticas_amostra.txt", "w").write("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    contagens()
    estatisticas(amostra())
