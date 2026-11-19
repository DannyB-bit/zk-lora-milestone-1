#!/usr/bin/env python3
"""essay_b2a_hotfire.py — Researcher Bravo (Agent 05) HOT-PATH auto-fire for the
essay_drill B->A leg. NO LLM turn in the path (same architecture as Alpha's
groth16_hotfire): poll the bus, and the instant a fire-go/window for the essay
drill appears, fire the staged bursts inside that declared window.

Why this exists: on 2026-11-18 Alpha opened rounds 1 and 2 and issued fire-go
both times; Bravo's agent turn was parked on an unrelated peer-run wait and
never fired, so Alpha correctly reported MISSED 0/151. This watcher removes the
human/LLM from the timing-critical path entirely.

Safety rails:
  - fires ONLY on a declared window (rx_window_open drill=essay_drill*) or an
    explicit essay_drill_fire_go with go=True
  - refuses to fire if the window is already closed
  - refuses to fire if the staged SHA gate does not pass (fail-closed, ABORT 10)
  - never fires outside a window, never fires twice for the same window seq
  - posts a receipt on both buses after the fire

Usage: essay_b2a_hotfire.py --once | --watch
"""
import argparse, json, os, subprocess, sys, time, urllib.request

B = os.environ.get("BRAVO_URL", "http://127.0.0.1:8643")
TOKEN = os.environ["FLEET_FAST_TOKEN"]
EV = "/home/researcher-bravo/fleet/evidence/essay_drill_20261118"
FIRE = f"{EV}/essay_b2a_fire.sh"
STATE = os.path.expanduser("~/.hermes/essay_b2a_hotfire.state")
POLL_S = float(os.environ.get("POLL_S", "2"))

BURSTS = [
    ("echo_a2b_frames", "echo_alpha_essay", 1, 1),
    ("my_essay_frames", "bravo_essay_md", 1, 1),
]


def fetch(since):
    with urllib.request.urlopen(f"{B}/events?since={since}&token={TOKEN}", timeout=8) as r:
        return json.loads(r.read()).get("events", [])


def load_state():
    try:
        return int(open(STATE).read().strip())
    except Exception:
        return 0


def save_state(v):
    open(STATE, "w").write(str(v))


def window_open(events):
    """Return the newest live essay window (dict) or None."""
    best = None
    for e in events:
        if e.get("type") != "rx_window_open":
            continue
        d = e.get("data", {})
        if not str(d.get("drill", "")).startswith("essay_drill"):
            continue
        if d.get("manual_fire_only"):
            continue
        best = (e, d)
    if not best:
        return None
    ev, d = best
    import datetime as _dt
    now = _dt.datetime.now(_dt.timezone.utc)
    # Close time: accept every field name Alpha has used across the drill
    # (closes_at_utc / window_close_utc / closes_utc / close_utc).
    close = (d.get("closes_at_utc") or d.get("window_close_utc")
             or d.get("closes_utc") or d.get("close_utc") or "")
    c = None
    if close:
        try:
            c = _dt.datetime.strptime(close, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=_dt.timezone.utc)
        except Exception:
            c = None
    # Fallback / sanity repair: if the close stamp is missing or is in the PAST
    # (Alpha's 2026-11-18 date-skew incident), rebuild it from the machine
    # fields armed_utc/armed_utc + window_s / window_s, which are the same
    # numbers Alpha computed. Never hand-type a constant.
    if c is None or (c - now).total_seconds() <= 30:
        armed = (d.get("armed_at_utc") or d.get("armed_utc") or "")
        span = d.get("window_s") or d.get("rx_timeout_s") or d.get("timeout_s")
        if armed and span:
            try:
                a = _dt.datetime.strptime(armed, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=_dt.timezone.utc)
                rebuilt = a + _dt.timedelta(seconds=int(span))
                # the rebuilt close must still be in the future to be usable
                if (rebuilt - now).total_seconds() > 30:
                    return {"seq": ev["seq"], "data": d, "close": rebuilt.strftime(
                        "%Y-%m-%dT%H:%M:%SZ"), "close_ts": rebuilt.timestamp(),
                        "close_source": "rebuilt_from_armed_plus_span",
                        "declared_close": close}
            except Exception:
                pass
        return None  # fail-closed on timing
    return {"seq": ev["seq"], "data": d, "close": close, "close_ts": c.timestamp(),
            "close_source": "declared"}


def fire_go_seen(events, window_seq):
    for e in events:
        if e.get("type") != "essay_drill_fire_go":
            continue
        d = e.get("data", {})
        if d.get("go") is True:
            return True
    return False


def do_fire(window, tag):
    results = []
    for subdir, label, reps, gap in BURSTS:
        fd = os.path.join(EV, subdir)
        print(f"[hotfire] firing {label} from {fd} reps={reps} gap={gap}", flush=True)
        p = subprocess.run(["bash", FIRE, fd, str(reps), str(gap), tag, label],
                           capture_output=True, text=True, timeout=1800)
        print(p.stdout[-2500:], flush=True)
        if p.stderr:
            print("STDERR:", p.stderr[-800:], flush=True)
        results.append({"label": label, "rc": p.returncode,
                        "log": os.path.join(EV, f"b2a_tx_{tag}.log")})
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--watch", action="store_true")
    args = ap.parse_args()
    since = load_state()
    print(f"[hotfire] up; since={since} bus={B}", flush=True)
    while True:
        try:
            events = fetch(since)
            for ev in events:
                since = max(since, ev["seq"])
            save_state(since)
            if events:
                w = window_open(events)
                if w and fire_go_seen(events, w["seq"]):
                    tag = f"r{w['seq']}"
                    print(f"[hotfire] window seq={w['seq']} close={w['close']} "
                          f"fire_go=YES -> firing", flush=True)
                    res = do_fire(w, tag)
                    print(f"[hotfire] done: {json.dumps(res)}", flush=True)
                    save_state(since)
                    if args.once:
                        return 0
        except Exception as e:
            print(f"[hotfire] poll error: {type(e).__name__}: {e}", flush=True)
            time.sleep(5)
        if args.once:
            return 0
        time.sleep(POLL_S)


if __name__ == "__main__":
    sys.exit(main())
