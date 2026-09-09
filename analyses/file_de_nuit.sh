#!/bin/zsh
# File de calcul, v4 ecrite a 05:02 apres la fin de C3 : C3F (fin 06:20) puis extension C2 (fin 08:30).
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim || exit 1
T=data/traces
log() { print -r -- "$(date '+%H:%M:%S') $*" >> $T/file-de-nuit.log }
attendre_serveur_libre() { while pgrep -f llama-server >/dev/null; do sleep 20; done }
log "file v4 : C3F puis extension C2"
attendre_serveur_libre
log "lancement de a5 --familles (C3F), fin dure 06:20"
.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --familles --fin 06:20 >> $T/a5-familles.log 2>&1
log "C3F termine ou arrete, code $?"
attendre_serveur_libre
log "lancement de l'extension C2 (a21), fin dure 08:30"
.venv/bin/python analyses/a21_extension_c2.py --fin 08:30 >> $T/a5-ext.log 2>&1
log "extension C2 terminee ou arretee, code $?"
log "FILE TERMINEE"
