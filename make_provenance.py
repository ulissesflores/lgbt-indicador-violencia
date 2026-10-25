"""Selo de proveniência: um chain_hash SHA-256 sobre TUDO que o repositório distribui.

(código, testes, dados derivados, ledgers, documentos).

Uso:
    python3 -I make_provenance.py --build    # grava manifest/SHA256SUMS.txt, output/provenance.json
                                             # e output/hash-chain.md
    python3 -I make_provenance.py --verify   # recalcula e compara com o selo gravado
                                             # (exit 1 se divergir)

O que entra: todo arquivo versionável sob a raiz, exceto o próprio selo (output/provenance.json,
output/hash-chain.md), BUILD-STATE.md, caches, .git, .work e .run, e o que o .gitignore exclui por
regra (microdado bruto, dados nominais).
O artigo NÃO entra: o repositório vem primeiro e o artigo deriva dele (cita a URL e o chain_hash
deste selo), então o selo não pode cobrir o próprio artigo. Ficam fora do selo ``paper/paper.md``,
``paper/AUDIT.md``, ``paper/build/`` (PDF, DOCX, saídas do juiz), ``paper/tools/`` (ferramentas de
export e auditoria do artigo), ``paper/tests/test_anexo.py`` (testa o build do artigo) e
``paper/PAPER-SHA256.txt`` (hash do PDF final, gravado depois). As figuras (``paper/figures/``) e
os testes de figura ENTRAM: são derivados dos dados do repositório.
Entra byte a byte: a conferência de que os scripts RECALCULAM os derivados (e batem com o commitado)
é outra etapa (scripts/reproduzir.py), porque o recálculo pode diferir na última casa binária entre
sistemas; o selo cobre o que está publicado, não o que a máquina de quem confere recalcula.
chain_hash = sha256 de "<caminho>\\0<sha256>\\n" para cada arquivo, em ordem lexicográfica de
caminho (inclui manifest/SHA256SUMS.txt).
"""

import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
OUT = RAIZ / "output"
# fig-embed: cópias leves das figuras que o build do PDF regrava a cada execução (fora do git)
EXCLUI_DIRS = {
    ".git",
    ".work",
    ".run",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "fig-embed",
}
# microdado bruto baixado pelos scripts acquire_* (ignorado pelo git): nunca entra no selo
EXCLUI_PREFIXOS = (
    "fontes/p3-ggb/",
    "fontes/q1-textointegral/",
    "fontes/p2-sim-microdados/",
    "fontes/p2-sinan-microdados/",
    "fontes/p2-f8-governos/tse/",
    "fontes/pns2019/",
)
RAW_LOCAIS = re.compile(r"(^raw/)|(/dados/raw/)|(/ideologia/raw/)|(/F6-asia-africa/raw/)")
# Artigo e o que só existe para construí-lo: fora do selo, para sempre (o artigo cita o selo, não o
# integra). Entram no git num commit posterior; o hash do PDF final vai a paper/PAPER-SHA256.txt.
EXCLUI_PAPER_DIRS = ("paper/build/", "paper/tools/")
EXCLUI_PAPER_ARQ = {
    "paper/paper.md",
    "paper/AUDIT.md",
    "paper/PAPER-SHA256.txt",
    "paper/tests/test_anexo.py",
}
EXCLUI_ARQ = {"BUILD-STATE.md", ".DS_Store", "output/provenance.json", "output/hash-chain.md"}
SOMAS = "manifest/SHA256SUMS.txt"


