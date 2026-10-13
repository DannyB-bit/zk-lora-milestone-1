# cycle-80 corrections — Codex review PR #45 (2026-10-11T02:10Z), all remediated same day

Source: automated Codex review on commit `1a02659`, 2×P1 + 1×P2. Every finding was
re-derived from live artifacts before any edit (fleet rule: verify the reviewer, then fix).

## P1-1 — hot-path timing (README line 18)

- **Claim was**: declare 01:38:56Z → proof declare +30 s → TX done 01:40:46Z = 80 s.
- **Bus ground truth** (`bus_timing_v2.json`, machine-derived from both buses):
  - B1186/A455 `rx_window_open` posted **01:39:25Z**
  - B1188/A456 `groth16_proof_tx` posted **01:39:26Z** (+1 s, not +30 s)
  - B1189/A457 `groth16_tx_fired` (5/5 TX_DONE complete) **01:40:46Z**
  - declare-to-fire = **81 s**, not 80 s.
- **Root cause**: `01:38:56Z` is the composer *invocation* stamp recorded in
  `capture_meta.json` (start of `declare_rx_window.py`), ~29 s before the bus POST
  landed. The metric must be measured bus-stamp-to-bus-stamp.
- **Impact on streak**: 6-fire hot-path line corrects 80 → **81 s**
  (81/81/82/80/79/81). All six remain in the 80 s class; no verdict changes.

## P1-2 — chain readback (README line 50)

- **Claim was**: "machine-fetched byte-match PASS … raw 32 B root present".
- **Artifact ground truth**: `chain_readback.json` records
  `merkle_root_hex_in_account_bytes: false` — the probe searched for the 64-char
  **hex string** of the root inside raw account bytes. The program stores the root as
  **raw 32 bytes**, so that probe can only ever return false. The claim was not
  supported by the cited artifact.
- **Live re-verification** (`chain_readback_v2.json`, 2026-10-11T03:52Z,
  `getAccountInfo` on devnet RPC): account 103 B, program-owned, root byte-exact at
  Anchor offset 62..94, session ASCII at 40..56, coords raw at 56..62 — **ALL PASS**.
- **Verdict**: the settlement itself was sound; the readback *evidence* was
  structurally void. v1 superseded; README corrected to cite the raw-byte readback.
- **Class fix (all cycles)**: every cycle's readback now must probe raw 32 B at the
  Anchor layout offset, not a hex-string containment. Recorded as a class law.

## P2 — battery control provenance (settle_run.log line 21)

- **Claim was**: `SETTLE_VERIFIED` echoed "control-diff key-32 ff238e52".
- **Battery ground truth** (`t12_cycle80_battery.log`): executed CONTROL-diff was
  `c300e5b4` (key-32, c-70, machine-picked from committed evidence). `ff238e52` is
  Alpha's remaining **warm cache proof** (per his b_ack A454), never a battery control.
- **Root cause**: hand-written `SETTLE_VERIFIED` env var in `settle_cycle80.sh` named
  the cache proof instead of the executed control — a hand-typed-constant defect.
- **Fix**: README T12 section now names the executed control with provenance;
  class law: settle metadata must be machine-derived from the battery log, never
  hand-typed.

## Also fixed this pass (PR #43 / c-78 class findings, same review family)

- `declare_rx_window.py` committed to the repo (`tools/` — previously lived only in
  `~/fleet/scripts/`, so the "durable composer" claim had no committed artifact).

## Commands to reproduce the verifications

```
# bus timing (raw events from both buses, machine-stamped):
python3 tools/bus_timing_probe.py --cycle 80
# raw-byte chain readback:
python3 tools/chain_readback_v2.py --pda 4VtY6koUbfc5raGD6VnFjKbFrdXuZnGsGGX2FqfKdXVv \
  --expect-root aee2816a0a98fc4db4ff0e61e29c846a2945f4d50ede9e5e16c030c02223baa8 \
  --expect-coords 132,182,56,35,123,217 --expect-session aee2816a0a98fc4d
```
