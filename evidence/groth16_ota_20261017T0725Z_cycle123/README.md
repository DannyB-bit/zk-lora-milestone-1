# groth16_ota cycle-123 A->B — key-65 FIRST-OF-CLASS COMPLETE VALID + settled Devnet

**Cycle:** 123 · **Key:** 65 (identity era, VK 78352ffa) · **Proof SHA256:** `a5b1554d234d45c3377ce5b2f66294c208ae3da2740d33b0e69819028b42d124`

## Radio transfer (903.9 MHz, SF9/125 kHz, radio A 904.3 IF -400 kHz)
- Window B1994/A809 armed 2026-10-17T07:25:17Z -> closes 2026-10-17T09:25:17Z (declare_rx_window.py v1.0, cert PASS, 20th gate pass, skew 1.0s, 3301s headroom at declare)
- Alpha watcher declared key-65 (A seq 810 / B mirror 1995) and fired **5/5 TX_DONE @ 2026-10-17T08:31:37Z** — declare-to-fire ~80s, ninth consecutive
- Capture: **5/5 CRC-OK 128B frames**, all sha256 == `a5b1554d…b42d124`, SNR +10.5..+11.2 dB, count_us 3907136071..3974201286 (pre-wrap, machine-selected branch), inter-frame ~16.8s uniform, session slice from ARM banner line 3049 (live-session EOF bound, c-117 law, seventh use)
- Extract: b_rx_extract.py rc=0, sha256_match TRUE; dual-bus declare byte-diff B==A TRUE; fired byte-diff B==A TRUE

## T12 battery (attempt-6, BATTERY_EXIT=0)
- PRIMARY key-65 `a5b1554d` **VALID** 160.0s
- CONTROL-diff1 key-64 (c-122, restored byte-exact from PR#88 head) VALID 159.7s
- CONTROL-diff2 key-63 (c-121) VALID 160.1s
- CLASS SCAN: statement-class key-65 pih[-1]=b93f581f533ca207, prior-declares B=0 A=0 -> **FIRST-OF-CLASS (positively asserted, c-84 law)**
- GUARD-AFTER unchanged (binary 4c8e1f8a / PK aea2ed17 / VK 78352ffa); throttled=0x0; temp 41.3->45.2C

## Devnet settlement (Cuneiform, Program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- REGISTER TX `p2URWiWs93cbHsfrn6qXUwm2Nk2nUJtA5chCvQ1mK63NzPzE18BaQz4x2HrpzTUkuihXRTQcVMgMw1kia3Fpxcn`
- Record PDA `DS7hZazJ7jWGPdsd9JU1Ujzi3mYVLnYwgcKAZCnHtgwv` — chain_readback_v2 all_byte_checks_pass TRUE (session_id/coords/merkle-root byte-exact, 103B account, owner == program)
- Settle TX rank-1 in PDA sig-history, err=null, machine-fetched via getSignaturesForAddress (c-30 gate)
- merkle root = proof payload SHA256; coords = payload bytes 0..5 = [221,109,6,23,238,181]; 100k-lamport CPI fee; 6/6 settle tests passed

## Honest ledger (all attempts on the record)
1. Battery attempts 1-2 (ABORT: evidence dir not found) — operator-side hand-typed-constant bug: my evidence-dir rename typo (`2026017` vs `20261017` digit transposition) vs the sed-mirrored launcher's correct path; fixed by machine-deriving the dir name from the ARM banner. Fail-closed, zero pairing cost.
2. Battery attempts 3-5 (ABORT: expected 5 declared-digest frames, found 0) — NEW c-121-law instance: the sed-mirrored launcher carried `--cycle 122` (the space-separated arg survived the `cycle122->cycle123` token replace), so the template machine-located the c-122 window (B1980) and key-64 SHA f7f98185; 0 of the 5 key-65 frames matched. Deterministic mis-target, fail-closed, zero pairing cost. Same class found+fixed in settle_cycle123.sh (T12_CYCLE122 label grep + attempt1 log path) BEFORE any settle ran.
3. One instrumented probe run (scratch copy; sha-guarded canonical untouched) killed at harness timeouts (120s/240s) mid-primary-pairing — honest kill, no verdict claimed. Probe DBG output proved all inputs correct (declared=a5b1554d, 5 frames in segment), isolating the bug to the launcher `--cycle` arg.
4. c-91 control restore: hand-typed pathspec reads of PR#88 head failed repeatedly; the machine-derived blob path (ls-tree | grep) cat-file'd cleanly. Extends the hand-typed-constant law to git paths.
5. Node anomaly (disclosed): intermittent ENOENT on the evidence dir across the settle window (byte-verified paths failing open() then succeeding; writes failing then landing on retry); no concurrent tick in executions.db, no fs I/O errors in dmesg, disk 96% full (1.2G free on /). All gates re-verified after each retry; on-chain state machine-read twice (chain_readback_v2 PASS + sig-history rank-1).

## Controls (this PR carries the restored bytes)
- key-64 (c-122): rx_payload_128b.bin restored byte-exact from PR#88 head 77a554f via machine-derived blob OID path, sha256 f7f98185… == dual-bus declares A seq 803 / B seq 1982 — control_restore_provenance.json (rides in this PR per c-91 law)
- key-63 (c-121) + key-62 (c-120): control bins on their open PR branches

## Reproduce (fresh checkout of this PR head)
1. `bash evidence/groth16_ota_20261017T0725Z_cycle123/launch_t12_cycle123.sh` (sha-guarded launcher, `--cycle 123`; requires live buses + guard log)
2. `bash evidence/groth16_ota_20261017T0725Z_cycle123/settle_cycle123.sh` (gated on complete-line BATTERY_EXIT=0 + PRIMARY VALID + CONTROLS VALID)

Event trail (dual-bus): window B1994/A809 · declare B1995/A810 · fired B1997/A811 · rx_capture_confirmed B2000/A812 · rx_verdict B2006/A813 — all content-verified on readback.
