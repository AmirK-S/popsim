#!/bin/zsh
# Cinquieme file de la nuit du 8 au 9 septembre 2026 : R4, l'oracle des camps sur le
# modele socle.
#
# Elle ne lance AUCUN serveur elle meme et n'en arrete aucun. Sa seule raison d'exister
# est la contrainte machine : un seul llama-server a la fois. Elle est la derniere de la
# nuit et se place derriere la file 4.
#
#   1. Attendre la fin de la file 4 : la ligne « FILE 4 TERMINEE » dans
#      data/traces/file-nuit-4.log, ou 09:00 heure machine, la premiere des deux.
#   2. Attendre qu'aucun llama-server ne tourne (pgrep -x), dix minutes au plus, puis
#      SIGTERM au serveur restant.
#   3. Lancer R4, analyses/r4_oracle_socle.py, fin dure 10:00.
#   4. Une fois le run fini ou coupe, faire l'evaluation, qui ne demande aucun serveur :
#      r4_oracle_socle.py --evaluer, puis --h4. Ainsi les tableaux du matin existent
#      deja quand Amir se leve, meme si le run a ete tronque.
#
# Trois ecarts au script tel qu'il a ete demande, tous dans le sens de la prudence, tous
# journalises quand ils se produisent.
#
#   a. si l'heure de la fin dure de R4 est deja passee au moment de lancer, R4 n'est PAS
#      lance : heure_de_fin() de a5 basculerait la cible au lendemain et R4 tournerait
#      24 h de trop. L'evaluation, elle, est quand meme faite sur ce qui existe.
#   b. si un llama-server survit au SIGTERM, R4 n'est pas lance : deux serveurs a la fois
#      sont le critere de chute 7 du preenregistrement, et un run jete coute plus cher
#      qu'un run non fait.
#   c. l'evaluation est lancee dans tous les cas, y compris si R4 n'a pas tourne : elle
#      tolere le partiel et le vide, et son echec ne doit pas passer inapercu.
#
# Precautions reprises de file_nuit_2.sh et file_nuit_3.sh, avec leur raison.
#
# `pgrep -x llama-server` et non `pgrep -f llama-server` : -f compare la ligne de
# commande, et un processus de surveillance dont la ligne contient la chaine
# « llama-server » ferait attendre la file indefiniment. -x compare le nom du processus.
#
# Toutes les gardes horaires sont des epochs calcules AVEC LE JOUR, jamais des chaines
# HHMM comparees entre elles : « 0900 » compare a « 2350 » place minuit du mauvais cote
# et ferait partir la file avant que la file 4 ait commence.
#
# Variables d'environnement, pour l'essai hors ligne seulement :
#   R4_HEURE_LIMITE, R4_HEURE_FIN, R4_PAS, R4_ESSAI, R4_TRACES, R4_MARQUEUR,
#   R4_PLAFOND_SERVEUR, R4_MODELE.

cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim || exit 1
T=${R4_TRACES:-data/traces}
PY=.venv/bin/python

# Heure au dela de laquelle on n'attend plus la file 4.
HEURE_LIMITE=${R4_HEURE_LIMITE:-09:00}
# Fin dure du run.
HEURE_FIN=${R4_HEURE_FIN:-10:00}
PAS=${R4_PAS:-60}
ESSAI=${R4_ESSAI:-0}
PLAFOND_SERVEUR=${R4_PLAFOND_SERVEUR:-600}
MODELE=${R4_MODELE:-q4base,q4nogab,q4hyb}
MARQUEUR=${R4_MARQUEUR:-FILE 4 TERMINEE}
JOURNAL_FILE4=$T/file-nuit-4.log

if [ "$ESSAI" = "1" ]; then
  LOG=$T/file-nuit-5-essai.log
else
  LOG=$T/file-nuit-5.log
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

# ---------------------------------------------------------------------------
read LIMITE_TS LIMITE_ISO <<< "$(prochaine_occurrence $HEURE_LIMITE)"
read FIN_TS FIN_ISO <<< "$(prochaine_occurrence $HEURE_FIN)"

log "================================================================"
log "FILE NUIT 5 : depart, PID $$. Horloge machine : $(date '+%Y-%m-%d %H:%M:%S %Z')."
log "attente du marqueur « $MARQUEUR » dans $JOURNAL_FILE4, ou de $LIMITE_ISO ($LIMITE_TS)."
log "R4, fin dure $FIN_ISO ($FIN_TS), modeles $MODELE."
log "page de plan : resultats/r4-preenregistrement.md, horodatee 2026-09-08 23:45 CEST."
log "aucun serveur n'est lance ni arrete par cette file tant que la machine est occupee."
print -r -- $$ > $T/file-nuit-5.pid

