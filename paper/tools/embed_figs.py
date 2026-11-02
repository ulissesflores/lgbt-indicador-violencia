"""Cópias leves das figuras só para embutir no DOCX/PDF (limite de 4 MB do canon).

As figuras de referência (figures/*.png, 300 dpi, travadas por tests/test_figuras.py) não
são tocadas: este passo grava em build/fig-embed/ uma cópia com no máximo LARGURA px de
largura (cerca de 190 dpi na largura útil da página) em paleta de 256 cores, e reescreve os
caminhos em build/paper-export.md. Mínimo: Pillow já é dependência das figuras.

v0.3 (P2a): `python3 -I embed_figs.py [export.md] [--largura PX]` — o build chama uma vez por PDF
(principal e anexos); cada PDF tem cerca de metade das figuras, e a largura maior deixa legível a
letra de dentro das figuras sem tocar nos PNG de referência.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

LARGURA = 950  # v0.3: 28 figuras; 1200 px dava PDF de 6,0 MB, acima do limite de 4 MB do canon (o LibreOffice regrava em JPEG)
ROOT = Path(__file__).resolve().parents[1]
SAIDA = ROOT / "build" / "fig-embed"
CORES = 256


def main() -> int:
    args = sys.argv[1:]
    largura = LARGURA
    if "--largura" in args:
        i = args.index("--largura")
        largura = int(args[i + 1])
        del args[i:i + 2]
    export = Path(args[0]).resolve() if args else ROOT / "build" / "paper-export.md"
    texto = export.read_text(encoding="utf-8")
    SAIDA.mkdir(parents=True, exist_ok=True)
    nomes = sorted(set(re.findall(r"\]\(figures/([\w.-]+\.png)\)", texto)))
    for nome in nomes:
        img = Image.open(ROOT / "figures" / nome).convert("RGB")
        if img.width > largura:
            img = img.resize((largura, round(img.height * largura / img.width)), Image.LANCZOS)
        img.quantize(CORES, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
            SAIDA / nome, optimize=True)
    texto = re.sub(r"\]\(figures/([\w.-]+\.png)\)", r"](build/fig-embed/\1)", texto)
    export.write_text(texto, encoding="utf-8")
    tam = sum((SAIDA / n).stat().st_size for n in nomes)
    print(f"[OK] {len(nomes)} figuras leves ({largura} px) em build/fig-embed para {export.name} ({tam} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
