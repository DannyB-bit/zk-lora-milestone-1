# groth16_ota cycle-87 — COMPLETE VALID A→B (36th valid cycle)

**Payload:** `e703bfd384a2f1d4ca480e8c5fa3702d1a9a526d1319a529678dfe1e0cfd0d24` (128 B, key-33, deposit 100002)
**Verdict:** PRIMARY VALID + CONTROLS VALID — radio 5/5 SHA MATCH (post-wrap) + pairing VALID on B die; declare cross-bus byte-equal; machine-located; settle + chain-readback PASS.

## Chain of custody

| Step | Evidence |
|---|---|
| Window armed | `2026-10-12T02:06:27Z` (GATE PASS banner, 4th session of chained standby log `rx_standby_continuous_20261011T200428Z.log`; `LORA_CHIRP_RECOVERY_PASS=YES`, chip_id rc=0, version reg 0x10 v1.0) |
| Declared | B-bus seq **1293** / A-bus mirror seq **500**, `2026-10-12T03:12:5xZ`, via `declare_rx_window.py v1.0` (tz-aware close 2026-10-12T04:06:27Z; cert: 4 gate-PASS events in log, listener PID 41086 skew 0.0 s, 2893 s remaining at declare) |
| Alpha proof declare | `groth16_proof_tx` B **1294** == A **501** (byte-equal, cross-bus diff PASS), key-33 deposit 100002, ts 03:18:15Z, watcher hot-path cache pop (FIFO 3rd: 4f3c0b19→c-85, d6583513→c-86, e703bfd3→c-87; key-34 81fd764b first-of-class remains WARM for c-88) |
| Fired | `groth16_tx_fired` 03:19:35Z, 5/5 TX_DONE — **80 s declare-to-fire (11th consecutive 80s-class)** |
| Captured | 5/5 CRC-OK 128 B @ 903.9 MHz SF9, SNR +10.5..+11.0 dB, count_us 19661820..87013145 (**post-wrap**), walls **03:18:21Z..03:19:28Z** (machine-derived, origin = arm banner second 02:06:27Z + 4294.967296 s) |
| SHA gate | 64/64 digest(captured) == declare |
| Battery | `t12_cycle87_battery.log` — run 2026-10-12T03:38:13Z, **NORMAL mode** (class scan: key-33 pih vector, priors B1250/A484 → NOT first-of-class, correct), GUARD-BEFORE/AFTER binary `a0c74748` PK `8dda8b79` VK `7bd5683f` unchanged, throttled=0x0, 42.8→47.2 °C. PRIMARY `e703bfd3` VALID 142.1 s + CONTROL-same c-84 `4b416048` (key-33, **vendored**, see below) VALID 142.1 s + CONTROL-diff c-86 `d6583513` (key-32) VALID 142.0 s |
| Settle | REGISTER TX `5Xi8tY3B…GRTsc`, slot **510133828** (err none), record PDA `8taRSCF7VmPM9djaPqsNDMN5tCvtDPs7eRvAwcS528A8`, session `e703bfd384a2f1d4`, merkle root = proof SHA256, coords = payload[0:6]=[152,37,178,86,202,45], treasury +100,000 lamports, 6/6 tests |
| Chain-readback | `chain_readback.json` — signature byte-match on PDA (slot 510133828, err none, blockTime 03:50:47Z), root present in 105 B digest-only PDA data, decode-info scan NONE — **PASS** |

## Honest ledger

- **Fail-closed abort → vendored same-class control (first occurrence of the template's
  own recovery path, live):** attempt 1 ABORTED (`t12_cycle87_battery_attempt1_abort.no-local-sameclass-control.log`)
  because the prior same-statement-class payload (c-84 `4b416048`, declare B1250/A484)
  lives on open PR#48's branch, not on main. Per the template's instruction and the
  c-84 precedent (e6a6b296 vendored from origin/main PR#10 blob), the payload was
  vendored byte-exact from `158c0a52` (`git show 158c0a52:evidence/groth16_ota_20261011T1840Z_cycle84/rx_payload_128b.bin`),
  provenance in `evidence/groth16_ota_20261011T1840Z_cycle84/VENDORED_PROVENANCE.md`,
  sha256 verified `4b4160488a948fa96117efa820065c07bf7cd85fb2cda7def8be6cf4954912c0`
  before re-run. The battery then ran NORMAL mode with the vendored control VALID.
  This is exactly the discipline PR#48 enforces: absence of evidence is never
  first-of-class, and a NOT-first-of-class primary never silently relabels.
- **FIFO cache-pop disclosure:** Alpha's watcher pops the cache FIFO; proof_3 (e703bfd3,
  key-33) fired this cycle. Key-34 `81fd764b` — the true first-of-class — remains WARM
  in his cache for c-88, where PR#48's FIRST-OF branch gets its first live assertion.
- **Battery template provenance:** the run used the corrected template staged from
  PR#48 head (`158c0a5`), because the first-of-class/NORMAL class-scan remediation is
  not yet on main. Same disclosure as c-85/c-86. Merging PR#48 supersedes the staging.
- **Wrap branch:** POST-WRAP machine-selected by the battery's fired-stamp gate
  (exactly one branch satisfies fired −180..+240 s); walls causal with the declare
  (first frame 03:18:21Z vs declare 03:18:15Z).

## Reproduce

1. Extract: `python3 tools/b_rx_extract.py c87_session_slice.log --expect-sha e703bfd3…f0d24 --min-size 100`
2. Battery: `python3 t12_battery_template_PR48head_158c0a5.py --cycle 87 --evidence-dir <this dir> --guard-log ~/fleet/logs/rx_standby_continuous_20261011T200428Z.log` (or the in-tree template once PR#48 merges)
3. Settle: `bash ~/fleet/scripts/settle_cycle87.sh` (SHA + meta machine-parsed from extract/capture_meta, fail-closed); chain-readback via `getSignaturesForAddress` on the record PDA.

## Files

- `c87_session_slice.log` — listener session slice (arm banner 02:06:27Z → present)
- `b_rx_extract_output.json` — machine parse, 5/5 SHA-matched
- `rx_payload_128b.bin` — captured 128 B proof, sha256 = declare
- `capture_meta.json` — machine-derived capture metadata (post-wrap walls)
- `t12_battery_template_PR48head_158c0a5.py` — staged template (git show 158c0a52:tools/t12_battery_template.py)
- `t12_cycle87_battery_attempt1_abort.no-local-sameclass-control.log` — fail-closed abort, honest history
- `t12_cycle87_battery.log` + `t12_cycle87_battery_raw.log` — battery verdict + raw console
- `bus_events_c87.json` — c-87 bus events (declare/fired both buses, machine-fetched)
- `settle_run.log`, `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle artifacts
- `chain_readback.json` — independent chain-readback gate result
