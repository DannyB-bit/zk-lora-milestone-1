# groth16_ota cycle-38 (2026-10-07T01:24Z) — COMPLETE VALID CYCLE, third win inside one hour

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T12 battery: primary + same-class +
different-class controls, all VALID, one session). Ninth autonomous A->B
Groth16 OTA exchange — and the **third complete cycle inside one hour**
(c-36 21:37Z + c-37 00:15Z + c-38 01:24Z), fired by the zero-LLM watcher
hot-path **3 seconds after B's window declare**. First **PRE-WRAP** burst
since cycle-29.

## Context

Window declared by B at 01:22:52Z (B-bus seq 796 / A-bus mirror 279) over the
listener armed 00:23:19Z (38th consecutive chirp-recovery gate PASS). Alpha's
watcher declared at 01:22:55Z (B798 / A280, verify-fields byte-equal
cross-bus, machine-diffed in the battery; key-32, pre-proven warm cache
`efd4f5a1`) and fired 01:24:15Z (B799 / A281, 5/5 TX_DONE).
Declare-to-declare latency: 3 s; declare-to-fired-receipt: 80 s.

## Radio capture (B) — PRE-WRAP frames

- 5 frames, `status 0x10` (CRC-OK), 903.9 MHz chan 3, SF9, SNR +10.8..+11.0,
  inter-frame 16.8/16.9 s, deterministic
- count_us 3582497847..3649735970; the 32-bit counter would wrap at
  ~01:34:53Z (arm + 4294.967296 s) — AFTER the last frame (01:24:08.735Z
  wall), so this burst is **PRE-WRAP**: the wrap branch was still
  MACHINE-SELECTED by the fired-stamp consistency assert (exactly one of
  {+0s, +4294.967296s} passes the -180..+240s last-frame-vs-fired gate; the
  +wrap branch maps the last frame to 02:35:43Z, outside the window).
- **No 128B RF-ghost this window** (c-30/c-37 class ghost absent); one
  ambient 23 B `status 0x11` CRC-BAD frame at 903.9 and nine ambient 23 B
  CRC-OK frames are disclosed in the capture slice, excluded by the
  128B + SHA gates.
- **SHA GATE: MATCH 64/64** — digest(captured) == B798 declare == A280 mirror
  == fired B799: `efd4f5a1ebf785c1e74c6d26e915a43339f321c734585a26aa90ae6e8dbfdacf`

## Pairing (T12 battery) — t12_cycle38_battery.py

- **PRIMARY (cycle-38 captured bytes): VALID, 142.5 s, exit 0**
- **CONTROL-1 (cycle-30 key-32 `4152dc05` — SAME statement class): VALID,
  141.9 s** — class label machine-verified at runtime: the control's
  `private_key_id` was parsed from its bus declare and asserted equal to the
  primary's machine-parsed key id.
- **CONTROL-2 (cycle-29 key-31 `a44de797` — DIFFERENT class): VALID, 141.9 s**
  — label machine-verified by the same assert (not equal).
- Declare vectors machine-parsed from both buses and byte-diffed equal;
  binary/PK/VK sha-guarded unchanged before+after
  (a0c74748 / 8dda8b79 / 7bd5683f); SoC 40.4→45.2 °C, throttled 0x0.
- Canon verification ran with `ZK_LORAWAN_REPRODUCIBLE_SETUP` unset (disk
  keys); keys backed up before the session.

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `38n8vFMT9pPZzyL3tycLyk1Kuvj7aYXLtdoofFGGs9TUm2B16cWCiD6UaTfjSQPmkbRo5BPZhki4Pwyd3iXMQ6Bs`** — confirmed, slot 508322710,
  record PDA `32u5MDD7toDBAxiBc6ncmixVoS5H2pRTebpVoWrDpqNE`, session_id `efd4f5a1ebf785c1`,
  merkle_root = proof SHA256, coords [152, 70, 249, 62, 116, 115]
- **Chain-readback gate PASS**: signature machine-fetched via
  `getSignaturesForAddress` on the record PDA and byte-compared to this
  artifact before commit — byte-equal, err=null.
- Treasury fee +100,000 lamports; 6/6 tests PASS
- Explorer: https://explorer.solana.com/tx/38n8vFMT9pPZzyL3tycLyk1Kuvj7aYXLtdoofFGGs9TUm2B16cWCiD6UaTfjSQPmkbRo5BPZhki4Pwyd3iXMQ6Bs?cluster=devnet

## Honest ledger

- **Run-stamp label**: the executed battery copy carried a template leftover
  in its first log line (`T12_CYCLE37_BATTERY_RUN_UTC`); the committed
  `t12_cycle38_battery.py` corrects that label to CYCLE-38 post-run. Label
  only — zero logic difference; the committed `t12_cycle38_battery.log` is
  the verbatim executed output.
- **Wall-clock origin**: count_us origin = arm-banner second (00:23:19Z);
  banner-second jitter of order ~15 s cannot be excluded with the session
  listener gone. `fired_utc` is Alpha's burst completion stamp — first frame
  lands ~74 s before it, the same offset pattern as c-36/c-37. The SHA gate
  does not depend on walls.
- The settlement `result_summary.txt` `SETTLED_TRANSFER` line was edited
  post-run from the script's stale default to name cycle-38 explicitly; all
  machine-measured lines untouched.

## Files

- `capture_slice_cycle38_session.txt` — verbatim listener session segment
  (arm banner → Test End), incl. disclosed ambient frames
- `bus_events_drill.json` — raw window/declare/fired events, both buses
- `b_rx_extract_output.json` — machine extraction (5/5 CRC-OK, SHA match)
- `rx_payload_128b.bin` — the 128 B on-air proof (from parser hex)
- `t12_cycle38_battery.py` / `.log` / `t12_launch.log` — battery + verbatim output
- `result_summary.txt`, `tests_passed.txt` — settlement record (6/6 PASS)
