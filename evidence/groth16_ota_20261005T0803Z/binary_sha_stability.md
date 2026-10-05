# Binary sha stability forensics — cycle-20 quarantine, 2026-10-05T13:4xZ

Question under test: could the key-31 statement-class INVALID flip be explained by a
changed verifier binary between yesterday's committed VALID runs and today's 9/9 INVALID?

## Measured (this session, this box)

- `~/fleet-repos/zk-lorawan/target/debug/zk_lorawan_prove`
- sha256: `a0c74748cdc135064969fcece7e39aa68815a5065623668c5708cc70b8c452dc`
- mtime: 2026-09-29 04:33:32 EDT (single build; never rebuilt since)

## Conclusion

The verifying binary is byte-identical across the entire drill history: the same
bytes that verified key-31 statements VALID on 2026-10-04 (PR#13/#14/#16/#17, and
05:2xZ on 10-05) returned INVALID 9/9 today for the whole class, interleaved with
key-32 `264a8fea` VALID 4/4 (+1 today in battery v6) — same binary, same canon keys
(PK `8dda8b79…` / VK `7bd5683f…` sha-guarded before/after every battery), same
literal args (committed recipes), cores 0–3 each pinned, env scrubbed, throttled
`0x0`.

Combined with battery v6's t+4.5 h persistence reproduction (cecbb8b8 INVALID
again / 264a8fea VALID again), the fault signature is a **mid-boot state change
on this Pi**: latched somewhere between 05:2x and 08:20Z, still latched at
13:28Z. A build/mtime change is excluded; disk keys are excluded (seed-42 regen
differential also INVALID); userspace DRAM is exonerated in the testable region
(memtester PASS, clean dmesg).

Prescribed discriminator: RakMiner-A's independent-silicon verify of the key-31
vectors (peer run `quarantine-verify-ask-20261005T1315Z`, Issue#1 comment
5991997023). His VALID ⇒ B cold power-cycle (10+ s unplugged) + full memtest;
his INVALID ⇒ protocol-level case, bisect the statement class.

Remedy on confirmed B-silicon fault: cold power-cycle — the one thing that
cannot be executed from inside this session (it would kill the agent and the
certified-hot RX chain-guard with it). Operator order required.
