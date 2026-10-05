#!/usr/bin/env python3
"""Pairing battery — cycle-20 groth16_ota daemon-fire (PRIMARY 264a8fea, key 32)
+ CONTROL bd4c9ab2 (PR#14 known-VALID, committed invocation, byte-identical args).
Clean path: Python subprocess list-args (proven 2026-10-05 cycle-19 postmortem),
canon disk keys, ZK_LORAWAN_REPRODUCIBLE_SETUP unset, keys sha-guarded both ends.
"""
import hashlib
import os
import subprocess
import time

EVID = os.path.expanduser("~/fleet/evidence/20261005T0803Z_groth16_ota_daemon_cycle20")
LOG = os.path.join(EVID, "pairing_verify_timed.log")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
PRIM = os.path.join(EVID, "rx_payload_128b.bin")            # 264a8fea (this drill)
CTRL = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261004T1922Z/rx_payload.bin")  # bd4c9ab2

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
# PRIMARY public inputs — A-bus seq217 groth16_proof_tx (key 32, coord 123456790, deposit 100001)
PRIM_HASHES = [
    "515d79c3c4a8f85f775b37eb6e0c2b1d335d0f78b34ba7d6a5c7f86f2ab71d0e",
    "507fdd3d109ac0a11cdc7f952893123bd8f893d35579fd3e6075e412a8df4d04",
    "23a2be793fe04545dfffa73da78ade2ae9da1957b10aa9d054b8b5f6129ad11d",
    "3618eed84a884b75539485359a6a9900c132f3d29538acb1acb5ab6d4c04c705",
]
PRIM_DEPOSIT = "100001"
# CONTROL public inputs — committed cycle-19 battery recipe (bd4c9ab2 known-VALID)
CTRL_HASHES = [
    "cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
    "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
    "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",
    "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005",
]
CTRL_DEPOSIT = "100000"


def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256, f"{path}: {len(h)//2} bytes"
    return [h[:64], h[64:192], h[192:256]]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(label, payload, hashes, deposit, out):
    args = [BIN, "verify", *slices(payload), *hashes, GATEWAY, deposit, FIRMWARE]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items()
                            if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
    dt = time.time() - t0
    out.append(f"{label}: exit={r.returncode} wall_s={dt:.1f}")
    out.append(f"{label}: stdout={r.stdout.strip()[:400]}")
    if r.stderr.strip():
        out.append(f"{label}: stderr={r.stderr.strip()[:400]}")
    print(f"{label}: exit={r.returncode} wall_s={dt:.1f}")
    return r.returncode, dt


def main():
    os.makedirs(EVID, exist_ok=True)
    lines = []
    lines.append(f"BATTERY_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    lines.append("PATH=python subprocess list-args (clean path), CWD=zk-lorawan root, "
                 "ZK_LORAWAN_REPRODUCIBLE_SETUP unset, canon disk keys")
    lines.append(f"keys sha-guard BEFORE: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))} "
                 f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))}")
    print(lines[-1])
    assert sha(PRIM) == "264a8fea20714a487b38e92634480fcae707c22bf2d2dce6c1c53ec779f9d4e2"
    assert sha(CTRL).startswith("bd4c9ab2"), sha(CTRL)
    lines.append(f"PRIMARY payload sha256={sha(PRIM)}")
    lines.append(f"CONTROL payload sha256={sha(CTRL)}")

    p_ex, p_s = run("PRIMARY 264a8fea (cycle-20 daemon-fire, A seq217 declare 08:01:29Z / fired 08:03:10Z)",
                    PRIM, PRIM_HASHES, PRIM_DEPOSIT, lines)
    c_ex, c_s = run("CONTROL bd4c9ab2 (PR#14 known-VALID, committed recipe)",
                    CTRL, CTRL_HASHES, CTRL_DEPOSIT, lines)

    lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))} "
                 f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))}")
    verdict = "PASS" if (p_ex == 0 and c_ex == 0) else "QUARANTINE"
    lines.append(f"BATTERY_VERDICT={verdict} (primary exit {p_ex} / control exit {c_ex})")
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"BATTERY_VERDICT={verdict}")


if __name__ == "__main__":
    main()
