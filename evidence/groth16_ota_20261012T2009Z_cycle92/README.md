# groth16_ota cycle-92 — COMPLETE VALID A→B (16th consecutive), 80s declare-to-fire

**Cycle:** 92 · **Drill:** groth16_ota (128 B Groth16/BN254 proof OTA)
**Verdict:** COMPLETE VALID — radio SHA match + on-die pairing VALID + controls VALID + Cuneiform devnet settle + chain-readback PASS
**UTC:** window armed 2026-10-12T20:09:29Z → declared 21:51:46Z (B1383/A531) → fired 21:53:06Z → captured 21:51:53..21:53:00Z → battery VALID 22:10:46–22:17:54Z → settled 22:19:37Z (slot 510412182)

## Summary

| Plane | Result |
|---|---|
| Radio | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9 (chan 3, status 0x10), SNR +10.8..+11.2 dB, count_us 1849250204..1916348947, inter-frame ~16.8 s, **POST-WRAP (+4294.967296 s)** — machine-selected by the battery's wrap-branch discriminator |
| SHA gate | digest(captured) == declare `79e06d07d6d36a51d05f8b1d4c76898f1f3d9d3cc9ab1f6d22763b33b3cc3f03` 64/64 (b_rx_extract.py exit 0, full 64-hex, `sha256_match: true`) |
| Declare | A-bus seq 531 == B-bus seq 1383, cross-bus byte-diff: all 7 fields EQ (public_input_hashes, gateway, firmware, deposit, key id, commitment, proof sha) |
| Pairing (T12 battery, NORMAL mode — attempt-2) | PRIMARY `79e06d07` (key-34, deposit 100003) **VALID 142.1 s** + CONTROL-same c-88 `81fd764b` (key-34, same statement-class, restored) **VALID 142.0 s** + CONTROL-diff c-70 `c300e5b4` (key-32, different class) **VALID 142.2 s** — B die, keys sha-guarded unchanged (PK `8dda8b79…`, VK `7bd5683f…`), silicon 44.3→48.7 °C, throttled=0x0 |
| Class scan | key-34 statement class: priors B=1 / A=1 (c-88, B1308/A507) → **NOT first-of-class** — c-92 is the SECOND key-34 statement cycle (first was c-88, positively asserted in PR#52 `ae664d9`) |
| Settle (Cuneiform devnet) | REGISTER TX `sBqpfqp8hGhYgeZAp33nqnpQKzT6osGkAtd5fgopSU4BtztLUrcwkuZCNUwN6W5vnDhQTJw6fmUHBEfeuL4GVF6`, record PDA `6jaL2aFxMZ8L57aCMDWQGc9f6HQjfToNRLaZC1pMS2mE`, slot **510412182**, err null; merkle root = proof SHA256; 100k-lamport CPI fee; 6/6 PASS |
| Chain-readback | machine-fetched via `getSignaturesForAddress` on the record PDA — tx present, slot 510412182, account 103 B owned by the Cuneiform program, root bytes in PDA, digest-only (decode-info scan NONE) → **GATE PASS** |
| Cadence | 80 s declare→fire (**16th consecutive 80s-class**), 41st valid fleet cycle |

## Reproduce (fresh checkout of this PR head)

```bash
# 1. Radio capture gate — session slice of the guard log, fail-closed digest contract:
python3 tools/b_rx_extract.py evidence/groth16_ota_20261012T2009Z_cycle92/c92_session_slice.log \
  --min-size 128 --expect-sha 79e06d07d6d36a51d05f8b1d4c76898f1f3d9d3cc9ab1f6d22763b33b3cc3f03
# rc=0 + sha256_match:true + 5 CRC-OK frames. rc=2 = abbreviated digest refused; rc=3 = mismatch = FAILURE.

# 2. Byte-verify the captured payload bin:
sha256sum evidence/groth16_ota_20261012T2009Z_cycle92/rx_payload_128b.bin
# -> 79e06d07d6d36a51d05f8b1d4c76898f1f3d9d3cc9ab1f6d22763b33b3cc3f03

# 3. T12 pairing battery from THIS PR's vendored, byte-exact template (sha 92f31236…):
export FLEET_FAST_TOKEN=…   # from ~/.hermes/.env
python3 evidence/groth16_ota_20261012T2009Z_cycle92/t12_battery_template_PR48head_158c0a5.py \
  --cycle 92 --evidence-dir evidence/groth16_ota_20261012T2009Z_cycle92 \
  --guard-log <path-to-rx-standby-guard-log>
# -> BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID (see t12_cycle92_battery.log, committed)
# NOTE: the same-class control (c-88 key-34 payload 81fd764b) is restored by this PR to
# evidence/groth16_ota_20261012T0406Z_cycle88/rx_payload_128b.bin (byte-exact from PR#52 head
# ae664d9, provenance in vendored_control_provenance.json) — without it the battery ABORTs fail-closed.

# 4. Settle readback gate (devnet):
# getSignaturesForAddress(6jaL2aFxMZ8L57aCMDWQGc9f6HQjfToNRLaZC1pMS2mE) contains
# sBqpfqp8hGhYgeZAp33nqnpQKzT6osGkAtd5fgopSU4BtztLUrcwkuZCNUwN6W5vnDhQTJw6fmUHBEfeuL4GVF6 @ slot 510412182, err null
# getAccountInfo(PDA).data contains merkle root 79e06d07… (see chain_readback.json)
```

## Files

- `c92_session_slice.log` — raw RX session slice (arm banner 20:09:29Z → live session EOF)
- `b_rx_extract_output.json` — machine parse, `sha256_match: true`, 5/5 CRC-OK
- `rx_payload_128b.bin` — captured 128 B proof payload (A‖B‖C), sha `79e06d07…`
- `declare_snapshot.json` — machine-fetched declare from BOTH buses (A531/B1383), byte-identical
- `capture_meta.json` — walls serialized from the parse (origin = arm banner second), NOT derived from fire stamps
- `t12_battery_template_PR48head_158c0a5.py` — vendored battery (byte-exact, sha `92f31236…`)
- `t12_cycle92_battery.log` — attempt-2 battery run log: PRIMARY + 2 controls VALID
- `t12_cycle92_battery_attempt1_abort.no-local-sameclass-control.log` — attempt-1 fail-closed ABORT (verbatim content preserved; see honest ledger for the overwrite note)
- `vendored_control_provenance.json` — same-class control restoration provenance (c-88 payload, byte-exact from PR#52 head `ae664d9`)
- `evidence/groth16_ota_20261012T0406Z_cycle88/rx_payload_128b.bin` — restored in this PR (original dir path, sha `81fd764b…`)
- `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle (6/6)
- `chain_readback.json` — signature + account readback, GATE PASS

## Honest ledger

- **Attempt-1 ABORT (fail-closed, working as designed):** I initially read the c-92 declare as a possible FIRST key-34 cycle and pre-labeled the settle draft "FIRST key-34 statement class". The template's class scan proved otherwise — priors B[1308] A[507] = cycle-88 (same public-input vector, deposit 100003) — and, finding no local same-class payload (stranded on unmerged PR#52), it ABORTed rather than relabel. **Fix per the vendoring contract:** restored the c-88 captured payload byte-exact from PR#52 head `ae664d9` via `git cat-file blob` (sha-verified `81fd764b…` against the dual-bus declare B1308/A507) to its original path `evidence/groth16_ota_20261012T0406Z_cycle88/rx_payload_128b.bin`; provenance JSON committed. Attempt-2 then ran NORMAL mode: same-class c-88 + different-class c-70 controls, all VALID.
- **Label correction disclosed:** the settle artifact's draft `SETTLE_VERIFIED` / `SETTLED_TRANSFER` strings carried the pre-battery "FIRST key-34" wording. Corrected on disk BEFORE commit to "SECOND key-34 statement cycle"; on-chain commitments were never affected (they carry only digest anchors: merkle root, session id, coords, ts).
- **Attempt-1 abort log overwritten, reconstructed:** the launcher redirects the battery log to a fixed filename, so attempt-2's run overwrote attempt-1's abort log. The verbatim content (3 lines) was captured from a same-turn read and is committed as `…attempt1_abort…log` with this disclosure; the abort is also fully described in the battery's own attempt-2 provenance and the bus verdict. Launcher lesson (same class as the c-90 buffering law): rotate log filenames per attempt.
- **POST-WRAP capture:** frames landed 6144.4–6251.5 s after arm — past the 71.6-min count_us wrap horizon; battery wrap-branch discriminator machine-selected +4294.967296 s (fired-stamp gate: only the post-wrap branch passes −180..+240 s; pre-wrap is 4367.7 s off). Walls are reporting-only; the SHA gate is the binding constraint.
- **Concurrency disclosure:** this cycle was declared (21:51:44Z), fired (21:53:06Z), captured, and battery-verified inside a single hourly tick that ran ~16 min past the window close. No foreign commits landed on any open PR branch (pre-push fetch performed at commit time).
- Fire came from the **watcher hot path (no LLM turn)**: source field in the declare, `groth16_tx_fired` 5/5 TX_DONE.
- ZK Settlement Law compliance: on-chain record carries ONLY digest anchors (merkle root = payload SHA, session = SHA[0:16], coords = payload bytes 0..5). No decode recipes, dictionaries, or pre-images. Decode-info scan of the settled PDA: NONE — digest-only (103 B).
- Radio honesty: 5 frames captured, 0 CRC-BAD in the drill session, 0 RF-ghosts on adjacent IF channels this cycle. Chip version 0x10 banner in capture log is ground truth (probe skipped while listener holds the bus). Standby re-armed automatically at 22:09:49Z (PID 164655).
