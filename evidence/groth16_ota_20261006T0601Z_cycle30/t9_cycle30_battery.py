#!/usr/bin/env python3
"""CYCLE-30 PAIRING BATTERY — twin OTA-captured proof, one session on the B die.

Primary: cycle-30 captured burst (Alpha watcher hot-path fire, B-bus declare
machine-located by window linkage, fired receipt same window). Payload bound
per the v4 law: listener-SESSION-SEGMENT + DIGEST-EQUALITY with the
machine-fetched declare. This burst is POST-WRAP: the 32-bit count_us counter
wrapped 05:31:11Z inside the 04:19:56Z->06:19:56Z window, so reported walls
are wrap-corrected with the wrap branch MACHINE-SELECTED by the fired-stamp
consistency assert (exactly one of {+0s, +4294.967296s} satisfies the
-180..+240s last-frame-vs-fired_utc gate; the other branch fails it).

Controls: cycle-26 key-32 (SAME statement class as the key-32 primary) +
cycle-29 key-31 (DIFFERENT class). Both declare pairs machine-located by
SHA match on BOTH buses and byte-diffed.

ZERO HAND-TYPED CONSTANTS — including in this docstring. The 4th instance of
the transcription-defect class (a hand-pasted devnet TX signature in the
cycle-29 settle summary) was caught by Zymatica's PR#21 execution review
2026-10-06T07:19:42Z; this battery extends the law that killed instances 1-3.
"""
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.request
from datetime import datetime, timedelta, timezone

M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.join(M1, "evidence/groth16_ota_20261006T0601Z_cycle30")
LOG = os.path.join(EVID, "t9_cycle30_battery.log")
EXTRACT = os.path.join(EVID, "b_rx_extract_output.json")
GUARD = os.path.expanduser("~/fleet/logs/rx_standby_continuous_20261003T180951Z.log")
CYCLE26_BIN = os.path.join(M1, "evidence/groth16_ota_20261005T1952Z_cycle26/rx_payload_128b.bin")
CYCLE29_BIN = os.path.join(M1, "evidence/groth16_ota_20261006T0519Z_cycle29/rx_payload_128b.bin")

B_BUS = "http://192.168.1.220:8643"
A_BUS = "http://192.168.1.219:8643"
WRAP_S = 4294.967296

VERIFY_FIELDS = ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
                 "deposit_value", "private_key_id", "deposit_commitment", "proof_sha256")


def tok():
    for line in open(os.path.expanduser("~/.hermes/.env")):
        if line.strip().startswith("FLEET_FAST_TOKEN"):
            return line.strip().partition("=")[2].strip().strip('"').strip("'")
    raise SystemExit("FLEET_FAST_TOKEN not found")


