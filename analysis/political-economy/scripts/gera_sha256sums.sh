#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
#
# Write the SHA-256 checksum list of the political-economy folder.
#
# Changes into the political-economy analysis folder and writes SHA256SUMS.txt with the hashes
# (relative paths, sorted) of the README, the source ledger, the acquisition queue, the scripts
# and the data files, skipping zip archives, .DS_Store and Python caches. It then appends the
# hashes of the budget zip archives found in data/raw/orcamento (relative to that folder) and
# prints the line count.
#
# Inputs
# ------
# - analysis/political-economy/README.md, sources.jsonl, fila-aquisicao.jsonl, scripts/ and dados/
# - data/raw/orcamento/*.zip relative to analysis/political-economy (budget archives)
#
# Outputs
# -------
# - analysis/political-economy/SHA256SUMS.txt
# - prints the number of lines to stdout
#
# Usage
# -----
# bash analysis/political-economy/scripts/gera_sha256sums.sh
#
# Status
# ------
# No registration status is claimed for this file.
#
# Author
# ------
# Carlos Ulisses Flores (Codex Hash Research Laboratory),
# ORCID https://orcid.org/0000-0002-6034-7765.
# Repository: https://github.com/ulissesflores/lgbt-indicador-violencia

# Gera SHA256SUMS.txt na raiz da pasta F5 (caminhos relativos). Rodar: bash scripts/gera_sha256sums.sh
cd "$(dirname "$0")/.." || exit 1
find README.md sources.jsonl fila-aquisicao.jsonl scripts dados -type f ! -name '*.zip' ! -name '.DS_Store' ! -name '*.pyc' -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS.txt
(cd data/raw/orcamento && shasum -a 256 *.zip) | sed 's#  #  data/raw/orcamento/#' >> SHA256SUMS.txt
wc -l SHA256SUMS.txt
