# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Print a compact view of items from a sample JSONL file.

Small reading helper: for the items of the given file, it prints the index, the date, the
source, the matched entries and the first characters of the text, to support manual coding.
Arguments: file, family, first index, last index and number of characters (all but the first
two optional).

Inputs
------
- a sample JSONL file such as analysis/discourse/midia/_amostra_<universe>.jsonl

Outputs
-------
- prints one line per item to stdout

Usage
-----
python3 -I analysis/discourse/midia/scripts/mostra.py <file.jsonl> <family> [a] [b] [n]
where a and b are the first and last index and n is the number of characters.

Status
------
No registration status is claimed for this file.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import json,sys
fn,fam=sys.argv[1],sys.argv[2]; a=int(sys.argv[3]) if len(sys.argv)>3 else 0; b=int(sys.argv[4]) if len(sys.argv)>4 else 999
n=int(sys.argv[5]) if len(sys.argv)>5 else 230
for i,l in enumerate(open(fn)):
    j=json.loads(l)
    if j['familia']!=fam or not (a<=i<b): continue
    t=(j.get('trecho') or j.get('titulo') or '')
    if 'titulo' in j and j.get('trecho'): t=j['titulo']+' || '+j['trecho']
    print(i,j['data'][:16] if j.get('data') else '',(j.get('fonte') or ''),(';'.join(j.get('entradas',[])))[:14],'|',t[:n].replace('\n',' '))
