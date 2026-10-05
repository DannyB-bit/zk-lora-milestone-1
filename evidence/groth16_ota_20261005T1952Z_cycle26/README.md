# groth16_ota cycle-26 (2026-10-05T19:52Z) — FIRST FULLY-CLEAN A→B CYCLE

**Verdict: VALID** — radio 5/5 CRC-OK SHA MATCH + Groth16/BN254 pairing VALID on B die,
with the public-input vector **machine-parsed from the bus declares** (zero hand
transcription). First cycle run end-to-end with no quarantine, no fault flag, no
retraction — the fleet loop as designed.

## Context

Minutes after the §5 overturn (commit `f977d73`, PR#18 — silicon-fault verdict retracted,
root cause = B's hand-transcription typo in the key-31 attestation hash), B declared a
live-fire window (B-bus seq 662, closes 20:18:14Z) against Alpha's remaining warm proof.
Alpha's watcher auto-fired within 87 s of the declare: `groth16_proof_tx` seq 663
(B-bus) / seq 233 (A-bus) — key-32 proof `c11788f4…`, deposit 100001 — then
`groth16_tx_fired` 5/5 TX_DONE at 19:53:47Z.

## Radio capture (B, cycle-27 standby window armed 18:18:14Z)

- Listener: `test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0`
- 5/5 frames CRC-OK, 903.9 MHz ref channel (chan 3, datr 9/SF9, codr 1), SNR +10.8…+11.5
- Inter-frame spacing ~16.8–17.0 s; frame SHAs identical across all 5 sends (deterministic payload)
- Extractor (`tools/b_rx_extract.py --expect-sha c11788f4…`): `sha256_match: true`,
  reconstructed payload 128 B, sha `c11788f40a31543625adbbbcecae06af9f9e47ba01b5e0fc5ef364a09366b83a`
  — **MATCH vs the declare**.

## Pairing verification (T6, reformed protocol)

- Vector provenance: parsed programmatically from BOTH bus declares (A seq 233 and
  B seq 663), asserted byte-equal before the run — the new fleet law from §5.
- Recipe: canon disk keys (PK `8dda8b79…`, VK `7bd5683f…`), binary sha `a0c74748…`,
  CWD = zk-lorawan repo root, `ZK_LORAWAN_REPRODUCIBLE_SETUP` unset, keys sha-guarded after.
- Result: **VALID, exit 0, 142.1 s** (`t6_cycle26_verify.log`).

## Timeline (UTC)

| Time | Event |
|---|---|
| 18:18:14Z | B standby gate PASS #26 → listener armed (cycle-27 window, closes 20:18:14Z) |
| 19:52:27Z | B declares live-fire window (B-bus seq 662) |
| 19:52:27Z | Alpha watcher declare: key-32 `c11788f4…` (B seq 663 / A seq 233) |
| 19:53:47Z | Alpha `groth16_tx_fired` 5/5 TX_DONE (B seq 664 / A seq 234) |
| 19:53–20:00Z | B capture: 5/5 CRC-OK, SHA MATCH |
| 20:11:10Z | T6 pairing verify: **VALID** 142.1 s on B die |
| 20:1xZ | Verdict posted both buses (B seq 667 / A seq 236) |

## Files

- `rx_payload_128b.bin` — reconstructed 128 B proof (sha `c11788f4…`)
- `b_rx_extract_output.json` — extractor output (sha gate PASS)
- `rx_frames_meta.txt` — the 5 CRC-OK frame headers
- `capture_log_excerpt.txt` — raw listener log around the 5 frames
- `bus_events_drill.json` — window declare, Alpha declare/fire (both buses), verdict
- `t6_cycle26_verify.py` / `.log` — machine-parsed-vector verify + result
