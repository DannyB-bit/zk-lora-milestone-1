# groth16_ota cycle-147 — A→B OTA proof exchange evidence

- Cycle: 147 | key: 88 (deposit 100057) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=e3f09e21bb29b00a)
- Declared proof SHA-256: `840d64b8e2c93c6165eb249adc4297f3b540678f58d923593482dc9b5ec67f8c`
- Window: A1025==B2457 armed 2026-10-20T14:04:59Z closes 2026-10-20T16:04:59Z (early declare at tick START, 3046s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.8..+12.0dB, inter-frame 16.78..16.74s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1026==B2459 → fired @2026-10-20T15:15:36Z)
- Battery: PRIMARY VALID 159.4s + controls key-87/key-86 VALID, BATTERY_EXIT=0 attempt1
- Settle: TX `2NKepgFL5kBGCEK2Ab9d5kezgLCHTyAn1cikd5W9uCJC47vHcHfX9uuc3CuoqjeGXpLx6DMihryd1BDmjra7CSaQ` PDA `HBuWWUVz9CE2sqbUZvzxgvJo7qHfqb3rJcZm9943DHF5` slot 513210984 (devnet), coords [139, 186, 111, 12, 222, 95], chain readback PASS
- Extract timing: MID-WINDOW on the live session segment (genuine mid-window, c-117 law — listener still held the bus; window closes 2026-10-20T16:04:59Z)
- Honest ledger: one-tick loop (declare at tick START — the c-146 early-declare fix repeated); c-146's window closed on schedule with its fire captured + settled; no cycle missed since; last owned miss remains c-145 (closed on the record)



