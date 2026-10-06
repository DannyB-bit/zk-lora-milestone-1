# groth16_ota cycle-28 (2026-10-06T01:50Z) — COMPLETE VALID CYCLE + a transcription-defect retraction

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH (64/64,
machine-verified against both bus declares and the fired event) + Groth16/BN254
pairing VALID on the B die with a same-session different-statement-class control
(T7 v3 battery). First agent-lane manual declare-before-fire cycle: Alpha's lane
work was flawless end-to-end.

**And an honest-ledger retraction:** during analysis I briefly reported a
"2-char SHA divergence" in Alpha's declare chain. That was **my own error** —
a hand-typed expected-SHA constant in an exploratory parse (transposed 2 chars),
the third instance of the hand-typed-constant defect class on this box. Full
postmortem below; the declare chain is clean end-to-end.

## Context

Cycle-28 window (B-bus seq 687 / A-bus seq 240, armed 2026-10-06T00:19:15Z,
closes 02:19:15Z — 28th consecutive chirp-recovery gate PASS). Alpha's agent
lane returned, refilled his cache (proof_1 key-31 `a44de797…`, proof_2 key-32
`4152dc05…`), then declared a **fresh key-31 re-prove** (new randomness,
twin-key set closure): `groth16_proof_tx` B seq 688 / A seq 242, byte-equal
across buses; `groth16_tx_fired` B seq 689 / A seq 243 — 5/5 TX_DONE,
01:50:30Z–01:53:20Z.

## Radio capture (B)

- Listener: `test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0` (903.9 MHz ref, SF9, 125 kHz)
- 5 frames, all `status 0x10` (CRC-OK), chan 3, SF9, SNR +11.0, RSSI 198
- count_us 1276388753 … 1343497113, inter-frame 16.8 s exactly, deterministic burst
- Walls (arm-origin + wrap): 01:52:06.356Z … 01:53:13.464Z — inside the fired window
- **SHA GATE: MATCH 64/64** — digest(captured) `8d7bf2fe46a9576a0da7bcdc2e0f6de8d87f804fbfce6c9a7b0a81d3b50af61f`
  == B-bus declare (seq 688) == A-bus declare (seq 242) == fired event (seq 689)

## Pairing (T7 discriminator battery, final v3)

- Burst binding: listener-session segment (guard-log lines 5543→5827) ∩
  wrap-corrected fired window; 5/5 frames selected, digests uniform
- Vector provenance: machine-parsed from BOTH bus declares, byte-diffed equal
- **PRIMARY (captured bytes): VALID, 142.0 s, exit 0**
- **CONTROL (cycle-26 key-32 `c11788f4…`, different statement class): VALID, 142.0 s**
- Guards: binary `a0c74748` / PK `8dda8b79` / VK `7bd5683f` unchanged before+after;
  SoC 39.9→44.3 °C, throttled `0x0`; `ZK_LORAWAN_REPRODUCIBLE_SETUP` stripped

## Honest ledger — my transcription defect (retracted)

1. **Exploratory parse (defect):** I hand-typed the expected SHA into a
   throwaway analysis cell — `…ce6b7a7b0…` instead of the true
   `…ce6c9a7b0…` — read the resulting mismatch as Alpha's defect, and
   propagated it into a battery v1/v2 spec, a cycle-29 window event (B seq 699)
   and a draft README. **False claim.** Machine refetch (canonical test in this
   bundle's battery logs): captured == B688 == A242 == B689, 64/64, byte-equal.
2. **Battery v1 mis-target (quarantined):** v1 selected the burst by
   most-common-payload and hit the 2026-10-04 phantom `3b9b6d2e…`; its printed
   "INVALID + control VALID" was the Oct-4 phantom verdict, not cycle-28. Its
   own avalanche check exposed the mis-target; log preserved
   (`t7_battery_v1_wrongtarget.log`), **no verdict was issued from v1**.
3. **Battery v2 fail-closed catch (no impact):** fired-window binding alone
   matched 12 frames across listener sessions; v2's assert stopped the run
   before any pairing. Fix: session-segment ∩ fired-window (v3 law).
4. **Retraction posted:** bus `rx_verdict` B seq 706 / A seq 248 + Issue #1.
   The cycle-29 window event (B seq 699) carries a `note`/`expected_next_proof`
   that repeat the false divergence claim — superseded by the retraction event.

**Law reaffirmed and extended:** EVERY constant is machine-computed —
including in throwaway/exploratory parsing, window events, and prose. A
hand-typed constant in a scratch cell produced a false peer-defect claim that
survived three tool calls before a machine refetch killed it.

## Files

- `rx_payload_128b.bin` — captured 128 B burst payload (SHA-matched)
- `b_rx_extract_output.json` — canon extractor output over the guard log
- `rx_frames_meta.txt` — the 5 CRC-OK frames, wrap-corrected walls
- `capture_log_excerpt.txt` — arm banner (28th gate PASS) + raw frames
- `bus_events_drill.json` — window/declare/fire events from both buses
- `t7_cycle28_battery_v2.py` (as-run v3 logic) / `t7_cycle28_battery_v2.log` — final battery + VALID verdict
- `t7_battery_v1_wrongtarget.log`, `t7_launch_v1.log` — v1 quarantine record
- `t7_cycle28_discriminator_battery.py` — v1 script (defect preserved)

## Disposition

Cycle-28 radio + pairing COMPLETE and VALID. Settle queued on Cuneiform devnet
alongside cycle-29 (captured this same session — see
`../groth16_ota_20261006T0519Z_cycle29/`).
