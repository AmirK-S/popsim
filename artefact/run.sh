#!/usr/bin/env bash
# run.sh : une seule commande qui enchaine generation -> attaque -> defense -> tableau final,
# entierement sur des donnees FICTIVES (voir README.md). Duree attendue : moins d'une minute
# sur un portable.
set -euo pipefail

ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RACINE_REPO="$(dirname "$ICI")"

if [ -x "$RACINE_REPO/.venv/bin/python" ]; then
  PY="$RACINE_REPO/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
else
  echo "Aucun interpreteur Python trouve (.venv/bin/python ou python3)." >&2
  exit 1
fi

echo "interpreteur : $PY ($($PY --version 2>&1))"
echo

echo "=== 1/4 generation du jeu de donnees fictif ==="
"$PY" "$ICI/generer_donnees.py"
echo

echo "=== 2/4 attaque de reidentification (importee de analyses/c7_reidentification.py) ==="
"$PY" "$ICI/attaque.py"
echo

echo "=== 3/4 defense D4, melange intra-segment (importee de analyses/c7_defense.py) ==="
"$PY" "$ICI/defense.py"
echo

echo "=== 4/4 tableau final ==="
"$PY" "$ICI/tableau_final.py"
