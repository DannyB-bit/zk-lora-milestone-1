# Groth16 OTA — autonomous daemon-fire, 2026-10-04T19:22Z — FIRST FULLY-UNATTENDED A→B ZK PROOF EXCHANGE: radio 5/5 + pairing VALID + devnet settle

RakMiner-A's watcher consumed B's `rx_window_open` (drill `groth16_ota`) and his daemon
completed declare→fire **with his Hermes agent lane dark** (peer_status_check 404,
`run_d60e83d9`, since ~11:26Z — 8 h before this drill). Every gate that makes a drill
lawful was upheld unattended: declare-before-fire, canon keyset, drill-gated legacy
suppression, fail-closed cache. This proves the fleet's ZK RF exchange is now
**daemon-grade**: it no longer depends on either agent session being alive.

## Chain of custody
1. **B window** — `rx_window_open` B-bus seq551 (19:21:09Z), drill `groth16_ota`,
   armed 2026-10-04T18:14:10Z → closes 20:14:10Z. Cycle-14 of the continuous standby
   guard; cert gate `LORA_CHIRP_RECOVERY_PASS=YES`
   (`lora_chirp_recovery_gate.log`, 13th consecutive PASS in the chain, 0 FAIL).
2. **A declaration** — A-bus seq194 `groth16_proof_tx` 19:21:10Z (1 s after the
   window event): proof SHA256
   `bd4c9ab27d199f5559d55ac41c955f0ed31cd6d618f468dcb315fd0b4bd3788b`, 128 B
   A(32)||B(64)||C(32), full spec-v2 public-input vector (4×32B hashes, gateway,
   deposit 100000, firmware), canon PK `8dda8b79…`/VK `7bd5683f…` **measured at prove
   time**, kind=autonomous daemon-fire, cache-populated (no prover run inside the
   window).
3. **A fired** — A-bus seq195 `groth16_tx_fired` 19:22:30Z, 5/5 TX_DONE, exit 0.
   The whole declare→fire took 80 s, unattended.
4. **B capture** — 5× CRC-OK 128 B byte-identical frames @ 903.9 MHz chan 3,
   SF9/125 kHz, SNR +10.8..+11.2 dB, LoRa CRC `0x108E` on all five. First arrival
   19:21:16.686Z (6 s after declaration), inter-frame 16.76 s. No count_us wrap in
   play (burst all pre-wrap; the window's wrap fell at 19:25:44Z, after the burst).
   One 128 B chan-6 @904.5 MHz CRC-fail copy (`0x1828`, SNR -11.0) — multipath
   duplicate of the same wave, discarded, disclosed.
5. **B extract** — `tools/b_rx_extract.py --min-size 128 --expect-sha bd4c9ab2…` →
   `sha256_match: true`, exit 0 (`b_rx_extract_output.json`).
6. **B pairing battery** — `zk_lorawan_prove verify` (arkworks BN254) at zk-lorawan
   repo root, canon disk keys, `ZK_LORAWAN_REPRODUCIBLE_SETUP` UNSET:
   - **PRIMARY** `bd4c9ab2` → **VALID**, exit 0, **142.0 s** (full-PK canon path —
     a ~6 s return would indicate the in-memory regen path; none observed).
   - **CONTROL** PR#13 `fc816080` (known-VALID) → **VALID**, exit 0, 142.1 s (same
     session/binary/VK/keys) → RX verifier path sound.
   - Keys sha256-guarded byte-identical before and after the battery:
     `8dda8b79…`/`7bd5683f…`.
7. **Settle** — Cuneiform Devnet `register_coordinates` TX
   `4P7KViea19JDei2uTiW9Khcm3HaqmAhaaV2VNn65Zc7gwQEFZCZhdvfVcKSSH7EEvgVPsKBrEygM92CAFxknpry`
   (finalized, slot 507479783), session `bd4c9ab27d199f55`, PDA
   `ANSHm2HwujSqzhb4QnaWkYPkhZ5KDY2EfFSkQFUX4Y7c`, coords = proof bytes 0..5 =
   [20,162,130,194,129,147], merkle root = proof SHA256, 100k-lamport treasury CPI,
   6/6 PASS. Independent readback: PDA owned by Program 2is5Q4rP…, 103 B digest-only
   account, coords + root byte-verified on-chain, decode-info scan clean (ZK
   Settlement Law G5). Settlement artifacts live in the cuneiform repo
   `artifacts/milestone1/devnet_bravo/groth16_ota_settlement_20261004_daemon_fire/`.

## Honest ledger
- **Window-consumption asymmetry (disclosed)**: A's watcher consumed the **B-bus
  copy** (seq551, 19:21:09Z) of the window — the cross-post to his own bus (A-bus
  seq196) landed at 19:22:48Z, ~90 s AFTER his fire completed, because B's
  cross-post turn was blocked on a bus readback. The window he acted on was live,
  certified and identical in content. No integrity impact; recorded so the
  timestamps in `bus_events_drill.json` don't confuse a future auditor: seq196's
  ts is the cross-post arrival, not the window's opening.
- **B watcher HOLD verified**: my own B-side watcher posted `watcher_notice`
  seq554 `hold_non_b_ack` on the cross-posted A-bus window (seq196) — the
  drill-gate correctly suppressed any B-side auto-fire. No double-fire anywhere.
- **Agent-lane disclosure**: this drill was B-armed/B-verified while A's agent lane
  was dark. A's side of the evidence (cache state, his fire log) is daemon-authored
  only. When A's agent lane returns, his review of this PR is the pending step.
  Nothing on this branch asserts A-authored claims beyond his daemon's bus
  declarations.
- **A's TX-side report**: 5/5 TX_DONE — consistent with B's 5/5 CRC-OK capture.
- **A heartbeat**: still current (B-bus seq556 19:48:25Z, EUI hot, TX armed) —
  daemon healthy throughout.

## Reproduce
```bash
python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261003T180951Z.log \
  --min-size 128 --expect-sha bd4c9ab27d199f5559d55ac41c955f0ed31cd6d618f468dcb315fd0b4bd3788b
cd ~/fleet-repos/zk-lorawan
./target/debug/zk_lorawan_prove verify <A_hex[0:64]> <B_hex[64:192]> <C_hex[192:256]> \
  cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d \
  a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029 \
  8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a \
  2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005 \
  0016c001ff18afa3903900000000000000000000000000000000000000000000 \
  100000 656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
# expect: VALID (exit 0, ~142 s full-PK canon path)
```
