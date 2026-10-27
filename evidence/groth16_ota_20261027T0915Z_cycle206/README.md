# groth16_ota cycle-206 — A→B OTA proof exchange evidence

- Cycle: 206 | key: 114 (deposit 100083) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=12ced8c2a0125f29)
- Declared proof SHA-256: `cad4fd87fc0f25c5a819606c3ee5b14fcab480c26e8adefbc7d19ca345cd091d`
- Window: A1239==B2965 armed 2026-10-27T07:30:34Z closes 2026-10-27T09:30:34Z (declared @2026-10-27T09:14:27Z at the 09:1xZ tick, 969s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.5..+11.5dB, inter-frame 16.7..16.9s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1240==B2967 → fired @2026-10-27T09:15:49Z, WATCHER HOT-PATH auto-fire on the fully lit lane)
- Battery: PRIMARY VALID 160.4s + controls key-113/key-112 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `62WNAZaVBh5MCEMALkpnfUjtrqF2AgUbsQb6cUB5jmRerf7wNuNSPiCk87gQRF7gogQYEBYspribcehLoPpHTMFU` PDA `CPULDLJuSreTFBMGdB8EyWLVLimfqtC4o5JoP8Bjvx5a` slot 515726938 (devnet), coords [24, 211, 90, 142, 175, 168], chain readback PASS
- Extract timing: POST-CLOSE on the intact frozen session segment (c-141/c-155 post-close law — slice banner line 3397 -> first listener exit line 3520; the window closed on schedule 2026-10-27T09:30:34Z rc=124, burst captured in-window)
- Honest ledger: ONE-SPAN POST-CLOSE declare-to-land (declare at the 09:1xZ tick 2026-10-27 with 969s remaining inside the 07:30-09:30 window; watcher hot-path auto-fire ~80s later — lane fully lit, cache warm; burst captured in-window; window closed on schedule; extract post-close on the frozen segment; battery + settle completed @2026-10-27T14:1x..14:4xZ this tick, this PR riding the 14:4xZ tick); the prior cycle c-205 landed 2026-10-27T05:5xZ at PR#130 (fifty-eighth loop, TX 4YHPkpL1 slot 515591684) as a ONE-TICK POST-CLOSE landing on the WATCHER hot path; the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; the keys 115/116 ask rides this tick (key-115 remains warm from the 30th refill pair); no cycle missed since; last owned miss remains c-145 (closed on the record)
