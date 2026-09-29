# Node-B RX Evidence — First Over-The-Air Groth16 Proof Captured (M2)

**Receiver:** RakMiner-B (Agent 05), window `node-b-rx_20260929T152830Z` (armed 15:28:30Z, certified: recovery PASS 12:50:04Z + chip_id rc=0).
**TX:** RakMiner-A fired 5x 128 B proof frames 15:44:20Z→15:48:45Z (PR #6 `node-a-tx_20260929T154420Z`).

## Capture
- 5/5 **CRC-OK 128 B** frames @ 903.9 MHz / SF9 / 125 kHz, SNR +11.0..+11.5 dB, ~17.2 s spacing, all byte-identical
- RX payload SHA256 `f8bec8809cdbe23e074ce6596345900e6ffcf3c5ef2c42d88c7dde5897ad8a04` == A's pre-fire declaration (bravo bus seq47) == PR #6 committed TX bin (byte-identity, sha256sum on disk)
- Construction: A(32 B G1) ‖ B(64 B G2) ‖ C(32 B G1), arkworks compressed — fits the 255 B LoRa MTU with 127 B to spare

## Verify leg — BLOCKED, honestly disclosed
The on-chip Groth16 pairing check cannot run yet: the circuit binds **8 public inputs**, and the drill declaration spec only required 4 (identity/nullifier/attestation/ciphertext hashes). The **gateway_address (32 B)** was never declared (elided in PR #6 as `<32-byte gateway address>`), and it is not derivable — Groth16 rejects all wrong bindings.
Tested on-chip against the seed-42 canon VK (`ZK_LORAWAN_REPRODUCIBLE_SETUP=1`): 11 gateway candidates (zeros, A/B fleet wallets, Cuneiform program + treasury pubkeys, both node EUIs left/right-padded) → **all INVALID**, tamper control also INVALID (verifier sound). A's decryption-key/coordinate/firmware inputs decode to the repo canon demo values (ciphertext hash matches demo set exactly), so only the gateway (and/or PK source) remains.

**Ask to Alpha (drill spec v2):** `groth16_proof_tx` must declare the FULL public input vector — proof SHA + 4 hashes + `gateway_address_hex` + `deposit_value` + `firmware_hash_hex` — plus which PK/VK the proof was generated against (seed-42 reproducible vs repo-committed `keys/`).

## B-side honest ledger
- Listener exited 16:01Z (clean SPI close, cause not in log) — A's 16:55:37Z test-window hotfire (`8f2fe020…`, bus seq32) fired into dark air on my side: **B-side miss, disclosed**
- My 15:53:48Z `rx_verdict` (seq50) was posted before processing A's seq47/48 — misdiagnosis window, corrected by A's seq30 state-sync
- RX re-armed 17:44:42Z (clean 2 h window to 19:44:42Z, zero 128 B frames — expected, no fire) and again post-evidence (recovery PASS re-run)

## Files
- `rx_groth16_proof_128b.bin` — captured payload, byte-exact
- `rx_capture_full.log` — full listener log (17 packets, incl. 23 B SF10 noise + CRC-BAD RF ghosts)
- `rx_parser_output.json` — `tools/b_rx_extract.py` output (gates: STAT_CRC_OK=0x10, min-size 128)
- `result_summary.txt` — KEY=VALUE summary

— Researcher Bravo (Agent 05, RakMiner-B), RX side
