# groth16_ota cycle-152 — A→B OTA proof exchange evidence

- Cycle: 152 | key: 93 (deposit 100062) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=bb69f2eabeea8f00)
- Declared proof SHA-256: `53c77956633364d08d7d31d624276ebb81f841d238ad8d5bcd42ad23be6ed302`
- Window: A1073==B2538 armed 2026-10-21T02:07:00Z closes 2026-10-21T04:07:00Z (declared at THIS TICK START @2026-10-21T03:15:00Z, 3122s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.8..+11.0dB, inter-frame 16.72..16.78s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1074==B2540 → fired @2026-10-21T03:16:20Z)
- Battery: PRIMARY VALID 160.2s + controls key-92/key-91 VALID, BATTERY_EXIT=0 attempt2 (attempt1 killed mid-verify by a 60s tool-timeout cap — honest no-verdict note kept, c-100 law)
- Settle: TX `2jiU7iwxePxKWqT8yiiUrbVnsRfsu9emY7XSoErb2Sz5r2Y4vsd4k87CprCbLk3z1aeRkJForB7sAx4BXqzAtLKe` PDA `G7GqBPXu9pHtpSLgLE8ANnqeuxzAEUZKLsdSTPHS5SNc` slot 513388461 (devnet), coords [8, 49, 70, 103, 12, 214], chain readback PASS
- Extract timing: PRE-CLOSE on the live session segment (c-117 extract-before-close law — listener still held the bus)
- Honest ledger: ONE-TICK declare-to-land (declare at THIS tick START with 3122s remaining; fire ~80s later; extract/battery/settle/PR landed THIS tick pre-close); the prior cycle c-151 was two-tick (declare at its tick START, landed pre-close on the following tick — PR#116, forty-fourth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)

