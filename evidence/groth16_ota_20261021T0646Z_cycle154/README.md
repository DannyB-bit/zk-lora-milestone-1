# groth16_ota cycle-154 — A→B OTA proof exchange evidence

- Cycle: 153 | key: 95 (deposit 100064) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=cb6148890a495905)
- Declared proof SHA-256: `6df80d0d3e69b9e30d5b3b5cef6c30e1f91ee9fd3b6a5ad2dcd4cc226a58a673`
- Window: A1091==B2568 armed 2026-10-21T06:07:40Z closes 2026-10-21T08:07:40Z (declared at THIS TICK START @2026-10-21T06:45:23Z, 4939s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.2..+11.0dB, inter-frame 16.78..16.79s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1092==B2569 → fired @2026-10-21T06:46:43Z)
- Battery: PRIMARY VALID 160.0s + controls key-94/key-93 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `2y8rnCUKR4w8zueXrBEHfsvzBbZiRnugkPGDtECyjL1iBCK3UkfpSj13hDUpwxHqv3GuVSDpC9trptkbiCSmwfMY` PDA `EKY8K7DdFPVBH9wmid2ZbeAekWCHrWVCjdk4Fhw6mRsd` slot 513452339 (devnet), coords [108, 218, 139, 224, 9, 192], chain readback PASS
- Extract timing: PRE-CLOSE on the live session segment (c-117 extract-before-close law — listener still held the bus)
- Honest ledger: ONE-TICK declare-to-land (declare at THIS tick START with 4939s remaining; fire ~80s later; extract/battery/settle/PR landed THIS tick pre-close); the prior cycle c-153 was one-tick (declare at its tick START, landed same tick — PR#118, forty-sixth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)


