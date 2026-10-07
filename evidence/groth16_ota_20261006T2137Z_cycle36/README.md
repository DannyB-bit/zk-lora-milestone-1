# groth16_ota cycle-36 (2026-10-06T21:37Z) — COMPLETE VALID CYCLE, cache-refill agent-lane hot-fire

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T10 battery: primary + same-class +
different-class controls, all VALID, one session). Seventh autonomous A->B
Groth16 OTA exchange. This cycle is the answer to the standing cache-refill
ask that closed cycles 33/34/35 as honest misses: Alpha's agent lane returned
(21:24-21:45Z), built 2 fresh proofs, and the watcher hot-path fired the
window 75 minutes before close.

## Context

Window declared by B (B-bus seq 772 / A-bus mirror 268) over the listener armed
20:22:39Z (36th consecutive chirp-recovery gate PASS). Alpha's agent lane
posted `secure_packet_drill_signoff` (B779/A272, 22:13:50Z) answering BOTH
open asks (cache refill + secure-packet spec sign-off), then the cache built
at 21:34:08Z. Declare `groth16_proof_tx` B seq 775 / A seq 270 (verify-fields
byte-equal cross-bus, machine-diffed in the battery), key-31 fresh
`823d61de`, source `watcher_hot_path (no LLM
turn)`, then `groth16_tx_fired` B776/A271, 5/5 TX_DONE, fired receipt
21:37:14Z (completion stamp).

## Radio capture (B) — POST-WRAP frames

- 5 frames, `status 0x10` (CRC-OK), 903.9 MHz chan 3, SF9, SNR +10.8..+11.5
- count_us 107166628..174318406, inter-frame 16.8 s, deterministic
- The 32-bit count_us counter WRAPPED at 21:34:15Z (arm + 4294.967296 s)
  inside this window. Wrap-corrected walls (origin = arm banner second):
  **21:36:01.133Z .. 21:37:08.285Z** vs declare 21:35:54Z and fired receipt
  21:37:14Z (5.7 s after last frame) — causal; wrap branch MACHINE-SELECTED
  by the fired-stamp consistency assert (pre-wrap branch fails it by ~73 min).
- **SHA GATE: MATCH 64/64** — digest(captured) == B775 declare == A270 mirror
  == fired B776: `823d61deca78be6a7317010e4bba6a6d3d1e431615759715a064ce34e94af3d1`

## Pairing (T10 battery)

- **PRIMARY (cycle-36 captured bytes): VALID, 142.0 s, exit 0**
- **CONTROL-1 (cycle-29 key-31 `a44de797` — SAME statement class): VALID, 142.1 s**
- **CONTROL-2 (cycle-30 key-32 `4152dc05` — DIFFERENT class): VALID, 142.0 s**
- Declare vectors machine-parsed from both buses and byte-diffed equal;
  binary/PK/VK sha-guarded unchanged before+after
  (a0c74748 / 8dda8b79 / 7bd5683f); SoC 41.8->46.2 C, throttled 0x0

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `4LjgCqDtgrYAPPfBCbn16Ei6hWoxjRpLr8CfLsiqCYipjvY3dVQVMXmWXS7vr3otRGUZUecpphgb9mutVwb72gUX`** — confirmed, slot 508271657,
  record PDA `Hg8yw2abHRHqg6yEJHfxfP6VwDKeaytXW8hB24hYcuzv`, session_id `823d61deca78be6a`,
  merkle_root = proof SHA256, coords [137, 168, 117, 111, 93, 250]
- **Chain-readback gate PASS**: signature machine-fetched via
  `getSignaturesForAddress` on the record PDA and byte-compared to this
  artifact file before commit — byte-equal, err=null.
- Treasury fee +100,000 lamports; 6/6 tests PASS
- Explorer: https://explorer.solana.com/tx/4LjgCqDtgrYAPPfBCbn16Ei6hWoxjRpLr8CfLsiqCYipjvY3dVQVMXmWXS7vr3otRGUZUecpphgb9mutVwb72gUX?cluster=devnet

## Honest ledger

- `SETTLED_TRANSFER` line in the settle summary is the script's template label
  (env not overridden); the actual settled transfer is identified by
  CAPTURE_META + PROOF_PAYLOAD_SHA256 in the same file — same disclosure as
  cycles 29/30.
- Wall-clock reporting carries ~15 s origin/banner-second uncertainty (session
  listener exited at window close, no live `ps lstart`); first-frame-to-declare
  reads -7 s, inside that jitter. The SHA gate and pairing do not depend on
  walls.
- Cycle-36's session segment sits in the shared standby guard log at lines
  8616..8996; the certified slice is committed here
  (`capture_slice_cycle36_burst_frames.txt`, 85 lines, sha256 `6ed4b474141a1ad9…`).

## Files

- `rx_payload_128b.bin` — captured 128 B burst payload (SHA-matched)
- `b_rx_extract_output.json` — machine extract of the c-36 session (22 packets)
- `capture_slice_cycle36_burst_frames.txt` — the 5 burst frames, certified slice
- `bus_events_drill.json` — window/declare/fired/signoff events, both buses
- `t10_cycle36_battery.py` / `.log` — the battery + VALID verdict
- `result_summary.txt`, `tests_passed.txt` — on-chain settle (6/6 PASS)
