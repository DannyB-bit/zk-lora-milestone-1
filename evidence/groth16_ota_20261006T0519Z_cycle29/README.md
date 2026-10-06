# groth16_ota cycle-29 (2026-10-06T04:42Z) — COMPLETE VALID CYCLE, zero-LLM watcher hot-path

**Verdict: VALID cycle COMPLETE** — radio 5/5 CRC-OK SHA MATCH 64/64 +
Groth16/BN254 pairing VALID on the B die (T8 battery: primary + two controls,
all VALID, one session). Fifth autonomous A→B Groth16 OTA exchange, and the
**first fired entirely without an LLM turn on the A side** (watcher hot-path
from his pre-proven cache; only the RX side used an agent lane).

## Context

Cycle-29 window declared by B at 04:41:06Z (B-bus seq 699 / A-bus mirror seq
245) over the listener armed 04:19:56Z (29th consecutive chirp-recovery gate
PASS). Alpha's watcher answered in **2 seconds**: `groth16_proof_tx` B seq
700 / A seq 246 (byte-equal cross-bus, source `watcher_hot_path (no LLM
turn)`, construction seed-42 canon PK, pre-proven cache proof_1) — then
`groth16_tx_fired` B seq 703, 5/5 TX_DONE, fired_utc 04:42:28Z (his script's
completion stamp; walls below show the sends at 04:41:14–04:42:21Z).

## Radio capture (B)

- 5 frames, `status 0x10` (CRC-OK), chan 3, SF9, SNR +11.0, RSSI 198
- count_us 1278484711 … 1345694264, inter-frame 16.7–16.9 s, deterministic
- Walls (listener-lstart origin, ps lstart tz-corrected): 04:41:14.484Z …
  04:42:21.694Z — the fired event's 04:42:28Z stamp lands after the last
  frame, consistent with a completion-stamp semantics (disclosed)
- **SHA GATE: MATCH 64/64** — digest(captured) `a44de79723f68c23c6a8e0b26a2547ebfc57252b6a3b7c3408e3fe2fedac9cae`
  == B700 declare == A246 declare == fired B703

## Pairing (T8 battery)

- **PRIMARY (cycle-29 captured bytes): VALID, 142.1 s, exit 0**
- **CONTROL-1 (cycle-28 key-31 `8d7bf2fe…`): VALID, 142.3 s** — fresh-proof same-class control
- **CONTROL-2 (cycle-26 key-32 `c11788f4…`): VALID, 142.1 s** — different statement class
- Vectors machine-parsed from both bus declares, byte-diffed equal (watcher-path
  declare omits only the informational `coordinate` field; all verify-consumed
  fields present and equal — machine-checked)
- Guards: binary `a0c74748` / PK `8dda8b79` / VK `7bd5683f` unchanged before+after;
  SoC 37.4→42.3 °C, throttled `0x0`

## Cuneiform Devnet settlement (same tick)

- **REGISTER TX `4HUehK4YE9UraqMznAksBxqqJ6ms9i92pduTTQ3PLSMkyAfvzbSbeXr6vFgX7rZnRWaaAYwo65kHrr9sPPZgcpzX`** — confirmed
- Record PDA `46ythtFejjFq6L4d99c1aaUCxWYaLAwnPzrot1dMdWKd`,
  session_id `a44de79723f68c23`, merkle_root = proof SHA256, coords [194,43,39,37,54,115]
- Readback: on-chain coords/root byte-match; treasury fee +100,000 lamports; 6/6 PASS

## Battery engineering notes (honest ledger)

- Burst binding v4 law: **session-segment ∩ digest-equality** with the
  machine-fetched declare. Wall-clock binding alone is fragile (fired_utc is a
  completion stamp; count_us origin is the listener process boot).
- `ps lstart` prints **local time** — naive-parse as UTC caused a 4-hour false
  offset (EDT); tz-corrected via `.astimezone()`. Caught by the battery's own
  skew assert, zero verdict impact.
- Cycle-28's transient "SHA divergence" incident (my hand-typed constant,
  retracted on the record — see `../groth16_ota_20261006T0150Z_cycle28/`)
  directly produced the digest-equality binding used here: every SHA in this
  battery is computed from bytes on disk or fetched from the bus at run time.

## Files

- `rx_payload_128b.bin` — captured 128 B burst payload (SHA-matched)
- `b_rx_extract_output.json`, `rx_frames_meta.txt`, `capture_log_excerpt.txt`
- `bus_events_drill.json` — window/declare/fire/verdict events, both buses
- `t8_cycle29_battery.py` / `.log` — the battery + VALID verdict
- `settle_result_summary_cycle29.txt` — on-chain settle readback (6/6 PASS)

## Disposition

Cycle-29 COMPLETE VALID end-to-end: RF → SHA gate → pairing battery →
Cuneiform devnet record, closed in a single tick. Alpha's cache now holds
proof_2 key-32 (`4152dc05…`) — next window re-arm queued.
