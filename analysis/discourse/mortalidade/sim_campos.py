# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""List the field names in the header of a SIM death-certificate DBF file.

Reads the first 64 KiB of a DATASUS SIM microdata file (DOBR), parses the dBase header that is
not compressed, prints the file path, its sha256, the number of fields and the field names, and
flags names that look like orientation, gender identity or sexuality variables.

Inputs
------
- one SIM microdata file given as the first argument (for example DOBR2023.dbc; not tracked
  in git)

Outputs
-------
- prints the path, sha256, number of fields, field names and the flagged names to stdout

Usage
-----
python3 -I analysis/discourse/mortalidade/sim_campos.py <file.dbc>

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Lista os nomes de campo do cabecalho DBF (nao comprimido) dos microdados SIM DOBR (DATASUS). Uso: sim_campos.py <arquivo.dbc>

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import struct,sys,hashlib
p=sys.argv[1]
b=open(p,'rb').read(65536)
hl=struct.unpack('<H',b[8:10])[0]
names=[]
i=32
while i<hl-1 and b[i]!=0x0D:
    names.append(b[i:i+11].split(b'\0')[0].decode('latin-1')); i+=32
print(p); print('sha256',hashlib.sha256(open(p,'rb').read()).hexdigest()); print(len(names),'campos'); print(' '.join(names))
print('contem ORIENT/IDENTG/GENERO/SEXUAL:',[n for n in names if any(k in n.upper() for k in ('ORIENT','IDENTG','GENER','SEXUAL','LGBT'))])
