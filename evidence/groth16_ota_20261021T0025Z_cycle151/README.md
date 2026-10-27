# groth16_ota cycle-151 — A→B OTA proof exchange evidence

- Cycle: 151 | key: 92 (deposit 100061) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=d9db52723427892e)
- Declared proof SHA-256: `d9196a209f1160ade4b3e90437e72f9be69836a2035ed0d066a91a7f94bdcd3a`
- Window: A1063==B2519 armed 2026-10-21T00:06:39Z closes 2026-10-21T02:06:39Z (declared at the PRIOR TICK START @2026-10-21T00:23:47Z, 6174s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.8..+12.0dB, inter-frame 16.74..16.73s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1064==B2520 → fired @2026-10-21T00:25:06Z)
- Battery: PRIMARY VALID 162.1s + controls key-91/key-90 VALID, BATTERY_EXIT=0 attempt1
- Settle: TX `4dC117YVJUoYavEcuB4qt3SDbxDNVqGfCDesUoBp6erBUGsAcJwbHXGG6G1DdPoy3EL7G3R7wa24nzxdd8hwXPUA` PDA `HcVVwwuCoRNrfTPibV5idsX5PmpweJiEtxoqBSqAv72Y` slot 513362353 (devnet), coords [58, 222, 131, 158, 84, 52], chain readback PASS
- Extract timing: PRE-CLOSE on the live session segment (c-117 extract-before-close law — listener still held the bus)
- Honest ledger: TWO-TICK declare-to-land (declare at the PRIOR tick START with 6174s remaining; fire ~79s later; extract/battery/settle/PR landed THIS tick pre-close); the prior cycle c-150 was one-tick (declare at tick START, same-tick landing); no cycle missed since; last owned miss remains c-145 (closed on the record)



