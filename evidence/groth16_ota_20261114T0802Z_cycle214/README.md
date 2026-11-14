# groth16_ota cycle-214 — FINAL cycle of the current proof-key ladder

**Cycle:** 214 · **Proof key:** key-135 (**FIRST-OF-CLASS**, and the **LAST rung** of Alpha's ladder `range(31,136)`)
**Window:** B4237/A1426 — armed 2026-11-14T08:02:32Z, closed 10:02:32Z
**Declare:** 2026-11-14T09:02:20Z (EARLY, 3614 s remaining — c-146 law)
**Fired:** 2026-11-14T09:03:41Z — 5/5 TX_DONE, **80 s watcher hot-path, no LLM turn**
**PR:** https://github.com/DannyB-bit/zk-lora-milestone-1/pull/151

## Radio capture (ground truth)

- 5/5 CRC-OK 128 B frames @ **903.900 MHz** (radio A 904.3 − IF −400 kHz), SF9 / 125 kHz
- SNR **+10.2 .. +11.0 dB**, inter-frame 16.75/16.72/16.72/16.73 s uniform, **pre-wrap (+0 s)**
- `count_us` 3596002053 .. 3662914826 (listener process-boot origin)
- `sha256_match` true; `sha256(rx_payload_128b.bin)` == the declared payload digest **64/64**

## Pairing + battery verdict (B die)

- **FIRST-OF-CLASS key-135**: statement class `pih[-1]=9c255419e8037e2f`, prior-declares B=0 A=0,
  pih-only-priors B=0 A=0 — positively asserted, not inferred
- `BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID`, `BATTERY_EXIT=0` via the exit contract
- PRIMARY key-135 **161.8 s**; controls key-134 **161.5 s** + key-133 **161.0 s** (distinct statement classes)
- `GUARD-AFTER` binary/PK/VK pins unchanged; silicon 46.7 °C, no throttling

**Battery provenance (single attempt, clean):** launched via `~/fleet/scripts/launch_t12_cycle214.sh` from the
**main** repo worktree (c-207 law), so the log carries a complete-line `BATTERY_EXIT=0` inline — the c-213 lesson
applied, no second attempt was needed.

## On-chain settle (Cuneiform devnet)

| Item | Value |
|---|---|
| TX | `26bYHQNRRuoVkWb7kvQM97t8xDtrY2DCFfa93cXMN9mA1aF6vb855qQaPzJsiYNxZxqyVaDHR7kxUAnQrFj3Vfkp` |
| PDA | `3aF5JGtUVRud5avvvb8u2Ub8gWTdPwKZTgkGQPqnyUm1` |
| Settle slot | 522138836 (block_time 2026-11-14T09:23:19Z), err null, exactly one signature |
| Readback | verdict **PASS**, all byte checks true |
| Session (on-chain) | `6005c219048e1b2b` |
| Coords | `[92,214,32,7,57,189]` == payload bytes 0..5 |
| Merkle root | on-chain == `sha256(rx_payload_128b.bin)` 64/64 |
| Fee | 100000-lamport protocol fee, CPI-collected (wallet `14aTW9yp` 5.81077996 → 5.80950148 SOL) |
| Tests | 6/6 PASS, 0 failed |
| Owner | `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy` |

## Proof cache — now EMPTY (0 warm rungs)

key-135 was the **last** rung of Alpha's on-disk ladder `range(31,136)`. After this cycle the cache holds **zero**
warm keys, so the **c-139 0-warm law fires**: a `cache_refill_ask` for key ids **136/137** (machine-derived as
max+1/max+2 of the newest notice's key ids) rides the stage-2 post as its own event, on Bravo's bus as **B4245**.
Alpha's own `alpha_final_status` (B4242/A1429) states the same conclusion in advance: `key_135_is_last: true`,
`warm_rungs: 0`, "cycle-215 is NOT possible without a new mint", and that it would mint 136/137 on the ask.

## Stage-2 bus readback

| Event | Bravo seq | Alpha seq |
|---|---|---|
| `groth16_ota_cycle_landed` | 4243 | **pending mirror** (Alpha's bus server defect, see below) |
| `groth16_ota_cycle_landed_stage2` | 4244 | **pending mirror** |
| `cache_refill_ask` | 4245 | **pending mirror** |

**Alpha bus defect (measured, disclosed):** from 09:27Z, `POST` to Alpha's bus (`192.168.1.219:8643`) fails with
`RemoteDisconnected` **after** the server assigns a seq — Bravo's landed post returned 1431 and never committed.
`/health` reports `events: 1430` while `/events` serves only 1429. Bravo's bus is therefore the authoritative
record for the c214 close, the three Alpha mirrors are recorded as pending in `bus_stage2_raw.json`, and Alpha was
briefed (A2A) to repair its own bus, re-mirror the three events byte-for-byte from Bravo's payloads, and mint the
136/137 pair. No field was re-typed to work around the failure.

## File inventory

`capture_meta.json`, `provenance.json`, `chain_readback.json`, `settle_readback.json`, `settle_result_summary.txt`,
`settle_tests_passed.txt`, `settle_stdout.log`, `b_rx_extract_output.json`, `c214_session_slice.log`,
`declare_{A,B,dual}_bus_raw.json`, `tx_fired_{A,B}_bus_raw.json`, `rx_payload_128b.bin`,
`t12_cycle214_battery{,_attempt1}.log`, `bus_stage2_raw.json`
