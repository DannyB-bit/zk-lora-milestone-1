#!/usr/bin/env bash
# init.sh — fleet harness startup gate for zk-lora-milestone-1 (Bravo edge node).
# Runs the checks an agent must pass BEFORE touching a cycle. Exits 0 only when
# the environment is healthy. No network writes, no chain writes, no radio TX.
set -uo pipefail
cd "$(dirname "$0")"

FAIL=0
pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1"; FAIL=1; }
warn() { echo "  [WARN] $1"; }

echo "=== Harness Initialization — zk-lora-milestone-1 ==="
echo "repo:    $(pwd)"
echo "branch:  $(git branch --show-current 2>/dev/null || echo '?')"
echo "commit:  $(git rev-parse --short HEAD 2>/dev/null || echo '?')"
echo

echo "--- Subsystem 1: Runtime ---"
if command -v python3 >/dev/null 2>&1; then
  pass "python3 $(python3 --version 2>&1 | awk '{print $2}')"
else
  fail "python3 not found"
fi
if python3 -c "import cryptography" 2>/dev/null; then
  pass "cryptography $(python3 -c 'import cryptography;print(cryptography.__version__)') importable"
else
  fail "cryptography missing — pip install -r requirements.txt"
fi

echo
echo "--- Subsystem 2: State artifacts ---"
for f in AGENTS.md PROGRESS.md cycle_registry.json requirements.txt; do
  [ -f "$f" ] && pass "$f present" || fail "$f missing"
done
[ -f PROGRESS.md ] && grep -q '^## Current State' PROGRESS.md \
  && pass "PROGRESS.md has Current State block" \
  || fail "PROGRESS.md missing '## Current State' block"

echo
echo "--- Subsystem 3: Verification (L1 static) ---"
python3 -m compileall -q tools/ >/dev/null 2>&1 && pass "compileall tools/" || fail "compileall tools/ failed"
if python3 tools/test_b_rx_extract.py >/tmp/.h_b_rx.log 2>&1; then
  pass "test_b_rx_extract.py -> $(grep -o 'UNIT TEST: PASS' /tmp/.h_b_rx.log | tail -1)"
else
  fail "test_b_rx_extract.py failed (see /tmp/.h_b_rx.log)"
fi
if python3 tools/test_t12_battery_template.py >/tmp/.h_t12.log 2>&1; then
  pass "test_t12_battery_template.py -> $(grep -o 'T12 EXIT-CONTRACT UNIT TEST: PASS' /tmp/.h_t12.log | tail -1)"
else
  fail "test_t12_battery_template.py failed (see /tmp/.h_t12.log)"
fi

echo
echo "--- Subsystem 4: Evidence integrity (latest merged cycle) ---"
LATEST="$(ls -d evidence/groth16_ota_*_cycle1?? 2>/dev/null | sort | tail -1)"
if [ -n "${LATEST:-}" ]; then
  echo "  latest evidence dir: $LATEST"
  if [ -f "$LATEST/chain_readback.json" ]; then
    V="$(python3 -c "import json;print(json.load(open('$LATEST/chain_readback.json')).get('verdict','UNKNOWN'))" 2>/dev/null)"
    case "$V" in PASS*) pass "chain_readback verdict: $V" ;; *) fail "chain_readback verdict: $V" ;; esac
  else
    warn "$LATEST has no chain_readback.json"
  fi
  if [ -f "$LATEST/SHA256SUMS" ]; then
    (cd "$LATEST" && sha256sum -c SHA256SUMS >/tmp/.h_sha.log 2>&1) && pass "SHA256SUMS verify" || fail "SHA256SUMS verify failed (see /tmp/.h_sha.log)"
  fi
else
  warn "no evidence/groth16_ota_*_cycle* dir found"
fi

echo
echo "--- Subsystem 5: Fleet bus + chain access (read-only) ---"
if [ -f "$HOME/.hermes/.env" ]; then
  # shellcheck disable=SC1090
  set -a; . "$HOME/.hermes/.env"; set +a
  TOKEN="${FLEET_FAST_TOKEN:-}"
  if [ -n "$TOKEN" ]; then
    CODE="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:8643/health?token=$TOKEN" 2>/dev/null)"
    case "$CODE" in 200) pass "bravo bus 127.0.0.1:8643 healthy" ;; *) warn "bravo bus health -> HTTP $CODE" ;; esac
    CODE2="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://192.168.1.219:8643/health?token=$TOKEN" 2>/dev/null)"
    case "$CODE2" in 200) pass "alpha bus 192.168.1.219:8643 healthy" ;; *) warn "alpha bus health -> HTTP $CODE2 (twin may be offline)" ;; esac
  else
    warn "FLEET_FAST_TOKEN not set — skipping bus checks"
  fi
else
  warn "$HOME/.hermes/.env not found — skipping bus checks"
fi
if command -v solana >/dev/null 2>&1; then
  pass "solana CLI $(solana --version 2>/dev/null | head -1)"
else
  warn "solana CLI not on PATH (settle/readback scripts resolve it themselves)"
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "=== Verification Complete — harness healthy ==="
  echo "Next: read PROGRESS.md and cycle_registry.json, pick ONE unfinished cycle, work it."
  exit 0
else
  echo "=== Verification FAILED — repair before adding scope ==="
  exit 1
fi
