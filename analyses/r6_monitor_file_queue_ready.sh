#!/usr/bin/env bash
# Moniteur passif: lit seulement PID, STOP-R6 et l'état du lanceur qu'il ne contrôle pas.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PID_FILE="data/traces/reprise/r6-campagnes-queue-ready-20260911.pid"
STATUS="data/traces/reprise/r6-campagnes-queue-ready-20260911.status"
MONITOR="data/traces/reprise/r6-campagnes-queue-ready-20260911.monitor"

timestamp() { date '+%Y-%m-%dT%H:%M:%S%z'; }
if [[ ! -r "$PID_FILE" ]]; then
  printf 'timestamp=%s\nstate=NO_PID\n' "$(timestamp)" > "$MONITOR"
  exit 0
fi
runner_pid="$(tr -d '[:space:]' < "$PID_FILE")"
while kill -0 "$runner_pid" 2>/dev/null; do
  stop_r6=false
  [[ -e data/traces/STOP-R6 ]] && stop_r6=true
  printf 'timestamp=%s\nstate=RUNNING\nrunner_pid=%s\nstop_r6=%s\n' \
    "$(timestamp)" "$runner_pid" "$stop_r6" > "$MONITOR"
  sleep 60
done
printf 'timestamp=%s\nstate=RUNNER_NOT_ALIVE\nrunner_pid=%s\n' \
  "$(timestamp)" "$runner_pid" > "$MONITOR"
