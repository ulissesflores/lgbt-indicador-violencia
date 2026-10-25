#!/bin/bash
# Gera SHA256SUMS.txt na raiz da pasta F5 (caminhos relativos). Rodar: bash scripts/gera_sha256sums.sh
cd "$(dirname "$0")/.." || exit 1
find README.md sources.jsonl fila-aquisicao.jsonl scripts dados -type f ! -name '*.zip' ! -name '.DS_Store' ! -name '*.pyc' -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS.txt
(cd dados/raw/orcamento && shasum -a 256 *.zip) | sed 's#  #  dados/raw/orcamento/#' >> SHA256SUMS.txt
wc -l SHA256SUMS.txt
