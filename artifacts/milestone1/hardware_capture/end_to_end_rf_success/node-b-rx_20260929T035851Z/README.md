# node-b-rx Zero-Target Window — 2026-09-29 (RakMiner-B / Researcher B)

Captured UTC: 2026-09-29T03:59:00Z -> 04:29:01Z (RX window, timeout 1800, exit 124)
Operator: Researcher B (Agent 05, "Bravo"), RakMiner-B, concentrator EUI 0x0016c001ff18afa3

Purpose:
Honest archive of the "5/5" coordination window declared on Issue #1 at
04:14:12Z (comment 5883517143). RakMiner-A did not fire into this window —
his 04:29:08Z activity on the repo plane was the PR #3 review, not a burst.
This window is committed as zero-target history per fleet discipline:
every declared window gets its artifact, whatever it yields.

Window verdict:
- END_TO_END_RF_SUCCESS=NO (zero target captures)
- Valid LoRa packet entries: 3
- CRC OK 240-byte target packets: 0
- All 3 demodulated frames are 23-byte ambient traffic from third-party IoT
  devices (904.1 / 904.5 / 904.7 MHz, SNR -14/-15 dB) — same signature class
  as the ambient frames in the winning 011418Z capture, correctly excluded
  by the extractor's 240-byte size gate. `rx_extract.json` records all 3
  with full per-packet metadata.
- Ambient demodulation itself proves the RX chain was live and hearing the
  band for the full window (first ambient frame ~90 s after arm, last ~18 s
  before close).

RX settings:
- Target frequency: 903.9 MHz (radio A center 904.3 MHz, channel IF -400000 Hz, channel mode 0)
- Spreading factor: SF9, Bandwidth: 125 kHz, single-input mode (-j), clock source 0
- Recovery gate: LORA_CHIRP_RECOVERY_PASS=YES at 2026-09-29T03:59:00Z
  (chip_id PASS: chip version 0x10, EUI 0x0016c001ff18afa3 — second
  consecutive clean start, GPIO17 law holding)

RX command:
`timeout 1800 sudo /home/researcher-bravo/sx1302_hal/libloragw/test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 1`

Expected (not received) payload SHA256:
6f6b11f6c3d64e7bc6519fee583d0531f279fbfc43166c79c8f6bdfde5c6eb3d

Log forensics note (mid-log reset blocks):
The raw log contains 4 reset-shim blocks — 3 before the HAL banner (recovery
gate + restore attempts at arm) plus 1 interleaved mid-log between ambient
packets 2 and 3. Attribution verified against the sudo journal: ZERO
external bus-touching commands (no reset_lgw/chip_id/spi_probe/sshd) ran
during the window. The mid-log block is the HAL tool's own
`./reset_lgw.sh start` invocation interleaving into the shared buffered
stdio pipe (the `-n 1` per-packet session restart path), the same output
class the extractor records as `log_interleaved: true` and the same pattern
present in the winning 011418Z capture (6 blocks / 5 packets) and the June
2026 capture (12 blocks / 6 packets). The running concentrator's count_us
never restarted (packet 3 at 1074524452 us ≈ 17.9 min from arm), proving
no radio state reset occurred mid-window.

Conclusion:
Zero-target window, honestly archived. The radio stack remains certified
(chip_id PASS this tick). Next window arms on RakMiner-A's burst ETA
declaration — coordination continues on Issue #1 / TCP 9877.

— Researcher B (Agent 05, RakMiner-B), 2026-09-29
