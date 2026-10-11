# groth16_ota cycle-85 — COMPLETE VALID A→B (34th valid cycle), NORMAL-mode first live run

**Payload:** `4f3c0b1906cf35769eae387a5b50802de951013c9e1c91dfde9247e76b0f8323` (128 B, key-31, deposit 100000)
**Verdict:** PRIMARY VALID + CONTROLS VALID — radio 5/5 SHA MATCH (pre-wrap) + pairing VALID on B die; declare cross-bus byte-equal; machine-located; settle + chain-readback PASS.

## Chain of custody

| Step | Evidence |
|---|---|
| Window armed | `2026-10-11T22:05:47Z` (GATE PASS banner; 95th consecutive gate PASS, disk-counted) |
| Declared | B-bus seq **1269** / A-bus mirror seq **490**, `2026-10-11T23:02:35Z`, via `declare_rx_window.py v1.0` (tz-aware close 2026-10-12T00:05:47Z) |
| Alpha proof declare | `groth16_proof_tx` B **1271** == A **491** (+1.0 s), key-31, deposit 100000, watcher hot-path cache pop |
| Fired | `groth16_tx_fired` 23:03:57Z, 5/5 TX_DONE — **82 s declare-to-fire** (9th consecutive 80 s-class) |
| Captured | 5/5 CRC-OK 128 B @ 903.9 MHz SF9, SNR 10.8–11.0 dB, count_us 3416942877..3484013915 (pre-wrap), walls **23:02:43Z..23:03:51Z** (machine-derived, origin = arm banner second) |
| SHA gate | 64/64 digest(captured) == declare |
| Battery | `t12_cycle85_battery.log` — run 2026-10-11T23:08:18Z, GUARD-BEFORE/AFTER binary `a0c74748` PK `8dda8b79` VK `7bd5683f` unchanged, throttled=0x0, 45.2→48.7 °C |
| Settle | REGISTER TX `3k9Dky4v…dbK3`, slot **510065722**, record PDA `DELQUFTYJnLWQhVPsmmzgWcdQYz5un8G9z3ryRL6tWVx`, treasury +100,000 lamports, 6/6 tests |
| Chain-readback | `chain_readback.json` — signature byte-match on PDA, merkle-root bytes present in on-chain PDA data (103 B digest-only, ZK-lawful) — **PASS** |

## NORMAL-mode first live run (corrected template)

This cycle is the first live run of the corrected `tools/t12_battery_template.py`
(Codex P1/P2 remediation, riding in PR#48 `158c0a5`):

- **CLASS SCAN (complete dual-bus history):** key-31/deposit-100000 — 25 B-priors +
  26 A-priors + 26/28 pih-only priors + 5 unclassable declares → **NOT first-of-class**;
  the battery correctly engaged NORMAL mode (no silent relabel).
- **CONTROL-same:** c-69 `edac7acc` (key-31, SAME statement-class, machine-picked by
  declare timestamp) — VALID 142.0 s.
- **CONTROL-diff:** c-84 `4b416048` (key-33, DIFFERENT statement-class) — VALID 142.4 s.
- Primary `4f3c0b19` VALID 142.3 s.

## Honest ledger

- **Attempt 1 abort**: battery launched before the extract JSON was staged — aborted
  at the fail-closed extraction gate (13 s, no pairing spent). Honest history.
- **capture_meta.json correction (hand-typed-constant law instance #7):** the
  `capture_utc_range` was initially derived from the fired-completion stamp instead of
  serialized from the parse (23:03:57..23:05:04Z vs machine-derived 23:02:43..23:03:51Z);
  rewritten programmatically from `b_rx_extract_output.json` + battery origin line before commit.
- Both fleet boxes took uncommanded power-loss-class reboots today (B ~16:04 UTC local /
  A bus server_boot 20:01:43Z; B earlier at 14:40Z wave). Both standby guards
  auto-recovered; Alpha's post-reboot verify (watcher ACTIVE, since-pointer current)
  is in his b_ack A489/B1263.

## Reproduce

1. Extract: `python3 tools/b_rx_extract.py c85_session_slice.log --expect-sha 4f3c0b19…2323 --min-size 100`
2. Battery: `python3 tools/t12_battery_template.py --cycle 85 --evidence-dir evidence/groth16_ota_20261011T2302Z_cycle85 --guard-log <newest ~/fleet/logs/rx_standby_continuous_*.log>`
3. Settle: `tsx app/src/settle_groth16_ota.ts` with `SETTLE_RX_BIN=this dir's rx_payload_128b.bin`, `SETTLE_EXPECT_SHA=4f3c0b19…2323`; chain-readback via `getSignaturesForAddress` on the record PDA.

## Files

- `c85_session_slice.log` — listener session slice (arm banner 22:05:47Z → live tail)
- `b_rx_extract_output.json` — machine parse, 5/5 SHA-matched
- `rx_payload_128b.bin` — captured 128 B proof, sha256 = declare
- `capture_meta.json` — machine-derived capture metadata (walls machine-serialized)
- `t12_cycle85_battery.log` + `t12_cycle85_battery_raw.log` — battery verdict + raw console
- `settle_run.log`, `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle artifacts
- `chain_readback.json` — independent chain-readback gate result (PASS)

[B-SYNC] B RX-HOT — c-85 COMPLETE VALID + settled (34th valid cycle), NORMAL-mode first live run PASS; c-84 label corrected to first-of-statement-class; PR#48 remediation pushed; next: key-34 first-of-class cycle.
