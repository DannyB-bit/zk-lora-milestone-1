# groth16_ota cycle-212 — RF evidence + on-chain settle

**Cycle:** 212 · **Proof key:** key-133 (SECOND rung of Alpha's refill pair A1403/B4085, keys 132/133)
**Window:** B4100/A1407 — armed 2026-11-12T15:55:46Z, closed 17:55:46Z (listener exit rc=124)
**Declare:** 2026-11-12T16:18:37Z (EARLY, 5829 s remaining — c-146 law)
**Fired:** 2026-11-12T16:19:56Z — 5/5 TX_DONE, **79 s watcher hot-path, no LLM turn**
**PR:** https://github.com/DannyB-bit/zk-lora-milestone-1/pull/149

## Radio capture (ground truth)

- 5/5 CRC-OK 128 B frames @ **903.900 MHz** (radio A 904.3 − IF −400 kHz), SF9 / 125 kHz
- SNR **+10.5 .. +11.2 dB**, inter-frame 16.73/16.74/16.71/16.75 s uniform
- `count_us` 1377505187 .. 1444434323 (listener process boot origin)
- 13 packets demodulated in the session segment: 5 digest-matched (`38b9e402…`), remainder excluded by the
  digest+size+CRC gate
- `sha256_match` true; `sha256(rx_payload_128b.bin)` == declared payload digest **64/64**

## Pairing + battery verdict (B die)

- **FIRST-OF-CLASS key-133**: statement class `pih[-1]=34bd1b35c5a04724`, prior-declares B=0 A=0,
  pih-only-priors B=0 A=0 — positively asserted, not inferred
- `BATTERY_VERDICT: PRIMARY VALID + CONTROLS VALID`, `BATTERY_EXIT=0` via the exit contract
- Full log: `t12_cycle212_battery_attempt1.log` (the non-attempt file is the pre-run copy)

## On-chain settle (Cuneiform devnet)

| Item | Value |
|---|---|
| TX | `26axTNbLGdUqbGpPpNndodao2GGc59HyXGYfBw7yusNeHp5YRc8TYtY9PSs6gKvG8YsKiZe7TeVkgZF3aubKCZT6` |
| PDA | `2Q4WUyaCyMQnJaVk6KbgSK2t7ecdZRvRPNPjXQX4BUzT` |
| Settle slot | 521624329 (block_time 2026-11-12T23:11:38Z), err null, exactly one signature |
| Readback | verdict **PASS**, all byte checks true, slot 521624597 @ 2026-11-12T23:12:43Z |
| Session (on-chain) | `38b9e402d2417a93` |
| Coords | `[140,36,150,85,199,198]` == payload bytes 0..5 |
| Merkle root | on-chain == `sha256(rx_payload_128b.bin)` 64/64 |
| Fee | 100000-lamport protocol fee, CPI-collected (wallet `14aTW9yp` 5.81333692 → 5.81205844 SOL) |
| Tests | 6/6 PASS, 0 failed |
| Owner | `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy` |

## Stage-2 bus readback (dual-bus, byte-equal)

| Event | Bravo seq | Alpha seq |
|---|---|---|
| `groth16_ota_cycle_landed` | 4204 | 1415 |
| `groth16_ota_cycle_landed_stage2` | 4205 | 1416 |
| `chirp245_verdict_correction` | 4206 | 1417 |

Raw: `bus_stage2_raw.json`. **No `cache_refill_ask` was posted** — the proof cache is not at 0 warm
(Alpha notice A1412/B4111 minted keys 134/135; machine-derived from the newest notice, not typed).

## ⚠️ Honest disclosure — the chirp245_sealed_frame drill in this window was NOT re-flown

Bus event **B4108 / A1411** (`chirp245_rx_verdict`, 2026-11-12T17:23:16Z) reported `DECRYPT_OK` for drill
`chirp245_sealed_frame`, frame sha `6f67d0eb…`, 81 coords. Machine verification shows **no sealed frame
flew in this window**:

| Check | Result |
|---|---|
| 245-byte frames in the cycle-212 session slice | **0** |
| 245-byte frames in the continuous standby log(s) | **0** |
| cycle-212 extract inventory | 13 packets: 5× 128 B (`38b9e402…`) + 8 non-matching — **no 245 B frame** |
| decrypt artifact | `~/fleet/logs/chirp245_decrypt_output.json`, regenerated **2026-11-12T17:21:59Z** from the archived frame bytes |
| frame sha `6f67d0eb…` | identical to the 2026-11-06 capture (`evidence/chirp245_frame_6f67d0eb_closed_20261106/`) |

**Conclusion:** the verdict decrypted the *archived 2026-11-06 frame*; the sealed frame was **not** transmitted
and **not** re-captured in the cycle-212 window. A corrective event (`chirp245_verdict_correction`, B4206/A1417)
was posted on both buses with this evidence.

**Scope of the correction:** only the chirp245 sealed-frame claim. The `groth16_ota` half of cycle-212 — the
128 B proof burst capture, the FIRST-OF-CLASS pairing verdict, the battery gate, the devnet settle and the
independent RPC readback — is **unchanged and remains VALID**.

**Still required to close the chirp245 drill:** transmit the 245 B sealed frame inside a declared window, keep the
RF capture artifact (245-byte frame in the session slice + digest match), and publish `DECRYPT_OK` only after that
artifact exists.

## File inventory

`capture_meta.json`, `chain_readback.json`, `settle_readback.json`, `settle_result_summary.txt`,
`b_rx_extract_output.json`, `b_rx_extract_stdout.log`, `c212_session_slice.log`, `cycle212_window_declare.json`,
`declare_{A,B,dual}_bus_raw.json`, `rx_window_open_{A,B}_bus_raw.json`, `tx_fired_{A,B}_bus_raw.json`,
`rx_payload_128b.bin`, `t12_cycle212_battery{,_attempt1}.log`, `provenance.json`, `bus_stage2_raw.json`
