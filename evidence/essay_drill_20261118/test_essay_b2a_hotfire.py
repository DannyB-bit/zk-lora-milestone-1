#!/usr/bin/env python3
"""test_essay_b2a_hotfire.py — logic test for the hot-fire watcher.
NO AIRTIME: it exercises window detection against synthetic events only.
"""
import datetime as dt
import importlib.util, json, sys

spec = importlib.util.spec_from_file_location(
    "hf", "/home/researcher-bravo/fleet/evidence/essay_drill_20261118/essay_b2a_hotfire.py")
hf = importlib.util.module_from_spec(spec)
sys.modules["hf"] = hf
spec.loader.exec_module(hf)


def ev_window(seq, drill, close_in_s, **extra):
    close = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=close_in_s)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    d = {"drill": drill, "closes_at_utc": close}
    d.update(extra)
    return {"seq": seq, "type": "rx_window_open", "data": d}


def ev_go(seq):
    return {"seq": seq, "type": "essay_drill_fire_go", "data": {"go": True}}


results = []


def check(name, cond):
    results.append({"test": name, "ok": bool(cond)})
    print(("PASS " if cond else "FAIL ") + name)


# 1. live essay window IS detected
w = hf.window_open([ev_window(1, "essay_drill", 3600)])
check("live_essay_window_detected", w is not None and w["seq"] == 1)

# 2. expired window is REFUSED
w2 = hf.window_open([ev_window(2, "essay_drill", -600)])
check("expired_window_refused", w2 is None)

# 3. window closing in <30s is REFUSED
w3 = hf.window_open([ev_window(3, "essay_drill", 10)])
check("near_close_window_refused", w3 is None)

# 4. manual_fire_only window is REFUSED
w4 = hf.window_open([ev_window(4, "essay_drill", 3600, manual_fire_only=True)])
check("manual_fire_only_refused", w4 is None)

# 5. non-essay drill is ignored
w5 = hf.window_open([ev_window(5, "groth16_ota", 3600)])
check("other_drill_ignored", w5 is None)

# 6. no machine close time -> REFUSED (fail-closed on timing)
w6 = hf.window_open([{"seq": 6, "type": "rx_window_open", "data": {"drill": "essay_drill"}}])
check("missing_close_time_refused", w6 is None)

# 7. newest window wins
w7 = hf.window_open([ev_window(7, "essay_drill", 3600), ev_window(9, "essay_drill", 3600)])
check("newest_window_wins", w7 is not None and w7["seq"] == 9)

# 8. fire_go detection
check("fire_go_detected", hf.fire_go_seen([ev_go(10)], 10) is True)
check("no_fire_go_not_detected", hf.fire_go_seen([ev_window(11, "essay_drill", 3600)], 11) is False)

# 9. fire_go with go=False is not a fire_go
check("fire_go_false_ignored",
      hf.fire_go_seen([{"seq": 12, "type": "essay_drill_fire_go", "data": {"go": False}}], 12) is False)

# --- regression tests for the round-3 field shapes (real Alpha event A1489) ----
def ev_alpha_style(seq, close_date, armed_date, span):
    """Alpha's real rx_window_open shape: closes_utc + armed_utc + window_s."""
    return {"seq": seq, "type": "rx_window_open", "data": {
        "drill": "essay_drill", "round": 3, "freq_mhz": 903.9, "sf": 9, "bw_khz": 125,
        "window_s": span, "armed_utc": armed_date, "closes_utc": close_date}}


# A1489 exact shape (Alpha posted 2026-11-18 dates but the real UTC was 11-19):
# declared close is in the PAST -> watcher must rebuild from armed_utc + window_s
import datetime as _dt
_now = _dt.datetime.now(_dt.timezone.utc)
_skewed_armed = (_now - _dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
_skewed_close = (_now - _dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
w_skew = hf.window_open([ev_alpha_style(20, _skewed_close, _skewed_armed, 3600)])
check("alpha_closes_utc_field_parsed", w_skew is not None)
check("skewed_close_rebuilt_from_armed_plus_span",
      w_skew is not None and w_skew.get("close_source") == "rebuilt_from_armed_plus_span")

# Normal closes_utc in the future -> used directly
_ok_armed = (_now - _dt.timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
_ok_close = (_now + _dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
w_ok = hf.window_open([ev_alpha_style(21, _ok_close, _ok_armed, 3600)])
check("closes_utc_used_directly",
      w_ok is not None and w_ok.get("close_source") == "declared")

# closes_at_utc (Bravo's own composer field) still works
w_b = hf.window_open([ev_window(22, "essay_drill", 3600)])
check("closes_at_utc_still_works", w_b is not None and w_b.get("close_source") == "declared")

# A window whose armed+span is ALSO in the past must still be refused
_past_armed = (_now - _dt.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
_past_close = (_now - _dt.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
w_past = hf.window_open([ev_alpha_style(23, _past_close, _past_armed, 3600)])
check("fully_expired_alpha_window_refused", w_past is None)

ok = sum(1 for r in results if r["ok"])
out = {"passed": ok, "total": len(results), "results": results}
json.dump(out, open("/home/researcher-bravo/fleet/evidence/essay_drill_20261118/"
                    "hotfire_logic_test.json", "w"), indent=1)
print(json.dumps(out, indent=1))
sys.exit(0 if ok == len(results) else 1)
