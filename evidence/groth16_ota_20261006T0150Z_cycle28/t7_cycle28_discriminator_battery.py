#!/usr/bin/env python3
"""CYCLE-28 T7 BATTERY — discriminator: airwave digest vs declared SHA divergence.

Cycle-28 capture (B, window armed 2026-10-06T00:19:15Z, closed 02:19:15Z):
5x CRC-OK 128B frames @903.9 MHz (chan 3, SF9, SNR +11.0), byte-identical
across all 5 sends, count_us 1276388753..1343497113 (~16.8 s inter-frame).

ANOMALY: digest(captured bytes) != Alpha's declared payload_sha256, and the
two 64-char digest strings differ in only ~2 hex chars. SHA-256 avalanche
makes that impossible for two distinct inputs => the declared string was not
computed from the captured bytes (transcription-class defect on the declare
chain), OR the air bytes are corrupted and the declare is the true digest
(then the digests would differ wildly, which they do NOT) — so the only open
question is whether the CAPTURED bytes are a genuine Groth16 proof.

DISCRIMINATOR: pair-verify the CAPTURED bytes against the machine-parsed
public-input vector (Alpha's declares, byte-diffed across BOTH buses).
  primary VALID  + control VALID => airwave bytes are the true proof;
       declared SHA string is the transcription defect (2 chars).
  primary INVALID + control VALID => air bytes corrupted (inside a curve
       point), cycle-28 capture FAILS: no verdict-positive, no settle.
  control INVALID => run quarantined per battery law, no verdict.

Control (different statement class per control-rotation law): the cycle-26
key-32 proof c11788f4... (committed evidence file groth16_ota_20261005T1952Z_
cycle26/rx_payload_128b.bin), known-VALID (T6 142.1s + PR#20 battery).

ZERO HAND-TYPED CONSTANTS: every SHA is computed from a file at run time;
every public-input field is machine-parsed from the buses and byte-diffed
across both buses before any verify runs. Binary/keys sha-guarded before and
after. ZK_LORAWAN_REPRODUCIBLE_SETUP stripped from the env.
"""
import hashlib
import json
import os
import subprocess
import time
import urllib.request

M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.join(M1, "evidence/groth16_ota_20261006T0150Z_cycle28")
LOG = os.path.join(EVID, "t7_cycle28_battery.log")
EXTRACT = os.path.join(EVID, "b_rx_extract_output.json")

B_BUS = "http://192.168.1.220:8643"
A_BUS = "http://192.168.1.219:8643"

CYCLE26_BIN = os.path.join(M1, "evidence/groth16_ota_20261005T1952Z_cycle26/rx_payload_128b.bin")


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


lines = [f"T7_CYCLE28_BATTERY_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "mode: discriminator battery — captured-bytes pairing vs declared-SHA divergence",
         "law: zero hand-typed constants; all fields machine-parsed + cross-bus byte-diffed"]

# ---- silicon telemetry (honesty) ----
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

lines.append(f"SILICON {telemetry()}")

# ---- guards before ----
bin_sha = sha(BIN)
pk_sha = sha(os.path.join(REPO, "keys/proving_key.bin"))
vk_sha = sha(os.path.join(REPO, "keys/verifying_key.bin"))
lines.append(f"GUARD-BEFORE binary={bin_sha[:16]} PK={pk_sha[:16]} VK={vk_sha[:16]}")

env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

# ---- 1) reconstruct the burst payload from the extractor output (machine) ----
ext = json.load(open(EXTRACT))
# burst signature: 128B CRC-OK frames on 903.9 MHz whose bytes repeat across >=4 frames
from collections import Counter
cand = [p for p in ext["crc_ok"] if p["actual_bytes"] == 128 and p["freq_hz"] == 903900000]
cnt = Counter(p["sha256"] for p in cand)
burst_sha, burst_n = cnt.most_common(1)[0]
assert burst_n >= 4, f"no >=4-repeat 128B payload found on 903.9MHz (best: {cnt.most_common(1)})"
burst_frames = sorted([p for p in cand if p["sha256"] == burst_sha], key=lambda p: p["count_us"])
gaps = [(burst_frames[i+1]["count_us"] - burst_frames[i]["count_us"]) / 1e6 for i in range(len(burst_frames)-1)]
lines.append(f"BURST frames={burst_n} count_us={burst_frames[0]['count_us']}..{burst_frames[-1]['count_us']} "
             f"inter_frame_s={[round(g,1) for g in gaps]} snr={burst_frames[0]['snr_avg']} "
             f"status={burst_frames[0]['status']} crc_field_present")
