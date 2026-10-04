# Canon VK custody-closure rerun — 2026-10-04T23:45Z — Dan's PR#13/#14 review custody note CLOSED with executed bytes

Dan's 22:08Z execution reviews of record merged PR#13 + PR#14 (and cuneiform-m1 PR#9) with one
open custody note: the arkworks pairing leg runs on the `zk-lorawan` checkout whose canon VK
(`7bd5683f…`) his PAT cannot read (`zk-lorawan` 404 from his seat), so he verified the pairing
as "committed-log report, structurally corroborated" — not as an independently rerun computation.

This directory closes that gap from the RX seat: **both merged payloads re-verified live, from
the merged-main artifacts, in one fresh session**, using the exact committed reproduction recipe
(PR#14 README `## Reproduce`, identical public-input vector, gateway, deposit, firmware).

## Executed battery (RakMiner-B, ARM Cortex-A72, arkworks BN254, 2026-10-04T23:45Z)
- **PRIMARY — PR#14 `bd4c9ab2…`** (`evidence/groth16_ota_20261004T1922Z/rx_payload.bin` at main
  `b3851a0`): `zk_lorawan_prove verify` → **VALID, exit 0, 142.0 s** — the full-PK canon-disk
  path (a ~6 s return would indicate the in-memory seed-42 regen path; none observed).
- **CONTROL — PR#13 `fc816080…`** (`evidence/groth16_ota_20261004T1124Z/rx_payload.bin`):
  **VALID, exit 0, 142.0 s** — same session/binary/VK/keys.
- **Keys sha-guard**: VK `7bd5683f13f35847…`, PK `8dda8b798458bb5b…` — byte-identical before and
  after the battery. `ZK_LORAWAN_REPRODUCIBLE_SETUP` UNSET (canon disk keys).
- **Payload SHA recompute before verify**: both `.bin` files re-hashed from the merged-main
  checkout — `bd4c9ab27d19…788b` and `fc8160800267…7261`, exact match to declared + on-chain
  settled session strings.

Result: the pairing legs of PR#13 and PR#14 are now **independently rerun, not just corroborated**.
Every leg of both drills — radio capture, SHA match, Groth16 pairing, devnet settle — is verified
live from at least one seat other than the originating agent.

## Files
- `rerun_pr14_primary_bd4c9ab2.log` — fresh verify transcript (VALID, exit 0, 142.0 s)
- `rerun_pr13_control_fc816080.log` — fresh control verify (VALID, exit 0, 142.0 s)
- `rerun_summary.txt` — KEY=VALUE record: key shas, elapsed times, sha-guard result

## Reproduce
Identical to the PR#14 README `## Reproduce` block, against `main` @ `b3851a0` artifacts.
