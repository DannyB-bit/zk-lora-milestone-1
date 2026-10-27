# groth16_ota cycle-156 — A→B OTA proof exchange evidence

- Cycle: 156 | key: 97 (deposit 100066) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=5b99f550d1e5831f)
- Declared proof SHA-256: `b2b3139fafeb6e2eb65dcf2c8a2eeb7c99f0bfa6d8d44d0c31549b4eecc3ca5b`
- Window: A1108==B2603 armed 2026-10-21T12:08:41Z closes 2026-10-21T14:08:41Z (declared @2026-10-21T12:14:49Z at the 12:1xZ tick, 6833s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +10.8..+11.8dB, inter-frame 16.71..16.74s, pre-wrap (+0s) (battery-selected)
- Declare→fire ~80s (A1109==B2604 → fired @2026-10-21T12:16:08Z)
- Battery: PRIMARY VALID 160.0s + controls key-96/key-95 VALID, BATTERY_EXIT=0 attempt1 first try (no dual-bus posts during the battery's run window this tick)
- Settle: TX `5kWMa2NV5A7HkjKvNVvP5HXha44SWQRgSJQhkmPh5gcnM4EPzr9QjPXdu4x3iVQbA7EhW1tvy9CcNTS7Tu2sC55Q` PDA `GNbWKZksaHRkKspfGCfruyiZECNT54oABSAd6As6FvML` slot 513584332 (devnet), coords [22, 201, 232, 130, 215, 37], chain readback PASS
- Extract timing: POST-CLOSE on the CLOSED session segment (post-close slice law — the window closed on schedule rc=124 with the burst captured in-window; slice banner->first 'listener exit rc=124' line)
- Honest ledger: TWO-TICK declare-to-land (declare at the 12:1xZ tick with 6833s remaining; fire ~80s later; burst captured in-window; window closed on schedule rc=124; extract/battery/settle/PR landed THIS tick POST-CLOSE on the closed session segment); the prior cycle c-155 was one-tick (declare at its tick START, landed same tick — PR#120, forty-eighth loop); no cycle missed since; last owned miss remains c-145 (closed on the record)


