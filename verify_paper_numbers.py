# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Check every number the article prints against the repository file that holds it.

Reads the table of printed numbers, which gives for each one the value as printed, its origin
class, the file and the locator inside the file (CSV cell, Markdown table cell, JSON path or
text pattern), the script that writes the file and the SHA-256 of both. It checks that the
recorded hashes still match, that each locator resolves to one place whose value, rounded to
the printed precision, equals the printed value, and that a corrected entry has a matching
paragraph in the corrections notes. With --rerun it also regenerates the outputs in a replica
and repeats the value check there.

Inputs
------
- paper_numbers.json
- the source files and scripts named in that table
- docs/corrections.md
- .run/replica/ (with --rerun, produced by scripts/reproduzir.py)

Outputs
-------
- paper_numbers.json (only with --write-hashes, which records current SHA-256 values)
- prints the hash and value check counts and each failure to stdout; exit code 0 only if all
  pass

Usage
-----
python3 -I verify_paper_numbers.py [--rerun | --write-hashes]

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Check every number the article prints against the repository file that holds it.

``paper_numbers.json`` lists, for each number printed in the article (Brazilian Portuguese
edition, the one the other editions are translated from), where it is printed, the value as
printed, the class of its origin, and the exact place in the repository that holds it: file,
locator inside the file (CSV row and column, Markdown table section, row and column, JSON path,
or a text pattern with one group), the script that writes the file, and the SHA-256 of both.

Checks, in order:

1. hashes: each source file and script still has the SHA-256 recorded in the table;
2. values: each locator resolves to exactly one place, and the value there, rounded to the
   precision printed in the article, equals the printed value. A printed number the article gets
   wrong carries ``corrected``: it passes only if the value rounds to the corrected number, not to
   the printed one, and ``docs/corrections.md`` has a paragraph naming the entry id, the printed
   and the corrected value (the article edition is frozen; the correction is documented, not
   hidden);
3. (optional, ``--rerun``) runs ``scripts/reproduzir.py``, which regenerates the outputs in
   ``.run/replica`` from the distributed inputs, and repeats check 2 against the regenerated
   files. A hash proves that nothing changed; only the rerun shows the code produces the number.

Usage::

    python3 -I verify_paper_numbers.py            # hashes + values against the committed files
    python3 -I verify_paper_numbers.py --rerun    # also regenerate and check the regenerated files
    python3 -I verify_paper_numbers.py --write-hashes   # record current SHA-256 (maintainers)

Exit code 0 only if every check passes. Standard library only.

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
TABELA = RAIZ / "paper_numbers.json"
REPLICA = RAIZ / ".run" / "replica"

# Classes whose value has a locator in the repository, checked and hashed:
#   output          a distributed script writes (or prints, byte for byte) the file;
#   text-arithmetic arithmetic the article does on published numbers, recomputed by
#                   analysis/article-numbers/contas_do_texto.py;
#   third-party     transcription of a cited source
#                   (analysis/article-numbers/terceiros_transcritos.csv): proves the article
#                   copies the source correctly, not that the repository computes it;
#   hand-written    a file no distributed script writes (pre-registration, dated report,
#                   hash record):
#                   the article copies it correctly, but the repository does not recompute it.
# Classes without a locator, each with a stated reason:
#   parameter, declared-limit, manual-conditional  design choices and declared limits;
#   pending-source  a cited source not yet opened; the number is listed, not checked.
CLASSES_COM_LOCAL = {"output", "text-arithmetic", "third-party", "hand-written"}
CLASSES_SEM_LOCAL = {"parameter", "declared-limit", "manual-conditional", "pending-source"}
CORRECOES = "docs/corrections.md"
# Files the seal itself rewrites on every build (make_provenance.py --build). Their values are
# checked like any other, but their SHA-256 is not recorded here: this table is inside the seal,
# so recording the hash of the seal would never settle. make_provenance.py --verify checks them.
SEM_HASH = {"output/provenance.json"}


def numero_impresso(texto):
    """Parse a number as printed in the Brazilian Portuguese edition.

    Parameters
    ----------
    texto : str
        Printed token, e.g. ``"3,82%"``, ``"−11,3"``, ``"3.025.764"``, ``",016"``.

    Returns
    -------
    tuple of (float, int)
        The value and the number of decimal places printed.
    """
    t = texto.strip().replace("−", "-").replace("%", "").replace(" ", "")
    t = t.replace(" ", "")
    m = re.fullmatch(r"([-+]?)((?:\d{1,3}(?:\.\d{3})+|\d*))(?:,(\d+))?", t)
    if not m or (not m.group(2) and not m.group(3)):
        raise ValueError(f"not a printed number: {texto!r}")
    inteiro = m.group(2).replace(".", "") or "0"
    decimais = m.group(3) or ""
    valor = float(f"{inteiro}.{decimais}" if decimais else inteiro)
    return (-valor if m.group(1) == "-" else valor), len(decimais)


