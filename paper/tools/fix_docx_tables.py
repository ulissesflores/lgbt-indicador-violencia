"""Copiado de um artigo anterior do laboratório (repositório privado);
unica mudanca: caminho do canon (variável CODEX_HASH_CANON; canon da casa, não distribuído).

Post-process the exported DOCX: give every table a fixed layout with a wider
first column (label column), so labels like "Isolation Forest" never wrap
mid-word. Pandoc emits equal-width gridCols for narrow pipe tables; Word then
splits labels. This step is part of the standard export pipeline.

It also owns the HOUSE PAGINATION (`make_apa7_export.py` has PAGE_BREAK = '', so the
page breaks come from here alone) and the proofing language. Both are per-edition:
the heading list is read from the canon (`i18n.langs.<lang>.page_break_before_headings`)
instead of hardcoded, because a PT list applied to the EN edition would break only
before "Abstract" and leave Introduction/References glued to the previous page.

Usage: python scripts/fix_docx_tables.py docs/paper/paper-final.docx [--lang pt-BR|en]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

USABLE = 12240 - 2 * 1440  # Letter width minus 1" margins, in twips
FIRST_COL_WEIGHT = 2.0     # label column twice as wide as the others
CANON = Path(os.environ.get("CODEX_HASH_CANON", "codex-hash-canon.json"))  # canon da casa (não distribuído)
PROOFING = {"pt-BR": "pt-BR", "en": "en-US"}


def fix(path: Path, lang: str = "pt-BR", parte: str = "tudo") -> None:
    heads = json.loads(CANON.read_text(encoding="utf-8"))["i18n"]["langs"][lang][
        "page_break_before_headings"]
    # v0.3 (P2a): o PDF de anexos não tem Resumo/Abstract/Introdução/Referências; nele, cada
    # "Anexo X — ..." abre página (a lista vem do próprio DOCX, não de nome fixo)
    anexos = parte == "anexos"
    if anexos:
        heads = []
    proofing = PROOFING[lang]
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    xml = data["word/document.xml"].decode("utf-8")

    def rewrite_table(m: re.Match) -> str:
        """Grid proporcional ao maior PEDACO INDIVISIVEL de cada coluna.

        Divergencia deliberada do precedente `operating-point-dominance`, que dava peso
        fixo 2.0 a primeira coluna e dividia o resto igualmente: com 6 colunas isso
        partiu "Organizations"/"Organizacoes" no meio da palavra nas DUAS edicoes
        (medido no PDF, 2026-09-04). A regra e a licao 2 da skill `formatacao-agtu`: a
        largura minima de uma coluna e o maior token que nao pode quebrar, nunca a media.
        """
        tbl = m.group(0)
        grid = re.search(r"<w:tblGrid>.*?</w:tblGrid>", tbl, re.S)
        if not grid:
            return tbl
        n = len(re.findall(r"<w:gridCol[^/]*/>", grid.group(0)))
        if n < 2:
            return tbl
        # maior token por coluna, lido das proprias celulas
        maiores = [1] * n
        for row in re.findall(r"<w:tr[^>]*>.*?</w:tr>", tbl, re.S):
            for i, cell in enumerate(re.findall(r"<w:tc>.*?</w:tc>", row, re.S)[:n]):
                texto = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", cell))
                if texto.strip():
                    maiores[i] = max(maiores[i], max(len(w) for w in texto.split()))
        # v0.2: largura por conteúdo, na fonte real da tabela (10 pt; 9 pt com 5+ colunas):
        # piso = maior token (não parte palavra); desejado = maior célula, limitado a 30
        # caracteres (célula curta não quebra; coluna de frase divide a sobra).
        fonte = 180 if n >= 5 else 200          # twips por em
        cw = 0.58 * fonte                       # largura média de caractere (Times)
        maxcel = [1] * n
        for row in re.findall(r"<w:tr[^>]*>.*?</w:tr>", tbl, re.S):
            for i, cell in enumerate(re.findall(r"<w:tc>.*?</w:tc>", row, re.S)[:n]):
                texto = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", cell)).strip()
                maxcel[i] = max(maxcel[i], len(texto))
        pad = 200
        minimos = [int(c * cw) + pad for c in maiores]
        desejados = [max(m, int(min(max(c, 6), 30) * cw) + pad) for m, c in zip(minimos, maxcel)]
        if sum(desejados) <= USABLE:            # tudo cabe sem quebrar: sobra proporcional
            widths = [int(d * USABLE / sum(desejados)) for d in desejados]
        elif sum(minimos) <= USABLE:            # entre piso e desejado
            extra = [d - m for d, m in zip(desejados, minimos)]
            livre = USABLE - sum(minimos)
            widths = [m + int(livre * e / max(1, sum(extra))) for m, e in zip(minimos, extra)]
        else:                                   # nem o piso cabe: proporção do piso
            widths = [max(600, int(USABLE * w / sum(minimos))) for w in minimos]
        widths[-1] += USABLE - sum(widths)   # absorve arredondamento
        novo = "<w:tblGrid>" + "".join(
            f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
        tbl = tbl.replace(grid.group(0), novo, 1)
        # largura declarada por celula tem de acompanhar o grid, senao o Word ignora
        def cell_w(rm: re.Match) -> str:
            row = rm.group(0)
            for i, tcw in enumerate(re.findall(r'<w:tcW [^/]*/>', row)[:n]):
                row = row.replace(tcw, f'<w:tcW w:w="{widths[i]}" w:type="dxa"/>', 1)
            return row
        tbl = re.sub(r"<w:tr[^>]*>.*?</w:tr>", cell_w, tbl, flags=re.S)
        # fonte de tabela a 10pt: APA 7 admite 8 a 12, e reduzir a fonte e sempre melhor
        # que espremer a coluna e partir palavra (licao 5 da mesma skill).
        tbl = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="20"/>', tbl)
        tbl = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="20"/>', tbl)
        return tbl

    xml = re.sub(r"<w:tbl>.*?</w:tbl>", rewrite_table, xml, flags=re.S)

    # fixed layout so Word honours the grid. Idempotent AND dedup-safe: strip any
    # <w:tblLayout> already present in the tblPr (pandoc emits an autofit one, not
    # necessarily as the first child), then insert exactly one "fixed" at the front.
    # <w:tblLayout> is maxOccurs=1 in CT_TblPrBase — a duplicate is invalid OOXML
    # and a second run must not create one (lição 20(c)).
    def set_tbllayout(m: re.Match) -> str:
        tblpr = re.sub(r"<w:tblLayout[^>]*/>", "", m.group(0))
        return tblpr.replace("<w:tblPr>", '<w:tblPr><w:tblLayout w:type="fixed"/>', 1)
    xml = re.sub(r"<w:tblPr>.*?</w:tblPr>", set_tbllayout, xml, flags=re.S)

    # keep each table on ONE page: keepNext on every cell paragraph of every row
    # except the last row (so the whole block flows to the next page if needed).
    # Idempotent: strip any existing keepNext in the row first, then add exactly
    # one — no sentinel dance (the old dance leaked "__KN__" into the DOCX because
    # step 2 re-matched what step 1 had just written; lição 20(c)).
    def keep_table(m: re.Match) -> str:
        tbl = m.group(0)
        rows = re.findall(r"<w:tr[^>]*>.*?</w:tr>", tbl, re.S)
        for row in rows[:-1]:  # every row except the last keeps with the next
            fixed = row.replace("<w:keepNext/>", "")            # strip existing (idempotent)
            fixed = fixed.replace("<w:p><w:pPr>", "<w:p><w:pPr><w:keepNext/>")
            fixed = re.sub(r"<w:p>(?!<w:pPr>)",
                           "<w:p><w:pPr><w:keepNext/></w:pPr>", fixed)
            tbl = tbl.replace(row, fixed, 1)
        return tbl

    xml = re.sub(r"<w:tbl>.*?</w:tbl>", keep_table, xml, flags=re.S)

    # v0.2 (pedido do autor: "o layout da tabela tá feio"): linhas finas horizontais,
    # cabeçalho com fundo sutil e negrito, zebra leve, linha que não quebra entre páginas,
    # margem interna de célula, 9 pt em tabela de 5+ colunas, hash em fonte monoespaçada.
    # Tabela de UMA coluna é "caixa" explicativa: borda inteira e fundo próprio, sem zebra.
    HEX = re.compile(r"^[0-9a-f]{12,64}(?:…|\.\.\.)?$")

    def estilo(m: re.Match) -> str:
        tbl = m.group(0)
        ncol = len(re.findall(r"<w:gridCol[^/]*/>", tbl))
        caixa = ncol == 1
        if caixa:
            bordas = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="2A78D6"/>'
                      '<w:left w:val="single" w:sz="8" w:space="0" w:color="2A78D6"/>'
                      '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="2A78D6"/>'
                      '<w:right w:val="single" w:sz="8" w:space="0" w:color="2A78D6"/></w:tblBorders>')
        else:
            bordas = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="404040"/>'
                      '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="404040"/>'
                      '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="C8CDD3"/></w:tblBorders>')
        mar = ('<w:tblCellMar><w:top w:w="50" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
               '<w:bottom w:w="50" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar>')

        def tblpr(pm: re.Match) -> str:
            t = re.sub(r"<w:tblBorders>.*?</w:tblBorders>|<w:tblCellMar>.*?</w:tblCellMar>", "", pm.group(0), flags=re.S)
            return t.replace("</w:tblPr>", bordas + mar + "</w:tblPr>", 1)
        tbl = re.sub(r"<w:tblPr>.*?</w:tblPr>", tblpr, tbl, count=1, flags=re.S)
        rows = re.findall(r"<w:tr[ >].*?</w:tr>|<w:tr>.*?</w:tr>", tbl, re.S)
        for k, row in enumerate(rows):
            novo = row
            cab = k == 0
            fill = "DCE8F7" if (cab and caixa) else "E9EEF4" if cab else ("F4F6F9" if (k % 2 == 0 and not caixa) else None)
            if caixa and not cab:
                fill = "F3F8FE"
            # trPr: cantSplit (+ tblHeader já vem do pandoc no cabeçalho)
            if "<w:trPr>" in novo:
                novo = novo.replace("<w:trPr>", "<w:trPr><w:cantSplit/>", 1) if "<w:cantSplit/>" not in novo else novo
            elif "<w:trPr " not in novo:
                novo = re.sub(r"^(<w:tr[^>]*>)", r"\1<w:trPr><w:cantSplit/></w:trPr>", novo, count=1)
            if fill:
                shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
                novo = re.sub(r"<w:tcPr\s*/>", f"<w:tcPr>{shd}</w:tcPr>", novo)
                novo = re.sub(r"<w:tcPr>(?!<w:shd)", f"<w:tcPr>{shd}", novo)
            if cab:  # negrito no cabeçalho
                novo = re.sub(r"<w:rPr>(?!<w:b/>)", "<w:rPr><w:b/>", novo)
                novo = re.sub(r"<w:r>(?!<w:rPr>)", "<w:r><w:rPr><w:b/></w:rPr>", novo)
            # hash em monoespaçada
            def mono(rm: re.Match) -> str:
                run = rm.group(0)
                txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run)).strip()
                if HEX.match(txt):
                    run = re.sub(r"<w:rPr>", '<w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>', run, count=1)
                return run
            novo = re.sub(r"<w:r>.*?</w:r>", mono, novo, flags=re.S)
            tbl = tbl.replace(row, novo, 1)
        if ncol >= 5:
            tbl = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="18"/>', tbl)
            tbl = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="18"/>', tbl)
        # células sem rPr de tamanho herdariam Compact 11 pt: força o tamanho em todo run
        tam = "18" if ncol >= 5 else "20"
        def tamanho(rm: re.Match) -> str:
            rpr = rm.group(0)
            if "<w:sz " in rpr:
                return rpr
            ins = f'<w:sz w:val="{tam}"/><w:szCs w:val="{tam}"/>'
            # ordem do esquema OOXML: sz/szCs vêm antes de lang
            return rpr.replace("<w:lang", ins + "<w:lang", 1) if "<w:lang" in rpr else rpr.replace("</w:rPr>", ins + "</w:rPr>")
        tbl = re.sub(r"<w:rPr>.*?</w:rPr>", tamanho, tbl, flags=re.S)
        return tbl

    xml = re.sub(r"<w:tbl>.*?</w:tbl>", estilo, xml, flags=re.S)

    # tabela longa (> 14 linhas) não pode ficar presa numa página só: tira o keepNext dela
    def solta_longa(m: re.Match) -> str:
        tbl = m.group(0)
        # v0.3: também solta tabela de texto longo (mais de ~1.800 caracteres): presa, ela pulava para a página
        # seguinte e deixava a anterior quase vazia (Tabelas 1 e 2 da abertura)
        texto = sum(len(x) for x in re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tbl))
        if len(re.findall(r"<w:tr[ >]", tbl)) > 14 or texto > 1800:
            tbl = tbl.replace("<w:keepNext/>", "")
        # v0.3 (P2a): tabela de várias colunas com mais de 4 linhas pode quebrar entre linhas (a linha
        # não parte, cantSplit, e o cabeçalho se repete, tblHeader); só cabeçalho e 1ª linha seguem presos
        # à legenda. Presa inteira, a Tabela 4 pulava de página e deixava 2/3 da anterior em branco.
        rows = re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S)
        if len(re.findall(r"<w:gridCol[^/]*/>", tbl)) > 1 and len(rows) > 4:
            for row in rows[1:]:
                tbl = tbl.replace(row, row.replace("<w:keepNext/>", ""), 1)
        return tbl
    xml = re.sub(r"<w:tbl>.*?</w:tbl>", solta_longa, xml, flags=re.S)

    # anexos (a partir de "Anexo A"): tipografia compacta (8 pt) e tabela que pode quebrar
    # entre páginas (o cabeçalho se repete pelo tblHeader do pandoc); só o cabeçalho e a
    # primeira linha seguem presos, para a legenda não ficar sozinha. Evita meia página em branco.
    ini = xml.find(">Anexo A — ")
    if ini != -1:
        def anexo(m: re.Match) -> str:
            tbl = m.group(0)
            rows = re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S)
            for row in rows[1:]:
                tbl = tbl.replace(row, row.replace("<w:keepNext/>", ""), 1)
            tbl = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="16"/>', tbl)
            return re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="16"/>', tbl)
        xml = xml[:ini] + re.sub(r"<w:tbl>.*?</w:tbl>", anexo, xml[ini:], flags=re.S)

    # Resumo/Abstract: o parágrafo antes de "Palavras-chave:"/"Keywords:" fica com ele na
    # mesma página (no v0.1 as palavras-chave caíram sozinhas na página seguinte).
    def junta_chaves(m: re.Match) -> str:
        p = m.group(1)
        if "<w:keepNext/>" in p:
            return m.group(0)
        p = p.replace("<w:pPr>", "<w:pPr><w:keepNext/>", 1) if "<w:pPr>" in p else re.sub(r"^<w:p>", "<w:p><w:pPr><w:keepNext/></w:pPr>", p)
        return p + m.group(2)
    # linha de palavras-chave alinhada à esquerda (justificada, abria buracos entre as palavras)
    def chave_esq(m: re.Match) -> str:
        p = m.group(0)
        p = re.sub(r'<w:jc w:val="[^"]+"\s*/>', "", p)
        return p.replace("</w:pPr>", '<w:jc w:val="left"/></w:pPr>', 1) if "</w:pPr>" in p else p.replace("<w:p>", '<w:p><w:pPr><w:jc w:val="left"/></w:pPr>', 1)
    xml = re.sub(r"(<w:p>(?:(?!</w:p>).)*</w:p>)(<w:p>(?:(?!</w:p>).)*?(?:Palavras-chave:|Keywords:))",
                 junta_chaves, xml, flags=re.S)
    xml = re.sub(r"<w:p>(?:(?!</w:p>).)*?(?:Palavras-chave:|Keywords:)(?:(?!</w:p>).)*</w:p>", chave_esq, xml, flags=re.S)

    # v0.3 (P2b): Resumo e Abstract cabem cada um numa página com as palavras-chave. Só espaçamento
    # ENTRE parágrafos (antes/depois) do parágrafo de abertura e dos itens; a entrelinha do canon não muda.
    def compacta(m: re.Match) -> str:
        seg = m.group(0)
        def zera(pm: re.Match) -> str:
            q = pm.group(0)
            if not re.search(r'w:val="(?:FirstParagraph|Compact)"', q):
                return q
            if "<w:spacing " in q:  # já tem espaçamento: só antes/depois mudam (a entrelinha fica)
                return re.sub(r"<w:spacing [^>]*/>", lambda sp: re.sub(r'\s*w:(?:before|after)="\d+"', "", sp.group(0))
                              .replace("<w:spacing", '<w:spacing w:before="0" w:after="0"', 1), q, count=1)
            # ordem do esquema OOXML no pPr: pStyle, ..., numPr, ..., spacing
            ancora = r"(</w:numPr>)" if "</w:numPr>" in q else r'(<w:pStyle w:val="(?:FirstParagraph|Compact)"\s*/>)'
            return re.sub(ancora, r'\1<w:spacing w:before="0" w:after="0"/>', q, count=1)
        return re.sub(r"<w:p>(?:(?!</w:p>).)*</w:p>", zera, seg, flags=re.S)
    xml = re.sub(r"<w:t[^>]*>(?:Resumo|Abstract)</w:t>.*?(?=<w:p>(?:(?!</w:p>).)*?(?:Palavras-chave:|Keywords:))",
                 compacta, xml, flags=re.S)

    # house pagination: these headings always start a fresh page (pageBreakBefore
    # occupies no height on the previous page — no phantom blank pages)
    for head in heads:
        pat = (r'(<w:p[ >](?:(?!</w:p>).)*?<w:pStyle w:val="Heading\d"\s*/>)'
               r'((?:(?!</w:p>|<w:pageBreakBefore).)*?<w:t[^>]*>' + re.escape(head) + r'</w:t>)')
        xml = re.sub(pat, r'\1<w:pageBreakBefore/>\2', xml, flags=re.S)
        # verificação (idempotente: numa 2ª rodada a substituição não casa, mas a
        # quebra JÁ está lá — o que importa é o estado final, não o nº de trocas)
        done = (r'<w:p[ >](?:(?!</w:p>).)*?<w:pStyle w:val="Heading\d"\s*/>'
                r'(?:(?!</w:p>).)*?<w:pageBreakBefore/>(?:(?!</w:p>).)*?<w:t[^>]*>'
                + re.escape(head) + r'</w:t>')
        if not re.search(done, xml, flags=re.S):
            raise SystemExit(f"[FAIL] heading do canon sem quebra de página no DOCX: {head!r}")

    # fail-closed: nenhum caminho de sistema pode sobreviver no corpo publicado (B1 —
    # o canon deu 53/53 uma vez COM um path vazando no `descr` de uma imagem)
    leak = re.search(r"/(?:Users)/|/home/[^/]+/|[A-Za-z]:\\", xml)
    if leak:
        raise SystemExit("[FAIL] caminho de sistema vazou em document.xml: "
                         + repr(xml[max(0, leak.start() - 40):leak.start() + 60]))
    if anexos:
        tit = re.findall(r'<w:pStyle w:val="Heading\d"\s*/>(?:(?!</w:p>).)*?<w:t[^>]*>(Anexo [A-Z] — [^<]*)</w:t>', xml, flags=re.S)
        if not tit:
            raise SystemExit("[FAIL] DOCX de anexos sem nenhum título 'Anexo X — '")
        for head in tit:
            pat = (r'(<w:p[ >](?:(?!</w:p>).)*?<w:pStyle w:val="Heading\d"\s*/>)'
                   r'((?:(?!</w:p>|<w:pageBreakBefore).)*?<w:t[^>]*>' + re.escape(head) + r'</w:t>)')
            xml = re.sub(pat, r'\1<w:pageBreakBefore/>\2', xml, count=1, flags=re.S)
        heads = tit
    data["word/document.xml"] = xml.encode("utf-8")

    # dedupe styles: the reference-doc template itself defines Bibliography twice —
    # an empty block (no pPr) plus the full one (hanging indent) — and the canon's
    # Bibliography regex matches the FIRST, so the empty one must go (duplicate
    # styleId is invalid and confused one external auditor); keep the def WITH pPr.
    styles = data["word/styles.xml"].decode("utf-8")
    seen: dict[str, str] = {}
    for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>.*?</w:style>', styles, re.S):
        sid, block = m.group(1), m.group(0)
        if sid in seen:
            keep, drop = (block, seen[sid]) if "<w:pPr>" in block else (seen[sid], block)
            styles = styles.replace(drop, "", 1)
            seen[sid] = keep
        else:
            seen[sid] = block
    # proofing language: o reference-doc v2 carimba pt-BR no docDefaults e sublinharia
    # cada palavra inglesa; o canon confere isso (`proofing_lang_must_match_doc`).
    styles = re.sub(r'(<w:lang [^>]*w:val=")[^"]+(")', r"\1" + proofing + r"\2", styles)
    # v0.2: referências alinhadas à esquerda (URL longa abria buracos na linha justificada)
    # v0.3 (P2a): referências em entrelinha simples com 6 pt entre entradas. O canon fixa a entrelinha
    # dupla só do estilo Normal (line 480) e, da Bibliography, só o recuo deslocado (hanging 720), que fica;
    # a lista de 78 entradas ocupava 16 páginas em entrelinha dupla.
    def bib_esq(m: re.Match) -> str:
        b = re.sub(r'<w:jc w:val="[^"]+"\s*/>', "", m.group(0))
        b = re.sub(r'<w:spacing [^>]*/>', '<w:spacing w:after="120" w:line="240" w:lineRule="auto"/>', b)
        return b.replace("</w:pPr>", '<w:jc w:val="left"/></w:pPr>', 1)
    styles = re.sub(r'<w:style [^>]*w:styleId="Bibliography"[^>]*>.*?</w:style>', bib_esq, styles, flags=re.S)
    data["word/styles.xml"] = styles.encode("utf-8")

    if "docProps/core.xml" in data:
        core = data["docProps/core.xml"].decode("utf-8")
        core = re.sub(r"<dc:language>[^<]*</dc:language>",
                      f"<dc:language>{proofing}</dc:language>", core)
        data["docProps/core.xml"] = core.encode("utf-8")

    tmp = Path(tempfile.mkstemp(suffix=".docx")[1])
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, data[n])
    shutil.move(tmp, path)
    print(f"[OK] table grids fixed + page breaks {heads} + proofing lang={proofing}: {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--lang", choices=sorted(PROOFING), default="pt-BR")
    ap.add_argument("--parte", choices=("tudo", "principal", "anexos"), default="tudo")
    a = ap.parse_args()
    fix(Path(a.docx), a.lang, a.parte)
