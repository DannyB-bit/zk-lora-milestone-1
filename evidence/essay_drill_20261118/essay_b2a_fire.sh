#!/bin/bash
# essay_b2a_fire.sh — Researcher Bravo (Agent 05) B->A fire for the essay_drill.
#
# Law (rak-miner-v2-radio + minigame drill precedent):
#   1. fail-closed: verify EVERY staged frame SHA256 against its manifest BEFORE
#      touching the radio (ABORT 10 on any mismatch/missing)
#   2. stop the RX chain-guard + kill any live listener (SX1302 cannot RX+TX at once)
#   3. fire via cd-first law (HAL tools call ./reset_lgw.sh by RELATIVE path)
#   4. re-certify with RECOVERY_LOG=<this run's log> (gate reads ONLY this run)
#   5. ALWAYS restart fleet-rx-standby.service on every exit path, or RX stays dark
#   6. post chirp_raw_tx_fired to BOTH buses with the real TX_DONE count
#
# Usage: essay_b2a_fire.sh <frames_dir> <reps> <gap_s> <run_tag> <payload_label>
set -u

FRAMES_DIR="$1"
REPS="${2:-1}"
GAP_S="${3:-1}"
TAG="${4:-run}"
LABEL="${5:-payload}"
EV=/home/researcher-bravo/fleet/evidence/essay_drill_20261118
HAL=/home/researcher-bravo/sx1302_hal/libloragw
TXBIN="$EV/chirp_frames_tx"
TXLOG="$EV/b2a_tx_${TAG}.log"
RECOVERY_LOG="$EV/recovery_${TAG}.log"
MANIFEST="$FRAMES_DIR/manifest.json"

echo "=== [1/6] fail-closed staged-SHA verification ($LABEL) ==="
python3 "$EV/staged_sha_gate.py" "$FRAMES_DIR" "$MANIFEST" || { echo "ABORT 10: staged SHA gate failed"; exit 10; }

echo "=== [2/6] stop RX chain-guard + kill listener ==="
systemctl --user stop fleet-rx-standby.service 2>>"$TXLOG" || true
PIDS=$(pgrep -x test_loragw_hal 2>/dev/null || true)
if [ -n "$PIDS" ]; then
  echo "killing HAL listeners: $PIDS"
  for p in $PIDS; do kill -9 "$p" 2>/dev/null || true; done
  sleep 2
fi
if pgrep -x test_loragw_hal >/dev/null 2>&1; then
  echo "ABORT 11: SPI bus still held after kill"
  systemctl --user start fleet-rx-standby.service 2>>"$TXLOG" || true
  exit 11
fi
echo "RX guard stopped; listeners remaining: $(pgrep -x test_loragw_hal | wc -l)"

echo "=== [3/6] FIRE ($LABEL: $(ls "$FRAMES_DIR"/frame_*.bin | wc -l) frames x ${REPS} rep @903.9 SF9 125kHz 14dBm) ==="
cd "$HAL" || { echo "ABORT 11: no HAL dir"; systemctl --user start fleet-rx-standby.service; exit 11; }
sudo timeout 900 "$TXBIN" -d "$FRAMES_DIR" -f 903.9 -s 9 -b 125 -p 14 -n "$REPS" -g "$GAP_S" -c /dev/spidev0.0 2>&1 | tee "$TXLOG"
TX_RC=${PIPESTATUS[0]}
echo "TX_RC=$TX_RC"

echo "=== [4/6] re-certify chain (this run's recovery log only) ==="
cd /home/researcher-bravo/fleet-repos/zk-lora-milestone-1/tools || true
RECOVERY_LOG="$RECOVERY_LOG" bash ./lora_chirp_recovery.sh 2>&1 | tail -20
GATE_RC=${PIPESTATUS[0]}
echo "RECOVERY_RC=$GATE_RC"

echo "=== [5/6] re-arm RX standby ==="
systemctl --user start fleet-rx-standby.service
sleep 3
systemctl --user is-active fleet-rx-standby.service

echo "=== [6/6] post chirp_raw_tx_fired to both buses ==="
export FLEET_FAST_TOKEN=$(grep -m1 '^FLEET_FAST_TOKEN=' ~/.hermes/.env | cut -d= -f2- | tr -d '"'"'"' ')
python3 - "$FRAMES_DIR" "$LABEL" "$TXLOG" "$TX_RC" "$REPS" "$GAP_S" <<'PYEOF'
import json, os, sys, urllib.request
sys.path.insert(0, "/home/researcher-bravo/fleet-repos/fleet/fast-channel")
from post_event import post
frames_dir, label, txlog, tx_rc, reps, gap = sys.argv[1:7]
man = json.load(open(os.path.join(frames_dir, "manifest.json")))
log = open(txlog, errors="replace").read() if os.path.exists(txlog) else ""
done = log.count("TX_DONE") + log.count("A_LORA_TX_FILE_SEND_COMPLETE=YES")
data = {"to": "alpha", "from": "bravo", "type": "chirp_raw_tx_fired",
        "drill": "essay_drill", "leg": "B_to_A", "payload_label": label,
        "payload_file": man.get("file"), "payload_bytes": man["file_bytes"],
        "file_sha256": man["file_sha256"], "total_chunks": man["total_chunks"],
        "frames_fired": man["total_chunks"], "reps": int(reps), "gap_s": int(gap),
        "rf": "903.9MHz SF9 BW125 14dBm", "tx_exit_code": tx_rc,
        "tx_done_markers": done, "tx_log": txlog,
        "frame_sha256": [f["frame_sha256"] for f in man["frames"]]}
out = {}
for url, plane in (("http://127.0.0.1:8643", "B"), ("http://192.168.1.219:8643", "A")):
    try:
        out[plane] = post(url, "chirp_raw_tx_fired", data)
    except Exception as e:
        out[plane] = {"error": f"{type(e).__name__}: {e}"}
print(json.dumps(out, indent=1))
json.dump({"post": out, "data": data},
          open(os.path.join(os.path.dirname(txlog), f"chirp_raw_tx_fired_{label}.json"), "w"), indent=1)
PYEOF

echo "TXLOG=$TXLOG"
echo "RECOVERY_LOG=$RECOVERY_LOG"
echo "FIRE_DONE tx_rc=$TX_RC recovery_rc=$GATE_RC"
exit $TX_RC
