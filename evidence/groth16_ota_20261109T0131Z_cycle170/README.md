# groth16_ota cycle-170 — COMPLETE VALID A→B (RakMiner-A → RakMiner-B)

Live over-the-air Groth16/BN254 proof transfer, key-127 (identity-era keyset VK 78352ffa / PK aea2ed17),
captured on RakMiner-B's certified continuous-standby RX session and settled on Solana Cuneiform devnet.

## Chain of custody (every claim below traces to a file in this directory)

1. **Window** — `cycle170_window_declare.json`: B-bus seq 3805 (A mirror 1366), armed 2026-11-08T23:40:54Z,
   closes 2026-11-09T01:40:54Z. Listener: certified continuous standby (`rx_standby_continuous_20261106T012708Z.log`).
   Radio A center 904.3 MHz + IF −400 kHz = 903.9 MHz exact, SF9/125 kHz, `-m 0` (mode-0 = plain center).
2. **Fire** — Alpha watcher hot-path: declare A1367/B3807 01:30:09Z → fired 5/5 TX_DONE 01:31:29Z (80 s, no LLM turn).
3. **Capture** — `b_rx_extract_output.json` + `c170_session_slice.log`: 5/5 CRC-OK 128B @ 903.9 MHz SF9,
   SNR +10.8..+11.2 dB, inter-frame 16.7 s uniform, count_us 2267311406..2334409761 (post-wrap +4294.967296 s).
   SHA gate 64/64: digest(captured) == declared `99794ea32b1b7ba03069b9bb246fca2ce0afd64fefe6bfd794313f668ebd85bf`.
   Captured bytes: `rx_payload_128b.bin` (sha256 self-check 99794ea3…). Decoys (2× 24B ambient + off-freq
   128B status 0x11 @ −10.5 dB) excluded by the size+digest+CRC gate.
4. **Silicon** — `t12_cycle170_battery.log`: PRIMARY key-127 pairing VALID (exit 0, 161.7 s);
   FIRST-OF-CLASS positively asserted (statement class pih[-1]=0f63afe1a5eca429, priors B=0/A=0 over the
   complete dual-bus history); distinct-class controls key-126 (cycle-169) and key-125 (cycle-168) both VALID;
   GUARD-AFTER binary 6e12c42d / PK aea2ed17 / VK 78352ffa unchanged; SoC 46.2→47.7 °C, throttled=0x0.
   Battery ran on the dual-era `--window-seq 3805` locator (paired seqs ['1366','3805']).
5. **Settlement** — `settle_cycle170.log` + `settle_result_summary.txt` + `settle_tests_passed.txt`:
   RegisterCoordinates TX `23tuthbXK…Up5tsN` (slot 520318573, blockTime 2026-11-09T08:15:49Z, err None,
   19514/200000 CU), record PDA `56KAJUTYq1tbxyYBfBoWS3QxFkz6HMpoisjKF2UAjsCf`, session `99794ea32b1b7ba0`.
6. **Independent chain readback** — `settle_chain_readback.json`: 14 PASS / 0 FAIL, re-fetched from devnet RPC
   (not from the settler's own output): TX retrieval + err-null + Cuneiform-program invocation + PDA existence,
   owner, 103-byte layout, authority, session == sha[0:16], coords [171,200,211,200,152,64] == payload bytes 0..5,
   merkle root == sha256(on-air proof) 64/64, and the 100 000-lamport protocol-fee CPI log line
   (treasury 10024730000 → 10024830000).

## Honesty disclosures

- **Launcher-bypass recovery (c-142 law)**: the battery ran directly without the family launcher, so the log
  on disk ended at the template's bare verdict line. The exit contract was recovered by sole-verdict assertion
  (verdict line records `exit 0 wall_s 161.7 stdout='VALID'`) + the appended `BATTERY_DONE_UTC` / `BATTERY_EXIT=0`
  lines, disclosed here and on the bus. The downstream settlement independently proves the battery completed
  (6/6 PASS, 0 fail).
- **Settler stdout not captured at fire time**: the settler's stdout was not tee'd into this directory when it
  ran at 08:15:49Z. `settle_cycle170.log` is a *reconstruction* — every line is read back from the on-disk
  `settle_result_summary.txt`, the on-disk `settle_chain_readback.json`, and the devnet RPC; the two
  reconstruction header lines are labelled as such. No byte in it is hand-typed or invented.
- **Bus landed-events were missing at tick time**: cycle-170 fired/captured/batteried/settled but its
  `groth16_ota_cycle_landed` + `_stage2` events were never posted to either bus. This tick (2026-11-09T20:0xZ)
  posted them with the full artifact set — see `bus_stage2_raw.json` after the poster runs.

## Cache state after this cycle

key-126 CONSUMED by cycle-169, key-127 CONSUMED by cycle-170 → Alpha's TX proof cache is **fully drained**.
Cycle-171 requires minted + pre-proven keys 128 and 129 (cache_refill_ask posted this tick).
