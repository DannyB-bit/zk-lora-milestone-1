# groth16_ota cycle-164 A->B evidence — COMPLETE VALID A->B (watcher hot-path, Alpha agent lane dark)

**Cycle:** 164 · **Window:** B-bus seq 3569 / A-bus seq 1317 · **Armed:** 2026-11-06T09:30:26Z · **Closes:** 2026-11-06T11:30:26Z
**Primary:** key-121 (FIRST-OF-CLASS), deposit 100090, coord 123456879, identity-era keyset
**Verdict:** radio 5/5 SHA MATCH + pairing PRIMARY VALID + CONTROLS VALID (`BATTERY_EXIT=0` 2026-11-06T10:34:13Z)
**Settle:** Cuneiform devnet REGISTER_TX `2QYCezcedmWhyTw1wQQuZB3uhV49HNvcapA9fxDg7M8BXWjkJVukHqsc2EQf3EZ3ieVsUoDQSpMhkiZPZ5FtYZy9` slot 519271473 (chain-readback PASS)

## What happened (all times UTC, machine-serialized)

1. **09:30:26Z** — standby supervisor certified a fresh arm (LORA_CHIRP_RECOVERY_PASS, chip 0x10 v1.0, STTS751 patch active) and armed a 7200s HOLD_FIRE window.
2. **10:03:17Z** — Bravo's hourly tick declared `rx_window_open` cycle-164 via `declare_rx_window.py --cycle 164` (tz-aware composer, all gates PASS, 4430s remaining). Dual-era note: the cycle-164 NUMBER also exists in the Oct-22 era (key-104 window B2679, never captured on B, unlanded) — the live era is pinned by window seq 3569.
3. **10:03:19Z** — Alpha's **systemd watcher hot-path** (agent lane dark since Oct-31) auto-fired: `groth16_proof_tx` B3571 == A1318 byte-equal (sha `801ef6ac...`, key-121, deposit 100090, VK `78352ffa`, PK `aea2ed17`, 4 public-input hashes).
4. **10:17:59Z** — `groth16_tx_fired` B3572 == A1319 byte-equal: 5/5 TX_DONE, ~80s declare-to-fire.
5. **Capture** — listener (PID 72932, `test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0` ⇒ 903.9 MHz exact, SF9/125 kHz) logged 5/5 CRC-OK 128B frames, count_us 2779866988..2846945395 (pre-wrap +0s branch, battery-selected), inter-frame 16.8/16.7/16.7/16.9 s, SNR +10.5..+11.0 dB. digest(captured) == declared **64/64**. Two ambient 24B CRC-OK frames from a non-fleet transmitter sat in the same session and were excluded by the `--min-size 100` gate.
6. **Battery** — `t12_battery_template.py --cycle 164 --window-seq 3569`: PRIMARY cycle-164 VALID 161.0s; FIRST-OF-CLASS key-121 positively asserted (prior-declares B=0 A=0 over complete dual-bus history); controls key-120 (c-163 dir) VALID 161.2s + key-119 (c-211 dir) VALID 161.4s — 2 DISTINCT statement classes; GUARD-AFTER binary/PK/VK unchanged; SoC 49.6→53.0 °C, throttled=0x0.
7. **Settle** — `settle_groth16_ota.ts`: 5/5 tests PASS (128B, airwave byte-tie, on-chain coords == proof bytes 0..5, on-chain merkle root == proof SHA256, 100000-lamport treasury fee). RECORD_PDA `Erhi85JfSJvEBDyQte2aFwG1iHk1aCdtU6j2TmPE4kpQ`.

## Verification recipe (reproduce from this checkout)

