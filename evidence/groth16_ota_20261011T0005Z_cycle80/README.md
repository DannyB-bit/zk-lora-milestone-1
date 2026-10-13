# groth16_ota cycle-80 — COMPLETE VALID A→B (30th valid cycle)

**Window**: armed 2026-10-11T00:05:49Z → close 2026-10-11T02:05:49Z (listener PID 117620,
`test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0`,
83rd consecutive `LORA_CHIRP_RECOVERY_PASS=YES` gate, chip 0x10 v1.0, `ps lstart` == arm
banner second — zero post-NTP drift). Third window declared by the durable tz-aware composer
`declare_rx_window.py v1.0` (B1186/A455), machine-parsed cert, dual-bus readback.

**Hold-and-release**: B saw Alpha's cache at 0 warm after c-79 spent `0241669a` (his key-32);
wake brief (`hermes peer run`, idempotency key `bravo-c80-wake-20261011T0014Z`) relit his
agent lane → he rebuilt 2 WARM proofs (`aee2816a` key-31, deposit 100000 + `ff238e52`
key-32, deposit 100001, both canon VK 7bd5683f) → his b_ack A454 said **"RELEASE YOUR
c-80 DECLARE"** → declared same turn. Zero fires burned on a cold cache.

**Fire** (bus-stamp derived — corrected per Codex review, see `bus_timing_v2.json`):
B1186/A455 posted 01:39:25Z → Alpha watcher declared in **1 s** (B1188/A456 01:39:26Z,
`aee2816a` key-31, deposit 100000 — exactly the warm proof his 00:30:08Z b_ack promised)
→ 5/5 TX_DONE 01:40:46Z: **81 s declare-to-fire — 6th consecutive 80 s-class hot-path
fire (81/81/82/80/79/81 s)**, 6th consecutive watcher-autonomous fire, no LLM turn in
the loop. The original 80 s figure used the composer *invocation* stamp (01:38:56Z in
`capture_meta.json`); the bus POST timestamps are the authoritative metric — correction
recorded in `corrections.md`.

**Proof**: key-31, deposit 100000, 128 B compressed Groth16/BN254
(A 32B G1 || B 64B G2 || C 32B G1), seed-42 canon PK (PK sha 8dda8b79 / VK sha 7bd5683f),
watcher hot-path cache pop, full public-input vector declared (4 hashes + gateway
`0016c001ff18afa3...` + deposit + firmware hash).

**Payload SHA256**: `aee2816a0a98fc4db4ff0e61e29c846a2945f4d50ede9e5e16c030c02223baa8`

## Radio capture (machine-extracted, `b_rx_extract.py` rc=0)

- 5/5 CRC-OK 128 B frames @ 903.9 MHz (radio A 904.3 MHz, IF −400 kHz), SF9/125 kHz
- count_us 1328494168..1395645163 (**POST-WRAP** frames — arm 00:05:49Z + count_us/1e6 +
  4294.967296 s; branch machine-selected by the battery, assert len(passing)==1),
  inter-frame ≈16.8 s, SNR +10.8..+11.5 dB
- `sha256(payload) == declare` — 5/5 byte-identical, `sha256_match: true`

## T12 pairing battery (`T12_CYCLE80_BATTERY_RUN_UTC=2026-10-11T01:52:10Z`)

- PRIMARY cycle-80 captured `aee2816a` (key-31): **VALID**, 142.1 s
- CONTROL-diff key-32 `c300e5b4` (c-70, different statement class): **VALID**, 142.1 s
  — the **executed** control (machine-picked by the battery from committed evidence;
  `ff238e52` was the second warm cache proof, NOT a battery control — the settle_run.log
  env echo naming it was wrong, corrected per Codex P2, see `corrections.md`)
- CONTROL-same key-31 `edac7acc` (c-69, same class): **VALID**, 142.0 s
- SHA gate 64/64; declare cross-bus byte-equal (A456 == B1188, 7 fields EQ); GUARD binary
  a0c74748 / PK 8dda8b79 / VK 7bd5683f unchanged before/after; silicon 40.4 → 45.7 °C,
  throttled=0x0

## Cuneiform Devnet settlement (chain-readback verified)

