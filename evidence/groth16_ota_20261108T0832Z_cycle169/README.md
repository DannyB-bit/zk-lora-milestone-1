# groth16_ota cycle-169 — COMPLETE VALID A→B (RakMiner-A → RakMiner-B)

Live over-the-air Groth16/BN254 proof transfer, key-126 (identity-era keyset VK 78352ffa / PK aea2ed17),
captured on RakMiner-B's certified continuous-standby RX session and settled on Solana Cuneiform devnet.

## Chain of custody (every claim below traces to a file in this directory)

1. **Window** — `cycle169_window_declare.json`: B-bus seq 3751 (A mirror 1361), armed 2026-11-08T07:38:12Z,
   closes 09:38:12Z. Listener: certified continuous standby (`rx_standby_continuous_20261106T012708Z.log`,
   arm banner line 5080; chirp-recovery PASS before arm). Radio A center 904.3 MHz + IF −400 kHz = 903.9 MHz exact,
   SF9/125 kHz.
2. **Fire** — Alpha watcher hot-path: declare A1362/B3753 08:31:19Z → fired 5/5 TX_DONE 08:32:38Z (79s, no LLM turn).
3. **Capture** — `b_rx_extract_output.json` + `c169_session_slice.log`: 5/5 CRC-OK 128B @ 903.9 MHz SF9,
   SNR +10.8..+11.5 dB, inter-frame 16.7 s uniform, count_us 3193655658..3260545090 (pre-wrap +0s).
   SHA gate 64/64: digest(captured) == declared `2d1a1db001772b8d483ee90ce17cf1be836f73f62a579f9541c6851697ab179d`.
   Captured bytes: `rx_payload_128b.bin` (sha256 self-check 2d1a1db0…).
4. **Silicon** — `t12_cycle169_battery.log`: PRIMARY key-126 pairing VALID (exit 0, 161.2 s);
   FIRST-OF-CLASS positively asserted (statement class pih[-1]=675cfec9611d5213, priors B=0/A=0 over the
   complete dual-bus history); distinct-class controls key-125 (cycle-168) and key-119 (cycle-211) both VALID;
   GUARD-AFTER binary 6e12c42d / PK aea2ed17 / VK 78352ffa unchanged; SoC 45.2→48.2 °C, throttled=0x0.
   Battery ran on the dual-era `--window-seq 3751` locator (paired seqs ['1361','3751']).
5. **Settlement** — `settle_cycle169.log` + `settle_result_summary.txt`: RegisterCoordinates TX
   `5cQ6a6wv…mPsa` (slot 520138576, 2026-11-08T21:37:47Z), record PDA `7M8cQ7Av5GhZgCsKrC59hTiGZpoghF8U9HMac9RQFv9h`,
   session `2d1a1db001772b8d`, on-chain merkle root == sha256 of the on-air proof (PDA data offset 62),
   coords [216,1,212,195,162,145] == payload bytes 0..5, 100000-lamport protocol fee CPI-collected.
   Wallet 14aTW9yp…iaMa3: 5.822286280 → 5.821007800 SOL.

**Verdict: E2E_RF_EVIDENCE=PASS** — CRC-OK ≥1 AND SHA match; pairing VALID on B die; settled on-chain same day.

Files: `rx_payload_128b.bin`, `b_rx_extract_output.json`, `c169_session_slice.log`, `capture_meta.json`,
`cycle169_window_declare.json`, `t12_cycle169_battery.log`, `settle_cycle169.log`,
`settle_result_summary.txt`, `settle_tests_passed.txt`.

— Bravo, Agent 05 (RakMiner-B)
