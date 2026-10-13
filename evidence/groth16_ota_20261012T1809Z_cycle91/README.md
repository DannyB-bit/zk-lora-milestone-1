# groth16_ota cycle-91 — COMPLETE VALID A→B (15th consecutive), 81s declare-to-fire

**Cycle:** 91 · **Drill:** groth16_ota (128 B Groth16/BN254 proof OTA)
**Verdict:** COMPLETE VALID — radio SHA match + on-die pairing VALID + controls VALID + Cuneiform devnet settle + chain-readback PASS
**UTC:** window armed 2026-10-12T18:09:09Z → fired 19:36:35Z → captured 19:35:22..19:36:29Z → battery VALID 20:18–20:25Z → settled 20:28:08Z (slot 510384147)

## Summary

| Plane | Result |
|---|---|
| Radio | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9 (chan 3, status 0x10), SNR +10.8..+11.8 dB, count_us 878116836..945252258, inter-frame ~16.8 s, **POST-WRAP (+4294.967296 s)** — machine-selected by the battery's wrap-branch discriminator |
| SHA gate | digest(captured) == declare `659c542e994fdb460e2b7e67b40929f5a8630d077d4b3d54e26127c1cf98f51f` 64/64 (b_rx_extract.py exit 0, full 64-hex, `sha256_match: true`) |
| Declare | A-bus seq 524 == B-bus seq 1369, cross-bus byte-diff: all 7 fields EQ (public_input_hashes, gateway, firmware, deposit, key id, commitment, proof sha) |
| Pairing (T12 battery, NORMAL mode — attempt-3) | PRIMARY `659c542e` (key-33, deposit 100002) **VALID 141.9 s** + CONTROL-same c-87 `e703bfd3` (key-33, same statement-class, vendored) **VALID 141.9 s** + CONTROL-diff c-90 `383ef437` (key-32, different class) **VALID 142.2 s** — B die, keys sha-guarded unchanged (PK `8dda8b79…`, VK `7bd5683f…`), silicon 41.8 °C, throttled=0x0 |
| Class scan | key-33 statement class: priors B=2 / A=2 → **NOT first-of-class** (NORMAL mode, 2-control battery) |
| Settle (Cuneiform devnet) | REGISTER TX `4QLP3ZnM3LZjZmP2xVQdrPtQqQ2dMKfLBP5aDjjAphmcQv8Nv73p1LmNQtenufoqZ645TYosfHRnp4aLLuaSGEKS`, record PDA `CK1fdyCFGphgyJsJaFaG5nDiqnERHjc1RVUp6xi6NUCU`, slot **510384147**, err null; merkle root = proof SHA256; 100k-lamport CPI fee; 6/6 PASS |
| Chain-readback | machine-fetched via `getSignaturesForAddress` on the record PDA — tx present, slot 510384147, account 103 B, root bytes in PDA, digest-only (decode-info scan NONE) → **GATE PASS** |
| Cadence | 81 s declare→fire (**15th consecutive 80s-class**), 40th valid fleet cycle |

## Reproduce (fresh checkout of this PR head)

```bash
# 1. Radio capture gate — session slice of the guard log, fail-closed digest contract:
python3 tools/b_rx_extract.py evidence/groth16_ota_20261012T1809Z_cycle91/c91_session_slice.log \
  --min-size 128 --expect-sha 659c542e994fdb460e2b7e67b40929f5a8630d077d4b3d54e26127c1cf98f51f
# rc=0 + sha256_match:true + 5 CRC-OK frames. rc=2 = abbreviated digest refused; rc=3 = mismatch = FAILURE.

# 2. Byte-verify the captured payload bin:
sha256sum evidence/groth16_ota_20261012T1809Z_cycle91/rx_payload_128b.bin
# -> 659c542e994fdb460e2b7e67b40929f5a8630d077d4b3d54e26127c1cf98f51f

# 3. T12 pairing battery from THIS PR's vendored, byte-exact template (sha 92f31236…):
export FLEET_FAST_TOKEN=…   # from ~/.hermes/.env
python3 evidence/groth16_ota_20261012T1809Z_cycle91/t12_battery_template_PR48head_158c0a5.py \
  --cycle 91 --evidence-dir evidence/groth16_ota_20261012T1809Z_cycle91 \
  --guard-log <path-to-rx-standby-guard-log>
# -> BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID (see t12_cycle91_battery.log, committed)
# NOTE: the same-class control (c-87 key-33 payload e703bfd3) is restored by this PR to
# evidence/groth16_ota_20261012T0206Z_cycle87/rx_payload_128b.bin (byte-exact from commit 26e2edc,
# provenance in vendored_control_provenance.json) — without it the battery ABORTs fail-closed.

# 4. Settle readback gate (devnet):
# getSignaturesForAddress(CK1fdyCFGphgyJsJaFaG5nDiqnERHjc1RVUp6xi6NUCU) contains
# 4QLP3ZnM3LZjZmP2xVQdrPtQqQ2dMKfLBP5aDjjAphmcQv8Nv73p1LmNQtenufoqZ645TYosfHRnp4aLLuaSGEKS @ slot 510384147, err null
# getAccountInfo(PDA).data contains merkle root 659c542e… (see chain_readback.json)
```

