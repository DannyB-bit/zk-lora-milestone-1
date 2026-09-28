# node-a-tx End-to-End RF TX Evidence — 2026-09-28 (RakMiner-A / Researcher A)

Captured UTC: 2026-09-28T15:54:22Z (TX window 15:54:36Z → 15:54:52Z)
Operator: Researcher A (Agent 04, "Alpha"), RakMiner-A, concentrator EUI 0x0016c001ff1aadc0

Purpose:
A-side deterministic Milestone 1 payload transmission over the live SX1302 RF chain,
using the new `zk_lora_tx_app` (deterministic file-payload transmitter built against
the patched sx1302 HAL on RakMiner-A), coordinated with RakMiner-B via Hermes A2A.

TX settings:
- Frequency: 903.9 MHz
- SF: 9
- Bandwidth: 125 kHz
- Power: 14 dBm
- RF chain 0, SX1250 single-input mode
- Payload: 240 bytes, deterministic (see tools/node_a_tx_evidence.sh payload recipe)
- Sends: 5/5 TX_DONE — `A_LORA_TX_FILE_SEND_COMPLETE=YES (5/5 sends, 240 bytes)`

Payload SHA256:
6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d

Included:
- lora_chirp_recovery.log with LORA_CHIRP_RECOVERY_PASS=YES (gateway services stopped,
  GPIO25 reset sequence, chip_id verification: chip version 0x10 (v1.0), EUI verified)
- payload_path.txt / payload_stat.txt / payload_sha256.txt
- tx_start_utc.txt and tx_end_utc.txt
- full TX log (tx_repeated_payloads.log) — 5× TX_DONE, exit 0
- tx_exit_code.txt
- tx_send_complete_lines.txt — all A_LORA_TX_FILE_SEND_* status lines
- a_lora_tx_file_send_complete_count.txt

Iteration history (honest record):
- 20260928T143606Z — recovery PASS, stock test_loragw_hal_tx 5/5 (39-byte tool-generated pattern; superseded — not the deterministic payload)
- 20260928T144243Z — recovery PASS, stock tool 5/5 (as above; superseded)
- 20260928T152626Z — zk_lora_tx_app first run: txgain_setconf failed (mix_gain=0 invalid; fixed to 5 per stock tool workaround)
- 20260928T153615Z — lgw_start failed: SX1250 STANDBY_RC (fixed: reset_lgw.sh start immediately before lgw_start, stock parity; sudo)
- 20260928T154807Z — lgw_start OK, lgw_send rejected: BANDWIDTH NOT SUPPORTED (fixed: pkt.bandwidth must be BW_125KHZ enum, not kHz value)
- 20260928T155422Z — **SUCCESS: 5/5 TX_DONE, exit 0, deterministic 240-byte payload**

Evidence rule:
This artifact proves A-side TX only. End-to-end RF success requires RakMiner-B CRC OK
and RX SHA256 matching A payload SHA256 (above). RakMiner-B RX verification evidence
should be committed under node-b-rx_<UTCSTAMP> with the same recovery + SHA discipline.

Reproduction:
- tools/node_a_tx_evidence.sh — full harness (recovery → deterministic payload → TX → evidence files)
- zk_lora_tx_app.c source: sx1302_hal/libloragw/tst/zk_lora_tx_app.c on RakMiner-A
  (build: gcc -O2 -o tst/zk_lora_tx_app tst/zk_lora_tx_app.c -Iinc -I../libtools/inc -L. -L../libtools -lloragw -ltinymt32 -lrt -lm, from libloragw/)
