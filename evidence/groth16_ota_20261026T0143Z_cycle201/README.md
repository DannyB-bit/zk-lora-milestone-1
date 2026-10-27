# groth16_ota cycle-201 — A→B OTA proof exchange evidence

- Cycle: 201 | key: 109 (deposit 100078) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=a6d3454459609e02)
- Declared proof SHA-256: `4748bf70b33130e141dd76b989469fdb40f89dc0ead71304be09a7ca9cfe2e28`
- Window: A1193==B2825 armed 2026-10-26T01:25:30Z closes 2026-10-26T03:25:30Z (declared @2026-10-26T01:42:27Z at the 01:4xZ tick, 6186s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.0..+12.2dB, inter-frame 16.85..16.8s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1194==B2827 → fired @2026-10-26T01:43:47Z, WATCHER HOT-PATH auto-fire on the fully restored lane)
- Battery: PRIMARY VALID 160.3s + controls key-108/key-100 VALID, BATTERY_EXIT=0 attempt2 carried the verdict (on-disk attempt series: t12_cycle201_battery_attempt1.log, t12_cycle201_battery_attempt2.log — earlier attempts disclosed by their own logs, never re-numbered away)
- Settle: TX `4pj6Qtef4imUGepGzn5hmnUs2t72VRvq5JKW6yofFypuxBLt6otaAe7wjMav5RJrazEaBoaN3Gmtbide7zmFJ2xX` PDA `DFH13wn7EDTYuSZ7Y6tt9Pu6NerEta7qnsD7CuaBnZVo` slot 515212784 (devnet), coords [100, 55, 7, 109, 159, 64], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-26T03:25:30Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 01:4xZ tick 2026-10-26 with 6186s remaining; watcher hot-path auto-fire ~80s later — lane fully restored, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle + this PR same tick); the prior cycle c-200 landed 2026-10-26T01:41:5xZ at PR#125 (fifty-third loop) as a ONE-TICK POST-CLOSE landing on the RELIT agent lane; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