# ---------------------------------------------------------------------------
# 1. Attendre la fin de la file 4, ou l'heure limite
# ---------------------------------------------------------------------------
while :; do
  if grep -q "$MARQUEUR" $JOURNAL_FILE4 2>/dev/null; then
    log "marqueur « $MARQUEUR » trouve dans $JOURNAL_FILE4"
    break
  fi
  MAINTENANT=$(date +%s)
  if [ "$MAINTENANT" -ge "$LIMITE_TS" ]; then
    log "$LIMITE_ISO atteint sans marqueur : on passe a la suite"
    break
  fi
  sleep $PAS
done

# ---------------------------------------------------------------------------
# 2. Attendre qu'aucun llama-server ne tourne
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
    break
  fi
  log "un llama-server tourne encore ($(serveurs | tr '\n' ' ')), attente 20 s"
  sleep 20
  ATTENTE=$((ATTENTE + 20))
done

if serveurs >/dev/null && [ "$ESSAI" != "1" ]; then
  log "ARRET : un llama-server survit au SIGTERM ($(serveurs | tr '\n' ' ')). R4 n'est PAS"
  log "lance : deux serveurs a la fois sont le critere de chute 7 du preenregistrement."
  log "FILE 5 TERMINEE"
  exit 1
fi
log "machine libre au bout de $ATTENTE s d'attente"

# ---------------------------------------------------------------------------
# 3. R4
# ---------------------------------------------------------------------------
LANCE=0
MAINTENANT=$(date +%s)
if [ "$MAINTENANT" -ge "$FIN_TS" ]; then
  log "ATTENTION : $FIN_ISO est deja passe, R4 n'est PAS lance (il tournerait jusqu'au lendemain)"
elif [ ! -f analyses/r4_oracle_socle.py ]; then
  log "ATTENTION : analyses/r4_oracle_socle.py absent, R4 n'est PAS lance"
else
  RESTE=$(( (FIN_TS - MAINTENANT) / 60 ))
  log "lancement de R4 : $MODELE, fin dure $HEURE_FIN ($RESTE min)"
  if [ "$ESSAI" = "1" ]; then
    log "MODE ESSAI : la commande n'est pas executee. Elle aurait ete :"
    log "  $PY analyses/r4_oracle_socle.py --modele $MODELE --fin $HEURE_FIN >> $T/r4-run.log 2>&1"
  else
    $PY analyses/r4_oracle_socle.py --modele $MODELE --fin $HEURE_FIN >> $T/r4-run.log 2>&1
    CODE=$?
    LANCE=1
    log "R4 termine ou arrete, code $CODE"
    if grep -q "RUN TERMINE" $T/r4-run.log 2>/dev/null; then
      log "marqueur RUN TERMINE present dans r4-run.log"
    else
      log "ATTENTION : aucun marqueur RUN TERMINE dans r4-run.log"
    fi
  fi
fi

# Le serveur du dernier modele est arrete par le finally du script de run. On verifie.
ATTENTE=0
while serveurs >/dev/null && [ "$ESSAI" != "1" ]; do
  if [ "$ATTENTE" -ge 120 ]; then
    log "ATTENTION : un llama-server survit a R4 ($(serveurs | tr '\n' ' ')). SIGTERM."
    for p in $(serveurs); do kill -TERM $p 2>>$LOG; done
    sleep 15
    break
  fi
  log "un llama-server survit a R4, attente 20 s"
  sleep 20
  ATTENTE=$((ATTENTE + 20))
done

# ---------------------------------------------------------------------------
# 4. L'evaluation, qui ne demande aucun serveur
# ---------------------------------------------------------------------------
log "evaluation : r4_oracle_socle.py --evaluer (r1_evaluer.py --suffixe r4, sans modification)"
if [ "$ESSAI" = "1" ]; then
  log "MODE ESSAI : les commandes d'evaluation ne sont pas executees. Elles auraient ete :"
  log "  $PY analyses/r4_oracle_socle.py --evaluer >> $T/r4-evaluation.log 2>&1"
  log "  $PY analyses/r4_oracle_socle.py --h4      >> $T/r4-evaluation.log 2>&1"
else
  $PY analyses/r4_oracle_socle.py --evaluer >> $T/r4-evaluation.log 2>&1
  log "evaluation terminee, code $?"
  $PY analyses/r4_oracle_socle.py --h4 >> $T/r4-evaluation.log 2>&1
  log "H4 terminee, code $?"
fi

log "FILE 5 TERMINEE"
