# groth16_ota cycle-100 — FIRST FULL T12 BATTERY COMPLETE VALID → Cuneiform Devnet settle

- **Cycle**: 100 — groth16_ota drill, A→B, 2026-10-14
- **Primary**: key-42, deposit 100011, identity era (VK `78352ffa2d0bfe92…`, PK `aea2ed17290f3294…`),
  `proof_sha256 = 237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d`
- **Verdict**: **BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID — BATTERY_EXIT=0** (attempt5,
  `t12_cycle100_battery_attempt5.log`) — the fleet's **first full-battery COMPLETE VALID**,
  and the **first settle ever gated on a true full-battery BATTERY_EXIT=0**.
- **Window**: declared B-bus seq 1576 / A-bus mirror seq 625 (armed 08:10:53Z, closes 10:10:53Z,
  certified: gate pass #10, chip v1.0, zero arm skew). Alpha's watcher auto-fired **80 s** after
  declare (A626 declare → A627 `groth16_tx_fired` 5/5 TX_DONE @ 08:14:56Z).
- **Capture**: 5/5 CRC-OK (0x10), 128 B each, 903.9 MHz exact (radio A 904.3, IF −400 kHz), SF9/125 kHz,
  SNR +10.8..+11.8 dB, inter-frame 16.8 s uniform, count_us 169815298..236853714, pre-wrap (+0 s),
  frames 08:13:42Z..08:14:49Z — causal with the fired stamp (span 6 s). SHA gate: captured digest ==
  declared digest, 64/64.
- **Class scan**: key-42 **FIRST-OF-CLASS positively asserted** (zero prior declares of the statement
  class over complete dual-bus history; 5 unclassable-declares counted).
- **Controls** (machine-picked, distinct statement classes, era-matched to primary VK):
  - `CONTROL-diff1` c-99 key-41 `e5e6c439…` → **VALID** (159.6 s)
  - `CONTROL-diff2` c-98 key-40 `62f2019e…` → **VALID** (160.3 s)
- **Guards**: binary `4c8e1f8a` + PK + VK unchanged before/after; silicon 46.7→52.1 °C, `throttled=0x0`.
- **Settle** (Cuneiform Devnet): REGISTER_TX
  `2L8b5uUAQiHHxzBrXxcWyjriT23U9RAajRWzWj992zinf3FGmnCSFCf9JxKRdySgzCfGbXYpXgRkcpE52uc2vUBWc`,
  record PDA `CkCFMYBRdnAMJQE96PqTVM7gbiPVsnoPcqUXZJfDUPQ2`, merkle root == captured proof SHA256,
  independent RPC readback: TX slot 510951640 err=null; PDA live, owner = Cuneiform program
  `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, 100,000-lamport protocol fee, 6/6 tests.

## Honest ledger — what broke, what was fixed, in order

1. **attempt1 (08:27Z, canonical template as shipped)**: PRIMARY VALID but control-diff2 c-97 key-39
   (canon-era VK 7bd5683f) INVALID under identity keys → QUARANTINED, correct per battery law —
   yet the run **exited 0**. Root cause: the canonical's `__main__` called `main()` bare, discarding
   `battery_rc`. The exit contract (PR#55/56, my own PR#58 flagship) was dead code **in the file every
   launcher runs**.
2. **Root cause of the era-hole**: commit `33eefd9` (PR#58 head) patched
   `tools/t12_battery_template.py` — the non-canonical — while every launcher runs
   `tools/t12_battery_template_canonical_fixed_6a49d04.py`. All three fixes (exit contract, era-pin,
   window_seq+SHA phantom-join) were absent from the running file. `git diff 33eefd9 -- <canonical>`
   was empty — the fixes never landed where they execute.
3. **Fix (this PR)**: all three fixes ported into the canonical + unit test
   (`tools/test_t12_battery_template.py`) extended to pin the canonical's entry contract
   (`sys.exit(main())`), inline 3/4 verdict mapping, era-pin, and phantom-join. Canonical sha is now
   `9c85e6a6a9901147…` (launcher guard updated).
4. **attempt2/attempt3 (08:32Z–08:46Z)**: a concurrent hourly twin-tick session (same node, same
   mission) ran the c-100 pipeline in parallel on the stale template; its runs produced the same
   quarantine class, one sha-guard abort, and a wrong bus ask (B1584/A630: "re-mirror c-98 declare to
   B-bus — never mirrored"). That ask was **retracted by countermand B1587/A631** after a live
   dual-bus simulation of the fixed candidate join proved c-98 USABLE (B1538 full-SHA byte-exact,
   vk-pinned, A615 1:1 via window_seq+SHA, A612 dry-run phantom excluded). No duplicate mirror was
   posted; the 1:1 dual-bus gate stays intact for all future scans.
5. **attempt4**: killed at the 420 s agent-terminal cap mid-primary-verify (template emits output
   only at completion — empty log by design, no verdict). Honest history, kept as a 2-line note.
6. **attempt5 (the green run)**: fixed canonical, template sha guard `9c85e6a6…`,
   scan line reads `2 usable / 0 skipped / 45 skipped-era-mismatch [vk_sha256 pin, c-96 law]` —
   both identity-era controls picked (key-41, key-40), all VALID, **BATTERY_EXIT=0**.

## Files

- `session_slice_cycle100.log` — armed-banner session segment (this session's slice)
- `session_slice.log` — twin-tick session's slice (identical source, kept for the record)
- `b_rx_extract_output.json` — fail-closed extractor output (5/5, sha256_match true)
- `window_declare_raw.json` / `declare_dual_bus_raw.json` / `fired_dual_bus_raw.json` — raw bus events
- `capture_meta.json` — overwritten by the twin-tick session (extract-shaped); raw sources above are
  ground truth; settle gates read extract + battery log + declare raws only
- `t12_cycle100_battery_attempt{1,2,3,4,5}.log` + `t12_cycle100_battery.log` — full honest history
- `settle_summary.md` — settle log + independent RPC readback

Artifacts at commit time: no radio listener currently holds the bus (continuous standby guard
re-arms on gate PASS; window closed 10:10:53Z).
