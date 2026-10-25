"""Auditoria de publicação: itens 6, 9, 10 e 12 do checklist do escrutínio externo (v0.3).

Cada verificação imprime o que conferiu e devolve um código de saída:

- ``0``: critério atendido;
- ``1``: critério NÃO atendido (a lista do que falhou sai na tela);
- ``2``: NÃO EXERCIDO (a verificação depende de algo que ainda não existe ou não está instalado).

Verificações (``--check``):

- ``literatura``: todo registro de ledger tem identificador, URL e data; na planilha de verificação,
  todo veredito sobre o conteúdo (confirmado, com ressalva, contradito) vem de texto lido (integral
  ou manuscrito do autor) e "sem texto integral" não traz veredito;
  quando o artigo está no repositório (``paper/paper.md`` e ``paper/tools/``, que entram depois do
  primeiro commit e ficam fora do selo), ``paper/tools/verifica_referencias.py`` passa (referência
  com ledger, autoria e ano, citação x lista, vocabulário); sem o artigo, essa conferência sai
  "NÃO EXERCIDA" na mensagem e não altera o código de saída;
- ``inventario``: ``scripts/inventario_publico.py --check`` confere;
  ``manifest/MANIFESTO-FONTES.csv`` cobre todo identificador dos ledgers distribuídos; o README cita
  os números do inventário;
- ``privacidade``: as conferências de ``tests/test_integridade.py`` (colunas nominais, ids, e-mail,
  CPF, caminho de home, PDFs e microdado de terceiros, caminhos absolutos em scripts) e o gitleaks
  sobre uma cópia do conjunto distribuído; a varredura nominal exige a lista nominal privada e não é
  exercível aqui;
- ``release``: metadados coerentes com a fase pré-DOI (versão 0.x igual nos 4 arquivos, acesso
  fechado, sem DOI); a sequência repositório público -> Zenodo -> rc1 -> DOI -> final só pode ser
  conferida depois que existir, por isso sai NÃO EXERCIDO (código 2).

Uso::

    python3 -I scripts/auditar_publicacao.py --check literatura|inventario|privacidade|release
        [--raiz DIR] [--stage final]
"""

import csv
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OK, FALHOU, NAO_EXERCIDO = 0, 1, 2
VEREDITO_LIDO = {"CONFIRMADO", "CONFIRMADO_COM_RESSALVA", "CONTRADITO"}
VERIFICACAO = "research-2026-10-21-rodada3/A-textointegral/verificacao-metadados.csv"


def _modulo(nome, arq):
    """Importa um arquivo .py como módulo sem executar o bloco ``__main__``.

    Parameters
    ----------
    nome : str
        Nome do módulo.
    arq : pathlib.Path
        Caminho do arquivo.

    Returns
    -------
    module
        Módulo carregado.
    """
    spec = importlib.util.spec_from_file_location(nome, arq)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _py(raiz, *args):
    """Roda um script Python do repositório em modo isolado, com ``REPO_ROOT`` = raiz.

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.
    *args : str
        Script (relativo à raiz) e argumentos.

    Returns
    -------
    subprocess.CompletedProcess
        Resultado, com a saída capturada.
    """
    env = dict(os.environ, REPO_ROOT=str(raiz), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        [sys.executable, "-B", "-I", str(raiz / args[0]), *args[1:]],
        cwd=str(raiz),
        env=env,
        capture_output=True,
        text=True,
    )


def _ledgers(raiz):
    """Registros de todos os ledgers distribuídos.

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.

    Returns
    -------
    list of tuple
        (ledger relativo, número da linha, registro).
    """
    prov = _modulo("_prov_aud", raiz / "make_provenance.py")
    regs = []
    for a in prov.arquivos():
        if re.search(r"(^|/)sources[^/]*\.jsonl$", a):
            for i, linha in enumerate((raiz / a).read_text(encoding="utf-8").splitlines(), 1):
                if linha.strip():
                    regs.append((a, i, json.loads(linha)))
    return regs


