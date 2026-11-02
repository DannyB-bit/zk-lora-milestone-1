# groth16_ota cycle-208 — A→B OTA proof exchange evidence

- Cycle: 207 | key: 116 (deposit 100085) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=09894bd45c626902)
- Declared proof SHA-256: `fae1e3b8baec67e4ca863448840f43c35bad16471c97efbde2a49ee7c4db871f`
- Window: A1261==B3034 armed 2026-10-27T23:33:16Z closes 2026-10-28T01:33:16Z (declared @2026-10-28T01:13:01Z at the 19:2xZ tick, 1218s remaining — LATE DECLARE disclosed, c-145 lesson)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.5..+11.2dB, inter-frame 16.71..16.75s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1262==B3036 → fired @2026-10-28T01:14:20Z, WATCHER HOT-PATH auto-fire on the fully lit lane)
- Battery: PRIMARY VALID 161.1s + controls key-115/key-114 VALID, BATTERY_EXIT=0 attempt1 FIRST VERDICT
- Settle: TX `5FWjNMuHcCArpKUMQLBpseKWXMAH2h7mPAHC8cRUQVmpBgHBZ5BXT45nfGJiCGrdX4hh3cf3DpUfoLsbNinfpSTF` PDA `HrPydgZzcHT2rqDRJziiqmoxedMwjLsikdZd2JvV2Emr` slot 515895424 (devnet), coords [98, 117, 177, 78, 143, 60], chain readback PASS
- Landing timing: SAME-TICK POST-CLOSE — burst captured IN-WINDOW; ALL landing stages post-close on the intact frozen session segment (c-141/c-155 post-close law — slice banner 3868 -> first listener exit line 3976; the window closed on schedule 2026-10-28T01:33:16Z rc=124)
- Honest ledger: SAME-TICK POST-CLOSE declare-to-land (declare at the 19:2xZ tick 2026-10-27 with 1218s remaining — late declare owned; watcher hot-path auto-fire ~80s later; burst captured in-window; window closed on schedule; extract+bundle+battery+settle+PR post-close within the same tick); attempt1 pre-silicon abort (control-scan root misresolution) disclosed by its own log; launcher-bypass c-142 recovery disclosed; the prior cycle c-206 landed 2026-10-27T16:2xZ at PR#131 (fifty-ninth loop / BUS 43rd, TX 5F3tT3sN); the 35 catch-up frames (keys 101..107, cycles 193..199) remain awaiting landing batteries; no cycle missed since; last owned miss remains c-145 (closed on the record)



