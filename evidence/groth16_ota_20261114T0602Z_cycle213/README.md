# groth16_ota cycle-213 — RF evidence, on-chain settle, and the FIRST REAL chirp245 drill

**Cycle:** 213 · **Proof key:** key-134 (FIRST rung of Alpha's refill pair 134/135)
**Window:** B4220/A1418 — armed 2026-11-14T06:02:11Z, closed 08:02:11Z (listener exit rc=124)
**Declare:** 2026-11-14T06:03:38Z (EARLY, 7115 s remaining — c-146 law)
**Fired:** 2026-11-14T06:04:58Z — 5/5 TX_DONE, **~80 s watcher hot-path, no LLM turn**
**PR:** https://github.com/DannyB-bit/zk-lora-milestone-1/pull/150

## Radio capture — groth16_ota burst (ground truth)

- 5/5 CRC-OK 128 B frames @ **903.900 MHz** (radio A 904.3 − IF −400 kHz), SF9 / 125 kHz
- SNR **+10.5 .. +11.2 dB**, inter-frame 16.73/16.74/16.78/16.71 s uniform, **pre-wrap (+0 s)**
- `count_us` 93687548 .. 160644077 (listener process-boot origin)
- `sha256_match` true; `sha256(rx_payload_128b.bin)` == the declared payload digest **64/64**

## Pairing + battery verdict (B die)

- **FIRST-OF-CLASS key-134**: statement class `pih[-1]=61adca309ee53c24`, prior-declares B=0 A=0,
  pih-only-priors B=0 A=0 — positively asserted, not inferred
- `BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID`, `BATTERY_EXIT=0` via the exit contract
- PRIMARY key-134 **161.8 s**; controls key-131 **161.5 s** + key-130 **161.0 s** (distinct statement classes)
- `GUARD-AFTER` binary/PK/VK pins unchanged; silicon 47.2 °C, no throttling

**Battery provenance (two attempts, both disclosed):** attempt1 was invoked directly, so its stdout was
redirected without the exit-code line (the template does not print `BATTERY_EXIT`; the family logs carry it
because the launcher echoes the status). The tracked wrapper recorded `BATTERY_EXIT=0` for attempt1, and
attempt1's artifacts are preserved as `t12_cycle213_battery_attempt1.log`. The settler gate requires a
complete-line `BATTERY_EXIT=0`, so attempt2 was re-run through `~/fleet/scripts/launch_t12_cycle213.sh`
from the **main** repo worktree (c-207 law) with the exit code recorded inline — `t12_cycle213_battery_attempt2.log`
/ `t12_cycle213_battery.log`. Both runs produced the same verdict and the same wall-clock branch timings.

## On-chain settle (Cuneiform devnet)

| Item | Value |
|---|---|
| TX | `4RVswoLCDsH8JALNBihBui9H8cDziAL1AyFEoiFTUg9PSRWqAjC6LDKwtSMe9seFZRM6oiB1Atpc9iEe3YMjPs8V` |
| PDA | `EktpjR3tiMPDfKDpGvgwJisUHyWD6tABjKUN7FMT9hMT` |
| Settle slot | 522119697, err null, exactly one signature |
| Readback | verdict **PASS**, all byte checks true |
| Session (on-chain) | `9a35251f3712f114` |
| Coords | `[5,110,149,83,89,56]` == payload bytes 0..5 |
| Merkle root | on-chain == `sha256(rx_payload_128b.bin)` 64/64 |
| Fee | 100000-lamport protocol fee, CPI-collected (wallet `14aTW9yp` 5.81205844 → 5.81077996 SOL) |
| Tests | 6/6 PASS, 0 failed |
| Owner | `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy` |

## 🔒 chirp245_sealed_frame — the drill that finally has an RF artifact

The previous drill verdict (B4108/A1411) claimed `DECRYPT_OK` while **zero** 245-byte frames had ever been
captured over the air; that claim was retracted (B4206/A1417) and the drill was held OPEN. This cycle closed it:

- **Frame built with the canonical tool** (`solana-cuneiform-milestone1/tools/chirp245.py build`, Alpha's @391ec84):
  X25519 fresh-ephemeral DH + HKDF-SHA256 (salt `zk-lora-chirp245-v1`, info `chirp245-aead-key`) + **AES-256-GCM**,
  layout `ver(1)|n(1)|nonce(12)|ephpub(32)|ct(183)|tag(16)` = **245 B**, sealed to B's public key, 81 coords,
  frame sha `135476e3…`
- **Payload posted to both buses** (`chirp245_tx_payload` B4224/A1421) — Alpha fetched the bytes from the bus,
  never retyped them
- **Alpha transmitted it radio-only** inside the declared window (`chirp245_tx_fired` B4226/A1422): 5 sends,
  fired 06:14:24Z
- **B captured 5/5 CRC-OK 245 B frames** in the session slice (sha match true, SNR +10.5..+11.5 dB,
  measured inter-frame ≈ 2.2 s)
- **Canonical `verify`/`open_chirp` decrypted the captured bytes**: 81 coords, leading coords byte-match the seal
- **Verdict published only after the artifact existed**: `chirp245_rx_verdict` B4227/A1423

**Provenance disclosed:** the ciphertext was sealed on B (sealing needs only B's public key); the RF transmit was
Alpha's radio. This proves the 245 B RF capacity + the X25519/HKDF/AES-256-GCM open path end to end — it is not
evidence of an independently-sealed payload.

**Minor deviation (honest):** Alpha's `chirp245_tx_fired` event states ">=10s apart per app schedule", but the
captured inter-frame spacing measures ≈2.2 s. The capture is 5/5 valid; the spacing claim in Alpha's event does
not match the RF measurement.

## Proof cache

key-134 = FIRST rung of Alpha's refill pair **A1412/B4111** (keys 134/135). After this cycle the warm rungs are
**[135]** — the cache is NOT at 0 warm, so **no `cache_refill_ask` was posted**.

## File inventory

`capture_meta.json`, `provenance.json`, `chain_readback.json`, `settle_readback.json`, `settle_result_summary.txt`,
`settle_tests_passed.txt`, `settle_stdout.log`, `b_rx_extract_output.json`, `c213_session_slice.log`,
`chirp245_extract_output.json`, `chirp245_decrypt_result.json`, `declare_{A,B,dual}_bus_raw.json`,
`rx_window_open`/`tx_fired` bus raw, `rx_payload_128b.bin`,
`t12_cycle213_battery{,_attempt1,_attempt2}.log`, `bus_stage2_raw.json`
