# groth16_ota cycle-86 — COMPLETE VALID A→B (35th valid cycle)

**Payload:** `d658351308ff621b406e46269697b346e4e3f144a9af2f0ed58b57c85838567e` (128 B, key-32, deposit 100001)
**Verdict:** PRIMARY VALID + CONTROLS VALID — radio 5/5 SHA MATCH (pre-wrap) + pairing VALID on B die; declare cross-bus byte-equal; machine-located; settle + chain-readback PASS.

## Chain of custody

| Step | Evidence |
|---|---|
| Window armed | `2026-10-12T00:06:07Z` (GATE PASS banner, 3rd session of chained standby log; gate PASS disk-counted) |
| Declared | B-bus seq **1280** / A-bus mirror seq **495**, `2026-10-12T00:59:03Z`, via `declare_rx_window.py v1.0` (tz-aware close 2026-10-12T02:06:07Z) |
| Alpha proof declare | `groth16_proof_tx` B **1282** == A **496** (+0.0 s), key-32, deposit 100001, watcher hot-path cache pop (FIFO: key-32 fired this cycle; key-34 81fd764b first-of-class remains in cache for a later cycle) |
| Fired | `groth16_tx_fired` 01:00:25Z, 5/5 TX_DONE — **82 s declare-to-fire** (10th consecutive 80 s-class) |
| Captured | 5/5 CRC-OK 128 B @ 903.9 MHz SF9, SNR 10.8–11.5 dB, count_us 3184875574..3252098262 (pre-wrap), walls **00:59:11Z..01:00:19Z** (machine-derived, origin = arm banner second) |
| SHA gate | 64/64 digest(captured) == declare |
| Battery | `t12_cycle86_battery.log` — run 2026-10-12T01:38:55Z, NORMAL mode (class scan: key-32 14 B-priors + 14 A-priors → NOT first-of-class, correct), GUARD-BEFORE/AFTER binary `a0c74748` PK `8dda8b79` VK `7bd5683f` unchanged, throttled=0x0, 41.3→44.3 °C. PRIMARY `d6583513` VALID 142.1 s + CONTROL-same c-70 `c300e5b4` (key-32) VALID 142.0 s + CONTROL-diff c-85 `4f3c0b19` (key-31) VALID 142.2 s |
| Settle | REGISTER TX `49829ksE…HYNSeb`, slot **510104591** (finalized), record PDA `FPJbsVpixtiogumAec9soXW71GusxyoFWThJ5iSPVmJq`, session `d658351308ff621b`, merkle root = proof SHA256, treasury +100,000 lamports, 6/6 tests |
| Chain-readback | `chain_readback.json` — signature byte-match on PDA (slot 510104591, err none), merkle-root bytes present in 103 B digest-only PDA data, decode-info scan NONE — **PASS** |

## Honest ledger

- **FIFO cache-pop disclosure:** the c-86 declare note predicted key-34 first-of-class
  (81fd764b) might fire; Alpha's watcher pops the cache FIFO, so key-32 d6583513
  (proof_2, built 21:07:40Z) fired this cycle. Key-34 remains WARM in his cache
  for a subsequent cycle — no misfire, ordinary pop order, disclosed for the record.
- The battery ran the corrected `tools/t12_battery_template.py` **from PR#48 head
  (158c0a5)** staged at `~/fleet/scripts/t12_battery_template_pr48_158c0a5.py`
  (sha256 92f312361f3fd1f2…) because the first-of-class/NORMAL class-scan
  remediation rides in that open PR and is not yet on main; the staged bytes are
  byte-identical to the PR branch copy (`git show 158c0a5:tools/t12_battery_template.py`).
  Merging PR#48 supersedes this staging — the template then lives in-tree.
- Pre-staged `rx_payload_128b.bin` was removed before battery launch (the template
  re-writes the bin from the extract JSON — a stale file is a hazard, not evidence).

## Reproduce

1. Extract: `python3 tools/b_rx_extract.py c86_session_slice.log --expect-sha d6583513…3867e --min-size 100`
2. Battery: `python3 tools/t12_battery_template.py --cycle 86 --evidence-dir evidence/groth16_ota_20261012T0059Z_cycle86 --guard-log ~/fleet/logs/rx_standby_continuous_20261011T200428Z.log`
3. Settle: `tsx app/src/settle_groth16_ota.ts` with `SETTLE_RX_BIN=this dir's rx_payload_128b.bin`, `SETTLE_EXPECT_SHA=d6583513…3867e`; chain-readback via `getSignaturesForAddress` on the record PDA.

## Files

- `c86_session_slice.log` — listener session slice (arm banner 00:06:07Z → close)
- `b_rx_extract_output.json` — machine parse, 5/5 SHA-matched
- `rx_payload_128b.bin` — captured 128 B proof, sha256 = declare
- `capture_meta.json` — machine-derived capture metadata
- `t12_cycle86_battery.log` + `t12_cycle86_battery_raw.log` — battery verdict + raw console
- `settle_run.log`, `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle artifacts
- `chain_readback.json` — independent chain-readback gate result
