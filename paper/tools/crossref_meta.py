"""Baixa metadados (Crossref; DataCite como fallback) de cada DOI da lista de referencias.

Serve a `verifica_autoria`: a lista de referencias do paper e escrita a partir destes
metadados, e o probe confere sobrenome do 1o autor, ano e titulo contra eles. Cache em
`cache/doi_meta.json` (reexecucao sem rede usa o cache).

Uso: python3 -I crossref_meta.py <doi> [<doi> ...]
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache" / "doi_meta.json"
UA = {"User-Agent": "codex-hash-paper-check/1.0 (mailto:seu-email@exemplo.org)"}


def get(url):
    """GET JSON com timeout curto."""
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read())


def meta(doi):
    """Metadados minimos de um DOI: autores, ano, titulo, periodico, volume, numero, paginas."""
    q = urllib.parse.quote(doi)
    try:
        m = get(f"https://api.crossref.org/works/{q}")["message"]
        ano = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0]
        return {"fonte": "crossref", "autores": [(a.get("family") or a.get("name"), a.get("given")) for a in m.get("author", [])],
                "ano": ano, "titulo": (m.get("title") or [""])[0], "periodico": (m.get("container-title") or [""])[0],
                "volume": m.get("volume"), "numero": m.get("issue"), "paginas": m.get("page"),
                "editora": m.get("publisher"), "tipo": m.get("type")}
    except Exception as e:  # noqa: BLE001 - registra e tenta DataCite
        erro = str(e)
    try:
        a = get(f"https://api.datacite.org/dois/{q}")["data"]["attributes"]
        return {"fonte": "datacite", "autores": [(c.get("familyName") or c.get("name"), c.get("givenName")) for c in a.get("creators", [])],
                "ano": a.get("publicationYear"), "titulo": a["titles"][0]["title"], "periodico": a.get("publisher"),
                "volume": None, "numero": None, "paginas": None, "editora": a.get("publisher"), "tipo": a.get("types", {}).get("resourceTypeGeneral")}
    except Exception as e:  # noqa: BLE001
        return {"fonte": "erro", "erro": f"crossref: {erro}; datacite: {e}"}


if __name__ == "__main__":
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    for doi in sys.argv[1:]:
        if doi.lower() not in cache or cache[doi.lower()].get("fonte") == "erro":
            cache[doi.lower()] = meta(doi)
        m = cache[doi.lower()]
        print(doi, "|", m.get("fonte"), "|", m.get("ano"), "|", "; ".join(f"{f}, {g}" for f, g in (m.get("autores") or [])[:8]),
              "|", (m.get("titulo") or "")[:90], "|", m.get("periodico"), m.get("volume"), m.get("numero"), m.get("paginas"), m.get("erro", ""))
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
