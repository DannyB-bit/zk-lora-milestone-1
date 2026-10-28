# groth16_ota cycle-207 — A→B OTA proof exchange evidence

- Cycle: 207 | key: 115 (deposit 100084) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=c9fe09198712d924)
- Declared proof SHA-256: `3a566df806ded97a082f501d3620b4fd6027d22e2b27c5e80a0ee0134f89e297`
- Window: A1249==B3005 armed 2026-10-27T17:32:15Z closes 2026-10-27T19:32:15Z (declared @2026-10-27T19:24:58Z at the 19:2xZ tick, 441s remaining — LATE DECLARE disclosed, c-145 lesson)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.8..+12.0dB, inter-frame 16.75..16.71s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1250==B3006 → fired @2026-10-27T19:26:17Z, WATCHER HOT-PATH auto-fire on the fully lit lane)
- Battery: PRIMARY VALID 160.9s + controls key-114/key-113 VALID, BATTERY_EXIT=0 attempt2 carried the verdict (on-disk attempt series: t12_cycle207_battery_attempt1.log, t12_cycle207_battery_attempt2.log — attempt1 pre-silicon abort disclosed by its own log, never re-numbered away)
- Settle: TX `5F3tT3sNDV653PgrYQJdzDLJfiFLhk4qgWn3tBtDmLCnVKZAteAuCV8wHTDjszstxkPFsb6zRSnvzkmYfN4XrcR5` PDA `H2y5bhnEtGeGqAkpUpqB31ZZPex8ZRi1D4ebiLy2hZo` slot 515821676 (devnet), coords [117, 7, 243, 159, 139, 203], chain readback PASS
- Landing timing: SAME-TICK POST-CLOSE — burst captured IN-WINDOW; ALL landing stages post-close on the intact frozen session segment (c-141/c-155 post-close law — slice banner 3868 -> first listener exit line 3976; the window closed on schedule 2026-10-27T19:32:15Z rc=124)
- Honest ledger: SAME-TICK POST-CLOSE declare-to-land (declare at the 19:2xZ tick 2026-10-27 with 441s remaining — late declare owned; watcher hot-path auto-fire ~80s later; burst captured in-window; window closed on schedule; extract+bundle+battery+settle+PR post-close within the same tick); attempt1 pre-silicon abort (control-scan root misresolution) disclosed by its own log; launcher-bypass c-142 recovery disclosed; the prior cycle c-206 landed 2026-10-27T16:2xZ at PR#131 (fifty-ninth loop / BUS 43rd, TX 62WNAZaV); the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



