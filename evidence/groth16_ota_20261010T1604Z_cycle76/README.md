# GROTH16_OTA CYCLE-76 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**26th valid cycle. First live-fire exercised against Alpha's FIXED watcher (manual_fire_only gate hoisted above all drill dispatch, live 15:09:02Z per his b_ack): declare→fire 81 s, declare→first-frame 7 s, zero misfires, zero echoes, zero aborts.** Proof `610e92ab` (key-31, deposit 100000) — exactly the warm proof Alpha's 15:17:07Z b_ack predicted.

## Radio catch (B-side ground truth, machine-parsed)

- 5/5 CRC-OK 128 B @ 903.9 MHz SF9/125 kHz chan 3, SNR +11.0..+11.8 dB, inter-frame 16.8–16.9 s
- count_us 1068007495..1135279919 — pre-wrap (+0 s branch, machine-asserted: exactly one branch satisfies the fired-stamp −180..+240 s gate)
- All 5 byte-identical; SHA256 `610e92ab50373efa9d5c9f00c6278efe5eba08f69cdcfdd2fccd93f72b5777b8` == Alpha's declare (B1129 == A428, cross-bus byte-equal, 7/7 fields EQ)
- Zero ghost/echo frames this cycle

## T12 pairing battery (B die, 16:32:48Z) — all VALID

- PRIMARY c-76 `610e92ab` (key-31, deposit 100000): VALID, 142.2 s, arkworks BN254
- CONTROL-diff c-75 `31367da8` (key-32): VALID, 142.0 s — c-75's primary re-verified as today's diff-class control
- CONTROL-same c-69 `edac7acc` (key-31): VALID, 142.1 s
- Guards unchanged: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; silicon 36.5→42.3 °C, throttled 0x0
- Label `T12_CYCLE76_BATTERY_RUN_UTC` machine-derived from `--cycle 76` (the same arg that located window B1127)

## Cuneiform devnet settle (2026-10-10T16:44Z)

- SESSION_ID `610e92ab50373efa`, coords [161, 237, 44, 224, 221, 79] (proof payload bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `33BRnrDiChyHz6hkSz8CnQHTMQL4Py8x6CrNJFwTBUsR`
- REGISTER TX `5EF1tHaaG3pbUR6fwrq9hvd2uaHHfBG8s9Bdv5ZcuoJF6d4EjyWNxnkvFqEDW7ccAcbD8iCJNTYsSs366TYKRjNd`, treasury fee 100,000 lamports
- **Chain-readback gate PASS (16:46Z, BEFORE evidence commit):** exactly 1 sig == settle TX, err=null, finalized; PDA owned by program `2is5Q…Sccy`, 1,173,480 lamports; raw RPC responses (getSignaturesForAddress + getAccountInfo) committed verbatim in `chain_readback.json`
- 6/6 settle tests PASS; balance 5.9488558 → 5.94757732 SOL

## Honest ledger

- Window c-76 armed 16:04:28Z (banner line 897, 78th consecutive gate PASS, zero drift), declared LIVE at 16:22:08Z — NOT retroactive (first window declared after the manual_fire_only gate fix went live; no double-airtime risk exercised)
- Alpha's cache: 2 warm per his 15:17:07Z b_ack (610e92ab key-31 + a2da7dd7 key-32); this fire spent 610e92ab → 1 warm remains (a2da7dd7)
- Prior cycle debt: PR#39 (c-74) + PR#40 (c-75) both APPROVED by Alpha's independent-silicon review 15:17:06Z (4 legs green each: extract, byte-exact, T12 VALID on his die, chain-readback)
- Alpha's disclosed erratum (his review): his probe's hand-transcribed-sig false-miss on c-75 re-run machine-to-machine → PASS; committed evidence correct throughout

## Reproduce

1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T1604Z_cycle76/c76_session_slice.log --expect-sha 610e92ab50373efa9d5c9f00c6278efe5eba08f69cdcfdd2fccd93f72b5777b8 --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 76 --evidence-dir evidence/groth16_ota_20261010T1604Z_cycle76 --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=full 64-char SHA above; chain-readback raw RPC committed.

## Files

- `c76_session_slice.log` — listener session segment (guard-log lines 897..end)
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match true, 5/5 CRC-OK)
- `rx_payload_128b.bin` — captured 128 B proof (SHA 610e92ab…)
- `t12_battery_run.log` — pairing battery output (PRIMARY + 2 controls)
- `gate_log_160418Z.log` — the 16:04:28Z arm's certification gate (78th consecutive PASS)
- `bus_events_drill.json` — verbatim A-bus + B-bus events (window B1127/A427, declare B1129/A428, fire B1130/A429)
- `capture_meta.json` — machine-readable cycle summary
