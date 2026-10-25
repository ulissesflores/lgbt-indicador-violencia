"""Testes de ``scripts/auditar_publicacao.py`` e ``scripts/inventario_publico.py`` (v0.3).

Cada verificação roda no repositório (tem de passar) e numa cópia do conjunto distribuído com um
erro plantado (controle negativo: tem de falhar com código 1). ``release`` sai 2 (NÃO EXERCIDO)
enquanto não há repositório público, e 1 se os metadados da fase pré-DOI forem quebrados.
"""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
AUD = RAIZ / "scripts" / "auditar_publicacao.py"


def _rodar(raiz, check):
    """Roda o auditor sobre ``raiz`` e devolve (código, saída).

    Parameters
    ----------
    raiz : pathlib.Path
        Raiz a auditar.
    check : str
        Nome da verificação.

    Returns
    -------
    tuple of (int, str)
        Código de saída e saída padrão.
    """
    r = subprocess.run(
        [
            sys.executable,
            "-B",
            "-I",
            str(raiz / "scripts" / "auditar_publicacao.py"),
            "--check",
            check,
            "--raiz",
            str(raiz),
        ],
        capture_output=True,
        text=True,
        cwd=str(raiz),
    )
    return r.returncode, r.stdout + r.stderr


def _copia(tmp):
    """Copia o conjunto distribuído (o mesmo do selo) para ``tmp`` e devolve a raiz da cópia.

    Parameters
    ----------
    tmp : str
        Diretório temporário.

    Returns
    -------
    pathlib.Path
        Raiz da cópia.
    """
    spec = importlib.util.spec_from_file_location("_prov_teste", RAIZ / "make_provenance.py")
    prov = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prov)
    dst = Path(tmp) / "repo"
    for a in prov.arquivos():
        (dst / a).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ / a, dst / a)
    return dst


def test_inventario_confere_e_reproduz_o_painel():
    """O inventário gravado é o que o script gera.

    Restrito aos 17 ledgers do painel, reproduz 829 / 1.569 / 10 / tipos.
    """
    r = subprocess.run(
        [sys.executable, "-B", "-I", str(RAIZ / "scripts" / "inventario_publico.py"), "--check"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout
    inv = json.loads((RAIZ / "manifest" / "INVENTARIO-PUBLICO.json").read_text(encoding="utf-8"))
    sub = inv["reconciliacao_painel"]["so_ledgers_do_painel"]
    assert (
        sub["iguais_ao_painel"]
        and sub["identificadores_unicos"] == 829
        and sub["registros"] == 1569
        and sub["idiomas"] == 10
    )
    assert inv["fontes"]["pares_de_versao"] == [
        ["doi:10.21203/rs.3.rs-2864681", "doi:10.21203/rs.3.rs-2864681/v1"]
    ]
    assert (
        inv["scripts"]["lista_do_titulo"] == 139
        and inv["scripts"]["da_lista_no_repositorio"] == 128
    )
    assert len(inv["scripts"]["da_lista_fora_do_repositorio"]) == 11
    assert inv["reconciliacao_painel"]["ledgers_do_painel_ausentes_no_repositorio"] == []


def test_auditor_no_repositorio():
    """No repositório: inventário e privacidade passam.

    Privacidade 2 só sem gitleaks; release = NÃO EXERCIDO; literatura sem falha de ledger.
    """
    assert _rodar(RAIZ, "inventario")[0] == 0
    cod, saida = _rodar(RAIZ, "privacidade")
    assert cod == (0 if shutil.which("gitleaks") else 2), saida
    assert _rodar(RAIZ, "release")[0] == 2
    spec = importlib.util.spec_from_file_location("_aud", AUD)
    aud = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aud)
    _, msgs = aud.check_literatura(RAIZ)
    # o resultado de paper/tools/verifica_referencias.py depende do texto do artigo em edição: o
    # comando do auditor o reporta
    assert not [
        m
        for m in msgs
        if (
            "registro sem" in m
            or "veredito" in m
            and "sem texto lido" in m
            or "mas texto_integral" in m
        )
    ]


def test_auditor_falha_com_erro_plantado():
    """Controles negativos com erro plantado.

    Casos: caminho de home, veredito sem texto lido, script novo sem inventário e acesso aberto
    antes do DOI.
    """
    with tempfile.TemporaryDirectory() as tmp:
        c = _copia(tmp)
        readme = c / "dados" / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8") + "\n/" + "Users/fulano/pasta\n", encoding="utf-8"
        )
        assert _rodar(c, "privacidade")[0] == 1
        ver = c / "research-2026-10-21-rodada3" / "A-textointegral" / "verificacao-metadados.csv"
        linhas = ver.read_text(encoding="utf-8").splitlines()
        k = next(i for i, x in enumerate(linhas) if ",sim,CONFIRMADO," in x)
        linhas[k] = linhas[k].replace(",sim,CONFIRMADO,", ",nao,CONFIRMADO,")
        ver.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        assert _rodar(c, "literatura")[0] == 1
        (c / "dados" / "script_novo.py").write_text('"""Script plantado."""\n', encoding="utf-8")
        assert _rodar(c, "inventario")[0] == 1
        z = c / ".zenodo.json"
        z.write_text(z.read_text(encoding="utf-8").replace('"closed"', '"open"'), encoding="utf-8")
        assert _rodar(c, "release")[0] == 1
