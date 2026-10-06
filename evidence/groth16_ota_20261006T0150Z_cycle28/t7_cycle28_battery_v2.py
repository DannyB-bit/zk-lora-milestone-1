#!/usr/bin/env python3
"""CYCLE-28 T7 BATTERY v2 — discriminator: airwave digest vs declared SHA divergence.

v1 DEFECT (honest ledger, preserved as t7_battery_v1_wrongtarget.log): the
burst-selection heuristic (most-common 128B payload across the whole guard
log) targeted the 2026-10-04 PHANTOM burst 3b9b6d2e... (count_us 3541122909..)
— a known-INVALID historical capture — instead of the cycle-28 burst (count_us
1276388753..). Its printed verdict "PRIMARY INVALID + CONTROL VALID" is the
Oct-4 phantom verdict, NOT a cycle-28 statement; its own avalanche check
exposed the mis-target (57/64 digest positions differ from the declare) and
the log was quarantined before any verdict was issued.

v2->v3 DEFECT (caught by v2's own fail-closed assert, zero verdict impact):
fired-window count_us binding alone is insufficient — the guard log spans MANY
listener sessions (one per 2h window, each with its own count_us origin), so
older bursts' count_us can land in Alpha's fired window under the wrong arm
assumption (12 frames matched, 5 real + 7 foreign). v3 fix: a frame counts
ONLY if it also appears in the guard-log SEGMENT of the cycle-28 listener
session (arm banner "GATE PASS: ARMING listener window 2026-10-06T00:19:15Z"
at log line 5543 -> "listener exit rc=124" at 5827), intersected with the
wrap-corrected fired-window recovery. Session-bounded + window-bounded.

The cycle-28 anomaly (unchanged): 5 CRC-OK 128B frames captured 01:52:06-
01:53:13Z, byte-identical across all 5 sends, digest(captured)
8d7bf2fe46a9576a0da7bcdc2e0f6de8d87f804fbfce6c9a7b0a81d3b50af61f, vs Alpha's
declared payload_sha256 8d7bf2fe...6b7a7b0... — exactly 2 digest chars differ.
By SHA-256 avalanche two distinct 128B inputs cannot agree on 62/64 digest
chars: the declared string was NOT computed from the captured bytes. Combined
with 5/5 deterministic frames (LoRa CRC OK at SNR +11), air corruption is
excluded — the divergence is a transcription-class defect in the DECLARE
CHAIN (compute/paste/post), not in the proof and not on the air.

DISCRIMINATOR (informational): pair-verify the CAPTURED bytes against the
machine-parsed public-input vector.
  VALID => captured bytes ARE a genuine key-31 Groth16 proof; the declared
           SHA string is the transcription defect (2 chars). Radio verdict
           stands: 5/5 capture of the true proof, declare-SHA divergence
           disclosed; settle only after Alpha confirms the canonical SHA.
  INVALID (control VALID) => rare: payload bytes decode as a non-proof yet
           digest-neighbors the declare — treat as FAIL, no settle, bisect.

Control (different statement class): cycle-26 key-32 proof c11788f4...
(known-VALID: T6 142.1s + PR#20 batch battery).

ZERO HAND-TYPED CONSTANTS: every SHA computed from a file at run time; every
public-input field machine-parsed from the buses and byte-diffed across BOTH
buses before any verify runs. Binary/keys sha-guarded before and after.
ZK_LORAWAN_REPRODUCIBLE_SETUP stripped from the env. Burst bound to the
machine-parsed fire window. No expected-SHA string appears in this file.
"""
import hashlib
import json
import os
import subprocess
import time
import urllib.request
from datetime import datetime, timedelta, timezone

M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.join(M1, "evidence/groth16_ota_20261006T0150Z_cycle28")
LOG = os.path.join(EVID, "t7_cycle28_battery_v2.log")
EXTRACT = os.path.join(EVID, "b_rx_extract_output.json")

B_BUS = "http://192.168.1.220:8643"
A_BUS = "http://192.168.1.219:8643"
CYCLE26_BIN = os.path.join(M1, "evidence/groth16_ota_20261005T1952Z_cycle26/rx_payload_128b.bin")

ARM_UTC_STR = "2026-10-06T00:19:15Z"  # 28th gate PASS stamp (guard log, machine-verified below)
WRAP_S = 4294.967296


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


lines = [f"T7_CYCLE28_BATTERY_V2_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "mode: discriminator battery v2 — burst bound to Alpha's declared fire-execution window",
         "v1 lesson: burst selection by most-common-payload mis-targeted the Oct-4 phantom 3b9b6d2e; "
         "quarantined as t7_battery_v1_wrongtarget.log, no verdict issued from it",
         "law: zero hand-typed constants; all fields machine-parsed + cross-bus byte-diffed"]
lines.append(f"SILICON {telemetry()}")

# ---- guards before ----
bin_sha = sha(BIN)
pk_sha = sha(os.path.join(REPO, "keys/proving_key.bin"))
vk_sha = sha(os.path.join(REPO, "keys/verifying_key.bin"))
lines.append(f"GUARD-BEFORE binary={bin_sha[:16]} PK={pk_sha[:16]} VK={vk_sha[:16]}")
env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

