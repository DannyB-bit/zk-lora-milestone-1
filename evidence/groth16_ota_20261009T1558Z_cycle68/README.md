# GROTH16_OTA CYCLE-68 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**19th valid cycle. 7th today (2026-10-09: c65 → c66 → c67 → c68). Watcher hot-path: declare 13:56:41Z → 5/5 TX_DONE 13:58:00Z = 80 s declare-to-fire (record tie).** Fired per my 13:46Z wake brief — Alpha's cache refilled and fired inside the window without an LLM turn (watcher hot-path).

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.5..+10.8 dB, inter-frame 16.7–16.8 s, count_us 1936930540..2003982295
- All 5 byte-identical; payload SHA256 `94dad8d98e558fa52e95e7dda31d4a2aac5337b8ffc270eb63294c8bab99285d` == Alpha's declare (B1008 == A372, cross-bus byte-equal, machine-diffed data payloads)
- PRE-WRAP branch (fire 13:58:00Z vs wrap point ~14:36:10Z)
- Listener: PID 183958 comm-exact `test_loragw_hal`, 68th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T132420Z.log`, repo-dir verdict copy; ARM banner chained-log line 3999, banner second == armed_at, zero drift)
- Session segment: 10 packets total, 5 CRC-OK burst frames + 5 ambient 23 B frames elsewhere in band (904.5/904.7 MHz, SNR −16..−17 dB) — none in the 903.9 gate

## T12 pairing battery (this die, 2026-10-09T15:25Z)
- PRIMARY cycle-68 captured 94dad8d9 (key-31): **VALID**, 142.1 s, arkworks BN254
- CONTROL-diff class 6e7681f9 (key-32, c-67): **VALID**, 141.9 s
- CONTROL-same class c2855891 (key-31, c-65): **VALID**, 142.3 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 47.7 °C, throttled=0x0
- SHA GATE 64/64; label `T12_CYCLE68_BATTERY_RUN_UTC` machine-derived from --cycle 68 (template law)

## Cuneiform devnet settle (2026-10-09T15:32:25Z)
- SESSION_ID `94dad8d98e558fa5`, coords [39,166,54,150,227,186] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `S9JmABF5yRKt23BWFwmyaCvjPB7yHbx1s7n2hH65Hw2`
- REGISTER TX `41ZyMbwVVew2HLEuN4a1YzTmtJqgzasvYU1VZoCH8hsfrrJzRXTN29utCruEttKoDo9ohAghk9uq7YUbzxnywH7b` (slot 509224980), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null, finalized (1 signature total on the PDA — fresh-PDA gate G4 holds)
- 6/6 settle tests PASS; balance 5.95780516 → 5.95652668 SOL

## Honest ledger
1. Declare→fire 80 s (record tie with c-61/c-65/c-66) — watcher fired on its own poll cadence per wake brief; no cache-side miss.
2. `deposit_value=100000` on this key-31 declare — normal; the c-67 "anomaly" (100001) is CLOSED by Alpha's PR#33 audit: deposit is key-indexed BY DESIGN (`build_one(key, 123456789+i, 100_000+i)`), key-31=100000 / key-32=100001 — a discriminator, not an anomaly.
3. Settle artifact nit (cosmetic): `settle_result_summary.txt` line `SETTLED_TRANSFER` carries the script's hardcoded default string ("first verified OTA…20260929T223317Z") because the `SETTLE_TRANSFER` env var was not set at run time. All material fields (SHA, PDA, TX sig, balances, tests) are machine-correct; the on-chain record is unaffected. Disclosed, not re-run (fresh-PDA gate makes settle idempotent; a re-run is unnecessary devnet spend).
4. My bus capture verdict B-seq1014 (mirror A-375) posted before PR staging per the immediate-verdict law; complete-valid verdict B-seq1016 (A-376).

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T1558Z_cycle68/c68_session_slice.log --expect-sha 94dad8d9… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 68 --evidence-dir evidence/groth16_ota_20261009T1558Z_cycle68 --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=94dad8d9…, SETTLE_TRANSFER=cycle-68 OTA Groth16 proof 94dad8d9 (set it — see honest-ledger nit 3); chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true, 5 CRC-OK burst)
- `c68_session_slice.log` — listener session segment (arm banner line 3999 → end)
- `groth16_payload_94dad8d9.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA 94dad8d9…)
- `t12_cycle68_battery.log` / `t12_cycle68_battery_raw.log` — pairing battery (processed + raw)
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
- `capture_meta.json` — machine-written cycle metadata (declare seqs, battery, SHA gate)
- `chain_readback.json` — on-chain readback of the record PDA signature (fetched this turn)
