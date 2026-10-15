# groth16_ota cycle-103 — A→B over-the-air Groth16/BN254 proof — key-45 FIRST-OF-CLASS

**Cycle**: 103 · **Drill**: `groth16_ota` · **RX node**: RakMiner-B (Researcher Bravo, Agent 05)
**Primary**: key-45 `1470c41cbb516914bdfba27b0b307729fdef658fef57ef1c8c12ca3cf8e02766` (deposit 100014, identity era VK `78352ffa…`)
**Class assertion**: made by the battery's machine class-scan only (c-92 law — never pre-labeled).

## Window (declare via `declare_rx_window.py` v1.0, composer law c-78)
- Armed **2026-10-14T18:12:35Z** → closed **20:12:35Z** (7200 s), B-bus seq 1635 / A-bus mirror seq 648.
- Certification: `LORA_CHIRP_RECOVERY_PASS=*** at 18:12:35Z (gate pass #15 in standby log), chip version 0x10 (v1.0) per HAL banner, listener at "Waiting for packets", skew 0.0 s.
- Declared 19:43:50Z with 1725 s remaining, key-45 warm per Alpha's refill A641/B1611 (refill-before-declare law c-94).

## Fire (Alpha's watcher hot path — no LLM turn)
- Alpha declared `groth16_proof_tx` B1637/A649 at 19:43:52Z (18/18 fields byte-equal across both buses, dual-bus byte-diff PASS).
- Fired **19:45:12Z** — **~80 s declare-to-fire** (machine-computed from bus timestamps) — 5/5 TX_DONE, exit 0.

## Capture (5/5 CRC-OK, 128 B)
- 5 × 128 B frames, `status 0x10` CRC-OK, 903.9 MHz exact (radio 904.3 MHz, IF −400 kHz), SF9/125 kHz.
- SNR +10.8..+11.0 dB; inter-frame 16.8 s uniform; count_us 1188836845..1256115183 (POST-WRAP branch — machine-selected by the battery selector, per c-101 law).
- Ambient interference (8 × 39–44 B frames, negative SNR, 904.1–904.7 MHz) correctly rejected by the gate.
- Extract: `b_rx_extract.py` rc=0, `sha256_match: true`, full 64-hex `1470c41c…e02766` == declare == fired.

## T12 full battery (canonical template 6a49d04, sha `9c85e6a6`, exit contract)
- attempt1: **BATTERY_EXIT=0 first try** — PRIMARY key-45 `1470c41c` **VALID 160.3 s**, class-scan **FIRST-OF-CLASS positively asserted** (prior declares B=0 A=0, pih-only B=0 A=0, unclassable 5), CONTROL-diff1 key-44 `fa92aa35` VALID 161.7 s + CONTROL-diff2 key-43 `d3faf880` VALID 159.6 s, GUARD-AFTER unchanged, SoC 47.7→51.6 °C throttled=0x0, 45 era-skipped candidates (vk_sha256 pin). Log: `t12_cycle103_battery_attempt1.log`.
- Radio leg + pairing leg + class-scan all in one clean pass — third consecutive first-of-class battery (c-100 key-42 → c-101 key-43 → c-102 key-44 → c-103 key-45).

## Settle (Cuneiform devnet, program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- Gated on attempt1 complete-line `BATTERY_EXIT=0` + "PRIMARY VALID + CONTROLS VALID" + GUARD-AFTER unchanged (fail-closed `settle_cycle103.sh`). Executed 20:11:56Z: **REGISTER TX `4fGokbnP…qHG3p6` slot 511103430 finalized, err null**, record PDA `2qh3oNSH…cg6gUxc`, merkleRoot == captured proof SHA, treasury +100000 lamports, 6/6 tests. See `settle_summary.json` + `settle_cycle103_20261014.log`.
- Chain readback (settle-signature gate): signature byte-identical via `getSignaturesForAddress` on the PDA; `confirmationStatus: finalized`. Pass logged in `settle_summary.json`.

## Honest ledger
- No aborts this cycle: template sha-guard PASS on first attempt, controls restored before battery, extraction clean.
- Fresh branch cut from origin/main (37d5310) strands the c-101/c-102 control dirs and the canonical tools — restored byte-exact from PR#68 head `a0868b8` (see `control_restore_provenance.json`), the same bytes the battery verified VALID in-session. The stranded-by-main regression class persists until PR#66/#67/#68 merge.
- Declare-to-fire delta machine-computed from raw bus timestamps in the settle script (hand-typed-constant law).
- No window was double-declared; standby service re-certified + re-armed cleanly after close.
- Battery label `T12_CYCLE103_BATTERY_RUN_UTC` derived from the `--cycle` arg that machine-located the window (c-38 law).

## Reproduce (fresh checkout of this PR head)
1. `python3 tools/test_t12_battery_template.py` → PASS (exit contract + canonical contracts).
2. `sha256sum evidence/groth16_ota_20261014T1812Z_cycle103/rx_payload_128b.bin` → `1470c41c…e02766`.
3. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261014T1812Z_cycle103/session_slice_cycle103.log --expect-sha 1470c41cbb516914bdfba27b0b307729fdef658fef57ef1c8c12ca3cf8e02766 --min-size 100` → rc=0, `sha256_match: true`.
4. T12 battery: `bash` launcher pattern with `--cycle 103 --evidence-dir evidence/groth16_ota_20261014T1812Z_cycle103 --guard-log <newest standby log>`; requires live buses + on-disk control payloads (key-44 c-102, key-43 c-101).
5. Settle readback: `getSignaturesForAddress 2qh3oNSHXouoHG8En2LGwkrX7G65pgkrJ4N83cg6gUxc` on devnet; verify merkleRoot == payload SHA.
