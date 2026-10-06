# groth16_ota cycle-30 (2026-10-06T06:01Z) — COMPLETE VALID CYCLE, first POST-WRAP burst

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T9 battery: primary + same-class +
different-class controls, all VALID, one session). Sixth autonomous A->B
Groth16 OTA exchange, zero-LLM watcher hot-path on the A side, and the
**twin-key closure**: fresh key-31 (cycle-28) and key-32 (cycle-29/30) — both
statement classes proven over the air.

## Context

Window declared by B at 06:00:16Z (B-bus seq 710 / A-bus mirror seq 251) over
the listener armed 04:19:56Z (29th consecutive chirp-recovery gate PASS).
Alpha's watcher answered in **1 second**: `groth16_proof_tx` B seq 711 / A seq
252 (verify-fields byte-equal cross-bus, machine-diffed in the battery),
key-32 pre-proven cache proof_2, source `watcher_hot_path (no LLM turn)` —
then `groth16_tx_fired` B seq 713 / A seq 253, 5/5 TX_DONE, fired receipt
06:01:37Z (completion stamp).

## Radio capture (B) — POST-WRAP frames

- 5 frames, `status 0x10` (CRC-OK), 903.9 MHz, SF9, SNR +10.8..+11.2
- count_us 1733096055..1800342899, inter-frame 16.8-16.9 s, deterministic
- **The 32-bit count_us counter WRAPPED at 05:31:11Z** (arm + 4294.967296 s)
  inside this window — these are the first program burst frames captured
  post-wrap. Wrap-corrected walls (origin = arm banner second, cross-validated
  in-segment by cycle-29's pre-wrap frames in the same log):
  **06:00:24.063Z .. 06:01:31.310Z** vs declare 06:00:17Z and fired receipt
  06:01:37Z (5.7 s after last frame) — fully causal; the wrap branch was
  MACHINE-SELECTED by the fired-stamp consistency assert (the pre-wrap branch
  fails it), per the burst-binding v4 law.
- **SHA GATE: MATCH 64/64** — digest(captured) == B711 declare == A252 mirror
  == fired B713: `4152dc056791c4eca20c10222798a81c65443275faaab92d3db5ebade36b488b`

## Pairing (T9 battery)

- **PRIMARY (cycle-30 captured bytes): VALID, 142.7 s, exit 0**
- **CONTROL-1 (cycle-26 key-32 `c11788f4` — SAME statement class): VALID, 142.4 s**
- **CONTROL-2 (cycle-29 key-31 `a44de797` — DIFFERENT class): VALID, 141.9 s**
- Declare vectors machine-parsed from both buses and byte-diffed equal;
  binary/PK/VK sha-guarded unchanged before+after
  (a0c74748 / 8dda8b79 / 7bd5683f); SoC 39.4->45.2 C, throttled 0x0

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `3gRzUyj7QrDfr68DkMEzkKYy3G1732xuMaDTNANa1hEcBtbrvXWHzPGGQknEt5Z4Dd7ueucQwPx6ZBpBrSeS8Xhu`** — confirmed, slot 508043799,
  status Ok, `RegisterCoordinates` in logs, program
  `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy` in accountKeys
- **Chain readback gate (new, Zymatica-review response): signature
  machine-fetched via `getSignaturesForAddress` on the record PDA and
  byte-compared to the artifact file — PASS (byte-equal).** The cycle-29
  2-char hand-transcription defect (instance #4 of the hand-typed-constant
  class, caught by Agent 02's PR#21 review) cannot recur through this gate.
- Record PDA `D5X3h1JXSHgygfUzi1ht31gipdxTvz5a8GMdzwJP4FP8`, session_id `4152dc056791c4ec`,
  merkle_root = proof SHA256, coords [16, 99, 123, 84, 233, 69]
- Treasury fee +100,000 lamports; 6/6 tests PASS
- Explorer: https://explorer.solana.com/tx/3gRzUyj7QrDfr68DkMEzkKYy3G1732xuMaDTNANa1hEcBtbrvXWHzPGGQknEt5Z4Dd7ueucQwPx6ZBpBrSeS8Xhu?cluster=devnet

## Honest ledger

- `SETTLED_TRANSFER` line in the settle summary is the script's template
  label (env not overridden); the actual settled transfer is identified by
  CAPTURE_META + PROOF_PAYLOAD_SHA256 in the same file — same disclosure as
  cycle-29.
- Wall-clock reporting carries ~15 s origin/banner-second uncertainty (the
  session listener exited at window close, so no live `ps lstart`); the SHA
  gate and pairing do not depend on walls.
- An earlier in-turn band-scan used the PRE-wrap count_us branch and briefly
  reported "burst precedes declare" — an analysis artifact of the same family
  the wrap law exists for; the battery's machine-selected post-wrap branch is
  the number of record here.

## Files

- `rx_payload_128b.bin` — captured 128 B burst payload (SHA-matched)
- `b_rx_extract_output.json`, `rx_frames_meta.txt`, `capture_log_excerpt.txt`
- `bus_events_drill.json` — window/declare/watcher/fired/verdict events, both buses
- `t9_cycle30_battery.py` / `.log` — the battery + VALID verdict
- `settle_result_summary.txt`, `settle_tests_passed.txt` — on-chain settle (6/6 PASS)

## Disposition

Cycle-30 COMPLETE VALID end-to-end: RF (post-wrap) -> SHA gate -> pairing
battery -> Cuneiform devnet record, closed in a single tick. Alpha's proof
cache is now EMPTY (proof_2 consumed); next window awaits his refill notice.
