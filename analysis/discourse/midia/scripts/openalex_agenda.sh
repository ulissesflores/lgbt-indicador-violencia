#!/bin/zsh
: "${REPO_ROOT:?defina REPO_ROOT (raiz do repositório)}"
# espera o reset da cota sem chave do OpenAlex (00:00 UTC) e roda contagem + uniao + amostra de uma vez
LOG=$REPO_ROOT/analysis/discourse/midia/openalex_agenda.log
cd $REPO_ROOT/analysis/discourse/midia/scripts
while [ "$(date -u +%H)" != "00" ]; do sleep 120; done
sleep 60
/opt/homebrew/bin/python3.14 -I openalex_contar.py contar >> $LOG 2>&1
echo "FIM $(date -u +%FT%TZ)" >> $LOG
