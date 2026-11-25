# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Write the source ledger of the GGB series study.

Reads the panel of deaths and, for each distinct source document in it, calls the ledger
script named by EMIT_SOURCES (default emit_sources.py) to append an entry with URL, access
type, language, channel, title, year and SHA-256. It then adds a fixed list of sources that
were consulted but are not in the panel. It stops if the ledger file already exists.

Inputs
------
- analysis/ggb-series/series/painel_mortes_lgbt.csv
- the ledger script named by EMIT_SOURCES

Outputs
-------
- analysis/ggb-series/series/sources.jsonl
- prints the ledger path to stdout

Usage
-----
python3 -I analysis/ggb-series/series/scripts/s07_emit_sources.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Gera series/sources.jsonl SOMENTE via emit_sources.py (ledger). Le o painel (doc_id, url, sha256, titulo) + fontes consultadas fora do painel.
Rodar uma vez; para refazer, apague series/sources.jsonl (arquivo nosso) antes. Uso: python3 -I s07_emit_sources.py

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, subprocess, pathlib, re, hashlib, sys
S = pathlib.Path(__file__).resolve().parent.parent
EM = _os.environ.get("EMIT_SOURCES", "emit_sources.py")
BASE = pathlib.Path(REPO_ROOT)
if (S / "sources.jsonl").exists(): sys.exit("sources.jsonl ja existe: apague para refazer")
def emit(**k):
    cmd = [sys.executable, EM, "--out", str(S), "--origem", "rodada3-GGB-series"]
    for a, v in k.items():
        if v not in (None, ""): cmd += ["--" + a.replace("_", "-"), str(v)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"emit falhou: {k.get('id')}: {r.stderr[:300]}")
seen = set()
for r in csv.DictReader(open(S / "painel_mortes_lgbt.csv")):
    if r["doc_id"] in seen or not r["url"]: continue
    seen.add(r["doc_id"])
    if r["url"].startswith("ftp://"): r["url"] = "https://datasus.saude.gov.br/transferencia-de-arquivos/"
    m = re.search(r"(20\d\d)", r["doc_id"]) or re.search(r"(20\d\d)", r["titulo"])
    canal = {"TGEU_TMM": "ong", "TDoR_lista": "ong", "SIM_DATASUS": "oficial"}.get(r["fonte"], "ong" if r["doc_id"].startswith(("ggb", "antra", "obs")) else "oficial" if r["doc_id"].startswith(("anu", "atlas", "sim")) else "imprensa")
    emit(url=r["url"], id=r["url"], id_kind="url", acesso="oa", sha256=r["sha256"] if len(r["sha256"]) == 64 else None, idioma="en" if r["fonte"] in ("TGEU_TMM", "TDoR_lista") else "pt", canal=canal, titulo=r["titulo"], ano=m.group(1) if m else None,
         nota=("contagem declarada" if canal == "ong" else "dado oficial/agregado") + f"; categorias no painel: {r['doc_id']}")
extra = [
 ("https://antrabrasil.org/assassinatos/", "ANTRA, pagina dos dossies de assassinatos (lista de PDFs 2017-2026)", "oa", "pt", "ong", 2026, "pagina publica; nenhum PDF traz lista nominal; Mapa dos Assassinatos tem 'acesso restrito' (ANTRA 2020, nota 18): NAO PUBLICADO sem pedir"),
 ("https://www.google.com/maps/d/viewer?mid=1yMKNg31SYjDAS0N-ZwH1jJ0apFQ", "ANTRA, Mapa dos Assassinatos 2017 (Google My Maps)", "closed", "pt", "ong", 2017, "link citado pelos dossies; KML responde 403 e a pagina e app JS: so navegador (fila-chrome)"),
 ("https://homofobiamata.wordpress.com/", "Homofobia Mata (Eduardo Michels), blog fonte das series GGB 2011-2018", "oa", "pt", "ong", 2018, "so agregados e texto; nenhum arquivo nominal anual encontrado; 'in memoriam'"),
 ("https://zenodo.org/records/7957710", "Observatorio, Dossie 2022 (deposito Zenodo, copia)", "oa", "pt", "ong", 2023, "PDF baixado de zenodo.org API; depositante terceiro (Unesp), conteudo = dossie Acontece/ANTRA/ABGLT"),
 ("https://zenodo.org/records/14715580", "Observatorio, Dossie 2023 (deposito Zenodo, copia)", "oa", "pt", "ong", 2024, "idem"),
 ("https://tdor.translivesmatter.info/reports", "TDoR Remembering Our Dead, relatorios por pais/ano (export publico)", "oa", "en", "ong", 2026, "exports 2008-2025 Brasil em _raw/tdor/anual (nomes so em _raw)"),
 ("https://transmurdermonitoring.tgeu.org/", "TGEU Trans Murder Monitoring (app Uwazi; API publica)", "oa", "en", "ong", 2026, "API /api/search sem login; 5.320 casos globais, 2.031 do Brasil; campo reported_by mostra GGB, IBTE, Rede Trans Brasil"),
 ("https://ondh.mdh.gov.br/", "Painel de dados da Ouvidoria Nacional de Direitos Humanos (Disque 100)", "closed", "pt", "oficial", 2026, "painel interativo: nao lido; fila-chrome; sem ele so ha agregados de imprensa/Atlas"),
]
for u, t, ac, idm, canal, ano, nota in extra:
    emit(url=u, id=u, id_kind="url", acesso=ac, idioma=idm, canal=canal, titulo=t, ano=ano, nota=nota)
print("ledger gerado em", S / "sources.jsonl")