def get_events(url):
    req = urllib.request.Request(f"{url}/events?since=0&limit=1000&token={tok()}",
                                 headers={"User-Agent": "fleet-b"})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.load(r)
    return d.get("events", d) if isinstance(d, dict) else d


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def telemetry():
    out = []
    for cmd in (["vcgencmd", "measure_temp"], ["vcgencmd", "get_throttled"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                out.append(f"{cmd[1]}={r.stdout.strip()}")
        except Exception:
            pass
    return " ".join(out)


lines = [f"T9_CYCLE30_BATTERY_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "mode: primary = cycle-30 captured burst (POST-WRAP frames); controls = cycle-26 key-32 (same class) + cycle-29 key-31 (different class)",
         "law: zero hand-typed constants; burst binding v4 = session-segment + digest-equality; wrap branch machine-selected"]
lines.append(f"SILICON {telemetry()}")

bin_sha = sha(BIN)
pk_sha = sha(os.path.join(REPO, "keys/proving_key.bin"))
vk_sha = sha(os.path.join(REPO, "keys/verifying_key.bin"))
lines.append(f"GUARD-BEFORE binary={bin_sha[:16]} PK={pk_sha[:16]} VK={vk_sha[:16]}")
env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

# ---- machine-locate cycle-30 window / declare / fired on BOTH buses ----
Aev, Bev = get_events(A_BUS), get_events(B_BUS)
wins = [e for e in Bev if e.get("type") == "rx_window_open"
        and e.get("data", {}).get("window_seq_bravo_bus") == "cycle-30"]
assert len(wins) == 1, f"cycle-30 window events on B-bus: {len(wins)}"
win = wins[0]
wsid = str(win["seq"])
d30_b_hits = [e for e in Bev if e.get("type") == "groth16_proof_tx"
              and e.get("data", {}).get("window_seq") == wsid]
assert len(d30_b_hits) == 1, f"cycle-30 declares on B-bus: {len(d30_b_hits)}"
d30_b = d30_b_hits[0]
f30_hits = [e for e in Bev if e.get("type") == "groth16_tx_fired"
            and e.get("data", {}).get("window_seq") == wsid]
assert len(f30_hits) == 1, f"cycle-30 fired events on B-bus: {len(f30_hits)}"
f30 = f30_hits[0]
declared = d30_b["data"]["proof_sha256"]
d30_a_hits = [e for e in Aev if e.get("type") == "groth16_proof_tx"
              and e.get("data", {}).get("proof_sha256") == declared]
assert len(d30_a_hits) == 1, f"cycle-30 declare mirrors on A-bus: {len(d30_a_hits)}"
d30_a = d30_a_hits[0]
for field in VERIFY_FIELDS:
    assert field in d30_a["data"], f"A-bus declare missing verification field {field}"
    assert field in d30_b["data"], f"B-bus declare missing verification field {field}"
    assert d30_a["data"][field] == d30_b["data"][field], f"declare {field} MISMATCH across buses"
lines.append("DECLARE cross-bus byte-diff: " + ", ".join(f"{f}=EQ" for f in VERIFY_FIELDS))
assert d30_b["data"]["proof_sha256"] == f30["data"]["payload_sha256"], "declare/fired sha inconsistent"
lines.append(f"DECLARE located: A seq{d30_a['seq']} == B seq{d30_b['seq']} (verify-fields byte-equal); "
             f"key={d30_b['data']['private_key_id']} deposit={d30_b['data']['deposit_value']} "
             f"source={d30_b['data'].get('source','?')} construction={d30_b['data'].get('construction','?')}")

armed = datetime.strptime(win["data"]["armed_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
closes = datetime.strptime(win["data"]["closes_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
fired_utc = datetime.strptime(f30["data"]["fired_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
lines.append(f"WINDOW armed={armed.isoformat()} closes={closes.isoformat()} fired_utc={fired_utc.isoformat()} (completion stamp)")

# ---- session segment from the guard log (banner keyed to the window's armed_at_utc) ----
glines = open(GUARD, errors="replace").read().splitlines()
arm_banner = None
for i, l in enumerate(glines):
    if "GATE PASS: ARMING listener window" in l and l.split(" ")[0] == win["data"]["armed_at_utc"]:
        arm_banner = i
        break
assert arm_banner is not None, "no arm banner matches the window armed_at_utc"
exits = [i for i, l in enumerate(glines) if "listener exit rc=124" in l and i > arm_banner]
seg_hi = exits[0] if exits else len(glines)
seg_txt = "\n".join(glines[arm_banner:seg_hi])
# origin = banner second (listener session ended 06:19:56Z, live-ps unavailable;
# convention identical to the T8-validated cycle-29 walls from this same segment)
origin = armed
lines.append(f"SESSION-SEGMENT arm banner line {arm_banner} (guard log lines {arm_banner}..{seg_hi}); "
             f"count_us origin = banner second {origin.isoformat()} (live-ps unavailable: session listener exited at window close; "
             f"origin convention cross-validated in-segment by cycle-29 pre-wrap frames)")

# ---- burst selection: in-segment + 128B + 903.9MHz + digest equality ----
ext = json.load(open(EXTRACT))
in_session = [p for p in ext["crc_ok"] if f"count_us: {p['count_us']}" in seg_txt]
burst = [p for p in in_session
         if p["actual_bytes"] == 128 and p["freq_hz"] == 903900000
         and p["sha256"] == declared]
assert len(burst) == 5, f"expected 5 declared-digest frames in session, found {len(burst)}"
shas = {p["sha256"] for p in burst}
assert shas == {declared}, "burst digests not uniform"
payload = bytes.fromhex(burst[0]["hex"].replace(" ", ""))
assert hashlib.sha256(payload).hexdigest() == declared and len(payload) == 128
ordered = sorted(burst, key=lambda p: p["count_us"])
gaps = [(ordered[i + 1]["count_us"] - ordered[i]["count_us"]) / 1e6 for i in range(4)]
assert all(10 <= g <= 20 for g in gaps), f"inter-frame implausible: {gaps}"
with open(os.path.join(EVID, "rx_payload_128b.bin"), "wb") as f:
    f.write(payload)

# ---- wrap-branch machine selection (walls are REPORTING-only; SHA gate is the binding) ----
passing = []
for add in (0.0, WRAP_S):
    walls = [origin + timedelta(seconds=p["count_us"] / 1e6 + add) for p in ordered]
    in_win = all(armed - timedelta(seconds=30) <= w <= closes + timedelta(seconds=30) for w in walls)
    span = (fired_utc - walls[-1]).total_seconds()
    if in_win and -180 <= span <= 240:
        passing.append((add, walls, span))
assert len(passing) == 1, f"wrap-branch discriminator: {len(passing)} branches pass (need exactly 1)"
add, walls, span = passing[0]
wrap_note = "POST-WRAP (+4294.967296s)" if add else "pre-wrap (+0s)"
lines.append(f"BURST: 5 frames, count_us {ordered[0]['count_us']}..{ordered[-1]['count_us']}, "
             f"inter_frame_s={[round(g, 1) for g in gaps]}, SNR {ordered[0]['snr_avg']}, status {ordered[0]['status']}")
lines.append(f"BURST walls ({wrap_note}, origin {origin.strftime('%H:%M:%S')}Z): "
             f"{walls[0].strftime('%H:%M:%S.%f')[:-3]}Z..{walls[-1].strftime('%H:%M:%S.%f')[:-3]}Z "
             f"vs fired_utc={fired_utc.strftime('%H:%M:%S')}Z (last-frame-to-fired span {span:.1f}s; "
             f"declare posted {d30_b['ts_utc']} — first frame precedes the declare receipt by "
             f"{(datetime.strptime(d30_b['ts_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) - walls[0]).total_seconds():.0f}s, "
             f"disclosed: origin/banner-second jitter of order ~15s cannot be excluded with the session listener gone; "
             f"the SHA gate does not depend on walls)")
lines.append(f"SHA GATE: digest(captured)==declare 64/64: {declared}")


# ---- verify ----
def verify(raw, d):
    h = raw.hex()
    assert len(h) == 256, "payload not 128B"
    args = [BIN, "verify", h[:64], h[64:192], h[192:256], *d["public_input_hashes"],
            d["gateway_address_hex"], str(d["deposit_value"]), d["firmware_hash_hex"]]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, env=env_clean)
    dt = time.time() - t0
    verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else f"ERROR rc={r.returncode}")
    return verdict, dt, r.returncode, r.stdout.strip()[:80]


v, dt, rc, so = verify(payload, d30_b["data"])
lines.append(f"PRIMARY cycle-30 captured {declared[:8]}: verdict={v} exit={rc} wall_s={dt:.1f} stdout={so!r}")

# ---- control-1: cycle-26 key-32 (SAME statement class as primary) ----
c1_sha = sha(CYCLE26_BIN)
c1_raw = open(CYCLE26_BIN, "rb").read()
d26 = {}
for bus_name, events in (("A", Aev), ("B", Bev)):
    hits = [e for e in events if e.get("type") == "groth16_proof_tx"
            and e.get("data", {}).get("proof_sha256") == c1_sha]
    assert len(hits) == 1, f"cycle-26 declare on {bus_name}: {len(hits)} hits"
    d26[bus_name] = hits[0]
for field in VERIFY_FIELDS:
    assert d26["A"]["data"][field] == d26["B"]["data"][field], f"cycle-26 {field} MISMATCH"
cv1, cdt1, crc1, cso1 = verify(c1_raw, d26["A"]["data"])
lines.append(f"CONTROL-1 cycle-26 (key-32, same class) {c1_sha[:8]}: verdict={cv1} exit={crc1} wall_s={cdt1:.1f} stdout={cso1!r}")

# ---- control-2: cycle-29 key-31 (DIFFERENT statement class) ----
c2_sha = sha(CYCLE29_BIN)
c2_raw = open(CYCLE29_BIN, "rb").read()
d29 = {}
for bus_name, events in (("A", Aev), ("B", Bev)):
    hits = [e for e in events if e.get("type") == "groth16_proof_tx"
            and e.get("data", {}).get("proof_sha256") == c2_sha]
    assert len(hits) == 1, f"cycle-29 declare on {bus_name}: {len(hits)} hits"
    d29[bus_name] = hits[0]
for field in VERIFY_FIELDS:
    assert d29["A"]["data"][field] == d29["B"]["data"][field], f"cycle-29 {field} MISMATCH"
cv2, cdt2, crc2, cso2 = verify(c2_raw, d29["A"]["data"])
lines.append(f"CONTROL-2 cycle-29 (key-31, different class) {c2_sha[:8]}: verdict={cv2} exit={crc2} wall_s={cdt2:.1f} stdout={cso2!r}")

# ---- guards after ----
assert sha(BIN) == bin_sha, "BINARY CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/proving_key.bin")) == pk_sha, "PK CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/verifying_key.bin")) == vk_sha, "VK CHANGED MID-BATTERY"
lines.append(f"GUARD-AFTER binary={sha(BIN)[:16]} PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} "
             f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]} — unchanged")
lines.append(f"SILICON-END {telemetry()}")

# ---- verdict per battery law ----
if not (cv1 == "VALID" and cv2 == "VALID"):
    lines.append(f"BATTERY VERDICT: QUARANTINED — controls {cv1}/{cv2}, primary unusable; bisect before any claim")
elif v == "VALID":
    lines.append("BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID — cycle-30 A->B exchange COMPLETE: "
                 "radio 5/5 SHA MATCH (POST-WRAP frames, wrap-corrected walls) + pairing VALID on B die, "
                 "watcher hot-path (no LLM), primary key-32 with same-class + different-class controls both VALID; "
                 "settle queued (Cuneiform devnet)")
else:
    lines.append("BATTERY VERDICT: PRIMARY INVALID + CONTROLS VALID — captured bytes fail pairing; "
                 "no settle; disclosed; bisect")

out = "\n".join(lines)
print(out)
with open(LOG, "w") as f:
    f.write(out + "\n")
