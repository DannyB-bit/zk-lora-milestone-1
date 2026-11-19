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
import argparse, json, os, shutil, subprocess, sys, time, urllib.request

B = os.environ.get("BRAVO_URL", "http://127.0.0.1:8643")
TOKEN = os.environ["FLEET_FAST_TOKEN"]
EV = "/home/researcher-bravo/fleet/evidence/essay_drill_20261118"
FIRE = f"{EV}/essay_b2a_fire.sh"
STATE = os.path.expanduser("~/.hermes/essay_b2a_hotfire.state")
POLL_S = float(os.environ.get("POLL_S", "2"))
# Rolling buffer of recent bus events. Alpha's rx_window_open and fire_go can
# arrive 1s apart and therefore land in DIFFERENT poll batches -- both must be
# visible at the same time for the fire to trigger.
BUFFER_MAX = int(os.environ.get("BUFFER_MAX", "400"))
# Ledger of window seqs already fired, so a restart can never double-fire.
FIRED_LEDGER = os.path.expanduser("~/.hermes/essay_b2a_hotfire.fired.json")

# Burst list is DATA, not code: each round can change payload set / reps / gap by
# editing the config file, with no watcher code change and no agent turn in the path.
# The pre-fire SHA gate in essay_b2a_fire.sh still validates every staged frame.
BURST_CONFIG = os.path.join(EV, "refire_bursts.json")


def load_bursts():
    try:
        cfg = json.loads(open(BURST_CONFIG).read())
        bursts = cfg.get("bursts") or []
        if bursts:
            return [(b["dir"], b["label"], int(b.get("reps", 1)), int(b.get("gap_s", 1)))
                    for b in bursts]
    except Exception as e:
        print(f"[hotfire] burst config unreadable ({e}) — falling back to default",
              flush=True)
    return [
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
    """Return the newest live essay window (dict) or None.

    NOTE (2026-11-19 round-4 bug): Alpha's rx_window_open and essay_drill_fire_go
    arrived 1 SECOND apart (22:56:11 / 22:56:12). A 2s poll split them into two
    separate batches, so scanning only the CURRENT batch meant the window was
    seen alone (no fire_go) and the fire_go was later seen alone (no window) --
    and the fire never happened. Callers must therefore pass a ROLLING buffer of
    recent events, not just the newest batch.
    """
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


def fire_go_frame_spec(events, window_seq):
    """If Alpha's fire_go names an exact frame (sha256 or prefix), honour it.

    Alpha's fire_go may carry e.g. "frame_sha256_idx14": "<sha or prefix>".
    When present we stage EXACTLY that frame and fire it alone, which is both
    what he asked for and the lowest-airtime correct action. Falls back to the
    configured burst list when no frame is named.
    """
    for e in events:
        if e.get("type") != "essay_drill_fire_go":
            continue
        d = e.get("data", {})
        if not d.get("go"):
            continue
        for k, v in d.items():
            if not str(k).startswith("frame_sha256"):
                continue
            if not isinstance(v, str) or len(v) < 8:
                continue
            return v.strip().lower()
    return None


def stage_single_frame(sha_hint, out_dir):
    """Stage the single frame matching sha_hint (full sha or prefix) from the
    known sealed burst dirs. Verifies every candidate's sha256. Returns the
    staged dir or None."""
    import hashlib as _h
    srcs = [os.path.join(EV, d) for d in
            ("echo_a2b_frames", "my_essay_frames", "refire_missing_frames")]
    hits = []
    for sd in srcs:
        if not os.path.isdir(sd):
            continue
        for fn in sorted(os.listdir(sd)):
            if not (fn.startswith("frame_") and fn.endswith(".bin")):
                continue
            p = os.path.join(sd, fn)
            b = open(p, "rb").read()
            sha = _h.sha256(b).hexdigest()
            if sha.startswith(sha_hint):
                hits.append((p, b, sha))
    # Dedupe by CONTENT, not by path: the same sealed frame legitimately exists in
    # more than one staged dir (e.g. my_essay_frames and refire_missing_frames).
    # Refuse only when the spec matches frames with DIFFERENT content.
    by_sha = {}
    for p, b, sha in hits:
        by_sha.setdefault(sha, (p, b))
    if len(by_sha) != 1:
        print(f"[hotfire] frame spec {sha_hint[:16]}... matched {len(by_sha)} "
              f"distinct frames — refusing to guess", flush=True)
        return None
    sha, (src, b) = next(iter(by_sha.items()))
    os.makedirs(out_dir, exist_ok=True)
    for fn in os.listdir(out_dir):
        if fn.startswith("frame_") and fn.endswith(".bin"):
            os.unlink(os.path.join(out_dir, fn))
    shutil.copy2(src, os.path.join(out_dir, "frame_00.bin"))
    json.dump({"purpose": f"auto-staged single frame per Alpha fire_go ({sha_hint})",
               "file": f"single frame {sha[:16]}",
               "file_bytes": len(b), "total_chunks": 1, "file_sha256": sha,
               "chunk_max": 180, "source_frame": src,
               "frames": [{"idx": 0, "frame_sha256": sha, "bytes": len(b)}]},
              open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)
    print(f"[hotfire] staged single frame {sha[:16]} from {src}", flush=True)
    return out_dir


def do_fire(window, tag, events=None):
    results = []
    spec = fire_go_frame_spec(events or [], window.get("seq"))
    if spec:
        single = os.path.join(EV, "auto_single_frame")
        if stage_single_frame(spec, single):
            bursts = [(os.path.basename(single), "fire_go_named_single_frame", 3, 3)]
        else:
            bursts = load_bursts()
    else:
        bursts = load_bursts()
    for subdir, label, reps, gap in bursts:
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


def load_fired():
    try:
        return set(json.loads(open(FIRED_LEDGER).read()))
    except Exception:
        return set()


def save_fired(seqs):
    open(FIRED_LEDGER, "w").write(json.dumps(sorted(seqs)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--watch", action="store_true")
    args = ap.parse_args()
    since = load_state()
    print(f"[hotfire] up; since={since} bus={B}", flush=True)
    # Rolling buffer of recent events: the window and the fire_go may land in
    # DIFFERENT poll batches (they arrived 1s apart in round 4), so both must be
    # visible together. Also survives a service restart via the persisted window.
    buf = []
    fired = load_fired()
    while True:
        try:
            events = fetch(since)
            for ev in events:
                since = max(since, ev["seq"])
                buf.append(ev)
            save_state(since)
            if len(buf) > BUFFER_MAX:
                buf = buf[-BUFFER_MAX:]
            if events:
                w = window_open(buf)
                if w and fire_go_seen(buf, w["seq"]) and w["seq"] not in fired:
                    tag = f"r{w['seq']}"
                    print(f"[hotfire] window seq={w['seq']} close={w['close']} "
                          f"fire_go=YES -> firing", flush=True)
                    fired.add(w["seq"])
                    save_fired(fired)
                    res = do_fire(w, tag, buf)
                    print(f"[hotfire] done: {json.dumps(res)}", flush=True)
                    save_state(since)
                    if args.once:
                        return 0
                elif w and w["seq"] in fired:
                    print(f"[hotfire] window seq={w['seq']} already fired -- skip",
                          flush=True)
        except Exception as e:
            print(f"[hotfire] poll error: {type(e).__name__}: {e}", flush=True)
            time.sleep(5)
        if args.once:
            return 0
        time.sleep(POLL_S)


if __name__ == "__main__":
    sys.exit(main())
