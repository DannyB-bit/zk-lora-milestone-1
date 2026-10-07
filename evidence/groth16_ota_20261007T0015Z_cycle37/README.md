# groth16_ota cycle-37 (2026-10-07T00:15Z) — COMPLETE VALID CYCLE, watcher hot-path at full speed

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T11 battery: primary + same-class +
different-class controls, all VALID, one session). Eighth autonomous A->B
Groth16 OTA exchange — and the second complete cycle inside one hour
(c-36 21:37Z + c-37 00:15Z), fired by the zero-LLM watcher hot-path **2 seconds
after B's window declare**.

## Context

Window declared by B at 00:13:56Z (B-bus seq 786 / A-bus mirror 274) over the
listener armed 22:22:59Z (37th consecutive chirp-recovery gate PASS) — with
only ~9 minutes of window left. Alpha's watcher declared at 00:13:57Z
(B788 / A275, verify-fields byte-equal cross-bus, machine-diffed in the
battery; key-31, pre-proven warm cache `e5e0d1b4`) and fired 00:15:17Z
(B789/A276, 5/5 TX_DONE). Declare-to-fire latency: 80 s; declare-to-declare
latency: 2 s.

## Radio capture (B) — POST-WRAP frames

- 5 frames, `status 0x10` (CRC-OK), 903.9 MHz chan 3, SF9, SNR +10.8..+11.5,
  inter-frame 16.8 s, deterministic
- count_us 2370103922..2437232655; the 32-bit counter WRAPPED at 23:34:34Z
  (arm + 4294.967296 s) inside this window; wrap-corrected walls (origin =
  arm banner second): **00:14:04.071Z .. 00:15:11.199Z** vs fired receipt
  00:15:17Z (5.8 s after last frame) — causal; wrap branch MACHINE-SELECTED
  by the fired-stamp consistency assert.
- **Disclosed RF-ghost**: one `status 0x11` CRC-BAD 128 B frame 23 µs before
  frame 1 (count_us 2370103899, SNR -11.0) — same class as the cycle-30 ghost;
  excluded from the burst by the CRC gate, shown in the capture slice.
- **SHA GATE: MATCH 64/64** — digest(captured) == B788 declare == A275 mirror
  == fired B789: `e5e0d1b4d54f20dd34f69c01a28265dc1df2c2717777355f2a1fb22c6c06df3e`

## Pairing (T11 battery)

- **PRIMARY (cycle-37 captured bytes): VALID, 141.9 s, exit 0**
- **CONTROL (cycle-29 key-31 `a44de797` — SAME statement class; declare
  `private_key_id` machine-parsed as 31, correcting the battery author's
  initial key-32 assumption — the machine-parse law working as designed):
  VALID, 142.0 s**
- **CONTROL (cycle-30 key-32 `4152dc05` — DIFFERENT class): VALID, 142.0 s**
- Declare vectors machine-parsed from both buses and byte-diffed equal;
  binary/PK/VK sha-guarded unchanged before+after
  (a0c74748 / 8dda8b79 / 7bd5683f); SoC 43.3->46.2 C, throttled 0x0

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `iACGCSe7gUeihrNfeKfgzHPSTrrthdR1nLLMq8v9oeSfB5eAQD4hcvTtvgTiBPDFP6zZXFxQQjzPbDqWiahzbx6`** — confirmed, slot 508287747,
  record PDA `9MoFV73rXfFJxnFAadug1beBVqm1NaDnT2eZpNjBscdk`, session_id `e5e0d1b4d54f20dd`,
  merkle_root = proof SHA256, coords [6, 105, 59, 113, 3, 34]
- **Chain-readback gate PASS**: signature machine-fetched via
  `getSignaturesForAddress` on the record PDA and byte-compared to this
  artifact before commit — byte-equal, err=null.
- Treasury fee +100,000 lamports; 6/6 tests PASS
- Explorer: https://explorer.solana.com/tx/iACGCSe7gUeihrNfeKfgzHPSTrrthdR1nLLMq8v9oeSfB5eAQD4hcvTtvgTiBPDFP6zZXFxQQjzPbDqWiahzbx6?cluster=devnet

## Honest ledger

- Battery control labels: the T11 battery file names cycle-30 as the
  "same-class" control, but the declare's machine-parsed `private_key_id` is
  31 — so the same-class control is cycle-29 and the different-class control
  is cycle-30. Both ran VALID regardless; the pairing-law requirement
  (same-class + different-class controls both VALID in the same session) is
  satisfied. Correction disclosed rather than papered over.
- `SETTLED_TRANSFER` line in the settle summary is the script's template label
  (env not overridden); the actual settled transfer is identified by
  CAPTURE_META + PROOF_PAYLOAD_SHA256 in the same file — same disclosure as
  cycles 29/30/36.
- Wall-clock reporting carries ~15 s origin/banner-second uncertainty; the
  SHA gate and pairing do not depend on walls.

## Files

- `rx_payload_128b.bin` — captured 128 B burst payload (SHA-matched)
- `b_rx_extract_output.json` — machine extract of the c-37 session
- `capture_slice_cycle37_burst_frames.txt` — 5 burst frames + disclosed ghost
  (100 lines, sha256 `e92e6d981f8411dd…`)
- `bus_events_drill.json` — window/declare/fired events, both buses
- `t11_cycle37_battery.py` / `.log` — the battery + VALID verdict
- `result_summary.txt`, `tests_passed.txt` — on-chain settle (6/6 PASS)
