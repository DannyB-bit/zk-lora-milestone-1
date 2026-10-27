# groth16_ota cycle-205 — A→B OTA proof exchange evidence

- Cycle: 204 | key: 113 (deposit 100082) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=cde72ed72e023025)
- Declared proof SHA-256: `45d8b926ec1d47d5914589c74d2f815bbfd17edb4510a894b00304e27b921985`
- Window: A1230==B2937 armed 2026-10-27T01:29:33Z closes 2026-10-27T03:29:33Z (declared @2026-10-27T02:39:36Z at the 02:3xZ tick, 3003s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.5..+11.2dB, inter-frame 16.74..16.72s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1231==B2939 → fired @2026-10-27T02:40:56Z, WATCHER HOT-PATH auto-fire on the fully restored lane)
- Battery: PRIMARY VALID 161.0s + controls key-112/key-111 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `4YHPkpL1EeHmKA4xLwH3Cc844iX1Xzj5fAhYkQo3pRZnQgxMLku4fj9ze47S8ZntQSJCjDK9fxVDw7SMfbrYnr5c` PDA `2GBSpKKnyuHCwXZHQfuJfTbVvPvidY7dTcZ4iQBWyx8i` slot 515591684 (devnet), coords [151, 218, 27, 29, 195, 139], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-27T03:29:33Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 02:3xZ tick 2026-10-27 with 3003s remaining; watcher hot-path auto-fire ~80s later — lane fully restored, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle on the prior turn, this PR on the 04:0xZ tick); the prior cycle c-204 landed 2026-10-27T02:3xZ at PR#129 (fifty-seventh loop) as a ONE-TICK POST-CLOSE landing on the WATCHER hot path; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



