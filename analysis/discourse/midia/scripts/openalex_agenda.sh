#!/bin/zsh
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
#
# Wait for the OpenAlex daily quota reset and then run the counts.
#
# Sleeps until 00:00 UTC, when the keyless OpenAlex quota resets, waits one more minute and then
# runs openalex_contar.py in count mode, appending its output and a closing line to a log.
# REPO_ROOT must be set.
#
# Inputs
# ------
# - environment variable REPO_ROOT (repository root)
# - analysis/discourse/midia/scripts/openalex_contar.py (run in count mode)
#
# Outputs
# -------
# - analysis/discourse/midia/openalex_agenda.log (not tracked in git)
# - the outputs of openalex_contar.py in count mode
#
# Usage
# -----
# REPO_ROOT=$PWD /bin/zsh analysis/discourse/midia/scripts/openalex_agenda.sh
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
# espera o reset da cota sem chave do OpenAlex (00:00 UTC) e roda contagem + uniao + amostra de uma vez
LOG=$REPO_ROOT/analysis/discourse/midia/openalex_agenda.log
cd $REPO_ROOT/analysis/discourse/midia/scripts
while [ "$(date -u +%H)" != "00" ]; do sleep 120; done
sleep 60
python3 -I openalex_contar.py contar >> $LOG 2>&1
echo "FIM $(date -u +%FT%TZ)" >> $LOG
