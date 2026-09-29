#!/usr/bin/env bash
# Researcher B (Bravo, Agent 05, RakMiner-B) — M1-native RX evidence harness.
# Mirrors the committed M1 end_to_end_rf_success/node-b-rx format:
#   recovery log (PASS=YES) -> RX capture (proven M1 config) -> payload
#   extraction -> SHA256 comparison vs A's TX payload -> evidence files.
#
# Fail-closed: any step failing stops the run and records the failure honestly.
#
# Env:
#   EXPECT_SHA256   A-side TX payload SHA256 to match (default: PR#2 payload)
#   RX_SECS         RX window seconds (default 420)
#   ARTIFACT_ROOT   override artifact parent dir (validation runs use scratch)
set -euo pipefail

ROOT="/home/researcher-bravo/fleet-repos/zk-lora-milestone-1"
HAL="/home/researcher-bravo/sx1302_hal"
EXPECT_SHA256="${EXPECT_SHA256:-6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d}"
RX_SECS="${RX_SECS:-420}"
ARTIFACT_ROOT="${ARTIFACT_ROOT:-$ROOT/artifacts/milestone1/hardware_capture/end_to_end_rf_success}"
ROLE="node-b-rx"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT="$ARTIFACT_ROOT/${ROLE}_${STAMP}"
mkdir -p "$ARTIFACT"

echo "EXPECT_SHA256=$EXPECT_SHA256"
echo "ARTIFACT=$ARTIFACT"

# 1. Concentrator recovery — single-owner rule + chip_id verification.
RECOVERY_LOG="$ARTIFACT/lora_chirp_recovery.log"
ROLE="$ROLE" RECOVERY_LOG="$RECOVERY_LOG" bash "$ROOT/tools/lora_chirp_recovery.sh" node-b-rx || true
if ! grep -q "LORA_CHIRP_RECOVERY_PASS=YES" "$RECOVERY_LOG"; then
    echo "RECOVERY FAILED — RX window NOT opened; recording blocker evidence" | tee "$ARTIFACT/result_summary.txt"
    date -u +"%Y-%m-%dT%H:%M:%SZ" > "$ARTIFACT/recovery_end_utc.txt"
    echo "BLOCKED: concentrator recovery failed (see lora_chirp_recovery.log)" > "$ARTIFACT/rx_exit_code.txt"
    exit 1
fi
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$ARTIFACT/recovery_end_utc.txt"

# 2. RX capture — proven M1 config (radio A 904.3, IF -400 kHz -> 903.9).
RX_CMD="timeout $RX_SECS sudo $HAL/libloragw/test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 1"
echo "$RX_CMD" > "$ARTIFACT/rx_command.txt"
cat > "$ARTIFACT/rx_settings.txt" <<EOF
Target frequency: 903.9 MHz (radio A center 904.3 MHz, channel IF -400000 Hz)
Spreading factor: SF9 (multi-SF demod, channel mode 0)
Bandwidth: 125 kHz
Concentrator: /dev/spidev0.0, radio type SX1250 (-r 1250), clock source 0
Single input mode: yes (-j)
Payload expected: 240 bytes, SHA256 $EXPECT_SHA256
EOF

date -u +"%Y-%m-%dT%H:%M:%SZ" > "$ARTIFACT/rx_start_utc.txt"
set +e
cd "$HAL/libloragw"
$RX_CMD > "$ARTIFACT/raw_hal_rx_9039_sf9_125k.log" 2>&1
RX_EXIT=$?
set -e
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$ARTIFACT/rx_end_utc.txt"
echo "$RX_EXIT" > "$ARTIFACT/rx_exit_code.txt"
echo "RX exit: $RX_EXIT (124 = timeout-bounded window, expected)"

# 3. Extract CRC-OK payloads + SHA comparison.
python3 "$ROOT/tools/b_rx_extract.py" "$ARTIFACT/raw_hal_rx_9039_sf9_125k.log" \
    --expect-sha "$EXPECT_SHA256" --min-size 240 > "$ARTIFACT/rx_extract.json" || true

python3 - "$ARTIFACT" "$EXPECT_SHA256" <<'PYEOF' || true
import json, sys, pathlib
art, expect = sys.argv[1], sys.argv[2]
d = json.load(open(f"{art}/rx_extract.json"))
crc_ok = d["crc_ok"]
(art_p := pathlib.Path(art))
(art_p / "crc_ok_count.txt").write_text(f"{len(crc_ok)}\n")
(art_p / "valid_packet_count.txt").write_text(f"{d['total_packets']}\n")
if crc_ok:
    p = crc_ok[0]
    data = bytes.fromhex(p["hex"])
    (art_p / "rx_payload_crc_ok_1.bin").write_bytes(data)
    (art_p / "rx_payload_crc_ok_1.hex").write_text(p["hex"] + "\n")
    (art_p / "rx_payload_byte_count.txt").write_text(f"{len(data)}\n")
    (art_p / "rx_payload_sha256.txt").write_text(f"{p['sha256']}  rx_payload_crc_ok_1.bin\n")
    (art_p / "a_payload_sha256.txt").write_text(f"{expect}  (RakMiner-A TX payload, PR #2)\n")
    (art_p / "payload_sha256_comparison.txt").write_text(
        f"A TX payload SHA256: {expect}\nB RX payload SHA256: {p['sha256']}\n"
        f"Payload SHA256 match: {'YES' if d['sha256_match'] else 'NO'}\n")
    (art_p / "result_summary.txt").write_text(
        f"CRC OK packets: {len(crc_ok)} of {d['total_packets']}\n"
        f"First CRC OK payload bytes: {len(data)}\n"
        f"SHA256 match vs A TX: {'YES' if d['sha256_match'] else 'NO'}\n")
else:
    (art_p / "result_summary.txt").write_text(
        f"CRC OK packets: 0 of {d['total_packets']} — no valid RX payload\n")
PYEOF

cat "$ARTIFACT/result_summary.txt"
grep -q "SHA256 match: YES" "$ARTIFACT/payload_sha256_comparison.txt" 2>/dev/null \
    && echo "E2E_RF_EVIDENCE=PASS" || echo "E2E_RF_EVIDENCE=INCOMPLETE"
