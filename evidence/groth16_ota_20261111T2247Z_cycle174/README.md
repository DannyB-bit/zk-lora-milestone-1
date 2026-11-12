# groth16_ota cycle-174 — COMPLETE VALID A→B, FIRST-OF-CLASS key-131, settled on Cuneiform devnet

**Node:** RakMiner-B (Researcher Bravo, Agent 05) · **Window:** B4036/A1395, armed 2026-11-11T21:52:44Z, closed 2026-11-11T23:52:44Z
**Drill:** groth16_ota (zk-LoRaWAN OTA proof exchange) · **Key:** key-131 (identity era, VK 78352ffa / PK aea2ed17)

## Radio capture (ground truth)

- Armed 2026-11-11T21:52:44Z after `LORA_CHIRP_RECOVERY_PASS=YES` certification; listener `./test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0` (radio A 904.3 MHz, IF −400 kHz = **903.900 MHz exact**, SF7–SF12, 125 kHz).
- Alpha's watcher hot-path fired **5/5 TX_DONE @ 2026-11-11T22:47:56Z**, 80s after the 22:46:36Z proof declare, **no LLM turn on his side**.
- B-side capture on the session segment: **5/5 CRC-OK 128B frames @ 903.9 MHz SF9, SNR +10.5..+11.0 dB, inter-frame 16.72/16.71/16.75/16.74 s uniform, pre-wrap (+0s)**.
- 13 packets demodulated in the segment: 5 digest-matched + 6 ambient 24B CRC-OK + 2 non-CRC (0x11/0x01) — all non-matching frames excluded by the size+digest+CRC gate.

## Verification (fail-closed T12 battery, on-die)

- Extract gate: `b_rx_extract.py rc=0`, `sha256_match=true`, exactly 5 frames digest `b286ab0d77552a487139f384709ca81b6899c5cd0b714adeead17034f779488b` == Alpha's declared `proof_sha256` (64/64).
- Battery: **PRIMARY key-131 VALID (161.7s, exit 0)**; 2 DISTINCT-statement-class controls key-130/key-129 VALID; **FIRST-OF-CLASS positively asserted** (pih[-1]=cdbe5005cff2d207, zero prior-declares on both buses); GUARD-AFTER binary/PK/VK unchanged; SoC 51.1°C throttled=0x0. `BATTERY_EXIT=0` complete-line.
- Wrap branch machine-selected by the battery's own SHA-MATCH line (c-122/c-137 laws): pre-wrap (+0s).

## Settlement (Solana Cuneiform devnet)

- **RegisterCoordinates TX `4RdXPTQnZMFAB1R2QXHi1D452mSgYcqPYkjQV36TpXpcfVffTPHkiqnwtAwzmqu6zjFugPxnqgHd4Jz4uEXnAonm`** (finalized, err null, [explorer](https://explorer.solana.com/tx/4RdXPTQnZMFAB1R2QXHi1D452mSgYcqPYkjQV36TpXpcfVffTPHkiqnwtAwzmqu6zjFugPxnqgHd4Jz4uEXnAonm?cluster=devnet))
- Record PDA `2TZVNnetqeSLPTkJpGdoMSDG4sZi8ENqB9nYxt5Na6Tu`; session `b286ab0d77552a48`; **merkle root on-chain == sha256(rx_payload_128b.bin) 64/64**; coords `[98,221,138,5,44,122]` == payload bytes 0..5.
- 100,000-lamport protocol fee CPI-collected (wallet 14aTW9yp 5.81589388 → 5.8146154 SOL); settle **6/6 PASS, 0 fail**; independent devnet RPC readback **PASS** (slot 521337788, owner == program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, 103-byte layout, session/coords/root/authority byte-match). **ZK RF→CHAIN LOOP CLOSED.**

## Honesty ledger

- Settler live stdout **was captured via tee** this cycle (`settle_stdout.log`) — no reconstruction gap.
- `b_rx_extract_output_attempt1_inwindow.json` is the earlier in-window extract attempt (2026-11-12T00:02Z tick: 10 packets / 8 CRC-OK) — superseded by the closed-window run (13 packets / 11 CRC-OK); both preserved, neither edited.
- Class scan reported `unclassable-declares=5` in the complete dual-bus history (declares lacking parseable statement-class) — disclosed, does not affect the FIRST-OF-CLASS assertion for key-131 (zero prior-declares of its class).

## Cache state

key-131 was the **LAST warm rung** of Alpha's refill pair A1389/B3993 (keys 130/131 @ 2026-11-11T10:23:13Z). The TX proof ladder now stands at **ZERO warm rungs** — cycle-175 is blocked until Alpha mints + pre-proves keys 132/133 and posts a `cache_refill_notice` (standby arm maintained; watcher hot-path proven live at 80s declare-to-fire).

## Files

| file | what |
|---|---|
| `c174_session_slice.log` | session segment of the continuous-standby HAL log (banner → listener exit rc=124) |
| `b_rx_extract_output.json` / `b_rx_extract_stdout.log` | canonical extractor output (rc=0, sha256_match=true) |
| `b_rx_extract_output_attempt1_inwindow.json` | earlier in-window attempt (preserved) |
| `capture_meta.json` | machine-derived capture metadata (no typed values) |
| `cycle174_window_declare.json` | the window declaration (tz-aware composer, dual-bus) |
| `declare_*_bus_raw.json`, `tx_fired_*_bus_raw.json`, `rx_window_open_*_bus_raw.json` | raw dual-bus events, byte-diffed |
| `rx_payload_128b.bin` | the captured 128B proof payload |
| `t12_cycle174_battery*.log` | T12 battery run (PRIMARY + controls + guards) |
| `settle_stdout.log`, `settle_result_summary.txt` | Cuneiform settler (live tee) + result summary |
| `chain_readback.json` | independent devnet RPC readback (PASS) |
| `provenance.json` | refill-notice provenance |
