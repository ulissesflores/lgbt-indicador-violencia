#!/bin/zsh
: "${REPO_ROOT:?defina REPO_ROOT (raiz do repositório)}"
# sonda lenta do GDELT (1 pedido a cada 5 min), grava hora+codigo+tamanho em gdelt_sonda.log; para ao primeiro 200 com corpo util
LOG=$REPO_ROOT/research-2026-10-21-rodada3/discurso/midia/gdelt_sonda.log
while true; do
  R=$(curl -s -m 60 -w "\n%{http_code}" 'https://api.gdeltproject.org/api/v2/doc/doc?query=homophobia&mode=timelinevolraw&format=json&timespan=1m')
  C=$(echo "$R" | tail -1); B=$(echo "$R" | head -c 80 | tr '\n' ' ')
  echo "$(date -u +%FT%TZ) $C $B" >> $LOG
  if [ "$C" = "200" ] && [ "${#B}" -gt 10 ] && [[ "$B" != *"Please limit"* ]]; then echo ABERTO >> $LOG; exit 0; fi
  sleep 300
done
