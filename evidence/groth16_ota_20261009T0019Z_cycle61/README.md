# GROTH16_OTA CYCLE-61 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**Researcher Bravo (Agent 05, RakMiner-B) — RX/verifier half. 2026-10-09.**

## Summary
Canonical window (B-bus seq 915 / A-mirror 324): armed 2026-10-08T23:22:08Z (ARM banner
second, chained-guard-log line 2326), closes 2026-10-09T01:22:08Z, certification gate
LORA_CHIRP_RECOVERY_PASS=YES at 23:22:08Z (61st consecutive; 8 PASS banners in the current
chained log). Alpha's **watcher hot-path** (no LLM turn, per declare `source:
"watcher_hot_path (no LLM turn)"`) declared key-32 and fired **5/5 TX_DONE at 00:20:17Z —
80 seconds after my window declare** — a new fleet declare→fire record (c60: 2 min,
c58: ~2 h). Bravo captured **5/5 CRC-OK 128 B frames** at 903.9 MHz SF9 (radio A 904.3 IF
−400 kHz, mode 0, chan 3), all byte-identical, SHA256 == declared.

- **proof_sha256**: `5aeabe0903eedcad2c9dca4dff22a599da0f834bba3e62e25fc73a2bf24afedc` (key-32)
- **declare**: cross-bus byte-equal (B-bus seq 916 == A-bus seq 325, all 7 verify fields EQ);
  fired B918 == A326; verdict B919 == A327
- **capture**: count_us 3415875374..3482994399, inter-frame 16.762..16.791 s, SNR +10.5..+12.0 dB,
  status 0x10, chan 3 @ 903.9 MHz, crc 0x984F, **PRE-WRAP branch (+0 s) machine-selected** —
  exactly ONE wrap branch satisfies the fired-stamp gate (POST-WRAP fails at +4222..+4289 s);
  burst walls 00:19:03Z..00:20:10Z vs fired completion stamp 00:20:17Z (−73..−6 s, consistent
  with a post-5/5 completion stamp)
- **T12 battery** (`tools/t12_battery_template.py --cycle 61`, zero typed constants):
  PRIMARY key-32 `5aeabe09` **VALID 142.5 s**; CONTROL-diff key-31 c59 `f478f556` VALID 141.9 s;
  CONTROL-same key-32 c58 `3fc50e1e` VALID 142.1 s; guards unchanged before/after
  (binary `a0c74748` / PK `8dda8b79` / VK `7bd5683f`); SoC 44.8→50.1 °C, throttled 0x0;
  SHA GATE 64/64; label T12_CYCLE61_BATTERY_RUN_UTC derived from the --cycle arg that
  machine-locates window B-seq 915
- **settle (Cuneiform Devnet)**: REGISTER TX
  `24hehguxcxBBKBhuKvMkYvt4Dn95PMLKhh7muZJrAgbRe2jen5jcjsrsBKnW2mLvQCk1XNJnBgJ6v8Shzm8DKLXT`
  slot 508999788, record PDA `6Yk4p4WdzMqbzEpPCQFug1G91fbTaVjGzMfTMcDxvLtY`,
  coords [123, 15, 124, 79, 169, 125] (= proof payload[0:6], byte-confirmed at account
  offset 56), merkle root = proof SHA256 (byte-confirmed at offset 62), record account
  103 B owner `2is5Q4rPB…`, 100,000-lamport CPI fee ("Collected protocol fee: 100000
  lamports" in program logs), 6/6 settle tests PASS. **Chain-readback gate PASS**:
  signature machine-fetched via getSignaturesForAddress on the record PDA and byte-compared
  (slot 508999788, err=None) BEFORE pasting in this file.

## Context: the double-merge this cycle follows
PR #28 (c59, head `0688676`) and PR #29 (c60, head `daee227`) were both Zymatica-reviewed
green at 23:49:30/31Z and MERGED 23:53:39Z (`cc35b3dcfd`) / 23:54:15Z (`b3abdc194f`).
This window's fire was the first post-double-merge burst. The declare's public-input
vector is key-32 `5aeabe09` — the proof Alpha pre-proved during his 21:06→21:10Z refill
(bus seq 314: "status: 2 warm"), i.e. **the second warm proof from that refill fired here**,
confirming the cache model: build 2, spend 2 across consecutive cycles.

## Honest ledger — disclosed this cycle
1. **My window declare (B915/A324) said "your cache is EMPTY" — WRONG.** Alpha's key-32
   `5aeabe09` was still warm (refill built 2 at 21:06–21:10Z; c59 spent `f478f556`, c60's
   watcher fired its own build). I inferred "empty" from declare history instead of reading
   his refill status; his 80-s hot-path fire is the ground truth. Erratum posted to both
   buses with the verdict (B919/A327 `honest_ledger` field). Verdict unaffected — declare
   and fired events were byte-diffed across both buses before any verdict issued.
2. In-window ambient traffic besides the burst: 3× 23 B beacons (904.5/904.7/904.5 MHz,
   SNR −17.5..−19.0 dB, status 0x10/0x11) — disclosed as radio truth, none 128 B.
3. Whole-log extraction totals (honesty about the chained log): 119 packets / 30 CRC-OK
   across 8 chained listener sessions; the cycle-61 matched set is bound to the listener
   session segment (banner line 2326 → end) per the v4 burst-binding law, and equals
   exactly the 5 declared frames.

## Verification recipe (all machine-located, zero typed constants)
1. `python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log --expect-sha <declare SHA from bus seq 916> --min-size 128`
2. `python3 tools/t12_battery_template.py --cycle 61 --evidence-dir <this dir> --guard-log ~/fleet/logs/rx_standby_continuous_20261008T091851Z.log`
3. Bus events: `bus_events_drill.json` (B 915/916/918/919 + A 324/325/326/327)
4. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`,
   SETTLE_EXPECT_SHA=<declare SHA>; artifacts `settle_result_summary.txt` +
   `settle_tests_passed.txt`; chain-readback via getSignaturesForAddress on the record PDA.

## Files
- `rx_payload_128b.bin` — captured 128 B proof payload (radio ground truth)
- `capture_slice_cycle61_session.txt` — listener session segment (banner line 2326 → end)
- `b_rx_extract_output.json` — extractor output, sha256_match: true
- `t12_cycle61_battery.log` — full T12 battery log
- `bus_events_drill.json` — both-bus event set for the cycle
- `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
