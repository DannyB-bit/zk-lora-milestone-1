# groth16_ota cycle-104 — A→B over-the-air Groth16/BN254 proof — key-46 FIRST-OF-CLASS

**Cycle**: 104 · **Drill**: `groth16_ota` · **RX node**: RakMiner-B (Researcher Bravo, Agent 05)
**Primary**: key-46 `c661f2e1c869036c48a2be62aaaa5c588d953b0ed829f87aa8ef5d5f8c772205` (deposit 100015, identity era VK `78352ffa…`)
**Class assertion**: made by the battery's machine class-scan only (c-92 law — never pre-labeled).

## Window (declare via `declare_rx_window.py` v1.0, composer law c-78)
- Armed **2026-10-14T22:13:15Z** → closed **2026-10-15T00:13:15Z** (7200 s), B-bus seq 1656 / A-bus mirror seq 657.
- Certification: `LORA_CHIRP_RECOVERY_PASS=YES` at 22:13:15Z (gate pass #16 in standby log), chip version 0x10 (v1.0) per HAL banner, listener at "Waiting for packets", skew 0.0 s.
- Declared 23:34:55Z with 2299 s remaining, cache warm per Alpha's refill notice **B1653 == A656 byte-equal** (refill-before-declare law c-94) — key-46 `c661f2e1` / key-47 `32451e4f`, both identity era.
- Alpha's prune report (A656): A-disk root 94% → 89% (1.9G → 3.3G free), zk-lorawan build cache + PR-evidence tarballs + embeddinggemma model pruned; Dan's model files untouched.

## Fire (Alpha's watcher hot path — no LLM turn)
- Alpha declared `groth16_proof_tx` B1658/A658 at 23:34:57Z — **2 s after window-open** (fastest declare yet; previous 80 s avg was cache-refill-era). All fields byte-equal across both buses (dual-bus byte-diff PASS).
- Fired **23:36:16Z** — ~79 s declare-to-fire, 5/5 TX_DONE, exit 0.

## Capture (5/5 CRC-OK, 128 B)
- 5 × 128 B frames, `status 0x10` CRC-OK, 903.9 MHz exact (radio 904.3 MHz, IF −400 kHz), SF9/125 kHz.
- SNR +11.0..+11.2 dB; inter-frame 16.7–16.8 s uniform; count_us 613207342..680267936 (**POST-WRAP branch — machine-selected by the battery selector**, per c-101 law; wrap at ~23:24:50Z).
- 1 × 152 B ambient (CRC-fail, 904.3 MHz, SNR −7.8) correctly rejected by the gate.
- Extract: `b_rx_extract.py` rc=0, `sha256_match: true`, full 64-hex `c661f2e1…772205` == declare == fired.

## T12 full battery (canonical template 6a49d04, sha `9c85e6a6`, exit contract)
- attempt1: **BATTERY_EXIT=0 first try** — PRIMARY key-46 `c661f2e1` **VALID 160.0 s**, class-scan **FIRST-OF-CLASS positively asserted** (prior declares B=0 A=0, pih-only B=0 A=0, unclassable 5), CONTROL-diff1 key-45 `1470c41c` VALID 162.3 s + CONTROL-diff2 key-44 `fa92aa35` VALID 159.6 s, GUARD-AFTER unchanged, SoC 48.7→51.6 °C throttled=0x0, 45 era-skipped candidates (vk_sha256 pin). Log: `t12_cycle104_battery_attempt1.log`.
- **Fifth consecutive first-of-class battery** (c-100 key-42 → c-101 key-43 → c-102 key-44 → c-103 key-45 → c-104 key-46 — all five positively asserted in committed battery logs) — every key-N since the ladder extension has been the first of its class in fleet history.
- Unit test before silicon: `tools/test_t12_battery_template.py` PASS (exit-contract 7-fixture + canonical contracts).

## Settle (Cuneiform devnet, program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- Gated on attempt1 complete-line `BATTERY_EXIT=0` + "PRIMARY VALID + CONTROLS VALID" + GUARD-AFTER unchanged (fail-closed `settle_cycle104.sh`). Executed 00:24:45Z: **REGISTER TX `4pubw3Wf…UsNSUX` slot 511166984 finalized, err null**, record PDA `ntaCosYc…eekrq`, merkleRoot == captured proof SHA, treasury +100000 lamports, 6/6 tests. See `settle_summary.json` + `settle_cycle104_20261014.log`.
- Chain readback (settle-signature gate): signature byte-identical via `getSignaturesForAddress` on the PDA; `confirmationStatus: finalized`. Pass recorded in `settle_summary.json`.

## Honest ledger
- No aborts this cycle: template sha-guard PASS on first attempt, controls restored before battery, extraction clean first pass.
- Fresh branch cut from origin/main (37d5310) strands the c-101/c-102/c-103 control dirs and the canonical tools — restored byte-exact from PR#69 head `8597fcc` (see `control_restore_provenance.json`), the same bytes the c-103 battery verified VALID in-session. **The stranded-by-main regression class persists until PR#66/#67/#68/#69 merge.**
- Declare-to-fire delta machine-computed from raw bus timestamps in the settle script (hand-typed-constant law).
- No window was double-declared; the standby service will re-certify + re-arm window #18 at window close (00:13:15Z), per the continuous-RX posture.
- Battery label `T12_CYCLE104_BATTERY_RUN_UTC` derived from the `--cycle` arg that machine-located the window (c-38 law).
- Cache state after this cycle: key-47 `32451e4f` remains warm (per A656); refill ask for keys 48/49 rides the verdict event (c-94 law).

## Reproduce (fresh checkout of this PR head)
1. `python3 tools/test_t12_battery_template.py` → PASS (exit contract + canonical contracts).
2. `sha256sum evidence/groth16_ota_20261014T2213Z_cycle104/rx_payload_128b.bin` → `c661f2e1…772205`.
3. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261014T2213Z_cycle104/session_slice_cycle104.log --expect-sha c661f2e1c869036c48a2be62aaaa5c588d953b0ed829f87aa8ef5d5f8c772205 --min-size 100` → rc=0, `sha256_match: true`.
4. T12 battery: `bash ~/fleet/scripts/run_t12_c104.sh` pattern with `--cycle 104 --evidence-dir evidence/groth16_ota_20261014T2213Z_cycle104 --guard-log <newest standby log>`; requires live buses + on-disk control payloads (key-45 c-103, key-44 c-102).
5. Settle readback: `getSignaturesForAddress ntaCosYcaQt6Ai2xnojbpFq91PA8D86dvMES7Keekrq` on devnet; verify merkleRoot == payload SHA.
