# cycle-79 corrections — Codex review PR #44 (2026-10-10T22:58Z), remediated 2026-10-11

Source: automated Codex review on the c-79 PR, 1×P2 (missing control artifact).
Re-derived from live buses before any edit (fleet law: verify the reviewer, then fix).

## P2 — commit the battery control artifact (cycle-78 payload `154750eb`)

- **Finding**: the T12 battery's CONTROL-diff was cycle-78's payload `154750eb…`, but
  `groth16_ota_20261010T2005Z_cycle78/` existed only on the c-78 branch — a clean
  checkout of THIS branch couldn't reproduce the battery or audit the control.
- **Fix**: merged the (remediated) cycle-78 branch into this one — brings the c-78
  payload + declaration evidence AND, via the stacked merge, the cycle-77 control
  (`a2da7dd7`) that the c-78 battery used. The battery's reproduction command now
  selects the true control from the tracked tree.

## Timing correction (same invocation-stamp class the c-80 review exposed)

- **Claim was**: 79 s declare-to-fire (composer invocation 22:37:16Z → TX complete
  22:38:35Z) — "fastest hot-path yet".
- **Bus ground truth** (`tools/bus_timing_probe.py --cycle 79`, both buses agree):
  window open B1168/A447 **22:37:15Z** → proof declare B1169/A448 22:37:16Z (+1 s)
  → TX complete B1171/A449 22:38:35Z = **80 s declare-to-fire**, not 79.
- **Impact**: streak line corrects to **81/81/82/80/80** — the "fastest yet" claim is
  retracted; c-78's 80 s stands as the floor. All five remain 80 s-class.

## Settlement re-verification (live)

- `tools/chain_readback_v2.py` on PDA `EVLHYcRumzgBzvHiiNuvUmayimstsNerexgnYKf3UyJA`:
  session ASCII `0241669ab1938fe4`, coords `[229,46,124,107,81,23]`, root
  `0241669ab1938fe4…9030` raw 32 B byte-exact at Anchor offset 62..94 — **ALL PASS**
  (slot 509778660). The v1 readback on this branch proved signature existence only;
  the raw-byte probe is the new class standard (tools committed with this merge).

## Composer + probes

- `tools/declare_rx_window.py`, `tools/bus_timing_probe.py`, `tools/chain_readback_v2.py`
  now tracked on this branch via the same merge (closes the untracked-composer class
  finding raised on PR #43 for this branch family).
