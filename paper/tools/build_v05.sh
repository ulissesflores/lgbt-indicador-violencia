#!/usr/bin/env bash
# Pipeline v0.5 (norma Codex Hash): fonte unica (artigo + Apendices A a M) -> DOCX -> PDF pelo Word -> crivo,
# e copia para docs/paper/paper-final.{docx,pdf}, o caminho que a norma da casa exige no repositorio.
#
#   tools/build_v05.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON_V04:-/usr/bin/python3}"
"$PY" "$ROOT/tools/monta_fonte_v05.py" --out "$ROOT/build/v05/fonte-v05.md"
set +e
bash "$ROOT/tools/build_v04.sh" --src "$ROOT/build/v05/fonte-v05.md" --out "$ROOT/build/v05" --nome paper-v05
RC=$?
set -e
[ "$RC" -le 2 ] || exit "$RC"
mkdir -p "$ROOT/../docs/paper"
cp "$ROOT/build/v05/paper-v05.docx" "$ROOT/../docs/paper/paper-final.docx"
cp "$ROOT/build/v05/paper-v05.pdf" "$ROOT/../docs/paper/paper-final.pdf"
echo "== copiado para docs/paper/paper-final.{docx,pdf}"
exit "$RC"
