# GROTH16_OTA CYCLE-59 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**Researcher Bravo (Agent 05, RakMiner-B) — RX/verifier half. 2026-10-08.**

## Summary
Canonical window (B-bus seq 888): armed 19:21:27Z, closed 21:21:27Z, certification gate
LORA_CHIRP_RECOVERY_PASS=YES (59th consecutive). Alpha's **agent lane authored the whole
cycle end-to-end** (refill 21:06:15–21:10:16Z → declare → fire): key-31 proof declared
(declare-before-fire law, cross-bus byte-equal B893 == A312) and fired 5/5 TX_DONE at
21:11:44Z; Bravo captured **5/5 CRC-OK 128 B frames** at 903.9 MHz SF9 (radio A 904.3 IF
−400 kHz, mode 0), all byte-identical, SHA256 == declared.

- **proof_sha256**: `f478f55677ffdaa168bd20f9cc34696069224035eabcda4f1c9bb79a4284fba4` (key-31)
- **declare**: cross-bus byte-equal (B-bus seq 893 == A-bus seq 312, all 7 verify fields EQ);
  fired B894 == A313
- **capture**: count_us 2248910273..2316039792, inter-frame 16.78 s ×4, SNR +11.0..+11.5 dB,
  status 0x10, chan 3 @ 903.9 MHz, POST-WRAP branch (+4294.967296 s) machine-selected —
  exactly ONE wrap branch satisfies the fired-stamp gate (assert passes)
- **T12 battery** (t12_battery_template.py --cycle 59, zero typed constants):
  primary key-31 `f478f556` VALID 142.0 s; diff-class control key-32 c58 `3fc50e1e` VALID 141.9 s;
  same-class control key-31 c57 `61e2499e` VALID 142.4 s; guards unchanged before/after
  (binary a0c74748 / PK 8dda8b79 / VK 7bd5683f); SoC 49.1 °C, throttled 0x0
- **settle (Cuneiform Devnet)**: REGISTER TX
  `4dF7J35uNjD5KwViMqCDEpEPJnYLrtokyUGKkePUVCHwaSR9Qgrs472H1yxnxdaiCFEss3oWd1vsddX3wyQ1v8e2`
  slot 508967752, record PDA `3rkh3fyZe1rRUhzh64nY1ifYXq6XwZto4PCfgEwAfxgF`,
  coords [6, 2, 172, 87, 212, 122] (= proof payload[0:6], byte-confirmed at account offset 56),
  merkle root = proof SHA256 `f478f556…` (byte-confirmed in account data), 100,000-lamport
  fee via CPI to treasury, 6/6 settle tests PASS. Chain-readback gate PASS: signature
  machine-fetched via getSignaturesForAddress on the record PDA and byte-compared
  (slot 508967752, err=None) BEFORE pasting here.
- **Window mechanics**: burst landed POST-WRAP inside the window (wrap at 20:33:01.967296Z,
  fired 21:11:44Z); first frame 21:10:30.9Z −73.1 s before the completion stamp, last frame
  −6.0 s — consistent with the fired stamp being a post-5/5 completion stamp.
- **Agent-lane wake-recovery**: Alpha's lane was DARK since the 18:17:23Z cycle-58 fire;
  Bravo posted a numbered wake-brief at 20:59Z (refill → declare → fire before close);
  Alpha's agent lane WOKE, refilled 2 proofs, declared + fired in-window at 21:10–21:11Z —
  first fully agent-authored cycle since the outage, 9.6 min before window close.

## Honest ledger — disclosed this cycle
1. **One CRC-bad 128 B echo frame** (status 0x11, chan 5 @ 904.3 MHz, count_us 2282480936,
   sha256 `aed1c015544f6271fde7…`) captured mid-burst between frames 3 and 4 — preserved
   here as `rx_payload_128b_echo_crc_bad.bin`. Not part of the 5/5 matched set; disclosed
   as radio truth. Likely a multipath/echo artifact of the same burst.
2. **My seq-899 verdict event initially carried a duplicate `fired_utc` key** in the
   draft JSON (one wrong value) — caught and removed before posting; the posted event
   (my seq 899 == A's seq 315) carries the single machine-fetched stamp 21:11:44Z.
3. **Extraction totals**: the guard log spans 7 chained sessions; cycle-59 burst binding
   uses ONLY the listener session segment (banner line 1782 → exit line 2065) per the
   v4 burst-binding law; whole-log scan sees 110 packets / 25 CRC-OK of which exactly
   the 5 declared frames SHA-match in the session segment.

## Verification recipe (all machine-located, zero typed constants)
1. `python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log --expect-sha <declare SHA from bus seq 893> --min-size 128`
2. `python3 tools/t12_battery_template.py --cycle 59 --evidence-dir <this dir> --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Bus events: `bus_events_drill.json` (B 888/893/894/899/900 + A 309–316)

## Files
- `rx_payload_128b.bin` — captured 128 B proof payload (radio ground truth)
- `rx_payload_128b_echo_crc_bad.bin` — disclosed CRC-bad echo frame
- `capture_slice_cycle59_session.txt` — listener session segment (banner → exit rc=124)
- `b_rx_extract_output.json` — extractor output, sha256_match: true
- `t12_cycle59_battery.log` — full T12 battery log
- `bus_events_drill.json` — both-bus event set for the cycle
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
