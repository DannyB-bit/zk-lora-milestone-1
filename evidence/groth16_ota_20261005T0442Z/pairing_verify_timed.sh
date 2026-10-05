#!/usr/bin/env bash
# PRIMARY a1706406 (this drill, watcher_hot_path daemon-fire cycle-19) + CONTROL bd4c9ab2 (PR#14 known-VALID)
set -u
EVID="$HOME/fleet/evidence/20261005T0442Z_groth16_ota_daemon_cycle19"
LOG="$EVID/pairing_verify_timed.log"
cd "$HOME/fleet-repos/zk-lorawan"
unset ZK_LORAWAN_REPRODUCIBLE_SETUP
{
echo "keys sha-guard BEFORE:"; sha256sum keys/proving_key.bin keys/verifying_key.bin
echo "PRIMARY a1706406 (this drill, watcher_hot_path daemon-fire, A-bus declare 04:41:30Z / fired 04:42:50Z, B cycle-19)"
date -u +%H:%M:%S.%3NZ
S=$(date +%s)
P="$EVID/rx_payload_128b.bin"
./target/debug/zk_lorawan_prove verify \
  "$(python3 -c "h=open('$P','rb').read().hex();print(h[:64])")" \
  "$(python3 -c "h=open('$P','rb').read().hex();print(h[64:192])")" \
  "$(python3 -c "h=open('$P','rb').read().hex();print(h[192:256])")" \
  cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d \
  a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029 \
  8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a \
  2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005 \
  0016c001ff18afa3903900000000000000000000000000000000000000000000 \
  100000 \
  656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
echo "PRIMARY_EXIT=$?"
echo "PRIMARY wall_s=$(( $(date +%s) - S ))"
date -u +%H:%M:%S.%3NZ
CTRL="$HOME/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261004T1922Z/rx_payload.bin"
if [ ! -f "$CTRL" ]; then CTRL=$(find "$HOME/fleet-repos/zk-lora-milestone-1" -name "*.bin" -path "*1922*" | head -1); fi
echo "CONTROL bd4c9ab2 (PR#14 known-VALID) file=$CTRL"
S=$(date +%s)
./target/debug/zk_lorawan_prove verify \
  "$(python3 -c "h=open('$CTRL','rb').read().hex();print(h[:64])")" \
  "$(python3 -c "h=open('$CTRL','rb').read().hex();print(h[64:192])")" \
  "$(python3 -c "h=open('$CTRL','rb').read().hex();print(h[192:256])")" \
  cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d \
  a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029 \
  8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a \
  2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005 \
  0016c001ff18afa3903900000000000000000000000000000000000000000000 \
  100000 \
  656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
echo "CONTROL_EXIT=$?"
echo "CONTROL wall_s=$(( $(date +%s) - S ))"
date -u +%H:%M:%S.%3NZ
echo "keys sha-guard AFTER:"; sha256sum keys/proving_key.bin keys/verifying_key.bin
} >> "$LOG" 2>&1
echo "DONE" >> "$LOG"
tail -30 "$LOG"
