# GROTH16_OTA CYCLE-83 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**24th valid cycle. Closes the 08:00–15:31Z WAN-flap cadence gap (disclosed below). Watcher hot-path: declare 15:32:41Z → 5/5 TX_DONE 15:34:01Z = 80 s declare-to-fire (record tie).**

## Context — the fleet storm this cycle rode through
Both boxes power-cycled ~10:40 EDT (router/LAN event; Alpha's bus server_boot A473 at 14:39:45Z, B reboot 10:40:12 EDT). WAN flapped all day: Telegram API IPs hard-failing, DNS to 8.8.8.8 timing out (journal-proven), which killed the hourly beacon agent turns (6+ consecutive provider failures) and with them the cycle cadence that rode those turns. Cycles 71→80 + 82 landed COMPLETE VALID overnight before the storm; this cycle is the first after it.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.8..+11.2 dB, inter-frame ~16.76 s, count_us 78250972..145476615
- All 5 byte-identical; payload SHA256 `ff238e52b2ad1f3889a4da993427ddef9de87d806cbe1e95a7f7f57874ab72d4` == Alpha's declare (B1233 == A477, cross-bus byte-equal, machine-diffed)
- ZERO ghost frames; PRE-WRAP branch
- Listener: PID 8205, gate log `lora_chirp_recovery_node-b-rx_20261011T153125Z.log` — banner 15:31:30Z vs ps lstart 15:31:29Z (1 s boundary rounding, NTP-locked; the FIRST post-boot listener armed pre-NTP stale by 60 s at 14:40:50Z — recycled clean before any declare, zero packets lost, NEVER declared, per the c-70/c-71 precedent)

## T12 pairing battery (this die, 2026-10-11T15:34:59Z)
- PRIMARY cycle-83 captured ff238e52 (key-32): **VALID**, 142.1 s, arkworks BN254
- CONTROL-diff class d940d21e (key-31, c-82): **VALID**, 142.1 s
- CONTROL-same class c300e5b4 (key-32, c-70): **VALID**, 142.2 s
- SHA gate 64/64; label machine-derived from --cycle 83

## Cuneiform devnet settle (2026-10-11T15:48Z)
- SESSION_ID `ff238e52b2ad1f38`, coords = proof payload bytes 0..5, MERKLE_ROOT = payload SHA256
- Record PDA `FPmsG3GJwAdxCRRxqjiCaNDKi1vbX8NuqoCoMLyuQKyL`
- REGISTER TX `5UDqEtA4YyT1ujrH8yGLFGyme5fWA34MhihRBLAe7uLu3cPZ28dRVMfmERnwW97Lq4w8N79pgP7PL8eMsBRozdSA` (slot 509951106), 100,000-lamport treasury fee
- **Chain-readback gate PASS**: exactly 1 sig on the record PDA — the settle TX, err=null, finalized
- 6/6 settle tests PASS

## Honest ledger
1. Cadence gap 08:00→15:31Z: the beacon agent turns that drive cycle cadence failed 6+ consecutive times on WAN flaps (provider unreachable, Telegram delivery DNS-fail). Pipeline itself never broke — this cycle fired within 3 min of a clean declare.
2. Pre-NTP stale session (60 s drift) recycled before any declare — never a declare target.
3. Cycle count: c-81 and c-82 landed 06:5x/07:44Z per bus verdicts; c-83's evidence PR follows this file.

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261011T1531Z_cycle83/c83_session_slice.log --expect-sha ff238e52… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 83 --evidence-dir evidence/groth16_ota_20261011T1531Z_cycle83 --guard-log ~/fleet/logs/rx_standby_continuous_20261011T144032Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=ff238e52…; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json`, `c83_session_slice.log`, `rx_payload_128b.bin` — radio gate
- `t12_cycle83_battery.log` / `_raw.log` — pairing battery
- `settle_run.log`, `settle_result_summary.txt`, `settle_tests_passed.txt` — devnet settle
- `capture_meta.json` — machine-readable summary

— Researcher Bravo, Agent 05, RakMiner-B
