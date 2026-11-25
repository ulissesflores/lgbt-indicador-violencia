# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Lock the numbers drawn in the README art to the numbers printed in the article.

The finding cards read their numbers from the sealed data files through the brand script.
These tests check that what they read matches what the article prints (PNS by type, ratio
2.82, the 160 to 50 sequence, and the report counts), that every picture the five READMEs
embed exists in each language and in light and dark themes, and that each README embeds only
the pictures of its own language. SVG bytes are not compared.

Inputs
------
- assets/brand/make_brand.py (loaded as a module)
- assets/brand/ (SVG and PNG pictures, one set per language and theme)
- README.md, README.pt-BR.md, README.es.md, README.it.md, README.he.md

Outputs
-------
- none (assertions only)

Usage
-----
python3 -I -m pytest tests/test_readme_arte.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Lock the numbers drawn in the README art (``assets/brand/make_brand.py``) to the article.

The finding cards read their numbers from the sealed data files (``dados()``); this test checks
that what they read is what the article prints (Abstract, sections 3.1, 3.5 and 3.7), so the art
cannot drift from the paper. The SVG bytes are not compared: matplotlib output may differ across
machines, the numbers may not.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import importlib.util
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import RAIZ, perto  # noqa: E402


def _brand():
    """Load ``assets/brand/make_brand.py`` as a module."""
    spec = importlib.util.spec_from_file_location("make_brand", RAIZ / "assets/brand/make_brand.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_cartoes_do_readme_batem_com_o_artigo():
    """Cards and Results figure: PNS by type, ratio 2.82, 160->...->50, reports 783..3,481."""
    d = _brand().dados()
    p = d["pns"]
    assert perto(p["lgb"], 14.70, 0.005) and perto(p["het"], 3.82, 0.005)
    assert perto(p["rp"], 2.82, 0.005)
    assert perto(p["ic"][0], 2.16, 0.005) and perto(p["ic"][1], 3.68, 0.005)
    assert d["ggb"] == [160, 106, 88, 74, 50]
    pct = (Decimal(100 * 50) / Decimal(160)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    assert str(pct) == "31.3"
    assert d["bo"] == {2022: 783, 2023: 1633, 2024: 2567, 2025: 3481}
    assert d["g"] == [-0.05, 0.0, 0.15]
    t = d["tipos"]
    for rot, (lgb, het) in {
        "física": (14.70, 3.82),
        "sexual": (4.86, 0.68),
        "psicológica": (40.03, 16.73),
    }.items():
        assert perto(t[rot][0], lgb, 0.005) and perto(t[rot][1], het, 0.005)


README_IDIOMA = {
    "README.md": "en",
    "README.pt-BR.md": "pt-BR",
    "README.es.md": "es",
    "README.it.md": "it",
    "README.he.md": "he",
}


def test_arte_do_readme_existe_nos_cinco_idiomas_e_dois_temas():
    """Every picture the five READMEs embed exists, in each language, light and dark."""
    for lg in README_IDIOMA.values():
        for nome in ("banner", "findings", "results"):
            for tema in ("light", "dark"):
                assert (RAIZ / f"assets/brand/{nome}-{lg}-{tema}.svg").stat().st_size > 1000
    assert (RAIZ / "assets/brand/icon.svg").is_file()
    for tema in ("light", "dark"):
        assert (RAIZ / f"assets/brand/lab-lockup-{tema}.png").stat().st_size > 1000


def test_cada_readme_usa_a_arte_do_seu_idioma():
    """Each README embeds the banner, cards and Results figure of its own language, no other."""
    for readme, lg in README_IDIOMA.items():
        usados = set(
            re.findall(
                r"assets/brand/(?:banner|findings|results)-([A-Za-z-]+)-(?:light|dark)\.svg",
                (RAIZ / readme).read_text(encoding="utf-8"),
            )
        )
        assert usados == {lg}, (readme, usados)
