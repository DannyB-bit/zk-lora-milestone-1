# groth16_ota cycle-132 — A→B over 903.9 MHz LoRa (key-74, FIRST-OF-CLASS)

**Verdict: COMPLETE VALID — T12 battery PRIMARY VALID + 2 distinct-class controls VALID, BATTERY_EXIT=0 (attempt1)**
**Settled on Solana Cuneiform devnet — 26th consecutive radio-to-chain loop closed.**

## What flew
- Alpha's watcher fired the cached key-74 Groth16/BN254 proof (`dfee90424c8d79822c4c9b5a5ff00d84e2fad076fc8a8c99bc479e04a74bf451`, 128 B = A(32)||B(64)||C(32)) into my certified RX window: **~80s declare-to-fire** (declare A900/B2191 2026-10-18T18:12:25Z → fired A901 2026-10-18T18:13:47Z, 5/5 TX_DONE).
- Window: armed 2026-10-18T17:57:32Z → closes 19:57:32Z (LORA_CHIRP_RECOVERY_PASS=YES, chip 0x10 v1.0, listener PID 478767, arm-banner skew 1.0 s, 6340 s remaining at declare; B2189==A899).
- Radio: 903.9 MHz (radio A 904.3, IF −400 kHz), SF9/125 kHz, mode 0.
- Capture: **5/5 CRC-OK proof frames** (digest == declare 64/64), SNR +11.0..+11.5 dB, inter-frame 16.7..16.8 s uniform, pre-wrap (+0s) burst (machine-selected), count_us 903034826..970038014. The in-window slice also demodulated ambient traffic (146 CRC-OK incl. ambient, 27 CRC-BAD) — excluded by the sha gate.
- SHA gate: captured digest == dual-bus declare 64/64 hex.

## Dual-bus integrity
- Window B2189==A899, declare B2191==A900, fired A901 @18:13:47Z — all byte-identical across both buses (cross-bus byte-diff TRUE per battery log).

## T12 battery (attempt1, exit 0)
- PRIMARY: key-74 `dfee9042` — pairing VALID on B die, 159.9 s.
- Controls: key-73 8e677f99 (c-131) + key-72 22d2ef8a (c-130), machine-picked distinct statement-class, VALID 159.9 s / 160.2 s; vendored byte-exact from PR#97/#96 heads BEFORE silicon per c-91 law, sha-verified vs dual-bus declares.
- Class scan: complete dual-bus history, key-74 pih[-1]=`dd7261a471fbc229`, prior-declares B=0 A=0, unclassable-declares=5 → FIRST-OF-CLASS (positively asserted).
- Era: identity (VK 78352ffa / PK aea2ed17); era-pin skipped 45 canon-era controls (c-96 law).
- Silicon: temp 37.0 → 39.4 °C, throttled 0x0. GUARD-AFTER unchanged (binary 4c8e1f8a46952c1b, PK aea2ed17290f3294, VK 78352ffa2d0bfe92).
- Battery run 2026-10-18T20:13:28Z → 20:21:31Z.

## Settle (Cuneiform devnet)
- TX [`1P2kUJkM…`](https://explorer.solana.com/tx/1P2kUJkM4P39nZBYuPBwPhqp1z4uR2t15YV3cQghWyupFmTFtcjnZZYJuhhyCwZnLZGn598bVpjyxMbJDGA6zHs?cluster=devnet),
  PDA `89f9nWnKmW1rfVqBfqSoKTLDL6uX33XGwM48ekxspMc8`, slot 512555386, err=null, 6/6 settle tests PASS.
- settle_readback: live RPC getSignaturesForAddress sig byte-match, block_time 2026-10-18T20:23:43Z.
- chain_readback_v2 PASS: account owner = program `2is5Q4r…`, session-id/coords/merkle-root/authority all byte-match; coords [63,37,174,27,241,136] = payload[0:6]; merkle root = proof SHA.
- Fee 100000 lamports; balance 5.87981788 → 5.8785394 SOL.

## Honest ledger
- Two-turn publish gap, disclosed: extract+payload staged in the 18:4xZ turn (before the 19:57:32Z close, c-117 law) then the turn ended before bus-post/battery; rx_capture_confirmed posted 20:08:26Z (B2199/A902), battery 20:13→20:21Z, settle 20:23:43Z; the 19:5xZ tick noted "c-132 PR push backfill in flight" but the branch commit/push/PR did not land — **this evidence dir + PR landed 2026-10-19T01:3xZ**, with settle/chain readbacks re-fetched live (00:08:41Z / 00:09:02Z).
- Fresh branch off the c-131 PR#97 head per c-91/c-108 (main still pre-fix); template trio + prior evidence dirs inherited byte-exact, sha-verified against dual-bus declares BEFORE silicon.

## Reproduce
1. `bash ~/fleet/scripts/launch_t12_cycle132.sh attempt1` (sha-guarded canonical template)
2. `bash ~/fleet/scripts/settle_cycle132.sh` (gates on BATTERY_EXIT=0 + dual-bus byte-diffs)
3. `python3 tools/chain_readback_v2.py --pda 89f9nWnKmW1rfVqBfqSoKTLDL6uX33XGwM48ekxspMc8 --expect-root dfee90424c8d79822c4c9b5a5ff00d84e2fad076fc8a8c99bc479e04a74bf451 --expect-session dfee90424c8d7982 --expect-coords 63,37,174,27,241,136`
