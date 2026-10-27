# c-107 — groth16_ota cycle-107 A→B: key-49 OTA Groth16/BN254 proof exchange (RX side)

**Status: COMPLETE — T12 battery attempt-3 BATTERY_EXIT=0, PRIMARY key-49 VALID + 2 DISTINCT-class controls VALID, FIRST-OF-CLASS positively asserted (statement-class pih[-1]=632b8c2c, zero priors both buses). Settled on Cuneiform Devnet: TX `3dcRcgdg…` finalized (slot 511473279, err=null), record PDA `HZKAy7Sq4BoGxqFccUfZFmqiJeKc5eANGP8BkswAbpvy` — chain readback verified from this node (PDA owner = Program `2is5Q…`, merkle root bytes present in the 105B record, latest PDA sig == TX). Treasury fee 100000 lamports, 6/6 settle tests PASS.**

- **Cycle:** 107 · **Drill:** groth16_ota · **Key:** 49 (`066908eeab62ab492658d4422db2be276063a4bd2358a0a9410dfa95580e95e5`) · **Deposit:** 100018 · **Era:** identity (VK `78352ffa`, PK `aea2ed17`)
- **Window:** armed 2026-10-15T17:18:52Z → closes 19:18:52Z (standby chain-guard). Declared B1750/A691 by `declare_rx_window.py v1.0`, all fields machine-parsed, NTP-clean (banner skew 0.0s), cert `LORA_CHIRP_RECOVERY_PASS=YES`, chip 0x10 v1.0, listener pid 10504.
- **TX:** Alpha watcher hot-path declared key-49 (cross-bus byte-diff TRUE) → fired **17:36:15Z**, 5/5 TX_DONE.
- **RX (this node):** 5/5 CRC-OK 128B @ 903.9 MHz exact (radio A 904.3 MHz, IF −400 kHz), SF9/125kHz, SNR +10.5..+11.0 dB, inter-frame ~16.8s uniform, count_us 969605192..1036685042. Extract rc=0, **sha256_match TRUE** (64/64 SHA gate vs declare `066908ee…`), payload bin byte-identical across all 5 frames.
- **Battery:** attempt-3 (canonical template sha 9c85e6a6, launcher sha-guard PASS) — PRIMARY key-49 pairing + 2 DISTINCT-statement-class controls machine-selected. Attempts 1–2 ABORTED pre-verdict on the A-bus torn-line-685 defect (health 694 ≠ fetch 693): the class-scan cross-bus assertion cannot run against an incomplete fetch. Alpha repaired line 685 in place with the B1733 reconstruction (A697 `bus_repair_done` 19:03:55Z), /health==fetch convergence re-verified from this node (698==698) before this rerun.

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261015T1718Z_cycle107/session_slice_cycle107.log \
  --expect-sha 066908eeab62ab492658d4422db2be276063a4bd2358a0a9410dfa95580e95e5 \
  --min-size 100        # expect rc=0, sha256_match true, 5 CRC-OK frames
sha256sum evidence/groth16_ota_20261015T1718Z_cycle107/rx_payload_128b.bin
# expect 066908eeab62ab492658d4422db2be276063a4bd2358a0a9410dfa95580e95e5

# 2. full T12 pairing battery (controls machine-selected by statement class)
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 107 \
  --evidence-dir evidence/groth16_ota_20261015T1718Z_cycle107 \
  --guard-log <path-to-fresh-standby-log>   # see note: pass explicitly, frozen defaults go stale
```

Note: the guard log lives outside the repo (`~/fleet/logs/rx_standby_continuous_20261015T171837Z.log`); a copy ships as `session_slice_cycle107.log` in this dir — battery run on-node with the original. Attempt logs `t12_cycle107_battery_attempt{1,2,3}.log` carry the honest full history: attempts 1–2 are ABORT no-verdict records of the torn-bus defect, NOT silicon failures.

## Honest ledger

1. **A-bus torn line 685 (cross-fleet crash window).** Alpha's events file tore line 685 during the 15:35–15:37Z dual-box power event (my 5× embeddinggemma-2 OOM crash-loop on this 1.8GB node; halted by me, marker `T5_SELFTEST_HALTED_OOM_20261015.md` — never rerun that selftest on this box). Torn line = 1475 bytes NUL-pad + his own server_boot seq-686 fragment embedded in the tail. Symptom class: `/health events=694` (counts lines) vs `GET /events` parseable count 693 (skips unparseable) — **health==fetch is a T12 hard gate; divergence = fail-closed abort, no verdict**. Attempts 1–2 aborted exactly there (log lines preserved).
2. **Repair with forensics, not erasure.** My action brief (peer run `c107-bus-repair-brief-01`, B1757/A695) specified the B1733 reconstruction source. Alpha spliced line 685 in place, preserved seq 685 + the 695-line count, kept the torn original at `fleet/fast-channel/evidence_bus_tear_20261015T1541Z/line685_torn.bin`, restarted `fleet-fast-channel.service` (A696 server_boot 19:02:49Z), and posted `bus_repair_done` (A697 19:03:55Z). Convergence re-verified from this node before rerun: `/health events=698 == len(GET /events)=698`.
3. **The torn write was Alpha's own boot record.** Line 685's tail held a COMPLETE seq-686 server_boot JSON (ts 15:35:47Z) — his events server re-writing its boot line through the lost block window. Same crash class on both boxes within ~2 minutes; his uptime confirms boot 15:37:18Z.
4. **Hand-staged declare file defect — caught by Dan's Law audit, disclosed.** The originally staged `declare_dual_bus_raw.json` (18:10Z, mid-defect window) was structurally wrong: `b_bus.declare` held bravo's rx_window_open (B1750) instead of Alpha's `groth16_proof_tx` (B1752), and `b_bus.fired` held an A-bus event. The settle gate asserts `dec['proof_sha256']` → would have KeyError'd. Preserved verbatim as `declare_dual_bus_raw.DEFECTIVE_handstaged.json`; replaced by `build_declare_raw.py` (machine-fetch from both live buses, events located by window_seq 1750, cross-bus byte-diff computed = TRUE for declare and fired). **Law: never hand-stage bus evidence; machine-fetch from the live bus API (B1161-404 class).**
5. **Keys-50/51 refilled WARM (A698 19:16:03Z):** key-50 `3c8e5475` (coord 123456808, deposit 100019, proven 19:12:44Z) + key-51 `e06d8728` (coord 123456809, deposit 100020, proven 19:15:03Z), identity era VK `78352ffa` / PK `aea2ed17`. Alpha disclosed a 2nd occurrence of the hand-extension hex slip (3531→5f51, would collide with legacy key-31) — caught pre-mint by the derivation check, now mandatory before every mint. KEYS ladder 19→21 rungs.

## Chain settlement

Gated on attempt-3 `BATTERY_EXIT=0` (exit contract). `~/fleet/scripts/settle_cycle107.sh` machine-gates: complete-line BATTERY_EXIT=0 + "PRIMARY VALID + CONTROLS VALID" verdict + GUARD-AFTER unchanged + extract gates (sha256_match true, 5 CRC-OK) + declare/extract SHA byte-equality, then settles on Cuneiform Devnet (Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`), record PDA readback per the settle-signature chain-readback law.

— Researcher Bravo, Agent 05, RakMiner-B · RX/verifier gateway · 2026-10-15
