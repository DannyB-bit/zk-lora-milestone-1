# groth16_ota cycle-172 — COMPLETE VALID A→B (RakMiner-A → RakMiner-B)

Live over-the-air Groth16/BN254 proof transfer, key-129 (identity-era keyset VK 78352ffa / PK aea2ed17),
captured on RakMiner-B's certified continuous-standby RX session and settled on Solana Cuneiform devnet.
Register TX `cjLJTKRX…bQ6n5` · record PDA `Cou52q3y5oByzZmzUKpU2fBFuSAbDCCzKaNKCmdpdsWE` · 6/6 PASS settle,
independent chain readback PASS (PDA/owner/session/coords/merkle-root/authority byte-match 64/64).

This cycle consumed the LAST warm rung of Alpha's proof cache (key-129, the second of the keys 128/129
refill notice A1374/B3875 @ 2026-11-09T22:46:29Z). The TX proof ladder now stands at ZERO warm rungs;
a standing keys-130/131 refill ask rides the stage-2 bus post and the PR description.

## Chain of custody (every claim below traces to a file in this directory)

1. **Window** — `cycle172_window_declare.json`: B-bus seq 3964 (A mirror 1382), armed 2026-11-11T01:49:22Z,
   closes 2026-11-11T03:49:22Z. Listener: certified continuous standby
   (`/home/researcher-bravo/fleet/logs/rx_standby_continuous_20261106T012708Z.log`, gate PASS #61 in this
   log, listener PID 1050119, arm-skew 1.0 s). Radio A center 904.3 MHz + IF −400 kHz = 903.9 MHz exact,
   SF9/125 kHz, `-m 0` (mode-0 = plain center). Declared 2026-11-11T02:54:33Z with 3290 s remaining —
   EARLY declare inside the certified window, composer law c-78 / c-146.
2. **Fire** — Alpha watcher hot-path: proof declare `groth16_proof_tx` A1383/B3965 @ 02:54:34Z, fired
   5/5 TX_DONE 02:55:54Z (`groth16_tx_fired` A1384/B3967), 80 s declare-to-fire, no LLM turn on either
   side. Key-129 warm rung = last of Alpha's cache refill A1374/B3875 (keys 128/129 minted + pre-proved
   on real A72, battery PASS on A's die).
3. **Capture** — `b_rx_extract_output.json` + `c172_session_slice.log`: **5/5 CRC-OK 128 B @ 903.9 MHz
   SF9**, status 0x10, SNR +10.8..+11.2 dB, inter-frame 16.71..16.99 s, count_us 3919048552..3986239160,
   PRE-WRAP burst (+0 s, machine-selected by the battery from its own SHA-MATCH line, c-122/c-137 laws).
   SHA gate 64/64: digest(captured) == declared `cb186efbbbc6db12ee73c7bd5813a955f3f009176ab615e15060d91a88d458cf`.
   Captured bytes: `rx_payload_128b.bin` (128 B, sha256 self-check pass). Excluded: 2× SF10 status 0x11
   CRC-failed frames (−17.0/−18.2 dB) + 2× SF10 CRC-OK ambient frames (−13.8/−17.0 dB) — size+digest+CRC
   gate; 9 packets demodulated in the segment, 5 matched.
4. **Silicon** — `t12_cycle172_battery.log` + `t12_cycle172_battery_attempt1.log`: PRIMARY key-129
   pairing VALID (exit 0, 161.4 s, complete-line `BATTERY_EXIT=0`, done 2026-11-11T03:55:42Z);
   FIRST-OF-CLASS positively asserted (statement-class pih[-1]=c8248ac81038bf2d, prior-declares B=0/A=0
   over the complete dual-bus history); distinct-class controls key-128 (cycle-171, VALID 160.2 s) and
   key-126 (cycle-169, VALID 161.4 s); GUARD-AFTER binary 6e12c42de5d333fd / PK aea2ed17290f3294 /
   VK 78352ffa2d0bfe92 unchanged; SoC 45.7 °C → 50.1 °C, throttled=0x0. Battery ran on the
   `--window-seq 3964` era-pinned locator.
5. **Settlement** — `settle_result_summary.txt` + `settle_tests_passed.txt`: RegisterCoordinates TX
   `cjLJTKRX…bQ6n5` (devnet, finalized, err null), record PDA
   `Cou52q3y5oByzZmzUKpU2fBFuSAbDCCzKaNKCmdpdsWE`, session `cb186efbbbc6db12`, settler clock
   2026-11-11T03:59:08.683Z, coords [238,99,228,71,25,146] == payload bytes 0..5, merkle root ==
   sha256(rx payload) 64/64, 100 000-lamport protocol fee CPI-collected, wallet
   14aTW9yp…ziaMa3 5.81845084 → 5.81717236 SOL. Settler 6/6 PASS, 0 fail.
6. **Independent chain readback** — `settle_chain_readback.json`: PASS, re-fetched from devnet RPC
   2026-11-11T04:00:04Z (slot 520975689), not from the settler's own output: account exists, 103-byte
   layout, owner == Cuneiform program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy, authority == fleet
   wallet, session == sha[0:16], coords byte-match, merkle root raw-32B byte-match 64/64. Verdict PASS.

## Honesty disclosures

- The settler's live stdout tee (`settle_cycle172.log`) was NOT captured for this cycle — the run was
  executed without `tee`. No reconstruction has been attempted: settlement evidence here is the settler's
  own `result_summary.txt` / `tests_passed.txt` (TEST_RUN block) plus the INDEPENDENT on-chain RPC
  readback, which is the strongest single artifact and stands on its own.
- The RX session slice was cut from the listener's session banner (banner-second convention); the
  session continued past this window, so the slice has no exit line — the burst is in-window by
  armed/closes timestamps and by count_us origin at the banner second.
- Total packets demodulated inside the segment: 9 (5 matched; 4 excluded as documented in §3).

— Researcher Bravo (Agent 05, RakMiner-B), 2026-11-11T07:1x UTC
