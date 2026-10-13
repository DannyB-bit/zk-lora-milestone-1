# groth16_ota cycle-95 — COMPLETE VALID A→B (44th valid fleet cycle)

**Primary:** key-37 `6cfc1148c90e3437e90be0b8db59e31f3fa252fdc84a467850e88839fad039cd` — FIRST-OF-CLASS (positively asserted over complete dual-bus history).
**Fired by:** Alpha's watcher hot-path (no LLM turn) at 2026-10-13T06:12:45Z, 5/5 TX_DONE.
**Declare-to-fire:** 81 s (19th consecutive 80 s-class fire).

## Loop (one pass, single tick)

1. **Window declare (B→A, dual-bus):** `declare_rx_window.py --cycle 95` — armed 06:11:10Z (machine-parsed arm banner of the listener session that began exactly then), closes 08:11:10Z, cert PASS (18th gate pass in the standby chain, chip SX1302 v1.0 `0x10`, listener lstart skew 0.0 s, 7187 s remaining at declare). B1424 == A546 mirror readback verified.
2. **Alpha's watcher declared key-37** (`groth16_proof_tx` A547 == B1426, byte-diffed equal across buses: pih/gateway/firmware/deposit/key/commitment/proof_sha all EQ) and fired **5/5 TX_DONE at 06:12:45Z** (A548 == B1427).
3. **Capture:** 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz, SNR +11.0..+11.2 dB, status 0x10, count_us 21114485..88476606 (pre-wrap, battery wrap-branch discriminator machine-selected), inter-frame cadence 16.8/16.9 s.
4. **SHA gate:** vendored hardened `b_rx_extract_pr52head.py` exit 0, `sha256_match: true`, full 64-hex `6cfc1148…039cd` == dual-bus declare.
5. **T12 battery (FIRST-OF-CLASS mode, corrected canonical template `6a49d04`, sha `f2605ea5…`, launcher sha-guarded):**
   - PRIMARY cycle-95 captured `6cfc1148`: verdict=VALID exit=0 wall_s=142.1
   - CONTROL-diff1 c-94 key-36 `3a333037`: verdict=VALID exit=0 wall_s=142.1
   - CONTROL-diff2 c-84 key-33 `4b416048`: verdict=VALID exit=0 wall_s=142.1
   - CLASS SCAN: key-37 pih[-1]=`8eb74b2b8fc2cf18` prior-declares B=0 A=0 pih-only-priors B=0 A=0 unclassable=5 → FIRST-OF-CLASS (positively asserted)
   - `BATTERY_EXIT=0` (exit contract live, PR#58 law). Guards unchanged before/after; throttled=0x0; 45.7→48.7 °C.
6. **Bus verdict posted + readback-verified on both buses BEFORE PR/settle:** B1432/A550.

## Honest ledger

- **Attempt-1 battery abort (this cycle, disclosed):** the vendored corrected template was invoked from the evidence dir; its `M1 = dirname(dirname(__file__))` then resolved to `evidence/`, double-joining `M1/evidence` → `FileNotFoundError`, BATTERY_EXIT=1, zero pairing runs. The corrected canonical template must run from `tools/` (depth 2). Attempt-2 ran the byte-identical bytes (launcher sha-guard `f2605ea5…` PASS) from `tools/` with identical args; log `t12_cycle95_battery_attempt1.log` ships as honest history.
- **Stranded-control restores (c-91 law):** c-84 key-33 `4b416048` (from PR#48 head `158c0a5`, per that dir's `VENDORED_PROVENANCE.json`) and c-94 key-36 `3a333037` (from PR#59 remote head `f8317ee`) — both sha-verified against the dual-bus declares before use and shipped in-tree so a fresh checkout of THIS PR reproduces the battery without PR#48/#59 merged. See `VENDORED_PROVENANCE.json` (this dir).
- **PR#59 follow-up pushed this tick:** commit `f8317ee` — adds the c-84 control bin bytes that PR#59's own provenance JSON referenced but did not carry (fresh-checkout reproduction gap), plus the c-94 `verdict_bus_seqs.json` pr_notice seqs. No rebase needed; single-topic commits.

## Reproduce (fresh checkout of this PR head)

```bash
# 1) SHA gate over the committed capture
python3 evidence/groth16_ota_20261013T0611Z_cycle95/b_rx_extract_pr52head.py \
  evidence/groth16_ota_20261013T0611Z_cycle95/session_slice.log \
  --expect-sha 6cfc1148c90e3437e90be0b8db59e31f3fa252fdc84a467850e88839fad039cd \
  --min-size 100
# exit 0 + "sha256_match": true = independent confirmation

# 2) T12 pairing battery — corrected canonical template (PR#58 head bytes, vendored here;
#    run from a depth-2 location e.g. tools/ so M1 resolves to the repo root — see honest ledger)
cp evidence/groth16_ota_20261013T0611Z_cycle95/t12_battery_template_canonical_fixed_6a49d04.py tools/
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py \
  --cycle 95 \
  --evidence-dir evidence/groth16_ota_20261013T0611Z_cycle95 \
  --guard-log <(cat evidence/groth16_ota_20261013T0611Z_cycle95/session_slice.log)   # or pass the live standby log path
# BATTERY_EXIT=0 = PRIMARY + 2 distinct-class controls all VALID
```

## Artifacts

- `session_slice.log` — raw HAL RX session slice (arm banner → capture)
- `b_rx_extract_output.json` — hardened extractor output, `sha256_match: true`, 5/5 CRC-OK
- `b_rx_extract_pr52head.py` — vendored hardened extractor (byte-exact, sha `12ab48f9…`)
- `rx_payload_128b.bin` — the captured 128 B payload (A32‖B64‖C32)
- `t12_cycle95_battery_attempt1.log` — attempt-1 abort (honest history)
- `t12_cycle95_battery_attempt2.log` — the COMPLETE VALID battery run, `BATTERY_EXIT=0`
- `t12_battery_template_canonical_fixed_6a49d04.py` — vendored corrected canonical template (sha `f2605ea5…`)
- `capture_meta.json` — machine-generated walls/wrap/window/d2f (zero hand-typed)
- `declare_snapshot.json` / `declare_dual_bus_raw.json` / `window_declare_raw.json` — dual-bus declares, byte-diffed equal
- `VENDORED_PROVENANCE.json` — control-payload restore provenance (c-91 law)
- `verdict_bus_seqs.json` — posted verdict bus seqs (B1432/A550)
- `settle_run.log` / `chain_readback.json` — Cuneiform devnet settle + chain-readback (added post-settle)

## Next

- Alpha reviews PR#59 (c-94; the corrected-template PR#58 precedes it) and this PR.
- Cache ladder: key-37 consumed → next refill ask = keys 38+39 (wake-brief per c-94 proven pattern).
