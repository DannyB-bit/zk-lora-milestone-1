# groth16_ota cycle-131 — A→B over 903.9 MHz LoRa (key-73, FIRST-OF-CLASS)

**Verdict: COMPLETE VALID — T12 battery PRIMARY VALID + 2 distinct-class controls VALID, BATTERY_EXIT=0 (attempt1, FIRST TRY)**
**Settled on Solana Cuneiform devnet — 25th consecutive radio-to-chain loop closed.**

## What flew
- Alpha's watcher fired the cached key-73 Groth16/BN254 proof (`8e677f99a4d284a6…`, 128 B = A(32)||B(64)||C(32)) into my
  certified RX window: **80s declare-to-fire** (declared 2026-10-18T13:06:56Z, fired 2026-10-18T13:08:16Z).
- Window: armed 2026-10-18T11:30:00Z → closes 13:30:00Z (34th chirp-recovery gate pass, chip 0x10 v1.0, listener PID
  434548, arm-banner skew 0.0 s, 1387s remaining at declare).
- Radio: 903.9 MHz (radio A 904.3, IF −400 kHz), SF9/125 kHz, mode 0.
- Capture: **5/5 CRC-OK frames**, SNR +10.5..+11.8 dB, inter-frame 16.8 s uniform, POST-WRAP (+4294.967296s)
  (machine-selected by the battery), count_us 1528031246..1595214712, 0 CRC-BAD ambient this window.
- SHA gate: captured digest == dual-bus declare 64/64 hex — `8e677f99a4d284a65a273b62aa36014243afacc7981cb35021444b3793230b11`.

## Dual-bus integrity
- Window, declare, fired events all byte-identical across both buses (B2162==A888,
  declare B2163==A889, fired B2166==A890).

## T12 battery (attempt1 — first-try clean)
- PRIMARY: key-73 `8e677f99` — pairing VALID on B die, 159.5 s.
- Controls (first-of-class requires 2 distinct statement-class controls, c-84 law): key-72 (c-130) + key-71 (c-129),
  vendored byte-exact from open PR#96 head BEFORE silicon per c-91 law, sha-verified against dual-bus declares
  (canonical template `9c85e6a6…`, key-71 `685002e7…`, key-72 `22d2ef8a…`) — the c-130 attempt1 abort lesson applied,
  zero re-runs needed this cycle.
- Class scan: complete dual-bus history, key-73 pih[-1]=`ad01ab85777bb009` → FIRST-OF-CLASS (positively asserted).
- Era: identity (VK 78352ffa / PK aea2ed17); era-pin correctly skipped the 45 canon-era controls (c-96 law).
- Silicon: temp 40.4 → 44.8 °C, throttled 0x0. GUARD-AFTER unchanged.

## Settle (Cuneiform devnet)
- TX [`FaQjGi1c…`](https://explorer.solana.com/tx/FaQjGi1cH7Qc1jfdqhaJvHo1uTUtXCsKdaNsCqSiqR3oUpt2wBx35Ebm8R1TSMb6su3xtvLaV1Wo1umKpx8LG7A?cluster=devnet),
  PDA `6eFAqA6AmbH1niy4WxvNiYXxgy5EP65rT2mYSXuTWfT4`, slot 512452847, err=null, 6/6 settle tests PASS.
- chain_readback_v2 PASS: account owner = program `2is5Q4r…`, session-id/coords/merkle-root/authority all byte-match;
  coords [48,77,8,196,253,9] = payload[0:6]; merkle root = proof SHA; sig byte-match via getSignaturesForAddress.

## Honest ledger
- One launcher hiccup before silicon: the first background launch of the battery exited 127 (tool wrapper rejected the
  heredoc that authored the launcher — the script did not exist yet). Relaunched in 3.5 min; the real battery run was
  attempt1, first try, no aborts. No re-numbering.
- Extract-before-close (c-117 law): extraction 13:11Z, battery 13:21:57→13:29:59Z, settle 13:36Z — declare-to-settle
  inside a single sync tick (declared 13:06:54Z).
- Fresh branch off origin/main per c-91/c-108 (main still pre-fix — instance #6 carried forward); template trio +
  prior evidence dirs (c-129, c-130) restored byte-exact from PR#96 head via machine-listed cat-file blobs.

## Reproduce
1. `bash ~/fleet/scripts/extract_c131.sh` (slice from ARM banner line 4984 + fail-closed extractor with machine-fetched SHA)
2. `bash ~/fleet/scripts/launch_t12_cycle131.sh attempt1` (sha-guarded canonical `9c85e6a6…`)
3. `bash ~/fleet/scripts/settle_cycle131.sh` (gates on BATTERY_EXIT=0 + dual-bus byte-diffs)
4. `python3 tools/chain_readback_v2.py --pda 6eFAqA6AmbH1niy4WxvNiYXxgy5EP65rT2mYSXuTWfT4 --expect-root 8e677f99a4d284a65a273b62aa36014243afacc7981cb35021444b3793230b11 --expect-session 8e677f99a4d284a6 --expect-coords 48,77,8,196,253,9`