def check_literatura(raiz):
    """Rastreabilidade das referências (item 6 do checklist).

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.

    Returns
    -------
    tuple of (int, list of str)
        Código de saída e mensagens.
    """
    falhas, msgs = [], []
    regs = _ledgers(raiz)
    for a, i, r in regs:
        faltam = [c for c in ("id", "id_kind", "url", "ts") if not str(r.get(c) or "").strip()]
        if faltam:
            falhas.append(f"{a}:{i}: registro sem {', '.join(faltam)}")
    msgs.append(f"ledgers: {len(regs)} registros conferidos (id, tipo de id, URL, data de acesso)")
    with open(raiz / VERIFICACAO, encoding="utf-8", newline="") as fh:
        ver = list(csv.DictReader(fh))
    for n, r in enumerate(ver, 2):
        lido = r["texto_integral"] in ("sim", "parcial")
        if r["veredito"] in VEREDITO_LIDO and not lido:
            falhas.append(
                f"{VERIFICACAO}:{n}: veredito {r['veredito']} sem texto lido ({r['doi']})"
            )
        if r["veredito"] == "SEM_TEXTO_INTEGRAL" and lido:
            falhas.append(
                f"{VERIFICACAO}:{n}: 'sem texto integral' mas texto_integral={r['texto_integral']} "
                f"({r['doi']})"
            )
    sem = sum(r["veredito"] == "SEM_TEXTO_INTEGRAL" for r in ver)
    msgs.append(
        f"verificação de texto integral: {len(ver)} linhas; "
        f"{len(ver) - sem} com veredito sobre o conteúdo, todas com texto lido; "
        f"{sem} sem texto integral (não decidem veredito)"
    )
    if (raiz / "paper" / "paper.md").is_file() and (
        raiz / "paper" / "tools" / "verifica_referencias.py"
    ).is_file():
        rv = _py(raiz, "paper/tools/verifica_referencias.py")
        linhas = [
            x
            for x in rv.stdout.splitlines()
            if re.match(r"^\d\. ", x) or "[PASS]" in x or "FALH" in x.upper()
        ]
        msgs += [f"verifica_referencias: {x.strip()}" for x in linhas]
        if rv.returncode:
            falhas.append(
                f"paper/tools/verifica_referencias.py terminou com {rv.returncode} falha(s)"
            )
    else:
        msgs.append(
            "verifica_referencias: NÃO EXERCIDA (o artigo e suas ferramentas entram depois do "
            "primeiro commit, fora do selo)"
        )
    return (FALHOU if falhas else OK), msgs + falhas


def check_inventario(raiz):
    """Inventário público, manifesto e README vêm da mesma distribuição (item 9 do checklist).

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.

    Returns
    -------
    tuple of (int, list of str)
        Código de saída e mensagens.
    """
    falhas, msgs = [], []
    ri = _py(raiz, "scripts/inventario_publico.py", "--check")
    msgs.append("inventário: " + ri.stdout.strip())
    if ri.returncode:
        falhas.append(
            "manifest/INVENTARIO-PUBLICO.{json,md} não confere com o conjunto distribuído"
        )
    with open(raiz / "manifest" / "MANIFESTO-FONTES.csv", encoding="utf-8", newline="") as fh:
        man = {(r["id"], r["url"]) for r in csv.DictReader(fh) if r["parte"] == "A-ledger"}
    regs = _ledgers(raiz)
    fora = sorted({(r.get("id", ""), r.get("url", "")) for _, _, r in regs} - man)
    msgs.append(
        f"manifesto: {len(man)} pares (id, URL) de ledger; "
        f"{len(fora)} par(es) de ledger fora do manifesto"
    )
    falhas += [f"fora do manifesto: {i} {u}" for i, u in fora[:20]]
    inv = json.loads((raiz / "manifest" / "INVENTARIO-PUBLICO.json").read_text(encoding="utf-8"))
    readme = (raiz / "README.md").read_text(encoding="utf-8")
    citados = {
        "identificadores": f"{inv['fontes']['identificadores_unicos']} identificadores",
        "ledgers": f"{inv['ledgers']['n']} ledgers",
        "scripts": f"{inv['scripts']['no_repositorio']} scripts",
    }
    for k, frase in citados.items():
        if frase not in readme:
            falhas.append(f"README não cita '{frase}' (número de {k} do inventário)")
    msgs.append("README cita: " + "; ".join(citados.values()))
    return (FALHOU if falhas else OK), msgs + falhas


