# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Convert the main content of an HTML page to plain text.

Removes script, style, navigation and similar blocks with the standard library, keeps the main
or article element when present, turns block tags into line breaks, decodes entities and
collapses whitespace.

Inputs
------
- an HTML file path (first argument)

Outputs
-------
- the text file named by the optional second argument, or stdout when it is omitted

Usage
-----
python3 -I analysis/ggb-series/perfil/scripts/html2txt.py in.html [out.txt]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

html -> texto do <main>/article (stdlib). uso: python3 -I html2txt.py in.html [out.txt]

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import sys, re, html
h = open(sys.argv[1], encoding='utf8', errors='replace').read()
h = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>', ' ', h)
m = re.search(r'(?is)<main.*?</main>', h) or re.search(r'(?is)<article.*?</article>', h)
b = m.group(0) if m else h
b = re.sub(r'(?i)<br\s*/?>|</(p|div|h\d|li|tr|section)>', '\n', b)
b = re.sub(r'(?s)<[^>]+>', ' ', b)
b = html.unescape(b)
b = re.sub(r'[ \t\xa0]+', ' ', b)
b = re.sub(r'\n\s*\n+', '\n', b).strip()
out = sys.argv[2] if len(sys.argv) > 2 else None
(open(out, 'w', encoding='utf8').write(b) if out else print(b))
