# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Provide a helper that writes manual coding records for the media sample.

Library function grava(universe, index_range, default, overrides, text) that creates or updates
the coding file of one universe: every index in the range gets the default eight fields plus
the text mode, and the overrides replace single items.

Inputs
------
- analysis/discourse/midia/_codif/<universe>.json (read if it already exists)

Outputs
-------
- analysis/discourse/midia/_codif/<universe>.json (updated)
- prints the universe name and the number of coded items

Usage
-----
Imported as "from cod import grava" by coding scripts; not run directly.

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Auxiliar de codificacao: grava/atualiza _codif/<universo>.json. Uso: from cod import grava
grava(universo, indices_range, default=[...8 campos...], overrides={idx:[...]}, texto='so_titulo')

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import json, os
D = (REPO_ROOT + "/analysis/discourse/midia/_codif")
def grava(uni, rng, overrides, default=("FORA", "", "nenhuma", "", 0, 0, 0, 0), texto="so_titulo"):
    fn = f"{D}/{uni}.json"
    cur = json.load(open(fn)) if os.path.exists(fn) else {}
    for i in rng:
        cur[str(i)] = list(default) + [texto]
    for i, v in overrides.items():
        v = list(v) + ['', 'nenhuma', '', 0, 0, 0, 0][len(v) - 1:] if len(v) < 8 else list(v)
        cur[str(i)] = v + [texto]
    json.dump(cur, open(fn, "w"))
    print(uni, len(cur))
