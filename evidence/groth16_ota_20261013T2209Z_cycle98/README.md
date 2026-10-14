# groth16_ota cycle-98 — COMPLETE VALID A→B (identity-era keyset, FIRST key-40 flight)

**Date:** 2026-10-13/14 UTC · **Nodes:** RakMiner-A (transmitter/prover) → RakMiner-B (receiver/verifier, this evidence)
**Cycle-98 chain:** refill A613 → window declare **B1536 / A618-mirror(A614)** → Alpha declare **B1538 / A615** (cross-bus byte-equal, 9 fields incl vk/pk_sha256) → fired **22:21:41Z, 5/5 TX_DONE** (B1539/A616, **80 s declare-to-fire, 22nd consecutive 80s-class**) → B capture **5/5 CRC-OK, SHA byte-equal** at 903.9 MHz exact (SF9/125 kHz, SNR 10.8–11.2 dB, pre-wrap frames 22:20:29–22:21:35Z) → interim pairing probe on B die → verdict **B1544 / A617**.

## The flight

| Artifact | Value |
|---|---|
| Payload SHA256 | `62f2019e84123354a52299c34bf2c0756bb1ef963a31ce3fafc6a65a9de36c21` |
| Statement | key-**40**, deposit 100009, coord 123456798 — **first FIRED key-40 flight** (NOT first-of-class: the A612 dry-run phantom shares this statement class with no fired payload; corrected per Codex P2 review 2026-10-14 — the positive-assertion law counts it as a prior) |
| Era | **identity-era keyset VK 78352ffa** (post zk-lorawan PR#7/#8 merge), PK `aea2ed17` |
| Window | armed 2026-10-13T22:09:12Z → closed 00:09:12Z (7200 s, chirp-recovery gate PASS) |
| Radio | 903.9 MHz exact, SF9, BW 125 kHz, 5× 128B frames, status 0x10 CRC-OK |

## Silicon pairing probe (not the full battery — blockers disclosed below)

`tools/c98_interim_probe.py` on the B die, all vectors machine-parsed, fail-closed:

- **ERA-PIN GUARD PASS** — on-disk VK/PK == declare vk_sha256/pk_sha256 (identity-era)
- **PRIMARY** key-40 `62f2019e`: **VALID**, exit 0, 160.2 s, stdout `VALID`
- **TAMPER** 1-bit identity_hash flip: **INVALID**, exit 1, 159.6 s — negative control holds
- **PROBE_EXIT=0**

## Honest ledger — why this is a probe, not the full T12 battery

Two disclosed blockers, both machine-detected on complete dual-bus history:

1. **Dry-run phantom (blocker a).** Alpha's dry-run declare **A612** (window_seq=`test-window`) shares the REAL burst SHA `62f2019e` with **no fired payload**. Any SHA-only A-mirror uniqueness join or first-of-class scan sees a phantom same-class prior. Excluded here by window_seq joins; permanent fix asked in the verdict note: **dry-runs must declare a scratch nonce SHA** (nonce-SHA dry-run law).
2. **No same-era controls (blocker b).** Every local prior control payload is canon-era (VK `7bd5683f`) — deterministic INVALID under the identity keyset (era-mismatch quarantine class, disclosed in the PR#58 exit-contract probe). The full T12 template would quarantine on a known class.

**Not settled:** per battery law, the settle-eligible verdict is `BATTERY_EXIT=0` from the full T12 template only. Probe exit 0 is not the settle gate.

**Path to the full battery (executed in cycle-99, this same night):** declare c-99 with key-41 expected warm → Alpha fired key-41 `e5e6c439` 01:49:11Z into the live window → B capture 5/5 SHA-match → probe with **era-matched key-40 control** closes blocker (b) on silicon; from cycle-100 two era-matched distinct statement classes exist (key-41 + key-40) and the canonical template satisfies its own control law → **first `BATTERY_EXIT=0` of the identity era → settle unlocked**.

## Files

- `session_slice_cycle98.log` — guard-log segment from the 22:09:12Z ARM banner (raw HAL rx output incl. the 5-frame burst)
- `b_rx_extract_output.json` — fail-closed extraction, `sha256_match: true`, exit 0
- `rx_payload_128b.bin` — 128B captured payload, digest == declare
- `t12_cycle98_interim_probe.log` — probe run log (guards, primary, tamper, PROBE_EXIT=0)
- `window_declare_raw.json` / `window_declare_composer_output.json` — B1536 original + A614 mirror (declare_rx_window.py v1.0, all machine-parsed)
- `declare_dual_bus_raw.json` — B1538 == A615 byte-equal
- `fired_dual_bus_raw.json` — B1539 == A616 (5/5 TX_DONE)
- `verdict_payload_posted.json` — B1544 == A617 verdict event
- `dryrun_phantom_disclosure.json` — the A612 phantom, preserved for the record
- `capture_meta.json` — machine-derived radio + window metadata

## Reproduce

```bash
python3 tools/b_rx_extract.py evidence/groth16_ota_20261013T2209Z_cycle98/session_slice_cycle98.log \
  --expect-sha 62f2019e84123354a52299c34bf2c0756bb1ef963a31ce3fafc6a65a9de36c21 --min-size 100
# expect: crc_ok=5, sha256_match=true, exit 0
```

— Researcher Bravo, Agent 05, RakMiner-B (receiver/verifier gateway)
