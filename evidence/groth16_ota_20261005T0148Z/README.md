# Groth16 OTA — cache_refill_first_use, 2026-10-05T01:48Z — A→B proof exchange with ALL THREE LEGS GREEN: radio 5/5 + pairing VALID + devnet settle

**Drill**: `groth16_ota`, kind `cache_refill_first_use` — first use of Alpha's
refilled canon-key cache, ordered by B at 01:05Z (B-outbox cache-refill order),
authored end-to-end by Alpha's agent lane at 01:35–01:52Z.

## Chain of custody

| Leg | Evidence |
|---|---|
| A declare | A-bus seq207 `groth16_proof_tx` 01:47:43Z, spec v2 full vector, proof SHA `cecbb8b8…73b5`, canon PK `8dda8b79…`/VK `7bd5683f…` measured at prove time |
| A fired | A-bus seq208 `groth16_tx_fired` 01:47:55Z–01:49:26Z, 5/5 TX_DONE, exit 0 |
| B window | B cycle-17, cert gate 17th consecutive PASS (armed 00:15:11Z → closed 02:15:11Z) |
| B capture | 5× CRC-OK 128 B byte-identical @903.9 MHz chan 3, SF9/125 kHz, SNR +10.8..+11.2 dB, LoRa CRC 0x4CD5 all five; first arrival 01:48:12.514Z wrap-corrected, inter-frame ~16.8 s |
| B SHA gate | `b_rx_extract.py --expect-sha cecbb8b8…` → `sha256_match=true`, exit 0 |
| B pairing PRIMARY | `zk_lorawan_prove verify` (arkworks BN254) at zk-lorawan root, canon disk keys, `ZK_LORAWAN_REPRODUCIBLE_SETUP` UNSET → **VALID, exit 0, 142.2 s** |
| B pairing CONTROL | known-VALID `bd4c9ab2` (PR#14) re-verified same session → VALID, exit 0, 142.3 s → RX path sound |
| Keys sha-guard | PK `8dda8b79…` / VK `7bd5683f…` byte-identical before/after |
| Settle | Cuneiform Devnet TX `3DZJquNsvqSLx8uihVaxT399PKHqzsXY47NKJKzVbNdUFmYrgXfVRehoy5R1ABPCUfXcJJxz3FfHHjKxbgfVZFfv`, finalized slot 507589350, 6/6 PASS |
| Readback | record PDA `F6wXuecm9q8Q2oGWUt6kpqY4HFsJCPZifssndC5bSGnH` read via public RPC: owner `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, 103 B, merkle root `cecbb8b8…` at offset 62, coords [253,147,102,74,199,254] present, session `cecbb8b83f7990a5` |

## Files

- `rx_payload.bin` — captured 128 B proof, SHA256 `cecbb8b83f7990a57233b3939ccb2e7036f9dfb83907fc26c44442c17ba703b5`
- `capture_log_excerpt.txt` — cycle-17 arm banner + the five 128 B packet blocks verbatim from `rx_standby_continuous_20261003T180951Z.log`
- `b_rx_extract_output.json` — full extractor output (all 11 CRC-OK packets in window, ambient included)
- `bus_events_drill.json` — A-bus seq 206–210 verbatim (cache_refill_notice, proof_tx, tx_fired, refill_complete, + B verdict cross-post)
- `bus_event_bravo_verdict_seq590.json` — B-bus verdict post (PASS, all legs)
- `pairing_verify_timed.log` — PRIMARY VALID + CONTROL VALID, timed
- `lora_chirp_recovery_gate.log` — cycle-17 arm certification (17th consecutive PASS)
- `settle_result_summary.txt` / `settle_tests_passed.txt` — Cuneiform settlement 6/6 PASS

## Honest ledger

- **Drill discipline**: A declared before fire (seq207 01:47:43Z → first send 01:47:55Z), full spec-v2 vector, canon keyset enforced at prove time by his patched cache builder. No gate violations.
- **Cycle-17 ambient**: 6×23 B ambient OTAA-join frames in window (ambient LoRa traffic, disclosed, excluded from the verdict); all 5 proof frames at 128 B with identical CRC — no size confusion possible.
- **Post-wrap capture**: the burst crossed the 32-bit count_us wrap (wrap at ~01:26:47Z); timestamps above are wrap-corrected (arm 00:15:11Z + count_us/1e6 + 4294.967296 s). Verify formula before use.
- **Second RF path**: no chan-6 multipath ghost this drill — all five proof frames arrived on chan 3 only. Cycle-17's ambient 23 B frames (crc 0x0B4B/0x9662/0xD5FC/0x79CA/0xB582/0xE3D5/0x92A4/0x859B) are the usual neighborhood OTAA traffic.
- **Bus cross-post lag**: B verdict posted to both buses 02:53:00Z, ~63 min after burst close — this tick ran long (extract + 2×142 s verifies + settle). Alpha's cache now holds 2 warm proofs (`a1706406`, `264a8fea`), canon-stamped.
- **Wallet**: settle fee 100,000 lamports CPI'd to treasury `CotbUcSMqaqn69YSmh2YgYZjKfE7cZk4fTsEmE3kfWJ`; balance 5.97953932 → 5.97826084 SOL.

## Reproduce (B side)

```bash
python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261003T180951Z.log \
  --min-size 128 --expect-sha cecbb8b83f7990a57233b3939ccb2e7036f9dfb83907fc26c44442c17ba703b5
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

Explorer: https://explorer.solana.com/tx/3DZJquNsvqSLx8uihVaxT399PKHqzsXY47NKJKzVbNdUFmYrgXfVRehoy5R1ABPCUfXcJJxz3FfHHjKxbgfVZFfv?cluster=devnet
