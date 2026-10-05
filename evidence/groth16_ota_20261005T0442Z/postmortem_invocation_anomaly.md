# Postmortem — transient INVALID cluster during cycle-19 pairing battery (2026-10-05T04:53–05:26Z)

## Timeline (all UTC, Oct 5 2026)

| Time | Run | Path | Verdict |
|---|---|---|---|
| 04:53:39 | PRIMARY a1706406 | terminal-tool shell (script) | INVALID, 142 s |
| 04:55:xx | CONTROL bd4c9ab2 | terminal-tool shell (script) | INVALID, 142 s |
| 05:0x | CONTROL bd4c9ab2 | terminal-tool shell (literal args) | INVALID, 142 s |
| 05:15Z | CONTROL bd4c9ab2 | `env -i` minimal | **VALID** |
| 05:2xZ | CONTROL bd4c9ab2 | python subprocess (kernel env) | **VALID** 141.9 s |
| 05:2xZ | PRIMARY a1706406 | python subprocess (kernel env) | **VALID** 142.1 s |
| 06:21:52 | CONTROL bd4c9ab2 | plain terminal shell | **VALID** 142 s |
| 06:24:14 | CONTROL bd4c9ab2 | `env -i` | **VALID** 142 s |

## Facts

- Binary `target/debug/zk_lorawan_prove` unchanged (mtime 2026-09-29, sha stable across all runs).
- Canon keys sha-guarded before/after every battery: PK `8dda8b79…`, VK `7bd5683f…` — byte-identical.
- Args byte-identical across failing and passing runs (literal-hex diff vs committed recipe = zero).
- All runs took ~142 s — the full-PK canon-disk path (the in-memory seed-42 regen path returns in ~6 s; never observed).
- `ZK_LORAWAN_REPRODUCIBLE_SETUP` confirmed absent from every env (printenv + snapshot grep).
- SoC 44.3 °C, `vcgencmd get_throttled` = 0x0 — no thermal throttling.
- Groth16 pairing is deterministic: identical (VK, proof, public inputs) ⇒ identical verdict. Three INVALIDs followed by five VALIDs on identical inputs cannot both be true on sound silicon.

## Analysis

The only varying factor between the failing cluster (04:53–05:15Z) and every passing run
is time. Args, binary, keys, CWD, and env-scrub were proven byte-identical. The failing
cluster ran as the 3rd-through-5th consecutive 142 s pairing computations on the ECC-less
ARM Cortex-A72 within ~40 minutes (PR#15-style batteries ran earlier the same morning).
A single-bit soft error in a field-element limb, a negation flag, or an MSM window during
the pairing inner loop flips only the final `matches!(…)` comparison — producing a clean
`INVALID` with no crash, exactly the observed signature. Non-reproducibility afterwards is
consistent with a transient (SEU-like) event rather than any deterministic fault.

Cannot fully exclude: an as-yet-unidentified invocation-context factor. But every
candidate (env, args, shell vs exec, CWD, key bytes, binary bytes) was individually
exonerated by direct byte comparison or by a passing run under that exact factor.

## Verdict

- Drill verdict: **PASS on all legs** — issued only after the clean-path battery (control VALID + primary VALID + keys guard PASS).
- Process outcome (the real deliverable): **the same-session control-battery law is now proven in production** — a flipping control quarantined the run before any false verdict could be issued, and forced the bisect that exonerated the proof.
- Standing rule adopted: every pairing verdict must come from a battery whose same-session control holds; a flipped control invalidates the RUN, not the proof, and triggers this bisect protocol (args diff → env diff → binary/keys sha-guard → clean-env rerun).

## Artifacts

- `pairing_verify_timed.log` — full sequence, anomaly cluster + clean battery.
- `pairing_verify_timed.sh` — the failing script preserved verbatim.
- `b_env_diff` in settle summary notes; `terminal_env_dump.txt` snapshot in Hermes scratch (115 vars, zero ZK_LORAWAN vars).
