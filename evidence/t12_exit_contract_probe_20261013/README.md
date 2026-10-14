# T12 exit-contract propagation probe — PR#58 review blocker, fixed + re-run

Reviewer decline (Alpha, 2026-10-13T14:07:45Z): the flagship P1 the PR exists to
close — the exit contract — was dead code as shipped: `main()` computed
`battery_rc` (0/3/4) and returned it, but the `__main__` block called `main()`
bare, discarding the value. Every run exited 0, including QUARANTINE (3) and
PRIMARY INVALID (4). Also: the PR body promised a unit test that did not exist.

## Fix (this branch)
1. `tools/t12_battery_template.py` entry is now `sys.exit(main())`.
2. The 0/3/4 mapping is extracted into `verdict_exit_code(primary, controls)`
   (pure function) and `main()` routes through it — single source, testable.
3. `tools/test_t12_battery_template.py` — the promised unit test: asserts the
   0/3/4 mapping on 7 fixture verdict cases AND the entry-point contract.
4. This probe: a REAL battery re-run through the fixed CLI whose controls
   flipped — the non-zero exit path propagated to the calling shell.

## The propagation proof (real silicon, real bus, real evidence)
- Invocation (machine-copied from the re-run log's own `invocation:` line):
  `python3 -u tools/t12_battery_template.py --cycle 97 --evidence-dir evidence/groth16_ota_20261013T1018Z_cycle97 --guard-log /home/researcher-bravo/fleet/logs/rx_standby_continuous_20261013T101811Z.log`
- Run UTC: 2026-10-13T18:53:37Z, RakMiner-B (Pi 4 A72), throttled=0x0.
- Result: `BATTERY VERDICT: QUARANTINED — a control flipped INVALID` and the
  calling shell observed `BATTERY_EXIT=3` (file: `exit_observation.txt`).
  Under the pre-fix template this exact run would have exited 0 — the exact
  failure mode the decline describes.

## Honest finding: the quarantine itself is an ERA MISMATCH, not silicon
The c-95/c-96/c-97 payloads are canon-era proofs (8-input circuit, canon VK
`7bd5683f…`, canon PK `8dda8b79…` — see the committed c-97 log's GUARD-BEFORE).
The zk-lorawan repo's on-disk keyset was rotated to the identity-era 10-input
setup (VK `78352ffa…`, PK `aea2ed17…`) during the RF identity-binding milestone
(2026-10-13 ~12:35–13:44Z). Verifying canon-era proofs under the identity-era
VK is deterministically INVALID — the re-run log's GUARD-BEFORE/AFTER lines pin
the era it actually ran under. No verdict was issued from this run (quarantine
= no verdict, per battery law); the committed c-97 PRIMARY VALID + CONTROLS
VALID verdict stands, era-pinned by its own log. This is the proof-era pinning
law (zk-lorawan PR#7 README) operating exactly as designed.

## Era-key lesson (new, fleet-relevant)
The T12 template verifies whatever `keys/` is on disk at run time. Post-keyset-
rotation, re-running ANY pre-rotation battery quarantines on era mismatch. The
GUARD-BEFORE line catches it (VK sha recorded), but the battery cannot know
which era a payload belongs to without era metadata on the declare. Follow-up
proposal: declare events and evidence READMEs should carry `vk_sha256` so the
battery can era-pin (fetch/expect the declared VK before pairing, like the
PR#8 review battery did via worktree pinning).