```bash
cd ~/fleet-repos/zk-lora-milestone-1
# 1) capture digest — the airwave half
python3 tools/b_rx_extract.py evidence/groth16_ota_20261106T1017Z_cycle164/c164_session_slice.log \
  --expect-sha 801ef6acfd0a17f99212e6a28ac2f4e4ceb959f35917a984da20d360babcfcd9 --min-size 100
# exit 0 + sha256_match: true (5 CRC-OK 128B frames)
sha256sum evidence/groth16_ota_20261106T1017Z_cycle164/rx_payload_128b.bin   # == 801ef6ac...
# 2) pairing — the silicon half (same-session controls, ~8 min on ARM Cortex-A72)
python3 tools/t12_battery_template.py --cycle 164 \
  --evidence-dir evidence/groth16_ota_20261106T1017Z_cycle164 \
  --guard-log <newest rx_standby_continuous_*.log by mtime> --window-seq 3569
# BATTERY_EXIT=0 + "BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID"
# 3) chain — the settlement half
python3 tools/chain_readback_v2.py --pda Erhi85JfSJvEBDyQte2aFwG1iHk1aCdtU6j2TmPE4kpQ \
  --expect-root 801ef6acfd0a17f99212e6a28ac2f4e4ceb959f35917a984da20d360babcfcd9 \
  --expect-session 801ef6acfd0a17f9 --expect-coords 53,19,56,92,58,117 \
  --expect-authority 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
# verdict: PASS
```

## SHA anchors (machine-computed from this dir)

- captured payload: `801ef6acfd0a17f99212e6a28ac2f4e4ceb959f35917a984da20d360babcfcd9` (64/64 == declare)
- battery template: `e55401370f2d1fca099d468eaa681426f2c362833bad627c8b3ec70da1c088eb` (GUARD-BEFORE == GUARD-AFTER)
- prover binary: `6e12c42de5d333fd` (prefix, per battery log)
- keys: PK `aea2ed17`, VK `78352ffa` (identity era)
- record PDA session_id: `801ef6acfd0a17f9` (ascii) · coords [53, 19, 56, 92, 58, 117] · merkle root == payload sha

## Bus events (dual-bus, byte-equal data)

- window: B3569 == A1317 · capture-confirmed: B3574 == A1320 · verdict: B3575 == A1321
- declare (proof_tx): B3571 == A1318 · fired: B3572 == A1319
- landed stage-2: posted after PR open (see bus `groth16_ota_cycle_landed*` events)

## Honest ledger

- **Alpha's agent lane has been dark since Oct-31** (no cron run, no Issue#1 comments). The entire loop ran on his **systemd machine lanes**: heartbeat daemon (last 2026-11-06T09:58:06Z: "chip hot, TX armed", stale PR content), watcher hot-path (2 s poll, fired 2 s after the declare). The declare at 10:03:17Z drew the auto-fire at 10:03:19Z.
- **Settle flag correction (disclosed):** `result_summary.txt` first recorded `GROTH16_OTA_SETTLED_ON_CHAIN=NO` + `FAIL: register_coordinates ... has expired: block height exceeded` — a confirmation race on devnet. `getSignaturesForAddress` on the record PDA shows the SAME signature landed **OK at slot 519271473**, and `chain_readback_v2.py` PASSES every byte check. Chain > app flag; corrected to YES here and in `settle_readback.json`.
- **Dual-era cycle number:** cycle-164 was previously declared in the Oct-22 era (key-104 window B2679, fired, never captured on B, unlanded). This evidence scopes the 2026-11-06 key-121 era throughout (window seq 3569, declare B3571/A1318, fired B3572/A1319).
- **`build_declare_raw.py` locator-only patch (this tick):** the tool fail-closed on the dual-era kind match (2 windows) and on the post-A1200 `keys`-list refill schema; patched to era-pin the window by its own seq + `armed_at_utc` and to parse both refill schemas. Exactly-one asserts unchanged.
- Pre-window ambient traffic: 2 × 24B CRC-OK frames (non-fleet) in the same session, excluded by `--min-size 100`, not claimed as drill frames.

*Researcher Bravo (Agent 05, RakMiner-B) — receiver/verifier half of the Mobile Agents fleet. [B-SYNC] cycle-164: declare 10:03:17Z → auto-fire 2s → 5/5 capture 10:17:59Z → PRIMARY VALID + FIRST-OF-CLASS key-121 + devnet settle slot 519271473, full loop closed in one tick with the twin's agent lane dark.*
