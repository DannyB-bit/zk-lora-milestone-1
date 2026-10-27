# groth16_ota cycle-105 — A→B over-the-air Groth16/BN254 proof — key-47 FIRST-OF-CLASS

**Cycle**: 105 · **Drill**: `groth16_ota` · **RX node**: RakMiner-B (Researcher Bravo, Agent 05)
**Primary**: key-47 `32451e4f206df7765b38c6804522387173e825511418b90af0b6b66ac12247f9` (deposit 100016, identity era VK `78352ffa…`)
**Class assertion**: made by the battery's machine class-scan only (c-92 law — never pre-labeled).

## Window (declare via `declare_rx_window.py` v1.0, composer law c-78)
- Armed **2026-10-15T02:13:56Z** → closes **2026-10-15T04:13:56Z** (7200 s), B-bus seq 1673 / A-bus mirror seq 665. Gate pass #19 in standby log; chip version 0x10 (v1.0) per HAL banner; `LORA_CHIRP_RECOVERY_PASS=YES` at 02:13:56Z; listener at "Waiting for packets", skew 0.0 s.
- Declared 02:32:25Z with 6092 s remaining. Cache warm per Alpha's refill notice **B1653 == A656 byte-equal** (refill-before-declare law c-94) — key-46 `c661f2e1` (consumed by c-104) / key-47 `32451e4f` fired this cycle.
- Honest ledger: window #18 (00:13:36Z–02:13:36Z) rolled **unfired** — the previous tick's pipeline (c-104 settle + PR#70) ran past its close with no `rx_window_open` posted into it; its segment recorded 0 CRC-OK frames. No wasted airtime (correct watcher hold), but no declare either — a scheduling miss owned on the record.

## Fire (Alpha's watcher hot path — no LLM turn)
- Alpha declared `groth16_proof_tx` B1675/A666 at 02:32:26Z — **1 s after window-open** (watcher hot path at 2 s poll). All fields byte-equal across both buses (dual-bus byte-diff PASS).
- Fired **02:33:46Z** — ~80 s declare-to-fire, 5/5 TX_DONE, exit 0.

## Capture (5/5 CRC-OK, 128 B)
- 5 × 128 B frames, `status 0x10` CRC-OK, 903.9 MHz exact (radio 904.3 MHz, IF −400 kHz), SF9/125 kHz.
- SNR +10.8..+11.8 dB; inter-frame 16.7–16.8 s uniform; count_us 1117145232..1184218659 (**pre-wrap +0 s branch — machine-selected by the battery selector**, per c-101 law).
- Extract: `b_rx_extract.py` rc=0, `sha256_match: true`, full 64-hex `32451e4f…2247f9` == declare == fired.

## T12 full battery (canonical template 6a49d04, sha `9c85e6a6`, exit contract)
- attempt1: **BATTERY_EXIT=0 first try** — PRIMARY key-47 `32451e4f` **VALID 160.0 s**, class-scan **FIRST-OF-CLASS positively asserted** (prior declares B=0 A=0, pih-only B=0 A=0, unclassable 5), CONTROL-diff1 key-46 `c661f2e1` VALID 160.1 s + CONTROL-diff2 key-45 `1470c41c` VALID 159.6 s, GUARD-AFTER unchanged, SoC 47.2→51.1 °C throttled=0x0, 45 era-skipped candidates (vk_sha256 pin). Log: `t12_cycle105_battery_attempt1.log`.
- **Sixth consecutive first-of-class battery** (c-100 key-42 → c-101 key-43 → c-102 key-44 → c-103 key-45 → c-104 key-46 → c-105 key-47 — all six positively asserted in committed battery logs, machine-counted this turn from worktree + PR-head refs). Every key-N since the ladder extension has been the first of its class in fleet history.
- Unit test before silicon: `tools/test_t12_battery_template.py` PASS (exit-contract 7-fixture + canonical contracts).

## Settle (Cuneiform devnet, program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- Gated on attempt1 complete-line `BATTERY_EXIT=0` + "PRIMARY VALID + CONTROLS VALID" + GUARD-AFTER unchanged (fail-closed `settle_cycle105.sh`). Executed 03:08:00Z: **REGISTER TX `333iH7nC…bmGPkxj` slot 511208034 finalized, err null**, record PDA `6zRarqef…wuqKWn`, merkleRoot == captured proof SHA, treasury +100000 lamports, 6/6 tests. See `settle_summary.json`.
- Chain readback (settle-signature gate): signature byte-identical via `getSignaturesForAddress` on the PDA; `confirmationStatus: finalized`; `chain_readback_v2.py` raw-byte layout verify PASS (session_id_ascii `32451e4f206df776`, coords `[203,196,249,94,232,120]`, merkle_root raw 32 B — all byte-match at Anchor offsets). Recorded in `settle_summary.json` + `chain_readback.json`.

## Honest ledger
- No aborts this cycle: template sha-guard PASS on first attempt, controls restored before battery, extraction clean first pass, battery exit-0 first try, settle gates clean.
- Fresh branch cut from origin/main (37d5310) strands the c-100..c-103 control dirs and the canonical tools — restored byte-exact from PR#66/#67/#68/#69 head refs (see `control_restore_provenance.json`), the same bytes the c-104/c-105 batteries verified VALID in-session. **The stranded-by-main regression class persists until PR#66/#67/#68/#69 merge.**
- Declare-to-fire delta machine-computed from raw bus timestamps in the settle script (hand-typed-constant law).
- Battery label `T12_CYCLE105_BATTERY_RUN_UTC` derived from the `--cycle` arg that machine-located the window (c-38 law).
- Cache state after this cycle: **EMPTY** — key-46 and key-47 both burned. Refill ask for keys 48/49 rides the verdict + settle events (c-94 law). Next declare waits on Alpha's dual-bus `cache_refill_notice`.
- Window #19 remains armed (closes 04:13:56Z); the standby service re-certifies + re-arms on close per the continuous-RX posture.

## Reproduce (fresh checkout of this PR head)
1. `python3 tools/test_t12_battery_template.py` → PASS (exit contract + canonical contracts).
2. `sha256sum evidence/groth16_ota_20261015T0213Z_cycle105/rx_payload_128b.bin` → `32451e4f…2247f9`.
3. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261015T0213Z_cycle105/session_slice_cycle105.log --expect-sha 32451e4f206df7765b38c6804522387173e825511418b90af0b6b66ac12247f9 --min-size 100` → rc=0, `sha256_match: true`.
4. T12 battery: `tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 105 --evidence-dir evidence/groth16_ota_20261015T0213Z_cycle105 --guard-log <newest standby log>`; requires live buses + on-disk control payloads (key-46 c-104, key-45 c-103).
5. Settle readback: `getSignaturesForAddress 6zRarqefBUoKvvHRGW46g22xVuNX4W6QG3muHWwuqKWn` on devnet → signature `333iH7nC…bmGPkxj`, err null; verify on-chain merkleRoot raw 32 B == payload SHA.
