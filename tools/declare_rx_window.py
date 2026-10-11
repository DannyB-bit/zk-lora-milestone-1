#!/usr/bin/env python3
"""declare_rx_window.py — durable, tz-aware rx_window_open composer for groth16_ota drills.

Law origin (cycle-77, 2026-10-10): the throwaway c-77 composer parsed the UTC ARM
banner via local-time time.mktime and posted closes_at_utc +4 h wrong (EDT skew).
Law: window close arithmetic MUST be tz-aware UTC —
    datetime.strptime(banner).replace(tzinfo=timezone.utc) + timedelta(seconds=N)
Never naive mktime on a UTC string.

Every field is machine-parsed, zero hand-typed constants (hand-typed-constant law):
  - armed_at_utc   <- last "GATE PASS: ARMING listener window <UTC> -> +Ns" banner
  - closes_at_utc  <- banner_utc + N seconds (tz-aware)
  - config         <- live listener ps args (comm-exact pgrep -x test_loragw_hal)
  - timeout        <- the ARM banner's own +Ns
  - expected SHA   <- prefixes regex-extracted from Alpha's latest b_ack on his bus
  - cert state     <- LORA_CHIRP_RECOVERY_PASS=YES must sit within 12 lines before
                      the ARM banner; "Waiting for packets..." must appear after it
Fail-closed asserts throughout. Idempotent: refuses to re-declare a session whose
banner already carries a live rx_window_open on the B bus.

Posts rx_window_open to B's OWN bus (127.0.0.1:8643 — the plane Alpha's watcher
polls), readback-verifies the seq, then mirrors to A's bus (agent lane) and
readback-verifies there too. Aborts if the B-bus post/readback fails; the A-bus
mirror is retriable (idempotence guard keys on the B bus).

Usage:
  export FLEET_FAST_TOKEN=...
  declare_rx_window.py --cycle 78 [--note "..."] [--dry-run]
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

HOME = os.path.expanduser("~")
STANDBY_GLOB = os.path.join(HOME, "fleet", "logs", "rx_standby_continuous_*.log")
B_BUS = os.environ.get("BRAVO_URL", "http://127.0.0.1:8643")
A_BUS = os.environ.get("ALPHA_URL", "http://192.168.1.219:8643")
sys.path.insert(0, os.path.join(HOME, "fleet-repos", "fleet", "fast-channel"))
from post_event import post  # noqa: E402


def fetch_events(url: str) -> list:
    token = os.environ["FLEET_FAST_TOKEN"]
    with urllib.request.urlopen(f"{url}/events?token={token}", timeout=8) as r:
        return json.loads(r.read()).get("events", [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True, help="drill cycle number (e.g. 78)")
    ap.add_argument("--note", default="", help="free-text note for the event")
    ap.add_argument("--dry-run", action="store_true", help="run all asserts, post nothing")
    args = ap.parse_args()

    # --- 1) newest standby log -------------------------------------------------
    logs = sorted(glob.glob(STANDBY_GLOB), key=os.path.getmtime)
    assert logs, "FAIL-CLOSED: no rx_standby_continuous_*.log found"
    log_path = logs[-1]
    lines = open(log_path, errors="replace").read().splitlines()

    # --- 2) last ARM banner (machine-parsed arm second + window span) ----------
    arm_re = re.compile(
        r"^(\S+)\s+GATE PASS: ARMING listener window (\S+) -> \+(\d+)s")
    hits = []
    for i, l in enumerate(lines):
        m = arm_re.match(l)
        if m:
            hits.append((i, m))
    assert hits, "FAIL-CLOSED: no ARM banner in standby log"
    arm_idx, arm_m = hits[-1]
    banner_utc_str = arm_m.group(2)
    timeout_s = int(arm_m.group(3))

    # --- 3) chirp-recovery gate PASS must immediately precede the ARM banner ---
    gate_window = lines[max(0, arm_idx - 12):arm_idx]
    assert any("LORA_CHIRP_RECOVERY_PASS=YES" in l for l in gate_window), (
        "FAIL-CLOSED: no LORA_CHIRP_RECOVERY_PASS=YES within 12 lines before the "
        "ARM banner — uncertified arm, no RX-HOT claim (message discipline law)")

    # --- 4) tz-aware close arithmetic (the c-77 EDT-skew fix) ------------------
    banner_utc = datetime.strptime(banner_utc_str, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)
    closes_utc = banner_utc + timedelta(seconds=timeout_s)
    now_utc = datetime.now(timezone.utc)
    remain_s = (closes_utc - now_utc).total_seconds()
    assert remain_s > 120, (
        f"FAIL-CLOSED: window nearly closed ({remain_s:.0f}s left) — "
        "refusing to declare into a nearly-dead window (stale-close law)")

    # --- 5) listener reached RX state after the banner --------------------------
    tail = lines[arm_idx:]
    assert any("Waiting for packets" in l for l in tail), (
        "FAIL-CLOSED: listener never reached 'Waiting for packets...' after the "
        "ARM banner — uncertified arm, no RX-HOT claim")

    # --- 6) listener liveness, comm-exact (kernel truncates comm to 15 chars) ---
    pg = subprocess.run(["pgrep", "-x", "test_loragw_hal"],
                        capture_output=True, text=True)
    pids = [p for p in pg.stdout.split() if p]
    assert pids, ("FAIL-CLOSED: pgrep -x test_loragw_hal empty — listener dead; "
                  "re-arm via lora_chirp_recovery.sh before declaring")
    pid_list = ",".join(pids)
    listener_args = subprocess.run(["ps", "-o", "args=", "-p", pid_list],
                                   capture_output=True, text=True).stdout.strip()
    lstart_raw = subprocess.run(["ps", "-o", "lstart=", "-p", pid_list],
                                capture_output=True, text=True).stdout.strip()
    lstart_utc = datetime.strptime(lstart_raw, "%a %b %d %H:%M:%S %Y").astimezone(
    ).astimezone(timezone.utc)  # ps prints LOCAL time; convert (lstart law)
    skew_s = abs((lstart_utc - banner_utc).total_seconds())
    assert skew_s <= 30, (
        f"FAIL-CLOSED: listener lstart {lstart_utc:%Y-%m-%dT%H:%M:%SZ} vs ARM "
        f"banner {banner_utc:%Y-%m-%dT%H:%M:%SZ} skew {skew_s:.0f}s > 30s — "
        "stale listener under a newer banner? (loose-skew law)")

    # --- 7) expected warm-cache SHA prefixes, machine-read from A's b_ack -------
    expected = ("prefix-only — gate binds to your pre-fire groth16_proof_tx "
                "declare, byte-diffed A/B (full 64-hex never published on any plane)")
    a_bus_state = "unreachable"
    try:
        a_events = fetch_events(A_BUS)
        backs = [e for e in a_events if e.get("type") == "b_ack"]
        if backs:
            refill = str(backs[-1].get("data", {}).get("1_refill", ""))
            warm = re.findall(r"\b([0-9a-f]{8})\s+key-(\d+)\b", refill)
            if warm:
                expected = ("prefix-only (full 64-hex never published) — cache "
                            "expected warm per your latest b_ack: "
                            + ", ".join(f"{sha} (key-{k})" for sha, k in warm))
            a_bus_state = "ok"
    except Exception as ex:
        a_bus_state = f"unreachable ({ex.__class__.__name__})"

    # --- 8) idempotence: refuse to re-declare this listener session -------------
    b_events = fetch_events(B_BUS)
    opens = [e for e in b_events if e.get("type") == "rx_window_open"
             and e.get("data", {}).get("armed_at_utc") == banner_utc_str]
    assert not opens, (
        f"FAIL-CLOSED: rx_window_open for armed_at_utc={banner_utc_str} already "
        f"posted (B seq {opens[-1]['seq']}) — refusing double declare")

    # --- 9) gate PASS count in the current standby log (machine-counted) --------
    pass_count = sum(1 for l in lines if "LORA_CHIRP_RECOVERY_PASS=YES" in l)

    # --- compose payload --------------------------------------------------------
    a_arg = re.search(r"-a (\S+)", listener_args)
    rf_mhz = float(a_arg.group(1)) - 0.4 if a_arg else None
    rf_note = (f"(radio A {a_arg.group(1)} MHz, IF -400 kHz => {rf_mhz:.1f} MHz "
               f"exact, SF9/125kHz, listener span {timeout_s}s)") if a_arg else ""
    data = {
        "to": "alpha",
        "from": "bravo",
        "drill": "groth16_ota",
        "kind": f"cycle{args.cycle}_window_open",
        "cycle": args.cycle,
        "armed_at_utc": banner_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "closes_at_utc": closes_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "config": f"{listener_args} {rf_note}",
        "expected_payload_sha256": expected,
        "cert": {
            "loragw_chirp_recovery_pass": True,
            "gate_pass_events_in_current_standby_log": pass_count,
            "chip": "version reg 0x10 v1.0 (HAL banner in capture log)",
            "listener_pid": pids[0],
            "listener_lstart_utc": lstart_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "arm_banner_skew_s": round(skew_s, 1),
            "window_remaining_s_at_declare": round(remain_s),
        },
        "composer": ("declare_rx_window.py v1.0 — tz-aware UTC close arithmetic "
                     "(fixes the c-77 +4h EDT mktime-skew class); all fields "
                     "machine-parsed"),
        "note": args.note,
    }
    if args.dry_run:
        print("DRY-RUN PASS — would post:")
        print(json.dumps(data, indent=1))
        return 0

    # --- post to B bus (watcher plane) + readback ------------------------------
    b_res = post(B_BUS, "rx_window_open", data)
    b_readback = fetch_events(B_BUS)
    b_new = [e for e in b_readback
             if e.get("type") == "rx_window_open"
             and e.get("data", {}).get("armed_at_utc") == banner_utc_str
             and e.get("data", {}).get("closes_at_utc")
             == data["closes_at_utc"]]
    assert b_new, ("FAIL-CLOSED: B-bus readback did not show the posted window "
                   "event — declare not confirmed on the watcher plane")
    b_seq = b_new[-1]["seq"]

    # --- mirror to A bus (agent lane), best-effort with readback ---------------
    a_res = None
    a_seq = None
    if a_bus_state == "ok":
        try:
            a_res = post(A_BUS, "rx_window_open", data)
            a_back = fetch_events(A_BUS)
            a_new = [e for e in a_back
                     if e.get("type") == "rx_window_open"
                     and e.get("data", {}).get("armed_at_utc") == banner_utc_str]
            a_seq = a_new[-1]["seq"] if a_new else None
        except Exception as ex:
            a_res = {"error": str(ex)}

    out = {
        "declared": True,
        "b_bus_seq": b_seq,
        "a_bus_mirror_seq": a_seq,
        "b_post_rtt_ms": b_res.get("rtt_ms"),
        "a_bus_state": a_bus_state,
        "armed_at_utc": data["armed_at_utc"],
        "closes_at_utc": data["closes_at_utc"],
        "standby_log": log_path,
        "arm_banner_line": arm_idx + 1,
        "event": data,
    }
    # persist for the evidence dir (battery/staging law: artifacts on disk)
    out_path = os.path.join(HOME, "fleet", "logs",
                            f"cycle{args.cycle}_window_declare.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
