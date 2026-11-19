#!/bin/bash
# essay-b2a-hotfire wrapper: load the fleet token from the Hermes env file, then
# exec the hot-fire watcher (no LLM turn in the transmit path).
set -u
export FLEET_FAST_TOKEN="$(grep -m1 '^FLEET_FAST_TOKEN=' "$HOME/.hermes/.env" | cut -d= -f2- | tr -d '\"' | tr -d "'")"
if [ -z "${FLEET_FAST_TOKEN:-}" ]; then
  echo "FATAL: FLEET_FAST_TOKEN not found in $HOME/.hermes/.env" >&2
  exit 1
fi
exec python3 "$HOME/fleet/evidence/essay_drill_20261118/essay_b2a_hotfire.py" --watch
