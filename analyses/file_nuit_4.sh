#!/bin/zsh
# File 4 : le run « composition des camps » (a46, 120 appels, environ 10 min) apres R3.
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim || exit 1
T=data/traces
log() { print -r -- "$(date '+%Y-%m-%d %H:%M:%S') $*" >> $T/file-nuit-4.log }
LIM=$(date -j -f "%Y-%m-%d %H:%M" "2026-09-09 08:05" +%s)
log "file 4 : attente de la fin de R3 (RUN TERMINE dans r3-run.log) ou de 08:05 (epoch $LIM)"
while true; do
  if grep -q "RUN TERMINE" $T/r3-run.log 2>/dev/null; then log "R3 termine"; break; fi
  if [[ $(date +%s) -ge $LIM ]]; then log "08:05 atteint"; break; fi
  sleep 120
done
n=0; while pgrep -x llama-server >/dev/null; do sleep 20; n=$((n+1)); if [[ $n -ge 30 ]]; then log "un serveur tourne encore apres 10 min, SIGTERM"; pkill -x llama-server; sleep 15; fi; done
log "lancement du run composition, modeles q4,oss20,q30, fin dure 08:50"
.venv/bin/python analyses/a46_run_composition.py --modele q4,oss20,q30 --fin 08:50 >> $T/a46-composition-run.log 2>&1
log "run composition termine ou arrete, code $?"
log "FILE 4 TERMINEE"