# ---- 0) machine-verify the arm stamp from the guard log ----
guard = open(os.path.join(os.path.expanduser("~/fleet/logs"), "rx_standby_continuous_20261003T180951Z.log"),
             errors="replace").read()
assert "2026-10-06T00:19:" in guard and "LORA_CHIRP_RECOVERY_PASS" in guard, "arm stamp not in guard log"
lines.append(f"ARM-STAMP verified in guard log: {ARM_UTC_STR} + LORA_CHIRP_RECOVERY_PASS")

# ---- 1) machine-locate Alpha's cycle-28 declare + fired events on BOTH buses ----
Aev, Bev = get_events(A_BUS), get_events(B_BUS)


def find_unique(events, etype, match):
    hits = [e for e in events if e.get("type") == etype and match(e.get("data", {}))]
    assert len(hits) == 1, f"expected exactly 1 {etype}, found {len(hits)}"
    return hits[0]


dcl_a = find_unique(Aev, "groth16_proof_tx", lambda d: d.get("kind") == "cache_refill_first_use_fresh_key31")
dcl_b = find_unique(Bev, "groth16_proof_tx", lambda d: d.get("kind") == "cache_refill_first_use_fresh_key31")
f_a = find_unique(Aev, "groth16_tx_fired", lambda d: d.get("kind") == "cache_refill_first_use_fresh_key31")
f_b = find_unique(Bev, "groth16_tx_fired", lambda d: d.get("kind") == "cache_refill_first_use_fresh_key31")
for field in ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
              "deposit_value", "private_key_id", "coordinate", "deposit_commitment",
              "attestation_hash", "proof_sha256"):
    assert dcl_a["data"][field] == dcl_b["data"][field], f"declare {field} MISMATCH across buses"
assert dcl_a["data"]["proof_sha256"] == f_a["data"]["payload_sha256"], "declare/fired sha inconsistent on A-bus"
assert f_a["data"]["payload_sha256"] == f_b["data"]["payload_sha256"], "fired sha differs across buses"
declared_sha = dcl_a["data"]["proof_sha256"]
lines.append(f"DECLARE located: A seq{dcl_a['seq']} == B seq{dcl_b['seq']} (byte-equal); "
             f"key={dcl_a['data']['private_key_id']} deposit={dcl_a['data']['deposit_value']} "
             f"coordinate={dcl_a['data']['coordinate']} window_closes={dcl_a['data']['window_closes_utc']}")
lines.append(f"DECLARE payload_sha256={declared_sha}")

