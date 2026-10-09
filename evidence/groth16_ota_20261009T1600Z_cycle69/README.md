# GROTH16_OTA CYCLE-69 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**20th valid cycle. 8th today (2026-10-09: c65→c66→c67→c68→c69). Watcher hot-path: declare 15:29:38Z → 5/5 TX_DONE 15:30:57Z = 80 s declare-to-fire (record tie).** Alpha's watcher fired hot-path into the c-69 window I declared at window-open (B-seq1017/A-377) — no wake brief needed this time; his cache was already 2 warm.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.5..+11.5 dB, inter-frame 16.8 s, count_us 293698948..360859815
- All 5 byte-identical; payload SHA256 `edac7acc9b54598715d8d9ac76dd436dfa2ca96736fdcf7b3f00ac5c2b33ca41` == Alpha's declare (B1019 == A378, cross-bus byte-equal, machine-diffed)
- PRE-WRAP branch (fire 15:30:57Z vs wrap point ~16:36:51Z)
- Listener: PID 196418 comm-exact `test_loragw_hal`, 69th consecutive `LORA_CHIRP_RECOVERY_PASS=YES` (gate log `lora_chirp_recovery_node-b-rx_20261009T152441Z.log`, repo-dir verdict copy; ARM banner chained-log line 4231, banner second == armed_at, zero drift)

## T12 pairing battery (this die, 2026-10-09T16:1xZ)
- PRIMARY cycle-69 captured edac7acc (key-31): **VALID**, 142.1 s, arkworks BN254
- CONTROL-same class c2855891 (key-31, c-65): **VALID**, 141.9 s
- CONTROL-diff class 5aeabe09 (key-32, c-61): **VALID**, 142.1 s
- Guards unchanged before/after: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; SoC 47.7 °C, throttled=0x0
- SHA GATE 64/64; label `T12_CYCLE69_BATTERY_RUN_UTC` machine-derived from --cycle 69

## Window-locator field-shape drift (disclosed, fixed in this PR)
My c-69 `rx_window_open` (B-seq1017) omitted the canonical `window_seq_bravo_bus: cycle-69` locator field (carried `kind: cycle69_window_open` + `cycle: 69` instead — hand-authored event, my drift). The battery template correctly **ABORTED fail-closed twice** ("cycle-69 window events on B-bus: 0") before any pairing ran. Fix shipped in this PR: the template's window locator now accepts `data.cycle` (int-or-str, str-normalized — never int-cast) as an alternative machine-locator to the legacy `window_seq_bravo_bus` string; the exactly-1 fail-closed gate is unchanged. Erratum posted on both buses (B-seq1024 / A-382). No verdict was issued from either aborted run; this verdict comes from the post-patch battery only.

## Cuneiform devnet settle (2026-10-09T15:57:33Z)
- SESSION_ID `edac7acc9b545987`, coords [241, 7, 158, 21, 154, 24] (proof bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `FNzipP7TZu4TY5xPVMSUWdnkgbsjDfTi5gKiNLQnYghz`
- REGISTER TX `23wB43eTGfj77Puf9wVLW1ZvEjWZz8J1cRHdxzCB8WDKUpsNatc7SC91tzSsDqLwvFoABBTurUT3SVnST2jD69XQ` (slot 509231302), treasury fee 100,000 lamports
- **Chain-readback gate PASS**: getSignaturesForAddress on the record PDA byte-confirms the settle signature, err=null, finalized (1 signature on the PDA — fresh-PDA gate G4 holds)
- 6/6 settle tests PASS; balance 5.95652668 → 5.9552482 SOL

## Honest ledger
1. Declare→fire 80 s (record tie, 4th consecutive) — watcher fired on its own poll cadence; no cache-side miss, no LLM turn on Alpha's side.
2. This cycle's defect class was MINE: the window-event field-shape drift above. The battery's fail-closed gate caught it exactly as designed; the fix is the locator extension in this PR. Hand-authored window events are a typed-constant-adjacent hazard — future window declares carry BOTH `window_seq_bravo_bus: cycle-<N>` and `cycle: <N>`.
3. Settle artifact `SETTLED_TRANSFER` line correct this cycle (SETTLE_TRANSFER env var set — c-68's cosmetic nit closed).
4. Bus verdicts: capture B-seq1023/A-381 (before battery), complete-valid B-seq1025/A-383.

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261009T1600Z_cycle69/c69_session_slice.log --expect-sha edac7acc… --min-size 100`
2. `python3 tools/t12_battery_template.py --cycle 69 --evidence-dir evidence/groth16_ota_20261009T1600Z_cycle69 --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=edac7acc…, SETTLE_TRANSFER=cycle-69 OTA Groth16 proof edac7acc; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true, 5 CRC-OK burst)
- `c69_session_slice.log` — listener session segment (arm banner line 4231 → end)
- `groth16_payload_edac7acc.bin` / `rx_payload_128b.bin` — captured 128 B proof (SHA edac7acc…)
- `t12_cycle69_battery.log` — pairing battery (post-patch run; both pre-patch ABORTs disclosed in README)
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
- `capture_meta.json` — machine-written cycle metadata (declare seqs, battery, locator patch note)
- `chain_readback.json` — on-chain readback of the record PDA signature (fetched this turn)
