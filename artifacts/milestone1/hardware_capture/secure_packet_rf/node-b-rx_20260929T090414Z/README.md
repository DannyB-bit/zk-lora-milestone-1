# node-b-rx_20260929T090414Z — FIRST over-the-air ZL1P secure packet (RakMiner-A → RakMiner-B)

## What this is
The fleet's first RF capture of a full ZK-LoRa secure packet: a 234-byte
ZL1P frame carrying a Groth16-reference proof binding, HMAC-authenticated
and stream-encrypted, fired by RakMiner-A over 903.9 MHz / SF9 / 125 kHz and
demodulated CRC-OK by RakMiner-B's always-on listener.

## Capture
- Window: always-on listener 2026-09-29T07:47:43Z -> 09:47:43Z (timeout 7200, -n 0)
- Arm gate: LORA_CHIRP_RECOVERY_PASS=YES @ 07:45:47Z (chip_id rc=0, chip 0x10, EUI 0016c001ff18afa3)
- Frame: chan 3 (mode 0, IF -400 kHz => 903.9 MHz exact), status 0x10 (CRC OK),
  SNR +11.5 dB, RSSI 196, size 234 B, count_us 270542581
- RF ghost twin: same burst demodulated corrupted on chan 6 (904.5 MHz),
  status 0x11 (CRC BAD), count_us 33 us earlier - retained as
  rx_secure_packet_ghost_crcbad_234b.bin
- TX side: Alpha declared the fire on the fast channel (event secure_packet_tx,
  bravo bus seq 18, posted 09:05:58Z): fired 09:03:41Z-09:03:55Z, TX_DONE 1/1, exit 0

## Byte-identity
- Captured packet SHA256 = 90164329f2c4f0a637f19fe18a3ee9338dd841f1b76161a8dba2e84d8768763c
- Alpha's declared packet SHA256 = identical - byte-exact match
- Header fields vs TX declaration: nonce, public_input, ceremony_hash, proof_hash
  all match exactly (verify_manifest.json holds the full record)

## Cryptographic gates (tools/zk_lora_secure_packet.py verify --tamper-test --nonce-db)
- packet_auth_ok = true (HMAC-SHA256 tag)
- decrypt_ok = true (plaintext hash matches embedded pt_hash)
- zk_reference_proof_verify_ok = true
- tamper_rejected = true (bit-flip in ciphertext -> auth fails)
- wrong_key_rejected = true
- replay: 2nd submission of same nonce -> replay_ok=false (nonce-db gate)
- Plaintext (99 B): ZK-LoRa M1 secure packet A->B 2026-09-29: M1 closed, PR3 merged, fast channel live, cuneiform next.
- END_TO_END_SECURE_PACKET_OK = YES

## On-chain settlement (Solana Cuneiform devnet, Program 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy)
- Register TX: 46LFuEnwk7oVK8W1Bvm4UBHTLyux3dtou2qqjWhVkaFBp2zxwsD2i4HzEG3MWRqG6M33Etk4HRSVXZh2iZTrNUPi (confirmed @ 2026-09-29T11:17:08Z)
- Record PDA: 72QCeXMXAqLAPaFV9fSpppp7ANKgXzJENeKdQ7BQAQoi, session 90164329f2c4f0a6
- merkle_root = captured packet SHA256 (read back equal); coords = proof_hash[0:6] = [44,221,209,176,190,54]
- 100,000-lamport CPI fee to treasury verified; evidence: solana-cuneiform-milestone1 artifacts/milestone1/devnet_bravo/secure_packet_settlement_20260929/

## New hardware observation - count_us wraps at 2^32 us
HAL count_us is a 32-bit microsecond counter: it wraps every ~71.6 minutes.
This 2-hour window contains one wrap; naive no-wrap timestamp math inverts the
packet order (ambient frames appear to precede the arm). Any window > 71.6 min
MUST account for the wrap when mapping count_us -> wall clock. This capture's
wall-clock time is anchored to Alpha's declared TX span (09:03:41Z-09:03:55Z).

## Honest disclosures
- The window's stdout was not durable for its first ~53 min (dead session pipe);
  remediated ~08:54Z via gdb dup2 to the durable log. Ambient frames before the
  remediation were recovered from the transcript reconstruction; the captured
  234 B secure packet and every frame after it were written live to the log.
- The artifact dir label (090414Z) predates the wrap-epoch correction; the
  authoritative capture time is inside Alpha's declared TX span (see above).
- No rx_window_open event declared for this window (always-on listener);
  Alpha's fire targeted the standing "B RX open until 09:47Z" state.

## Files
- rx_secure_packet_234b.bin - the captured CRC-OK frame (byte-exact vs TX)
- rx_secure_packet_ghost_crcbad_234b.bin - the RF-corrupted ghost twin
- raw_hal_rx_9039_sf9_125k.log - full window HAL log (14 CRC-OK packets)
- verify_manifest.json - full crypto-verify output
- nonce_db.txt - replay-gate nonce ledger
- result_summary.txt - KEY=VALUE summary (M1 standard)

- Researcher Bravo (Agent 05, RakMiner-B), 2026-09-29
