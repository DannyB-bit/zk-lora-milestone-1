# groth16_ota cycle-97 — COMPLETE VALID A→B (2026-10-13, 46th valid fleet cycle)

**Alpha fired a 128 B compressed Groth16 proof (key-39, SHA-256
`741392bdd020c88114701892f4e70420e829690b7bd70aa45dbddd08adce9007`) 79 s
after my window declare; I captured 5/5 CRC-OK frames at 903.9 MHz exact,
byte-identical to the declare, and the T12 first-of-class pairing battery
returned PRIMARY VALID + both distinct-class controls VALID on my die.**

- **Window** B1481/A590, armed 2026-10-13T10:18:26Z → closes 12:18:26Z
  (declared via `declare_rx_window.py --cycle 97`, all fields machine-parsed).
- **Declare** B1483/A591 at 11:26:47Z, cross-bus byte-equal on all 7 fields
  (`public_input_hashes`, gateway, firmware, deposit 100008, key-39,
  deposit_commitment, proof_sha256).
- **Fired** 11:28:06Z (5/5 TX_DONE) — **79 s declare-to-fire, 21st
  consecutive 80s-class**. First frame on-air 11:26:53.7Z (declare +1.3 s).
- **Capture** 5 frames, count_us 4107740470..4174962863 (pre-wrap), walls
  11:26:53.7Z..11:28:00.9Z, SNR 10.5–11.0 dB, chan 3, datr 9, status 0x10.
- **T12 battery** (`T12_CYCLE97_BATTERY_RUN_UTC=2026-10-13T11:41:02Z`):
  primary key-39 VALID 141.9 s; CLASS SCAN over complete dual-bus history →
  **FIRST-OF-CLASS positively asserted** (prior declares B=0/A=0, pih-only
  B=0/A=0, unclassable=5); controls key-38 (c-96) VALID 142.0 s + key-36
  (c-94) VALID 141.9 s, machine-picked distinct statement classes; guards
  unchanged (binary a0c74748, PK 8dda8b79, VK 7bd5683f); temp 45.7→49.6 °C,
  throttled 0x0; `BATTERY_EXIT=0`, attempt-1 clean pass from tools/ depth-2.
- **Cuneiform devnet settle**: TX
  `5VWnq93oRotcSt3pvs2YMbRQQiXA2Msc6vxGJ22mrExfs544UTLkJHT1gyA97cDX2nacqN8RQvXikFM3YavBqzY`,
  record PDA `4V4Do7ULmVomWPaDgKvmwo3Wsa9uEwW5UEV52AD5iaAP`, slot 510617580,
  **chain-readback PASS** (signature machine-fetched via
  `getSignaturesForAddress` on the record PDA and byte-compared; err=None).
  103 B digest-only record (ZK Settlement Law: commitments + anchors only).

## Honest ledger

- **Chained-session contamination caught in-staging (c-96 law applied at the
  extractor level):** the raw listener log spans TWO bursts in one armed
  session — the leg-3 conversation burst (key-38 `d3ccac4a`, 10:20:58–10:22:05Z)
  and this cycle-97 burst (11:26:53–11:28:00Z). A first staging attempt wrote
  `crc_ok[0]` (the leg-3 frame) as the payload bin; the bin-SHA check caught
  it immediately, the contaminated bin was deleted, and `session_slice.log`
  was band-filtered to the key-39 burst (count_us > 4.0e9) before the
  official extract. The 10 dropped frames are visible in
  `t12_cycle97_battery.log`'s session segment (guard log lines 44..242).
- **Two hand-typed-constant instances, both caught by guards at zero pairing
  cost (the law extends to git leases and provenance constants):**
  1. The `git push --force-with-lease` expected-SHA was typed from the 8-char
     commit prefix with an invented tail → push rejected ("stale info"),
     lease refetched machine-side via `git ls-remote`, pushed clean. The
     guard worked as designed.
  2. The vendored key-36 control's expected-SHA was typed from the `3a333037`
     prefix with an invented tail → sha-guard failed the restore. Full SHA
     re-fetched from the dual-bus c-94 declare (byte-diffed B==A):
     `3a33303728b85008d54b73942e530e3d9082183aa57f156f5939224d76ca4090`.
     Disclosure lives in `vendored_controls/VENDORED_PROVENANCE.json`.
- **Working-tree divergence disclosed:** the concurrent tick's conversation
  PR#62 branch carried the local HEAD when this evidence was staged; this PR
  is cut fresh off `origin/main` (base 3c9676b) per the one-drill-per-branch
  law, byte-identical payload files sha-verified after the cherry-pick.

## Files

- `session_slice.log` — band-filtered RX slice (key-39 burst only)
- `b_rx_extract_output.json` — fail-closed extractor output: 5 CRC-OK frames,
  `sha256_match: true`, exit 0 (PR#52 exit-contract build)
- `rx_payload_128b.bin` — the captured proof bytes (sha256 = declare)
- `declare_dual_bus_raw.json` / `fired_dual_bus_raw.json` / `window_declare_raw.json`
- `t12_cycle97_battery_attempt1.log` / `t12_cycle97_battery.log` — battery logs
- `capture_meta.json` / `verdict_payload_posted.json` / `chain_readback.json`
- `vendored_controls/` — c-91 law: key-38 + key-36 control payloads restored
  byte-exact from PR#61's branch, sha-verified against the dual-bus declares,
  so a fresh checkout reproduces the first-of-class battery
- `result_summary.txt` — one-glance verdict sheet

## Reproduce

```bash
python3 tools/b_rx_extract.py session_slice.log \
  --expect-sha 741392bdd020c88114701892f4e70420e829690b7bd70aa45dbddd08adce9007 --min-size 100
# expect: crc_ok=5, sha256_match=true, exit 0
```

Vendored controls:
```bash
sha256sum vendored_controls/*_rx_payload_128b.bin
# key-38: d3ccac4a568fe31de57bbb3626ba573f0fbf8f955e24bac4d742d3534843477c
# key-36: 3a33303728b85008d54b73942e530e3d9082183aa57f156f5939224d76ca4090
```
