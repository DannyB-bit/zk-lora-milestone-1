# groth16_ota cycle-102 — A→B over-the-air Groth16/BN254 proof — key-44 FIRST-OF-CLASS candidate

**Cycle**: 102 · **Drill**: `groth16_ota` · **RX node**: RakMiner-B (Researcher Bravo, Agent 05)
**Primary**: key-44 `fa92aa353492e907d86def4e6283f4d6d1dd6af2130322b554afad3e50a7d06c` (deposit 100013, identity era VK `78352ffa…`)
**Class assertion**: made by the battery's machine class-scan only (c-92 law — never pre-labeled).

## Window (declare via `declare_rx_window.py` v1.0, composer law c-78)
- Armed **2026-10-14T14:11:54Z** → closed **16:11:54Z** (7200 s), B-bus seq 1618 / A-bus mirror seq 642.
- Certification: `LORA_CHIRP_RECOVERY_PASS=YES` at 14:11:54Z (gate pass #11 in standby log), chip version 0x10 (v1.0) per HAL banner, listener at "Waiting for packets", skew 0.0 s.
- Declared 16:05:48Z with 366 s remaining, after the c-102 refill (A seq 641: key-44 + key-45 warm — refill-before-declare law c-94).

## Fire (Alpha's watcher hot path — no LLM turn)
- Alpha declared `groth16_proof_tx` B1620/A643 at 16:05:50Z (18/18 fields byte-equal across both buses, dual-bus byte-diff PASS).
- Fired **16:07:10Z** — **~80 s declare-to-fire** (machine-computed from bus timestamps) — 5/5 TX_DONE, exit 0.

## Capture (5/5 CRC-OK, 128 B)
- 5 × 128 B frames, `status 0x10` CRC-OK, 903.9 MHz exact (radio 904.3 MHz, IF −400 kHz), SF9/125 kHz.
- SNR +10.5..+11.0 dB; inter-frame 16.8 s uniform; count_us 2547424724..2614680655 (POST-WRAP branch — machine-selected by the battery selector, per c-101 law).
- Burst walls vs fired stamp: burst spans ~16:05:5xZ→16:07:0xZ (post-wrap recovery), fired completion 16:07:10Z — causal, in-window, ~4.7 min before close.
- Extract: `b_rx_extract.py` rc=0, `sha256_match: true`, full 64-hex `fa92aa35…a7d06c` == declare == fired.

## T12 full battery (canonical template 6a49d04, sha `9c85e6a6`, exit contract)
- attempt1: **ABORT pre-silicon** — launcher sha-guard refused: on-disk canonical was `f2605ea5` (pre-fix bytes, no `sys.exit(main())`). Root cause: the c-101 tick cut PR#67's branch from origin/main (37d5310), which does NOT contain the 612292c port (that lives on open PR#66's branch) — the branch switch silently reverted `tools/` to origin/main bytes. Guard worked exactly as designed; abort log kept as honest history.
- Restore (this cycle, c-100 port law): fresh branch off origin/main → byte-exact restore of canonical + unit test from pr66-head (612292c) → non-canonical + unit test from pr58-current (33eefd9) → **unit test PASS** (mapping 7 fixtures + canonical era-pin + phantom-join + entry contracts) → attempt2 relaunch.
- attempt2: ABORT `control classes not satisfiable` — **BATTERY_EXIT=1 propagated** (exit contract WORKED: the pre-fix bytes would have printed 0). Cause: the fresh branch off origin/main dropped the tracked control-payload dirs (c-98/99/100/101 evidence lives on unmerged PR branches — stranded-controls class, c-91 law). Fixed by byte-exact restore + bus-verified provenance (see `control_restore_provenance.json`).
- attempt3: **BATTERY_EXIT=0** — PRIMARY key-44 `fa92aa35` **VALID 160.1 s**, class-scan **FIRST-OF-CLASS positively asserted** (prior declares B=0 A=0, pih-only B=0 A=0, unclassable 5), CONTROL-diff1 key-43 `d3faf880` VALID 159.7 s + CONTROL-diff2 key-42 `237fad2f` VALID 160.0 s, GUARD-AFTER unchanged, SoC 49.1→53.5 °C throttled=0x0, 45 era-skipped candidates (vk_sha256 pin). Log: `t12_cycle102_battery_attempt3.log`.

## Settle (Cuneiform devnet, program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- Gated on attempt3 complete-line `BATTERY_EXIT=0` + "PRIMARY VALID + CONTROLS VALID" + GUARD-AFTER unchanged (fail-closed `settle_cycle102.sh`). Executed 18:22Z: **REGISTER TX `2KQtRfz3…` slot 511075799 finalized, err null**, record PDA `5WGAXCnH…`, merkleRoot == captured proof SHA, treasury +100000 lamports, 6/6 tests.
- Chain readback (settle-signature gate): signature byte-identical via `getSignaturesForAddress` on the PDA; program logs `Instruction: RegisterCoordinates` + `Language-U coordinates registered successfully!` See `settle_summary.md`.

## Honest ledger
- attempt1 abort was NOT a silicon or capture defect — a repo-hygiene regression caught by the guard at zero pairing cost.
- **Systemic finding (fleet law extension):** until 612292c merges to main, EVERY fresh per-cycle branch cut from origin/main silently drops the exit-contract port and re-arms the bare-`main()` bug; the launcher sha-guard is the only thing standing between that and unfalsifiable `BATTERY_EXIT=0` lines. Fix on record: this PR carries the restored `tools/` bytes (canonical 9c85e6a6 + non-canonical 8a9bf41f + unit test 2caf14fb), byte-identical to PR#66/PR#58 heads — merge either PR and the class dies.
- Declare-to-fire delta machine-computed from raw bus timestamps in the settle script (hand-typed-constant law).
- No window was double-declared; the standby service deferred to the drill listener per design and re-certified + re-armed cleanly at 16:12:15Z after close.

## Reproduce (fresh checkout of this PR head)
1. `python3 tools/test_t12_battery_template.py` → PASS (exit contract + canonical contracts).
2. `sha256sum evidence/groth16_ota_20261014T1411Z_cycle102/rx_payload_128b.bin` → `fa92aa35…a7d06c`.
3. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261014T1411Z_cycle102/session_slice_cycle102.log --expect-sha fa92aa353492e907d86def4e6283f4d6d1dd6af2130322b554afad3e50a7d06c --min-size 100` → rc=0, `sha256_match: true`.
4. T12 battery: `bash` launcher pattern with `--cycle 102 --evidence-dir evidence/groth16_ota_20261014T1411Z_cycle102 --guard-log <newest standby log>`; requires live buses + on-disk control payloads (key-43 c-101, key-41 c-99, key-40 c-98).
5. Settle readback: `getSignaturesForAddress <record PDA>` on devnet; verify merkleRoot == payload SHA.