## Files

- `c91_session_slice.log` — raw RX session slice (arm banner 18:09:09Z → live session EOF)
- `b_rx_extract_output.json` — machine parse, `sha256_match: true`, 5/5 CRC-OK
- `rx_payload_128b.bin` — captured 128 B proof payload (A‖B‖C), sha `659c542e…`
- `declare_snapshot.json` — machine-fetched declare from BOTH buses (A524/B1369)
- `capture_meta.json` — walls serialized from the parse (origin = arm banner second), NOT derived from fire stamps
- `t12_battery_template_PR48head_158c0a5.py` — vendored battery (byte-exact, sha `92f31236…`)
- `t12_cycle91_battery.log` — attempt-3 battery run log: PRIMARY + 2 controls VALID
- `t12_cycle91_battery_attempt1_abort.no-local-sameclass-control.log` — attempt-1 fail-closed ABORT (honest history)
- `t12_cycle91_battery_attempt2_abort.invented-attempt2-flag.log` — attempt-2 launcher bug (honest history)
- `vendored_control_provenance.json` — same-class control restoration provenance (c-87 payload, byte-exact from 26e2edc)
- `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle (6/6)
- `chain_readback.json` — signature + account readback, GATE PASS

## Honest ledger

- **Attempt-1 ABORT (fail-closed, working as designed):** key-33 is NOT first-of-class (priors B1250/B1294, A484/A501 = the c-84/c-87 cycles), but the prior same-class payloads lived only on the unmerged PR#51 branch — no local `rx_payload_128b.bin` was verifiable. The template refused to relabel and refused to weaken controls. **Fix per the vendoring contract:** restored the c-87 captured payload byte-exact from commit `26e2edc` (sha-verified `e703bfd3…`) to its original path `evidence/groth16_ota_20261012T0206Z_cycle87/rx_payload_128b.bin`, provenance JSON committed. The c-87 run performed the identical restoration for its c-84 control.
- **Attempt-2 ABORT (my error, disclosed):** the relaunch script passed an invented `--attempt2` flag the template does not accept — argparse exit 2 before any work. Sloppy flag spec on my side; both abort logs are committed as honest history.
- **POST-WRAP capture:** frames landed 5153.7–5220.5 s after arm — past the 71.6-min count_us wrap horizon; battery wrap-branch discriminator machine-selected +4294.967296 s. Walls are reporting-only; the SHA gate is the binding constraint.
- **Concurrency disclosure:** this cycle was declared (19:35:14Z), fired (19:36:35Z), captured, and battery-verified inside a single hourly tick that also closed cycle-90 end-to-end. No foreign commits landed on any open PR branch (pre-push fetch performed at commit time).
- Fire came from the **watcher hot path (no LLM turn)**: source field in the declare, `groth16_tx_fired` 5/5 TX_DONE.
- ZK Settlement Law compliance: on-chain record carries ONLY digest anchors (merkle root = payload SHA, session = SHA[0:16], coords = payload bytes 0..5). No decode recipes, dictionaries, or pre-images. Decode-info scan of the settled PDA: NONE — digest-only.
- Radio honesty: 5 frames captured, 0 CRC-BAD in the drill session, 0 RF-ghosts on adjacent IF channels this cycle. Chip version 0x10 banner in capture log is ground truth (probe skipped while listener holds the bus).
