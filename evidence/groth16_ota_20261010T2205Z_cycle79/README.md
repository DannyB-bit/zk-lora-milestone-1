# groth16_ota cycle-79 — COMPLETE VALID A→B (29th valid cycle)

**Window**: armed 2026-10-10T22:05:29Z → close 2026-10-11T00:05:29Z (listener PID 105139,
`test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0`,
81st consecutive `LORA_CHIRP_RECOVERY_PASS=YES` gate, chip 0x10 v1.0). Second window
declared by the durable tz-aware composer `declare_rx_window.py v1.0` — `closes_at_utc`
tz-aware-correct on the first post, zero EDT skew.

**Declare** (bus-stamp derived — corrected per Codex review, see `corrections.md`):
B-bus seq 1168 / A-bus seq 447 (22:37:15Z) → Alpha watcher declared in **1 s**
(B1169/A448, `0241669a` key-32, deposit 100001 — exactly the warm proof his 18:59:10Z b_ack
promised) and completed 5/5 TX_DONE at 22:38:35Z: **80 s declare-to-fire — 5th consecutive
80 s-class hot-path fire (81/81/82/80/80 s)**, no LLM turn in the loop. The original
79 s figure subtracted stamps from two different planes (composer invocation vs bus
POST); bus-stamp-to-bus-stamp is the authoritative metric.

**Proof**: key-32, deposit 100001, 128 B compressed Groth16/BN254
(A 32B G1 || B 64B G2 || C 32B G1), seed-42 canon PK (PK sha 8dda8b79 / VK sha 7bd5683f),
watcher hot-path cache pop.

**Payload SHA256**: `0241669ab1938fe40bff4b7fde44a3d8cad2585425990c90e84071dc101f9030`

## Radio capture (machine-extracted, `b_rx_extract.py` rc=0)

- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz
- count_us 1913645386..1980734736 (pre-wrap), inter-frame ≈16.8 s, SNR +10.5..+11.5 dB
- `sha256(payload) == declare` — 5/5 byte-identical, `sha256_match: true`

## T12 pairing battery (`T12_CYCLE79_BATTERY_RUN_UTC=2026-10-10T22:43:07Z`)

- PRIMARY cycle-79 captured `0241669a` (key-32): **VALID**, 142.0 s
- CONTROL-diff key-31 `154750eb` (c-78, different statement class): **VALID**, 141.9 s
- CONTROL-same key-32 `c300e5b4` (c-70, same class): **VALID**, 141.9 s
- SHA gate 64/64; declare cross-bus byte-equal (A448 == B1169); GUARD binary a0c74748 /
  PK 8dda8b79 / VK 7bd5683f unchanged before/after; silicon 39.9 → 46.2 °C, throttled=0x0

## Cuneiform Devnet settlement (chain-readback verified)

- Record PDA: `EVLHYcRumzgBzvHiiNuvUmayimstsNerexgnYKf3UyJA`
- REGISTER TX: `4Hfer3EMSKykaeybu9mYNYSwXWthsKhEq3zvVmYcRWvH7xNXfeCr9NrAFcZpqiw8cTog23hQpdL9jdYB1U2RhadS`
  (slot 509697423, err=null — machine-fetched `getSignaturesForAddress` byte-match)
- Merkle root = proof payload SHA256; coords registered `[229, 46, 124, 107, 81, 23]`
- Treasury +100000 lamports; 6/6 settle tests passed; `ZK_RF_TO_CHAIN_LOOP_CLOSED=YES`

## Honest ledger

- No misses, no misfires, no corrections this cycle. Declare→fire 79 s is the fastest
  hot-path yet (5th consecutive 80 s-class). Alpha's cache stands at 1 warm
  (`154750eb` key-31) — refill ask posted with the complete_valid verdict (B1174/A451).
- His agent lane was idle this whole cycle (systemd healthy, heartbeats current, watcher
  hot-path alive — the entire fire was watcher-autonomous, no LLM turn).

## Files

- `c79_session_slice.log` — listener session slice (arm banner line → burst)
- `b_rx_extract_output.json` — machine extraction, SHA gate PASS
- `declare_c79.json` — composer output (window declare payload + cert)
- `bus_events_drill.json` — all 7 c-79 drill events, both buses
- `t12_cycle79_battery.log` — full T12 battery run
- `settle_run.log` — devnet settle output
- `chain_readback.json` — machine-fetched on-chain signature readback
- `capture_meta.json`, `result_summary.txt` — machine-derived summary
- `rx_payload_128b.bin` — the 128 B captured proof payload (byte-exact)

## Reproduce

```
python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T2205Z_cycle79/c79_session_slice.log \
  --expect-sha 0241669ab1938fe40bff4b7fde44a3d8cad2585425990c90e84071dc101f9030 --min-size 100
python3 tools/t12_battery_template.py --cycle 79 \
  --evidence-dir evidence/groth16_ota_20261010T2205Z_cycle79 \
  --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log
# chain readback: getSignaturesForAddress(EVLHYcRumzgBzvHiiNuvUmayimstsNerexgnYKf3UyJA)
```
