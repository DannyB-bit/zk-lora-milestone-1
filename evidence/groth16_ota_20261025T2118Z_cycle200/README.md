# groth16_ota cycle-200 — A→B OTA proof exchange evidence

- Cycle: 200 | key: 108 (deposit 100077) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=bb387be19bc32c1f)
- Declared proof SHA-256: `21f39d4e6dc8437fceee77ea90eb039cea234c19c9fbe4bc3f5cf33b4f555bb9`
- Window: A1181==B2798 armed 2026-10-25T19:24:21Z closes 2026-10-25T21:24:21Z (declared @2026-10-25T21:16:41Z at the 20:3xZ tick, 3074s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.8..+11.2dB, inter-frame 16.81..16.72s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1184==B2803 → fired @2026-10-25T21:18:01Z, AGENT-LANE manual prove+fire on the RELIT lane)
- Battery: PRIMARY VALID 160.5s + controls key-100/key-99 VALID, BATTERY_EXIT=0 attempt4 first verdict (attempt1 missing binary, attempt2 killed 0-byte, attempt3 aborted fail-closed on the control-class gate — cycle-158 payload bin vendored byte-exact from committed evidence, sha-verified)
- Settle: TX `bvsTAws9y2QTaCf82VG978GTiZXxLyWam73YaeNtkqgg8BX7EfYKbebKAagYVY3vfioVLK4f3sfZ2ZJdpeqx2Zk` PDA `3bg324GGZrjG1vKsdVueWBroheUAjy1TbTqPnDYh3vGn` slot 515164756 (devnet), coords [77, 101, 109, 104, 118, 238], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-25T21:24:21Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 20:3xZ tick 2026-10-25 with 3074s remaining; agent-lane manual prove+fire ~80s later — lane relit via peer-run wake after ~4 days dark; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle + this PR same tick); the prior cycle c-159 was TWO-TICK POST-CLOSE (landed 2026-10-25T19:11:34Z at PR#124, thirty-sixth loop) after Alpha's ~70h dark turn; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



