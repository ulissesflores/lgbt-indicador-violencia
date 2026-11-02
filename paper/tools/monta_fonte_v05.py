#!/usr/bin/env python3
"""Fonte unica do PDF v0.5: artigo (paper/v05/MANUSCRITO.md) + Material Complementar no MESMO arquivo.

Regra da casa: um PDF so, com apendices dentro; nunca PDF de anexos separado. O Material Complementar entra
depois do Apendice A, cada MC em pagina nova (titulo de nivel 1 no exportador). Nenhuma palavra muda: so
o cabecalho de metadados (que o exportador usa na folha de rosto), o nivel do titulo do MC e os caminhos
das figuras, reescritos relativos a paper/ (onde o exportador procura).

O Material Complementar entra como Apendices B a M (APA 7); as obras citadas nele estao na lista unica do artigo.

Uso: python3 tools/monta_fonte_v05.py --out build/v05/fonte-v05.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # paper/
V05 = ROOT / "v05"

META = """---
title: "Mortalidade e violência contra pessoas LGBT+ no Brasil: o que os dados públicos permitem afirmar"
subtitle: "Uma auditoria de fontes e indicadores de 2010 a 2026"
author: "Carlos Ulisses Flores"
affiliation: "Codex Hash Research Laboratory"
orcid: "0000-0002-6034-7765"
date: "{data}"
lang: pt-BR
version: "0.5.0"
repository: "https://github.com/ulissesflores/lgbt-indicador-violencia"
---

"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--data", default="2026-11-01")
    a = ap.parse_args()
    art = (V05 / "MANUSCRITO.md").read_text(encoding="utf-8")
    mc = (V05 / "MATERIAL-COMPLEMENTAR.md").read_text(encoding="utf-8")
    art = re.sub(r"\]\(figures/", "](v05/figures/", art)
    mc = re.sub(r"\]\(\.\./figures/", "](figures/", mc)
    # o H1 do arquivo dos apendices sai: cada "## Apêndice X —" ja e titulo de nivel 1 no documento
    mc, k = re.subn(r"\A# Apêndices B a M — .*\n+", "", mc)
    assert k == 1, "titulo do arquivo dos apendices nao encontrado"
    # lista de referencias como itens "- " (forma que o validador da casa conta); listas dos apendices com "* "
    # (mesmo marcador no DOCX), para que so as referencias contem como "- " depois de "## Referências"
    ini = art.index("\n## Referências\n") + len("\n## Referências\n")
    fim = art.index("\n## Apêndice A")
    refs = [e.strip() for e in art[ini:fim].split("\n\n") if e.strip()]
    art = art[:ini] + "\n" + "\n".join("- " + e for e in refs) + "\n" + art[fim:]
    mc = re.sub(r"^- ", "* ", mc, flags=re.M)
    resto = re.findall(r"\]\((?!v05/figures/|figures/)[^)]+\.png\)", art + mc)
    assert not resto, f"figura com caminho fora do previsto: {resto[:3]}"
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(META.format(data=a.data) + art.rstrip() + "\n\n" + mc, encoding="utf-8")
    print(f"[OK] {out} ({len((art + mc).split())} palavras)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