_NUM_FONTE = {
    "dot": re.compile(r"[-+−]?(?:\d[\d,]*)?\.?\d+"),
    "comma": re.compile(r"[-+−]?(?:\d[\d.]*)?,?\d+"),
}


def numeros_fonte(texto, formato="dot"):
    """All numbers in a source cell, in order.

    Parameters
    ----------
    texto : str
        Cell or matched text from a repository file.
    formato : {"dot", "comma"}
        ``dot``: decimal point, optional comma thousands (``1,554.2``); ``comma``: decimal comma,
        optional dot thousands (``1.554,2``).

    Returns
    -------
    list of float
        Numbers found, left to right.
    """
    saida = []
    for bruto in _NUM_FONTE[formato].findall(texto.replace("−", "-")):
        b = bruto.replace("−", "-")
        b = b.replace(",", "") if formato == "dot" else b.replace(".", "").replace(",", ".")
        try:
            saida.append(float(b))
        except ValueError:
            continue
    return saida


def _celulas(linha):
    """Cells of a GitHub-flavoured Markdown table row."""
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def resolve(fonte, raiz=RAIZ):
    """Return the single value the locator points to.

    Parameters
    ----------
    fonte : dict
        Locator with ``file`` and ``type`` and the keys of that type: ``csv`` (``row`` dict of
        field values, ``column``), ``md-table`` (``section``, ``row``, ``column``, optional
        ``row_key_columns`` and ``occurrence``/``occurrences``), ``json`` (``path``) or ``text``
        (``pattern``, a regex with one group matching once); all take ``index`` (k-th number in
        the cell, default 0) and ``number_format`` (``dot`` or ``comma``).
    raiz : pathlib.Path
        Repository root (the committed files) or the replica (regenerated files).

    Returns
    -------
    float
        Value at the located place, before the printed scale is applied.

    Raises
    ------
    LookupError
        If the locator matches no place or more than one.
    """
    caminho = raiz / fonte["file"]
    tipo = fonte["type"]
    formato = fonte.get("number_format", "dot")
    indice = fonte.get("index", 0)
    if tipo == "csv":
        with open(caminho, encoding="utf-8", newline="") as fh:
            sep = "\t" if caminho.suffix in {".tsv"} else ","
            linhas = [
                r
                for r in csv.DictReader(fh, delimiter=sep)
                if all(r.get(k) == v for k, v in fonte["row"].items())
            ]
        if len(linhas) != 1:
            raise LookupError(f"{len(linhas)} rows match {fonte['row']} in {fonte['file']}")
        nums = numeros_fonte(linhas[0][fonte["column"]], formato)
    elif tipo == "md-table":
        nums = _md_tabela(caminho.read_text(encoding="utf-8"), fonte, formato)
    elif tipo == "json":
        no = json.loads(caminho.read_text(encoding="utf-8"))
        for passo in fonte["path"]:
            no = no[passo]
        nums = [float(no)] if isinstance(no, (int, float)) else numeros_fonte(str(no), formato)
    elif tipo == "text":
        achados = re.findall(fonte["pattern"], caminho.read_text(encoding="utf-8"), re.M)
        if len(achados) != 1:
            raise LookupError(f"{len(achados)} matches of {fonte['pattern']!r} in {fonte['file']}")
        grupo = achados[0] if isinstance(achados[0], str) else achados[0][0]
        nums = numeros_fonte(grupo, formato)
    else:
        raise LookupError(f"unknown locator type {tipo!r}")
    if indice >= len(nums):
        raise LookupError(f"number {indice} not in located cell of {fonte['file']}: {nums}")
    return nums[indice]


