# cycle-78 corrections — Codex review PR #43 (2026-10-10T20:56Z), remediated 2026-10-11

Source: automated Codex review on the c-78 PR, 3×P2. Every finding re-derived from
live artifacts/buses before any edit (fleet law: verify the reviewer, then fix).

## P2-1 — commit the composer (`declare_rx_window.py`)

- **Finding**: the "durable tz-aware composer" closing the c-77 EDT-skew class had no
  tracked artifact — repo searches found only assertions inside the evidence README.
- **Fix**: `tools/declare_rx_window.py` is now committed (brought from the c-80 branch,
  where the same class finding was fixed first). The composer that produced
  `declare_c78.json` is now reviewable and runnable from a clean checkout.

## P2-2 — commit the battery control artifact (cycle-77 payload `a2da7dd7`)

- **Finding**: the T12 battery's CONTROL-diff was cycle-77's payload `a2da7dd7…`, but
  `groth16_ota_20261010T1804Z_cycle77/` (including its `rx_payload_128b.bin`) existed
  only on the c-77 branch — a clean checkout of THIS branch couldn't reproduce the
  battery or audit the control.
- **Fix**: merged the cycle-77 evidence branch into this branch (non-fast-forward,
  preserving its original commits). The battery's documented reproduction command now
  selects the true control from the tracked tree. Verified live: the c-77 payload SHA256
  re-hashes to `a2da7dd7737f574c47b0a8d4aa846603fa7016d48f3c7cf4c82d04109b37d138` and
  its devnet record PDA `FpYDe2qMPiWEHxFtu2vMDLUZRfYYEg32Dgkzoc8SPGJ3` passes the
  raw-byte `chain_readback_v2.py` probe (root at 62..94 byte-exact, slot 509778765).

## P2-3 — wrong event IDs in the capture verdict

- **Finding**: the committed `bus_events_drill.json` verdict lines cited `B442` (not a
  B-bus event) and mismatched pairs like `1154/A441`; the true same-type pairs are
  B1154/A440 (window), B1155/A441 (proof declare), B1157/A442 (fire).
- **Fix**: README Declare section rewritten with the correct same-type pairs and the
  bus-stamp-derived metric (80 s declare-to-fire, watcher react +0 s per
  `tools/bus_timing_probe.py --cycle 78`). The committed JSON verdict lines carry the
  historical event-pair typos; the corrected pairs are recorded here and in the README
  (the raw bus JSONL on each node remains the ground truth those lines paraphrase).

## Timing integrity (class check, same review family as c-80 P1)

- `tools/bus_timing_probe.py --cycle 78`: window open 20:27:50Z → proof declare +1 s
  → TX complete 20:29:10Z = **80 s** — the headline 80 s figure for c-78 was already
  bus-stamp-consistent. No change to the 4-fire streak (81/81/82/80).

## Settlement re-verification (live)

- `tools/chain_readback_v2.py` on PDA `8y8TBKWMT4kJE6X561ih5bbA6tMNznXo6AZwwh2kUWg4`:
  session ASCII `154750eb50ff6008`, coords `[124,33,233,4,70,122]`, root
  `154750eb50ff6008…d6a8` raw 32 B at offset 62..94 — **ALL PASS** (slot 509778715).
