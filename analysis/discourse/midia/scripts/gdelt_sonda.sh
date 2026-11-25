#!/bin/zsh
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
#
# Probe the GDELT API slowly until it answers with a useful body.
#
# Sends one request every 5 minutes to the public GDELT DOC 2.0 API, appends the UTC time, the
# HTTP status code and the first bytes of the body to a log, and stops at the first 200 answer
# with a useful body (it then writes the word ABERTO to the log). REPO_ROOT must be set.
#
# Inputs
# ------
# - https://api.gdeltproject.org/api/v2/doc/doc (network access, through curl)
# - environment variable REPO_ROOT (repository root)
#
# Outputs
# -------
# - analysis/discourse/midia/gdelt_sonda.log (not tracked in git)
#
# Usage
# -----
# REPO_ROOT=$PWD /bin/zsh analysis/discourse/midia/scripts/gdelt_sonda.sh
#
# Status
# ------
# Data acquisition step; no analysis claim.
#
# Author
# ------
# Carlos Ulisses Flores (Codex Hash Research Laboratory),
# ORCID https://orcid.org/0000-0002-6034-7765.
# Repository: https://github.com/ulissesflores/lgbt-indicador-violencia

: "${REPO_ROOT:?defina REPO_ROOT (raiz do repositório)}"
# sonda lenta do GDELT (1 pedido a cada 5 min), grava hora+codigo+tamanho em gdelt_sonda.log; para ao primeiro 200 com corpo util
LOG=$REPO_ROOT/analysis/discourse/midia/gdelt_sonda.log
while true; do
  R=$(curl -s -m 60 -w "\n%{http_code}" 'https://api.gdeltproject.org/api/v2/doc/doc?query=homophobia&mode=timelinevolraw&format=json&timespan=1m')
  C=$(echo "$R" | tail -1); B=$(echo "$R" | head -c 80 | tr '\n' ' ')
  echo "$(date -u +%FT%TZ) $C $B" >> $LOG
  if [ "$C" = "200" ] && [ "${#B}" -gt 10 ] && [[ "$B" != *"Please limit"* ]]; then echo ABERTO >> $LOG; exit 0; fi
  sleep 300
done
