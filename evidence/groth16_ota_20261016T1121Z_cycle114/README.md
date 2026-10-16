# c-114 — groth16_ota cycle-114 A→B: key-56 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-1 BATTERY_EXIT=0 (first attempt, clean), PRIMARY key-56 VALID + 2 DISTINCT-statement-class controls (key-55, key-54) VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=0652a166a958dd16, prior-declares B=0 A=0 over complete dual-bus history). Settled on Cuneiform Devnet: TX `3poCkJ5TTWcnfV3yRDLg2yR6YUdCnFVzqJWuiNvmR2Ugjt1C5J9dvS7eiD6iDU6qPuRPHCRdpZUrGK6tm7NQHYvX` (slot 511720058, err=null), record PDA `Gm3pVEzBAWhGEke43LW7fQAKQU38qh1v4ii7BiNxkVi9` — chain readback verified from this node (PDA owner = Program `2is5…`, merkle root raw bytes byte-exact in the 103 B digest-only PDA data, settle sig rank-1 in PDA sig-history, bin sha == root). 6 settle tests PASS. PRE-WRAP segment. Eight consecutive release-note loops (c-107..c-114), all first-attempt VALID + settled.**

- **Cycle:** 114 · **Drill:** groth16_ota · **Key:** 56 (`ab66569bdbcf832259741fa035f00cb0f8f09a8dbc6b93cdae8a4831c81a735a`) · **Deposit:** 100025 · **Era:** identity (VK `78352ffa…`, PK `aea2ed17…`)
- **Window:** armed 2026-10-16T11:21:54Z → closes 2026-10-16T13:21:54Z (standby listener session `rx_standby_continuous_20261015T171837Z.log`, arm banner line 1480 of guard log). Declared B1857/A739 at 12:20:44Z by `declare_rx_window.py v1.0`, cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 126466, banner skew 0.0 s, 3671 s remaining at declare. Key-56 drawn per Alpha's A732 refill release ("c-114 can draw key-56 immediately after", byte-diff B==A TRUE at B1839/A732).
- **TX:** Alpha watcher hot-path declared key-56 B1859/A740 at 12:20:45Z (cross-bus byte-diff TRUE, `declare_dual_bus_raw.json`) → fired **2026-10-16T12:22:05Z**, 5/5 TX_DONE, ~80 s declare-to-fire.
- **RX (this node):** 5/5 new CRC-OK 128 B frames @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +11.0..+11.2 dB, inter-frame 16.9/16.8/16.8/16.7 s uniform, count_us 3537678465..3604882011 (PRE-WRAP branch, machine-selected). Extract rc=0, **sha256_match TRUE** vs declare `ab66569b…`.
- **Battery:** attempt-1 clean — PRIMARY key-56 pairing VALID (162.1 s) + controls key-55 (c-113, 159.6 s) + key-54 (c-112, 160.1 s) both VALID; GUARD-BEFORE/AFTER unchanged (binary `4c8e1f8a…`, PK `aea2ed17…`, VK `78352ffa…`); silicon 46.2→52.1 °C, throttled 0x0. CLASS SCAN over complete dual-bus history: statement-class key-56 pih[-1]=`0652a166a958dd16`, prior-declares B=0 A=0, pih-only-priors B=0 A=0 → FIRST-OF-CLASS (positively asserted); label `T12_CYCLE114_BATTERY_RUN_UTC` derived from the window event's own cycle id (c-92 law, never typed). Battery run 2026-10-16T12:44:08Z → BATTERY_EXIT=0 @ 12:52:12Z.
- **Settle (Cuneiform Devnet):** `settle_cycle114.sh` gates passed (BATTERY_EXIT=0 complete line, PRIMARY VALID + CONTROLS VALID verdict, extract sha match + exactly 5 frames digesting to the declared sha, declare/extract SHA byte-equality, dual-bus declare byte-equal, GUARD-AFTER unchanged). REGISTER TX `3poCkJ5T…m7NQHYvX` finalized slot 511720058, record PDA `Gm3pVEzBAWhGEke43LW7fQAKQU38qh1v4ii7BiNxkVi9`, merkle root = proof SHA256 `ab66569b…7a0d`, coords `[88,190,25,150,192,234]` (= proof payload bytes 0..5), treasury fee 100000 lamports, 6/6 tests PASS (`tests_passed.txt`), authority `14aTW9yp…` balance 5.90283052 → 5.90155204 SOL. Chain readback machine-verified from this node (`settle_chain_readback.json`): PDA owner `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, root raw bytes at Anchor offset 62..94 byte-exact, session-id ASCII byte-match, coords byte-match, settle sig in PDA sig-history rank-1 (getSignaturesForAddress), all_byte_checks_pass TRUE.
- **Eight-loop streak:** c-107 (PR#74) · c-108 (PR#74-precursor) · c-109 (PR#75) · c-110 (PR#76) · c-111 (PR#77) · c-112 (PR#78) · c-113 (PR#79) · c-114 (this) — eight consecutive release-note loops, every one first-attempt VALID + Devnet-settled.

## Evidence files
- `session_slice_cycle114.log` — raw RX log slice from the 11:21:54Z arm banner (this node's capture, ground truth)
- `b_rx_extract_output.json` — extractor output: 5/5 CRC-OK, sha256_match TRUE, per-frame count_us/SNR/RSSI + hex
- `b_rx_extract_stderr.log` — extractor stderr (empty, rc=0)
- `rx_payload_128b.bin` — captured 128 B proof payload (SHA `ab66569b…7a0d`)
- `cycle114_window_declare.json` — machine-parsed window declare (B1857/A739)
- `declare_dual_bus_raw.json` — dual-bus declare/fired/window/refill, byte-diff TRUE/TRUE
- `capture_meta.json` — window seq stamps, fire stamp, per-frame SNR/count_us/gaps
- `t12_cycle114_battery_attempt1.log` — T12 pairing battery, BATTERY_EXIT=0 (also mirrored at `~/fleet/logs/`)
- `t12_cycle114_battery.log` — battery stdout mirror
- `control_provenance.json` — primary + 2 controls machine-sourced (c-91 law); control bins verified byte-exact in this branch tree against the battery-quoted prefixes + dual-bus declares
- `inflight_marker_event.json` — c-100 twin-tick race marker (B1864/A743): pipeline owned by the 12:0xZ tick, concurrent ticks stood down
- `rx_capture_confirmed_event.json` / `rx_verdict_event.json` — bus-first verdict events as posted (B1862/A742, B1865/A744)
- `settle_cycle114.log` — settle gate output (TX, PDA, root, fee, 6/6 PASS); machine-composed from the settle's on-disk artifacts per the c-109 composition law (every value read from `result_summary.txt` + `settle_chain_readback.json`, zero retyped constants)
- `settle_chain_readback.json` — RPC chain readback: owner/root/session/coords byte-exact, sig-history verified
- `result_summary.txt`, `tests_passed.txt` — machine-written settle artifacts (app artifacts mirror)

## Reproduce (from a fresh checkout of this PR head)
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261016T1121Z_cycle114/session_slice_cycle114.log --expect-sha ab66569bdbcf832259741fa035f00cb0f8f09a8dbc6b93cdae8a4831c81a735a --min-size 128` → rc=0, `sha256_match: true`
2. `sha256sum evidence/groth16_ota_20261016T1121Z_cycle114/rx_payload_128b.bin` → `ab66569bdbcf832259741fa035f00cb0f8f09a8dbc6b93cdae8a4831c81a735a`
3. `python3 tools/chain_readback_v2.py --pda Gm3pVEzBAWhGEke43LW7fQAKQU38qh1v4ii7BiNxkVi9 --expect-root ab66569bdbcf832259741fa035f00cb0f8f09a8dbc6b93cdae8a4831c81a735a --expect-session ab66569bdbcf8322 --expect-coords 88,190,25,150,192,234` → verdict PASS
4. T12 battery: run `tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 114 --evidence-dir evidence/groth16_ota_20261016T1121Z_cycle114 --guard-log <this node's live standby log>` — note the guard log lives on the RX node; the committed `session_slice_cycle114.log` + `declare_dual_bus_raw.json` pin the burst machine-locatably for reviewers (battery log `t12_cycle114_battery_attempt1.log` is the record of the bytes that ran, template sha `9c85e6a6…` pinned by the launcher's EXPECT_TPL_SHA guard).

— Researcher Bravo (Agent 05, RakMiner-B), 2026-10-16T13:0xZ
