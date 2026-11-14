# ZK-LoRa Milestone 1 — physical RF evidence repository (Bravo, Agent 05)

This repository is the **system of record** for the ZK-LoRa privacy layer's physical
RF evidence. One *cycle* = one real LoRa burst captured on a **RAK Miner v2**
(SX1302/SX1303, US915 **903.9 MHz**, SF9, 125 kHz, 128-byte payloads), gated by CRC
and SHA-256 on the receiving die, paired against a T12 battery verdict, then settled
and independently read back on **Solana devnet** against the Cuneiform program
`2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`.

Owner: **Researcher Bravo** (Agent 05 — receiver/verifier gateway).
Counterpart: **Researcher A** (Agent 04 — transmitter/prover node).

## Startup Workflow

1. `pwd` and `git branch --show-current` — confirm the intended branch.
2. Read this file completely.
3. Run `./init.sh` — environment + integrity gates. If it fails, repair it before adding scope.
4. Read `PROGRESS.md` — current state, in-progress work, next steps, blockers.
5. Read `cycle_registry.json` — machine-readable cycle status (the fleet's `feature_list.json` analog).
6. `git log --oneline -5` and `git status --short`.

## Working Rules

- **WIP = 1.** One cycle at a time. Finish and land the current cycle before opening the next.
- **Evidence before done.** A cycle is not done because code ran; it is done when the
  on-chain readback is PASS and the artifacts are in the repo.
- **Machine-read, never hand-type.** Transaction signatures, PDAs, bus URLs, slots and
  window timestamps are fetched from the API or parsed from artifacts — never typed by hand.
- **Update docs in the same commit** as the code change — no stale documentation.
- **Atomic commits.** One logical operation per commit; no partial work.
- **Update `PROGRESS.md` and `cycle_registry.json` before ending a session.**

## Constraints (MUST / MUST NOT)

- **MUST** declare an RX window only through `python3 tools/declare_rx_window.py --cycle N`
  (tz-aware close, machine-parsed certificate, fail-closed, dual-bus readback, idempotent).
- **MUST NOT** hand-type bus event URLs, TX signatures, PDAs or slots.
- **MUST NOT** publish a claim that no artifact supports (no fabricated CRC values, no
  synthetic benchmark answers, no "replayed" verdict that was never re-captured over the air).
- **MUST NOT** merge a PR. The operator merges. Open the PR, post the evidence, stop.
- **MUST NOT** accept or transmit passwords in chat. Operations are unprivileged or key-based.
- **MUST** post the stage-2 bus readback for every landed cycle (landed + stage2, byte-equal
  on both buses) and commit the raw readback JSON into the cycle's evidence directory.
- **MUST** run `./init.sh` and record its result in `PROGRESS.md` before claiming done.
- **MUST** record `tx`, `pda`, `slot`, `pr` and `evidence` for the cycle in `cycle_registry.json`.

## Verification Commands

```bash
# Full gate — run before every commit and before claiming done
./init.sh

# Component gates (also executed by init.sh)
python3 tools/test_b_rx_extract.py          # -> UNIT TEST: PASS
python3 tools/test_t12_battery_template.py  # -> T12 EXIT-CONTRACT UNIT TEST: PASS
python3 -m compileall -q tools/             # syntax gate
```

Per-cycle runtime gates (evidence artifacts, not unit tests):

```bash
python3 tools/b_rx_extract.py --log <cycle>_session_slice.log --out b_rx_extract_output.json
python3 tools/t12_battery_template.py --log t12_cycle<N>_battery_attempt1.log   # exit 0 = VALID
python3 tools/chain_readback_v2.py --tx <register_tx> --pda <record_pda>          # verdict PASS
```

## Definition of Done — three layers (do not stop early)

| Layer | Gate | Evidence |
|-------|------|----------|
| **L1 — static** | `compileall` clean, both unit suites PASS | terminal output |
| **L2 — runtime** | real RX capture: 5/5 CRC-OK, `sha256_match` true, T12 battery `BATTERY_EXIT=0` with PRIMARY + controls VALID | evidence dir artifacts |
| **L3 — system confirmation** | devnet RPC readback verdict PASS (session/coords/merkle/authority byte-match), dual-bus byte-equal stage-2, PR open with evidence linked | readback JSON + bus raw + PR URL |

**All three layers must pass.** Unit tests passing is *not* task completion.

## End of Session (clock-out)

1. Update `PROGRESS.md` (Current State: commit hash + verification result + next steps).
2. Update `cycle_registry.json` with the cycle's final status and evidence pointers.
3. Record unresolved risks/blockers.
4. Commit once the work is in a safe state (atomic message, explain **why**).
5. Leave the repo restartable: `./init.sh` must pass for the next session.

## Escalation

- Architecture/settle-design questions → Cuneiform program owner (`solana-cuneiform-milestone1`).
- Unclear requirements → check `cycle_registry.json` + `PROGRESS.md` before asking the operator.
- Repeated gate failures → record in `PROGRESS.md` Blockers and flag for human review.
- RF/HAL issues → `docs/` and the `rak-miner-v2-radio` / `rak-sx1302-lora-bringup` skill references.
