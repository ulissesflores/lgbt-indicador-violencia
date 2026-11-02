#!/usr/bin/env bash
# Pipeline v0.4 (P4a): paper.md -> DOCX (APA 7, preprint publico) -> PDF GERADO PELO WORD -> crivos.
#
#   tools/build_v04.sh [--src paper.md] [--out build/v04] [--nome paper-v04] [--fig-cm auto|14]
#
# 1. export_v04.py: pandoc SEM reference-doc + pos-processador (Times 12 em tudo, tabelas APA, figuras de
#    largura unica, apendices em pagina nova, numero de pagina no topo a direita);
# 2. Word (AppleScript) exporta o PDF; se passar de 4 MB, recomprime SO as imagens (menos pixels) e repete;
# 3. crivo_docx.py confere o DOCX e o PDF (pdffonts, tabela orfa, paginas a renderizar).
#
# Requisitos: pandoc, qpdf, poppler (pdffonts/pdfinfo/pdftoppm), Microsoft Word, e um Python com lxml e Pillow
# (PyMuPDF para a deteccao de tabela orfa). Padrao: /usr/bin/python3 (3.9), que ja tem os tres. Troque por
# PYTHON_V04=/caminho/python se preciso. O Word NAO e encerrado se ja havia documento aberto (o autor mantem
# trabalho dele no Word): fecha-se so o documento exportado.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON_V04:-/usr/bin/python3}"
SRC="$ROOT/paper.md"; OUT="$ROOT/build/v04"; NOME="paper-v04"; FIG="auto"
while [ $# -gt 0 ]; do
  case "$1" in
    --src) SRC="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift 2;;
    --out) mkdir -p "$2"; OUT="$(cd "$2" && pwd)"; shift 2;;
    --nome) NOME="$2"; shift 2;;
    --fig-cm) FIG="$2"; shift 2;;
    *) echo "uso: $0 [--src md] [--out pasta] [--nome base] [--fig-cm auto|N]"; exit 64;;
  esac
done
case "$OUT" in /private/tmp/*|/tmp/*) echo "[FAIL] saida em /tmp: o Word abre em modo protegido e a regra da casa proibe arvore de projeto la"; exit 65;; esac
mkdir -p "$OUT"
TETO=$((4*1024*1024))
PXS=(${PX_LIST:-850 700 600 500})
DOCX="$OUT/$NOME.docx"; PDF="$OUT/$NOME.pdf"

# O Word (sandbox) pede "Grant File Access" na PRIMEIRA vez que abre um caminho novo; a permissao fica gravada
# para aquele caminho. Por isso o DOCX e copiado SEMPRE para o mesmo arquivo de troca (WORD_IO) e o PDF nasce ao
# lado dele. Primeira vez num caminho novo: o autor clica "Select..." uma vez (o consentimento nao e automatizado).
WORD_IO="${WORD_IO:-$ROOT/build/v04/word-io/entrada-word.docx}"
word_pdf() {  # $1 docx, $2 pdf final  (fora de /private/tmp; so fecha o proprio documento)
  mkdir -p "$(dirname "$WORD_IO")"
  cp "$1" "$WORD_IO"
  local pdf_io="${WORD_IO%.docx}.pdf"
  rm -f "$pdf_io" "$(dirname "$WORD_IO")/~\$$(basename "$WORD_IO")"
  osascript - "$WORD_IO" "$pdf_io" <<'EOF'
on run argv
  set docPath to item 1 of argv
  set pdfPath to item 2 of argv
  set docName to do shell script "basename " & quoted form of docPath
  with timeout of 900 seconds
    tell application "Microsoft Word"
      set n0 to count of documents
      open POSIX file docPath
      set t to 0
      repeat until (exists document docName) or t > 120
        delay 1
        set t to t + 1
      end repeat
      if not (exists document docName) then
        if n0 = 0 then quit saving no
        error "o Word nao abriu " & docName & " em 120 s (provavel 'Grant File Access': aprove o caminho uma vez, ou use WORD_IO=<caminho ja autorizado>)"
      end if
      set d to document docName
      save as d file name pdfPath file format format PDF
      close d saving no
      if n0 = 0 then quit saving no
    end tell
  end timeout
end run
EOF
  mv "$pdf_io" "$2"
}

for PX in "${PXS[@]}"; do
  echo "== exportando DOCX (imagens ${PX}px)"
  "$PY" "$ROOT/tools/export_v04.py" --src "$SRC" --work "$OUT/work" --out "$DOCX" --fig-cm "$FIG" --img-px "$PX"
  echo "== Word -> PDF"
  word_pdf "$DOCX" "$PDF"
  [ -s "$PDF" ] || { echo "[FAIL] o Word nao gerou $PDF"; exit 70; }
  TAM=$(stat -f%z "$PDF")
  echo "   PDF: $TAM bytes ($(pdfinfo "$PDF" | awk '/^Pages:/{print $2}') paginas)"
  [ "$TAM" -le "$TETO" ] && break
  echo "   > 4 MB: recomprimindo so as imagens"
done
[ "$TAM" -le "$TETO" ] || { echo "[FAIL] PDF acima de 4 MB mesmo com imagens a ${PX}px"; exit 71; }
qpdf --check "$PDF" >/dev/null && echo "[OK] qpdf --check"
echo "== crivo"
set +e
"$PY" "$ROOT/tools/crivo_docx.py" "$DOCX" --pdf "$PDF" --render "$OUT/render"
RC=$?
set -e
mkdir -p "$OUT/render" && rm -f "$OUT/render"/p-*.png && pdftoppm -r 100 -png "$PDF" "$OUT/render/p" && echo "== $(ls "$OUT/render"/p-*.png | wc -l) paginas renderizadas em $OUT/render (ler as listadas em paginas-a-ler.txt, no minimo)"
echo "crivo_docx saiu com $RC (0 = limpo; 1 = violacao de FORMA; 2 = so pendencia de CONTEUDO)"
exit $RC
