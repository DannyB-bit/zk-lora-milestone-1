# c-112 — groth16_ota cycle-112 A→B: key-54 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-54 VALID + 2 DISTINCT-statement-class controls (key-53, key-51) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=4828073c2b81bc18, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `31KVhR1KF83aqF6PzZJ1tZUYvPe55bwyPRLMLMp789fbY5xeQhbrWyRHHpLH6nzW3T267ke42H9dEUF6Eoq2cLHn` (slot 511645268, err=null), record PDA `BhKmXnMx2nzw7jY1r8VBiJPYp526Fmu4F8vyz4pnhmeo` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root bytes present in the 103 B digest-only PDA data, TX sig in PDA sig-history, bin sha == root). 6 settle tests PASS. PRE-WRAP segment. Six consecutive release-note loops (c-107..c-112), all first-attempt VALID + settled.**

- **Cycle:** 112 · **Drill:** groth16_ota · **Key:** 54 (`ae28031841207fce4b96aa6cd23f40e10dd5f10db5d548c7c519a53b4236cf20`) · **Deposit:** 100023 · **Era:** identity (VK `78352ffa…`, PK `aea2ed17…`)
- **Window:** armed 2026-10-16T07:21:14Z → closes 2026-10-16T09:21:14Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 1064 of guard log). Declared B1829/A726 07:33:2xZ by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 99745, banner skew 1.0 s, 6193 s remaining at declare.
- **TX:** Alpha watcher hot-path declared key-54 B1831/A727 (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **2026-10-16T07:39:23Z**, 5/5 TX_DONE, ~80 s declare-to-fire.
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +11.0..+11.2 dB, inter-frame 16.7/16.7/16.7/16.9 s uniform, count_us 1016095709..1083185990 (PRE-WRAP branch, machine-selected). Extract rc=0, **sha256_match TRUE** vs declare `ae280318…`.
- **Battery:** attempt-1 clean — PRIMARY key-54 pairing VALID + controls key-53 (c-111, 160.1 s) + key-51 (c-109, 159.9 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a…`, PK `aea2ed17…`, VK `78352ffa…`); CLASS SCAN over complete dual-bus history: statement-class key-54 pih[-1]=`4828073c2b81bc18`, prior-declares B=0 A=0, pih-only-priors B=0 A=0 → FIRST-OF-CLASS (positively asserted); label `T12_CYCLE112_BATTERY_RUN_UTC` derived from the window event's own cycle id (c-92 law, never typed). Battery run 2026-10-16T07:58:50Z → BATTERY_EXIT=0 @ 08:06:52Z.
- **Settle (Cuneiform Devnet):** `settle_cycle112.sh` gates passed (BATTERY_EXIT=0 complete line, PRIMARY VALID + CONTROLS VALID verdict, extract sha match + exactly 5 frames digesting to the declared sha, declare/extract SHA byte-equality, dual-bus declare byte-equal, GUARD-AFTER unchanged). REGISTER TX `31KVhR1K…cLHn` finalized slot 511645268, record PDA `BhKmXnMx2nzw7jY1r8VBiJPYp526Fmu4F8vyz4pnhmeo`, merkle root = proof SHA256 `ae280318…cf20`, coords `[99,214,195,77,172,128]` (= proof payload bytes 0..5), treasury fee 100000 lamports, 6/6 tests PASS (`tests_passed.txt`), authority `14aTW9yp…` balance 5.90538748 → 5.904109 SOL. Chain readback machine-verified from this node (`settle_chain_readback.json`): PDA owner `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, root bytes in 103 B PDA data, sig in PDA sig-history, `bin_equals_root` TRUE.
- **Six-loop streak:** c-107 (PR#74) · c-108 (PR#75-precursor) · c-109 (PR#75) · c-110 (PR#76) · c-111 (PR#77) · c-112 (this) — six consecutive release-note loops, every one first-attempt VALID + Devnet-settled.

## Evidence files
- `session_slice_cycle112.log` — raw RX log slice from the 07:21:14Z arm banner (this node's capture, ground truth)
- `b_rx_extract_output.json` — extractor output: 5/5 CRC-OK, sha256_match TRUE, per-frame count_us/SNR/RSI + hex
- `b_rx_extract_stderr.log` — extractor stderr (empty, rc=0)
- `rx_payload_128b.bin` — captured 128 B proof payload (SHA `ae280318…cf20`)
- `cycle112_window_declare.json` — machine-parsed window declare (B1829/A726)
- `declare_dual_bus_raw.json` — dual-bus declare/fired/window/refill, byte-diff TRUE/TRUE
- `capture_meta.json` — window seq stamps (B1829/A726, armed/closes)
- `t12_cycle112_battery_attempt1.log` — T12 pairing battery, BATTERY_EXIT=0 (also mirrored at `~/fleet/logs/`)
- `t12_cycle112_battery.log` — battery stdout mirror
- `control_provenance.json` — primary + 2 controls machine-sourced (c-91 law)
- `settle_cycle112.log` — settle gate output (TX, PDA, root, fee, 6/6 PASS)
- `settle_chain_readback.json` — RPC chain readback: owner/root/sig-history verified
- `result_summary.txt`, `tests_passed.txt` — machine-written settle artifacts (app artifacts mirror)

— Researcher Bravo (Agent 05, RakMiner-B), 2026-10-16T08:1xZ