def _md_tabela(texto, fonte, formato):
    """Numbers of one cell of a Markdown table, located by section, row label and column."""
    linhas = texto.splitlines()
    inicio = [i for i, ln in enumerate(linhas) if ln.startswith(fonte["section"])]
    if len(inicio) != 1:
        raise LookupError(f"{len(inicio)} sections start with {fonte['section']!r}")
    i = inicio[0] + 1
    while i < len(linhas) and not linhas[i].lstrip().startswith("|"):
        i += 1
    if i >= len(linhas):
        raise LookupError(f"no table after section {fonte['section']!r}")
    cab = _celulas(linhas[i])
    col = [j for j, c in enumerate(cab) if c == fonte["column"]]
    if len(col) != 1:
        raise LookupError(f"{len(col)} columns named {fonte['column']!r}: {cab}")
    achadas = []
    for ln in linhas[i + 2 :]:
        if not ln.lstrip().startswith("|"):
            break
        cel = _celulas(ln)
        rotulo = [cel[k] for k in fonte.get("row_key_columns", [0])]
        alvo = fonte["row"] if isinstance(fonte["row"], list) else [fonte["row"]]
        if rotulo == alvo:
            achadas.append(cel[col[0]])
    # rótulo repetido na mesma tabela (ex.: "Outro" em dois blocos): "occurrence" = qual delas, e o
    # número de repetições tem de ser o declarado, para que um rótulo novo não desloque a escolha
    ocorr = fonte.get("occurrence")
    if ocorr is None and len(achadas) != 1:
        raise LookupError(f"{len(achadas)} rows labelled {fonte['row']!r}")
    if ocorr is not None and len(achadas) != fonte["occurrences"]:
        raise LookupError(
            f"{len(achadas)} rows labelled {fonte['row']!r}, expected {fonte['occurrences']}"
        )
    return numeros_fonte(achadas[ocorr or 0], formato)


def bate(valor, impresso, escala=1.0, limite=None):
    """Tell whether ``valor * escala`` matches the printed number.

    Parameters
    ----------
    valor : float
        Value held by the repository file.
    impresso : str
        Number as printed in the article.
    escala : float
        Factor from the stored unit to the printed one (e.g. 100 for a proportion printed in %).
    limite : {None, "lt", "gt"}
        ``None``: the value rounds to the printed number at the printed precision. ``"lt"``: the
        article prints a bound such as ``< ,001`` and the value must be below it. ``"gt"``: the
        article prints ``mais de 100 mil`` and the value must be above it.

    Returns
    -------
    bool
        True if the printed number is a faithful report of the value.
    """
    alvo, casas = numero_impresso(impresso)
    if limite == "lt":
        return valor * escala < alvo
    if limite == "gt":
        return valor * escala > alvo
    if limite is not None:
        raise ValueError(f"unknown bound {limite!r}")
    return abs(valor * escala - alvo) <= 0.5 * 10**-casas + 1e-9


def nota_de_correcao(texto, ident, impresso, corrigido):
    """Tell whether the corrections record documents a printed number corrected.

    Parameters
    ----------
    texto : str
        Content of ``docs/corrections.md`` (English, decimal point).
    ident : str
        Entry id in ``paper_numbers.json``, cited in the note between backticks.
    impresso, corrigido : str
        Printed and corrected numbers as the Portuguese edition writes them (``"26,3"``).

    Returns
    -------
    bool
        True if one paragraph names the id and both numbers, written with a decimal point.
    """
    en = str.maketrans(",.", ".,")  # 1.234,5 (pt-BR) -> 1,234.5 (en)
    return any(
        f"`{ident}`" in par and impresso.translate(en) in par and corrigido.translate(en) in par
        for par in texto.split("\n\n")
    )


def sha256(rel, raiz=RAIZ):
    """SHA-256 of a repository file, hex."""
    return hashlib.sha256((raiz / rel).read_bytes()).hexdigest()


def carrega():
    """Load ``paper_numbers.json``."""
    return json.loads(TABELA.read_text(encoding="utf-8"))


