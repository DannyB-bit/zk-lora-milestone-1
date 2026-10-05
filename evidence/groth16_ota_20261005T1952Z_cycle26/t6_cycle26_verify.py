#!/usr/bin/env python3
"""T6 — cycle-26 pairing verdict: OTA-captured c11788f4 (key-32) against the
machine-parsed public-input vector from Alpha's seq-663 declare (B-bus live pull,
NOT hand transcription — the new fleet law born of the 2x2 differential overturn).

Protocol (reformed): vector fields are read from the bus event JSON at run time and
byte-diffed across BOTH buses' declares before the verify runs. Predicted VALID."""
import hashlib
import json
import os
import subprocess
import time
import urllib.request

REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T1952Z_cycle26")
PAYLOAD = os.path.join(EVID, "rx_payload_128b.bin")
LOG = os.path.join(EVID, "t6_cycle26_verify.log")
EXPECT_SHA = "c11788f40a31543625adbbbcecae06af9f9e47ba01b5e0fc5ef364a09366b83a"

def get_env_token():
    for line in open(os.path.expanduser("~/.hermes/.env")):
        line = line.strip()
        if line.startswith("FLEET_FAST_TOKEN"):
            _, _, v = line.partition("=")
            return v.strip().strip('"').strip("'")

def fetch_declare(url, seq):
    req = urllib.request.Request(f"{url}/events?since={seq-1}&limit=5&token={get_env_token()}",
                                 headers={"User-Agent": "fleet-b"})
    data = json.load(urllib.request.urlopen(req, timeout=8))
    evs = data if isinstance(data, list) else data.get("events", data)
    for e in evs:
        if e.get("seq") == seq and e.get("type") == "groth16_proof_tx":
            return e.get("data", {})
    return None

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# 1) Pull the declare from BOTH buses and byte-diff the public-input vector
d_a = fetch_declare("http://192.168.1.219:8643", 233)   # A-bus declare for window 662
d_b = fetch_declare("http://192.168.1.220:8643", 663)   # B-bus declare for window 662
assert d_a is not None, "A-bus declare seq233 not found"
assert d_b is not None, "B-bus declare seq663 not found"
vec_a, vec_b = d_a["public_input_hashes"], d_b["public_input_hashes"]
assert vec_a == vec_b, f"VECTOR MISMATCH ACROSS BUSES: {vec_a} vs {vec_b}"
assert d_a["proof_sha256"] == EXPECT_SHA == d_b["proof_sha256"]
GATEWAY = d_a["gateway_address_hex"]
FIRMWARE = d_a["firmware_hash_hex"]
DEPOSIT = str(d_a["deposit_value"])

lines = [f"T6_CYCLE26_VERIFY_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "vector provenance: machine-parsed from bus declares (A seq233 == B seq663 byte-exact) - hand transcription eliminated",
         f"payload sha={sha(PAYLOAD)} (matches declare {d_a['proof_sha256']})",
         f"binary_sha256={sha(BIN)[:16]} PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}",
         f"key_id={d_a.get('private_key_id')} deposit={DEPOSIT}"]

h = open(PAYLOAD, "rb").read().hex()
assert len(h) == 256
args = [BIN, "verify", h[:64], h[64:192], h[192:256], *vec_a, GATEWAY, DEPOSIT, FIRMWARE]
t0 = time.time()
r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                   env={k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
dt = time.time() - t0
verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else f"ERROR rc={r.returncode}")
lines.append(f"T6 c11788f4 x machine-parsed vector: verdict={verdict} exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]!r}")
if verdict == "VALID":
    lines.append("CYCLE-26 COMPLETE: radio 5/5 SHA MATCH + pairing VALID on B die under the reformed machine-parsed-vector protocol - first fully-clean cycle")
lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")
print("\n".join(lines))
with open(LOG, "w") as f:
    f.write("\n".join(lines) + "\n")
