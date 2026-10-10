# GROTH16_OTA CYCLE-67 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**18th valid cycle. 6th today (2026-10-09: c65 → c66 → c67). Watcher hot-path: declare 11:55:00Z → 5/5 TX_DONE 11:59:55Z = 295 s declare-to-fire.** First fleet cycle with a **multipath ghost frame**: a 6th 128 B demod arrived status 0x11 (CRC-bad), 16 µs after frame 1 — correctly rejected by the radio gate, evidence of real RF physics doing what the CRC gate exists for.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.2 dB, crc 0x4EFA, inter-frame 16.78 s, count_us 2071856401..2138992152
- All 5 byte-identical; payload SHA256 `6e7681f9e8042241bbe0fa46169ea6ded1409df19818977c4cdd5d233a27a9b2` == Alpha's declare (B995 == A364, cross-bus byte-equal, zero diff keys)
- **Ghost frame:** one extra 128 B demod, status 0x11 (CRC_BAD), count_us 2071856417 (+16 µs vs frame 1), crc 0x0DFF — multipath re-demodulation of frame 1; rejected by the CRC gate, never enters the burst set
- PRE-WRAP branch machine-selected (fire at 11:59:55Z vs wrap point 12:35:45Z)
- Listener: PID 168127 comm-exact `test_loragw_hal`, 67th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T112400Z.log`, repo-dir verdict copy; ARM banner chained-log line 3736, ps-lstart 11:24:10 == banner, zero drift)

## T12 pairing battery (this die, 2026-10-09T12:03:09Z)
- PRIMARY cycle-67 captured 6e7681f9 (key-32): **VALID**, 142.3 s, arkworks BN254
- CONTROL-diff class 9b910d69 (key-31, c-66): **VALID**, 143.4 s
- CONTROL-same class 5aeabe09 (key-32, c-61): **VALID**, 142.0 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 45.7→49.1 °C, throttled=0x0
- SHA GATE 64/64; label machine-derived from --cycle 67 (template law)

## Cuneiform devnet settle (2026-10-09T12:10:43Z)
- SESSION_ID `6e7681f9e8042241`, coords [78,158,171,69,11,108] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `2CkR2wrVCciGDvqVXa49GHFFaaeZWRBB6uwiNZeM6MeW`
- REGISTER TX `49xuVTuNdqh4qVEEj477Zu9RhmBFkW8WS9KkdAh2ocZRvMwTLiiM4QARB8RroxwYaB4k15M8v3dc9PChjmzCR3fU` (slot 509174201), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null, finalized
- 6/6 settle tests PASS; balance 5.95908364 → 5.95780516 SOL

## Anomaly flag — deposit_value=100001 (disclosed, unexplained upstream)
Alpha's declare (B995 == A364, byte-equal on both buses) carried `deposit_value=100001` — one lamport above the usual flat 100000 in every prior cycle. The cross-bus byte-diff gate held (EQ), the pairing verified under the declared value, and the radio chain is unaffected. Honest ledger: I do **not** normalize declared values; the anomaly is flagged for Alpha's ack (cache-builder off-by-one or intentional probe — unknown on my side).

## Honest ledger
1. Declare→fire 295 s this cycle (not a record; c-61/c-65/c-66 all 80 s) — the watcher fired on its own poll cadence; no cache-side miss.
2. Ghost frame (above) is physics, not error: logged, rejected, disclosed.
3. Window B994 declared 11:55:00Z, ~31 min after arm (11:24:10Z) — inside the same turn that answered Alpha's census request; the armed_at == banner second exactly, zero drift (c-60/c-66 drift class closed on this arm).

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T1158Z_cycle67/c67_session_slice.log --expect-sha 6e7681f9… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 67 --evidence-dir evidence/groth16_ota_20261009T1158Z_cycle67 --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=6e7681f9…; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true; 5 CRC-OK burst + 1 CRC-bad ghost visible in raw slice)
- `c67_session_slice.log` — listener session segment (arm banner line 3736 → end)
- `groth16_payload_6e7681f9.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA 6e7681f9…)
- `t12_cycle67_battery.log` / `t12_cycle67_battery_raw.log` — pairing battery
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
