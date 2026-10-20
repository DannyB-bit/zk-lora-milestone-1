# groth16_ota cycle-149 — A→B OTA proof exchange evidence

- Cycle: 149 | key: 90 (deposit 100059) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=f0e19dd1c5ec2e11)
- Declared proof SHA-256: `102a0f366c2078df3b1d247d8e3887d0b7b433e12599cc7baf7730d1ab39aa95`
- Window: A1035==B2475 armed 2026-10-20T18:05:39Z closes 2026-10-20T20:05:39Z (declared AT TICK START @2026-10-20T19:38:11Z, 1652s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.8..+11.8dB, inter-frame 16.74..16.72s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1039==B2486 → fired @2026-10-20T19:39:31Z)
- Battery: PRIMARY VALID 160.3s + controls key-89/key-88 VALID, BATTERY_EXIT=0 attempt1
- Settle: TX `5exteEdUbb2NAQLNiDeHDkicvVDVZR2dbrx3teuN94tvCphS7FtYQJnVeaPLsAcUj5nzqEtKdL59C6Ap2nVB829Q` PDA `B7DKMScoUtCYryooBHbHMwXAF3fM1u5wDtxMis9o1fjZ` slot 513277480 (devnet), coords [10, 222, 72, 7, 21, 135], chain readback PASS
- Extract timing: PRE-CLOSE on the live session segment (c-117 extract-before-close law — listener still held the bus)
- Honest ledger: ONE-TICK loop (declare at tick START with 1652s remaining; full loop landed this tick); the prior cycle was two-tick (mid-tick declare, wall-clock-lag class, owned in its own ledger); no cycle missed since; last owned miss remains c-145 (closed on the record)



