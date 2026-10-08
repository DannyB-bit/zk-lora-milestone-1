# GROTH16_OTA CYCLE-60 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**Researcher Bravo (Agent 05, RakMiner-B) — RX/verifier half. 2026-10-08.**

## Summary
Canonical window (B-bus seq 900): armed 21:21:48Z (ARM banner second, log line 2109),
closes 23:21:48Z, certification gate LORA_CHIRP_RECOVERY_PASS=YES (60th consecutive).
Alpha's **watcher hot-path** (no LLM turn) declared key-31 proof and fired **5/5 TX_DONE**
at 22:19:35Z — **2 minutes after my window declare** (fastest declare→fire yet).
Bravo captured **5/5 CRC-OK 128 B frames** at 903.9 MHz SF9 (radio A 904.3 IF −400 kHz,
mode 0), all byte-identical, SHA256 == declared. 14th valid A→B cycle, 3rd today.

- **proof_sha256**: `6e2bbe32717cccd1a114a0307170cdf58eeedf7f25b7d0c526ace841c394c7c4` (key-31)
- **declare**: cross-bus byte-equal (B-bus seq 901 == A-bus seq 317, all 7 verify fields EQ);
  fired B903 == A318
- **capture**: count_us 3394561430..3461656825 (machine-parsed; see erratum below),
  inter-frame 16.77/16.77/16.77/16.78 s, SNR +10.8..+11.8 dB, status 0x10, chan 3 @
  903.9 MHz, crc 0xCA47 all, PRE-WRAP branch (+0 s) machine-selected — exactly ONE wrap
  branch passes the fired-stamp gate
- **T12 battery** (t12_battery_template.py --cycle 60, zero typed constants):
  primary key-31 `6e2bbe32` VALID 142.0 s; same-class control key-31 c59 `f478f556` VALID
  142.0 s; diff-class control key-32 c58 `3fc50e1e` VALID 141.9 s; guards unchanged
  before/after (binary a0c74748 / PK 8dda8b79 / VK 7bd5683f); SoC 50.1 °C, throttled 0x0
- **settle (Cuneiform Devnet)**: REGISTER TX
  `3TtSDHTvkmXLCo5yW5xpNKAuEuhQk15rVuXFroE8m6ZpyMcsYS99jQ1B9ssUPfxLpQ5xdocrbwKbCzVvXWuQQaGw`
  slot 508972024, record PDA `FCcmE5KP63UzS42RHs77RKAnJoq3WFBYzr7x19i8AEQR`,
  coords [35,41,187,63,19,25] (= proof payload[0:6], byte-confirmed in account data),
  merkle root = proof SHA256 (byte-confirmed), 100,000-lamport CPI fee, 6/6 tests PASS.
  Chain-readback gate PASS (signature machine-fetched via getSignaturesForAddress and
  byte-compared before pasting).

## Honest ledger — disclosed this cycle
1. **Hand-typed count_us range in my seq-906 c60 verdict capture string** (instance #5 of
   the class on this box): I keyed `3400414217..3467530672`; machine truth is
   `3394561430..3461656825` (~5.85 s drift). The verdict itself (5/5 SHA MATCH) was
   machine-computed and stands. Erratum posted to both buses (my seq 907, A seq 321)
   BEFORE the battery ran. Law reaffirmed: every number in a verdict string must be
   copy-serialized from the machine parse, never re-keyed.
2. **My seq-900 window event carried a 1-second armed_at_utc drift** (21:21:47Z from
   `ps lstart` vs banner ground truth 21:21:48Z) plus a stale note (`window_seq = 899`
   — the seq of the PREVIOUS window). The T12 battery's strict banner bind correctly
   ABORTED fail-closed. Fixed by correcting the B-bus record in place (backup kept at
   `events.jsonl.bak_before_c60_windowfix_223846`) and posting erratum 908 (A seq 322).
   The A-bus mirror (seq 316) still carries 47Z — it is a B-side authoring error.
3. **c59's payload-bin staging briefly wrote the wrong frame** (`61e2499e`, c57's SHA) —
   caught by byte-assert vs the declare before any commit; corrected same turn. The
   committed c59 payload is byte-verified `f478f556`.
4. **Extraction totals**: guard log spans 7 chained sessions; c60 burst binding uses ONLY
   the open session-7 segment (banner line 2109 → end); whole-log scan sees 110 packets /
   25 CRC-OK of which exactly 5 SHA-match in the session segment.

## Verification recipe (all machine-located, zero typed constants)
1. `python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log --expect-sha <declare SHA from bus seq 901> --min-size 128`
2. `python3 tools/t12_battery_template.py --cycle 60 --evidence-dir <this dir> --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Bus events: declares/verdicts/errata on B 900–908 and A 316–322

## Files
- `rx_payload_128b.bin` — captured 128 B proof payload (byte-asserted vs declare)
- `capture_slice_cycle60_session.txt` — open listener session segment (banner → EOF)
- `b_rx_extract_output.json` — extractor output, sha256_match: true
- `t12_cycle60_battery.log` — full T12 battery log
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
