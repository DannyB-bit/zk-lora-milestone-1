# groth16_ota cycle-171 — COMPLETE VALID A→B (RakMiner-A → RakMiner-B)

Live over-the-air Groth16/BN254 proof transfer, key-128 (identity-era keyset VK 78352ffa / PK aea2ed17),
captured on RakMiner-B's certified continuous-standby RX session and settled on Solana Cuneiform devnet.
Register TX `5b61iRfx…izh2t` · record PDA `SwSbnj5seZuRpiTSCevbTWfm4HtXggHwzgwB86Ume7W` · 6/6 PASS settle,
independent chain readback PASS (PDA/owner/session/coords/merkle-root/authority byte-match 64/64).

## Chain of custody (every claim below traces to a file in this directory)

1. **Window** — `cycle171_window_declare.json`: B-bus seq 3879 (A mirror 1376), armed 2026-11-09T21:44:36Z,
   closes 2026-11-09T23:44:36Z. Listener: certified continuous standby
   (`rx_standby_continuous_20261106T012708Z.log`, gate PASS #47 in this log, listener PID 809698, arm-skew 0.0 s).
   Radio A center 904.3 MHz + IF −400 kHz = 903.9 MHz exact, SF9/125 kHz, `-m 0` (mode-0 = plain center).
   Declared at 23:39:37Z with 299 s remaining — inside the certified window, composer law c-78.
2. **Fire** — Alpha watcher hot-path: proof declare `groth16_proof_tx` A1377/B3877 @ 23:39:38Z (same second as
   my declare mirror landed — no LLM turn), fired 5/5 TX_DONE 23:40:58Z (`groth16_tx_fired` A1378/B3878),
   ~80 s declare-to-fire. Key-128 warm rung from Alpha's cache refill notice A1374/B3875 @ 22:46:29Z
   (keys 128/129 minted + pre-proved on real A72, battery PASS, tamper INVALID).
3. **Capture** — `b_rx_extract_output.json` + `c171_session_slice.log`: **5/5 CRC-OK 128 B @ 903.9 MHz SF9**,
   status 0x10, SNR +10.8..+11.5 dB, inter-frame 16.71..16.77 s uniform, count_us 2613956951..2680902198,
   POST-WRAP burst (+4294.967296 s, machine-derived by the battery from its own SHA-MATCH line, c-122 law).
   SHA gate 64/64: digest(captured) == declared `42554e708fc682e6c073870565d42b767df9903c8f1fad65d088845ef5050eaf`.
   Captured bytes: `rx_payload_128b.bin` (128 B, sha256 self-check pass). Excluded: 1× off-channel 128 B
   status 0x11 (chan 6, −11.2 dB) decoy + ambient 23–24 B frames — size+digest+CRC gate.
4. **Silicon** — `t12_cycle171_battery.log` + `t12_cycle171_battery_attempt1.log`: PRIMARY key-128 pairing
   VALID (exit 0, 161.2 s, `BATTERY_EXIT=0` complete line, done 2026-11-10T00:01:42Z); FIRST-OF-CLASS
   positively asserted (statement-class pih[-1]=7419ef7cbd45e917, prior-declares B=0/A=0 over the complete
   dual-bus history); distinct-class controls key-127 (cycle-170, VALID 161.3 s) and key-126 (cycle-169,
   VALID 160.9 s); GUARD-AFTER binary 6e12c42d / PK aea2ed17 / VK 78352ffa unchanged; SoC 48.7 °C,
   throttled=0x0. Battery ran on the `--window-seq 3879` era-pinned locator.
5. **Settlement** — `settle_cycle171.log` + `settle_result_summary.txt` + `settle_tests_passed.txt`:
   RegisterCoordinates TX `5b61iRfx…izh2t` (devnet, finalized, err null), record PDA
   `SwSbnj5seZuRpiTSCevbTWfm4HtXggHwzgwB86Ume7W`, session `42554e708fc682e6`, on-chain readback ts
   2026-11-10T00:12:46Z, coords [31,131,93,89,159,176] == payload bytes 0..5, merkle root == sha256(rx payload)
   64/64, 100 000-lamport protocol fee CPI-collected (treasury delta +100000), wallet
   14aTW9yp…ziaMa3 5.81972932 → 5.81845084 SOL. Settler 6/6 PASS, 0 fail.
6. **Independent chain readback** — `settle_chain_readback.json`: PASS, re-fetched from devnet RPC
   (not from the settler's own output): account exists, 103-byte layout, owner == Cuneiform program
   2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy, authority == fleet wallet, session == sha[0:16],
   coords byte-match, merkle root raw-32B byte-match 64/64. Verdict PASS, exit 0.

## Honesty disclosures

- Settler stdout was captured live via `tee` into `settle_cycle171.log` (no c-170-style reconstruction gap);
  `settle_result_summary.txt` is the TEST_RUN block of that same file.
- `capture_meta.json`'s `wrap_branch` initially carried a hand-typed value; corrected to the battery's
  machine-derived POST-WRAP result (c-122 law) — the battery's own SHA-MATCH line is the only accepted source.
- The listener session continues under the standby supervisor's 2 h re-arm law; this cycle's frames were
  captured before the 23:44:36Z close (last matched frame count_us 2680902198, in-window).

— Researcher Bravo (Agent 05, RakMiner-B), 2026-11-10T00:15Z UTC
