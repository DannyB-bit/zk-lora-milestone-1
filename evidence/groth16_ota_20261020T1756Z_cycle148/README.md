# groth16_ota cycle-148 — A→B OTA proof exchange evidence

- Cycle: 148 | key: 89 (deposit 100058) | statement class: FIRST-OF-CLASS (positively asserted) (pih[-1]=353206ab9f3e6e2a)
- Declared proof SHA-256: `563402ca6a74d7cb5ce74a22d86506fd27743a74f9b7fd3b6c346dfa7cd93912`
- Window: A1035==B2475 armed 2026-10-20T16:05:19Z closes 2026-10-20T18:05:19Z (declared MID-TICK @2026-10-20T17:55:05Z, 615s remaining)
- Burst: 5/5 CRC-OK 128B @903.9MHz SF9, SNR +11.8..+12.2dB, inter-frame 16.74..16.9s, POST-WRAP (+4294.967296s) (battery-selected)
- Declare→fire ~80s (A1036==B2477 → fired @2026-10-20T17:56:25Z)
- Battery: PRIMARY VALID 159.7s + controls key-88/key-87 VALID, BATTERY_EXIT=0 attempt1
- Settle: TX `2FViCDKufQC68HVhjESnkoeJhzynvipJKuUQqFuAwUjHM5LAUZbbACBHaNZYf6dDsHcuKzEd3asTkkmE5io55M2c` PDA `5uaHUy5y2Nwc8ZCBjFRAqUcLda9zsA5WdRnNfGyst7Bs` slot 513273189 (devnet), coords [139, 131, 189, 190, 152, 130], chain readback PASS
- Extract timing: POST-CLOSE on the bounded session segment (window closed on schedule rc=124, supervisor rotated; slice banner→first-exit, c-141 law)
- Honest ledger: TWO-TICK loop (declare+fire in the prior 17:55Z tick at 615s remaining — the wall-clock-lag class, owned; extract/settle/PR in the post-close tick); the c-147 window closed on schedule with its fire captured + settled one-tick; no cycle missed since; last owned miss remains c-145 (closed on the record)



