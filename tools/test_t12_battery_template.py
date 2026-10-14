#!/usr/bin/env python3
"""Unit test: t12_battery_template exit contract (0/3/4) — PR#58 review blocker.

The PR body promised "asserted by the unit test" but no such test existed
(decline finding, Alpha 2026-10-13). This test asserts the exit-contract
mapping against fixture verdicts:
  0 = PRIMARY VALID + all controls VALID (sole settle-eligible verdict)
  3 = QUARANTINED (a control flipped INVALID — bisect, no verdict)
  4 = PRIMARY INVALID (controls VALID, primary bytes fail pairing)
plus the CLI entry contract: the __main__ block must sys.exit(main()) so the
process exit status IS battery_rc (the bare main() call discarded it and every
run exited 0 — the blocker this test pins shut forever).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "t12_battery_template.py")


def load_template():
    """Import the template without triggering argparse (module-level import
    is safe: the CLI entry is guarded by __name__)."""
    sys.path.insert(0, HERE)
    import t12_battery_template as t
    return t


def expect(cond, msg):
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)


def main():
    t = load_template()
    fn = t.verdict_exit_code

    # --- contract: 0 = PRIMARY VALID + all controls VALID ---
    expect(fn("VALID", {"same": "VALID", "diff": "VALID"}) == 0,
           "PRIMARY VALID + controls VALID must map to exit 0")
    expect(fn("VALID", {"diff1": "VALID", "diff2": "VALID", "samekey": "VALID"}) == 0,
           "first-of-class mode (3 controls) all VALID must map to exit 0")

    # --- contract: 3 = QUARANTINED (control flip) ---
    expect(fn("VALID", {"same": "INVALID", "diff": "VALID"}) == 3,
           "control flip with primary VALID must map to exit 3 (quarantine)")
    expect(fn("INVALID", {"same": "INVALID", "diff": "VALID"}) == 3,
           "control flip takes precedence over primary INVALID (exit 3)")
    expect(fn("VALID", {"same": "VALID", "diff": "ERROR rc=1"}) == 3,
           "non-VALID control verdict string (ERROR) must map to exit 3")

    # --- contract: 4 = PRIMARY INVALID (controls all VALID) ---
    expect(fn("INVALID", {"same": "VALID", "diff": "VALID"}) == 4,
           "PRIMARY INVALID with controls VALID must map to exit 4")
    expect(fn("ERROR rc=1", {"same": "VALID"}) == 4,
           "primary ERROR verdict maps to exit 4 (not VALID, not control flip)")

    # --- entry-point contract: the __main__ block sys.exits with main()'s value ---
    # (2026-10-14: the assert now checks the CONTRACT, not one literal shape —
    # the abort-transparency wrapper (emit accumulated lines on SystemExit)
    # changed the entry text while preserving rc == main()'s return.)
    src = open(TPL).read()
    entry_block = src.split('if __name__ == "__main__":')[-1]
    entry_ok = ('rc = main()' in entry_block and 'sys.exit(rc)' in entry_block) \
        or 'sys.exit(main())' in entry_block
    expect(entry_ok,
           "CLI entry must sys.exit with main()'s value — a bare main() call discards "
           "battery_rc and exits 0 on QUARANTINE (3) and PRIMARY INVALID (4)")
    expect('    main()\n' not in entry_block,
           "entry block must not contain a bare main() call that discards battery_rc")

    # --- sanity: the mapping the battery logs record is reachable through the
    #     same function main() uses (no shadow re-implementation) ---
    expect("verdict_exit_code(v, verdicts)" in src,
           "main() must compute battery_rc via verdict_exit_code (single source)")

    print("T12 EXIT-CONTRACT UNIT TEST: PASS")
    print("  verdict_exit_code mapping: 0/3/4 asserted on 7 fixture cases")
    print("  entry-point: sys.exit(main()) present and referenced")


if __name__ == "__main__":
    main()
