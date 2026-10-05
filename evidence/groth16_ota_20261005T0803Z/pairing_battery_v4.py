#!/usr/bin/env python3
"""Pairing battery v4 — statement-class + core-affinity discriminators.

Established today (Oct 5, 08:19-09:02Z):
  - key-31 statement (pub hashes cbe1d4d7..., deposit 100000): bd4c9ab2 INVALID
    3x under disk VK + 1x under seed-42 regen VK; fc816080 INVALID 1x
    (both were committed VALID Oct-4 through 05:2xZ today)
  - key-32 statement (pub hashes 515d79c3..., deposit 100001): 264a8fea VALID 3/3
  - keys sha-guard unchanged; binary unchanged (a0c74748...); throttled=0x0

v4 runs:
  D1: a1706406 (key-31 statement, PROVED TODAY by patched builder, VALID 05:2xZ
      in cycle-19 battery) under disk VK -> did the whole key-31 statement class
      flip, or only the two Oct-4 proofs?
  D2: bd4c9ab2 pinned to each of cores 0..3 via taskset -> per-core defect?
      (a bad L1/L2 SRAM bit yields per-affinity verdicts; software state does not)
"""
import hashlib
import os
import subprocess
import time

EVID = os.path.expanduser("~/fleet/evidence/20261005T0803Z_groth16_ota_daemon_cycle20")
LOG = os.path.join(EVID, "pairing_verify_timed_v4.log")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
K31 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261004T1922Z/rx_payload.bin")  # bd4c9ab2
K31B = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T0442Z/rx_payload.bin")  # a1706406
K31_HASHES = ["cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
              "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
              "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",
              "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005"]

def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256
    return [h[:64], h[64:192], h[192:256]]

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def verify(label, payload, prefix, out, taskset_core=None):
    args = [BIN, "verify", *slices(payload), *K31_HASHES, GATEWAY, "100000", FIRMWARE]
    if taskset_core is not None:
        args = ["taskset", "-c", str(taskset_core)] + args
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
    lines = [f"BATTERY_V4_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
             "D1 statement-class discriminator + D2 core-affinity discriminator"]
    assert sha(K31).startswith("bd4c9ab2")
    assert sha(K31B) == "a1706406ec05b564466dba60bf61c36b28e6ce3983eacc60275031c0a032bea4"

    # D1: a1706406 — same key-31 statement, proved today, VALID at 05:2xZ
    verify("D1 a1706406 (key-31 stmt, proved today, was VALID 05:2xZ)", K31B, None, lines)
    # D2: bd4c9ab2 across cores 0..3
    for core in (0, 1, 2, 3):
        verify(f"D2 bd4c9ab2 pinned core{core}", K31, None, lines, taskset_core=core)

    lines.append(f"BATTERY_V4_DONE={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("V4 COMPLETE", flush=True)

if __name__ == "__main__":
    main()
