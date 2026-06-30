# Forum Readiness Notes

Status: prototype-ready for community review, not production-ready.

Verified locally:
- Python reference proof runner passes.
- Full `python verify_all_proofs.py` suite passes 20/20 runtimes.
- C++ verifier source builds and runs with Clang on Windows amd64.
- Rust WASM verifier builds for `wasm32-unknown-unknown`; artifact captured in `artifacts/milestone1/`.
- `benchmark_milestone1.py` records separate reference proof generation and verification timings.
- Rust operator builds.
- TypeScript operator builds and runs `npm test`.
- Go operator builds and runs `go test` plus `go run . --test`.
- RAK Miner A hardware evidence shows SX1302 SPI access, chip `0x10`, and repeated LoRa TX bursts completed.
- RAK Miner B hardware evidence shows SX1302 SPI access, chip `0x10`, and HAL RX bring-up.

Do not overclaim:
- The proof code is a reference/structural prototype.
- This milestone does not yet provide production Groth16, halo2, arkworks, or gnark proof artifacts.
- The committed B-side RF attempts did not decode a valid packet; do not claim end-to-end A-to-B packet receipt until `artifacts/milestone1/hardware_capture/end_to_end_rf_success/` is populated with CRC/hash-match evidence.
- Zcash payment scanning belongs to later milestones.

Forum checklist:
- Present this repo as the multi-language identity/proof prototype.
- Link `artifacts/milestone1/README.md`, `docs/milestone1_hardware_layout.md`, and `docs/MILESTONE_1_REVIEWER_EVIDENCE.md`.
- Include negative-test and production-proof work as next steps.
- Avoid implying this is audited cryptography.
