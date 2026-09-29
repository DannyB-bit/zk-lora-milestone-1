# Node-A TX Evidence — First Real Groth16 Proof Over The Air (M2)

**Fired:** RakMiner-A (Agent 04), 2026-09-29 15:44:20Z → 15:48:45Z UTC
**Payload:** 128 bytes compressed Groth16 proof = A(32B G1) || B(64B G2) || C(32B G1)
**Proven on-node:** arkworks/ark-groth16, seed-42 canon PK (repo keys/proving_key.bin), ~10 min on ARM Cortex-A72
**Radio:** 903.9 MHz, SF9, 125 kHz, 14 dBm, 5 sends ≥10 s apart — 5/5 TX_DONE

## Integrity anchors
- tx_groth16_proof_128b.bin SHA256: `f8bec8809cdbe23e074ce6596345900e6ffcf3c5ef2c42d88c7dde5897ad8a04`
- Public input hashes (declared pre-fire, bus seq 26/47): identity `cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d`, nullifier `a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029`, attestation `8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a`, ciphertext `2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005`
- Declaration posted BEFORE firing per B's fire protocol (groth16_proof_tx, bravo bus seq 47)
- Full proof bundle JSON: proof_bundle.json (A/B/C compressed + uncompressed + all hashes)
- Radio log: tx_radio_log.txt (5x TX_DONE)
- Bus evidence: bus_events.json (decl seq 22 → proof_tx seq 26 → fired seq 27 → B state-sync reply seq 30)

## Honest ledger
- Window seq 32 (12:53–14:53Z): missed by 8 s (binary linked 14:50Z) — declared, no fire attempted
- Stale-watcher legacy misfires 1–3 (13:03Z, 15:17Z, 15:37Z): mine, owned, fixed (service restart 16:01Z; PR #5)
- This fire went into B's OPEN window (15:28:30Z → 17:28:30Z, armed seq 45), declared pre-fire
- RX verdict: pending from RakMiner-B (their window, their certified verifier)

## Verification recipe (any reviewer)
```
sha256sum tx_groth16_proof_128b.bin   # == f8bec8809cdbe23e074ce6596345900e6ffcf3c5ef2c42d88c7dde5897ad8a04
# decompress: bytes 0..32 = G1 A, 32..96 = G2 B, 96..128 = G1 C (arkworks compressed)
# verify against seed-42 canon VK (keys/verifying_key.bin) with 4 public input hashes above
```
— Researcher A (Agent 04, RakMiner-A), TX side
