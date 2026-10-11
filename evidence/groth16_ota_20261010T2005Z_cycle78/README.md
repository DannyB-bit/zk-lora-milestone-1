# groth16_ota cycle-78 — COMPLETE VALID A→B (28th valid cycle)

**Window**: armed 2026-10-10T20:05:09Z → close 2026-10-10T22:05:09Z (listener PID 92336,
`test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0`,
80th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` gate, chip 0x10 v1.0).
**First window declared by the durable tz-aware composer `declare_rx_window.py v1.0`** —
`closes_at_utc` was posted tz-aware-correct on the first try, closing the c-77 +4 h EDT
`mktime`-skew defect class (proven 2026-10-10 cycle-77, correction event B1142).

**Declare** (bus-stamp derived — corrected per Codex review on PR #43): B-bus seq
1154 / A-bus seq 440 (20:27:50Z) → Alpha watcher proof-declared in **1 s** (B1155/A441)
→ 5/5 TX_DONE complete **20:29:10Z** (B1157/A442) = **80 s declare-to-fire, watcher
react +0 s** — 4th consecutive 80 s-class hot-path fire (81/81/82/80 s), no LLM turn
in the loop. The earlier `bus_events_drill.json` line `B442` was a bad event ID
(nonexistent on the B bus) — corrected; see `corrections.md`.

**Proof**: key-31, deposit 100000, 128 B compressed Groth16/BN254
(A 32B G1 || B 64B G2 || C 32B G1), seed-42 canon PK (PK sha 8dda8b79 / VK sha 7bd5683f),
watcher hot-path cache pop (refilled by Alpha 18:49Z b_ack: `154750eb` key-31).

**Payload SHA256**: `154750eb50ff6008c582bb830386f3955cdf13ac58c28eec3b91566d5dc6d6a8`

## Radio capture (machine-extracted, `b_rx_extract.py` rc=0)

- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz
- count_us 1368486994..1435873897 (pre-wrap), inter-frame ≈16.9 s, SNR +10.8..+11.5 dB
- `sha256(payload) == declare` — 5/5 byte-identical, `sha256_match: true`
- Ambient 23 B frame in the same listener session (count_us 367589808, chan 7) is NOT
  part of the burst; `b_rx_extract.py` gates it out by size (≥100 B) + digest equality.

## T12 pairing battery (`T12_CYCLE78_BATTERY_RUN_UTC=2026-10-10T20:35:54Z`)

- PRIMARY cycle-78 captured `154750eb` (key-31): **VALID**, 142.1 s
- CONTROL-diff key-32 `a2da7dd7` (c-77, different statement class): **VALID**, 142.0 s
- CONTROL-same key-31 `edac7acc` (c-69, same class): **VALID**, 142.1 s
- SHA gate 64/64; declare cross-bus byte-equal (A441 == B1155); GUARD binary a0c74748 /
  PK 8dda8b79 / VK 7bd5683f unchanged before/after; silicon 38.4 → 43.8 °C, throttled=0x0

## Cuneiform Devnet settlement (chain-readback verified)

- Record PDA: `8y8TBKWMT4kJE6X561ih5bbA6tMNznXo6AZwwh2kUWg4`
- REGISTER TX: `4FzavZgsh1hpQBp2QNMH4qU4oDCrSGjtoPnUJGbH8BkqiWLjX5A7Ja8ssg9pmmWYoeYbVm4PWEVeHQx2B3ZMNiri`
  (slot 509665187, err=null — machine-fetched `getSignaturesForAddress` byte-match)
- Merkle root = proof payload SHA256 — **raw-32-byte readback re-verified live
  2026-10-11T04:2xZ via `tools/chain_readback_v2.py`: root byte-exact at Anchor offset
  62..94, session 40..56, coords 56..62 — PASS** (the v1 readback artifact class only
  proved signature existence; the c-80 review exposed its hex-string probe defect)
- Merkle root = proof payload SHA256; coords registered `[124, 33, 233, 4, 70, 122]`
- Treasury +100000 lamports; 6/6 settle tests passed; `ZK_RF_TO_CHAIN_LOOP_CLOSED=YES`

## Honest ledger

- No misses, no misfires, no corrections this cycle. The c-77 window-composer EDT-skew
  defect was closed this turn by the durable composer (this PR's declare event is the
  first machine-composed window; the c-77 correction B1142 remains the record for that
  defect). Alpha's independent-silicon reviews (PR#41, PR#42 — APPROVE with full
  reproduce matrix on his die, T12 VALID 116 s/115 s) closed both pending reviews.
- Untracked gate logs from Oct 4–5 sit in the repo worktree; not part of this PR.

## Files

- `c78_session_slice.log` — listener session slice (arm banner line → window still open)
- `b_rx_extract_output.json` — machine extraction, SHA gate PASS
- `declare_c78.json` — composer output (window declare payload + cert)
- `bus_events_drill.json` — all 10 c-78 drill events, both buses
- `t12_cycle78_battery.log` — full T12 battery run
- `settle_run.log` — devnet settle output
- `chain_readback.json` — machine-fetched on-chain signature readback
- `capture_meta.json`, `result_summary.txt` — machine-derived summary
- `rx_payload_128b.bin` — the 128 B captured proof payload (byte-exact)

## Reproduce

```
python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T2005Z_cycle78/c78_session_slice.log \
  --expect-sha 154750eb50ff6008c582bb830386f3955cdf13ac58c28eec3b91566d5dc6d6a8 --min-size 100
python3 tools/t12_battery_template.py --cycle 78 \
  --evidence-dir evidence/groth16_ota_20261010T2005Z_cycle78 \
  --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log
# chain readback: getSignaturesForAddress(8y8TBKWMT4kJE6X561ih5bbA6tMNznXo6AZwwh2kUWg4)
```
