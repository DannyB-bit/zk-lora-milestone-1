# GROTH16_OTA CYCLE-71 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**22nd valid cycle. First cycle after the 10-10 fleet recovery: B box rebooted 02:46 EDT (pre-boot journal lost, DNS outage pre-reboot); this cycle ran on the NTP-locked re-armed session. Watcher hot-path: declare 08:03:44Z → 5/5 TX_DONE 08:05:04Z = 80 s declare-to-fire (4th consecutive record tie).** Alpha's watcher fired hot-path into the c-71 window (B-seq1070/A-400) — cache warm from his 19:22Z rebuild; no LLM turn on his side. His heartbeat at 08:04:51Z confirms: "live: 2s poll on your rx_window_open -> auto-fire burst".

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.8..+11.0 dB, inter-frame ~16.76 s, count_us 43822786..110870939
- All 5 byte-identical; payload SHA256 `709f3a8a004744fe00c7468360535e10adf70bf217027faf81325e92e662805a` == Alpha's declare (B1071 == A401, cross-bus byte-equal, machine-diffed, all 7 fields EQ)
- ZERO ghost frames this cycle (c-67's multipath ghost was the exception, not the rule)
- PRE-WRAP branch (fire 08:05:04Z vs wrap point ~09:14:47Z)
- Listener: PID 11665, 70th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261010T080257Z.log`, repo-dir verdict copy; ARM banner chained-log `rx_standby_continuous_20261010T064617Z.log` line 167, ps lstart 08:03:07Z == banner second, ZERO drift)

## Honest ledger — the pre-NTP stale session was recycled, never declared
The FIRST post-reboot listener (banner 06:46:35Z) armed on a pre-NTP-stale clock — ps lstart 06:48:30Z vs banner = **115 s drift** (this box has no RTC; the c-70 recovery caught the same class at 195 s). It was recycled clean at 08:02Z before ANY window was declared on it (c-70 precedent: a stale session is never a declare target), zero packets lost. Cycle-71's session is NTP-locked, zero drift. Disclosed per the honesty law — the drift would have silently mis-timestamped every capture wall-clock.

## T12 pairing battery (this die, 2026-10-10T08:17:34Z)
- PRIMARY cycle-71 captured 709f3a8a (key-31, deposit 100000): **VALID**, 142.2 s, arkworks BN254
- CONTROL-diff class c300e5b4 (key-32, c-70): **VALID**, 142.1 s
- CONTROL-same class c2855891 (key-31, c-65): **VALID**, 142.3 s
- Guards unchanged: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; label machine-derived from --cycle 71 (template law)

## Cuneiform devnet settle (2026-10-10T08:26:24Z)
- SESSION_ID `709f3a8a004744fe`, coords [66, 80, 29, 223, 30, 6] (proof payload bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `3RQtm7XHecukhuCeLettUDJdo8eaTfHKPoPmUFkK6GHB`
- REGISTER TX `2qfaCfUad41innA5DH1bxAxqs8htrnoRZHadXJM3GEMXtAvyDCqRQJ1XXvigxRFS9hR85vsTm5fFDRFB5kp2DEzt` (slot 509479938), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature — exactly 1 sig, err=null, finalized
- 6/6 settle tests PASS; balance 5.95396972 → 5.95269124 SOL

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T0803Z_cycle71/c71_session_slice.log --expect-sha 709f3a8a… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 71 --evidence-dir evidence/groth16_ota_20261010T0803Z_cycle71 --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=709f3a8a…; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true; 5/5 CRC-OK)
- `c71_session_slice.log` — listener session segment (arm banner → end)
- `rx_payload_128b.bin` — captured 128 B proof (SHA 709f3a8a…)
- `t12_cycle71_battery.log` / `t12_cycle71_battery_raw.log` — pairing battery
- `settle_run.log` / `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
- `capture_meta.json` — machine-readable cycle summary

— Researcher Bravo, Agent 05, RakMiner-B
