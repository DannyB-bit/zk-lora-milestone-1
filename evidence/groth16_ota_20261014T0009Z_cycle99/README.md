# groth16_ota cycle-99 — COMPLETE VALID A→B (key-41, identity era) — ERA-MATCHED CONTROL CLOSED ON SILICON

**Date:** 2026-10-14 UTC · **Nodes:** RakMiner-A (transmitter/prover) → RakMiner-B (receiver/verifier, this evidence)
**Chain:** window declare **B1551 / A618** (key-41 expected warm; guard re-arm certified 00:09:32Z) → Alpha watcher declare **B1553 / A619** (9 fields byte-equal incl vk/pk_sha256) → fired **01:49:11Z, 5/5 TX_DONE** (**80 s declare-to-fire, 23rd consecutive 80s-class**) → B capture **5/5 CRC-OK, SHA byte-equal** (903.9 MHz exact, SF9/125 kHz, SNR 10.5–11.5 dB, **POST-WRAP** frames 01:48:18–01:49:05Z) → interim pairing probe → verdict **B1558 / A621**.

## The flight

| Artifact | Value |
|---|---|
| Payload SHA256 | `e5e6c4394e2b7166c4971342f63ae9412b0591a4b20873fefa1465387a6cabcd` |
| Statement | key-**41**, deposit 100010, coord 123456799 — **first key-41 statement class in fleet history** |
| Era | identity-era keyset **VK 78352ffa** / PK `aea2ed17` (era-pin guard PASS) |
| Window | armed 2026-10-14T00:09:32Z → closed 02:09:32Z (7200 s, chirp-recovery gate PASS) |
| Radio | 903.9 MHz exact, SF9, BW 125 kHz, 5× 128B frames, status 0x10 CRC-OK |

## Silicon pairing probe — PRIMARY + TAMPER + era-matched control

`tools/c99_interim_probe.py` (new this cycle), all vectors machine-parsed, fail-closed:

- **ERA-PIN GUARD PASS** — on-disk VK/PK == declare keyset (identity-era VK 78352ffa)
- **PRIMARY** key-41 `e5e6c439`: **VALID**, exit 0, 159.7 s
- **TAMPER** 1-bit identity_hash flip: **INVALID**, exit 1, 159.6 s
- **ERA-MATCHED CONTROL** — c-98 key-40 payload `62f2019e` (on-disk, its declare B1538==A615 re-joined by window_seq+SHA): **VALID**, exit 0, 160.1 s → **B617 blocker (b) CLOSED on silicon**
- **PROBE_EXIT=0**

**Why a probe, not the full T12 battery:** key-41 is first-of-class, so the canonical template demands 2 DISTINCT-statement-class controls; only ONE era-matched distinct class exists tonight (key-40). The older canon-era controls (VK 7bd5683f) verify INVALID under the identity keyset by construction — era-mismatch quarantine class. Running the full battery now would quarantine on a known class. **From cycle-100 the control law is satisfiable** (key-41 + key-40 = two era-matched distinct classes) → predicted first `BATTERY_EXIT=0` of the identity era → settle unlocked.

**Blocker (a) still open (asked to Alpha in B1558/A621):** the A612 dry-run declare (window_seq=`test-window`) shares the real c-98 burst SHA with no fired payload — SHA-only A-mirror uniqueness joins and first-of-class scans still see the phantom. Permanent fix: **nonce-SHA dry-run law** (dry-runs declare a scratch nonce SHA). This probe joins the control's A-mirror on window_seq + SHA, excluding the phantom.

**Honest engineering note:** the probe's first control lookup failed closed (`ABORT: control declare not unique on A-bus (found 2)` — the phantom); fixed by the window_seq+SHA join and re-run clean. Both runs are disclosed here.

## Files

- `session_slice_cycle99.log` — guard-log segment from the 00:09:32Z ARM banner (raw HAL rx output incl. the 5-frame burst)
- `b_rx_extract_output.json` — fail-closed extraction, `sha256_match: true`, exit 0
- `rx_payload_128b.bin` — 128B captured payload, digest == declare
- `t12_cycle99_interim_probe.log` — probe run log (guards, primary, tamper, era-matched control, PROBE_EXIT=0)
- `window_declare_raw.json` — B1551 original + A618 mirror
- `declare_dual_bus_raw.json` — B1553 == A619
- `fired_dual_bus_raw.json` — B1554 == A620 (5/5 TX_DONE)
- `verdict_payload_posted.json` — B1558 == A621
- `capture_meta.json` — machine-derived radio + window metadata

## Reproduce

```bash
python3 tools/b_rx_extract.py evidence/groth16_ota_20261014T0009Z_cycle99/session_slice_cycle99.log \
  --expect-sha e5e6c4394e2b7166c4971342f63ae9412b0591a4b20873fefa1465387a6cabcd --min-size 100
# expect: crc_ok=5, sha256_match=true, exit 0
```

— Researcher Bravo, Agent 05, RakMiner-B (receiver/verifier gateway)
