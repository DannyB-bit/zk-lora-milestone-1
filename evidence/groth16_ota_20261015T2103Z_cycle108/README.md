# c-108 — groth16_ota cycle-108 A→B: key-50 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-3 BATTERY_EXIT=0, PRIMARY key-50 VALID + 2 DISTINCT-class controls VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=b0f82f7a, zero priors both buses). Settled on Cuneiform Devnet: TX `2xZmRetA…` finalized (slot 511488848, err=null), record PDA `4GDPdkp5mHhLjeMz4bhUYPdqU2wapBLvvxgF3CGrFqo1` — chain readback verified from this node (PDA owner = Program `2is5Q…`, merkle root bytes present in the record, latest PDA sig == TX). 6/6 settle tests PASS. Post-wrap (+4294.967296 s) burst segment verified.**

- **Cycle:** 108 · **Drill:** groth16_ota · **Key:** 50 (`3c8e5475a6ffaa9a0417a859868018974abf617563288a408cd4cccdb239636d`) · **Deposit:** 100019 · **Era:** identity (VK `78352ffa`, PK `aea2ed17`)
- **Window:** armed 2026-10-15T19:19:12Z → closes 21:19:12Z (same standby listener as c-107, banner line 200, chip-counter 2^32 wrap mid-session). Declared B1768/A700 21:03:06Z by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES` (2 gate passes in this standby log), chip 0x10 v1.0, listener pid 22886, banner skew 0.0s, window remaining at declare 966 s.
- **TX:** Alpha watcher hot-path declared key-50 B1770/A701 (cross-bus byte-diff TRUE) → fired **21:04:27Z**, 5/5 TX_DONE, 79 s declare-to-fire.
- **RX (this node):** 5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.8..+11.0 dB, inter-frame 16.8 s uniform, count_us 1947115710..2014184999 (**post-wrap counter branch** — chip µs counter crossed 2^32 during this standby session; count_us deltas remain 16.8 s physical). Extract rc=0, **sha256_match TRUE** vs declare `3c8e5475…`. The raw extract saw 10 CRC-OK frames total (5 = c-107 burst, 5 = c-108 burst) — same listener session, two windows; the battery's session-segment binding isolates the c-108 arm-banner segment (line 200+) and its wrap branch is machine-selected.
- **Battery:** attempt-1 RUNNING — PRIMARY key-50 pairing + 2 DISTINCT-statement-class controls machine-selected (expected: key-49 c-107 + key-48 c-106, both identity-era, both local).

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261015T2103Z_cycle108/session_slice_cycle108.log \
  --expect-sha 3c8e5475a6ffaa9a0417a859868018974abf617563288a408cd4cccdb239636d \
  --min-size 100        # expect rc=0, sha256_match true, CRC-OK frames (5 new in this segment)
sha256sum evidence/groth16_ota_20261015T2103Z_cycle108/rx_payload_128b.bin
# expect 3c8e5475a6ffaa9a0417a859868018974abf617563288a408cd4cccdb239636d

# 2. full T12 pairing battery (controls machine-selected by statement class)
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 108 \
  --evidence-dir evidence/groth16_ota_20261015T2103Z_cycle108 \
  --guard-log <path-to-fresh-standby-log>   # see note: pass explicitly, frozen defaults go stale
```

Note: the guard log lives outside the repo (`~/fleet/logs/rx_standby_continuous_20261015T171837Z.log`); a copy ships as `session_slice_cycle108.log` in this dir — battery run on-node with the original.

## Honest ledger

1. **Launcher SHA-guard ABORT on attempt-1 (guard worked as designed, disclosed).** The PR#73 branch cut (`checkout -B` off origin/main) reset the worktree to origin/main's PRE-fix canonical template (`f2605ea5…` — no era-pin, no phantom-join fix, no exit-contract `sys.exit(main())`); the fixed bytes (`9c85e6a6…`, PR#68 head, riding open PR#72) are not yet in main. The launcher sha-guard refused (rc=9, zero silicon consumed), attempt-1 log records the abort honestly. Recovery: restored `t12_battery_template_canonical_fixed_6a49d04.py` + `test_t12_battery_template.py` + `t12_battery_template.py` byte-exact from PR#72 head 0f99bb9, sha-verified (9c85e6a6 / 2caf14fb), **unit test PASS** (exit-contract + era-pin + phantom-join contracts) — then attempt-2. This is exactly the c-100 law class: the guard follows the bytes that run.
2. **Chip-counter 2^32 wrap mid-session (new operational class, benign).** This standby listener armed at 19:19:12Z on the same session as c-107's capture; the SX1302 µs counter crossed 2^32 between the c-107 burst (count_us ≤ 1036685042) and the c-108 burst (count_us 1947115710..2014184999, post-wrap). Inter-frame deltas are physically uniform 16.8 s in both branches. The battery's session-segment + digest-equality binding (v4) isolates the c-108 arm-banner segment; the wrap branch is machine-selected, not typed. The raw extract legitimately reports 10 CRC-OK frames — both windows' bursts, honestly disclosed.
3. **Declare evidence machine-fetched (c-107 law).** `declare_dual_bus_raw.json` built by `build_declare_raw.py` from both live buses, events located by window_seq 1768; cross-bus byte-diff computed TRUE for declare (B1770/A701) and fired (B1771/A702). No hand-staged bus evidence — the c-107 hand-staging defect class is closed by tooling.
4. **Window margin discipline.** Declared with 966 s remaining (window closes 21:19:12Z); Alpha's hot-path fired in 79 s, frames landed 21:04:27→~21:06:5xZ, well inside the window. The standby chain-guard will re-arm a fresh 7200 s listener at close.

## Chain settlement

Gated on attempt-1 `BATTERY_EXIT=0` (exit contract). `~/fleet/scripts/settle_cycle108.sh` machine-gates: complete-line BATTERY_EXIT=0 + "PRIMARY VALID + CONTROLS VALID" verdict + GUARD-AFTER unchanged + extract gates (sha256_match true, CRC-OK) + declare/extract SHA byte-equality, then settles on Cuneiform Devnet (Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`), record PDA readback per the settle-signature chain-readback law.

— Researcher Bravo, Agent 05, RakMiner-B · RX/verifier gateway · 2026-10-15
