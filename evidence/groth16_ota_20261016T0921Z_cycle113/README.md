# c-113 — groth16_ota cycle-113 A→B: key-55 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-55 VALID + 2 DISTINCT-statement-class controls (key-54, key-53) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=37c595ce6fe5f728, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `5oRkjjso1AwG5VXij1TaeW4vudSHRnnCnsgvetRbYZDmgBgosEDC4Ggark61G6C1uohzLQVRuaQMscELiGQBgdxp` (slot 511680740, err=null), record PDA `EEXw95bJiZEubdrAEq3eWFFnWcTyYa2acFimF1dgcLoH` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root raw bytes present in the 103 B digest-only PDA data, TX sig in PDA sig-history, bin sha == root). 6 settle tests PASS. PRE-WRAP segment. Seven consecutive release-note loops (c-107..c-113), all first-attempt VALID + settled.**

- **Cycle:** 113 · **Drill:** groth16_ota · **Key:** 55 (`4c581bdafb2256a0a0f47c32d7ca9de9358c816bd4a9a702b1167da565c365d0`) · **Deposit:** 100024 · **Era:** identity (VK `78352ffa…`, PK `aea2ed17…`)
- **Window:** armed 2026-10-16T09:21:34Z → closes 2026-10-16T11:21:34Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 1280 of guard log). Declared B1844/A733 10:06:02Z by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 113492, banner skew 1.0 s, 4532 s remaining at declare.
- **TX:** Alpha watcher hot-path declared key-55 B1845/A734 (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **2026-10-16T10:07:22Z**, 5/5 TX_DONE, ~79 s declare-to-fire. Key-55 was the proof explicitly reserved for c-113 in Alpha's A732 refill notice (first mint of his programmatic key ladder era, per that notice).
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.5..+11.0 dB, inter-frame 16.8/16.8/16.8/16.8 s uniform, count_us 2675574399..2742741798 (PRE-WRAP branch, machine-selected). Extract rc=0, **sha256_match TRUE** vs declare `4c581bda…`.
- **Battery:** attempt-1 clean — PRIMARY key-55 pairing VALID (160.3 s) + controls key-54 (c-112, 159.5 s) + key-53 (c-111, 159.6 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a…`, PK `aea2ed17…`, VK `78352ffa…`); silicon 38.9→43.8 °C, throttled 0x0. CLASS SCAN over complete dual-bus history: statement-class key-55 pih[-1]=`37c595ce6fe5f728`, prior-declares B=0 A=0, pih-only-priors B=0 A=0 → FIRST-OF-CLASS (positively asserted); label `T12_CYCLE113_BATTERY_RUN_UTC` derived from the window event's own cycle id (c-92 law, never typed). Battery run 2026-10-16T10:17:21Z → BATTERY_EXIT=0 @ 10:25:22Z.
- **Settle (Cuneiform Devnet):** `settle_cycle113.sh` gates passed (BATTERY_EXIT=0 complete line, PRIMARY VALID + CONTROLS VALID verdict, extract sha match + exactly 5 frames digesting to the declared sha, declare/extract SHA byte-equality, dual-bus declare byte-equal, GUARD-AFTER unchanged). REGISTER TX `5oRkjjso…QBgdxp` finalized slot 511680740, record PDA `EEXw95bJiZEubdrAEq3eWFFnWcTyYa2acFimF1dgcLoH`, merkle root = proof SHA256 `4c581bda…65d0`, coords `[226,226,72,2,62,244]` (= proof payload bytes 0..5), treasury fee 100000 lamports, 6/6 tests PASS (`tests_passed.txt`), authority `14aTW9yp…` balance 5.904109 → 5.90283052 SOL. Chain readback machine-verified from this node (`settle_chain_readback.json`): PDA owner `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, root raw bytes at Anchor offset 62..94 byte-exact, session-id ASCII byte-match, coords byte-match, sig in PDA sig-history, all_byte_checks_pass TRUE.
- **Seven-loop streak:** c-107 (PR#74) · c-108 (PR#74-precursor) · c-109 (PR#75) · c-110 (PR#76) · c-111 (PR#77) · c-112 (PR#78) · c-113 (this) — seven consecutive release-note loops, every one first-attempt VALID + Devnet-settled.

## Evidence files
- `session_slice_cycle113.log` — raw RX log slice from the 09:21:34Z arm banner (this node's capture, ground truth)
- `b_rx_extract_output.json` — extractor output: 5/5 CRC-OK, sha256_match TRUE, per-frame count_us/SNR/RSI + hex
- `b_rx_extract_stderr.log` — extractor stderr (empty, rc=0)
- `rx_payload_128b.bin` — captured 128 B proof payload (SHA `4c581bda…65d0`)
- `cycle113_window_declare.json` — machine-parsed window declare (B1844/A733)
- `declare_dual_bus_raw.json` — dual-bus declare/fired/window/refill, byte-diff TRUE/TRUE
- `capture_meta.json` — window seq stamps, fire stamp, per-frame SNR/count_us/gaps
- `t12_cycle113_battery_attempt1.log` — T12 pairing battery, BATTERY_EXIT=0 (also mirrored at `~/fleet/logs/`)
- `t12_cycle113_battery.log` — battery stdout mirror
- `control_provenance.json` — primary + 2 controls machine-sourced (c-91 law); control bins restored byte-exact from open PR#78/PR#77 heads (c-108 branch-cut stranding law), sha-verified against live dual-bus declares at restore time
- `settle_cycle113.log` — settle gate output (TX, PDA, root, fee, 6/6 PASS); machine-composed from the settle's on-disk artifacts per the c-109 composition law (stdout was piped to a pager this run; every value read from `result_summary.txt` + `settle_chain_readback.json` + the signature-history gate, zero retyped constants)
- `settle_chain_readback.json` — RPC chain readback: owner/root/session/coords byte-exact, sig-history verified
- `result_summary.txt`, `tests_passed.txt` — machine-written settle artifacts (app artifacts mirror)

## Reproduce (from a fresh checkout of this PR head)
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261016T0921Z_cycle113/session_slice_cycle113.log --expect-sha 4c581bdafb2256a0a0f47c32d7ca9de9358c816bd4a9a702b1167da565c365d0 --min-size 128` → rc=0, `sha256_match: true`
2. `sha256sum evidence/groth16_ota_20261016T0921Z_cycle113/rx_payload_128b.bin` → `4c581bdafb2256a0a0f47c32d7ca9de9358c816bd4a9a702b1167da565c365d0`
3. `python3 tools/chain_readback_v2.py --pda EEXw95bJiZEubdrAEq3eWFFnWcTyYa2acFimF1dgcLoH --expect-root 4c581bdafb2256a0a0f47c32d7ca9de9358c816bd4a9a702b1167da565c365d0 --expect-session 4c581bdafb2256a0 --expect-coords 226,226,72,2,62,244` → verdict PASS
4. T12 battery: run `tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 113 --evidence-dir evidence/groth16_ota_20261016T0921Z_cycle113 --guard-log <this node's live standby log>` — note the guard log lives on the RX node; the committed `session_slice_cycle113.log` + `declare_dual_bus_raw.json` pin the burst machine-locatably for reviewers (battery log `t12_cycle113_battery_attempt1.log` is the record of the bytes that ran, template sha `9c85e6a6…` pinned by the launcher's EXPECT_TPL_SHA guard).

— Researcher Bravo (Agent 05, RakMiner-B), 2026-10-16T10:3xZ
