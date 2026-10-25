"""Dicionário harmonizado (rótulo verbatim -> classe pré-registrada), a partir de saidas/estrutura/<periodo>.json.
Não lê raw/ nem conta nada: só aplica as regras de d100_comum.py a cada rótulo visto e diz em que períodos ele aparece.

Uso: /opt/homebrew/bin/python3.14 -I scripts/d100_dicionario.py
Saída: saidas/dicionario_rotulos.csv (campo_harmonizado, formato, coluna_origem, rotulo_verbatim, classe, periodos)
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d100_comum as dc  # noqa: E402


def classe_sogi(fmt, col, rot):
    if fmt == "A":
        row = {"vitima_orientacao_sexual": "NULL", "vitima_identidade_genero": "NULL"}
    elif fmt == "B":
        row = {"orientacao_sexual": "NULL", "Gênero_da_vítima": "NULL"}
    else:
        row = {"Orientação_sexual_da_vítima": "NULL", "Gênero_da_vítima": "NULL"}
    row[col] = rot
    return dc.sogi_vitima(fmt, row)


def main():
    acc = defaultdict(set)  # (campo, fmt, col, rotulo, classe) -> periodos
    for p, _ in dc.PERIODOS:
        f = dc.BASE / "saidas/estrutura" / f"{p}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        fmt, rot = d["formato"], d["rotulos"]
        regras = []
        for campo, cols in dc.HARMONIZADO.items():
            col = cols[fmt]
            if col is None or col not in rot or not isinstance(rot[col], list):
                continue
            for r in rot[col]:
                if campo == "grupo":
                    cl = "grupo_lgbt" if dc.grupo_lgbt(r) else "outro_grupo"
                elif campo in ("sexo_vitima", "sexo_suspeito"):
                    cl = dc.sexo(r)
                elif campo in ("orientacao_vitima", "identidade_vitima"):
                    cl = classe_sogi(fmt, col, r)
                elif campo == "motivacao":
                    cl = "motivacao_sogi" if dc.RE_SOGI.search(dc.norm(r)) else (dc.faltante(r) or "outra_motivacao")
                elif campo == "violacao":
                    cl = dc.macro_violacao(r) + ("|violacao_sogi" if dc.violacao_sogi(r) else "")
                elif campo == "uf":
                    cl = dc.uf(r)
                elif campo == "orientacao_suspeito":
                    cl = "registrado (não analisado)"
                else:
                    continue
                regras.append((campo, col, r, cl))
        for campo, col, r, cl in regras:
            acc[(campo, fmt, col, r, cl)].add(p)
    ordem = [p for p, _ in dc.PERIODOS]
    with open(dc.BASE / "saidas/dicionario_rotulos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["campo_harmonizado", "formato", "coluna_origem", "rotulo_verbatim", "classe", "periodos"])
        for (campo, fmt, col, r, cl), ps in sorted(acc.items()):
            w.writerow([campo, fmt, col, r, cl, ";".join(sorted(ps, key=ordem.index))])
    print(len(acc), "rótulos")


if __name__ == "__main__":
    main()
