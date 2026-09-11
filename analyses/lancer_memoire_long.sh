#!/usr/bin/env bash
# Lancement differe de memoire_long_gss.py. Attend la fin du PID de l'etude C5 en cours
# (78162, c5_formulation.py) pour ne jamais faire tourner deux llama.cpp en meme temps sur
# une machine a memoire limitee, fait un micro-test de parse (10 appels), n'enchaine sur
# le run complet QUE si au moins 90 % des appels du micro-test sont parses, puis lance le
# run complet avec une fin dure de securite.
#
# Usage :
#   nohup analyses/lancer_memoire_long.sh > data/traces/memoire-long/lancement-nohup.log 2>&1 &
#   caffeinate -i -w <pid du nohup ci-dessus>
#
# N'ecrit ni ne lit aucun fichier STOP global : un `touch data/traces/memoire-long/STOP`
# arrete le run complet proprement (voir memoire_long_gss.py), mais n'arrete pas ce
# wrapper avant le lancement, qui n'a pas d'appel de modele a interrompre.

set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PID_A_ATTENDRE="${1:-78162}"
MODELE="${MEMOIRE_LONG_MODELE:-oss20}"
T=data/traces/memoire-long
mkdir -p "$T"
LOG="$T/lancement.log"
RESUME_SMOKE="$T/ml-resume-smoke.json"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { printf '%s %s\n' "$(timestamp)" "$*" >> "$LOG"; }

log "WRAPPER DEMARRE pid=$$ modele=$MODELE attente_pid=$PID_A_ATTENDRE"

# 1. Attente active de la fin du run C5 en cours. Contrainte du depot : deux llama.cpp en
#    meme temps saturent la RAM et font echouer les deux runs.
while kill -0 "$PID_A_ATTENDRE" 2>/dev/null; do
  sleep 60
done
log "PID $PID_A_ATTENDRE termine (ou deja absent), verification memoire avant micro-test"
vm_stat >> "$LOG" 2>&1

# 2. Micro-test de parse : 10 appels, modele leger d'abord verifie present. Fin dure
#    courte (20 min) pour ne jamais bloquer sur un micro-test qui derape.
FIN_SMOKE="$(date -v+20M '+%H:%M' 2>/dev/null || date -d '+20 minutes' '+%H:%M')"
log "lancement du micro-test de parse (10 appels, modele=$MODELE, fin dure $FIN_SMOKE)"
.venv/bin/python analyses/memoire_long_gss.py --modele "$MODELE" --personnes 3 --items 2 \
    --suffixe smoke --limite 10 --fin "$FIN_SMOKE" >> "$LOG" 2>&1
CODE_SMOKE=$?
log "micro-test termine, code=$CODE_SMOKE"

if [[ ! -f "$RESUME_SMOKE" ]]; then
  log "ARRET : pas de resume de micro-test ($RESUME_SMOKE absent), run complet NON lance"
  exit 1
fi

TAUX_REJET=$(.venv/bin/python -c "
import json
d = json.load(open('$RESUME_SMOKE'))
print(d['resultat']['taux_rejet'])
" 2>>"$LOG")
if [[ -z "$TAUX_REJET" ]]; then
  log "ARRET : impossible de lire le taux de rejet du micro-test, run complet NON lance"
  exit 1
fi
log "taux de rejet du micro-test : $TAUX_REJET (seuil d'arret : > 0.10, soit < 90 % de parse)"

SEUIL_OK=$(.venv/bin/python -c "print(1 if $TAUX_REJET <= 0.10 else 0)")
if [[ "$SEUIL_OK" != "1" ]]; then
  log "ARRET : taux de rejet $TAUX_REJET > 0.10 (moins de 90 % de parse), run complet NON lance"
  exit 1
fi
log "micro-test OK (>= 90 % de parse), lancement du run complet"

# 3. Run complet. Fin dure genereuse : ~16 000 appels attendus (402 personnes x 20 items
#    x 2 horizons), estimation 2h30 a 4h a partir du debit mesure ailleurs sur ce depot
#    pour des profils comparables (voir data/traces/memoire-long/LANCEMENT.txt) ; 8 heures
#    laisse une marge large sans risquer de tourner jusqu'au reveil de l'utilisateur.
FIN_COMPLET="$(date -v+8H '+%H:%M' 2>/dev/null || date -d '+8 hours' '+%H:%M')"
log "lancement du run complet (modele=$MODELE, fin dure $FIN_COMPLET)"
.venv/bin/python analyses/memoire_long_gss.py --modele "$MODELE" --fin "$FIN_COMPLET" \
    >> "$LOG" 2>&1
CODE_COMPLET=$?
log "run complet termine, code=$CODE_COMPLET"
log "WRAPPER TERMINE"
