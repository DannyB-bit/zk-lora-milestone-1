#!/usr/bin/env bash
# c-123 T12 battery launcher — exit-contract lines the settle gate asserts on
# (c-95 law: complete-line BATTERY_EXIT=<rc> + BATTERY_DONE_UTC after; per-attempt
# log naming c-90 law; --guard-log explicit c-82/c-84 law; template sha-guard c-95 law)
# Mirrors launch_t12_cycle122.sh (proven c-122, PR#88) with c-123 paths; NEW c-121-law instance caught: sed-mirror left --cycle 122 (space-separated arg survived cycle122->cycle123 token replace) — attempts 1-5 honest ledger.
set -u
cd "$HOME/fleet-repos/zk-lora-milestone-1"
TPL="tools/t12_battery_template_canonical_fixed_6a49d04.py"
EXPECT_TPL_SHA="9c85e6a6a9901147a0bd560a42d1683cdca8ee6660dceeb34988f8d9edec22e0"
ACTUAL_TPL_SHA=$(sha256sum "$TPL" | cut -d' ' -f1)
if [ "$ACTUAL_TPL_SHA" != "$EXPECT_TPL_SHA" ]; then
  echo "SHA-GUARD ABORT: canonical template bytes changed ($ACTUAL_TPL_SHA != $EXPECT_TPL_SHA)"
  exit 9
fi
ATTEMPT="${1:-attempt1}"
LOG="$HOME/fleet/logs/t12_cycle123_battery_${ATTEMPT}.log"
python3 -u "$TPL" --cycle 123 \
  --evidence-dir evidence/groth16_ota_20261017T0725Z_cycle123 \
  --guard-log "$HOME/fleet/logs/rx_standby_continuous_20261015T171837Z.log" \
  >> "$LOG" 2>&1
rc=$?
printf 'BATTERY_EXIT=%d\n' "$rc" >> "$LOG"
printf 'BATTERY_DONE_UTC=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
echo "launcher done rc=$rc log=$LOG"
exit "$rc"
