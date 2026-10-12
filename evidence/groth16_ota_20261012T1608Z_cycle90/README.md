# groth16_ota cycle-90 — COMPLETE VALID A→B (14th consecutive), 82s declare-to-fire

**Cycle:** 90 · **Drill:** groth16_ota (128 B Groth16/BN254 proof OTA)
**Verdict:** COMPLETE VALID — radio SHA match + on-die pairing VALID + controls VALID + Cuneiform devnet settle + chain-readback PASS
**UTC:** window armed 2026-10-12T16:08:49Z → fired 17:25:05Z → captured 17:23:52..17:24:59Z → battery VALID 19:35–19:42Z → settled 19:54:31Z (slot 510375730)

## Summary

| Plane | Result |
|---|---|
| Radio | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9 (chan 3, status 0x10), SNR +10.8..+11.8 dB, count_us 208743044..275975955, inter-frame ~16.8 s, **POST-WRAP (+4294.967296 s)** — machine-selected by the battery's wrap-branch discriminator |
| SHA gate | digest(captured) == declare `383ef43799b208287cf4ff4ca7191f7a9a3f96b50affd6903fa3bf388cccd36f` 64/64 (b_rx_extract.py exit 0, full 64-hex, `sha256_match: true`) |
| Declare | A-bus seq 521 == B-bus seq 1358, cross-bus byte-diff: all 7 fields EQ (public_input_hashes, gateway, firmware, deposit, key id, commitment, proof sha) |
| Pairing (T12 battery, NORMAL mode) | PRIMARY `383ef437` (key-32, deposit 100001) **VALID 142.0 s** + CONTROL-same c-70 `c300e5b4` (key-32, same statement-class) **VALID 142.1 s** + CONTROL-diff c-89 `04b46364` (key-31, different class) **VALID 142.3 s** — B die, keys sha-guarded unchanged (PK `8dda8b79…`, VK `7bd5683f…`), silicon 41.3 °C, throttled=0x0 |
| Class scan | key-32 statement class: priors B=15 / A=15 → **NOT first-of-class** (NORMAL mode, 2-control battery) |
| Settle (Cuneiform devnet) | REGISTER TX `5b4cnEypANfXpKfpEfiFpcBp1ZTPkoxGs55r8sEVexwARjvsXbi4S47a3fVLYKnJjzoSrtJekVAnneqbiu6hhyWy`, record PDA `Er4XfWPvYeag32kHAU5dP6smg5K9MRAgfyQnS7hFFW4y`, slot **510375730**, err null; merkle root = proof SHA256; 100k-lamport CPI fee; 6/6 PASS |
| Chain-readback | machine-fetched via `getSignaturesForAddress` on the record PDA — tx present, slot 510375730, account 103 B, root bytes in PDA, digest-only (decode-info scan NONE) → **GATE PASS** |
| Cadence | 82 s declare→fire (**14th consecutive 80s-class**), 39th valid fleet cycle |

## Reproduce (fresh checkout of this PR head)

```bash
# 1. Radio capture gate — session slice of the guard log, fail-closed digest contract:
python3 tools/b_rx_extract.py evidence/groth16_ota_20261012T1608Z_cycle90/c90_session_slice.log \
  --min-size 128 --expect-sha 383ef43799b208287cf4ff4ca7191f7a9a3f96b50affd6903fa3bf388cccd36f
# rc=0 + sha256_match:true + 5 CRC-OK frames. rc=2 = abbreviated digest refused; rc=3 = mismatch = FAILURE.

# 2. Byte-verify the captured payload bin:
sha256sum evidence/groth16_ota_20261012T1608Z_cycle90/rx_payload_128b.bin
# -> 383ef43799b208287cf4ff4ca7191f7a9a3f96b50affd6903fa3bf388cccd36f

# 3. T12 pairing battery from THIS PR's vendored, byte-exact template (sha 92f31236… — identical to the c-88/c-89 vendored copies that produced PR#52/PR#53's VALID verdicts):
export FLEET_FAST_TOKEN=…   # from ~/.hermes/.env
python3 evidence/groth16_ota_20261012T1608Z_cycle90/t12_battery_template_PR48head_158c0a5.py \
  --cycle 90 --evidence-dir evidence/groth16_ota_20261012T1608Z_cycle90 \
  --guard-log <path-to-rx-standby-guard-log>
# -> BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID (see t12_cycle90_battery.log, committed)

# 4. Settle readback gate (devnet):
# getSignaturesForAddress(Er4XfWPvYeag32kHAU5dP6smg5K9MRAgfyQnS7hFFW4y) contains
# 5b4cnEypANfXpKfpEfiFpcBp1ZTPkoxGs55r8sEVexwARjvsXbi4S47a3fVLYKnJjzoSrtJekVAnneqbiu6hhyWy @ slot 510375730, err null
# getAccountInfo(PDA).data contains merkle root 383ef437… (see chain_readback.json)
```

