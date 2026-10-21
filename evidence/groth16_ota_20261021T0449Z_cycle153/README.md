# groth16_ota cycle-153 — A→B OTA proof exchange evidence

- Cycle: 153 | key: 94 (deposit 100063) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=445a5e7f0e79b52c)
- Declared proof SHA-256: `2d932df06a5d8987eb4a0798ed109373fd22216eb67d2303aec34788af675af7`
- Window: A1082==B2553 armed 2026-10-21T04:07:20Z closes 2026-10-21T06:07:20Z (declared at THIS TICK START @2026-10-21T04:47:43Z, 4779s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.5..+11.0dB, inter-frame 16.78..16.76s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1083==B2555 → fired @2026-10-21T04:49:02Z)
- Battery: PRIMARY VALID 159.6s + controls key-93/key-92 VALID, BATTERY_EXIT=0 attempt2 (attempt1 aborted fail-closed pre-silicon on an A-bus incomplete-fetch race — honest no-verdict note kept, c-100 law)
- Settle: TX `4QuB8bB48L9DEF7g8rwRzm2xemg38XhVdfCwjJcctMkY5hPjfoptbcW2ifYSQXgRuQaQi6Ua5DgcDAuP5HzUzR2r` PDA `8eFNmeydVmrJCsjhwt958eZ9oWsGcgWGCZS8e1AmPKY6` slot 513413477 (devnet), coords [55, 21, 195, 32, 235, 5], chain readback PASS
- Extract timing: PRE-CLOSE on the live session segment (c-117 extract-before-close law — listener still held the bus)
- Honest ledger: ONE-TICK declare-to-land (declare at THIS tick START with 4779s remaining; fire ~80s later; extract/battery/settle/PR landed THIS tick pre-close); the prior cycle c-152 was one-tick (declare at its tick START, landed same tick — PR#117, forty-fifth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)


