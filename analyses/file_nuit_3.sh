#!/bin/zsh
# Troisieme file de la nuit du 8 au 9 septembre 2026.
#
# Elle ne lance aucun serveur elle meme et n'en arrete qu'un seul : celui de R2, en
# passant par le processus qui le possede. Sa seule raison d'exister est la contrainte
# machine : un seul llama-server a la fois.
#
#   1. Attendre que R2 (analyses/r2_rares_apparie.py, lance par analyses/file_nuit_2.sh)
#      ait DEMARRE : data/traces/r2-run.pid existe, le PID est vivant, et sa ligne de
#      commande est bien celle de r2_rares_apparie.
#   2. A 05:45 le 9 septembre, envoyer SIGINT a ce PID. r2_rares_apparie ecrit sa trace
#      au fil de l'eau avec flush a chaque ligne et arrete son serveur dans un finally :
#      un KeyboardInterrupt lui coute au plus l'appel en cours, et sa trace est
#      resumable par (condition, pid, item).
#   3. Attendre qu'aucun llama-server ne tourne, dix minutes au plus, puis SIGTERM au
#      serveur restant.
#   4. Lancer R3, analyses/r3_ablation_etiquette.py, fin dure 08:00.
#
# Deux ecarts au script tel qu'il a ete demande, tous deux dans le sens de la prudence,
# et tous deux journalises quand ils se produisent :
#
#   a. si R2 est deja MORT avant 05:45, la file n'attend pas 05:45 pour rien : elle
#      passe a l'etape 3 des qu'elle constate la mort du processus. La contrainte est
#      « un seul serveur », pas « ne rien faire avant 05:45 », et attendre laisserait le
#      GPU vide.
#   b. si l'heure de la fin dure de R3 est deja passee au moment de lancer, R3 n'est PAS
#      lance : heure_de_fin() de a5 basculerait la cible au lendemain et R3 tournerait
#      24 h de trop.
#
# Precautions reprises de file_nuit_2.sh, avec leur raison.
#
# `pgrep -x llama-server` et non `pgrep -f llama-server` : -f compare la ligne de
# commande, et un processus de surveillance dont la ligne contient la chaine
# « llama-server » ferait attendre la file indefiniment. -x compare le nom du processus.
#
# Toutes les gardes horaires sont des epochs calcules AVEC LE JOUR, jamais des chaines
# HHMM comparees entre elles : « 0545 » compare a « 2230 » place minuit du mauvais cote
# et declencherait l'arret de R2 avant qu'il ait commence.
#
# Variables d'environnement, pour l'essai hors ligne seulement :
#   R3_HEURE_ARRET_R2, R3_HEURE_LIMITE_R2, R3_HEURE_FIN, R3_PAS, R3_ESSAI.

cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim || exit 1
T=${R3_TRACES:-data/traces}
PY=.venv/bin/python

HEURE_ARRET_R2=${R3_HEURE_ARRET_R2:-05:45}
HEURE_LIMITE_R2=${R3_HEURE_LIMITE_R2:-04:00}
HEURE_FIN_R3=${R3_HEURE_FIN:-08:00}
PAS=${R3_PAS:-30}
ESSAI=${R3_ESSAI:-0}
# Plafond d'attente d'un GPU libre, en secondes. Dix minutes en production, comme demande.
PLAFOND_SERVEUR=${R3_PLAFOND_SERVEUR:-600}

if [ "$ESSAI" = "1" ]; then
  LOG=$T/file-nuit-3-essai.log
else
  LOG=$T/file-nuit-3.log
fi
mkdir -p $T

log() { print -r -- "$(date '+%Y-%m-%d %H:%M:%S') $*" >> $LOG }

# Prochaine occurrence d'une heure locale, en epoch, AVEC le jour. Rendue par python,
# pour que le passage a minuit soit calcule au meme endroit que dans heure_de_fin() de
# a5, que le script de run appelle.
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

serveurs() { pgrep -x llama-server }

# Le PID de R2 est vivant ET c'est bien R2 ? Un PID seul ne suffit pas : un processus
# mort libere son numero, et le systeme peut le reattribuer. On verifie la ligne de
# commande avant d'envoyer un signal a quoi que ce soit.
r2_vivant() {
  [ -f $T/r2-run.pid ] || return 1
  local pid=$(cat $T/r2-run.pid 2>/dev/null)
  [ -n "$pid" ] || return 1
  kill -0 $pid 2>/dev/null || return 1
  ps -p $pid -o command= 2>/dev/null | grep -q "r2_rares_apparie" || return 1
  return 0
}

pid_r2() { cat $T/r2-run.pid 2>/dev/null }

# ---------------------------------------------------------------------------
read ARRET_TS ARRET_ISO <<< "$(prochaine_occurrence $HEURE_ARRET_R2)"
read LIMITE_TS LIMITE_ISO <<< "$(prochaine_occurrence $HEURE_LIMITE_R2)"
read FIN_TS FIN_ISO <<< "$(prochaine_occurrence $HEURE_FIN_R3)"

log "================================================================"
log "FILE NUIT 3 : depart, PID $$. Horloge machine : $(date '+%Y-%m-%d %H:%M:%S %Z')."
log "R2 sera interrompu a $ARRET_ISO ($ARRET_TS)."
log "si R2 n'a pas demarre a $LIMITE_ISO ($LIMITE_TS), R3 part directement."
log "R3, fin dure $FIN_ISO ($FIN_TS)."
log "page de plan : resultats/r3-preenregistrement.md, horodatee 22:30:01 CEST."
log "aucun serveur n'est lance par cette file ; elle n'arrete que celui de R2."
print -r -- $$ > $T/file-nuit-3.pid

