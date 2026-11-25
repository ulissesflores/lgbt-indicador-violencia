# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Search a PDF page by page for a regular expression.

Extracts the text of a PDF with pdftotext, splits it by page and prints, for every match of the
case-insensitive regular expression, the page number and the surrounding text with whitespace
normalized. Used to find the page of a quote while building the GGB profile.

Inputs
------
- a PDF path (first argument), a regular expression (second) and an optional context width
  (third, default 220 characters)
- poppler tools pdftotext and pdfinfo on the PATH

Outputs
-------
- prints "p<page> | ...context..." for each match to stdout

Usage
-----
python3 -I analysis/ggb-series/perfil/scripts/gp.py file.pdf 'regex' [width]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

grep por pagina em PDF (pdftotext por pagina, cache em memoria).
uso: python3 -I gp.py arquivo.pdf 'regex' [largura=220]
imprime: pag | trecho (whitespace normalizado)

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import sys, re, subprocess
pdf, rx = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 220
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
for i, t in enumerate(txt[:n], 1):
    t = re.sub(r'\s+', ' ', t)
    for m in re.finditer(rx, t, re.I):
        s = max(0, m.start() - w // 2); print(f'p{i} | ...{t[s:m.end() + w // 2]}...')
