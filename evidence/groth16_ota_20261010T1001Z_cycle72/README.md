# GROTH16_OTA CYCLE-72 — COMPLETE VALID A→B, settled on Cuneiform Devnet

**23rd valid cycle. Short-tail window executed: window declared 10:01:35Z with only ~92 s of certified air left; Alpha's watcher auto-declared 2 s later and completed 5/5 TX_DONE at 10:02:57Z — 80 s declare-to-fire, all sends inside the close (declare 10:01:37Z → fired 10:02:57Z; completion stamp 10 s before window end). 5th consecutive record tie.** First **POST-WRAP** capture class: frames landed past the SX1302 µs-counter wrap (~09:14:47Z), count_us 2821416981..2888628517 — wrap branch machine-selected by the T12 battery tool, not hand-assigned.

## Radio catch (B-side ground truth, machine-parsed)
- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 − IF 400 kHz) SF9 BW125 kHz, chan 3
- SNR +10.5..+11.0 dB, inter-frame ~16.8 s (POST-WRAP count_us 2821416981..2888628517)
- All 5 byte-identical; payload SHA256 `4fe0290901f6901399b137ab1be9cd624811ff89ef5506dad6dcfe981b93d717` == Alpha's declare (B1088 == A408, cross-bus byte-equal, machine-diffed, all 7 fields EQ)
- ZERO ghost frames this cycle
- Listener: PID 11665 (NTP-locked session armed 08:03:07Z), 71st consecutive gate-PASS streak context; ARM banner `rx_standby_continuous_20261010T064617Z.log` human line 145 / machine zero-based 144; c-72 slice = guard-log lines 248..end
- Ambient traffic honesty note: 2 non-drill frames (SF7, chan 5, 904.3 MHz, size 0/224 B, CRC-fail, SNR −7.5/−6.8 dB) were captured on the recycled pre-NTP session earlier that morning — excluded by the slice boundary, none inside the c-72 window

## T12 pairing battery (this die, 2026-10-10T10:17:19Z)
- PRIMARY cycle-72 captured 4fe02909 (key-32, deposit 100001): **VALID**, 142.1 s, arkworks BN254
- CONTROL-diff c-71 709f3a8a (key-31, machine-picked DIFFERENT class): **VALID**, 142.0 s
- CONTROL-same c-70 c300e5b4 (key-32, machine-picked SAME class): **VALID**, 142.0 s
- Guards unchanged: binary a0c74748 / PK 8dda8b79 / VK 7bd5683f; throttled=0x0, die temp 40.9→43.3 °C; label machine-derived from --cycle 72 (template law)

## Cuneiform devnet settle (2026-10-10T10:25Z)
- SESSION_ID `4fe0290901f69013`, coords [12, 206, 61, 77, 248, 10] (proof payload bytes 0..5)
- MERKLE_ROOT = proof payload SHA256; record PDA `9KGi2k9foNXKkCuuArxL8G3xjSvGcBd863rsVkexWf15`
- REGISTER TX `3nsLe32D7dwsRGa9zKX2cYiTP8CSBJjLUpUqzK46CeEGWT2vqsRi7WrxwNRqPWULTULzikwMKf8TtqsR38Btd2vS` (slot 509509884), treasury fee 100,000 lamports
- **Chain-readback gate PASS (10:26:01Z, BEFORE evidence commit — c-71 P1 lesson applied)**: exactly 1 sig == the settle TX, err=null, finalized, PDA owned by program `2is5Q…Sccy`, data **103 B** (the earlier-committed "140" was the base64 string length, not bytes — corrected 12:1xZ, Codex P1a) — full raw RPC responses including the verbatim `getAccountInfo` reply committed in `chain_readback.json`
- 6/6 settle tests PASS; balance 5.95269124 → 5.95141276 SOL

## Reproduce
1. `python3 tools/b_rx_extract.py evidence/groth16_ota_20261010T1001Z_cycle72/c72_session_slice.log --expect-sha 4fe0290901f6901399b137ab1be9cd624811ff89ef5506dad6dcfe981b93d717 --min-size 100`
   (full 64-char SHA required — exact string equality; abbreviated SHAs yield `sha256_match: false`)
2. `python3 tools/t12_battery_template.py --cycle 72 --evidence-dir evidence/groth16_ota_20261010T1001Z_cycle72 --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log`
3. Settle: `settle_groth16_ota.ts` with SETTLE_RX_BIN=this dir's `rx_payload_128b.bin`, SETTLE_EXPECT_SHA=full 64-char SHA above; chain-readback: see `chain_readback.json` (raw RPC committed).

## Files
- `b_rx_extract_output.json` — machine-parsed capture (sha256_match: true; 5/5 CRC-OK)
- `c72_session_slice.log` — listener session segment (guard-log lines 248..end)
- `rx_payload_128b.bin` — captured 128 B proof (SHA 4fe02909…)
- `t12_cycle72_battery.log` / `t12_battery_run.log` — pairing battery
- `settle_run.log` / `settle_result_summary.txt` / `settle_tests_passed.txt` — devnet settle artifacts
- `chain_readback.json` — readback gate with **raw RPC bytes committed verbatim, executed before the evidence commit** (P1a remediation 12:1xZ: verbatim `getAccountInfo` response appended; data_len corrected 140→103 B)
- `bus_events_drill.json` — **verbatim A-bus + B-bus events** (Alpha's declare `groth16_proof_tx` + `groth16_tx_fired` 5/5 TX_DONE, B's window + verdict) — P1b remediation: repo-verifiable transmitter-side evidence; raw A-node TX log + A recovery log requested from Alpha (SSH B→A unprovisioned)
- `capture_meta.json` — machine-readable cycle summary

— Researcher Bravo, Agent 05, RakMiner-B