# ---------------------------------------------------------------------------
# 1. Attendre que R2 ait demarre
# ---------------------------------------------------------------------------
R2_VU=0
while :; do
  if r2_vivant; then
    R2_VU=1
    log "R2 a demarre, PID $(pid_r2)"
    break
  fi
  MAINTENANT=$(date +%s)
  if [ "$MAINTENANT" -ge "$LIMITE_TS" ]; then
    log "limite $LIMITE_ISO atteinte sans R2 vivant : R3 partira des que la machine est libre"
    break
  fi
  if [ "$MAINTENANT" -ge "$ARRET_TS" ]; then
    log "l'heure d'arret est deja passee et R2 n'est pas la : on passe a la suite"
    break
  fi
  sleep $PAS
done

# ---------------------------------------------------------------------------
# 2. Attendre 05:45, puis SIGINT ; ou constater la mort de R2 avant l'heure
# ---------------------------------------------------------------------------
if [ "$R2_VU" = "1" ]; then
  while :; do
    MAINTENANT=$(date +%s)
    if ! r2_vivant; then
      log "R2 s'est termine de lui meme avant $ARRET_ISO : aucun signal envoye"
      break
    fi
    if [ "$MAINTENANT" -ge "$ARRET_TS" ]; then
      PID=$(pid_r2)
      log "$ARRET_ISO atteint : SIGINT au PID $PID (KeyboardInterrupt, son finally arrete le serveur, sa trace est resumable)"
      if [ "$ESSAI" = "1" ]; then
        log "MODE ESSAI : aucun signal n'est envoye"
      else
        kill -INT $PID 2>>$LOG
      fi
      break
    fi
    sleep $PAS
  done

  # Laisser R2 finir son arret propre. On ne le tue pas : c'est son finally qui arrete
  # le serveur, et le tuer laisserait le llama-server orphelin.
  ATTENTE=0
  while r2_vivant && [ "$ESSAI" != "1" ]; do
    if [ "$ATTENTE" -ge 300 ]; then
      log "R2 encore vivant 300 s apres le SIGINT, on continue et on regarde le serveur"
      break
    fi
    sleep 10
    ATTENTE=$((ATTENTE + 10))
  done
  log "R2 n'est plus la (ou ne repond plus), attente $ATTENTE s"
fi

# ---------------------------------------------------------------------------
# 3. Attendre qu'aucun llama-server ne tourne, dix minutes au plus
# ---------------------------------------------------------------------------
ATTENTE=0
while serveurs >/dev/null; do
  if [ "$ATTENTE" -ge "$PLAFOND_SERVEUR" ]; then
    RESTANTS=$(serveurs | tr '\n' ' ')
    log "$PLAFOND_SERVEUR s ecoulees, llama-server encore la : $RESTANTS. SIGTERM."
    if [ "$ESSAI" = "1" ]; then
      log "MODE ESSAI : aucun signal n'est envoye"
      break
    fi
    for p in $(serveurs); do kill -TERM $p 2>>$LOG; done
    sleep 20
    if serveurs >/dev/null; then
      log "ATTENTION : un llama-server survit au SIGTERM ($(serveurs | tr '\n' ' ')). R3 refusera de demarrer, et c'est voulu."
    fi
    break
  fi
  log "un llama-server tourne encore ($(serveurs | tr '\n' ' ')), attente 20 s"
  sleep 20
  ATTENTE=$((ATTENTE + 20))
done
log "machine libre au bout de $ATTENTE s d'attente"

# ---------------------------------------------------------------------------
# 4. R3
# ---------------------------------------------------------------------------
MAINTENANT=$(date +%s)
if [ "$MAINTENANT" -ge "$FIN_TS" ]; then
  log "ARRET : $FIN_ISO est deja passe, R3 n'est PAS lance (il tournerait jusqu'au lendemain)"
  log "FILE TERMINEE"
  exit 0
fi

if [ ! -f analyses/r3_ablation_etiquette.py ]; then
  log "ARRET : analyses/r3_ablation_etiquette.py absent"
  log "FILE TERMINEE"
  exit 1
fi

RESTE=$(( (FIN_TS - MAINTENANT) / 60 ))
log "lancement de R3, ablation de l'etiquette, C3E puis C2S puis C3ES, fin dure $HEURE_FIN_R3 ($RESTE min)"

if [ "$ESSAI" = "1" ]; then
  log "MODE ESSAI : la commande n'est pas executee. Elle aurait ete :"
  log "  $PY analyses/r3_ablation_etiquette.py --fin $HEURE_FIN_R3 >> $T/r3-run.log 2>&1"
else
  $PY analyses/r3_ablation_etiquette.py --fin $HEURE_FIN_R3 >> $T/r3-run.log 2>&1
  log "R3 termine ou arrete, code $?"
  if grep -q "RUN TERMINE" $T/r3-run.log 2>/dev/null; then
    log "marqueur RUN TERMINE present dans r3-run.log"
  else
    log "ATTENTION : aucun marqueur RUN TERMINE dans r3-run.log"
  fi
fi

while serveurs >/dev/null && [ "$ESSAI" != "1" ]; do
  log "un llama-server survit a R3 ($(serveurs | tr '\n' ' ')), attente 20 s"
  sleep 20
done
log "FILE TERMINEE"
