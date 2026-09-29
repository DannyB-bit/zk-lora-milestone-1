# node-b-rx_20260929T223317Z — Groth16 OTA v2 window capture (RakMiner-B)

First machine-coordinated **spec-v2** fire window: Alpha's watcher auto-fired 83 s
after the `rx_window_open` declaration (bus seq75) — zero human latency.

- 5/5 CRC-OK 128-byte frames @ 903.9 MHz SF9, SNR +10.8..+11.2 dB
- All 5 payloads byte-exact vs TX declaration: SHA-256 `8f2fe020…6485995`
- Radio + CRC + protocol legs: PASS. Pairing leg vs declared statement: INVALID
  (canon VK AND seed-42 regen VK; 6-variant gateway sweep). Suspected hot-path
  proof/declaration binding mismatch on the TX side (declared private_key_id `31`
  with id-1 hashes). Fail-closed verdict preserved honestly.

Files:
- `rx_groth16_proof_128b.bin` — captured payload written from parser hex
- `rx_raw_capture.log` — full always-on RX session log
- `result_summary.txt` — KEY=VALUE evidence (M1 standard)

Compare with `node-b-rx_20260929T154420Z`: same drill, Alpha agent-turn proof
(SHA `f8bec880…`), which B **verified VALID** under the repo-committed canon VK
and settled on Cuneiform devnet (TX `2q6y8cEn…WTk2ha`).
