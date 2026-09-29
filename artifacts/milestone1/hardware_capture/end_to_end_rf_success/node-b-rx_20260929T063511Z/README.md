# node-b-rx End-to-End RF RX Evidence — 2026-09-29 FAST-CHANNEL COORDINATED (RakMiner-B / Researcher B)

Captured UTC: 2026-09-29T06:35:21Z -> 07:05:21Z (RX window, timeout 1800, exit 124)
Operator: Researcher B (Agent 05, "Bravo"), RakMiner-B, concentrator EUI 0x0016c001ff18afa3

Purpose:
First fully machine-to-machine-coordinated A→B LoRaWAN transfer. This window
was NOT declared via 20-minute polling or human relay: it was armed, certified,
and announced on the fleet fast channel (event bus, port 8643), and
RakMiner-A's watcher AUTO-FIRED the burst on the rx_window_open event —
zero human latency, zero LLM turns.

Coordination timeline (event bus records, both nodes):
- 06:24:16Z  bravo bus server_boot (fast channel deployed, systemd user unit)
- 06:24:49Z  heartbeat_bravo cross-posted to alpha bus (RTT 253.9 ms)
- 06:35:21Z  window armed + certified: LORA_CHIRP_RECOVERY_PASS=YES, chip_id
             rc=0 (chip version 0x10, EUI 0x0016c001ff18afa3), HAL banner
             + "Waiting for packets..." (third consecutive clean start this day)
- 06:37:30Z  rx_window_open posted to both buses (bravo seq 4, alpha seq 9,
             cross-bus RTT 57.6 ms), carrying closes_at_utc + config + expected SHA
- 06:39:00Z  alpha bus tx_burst_fired: watcher fired automatically, 22.7 s
             burst run, exit 0 — 169 s after window open
- 07:05:21Z  window closed (timeout-bounded); extraction + SHA verdict below

RX settings:
- Target frequency: 903.9 MHz (radio A center 904.3 MHz, channel IF -400000 Hz, channel mode 0)
- Spreading factor: SF9, Bandwidth: 125 kHz, single-input mode (-j), clock source 0
- Recovery gate: LORA_CHIRP_RECOVERY_PASS=YES at 2026-09-29T06:35:21Z

RX command:
`timeout 1800 sudo /home/researcher-bravo/sx1302_hal/libloragw/test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 1`

RX result:
- Valid LoRa packet entries: 4 (all CRC-OK, status 0x10)
- CRC OK 240-byte target packets: 2 (both at 903.9 MHz, SNR +11.5 / +11.8 dB)
- Ambient frames: 2 × 23-byte third-party IoT traffic (904.1 MHz SNR -14.5;
  903.9 MHz SNR -15.8), excluded by the 240-byte size gate, recorded in
  rx_extract.json with full metadata — nothing hidden
- First CRC OK payload bytes: 240
- A TX payload SHA256: 6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
- B RX payload SHA256: 6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d
- Payload SHA256 match: YES
- END_TO_END_RF_SUCCESS=YES (per M1 evidence rule: CRC OK >= 1 AND byte-exact
  SHA match between A TX and B RX)

Conclusion:
The complete machine-to-machine loop is proven:
  rx_window_open (58 ms cross-bus RTT) -> alpha watcher auto-fire (06:39:00Z)
  -> 2x CRC-OK 240B captures at 903.9/SF9/SNR +11.5 -> SHA256 byte-exact match.
This is the second independent end-to-end A→B capture of the day (first:
node-b-rx_20260929T011418Z, PR #3) and the first requiring no human in the
coordination path. The fleet now closes fire drills at wire speed.

— Researcher B (Agent 05, RakMiner-B), 2026-09-29
