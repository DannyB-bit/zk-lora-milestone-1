# Cycle-24 OTA Groth16 Exchange — the disputed key-31 statement class, live over 903.9 MHz

**Window:** cycle-24, armed 2026-10-05T14:17:33Z → closes 16:17:33Z (23rd consecutive
cert gate PASS, zero dark seconds since 10-01).
**Fired by Alpha:** watcher hot-path (no LLM), declared seq 229 @ 16:00:43Z
(`groth16_proof_tx`, declare-before-fire), fired 16:02:03Z, **5/5 TX_DONE**.
**Captured by B:** **5/5 CRC-OK, 128 B, byte-identical SHA
`96db35c5594c2c258c09b80a64991153ce7f49dc68b727945f9baa58970faad8`** — **SHA MATCH**.

## Why this fire matters

This is the **key-31 statement class** (`cbe1d4d7…` vector, deposit 100000) that B's
silicon flagged INVALID 9/9 today (batteries v1-v6) while Alpha's silicon verified it
**VALID** in paired runs (seq 225: a1706406 VALID 116 s @ 13:38Z; 264a8fea control
VALID 115 s). Per B's pre-declared decision matrix: **B silicon fault CONFIRMED** —
identical bytes, identical keys, identical binary, split verdicts across two A72s.
Radio capture is silicon-independent and byte-exact; the disputed proof bytes are now
tied to a live over-the-air transfer, independently VALID on the transmitting die.

## Radio leg (fully green, silicon-independent)

- Alpha declared pre-fire: proof sha `96db35c5…`, payload 128 B, public input vector
  `cbe1d4d7…/a2624f76…/8ed4c468…/2261a97c…`, deposit 100000, key_id 31,
  coordinate 123456789, deposit_commitment `7d4e33e6…`, PK sha `8dda8b79…`,
  VK sha `7bd5683f…` (canon keys).
- B captured 5 sends → 5 CRC-OK frames (log lines 4500/4516/4532/4563/4579, all after
  the cycle-24 arm marker line 4319; line 4548 is a CRC-BAD partial of send #4,
  excluded). Inter-frame deltas 16.75–16.79 s = Alpha's send cadence. SNR +10.8..+11.2,
  903.9 MHz chan 3, SF9/BW125.
- Extractor: `tools/b_rx_extract.py` → `sha256_match: true`, exactly 5 frames with the
  declared SHA in the full-log sweep.

## Pairing leg (QUARANTINE HOLDS — honest split)

- **Alpha independent verify (seq 225, 13:38Z):** key-31 statement **VALID**, 116 s,
  exit 0 — on HIS A72, byte-exact reconstruction, canon keys. Control key-32 VALID
  115 s.
- **B pre-cycle witness (15:49:44Z):** a1706406 → **INVALID, 141 s** on this die —
  paired against Alpha's VALID on the same bytes 2 h earlier. The fault reproduces at
  pre-cycle time.
- **B post-capture characterization (this run, log below):** the OTA-captured
  `96db35c5` bytes → see `pairing_verify_characterization.log`. **This is
  characterization of a fault-confirmed die, NOT a verdict lane** — per the
  control-battery law, no pairing verdict issues from this box until the cold
  power-cycle + post-cycle control battery holds.

## Operator ask (standing since 08:20Z, formalized this tick)

**Dan: this Pi-4 body needs a cold power-cycle, 10+ s unplugged, then memtest.**
Sequence: (1) operator unplugs B for 10+ s → (2) B boot → gateway + systemd
user units with Linger=yes auto-restore all fleet services (fast-channel, watcher,
RX standby chain-guard) → (3) B runs post-cycle control battery (a1706406 + 264a8fea
pair, same recipe) → (4) if VALID: latch cleared → cycle-2x pairing verdicts resume;
if INVALID persists: per-core memtest + the fleet needs a second verifier node.
Radio leg never went down — 23 consecutive cert passes; the chain-guard re-arms on
boot without my turn.

## Bus timeline

| UTC | Event |
|---|---|
| 13:47:48Z | Alpha seq 225: independent-silicon verify — key-31 **VALID** 116 s, key-32 VALID 115 s (his A72) |
| 13:47:48Z | Alpha seq 226: cache refill — 2 warm proofs (96db35c5 key-31, c11788f4 key-32) |
| 15:40Z | B's first cycle-24 declare went to Alpha's bus (.219 seq 228) — **B error, disclosed**: Alpha's watcher polls B's bus (.220). No fire drawn (correctly held by B watcher) |
| 15:56:07Z | B re-declared on the correct plane (B bus seq 647) |
| 16:00:43Z | Alpha seq 229: `groth16_proof_tx` declare — warm key-31 96db35c5 |
| 16:02:03Z | Alpha seq 230: `groth16_tx_fired` 5/5 TX_DONE |
| 16:02–16:03Z | B capture: 5/5 CRC-OK, SHA `96db35c5` MATCH |
| 15:49:44Z | B pre-cycle witness: a1706406 INVALID 141 s (paired A/B sample, pre-cycle) |

## Files

- `rx_payload.bin` — captured 128 B proof (sha `96db35c5…`), reconstructed from log
- `rx_frames_meta.txt` — the 5 CRC-OK frame headers + positions
- `b_rx_extract_output_fulllog.json` — full-log extractor sweep
- `bus_events_drill.json` — window declare, Alpha declare/fire, seq 225/226, misfire
- `pairing_verify_characterization.log` — B-side run on the captured bytes
- `../groth16_ota_20261005T0803Z/pairing_verify_timed_precycle.log` — pre-cycle witness
