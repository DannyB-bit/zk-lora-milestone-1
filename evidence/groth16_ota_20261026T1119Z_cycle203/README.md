# groth16_ota cycle-203 — A→B OTA proof exchange evidence

- Cycle: 202 | key: 111 (deposit 100080) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=2f8be73fbf95302f)
- Declared proof SHA-256: `cd5d7ac74e4b0884800ee02c6d9275b350f428f27eb66dbb808c42eaca2bff6f`
- Window: A1207==B2868 armed 2026-10-26T09:26:51Z closes 2026-10-26T11:26:51Z (declared @2026-10-26T11:18:09Z at the 11:1xZ tick, 524s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.0..+11.2dB, inter-frame 16.9..16.72s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1208==B2869 → fired @2026-10-26T11:19:29Z, WATCHER HOT-PATH auto-fire on the fully restored lane)
- Battery: PRIMARY VALID 161.6s + controls key-110/key-109 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `3m8LFaApKw5ZV6ibN4KVgCRSHYv16v1nuFRayA67W45MjnXpmxu5WXog1QdnGLxzWNtu7og85KCCsiQ6An4u84HB` PDA `AvSyPKGWhKYKZpznTFnz3jQMcciSLDJ7wBFEWQGT9vyp` slot 515334361 (devnet), coords [254, 7, 254, 242, 160, 249], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-26T11:26:51Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 11:1xZ tick 2026-10-26 with 524s remaining; watcher hot-path auto-fire ~80s later — lane fully restored, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle + this PR same tick); the prior cycle c-202 landed 2026-10-26T13:1xZ at PR#127 (fifty-fifth loop) as a ONE-TICK POST-CLOSE landing on the WATCHER hot path; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



