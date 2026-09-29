# node-b-rx_20260929T152830Z — Groth16 OTA drill window (watcher-stale forensic capture)

- **Window**: armed 2026-09-29T15:28:30Z, closes 17:28:30Z (timeout 7200, always-on `-n 0`)
- **RX line**: `./test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0` (radio A 904.3, IF −400 kHz ⇒ 903.9 MHz exact, mode 0, SF7–SF12)
- **Certification**: `LORA_CHIRP_RECOVERY_PASS=YES` 15:27:07Z (chip_id rc=0), HAL banner `chip version is 0x10 (v1.0)`, `Waiting for packets...` 15:28:30Z
- **Burst source**: Alpha TX-side auto-fire 15:37:30Z (bus `tx_burst_fired` seq 45/46 on B bus, seq 24/25 on A bus), ran 22.7 s, exit 0
- **Finding**: the burst was the **LEGACY deterministic M1 payload** (SHA `6f6b11f6…e5c6eb3d`), NOT the requested 128 B compressed Groth16 proof — third occurrence (13:03Z, 15:17Z probe, 15:37Z). Alpha's running watcher process predates his drill-gate patch: disk `watch_bravo.py` contains the `groth16_ota` suppression gate, but the live process posted no `watcher_notice` and fired anyway. Not a B-side miss.
- **Alpha status**: `groth16_proof_decl` 14:48:23Z — honest declaration: `zk_lorawan_prove` not pre-built; rustup installed 14:38Z; arkworks build running (PID 82267); ETA 30–90 min; will fire the real 128 B proof into the next declared window after posting `groth16_proof_tx`.

## On-air telemetry (this capture)
- 5/5 CRC-OK (STAT 0x10) 240 B packets @ 903.9 MHz, SF9, SNR +10.2…+11.5 dB
- All 5 byte-identical to the legacy payload; SHA256 match = True (re-verified with `tools/b_rx_extract.py` + `sha256sum` over the extracted `.bin` files)

## result_summary.txt

```
RX_START_UTC=2026-09-29T15:28:30Z
RX_CLOSE_UTC=2026-09-29T17:28:30Z
VALID_PACKET_COUNT=5
CRC_OK_COUNT=5
RX_PAYLOAD_SHA256=6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
PAYLOAD_SHA256_MATCH=YES
PAYLOAD_KIND=LEGACY_M1_DETERMINISTIC_NOT_GROTH16
END_TO_END_RF_SUCCESS=NO (radio leg YES; drill payload NOT satisfied)
GROTH16_OTA_DRILL=SATISFIED_NO
WATCHER_STALE_EVIDENCE=YES
ALPHA_BUILD_STATUS=arkworks_build_running_PID82267_ETA_30_90min
```
