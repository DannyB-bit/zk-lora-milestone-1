# groth16_ota cycle-133 — A→B over 903.9 MHz LoRa (key-75, FIRST-OF-CLASS)

**Verdict: COMPLETE VALID — T12 battery PRIMARY VALID + 2 distinct-class controls VALID, BATTERY_EXIT=0 (attempt1, FIRST TRY)**
**Settled on Solana Cuneiform devnet — 27th consecutive radio-to-chain loop closed.**

## What flew
- Alpha's watcher fired the cached key-75 Groth16/BN254 proof (`136a7be73bdf3896c8360a522999bd3d3a7cddb6a653b0a07706efc4131e7328`, 128 B = A(32)||B(64)||C(32)) into my certified RX window: **~80s declare-to-fire** (declare A905/B2205 2026-10-18T21:28:43Z → fired A906 2026-10-18T21:30:03Z, 5/5 TX_DONE).
- Window: armed 2026-10-18T19:57:52Z → closes 21:57:52Z (LORA_CHIRP_RECOVERY_PASS=YES @ 19:57:52Z, chip 0x10 v1.0, listener PID 490852, arm-banner skew 1.0 s, 1752 s remaining at declare; B2204==A904).
- Radio: 903.9 MHz (radio A 904.3, IF −400 kHz), SF9/125 kHz, mode 0.
- Capture: **5/5 CRC-OK frames, 0 CRC-BAD ambient this window**, SNR +10.8..+11.2 dB, inter-frame 16.71..16.78 s uniform, POST-WRAP (+4294.967296 s) burst (machine-selected), count_us 1163373484..1230394947.
- SHA gate: captured digest == dual-bus declare 64/64 hex — `136a7be73bdf3896c8360a522999bd3d3a7cddb6a653b0a07706efc4131e7328`.

## Dual-bus integrity
- Window B2204==A904, declare B2205==A905, fired A906 @21:30:03Z — all byte-identical across both buses (cross-bus byte-diff TRUE per battery log).

## T12 battery (attempt1 — first-try clean)
- PRIMARY: key-75 `136a7be7` — pairing VALID on B die, 160.6 s.
- Controls: key-74 dfee9042 (c-132) + key-73 8e677f99 (c-131), machine-picked distinct statement-class, VALID 160.1 s / 160.3 s; vendored byte-exact from the c-132/c-131 evidence BEFORE silicon per c-91 law, sha-verified vs dual-bus declares.
- Class scan: complete dual-bus history, key-75 pih[-1]=`54e020ec41f44e02`, prior-declares B=0 A=0, unclassable-declares=5 → FIRST-OF-CLASS (positively asserted).
- Era: identity (VK 78352ffa / PK aea2ed17); era-pin skipped 45 canon-era controls (c-96 law).
- Silicon: temp 36.0 → 41.3 °C, throttled 0x0. GUARD-AFTER unchanged (binary 4c8e1f8a46952c1b, PK aea2ed17290f3294, VK 78352ffa2d0bfe92).
- Battery run 2026-10-18T21:34:06Z → 21:42:11Z.

## Settle (Cuneiform devnet)
- TX [`2ZxNd3Yf…`](https://explorer.solana.com/tx/2ZxNd3Yfd6sUwCHsc1cyU3uF6VqhmQzYhJRQNqTAFR8z1NSiH1jJo6wuStLfMiYvao6staKEzL6UkdvzzdBBCJGe?cluster=devnet),
  PDA `2sEL3hton5izo7JLn4974z1yrFVLH3d9nfxjpvyUhSfW`, slot 512575280, err=null, 6/6 settle tests PASS, settled 21:42:46Z inside the window (closed 21:57:52Z).
- settle_readback: live RPC getSignaturesForAddress sig byte-match, block_time 2026-10-18T21:42:46Z.
- chain_readback_v2 PASS (re-fetched live 2026-10-19T01:2xZ, context slot 512631339): account owner = program `2is5Q4r…`, session-id/coords/merkle-root/authority byte-match; coords [113,146,3,85,253,187] = payload[0:6].
- Fee 100000 lamports; balance 5.8785394 → 5.87726092 SOL.

## Honest ledger
- Single-tick declare-to-settle loop: declared 21:28:42Z, fired 21:30:03Z, extract 21:3xZ before close 21:57:52Z (c-117 law), battery 21:34→21:42Z, settle 21:42:47Z. The delivery chain (rx_verdict, PR, bus notices) slipped to this backfill tick (2026-10-19T01:3xZ) — disclosed, not renumbered.
- Fresh branch off the c-131 PR#97 head per c-91/c-108 (main still pre-fix); template trio + prior evidence dirs inherited byte-exact from PR#97 head.

## Reproduce
1. `bash ~/fleet/scripts/extract_c133.sh` (slice from ARM banner line 5618 + fail-closed extractor with machine-fetched SHA)
2. `bash ~/fleet/scripts/launch_t12_cycle133.sh attempt1` (sha-guarded canonical template)
3. `bash ~/fleet/scripts/settle_cycle133.sh` (gates on BATTERY_EXIT=0 + dual-bus byte-diffs)
4. `python3 tools/chain_readback_v2.py --pda 2sEL3hton5izo7JLn4974z1yrFVLH3d9nfxjpvyUhSfW --expect-root 136a7be73bdf3896c8360a522999bd3d3a7cddb6a653b0a07706efc4131e7328 --expect-session 136a7be73bdf3896 --expect-coords 113,146,3,85,253,187`
