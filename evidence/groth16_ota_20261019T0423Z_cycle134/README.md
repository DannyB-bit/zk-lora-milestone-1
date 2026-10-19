# c-134 groth16_ota A->B evidence (RakMiner-B / Researcher Bravo, Agent 05)

**BUS 12th / PR-body 28th consecutive radio-to-chain loop. FIRST-OF-CLASS key-76.**

## Radio capture (node-b-rx)
- 5/5 CRC-OK 128B frames @ 903.9 MHz exact (radio A 904.3 - IF 400kHz), SF9 BW125, CR 4/8, chain 0
- SNR +10.8..+11.8 dB, 0 CRC-BAD; inter-frame 16.71..16.79 s uniform
- pre-wrap (+0s) burst, count_us 1343266570..1410294233, origin = listener boot banner 2026-10-19T03:59:13Z
- session segment: guard log lines 5985..6088 of rx_standby_continuous_20261015T171837Z.log

## Declaration + fire (fast channel)
- window declare B2238 == A917, armed 2026-10-19T03:59:13Z (+7200s), close 05:59:13Z; cert LORA_CHIRP_RECOVERY_PASS=YES, chip v1.0 (0x10), skew 0.0s, 5866s remaining at declare
- proof declare (groth16_proof_tx) A918 == B2239 byte-diff EQ (public_input_hashes, gateway, firmware, deposit, key id, deposit_commitment, proof sha)
- key-76 sha 78910fc8745af74416a761f8767902b773e9757a841e5ac08212d8825c8b7362, deposit 100045, identity era (VK 78352ffa / PK aea2ed17)
- warm cache per dual-bus cache_refill_notice B2234 == A916 (Alpha minted + self-verified keys 76/77 @133s each)
- fired: 5/5 TX_DONE @ 2026-10-19T04:22:49Z; declare-to-fire 79s (machine-derived from bus timestamps)

## Verification (this box, T12 battery)
- PRIMARY key-76 78910fc8: VALID exit=0 wall_s=159.6
- FIRST-OF-CLASS positively asserted: statement-class key-76 pih[-1]=70eb9e9bf896b810, prior-declares B=0 A=0, pih-only priors 0/0, unclassable 5
- Controls (2 DISTINCT classes): key-75 136a7be7 (c-133) VALID 160.0s; key-74 dfee9042 (c-132) VALID 160.1s — vendored byte-exact from pr99-head evidence BEFORE silicon (c-91 law)
- GUARD-BEFORE == GUARD-AFTER (binary 4c8e1f8a PK aea2ed17 VK 78352ffa); temp 35.5->38.4C throttled=0x0
- BATTERY_EXIT=0 attempt1 (first try); session-segment + digest-equality burst binding (v4 law)

## Settlement (Solana Cuneiform devnet)
- REGISTER_TX krQgTuS5eNK8JhQkK8mDgSzuMbv7LEdbzPfFaMrEgJTdQv6qSWJX2MfKjXWFARDX4Zd2zvrj2N2A2ASze63KTS slot 512679030 err=null
- RECORD_PDA 889z7ub9DptwWoNKbeCYNMGvY9Rm5STGwUgwK9mRefre; MERKLE_ROOT = payload sha 64/64; SESSION_ID 78910fc8745af744
- coords [199,101,53,29,152,16] = payload bytes 0..5; protocol fee 100000 lamports; wallet 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3, balance after 5.87598244 SOL
- chain_readback_v2 verdict PASS (session/coords/merkle/authority byte-match); signature machine-read from result_summary.txt and byte-matched against live getSignaturesForAddress (first hand-typed compare cell failed on a hand-copy typo — disclosed)

## Files
- b_rx_extract_output.json (fail-closed extractor rc=0, sha256_match true, 5 frames)
- c134_session_slice.log (session segment of the guard log)
- rx_payload_128b.bin (sha == declare 64/64)
- capture_meta.json (machine-derived), declare/rx_window_open/tx_fired dual-bus raws + declare_dual_bus_raw.json
- cycle134_window_declare.json (composer output), t12_cycle134_battery_attempt1.log (contract line BATTERY_EXIT=0)
- result_summary.txt + tests_passed.txt (settle artifacts), chain_readback.json (PASS), settle_readback.json (live sig match)

## Honest ledger
- extract-before-close per c-117 law (window close 05:59:13Z, all gates ran well before)
- single-tick declare-to-settle loop (declare 04:21:30Z -> fire 04:22:49Z -> battery done 04:34:19Z -> settle 04:35:16Z -> readbacks same tick)
- loop ordinal machine-counted on B bus (28 consecutive per PR-body series; BUS series 12th per dual-series disclosure A914)
- first signature-compare cell hand-typed the TX and failed on a typo; machine-read retry passed (hand-typed-constant law applied to our own check)
