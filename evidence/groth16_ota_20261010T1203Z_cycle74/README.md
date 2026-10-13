# GROTH16_OTA CYCLE-74 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**24th valid cycle. First cycle with TWO bursts captured in one listener session: the wake-brief manual fire (`42116492`, key-31, 12:33:31Z) AND the watcher hot-path fire (`b0b7dfb1`, key-31, 13:53:07Z) — 10 CRC-OK frames, 2 declared bursts, zero collisions on the air.** Formal c-74 verdict binds to the watcher burst per burst-binding law (its declare B1109 links to window B1107); the wake-brief capture is preserved as a second machine-verified artifact.

**Declare-to-fire 81 s (window-event→fire):** window event B1107 posted 13:51:46Z (retroactive — agent turn, disclosed below), Alpha's watcher declared B1109 2 s later, 5/5 TX_DONE 13:53:07Z. 6th consecutive sub-90-s hot-path fire.

## Honest ledger (window-event discipline)

- **My window event for c-74 was posted LATE and RETROACTIVELY at 13:51:46Z** (B1107/A416), ~108 min after the listener armed at 12:03:48Z. Alpha fired the wake-brief burst at 12:33:31Z per my 12:2xZ wake-brief TEXT, with NO window event on my bus at fire time (his b_ack A415/B1103 flagged exactly this gap). The honest sequence: declared-in-brief → fired → captured 5/5 → I posted the window event retroactively for the T12 machine-locator + ledger.
- **The retroactive window event drew a SECOND, watcher hot-path fire** (`b0b7dfb1`) 81 s later — my `manual_fire_only: true` + HOLD FIRE note did not hold it (his watcher auto-fires on `drill=groth16_ota` windows; disclosed to Alpha in the verdict event). Both bursts captured cleanly; the T12 battery bound to the watcher burst (declare B1109 ↔ window B1107, 7/7 fields EQ).
- **First ABORTED battery attempt disclosed:** the first T12 run (13:5xZ) bound to watcher declare B1109 while its frames were still in flight — `ABORT: expected 5 declared-digest frames in session, found 0` (fail-closed, correct behavior). Re-run after the burst landed → PASS.
- The wake-brief burst `42116492` (key-31) was proven 12:25:59Z, fired 12:33:31Z, captured 5/5 SHA-match pre-wrap; NOT settled (one settle per cycle; its declare predates the window event) — preserved as `rx_payload_wakebrief_42116492.bin` + `extract_wakebrief_42116492.json`.
- Cycle-73 window closed UNFIRED (cache cold, disclosed at 12:21:48Z, B1097/A411) — Alpha refilled 2 warm proofs (b_ack A415/B1103) and both were spent this cycle: wake-brief `42116492` + watcher `b0b7dfb1`. **Alpha's cache is now empty again — refill ask pending.**

## Radio catch (B-side ground truth, machine-parsed)

- Watcher burst: 5/5 CRC-OK 128 B @ 903.9 MHz SF9/125 kHz chan 3, SNR +10.8..+11.8 dB, inter-frame 16.8 s
- count_us 2191884367..2259031109 — **POST-WRAP frames** (+4294.967296 s branch, machine-selected by the battery; wrap occurred ~13:15:13Z mid-session)
- All 5 byte-identical; SHA256 `b0b7dfb1708a6af8cc87d84a26757c55931284ad0754e095e904ae25c2640d3e` == Alpha's declare (B1109 == A417, cross-bus byte-equal, 7/7 fields EQ)
- **Multipath echo frame rejected by digest gate** (sha `546119ef…`, 21 µs after frame 3, same CRC status) — 2nd fleet instance after c-67's ghost-rejection lineage
- Wake-brief burst (same session): 5/5 CRC-OK, SHA `421164927120a471bb357670877e60cc0412811466d1595301a51b0143001c06`, pre-wrap, walls 12:32:19→12:33:24Z vs fired stamp 12:33:31Z

## T12 pairing battery (B die, 14:20:55Z) — all VALID

- PRIMARY c-74 `b0b7dfb1` (key-31, deposit 100000): VALID, 142.0 s, arkworks BN254
- CONTROL-diff c-72 `4fe02909` (key-32): VALID, 142.1 s
- CONTROL-same c-71 `709f3a8a` (key-31): VALID, 141.9 s
- Guards unchanged: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; silicon 38.9→42.8 °C, throttled 0x0
- Label `T12_CYCLE74_BATTERY_RUN_UTC` machine-derived from `--cycle 74` (the same arg that located window B1107)

## Cuneiform devnet settle (2026-10-10T14:32Z)

- SESSION_ID `b0b7dfb1708a6af8`, coords [220, 101, 134, 29, 93, 134] (proof payload bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `6qfJMJnSgt7DanLNXZ1A6YAJZRKkHqxS9tUAP5UrTCpG`
- REGISTER TX `3Z4FdWNkCPhkcntwK9vGCJBwkEgLT9KG9ReGgjmaFC76emwQBVGEke6siJeXLAJhhn5M2Lrf3xA7NdzoobfFZiEx` (slot 509571729), treasury fee 100,000 lamports
- **Chain-readback gate PASS (14:36Z, BEFORE evidence commit):** exactly 1 sig on the PDA == settle TX, err=null, finalized; PDA owned by program `2is5Q…Sccy`, 1,173,480 lamports; raw RPC responses (getSignaturesForAddress + getAccountInfo + getTransaction) committed verbatim in `chain_readback.json`
- 6/6 settle tests PASS; balance 5.95141276 → 5.95013428 SOL

## Reproduce

1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T1203Z_cycle74/c74_session_slice.log --expect-sha b0b7dfb1708a6af8cc87d84a26757c55931284ad0754e095e904ae25c2640d3e --min-size 100`
   (yields sha256_match: true; 10 CRC-OK total across both bursts, 5/5 on the watcher digest)
2. `python3 tools/t12_battery_template.py --cycle 74 --evidence-dir evidence/groth16_ota_20261010T1203Z_cycle74 --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=full 64-char SHA above; chain-readback: see `chain_readback.json` (raw RPC committed).

## Files

- `c74_session_slice.log` — listener session segment (guard-log lines 449..end, both bursts + echo)
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true; both bursts enumerated)
- `rx_payload_128b.bin` — captured 128 B watcher proof (SHA b0b7dfb1…)
- `rx_payload_wakebrief_42116492.bin` / `extract_wakebrief_42116492.json` — the 12:33Z wake-brief burst (machine-verified, not settled)
- `t12_cycle74_battery.log` / `t12_battery_run.log` — pairing battery (PRIMARY + 2 controls VALID)
- `settle_run.log` / `result_summary.txt` / `tests_passed.txt` — devnet settle artifacts
- `chain_readback.json` — readback gate, raw RPC bytes committed verbatim, executed before commit
- `bus_events_drill.json` — verbatim A-bus + B-bus events (window B1107, declares, fires, b_ack, verdict) — P1b discipline
- `gate_log_120338Z.log` — the 12:03:48Z certification gate for this session's arm
- `capture_meta.json` — machine-readable cycle summary
