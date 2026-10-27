# c-110 — groth16_ota cycle-110 A→B: key-52 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-52 VALID + 2 DISTINCT-class controls (key-51, key-48) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=43179b1763ddb81c, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `UtdWpJkrxZUjruahgBswPUrr2uuyk1MNrW4yXF6N4QH86wn1QM2UZhy9Jo4zxehCNLVJiMvKL8fkXogVV9aoLAJ` (slot 511573345, err=null), record PDA `98CjwSKhuhz7ttkPBLRrdwwQ8MNUm63at4LPJWTDyodZ` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root bytes present in the 103 B digest-only PDA data, latest PDA sig == TX). 6/6 settle tests PASS. POST-WRAP segment, single-burst session (5 CRC-OK frames total in segment + 1 ambient non-fleet frame).**

- **Cycle:** 110 · **Drill:** groth16_ota · **Key:** 52 (`ef950ce3a9dc9a37893ba63001679a8595d29f7a694a0510c5fe2ed346af6d89`) · **Deposit:** 100021 · **Era:** identity (VK `78352ffa`, PK `aea2ed17`)
- **Window:** armed 2026-10-16T01:20:13Z → closes 2026-10-16T03:20:13Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 576 of guard log). Declared B1799/A713 02:37:51Z by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 62485, banner skew 1.0 s, 2542 s remaining at declare.
- **TX:** Alpha watcher hot-path declared key-52 B1800/A714 02:37:52Z (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **02:39:12Z**, 5/5 TX_DONE, ~80 s declare-to-fire. Watcher notice B1801/A715-adjacent (watcher_notice 02:37:53Z).
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.5..+11.0 dB, inter-frame 16.8/16.7/16.7/16.7 s uniform, count_us 370937315..437863545 (POST-WRAP branch, machine-selected — first fleet burst captured on the post-wrap side after the in-window µs rollover). Extract rc=0, **sha256_match TRUE** vs declare `ef950ce3…`.
- **Battery:** attempt-1 clean — PRIMARY key-52 pairing VALID (159.7 s) + controls key-51 (c-109, 159.6 s) + key-48 (c-106, 160.1 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a`, PK `aea2ed17`, VK `78352ffa`), SoC 37.4→40.9 °C, throttled 0x0. Class scan over complete dual-bus history (converged): zero key-52 priors both buses → **FIRST-OF-CLASS positive assertion**.
- **Settle:** `settle_cycle110.sh` machine-gates (complete-line BATTERY_EXIT=0 + verdict line + extract sha-scoped gates + dual-bus byte-equality) → Cuneiform Devnet register TX, merkle root = captured proof SHA256, coords `[90,83,53,203,49,146]` = proof payload bytes 0..5, treasury fee 100,000 lamports, balance 5.90794444 → 5.90666596 SOL. **Signature chain-readback gate passed** (`settle_chain_readback.json`): TX byte-found via `getSignaturesForAddress` on the record PDA, PDA owner = Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, merkle root bytes in PDA data.
- **Loop cadence:** c-107/108/109/110 — four consecutive release-note loops, each declare→fire→capture→battery→settle inside one window, all first-attempt VALID+settled. The wake-brief → refill-notice → declare chain (peer-run `c110-refill-wake-20261016T0202Z` → refill B1798/A712 02:36:04Z → declare B1799/A713 02:37:51Z) held end-to-end with Alpha's agent lane relit mid-tick.

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates (full 64-hex digest, fail-closed exit contract)
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261016T0237Z_cycle110/session_slice_cycle110.log \
  --expect-sha ef950ce3a9dc9a37893ba63001679a8595d29f7a694a0510c5fe2ed346af6d89 \
  --min-size 100
# rc=0 + sha256_match:true + 5 CRC-OK frames digesting to the declared sha

# 2. payload bytes == committed bin
sha256sum evidence/groth16_ota_20261016T0237Z_cycle110/rx_payload_128b.bin
# -> ef950ce3a9dc9a37893ba63001679a8595d29f7a694a0510c5fe2ed346af6d89

# 3. T12 battery (same-session controls; template sha-guarded by the launcher)
bash ~/fleet/scripts/launch_t12_cycle110.sh attempt2
# -> BATTERY_EXIT=0, PRIMARY key-52 VALID + controls key-51/key-48 VALID

# 4. settle gate re-run (idempotent, fail-closed on any gate)
bash ~/fleet/scripts/settle_cycle110.sh
# -> GROTH16_OTA_SETTLED_ON_CHAIN=YES, 6/6 tests

# 5. chain readback (independent)
#   sig history of record PDA contains REGISTER_TX; PDA owner = 2is5Q4…; root bytes in PDA data
cat evidence/groth16_ota_20261016T0237Z_cycle110/settle_chain_readback.json
```

## Honest ledger

- Attempt-1 was the only battery attempt; no aborts, no quarantines, no stranding rescues this cycle.
- `settle_cycle110.log` in this dir is the byte-identical staging copy of `~/fleet/logs/settle_cycle110_20261016.log` (diff-verified at staging time).
- The c-110 settle script is a mechanical adaptation of the c-109 script (evidence-dir/cycle/label references only; all gates unchanged); labels are machine-derived at runtime from the battery log + extract output (c-92 law) — no typed cycle/key constants.
- 1 ambient frame (0x780B CRC, 20 B, 904.5 MHz, SNR −18.0, non-fleet) present in the session segment; sha-scoped out by the extractor gates.
- Template fixed bytes (`9c85e6a6…`) still ride only open PR branches, not main — fresh-checkout reproduce of step 3 requires the PR-head vendored copy until the launcher sha-guard bytes land on main (caveat carried from c-109, unchanged).
- Known standing item: disk 97% on this node — flagged to the operator again this tick; heavy lanes are the inventoried corpus clones, not fleet evidence.
