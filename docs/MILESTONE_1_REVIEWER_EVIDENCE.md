# Milestone 1 Reviewer Evidence

This file is the reviewer-facing index for the Milestone 1 evidence package.

## Executive status

Milestone 1 is complete as a reference prototype and hardware bring-up package:

- The multi-language proof suite runs and passes.
- The C++ verifier builds and runs.
- The WASM verifier builds and is committed as an artifact.
- The benchmark script records proof generation and verification timing.
- RAK Miner A proves real SX1302/SPI LoRa transmit bring-up.
- RAK Miner B proves real SX1302/SPI LoRa receive bring-up.
- The hardware layout and capture process are documented.

End-to-end A-to-B RF packet decode is not yet claimed in this repo. The current committed B-side RX attempts did not decode a valid packet, and that result is preserved honestly.

## Artifact map

| Evidence area | Path | Reviewer read |
| :--- | :--- | :--- |
| Full proof suite | `artifacts/milestone1/verify_all_proofs_report.txt`, `VERIFICATION_REPORT.md` | 20/20 runtimes passed |
| C++ native verifier | `artifacts/milestone1/cpp_verifier_build_report.md`, `artifacts/milestone1/cpp_verifier_run.log` | Builds and runs with Clang |
| WASM verifier | `artifacts/milestone1/wasm_verifier_build_report.md`, `artifacts/milestone1/zk_lora_wasm_verifier.wasm` | WASM artifact committed with SHA-256 |
| Benchmark | `artifacts/milestone1/benchmark_report.md` | Local reference proof timing captured |
| Hardware layout | `docs/milestone1_hardware_layout.md` | 3-node RAK/Raspberry Pi topology documented |
| RF recovery/runbook | `tools/lora_chirp_recovery.sh`, `docs/codex_a_b_rf_evidence_runbook.md` | LoRa Chirp service stop, reset, chip check, and coordinated A/B capture procedure |
| RAK Miner A baseline | `artifacts/milestone1/hardware_capture/node-a-tx/README.md` | A host inventory and proof/benchmark run |
| RAK Miner A real TX | `artifacts/milestone1/hardware_capture/node-a-tx/interactive_privileged_retry/README.md` | SPI opened, SX1302 chip `0x10`, TX completed |
| RAK Miner A repeated TX | `artifacts/milestone1/hardware_capture/node-a-tx/manual_tx_for_b_rx_20260630/repeated_tx_burst.log` | Five LoRa TX bursts completed with exit 0 |
| RAK Miner B baseline | `artifacts/milestone1/hardware_capture/node-b-rx/README.md` | B host inventory and proof/benchmark run |
| RAK Miner B RX attempts | `artifacts/milestone1/hardware_capture/node-b-rx/real_lora_rx_20260630/README.md` | RX hardware bring-up succeeded; no valid packet decoded |

## What the RAK evidence proves

RAK Miner A:

- Ran on Raspberry Pi / RAK hardware.
- Opened SPI against the SX1302 concentrator.
- Detected SX1302 chip version `0x10`.
- Used GPIO25 for SX1302 reset and GPIO22 for SX1261 reset in the successful TX path.
- Sent deterministic 240-byte payload bursts at 903.9 MHz, SF9, 125 kHz, 14 dBm.
- Completed all five repeated bursts with `A_LORA_TX_FILE_SEND_COMPLETE=YES` and exit status `0`.

RAK Miner B:

- Ran on Raspberry Pi / RAK hardware.
- Opened SPI against the SX1302 concentrator.
- Detected SX1302 chip version `0x10`.
- Ran a corrected HAL RX command during a timestamped A TX window.
- Preserved the receive result honestly: `Nb valid packets received: 0 CRC OK (1)`.

## What is not claimed yet

This repository does not yet claim:

- A valid packet was decoded by RAK Miner B.
- TX payload SHA-256 equals RX payload SHA-256.
- CRC-pass end-to-end A-to-B RF packet reconstruction.
- Production Groth16, halo2, gnark, arkworks, or Zcash consensus proof verification.

Those claims require an additional committed success folder with the actual B-side RX packet bytes, CRC pass, and hash match.

## Success artifact import target

If Phase 15/16 evidence exists on the miners or USB evidence freeze, import it under:

`artifacts/milestone1/hardware_capture/end_to_end_rf_success/`

Required files:

- `README.md` with exact claim, UTC window, devices, and RF settings.
- A-side TX log showing packet bytes/hash and TX completion.
- B-side RX log showing packet bytes, RSSI/SNR, CRC pass, and RX completion.
- `tx_payload.bin` and `rx_payload.bin`, or canonical hex dumps if binary capture is unavailable.
- `tx_payload.sha256` and `rx_payload.sha256`.
- Reconstruction output and hash, if compression/restore was used.
- Service-stop/reset log showing conflicting gateway services were stopped and SX1302/SX1261 reset pins used.
- `lora_chirp_recovery.log` from `tools/lora_chirp_recovery.sh` showing `LORA_CHIRP_RECOVERY_PASS=YES` on both nodes.

Minimum reviewer-safe success test:

```text
TX_SHA256 == RX_SHA256
CRC_PASS == YES
RX_PACKET_BYTES > 0
```

Until that folder exists, use the current repo as a Milestone 1 prototype plus hardware bring-up proof, not an end-to-end RF decode proof.
