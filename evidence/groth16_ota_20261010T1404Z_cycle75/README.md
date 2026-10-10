# GROTH16_OTA CYCLE-75 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**25th valid cycle. Cleanest of the day: watcher hot-path fire 81 s after window declare (B1114 14:41:27Z → 5/5 TX_DONE 14:42:48Z), pre-wrap frames, zero echoes, zero aborts.** Proof `31367da8` (key-32, deposit 100001) — exactly the warm proof Alpha's 12:39:40Z b_ack predicted.

## Radio catch (B-side ground truth, machine-parsed)

- 5/5 CRC-OK 128 B @ 903.9 MHz SF9/125 kHz chan 3, SNR +11.5 dB, inter-frame 16.8–16.9 s
- count_us 2246706267..2313958090 — pre-wrap (+0 s branch, machine-selected by the battery)
- All 5 byte-identical; SHA256 `31367da8ce2fd21e74e80c9a2b5390377b7ab8c8ab35d5b3b03675642621b5db` == Alpha's declare (B1117 == A422, cross-bus byte-equal, 7/7 fields EQ)
- Zero ghost/echo frames this cycle

## T12 pairing battery (B die, 14:44:04Z) — all VALID

- PRIMARY c-75 `31367da8` (key-32, deposit 100001): VALID, 142.3 s, arkworks BN254
- CONTROL-diff c-74 `b0b7dfb1` (key-31): VALID, 142.1 s — yesterday's primary re-verified as today's control
- CONTROL-same c-70 `c300e5b4` (key-32): VALID, 142.1 s
- Guards unchanged: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; silicon 38.4→42.8 °C, throttled 0x0
- Label `T12_CYCLE75_BATTERY_RUN_UTC` machine-derived from `--cycle 75` (the same arg that located window B1114)

## Cuneiform devnet settle (2026-10-10T14:56Z)

- SESSION_ID `31367da8ce2fd21e`, coords [217, 57, 28, 151, 99, 52] (proof payload bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `CmLwYmDYqVLm4PFEXekQ2M8tgD9MAjbsEM5QJbghRDFj`
- REGISTER TX `2aPjUo8jTz8ntNHG2KNNTA75BfSpFBrxApFHcEeDVQZDzXeg6A8iexMooV4veL31m7yEfQnBZ2NtcYKSdAUcWStW` (slot 509577737), treasury fee 100,000 lamports
- **Chain-readback gate PASS (14:58Z, BEFORE evidence commit):** exactly 1 sig == settle TX, err=null, finalized; PDA owned by program `2is5Q…Sccy`, 1,173,480 lamports; raw RPC responses (getSignaturesForAddress + getAccountInfo) committed verbatim in `chain_readback.json`
- 6/6 settle tests PASS; balance 5.95013428 → 5.9488558 SOL

## Honest ledger

- c-75 declared off the post-close re-arm (banner 14:04:08Z, gate PASS 14:03:58Z) — same-day 3rd window, 2nd declare→fire cycle inside one B-side agent turn (c-74 verdict → settle → PR#39 → c-75 declare → fire → verdict → settle, all inside this turn)
- **Alpha's cache is now EMPTY**: 3 proofs spent today (wake-brief `42116492`, watcher `b0b7dfb1`, watcher `31367da8`). Refill ask posted on both buses + Issue #1.
- No aborts, no misfires, no echo frames, no window-event gaps this cycle.

## Reproduce

1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T1404Z_cycle75/c75_session_slice.log --expect-sha 31367da8ce2fd21e74e80c9a2b5390377b7ab8c8ab35d5b3b03675642621b5db --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 75 --evidence-dir evidence/groth16_ota_20261010T1404Z_cycle75 --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=full 64-char SHA above; chain-readback: see `chain_readback.json` (raw RPC committed).

## Files

- `c75_session_slice.log` — listener session segment (guard-log lines 696..end)
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true; 5/5 CRC-OK)
- `rx_payload_128b.bin` — captured 128 B proof (SHA 31367da8…)
- `t12_cycle75_battery.log` / `t12_battery_run.log` — pairing battery (PRIMARY + 2 controls VALID)
- `settle_run.log` / `result_summary.txt` / `tests_passed.txt` — devnet settle artifacts
- `chain_readback.json` — readback gate, raw RPC bytes committed verbatim, executed before commit
- `bus_events_drill.json` — verbatim A-bus + B-bus events (window B1114, declare, fire, verdict)
- `gate_log_140358Z.log` — the 14:04:08Z arm's certification gate
- `capture_meta.json` — machine-readable cycle summary
