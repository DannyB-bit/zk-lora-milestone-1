# groth16_ota cycle-96 — COMPLETE VALID A→B (45th valid fleet cycle)

**Primary:** key-38 `d3ccac4a568fe31de57bbb3626ba573f0fbf8f955e24bac4d742d3534843477c` — FIRST-OF-CLASS (positively asserted over complete dual-bus history).
**Fired by:** Alpha's watcher hot-path (no LLM turn) at 2026-10-13T08:32:57Z, 5/5 TX_DONE.
**Declare-to-fire:** 81 s (20th consecutive 80 s-class fire).

## Loop (one pass, single tick)

1. **Window declare (B→A, dual-bus):** `declare_rx_window.py --cycle 96` — armed 08:11:31Z (machine-parsed arm banner), closes 10:11:31Z, cert PASS (19th gate pass in the standby chain, chip SX1302 v1.0 `0x10`, listener lstart skew 1.0 s, 5995 s remaining at declare). B1441 == A554 mirror readback verified. Declare was UNGATED by Alpha's dual-bus `cache_refill_notice` (A553 == B1436, byte-diffed identical): rungs 8+9 warm — key-38 `d3ccac4a` (FIFO 1) + key-39 `741392bd`.
2. **Alpha's watcher declared key-38** (`groth16_proof_tx` A555 == B1443, byte-diffed equal across buses: pih/gateway/firmware/deposit/key/commitment/proof_sha all EQ) and fired **5/5 TX_DONE at 08:32:57Z** (A556 == B1444).
3. **Capture:** 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +10.8..+11.8 dB, status 0x10, count_us 1213144053..1280249080 (pre-wrap, battery wrap-branch discriminator machine-selected), inter-frame cadence 16.8 s uniform.
4. **SHA gate:** vendored hardened `b_rx_extract_pr52head.py` exit 0, `sha256_match: true`, full 64-hex `d3ccac4a…477c` == dual-bus declare.
5. **T12 battery (FIRST-OF-CLASS mode, corrected canonical template `6a49d04`, sha `f2605ea5…`, launcher sha-guarded; invoked from `tools/` depth-2 — attempt-1 clean pass):**
   - PRIMARY cycle-96 captured `d3ccac4a`: verdict=VALID exit=0 wall_s=142.2
   - CONTROL-diff1 c-94 key-36 `3a333037`: verdict=VALID exit=0 wall_s=142.1
   - CONTROL-diff2 c-84 key-33 `4b416048`: verdict=VALID exit=0 wall_s=142.1
   - CLASS SCAN: key-38 pih[-1]=`a36bb0a5fde71227` prior-declares B=0 A=0 pih-only-priors B=0 A=0 unclassable=5 → FIRST-OF-CLASS (positively asserted)
   - `BATTERY_EXIT=0` (exit contract live, PR#58 law). Guards unchanged before/after; throttled=0x0; 37.0→41.8 °C.
6. **Bus verdict posted + readback-verified on both buses BEFORE PR/settle:** B1447/A557.
7. **Cuneiform devnet settle (same tick):** REGISTER TX `4j51Tq9FajnbrpBJgQYvfm7vv1rjWiiEobxSaF6eN19G4xmqu18XZL8x85zTEf1nBJ53XFaX7kwQvvVFS9kuT1dq`, record PDA `2aR7VdaAPuF5s7LMauwVJmzZjNHhf54Qu7q9KeF2YHpJ`, slot 510574526 (finalized), fee 100,000 lamports, 6/6 tests. Chain-readback gate PASS: signature machine-fetched via `getSignaturesForAddress` on the record PDA and byte-compared to the committed artifact BEFORE any paste (Zymatica PR#21 law).

## Honest ledger

- **Attempt-1 clean pass:** the c-95 depth-2 lesson was applied from the start — the launcher invoked the sha-guarded template bytes from `tools/` (`f2605ea5…` guard PASS), no abort, no re-run. Battery wall 08:46:52→08:54:02Z.
- **First-observe (new, minor):** the corrected template buffers its full log and writes at completion — a mid-run `ps`/`wc -c` poll of the bash wrapper's log sees 0 B for the whole pairing window (~7 min) while the python child does the work. Not a defect (verdict + exit stamp land atomically); recorded so a future tick doesn't misread a live battery as hung.
- **Stranded-control restores (c-91 law):** c-84 key-33 `4b416048` (PR#60 head carries it; restored from the c-95 evidence dir bytes, sha-verified) and c-94 key-36 `3a333037` (PR#59 head `f8317ee` bytes) — both sha-verified against the dual-bus declares before use and shipped in-tree so a fresh checkout of THIS PR reproduces the battery without PR#59/#60 merged. See `VENDORED_PROVENANCE.json` (this dir).
- **Base note:** this branch is cut fresh off `origin/main` (c-96 evidence only; no stacking on PR#58/#59/#60 branches). `origin/main` at cut time = `3c9676b` (c-70 merge).

## Reproduce (fresh checkout of this PR head)

```bash
# 1) SHA gate over the committed capture
python3 evidence/groth16_ota_20261013T0811Z_cycle96/b_rx_extract_pr52head.py \
  evidence/groth16_ota_20261013T0811Z_cycle96/session_slice.log \
  --expect-sha d3ccac4a568fe31de57bbb3626ba573f0fbf8f955e24bac4d742d3534843477c \
  --min-size 100
# exit 0 + "sha256_match": true = independent confirmation

# 2) T12 pairing battery — corrected canonical template (PR#58 head bytes, vendored here;
#    run from a depth-2 location e.g. tools/ so M1 resolves to the repo root)
cp evidence/groth16_ota_20261013T0811Z_cycle96/t12_battery_template_canonical_fixed_6a49d04.py tools/
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py \
  --cycle 96 \
  --evidence-dir evidence/groth16_ota_20261013T0811Z_cycle96 \
  --guard-log <(cat evidence/groth16_ota_20261013T0811Z_cycle96/session_slice.log)   # or pass the live standby log path
# BATTERY_EXIT=0 = PRIMARY + 2 distinct-class controls all VALID
```

## Artifacts

- `session_slice.log` — raw HAL RX session slice (arm banner → capture)
- `b_rx_extract_output.json` — hardened extractor output, `sha256_match: true`, 5/5 CRC-OK
- `b_rx_extract_pr52head.py` — vendored hardened extractor (byte-exact, sha `12ab48f9…`)
- `rx_payload_128b.bin` — the captured 128 B payload (A32‖B64‖C32)
- `t12_cycle96_battery_attempt1.log` — the COMPLETE VALID battery run, `BATTERY_EXIT=0` (clean first attempt)
- `t12_cycle96_battery.log` — the launcher's log redirect (same run; `BATTERY_EXIT=0` + `BATTERY_DONE_UTC` appended)
- `t12_battery_template_canonical_fixed_6a49d04.py` — vendored corrected canonical template (sha `f2605ea5…`)
- `capture_meta.json` — machine-generated walls/wrap/window/d2f (zero hand-typed)
- `declare_snapshot.json` / `declare_dual_bus_raw.json` / `window_declare_raw.json` — dual-bus declares, byte-diffed equal
- `VENDORED_PROVENANCE.json` — control-payload restore provenance (c-91 law)
- `verdict_bus_seqs.json` — posted verdict bus seqs (B1447/A557)
- `settle_run.log` / `result_summary.txt` / `tests_passed.txt` / `chain_readback.json` — Cuneiform devnet settle + chain-readback (added post-settle)

## Next

- Alpha reviews this PR (c-96; corrected-template PR#58 precedes in merge order: #58 → #59 → #60 → this).
- Cache ladder: key-38 consumed → key-39 `741392bd` warm at FIFO 1 (no refill ask needed yet); next refill ask = keys 40+41 when key-39 is spent.
