# groth16_ota cycle-157 — A→B OTA proof exchange evidence

- Cycle: 157 | key: 98 (deposit 100067) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=306a4bc239023019)
- Declared proof SHA-256: `a6d1ccb0727297a302db64e7f81c0b7b9d9e35af5481d9fa859e602ee74320a7`
- Window: A1112==B2620 armed 2026-10-21T16:09:21Z closes 2026-10-21T18:09:21Z (declared @2026-10-21T16:28:48Z at the 16:2xZ tick, 6033s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.5..+11.8dB, inter-frame 16.72..16.8s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1113==B2621 → fired @2026-10-21T16:30:08Z)
- Battery: PRIMARY VALID 159.9s + controls key-97/key-96 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `brcmmzb3YmUrcvb6WrtRD8gG5iPeThRiBpEWxbco7Qxo76k9RxQMVnj9UUPony24AQWvto1TayUZnFxNirp26uD` PDA `3Tys7Lm2izw1cdVeEp4oUMPwrANY3FzHMrWVWP5CDJBb` slot 513616523 (devnet), coords [245, 220, 114, 128, 215, 178], chain readback PASS
- Extract timing: POST-CLOSE on the CLOSED session segment (post-close slice law — the window closed on schedule rc=124 with the burst captured in-window; slice banner->first 'listener exit rc=124' line)
- Honest ledger: TWO-TICK declare-to-land (declare at the 16:2xZ tick with 6033s remaining; fire ~80s later; burst captured in-window; window closed on schedule rc=124; extract/battery/settle/PR landed THIS tick POST-CLOSE on the closed session segment); the prior cycle c-156 was also two-tick (declare at the 12:1xZ tick, landed post-close at the 16:2xZ tick — PR#121, forty-ninth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)



