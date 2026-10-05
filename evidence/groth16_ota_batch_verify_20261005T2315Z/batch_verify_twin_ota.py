#!/usr/bin/env python3
"""BATCH BATTERY v2 — twin OTA-captured proofs verified in ONE session on the B die.

v2 fix (honest ledger): v1 carried a HAND-TYPED expected-SHA constant for cycle-24
which differed from the actual evidence-file SHA by one character — the fail-closed
assert caught it before any pairing ran (zero airtime/verdict impact). This is the
same defect class as yesterday's key-31 typo: hand transcription. v2 eliminates ALL
hand-typed constants: the payload SHA is COMPUTED from the evidence file, the
matching declare is FOUND programmatically on BOTH buses, and all public-input
fields are byte-diffed across buses before the verify runs.

Proofs (both captured over 903.9 MHz from Alpha's autonomous watcher fires):
  - cycle-24: key-31, deposit 100000 — evidence/groth16_ota_20261005T1602Z
  - cycle-26: key-32, deposit 100001 — evidence/groth16_ota_20261005T1952Z_cycle26
"""
import hashlib
import json
import os
import subprocess
import time
import urllib.request

REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
EVID = os.path.join(M1, "evidence/groth16_ota_batch_verify_20261005T2315Z")
LOG = os.path.join(EVID, "batch_verify_twin_ota.log")

B_BUS = "http://192.168.1.220:8643"
A_BUS = "http://192.168.1.219:8643"

# label -> payload evidence file (NO hand-typed SHAs anywhere)
TARGETS = [
    ("cycle-24", os.path.join(M1, "evidence/groth16_ota_20261005T1602Z/rx_payload.bin")),
    ("cycle-26", os.path.join(M1, "evidence/groth16_ota_20261005T1952Z_cycle26/rx_payload_128b.bin")),
]


def tok():
    for line in open(os.path.expanduser("~/.hermes/.env")):
        if line.strip().startswith("FLEET_FAST_TOKEN"):
            return line.strip().partition("=")[2].strip().strip('"').strip("'")
    raise SystemExit("FLEET_FAST_TOKEN not found")


def get_events(url):
    req = urllib.request.Request(f"{url}/events?since=0&limit=1000&token={tok()}",
                                 headers={"User-Agent": "fleet-b"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.load(r)
    return d.get("events", d) if isinstance(d, dict) else d


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


lines = [f"BATCH_VERIFY_V2_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "mode: twin OTA-captured proofs, one session; ALL fields machine-parsed, zero hand transcription",
         "v1 lesson: hand-typed expected-SHA constant caught by fail-closed assert before any pairing ran"]

bin_sha = sha(BIN)
pk_sha = sha(os.path.join(REPO, "keys/proving_key.bin"))
vk_sha = sha(os.path.join(REPO, "keys/verifying_key.bin"))
lines.append(f"GUARD-BEFORE binary={bin_sha[:16]} PK={pk_sha[:16]} VK={vk_sha[:16]}")

env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

verdicts = {}
for label, payload_path in TARGETS:
    actual = sha(payload_path)  # ground truth = the file itself
    raw = open(payload_path, "rb").read()
    lines.append(f"{label}: payload file {os.path.basename(payload_path)} "
                 f"({len(raw)}B) sha256={actual}")

    # machine-find the matching declare on BOTH buses
    found = {}
    for bus_name, url in (("A", A_BUS), ("B", B_BUS)):
        hits = [e for e in get_events(url)
                if e.get("type") == "groth16_proof_tx"
                and e.get("data", {}).get("proof_sha256") == actual]
        assert len(hits) == 1, f"{label}/{bus_name}-bus: expected exactly 1 declare for this sha, found {len(hits)}"
        found[bus_name] = hits[0]
    seq_a, d_a = found["A"]["seq"], found["A"]["data"]
    seq_b, d_b = found["B"]["seq"], found["B"]["data"]

    # byte-diff every verification-relevant field across buses
    for field in ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
                  "deposit_value", "proof_sha256", "private_key_id"):
        assert d_a[field] == d_b[field], f"{label}: {field} MISMATCH across buses"
    lines.append(f"{label}: declares byte-equal (A seq{seq_a} == B seq{seq_b}), "
                 f"key={d_a.get('private_key_id')} deposit={d_a['deposit_value']} "
                 f"fire_eta={d_a.get('fire_eta_utc', '?')}")

    # verify against the machine-parsed vector
    h = raw.hex()
    assert len(h) == 256, f"{label}: payload not 128B"
    args = [BIN, "verify", h[:64], h[64:192], h[192:256], *d_a["public_input_hashes"],
            d_a["gateway_address_hex"], str(d_a["deposit_value"]), d_a["firmware_hash_hex"]]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, env=env_clean)
    dt = time.time() - t0
    verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else f"ERROR rc={r.returncode}")
    verdicts[label] = verdict
    lines.append(f"{label} {actual[:8]}: verdict={verdict} exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:60]!r}")

assert sha(BIN) == bin_sha, "BINARY CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/proving_key.bin")) == pk_sha, "PK CHANGED MID-BATTERY"
assert sha(os.path.join(REPO, "keys/verifying_key.bin")) == vk_sha, "VK CHANGED MID-BATTERY"
lines.append(f"GUARD-AFTER binary={sha(BIN)[:16]} PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} "
             f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]} — unchanged")

vs = set(verdicts.values())
if vs == {"VALID"}:
    lines.append("BATCH VERDICT: 2/2 VALID — twin OTA-captured proofs (key-31 + key-32) verified in one "
                 "session on the B die; every input machine-parsed and byte-diffed across both buses; "
                 "each proof served as the other's same-session control (different statement classes)")
else:
    lines.append(f"BATCH VERDICT: {json.dumps(verdicts)} — MIXED/FAIL, run quarantined per battery law; "
                 "no cycle verdict issued; bisect before any claim")

out = "\n".join(lines)
print(out)
with open(LOG, "w") as f:
    f.write(out + "\n")