def excluido(rel):
    """Diz se um caminho relativo (posix) fica fora do conjunto distribuído e selado.

    É a regra única de exclusão: o selo, o inventário público, os testes de privacidade e o
    auditor a usam, para que todos vejam o mesmo conjunto.

    Parameters
    ----------
    rel : str
        Caminho relativo à raiz, com barras.

    Returns
    -------
    bool
        True se o arquivo não é distribuído (cache, bruto, artigo, o próprio selo).
    """
    partes = rel.split("/")
    return bool(
        EXCLUI_DIRS & set(partes)
        or rel in EXCLUI_ARQ
        or rel in EXCLUI_PAPER_ARQ
        or rel.startswith(EXCLUI_PAPER_DIRS)
        or partes[-1] == ".DS_Store"
        or rel.endswith((".pyc", ".dbc", ".dbf"))
        or rel.startswith(EXCLUI_PREFIXOS)
        or RAW_LOCAIS.search(rel)
    )


def arquivos():
    """Caminhos relativos (posix, ordenados) dos arquivos distribuídos, sem o selo."""
    return sorted(
        rel
        for p in RAIZ.rglob("*")
        if p.is_file() and not excluido(rel := p.relative_to(RAIZ).as_posix())
    )


def sha(rel):
    """SHA-256 de um arquivo (relativo à raiz), em blocos de 1 MiB."""
    h = hashlib.sha256()
    with open(RAIZ / rel, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def somas_txt(arqs):
    """Conteúdo de manifest/SHA256SUMS.txt (formato sha256sum).

    Cobre os arquivos dados, exceto ele mesmo.
    """
    return "".join(f"{sha(a)}  {a}\n" for a in arqs if a != SOMAS)


def selo():
    """Calcula o conteúdo de SHA256SUMS.txt e o chain_hash; devolve também a lista de itens."""
    arqs = [a for a in arquivos() if a != SOMAS]
    conteudo = somas_txt(arqs)
    itens = [{"arquivo": a, "sha256": sha(a)} for a in arqs]
    itens.append({"arquivo": SOMAS, "sha256": hashlib.sha256(conteudo.encode()).hexdigest()})
    itens.sort(key=lambda i: i["arquivo"])
    cadeia = hashlib.sha256()
    for i in itens:
        cadeia.update(f"{i['arquivo']}\0{i['sha256']}\n".encode())
    return conteudo, {"chain_hash": cadeia.hexdigest(), "n_arquivos": len(itens), "arquivos": itens}


def main():
    """Grava o selo (``--build``) ou o confere (``--verify``); devolve 0 se confere."""
    conteudo, atual = selo()
    if "--build" in sys.argv:
        (RAIZ / "manifest").mkdir(exist_ok=True)
        OUT.mkdir(exist_ok=True)
        (RAIZ / SOMAS).write_text(conteudo, encoding="utf-8")
        _, atual = selo()  # recalcula: o hash de SHA256SUMS.txt acabou de ser gravado
        json.dump(
            atual,
            open(OUT / "provenance.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=1,
        )
        linhas = [
            "# Hash chain",
            "",
            f"chain_hash: `{atual['chain_hash']}` ({atual['n_arquivos']} arquivos)",
            "",
            "Verificar: `python3 -I make_provenance.py --verify`",
            "",
        ]
        (OUT / "hash-chain.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
        print(f"selo gravado: {atual['chain_hash']} ({atual['n_arquivos']} arquivos)")
        return 0
    gravado = json.load(open(OUT / "provenance.json", encoding="utf-8"))
    if (RAIZ / SOMAS).read_text(encoding="utf-8") != conteudo:
        print("SHA256SUMS.txt DIVERGE do conteúdo atual dos arquivos")
    if gravado["chain_hash"] != atual["chain_hash"]:
        antes = {i["arquivo"]: i["sha256"] for i in gravado["arquivos"]}
        agora = {i["arquivo"]: i["sha256"] for i in atual["arquivos"]}
        dif = sorted(k for k in antes.keys() | agora.keys() if antes.get(k) != agora.get(k))
        print("selo DIVERGE em: " + ", ".join(dif[:50]) + (" ..." if len(dif) > 50 else ""))
        return 1
    print(f"provenance verified: {atual['chain_hash']} ({atual['n_arquivos']} arquivos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