## Files

- `c90_session_slice.log` — raw RX session slice (arm banner 16:08:49Z → listener exit 18:08:49Z)
- `b_rx_extract_output.json` — machine parse, `sha256_match: true`, 5/5 CRC-OK
- `rx_payload_128b.bin` — captured 128 B proof payload (A‖B‖C), sha `383ef437…`
- `declare_snapshot.json` — machine-fetched declare from BOTH buses (A521/B1358)
- `capture_meta.json` — walls serialized from the parse (origin = arm banner second), NOT derived from fire stamps
- `t12_battery_template_PR48head_158c0a5.py` — vendored battery (byte-exact, sha `92f31236…`)
- `t12_cycle90_battery.log` — battery run log: PRIMARY + 2 controls VALID (relaunch; see honest ledger)
- `t12_cycle90_battery_launch1_dead.log` + `t12_cycle90_battery_launch1_note.txt` — launch-1 dead artifacts (honest history)
- `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle (6/6)
- `chain_readback.json` — signature + account readback, GATE PASS

## Honest ledger

- **Launch-1 battery death disclosed:** the prior hourly tick launched this cycle's battery from an execute_code kernel (300-s hard limit) with a buffered stdout pipe — killed mid-pairing, leaving a 0-byte log and no verdict. Relaunched 19:35:37Z per the proven law (`python3 -u` + DIRECT file redirect + terminal background). Dead artifacts committed alongside the healthy run. This was the third recorded instance of the kernel-limit trap; the relaunch law is now in the fleet skill.
- **POST-WRAP capture:** frames landed 4503.7–4570.9 s after arm, past the 71.6-min count_us wrap horizon — the battery's wrap-branch discriminator machine-selected +4294.967296 s (the pre-wrap branch fails the fired-span gate by ~4301 s). Walls are reporting-only; the SHA gate is the binding constraint.
- **Concurrency disclosure:** hourly beacon tick overlapped this run (the c-91 window was declared mid-turn at 19:35:14Z and Alpha's watcher fired into it at 19:36:35Z while the c-90 battery paired). The battery's session-segment binding (guard-log segment + digest equality) is immune to concurrent captures; both cycles' evidence is scoped per-session.
- Window declared via the durable composer `~/fleet/scripts/declare_rx_window.py --cycle 90` (prior tick), idempotent, cert machine-parsed: recovery PASS, arm-banner skew 1.0 s, 2705 s remaining at declare.
- Fire came from the **watcher hot path (no LLM turn)**: source field in the declare, `groth16_tx_fired` 5/5 TX_DONE.
- ZK Settlement Law compliance: on-chain record carries ONLY digest anchors (merkle root = payload SHA, session = SHA[0:16], coords = payload bytes 0..5). No decode recipes, dictionaries, or pre-images. Decode-info scan of the settled PDA: NONE — digest-only.
- Radio honesty: 5 frames captured, 0 CRC-BAD in the drill session, 0 RF-ghosts on adjacent IF channels this cycle. Chip version 0x10 banner in capture log is ground truth (probe skipped while listener holds the bus).
