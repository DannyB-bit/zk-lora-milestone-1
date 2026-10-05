#!/usr/bin/env python3
"""T5 — re-issue the cycle-24 pairing verdict: OTA-captured 96db35c5 (key-31) against the
CORRECT public-input vector (Alpha's seq229 machine declare), on B silicon, canon recipe.
Predicted: VALID. If VALID, the cycle-24 A->B loop closes end-to-end: radio 5/5 SHA match
+ pairing VALID on the receiving die — with the quarantine lifted by the 2x2 differential
(battery_vector_differential.log, T1-T4)."""
import hashlib
import os
import subprocess
import time

REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T1602Z")
PAYLOAD = os.path.join(EVID, "rx_payload.bin")
LOG = os.path.join(EVID, "t5_cycle24_reissue.log")

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
K31_CORRECT = [
    "cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
    "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
    "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a",
    "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005",
]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

assert sha(PAYLOAD) == "96db35c5594c2c258c09b80a64991153ce7f49dc68b727945f9baa58970faad8", sha(PAYLOAD)
h = open(PAYLOAD, "rb").read().hex()
assert len(h) == 256
args = [BIN, "verify", h[:64], h[64:192], h[192:256], *K31_CORRECT, GATEWAY, "100000", FIRMWARE]

lines = [f"T5_CYCLE24_REISSUE_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
         "payload=96db35c5 (cycle-24 OTA-captured, key-31) x CORRECT vector (Alpha seq229 machine declare)",
         f"binary_sha256={sha(BIN)[:16]} PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}"]
t0 = time.time()
r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                   env={k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
dt = time.time() - t0
verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else f"ERROR rc={r.returncode}")
lines.append(f"T5 96db35c5 x CORRECT vector: verdict={verdict} exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]!r}")
if r.returncode == 0:
    lines.append("CYCLE-24 PAIRING VERDICT RE-ISSUED: VALID on B silicon — radio 5/5 SHA match + pairing VALID, loop closed")
lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")
print("\n".join(lines))
with open(LOG, "w") as f:
    f.write("\n".join(lines) + "\n")
