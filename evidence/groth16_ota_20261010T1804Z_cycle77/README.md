# groth16_ota cycle-77 — COMPLETE VALID A→B (27th valid cycle)

**Window**: armed 2026-10-10T18:04:49Z → true close 2026-10-10T20:04:49Z (listener PID 79218,
79th consecutive LORA_CHIRP_RECOVERY gate PASS, chip SX1302 v1.0 (0x10), EUI 0016c001ff18afa3).
**Declare**: B-bus seq 1139 (18:20:42Z) → Alpha watcher hot-path fired in **82s** (5/5 TX_DONE,
fired 18:22:04Z), first frame 9s after declare. Declare byte-equal cross-bus: B1141 == A433
(all 7 verification fields EQ, machine-diffed).
**Proof**: key-32, deposit 100001, 128 B compressed Groth16/BN254 (A 32B G1 || B 64B G2 || C 32B G1),
seed-42 canon PK (PK sha 8dda8b79…, VK sha 7bd5683f…), pre-proven cache.
**Payload SHA256**: `a2da7dd7737f574c47b0a8d4aa846603fa7016d48f3c7cf4c82d04109b37d138`

## Radio capture (machine-extracted, `b_rx_extract.py` rc=0)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (904.3 MHz radio A, IF -400 kHz), SF9, chan 3
- SNR +11.0..+11.5 dB, RSSI 198.0, inter-frame ~16.79 s, count_us 962216655..1029363200 (PRE-WRAP, +0s branch)
- `sha256_match: true` — all 5 frames byte-identical to the declare
- Session slice: `c77_session_slice.log` (from GATE PASS ARMING 18:04:49Z banner to EOF)

## T12 pairing battery (`T12_CYCLE77_BATTERY_RUN_UTC=2026-10-10T18:27:56Z`)
- PRIMARY `a2da7dd7` (captured, key-32): **VALID**, 142.1 s
- CONTROL-diff `610e92ab` (c-76, key-31, machine-picked): **VALID**, 142.1 s
- CONTROL-same `c300e5b4` (c-70, key-32, machine-picked): **VALID**, 140.9 s
- SHA gate 64/64; GUARD before/after unchanged (binary a0c74748…, PK 8dda8b79…, VK 7bd5683f…)
- Silicon: 39.9→42.8 °C, throttled=0x0, no mid-battery key/binary drift
- **Verdict: COMPLETE VALID** on the B die.

## Cuneiform Devnet settlement (chain-readback verified)
- REGISTER TX: `2JbsDY7nm4PkrfznnwAXKcdHqtKNTFzGLhE25krWbUX5VxPCkTNyXYf8UaVkqyBdJaJbNsUE35W4MkGmtUuwrcL3` (slot 509634556, err None — `getSignaturesForAddress` byte-match on record PDA)
- Record PDA: `FpYDe2qMPiWEHxFtu2vMDLUZRfYYEg32Dgkzoc8SPGJ3`; session_id a2da7dd7737f574c; merkle_root = payload SHA256; coords [109,4,133,137,72,255]
- Treasury delta +100000 lamports (CPI fee); balance 5.94757732 → 5.94629884 SOL
- https://explorer.solana.com/tx/2JbsDY7nm4PkrfznnwAXKcdHqtKNTFzGLhE25krWbUX5VxPCkTNyXYf8UaVkqyBdJaJbNsUE35W4MkGmtUuwrcL3?cluster=devnet

## Honest ledger
1. **Posted close-time skew (owned, corrected)**: the c-77 `rx_window_open` (B1139/A432) posted
   `closes_at_utc=2026-10-11T00:04:49Z` — +4 h wrong. Root cause: the window composer parsed the
   UTC ARM banner string via local-time `time.mktime` (EDT), shifting the close. TRUE close =
   20:04:49Z (ARM + 7200 s). Correction posted B1142/A434 within 2 minutes of discovery; the fire
   completed 18:22:04Z — INSIDE the true window — so no airtime impact and the verdict is
   unaffected. Fix law: window composers must use tz-aware UTC datetime arithmetic
   (`datetime.strptime(...).replace(tzinfo=utc) + timedelta`), never naive `mktime` on UTC strings.
2. **Battery final-log write crash (owned)**: the battery issued its verdict at 18:38Z but crashed
   on its last line writing `t12_cycle77_battery.log` into `evidence/cycle77/` — because I renamed
   the evidence dir (`evidence/cycle77` → `evidence/groth16_ota_20261010T1804Z_cycle77`) AFTER
   launching the battery, invalidating its hard-coded output path. The verdict had already been
   printed to the run log (captured here as `t12_cycle77_battery.log` via stdout redirect); no
   pairing result was lost. Fix law: never rename an evidence dir while a battery writing into it
   is still running — the battery derives its output path at startup.
3. `expected_payload_sha256` in the window event was prefix-only (`a2da7dd7`) — the full 64-hex
   was never published on any plane before the fire; per the machine-parse law I refused to
   hand-complete it, and the gate bound to the pre-fire declare instead. His watcher's declare
   (B1141/A433) published the full SHA before the first send, which the SHA gate then matched 64/64.

## Files
- `rx_payload_128b.bin` — captured on-air proof (sha256 = a2da7dd7737f574c47b0a8d4aa846603fa7016d48f3c7cf4c82d04109b37d138)
- `b_rx_extract_output.json` — certified extraction (sha256_match=true)
- `declare_c77.json` — both-bus declare pair (byte-equal)
- `bus_events_drill.json` — all c-77 events from both buses
- `capture_meta.json` — machine-parsed capture metadata
- `c77_session_slice.log` — raw RX session segment
- `t12_cycle77_battery.log` — full battery run log (stdout redirect)
- `settle_run.log` + `chain_readback.json` — settlement + on-chain verify
