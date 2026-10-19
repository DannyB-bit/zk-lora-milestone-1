# c-135 groth16_ota A->B evidence (RakMiner-B / Researcher Bravo, Agent 05)

**BUS 13th / PR-body 29th consecutive radio-to-chain loop. FIRST-OF-CLASS key-77.**

## Radio capture (node-b-rx)
- 5/5 CRC-OK 128B frames @ 903.9 MHz exact (radio A 904.3 - IF 400kHz), SF9 BW125, CR 4/8, chain 0
- SNR +10.8..+11.2 dB, 0 CRC-BAD; inter-frame 16.72..16.92 s uniform
- pre-wrap (+0s) burst, count_us 636487445..703601382, origin = listener boot banner 2026-10-19T10:00:14Z
- session segment: guard log lines 6298..6400 of rx_standby_continuous_20261015T171837Z.log

## Declaration + fire (fast channel)
- window declare B2265 == A927, armed 2026-10-19T10:00:14Z (+7200s), close 12:00:14Z; cert LORA_CHIRP_RECOVERY_PASS=YES, chip v1.0 (0x10), skew 1.0s, 6572s remaining at declare
- proof declare (groth16_proof_tx) A928 == B2267 byte-diff EQ (public_input_hashes, gateway, firmware, deposit, key id, deposit_commitment, proof sha)
- key-77 sha e7361bfeded81516ea7d0eff6f7baa2b12fab33b7a09de2a131e80f0f04b87f9, deposit 100046, identity era (VK 78352ffa / PK aea2ed17)
- warm cache per dual-bus cache_refill_notice (Alpha A seq 926 "RELIGHT + REFILL 08:3xZ", keys 77/78/79 minted + self-verified @133s each; B-bus mirror byte-equal)
- fired: 5/5 TX_DONE @ 2026-10-19T10:12:03Z; declare-to-fire 80s (machine-derived from bus timestamps)

## Verification (this box, T12 battery)
- PRIMARY key-77 e7361bfe: VALID exit=0 wall_s=160.2
- FIRST-OF-CLASS positively asserted: statement-class key-77 pih[-1]=8cd4dd6ef5de6517, prior-declares B=0 A=0, pih-only priors 0/0, unclassable 5
- Controls (2 DISTINCT classes): key-76 78910fc8 (c-134) VALID 160.3s; key-75 136a7be7 (c-133) VALID 160.0s — vendored byte-exact from pr100-head evidence BEFORE silicon (c-91 law)
- GUARD-BEFORE == GUARD-AFTER (binary 4c8e1f8a PK aea2ed17 VK 78352ffa); temp 35.0->37.9C throttled=0x0
- BATTERY_EXIT=0 attempt1 (first try); session-segment + digest-equality burst binding (v4 law)

## Settlement (Solana Cuneiform devnet)
- REGISTER_TX 2xfj6A16wkDPKLTmgnJeYqgPkJMQakeYc6zob4u6h1KmTz2mmGhihJDjZq9eWNae5jTawHqiMmDZQQifwZRBby26 slot 512768340 err=null finalized
- RECORD_PDA BNfoVJyTmks93Hn3dBdaEQQwSvsNuJtbHWayXEQxagp; MERKLE_ROOT = payload sha 64/64; SESSION_ID e7361bfeded81516
- coords [106,67,119,125,119,128] = payload bytes 0..5; protocol fee 100000 lamports; wallet 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3, balance after 5.87470396 SOL
- chain_readback_v2 verdict PASS (session/coords/merkle/authority byte-match); signature machine-read from result_summary.txt and byte-matched against live getSignaturesForAddress on the record PDA

## Files
- b_rx_extract_output.json (fail-closed extractor rc=0, sha256_match true, 5 frames)
- c135_session_slice.log (session segment of the guard log)
- rx_payload_128b.bin (sha == declare 64/64)
- capture_meta.json (machine-derived), declare/rx_window_open/tx_fired dual-bus raws + declare_dual_bus_raw.json
- cycle135_window_declare.json (composer output), t12_cycle135_battery_attempt1.log (contract line BATTERY_EXIT=0)
- result_summary.txt + tests_passed.txt (settle artifacts), chain_readback.json (PASS), settle_readback.json (live sig match)

## Honest ledger
- extract-before-close per c-117 law (window close 12:00:14Z, all gates ran well before)
- single-tick declare-to-settle loop (declare 10:10:43Z -> fire 10:12:03Z -> battery done 10:28:51Z -> settle 10:30:11Z -> readbacks same tick)
- loop ordinal machine-counted on B bus (29 consecutive per PR-body series; BUS series 13th per dual-series disclosure)
- window-rotation disclosure: this tick's pre-run gather (09:57Z) showed the prior listener (PIDs 570068/570069) closing 09:59:54Z; the live re-check at 10:00:0xZ found the fleet-rx-standby supervisor had re-certified (47th gate PASS 10:00:14Z) and re-armed 10:00:14Z -> 12:00:14Z — the c-135 declare went into the fresh window, not the stale one (gather-vs-post law applied)
- stage-1 rx_verdict bus post initially failed FileNotFoundError (battery attempt log not yet staged into the evidence dir at that moment — the settle step stages it); re-run after settle staged the log, posted B2271 == A931 byte-diff EQ. Disclosed same-turn.
