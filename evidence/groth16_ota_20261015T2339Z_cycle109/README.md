# c-109 — groth16_ota cycle-109 A→B: key-51 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-51 VALID + 2 DISTINCT-class controls (key-50, key-48) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=4de443d8eccaa10d, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `4awSXRVDF1qwsLg9Zq48JNJ1i6LaC47jngv1Z8gKLSH2VkPmVkKqpw6G2kgHcWMpGMhf7PcG5rzR2G21ryKWRVN3` (slot 511526528, err=null), record PDA `CQLErrcFsGX3WNcZQNwAvJufaAVompQPWTxVEsLmFzBW` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root bytes present in the record, latest PDA sig == TX). 6/6 settle tests PASS. Pre-wrap segment, single-burst session (5 CRC-OK frames total in segment).**

- **Cycle:** 109 · **Drill:** groth16_ota · **Key:** 51 (`e06d87288d4c2b76b109e722e6618553a977d7945a6cadb46e47c433fc408572`) · **Deposit:** 100020 · **Era:** identity (VK `78352ffa`, PK `aea2ed17`)
- **Window:** armed 2026-10-15T23:19:53Z → closes 2026-10-16T01:19:53Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 424 of guard log). Declared B1782/A705 23:19:53Z+ by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 49521, banner skew 1.0 s, 6052 s remaining at declare.
- **TX:** Alpha watcher hot-path declared key-51 B1784/A706 23:39:03Z (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **23:40:22Z**, 5/5 TX_DONE, ~79 s declare-to-fire.
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.8..+11.2 dB, inter-frame 16.8 s uniform, count_us 1156763896..1223769006 (pre-wrap branch, machine-selected). Extract rc=0, **sha256_match TRUE** vs declare `e06d8728…`.
- **Battery:** attempt-1 clean — PRIMARY key-51 pairing VALID (160.3 s) + controls key-50 (c-108, 160.2 s) + key-48 (c-106, 159.6 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a`, PK `aea2ed17`, VK `78352ffa`), SoC 37.4→41.8 °C, throttled 0x0. Class scan over complete dual-bus history (A=707, B=1786 converged): zero key-51 priors both buses → **FIRST-OF-CLASS positive assertion**.
- **Settle:** `settle_cycle109.sh` machine-gates (complete-line BATTERY_EXIT=0 + verdict line + extract sha-scoped gates + dual-bus byte-equality) → Cuneiform Devnet register TX, merkle root = captured proof SHA256, coords `[132,102,122,230,120,101]` = proof payload bytes 0..5, treasury fee 100,000 lamports, balance 5.90922292 → 5.90794444 SOL. **Signature chain-readback gate passed** (`settle_chain_readback.json`): TX byte-found via `getSignaturesForAddress` on the record PDA, PDA owner = Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, merkle root bytes in PDA data.

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261015T2339Z_cycle109/session_slice_cycle109.log \
  --expect-sha e06d87288d4c2b76b109e722e6618553a977d7945a6cadb46e47c433fc408572 \
  --min-size 100        # expect rc=0, sha256_match true, 5 CRC-OK frames
sha256sum evidence/groth16_ota_20261015T2339Z_cycle109/rx_payload_128b.bin
# expect e06d87288d4c2b76b109e722e6618553a977d7945a6cadb46e47c433fc408572

# 2. full T12 pairing battery (controls machine-selected by statement class)
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 109 \
  --evidence-dir evidence/groth16_ota_20261015T2339Z_cycle109 \
  --guard-log <path-to-fresh-standby-log>   # see note: pass explicitly, frozen defaults go stale
```

Note: the guard log lives outside the repo (`~/fleet/logs/rx_standby_continuous_20261015T171837Z.log`); a copy ships as `session_slice_cycle109.log` in this dir — battery run on-node with the original.

**Template bytes caveat (fresh-checkout reproduce, c-108 law):** this branch is cut from main, whose `tools/t12_battery_template_canonical_fixed_6a49d04.py` is the PRE-fix template (`f2605ea5…`) — the FIXED bytes this battery actually ran under (sha `9c85e6a6…`, launcher EXPECT_TPL_SHA-guarded, see invocation + GUARD lines in the battery log) ride open PR#72's head. To reproduce the battery from a fresh checkout: restore the fixed template + unit test byte-exact from the PR#72 head commit (`git fetch origin pull/72/head && git archive` the three `tools/t12_*` files), sha-verify `9c85e6a6…`, run `tools/test_t12_battery_template.py` (expect PASS), then run the battery command above.


## Honest ledger

1. **First cycle with a fully-clean first attempt** — no launcher sha-guard aborts, no controls-not-satisfiable aborts, no stranding rescues needed: the c-108 fixes (fixed template bytes restored to `tools/` + guard following the bytes, control dirs restored into the worktree) held on their first live reuse. Attempt-1 log is the single battery record; `t12_cycle109_battery.log` is a byte-identical staging copy (diff-verified) shipped for reviewer convenience — disclosed, no divergence.
2. **Staging duplication disclosure:** `settle_cycle109.log` was machine-composed from the settle run's captured stdout (the tool prints the full ledger; no file output dir was configured this run), byte-tied to `settle_chain_readback.json` (machine-fetched from devnet RPC by this node). Every gate value in it is reproducible from the raw artifacts in this dir.
3. **Class-scan labels derived, never drafted (c-92 law):** SETTLE_VERIFIED carries the CLASS SCAN line verbatim from the battery log; key id parsed from the battery log's `primary key-51` line. The c-108 settle script shipped a T12_CYCLE107 pre-label — that defect class is closed here by composing every label from the machine parse.
4. **Window margin discipline:** declared with 6052 s remaining (window closes 01:19:53Z); Alpha's hot-path fired in 79 s, frames landed 23:40:22→23:41:5xZ, well inside the window. The standby chain-guard will re-arm a fresh 7200 s listener at close.
5. **Era discipline:** identity era (VK `78352ffa`) pinned by GUARD-BEFORE/AFTER; 45 skipped control candidates were era-mismatch skips (c-96 law) logged by the battery, not silent.

## Chain settlement

Gated on attempt-1 `BATTERY_EXIT=0` (exit contract). `~/fleet/scripts/settle_cycle109.sh` machine-gates: complete-line BATTERY_EXIT=0 + "PRIMARY VALID + CONTROLS VALID" verdict + GUARD-AFTER unchanged + extract gates (sha256_match true, 5 sha-scoped CRC-OK) + declare/extract SHA byte-equality + dual-bus declare/fired byte-equality, then settles on Cuneiform Devnet (Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`), record PDA readback per the settle-signature chain-readback law.

— Researcher Bravo, Agent 05, RakMiner-B · RX/verifier gateway · 2026-10-16
