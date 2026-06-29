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

Do not overclaim:
- The proof code is a reference/structural prototype.
- This milestone does not yet provide production Groth16, halo2, arkworks, or gnark proof artifacts.
- Hardware/RF layout is documented, but packet-forwarder/photo-backed Raspberry Pi/RAK evidence is still pending.
- Zcash payment scanning belongs to later milestones.

Forum checklist:
- Present this repo as the multi-language identity/proof prototype.
- Link `artifacts/milestone1/README.md` and `docs/milestone1_hardware_layout.md`.
- Include negative-test and production-proof work as next steps.
- Avoid implying this is audited cryptography.
