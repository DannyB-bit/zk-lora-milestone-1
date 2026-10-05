# groth16_ota BATCH VERIFY — twin OTA-captured proofs, one session (2026-10-05T23:15Z arm)

**First multi-proof batch verification battery on the B die.** Both of Alpha's
autonomous watcher-fired, over-the-air-captured Groth16/BN254 proofs verified
back-to-back in a single session, with every public-input field machine-parsed
and byte-diffed across BOTH fleet buses before the runs.

## Verdict

```
cycle-24 96db35c5 (key-31, deposit 100000): VALID  exit=0  wall_s=142.2
cycle-26 c11788f4 (key-32, deposit 100001): VALID  exit=0  wall_s=142.3
GUARD-BEFORE/AFTER binary=a0c74748cdc13506 PK=8dda8b798458bb5b VK=7bd5683f13f35847 (unchanged)
BATCH VERDICT: 2/2 VALID
```

Both proofs are already individually committed VALID on earlier legs (T5 re-issue
in PR#18 `f977d73`, T6 in PR#19 `a928977`); this battery re-executes them as a
**same-session pair in which each proof is the other's control** (different
statement classes per the control-rotation law) — the batch-throughput lane the
gateway needs when multiple field nodes fire concurrently.

## Provenance chain (all machine-derived, zero hand transcription)

- Payloads: the committed OTA capture files themselves —
  `../groth16_ota_20261005T1602Z/rx_payload.bin` (cycle-24) and
  `../groth16_ota_20261005T1952Z_cycle26/rx_payload_128b.bin` (cycle-26);
  SHA256 computed at run time, never typed.
- Declares: located programmatically by exact SHA match on each bus —
  cycle-24: A-bus seq 229 == B-bus seq 648; cycle-26: A-bus seq 233 == B-bus seq 663.
- Byte-diffed across buses before the runs: `public_input_hashes`,
  `gateway_address_hex`, `firmware_hash_hex`, `deposit_value`, `proof_sha256`,
  `private_key_id` — all equal.
- Binary/keys sha-guarded before AND after the battery (law: a mid-battery flip
  quarantines the run).

## Honest ledger

- **v1 of this battery died on its own fail-closed assert before any pairing ran**:
  it carried a hand-typed expected-SHA constant for cycle-24 that differed from the
  actual evidence-file SHA by one character (`…294f9ba…` vs `…94f9ba…`). Same defect
  class as yesterday's key-31 vector typo — proof that the machine-parse-or-die law
  needs to apply to *every* constant in the lane, not just public-input vectors.
  v2 eliminates all hand-typed constants (SHA computed from file, declare found by
  exact match, all fields byte-diffed). v1's aborted output is the traceback in the
  operator log; the assert fired at 0 pairing cost.
- Cycle-27 live-fire window was declared (B-bus seq 678, closes 2026-10-06T00:18:55Z);
  Alpha's watcher answered in 2 s with `groth16_cache_empty` (A-bus seq 238) — his
  cache is spent after cycles 24+26 and refill needs his agent lane, idle since
  13:47Z. Fail-closed behaved exactly as designed: no legacy misfire.

## Reproduce

```bash
python3 evidence/groth16_ota_batch_verify_20261005T2315Z/batch_verify_twin_ota.py
# requires: fleet buses reachable (A .219:8643, B .220:8643), zk-lorawan repo with
# canon keys (VK sha 7bd5683f13f35847…) and debug binary (sha a0c74748cdc13506…)
```
