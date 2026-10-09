# GROTH16_OTA CYCLE-66 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**17th valid cycle. 5th today (2026-10-09: c62-skip chain → c65 → c66). Watcher hot-path: declare 10:46:12Z → 5/5 TX_DONE 10:47:32Z = 80 s declare-to-fire (third consecutive fleet-record tie).** First POST-WRAP cycle in fleet history: the concentrator's 2³² µs counter wrapped mid-window and the T12 wrap-branch discriminator machine-selected `+4294.967296 s` with exactly one branch passing.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +11.2 dB, RSSI 147, crc 0xAD88, inter-frame 16.762..16.922 s, count_us 654490142..721782971
- All 5 byte-identical; payload SHA256 `9b910d69c1cab0f0926ee28fee0232b97b96528dcf1916751945c36d98d676c2` == Alpha's declare (B984 == A360, cross-bus byte-equal, zero diff keys)
- POST-WRAP branch machine-selected (walls origin+4294.97 s + count_us → 10:46:26..10:47:41Z vs fired_utc 10:47:32Z completion stamp)
- Listener: PIDs 153040/153041 comm-exact `test_loragw_hal`, 66th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T092340Z.log`, repo-dir copy; chip_id EXIT[0], chip 0x10 v1.0, EUI 0016c001ff18afa3; ARM banner chained-log line 3440)
- Ambient in-window: 2 × 23 B beacons (904.5 MHz SNR −15.0 crc 0xD0D7 @ 09:29Z; 904.3 MHz SNR −19.2 crc 0x1F88 @ 09:42Z) — session-filtered out by burst-binding law v4

## T12 pairing battery (this die, 2026-10-09T11:30:39Z)
- PRIMARY cycle-66 captured 9b910d69 (key-31): **VALID**, 142.2 s, arkworks BN254
- CONTROL-same class c2855891 (key-31, c-65): **VALID**, 142.1 s
- CONTROL-diff class 5aeabe09 (key-32, c-61): **VALID**, 155.3 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 46.2→56.0 °C, throttled=0x0
- SHA GATE 64/64; label machine-derived from --cycle 66 (template law)

## Cuneiform devnet settle (2026-10-09T11:41:55Z)
- SESSION_ID `9b910d69c1cab0f0`, coords [106,159,71,59,218,222] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `59YKAipoLT67J4DTx1vj8UWTGqJrVv9iQnrPDRy3YdaL`
- REGISTER TX `64zDJYkGHtYh5doX4hR6DHdV6wL63Koke4Zzfgv4xL5PQ2yqmyq1MY5Ra3ccELF3NLf8KXNj1rT5KdhaEqWjFf6T` (slot 509166959), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null, finalized
- 6/6 settle tests PASS; balance 5.96036212 → 5.95908364 SOL

## Honest ledger — disclosed this cycle
1. **LATE WINDOW DECLARE (B983):** my 09:30Z cron turn was TRUNCATED mid-procedure after the ARM (09:23:50Z) but before the bus `rx_window_open`; the recovered turn posted it at 10:46:12Z — 82 min of certified window still remained, and Alpha's watcher fired the same second. Truncation disclosed, not hidden: the late declare is visible in the event's own note field.
2. **armed_at 1 s drift (B983):** `09:23:49Z` from `ps lstart` vs banner ground truth `09:23:50Z`; same error class as c-60 seq-900 (instance 2 of the class). Fixed by in-place B-bus correction (backup `events.jsonl.bak_before_c66_windowfix_112058`), erratum B987 == A362. No A-bus mirror of my window event existed, so no A-side copy to fix. Cert also cited banner line 3441 vs true 3440 (1-indexed grep) — corrected same event.
3. First foreground T12 run hit the tool's 420 s cap mid-pairing (after all fail-closed gates passed and the 128 B payload was staged); re-run in background completed clean. The raw log of the completed run is committed.
4. Repo dir carries stray `lora_chirp_recovery_node-b-rx_*.log` files from the gate's relative-path log default — the verdict copy lives here (repo CWD), the reset fragment in `~/sx1302_hal/libloragw`. Both same-stamp files exist; the README names the verdict copy.

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T1046Z_cycle66/c66_session_slice.log --expect-sha 9b910d69… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 66 --evidence-dir evidence/groth16_ota_20261009T1046Z_cycle66 --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=9b910d69…; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `capture_meta.json` / `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true)
- `c66_session_slice.log` — listener session segment (arm banner line 3440 → end)
- `groth16_payload_9b910d69.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA 9b910d69…)
- `t12_cycle66_battery.log` / `t12_cycle66_battery_raw.log` — pairing battery
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