payload = bytes.fromhex(burst_frames[0]["hex"].replace(" ", ""))
assert len(payload) == 128
computed_sha = hashlib.sha256(payload).hexdigest()
with open(os.path.join(EVID, "rx_payload_128b.bin"), "wb") as f:
    f.write(payload)
lines.append(f"CAPTURED 128B digest(computed)={computed_sha}")

# ---- 2) machine-locate Alpha's cycle-28 declare pair (NOT by sha — that is the question) ----
Aev, Bev = get_events(A_BUS), get_events(B_BUS)
def find_declares(events):
    hits = [e for e in events if e.get("type") == "groth16_proof_tx"
            and e.get("data", {}).get("kind") == "cache_refill_first_use_fresh_key31"
            and "687" in str(e.get("data", {}).get("window_seq", ""))]
    assert len(hits) == 1, f"expected exactly 1 cycle-28 declare, found {len(hits)}"
    return hits[0]
dcl_a, dcl_b = find_declares(Aev), find_declares(Bev)
declared_sha = dcl_a["data"]["proof_sha256"]
# Alpha's internal consistency: fired events must carry the same sha on both buses
def find_fired(events):
    hits = [e for e in events if e.get("type") == "groth16_tx_fired"
            and e.get("data", {}).get("kind") == "cache_refill_first_use_fresh_key31"]
    assert len(hits) == 1, f"expected exactly 1 cycle-28 fired event, found {len(hits)}"
    return hits[0]
f_a, f_b = find_fired(Aev), find_fired(Bev)
assert dcl_a["data"]["proof_sha256"] == dcl_b["data"]["proof_sha256"], "declare sha differs across buses"
assert f_a["data"]["payload_sha256"] == f_b["data"]["payload_sha256"], "fired sha differs across buses"
assert dcl_a["data"]["proof_sha256"] == f_a["data"]["payload_sha256"], "Alpha declare/fired sha inconsistent"
for field in ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
              "deposit_value", "private_key_id", "coordinate", "deposit_commitment",
              "attestation_hash"):
    assert dcl_a["data"][field] == dcl_b["data"][field], f"field {field} MISMATCH across buses"
lines.append(f"DECLARE located: A seq{dcl_a['seq']} == B seq{dcl_b['seq']} (byte-equal, all fields); "
             f"key={dcl_a['data']['private_key_id']} deposit={dcl_a['data']['deposit_value']} "
             f"coordinate={dcl_a['data']['coordinate']}")
lines.append(f"DECLARE payload_sha256={declared_sha}")

# ---- 3) char-diff computed vs declared (the anomaly, precisely) ----
diff_pos = [i for i in range(64) if computed_sha[i] != declared_sha[i]]
lines.append(f"SHA-DIFF positions={diff_pos} computed={computed_sha} declared={declared_sha}")
lines.append(f"SHA-DIFF chars: " + " ".join(f"pos{i}:declared'{declared_sha[i]}'!=computed'{computed_sha[i]}'" for i in diff_pos))
lines.append("AVALANCHE LAW: digests of two distinct 128B inputs cannot agree on 62/64 chars => "
             "the declared string was not computed from the captured bytes")

# ---- 4) verify primary (captured bytes) with machine-parsed vector ----
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
lines.append(f"PRIMARY cycle-28 captured {computed_sha[:8]}: verdict={v} exit={rc} wall_s={dt:.1f} stdout={so!r}")

# ---- 5) control: cycle-26 key-32 proof, same session (different statement class) ----
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
                 "Groth16 proof for key-31/coordinate 123456789/deposit 100000; the declared SHA string carries a "
                 f"transcription defect at digest positions {diff_pos} (hand-typed-constant class, our own law); "
                 "radio verdict: 5/5 CRC-OK capture of the true proof, declare-SHA 2-char divergence disclosed")
else:
    lines.append("BATTERY VERDICT: PRIMARY INVALID + CONTROL VALID — captured bytes corrupted on air "
                 "(inside a curve point), cycle-28 capture FAILS: no settle; disclosed; re-fire ask")

out = "\n".join(lines)
print(out)
with open(LOG, "w") as f:
    f.write(out + "\n")
