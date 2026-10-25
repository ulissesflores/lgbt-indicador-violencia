"""Extrai mandatos de governador das listas da Wikipedia pt (baixadas em fontes/.../governadores/).
Saída intermediária: mandatos com nome, início, fim, partido (quando a tabela tem coluna de partido).
Recorte: 2011-01-01 a 2026-12-31; 'Atual' = 2026-10-11 (data do download)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, datetime, glob, html, json, os, re, sys

BASE = REPO_ROOT
GOV = os.path.join(BASE, "fontes/p2-f8-dados-uf/governadores")
MESES = {m: i for i, m in enumerate(["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
                                     "agosto", "setembro", "outubro", "novembro", "dezembro"], 1)}
DATA_RE = re.compile(r"(\d{1,2})\s+de\s+([a-zçõãáéíóú]+)\s+de\s+(\d{4})", re.I)
DMY_RE = re.compile(r"(\d{2})/(\d{2})/(\d{4})")
HOJE = datetime.date(2026, 10, 11)
UF_FILE = {"Acre": "wiki_acre_fix.html", "Alagoas": "wiki_Alagoas.html", "Amapá": "wiki_Amap_.html",
           "Amazonas": "wiki_Amazonas.html", "Bahia": "wiki_Bahia.html", "Ceará": "wiki_Cear_.html",
           "Distrito Federal": "wiki_Distrito_Federal.html", "Espírito Santo": "wiki_Esp_rito_Santo.html",
           "Goiás": "wiki_Goi_s.html", "Maranhão": "wiki_Maranh_o.html", "Mato Grosso": "wiki_Mato_Grosso.html",
           "Mato Grosso do Sul": "wiki_Mato_Grosso_do_Sul.html", "Minas Gerais": "wiki_Minas_Gerais.html",
           "Pará": "wiki_Par_.html", "Paraíba": "wiki_Para_ba.html", "Paraná": "wiki_Paran_.html",
           "Pernambuco": "wiki_Pernambuco.html", "Piauí": "wiki_Piau_.html", "Rio de Janeiro": "wiki_Rio_de_Janeiro.html",
           "Rio Grande do Norte": "wiki_Rio_Grande_do_Norte.html", "Rio Grande do Sul": "wiki_Rio_Grande_do_Sul.html",
           "Rondônia": "wiki_Rond_nia.html", "Roraima": "wiki_Roraima.html", "São Paulo": "wiki_S_o_Paulo.html",
           "Santa Catarina": "wiki_Santa_Catarina.html", "Sergipe": "wiki_Sergipe.html", "Tocantins": "wiki_Tocantins.html"}


def txt(cell):
    s = re.sub(r"<sup.*?</sup>", "", cell, flags=re.S)
    s = re.sub(r"<style.*?</style>|<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def data(s):
    m = DATA_RE.search(s)
    if m and m.group(2).lower() in MESES:
        return datetime.date(int(m.group(3)), MESES[m.group(2).lower()], int(m.group(1)))
    m = DMY_RE.search(s)
    if m:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    if re.search(r"atual|presente|em exerc", s, re.I):
        return HOJE
    return None


def tabelas(fonte):
    t = open(fonte, "rb").read().decode("utf-8", "replace")
    for tb in re.findall(r"<table[^>]*class=\"[^\"]*wikitable[^\"]*\".*?</table>", t, re.S):
        rows = []
        for tr in re.findall(r"<tr.*?</tr>", tb, re.S):
            cells = re.findall(r"<(th|td)[^>]*>(.*?)</t[hd]>", tr, re.S)
            if cells:
                rows.append([(k, c) for k, c in cells])
        yield rows


def mandatos(uf, fonte):
    out = []
    for rows in tabelas(fonte):
        hdr, idx = None, {}
        for r in rows:
            labels = [txt(c).lower() for k, c in r]
            if any(("início" in l or "inicio" in l) for l in labels) and not idx:
                hdr = labels
                for i, l in enumerate(labels):
                    if re.search(r"nome|governador|governante|prefeito", l) and "nome" not in idx and "gov" not in idx:
                        idx["nome"] = i
                    if re.search(r"início|inicio", l) and "ini" not in idx:
                        idx["ini"] = i
                    if re.search(r"fim|término|termino", l) and "fim" not in idx:
                        idx["fim"] = i
                    if l.startswith("período") or l.startswith("periodo"):
                        idx.setdefault("periodo", i)
                    if "partido" in l and "vice" not in l and "partido" not in idx:
                        idx["partido"] = i
                continue
            if idx and "nome" in idx and len(r) > max(idx.values()):
                cells = [txt(c) for k, c in r]
                nome = cells[idx["nome"]]
                if not nome or nome.lower() in ("nome", "governador"):
                    continue
                ini = data(cells[idx["ini"]]) if "ini" in idx else None
                fim = data(cells[idx["fim"]]) if "fim" in idx else None
                if ini is None and "periodo" in idx:
                    ds = [d for d in (data(x) for x in re.split(r"\s+a\s+|–|-", cells[idx["periodo"]])) if d]
                    if ds:
                        ini, fim = ds[0], (ds[1] if len(ds) > 1 else None)
                if ini is None:
                    continue
                partido = cells[idx["partido"]] if "partido" in idx else ""
                out.append({"uf": uf, "governador": re.sub(r"\(.*?\)", "", nome).strip(" .,"),
                            "partido_wiki": partido, "ini": ini, "fim": fim or HOJE,
                            "tabela_cols": "|".join(hdr[:8]) if hdr else ""})
    return out


def main():
    res = {}
    for uf, fn in UF_FILE.items():
        ms = mandatos(uf, os.path.join(GOV, fn))
        ms = [m for m in ms if m["fim"] >= datetime.date(2011, 1, 1) and m["ini"] <= datetime.date(2026, 12, 31)]
        seen, dedup = set(), []
        for m in ms:
            k = (m["governador"], m["ini"])
            if k not in seen:
                seen.add(k); dedup.append(m)
        res[uf] = dedup
        print(f"{uf}: {len(dedup)} mandatos | partido_wiki: {sum(1 for m in dedup if m['partido_wiki'])}", file=sys.stderr)
    json.dump({uf: [{**m, "ini": m["ini"].isoformat(), "fim": m["fim"].isoformat()} for m in v]
               for uf, v in res.items()}, open(os.path.join(BASE, "dados/scripts/mandatos_wiki.json"), "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
