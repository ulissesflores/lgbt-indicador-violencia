#!/usr/bin/env bash
# LEGADO (v0.3): pipeline de DOIS PDFs pelo LibreOffice, com o título antigo do artigo. NÃO constrói a v0.4:
# o artigo vigente (um PDF, gerado pelo Word) sai de tools/build_v04.sh. Mantido só como registro de como a v0.3 foi
# construída; nenhuma ferramenta da v0.4 o chama (tools/juiz_rubrica.py deixou de chamá-lo na v0.4.1).
# DOCX + PDF de publicacao a partir de paper.md (pipeline da casa, CODEX-HASH-STYLE.md §4):
# canonico -> fonte de publicacao (make_export.py) -> pandoc com reference-doc v2 ->
# fix_docx_tables (grade de tabela, paginacao do canon, idioma de revisao) -> PDF pelo
# LibreOffice -> qpdf --check e limite de 4 MB. Adaptado do build_export.sh do exemplar
# um artigo anterior do laboratório (repositório privado).
# FERRAMENTA DO AUTOR (não reproduzível só com este repositório): exige o modelo DOCX da casa (CODEX_HASH_REFERENCE_DOCX), o canon
# (CODEX_HASH_CANON), pandoc, LibreOffice e qpdf. O PDF e o DOCX distribuídos em build/ são os gerados pelo autor.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="${CODEX_HASH_REFERENCE_DOCX:?defina CODEX_HASH_REFERENCE_DOCX (modelo DOCX da casa, não distribuído)}"
PY="${PYTHON:-python3}"
mkdir -p "$ROOT/build"
TITULO="Gays morrem mais no Brasil? Ninguém sabe! Passei 14 dias, 829 fontes em 10 idiomas, 139 scripts e 4 revisores hostis atrás da resposta"
# v0.3 (P2a): o MESMO paper.md gera dois PDFs, separados pelo marcador <!-- parte:anexos -->:
# build/paper.pdf (artigo principal) e build/anexos.pdf (Anexos A a F). Largura das figuras embutidas
# por parte (cada PDF tem cerca de metade das 28 figuras): LARGURA_PRINCIPAL / LARGURA_ANEXOS.
LARGURA_PRINCIPAL="${LARGURA_PRINCIPAL:-1200}"
LARGURA_ANEXOS="${LARGURA_ANEXOS:-1200}"
cd "$ROOT"
monta() {  # $1 = parte (principal|anexos), $2 = nome base da saída, $3 = largura das figuras
  local parte="$1" base="$2" larg="$3" export
  export="build/$([ "$parte" = anexos ] && echo anexos || echo paper)-export.md"
  $PY -I "$ROOT/tools/make_export.py" --lang pt-BR --parte "$parte"
  $PY -I "$ROOT/tools/embed_figs.py" "$export" --largura "$larg"
  pandoc "$export" \
    -f 'markdown-tex_math_dollars-implicit_figures' \
    -M lang=pt-BR \
    --resource-path="$ROOT" \
    --reference-doc="$TEMPLATE" \
    -o "build/$base.docx"
  $PY -I "$ROOT/tools/fix_docx_tables.py" "build/$base.docx" --lang pt-BR --parte "$parte"
  $PY -I "$ROOT/tools/set_core_props.py" "build/$base.docx" "$TITULO" "Carlos Ulisses Flores"
  ( cd build && soffice --headless --convert-to 'pdf:writer_pdf_Export:{"Quality":{"type":"long","value":"75"}}' "$base.docx" >/dev/null 2>&1 )
  qpdf --check "build/$base.pdf" >/dev/null && echo "[OK] qpdf --check build/$base.pdf"
  local size
  size=$(stat -f%z "build/$base.pdf")
  [ "$size" -le $((4*1024*1024)) ] || { echo "[FAIL] build/$base.pdf > 4 MB ($size)"; exit 1; }
  echo "[OK] build/$base.docx; build/$base.pdf ($size bytes)"
}
monta principal paper "$LARGURA_PRINCIPAL"
monta anexos anexos "$LARGURA_ANEXOS"
