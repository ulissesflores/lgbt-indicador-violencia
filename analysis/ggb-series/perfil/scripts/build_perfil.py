# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
"""Verify every verbatim quote of the GGB profile and write the evidence tables.

For each claim registered in claims.py it finds the quote in the text of the source file (PDF
page by page through pdftotext, or a saved web text), computes the page and the file SHA-256,
and writes the evidence table and the year-by-year methodology table. It aborts with exit status
1 if any quote is not found. It also rebuilds the source ledger by calling the emit_sources
script once per source file used.

Inputs
------
- analysis/ggb-series/perfil/scripts/claims.py (claims, methodology rows, source file registry)
- source files under sources/public/p3-ggb/_raw/ (PDFs and saved web pages; not tracked in git)
- poppler tools pdftotext and pdfinfo on the PATH
- the ledger script named by EMIT_SOURCES (default emit_sources.py)

Outputs
-------
- analysis/ggb-series/perfil/evidencias.csv
- analysis/ggb-series/perfil/metodologia_por_ano.csv
- analysis/ggb-series/perfil/sources.jsonl (deleted and rebuilt)
- prints the counts of evidence rows, methodology rows and sources to stdout

Usage
-----
python3 -I analysis/ggb-series/perfil/scripts/build_perfil.py

Status
------
No registration status is claimed for this file.

Notes
-----
Original description (Portuguese), kept verbatim:

Verifica cada trecho verbatim contra o arquivo, calcula pagina e sha256, grava CSVs e o ledger.
uso: python3 -I build_perfil.py   (cwd irrelevante; caminhos absolutos)

Author
------
Carlos Ulisses Flores (Codex Hash Research Laboratory),
ORCID https://orcid.org/0000-0002-6034-7765.
Repository: https://github.com/ulissesflores/lgbt-indicador-violencia
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as K

OUT = (REPO_ROOT + '/analysis/ggb-series/perfil/')
EMIT = _os.environ.get("EMIT_SOURCES", "emit_sources.py")
PY = sys.executable

def ns(s):  # compara sem espacos, hifens de quebra e soft hyphen
    return re.sub(r'[\s­]+', '', s).replace('-', '')

sha_cache, page_cache = {}, {}
def sha(p):
    if p not in sha_cache:
        sha_cache[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return sha_cache[p]

def pages(key):
    if key in page_cache: return page_cache[key]
    f = K.FILES[key]
    if f['txt']:
        pg = [('html', ns(open(f['txt'], encoding='utf8', errors='replace').read()))]
    else:
        raw = subprocess.run(['pdftotext', f['path'], '-'], capture_output=True, text=True).stdout.split('\f')
        n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', f['path']], capture_output=True, text=True).stdout).group(1))
        pg = [(str(i), ns(t)) for i, t in enumerate(raw[:n], 1)]
    page_cache[key] = pg
    return pg

def locate(key, quote):
    q = ns(quote)
    hits = [p for p, t in pages(key) if q in t]
    return hits

bad, ev, used = [], [], set()
for cid, sec, claim, key, quote in K.C:
    h = locate(key, quote) if cid != 'ID09' else ['visual:1-4']
    if not h:
        bad.append((cid, key, quote[:70])); continue
    used.add(key)
    f = K.FILES[key]
    pag = h[0] if f['txt'] is None else 'pagina web (snapshot/URL na coluna fonte)'
    ev.append(dict(id=cid, secao=sec, afirmacao=claim, arquivo=f['path'], pagina_pdf=pag, n_paginas_com_o_trecho=len(h),
                   trecho_verbatim=quote, sha256=sha(f['path']), url_origem=f['url'],
                   verificacao='leitura visual do scan (sem camada de texto)' if cid == 'ID09' else 'trecho localizado por busca automatica no texto do arquivo'))
mt, bad_m = [], []
for ano, tot, fontes, crit, mud, key, quote in K.M:
    h = locate(key, quote)
    if not h:
        bad_m.append((ano, key, quote[:70])); continue
    used.add(key)
    f = K.FILES[key]
    mt.append(dict(ano=ano, total_declarado=tot, fontes_declaradas=fontes, criterio_inclusao=crit, mudancas=mud,
                   pagina=h[0] if f['txt'] is None else 'pagina web', arquivo=f['path'], sha256=sha(f['path']),
                   trecho_verbatim=quote, url_origem=f['url']))
for ano, nota in K.SEM_DOC:
    mt.append(dict(ano=ano, total_declarado='', fontes_declaradas='', criterio_inclusao='', mudancas='NAO PUBLICADO/NAO LOCALIZADO: ' + nota,
                   pagina='', arquivo='', sha256='', trecho_verbatim='', url_origem=''))
mt.sort(key=lambda r: str(r['ano']))
if bad or bad_m:
    print('FALHAS DE VERBATIM:'); [print(' ', b) for b in bad + bad_m]; sys.exit(1)

def w(name, rows):
    with open(OUT + name, 'w', newline='', encoding='utf8') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
w('evidencias.csv', ev)
w('metodologia_por_ano.csv', mt)

# ledger (so via emit_sources.py); recria do zero (arquivo e meu)
led = OUT + 'sources.jsonl'
if os.path.exists(led): os.remove(led)
for key in sorted(used):
    f = K.FILES[key]
    notas = {'wayback': 'copia Wayback id_ (bytes originais); ', 'oa': ''}
    nota = notas.get(f['acesso'], '') + 'contagem declarada/ documento citado; sha256 do arquivo local em _raw (fora do git)'
    cmd = [PY, EMIT, '--out', OUT, '--url', f['url'], '--id', f['url'], '--id-kind', 'url', '--acesso', f['acesso'],
           '--idioma', f['idioma'], '--canal', f['canal'], '--titulo', f['titulo'], '--ano', str(f['ano']),
           '--sha256', sha(f['path']), '--nota', nota, '--origem', 'rodada3-GGB-perfil']
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print('EMIT FALHOU', key, r.stderr[:300]); sys.exit(1)
print('ok: evidencias', len(ev), '| metodologia', len(mt), '| ledger', len(used), '| arquivos usados', sorted(used))
