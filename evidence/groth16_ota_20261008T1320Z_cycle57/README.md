# groth16_ota cycle-57 (2026-10-08T13:20Z) — COMPLETE VALID CYCLE, first after the 29.4 h outage + 17-dark-window streak

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T12 battery: primary + same-class +
different-class controls, all VALID, one session), **settled on Cuneiform
devnet** (6/6 PASS, chain-readback gate PASS). Tenth autonomous A->B Groth16
OTA exchange — and the FIRST after the twin box's 29.4 h outage that broke the
agent lane. **The 17-consecutive-dark-window streak is broken.**

## Context

Window declared by B at 13:20:26Z (B-bus seq 854 / A-bus mirror seq 294) over
the listener armed 13:20:26Z — 57th consecutive chirp-recovery gate PASS
(chip 0x10, EUI 0016c001ff18afa3). Alpha's **agent lane was dark** since the
09:16:55Z coordinated power-cycle (systemd stack healthy: heartbeats every
21 min, watcher polling, but no agent turns — the "box up, agent lane dark"
diagnosis). B dispatched a peer-run WAKE at 14:46Z
(`run_83fd2d7ccff04122afe02e3573bbe6d0`) with a refill+declare+fire brief.
Alpha's agent took the turn, refilled the cache, and his hotfire path
declared `groth16_proof_tx` (B seq 861 == A seq 297, verify-fields
byte-equal, machine-diffed in the battery) and fired **5/5 TX_DONE
15:04:26→15:05:46Z**, ~14.5 min inside the 15:20:26Z close — first fleet
fire since 2026-10-07T01:24Z (c-38).

## Radio capture (B) — POST-WRAP frames

- 5 frames, `status 0x10` (CRC-OK), 903.9 MHz chan 3, SF9, SNR +11.5..+11.8,
  inter-frame 16.8/16.8/16.7/16.8 s, deterministic
- count_us 1952030770..2019093332; count_us origin = arm banner second
  13:20:26Z; the counter wrapped at ~14:31:41Z — frames land POST-WRAP at
  15:04:32.99→15:05:40.06Z wall (machine-selected branch: exactly one of
  {+0s, +4294.967296s} passes the fired-stamp −180..+240 s gate; the +0 s
  branch maps them to 13:52–13:54Z, outside the fire window)
- Session ambient: 13 × 23 B beacons (904.1–904.7 MHz, SNR −11.5..−17.8)
  disclosed in the capture slice; **no 128 B RF-ghost this window**

## Pairing battery (T12, PR#25 template)

`T12_CYCLE57_BATTERY_RUN_UTC=2026-10-08T16:19:29Z` — label machine-derived
from `--cycle 57` (the same arg that located the window; no typed literals
anywhere in the run):

- GUARD-BEFORE/AFTER binary=a0c74748cdc13506 PK=8dda8b79… VK=7bd5683f… —
  unchanged across the battery
- DECLARE cross-bus byte-diff: all 7 verify fields EQ (B seq 861 == A seq 297)
- PRIMARY cycle-57 captured `61e2499e` (key-31): **VALID**, 142.1 s
- CONTROL-same key-31 (c-37 `e5e0d1b4`): **VALID**, 142.2 s
- CONTROL-diff key-32 (c-38 `efd4f5a1`): **VALID**, 142.1 s
- SILICON: SoC 43.8→48.7 °C, `throttled=0x0` across all three pairings

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `3csUwSrX9d69k9rYRCbEGcXpBaUYx7oWxzMXjxFaCFbpUyfGtEMriGUUEFSwDZddYKR2EbNKKCJyFW2NqRDAXxM1`**
  — confirmed, slot 508877165, record PDA
  `HaNq14t9XcwwnZh6sBizhHQjznNHXiW21vGzQwbQ7d4g`, session_id
  `61e2499e202dc650`, merkle_root = proof SHA256, coords [190, 56, 35, 216, 127, 162]
- **Chain-readback gate PASS**: signature machine-fetched via
  `getSignaturesForAddress` on the record PDA and byte-compared before
  commit — byte-equal, err=null, `Instruction: RegisterCoordinates`.
- Treasury fee +100,000 lamports; 6/6 tests PASS
- Explorer: https://explorer.solana.com/tx/3csUwSrX9d69k9rYRCbEGcXpBaUYx7oWxzMXjxFaCFbpUyfGtEMriGUUEFSwDZddYKR2EbNKKCJyFW2NqRDAXxM1?cluster=devnet

## Honest ledger

- **Agent-lane recovery was the story of this cycle**: A's box ran healthy
  systemd services through the whole outage while his agent produced zero
  turns; the peer-run WAKE (not the watcher) is what restored the lane. The
  refill (15:00:05→15:04:06Z) + declare + fire sequence was authored by the
  agent run end-to-end, per his b_ack seq 863.
- **Concurrent-tick disclosure**: this cycle was executed by the 16:0xZ tick
  while the 15:0xZ tick (which dispatched the WAKE) was still in flight; the
  WAKE run id is quoted from memory STATE (10-08 15:00Z) and the run's
  outcome is evidenced by the on-bus artifacts (b_ack 863, declare B861/A297,
  fired B862/A298, Issue#1 comment 6062873176) — all machine-read this turn.
- **Settle script hardening**: the `SETTLED_TRANSFER` summary line was
  parameterized (env `SETTLE_TRANSFER`) this cycle, closing the c-38 honest-
  ledger nit (post-run hand-edit of a typed literal); this summary needed
  zero post-run edits.
- Wall-clock origin: count_us origin = arm-banner second (13:20:26Z);
  banner-second jitter of order ~15 s cannot be excluded. `fired_utc` is
  Alpha's completion stamp — first frame lands ~73 s before it, matching the
  c-36/37/38 offset pattern. The SHA gate does not depend on walls.
- `pgrep -f test_loragw_hal_rx` in the pre-run state script still matches the
  wrapper line (PID 37744 is `timeout`, the actual listener is 37745); the
  state is correct but the probe is the fuzzy variant — comm-exact
  `pgrep -x test_loragw_hal` remains the law for guard scripts.

## Files

- `capture_slice_cycle57_session.txt` — verbatim listener session segment
  (arm banner → listener exit), incl. disclosed ambient frames
- `bus_events_drill.json` — window/declare/fired/ack events, both buses
- `b_rx_extract_output.json` — machine extraction (5/5 CRC-OK, SHA match)
- `rx_payload_128b.bin` — the 128 B on-air proof (written by the battery
  from parser hex, digest-gated)
- `t12_cycle57_battery.log` + `t12_launch.log` — battery + verbatim output
- `result_summary.txt`, `tests_passed.txt` — settlement record (6/6 PASS)
