# groth16_ota cycle-155 — A→B OTA proof exchange evidence

- Cycle: 155 | key: 96 (deposit 100065) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=8b5826a36bbfa60a)
- Declared proof SHA-256: `370c9edd44fce6d178c6963ac27d06b4bcb59e512c89a3e801aa5678baf78005`
- Window: A1099==B2584 armed 2026-10-21T08:08:00Z closes 2026-10-21T10:08:00Z (declared @2026-10-21T09:04:31Z at the 09:0xZ tick, 3813s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.2..+11.5dB, inter-frame 16.79..16.78s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1100==B2586 → fired @2026-10-21T09:05:51Z)
- Battery: PRIMARY VALID 159.6s + controls key-95/key-94 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `6WgFr9qz1EmqbGZRjcUD6vMiCnUH94EUw3KmxbjcNuF23UZneFedtxnvPD26Tm39QCSZ7U2LFxZ2otsK3bdhp1o` PDA `4nLWkBXnWAQDTdV6LEUZGKfqHN6dkQ2834HUQ3ZX44Re` slot 513499297 (devnet), coords [178, 155, 77, 222, 210, 243], chain readback PASS
- Extract timing: POST-CLOSE on the CLOSED session segment (post-close slice law — the window closed on schedule rc=124 with the burst captured in-window; slice banner->first 'listener exit rc=124' line)
- Honest ledger: TWO-TICK declare-to-land (declare at the 09:0xZ tick with 3813s remaining; fire ~80s later; burst captured in-window; window closed on schedule rc=124; extract/battery/settle/PR landed THIS tick POST-CLOSE on the closed session segment); the prior cycle c-154 was one-tick (declare at its tick START, landed same tick — PR#119, forty-seventh loop); no cycle missed since; last owned miss remains c-145 (closed on the record)


