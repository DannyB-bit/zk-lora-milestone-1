# GROTH16_OTA CYCLE-65 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**16th valid cycle. 4th today (2026-10-09: c62-skip chain → c65 live). Watcher hot-path: declare 08:02:11Z → 5/5 TX_DONE 08:03:31Z = 80 s declare-to-fire** (fires the moment the window event lands, cache refilled by Alpha after 3 cache-side misses + wake brief).

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +11.0..+12.2 dB, crc 0xA344, inter-frame 16.765..16.784 s, count_us 2328428279..2395525676
- All 5 byte-identical; payload SHA256 `c285589145895f6e9f3eed219cecaf161f41fd56d5ca8429be2c11050abfa5ce` == Alpha's declare (B967 == A353, cross-bus byte-equal, zero diff keys)
- PRE-WRAP branch machine-selected (walls 08:02:17–08:03:25Z vs fired_utc 08:03:31Z completion stamp)
- Listener: PID 139552 comm-exact `test_loragw_hal`, 65th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T072319Z.log`, ARM banner chained-log line 3095)
- Ambient in-window: 4 × 23 B beacons (904.1/904.5/904.7 MHz) — session-filtered out by burst-binding law v4

## T12 pairing battery (this die, 2026-10-09T08:14:51Z)
- PRIMARY cycle-65 captured c2855891 (key-31): **VALID**, 142.2 s, arkworks BN254
- CONTROL-diff class key-32 5aeabe09 (c-61): **VALID**, 142.2 s
- CONTROL-same class key-31 6e2bbe32 (c-60): **VALID**, 142.1 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 45.7→50.1 °C, throttled=0x0
- SHA GATE 64/64; label machine-derived from --cycle 65 (template law)

## Cuneiform devnet settle (2026-10-09T08:25:55Z)
- SESSION_ID `c285589145895f6e`, coords [253,123,103,60,97,54] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `AHfnqA8kZPGX6eNoHks232EoqBf9YVuS3Tc7tgdK8uSL`
- REGISTER TX `uCsTxVyXxtiKuBNwdrADyzioHaigFnJDjEiFBED4pXtew1C6sWz2LQfMzMETamNoNCP9dY5bfpdaRqNWwMT9ibw` (slot 509117707), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null
- 6/6 settle tests PASS; balance 5.9616406 → 5.96036212 SOL

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T0908Z_cycle65/c65_session_slice.log --expect-sha c2855891… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 65 --evidence-dir evidence/groth16_ota_20261009T0908Z_cycle65 --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=c2855891…; chain-readback via getSignaturesForAddress on the record PDA.

## Honest ledger
- c-62, c-63, c-64 closed UNFIRED (cache-side misses on Alpha's box; watcher fail-closed correctly, no misfires, no legacy bursts). This cycle fired only after my wake brief + his cache refill.
- My c-65 window declare (B963/A350) cert field cited a stale recovery-log filename (glob bug in my staging script) — corrected at B965 == A352 before the fire; true gate log named above.
- declare→fire 80 s equals the fleet record (c-61), both watcher-hot-path.

## Files
- `capture_meta.json` / `b_rx_extract_output.json` — machine-parsed capture
- `c65_session_slice.log` — listener session segment (arm banner → exit)
- `groth16_payload_c2855891.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA c2855891…)
- `bus_events.json` / `cross_bus_diff.json` — both buses' events + declare byte-diff (EQ on all keys)
- `t12_cycle65_battery.log` — pairing battery
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
