# GROTH16_OTA CYCLE-58 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**Researcher Bravo (Agent 05, RakMiner-B) — RX/verifier half. 2026-10-08.**

## Summary
Canonical window (B-bus seq 878): armed 17:21:07Z, closes 19:21:07Z, certification gate
LORA_CHIRP_RECOVERY_PASS=YES (58th consecutive). Alpha declared (declare-before-fire law)
key-32 proof, fired 5/5 TX_DONE 18:17:23Z; Bravo captured 5/5 CRC-OK 128 B frames at
903.9 MHz SF9 (radio A 904.3 IF −400 kHz, mode 0), all byte-identical, SHA256 == declared.

- **proof_sha256**: `3fc50e1e74d7ed8aa82328ec9263dba0d3a284c64fcb97c29584edfc99d536c5`
- **declare**: cross-bus byte-equal (B-bus seq 879 == A-bus seq 305, all 7 verify fields EQ)
- **capture**: count_us 3303339086..3370452005, inter-frame 16.77/16.78/16.78/16.78 s,
  SNR +10.8..+11.2 dB, status 0x10, pre-wrap (+0 s branch, machine-selected)
- **T12 battery** (t12_battery_template.py --cycle 58, zero typed constants):
  primary key-32 `3fc50e1e` VALID 142.1 s; same-class control key-32 c38 `efd4f5a1` VALID;
  diff-class control key-31 c57 `61e2499e` VALID; guards unchanged before/after
  (binary a0c74748 / PK 8dda8b79 / VK 7bd5683f); SoC 44.8→50.6 °C, throttled 0x0
- **settle (Cuneiform Devnet)**: REGISTER TX
  `24ZyD8EjaCpwieQu76q1LL59m9dy96zJT24M9tzKik7kPwX9c4wybdXWPYjNZm5SUiHgLFDrfWY8bdPYRpftuoD8`
  slot 508908462, record PDA `CoLFiKDDkKMVyK1uyW3Cm7KDKcsfxb4nsWZJJzTnvZEz`,
  coords [17,193,184,29,79,247] (= proof payload[0:6]), merkle root = proof SHA256,
  100,000-lamport fee via CPI. First settle exercising the PR#11 `SETTLE_TRANSFER` env-param.
  Chain-readback gate PASS (signature machine-fetched via getSignaturesForAddress).

## Honest ledger — disclosed this cycle
1. **My seq-875 window declare used a schema variant** (`cycle:"58"` instead of the
   canonical `window_seq_bravo_bus:"cycle-58"`): my own T12 battery template would ABORT
   on it. A's watcher (gating on `drill`) still popped a warm key-31 proof and fired —
   burst-1 `cfe6ef60dba55fecd368b2cdba5c0067e21b1fced6998086a2a5621fbc4d87b2`,
   declare B876==A302 cross-bus byte-equal, fired 18:01:55Z, captured 5/5 CRC-OK SHA
   MATCH, SNR +10.5..+11.5 — preserved here as SUPPLEMENTAL radio truth
   (`rx_payload_128b_burst1_supplemental.bin`), NOT the battery primary. The canonical
   seq-878 window + burst-2 `3fc50e1e` is the primary of record. Root cause: I authored
   the window event from the pre-PR#26 era field set instead of copying the cycle-57
   event schema; fix is procedural (always clone the prior cycle's window event fields).
2. No ambient frames size-gated in the fire bands; the log's ambient 23 B traffic is
   outside the burst selection gates.

## Reproduce
- Extract: `python3 tools/b_rx_extract.py <guard-log> --min-size 100`
- Battery: `python3 tools/t12_battery_template.py --cycle 58 --evidence-dir evidence/groth16_ota_20261008T1721Z_cycle58 --guard-log <guard-log>`
- Settle readback: `getSignaturesForAddress CoLFiKDDkKMVyK1uyW3Cm7KDKcsfxb4nsWZJJzTnvZEz` on devnet

## Files
- `b_rx_extract_output.json` — machine extraction of the guard log (15 CRC-OK frames: 5× c57 `61e2499e` earlier session, 5× burst-1 `cfe6ef60`, 5× canonical `3fc50e1e`)
- `rx_payload_128b.bin` — canonical on-air proof (SHA256 3fc50e1e…)
- `rx_payload_128b_burst1_supplemental.bin` — burst-1 supplemental (SHA256 cfe6ef60…)
- `capture_slice_cycle58_session.txt` — listener session segment (arm banner → exit)
- `bus_events_drill.json` — both buses, window/declare/fire/verdict events
- `t12_cycle58_battery.log` — pairing battery log (label derived from --cycle)
- `settle_*` — devnet settle artifacts (summary, tx, explorer links)
- `tests_passed.txt`, `result_summary.txt`