def check_privacidade(raiz):
    """Privacidade e conteúdo redistribuído (item 10 do checklist).

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.

    Returns
    -------
    tuple of (int, list of str)
        Código de saída e mensagens.
    """
    falhas, msgs = [], []
    ti = _modulo("_integridade_aud", raiz / "tests" / "test_integridade.py")
    ti.RAIZ = raiz
    for nome in (
        "test_nenhuma_coluna_nominal",
        "test_ids_de_casos_sao_hash_de_10_hex",
        "test_sem_segredo_email_cpf_ou_caminho_de_home",
        "test_nada_de_terceiros_nem_microdado_bruto",
        "test_scripts_usam_repo_root_em_vez_de_caminho_absoluto",
    ):
        try:
            getattr(ti, nome)()
            msgs.append(f"ok {nome}")
        except AssertionError as erro:
            falhas.append(f"{nome}: {str(erro)[:300]}")
    msgs.append(
        "exceções conhecidas de caminho de home (pré-registros com hash gravado): "
        + ", ".join(sorted(ti.CAMINHO_HASH_TRAVADO))
    )
    codigo = FALHOU if falhas else OK
    gl = shutil.which("gitleaks")
    if not gl:
        msgs.append("gitleaks: NÃO EXERCIDO (não instalado)")
        codigo = codigo or NAO_EXERCIDO
    else:
        prov = _modulo("_prov_priv", raiz / "make_provenance.py")
        with tempfile.TemporaryDirectory() as tmp:
            for a in prov.arquivos():
                (Path(tmp) / a).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(raiz / a, Path(tmp) / a)
            g = subprocess.run(
                [gl, "detect", "--source", tmp, "--no-git", "--no-banner", "--redact"],
                capture_output=True,
                text=True,
            )
        resumo = (
            re.sub(r"\x1b\[[0-9;]*m", "", g.stdout + g.stderr).strip().splitlines()
        )  # sem cores de terminal
        msgs.append(
            "gitleaks (conjunto distribuído): "
            + (resumo[-1] if resumo else f"código {g.returncode}")
        )
        if g.returncode:
            falhas.append("gitleaks achou possível segredo")
            codigo = FALHOU
    msgs.append(
        "varredura de nomes de vítimas: não exercível a partir do clone "
        "(exige a lista nominal, que não é distribuída); "
        "o resultado da última varredura do autor fica no relatório da versão"
    )
    return codigo, msgs + falhas


def check_release(raiz, final=False):
    """Fase de publicação (item 12 do checklist).

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz do repositório auditado.
    final : bool
        ``True`` para ``--stage final`` (exige URL pública, release e DOI).

    Returns
    -------
    tuple of (int, list of str)
        Código de saída e mensagens.
    """
    falhas, msgs = [], []
    pyproj = re.search(
        r'^version = "([^"]+)"', (raiz / "pyproject.toml").read_text(encoding="utf-8"), re.M
    )
    cff = re.search(r"^version: (\S+)", (raiz / "CITATION.cff").read_text(encoding="utf-8"), re.M)
    cm = json.loads((raiz / "codemeta.json").read_text(encoding="utf-8"))
    zen = json.loads((raiz / ".zenodo.json").read_text(encoding="utf-8"))
    versoes = {
        "pyproject": pyproj and pyproj.group(1),
        "CITATION.cff": cff and cff.group(1),
        "codemeta": cm.get("version"),
        ".zenodo.json": zen.get("version"),
    }
    msgs.append("versões: " + ", ".join(f"{k} {v}" for k, v in versoes.items()))
    if len(set(versoes.values())) != 1 or not str(versoes["pyproject"]).startswith("0."):
        falhas.append("versões divergentes ou fora de 0.x antes do DOI")
    if zen.get("access_right") != "closed":
        falhas.append(
            ".zenodo.json: access_right deveria ser 'closed' antes da autorização do autor"
        )
    if "doi" in (raiz / "CITATION.cff").read_text(encoding="utf-8").split("references:")[0].lower():
        falhas.append("CITATION.cff traz DOI próprio antes do release")
    if falhas:
        return FALHOU, msgs + falhas
    msgs.append("fase pré-DOI coerente (0.x, acesso fechado, sem DOI próprio)")
    etapa = "final" if final else "pré-release"
    msgs.append(
        f"NÃO EXERCIDO ({etapa}): ainda não há repositório público, toggle do Zenodo, "
        "release rc1 nem DOI; "
        "a sequência repositório -> Zenodo -> rc1 -> DOI -> final "
        "só pode ser conferida depois do aval do autor"
    )
    return NAO_EXERCIDO, msgs


def main(argv=None):
    """Interpreta os argumentos, roda a verificação pedida e devolve o código de saída.

    Parameters
    ----------
    argv : list of str, optional
        Argumentos (padrão: ``sys.argv[1:]``).

    Returns
    -------
    int
        0 atendido, 1 não atendido, 2 não exercido.
    """
    argv = sys.argv[1:] if argv is None else argv
    if "--check" not in argv:
        print(__doc__)
        return FALHOU
    qual = argv[argv.index("--check") + 1]
    raiz = (
        Path(argv[argv.index("--raiz") + 1]).resolve()
        if "--raiz" in argv
        else Path(__file__).resolve().parents[1]
    )
    checks = {
        "literatura": check_literatura,
        "inventario": check_inventario,
        "privacidade": check_privacidade,
    }
    if qual == "release":
        codigo, msgs = check_release(raiz, final="final" in argv)
    elif qual in checks:
        codigo, msgs = checks[qual](raiz)
    else:
        print(f"check desconhecido: {qual}")
        return FALHOU
    for m in msgs:
        print(" ", m)
    print(
        {OK: f"[OK] {qual}", FALHOU: f"[FALHOU] {qual}", NAO_EXERCIDO: f"[NÃO EXERCIDO] {qual}"}[
            codigo
        ]
    )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