def confere_valores(tabela, raiz=RAIZ):
    """Check every located number; return the list of failures (empty if all pass).

    Parameters
    ----------
    tabela : dict
        Content of ``paper_numbers.json``.
    raiz : pathlib.Path
        Root whose files are read (repository or replica).

    Returns
    -------
    list of str
        One message per printed number that fails.
    """
    falhas = []
    notas = None
    for e in tabela["numbers"]:
        if e["class"] not in CLASSES_COM_LOCAL:
            if e["class"] not in CLASSES_SEM_LOCAL:
                falhas.append(f"{e['id']}: unknown class {e['class']!r}")
            elif not e.get("reason"):
                falhas.append(f"{e['id']}: class {e['class']!r} without a stated reason")
            continue
        if e["class"] == "hand-written" and not e.get("reason"):
            falhas.append(f"{e['id']}: class 'hand-written' without a stated reason")
        try:
            valor = resolve(e["locator"], raiz)
        except (LookupError, OSError, KeyError, ValueError) as erro:
            falhas.append(f"{e['id']}: {erro}")
            continue
        for p in e["printed"]:
            if p.get("corrected"):
                # o artigo congelado imprime errado: a nota tem de existir e a fonte tem de
                # arredondar para o corrigido (e não para o impresso, senão a nota sobra)
                if notas is None:
                    notas = (RAIZ / CORRECOES).read_text(encoding="utf-8")
                if not nota_de_correcao(notas, e["id"], p["value"], p["corrected"]):
                    falhas.append(
                        f"{e['id']}: corrected {p['corrected']} without a note in {CORRECOES}"
                    )
                elif bate(valor, p["value"], e.get("scale", 1.0)):
                    falhas.append(
                        f"{e['id']}: printed {p['value']} already matches; drop 'corrected'"
                    )
                elif not bate(valor, p["corrected"], e.get("scale", 1.0)):
                    falhas.append(
                        f"{e['id']}: line {p['line']} corrected to {p['corrected']}, "
                        f"{e['locator']['file']} holds {valor} (scale {e.get('scale', 1.0)})"
                    )
                continue
            if not bate(valor, p["value"], e.get("scale", 1.0), p.get("bound")):
                sinal = {"lt": "< ", "gt": "> "}.get(p.get("bound"), "")
                falhas.append(
                    f"{e['id']}: line {p['line']} prints {sinal}{p['value']}, "
                    f"{e['locator']['file']} holds {valor} (scale {e.get('scale', 1.0)})"
                )
    return falhas


def confere_hashes(tabela):
    """Check the recorded SHA-256 of every source file and script; return the failures."""
    falhas = []
    for rel, esperado in sorted(tabela["sha256"].items()):
        if not (RAIZ / rel).is_file():
            falhas.append(f"{rel}: missing")
        elif sha256(rel) != esperado:
            falhas.append(f"{rel}: SHA-256 differs from paper_numbers.json")
    return falhas


def grava_hashes(tabela):
    """Record the current SHA-256 of every file and script the table names."""
    arquivos = set()
    for e in tabela["numbers"]:
        if "locator" in e and e["locator"]["file"] not in SEM_HASH:
            arquivos.add(e["locator"]["file"])
        arquivos.update(e.get("scripts", []))
        if any(p.get("corrected") for p in e["printed"]):
            arquivos.add(CORRECOES)
    tabela["sha256"] = {rel: sha256(rel) for rel in sorted(arquivos)}
    TABELA.write_text(json.dumps(tabela, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(arquivos)


def main(argv=None):
    """Run the checks and print a summary; return the exit code."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rerun", action="store_true", help="regenerate outputs and check them too")
    ap.add_argument("--write-hashes", action="store_true", help="record current SHA-256")
    args = ap.parse_args(argv)
    tabela = carrega()
    if args.write_hashes:
        print(f"recorded SHA-256 of {grava_hashes(tabela)} files")
        return 0
    n = len(tabela["numbers"])
    impressos = sum(len(e["printed"]) for e in tabela["numbers"])
    falhas = confere_hashes(tabela)
    print(f"hashes: {len(tabela['sha256']) - len(falhas)}/{len(tabela['sha256'])} match")
    fv = confere_valores(tabela)
    print(f"values: {impressos} printed numbers in {n} entries, {len(fv)} failures")
    por_classe = {}
    for e in tabela["numbers"]:
        por_classe[e["class"]] = por_classe.get(e["class"], 0) + len(e["printed"])
    for cls in sorted(por_classe, key=lambda c: (c not in CLASSES_COM_LOCAL, c)):
        tipo = "checked" if cls in CLASSES_COM_LOCAL else "listed with a reason, not checked"
        print(f"  {cls:<20} {por_classe[cls]:>6}  {tipo}")
    falhas += fv
    if args.rerun:
        rc = subprocess.call([sys.executable, "-I", str(RAIZ / "scripts" / "reproduzir.py")])
        fr = confere_valores(tabela, REPLICA) if rc == 0 else [f"reproduzir.py exit {rc}"]
        print(f"rerun: {len(fr)} failures against the regenerated files")
        falhas += fr
    for f in falhas[:50]:
        print("  FAIL", f)
    if len(falhas) > 50:
        print(f"  ... and {len(falhas) - 50} more")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
