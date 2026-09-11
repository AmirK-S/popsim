#!/usr/bin/env bash
# Lance la file R6 READY dans l'ordre scellé. Ne crée ni GO ni STOP.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
QUEUE="data/traces/reprise/R6-campagnes-QUEUE_READY-20260910.json"
QUEUE_SHA="115e1b2e15b115f5926c70d47bef8a45ac46fb65315ec9f2bf7b014d14eb36e4"
LOG="data/traces/reprise/r6-campagnes-queue-ready-20260911.log"
PID_FILE="data/traces/reprise/r6-campagnes-queue-ready-20260911.pid"
STATUS="data/traces/reprise/r6-campagnes-queue-ready-20260911.status"

# Amendement 429 optionnel : R6_AMENDEMENT_429 et R6_AMENDEMENT_429_SHA256 sont transmis
# tels quels au runner, qui refuse une paire incomplete ou non scellee. Sans elles, la
# commande est inchangee. Compatible bash 3.2 (tableau vide sous set -u).
AMENDEMENT_ARGS=()
if [[ -n "${R6_AMENDEMENT_429:-}" ]]; then
  AMENDEMENT_ARGS+=(--amendement-429 "$R6_AMENDEMENT_429")
fi
if [[ -n "${R6_AMENDEMENT_429_SHA256:-}" ]]; then
  AMENDEMENT_ARGS+=(--amendement-429-sha256 "$R6_AMENDEMENT_429_SHA256")
fi

timestamp() { date '+%Y-%m-%dT%H:%M:%S%z'; }
write_status() {
  printf 'timestamp=%s\nstate=%s\nmodel=%s\npid=%s\n' \
    "$(timestamp)" "$1" "$2" "$$" > "$STATUS"
}
log() { printf '%s %s\n' "$(timestamp)" "$*" >> "$LOG"; }

printf '%s\n' "$$" > "$PID_FILE"
log "START queue_sha=$QUEUE_SHA pid=$$"
write_status "STARTED" ""

run_model() {
  local model="$1"
  local go="$2"
  write_status "RUNNING" "$model"
  log "MODEL_START model=$model go=$go"
  if PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_runner_campagnes.py \
      --file "$QUEUE" --file-sha256 "$QUEUE_SHA" --modele "$model" --go "$go" \
      ${AMENDEMENT_ARGS[@]+"${AMENDEMENT_ARGS[@]}"} >> "$LOG" 2>&1; then
    log "MODEL_DONE model=$model"
    return 0
  else
    local rc=$?
    log "MODEL_STOP model=$model exit=$rc"
    write_status "STOPPED" "$model"
    return "$rc"
  fi
}

run_model "deepseek/deepseek-v4-flash" "data/traces/GO-R6-campagne-deepseek-deepseek-v4-flash.json" || exit $?
run_model "mistralai/mistral-small-2603" "data/traces/GO-R6-campagne-mistralai-mistral-small-2603.json" || exit $?
run_model "qwen/qwen3.7-plus" "data/traces/GO-R6-campagne-qwen-qwen3.7-plus.json" || exit $?
run_model "z-ai/glm-5" "data/traces/GO-R6-campagne-z-ai-glm-5.json" || exit $?
run_model "anthropic/claude-haiku-4.5" "data/traces/GO-R6-campagne-anthropic-claude-haiku-4.5.json" || exit $?
run_model "x-ai/grok-4.3" "data/traces/GO-R6-campagne-x-ai-grok-4.3.json" || exit $?

log "QUEUE_DONE"
write_status "DONE" ""
