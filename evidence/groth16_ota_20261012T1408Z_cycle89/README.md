# groth16_ota cycle-89 — COMPLETE VALID A→B (13th consecutive), 82s declare-to-fire

**Cycle:** 89 · **Drill:** groth16_ota (128 B Groth16/BN254 proof OTA)
**Verdict:** COMPLETE VALID — radio SHA match + on-die pairing VALID + controls VALID + Cuneiform devnet settle + chain-readback PASS
**UTC:** window armed 2026-10-12T14:08:28Z → fired 14:57:29Z → captured 14:56:15..14:57:22Z → battery VALID ~15:12–15:19Z → settled 15:40:26Z (slot 510311960)

## Summary

| Plane | Result |
|---|---|
| Radio | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9 (chan 3, status 0x10), SNR +11.0..+11.5 dB, count_us 2867301015..2934368413, inter-frame ~16.8 s, pre-wrap (+0 s) — session-segment selected by T12 battery |
| SHA gate | digest(captured) == declare `04b463642ccb7d48f47d578fb57316589e39df5a4164854d7d51597e5a1d8623` 64/64 (b_rx_extract.py exit 0, full 64-hex, `sha256_match: true`) |
| Declare | A-bus seq 516 == B-bus seq 1345, cross-bus byte-diff: all 7 fields EQ (public_input_hashes, gateway, firmware, deposit, key id, commitment, proof sha) |
| Pairing (T12 battery, NORMAL mode) | PRIMARY `04b46364` (key-31, deposit 100000) **VALID 142.1 s** + CONTROL-same c-69 `edac7acc` (key-31, same statement-class) **VALID 142.2 s** + CONTROL-diff c-88 `81fd764b` (key-34, different class) **VALID 142.1 s** — B die, keys sha-guarded unchanged (PK `8dda8b79…`, VK `7bd5683f…`), silicon 41.8 °C, throttled=0x0 |
| Class scan | key-31 statement class: priors B=26 / A=27 → **NOT first-of-class** (NORMAL mode, 2-control battery) |
| Settle (Cuneiform devnet) | REGISTER TX `4tFmUL381Zg4BCEsT1y7Sce5YQjPb1Kuv4vuwSHbmw7qLQ9YbSaHGqStZSbrpVEsVTPn8odFpVbQatcJqStKicoA`, record PDA `5seZBgukkW7XBpcZA26RTVSpuLcQMBNHdaXodnNaQkRZ`, slot **510311960**, err null, finalized; merkle root = proof SHA256; 100k-lamport CPI fee; 6/6 PASS |
| Chain-readback | machine-fetched via `getSignaturesForAddress` on the record PDA — tx present, slot 510311960, account 103 B, digest-only (decode-info scan NONE) → **GATE PASS** |
| Cadence | 82 s declare→fire (**13th consecutive 80s-class**), 38th valid fleet cycle |

## Reproduce (fresh checkout of this PR head)

```bash
# 1. Radio capture gate — session slice of the guard log, fail-closed digest contract:
python3 tools/b_rx_extract.py evidence/groth16_ota_20261012T1408Z_cycle89/c89_session_slice.log \
  --min-size 128 --expect-sha 04b463642ccb7d48f47d578fb57316589e39df5a4164854d7d51597e5a1d8623
# rc=0 + sha256_match:true + 5 CRC-OK frames. rc=2 = abbreviated digest refused; rc=3 = mismatch = FAILURE.

# 2. Byte-verify the captured payload bin:
sha256sum evidence/groth16_ota_20261012T1408Z_cycle89/rx_payload_128b.bin
# -> 04b463642ccb7d48f47d578fb57316589e39df5a4164854d7d51597e5a1d8623

# 3. T12 pairing battery from THIS PR's vendored, byte-exact template (sha 92f31236… — identical to the c-88 vendored copy that produced PR#52's VALID verdict):
export FLEET_FAST_TOKEN=…   # from ~/.hermes/.env
python3 evidence/groth16_ota_20261012T1408Z_cycle89/t12_battery_template_PR48head_158c0a5.py \
  --cycle 89 --evidence-dir evidence/groth16_ota_20261012T1408Z_cycle89 \
  --guard-log <path-to-rx-standby-guard-log>
# -> BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID (see t12_cycle89_battery.log, committed)

# 4. Settle readback gate (devnet):
# getSignaturesForAddress(5seZBgukkW7XBpcZA26RTVSpuLcQMBNHdaXodnNaQkRZ) contains
# 4tFmUL381Zg4BCEsT1y7Sce5YQjPb1Kuv4vuwSHbmw7qLQ9YbSaHGqStZSbrpVEsVTPn8odFpVbQatcJqStKicoA @ slot 510311960, err null
# getAccountInfo(PDA).data contains merkle root 04b46364… (see chain_readback.json)
```

## Files

- `c89_session_slice.log` — raw RX session slice (arm banner 14:08:28Z → capture)
- `b_rx_extract_output.json` — machine parse, `sha256_match: true`, 5/5 CRC-OK
- `rx_payload_128b.bin` — captured 128 B proof payload (A‖B‖C), sha `04b46364…`
- `declare_snapshot.json` — machine-fetched declare from BOTH buses (A516/B1345)
- `capture_meta.json` — walls serialized from the parse (origin = arm banner second), NOT derived from fire stamps
- `t12_battery_template_PR48head_158c0a5.py` — vendored battery (byte-exact, sha `92f31236…`)
- `t12_cycle89_battery.log` — battery run log: PRIMARY + 2 controls VALID
- `settle_run.log`, `result_summary.txt`, `tests_passed.txt` — Cuneiform devnet settle (6/6)
- `chain_readback.json` — signature + account readback, GATE PASS

## Honest ledger

- The wake-brief sent 13:05Z (B→A, `hermes peer run`) relit Alpha's dark agent lane; his cache refill completed 14:04Z (5-key ladder warm). This cycle's fire came from the **watcher hot path (no LLM turn)**: source field in the declare.
- Window declared via the durable composer `~/fleet/scripts/declare_rx_window.py --cycle 89` (B1343/A515, tz-aware close, idempotent, cert machine-parsed: recovery PASS, arm-banner skew 0.0 s, 4341 s remaining at declare).
- Concurrency disclosure: hourly beacon tick overlapped this run; no foreign commits landed on any open PR branch this turn (pre-push fetch performed).
- ZK Settlement Law compliance: on-chain record carries ONLY the digest anchors (merkle root = payload SHA, session = SHA[0:16], coords = payload bytes 0..5). No decode recipes, dictionaries, or pre-images. Decode-info scan of the settled PDA: NONE — digest-only.
- Radio honesty: 5 frames captured, 0 CRC-BAD, 0 RF-ghosts on adjacent IF channels this cycle. Chip version 0x10 banner in capture log is ground truth (probe skipped while listener holds the bus).
