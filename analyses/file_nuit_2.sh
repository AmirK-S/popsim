#!/bin/zsh
# File de calcul de la nuit du 8 au 9 septembre 2026, seconde file.
#
#   1. R1, l'oracle des camps (analyses/r1_oracle_camps.py), trois modeles l'un apres
#      l'autre, un seul llama-server a la fois, fin dure a 02:30.
#   2. R2, la comparaison appariee sur les gens rares (analyses/r2_rares_apparie.py),
#      preparee par un autre agent, lancee seulement quand R1 est fini ET que le fichier
#      temoin data/traces/r2-pret existe. Attente de ce temoin plafonnee a 01:30.
#
# Deux precautions qui ont une raison.
#
# `pgrep -x llama-server` et non `pgrep -f llama-server` : un processus de surveillance
# tourne cette nuit dont la ligne de commande CONTIENT la chaine « llama-server ». Avec
# `-f` l'attente ne se terminerait jamais. `-x` compare le nom du processus, pas sa ligne
# de commande.
#
# Toutes les gardes horaires sont des epochs calcules avec le jour, jamais des chaines
# HHMM comparees entre elles : une comparaison de « 0130 » a « 2230 » place minuit du
# mauvais cote et arrete la file avant qu'elle ait commence.

cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim || exit 1
T=data/traces
PY=.venv/bin/python

log() { print -r -- "$(date '+%Y-%m-%d %H:%M:%S') $*" >> $T/file-nuit-2.log }

attendre_serveur_libre() {
  while pgrep -x llama-server >/dev/null; do
    log "un llama-server tourne deja, attente 20 s"
    sleep 20
  done
}

# Prochaine occurrence d'une heure locale, en epoch, avec le jour. Rendue par python pour
# que le calcul du passage a minuit soit fait une fois et au meme endroit que dans le
# script de run.
prochaine_occurrence() {
  $PY - "$1" <<'PYEOF'
import datetime, sys
h, m = (int(v) for v in sys.argv[1].split(":"))
maintenant = datetime.datetime.now()
cible = maintenant.replace(hour=h, minute=m, second=0, microsecond=0)
if cible <= maintenant:
    cible += datetime.timedelta(days=1)
print(f"{int(cible.timestamp())} {cible:%Y-%m-%d %H:%M:%S}")
PYEOF
}

FIN_R1="02:30"
FIN_R2="08:00"
LIMITE_ATTENTE_R2="01:30"

read LIMITE_TS LIMITE_ISO <<< "$(prochaine_occurrence $LIMITE_ATTENTE_R2)"
read FIN_R1_TS FIN_R1_ISO <<< "$(prochaine_occurrence $FIN_R1)"
read FIN_R2_TS FIN_R2_ISO <<< "$(prochaine_occurrence $FIN_R2)"

log "FILE NUIT 2 : depart. R1 fin dure $FIN_R1_ISO ($FIN_R1_TS)."
log "attente du temoin $T/r2-pret plafonnee a $LIMITE_ISO ($LIMITE_TS) ; R2 fin dure $FIN_R2_ISO ($FIN_R2_TS)."

# ---------------------------------------------------------------------------
# 1. R1
# ---------------------------------------------------------------------------
attendre_serveur_libre
log "lancement de R1, oracle des camps, modeles q4 puis oss20 puis q30"
$PY analyses/r1_oracle_camps.py --modele q4,oss20,q30 --fin $FIN_R1 >> $T/r1-run.log 2>&1
CODE_R1=$?
log "R1 termine ou arrete, code $CODE_R1"

if grep -q "RUN TERMINE" $T/r1-run.log 2>/dev/null; then
  log "marqueur RUN TERMINE present dans r1-run.log"
else
  log "ATTENTION : aucun marqueur RUN TERMINE dans r1-run.log"
fi

# Le run arrete son serveur dans un finally, mais on verifie : R2 ne doit jamais demarrer
# a cote d'un serveur survivant.
attendre_serveur_libre

# ---------------------------------------------------------------------------
# 2. Attente du temoin de R2, puis R2
# ---------------------------------------------------------------------------
while [ ! -f $T/r2-pret ]; do
  MAINTENANT=$(date +%s)
  if [ "$MAINTENANT" -ge "$LIMITE_TS" ]; then
    log "limite $LIMITE_ISO atteinte sans temoin r2-pret, R2 n'est pas lance"
    break
  fi
  sleep 60
done

if [ -f $T/r2-pret ]; then
  if [ -f analyses/r2_rares_apparie.py ]; then
    attendre_serveur_libre
    log "temoin r2-pret trouve, lancement de R2, fin dure $FIN_R2_ISO"
    $PY analyses/r2_rares_apparie.py --fin $FIN_R2 >> $T/r2-run.log 2>&1
    log "R2 termine ou arrete, code $?"
  else
    log "ATTENTION : temoin r2-pret present mais analyses/r2_rares_apparie.py absent"
  fi
fi

attendre_serveur_libre
log "FILE TERMINEE"
