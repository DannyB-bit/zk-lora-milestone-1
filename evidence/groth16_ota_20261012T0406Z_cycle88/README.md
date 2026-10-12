# groth16_ota cycle-88 — COMPLETE VALID A→B (37th valid cycle) — **first key-34 in fleet history**

**Payload:** `81fd764bddb87b7a1bf4e9177690706ce0b2c37dcd40449a843ffc00ada0d1e2` (128 B, key-34, deposit 100003)
**Verdict:** PRIMARY VALID + 2 DISTINCT-CLASS CONTROLS VALID — radio 5/5 SHA MATCH (post-wrap) + pairing VALID on B die; declare cross-bus byte-equal; machine-located; FIRST-OF-CLASS positively asserted (key-34 priors B=0 A=0); settle + chain-readback PASS.

## Chain of custody

| Step | Evidence |
|---|---|
| Window armed | `2026-10-12T04:06:48Z` (GATE PASS banner, 5th session of chained standby log `rx_standby_continuous_20261011T200428Z.log`; `LORA_CHIRP_RECOVERY_PASS=YES`, chip_id rc=0, version reg 0x10 v1.0) |
| Declared | B-bus seq **1306** / A-bus mirror seq **506**, `2026-10-12T05:19:27Z`, via `declare_rx_window.py v1.0` (tz-aware close 2026-10-12T06:06:48Z; cert: 5 gate-PASS events in log, listener PID 54049 skew 1.0 s, 2841 s remaining at declare) |
| Alpha proof declare | `groth16_proof_tx` B **1308** == A **507** (byte-equal, cross-bus diff PASS), key-34 deposit 100003, ts 05:19:27Z, watcher hot-path cache pop (FIFO 4th and final: 4f3c0b19→c-85, d6583513→c-86, e703bfd3→c-87, **81fd764b→c-88**) |
| Fired | `groth16_tx_fired` 05:20:47Z, 5/5 TX_DONE — **80 s declare-to-fire (12th consecutive 80s-class)** |
| Captured | 5/5 CRC-OK 128 B @ 903.9 MHz SF9, SNR +10.8..+11.0 dB, count_us 71769682..138986555 (**post-wrap**), walls **05:19:34.7Z..05:20:41.9Z** (machine-derived, origin = arm banner second 04:06:48Z + 4294.967296 s) |
| SHA gate | 64/64 digest(captured) == declare |
| Battery | `t12_cycle88_battery.log` — run 2026-10-12T05:36:48Z, **FIRST-OF-CLASS mode (positively asserted)** (class scan over complete dual-bus history: key-34 priors B=0 A=0, pih-only B=0 A=0, 5 unclassable declares correctly excluded; 2 DISTINCT-statement-class controls required and satisfied), GUARD-BEFORE/AFTER binary `a0c74748` PK `8dda8b79` VK `7bd5683f` unchanged, throttled=0x0, 43.3→48.2 °C. PRIMARY `81fd764b` VALID 142.1 s + CONTROL-diff1 c-87 `e703bfd3` (key-33) VALID 141.8 s + CONTROL-diff2 c-70 `c300e5b4` (key-32) VALID 142.1 s |
| Settle | REGISTER TX `5Y4WwE8B…nJnYn`, slot **510165159** (err none), record PDA `FwYNmw6KF3wA9s3JAqDKUDzZTChmnGYRdCufMGvd4upR`, session `81fd764bddb87b7a`, merkle root = proof SHA256, coords = payload[0:6]=[158,104,62,58,18,133], treasury +100,000 lamports, 6/6 tests |
| Chain-readback | `chain_readback.json` — signature byte-match on PDA (slot 510165159, err none, blockTime 05:55:32Z), root present in 103 B digest-only PDA data, decode-info scan NONE — **PASS** |

## Honest ledger

- **FIRST-OF-CLASS, positively asserted (PR#48's corrected discipline, first live assertion):** this is the
  first key-34 statement ever declared in fleet history. The T12 class scan over the COMPLETE dual-bus
  history found zero prior key-34 declares (B=0, A=0), zero pih-only priors, and correctly excluded 5
  unclassable declares (no key id) from enabling the claim — exactly the Codex-P1-corrected rule set:
  first-of-class requires zero prior declares of that class, absence-of-evidence is never first-of-class,
  and the assertion is logged distinctly from pih-only claims. The battery then required and ran
  **2 DISTINCT-statement-class controls** — c-87 `e703bfd3` (key-33) VALID and c-70 `c300e5b4`
  (key-32) VALID — the first live satisfaction of the PR#48 FIRST-OF branch. No vendoring was needed:
  both control payloads sit in main-tree evidence dirs.
- **Two hollow bus posts (B1311/A509), corrected same-turn:** my first `rx_verdict` post attempt passed
  a JSON *string* to `post_event.post()` (which takes a dict), so the events landed with empty `data`.
  Detected by readback within the same turn; corrected by re-posting the full verdict (B1312/A510, fields
  readback-verified). Hollow seqs remain in the bus history as honest artifacts of the mistake.
  Lesson recorded: `post(url, type, data_dict)` — never `json.dumps` the payload when calling the
  Python API directly.
- **FIFO cache-pop disclosure:** Alpha's watcher pops the prover cache in FIFO order (refill at
  21:11:41Z, 4 proofs). Cycle-88 consumed the 4th and final warm proof — **Alpha's cache is now EMPTY**;
  a c-89 declare would draw nothing without a refill. Refill ask carried to Alpha in the bus verdict.

## Reproduce

1. Extract: `python3 tools/b_rx_extract.py c88_session_slice.log --expect-sha 81fd764b…a0d1e2 --min-size 100`
2. Battery: `python3 evidence/groth16_ota_20261012T0206Z_cycle87/t12_battery_template_PR48head_158c0a5.py --cycle 88 --evidence-dir evidence/groth16_ota_20261012T0406Z_cycle88 --guard-log ~/fleet/logs/rx_standby_continuous_20261011T200428Z.log` (or the in-tree template once PR#48 merges)
3. Settle: `bash ~/fleet/scripts/settle_cycle88.sh` (SHA + meta machine-parsed from extract/capture_meta, fail-closed); chain-readback via `getSignaturesForAddress` on the record PDA.

## Files

- `c88_session_slice.log` — listener session slice (arm banner 04:06:48Z → present)
- `b_rx_extract_output.json` — machine parse, 5/5 SHA-matched
- `rx_payload_128b.bin` — captured 128 B proof, sha256 = declare
- `capture_meta.json` — machine-derived capture metadata (post-wrap walls)
- `t12_cycle88_battery.log` — FIRST-OF-CLASS battery verdict
- `t12_cycle88_battery_raw.log` — raw console (empty: clean run)
- `bus_events_c88.json` — c-88 bus events (declare/fired both buses, machine-fetched, cross-bus byte-equal)
- `settle artifacts` — staged by settle_cycle88.sh into cuneiform-m1 app dir (groth16_ota_settlement_20261012T0406Z_cycle88) — copy staged below
- `chain_readback.json` — independent chain-readback gate result (PASS)

## Status

37th valid cycle. First key-34 in fleet history — first-of-class positively asserted, verified by
2 distinct-class controls, settled digest-only on Cuneiform devnet. [B-SYNC] cycle-88 COMPLETE
VALID settled; first-of-class asserted; next: Alpha cache refill for c-89.
