# Vendored control payload — key-33 e6a6b296 (SAME key, DIFFERENT statement)

Vendored 2026-10-11T20:5xZ as part of PR#48 Codex remediation (P1 + P2).

- **payload**: `rx_payload_128b.bin` — sha256 `e6a6b296e5c56e33b1f711f7d8b61f65bdec34596b83559b7dc417ddda0e6f93`
- **source**: `git show origin/main:artifacts/milestone1/hardware_capture/groth16_rf/node-b-rx_20260930T074711Z/rx_groth16_proof_128b.bin` (blob `6b82efc44bbccb846ec445d48c6dd12fc7ad2e67`), byte-identical to the capture committed by merged PR#10 (2026-09-30).
- **declare**: B-bus seq 119 / A-bus seq 53, 2026-09-30T08:28:55Z — `private_key_id=33`, `deposit_value=100000`, pih[-1]=`2261a97c…` (DIFFERENT public-input vector from the cycle-84 primary: deposit 100002, pih[-1]=`8611d46f…`), cross-bus byte-equal on all VERIFY_FIELDS (machine-checked 2026-10-11).
- **known verdict**: VALID (PR#10, canon VK 7bd5683f… — same verifying key sha as today's GUARD).

## Why this directory exists

The cycle-84 battery labeled its primary `4b416048` "FIRST-OF-CLASS key-33" because the
prior key-33 payload was absent from the local evidence scan — absence treated as
first-of-class (exactly the fail-open Codex flagged as P1). A prior key-33 proof
existed all along (this one). The corrected claim: cycle-84 is the first proof of its
**full statement class** (key-33 + the deposit-100002 public-input vector) —
positively asserted against complete dual-bus history by the patched template —
and this payload now serves as the SAME-KEY different-statement regression control,
verified in the same session as the primary (see `t12_cycle84_battery.log`, CONTROL-samekey).
