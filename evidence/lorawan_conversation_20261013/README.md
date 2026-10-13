# A-B LoRaWAN Conversation - 2026-10-13 (Dan-ordered, all legs over real RF)

**The order:** carry a conversation between the twins via LoRaWAN chirps ONLY - real execution,
log all evidence, each twin confirms the other's messages are legit + received + true.

## The conversation (3 legs, all cross-confirmed)

| Leg | Direction | Payload | TX (Z) | RX proof | Cross-confirmation |
|---|---|---|---|---|---|
| 1 | A->B | 128B compressed Groth16 proof (SHA d3ccac4a...477c) | 08:32:57 | 5/5 CRC-OK, SHA match, T12 battery VALID | Alpha rx_confirm A563: TRUE/LEGIT vs 3 machine sources |
| 2 | B->A | 23B reply-chirp ack (SHA cc1b77d5...b131) | 10:17:51 + 10:18:16 | 2 independent OTA receptions, SNR 11.2/11.8 dB, CRC OK | Alpha chirp_received_RECEIPT A580: sha_match=true |
| 3 | A->B | 128B Groth16 reply (SHA d3ccac4a...477c) | 10:22:11 | 5/5 CRC-OK, SNR 10.8-11.2 dB, SHA match, extractor rc=0 | This evidence dir + B-bus receipt B1471/A583 |

Radio: 903.9 MHz exact, SF9/125 kHz, 14 dBm conducted on both SX1302 nodes.

## Honest ledger (misses disclosed per fleet law)
- Leg 2 took 3 armed windows: Alpha's first two captures missed MY 09:56/10:01 acks -
  his node had 4-6 stale HAL RX listeners contending for the SPI bus (a fresh window's
  GPIO reset kills any in-flight frame) plus a C stdio buffer-flush loss at session end.
  Both disclosed by Alpha same-turn (A567/A570), both fixed (stale listeners killed,
  stdbuf line-buffering), window re-armed clean at 10:17:29Z -> next fires captured 2x.
- My side fired the staged ack 6 times total (09:47, 09:56, 10:01, 10:09, 10:17:27,
  10:17:53) - every fire logged in b_ack_fire_*.log; only the last two (into the clean
  window) were received, exactly as his miss forensics predict.
- The 09:47 fire preceded Alpha's first RX window (armed 09:55:37Z) - timing miss on my
  side, disclosed; the watcher then auto-fired on each of his declares.

## Files
- b_ack_fire_*.log - 6 B-side TX logs (staged SHA, GPIO reset sequence, TX done, re-arm)
- leg3_rx_log.log - B-side raw RX log for Alpha's leg-3 burst
- leg3_b_rx_extract.json - fail-closed extractor output: 5 CRC-OK frames, 128B, 903.9 MHz,
  sha256_match: true vs the A582 declaration, exit 0 (PR#52 exit-contract build)
- bus_conversation_transcript.json - 53 events from both buses: declares, fires, receipts,
  confirmations, honest-miss disclosures

## Reproduce
```bash
python3 tools/b_rx_extract.py leg3_rx_log.log \
  --expect-sha d3ccac4a568fe31de57bbb3626ba573f0fbf8f955e24bac4d742d3534843477c --min-size 100
# expect: crc_ok=5, sha256_match=true, exit 0
```

**Verdict: zk-LoRaWAN works.** The twins held a real, three-leg, bidirectional conversation
over LoRa chirps at 903.9 MHz with cryptographic SHA cross-confirmation on every message,
and every miss was disclosed and root-caused on the record.


## Layman's explanation of the verification chain (Dan's ask)

Think of it like verifying a phone call happened:
1. **The transcript (bus events)** = the phone company's call log: shows who claimed what, when. But a skeptic says "both phones share the same account" — so the log alone proves *claims*, not *physics*.
2. **The raw radio recordings (RX logs, both sides now in this bundle)** = two tape recorders, one at each end of the line, that independently recorded the *same sounds*. Shared-token skeptics are answered by the recordings: BOTH radios' front-ends caught the identical bytes with real signal strength (SNR ~11 dB) — a fake would have to be planted on both tapes, in both radios, in the same milliseconds.
3. **The blockchain entry (devnet PDA)** = a notarized seal on the envelope content: anyone can read it live today and confirm the exact digest, without asking either twin.
4. **The declare-before-fire order** = the sender wrote the sealed envelope's contents down publicly BEFORE the mail was sent — so the receiver can't have "found" bytes that fit after the fact.

**What "irrefutable" still awaits:** which *specific radio* sent the bytes (identity binding). The seal proves "these exact bytes flew between two SX1302 radios," not "it was RakMiner-B's radio." That is precisely the Groth16 identity-proof milestone already on the roadmap: bind the radio's identity into the zero-knowledge proof itself, so the proof carries the signature of the sender without revealing the payload.

## Both radios' raw captures now in this bundle
- `leg1_rx_session_slice.log` + `leg1_b_rx_extract.json` — B-side raw capture of Alpha's leg-1 burst (5/5, SHA match) — closes the "both radios recorded it" gap for leg 1
- `leg3_rx_log.log` + `leg3_b_rx_extract.json` — B-side raw capture of Alpha's leg-3 burst (5/5, SHA match)
- Alpha's `rx_conv_leg3.log` (his side, leg-2 receipt, referenced A580) + his TX logs on his node complete the A-side half
