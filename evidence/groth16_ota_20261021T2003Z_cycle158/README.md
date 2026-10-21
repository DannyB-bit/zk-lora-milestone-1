# groth16_ota cycle-158 — A→B OTA proof exchange evidence

- Cycle: 158 | key: 99 (deposit 100068) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=0bd02badffd03b0c)
- Declared proof SHA-256: `f2c9f8f52fd19615471157198f5ba0d2b04ac14e81d026b68d5a8937deae9aa8`
- Window: A1126==B2645 armed 2026-10-21T18:09:42Z closes 2026-10-21T20:09:42Z (declared @2026-10-21T20:02:10Z at the 20:0xZ tick, 456s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.2..+11.8dB, inter-frame 16.73..16.93s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1127==B2647 → fired @2026-10-21T20:03:29Z)
- Battery: PRIMARY VALID 160.0s + controls key-98/key-97 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `24YFNv8Ebagpe7iEwsmR2PcFx6cdSe3XzH5KarjcLSWZNTUTZtnf6nLFe23PyeKycoyPwkeesxYoQHbX9X6qZroH` PDA `FZ6BJWKTPtHoC5c9EAxSYs4FCatzrLtwxhj1dtphdu6Z` slot 513649898 (devnet), coords [145, 225, 35, 97, 228, 246], chain readback PASS
- Extract timing: POST-CLOSE on the CLOSED session segment (post-close slice law — the window closed on schedule rc=124 with the burst captured in-window; slice banner->first 'listener exit rc=124' line)
- Honest ledger: TWO-TICK declare-to-land (declare at the 20:0xZ tick with 456s remaining; fire ~80s later; burst captured in-window; window closed on schedule rc=124; extract/battery/settle/PR landed THIS tick POST-CLOSE on the closed session segment); the prior cycle c-157 was also two-tick (declare at the 16:2xZ tick, landed post-close at the 20:0xZ tick — PR#122, fiftieth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)



