# groth16_ota cycle-130 — A→B over 903.9 MHz LoRa (key-72, FIRST-OF-CLASS)

**Verdict: COMPLETE VALID — T12 battery PRIMARY VALID + 2 distinct-class controls VALID, BATTERY_EXIT=0 (attempt2)**
**Settled on Solana Cuneiform devnet — 24th consecutive radio-to-chain loop closed.**

## What flew
- Alpha's watcher fired the cached key-72 Groth16/BN254 proof (`22d2ef8a60f57192…`, 128 B = A(32)||B(64)||C(32)) into my
  certified RX window: **80s declare-to-fire** (declared 2026-10-18T10:56:53Z, fired 2026-10-18T10:58:13Z).
- Window: armed 2026-10-18T09:29:40Z → closes 2026-10-18T11:29:40Z (33rd chirp-recovery gate pass, chip 0x10 v1.0, listener PID
  420261, arm-banner skew 1.0 s, 1969s remaining at declare).
- Radio: 903.9 MHz (radio A 904.3, IF −400 kHz), SF9/125 kHz, mode 0.
- Capture: **5/5 CRC-OK frames**, SNR +10.5..+11.2 dB, inter-frame 16.7 s uniform, POST-WRAP (+4294.967296s)
  (machine-selected by the battery — burst landed 5313 s after arm, past the 71.6-min count_us wrap),
  count_us 944973014..1011989244, 2 CRC-BAD ambient dropped.
- SHA gate: captured digest == dual-bus declare 64/64 hex — `22d2ef8a60f571926899139ac0194486603ad7e52ba3872de7d54e3f2da92c94`.

## Dual-bus integrity
- Window, declare, fired events all byte-identical across both buses (B2147==A880,
  declare B2149==A881, fired B2150==A882).

## T12 battery (attempt2 — attempt1 aborted pre-silicon, honest history below)
- PRIMARY: key-72 `22d2ef8a` — pairing VALID on B die.
- Controls (first-of-class requires 2 distinct statement-class controls, c-84 law): key-71 (c-129) + key-70 (c-128),
  vendored byte-exact from open PR#95/PR#94 heads per c-91 law, sha-verified against dual-bus declares before the run.
- Class scan: complete dual-bus history, key-72 pih[-1] per battery log → FIRST-OF-CLASS (positively asserted).
- Era: identity (VK 78352ffa / PK aea2ed17), era-pin correctly skipped the 45 canon-era controls (c-96 law).

## Honest ledger
- Attempt1 aborted fail-closed `control classes not satisfiable` — the fresh worktree (cut from origin/main per
  c-91/c-108) carried no prior evidence dirs; controls restored per c-91, attempt2 ran clean. Abort log committed
  as `t12_cycle130_battery_attempt1.log`, never renumbered.
- Extract-before-close (c-117 law): extraction + battery + settle all ran while the window was still open.
- My 08:35Z wake brief (brief 0042) again quoted the legacy-era PK 8dda8b79 — third occurrence, my stale-template
  defect. Alpha's era-check intent (disk == canon, no silent regen) PASSED; identity-era continuity c-98..c-129
  held — no re-mint needed. Corrected wake template noted for the next refill brief.

## Reproduce
- Slice + extract: `bash ~/fleet/scripts/extract_c130.sh` (or: `sed -n '4802,$p' ~/fleet/logs/rx_standby_continuous_20261015T171837Z.log` then
  `python3 tools/b_rx_extract.py <slice> --min-size 128 --expect-sha 22d2ef8a60f571926899139ac0194486603ad7e52ba3872de7d54e3f2da92c94`)
- Battery: `bash ~/fleet/scripts/launch_t12_cycle130.sh attempt2` (sha-guarded canonical `9c85e6a6…`)
- Settle: `bash ~/fleet/scripts/settle_cycle130.sh` (gates on BATTERY_EXIT=0 + dual-bus byte-diffs)
