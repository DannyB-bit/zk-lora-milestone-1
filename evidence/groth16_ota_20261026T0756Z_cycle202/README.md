# groth16_ota cycle-202 — A→B OTA proof exchange evidence

- Cycle: 202 | key: 110 (deposit 100079) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=429c9597ba1a2930)
- Declared proof SHA-256: `18a652b609ae9323c7eadbbf4a49efe1597fce71267454ef84f50423fb253251`
- Window: A1203==B2853 armed 2026-10-26T07:26:31Z closes 2026-10-26T09:26:31Z (declared @2026-10-26T07:54:49Z at the 07:5xZ tick, 5503s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.0..+11.2dB, inter-frame 16.78..16.76s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1204==B2854 → fired @2026-10-26T07:56:09Z, WATCHER HOT-PATH auto-fire on the fully restored lane)
- Battery: PRIMARY VALID 161.2s + controls key-109/key-108 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `45SgAkgSNZjJCrLJC5qqEu4Hbxhn7UES2yqHY82NvtBiL5vGxE22dhtBJUdwJWuxQWB8Vhh7wbuktiGwP2mBynxW` PDA `8nb5Mxuz9eCF2ykGeJ3s2LNGxGN7nUtj1bW7rXvNYCjB` slot 515324139 (devnet), coords [98, 22, 108, 91, 72, 236], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-26T09:26:31Z rc=124, burst captured in-window)
- Honest ledger: ONE-TICK POST-CLOSE declare-to-land (declare at the 07:5xZ tick 2026-10-26 with 5503s remaining; watcher hot-path auto-fire ~80s later — lane fully restored, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle + this PR same tick); the prior cycle c-201 landed 2026-10-26T04:35:2xZ at PR#126 (fifty-fourth loop) as a ONE-TICK POST-CLOSE landing on the WATCHER hot path; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