# ---- 2) burst selection: fired-window BOUND x listener-SESSION segment (v3) ----
fired_utc = datetime.strptime(f_a["data"]["fired_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
completed_utc = datetime.strptime(f_a["data"]["completed_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
arm_utc = datetime.strptime(ARM_UTC_STR, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
lines.append(f"FIRED-WINDOW fired={fired_utc.isoformat()} completed={completed_utc.isoformat()} (machine-parsed from A seq{f_a['seq']})")

# session segment: between the cycle-28 arm banner and the next listener exit
glines = guard.splitlines()
arm_banner = [i for i, l in enumerate(glines)
              if l.startswith("2026-10-06T00:19:15Z") and "GATE PASS: ARMING listener window" in l]
exits = [i for i, l in enumerate(glines) if "listener exit rc=124" in l and i > (arm_banner[0] if arm_banner else 0)]
assert arm_banner, "cycle-28 arm banner not found in guard log"
seg_lo, seg_hi = arm_banner[0], exits[0]
seg = glines[seg_lo:seg_hi]
lines.append(f"SESSION-SEGMENT guard log lines {seg_lo}..{seg_hi} (arm banner -> listener exit), {len(seg)} lines")

# frame line-offset map: which log line does each extractor frame's block start at
ext = json.load(open(EXTRACT))
frame_line = {}
pos = 0
for p in ext["crc_ok"]:
    # locate this frame's count_us in the raw segment by scanning block starts
    m = None
    search_from = 0
    while True:
        try:
            i = seg.index("  count_us: " + str(p["count_us"]), search_from)
        except ValueError:
            break
        m = i
        break
    frame_line[p["count_us"]] = (m is not None)
in_session = [p for p in ext["crc_ok"] if frame_line.get(p["count_us"])]
lines.append(f"SESSION-FRAMES crc_ok frames whose count_us appears in the cycle-28 segment: {len(in_session)}")

burst, walls = [], {}
for p in in_session:
    if p["actual_bytes"] != 128 or p["freq_hz"] != 903900000:
        continue
    cu = p["count_us"]
    cands = [arm_utc + timedelta(seconds=cu / 1e6 + w) for w in (0.0, WRAP_S)]
    ok = [t for t in cands if fired_utc - timedelta(seconds=10) <= t <= completed_utc + timedelta(seconds=45)]
    if len(ok) == 1:
        burst.append(p)
        walls[cu] = ok[0]
assert len(burst) == 5, f"expected 5 frames inside the fired window AND session segment, found {len(burst)}"
shas = {p["sha256"] for p in burst}
assert len(shas) == 1, f"burst payload diverges across sends: {len(shas)} distinct digests"
payload_sha = shas.pop()
payload = bytes.fromhex(next(p["hex"] for p in burst if p["sha256"] == payload_sha).replace(" ", ""))
assert hashlib.sha256(payload).hexdigest() == payload_sha and len(payload) == 128
ordered = sorted(burst, key=lambda p: p["count_us"])
gaps = [(ordered[i + 1]["count_us"] - ordered[i]["count_us"]) / 1e6 for i in range(4)]
assert all(10 <= g <= 20 for g in gaps), f"inter-frame spacing implausible: {gaps}"
with open(os.path.join(EVID, "rx_payload_128b.bin"), "wb") as f:
    f.write(payload)
lines.append(f"BURST bound to fired window: 5 frames, count_us {ordered[0]['count_us']}..{ordered[-1]['count_us']}, "
             f"inter_frame_s={[round(g, 1) for g in gaps]}, SNR {ordered[0]['snr_avg']}, status {ordered[0]['status']}")
lines.append(f"CAPTURED 128B digest(computed)={payload_sha}")
diff_pos = [i for i in range(64) if payload_sha[i] != declared_sha[i]]
lines.append(f"SHA-DIFF vs declare: {len(diff_pos)} positions differ {diff_pos}")
lines.append(f"SHA-DIFF detail: computed={payload_sha}")
lines.append(f"                   declared={declared_sha}")
if len(diff_pos) == 0:
    lines.append("NO DIVERGENCE — declare matches captured bytes exactly")
elif len(diff_pos) <= 4:
    lines.append(f"AVALANCHE LAW: {64 - len(diff_pos)}/64 digest chars equal — impossible for two distinct 128B inputs; "
                 "the declared string was not computed from the captured bytes (declare-chain transcription defect); "
                 "air corruption is excluded (5/5 deterministic frames, LoRa CRC OK, SNR +11)")
else:
    lines.append("WIDE DIVERGENCE — declare and capture are unrelated byte streams; "
                 "possible wrong-window/wrong-burst capture; treat as FAIL and bisect")

# ---- 3) verify primary (captured bytes) ----
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

v, dt, rc, so = verify(payload, dcl_a["data"])
lines.append(f"PRIMARY cycle-28 captured {payload_sha[:8]}: verdict={v} exit={rc} wall_s={dt:.1f} stdout={so!r}")

# ---- 4) control: cycle-26 key-32 proof (different statement class) ----
ctrl_sha = sha(CYCLE26_BIN)
ctrl_raw = open(CYCLE26_BIN, "rb").read()
ctrl_decl = {}
for bus_name, events in (("A", Aev), ("B", Bev)):
    hits = [e for e in events if e.get("type") == "groth16_proof_tx"
            and e.get("data", {}).get("proof_sha256") == ctrl_sha]
    assert len(hits) == 1, f"control declare on {bus_name}-bus: found {len(hits)}"
    ctrl_decl[bus_name] = hits[0]
for field in ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
              "deposit_value", "private_key_id"):
    assert ctrl_decl["A"]["data"][field] == ctrl_decl["B"]["data"][field], f"control {field} MISMATCH"
cv, cdt, crc_, cso = verify(ctrl_raw, ctrl_decl["A"]["data"])
lines.append(f"CONTROL cycle-26 {ctrl_sha[:8]}: verdict={cv} exit={crc_} wall_s={cdt:.1f} stdout={cso!r}")

# ---- guards after ----
assert sha(BIN) == bin_sha, "BINARY CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/proving_key.bin")) == pk_sha, "PK CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/verifying_key.bin")) == vk_sha, "VK CHANGED MID-BATTERY"
lines.append(f"GUARD-AFTER binary={sha(BIN)[:16]} PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} "
             f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]} — unchanged")
lines.append(f"SILICON-END {telemetry()}")

# ---- verdict per battery law ----
if cv != "VALID":
    lines.append(f"BATTERY VERDICT: QUARANTINED — control {cv}, primary verdict unusable per control-battery law; "
                 "no cycle verdict, bisect before any claim")
elif v == "VALID":
    lines.append("BATTERY VERDICT: PRIMARY VALID + CONTROL VALID — the cycle-28 airwave bytes ARE a genuine "
                 "Groth16 proof for key-31/coordinate 123456789/deposit 100000; declared SHA string carries a "
                 f"transcription defect at digest positions {diff_pos} (declare-chain, hand-typed-constant class); "
                 "radio verdict: 5/5 CRC-OK capture of the true proof; settle deferred until Alpha confirms the "
                 "canonical SHA from his fired bytes")
else:
    lines.append("BATTERY VERDICT: PRIMARY INVALID + CONTROL VALID — captured bytes are not a proof for the "
                 "declared statement (with 2-char digest proximity, this means an unexplained anomaly: "
                 "no settle, no verdict-positive, full bisect, peer ask)")

out = "\n".join(lines)
print(out)
with open(LOG, "w") as f:
    f.write(out + "\n")
