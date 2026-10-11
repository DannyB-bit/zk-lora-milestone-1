# groth16_ota cycle-82 — RX capture evidence (RakMiner-B)

- **Cycle:** 82 (86th consecutive arm-gate PASS)
- **Window:** armed 2026-10-11T06:06:50Z, closes 2026-10-11T08:06:50Z, listener PID 154996
  (`test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0`,
  radio A 904.3 MHz − 400 kHz IF ⇒ 903.9 MHz exact, SF9/125 kHz)
- **Declare:** B1214/A466 posted 07:23:27Z via `declare_rx_window.py v1.0`
  (release triggered by Alpha's 3-warm b_ack A463: d940d21e key-31, ff238e52 key-32, 4b416048 key-33)
- **Fire:** Alpha watcher hot-path — proof_tx B1216/A467 07:23:29Z (2.0s after declare),
  5/5 TX_DONE fired 07:24:49Z — **declare→fire 82s, 7th consecutive 80s-class (81/81/82/80/80/81/82)**
- **Payload:** 128 B compressed Groth16/BN254 proof (A 32B G1 ‖ B 64B G2 ‖ C 32B G1),
  SHA-256 `d940d21e1280adb1d0d632e48a727c156b0bfe0a12dadbc37b5fbad3552a5bec`
  (key-31, deposit 100000, gateway `0016c001ff18afa3…`)
- **Capture:** 5/5 CRC-OK 128B frames @ 903.9 MHz exact (freq_hz 903900000), SF9,
  SNR +11.0..+11.8 dB, inter-frame 16.75–16.79s, count_us 310964013..378036496
  (POST-WRAP branch, machine-selected by the T12 battery; origin = banner second 06:06:50Z)
- **SHA gate:** `tools/b_rx_extract.py --expect-sha d940d21e… --min-size 128` → 5/5 match,
  `sha256_match: true` (independent pre-battery confirmation)
- **Declare byte-diff:** cross-bus B1216 == A467 byte-equal (battery asserts)
- **Public inputs (machine-parsed from declare):** identity `cbe1d4d7…`, nullifier `a2624f76…`,
  attestation `8ed4c468…`, ciphertext `2261a97c…`; PK `8dda8b79…`, VK `7bd5683f…` (canon repo keys)

## Files
| File | Purpose |
|---|---|
| `c82_session_slice.log` | RX session slice from the 06:06:50Z arm banner (guard log) |
| `declare_c82.json` | Composer output (window declare B1214/A466, cert fields) |
| `b_rx_extract_output.json` | Fail-closed parser output: 5/5 CRC-OK, SHA match |
| `rx_payload_128b.bin` | Reconstructed 128B payload from parser hex (SHA-gated) |
| `extract_run.log` | Raw extract invocation |
| `capture_meta.json` | Machine-derived capture metadata (walls, count_us, SNR, declare chain) |
| `t12_cycle82_battery.log` | T12 pairing battery (PRIMARY + control-diff + control-same) |

## Honest ledger
- c-81 (armed 04:06:30Z) expired **undeclared** — cache-hold protocol (1 warm) held as designed;
  both twins co-logged the honest miss.
- First T12 launch this cycle aborted (`no arm banner matches the window armed_at_utc`) —
  template `DEFAULT_GUARD` pointed at the stale Oct-3 standby log; fixed same-turn
  (machine-glob newest guard log) and re-run with explicit `--guard-log`. Fix committed
  alongside this evidence.
- Radio verdict: `rx_verdict cycle82_capture_confirmed` posted B1218/A469 BEFORE battery/PR/settle
  (bus verdict first — the TX twin waits on it).
- Field correction B1220/A470: my bus verdict hand-derived "pre-wrap" and a fabricated
  count_us upper bound (`377222039` — extrapolated, not in any parse). Battery machine parse:
  POST-WRAP branch, count_us 310964013..378036496. Same-turn correction posted; hand-typed-constant
  instance #6 on B, owned.
