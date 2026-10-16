# c-111 — groth16_ota cycle-111 A→B: key-53 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-53 VALID + 2 DISTINCT-class controls (key-52, key-51) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=86776c77a01c8121, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `4eJdMS1zymwpFFe7CocQmPD9J2KJDJZCG7MVPiijZEch8WY2pxsmfn2N58LZsrpuKAfoZdTDdcZeJjqP6W8TcaEy` (slot 511604636, err=null), record PDA `31vgYJAGE6dMutcXgQnFguUGSy1hTGFgTnjxdDQ2XiC6` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root bytes present in the 103 B digest-only PDA data, TX sig in PDA sig-history, bin sha == root). 6 settle tests PASS. POST-WRAP segment. Five consecutive release-note loops (c-107..c-111), all first-attempt VALID + settled.**

- **Cycle:** 111 · **Drill:** groth16_ota · **Key:** 53 (`2febd2ee660af9cf31d3a848d7ccc8d865e24c05fc114b2069144ca81cc66352`) · **Deposit:** 100022 · **Era:** identity (VK `78352ffa…`, PK `aea2ed17…`)
- **Window:** armed 2026-10-16T03:20:33Z → closes 2026-10-16T05:20:33Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 744 of guard log). Declared B1813/A719 05:04:43Z by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 74772, banner skew 1.0 s, 950 s remaining at declare.
- **TX:** Alpha watcher hot-path declared key-53 B1814/A720 05:04:43Z (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **2026-10-16T05:06:03Z**, 5/5 TX_DONE, ~80 s declare-to-fire.
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.8..+11.8 dB, inter-frame 16.7/16.7/16.7/16.7 s uniform, count_us 1961953284..2028925833 (POST-WRAP branch, machine-selected — second consecutive post-wrap capture). Extract rc=0, **sha256_match TRUE** vs declare `2febd2ee…`.
- **Battery:** attempt-1 clean — PRIMARY key-53 pairing VALID (160.1 s) + controls key-52 (c-110, 161.3 s) + key-51 (c-109, 159.9 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a…`, PK `aea2ed17…`, VK `78352ffa…`), SoC 37.4→41.3 °C, throttled 0x0. Class scan over complete dual-bus history (converged): zero key-53 priors both buses → **FIRST-OF-CLASS positive assertion**. Battery run 2026-10-16T05:11:57Z.
- **Settle:** `settle_cycle111.sh` machine-gates (complete-line BATTERY_EXIT=0 + verdict line + extract sha-scoped gates + dual-bus byte-equality) → Cuneiform Devnet register TX, merkle root = captured proof SHA256, coords `[170, 83, 209, 13, 175, 70]` = proof payload bytes 0..5, treasury fee 100,000 lamports, balance 5.90666596 → 5.90538748 SOL. **Signature chain-readback gate passed** (`settle_chain_readback.json`): TX byte-found via `getSignaturesForAddress` on the record PDA, PDA owner = Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, merkle root bytes in PDA data, tx err=null.
- **Loop cadence:** c-107/108/109/110/111 — five consecutive release-note loops, each declare→fire→capture→battery→settle inside one window, all first-attempt VALID+settled. This cycle consumed the ladder's last warm proof (key-53); refill ask for keys 54+55 dispatched to Alpha (outbox brief 0032 + peer-run wake `c111-refill-wake-20261016T0530Z`).

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates (full 64-hex digest, fail-closed exit contract)
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261016T0506Z_cycle111/session_slice_cycle111.log \
  --expect-sha 2febd2ee660af9cf31d3a848d7ccc8d865e24c05fc114b2069144ca81cc66352 \
  --min-size 100
# rc=0 + sha256_match:true + 5 CRC-OK frames digesting to the declared sha

# 2. payload bytes == committed bin
sha256sum evidence/groth16_ota_20261016T0506Z_cycle111/rx_payload_128b.bin
# -> 2febd2ee660af9cf31d3a848d7ccc8d865e24c05fc114b2069144ca81cc66352

# 3. T12 battery (same-session controls; template sha-guarded by the launcher)
bash ~/fleet/scripts/launch_t12_cycle111.sh attempt2
# -> BATTERY_EXIT=0, PRIMARY key-53 VALID + controls key-52/key-51 VALID
# (fixed template bytes 9c85e6a6… still ride open PR branches, not main — fresh-checkout
#  reproduce requires the PR-head vendored copy until the bytes land on main)

# 4. settle gate re-run (idempotent, fail-closed on any gate)
bash ~/fleet/scripts/settle_cycle111.sh
# -> GROTH16_OTA_SETTLED_ON_CHAIN=YES, 6/6 tests
# (idempotent fail-closed: a fresh PDA gate blocks a second register — re-run asserts gates only)

# 5. chain readback (independent)
#   sig history of record PDA contains REGISTER_TX; PDA owner = 2is5…; root bytes in PDA data
cat evidence/groth16_ota_20261016T0506Z_cycle111/settle_chain_readback.json
```

## Honest ledger

- Attempt-1 was the only battery attempt; no aborts, no quarantines, no stranding rescues this cycle.
- `settle_cycle111.log` in this dir is the staging copy of `~/fleet/logs/settle_cycle111_20261016.log` (tee'd at settle time).
- The c-111 settle script is a mechanical adaptation of the c-110 script (evidence-dir/cycle/label references only; all gates unchanged); labels are machine-derived at runtime from the battery log + extract output (c-92 law) — the two stale c-110 header-comment references were corrected before first execution (disclosed here).
- Ambient frames in the session segment, sha-scoped out by the extractor gates: 0 — none.
- `b_rx_extract_stderr.log` (0 bytes) ships as the extract's clean-stderr witness.
- Template fixed bytes (`9c85e6a6…`) still ride only open PR branches, not main (caveat carried from c-109/c-110, unchanged).
- Known standing item: disk 97% on this node — flagged to the operator again this tick; heavy lanes are the inventoried corpus clones, not fleet evidence.
