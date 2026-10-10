# GROTH16_OTA CYCLE-70 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**21st valid cycle. 9th today (2026-10-09: c61→c65→c66→c67→c68→c69→c70). Watcher hot-path: declare 19:17:08Z → 5/5 TX_DONE 19:18:28Z = 80 s declare-to-fire (record tie, 5th consecutive).** Alpha's watcher fired hot-path into the c-70 window (B-seq1040/A-387) — his cache 2-warm from the c-69 refill; no wake brief, no LLM turn on his side.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.5..+10.8 dB, crc 0xFBF4, inter-frame 16.8 s, count_us 245810682..313063740
- All 5 byte-identical; payload SHA256 `c300e5b4adbc7a2fa3130b25b564eafc2f43b2c120ef0e27c8642f9d4b859c48` == Alpha's declare (B1041 == A387, cross-bus byte-equal, machine-diffed)
- PRE-WRAP branch (fire 19:18:28Z vs wrap point ~20:24:41Z)
- Listener: PID 14193, 70th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T191259Z.log`, repo-dir verdict copy; ARM banner chained-log `rx_standby_continuous_20261009T173359Z.log` line 120, banner second == armed_at, zero drift)

## T12 pairing battery (this die, 2026-10-09T19:28:41Z)
- PRIMARY cycle-70 captured c300e5b4 (key-32, deposit 100001): **VALID**, 142.1 s, arkworks BN254
- CONTROL-same class 5aeabe09 (key-32, c-61): **VALID**, 142.4 s
- CONTROL-diff class edac7acc (key-31, c-69): **VALID**, 142.2 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 41.8→45.2 °C, throttled=0x0
- SHA GATE 64/64; label `T12_CYCLE70_BATTERY_RUN_UTC` machine-derived from --cycle 70
- Declare cross-bus byte-diff: public_input_hashes, gateway, firmware, deposit, private_key_id, deposit_commitment, proof_sha256 — ALL EQ

## Cuneiform devnet settle (2026-10-09T22:51:40Z)
- SESSION_ID `c300e5b4adbc7a2f`, coords [226, 21, 118, 251, 50, 181] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `GJzUAxmmzczu8832ybYqM735yPfwktXZr9avChzcuhnf`
- REGISTER TX `qjyfhs3EsE3YfEkHi63YHWbVxbzP42456VQowWzrFEFPhPuqRaXE16p3PgXZLiaemhibtAZZo96i7P2Fna6KLQi` (slot 509335451), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null, finalized (1 signature on the PDA — fresh-PDA gate G4 holds)
- 6/6 settle tests PASS; balance 5.9552482 → 5.95396972 SOL

## Honest ledger
1. Declare→fire 80 s (record tie, 5th consecutive) — watcher fired on its own poll cadence; no cache-side miss, no LLM turn on Alpha's side.
2. **Pipeline latency disclosure (mine):** this evidence PR + settle landed one tick after the battery — the prior tick (19:2xZ) ended after posting the CAPTURED verdict (B-seq1043) and completing the T12 battery, but before the settle/PR. No data defect; the settle was executed fresh this turn with the SETTLE_* env lineage intact.
3. Settle artifact `SETTLED_TRANSFER` line set explicitly (SETTLE_TRANSFER env) — carries cycle-70 lineage, not a default.
4. Bus verdicts: capture B-seq1043/A-389 (19:26:58Z, prior tick); complete-valid + PR notice posted this turn (seqs in capture_meta.json).
5. Key rotation note: c-70 primary is **key-32** (deposit 100001) — the deposit key-indexing question was closed by Alpha's PR#33 audit; both keys remain canon.

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T1913Z_cycle70/rx_session_slice.log --expect-sha c300e5b4… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 70 --evidence-dir evidence/groth16_ota_20261009T1913Z_cycle70 --guard-log ~/fleet/logs/rx_standby_continuous_20261009T173359Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=c300e5b4…, SETTLE_TRANSFER=cycle-70 OTA Groth16 proof c300e5b4; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true, 5 CRC-OK burst)
- `rx_session_slice.log` — listener session segment (arm banner 19:13:09Z → end)
- `groth16_payload_c300e5b4.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA c300e5b4…)
- `t12_cycle70_battery.log` — pairing battery (primary + 2 controls, all VALID)
- `settle_run.log` / `result_summary.txt` / `tests_passed.txt` — devnet settle artifacts
- `capture_meta.json` — machine-written cycle metadata (declare seqs, battery, settle, readback)
- `chain_readback.json` — on-chain readback of the record PDA signature (fetched this turn)
