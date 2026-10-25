"""Inventário público gerado só a partir do que este repositório distribui.

(escrutínio Astra, item T02).

O painel do artigo (``dashboard/build_dashboard.py``) contou fontes, idiomas, tipos e scripts na
árvore completa do projeto de origem, que não é distribuída. Este script refaz as contagens com os
arquivos do repositório, usando as MESMAS regras de identidade, idioma e tipo (funções importadas do
painel, sem cópia), e reconcilia com os números do painel
(``dashboard/dashboard_dados.publico.json``).

Regras (também gravadas na saída):

- conjunto: arquivos distribuídos segundo ``make_provenance.arquivos()`` (mesmo conjunto do selo);
- ledgers: todo ``sources*.jsonl`` do conjunto; registro = linha não vazia;
- fonte única (identificador): ``chave_id`` do painel (DOI em minúsculas; URL minúscula sem barra
  final; URL doi.org dobrada em DOI);
- obra distinta: identificador sem o sufixo de versão ``/vN`` de DOI (o mesmo preprint registrado
  com e sem ``/v1`` conta uma vez);
- idioma: ``idioma_do_id`` do painel (pt e pt-BR fundidos; maioria; empate pelo ledger consolidado);
- tipo: ``tipo_do_id`` do painel; quartis da planilha ``verificacao-metadados.csv`` (metadados
  extraídos das planilhas privadas de verificação) e das tabelas dos dossiês em ``docs/dossies/``,
  nessa ordem;
- scripts: todo ``*.py`` do conjunto; cruzado com a lista dos 139 do título (painel).

Uso::

    python3 -I scripts/inventario_publico.py           # grava manifest/INVENTARIO-PUBLICO.{json,md}
    python3 -I scripts/inventario_publico.py --check   # só confere com o gravado
                                                       # (exit 1 se divergir)
"""

import csv
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA_JSON = RAIZ / "manifest" / "INVENTARIO-PUBLICO.json"
SAIDA_MD = RAIZ / "manifest" / "INVENTARIO-PUBLICO.md"
PAINEL_JSON = "dashboard/dashboard_dados.publico.json"
VERSAO = re.compile(r"/v\d+$")
QUARTIL_DOSSIE = re.compile(r"\|\s*(10\.\d{4,9}/[^\s|]+)\s*\|\s*(Q[1-4])")
DOSSIES = (
    "DOSSIE-CONSOLIDADO-2026-10-12.md",
    "DOSSIE-2026-10-11-parte2.md",
    "DOSSIE-2026-10-10.md",
)
# Diretórios cujos scripts são de análise (geram ou leem dados); o resto é empacotamento do
# repositório.
ANALISE = ("dados/", "simulacao/", "research-")


def _modulo(nome, rel):
    """Importa um arquivo .py do repositório como módulo, sem executar o bloco ``__main__``.

    Parameters
    ----------
    nome : str
        Nome do módulo a registrar.
    rel : str
        Caminho relativo à raiz do repositório.

    Returns
    -------
    module
        Módulo carregado.
    """
    spec = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def obra(chave):
    """Chave de obra distinta: identificador sem o sufixo de versão ``/vN`` quando é DOI.

    Parameters
    ----------
    chave : str
        Identificador único segundo ``chave_id`` do painel.

    Returns
    -------
    str
        Chave sem versão (igual à entrada se não for DOI versionado).
    """
    return VERSAO.sub("", chave) if chave.startswith("doi:") else chave


def carregar_ledgers(conjunto):
    """Lê todos os ledgers distribuídos.

    Parameters
    ----------
    conjunto : list of str
        Caminhos relativos dos arquivos distribuídos.

    Returns
    -------
    tuple of (list of str, list of dict)
        Ledgers (ordenados) e registros, cada um com o campo ``_f`` (ledger de origem).
    """
    arqs = sorted(a for a in conjunto if re.search(r"(^|/)sources[^/]*\.jsonl$", a))
    regs = []
    for a in arqs:
        for linha in (RAIZ / a).read_text(encoding="utf-8").splitlines():
            if linha.strip():
                r = json.loads(linha)
                r["_f"] = a
                regs.append(r)
    return arqs, regs


