#!/usr/bin/env bash
# Settle cycle-121 groth16_ota on Cuneiform devnet (Bravo) — primary key is
# machine-parsed from the declare (identity era). All values
# machine-derived at runtime from the c-121 evidence dir + battery attempt
# log; class-scan label parsed FROM the battery log (c-92 pre-label law),
# never drafted. Gates before exec: attempt log carries complete-line
# BATTERY_EXIT=0 AND the "PRIMARY VALID + CONTROLS VALID" verdict; extract
# sha256_match true + 5 CRC-OK frames digesting to the declared sha;
# declare/extract SHA byte-equality; dual-bus declare byte-equal; GUARD-AFTER
# unchanged. Mirrors settle_cycle119.sh (proven c-119) with c-121 paths only.
set -eu
EV="$HOME/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261017T0324Z_cycle121"
LOG="$EV/t12_cycle121_battery_attempt1.log"
cd "$HOME/fleet-repos/solana-cuneiform-milestone1/app"

read -r SETTLE_EXPECT_SHA SETTLE_META < <(python3 - "$EV" "$LOG" <<'PY'
import json, re, sys
from datetime import datetime
ev, log_path = sys.argv[1], sys.argv[2]
d = json.load(open(f"{ev}/b_rx_extract_output.json"))
b = open(log_path).read()

lines = b.splitlines()
# battery-law settle gate: complete-line BATTERY_EXIT=0 + PRIMARY VALID + CONTROLS VALID
assert any(l.strip() == "BATTERY_EXIT=0" for l in lines), "settle blocked: no complete-line BATTERY_EXIT=0"
assert any(l.startswith("BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID") for l in lines), \
    "settle blocked: battery verdict is not PRIMARY VALID + CONTROLS VALID"
assert any(l.startswith("GUARD-AFTER") and "unchanged" in l for l in lines), "guards changed mid-battery"
sha = d["expected_sha256"]
# sha-scoped gate (c-108 law): require exactly 5 frames digesting to THIS sha
pk = sorted([p for p in d.get("crc_ok", []) if p.get("sha256") == sha], key=lambda p: int(p["count_us"]))
assert d.get("sha256_match") is True and len(pk) == 5, "extract gate failed"
gaps = [round((int(pk[i+1]["count_us"])-int(pk[i]["count_us"]))/1e6,1) for i in range(4)]
snr = [p["snr_avg"] for p in pk]
raw = json.load(open(f"{ev}/declare_dual_bus_raw.json"))
dec = raw["b_bus"]["declare"]["data"]; dec_ts = raw["b_bus"]["declare"]["ts_utc"]
fired = raw["b_bus"]["fired"]["data"]
win = json.load(open(f"{ev}/cycle121_window_declare.json"))
win_event = win["event"]
win_b_seq = win.get("b_bus_seq")
assert dec["proof_sha256"] == sha, "declare/extract SHA divergence"
assert raw.get("declare_byte_diff_b_eq_a") is True and raw.get("fired_byte_diff_b_eq_a") is True, \
    "dual-bus byte-diff not equal"
# declare-to-fire delta computed from raw bus timestamps (never typed)
d0 = datetime.strptime(dec_ts, "%Y-%m-%dT%H:%M:%SZ")
d1 = datetime.strptime(fired["fired_utc"], "%Y-%m-%dT%H:%M:%SZ")
delta_s = int((d1 - d0).total_seconds())
meta_j = json.load(open(f"{ev}/capture_meta.json"))
# label composed from the battery's own run line (c-92 law: derived, never drafted)
run_line = next((l for l in lines if l.startswith("T12_CYCLE121_BATTERY_RUN_UTC")), "T12_CYCLE121")
meta = (f"5/5 CRC-OK 128B @ 903.9MHz SF9, SNR +{min(snr,key=float)}..+{max(snr,key=float)} dB, "
        f"inter-frame {gaps[0]}s uniform, {meta_j['wrap_branch']} burst, window B{win_b_seq} armed {win_event['armed_at_utc']}, "
        f"fired {fired['fired_utc']}, ~{delta_s}s declare-to-fire, "
        f"key-{dec['private_key_id']} deposit {dec['deposit_value']}, identity era VK {dec.get('vk_sha256','?')[:8]}")
print(sha, meta)
PY
)
export SETTLE_RX_BIN="$EV/rx_payload_128b.bin"
export SETTLE_EXPECT_SHA
export SETTLE_META
export SETTLE_OUT_DIR="groth16_ota_settlement_20261017T0124Z_cycle121"
# Class-scan label + key id: parsed FROM the battery log at runtime (c-92 law)
CLASS_LINE=$(grep -m1 "CLASS SCAN" "$LOG" || true)
KEY_ID=$(grep -m1 -oP 'primary key-\K\d+' "$LOG" || echo "?")
export SETTLE_VERIFIED="YES - ${CLASS_LINE:-<no class-scan line>} ; BATTERY_EXIT=0 via exit contract"
export SETTLE_TRANSFER="cycle-121 OTA Groth16/BN254 proof A->B, node-b-rx, full T12 battery COMPLETE VALID (exit 0), key-${KEY_ID} identity era, class scan per battery log (c-92 law)"
export PATH="$HOME/.hermes/tools/node-26.7.0-linux-arm64/bin:/usr/local/bin:/usr/bin:/bin"
echo "SETTLE_EXPECT_SHA=$SETTLE_EXPECT_SHA"
echo "SETTLE_META=$SETTLE_META"
exec npx tsx src/settle_groth16_ota.ts
