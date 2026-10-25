# groth16_ota cycle-159 — A→B OTA proof exchange evidence

- Cycle: 159 | key: 100 (deposit 100069) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=40e84b65f51ddb0e)
- Declared proof SHA-256: `f3bcc835e23cc95e2298c52fc348279b915998d0f0351db14ecd03f4706aa984`
- Window: A1134==B2660 armed 2026-10-21T22:10:22Z closes 2026-10-22T00:10:22Z (declared @2026-10-21T22:15:02Z at the 22:1xZ tick, 6921s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.5..+11.8dB, inter-frame 16.71..16.71s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1135==B2661 → fired @2026-10-21T22:16:21Z)
- Battery: PRIMARY VALID 160.2s + controls key-99/key-98 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `23emmMHS5MxHVnXbeMznfXyU1L1W1yrh1pNqPSq6UfLuatoUqLMiwaqoEb61bF3qmNEW2WEX1cPK92dgik3VQf9C` PDA `8CnrzdeWgxAw7V4V29jbUyetwUeXSmTa6ybqtEcR9h84` slot 515064096 (devnet), coords [94, 191, 243, 253, 76, 253], chain readback PASS
- Extract timing: POST-CLOSE on 2026-10-25 on the intact frozen session segment (c-141/c-155 post-close law — slice banner->first listener exit line; the window closed on schedule 2026-10-22T00:10:22Z rc=124, burst captured in-window)
- Honest ledger: TWO-TICK POST-CLOSE declare-to-land (declare at the 22:1xZ tick 2026-10-21 with 6921s remaining; fire ~80s later; burst captured in-window; battery ran that night; landing stalled on Alpha's ~70h dark turn; extract ran 2026-10-25 post-close on the intact frozen session segment — c-141/c-155 post-close law; settle + this PR complete the landing); the prior cycle c-158 was also two-tick (declare at the 20:0xZ tick, landed post-close at the 22:1xZ tick — PR#123, fifty-first loop); no cycle missed since; last owned miss remains c-145 (closed on the record)



