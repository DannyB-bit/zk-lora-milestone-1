# node-b-rx End-to-End RF RX Evidence — 2026-09-29 (RakMiner-B / Researcher B)

Captured UTC: 2026-09-29T01:14:28Z -> 01:44:28Z (RX window, timeout 1800)
Operator: Researcher B (Agent 05, "Bravo"), RakMiner-B, concentrator EUI 0x0016c001ff18afa3

Purpose:
Receiver-side evidence for RakMiner-A to RakMiner-B Milestone 1 deterministic
payload transfer, completing the end-to-end RF evidence rule of PR #2
(A-side TX evidence, committed by Researcher A / RakMiner-A).

TX side (per RakMiner-A, PR #2):
- Burst fired 2026-09-29T01:27:45Z (inside this RX window): 5/5 TX_DONE
- Payload: 240 bytes deterministic, SHA256 6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
- RF: 903.9 MHz, SF9, BW 125 kHz, 14 dBm, RF chain 0

RX settings:
- Target frequency: 903.9 MHz
- HAL radio A center: 904.3 MHz, channel IF -400000 Hz (channel mode 0, multi-SF)
- Spreading factor: SF9, Bandwidth: 125 kHz, single-input mode (-j), clock source 0
- Concentrator EUI (read from silicon at bring-up): 0x0016c001ff18afa3
- Recovery: LORA_CHIRP_RECOVERY_PASS=YES at 2026-09-29T01:14:28Z

RX command:
`timeout 1800 sudo /home/researcher-bravo/sx1302_hal/libloragw/test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 1`

RX result:
- Valid LoRa packet entries: 5
- CRC OK packets: 2 (each 240 bytes, both at 903.9 MHz)
- First CRC OK payload bytes: 240
- A TX payload SHA256: 6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
- B RX payload SHA256: 6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
- Payload SHA256 match: YES
- rx_exit_code.txt is 124 because the receiver was intentionally bounded by `timeout 1800`.

Conclusion:
End-to-end RF success observed per the M1 evidence rule: RakMiner-B decoded
CRC-OK LoRa packets at 903.9 MHz / SF9 during RakMiner-A's in-window burst,
and the received 240-byte payload SHA256 matched RakMiner-A's transmitted
payload SHA256 exactly.

Honest iteration history (all archived in-repo):
- node-b-rx_20260928T235039Z / T235856Z: recovery fail-closed (verifier path bugs, fixed)
- node-b-rx_20260929T000419Z: window open 00:04:29Z-00:11:29Z, 0 packets (A missed window)
- node-b-rx_20260929T004308Z: window open 00:43:18Z-00:50:18Z, 0 packets (A burst landed 21 min past close, honestly logged on A side as 5/5 TX_DONE into closed window)
- This artifact: 30-min window protocol, A burst inside window, 2 CRC-OK SHA-matched.

Notes:
- Receiver-side concentrator reset uses the June-faithful GPIO17 (SX1302) /
  GPIO22 (SX1261) sequence; power enable skipped, per this box's own June 30
  M1 evidence logs. The SPI data byte for raw probing is transfer byte index 4.
- Extraction: tools/b_rx_extract.py (STAT_CRC_OK=0x10 exact gate, interleaved-log
  salvage). Unit test: tools/test_b_rx_extract.py (PASS).

— Researcher B (Agent 05, RakMiner-B), coordinated via Hermes A2A with Researcher A.
