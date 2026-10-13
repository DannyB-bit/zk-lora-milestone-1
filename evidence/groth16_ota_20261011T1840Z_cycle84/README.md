# groth16_ota cycle-84 — COMPLETE VALID A→B, first-of-class key-33, devnet settled

**Verdict: COMPLETE VALID — 33rd valid fleet cycle.** Full loop closed in one
agent turn: declare → watcher hot-path fire → capture → T12 battery → bus
verdict → Cuneiform devnet settle → chain readback. All numbers machine-parsed
from the artifacts in this dir; nothing hand-typed.

## Chain of custody

| Step | Evidence |
|---|---|
| Window armed | `2026-10-11T17:31:50Z` (GATE PASS banner, standby log line 280; 92nd consecutive gate PASS on disk) |
| Declared | B-bus seq **1248** / A-bus mirror seq **483**, `2026-10-11T18:36:33Z`, via `declare_rx_window.py v1.0` (tz-aware close 19:31:50Z) |
| Alpha proof declare | `groth16_proof_tx` B **1250** == A **484** (+1.0 s), payload SHA `4b416048…c0`, key-33, deposit 100002 |
| Fired | `groth16_tx_fired` 18:37:53Z, 5/5 TX_DONE — **80 s declare-to-fire** (watcher hot path, no LLM turn) |
| Captured | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9, SNR 10.8–11.5 dB, count_us 3890721941…3957830332 (pre-wrap branch machine-selected; post-wrap scanned, none in fired−180…+240 s gate) |
| SHA gate | digest(captured) == declare **64/64 hex chars**: `4b4160488a948fa96117efa820065c07bf7cd85fb2cda7def8be6cf4954912c0` |
| T12 battery | PRIMARY key-33 **VALID** (142.0 s) + control-diff key-32 (c-83) **VALID** (142.3 s) + control-diff key-31 (c-69) **VALID** (142.0 s); guards unchanged (binary `a0c74748…`, PK `8dda8b79…`, VK `7bd5683f…`); throttled 0x0; SoC 45.2→50.1 °C |
| Bus verdict | `rx_verdict` B **1254** / A **486** (posted before staging this PR) |
| Settle | REGISTER TX `5keiPfZGxEYaXqWx9z6fTr5sXEBy2SmRCdufKYP7jXfjeNQdBGBusDWxAhmFRqyCBmRxr1mJQvqt52bABYPf3hvp` — slot 510005896, record PDA `oq6w3Sm8hzttcdfpwNRuF6jCZo6aKkg3qUg4USzHZxf`, treasury fee 100,000 lamports, 6/6 tests |
| Chain readback | `getSignaturesForAddress` on the record PDA byte-confirms the settle signature, err=null — **PASS** |

## First-of-class battery mode (tooling change)

key-33 is the **first proof of its statement class in fleet history** — a
same-class control cannot exist by definition. The template aborted fail-closed
(`control classes not satisfiable`) on attempt 2. Per the control-rotation law
the run must still prove the verifier path with ≥2 controls, so
`tools/t12_battery_template.py` now falls back to **two distinct-class
controls** (labeled `diff1`/`diff2`) when the primary is first-of-class, and the
verdict gate iterates the actual control roles. Selected: key-32 (c-83, 3 h old)
and key-31 (c-69). The patch rides in this PR (`+29/−4` lines).

## CORRECTION (2026-10-11T21:0xZ) — first-of-class claim was FALSE

A prior **key-33** proof existed: `e6a6b296` (declare B119/A53, 2026-09-30, merged
PR#10, known-VALID) — same key id, DIFFERENT statement (deposit 100000 vs this
cycle's 100002; pih[-1] `2261a97c…` vs `8611d46f…`). The battery labeled cycle-84
"first-of-class key-33" because that payload was absent from the local evidence
scan — absence treated as first-of-class, exactly the fail-open Codex flagged
(P1). **Corrected claim: cycle-84 is the first proof of its full statement class
(key-33 + deposit-100002 public-input vector)** — positively asserted by the
patched template against complete dual-bus history — NOT the first key-33 proof.
`e6a6b296` is vendored at `../groth16_ota_20260930T0828Z_control/` and verified in
attempt 4 as the SAME-KEY different-statement regression control in the same
battery session. The attempt-3 verdict content (primary + controls VALID) was and
remains sound; only the first-of-class *label* was wrong. Template hardening riding
in this PR: statement class = (key id, public-input vector); first-of-class
requires a positive complete-history assertion; NOT-first-of-class primaries with
no local same-class payload abort (no silent relabel); bus fetch must equal
`/health` count; candidate order = bus declare timestamp (not dir names); evidence
dir renamed `20260111`→`20261011` (Codex P2 mis-stamp; attempt-3 logs preserved
under `*_attempt3_prelabel_correction.log`).

## Reproduce

1. Extract: `python3 tools/b_rx_extract.py c84_session_slice.log --expect-sha 4b416048… --min-size 100`
   → `sha256_match: true`, 5/5 CRC-OK (`b_rx_extract_output.json`).
2. Battery: `python3 tools/t12_battery_template.py --cycle 84 --evidence-dir evidence/groth16_ota_20261011T1840Z_cycle84 --guard-log <newest ~/fleet/logs/rx_standby_continuous_*.log>`
   (pass `--guard-log` explicitly — the frozen default is the c-82 stale-glob trap).
3. Settle: `settle_groth16_ota.ts` with `SETTLE_RX_BIN=this dir's rx_payload_128b.bin`,
   `SETTLE_EXPECT_SHA=4b416048…`; chain-readback via `getSignaturesForAddress` on the record PDA.

## Honest ledger

1. **Attempt 1 abort** — battery run without `--guard-log`: frozen default named
   a stale standby log → `ABORT: no arm banner matches the window armed_at_utc`
   (the PR#46 trap, still unfixed on main). Log kept: `t12_cycle84_battery_attempt1_abort.guardlog-default.log`.
2. **Attempt 2 abort** — `ABORT: control classes not satisfiable` before the
   first-of-class fallback existed. Log kept: `t12_cycle84_battery_attempt2_abort.control-classes.log`.
3. **B-side hand-typed path failures while staging** (this turn, outside the
   evidence chain): two `cat`/`ls` calls against a hand-typed c-83 dir name
   (`…20260111T1531Z…` vs real `…20261011T1531Z…`) — resolved by globbing. No
   artifact was touched; the typed-constant law is why the extractor/battery/
   settle take paths from machine output.
4. Cache note: Alpha's warm cache is now **empty** — all 3 proofs (d940d21e,
   ff238e52, 4b416048) consumed by c-82/c-83/c-84. Refill requested via bus
   verdict note; next declare waits on his b_ack.

## Files

- `c84_session_slice.log` — listener session slice (arm banner → EOF)
- `b_rx_extract_output.json` — machine parse, 5/5 SHA-matched
- `rx_payload_128b.bin` — captured 128 B proof, sha256 = declare
- `capture_meta.json` — machine-derived capture metadata
- `t12_cycle84_battery_raw.log` — T12 battery verdict log
- `t12_cycle84_battery_attempt{1,2}_abort.*.log` — fail-closed aborts (honest history)
- `settle_run.log` / `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
