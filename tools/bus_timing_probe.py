#!/usr/bin/env python3
"""bus_timing_probe.py — declare-to-fire timing derived ONLY from fleet bus stamps.

Law origin (cycle-80 Codex review, 2026-10-11): the c-80 headline metric used the
composer *invocation* stamp (capture_meta.json) as the declare time, but the
authoritative metric is bus-stamp-to-bus-stamp:

    declare-to-fire = ts(rx_window_open) -> ts(groth16_tx_fired)   [same window_seq]
    watcher-react   = ts(groth16_proof_tx) - ts(rx_window_open)

Reads BOTH buses (B: 127.0.0.1:8643, A: alpha), cross-checks stamps agree, and emits
JSON. Fail-closed: exits nonzero if the window, declare, or fire event cannot be
located on the B bus.

Usage:
  export FLEET_FAST_TOKEN=...
  python3 tools/bus_timing_probe.py --cycle 80 [--out evidence/.../bus_timing_v2.json]
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

B_BUS = os.environ.get("BRAVO_URL", "http://127.0.0.1:8643")
A_BUS = os.environ.get("ALPHA_URL", "http://192.168.1.219:8643")


def fetch_events(url):
    token = os.environ["FLEET_FAST_TOKEN"]
    with urllib.request.urlopen(f"{url}/events?token={token}", timeout=10) as r:
        return json.loads(r.read()).get("events", [])


def parse_ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def locate(events, cycle, b_window_seq=None):
    """Locate the window/proof/fire trio for a cycle.

    `b_window_seq`: on the A bus the mirrored proof/fire events carry the B-bus
    window seq (e.g. "1186"), not the local window event's seq — accept either.
    """
    window = proof = fired = None
    for e in events:
        d = e.get("data", {})
        if e.get("type") == "rx_window_open" and str(d.get("cycle")) == str(cycle):
            window = e
        elif e.get("type") == "groth16_proof_tx" and window is not None \
                and str(d.get("window_seq")) in {str(window["seq"]), str(b_window_seq)} \
                and proof is None:
            proof = e
        elif e.get("type") == "groth16_tx_fired" and window is not None \
                and str(d.get("window_seq")) in {str(window["seq"]), str(b_window_seq)} \
                and fired is None:
            fired = e
    return window, proof, fired


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    b_events = fetch_events(B_BUS)
    window, proof, fired = locate(b_events, args.cycle)
    if not (window and proof and fired):
        print(f"FAIL: could not locate window/proof/fire for cycle {args.cycle} on B bus",
              file=sys.stderr)
        return 1

    wt, pt, ft = (parse_ts(window["ts_utc"]), parse_ts(proof["ts_utc"]), parse_ts(fired["ts_utc"]))
    watcher_react_s = (pt - wt).total_seconds()
    declare_to_fire_s = (ft - wt).total_seconds()

    # Cross-bus check: the A-bus mirror must show the same three stamps, with its
    # proof/fire events referencing the B-bus window seq.
    a_events = fetch_events(A_BUS)
    a_window, a_proof, a_fired = locate(a_events, args.cycle, b_window_seq=window["seq"])
    cross_bus_stamps_agree = bool(
        a_window and a_proof and a_fired
        and a_window["ts_utc"] == window["ts_utc"]
        and a_proof["ts_utc"] == proof["ts_utc"]
        and a_fired["ts_utc"] == fired["ts_utc"]
    )

    report = {
        "derivation_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "bus_timing_probe.py",
        "cycle": args.cycle,
        "metric_definition": "declare-to-fire = ts(rx_window_open) -> ts(groth16_tx_fired), "
                             "both machine-stamped by the bus server; watcher-react = "
                             "ts(groth16_proof_tx) - ts(rx_window_open)",
        "b_bus": {
            "window_open_seq": window["seq"], "window_open_ts_utc": window["ts_utc"],
            "proof_tx_seq": proof["seq"], "proof_tx_ts_utc": proof["ts_utc"],
            "tx_fired_seq": fired["seq"], "tx_fired_ts_utc": fired["ts_utc"],
        },
        "watcher_react_s": watcher_react_s,
        "declare_to_fire_s": declare_to_fire_s,
        "cross_bus_stamps_agree": cross_bus_stamps_agree,
        "verdict": f"bus-stamp declare-to-fire = {declare_to_fire_s:.0f}s",
    }
    text = json.dumps(report, indent=1)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
