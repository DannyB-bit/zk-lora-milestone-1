# groth16_ota cycle-204 — A→B OTA proof exchange evidence

- Cycle: 204 | key: 112 (deposit 100081) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=1248fdb56d5a710d)
- Declared proof SHA-256: `ed5096cec330a0fb961ec7c4323ce2a54cec3a6f75eba1f6bbf76f53e6c0fb0f`
- Window: A1222==B2917 armed 2026-10-26T21:28:52Z closes 2026-10-26T23:28:52Z (declared @2026-10-26T22:50:01Z at the 22:5xZ tick, 2332s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.8..+11.5dB, inter-frame 16.87..16.71s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1223==B2918 → fired @2026-10-26T22:51:21Z, WATCHER HOT-PATH auto-fire on the fully restored lane)
- Battery: PRIMARY VALID 161.2s + controls key-111/key-110 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `61KeQSTSMmDyjpE3hUn4GjN2SUkNXexRpDwryUFTeNBNQPzxYF2nEXEUjBLnxDznnYBSgHzHPABfaPRLobbX1umd` PDA `HvgPsK5Mtq43xb9vgwABC4DfpGUfwEFJGei4RGwmQ6tB` slot 515500272 (devnet), coords [163, 253, 7, 200, 240, 219], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-26T23:28:52Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 22:5xZ tick 2026-10-26 with 2332s remaining; watcher hot-path auto-fire ~80s later — lane fully restored, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle on the prior turn, this PR on the 00:5xZ tick); the prior cycle c-203 landed 2026-10-26T14:04:15Z at PR#128 (fifty-sixth loop) as a ONE-TICK POST-CLOSE landing on the WATCHER hot path; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



