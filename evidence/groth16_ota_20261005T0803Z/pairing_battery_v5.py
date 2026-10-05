#!/usr/bin/env python3
"""Pairing battery v5 — final class discrimination, cycle-20 forensics.

Battery v4 established: a1706406 (key-31 statement, PROVED TODAY, committed
VALID 05:2xZ in the cycle-19 battery) now INVALID; bd4c9ab2 INVALID on cores
0/1/2 (core3 result in pairing_verify_timed_v4.log).

v5 pairs, in ONE session:
  - cecbb8b8 (PR#16, FOURTH distinct proof-byte set of the key-31 statement
    class, committed VALID 01:5xZ today) -> class hypothesis test
  - 264a8fea (cycle-20 primary, key-32 statement) -> 4th repeat
If cecbb8b8 INVALID + 264a8fea VALID in the same session minutes apart:
statement-class-correlated flip is airtight, no committed control holds today,
cycle-20 pairing verdict stays QUARANTINED (fail-closed), hardware case opens.
"""
import hashlib
import os
import subprocess
import time

EVID = os.path.expanduser("~/fleet/evidence/20261005T0803Z_groth16_ota_daemon_cycle20")
LOG = os.path.join(EVID, "pairing_verify_timed_v5.log")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
PRIM = os.path.join(EVID, "rx_payload_128b.bin")  # 264a8fea key-32
CEC = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T0148Z/rx_payload.bin")  # cecbb8b8 key-31

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
K31_HASHES = ["cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
              "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
              "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",
              "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005"]
K32_HASHES = ["515d79c3c4a8f85f775b37eb6e0c2b1d335d0f78b34ba7d6a5c7f86f2ab71d0e",
              "507fdd3d109ac0a11cdc7f952893123bd8f893d35579fd3e6075e412a8df4d04",
              "23a2be793fe04545dfffa73da78ade2ae9da1957b10aa9d054b8b5f6129ad11d",
              "3618eed84a884b75539485359a6a9900c132f3d29538acb1acb5ab6d4c04c705"]


def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256
    return [h[:64], h[64:192], h[192:256]]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def verify(label, payload, hashes, deposit, out):
    args = [BIN, "verify", *slices(payload), *hashes, GATEWAY, deposit, FIRMWARE]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items()
                            if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
    dt = time.time() - t0
    line = f"{label}: exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]}"
    out.append(line)
    print(line, flush=True)
    return r.returncode


def main():
    lines = [f"BATTERY_V5_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
             "class discrimination: cecbb8b8 (4th key-31 proof-byte set, committed VALID 01:5xZ) + 264a8fea 4th repeat, one session",
             f"keys sha-guard BEFORE: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}"]
    assert sha(PRIM) == "264a8fea20714a487b38e92634480fcae707c22bf2d2dce6c1c53ec779f9d4e2"
    assert sha(CEC).startswith("cecbb8b8"), sha(CEC)

    c1 = verify("cecbb8b8 (PR#16, key-31 class, committed VALID 01:5xZ today)", CEC, K31_HASHES, "100000", lines)
    verify("264a8fea (cycle-20 primary, key-32 class, repeat #4)", PRIM, K32_HASHES, "100001", lines)

    lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")
    lines.append(f"BATTERY_V5_DONE={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("V5 COMPLETE", flush=True)


if __name__ == "__main__":
    main()