- Record PDA: `4VtY6koUbfc5raGD6VnFjKbFrdXuZnGsGGX2FqfKdXVv`
- REGISTER TX: `4VRiSnzdVBViDHKKdM3784qiAmJcPyHfJELdKuRfvXuTbNNqkGT7CzQB1mSxwhgXULdKjV4oz2sWQgim7czsnb47`
  (slot 509744368, err=null — machine-fetched `getSignaturesForAddress` byte-match)
- Merkle root = proof payload SHA256 — **raw-32-byte readback PASS** (`chain_readback_v2.json`:
  `getAccountInfo` → root at Anchor offset 62..94 byte-exact, session ASCII 40..56, coords
  raw 56..62, slot 509772356). The v1 `chain_readback.json` hex-string probe was structurally
  void (it searched for the 64-char hex *string* inside raw account bytes; the program stores
  the root as raw 32 B) — superseded, see `corrections.md`.
  Coords registered `[132, 182, 56, 35, 123, 217]` (proof payload bytes 0..5)
- Treasury +100000 lamports; 6/6 settle tests passed; `ZK_RF_TO_CHAIN_LOOP_CLOSED=YES`

## Honest ledger

- **Corrections this cycle** (Codex review on PR #45, 2026-10-11T02:10Z, all verified
  against real bytes and fixed in `corrections.md`): (1) hot-path timing re-derived from
  bus stamps — 81 s, not 80 s; (2) v1 chain readback hex-string probe superseded by a
  raw-byte `getAccountInfo` readback (PASS — settlement itself was sound); (3) settle
  metadata named the wrong control (`ff238e52` vs executed `c300e5b4`).
- No misses, no misfires, no URL corrections this cycle (the c-78 hand-typed-URL defect
  class stays closed — PR URL below is machine-fetched from the API readback).
- Alpha's cache after this fire: 1 warm (`ff238e52` key-32) — refill ask posted with the
  complete_valid verdict.
- His agent lane was again idle through the fire itself (heartbeats current, watcher
  hot-path alive) — the fire loop remains fully watcher-autonomous.
- First cycle closed end-to-end (declare→fire→capture→T12→settle→PR) inside a single
  agent turn.

## Files

- `c80_session_slice.log` — listener session slice (arm banner line 1538 → burst)
- `b_rx_extract_output.json` — machine extraction, SHA gate PASS
- `declare_c80.json` — composer output (window declare payload + cert)
- `bus_events_drill.json` — c-80 drill events, both buses
- `bus_timing_v2.json` — **bus-stamp timing derivation (Codex P1 fix)**: window open
  01:39:25Z → proof declare 01:39:26Z (+1 s) → TX complete 01:40:46Z = 81 s
- `t12_cycle80_battery.log` — full T12 battery run (post-wrap branch selected)
- `settle_run.log` — devnet settle output
- `chain_readback.json` — v1 signature readback (superseded — hex-string probe defect)
- `chain_readback_v2.json` — **raw-byte account readback (Codex P1 fix)**:
  session/coords/root byte-exact at Anchor offsets 40/56/62, slot 509772356
- `corrections.md` — all three Codex findings, verified + remediated, with byte evidence
- `capture_meta.json`, `result_summary.txt` — machine-derived summary
- `rx_payload_128b.bin` — the 128 B captured proof payload (byte-exact)
- `extract_run.log`, `t12_console.log` — raw tool/console output of this cycle
- `c80_wake_brief_result.json` — the peer-run wake brief that relit Alpha's agent lane

## Reproduce

```
python3 tools/b_rx_extract.py evidence/groth16_ota_20261011T0005Z_cycle80/c80_session_slice.log \
  --expect-sha aee2816a0a98fc4db4ff0e61e29c846a2945f4d50ede9e5e16c030c02223baa8 --min-size 100
python3 tools/t12_battery_template.py --cycle 80 \
  --evidence-dir evidence/groth16_ota_20261011T0005Z_cycle80 \
  --guard-log ~/fleet/logs/rx_standby_continuous_20261010T064617Z.log
# chain readback: getSignaturesForAddress(4VtY6koUbfc5raGD6VnFjKbFrdXuZnGsGGX2FqfKdXVv)
```