def quartis():
    """Quartis na mesma ordem do painel: planilhas de verificação, depois tabelas dos dossiês.

    No repositório a planilha é ``verificacao-metadados.csv`` (só metadados extraídos das planilhas
    privadas de verificação; mesma coluna ``quartil_sjr``) e os dossiês ficam em ``docs/dossies/``.

    Returns
    -------
    dict
        DOI em minúsculas -> ``"Q1"``..``"Q4"`` (primeira ocorrência vale).
    """
    q = {}
    for arq in sorted(
        (RAIZ / "research-2026-10-21-rodada3" / "A-textointegral").glob("verificacao-*.csv")
    ):
        with open(arq, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                m = re.match(r"\s*Q([1-4])", r.get("quartil_sjr", ""))
                if m:
                    q.setdefault(r["doi"].strip().lower(), "Q" + m.group(1))
    for nome in DOSSIES:
        for linha in (RAIZ / "docs" / "dossies" / nome).read_text(encoding="utf-8").splitlines():
            for m in QUARTIL_DOSSIE.finditer(linha):
                q.setdefault(m.group(1).lower(), m.group(2))
    return q


def contar(regs, painel, quart):
    """Identificadores, idiomas e tipos de um conjunto de registros, com as regras do painel.

    Parameters
    ----------
    regs : list of dict
        Registros de ledger (com ``_f``).
    painel : module
        ``dashboard/build_dashboard.py`` importado.
    quart : dict
        DOI -> quartil.

    Returns
    -------
    tuple of (dict, dict, collections.Counter)
        Registros por identificador, idioma por identificador e contagem por tipo.
    """
    por_id = defaultdict(list)
    for r in regs:
        por_id[painel.chave_id(r)].append(r)
    idioma = {k: painel.idioma_do_id(v)[0] for k, v in por_id.items()}
    return por_id, idioma, Counter(painel.tipo_do_id(v, quart) for v in por_id.values())


def calcular():
    """Calcula o inventário a partir do conjunto distribuído.

    Returns
    -------
    dict
        Inventário (contagens, regras, listas e reconciliação com o painel).
    """
    prov = _modulo("_prov", "make_provenance.py")
    painel = _modulo("_painel", "dashboard/build_dashboard.py")
    conjunto = prov.arquivos()
    arqs, regs = carregar_ledgers(conjunto)
    quart = quartis()
    por_id, idioma, tipos = contar(regs, painel, quart)
    obras = defaultdict(set)
    for k in por_id:
        obras[obra(k)].add(k)
    versoes = sorted(sorted(v) for v in obras.values() if len(v) > 1)
    idiomas_obra = Counter(idioma[sorted(v)[0]] for v in obras.values())
    publico = json.loads((RAIZ / PAINEL_JSON).read_text(encoding="utf-8"))["numeros"]
    lista139 = publico["scripts"]["origem"]["lista"]
    scripts = sorted(a for a in conjunto if a.endswith(".py"))
    no_repo = sorted(set(lista139) & set(scripts))
    fora = sorted(set(lista139) - set(scripts))
    extras = sorted(set(scripts) - set(lista139))
    extras_analise = [a for a in extras if a.startswith(ANALISE)]
    extras_pacote = [a for a in extras if not a.startswith(ANALISE)]
    ledgers_painel = publico["fontes_unicas"]["origem"]["arquivos"]
    # mesmo cálculo restrito aos ledgers que o painel contou: tem de reproduzir os números do painel
    sub_id, sub_idioma, sub_tipos = contar(
        [r for r in regs if r["_f"] in ledgers_painel], painel, quart
    )
    return {
        "regras": {
            "conjunto": "arquivos distribuídos segundo make_provenance.arquivos() "
            "(o mesmo conjunto do selo)",
            "ledger": "todo sources*.jsonl do conjunto; registro = linha não vazia",
            "fonte_unica": "chave_id do painel: DOI minúsculo; URL minúscula sem barra final; "
            "URL doi.org vira DOI",
            "obra_distinta": "fonte única sem o sufixo /vN de DOI "
            "(mesmo preprint com e sem versão conta uma vez)",
            "idioma": "idioma_do_id do painel: pt e pt-BR fundidos; maioria entre registros; "
            "empate pelo ledger consolidado",
            "tipo": "tipo_do_id do painel; quartis de A-textointegral/verificacao-metadados.csv "
            "(extraída das planilhas privadas de verificação, só metadados) e das tabelas dos "
            "dossiês em docs/dossies/, nessa ordem",
            "scripts": "todo *.py do conjunto; cruzado com a lista dos 139 do título (painel); "
            "análise = dados/, simulacao/, research-*; o resto é empacotamento do repositório",
        },
        "ledgers": {"n": len(arqs), "arquivos": arqs, "registros": len(regs)},
        "fontes": {
            "identificadores_unicos": len(por_id),
            "obras_distintas": len(obras),
            "pares_de_versao": versoes,
            "por_idioma_identificador": dict(
                sorted(Counter(idioma.values()).items(), key=lambda kv: (-kv[1], kv[0]))
            ),
            "por_idioma_obra": dict(sorted(idiomas_obra.items(), key=lambda kv: (-kv[1], kv[0]))),
            "idiomas": len(set(idioma.values())),
            "por_tipo": {t: tipos.get(t, 0) for t in painel.TIPOS},
        },
        "scripts": {
            "no_repositorio": len(scripts),
            "lista_do_titulo": len(lista139),
            "da_lista_no_repositorio": len(no_repo),
            "da_lista_fora_do_repositorio": fora,
            "fora_da_lista_analise": extras_analise,
            "fora_da_lista_empacotamento": len(extras_pacote),
            "empacotamento_por_pasta": dict(
                sorted(
                    Counter(
                        a.split("/")[0] if "/" in a else "(raiz)" for a in extras_pacote
                    ).items()
                )
            ),
        },
        "reconciliacao_painel": {
            "painel_ledgers": publico["ledgers"]["valor"],
            "painel_registros": publico["registros_brutos"]["valor"],
            "painel_fontes_unicas": publico["fontes_unicas"]["valor"],
            "painel_idiomas": publico["idiomas"]["valor"],
            "painel_tipos": publico["tipos"]["valor"],
            "painel_scripts": publico["scripts"]["valor"],
            "so_ledgers_do_painel": {
                "registros": sum(len(v) for v in sub_id.values()),
                "identificadores_unicos": len(sub_id),
                "idiomas": len(set(sub_idioma.values())),
                "por_tipo": {t: sub_tipos.get(t, 0) for t in painel.TIPOS},
                "iguais_ao_painel": (
                    sum(len(v) for v in sub_id.values()) == publico["registros_brutos"]["valor"]
                    and len(sub_id) == publico["fontes_unicas"]["valor"]
                    and len(set(sub_idioma.values())) == publico["idiomas"]["valor"]
                    and {t: sub_tipos.get(t, 0) for t in painel.TIPOS} == publico["tipos"]["valor"]
                ),
            },
            "ledgers_do_painel_ausentes_no_repositorio": sorted(set(ledgers_painel) - set(arqs)),
            "ledgers_do_repositorio_posteriores_ao_painel": sorted(set(arqs) - set(ledgers_painel)),
        },
    }


def markdown(inv, h):
    """Versão legível do inventário.

    Parameters
    ----------
    inv : dict
        Saída de :func:`calcular`.
    h : str
        sha256 do JSON gravado.

    Returns
    -------
    str
        Texto Markdown (GFM).
    """
    f, s, r = inv["fontes"], inv["scripts"], inv["reconciliacao_painel"]
    linhas = [
        "# Inventário público (gerado por `scripts/inventario_publico.py`; não editar à mão)",
        "",
        f"sha256 de `manifest/INVENTARIO-PUBLICO.json`: `{h}`",
        "",
        "Contado só com os arquivos deste repositório (o mesmo conjunto do selo), "
        "com as regras de identidade, idioma e tipo do painel do artigo.",
        "",
        "| Item | Repositório | Painel do artigo (árvore privada, até 2026-10-23) |",
        "| --- | --- | --- |",
        f"| Ledgers `sources.jsonl` | {inv['ledgers']['n']} | {r['painel_ledgers']} |",
        f"| Registros nos ledgers | {inv['ledgers']['registros']} | {r['painel_registros']} |",
        f"| Fontes únicas (identificadores) | {f['identificadores_unicos']} "
        f"| {r['painel_fontes_unicas']} |",
        f"| Obras distintas (sem sufixo de versão) | {f['obras_distintas']} | - |",
        f"| Idiomas | {f['idiomas']} | {r['painel_idiomas']} |",
        f"| Scripts Python | {s['no_repositorio']} | {r['painel_scripts']} |",
        "",
        "## Regras",
        "",
        *[f"- **{k}**: {v}" for k, v in inv["regras"].items()],
        "",
        "## Fontes por idioma (identificadores únicos)",
        "",
        "| Idioma | n |",
        "| --- | --- |",
        *[f"| {k} | {v} |" for k, v in f["por_idioma_identificador"].items()],
        "",
        "## Fontes por tipo (identificadores únicos)",
        "",
        "| Tipo | Repositório | Painel |",
        "| --- | --- | --- |",
        *[f"| {k} | {v} | {r['painel_tipos'].get(k, 0)} |" for k, v in f["por_tipo"].items()],
        "",
        "Diferenças de tipo vêm só das fontes novas da v0.3 "
        "(ledgers posteriores ao painel, abaixo).",
        "",
        f"**Reconciliação.** O mesmo cálculo, restrito aos {r['painel_ledgers']} ledgers "
        f"que o painel contou, dá "
        f"{r['so_ledgers_do_painel']['registros']} registros, "
        f"{r['so_ledgers_do_painel']['identificadores_unicos']} identificadores, "
        f"{r['so_ledgers_do_painel']['idiomas']} idiomas e a mesma contagem por tipo: "
        + (
            "**igual ao painel em tudo**."
            if r["so_ledgers_do_painel"]["iguais_ao_painel"]
            else "**DIFERENTE do painel** (ver o JSON)."
        )
        + f" Os {f['identificadores_unicos'] - r['so_ledgers_do_painel']['identificadores_unicos']}"
        " identificadores a mais vêm dos ledgers posteriores ao painel.",
        "",
        "## Pares de versão fundidos em obra única",
        "",
        *[f"- {' = '.join(f'`{x}`' for x in par)}" for par in f["pares_de_versao"]],
        "",
        "## Scripts",
        "",
        f"- Lista do título (painel): {s['lista_do_titulo']}; "
        f"no repositório: {s['da_lista_no_repositorio']}; "
        f"fora: {len(s['da_lista_fora_do_repositorio'])} (aquisição e ferramentas de lote, "
        "que leem material de terceiros não distribuído).",
        *[f"  - `{a}`" for a in s["da_lista_fora_do_repositorio"]],
        f"- Fora da lista, de análise ({len(s['fora_da_lista_analise'])}): "
        "criados depois do painel (v0.3) ou em pastas de dados.",
        *[f"  - `{a}`" for a in s["fora_da_lista_analise"]],
        f"- Fora da lista, de empacotamento ({s['fora_da_lista_empacotamento']}): "
        + "; ".join(f"{k} {v}" for k, v in s["empacotamento_por_pasta"].items())
        + ".",
        "",
        "## Ledgers",
        "",
        *[f"- `{a}`" for a in inv["ledgers"]["arquivos"]],
        "",
        "Posteriores ao painel: "
        + (
            ", ".join(f"`{a}`" for a in r["ledgers_do_repositorio_posteriores_ao_painel"])
            or "nenhum"
        )
        + ".",
        "Do painel e ausentes aqui: "
        + (", ".join(f"`{a}`" for a in r["ledgers_do_painel_ausentes_no_repositorio"]) or "nenhum")
        + ".",
        "",
    ]
    return "\n".join(linhas)


def main():
    """Grava (ou confere, com ``--check``) o inventário.

    Returns
    -------
    int
        0 se gravou ou se confere; 1 se ``--check`` achou divergência.
    """
    inv = calcular()
    js = json.dumps(inv, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    h = hashlib.sha256(js.encode("utf-8")).hexdigest()
    md = markdown(inv, h)
    if "--check" in sys.argv:
        ok = (
            SAIDA_JSON.exists()
            and SAIDA_JSON.read_text(encoding="utf-8") == js
            and SAIDA_MD.exists()
            and SAIDA_MD.read_text(encoding="utf-8") == md
        )
        print(
            "inventário confere com o gravado"
            if ok
            else "inventário DIVERGE do gravado: rode scripts/inventario_publico.py"
        )
        return 0 if ok else 1
    SAIDA_JSON.write_text(js, encoding="utf-8")
    SAIDA_MD.write_text(md, encoding="utf-8")
    print(
        f"inventário gravado: {inv['ledgers']['n']} ledgers, "
        f"{inv['ledgers']['registros']} registros, "
        f"{inv['fontes']['identificadores_unicos']} identificadores, "
        f"{inv['fontes']['obras_distintas']} obras, "
        f"{inv['fontes']['idiomas']} idiomas, "
        f"{inv['scripts']['no_repositorio']} scripts; sha256 {h}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
